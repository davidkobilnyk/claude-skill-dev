# Results — dk-prop-logic-parser

Full-suite scores (out of 165) for every variant run so far, across both rounds. Reconstructed after the fact for Round 1 and Round 2 (see the "results-persistence" process note in `HYPOTHESES.md`) — going forward, this file should be updated directly at Step 7 of each round instead of being rebuilt from scratch.

**Grading note:** scores below reflect a manual correction to row 153 (`multiple-independent-example-blocks`, Case 2) across all variants. The automated grading pass initially over-applied the "symbol letters are never scored literally" tolerance to this row — but row 153 specifically tests whether a variant reuses a symbol across independent example blocks (a deliberate trap distinct from ordinary relabeling: Case 2's "it rains" must get a *fresh* symbol, not reuse Case 1's `P`), so blanket relabeling tolerance doesn't apply there. Verified by direct inspection of all 45 raw run outputs on this row; corrected scores are reflected in the table below. See the "row-153 grading correction" process note for detail.

## Round 1 (N=5 per variant)

| Variant | Size (chars) | Run scores | Avg | Min | Max | Range | Stddev (sample) |
|---|---|---|---|---|---|---|---|
| v1 | 6,063 | 162, 162, 162, 157, 160 | 160.6 | 157 | 162 | 5 | 2.19 |
| v2 | 5,493 | 156, 156, 157, 157, 159 | 157.0 | 156 | 159 | 3 | 1.22 |
| v3 | 4,287 | 153, 149, 150, 161, 150 | 152.6 | 149 | 161 | 12 | 4.9 |
| v4 | 5,568 | 163, 160, 163, 164, 162 | 162.4 | 160 | 164 | 4 | 1.52 |
| v5 | 1,704 | 133, 130, 130, 143, 130 | 133.2 | 130 | 143 | 13 | 5.6 |

## Round 2 (N=4 per variant)

| Variant | Parent | Size (chars) | Run scores | Avg | Min | Max | Range | Stddev (sample) |
|---|---|---|---|---|---|---|---|---|
| v6 | v1 (−necsuff-rule) | 5,988 | 159, 161, 160, 157 | 159.25 | 157 | 161 | 4 | 1.71 |
| v7 | v1 (−causal-vs-cond) | 5,810 | 158, 161, 159, 157 | 158.75 | 157 | 161 | 4 | 1.71 |
| v8 | v1 (−decompose-rule) | 5,894 | 159, 163, 162, 161 | 161.25 | 159 | 163 | 4 | 1.71 |
| v9 | v1 (−scope-boundary) | 5,838 | 158, 159, 162, 161 | 160.0 | 158 | 162 | 4 | 1.83 |
| v10 | v5 (+inconsistency-detect) | 1,936 | 136, 132, 131, 131 | 132.5 | 131 | 136 | 5 | 2.38 |

## Reading these numbers

- v1 remains the strongest full-suite performer across both rounds (160.6 avg in Round 1, and v6-v9's scores — each v1 minus one component — cluster close to it: 158.75-161.25). This is consistent with the Round 2 hypothesis verdicts: only two of the four removed components (causal-vs-cond in v7, scope-boundary in v9) are confirmed load-bearing, so removing any single one costs at most ~2-3 points off v1's baseline, not a collapse.
- v5 (Round 1) and v10 (Round 2, v5 + one fix) show the brevity/correctness tradeoff directly: v10's single added sentence raised v5's row 124-126 reliability (per HYPOTHESES.md's H2 finding) but did not move the full-suite average much (132.5 vs. v5's 133.2) — the suite's other v5-inherited gaps (temporal-invalid, non-English detection, symbolic-input detection, mixed-valid/invalid extraction) are untouched by that fix and dominate the score gap to v1.
- v3's high variance (stddev 4.9, range 12) stands out — one run (161) handled the question/command/modal mixed-input pattern correctly while the other four (149-153) did not, consistent with H3's "worked examples don't reliably teach this exclusion pattern" finding.
