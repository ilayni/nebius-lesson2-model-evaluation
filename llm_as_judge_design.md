# LLM-as-Judge Design Summary

## Model Choice

- **Judge model:** `meta-llama/Meta-Llama-3.1-8B-Instruct` — the model NOT used for generation (Task 2 used Gemma)
- Fallback option: `Qwen/Qwen3-30B-A3B-Instruct-2507` if the 8B model struggles as judge
- Model is configurable via a single `JUDGE_MODEL` variable

## Criteria Evaluated by Judge

The judge evaluates 5 text-quality criteria: **Fluency, Grammar, Tone, Length, Grounding**.

Cost and Latency are excluded — they are measured programmatically from the generation API response, not by the judge.

## Schema Design: Explanation Before Verdict

Each criterion returns a Pydantic-enforced structure:

```python
class CriterionResult(BaseModel):
    explanation: str   # reasoning FIRST
    verdict: Literal["good", "ok", "bad"]
```

**Why this ordering matters:** LLMs generate tokens left-to-right. Placing `explanation` before `verdict` forces the model to reason through the rubric before committing to a rating. This is schema-level chain-of-thought — it reduces snap judgments and improves consistency.

## Grounding Requires Source Data

The judge **must** receive the original product info (name, attributes, material, warranty) alongside the generated description. Without source data, the judge cannot detect hallucinations or omitted attributes. The user message is structured as:

```
═══ SOURCE DATA ═══
Product Name: ...
Attributes: ...
Material: ...
Warranty: ...

═══ GENERATED DESCRIPTION ═══
...
```

## Two Judging Modes

1. **All-criteria-at-once** — one API call per product, evaluating all 5 criteria. Output: `task_06_all_criteria.xlsx`
2. **Criterion-by-criterion** — one API call per criterion per product (5 calls per product). Output: `task_06_product_criteria.xlsx`

Criterion-by-criterion judging isolates each evaluation so one criterion's assessment cannot bleed into another (cross-criterion contamination).

## Structured Output via Nebius API

Uses Pydantic schemas with:

```python
response_format={
    "type": "json_schema",
    "json_schema": MyModel.model_json_schema(),
}
```

Response comes back as JSON string in `response.choices[0].message.content` — parsed with `json.loads()`.

## Pass/Fail Logic

Same rules from Task 1, combining 5 judge verdicts + 2 programmatic ratings (cost, latency):

- **Auto-fail (go/no-go):** Grounding bad, Length bad, or Grammar bad
- **Cumulative pass bar:** >= 5 "good" ratings across all 7 criteria AND total score >= 17/21

## Key Design Decisions

- `temperature=0.0` for deterministic, reproducible judge output
- `time.sleep(0.5)` between API calls to avoid rate limiting
- Error handling fills failed calls with `verdict="bad"` so the pipeline doesn't break
- The full rubric text is embedded in the system prompt — best practice is to provide the schema both in the prompt and as `json_schema` parameter
