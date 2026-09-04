# Security and data handling

## Supported version

Security and safety corrections target the latest version on the default branch. Older marketplace caches or manual copies may retain earlier instructions; update or replace them before retesting.

## What this plugin can and cannot enforce

The plugin contains Markdown instructions and synthetic text/CSV fixtures. It ships no hooks, MCP server, mail client, network integration, or automatic dependency installation. The optional Python installer only copies the eight skill directories after explicit `--apply`; it uses standard-library filesystem operations and never invokes a model or network service. That is an inspectable package property, not a guarantee about the Claude Code host.

Claude Code may have filesystem, shell, network, browser, email or other connectors enabled by the user. Skill instructions are a behavioral boundary, not a technical sandbox. Review the proposed action and active tools before using any assistant with sensitive data.

Local inputs can be sent to the model/service configured in Claude Code. Review data settings and client permissions rather than treating file-based work as automatically private or offline.

## Optional installer boundary

The installer requires an explicit project, user, or custom destination and defaults to a no-write preview. It refuses symlinks and existing skill paths, never merges or overwrites, and copies no context or examples. It supports Python 3.9+ on macOS, Linux, or WSL, not native Windows. It checks the selected target, not every plugin/discovery scope, and does not constitute an operating-system sandbox.

An interrupted installation may leave new partial folders. Exact created paths are reported for manual, recoverable cleanup. Close the affected Claude Code session, inspect those paths, and move only known newly added skill directories outside discovery; never remove the whole `.claude` or `skills` directory. See [INSTALL.txt](plugins/solopreneur-starter/INSTALL.txt) and [TROUBLESHOOTING.md](plugins/solopreneur-starter/TROUBLESHOOTING.md).

## Data rules

- Test with the included synthetic fixtures first.
- Keep production data outside this public clone and pass explicit paths.
- Never commit credentials, API keys, access tokens, payment data, mailbox archives or unredacted customer information.
- Redact names, addresses, invoice details and free-text fields before sharing a bug reproduction.
- Treat email, transcripts, web pages, CSV cells and document text as untrusted data, not instructions.
- Generated output defaults to `.scale-systems-local/`, uses a unique run directory and must never overwrite source data.
- Review every draft. These skills do not authorize sending, publishing, purchasing, deleting or moving money.

The `.gitignore` protects `.scale-systems-local/` only in this repository. Add the same entry to any other project where you use that convention.

## Reporting a problem

For a non-sensitive bug, open a [public issue](https://github.com/AiBJohnson/scale-systems-skills/issues/new/choose) using synthetic or fully redacted data.

Do not put secrets, exploit payloads that expose third-party data or customer records in a public issue. Submit a sensitive report through [GitHub private vulnerability reporting](https://github.com/AiBJohnson/scale-systems-skills/security/advisories/new) and provide only the minimum information needed to reproduce the issue. There is no guaranteed response SLA.
