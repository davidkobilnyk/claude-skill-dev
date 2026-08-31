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

## Depth escalation: dk-arithmetic-v2 to N=20
Per the Step 7 hard rule, no variant can be called "final" or "reliable" below N=20 zero-failure. v2 is the current top-ranked candidate (tied-best correctness, lowest char count) — escalating it to N=20 fresh runs to test whether its clean N=5 record holds at depth, per the project's zero-tolerance failure bar from intake.
Result: CONFIRMED. All 20 fresh runs scored 102/102, zero failures. Combined with Round 1's original N=5 (also 102/102), v2 now has 25/25 clean runs total — it clears the N≥20 zero-failure bar and can legitimately be called reliable (not just "clean at N=5").
Lesson: v2's comprehensive explicit-rules design holds up at depth with no cracks appearing between N=5 and N=25 — worth noting since this lab has previously seen small samples look perfect and then crack at depth (per skill-variant-lab's own guidance). v2b (identical text minus one rule) is the natural next depth-escalation candidate, since it already matches v2 at N=5 and is now the brevity leader.
