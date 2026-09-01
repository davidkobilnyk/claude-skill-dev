---
name: skill-variant-lab
description: run only when explicitly called; drives the full iterative loop of designing a simple, testable skill, generating multiple competing SKILL.md variants, running them against a shared test suite in isolated subagents, and evolving new variants from data-backed hypotheses about why some did better than others (both correctness and skill-text brevity)
---

# skill-variant-lab

Orchestrates an experimental loop for developing a simple, deterministic-ish skill (like "add these numbers") through competing variants scored against a fixed test suite. Use only when the user explicitly invokes this process — this is not a general skill-authoring tool (see `skill-creator`/`skill-dev-orchestrator` for that); it's specifically for the "generate variants, test them, learn, iterate" loop.

**Standing discipline — cite the rule's purpose, not just its name.** This skill contains several hard rules (no-bundling, ranking-primary-on-correctness, N≥20-before-"reliable", and others below). Whenever one of them is the stated reason for *not* doing something — deferring a proposal, holding off an escalation, declining a merge — name the rule's underlying purpose in the same sentence, not just its label, and check whether that purpose still applies right now. "Not proposing X because of the no-bundling rule" is a name-check; "not proposing X because neither half is independently verified yet, which is what the no-bundling rule protects against" is a live check — and it's the live check that catches the moment a rule's letter has outlived its reason, instead of quietly following it past that point.

**Standing discipline — log process realizations the moment they're articulated.** If, at any point in a lab (not just at scheduled checkpoints), a conversation surfaces *why* the process handled something suboptimally — a rule applied past its rationale, a gap in scenario coverage, a bias in what got prioritized — write it into `skill-lab/<name>/HYPOTHESES.md` under a `## Process note` heading as part of that same turn, before moving on. Don't wait to be asked to write it down, and don't treat it as separate from the lab's own record just because it's about the process rather than a specific variant — a realization about *why* is exactly the kind of thing this file exists to preserve, and it decays fast once the conversation moves on.

## File layout

Everything for one variant set lives together in `skill-lab/<name>/`, next to (not inside) `skills/`:

- `skill-lab/<name>/v<N>/SKILL.md` — each variant, one per subfolder. The `name:` frontmatter inside stays a full unique name (e.g. `<name>-v<N>`) even though the folder itself is just `v<N>`.
- `skill-lab/<name>/tests.csv` — shared test suite, columns `input,expected_output,scenario`. Fixed once locked in step 3; never edited mid-lineage (see step 3).
- `skill-lab/<name>/tests_inputs_only.txt` — the `input` column only, numbered to match `tests.csv`'s rows, with no `expected_output` present. Generated once `tests.csv` locks; this is what subagents are actually pointed at in step 6, never `tests.csv` itself.
- `skill-lab/<name>/COMPONENTS.md` — the named mechanism inventory and the components × variants reference table (see step 4).
- `skill-lab/<name>/HYPOTHESES.md` — lineage/lessons log (see step 10). Created on the first hypothesis round and appended to every round after.
- `references/text-principles.md` (in this skill's own folder, not per-lab) — lessons on writing variant instruction text; read it in step 5.

## Step 1 — Intake

Ask the user what the target skill should do: a short name/prefix, the core behavior in plain language, and any known edge cases or quirks they already anticipate. Do not proceed until this is clear enough to write test cases from.

Also ask what the acceptable failure rate is for the finished skill: optimize for the best average performance, or zero-tolerance (any single observed failure disqualifies a variant, however good its average)? Record the answer — it sets the default run count in step 6 and the bar for calling anything "final" in step 7.

## Step 2 — Scenario brainstorming

Before writing a single test case, deliberately and creatively enumerate the *categories* of scenario this skill could encounter — don't jump straight to test cases. Think broadly across axes like: the plain/normal case, phrasing/format variety, boundary and degenerate inputs (empty, single-item, maximal), inputs that stress the specific mechanism the skill will likely use (e.g. anything a naive character scan collapses or skims past), ambiguous cases where a reasonable rule could go either way, adversarial/injection-shaped input, inputs shaped like other data formats (structured/JSON-ish, code, markdown), and any known quirks or edge cases surfaced in intake.

Target **25–35 distinct scenarios**, each a one-line description of *what's being stressed and why*, not an example input yet.

**Required axis-coverage check before presenting the list.** The axes above are a checklist, not just a prompt for inspiration — draft the scenario list, then build a small table mapping each named axis (plain/normal, phrasing/format variety, boundary/degenerate, mechanism-stress, ambiguous, adversarial/injection, structured-format-shaped, known quirks from intake) to the scenario numbers that cover it. Any axis with zero scenarios mapped to it is a gap — fill it before presenting the list, don't rely on having "thought broadly" during drafting to guarantee every axis actually landed a scenario. This is what catches categories (e.g. empty input, non-numeric text, deceptive/injection-shaped phrasing) that are easy to skip past even when the axis they belong to was right there in the brainstorm prompt.

Present the full list (with its axis-coverage table) to the user and get their sign-off (adding, cutting, or merging scenarios) before generating any actual test cases — this list is the map of the problem space that every later round gets tested against, so it's worth getting genuinely broad here rather than letting it grow reactively later.

## Step 3 — Test case generation (locked before any variant exists)

For each confirmed scenario, write **3 concrete `input,expected_output` test cases** that instantiate it (different inputs, same underlying stress). This yields roughly 75–105 total test cases.

**Required extremity check for any scenario that claims to stress a mechanism at scale or degree.** A scenario named "many-decimal-place operands" or "very large numbers" or similar is a claim, not a guarantee — the concrete instantiation has to actually clear the threshold where the named mechanism would break, not just gesture at the category. Before finalizing test cases for such a scenario, name the specific threshold being targeted (e.g. "typical floating-point precision is ~15-17 significant digits, so this needs operands with more digits than that to actually risk a precision bug") and confirm the chosen inputs clear it. A test case that's merely *shaped like* an extreme case without actually being extreme enough gives false confidence that the mechanism was stressed when it wasn't.

Show the full table to the user. Wait for explicit confirmation or edits before writing `skill-lab/<name>/tests.csv`.

**This suite is then locked for the entire lineage.** Do not add, remove, or edit rows in later rounds just because a new failure mode was discovered mid-project — that breaks comparability between early and late rounds' scores (a variant that "improved" might just be facing an easier suite). If a genuinely new scenario category is discovered later that the original brainstorm missed, treat it the same as a new hypothesis: propose it explicitly to the user, and if approved, version the suite (`tests_v2.csv`) rather than silently mutating `tests.csv`, and note in `HYPOTHESES.md` exactly which round the suite changed at so historical scores stay interpretable.

## Step 4 — Mechanism/component inventory

Before writing any variant, name the distinct, atomic *components* a variant's text or design could plausibly include — the building blocks you expect to mix and match across variants. Examples of what a component is: "spell-out-before-counting step," "length-check verification (compare transcribed length to input length)," "independent recount," "explicit rule for [specific ambiguity], stated as a general principle," "explicit rule for [specific ambiguity], stated as an enumerated list," "worked example," "code-execution via a pre-written script," "structured primary/fallback split." Give each a short ID (e.g. `spell-out`, `len-check`, `homoglyph-rule-general`).

Write this list to `skill-lab/<name>/COMPONENTS.md`, along with a table with one row per component and one column per variant (added to as variants are created), marking which components each variant contains. Keep this table current every time a variant is added — it's what makes it possible to later ask "which component actually explains this score difference" instead of only "which variant scored higher," since variants often differ by more than one component at once.

## Step 5 — Initial variants

Generate 3–5 variants (never exceed 6 active at once — see the cap rule below) that take genuinely different approaches to the same instruction, not just paraphrases of each other. Before drafting or revising any variant's text, read `references/text-principles.md` — lessons on ambiguity, verification criteria, and fallback structure carried over from prior labs. Write each variant to `skill-lab/<name>/v<N>/SKILL.md`. Update the components × variants table in `COMPONENTS.md` for each one, adding any new component IDs discovered along the way.

## Step 6 — Run the round

For every active variant, spawn **N independent background subagents** (the `Agent` tool, `run_in_background: true`), each running the *entire* test suite internally in one pass (not one subagent per test case — that multiplies fixed per-agent overhead for no benefit). Launch all of them in one message so they run concurrently.

**Run count**: a single run per variant is not evidence of reliability — it's one sample of what can be a genuinely noisy distribution. Default to **N=5** for an early/exploratory round comparing several variants. Once a variant is a serious "final" candidate under a low-tolerance correctness bar, escalate to a much deeper round (N=20–30) specifically for that variant before treating any zero-failure record as real — small samples have repeatedly looked perfect in this lab and then cracked at depth.

**Hard rule — read the file, do not invoke the skill by name.** Each subagent's prompt must tell it to `Read` the specific `skill-lab/<name>/v<N>/SKILL.md` file and follow its instructions directly, then report a numbered list of its own computed outputs. Never instruct a subagent to invoke the skill via the `Skill` tool by name. Freshly created skills are frequently invisible to a fresh subagent's own skill listing (observed roughly 1 success in 44 attempts in practice) — invoking by name silently wastes most of the run on "Unknown skill" errors instead of real results.

**Hard rule — blind the subagent structurally, not by instruction.** `tests.csv` has the `expected_output` column sitting right next to each `input` — a subagent told to "apply the SKILL.md to every row in `tests.csv`... but don't compare against `expected_output`" is being trusted to notice an answer in its own context and deliberately look away from it. Don't rely on that. Before launching the round, generate a separate `skill-lab/<name>/tests_inputs_only.txt` containing only the `input` column, numbered to match `tests.csv`'s row order (e.g. one `N. <input>` line per row, inputs given as `repr()`-style quoted strings so embedded newlines/whitespace survive intact). Point every subagent at this file instead of `tests.csv` — the expected answers are then structurally absent from its context, not just off-limits by instruction. Regenerate it once, after `tests.csv` locks in Step 3, and again only if the suite is ever versioned (`tests_v2.csv` → `tests_v2_inputs_only.txt`).

Wait for all task-notifications before compiling results; do not guess or predict outcomes ahead of the notifications arriving. Watch for garbled/misnumbered subagent output (an internal transcription slip in the agent's own final list, not a counting/reasoning failure) — flag and exclude these runs from scoring as a reporting artifact, noted explicitly, rather than force-realigning or guessing at the intended values.

**Required mechanism-compliance check for any component whose whole point is a specific mechanism** (`code-execution`, `primary-fallback-split`, or similar — anything where the component is supposed to make the subagent *do* something specific, not just produce a correct-looking answer). A correct final answer doesn't prove the mechanism ran: a subagent can skip a bundled script entirely, compute the arithmetic itself, and still land on the right string, and a same-final-output check can't tell the difference. Each subagent's completion notification carries a `tool_uses` count — for a variant whose mechanism implies roughly one tool call per test row (e.g. one script invocation per item), check that count against what the mechanism should produce. A suspiciously low `tool_uses` count relative to the test suite size is a signal the mechanism was bypassed for some rows even though the final answers came out right, the same way a bare correct output can hide that a step was silently skipped. Note any such mismatch in `HYPOTHESES.md` rather than letting a perfect score stand for perfect mechanism fidelity.

## Step 7 — Results table

**Required scoring-methodology note, written the first time any row needs interpretive judgment.** Scoring means comparing a subagent's computed output against `tests.csv`'s `expected_output` — but for many tasks more than one string can be a legitimate answer to the same row (formatting variants, equivalent-but-differently-rounded numbers, alternate valid phrasings). The moment scoring requires anything beyond exact string equality, write down the matching rule being used (e.g. "numeric answers compared with tolerance 1e-6," "repeating-decimal answers accepted if the leading digits or the reduced fraction match") in `COMPONENTS.md`, before scoring the round. This is a real methodology choice that shapes which runs count as failures — leaving it as an unwritten default means no one, including a later re-read of this project, can tell whether "102/102" reflects the variant's behavior or a lenient grader.

For each variant, across its N runs, report: per-run score, **avg, min, range (max−min), and stddev**, plus the variant's character count (`wc -c` on the whole `SKILL.md` file, frontmatter included, plus any bundled asset files) and its **average per-run token count** (each subagent's completion notification carries a `subagent_tokens` figure in its usage stats — average that across the N runs; report it starting from the very first round, not deferred until cost becomes a question). Also report **failure rate** (fraction of runs with zero misses) as its own number alongside the average — a high average can still hide a meaningful nonzero failure rate, which matters most once the project's bar is "never fails" rather than "best on average."

**"Too-clean" flag — two distinct questions, not one.** If three or more variants tie at a perfect or near-perfect score in the same round, that's a signal to check, not just a comfortable result — but it's worth separating two different things a tie can mean:
1. *Are these variants indistinguishable from each other* because the suite/depth isn't stressing the differences between their designs? (Escalating depth or scenario coverage is the fix.)
2. *Is the suite itself too weak to fail anything*, independent of which variants are being compared? A test suite (or a scoring-methodology note that's grown too lenient) that nothing ever fails isn't evidence of quality — it's evidence the check isn't checking anything. This mirrors a plain fact about test design: a check that always passes on the first try is usually too weak to have been worth writing, whether the "check" is a judge, a test case, or a matching rule.
Note explicitly which of the two (or both) looks like what's happening, rather than defaulting to the comfortable read.

**Token-cost note**: don't attribute token-cost differences to `SKILL.md` size alone. A variant that makes extra tool calls (e.g. running a bundled script per test item) pays a per-call overhead — the command text and its captured output re-entering context — that dwarfs what the instruction text itself costs. Before crediting a token gap to brevity, check whether the compared variants differ in tool-call count; if they do, that's the more likely driver, and the comparison should be framed as "size effect" vs. "tool-call effect" rather than collapsed into one number.

Break out **per-row miss frequency** across the N runs for any variant with failures — which specific rows are actually driving the misses, and whether misses within a single bad run cluster together (suggesting one bad pass corrupted several answers) or are scattered independently across different runs (suggesting isolated slips). This is usually more informative than the aggregate score alone for deciding what to fix next.

**Ranking rule**: correctness (average, then failure rate, then min) is primary. Brevity (lower char count) is used only as a tiebreaker between variants with equal correctness — including when both are equally low-scoring.

**Hard rule — no "final" or "reliable" language below N=20.** Never describe a variant as final, reliable, or recommended for shipping in this table or any summary unless it has been run at N≥20 with zero failures. A clean run at lower N is reported as exactly that — "clean at N=5" — never rounded up to a reliability claim.

## Step 8 — Hypotheses

Compare higher- vs. lower-ranked variants (by the rule above) and write plain-language hypotheses about what caused the difference — on correctness, on brevity, or both. Ground each hypothesis in a specific **component** from the `COMPONENTS.md` table (not just "variant A vs variant B" — if two variants differ by more than one component, the table tells you which components are actually in play, and the hypothesis should isolate one) or a specific textual difference. Cross-reference the atomic-component consistency numbers across variants that share a component to see whether a pattern is really tied to that component or just to one variant's overall text.

Before drawing conclusions, spot-check that `COMPONENTS.md`'s table still matches the actual `SKILL.md` text of the variants being compared (a quick grep for each component's characteristic phrase is enough) — correct any drift found before hypothesizing from it.

**Required rival-explanation check whenever a hypothesis is marked CONFIRMED.** A hypothesis being "confirmed" means the predicted pattern showed up — it doesn't rule out a different cause producing the same pattern (a lucky sample at this N, an unrelated fix that happened to cover the same rows, noise). Before marking `Result: CONFIRMED` in `HYPOTHESES.md`, name the most likely rival explanation and the specific piece of evidence that rules it out. If no piece of evidence actually rules it out, the honest status is `CONFIRMED (tentative)`, not `CONFIRMED` — say so, and note what additional data (usually depth) would settle it.

**Required merge-opportunity scan.** After writing this round's hypotheses, explicitly list every pair (or set) of variants from this round whose miss clusters are disjoint — no overlapping rows, no evidence either variant's fix touches the other's failure mode. For each such pair, note in `HYPOTHESES.md` whether a merge is a candidate for the next round. This is not optional bookkeeping: a variant that's cheap but not yet top-ranked is easy to under-value once Step 7's correctness-primary ranking has already sorted it below the perfect scorers, even when it's one already-diagnosed fix away from matching them. Naming the merge opportunity here, in the same round its evidence appears, is what keeps it from being silently skipped in favor of escalating an already-passing incumbent.

## Step 9 — Next-gen proposals

**Hard rule — one hypothesis per new variant, with one exception.** For each hypothesis worth testing, propose exactly one new variant that changes only that one thing (ideally: adds, removes, or swaps exactly one named component) relative to its named parent variant. Never bundle two *untested* changes into one new variant, even if both seem obviously good — that destroys attribution.

**Exception — verified-safe merges.** If Step 8's merge-opportunity scan flagged two or more variants that each independently confirmed against disjoint, non-overlapping miss clusters (checked again after this round's results land), their union is not speculative bundling — both halves are already verified, and there's no attribution to destroy. Propose that merge as a variant in this round's plan by default, without waiting for it to separately out-rank the current leader first. A merge across variants that still have any unexplained or overlapping misses does not qualify — treat it as an untested combination and fall back to the one-hypothesis rule.

For each proposed variant, record before building it:
- parent variant
- the single hypothesis being tested
- the specific change being made (named against the component ID it adds/removes/swaps, per `COMPONENTS.md`)

**Required deferred-candidates log.** Alongside the proposed variants, list every hypothesis or merge candidate that was *considered this round and not proposed*, with one line naming why (e.g. "ranked below the tied leaders — deferred," "no rule blocks it, but this round's budget went to other tests," "components not yet independently confirmed"). This is not optional: a plan that only records what's included is invisible to a later check on what's being systematically passed over, and reasons that seemed sufficient in the moment (a ranking rule, a budget call, an unconfirmed component) can stop applying a round or two later without anyone noticing unless the reason itself was written down where it can be re-read. Append this log to `HYPOTHESES.md` under a `## Deferred — Round <N>` heading.

Present this plan to the user before writing any files.

## Step 10 — Create files + log

Write the new `SKILL.md` files per the approved plan. Update `skill-lab/<name>/COMPONENTS.md`'s reference table for each new variant. Then update `skill-lab/<name>/HYPOTHESES.md`, appending one entry per new variant:

```
## <name>-v<N> (parent: <name>-v<M>)
Hypothesis: <what we believed and why>
Change made: <the single concrete change, named against its component ID>
Result: (fill in after the next run: confirmed / confirmed (tentative) / refuted / inconclusive)
Rival explanation considered: (required if Result is confirmed — the most likely alternative cause and the evidence that rules it out, or "none available" if it's only confirmed-tentative)
Lesson: (fill in after the next run)
```

Leave `Result` and `Lesson` blank until the next run's data comes in, then fill them in as part of step 7/8 of that next round — this file is the persistent memory of what's already been tried and learned, so don't re-test a hypothesis that a past entry already refuted without a new reason to believe it'd go differently.

## Step 11 — Confirm before re-running, and propose retirement

Before spending more tokens on another round:
- **Never re-run with the same variant set and same N as a prior round.** Every re-run must either include at least one new variant from step 9/10, or be a deliberate depth escalation on an existing variant (more runs to firm up a reliability estimate) — state explicitly which of the two a new round is for.
- **Before choosing to depth-escalate the current leader, check for a cheaper near-miss first.** Step 7's ranking rule (correctness primary, brevity only as tiebreaker) is for *reporting* rank — it is not automatically the right guide for what to spend the next round's budget on. Specifically check: is there a smaller/cheaper variant whose only misses are already fully diagnosed (a named missing component, not an unexplained slip) and disjoint from each other? If yes, proposing that fix (or, per Step 9's merge exception, that merge) is usually higher-value than escalating the depth of an already-passing incumbent — a verified-safe merge that could dethrone the leader on brevity is a better use of the round than re-confirming what's already known to work. Escalating the incumbent's depth is still worth doing eventually (per the N≥20 rule), but a cheap, already-diagnosed alternative shouldn't be left waiting on the incumbent's validation to finish first.
- Recommend retiring the oldest/weakest variants when a newer variant clearly dominates them on both correctness and brevity — keep the active set within the 3–5 target (never above 6). "Retire" means excluding from future rounds, not deleting the files — leave them in the repo/git history for audit purposes unless the user explicitly asks to delete.
- Ask the user to confirm the new variant set and the retirement list before launching the next round.
- **Every third round, or whenever the total variant count across the whole lineage exceeds ~15**, summarize total rounds run so far and the rough token spend, and ask the user whether to continue, narrow scope, or wrap up with the current best candidate.
- **At that same checkpoint, reconsider whether Step 1's original framing still fits what's been learned**, not just which variant is winning. In particular: does the failure-tolerance bar (best-average vs. zero-tolerance) chosen in Step 1 still match what the data has shown to be achievable? A zero-tolerance bar set before anyone knew a clean N=20+ record was reachable, or a best-average bar chosen when zero-tolerance now looks within reach cheaply, are both worth surfacing to the user rather than silently carrying the original framing forward.
- **At that same checkpoint, re-read every entry in the deferred-candidates log accumulated so far** and ask, for each: does its stated reason still hold given what's landed since? A reason of "components not yet independently confirmed" that both since confirmed cleanly means the deferral has expired — surface it as a proposal now rather than leaving it logged-but-dormant. A reason of "ranked below the tied leaders" is worth rechecking against Step 11's near-miss guidance above, not just re-stated. Report which deferred items are still validly deferred and which should move into this round's plan.

## Step 12 — Real-world validation

Once a variant clears the N≥20 zero-failure bar from step 7, and if the skill's real deployment surface differs from this lab's testing environment (e.g. claude.ai chat vs. Claude Code, where bundled-asset availability and trust context can differ), package it and test it there before calling it done. Log the result in `HYPOTHESES.md` under a "Real-world spot check" heading, the same way as any other round's results. If the deployment surface is unknown or identical to the testing environment, note that explicitly rather than skipping the step silently.

## Step 13 — Process retrospective (required close-out, not optional)

Before considering the lab finished, review every `## Process note` entry logged in `HYPOTHESES.md` over the course of the project (per the standing discipline in the intro). For each one that points at a gap in `skill-variant-lab` itself — not just a one-off mistake in this particular lab — proactively draft a suggested patch to this skill file and present it to the user for approval, the same way Step 12's real-world check is a required action rather than something that waits to be asked for. If no process notes were logged, or none of them implicate the lab's own process, say so explicitly rather than skipping the step silently.

In addition to the process-note review above, look back over the whole conversation and answer these two questions explicitly, even if nothing was logged as a formal process note along the way:

- **What did I have to figure out this time that wasn't explicit in this skill or its supporting docs (`text-principles.md`, etc.), and might be worth adding?** Scoring/matching logic, subagent prompt engineering details, technical bugs caught by trial rather than by instruction, and similar gap-filling all count — even when they were handled well, naming them is what turns tacit know-how into something the next lab doesn't have to rediscover from scratch.
- **What did the user have to explicitly ask for that I didn't do on my own?** Include things skipped because a hard rule discouraged them, things not proposed because they hadn't separately out-ranked an incumbent yet, and habits (like logging a lesson, or proposing a skill patch) that only happened once asked. Each one is a candidate for a standing discipline, a required check, or a rule adjustment — the same way earlier answers to this exact question produced several of the steps and standing disciplines already in this file.

Report the answers to both questions to the user, and treat anything found as material for this step's proactive patch-drafting above rather than a one-off answer to file away.
