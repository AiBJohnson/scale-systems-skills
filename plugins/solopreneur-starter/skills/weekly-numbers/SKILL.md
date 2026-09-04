---
name: weekly-numbers
description: Produce the Monday business summary from a sales export - revenue, orders, average order value, top products, and anything that moved sharply. Use when the user asks for their weekly numbers, a business summary, or "how did last week go".
user-invocable: true
---

# Weekly numbers

Produce a one-screen summary a solo operator can read in thirty seconds.

## Before you calculate anything

1. Ask which file to read, or look for a `.csv` export in the working folder.
2. **Read the file and report its actual columns before writing any code.** Do not assume column names. Exports differ between platforms and assuming is where this breaks.
3. If a refund or status column exists, exclude refunded rows from revenue and say that you did.

## Produce

- Revenue last 7 days, and the change against the previous 7 days as both a figure and a percentage
- Order count and average order value, same comparison
- Revenue by product, highest first
- **Exceptions only:** anything that moved more than 20% in either direction

## Rules

- If the file has fewer than two weeks of data, say so and give the single-period figures rather than inventing a comparison.
- Never estimate a number that is not in the data. If something cannot be computed, name it and say why.
- Keep the whole output under one screen. This is a scan, not a report.

## Verify

State the row count you read and the date range it covers, so the user can sanity-check that the export was complete before trusting the numbers.
