# Skill Spec: Meeting Notes → Action Item List

**Owner:** David Kobilnyk
**Status:** Draft v1, ready for build
**Last updated:** 2026-08-30

---

## 1. Problem Statement

David takes messy, live-typed notes in Google Docs during product/eng meetings and client calls. After each meeting he manually rewrites those notes into a clean list to post in Slack (and occasionally re-copies a couple of items into Asana by hand). This reformatting is repetitive and takes real time after every meeting. The skill should take the raw notes as input and produce a clean, ready-to-paste output in the team's expected format, without inventing content that wasn't actually in the notes.

## 2. Goals

- Turn raw, messy meeting notes into a clean, Slack-ready list in one pass.
- Correctly separate three kinds of content: decisions, action items, and open questions/follow-ups.
- Attach owner and (when explicitly stated) due date to each action item, using team-member initials as given.
- Flag missing owner/date visibly rather than guessing.
- Never add action items, owners, or dates that aren't traceable to the source notes.
- Support two grouping modes for the Action Items section: by owner (default) and by topic (alternate).

## 3. Non-Goals (v1)

- No integration with Asana, Jira, Linear, or any ticketing system — output is plain copy-pasteable text/markdown only.
- No audio/video transcription — input is always David's own typed notes, not a raw meeting transcript.
- No calendar or meeting-metadata lookup (attendee lists, meeting title/date are taken from what's in the notes, if present, not fetched externally).
- No cross-meeting memory/tracking of whether previous action items were completed (that's a possible v2).

## 4. Inputs

- **Format:** Plain text or Google Docs export (paste), typed live during the meeting.
- **Characteristics to expect:**
  - Fragmented bullets, half-sentences, inconsistent punctuation.
  - People referred to by initials (e.g., "JT", "MR") rather than full names — the skill does not need to resolve these to full names, just preserve them consistently.
  - No consistent marker distinguishing "what was said" from "what was decided" — this must be inferred from phrasing (see §6.2).
  - Occasional first-person asides from David to himself (e.g., "(check this myself later)") mixed into the bullets.
  - Length: roughly 10 bullets (short sync) up to ~2 pages (longer planning session). Not designed for hour-long verbatim transcripts.
- **Meeting types covered:** internal product/eng syncs (30–45 min) and client calls. Not designed for large all-hands.

## 5. Output

### 5.1 Destination and format
Plain markdown text, formatted to paste directly into Slack. No file generation, no ticket creation.

### 5.2 Structure
Three sections, in this order, using these exact headers unless the input has no content for a section (in which case omit that section entirely rather than showing it empty):

```
**Decisions Made**
- <decision, stated plainly, no owner/date needed>

**Action Items**
- <action verb phrase> — Owner: <initials or "TBD"> — Due: <date or omit if not stated>

**Open Questions / Follow-ups**
- <question or unresolved item>
```

### 5.3 Grouping modes for Action Items
- **Default — By Owner:** group action items under a bolded owner sub-heading (e.g., `**JT**`), in the order owners first appear in the notes. Items with no identifiable owner go under a final `**TBD**` group.
- **Alternate — By Topic:** group under bolded topic/project sub-headings inferred from the notes' own structure (e.g., existing headers, or repeated project names). Use this mode only when explicitly requested (e.g., "group by topic" or for larger cross-functional meetings); default is by-owner.

### 5.4 Formatting conventions
- Action items use the shape: **imperative verb phrase — Owner: X — Due: Y** (omit `— Due: Y` entirely if no date was stated; do not write "Due: TBD").
- Owner is always shown, using `TBD` (bolded) when no owner is identifiable from the notes.
- Keep each line under ~20 words; rewrite fragments into a clear imperative phrase without changing their meaning.
- Preserve initials exactly as used in the notes; do not expand or guess full names.

## 6. Processing Rules

### 6.1 Segmentation
Read through the notes bullet by bullet (or paragraph by paragraph for prose-style notes) and classify each into one of four buckets: Decision, Action Item, Open Question/Follow-up, or Discard (irrelevant noise, e.g., "ok let's start").

### 6.2 Classification heuristics
- **Decision:** phrasing indicates something was settled/agreed ("we decided," "agreed to," "going with," "final call:"), stated as fact rather than a task. No owner or date attached.
- **Action Item:** phrasing indicates a task assigned to someone, explicit or clearly implied by context ("JT will...", "need to send...", "follow up with client on..."). Must have an identifiable action, even if owner is unclear.
- **Open Question/Follow-up:** phrasing indicates something unresolved, a question raised, or a first-person aside from the note-taker to himself that doesn't name another team member as owner (e.g., "(check this myself later)" → Open Question/Follow-up, not an Action Item, unless David is later explicitly named as the owner elsewhere in the notes).
- **Discard:** meeting logistics, greetings, filler with no informational content.

### 6.3 Owner extraction
- Look for explicit names/initials adjacent to the task ("MR to send deck", "assigned to JT").
- If a task is stated in a way that clearly implies a single obvious actor from immediate context (e.g., a sub-bullet directly under a heading "JT updates" listing his own tasks), attribute to that person.
- If no owner can be determined with reasonable confidence, mark **Owner: TBD**. Do not guess based on role, seniority, or who talks about the topic most.

### 6.4 Due date extraction
- Only extract a due date if it is **explicitly stated** in connection with the task ("by Friday," "before the launch on the 12th," "EOD tomorrow").
- Do not infer a date from general meeting context, urgency language ("ASAP," "soon"), or unrelated dates mentioned elsewhere in the notes.
- Normalize relative dates only when the meeting date is known from the notes (e.g., "Friday" → resolve to a calendar date if the notes state the meeting date; otherwise keep as stated, e.g., "Friday").
- If no date is stated, omit the `— Due:` portion entirely (do not write "Due: TBD").

### 6.5 Anti-hallucination rule (hard constraint)
Every decision, action item, and follow-up in the output must be traceable to specific content in the input notes. The skill must not:
- Invent action items to make the list look more complete.
- Assign an owner or date that wasn't stated or clearly implied.
- Merge two unrelated bullets into one fabricated combined task.
- Pad short meetings with extra items. A meeting with two real action items produces a two-item list.

### 6.6 Deduplication and merging
If the same action item is mentioned more than once in the notes (common when discussion revisits a topic), merge into a single line, keeping the most complete owner/date info found across mentions — do not duplicate the line.

## 7. Worked Example

### Input (raw notes, as typed live)
```
Product sync 8/28

- quick recap of last week
- JT: API rate limiting is done, deployed friday
- discussion on whether to ship v2 onboarding this sprint or next
- decided: shipping v2 onboarding next sprint, not this one, too risky
- MR needs to update the pricing page copy before the launch on the 12th
- someone should look at the support ticket backlog, not sure who yet
- (check this myself later - re: the vendor contract renewal date)
- client call notes: client asked about SSO timeline, we said "later this year", need to follow up with actual date
- JT to send updated API docs to MR by EOD tomorrow
- ok that's it, thanks everyone
```

### Output
```
**Decisions Made**
- Ship v2 onboarding next sprint, not this sprint (deemed too risky to ship now).

**Action Items**

**JT**
- Send updated API docs to MR — Owner: JT — Due: EOD tomorrow

**MR**
- Update pricing page copy — Owner: MR — Due: before the 12th launch

**TBD**
- Review the support ticket backlog — Owner: TBD

**Open Questions / Follow-ups**
- Follow up with client on a concrete SSO timeline (currently only said "later this year").
- Check on the vendor contract renewal date (David, personal follow-up).
```

Note what did *not* make it into Action Items: "API rate limiting is done" is past-tense/status, not a forward task, so it's dropped as noise (or could optionally appear as a one-line status note if David wants that in a future version — flagged as an open question below).

## 8. Edge Cases

| Case | Handling |
|---|---|
| No action items in a short meeting | Output only the sections that have content; if truly nothing in a bucket, omit that section's header entirely. |
| Notes contain a full sentence that's ambiguous between decision and action item | Prefer Action Item if there's an implied next step/owner; prefer Decision if it's purely a settled fact with no task attached. |
| Same person referred to by two different initials/spellings (typo) | Best-effort treat as the same person if unambiguous from context; do not silently merge if genuinely ambiguous — keep separate and let David reconcile. |
| Notes include a heading structure (e.g., "Client Call," "Eng Sync") within one doc for multiple mini-meetings | Process as one input, but preserve topic grouping cues for use if By Topic mode is selected. |
| A bullet is entirely illegible/fragmentary with no recoverable meaning | Drop silently; do not guess at intent. |
| Notes exceed ~2 pages | Out of spec for v1 — flag to David that output may be less reliable beyond typical length rather than silently truncating. |

## 9. Open Questions for Future Versions (not in v1 scope)

- Should completed/status-only items (like "API rate limiting is done") get a lightweight "Status Updates" section instead of being dropped? (Currently dropped in v1.)
- Should the skill remember action items across meetings to flag ones that keep recurring unresolved?
- Should there be an Asana-task-formatted output mode as an optional secondary output block?

## 10. Success Criteria (summary)
See `rubric.md` for the full scoring rubric. At a high level, a successful run:
1. Contains zero fabricated owners, dates, decisions, or action items.
2. Correctly buckets nearly all items into Decisions / Action Items / Open Questions.
3. Matches the specified output format exactly (headers, grouping, line shape).
4. Is at least as fast to review/paste as David's current manual process — i.e., requires only light touch-up, not a rewrite.
