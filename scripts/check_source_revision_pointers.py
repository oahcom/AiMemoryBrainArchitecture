#!/usr/bin/env python3
"""Verify bilingual Source revision / 源版本 pointers against the current Git tree.

Exit 0 only when every live pointer resolves and matches its source blob, and
every DEREFERENCED record names an existing surviving counterpart.

"Every live pointer" includes the ones that do not name a blob. A value such as
`main`, `HEAD` or `v1.2` cannot be compared to anything, so it used to be
printed as NON_BLOB_REFERENCE and then dropped from the verdict: a movable
reference passed a gate whose docstring claims every pointer resolves. It is
now a failure like a stale SHA.

Each pointer is compared to the `Source:` line that belongs to it -- the n-th
live revision record with the n-th live source line, in document order. Before
this, every pointer in a document was compared against `links[0]`, so a
document with two pairs had its second pointer checked against the first
pointer's file: a correct pointer could be reported STALE, and a wrong one
could be confirmed by the wrong blob.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REVISION_RE = re.compile(
    r"^\s*-\s*(?:Source revision|源版本|源文件版本)[:：]\s*(.*?)\s*$",
    re.MULTILINE,
)
SOURCE_LINE_RE = re.compile(
    r"^\s*-\s*(?:Source:|源规范：|源规范:|对应完整源规范：|对应完整源规范:).*$",
    re.MULTILINE,
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SHA_RE = re.compile(r"[0-9a-f]{40}\Z")


def doc_roots(root: Path) -> tuple[Path, Path]:
    return (root / "docs" / "en", root / "docs" / "zh-CN")


def git_blob(root: Path, path: str) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=root,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if result.returncode:
        return None
    return result.stdout.strip()


def repo_relative(root: Path, doc: Path, raw_link: str) -> str | None:
    link = unquote(raw_link.strip()).split("#", 1)[0]
    if not link or "://" in link or link.startswith("//"):
        return None
    target = (doc.parent / link).resolve()
    try:
        return target.relative_to(root).as_posix()
    except ValueError:
        return None


def source_lines(text: str) -> list[str]:
    return SOURCE_LINE_RE.findall(text)


def scan(root: Path) -> tuple[dict[str, int], list[str]]:
    totals = {
        "pointers": 0,
        "accurate": 0,
        "stale": 0,
        "unresolved": 0,
        "dereferenced": 0,
        "bad_dereference": 0,
        "non_blob_reference": 0,
    }
    details: list[str] = []

    for doc_root in doc_roots(root):
        if not doc_root.exists():
            continue
        for doc in sorted(doc_root.rglob("*.md")):
            text = doc.read_text(encoding="utf-8")
            rel_doc = doc.relative_to(root).as_posix()

            # One entry per live revision record, in document order. Records
            # that carry their own replacement are handled in the DEREFERENCED
            # branch and are not paired with a source line.
            live_revisions: list[tuple[int, str]] = []
            for match in REVISION_RE.finditer(text):
                line_no = text.count("\n", 0, match.start()) + 1
                value = match.group(1).strip()

                if "DEREFERENCED" not in value:
                    live_revisions.append((line_no, value))
                    continue

                totals["pointers"] += 1
                candidates = [
                    line for line in source_lines(text)
                    if "DEREFERENCED" in line
                ]
                alt = None
                for line in candidates:
                    links = MARKDOWN_LINK_RE.findall(line)
                    if links:
                        alt = repo_relative(root, doc, links[-1])
                        break
                if alt and git_blob(root, alt):
                    totals["dereferenced"] += 1
                    details.append(
                        f"DEREFERENCED {rel_doc}:{line_no} -> {alt}"
                    )
                else:
                    totals["bad_dereference"] += 1
                    details.append(
                        f"BAD_DEREFERENCE {rel_doc}:{line_no} "
                        f"alternative_missing={alt or 'NO_LINK'}"
                    )

            live_sources = [
                line for line in source_lines(text) if "DEREFERENCED" not in line
            ]

            for index, (line_no, value) in enumerate(live_revisions):
                if not SHA_RE.fullmatch(value):
                    # A movable reference (`main`, `HEAD`, a tag) is not a
                    # verifiable pointer. Counting it in a category the verdict
                    # ignores is how it used to pass.
                    totals["non_blob_reference"] += 1
                    details.append(
                        f"NON_BLOB_REFERENCE {rel_doc}:{line_no} -> {value}"
                    )
                    continue

                totals["pointers"] += 1
                paired = live_sources[index] if index < len(live_sources) else ""
                links = MARKDOWN_LINK_RE.findall(paired)
                source_path = repo_relative(root, doc, links[0]) if links else None
                actual = git_blob(root, source_path) if source_path else None

                if not source_path or not actual:
                    totals["unresolved"] += 1
                    details.append(
                        f"UNRESOLVED {rel_doc}:{line_no} -> "
                        f"{source_path or 'NO_SOURCE_LINK'}"
                    )
                elif actual != value:
                    totals["stale"] += 1
                    details.append(
                        f"STALE {rel_doc}:{line_no} -> {source_path} "
                        f"declared={value} actual={actual}"
                    )
                else:
                    totals["accurate"] += 1
                    details.append(
                        f"ACCURATE {rel_doc}:{line_no} -> {source_path} {actual}"
                    )

    return totals, details


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="repository root to scan (default: the one containing this script)",
    )
    args = parser.parse_args(argv)

    totals, details = scan(args.root.resolve())

    bad = (
        totals["stale"]
        + totals["unresolved"]
        + totals["bad_dereference"]
        + totals["non_blob_reference"]
    )
    print("SOURCE_POINTER_SCAN")
    for key in (
        "pointers", "accurate", "stale", "unresolved",
        "dereferenced", "bad_dereference", "non_blob_reference",
    ):
        print(f"{key.upper()}={totals[key]}")
    print(f"BAD={bad}")
    for detail in details:
        print(detail)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
