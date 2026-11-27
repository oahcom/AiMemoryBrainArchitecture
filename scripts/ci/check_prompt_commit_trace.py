#!/usr/bin/env python3
"""Read-only prompt-to-implementation trace audit.

Primary decision order (contract; regression-tested):
1. NO_TRACE: prompt digest or implementation commit is absent/placeholder.
2. DIGEST_UNPINNED: a digest exists but neither immutable prompt pin exists.
   HEAD_MATCH does not establish an execution-time pin.
3. DIGEST_MISMATCH: at least one supplied immutable pin does not verify the digest.
4. COMMIT_UNREACHABLE: the implementation commit cannot be resolved or is not
   an ancestor of implementation.merge_commit_sha, otherwise --base.
5. TRACEABLE: an immutable prompt pin verifies and the implementation commit
   is reachable. Findings and the prompt×commit matrix retain orthogonal facts.
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

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_ROOT = "14-ai-development/work-items"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
PLACEHOLDERS = {"", "PENDING", "NOT_STARTED", "NOT_VERIFIED", "N/A", "NULL"}
PRIMARY = ("NO_TRACE", "DIGEST_UNPINNED", "DIGEST_MISMATCH",
           "COMMIT_UNREACHABLE", "TRACEABLE")
PROMPT = ("PINNED_OK", "HEAD_MATCH", "UNPINNED_MISMATCH", "ABSENT")
COMMITS = ("REACHABLE", "UNREACHABLE", "ABSENT")
FINDINGS = ("digest_absent", "digest_not_verified", "digest_unpinned",
            "digest_head_mismatch", "digest_pinned_mismatch", "commit_absent",
            "commit_pending", "commit_unresolvable", "commit_unreachable")
# Lower is better. Ratchet regressions are movements toward a larger rank.
SEVERITY = {"TRACEABLE": 0, "COMMIT_UNREACHABLE": 1, "DIGEST_MISMATCH": 2,
            "DIGEST_UNPINNED": 3, "NO_TRACE": 4}


def git(root, *args, check=True):
    p = subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    if check and p.returncode:
        raise RuntimeError(p.stderr.decode("utf-8", "replace").strip())
    return p.stdout


def real(v):
    return isinstance(v, str) and v.strip().upper() not in PLACEHOLDERS


def manifests(root, ref):
    names = git(root, "ls-tree", "-r", "--name-only", ref).decode().splitlines()
    return sorted(p for p in names
                  if p.startswith(MANIFEST_ROOT + "/") and p.endswith("/manifest.yaml"))


def resolve_commit(root, value):
    if not real(value) or not re.fullmatch(r"[0-9a-fA-F]{7,40}", str(value)):
        return None
    resolved = git(root, "rev-parse", "--verify", str(value) + "^{commit}",
                   check=False).decode().strip()
    return resolved if HEX40.fullmatch(resolved) else None


def read_git_blob(root, oid):
    if not real(oid) or not re.fullmatch(r"[0-9a-fA-F]{40}", str(oid)):
        return None
    kind = git(root, "cat-file", "-t", str(oid), check=False).decode().strip()
    if kind != "blob":
        return None
    p = subprocess.run(["git", "cat-file", "blob", str(oid)], cwd=root,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout if p.returncode == 0 else None


def read_path_at_commit(root, commit, path):
    resolved = resolve_commit(root, commit)
    if not resolved or not real(path):
        return None
    p = subprocess.run(["git", "show", resolved + ":" + str(path)], cwd=root,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout if p.returncode == 0 else None


def classify_primary(digest_present, implementation_present, any_pin, pinned_ok, commit_reachable):
    # Do not reorder: the order is part of the audit contract.
    if not digest_present or not implementation_present:
        return "NO_TRACE"
    if not any_pin:
        return "DIGEST_UNPINNED"
    if not pinned_ok:
        return "DIGEST_MISMATCH"
    if not commit_reachable:
        return "COMMIT_UNREACHABLE"
    return "TRACEABLE"


def audit(root, ref, base):
    rows = []
    base_sha = resolve_commit(root, base)
    if not base_sha:
        raise RuntimeError("cannot resolve comparison base: " + str(base))
    for mp in manifests(root, ref):
        raw = read_path_at_commit(root, ref, mp)
        if raw is None:
            raise RuntimeError("cannot read manifest " + mp)
        doc = yaml.safe_load(raw.decode("utf-8")) or {}
        digest, pfile = doc.get("prompt_sha256"), doc.get("prompt_file")
        pblob = doc.get("prompt_file_blob_sha")
        pcommit = doc.get("prompt_file_commit_sha")
        impl_section = doc.get("implementation") or {}
        impl = impl_section.get("implementation_commit_sha") or doc.get("implementation_commit_sha")
        merge_target = impl_section.get("merge_commit_sha") or doc.get("merge_commit_sha")
        findings = []

        digest_valid = bool(real(digest) and HEX64.fullmatch(str(digest)))
        if not real(digest):
            findings.append("digest_absent" if digest is None else "digest_not_verified")
        elif not digest_valid:
            findings.append("digest_not_verified")

        has_blob_pin, has_commit_pin = real(pblob), real(pcommit)
        has_any_pin = has_blob_pin or has_commit_pin
        if real(digest) and not has_any_pin:
            findings.append("digest_unpinned")

        head_bytes = read_path_at_commit(root, ref, pfile)
        head_match = bool(head_bytes is not None and digest_valid and
                          hashlib.sha256(head_bytes).hexdigest() == digest.lower())
        if real(digest) and not head_match:
            findings.append("digest_head_mismatch")

        pin_results = []
        if has_blob_pin:
            blob_bytes = read_git_blob(root, pblob)
            pin_results.append(bool(blob_bytes is not None and digest_valid and
                                    hashlib.sha256(blob_bytes).hexdigest() == digest.lower()))
        if has_commit_pin:
            commit_bytes = read_path_at_commit(root, pcommit, pfile)
            commit_blob_oid = ""
            resolved_pin_commit = resolve_commit(root, pcommit)
            if resolved_pin_commit and real(pfile):
                commit_blob_oid = git(root, "rev-parse", "--verify",
                                      resolved_pin_commit + ":" + str(pfile),
                                      check=False).decode().strip()
            commit_ok = bool(commit_bytes is not None and digest_valid and
                             hashlib.sha256(commit_bytes).hexdigest() == digest.lower())
            if has_blob_pin:
                commit_ok = commit_ok and commit_blob_oid == str(pblob).lower()
            pin_results.append(commit_ok)
        pinned_ok = bool(has_any_pin and all(pin_results))
        if has_any_pin and not pinned_ok:
            findings.append("digest_pinned_mismatch")

        if not real(impl):
            findings.append("commit_absent" if impl is None else "commit_pending")
            cdim = "ABSENT"
            impl_sha = None
        else:
            impl_sha = resolve_commit(root, impl)
            if not impl_sha:
                findings.append("commit_unresolvable")
                cdim = "UNREACHABLE"
            else:
                target = merge_target if real(merge_target) else base_sha
                target_sha = resolve_commit(root, target)
                ancestor = False
                if target_sha:
                    probe = subprocess.run(
                        ["git", "merge-base", "--is-ancestor", impl_sha, target_sha],
                        cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    ancestor = probe.returncode == 0
                cdim = "REACHABLE" if ancestor else "UNREACHABLE"
                if not ancestor:
                    findings.append("commit_unreachable")

        primary = classify_primary(real(digest), real(impl), has_any_pin,
                                   pinned_ok, cdim == "REACHABLE")

        if not real(digest):
            pdim = "ABSENT"
        elif has_any_pin:
            pdim = "PINNED_OK" if pinned_ok else "UNPINNED_MISMATCH"
        else:
            pdim = "HEAD_MATCH" if head_match else "UNPINNED_MISMATCH"
        rows.append({"manifest": mp,
                     "work_item_id": doc.get("work_item_id", Path(mp).parent.name),
                     "primary_status": primary, "findings": findings,
                     "prompt_dimension": pdim, "commit_dimension": cdim})
    return rows


def summarize(rows):
    counts = {s: 0 for s in PRIMARY}
    matrix = {p: {c: 0 for c in COMMITS} for p in PROMPT}
    fc = {f: 0 for f in FINDINGS}
    for row in rows:
        counts[row["primary_status"]] += 1
        matrix[row["prompt_dimension"]][row["commit_dimension"]] += 1
        for finding in row["findings"]:
            fc[finding] += 1
    return {"manifest_count": len(rows), "primary_status": counts,
            "matrix": matrix, "findings": fc, "manifests": rows}


def ratchet_violations(result, baseline):
    old = baseline.get("manifests", {})
    violations = []
    for row in result["manifests"]:
        ident = row["work_item_id"]
        prior = old.get(ident)
        if prior is None:
            if row["primary_status"] != "TRACEABLE":
                violations.append(f"NEW_NON_TRACEABLE {ident} {row['primary_status']}")
            continue
        if SEVERITY[row["primary_status"]] > SEVERITY[prior["primary_status"]]:
            violations.append(f"REGRESSION {ident} {prior['primary_status']} -> {row['primary_status']}")
        added = sorted(set(row["findings"]) - set(prior.get("findings", [])))
        if added:
            violations.append(f"NEW_FINDINGS {ident} {','.join(added)}")
    return violations


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--commit", default="origin/main",
                    help="manifest tree to audit (default: origin/main)")
    ap.add_argument("--base", default="origin/main",
                    help="ancestor comparison target when manifest has no implementation.merge_commit_sha")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--emit-baseline", type=Path, help="write a reviewed baseline snapshot")
    ap.add_argument("--baseline", type=Path,
                    help="required ratchet baseline; absence is a hard error")
    args = ap.parse_args()
    try:
        ref = resolve_commit(args.root, args.commit)
        if not ref:
            raise RuntimeError("cannot resolve audit commit: " + args.commit)
        result = summarize(audit(args.root, ref, args.base))
        if args.emit_baseline:
            snapshot = {"schema_version": 1, "commit": ref, "source_commit": ref,
                        "manifests": {row["work_item_id"]: {
                            "primary_status": row["primary_status"],
                            "findings": row["findings"]} for row in result["manifests"]}}
            args.emit_baseline.write_text(json.dumps(snapshot, sort_keys=True, indent=2) + "\n")
            print(json.dumps(snapshot, sort_keys=True, indent=2))
            return 0
        if not args.baseline or not args.baseline.is_file():
            raise RuntimeError("required ratchet baseline is missing: " + str(args.baseline))
        baseline = json.loads(args.baseline.read_text())
        if baseline.get("schema_version") != 1 or not isinstance(baseline.get("manifests"), dict):
            raise RuntimeError("invalid prompt-commit-trace baseline schema")
        baseline_commit = baseline.get("commit")
        expected_commit = resolve_commit(args.root, args.base)
        if not HEX40.fullmatch(str(baseline_commit or "")) or baseline_commit != expected_commit:
            raise RuntimeError("baseline commit pin does not match comparison base: "
                               + str(baseline_commit) + " != " + str(expected_commit))
        violations = ratchet_violations(result, baseline)
        if args.json:
            result["ratchet_violations"] = violations
            print(json.dumps(result, sort_keys=True, indent=2))
        else:
            print(f"PROMPT-COMMIT-TRACE commit={ref} base={args.base} manifests={result['manifest_count']}")
            for status, count in result["primary_status"].items():
                print(f"PRIMARY {status}={count}")
            for prompt, commits in result["matrix"].items():
                for commit, count in commits.items():
                    print(f"MATRIX {prompt} x {commit}={count}")
            for finding, count in result["findings"].items():
                print(f"FINDING {finding}={count}")
            for violation in violations:
                print("RATCHET " + violation)
        return 1 if violations else 0
    except Exception as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
