#!/usr/bin/env python3
"""Preview or install only this pack's skill directories; never overwrite.

Standard library only. macOS, Linux and WSL, Python 3.9+. No account access,
network, model invocation, context-file copying, deletion or automatic updates.
"""

from __future__ import annotations

import argparse
import contextlib
import os
from pathlib import Path
import shutil
import stat
import sys


EXPECTED_SKILLS = (
    "content-repurpose", "decision-brief", "expense-categorise", "file-organiser",
    "inbox-triage", "invoice-chase", "meeting-notes", "weekly-numbers",
)


class InstallError(Exception):
    """A validation failure that must not be worked around automatically."""


def absolute_path(value: str) -> Path:
    # Do not resolve symlinks: they must remain visible to the refusal checks.
    return Path(os.path.abspath(os.path.expanduser(value)))


def check_directory_path(path: Path, must_exist: bool = False) -> None:
    current = Path(path.anchor)
    for component in path.parts[1:]:
        current /= component
        try:
            info = current.lstat()
        except FileNotFoundError:
            if must_exist:
                raise InstallError(f"Directory does not exist: {current}")
            return
        if stat.S_ISLNK(info.st_mode):
            raise InstallError(f"Symlink paths are not allowed: {current}")
        if not stat.S_ISDIR(info.st_mode):
            raise InstallError(f"Expected a directory, found another object: {current}")


def validate_tree(path: Path) -> None:
    for child in sorted(path.iterdir()):
        info = child.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise InstallError(f"Source contains a symlink: {child}")
        if stat.S_ISDIR(info.st_mode):
            validate_tree(child)
        elif not stat.S_ISREG(info.st_mode):
            raise InstallError(f"Source contains a non-regular file: {child}")


@contextlib.contextmanager
def directory_fd(path: Path):
    """Open each existing ancestor without following symlinks."""
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    descriptor = os.open(path.anchor, flags)
    try:
        for component in path.parts[1:]:
            next_descriptor = os.open(component, flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = next_descriptor
        yield descriptor
    finally:
        os.close(descriptor)


def copy_tree(source_fd: int, target_fd: int) -> None:
    """All target entries are new, created exclusively relative to a pinned fd."""
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    for name in sorted(os.listdir(source_fd)):
        info = os.stat(name, dir_fd=source_fd, follow_symlinks=False)
        if stat.S_ISDIR(info.st_mode):
            os.mkdir(name, mode=0o755, dir_fd=target_fd)
            with contextlib.ExitStack() as stack:
                source_child = os.open(name, flags, dir_fd=source_fd)
                stack.callback(os.close, source_child)
                target_child = os.open(name, flags, dir_fd=target_fd)
                stack.callback(os.close, target_child)
                copy_tree(source_child, target_child)
        elif stat.S_ISREG(info.st_mode):
            with contextlib.ExitStack() as stack:
                source_file = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=source_fd)
                source_stream = stack.enter_context(os.fdopen(source_file, "rb"))
                if not stat.S_ISREG(os.fstat(source_stream.fileno()).st_mode):
                    raise InstallError(f"Source changed during installation: {name}")
                target_file = os.open(
                    name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                    stat.S_IMODE(info.st_mode) & 0o777, dir_fd=target_fd,
                )
                target_stream = stack.enter_context(os.fdopen(target_file, "wb"))
                shutil.copyfileobj(source_stream, target_stream)
        else:
            raise InstallError(f"Source changed or contains an unsafe entry: {name}")


def apply_install(source: Path, base: Path, destination: Path, created: list[Path]) -> None:
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    with directory_fd(base) as base_fd, contextlib.ExitStack() as stack:
        target_fd = os.dup(base_fd)
        stack.callback(os.close, target_fd)
        current = base
        for component in destination.relative_to(base).parts:
            current /= component
            try:
                os.mkdir(component, mode=0o755, dir_fd=target_fd)
                created.append(current)
            except FileExistsError:
                pass  # Open below rejects a symlink or non-directory, even after a race.
            target_fd = os.open(component, flags, dir_fd=target_fd)
            stack.callback(os.close, target_fd)

        # Recheck the complete set before creating any skill folder.
        for name in EXPECTED_SKILLS:
            try:
                os.stat(name, dir_fd=target_fd, follow_symlinks=False)
            except FileNotFoundError:
                continue
            raise InstallError(f"Destination collision: {destination / name}")

        with directory_fd(source) as source_fd:
            for name in EXPECTED_SKILLS:
                os.mkdir(name, mode=0o755, dir_fd=target_fd)
                created.append(destination / name)
                with contextlib.ExitStack() as skill_stack:
                    source_skill = os.open(name, flags, dir_fd=source_fd)
                    skill_stack.callback(os.close, source_skill)
                    target_skill = os.open(name, flags, dir_fd=target_fd)
                    skill_stack.callback(os.close, target_skill)
                    copy_tree(source_skill, target_skill)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--project", metavar="FOLDER", help="existing project; install in its .claude/skills")
    scope.add_argument("--user", action="store_true", help="explicitly install user-wide in ~/.claude/skills")
    scope.add_argument("--destination", metavar="FOLDER", help="exact skill destination; its parent must exist")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="create the previewed skill folders")
    mode.add_argument("--dry-run", action="store_true", help="preview only (the default)")
    args = parser.parse_args(argv)
    created: list[Path] = []
    try:
        if sys.version_info < (3, 9) or os.name != "posix" or not hasattr(os, "O_NOFOLLOW"):
            raise InstallError("Use Python 3.9+ on macOS, Linux or WSL; native Windows is not supported.")
        source = absolute_path(str(Path(__file__).parent / "skills"))
        check_directory_path(source, must_exist=True)
        actual_names = sorted(child.name for child in source.iterdir())
        if actual_names != sorted(EXPECTED_SKILLS):
            raise InstallError("Source inventory differs from this pack's audited skill list. Use a fresh download.")
        for name in EXPECTED_SKILLS:
            check_directory_path(source / name, must_exist=True)
            skill_file = source / name / "SKILL.md"
            if not skill_file.is_file() or skill_file.is_symlink():
                raise InstallError(f"Missing or unsafe SKILL.md: {skill_file}")
            validate_tree(source / name)

        if args.project:
            base = absolute_path(args.project)
            destination = base / ".claude" / "skills"
        elif args.user:
            base = absolute_path(str(Path.home()))
            destination = base / ".claude" / "skills"
        else:
            destination = absolute_path(args.destination)
            base = destination.parent
        if destination in (Path(destination.anchor), absolute_path(str(Path.home()))):
            raise InstallError("Choose a dedicated skills directory, not a filesystem root or home directory.")
        if source.parent == destination or source.parent in destination.parents:
            raise InstallError("Do not install inside the extracted product folder. Choose a separate project.")
        check_directory_path(base, must_exist=True)
        check_directory_path(destination)
        conflicts = [destination / name for name in EXPECTED_SKILLS if os.path.lexists(destination / name)]
        if conflicts:
            raise InstallError("Existing skill paths; nothing will be merged or replaced:\n  " + "\n  ".join(map(str, conflicts)))

        print(f"{'APPLY' if args.apply else 'DRY RUN'}: {len(EXPECTED_SKILLS)} skill folders")
        print(f"Source: {source}")
        print(f"Destination: {destination}")
        for name in EXPECTED_SKILLS:
            print(f"  NEW {destination / name}")
        print("Only skill folders are included. No context, examples, accounts or settings are changed.")
        if not args.apply:
            print("Nothing was written. To install, rerun the same command with --apply.")
            return 0
        apply_install(source, base, destination, created)
        print(f"Installed {len(EXPECTED_SKILLS)} skill folders. No existing file was overwritten.")
        print("Keep this exact path list for recovery. Check INSTALL.txt before your first run.")
        return 0
    except (InstallError, OSError) as error:
        print(f"STOPPED: {error}", file=sys.stderr)
        if created:
            print("Installation may be incomplete. Existing files were not overwritten. Inspect only these newly created paths:", file=sys.stderr)
            for path in created:
                print(f"  {path}", file=sys.stderr)
            print("Do not run partial skills. See TROUBLESHOOTING.md for target-specific recovery.", file=sys.stderr)
        else:
            print("Nothing was written.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
