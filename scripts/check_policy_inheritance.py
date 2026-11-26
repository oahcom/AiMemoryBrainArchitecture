#!/usr/bin/env python3
"""Validate an inherited GOV-DOC-001 policy declaration.

The checker verifies the policy identity, approved version, source commit,
and actual policy blob resolved from that commit.

This is a repository-local validation mechanism. GitHub enforcement requires
a workflow to invoke it on the required events and branch protections to
require the resulting check.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


POLICY_ID = "GOV-DOC-001"
APPROVED_VERSION = "1.1"

SOURCE_COMMIT = (
    "c33a1bcd36f767c96f641d2a154f34d102ce2645"
)

SOURCE_PATH = (
    "00-governance/bilingual-documentation-policy.md"
)

APPROVED_BLOB = (
    "0e170479e1a71e8f4c124c6f1dc170241652f42b"
)

SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class ValidationError(Exception):
    """Raised when inheritance evidence is invalid."""


SHALLOW_HISTORY_ERROR = (
    "cannot verify policy inheritance provenance on a shallow clone; "
    "run git fetch --unshallow"
)


class ShallowRepositoryError(RuntimeError):
    """Raised when a pin cannot resolve because history is truncated."""


def git_history_is_shallow(repo: Path) -> bool:
    """Whether this clone holds truncated history. Fails closed if unknowable.

    Shallow history is not itself a defect: a clone deep enough to contain the
    pinned source commit answers correctly. It only matters once the pin fails
    to resolve, because then "absent here" and "never existed" are
    indistinguishable -- and calling that a content violation is a fabrication.
    """
    result = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--is-shallow-repository"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(
            "git rev-parse --is-shallow-repository failed: "
            f"{result.stderr.strip() or 'no diagnostic'}"
        )
    answer = result.stdout.strip().lower()
    if answer == "true":
        return True
    if answer == "false":
        return False
    raise RuntimeError(
        "Unable to determine whether the Git repository has complete history: "
        f"unexpected rev-parse output {result.stdout!r}"
    )


def git(repo: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.CalledProcessError as exc:
        raise ValidationError(
            f"Git verification failed: {' '.join(args)}"
        ) from exc

    return result.stdout.strip()


def validate_declaration(
    declaration: dict,
    repo: Path,
    shallow: bool = False,
) -> list[str]:
    errors: list[str] = []

    if not isinstance(declaration, dict):
        raise ValidationError(
            "Declaration must be a JSON object"
        )

    expected = {
        "policy_id": POLICY_ID,
        "inherited_version": APPROVED_VERSION,
        "source_commit": SOURCE_COMMIT,
        "source_path": SOURCE_PATH,
        "policy_blob_sha": APPROVED_BLOB,
    }

    for field, value in expected.items():
        actual = declaration.get(field)

        if actual != value:
            errors.append(
                f"{field}: expected {value!r}, "
                f"received {actual!r}"
            )

    commit = declaration.get("source_commit", "")
    blob = declaration.get("policy_blob_sha", "")

    if not isinstance(commit, str) or not SHA_RE.fullmatch(commit):
        errors.append("source_commit is not a valid full SHA-1")

    if not isinstance(blob, str) or not SHA_RE.fullmatch(blob):
        errors.append("policy_blob_sha is not a valid full SHA-1")

    if errors:
        return errors

    try:
        try:
            actual_commit = git(
                repo,
                "rev-parse",
                "--verify",
                f"{SOURCE_COMMIT}^{{commit}}",
            )
        except ValidationError:
            # The pin may exist upstream and simply lie below this clone's
            # horizon. Calling that a content violation would be a
            # fabrication, so truncated history is INCOMPLETE, not a failure.
            if shallow:
                raise ShallowRepositoryError(SHALLOW_HISTORY_ERROR) from None
            raise

        if actual_commit != SOURCE_COMMIT:
            errors.append(
                "Source Commit resolved to an unexpected object"
            )
            return errors

        actual_blob = git(
            repo,
            "rev-parse",
            f"{SOURCE_COMMIT}:{SOURCE_PATH}",
        )

        if actual_blob != APPROVED_BLOB:
            errors.append(
                f"Source Blob mismatch: expected {APPROVED_BLOB}, "
                f"received {actual_blob}"
            )

        object_type = git(
            repo,
            "cat-file",
            "-t",
            actual_blob,
        )

        if object_type != "blob":
            errors.append(
                "Resolved policy object is not a Git blob"
            )

    except ValidationError as exc:
        errors.append(str(exc))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--repo",
        default=".",
        help="Git repository path",
    )

    parser.add_argument(
        "--declaration",
        required=True,
        help="Inheritance declaration JSON file",
    )

    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    declaration_path = Path(args.declaration)

    if not declaration_path.is_absolute():
        declaration_path = repo / declaration_path

    if not declaration_path.is_file():
        print(
            f"FAIL: declaration file missing: "
            f"{declaration_path}",
            file=sys.stderr,
        )
        return 1

    try:
        shallow = git_history_is_shallow(repo)
    except RuntimeError as exc:
        print(
            f"::error::Unable to determine Git history completeness: {exc}",
            file=sys.stderr,
        )
        return 2

    try:
        declaration = json.loads(
            declaration_path.read_text(encoding="utf-8")
        )

        errors = validate_declaration(
            declaration,
            repo,
            shallow,
        )

    except ShallowRepositoryError as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2

    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)

        print("POLICY INHERITANCE: FAIL")
        return 1

    print("Policy ID: PASS")
    print("Approved version: PASS")
    print("Source Commit SHA: PASS")
    print("Source Blob SHA: PASS")
    print("Git object verification: PASS")
    print("POLICY INHERITANCE: PASS")

    return 0


if __name__ == "__main__":
    sys.exit(main())
