# Rubric: Meeting Notes → Action Items

## Criteria

### 1. Triggering accuracy
Checks both halves: does the skill fire when someone pastes messy notes and asks to have them turned into an action list (in whatever phrasing), and does it correctly stay quiet on the named near-misses — a request for a meeting summary/minutes, a request to draft an upcoming agenda, general note organizing with no action-list intent, or notes pasted with no request attached at all.

- **3:** Fires on natural phrasings ("clean this up for the team," "sort this out," a bare paste of notes with "format this") and correctly declines or asks a clarifying question on every near-miss case (summary request, agenda request, no-request paste) instead of guessing.
- **2:** Fires correctly on the clear cases but is uncertain or asks an unnecessary clarifying question on one obvious near-miss instead of confidently recognizing it (e.g., hesitates on a plainly agenda-drafting request).
- **1:** Fires correctly most of the time but produces an action list on at least one case that should have been declined or asked about (e.g., silently treats a "summarize this meeting" request as an action-item request).
- **0:** Regularly conflates action-item requests with meeting-summary requests, or fires on notes pasted with no request attached at all, producing unrequested output.

### 2. Action item extraction completeness
Checks that every genuine action item in the notes makes it into the list — nothing buried mid-note gets skipped — and that duplicate or near-duplicate mentions of the same item (e.g., "look into stripe" and later "mike's looking into the webhook thing") are merged into one bullet rather than listed twice or missed. This is the single complaint David named most directly about the manual version.

- **3:** Every real action item is captured, including ones buried mid-list among decisions/asides, and every duplicate mention (worded differently or not) is correctly merged into a single bullet under the right owner.
- **2:** All action items are captured, but one duplicate mention slips through as a separate bullet, or one item's phrasing is slightly reworded from the source without changing its meaning.
- **1:** At least one genuine action item is missed entirely (the exact failure mode David described from doing this by hand), even if duplicates are handled correctly.
- **0:** Multiple action items are missed, or the list fabricates an item that wasn't actually stated in the notes.

### 3. Owner attribution accuracy
Checks that owners are correctly identified when stated or clearly implied (e.g., "mike said he'd take a look"), that items with no owner are grouped into the "Needs an owner" sub-list rather than guessed at or silently dropped, and that names are recognized consistently even when referred to inconsistently (first name vs. initials).

- **3:** Every stated or clearly implied owner is correctly attributed, and every genuinely unowned item is grouped under "Needs an owner" — no fabricated owners anywhere.
- **2:** Owners are attributed correctly, but one unowned item is left ungrouped in the main list instead of being separated out (still visible, just not flagged as clearly as it should be).
- **1:** One item is given a fabricated or guessed owner not actually supported by the text, or one clearly-implied owner (like "mike said he'd take a look") is missed and wrongly grouped as unowned.
- **0:** Owners are fabricated routinely, or the "Needs an owner" grouping is dropped entirely, letting unowned items blend in and get missed the same way the manual process did.

### 4. Due date handling
Checks that stated or explicit dates (e.g., "due before launch on 9/15") are captured correctly, that purely relative phrases with no anchor ("whenever he gets a chance") are correctly treated as no due date rather than resolved into an invented date, and that this doesn't drift week to week the way David's manual version did.

- **3:** Every explicitly stated date is captured correctly and attached to the right item; every item with no real date is left with no due-date clause at all — never fabricated, never inconsistently included.
- **2:** Dates are handled correctly, but formatting of a stated date is inconsistent (e.g., "9/15" vs. "September 15" mixed within the same list) without being wrong.
- **1:** One item with no real due date is given a fabricated or inferred one (e.g., turning "whenever he gets a chance" into a specific date), or one genuinely-stated date is dropped.
- **0:** Due dates are fabricated or omitted inconsistently across the list — the same unreliability problem that made David's team stop trusting the manual recap.

### 5. Decisions vs. action item separation
Checks that decision statements ("decided to go with option B") are routed to the separate optional Decisions section and never listed as action items, that personal/logistical notes ("Mike's on vacation next Wed") go to the small FYI section or are dropped rather than treated as team actions, and that pure noise (unrelated asides) is dropped silently.

- **3:** Decisions are cleanly separated from the action list, personal/logistical notes are correctly routed to FYI or dropped, and pure noise never appears anywhere in the output.
- **2:** Separation is correct, but one decision or FYI item is included in the main output when the notes had no decisions/FYI content to report (over-inclusion of a borderline case rather than a real miscategorization).
- **1:** One decision or personal-only note is misfiled as an action item (e.g., "decided to go with option B" appearing as a to-do), or noise like the snacks aside leaks into the output.
- **0:** Decisions and action items are not meaningfully distinguished, or personal/logistical content is regularly presented as team action items.

### 6. Ambiguous or garbled input handling
Checks that a note fragment too unclear to confidently phrase as an action gets flagged inline (`⚠️ unclear —` plus what's ambiguous) rather than silently dropped or guessed into something more specific than the notes actually support, and that this flagging never blocks the rest of the output from being produced.

- **3:** Every genuinely unclear fragment is flagged inline with a short, accurate note on what's ambiguous, phrasing elsewhere stays exactly as vague or specific as the source (no invented specificity), and the rest of the output is produced without being blocked by the unclear lines.
- **2:** Unclear fragments are flagged correctly, but the flag's explanation is vague enough that David would need to go re-read the original note to know what's actually unclear about it.
- **1:** One genuinely ambiguous fragment is either silently dropped or resolved into something more specific than the notes support, instead of being flagged.
- **0:** The output stalls or asks the person to resolve ambiguity before producing anything, or ambiguous lines are routinely guessed into confident-sounding but unsupported action items.

### 7. Output format consistency & readability
Checks that the output matches the spec'd structure — plain hyphen-bullet list, no tables, `[Owner]: action, due <date>` format, "Needs an owner" and optional Decisions/FYI sections in the right place — and reads cleanly whether pasted into Slack or email, plus that two clearly-separated meetings in one paste stay under their own distinct headers rather than being merged into one undifferentiated list.

- **3:** Structure matches the spec exactly (bullets, no tables, correct sub-sections in the right place), reads cleanly copy-pasted into either Slack or email, and two distinctly-headered meetings stay correctly separated.
- **2:** Structure is correct and usable, but has a minor cosmetic inconsistency (e.g., inconsistent spacing or bullet style between sections) that doesn't affect readability in Slack or email.
- **1:** The output uses a markdown table or another format element that would render poorly in Slack, or two clearly-separated meetings get incorrectly merged into one list.
- **0:** The structure drifts from the agreed format enough that it wouldn't be immediately obvious this came from the same skill week to week — the exact "inconsistent formatting" complaint that eroded the team's trust in the manual version.

### 8. Tone fit
Checks that phrasing stays plain and direct, matching a casual startup team's voice, rather than drifting into stiff, corporate, or overly formal language — a specific failure David named from his own rushed manual attempts (e.g., turning "update the API docs" into "please proceed to update the relevant API documentation at your earliest convenience").

- **3:** Phrasing throughout reads plain and direct, close to how the notes themselves were phrased, with no stiff or corporate-sounding rewrites anywhere in the list.
- **2:** Overwhelmingly plain and direct, but one phrase reads more formal than necessary without being actually stiff or out of place.
- **1:** Noticeably corporate or over-formal phrasing shows up repeatedly across the list (the "at your earliest convenience" pattern), even though the content itself is accurate.
- **0:** The list reads like a formal corporate memo throughout, losing the casual voice David explicitly asked this to preserve.

### 9. Boundary respect
Checks adherence to the spec's non-goals and stop conditions: never auto-posts or sends the output anywhere, never reads from a connected doc/Notion source instead of pasted text, never produces a full meeting-summary/minutes narrative unless that was actually what was asked for, and correctly asks for pasted text (rather than attempting to process it) when given audio, an image, or a doc link instead.

- **3:** Output stays a plain text list handed back to the person with no attempt to post/send it anywhere, no attempt to fetch from any external source, no unrequested meeting-narrative content, and correctly declines/redirects when given a non-text input (audio, image, doc link).
- **2:** Boundaries are respected, but the response includes one small unrequested extra (e.g., a one-line meeting-narrative preamble above the list) that wasn't asked for, without crossing into a full summary.
- **1:** The output drifts into a real non-goal once — e.g., producing a full narrative meeting summary unprompted, or offering to post the result to Slack directly.
- **0:** The skill attempts to act outside pasted-text input entirely (e.g., claims to read from a linked doc), or regularly produces meeting-minutes-style output instead of the requested action list.

## Scoring summary

| Criterion | Score (0–3) |
|---|---|
| 1. Triggering accuracy | |
| 2. Action item extraction completeness | |
| 3. Owner attribution accuracy | |
| 4. Due date handling | |
| 5. Decisions vs. action item separation | |
| 6. Ambiguous or garbled input handling | |
| 7. Output format consistency & readability | |
| 8. Tone fit | |
| 9. Boundary respect | |
| **Total (max 27)** | |

**Interpretation** (bands computed against this rubric's actual max of 27, across 9 criteria):
- **~90%+ of max (24–27):** Ready to use as-is.
- **~65–89% (18–23):** Usable but needs light touch-up — worth checking which criterion is dragging the score down.
- **~45–64% (12–17):** Needs real revision before trusting it.
- **Below ~45% (0–11):** Not yet reliable — investigate for a systematic issue rather than a one-off slip.
