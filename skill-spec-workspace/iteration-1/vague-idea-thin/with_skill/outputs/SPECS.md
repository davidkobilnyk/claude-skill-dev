# Spec: Expense Report Builder

## Purpose
Turns a freelancer's pile of mixed-format receipts and confirmations for a given month into a categorized, client-ready expense report — either a filled-in Excel template or an itemized PDF summary — cutting the manual transcription work down to a review-and-send pass. Addresses the recurring monthly dread of manually retyping every receipt into a client's spreadsheet, and the risk of typos, dropped receipts, or miscategorized line items that comes with doing it by hand.

## Trigger conditions
Fires when:
- The user hands over a batch of receipts/confirmations (photos, PDFs, forwarded emails) and asks to build, assemble, or turn them into an expense report for a named client or period — e.g. "put together my expense report for Acme for July," "turn these receipts into an expense report," "here's this month's receipts for [client]."
- The user references one of their known client templates by name when asking to generate a report.

Should NOT fire (looks similar but isn't this):
- A one-off "what category is this receipt" question with no report being assembled.
- A request to submit, file, email, or upload the report anywhere — this skill stops at producing the file (see Scope & boundaries).
- General bookkeeping/accounting or tax questions unrelated to a specific report being built (e.g. "how do I track my quarterly taxes").
- Anything involving the third client's manual-portal workflow — that client is explicitly out of scope (see Non-goals).

## Inputs
- A batch of receipts/proof-of-expense for one reporting period (typically a month), in mixed formats: photos of paper receipts, PDF vendor invoices/emailed receipts (e.g. Uber, hotels, SaaS subscriptions), and forwarded confirmation emails that may have no attachment at all (e.g. a flight confirmation email body).
- Which client the report is for — this determines the category scheme, any spending caps, and the output template (see Outputs).
- Occasional foreign-currency receipts (observed case: CAD) mixed in with USD.
- Assume no personal expenses are mixed into the input pile — the user maintains a separate personal card and only surfaces business receipts.
- Completeness varies: some items may lack a clear amount (illegible/blurry), lack a receipt entirely (confirmation-only), or lack enough detail to categorize confidently.
- Assume the batch handed over in a single run belongs to one client. If receipts for more than one client are mixed into the same batch, that's an edge case (see Edge cases), not a supported multi-client input.

## Outputs
Two supported client-specific formats, selected by which named client the report is for:

1. **Excel-template output** (Client A's format) — fills in a template with columns: Date, Category, Amount (USD), Description/Business Purpose, Receipt attached (yes/no). Category scheme: Travel, Meals, Software/Tools, Other. Meal line items exceeding $75/day should be flagged, not withheld or auto-adjusted. Each line needs a short, specific Description/Business Purpose (e.g. "Client dinner with X team"), not a generic placeholder.

2. **PDF itemized-summary output** (Client B's format) — an itemized list of date, category, and amount per expense, totaled. This client uses a simpler, separate category scheme: **Travel** and **Everything else** — it is not the same four-category scheme as Client A's template. No per-line business-purpose text is required for this client.

Both formats:
- Include a clearly separated "Needs Review" section listing anything flagged (missing amount, no receipt attached, unclear category, foreign currency needing a rate check, a meal over the $75/day cap, a probable duplicate) — flagged items still appear in their normal place in the body of the report as well, just marked, rather than being pulled out of the main list.
- The report total should reconcile to the sum of everything in the input pile with a legible amount. Items with no legible/stated amount are excluded from the total, shown as blank (not a guessed figure), and called out in Needs Review.
- Foreign-currency line items are converted to USD using the transaction date's exchange rate, with the original currency/amount noted alongside the converted figure so the user can double-check it.

A third client (Client C) uses a manual web portal the user enters into by hand; no output format is produced for this client at all (see Non-goals).

For a client not yet mapped to either known template and category scheme above, the skill should ask which output format and category scheme is wanted rather than guessing or defaulting to one of the two known ones.

## Scope & boundaries
- Produces the finished report file (Excel or PDF) for the user to review and send themselves.
- Never sends, emails, uploads, or submits the report anywhere, to any client, under any circumstances — that action stays entirely with the user, without exception.
- Handles only the two clients whose output formats and category schemes are defined above; a genuinely new/unmapped client triggers a clarifying question rather than an assumed format.
- Single-user context: this builds the user's own report for their own submission. No multi-person approval, review-by-manager, or team-expense-pooling workflow is in scope.
- Does not integrate with any accounting or expense platform (e.g. QuickBooks, Expensify, a client's portal) — output is a standalone file.
- A single run is scoped to one client's batch of receipts. Mixed-client input is an edge case to be flagged, not silently split and processed (see Edge cases).

## Non-goals
- Auto-submitting or filing the report anywhere (portal, email, upload) — explicitly and permanently out of scope, not just "not yet built."
- Supporting Client C's manual-portal workflow in any form — the user handles that entirely by hand using her own totals.
- Real-time/as-you-go expense logging — this is a monthly batch job triggered when the user hands over a period's worth of receipts, not a running tracker.
- Distinguishing business from personal expenses — the input pile is assumed pre-filtered to business-only by the user before it's handed over.
- Tax categorization, quarterly tax prep, or accounting-system integration.
- Enforcing or blocking over-cap spending — the skill flags a meal line over the $75/day cap for the user's attention; it never removes, caps, or auto-adjusts the figure.
- Automatically splitting or allocating a mixed-client batch across clients — see Edge cases.

## Edge cases
- **Illegible or missing amount on a receipt**: never guess a number. Exclude it from the report total, list it in Needs Review with the amount left blank, and note whatever else is known (vendor/date if visible).
- **Confirmation email with no attached receipt** (e.g. a flight booking confirmation): include as a line item using whatever amount/detail is stated in the email body if present; if no amount is stated anywhere, treat it like a missing amount (flag, don't guess).
- **Foreign currency receipt (e.g. CAD)**: convert to USD using the transaction date's exchange rate, show the original currency and amount alongside the converted figure, and flag it in Needs Review so the user can double-check the rate.
- **Meal expense over the $75/day cap (Client A only)**: include it at its real amount, flag it in Needs Review; never cap, drop, or silently adjust it.
- **Ambiguous category**: make a best-effort categorization using the named client's defined scheme, but flag it in Needs Review so the user can confirm or correct it — never silently pick a category without flagging when it was genuinely ambiguous.
- **Named client has no known template/category scheme**: stop and ask the user which output format and categories they want, rather than defaulting to either known scheme or inventing a new one.
- **Receipt duplicated in the pile** (e.g. the same purchase appears as both a photo and a forwarded confirmation email): flag as a probable duplicate in Needs Review rather than silently including it twice or silently dropping one.
- **Total doesn't obviously reconcile** (e.g. the user mentions spending more than what's visible in the pile): flag the discrepancy rather than presenting an incomplete total as final.
- **Mixed-client batch** (receipts for more than one client handed over together in one run): don't guess an allocation. Flag it clearly and ask the user to confirm which receipts belong to which client before producing either report, rather than silently splitting them by best guess.

## Open assumptions
- "The transaction date's exchange rate" is assumed to mean the rate on the date of purchase; the specific rate source wasn't pinned down by the user and is left to whatever the skill's builder finds reasonable, as long as the figure is clearly noted as needing the user's double-check.
- Client A's $75/day meal cap and four-category scheme, and Client B's two-category scheme, are the two concrete cases the user described; the spec assumes a genuinely new client's rules are supplied by the user at the start of a run (stated then, or established in an earlier conversation) rather than invented by the skill — same treatment as an unmapped template.
- "Duplicate" detection is assumed to be a best-effort same-vendor/same-date/same-amount heuristic that gets flagged for human confirmation, not a guaranteed dedup; exact matching rules are left to the builder.
- The user will name which client the batch is for at the start of each run. A batch is assumed single-client; multi-client batches are handled per the Edge cases entry above (flagged, not auto-split) rather than the skill inferring client assignment from receipt content.
