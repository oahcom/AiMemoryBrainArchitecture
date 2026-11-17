#!/usr/bin/env python3
"""Validate bilingual AI-RUN architecture docs and their local Markdown links."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOC_PREFIXES = ("14-ai-development/", "reviews/ai-run-003/")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
ZH_RE = re.compile(r"[\u4e00-\u9fff]")
EN_RE = re.compile(r"[A-Za-z]")
SKIP_SCHEMES = ("http:", "https:", "mailto:", "app:", "data:", "#")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def changed_markdown(base: str, head: str) -> list[Path]:
    names = git("diff", "--name-only", "--diff-filter=ACMRT", base, head).splitlines()
    return [
        ROOT / name
        for name in names
        if name.endswith(".md") and name.startswith(DOC_PREFIXES) and (ROOT / name).is_file()
    ]


def validate_bilingual(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if not ZH_RE.search(text):
        errors.append(f"{path.relative_to(ROOT)}: missing Chinese content")
    if not EN_RE.search(text):
        errors.append(f"{path.relative_to(ROOT)}: missing English content")
    return errors


def validate_local_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for raw in LINK_RE.findall(text):
        target = raw.strip().split()[0].strip("<>")
        if not target or target.startswith(SKIP_SCHEMES):
            continue
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue
        relative = unquote(parsed.path)
        if not relative:
            continue
        candidate = (path.parent / relative).resolve()
        try:
            candidate.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: link escapes repository: {target}")
            continue
        if not candidate.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken local link: {target}")
    return errors


def main() -> int:
    base = os.environ.get("BASE_SHA", "")
    head = os.environ.get("HEAD_SHA", "")
    if not base or not head:
        print("BASE_SHA and HEAD_SHA are required", file=sys.stderr)
        return 2
    files = changed_markdown(base, head)
    if not files:
        print("No changed AI-RUN markdown files in the validation scope.")
        return 0
    errors: list[str] = []
    for path in files:
        errors.extend(validate_bilingual(path))
        errors.extend(validate_local_links(path))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated bilingual content and local links in {len(files)} changed Markdown files.")
    for path in files:
        print(f"PASS {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
