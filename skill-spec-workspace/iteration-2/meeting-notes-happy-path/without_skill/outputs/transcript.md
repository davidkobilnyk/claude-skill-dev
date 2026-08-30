# Transcript — Meeting Notes → Action Items Skill Spec

**Date:** 2026-08-30

---

## User

I keep manually turning my messy meeting notes into clean action item lists for my team afterward, and it takes forever. I want a skill that does this so I don't have to reformat it every time. Can you help me spec this out — I want a proper written spec and rubric before I actually build it, not just a quick chat.

## Assistant

Happy to help spec this properly. Before I draft anything, I want to nail down the specifics — a spec that's vague about inputs/outputs will just cause rework later. A few questions:

1. **What do your raw meeting notes actually look like?** Plain text you type live during the meeting? A transcript from a recording tool (Zoom/Otter/Fireflies)? Bullet points, stream-of-consciousness, shorthand? Can you paste a real (sanitized) example?

2. **Who's the audience for the cleaned-up list, and where does it end up?** Posted in Slack, emailed, pasted into Notion/Asana/Linear, or something else? Does the destination impose a format (e.g., Slack markdown vs. plain checkboxes)?

3. **What does a "clean action item" look like to you?** At minimum I'm guessing: task description, owner, due date if any. Anything else you track — priority, status, related project/ticket link?

4. **How do you currently figure out who owns what?** Are owners usually named explicitly in your notes ("Sarah to follow up with vendor"), or do you infer it from who was talking / context? What should happen when it's genuinely unclear who owns something?

5. **Volume and cadence** — roughly how long are your notes (a few bullets vs. multiple pages), and how often does this run (after every meeting? daily digest?)

6. **What should NOT happen?** E.g., should it ever invent an action item that wasn't really there, silently drop things it's unsure about, or merge similar-sounding items? Any past bad experience with a tool/AI doing this badly that you want to avoid repeating?

## User

Good questions, let me go through them.

1. My notes are typed live during the meeting, in a plain markdown file, pretty rough — half sentences, sometimes just a name and a fragment, discussion points mixed in with decisions and to-dos with no consistent structure. Example:

```
standup 8/28
- sarah: vendor contract still stuck w/ legal, following up today
- talked about q3 roadmap slip, need to decide by fri whether we cut the reporting feature
- mike found the bug in checkout flow, root cause is the webhook retry logic
- mike to fix by wed, will need code review from someone
- decided: moving daily standup to 9:30 starting next week
- alex raised concern about onboarding drop-off, wants data pulled before we discuss further - no owner yet
- reminder: renew the ssl cert (whose job is this? unclear)
- great, ship it - re: the pricing page copy, kate approved
```

2. It gets pasted into Slack, in our #team-actions channel, as a normal message (not a bot integration, I just copy-paste it in). So it needs to render cleanly as Slack markdown — bold, bullets, no headers with #, since Slack doesn't support markdown headers.

3. Clean action item = task description (imperative, short), owner, due date if mentioned. No priority/status tracking needed right now, that's overkill for us. Nice to have: a checkbox so people can see it as a literal to-do.

4. Owners are usually named explicitly ("mike to fix by wed") but sometimes it's ambiguous or missing (the SSL cert example, the onboarding data pull). When unclear, I don't want the tool guessing — I want it flagged as "Owner: [unassigned]" or similar so someone has to claim it in the channel, rather than the tool silently picking the most-likely person.

5. Notes are usually 15-40 lines, meetings are 20-45 min standups/syncs. This runs after basically every meeting, so multiple times a day some days.

6. Big one: don't invent action items that aren't there — I've had ChatGPT do this before, where a discussion point ("we talked about the roadmap slip") got turned into a fake action item like "Team to finalize roadmap decision" when nobody actually committed to that as a next step. Also don't silently drop the ambiguous ones (the SSL cert line) — those are exactly the ones that fall through the cracks in real life, which is the whole reason I want this tool. And don't merge two separate to-dos into one just because they're related (e.g. the bug root cause note and "mike to fix by wed" are two different things — one's context, one's the actual action item).

## Assistant

This is very clear — thank you. That last point about not fabricating action items from discussion, and not silently dropping ambiguous ownership, is really the crux of what makes this hard (and what makes a generic "summarize this" prompt fail). I'll build the spec and rubric around those as first-class requirements, not afterthoughts.

I'm going to write two documents:

- **`spec.md`** — defines scope, input assumptions, the exact output format (with your Slack-safe formatting), the processing rules (in particular: how to classify a line as action-item vs. context/decision, how to extract owner/due date, and the explicit "flag, don't guess, don't drop" policy for ambiguous cases), edge cases, and a worked example using your standup notes above.
- **`rubric.md`** — a scoring rubric you (or I) can use to grade any candidate output against real notes, with the fabrication and dropped-item failure modes weighted as hard fails rather than just point deductions, since those are the ones you specifically called out as unacceptable.

Drafting both now.

*(assistant writes `spec.md` and `rubric.md`, described below)*

## Assistant

Both documents are done:

- `spec.md` — full functional spec: purpose/scope, input assumptions, classification rules for action item vs. context vs. decision, owner/due-date extraction rules, the output template (Slack-safe), an edge case table, and a fully worked example using your actual standup notes so you can see exactly what the output should look like.
- `rubric.md` — scoring rubric with 8 criteria (weighted), two of which — **no fabricated action items** and **no silently dropped ambiguous items** — are marked as automatic hard-fail conditions rather than partial-credit criteria, per what you told me. Includes a 1-5 scale per criterion, a worked scoring example against the sample output, and a pass/fail threshold (any hard-fail = fail regardless of total score; otherwise pass at ≥32/40 with no criterion below 3).

Take a look at both — once you're happy with them, the natural next step is to actually build the skill (e.g. as a Claude Code skill / SKILL.md, or a saved prompt template, depending on how you want to invoke it) and I'd test it against a handful of your real past notes, scoring the output with this rubric before you trust it on live meetings.

## User

This looks solid, thanks. Let's go with these — I'll review them and come back when I'm ready to build it out.

## Assistant

Sounds good. Both files are saved:

- `spec.md`
- `rubric.md`

When you're ready to build, I'd suggest a quick pass first: run 3-5 of your real recent meeting notes through a draft prompt/skill, score each output against `rubric.md`, and specifically stress-test the two hard-fail cases (a line that's discussion-only but could be mistaken for an action item, and a line with a genuinely ambiguous or missing owner) before rolling it out to daily use. Happy to help with that testing pass whenever you're ready.
