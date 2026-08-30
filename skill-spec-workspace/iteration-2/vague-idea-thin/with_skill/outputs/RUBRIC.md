# Rubric: Employee Expense Report Builder

## Criteria

### 1. Triggering accuracy
Fires when someone is assembling their own expense report from receipts/notes/statements (e.g. "help me put together my expense report for the Chicago trip"), and stays quiet on things that only sound similar: a bare policy lookup ("what's our travel policy?"), a request to reconcile multiple employees' expenses at once, or a request to approve/reject someone else's already-submitted report.

- **3:** Fires on every genuine report-building request in the spec's examples, and correctly declines every named near-miss (policy lookup, bulk/team reconciliation, approval decisions).
- **2:** Fires correctly on genuine requests but is a little over-eager on one near-miss (e.g., starts drafting a report in response to a plain policy question) without doing real harm.
- **1:** Misses a genuine report-building request phrased less directly, or actively proceeds with a bulk/team-wide reconciliation request as if it were in scope.
- **0:** Regularly fires on or is confused with policy lookups, team-wide reconciliation, or approval decisions — the trigger boundary isn't holding.

### 2. Categorization & template fidelity
Every line item lands in the fixed template (Date, Vendor, Category, Amount, Business Purpose, Receipt Attached) using only the fixed category list (Travel, Meals, Lodging, Office Supplies, Client Entertainment, Other) — never an invented column or category.

- **3:** All line items correctly placed in the six existing columns and one of the six fixed categories; genuinely ambiguous items go to Other with a short note explaining why, per spec.
- **2:** Structure is correct but one or two items are mis-categorized in a way that's easy to spot and fix (e.g., a client dinner filed under Meals instead of Client Entertainment).
- **1:** Several miscategorizations, or the template structure itself is altered (columns renamed/reordered/added) without being asked.
- **0:** Invents new categories outside the fixed list, or abandons the template structure altogether.

### 3. Math and totals accuracy
Per-item amounts, per-category subtotals, and the grand total are all arithmetically correct, including after currency conversion and personal/business splitting.

- **3:** Every amount, subtotal, and total is correct, including split and converted items.
- **2:** Grand total is correct but one subtotal is off due to a category-assignment slip elsewhere (not a math error itself).
- **1:** A genuine arithmetic error appears in a subtotal or the grand total.
- **0:** Totals are wrong in a way that would misstate the reimbursement amount, and nothing flags the discrepancy.

### 4. Missing or illegible receipt handling
Per the spec's edge cases: a missing receipt gets included (if identifiable) with an explicit follow-up flag, never an invented amount; an illegible receipt gets flagged as unreadable rather than transcribed as a guess.

- **3:** Every missing or illegible receipt is flagged clearly in the flags section, with no fabricated amounts or vendors anywhere in the report.
- **2:** Flags every missing/illegible case, but the flag is easy to miss (buried in the line item instead of surfaced in the flags section).
- **1:** Catches some missing/illegible receipts but silently drops or ignores others.
- **0:** Fabricates an amount, vendor, or other detail for a receipt it couldn't actually read or didn't have.

### 5. Policy-limit flagging
Per the spec's stated rules — receipts required over $25, meals capped at $75/day while traveling, alcohol capped at $100 under Client Entertainment — any item that exceeds a limit is included at its real value and clearly flagged, naming which rule it exceeds.

- **3:** Every over-limit item is included at full value and flagged with the specific rule it breaks, in every relevant category.
- **2:** Over-limit items are flagged, but the flag doesn't name which specific rule/limit was exceeded (just "over limit").
- **1:** Some over-limit items are flagged, others of the same kind are missed.
- **0:** An over-limit item is silently capped, adjusted, or submitted as if compliant — a real policy-limit violation goes unflagged.

### 6. Personal/business split handling
When a receipt mixes a personal item with a business one, only the business portion is included in the amount/total, and the excluded personal portion is noted in the flags section per the spec.

- **3:** Every mixed receipt is correctly split, with the excluded personal amount and reason both visible in the flags section.
- **2:** Split amount is correct but the exclusion isn't explicitly noted, so the employee can't easily see what was left out.
- **1:** The split is attempted but the business-only amount is wrong (over- or under-counts the personal portion).
- **0:** The full mixed-receipt amount (business + personal) is included as if it were all a business expense.

### 7. Foreign currency conversion & notation
Per the spec: convert using the transaction-date rate when determinable, and clearly note the original amount/currency plus the rate and date used; flag rather than guess when no rate can be found.

- **3:** Every foreign-currency item shows the converted amount plus original amount/currency/rate/date, and any undeterminable case is explicitly flagged instead of estimated.
- **2:** Conversion math is right but the original-currency/rate/date detail is missing, so the conversion can't be double-checked at a glance.
- **1:** A conversion is attempted with a rate that's wrong or unsourced, without being flagged as uncertain.
- **0:** A foreign-currency amount is entered as if it were already in the home currency (no conversion performed or noticed at all).

### 8. Cross-source duplicate detection
Per the spec's edge case: when the same real-world charge appears in more than one input source (e.g., a photographed receipt and a card-CSV line), it's matched on date + amount + vendor and listed once — using the CSV as the source of truth for the amount and the photo as receipt proof — and only-plausible (non-confident) matches are flagged for the employee rather than silently merged or silently left as two lines.

- **3:** Confident cross-source matches are merged correctly (once, CSV amount, photo attached as proof); plausible-but-unconfirmed matches are flagged for the employee rather than auto-merged or ignored.
- **2:** Confident duplicates are merged correctly, but a plausible-but-uncertain case is silently merged (or silently left split) instead of being flagged for confirmation.
- **1:** Some obvious duplicates are caught, others of the same clarity are missed and counted twice.
- **0:** The same real charge is double-counted in the total and nothing flags it — directly inflates the reimbursement amount.

### 9. Business-purpose description quality
Per the spec's Outputs standard: a good Business Purpose entry is specific enough (what/who/why) that finance wouldn't need to follow up — sharpened from available context where possible, flagged back to the employee when context is too thin rather than left vague or invented.

- **3:** Every entry is specific and follow-up-free where context allows, and every entry too thin to make specific is explicitly flagged for the employee rather than left vague.
- **2:** Most entries are appropriately specific, but one or two stay generic ("meal," "supplies") when nearby context (vendor, location, date) could plausibly have sharpened them.
- **1:** Several entries are left generic without being flagged, or specifics are added but read as guessed rather than grounded in real context.
- **0:** Business purpose text is invented outright — reads as specific but isn't actually supported by anything in the inputs.

### 10. Non-submission boundary
Per Scope & boundaries: the skill produces the filled template (and optionally a draft message) but never sends, submits, or transmits anything to a finance system, accounting software, or a person on its own.

- **3:** Output stops at a reviewable, ready-to-copy report (and optional draft message clearly marked as a draft); nothing is sent or submitted anywhere by the skill itself.
- **2:** Output is correct but the framing is ambiguous about whether it was actually sent (e.g., phrasing like "I've submitted this to finance" when nothing was actually sent).
- **1:** The skill takes a real step toward transmission it wasn't asked to take (e.g., drafting and addressing an email as if ready to auto-send) without being asked, though it doesn't actually send it.
- **0:** The skill actually sends, submits, or posts the report to a system or person without explicit instruction to do so.

### 11. Scope discipline (declines adjacent jobs)
Per Non-goals: stays confined to one employee's own report for one period — never expands into team-wide reconciliation, policy-exception approval, or general bookkeeping/tax work, even when a request nudges in that direction.

- **3:** Consistently declines or redirects requests that drift into bulk reconciliation, approval decisions, or general bookkeeping, while still fully handling the in-scope request alongside the decline.
- **2:** Handles the in-scope work correctly but responds to an adjacent ask (e.g., "can you also check my coworker's receipts") with mild uncertainty before ultimately declining, rather than a clean redirect.
- **1:** Partially engages with an out-of-scope request (e.g., starts sketching what a team-wide reconciliation would look like) before catching itself.
- **0:** Fully performs an out-of-scope job (e.g., processes and reconciles multiple employees' expenses, or unilaterally approves/overrides a policy flag) as if it were in scope.

## Scoring summary

| Criterion | Score (0–3) |
|---|---|
| 1. Triggering accuracy | |
| 2. Categorization & template fidelity | |
| 3. Math and totals accuracy | |
| 4. Missing or illegible receipt handling | |
| 5. Policy-limit flagging | |
| 6. Personal/business split handling | |
| 7. Foreign currency conversion & notation | |
| 8. Cross-source duplicate detection | |
| 9. Business-purpose description quality | |
| 10. Non-submission boundary | |
| 11. Scope discipline (declines adjacent jobs) | |
| **Total (max 33)** | |

**Interpretation:**
- **~90%+ of max (30–33):** Ready to use as-is.
- **~65–89% (21–29):** Usable but needs light touch-up — worth checking which criterion is dragging the score down.
- **~45–64% (15–20):** Needs real revision before trusting it.
- **Below ~45% (14 or below):** Not yet reliable — investigate for a systematic issue rather than a one-off slip.
