# Spec: Employee Expense Report Builder

## Purpose

Lets an individual employee turn their loose collection of receipts, card-statement lines, and informal notes into a correctly categorized, correctly totaled expense report in the company's existing reimbursement template — ready for the employee to review and submit themselves. The underlying need: the person who processes these reports today (finance/ops) loses significant time chasing missing receipts and re-checking other people's math; this skill exists to catch those problems *before* a report reaches them, not to replace their review.

## Trigger conditions

**Should fire** when someone is trying to assemble their own expense report from raw materials, e.g.:
- "Help me put together my expense report for the Chicago trip"
- "Can you organize these receipts into an expense report"
- "Turn these receipts and my card statement into something I can submit for reimbursement"
- "I need to file an expense report for last month"

**Should NOT fire** on requests that only sound adjacent:
- A factual policy lookup with no report being built — "What's our travel policy?" / "What's the meal per diem?"
- A request to reconcile or audit *multiple employees'* expenses at once (team-wide/month-end reconciliation) — this is explicitly out of scope; see Non-goals.
- A request to approve, reject, or make a judgment call on someone else's already-submitted report — that's a finance/manager decision, not this skill's job.
- A general bookkeeping/accounting request unrelated to an individual's own reimbursement (e.g., categorizing business revenue, tax prep).

## Inputs

What a person has on hand when invoking this, in any combination:
- Receipt photos or PDFs (phone camera captures, forwarded email receipts).
- A corporate card statement/CSV export from the bank portal, when the card was used.
- Informal notes about what a charge was for — anything from a full sentence to nothing at all.

Expected variation:
- Receipts range from clear and typed to blurry, cropped, or handwritten.
- Amounts may be in a foreign currency (when the employee traveled internationally).
- A single receipt may mix a business expense with a personal item bought at the same time/place.
- The same real-world charge may appear in more than one input source at once — e.g., a corporate-card meal that was also photographed as a paper receipt. This is common enough to plan for, not an edge case to dismiss.
- Business-purpose context may or may not be provided per item; when it is, it ranges from specific ("dinner with Acme Corp re: Q3 renewal") to vague ("meal").

## Outputs

A filled-in version of the company's existing Google Sheet expense template, with these columns, populated per line item:

| Date | Vendor | Category | Amount | Business Purpose | Receipt Attached (Y/N) |

Categories are fixed to the company's existing set: **Travel, Meals, Lodging, Office Supplies, Client Entertainment, Other.** This skill does not invent new categories.

Beyond the raw table, "done" includes:
- A running total, and a subtotal per category.
- A clearly separated **flags section** (not buried inline in the table) listing anything that needs the employee's attention before they submit: missing receipts, illegible receipts, over-policy-limit items, personal/business splits, and resolved or ambiguous duplicate charges (see Edge cases).
- **Business Purpose quality bar:** a good entry names what the expense was, who was involved (if relevant), and why it was a business expense — specific enough that finance wouldn't need to ask a follow-up question (the "dinner with Acme Corp re: Q3 renewal" standard). A vague entry ("meal", "supplies") should either be sharpened using whatever context is available (date, vendor, location, any note the employee gave) or, if there isn't enough context to make it specific, flagged back to the employee to supply more detail rather than left vague or invented.
- Optionally, a short draft email/message to finance summarizing the report, for the employee to send themselves — never sent automatically (see Scope & boundaries).

This is a fixed-structure output (the template columns and categories are not negotiable) with one genuinely subjective dimension — the quality/specificity of Business Purpose text — which is scored qualitatively rather than checked as pass/fail.

## Scope & boundaries

**Handles:**
- One individual employee's own expenses, for one reporting period/trip at a time.
- Populating the existing Sheet template from receipts, card CSV lines, and informal notes.
- Categorizing each line item into the fixed category list.
- Computing totals and per-category subtotals.
- Applying the stated policy rules and flagging violations (see Edge cases) — flagging, not adjudicating exceptions.
- Detecting and resolving duplicate charges that appear across more than one input source.
- Drafting (not sending) an optional summary message to finance.

**Stops / hands off when:**
- A receipt is missing or illegible — hands back to the employee to supply it, rather than guessing.
- A flagged policy violation needs a judgment call (e.g., is this over-limit meal actually justified?) — flags it for a human (the employee's manager or finance), never decides it itself.
- Business Purpose context is too thin to make specific even with available context — hands back to the employee for more detail rather than inventing a plausible-sounding reason.
- The report is complete and flagged — the skill's job ends there; it never submits, sends, or transmits the report to any system or person on its own.

## Non-goals

- **Not** a bulk/team-wide reconciliation tool — it does not process or cross-check multiple employees' expenses against each other or against a company card program at once. That is a distinctly different job from an individual preparing their own report, and was explicitly ruled out as a fork during scoping.
- **Not** an approval or audit tool — it never approves, rejects, or overrides a policy flag; those decisions belong to a human.
- **Not** a submission/integration tool — it does not connect to or push data into any finance system, accounting software, or the Sheet itself (it produces content ready to paste in, not a live write).
- **Not** a general bookkeeping, tax-prep, or company-wide accounting assistant.
- **Not** a policy-lookup tool — answering "what's the travel policy" with no report being assembled is out of scope for this skill (see Trigger conditions).

## Edge cases

| Situation | Expected behavior |
|---|---|
| Receipt is missing entirely | Include the line item if enough info exists to identify it (from a card CSV line or a note); flag "Receipt Attached: N" and call it out in the flags section as needing follow-up. Never invent an amount. |
| Receipt is present but blurry/illegible | Flag it explicitly as unreadable rather than guessing at the amount or vendor; ask the employee to confirm the value instead of transcribing a best guess. |
| Amount is in a foreign currency | Convert using that day's exchange rate where it can be determined; note in the line item both the original amount/currency and that it was converted, plus the rate/date used. If no rate can be determined, flag it rather than guessing a conversion. |
| A receipt mixes a personal item with a business item | Include only the business-expense portion in the amount and category; note in the flags section what was excluded and why, so the employee can see the split. |
| An expense exceeds a policy limit (e.g., a $150 dinner against the $75/day meal cap, alcohol over the $100 Client Entertainment cap) | Include the line item at its real amount — never silently cap or reduce it — and flag it clearly in the flags section as over-limit, naming which rule it exceeds. |
| The same real-world charge appears in more than one input source (e.g., photographed receipt *and* a line on the card CSV) | Match candidates on date + amount + vendor. When a confident match is found, list it once: use the card CSV as the source of truth for the amount, and attach the photographed receipt as the supporting proof. When a match is only plausible, not confident (e.g., same amount and date but a different or missing vendor name), do not silently merge — flag it as a possible duplicate for the employee to confirm. |
| Business Purpose has little or no context | Try to sharpen it using available context (date, vendor, location, any note given). If that's not enough to be specific, flag it back to the employee for more detail rather than writing something vague or inventing a plausible-sounding purpose. |
| Category is genuinely ambiguous (item doesn't cleanly fit Travel/Meals/Lodging/Office Supplies/Client Entertainment) | Place it in "Other" and note briefly why, rather than forcing it into a mismatched category. |

## Open assumptions

- **Currency-rate lookup capability is assumed available.** The spec assumes the skill has some way to determine a historical daily exchange rate (e.g., a lookup tool). If no such capability exists in the eventual build environment, the foreign-currency edge case should degrade to "flag for manual conversion" rather than silently failing — this wasn't explicitly confirmed with the user and should be checked before building.
- **No direct write access to the Google Sheet is assumed.** The output is assumed to be content the employee copies/pastes or that gets attached, not a live API write into the actual company Sheet — the user did not confirm whether such an integration exists or is wanted, so this is treated as out of scope by default per the Non-goals above.
- **Single employee, single reporting period per run.** The spec assumes each invocation covers one person's one trip/period, matching how the trigger conditions are phrased; it does not assume the same person running it repeatedly across periods needs cross-run memory of past reports (e.g., to catch a duplicate submitted last month) — that would be a reasonable future extension but wasn't asked about, so it's left out.
- **The fixed category list and template columns are assumed stable** (Travel, Meals, Lodging, Office Supplies, Client Entertainment, Other; Date/Vendor/Category/Amount/Business Purpose/Receipt Attached). If the company's template or policy numbers change, the spec's specifics would need updating, but the shape of the skill (categorize, total, flag) would not.
