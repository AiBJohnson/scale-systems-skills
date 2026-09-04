---
name: invoice-chase
description: Find unpaid or overdue invoices in an export and draft polite chaser emails for each. Drafts only, never sends. Use when the user mentions chasing invoices, late payments, or money owed.
user-invocable: true
---

# Invoice chase

Most late invoices are not refusals. They are people who forgot. Write accordingly.

## Steps

1. Read the invoice export. Report the columns you found before proceeding.
2. Identify unpaid invoices and calculate days overdue against today's date.
3. Group into three buckets: **1-14 days**, **15-30 days**, **30+ days**.
4. Draft one email per invoice, with tone matched to the bucket:
   - **1-14 days:** assume it was missed. Friendly, short, no pressure.
   - **15-30 days:** direct, restate the amount and due date, ask for a payment date.
   - **30+ days:** firm and specific. State the amount, the age, and what happens next. Still not rude.
5. Write each draft to a separate file in `drafts/` named by invoice number.

## Rules

- **Never send anything.** Drafts only. Do not connect to email even if a connector is available.
- Include the exact invoice number, amount and due date in every draft. A chaser without specifics gets ignored.
- Never invent a late fee, a threat, or a legal consequence that the user has not told you exists.
- Flag any invoice where the data looks wrong (negative amount, future date, missing client) instead of drafting for it.

## Verify

Print a table of what you drafted: invoice, client, amount, days overdue, bucket. Total the outstanding amount so the user sees what is at stake.
