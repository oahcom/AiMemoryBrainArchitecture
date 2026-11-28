#!/usr/bin/env python3
"""Structural carrier validator for AID-2026-293.

Exit codes:
  0: all structural rules pass
  1: one or more carrier rules fail
  2: invalid CLI arguments or unreadable input
"""
from __future__ import annotations

import argparse
import re
import sys
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


def issue(rule: str, object_id: str, reason: str) -> str:
    return f"{rule} {object_id} {reason}"


def is_path_line(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    return re.fullmatch(r".+:\d+", value.strip()) is not None


def validate(data: Any) -> list[str]:
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
        if statuses.get("ac6_negative_cases") != "PENDING_COORDINATOR_EXECUTION":
            errors.append(issue("R7_AC6_AC8_PENDING", "AC6",
                                "negative cases must remain pending coordinator execution"))
        if statuses.get("ac8_independent_review") != "PENDING_INDEPENDENT_REVIEW":
            errors.append(issue("R7_AC6_AC8_PENDING", "AC8",
                                "independent review must remain pending"))

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
    except (OSError, yaml.YAMLError) as exc:
        print(f"ERROR: cannot read YAML data: {exc}", file=sys.stderr)
        return 2

    errors = validate(raw)
    if errors:
        for item in errors:
            print(item)
        return 1

    print("AID-2026-293 CARRIER CHECK PASS")
    print("R1-R7: 7/7 structural rules satisfied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
