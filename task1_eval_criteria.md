# Task 1: Product Description Evaluation Rubric

## 1. Criterion Definitions

| Criterion | Good (3 points) | Ok (2 points) | Bad (1 point) |
| :--- | :--- | :--- | :--- |
| **Fluency** | Smooth, varied sentence structure; flows naturally; no robotic repetition; no two sentences in the description start with the same word. | 1 instance of awkward phrasing, a repeated sentence opener, or a robotic transition. | 3+ awkward phrases, highly repetitive sentence structures, or bullet-point style output. |
| **Grammar** | 0 spelling, punctuation, or grammatical errors. | 1 minor errors (e.g., a missing comma) that do not obscure meaning. | 2+ errors, or any error that makes a sentence difficult to understand. |
| **Tone** | Actively persuasive: uses at least two distinct persuasive techniques (e.g., benefit framing, emotional/aspirational appeal, sensory language, social proof, urgency). | Uses sales-oriented language but relies on only one persuasive technique or describes features without evoking benefit or aspiration (informative but flat). | Dry/robotic/technical-manual style, overly aggressive, or inappropriate. |
| **Length** | Exactly 55–85 words. | 50–54 or 86–90 words. | Outside the range (<50 or >90 words). |
| **Grounding** | Mentions Name, Material, Warranty, AND all structured attributes — woven naturally into sentences, with zero hallucinations or invented specs. | Mentions Name, Material, and Warranty but omits one or more structured attributes; OR includes 1 minor plausible but unstated detail. | Contradicts any provided field, invents specs, or omits more than one of Name/Material/Warranty. |
| **Cost** | Combined input/output cost < $0.00002 per description. | Cost is between $0.00002 and $0.0005 per description. | Cost is > $0.0005 per description. |
| **Latency** | Full response generated in < 5 seconds. | Response generated in 5–10 seconds. | Response takes > 10 seconds. |

## 2. Pass/Fail Decision Logic

A description receives a **Pass** verdict only if it clears both the mandatory filters and the quality threshold.

### A. Go/No-Go Rules (Automatic Failure)
The output is automatically marked as **FAIL** if:
* **Grounding is "Bad"**: Any factual hallucination or contradiction of source data.
* **Length is "Bad"**: Output is less than 40 words or greater than 90 words.
* **Grammar is "Bad"**: Three or more errors, or errors that impede readability.

### B. Cumulative Pass Bar
If all Go/No-Go rules are satisfied, the description must meet this threshold:
* **Minimum Quality**: At least **5 "Good" ratings** across the 7 criteria.
* **Point Threshold**: A minimum total score of **17/21 points**.

---

## 3. Constraints for Generation (Task 2)
* **Word Count**: 50–90 words.
* **Factual Accuracy**: Must include Name, Material, and Warranty fields.
* **Persona**: Friendly, credible sales voice.