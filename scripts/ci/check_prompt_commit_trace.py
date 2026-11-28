#!/usr/bin/env python3
"""Audit immutable prompt evidence and implementation-commit reachability.

TRACEABLE is deliberately strict: a matching prompt file at the audited HEAD
is not an execution-time pin. At least one immutable prompt pin must verify.
The audit population is every AID manifest in the selected Git tree.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
PLACEHOLDERS = {
    "", "PENDING", "NOT_STARTED", "NOT_VERIFIED", "NOT_RECORDED",
    "NOT_APPLICABLE", "N/A", "NULL", "NONE",
}
PRIMARY = (
    "NO_TRACE",
    "DIGEST_UNPINNED",
    "DIGEST_MISMATCH",
    "COMMIT_UNREACHABLE",
    "TRACEABLE",
)
PROMPT_DIMENSIONS = (
    "PINNED_OK", "HEAD_MATCH", "UNPINNED_MISMATCH", "ABSENT",
)
COMMIT_DIMENSIONS = ("REACHABLE", "UNREACHABLE", "ABSENT")
FINDINGS = (
    "digest_absent",
    "digest_not_verified",
    "digest_unpinned",
    "digest_head_mismatch",
    "digest_pinned_mismatch",
    "commit_absent",
    "commit_pending",
    "commit_unresolvable",
    "commit_unreachable",
    "commit_unexpected_for_lifecycle",
)
SEVERITY = {
    "TRACEABLE": 0,
    "COMMIT_UNREACHABLE": 1,
    "DIGEST_MISMATCH": 2,
    "DIGEST_UNPINNED": 3,
    "NO_TRACE": 4,
}


def git(root: Path, *args: str, check: bool = True) -> bytes:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and proc.returncode:
        raise RuntimeError(
            proc.stderr.decode("utf-8", "replace").strip()
            or f"git {' '.join(args)} exited {proc.returncode}"
        )
    return proc.stdout


def real(value: object) -> bool:
    return (
        isinstance(value, str)
        and value.strip().upper() not in PLACEHOLDERS
    )


def resolve_commit(root: Path, value: object) -> str | None:
    if not real(value) or not re.fullmatch(r"[0-9a-fA-F]{7,40}", str(value)):
        return None
    resolved = git(
        root, "rev-parse", "--verify", f"{value}^{{commit}}", check=False
    ).decode("ascii", "replace").strip().lower()
    return resolved if HEX40.fullmatch(resolved) else None


def is_ancestor(root: Path, ancestor: str | None, descendant: str | None) -> bool:
    if not ancestor or not descendant:
        return False
    proc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode not in (0, 1):
        raise RuntimeError(
            proc.stderr.decode("utf-8", "replace").strip()
            or "git merge-base --is-ancestor failed"
        )
    return proc.returncode == 0


def read_path_at_commit(
    root: Path, commit: str, path: object
) -> bytes | None:
    if not real(path):
        return None
    normalized = str(path).replace("\\", "/")
    if normalized.startswith("/") or ".." in Path(normalized).parts:
        raise ValueError(f"manifest path is not repository-relative: {path}")
    proc = subprocess.run(
        ["git", "show", f"{commit}:{normalized}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.stdout if proc.returncode == 0 else None


def read_git_blob(root: Path, oid: object) -> bytes | None:
    if not isinstance(oid, str) or not HEX40.fullmatch(oid.lower()):
        return None
    kind = git(root, "cat-file", "-t", oid, check=False).decode().strip()
    if kind != "blob":
        return None
    proc = subprocess.run(
        ["git", "cat-file", "blob", oid],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.stdout if proc.returncode == 0 else None


def manifest_paths(root: Path, commit: str) -> list[str]:
    names = git(
        root, "ls-tree", "-r", "--name-only", commit
    ).decode("utf-8", "replace").splitlines()
    return sorted(
        path for path in names
        if path.startswith("14-ai-development/work-items/")
        and path.endswith("/manifest.yaml")
    )


def classify_primary(
    digest_present: bool,
    implementation_present: bool,
    any_pin: bool,
    pinned_ok: bool,
    commit_reachable: bool,
) -> str:
    # This precedence is part of the public audit contract.
    if not digest_present or not implementation_present:
        return "NO_TRACE"
    if not any_pin:
        return "DIGEST_UNPINNED"
    if not pinned_ok:
        return "DIGEST_MISMATCH"
    if not commit_reachable:
        return "COMMIT_UNREACHABLE"
    return "TRACEABLE"


def audit(root: Path, commit_ref: str, base_ref: str) -> list[dict]:
    commit = resolve_commit(root, commit_ref)
    base = resolve_commit(root, base_ref)
    if not commit:
        raise RuntimeError(f"cannot resolve audit commit: {commit_ref}")
    if not base:
        raise RuntimeError(f"cannot resolve comparison base: {base_ref}")

    rows = []
    for manifest_path in manifest_paths(root, commit):
        raw = read_path_at_commit(root, commit, manifest_path)
        if raw is None:
            raise RuntimeError(f"cannot read manifest at {commit}: {manifest_path}")
        doc = yaml.safe_load(raw.decode("utf-8")) or {}
        if not isinstance(doc, dict):
            raise ValueError(f"{manifest_path}: manifest root is not a mapping")

        work_id = str(doc.get("work_item_id") or Path(manifest_path).parent.name)
        impl_section = doc.get("implementation") or {}
        if not isinstance(impl_section, dict):
            impl_section = {}

        digest = doc.get("prompt_sha256")
        prompt_path = doc.get("prompt_file")
        blob_pin = doc.get("prompt_file_blob_sha")
        prompt_commit_pin = doc.get("prompt_file_commit_sha")

        lifecycle = str(impl_section.get("status", "")).upper()
        implementation_sha = (
            impl_section.get("implementation_commit_sha")
            or doc.get("implementation_commit_sha")
        )
        merge_target = (
            impl_section.get("merge_commit_sha")
            or doc.get("merge_commit_sha")
        )
        findings: list[str] = []

        digest_valid = bool(
            real(digest)
            and isinstance(digest, str)
            and HEX64.fullmatch(digest.lower())
        )
        if not real(digest):
            findings.append(
                "digest_absent" if digest is None else "digest_not_verified"
            )
        elif not digest_valid:
            findings.append("digest_not_verified")

        has_blob_pin = real(blob_pin)
        has_commit_pin = real(prompt_commit_pin)
        has_any_pin = has_blob_pin or has_commit_pin
        if real(digest) and not has_any_pin:
            findings.append("digest_unpinned")

        head_bytes = read_path_at_commit(root, commit, prompt_path)
        head_match = bool(
            head_bytes is not None
            and digest_valid
            and hashlib.sha256(head_bytes).hexdigest() == digest.lower()
        )
        if real(digest) and not head_match:
            findings.append("digest_head_mismatch")

        pin_results = []
        if has_blob_pin:
            pinned_bytes = read_git_blob(root, blob_pin)
            pin_results.append(
                pinned_bytes is not None
                and digest_valid
                and hashlib.sha256(pinned_bytes).hexdigest() == digest.lower()
            )

        if has_commit_pin:
            pin_commit = resolve_commit(root, prompt_commit_pin)
            pinned_path_bytes = (
                read_path_at_commit(root, pin_commit, prompt_path)
                if pin_commit else None
            )
            pin_results.append(
                pinned_path_bytes is not None
                and digest_valid
                and hashlib.sha256(pinned_path_bytes).hexdigest() == digest.lower()
            )
            if has_blob_pin and pin_commit and real(prompt_path):
                commit_blob = git(
                    root, "rev-parse", "--verify",
                    f"{pin_commit}:{prompt_path}", check=False,
                ).decode("ascii", "replace").strip().lower()
                if commit_blob != str(blob_pin).lower():
                    pin_results[-1] = False

        pinned_ok = bool(has_any_pin and pin_results and all(pin_results))
        if has_any_pin and not pinned_ok:
            findings.append("digest_pinned_mismatch")

        # A lifecycle that has not begun cannot contribute an implementation
        # commit to reachability, even if a stale SHA is present in the record.
        if lifecycle in {"NOT_STARTED", "DISPATCHED", "NOT_APPLICABLE"}:
            if real(implementation_sha):
                findings.append("commit_unexpected_for_lifecycle")
            implementation_sha = None

        if not real(implementation_sha):
            findings.append(
                "commit_absent"
                if implementation_sha is None
                else "commit_pending"
            )
            commit_dimension = "ABSENT"
            resolved_impl = None
        else:
            resolved_impl = resolve_commit(root, implementation_sha)
            if not resolved_impl:
                findings.append("commit_unresolvable")
                commit_dimension = "UNREACHABLE"
            else:
                target_ref = merge_target if real(merge_target) else base
                target = resolve_commit(root, target_ref)
                reachable = is_ancestor(root, resolved_impl, target)
                commit_dimension = "REACHABLE" if reachable else "UNREACHABLE"
                if not reachable:
                    findings.append("commit_unreachable")

        primary = classify_primary(
            digest_present=real(digest),
            implementation_present=real(implementation_sha),
            any_pin=has_any_pin,
            pinned_ok=pinned_ok,
            commit_reachable=commit_dimension == "REACHABLE",
        )

        if not real(digest):
            prompt_dimension = "ABSENT"
        elif has_any_pin:
            prompt_dimension = "PINNED_OK" if pinned_ok else "UNPINNED_MISMATCH"
        else:
            prompt_dimension = "HEAD_MATCH" if head_match else "UNPINNED_MISMATCH"

        rows.append({
            "manifest": manifest_path,
            "work_item_id": work_id,
            "primary_status": primary,
            "findings": findings,
            "prompt_dimension": prompt_dimension,
            "commit_dimension": commit_dimension,
        })
    return rows


def summarize(rows: list[dict]) -> dict:
    primary = {status: 0 for status in PRIMARY}
    matrix = {
        prompt: {commit: 0 for commit in COMMIT_DIMENSIONS}
        for prompt in PROMPT_DIMENSIONS
    }
    findings = {finding: 0 for finding in FINDINGS}
    for row in rows:
        primary[row["primary_status"]] += 1
        matrix[row["prompt_dimension"]][row["commit_dimension"]] += 1
        for finding in row["findings"]:
            if finding in findings:
                findings[finding] += 1
    return {
        "manifest_count": len(rows),
        "primary_status": primary,
        "matrix": matrix,
        "findings": findings,
        "manifests": rows,
    }


def ratchet_violations(
    result: dict, baseline: dict, base_manifest_ids: set[str]
) -> list[str]:
    old = baseline.get("manifests", {})
    violations = []
    for row in result["manifests"]:
        work_id = row["work_item_id"]
        previous = old.get(work_id)
        if work_id not in base_manifest_ids:
            if row["primary_status"] != "TRACEABLE":
                violations.append(
                    f"NEW_FINDINGS:{work_id}:{row['primary_status']}"
                )
            continue
        if previous is None:
            continue
        old_status = previous["primary_status"]
        new_status = row["primary_status"]
        if SEVERITY[new_status] > SEVERITY[old_status]:
            violations.append(f"REGRESSION:{work_id}:{old_status}->{new_status}")
        added = sorted(
            set(row["findings"]) - set(previous.get("findings", []))
        )
        if added:
            violations.append(f"NEW_FINDINGS:{work_id}:{','.join(added)}")
    return violations


def print_report(result: dict) -> None:
    print(f"PROMPT-COMMIT-TRACE manifests={result['manifest_count']}")
    for status, count in result["primary_status"].items():
        print(f"PRIMARY {status}={count}")
    for prompt, commits in result["matrix"].items():
        for commit, count in commits.items():
            print(f"MATRIX {prompt} x {commit}={count}")
    for finding, count in result["findings"].items():
        print(f"FINDING {finding}={count}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--commit", default="HEAD", help="tree/commit to audit")
    parser.add_argument("--base", default="HEAD", help="reachability comparison target")
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--audit-only", action="store_true",
        help="report evidence without applying the baseline ratchet",
    )
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--base-snapshot", type=Path)
    args = parser.parse_args(argv)

    try:
        root = args.root.resolve()
        commit = resolve_commit(root, args.commit)
        base = resolve_commit(root, args.base)
        if not commit:
            raise RuntimeError(f"cannot resolve audit commit: {args.commit}")
        if not base:
            raise RuntimeError(f"cannot resolve comparison base: {args.base}")
        result = summarize(audit(root, commit, base))

        if args.audit_only:
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print_report(result)
            return 0

        if not args.baseline or not args.baseline.is_file():
            raise RuntimeError("required --baseline file is missing")
        if not args.base_snapshot or not args.base_snapshot.is_file():
            raise RuntimeError("required --base-snapshot file is missing")

        baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
        base_snapshot = json.loads(
            args.base_snapshot.read_text(encoding="utf-8")
        )
        if baseline.get("schema_version") != 1:
            raise RuntimeError("invalid baseline schema_version")
        if base_snapshot.get("schema_version") != 1:
            raise RuntimeError("invalid base-snapshot schema_version")
        if not isinstance(baseline.get("manifests"), dict):
            raise RuntimeError("invalid baseline manifests mapping")
        if not isinstance(base_snapshot.get("manifests"), dict):
            raise RuntimeError("invalid base-snapshot manifests mapping")
        snapshot_commit = resolve_commit(root, base_snapshot.get("commit"))
        if snapshot_commit != base:
            raise RuntimeError("--base-snapshot commit does not match --base")
        baseline_commit = resolve_commit(root, baseline.get("commit"))
        if not baseline_commit or not is_ancestor(root, baseline_commit, base):
            raise RuntimeError("baseline commit is not an ancestor of --base")

        base_ids = set(base_snapshot["manifests"])
        violations = ratchet_violations(result, baseline, base_ids)
        if args.json:
            result["ratchet_violations"] = violations
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print_report(result)
            for violation in violations:
                print(f"RATCHET {violation}")
        return 1 if violations else 0
    except (OSError, ValueError, RuntimeError, yaml.YAMLError) as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
