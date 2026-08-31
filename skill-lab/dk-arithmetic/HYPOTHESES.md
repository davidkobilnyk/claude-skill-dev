# Hypotheses — dk-arithmetic

## Round 1 (N=5, all 5 initial variants)

Results: v1 avg 97.80 / min 96 / 100% failure rate / 467 chars. v2, v3, v4, v5 all scored 102/102 on every run (0% failure rate) at N=5, with char counts 2794 / 6606 / 3133 / 7163 respectively.

Ranking (correctness primary, brevity tiebreaker among the tied top four): **v2 > v4 > v3 > v5 > v1**.

Observations feeding the round-2 hypotheses below:
- v1's only misses were rows 79-81 ("single number, no operator") and 82-84 (repeating-decimal division) — exactly the two scenario categories where v1 has no explicit component addressing them.
- v1 answered all 3 injection-shaped rows (100-102) correctly in all 5 runs despite having no `injection-immunity-rule` — suggesting that component may not be load-bearing in v2-v5 either.
- v3 (`code-execution`) and v4 (`worked-example` + `verification-recompute`) matched v2's score while costing 2.4x and 1.1x more characters, with no visible correctness benefit at this N.

## dk-arithmetic-v1b (parent: dk-arithmetic-v1)
Hypothesis: v1's misses on rows 82-84 (repeating-decimal division) are caused specifically by the missing `repeating-decimal-format-rule` — adding only that one rule to v1's otherwise-minimal text should fix those rows without needing any of v2's other rules.
Change made: added `repeating-decimal-format-rule` (the same sentence used in v2) to v1's text. No other change.
Result: CONFIRMED. N=5: avg 99.0, rows 82-84 correct in 5/5 runs; rows 79-81 (untouched) still missed in 5/5, exactly as expected since that rule wasn't added.
Lesson: a single, precisely-targeted sentence can fully fix an isolated miss cluster without any of the surrounding structure v2 has (no `parse-then-eval-split`, no other rules needed). Miss clusters really do map 1:1 to missing rules when the rest of the model's behavior is otherwise sound.

## dk-arithmetic-v1c (parent: dk-arithmetic-v1)
Hypothesis: v1's misses on rows 79-81 (bare number, no operator) are caused specifically by the model not recognizing a lone number as "arithmetic to compute," triggering the no-expression fallback. Adding an explicit `bare-number-rule` should fix those rows.
Change made: added a new component `bare-number-rule` — one sentence stating that a single number with no operator is itself the expression to output, distinct from the no-expression case.
Result: CONFIRMED. N=5: rows 79-81 correct in 5/5 runs. Rows 82-84 (untouched) still missed the intended fraction-plus-repeating-decimal format in 4/5 runs (one run happened to phrase a compatible repeating notation on its own), consistent with that rule not being present.
Lesson: same pattern as v1b — one targeted sentence, one fixed miss cluster, no side effects on the rest of the suite.

## dk-arithmetic-v2b (parent: dk-arithmetic-v2)
Hypothesis: `injection-immunity-rule` is not load-bearing — v1 handled all injection-shaped test rows correctly with no such rule, suggesting the model already resists this kind of embedded-instruction redirection by default. Removing the rule from v2 should not cost any correctness, while reducing size.
Change made: removed the `injection-immunity-rule` sentence from v2's Step 1. No other change.
Result: CONFIRMED. N=5: 102/102 on every run, identical to v2's own record — all 3 injection-shaped rows (100-102) still answered correctly in all 5 runs with the rule removed. v2b is now the leanest variant with a perfect record (2,527 chars vs. v2's 2,794).
Lesson: not every plausible-sounding safety rule is actually load-bearing for a given model/task — the model already resists this specific injection pattern by default. Confirmed by subtraction, not just by v1's absence of the rule (different variant, more confounds), which is why this component-isolation test was worth running on v2 directly. v2b now becomes the new brevity-ranked leader over v2, tied on correctness.

## dk-arithmetic-v1d (parent: dk-arithmetic-v1b + dk-arithmetic-v1c, combined)
Note: this variant deliberately combines two components (`repeating-decimal-format-rule` + `bare-number-rule`) in one step, at the user's explicit request, rather than following the lab's default one-hypothesis-per-variant rule. The user is specifically interested in how far a very short SKILL.md (v1's minimal style, extended with just the two smallest fixes) can go on correctness.
Hypothesis: since v1b and v1c each independently and fully fixed their respective miss cluster with no side effects on the other rows, combining both additions onto v1 should fix both miss clusters simultaneously and produce a 102/102 result, while staying far shorter than v2/v2b (662 + 670 - v1's base ≈ 865 bytes expected, vs. v2b's 2,527).
Change made: v1's text plus both the `repeating-decimal-format-rule` sentence (from v1b) and the `bare-number-rule` sentence (from v1c). No other changes — no `parse-then-eval-split`, no other v2-style rules.
Result: CONFIRMED, and decisively. At N=20, v1d scored 102/102 on every single run (0% failure rate) at only 863 characters — matching the top-tier reliability of v3 (6,606 chars) and v5 (7,163 chars) at roughly 13% of the file size, and using ~13% fewer tokens per run (47,527 avg vs. 54,349 for v3 and 53,666 for v5).
Lesson: for this task, two small targeted rules were sufficient to reach the same reliability ceiling as much heavier designs (code-execution, primary/fallback duplication, or the full v2-style rule set). Neither `parse-then-eval-split`'s structural scaffolding nor `code-execution`'s mechanical precision guarantee bought any measurable correctness benefit over v1d's minimal-plus-two-fixes approach on this test suite — brevity was essentially free here. v1d is now the overall lineage leader, ahead of v2b (2,527 chars).

## Round 3: v1d vs. v3 vs. v5 at N=20, with token-count tracking
At the user's request: ran the new `v1d` combination variant against `v3` (code-execution) and `v5` (primary/fallback) at N=20 each (60 runs total), with average per-run token consumption added to the Step 7 results table (not tracked in Rounds 1-2). Result: all three variants scored a perfect 102/102 across all 20 runs each — see the `v1d` entry above for the comparative token/size analysis.

## Depth escalation: dk-arithmetic-v2 to N=20
Per the Step 7 hard rule, no variant can be called "final" or "reliable" below N=20 zero-failure. v2 is the current top-ranked candidate (tied-best correctness, lowest char count) — escalating it to N=20 fresh runs to test whether its clean N=5 record holds at depth, per the project's zero-tolerance failure bar from intake.
Result: CONFIRMED. All 20 fresh runs scored 102/102, zero failures. Combined with Round 1's original N=5 (also 102/102), v2 now has 25/25 clean runs total — it clears the N≥20 zero-failure bar and can legitimately be called reliable (not just "clean at N=5").
Lesson: v2's comprehensive explicit-rules design holds up at depth with no cracks appearing between N=5 and N=25 — worth noting since this lab has previously seen small samples look perfect and then crack at depth (per skill-variant-lab's own guidance). v2b (identical text minus one rule) is the natural next depth-escalation candidate, since it already matches v2 at N=5 and is now the brevity leader.
