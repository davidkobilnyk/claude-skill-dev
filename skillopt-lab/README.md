# skillopt-lab

A first trial of Microsoft's [SkillOpt](https://github.com/microsoft/SkillOpt) skill optimizer, driven entirely through the Claude Code CLI (no API key), against two of this repo's existing `skill-lab` test suites. This directory holds everything needed to reproduce the runs plus the run artifacts and a write-up of what happened.

Session: 2026-09-02. SkillOpt pinned at commit `db46cd9` (see `SKILLOPT_COMMIT`).

## Layout

| Path | What it is |
|---|---|
| `apply_overlay.sh` | Clones SkillOpt at the pinned commit, applies the patch, copies the overlay, installs. |
| `overlay/skillopt/envs/csvqa/` | New SkillOpt environment: reads a `skill-lab` style CSV (`input,expected_output,scenario`), runs the target once per row, grades with a pluggable grader. |
| `overlay/skillopt/envs/csvqa/graders.py` | `arith` (numeric normalization, repeating decimals, N/A rows) and `proplogic` (relabeling-invariant structural comparison; see below). |
| `overlay/configs/csvqa/` | Run configs: arithmetic and prop-logic, smoke and full, plus `proplogic_rep.yaml` with repeated gate validation. |
| `overlay/skillopt-core.patch` | Three small changes to SkillOpt itself: register the env in `train.py`/`eval_only.py`, and a `CLAUDE_CHAT_TOOLS` env var so the `claude_chat` backend can pass `--tools ""` (otherwise the target may shell out to Python for arithmetic). |
| `results/<run>/` | Training log, per-step records, candidate skills, gate and test `results.jsonl`, split manifests. Transcripts omitted. |

## How the runs were set up

- Optimizer and target both run through `claude -p` via SkillOpt's `claude_chat` backend. The skill under optimization is passed as an appended system prompt; the trainable state is one markdown document.
- Initial skill = the repo's `v1/SKILL.md` body with frontmatter stripped. A fixed answer-layout block (not editable by the optimizer) tells the target the exact `P=...; Q=... => formula` syntax so answers are machine-gradable.
- Split 4:2:4 by row (train / gate-validation / test), seed 42. Gate accepts a candidate only if its validation hard score strictly exceeds the current one.

## Results

### Smoke runs (Sonnet 5 target, 6 rows per split)

Both suites: 100 % on every row seen, 0 edits accepted. In the arithmetic run the optimizer proposed the same bare-number rule the manual lab found (v1c), but at 100 % validation nothing can show a strict improvement, so it was rejected. Lesson: SkillOpt is inert on a saturated validation set.

### Full prop-logic run (Haiku 4.5 target, Sonnet 5 optimizer)

`results/proplogic_haiku/`. 66 train / 33 val / 66 test rows, 2 epochs × 6 steps, 3 edits per step.

| Step | Batch acc | Edit target (from that batch's failures) | Candidate on val | Gate |
|---|---|---|---|---|
| 1 | 11/11 | none | – | skip |
| 2 | 9/11 | "can" not modal; uniform subscripts; shared-subject clauses | 27/33 | reject |
| 3 | 10/11 | fully symbolic input is valid, echo it | 30/33 (tie) | reject |
| 4 | 10/11 | narrow the implicit-generalization rule | 27/33 | reject |
| 5 | 10/11 | antonym pairs map to `¬P` | 27/33 | reject |
| 6 | 10/11 | inconsistent symbol redefinition handling | 27/33, **fixed its target val row** | reject |
| 7 | 9/11 | (epoch 2, similar) | 27/33 | reject |
| 8–9 | 11/11 | none | – | skip |
| 10–12 | 10/11 | (similar) | ≤30/33 | reject |

Baseline validation 30/33 (0.9091). Final = initial skill. Test score of the initial skill (66 rows, Haiku 4.5): **0.8333** hard accuracy.

The trainer evaluated that *same* initial text on the test set twice (once as the S_0 baseline, once as the best-on-val skill) and got **56/66 (0.8485)** and then **55/66 (0.8333)**. Identical text, different score: that one-row swing on 66 rows is the run-to-run variance the gate had to see through on 33.

### Why nothing was accepted

Every proposed edit was locally sensible and addressed the real failure in its batch. None survived the gate because:

1. **Headroom ≈ noise.** Haiku misses 3 of 33 validation rows on the base text, and its run-to-run variance on the *same* text is also ≈3 rows (the fully-symbolic rows flip between a trivial legend and `INVALID: not in English`). A single-run strict-improvement gate cannot resolve a 1-row real gain inside a 3-row noise band. Step 6 fixed its target row and still lost 30→27.
2. **Reflection only sees the training batch**, so the three persistent validation misses are rarely targeted.
3. **Some validation misses were not fixable by any skill text** (next section).

### Test-case audit

Of 18 rows that ever failed (see the per-row table in the session notes), the three that defined the validation headroom were:

- **r149 (and r148) equivocation** — expected keeps "the spring was cold and clear" as ONE atom, but the skill's own decompose rule says otherwise; the model always gets the actual equivocation point (two senses → two symbols) right. The lab's own notes already called these rows irresolvable. **Test-case defect.**
- **r083 contradiction** — expected `P; ¬P` treating "closed" as `¬open`. A convention the flag itself admits; `P; Q` is defensible. Skill text can state the convention, but the gate should not lean on it.
- **r124 redefinition** — genuine; step 6's edit fixed it.

Grader-side noise also found and fixed for future runs: Haiku sometimes writes a `Note:` line inside the answer tags; the grader now ignores trailing commentary lines.

### Rows where the *expected* output is fine and the v1 text is weak

- Fully-symbolic input (r115–r120): v1 says "not in English" is invalid and also says to adopt given symbols; Haiku resolves the contradiction randomly. This is the main noise source and the fix is step 3's rejected edit.
- "sufficient for" read as a generalization (r134), "can" read as modal (r003), "means" read as `∧` (r035): real, fixable.

## The `proplogic` grader

Deterministic, no LLM. Parses `legend => formulas`, maps the model's symbols onto the expected symbols by definition-text similarity (token Jaccard with a crude stemmer, digits kept), then compares formulas as canonical ASTs (commutative operators sorted, `→` right-assoc, redundant parens dropped). Handles: `INVALID:` rows, independent blocks (`Block1: … Block2: …`), `Premises: … Conclusion: …`, the flagged alternative readings (`∨`/`⊕`, `↔`/`→`, the row-76 lenient reading, `(equivalently …)`), `[note:]`/`[flag:]` suffixes, ASCII connectives, and the `P1∧P2∧...∧P27` ellipsis shorthand. Self-consistent on all 165 expected outputs; 21 perturbation checks (swapped direction fails, relabeling passes, block-scope reuse fails, etc.).

## Prepared but not run: `proplogic_rep.yaml`

Adds `env.gate_repeats: 3` — the csvqa adapter runs every gate evaluation three times and reports per-row mean scores, so the gate compares 99 samples instead of one 33-row draw (same idea as HDSO's paired repeated validation). Tested offline. Before using it, also fix or override rows 148/149 (accept the `P∧Q; R` decomposition) or the headroom stays illusory.

## Takeaways for skill development here

- Automated optimizers need headroom that clearly exceeds target variance; measure both with a no-skill and a repeated-baseline run before optimizing.
- Validate the test suite against the skill's own rules before locking it; a row that contradicts the skill's stated policy is a permanent, un-fixable miss that poisons every gate decision.
- A deterministic, structure-aware grader is worth building; LLM grading noise stacks on target noise.
- SkillOpt's edits were consistently reasonable. The bottleneck in this trial was measurement, not proposal quality.
