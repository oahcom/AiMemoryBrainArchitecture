#!/usr/bin/env python3
"""Verify that every declared required check actually ran on a PR's exact head.

Verdicts:
    EXECUTED   all required contexts completed successfully on the head
    ABSENT     at least one required context has no check run on the head
    STALE      GitHub reports mergeable_state=dirty
    FAILED     a latest required check run completed without success
    INCOMPLETE required evidence could not be read or is still pending

Exit codes:
    0 EXECUTED
    1 ABSENT / STALE / FAILED
    2 INCOMPLETE
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

DEFAULT_REPO = "oahcom/AiMemoryBrainArchitecture"
DEFAULT_API = "https://api.github.com"
TIMEOUT_SECONDS = 20
DOC_PATH = Path("14-ai-development/PR-GOVERNANCE-001.md")
MARKER = "<!-- declared-check-contexts"
FENCE_RE = re.compile(r"^```")

EXIT_CODES = {
    "EXECUTED": 0,
    "ABSENT": 1,
    "STALE": 1,
    "FAILED": 1,
    "INCOMPLETE": 2,
}


class IncompleteError(Exception):
    """Required evidence could not be established."""


def declared_contexts(doc_text: str) -> list[str]:
    """Parse the same fenced declaration used by check_declared_check_contexts.py."""
    lines = doc_text.splitlines()

    start = next(
        (
            i for i, line in enumerate(lines)
            if line.lstrip().startswith(MARKER)
        ),
        None,
    )
    if start is None:
        raise IncompleteError(
            f"declaration marker missing in {DOC_PATH}"
        )

    opening = next(
        (
            i for i in range(start, len(lines))
            if FENCE_RE.match(lines[i])
        ),
        None,
    )
    if opening is None:
        raise IncompleteError(
            f"declaration opening fence missing in {DOC_PATH}"
        )

    contexts = []
    closing_found = False

    for line in lines[opening + 1:]:
        if FENCE_RE.match(line):
            closing_found = True
            break
        name = line.strip()
        if name:
            contexts.append(name)

    if not closing_found or not contexts:
        raise IncompleteError(
            f"declaration fence is incomplete or empty in {DOC_PATH}"
        )

    if len(contexts) != len(set(contexts)):
        raise IncompleteError(
            f"duplicate required contexts in {DOC_PATH}"
        )

    return contexts


def _api_get(path: str, token: str) -> dict[str, Any]:
    """GET a GitHub REST API endpoint. Kept injectable for offline tests."""
    request = urllib.request.Request(
        f"{os.environ.get('GITHUB_API_URL', DEFAULT_API).rstrip('/')}/{path.lstrip('/')}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "required-context-execution-audit",
        },
    )

    with urllib.request.urlopen(
        request, timeout=TIMEOUT_SECONDS
    ) as response:
        payload = json.load(response)

    if not isinstance(payload, dict):
        raise IncompleteError("GitHub API returned a non-object payload")

    return payload


def _result(
    verdict: str,
    head_sha: str | None = None,
    mergeable_state: str | None = None,
    missing: list[str] | None = None,
    failed: list[str] | None = None,
    pending: list[str] | None = None,
    stale: list[str] | None = None,
    retries_used: int = 0,
    checks: list[dict[str, Any]] | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    return {
        "verdict": verdict,
        "head_sha": head_sha,
        "mergeable_state": mergeable_state,
        "missing": missing or [],
        "failed": failed or [],
        "pending": pending or [],
        "stale": stale or [],
        "retries_used": retries_used,
        "checks": checks or [],
        "error": error,
    }


def evaluate(
    pr: int,
    repo: str = DEFAULT_REPO,
    token: str | None = None,
    retries: int = 5,
    retry_delay: float = 5.0,
    root: Path | None = None,
    api_get: Callable[[str, str], dict[str, Any]] | None = None,
    sleep: Callable[[float], None] | None = None,
) -> dict[str, Any]:
    """Evaluate one PR. API and sleep dependencies are injectable."""
    api_get = api_get or _api_get
    sleep = sleep or time.sleep

    if not token:
        return _result(
            "INCOMPLETE",
            error="GITHUB_TOKEN or GH_TOKEN is required",
        )

    if retries < 0 or retry_delay < 0:
        return _result(
            "INCOMPLETE",
            error="retries and retry-delay must be non-negative",
        )

    try:
        doc_path = (root or Path(__file__).resolve().parents[2]) / DOC_PATH
        contexts = declared_contexts(
            doc_path.read_text(encoding="utf-8")
        )
    except Exception as exc:
        return _result(
            "INCOMPLETE",
            error=f"cannot read required contexts: {type(exc).__name__}: {exc}",
        )

    retries_used = 0

    try:
        pr_data = api_get(f"repos/{repo}/pulls/{pr}", token)

        if not isinstance(pr_data.get("head"), dict):
            raise IncompleteError("PR response has no valid head object")

        head_sha = pr_data["head"].get("sha")
        mergeable_state = pr_data.get("mergeable_state")

        if not isinstance(head_sha, str) or not head_sha:
            raise IncompleteError("PR response has no head.sha")

        # GitHub mergeability is lazily computed. Unknown is never evidence.
        while mergeable_state == "unknown" and retries_used < retries:
            sleep(retry_delay)
            retries_used += 1

            pr_data = api_get(f"repos/{repo}/pulls/{pr}", token)

            if not isinstance(pr_data.get("head"), dict):
                raise IncompleteError("PR response has no valid head object")

            # A changing head invalidates the original observation.
            refreshed_sha = pr_data["head"].get("sha")
            if refreshed_sha != head_sha:
                raise IncompleteError(
                    "PR head changed while waiting for mergeability"
                )

            mergeable_state = pr_data.get("mergeable_state")

        if mergeable_state == "unknown":
            return _result(
                "INCOMPLETE",
                head_sha=head_sha,
                mergeable_state=mergeable_state,
                retries_used=retries_used,
                error="mergeable_state remained unknown after retries",
            )

        if not isinstance(mergeable_state, str) or not mergeable_state:
            raise IncompleteError(
                "PR response has no valid mergeable_state"
            )

        # Dirty means this head cannot be dispatched through the normal
        # integration path. Existing check runs cannot establish execution
        # for this head under the requested contract.
        if mergeable_state == "dirty":
            return _result(
                "STALE",
                head_sha=head_sha,
                mergeable_state=mergeable_state,
                stale=list(contexts),
                retries_used=retries_used,
            )

        response = api_get(
            f"repos/{repo}/commits/{head_sha}/check-runs?per_page=100",
            token,
        )

        runs = response.get("check_runs")
        if not isinstance(runs, list):
            raise IncompleteError(
                "check-runs response has no valid check_runs list"
            )

        latest_by_name: dict[str, dict[str, Any]] = {}

        for run in runs:
            if not isinstance(run, dict):
                raise IncompleteError("check_runs contains a non-object entry")

            name = run.get("name")
            if not isinstance(name, str):
                raise IncompleteError("check run has no valid name")

            started_at = run.get("started_at")
            if started_at is not None and not isinstance(started_at, str):
                raise IncompleteError(
                    f"invalid started_at for check run {name!r}"
                )

            previous = latest_by_name.get(name)

            # API response ordering is not guaranteed. Compare timestamps,
            # never list position.
            if (
                previous is None
                or (started_at or "") > (previous.get("started_at") or "")
            ):
                latest_by_name[name] = run

        missing: list[str] = []
        failed: list[str] = []
        pending: list[str] = []
        check_details: list[dict[str, Any]] = []

        for name in contexts:
            run = latest_by_name.get(name)

            if run is None:
                missing.append(name)
                check_details.append({
                    "name": name,
                    "status": None,
                    "conclusion": None,
                    "started_at": None,
                    "run_id": None,
                })
                continue

            status = run.get("status")
            conclusion = run.get("conclusion")
            started_at = run.get("started_at")
            run_id = run.get("id")

            check_details.append({
                "name": name,
                "status": status,
                "conclusion": conclusion,
                "started_at": started_at,
                "run_id": run_id,
            })

            if status != "completed":
                pending.append(name)
            elif conclusion != "success":
                failed.append(name)

        # A missing context takes precedence over pending and failed runs.
        # This keeps "never ran" distinct from "ran but failed".
        if missing:
            verdict = "ABSENT"
        elif pending:
            verdict = "INCOMPLETE"
        elif failed:
            verdict = "FAILED"
        else:
            verdict = "EXECUTED"

        return _result(
            verdict,
            head_sha=head_sha,
            mergeable_state=mergeable_state,
            missing=missing,
            failed=failed,
            pending=pending,
            retries_used=retries_used,
            checks=check_details,
        )

    except Exception as exc:
        return _result(
            "INCOMPLETE",
            head_sha=locals().get("head_sha"),
            mergeable_state=locals().get("mergeable_state"),
            retries_used=retries_used,
            error=f"{type(exc).__name__}: {exc}",
        )


def print_human(result: dict[str, Any]) -> None:
    print(f"Verdict: {result['verdict']}")
    print(f"Head SHA: {result['head_sha'] or 'UNAVAILABLE'}")
    print(
        "Mergeable state: "
        f"{result['mergeable_state'] or 'UNAVAILABLE'}"
    )
    print(f"Retries used: {result['retries_used']}")
    print()

    for check in result["checks"]:
        print(
            f"{check['name']} | "
            f"status={check['status'] or 'ABSENT'} | "
            f"conclusion={check['conclusion'] or 'NONE'} | "
            f"started_at={check['started_at'] or 'NONE'} | "
            f"run_id={check['run_id'] if check['run_id'] is not None else 'NONE'}"
        )

    for category in ("missing", "pending", "failed", "stale"):
        values = result[category]
        if values:
            print(f"{category.upper()}: {', '.join(values)}")

    if result["error"]:
        print(f"Error: {result['error']}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit actual execution of all required PR check contexts."
    )
    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--retry-delay", type=float, default=5.0)

    args = parser.parse_args(argv)

    if args.pr <= 0:
        parser.error("--pr must be a positive integer")

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

    result = evaluate(
        pr=args.pr,
        repo=args.repo,
        token=token,
        retries=args.retries,
        retry_delay=args.retry_delay,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human(result)

    return EXIT_CODES[result["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
