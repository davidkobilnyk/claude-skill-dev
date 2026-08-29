---
name: skill-scoring-framework
description: Given a drafted SKILL.md and its skill-scenarios categories, work with the user to derive a custom scoring rubric and write SCORING.md — stable prose criteria (always including under- and over-triggering accuracy, plus criteria specific to the skill's purpose) with an overall score out of 10. Use when someone wants to define what "good" looks like for a finished skill, wants a rubric to judge it against over time, or asks "how should this skill be judged," "set up scoring before I iterate," or "how do I know if future edits are improvements" — even without the word "scoring." Do NOT use to generate test prompts (skill-test-prompts-post's job), to score a skill against actual test results (a separate future skill's job), or to edit the target SKILL.md — redirect instead. Do NOT use on a skill with no real draft yet; run skill-scenarios on a finished draft first.
---

# Skill Scoring Framework

## Purpose

Take a finished (or near-finished) SKILL.md, together with the scenario categories `skill-scenarios` identified for it, and turn them into a durable scoring rubric: a small set of prose criteria, each capturing something the skill genuinely needs to get right, plus an overall score out of 10. The output is `SCORING.md` — a fixed target that the skill's author can keep drafting *against* as the skill goes through revisions, and that a future scoring skill will use to grade the skill's actual performance on test prompts.

This is a rubric-design tool, not a test-generation tool and not a scoring-execution tool. It doesn't write test prompts, and it doesn't grade any particular run of the skill.

## Boundaries (read this first)

This skill sits at a specific point in the pipeline, and mixing it up with its neighbors is the main failure mode:

- **Input is the SKILL.md plus its `skill-scenarios` output.** If scenario categories don't exist yet for this skill, say so and suggest running `skill-scenarios` first — don't invent scenario coverage from scratch as a substitute, and don't skip straight to criteria without it.
- **Never generates test prompts.** If asked for example prompts, trigger phrases, or test cases, say plainly that's `skill-test-prompts-post`'s job (which can later use this framework to write criteria-informed prompts) and don't produce them yourself.
- **Never scores a skill against actual outputs.** This skill defines *what* to judge, not *how a particular run did*. If asked to actually grade a transcript, a test run, or "how did the skill do here," say that's a downstream scoring skill's job (not yet built) and stop.
- **Never edits the target skill's SKILL.md.** Even if a gap in the rubric points at an obvious fix to the skill itself, don't make that edit here — note it if useful, but the fix belongs to `skill-creator`'s revision loop.
- **Only for skills that already have a real draft.** If the skill is still an idea being clarified, this isn't the right tool — that's `skill-coach` or `skill-test-prompts-pre`'s territory. Say so.
- **The framework is stable by design.** Don't regenerate or silently revise `SCORING.md` just because the target skill's SKILL.md changed. Only touch it when the user explicitly asks to update the scoring framework itself — the intent is a fixed target the skill iterates against, not a moving one.

## How to build the framework

### Step 1: Read the inputs

Read the full SKILL.md (frontmatter description and body) and the `skill-scenarios` categories for it. If scenario output isn't available, ask for it or offer to have the user run that skill first — don't proceed without it.

### Step 2: Propose candidate criteria, then iterate

Don't draft the full rubric in one pass. Instead:

1. Always start from two fixed criteria: **under-triggering accuracy** (does the skill fire when it should) and **over-triggering accuracy** (does it stay quiet when it shouldn't fire — on adjacent tasks, near-misses, or things a sibling skill should handle instead).
2. From the SKILL.md's actual purpose and values, plus the scenario categories, propose additional candidate criteria — the specific things *this* skill needs to get right (e.g., for a summarization skill: "preserves ownership/attribution accuracy"; for a tone-sensitive skill: "matches register without becoming stiff or robotic"). Ground each proposal in something concrete from the SKILL.md or scenarios, not a generic template.
3. Present the candidates to the user and ask which feel right, which are missing, and which don't actually matter for this skill. Ask clarifying questions where the skill's intent is ambiguous enough that you're not confident what "good" means here.
4. Keep iterating — propose, ask, revise — until the user is confident the criteria genuinely capture what this skill is supposed to achieve, not just what could go wrong with it.

This mirrors `skill-coach`'s interaction style: ask-then-refine, not draft-then-flag-uncertainty.

### Step 3: Size the list

Aim for around 5 criteria total (including the two fixed triggering criteria). Go beyond 5 only when a genuinely important, distinct criterion would otherwise be dropped — don't pad to hit a number, and don't force a sprawling skill into exactly 5 if it truly needs more. This mirrors `skill-scenarios`' soft cap of ~7.

### Step 4: Write SCORING.md

Each criterion should be prose, not a checklist item — a short paragraph that:
- Names the criterion
- Explains what "doing this well" looks like for *this specific skill*, not skills in general
- Notes what a clear failure looks like, when useful for making the criterion concrete

Close with an **overall score out of 10** — not a fixed formula for combining the criteria, but a short paragraph describing how the overall score should be judged holistically (e.g., "a skill scoring 9-10 nails triggering and handles every scenario category cleanly; a skill in the 5-6 range gets the core case right but has real gaps in edge-case handling..."). Leave the actual weighing of criteria against each other to judgment at scoring time, not a rigid formula here.

The criteria taken together should express what the skill is *for* — its underlying purpose and values — so that they remain useful for improving the skill indefinitely, not just as a one-time pass/fail gate.

### Step 5: Confirm and hand off

Once the user is satisfied, save the file as `SCORING.md` alongside the target skill's dev files. Note plainly that this file is meant to stay stable across future revisions of the skill, and that it should only be regenerated when the user explicitly asks to update the scoring framework itself — not automatically alongside skill edits.

## Output format

A single `SCORING.md` file:

```markdown
# Scoring Framework: <skill-name>

## Criteria

### 1. Under-triggering accuracy
<prose>

### 2. Over-triggering accuracy
<prose>

### 3. <Skill-specific criterion>
<prose>

...

## Overall Score (out of 10)
<prose describing how to judge holistically>
```

## Tone

Like `skill-coach`, this is a collaborative design conversation, not an audit. Plain language by default, and lean on concrete examples grounded in the actual SKILL.md rather than abstract rubric-speak.
