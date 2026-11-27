#!/usr/bin/env python3
"""Verify manifest blob pins against their explicitly declared S-C scope."""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

import yaml

MANIFEST_ROOT = "14-ai-development/work-items"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
FINDING_KINDS = {"MISMATCH", "PATH_MISSING", "UNCLASSIFIED", "NO_SCOPE", "SCOPE_UNRESOLVABLE"}
DIGEST_KEY = re.compile(r"(?:blob|digest|sha256|sha1)", re.IGNORECASE)


class GateError(Exception):
    pass


def git(root: Path, *args: str, allow_missing: bool = False) -> bytes:
    try:
        proc = subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, check=False)
    except OSError as exc:
        raise GateError(f"git execution failed: {exc}") from exc
    if proc.returncode:
        if allow_missing:
            return b""
        detail = proc.stderr.decode("utf-8", "replace").strip()
        raise GateError(detail or f"git {' '.join(args)} failed ({proc.returncode})")
    return proc.stdout


def resolve_commit(root: Path, value: str) -> str:
    if not isinstance(value, str) or not HEX40.fullmatch(value):
        raise GateError(f"candidate commit must be a full lowercase 40-character SHA: {value!r}")
    resolved = git(root, "rev-parse", "--verify", value + "^{commit}").decode().strip()
    if resolved != value:
        raise GateError(f"candidate commit did not resolve exactly: {value}")
    return resolved


def discover_manifests(root: Path, candidate: str) -> list[str]:
    names = git(root, "ls-tree", "-r", "--name-only", candidate).decode("utf-8").splitlines()
    return sorted(name for name in names
                  if name.startswith(MANIFEST_ROOT + "/") and name.endswith("/manifest.yaml"))


def read_manifest(root: Path, candidate: str, path: str) -> dict:
    raw = git(root, "cat-file", "blob", f"{candidate}:{path}")
    value = yaml.safe_load(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise GateError(f"manifest top-level value is not a mapping: {path}")
    return value


def get_field(document, field_path: str):
    """Resolve dotted mapping keys and [index] sequence selectors."""
    tokens = re.findall(r"[^.\[\]]+|\[(\d+)\]", field_path)
    current = document
    for token in tokens:
        if isinstance(token, tuple):
            token = token[0]
        if token.isdigit() and isinstance(current, list):
            index = int(token)
            if index >= len(current):
                raise KeyError(field_path)
            current = current[index]
        elif isinstance(current, dict) and token in current:
            current = current[token]
        else:
            raise KeyError(field_path)
    return current


def discover_digest_fields(value, prefix=""):
    """Find digest-like source declarations; blob_pins is the registration, not source."""
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "blob_pins":
                continue
            path = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(key, str) and DIGEST_KEY.search(key) and not isinstance(child, (dict, list)):
                found.append((path, child))
            found.extend(discover_digest_fields(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(discover_digest_fields(child, f"{prefix}[{index}]"))
    return found


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def emit(kind: str, manifest: str, pin_id: str, field: str, scope: str, locator: str):
    # stdout is the stable ratchet identity channel. Never add computed values here.
    print(f"{kind} manifest={manifest} pin_id={pin_id} field={field} scope={scope} locator={locator}")


def diagnostic(message: str):
    print(message, file=sys.stderr)


def verify_pin(root: Path, candidate: str, manifest: str, pin: dict):
    required = ("pin_id", "field_path", "locator", "algorithm", "expected", "scope")
    if not isinstance(pin, dict) or any(key not in pin for key in required):
        diagnostic(f"UNCLASSIFIED detail manifest={manifest}: malformed blob_pins entry")
        emit("UNCLASSIFIED", manifest, "none", "blob_pins[]", "none", "none")
        return 1
    pin_id = pin["pin_id"]
    field = pin["field_path"]
    locator = pin["locator"]
    scope_obj = pin["scope"]
    scope = scope_obj.get("kind") if isinstance(scope_obj, dict) else None
    if not isinstance(pin_id, str) or not pin_id or not isinstance(field, str) or not field:
        emit("UNCLASSIFIED", manifest, str(pin_id or "none"), str(field or "none"),
             str(scope or "none"), str(locator or "none"))
        return 1
    if not isinstance(locator, str) or not locator.strip():
        emit("UNCLASSIFIED", manifest, pin_id, field, str(scope or "none"), "none")
        return 1
    if scope not in {"candidate", "commit", "content"}:
        emit("NO_SCOPE", manifest, pin_id, field, "none", locator)
        return 1
    if scope == "candidate":
        if set(scope_obj) != {"kind"}:
            emit("NO_SCOPE", manifest, pin_id, field, scope, locator)
            return 1
        target = candidate
    elif scope == "commit":
        commit_sha = scope_obj.get("commit_sha")
        if set(scope_obj) != {"kind", "commit_sha"} or not isinstance(commit_sha, str) or not HEX40.fullmatch(commit_sha):
            emit("NO_SCOPE", manifest, pin_id, field, scope, locator)
            return 1
        target = commit_sha
        try:
            resolved = git(root, "rev-parse", "--verify", target + "^{commit}").decode().strip()
        except GateError as exc:
            emit("SCOPE_UNRESOLVABLE", manifest, pin_id, field, scope, locator)
            diagnostic(f"SCOPE_UNRESOLVABLE detail manifest={manifest} pin_id={pin_id}: {exc}")
            return 2
        if resolved != target:
            emit("SCOPE_UNRESOLVABLE", manifest, pin_id, field, scope, locator)
            diagnostic(f"SCOPE_UNRESOLVABLE detail manifest={manifest} pin_id={pin_id}: commit resolution was not exact")
            return 2
    else:
        if set(scope_obj) != {"kind", "content_ref"} or not isinstance(scope_obj.get("content_ref"), str) or not scope_obj["content_ref"].strip():
            emit("NO_SCOPE", manifest, pin_id, field, scope, locator)
            return 1
        emit("SCOPE_UNRESOLVABLE", manifest, pin_id, field, scope, locator)
        diagnostic(f"SCOPE_UNRESOLVABLE detail manifest={manifest} pin_id={pin_id}: no trusted immutable content resolver is configured")
        return 2

    algorithm = pin["algorithm"]
    expected = pin["expected"]
    if algorithm not in {"git-blob-sha1", "sha256", "byte-length"}:
        emit("UNCLASSIFIED", manifest, pin_id, field, scope, locator)
        diagnostic(f"UNCLASSIFIED detail manifest={manifest} pin_id={pin_id}: unsupported algorithm {algorithm!r}")
        return 1
    if algorithm == "git-blob-sha1" and (not isinstance(expected, str) or not HEX40.fullmatch(expected)):
        emit("UNCLASSIFIED", manifest, pin_id, field, scope, locator)
        diagnostic(f"UNCLASSIFIED detail manifest={manifest} pin_id={pin_id}: invalid git-blob-sha1 expected value")
        return 1
    if algorithm == "sha256" and (not isinstance(expected, str) or not HEX64.fullmatch(expected)):
        emit("UNCLASSIFIED", manifest, pin_id, field, scope, locator)
        diagnostic(f"UNCLASSIFIED detail manifest={manifest} pin_id={pin_id}: invalid sha256 expected value")
        return 1
    if algorithm == "byte-length" and (isinstance(expected, bool) or not isinstance(expected, int) or expected < 0):
        emit("UNCLASSIFIED", manifest, pin_id, field, scope, locator)
        diagnostic(f"UNCLASSIFIED detail manifest={manifest} pin_id={pin_id}: invalid byte-length expected value")
        return 1

    try:
        normalized = PurePosixPath(locator)
        if normalized.is_absolute() or ".." in normalized.parts:
            raise GateError(f"unsafe repository locator: {locator!r}")
        data = git(root, "cat-file", "blob", f"{target}:{normalized.as_posix()}", allow_missing=True)
        exists = bool(data) or git(root, "cat-file", "-e", f"{target}:{normalized.as_posix()}", allow_missing=True) == b""
        # cat-file -e returns empty output both on success and failure; inspect status separately.
        check = subprocess.run(["git", "cat-file", "-e", f"{target}:{normalized.as_posix()}"],
                               cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if check.returncode:
            emit("PATH_MISSING", manifest, pin_id, field, scope, locator)
            diagnostic(f"PATH_MISSING detail manifest={manifest} pin_id={pin_id}: locator absent in declared scope")
            return 1
    except GateError as exc:
        emit("SCOPE_UNRESOLVABLE", manifest, pin_id, field, scope, locator)
        diagnostic(f"SCOPE_UNRESOLVABLE detail manifest={manifest} pin_id={pin_id}: {exc}")
        return 2

    if algorithm == "git-blob-sha1":
        actual = blob_sha(data)
    elif algorithm == "sha256":
        actual = hashlib.sha256(data).hexdigest()
    else:
        actual = len(data)
    if actual != expected:
        emit("MISMATCH", manifest, pin_id, field, scope, locator)
        diagnostic(f"MISMATCH detail manifest={manifest} pin_id={pin_id} expected={expected!r} actual={actual!r}")
        return 1
    return 0


def verify(root: Path, candidate_ref: str, verbose: bool = True) -> int:
    candidate = resolve_commit(root, candidate_ref)
    manifests = discover_manifests(root, candidate)
    if not manifests:
        raise GateError(f"no manifests found in candidate {candidate}")
    status = 0
    for manifest in manifests:
        try:
            doc = read_manifest(root, candidate, manifest)
        except (GateError, UnicodeError, yaml.YAMLError) as exc:
            diagnostic(f"manifest parse/internal error manifest={manifest}: {exc}")
            status = 2
            continue

        raw_fields = discover_digest_fields(doc)
        pins = doc.get("blob_pins", [])
        if not isinstance(pins, list):
            emit("UNCLASSIFIED", manifest, "none", "blob_pins", "none", "none")
            diagnostic(f"UNCLASSIFIED detail manifest={manifest}: blob_pins must be a sequence")
            status = max(status, 1)
            continue

        by_field = {}
        by_id = set()
        for pin in pins:
            if not isinstance(pin, dict):
                emit("UNCLASSIFIED", manifest, "none", "blob_pins[]", "none", "none")
                status = max(status, 1)
                continue
            pin_id = pin.get("pin_id", "none")
            field = pin.get("field_path", "none")
            by_field.setdefault(field, []).append(pin)
            if pin_id in by_id:
                emit("UNCLASSIFIED", manifest, str(pin_id), str(field), "none", str(pin.get("locator", "none")))
                diagnostic(f"UNCLASSIFIED detail manifest={manifest}: duplicate pin_id {pin_id!r}")
                status = max(status, 1)
            by_id.add(pin_id)

        raw_by_field = {}
        for field, value in raw_fields:
            raw_by_field.setdefault(field, []).append(value)

        for field, values in raw_by_field.items():
            entries = by_field.get(field, [])
            if not entries:
                emit("UNCLASSIFIED", manifest, "none", field, "none", "none")
                diagnostic(f"UNCLASSIFIED detail manifest={manifest} field={field}: source declaration has no blob_pins registration")
                status = max(status, 1)
                continue
            if len(entries) != 1 or len(values) != 1:
                emit("UNCLASSIFIED", manifest, "none", field, "none", "none")
                diagnostic(f"UNCLASSIFIED detail manifest={manifest} field={field}: declaration/registration is not one-to-one")
                status = max(status, 1)
                continue
            pin = entries[0]
            if str(pin.get("expected")) != str(values[0]):
                emit("UNCLASSIFIED", manifest, str(pin.get("pin_id", "none")), field,
                     str((pin.get("scope") or {}).get("kind", "none")), str(pin.get("locator", "none")))
                diagnostic(f"UNCLASSIFIED detail manifest={manifest} field={field}: expected differs from source declaration")
                status = max(status, 1)
                continue
            status = max(status, verify_pin(root, candidate, manifest, pin))

        for field, entries in by_field.items():
            if field not in raw_by_field:
                for pin in entries:
                    scope = pin.get("scope") if isinstance(pin.get("scope"), dict) else {}
                    emit("UNCLASSIFIED", manifest, str(pin.get("pin_id", "none")), str(field),
                         str(scope.get("kind", "none")), str(pin.get("locator", "none")))
                    diagnostic(f"UNCLASSIFIED detail manifest={manifest} field={field}: registration has no source declaration")
                    status = max(status, 1)
    return status


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--commit", default="HEAD",
                        help="exact merge-candidate commit checked as the candidate scope")
    args = parser.parse_args(argv)
    try:
        return verify(args.root, args.commit)
    except (GateError, OSError) as exc:
        diagnostic(f"INTERNAL_ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
