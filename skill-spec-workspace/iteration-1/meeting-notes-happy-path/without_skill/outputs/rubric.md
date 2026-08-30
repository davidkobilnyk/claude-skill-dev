# Scoring Rubric: Meeting Notes → Action Item List

**Companion to:** `spec.md`
**Purpose:** Give David (or Claude, when self-checking) a consistent way to judge whether a given run of the skill actually did its job, rather than eyeballing it. Use this on real outputs during build/testing and periodically afterward.

---

## How to use this rubric

Run the skill on a real (or realistic) set of meeting notes. Score each criterion below against that single output. Criteria 1–2 are **hard gates**: failing either means the run fails regardless of other scores, because they represent the two things David explicitly said would make him abandon the tool (fabrication, and unusable format). Criteria 3–8 are scored 0–3 and summed for an overall quality score out of 18.

---

## Hard Gates (pass/fail — either failing fails the whole run)

### Gate 1: No Fabrication
**Pass condition:** Every decision, action item, owner, and due date in the output is directly traceable to specific text in the input notes. Nothing is invented, guessed, or padded in to make the list look more complete.

- Check each action item: can you point to the exact bullet(s) in the source notes it came from?
- Check each owner: was that person/initials actually associated with that task in the notes, or only inferred by "seems like their kind of thing"?
- Check each due date: was it explicitly stated, or interpolated from vague urgency language?
- Check item count: does a short meeting with few real tasks produce a short list, not a padded one?

**FAIL** if even one item is fabricated, over-attributed, or has an invented date.

### Gate 2: Correct Ambiguity Handling
**Pass condition:** Wherever the source notes don't clearly state an owner, the output shows `Owner: TBD` rather than a guessed name. Wherever no date is stated, the output omits the due date field entirely (not "Due: TBD", not an invented date).

**FAIL** if any item silently assigns an owner or date that wasn't explicit in the notes, or if unclear items are dropped instead of flagged as TBD (dropping hides risk of missed work, which is worse than flagging).

---

## Scored Criteria (0–3 each, only scored if both gates pass)

### 1. Bucketing Accuracy
Did each item land in the right section — Decisions Made / Action Items / Open Questions & Follow-ups — per the classification heuristics in the spec?
- **3:** All items correctly bucketed, including judgment-call cases (e.g., first-person asides, decision-vs-task ambiguity) handled per spec.
- **2:** One clear misclassification, otherwise correct.
- **1:** Multiple misclassifications, or a systematic error (e.g., all decisions dumped into Action Items).
- **0:** Bucketing largely absent or unusable.

### 2. Format Compliance
Does the output match the specified structure — section headers, owner/topic grouping, the "verb — Owner: X — Due: Y" line shape, omission rules for empty sections and missing dates?
- **3:** Matches spec exactly, ready to paste into Slack with no reformatting.
- **2:** Minor deviations (e.g., inconsistent bolding, slightly off line shape) that don't require real rework.
- **1:** Recognizable structure but needs meaningful manual cleanup before posting.
- **0:** Structure doesn't resemble the spec.

### 3. Completeness
Are all genuine action items and decisions from the notes present in the output — nothing real left out?
- **3:** Nothing missed.
- **2:** One minor item missed (e.g., a low-signal follow-up).
- **1:** A clear action item or decision is missing.
- **0:** Multiple real items missing; output is materially incomplete.

### 4. Deduplication
Are repeated mentions of the same task/decision correctly merged into a single line rather than duplicated?
- **3:** Clean merging, most complete owner/date info retained.
- **2:** Merged but lost some detail (e.g., dropped the date that appeared on the second mention).
- **1:** Partial duplication remains.
- **0:** Same item appears multiple times as if separate.

### 5. Clarity and Concision
Are action items rewritten into clear, scannable imperative phrases (not copy-pasted fragments), each reasonably short, without changing their meaning?
- **3:** Every line reads cleanly and matches the source's actual meaning.
- **2:** Mostly clean, one or two awkward/fragmentary lines.
- **1:** Several lines are still fragment-like or unclear.
- **0:** Output reads like raw notes, not a cleaned list.

### 6. Grouping Correctness
If By Owner mode: are items correctly grouped under the right owner, in a sensible order, with a single TBD group for unclear owners? If By Topic mode: are groupings sensible and drawn from the notes' own structure?
- **3:** Grouping fully correct and useful.
- **2:** Grouping present but with one misplacement or awkward ordering.
- **1:** Grouping attempted but confusing or partly wrong.
- **0:** No meaningful grouping despite being required.

---

## Scoring Summary

| Gate 1: No Fabrication | Pass / Fail |
|---|---|
| Gate 2: Ambiguity Handling | Pass / Fail |

If either gate fails → **Overall result: FAIL**, regardless of the scored total below.

If both gates pass:

| Criterion | Score (0–3) |
|---|---|
| 1. Bucketing Accuracy | |
| 2. Format Compliance | |
| 3. Completeness | |
| 4. Deduplication | |
| 5. Clarity & Concision | |
| 6. Grouping Correctness | |
| **Total (max 18)** | |

**Interpretation:**
- **16–18:** Ready to use as-is; matches or beats David's manual process.
- **12–15:** Usable but needs light touch-up; worth checking which criterion is dragging the score down.
- **8–11:** Needs real revision before trusting it for a real Slack post; treat as a draft only.
- **Below 8:** Not yet reliable; investigate systematic issues (likely a spec rule the implementation isn't following) before further use.

---

## Example Scoring (using the worked example from spec.md §7)

| Item | Result |
|---|---|
| Gate 1: No Fabrication | Pass — all 6 output items trace to specific source bullets; no invented owners/dates. |
| Gate 2: Ambiguity Handling | Pass — support ticket item correctly shows Owner: TBD; SSO follow-up correctly has no invented date. |
| 1. Bucketing Accuracy | 3 — "check the vendor contract" correctly treated as a personal follow-up, not an action item, since no team member is named as owner. |
| 2. Format Compliance | 3 — matches template exactly. |
| 3. Completeness | 3 — all real items captured; the status-only "API rate limiting is done" is correctly dropped per spec (not a forward task). |
| 4. Deduplication | 3 — n/a, no repeated mentions in this sample, no duplication introduced. |
| 5. Clarity & Concision | 3 — all lines are clean imperative phrases. |
| 6. Grouping Correctness | 3 — owner grouping correct, TBD group placed last. |
| **Total** | **18/18 — Ready to use as-is.** |
