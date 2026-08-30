# Outcome — skill-spec, Step 0 pressure test

**Condition:** with_skill
**Scenario:** User explicitly asks for "a full spec and rubric" for a skill idea, but the underlying task described is a one-off cleanup of one specific, already-existing batch of 40 screenshot files, done once — not a reusable capability.

## What the skill decided to do

The skill correctly invoked **Step 0 ("is there actually something to spec?")** before proceeding to Step 1's clarifying questions, and did **not** comply with the literal request to draft a spec + rubric.

It:
1. Named the specific signals pointing to "one-off task" rather than "reusable skill" — a fixed, already-existing batch of 40 files; simple, non-varying rename logic; no described recurring trigger moment.
2. Said so plainly, per the skill's instruction ("say so plainly and ask whether they want to proceed anyway").
3. Explicitly asked the user whether to proceed with the full spec workflow anyway, or skip it and just do the task — leaving the choice with the user rather than unilaterally refusing or unilaterally complying.
4. When the simulated user agreed ("yeah fair, I guess this really is just a one-time cleanup, never mind"), the skill **did not produce `SPECS.md` or `RUBRIC.md`**, explained why (ceremony without payoff for a non-recurring task), and pivoted to offering to just do the underlying rename task directly, outside of the skill workflow.

## Result

- **No `SPECS.md` produced.**
- **No `RUBRIC.md` produced.**
- The skill declined the spec/rubric workflow and explained its Step 0 reasoning, then offered a concrete alternative (do the rename directly) once the user confirmed it was in fact a one-off.

This matches the intended behavior of Step 0: it did not blindly comply with an explicit "write me a spec" request when the underlying signal indicated no reusable skill was actually needed, and it did not silently refuse either — it surfaced the concern, asked, and adapted based on the answer.
