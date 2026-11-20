#!/usr/bin/env python3
"""Full-repository structural inventory for GOV-DOC-001 bilingual docs.

This is a path/coverage checker, not a semantic translation or Owner-approval
checker. It scans tracked Markdown files and reports missing counterpart paths.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

NORMATIVE_ROOTS = {
    "00-governance", "01-system-architecture", "02-domain-model",
    "03-memory-brain", "04-memory-compiler", "05-memory-runtime",
    "06-memory-context", "07-agent-integration", "08-protocols",
    "09-storage-and-index", "10-security-and-governance",
    "11-consistency-and-recovery", "12-testing-and-acceptance",
    "13-engineering-decisions", "14-ai-development",
}
EMBEDDED_BILINGUAL = {
    "00-governance/bilingual-documentation-policy.md",
    "00-governance/drafts/GOV-DOC-001-v1.2-DRAFT.md",
    "00-governance/bilingual-governance-migration-register.md",
    "00-governance/templates/bilingual-issue-template.md",
    "00-governance/templates/bilingual-umbrella-requirement-template.md",
    "00-governance/templates/bilingual-commit-message.md",
    "00-governance/templates/repository-policy-inheritance.md",
    "00-governance/reports/bilingual-baseline-remediation-report.md",
    "00-governance/reports/f06-object-reconciliation.md",
    "14-ai-development/ai-development-standard.md",
    "14-ai-development/AI-EXEC-UNIFICATION-RULING-001.md",
    "14-ai-development/AI-EXEC-INDEPENDENCE-RULING-001.md",
    "14-ai-development/PR-GOVERNANCE-001.md",
    "14-ai-development/prompt-and-evidence-template.md",
    "14-ai-development/prompt-authoring-standard.md",
    "14-ai-development/iteration-lifecycle.md",
    "14-ai-development/owner-automation-operating-model.md",
    "14-ai-development/README.md",
}
OPERATIONAL_EXEMPT_PREFIXES = (
    "14-ai-development/work-items/",
    "14-ai-development/prompts/",
    "14-ai-development/adr/",
)
ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".svg", ".drawio"}


def tracked_paths(paths_file: str | None) -> set[str]:
    if paths_file:
        raw = Path(paths_file).read_text(encoding="utf-8").splitlines()
    else:
        result = subprocess.run(
            ["git", "ls-files", "-z"], check=True, capture_output=True
        )
        raw = result.stdout.decode("utf-8").split("\0")
    return {p.strip().replace("\\", "/") for p in raw if p.strip()}


def in_scope(path: str) -> bool:
    if Path(path).suffix.lower() != ".md":
        return False
    return (
        any(path.startswith(root + "/") for root in NORMATIVE_ROOTS)
        or path.startswith("docs/en/")
        or path.startswith("docs/zh-CN/")
    )


def counterpart(path: str, files: set[str]) -> str | None:
    if path.startswith(OPERATIONAL_EXEMPT_PREFIXES):
        return "EXEMPT: operational record/template subtree"
    if (
        path.startswith("14-ai-development/")
        or path.startswith("docs/en/14-ai-development/")
        or path.startswith("docs/zh-CN/14-ai-development/")
    ):
        if path.endswith(".en.md"):
            stem = path[:-6]
            return next(
                (p for p in (stem + ".zh-CN.md", stem + ".md") if p != path and p in files),
                None,
            )
        if path.endswith(".zh-CN.md"):
            candidate = path[:-9] + ".en.md"
            return candidate if candidate in files else None
        if path.startswith("14-ai-development/"):
            stem = path[:-3] if path.endswith(".md") else path
            for candidate in (
                stem + ".en.md",
                stem + ".zh-CN.md",
                "docs/en/" + path,
            ):
                if candidate != path and candidate in files:
                    return candidate
            return None
        rest = path.removeprefix("docs/en/").removeprefix("docs/zh-CN/")
        other = (
            "docs/zh-CN/" if path.startswith("docs/en/") else "docs/en/"
        ) + rest
        if rest in files:
            return rest
        return other if other in files else None
    if path.startswith("docs/en/"):
        candidate = "docs/zh-CN/" + path[len("docs/en/"):]
        return candidate if candidate in files else None
    if path.startswith("docs/zh-CN/"):
        candidate = "docs/en/" + path[len("docs/zh-CN/"):]
        return candidate if candidate in files else None
    if any(path.startswith(root + "/") for root in NORMATIVE_ROOTS):
        en = "docs/en/" + path
        zh = "docs/zh-CN/" + path
        if en in files and zh in files:
            return f"{en} + {zh}"
        return None
    return "EXEMPT: outside normative roots"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--paths-file",
        help="newline-delimited tracked path snapshot; default uses git ls-files",
    )
    parser.add_argument(
        "--report", help="write the full violation inventory as Markdown"
    )
    parser.add_argument(
        "--source-revision", help="commit SHA represented by --paths-file"
    )
    args = parser.parse_args()
    try:
        files = tracked_paths(args.paths_file)
    except (OSError, subprocess.CalledProcessError, UnicodeError) as exc:
        print(f"ERROR: cannot enumerate tracked files: {exc}")
        return 2

    docs = sorted(p for p in files if in_scope(p))
    violations: list[tuple[str, str]] = []
    excluded = 0
    for path in docs:
        if path in EMBEDDED_BILINGUAL or Path(path).suffix.lower() in ASSET_SUFFIXES:
            excluded += 1
            continue
        expected = counterpart(path, files)
        if expected and expected.startswith("EXEMPT:"):
            excluded += 1
        elif not expected:
            if path.startswith("14-ai-development/") and path.endswith(".md"):
                expected_path = (
                    "side-by-side .en.md/.zh-CN.md or docs/en/14-ai-development mirror"
                )
            elif path.startswith("docs/en/"):
                expected_path = "docs/zh-CN/" + path[len("docs/en/"):]
            elif path.startswith("docs/zh-CN/"):
                expected_path = "docs/en/" + path[len("docs/zh-CN/"):]
            else:
                expected_path = (
                    "docs/en/" + path + " AND docs/zh-CN/" + path
                )
            violations.append((path, expected_path))

    lines = [
        "# GOV-DOC-001 full-repository structural inventory",
        "",
        f"- Source revision: {args.source_revision or 'working tree'}",
        f"- Tracked paths: {len(files)}",
        f"- In-scope Markdown files: {len(docs)}",
        f"- Explicitly excluded/in-policy-exempt files: {excluded}",
        f"- Violations: {len(violations)}",
        "",
    ]
    if violations:
        lines += [
            "| # | Source path | Missing counterpart |",
            "|---:|---|---|",
        ]
        lines += [
            f"| {i} | \`{src}\` | \`{want}\` |"
            for i, (src, want) in enumerate(violations, 1)
        ]
    else:
        lines.append("No missing structural counterpart paths found.")
    report = "\n".join(lines) + "\n"
    if args.report:
        Path(args.report).write_text(report, encoding="utf-8")

    print(
        f"GOV-DOC-001 full scan: {len(docs)} in-scope Markdown files; "
        f"{excluded} exempt; {len(violations)} violations."
    )
    if violations:
        for i, (src, want) in enumerate(violations, 1):
            print(f"{i:03d}. {src} -> {want}")
        print("GOV-DOC-001 full scan: FAIL")
        return 1
    print("GOV-DOC-001 full scan: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
