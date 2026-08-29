---
name: skill-scorer
description: Grade a finished skill against its own SCORING.md rubric using a set of test prompts (from skill-test-prompts-post) and their results. Produces per-criterion scores with justification tied to specific test results, an overall score out of 10, and cross-prompt failure patterns. Use when someone wants to know how well a skill actually performs against its scoring framework, wants a one-shot grading pass, or asks things like "score this skill," "grade this against SCORING.md," "how well does this skill actually do on its test prompts." Do NOT use this if no SCORING.md exists yet (that's skill-scoring-framework's job — run it first), if no test prompts exist yet (that's skill-test-prompts-post's job), or to compare two versions/revisions of a skill (this is one-shot grading only, not a diff). Do NOT use this to generate new test prompts or to edit the skill being graded.
---

# Skill Scorer

## Purpose

Take a skill's `SCORING.md` (from `skill-scoring-framework`) and a set of test prompts (from `skill-test-prompts-post`), get results for each prompt, and grade the skill: a score and justification for each criterion, an overall score out of 10, and any patterns across failures worth noticing. This is a one-shot grading pass — it judges how the skill performs right now, on this set of results. It does not compare across revisions or track a skill's grades over time.

## Boundaries (read this first)

- **Requires `SCORING.md` to already exist.** If it doesn't, say so and point to `skill-scoring-framework` — don't improvise criteria as a substitute.
- **Requires test prompts to already exist.** If they don't, say so and point to `skill-test-prompts-post` — don't invent your own prompts to fill the gap.
- **Trust `SCORING.md`'s criteria as written.** Grade against what the rubric says matters, not against your own independent judgment of what should matter. If a criterion seems off or missing, note it briefly at the end, but grade against the rubric as it stands — a mismatch is feedback for a future `skill-scoring-framework` update, not something to silently correct here.
- **One-shot only.** If asked to compare this grading run against an earlier one, or to judge whether a revision improved things, say plainly that's out of scope for this skill and would need a separate comparison step — don't attempt an implicit diff.
- **Never edit the target skill.** Grading surfaces problems; fixing them is `skill-creator`'s job.
- **Never generate test prompts.** If the test set feels thin or is missing an obvious case, say so in the write-up, but that's `skill-test-prompts-post`'s job to fix, not this skill's.

## Step 1: gather what's needed

Confirm you have, or can get, all three:
1. The target skill's SKILL.md
2. Its `SCORING.md`
3. A set of test prompts for it (from `skill-test-prompts-post`)

If any are missing, stop and redirect to the right skill rather than proceeding with gaps.

## Step 2: get results for each test prompt

Check whether completed results (prompt + actual output, or a full transcript) already exist for this test set — the user may have already run them, or be handing you transcripts.

- **If results already exist**: use them directly. Don't re-run anything.
- **If results don't exist yet**, the right way to get them depends on the environment:

**In Claude Code or Cowork**: dispatch a subagent per test prompt. Each subagent should run fresh — no shared context with the conversation that's grading it, and no awareness of the target skill's authorship. This gives real isolation: the same instance that reasons about how a skill "should" behave isn't the one whose transcript gets judged. Collect each subagent's output before moving to Step 3.

**In this chat (no subagent capability)**: there's no way to isolate the run — the same conversation that will grade the results would also be the one producing them. Ask the user before doing anything: do they want you to run the test prompts yourself, one at a time, in this conversation (accepting that trade-off), or do they already have completed results to hand you instead? Don't default silently to either — this materially affects how much to trust the grading.

## Step 3: grade against each criterion

For each criterion in `SCORING.md`:
- Go through the test results and identify which ones speak to this criterion.
- Give a grade (use whatever scale the criterion implies — pass/fail, a short rating, or prose verdict — matching how `SCORING.md` frames it) with justification that cites specific test prompts/outputs, not a generic impression.
- If the test set doesn't actually cover this criterion (no prompt exercises it), say so plainly: give a best-effort judgment if there's any indirect signal, but flag clearly that the evidence is thin and the grade is a weak inference, not a confident read.

## Step 4: look for patterns across failures

Beyond grading each criterion in isolation, check whether failures cluster:
- Do multiple failures trace back to the same root cause (e.g., every miss involves ambiguous phrasing, or every over-triggering case involves a specific adjacent skill)?
- Does one scenario category from `skill-scenarios` account for a disproportionate share of the problems?

Name these patterns explicitly — they're often more actionable than the per-criterion grades alone.

## Step 5: overall score

Using `SCORING.md`'s holistic guidance for the overall score, assign a score out of 10 and explain how the per-criterion grades and patterns add up to that number. Don't apply a rigid formula if `SCORING.md` didn't specify one — use the same holistic judgment the rubric describes.

## Output format

- Per-criterion: grade + justification (with specific test references), or an explicit "insufficient evidence" flag
- Cross-prompt patterns, if any
- Overall score out of 10 with reasoning
- Optional closing note on rubric or test-set gaps noticed along the way (not fixed here, just flagged)

Keep it conversational and scannable rather than a dense report, unless the user is clearly running a larger structured process.
