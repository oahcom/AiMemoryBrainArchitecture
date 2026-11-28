#!/usr/bin/env python3
"""Verify actual execution of required PR check contexts on an exact head.

Verdicts:
    EXECUTED    all required contexts completed successfully
    ABSENT      a required context has no run after the freshness window
    STALE       GitHub reports mergeable_state=dirty
    FAILED      a latest completed run has a non-success conclusion
    INCOMPLETE  execution is not yet established or evidence is unavailable

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
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

DEFAULT_REPO = "oahcom/AiMemoryBrainArchitecture"
DEFAULT_API = "https://api.github.com"
TIMEOUT_SECONDS = 20
DEFAULT_MIN_AGE_SECONDS = 600
DOC_PATH = Path("14-ai-development/PR-GOVERNANCE-001.md")
MARKER = "<!-- declared-check-contexts"
FENCE_RE = re.compile(r"^```")

SCHEDULABLE_STATES = {"clean", "unstable", "behind", "blocked"}

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
    """Parse the canonical fenced declaration."""
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
    """GET a GitHub REST API endpoint. Injectable for offline tests."""
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
        raise IncompleteError(
            "GitHub API returned a non-object payload"
        )

    return payload


def _parse_timestamp(value: Any) -> datetime | None:
    """Parse an ISO-8601 timestamp into an aware UTC datetime."""
    if not isinstance(value, str) or not value:
        return None

    try:
        parsed = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def _head_age(
    repo: str,
    pr: int,
    sha: str,
    pr_data: dict[str, Any],
    token: str,
    api_get: Callable[[str, str], dict[str, Any]],
    now: datetime,
) -> tuple[float | None, str | None]:
    """Get head age from commit date, falling back to PR updated_at."""
    commit_date = None

    try:
        commit_data = api_get(
            f"repos/{repo}/commits/{sha}",
            token,
        )
        commit = commit_data.get("commit")
        if isinstance(commit, dict):
            committer = commit.get("committer")
            if isinstance(committer, dict):
                commit_date = _parse_timestamp(
                    committer.get("date")
                )
    except Exception:
        # A commit endpoint failure does not itself make the audit
        # incomplete if the PR updated_at fallback is available.
        commit_date = None

    if commit_date is not None:
        source = "commit.committer.date"
        timestamp = commit_date
    else:
        timestamp = _parse_timestamp(pr_data.get("updated_at"))
        source = "pull.updated_at"

    if timestamp is None:
        return None, None

    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)

    age = max(
        0.0,
        (now.astimezone(timezone.utc) - timestamp).total_seconds(),
    )

    return age, source


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
    head_age_seconds: float | None = None,
    head_age_source: str | None = None,
    reason: str | None = None,
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
        "head_age_seconds": head_age_seconds,
        "head_age_source": head_age_source,
        "reason": reason,
        "error": error,
    }


def evaluate(
    pr: int,
    repo: str = DEFAULT_REPO,
    token: str | None = None,
    retries: int = 5,
    retry_delay: float = 5.0,
    min_age_seconds: float = DEFAULT_MIN_AGE_SECONDS,
    root: Path | None = None,
    api_get: Callable[[str, str], dict[str, Any]] | None = None,
    sleep: Callable[[float], None] | None = None,
    now: Callable[[], datetime] | None = None,
) -> dict[str, Any]:
    """Evaluate one PR with injectable API, clock and sleep dependencies."""
    api_get = api_get or _api_get
    sleep = sleep or time.sleep
    now = now or (lambda: datetime.now(timezone.utc))

    if not token:
        return _result(
            "INCOMPLETE",
            reason="api-error",
            error="GITHUB_TOKEN or GH_TOKEN is required",
        )

    if (
        retries < 0
        or retry_delay < 0
        or min_age_seconds < 0
    ):
        return _result(
            "INCOMPLETE",
            reason="api-error",
            error=(
                "retries, retry-delay and min-age-seconds "
                "must be non-negative"
            ),
        )

    try:
        doc_path = (
            root or Path(__file__).resolve().parents[2]
        ) / DOC_PATH

        contexts = declared_contexts(
            doc_path.read_text(encoding="utf-8")
        )
    except Exception as exc:
        return _result(
            "INCOMPLETE",
            reason="api-error",
            error=(
                f"cannot read required contexts: "
                f"{type(exc).__name__}: {exc}"
            ),
        )

    retries_used = 0
    head_sha = None
    mergeable_state = None
    pr_data = None

    try:
        pr_path = f"repos/{repo}/pulls/{pr}"
        pr_data = api_get(pr_path, token)

        if not isinstance(pr_data.get("head"), dict):
            raise IncompleteError(
                "PR response has no valid head object"
            )

        head_sha = pr_data["head"].get("sha")
        mergeable_state = pr_data.get("mergeable_state")

        if not isinstance(head_sha, str) or not head_sha:
            raise IncompleteError("PR response has no head.sha")

        # Unknown is a lazy GitHub mergeability computation state,
        # never evidence of execution or staleness.
        while mergeable_state == "unknown" and retries_used < retries:
            sleep(retry_delay)
            retries_used += 1

            pr_data = api_get(pr_path, token)

            if not isinstance(pr_data.get("head"), dict):
                raise IncompleteError(
                    "PR response has no valid head object"
                )

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
                reason="unknown-state",
                error="mergeable_state remained unknown after retries",
            )

        if not isinstance(mergeable_state, str) or not mergeable_state:
            raise IncompleteError(
                "PR response has no valid mergeable_state"
            )

        # Dirty takes precedence over all run and freshness results.
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
                raise IncompleteError(
                    "check_runs contains a non-object entry"
                )

            name = run.get("name")

            if not isinstance(name, str):
                raise IncompleteError(
                    "check run has no valid name"
                )

            started_at = run.get("started_at")

            if (
                started_at is not None
                and not isinstance(started_at, str)
            ):
                raise IncompleteError(
                    f"invalid started_at for check run {name!r}"
                )

            previous = latest_by_name.get(name)

            # Do not rely on API response ordering.
            if (
                previous is None
                or (started_at or "")
                > (previous.get("started_at") or "")
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

        # Missing execution is ambiguous until the head is old enough.
        if missing:
            age, age_source = _head_age(
                repo=repo,
                pr=pr,
                sha=head_sha,
                pr_data=pr_data,
                token=token,
                api_get=api_get,
                now=now(),
            )

            if age is None:
                return _result(
                    "INCOMPLETE",
                    head_sha=head_sha,
                    mergeable_state=mergeable_state,
                    missing=missing,
                    failed=failed,
                    pending=pending,
                    retries_used=retries_used,
                    checks=check_details,
                    reason="api-error",
                    error="cannot determine head age from commit date or PR updated_at",
                )

            if (
                age < min_age_seconds
                and mergeable_state in SCHEDULABLE_STATES
            ):
                return _result(
                    "INCOMPLETE",
                    head_sha=head_sha,
                    mergeable_state=mergeable_state,
                    missing=missing,
                    failed=failed,
                    pending=pending,
                    retries_used=retries_used,
                    checks=check_details,
                    head_age_seconds=age,
                    head_age_source=age_source,
                    reason="not-yet-scheduled",
                )

            return _result(
                "ABSENT",
                head_sha=head_sha,
                mergeable_state=mergeable_state,
                missing=missing,
                failed=failed,
                pending=pending,
                retries_used=retries_used,
                checks=check_details,
                head_age_seconds=age,
                head_age_source=age_source,
            )

        if pending:
            return _result(
                "INCOMPLETE",
                head_sha=head_sha,
                mergeable_state=mergeable_state,
                pending=pending,
                retries_used=retries_used,
                checks=check_details,
                reason="pending",
            )

        if failed:
            return _result(
                "FAILED",
                head_sha=head_sha,
                mergeable_state=mergeable_state,
                failed=failed,
                retries_used=retries_used,
                checks=check_details,
            )

        return _result(
            "EXECUTED",
            head_sha=head_sha,
            mergeable_state=mergeable_state,
            retries_used=retries_used,
            checks=check_details,
        )

    except Exception as exc:
        return _result(
            "INCOMPLETE",
            head_sha=head_sha,
            mergeable_state=mergeable_state,
            retries_used=retries_used,
            reason="api-error",
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

    if result["head_age_seconds"] is not None:
        print(
            f"Head age: {result['head_age_seconds']:.1f}s "
            f"(source={result['head_age_source']})"
        )

    if result["reason"]:
        print(f"Reason: {result['reason']}")

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
        description=(
            "Audit actual execution of all required PR check contexts."
        )
    )

    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--retry-delay", type=float, default=5.0)
    parser.add_argument(
        "--min-age-seconds",
        type=float,
        default=DEFAULT_MIN_AGE_SECONDS,
        help="Minimum head age before missing contexts become ABSENT (default: 600)",
    )

    args = parser.parse_args(argv)

    if args.pr <= 0:
        parser.error("--pr must be a positive integer")

    if (
        args.retries < 0
        or args.retry_delay < 0
        or args.min_age_seconds < 0
    ):
        parser.error(
            "--retries, --retry-delay and --min-age-seconds "
            "must be non-negative"
        )

    token = (
        os.environ.get("GITHUB_TOKEN")
        or os.environ.get("GH_TOKEN")
    )

    result = evaluate(
        pr=args.pr,
        repo=args.repo,
        token=token,
        retries=args.retries,
        retry_delay=args.retry_delay,
        min_age_seconds=args.min_age_seconds,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human(result)

    return EXIT_CODES[result["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
