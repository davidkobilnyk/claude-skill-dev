# Transcript — Expense Report Skill Spec (no skill loaded, default behavior)

**User:**
I have an idea for a skill around "expense reports" but haven't thought it through much. Can you spec it out for me?

---

**Claude:**
Happy to help spec this out. "Expense reports" could mean a few pretty different things depending on what's actually annoying you, so let me ask a handful of quick questions before I draft anything:

1. **Who's this for** — just you personally, or something meant for a team/company to use?
2. **What are the inputs?** E.g., a pile of receipt photos/PDFs, a bank or credit card statement export, both?
3. **What's the output supposed to be** — a filled-out company template (Excel/PDF), a submission into a system like Expensify/Concur/SAP, or just a clean summary for your own records?
4. **How often would you run this** — per trip, monthly, ad hoc?
5. **Any policy rules that need to be enforced** (spending caps, required receipts above a certain amount, disallowed categories), or is this purely "organize and total what I spent"?

Even rough/guessed answers are fine — I can note assumptions and refine later.

---

**User:**
Good questions, let me think...

It's just for me personally — I travel for work a few times a month and right now I build my expense report by hand, which is a pain. I usually end up with a folder of receipt photos from my phone plus some PDF receipts from email, and I also have my card statement I can export as a CSV. My company doesn't use one of those fancy systems like Concur — we just have a shared Excel template with fixed columns (Date, Vendor, Category, Amount, Business Purpose, Payment Method) and a dropdown list of allowed categories. I'd want the skill to fill that template out for me, plus maybe give me a quick summary so I can sanity-check totals before I submit it over email.

I'd run it maybe once a month, or right after a trip. As for policy — I don't have a formal written policy handy, but I know informally there's a per-meal cap and you're supposed to have a receipt for anything over some small amount. I don't want the skill to just guess and auto-approve stuff though — I'd rather it flag anything it's not sure about and let me decide.

---

**Claude:**
That's a solid picture. A couple more things before I lock in the draft:

1. Should the skill try to **match your receipts against your card statement** (to catch things you forgot to photograph, or receipts with no matching charge — cash tips, etc.), or just process the receipts on their own?
2. Any **foreign currency** trips, or is everything in USD?
3. If it hits something it can't confidently OCR or categorize (crumpled receipt, ambiguous vendor), what should happen — dump it in an "exceptions" pile for you to fill in by hand, rather than guessing?

---

**User:**
Yes — matching against the statement would actually be really valuable, that's the part I always mess up (forgetting a receipt, or not noticing a charge I never got a receipt for). Occasionally I do have foreign trips, so it should handle that if it can, though most months it's all USD. And yes, exceptions pile for anything it's not confident about — I'd much rather manually fix a handful of flagged items than have it silently put something in the wrong category or miss a mismatch.

---

**Claude:**
Great, that's enough to draft a real spec. Here's what I put together — I wrote it as a standalone document (`expense-report-skill-spec.md`) rather than just pasting it inline, since it's the kind of thing you'll want to revise and hand off later.

**Summary of what's in it:**

- **Problem & motivation** — replacing your manual receipt-hunting + Excel entry with an automated first pass.
- **Inputs**: receipt photos/PDFs (unsorted), a bank CSV export, your company's fixed .xlsx template, and optional free-text trip context (dates, client).
- **Outputs**: the filled .xlsx template matching your existing columns/categories exactly, plus a short summary (totals by category/day) and an explicit **exceptions list** — missing receipts, unmatched charges, amount mismatches, possible policy issues.
- **Core workflow**: ingest receipts → parse the statement → match receipt-to-charge by amount/date/vendor → categorize into your fixed dropdown values → fill the template → summarize and flag → you do a final human review before submitting.
- **Policy rules**: I stubbed in placeholders (per-meal cap ~$75, receipt-required threshold ~$25) since you don't have a written policy doc — flagged clearly as guesses to confirm, not hardcode blindly.
- **Edge cases** I called out: OCR reliability on messy receipts, foreign currency reconciliation, split/shared expenses, multiple cards, duplicate receipts, and what happens if the company template's columns ever change (should fail loudly, not silently mis-map).
- **Definition of done**: minimal re-keying of anything clearly matchable, and zero *false-confident* errors — a flagged item is fine, a wrong-but-confident entry is not.
- **Explicitly out of scope for v1**: no auto-submission anywhere (you're on plain Excel, not an API-backed system), no multi-user/approval workflow, no learning/adaptive categorization yet.
- **Next steps**: confirm the real per-meal cap and receipt threshold, get an actual sample of the .xlsx template and a sample CSV to nail down exact headers before building, and decide on OCR approach once you have real (messy) receipt samples to test against.

That's a full first-draft spec, not a working skill yet — no SKILL.md, no code. If you want, the natural next step would be turning this into an actual buildable skill (instructions + maybe a helper script for the CSV/xlsx handling) once you've got a real template file and CSV sample to test against. Let me know if you want to go that direction, or if anything in the spec above should change first.

---

*Deliverable produced this session:* `expense-report-skill-spec.md`
