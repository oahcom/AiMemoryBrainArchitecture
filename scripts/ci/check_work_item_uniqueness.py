#!/usr/bin/env python3
"""Merge-time uniqueness gate for work-item identities.

Candidate additions are measured from merge-base to the exact candidate HEAD;
occupancy is measured on the exact latest target commit supplied by CI.

Identity sources: directory names, top-level manifest work_item_id, top-level
legacy aid, and INDEX.md registrations.

Exit codes: 0 PASS; 1 VIOLATION; 2 INCOMPLETE.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict

ROOT = "14-ai-development/work-items"
INDEX = f"{ROOT}/INDEX.md"
ID_RE = re.compile(r"^AID-\d{4}-\d{3}$")
DIR_RE = re.compile(rf"^{re.escape(ROOT)}/(AID-\d{{4}}-\d{{3}})/")
CHECK_VERSION = "2026-11-27.2"
TIMEOUT = 30


class Incomplete(RuntimeError):
    """The comparison could not be completed safely."""


def run_git(*args: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise Incomplete(f"git {args!r}: {type(exc).__name__}: {exc}") from exc
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise Incomplete(
            f"git {args!r} exited {result.returncode}: {detail}"
        )
    return result.stdout


def resolve_commit(ref: str, label: str) -> str:
    if not re.fullmatch(r"[0-9a-fA-F]{40}", ref or ""):
        raise Incomplete(f"{label} must be a full 40-hex commit SHA")
    resolved = run_git("rev-parse", "--verify", f"{ref}^{{commit}}")
    sha = resolved.decode("ascii", errors="strict").strip().lower()
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise Incomplete(f"{label} did not resolve to a full commit SHA")
    return sha


def tree_paths(commit: str) -> list[str]:
    raw = run_git("ls-tree", "-r", "--name-only", "-z", commit)
    try:
        return [
            item.decode("utf-8", errors="strict")
            for item in raw.split(b"\0")
            if item
        ]
    except UnicodeError as exc:
        raise Incomplete(f"tree path is not valid UTF-8: {exc}") from exc


def read_blob(commit: str, path: str) -> str | None:
    try:
        raw = run_git("show", f"{commit}:{path}")
    except Incomplete as exc:
        run_git("cat-file", "-e", f"{commit}^{{commit}}")
        listing = run_git(
            "ls-tree", "-r", "--name-only", "-z", commit, "--", path
        )
        if not listing:
            return None
        raise Incomplete(f"cannot read {path} on {commit}: {exc}") from exc
    try:
        return raw.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise Incomplete(f"{path} on {commit} is not UTF-8: {exc}") from exc


def parse_scalar(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except ValueError as exc:
            raise Incomplete(f"invalid quoted manifest scalar {value!r}") from exc
        return parsed if isinstance(parsed, str) else ""
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise Incomplete(f"invalid single-quoted manifest scalar {value!r}")
        return value[1:-1].replace("''", "'")
    return re.split(r"\s+#", value, maxsplit=1)[0].strip()


def manifest_identities(content: str, path: str) -> set[str]:
    found: set[str] = set()
    for line_number, line in enumerate(content.splitlines(), 1):
        if line.startswith((" ", "\t")):
            continue
        match = re.match(r"^(work_item_id|aid)\s*:\s*(.*?)\s*$", line)
        if not match:
            continue
        identity = parse_scalar(match.group(2))
        if identity and ID_RE.fullmatch(identity):
            found.add(identity)
        elif identity:
            print(
                f"NOTICE: ignored non-AID identity in {path}:{line_number}",
                file=sys.stderr,
            )
    return found


def index_identities(content: str | None) -> set[str]:
    if content is None:
        return set()
    return set(re.findall(r"\bAID-\d{4}-\d{3}\b", content))


def directory_identities(paths: list[str]) -> set[str]:
    result: set[str] = set()
    for path in paths:
        match = DIR_RE.match(path)
        if match:
            result.add(match.group(1))
    return result


def occupied_identities(commit: str, paths: list[str]) -> set[str]:
    occupied = directory_identities(paths)
    for path in paths:
        match = DIR_RE.match(path)
        if match and path == f"{ROOT}/{match.group(1)}/manifest.yaml":
            content = read_blob(commit, path)
            if content is not None:
                occupied.update(manifest_identities(content, path))
    occupied.update(index_identities(read_blob(commit, INDEX)))
    return occupied


def introduced_directories(merge_base: str, head: str) -> list[str]:
    raw = run_git(
        "diff",
        "--diff-filter=A",
        "--name-only",
        "-z",
        "--no-renames",
        merge_base,
        head,
        "--",
        ROOT,
    )
    try:
        names = [
            item.decode("utf-8", errors="strict")
            for item in raw.split(b"\0")
            if item
        ]
    except UnicodeError as exc:
        raise Incomplete(f"candidate path is not UTF-8: {exc}") from exc

    candidates: set[str] = set()
    for name in names:
        match = DIR_RE.match(name)
        if match:
            candidates.add(f"{ROOT}/{match.group(1)}")

    base_paths = set(tree_paths(merge_base))
    return sorted(
        directory
        for directory in candidates
        if not any(path.startswith(directory + "/") for path in base_paths)
    )


def candidate_claims(
    head: str,
    merge_base: str,
    head_paths: list[str],
    introduced: list[str],
) -> dict[str, set[str]]:
    claims: dict[str, set[str]] = defaultdict(set)

    for directory in introduced:
        directory_id = directory.rsplit("/", 1)[-1]
        claims[directory_id].add(directory)

        manifest_path = f"{directory}/manifest.yaml"
        if manifest_path in head_paths:
            content = read_blob(head, manifest_path)
            if content is not None:
                for identity in manifest_identities(content, manifest_path):
                    claims[identity].add(directory)

    old_index = index_identities(read_blob(merge_base, INDEX))
    new_index = index_identities(read_blob(head, INDEX)) - old_index
    for identity in new_index:
        if not claims.get(identity):
            claims[identity].add(f"{INDEX}#{identity}")

    return claims


def check(base_ref: str, head_ref: str) -> int:
    try:
        base = resolve_commit(base_ref, "base")
        head = resolve_commit(head_ref, "candidate")
        merge_base = run_git("merge-base", base, head).decode(
            "ascii", errors="strict"
        ).strip().lower()
        if not re.fullmatch(r"[0-9a-f]{40}", merge_base):
            raise Incomplete("Git returned an invalid or empty merge-base")
        run_git("cat-file", "-e", f"{merge_base}^{{commit}}")

        base_paths = tree_paths(base)
        head_paths = tree_paths(head)
        introduced = introduced_directories(merge_base, head)
        occupied = occupied_identities(base, base_paths)
        claims = candidate_claims(head, merge_base, head_paths, introduced)

        violations: list[str] = []
        for identity, sources in sorted(claims.items()):
            directory_sources = {
                source for source in sources if source.startswith(ROOT + "/")
            }
            if identity in occupied:
                violations.append(
                    f"duplicate work-item identity '{identity}': candidate "
                    f"claim(s) {', '.join(sorted(sources))} already occupied "
                    f"on target {base}"
                )
            if len(directory_sources) > 1:
                violations.append(
                    f"candidate contains multiple directory claims for "
                    f"'{identity}': {', '.join(sorted(directory_sources))}"
                )

    except (Incomplete, UnicodeError) as exc:
        print(f"WORK-ITEM UNIQUENESS: INCOMPLETE ({exc})")
        return 2

    unique_violations = sorted(set(violations))
    for violation in unique_violations:
        print(f"::error::{violation}")

    if unique_violations:
        print(
            "WORK-ITEM UNIQUENESS: VIOLATION "
            f"(base={base} candidate={head} merge_base={merge_base} "
            f"introduced_directories={len(introduced)} "
            f"occupied_identities={len(occupied)} "
            f"violations={len(unique_violations)})"
        )
        return 1

    print(
        "WORK-ITEM UNIQUENESS: PASS "
        f"(base={base} candidate={head} merge_base={merge_base} "
        f"introduced_directories={len(introduced)} "
        f"occupied_identities={len(occupied)} violations=0)"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="full SHA of latest target commit")
    parser.add_argument("--head", help="full SHA of exact candidate commit")
    args = parser.parse_args(argv)

    missing = [
        option
        for option, value in (("--base", args.base), ("--head", args.head))
        if not value
    ]
    if missing:
        print(
            "WORK-ITEM UNIQUENESS: INCOMPLETE "
            f"(missing required ref(s): {', '.join(missing)})"
        )
        return 2

    return check(args.base, args.head)


if __name__ == "__main__":
    sys.exit(main())
