#!/usr/bin/env python3
"""Generate the deterministic DM-16 supersession reverse index."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from check_document_management import (  # noqa: E402
    collect_governed,
    dig,
    read_metadata,
)

INDEX_REL = Path("14-ai-development/reports/supersession-index.json")


def build_index(root: Path) -> dict:
    targets, problems = collect_governed(root)
    if problems:
        raise RuntimeError(
            "cannot generate supersession index from an incomplete governed "
            "document scan: " + "; ".join(problems)
        )

    reverse: dict[str, set[str]] = {}
    for path in targets:
        if not path.is_file():
            raise RuntimeError(f"governed path is not a file: {path}")
        rel = path.relative_to(root).as_posix()
        metadata = read_metadata(path.read_text(encoding="utf-8"))
        if metadata is None:
            continue

        supersedes = dig(
            metadata, "lifecycle", "supersession", "supersedes"
        )
        if supersedes is None:
            continue
        if not isinstance(supersedes, list):
            raise RuntimeError(
                f"{rel}: lifecycle.supersession.supersedes must be a list"
            )

        for target in supersedes:
            if not isinstance(target, str) or not target.strip():
                raise RuntimeError(
                    f"{rel}: supersedes entries must be non-empty strings"
                )
            target = target.strip().replace("\\", "/")
            reverse.setdefault(target, set()).add(rel)

    return {
        "schema_version": 1,
        "superseded_by": {
            target: sorted(sources)
            for target, sources in sorted(reverse.items())
        },
    }


def render_index(root: Path) -> bytes:
    payload = build_index(root)
    return (
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()

    root = args.root.resolve()
    target = root / INDEX_REL
    try:
        expected = render_index(root)
        if args.write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(expected)
            print(f"DM-16 generated: {INDEX_REL.as_posix()}")
            return 0

        if not target.is_file():
            print(
                f"DM-16 generated supersession index is missing: "
                f"{INDEX_REL.as_posix()}",
                file=sys.stderr,
            )
            return 1
        actual = target.read_bytes()
        if actual != expected:
            print(
                f"DM-16 generated supersession index is stale: "
                f"{INDEX_REL.as_posix()}",
                file=sys.stderr,
            )
            return 1
        print("DM-16 generated supersession index: current")
        return 0
    except (OSError, UnicodeError, RuntimeError, ValueError) as exc:
        print(f"DM-16 generation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
