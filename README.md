# Client Work Starter for Claude Code

[![Repository checks](https://github.com/AiBJohnson/scale-systems-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/AiBJohnson/scale-systems-skills/actions/workflows/validate.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-2dd4bf.svg)](LICENSE)
[![Gumroad download](https://img.shields.io/badge/Gumroad-pay%20what%20you%20want-f0b429.svg)](https://aibjohnson.gumroad.com/l/claude-code-starter-skills?utm_source=github&utm_medium=repository&utm_campaign=client_work_v1)

Eight Claude Code skills for freelance web designers and website consultants already using Claude Code.

Start with one client call: turn rough notes into decisions, action owners, and questions you still need to resolve. Then try invoice-follow-up drafts or saved-message triage if those tasks fit your work. You provide the source information, review the result, and decide what to share.

The public repository is free and MIT-licensed. The eight complete skills are editable instruction files, not a client portal, CRM, payment service, or autonomous business. Claude Code access is separate. There is no proven superiority over a plain prompt or another free resource; use the examples to decide whether the structure helps your own work.

## Try one client call first

Follow the [client-work quickstart](plugins/solopreneur-starter/CLIENT-WORK-QUICKSTART.md). It pairs [fictional Birchlight call notes](plugins/solopreneur-starter/examples/client-work/client-call-notes.md) with an [editor-prepared expected example](plugins/solopreneur-starter/examples/client-work/client-call-EXPECTED.md), not a saved model response.

After marketplace installation below, use:

```text
/solopreneur-starter:meeting-notes
Read only plugins/solopreneur-starter/examples/client-work/client-call-notes.md.
Return the draft in chat. Separate decisions, actions, unresolved questions,
and promises. Preserve unknown owners and dates. Do not send or create tasks.
```

This relative path assumes Claude Code is open in the repository root. From a separate disposable project, supply the exact absolute path to the same synthetic file. For downloaded-folder installation, use `/meeting-notes` without the marketplace prefix.

The expected check is **two decisions, four actions, one unassigned action, and four open questions**. Domain ownership has no assigned action owner. “Late September” is discussion, not an agreed launch date. The sample demonstrates a review target; it does not establish that a model or real customer task passed.

No inbox, calendar, or account connection is needed. Test synthetic data first, then a sanitized copy of one task you are permitted to share with your configured model service.

## What is included

| Skill | Purpose | Important boundary |
| --- | --- | --- |
| `weekly-numbers` | Compare two seven-day sales periods | Reports the columns and reporting dates before calculating |
| `inbox-triage` | Classify saved messages and draft replies | Never sends or connects to a mailbox |
| `invoice-chase` | Find overdue invoices and draft chasers | Uses an explicit as-of date and never sends |
| `expense-categorise` | Map transactions to your categories | Does not invent categories or guess ambiguous items |
| `meeting-notes` | Extract decisions, actions and open questions | Does not invent owners or deadlines |
| `content-repurpose` | Adapt one source into five native formats | Does not add unsupported claims |
| `decision-brief` | Compare options and challenge a preferred choice | Marks unknown costs instead of inventing them |
| `file-organiser` | Preview and apply rule-based file moves | Requires approval and never deletes or overwrites |

## Install from the marketplace

In Claude Code, run:

```text
/plugin marketplace add AiBJohnson/scale-systems-skills
/plugin install solopreneur-starter@scale-systems
```

Run `/reload-plugins` after installing so the current session discovers the plugin. Marketplace installs use namespaced commands:

```text
/solopreneur-starter:weekly-numbers
/solopreneur-starter:inbox-triage
/solopreneur-starter:invoice-chase
```

Run `/plugin list` if you need to confirm that `solopreneur-starter@scale-systems` is enabled.

## Downloaded-folder alternative: preview before applying

The optional installer needs Python 3.9+ on macOS, Linux, or WSL; native Windows is not supported by its symlink-safe copy mechanism. The marketplace route above does not require this installer.

In a terminal, enter the plugin directory. Replace the example project path with an **existing** disposable project folder:

```sh
cd plugins/solopreneur-starter
python3 install_skills.py --project "/absolute/path/to/client-sandbox"
```

This default dry run lists the exact eight target folders and writes nothing. Inspect the path list, then explicitly apply:

```sh
python3 install_skills.py --project "/absolute/path/to/client-sandbox" --apply
```

Only the eight skill folders are copied into that project's `.claude/skills/`. The installer refuses all existing skill paths, symlinks, and unexpected source contents; it never merges, overwrites, copies context/examples, or changes settings. Keep the exact path list for recovery. An I/O error can leave new partial folders; [troubleshooting](plugins/solopreneur-starter/TROUBLESHOOTING.md) explains how to inspect and recover only those specific additions.

Use `--user` instead of `--project ...` only for deliberate user-wide installation in `~/.claude/skills/`. Advanced users can select `--destination "/absolute/custom/skills"` when its parent exists; arbitrary directories are not automatically discovered. See [INSTALL.txt](plugins/solopreneur-starter/INSTALL.txt) for the exact scope, optional context, upgrade, and removal steps.

Standalone skills normally live-reload under an already existing top-level skills directory. Open Claude Code in the intended project and type `/`; restart the session if the names are missing, especially when the skills directory was created during that session. Downloaded-folder commands are normally unnamespaced, such as `/meeting-notes`.

Do not keep marketplace and downloaded copies of the same eight, or competing project/user copies, installed together. The installer checks only the selected destination, not all discovery scopes. Inspect and preserve existing custom edits before moving any known prior copy outside skill discovery.

## Synthetic test inputs

The files under `plugins/solopreneur-starter/examples/` contain invented names, masked example addresses and synthetic transactions. They are not real customer records. Each skill has a fixed input or explicit fixture mode:

| Skill | Input | Fixed test instruction |
| --- | --- | --- |
| `weekly-numbers` | `sample-sales.csv` | End the reporting period on 2026-08-31 |
| `invoice-chase` | `sample-invoices.csv` | Use 2026-09-04 as the as-of date |
| `expense-categorise` | `sample-expenses.csv` | Verify that it requests a category list rather than inventing one |
| `inbox-triage` | `inbox/` | Use only the four saved messages; do not connect to a mailbox |
| `content-repurpose` | `content-repurpose/source-article.md` | Create local drafts only; add no facts absent from the source |
| `meeting-notes` | `meeting-notes/raw-notes.md` | Preserve unresolved owners, dates and questions |
| `decision-brief` | `decision-brief/decision-context.md` | Recommend without buying or changing an account |
| `file-organiser` | `file-organiser/preview-request.md` | Manifest-only preview; do not perform any filesystem move |

For a reproducible `weekly-numbers` test, point the skill at `sample-sales.csv` and set the reporting-period end date to **2026-08-31**. It should begin with the real schema and state the date windows:

```text
Reading sample-sales.csv.
Columns: order_id, date, product, price, currency, refunded, customer_email, country.
Current period: 2026-08-25 through 2026-08-31.
Comparison period: 2026-08-18 through 2026-08-24.
Excluding rows where refunded = true from revenue and order calculations.
```

For `invoice-chase`, use **2026-09-04** as the as-of date. Do not use the computer's current date for either fixture. Deterministic calculation checks and expected model-behavior invariants are documented separately in [`examples/EXPECTED_OUTPUTS.md`](plugins/solopreneur-starter/examples/EXPECTED_OUTPUTS.md).

When testing a marketplace install, use the namespaced commands:

```text
/solopreneur-starter:weekly-numbers
/solopreneur-starter:invoice-chase
/solopreneur-starter:expense-categorise
/solopreneur-starter:inbox-triage
/solopreneur-starter:meeting-notes
/solopreneur-starter:content-repurpose
/solopreneur-starter:decision-brief
/solopreneur-starter:file-organiser
```

## Working files and privacy

Keep live exports and generated drafts outside this public clone whenever practical. Pass the skill an explicit input path rather than copying customer files into `examples/`.

If you work inside a Git project, the skills default generated files to a unique run directory under:

```text
.scale-systems-local/runs/<skill>/<YYYYMMDD-HHMMSSZ>/
```

This repository ignores `.scale-systems-local/`, but your own project will only ignore it if its `.gitignore` also contains that entry. Every file-writing skill must state its planned output path first, create a new run directory and refuse to overwrite an existing file. `file-organiser` is the exception only in destination: it can move the files you explicitly approve, while recording a collision-safe log under the local run directory.

For optional context, inspect [`context/CLAUDE.md`](plugins/solopreneur-starter/context/CLAUDE.md) and [`context/voice.md`](plugins/solopreneur-starter/context/voice.md). Use an editor to create an absent destination or carefully merge selected non-sensitive facts into an existing one; never replace your project's `CLAUDE.md` or voice guide with an example. [`examples/voice.example.md`](plugins/solopreneur-starter/examples/voice.example.md) is another fictional reference, not a real customer voice.

Local source files may be sent to the model or service configured in Claude Code. “Local files” does not mean “never leaves your computer.” Check your environment's data settings and client permissions; do not commit private business or customer information.

Never put credentials, access tokens, private mailbox exports, unredacted customer data or payment data in this repository. See [`SECURITY.md`](SECURITY.md) for the complete data and tool boundary.

## The injection test

`examples/inbox/04-injection-test.txt` contains instructions embedded in a fictional email. It is intentionally hostile test data.

`inbox-triage` must treat that content as data, flag it as suspicious and refuse to follow it. The fixture does not prove that every model or host configuration is safe; it is a regression check for the skill's written instruction boundary. Test with synthetic data before considering real inbox exports.

## What the automated checks prove

`python3 scripts/validate_repo.py` deterministically checks manifest consistency, the eight expected skill files, fixed fixture presence, CSV schemas, sample arithmetic, client-work example facts, and required written safety boundaries. It also checks installer preview/conflict/application behavior in a disposable temporary project; it does not use your real `~/.claude` directory. `claude plugin validate ... --strict` checks the plugin and marketplace manifest structure.

Neither check invokes a model, runs a skill conversation, exercises host tools or proves end-to-end behavior. The qualitative sections of `EXPECTED_OUTPUTS.md` are acceptance criteria for a separate manual or model evaluation; they are not claims that such an evaluation passed.

## Shared rules

1. **Say what is missing.** The skills flag gaps instead of filling them with plausible details.
2. **Use reproducible dates.** Date-sensitive work states its as-of date or reporting window.
3. **Keep inputs read-only.** Generated files go to a unique local run directory and never replace a source file.
4. **Preview consequential file moves.** `file-organiser` shows the full plan and waits for approval.
5. **Draft, never send.** These skills do not post, email, purchase or move money.

These are behavioral instructions, not a technical sandbox. The plugin ships no hooks, MCP servers, mail integration or runtime dependencies, but Claude Code may have tools and connectors enabled by the user. The skills instruct Claude not to use those capabilities for sending, publishing or moving money.

## Requirements and maintenance

You need your own Claude Code access; any applicable account or model-service cost is separate. The marketplace skill runtime consists of JSON manifests, Markdown instructions, and synthetic text/CSV fixtures, with no build step or runtime dependency. The optional installer and maintainer validation script use standard-library Python; the installer requires Python 3.9+ on macOS, Linux, or WSL. Neither runs automatically when a skill is used.

Update or remove a marketplace installation with:

```text
/plugin update solopreneur-starter@scale-systems
/plugin uninstall solopreneur-starter@scale-systems
```

After an update, run `/reload-plugins` to load the updated marketplace plugin in the current session.

For troubleshooting, include the Claude Code version, installation method, exact command name, sanitized input schema and observed output. Do not attach live customer data or secrets. Open a [bug report](https://github.com/AiBJohnson/scale-systems-skills/issues/new/choose) or read [`CONTRIBUTING.md`](CONTRIBUTING.md).

## The paid collection

The paid collection contains 18 skills total: these eight starter skills plus ten additional workflows covering client onboarding, SOP writing, a structured weekly review, offer audits, price-change drafts, launch kits, refund analysis, testimonial permission drafts, one-time competitor comparison, and read-only backup screening. It includes eighteen guided walkthroughs and additional examples; it is still instructions and review aids, not hosted automation. Details are on [Gumroad](https://aibjohnson.gumroad.com/l/solopreneur-skills-pack?utm_source=github&utm_medium=repository&utm_campaign=client_work_v1).

The public eight are complete skills, not shortened demos. This repository cannot verify the current contents of a separately delivered purchase; consult that product's listing and included license before relying on its counts or reuse terms.

## License

The public repository, including all eight files under `plugins/solopreneur-starter/skills/`, is MIT-licensed. You may use, modify, redistribute and sell copies subject to the notice requirement in [`LICENSE`](LICENSE). [`LICENSES.md`](LICENSES.md) explains the repository boundary and why a separately delivered paid package may have different terms.
