# Skill Spec: Expense Report Builder

**Status:** Draft v1 — based on a short scoping conversation, not yet built or tested.
**Owner:** David Kobilnyk
**Date:** 2026-08-30

---

## 1. Problem / Motivation

David travels for work a few times a month and currently builds expense reports by hand:
gathering receipt photos/PDFs from his phone and email, cross-referencing them against a
bank/card CSV export, and manually entering everything into a shared company Excel template.
It's tedious and error-prone (easy to miss a receipt, miscategorize a purchase, or fat-finger
a total).

The skill should take that pile of raw inputs and produce a submission-ready expense report
with minimal manual entry, while flagging anything that needs a human decision (missing
receipts, out-of-policy amounts, ambiguous categories).

## 2. Who Uses It / When It Triggers

- **User:** David, personal use (not built for a team/org rollout, at least not v1).
- **Trigger phrasing:** things like "build my expense report for [trip/month]", "process
  these receipts", "put together my expenses for the Chicago trip."
- **Cadence:** roughly monthly, or after each business trip. Not a background/automated
  process — invoked explicitly each time with that trip's/month's files.

## 3. Inputs

| Input | Format | Notes |
|---|---|---|
| Receipts | Photos (jpg/png/heic) and PDFs, dumped in a folder | Not pre-sorted; may include duplicates or non-receipt junk |
| Card/bank statement | CSV export from bank | Ground truth for amounts and dates; used to catch missing receipts |
| Company template | .xlsx, fixed columns (Date, Vendor, Category, Amount, Business Purpose, Payment Method) | Category values are a fixed dropdown list in the template — must match exactly |
| Trip context (optional, free text) | e.g. "Chicago trip, Aug 12–15, client: Acme Corp" | Used to fill in "Business Purpose" and to scope which statement lines are in-trip vs personal |

## 4. Outputs

1. **Filled company .xlsx template** — one row per expense, matching existing column
   headers and category dropdown values exactly, ready to attach to the internal
   submission email/system.
2. **Short PDF or on-screen summary** — total by category, total by day, grand total,
   and an explicit **exceptions list**:
   - Statement charges with no matching receipt found
   - Receipts with no matching statement charge (cash, or card not in this statement)
   - Amounts that don't reconcile between receipt and statement (tip added, currency
     conversion, etc.)
   - Anything that looks out-of-policy (see §6)
3. Nothing gets auto-submitted anywhere — output is a file David reviews and sends himself.

## 5. Core Workflow (draft)

1. **Ingest** — read every file in the receipts folder; OCR/parse images and PDFs to pull
   vendor, date, amount, and (if present) a line-item description.
2. **Parse statement** — read the bank CSV; normalize dates/amounts.
3. **Match** — pair each statement line to a receipt by amount + date proximity (±1–2 days
   to allow for posting delay) and rough vendor name match. Anything below a confidence
   threshold goes to the exceptions list instead of being force-matched.
4. **Categorize** — map each matched expense to one of the template's fixed category values
   (e.g. Meals, Lodging, Airfare, Ground Transport, Other) using vendor name/description;
   default to "Other" plus a flag when uncertain rather than guessing silently.
5. **Filter to trip scope** — if trip context/date range is given, exclude statement lines
   clearly outside it (or ask, rather than silently drop, if ambiguous).
6. **Fill template** — write matched, categorized rows into a copy of the .xlsx template,
   preserving its existing formatting/columns.
7. **Summarize + flag** — produce the totals-by-category view and the exceptions list.
8. **Human review checkpoint** — present the summary and exceptions before considering the
   report "done"; David fixes/fills gaps by hand for the flagged items.

## 6. Policy Rules to Encode (v1 guesses — confirm against actual company policy doc)

- Meals: flag if a single receipt exceeds a per-meal cap (placeholder: $75) — company's
  actual number TBD, should be read from a policy doc if one exists rather than hardcoded.
- Alcohol: flag separately if identifiable, since many corporate policies cap or exclude it.
- Receipts required above some threshold (placeholder: $25) — anything above that with no
  receipt is a hard exception, not a soft one.
- No auto-approval logic of any kind — the skill flags, it never decides something is fine.

## 7. Edge Cases / Open Questions

- **OCR reliability** on crumpled/handwritten/foreign-language receipts — expect a
  non-trivial "couldn't read this one, here it is for manual entry" bucket.
- **Foreign currency** — statement CSV will show converted USD; receipt shows local
  currency. Need to reconcile without treating the FX difference as a mismatch exception.
- **Split expenses** (e.g. a group dinner where David paid and will be reimbursed by
  colleagues separately) — out of scope for v1; treat as a normal expense unless told
  otherwise.
- **Multiple cards/accounts** — v1 assumes one CSV per report; multi-card support is a
  later enhancement.
- **Duplicate receipts** (same charge photographed twice) — de-dupe by amount+date+vendor
  before matching.
- **Template drift** — if the company changes the .xlsx template's columns/categories, the
  skill should fail loudly (mismatched headers) rather than silently writing into the wrong
  columns.

## 8. Definition of Done (v1)

Given a folder of receipts, one bank CSV, and the blank company template for a single trip,
the skill produces:
- a filled template with every clearly-matchable expense correctly rowed and categorized,
- an exceptions list that catches everything it couldn't confidently resolve (never silently
  drops or misfiles something), and
- a summary David can read in under a minute to sanity-check totals before submitting.

Success is measured by: **little/no re-keying of matched expenses**, and **zero
false-confident errors** (a wrong entry is worse than a flagged one).

## 9. Explicitly Out of Scope (v1)

- Auto-submitting to any expense system (Concur, etc.) — David's company uses a plain
  Excel template, not a system with an API.
- Multi-user / team rollout, approval workflows, manager sign-off.
- Tax/accounting treatment beyond what the template already captures.
- Learning/adapting category mappings over time (could be a v2 idea — start with a static
  vendor→category heuristic list).

## 10. Next Steps

- Confirm actual company expense policy (per-meal cap, receipt threshold, alcohol rules)
  instead of the placeholder numbers in §6.
- Get a sample (real or scrubbed) copy of the .xlsx template and a sample CSV export to
  nail down exact column headers/category values before building anything.
- Decide OCR approach (built-in image reading vs. a dedicated OCR step) once real receipt
  samples are available — messy real-world receipts may need more robust handling than
  clean test images.
- Once those are in hand, this spec is ready to hand to a skill-building process to turn
  into an actual buildable skill (instructions, any helper scripts for CSV/xlsx parsing,
  and a couple of test scenarios like "trip with a missing receipt" and "trip with a
  foreign-currency charge").
