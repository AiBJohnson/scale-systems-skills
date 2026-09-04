---
name: file-organiser
description: Sort a messy folder into a structure the user defines, renaming by rule. Always previews before touching anything. Use for downloads, client deliverables, invoices or receipts.
user-invocable: true
---

# File organiser

## The rule that matters most

**Preview first, always.** Print exactly what would move and where, and stop. Do not move a single file until the user has approved the preview. This is not optional, and it is not skipped because the folder "looks simple".

## Steps

1. Ask for the rules, or propose a set based on what is actually in the folder and get approval.
2. Read the folder and infer what each file is from its name, extension, and date.
3. **Print the full plan** as a table: current name, proposed name, destination.
4. Explicitly list anything you could not classify. Never move a file you had to guess about — leave it where it is.
5. Wait for approval.
6. On approval, move the files and write `organiser-log.md` recording every move, so it can be reversed.

## Rules

- **Never delete anything.** Ever. Not even things that look like duplicates — move them to `review/` instead.
- Never overwrite an existing file. Append a suffix and flag the collision.
- Preserve original creation dates in the log so nothing is lost if a rename was wrong.

## Verify

After the move, report: files moved, files skipped, collisions handled, and the log path.
