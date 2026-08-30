# Transcript — Expense Report Skill Spec (no skill loaded, default behavior)

**User:** I have an idea for a skill around 'expense reports' but haven't thought it through much. Can you spec it out for me?

---

**Claude:**

Happy to help spec this out — but "expense reports" could mean a lot of different things depending on who's using it and what's painful about the current process. Before I draft anything, a few questions:

1. **Who's this for, and in what context?** Are you filing expenses for yourself (freelancer/consultant reimbursement), for a team (approving other people's expenses), or something else (e.g., tracking spend for budgeting, not reimbursement)?
2. **What's the input?** Receipt photos/scans, a bank or credit card CSV export, a phone expense-tracking app export, or just you typing things out as you go?
3. **What's the desired output?** A spreadsheet, a PDF, a specific template a client/employer requires, or something that feeds into another tool (QuickBooks, Concur, Expensify, etc.)?
4. **What's actually annoying about doing this today?** Manual categorization, chasing missing receipts, currency conversion, formatting per recipient, something else?
5. **Any policy rules that matter** — spending limits, non-reimbursable categories, mileage, per diem — or is this pretty freeform?

Rough answers are totally fine — I just want to make sure the spec matches a real workflow instead of a generic one.

---

**User:** Fair questions. I'm an independent consultant — I work with a few different clients and bill them for reimbursable expenses (travel, meals, that kind of thing) separately from my actual invoices. Right now I take photos of receipts on my phone throughout the month and then at the end of the month I sit down and manually build a spreadsheet — grouping by category, adding it up, formatting it so it looks reasonable to send to whichever client it's for. It's tedious and I sometimes lose track of a receipt or double-count something. I don't use any expense software, it's all manual. Output-wise, clients mostly just want something in Excel they can look at — no fancy integration needed. Sometimes I travel abroad so there's occasional foreign currency stuff too.

---

**Claude:**

That's a clear enough picture to spec against — thanks. A couple more things before I write it up, both fairly quick:

1. **Receipt input:** do you want the skill to actually read the receipt photos (OCR) and pull out vendor/amount/date itself, or would you rather hand it a list you've already transcribed (or a CSV from a tracking app), with photos just kept as backup? OCR is doable but not perfect, so I want to know how much you're trusting it to get right unsupervised.
2. **Anything it should flag automatically** — e.g., a receipt over some dollar amount that's missing, a possible duplicate entry, an item that looks non-reimbursable (like alcohol) — or should it just format whatever you give it without judgment calls?
3. **Currency conversion** — should it look up a live exchange rate, or would you rather supply/confirm the rate yourself so there's no ambiguity about what number ended up on the client's report?

---

**User:** Good questions.

1. Honestly, let it try OCR on the photos since that saves me the most time, but I don't fully trust it — so if it's not confident about a read, I want it to ask me rather than just put a number down. And I'll sometimes just type stuff in directly too ("Uber $42 on the 12th") for things I don't have a photo of yet.
2. Yes please, flag stuff — missing receipts over like $25, possible duplicates, anything that looks like it might not be reimbursable (I'll make the final call, just don't want to miss something). Don't want it silently fixing or dropping anything though.
3. I'd rather confirm the rate myself or have it clearly state what rate it used — I don't want a client questioning a number and me not knowing where it came from.

One more thing since you asked what's annoying: it'd be great if it broke out a per-day total for trips, since some clients want to see the day-by-day for travel specifically. And output filename should probably include the client name and month so I can find things later.

---

**Claude:**

Got it — that's enough to write a solid v1 spec. Here's the plan:

- **Inputs:** receipt photos (OCR'd, with low-confidence reads sent back to you), CSV exports, and freeform typed entries — all mixed together in one batch.
- **Processing:** auto-categorize (Travel, Lodging, Meals & Entertainment, Software/Subscriptions, Office Supplies, Other), validate (missing receipt >$25, possible duplicates, non-reimbursable-looking items, low-confidence OCR) — all surfaced to you, nothing auto-corrected or dropped silently.
- **Output:** an .xlsx report grouped by category with subtotals + grand total, a per-day breakdown for multi-day trips, filename pattern `[Client]_Expenses_[Month][Year].xlsx`. PDF summary available on request.
- **Currency:** original amount/currency shown alongside a converted USD amount, using a rate you supply or confirm — always stated on the report, never silently sourced.
- **Explicitly out of scope for v1:** no accounting-software integration, no approval workflow (you're both filer and reviewer), no automated FX lookup, no mileage calculator — noted as possible v2 additions.

I've written this up as a full spec document: `expense-report-skill-spec.md`. It covers the problem statement, target user, trigger conditions, inputs/outputs, the step-by-step workflow, validation rules, the category taxonomy, what's explicitly out of scope for v1, and a few open questions for when you're ready to extend it (per-client templates, mileage, recurring-subscription detection, live FX rates).

Take a look and let me know what's off before this becomes an actual build — particularly whether the validation thresholds ($25 receipt cutoff, the category list) match what your clients actually expect, since that varies client to client.

---

**User:** This looks like a solid starting point, thanks. I'll review the details and get back to you if anything needs adjusting.

---

**Claude:**

Sounds good — the spec is saved and ready whenever you want to move to building it out. A few things worth flagging for when you do:

- The $25 receipt-flagging threshold and the six-category taxonomy are reasonable defaults, but double-check them against what each client's finance team actually expects, since that's the part most likely to need per-client tweaking.
- If OCR accuracy turns out to be worse than expected in practice, the "ask when not confident" fallback is the safety net — worth watching whether that ends up asking too often (annoying) or too rarely (risky) once you're using it for real.
- When you're ready to turn this spec into an actual working skill, that's a good next step to take on separately — happy to help with that whenever you want.
