# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Nebius Academy Assignment 1: LLM evaluation pipeline for e-commerce product description generation. The assignment involves generating product descriptions using Nebius Token Factory models, then evaluating them via human scoring and LLM-as-a-judge.

**Due date:** April 5, 2026

## Key Files

- `assingment1_evaluation_instrunctions.md` — Full assignment spec (6 tasks)
- `product_dataset.csv` — 20+ e-commerce products with name, attributes, material, warranty
- `task1_eval_criteria.md` — Rubric definitions (to be filled in for Task 1)
- `.env` — API credentials for Nebius Token Factory
- `assignment_01.xlsx` — Output spreadsheet with generated descriptions and evaluations (created in Task 2)

## Assignment Structure

1. **Task 1** (15pts): Define rubric with good/ok/bad for each criterion (Fluency, Grammar, Tone, Length, Grounding, Latency, Cost) + pass/fail rules
2. **Task 2** (20pts): Generate descriptions using Gemma-2-9b-it or Meta-Llama-3.1-8B-Instruct via Nebius API. Collect `generated_description`, `latency_ms`, `input_tokens`, `output_tokens`. Save to Excel.
3. **Task 3** (10pts): Manual evaluation of 10-15 products, add cost column (USD per call)
4. **Task 4** (15pts): Iterate on prompt/model/params to improve scores
5. **Task 5** (20pts): Build LLM judge using Pydantic structured output. Use the model NOT used in Task 2. Explanation must precede verdict in schema.
6. **Task 6** (20pts): Run judge on all products, compare agreement with human eval, try criterion-by-criterion judging

## API Details

- **Platform:** Nebius AI Studio (Token Factory)
- **Models for generation:** `Gemma-2-9b-it`, `Meta-Llama-3.1-8B-Instruct` (pick one)
- **Judge model:** Use the other model, or upgrade to `Qwen3-30B-A3B-Instruct-2507` if needed
- **API style:** OpenAI-compatible (base URL and key in `.env`)

## Technical Notes

- Structured output via Pydantic schema enforced through the API's structured output support
- In the judge schema, `explanation` must come before `verdict` — this matters because it forces chain-of-thought before the rating
- Cost calculation requires separate input/output token pricing per model
- Latency is measured as end-to-end generation time, not time-to-first-byte
