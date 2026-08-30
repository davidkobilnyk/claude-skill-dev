# Rubric: Meeting Notes → Action Items

## Criteria

### 1. Triggering accuracy
Fires when someone provides meeting notes and asks for them to be turned into an action item list (explicit phrasing like "turn these into action items," or notes pasted with a short "format this"-style instruction), and stays quiet — or, for a mixed request, does only the action-item portion and says so — on requests that sound adjacent but want something else: a general meeting summary or "what were the key decisions," a request to actually post/send/file the output somewhere, or non-meeting text (a personal to-do list, a project brief).

- **3:** Fires correctly on every genuine trigger case, and on every near-miss either declines cleanly or (for a mixed request) does only the action-item portion and names what was left out.
- **2:** Fires correctly on genuine triggers, but on one near-miss case either fires when it shouldn't or silently expands scope (e.g., produces a summary alongside the action items without flagging it) rather than declining or scoping down.
- **1:** Misses a real trigger phrasing that should have worked, or fires and delivers a full meeting summary/minutes when only action items were the ask.
- **0:** Systematically confuses this task with a different one — e.g., treats every "summarize this meeting" request as an action-item request, or vice versa.

### 2. Action item extraction accuracy
Whether the output correctly identifies which lines in the notes are genuine commitments (something someone said or clearly implied they'd do) versus decisions, FYIs, or discussion that merely sound task-like.

- **3:** Every genuine commitment in the notes is captured, and nothing that was only a decision, FYI, or open discussion point is listed as an action item.
- **2:** All genuine commitments are captured, but one borderline decision/FYI is also listed as if it were an action item (over-inclusion), without materially changing what the list means.
- **1:** A real commitment is missed entirely, or more than one non-commitment is listed as an action item.
- **0:** The list is built primarily from decisions/discussion rather than actual commitments — the core purpose of the output is not met.

### 3. Owner & due-date fidelity
Whether owners and due dates on each item come only from what is stated or clearly implied in the notes, with uncertainty flagged rather than resolved by guessing.

- **3:** Every owner and date shown is either explicitly stated or clearly implied by context; anything genuinely uncertain is marked as such rather than presented as fact; nothing is invented.
- **2:** All shown owners/dates are real, but one clearly-implied case is treated as unconfirmed when it didn't need to be (an overly cautious flag), or a genuinely unconfirmed case is stated slightly too plainly without a clear "unconfirmed" marker.
- **1:** One owner or date is stated as fact when the notes only weakly implied it, or something with a genuinely missing owner/date is placed in the wrong group instead of "Needs an owner" / left undated.
- **0:** An owner, name, or date is invented outright — attributed to someone or something never mentioned in the notes, or a due date is stated for an item the notes never dated.

### 4. Grouping & format
Whether the output matches the specified structure: bulleted, Slack-markdown, grouped by bolded owner name, with a trailing "Needs an owner" group, and nothing beyond what renders cleanly in Slack.

- **3:** Correctly grouped by owner with bold names, unassigned items correctly collected in a trailing "Needs an owner" group, and formatting is clean, pasteable Slack markdown with no extraneous structure (no tables, no unnecessary headers).
- **2:** Grouping and formatting are correct, but a minor cosmetic inconsistency exists (e.g., inconsistent bolding, an owner group ordered oddly) that doesn't affect scanability.
- **1:** Items are correctly identified but the grouping structure is wrong in a way that hurts scanning (e.g., flat list instead of grouped by owner, or unassigned items scattered rather than collected at the bottom).
- **0:** Output isn't usably formatted at all — e.g., a paragraph instead of a list, or formatting that would render broken in Slack.

### 5. No-action-items handling
Whether the output correctly recognizes and plainly states when a set of notes contains no genuine action items, rather than padding the list.

- **3:** When notes are purely discussion/decisions/status with nothing committed to, the output says so plainly and does not force any item onto the list.
- **2:** Correctly recognizes there are no action items, but the "none found" statement is vague or awkwardly phrased rather than direct.
- **1:** Pads the list with a decision or FYI dressed up as an action item to avoid returning an empty result.
- **0:** Fabricates one or more action items that have no basis anywhere in the notes.

### 6. Edge-case structural handling
Whether the output correctly handles the shape of the specific structural edge cases named in the spec — tabled/deferred items, superseded or reassigned items, and multiple meetings pasted into one document — assuming nothing is being invented (fabrication itself is scored under criterion 7).

- **3:** Tabled/deferred items are excluded from the action list (optionally called out separately); superseded items appear once, correctly reflecting only the most recent statement; multiple meetings in one document are correctly split into separate per-meeting lists using markers present in the notes.
- **2:** One of these three cases is handled slightly imperfectly in a low-stakes way — e.g., a tabled item is omitted with no callout when one would have helped, without it being treated as an action item.
- **1:** One of these cases is handled wrong in a way that changes what the output communicates — e.g., an outdated (superseded) version of an item is shown instead of the current one, or two meetings' items are merged into a single undifferentiated list.
- **0:** A tabled/deferred item is presented as a live action item, or a superseded assignment leads to the same task appearing twice under two different owners with no resolution.

### 7. Source fidelity (no fabrication)
Whether every action item, owner, and date in the output is traceable to something actually present in the notes — the specific failure mode of inventing content, independent of whether an edge case's structure was handled correctly.

- **3:** Every element of the output — items, owners, dates — is grounded in the actual notes; nothing is invented to fill a gap or make the output look more complete.
- **2:** Output is fully grounded, but phrasing on one item slightly overstates the notes' certainty (e.g., stating an implied owner a touch more confidently than the notes support) without inventing a person, date, or task outright.
- **1:** One detail (a name, date, or minor item) is invented that isn't supported anywhere in the notes.
- **0:** Multiple invented details appear, or a person is named as an owner who is never mentioned anywhere in the source notes.

### 8. Boundary adherence
Whether the output stays within the skill's actual job — producing a paste-ready text list — without drifting into the non-goals: posting/sending on the person's behalf, creating calendar or ticket entries, or writing a general meeting summary.

- **3:** Output is exactly a text action-item list, nothing more — no attempt to send/post it anywhere, no calendar or ticket content generated, no general summary included unless the action-item portion of a mixed request was explicitly all that was asked for.
- **2:** Output stays in scope but includes a small unrequested extra (e.g., one unprompted sentence of overall meeting recap) that doesn't misrepresent the list itself.
- **1:** Output meaningfully drifts into a non-goal — e.g., includes a real summary/minutes section without being asked, or drafts calendar-style text ("Reminder: ...") beyond the action item itself.
- **0:** Output behaves as if it actually performed an integration action (claims to have posted, sent, or filed something) rather than just producing text.

## Scoring summary

| Criterion | Score (0–3) |
|---|---|
| 1. Triggering accuracy | |
| 2. Action item extraction accuracy | |
| 3. Owner & due-date fidelity | |
| 4. Grouping & format | |
| 5. No-action-items handling | |
| 6. Edge-case structural handling | |
| 7. Source fidelity (no fabrication) | |
| 8. Boundary adherence | |
| **Total (max 24)** | |

**Interpretation** (cutoffs computed against 8 criteria, max 24):
- **22–24 (~92%+):** Ready to use as-is.
- **16–21 (~67–88%):** Usable but needs light touch-up — worth checking which criterion is dragging the score down.
- **11–15 (~46–63%):** Needs real revision before trusting it.
- **0–10 (below ~46%):** Not yet reliable — investigate for a systematic issue rather than a one-off slip.
