---
name: expense-categorise
description: Read a bank or card statement export and sort every transaction into the user's accounting categories, flagging anything ambiguous rather than guessing. Use for bookkeeping, tax prep, or expense review.
user-invocable: true
---

# Expense categorise

## Before starting

Ask for the category list. If the user does not have one, ask for their accountant's categories — **do not invent a chart of accounts.** Wrong categories are worse than uncategorised transactions, because they look finished.

## Steps

1. Read the export and report its columns.
2. Categorise each transaction.
3. Put anything you are not confident about into a **Needs review** group. Err heavily toward this group.
4. Output a spreadsheet-ready CSV plus a summary of totals per category.
5. Separately list every recurring charge found, with its annual cost, sorted highest first. This is usually the most valuable part of the output.

## Rules

- **Never invent a category the user did not give you.**
- Never guess at a personal-versus-business split. Flag it.
- Flag anything that looks like a duplicate charge, along with both dates.
- State the total of the Needs review group so the user knows how much is unresolved.

## Verify

Report: transactions read, categorised, needing review, and whether the sum of all categories equals the statement total. If it does not balance, say so prominently — that means something was missed.
