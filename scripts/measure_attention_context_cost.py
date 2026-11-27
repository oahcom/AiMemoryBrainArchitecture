#!/usr/bin/env python3
"""Read-only measurement of declared work-item root/domain fan-out.

No YAML package or other third-party dependency is used. The reader intentionally
consumes only path-bearing lists under scope (changes, files_to_create,
files_to_modify, files_changed); prose and files_out_of_scope are excluded.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

ROOTS = (
    ".github", "00-governance", "01-system-architecture", "02-domain-model",
    "03-memory-brain", "04-memory-compiler", "05-memory-runtime",
    "06-memory-context", "07-agent-integration", "08-bmcp-protocol",
    "09-security-governance", "10-storage-consistency",
    "13-engineering-decisions", "14-ai-development", "scripts", "docs",
    "reviews", "tests", "crates", "experiments", "prompts", "recovery", "tools",
)
MANIFEST_RE = re.compile(
    r"^14-ai-development/work-items/(AID-2026-(\d{3}))/manifest\.yaml$"
)
SCOPE_LISTS = {"changes", "files_to_create", "files_to_modify", "files_changed"}


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], check=False, text=True, encoding="utf-8",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} exited {result.returncode}")
    return result.stdout


def scope_paths(manifest: str) -> list[str]:
    lines = manifest.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line == "scope:")
    except StopIteration:
        return []
    selected: list[str] = []
    active = False
    for line in lines[start + 1:]:
        if line and not line[0].isspace() and re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:", line):
            break
        key = re.match(r"^  ([A-Za-z_][A-Za-z0-9_-]*):\s*$", line)
        if key:
            active = key.group(1) in SCOPE_LISTS
            continue
        if not active:
            continue
        item = re.match(r"^\s+-\s+(?:path:\s*)?(.+?)\s*$", line)
        if item:
            value = item.group(1).strip().strip("\"'").rstrip("/")
            if "/" in value:
                selected.append(value)
    return selected


def domains_for(paths: list[str]) -> list[str]:
    found = set()
    for value in paths:
        for root in ROOTS:
            if re.search(r"(?<![A-Za-z0-9_.-])" + re.escape(root) + r"/", value):
                found.add(root)
    return sorted(found)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="HEAD", help="Git ref whose committed tree is measured (default: HEAD)")
    parser.add_argument("--limit", type=int, default=10, help="most recent AID manifests to include (default: 10)")
    parser.add_argument("--budget", type=int, default=3, help="soft root/domain fan-out budget (default: 3)")
    parser.add_argument("--hard-cap", type=int, default=5, help="hard fan-out cap; exceeding it is a stop (default: 5)")
    args = parser.parse_args()
    if args.limit < 1 or args.budget < 1 or args.hard_cap < args.budget:
        parser.error("limit and budget must be positive; hard-cap must be >= budget")
    try:
        names = git("ls-tree", "-r", "--name-only", args.ref).splitlines()
        manifests = []
        for path in names:
            match = MANIFEST_RE.fullmatch(path)
            if match:
                manifests.append((int(match.group(2)), path))
        manifests.sort(reverse=True)
        selected = manifests[:args.limit]
        if not selected:
            print(f"ERROR: no AID-2026 manifests found at {args.ref}", file=sys.stderr)
            return 2
        rows = []
        for number, path in selected:
            content = git("show", f"{args.ref}:{path}")
            domains = domains_for(scope_paths(content))
            rows.append((f"AID-2026-{number:03d}", domains))
    except (RuntimeError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    total = sum(len(domains) for _, domains in rows)
    maximum = max(len(domains) for _, domains in rows)
    distribution = {}
    for _, domains in rows:
        distribution[len(domains)] = distribution.get(len(domains), 0) + 1
    print(f"ref={args.ref} cohort={len(rows)}")
    for item, domains in rows:
        print(f"{item} roots={len(domains)} [{', '.join(domains) if domains else 'UNDECLARED'}]")
    print(f"mean_roots_per_work_item={total / len(rows):.2f} ({total}/{len(rows)})")
    print(f"max_roots_per_work_item={maximum}")
    print("distribution=" + ", ".join(f"{key}:{distribution[key]}" for key in sorted(distribution)))
    over = [item for item, domains in rows if len(domains) > args.budget]
    hard = [item for item, domains in rows if len(domains) > args.hard_cap]
    print(f"over_soft_budget(>{args.budget})={len(over)} [{', '.join(over) if over else 'none'}]")
    print(f"over_hard_cap(>{args.hard_cap})={len(hard)} [{', '.join(hard) if hard else 'none'}]")
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
