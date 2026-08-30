---
name: skill-spec
description: Turn a rough skill idea into two durable, buildable documents — SPECS.md (a build-ready specification: purpose, trigger conditions, inputs/outputs, scope boundaries, non-goals, edge cases) and RUBRIC.md (a tailored scoring rubric derived from that spec). Use this whenever someone wants a written spec and matching rubric for a skill idea that's detailed enough for someone else to build and later judge from, with no further clarification needed — not just a casual brainstorm. Trigger on requests like "write up a full spec for this skill idea," "I want a detailed spec and rubric before we build this," "flesh this idea out into something buildable," or "spec this out." Goes deep: expect thorough, in-depth questioning across purpose, inputs, variation, edge cases, and success criteria before anything gets written — more probing than a quick clarifying chat. Always converges on exactly ONE spec and ONE rubric per run; never produces multiple competing candidate specs side by side. Does not write any SKILL.md content itself, and does not score or apply the rubric it produces — those are separate, later steps for someone else to do.
---

# Skill Spec

## Purpose

Take a rough, half-formed skill idea and turn it into two finished, standalone documents:

- **`SPECS.md`** — a specification detailed enough that someone could build the actual skill directly from it, without asking any follow-up questions.
- **`RUBRIC.md`** — a scoring rubric, tailored to that specific spec, describing what "good" would look like once the skill exists.

This skill's job ends there. It never writes the skill itself, and it never applies the rubric to anything. Both documents are deliverables meant to be picked up and used by someone (or something) else, later.

## Step 0: is there actually something to spec?

If the request is really a one-off task with no signal that a *reusable* skill is wanted, say so plainly and ask whether they want to proceed anyway rather than forcing this workflow onto something that doesn't need it.

## Step 1: take stock of what's known vs. unknown

Before asking anything, note what's already been said (in this message or earlier in the conversation) versus what's still vague. Never re-ask something already answered.

This skill needs to go deeper than a casual "let's think this through" conversation — the bar for `SPECS.md` is that someone could build from it with zero follow-up questions, so treat every gap below as something that must be pinned down, not just touched on:

1. **Core job** — What should the finished skill make possible? What's the trigger moment — what does someone say or do right before they'd want it to fire?
2. **Inputs** — What comes in? Does it vary in format, structure, or completeness? Are there real examples to ground this in?
3. **Variation** — Are there genuinely different approaches to solving this, or is the underlying logic the same regardless of surface differences? (See Step 3 for why this matters — this skill converges to one spec, so real forks need to be resolved here, through questions, not left for later.)
4. **Output** — What does "done" look like? Fixed and checkable, or more subjective (tone, style, judgment calls)?
5. **Edge cases** — What's the messiest or most malformed input this could realistically see? What should happen when something's missing, ambiguous, or contradictory?
6. **Boundaries** — What should this explicitly *not* do? Where's the line past which it should stop and hand off (to a person, a different tool, a judgment call) rather than push forward?
7. **Success/failure** — How would someone know if the finished skill did a bad job? What past frustration is this meant to specifically fix?

Not every gap needs its own question — group naturally where it helps.

## Step 2: ask, don't assume

Ask a handful of questions at a time, in plain conversational language — no unexplained jargon unless the person has already used those terms themselves. If the idea is extremely thin (a single word or fragment), start with grounding questions before anything else.

Keep iterating — ask, listen, ask again — until every gap in Step 1 is concrete enough to write down without guessing, and any genuine fork in approach has been resolved down to one direction (see Step 3). Don't rush this: under-clarifying here produces a `SPECS.md` that looks complete but isn't actually buildable-without-follow-up, which defeats the point of the exercise.

If the person explicitly says to proceed on a stated assumption rather than keep answering, that's fine — just record the assumption plainly in the spec rather than silently smoothing it over.

### If the idea seems to fork into multiple approaches

This skill always produces exactly one `SPECS.md`, never several side-by-side candidates. If the conversation surfaces more than one plausible approach:

- First, try to resolve it with more questions — ask which direction actually matches the underlying need, or whether the "two approaches" are really the same thing described differently.
- If a genuine, worthwhile fork remains and there's no way to pick one, don't stall indefinitely — ask the person to pick a direction, or note the alternative as a called-out consideration *within* the single spec (e.g., a short "alternative approach considered" note under the relevant section), rather than writing a second document.

## Step 3: draft `SPECS.md`

Write the specification once you're confident every Step 1 gap is settled. This is a lightweight PRD, not implementation detail — describe *what* the skill should do and where its edges are, not code or prompt engineering.

Required sections:

```markdown
# Spec: <name/working title>

## Purpose
What this skill makes possible, in a sentence or two, plus the underlying need it addresses.

## Trigger conditions
What a person says or does that should cause this to fire. Include both clear-cut phrasings and less obvious ones. Note anything that looks similar but should NOT trigger it.

## Inputs
What comes in, expected formats/structure, how much it varies, and how completeness/quality might differ.

## Outputs
What "done" looks like. If there's a fixed structure, spell it out. If it's more subjective, describe the qualities that make an output good.

## Scope & boundaries
What this explicitly handles, and where it should stop, hand off, or decline.

## Non-goals
What this is deliberately NOT trying to do, even if adjacent or tempting to fold in.

## Edge cases
The messiest realistic inputs and what should happen with each — missing data, ambiguous requests, malformed input, conflicting signals.

## Open assumptions
Anything decided by assumption rather than explicit answer, stated plainly so it's visible to whoever builds from this.
```

Every section should be concrete enough that a builder wouldn't need to come back and ask "but what about X" — if you notice a section is vague while writing it, that's a signal to go back and ask more questions rather than paper over the gap.

## Step 4: draft `RUBRIC.md`

Once `SPECS.md` is written, derive a scoring rubric from it — not a generic checklist, but criteria that follow specifically from what this spec says the skill is for and where its edges are.

1. Always include **triggering accuracy** as two sides of one criterion: firing when the trigger conditions in the spec are met, and staying quiet on things that merely look similar (the near-misses named in the spec's trigger conditions section).
2. From the spec's purpose, outputs, and edge cases, derive additional criteria — the specific things *this* skill would need to get right to be worth using. Ground each one in a concrete section of `SPECS.md`, not a generic template.
3. Aim for around 4–6 criteria total (including triggering accuracy). Go beyond that only when a genuinely distinct, important criterion would otherwise be dropped.

Format, mirroring `SPECS.md`'s directness:

```markdown
# Rubric: <name/working title>

## Criteria

### 1. Triggering accuracy
<prose: what firing correctly and staying quiet correctly both look like, grounded in the spec's trigger conditions>

### 2. <spec-derived criterion>
<prose: what doing this well looks like for this specific skill, and what a clear failure looks like>

...

## Overall score (out of 10)
<prose describing how to judge holistically — not a rigid formula, a description of what a 9-10 vs. a 5-6 looks like>
```

This document is a deliverable, not something this skill applies to anything — it's handed off unused, ready for whoever later tests and grades the finished skill.

## Step 5: self-evaluate before showing the user

Before presenting the draft, reread both documents adversarially, as if you were the person who'd have to build from `SPECS.md` with no further access to ask questions:

- Is there any section that's vague, generic, or could be interpreted more than one way?
- Does any rubric criterion fail to trace back to something specific in the spec?
- Did an edge case get named in Step 1 but not actually addressed in the spec?
- Is either document ballooning in a way that suggests scope crept beyond the original idea?

Note what you find, fix what you can fix yourself, and flag anything you're genuinely unsure about rather than silently picking an answer.

## Step 6: loop with the user

Present both documents along with your self-evaluation notes. Ask directly whether it looks buildable and whether the rubric feels like it captures what would actually matter. Revise based on their feedback — and re-run the Step 5 self-check after any nontrivial revision — until both you and the person are satisfied. Then stop; the job is done.

## Hard boundaries (never cross these)

- **Never write any SKILL.md content** — not the frontmatter, not instructions, not even a rough skeleton or example. Stay at the specification level, however tempting it is to sketch ahead.
- **Never score or apply the rubric.** `RUBRIC.md` is a deliverable, not a tool this skill uses on anything — don't grade the spec against it, don't grade anything else against it.
- **Never produce more than one spec per run.** No side-by-side candidate documents, no `SPECS-v1.md` / `SPECS-v2.md`. Resolve forks through questions (Step 2) instead.
- **Watch the size of both files.** If it becomes clear that `SPECS.md` or `RUBRIC.md` is headed past roughly 30,000 tokens, stop and check with the person before continuing to expand it — that's usually a sign the idea is actually several skills, or that detail is being added past the point of usefulness.
- **Don't assume a new skill is warranted** (Step 0) — a one-off task dressed up as a skill idea doesn't need this treatment.

## Tone

A thorough planning conversation, not an interrogation and not a rubber stamp. Ask naturally, react to what the person actually says, and take the extra rounds of questioning seriously — the entire value of this skill is that the output needs no follow-up, so shortcuts in the conversation show up later as gaps in the spec.
