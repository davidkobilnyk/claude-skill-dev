# Spec: Meeting Notes → Action Items

**Owner:** David Kobilnyk
**Status:** Draft v1
**Last updated:** 2026-08-30

## 1. Purpose

Turn rough, live-typed meeting notes into a clean, Slack-ready list of action items, grouped by owner, so David doesn't have to manually reformat notes after every meeting before posting them to `#team-actions`.

## 2. Scope

**In scope:**
- Parsing informal, unstructured markdown-style notes (bullets, fragments, mixed content).
- Distinguishing genuine action items from discussion points, decisions, and pure context.
- Extracting owner and due date when present in the text.
- Flagging action items with unclear or missing ownership — never guessing.
- Producing Slack-safe markdown output (bold/bullets/checkboxes; no `#` headers).

**Out of scope (v1):**
- Priority levels or status tracking.
- Direct posting to Slack (output is copy-pasted by David; no bot/API integration).
- Integration with task trackers (Asana/Linear/Notion) — plain text output only.
- Processing audio/video directly — input is always David's typed text notes.
- Multi-meeting rollups or historical tracking across sessions.

## 3. Input Assumptions

- Input is a single meeting's notes, plain text/markdown, typed live during the meeting.
- Length: typically 15–40 lines, occasionally longer.
- Style: informal, inconsistent structure — bullets mixing decisions, discussion points, action items, and asides. Fragments and shorthand are common (e.g., "mike to fix by wed").
- No guaranteed structure or delimiters separating "types" of line — classification must be inferred from content.
- Names in notes refer to real team members; the skill does not need a roster (any name mentioned is trusted as a valid owner candidate) but must not invent names that never appear in the notes.

## 4. Line Classification

Every line/bullet in the input must be classified into exactly one of:

| Type | Definition | Example from sample notes |
|---|---|---|
| **Action item** | A concrete next step with a clear commitment to do something, even if owner/date is missing | "mike to fix by wed", "alex ... wants data pulled ... no owner yet", "reminder: renew the ssl cert" |
| **Decision** | A choice or resolution that was made, with no further action implied | "decided: moving daily standup to 9:30 starting next week" |
| **Context/discussion** | Background, a topic that was discussed, a finding, or an open question with no committed next step | "talked about q3 roadmap slip, need to decide by fri", "mike found the bug in checkout flow, root cause is the webhook retry logic" |

**Classification rule of thumb:** a line becomes an action item only if the text implies someone (named or not) is going to *do* something as a result — not merely that something was *discussed*, *found*, or *decided as a state of affairs*. A decision to change a process ("moving standup to 9:30") is a decision, not an action item, unless it also names a follow-up task.

Discussion points that contain a deadline for a future decision (e.g., "need to decide by fri whether we cut the reporting feature") are context, not an action item — nobody has committed to doing the deciding as a task; if David wants this treated as an action item in a future version, see Open Questions (§8).

## 5. Extraction Rules

For each line classified as an **action item**, extract:

- **Task** — rewritten as a short imperative phrase (e.g., "Fix checkout webhook retry bug" not "mike found the bug... root cause is..."). Strip filler and restate concisely, but do not add detail that wasn't stated.
- **Owner** — the person's name if stated or clearly implied by direct address ("mike to fix..."). If no name is present or the note explicitly says ownership is unresolved (e.g., "no owner yet", "whose job is this? unclear"), set owner to `[unassigned]`. Never infer an owner from context, role, or who raised the topic.
- **Due date** — only if explicitly stated ("by wed"). Normalize relative dates against the meeting date if given (e.g., "wed" → the coming Wednesday's date), otherwise keep the relative phrase as written (e.g., "by Wed") rather than guessing a calendar date with no anchor. If no due date is mentioned, omit the field entirely — do not write "TBD" or invent urgency.

**Hard rule — no fabrication:** An action item must trace back to specific text in the notes. Never synthesize a new action item to "resolve" an open discussion point, even if it seems like an obvious next step. If the notes only say a topic was discussed, the output must not imply anyone committed to act on it.

**Hard rule — no silent drops:** Every line that is ambiguous — a clear intent to act but missing/unclear owner, unclear scope, or an unresolved question about responsibility — must still appear in the output, flagged, rather than being omitted for lack of confidence.

**Hard rule — no merging:** Two distinct action items are never combined into one line, even when they're topically related (e.g., a bug's root cause description and a separate "fix by Wed" commitment stay as one action item, informed by — but not merged with — the context line).

## 6. Output Format

Plain text, Slack-markdown-safe (bold via `*text*`, bullets via `-`, checkboxes via `- [ ]`, no `#` headers, no tables).

Grouped by owner; unassigned items in their own trailing section so they're visually distinct and prompt someone to claim them.

```
*Action Items — [meeting name/date if given]*

*Mike*
- [ ] Fix checkout webhook retry bug (Due: Wed)

*Unassigned*
- [ ] Pull onboarding drop-off data (before further discussion)
- [ ] Renew SSL cert — owner unclear, needs to be claimed
```

Notes:
- Owner name formatting matches how it appeared in source notes (don't invent last names/capitalization not present).
- If literally zero action items are found, output a single line: `*Action Items — none identified this meeting.*` — never fabricate one to avoid an empty list.
- Decisions and context are **not** included in the output in v1 (see §8 for whether a future version should add an optional "Decisions" section) — this skill's job is action items only, to keep the Slack post short and scannable.

## 7. Worked Example

**Input** (David's standup notes, 8/28):
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

**Line-by-line classification:**
| Line | Type | Notes |
|---|---|---|
| sarah: vendor contract... following up today | Action item | Sarah has a clear next step (follow up) |
| talked about q3 roadmap slip... | Context | Discussion + future deadline for a *decision*, not a task |
| mike found the bug... root cause... | Context | Describes a finding, not a commitment |
| mike to fix by wed... | Action item | Clear owner + due date; code review need is a separate, currently-unassigned follow-on |
| decided: moving daily standup... | Decision | No further action implied |
| alex raised concern... no owner yet | Action item, unassigned | Explicit intent to act ("wants data pulled"), no owner |
| reminder: renew the ssl cert... unclear | Action item, unassigned | Explicit task, ownership explicitly unresolved |
| great, ship it - kate approved | Decision | Approval given, no outstanding task |

**Output:**
```
*Action Items — Standup 8/28*

*Sarah*
- [ ] Follow up with legal on vendor contract (Due: today)

*Mike*
- [ ] Fix checkout webhook retry bug (Due: Wed)

*Unassigned*
- [ ] Pull onboarding drop-off data before further discussion (raised by Alex)
- [ ] Find code reviewer for checkout fix
- [ ] Renew SSL cert — owner unclear, needs to be claimed
```

Note: "will need code review from someone" is correctly split out as its own unassigned action item rather than folded into Mike's line, per the no-merging rule — it's a distinct piece of work with a distinct (currently absent) owner.

## 8. Edge Cases

| Case | Expected behavior |
|---|---|
| Line implies action but has zero identifiable task content (e.g., just a name and trailing thought) | Skip only if there is genuinely no actionable content; if in doubt, include as unassigned rather than drop |
| Same person appears under multiple casing/spelling ("mike" vs "Mike") | Normalize to one casing per output list; use the more complete form if both appear |
| Due date given as a weekday with no meeting date context | Keep as written ("by Wed") rather than guessing a calendar date |
| A line is sarcastic, a joke, or clearly not literal ("we'll get right on that lol") | Do not extract as an action item |
| Notes contain no action items at all | Output the explicit "none identified" line (§6), not a blank message |
| An action item is mentioned twice in slightly different words (restated later in the meeting) | Merge into a single line only if clearly the same task; keep the more complete/final phrasing |
| Notes reference a decision that also implies a task ("decided: moving standup to 9:30, someone needs to update the calendar invite") | Treat the invite-update as a separate action item; the schedule decision itself stays a decision, not listed |

## 9. Non-Goals / Explicit Anti-Patterns

Restating David's stated failure mode from a prior tool, as a permanent constraint on this skill:

- **Never** convert a discussion point into a fabricated action item just because it sounds like it should have one ("we talked about X" → "Team to finalize X" is explicitly forbidden).
- **Never** silently drop a line just because ownership or scope is unclear — flag it instead.
- **Never** merge two distinct pieces of work into a single action item because they're topically adjacent.

Any candidate output that violates one of these three is an automatic fail regardless of how clean the formatting is (see `rubric.md`).

## 10. Open Questions (for David, before build)

1. Should context/discussion lines with an explicit future deadline for a *decision* (not a task) eventually get a lightweight "Decisions Pending" section, separate from action items? Currently out of scope, but flagged since it's a near-miss case in the sample notes (the Q3 roadmap line).
2. Should the skill attempt any date normalization (e.g., "Wed" → "9/3") if it's given today's date, or should it always preserve relative phrasing as-is? Current spec defaults to preserving relative phrasing to avoid wrong-date errors.
3. Any interest in a lightweight "carried over from last time" concept for chronically-unassigned items (e.g., the SSL cert), or is that entirely out of scope for a single-meeting tool? Current spec treats every run as stateless/single-meeting.
