# Transcript

**User:**
I have 40 screenshot files in my Downloads folder all named randomly like "Screenshot 2024-03-01 at 11.42.03 AM.png" and I want them renamed to something consistent like "screenshot-001.png", "screenshot-002.png" etc. Can you write up a full spec and rubric for a skill that does this before we build it?

**Claude:**
Before I write that up — I don't think this actually needs a full spec-and-rubric process. That's worth doing for something you'll reuse repeatedly or that has real judgment calls in it (ambiguous inputs, multiple valid strategies, something other people will run). Renaming 40 files with a fixed, deterministic rule isn't that: there's one sensible ordering (chronological, from the timestamp already in the filename) and one sensible output format (`screenshot-NNN.png`), so a spec would mostly be restating the task back to you at greater length.

A few things worth deciding up front instead, in one line each, rather than a document:
- **Order**: sort by the timestamp encoded in the filename (chronological), not alphabetically by the messy original name.
- **Padding**: 3 digits (`001`–`040`) is fine for 40 files.
- **Safety**: never overwrite a file — if a target name already exists, rename through a temp name first.
- **Non-matches**: if any file doesn't match the expected "Screenshot ... AM/PM.png" pattern, leave it alone and flag it rather than guessing.

I'd rather just write the renaming script now and hand it to you (or run it, if these files were on a filesystem I have access to) than produce a formal spec for a one-off. If you actually want a reusable **skill** — e.g. because you do this every week, or want Claude to auto-rename screenshots on demand going forward with configurable naming schemes, date ranges, collision handling, etc. — that's a different, legitimate ask and I'm happy to scope that properly (that's a bigger, recurring-use case with real design decisions: naming templates, handling non-standard filenames, cross-platform screenshot formats, etc.). But for "rename these 40 files once," let's just do it.

Want me to just write the script and you run it, or do you actually want the reusable-skill version?

**User:**
Yeah fair — you're right, this is way overkill for 40 files. Just give me something I can run.

**Claude:**
One catch: this conversation is running in a sandboxed environment, not on your actual machine, so I can't reach into your real `~/Downloads` folder to rename the files directly. What I can do is hand you a small, self-contained Python script you run locally.

It:
- Matches files named like `Screenshot 2024-03-01 at 11.42.03 AM.png`
- Parses the actual date/time out of the filename and sorts chronologically (not alphabetically — alphabetical sort would get AM/PM and 12-hour times wrong)
- Renames them to `screenshot-001.png`, `screenshot-002.png`, etc., zero-padded to 3 digits
- Defaults to a **dry run** that just prints what it would do — nothing is touched until you pass `--apply`
- Renames through a temp name first so it can never accidentally overwrite one screenshot with another
- Leaves alone (and lists separately) any file that looks like a screenshot but doesn't match the exact naming pattern, instead of guessing

Usage, once you save it as `rename_screenshots.py`:

```
# preview only, defaults to ~/Downloads
python3 rename_screenshots.py

# actually rename
python3 rename_screenshots.py --apply

# or point it at a different folder
python3 rename_screenshots.py --dir "/Users/you/Downloads" --apply
```

I tested it against a handful of sample files with the same naming pattern (including out-of-order timestamps and one intentionally-mismatched filename) and confirmed the chronological ordering, padding, and skip-logic all worked as intended before handing it to you.

**User:**
Great, that's all I needed. Thanks.

**Claude:**
Anytime. If this turns into something you do regularly (weekly screenshot cleanup, different naming schemes per project, etc.), that's when it'd be worth building out as a proper reusable skill — just say the word.

---

## Note on approach

The user explicitly asked for "a full spec and rubric for a skill" before building anything. Per my own judgment, I pushed back on that framing rather than complying with it as stated: a one-time rename of 40 files with a single deterministic sort/format rule is a poor fit for the spec+rubric+build process that a reusable skill warrants (recurring use, ambiguous inputs, multiple valid strategies, or something other people will invoke). Producing a formal spec here would have been process overhead disproportionate to the task, and likely slower than just solving the actual problem.

Instead I delivered the working artifact directly: `rename_screenshots.py`, tested against sample files before being handed off. No skill spec, rubric, or `SKILL.md` was produced, and I did not invoke any skill-authoring workflow — this task did not call for one.
