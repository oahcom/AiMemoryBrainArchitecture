#!/usr/bin/env python3
"""Audit GitHub Actions workflows for self-hosted admission violations.

Document: DOC-OPS-001 section 4, AI-RUN-002-RUNBOOK section 4.1.
Policy: a workflow whose job targets a self-hosted runner MUST be reachable only
through workflow_dispatch, schedule, or a push restricted to refs/heads/main.

This is the L2 (repository) layer of admission control. The L1 (service) layer is
a job-started hook on the runner host, and it is the one that actually blocks
execution; this audit exists so violations are visible before merge.

Exit status: 0 = clean, 1 = at least one violation, 2 = the audit itself failed.
"""

from __future__ import annotations

import argparse
import json
import os

import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - surfaced as exit 2
    print("audit: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

ALLOWED_EVENTS = {"workflow_dispatch", "schedule", "push"}
TRUSTED_PUSH_BRANCHES = {"main"}
WORKFLOW_DIR = Path(".github/workflows")
SELF_HOSTED = "self-hosted"


def load_workflow(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError("workflow is not a mapping")
    return data


def triggers_of(workflow: dict) -> dict:
    """Normalize the `on:` key. PyYAML resolves a bare `on` to the boolean True."""
    raw = workflow.get("on", workflow.get(True))
    if raw is None:
        return {}
    if isinstance(raw, str):
        return {raw: None}
    if isinstance(raw, list):
        return {str(item): None for item in raw}
    if isinstance(raw, dict):
        return {str(key): value for key, value in raw.items()}
    raise ValueError("unrecognized `on:` shape")


def iter_jobs(workflow: dict):
    jobs = workflow.get("jobs") or {}
    if not isinstance(jobs, dict):
        return
    for job_id, job in jobs.items():
        if isinstance(job, dict):
            yield str(job_id), job


def targets_self_hosted(job: dict) -> tuple[bool, str | None]:
    """Return (is_self_hosted, unevaluable_reason)."""
    runs_on = job.get("runs-on")
    if runs_on is None:
        return False, None
    values: list[str] = []
    if isinstance(runs_on, str):
        values = [runs_on]
    elif isinstance(runs_on, list):
        values = [str(item) for item in runs_on]
    else:
        return False, None

    for value in values:
        if "${{" in value:
            return True, "runs-on uses an expression; the target cannot be audited"
    return SELF_HOSTED in values, None


def branch_filters(push_cfg) -> list[str]:
    if not isinstance(push_cfg, dict):
        return []
    branches = push_cfg.get("branches")
    if isinstance(branches, str):
        return [branches]
    if isinstance(branches, list):
        return [str(item) for item in branches]
    return []


def audit_file(path: Path) -> list[str]:
    problems: list[str] = []
    try:
        workflow = load_workflow(path)
    except Exception as exc:  # noqa: BLE001 - report, do not crash the audit
        return [f"cannot parse workflow: {type(exc).__name__}: {exc}"]

    try:
        triggers = triggers_of(workflow)
    except ValueError as exc:
        return [str(exc)]

    self_hosted_jobs = []
    for job_id, job in iter_jobs(workflow):
        is_self_hosted, reason = targets_self_hosted(job)
        if is_self_hosted:
            self_hosted_jobs.append(job_id)
            if reason:
                problems.append(f"job `{job_id}`: {reason}")

    if not self_hosted_jobs:
        return problems

    untrusted = sorted(name for name in triggers if name not in ALLOWED_EVENTS)
    if untrusted:
        problems.append(
            "self-hosted jobs are reachable from untrusted trigger(s): "
            + ", ".join(untrusted)
            + "; allowed triggers are workflow_dispatch, schedule, push(branches: [main])"
        )

    if not triggers:
        problems.append("no `on:` triggers declared; self-hosted reachability is undefined")

    if "push" in triggers:
        branches = branch_filters(triggers["push"])
        if not branches:
            problems.append(
                "`push` has no `branches:` filter, so any branch push can reach the runner"
            )
        else:
            extra = sorted(set(branches) - TRUSTED_PUSH_BRANCHES)
            if extra:
                problems.append(
                    "`push.branches` includes untrusted ref(s): " + ", ".join(extra)
                )

    if "pull_request_target" in triggers:
        problems.append(
            "`pull_request_target` runs with a write token and repository secrets; "
            "it MUST NOT share a workflow with self-hosted jobs"
        )

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root (default: .)")
    parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    workflow_dir = root / WORKFLOW_DIR
    if not workflow_dir.is_dir():
        print(f"audit: no {WORKFLOW_DIR} directory under {root}; nothing to audit")
        return 0

    results: dict[str, dict] = {}
    violations = 0
    for path in sorted(list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))):
        problems = audit_file(path)
        rel = str(path.relative_to(root)).replace(os.sep, "/")
        results[rel] = {"problems": problems}
        if problems:
            violations += len(problems)

    if args.json:
        print(json.dumps({"violations": violations, "workflows": results}, indent=2))
    else:
        audited = len(results)
        if not violations:
            print(f"runner admission: OK — {audited} workflow(s) audited, no violations")
        else:
            print(f"runner admission: FAILED — {violations} violation(s) in {audited} workflow(s)")
            for rel, result in results.items():
                for problem in result["problems"]:
                    print(f"  {rel}: {problem}")
            print()
            print("Remediation: self-hosted jobs must be reachable only via")
            print("  on: workflow_dispatch")
            print("  on: schedule")
            print("  on: push: branches: [main]")
            print("Move untrusted-event jobs to GitHub-hosted runners, or split them into a")
            print("separate workflow that does not target self-hosted.")

    return 0 if violations == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - audit failures must be loud but distinct
        print(f"audit: internal failure: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(2)
