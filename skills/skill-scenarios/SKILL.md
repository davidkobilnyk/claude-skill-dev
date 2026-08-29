---
name: skill-scenarios
description: Given an already-drafted SKILL.md, identify the categories of real-world scenarios someone might hit when using that skill — including edge cases and failure modes — so the skill's author can spot gaps in coverage before shipping it. Use whenever someone shares a finished or near-finished skill file and asks what scenarios to plan for, what they might be missing, what could go wrong, or wants a coverage check — even if they don't use the word "scenarios" (e.g. "what am I not thinking about with this skill", "stress-test this before I ship it", "what edge cases apply here"). Do NOT use this for a skill that hasn't been written yet (that's planning-stage work, a different skill's job) and do NOT use this to generate sample test prompts or trigger phrases for those scenarios — this skill stops at naming and explaining the scenario categories themselves.
---

# Skill Scenarios

## Purpose

Take a finished (or near-finished) SKILL.md and map out the categories of situations someone might actually be in when they invoke it — the ordinary case, the messy variants, the edge cases, and the ways it could quietly fail. The output is a short, scannable list of categories with why each one matters. Nothing more.

This is a coverage-mapping tool, not a critique tool and not a test-generation tool. It doesn't grade the skill's writing, description, or structure, and it doesn't produce prompts to run against the skill.

## Boundaries (read this first)

- **Input is the SKILL.md itself, nothing else.** Don't ask the user for transcripts, example conversations, or more detail before starting — work with whatever is in the file. If the file is thin (a one- or two-line description, no examples, no body), still produce the best category list you can from what's there. A short file just means fewer categories will be well-supported — say so briefly rather than stalling to ask for more.
- **Stop at naming scenarios.** If asked to also generate example prompts, trigger phrases, or test cases for these scenarios, say plainly that this is a downstream step (a test-prompt-generation skill's job, if the user has one) and don't produce them yourself.
- **Don't review the skill.** Resist the pull to comment on the skill's description quality, triggering risk, length, or writing style — even if something jumps out. That's a different workflow. Stay focused on "what situations would a user of this skill be in," not "is this skill well-made."
- **Only for skills that already exist.** If someone describes a skill idea that hasn't been drafted yet, this isn't the right tool — that's a planning/ideation conversation, not a coverage check on a written artifact. Say so.

## How to generate the categories

Read the full SKILL.md — frontmatter description and body. Then think through where it could be used from several angles, and pull out the categories that are actually significant for *this* skill (skip angles that don't apply):

- **The core case** — the obvious, central way this skill gets used.
- **User expertise/context variation** — a novice vs. an expert user, a first-time user vs. someone using it repeatedly with shorthand requests.
- **Input format/quality variation** — clean vs. messy, complete vs. partial, structured vs. freeform, differently-formatted inputs the skill might receive.
- **Underlying intent variation** — the same surface request made for meaningfully different reasons or with different downstream goals.
- **Edge cases** — unusual but plausible situations: missing data, conflicting instructions, an input at the boundary of what the skill covers.
- **Failure modes** — ways the skill could produce a technically-following-instructions but unhelpful or wrong result, or could be invoked in a situation it's not actually equipped to handle well.

Not every skill will have something meaningful to say in every one of these buckets — don't pad the list with a weak, generic entry just to cover a bucket. Only surface categories that are genuinely significant given what this specific skill does.

## Output format

A list of categories. For each one:

- **A short name/label** for the scenario type
- **A one- or two-sentence description** of the scenario itself
- **A brief explanation of why it matters** — what could go right or wrong here, or what the skill's author should think about

Cap the list at around 7 categories. If the skill is broad enough that more significant categories exist beyond that, stop at 7, say plainly that there are more worth considering, and ask the user if they'd like to see them. Don't silently truncate and don't dump everything at once by default.

Keep the tone conversational and the list scannable — this is meant to be read in a couple of minutes, not studied like a spec.

## Example

Given a skill for summarizing meeting notes into action items, a good output looks like:

**1. Clean, well-structured notes (core case)**
The notes clearly separate discussion from decisions, with names attached to action items.
Why it matters: this is the baseline the skill should nail — if this isn't solid, nothing else matters.

**2. Freeform or stream-of-consciousness notes**
Notes with no headers, mixed topics, and action items buried mid-paragraph rather than listed.
Why it matters: the skill needs to extract structure that isn't already there, not just reformat existing structure.

**3. No clear action items present**
Notes that are purely informational — a status update with no decisions or follow-ups.
Why it matters: the skill should recognize this and say so rather than inventing action items to fill the output.

**4. Ambiguous ownership**
An action item is mentioned but it's unclear who owns it ("someone should follow up on this").
Why it matters: silently assigning an owner could create real confusion; the skill should flag ambiguity instead of guessing.

...and so on, stopping around 7 and asking if the user wants more if applicable.
