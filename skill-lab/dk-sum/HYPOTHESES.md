# dk-sum hypotheses log

Tracks, per new variant: the hypothesis it tests, the change made, and (after the next run) the result and lesson learned.

## dk-sum-v2 (parent: dk-sum-v1)
Hypothesis: instructing exact digit-by-digit long addition (align decimal points, pad, add column by column with carries) prevents floating-point-style precision loss on long repeating decimals.
Change made: replaced the bare "add numbers and return the sum" instruction with an explicit long-addition procedure.
Result: confirmed — fixed the 0.999...→1.0 rounding failure v1 had, and all other tests still passed.
Lesson: explicit digit-by-digit procedure text reliably avoids float-style rounding.

## dk-sum-v3 (parent: dk-sum-v1)
Hypothesis: converting to exact integer/fixed-point arithmetic (shift by 10^N, add as integers, shift back) also prevents the same precision loss, as an alternative mechanism to v2's long addition.
Change made: replaced the bare instruction with an integer/fixed-point conversion procedure.
Result: confirmed on the original 11-case suite (11/11), but refuted on the later high-precision 3-addend stress case (test 12) added afterward — v3 dropped precision there (`164.4202` instead of the full value) while v2/v4/v5/v6/v7 did not.
Lesson: the fixed-point approach is less robust than digit-by-digit long addition once more than two addends or very long decimals are involved — don't treat "passed the initial suite" as proof a numeric-precision approach generalizes; keep adding stress cases.

## dk-sum-v4 (parent: dk-sum-v1)
Hypothesis: an explicit "determine required output precision up front, then verify the last digit against true column addition before reporting" procedure fixes the precision-loss failure via a verification step rather than a pure computation-method change.
Change made: replaced the bare instruction with a precision-determination + digit-by-digit computation + explicit final verification step.
Result: confirmed — 12/12 on the full suite including the later stress test.
Lesson: the verification step approach works and generalizes at least as well as v2's long addition.

## dk-sum-v5 (parent: dk-sum-v4)
Hypothesis: v4's full text can be compressed to roughly half its length while keeping the "match decimal places, add digit-by-digit, verify before reporting" core intact, without losing correctness.
Change made: condensed v4's wording, keeping all 4 core steps but trimming explanatory phrasing.
Result: confirmed — 746 chars (43% of v4's 1732), 12/12 on the full suite.
Lesson: v4's original phrasing had significant compressible slack with no correctness cost.

## dk-sum-v6 (parent: dk-sum-v5)
Hypothesis: v5 can be compressed further (toward one-third of v4's length) by dropping the explicit "extract every number" step (implicit in the task) and merging remaining wording, without losing correctness.
Change made: condensed v5 further, dropping the extraction step and merging the precision-matching/digit-by-digit/verify steps into tighter prose.
Result: confirmed — 548 chars (32% of v4), 12/12 on the full suite.
Lesson: the extraction step was genuinely redundant for this model; further compression was still safe.

## dk-sum-v7 (parent: dk-sum-v6)
Hypothesis: the core fix can be compressed to a single sentence (~one-fifth of v4's length) as long as it still names the concrete example (0.999...≠1.0) and the three core moves (match decimals, digit-by-digit, verify), without losing correctness.
Change made: condensed to one instruction sentence naming the example and the three core moves.
Result: confirmed — 354 chars (20% of v4), 12/12 on the full suite. Best accuracy-per-character in the set.
Lesson: for this task, correctness didn't depend on verbose step-by-step scaffolding — a single well-chosen sentence naming the failure mode and the fix sufficed. Brevity gains stopped yielding correctness losses well past the point we might have expected.
