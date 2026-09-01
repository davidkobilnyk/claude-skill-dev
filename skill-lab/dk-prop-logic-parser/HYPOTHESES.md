# Hypotheses — dk-prop-logic-parser

## Process note (Round 1, Step 6)

**Observation:** With 5 initial variants at the lab's default N=5 runs/variant, Step 6 needed 25 concurrent subagents, but the harness caps concurrent subagents at 20. The first launch batch got 20 through and the last 5 (v5's runs) failed with "concurrent subagent limit reached," requiring a second launch once slots freed up — an avoidable extra round-trip.

**Root cause:** `skill-variant-lab`'s Step 5 says "generate 3–5 variants" and Step 6 defaults to "N=5" for an exploratory round, but nothing in the skill flags that `variants × N` can exceed the harness's concurrency ceiling, or suggests keeping the product at or under it.

**Fix for future labs:** When starting with 5 variants at N=5 (25 total), either (a) start with 4 variants instead of 5 so `4×5=20` fits in one launch batch, or (b) if 5 variants is preferred, launch in two batches (e.g. 4 variants fully, then the 5th) rather than firing all 25 at once and eating a failed-launch retry. Worth proposing as a small addition to `skill-variant-lab` Step 6 at the Step 13 process retrospective: name the harness's concurrent-subagent ceiling explicitly and suggest sizing `variants × N` against it before the first launch of a round.

**Status:** Logged for the Step 13 retrospective patch-drafting; not yet proposed as a skill edit (that step hasn't been reached — this lab is still on Round 1).

## Process note (Round 1, post-Step 8)

**Observation:** After seeing v5 (leanest, 1,704 chars) score last on correctness, the user clarified they weight brevity more heavily than the lab's default ranking rule does ("correctness primary, brevity only as tiebreaker"). They also proposed a different search strategy than the lab defaults to: instead of only building up from weak variants (adding missing components until they catch up), prune down from the strong leader (v1) one component at a time to find the true minimum necessary set — directly testing which of v1's components are load-bearing vs. safely droppable, rather than inferring it from v5's gaps.

**Why this wasn't already surfaced:** `text-principles.md` already states the general principle ("don't assume scaffolding is load-bearing... the only way to know is a targeted subtractive variant"), and Step 11 already permits proposing a leaner alternative to the current leader. But nothing in the lab's default flow *prompts* subtractive-from-the-leader experiments proactively — Step 9's default framing is additive (fix a diagnosed miss), and pruning-the-winner only came up because the user raised it after seeing the results, not because the process suggested it.

**Adjustment going forward:** Step 9 for this round will include pruning variants built from v1 (the current leader), each removing exactly one narrow-scope component (per the one-hypothesis-per-variant rule), to directly test what v1 actually needs vs. what's dead weight — alongside the standard additive fixes for v2/v3/v5's diagnosed misses.

**Candidate patch to `skill-variant-lab` for Step 13:** Step 9 or Step 11 could explicitly prompt "propose at least one subtractive-from-the-leader variant per round, not only additive fixes for laggards" — flag for the retrospective.

## Step 8 findings (Round 1)

- **H1 (CONFIRMED):** `symbolic-detect` is load-bearing. v5 (lacks it) failed all 6 already-symbolic-input rows (scenarios 40-44) in all 5/5 runs; v1-v4 (have it) never missed these.
- **H2 (CONFIRMED):** `inconsistency-detect` is load-bearing but v5's one-line version is unreliable — passed 2/5 runs, failed 3/5 on the identical scenario (124-126), vs. 5/5 correct for v1-v4's fuller prose treatment.
- **H3 (CONFIRMED, tentative):** v3's worked examples don't teach "exclude only the bad sentence" for question/command/modal mixes (scenarios 79-80, 91-93, 100-105) — wholesale-INVALID in 4/5 runs, correct partial-conversion in 1/5. No worked example demonstrates this exact exclusion pattern.
- **H4 (CONFIRMED):** v1 and v4's checklists both list "could" as a disqualifying modal word, causing false-positive rejection of "he couldn't bear the pain" (scenario 150, near-miss-false-paraphrase-trap analog) in most runs of both variants.
- **H5 (new):** v2's principle-based validity framing never mentions language, so it converts non-English input (scenarios 94-96) instead of returning INVALID in ~5/5 runs, unlike v1/v3/v4/v5's explicit checklist item.

**Merge-opportunity scan:** v2's H5 gap and v3's H3 gap are disjoint from each other — a v2×v3 merge is a candidate, but deferred (see below) since neither currently leads. v1 and v4's misses overlap (both hit H4) — not a merge candidate.

## Process note (Round 1, pre-Round-2 hypothesis selection)

**Observation:** When selecting H6/H7/H9/H10 (four subtractive tests, each removing one different component from v1) for the same round, a mutual-informativeness check surfaced two distinct correlations the lab's process doesn't currently prompt for:
1. A shared meta-question — each result also updates the prior on "is v1 over-specified in general," not just on that one component, so the four aren't fully independent bits of evidence even though each targets a genuinely different sub-skill.
2. A shared structural confound — all four remove one bullet from the same list in the same document; if removing *any* bullet changes how the model weighs the remaining ones (a recency/attention effect independent of content), a uniform "no regression" result across all four would be ambiguous between "none of these rules were load-bearing" and "the confound, not the content, explains the null result."

**Candidate patch to `skill-variant-lab` for Step 13:** Add a mutual-informativeness/structural-confound check as part of Step 9's next-gen proposal step whenever multiple subtractive variants share the same parent and document region — and, when a batch of same-parent subtractive tests comes back uniformly null, flag that as ambiguous (confound vs. genuine non-necessity) rather than treating it as a clean confirmation that the components were unnecessary.

**Status:** Logged for Step 13; not yet applied as a mitigation this round (accepted as a known interpretive risk for the current H6/H7/H9/H10 batch rather than redesigned around).

## Round 2 — Regression risk notes (pre-run)

- **v7 (H7):** the causal-vs-conditional bullet's blast radius is wider than its 4 "home" rows (scenario 41, 67–69) suggest — scenario 94 (the French non-English row, "il pleut, donc...") also depends on the same causal-claim logic in several Round 1 runs. Watch row 94 in v7's results, not just its named target rows.
- **v8 (H9):** even with the decomposition rule present, Round 1 data (v4's runs) showed some models default to a bundled `P→(Q∧R)` form on scenario 40/42-shaped sentences regardless. A clean result on v8's target rows (46–48, 106–108) may not cleanly confirm or refute the rule's necessity if the underlying tendency is partly rule-independent.

## Round 2 — New variants

### dk-prop-logic-parser-v6 (parent: v1)
Hypothesis: H4 was not selected for this round — v6 instead tests H6 (see Step 8 findings above): the model needs no explicit rule to get necessary/sufficient-condition direction right, since this is a very commonly-taught construction it may already handle from general capability.
Change made: removed the `necsuff-rule` component (the "A is necessary for B" / "A is sufficient for B" bullets in Step 3) — nothing else changed from v1.
Result: (fill in after the next run)
Rival explanation considered: (fill in after the next run)
Lesson: (fill in after the next run)

### dk-prop-logic-parser-v7 (parent: v1)
Hypothesis: H7 — the model needs no explicit rule to avoid treating a completed causal claim ("because X, Y") as a hypothetical conditional.
Change made: removed the `causal-vs-cond` component (the "Because A, B" / "A caused B" bullet in Step 3) — nothing else changed from v1.
Result: (fill in after the next run)
Rival explanation considered: (fill in after the next run)
Lesson: (fill in after the next run)

### dk-prop-logic-parser-v8 (parent: v1)
Hypothesis: H9 — the model needs no explicit rule to decompose a sentence bundling multiple independent claims into separate atomic propositions.
Change made: removed the `decompose-rule` component (the bundling bullet in Step 3) — nothing else changed from v1.
Result: (fill in after the next run)
Rival explanation considered: (fill in after the next run)
Lesson: (fill in after the next run)

### dk-prop-logic-parser-v9 (parent: v1)
Hypothesis: H10 — the model needs no explicit rule to reset symbol scope across independent labeled blocks (e.g. "Example 1: ... Example 2: ...").
Change made: removed the `scope-boundary` component (the block-boundary bullet in Step 2) — nothing else changed from v1.
Result: (fill in after the next run)
Rival explanation considered: (fill in after the next run)
Lesson: (fill in after the next run)

### dk-prop-logic-parser-v10 (parent: v5)
Hypothesis: H2 — v5's unreliable handling of mid-input symbol redefinition (passed 2/5 runs, failed 3/5 on the identical scenario in Round 1) can be made deterministic with a more concrete rule, without meaningfully eroding v5's brevity advantage.
Change made: added one sentence to v5 stating the `inconsistency-detect` rule explicitly (keep the first meaning of a redefined symbol, mint a new symbol for the second) — nothing else changed from v5.
Result: (fill in after the next run)
Rival explanation considered: (fill in after the next run)
Lesson: (fill in after the next run)

## Round 2 — Active set

v1, v6, v7, v8, v9, v10 (6, at the cap). v2, v3, v4, v5 retired from the active set this round — their Round 1 data stays on record above; H3 (v3) and H5 (v2) remain deferred, not abandoned, and can return in a future round once budget allows.

## Deferred — Round 1

- **v2×v3 merge** (H5 + H3 are disjoint) — deferred: neither variant currently leads; depth-confirming v1/v4 first, and pruning v1, is higher-value this round.
- **Symbol-exhaustion labeling scheme** variance (pure `P1..Pn` vs. domain-prefixed vs. letter-then-subscript) — not a hypothesis worth testing; suite accepts any consistent scheme.
- **v4's bundled-vs-split formula** (`P→(Q∧R)` vs. `P→Q;P→R` on scenarios 40/42) — logically equivalent, not scored as a miss.
