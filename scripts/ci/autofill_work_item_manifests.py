#!/usr/bin/env python3
"""Stage-1, read-only proposal generator for work-item manifest findings."""

from __future__ import annotations

import argparse
import copy
import difflib
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required", file=sys.stderr)
    raise SystemExit(2)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def pointer_parts(pointer: str) -> list[str]:
    if not pointer:
        return []
    return [
        part.replace("~1", "/").replace("~0", "~")
        for part in pointer.lstrip("/").split("/")
    ]


def get_pointer(document: Any, pointer: str) -> Any:
    current = document
    for part in pointer_parts(pointer):
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list) and part.isdigit():
            index = int(part)
            current = current[index] if index < len(current) else None
        else:
            return None
    return current


def set_top_level(document: dict, key: str, value: Any) -> None:
    document[key] = copy.deepcopy(value)


def markdown_relationship(path: Path) -> str | None:
    name = path.name.lower()
    if name == "evidence.md" or name.startswith("session-evidence"):
        return "evidence"
    if name.startswith("prompt") and path.suffix.lower() == ".md":
        return "reference"
    if name in {"readme.md", "index.md"}:
        return "reference"
    return None


def work_item_markdown(root: Path, manifest: Path) -> list[dict[str, str]]:
    directory = manifest.parent
    result: list[dict[str, str]] = []

    for path in sorted(directory.glob("*.md")):
        if path.name.upper() == "INDEX.MD":
            continue

        if not path.is_file() or path.is_symlink():
            continue

        relationship = markdown_relationship(path)
        if relationship is None:
            continue

        result.append(
            {
                "path": path.relative_to(root).as_posix(),
                "relationship": relationship,
            }
        )

    return result


def explicit_scope_paths(document: dict, root: Path) -> list[str]:
    scope = document.get("scope")
    if not isinstance(scope, dict):
        return []

    result = []
    for key in ("files_to_create", "files_to_modify"):
        values = scope.get(key)
        if not isinstance(values, list):
            continue
        for value in values:
            if not isinstance(value, str):
                continue
            candidate = value.strip()
            path = root / candidate
            if (
                candidate
                and not Path(candidate).is_absolute()
                and not Path(candidate).is_symlink()
                and candidate not in result
            ):
                result.append(candidate)
    return result


def implementation_candidate(
    document: dict, field: str, root: Path
) -> tuple[Any | None, dict | None, str]:
    implementation = document.get("implementation")
    if not isinstance(implementation, dict):
        implementation = {}

    if field == "summary":
        scope = document.get("scope")
        objective = scope.get("objective") if isinstance(scope, dict) else None
        if isinstance(objective, str) and objective.strip():
            return (
                objective.strip(),
                {
                    "type": "existing_manifest_field",
                    "path": "scope.objective",
                },
                "Copied from the existing scope objective; not independently asserted as test evidence.",
            )
        return None, None, "No existing scope.objective supplies an implementation summary."

    if field == "files_changed":
        existing = implementation.get("files_changed")
        if isinstance(existing, list) and existing:
            return (
                copy.deepcopy(existing),
                {
                    "type": "existing_manifest_field",
                    "path": "implementation.files_changed",
                },
                "Existing implementation file list is already present.",
            )

        paths = explicit_scope_paths(document, root)
        if paths:
            return (
                paths,
                {
                    "type": "existing_manifest_scope",
                    "paths": paths,
                },
                "Paths are explicitly listed under scope.files_to_create/files_to_modify and exist in the working tree.",
            )
        return None, None, (
            "No explicit existing files_to_create/files_to_modify list with "
            "verifiable paths was found. Commit-wide inference is not used."
        )

    if field == "tests":
        existing = implementation.get("tests")
        if isinstance(existing, list) and existing:
            return (
                copy.deepcopy(existing),
                {
                    "type": "existing_manifest_field",
                    "path": "implementation.tests",
                },
                "Existing implementation test commands are already present.",
            )

        scope = document.get("scope")
        tests = scope.get("tests") if isinstance(scope, dict) else None
        if isinstance(tests, list) and tests:
            return (
                copy.deepcopy(tests),
                {
                    "type": "existing_manifest_field",
                    "path": "scope.tests",
                },
                "Copied from the existing scope.tests list.",
            )
        return None, None, (
            "No existing implementation.tests or scope.tests list was found. "
            "Git commit messages are not treated as proof that tests were run."
        )

    return None, None, f"Unsupported implementation key: {field}"


def enum_for_rule(rule: str, schema: dict) -> tuple[str | None, list | None]:
    fields = schema.get("fields", {})
    if rule == "implementation.status.enum":
        enum = fields.get("implementation", {}).get("status_enum")
        return "implementation.status", enum
    if rule == "documentation.relationship.enum":
        enum = fields.get("documentation", {}).get("relationship_enum")
        return "documentation[].relationship", enum
    return None, None


def find_enum_value(document: dict, location: str) -> Any:
    if location == "implementation.status":
        implementation = document.get("implementation")
        return implementation.get("status") if isinstance(implementation, dict) else None
    if location == "documentation[].relationship":
        docs = document.get("documentation")
        if isinstance(docs, list):
            return [
                item.get("relationship")
                for item in docs
                if isinstance(item, dict)
            ]
    return None


def propose_one(
    finding: dict,
    document: dict,
    root: Path,
    manifest: Path,
    schema: dict,
) -> dict:
    rule = finding["rule"]
    pointer = finding["pointer"]
    result = {
        "finding": copy.deepcopy(finding),
        "status": "BLOCKED",
        "proposed_value": None,
        "operation": None,
        "source": None,
        "reason": None,
    }

    enum_location, allowed = enum_for_rule(rule, schema)
    if enum_location:
        current = find_enum_value(document, enum_location)
        invalid = (
            current is not None
            and (
                any(value not in allowed for value in current)
                if isinstance(current, list)
                else current not in allowed
            )
        )
        if (
            rule == "implementation.status.enum"
            and pointer == "/implementation/status"
            and current == "MERGED"
            and isinstance(allowed, list)
            and "IMPLEMENTED" in allowed
        ):
            result.update({
                "status": "PROPOSED",
                "proposed_value": "IMPLEMENTED",
                "operation": {
                    "type": "set_nested_key",
                    "path": ["implementation", "status"],
                    "value": "IMPLEMENTED",
                },
                "source": {
                    "type": "existing_manifest_value",
                    "pointer": "/implementation/status",
                    "value": "MERGED",
                },
                "reason": (
                    "MERGED explicitly records that the implementation was merged. "
                    "IMPLEMENTED is the corresponding value in the implementation.status schema enum."
                ),
            })
            return result

        if invalid:
            result["reason"] = (
                f"Existing value {current!r} is outside schema enum "
                f"{allowed!r}; stage-1 will not guess a replacement."
            )
            result["source"] = {
                "type": "schema",
                "path": "schema.fields",
                "allowed_values": allowed,
            }
            return result

        result["reason"] = (
            "The finding concerns an enum constraint, but no invalid existing "
            "value was identified. No replacement is inferred."
        )
        result["source"] = {
            "type": "schema",
            "path": "schema.fields",
            "allowed_values": allowed,
        }
        return result

    if rule in {"top_level.documentation.required", "documentation.required"}:
        candidates = work_item_markdown(root, manifest)
        if not candidates:
            result["reason"] = (
                "No eligible Work Item markdown document was found. "
                "INDEX.md is an index and is not accepted as documentation "
                "evidence."
            )
            return result

        result.update({
            "status": "PROPOSED",
            "proposed_value": candidates,
            "operation": {
                "type": "replace_top_level_key",
                "key": "documentation",
                "value": candidates,
            },
            "source": {
                "type": "existing_work_item_markdown",
                "files": candidates,
            },
            "reason": (
                "Each path exists in the Work Item directory. Relationships "
                "are conservative filename-based candidates and require review."
            ),
        })
        return result

    if rule == "implementation.required_key":
        parts = pointer_parts(pointer)
        field = parts[-1] if parts else ""
        if field not in {"summary", "files_changed", "tests"}:
            result["reason"] = (
                f"Unsupported or ambiguous implementation pointer {pointer!r}."
            )
            return result

        value, source, reason = implementation_candidate(document, field, root)
        if value is None:
            result["reason"] = reason
            return result

        result.update({
            "status": "PROPOSED",
            "proposed_value": value,
            "operation": {
                "type": "set_nested_key",
                "path": ["implementation", field],
                "value": value,
            },
            "source": source,
            "reason": reason,
        })
        return result

    if rule == "top_level.date.required":
        result["reason"] = (
            "A Git author date or file timestamp does not establish the "
            "Work Item's normative date. An authoritative date record is required."
        )
        return result

    if rule == "top_level.base_commit_sha.required":
        result["reason"] = (
            "The current merge-base is not proof of the historical base commit "
            "used by this Work Item. Recover the recorded base SHA from its "
            "original PR/session evidence."
        )
        return result

    if rule == "top_level.risk_rationale.required":
        result["reason"] = (
            "A fixed phrase such as 'no risk declared' would invent a risk "
            "assessment. A rationale must be recovered from an existing "
            "authoritative record or supplied by an accountable human."
        )
        return result

    result["reason"] = (
        "No conservative, source-backed resolver exists for this rule. "
        "No value is fabricated."
    )
    return result


def apply_operation(document: dict, operation: dict) -> None:
    if operation["type"] == "replace_top_level_key":
        set_top_level(document, operation["key"], operation["value"])
        return

    if operation["type"] == "set_nested_key":
        current = document.get("implementation")
        if not isinstance(current, dict):
            current = {}
            document["implementation"] = current
        current[operation["path"][-1]] = copy.deepcopy(operation["value"])


def render_yaml(document: dict) -> str:
    return yaml.safe_dump(
        document,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=100,
    )


def make_diff(path: str, before: str, after: str) -> tuple[str, str]:
    forward = "".join(difflib.unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile=f"a/{path}",
        tofile=f"b/{path}",
    ))
    reverse = "".join(difflib.unified_diff(
        after.splitlines(keepends=True),
        before.splitlines(keepends=True),
        fromfile=f"b/{path}",
        tofile=f"a/{path}",
    ))
    return forward, reverse


def build_proposals(root: Path, findings: list, schema: dict) -> dict:
    grouped = defaultdict(list)
    for index, finding in enumerate(findings):
        for key in ("manifest", "rule", "pointer", "category", "message"):
            if key not in finding:
                raise ValueError(f"finding[{index}] missing required key {key!r}")
        grouped[finding["manifest"]].append(finding)

    manifests = []
    total_proposed = 0
    total_blocked = 0

    for relative in sorted(grouped):
        relative_path = Path(relative)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"unsafe manifest path: {relative!r}")

        manifest = root / relative_path
        if not manifest.is_file() or manifest.is_symlink():
            raise ValueError(f"manifest does not exist or is not a regular file: {relative}")

        original_text = manifest.read_text(encoding="utf-8")
        original = load_yaml(manifest)
        if not isinstance(original, dict):
            raise ValueError(f"manifest root must be a mapping: {relative}")

        proposed_document = copy.deepcopy(original)
        entries = []

        for finding in grouped[relative]:
            entry = propose_one(finding, proposed_document, root, manifest, schema)
            entries.append(entry)
            if entry["status"] == "PROPOSED":
                apply_operation(proposed_document, entry["operation"])
                total_proposed += 1
            else:
                total_blocked += 1

        after_text = render_yaml(proposed_document)
        forward, reverse = make_diff(relative, original_text, after_text)

        manifests.append({
            "manifest": relative,
            "before_sha256": sha256(original_text),
            "proposed_sha256": sha256(after_text),
            "findings": entries,
            "diff": forward,
            "reverse_diff": reverse,
        })

    return {
        "mode": "stage-1-read-only",
        "files_written": 0,
        "finding_count": len(findings),
        "manifest_count": len(manifests),
        "proposed_count": total_proposed,
        "blocked_count": total_blocked,
        "manifests": manifests,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--findings", required=True, type=Path)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Reserved for a future stage-2 implementation; always rejected.",
    )
    args = parser.parse_args()
    if args.write:
        parser.error("--write is not available in stage-1; no files are modified")
    return args


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    findings = json.loads(args.findings.read_text(encoding="utf-8"))
    if not isinstance(findings, list):
        raise ValueError("--findings must contain a JSON array")

    schema = load_yaml(args.schema)
    if not isinstance(schema, dict):
        raise ValueError("--schema must contain a YAML mapping")

    result = build_proposals(root, findings, schema)
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)

    print(
        "STAGE1: findings={finding_count} manifests={manifest_count} "
        "proposed={proposed_count} blocked={blocked_count} files_written=0".format(
            **result
        ),
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
