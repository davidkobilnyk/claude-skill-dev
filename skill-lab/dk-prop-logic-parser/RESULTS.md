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

## Round 3 (N=5 per variant) — target-row pass rates, not full-suite scores

Round 3's four variants are single-hypothesis diagnostic tests (v11, v12, v13 each change one narrow, well-isolated thing; v14 is a compound-hypothesis test), so — consistent with how Round 2's hypothesis verdicts were actually established — the informative number is the target-row pass rate, not a full 165-row grade. A clean full-suite score wouldn't add diagnostic power here and wasn't computed this round.

| Variant | Parent | Hypothesis | Target rows | Pass rate (N=5) |
|---|---|---|---|---|
| v11 | v3 (+5th worked example) | H3 | 91-93, 100-105 (9 rows) | 5/5 clean; adjacent row 81 (79-80 family) correct in 4/5 |
| v12 | v1 (+paraphrase-merge bullet) | H11 | 34 (primary); 109-111 (check) | 5/5 row 34 fixed; 5/5 no over-merge on 109-111 |
| v13 | v1 (tightened causal-vs-cond) | H18 | 41 (primary); 67-69, 40/42 (check) | 5/5 row 41 held; 5/5 rows 67-69 held; **2/5 new regression on rows 40/42** |
| v14 | v2 × v3 (compound) | H21 | 91-93, 100-105 (primary); 94-96 (side effect); 81 (predicted miss) | 5/5 primary family (matches v2 alone, no lift from the merge); 5/5 rows 94-96 fixed; 4/5 row 81 still wrong as predicted |

See `HYPOTHESES.md`'s Round 3 entries for the full Result/Rival-explanation/Lesson writeups, including the v13 regression's likely mechanism (the tightened rule's "triggered" keyword false-triggering on rows 40/42's unrelated conditional use of the same word) and v14's sharpened reading of what the compound merge actually demonstrated.

### Round 3 — per-run generation time

Tracked starting this round (see the "tracking per-run generation time" process note in `HYPOTHESES.md`) — going forward, record this alongside every round's pass-rate/score table, not just reconstructed after the fact.

| Variant | Size (chars) | Avg duration (N=5) | Min | Max |
|---|---|---|---|---|
| v11 | 5,372 | 3.26 min | 2.9 min | 3.5 min |
| v12 | 6,489 | 4.95 min | 4.0 min | 5.9 min |
| v13 | 6,031 | 4.57 min | 3.6 min | 5.3 min |
| v14 | 8,950 | 4.02 min | 3.5 min | 4.7 min |

Not simply a function of file size — v14 is the largest document by far but ran faster on average than v12 or v13. v12 (the paraphrase-merge bullet) was the slowest and had the widest spread, consistent with a rule that invites more per-row justification across the whole response rather than only on its target row.

## Round 4 (N=5 per variant) — target-row pass rates, not full-suite scores

All four Round 4 variants are single-hypothesis diagnostic tests, each changing one narrow, isolated thing from v1 (same rationale as Round 3). H25 (a fifth Round 4 hypothesis, about v12's extra generation time) was resolved via re-analysis of already-collected Round 1/3 data — no new variant or run needed; see `HYPOTHESES.md`.

| Variant | Parent | Hypothesis | Target rows | Pass rate (N=5) |
|---|---|---|---|---|
| v15 | v1 (−"subjective/vague still valid" bullet) | H29 | 70-72 | 5/5 still correctly valid — **REFUTED** |
| v16 | v1 (causal-vs-cond fix, completedness not keyword) | H22 | 41 (primary); 40/42 (regression check); 67-69 (check) | 5/5 clean on all target rows — **CONFIRMED** |
| v17 | v1 (−premise/conclusion structure-preservation step) | H27 | 163-165 | 4/5 structure flattened, labels dropped — **CONFIRMED** |
| v18 | v1 (−explicit 26-letter-then-P1,P2 overflow instruction) | H28 | 160-162 | 5/5 no errors, but all 5 abandon the letter-then-number scheme for a direct numbered scheme — **REFUTED** (correctness), format changed |

See `HYPOTHESES.md`'s Round 4 entries for full Result/Rival-explanation/Lesson writeups.

### Round 4 — per-run generation time

| Variant | Size (chars) | Avg duration (N=5) | Min | Max |
|---|---|---|---|---|
| v15 | 5,972 | 4.63 min | 4.45 min | 5.17 min |
| v16 | 6,340 | 4.81 min (N=4; one run's exact duration not captured) | 4.50 min | 5.44 min |
| v17 | 5,838 | 4.61 min | 4.06 min | 5.71 min |
| v18 | 5,991 | 4.65 min | 3.98 min | 5.41 min |

All four Round 4 variants cluster tightly around 4.6-4.8 minutes despite being close in size (~5.8-6.3K chars) — a much narrower spread than Round 3 (3.26-4.95 min across a similar size range), consistent with these being smaller, single-clause edits rather than Round 3's mix of added examples/bullets vs. a large compound merge (v14).

## Round 5 (N=5 per variant) — target-row pass rates, not full-suite scores

All four Round 5 variants are single-hypothesis diagnostic tests, each changing one narrow, isolated thing from v1 — picked via `U × D × ln(rows+1)` from a fresh, principle-first-generated 20-hypothesis backlog (H50-H69; see `HYPOTHESES.md`'s Round 5 section for the full principle taxonomy and scoring derivation).

| Variant | Parent | Hypothesis | Target rows | Pass rate (N=5) |
|---|---|---|---|---|
| v19 | v1 (necsuff-rule weakened, not removed — two directional bullets merged into one vaguer statement) | H69 | 130-138 (9 rows) | 45/45 correct — **REFUTED** |
| v20 | v1 (−paraphrase-merge-rule's near-certain-equivalence bullet) | H58 | 82-84 | 5/5 rows 82/84 held; **4/5 row 83 failed** (rendered as unrelated `P;Q` instead of `P;¬P`) — **CONFIRMED** |
| v21 | v1 (−polysemy clause from the vocabulary-overlap bullet) | H60 | 148-150 | 15/15 correct — **REFUTED** |
| v22 | v1 (−explicit-label-precedence bullet) | H61 | 121-123 | 15/15 correct — **REFUTED** |

See `HYPOTHESES.md`'s Round 5 entries for full Result/Rival-explanation/Lesson writeups.

## Round 6 (N=5) — v23, consolidation variant, full-suite score

The first variant graded with all 165 rows checked directly against `tests.csv`'s expected_output by dedicated grading agents (previous full-suite scores were not verified this literally — see `HYPOTHESES.md`'s Round 6 process note and write-up).

| Variant | Parent | Size (chars) | Run scores | Avg | Min | Max | Avg duration (N=5) | Min | Max |
|---|---|---|---|---|---|---|---|---|---|
| v23 | v1 (consolidation of all confirmed Round 2-5 fixes) | ~5,600 | 157, 158, 160, 155, 156 | 157.2 | 155 | 160 | 4.33 min | 3.89 min | 5.08 min |

Systematic misses (5/5 runs): row 41 (causal-vs-cond wording drops v1's one-sentence-vs-two-sentence distinction), row 81 (misclassified as INVALID), rows 148-149 (`decompose-rule` over-splits a compound predicate). Partial miss: row 150 (3/5, the known "could" modal/suite conflict). Noise (2/5): rows 124-126 (redefinition symbol not used in the final formula), rows 151-153 (scope-reset letter reuse). See `HYPOTHESES.md` for full detail.

## Reading these numbers

- v1 remains the strongest full-suite performer across both rounds (160.6 avg in Round 1, and v6-v9's scores — each v1 minus one component — cluster close to it: 158.75-161.25). This is consistent with the Round 2 hypothesis verdicts: only two of the four removed components (causal-vs-cond in v7, scope-boundary in v9) are confirmed load-bearing, so removing any single one costs at most ~2-3 points off v1's baseline, not a collapse.
- v5 (Round 1) and v10 (Round 2, v5 + one fix) show the brevity/correctness tradeoff directly: v10's single added sentence raised v5's row 124-126 reliability (per HYPOTHESES.md's H2 finding) but did not move the full-suite average much (132.5 vs. v5's 133.2) — the suite's other v5-inherited gaps (temporal-invalid, non-English detection, symbolic-input detection, mixed-valid/invalid extraction) are untouched by that fix and dominate the score gap to v1.
- v3's high variance (stddev 4.9, range 12) stands out — one run (161) handled the question/command/modal mixed-input pattern correctly while the other four (149-153) did not, consistent with H3's "worked examples don't reliably teach this exclusion pattern" finding.
