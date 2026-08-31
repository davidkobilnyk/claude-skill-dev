---
name: skill-variant-lab
description: run only when explicitly called; drives the full iterative loop of designing a simple, testable skill, generating multiple competing SKILL.md variants, running them against a shared test suite in isolated subagents, and evolving new variants from data-backed hypotheses about why some did better than others (both correctness and skill-text brevity)
---

# skill-variant-lab

Orchestrates an experimental loop for developing a simple, deterministic-ish skill (like "add these numbers") through competing variants scored against a fixed test suite. Use only when the user explicitly invokes this process — this is not a general skill-authoring tool (see `skill-creator`/`skill-dev-orchestrator` for that); it's specifically for the "generate variants, test them, learn, iterate" loop.

## File layout

Everything for one variant set lives together in `skill-lab/<name>/`, next to (not inside) `skills/`:

- `skill-lab/<name>/v<N>/SKILL.md` — each variant, one per subfolder. The `name:` frontmatter inside stays a full unique name (e.g. `<name>-v<N>`) even though the folder itself is just `v<N>`.
- `skill-lab/<name>/tests.csv` — shared test suite, columns `input,expected_output`.
- `skill-lab/<name>/HYPOTHESES.md` — lineage/lessons log (see step 7). Created on the first hypothesis round and appended to every round after.

## Step 1 — Intake

Ask the user what the target skill should do: a short name/prefix, the core behavior in plain language, and any known edge cases or quirks they already anticipate. Do not proceed until this is clear enough to write test cases from.

## Step 2 — Test case generation

Propose `input,expected_output` pairs covering: the plain/normal case, phrasing variety if relevant (natural language vs. symbolic), edge cases suggested by the intake, and at least one stress case that probes a likely failure mode. Show the full table to the user. Wait for explicit confirmation or edits before writing `skill-lab/<name>/tests.csv`. Only loop again if the user explicitly asks for changes — don't force multiple rounds.

## Step 3 — Initial variants

Generate 3–5 variants (never exceed 6 active at once — see the cap rule below) that take genuinely different approaches to the same instruction, not just paraphrases of each other. Write each to `skill-lab/<name>/v<N>/SKILL.md`.

## Step 4 — Run the matrix

For every (active variant × test case) pair, spawn an independent background subagent (the `Agent` tool, `run_in_background: true`), all launched in parallel in one message.

**Hard rule — read the file, do not invoke the skill by name.** Each subagent's prompt must tell it to `Read` the specific `skill-lab/<name>/v<N>/SKILL.md` file and follow its instructions directly, applying them to the given input, then report only the raw final output. Never instruct a subagent to invoke the skill via the `Skill` tool by name. Freshly created skills are frequently invisible to a fresh subagent's own skill listing (observed roughly 1 success in 44 attempts in practice) — invoking by name silently wastes most of the run on "Unknown skill" errors instead of real results.

Wait for all task-notifications before compiling results; do not guess or predict outcomes ahead of the notifications arriving.

## Step 5 — Results table

For each variant, show: per-test pass/fail (substring match — does `expected_output` appear in the actual output), the variant's total pass count, and its **character count** (`wc -c` on the whole `SKILL.md` file, frontmatter included). Present one table per variant, plus a summary table of all variants' scores and char counts, unless the user asked for a different format.

**Ranking rule**: correctness is primary. Brevity (lower char count) is used only as a tiebreaker between variants with equal pass counts — including when both are equally low-scoring (e.g. two variants both at 3/14 still get ranked against each other by brevity).

## Step 6 — Hypotheses

Compare higher- vs. lower-ranked variants (by the rule above) and write plain-language hypotheses about what caused the difference — on correctness, on brevity, or both. Ground each hypothesis in a specific textual difference between variants, not vague impressions.

## Step 7 — Next-gen proposals

**Hard rule — one hypothesis per new variant, always.** For each hypothesis worth testing, propose exactly one new variant that changes only that one thing relative to its named parent variant. Never bundle two changes into one new variant, even if both seem obviously good — that destroys attribution.

For each proposed variant, record before building it:
- parent variant
- the single hypothesis being tested
- the specific change being made

Present this plan to the user before writing any files.

## Step 8 — Create files + log

Write the new `SKILL.md` files per the approved plan. Then update `skill-lab/<name>/HYPOTHESES.md`, appending one entry per new variant:

```
## <name>-v<N> (parent: <name>-v<M>)
Hypothesis: <what we believed and why>
Change made: <the single concrete change>
Result: (fill in after the next run: confirmed / refuted / inconclusive)
Lesson: (fill in after the next run)
```

Leave `Result` and `Lesson` blank until the next run's data comes in, then fill them in as part of step 5/6 of that next round — this file is the persistent memory of what's already been tried and learned, so don't re-test a hypothesis that a past entry already refuted without a new reason to believe it'd go differently.

## Step 9 — Confirm before re-running, and propose retirement

Before spending more tokens on another full matrix run:
- **Never re-run the matrix with the same variant set as a prior run.** Every re-run must include at least one new variant from step 7/8. If the only motivation to re-run is to check whether a prior result was noise, that's a signal to design a targeted variant for it (e.g., a near-duplicate testing determinism isn't itself useful — prefer moving forward with real hypotheses), not to just repeat the exact same set.
- Recommend retiring the oldest/weakest variants when a newer variant clearly dominates them on both correctness and brevity — keep the active set within the 3–5 target (never above 6). "Retire" means excluding from future run matrices, not deleting the files — leave them in the repo/git history for audit purposes unless the user explicitly asks to delete.
- Ask the user to confirm the new variant set and the retirement list before launching the next matrix run.
