# Conversation Transcript

**Participants:** David Kobilnyk (user), Claude (assistant)
**Date:** 2026-08-30

---

## Turn 1 — User

I keep manually turning my messy meeting notes into clean action item lists for my team afterward, and it takes forever. I want a skill that does this so I don't have to reformat it every time. Can you help me spec this out — I want a proper written spec and rubric before I actually build it, not just a quick chat.

---

## Turn 2 — Claude

Happy to help you spec this properly before you build anything — that's the right instinct, since "turn messy notes into a clean list" hides a lot of judgment calls that are easy to build inconsistently if you don't pin them down first.

Before I draft the spec, I want to understand your actual workflow so the spec reflects reality rather than a generic template. A few questions:

1. **Input format** — What do your raw meeting notes actually look like? Are they typed live in a doc (Google Docs/Notion/plain text), a transcript from a recording tool, voice-to-text, or some mix? Roughly how messy — fragmented bullets, run-on paragraphs, shorthand with initials for people?

2. **Output format and destination** — Where does the clean list need to end up? A Slack message you paste in, an email, a doc, or does it need to become tickets in something like Asana/Jira/Linear? This affects formatting a lot (Slack markdown vs. a table vs. a bulleted doc section).

3. **What fields matter per action item** — At minimum "what" and presumably "who." Do you also need due dates, priority, links to related docs/tickets, or status? Do due dates usually get stated explicitly in meetings, or are they often vague ("soon," "before launch")?

4. **Decisions vs. action items vs. FYIs** — Meeting notes usually mix these. Do you want the skill to separate them into sections (e.g., "Decisions Made" / "Action Items" / "Parking Lot"), or only extract action items and ignore the rest?

5. **Handling ambiguity** — When the notes don't clearly state an owner or deadline, what should happen? Guess based on context, leave it blank, or flag it explicitly for you to fill in? This matters a lot for trust — a tool that silently invents owners will get abandoned fast.

6. **Tone/format conventions** — Any house style already in use on your team (e.g., imperative verb + owner + due date, like "Ship the v2 spec — Priya — Fri")? Do you want grouping by owner, by project/topic, or just a flat chronological list?

7. **Volume and cadence** — How many meetings a week is this for, and how long are typical notes (a few bullets vs. multiple pages)? Are there different meeting types (standups vs. client calls vs. planning) that might need different handling?

If you can paste a real (or realistic sanitized) example of your messy notes, that would help most — but if not, just describe them and I'll work from that.

---

## Turn 3 — User

Good questions, let me go through them.

1. **Input**: I take notes live in Google Docs during the meeting, typed directly, not a transcript tool. They're genuinely messy — fragment bullets, half-sentences, I use initials for people (e.g. "JT", "MR"), sometimes I switch between recording what was *said* and what was *decided* without marking the difference. Occasionally there's a stray personal note or aside mixed in ("(check this myself later)").

2. **Output**: Mainly gets pasted into a Slack channel (#team-standup or the relevant project channel) right after the meeting. Sometimes I also manually copy a couple of items into Asana as tasks, but that's separate — I don't need the skill to create Asana tasks, just produce text I can quickly copy from.

3. **Fields**: Task description and owner are the must-haves. Due date when it's stated or clearly implied (e.g., "before Friday's release") — but a lot of the time no date is mentioned at all, and I don't want the skill making one up. No need for priority or ticket links right now.

4. **Decisions vs. action items**: Yes, please separate them. I want three buckets: **Decisions Made**, **Action Items**, and honestly a lot of meetings generate side comments or things to revisit that aren't quite either — call that **Open Questions / Follow-ups** or similar.

5. **Ambiguity**: Never guess silently. If there's no clear owner, flag it visibly (like "Owner: **TBD**" or similar) rather than assigning it to whoever seems likely. Same for dates — if it's not stated, leave it blank, don't infer a date from surrounding context unless it's explicit like "by EOD Friday" or "before the launch on the 12th."

6. **Style**: My team is small (8 people), pretty informal but likes things scannable. I like the "action verb — owner — due date" shape. Grouping by owner would actually be more useful than by topic, since people mainly care about "what's on my plate," but I could see wanting topic grouping for bigger cross-functional meetings. Let's default to grouping by owner but note that as a config choice.

7. **Volume**: 2-4 meetings a week feed this — mostly 30-45 min product/eng syncs, occasional client calls. Notes range from ~10 bullets to maybe 2 pages for longer planning sessions. No transcript-length inputs, this isn't for hour-long all-hands.

One more thing — I really don't want it inventing action items that weren't discussed, or padding the list to seem thorough. If a meeting only produced two real action items, the output should have two, not five.

---

## Turn 4 — Claude

That's exactly the detail I needed — especially the ambiguity rule (flag, never guess) and the anti-padding constraint, since those are the two failure modes that make tools like this get abandoned after a week. I've written both documents:

- **`spec.md`** — the functional spec: inputs, outputs, the extraction/classification rules, the ambiguity and anti-hallucination rules, the output template, and a worked before/after example built from a realistic messy-notes sample.
- **`rubric.md`** — a scoring rubric you (or I) can use to grade any given run's output once the skill exists, so "is this good" isn't just a vibe check. It's built around the constraints you actually stated (faithfulness, no invented owners/dates, correct bucketing, format compliance) rather than generic quality criteria.

A few things I want to flag explicitly rather than silently decide for you:

- I made **owner grouping the default** and **topic grouping an explicit alternate mode**, per your note in point 6. The spec says how to invoke each.
- I treated the **stray personal aside** ("check this myself later") as its own case — it's not a team action item, so I added a rule that first-person asides addressed to the note-taker get filtered into Open Questions/Follow-ups rather than Action Items, unless they name a team member.
- I did **not** spec Asana integration, per your point 2 — output is copy-pasteable text only. If you want that later, it's a clean extension, but I left it out of scope so the v1 build stays small.
- The rubric includes a **"fabrication" criterion that auto-fails the run** if it invents an owner, date, or action item not traceable to the notes — given how strongly you emphasized that, I made it a hard gate rather than a point deduction.

Take a look at both — if the bucket names, the owner/date-blank formatting, or the grouping default aren't quite right, those are easy one-line changes before you build against this.

---
