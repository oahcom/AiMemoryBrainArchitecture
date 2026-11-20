#!/usr/bin/env python3
"""Verify bilingual Source revision / 源版本 pointers against the current Git tree.

Exit 0 only when every live pointer resolves and matches its source blob, and
every DEREFERENCED record names an existing surviving counterpart.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DOC_ROOTS = (ROOT / "docs" / "en", ROOT / "docs" / "zh-CN")
REVISION_RE = re.compile(
    r"^\s*-\s*(?:Source revision|源版本|源文件版本):\s*(.*?)\s*$",
    re.MULTILINE,
)
SOURCE_LINE_RE = re.compile(
    r"^\s*-\s*(?:Source:|源规范：|源规范:|对应完整源规范：|对应完整源规范:).*$",
    re.MULTILINE,
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SHA_RE = re.compile(r"[0-9a-f]{40}\Z")


def git_blob(path: str) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        return None
    return result.stdout.strip()


def repo_relative(doc: Path, raw_link: str) -> str | None:
    link = unquote(raw_link.strip()).split("#", 1)[0]
    if not link or "://" in link or link.startswith("//"):
        return None
    target = (doc.parent / link).resolve()
    try:
        return target.relative_to(ROOT).as_posix()
    except ValueError:
        return None


def source_lines(text: str) -> list[str]:
    return SOURCE_LINE_RE.findall(text)


def main() -> int:
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

    for doc_root in DOC_ROOTS:
        if not doc_root.exists():
            continue
        for doc in sorted(doc_root.rglob("*.md")):
            text = doc.read_text(encoding="utf-8")
            for match in REVISION_RE.finditer(text):
                line_no = text.count("\n", 0, match.start()) + 1
                value = match.group(1).strip()
                rel_doc = doc.relative_to(ROOT).as_posix()

                if "DEREFERENCED" in value:
                    totals["pointers"] += 1
                    candidates = [
                        line for line in source_lines(text)
                        if "DEREFERENCED" in line
                    ]
                    alt = None
                    for line in candidates:
                        links = MARKDOWN_LINK_RE.findall(line)
                        if links:
                            alt = repo_relative(doc, links[-1])
                            break
                    if alt and git_blob(alt):
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
                    continue

                if not SHA_RE.fullmatch(value):
                    totals["non_blob_reference"] += 1
                    details.append(
                        f"NON_BLOB_REFERENCE {rel_doc}:{line_no} -> {value}"
                    )
                    continue

                totals["pointers"] += 1
                links = []
                for line in source_lines(text):
                    if "DEREFERENCED" not in line:
                        links.extend(MARKDOWN_LINK_RE.findall(line))
                source_path = repo_relative(doc, links[0]) if links else None
                actual = git_blob(source_path) if source_path else None

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

    bad = totals["stale"] + totals["unresolved"] + totals["bad_dereference"]
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
