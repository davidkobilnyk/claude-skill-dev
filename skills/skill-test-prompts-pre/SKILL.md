---
name: skill-test-prompts-pre
description: Generate test questions/prompts for a skill the user is planning to create, before it has been written. Use when someone is designing a new skill and wants test cases, edge cases, or example prompts to validate scope and triggering before drafting the SKILL.md — e.g. "what should I test before I build a skill for X", "give me test prompts for my planned skill", "help me figure out edge cases before I write this skill." Do NOT use this for auditing or writing test cases for a skill that already exists and is fully written — that is a different workflow (near-miss testing against an existing description), and this skill should say so and offer to switch modes rather than proceeding. Do NOT use for simple one-step tasks that don't need a skill at all — just do the task directly.
---

# Skill Test Question Generator

## Purpose

Generate test questions/prompts for a skill that is being **planned**, not yet built. These questions are an intent-capture step: they surface scope, edge cases, and triggering boundaries before any SKILL.md exists. They should inform the eventual skill description — never the other way around.

## Boundary: planning-stage vs. an existing skill

This skill is for skills that don't exist yet, or exist only as a rough, incomplete draft.

- *"What should I test before I write a skill for X?"* → in scope.
- *"Here's my finished skill, write test cases for it."* → out of scope for this workflow. Auditing an existing skill means probing for near-miss triggering against its actual, already-written description — a different exercise from blank-slate intent capture. Say this plainly, and offer to switch modes: pull test cases from the existing description's language and check for over- or under-triggering, rather than running the interview-first process below.
- A rough/incomplete SKILL.md draft sits in between. Ask whether the user wants scenario-based stress-testing (treat it like planning) or a structural critique of the draft itself (length, progressive disclosure, description clarity). Don't assume — ask once, briefly.

## Step 0: is a skill even warranted?

Skills only trigger for genuinely non-trivial tasks — a simple one-step query won't invoke a skill even with a perfect description, because Claude just handles it directly with basic tools. If the task the user describes is something Claude would do fine unassisted (e.g. "read this PDF and tell me what's in it"), say so and skip test-question generation rather than manufacturing a test set for a skill that isn't needed.

## Step 1: check whether scope is actually settled

Before writing any test questions, look for signs the scope isn't fixed yet: the user names two possible domains without picking one ("could be for invoices or receipts"), or describes the skill only by desired outcome without saying what varies across inputs.

If scope looks undecided, don't generate test questions yet. Ask 2–4 narrowing questions instead, such as:
- Do [variant A] and [variant B] need different handling, or is the underlying logic the same?
- Will inputs of each type ever be mixed in the same request, or are they always handled separately?
- Can you share one real example of each so the difference is concrete rather than assumed?
- Does the output structure differ between them?

Only move to question generation once scope is reasonably fixed — either the user answers, or explicitly says to proceed on an assumption.

## Step 2: determine skill type — verifiable vs. subjective

This determines the shape of every test question that follows.

- **Objectively verifiable output** (data extraction, format conversion, schema validation, fixed multi-step workflows): pair each test question with a specific expected outcome. Prefer cases that isolate one failure mode at a time (one type error, one missing field, one malformed input) over cases that bundle several issues together.
- **Subjective output** (writing style, tone, critique, taste-driven tasks): don't invent pass/fail assertions. Write prompts meant for qualitative human review, and note what a reviewer should actually look for (tone, accuracy, appropriateness) instead of a rigid grading rule.

If it's unclear which type applies, ask — or state the assumption you're making and proceed.

## Step 3: generate the question set

Default to about 5 questions (more for genuinely broad or high-stakes skills), covering, roughly in this order of priority:

1. **Core in-scope case** — the obvious, central use case the skill is being built for.
2. **Indirect phrasing** — a version that avoids the domain's obvious keywords, to check that the eventual description won't under-trigger on realistic phrasing. Under-triggering is the documented default failure mode for skill descriptions, so this case matters even when it feels redundant.
3. **A genuine edge case** — malformed input, missing data, an unusual but plausible variant.
4. **A near-miss / adjacent-but-out-of-scope case** — something that sounds related but should *not* invoke the skill, or should invoke only a narrower part of it. Label it explicitly as a near-miss.
5. **An implicit/recurring-context case** — a terse, shorthand request with no explicit instructions, the way a returning user would actually phrase a follow-up. Tests whether the skill (once built) will handle realistic brevity, not just fully-spelled-out asks.

Attach an expected result to each question if the skill type is verifiable; attach a reviewer-facing note (what to judge, not a pass/fail rule) if the skill type is subjective.

## Step 4: keep this decoupled from the skill's description

Do not draft the skill's description in the same pass as the test questions, and do not derive question phrasing from a description that's already been drafted. If asked for both at once: generate the test questions first, from realistic phrasing independent of any description; draft the description afterward, checked against the questions rather than used to produce them.

If explicitly asked to generate both together in one shot, briefly explain the risk — testing that Claude can match its own wording back to itself rather than testing real triggering — and propose the sequenced version instead.

## Output format

Present as a numbered list. For each question, include:
- The question/prompt itself
- One line naming what it's testing for (core case, under-triggering check, edge case, near-miss, implicit-context case, etc.)
- For verifiable-output skills: the expected result
- For subjective-output skills: what a reviewer should evaluate

Keep the presentation conversational — this is a planning aid, not a formal spec — unless the user is clearly running a larger structured process (many skills, a description-optimization loop), in which case a more structured table is appropriate.

## Scope of this skill

This skill covers generating the *initial* test question set only. Once the user starts actually drafting the skill, running these questions against it, and refining the description based on results, that's a fuller build-and-iterate workflow — flag that a broader skill-creation process would be the natural next step, but don't take it over unprompted.
