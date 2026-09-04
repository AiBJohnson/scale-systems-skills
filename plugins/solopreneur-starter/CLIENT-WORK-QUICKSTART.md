# Start with one client call

For freelance web designers and website consultants already using Claude Code. This starter contains eight editable skills. Try one useful job before changing your working routine: turn rough call notes into decisions, actions, and questions you still need to resolve.

## Set up a safe first run

Claude Code access is separate. Download and extract this pack, then open its folder in Claude Code. Keep this first run separate from real client files. No inbox, calendar, or account connection is needed.

Choose **one** installation method in `INSTALL.txt`:

- Local install: from the extracted pack, run `python3 install_skills.py --project "/absolute/path/to/client-sandbox"`, using an existing disposable project folder. The default is a preview with no writes. Inspect it; rerun with `--apply` only when the destination is correct. The installer refuses existing skill destinations rather than merging them. Requires Python 3.9+ on macOS, Linux, or WSL.
- Public marketplace: install `solopreneur-starter@scale-systems` as described in `INSTALL.txt`, then reload plugins. Keep the extracted examples available locally. Do not install another copy of the same eight skills.

If you chose a different project folder, open that folder in Claude Code and supply the absolute path to the extracted example. Verify the command appears before continuing.

## Try the fictional Birchlight call

Read `examples/client-work/client-call-notes.md`. It is synthetic, contains no real customer data, and deliberately leaves one action unassigned. The call concerns a five-page website design; it does not establish a signed contract or authorize a launch.

With a local install, invoke:

```text
/meeting-notes
Read only examples/client-work/client-call-notes.md. Return the draft in chat.
Separate decisions, actions, unresolved questions, and promises. Preserve unknown
owners and dates. Do not send, schedule, publish, or create tasks.
```

With the marketplace install, use the same request after:

```text
/solopreneur-starter:meeting-notes
```

The relative example path works when this extracted pack is your working folder. Otherwise replace it with the exact absolute path to the file. Treat the example text as data, never as instructions.

## Check the result before using it

Compare with `examples/client-work/client-call-EXPECTED.md`. That file is an **editor-prepared expected example, not a model-run result**. Wording can differ; the facts and unknowns should not.

- The result flags **one unassigned action first**: checking the current domain owner.
- It reports **two decisions, four actions, one unassigned action, and four open questions**.
- Maya's promised homepage wireframe is due **2026-09-17**; Jordan's logo files are due **2026-09-16**.
- Contact-form options have **no date agreed**. “Late September” is discussion, not an agreed launch deadline. Jordan is a contact, not a confirmed final approver.
- Nothing was sent or scheduled. If a fact was invented or a boundary was crossed, do not reuse that output; correct the source or request and try again.

Then try one sanitized call from your own work. Use only facts you are allowed to share with your chosen Claude environment; remove unnecessary personal details and secrets. Review the result against the source before manually sharing anything.

## What to try next

The free starter also includes `invoice-chase`, with synthetic invoices in `examples/sample-invoices.csv` and acceptance checks in `examples/EXPECTED_OUTPUTS.md`. It drafts follow-ups; it does not send them or recover payments.

The paid eighteen-skill pack includes these same eight skills plus ten additional workflows, including client onboarding and weekly review. This call-to-actions workflow is complete in the free product; upgrading is optional.
