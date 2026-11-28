#!/usr/bin/env python3
"""Backfill AC4 documentation references for AID-2026-352."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

WORK_ITEMS = Path("14-ai-development/work-items")
BACKUP_NAME = "aid-2026-352-documentation-backup"

# Values are repository-relative paths beneath WORK_ITEMS/<ID>/.
MAPPINGS: dict[str, tuple[tuple[str, str], ...]] = {
    "AID-2026-100": (
        ("evidence-source-restore.md", "evidence"),
        ("evidence.md", "evidence"),
        ("owner-decision-merge-authorization.md", "design"),
        ("owner-delegation-record.md", "design"),
        ("prompt-v1.md", "reference"),
        ("session-evidence-source-restore.md", "evidence"),
    ),
    "AID-2026-112": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-113": (
        ("prompt-v1.md", "reference"),
        ("restore-evidence.md", "evidence"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-114": (
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-115": (
        ("gate-performance-and-rust-cache-evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-116": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-140": (
        ("prompt-v1.md", "reference"),
        ("restore-evidence.md", "evidence"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-150": (
        ("prompt-v1.md", "reference"),
        ("restore-evidence.md", "evidence"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-170": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-172": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-173": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-174": (
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-183": (
        ("prompt-v1.md", "reference"),
        ("session-evidence-827.md", "evidence"),
    ),
    "AID-2026-186": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-188": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-189": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-190": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-191": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-192": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-193": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-197": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-198": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-199": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-200": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-204": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-210": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-211": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-240": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-241": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("prompt-w3-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-256": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-261": (
        ("evidence.md", "evidence"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-268": (
        ("evidence.md", "evidence"),
        ("prompt-snapshot.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-279": (
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-280": (
        ("decision.md", "design"),
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
    "AID-2026-281": (
        ("evidence-05-index.md", "evidence"),
        ("evidence.md", "evidence"),
        ("prompt-v1.md", "reference"),
        ("session-evidence.md", "evidence"),
    ),
}


def backup_root_for(root: Path) -> Path:
    """Backups live inside the Git directory, which is a file in a worktree.

    Resolving it through Git keeps the backup untracked in a normal clone and
    in a linked worktree alike, instead of hard-coding `.git/`.
    """
    result = subprocess.run(
        ["git", "rev-parse", "--absolute-git-dir"],
        cwd=root, capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "cannot resolve the Git directory: "
            + (result.stderr or result.stdout).strip()
        )
    return Path(result.stdout.strip()) / BACKUP_NAME


def render_block(work_item: str) -> bytes:
    lines = ["documentation:"]
    for name, relationship in MAPPINGS[work_item]:
        lines.extend((
            f"  - path: 14-ai-development/work-items/{work_item}/{name}",
            f"    relationship: {relationship}",
        ))
    return ("\n".join(lines) + "\n").encode("utf-8")


def plan(root: Path) -> dict[Path, tuple[bytes, bytes]]:
    changes: dict[Path, tuple[bytes, bytes]] = {}
    for work_item, entries in MAPPINGS.items():
        manifest = root / WORK_ITEMS / work_item / "manifest.yaml"
        if not manifest.is_file():
            raise RuntimeError(f"missing manifest: {manifest}")
        original = manifest.read_bytes()
        text = original.decode("utf-8")
        block = render_block(work_item)

        for name, _relationship in entries:
            target = root / WORK_ITEMS / work_item / name
            if not target.is_file():
                raise RuntimeError(f"referenced document does not exist: {target}")

        # An exact previously-generated suffix is the idempotent state.
        if original.endswith(block):
            changes[manifest] = (original, original)
            continue

        if "\ndocumentation:" in "\n" + text:
            raise RuntimeError(
                f"refusing to overwrite non-generated documentation: {manifest}"
            )

        separator = b"" if original.endswith((b"\n", b"\r")) else b"\n"
        updated = original + separator + block
        if not updated.endswith(block):
            raise AssertionError(f"rendered block is not a suffix: {manifest}")
        changes[manifest] = (original, updated)

    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--rollback", action="store_true")
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.root.resolve()
    backup_root = backup_root_for(root)

    try:
        if args.rollback:
            if not backup_root.is_dir():
                raise RuntimeError(f"rollback backup does not exist: {backup_root}")
            restored = 0
            for work_item in MAPPINGS:
                rel = WORK_ITEMS / work_item / "manifest.yaml"
                backup = backup_root / rel
                target = root / rel
                if not backup.is_file():
                    raise RuntimeError(f"rollback backup missing: {backup}")
                target.write_bytes(backup.read_bytes())
                restored += 1
            print(f"rollback restored files: {restored}")
            return 0

        changes = plan(root)
        changed = {
            path: pair for path, pair in changes.items()
            if pair[0] != pair[1]
        }
        print(f"files to change: {len(changed)}")
        if args.dry_run:
            for path in sorted(changed):
                print(f"  {path.relative_to(root).as_posix()}")
            return 0

        if not changed:
            print("files changed: 0")
            print("idempotence: PASS")
            return 0

        if backup_root.exists():
            raise RuntimeError(
                f"backup already exists; refusing to overwrite: {backup_root}"
            )
        backup_root.mkdir(parents=True)
        for path, (original, updated) in sorted(changes.items()):
            rel = path.relative_to(root)
            backup = backup_root / rel
            backup.parent.mkdir(parents=True, exist_ok=True)
            backup.write_bytes(original)
            path.write_bytes(updated)

        # Verify exact byte idempotence after writing.
        second_plan = plan(root)
        if any(old != new for old, new in second_plan.values()):
            raise AssertionError("second run would change bytes; idempotence failed")
        print(f"files changed: {len(changed)}")
        print("idempotence: PASS")
        return 0
    except (OSError, UnicodeError, RuntimeError, AssertionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
