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

## Deferred — Round 1

- **v2×v3 merge** (H5 + H3 are disjoint) — deferred: neither variant currently leads; depth-confirming v1/v4 first, and pruning v1, is higher-value this round.
- **Symbol-exhaustion labeling scheme** variance (pure `P1..Pn` vs. domain-prefixed vs. letter-then-subscript) — not a hypothesis worth testing; suite accepts any consistent scheme.
- **v4's bundled-vs-split formula** (`P→(Q∧R)` vs. `P→Q;P→R` on scenarios 40/42) — logically equivalent, not scored as a miss.
