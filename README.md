# Assignment 1 — LLM Evaluation

Nebius Academy: hands-on LLM evaluation pipeline for e-commerce product description generation.

## Setup

Requires [uv](https://github.com/astral-sh/uv).

```bash
uv sync
```

Copy `.env` and fill in your Nebius API key:

```
NEBIUS_API_KEY=your_key_here
```

---

## Tasks

### Task 1 — Define the rubric
Edit `task1_eval_criteria.md` with your good/ok/bad definitions for each criterion and pass/fail rules. No script needed.

### Task 2 — Generate descriptions
Runs the generation model on every product in `product_dataset.csv` and saves results to `assignment_01.xlsx`.

```bash
# Default (Meta-Llama-3.1-8B-Instruct → assignment_01.xlsx)
uv run python task2_generate.py

# Override model
uv run python task2_generate.py --model meta-llama/Meta-Llama-3.1-8B-Instruct

# Override output file
uv run python task2_generate.py --output my_results.xlsx

# Use Gemma
uv run python task2_generate.py --model google/gemma-2-9b-it-fast --output assignment_01_gemma.xlsx

# Both
uv run python task2_generate.py --model Qwen/Qwen3-30B-A3B-Instruct-2507 --output my_results.xlsx
```

**Valid model names:**
- `meta-llama/Meta-Llama-3.1-8B-Instruct`
- `google/gemma-2-9b-it-fast`
- `Qwen/Qwen3-30B-A3B-Instruct-2507`

**Output:** `assignment_01.xlsx` (or custom name) — product info, generated descriptions, latency/token counts, blank rubric columns ready for Task 3.

### Task 3 — Manual evaluation
Open `assignment_01.xlsx` and:
1. Add a `cost` column (USD) using input/output token counts and model pricing.
2. Rate 10–15 products on each criterion (good/ok/bad) using the Task 1 rubric.
3. Fill in `final_score` (pass/fail) per your pass bar and go/no-go rules.

No script needed.

### Task 4 — Improvement cycle
*(Coming soon)* Iterate on prompt, model, or decoding params and re-evaluate.

### Task 5 — Judge model
*(Coming soon)* Build an LLM-as-a-judge using Pydantic structured output.

### Task 6 — Run and analyze the judge
*(Coming soon)* Full judge run, agreement analysis vs. human scores.
