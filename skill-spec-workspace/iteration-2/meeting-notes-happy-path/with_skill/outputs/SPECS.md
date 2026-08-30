# Spec: Meeting Notes → Action Items

## Purpose

This skill turns a person's raw, messy meeting notes into a clean, consistent action item list they can hand straight to their team — without the person having to manually sort, reformat, and double-check it every time a meeting ends.

The underlying need: David currently does this by hand after most meetings, it takes real time, and doing it by hand under time pressure has caused two recurring problems — items buried in long notes get missed, and the output format drifts week to week (sometimes due dates are included, sometimes forgotten), which has made the team stop trusting that the recap is complete or reliable.

## Trigger conditions

**Should fire when:**
- The person pastes raw meeting notes (of the messy, semi-structured kind described under Inputs) and asks for them to be turned into an action item list, cleaned up, formatted, or "made presentable for the team" — in their own words, not necessarily using the phrase "action items."
- Example phrasings: "turn these notes into action items," "clean this up for the team," "can you make this presentable," "here are my standup notes, sort this out," or simply pasting a block of raw notes with "format this."
- Fires per-paste — there's no standing/background trigger; the person brings notes each time they want a list produced.

**Should NOT fire on (near-misses):**
- A request for a **meeting summary or minutes** (a narrative recap of what was discussed) — this is a different deliverable than an action item list and is explicitly out of scope (see Non-goals). If a request is ambiguous between "summary" and "action items," ask which is wanted rather than guessing.
- A request to **draft an agenda** for an upcoming meeting — this skill only processes notes from a meeting that already happened.
- General note-taking help unrelated to producing an action list (e.g., "help me organize my notes by topic" with no mention of actions/follow-ups).
- Notes pasted with no request attached and no clear signal the person wants them turned into anything (e.g., someone pasting notes purely for reference/context in an unrelated conversation).

## Inputs

- **Format:** Freeform, unstructured or loosely-structured plain text — typically bullet lines, but not guaranteed. No fixed schema. Comes from Google Docs or a phone Notes app, then copy-pasted directly into the conversation. There is no direct connection to any note-taking tool (see Non-goals) — text is always pasted in by the person.
- **Typical messiness:** Half-sentences, inconsistent structure, action items mixed in the same list with decisions, reminders, and unrelated asides, casual/shorthand phrasing, people referred to inconsistently (first name, sometimes just initials, rarely full name).
- **Representative real example** (grounds the edge cases below):

  ```
  Standup notes 8/26
  - talked about the checkout redesign, sarah thinks we should push to next sprint
  - JK to update the API docs whenever he gets a chance
  - need someone to look into the stripe webhook failures asap, mike said he'd take a look
  - decided to go with option B for the pricing page
  - reminder: mike's on vacation next wed
  - follow up with legal about the ToS changes - due before launch on 9/15
  - what about the onboarding flow? nobody owns this yet, need to figure out
  - misc: office snacks order is late again lol
  ```

- **Scale:** Usually one meeting's worth of notes at a time. Occasionally two meetings get pasted together in one go (e.g., catching up after missing a day) — distinguishable when there are separate dated headers (like "Standup notes 8/26"); otherwise treated as a single undifferentiated block.
- **People referenced:** Small team, 7 people (first names Sarah, JK, Mike, Priya, Tom, Elena, plus David himself). Referred to inconsistently — first name most often, initials sometimes, full name rarely. No standing roster is provided by the person each time; names are inferred from the notes themselves.
- **Language/tone of source notes:** English, casual/internal shorthand — not a transcript, not formal writing.

## Outputs

A plain-text, hyphen-bullet action item list — no markdown tables (renders poorly in Slack) and no heavy formatting that would break when pasted into an email instead. The same output should work copy-pasted into either destination without rework.

**Structure:**

1. **Action items** (the primary, required section) — one bullet per item, in the form:
   `- [Owner]: <action>, due <date>` (due-date clause included only when a date was actually stated in the notes; omitted entirely otherwise, never fabricated).
   - Items with **no clear owner** are grouped separately under a **"Needs an owner"** sub-list rather than mixed into the main list or silently dropped, so they can't get missed.
   - Items that are too ambiguous to confidently phrase as a concrete action are still included, prefixed with `⚠️ unclear —` and a short note on what's unclear, rather than guessed at or dropped.
2. **Decisions** (optional section, included only when the notes actually contain decision statements) — a short bullet list of decisions made, for context, clearly separated from the action items so it's never confused with a to-do.
3. **FYI** (optional, small) — for personal/logistical notes that aren't team action items but might be worth keeping visible (e.g., someone's out next week) — kept brief, never treated as an action item.

**Tone:** Plain and direct, matching a casual startup team's voice — not corporate or stiffly formal. Short, natural phrasing (e.g., "update the API docs" not "Please proceed to update the relevant API documentation at your earliest convenience").

**Ordering/grouping:** If the pasted notes clearly contain two distinct dated meetings, keep the two action item lists separate under their own headers; otherwise produce one combined list.

## Scope & boundaries

**Handles:**
- Converting one pasted block of raw notes (one meeting, or two clearly separated meetings) into the action item list format above.
- Inferring owner and due date only when actually stated or clearly implied in the text (e.g., "mike said he'd take a look" implies Mike as owner).
- Merging genuinely duplicate/near-duplicate mentions of the same action item into a single bullet.
- Filtering out pure noise (asides with no work relevance) and personal-only items (routed to the small FYI section or dropped, never listed as team action items).
- Flagging (not silently resolving) contradictory information — e.g., if the same item is given two different due dates in the same notes, flag the conflict inline rather than picking one.

**Stops / hands off rather than pushing forward when:**
- A chunk of notes is too garbled to confidently produce even an unclear-item placeholder for — flagged inline for the person to fix by hand, not blocked on or guessed at broadly.
- The person's request is ambiguous between an action list and a full meeting summary — asks which, rather than assuming.
- Notes arrive in a form this skill doesn't handle at all (see Non-goals) — audio, images/photos of a whiteboard, a link to a doc rather than pasted text — the skill says plainly it can't process the input in that form and asks for it as pasted text instead.

## Non-goals

- **Not a meeting summary/minutes generator.** It does not narrate what was discussed; it extracts actionable items (plus optional short Decisions/FYI context), nothing more.
- **Not a connector to any notes tool.** It never reads directly from Google Docs, Notion, or any other source — input is always text pasted directly into the conversation. (Raised explicitly during spec discussion and ruled out — noted here so it isn't quietly assumed later.)
- **Not an auto-poster.** It produces text for the person to paste themselves into Slack/email; it never sends, posts, or delivers the output anywhere on its own.
- **Not a task-tracker integration.** It does not create Jira tickets, calendar entries, or reminders — output is a text list only.
- **Not an audio/image processor.** It does not transcribe recordings or read photos of whiteboards/handwritten notes — input must already be text.
- **Not a translator.** Notes are assumed to already be in English; non-English input handling is out of scope for this version.

## Edge cases

| Situation | What should happen |
|---|---|
| Action item has no stated owner (e.g., "onboarding flow — nobody owns this yet") | Group under a separate "Needs an owner" sub-list. Never guess an owner. |
| Action item has no stated due date | Omit the due-date clause entirely. Never fabricate a date. |
| Vague action ("look into X") with no more specific detail given | Keep the phrasing as stated — don't invent detail or specificity the notes didn't provide. |
| Decision statement mixed into the notes ("decided to go with option B") | Route to the separate Decisions section; never list as an action item. |
| Personal/logistical note with no team action ("Mike's on vacation next Wed") | Route to the small FYI section, or drop if not clearly worth keeping — never treat as a team action item. |
| Pure noise / unrelated aside ("snacks order is late") | Drop silently. |
| Same action item mentioned twice in different words (e.g., "look into stripe" and later "mike's looking into the webhook thing") | Merge into one bullet under the resolved owner; don't list twice. |
| Two meetings pasted together with separate dated headers | Keep as two separate lists, each under its own header. |
| One undifferentiated blob covering possibly more than one topic | Treat as a single combined list — don't guess at meeting boundaries that aren't marked. |
| Contradictory info for the same item (two different due dates given) | Flag the conflict inline rather than silently picking one. |
| A line too garbled/unclear to confidently phrase as an action | Include it prefixed with `⚠️ unclear —` plus a short note on what's ambiguous, rather than dropping it or guessing. Do not block the rest of the output on it. |
| Request is ambiguous between "action items" and "meeting summary" | Ask which is wanted rather than assuming. |
| Input isn't pasted text (audio, image, doc link) | State plainly this skill needs pasted text and ask for it in that form; don't attempt to process the other format. |

## Open assumptions

- Team size and roster (7 named people) are illustrative of David's actual team, not a hard limit — the skill should work generically for however many names actually appear in a given note, not assume exactly 7.
- No standing name-to-role roster is maintained between sessions; owner names are always inferred fresh from each pasted note's own content.
- "Due before launch on 9/15" and similar are treated as explicit dates when a real date is stated; purely relative phrases with no anchor ("whenever he gets a chance") are treated as *no due date* rather than something to resolve into a concrete date.
- Output destination (Slack vs. email) does not change the output format — one plain, table-free bullet format is assumed to work for both, per David's explicit confirmation.
- This version assumes English-language, text-based input only, consistent with David's actual usage; broader input types were explicitly scoped out rather than silently omitted.
