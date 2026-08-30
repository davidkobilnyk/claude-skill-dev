# Transcript — skill-spec run: "Meeting Notes → Action Items"

## Opening message (user)

> I keep manually turning my messy meeting notes into clean action item lists for my team afterward, and it takes forever. I want a skill that does this so I don't have to reformat it every time. Can you help me spec this out — I want a proper written spec and rubric before I actually build it, not just a quick chat.

---

## Step 0 — Is there actually something to spec?

This is clearly a recurring, reusable task (done "every time," described as taking "forever"), not a one-off — so the skill-spec workflow applies, no need to check whether they actually want it.

**Claude:** This sounds like a solid candidate for a real skill — a recurring task with a repeatable shape, not a one-off. Let's spec it out properly. Since I want `SPECS.md` to be buildable with zero follow-up questions, I'm going to ask a fair number of questions across a couple of rounds before drafting anything — that's the whole point of doing this instead of a quick chat. First round coming up.

---

## Step 1 & 2 — Round 1 of questions

**Claude asked:**
1. **Trigger** — When exactly do you want this to fire? Do you paste the notes in and explicitly say "turn these into action items," or should it also recognize meeting notes automatically even without an explicit ask?
2. **Inputs** — Where do your notes usually come from (Google Doc, Notion, plain text, something else)? Can you describe (or paste an example of) what "messy" typically looks like for you? Do the notes usually have names and dates in them, or are those often missing?
3. **Output** — Who receives the final list, and how do you usually get it to them (Slack message, email, a shared doc)? Do you always want the same fields — owner, task, due date — or does that vary by meeting?
4. **Context** — Roughly how big is your team, and what kinds of meetings does this apply to?

**User answered:**
> We type notes live in a Google Doc during the meeting — it's a mix of bullet fragments and half-sentences, sometimes with initials for who owns something, sometimes not. I'd paste the notes in and say something like "clean these up into action items" or "turn this into a list for the team." Dates are often vague — "before launch," "next week" — or just not mentioned even when someone clearly said something out loud. Final list usually goes into a Slack message to the team channel, sometimes I copy it into a follow-up email instead. I want owner, task, and due date every time. Team is 7 people, product team — we have a weekly planning meeting that covers several project threads at once, and a shorter twice-weekly sync that's usually just one topic.

---

## Step 1 & 2 — Round 2 of questions

Round 1 covered core job, inputs, and most of outputs. Still open: variation (does the planning meeting vs. the short sync need different treatment?), edge cases, boundaries, and success/failure criteria — so a second round.

**Claude asked:**
1. **Variation** — The planning meeting spans several project threads and the sync is single-topic — does the output need genuinely different structure for each, or is it really the same list, just sometimes grouped by topic and sometimes not?
2. **Edge cases** — What should happen when an item has no clear owner? No due date? When it's phrased ambiguously, like "someone should look into X"? What about notes that include stuff that isn't an action at all — FYI updates, decisions with no follow-up, tangents, pasted links?
3. **Boundaries** — Should this ever guess at an owner from context (e.g., "I'll take that" without a name), or always flag it instead? Should it post/send anything itself, or only produce text you paste in yourself? Should it remember action items across meetings over time?
4. **Success/failure** — What specifically goes wrong today with the manual process? What would make you trust this skill vs. not trust it?

**User answered:**
> It's really the same underlying list either way — the only difference is the planning meeting needs it grouped by project thread since there are several going on, and the sync doesn't need grouping since it's one topic. I don't want to have to tell it which each time — it should just be obvious from the notes whether there are multiple topics or one.
>
> For no owner — please don't guess, just flag it clearly so I know to fill it in myself, something like "TBD." Same for no date — don't make one up, just say there isn't one. "Someone should look into X" — still list it, just with the owner flagged. FYI stuff, decisions with no action attached, small talk, random pasted links — none of that should be in the list at all. I only want actual action items. If a decision *does* lead to someone needing to do something, capture that action, just not the decision itself.
>
> Don't guess an owner from "I'll take that" unless the notes actually say who said it — if there's no speaker attribution in the notes, don't infer it. Don't send anything anywhere — I'll copy-paste it myself into Slack or email, whichever I need that day. And no, it doesn't need to remember anything across meetings — each meeting's notes are a clean slate.
>
> What goes wrong today: it takes 20–30 minutes every time, the formatting is different every week because I'm doing it ad hoc, and I've definitely missed items that were buried in the middle of a tangent, or forgotten to note a date that was said out loud. I'd trust this if it consistently gets the real items, doesn't miss the buried ones, and doesn't just make up an owner or date when it doesn't actually know.

At this point every Step 1 gap is concrete: core job, inputs (with a real shape described), the one potential fork (grouped vs. flat) has been resolved into a single rule rather than left as two competing approaches, outputs, edge cases, boundaries, and success/failure are all pinned down. No further questions needed before drafting.

---

## Step 3 — Draft `SPECS.md`

Drafted in full — see `SPECS.md` in this folder for the version presented to the user in Step 6 (after the Step 5 self-check fixes described below were already folded in).

Notable drafting decisions worth surfacing:
- The "grouped vs. flat" fork was resolved into one auto-detection rule (multi-topic → group by topic; single-topic → flat list) rather than asked-per-run or split into two specs, per Step 3's instruction to resolve forks through questions rather than leaving them open.
- "TBD – needs assignment" and "No date set" were adopted as fixed placeholder strings (rather than just "don't guess" left vague) so the eventual builder — and the rubric — has something concrete and checkable to test against.

---

## Step 4 — Draft `RUBRIC.md`

Derived directly from the spec's purpose, outputs, and edge cases — see `RUBRIC.md` in this folder. Six criteria: triggering accuracy (required), extraction completeness/precision, correct handling of missing owner/date, output format consistency, respecting scope boundaries, and honest handling of empty/ambiguous input. Each traces to a specific section of `SPECS.md` rather than being a generic quality checklist.

---

## Step 5 — Self-evaluation (adversarial reread)

Read both documents as if I were a builder with no further access to the person, and as if I were about to grade a finished skill against the rubric with no context beyond it.

**Findings:**

1. **Gap found — duplicates not addressed.** The person didn't explicitly mention duplicate action items, but live meeting notes commonly restate the same task mid-discussion and again in a wrap-up. Leaving this unaddressed would let a builder ship something that lists the same item twice and would leave the rubric unable to penalize that specific, likely failure mode. *Fixed:* added a "Duplicate or near-duplicate items" edge case (merge into one entry) to `SPECS.md`.
2. **Gap found — zero-action-item case not addressed.** A status-only sync could produce no genuine action items at all. Without an explicit instruction, a model under pressure to "produce a list" might fabricate a plausible-sounding item rather than say the notes had none. *Fixed:* added an explicit edge case requiring the skill to say so plainly ("No action items found") rather than fabricate.
3. **Checked — output section was underspecified for "consistent formatting."** The person's core complaint was inconsistent week-to-week formatting, but the original draft only described the fields in prose, which leaves room for a builder to interpret the exact structure differently each time. *Fixed:* added a fixed Markdown template (with a checkbox-per-item structure) and worked examples for both the grouped and flat cases, so "done" is checkable rather than descriptive.
4. **Checked — rubric criteria all trace back.** Re-read each rubric criterion against `SPECS.md`: triggering accuracy → Trigger conditions section; extraction completeness → Purpose + Edge cases; owner/date handling → Edge cases + Scope & boundaries; format consistency → the new Outputs template; scope boundaries → Non-goals; empty/ambiguous handling → the newly added edge cases. No orphan criteria.
5. **Checked — scope creep.** Nothing in the draft pushed past the original idea (no sending, no tracking, no summarization crept in) — Non-goals section holds the line explicitly.
6. **Flagged, not resolved:** the spec assumes English-only notes and doesn't ask about localization, since the person never raised it and it didn't come up naturally in either round. Left as a stated open assumption rather than silently designed around, since I'm not fully sure it's a non-issue for this team.

All fixable gaps (1–3) were corrected directly in the drafts before presenting them. Item 6 is flagged for the person rather than resolved unilaterally.

---

## Step 6 — Present to the user and loop

**Claude presented:** both documents in full, plus the self-evaluation notes above (including the flagged, unresolved assumption about English-only notes), and asked directly: *"Does this look buildable to you — could someone build the actual skill from `SPECS.md` without having to come back and ask you anything? And does the rubric actually capture what would make this worth using, or is it missing something that would matter to you day-to-day?"*

**User feedback (round 1):**
> This is close. Two things. First — I want it to be extra explicit that it should never infer an owner just because someone used "I" in the notes without the notes saying who was speaking — that's exactly the kind of wrong-guess that would make me stop trusting it, so I want that spelled out as its own line, not folded into the general "don't guess" wording. Second — dates aren't just vague phrases like "next week," sometimes they're tied to an external event we haven't scheduled yet, like "after the conference" or "once legal signs off" — I want it clear that those get carried through as-is too, not treated differently from "next week." Other than that, the rubric looks right to me — it actually reflects what would make me trust this or not. English-only is fine, we're a US-based team, don't need to flag that as open anymore.

**Claude's revision:**
- `SPECS.md` → Scope & boundaries: split the owner-guessing rule out from the general "doesn't push forward" bullet into its own explicit bullet naming the "I"-without-speaker-attribution case directly, so it can't be read as folded into a softer general statement.
- `SPECS.md` → Edge cases: broadened the vague-due-date edge case to explicitly include event-dependent phrasing ("after the conference," "once legal signs off"), not just relative-time phrasing, so both are named as carried-through-as-stated.
- `SPECS.md` → Open assumptions: removed the English-only item as a *flagged* assumption and folded it in as a settled, stated assumption instead, since the person confirmed it directly.
- `RUBRIC.md` → Criterion 3 ("Correct handling of missing owner/date"): tightened the failure example to explicitly call out inferring ownership from an unattributed "I'll take that," matching the sharpened spec language, and confirmed the vague-date language already generalizes to event-dependent phrasing without needing a separate criterion.

**Re-ran Step 5 self-check after this revision** (required after any nontrivial change): reread the two edited spec sections and the one edited rubric criterion for vagueness, re-traced the tightened rubric criterion back to the now-more-explicit spec bullets, confirmed no new edge case was introduced without corresponding rubric coverage, and confirmed the file sizes are nowhere near the 30,000-token concern threshold (each document is a few thousand tokens). No new gaps found.

**Claude presented the revised sections and asked:** *"Does that cover it — anything else that would make you hesitate to actually build from this?"*

**User (round 2):**
> No, that covers it. This is good to build from.

**Stop.** Both documents are finalized as of this round; no further revision requested. Final versions are saved as `SPECS.md` and `RUBRIC.md` alongside this transcript.
