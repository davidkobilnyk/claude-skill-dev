# Transcript — skill-spec run on "expense reports" idea

**Scenario:** vague-idea-thin / with_skill
**Date:** 2026-08-30

---

## User (opening message)

> I have an idea for a skill around "expense reports" but haven't thought it through much. Can you spec it out for me?

---

## Claude — Step 0 / Step 1 (internal, before asking anything)

*(Internal reasoning, not shown verbatim to the user but reflected in what's asked next)*

Step 0 check: this reads as a genuine reusable-skill request ("I have an idea for a skill around X") — not a one-off task in disguise. No need to redirect; proceed.

Step 1 stock-take: essentially nothing is known yet beyond the two words "expense reports." That's a single fragment, not even a rough shape of who/what/when. Per Step 2, when the idea is this thin, start with grounding questions before anything else — don't guess at inputs, outputs, or variation yet.

---

## Claude — Round 1 (grounding questions)

Happy to spec this out properly — it'll take a few rounds of questions since "expense reports" is still pretty open. Let's start broad:

1. Who submits these expense reports, and who (or what) ultimately receives and processes them? Is this for individual employees, contractors, a finance team, something else?
2. What does the process look like today — paper receipts, a spreadsheet, an app like Expensify, email threads? What's actually happening right now when someone needs to file one?
3. What's the specific frustration that made you think "there should be a skill for this"? What's annoying or slow about the current way?

## "User" (simulated answer, round 1)

Good questions — honestly I haven't thought about this super carefully yet. I work at a smallish company, maybe 120 people. Employees submit expenses to get reimbursed, and I'm on the finance/ops side who has to process them. Right now it's kind of a mess — people email me receipts with a rough one-line summary, or sometimes they use a shared Google Sheet template we have, but inconsistently. I guess the pain is mostly mine: I spend a lot of time chasing people down for missing receipts and double-checking their math.

---

## Claude — Round 2 (narrowing: inputs, output format, policy, trigger)

That helps a lot. A few more, now that we have the shape of it:

1. When someone sits down to do this, what do they actually have in front of them — receipt photos, forwarded emails, a corporate card statement/CSV, handwritten notes, some mix?
2. Is there already a template or format the output needs to match (like that shared Google Sheet), or would this skill need to invent categories and structure from scratch?
3. What are the actual policy rules that matter — spending limits, receipt requirements, disallowed categories? Anything with real numbers attached?
4. What would someone actually say or do right before they'd want this skill to kick in — e.g., "help me put together my expense report for the Chicago trip"? Is there a similar-sounding request that should *not* trigger it (like just asking what the travel policy says)?

## "User" (simulated answer, round 2)

1. Usually a folder of receipt photos or PDFs from their phone/email, and sometimes a corporate card CSV export from the bank portal if they used the company card. People jot down what each thing was for — sometimes in a text to me, sometimes not at all.
2. Yes, we do have a template — a Google Sheet with columns: Date, Vendor, Category, Amount, Business Purpose, Receipt Attached (Y/N). Categories are Travel, Meals, Lodging, Office Supplies, Client Entertainment, Other.
3. Policy: receipts required for anything over $25. Meals capped at $75/day when traveling. Alcohol only reimbursable under Client Entertainment, capped at $100. No reimbursement for personal items even if they're on the same receipt as a business expense.
4. Trigger would be something like "help me put together my expense report for [trip/month]" or "can you organize these receipts into an expense report." It should *not* fire on something like "what's our travel policy" — that's just a factual lookup, not building a report.

---

## Claude — Round 3 (resolving the fork + edge cases + boundaries)

This is coming together well. Two things I want to pin down before I write anything, because they'd genuinely change the shape of the spec:

1. **Possible fork:** is this for an *individual employee* preparing their own reimbursement request, or could it also be used by you/finance to reconcile *everyone's* card statements in bulk at month-end? Those are pretty different jobs (one person's receipts vs. a team-wide reconciliation), and this skill can only be spec'd one way.
2. Walk me through the messiest realistic cases: a receipt is missing, a receipt is blurry/illegible, a charge is in a foreign currency, a receipt mixes a personal item with a business one, an expense blows past a policy limit, or the same charge shows up in more than one place. What should happen in each?
3. Should this ever actually *submit* or send the report anywhere on its own, or should it always stop at producing something for a human to review first?
4. Last one — what would make you actually trust and keep using this, versus give up on it after one bad experience?

## "User" (simulated answer, round 3)

1. Let's keep it to the individual employee side — someone preparing their own expense report to submit to me. Bulk reconciliation across the whole team is a different problem, let's not fold that in here.
2. Missing receipt → flag it as needing follow-up, don't guess an amount. Blurry/illegible → flag it rather than risk mis-transcribing a number. Foreign currency → convert using that day's rate if you can find one, and clearly note that it was converted (and from what currency/rate). Personal item mixed into a business receipt → only include the business portion in the total, and note the split so I can see what was excluded and why. Expense over a policy limit (like a $150 dinner) → include it but flag it clearly, don't silently submit it as if it's fine.
3. Never auto-submit or send anything anywhere. I always want to review before it goes to me "for real." At most it should fill out the Sheet template format and maybe draft a short email to me — I send it myself.
4. Trust = the receipts are categorized correctly, the math is right, and anything that needs my attention (missing receipt, over-limit expense) is clearly called out instead of buried in a wall of line items — that's literally the thing eating my time today. It would lose my trust fast if it confidently made up a number for a receipt it couldn't actually read, or missed an obvious policy violation.

---

## Claude — internal check before drafting

All Step 1 gaps now feel concrete enough to write down without guessing:

- **Core job / trigger** — pinned down, including an explicit non-trigger example.
- **Inputs** — receipt photos/PDFs, card CSV, informal notes; examples given.
- **Variation / fork** — resolved explicitly to individual-employee-only; bulk/team reconciliation ruled out as a non-goal.
- **Output** — fixed structure (the existing Sheet template + its exact columns/categories).
- **Edge cases** — missing receipt, illegible receipt, foreign currency, mixed personal/business, over-limit expense, and (noted but not yet fully drawn out) duplicate charges across sources.
- **Boundaries** — never auto-submits; stops at draft for human review.
- **Success/failure** — named explicitly (correct categorization + math + surfaced flags vs. fabricated numbers or missed violations).

One thing still thin: "duplicate charge across sources" was named in the question but the answer didn't directly address it — flagging this to come back to during the self-check in Step 5 rather than guessing now.

Proceeding to draft `SPECS.md`.

---

## Claude — drafting SPECS.md and RUBRIC.md

*(Full text of both documents as first drafted is in `SPECS.md` and `RUBRIC.md` in this same folder — the versions saved there are the final, post-revision versions. The first-draft `RUBRIC.md` had 10 criteria; see the Step 5 and Step 6 notes below for what changed.)*

First draft `RUBRIC.md` criteria (10 total): Triggering accuracy; Categorization & template fidelity; Math/totals accuracy; Missing/illegible receipt handling; Policy-limit flagging; Personal/business split handling; Foreign currency conversion & notation; No unauthorized auto-submission; Scope discipline (declines bulk/team reconciliation and generic policy questions); Clarity of flagged items.

---

## Claude — Step 5: self-evaluation (first pass)

Rereading both documents adversarially, as the person who'd have to build `SPECS.md` with no further access to ask questions:

1. **Duplicate charges across sources** — this was explicitly asked about in Round 3 but the user's answer didn't address it, and I didn't catch that gap before drafting. It's a realistic case (a lunch could appear both as a photographed receipt *and* as a line on the card CSV) and right now neither `SPECS.md`'s edge cases nor `RUBRIC.md` covers it. **This needs to go back to the user rather than being silently assumed** — I'll surface it in Step 6.
2. **Business Purpose field quality** — the template requires free text here, but the spec doesn't say anything about what makes that text adequate (a vague "meal" vs. "dinner with Acme Corp re: Q3 renewal") and the rubric doesn't score it either. This is a real gap between what "done" means and what's checked — worth raising too.
3. Checked every rubric criterion against a specific spec section: all 10 trace back cleanly (e.g. "Policy-limit flagging" → the exact $25/$75/day/$100 figures in Inputs; "No unauthorized auto-submission" → Scope & boundaries). No generic/template criteria found.
4. Checked each criterion's four levels for real separation (not near-duplicate phrasing between adjacent levels) — they hold up; e.g. for "Missing/illegible receipt handling," a 2 is "flags it but the flag is easy to miss/buried," a 1 is "flags it inconsistently — catches some, silently drops others," a 0 is "fabricates a number or invents a vendor for the unreadable receipt" — those are genuinely different failure shapes, not a gradient of the same sentence.
5. Size check: both documents are well under the 30,000-token concern threshold — this is a scoped, single-employee-workflow idea, not something that's ballooned into several skills' worth of surface area.

**Net finding:** the documents are solid but incomplete on two points (duplicate-charge handling, business-purpose text quality) that surfaced during this adversarial reread rather than during the Q&A. Flagging both to the user in Step 6 rather than quietly assuming an answer.

---

## Claude — Step 6: presenting to the user

Here's the draft. Two things came up when I reread it adversarially just now, before showing you anything:

1. **Duplicate charges across sources** — I asked about this in the last round but your answer skipped it. If a lunch shows up both as a photo you took *and* as a line on the card CSV, should the report catch that it's the same charge and only list it once? Or is it not actually a real overlap in practice (e.g., you only ever use one source or the other per expense)?
2. **"Business Purpose" text quality** — the template has a free-text field for this. Should the report only score/flag on the *structural* stuff (categorized right, math right, receipt present), or does the actual wording of that field matter too — like whether it reads as a real, specific justification ("dinner with Acme Corp re: Q3 renewal") vs. something vague ("meal")? That affects whether I should score it in the rubric at all.

*(Both `SPECS.md` and `RUBRIC.md` presented in full alongside this — see the finalized versions in this folder.)*

## "User" (simulated feedback, round 4)

Good catches, both real:

1. Yes — duplicates are a real problem. If someone pays with the corporate card *and* photographs the receipt (which happens more often than I'd like), it should not show up as two line items. Match by date + amount + vendor if possible, and if it finds an overlap, use the card CSV as the source of truth for the amount and just attach the photo as the receipt proof.
2. Actually yes, the wording matters more than I said — a vague "meal" business purpose is one of the top reasons I have to bounce a report back to someone. So it's fair to hold this skill to a standard here: it should turn "grabbed lunch" into something specific, or flag it back to the employee if there isn't enough context to write anything specific at all.

## Claude — revising

Updating both documents:

- **`SPECS.md`** — added an explicit edge case for cross-source duplicate charges (match on date + amount + vendor, card CSV as source of truth for amount, photo kept as receipt proof, and what happens when a match is ambiguous). Added a line under Outputs describing what a good Business Purpose entry looks like (specific enough to name what/who/why) versus what should get flagged back to the employee for more context.
- **`RUBRIC.md`** — added an 11th criterion, **Business-purpose description quality**, with its own 0–3 scale grounded in the "meal" vs. "dinner with Acme Corp re: Q3 renewal" example. Expanded the existing edge-case-driven criteria to also cover the duplicate-source case explicitly rather than leaving it implicit. Scoring summary table and max score updated from /30 to /33 (11 criteria × 3).

## Claude — Step 5: self-evaluation (second pass, after revision)

- Duplicate-charge handling is now named explicitly in both documents, with the exact resolution rule (date+amount+vendor match, CSV as source of truth) rather than a vague "handle duplicates."
- Business-purpose quality now has both a spec-level description of "good" (Outputs section) and a rubric criterion with concrete 0–3 levels — no more silent gap between what's built and what's scored.
- Rechecked all 11 rubric criteria trace to specific `SPECS.md` sections — still true, nothing generic added.
- Rechecked level-4 separation on the two changed criteria (the expanded edge-case criteria, and the new business-purpose criterion) — levels describe genuinely different outcomes, not restated phrasing.
- Size check again: still well under the token ceiling; the two additions were targeted, not scope creep into new territory (both were already-scoped edge cases inside "individual employee's own reimbursement report," not new capabilities).

No further gaps found. Presenting the revised documents.

## "User" (simulated final approval)

This looks buildable now — I don't see anything else I'd need to explain to someone before they built it. The rubric feels like it actually reflects what would make me trust or distrust this in practice, not a generic checklist. Good to stop here.

## Claude — closing

Both documents are finalized as `SPECS.md` and `RUBRIC.md`. Per this skill's scope, the job stops here — it does not write the actual skill (SKILL.md) or apply the rubric to anything; both are handoffs for whoever builds and later grades the finished skill.
