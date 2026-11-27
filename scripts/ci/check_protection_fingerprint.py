#!/usr/bin/env python3
"""Fail-closed protection fingerprint ratchet.

Reads exclusively:
GET /repos/{owner}/{repo}/branches/{branch}

The fingerprint covers only fields actually exposed by the branch endpoint:
- protection.enabled
- protection.required_status_checks.contexts
- protection.required_status_checks.enforcement_level

It deliberately does not call the /protection endpoint.

Exit codes:
    0: unchanged or tightened
    1: protection loosened
    2: incomplete, unreadable, unauthenticated, or invalid input
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_FINGERPRINT = (
    "scripts/ci/baselines/protection-fingerprint.json"
)

DEFAULT_API = "https://api.github.com"
TIMEOUT_SECONDS = 20
USER_AGENT = "protection-fingerprint-ratchet"
SCHEMA_VERSION = 2

# Higher values mean stricter enforcement.
ENFORCEMENT_LEVELS = {
    "off": 0,
    "non_admins": 1,
    "everyone": 2,
}

EXPERIMENT_FIELDS = (
    "experiment_pr",
    "experiment_head",
    "experiment_run",
    "experiment_date",
)


class IncompleteError(Exception):
    """The configuration cannot be established reliably."""


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )


def extract_fingerprint(payload: dict[str, Any]) -> dict[str, Any]:
    """Extract only fields actually present in the branch endpoint."""

    if not isinstance(payload, dict):
        raise IncompleteError("branch response is not an object")

    protection = payload.get("protection")

    if not isinstance(protection, dict):
        raise IncompleteError(
            "protection is missing or unreadable"
        )

    enabled = protection.get("enabled")

    if not isinstance(enabled, bool):
        raise IncompleteError(
            "protection.enabled is missing or not boolean"
        )

    checks = protection.get("required_status_checks")

    if not isinstance(checks, dict):
        raise IncompleteError(
            "protection.required_status_checks is missing or unreadable"
        )

    contexts = checks.get("contexts")

    if (
        not isinstance(contexts, list)
        or not all(
            isinstance(item, str) and item.strip()
            for item in contexts
        )
        or len(contexts) != len(set(contexts))
    ):
        raise IncompleteError(
            "required_status_checks.contexts must be a list "
            "of unique nonempty strings"
        )

    enforcement_level = checks.get("enforcement_level")

    if (
        not isinstance(enforcement_level, str)
        or enforcement_level not in ENFORCEMENT_LEVELS
    ):
        raise IncompleteError(
            "required_status_checks.enforcement_level is missing "
            "or has an unsupported value"
        )

    return {
        "enabled": enabled,
        "contexts": sorted(contexts),
        "enforcement_level": enforcement_level,
    }


def fetch_branch_payload(
    repo: str,
    branch: str,
    timeout: int = TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Fetch the GitHub branch object without using /protection."""

    token = os.environ.get("GITHUB_TOKEN")

    if not token:
        raise IncompleteError("GITHUB_TOKEN is not set")

    if not re.fullmatch(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",
        repo,
    ):
        raise IncompleteError(
            f"invalid repository slug: {repo!r}"
        )

    if not branch or "\n" in branch:
        raise IncompleteError("invalid branch name")

    api_base = os.environ.get(
        "GITHUB_API_URL",
        DEFAULT_API,
    ).rstrip("/")

    encoded_branch = urllib.parse.quote(
        branch,
        safe="",
    )

    url = (
        f"{api_base}/repos/{repo}/branches/{encoded_branch}"
    )

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
        ) as response:
            payload = json.load(response)

    except Exception as error:
        raise IncompleteError(
            f"branch API request failed: "
            f"{type(error).__name__}: {error}"
        ) from error

    if not isinstance(payload, dict):
        raise IncompleteError(
            "branch API returned a non-object payload"
        )

    return payload


def load_baseline(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(
            path.read_text(encoding="utf-8")
        )
    except Exception as error:
        raise IncompleteError(
            f"cannot read fingerprint {path}: {error}"
        ) from error

    if not isinstance(data, dict):
        raise IncompleteError(
            "fingerprint root must be an object"
        )

    if data.get("schema_version") != SCHEMA_VERSION:
        raise IncompleteError(
            f"unsupported fingerprint schema_version; "
            f"expected {SCHEMA_VERSION}"
        )

    protection = data.get("protection")

    if not isinstance(protection, dict):
        raise IncompleteError(
            "fingerprint protection object is missing"
        )

    try:
        normalized = extract_fingerprint({
            "protection": {
                "enabled": protection.get("enabled"),
                "required_status_checks": {
                    "contexts": protection.get("contexts"),
                    "enforcement_level": protection.get(
                        "enforcement_level"
                    ),
                },
            }
        })
    except IncompleteError as error:
        raise IncompleteError(
            f"invalid baseline protection: {error}"
        ) from error

    experiment = data.get("experiment")

    if not isinstance(experiment, dict):
        raise IncompleteError(
            "baseline experiment record is missing"
        )

    required = {"pr", "head", "run", "date", "result"}

    if not required.issubset(experiment):
        raise IncompleteError(
            "baseline experiment record is incomplete"
        )

    data["protection"] = normalized

    return data


def classify_field(
    field: str,
    recorded: Any,
    live: Any,
) -> str:
    """Classify one field as UNCHANGED, TIGHTENED or LOOSENED."""

    if canonical_json(recorded) == canonical_json(live):
        return "UNCHANGED"

    if field == "enabled":
        if not isinstance(recorded, bool) or not isinstance(live, bool):
            raise IncompleteError(
                "enabled must be boolean"
            )

        return "TIGHTENED" if live else "LOOSENED"

    if field == "contexts":
        if not isinstance(recorded, list) or not isinstance(live, list):
            raise IncompleteError(
                "contexts must be lists"
            )

        old = set(recorded)
        new = set(live)

        if old < new:
            return "TIGHTENED"

        if new < old:
            return "LOOSENED"

        # Simultaneous additions and removals are not pure tightening.
        return "LOOSENED"

    if field == "enforcement_level":
        if (
            recorded not in ENFORCEMENT_LEVELS
            or live not in ENFORCEMENT_LEVELS
        ):
            raise IncompleteError(
                "unknown enforcement_level"
            )

        if (
            ENFORCEMENT_LEVELS[live]
            > ENFORCEMENT_LEVELS[recorded]
        ):
            return "TIGHTENED"

        return "LOOSENED"

    raise IncompleteError(
        f"unknown fingerprint field: {field}"
    )


def compare_fingerprints(
    recorded: dict[str, Any],
    live: dict[str, Any],
) -> list[tuple[str, Any, Any, str]]:
    expected_fields = {
        "enabled",
        "contexts",
        "enforcement_level",
    }

    if set(recorded) != expected_fields:
        raise IncompleteError(
            "baseline does not contain exactly the supported fields"
        )

    if set(live) != expected_fields:
        raise IncompleteError(
            "live fingerprint does not contain exactly "
            "the supported fields"
        )

    differences = []

    for field in sorted(expected_fields):
        direction = classify_field(
            field,
            recorded[field],
            live[field],
        )

        if direction != "UNCHANGED":
            differences.append((
                field,
                recorded[field],
                live[field],
                direction,
            ))

    return differences


def make_experiment(
    args: argparse.Namespace,
) -> dict[str, Any]:
    values = (
        args.experiment_pr,
        args.experiment_head,
        args.experiment_run,
        args.experiment_date,
    )

    if any(value is None for value in values):
        raise IncompleteError(
            "--write requires all four parameters: "
            "--experiment-pr, --experiment-head, "
            "--experiment-run, --experiment-date"
        )

    if args.experiment_pr <= 0 or args.experiment_run <= 0:
        raise IncompleteError(
            "experiment PR and run must be positive integers"
        )

    if not re.fullmatch(
        r"[0-9a-f]{40}",
        args.experiment_head,
    ):
        raise IncompleteError(
            "experiment-head must be a full lowercase 40-character SHA"
        )

    if not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}",
        args.experiment_date,
    ):
        raise IncompleteError(
            "experiment-date must use YYYY-MM-DD"
        )

    return {
        "pr": args.experiment_pr,
        "head": args.experiment_head,
        "run": args.experiment_run,
        "date": args.experiment_date,
        "result": (
            "Failing required status check blocked the normal "
            "pull-request merge API path."
        ),
    }


def atomic_write(
    path: Path,
    data: dict[str, Any],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    content = (
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )

    temporary = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=path.name + ".",
            suffix=".tmp",
            delete=False,
        ) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())

        temporary.replace(path)

    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Compare GitHub branch protection with a committed "
            "protection fingerprint."
        )
    )

    parser.add_argument("--repo", required=True)
    parser.add_argument("--branch", default="main")
    parser.add_argument(
        "--fingerprint",
        default=DEFAULT_FINGERPRINT,
    )

    parser.add_argument(
        "--write",
        action="store_true",
    )

    parser.add_argument(
        "--experiment-pr",
        type=int,
    )
    parser.add_argument(
        "--experiment-head",
    )
    parser.add_argument(
        "--experiment-run",
        type=int,
    )
    parser.add_argument(
        "--experiment-date",
    )

    return parser


def main(
    argv: list[str] | None = None,
    *,
    payload_fetcher=None,
) -> int:
    args = build_parser().parse_args(argv)

    path = Path(args.fingerprint)

    experiment = None

    if args.write:
        try:
            experiment = make_experiment(args)
        except IncompleteError as error:
            print(
                f"INCOMPLETE: {error}",
                file=sys.stderr,
            )
            return 2

    try:
        payload = (
            payload_fetcher(args.repo, args.branch)
            if payload_fetcher is not None
            else fetch_branch_payload(
                args.repo,
                args.branch,
            )
        )

        live = extract_fingerprint(payload)

        if args.write:
            baseline = {
                "schema_version": SCHEMA_VERSION,
                "repository": args.repo,
                "branch": args.branch,
                "protection": live,
                "experiment": experiment,
            }

            atomic_write(path, baseline)

            print(
                f"PROTECTION FINGERPRINT: UPDATED {path}"
            )
            print(
                "PROTECTION FINGERPRINT: new experiment "
                "record attached"
            )
            return 0

        baseline = load_baseline(path)

        if baseline.get("repository") != args.repo:
            raise IncompleteError(
                "baseline repository does not match --repo"
            )

        if baseline.get("branch") != args.branch:
            raise IncompleteError(
                "baseline branch does not match --branch"
            )

        recorded = baseline["protection"]

        differences = compare_fingerprints(
            recorded,
            live,
        )

    except Exception as error:
        print(
            f"INCOMPLETE: protection fingerprint could not "
            f"be verified: {type(error).__name__}: {error}",
            file=sys.stderr,
        )
        return 2

    loosened = 0
    tightened = 0

    for field, old, new, direction in differences:
        if direction == "LOOSENED":
            loosened += 1
        elif direction == "TIGHTENED":
            tightened += 1

        print(
            f"FIELD {field}: "
            f"recorded={canonical_json(old)} "
            f"live={canonical_json(new)} "
            f"DIRECTION={direction}"
        )

    changed = len(differences)

    print(
        f"PROTECTION FINGERPRINT: "
        f"{changed} field(s) changed, "
        f"{loosened} loosened, "
        f"{tightened} tightened"
    )

    if loosened:
        print(
            "PROTECTION FINGERPRINT: VIOLATION; "
            "loosening requires a new failing-head experiment "
            "and reviewed baseline update",
            file=sys.stderr,
        )
        return 1

    if tightened:
        print(
            "NOTICE: protection tightened; synchronize the "
            "committed fingerprint through a reviewed --write operation"
        )
        return 0

    print("PROTECTION FINGERPRINT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
