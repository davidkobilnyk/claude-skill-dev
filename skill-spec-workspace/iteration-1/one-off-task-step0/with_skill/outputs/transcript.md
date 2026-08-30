# Transcript — skill-spec, Step 0 pressure test ("one-off task dressed as a spec request")

**Test condition:** with_skill (skill-spec loaded and triggered)
**Date:** 2026-08-30

---

## Turn 1 — User

> I have 40 screenshot files in my Downloads folder all named randomly like 'Screenshot 2024-03-01 at 11.42.03 AM.png' and I want them renamed to something consistent like 'screenshot-001.png', 'screenshot-002.png' etc. Can you write up a full spec and rubric for a skill that does this before we build it?

---

## Turn 2 — Claude (skill-spec loaded)

Before I dive into a full spec-and-rubric workflow for this, I want to flag something (this is Step 0 of how I approach these — "is there actually something to spec?").

What you've described sounds like a one-off cleanup, not a reusable skill:

- It's a fixed, already-existing batch — 40 specific files sitting in your Downloads folder right now, not an open-ended stream of screenshots that will keep showing up.
- The rename logic is about as simple as it gets — sort by name (which for `Screenshot YYYY-MM-DD at H.MM.SS AM/PM.png` also sorts chronologically) and zero-pad an incrementing counter onto `screenshot-NNN.png`. There's no real variation, ambiguity, or judgment call to spec out.
- There's no described trigger moment where this would need to fire again later — no "every time I download a screenshot" or "whenever I dump a batch of images in this folder." It reads as "I have this pile right now, make it go away."

If that's accurate, building a full `SPECS.md` + `RUBRIC.md` for it is a lot of ceremony for a task I could just... do — I can rename the 40 files directly in a couple of minutes, no skill required.

That said, I could be wrong about the shape of this — so: is this genuinely a one-time cleanup of the batch you have today, or do you actually want something reusable (e.g., a skill you'd invoke again next month on a fresh batch of screenshots, maybe with different naming conventions, subfolders, collision handling, non-screenshot files mixed in, etc.)? If it's the latter, I'm glad to go through the full spec process properly. If it's the former, I'd suggest skipping the spec/rubric and just doing the rename now — happy to do either.

---

## Turn 3 — User (simulated, per test instructions)

> Yeah fair, I guess this really is just a one-time cleanup, never mind. I just have this one folder of 40 screenshots from a few different projects and I want them in order. I'm not going to be doing this again — I usually just leave screenshots named whatever the OS gives them. Just wanted them cleaned up for now. Let's skip the spec stuff, can you just rename them for me?

---

## Turn 4 — Claude (skill-spec loaded)

Got it — skipping the spec/rubric process, since this is confirmed as a one-off cleanup and not a reusable capability. That's exactly the kind of case Step 0 of this workflow exists to catch: forcing a full spec-and-rubric pass onto a single, already-known batch of files with no future recurrence would just be ceremony without payoff.

No `SPECS.md` or `RUBRIC.md` produced.

For the actual cleanup — happy to do it directly, outside of this skill: I'd list the 40 files in your Downloads folder, sort them by their timestamp (the `Screenshot YYYY-MM-DD at H.MM.SS AM/PM.png` naming already sorts correctly by date/time as a plain string sort in that format, but I'd parse the actual timestamp to be safe), and rename them in place to `screenshot-001.png` through `screenshot-040.png` — zero-padded to 3 digits since 40 fits comfortably under 1,000. I'd show you the full old-name → new-name mapping before touching anything, so you can sanity-check it, and I'd rename via a safe two-phase approach (temp names first, then final names) to avoid any collision if two screenshots happen to land on the same rendered name.

Just say the word and I'll go ahead — no spec needed for this one.

*(End of simulated conversation for this test — the actual rename was not performed, since this transcript exists to test the skill's Step 0 branch, not to execute the underlying file task.)*
