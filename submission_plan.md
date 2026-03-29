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

### 2. Remove duplicate code cell ✅

Deleted cell 31 (stray duplicate of `generate_description_v2`). Cell indices shifted by -1 from here onward.

### 3. Tighten AI-sounding text ✅ (partial)

- **Cell 46 (was 47)**: Shortened explanation-before-verdict section. ✅
- **Cell 39 (was 40)**: Skipped — keep as is. ❌
- **Cell 78 (was 79)**: Skipped — keep as is. ❌

### 4. Fix full-run model mismatch ✅

- Fixed cell 63 (§6.1.6): reassigns `JUDGE_MODEL = JUDGE_MODEL_V2` ✅
- Fixed cell 68 (§6.2 full run): explicitly passes `model=JUDGE_MODEL` ✅
- Fixed cell 74 (§6.4 criterion-by-criterion): explicitly passes `model=JUDGE_MODEL` ✅
- Re-ran Tasks 5-6 with Qwen3 ✅

### 7. Update markdown conclusions to match new Qwen3 outputs ✅

| Cell | Section | Issue | Suggested Fix |
|------|---------|-------|---------------|
| 70 (md) | §6.2 Note | Says "only 4 out of 10 pass" — actual output is 25/50 pass | Rewrite: "Full-run pass rate is 50% (25/50). Failures driven by length (19 not-good) and grounding (9 not-good)." |
| 76 (md) | §6.4 Note | Vague, no numbers | Add numbers: "Pass rate 7/10. Length improved (8 good vs mixed), grammar dropped slightly (9/10)." |
| 79 (md) | §6.5 Note | Typo "ctireria"; vague | Fix typo + add numbers: "Crit-by-crit better on length (90% vs 70%) and pass/fail (7/10), but slightly worse on grammar (90% vs 100%) and grounding (50% vs 60%)." |
| 80 (md) | §6.6 Analysis | "The-all-at-once did perform better" awkward; "find tuned" typo | Fix phrasing and typo |
| 0 (md) | Companion files | May need updating for new .xlsx outputs | Verify after above fixes |

### 5. Delete empty trailing cell ✅

Cell 80 — empty markdown cell at end.

### 6. Companion files 💬

- Root-level working files (assignment_01_old.ipynb, task_05_06_judge.ipynb) — exclude from submission?
- task1_eval_criteria.md — already consistent with notebook, no changes needed.
