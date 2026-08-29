---
name: skill-test-prompts-post
description: Generate test prompts for a skill that already exists and is fully written, covering BOTH triggering behavior (does it fire when it should, and correctly not fire on near-misses) AND output quality once triggered. Use when someone has a finished SKILL.md and wants test cases, an audit, or a way to sanity-check it — e.g. "write test prompts for this skill," "audit this skill's triggering," "give me test cases to check if this skill actually works well," "stress-test my finished skill." Builds on skill-scenarios' category output as shared scaffolding for both triggering and quality prompts, running that skill's logic first if it hasn't already been applied. Do NOT use this for a skill that hasn't been written yet or is still a rough draft — that is skill-test-prompts-pre's job, and this skill should say so and offer to switch. Do NOT use this to only name scenario categories without producing runnable prompts — that bare version is skill-scenarios' job.
---

# Skill Test Prompt Generator (Post-Build)

## Purpose

Generate a set of runnable test prompts for a skill that is **already written** — a finished or near-finished SKILL.md. Unlike its sibling `skill-test-prompts-pre` (which captures intent before a skill exists), this skill audits something concrete: the actual description and instructions that are already on the page.

The output covers two angles at once, from a shared set of scenario categories:
1. **Triggering** — does the skill fire on the prompts it should, and correctly *not* fire (or fire only narrowly) on near-misses and adjacent cases?
2. **Quality** — once triggered, does the skill's instructions actually produce a good result for that situation?

This skill stops at producing the prompt list. It does not run the prompts, grade results, or rewrite the skill — those are `skill-creator`'s job downstream.

## Boundary: existing skill vs. planning-stage idea

- *"Here's my finished skill, write test cases for it."* → in scope.
- *"I'm thinking about building a skill for X, what should I test?"* → out of scope. No SKILL.md exists yet, so there's nothing to audit — that's `skill-test-prompts-pre`'s job (blank-slate intent capture). Say so and offer to switch.
- A rough/incomplete draft sits in between — if the draft is thin enough that scope itself still feels unsettled, say so and suggest `skill-test-prompts-pre` or `skill-coach` instead of forcing an audit onto something that isn't stable yet.

## Step 1: get scenario categories

Check whether `skill-scenarios` has already been run on this SKILL.md earlier in the conversation.

- **If yes**: reuse that category output directly — don't regenerate it.
- **If no**: read `/mnt/skills/user/skill-scenarios/SKILL.md` and follow its process yourself against the target SKILL.md to produce the category list (core case, expertise/context variation, input variation, intent variation, edge cases, failure modes — capped around 7, only the categories genuinely significant for this skill).

These categories are scaffolding for this skill's output, not the deliverable — don't just hand back the category writeup on its own.

## Step 2: turn each category into prompts, on both angles

For each scenario category, consider both angles and use whichever genuinely applies — don't force both onto every category:

- **Triggering angle**: would a realistic prompt drawn from this category actually invoke the skill? This fits naturally for categories like a near-miss/adjacent-but-out-of-scope case, terse shorthand from a returning/expert user, or an edge case sitting right at the skill's boundary.
- **Quality angle**: once triggered, does the skill's instructions actually handle this case well? This fits naturally for categories like input format/quality variation, underlying intent variation, or failure modes.

Some categories will only yield a good prompt for one angle — that's fine, don't pad the other angle in artificially.

If, after going through the categories, the set is missing an obvious baseline check, fill the gap directly rather than leaving it out:
- No plain core-case phrasing check → add one.
- No indirect/keyword-avoiding phrasing check (the classic under-triggering failure mode) → add one.

## Step 3: assign expected outcomes

- **Triggering prompts**: expected outcome is one of *should trigger*, *should not trigger*, or *should trigger, but only narrowly / partially*.
- **Quality prompts**: follow the same verifiable-vs-subjective split as `skill-test-prompts-pre`:
  - Objectively verifiable output → pair with a specific expected result.
  - Subjective output (style, tone, judgment-driven) → pair with reviewer notes: what a human should actually look for, not a pass/fail rule.
  - If unclear which applies, ask, or state the assumption and proceed.

## Output format

Present as a numbered list. For each prompt, include:
- The prompt itself
- The scenario category it came from (or "baseline check" if added in Step 2's gap-fill)
- Which angle(s) it tests — triggering, quality, or both
- The expected outcome (trigger verdict for triggering prompts; expected result or reviewer notes for quality prompts)

Default to one prompt per significant scenario category (so the set naturally scales up to ~7), plus any baseline checks added to fill gaps. Don't pad the list to hit a target count — a skill with only 3 significant categories should produce a shorter set, not a stretched one.

Keep the presentation conversational and scannable unless the user is clearly running a larger structured process, in which case a table is fine.

## Scope of this skill

This covers generating the test prompt set only. It does not run the prompts, grade the outputs, or touch the skill's description/instructions. If the user wants to actually execute these prompts and iterate on the skill based on results, that's `skill-creator`'s eval loop — mention it only if asked, don't volunteer a handoff unprompted.
