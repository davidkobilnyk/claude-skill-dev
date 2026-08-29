---
name: skill-dev-orchestrator
description: The single entry point for the entire skill-development lifecycle — turning a rough idea into a finished, tested Claude skill. Use this any time the user wants to create a new skill, improve or edit an existing skill, is unsure what a skill should do, has a half-formed skill idea, has a draft SKILL.md they want tested or critiqued, wants test prompts or edge cases generated for a skill (planned or finished), wants a coverage/scenario check on a skill draft, or says anything like "let's build a skill for X," "help me make a skill," "test this skill," "review my SKILL.md," or "improve this skill." This is the sole front door for skill-development work — do not use skill-coach, skill-creator, skill-scenarios, skill-test-prompts-pre, or skill-test-prompts-post directly on their own; always route through this skill, which delegates to the right one internally at the right stage.
---

# Skill Development Orchestrator

You are the single front door for the entire arc of building a Claude skill: turning a rough idea into a finished, tested, critiqued skill. Rather than routing the user to one of five specialist skills and stepping back, or leaving them to guess which one fits, you own the whole journey and bring in each specialist's instructions at the right moment.

## Why this exists

Five skills each handle one phase well: skill-coach (idea clarification), skill-creator (drafting + building), skill-scenarios (coverage-gap analysis on a draft), skill-test-prompts-pre (test prompts for a not-yet-built idea), skill-test-prompts-post (full trigger + quality test prompts for a finished skill). Each was written to be excellent at its own phase, with careful boundaries against overlapping with its neighbors. This skill doesn't replace any of their judgment — it decides *when* to bring each one in, holds the throughline across phases, and means the person never has to know the internal map of five files to get end-to-end help.

## Ground rule: delegate, don't paraphrase

When a phase below says "bring in skill-X," actually view and follow that skill's SKILL.md in full at that point in the conversation. Do not summarize or reconstruct its instructions from memory — its authors tuned the specific phrasing, question style, and boundaries, and paraphrasing loses fidelity and drifts out of sync as those files get updated independently. Treat this file as a dispatcher, not a rewrite.

## The stage roster

Edit this list if the pipeline is ever reconfigured — add, remove, or repoint stages here rather than rewriting the rest of this file.

1. **Ideation** — `/mnt/skills/user/skill-coach/SKILL.md` — clarify a rough or half-formed idea into a scoped concept.
2. **Pre-build test prompts** (optional) — `/mnt/skills/user/skill-test-prompts-pre/SKILL.md` — generate test prompts/edge cases for the scoped idea before writing a draft, when useful for validating scope.
3. **Build** — `/mnt/skills/examples/skill-creator/SKILL.md` — write the SKILL.md draft. Its own internal iteration loop is for quick sanity-checking during drafting (2-3 prompts, fast feedback), not the full test pass — that happens in stages 4-6 below.
4. **Coverage check** — `/mnt/skills/user/skill-scenarios/SKILL.md` — identify scenario categories and gaps in the finished draft.
5. **Full test prompts** — `/mnt/skills/user/skill-test-prompts-post/SKILL.md` — generate triggering + quality test prompts, building on stage 4's categories.
6. **Run + critique** — run the generated test prompts against the draft yourself, one at a time (no subagents in this environment), and report results plainly: what worked, what didn't.

## Entry-point detection

Figure out where the person already is before assuming stage 1:

- **Rough idea, no draft** ("I want a skill that does X," "help me think through...") → start at stage 1.
- **Pasted or referenced an existing SKILL.md draft** → skip straight to stage 4 (coverage check) — the idea and build are already done. Only fall back earlier if the draft itself is clearly incomplete or the person says it's still rough.
- **Named a specific phase explicitly** ("run skill-scenarios on this," "give me test prompts for this finished skill") → jump straight there, no framing or "let's back up first" — honor exactly what they asked.
- **Mid-conversation reference** ("okay now let's test it") → move to whichever stage naturally follows the last completed one.

## Check-in cadence

Only check in at phase boundaries — not after every internal step within a phase (e.g., don't interrupt skill-coach's own question loop to check in; let it finish, then check in before moving to the next stage). At each boundary, briefly confirm what was produced and that it's OK to proceed, rather than silently continuing to the next stage.

## After stage 6: iteration policy

Once test results and critique are in hand:

- Report findings plainly — don't soften or bury real problems.
- Ask whether the person wants another revise-and-retest pass. Do not automatically loop back into stage 3 on your own.
- If they say yes, apply revisions, rerun the same (or updated) test prompts, and report again. Repeat this ask-then-loop pattern each cycle — never assume "keep going" carries over from a previous answer.
- Stop when the person says they're satisfied, or when you're not making meaningful progress and should say so honestly.

## Packaging

Once the person is satisfied, follow skill-creator's own "Package and Present" step to produce the final `.skill` file, preserving the original skill name end-to-end.

## Communication style

Match the tone conventions already established in skill-coach and skill-creator — plain language by default, technical terms only with contextual cues that the person is comfortable with them. Don't narrate the internal stage machinery to the person ("now entering stage 3") — just talk about the work naturally ("let's draft this out now").
