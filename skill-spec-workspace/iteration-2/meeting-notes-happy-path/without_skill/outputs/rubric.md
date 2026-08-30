# Rubric: Meeting Notes → Action Items

**Companion to:** `spec.md`
**Purpose:** Score any candidate output (from a draft prompt, skill, or manual pass) against a real set of meeting notes, to decide if it's good enough to trust for daily use, and to compare revisions objectively.

## How to use this

1. Take a real (or representative) set of meeting notes and the candidate tool's output for them.
2. Manually classify the notes yourself first (or use the classification in `spec.md` §7 if using the sample notes) — this is your ground truth.
3. Score each of the 8 criteria below, 1–5.
4. Check the two hard-fail conditions first — if either is triggered, the output **fails** regardless of total score.
5. Otherwise, sum the weighted scores. **Pass threshold: ≥32/40, with no individual criterion scoring below 3.**

## Hard-Fail Conditions (check first)

These override the scored criteria entirely — a single instance fails the whole output.

- **HF-1 — Fabrication:** Any action item appears in the output that cannot be traced to a specific commitment in the source notes (e.g., a discussion point turned into a task nobody actually agreed to). Includes inventing an owner, a due date, or scope not present in the notes.
- **HF-2 — Silent drop:** Any line in the source notes that expresses a genuine intent to act, with ambiguous/missing ownership or scope, is simply absent from the output rather than flagged. (A line correctly judged as pure context/decision, and therefore excluded, does *not* count as a drop.)

If HF-1 or HF-2 triggers: record which line(s) caused it, mark the output **FAIL**, and stop — don't bother scoring the rest for that run, though it's still useful to note other issues for the fix-forward pass.

## Scored Criteria (1–5 each, only if no hard-fail)

| # | Criterion | 1 (poor) | 3 (acceptable) | 5 (excellent) |
|---|---|---|---|---|
| 1 | **Recall** — every real action item in the notes is represented in the output | Multiple genuine action items missing | One item missing or one edge case mishandled | All action items present, including subtle/split ones (e.g., the "needs a code reviewer" sub-item) |
| 2 | **Precision** — no context/decision lines wrongly promoted to action items | Several decisions/discussion points wrongly listed as action items | One borderline line wrongly included, defensible either way | Only genuine action items included; discussion/decisions correctly excluded |
| 3 | **Owner attribution accuracy** — owner correct when stated, `[unassigned]` used (not guessed) when not | Owner guessed/wrong on a stated case, or a truly unclear case given a confident (wrong) owner | Owners mostly right; one minor naming inconsistency (e.g. casing) | All stated owners correct; all unclear cases correctly flagged unassigned |
| 4 | **Due date accuracy** — dates extracted only when present, not invented, not silently dropped when present | Date invented, or a stated date dropped | Date preserved but normalized in a way that changes meaning (e.g. wrong day) | All stated dates preserved exactly (or correctly normalized per spec), no invented dates |
| 5 | **Task phrasing quality** — action items rewritten as short, clear, imperative tasks, not copy-pasted raw fragments or vague to the point of uselessness | Raw unedited fragments, or rewritten so loosely the original meaning is lost | Understandable but wordy or slightly awkward phrasing | Concise, imperative, immediately actionable phrasing that a teammate could read with zero context and know exactly what to do |
| 6 | **No merging of distinct items** — topically related but distinct commitments stay as separate line items | Two or more distinct tasks combined into one bullet, losing one of them or muddying ownership | All items separate, but one borderline case merged when it maybe shouldn't have been | Every distinct commitment is its own line, including sub-items like "find a reviewer" |
| 7 | **Format compliance** — matches the Slack-safe template exactly (grouping by owner, checkboxes, no `#` headers, unassigned section present when needed) | Uses unsupported Slack formatting (headers, tables) or ignores grouping entirely | Grouped correctly but minor formatting inconsistency (e.g. missing checkbox, inconsistent bold) | Pastes into Slack cleanly with zero manual cleanup needed |
| 8 | **Ready-to-post usability** — David could copy-paste this into `#team-actions` with zero edits | Needs substantial rewriting before posting | Needs a couple of small tweaks | Genuinely zero-edit, ready to post as-is |

**Scoring:** sum of the 8 criteria (max 40). Multiply nothing — all criteria weighted equally, since the two dimensions David cares most about (fabrication, silent drops) are already enforced as hard fails rather than folded into the weights here.

## Worked Example (scoring the sample output in `spec.md` §7)

Using the worked example output against the sample standup notes:

- HF-1 (fabrication): none triggered — every action item traces to an explicit line.
- HF-2 (silent drop): none triggered — SSL cert and onboarding-data lines both present and flagged unassigned.

| # | Criterion | Score | Why |
|---|---|---|---|
| 1 | Recall | 5 | All 4 real action items present, including the split-out "find a reviewer" item |
| 2 | Precision | 5 | Roadmap-slip and bug-root-cause discussion correctly excluded; standup-time and pricing-copy decisions correctly excluded |
| 3 | Owner attribution | 5 | Sarah/Mike correct; onboarding-data and SSL-cert both correctly unassigned |
| 4 | Due date accuracy | 5 | "today" and "Wed" both preserved as written, no invented dates |
| 5 | Task phrasing | 5 | Short imperative phrasing throughout |
| 6 | No merging | 5 | Code-review need correctly split from the bug fix |
| 7 | Format compliance | 5 | Matches template exactly |
| 8 | Ready-to-post | 5 | No edits needed |

**Total: 40/40 — PASS.** (This is the reference example the spec was built around, so a perfect score here is expected; real test runs against messier notes should be scored honestly and won't always look like this.)

## Recommended Test Set Before Trusting This Daily

Per the spec's worked example being a best case, run this rubric against at least:
- 3–5 real past meeting notes files (sanitized if needed), varying in messiness.
- At least one set that has zero real action items (tests the "none identified" path).
- At least one set with a joke/sarcastic line that could be misread as a commitment.
- At least one set with a duplicate/restated action item within the same notes.

A build is ready for daily use only when it passes (≥32/40, no hard-fails, no criterion <3) on all of the above, not just the one worked example.
