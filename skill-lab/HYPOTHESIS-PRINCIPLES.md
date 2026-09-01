# Hypothesis-generation principles — repo-wide tracking

A cross-project resource for `skill-variant-lab` runs. Where `HYPOTHESES.md` in each project directory (e.g. `dk-prop-logic-parser/HYPOTHESES.md`) tracks the hypotheses and results for *that skill*, this file tracks which *generating principle* produced each hypothesis and how valuable it turned out to be — accumulated across every skill lab this repo ever runs, so that over time we get evidence-based answers to "which principles for generating hypotheses actually pay off," instead of re-deciding by gut sense every round.

Background/rationale for this file: logged in `dk-prop-logic-parser/HYPOTHESES.md`'s process notes (H48 scoring-time testability lapse, and the broader "hypothesis generation is currently unprincipled" discussion, 2026-09-01).

## Principle taxonomy

Each hypothesis proposed in any project should be tagged with the principle(s) that motivated it, using the stable IDs below. A hypothesis may carry more than one tag.

- **P1 — Evidence-anchored.** Motivated by a specific thing already observed (a partial result, an unexplained pass/fail split, a design tension between two variants) — not free-associated speculation about a component just because it hasn't been touched yet.
- **P2 — Mechanism-first.** States a plausible causal explanation for *why* the predicted effect would occur, before the hypothesis is scored — the mechanism claim is what diagnosticity is actually measuring.
- **P3 — Testability-verified.** Confirmed testable against both (a) existing test rows and (b) an existing or readily-buildable isolated variant, *before* being scored or pursued — not discovered to be untestable only once scoring starts.
- **P4 — Non-redundant.** Checked against what prior rounds already resolved, to avoid re-litigating settled questions in new wording.
- **P5 — Organic count.** Generated until well-motivated candidates run out, not padded to hit a target quantity (e.g. "give me 20").
- **P6 — Structured coverage sweep.** Derived from a systematic grid (component × failure-mode: never tested / weakened / generalizes-beyond-its-example / holds-under-varied-input-shape) rather than one-shot free association.

This list is expected to grow or get refined as we see what actually predicts value — treat it as a living taxonomy, not fixed on day one.

## Value rubrics

Scored once a hypothesis resolves (same moment its Result/Rival-explanation/Lesson is written in the project's own `HYPOTHESES.md` — not reconstructed later). Kept as two **separate** 0-5 scores, never combined into one number — they measure genuinely different things and collapsing them would hide real patterns (e.g. a principle that reliably produces deep-insight/slow-to-act findings looks nothing like one that produces small, fast-shipping fixes, even if some combined score made them look equal).

### IV — Information Value
How much did the actual result update our beliefs, relative to what we expected going in?

| Score | Meaning | Anchor |
|---|---|---|
| 0 | No update — matched a near-certain prior, doesn't even add meaningful sample size. | — |
| 1 | Mild confirmation — expected direction and magnitude, adds a data point, teaches nothing new. | — |
| 2 | Minor detail resolved — settled a low-confidence guess, but the mechanism was already roughly understood. | — |
| 3 | Real structure revealed — expected direction, but surfaced a specific detail/failure pattern not previously pinned down. | H27 (we suspected structure-preservation mattered, didn't know it'd fail 4/5 cleanly once removed) |
| 4 | Assumption reversed — overturned something treated as settled. | H29 (subjective-inclusion bullet assumed necessary since v1; found fully redundant) |
| 5 | Reframes a class of problems, not just one component. | H25 (invisible-deliberation-cost pattern — now watched for on any future timing outlier, not just v12) |

### AV — Action Value
Did this change, or is it likely to change, what ships?

| Score | Meaning | Anchor |
|---|---|---|
| 0 | Dead end — no action taken or anticipated. | — |
| 1 | Logged only — filed as a process note/backlog item, no concrete next step yet. | — |
| 2 | Shaped prioritization — fed into deciding what to test next, didn't itself touch a variant. | — |
| 3 | Directly caused a new variant to be built. | H18 (v13's rows 40/42 regression is the direct reason H22/v16 got built) |
| 4 | Confirmed fix, not yet folded into the leading variant. | H22 (fix confirmed 5/5, not yet consolidated into v1) |
| 5 | Shipped to the leading/production variant, measurably moving its performance. | — (none yet as of this writing) |

## Workflow

1. **At proposal time:** tag each hypothesis with its generating principle(s) (P1-P6, or a new one if the taxonomy needs extending) in the project's own `HYPOTHESES.md` entry.
2. **At result-write time:** score IV and AV (0-5 each) in the same entry, using the anchors above as calibration.
3. **In this file:** append a row to the tracking table below for each resolved hypothesis, so principle-level patterns can be read off across all projects without re-parsing every project's `HYPOTHESES.md`.
4. **Aggregation/analysis** (average IV/AV per principle, etc.) is deliberately not built yet — deferred until there's enough rows to design it against real data rather than guesswork. Revisit once this table has meaningfully more entries.

## Tracking table

| Hypothesis | Project | Principle(s) | IV | AV | Note |
|---|---|---|---|---|---|
| H18 | dk-prop-logic-parser | P1 | 4 | 3 | v13's causal-vs-cond tightening regressed rows 40/42; directly motivated H22/v16. |
| H22 | dk-prop-logic-parser | P1, P2 | 3 | 4 | Re-qualifying by completedness (not keyword) confirmed 5/5; fix ready, not yet folded into v1. |
| H25 | dk-prop-logic-parser | P1 | 5 | 1 | Resolved via re-analysis, no new run. Revealed invisible-deliberation-cost pattern, generalizable to future timing outliers; no shipped action yet. |
| H27 | dk-prop-logic-parser | P6 | 3 | 2 | Structure-preservation step confirmed load-bearing (4/5 regression without it); informs keeping it in any future consolidated variant, not yet itself a shipped change. |
| H29 | dk-prop-logic-parser | P6 | 4 | 1 | Subjective-inclusion bullet found fully redundant; logged, no trim shipped yet. |
| H48 | dk-prop-logic-parser | P1 | 2 | 1 | Scored despite an unresolved confound (no variant isolates verify-step) — the finding here is about our own process, not the skill; logged as a process lesson, not yet actionable on the skill itself. |

Backfilled only for the hypotheses already used as calibration anchors above, plus H48 (the process-lapse case). The rest of this project's H1-H47/H49 backlog is not yet backfilled — apply this workflow going forward from Round 5 onward, and backfill earlier entries opportunistically rather than as a blocking task.
