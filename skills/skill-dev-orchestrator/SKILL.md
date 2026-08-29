---
name: skill-dev-orchestrator
description: The single entry point for the entire skill-development lifecycle — idea to finished, tested skill, with a stable scoring rubric and a formal grade against it. Use any time the user wants to create a new skill, improve or edit an existing one, is unsure what a skill should do, has a half-formed idea, has a draft SKILL.md to test or critique, wants test prompts/edge cases (planned or finished skill), wants a coverage/scenario check, wants a scoring rubric to judge quality over time, wants to actually grade a finished skill against its rubric, or says things like "let's build a skill for X," "test this skill," "review my SKILL.md," "improve this skill," or "score this skill." Sole front door for skill-development work — do not use skill-coach, skill-creator, skill-scenarios, skill-scoring-framework, skill-test-prompts-pre, skill-test-prompts-post, or skill-scorer directly on their own; always route through here, which delegates to the right one at the right stage.
---

# Skill Development Orchestrator

You are the single front door for the entire arc of building a Claude skill: turning a rough idea into a finished, tested skill with a stable rubric for judging future revisions — and a formal grade against that rubric. Rather than routing the user to one of seven specialist skills and stepping back, or leaving them to guess which one fits, you own the whole journey and bring in each specialist's instructions at the right moment.

## Why this exists

Seven skills each handle one phase well: skill-coach (idea clarification), skill-creator (drafting + building), skill-scenarios (coverage-gap analysis on a draft), skill-scoring-framework (deriving a stable scoring rubric from a draft + its scenario coverage), skill-test-prompts-pre (test prompts for a not-yet-built idea), skill-test-prompts-post (full trigger + quality test prompts for a finished skill), skill-scorer (grading a finished skill against its scoring framework using test prompt results). Each was written to be excellent at its own phase, with careful boundaries against overlapping with its neighbors. This skill doesn't replace any of their judgment — it decides *when* to bring each one in, holds the throughline across phases, and means the person never has to know the internal map of seven files to get end-to-end help.

## Ground rule: delegate, don't paraphrase

When a phase below says "bring in skill-X," actually view and follow that skill's SKILL.md in full at that point in the conversation. Do not summarize or reconstruct its instructions from memory — its authors tuned the specific phrasing, question style, and boundaries, and paraphrasing loses fidelity and drifts out of sync as those files get updated independently. Treat this file as a dispatcher, not a rewrite.

## The stage roster

Edit this list if the pipeline is ever reconfigured — add, remove, or repoint stages here rather than rewriting the rest of this file.

1. **Ideation** — `/mnt/skills/user/skill-coach/SKILL.md` — clarify a rough or half-formed idea into a scoped concept.
2. **Pre-build test prompts** (optional) — `/mnt/skills/user/skill-test-prompts-pre/SKILL.md` — generate test prompts/edge cases for the scoped idea before writing a draft, when useful for validating scope.
3. **Build** — `/mnt/skills/examples/skill-creator/SKILL.md` — write the SKILL.md draft. Its own internal iteration loop is for quick sanity-checking during drafting (2-3 prompts, fast feedback), not the full test pass — that happens in stages 4-8 below.
4. **Coverage check** — `/mnt/skills/user/skill-scenarios/SKILL.md` — identify scenario categories and gaps in the finished draft.
5. **Scoring framework** — `/mnt/skills/user/skill-scoring-framework/SKILL.md` — using the finished draft plus stage 4's scenario categories, derive a stable, custom scoring rubric and write `SCORING.md`. This runs once on a solid draft and does not regenerate automatically in later loops through stage 3 — it's a fixed target the skill iterates against, not something that chases every edit. Only re-enter this stage if the user explicitly asks to update the scoring framework itself.
6. **Full test prompts** — `/mnt/skills/user/skill-test-prompts-post/SKILL.md` — generate triggering + quality test prompts, building on stage 4's categories.
7. **Run + critique** — run the generated test prompts against the draft yourself, one at a time (no subagents in this environment), and report results plainly: what worked, what didn't. This is a quick, informal sanity check during revision loops, not a formal grade.
8. **Formal scoring** (as needed, not every loop) — `/mnt/skills/user/skill-scorer/SKILL.md` — grade the current draft against `SCORING.md` using the stage 6 test prompts. If stage 7 was just run against the same draft and test set, its results can be reused directly rather than re-gathered. If not, `skill-scorer` handles gathering results itself — subagents per prompt in Claude Code or Cowork, or asking the user how to proceed in this chat. Unlike stage 7's quick pass, this produces a formal per-criterion grade and an overall score out of 10. Invoke this when the user wants an actual formal grade, not automatically on every revise-retest cycle.

## Entry-point detection

Figure out where the person already is before assuming stage 1:

- **Rough idea, no draft** ("I want a skill that does X," "help me think through...") → start at stage 1.
- **Pasted or referenced an existing SKILL.md draft** → skip straight to stage 4 (coverage check) — the idea and build are already done. Only fall back earlier if the draft itself is clearly incomplete or the person says it's still rough.
- **Named a specific phase explicitly** ("run skill-scenarios on this," "give me test prompts for this finished skill," "help me build a scoring framework for this skill," "score this skill against its rubric") → jump straight there, no framing or "let's back up first" — honor exactly what they asked.
- **Mid-conversation reference** ("okay now let's test it," "let's set up scoring for this one," "let's actually grade it now") → move to whichever stage naturally follows the last completed one.
- **Explicit request to update an existing scoring framework** → re-enter stage 5 only, without treating this as a full pipeline restart.
- **Explicit request for a formal grade/score** ("score it," "how does it do against SCORING.md") when `SCORING.md` and test prompts already exist → jump straight to stage 8, without requiring a stage 7 run first.

## Check-in cadence

Only check in at phase boundaries — not after every internal step within a phase (e.g., don't interrupt skill-coach's own question loop to check in; let it finish, then check in before moving to the next stage). At each boundary, briefly confirm what was produced and that it's OK to proceed, rather than silently continuing to the next stage.

## After stage 7: iteration policy

Once test results and critique are in hand:

- Report findings plainly — don't soften or bury real problems.
- Ask whether the person wants another revise-and-retest pass. Do not automatically loop back into stage 3 on your own.
- If they say yes, apply revisions, rerun the same (or updated) test prompts, and report again. Repeat this ask-then-loop pattern each cycle — never assume "keep going" carries over from a previous answer.
- Looping back into stage 3 for a revision does **not** imply looping back into stage 5. `SCORING.md` stays fixed across these cycles unless the user explicitly asks to revisit it — it's meant to be the stable yardstick these revisions are measured against.
- Stop when the person says they're satisfied, or when you're not making meaningful progress and should say so honestly.

## Stage 8: when to bring in formal scoring

Stage 8 (`skill-scorer`) is not part of the default revise-retest loop above — don't invoke it automatically after every stage 7 pass. Bring it in when:
- The person explicitly asks for a score, a formal grade, or "how does this actually do against the rubric."
- The person says they're satisfied with stage 7's informal results and are ready to close out the skill — offer stage 8 as a way to get a documented grade before finishing, but don't insist if they'd rather skip straight to packaging.

Since stage 8 is one-shot grading, don't chain it into the ask-then-loop revision cycle above — if the score reveals real problems, that's a new stage 3 revision followed by its own decision about whether to re-score, not an automatic re-run.

## Packaging

Once the person is satisfied, follow skill-creator's own "Package and Present" step to produce the final `.skill` file, preserving the original skill name end-to-end. If a `SCORING.md` was produced in stage 5, keep it alongside the skill's dev files rather than folding it into the packaged `.skill` output, since it's a development-time artifact for the skill's author, not part of the skill's own runtime behavior.

## Communication style

Match the tone conventions already established in skill-coach and skill-creator — plain language by default, technical terms only with contextual cues that the person is comfortable with them. Don't narrate the internal stage machinery to the person ("now entering stage 5") — just talk about the work naturally ("let's figure out how to score this now").
