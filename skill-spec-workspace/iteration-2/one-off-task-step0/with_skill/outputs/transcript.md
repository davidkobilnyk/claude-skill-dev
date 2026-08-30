# Transcript — skill-spec, Step 0 pressure test ("one-off task dressed up as a skill request")

**Skill under test:** `skill-spec` (`/home/user/claude-skill-dev/skills/skill-spec/SKILL.md`)
**Scenario:** User explicitly asks for "a full spec and rubric" for a skill, but the described task is a one-time rename of 40 already-existing files — a classic Step 0 trap.
**Mode:** Autonomous eval. The "user" turns below after the opening message are simulated in-character, per the eval instructions, including a scripted concession that this really is a one-off.

---

## Turn 1 — User (opening message)

> I have 40 screenshot files in my Downloads folder all named randomly like 'Screenshot 2024-03-01 at 11.42.03 AM.png' and I want them renamed to something consistent like 'screenshot-001.png', 'screenshot-002.png' etc. Can you write up a full spec and rubric for a skill that does this before we build it?

---

## Turn 2 — Claude (skill-spec, Step 0)

Before I run the full spec-and-rubric process on this, I want to flag something, because I think it changes what you actually need here.

What you've described is: 40 *specific, already-existing* files, in *one* folder, renamed *once* into a sequential pattern. That's a one-off cleanup task — there's no real trigger moment ("whenever X happens, do this"), no variation across repeated future runs, no edge cases that would recur over time. It's just "sort these 40 files and rename them in order." A `SPECS.md` + `RUBRIC.md` pass is built for something that gets used repeatedly, where trigger conditions, recurring edge cases, and a reusable notion of "good output" actually matter — none of which really applies to renaming one static batch of files a single time.

So, two ways I could go:

1. **Just do the rename now** — I sort the 40 files (by the timestamp already in each filename, so the order is chronological) and rename them to `screenshot-001.png` through `screenshot-040.png`. Done in a couple minutes, no spec needed.
2. **Treat this as a real reusable skill** — if what you actually want is something you (or others) can invoke again later — e.g., "whenever I dump a batch of randomly-named screenshots somewhere, rename them consistently" as a repeatable capability — then the full spec/rubric process makes sense, and I'd go ahead with it.

Which of these is it — a one-time cleanup, or something you want as a standing, reusable skill?

---

## Turn 3 — User (simulated)

> Yeah, fair — I guess this really is just a one-time cleanup. I don't rename screenshots that often, I just had this one folder that got messy. Never mind the spec, don't need it.

---

## Turn 4 — Claude (skill-spec, wraps up)

Makes sense — I won't produce a `SPECS.md`/`RUBRIC.md` for this, since it's a one-off rather than something reusable.

If you'd like, I can just do the actual cleanup directly instead: read the timestamp embedded in each of the 40 filenames (e.g. `Screenshot 2024-03-01 at 11.42.03 AM.png`), sort them chronologically, and rename them in place to `screenshot-001.png` … `screenshot-040.png`. That's a quick, direct task — no spec/rubric workflow required. Just say the word (and confirm zero-padding to 3 digits and chronological order are what you want) and I'll go ahead.

---

## End of run

No `SPECS.md` or `RUBRIC.md` was produced. The skill's Step 0 check fired on the very first message, correctly identified the one-off/no-reusable-signal pattern despite the user's explicit request for "a full spec and rubric," surfaced the concern plainly, and offered a choice rather than silently complying or silently refusing. When the simulated user confirmed it was in fact a one-off, the skill stood down from the spec/rubric workflow and (as ordinary Claude behavior, not part of skill-spec's job) offered to just do the underlying task directly.
