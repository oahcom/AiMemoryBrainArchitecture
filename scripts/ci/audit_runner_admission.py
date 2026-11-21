#!/usr/bin/env python3
"""Audit the repository's preventive L2 admission policy.

ponytail: This is a deliberately restricted, line-oriented YAML reader, not a
YAML implementation. It supports ordinary GitHub workflow indentation,
top-level on:/jobs: mappings, job-level runs-on scalars and string lists
(including block lists), and push.branches scalar/list filters. It does not
resolve anchors, aliases, tags, folded scalars, complex keys, merge keys, or
arbitrary flow mappings. If workflow syntax grows beyond this subset, replace
this scanner with a pinned YAML parser once the CI runtime can guarantee that
dependency; until then, unsupported/dynamic runs-on values fail closed.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Optional, Tuple

WORKFLOW_DIR = Path(".github/workflows")
UNTRUSTED_TRIGGERS = {
    "pull_request",
    "pull_request_target",
    "issue_comment",
    "workflow_run",
    "workflow_call",
}
KEY_RE = re.compile(r"^\s*([^:#][^:]*?):\s*(.*?)\s*$")


def uncomment(line: str) -> str:
    """Remove a YAML comment while preserving hashes inside simple quotes."""
    quote = None
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quote == '"':
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = None
        elif char in ("'", '"'):
            quote = char
        elif char == "#":
            if index == 0 or line[index - 1].isspace():
                return line[:index].rstrip()
    return line.rstrip()


def key_value(line: str) -> Optional[Tuple[int, str, str]]:
    clean = uncomment(line)
    if not clean.strip() or clean.lstrip().startswith("-"):
        return None
    indent = len(clean) - len(clean.lstrip(" "))
    match = KEY_RE.match(clean)
    if not match:
        return None
    key = match.group(1).strip().strip("'\"")
    return indent, key, match.group(2).strip()


def scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def flow_items(value: str) -> Optional[list[str]]:
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return None
    inner = value[1:-1].strip()
    if not inner:
        return []
    # The supported subset intentionally excludes nested flow structures.
    return [scalar(item.strip()) for item in inner.split(",")]


def section(lines: list[str], key: str) -> Optional[Tuple[int, int, int, str]]:
    """Return (header index, end index, indent, inline value) for a root key."""
    for index, line in enumerate(lines):
        parsed = key_value(line)
        if parsed and parsed[0] == 0 and parsed[1] == key:
            end = index + 1
            while end < len(lines):
                candidate = lines[end]
                if candidate.strip() and not candidate.lstrip().startswith("#"):
                    indent = len(candidate) - len(candidate.lstrip(" "))
                    if indent == 0:
                        break
                end += 1
            return index, end, 0, parsed[2]
    return None


def direct_children(lines: list[str], start: int, end: int, parent_indent: int) -> list[Tuple[int, int, str, str]]:
    result = []
    for index in range(start + 1, end):
        parsed = key_value(lines[index])
        if parsed and parsed[0] > parent_indent:
            # Only the first indentation level below the parent is direct.
            if not any(
                key_value(lines[prior]) and key_value(lines[prior])[0] > parent_indent
                and key_value(lines[prior])[0] < parsed[0]
                for prior in range(start + 1, index)
            ):
                result.append((index, parsed[0], parsed[1], parsed[2]))
    return result


def value_items(lines: list[str], index: int, end: int, indent: int, value: str) -> Optional[list[str]]:
    """Read a scalar or a simple YAML string list."""
    value = value.strip()
    if value:
        items = flow_items(value)
        if items is not None:
            return items
        if value.startswith(("|", ">", "{", "&", "*", "!")) or "${{" in value:
            return None
        return [scalar(value)]
    items = []
    for cursor in range(index + 1, end):
        raw = uncomment(lines[cursor])
        if not raw.strip():
            continue
        current_indent = len(raw) - len(raw.lstrip(" "))
        if current_indent <= indent:
            break
        stripped = raw.strip()
        if stripped.startswith("-"):
            item = scalar(stripped[1:].strip())
            if not item or "${{" in item or item.startswith(("{", "[", "|", ">", "&", "*", "!")):
                return None
            items.append(item)
        elif key_value(lines[cursor]):
            break
        else:
            return None
    return items if items else None


def parse_triggers(lines: list[str]) -> Tuple[set[str], bool, Optional[list[str]]]:
    on_section = section(lines, "on")
    if on_section is None:
        return set(), False, None
    start, end, _, inline = on_section
    triggers: set[str] = set()
    push_present = False
    push_branches: Optional[list[str]] = None

    inline_items = flow_items(inline)
    if inline_items is not None:
        triggers.update(inline_items)
        push_present = "push" in triggers
    elif inline and not inline.startswith("{"):
        trigger = scalar(inline)
        triggers.add(trigger)
        push_present = trigger == "push"
    else:
        children = direct_children(lines, start, end, 0)
        for child_index, child_indent, child_key, child_value in children:
            triggers.add(child_key)
            if child_key == "push":
                push_present = True
                if child_value:
                    # A limited inline push map is supported for branches only.
                    match = re.search(r"branches\s*:\s*(\[[^]]*\]|[^,}]+)", child_value)
                    if match:
                        push_branches = flow_items(match.group(1)) or [scalar(match.group(1))]
                else:
                    push_end = end
                    for cursor in range(child_index + 1, end):
                        parsed = key_value(lines[cursor])
                        if parsed and parsed[0] <= child_indent:
                            push_end = cursor
                            break
                    for branch_index, branch_indent, branch_key, branch_value in direct_children(
                        lines, child_index, push_end, child_indent
                    ):
                        if branch_key == "branches":
                            push_branches = value_items(
                                lines, branch_index, push_end, branch_indent, branch_value
                            )
                            break
    return triggers, push_present, push_branches


def parse_jobs(lines: list[str]) -> list[Tuple[str, list[str], int]]:
    jobs_section = section(lines, "jobs")
    if jobs_section is None:
        return []
    start, end, _, inline = jobs_section
    if inline:
        raise ValueError("jobs: must be a block mapping in the supported YAML subset")
    jobs = []
    job_headers = []
    for index in range(start + 1, end):
        parsed = key_value(lines[index])
        if parsed and parsed[0] == 2:
            job_headers.append((index, parsed[1]))
    for position, (header_index, job_name) in enumerate(job_headers):
        job_end = job_headers[position + 1][0] if position + 1 < len(job_headers) else end
        runs_on = []
        for index in range(header_index + 1, job_end):
            parsed = key_value(lines[index])
            if parsed and parsed[1] == "runs-on":
                runs_on.append((index, parsed[0], parsed[2]))
        jobs.append((job_name, lines[header_index:job_end], header_index))
        # Store parsed runs-on values on the function attribute for this small scanner.
        jobs[-1] = (job_name, [f"\x00{idx}:{indent}:{value}" for idx, indent, value in runs_on] + lines[header_index:job_end], header_index)
    return jobs


def audit_workflow(path: Path) -> Tuple[int, list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    triggers, push_present, push_branches = parse_triggers(lines)
    jobs = parse_jobs(lines)
    audited = 0
    violations: list[str] = []

    for job_name, job_lines, _ in jobs:
        run_entries = []
        for entry in job_lines:
            if entry.startswith("\x00"):
                _, rest = entry.split("\x00", 1)
                idx_text, indent_text, value = rest.split(":", 2)
                run_entries.append((int(idx_text), int(indent_text), value))
        candidate = any(
            "self-hosted" in (flow_items(value) or [scalar(value)])
            or "${{" in value
            or (not value and any("self-hosted" in line for line in job_lines))
            for _, _, value in run_entries
        )
        if not candidate:
            continue
        audited += 1
        prefix = f"{path.as_posix()}:{job_name}: "

        for trigger in sorted(UNTRUSTED_TRIGGERS.intersection(triggers)):
            violations.append(prefix + f"untrusted trigger '{trigger}' is not permitted for self-hosted jobs")

        if push_present:
            if push_branches is None:
                violations.append(prefix + "on.push has no branches: filter")
            else:
                for branch in push_branches:
                    if branch != "main":
                        violations.append(prefix + f"on.push.branches includes non-main branch '{branch}'")

        if len(run_entries) != 1:
            violations.append(prefix + "runs-on is missing or cannot be statically evaluated")
        else:
            index, indent, value = run_entries[0]
            run_value = value_items(lines, index, len(lines), indent, value)
            if run_value is None or not run_value or any("${{" in item for item in run_value):
                violations.append(prefix + "runs-on cannot be statically evaluated as a string or string list")

    return audited, violations


def main() -> int:
    audited_total = 0
    violations: list[str] = []
    try:
        if not WORKFLOW_DIR.is_dir():
            raise RuntimeError(f"workflow directory not found: {WORKFLOW_DIR}")
        workflow_files = sorted(WORKFLOW_DIR.glob("*.yml"))
        if not workflow_files:
            raise RuntimeError(f"no .yml workflow files found in {WORKFLOW_DIR}")
        for workflow in workflow_files:
            audited, found = audit_workflow(workflow)
            audited_total += audited
            violations.extend(found)

        for violation in violations:
            print(f"::error::{violation}")
        print(
            f"runner admission: {audited_total} self-hosted job(s) audited, "
            f"{len(violations)} violation(s)"
        )
        if audited_total == 0:
            print("::error::no self-hosted jobs were discovered; admission scan is ineffective", file=sys.stderr)
            return 2
        return 1 if violations else 0
    except Exception as exc:
        print(f"::error::runner admission audit failed: {exc}", file=sys.stderr)
        print(
            f"runner admission: {audited_total} self-hosted job(s) audited, "
            f"{len(violations)} violation(s)"
        )
        return 2


if __name__ == "__main__":
    sys.exit(main())
