# Hypotheses — dk-prop-logic-parser

## Process note (Round 1, Step 6)

**Observation:** With 5 initial variants at the lab's default N=5 runs/variant, Step 6 needed 25 concurrent subagents, but the harness caps concurrent subagents at 20. The first launch batch got 20 through and the last 5 (v5's runs) failed with "concurrent subagent limit reached," requiring a second launch once slots freed up — an avoidable extra round-trip.

**Root cause:** `skill-variant-lab`'s Step 5 says "generate 3–5 variants" and Step 6 defaults to "N=5" for an exploratory round, but nothing in the skill flags that `variants × N` can exceed the harness's concurrency ceiling, or suggests keeping the product at or under it.

**Fix for future labs:** When starting with 5 variants at N=5 (25 total), either (a) start with 4 variants instead of 5 so `4×5=20` fits in one launch batch, or (b) if 5 variants is preferred, launch in two batches (e.g. 4 variants fully, then the 5th) rather than firing all 25 at once and eating a failed-launch retry. Worth proposing as a small addition to `skill-variant-lab` Step 6 at the Step 13 process retrospective: name the harness's concurrent-subagent ceiling explicitly and suggest sizing `variants × N` against it before the first launch of a round.

**Status:** Logged for the Step 13 retrospective patch-drafting; not yet proposed as a skill edit (that step hasn't been reached — this lab is still on Round 1).
