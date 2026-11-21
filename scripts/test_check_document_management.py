#!/usr/bin/env python3
"""Self-check for scripts/check_document_management.py.

Negative cases matter more than positive ones here: the parser is the trust
root, so every input outside the declared subset must fail, not degrade.

    python3 scripts/test_check_document_management.py
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_document_management import (  # noqa: E402
    GOVERNED_FILES,
    NO_AUTHORITATIVE_SOURCE,
    ParseError,
    body_hash,
    check_document,
    governed_files,
    main as gate_main,
    parse_yaml_subset,
    read_metadata,
    rel_path,
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
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    normative_status: Informative
    canonical_conflict_status: None
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
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    normative_status: Informative
    canonical_conflict_status: None
"""

CANONICAL = """
  domain: architecture
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
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
    "unescaped single quote": BASE.replace(
        "role: design-specification", "role: 'Architecture's governance'"
    ),
    "no space after colon": BASE.replace(
        "role: design-specification", "role:design-specification"
    ),
    "unknown key under supersession": BASE.replace(
        "    approval:\n      decision_status: Draft",
        "    supersession:\n      supersedes: []\n      unauthorized_field: true\n"
        "    approval:\n      decision_status: Draft",
    ),
    "lifecycle is a string": BASE.replace(
        "  lifecycle:\n    approval:\n      decision_status: Draft\n"
        "    evidence_verification:\n      verification_status: Unverified\n"
        "    usage_status: Active\n    modification_status: Unchanged",
        "  lifecycle: unexpected-string",
    ),
}


def run_parser() -> None:
    print("parser (fail-closed)")
    for name, text in PARSER_REJECTS.items():
        expect(f"rejects {name}",
               text if text.startswith("---") else doc(text),
               "DM-02" if "unknown key" in name else "DM-01")
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
    # P0-01: a non-scalar must be an error, not an unhashable-type crash.
    expect("list-valued domain is a DM-01 error", doc(BASE.replace(
        "  domain: architecture", "  domain: []"
    )), "DM-01")
    # P1-01: an empty shell must not pass just because the keys are present.
    expect("empty lifecycle/authority shell rejected", doc("""
  domain: architecture
  role: design-specification
  lifecycle:
    approval:
  authority:
"""), "DM-01")
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

def registry_text(governed, excluded=("tools",), files=None) -> str:
    """A scope registry matching the gate's own enforced roots.

    Built from NORMATIVE_ROOTS rather than hard-coded, so the fixture stays
    valid when the real roots change; the tests that matter pass an explicit
    governed list instead.
    """
    if files is None:
        files = GOVERNED_FILES
    lines = ['registry_version: "2"', "", "governed:"]
    lines += [f"  - {name}" for name in governed]
    lines += ["", "governed_files:"]
    lines += [f"  - {rel}" for rel in files]
    lines += ["", "excluded:", ""]
    for name in excluded:
        lines.append(f"  {name}:")
        lines.append("    kind: not-documentation")
        lines.append('    reason: "not documentation"')
        lines.append('    reason_zh: "非文档"')
        lines.append("")
    lines.append("  docs:")
    lines.append("    kind: not-documentation")
    lines.append('    reason: "mirrors and one governed file only"')
    lines.append('    reason_zh: "仅镜像与一个受治理文件"')
    return "\n".join(lines) + "\n"

def gate_roots():
    import check_document_management as gate
    return list(gate.NORMATIVE_ROOTS)

ENFORCED_ROOTS = [r for r in gate_roots() if r not in ("docs/en", "docs/zh-CN")]

def gate_roots():
    import check_document_management as gate
    return list(gate.NORMATIVE_ROOTS)

def _repo(tmp: str) -> Path:
    root = Path(tmp)
    for name in gate_roots():
        (root / name).mkdir(parents=True, exist_ok=True)
    (root / "tools").mkdir(parents=True, exist_ok=True)
    (root / "00-governance" / "document-scope-registry.yaml").write_text(
        registry_text(ENFORCED_ROOTS), encoding="utf-8"
    )
    # The contract travels with the repository. The gate loads the schema from
    # --root, so a fixture repo without one is a repo that cannot be checked.
    real = Path(__file__).resolve().parents[1] / "00-governance/architecture-document-metadata.schema.yaml"
    (root / "00-governance" / real.name).write_text(
        real.read_text(encoding="utf-8"), encoding="utf-8"
    )
    # GOVERNED_FILES names files that live in an excluded directory. The fixture
    # must provide them, or DM-14 correctly reports that they do not exist.
    import check_document_management as gate
    for rel in gate.GOVERNED_FILES:
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(doc(BASE), encoding="utf-8")
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
        expect_gate(
            "unclassified is INCOMPLETE, never PASS", root, 2
        )
        expect_gate("--strict rejects unclassified", root, 1, "--strict")
        # The count must balance: every governed file is either classified or
        # backlog. A silent drop in the loop would otherwise only show up as a
        # smaller total that nobody questions.
        record(
            "T21 governed count equals classified plus unclassified",
            len(governed_files(root)) == 2 + len(GOVERNED_FILES),
            f"  governed {len(governed_files(root))}, "
            f"expected {2 + len(GOVERNED_FILES)} (2 written + "
            f"{len(GOVERNED_FILES)} fixture governed files)",
        )

    # T06 / T07: a Resolved record must select the unique Canonical document.
    resolution = (
        "    canonical_conflict_status: Resolved\n"
        "    canonical_conflict_resolution:\n"
        '      resolution_decision_id: "GOV-CONF-001"\n'
        '      resolved_date: "2026-11-20"\n'
        '      selected_document: "00-governance/a.md"\n'
        "      resolution_evidence: []"
    )
    candidate = BASE.replace(
        "canonical_status: Non-Canonical",
        'canonical_status: Candidate\n'
        '    canonical_scope_id: "architecture/data-model-design"\n'
        + resolution,
    )
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "a.md").write_text(doc(candidate), encoding="utf-8")
        expect_gate("T06 Resolved without any Canonical fails", root, 1)

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "a.md").write_text(doc(candidate), encoding="utf-8")
        (root / "00-governance" / "b.md").write_text(doc(CANONICAL), encoding="utf-8")
        expect_gate("T07 Resolved selecting a non-Canonical document fails", root, 1)

    # T09 / T10: mirror parity needs a classified, correctly named group.
    def with_block(extra: str) -> str:
        return BASE + "\n  bilingual_counterpart:\n" + extra

    source_block = (
        '    en: "docs/en/a.md"\n'
        '    zh-CN: "docs/zh-CN/a.md"'
    )
    mirror_block = '    source: "00-governance/a.md"'

    def write_group(root: Path, *, source: str | None, mirrors: dict[str, str | None]):
        (root / "docs" / "en").mkdir(parents=True, exist_ok=True)
        (root / "docs" / "zh-CN").mkdir(parents=True, exist_ok=True)
        if source is not None:
            (root / "00-governance" / "a.md").write_text(
                doc(with_block(source)), encoding="utf-8")
        for lang, body in mirrors.items():
            p = root / "docs" / lang / "a.md"
            if body is None:
                p.write_text("---\ntitle: no metadata\n---\n\n# T\n", encoding="utf-8")
            else:
                p.write_text(doc(with_block(body)), encoding="utf-8")

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        write_group(root, source=source_block, mirrors={"en": None, "zh-CN": mirror_block})
        expect_gate("T09 counterpart without metadata fails", root, 1)

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        write_group(root, source=source_block,
                    mirrors={"en": "", "zh-CN": mirror_block})
        expect_gate("T10 counterpart not naming its source fails", root, 1)

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        write_group(root, source=source_block,
                    mirrors={"en": mirror_block, "zh-CN": mirror_block})
        expect_gate("T12 symmetric source/mirror group conforms", root, 0)

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        # Source lists only en; zh-CN still claims it: a missing third party.
        write_group(root, source='    en: "docs/en/a.md"',
                    mirrors={"en": mirror_block, "zh-CN": mirror_block})
        expect_gate("T13 unlisted third mirror fails", root, 1)

    # T08: the generated marker counts anywhere in the body, not just line 1-8.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        padding = "\n".join(f"line {i}" for i in range(9))
        (root / "00-governance" / "a.md").write_text(
            "---\ndocument_metadata:" + CANONICAL + "---\n\n" + padding
            + "\n<!-- GENERATED FILE - DO NOT EDIT -->\n",
            encoding="utf-8",
        )
        expect_gate("T08 generated marker after line 8 fails", root, 1)


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

        # T11: a branch name is not a commit id; it can move.
        moving = honest.replace(f'"{sha}"', '"main"')
        target.write_text(moving, encoding="utf-8")
        expect_gate("T11 mutable ref as approved_version fails", root, 1)


def run_changed_paths() -> None:
    """T01: a filename with a space must not dodge --require-changed."""
    print("changed-path parsing")
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        (root / "00-governance" / "seed.md").write_text(doc(BASE), encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed")
        base = _git(root, "rev-parse", "HEAD")
        (root / "00-governance" / "new policy.md").write_text("# no metadata\n", encoding="utf-8")
        expect_gate(
            "T01 spaced filename without metadata fails",
            root, 1, "--require-changed", base,
        )


def run_path_safety() -> None:
    """T14/T15: a path reference is validated, never silently rewritten.

    `lstrip("./")` takes a character set, so "../../x.md" would collapse to
    "x.md" and an illegal reference would become a legal-looking one.
    """
    print("path normalisation")
    for bad in (
        "../../00-governance/a.md",
        "/etc/passwd",
        "C:/Windows/system.ini",
        "././00-governance/a.md",
        "00-governance/../../etc/passwd",
        "a//b.md",
        "./a.md/",
        "..\\..\\a.md",
        "a.md\x00b.md",
    ):
        errs: list[str] = []
        got = rel_path(bad, "test", errs)
        record(
            f"T14 rejects unsafe path {bad!r}",
            got is None and bool(errs),
            f"  got {got!r}, errors {errs}",
        )
    record("T14 accepts a clean relative path",
           rel_path("00-governance/a.md", "test", []) == "00-governance/a.md")
    record("T14 accepts a single ./ prefix",
           rel_path("./00-governance/a.md", "test", []) == "00-governance/a.md")

def run_body_hash_equivalence() -> None:
    """T16: only the equivalences the policy names may collapse two bodies."""
    print("body hash equivalence")
    record("T16 CRLF is the same body as LF",
           body_hash("a\r\nb\r\n") == body_hash("a\nb\n"))
    record("T16 bare CR is the same body as LF",
           body_hash("a\rb\r") == body_hash("a\nb\n"))
    record("T16 trailing spaces are ignored",
           body_hash("a  \nb\t\n") == body_hash("a\nb\n"))
    record("T16 leading blank lines are ignored",
           body_hash("\n\na\nb\n") == body_hash("a\nb\n"))
    record("T16 leading spaces on a non-blank line are NOT ignored",
           body_hash("  a\n") != body_hash("a\n"))
    for name, sep in (("U+2028", "\u2028"), ("U+2029", "\u2029"),
                      ("U+000B", "\x0b"), ("U+000C", "\x0c"),
                      ("U+001C", "\x1c"), ("U+0085", "\x85")):
        record(
            f"T16 {name} is NOT a line break",
            body_hash(f"alpha{sep}beta") != body_hash("alpha\nbeta"),
            "  a Unicode line separator collapsed two different bodies",
        )

def run_bilingual_closure() -> None:
    """T17/T18: a mirror whose source declares nothing is an error."""
    print("DM-12 group closure")
    mirror = (
        "  domain: architecture\n"
        "  role: design-specification\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    normative_status: Informative\n"
        "    canonical_conflict_status: None\n"
    )
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "docs" / "en" / "00-governance").mkdir(parents=True)
        (root / "docs" / "zh-CN" / "00-governance").mkdir(parents=True)
        # Source exists and is classified, but declares no counterpart at all.
        (root / "00-governance" / "src.md").write_text(doc(mirror), encoding="utf-8")
        (root / "docs" / "en" / "00-governance" / "src.md").write_text(
            doc(mirror + '  bilingual_counterpart:\n    source: "00-governance/src.md"\n'),
            encoding="utf-8",
        )
        expect_gate(
            "T17 mirror whose source lists nothing is an error", root, 1
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "docs" / "en" / "00-governance").mkdir(parents=True)
        # The source exists but carries no metadata, so it cannot be a group
        # member. The mirror must not be silently accepted.
        (root / "00-governance" / "src.md").write_text("# no metadata\n", encoding="utf-8")
        (root / "docs" / "en" / "00-governance" / "src.md").write_text(
            doc(mirror + '  bilingual_counterpart:\n    source: "00-governance/src.md"\n'),
            encoding="utf-8",
        )
        expect_gate(
            "T18 mirror naming an unclassified source is an error", root, 1
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "docs" / "en" / "00-governance").mkdir(parents=True)
        # A mirror that declares nothing is in no group at all: no source can
        # list it, so the closure check above would never look at it.
        (root / "docs" / "en" / "00-governance" / "orphan.md").write_text(
            doc(mirror), encoding="utf-8"
        )
        expect_gate("T20 mirror with no declared source is an error", root, 1)

def run_schema_agreement() -> None:
    """T19: the published schema and the gate must accept the same shape.

    The schema file is machine-readable content, parsed with the gate's own
    parser and compared field by field. Both directions matter: a field the
    schema declares but the gate rejects is a documentation lie, and a field or
    enum value the gate accepts but the schema omits is an undocumented state.
    Substring matching would let a value mentioned only in a comment count as
    documented, which is what the previous version of this test did.
    """
    print("schema/gate agreement")
    import check_document_management as gate

    path = Path(__file__).resolve().parents[1] / gate.SCHEMA_FILE
    record("T19 schema file exists", path.is_file())
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    try:
        schema = parse_yaml_subset(text)
    except ParseError as exc:
        record("T19 schema parses under the gate's own subset", False, f"  {exc}")
        return
    record("T19 schema parses under the gate's own subset", isinstance(schema, dict))

    fields = schema.get("fields")
    record("T19 schema declares a fields mapping", isinstance(fields, dict))
    if not isinstance(fields, dict):
        return

    gate_shape = {
        "": gate.TOP_KEYS,
        "lifecycle": gate.LIFECYCLE_KEYS,
        "lifecycle.approval": gate.APPROVAL_KEYS,
        "lifecycle.approval.approved_version": gate.VERSION_KEYS,
        "lifecycle.approval.approval_scope": gate.SCOPE_KEYS,
        "lifecycle.approval.revocation": gate.REVOCATION_KEYS,
        "lifecycle.evidence_verification": gate.EVIDENCE_KEYS,
        "lifecycle.supersession": gate.SUPERSESSION_KEYS,
        "lifecycle.archival": gate.ARCHIVAL_KEYS,
        "authority": gate.AUTHORITY_KEYS,
        "authority.canonical_conflict_resolution": gate.RESOLUTION_KEYS,
        "bilingual_counterpart": gate.BILINGUAL_KEYS,
    }
    # `pattern` is deliberately absent: the gate never evaluates it, so allowing
    # it would let the schema publish a constraint nothing enforces. That is the
    # exact failure this test exists to catch, so the vocabulary is the set of
    # keys the gate actually reads.
    constraint_keys = {"kind", "required", "enum", "items", "when", "fields"}
    # The closed set of value kinds. Without this, `kind: completely-unknown-kind`
    # would pass a check that only asks whether `kind` is present.
    KINDS = {"string", "nullable-string", "mapping", "nullable-mapping", "sequence", "boolean"}

    declared: set[str] = set()
    problems: list[str] = []

    def walk(node, prefix: str) -> None:
        if not isinstance(node, dict):
            problems.append(f"{prefix or '<root>'} is not a mapping")
            return
        for key, value in node.items():
            full = f"{prefix}.{key}" if prefix else key
            declared.add(full)
            allowed = gate_shape.get(prefix)
            if allowed is None:
                problems.append(f"{full}: parent {prefix!r} is not a gate node")
            elif key not in allowed:
                problems.append(f"{full}: key not accepted by the gate")
            if not isinstance(value, dict):
                problems.append(f"{full}: constraint is not a mapping")
                continue
            unknown = set(value) - constraint_keys
            if unknown:
                problems.append(f"{full}: unknown constraint keys {sorted(unknown)}")
            if "kind" not in value:
                problems.append(f"{full}: no kind declared")
            elif value["kind"] not in KINDS:
                problems.append(f"{full}: kind {value['kind']!r} is not one of {sorted(KINDS)}")
            if value.get("kind") == "sequence":
                if "items" not in value:
                    problems.append(f"{full}: sequence without items")
                elif value["items"] not in KINDS:
                    problems.append(f"{full}: items {value['items']!r} is not a kind")
            if "required" in value and not isinstance(value["required"], bool):
                problems.append(f"{full}: required is not a boolean")
            if "enum" in value and value.get("kind") != "string":
                problems.append(f"{full}: enum on a non-string kind")
            nested = value.get("fields")
            if nested is not None:
                walk(nested, full)

    walk(fields, "")
    record("T19 every declared field is a field the gate accepts", not problems,
           "  " + "; ".join(problems[:8]))

    missing: list[str] = []
    for prefix, keys in gate_shape.items():
        for key in keys:
            full = f"{prefix}.{key}" if prefix else key
            if full not in declared:
                missing.append(full)
    record("T19 every gate-accepted field is declared in the schema", not missing,
           "  undeclared: " + ", ".join(sorted(missing)[:12]))

    enums = {
        "domain": gate.DOMAINS,
        "role": gate.ROLES,
        "lifecycle.approval.decision_status": gate.DECISION_STATUSES,
        "lifecycle.approval.approved_version.scheme": gate.VERSION_SCHEMES,
        "lifecycle.approval.approval_scope.type": gate.SCOPE_TYPES,
        "lifecycle.approval.approval_applicability": gate.APPLICABILITY,
        "lifecycle.evidence_verification.verification_status": gate.VERIFICATION_STATUSES,
        "lifecycle.usage_status": gate.USAGE_STATUSES,
        "lifecycle.modification_status": gate.MODIFICATION_STATUSES,
        "authority.canonical_status": gate.CANONICAL_STATUSES,
        "authority.canonical_conflict_status": gate.CONFLICT_STATUSES,
        "authority.normative_status": gate.NORMATIVE_STATUSES,
    }

    def node_at(dotted: str):
        """Descend a dotted metadata path through the schema's nested `fields`."""
        node = fields
        for part in dotted.split("."):
            if not isinstance(node, dict):
                return None
            if part in node:
                node = node[part]
            elif isinstance(node.get("fields"), dict) and part in node["fields"]:
                node = node["fields"][part]
            else:
                return None
        return node

    # `when` is declarative: the gate never executes it. That makes it the one
    # key in the schema that can quietly lie -- a condition naming a rule that
    # does not exist reads like enforcement and enforces nothing, which is the
    # same failure `required: true` used to be. It must name a real rule.
    policy = (Path(__file__).resolve().parents[1]
              / "00-governance/architecture-document-management-policy.md")
    rule_ids = set()
    if policy.is_file():
        rule_ids = set(re.findall(r"^\|\s*(DM-\d+)\s*\|",
                                  policy.read_text(encoding="utf-8"), re.M))
    record("T19 policy rule table is readable", len(rule_ids) >= 10,
           f"  found {sorted(rule_ids)}")

    dangling: list[str] = []
    for name in sorted(declared):
        node = node_at(name)
        when = node.get("when") if isinstance(node, dict) else None
        if when is None:
            continue
        if not isinstance(when, str):
            dangling.append(f"{name}: when is not a string")
            continue
        head = when.split()[0] if when.split() else ""
        if head not in rule_ids:
            dangling.append(f"{name}: when names {head!r}, not a policy rule")
    record("T19 every `when` names a rule that exists in the policy", not dangling,
           "  " + "; ".join(dangling[:6]))

    for where, allowed in enums.items():
        node = node_at(where)
        if not isinstance(node, dict):
            record(f"T19 enum field declared: {where}", False)
            continue
        declared_values = node.get("enum")
        if not isinstance(declared_values, list):
            record(f"T19 enum field has an enum list: {where}", False,
                   f"  got {type(declared_values).__name__}")
            continue
        got = {str(v) for v in declared_values}
        record(f"T19 {where} enum matches the gate exactly", got == set(allowed),
               f"  schema {sorted(got)} vs gate {sorted(allowed)}")

    for leaf in gate.required_fields():
        node = node_at(leaf)
        record(f"T19 required leaf declared and marked required: {leaf}",
               isinstance(node, dict) and node.get("required") is True)

    # No second hand-maintained list may exist: REQUIRED_FIELDS used to be one,
    # and it omitted approval_scope while the schema declared it required.
    record("T19 required leaves come from the schema, not a second list",
           not hasattr(gate, "REQUIRED_FIELDS"),
           "  gate still exposes a hard-coded REQUIRED_FIELDS")

    declared_required = {
        name for name in declared
        if isinstance(node_at(name), dict) and node_at(name).get("required") is True
    }
    record("T19 every required declaration is a leaf the gate checks",
           declared_required == set(gate.required_fields()),
           f"  schema-only {sorted(declared_required - set(gate.required_fields()))}, "
           f"gate-only {sorted(set(gate.required_fields()) - declared_required)}")

    forbidden = schema.get("forbidden")
    record("T19 forbidden list names superseded_by",
           isinstance(forbidden, list)
           and "lifecycle.supersession.superseded_by" in forbidden)
    tpl = (Path(__file__).resolve().parents[1]
           / "00-governance/templates/document-metadata-template.md")
    record("T19 copy-paste template exists", tpl.is_file())
    if tpl.is_file():
        tpl_text = tpl.read_text(encoding="utf-8")
        record("T19 template carries metadata", isinstance(read_metadata(tpl_text), dict))
        template_errors, _ = check_document(tpl, tpl_text)
        record("T19 template satisfies the gate", not template_errors,
               f"  {template_errors}")

def run_scope_registry() -> None:
    """DM-14: the scan set is the declared set, and nothing is left out.

    The accounting identity proves no file was dropped inside the scan. It is
    silent about a directory the scan never entered, which is the reviewer's
    `15-new-architecture/` counterexample. These cases pin the fix.
    """
    print("DM-14 scope registry")
    governed = ENFORCED_ROOTS

    # A new top-level directory with a governed-looking document must fail:
    # this is the exact counterexample, and the old gate passed it.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "15-new-architecture").mkdir()
        (root / "15-new-architecture" / "critical-policy.md").write_text(
            doc(BASE), encoding="utf-8"
        )
        expect_gate(
            "T22 unregistered top-level directory fails even when it is empty of rules",
            root, 1,
        )

    # Excluded without a reason is not an exclusion.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "document-scope-registry.yaml").write_text(
            registry_text(governed, excluded=()) .replace(
                "  docs:", "  tools:\n    reason_zh: \"非文档\"\n\n  docs:"
            ),
            encoding="utf-8",
        )
        expect_gate("T23 exclusion without a reason is an error", root, 1)

    # Declared scope must equal enforced scope, in both directions.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "document-scope-registry.yaml").write_text(
            registry_text(governed + ["16-phantom"]), encoding="utf-8"
        )
        (root / "16-phantom").mkdir()
        expect_gate("T24 registry naming a root the gate does not scan fails", root, 1)

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "document-scope-registry.yaml").write_text(
            registry_text(governed[1:]), encoding="utf-8"
        )
        expect_gate("T25 registry omitting a scanned root fails", root, 1)

    # A directory cannot be both governed and excluded.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "document-scope-registry.yaml").write_text(
            registry_text(governed, excluded=("tools", "00-governance")),
            encoding="utf-8",
        )
        expect_gate("T26 governed and excluded at once is an error", root, 1)

    # An individually governed file must sit in an excluded directory, and
    # must exist. Otherwise the list is either dead weight or a hidden scope
    # expansion nobody declared.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        for rel in GOVERNED_FILES:
            (root / rel).unlink()
        expect_gate("T38 governed file that does not exist is an error", root, 1)

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        # Point the individual entry at a governed root instead.
        import check_document_management as gate_mod
        original = gate_mod.GOVERNED_FILES
        gate_mod.GOVERNED_FILES = ("00-governance/extra.md",)
        (root / "00-governance" / "extra.md").write_text(doc(BASE), encoding="utf-8")
        try:
            expect_gate(
                "T39 governed file inside an already-governed root is an error",
                root, 1,
            )
        finally:
            gate_mod.GOVERNED_FILES = original

    # The registry's governed_files must equal the gate's, or one of them is a
    # claim the other does not honour.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "document-scope-registry.yaml").write_text(
            registry_text(governed, files=()), encoding="utf-8"
        )
        expect_gate("T40 registry omitting a governed file is an error", root, 1)

def run_kind_contract() -> None:
    """P0-01: the schema's declared kind must be enforced, not merely published.

    Each case below was a reviewer counterexample: the document parsed, no rule
    fired, and the gate reported success while the value's type contradicted
    the schema.
    """
    print("schema kind enforcement")
    import check_document_management as gate

    # null where `mapping` is declared
    null_mapping = doc(
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "      approval_scope: null\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    canonical_conflict_status: None\n"
        "    normative_status: Informative\n"
    )
    errs, _ = check_document(FILE, null_mapping)
    record(
        "T27 null where the schema declares mapping is a type error",
        any("approval_scope must be mapping" in e for e in errs),
        f"  got {errs}",
    )

    # bool inside a sequence of strings
    bool_in_seq = doc(
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "      evidence_reference:\n"
        "        - true\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    canonical_conflict_status: None\n"
        "    normative_status: Informative\n"
    )
    errs, _ = check_document(FILE, bool_in_seq)
    record(
        "T28 non-string element in a sequence of strings is a type error",
        any("evidence_reference[0] must be string" in e for e in errs),
        f"  got {errs}",
    )

    # null where `string` is declared, on an optional block
    null_string = doc(
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "      revocation:\n"
        "        revocation_decision_id: null\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    canonical_conflict_status: None\n"
        "    normative_status: Informative\n"
    )
    errs, _ = check_document(FILE, null_string)
    record(
        "T29 null where the schema declares string is a type error",
        any("revocation_decision_id must be string" in e for e in errs),
        f"  got {errs}",
    )

    # The nullable variants must still accept null: closing the hole must not
    # break the documents that legitimately omit an approval version.
    nullable_ok = doc(
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "      approved_version: null\n"
        "      revocation: null\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    canonical_conflict_status: None\n"
        "    normative_status: Informative\n"
    )
    errs, _ = check_document(FILE, nullable_ok)
    record(
        "T30 nullable kinds still accept null",
        not errs,
        f"  got {errs}",
    )

    # A broken schema must stop the gate, not silently disable type checks.
    record(
        "T31 schema is loaded from the published file",
        gate.schema().get("fields", {}).get("domain", {}).get("kind") == "string",
    )

# --------------------------------------------------------------------------
# Golden corpus: hand-written inputs with hand-written expected verdicts.
#
# This is the independent oracle T19 cannot be. T19 compares the schema against
# the gate's own constants, so if both are wrong in the same way it passes.
# Here the expectation is written by hand from the policy text, before looking
# at the implementation, and is deliberately not derived from any gate
# constant. If the gate and this table disagree, one of them is wrong and a
# human has to decide which -- that is the point.
#
# Each entry: (label, metadata body, should_pass, expected error fragment)
# `expected` is empty when should_pass is True.
# --------------------------------------------------------------------------
GOLDEN = [
    (
        "minimal Draft document is valid",
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    normative_status: Informative\n"
        "    canonical_conflict_status: None\n",
        True,
        "",
    ),
    (
        "unknown domain is rejected",
        "  domain: made-up-domain\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    normative_status: Informative\n"
        "    canonical_conflict_status: None\n",
        False,
        "not in enumeration",
    ),
    (
        "Approved without a version is rejected",
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Approved\n"
        "    evidence_verification:\n"
        "      verification_status: Verified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    normative_status: Informative\n"
        "    canonical_conflict_status: None\n",
        False,
        "approved_version",
    ),
    (
        "Revoked without a revocation block is rejected",
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Revoked\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    normative_status: Informative\n"
        "    canonical_conflict_status: None\n",
        False,
        "revocation",
    ),
    (
        "Archived without a date is rejected",
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Archived\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    normative_status: Informative\n"
        "    canonical_conflict_status: None\n",
        False,
        "archived_date",
    ),
    (
        "Canonical without a scope id is rejected",
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Canonical\n"
        "    normative_status: Normative\n"
        "    canonical_conflict_status: None\n",
        False,
        "canonical_scope_id",
    ),
    (
        "Canonical while under conflict is rejected",
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Canonical\n"
        "    canonical_scope: \"Architecture: x\"\n"
        "    canonical_scope_id: \"architecture/x\"\n"
        "    canonical_scope_keywords:\n"
        "      - x\n"
        "    normative_status: Normative\n"
        "    canonical_conflict_status: Under-Review\n",
        False,
        "MUST NOT be Canonical",
    ),
    (
        "hand-written superseded_by is rejected",
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "    supersession:\n"
        "      superseded_by: \"00-governance/other.md\"\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    normative_status: Informative\n"
        "    canonical_conflict_status: None\n",
        False,
        "CI-derived",
    ),
    (
        "scope id whose prefix contradicts the domain is rejected",
        "  domain: protocol\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Canonical\n"
        "    canonical_scope: \"Architecture: x\"\n"
        "    canonical_scope_id: \"architecture/x\"\n"
        "    canonical_scope_keywords:\n"
        "      - x\n"
        "    normative_status: Normative\n"
        "    canonical_conflict_status: None\n",
        False,
        "must equal the declared domain",
    ),
    (
        "selected-sections scope without sections is rejected",
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Approved\n"
        "      approved_version:\n"
        "        scheme: git\n"
        "        value: \"0000000000000000000000000000000000000000\"\n"
        "      approval_scope:\n"
        "        type: Selected-sections\n"
        "      approval_applicability: Applicable-To-Current-Version\n"
        "    evidence_verification:\n"
        "      verification_status: Verified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    normative_status: Informative\n"
        "    canonical_conflict_status: None\n",
        False,
        "included_sections",
    ),
]

# DM-09 needs the body, not just the metadata: the rule is "a file carrying the
# generated marker MUST NOT be Normative or Canonical". These three cases are
# the three dispositions the policy names, and each is written from the policy
# text rather than from GENERATED_MARKER's pattern.
GENERATED_MARKER_TEXT = "<!-- GENERATED FILE - DO NOT EDIT -->\n"

GOLDEN_GENERATED = [
    (
        "generated artifact claiming Canonical is rejected",
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Canonical\n"
        "    canonical_scope: \"Architecture: x\"\n"
        "    canonical_scope_id: \"architecture/x\"\n"
        "    canonical_scope_keywords:\n"
        "      - x\n"
        "    normative_status: Informative\n"
        "    canonical_conflict_status: None\n",
        False,
        "generated artifact",
    ),
    (
        "generated artifact claiming Normative is rejected",
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    normative_status: Normative\n"
        "    canonical_conflict_status: None\n",
        False,
        "generated artifact",
    ),
    (
        "generated artifact that stays Informative is accepted",
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    normative_status: Informative\n"
        "    canonical_conflict_status: None\n",
        True,
        "",
    ),
]

def run_golden_corpus() -> None:
    """T32: hand-written expectations, independent of the gate's constants."""
    print("golden corpus")
    for label, body, should_pass, fragment in GOLDEN:
        errs, meta = check_document(FILE, doc(body))
        if meta is None:
            record(f"T32 {label}", False, "  metadata did not parse")
            continue
        if should_pass:
            record(f"T32 {label}", not errs, f"  got {errs}")
        else:
            record(
                f"T32 {label}",
                any(fragment in e for e in errs),
                f"  wanted {fragment!r}, got {errs}",
            )

    # DM-09 is about the body, so these need the marker in the file itself.
    for label, body, should_pass, fragment in GOLDEN_GENERATED:
        text = doc(body).replace("# Title\n", "# Title\n\n" + GENERATED_MARKER_TEXT, 1)
        errs, meta = check_document(FILE, text)
        if meta is None:
            record(f"T32 {label}", False, "  metadata did not parse")
            continue
        if should_pass:
            record(f"T32 {label}", not errs, f"  got {errs}")
        else:
            record(
                f"T32 {label}",
                any(fragment in e for e in errs),
                f"  wanted {fragment!r}, got {errs}",
            )

def run_schema_fail_closed() -> None:
    """P1-04: a schema that declares nothing must not read as "no rules".

    `fields: {}` parses, is a dict, and leaves check_kinds() with nothing to
    check. Every type and required rule would pass silently. These cases pin
    the runtime guard, not just the self-check.
    """
    print("schema fail-closed")
    import check_document_management as gate

    real = Path(__file__).resolve().parents[1] / gate.SCHEMA_FILE

    def with_schema(body: str) -> tuple[int, str]:
        """Run the gate against a temp repo whose schema file is `body`."""
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            (root / "00-governance" / gate.SCHEMA_FILE.split("/")[-1]).write_text(
                body, encoding="utf-8"
            )
            (root / "00-governance" / "a.md").write_text(doc(BASE), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(real.parent.parent / "scripts" / "check_document_management.py"),
                 "--root", str(root)],
                capture_output=True, text=True,
            )
            return proc.returncode, (proc.stdout + proc.stderr)

    # Empty fields: must stop, not silently check nothing.
    code, out = with_schema('schema_version: "2"\nfields: {}\n')
    record("T33 empty fields stops the gate",
           code != 0 and "no fields mapping" in out or "no longer declares" in out,
           f"  exit {code}: {out.strip()[:160]}")

    # Fields without the four dimensions: also must stop.
    code, out = with_schema(
        'schema_version: "2"\nfields:\n  domain:\n    kind: string\n'
    )
    record("T34 schema missing the four dimensions stops the gate",
           code != 0 and ("no longer declares" in out or "fewer than" in out),
           f"  exit {code}: {out.strip()[:160]}")

    # A required leaf absent from the document must be reported, by path.
    missing = doc(
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    normative_status: Informative\n"
        "    canonical_conflict_status: None\n"
    )
    # `approval_scope` is not required for Draft (DM-03 covers Approved), so
    # drop a leaf that is: `authority.normative_status`.
    missing = missing.replace("    normative_status: Informative\n", "")
    errs, _ = check_document(FILE, missing)
    record("T35 absent required leaf is an error naming its path",
           any("missing required field" in e and "normative_status" in e for e in errs),
           f"  got {errs}")

def run_symlink_boundary() -> None:
    """P1-02: a directory symlink must not silently extend the governed set.

    DM-14 asks every top-level directory to be declared. `Path.is_dir()`
    follows symlinks, so an `external-docs -> /outside` link looks like a
    directory the registry must name. The gate must refuse to treat a symlink
    as a governed root, because scanning through it would read files that are
    not in this repository.
    """
    print("symlink boundary")
    import check_document_management as gate

    with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside:
        root = _repo(tmp)
        victim = Path(outside) / "leaked.md"
        victim.write_text(doc(BASE), encoding="utf-8")
        link = root / "15-linked"
        try:
            link.symlink_to(Path(outside), target_is_directory=True)
        except (OSError, NotImplementedError):
            record("T36 directory symlink is rejected as a governed root", True,
                   "  (symlinks unavailable on this platform; skipped)")
            return

        (root / "00-governance" / "document-scope-registry.yaml").write_text(
            registry_text(ENFORCED_ROOTS + ["15-linked"]), encoding="utf-8"
        )
        errors = gate.check_scope_registry(root)
        record(
            "T36 directory symlink is rejected as a governed root",
            any("symbolic link" in e or "symlink" in e for e in errors),
            f"  got {errors}",
        )

        # And it must not be scanned even if someone names it.
        scanned = {p.name for p in gate.governed_files(root)}
        record("T37 governed_files does not descend into a symlinked root",
               "leaked.md" not in scanned,
               f"  scanned {sorted(scanned)}")

def main() -> int:
    print("check_document_management self-check")
    run_parser()
    run_fields()
    run_resolver()
    run_repository_rules()
    run_approval_binding()
    run_changed_paths()
    run_path_safety()
    run_body_hash_equivalence()
    run_bilingual_closure()
    run_scope_registry()
    run_kind_contract()
    run_golden_corpus()
    run_schema_fail_closed()
    run_symlink_boundary()
    run_schema_agreement()
    passed, total = sum(RESULTS), len(RESULTS)
    print(f"{passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
