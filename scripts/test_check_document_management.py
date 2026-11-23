#!/usr/bin/env python3
"""Self-check for scripts/check_document_management.py.

Negative cases matter more than positive ones here: the parser is the trust
root, so every input outside the declared subset must fail, not degrade.

    python3 scripts/test_check_document_management.py
"""

from __future__ import annotations

import ast
import os
import re
import shutil
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
RESULTS_BY_NAME: dict[str, bool] = {}
SKIPPED: list[str] = []
UNEXPECTED_SKIPS: list[str] = []

# The only cases allowed to skip, and only for the stated reason. A skip is a
# coverage hole; an unbounded skip API is a way to convert "the test cannot run
# here" into "the suite is green". Both matter, so this list is the boundary:
# an unregistered skip fails the run, and `main()` refuses to return success
# when nothing executed.
ALLOWED_SKIPS = {
    "T68c a real 0o000 directory is reported by path (integration)":
        "running as root: mode bits cannot deny access",
}


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
    # Execution is recorded here, at the only place a result exists. AST can
    # prove a `record()` call is *written*; only this can prove it *ran*. A call
    # inside `if False:` is present in the tree and absent here.
    RESULTS_BY_NAME[name] = ok


def skip(name: str, why: str) -> None:
    """A case that could not run. Not a pass, and not a failure.

    Recording a skipped case as `True` inflates the pass count with a test that
    proved nothing: running as root, for instance, means mode bits cannot deny
    access, so a permission case silently became "ok" without executing.

    A skip is also bounded. `ALLOWED_SKIPS` names the cases permitted to skip
    and why; anything else is recorded as an unexpected skip, which `main()`
    turns into a failure. Without that, `skip()` is an escape hatch any future
    test can use to keep the suite green while checking nothing.
    """
    print(f"  [skip] {name}  ({why})")
    SKIPPED.append(name)
    if name not in ALLOWED_SKIPS:
        UNEXPECTED_SKIPS.append(f"{name} ({why})")
    elif why.strip() != ALLOWED_SKIPS[name]:
        UNEXPECTED_SKIPS.append(f"{name}: skip reason {why!r} is not the registered one")


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

    scope_id = "architecture/data-model-design"

    def fresh() -> dict:
        return read_metadata(doc(CANONICAL))

    def resolved_meta(selected: str = "a.md") -> dict:
        meta = fresh()
        authority = meta["authority"]
        authority["canonical_conflict_status"] = "Resolved"
        authority["canonical_conflict_resolution"] = {
            "resolution_decision_id": "GOV-CONF-2026-002",
            "resolved_date": "2026-05-10",
            "selected_document": selected,
            # Empty on purpose: this is the policy's own section 5.1 example.
            "resolution_evidence": [],
        }
        return meta

    # 1. No conflict record: the unique Canonical resolves.
    one = {"a.md": fresh()}
    record(
        "unique Canonical without conflict resolves",
        resolve_canonical(one, scope_id) == "a.md",
    )

    # 2. Resolved record selecting the unique Canonical: resolves.
    record(
        "Resolved conflict selecting the unique Canonical resolves",
        resolve_canonical(
            {"a.md": resolved_meta()},
            scope_id,
        ) == "a.md",
    )

    # 3. A selected document outside this scope must fail closed.
    record(
        "Resolved selection outside scope resolves to nothing",
        resolve_canonical(
            {"a.md": resolved_meta("outside.md")},
            scope_id,
        ) == NO_AUTHORITATIVE_SOURCE,
    )

    # 4. A selected member that is not Canonical must fail closed.
    noncanonical = resolved_meta()
    noncanonical["authority"]["canonical_status"] = "Candidate"
    record(
        "Resolved selection of a non-Canonical member resolves to nothing",
        resolve_canonical(
            {"a.md": noncanonical},
            scope_id,
        ) == NO_AUTHORITATIVE_SOURCE,
    )

    # 5. Resolved without the resolution block must fail closed.
    missing_block = fresh()
    missing_block["authority"]["canonical_conflict_status"] = "Resolved"
    missing_block["authority"].pop("canonical_conflict_resolution", None)
    record(
        "Resolved without a resolution block resolves to nothing",
        resolve_canonical(
            {"a.md": missing_block},
            scope_id,
        ) == NO_AUTHORITATIVE_SOURCE,
    )

    # 6. Under-Review remains unresolved.
    under_review = fresh()
    under_review["authority"]["canonical_conflict_status"] = "Under-Review"
    record(
        "Under-Review resolves to nothing",
        resolve_canonical(
            {"a.md": under_review},
            scope_id,
        ) == NO_AUTHORITATIVE_SOURCE,
    )

    # 7. Unknown states fail closed. This is a pure resolver test;
    # it intentionally bypasses DM-01 frontmatter enum validation.
    unknown = fresh()
    unknown["authority"]["canonical_conflict_status"] = "Disputed"
    record(
        "unknown conflict state resolves to nothing",
        resolve_canonical(
            {"a.md": unknown},
            scope_id,
        ) == NO_AUTHORITATIVE_SOURCE,
    )

    # 8. No Canonical member must fail closed.
    no_canonical = fresh()
    no_canonical["authority"]["canonical_status"] = "Candidate"
    record(
        "zero Canonical documents resolve to nothing",
        resolve_canonical(
            {"a.md": no_canonical},
            scope_id,
        ) == NO_AUTHORITATIVE_SOURCE,
    )

    # 9. Multiple Canonical members must fail closed.
    second_canonical = fresh()
    record(
        "multiple Canonical documents resolve to nothing",
        resolve_canonical(
            {"a.md": fresh(), "b.md": second_canonical},
            scope_id,
        ) == NO_AUTHORITATIVE_SOURCE,
    )

    # 10. The policy's own section 5.1 example: a Resolved record carrying
    # `resolution_evidence: []` and selecting the sole Canonical must resolve.
    # Record completeness is DM-11's rule; the resolver only resolves authority.
    record(
        "Resolved with empty evidence selecting the sole Canonical resolves",
        resolve_canonical(
            {"a.md": resolved_meta()},
            scope_id,
        ) == "a.md",
    )

    # 11. A Resolved record cannot make a second Canonical legitimate.
    record(
        "two Canonical members with a Resolved record resolve to nothing",
        resolve_canonical(
            {"a.md": resolved_meta(), "b.md": fresh()},
            scope_id,
        ) == NO_AUTHORITATIVE_SOURCE,
    )

    # 12. A resolution block that is not a mapping must fail closed.
    not_a_mapping = fresh()
    not_a_mapping["authority"]["canonical_conflict_status"] = "Resolved"
    not_a_mapping["authority"]["canonical_conflict_resolution"] = (
        "GOV-CONF-2026-002"
    )
    record(
        "Resolved with a non-mapping resolution block resolves to nothing",
        resolve_canonical(
            {"a.md": not_a_mapping},
            scope_id,
        ) == NO_AUTHORITATIVE_SOURCE,
    )

    # 13. A resolution naming no document must fail closed.
    missing_selected = resolved_meta()
    missing_selected["authority"]["canonical_conflict_resolution"].pop(
        "selected_document"
    )
    record(
        "Resolved without selected_document resolves to nothing",
        resolve_canonical(
            {"a.md": missing_selected},
            scope_id,
        ) == NO_AUTHORITATIVE_SOURCE,
    )

    # 14. The original unknown-scope guard remains covered.
    record(
        "unknown scope resolves to nothing",
        resolve_canonical(one, "architecture/unknown-scope")
        == NO_AUTHORITATIVE_SOURCE,
    )

# --------------------------------------------------------------------------
# 4. Repository-wide rules
# --------------------------------------------------------------------------

def registry_text(governed, excluded=("tools",), files=None, backlog=None) -> str:
    """A scope registry matching the gate's own enforced roots.

    Built from NORMATIVE_ROOTS rather than hard-coded, so the fixture stays
    valid when the real roots change; the tests that matter pass an explicit
    governed list instead.
    """
    if files is None:
        files = GOVERNED_FILES
    if backlog is None:
        backlog = {"docs": 1}
    lines = ['registry_version: "2"', "", "governed:"]
    lines += [f"  - {name}" for name in governed]
    lines += ["", "governed_files:"]
    lines += [f"  - {rel}" for rel in files]
    lines += ["", "backlog:", ""]
    for name, count in backlog.items():
        lines.append(f"  {name}:")
        lines.append(f"    documents: {count}")
        lines.append('    reason: "architecture documents not yet classified"')
        lines.append('    reason_zh: "尚未分类的架构文档"')
        lines.append("")
    lines.append("excluded:")
    lines.append("")
    for name in excluded:
        lines.append(f"  {name}:")
        lines.append("    kind: not-documentation")
        lines.append('    reason: "not documentation"')
        lines.append('    reason_zh: "非文档"')
        lines.append("")
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
    # A backlog root must contain the documents the registry claims. DM-14
    # compares the declared count to the disk, so an empty backlog directory
    # would fail the fixture before the test it belongs to ran.
    (root / "docs" / "research").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "research" / "backlog.md").write_text(doc(BASE), encoding="utf-8")
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
            len(governed_files(root)) == 3 + len(GOVERNED_FILES),
            f"  governed {len(governed_files(root))}, "
            f"expected {3 + len(GOVERNED_FILES)} (2 written + 1 backlog + "
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

    # S1-03: deleting metadata from an already-classified file. The increment
    # only requires metadata on changed files, so the question is whether a
    # removal counts as a change. It must: otherwise the cheapest way to escape
    # the gate would be to delete the block that proves you complied.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        victim = root / "00-governance" / "was-classified.md"
        victim.write_text(doc(BASE), encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed")
        base = _git(root, "rev-parse", "HEAD")
        victim.write_text("# metadata deleted\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "strip metadata")
        expect_gate(
            "T48 removing metadata from a classified file fails the increment",
            root, 1, "--require-changed", base,
        )

    # Empty increments are not successful verification. Use a complete Git
    # fixture with no unrelated DM-10 failures so the assertion tests only the
    # changed-set behavior.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed")
        head = _git(root, "rev-parse", "HEAD")
        expect_gate(
            "T72 same-HEAD increment is NOT_APPLICABLE (exit 3), never PASS",
            root, 3, "--require-changed", head,
        )

    # A pathspec is not a commit ref. It must be rejected before diffing;
    # otherwise the old two-dot fallback interprets it as a path filter.
    for bad_ref, label in (("docs", "path-like ref"), ("deadbeef", "invalid ref")):
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            _git(root, "init", "-q")
            _git(root, "config", "user.email", "gate@example.invalid")
            _git(root, "config", "user.name", "gate")
            _git(root, "add", "-A")
            _git(root, "commit", "-q", "-m", "seed")
            expect_gate(
                f"T73 {label} is rejected before diff (ERROR, exit 1)",
                root, 1, "--require-changed", bad_ref,
            )

    # A real non-empty code-only change remains a valid incremental run. The
    # gate must distinguish it from an empty diff rather than rejecting every
    # change set that contains no governed Markdown.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed")
        base = _git(root, "rev-parse", "HEAD")
        (root / "tools" / "only.rs").write_text("// code-only change\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "code only")
        expect_gate(
            "T74 non-empty code-only increment remains applicable",
            root, 0, "--require-changed", base,
        )

    # A deletion-only increment is a real increment. The diff is non-empty, the
    # verification ran, and no surviving path needed classifying -- so it
    # passes. It must NOT be reported as NOT_APPLICABLE: that verdict means "no
    # diff to inspect", and reusing it here failed CI on every PR that only
    # removed files, forever. This is the regression that made the distinction
    # necessary; keep it pinned.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed")
        scratch = root / "tools" / "scratch-output.txt"
        scratch.write_text("captured tool output\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "add scratch file")
        # Base is taken AFTER the file exists, so base...HEAD is purely the
        # deletion. Basing before the addition would make add+delete cancel to
        # an empty diff and test the same-HEAD case instead of this one.
        base = _git(root, "rev-parse", "HEAD")
        scratch.unlink()
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "drop scratch file")
        expect_gate(
            "T75 deletion-only increment is verified, not NOT_APPLICABLE",
            root, 0, "--require-changed", base,
        )

    # Deleting a governed, classified document. Recorded decision, not an
    # accident: a deleted path is not in `requirable`, so this gate does not
    # require metadata on it and does not block the removal. That is a KNOWN
    # HOLE -- removing a governed document escapes classification review via
    # this gate -- and it is deliberately NOT changed here. Pinned so that
    # changing it later is a visible decision rather than a silent drift.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        victim = root / "00-governance" / "classified-then-removed.md"
        victim.write_text(doc(BASE), encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed")
        base = _git(root, "rev-parse", "HEAD")
        victim.unlink()
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "remove governed document")
        expect_gate(
            "T76 deleting a governed classified document is not blocked by this gate",
            root, 0, "--require-changed", base,
        )

    # T77: a deletion combined with a Markdown modification is not
    # deletion-only; it remains an ordinary applicable increment.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        victim = root / "_dm.txt"
        victim.write_text("temporary gate output\n", encoding="utf-8")
        readme = root / "README.md"
        readme.write_text("# Original README\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed")
        base = _git(root, "rev-parse", "HEAD")
        victim.unlink()
        readme.write_text("# Updated README\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "delete output and modify README")
        expect_gate(
            "T77 deletion plus Markdown modification remains applicable",
            root, 0, "--require-changed", base,
        )

    # T78: a deletion combined with a code-only modification is not
    # deletion-only; the existing code-only incremental behavior is preserved.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        victim = root / "_dm.txt"
        victim.write_text("temporary gate output\n", encoding="utf-8")
        code = root / "tools" / "only.rs"
        code.parent.mkdir(parents=True, exist_ok=True)
        code.write_text("// original\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed")
        base = _git(root, "rev-parse", "HEAD")
        victim.unlink()
        code.write_text("// modified\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "delete output and modify code")
        expect_gate(
            "T78 deletion plus code-only modification remains applicable",
            root, 0, "--require-changed", base,
        )

    # T80: a deletion must not let a newly added unclassified governed
    # document escape validation in the same increment.
    with tempfile.TemporaryDirectory() as tmp:
        import contextlib
        import io

        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")

        scratch = root / "tools" / "scratch-output.txt"
        scratch.write_text("captured tool output\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed deletion target")
        base = _git(root, "rev-parse", "HEAD")

        scratch.unlink()
        unclassified = root / "00-governance" / "unclassified-new.md"
        unclassified.write_text("# no metadata\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "delete scratch and add unclassified document")

        captured_stdout = io.StringIO()
        captured_stderr = io.StringIO()
        with contextlib.redirect_stdout(captured_stdout), contextlib.redirect_stderr(captured_stderr):
            code = run_gate(root, "--require-changed", base)

        output = captured_stdout.getvalue() + captured_stderr.getvalue()
        record(
            "T80 deletion plus unclassified governed document still fails DM-01",
            code == 1 and "DM-01" in output,
            f"  gate returned {code}, expected 1; DM-01 present: {'DM-01' in output}",
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
            registry_text(governed, excluded=("tools",)).replace(
                '  tools:\n    kind: not-documentation\n    reason: "not documentation"\n',
                "  tools:\n    kind: not-documentation\n",
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
        "selected-assets scope without assets is rejected",
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Approved\n"
        "      approved_version:\n"
        "        scheme: git\n"
        "        value: \"0000000000000000000000000000000000000000\"\n"
        "      approval_scope:\n"
        "        type: Selected-assets\n"
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
        "included_assets",
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

    # R1-01: a governed FILE that is a symlink. The registry check used
    # `is_file()`, which follows links, so it passed; the scanner skipped
    # symlinks, so the file was never scanned. Declared and enforced sets
    # disagreed, and the gate reported zero governed documents.
    with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside:
        root = _repo(tmp)
        victim = Path(outside) / "gaps.md"
        victim.write_text(doc(BASE), encoding="utf-8")
        for rel in gate.GOVERNED_FILES:
            target = root / rel
            target.unlink()
            try:
                target.symlink_to(victim)
            except (OSError, NotImplementedError):
                record("T41 symlinked governed file is rejected", True,
                       "  (symlinks unavailable; skipped)")
                return
        errors = gate.check_scope_registry(root)
        record("T41 symlinked governed file is rejected",
               any("not a regular file inside the repository" in e for e in errors),
               f"  got {errors}")

    # R1-01b: the file is regular, but its PARENT is a link out of the repo.
    # `is_symlink()` on the final component cannot see this; containment is
    # proven on the resolved path instead.
    with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside:
        root = _repo(tmp)
        victim_dir = Path(outside) / "governance"
        victim_dir.mkdir()
        (victim_dir / "documentation-gaps.md").write_text(doc(BASE), encoding="utf-8")
        parent = root / "docs" / "governance"
        import shutil
        shutil.rmtree(parent)
        try:
            parent.symlink_to(victim_dir, target_is_directory=True)
        except (OSError, NotImplementedError):
            record("T42 governed file reached through a symlinked parent is rejected",
                   True, "  (symlinks unavailable; skipped)")
            return
        errors = gate.check_scope_registry(root)
        record("T42 governed file reached through a symlinked parent is rejected",
               any("not a regular file inside the repository" in e for e in errors),
               f"  got {errors}")

    # R1-02: a hidden top-level directory. Excluding dot-directories from the
    # on-disk set meant `.new-architecture/` was neither governed, excluded,
    # reported, nor scanned.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        hidden = root / ".new-architecture"
        hidden.mkdir()
        (hidden / "design.md").write_text(doc(BASE), encoding="utf-8")
        errors = gate.check_scope_registry(root)
        record("T43 hidden top-level directory must be accounted for",
               any(".new-architecture" in e for e in errors),
               f"  got {errors}")

    # `.git` is the one structural exception: present in every clone, absent in
    # every export, so requiring it in a tracked file would describe the working
    # copy rather than the repository.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / ".git").mkdir()
        errors = gate.check_scope_registry(root)
        record("T44 .git is structurally exempt from the registry",
               not any(".git" in e for e in errors),
               f"  got {errors}")

    # Backlog must be a number, not a sentence: a declared count that disagrees
    # with the disk is how "26 documents remain" quietly becomes false.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "document-scope-registry.yaml").write_text(
            registry_text(ENFORCED_ROOTS, backlog={"docs": 99}), encoding="utf-8"
        )
        errors = gate.check_scope_registry(root)
        record("T45 backlog count disagreeing with the disk is an error",
               any("declares 99 documents" in e for e in errors),
               f"  got {errors}")

    # And it must be a count, not free text.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "document-scope-registry.yaml").write_text(
            registry_text(ENFORCED_ROOTS, backlog={"docs": "many"}), encoding="utf-8"
        )
        errors = gate.check_scope_registry(root)
        record("T46 backlog count that is not an integer is an error",
               any("non-negative integer" in e for e in errors),
               f"  got {errors}")

    # A backlog directory is scanned. Otherwise declaring it would be the same
    # silent exclusion the registry exists to prevent, under a friendlier name.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        scanned = {p.name for p in gate.governed_files(root)}
        record("T47 backlog documents are actually scanned",
               "backlog.md" in scanned, f"  scanned {sorted(scanned)}")


def run_scan_boundary() -> None:
    """T49-T53: the scan and the count must be one walk with one rule.

    The tenth review found that they were two walks. A symlinked backlog root
    was skipped by the counter, so the declared count was compared to nothing,
    and skipped by the scanner too, so the run reported zero governed documents
    and exit 0. Both symptoms came from one cause: two traversals that were
    allowed to disagree. These cases pin the single-walk contract.

    Each asserts the *diagnostic*, not merely the exit code. A gate that fails
    for an unrelated reason satisfies "exit 1" while proving nothing.
    """
    print("scan boundary")
    import check_document_management as gate

    def run(root):
        proc = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parent
                                 / "check_document_management.py"),
             "--root", str(root)],
            capture_output=True, text=True,
        )
        return proc.returncode, proc.stdout + proc.stderr

    # T49: a backlog root that is itself a symlink is refused by name.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        outside = Path(tmp).parent / "outside-docs-t49"
        outside.mkdir(exist_ok=True)
        for i in range(3):
            (outside / f"f{i}.md").write_text("# x\n", encoding="utf-8")
        shutil.rmtree(root / "docs")
        (root / "docs").symlink_to(outside, target_is_directory=True)
        try:
            code, out = run(root)
            record("T49 symlinked backlog root is named in the diagnostic",
                   code != 0 and "docs is a symbolic link" in out,
                   f"  exit {code}, output {out[:200]}")
        finally:
            shutil.rmtree(outside, ignore_errors=True)

    # T50: a symlinked directory inside a backlog root is reported by path.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        outside = Path(tmp).parent / "outside-sub-t50"
        outside.mkdir(exist_ok=True)
        (outside / "external.md").write_text("# ext\n", encoding="utf-8")
        (root / "docs" / "linked").symlink_to(outside, target_is_directory=True)
        try:
            code, out = run(root)
            record("T50 symlinked directory inside a backlog root is reported",
                   code != 0 and "docs/linked is a symbolic link" in out,
                   f"  exit {code}, output {out[:200]}")
        finally:
            shutil.rmtree(outside, ignore_errors=True)

    # T51: a symlinked .md inside a backlog root is reported by path.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        outside = Path(tmp).parent / "outside-file-t51.md"
        outside.write_text("# ext\n", encoding="utf-8")
        (root / "docs" / "linked.md").symlink_to(outside)
        try:
            code, out = run(root)
            record("T51 symlinked markdown file inside a backlog root is reported",
                   code != 0 and "docs/linked.md is a symbolic link" in out,
                   f"  exit {code}, output {out[:200]}")
        finally:
            outside.unlink(missing_ok=True)

    # T52: the counter and the scanner see the same files.
    #
    # This is the property the two-walk version violated, stated as an equality
    # so a future split fails here rather than in production.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        for i in range(4):
            (root / "docs" / f"extra{i}.md").write_text("# x\n", encoding="utf-8")
        counts, problems = gate.backlog_counts(root)
        skip = gate.governed_prefixes()
        scanned, _ = gate.scan_root(root, "docs", skip)
        record("T52 backlog count equals the number of files the scan returns",
               counts.get("docs") == len(scanned) and not problems,
               f"  count {counts.get('docs')} vs scanned {len(scanned)}, "
               f"problems {problems}")

    # T53: a stale count is an error, not a sentence.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        reg = root / "00-governance" / "document-scope-registry.yaml"
        text = reg.read_text(encoding="utf-8")
        reg.write_text(text.replace("    documents: 1", "    documents: 9"), encoding="utf-8")
        code, out = run(root)
        record("T53 a declared backlog count that disagrees with disk fails",
               code != 0 and "declares 9 documents" in out,
               f"  exit {code}, output {out[:200]}")


def run_declared_but_unread() -> None:
    """T54-T56: every published key must be read by something.

    The reviewer asked twice what else is published and not executed. These
    three were found by asking that question of the schema itself.
    """
    print("declared-but-unread keys")
    import check_document_management as gate

    real = Path(__file__).resolve().parents[1] / gate.SCHEMA_FILE
    src = real.read_text(encoding="utf-8")

    # T54: schema_version is compared, not decorative.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "00-governance").mkdir()
        (root / gate.SCHEMA_FILE).write_text(
            src.replace('schema_version: "2"', 'schema_version: "3"'), encoding="utf-8"
        )
        try:
            gate.schema(root)
            record("T54 schema_version mismatch stops the run", False, "  no error raised")
        except SystemExit as exc:
            record("T54 schema_version mismatch stops the run",
                   "schema_version" in str(exc), f"  {exc}")

    # T55: DM-08 is driven by the schema's forbidden list, not a hard-coded key.
    body = (
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "    supersession:\n"
        "      superseded_by: 00-governance/x.md\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    normative_status: Informative\n"
        "    canonical_conflict_status: None\n"
    )
    errs, _ = check_document(FILE, doc(body))
    record("T55 forbidden path from the schema is rejected by DM-08",
           any("DM-08" in e and "superseded_by" in e for e in errs),
           f"  got {errs}")

    # T56: a `when` condition is refused outright. It cannot be evaluated, so
    # publishing it in the contract is a claim with no checker behind it.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "00-governance").mkdir()
        injected = src.replace(
            "          approval_scope:\n            kind: mapping\n",
            "          approval_scope:\n            kind: mapping\n"
            "            when: DM-03 decision_status == Draft\n",
            1,
        )
        record("T56 fixture actually injects a when key", "when: DM-03" in injected)
        (root / gate.SCHEMA_FILE).write_text(injected, encoding="utf-8")
        try:
            gate.schema(root)
            record("T56 an unevaluable `when` key is refused at load", False,
                   "  schema loaded")
        except SystemExit as exc:
            record("T56 an unevaluable `when` key is refused at load",
                   "when" in str(exc), f"  {exc}")



def run_unified_scan() -> None:
    """T57-T61: one governed set, no duplicates, no dropped diagnostics.

    The eleventh review found that fixing "two walks with two skip rules" was
    not the same as "one governed set". Three sources still fed the list at the
    call site, the problems from the normative-root walk were discarded, and
    nothing enforced uniqueness. `collect_governed()` is now the single entry
    point and these cases pin its three properties.
    """
    print("unified governed set")
    import check_document_management as gate

    def run(root):
        proc = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parent
                                 / "check_document_management.py"),
             "--root", str(root)],
            capture_output=True, text=True,
        )
        return proc.returncode, proc.stdout + proc.stderr

    # T57: no file appears twice, however it is reached.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        original = gate.GOVERNED_FILES
        # A governed file that a governed root already covers: the naive
        # concatenation would list it twice and inflate every count derived
        # from the list.
        (root / "00-governance" / "dupe.md").write_text(doc(BASE), encoding="utf-8")
        gate.GOVERNED_FILES = original + ("00-governance/dupe.md",)
        try:
            files, _ = gate.collect_governed(root)
            names = [p.as_posix() for p in files]
            record("T57 governed set contains each file exactly once",
                   len(names) == len(set(names)),
                   f"  {len(names)} entries, {len(set(names))} unique")
        finally:
            gate.GOVERNED_FILES = original

    # T58: a symlinked subdirectory inside a *normative* root is reported.
    #
    # This is R11-05. Only backlog problems reached DM-14, because
    # governed_files() discarded what scan_root() returned for normative roots.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        outside = Path(tmp).parent / "outside-norm-t58"
        outside.mkdir(exist_ok=True)
        (outside / "leak.md").write_text("# leak\n", encoding="utf-8")
        (root / "00-governance" / "linked").symlink_to(outside, target_is_directory=True)
        try:
            code, out = run(root)
            record("T58 symlinked subdirectory in a normative root is reported",
                   code != 0 and "00-governance/linked is a symbolic link" in out,
                   f"  exit {code}, output {out[:200]}")
        finally:
            shutil.rmtree(outside, ignore_errors=True)

    # T59: a top-level symlink to a directory is not an accounted directory.
    #
    # R11-02. is_dir() follows links, so a link satisfied both "on disk" and
    # "declared" -- making a registry entry true that pointed outside the repo.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        outside = Path(tmp).parent / "outside-top-t59"
        outside.mkdir(exist_ok=True)
        (root / "ghost").symlink_to(outside, target_is_directory=True)
        try:
            code, out = run(root)
            record("T59 top-level symlink is reported and does not satisfy the registry",
                   code != 0 and "symbolic links at the repository root" in out,
                   f"  exit {code}, output {out[:200]}")
        finally:
            shutil.rmtree(outside, ignore_errors=True)

    # T60: a declared directory that is only a symlink counts as missing.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        outside = Path(tmp).parent / "outside-decl-t60"
        outside.mkdir(exist_ok=True)
        # `tools` is declared as excluded by the fixture registry.
        shutil.rmtree(root / "tools")
        (root / "tools").symlink_to(outside, target_is_directory=True)
        try:
            code, out = run(root)
            record("T60 declared directory that is only a symlink is reported",
                   code != 0 and ("do not exist" in out or "symbolic links" in out),
                   f"  exit {code}, output {out[:200]}")
        finally:
            shutil.rmtree(outside, ignore_errors=True)

    # T61: DM-08 names the path it was given, not a same-named key elsewhere.
    body = (
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
        "    superseded_by: 00-governance/x.md\n"
    )
    errs, _ = check_document(FILE, doc(body))
    dm08 = [e for e in errs if "DM-08" in e]
    # The declared forbidden path is lifecycle.supersession.superseded_by, so a
    # key of the same name under `authority` is NOT a DM-08 violation. Matching
    # on the leaf name flagged it and named a location the author never wrote.
    record("T61 a same-named key elsewhere is not reported as the forbidden path",
           not dm08, f"  got {dm08}")

    # T62: the declared forbidden path is the one that fires.
    body2 = (
        "  domain: architecture\n"
        "  role: reference\n"
        "  lifecycle:\n"
        "    approval:\n"
        "      decision_status: Draft\n"
        "    supersession:\n"
        "      superseded_by: 00-governance/x.md\n"
        "    evidence_verification:\n"
        "      verification_status: Unverified\n"
        "    usage_status: Active\n"
        "    modification_status: Unchanged\n"
        "  authority:\n"
        "    canonical_status: Non-Canonical\n"
        "    normative_status: Informative\n"
        "    canonical_conflict_status: None\n"
    )
    errs2, _ = check_document(FILE, doc(body2))
    record("T62 the declared forbidden path is matched in full",
           any("lifecycle.supersession.superseded_by" in e for e in errs2 if "DM-08" in e),
           f"  got {[e for e in errs2 if 'DM-08' in e]}")


def run_schema_of_schema() -> None:
    """T63: known keys with illegal values must be refused.

    The eleventh review: rejecting unknown key *names* is not enforcement.
    `required: "false"` is a string, `is True` is False for it, and the field
    silently became optional. Every key is typed now.
    """
    print("schema-of-schema typing")
    import check_document_management as gate

    real = Path(__file__).resolve().parents[1] / gate.SCHEMA_FILE
    src = real.read_text(encoding="utf-8")
    base = "  domain:\n    kind: string\n    required: true\n"
    record("T63 fixture anchor is present", base in src)

    mutations = {
        "required is a string": "  domain:\n    kind: string\n    required: \"false\"\n",
        "items on a string kind": "  domain:\n    kind: string\n    items: string\n",
        "unknown kind": "  domain:\n    kind: strng\n",
        "enum on a boolean kind": "  domain:\n    kind: boolean\n    enum:\n      - x\n",
        "neither kind nor fields": "  domain:\n    required: true\n",
    }
    for label, replacement in mutations.items():
        mutated = src.replace(base, replacement, 1)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "00-governance").mkdir()
            (root / gate.SCHEMA_FILE).write_text(mutated, encoding="utf-8")
            try:
                gate.schema(root)
                record(f"T63 {label} is refused", False, "  schema loaded")
            except SystemExit as exc:
                record(f"T63 {label} is refused", True, f"  {str(exc)[:90]}")



def run_structural_schema() -> None:
    """T64: a node cannot claim a scalar kind and children at once.

    The twelfth review's counterexample: `kind: string` next to `fields:` was
    accepted, so one node stated two contradictory things and the gate honoured
    whichever it looked at first. `kind: mapping` + `fields:` is fine -- that is
    the same statement twice.
    """
    print("structural schema nodes")
    import check_document_management as gate

    real = Path(__file__).resolve().parents[1] / gate.SCHEMA_FILE
    src = real.read_text(encoding="utf-8")
    anchor = "  lifecycle:\n    kind: mapping\n"
    record("T64 fixture anchor is present", anchor in src)

    cases = {
        "fields with a scalar kind": src.replace(anchor, "  lifecycle:\n    kind: string\n", 1),
        "fields with a sequence kind": src.replace(anchor, "  lifecycle:\n    kind: sequence\n", 1),
    }
    for label, mutated in cases.items():
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "00-governance").mkdir()
            (root / gate.SCHEMA_FILE).write_text(mutated, encoding="utf-8")
            try:
                gate.schema(root)
                record(f"T64 {label} is refused", False, "  schema loaded")
            except SystemExit as exc:
                record(f"T64 {label} is refused", "mapping" in str(exc),
                       f"  {str(exc)[:90]}")

    # And the honest form still loads: the rule must not forbid the real schema.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "00-governance").mkdir()
        (root / gate.SCHEMA_FILE).write_text(src, encoding="utf-8")
        try:
            gate.schema(root)
            record("T64 kind: mapping with fields still loads", True)
        except SystemExit as exc:
            record("T64 kind: mapping with fields still loads", False, f"  {exc}")


def run_registry_version() -> None:
    """T65: registry_version is executed, not published.

    A version field nothing compares is decoration. If the registry is written
    for another generation, its backlog/excluded semantics may differ, and
    reading it as current would be a silent misreading.
    """
    print("registry version")
    import check_document_management as gate

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        reg = root / "00-governance" / "document-scope-registry.yaml"
        text = reg.read_text(encoding="utf-8")
        record("T65 fixture registry declares a version",
               'registry_version: "2"' in text)
        reg.write_text(text.replace('registry_version: "2"',
                                    'registry_version: "1"', 1), encoding="utf-8")
        errors = gate.check_scope_registry(root)
        record("T65 a registry version the gate does not implement is an error",
               any("registry_version" in e for e in errors),
               f"  got {errors[:3]}")


def run_bilingual_count() -> None:
    """T66: only `documents:` may state a document count.

    The twelfth review found `documents: 27` next to "26 architecture documents"
    in the English reason. The twelfth-review fix was to check that the two
    agree, which was the wrong shape: it left two numbers to keep in step and
    only noticed after they diverged. A count stated once cannot disagree with
    itself, so the gate now refuses a reason that restates one.
    """
    print("bilingual count agreement")
    import check_document_management as gate

    reg = Path(__file__).resolve().parents[1] / "00-governance" / "document-scope-registry.yaml"
    parsed = gate.parse_yaml_subset(reg.read_text(encoding="utf-8"))
    problems: list[str] = []
    for name, node in (parsed.get("backlog") or {}).items():
        if not isinstance(node, dict):
            continue
        for field in ("reason", "reason_zh"):
            said = gate.COUNT_CLAIM_RE.findall(str(node.get(field) or ""))
            if said:
                problems.append(f"{name}.{field} restates {said}")
    record("T66 the shipped registry states its backlog count exactly once",
           not problems, f"  {problems}")

    # And the rule is executed, not merely described: a reason that restates the
    # count must be refused by the gate, and the diagnostic must say which field.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        reg_path = root / "00-governance" / "document-scope-registry.yaml"
        text = reg_path.read_text(encoding="utf-8")
        # Inject a count claim into the English reason only.
        mutated = text.replace(
            '    reason: "architecture documents not yet classified"',
            '    reason: "27 architecture documents not yet classified"',
            1,
        )
        record("T66 mutation applied to the fixture reason", mutated != text)
        reg_path.write_text(mutated, encoding="utf-8")
        errors = gate.check_scope_registry(root)
        record("T66 a reason restating the backlog count is an error",
               any("restates a document count" in e for e in errors),
               f"  got {[e for e in errors if 'restates' in e]}")

    # T70 lives in run_count_vocabulary(): the vocabulary is a separate claim
    # from the registry being clean, and mixing them would let one failure hide
    # the other.


def run_count_vocabulary() -> None:
    """T70: the vocabulary the count rule covers, stated as cases.

    A regex nobody tested is a regex whose coverage is whatever its author
    imagined. Both directions matter: a phrasing that must be caught, and a
    phrasing that must not be (an unrelated number is not a count claim).

    The fifteenth review rejected an earlier version of this test that listed
    "twenty-seven documents" as a case that MUST be missed. That is not
    documenting a boundary, it is licensing a defect: a spelled-out count is
    still a second statement of the count, and "a regex cannot parse English" is
    not a reason to accept it. Spelled-out numerals are now caught, so the only
    remaining gaps are a noun outside the list and a number detached from its
    noun -- and those are listed here as *not detected*, not as *required to go
    undetected*.
    """
    print("count vocabulary")
    import check_document_management as gate

    caught = [
        "27 documents", "27 architecture documents", "27 docs", "27 files",
        "27 Markdown", "27 份", "27 个", "27 篇文档", "27 文档", "27 文件",
        "1 document", "3 doc",
        # Spelled-out numerals: still a second statement of the count.
        "twenty-seven documents", "twenty seven documents", "a hundred files",
        "二十七份文档", "三篇文档",
    ]
    not_a_claim = [
        # No document noun: not a count of documents.
        "Backlog with a known count under `documents:`.",
        "See section 9 for the rule.",
        "The gate implements version 2.",
        # A number that is not counting documents.
        "The gate has 14 rules.",
        "Two reviews rejected this.",
    ]
    bad = [s for s in caught if not gate.COUNT_CLAIM_RE.search(s)]
    record("T70 every declared phrasing is caught", not bad, f"  missed {bad}")
    noise = [s for s in not_a_claim if gate.COUNT_CLAIM_RE.search(s)]
    record("T70 prose that is not a document count is not a claim", not noise,
           f"  false positives {noise}")

    # There is deliberately no assertion that a known gap stays a gap. An
    # earlier version recorded "27 artefacts is still undetected" as a passing
    # case, which made the test a guard on the defect rather than on the
    # capability: widening the vocabulary would have failed the suite. A test
    # protects the capability it needs, not the shortfall it has. The gap is
    # named in the gate's comment and nowhere else; if the vocabulary grows,
    # only that comment needs updating.


def run_unreadable_walk() -> None:
    """T68: a directory the walk cannot read is a problem, not a shorter list.

    `os.walk` swallows errors by default: an unreadable directory is skipped and
    the walk continues. The scanned set then shrinks with no diagnostic, which
    is the tenth review's `0 governed documents, exit 0` arriving by another
    route. `scan_root()` passes `onerror`.

    Three cases, and each is named for the proposition it actually proves:
    T68a/T68b prove the callback is *wired* (they fail when the argument is
    dropped); T68c proves a real permission error is reported, which is a
    different claim and does NOT fail without `onerror` -- it is kept as an
    integration case, not offered as wiring evidence.
    """
    print("unreadable walk")
    import check_document_management as gate

    real_walk = gate.os.walk

    def fake_walk(top, followlinks=False, onerror=None):
        # Raise the same way the real walk would on an unreadable directory.
        if onerror is not None:
            onerror(OSError(13, "Permission denied", str(top)))
        return iter(())

    # T68a: wiring. Fails if `onerror=on_error` is removed.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        gate.os.walk = fake_walk
        try:
            files, problems = gate.scan_root(root, "00-governance")
        finally:
            gate.os.walk = real_walk
        record("T68a an unreadable directory is reported, not silently skipped",
               any("DM-14 cannot read" in p for p in problems),
               f"  files {len(files)}, problems {problems}")

    # T68b: wiring, one layer up. A walk that lost a subtree cannot pass.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        gate.os.walk = fake_walk
        try:
            errors = gate.check_scope_registry(root)
        finally:
            gate.os.walk = real_walk
        record("T68b the unreadable-walk problem reaches the gate verdict",
               any("cannot read" in e for e in errors),
               f"  got {[e for e in errors if 'cannot read' in e][:2]}")

    # T68b2: the diagnostic names the directory that failed, not the root it
    # started from. A message saying "cannot read 00-governance" when the real
    # failure was `00-governance/locked` sends the reader to the wrong place.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        failed = str(root / "00-governance" / "locked")

        def failing_child(top, followlinks=False, onerror=None):
            if onerror is not None:
                onerror(OSError(13, "Permission denied", failed))
            return iter(())

        gate.os.walk = failing_child
        try:
            _, problems = gate.scan_root(root, "00-governance")
        finally:
            gate.os.walk = real_walk
        record("T68b2 the diagnostic names the failing subdirectory",
               any("locked" in p for p in problems), f"  problems {problems}")

    # T68c: integration. A real permission denial is reported by path. This does
    # NOT prove the wiring -- remove `onerror` and it still passes, because
    # CPython's walk reports the failure through a different path -- so it is
    # not counted as wiring evidence. Skipped, not passed, when mode bits cannot
    # deny access (running as root).
    if hasattr(os, "geteuid") and os.geteuid() != 0:
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            locked = root / "00-governance" / "locked"
            locked.mkdir()
            (locked / "x.md").write_text("# x\n", encoding="utf-8")
            locked.chmod(0o000)
            try:
                _, problems = gate.scan_root(root, "00-governance")
            finally:
                locked.chmod(0o755)
            record("T68c a real 0o000 directory is reported by path (integration)",
                   any("cannot read" in p and "locked" in p for p in problems),
                   f"  problems {problems}")
    else:
        skip("T68c a real 0o000 directory is reported by path (integration)",
             "running as root: mode bits cannot deny access")


def run_manual_controls() -> None:
    """T69: section 9.2 is *generated* from MANUAL_CONTROLS, not kept beside it.

    An earlier version kept the list in the gate and a hand-kept table in the
    policy, then asserted the two agreed. That is two authorities plus a
    synchronisation test, which is the same shape as the duplicate backlog count
    the thirteenth review found -- and the same shape N13-01 removed. Two
    representations derived from one authority is fine; two independently
    maintained authorities is the defect.

    So the table now lives between generated-block markers and is rendered from
    `MANUAL_CONTROLS`. This case re-renders it and compares byte for byte, which
    means a hand edit inside the block fails here instead of drifting. The parse
    is scoped to section 9.2: scanning the whole policy would pick up an `M-11`
    mentioned in a change-log row and call it a missing control.
    """
    print("manual controls")
    import check_document_management as gate

    policy = (Path(__file__).resolve().parents[1] / "00-governance"
              / "architecture-document-management-policy.md").read_text(encoding="utf-8")

    # Scope: section 9.2 only, from its heading to the next `## ` heading.
    start = policy.index("### 9.2 Manual controls")
    nxt = policy.index("\n## ", start) if "\n## " in policy[start:] else len(policy)
    section = policy[start:nxt]

    begin = "<!-- BEGIN MANUAL-CONTROLS"
    end = "<!-- END MANUAL-CONTROLS -->"

    expected = "\n".join(
        f"| {cid} | {control} | {why} | {who} |"
        for cid, control, why, who in gate.MANUAL_CONTROLS
    )

    # R16-02/R16-04/R16-05: structure is checked by *line position*, not by
    # line content. The earlier version asked whether a row outside the block
    # was "not in" the block's rows -- which a byte-identical duplicate row
    # answers "no" to, so copying `| M-01 | ... |` verbatim just after the END
    # marker passed. Two identical lines are indistinguishable by content; only
    # position tells them apart.
    lines = policy.split("\n")

    def line_index(prefix: str, start: int = 0) -> int:
        return next(i for i in range(start, len(lines)) if lines[i].startswith(prefix))

    sec_start = line_index("### 9.2 Manual controls")
    sec_end = line_index("## 10.", sec_start)
    begin_at = line_index(begin, sec_start)
    end_at = line_index(end, begin_at)

    record("T69 the BEGIN marker is a line of its own",
           lines[begin_at].strip().startswith(begin)
           and lines[begin_at].strip().endswith("-->"))
    record("T69 the END marker is a line of its own",
           lines[end_at].strip() == end.strip())
    # Uniqueness stated directly, not inferred from a downstream failure: two
    # markers would make `line_index` pick the first and the block look fine.
    record("T69 exactly one BEGIN marker exists document-wide",
           sum(1 for l in lines if l.strip().startswith(begin)) == 1,
           f"  found {sum(1 for l in lines if l.strip().startswith(begin))}")
    record("T69 exactly one END marker exists document-wide",
           sum(1 for l in lines if l.strip() == end.strip()) == 1,
           f"  found {sum(1 for l in lines if l.strip() == end.strip())}")
    record("T69 the block sits inside section 9.2",
           sec_start < begin_at < end_at < sec_end)

    block_lines = lines[begin_at + 1:end_at]
    # Structure, in order: header, separator, then exactly the control rows.
    record("T69 the block starts with the header row",
           block_lines[0] == "| ID | Manual control | Why a machine cannot do it | Accountable |",
           f"  got {block_lines[0]!r}")
    record("T69 the header is followed immediately by the separator",
           block_lines[1] == "|---|---|---|---|", f"  got {block_lines[1]!r}")
    rows = block_lines[2:]
    record("T69 every control renders exactly one row",
           len(rows) == len(gate.MANUAL_CONTROLS),
           f"  {len(rows)} rows for {len(gate.MANUAL_CONTROLS)} controls")
    record("T69 no control appears twice",
           len({r.split("|")[1].strip() for r in rows}) == len(rows))
    record("T69 the table is byte-identical to the rendered constant",
           "\n".join(rows) == expected,
           f"  expected {expected[:120]!r}\n  got      {chr(10).join(rows)[:120]!r}")
    record("T69 the generated block is not empty", bool(rows))

    # R16-05: a second hand-kept control table anywhere in the document is the
    # failure mode a section-scoped scan misses. Scanning control-shaped rows
    # document-wide avoids the false positive the change log would otherwise
    # cause: a change-log row does not begin with `| M-`, and a prose mention of
    # `M-01` is not a table row.
    stray = [
        i + 1 for i, line in enumerate(lines)
        if re.match(r"^\s*\|\s*M-\d+\s*\|", line) and not (begin_at < i < end_at)
    ]
    record("T69 no control table exists outside the generated block", not stray,
           f"  rows at lines {stray[:4]}")

    # R15-06: the marker must not re-trigger DM-09. `GENERATED_MARKER` matches
    # `DO NOT EDIT` and `GENERATED FILE`, so a marker worded to please a human
    # would make this Normative policy a generated artifact and DM-09 would
    # reject it.
    marker = lines[begin_at]
    record("T69 the generated marker does not trip DM-09",
           not gate.GENERATED_MARKER.search(marker), f"  marker {marker[:80]!r}")

    # And it must reach the output, not just the constant: a list nothing prints
    # is a comment with a data type.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        proc = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parent
                                 / "check_document_management.py"),
             "--root", str(root)],
            capture_output=True, text=True,
        )
        out = proc.stdout + proc.stderr
        missing = sorted(cid for cid, *_ in gate.MANUAL_CONTROLS if cid not in out)
        record("T69 the manual-control boundary is printed on every run",
               not missing, f"  missing from output: {missing}")


# Which policy claim is proven by which test. This exists because the same
# defect recurred three times in this series -- implementation moved, the
# sentence describing the mechanism did not -- and adding prose review did not
# stop it. A registry cannot prove a test is *sufficient* for a claim; only a
# reviewer can. What it can prove is that the claim is still attached to a test
# that still exists and still runs, so deleting or renaming the test breaks the
# claim instead of leaving it standing.
#
# `section` is the heading the claim lives under; `tests` are the record() name
# prefixes that must appear in the run.
POLICY_ASSERTIONS = (
    ("manual-controls-are-rendered-not-compared", "9.1",
     ("T69 the table is byte-identical to the rendered constant",
      "T69 no control table exists outside the generated block")),
    ("backlog-count-is-stated-once", "9.1",
     ("T70 every declared phrasing is caught",
      "T66 a reason restating the backlog count is an error")),
    # T68a proves unreadable directories are reported; it does not prove the
    # skip registry works. The seventeenth review was right to reject that
    # binding. These are the two claims, each with evidence of its own.
    ("unreadable-directories-are-reported", "test-suite",
     ("T68a an unreadable directory is reported, not silently skipped",)),
    ("skips-are-registered-and-bounded", "test-suite",
     ("T72 an unregistered skip is refused",
      "T72 a skip whose reason does not match the registry is refused")),
)


def run_policy_assertions() -> None:
    """T71: every policy claim names the tests that prove it, and they ran.

    The three blockers before this one were all "the text describes a mechanism
    the code no longer has". The fix each time was to edit the text, and the
    next round found another sentence. This case does not check that the text is
    *true* -- that is a reviewer's job and no test can do it. It checks the
    weaker, machine-checkable part: the claim is attached to named tests, those
    tests exist in this file, and they executed in this run rather than being
    skipped.

    What it does NOT prove, stated plainly so nobody reads more into a green
    run: that the named test is *sufficient* evidence for the claim. A test can
    be wrong, or right but irrelevant. The registry makes a deletion visible; it
    cannot make a bad test good.
    """
    print("policy assertions")
    import check_document_management as gate  # noqa: F401

    here = Path(__file__).resolve()
    source = here.read_text(encoding="utf-8")
    policy = (here.parents[1] / "00-governance"
              / "architecture-document-management-policy.md").read_text(encoding="utf-8")

    # The registry names tests as strings, and those strings live in this very
    # file -- so `name in source` is true by construction and proves nothing.
    # That is the self-reference the thirteenth review found in T19, arriving
    # again. What must exist is a *record() call* whose first argument is that
    # name, which is why this parses the AST instead of searching text.
    tree = ast.parse(source)
    recorded: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if (getattr(func, "id", None) or getattr(func, "attr", None)) != "record":
            continue
        if node.args and isinstance(node.args[0], ast.Constant) \
                and isinstance(node.args[0].value, str):
            recorded.add(node.args[0].value)

    missing_test: list[str] = []
    missing_section: list[str] = []
    for claim, section, tests in POLICY_ASSERTIONS:
        for name in tests:
            if name not in recorded:
                missing_test.append(f"{claim}: no record() call named {name!r}")
        if section != "test-suite" and f"### {section}" not in policy:
            missing_section.append(f"{claim}: policy has no section {section}")

    record("T71 every registered claim names tests that exist",
           not missing_test, "  " + "; ".join(missing_test))
    record("T71 every registered claim names a policy section that exists",
           not missing_section, "  " + "; ".join(missing_section))

    # Presence in the AST is not execution. A `record()` call inside `if False:`
    # is in the tree and never runs, so the claim would stand on a test that
    # proves nothing. `RESULTS_BY_NAME` is written by `record()` itself, which is
    # the only place a result exists -- this is the difference the seventeenth
    # review asked for, and the reason the earlier version's `name in source`
    # was worthless.
    not_run: list[str] = []
    failed: list[str] = []
    for claim, _, tests in POLICY_ASSERTIONS:
        for name in tests:
            if name not in RESULTS_BY_NAME:
                not_run.append(f"{claim}: {name!r} did not run")
            elif not RESULTS_BY_NAME[name]:
                failed.append(f"{claim}: {name!r} failed")
    record("T71 every registered claim rests on a test that executed",
           not not_run, "  " + "; ".join(not_run))
    record("T71 every registered claim rests on a test that passed",
           not failed, "  " + "; ".join(failed))

    # A claim resting on a skipped test is the same hole by another route: the
    # skip is deliberate, so the test never produced a result to rest on.
    skipped_claims = [
        claim for claim, _, tests in POLICY_ASSERTIONS
        if any(t in name for name in SKIPPED for t in tests)
    ]
    record("T71 no registered claim rests on a skipped test",
           not skipped_claims, f"  {skipped_claims}")

    # Structure of the registry itself. The earlier `len(...) >= 3` made three
    # a minimum contract, which would fail if two claims were legitimately
    # merged while the traceability stayed intact.
    record("T71 the registry is not empty", bool(POLICY_ASSERTIONS))
    claim_ids = [claim for claim, _, _ in POLICY_ASSERTIONS]
    record("T71 claim identifiers are unique",
           len(claim_ids) == len(set(claim_ids)),
           f"  duplicates {[c for c in claim_ids if claim_ids.count(c) > 1]}")

def run_skip_boundary() -> None:
    """T72: the skip registry refuses what it was written to refuse.

    Three properties, each tested by driving `skip()` directly rather than by
    describing it:
      - an unregistered name is refused;
      - a registered name with an appended reason is refused (exact match, not
        substring: "running as root; also whatever" is a different claim);
      - a registered name with its registered reason is accepted.

    The third matters as much as the first two: a check that refuses everything
    would pass the first two and make the registry useless.
    """
    print("skip boundary")

    probe = "T72 probe case"
    before_unexpected = len(UNEXPECTED_SKIPS)
    before_skipped = len(SKIPPED)

    # 1. Unregistered name.
    skip(probe, "no reason that matters")
    record("T72 an unregistered skip is refused",
           len(UNEXPECTED_SKIPS) > before_unexpected,
           f"  unexpected {UNEXPECTED_SKIPS[before_unexpected:]}")

    # 2. Registered name, appended reason -- the substring hole.
    name, reason = next(iter(ALLOWED_SKIPS.items()))
    mid_unexpected = len(UNEXPECTED_SKIPS)
    skip(name, reason + "; and another unrelated reason")
    record("T72 a skip whose reason does not match the registry is refused",
           len(UNEXPECTED_SKIPS) > mid_unexpected,
           f"  unexpected {UNEXPECTED_SKIPS[mid_unexpected:]}")

    # 3. Registered name with the exact registered reason is accepted.
    ok_unexpected = len(UNEXPECTED_SKIPS)
    skip(name, reason)
    record("T72 a registered skip with its exact reason is accepted",
           len(UNEXPECTED_SKIPS) == ok_unexpected,
           f"  unexpected {UNEXPECTED_SKIPS[ok_unexpected:]}")

    # The probes above deliberately polluted the skip lists. Put them back, or
    # the run's own summary would report skips that were test fixtures.
    del SKIPPED[before_skipped:]
    del UNEXPECTED_SKIPS[before_unexpected:]


def run_single_entry_callers() -> None:
    """T67: governed_files() is diagnostics only, and that is checked.


    A comment promising good behaviour is not evidence. The tenth review's
    blocker was a scan that reported `0 governed documents` and exit 0; the
    shape that produced it was an entry point that dropped diagnostics.

    What this proves, precisely: no `.py` file inside the declared scan boundary
    calls `governed_files()`, and `main()` consumes the problems returned
    alongside the files. What it does not prove: that future production code
    will live inside that boundary, or that a non-Python entry point would be
    caught. The boundary is a directory set (`skipped_dirs`), so it is a rule
    about this repository's layout, and the case below asserts the boundary
    rather than describing it.
    """
    print("single entry point")
    import check_document_management as gate

    scripts_dir = Path(__file__).resolve().parent
    repo_root = scripts_dir.parent
    offenders: list[str] = []
    # Only an actual call is an offence. A docstring, a comment or the `def`
    # line mentioning the name is not, so the check runs on the module's AST
    # rather than on text: `governed_files()` appearing in prose is exactly the
    # kind of false positive that makes a rule get ignored.
    #
    # Scope: every `.py` file the repository ships, excluding test files and the
    # build directory. Scanning only `scripts/*.py` would have been a rule about
    # a directory, not about the gate: moving the entry point to `tools/` would
    # have silently retired it. The limit is named here and asserted below, so
    # a future move shows up as a failing case rather than as a comment that
    # stopped being true.
    skipped_dirs = {"target", ".git", "tests", "__pycache__"}
    scanned = [
        path for path in sorted(repo_root.rglob("*.py"))
        if not (set(path.relative_to(repo_root).parts) & skipped_dirs)
        and not path.name.startswith("test_")
    ]
    gate_path = scripts_dir / "check_document_management.py"
    record("T67 the scan covers the gate itself, not just scripts/*.py",
           gate_path in scanned and any(p.parent != scripts_dir for p in scanned),
           f"  scanned {[p.relative_to(repo_root).as_posix() for p in scanned]}")
    for path in scanned:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            name = getattr(func, "id", None) or getattr(func, "attr", None)
            if name == "governed_files":
                offenders.append(f"{path.relative_to(repo_root).as_posix()}:{node.lineno}")
    record("T67 no production script decides a verdict from governed_files()",
           not offenders, "  " + "; ".join(offenders[:4]))

    # And main() must consume the problems, not just the files.
    gate_src = (scripts_dir / "check_document_management.py").read_text(encoding="utf-8")
    record("T67 main() takes problems from the same call as the files",
           "targets, walk_problems = collect_governed(root)" in gate_src
           and "errors: list[str] = list(walk_problems)" in gate_src)


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
    run_scan_boundary()
    run_declared_but_unread()
    run_unified_scan()
    run_schema_of_schema()
    run_structural_schema()
    run_registry_version()
    run_bilingual_count()
    run_unreadable_walk()
    run_manual_controls()
    run_count_vocabulary()
    run_skip_boundary()
    run_policy_assertions()
    run_single_entry_callers()
    run_schema_agreement()
    passed, total = sum(RESULTS), len(RESULTS)
    print(f"{passed}/{total} passed")
    if SKIPPED:
        # Printed separately, and deliberately not folded into the total: a
        # skipped case is coverage the run did not have, and `n/n passed` would
        # read as if it did.
        print(f"{len(SKIPPED)} skipped, {len(SKIPPED) - len(UNEXPECTED_SKIPS)} "
              f"registered of {len(ALLOWED_SKIPS)} allowed: " + "; ".join(SKIPPED))
    # Three ways to be green while proving less than claimed, all refused:
    # a failure, an unregistered skip, and a run in which nothing executed.
    # The last one is the reason `total` is checked: `0/0 passed` is arithmetically
    # a pass and evidentially nothing.
    if total == 0:
        print("FAIL: no cases executed")
        return 1
    if UNEXPECTED_SKIPS:
        print(f"FAIL: {len(UNEXPECTED_SKIPS)} unregistered skip(s): "
              + "; ".join(UNEXPECTED_SKIPS))
        return 1
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
