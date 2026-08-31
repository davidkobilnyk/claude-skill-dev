---
name: skill-variant-lab
description: run only when explicitly called; drives the full iterative loop of designing a simple, testable skill, generating multiple competing SKILL.md variants, running them against a shared test suite in isolated subagents, and evolving new variants from data-backed hypotheses about why some did better than others (both correctness and skill-text brevity)
---

# skill-variant-lab

Orchestrates an experimental loop for developing a simple, deterministic-ish skill (like "add these numbers") through competing variants scored against a fixed test suite. Use only when the user explicitly invokes this process — this is not a general skill-authoring tool (see `skill-creator`/`skill-dev-orchestrator` for that); it's specifically for the "generate variants, test them, learn, iterate" loop.

## File layout

Everything for one variant set lives together in `skill-lab/<name>/`, next to (not inside) `skills/`:

- `skill-lab/<name>/v<N>/SKILL.md` — each variant, one per subfolder. The `name:` frontmatter inside stays a full unique name (e.g. `<name>-v<N>`) even though the folder itself is just `v<N>`.
- `skill-lab/<name>/tests.csv` — shared test suite, columns `input,expected_output,scenario`. Fixed once locked in step 3; never edited mid-lineage (see step 3).
- `skill-lab/<name>/COMPONENTS.md` — the named mechanism inventory and the components × variants reference table (see step 4).
- `skill-lab/<name>/HYPOTHESES.md` — lineage/lessons log (see step 10). Created on the first hypothesis round and appended to every round after.
- `references/text-principles.md` (in this skill's own folder, not per-lab) — lessons on writing variant instruction text; read it in step 5.

## Step 1 — Intake

Ask the user what the target skill should do: a short name/prefix, the core behavior in plain language, and any known edge cases or quirks they already anticipate. Do not proceed until this is clear enough to write test cases from.

Also ask what the acceptable failure rate is for the finished skill: optimize for the best average performance, or zero-tolerance (any single observed failure disqualifies a variant, however good its average)? Record the answer — it sets the default run count in step 6 and the bar for calling anything "final" in step 7.

## Step 2 — Scenario brainstorming

Before writing a single test case, deliberately and creatively enumerate the *categories* of scenario this skill could encounter — don't jump straight to test cases. Think broadly across axes like: the plain/normal case, phrasing/format variety, boundary and degenerate inputs (empty, single-item, maximal), inputs that stress the specific mechanism the skill will likely use (e.g. anything a naive character scan collapses or skims past), ambiguous cases where a reasonable rule could go either way, adversarial/injection-shaped input, inputs shaped like other data formats (structured/JSON-ish, code, markdown), and any known quirks or edge cases surfaced in intake.

Target **25–35 distinct scenarios**, each a one-line description of *what's being stressed and why*, not an example input yet. Present the full list to the user and get their sign-off (adding, cutting, or merging scenarios) before generating any actual test cases — this list is the map of the problem space that every later round gets tested against, so it's worth getting genuinely broad here rather than letting it grow reactively later.

## Step 3 — Test case generation (locked before any variant exists)

For each confirmed scenario, write **3 concrete `input,expected_output` test cases** that instantiate it (different inputs, same underlying stress). This yields roughly 75–105 total test cases. Show the full table to the user. Wait for explicit confirmation or edits before writing `skill-lab/<name>/tests.csv`.

**This suite is then locked for the entire lineage.** Do not add, remove, or edit rows in later rounds just because a new failure mode was discovered mid-project — that breaks comparability between early and late rounds' scores (a variant that "improved" might just be facing an easier suite). If a genuinely new scenario category is discovered later that the original brainstorm missed, treat it the same as a new hypothesis: propose it explicitly to the user, and if approved, version the suite (`tests_v2.csv`) rather than silently mutating `tests.csv`, and note in `HYPOTHESES.md` exactly which round the suite changed at so historical scores stay interpretable.

## Step 4 — Mechanism/component inventory

Before writing any variant, name the distinct, atomic *components* a variant's text or design could plausibly include — the building blocks you expect to mix and match across variants. Examples of what a component is: "spell-out-before-counting step," "length-check verification (compare transcribed length to input length)," "independent recount," "explicit rule for [specific ambiguity], stated as a general principle," "explicit rule for [specific ambiguity], stated as an enumerated list," "worked example," "code-execution via a pre-written script," "structured primary/fallback split." Give each a short ID (e.g. `spell-out`, `len-check`, `homoglyph-rule-general`).

Write this list to `skill-lab/<name>/COMPONENTS.md`, along with a table with one row per component and one column per variant (added to as variants are created), marking which components each variant contains. Keep this table current every time a variant is added — it's what makes it possible to later ask "which component actually explains this score difference" instead of only "which variant scored higher," since variants often differ by more than one component at once.

## Step 5 — Initial variants

Generate 3–5 variants (never exceed 6 active at once — see the cap rule below) that take genuinely different approaches to the same instruction, not just paraphrases of each other. Before drafting or revising any variant's text, read `references/text-principles.md` — lessons on ambiguity, verification criteria, and fallback structure carried over from prior labs. Write each variant to `skill-lab/<name>/v<N>/SKILL.md`. Update the components × variants table in `COMPONENTS.md` for each one, adding any new component IDs discovered along the way.

## Step 6 — Run the round

For every active variant, spawn **N independent background subagents** (the `Agent` tool, `run_in_background: true`), each running the *entire* test suite internally in one pass (not one subagent per test case — that multiplies fixed per-agent overhead for no benefit). Launch all of them in one message so they run concurrently.

**Run count**: a single run per variant is not evidence of reliability — it's one sample of what can be a genuinely noisy distribution. Default to **N=5** for an early/exploratory round comparing several variants. Once a variant is a serious "final" candidate under a low-tolerance correctness bar, escalate to a much deeper round (N=20–30) specifically for that variant before treating any zero-failure record as real — small samples have repeatedly looked perfect in this lab and then cracked at depth.

**Hard rule — read the file, do not invoke the skill by name.** Each subagent's prompt must tell it to `Read` the specific `skill-lab/<name>/v<N>/SKILL.md` file and follow its instructions directly, applying them to every row in `tests.csv`, then report a numbered list of its own computed outputs (not a comparison against `expected_output` — keep the subagent blind to the expected answers so it can't anchor to them). Never instruct a subagent to invoke the skill via the `Skill` tool by name. Freshly created skills are frequently invisible to a fresh subagent's own skill listing (observed roughly 1 success in 44 attempts in practice) — invoking by name silently wastes most of the run on "Unknown skill" errors instead of real results.

Wait for all task-notifications before compiling results; do not guess or predict outcomes ahead of the notifications arriving. Watch for garbled/misnumbered subagent output (an internal transcription slip in the agent's own final list, not a counting/reasoning failure) — flag and exclude these runs from scoring as a reporting artifact, noted explicitly, rather than force-realigning or guessing at the intended values.

## Step 7 — Results table

For each variant, across its N runs, report: per-run score, **avg, min, range (max−min), and stddev**, plus the variant's character count (`wc -c` on the whole `SKILL.md` file, frontmatter included, plus any bundled asset files). Also report **failure rate** (fraction of runs with zero misses) as its own number alongside the average — a high average can still hide a meaningful nonzero failure rate, which matters most once the project's bar is "never fails" rather than "best on average."

Break out **per-row miss frequency** across the N runs for any variant with failures — which specific rows are actually driving the misses, and whether misses within a single bad run cluster together (suggesting one bad pass corrupted several answers) or are scattered independently across different runs (suggesting isolated slips). This is usually more informative than the aggregate score alone for deciding what to fix next.

**Ranking rule**: correctness (average, then failure rate, then min) is primary. Brevity (lower char count) is used only as a tiebreaker between variants with equal correctness — including when both are equally low-scoring.

**Hard rule — no "final" or "reliable" language below N=20.** Never describe a variant as final, reliable, or recommended for shipping in this table or any summary unless it has been run at N≥20 with zero failures. A clean run at lower N is reported as exactly that — "clean at N=5" — never rounded up to a reliability claim.

## Step 8 — Hypotheses

Compare higher- vs. lower-ranked variants (by the rule above) and write plain-language hypotheses about what caused the difference — on correctness, on brevity, or both. Ground each hypothesis in a specific **component** from the `COMPONENTS.md` table (not just "variant A vs variant B" — if two variants differ by more than one component, the table tells you which components are actually in play, and the hypothesis should isolate one) or a specific textual difference. Cross-reference the atomic-component consistency numbers across variants that share a component to see whether a pattern is really tied to that component or just to one variant's overall text.

Before drawing conclusions, spot-check that `COMPONENTS.md`'s table still matches the actual `SKILL.md` text of the variants being compared (a quick grep for each component's characteristic phrase is enough) — correct any drift found before hypothesizing from it.

## Step 9 — Next-gen proposals

**Hard rule — one hypothesis per new variant, always.** For each hypothesis worth testing, propose exactly one new variant that changes only that one thing (ideally: adds, removes, or swaps exactly one named component) relative to its named parent variant. Never bundle two changes into one new variant, even if both seem obviously good — that destroys attribution.

For each proposed variant, record before building it:
- parent variant
- the single hypothesis being tested
- the specific change being made (named against the component ID it adds/removes/swaps, per `COMPONENTS.md`)

Present this plan to the user before writing any files.

## Step 10 — Create files + log

Write the new `SKILL.md` files per the approved plan. Update `skill-lab/<name>/COMPONENTS.md`'s reference table for each new variant. Then update `skill-lab/<name>/HYPOTHESES.md`, appending one entry per new variant:

```
## <name>-v<N> (parent: <name>-v<M>)
Hypothesis: <what we believed and why>
Change made: <the single concrete change, named against its component ID>
Result: (fill in after the next run: confirmed / refuted / inconclusive)
Lesson: (fill in after the next run)
```

Leave `Result` and `Lesson` blank until the next run's data comes in, then fill them in as part of step 7/8 of that next round — this file is the persistent memory of what's already been tried and learned, so don't re-test a hypothesis that a past entry already refuted without a new reason to believe it'd go differently.

## Step 11 — Confirm before re-running, and propose retirement

Before spending more tokens on another round:
- **Never re-run with the same variant set and same N as a prior round.** Every re-run must either include at least one new variant from step 9/10, or be a deliberate depth escalation on an existing variant (more runs to firm up a reliability estimate) — state explicitly which of the two a new round is for.
- Recommend retiring the oldest/weakest variants when a newer variant clearly dominates them on both correctness and brevity — keep the active set within the 3–5 target (never above 6). "Retire" means excluding from future rounds, not deleting the files — leave them in the repo/git history for audit purposes unless the user explicitly asks to delete.
- Ask the user to confirm the new variant set and the retirement list before launching the next round.
- **Every third round, or whenever the total variant count across the whole lineage exceeds ~15**, summarize total rounds run so far and the rough token spend, and ask the user whether to continue, narrow scope, or wrap up with the current best candidate.

## Step 12 — Real-world validation

Once a variant clears the N≥20 zero-failure bar from step 7, and if the skill's real deployment surface differs from this lab's testing environment (e.g. claude.ai chat vs. Claude Code, where bundled-asset availability and trust context can differ), package it and test it there before calling it done. Log the result in `HYPOTHESES.md` under a "Real-world spot check" heading, the same way as any other round's results. If the deployment surface is unknown or identical to the testing environment, note that explicitly rather than skipping the step silently.
