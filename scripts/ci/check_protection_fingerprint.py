#!/usr/bin/env python3
"""Fail-closed ratchet for the complete GitHub branch-protection endpoint."""

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

SCHEMA_VERSION = 3
DEFAULT_REPO = "oahcom/AiMemoryBrainArchitecture"
DEFAULT_BRANCH = "main"
DEFAULT_FINGERPRINT = "scripts/ci/baselines/protection-fingerprint.json"

BOOLEAN_DIRECTIONS = {
    # True means more protective.
    "strict": True,
    "enforce_admins": True,
    "required_linear_history": True,
    "block_creations": True,
    "required_conversation_resolution": True,
    "lock_branch": True,
    "required_signatures": True,
    # False means more protective.
    "allow_force_pushes": False,
    "allow_deletions": False,
    "allow_fork_syncing": False,
}

BOOLEAN_FIELDS = tuple(BOOLEAN_DIRECTIONS)
FINGERPRINT_FIELDS = (
    "strict",
    "contexts",
    "required_signatures",
    "enforce_admins",
    "required_linear_history",
    "allow_force_pushes",
    "allow_deletions",
    "block_creations",
    "required_conversation_resolution",
    "lock_branch",
    "allow_fork_syncing",
    "required_pull_request_reviews",
)


class IncompleteError(Exception):
    """The live payload or recorded baseline cannot be safely compared."""


class ApiError(Exception):
    """A GitHub API request failed with a known HTTP status."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def validate_bool(value: Any, field: str) -> bool:
    if type(value) is not bool:
        raise IncompleteError(f"{field} must be a boolean")
    return value


def extract_fingerprint(payload: Any) -> dict[str, Any]:
    """Extract the schema-v3 fingerprint from the unwrapped /protection payload."""
    if not isinstance(payload, dict):
        raise IncompleteError("live payload must be a JSON object")

    checks = payload.get("required_status_checks")
    if not isinstance(checks, dict):
        raise IncompleteError("required_status_checks must be an object")

    if "strict" not in checks:
        raise IncompleteError("required_status_checks.strict is missing")
    strict = validate_bool(checks["strict"], "required_status_checks.strict")

    contexts = checks.get("contexts")
    if not isinstance(contexts, list) or any(
        not isinstance(item, str) or not item for item in contexts
    ):
        raise IncompleteError("required_status_checks.contexts must be a list of non-empty strings")
    if len(contexts) != len(set(contexts)):
        raise IncompleteError("required_status_checks.contexts contains duplicates")

    result: dict[str, Any] = {
        "strict": strict,
        "contexts": sorted(contexts),
    }

    for field in BOOLEAN_FIELDS:
        if field == "strict":
            continue
        value = payload.get(field)
        if not isinstance(value, dict):
            raise IncompleteError(f"{field} must be an object")
        if "enabled" not in value:
            raise IncompleteError(f"{field}.enabled is missing")
        result[field] = validate_bool(value["enabled"], f"{field}.enabled")

    # Absence is an explicit, fingerprinted state. A present key must contain
    # an object; null or another type is not equivalent to absence.
    if "required_pull_request_reviews" not in payload:
        result["required_pull_request_reviews"] = None
    else:
        reviews = payload["required_pull_request_reviews"]
        if not isinstance(reviews, dict):
            raise IncompleteError("required_pull_request_reviews must be an object when present")
        try:
            # Round-trip to reject non-JSON values and produce a detached,
            # deterministic JSON-compatible object.
            result["required_pull_request_reviews"] = json.loads(
                json.dumps(reviews, sort_keys=True, ensure_ascii=False)
            )
        except (TypeError, ValueError) as exc:
            raise IncompleteError(f"required_pull_request_reviews is not JSON-compatible: {exc}") from exc

    if set(result) != set(FINGERPRINT_FIELDS):
        raise IncompleteError("internal fingerprint field set is incomplete")
    return result


def validate_baseline(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise IncompleteError("baseline must be a JSON object")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise IncompleteError(f"baseline schema_version must be {SCHEMA_VERSION}")

    fingerprint = data.get("fingerprint")
    if not isinstance(fingerprint, dict):
        raise IncompleteError("baseline fingerprint must be an object")
    if set(fingerprint) != set(FINGERPRINT_FIELDS):
        missing = sorted(set(FINGERPRINT_FIELDS) - set(fingerprint))
        extra = sorted(set(fingerprint) - set(FINGERPRINT_FIELDS))
        raise IncompleteError(f"baseline fingerprint field set invalid; missing={missing}, extra={extra}")

    if type(fingerprint["strict"]) is not bool:
        raise IncompleteError("baseline strict must be a boolean")
    if not isinstance(fingerprint["contexts"], list) or any(
        not isinstance(x, str) or not x for x in fingerprint["contexts"]
    ):
        raise IncompleteError("baseline contexts must be a list of non-empty strings")
    if len(fingerprint["contexts"]) != len(set(fingerprint["contexts"])):
        raise IncompleteError("baseline contexts contains duplicates")

    normalized = dict(fingerprint)
    normalized["contexts"] = sorted(normalized["contexts"])

    for field in BOOLEAN_FIELDS:
        if field == "strict":
            continue
        if type(normalized[field]) is not bool:
            raise IncompleteError(f"baseline {field} must be a boolean")

    reviews = normalized["required_pull_request_reviews"]
    if reviews is not None and not isinstance(reviews, dict):
        raise IncompleteError("baseline required_pull_request_reviews must be null or an object")

    experiment = data.get("experiment")
    required_experiment = ("pr", "head", "run", "date")
    if not isinstance(experiment, dict) or any(
        not isinstance(experiment.get(key), str) or not experiment[key].strip()
        for key in required_experiment
    ):
        raise IncompleteError("baseline experiment metadata is incomplete")

    return normalized


def load_baseline(path: str | Path) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IncompleteError(f"cannot read baseline: {exc}") from exc
    return validate_baseline(data)


def fetch_payload(repo: str, branch: str, token: str) -> dict[str, Any]:
    owner_repo = repo.split("/", 1)
    if len(owner_repo) != 2 or not all(owner_repo):
        raise IncompleteError("--repo must have the form owner/repository")

    owner, name = owner_repo
    url = (
        f"https://api.github.com/repos/{owner}/{name}/branches/"
        f"{urllib.parse.quote(branch, safe='')}/protection"
    )
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "protection-fingerprint-ratchet",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()
    except urllib.error.HTTPError as exc:
        raise ApiError(f"GitHub protection API HTTP {exc.code}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise ApiError(f"GitHub protection API transport error: {exc.reason}") from exc

    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise IncompleteError(f"GitHub protection API returned invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise IncompleteError("GitHub protection API response must be a JSON object")
    return payload


def classify_boolean(field: str, recorded: bool, live: bool) -> str:
    """Classify a boolean using its explicit protective polarity."""
    protective_value = BOOLEAN_DIRECTIONS[field]
    if recorded == live:
        return "UNCHANGED"
    if live == protective_value:
        return "TIGHTENED"
    return "LOOSENED"


def classify_contexts(recorded: list[str], live: list[str]) -> str:
    old, new = set(recorded), set(live)
    if old == new:
        return "UNCHANGED"
    if old < new:
        return "TIGHTENED"
    # Removal alone or additions mixed with removals are both loosening.
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

    # The approving-review count has a clear monotonic direction. Any other
    # review-policy mutation is conservatively classified as loosening:
    # this avoids silently accepting an ambiguous reduction in protection.
    old_count = recorded.get("required_approving_review_count")
    new_count = live.get("required_approving_review_count")
    if (
        type(old_count) is int
        and type(new_count) is int
        and old_count != new_count
    ):
        if new_count > old_count:
            return "TIGHTENED"
        return "LOOSENED"
    return "LOOSENED"


def classify_field(field: str, recorded: Any, live: Any) -> str:
    if field == "contexts":
        return classify_contexts(recorded, live)
    if field == "required_pull_request_reviews":
        return classify_reviews(recorded, live)
    if field in BOOLEAN_DIRECTIONS:
        return classify_boolean(field, recorded, live)
    raise IncompleteError(f"no direction rule for fingerprint field: {field}")


def stable_baseline_bytes(fingerprint: dict[str, Any], experiment: dict[str, str]) -> bytes:
    document = {
        "schema_version": SCHEMA_VERSION,
        "fingerprint": fingerprint,
        "experiment": experiment,
    }
    return (json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def write_baseline(path: str | Path, fingerprint: dict[str, Any], experiment: dict[str, str]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    content = stable_baseline_bytes(fingerprint, experiment)
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


def format_value(value: Any) -> str:
    if value is None:
        return "null"
    return canonical_json(value)


def compare(recorded: dict[str, Any], live: dict[str, Any]) -> tuple[int, int, int]:
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
            print(f"NOTICE: {field} tightened; review and synchronize the fingerprint baseline.")
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
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--experiment-pr")
    parser.add_argument("--experiment-head")
    parser.add_argument("--experiment-run")
    parser.add_argument("--experiment-date")
    return parser


def main(
    argv: list[str] | None = None,
    payload_fetcher: Callable[[str, str, str], dict[str, Any]] = fetch_payload,
    environ: dict[str, str] | None = None,
) -> int:
    args = build_parser().parse_args(argv)
    env = os.environ if environ is None else environ
    token = env.get("GITHUB_TOKEN", "").strip()
    if not token:
        print("INCOMPLETE: GITHUB_TOKEN is required", file=sys.stderr)
        return 2

    experiment_values = {
        "pr": args.experiment_pr,
        "head": args.experiment_head,
        "run": args.experiment_run,
        "date": args.experiment_date,
    }
    if args.write and any(not isinstance(value, str) or not value.strip()
                          for value in experiment_values.values()):
        print("INCOMPLETE: --write requires --experiment-pr, --experiment-head, "
              "--experiment-run, and --experiment-date", file=sys.stderr)
        return 2

    try:
        payload = payload_fetcher(args.repo, args.branch, token)
        live = extract_fingerprint(payload)
        if args.write:
            write_baseline(args.fingerprint, live, experiment_values)  # type: ignore[arg-type]
            print(f"PROTECTION FINGERPRINT: baseline written ({args.fingerprint})")
            return 0
        recorded = load_baseline(args.fingerprint)
    except ApiError as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2
    except IncompleteError as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # fail closed on unexpected runtime/IO errors
        print(f"INCOMPLETE: unexpected checker error: {exc}", file=sys.stderr)
        return 2

    try:
        _, loosened, _ = compare(recorded, live)
    except IncompleteError as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2
    return 1 if loosened else 0


if __name__ == "__main__":
    raise SystemExit(main())
