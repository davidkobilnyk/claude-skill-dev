# Spec: Meeting Notes → Action Items

## Purpose

Turn a person's raw, messy meeting notes into a clean, consistently formatted list of action items they can immediately copy and send to their team — without them having to manually reread, sort, and reformat the notes every time a meeting ends. The underlying need: the person currently spends 20–30 minutes per meeting doing this by hand, formatting is inconsistent week to week, and items buried in tangents or side conversation sometimes get missed entirely.

## Trigger conditions

**Should fire when:**
- The person pastes in raw meeting notes (typed live during a meeting — bullets, run-on sentences, shorthand, initials, timestamps, pasted links, tangents) and asks something like: "turn these into action items," "clean these notes up," "make this into a list I can send the team," "pull the action items out of this," or similarly pastes notes with no explicit instruction but clear meeting-notes shape (attendee list, agenda-like structure, discussion fragments).
- The notes are from a real meeting the person attended or ran — planning meetings, team syncs, 1:1s that produced follow-ups, client calls — regardless of length (from a few lines to 1–2 pages).

**Should NOT fire on (near-misses):**
- A person asking to summarize an article, document, or transcript that is not a meeting (that's a general summarization request, not this).
- A person asking to draft a meeting *agenda* (before a meeting, not after) — this skill only works on notes from a meeting that already happened.
- A person pasting a to-do list they wrote themselves outside of a meeting context and asking for it to be organized — no meeting notes involved.
- A request to actually send, post, or email the output to Slack/a team/an inbox — this skill only produces the text; sending it is a separate, out-of-scope action (see Non-goals).

## Inputs

- **Format:** Plain text or Markdown, pasted directly into the conversation. Typically typed live in a Google Doc during the meeting and copy-pasted in afterward.
- **Structure:** Unstructured to loosely structured — a mix of bullet fragments, full sentences, occasional timestamps, initials or first names for who's speaking/who owns something, pasted links, and off-topic tangents (small talk, FYI-only updates, unrelated notes).
- **Length:** Typically 1–2 pages for a planning meeting; a few lines to half a page for a short sync.
- **Completeness varies:**
  - Owners are sometimes explicit ("Jamie will follow up with design"), sometimes implied only by who was speaking (and the notes don't always capture who was speaking), sometimes entirely absent ("someone should look into the vendor pricing").
  - Due dates are sometimes stated explicitly ("by Friday"), sometimes vague/relative ("before launch," "next week," "soon"), sometimes not mentioned at all even though the notes imply urgency.
  - Meetings may cover a single topic (a short sync) or multiple distinct topics/workstreams in one sitting (a planning meeting spanning several project threads).
- **Real example the spec is grounded in** (from the person's own description): live-typed Google Doc notes for a 7-person product team's planning meeting — mix of bullets and sentence fragments, initials for owners some of the time, decisions noted without follow-up actions attached, a couple of pasted Slack/doc links, and asides unrelated to any task.

## Outputs

A clean, consistently formatted **action-items-only** list, in Markdown, that the person copies and pastes into wherever they send it (Slack message, email, doc — the skill does not send anything itself, see Non-goals).

**Fixed structure, per item:**
```
- [ ] <Task, stated as a clear action> — Owner: <Name or "TBD – needs assignment"> — Due: <Date/timeframe as stated, or "No date set">
```

**Grouping rule (auto-detected, not asked each time):**
- If the notes clearly cover multiple distinct topics/workstreams, group the action items under a `## <Topic>` heading per topic, in the order those topics appeared in the notes.
- If the notes are effectively single-topic (a short sync, a 1:1), skip grouping and produce one flat list.

**Example — multi-topic:**
```markdown
## Action Items — [Meeting name/date if stated in notes]

## Onboarding revamp
- [ ] Draft revised onboarding flow — Owner: Jamie — Due: Friday
- [ ] Get pricing from vendor for SSO integration — Owner: TBD – needs assignment — Due: No date set

## Q3 roadmap
- [ ] Circulate updated roadmap doc — Owner: Priya — Due: next week
```

**Example — single-topic (flat):**
```markdown
## Action Items — [Meeting name/date if stated in notes]

- [ ] Send follow-up email to client re: contract terms — Owner: Alex — Due: by EOD Thursday
- [ ] Schedule design review — Owner: TBD – needs assignment — Due: No date set
```

**What counts as "done":** every genuine action item from the notes is captured exactly once, each with an owner (explicit name or the standard TBD phrasing) and a due date (as stated or the standard "No date set" phrasing), grouped correctly per the rule above, with no non-action content (FYI updates, pure decisions with no follow-up, tangents, small talk) included in the list.

## Scope & boundaries

**Handles:**
- Reading messy, real-world meeting notes and extracting genuine action items from them.
- Formatting those items consistently (owner, due date, grouping) per the rules above.
- Flagging missing owners or due dates using the standard placeholder phrasing rather than guessing.
- Producing output the person can copy into Slack, email, or a doc themselves.

**Stops / hands off (does not push forward on its own):**
- Does not send, post, or deliver the output anywhere (no Slack/email integration) — the person always does that step themselves.
- Does not guess an owner from context beyond an explicit, unambiguous statement in the notes (e.g., "I'll take that" only counts if the notes themselves attribute that line to a specific speaker). If the notes don't make it unambiguous, it uses the TBD placeholder rather than inferring.
- **Never infers an owner from first-person phrasing alone** ("I'll take that," "I can do it") when the notes don't state who was speaking — this is called out as its own rule, not just a case of the general "don't guess" bullet above, because it's the single wrong-guess most likely to erode trust in the output.
- Does not invent or estimate a due date when none is stated or clearly implied — it uses the "No date set" placeholder rather than picking a plausible-sounding date.
- When the notes are so sparse or ambiguous that it's genuinely unclear whether something is an action item at all, it includes the item with the TBD/No-date-set placeholders rather than silently dropping it — favoring "flag it for the person to double check" over guessing wrong or leaving something out.

## Non-goals

- **Not a meeting transcription or note-taking tool** — it works only on notes the person already has, not audio/video.
- **Not a task/project management integration** — it does not create tickets, calendar events, or reminders in any external tool.
- **Not a sender** — it never posts to Slack, sends email, or delivers the output anywhere on the person's behalf.
- **Not a cross-meeting tracker** — it does not remember or roll up action items across multiple meetings over time; each run is scoped to the notes pasted in that run.
- **Not a general meeting summarizer** — it deliberately does not produce a discussion summary, a list of decisions, or minutes; the output is action items only, per the person's explicit ask.

## Edge cases

- **No owner stated or inferable:** use `Owner: TBD – needs assignment` rather than guessing who it might be.
- **No due date stated or inferable:** use `Due: No date set` rather than inventing a plausible date.
- **Vague/relative due date given** ("before launch," "soon," "next week") **or an event-dependent date** ("after the conference," "once legal signs off," tied to something not yet scheduled itself): carry the phrase through as-stated rather than converting it to a guessed calendar date, since the notes may not give enough to resolve it precisely — both relative-time and event-dependent phrasing are treated the same way.
- **Ambiguous ownership language** ("someone should look into X"): still capture it as an action item, with `Owner: TBD – needs assignment`.
- **Decisions with no follow-up action** ("we decided to go with option B"): excluded from the output entirely — it is action-items-only.
- **Decisions that do carry a follow-up** ("we decided to go with option B, so Jamie needs to update the doc"): the resulting action is captured; the decision framing itself is not restated.
- **Non-action tangents, FYI-only updates, small talk, pasted links with no associated task:** excluded from the output.
- **Notes containing zero genuine action items** (e.g., a status-only sync with nothing assigned): the skill says so plainly rather than fabricating items to fill out a list, e.g. "No action items found in these notes."
- **Multiple distinct topics vs. a single topic:** handled by the auto-detected grouping rule under Outputs — not asked about per run.
- **Duplicate or near-duplicate items** (the same task mentioned twice in different words, e.g. once mid-discussion and once in a wrap-up): merged into a single list entry rather than listed twice.
- **Notes clearly not from a meeting** (e.g., a personal to-do list): falls outside Trigger conditions — the skill does not attempt to process it as meeting notes.

## Open assumptions

- The output format is fixed Markdown with a checkbox (`- [ ]`) per item; the person did not ask for a different checkbox style, table format, or plain-text (non-Markdown) formatting, so Markdown-with-checkboxes is assumed as the universal-enough default since they paste it into Slack, email, or a doc interchangeably.
- "Due" is carried through in whatever form the notes state it (a specific date, a relative phrase, or "No date set") rather than normalized to a single date format — assumed acceptable since the person did not ask for date normalization and normalizing a vague phrase like "before launch" would require guessing.
- A meeting/date heading line (`## Action Items — [Meeting name/date]`) is included when the notes state a meeting name or date, and omitted when they don't — assumed reasonable as a light, non-invented header rather than something the skill should prompt for separately each time.
- No language/localization requirements were discussed; assumed English-language notes and output only.
