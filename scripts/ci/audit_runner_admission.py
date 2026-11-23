#!/usr/bin/env python3
"""Fail closed unless every GitHub Actions job uses a GitHub-hosted Ubuntu runner.

This repository no longer permits server-side/self-hosted Actions runners.
The deliberately small YAML reader supports the workflow subset used here and
rejects missing, dynamic, or non-ubuntu-latest runs-on values.
"""

from __future__ import annotations

import sys
from pathlib import Path

WORKFLOW_DIR = Path(".github/workflows")


def uncomment(line: str) -> str:
    quote = None
    escaped = False
    for i, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quote == '"':
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = None
        elif char in ("'", '"'):
            quote = char
        elif char == "#" and (i == 0 or line[i - 1].isspace()):
            return line[:i].rstrip()
    return line.rstrip()


def indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def parse_job_headers(lines: list[str]) -> list[tuple[str, int, int]]:
    jobs_index = next((i for i, line in enumerate(lines)
                       if indent_of(uncomment(line)) == 0
                       and uncomment(line).strip() == "jobs:"), None)
    if jobs_index is None:
        return []
    end = len(lines)
    for i in range(jobs_index + 1, len(lines)):
        clean = uncomment(lines[i])
        if clean.strip() and not clean.lstrip().startswith("#") and indent_of(clean) == 0:
            end = i
            break
    headers = []
    for i in range(jobs_index + 1, end):
        clean = uncomment(lines[i])
        if indent_of(clean) == 2 and clean.strip().endswith(":"):
            name = clean.strip()[:-1].strip(" '")
            headers.append((name, i, end))
    return [(name, start, headers[pos + 1][1] if pos + 1 < len(headers) else end)
            for pos, (name, start, _) in enumerate(headers)]


def parse_runs_on(lines: list[str], start: int, end: int) -> list[str] | None:
    entries = []
    for i in range(start + 1, end):
        clean = uncomment(lines[i])
        if indent_of(clean) == 4 and clean.strip().startswith("runs-on:"):
            entries.append((i, clean.split(":", 1)[1].strip()))
    if len(entries) != 1:
        return None
    index, value = entries[0]
    if value:
        return [value.strip(" '")]
    values = []
    for i in range(index + 1, end):
        clean = uncomment(lines[i])
        if not clean.strip():
            continue
        current_indent = indent_of(clean)
        if current_indent <= 4:
            break
        item = clean.strip()
        if current_indent != 6 or not item.startswith("-"):
            return None
        values.append(item[1:].strip(" '"))
    return values or None


def audit_workflow(path: Path) -> tuple[int, list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    jobs = parse_job_headers(lines)
    violations = []
    if not jobs:
        return 0, [f"{path}: no statically discoverable jobs"]
    for name, start, end in jobs:
        values = parse_runs_on(lines, start, end)
        if values is None:
            violations.append(f"{path}:{name}: runs-on is missing, dynamic, or unsupported")
        elif values != ["ubuntu-latest"]:
            violations.append(
                f"{path}:{name}: expected runs-on: ubuntu-latest; found {values!r}"
            )
    return len(jobs), violations


def main() -> int:
    files = sorted(WORKFLOW_DIR.glob("*.yml")) + sorted(WORKFLOW_DIR.glob("*.yaml"))
    if not files:
        print(f"::error::no workflow files found in {WORKFLOW_DIR}", file=sys.stderr)
        return 2
    total = 0
    violations = []
    for path in files:
        count, found = audit_workflow(path)
        total += count
        violations.extend(found)
    for violation in violations:
        print(f"::error::{violation}")
    print(f"GitHub-hosted runner policy: {total} job(s) audited, {len(violations)} violation(s)")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
