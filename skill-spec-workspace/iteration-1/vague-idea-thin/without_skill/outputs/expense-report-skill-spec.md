# Skill Spec: Expense Report Builder

**Status:** Draft v1 — ready for prototyping
**Author:** David Kobilnyk (via Claude)
**Date:** 2026-08-30

---

## 1. Overview

A skill that turns a pile of raw expense data — receipt photos, a phone-app export, or a manually typed list — into a clean, submission-ready expense report, grouped by category and by client, with totals and basic policy/sanity checks. Primary use case: an independent consultant who tracks expenses ad hoc through the month and needs to turn them into something a client's AP department will accept without back-and-forth.

## 2. Problem / Motivation

David currently reconstructs expense reports by hand at the end of each month: gathering receipt photos, transcribing amounts into a spreadsheet, grouping by category, and reformatting per client. It's repetitive, error-prone (duplicate or missing entries), and the output format has to be re-massaged per client. The skill should remove the manual transcription/formatting work while leaving room for him to review before sending.

## 3. Target User & Context

- Solo/independent consultant, not a company with a formal expense system.
- Submits reimbursable expenses to 2–3 different clients, each with slightly different expectations for report layout.
- No corporate expense tool (Concur, Expensify, etc.) in the loop — this skill *is* the tool.
- No multi-employee approval chain; David is both the filer and the final reviewer before sending.
- Expenses are occasionally in foreign currency (client travel abroad).

## 4. Trigger Conditions

Invoke when the user:
- Says something like "build/generate/put together an expense report," "log this expense," "add these receipts to my expense report," or shares a batch of receipts/expense data and asks for a report.
- Names a specific client or trip the report is for.

Do **not** trigger for general bookkeeping, invoicing *clients for services rendered* (that's revenue, not expense), or personal budgeting requests unrelated to reimbursement.

## 5. Inputs

The skill should accept whatever David has on hand for a given batch, in any combination:

| Input type | Format | Handling |
|---|---|---|
| Receipt photos/scans | JPG/PNG/PDF | Attempt OCR to extract vendor, date, amount, currency; low-confidence extractions are flagged for David to confirm rather than guessed silently. |
| Structured export | CSV from phone expense-tracking app | Parse directly; map its columns to the skill's internal schema. |
| Manually typed list | Free text in chat ("Uber $42 on 8/12, client dinner $110 on 8/14 with 3 people") | Parse into structured line items; ask for clarification only when an amount, date, or category is genuinely ambiguous. |
| Prior report (optional) | Existing spreadsheet | Used as a style/column reference if David wants the new report to match a client's established format. |

Required per line item: date, vendor/description, amount, currency, category. Optional: client/project, payment method, attendees (for meals), notes.

## 6. Outputs

- **Primary:** an Excel (.xlsx) file — David's stated preferred format, since that's what clients ask for.
- **Secondary (on request):** a one-page PDF summary (totals by category, grand total, date range) for quick email attachment.
- Report is organized by category (Travel, Meals, Lodging, Software/Subscriptions, Office Supplies, Other) with a subtotal per category and a grand total, plus a per-day breakdown section for multi-day trips.
- Multi-currency entries show original currency/amount and a converted USD amount (using a rate David supplies or a reasonable default the skill notes explicitly rather than silently assuming).
- Filename convention: `[Client]_Expenses_[MonthYYYY].xlsx`.

## 7. Core Workflow

1. Collect input (photos, CSV, and/or typed entries) for the batch/period David specifies.
2. Extract/parse each entry into the internal line-item schema (date, vendor, amount, currency, category, client, notes).
3. Auto-categorize by keyword/vendor heuristics (e.g., "Uber/Lyft" → Travel, "Marriott/Hilton" → Lodging); ask David to confirm anything it can't confidently categorize rather than guessing silently.
4. Run validation checks (Section 8).
5. Generate the .xlsx (and PDF summary if requested) using the category/total structure above.
6. Present David a short summary before finalizing: total amount, number of line items, any flags raised, so he can catch problems before the report goes out.
7. Save/output the file; do not auto-send to anyone — David reviews and sends manually.

## 8. Validation & Flags

The skill should surface, not silently fix:
- **Missing receipt** for any line item over $25 (a common reimbursement-policy threshold) — flagged, not blocked.
- **Possible duplicates** — same vendor + amount + date (or within 1 day) appearing twice.
- **Non-reimbursable-looking items** — e.g., alcohol-only line items, personal-sounding purchases — flagged for David's judgment call, never auto-removed.
- **Low-confidence OCR reads** — anything the OCR pass isn't confident about gets called out explicitly with the original image referenced, rather than a guessed number going in silently.
- **Missing required fields** (no date, no amount) — asked about directly rather than defaulted.

## 9. Categorization Taxonomy (v1, editable)

Travel, Lodging, Meals & Entertainment, Software/Subscriptions, Office Supplies, Other. David can rename/add categories per client later; v1 ships with this fixed default set plus an "Other" catch-all.

## 10. Out of Scope (v1)

- No direct integration with accounting/expense platforms (QuickBooks, Concur, Expensify, etc.) — output is a standalone file David sends manually.
- No multi-user approval workflow.
- No automatic currency-conversion API call — v1 asks David for the rate or uses a rate he confirms, and states the rate used on the report rather than sourcing it invisibly.
- No tax-filing/Schedule-C mapping (separate concern from client reimbursement).
- No mileage-rate calculator in v1 (flagged as a possible v2 addition — see below).

## 11. Open Questions / Future Enhancements

- **Per-client templates:** v1 ships one generic layout; if clients push back, a per-client template (matching their exact column order/branding) is a natural v2.
- **Mileage tracking:** if David starts logging mileage, a mileage-rate line-item type (IRS standard mileage rate, auto-calculated) could be added.
- **Recurring subscriptions:** auto-detecting recurring software charges from bank/CSV exports to save re-entry each month.
- **Direct currency-conversion lookup:** replace the manual-rate step with a live/near-live FX rate, once David decides he trusts an automated source for that.

## 12. Example Interaction (illustrative)

> **David:** "Put together my August expenses for Acme Corp — I've got these 12 receipt photos plus a couple Uber rides I'll just tell you about."
>
> **Skill:** ingests photos, OCRs them, asks David to confirm 2 low-confidence reads and clarify the category for one ambiguous item, takes the two Uber rides as typed input, flags one $340 hotel charge with no receipt attached, then produces `Acme_Expenses_Aug2026.xlsx` with category subtotals and a grand total, and reports the flag before finishing.
