#!/usr/bin/env python3
"""Ratchet full GitHub branch protection, with a visible summary-endpoint fallback."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

SCHEMA_VERSION = 4
DEFAULT_REPO = "oahcom/AiMemoryBrainArchitecture"
DEFAULT_BRANCH = "main"
DEFAULT_FINGERPRINT = "scripts/ci/baselines/protection-fingerprint.json"

BOOLEAN_DIRECTIONS = {
    "strict": True,
    "required_signatures": True,
    "enforce_admins": True,
    "required_linear_history": True,
    "allow_force_pushes": False,
    "allow_deletions": False,
    "block_creations": True,
    "required_conversation_resolution": True,
    "lock_branch": True,
    "allow_fork_syncing": False,
}
BOOLEAN_FIELDS = tuple(BOOLEAN_DIRECTIONS)
FINGERPRINT_FIELDS = (
    "strict", "contexts", "required_signatures", "enforce_admins",
    "required_linear_history", "allow_force_pushes", "allow_deletions",
    "block_creations", "required_conversation_resolution", "lock_branch",
    "allow_fork_syncing", "required_pull_request_reviews",
)
UNVERIFIABLE_FIELDS = (
    "strict", "required_signatures", "enforce_admins",
    "required_linear_history", "allow_force_pushes", "allow_deletions",
    "block_creations", "required_conversation_resolution", "lock_branch",
    "allow_fork_syncing", "required_pull_request_reviews",
)
SUMMARY_FIELDS = ("enabled", "contexts", "enforcement_level")
ENFORCEMENT_RANK = {"off": 0, "non_admins": 1, "everyone": 2}
FALLBACK_HTTP_STATUSES = {401, 403, 404}


class IncompleteError(Exception):
    """The live payload or recorded baseline cannot be safely compared."""


class ApiError(Exception):
    """A GitHub API request failed with a known HTTP status."""

    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def validate_bool(value: Any, field: str) -> bool:
    if type(value) is not bool:
        raise IncompleteError(f"{field} must be a boolean")
    return value


def normalize_contexts(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item for item in value
    ):
        raise IncompleteError(f"{field} must be a list of non-empty strings")
    if len(value) != len(set(value)):
        raise IncompleteError(f"{field} contains duplicates")
    return sorted(value)


def extract_fingerprint(payload: Any) -> dict[str, Any]:
    """Extract the 12 schema-v3 fields from the /protection response root."""
    if not isinstance(payload, dict):
        raise IncompleteError("full endpoint payload must be a JSON object")
    checks = payload.get("required_status_checks")
    if not isinstance(checks, dict):
        raise IncompleteError("required_status_checks must be an object")
    if "strict" not in checks:
        raise IncompleteError("required_status_checks.strict is missing")

    result: dict[str, Any] = {
        "strict": validate_bool(checks["strict"], "required_status_checks.strict"),
        "contexts": normalize_contexts(
            checks.get("contexts"), "required_status_checks.contexts"
        ),
    }
    for field in BOOLEAN_FIELDS:
        if field == "strict":
            continue
        value = payload.get(field)
        if not isinstance(value, dict) or "enabled" not in value:
            raise IncompleteError(f"{field}.enabled is missing")
        result[field] = validate_bool(value["enabled"], f"{field}.enabled")

    if "required_pull_request_reviews" not in payload:
        result["required_pull_request_reviews"] = None
    else:
        reviews = payload["required_pull_request_reviews"]
        if not isinstance(reviews, dict):
            raise IncompleteError(
                "required_pull_request_reviews must be an object when present"
            )
        try:
            result["required_pull_request_reviews"] = json.loads(
                json.dumps(reviews, sort_keys=True, ensure_ascii=False)
            )
        except (TypeError, ValueError) as exc:
            raise IncompleteError(
                f"required_pull_request_reviews is not JSON-compatible: {exc}"
            ) from exc

    if set(result) != set(FINGERPRINT_FIELDS):
        raise IncompleteError("internal full fingerprint field set is incomplete")
    return result


def extract_summary_fingerprint(payload: Any) -> dict[str, Any]:
    """Extract the three fields exposed by GET /branches/{branch}."""
    if not isinstance(payload, dict):
        raise IncompleteError("summary endpoint payload must be a JSON object")
    protection = payload.get("protection")
    if not isinstance(protection, dict) or "enabled" not in protection:
        raise IncompleteError("protection.enabled is missing")
    checks = protection.get("required_status_checks")
    if not isinstance(checks, dict):
        raise IncompleteError("protection.required_status_checks must be an object")
    if "enforcement_level" not in checks:
        raise IncompleteError(
            "protection.required_status_checks.enforcement_level is missing"
        )
    enforcement = checks["enforcement_level"]
    if enforcement not in ENFORCEMENT_RANK:
        raise IncompleteError(f"unknown enforcement_level: {enforcement!r}")
    return {
        "enabled": validate_bool(protection["enabled"], "protection.enabled"),
        "contexts": normalize_contexts(
            checks.get("contexts"), "protection.required_status_checks.contexts"
        ),
        "enforcement_level": enforcement,
    }


def validate_baseline(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise IncompleteError("baseline must be a JSON object")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise IncompleteError(f"baseline schema_version must be {SCHEMA_VERSION}")

    fingerprint = data.get("fingerprint")
    if not isinstance(fingerprint, dict) or set(fingerprint) != set(FINGERPRINT_FIELDS):
        raise IncompleteError(
            "baseline fingerprint must contain exactly the 12 schema-v3 fields"
        )
    if type(fingerprint["strict"]) is not bool:
        raise IncompleteError("baseline strict must be a boolean")
    normalized_full = dict(fingerprint)
    normalized_full["contexts"] = normalize_contexts(
        fingerprint["contexts"], "baseline contexts"
    )
    for field in BOOLEAN_FIELDS:
        if field != "strict" and type(fingerprint[field]) is not bool:
            raise IncompleteError(f"baseline {field} must be a boolean")
    reviews = fingerprint["required_pull_request_reviews"]
    if reviews is not None and not isinstance(reviews, dict):
        raise IncompleteError(
            "baseline required_pull_request_reviews must be null or an object"
        )

    summary = data.get("summary_fingerprint")
    if not isinstance(summary, dict) or set(summary) != set(SUMMARY_FIELDS):
        raise IncompleteError(
            "baseline summary_fingerprint must contain exactly enabled, contexts, enforcement_level"
        )
    if type(summary["enabled"]) is not bool:
        raise IncompleteError("baseline summary enabled must be a boolean")
    if summary["enforcement_level"] not in ENFORCEMENT_RANK:
        raise IncompleteError("baseline summary enforcement_level is unknown")
    normalized_summary = dict(summary)
    normalized_summary["contexts"] = normalize_contexts(
        summary["contexts"], "baseline summary contexts"
    )

    experiment = data.get("experiment")
    required = ("pr", "head", "run", "date")
    if not isinstance(experiment, dict) or any(
        not isinstance(experiment.get(key), str) or not experiment[key].strip()
        for key in required
    ):
        raise IncompleteError("baseline experiment metadata is incomplete")
    return {
        "fingerprint": normalized_full,
        "summary_fingerprint": normalized_summary,
        "experiment": dict(experiment),
    }


def load_baseline_document(path: str | Path) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IncompleteError(f"cannot read baseline: {exc}") from exc
    return validate_baseline(data)


def load_baseline(path: str | Path) -> dict[str, Any]:
    """Compatibility helper: return the full 12-field fingerprint."""
    return load_baseline_document(path)["fingerprint"]


def _api_url(repo: str, branch: str, suffix: str = "") -> str:
    parts = repo.split("/", 1)
    if len(parts) != 2 or not all(parts):
        raise IncompleteError("--repo must have the form owner/repository")
    owner, name = parts
    return (
        f"https://api.github.com/repos/{owner}/{name}/branches/"
        f"{urllib.parse.quote(branch, safe='')}{suffix}"
    )


def _request_json(url: str, token: str, label: str) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "protection-fingerprint-ratchet",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()
    except urllib.error.HTTPError as exc:
        raise ApiError(
            f"GitHub {label} API HTTP {exc.code}: {exc.reason}", exc.code
        ) from exc
    except urllib.error.URLError as exc:
        raise ApiError(f"GitHub {label} API transport error: {exc.reason}") from exc
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise IncompleteError(
            f"GitHub {label} API returned invalid JSON: {exc}"
        ) from exc
    if not isinstance(payload, dict):
        raise IncompleteError(f"GitHub {label} API response must be a JSON object")
    return payload


def fetch_payload(repo: str, branch: str, token: str) -> dict[str, Any]:
    return _request_json(_api_url(repo, branch, "/protection"), token, "protection")


def fetch_summary_payload(repo: str, branch: str, token: str) -> dict[str, Any]:
    return _request_json(_api_url(repo, branch), token, "branch summary")


def classify_boolean(field: str, recorded: bool, live: bool) -> str:
    protective_value = BOOLEAN_DIRECTIONS[field]
    if recorded == live:
        return "UNCHANGED"
    return "TIGHTENED" if live == protective_value else "LOOSENED"


def classify_contexts(recorded: list[str], live: list[str]) -> str:
    old, new = set(recorded), set(live)
    if old == new:
        return "UNCHANGED"
    if old < new:
        return "TIGHTENED"
    return "LOOSENED"


def classify_reviews(recorded: Any, live: Any) -> str:
    if recorded is None and live is None:
        return "UNCHANGED"
    if recorded is None:
        return "TIGHTENED"
    if live is None:
        return "LOOSENED"
    if canonical_json(recorded) == canonical_json(live):
        return "UNCHANGED"
    old_count = recorded.get("required_approving_review_count")
    new_count = live.get("required_approving_review_count")
    if type(old_count) is int and type(new_count) is int and old_count != new_count:
        return "TIGHTENED" if new_count > old_count else "LOOSENED"
    return "LOOSENED"


def classify_field(field: str, recorded: Any, live: Any) -> str:
    if field == "contexts":
        return classify_contexts(recorded, live)
    if field == "required_pull_request_reviews":
        return classify_reviews(recorded, live)
    if field in BOOLEAN_DIRECTIONS:
        return classify_boolean(field, recorded, live)
    raise IncompleteError(f"no direction rule for fingerprint field: {field}")


def classify_enforcement(recorded: str, live: str) -> str:
    if recorded not in ENFORCEMENT_RANK or live not in ENFORCEMENT_RANK:
        raise IncompleteError("unknown enforcement_level")
    old, new = ENFORCEMENT_RANK[recorded], ENFORCEMENT_RANK[live]
    if old == new:
        return "UNCHANGED"
    return "TIGHTENED" if new > old else "LOOSENED"


def stable_baseline_bytes(
    fingerprint: dict[str, Any],
    experiment: dict[str, str],
    summary_fingerprint: dict[str, Any] | None = None,
) -> bytes:
    if summary_fingerprint is None:
        raise IncompleteError("schema-v4 writes require summary_fingerprint")
    document = {
        "schema_version": SCHEMA_VERSION,
        "fingerprint": fingerprint,
        "summary_fingerprint": summary_fingerprint,
        "experiment": experiment,
    }
    return (
        json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def _atomic_write(path: str | Path, content: bytes) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=str(destination.parent)
    )
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, destination)
    finally:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass


def write_baseline(
    path: str | Path,
    fingerprint: dict[str, Any],
    experiment: dict[str, str],
    summary_fingerprint: dict[str, Any] | None = None,
) -> None:
    if summary_fingerprint is None:
        raise IncompleteError("schema-v4 writes require summary_fingerprint")
    _atomic_write(
        path, stable_baseline_bytes(fingerprint, experiment, summary_fingerprint)
    )


def write_baseline_section(
    path: str | Path,
    section: str,
    live: dict[str, Any],
    experiment: dict[str, str],
) -> None:
    """Update one endpoint's section while preserving the other section's JSON value."""
    try:
        original = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IncompleteError(
            f"cannot read existing v4 baseline for partial write: {exc}"
        ) from exc
    validate_baseline(original)
    updated = dict(original)
    updated["schema_version"] = SCHEMA_VERSION
    updated[section] = live
    updated["experiment"] = dict(experiment)
    # Preserve the other section's value; only deterministic serialization changes formatting.
    if section == "fingerprint":
        updated["summary_fingerprint"] = original["summary_fingerprint"]
    else:
        updated["fingerprint"] = original["fingerprint"]
    _atomic_write(
        path,
        (
            json.dumps(updated, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        ).encode("utf-8"),
    )


def format_value(value: Any) -> str:
    return "null" if value is None else canonical_json(value)


def compare(
    recorded: dict[str, Any], live: dict[str, Any]
) -> tuple[int, int, int]:
    changed = loosened = tightened = 0
    for field in FINGERPRINT_FIELDS:
        old, new = recorded[field], live[field]
        direction = classify_field(field, old, new)
        print(
            f"FIELD {field}: recorded={format_value(old)} "
            f"live={format_value(new)} DIRECTION={direction}"
        )
        if direction != "UNCHANGED":
            changed += 1
        if direction == "LOOSENED":
            loosened += 1
        elif direction == "TIGHTENED":
            tightened += 1
            print(
                f"NOTICE: {field} tightened; review and synchronize the fingerprint baseline."
            )
    print(
        f"PROTECTION FINGERPRINT: {changed} field(s) changed, "
        f"{loosened} loosened, {tightened} tightened"
    )
    return changed, loosened, tightened


def compare_summary(
    recorded: dict[str, Any], live: dict[str, Any], degraded: bool
) -> tuple[int, int, int]:
    changed = loosened = tightened = 0
    for field in SUMMARY_FIELDS:
        old, new = recorded[field], live[field]
        if field == "enabled":
            direction = (
                "UNCHANGED" if old == new
                else ("TIGHTENED" if new else "LOOSENED")
            )
        elif field == "contexts":
            direction = classify_contexts(old, new)
        else:
            direction = classify_enforcement(old, new)
        print(
            f"FIELD {field}: recorded={format_value(old)} "
            f"live={format_value(new)} DIRECTION={direction}"
        )
        if direction != "UNCHANGED":
            changed += 1
        if direction == "LOOSENED":
            loosened += 1
        elif direction == "TIGHTENED":
            tightened += 1
            print(
                f"NOTICE: {field} tightened; review and synchronize the fingerprint baseline."
            )

    if degraded:
        for field in UNVERIFIABLE_FIELDS:
            print(
                f"UNVERIFIABLE {field} "
                "(requires Administration read on /protection)"
            )
        print(
            "NOTE: baseline fields not re-verified this run: "
            + ", ".join(UNVERIFIABLE_FIELDS)
        )
        print(
            "PROTECTION FINGERPRINT: DEGRADED MODE — "
            f"{len(SUMMARY_FIELDS)} field(s) verifiable, "
            f"{len(UNVERIFIABLE_FIELDS)} unverifiable"
        )
    else:
        print(
            f"PROTECTION FINGERPRINT: {changed} field(s) changed, "
            f"{loosened} loosened, {tightened} tightened"
        )
    return changed, loosened, tightened


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("--fingerprint", default=DEFAULT_FINGERPRINT)
    parser.add_argument(
        "--endpoint", choices=("auto", "full", "summary"), default="auto"
    )
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--experiment-pr")
    parser.add_argument("--experiment-head")
    parser.add_argument("--experiment-run")
    parser.add_argument("--experiment-date")
    return parser


def _write_live_baseline(
    path: str | Path,
    endpoint: str,
    live: dict[str, Any],
    experiment: dict[str, str],
    repo: str,
    branch: str,
    token: str,
    summary_payload_fetcher: Callable[[str, str, str], dict[str, Any]],
    payload_fetcher: Callable[[str, str, str], dict[str, Any]],
) -> None:
    """Write a section, creating a complete v4 baseline when the file is absent."""
    destination = Path(path)
    if destination.exists():
        section = "fingerprint" if endpoint == "full" else "summary_fingerprint"
        write_baseline_section(path, section, live, experiment)
        return

    # A schema-v4 baseline requires both independently sourced sections.
    # Never invent or infer the section not returned by the selected endpoint.
    if endpoint == "full":
        summary_payload = summary_payload_fetcher(repo, branch, token)
        summary_live = extract_summary_fingerprint(summary_payload)
        write_baseline(path, live, experiment, summary_live)
        return

    if not token:
        raise IncompleteError(
            "cannot create a complete schema-v4 baseline from the summary endpoint "
            "without a token that can read /protection"
        )
    full_payload = payload_fetcher(repo, branch, token)
    full_live = extract_fingerprint(full_payload)
    write_baseline(path, full_live, experiment, live)


def main(
    argv: list[str] | None = None,
    payload_fetcher: Callable[[str, str, str], dict[str, Any]] = fetch_payload,
    environ: dict[str, str] | None = None,
    summary_payload_fetcher: Callable[
        [str, str, str], dict[str, Any]
    ] = fetch_summary_payload,
) -> int:
    args = build_parser().parse_args(argv)
    env = os.environ if environ is None else environ
    token = env.get("GITHUB_TOKEN", "").strip()

    experiment = {
        "pr": args.experiment_pr,
        "head": args.experiment_head,
        "run": args.experiment_run,
        "date": args.experiment_date,
    }
    if args.write and any(
        not isinstance(value, str) or not value.strip()
        for value in experiment.values()
    ):
        print(
            "INCOMPLETE: --write requires --experiment-pr, --experiment-head, "
            "--experiment-run, and --experiment-date",
            file=sys.stderr,
        )
        return 2

    try:
        # Resolve the requested endpoint and fetch/validate its live payload before
        # touching the baseline. This keeps HTTP status semantics observable even
        # when the baseline path is absent or unreadable.
        endpoint = args.endpoint
        degraded = False
        live_full: dict[str, Any] | None = None
        live_summary: dict[str, Any] | None = None
        selected_endpoint: str

        if endpoint == "full":
            if not token:
                raise ApiError("GITHUB_TOKEN is required for --endpoint full")
            full_payload = payload_fetcher(args.repo, args.branch, token)
            live_full = extract_fingerprint(full_payload)
            selected_endpoint = "full"

        elif endpoint == "summary":
            summary_payload = summary_payload_fetcher(args.repo, args.branch, token)
            live_summary = extract_summary_fingerprint(summary_payload)
            selected_endpoint = "summary"

        else:
            # auto: try the complete endpoint first; only auth/visibility statuses degrade.
            try:
                full_payload = payload_fetcher(args.repo, args.branch, token)
            except ApiError as exc:
                if exc.status not in FALLBACK_HTTP_STATUSES:
                    raise
                degraded = True
                print(
                    f"DEGRADED: /protection returned HTTP {exc.status}; "
                    "using the branch summary endpoint."
                )
                summary_payload = summary_payload_fetcher(
                    args.repo, args.branch, token
                )
                live_summary = extract_summary_fingerprint(summary_payload)
                selected_endpoint = "summary"
            else:
                live_full = extract_fingerprint(full_payload)
                selected_endpoint = "full"

        # A write to a missing path is allowed. The first baseline still must be
        # schema v4 complete: both endpoint sections must have been observed.
        if args.write:
            _write_live_baseline(
                args.fingerprint,
                selected_endpoint,
                live_full if selected_endpoint == "full" else live_summary,
                experiment,
                args.repo,
                args.branch,
                token,
                summary_payload_fetcher,
                payload_fetcher,
            )
            if selected_endpoint == "full":
                print(
                    f"PROTECTION FINGERPRINT: full baseline written ({args.fingerprint})"
                )
            elif degraded:
                print(
                    f"PROTECTION FINGERPRINT: degraded summary baseline written ({args.fingerprint})"
                )
            else:
                print(
                    f"PROTECTION FINGERPRINT: summary baseline written ({args.fingerprint})"
                )
            return 0

        # Comparisons require the complete, validated v4 baseline. Read it only
        # after the live endpoint has been resolved and its payload validated.
        baseline = load_baseline_document(args.fingerprint)

        if selected_endpoint == "full":
            assert live_full is not None
            _, loosened, _ = compare(baseline["fingerprint"], live_full)
        else:
            assert live_summary is not None
            _, loosened, _ = compare_summary(
                baseline["summary_fingerprint"], live_summary, degraded
            )
        return 1 if loosened else 0

    except ApiError as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2
    except IncompleteError as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"INCOMPLETE: unexpected checker error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
