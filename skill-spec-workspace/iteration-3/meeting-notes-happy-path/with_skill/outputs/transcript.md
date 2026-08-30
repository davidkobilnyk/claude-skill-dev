# Transcript — skill-spec run: "meeting notes → action items"

(Simulated eval run. The human side of this conversation is self-generated in-character, per test instructions, since no live user is available. The persona is referred to here only as "the requester" — any name used below is for narration flavor only and is never written into SPECS.md or RUBRIC.md.)

---

## Turn 1 — Requester (opening message)

> I keep manually turning my messy meeting notes into clean action item lists for my team afterward, and it takes forever. I want a skill that does this so I don't have to reformat it every time. Can you help me spec this out — I want a proper written spec and rubric before I actually build it, not just a quick chat.

## Turn 2 — Claude (skill-spec engaged)

**Step 0 check (internal):** This is clearly a request for a reusable skill, not a one-off task — "I want a skill that does this," "before I actually build it," explicit request for a written spec + rubric. No need to ask whether a skill is warranted; proceeding straight to Step 1/2.

**Claude's reply:**

Got it — let's build this out properly before you write a line of it. This is going to take a few rounds of questions since the goal is a spec someone could build from without needing to come back and ask "wait, what about X." I'll go in a few batches rather than firing everything at once.

First batch — the shape of the input and the trigger moment:

1. Where do your meeting notes actually live? Are you typing them live in a specific tool (Google Docs, Notion, a plain notes app), or do they start elsewhere (handwritten, a transcription tool like Otter/Fireflies) before you reformat them?
2. What do "messy" notes actually look like for you — stream-of-consciousness bullet dumps, half-sentences, notes that mix decisions/FYIs/action items together with no separation, missing attribution for who said what? A rough real example (even paraphrased) would help a lot.
3. What kind of meetings is this for — a recurring team sync, ad hoc meetings, client calls, all of the above? Does the format of the notes vary a lot between meeting types?
4. What triggers you to reach for this — is it always "I have a full set of notes from a meeting that just ended," or are there other moments (e.g., mid-meeting, partial notes)?

## Turn 3 — Requester (self-generated answer, round 1)

> Good questions.
> 1. Mostly Google Docs — I keep a running doc I type into live during the meeting. Sometimes it's a mix of stuff I typed and stuff a teammate pasted in from Notion after the fact if they took notes instead of me.
> 2. Yeah, exactly that — it's a wall of bullets and half-sentences typed in real time, no clean separation between "we decided X," "FYI Y," and "so-and-so will do Z by Friday." Sometimes it's not even clear who said what unless I remember the meeting. Example-ish: "- talked about q3 budget, sarah thinks we're over on ads - need to pull the report before next week - jake said he'd ping finance - also should we move the launch date? tabled for now - reminder standup moved to 10am starting monday"
> 3. Mostly our weekly team sync (6 people, marketing team), but sometimes client calls too. The client call notes are usually messier because I'm also half-participating, not just scribing.
> 4. Always after the meeting ends, with the full notes doc in front of me. I've never wanted this mid-meeting.

## Turn 4 — Claude

Great, that's a solid picture of the input side. Second batch — output shape and what "action item" actually means to you:

5. When you say "action item," what qualifies? Just things someone explicitly committed to ("Jake said he'd ping finance") — or do you also want things you can infer are implied work even if nobody said "I'll do it"?
6. What does the finished list need to include per item — owner, due date, both if available? What happens when the notes don't give you one or both of those (e.g., "need to pull the report before next week" — no named owner)?
7. Where does the output go once it's built — pasted into Slack, emailed, added to a doc, something else? Does that destination expect a particular format (e.g., Slack markdown, a specific template)?
8. Do you want it grouped any particular way — by owner, by topic, just a flat list in the order things came up?

## Turn 5 — Requester (self-generated answer, round 2)

> 5. Explicit commitments, mainly — someone saying or clearly implying they'll do something. I don't want it guessing at work nobody actually claimed, that's led to arguments before ("why do I have an action item, I never said I'd do that").
> 6. Owner if it's stated or obviously implied by context (like "I'll handle it" said right after someone was talking), due date if mentioned. If either is missing, I'd rather it flag that clearly than make something up — I do NOT want it inventing a name or a date.
> 7. I paste the output straight into our team Slack channel after the meeting. So it needs to look clean in Slack markdow n— bullets, bold names, that kind of thing, not a giant table.
> 8. Grouped by owner, since that's how people actually scan it — "what do I owe." An "unassigned / needs an owner" group at the bottom for anything without one.

## Turn 6 — Claude

That's really clear. Third batch — this is the "what could go wrong" round, since edge cases are where a spec usually turns out to be incomplete:

9. What happens with notes that don't have any real action items at all — just discussion and decisions? Should it say so plainly rather than force something into the list?
10. You mentioned tabled/reconsidered items ("should we move the launch date? tabled for now") — anything that gets raised and then explicitly walked back or deferred within the same notes. Should those ever show up, or are they always excluded?
11. Any chance of contradictory or duplicate signals — e.g. the same action item mentioned twice with two different-sounding deadlines, or someone assigned then later reassigned in the same notes?
12. Do your notes ever come in another language, or as a raw transcript dump from a recording tool rather than your own typed notes? (You mentioned Notion pastes from a teammate — is that ever a wall of raw transcript rather than notes?)
13. Where's the line for you — is there anything adjacent to this you explicitly do NOT want the skill doing? (e.g., actually posting to Slack for you, creating calendar reminders or Jira tickets, writing a full meeting summary rather than just action items)

## Turn 7 — Requester (self-generated answer, round 3)

> 9. Yes — some weeks are just status updates and nothing gets assigned. It should just say clearly there were no action items rather than padding the list with a decision dressed up as a task.
> 10. Tabled/deferred items should NOT show up as action items — but I could see wanting a quick separate note like "raised but not resolved: launch date" so it's not silently dropped either. That's a nice-to-have, not core though.
> 11. Yeah that happens sometimes, someone says "I'll do it" early on then later says "actually Jake's taking that one." It should go with whichever is the final/most recent statement, not both.
> 12. Always English, always typed notes — never a raw transcript dump, and never handwriting-to-text. My teammate's Notion pastes are also typed notes, just from a different person, same general messiness level.
> 13. Big one — I don't want it posting to Slack for me, I'll paste it myself. Don't want calendar/Jira integration, don't want it writing a general meeting summary (we don't need "the team discussed X, Y, Z" — just the action items). If notes are so garbled it truly can't tell what's an action item, it should say that rather than guess.

## Turn 8 — Claude

One last round before I write this up — success/failure and the actual trigger phrasing, so the spec's trigger section is grounded in real language rather than guesswork:

14. What's actually been going wrong with the manual version — is it mostly the time it takes, inconsistent formatting, missed items, something else? What would make you trust the output enough to paste it without double-checking every time?
15. What would you actually say to invoke this, in your own words? And — is there anything similar-sounding you'd NOT want it firing on (e.g., "summarize this meeting" without wanting action items pulled out specifically)?

## Turn 9 — Requester (self-generated answer, round 4)

> 14. Mostly time (10-15 min every week reformatting) plus inconsistency — sometimes I group by owner, sometimes I don't, depending how rushed I am, and teammates have said it's hard to scan when the format changes week to week. I'd trust it if it never invents an owner/date and it's honest when notes are ambiguous rather than guessing confidently.
> 15. Realistically I'd say something like "turn these notes into action items for the team" or "clean this up into a to-do list" while pasting the raw notes. I would NOT want it firing if I just say "summarize this meeting" or "what were the key decisions" — that's a different ask, I don't want a full summary, just the action items.

## Turn 10 — Claude (internal)

All Step 1 gaps are now concrete: core job/trigger, inputs (Google Docs live-typed notes, occasional teammate Notion pastes, always English, always typed, weekly sync + client calls, no transcript dumps), variation (client calls messier but same underlying task — no genuine fork, resolved down to one direction), output (Slack-markdown, grouped by owner + "needs an owner" bucket, no invented owners/dates), edge cases (no action items at all, tabled/deferred items excluded but optionally flagged, superseding statements take the latest one, notes too garbled to parse), boundaries (no auto-posting, no calendar/ticket creation, no full summary), success criteria (speed + consistency + never fabricating owner/date). No fork requiring a "pick one" moment — client-call messiness is a degree of the same problem, not a different approach. Proceeding to draft SPECS.md.

## Turn 11 — Claude presents drafts

*(SPECS.md and RUBRIC.md drafted — see accompanying files. Full text also reproduced at the end of this transcript.)*

**Step 5 self-evaluation (performed before presenting):**

- Vague/ambiguous sections? Purpose, Trigger conditions, Inputs, Outputs, Scope & boundaries, Non-goals all read concrete on reread. Initial draft of Non-goals said "doesn't write a full meeting summary" without saying what to do if asked for one alongside action items in the same request — tightened to note it should extract only the action-item portion of a mixed request and say so, rather than silently expanding scope.
- Rubric criteria tracing to the spec? All 8 trace to a specific section (checked against Purpose/Outputs/Edge cases/Scope & boundaries individually) — no generic filler criterion.
- Edge case named in Step 1 but dropped from the draft? Caught one: the "same item reassigned mid-notes, take the latest statement" case (Turn 7, item 11) was in my notes but the first Edge cases draft didn't mention it explicitly — added it as its own bullet rather than leaving it implied by the "no fabrication" language.
- Do rubric levels actually distinguish four outcomes? Reviewed "Owner & due-date fidelity" — the 2 vs 1 levels were nearly identical in the first pass ("mostly correct" vs "some errors"); rewrote 1 to specifically describe inventing a name/date (the requester's explicit red line) so it's a distinct, checkable failure rather than a vaguer "worse than 2."
- Did the requester's own name, or details only meaningful to them, slip into either document? Checked both files line by line — no name appears anywhere; all references are "the person using this skill" / "a team member" / illustrative sample names in the worked example only (which the skill's own generality rule explicitly allows). Confirmed clean.
- Scope creep / size? Both documents are appropriately sized for a single, well-scoped skill — nowhere near the 30k-token watch threshold. No sign this is secretly several skills.

**Claude's message presenting the drafts to the requester:**

Here's the spec and rubric, plus the notes above from my own pass over them before showing you. A few things worth your eyes specifically:

- I kept "tabled/deferred items get a called-out note" as explicitly optional-but-included, since you framed it as nice-to-have but useful — flag if you'd rather cut it for v1 simplicity.
- The rubric has 8 criteria (24 points max) — triggering accuracy, extraction accuracy, owner/due-date fidelity, grouping & format, edge-case handling, source fidelity (no fabrication), boundary adherence, and consistency across runs.

Does this look buildable as-is, and does the rubric feel like it's actually checking the things that would matter to you if someone else built this and you were judging the result?

## Turn 12 — Requester (self-generated feedback round)

> This is really close. Two things:
> 1. Looking at the rubric, "Source fidelity (no fabrication)" and "Edge-case handling" feel like they're scoring almost the same failure twice — both would ding a bad score for inventing an owner. Can you tighten the boundary between them so they're not double-counting the same mistake?
> 2. One realistic case the spec doesn't cover: sometimes I paste a whole week's worth of notes at once if I fell behind — like Monday's sync AND a client call from Wednesday in the same document, back to back. Can you add that as an edge case? I'd want the output to keep them as separate action-item lists per meeting, not merged into one blob.

## Turn 13 — Claude (revision)

Both fair, revising now.

1. Re-scoped the two criteria: **Source fidelity** now covers *fabrication and invention* specifically — never inventing an owner, date, or an action item that isn't grounded in the notes. **Edge-case handling** now covers *correct behavior on the named structural edge cases* (no action items present, tabled items, superseded assignments, garbled notes, multi-meeting batches) assuming nothing is being invented — i.e., did it handle the *shape* of the weird input correctly, not whether it fabricated content. Reworded both criteria's prose and level descriptions so a fabrication mistake only scores against Source fidelity, and a structural mishandling (e.g., merging two meetings together) only scores against Edge-case handling.
2. Added "Multiple meetings pasted in one document" to SPECS.md's Edge cases section, specifying that output should be split into separate per-meeting action-item lists (using whatever meeting/date markers exist in the notes to segment them), and flagged as an open assumption what to do if the notes don't clearly mark where one meeting ends and the next begins (defaulting to asking, rather than guessing at a split point).
3. Re-ran the Step 5 self-check after these edits: both criteria's level descriptions were reread side by side to confirm zero overlapping language now; the new edge case was checked against the rubric's Edge-case handling levels to make sure a 0/1/2/3 result is actually distinguishable for it; confirmed no name or personal framing was introduced by the edits.

## Turn 14 — Requester (self-generated close-out)

> That's exactly the distinction I wanted, and the multi-meeting case is handled the way I'd want it. This is buildable — thanks.

## Turn 15 — Claude

Glad it landed. Both documents are final — `SPECS.md` and `RUBRIC.md` below. This skill's job stops here: no `SKILL.md` gets written and no scoring happens against the rubric — that's for the build-and-grade step later.

---

*(End of live conversation. Final SPECS.md and RUBRIC.md follow in full, and are also saved as standalone files.)*
