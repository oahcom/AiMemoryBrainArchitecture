#!/usr/bin/env python3
"""Resolve the base commit used by the current GitHub Actions candidate."""

import os
import re
import subprocess
import sys


class ResolutionError(Exception):
    pass


def git(*args):
    result = subprocess.run(
        ["git", *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or "git command failed"
        raise ResolutionError(detail)
    return result.stdout.strip()


def resolve():
    event_name = os.environ.get("GITHUB_EVENT_NAME", "")
    candidate = os.environ.get("GITHUB_SHA", "")

    if not re.fullmatch(r"[0-9a-fA-F]{40}", candidate):
        raise ResolutionError("GITHUB_SHA is missing or is not a full commit SHA")

    candidate = git("rev-parse", "--verify", f"{candidate}^{{commit}}")

    if event_name == "pull_request":
        event_ref = os.environ.get("GITHUB_REF", "")
        if not re.fullmatch(r"refs/pull/[1-9][0-9]*/merge", event_ref):
            raise ResolutionError(
                "pull_request requires GITHUB_REF=refs/pull/<number>/merge"
            )

        parents = git("rev-list", "--parents", "-n", "1", candidate).split()
        if len(parents) != 3:
            raise ResolutionError(
                "pull_request GITHUB_SHA is not a two-parent synthetic merge commit"
            )

        first_parent = parents[1]
        verified = git("rev-parse", "--verify", f"{first_parent}^{{commit}}")
        if verified != first_parent:
            raise ResolutionError("synthetic merge first parent did not resolve")

        return verified

    if event_name == "push":
        before = os.environ.get("GITHUB_EVENT_BEFORE", "")
        if not re.fullmatch(r"[0-9a-fA-F]{40}", before):
            raise ResolutionError(
                "push requires a full, non-zero GITHUB_EVENT_BEFORE commit SHA"
            )
        if set(before) == {"0"}:
            raise ResolutionError(
                "push before-SHA is the all-zero initial-branch sentinel"
            )

        verified = git("rev-parse", "--verify", f"{before}^{{commit}}")
        if verified != before.lower():
            raise ResolutionError(
                "GITHUB_EVENT_BEFORE did not resolve to the declared commit"
            )
        return verified

    raise ResolutionError(f"unsupported GitHub event: {event_name!r}")


def main():
    try:
        print(resolve())
        return 0
    except (ResolutionError, OSError) as exc:
        print(f"INCOMPLETE: cannot resolve manifest blob-pin base: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
