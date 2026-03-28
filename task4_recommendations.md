# Task 4 — Improvement Recommendations

Baseline: Gemma (`google/gemma-2-9b-it-fast`) evaluated in Task 3.

---

## Root Cause Analysis

### Length violations — the #1 failure mode

Most failures across both Gemma and Meta-Llama come from descriptions exceeding 90 words:

| Model | Length failures (evaluated rows) | Examples |
|---|---|---|
| Gemma | 3 fails | Samsung S24 Ultra (98w), MacBook Air M3 (93w), Garmin (92w) |
| Meta-Llama | 1 fail | Garmin (92w), Sonos Move 2 (91w borderline) |

The system prompt says *"Write exactly 50–90 words. Count carefully."* — both models ignore this on products with many attributes.

### The "ok" problem — passing requires >=19 points

Scoring: good=3, ok=2, bad=1 across 7 criteria. Max score = 21. Pass bar = 19.

This means a product with **zero bad ratings can still fail** if it has 3 or more "ok" ratings (e.g., Sony WH-1000XM5: 4 good + 3 ok = 18 = fail). Pushing "ok" to "good" matters just as much as preventing "bad" ratings, especially for `grounding` and `length` which are the most common "ok" criteria.

---

## Experiment 1: Prompt engineering (Rec 2 + 5 + 6 combined)

Three prompt changes tested together as one experiment.

### 1a. Tighten the length instruction

**What changed:** Replace the vague length rule with an explicit rewrite instruction.

**Why I expected it to help:** Models follow instructions more reliably when given a concrete action to take on failure, not just a rule.

**Current:**
```
- Write exactly 50–90 words. Count carefully.
```

**Replace with:**
```
- Your description MUST be 50–90 words. Count every word before you finish.
  If your draft exceeds 90 words, shorten it before outputting.
  If it is under 50 words, expand it.
```

### 1b. Fix hallucination from metadata attribute labels

**What changed:** Clarify in the system prompt how to handle attribute labels that are metadata, not real features.

**Why I expected it to help:** Both models misinterpret attributes like `"battery: long-lasting"` on a water bottle (Stanley Quencher) or `"energy efficient"` on a memory card (SanDisk) as real product features, leading to `grounding: ok` ratings. Fixing this pushes grounding from ok to good, which matters for passing the 19-point bar.

**Add to system prompt:**
```
- Some attributes use labels like battery:, weight:, capacity:, rating:,
  dimensions:, or color options: — these are metadata descriptors, not product
  features. Only mention features that make sense for the product category
  (e.g., a water bottle does not have a battery).
```

### 1c. Add a few-shot example

**What changed:** Add one concrete example of a correct description (65 words, grounded, good tone) directly in the system prompt.

**Why I expected it to help:** A single example anchors both length and tone simultaneously, and is more reliable than instructions alone for small models like Gemma 9B.

**Add to end of system prompt:**
```
Example input:
  Product name: Breville Barista Express Espresso Machine
  Attributes: 15-bar Italian pump, integrated conical burr grinder, steam wand; dimensions: compact
  Material: brushed stainless steel
  Warranty: 2-year limited warranty

Example output:
  Craft cafe-quality espresso at home with the Breville Barista Express. Its
  integrated conical burr grinder delivers fresh grounds straight into the
  portafilter, while the 15-bar Italian pump extracts rich, balanced shots every
  time. The steam wand lets you texture milk for lattes and cappuccinos. Built
  from brushed stainless steel in a compact footprint, it fits neatly on any
  countertop. Backed by a 2-year limited warranty.
```

**New evaluation scores:** *(to be filled after running)*

---

## Experiment 2: Decoding parameters (temperature + top_p)

### 2a. Lower `temperature` from 0.7 to 0.3

**What changed:** Reduce the temperature decoding parameter.

**Why I expected it to help:** Temperature controls the "sharpness" of the probability distribution over the next token. At temperature=1.0, the model uses its raw probabilities. At temperature=0.7, less-likely tokens are somewhat suppressed. At temperature=0.3, the model becomes much more deterministic — it almost always picks the highest-probability next token.

For our task, lower temperature means the model sticks more closely to the patterns it learned during training for instruction-following (word count, factual grounding) rather than exploring creative but off-target phrasings.

**Change in `task2_generate.py`:**
```python
temperature=0.3,  # was 0.7; improves constraint following
```

### 2b. Add `top_p` (nucleus sampling)

**What is `top_p`:** While temperature reshapes the entire probability distribution, `top_p` (nucleus sampling) takes a different approach — it cuts off the distribution entirely. At each step, the model sorts all possible next tokens by probability and only considers the smallest set of tokens whose cumulative probability reaches `top_p`. Everything else is discarded.

For example, with `top_p=0.9`, if the top 50 tokens together account for 90% of the probability mass, the model only samples from those 50 tokens and ignores the remaining thousands. With `top_p=0.5`, it might only consider the top 5-10 tokens.

**How it differs from temperature:**
- **Temperature** makes the full distribution sharper or flatter — every token still has a chance, just with different odds.
- **Top_p** hard-cuts the tail — low-probability tokens are completely eliminated, not just down-weighted.

**Why I expected it to help:** For product descriptions, we want coherent, on-topic text. The "tail" of the distribution contains rare words and unusual phrasings that can lead to hallucinated features or runaway sentence structure. Setting `top_p=0.85` (down from default 1.0) trims these unlikely tokens while still allowing some natural variety in word choice — more variety than very low temperature alone.

**Combined effect with temperature:** Using both `temperature=0.3` and `top_p=0.85` is a belt-and-suspenders approach: temperature makes the distribution sharp (favoring high-probability tokens), and top_p removes the remaining low-probability tail entirely. This double constraint makes instruction-following (especially word count and grounding) more reliable.

**Change in `task2_generate.py`:**
```python
temperature=0.3,
top_p=0.85,  # nucleus sampling: discard tokens outside top 85% probability mass
```

**New evaluation scores:** *(to be filled after running)*

---

## Experiment 3: Post-processing

### 3a. Word count trim

**What changed:** After generation, trim the output at the last sentence boundary that keeps it under 90 words.

**Why I expected it to help:** Eliminates the #1 failure mode entirely, regardless of model behavior. A safety net for when prompt and decoding changes aren't enough.

**How to apply:** Add this function and call it on `generated_description` before saving:

```python
import re

def trim_to_word_limit(text: str, max_words: int = 90) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    truncated = " ".join(words[:max_words])
    match = re.search(r'^(.*[.!?])\s+\S', truncated + " X", re.DOTALL)
    return match.group(1) if match else truncated + "."
```

### 3b. Reduce `max_tokens` from 200 to 130

**What changed:** Lower the `max_tokens` parameter in the API call.

**Why I expected it to help:** 90 words ~ 115-125 tokens. A ceiling of 130 tokens prevents runaway long outputs while leaving a small buffer for punctuation. Acts as a hard API-level constraint that complements prompt-level instructions and the post-processing trim.

**Change in `task2_generate.py`:**
```python
max_tokens=130,  # was 200; 90 words ~ 115-125 tokens
```

**New evaluation scores:** *(to be filled after running)*

---

## Experiment 4: Model switch to Meta-Llama-3.1-8B-Instruct

**What changed:** Switched the generation model from Gemma to Meta-Llama.

**Why I expected it to help:** Meta-Llama shows fewer length failures in the baseline evaluation (1 vs 3 for Gemma among evaluated rows). It also produces slightly different phrasing, which may score better on fluency and tone for some products. The tradeoff is latency: Llama averages ~5,000ms per call vs Gemma's ~1,100ms — roughly 4-5x slower. This will likely push `latency_rating` from good to ok for some products.

**New evaluation scores:** *(filled from Task 3 Meta-Llama evaluation)*

---

## Suggested experiment order

1. **Experiment 4 (model switch)** — Already done, scores available from Meta-Llama Task 3 file.
2. **Experiment 2 (decoding params)** — Quick code change, re-run on Gemma, re-evaluate 10-15 products.
3. **Experiment 1 (prompt engineering)** — Combine with Experiment 2's params for a single improved run.
4. **Experiment 3 (post-processing)** — Apply on top of best-performing experiment as a safety net.

---

## What was NOT recommended

- **Ensembling (combining outputs from two models):** Overkill for a 50-product dataset. Would double API cost and latency for marginal gains.
- **`top_k` parameter:** While Task 4 mentions `top_k`, it's less useful here than `top_p`. `top_k` fixes a hard number of candidate tokens (e.g., top 40) regardless of how the probability is distributed. `top_p` adapts — if the model is confident, it considers fewer tokens; if uncertain, it considers more. For structured text like product descriptions, `top_p` gives better control.
