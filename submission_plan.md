# Submission Cleanup Plan

## Status Legend: ✅ Done | 🔄 In Progress | 💬 Discussing | ⬚ Todo

---

### 1. Fix typos and spelling errors ✅

| Cell | Fix |
|------|-----|
| 5 (md) | "go/on rules andc the pass bar" → "go/no-go rules and the pass bar" |
| 8 (code) | "You are a work for" → "You work for"; double-space fix |
| 33 (md) | "temprature" → "temperature" |
| 38 (code) | "You are a work for" → "You work for" |
| 40 (md) | arbirtary, reasnoable, imporved, signfinant, artirary |
| 42 (md) | trailing 'a' on model name; "not use" → "not used" |
| 63 (md) | "agrred" → "agreed" |
| 67 (md) | intermidate, strated, temprature, tempature, explantion |
| 75/76 (code) | MANAUAL_EVALUATED_PRODUCTS → MANUAL_EVALUATED_PRODUCTS |
| 79 (md) | resultoing, espcially, Chossing, Strating, temprature, meaningfull, accurtae, critcial, conside, criteria's |

### 2. Remove duplicate code cell 💬

Cell 31 is an exact copy of cell 34 (same `generate_description_v2` function). Replace with a comment or delete?

### 3. Tighten AI-sounding text 💬

- **Cell 47**: Explanation-before-verdict section — verbose with numbered list. Shorten?
- **Cell 40**: Informal commentary ("the new prompt really improved!!", "cost is not really significant"). Clean up?
- **Cell 79**: Production recommendation list — rewrite to be more professional?

### 4. Fix narrative consistency (full-run model mismatch) 💬

Full run (cell 69) and criterion-by-criterion (cell 75) use Llama 8B by default, but section 6.1.6 showed Qwen3 is much better (92% vs 24% agreement). Results are saved — can't re-run. Options:
- Add notes explaining the mismatch
- Update cell 0 companion file descriptions (currently imply Qwen3)
- Rewrite cell 71 (vague "Note!") with proper explanation

### 5. Delete empty trailing cell ✅

Cell 80 — empty markdown cell at end.

### 6. Companion files 💬

- Root-level working files (assignment_01_old.ipynb, task_05_06_judge.ipynb) — exclude from submission?
- task1_eval_criteria.md — already consistent with notebook, no changes needed.
