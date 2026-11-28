#!/usr/bin/env python3
"""Structural and source-evidence validator for AID-2026-293.

Exit codes:
  0: all carrier rules pass
  1: one or more carrier rules fail
  2: invalid CLI arguments or unreadable YAML input
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required: python -m pip install PyYAML", file=sys.stderr)
    raise SystemExit(2)

RISK_IDS = {f"R-{i:02d}" for i in range(1, 11)}
MODULE_IDS = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "Storage"}
DIMENSIONS = {"change_surface", "coupling", "irreversibility", "concurrency_state"}
VALID_EVIDENCE_STATES = {"PATH_LINE", "NO_EVIDENCE_FOUND", "PENDING_SEARCH_EXECUTION"}

STATUS_VALUES = {
    "ac3": {"CONFIRMED_BY_COORDINATOR"},
    "ac4": {"PENDING_SOURCE_EVIDENCE"},
    "ac6": {"EXECUTED_BY_COORDINATOR_NOT_IN_CI"},
    "ac6_negative_cases": {"EXECUTED_BY_COORDINATOR_NOT_IN_CI"},
    "ac8": {"PENDING_INDEPENDENT_REVIEW"},
    "ac8_independent_review": {"PENDING_INDEPENDENT_REVIEW"},
}

_TYPO = {
    ord(c): r
    for c, r in zip(
        "\u2018\u2019\u201a\u201b\u201c\u201d\u201e\u201f\u2013\u2014\u2015\u2212\u00a0",
        "'" * 4 + '"' * 4 + "-" * 4 + " ",
    )
}
_ZW = dict.fromkeys(map(ord, "\u200b\u200c\u200d\u200e\u200f\u2060\ufeff"))


def norm(s: str) -> str:
    """Normalize a source quote for whole-line comparison."""
    s = unicodedata.normalize("NFKC", s or "")
    s = s.translate(_TYPO).translate(_ZW)
    return re.sub(r"\s+", " ", s).strip()


def issue(rule: str, object_id: str, reason: str) -> str:
    return f"{rule} {object_id} {reason}"


def is_path_line(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    return re.fullmatch(r".+:\d+", value.strip()) is not None


def validate_source_evidence(
    evidence: Any,
    object_id: str,
    root: Path | None,
) -> list[str]:
    """Fail closed when a path, line number, or whole-line quote is invalid."""
    errors: list[str] = []

    if not isinstance(evidence, dict):
        return [
            issue("R8_PATH_EXISTS", object_id, "evidence entry must be a mapping"),
            issue("R9_LINE_IN_RANGE", object_id, "evidence entry must be a mapping"),
            issue("R10_QUOTE_MATCHES_LINE", object_id, "evidence entry must be a mapping"),
        ]

    path_line = evidence.get("path_line")
    quote = evidence.get("quote")

    parsed = False
    source_path: Path | None = None
    line_number: int | None = None

    if isinstance(path_line, str):
        match = re.fullmatch(r"(.+):(\d+)", path_line.strip())
        if match:
            raw_path, raw_line = match.groups()
            try:
                line_number = int(raw_line)
                candidate = Path(raw_path)
                if root is not None:
                    source_path = (root / candidate).resolve()
                    source_path.relative_to(root)
                    parsed = True
            except (ValueError, OSError, RuntimeError):
                parsed = False

    if not parsed or source_path is None:
        errors.append(
            issue(
                "R8_PATH_EXISTS",
                object_id,
                "path_line must resolve to a path inside --root",
            )
        )
        errors.append(
            issue(
                "R9_LINE_IN_RANGE",
                object_id,
                "path_line cannot be resolved beneath --root",
            )
        )
        errors.append(
            issue(
                "R10_QUOTE_MATCHES_LINE",
                object_id,
                "source line cannot be read for quote comparison",
            )
        )
        return errors

    if not source_path.is_file():
        errors.append(
            issue("R8_PATH_EXISTS", object_id, f"file does not exist: {path_line}")
        )
        errors.append(
            issue("R9_LINE_IN_RANGE", object_id, f"source file is unavailable: {path_line}")
        )
        errors.append(
            issue(
                "R10_QUOTE_MATCHES_LINE",
                object_id,
                f"source file is unavailable: {path_line}",
            )
        )
        return errors

    try:
        source_text = source_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        reason = f"cannot read UTF-8 source file: {exc}"
        errors.append(issue("R9_LINE_IN_RANGE", object_id, reason))
        errors.append(issue("R10_QUOTE_MATCHES_LINE", object_id, reason))
        return errors

    lines = source_text.splitlines()

    if line_number is None or line_number < 1 or line_number > len(lines):
        errors.append(
            issue(
                "R9_LINE_IN_RANGE",
                object_id,
                f"line number is outside 1..{len(lines)}: {path_line}",
            )
        )
        errors.append(
            issue(
                "R10_QUOTE_MATCHES_LINE",
                object_id,
                f"cannot compare quote because line is out of range: {path_line}",
            )
        )
        return errors

    if not isinstance(quote, str) or not quote.strip():
        errors.append(
            issue("R10_QUOTE_MATCHES_LINE", object_id, "quote must be a non-empty string")
        )
        return errors

    expected = norm(quote.replace(r"\|", "|"))
    actual = norm(lines[line_number - 1])

    if expected != actual:
        errors.append(
            issue(
                "R10_QUOTE_MATCHES_LINE",
                object_id,
                f"quote does not equal the complete source line: {path_line}",
            )
        )

    return errors


def validate(data: Any, root: Path | None = None) -> list[str]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return [issue("R1_WORK_ITEM_ID", "document", "root must be a mapping")]

    if data.get("work_item_id") != "AID-2026-293":
        errors.append(issue("R1_WORK_ITEM_ID", "AID-2026-293",
                            "work_item_id must equal AID-2026-293"))

    risks = data.get("risks")
    if not isinstance(risks, list):
        errors.append(issue("R2_RISK_REGISTER", "risks", "risks must be a list"))
        risks = []
    risk_ids = [r.get("id") for r in risks if isinstance(r, dict)]
    if set(risk_ids) != RISK_IDS or len(risk_ids) != 10:
        errors.append(issue("R2_RISK_REGISTER", "risks",
                            "must contain exactly one each of R-01..R-10"))

    for risk in risks:
        if not isinstance(risk, dict):
            continue
        rid = str(risk.get("id", "UNKNOWN"))
        state = risk.get("evidence_state")
        if state not in VALID_EVIDENCE_STATES:
            errors.append(issue("R3_RISK_EVIDENCE_STATE", rid,
                                "evidence_state is not a supported state"))
            continue
        if state == "PATH_LINE":
            if not is_path_line(risk.get("path_line")):
                errors.append(issue("R3_RISK_EVIDENCE_STATE", rid,
                                    "PATH_LINE requires path_line in path:line form"))
            if not isinstance(risk.get("quote"), str) or not risk["quote"].strip():
                errors.append(issue("R3_RISK_EVIDENCE_STATE", rid,
                                    "PATH_LINE requires a non-empty verbatim quote"))
            errors.extend(validate_source_evidence(risk, rid, root))
        elif state == "NO_EVIDENCE_FOUND":
            if not isinstance(risk.get("search_command"), str) or not risk["search_command"].strip():
                errors.append(issue("R3_RISK_EVIDENCE_STATE", rid,
                                    "NO_EVIDENCE_FOUND requires executed search_command"))
            if not isinstance(risk.get("search_scope"), str) or not risk["search_scope"].strip():
                errors.append(issue("R3_RISK_EVIDENCE_STATE", rid,
                                    "NO_EVIDENCE_FOUND requires search_scope"))
            if risk.get("search_executed") is not True:
                errors.append(issue("R3_RISK_EVIDENCE_STATE", rid,
                                    "search_executed must be true"))
        elif state == "PENDING_SEARCH_EXECUTION":
            if not isinstance(risk.get("planned_search_command"), str) or not risk["planned_search_command"].strip():
                errors.append(issue("R3_RISK_EVIDENCE_STATE", rid,
                                    "pending state requires planned_search_command"))

        if "additional_evidence" in risk:
            additional = risk["additional_evidence"]
            if not isinstance(additional, list):
                errors.append(
                    issue(
                        "R8_PATH_EXISTS",
                        rid,
                        "additional_evidence must be a list",
                    )
                )
            else:
                for index, evidence in enumerate(additional):
                    evidence_id = f"{rid}.additional_evidence[{index}]"
                    errors.extend(validate_source_evidence(evidence, evidence_id, root))

    modules = data.get("modules")
    if not isinstance(modules, list):
        errors.append(issue("R4_MODULE_COVERAGE", "modules", "modules must be a list"))
        modules = []
    module_ids = [m.get("id") for m in modules if isinstance(m, dict)]
    if set(module_ids) != MODULE_IDS or len(module_ids) != len(MODULE_IDS):
        errors.append(issue("R4_MODULE_COVERAGE", "modules",
                            "must contain exactly A,B,C,D,E,F,G,H,I,Storage"))

    for module in modules:
        if not isinstance(module, dict):
            continue
        mid = str(module.get("id", "UNKNOWN"))
        scores = module.get("scores")
        if not isinstance(scores, dict) or set(scores) != DIMENSIONS:
            errors.append(issue("R5_FOUR_DIMENSION_SCORES", mid,
                                "scores must contain exactly four named dimensions"))
            continue
        for dim in sorted(DIMENSIONS):
            value = scores.get(dim)
            if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 5:
                errors.append(issue("R5_FOUR_DIMENSION_SCORES", mid,
                                    f"{dim} must be an integer from 1 to 5"))

        if not is_path_line(module.get("path_line")):
            gap = module.get("evidence_gap")
            if not isinstance(gap, str) or not gap.strip():
                errors.append(issue("R6_MODULE_EVIDENCE", mid,
                                    "requires path_line or non-empty EVIDENCE_GAP"))
            elif not gap.startswith("EVIDENCE_GAP:"):
                errors.append(issue("R6_MODULE_EVIDENCE", mid,
                                    "evidence_gap must start with EVIDENCE_GAP:"))

    statuses = data.get("statuses")
    if not isinstance(statuses, dict):
        errors.append(issue("R7_AC6_AC8_PENDING", "statuses",
                            "statuses must be a mapping"))
    else:
        actual_keys = set(statuses)
        expected_keys = set(STATUS_VALUES)
        if actual_keys != expected_keys:
            errors.append(
                issue(
                    "R7_AC6_AC8_PENDING",
                    "statuses",
                    f"must contain exactly these fields: {','.join(sorted(expected_keys))}",
                )
            )

        for field, allowed_values in STATUS_VALUES.items():
            value = statuses.get(field)
            if value not in allowed_values:
                errors.append(
                    issue(
                        "R7_AC6_AC8_PENDING",
                        field,
                        f"unsupported status value; expected one of {','.join(sorted(allowed_values))}",
                    )
                )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="repository root")
    parser.add_argument("--data", required=True, help="YAML carrier data file")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    data_path = Path(args.data)
    if not data_path.is_absolute():
        data_path = root / data_path

    try:
        raw = yaml.safe_load(data_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        print(f"ERROR: cannot read YAML data: {exc}", file=sys.stderr)
        return 2

    errors = validate(raw, root=root)
    if errors:
        for item in errors:
            print(item)
        return 1

    print("AID-2026-293 CARRIER CHECK PASS")
    print("R1-R10: 10/10 structural and source-evidence rules satisfied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
