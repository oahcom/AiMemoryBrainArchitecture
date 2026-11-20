#!/usr/bin/env python3
"""Self-check for scripts/check_document_management.py.

Negative cases matter more than positive ones here: the parser is the trust
root, so every input outside the declared subset must fail, not degrade.

    python3 scripts/test_check_document_management.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_document_management import (  # noqa: E402
    NO_AUTHORITATIVE_SOURCE,
    check_document,
    main as gate_main,
    read_metadata,
    resolve_canonical,
)

FILE = Path("synthetic.md")
RESULTS: list[bool] = []


def doc(body: str) -> str:
    return f"---\ndocument_metadata:\n{body}\n---\n\n# Title\n"


BASE = """
  domain: architecture
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    normative_status: Informative
"""

APPROVED = """
  domain: architecture
  role: design-specification
  lifecycle:
    approval:
      decision_status: Approved
      approved_version:
        scheme: git
        value: "deadbeef"
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    normative_status: Informative
"""

CANONICAL = """
  domain: architecture
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Draft
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Canonical
    canonical_scope: "Architecture: data model design"
    canonical_scope_id: "architecture/data-model-design"
    canonical_scope_keywords:
      - data-model
      - entity
    canonical_conflict_status: None
    normative_status: Normative
"""


def record(name: str, ok: bool, detail: str = "") -> None:
    print(f"  [{'ok  ' if ok else 'FAIL'}] {name}{detail if not ok else ''}")
    RESULTS.append(ok)


def expect(name: str, text: str, needle: str = "", expect_clean: bool = False) -> None:
    errors, _ = check_document(FILE, text)
    if expect_clean:
        record(name, not errors, f"  unexpected: {errors}")
        return
    ok = any(needle in e for e in errors) if needle else bool(errors)
    record(name, ok, f"  expected {needle!r}, got {errors}")


def run_gate(root: Path, *extra: str) -> int:
    argv = sys.argv
    sys.argv = ["gate", "--root", str(root), *extra]
    try:
        return gate_main()
    finally:
        sys.argv = argv


def expect_gate(name: str, root: Path, want: int, *extra: str) -> None:
    code = run_gate(root, *extra)
    record(name, code == want, f"  gate returned {code}, expected {want}")


# --------------------------------------------------------------------------
# 1. Parser: anything outside the subset must fail (P0-1)
# --------------------------------------------------------------------------

PARSER_REJECTS = {
    "line with no colon": BASE + "\n  this is not valid mapping syntax",
    "duplicate key": BASE + "\n  role: reference",
    "block scalar": BASE + "\n  description: |\n    two lines",
    "flow sequence with content": BASE + "\n  tags: [a, b]",
    "anchor": BASE + "\n  role: &anchor design-specification",
    "tab indentation": BASE.replace("  role:", "\trole:"),
    "sequence item inside mapping": BASE + "\n  - orphan",
    "mapping inside sequence": """
  domain: architecture
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
    usage_status: Active
    modification_status: Unchanged
    evidence_reference:
      - reason: nope
  authority:
    canonical_status: Non-Canonical
    normative_status: Informative
""",
    "unterminated double quote": BASE.replace(
        "role: design-specification", 'role: "design-specification'
    ),
    "dedent inside the block": BASE + "\nlower_indent: true",
    "metadata as scalar": "---\ndocument_metadata: nope\n---\n\n# T\n",
    "empty block": "---\ndocument_metadata:\n---\n\n# T\n",
    "unclosed frontmatter": "---\ndocument_metadata:\n" + BASE + "\n# T\n",
}


def run_parser() -> None:
    print("parser (fail-closed)")
    for name, text in PARSER_REJECTS.items():
        expect(f"rejects {name}",
               text if text.startswith("---") else doc(text), "DM-01")
    quoted = BASE.replace(
        "role: design-specification",
        'role: design-specification\n  evidence: "a \\"quoted\\" # not a comment"',
    )
    meta = read_metadata(doc(quoted))
    record(
        'quoted "#" survives comment stripping',
        (meta or {}).get("evidence") == 'a "quoted" # not a comment',
        f"  got {(meta or {}).get('evidence')!r}",
    )
    expect("baseline conforms", doc(BASE), expect_clean=True)


# --------------------------------------------------------------------------
# 2. Field rules
# --------------------------------------------------------------------------

def run_fields() -> None:
    print("field rules")
    expect("bad domain rejected", doc(BASE.replace("architecture", "misc")), "DM-02")
    expect("unknown key rejected", doc(BASE + "\n  lifecycle_status: Active"), "unknown key")
    expect("Approved without version rejected", doc(APPROVED.replace(
        '      approved_version:\n        scheme: git\n        value: "deadbeef"\n', ""
    )), "DM-03")
    expect("Selected-sections without sections rejected", doc(APPROVED.replace(
        "type: Full-document", "type: Selected-sections"
    )), "DM-03")
    expect("Revoked without decision id rejected", doc(BASE.replace(
        "decision_status: Draft", "decision_status: Revoked\n      revocation: null"
    )), "DM-04")
    expect("Archived without reason rejected", doc(BASE.replace(
        "usage_status: Active",
        'usage_status: Archived\n    archival:\n      archived_date: "2026-01-01"',
    )), "DM-05")
    expect("unnormalized scope id rejected", doc(CANONICAL.replace(
        "architecture/data-model-design", "Architecture Data Model"
    )), "DM-06")
    expect("scope prefix must equal domain", doc(CANONICAL.replace(
        "architecture/data-model-design", "protocol/data-model-design"
    )), "DM-06")
    expect("Canonical without keywords rejected", doc(CANONICAL.replace(
        "    canonical_scope_keywords:\n      - data-model\n      - entity\n", ""
    )), "DM-06")
    expect("nested hand-written superseded_by rejected", doc(BASE.replace(
        "    approval:\n      decision_status: Draft",
        "    supersession:\n      superseded_by:\n        - docs/x.md\n"
        "    approval:\n      decision_status: Draft",
    )), "DM-08")
    expect("conflict state must not be Canonical", doc(CANONICAL.replace(
        "canonical_conflict_status: None", "canonical_conflict_status: Under-Review"
    )), "DM-11")
    expect("Resolved requires a record", doc(CANONICAL.replace(
        "canonical_conflict_status: None", "canonical_conflict_status: Resolved"
    )), "DM-11")
    expect("generated artifact must not be Normative", (
        "---\ndocument_metadata:" + CANONICAL + "---\n\n"
        "<!-- GENERATED FILE - DO NOT EDIT -->\n# Inventory\n"
    ), "DM-09")
    expect("Canonical conforms", doc(CANONICAL), expect_clean=True)


# --------------------------------------------------------------------------
# 3. A2 resolver: never guesses
# --------------------------------------------------------------------------

def run_resolver() -> None:
    print("resolve_canonical")
    one = {"a.md": read_metadata(doc(CANONICAL))}
    record("unique Canonical resolves", resolve_canonical(one, "architecture/data-model-design") == "a.md")

    second = read_metadata(doc(CANONICAL))
    two = {"a.md": read_metadata(doc(CANONICAL)), "b.md": second}
    record(
        "two Canonical documents resolve to nothing",
        resolve_canonical(two, "architecture/data-model-design") == NO_AUTHORITATIVE_SOURCE,
    )

    conflicted = read_metadata(doc(CANONICAL))
    conflicted["authority"]["canonical_conflict_status"] = "Under-Review"
    conflicted["authority"]["canonical_status"] = "Candidate"
    record(
        "unresolved conflict resolves to nothing",
        resolve_canonical({"a.md": conflicted}, "architecture/data-model-design")
        == NO_AUTHORITATIVE_SOURCE,
    )
    record(
        "unknown scope resolves to nothing",
        resolve_canonical(one, "architecture/unknown-scope") == NO_AUTHORITATIVE_SOURCE,
    )


# --------------------------------------------------------------------------
# 4. Repository-wide rules
# --------------------------------------------------------------------------

def _repo(tmp: str) -> Path:
    root = Path(tmp)
    (root / "00-governance").mkdir(parents=True)
    return root


def run_repository_rules() -> None:
    print("repository rules")
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        for name in ("a.md", "b.md"):
            (root / "00-governance" / name).write_text(doc(CANONICAL), encoding="utf-8")
        expect_gate("DM-07 duplicate Canonical scope fails", root, 1)

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "a.md").write_text(doc(CANONICAL), encoding="utf-8")
        (root / "00-governance" / "b.md").write_text(
            doc(BASE.replace(
                "canonical_status: Non-Canonical",
                "canonical_status: Non-Canonical\n    bilingual_counterpart:\n"
                '      en: "00-governance/missing.md"',
            )), encoding="utf-8")
        expect_gate("DM-12 missing counterpart fails", root, 1)

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "a.md").write_text(doc(BASE.replace(
            "    approval:\n      decision_status: Draft",
            "    supersession:\n      supersedes:\n        - 00-governance/gone.md\n"
            "    approval:\n      decision_status: Draft",
        )), encoding="utf-8")
        expect_gate("DM-13 missing supersedes target fails", root, 1)

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        for name, other in (("a.md", "b.md"), ("b.md", "a.md")):
            (root / "00-governance" / name).write_text(doc(BASE.replace(
                "    approval:\n      decision_status: Draft",
                f"    supersession:\n      supersedes:\n        - 00-governance/{other}\n"
                "    approval:\n      decision_status: Draft",
            )), encoding="utf-8")
        expect_gate("DM-13 cycle fails", root, 1)

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "a.md").write_text(doc(BASE), encoding="utf-8")
        (root / "00-governance" / "b.md").write_text("# no metadata\n", encoding="utf-8")
        expect_gate("unclassified is only a gap by default", root, 0)
        expect_gate("--strict rejects unclassified", root, 1, "--strict")


# --------------------------------------------------------------------------
# 5. DM-10: approval is bound to a version (P0-2)
# --------------------------------------------------------------------------

def _git(root: Path, *args: str) -> str:
    out = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=True
    )
    return out.stdout.strip()


def run_approval_binding() -> None:
    print("DM-10 version-bound approval")
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        target = root / "00-governance" / "a.md"

        body_approved = "body: approved text"
        template = doc(APPROVED.replace('"deadbeef"', '"SHA"'))
        target.write_text(template.replace("# Title", body_approved), encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "approved")
        sha = _git(root, "rev-parse", "HEAD")
        target.write_text(
            template.replace('"SHA"', f'"{sha}"').replace("# Title", body_approved),
            encoding="utf-8",
        )
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "record approval")
        expect_gate("unchanged body keeps approval valid", root, 0)

        target.write_text(
            template.replace('"SHA"', f'"{sha}"').replace("# Title", "edited text"),
            encoding="utf-8",
        )
        expect_gate("edited body invalidates approval", root, 1)

        honest = (
            target.read_text(encoding="utf-8")
            .replace("modification_status: Unchanged", "modification_status: Pending-Reapproval")
            .replace(
                "approval_applicability: Applicable-To-Current-Version",
                "approval_applicability: Not-Applicable-To-Current-Version",
            )
        )
        target.write_text(honest, encoding="utf-8")
        expect_gate("honest downgrade is accepted", root, 0)

        unknown = honest.replace(f'"{sha}"', '"0000000000000000000000000000000000000000"')
        target.write_text(unknown, encoding="utf-8")
        expect_gate("unresolvable approved_version fails", root, 1)


def main() -> int:
    print("check_document_management self-check")
    run_parser()
    run_fields()
    run_resolver()
    run_repository_rules()
    run_approval_binding()
    passed, total = sum(RESULTS), len(RESULTS)
    print(f"{passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
