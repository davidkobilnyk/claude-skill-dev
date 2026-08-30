# Spec: Meeting Notes → Action Items

## Purpose

Turns raw, messy meeting notes into a clean, consistently formatted list of action items, ready to paste directly into a team channel. The underlying need: this kind of reformatting is typically done by hand right after a meeting ends — skimming a wall of real-time notes, picking out what was actually committed to versus what was just discussed, and retyping it into a presentable list. Done manually, this takes real time (on the order of 10–15 minutes per meeting) and the resulting format tends to drift from week to week depending on how rushed the person is, which makes the output harder for teammates to scan consistently. This skill exists to make that reformatting instant and consistent, without changing what actually gets decided in the meeting or who is responsible for what.

## Trigger conditions

**Should fire** when someone provides (typically by pasting) a set of meeting notes and asks for them to be turned into an action item list — for example:
- "Turn these notes into action items for the team"
- "Clean this up into a to-do list"
- "Can you pull the action items out of this and format them?"
- Pasting raw notes directly with a short instruction like "format this" or "make this a task list," where the notes are clearly meeting notes (bullet fragments, references to what people said or decided, timestamps/attendee cues, etc.)

**Should NOT fire** on requests that sound adjacent but want something different:
- "Summarize this meeting" or "what were the key decisions" — a request for a general summary of the discussion, not specifically an extraction of committed tasks. If a request mixes both ("give me a summary and the action items"), this skill's job is only the action-item portion — it should extract and format that part and say plainly that it is not producing the summary portion, rather than silently expanding scope to cover the whole request.
- A request to actually post, send, or file the output somewhere (e.g., "post this to Slack for me," "create Jira tickets for these") — that is out of scope; see Non-goals.
- Notes that are not from a meeting at all (e.g., a personal to-do list, a project brief) — this skill is specifically for post-meeting notes, not general task extraction from arbitrary text.

## Inputs

- **Source:** A block of meeting notes, typically pasted as plain text. Notes are typed live during the meeting (not a recording/transcript-tool dump, not handwriting-to-text), most often in a running document, and are always in English.
- **Authorship:** Notes may be typed entirely by the person requesting the reformat, or may include a block pasted in from a teammate who took notes for the same meeting; both are treated the same way — a single combined set of notes for one meeting (except the multi-meeting case below).
- **Structure:** Unstructured — a running stream of bullet fragments and half-sentences typed in real time, with no separation between decisions, FYIs, and action items, and no guaranteed labeling of who is speaking. Sentences are often incomplete and use informal shorthand.
- **Variation:** Meeting type varies (recurring internal team sync vs. client call), and client-call notes tend to be messier since the note-taker is also partially participating — but this is a difference of degree, not a different kind of input; the same extraction approach applies to both.
- **Completeness:** Ranges from clear ("Jake said he'd ping finance") to ambiguous or incomplete (a task mentioned with no stated owner, or an owner implied only by context — e.g. someone speaking in first person right before the task is mentioned).

## Outputs

A bulleted, Slack-markdown-formatted action item list, grouped by owner, structured as follows:
- One group per named owner (owner name in bold), each with their action item(s) as bullets underneath, including a due date on the bullet if one was stated or clearly implied in the notes.
- A final "Needs an owner" group at the bottom for any action item where no owner is stated or reasonably inferable from context — each item in this group is still listed, just without an assignee.
- No table, no headers/formatting beyond what renders cleanly in Slack (bold, bullets, plain text) — output should be paste-ready as-is.
- If the notes contain no genuine action items at all, the output is a plain, direct statement of that fact (e.g., "No action items in these notes — just discussion/decisions") rather than a forced or padded list.
- Owners and due dates are only ever included when actually present or clearly implied in the notes — never invented. When a detail is uncertain rather than simply absent, the output should say so rather than silently guessing (e.g., a tentative owner is marked as unconfirmed rather than stated as fact).

## Scope & boundaries

**Handles:**
- Reading a full set of raw meeting notes for one meeting (or, per the multi-meeting edge case below, several meetings pasted together) and extracting genuine action items from them.
- Formatting those items into the grouped, Slack-ready list described in Outputs.
- Flagging ambiguity (missing owner, missing date, notes too garbled to confidently extract from) rather than guessing.

**Stops / hands off when:**
- The request asks for the output to actually be delivered somewhere (posted, emailed, filed as a ticket) — the skill produces the text; the person pastes/sends it themselves.
- The notes are so unclear or fragmentary that no action items can be confidently identified — the skill says so plainly rather than fabricating structure to make the notes look processed.
- The request is, in substance, for a different kind of document (a full meeting summary, meeting minutes, a decision log) — the skill either declines or, for a mixed request, does only the action-item portion and names what it left out.

## Non-goals

- **Not** a meeting summarizer or minutes-generator — it does not attempt to capture decisions, discussion points, or general recap; only action items.
- **Not** an integration — it does not post to Slack, send email, create calendar events, or create tickets in a task tracker on the person's behalf. Output is text handed back to the person to use as they choose.
- **Not** a transcription tool — it does not process audio or video, and is not designed around raw transcript-tool output (e.g., an Otter/Fireflies-style verbatim transcript); its input is assumed to be notes a person already typed, not a verbatim recording.
- **Not** a project-management or tracking system — it does not remember action items across meetings, track completion status, or follow up on whether something got done. Each run is a one-time transformation of the notes handed to it.

## Edge cases

- **No action items present:** Notes are entirely discussion/decisions/status updates with nothing committed to by anyone. Output states this plainly instead of manufacturing an item out of a decision or FYI.
- **Missing owner:** An item is clearly a commitment but no owner is stated or reasonably inferable. Item goes in the "Needs an owner" group rather than being assigned a guessed name.
- **Missing due date:** An item has a clear owner but no date, stated or implied. Item is included under its owner without a date rather than a fabricated one.
- **Tabled or deferred items:** Something is raised and explicitly not resolved or decided against within the same notes (e.g., "should we move the launch date? tabled for now"). These are excluded from the action item list itself, but are optionally called out in a short separate note (e.g., "Raised but not resolved: launch date") so they aren't silently dropped from view. This callout is a nice-to-have, not a required part of every output — omitting it is acceptable if it would clutter a simple case.
- **Superseded / reassigned items:** The same task is mentioned more than once with conflicting details (e.g., assigned to one person early in the notes, reassigned to someone else later, or given two different-sounding deadlines at different points). The most recent statement in the notes wins; the item appears once, under the final owner/date, not duplicated or left showing the outdated version.
- **Notes too garbled to extract from confidently:** If the notes are so fragmentary or ambiguous that action items can't be identified with reasonable confidence, the skill says so directly rather than guessing at structure to produce a plausible-looking but unreliable list.
- **Multiple meetings pasted into one document:** The notes contain more than one meeting's worth of content pasted back to back (e.g., a weekly sync and a separate client call from later the same week, submitted together after falling behind). Output is split into separate action-item lists, one per meeting, using whatever markers exist in the notes (dates, meeting names, clear topic breaks) to determine where one meeting ends and the next begins — items from different meetings are never merged into a single combined list.

## Open assumptions

- When notes contain multiple meetings but provide no clear marker (date, heading, or obvious topic break) showing where one meeting ends and the next begins, the assumption is that the skill should ask which meeting a given stretch of notes belongs to, rather than guess at a split point — this has not been tested against a real ambiguous example and may need adjustment once one is seen.
- The "tabled/deferred items" callout (see Edge cases) is treated as optional polish rather than a required element of every output; if this turns out to matter more than expected in practice, it may need to be promoted to a required section instead.
- Notes are assumed to always be in English and always typed (never a transcript-tool dump or handwriting-to-text conversion) based on the current use case; behavior for non-English or transcript-style input is out of scope and untested.
