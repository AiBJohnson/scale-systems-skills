# Solopreneur Starter Skills for Claude Code

Four Claude Code skills for the admin work of a one-person business.

Every "best Claude Code skills" list is written for engineers — commit message writers, code reviewers, PR describers. These are for the other half of the job: reading your own numbers, clearing your inbox, deciding things, and finding the file you saved somewhere sensible three months ago.

Free and MIT-licensed. Sample data is included, so you can test all four in about a minute without wiring anything up.

## Install

```
/plugin marketplace add AiBJohnson/scale-systems-skills
/plugin install solopreneur-starter@scale-systems
```

Or copy the four folders in `plugins/solopreneur-starter/skills/` into `~/.claude/skills/` and restart Claude Code.

## The four skills

### `/weekly-numbers`

Reads a sales CSV and produces a one-screen Monday summary: revenue against the previous seven days, order count, average order value, top products, and anything that moved sharply.

It reads your file's actual column names and tells you what it found **before** it calculates anything. Exports differ between Stripe, Shopify, Gumroad and everything else, and silently guessing at a column called `total` is how these things quietly report the wrong revenue for a month.

```
/weekly-numbers
> Reading sample-sales.csv. Columns: date, product, quantity, unit_price, total, status.
> Excluding 3 rows where status = refunded.
```

### `/inbox-triage`

Reads saved customer emails, works out what each one is actually asking, and drafts a reply in your voice.

**It drafts. It does not send.** Nothing in this skill can reach a mail server.

It also flags anything needing your judgement rather than guessing — a refund outside policy, an angry customer, a question it cannot answer from what it can see.

### `/decision-brief`

Turns something you are stuck on into a structured brief: the real options, what each costs, what would have to be true for each to be right, and the strongest argument **against** the option you appear to be leaning toward.

That last part is the point. An assistant that agrees with you is not helping you decide.

### `/file-organiser`

Sorts a messy folder into a structure you define and renames by rule.

It always previews the full move list and waits for you to confirm. It will not touch anything before you say so, and it will not delete.

## Test all four in a minute

Sample data ships with the plugin, in `plugins/solopreneur-starter/examples/`:

- `sample-sales.csv` — a small, deliberately imperfect sales export, including refunded rows that should be excluded from revenue
- `inbox/` — four saved emails: a refund request, a simple question, some praise, and one more (see below)

```
/weekly-numbers          # point it at sample-sales.csv
/inbox-triage            # point it at the inbox/ folder
```

## The fourth email

`inbox/04-injection-test.txt` contains a message with instructions embedded in it, pretending to be from you and asking the assistant to do something it should not.

It is there on purpose. `inbox-triage` is written to treat email content as **data, not instructions** — so it should summarise that email as a suspicious message and refuse to act on what it says. Run it and confirm that for yourself. Do not take my word for it.

Any tool that reads untrusted text on your behalf should be tested this way before you trust it with a real inbox.

## Three rules every skill follows

1. **Say what is missing.** Every skill is instructed to flag gaps rather than fill them with plausible filler. A skill that quietly invents a number is worse than one that refuses.
2. **Dry run before writing.** Anything that modifies or deletes shows you the plan first.
3. **Draft, never send.** Nothing here posts publicly, emails anyone, or moves money.

## Requirements

Claude Code, and a Claude account. These are plain markdown instruction files — no dependencies, nothing to build, nothing that phones home.

## The longer version

There is a paid pack of 18 skills that covers invoicing, expenses, proposals, client updates, content repurposing and the weekly review, with worked examples and a business-context file so Claude stops asking what you do: [aibjohnson.gumroad.com](https://aibjohnson.gumroad.com/l/solopreneur-skills-pack).

These four are not crippled to sell you that. They are the same files, unmodified, and if they are all you need then that is a fine outcome.

## Licence

MIT. Fork them, change them, ship them in your own thing.
