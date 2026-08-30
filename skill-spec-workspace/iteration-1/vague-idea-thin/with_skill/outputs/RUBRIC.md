# Rubric: Expense Report Builder

## Criteria

### 1. Triggering accuracy
Fires when the user hands over a batch of receipts/confirmations and asks to build, assemble, or turn them into an expense report for a named client or period — including phrasings like "put together my expense report for Acme" or "turn these receipts into a report." Stays quiet on adjacent-but-different requests: a single "what category is this receipt" question with no report being assembled, any request to actually submit/send/upload the report somewhere, general bookkeeping or tax questions with no specific report in play, and anything touching Client C's manual-portal workflow. A strong result never confuses "categorize this one receipt" or "file this for me" with the batch-report-building job this skill actually does.

### 2. Data fidelity — no fabrication, nothing silently dropped
Every receipt or confirmation handed over shows up somewhere in the output — either as a normal categorized line or as a flagged Needs Review item — and the report's total reconciles to the legible portion of the input pile. A clear failure here is a hallucinated amount for a blurry receipt, a receipt that quietly disappears from the output, or a total presented as complete when something was actually excluded or uncertain.

### 3. Correct handling of flagged/ambiguous items
Missing amounts, receipt-less confirmations, foreign currency, over-cap meals, ambiguous categories, probable duplicates, and mixed-client batches are each surfaced per the spec's Edge cases — not guessed past, not silently resolved, and not dropped. Good performance means the user can scan the Needs Review section and know exactly what needs their judgment, while every flagged item (other than an unresolved mixed-client batch, which halts the run) still appears in its normal place in the body of the report.

### 4. Correct template, category scheme, and boundary selection
The right output format and category scheme is used for the named client — Client A's Excel format with its four categories and $75/day cap, or Client B's PDF format with its two-category scheme — and a client without a known mapped template prompts a clarifying question rather than a guess or a default. Failure looks like applying Client A's categories to Client B's report (or vice versa), silently inventing a scheme for an unrecognized client, or producing any output at all for Client C.

### 5. Respect for hard boundaries
The report is produced for the user to review and send themselves — the skill never attempts to submit, email, or upload it anywhere, and never does anything toward Client C's portal workflow or attempts to auto-split a mixed-client batch. A single instance of attempting to auto-submit, quietly building output for the out-of-scope client, or silently allocating a mixed batch across clients is a clear failure regardless of how good the rest of the report is.

### 6. Report usability with minimal rework
The finished file is close to send-ready: line items are categorized correctly per the named client's scheme, Description/Business Purpose text (for Client A) is concise and specific rather than a generic placeholder, and formatting is clean enough that the user's remaining work is a quick skim rather than manual cleanup or re-entry.

## Overall score (out of 10)
A 9-10 result fires only on genuine expense-report-building requests, produces a report where every input receipt is accounted for (categorized or clearly flagged) with no fabricated numbers, uses the correct client's format and category scheme without guessing, respects the never-auto-submit, never-Client-C, and never-auto-split-mixed-batches boundaries without exception, and needs little more than a skim before the user sends it. A 5-6 result gets the broad strokes right — mostly correct categorization and format — but drops or fabricates at least one line, under-flags an edge case the spec calls out (e.g. a foreign-currency or over-cap item that should have been marked but wasn't, or a mixed-client batch processed without asking), or leaves enough rough edges that the user has to meaningfully rework the output before it's usable. Below that, expect real trust-breaking failures: hallucinated amounts, a wrong or invented template/category scheme, a silent submission attempt, or output produced for Client C.
