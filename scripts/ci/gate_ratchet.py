#!/usr/bin/env python3
"""Run a failure-set ratchet against a base-commit-anchored baseline.

The base commit is authoritative. The candidate baseline may remove entries
to pay down existing debt, but may never add entries.

Exit codes:
    0: ratchet holds
    1: regression, baseline growth, or stale remaining debt
    2: incomplete Git state, invalid invocation, or unreadable baseline
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

BASELINES = {
    "manifest-blob-pins": "scripts/ci/baselines/manifest-blob-pins.txt",
    "manifest-blob-pins-unresolved": (
        "scripts/ci/baselines/manifest-blob-pins-unresolved.txt"
    ),
    "bilingual-docs": "scripts/ci/baselines/bilingual-docs.txt",
}

NUMBERED_PREFIX = re.compile(r"^\d{3,4}\.\s+")
SUMMARY_RE = re.compile(
    r"^(?:PASS|FAIL|OK|FAILED|NO TESTS)(?![A-Za-z0-9_])"
    r"|^Ran\s"
    r"|^GOV-DOC-001 full scan:"
    r"|^runner admission:"
)
ITEM_TOKEN_RE = re.compile(
    r"\S*/\S*|\b[\w.-]+\.(?:md|py|ya?ml|rs|toml|json|txt)\b"
)


class IncompleteError(Exception):
    """The requested comparison cannot be established safely."""


def git_output(root: Path, *args: str) -> bytes:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=root,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        raise IncompleteError(f"cannot execute git: {exc}") from exc
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", errors="replace").strip()
        raise IncompleteError(
            f"git {' '.join(args)} failed ({proc.returncode}): {detail}"
        )
    return proc.stdout


def resolve_base_commit(root: Path, ref: str) -> str:
    if not ref or ref.startswith("-"):
        raise IncompleteError("baseline ref is missing or invalid")
    try:
        resolved = git_output(
            root, "rev-parse", "--verify", "--end-of-options",
            f"{ref}^{{commit}}",
        ).decode("ascii").strip()
    except IncompleteError as exc:
        raise IncompleteError(
            f"base ref is not an available commit: {ref}: {exc}"
        ) from exc
    if not re.fullmatch(r"[0-9a-fA-F]{40,64}", resolved):
        raise IncompleteError(f"base ref did not resolve to a commit: {ref}")
    return resolved


def parse_entries(data: bytes, description: str) -> set[str]:
    try:
        content = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise IncompleteError(
            f"{description} is not valid UTF-8: {exc}"
        ) from exc

    entries: set[str] = set()
    for raw in content.splitlines():
        item = raw.strip()
        if not item or item.startswith("#"):
            continue
        entries.add(item)
    return entries


def read_base_baseline(root: Path, commit: str, path: str) -> set[str]:
    try:
        data = git_output(root, "show", f"{commit}:{path}")
    except IncompleteError as exc:
        raise IncompleteError(
            f"baseline path does not exist or cannot be read at base "
            f"{commit}: {path}: {exc}"
        ) from exc
    return parse_entries(data, f"base baseline {path}")


def read_candidate_baseline(root: Path, path: str) -> set[str]:
    candidate = root / path
    try:
        if candidate.is_symlink():
            raise IncompleteError(
                f"candidate baseline must not be a symlink: {path}"
            )
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root.resolve(strict=True))
        if not resolved.is_file():
            raise IncompleteError(
                f"candidate baseline is not a regular file: {path}"
            )
        data = resolved.read_bytes()
    except IncompleteError:
        raise
    except (OSError, ValueError) as exc:
        raise IncompleteError(
            f"candidate baseline cannot be read: {path}: {exc}"
        ) from exc
    return parse_entries(data, f"candidate baseline {path}")


def is_summary(line: str) -> bool:
    return bool(SUMMARY_RE.match(line)) and not ITEM_TOKEN_RE.search(line)


def normalize(lines: list[str], fmt: str) -> list[str]:
    items: set[str] = set()
    for raw in lines:
        line = raw.strip()
        if not line or is_summary(line):
            continue
        if fmt == "paths":
            line = NUMBERED_PREFIX.sub("", line)
        items.add(line)
    return sorted(items)


def compare(
    baseline: set[str], current: list[str]
) -> tuple[list[str], list[str]]:
    """Return (regressions, remaining baseline entries no longer failing)."""
    unused = set(baseline)
    regressions: list[str] = []

    for item in current:
        matched = item if item in unused else None
        if matched is None:
            for entry in sorted(unused):
                if item.startswith(entry + " -> "):
                    matched = entry
                    break
        if matched is None:
            regressions.append(item)
        else:
            unused.remove(matched)

    return sorted(regressions), sorted(unused)


def run_command(command: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        raise IncompleteError(f"cannot execute wrapped command: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-ref", required=True)
    parser.add_argument("--baseline-id", required=True, choices=sorted(BASELINES))
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--command", required=True)
    parser.add_argument(
        "--format", choices=("schema", "paths"), default="schema"
    )
    args = parser.parse_args(argv)

    expected_path = BASELINES[args.baseline_id]
    if args.baseline.replace("\\", "/") != expected_path:
        print(
            "INCOMPLETE: baseline path does not match registered baseline "
            f"{args.baseline_id}: expected {expected_path}, "
            f"received {args.baseline}",
            file=sys.stderr,
        )
        return 2

    root = Path.cwd()
    try:
        base_commit = resolve_base_commit(root, args.baseline_ref)
        base_entries = read_base_baseline(root, base_commit, expected_path)
        candidate_entries = read_candidate_baseline(root, expected_path)
    except IncompleteError as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2

    try:
        proc = run_command(args.command)
    except IncompleteError as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2

    current = normalize(proc.stdout.splitlines(), args.format)

    additions = sorted(candidate_entries - base_entries)
    removals = sorted(base_entries - candidate_entries)

    print(f"ratchet: baseline-id={args.baseline_id}")
    print(f"ratchet: baseline-path={expected_path}")
    print(f"ratchet: baseline-ref={base_commit}")
    print(
        f"ratchet: base={len(base_entries)} "
        f"candidate={len(candidate_entries)} "
        f"added={len(additions)} removed={len(removals)}"
    )

    if additions:
        print(f"ratchet: wrapped-command-exit={proc.returncode}")
        for item in current:
            print(f"ratchet: wrapped-command-item: {item}")
        for item in additions:
            print(f"::error::unauthorized baseline addition: {item}")
        print(
            f"ratchet: FAIL - candidate baseline added "
            f"{len(additions)} unauthorized item(s)."
        )
        return 1

    for item in removals:
        print(f"ratchet: baseline debt retired: {item}")

    regressions, fixed = compare(candidate_entries, current)

    print(
        f"ratchet: current={len(current)} "
        f"regressions={len(regressions)} "
        f"remaining_fixed={len(fixed)}"
    )

    if proc.returncode not in (0, 1):
        print(
            f"ratchet: FAIL - wrapped command exited {proc.returncode}; "
            "only exit 0 and 1 provide a comparable failure set."
        )
        return 1

    if proc.returncode != 0 and not current:
        print(
            f"ratchet: FAIL - wrapped command exited {proc.returncode} "
            "without printing any item; a crash is not a clean run."
        )
        return 1

    for item in regressions:
        print(f"::error::ratchet regression: {item}")
    for item in fixed:
        print(f"::error::ratchet baseline is stale: {item}")

    if regressions or fixed:
        if regressions:
            print(
                f"ratchet: FAIL - {len(regressions)} new failure(s)."
            )
        if fixed:
            print(
                f"ratchet: FAIL - {len(fixed)} baseline item(s) "
                "no longer fail; lower the candidate baseline."
            )
        return 1

    print("ratchet: PASS - failure set matches the authorized baseline.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
