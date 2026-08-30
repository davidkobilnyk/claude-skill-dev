# Transcript — Meeting Notes → Action Items skill spec

**Context:** User (David) opened with a request to spec out a skill idea, not build it yet. Running the `skill-spec` skill.

---

## User (opening message)

> I keep manually turning my messy meeting notes into clean action item lists for my team afterward, and it takes forever. I want a skill that does this so I don't have to reformat it every time. Can you help me spec this out — I want a proper written spec and rubric before I actually build it, not just a quick chat.

---

## Claude — Step 0 check

This is clearly a recurring, reusable need ("I keep manually... every time"), not a one-off task, so it's worth the full spec treatment. Moving straight into it.

## Claude — Step 1 (internal: known vs. unknown)

**Known so far:**
- Core job: turn messy meeting notes into a clean action item list for the team
- Trigger moment: after a meeting, notes exist, David wants them reformatted
- Pain point: manual reformatting is slow and repetitive

**Unknown (needs questions):** where notes come from and what they look like, what "clean" output actually looks like and where it goes, team size/how people are referred to, how ambiguous cases (missing owner/date, decisions vs. actions, duplicates, tangents) should be handled, boundaries, and what's gone wrong with the manual version before.

## Claude — Round 1 of questions

To get this detailed enough to build from without follow-up questions later, I want to dig into a few things:

1. **Where do the raw notes come from, and what do they actually look like?** Do you type them live during the meeting, dictate them, jot rough shorthand, or something else? If you can paste a real (or realistic) example of what your notes look like before cleanup, that'll help a lot.
2. **Where does the cleaned-up list end up, and is there a format you already lean toward** — e.g. assignee, due date, priority — or is it just "readable bullets"?
3. **Roughly how big is the team, and how are people referred to in your notes** — full names, first names, initials, @-handles?

---

## User (round 1 answer)

Good questions.

1. I mostly type notes live during the meeting on my laptop (Google Docs or just a scratch doc), sometimes it's quick shorthand typed on my phone's Notes app if it's a hallway/standup type meeting. It's messy — half-sentences, no consistent structure, sometimes decisions and action items and random asides all mixed together. Here's a real-ish example of what I'd paste in:

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

2. Mostly I paste the result into our Slack team channel right after the meeting, occasionally I'll drop it into a follow-up email if someone missed the meeting. I don't have a format I love yet — I want something like: who owns it, what the action is, and the due date if one was actually mentioned. Nothing fancy, needs to look clean in Slack (so no markdown tables, those render terribly there).

3. It's a small team — 7 people (me, Sarah, JK, Mike, Priya, Tom, Elena). In notes I'll refer to people by first name usually, sometimes just initials for whoever's top of mind (like "JK"), rarely full names.

---

## Claude — Round 2 of questions

That example note is really useful — it already shows a few of the messy patterns I need to plan for (mixed decisions/actions/asides, an unowned item, a vague action, a date given as a hard deadline vs. none at all). A few more things:

4. In that example, "figure out who owns onboarding" has no owner, and "update the API docs" has no due date. What should happen in cases like that — leave the field blank, flag the item as needing attention, or something else?
5. Your notes mix actual action items with decisions ("went with option B"), reminders unrelated to work handoff ("Mike's on vacation"), and pure noise ("snacks order late"). Should the output *only* be action items, or do you also want decisions captured (even if in a separate section), with the noise dropped?
6. Do you ever paste notes that cover more than one meeting/topic in one go, or is it always one meeting's notes at a time? And if the same action item basically gets mentioned twice in slightly different words, should those get merged?
7. This is always you pasting the raw text directly into the chat, right? Or would you ever want this to pull notes directly from a Google Doc or Notion page instead of copy-pasting?

---

## User (round 2 answer)

4. Leave it blank rather than guessing — but I do want unowned items to stand out somehow, like grouped separately, so they don't get silently missed. Same for due dates: if nothing's said, just don't show a date, don't make one up.
5. Just action items should be the main list — but yeah, actually, decisions are useful context sometimes (like when someone asks "wait why are we doing X"), so a short separate "Decisions" section would be nice to have, optional but useful. The snack order stuff should just get dropped, nobody needs that in the recap.
6. Usually one meeting at a time, but sometimes I'll paste two standups back to back if I forgot to do it the day before. If it's clearly two different dated sections like my example header, keep them separate; if it's just one blob, treat it as one meeting. And yes — if something's basically said twice (like "look into stripe" and later "mike's looking into the webhook thing"), merge those into one item rather than listing both.
7. Always paste-in for now. I don't want it reaching into a doc or Notion on its own — I don't even keep a consistent single source, it's genuinely copy-paste from wherever I happened to type that day. Don't build the doc/Notion connection into this.

---

## Claude — Round 3 of questions

Good — that resolves a fork I was starting to see (paste-in text vs. reading from a connected doc). Going with paste-in only; I'll note the doc/Notion route explicitly as a non-goal so it's not silently assumed later. A last round on failure modes and boundaries:

8. When you've done this manually and it's gone badly, what specifically went wrong — items getting missed entirely, wrong person credited, tone that didn't land right for the channel, something else?
9. Is there anything that should *never* end up in the output even if it's technically phrased like a to-do — e.g. personal reminders, things already done, items clearly directed at just you and not the team?
10. If a chunk of notes is genuinely too garbled to confidently turn into an item (not just missing a field, but unclear what's even being asked), should the output flag that inline, or should it stop and ask you about it before finishing?

---

## User (round 3 answer)

8. Mostly missed items — when notes are long I'll skim past something buried in the middle. Also inconsistency: one week the recap has due dates, the next week I forget to include them even when they were mentioned, so the team stopped trusting the format was reliable. Tone-wise it's a casual startup team, so overly formal/corporate phrasing feels off — keep it plain and direct, not stiff.
9. Yeah — anything that's clearly just personal (like "Mike's on vacation next Wed") isn't an action item for the team, that's just FYI, drop it or maybe it belongs in a tiny "FYI" note at most, not the action list. Also don't include something already resolved in the meeting itself.
10. Flag it inline rather than stopping to ask — I paste this right after a meeting and want the bulk of it fast; if two or three lines are unclear, mark them clearly (like "⚠️ unclear — needs a human check") so I can fix just those by hand, rather than blocking the whole output on it.

---

## Claude — Step 1 gap check (internal)

Running back through the Step 1 list: core job ✓, inputs (format, source, real example) ✓, variation (paste-only resolved, no connector; single vs. multi-meeting pastes resolved) ✓, output (structure, destination, tone) ✓, edge cases (missing owner/date, decisions, duplicates, noise, garbled lines, personal-only items) ✓, boundaries (no auto-posting, no connector reads, no invented fields, no full meeting minutes unless separately asked) ✓, success/failure (missed items, inconsistent formatting, tone mismatch) ✓. No open forks remain. Drafting both documents now.

---

## Claude — drafts SPECS.md and RUBRIC.md

*(see `SPECS.md` and `RUBRIC.md` in this same folder for the full documents drafted at this point)*

## Claude — Step 5 self-evaluation (first pass)

Rereading both documents as the person who'd have to build from them with no further access to ask questions:

- **Vague/ambiguous sections?** The first draft of "Outputs" leaned Slack-specific ("no markdown tables") but David also mentioned occasionally pasting into email — email clients don't choke on markdown tables the way Slack does, so a Slack-only framing under-specifies the email case. Tightened the wording so the format requirement is "plain hyphen-bullet list, no tables, readable as raw text" — which happens to satisfy both destinations rather than special-casing one.
- **Rubric criteria traceability:** All criteria trace to a named spec section. One exception I flagged for myself: I had drafted a standalone "duplicate/near-duplicate merging" criterion, but the spec only supports this with a single example (the "stripe webhook" case) — thin grounding for a full criterion on its own. Noted for the loop step rather than silently cutting it.
- **Edge cases named but not addressed?** Checked all edge cases from Step 1/Q4–Q10 (missing owner, missing date, decisions, duplicates, multi-meeting pastes, personal-only items, garbled lines) — each has an explicit rule in the spec's Edge cases section. None orphaned.
- **Level descriptions distinguishing four real outcomes?** Reread each criterion's 0–3 scale. Levels for "Owner attribution accuracy" and "Boundary respect" were solid. The "Tone/format consistency" criterion (draft) had 2 vs. 1 blurring into near-identical phrasing ("mostly consistent" vs. "somewhat consistent") — needs sharper level 1/2 language, flagged below.
- **Scope creep?** Neither document is ballooning — SPECS.md stays focused on the paste-in, action-item-list scope David actually described; I didn't fold in meeting-minutes generation, calendar sync, or auto-posting even though they're adjacent, since David explicitly scoped those out.

**Fixed directly:** Outputs section wording (Slack-and-email-safe framing). **Flagged to raise with David rather than deciding alone:** whether "duplicate merging" deserves its own rubric criterion or should fold into extraction completeness, and I also tightened the blurry tone-consistency level language before presenting.

---

## Claude — presents documents to David

Here's the draft spec and rubric for **Meeting Notes → Action Items**. A few notes from my own review before you look:

- I sharpened the output-format wording so it works for both Slack and email pastes, not just Slack.
- I'm not fully sure the rubric needs a standalone "duplicate merging" criterion — it's grounded in only one example from our conversation. I left it in for now but wanted to flag it; happy to fold it into extraction completeness instead if it feels like overkill.
- Tone in the rubric's level descriptions got a tighten-up so level 2 and level 1 don't read as near-duplicates.

Does this look buildable to you as-is, and does the rubric feel like it's actually capturing what would make this useful or not? *(full documents shown to David — omitted here, see SPECS.md / RUBRIC.md)*

---

## User (feedback, Step 6 loop)

This is close. Two things:

1. You called it — fold "duplicate merging" into the extraction-completeness criterion, it's not a big enough thing on its own to score separately, I was going to say the same.
2. One thing missing: nothing in the rubric actually checks for the *tone* fitting a casual startup team vs. sounding like corporate email-speak. That was a real complaint I have about my own manual attempts sometimes (I overcorrect into stiff phrasing when I'm rushing). Can you add that as its own criterion instead of burying it inside format consistency?

Otherwise the spec itself looks right — the example you used matches what I actually paste in, and the edge case list covers what I was worried about.

---

## Claude — revision

Made both changes:

- Merged the duplicate/near-duplicate criterion into **Action item extraction completeness** (duplicates are now one of its explicit failure modes at each level, rather than a separate criterion).
- Split tone out of the old combined "Output format consistency & readability" criterion into its own **Tone fit** criterion, with levels grounded specifically in the "casual team, not corporate email-speak" complaint — and tightened the remaining format-consistency criterion's levels now that tone isn't riding along inside it.
- Net effect: criteria count stays at 9 (one merge, one split cancel out numerically), but the actual content is sharper — tone is now checkable on its own instead of hiding inside a broader bucket, and duplicate-handling is now grounded as an explicit failure mode within extraction completeness rather than floating as its own thinly-supported criterion.

## Claude — Step 5 self-evaluation (re-run after revision)

- Reconfirmed every remaining criterion still traces to a specific spec section (tone fit → Outputs section's tone note + Q8 startup-casual detail; extraction completeness's merged duplicate-handling → Edge cases' "stripe webhook" example).
- Re-checked the new Tone fit criterion's 0–3 levels for blur — level 2 ("mostly plain, one or two phrases read stiff") and level 1 ("noticeably corporate in tone throughout") are now clearly distinct outcomes, not paraphrases of each other.
- Reconfirmed scoring summary math: 9 criteria × 3 = 27 max; interpretation bands recomputed against 27, not left at the prior draft's 30.
- No new scope creep introduced by the edit — the split/merge was a rebalancing, not new territory.

## Claude — presents revision

Updated both. Duplicate-merging is folded into extraction completeness now (with the stripe-webhook pattern as its concrete example at each level), and Tone fit is its own criterion grounded in the corporate-vs-casual concern you raised. Scoring table recalculated for the new 9-criterion total (max 27).

---

## User

This looks right. Ready to build from.

---

## Claude

Good — spec and rubric are finalized as `SPECS.md` and `RUBRIC.md`. Per this skill's scope, that's where this stops: no `SKILL.md` gets written and the rubric doesn't get applied to anything here — those are the next, separate steps whenever you're ready to actually build it.

**[END OF RUN — natural stopping point reached, both documents finalized and accepted]**
