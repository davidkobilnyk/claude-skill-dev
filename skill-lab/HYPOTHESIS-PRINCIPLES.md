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

| Score | Meaning | Illustrative example (not tracking-table data — see note below) |
|---|---|---|
| 0 | No update — matched a near-certain prior, doesn't even add meaningful sample size. | — |
| 1 | Mild confirmation — expected direction and magnitude, adds a data point, teaches nothing new. | — |
| 2 | Minor detail resolved — settled a low-confidence guess, but the mechanism was already roughly understood. | — |
| 3 | Real structure revealed — expected direction, but surfaced a specific detail/failure pattern not previously pinned down. | H27 (we suspected structure-preservation mattered, didn't know it'd fail 4/5 cleanly once removed) |
| 4 | Assumption reversed — overturned something treated as settled. | H29 (subjective-inclusion bullet assumed necessary since v1; found fully redundant) |
| 5 | Reframes a class of problems, not just one component. | H25 (invisible-deliberation-cost pattern — now watched for on any future timing outlier, not just v12) |

### AV — Action Value
Did this change, or is it likely to change, what ships?

| Score | Meaning | Illustrative example (not tracking-table data — see note below) |
|---|---|---|
| 0 | Dead end — no action taken or anticipated. | — |
| 1 | Logged only — filed as a process note/backlog item, no concrete next step yet. | — |
| 2 | Shaped prioritization — fed into deciding what to test next, didn't itself touch a variant. | — |
| 3 | Directly caused a new variant to be built. | H18 (v13's rows 40/42 regression is the direct reason H22/v16 got built) |
| 4 | Confirmed fix, not yet folded into the leading variant. | H22 (fix confirmed 5/5, not yet consolidated into v1) |
| 5 | Shipped to the leading/production variant, measurably moving its performance. | — (none yet as of this writing) |

**Important — these examples are illustrations of the scale, not tracking-table entries, and the distinction matters more than it sounds.** H18/H22/H25/H27/H29 were generated the normal ad hoc way (whatever process actually produced them at the time) and only afterward labeled with a principle they happened to resemble. That's a different mechanism than *deliberately generating a hypothesis by applying a chosen principle as the seed* — the thing this file is actually trying to measure the value of. A hypothesis that was never generated *via* a principle can't provide valid evidence about that principle's productivity, no matter how it's scored — the causal link the tracking table is supposed to capture (principle → hypothesis → outcome) simply isn't present for a hypothesis produced first and labeled second. So these five stay in the rubric purely to calibrate what "IV=4" or "AV=3" *feel like*, and must never be copied into the tracking table below as if they were real principle-generation samples.

## Workflow

The generative order matters and cannot be reversed: a hypothesis only counts as data about a principle if the principle was chosen and applied *before* the hypothesis existed, as the actual seed/constraint used to produce it. Labeling an already-generated hypothesis with a principle it resembles in hindsight is not the same act and does not belong in the tracking table (see note above) — at most it's a description, never evidence.

1. **Before generating:** pick a principle (P1-P6, or propose a new one if the taxonomy needs extending) and hold it as the explicit generating constraint.
2. **Generate the hypothesis using that principle as the seed** — e.g. for P6 (structured coverage sweep), literally start from the component × failure-mode grid and let the grid produce the candidate, rather than free-associating and checking afterward whether it happens to fit a grid cell.
3. **At result-write time:** score IV and AV (0-5 each) in the project's own `HYPOTHESES.md` entry, using the rubric anchors above purely for calibration.
4. **In this file:** append a row to the tracking table below — but only for hypotheses that actually went through steps 1-2 in that order. A hypothesis generated the ordinary ad hoc way, even a valuable one, does not get a row here just because a principle can be attached to it after the fact.
5. **Aggregation/analysis** (average IV/AV per principle, etc.) is deliberately not built yet — deferred until there's enough rows to design it against real data rather than guesswork.

## Tracking table

Empty as of this writing — by design. No prior hypothesis in this project was generated principle-first, so none qualifies as valid data under the workflow above; backfilling would only reintroduce the exact problem this file exists to avoid. The first real rows should come from Round 5 onward, generated principle-first per the workflow.

| Hypothesis | Project | Principle applied (chosen before generation) | IV | AV | Note |
|---|---|---|---|---|---|
| *(none yet)* | | | | | |
