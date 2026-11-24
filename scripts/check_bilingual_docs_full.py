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

sys.path.insert(0, str(Path(__file__).resolve().parent))
# GOV-DOC-001 has exactly one authority for "what is normative" and "what is
# exempt": the incremental, required gate. This file is a whole-repository
# inventory over that authority, so it reads the constants instead of keeping
# copies. The copies are why the two scripts disagreed about the same bytes:
# this one named seven directories that do not exist (03-memory-brain,
# 05-memory-runtime, 08-protocols, 09-storage-and-index,
# 10-security-and-governance, 11-consistency-and-recovery,
# 12-testing-and-acceptance), omitted the real 08-bmcp-protocol root, and
# carried an 18-entry exemption list against the authority's 21.
from check_bilingual_docs import (
    EMBEDDED_BILINGUAL_SOURCES,
    NORMATIVE_ROOTS,
    PAIR_EXEMPT_PREFIXES,
)

ROOT = Path(__file__).resolve().parents[1]

# The authority keeps NORMATIVE_ROOTS as a literal, so the literal can still
# drift from the tree in silence. Deriving the set from disk turns that drift
# into a gate failure instead of a wrong verdict.
_DERIVED_ROOTS = {
    path.name
    for path in ROOT.iterdir()
    if path.is_dir() and path.name[:2].isdigit() and path.name[2:3] == "-"
}
if _DERIVED_ROOTS != NORMATIVE_ROOTS:
    sys.stderr.write(
        "GOV-DOC-001 root sets disagree: check_bilingual_docs.NORMATIVE_ROOTS="
        f"{sorted(NORMATIVE_ROOTS)} but the tree has {sorted(_DERIVED_ROOTS)}\n"
    )
    sys.exit(2)


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
    if path.startswith(PAIR_EXEMPT_PREFIXES):
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
        # Side-by-side pairing applies to every normative root, not only
        # 14-ai-development. Without this branch the full scan called every
        # side-by-side pair outside 14-ai-development a violation while the
        # incremental gate called the same file clean, so the two required
        # contexts disagreed about the same bytes.
        if path.endswith(".en.md"):
            stem = path[:-6]
            return next(
                (
                    candidate
                    for candidate in (stem + ".zh-CN.md", stem + ".md")
                    if candidate != path and candidate in files
                ),
                None,
            )
        if path.endswith(".zh-CN.md"):
            stem = path[:-9]
            return next(
                (
                    candidate
                    for candidate in (stem + ".en.md", stem + ".md")
                    if candidate != path and candidate in files
                ),
                None,
            )
        stem = path[:-3]
        for candidate in (stem + ".en.md", stem + ".zh-CN.md"):
            if candidate != path and candidate in files:
                return candidate
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
        # `docs` is already Markdown-only, so the authority's asset suffixes
        # cannot match here and are not consulted.
        if path in EMBEDDED_BILINGUAL_SOURCES:
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
            f"| {i} | `{src}` | `{want}` |"
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
