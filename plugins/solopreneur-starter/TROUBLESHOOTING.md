# Troubleshooting

## The installer says DRY RUN but no skills appeared

That is expected: the default previews and writes nothing. Check the displayed project
and exact eight folder paths. Rerun the same command with --apply only if they are correct.
The installer copies skills only; it deliberately does not copy context or example files.

## The installer stopped at an existing skill or symlink

It refuses every existing target skill path, including dangling symlinks, instead of
merging or replacing your work. Do not work around this with an overwrite command.

Check the exact path it printed. It may be a prior installation or a skill you customized.
Close the affected Claude Code session, inspect that folder, and use a file manager to
move only a known prior copy into a dated backup outside all .claude/skills/ locations.
Preserve unrelated skills. Then preview the install again.

For a symlinked project, .claude folder, or destination, choose a real, non-symlinked
project path. The installer intentionally does not follow symbolic links, including
existing ancestors. Do not remove a symlink or change its target just to pass this check.

## A permission or disk error interrupted --apply

No existing file is overwritten, but newly created folders may be incomplete. The error
prints those exact paths. Do not run partial skills. Close the affected session and inspect
only the newly created named skill folders. Move those folders to a dated recovery location
outside skill discovery using a file manager; do not remove the parent .claude or
skills directory. Fix the permission/storage issue, then run a new dry run.

The installer is not a transaction manager or backup tool. It does not automatically delete
partial work, repair permissions, or restore your system.

## The skills do not appear after a successful installation

First identify your installation method and scope.

- **Downloaded folders:** open Claude Code in the project shown in the installer output.
  Confirm that the selected .claude/skills/ contains the eight named folders, each with
  SKILL.md directly inside. Type /. Restart the session if the skills are missing,
  especially when the top-level skills folder was created during the session. Commands
  are normally unnamespaced, such as /meeting-notes.
- **Marketplace:** use /plugin list to confirm solopreneur-starter@scale-systems is
  enabled, then /reload-plugins. Use /solopreneur-starter:meeting-notes.
- **Custom destination:** an arbitrary directory is not automatically discovered. Choose
  project or user scope unless you deliberately manage another supported location.

Do not keep the same eight installed from both marketplace and downloaded folders, or
across competing project/user scopes. The installer cannot detect every duplicate outside
its selected destination. Check your existing setup before adding another copy.

## Python is missing or I am on native Windows

The optional installer requires Python 3.9+ on macOS, Linux, or WSL. It uses no external
packages. Native Windows is intentionally unsupported by this installer's symlink-safe
copy mechanism. Use the public marketplace route for the eight skills, or an appropriate
supported environment. Do not disable operating-system protections to make it run.

## A skill ignores my business details

The synthetic first run does not require a business context file. For your own work,
provide the relevant facts explicitly, or review the optional context instructions in
INSTALL.txt. An existing CLAUDE.md may contain important instructions: inspect and merge
carefully, never replace it with this pack's example. Start Claude Code in the intended
project and verify which context it has loaded.

## A skill invented a number, scope item, or commitment

Stop before using that output. Ask: "Show the source for each amount, date, decision, and
commitment; mark unsupported details unknown." Compare against the input and fixture
acceptance criteria. Skill instructions guide a model; they do not guarantee compliance.

## A skill wants to send, publish, or change an account

Decline. These skills prepare local drafts and reviews, not outbound actions. Confirm the
exact command and installed copy, inspect its SKILL.md, and check whether another plugin
or instruction changed the behavior. Never supply credentials to fix this.

## It is slow or costly

Use one specific input rather than a whole client folder. Reduce irrelevant context and
check Claude Code's usage information and your applicable plan. Access and usage costs
are separate from this download; this pack does not guarantee a time or cost saving.

## I want to uninstall or upgrade

Follow the exact-folder recovery steps in INSTALL.txt. Keep custom changes before moving
only this pack's added skill directories outside discovery. Do not delete .claude, the
whole skills directory, business context, or unrelated project files. For a marketplace
installation, manage the exact solopreneur-starter@scale-systems entry in the plugin manager.

## Something is genuinely broken

Reply to your receipt with the skill name, Claude Code version, operating system, Python
version if relevant, installation method, exact command, sanitized input schema, and
observed result. GitHub users can report a non-sensitive issue in the public repository.
Do not send client records, customer identities, passwords, access tokens, or full private logs.
