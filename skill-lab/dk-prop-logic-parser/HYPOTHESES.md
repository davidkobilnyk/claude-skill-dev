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

## Process note (Round 2, hypothesis-wording review)

**Observation:** H6 was stated as "Does the model get necessary/sufficient-condition direction right without an explicit rule?" — a question, not a falsifiable prediction. Both possible answers are equally consistent with having asked it, so "confirmed/refuted" language technically has nothing to attach to. What actually made H6 function as a testable hypothesis was an unwritten implicit prediction: since the rule was already present in v1 (the leader), the working assumption was that it's there because it's load-bearing, i.e. the real hypothesis was "the necsuff-rule component is necessary; removing it will cause direction errors on rows 130-135." That version is falsifiable, and it's the version the Round 2 data (4/4 clean without the rule) actually refuted.

**Root cause:** the lab's process doesn't currently require a hypothesis to be phrased as a directional prediction before a variant is built to test it — question-form and prediction-form both slip through Step 9 unchallenged.

**Candidate patch to `skill-variant-lab` for Step 13:** at hypothesis-proposal time (Step 9, or wherever H-numbers are first assigned), require each hypothesis to be stated as a falsifiable prediction with a specific expected outcome ("removing X causes Y on rows Z"), not as an open question ("does the model do X without Y?"). A quick litmus test: if both possible results would be reported the same way ("interesting, we learned something"), it isn't yet a hypothesis.

**Status:** Logged for the Step 13 retrospective. Not applied retroactively — H1-H10's existing wording in this document is left as-is; this is a going-forward lesson for how new hypotheses get written starting next round.

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
Result: REFUTED (as a "component is load-bearing" prediction). 4/4 runs at N=4 scored rows 130-135 correctly with no explicit rule present.
Rival explanation considered: could the target rows be unusually easy/leaky (e.g. answerable from the surrounding component-inventory context rather than the model's own necessary/sufficient knowledge)? No — the subagents only ever see the blinded `tests_inputs_only.txt`, never the component inventory or expected answers, so there's no leakage path. A second rival — that v1's other Step 3 bullets implicitly re-teach the direction — was checked against v1's text and found false; no other bullet mentions necessary/sufficient conditions.
Lesson: the `necsuff-rule` component is dead weight in v1 — safe to prune permanently. This is exactly the kind of scaffolding the user's "prune from the leader" strategy (Round 1 process note) was designed to surface.

### dk-prop-logic-parser-v7 (parent: v1)
Hypothesis: H7 — the model needs no explicit rule to avoid treating a completed causal claim ("because X, Y") as a hypothetical conditional.
Change made: removed the `causal-vs-cond` component (the "Because A, B" / "A caused B" bullet in Step 3) — nothing else changed from v1.
Result: CONFIRMED (as a "component is load-bearing" prediction — the opposite of H6/H9's outcome). 4/4 runs missed row 41 ("the engine overheated, so the car stalled" / "X caused Y" phrasing), converting it to a conditional `P→Q` (or similar) instead of the suite's `P∧Q` completed-causation reading. Only 1/4 runs (run1) also missed rows 67-69 ("because X, Y" phrasing) — the other 3/4 got 67-69 right even without the rule.
Rival explanation considered: is row 41's miss actually about causal phrasing, or a side effect of the pronoun back-reference in that scenario (a different, adjacent skill)? Checked v1's Round 1 runs on row 41 (correct 5/5 with the rule present) against v7's 4/4 miss (rule absent) — the only textual difference between v1 and v7 is the removed causal-vs-cond bullet, and row 41's phrasing hasn't changed, so the miss traces cleanly to the removed rule, not the pronoun structure. The scenario-94 blast-radius watch flagged in the pre-run regression note didn't materialize as a distinct failure mode — v7's row 94 outputs were consistent with v1's baseline in all 4 runs.
Lesson: `causal-vs-cond` is genuinely load-bearing and should stay in any future leader — but its necessity is stronger for "X caused Y" pronoun-based phrasing (row 41) than for explicit "because X, Y" phrasing (rows 67-69), where the model partially recovers the right reading from general knowledge even without the rule. A future version of this rule could be tightened to specifically flag the "caused" causal-verb pattern as the highest-risk case, rather than treating all causal phrasings as equally fragile.

### dk-prop-logic-parser-v8 (parent: v1)
Hypothesis: H9 — the model needs no explicit rule to decompose a sentence bundling multiple independent claims into separate atomic propositions.
Change made: removed the `decompose-rule` component (the bundling bullet in Step 3) — nothing else changed from v1.
Result: REFUTED (as a "component is load-bearing" prediction). 4/4 runs at N=4 scored all 6 target rows (46-48, 106-108) correctly, decomposing bundled claims into full `P→(Q∧R)`-style structure with no explicit rule present.
Rival explanation considered: the pre-run regression note flagged that Round 1 data (v4's runs) already showed some models default to bundled decomposition regardless of whether the rule was present — meaning a clean v8 result could reflect a rule-independent tendency rather than genuine non-necessity of the rule. This rival explanation cannot be fully ruled out with this experiment design alone: v8's clean result is consistent with both "the rule was truly unnecessary" and "the model decomposes bundled claims by default regardless of instruction," since there's no arm where the model is pushed toward the wrong (bundled, undecomposed) answer to distinguish the two. Unlike H6/H7's target rows (where the wrong answer is a distinct, unambiguous connective error), decomposition failure would look like a subtler structural miss, and none appeared — but the design can't fully separate "rule unnecessary" from "rule redundant with an even stronger prior."
Lesson: treat H9 as REFUTED-with-a-caveat rather than cleanly refuted. `decompose-rule` looks safe to prune based on this data, but because the regression-risk note's ambiguity concern wasn't resolved by the experiment, this is a weaker confirmation than H6's — a good reminder that "clean null result" and "definitively refuted" aren't always the same thing, and the diagnosticity of a subtractive test depends on whether the two possible wrong answers are actually distinguishable in the output.

### dk-prop-logic-parser-v9 (parent: v1)
Hypothesis: H10 — the model needs no explicit rule to reset symbol scope across independent labeled blocks (e.g. "Example 1: ... Example 2: ...").
Change made: removed the `scope-boundary` component (the block-boundary bullet in Step 2) — nothing else changed from v1.
Result: CONFIRMED (as a "component is load-bearing" prediction). 4/4 runs missed row 153 specifically — reusing symbols from Case 1 into Case 2 instead of resetting scope. Rows 151-152 (also scope-reset scenarios) were unaffected in all 4 runs.
Rival explanation considered: why would only row 153 break while 151/152 don't? Checked the three scenarios' wording — 151 and 152 introduce genuinely new propositions in their second block ("it snows / school is closed", "John comes / Mary comes"), so a fresh legend is needed regardless of any scope-reset rule. Row 153's second block ("Case 2: it rains, it snows") verbatim-repeats wording from a block used elsewhere in the suite, creating a plausible false continuity for the model to latch onto absent an explicit reset instruction — this is a genuine content-level distinction between the rows, not noise, so the CONFIRMED verdict is specific to that failure mode rather than to scope-reset generally.
Lesson: `scope-boundary` is load-bearing, but narrowly — the risk is concentrated in verbatim-repeated-wording block pairs, not scope-reset in general. Worth noting in COMPONENTS.md that this rule's value is disproportionate to its rows-affected count (1 of 3 target rows), since the risk it guards against is specific rather than general.

### dk-prop-logic-parser-v10 (parent: v5)
Hypothesis: H2 — v5's unreliable handling of mid-input symbol redefinition (passed 2/5 runs, failed 3/5 on the identical scenario in Round 1) can be made deterministic with a more concrete rule, without meaningfully eroding v5's brevity advantage.
Change made: added one sentence to v5 stating the `inconsistency-detect` rule explicitly (keep the first meaning of a redefined symbol, mint a new symbol for the second) — nothing else changed from v5.
Result: CONFIRMED. 4/4 runs at N=4 correctly minted fresh symbols on rows 124-126, a clear improvement over v5's Round 1 2/5 pass rate on the identical scenario.
Rival explanation considered: could 4/4 be within the range v5 itself would occasionally hit by chance, given v5's own 2/5 baseline wasn't 0/5? Yes in principle at this small N, but the direction and near-total flip (2/5 → 4/4) plus the mechanism being a direct, on-topic instruction addition (not an unrelated change) makes chance a weak rival; this should still be treated as CONFIRMED-tentative pending N≥20 before calling it fully reliable, per the lab's standing rule.
Lesson: a single concrete sentence closed v5's most severe reliability gap without materially eroding its brevity (character count added is minimal relative to v5's 1,704-char baseline). This directly supports the user's brevity-first framing: v5 plus this one fix may be a stronger brevity/correctness tradeoff than v1's full checklist, especially now that H6 and H9 suggest two of v1's checklist items are prunable anyway.

## Round 2 — Active set

v1, v6, v7, v8, v9, v10 (6, at the cap). v2, v3, v4, v5 retired from the active set this round — their Round 1 data stays on record above; H3 (v3) and H5 (v2) remain deferred, not abandoned, and can return in a future round once budget allows.

**Round 2 run note:** v1 dropped from the actual test launch — it tests none of this round's 5 hypotheses and already has a solid N=5 baseline from Round 1 to compare v6-v9 against, so re-running it would spend budget for no new information. That leaves 5 variants (v6-v10); to fit the 20-subagent concurrency cap in one launch batch, N=4 (not the usual default N=5) is used for this round's exploratory pass.

## Deferred — Round 1

- **v2×v3 merge** (H5 + H3 are disjoint) — deferred: neither variant currently leads; depth-confirming v1/v4 first, and pruning v1, is higher-value this round.
- **Symbol-exhaustion labeling scheme** variance (pure `P1..Pn` vs. domain-prefixed vs. letter-then-subscript) — not a hypothesis worth testing; suite accepts any consistent scheme.
- **v4's bundled-vs-split formula** (`P→(Q∧R)` vs. `P→Q;P→R` on scenarios 40/42) — logically equivalent, not scored as a miss.
