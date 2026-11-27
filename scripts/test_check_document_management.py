#!/usr/bin/env python3
"""Self-check for scripts/check_document_management.py.

Negative cases matter more than positive ones here: the parser is the trust
root, so every input outside the declared subset must fail, not degrade.

    python3 scripts/test_check_document_management.py
"""

from __future__ import annotations

import ast
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
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


def expect(
    name: str,
    text: str,
    needle: str = "",
    expect_clean: bool = False,
    *,
    msg: str = "",
) -> None:
    if needle and msg:
        raise ValueError("expect() accepts either needle or msg, not both")

    errors, _ = check_document(FILE, text)

    if expect_clean:
        record(name, not errors, f"  unexpected: {errors}")
        return

    if msg:
        ok = any(error.startswith(msg) for error in errors)
        expected = f"message prefix {msg!r}"
    elif needle:
        ok = any(needle in error for error in errors)
        expected = f"rule-id needle {needle!r}"
    else:
        ok = bool(errors)
        expected = "at least one error"

    record(name, ok, f"  expected {expected}, got {errors}")


def run_gate(root: Path, *extra: str) -> int:
    argv = sys.argv
    sys.argv = ["gate", "--root", str(root), *extra]
    try:
        return gate_main()
    finally:
        sys.argv = argv


def expect_gate(
    name: str,
    root: Path,
    want: int,
    *extra: str,
    msg: str = "",
) -> None:
    if not msg:
        code = run_gate(root, *extra)
        record(name, code == want, f"  gate returned {code}, expected {want}")
        return

    stdout = io.StringIO()
    stderr = io.StringIO()

    with redirect_stdout(stdout), redirect_stderr(stderr):
        code = run_gate(root, *extra)

    output = stdout.getvalue() + stderr.getvalue()
    message_found = any(
        line.strip().startswith(msg)
        for line in output.splitlines()
    )

    ok = code == want and message_found

    record(
        name,
        ok,
        f"  gate returned {code}, expected {want}; "
        f"expected message prefix {msg!r}; output: {output!r}",
    )


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
    try:
        parse_yaml_subset("- a\n- b\n")
    except ParseError as exc:
        record(
            "T90 parse_yaml_subset rejects a top-level sequence",
            str(exc) == "top level must be a mapping",
            f"unexpected ParseError message: {exc}",
        )
    except Exception as exc:
        record(
            "T90 parse_yaml_subset rejects a top-level sequence",
            False,
            f"expected ParseError, got {type(exc).__name__}: {exc}",
        )
    else:
        record(
            "T90 parse_yaml_subset rejects a top-level sequence",
            False,
            "expected ParseError for a top-level sequence, but parser returned",
        )


# --------------------------------------------------------------------------
# 2. Field rules
# --------------------------------------------------------------------------

def run_fields() -> None:
    print("field rules")
    expect("bad domain rejected", doc(BASE.replace("architecture", "misc")), "DM-02")
    # P0-01: a non-scalar must be an error, not an unhashable-type crash.
    expect(
        "list-valued domain is a DM-01 error",
        doc(BASE.replace(
            "  domain: architecture", "  domain: []"
        )),
        msg="DM-01 domain must be a scalar, got list",
    )
    expect(
        "approval as a scalar is a DM-01 error",
        doc(BASE.replace(
            "    approval:\n      decision_status: Draft\n", "    approval: 5\n"
        )),
        msg="DM-01 lifecycle.approval must be a mapping, got str",
    )
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
    expect("narrow approval scope rejected", doc(APPROVED.replace(
        "type: Full-document", "type: Selected-sections"
    )), "DM-03")
    expect(
        "Approved without approval_applicability rejected",
        doc(APPROVED.replace(
            "      approval_applicability: Applicable-To-Current-Version\n",
            "",
        )),
        msg="DM-03 Approved requires approval.approval_applicability",
    )
    expect(
        "Approved without approval_scope.type rejected",
        doc(APPROVED.replace(
            "        type: Full-document\n",
            "",
        )),
        msg="DM-03 Approved requires approval.approval_scope.type",
    )
    expect(
        "Canonical without canonical_scope rejected",
        doc(CANONICAL.replace(
            '    canonical_scope: "Architecture: data model design"\n',
            "",
        )),
        msg="DM-06 Canonical requires authority.canonical_scope",
    )
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

    def resolves_to_nothing(docs: dict, target_scope: str) -> bool:
        try:
            return (
                resolve_canonical(docs, target_scope)
                == NO_AUTHORITATIVE_SOURCE
            )
        except Exception:
            return False

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
    canonical_selecting_candidate = resolved_meta(selected="b.md")

    noncanonical = fresh()
    noncanonical["authority"]["canonical_status"] = "Candidate"

    record(
        "Resolved record selecting an in-scope non-Canonical member resolves to nothing",
        resolves_to_nothing(
            {
                "a.md": canonical_selecting_candidate,
                "b.md": noncanonical,
            },
            scope_id,
        ),
    )

    # 5. Resolved without the resolution block must fail closed.
    missing_block = fresh()
    missing_block["authority"]["canonical_conflict_status"] = "Resolved"
    missing_block["authority"].pop("canonical_conflict_resolution", None)
    record(
        "Resolved without a resolution block resolves to nothing",
        resolves_to_nothing(
            {"a.md": missing_block},
            scope_id,
        ),
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

    under_review_with_valid_resolution = resolved_meta()
    under_review_with_valid_resolution["authority"][
        "canonical_conflict_status"
    ] = "Under-Review"

    record(
        "Under-Review with a valid resolution block resolves to nothing",
        resolve_canonical(
            {"a.md": under_review_with_valid_resolution},
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
        resolves_to_nothing(
            {"a.md": no_canonical},
            scope_id,
        ),
    )

    # 9. Multiple Canonical members must fail closed.
    second_canonical = fresh()

    record(
        "multiple Canonical documents resolve to nothing",
        resolves_to_nothing(
            {"a.md": fresh(), "b.md": second_canonical},
            scope_id,
        ),
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
    invalid_resolution = fresh()
    invalid_resolution["authority"]["canonical_conflict_status"] = "Resolved"
    invalid_resolution["authority"]["canonical_conflict_resolution"] = None

    record(
        "Resolved with a non-mapping resolution block resolves to nothing",
        resolves_to_nothing(
            {"a.md": invalid_resolution},
            scope_id,
        ),
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
        resolves_to_nothing(one, "architecture/unknown-scope"),
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
    root = Path(tmp) / "repo"
    root.mkdir(parents=True, exist_ok=True)
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
        expect_gate(
            "DM-13 missing supersedes target fails",
            root,
            1,
            msg=(
                "DM-13 00-governance/a.md: "
                "supersedes target does not exist: 00-governance/gone.md"
            ),
        )

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
        (root / "00-governance" / "a.md").write_text(doc(BASE.replace(
            "    approval:\n      decision_status: Draft",
            "    supersession:\n      supersedes: 00-governance/b.md\n"
            "    approval:\n      decision_status: Draft",
        )), encoding="utf-8")
        # A string supersedes is also caught by the schema typing pass
        # (`must be sequence, got str`), so `want=1` alone would pass with this
        # diagnostic deleted. The `msg=` prefix is the binding.
        expect_gate(
            "DM-13 a supersedes value that is a string is refused",
            root, 1,
            msg="DM-13 00-governance/a.md: supersedes must be a list",
        )

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
        expect_gate(
            "T10 counterpart not naming its source fails",
            root,
            1,
            msg=(
                "DM-12 00-governance/a.md <-> docs/en/a.md: "
                "the counterpart does not name 00-governance/a.md as its source"
            ),
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        write_group(
            root,
            source=source_block,
            mirrors={
                "en": '    source: "00-governance/missing.md"',
                "zh-CN": mirror_block,
            },
        )
        expect_gate(
            "DM-12 source not classified as governed fails",
            root,
            1,
            msg=(
                "DM-12 docs/en/a.md: names 00-governance/missing.md "
                "as its source, but that file is not a classified governed document"
            ),
        )

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
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=True,
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
        expect_gate(
            "edited body invalidates approval",
            root,
            1,
            msg=(
                "00-governance/a.md: DM-10 content changed after "
                "approved_version: modification_status MUST be Pending-Reapproval"
            ),
        )

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


# --------------------------------------------------------------------------
# 5d. Git output decoding: locale-independent, and never a content verdict
# --------------------------------------------------------------------------

def run_git_decode_locale() -> None:
    """T95: an undecodable read is INCOMPLETE, never "the file was absent".

    Measured on a GBK console: `subprocess(text=True)` decoded git's stdout with
    the console codec, a UTF-8 document raised UnicodeDecodeError in the reader
    thread, `stdout` arrived as None, and DM-10 reported nine documents as
    "did not exist at approved_version" while `git cat-file -e` says every one
    of them exists at its pin. A decode failure and a real absence must not
    share a message, and neither may become a crash.
    """
    print("git output decoding (T95, locale-independent)")

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        target = root / "00-governance" / "a.md"
        # Git stores these bytes happily; no UTF-8 reader can decode them.
        target.write_bytes(b"---\ndocument_metadata:\n\xff\xfe not utf-8\n---\n")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "approved version with non-UTF-8 bytes")
        pinned = _git(root, "rev-parse", "HEAD")

        target.write_text(
            doc(APPROVED.replace('"deadbeef"', f'"{pinned}"')), encoding="utf-8"
        )
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "record approval")

        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = run_gate(root)
        output = stdout.getvalue() + stderr.getvalue()
        record(
            "T95a an undecodable approved version is INCOMPLETE (exit 2)",
            code == 2,
            f"  gate returned {code}, expected 2; output {output[-600:]!r}",
        )
        record(
            "T95a a decode failure is named, and absence is not asserted",
            "decode" in output and "did not exist" not in output,
            f"  output {output[-600:]!r}",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed without the governed file")
        before = _git(root, "rev-parse", "HEAD")
        (root / "00-governance" / "a.md").write_text(
            doc(APPROVED.replace('"deadbeef"', f'"{before}"')), encoding="utf-8"
        )
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "record approval")
        # The counterfactual: the message T95a removes must still exist for the
        # case where it is true, or the guard became a blanket silence.
        expect_gate(
            "T95b a pin that genuinely lacks the file still says it did not exist",
            root,
            1,
            msg=(
                "00-governance/a.md: DM-10 00-governance/a.md did not exist at "
                f"approved_version {before[:12]}"
            ),
        )


# --------------------------------------------------------------------------
# 5a. Approval scope (issue #833): the declared scope must be one the gate
#     honours. `Selected-sections` and `Selected-assets` were declarable for
#     months and never read: DM-10 hashed the whole body either way, so an edit
#     outside the "selected" part failed (pretending the scope held) and a
#     section list naming nothing was accepted (pretending the scope held).
#     Both directions were silent, so these cases bind the declaration itself.
# --------------------------------------------------------------------------

def run_approval_scope() -> None:
    print("approval scope (#833)")

    # (a) A value the gate cannot honour is refused by name, so it cannot be
    # read as a narrower approval than the one DM-10 checks.
    for scope in ("Selected-sections", "Selected-assets"):
        expect(
            f"T86 {scope} scope is refused, not reinterpreted",
            doc(APPROVED.replace("type: Full-document", f"type: {scope}")),
            "not implemented",
        )
        # Reverting the gate to the old enumeration makes the case above record
        # a failure: `expect()` sees no error at all.
    record(
        "T86 a refused scope names only Full-document as honoured",
        "Only 'Full-document' is honoured" in "".join(
            check_document(FILE, doc(APPROVED.replace(
                "type: Full-document", "type: Selected-sections")))[0]
        ),
        "  the diagnostic does not say what is honoured",
    )

    # (b) The two lists those scopes were declared with are gone: #904 removed
    # them from the schema and the corpus together, because with the values gone
    # they could only ever be empty. `run_scope_key_removal()` binds that.

    # (c) Control: `Full-document` behaves exactly as before. An unchanged body
    # passes; an edited body still fails DM-10, and fails with DM-10 rather than
    # with a scope diagnostic.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        target = root / "00-governance" / "a.md"
        body = "body: approved text"
        template = doc(APPROVED.replace('"deadbeef"', '"SHA"'))
        target.write_text(template.replace("# Title", body), encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "approved")
        sha = _git(root, "rev-parse", "HEAD")
        recorded = template.replace('"SHA"', f'"{sha}"')
        target.write_text(recorded.replace("# Title", body), encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "record approval")
        expect_gate("T88 Full-document with an unchanged body still passes",
                    root, 0)
        target.write_text(recorded.replace("# Title", "edited text"),
                          encoding="utf-8")
        code, out, err = _run_capture(root)
        output = out + err
        record("T88 Full-document with an edited body still fails DM-10",
               code == 1 and "DM-10 content changed after approved_version" in output,
               f"  exit {code}, DM-10 present: "
               f"{'DM-10 content changed after approved_version' in output}")


# --------------------------------------------------------------------------
# 5a-2. Approval scope keys (issue #904). Ruling 76 in #833 ordered the two
#     dead keys removed from `SCOPE_KEYS` AND from the corpus in the same
#     change; #888 removed the values and left the keys, so every approved
#     document carried two empty lists that declared nothing. These cases fail
#     if either key is readmitted to the gate, which is the only thing that
#     could let the shape back into the corpus unnoticed.
# --------------------------------------------------------------------------

def run_scope_key_removal() -> None:
    print("approval scope keys (#904)")
    import check_document_management as gate

    def refuse(name: str, injected: str) -> None:
        text = doc(APPROVED.replace(
            "        type: Full-document\n",
            f"        type: Full-document\n        {injected}\n",
        ))
        key = injected.split(":")[0]
        try:
            errors, _ = check_document(FILE, text)
            assert errors, f"a document carrying {key} was accepted by the gate"
            assert any("approval_scope" in e and "unknown key" in e for e in errors), \
                f"no approval_scope unknown-key diagnostic for {key}: {errors}"
        except AssertionError as exc:
            record(name, False, f"  AssertionError: {exc}")
            return
        record(name, True)

    refuse("T94 a document carrying included_sections is refused",
           "included_sections: []")
    refuse("T94 a document carrying included_assets is refused",
           "included_assets: []")
    refuse("T94 a non-empty included_sections is refused, not reinterpreted",
           "included_sections:\n          - nowhere.md")

    try:
        assert gate.SCOPE_KEYS == {"type"}, (
            "SCOPE_KEYS readmits "
            f"{sorted(set(gate.SCOPE_KEYS) - {'type'})}; #904 removed those keys "
            "from the corpus in the same change"
        )
    except AssertionError as exc:
        record("T94 SCOPE_KEYS admits only 'type'", False, f"  AssertionError: {exc}")
    else:
        record("T94 SCOPE_KEYS admits only 'type'", True)

    # Control: the shape the corpus actually uses is still accepted, so the
    # cases above are not passing because the fixture is broken.
    expect("T94 the corpus shape (type only) is still accepted",
           doc(APPROVED), expect_clean=True)

# --------------------------------------------------------------------------
# 5b. DM-10 scope: an incremental run blames only the documents it touched
#     (issue #808). A stale pin on an untouched document is counted, not
#     charged to whichever pull request happens to run the gate.
# --------------------------------------------------------------------------

# Exactly ONE DM-10 error per document: stale (the recorded content-hash is not
# the body's), honest about the modification, but still presenting the approval
# as applicable. The count assertions below are per-error, so a fixture that
# emitted two errors per document would make "1" pass for the wrong reason.
DM10_STALE = (
    APPROVED.replace("scheme: git", "scheme: content-hash")
    .replace('"deadbeef"', '"' + "0" * 64 + '"')
    .replace("modification_status: Unchanged", "modification_status: Pending-Reapproval")
)
DM10_COUNT_ONE = "DM-10 out-of-scope stale bindings: 1"
DM10_ERROR = "DM-10 content changed after approved_version"

def _dm10_repo(tmp: str) -> tuple[Path, str]:
    """A repository whose out-of-scope document `b.md` already carries a stale pin."""
    root = _repo(tmp)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "gate@example.invalid")
    _git(root, "config", "user.name", "gate")
    (root / "00-governance" / "b.md").write_text(doc(DM10_STALE), encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "seed with a stale pin")
    return root, _git(root, "rev-parse", "HEAD")

def _run_capture(root: Path, *extra: str) -> tuple[int, str, str]:
    import contextlib
    import io

    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = run_gate(root, *extra)
    return code, out.getvalue(), err.getvalue()

def test_incremental_in_scope_stale_pin_still_fails() -> None:
    """The verdict narrows the scope; it does not switch the gate off."""
    with tempfile.TemporaryDirectory() as tmp:
        root, base = _dm10_repo(tmp)
        (root / "00-governance" / "a.md").write_text(doc(DM10_STALE), encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "touch a")
        code, out, err = _run_capture(root, "--require-changed", base)
        in_scope = f"00-governance/a.md: {DM10_ERROR}"
        # Errors go to stderr; checking the merged stream could not tell a
        # refusal from a note about the same document.
        refused = in_scope in err
        record(
            "T81 incremental run still fails a stale pin on a document it changed",
            code == 1 and refused,
            f"  gate returned {code}, expected 1; in-scope diagnostic on stderr: {refused}",
        )

def test_incremental_out_of_scope_stale_pin_is_counted_not_failed() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root, base = _dm10_repo(tmp)
        (root / "notes.txt").write_text("unrelated change\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "touch nothing governed")
        code, out, err = _run_capture(root, "--require-changed", base)
        # The ruling asks for two things joined by "and": a note naming the
        # document, and a counted line. A number alone says how many, not which.
        # The count is asserted exactly: one stale pin must yield exactly one
        # note. "a note exists" would also pass if the collector swallowed every
        # governed document, which is the mistake T84's sibling catches.
        # Filtered on the note prefix, not on "DM-10 out-of-scope" anywhere: the
        # count line is itself "DM-10 out-of-scope stale bindings: N", so a
        # substring match counts it as a note and every run reports two. The
        # trailing space is deliberate too: the "approval binding NOT VERIFIED"
        # note is f"DM-10 {rel}: ...", which would match this prefix for a
        # document under an `out-of-scope/` directory.
        dm10_notes = [l for l in out.splitlines() if l.startswith("  note: DM-10 out-of-scope ")]
        noted = len(dm10_notes) == 1 and "00-governance/b.md" in dm10_notes[0]
        counted = DM10_COUNT_ONE in out.splitlines()
        leaked = f"00-governance/b.md: {DM10_ERROR}" in err
        record(
            "T82 incremental run counts an out-of-scope stale pin instead of failing it",
            code == 0 and counted and noted and not leaked,
            f"  gate returned {code}, expected 0; count line exact: {counted}; "
            f"out-of-scope notes: {len(dm10_notes)} (want 1, naming b.md); "
            f"DM-10 error on stderr: {leaked}",
        )

def test_whole_tree_run_still_reports_every_stale_pin() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root, _ = _dm10_repo(tmp)
        code, out, err = _run_capture(root)
        reported = f"00-governance/b.md: {DM10_ERROR}"
        record(
            "T83 whole-tree run still reports every stale pin",
            code == 1 and reported in err,
            f"  gate returned {code}, expected 1; b.md diagnostic on stderr: "
            f"{reported in err}",
        )

def test_incremental_one_in_scope_one_out_of_scope() -> None:
    """Classified per document, not as one global either/or."""
    with tempfile.TemporaryDirectory() as tmp:
        root, base = _dm10_repo(tmp)
        (root / "00-governance" / "a.md").write_text(doc(DM10_STALE), encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "touch a only")
        code, out, err = _run_capture(root, "--require-changed", base)
        in_scope = f"00-governance/a.md: {DM10_ERROR}" in err
        out_of_scope = f"00-governance/b.md: {DM10_ERROR}" in err
        # Exactly one note, and it belongs to the untouched document: an
        # implementation that noted both documents, or neither, or duplicated
        # the line, all keep "some note exists" true while being wrong. Same
        # prefix rule as T82 -- see the comment there for the two traps.
        dm10_notes = [l for l in out.splitlines() if l.startswith("  note: DM-10 out-of-scope ")]
        noted = len(dm10_notes) == 1 and "00-governance/b.md" in dm10_notes[0]
        counted = DM10_COUNT_ONE in out.splitlines()
        record(
            "T84 one in-scope and one out-of-scope stale pin are classified per document",
            code == 1 and in_scope and not out_of_scope and noted and counted,
            f"  gate returned {code}, expected 1; a.md on stderr: {in_scope}; "
            f"b.md on stderr: {out_of_scope}; out-of-scope notes: {len(dm10_notes)} "
            f"(want 1, naming b.md only); count line exactly 1: {counted}",
        )

def test_incremental_zero_out_of_scope_still_prints_the_count() -> None:
    """A missing line cannot be told apart from a run that never looked."""
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        (root / "00-governance" / "b.md").write_text(doc(BASE), encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed, no approvals")
        base = _git(root, "rev-parse", "HEAD")
        (root / "notes.txt").write_text("unrelated change\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "touch nothing governed")
        code, out, err = _run_capture(root, "--require-changed", base)
        zero = "DM-10 out-of-scope stale bindings: 0"
        record(
            "T85 incremental run with no out-of-scope stale pin prints the zero count",
            code == 0 and zero in (out + err).splitlines(),
            f"  gate returned {code}, expected 0; zero count line present: "
            f"{zero in (out + err).splitlines()}",
        )

def test_out_of_scope_stale_pin_emits_both_a_note_and_a_count() -> None:
    """The ruling's sentence joins two things with "and"; assert both.

    #862 shipped the counted line alone. A suite that asserts only the count
    stays green when the note disappears, which is exactly how that happened.
    This case is the regression gate for the half nobody was watching: the
    note must exist, it must name the document, and it must never be an error.
    """
    with tempfile.TemporaryDirectory() as tmp:
        root, base = _dm10_repo(tmp)
        (root / "notes.txt").write_text("unrelated change\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "touch nothing governed")
        code, out, err = _run_capture(root, "--require-changed", base)
        note_lines = [
            line for line in out.splitlines()
            if line.startswith("  note: DM-10 out-of-scope 00-governance/b.md:")
        ]
        count_lines = [line for line in out.splitlines() if line == DM10_COUNT_ONE]
        # The error form puts the sentence on stderr. The note must not appear
        # there: a note that also fails the run is the bug this issue fixes.
        on_stderr = "DM-10 out-of-scope" in err
        record(
            "T86 an out-of-scope stale pin is both noted and counted, never failed",
            code == 0 and len(note_lines) == 1 and len(count_lines) == 1
            and not on_stderr,
            f"  gate returned {code}, expected 0; note lines: {len(note_lines)}; "
            f"count lines: {len(count_lines)}; on stderr: {on_stderr}",
        )

def run_dm10_scope() -> None:
    print("DM-10 scope (issue #808)")
    test_incremental_in_scope_stale_pin_still_fails()
    test_incremental_out_of_scope_stale_pin_is_counted_not_failed()
    test_whole_tree_run_still_reports_every_stale_pin()
    test_incremental_one_in_scope_one_out_of_scope()
    test_incremental_zero_out_of_scope_still_prints_the_count()
    test_out_of_scope_stale_pin_emits_both_a_note_and_a_count()

def run_prose_status_census() -> None:
    print("prose-only document status (issue #481)")
    test_prose_only_work_item_status_is_counted_not_blocking()
    test_frontmatter_clears_the_prose_only_count()
    test_prose_only_status_counts_files_outside_work_items()

def test_prose_only_work_item_status_is_counted_not_blocking() -> None:
    """A prose-only status is counted, never failed.

    The defect is that DM-02 is structurally blind to these files, not that 89
    of them are "wrong". Reporting them as errors would turn the gate red for
    every unrelated change, so the count must arrive as a notice, and an
    increment that does not touch the file must still pass.
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        work = root / "14-ai-development" / "work-items"
        work.mkdir(parents=True, exist_ok=True)
        work_item = work / "AID-X.md"
        work_item.write_text(
            "# AID-X\n\n- Status: PROPOSED — pending owner adoption\n", encoding="utf-8"
        )
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed with a prose-only work item")
        base = _git(root, "rev-parse", "HEAD")
        (root / "notes.txt").write_text("unrelated change\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "touch nothing governed")
        code_with, out, err = _run_capture(root, "--require-changed", base)
        work_item.unlink()
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "drop the work item")
        code_without, out_zero, _ = _run_capture(root, "--require-changed", base)
        counted = any(
            line.startswith("::notice::advisory (non-blocking): 1 governed document(s)")
            for line in out.splitlines()
        )
        zero = any(
            line.startswith("::notice::advisory (non-blocking): 0 governed document(s)")
            for line in out_zero.splitlines()
        )
        named = any(
            "x1 PROPOSED — pending owner adoption" in line for line in out.splitlines()
        )
        on_stderr = "advisory" in err
        record(
            "T87 prose-only work-item status is counted as advisory, never failed",
            code_with == 0 and code_without == 0 and counted and zero and named
            and not on_stderr,
            f"  exit with={code_with} without={code_without}, expected 0 both; "
            f"count line: {counted}; zero line when absent: {zero}; "
            f"value printed: {named}; on stderr: {on_stderr}",
        )

def test_frontmatter_clears_the_prose_only_count() -> None:
    """The ratchet can go down only by conversion, so conversion must count.

    A file that carries both a metadata block and the original prose line is no
    longer prose-only: the human record stays, and DM-02 now sees the status.
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        work = root / "14-ai-development" / "work-items"
        work.mkdir(parents=True, exist_ok=True)
        (work / "AID-Y.md").write_text(
            doc(BASE) + "\n- Status: PROPOSED — pending owner adoption\n",
            encoding="utf-8",
        )
        _code, out, _err = _run_capture(root)
        zero = any(
            line.startswith("::notice::advisory (non-blocking): 0 governed document(s)")
            for line in out.splitlines()
        )
        no_values = not any("x1 PROPOSED" in line for line in out.splitlines())
        record(
            "T88 front-matter plus the original prose line is no longer prose-only",
            zero and no_values,
            f"  zero count line: {zero}; value lines absent: {no_values}",
        )

def test_prose_only_status_counts_files_outside_work_items() -> None:
    """The population is the governed set, not one directory (issue #481).

    A census that only walked `14-ai-development/work-items/` reported 5 files
    while the same class sat in `14-ai-development/adr/` and at the top level
    of `14-ai-development/`. The count claims to measure "files DM-02 cannot
    see", so it must cover exactly the files DM-02 is applied to.
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        adr = root / "14-ai-development" / "adr"
        adr.mkdir(parents=True, exist_ok=True)
        (adr / "ADR-X.en.md").write_text(
            "# ADR-X\n\n- Status: PROPOSED — decision pending\n", encoding="utf-8"
        )
        (root / "14-ai-development" / "TOP-LEVEL.md").write_text(
            "# TOP-LEVEL\n\n- Status: PROPOSED — decision pending\n", encoding="utf-8"
        )
        _code, out, _err = _run_capture(root)
        counted = any(
            line.startswith("::notice::advisory (non-blocking): 2 governed document(s)")
            for line in out.splitlines()
        )
        record(
            "T89 prose-only status outside work-items is counted too",
            counted,
            f"  expected '2 governed document(s)', got: "
            f"{[l for l in out.splitlines() if 'governed document(s)' in l]}",
        )


def run_shallow_history() -> None:
    """T70: an unanswerable question from a shallow clone is not a violation."""
    print("shallow history (exit 2, never a fabricated DM-10)")
    import check_document_management as gate

    real_git = gate.git

    def pretending_shallow(root_arg, *args, **kwargs):
        if args[:2] == ("rev-parse", "--is-shallow-repository"):
            return "true\n"
        return real_git(root_arg, *args, **kwargs)

    def pretending_garbage(root_arg, *args, **kwargs):
        if args[:2] == ("rev-parse", "--is-shallow-repository"):
            return "perhaps\n"
        return real_git(root_arg, *args, **kwargs)

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        target = root / "00-governance" / "a.md"
        body = "body: approved text"
        template = doc(APPROVED.replace('"deadbeef"', '"SHA"'))
        target.write_text(template.replace("# Title", body), encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "approved")
        sha = _git(root, "rev-parse", "HEAD")
        target.write_text(
            template.replace('"SHA"', f'"{sha}"').replace("# Title", body),
            encoding="utf-8",
        )
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "record approval")

        import contextlib
        import io

        def capture(*extra: str) -> tuple[int, str]:
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = run_gate(root, *extra)
            return code, out.getvalue() + err.getvalue()

        try:
            # Benign shallow: history is truncated but every pin resolves, so
            # the gate's verdict is exactly its full-clone verdict. Refusing
            # here would be a capability regression, not a safety win.
            gate.git = pretending_shallow
            code, output = capture()
            record("T70 benign shallow clone still produces its normal verdict",
                   code == 0, f"  gate returned {code}: {output.strip()[:200]}")

            code, output = capture("--require-changed", "no-such-ref")
            record("T70 shallow clone does not call an upstream ref a bad ref",
                   code == 2 and "does not resolve to a commit" not in output
                   and "shallow" in output,
                   f"  gate returned {code}: {output.strip()[:200]}")

            # The defect: a pin that cannot resolve because history is cut off.
            fabricated = (
                target.read_text(encoding="utf-8")
                .replace(f'"{sha}"', '"0000000000000000000000000000000000000000"')
            )
            target.write_text(fabricated, encoding="utf-8")

            code, output = capture()
            record("T70 unresolvable pin on a shallow clone exits 2 (INCOMPLETE)",
                   code == 2, f"  gate returned {code}")
            record("T70 shallow clone reports no fabricated DM-10 violation",
                   "is not a commit in this repository" not in output,
                   f"  output: {output.strip()[:200]}")
            record("T70 shallow clone names the condition and the remedy",
                   "shallow" in output and "git fetch --unshallow" in output,
                   f"  output: {output.strip()[:200]}")

            gate.git = pretending_garbage
            code, output = capture()
            record("T70 undeterminable history fails closed at 2", code == 2,
                   f"  gate returned {code}")
        finally:
            gate.git = real_git

        # Control: complete history still rejects the same fabricated pin.
        # The guard must not have weakened DM-10.
        code, output = capture()
        record("T70 full history still rejects a fabricated approved_version",
               code == 1 and "is not a commit in this repository" in output,
               f"  gate returned {code}: {output.strip()[:200]}")


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
        import contextlib
        import io

        captured_stdout = io.StringIO()
        captured_stderr = io.StringIO()
        with contextlib.redirect_stdout(captured_stdout), contextlib.redirect_stderr(captured_stderr):
            code = run_gate(root, "--require-changed", base)

        output = captured_stdout.getvalue() + captured_stderr.getvalue()
        deletion_only_message = "the increment contained only deletions"

        record(
            "T77 deletion plus Markdown modification remains applicable",
            code == 0 and deletion_only_message not in output,
            (
                f"  gate returned {code}, expected 0; "
                f"deletion-only message present: "
                f"{deletion_only_message in output}"
            ),
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
        import contextlib
        import io

        captured_stdout = io.StringIO()
        captured_stderr = io.StringIO()
        with contextlib.redirect_stdout(captured_stdout), contextlib.redirect_stderr(captured_stderr):
            code = run_gate(root, "--require-changed", base)

        output = captured_stdout.getvalue() + captured_stderr.getvalue()
        deletion_only_message = "the increment contained only deletions"

        record(
            "T78 deletion plus code-only modification remains applicable",
            code == 0 and deletion_only_message not in output,
            (
                f"  gate returned {code}, expected 0; "
                f"deletion-only message present: "
                f"{deletion_only_message in output}"
            ),
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

        import contextlib
        import io

        captured_stdout = io.StringIO()
        captured_stderr = io.StringIO()
        with contextlib.redirect_stdout(captured_stdout), contextlib.redirect_stderr(captured_stderr):
            code = run_gate(root, "--require-changed", base)

        output = captured_stdout.getvalue() + captured_stderr.getvalue()
        expected_error = (
            "DM-01 missing document_metadata block: "
            "00-governance/unclassified-new.md"
        )
        record(
            "T80 deletion plus unclassified governed document still fails DM-01",
            code == 1 and expected_error in output,
            (
                f"  gate returned {code}, expected 1; "
                f"expected DM-01 diagnostic present: "
                f"{expected_error in output}"
            ),
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

    # T20a/T20b: the two DM-12 sites that no case observed.
    #
    # Both were established by deleting the branch and watching the suite stay
    # green (#827 AC-A). Each inputs one thing -- a mapping where a path must
    # be, a source that names a mirror -- so the assertion names this site and
    # not a neighbour that fires on the same document.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "a.md").write_text(doc(BASE.replace(
            "  role: design-specification\n",
            "  role: design-specification\n"
            "  bilingual_counterpart:\n    en:\n      nested: x\n",
        )), encoding="utf-8")
        # Two emitters refuse this document: the schema typing pass says
        # `must be nullable-string`, and the path resolver says the thing
        # below. Asserting the resolver's wording is what binds the resolver.
        expect_gate(
            "T20a a counterpart path that is a mapping is refused by the resolver",
            root, 1,
            msg="DM-01 00-governance/a.md: bilingual_counterpart.en must be a string path, got dict",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "a.md").write_text(doc(BASE.replace(
            "  role: design-specification\n",
            "  role: design-specification\n"
            '  bilingual_counterpart:\n    source: "docs/en/a.md"\n',
        )), encoding="utf-8")
        expect_gate(
            "T20b a source that names a mirror is refused by name",
            root, 1,
            msg=("DM-12 00-governance/a.md: source must be the authoritative "
                 "file, not a mirror"),
        )

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

    # T23a/T23b: the two DM-14 registry-shape sites no case observed (#827 AC-A).
    #
    # Both are shape errors in the registry itself, so each fixture writes one
    # malformed registry and asserts the site's own wording. `want=1` alone
    # would not do: an empty governed list also trips "scope registry and
    # NORMATIVE_ROOTS disagree", and a non-mapping excluded also trips "top-level
    # directories not accounted for", so the run is red either way.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "document-scope-registry.yaml").write_text(
            registry_text([]), encoding="utf-8"
        )
        expect_gate(
            "T23a a registry with an empty governed list is refused",
            root, 1,
            msg="DM-14 00-governance/document-scope-registry.yaml must declare a non-empty governed list",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        base = registry_text(governed)
        # `excluded:` with a sequence value is valid YAML that the gate parses,
        # so the shape check is reached rather than the parser.
        (root / "00-governance" / "document-scope-registry.yaml").write_text(
            re.sub(r"^excluded:\n(?:  .*\n|\n)*", "excluded:\n  - tools\n", base, flags=re.M),
            encoding="utf-8",
        )
        expect_gate(
            "T23b an excluded block that is not a mapping is refused",
            root, 1,
            msg="DM-14 00-governance/document-scope-registry.yaml excluded must be a mapping",
        )

    # Declared scope must equal enforced scope, in both directions.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "document-scope-registry.yaml").write_text(
            registry_text(governed + ["16-phantom"]), encoding="utf-8"
        )
        expect_gate(
            "T24 registry naming a root the gate does not scan fails",
            root,
            1,
            msg=(
                "DM-14 00-governance/document-scope-registry.yaml "
                "names directories that do not exist: ['16-phantom']"
            ),
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "document-scope-registry.yaml").write_text(
            registry_text(governed[1:]), encoding="utf-8"
        )
        expect_gate("T25 registry omitting a scanned root fails", root, 1)

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        shutil.rmtree(root / "docs" / "en")
        expect_gate(
            "DM-14 missing English mirror directory fails",
            root,
            1,
            msg="DM-14 bilingual mirror directory docs/en is missing",
        )

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
        expect_gate(
            "T38 governed file that does not exist is an error",
            root,
            1,
            msg=(
                f"DM-14 collect_governed: governed file {GOVERNED_FILES[0]} "
                "is not a regular file inside the repository"
            ),
        )

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
                root,
                1,
                msg=(
                    "DM-14 governed file 00-governance/extra.md "
                    "is already covered by root 00-governance; drop the individual entry"
                ),
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

    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as tmp:
        root = _repo(tmp)
        registry_path = (
            root / "00-governance" / "document-scope-registry.yaml"
        )
        registry_path.write_text("- a\n- b\n", encoding="utf-8")

        expect_gate(
            "T91 top-level sequence scope registry is rejected by parser",
            root,
            1,
            msg=(
                "DM-14 cannot read scope registry "
                "00-governance/document-scope-registry.yaml: "
                "top level must be a mapping"
            ),
        )

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
    expect(
        "T27 null where the schema declares mapping is a type error",
        null_mapping,
        msg="DM-01 lifecycle.approval.approval_scope must be mapping, got NoneType",
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
        "Selected-assets' is not implemented",
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
        "Selected-sections' is not implemented",
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
        outside = Path(tmp) / "outside-docs-t49"
        outside.mkdir(exist_ok=True)
        for i in range(3):
            (outside / f"f{i}.md").write_text("# x\n", encoding="utf-8")
        shutil.rmtree(root / "docs")
        (root / "docs").symlink_to(outside, target_is_directory=True)
        code, out = run(root)
        record("T49 symlinked backlog root is named in the diagnostic",
               code != 0 and "docs is a symbolic link" in out,
               f"  exit {code}, output {out[:200]}")

    # T50: a symlinked directory inside a backlog root is reported by path.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        outside = Path(tmp) / "outside-sub-t50"
        outside.mkdir(exist_ok=True)
        (outside / "external.md").write_text("# ext\n", encoding="utf-8")
        (root / "docs" / "linked").symlink_to(outside, target_is_directory=True)
        code, out = run(root)
        record("T50 symlinked directory inside a backlog root is reported",
               code != 0 and "docs/linked is a symbolic link" in out,
               f"  exit {code}, output {out[:200]}")

    # T51: a symlinked .md inside a backlog root is reported by path.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        outside = Path(tmp) / "outside-file-t51.md"
        outside.write_text("# ext\n", encoding="utf-8")
        (root / "docs" / "linked.md").symlink_to(outside)
        code, out = run(root)
        record("T51 symlinked markdown file inside a backlog root is reported",
               code != 0 and "docs/linked.md is a symbolic link" in out,
               f"  exit {code}, output {out[:200]}")

    # T51b: a bilingual mirror directory that is a symlink is refused by name.
    #
    # `is_dir()` follows links, so a symlinked mirror looked present while the
    # scanner refused to descend into it: the registry asserted the mirror
    # existed and the run classified nothing from it. Both halves are asserted
    # -- `docs/en` is the link, `docs/zh-CN` is a real directory -- because if
    # the second mirror were also absent the "is missing" diagnostic would fire
    # in the same message and this case would pass for the wrong reason.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        outside = Path(tmp) / "outside-mirror-t51b"
        outside.mkdir()
        (outside / "leaked.md").write_text(doc(BASE), encoding="utf-8")
        shutil.rmtree(root / "docs" / "en")
        (root / "docs" / "en").symlink_to(outside, target_is_directory=True)
        (root / "docs" / "zh-CN").mkdir(parents=True, exist_ok=True)
        code, out = run(root)
        record("T51b symlinked bilingual mirror directory is refused by name",
               code != 0
               and "bilingual mirror directory docs/en is a symbolic link" in out
               and "a mirror must be real content of this repository" in out
               and "bilingual mirror directory docs/en is missing" not in out,
               f"  exit {code}, output {out[:240]}")

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
        outside = Path(tmp) / "outside-norm-t58"
        outside.mkdir(exist_ok=True)
        (outside / "leak.md").write_text("# leak\n", encoding="utf-8")
        (root / "00-governance" / "linked").symlink_to(outside, target_is_directory=True)
        code, out = run(root)
        record("T58 symlinked subdirectory in a normative root is reported",
               code != 0 and "00-governance/linked is a symbolic link" in out,
               f"  exit {code}, output {out[:200]}")

    # T59: a top-level symlink to a directory is not an accounted directory.
    #
    # R11-02. is_dir() follows links, so a link satisfied both "on disk" and
    # "declared" -- making a registry entry true that pointed outside the repo.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        outside = Path(tmp) / "outside-top-t59"
        outside.mkdir(exist_ok=True)
        (root / "ghost").symlink_to(outside, target_is_directory=True)
        code, out = run(root)
        record("T59 top-level symlink is reported and does not satisfy the registry",
               code != 0 and "symbolic links at the repository root" in out,
               f"  exit {code}, output {out[:200]}")

    # T60: a declared directory that is only a symlink counts as missing.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        outside = Path(tmp) / "outside-decl-t60"
        outside.mkdir(exist_ok=True)
        # `tools` is declared as excluded by the fixture registry.
        shutil.rmtree(root / "tools")
        (root / "tools").symlink_to(outside, target_is_directory=True)
        code, out = run(root)
        record("T60 declared directory that is only a symlink is reported",
               code != 0 and ("do not exist" in out or "symbolic links" in out),
               f"  exit {code}, output {out[:200]}")

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

    # Each case names the diagnostic that must carry it. `ok=True` on any
    # SystemExit proved only that the loader refused *something*: a case could
    # be satisfied by a neighbouring check, so removing its own emission went
    # unnoticed.
    mutations = {
        "required is a string": (
            "  domain:\n    kind: string\n    required: \"false\"\n",
            "declares required: 'false', which is str, not a boolean",
        ),
        "items on a string kind": (
            "  domain:\n    kind: string\n    items: string\n",
            "declares items on kind 'string'; only a sequence has items",
        ),
        "unknown kind": (
            "  domain:\n    kind: strng\n",
            "declares unknown kind 'strng'; legal kinds are",
        ),
        # This replacement leaves the original `enum:` list in place, so the YAML
        # parser refuses a second `enum:` key before the schema-of-schema sees a
        # node at all. The name says which detector answers, because a case named
        # for the enum-on-kind rule would be cited as coverage for the branch that
        # `neither kind nor fields` actually tests.
        "a second enum key": (
            "  domain:\n    kind: boolean\n    enum:\n      - x\n",
            "duplicate key 'enum'",
        ),
        "neither kind nor fields": (
            "  domain:\n    required: true\n",
            "declares no kind and no fields; the gate cannot type-check it",
        ),
    }
    for label, (replacement, expected) in mutations.items():
        mutated = src.replace(base, replacement, 1)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "00-governance").mkdir()
            (root / gate.SCHEMA_FILE).write_text(mutated, encoding="utf-8")
            try:
                gate.schema(root)
                record(f"T63 {label} is refused", False, "  schema loaded")
            except SystemExit as exc:
                record(
                    f"T63 {label} is refused",
                    expected in str(exc),
                    f"  expected {expected!r}, got {str(exc)[:160]}",
                )

    # The schema-of-schema aggregates its problems into one SystemExit, so two
    # sites can speak in the same message. Each needs its own discriminator.
    neither = (
        "  domain:\n    required: true\n",
        "declares enum on kind None, which cannot hold an enumerated value",
    )
    mutated = src.replace(base, neither[0], 1)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "00-governance").mkdir()
        (root / gate.SCHEMA_FILE).write_text(mutated, encoding="utf-8")
        try:
            gate.schema(root)
            record("T63 a node with no kind and no fields reports its own problem",
                   False, "  schema loaded")
        except SystemExit as exc:
            record(
                "T63 a node with no kind and no fields reports its own problem",
                neither[1] in str(exc),
                f"  expected {neither[1]!r}, got {str(exc)[:160]}",
            )



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


def run_restored_guards() -> None:
    """T93: the seven guards removed by #1070, checked at BOTH layers.

    #1070 was merged with seven deletions whose safety rested on a measurement
    that only ever drove the public CLI. `schema()` calls `check_schema_keys()`
    before any document is checked, so an unknown kind is refused there and can
    never reach `check_kinds()` at all: the CLI measurement was structurally
    blind to every guard inside `check_kinds`. This function tests each restored
    guard by calling it directly, and separately records what the CLI can and
    cannot see, rather than presenting one as the other.
    """
    print("restored guards (T93, direct call)")
    import check_document_management as gate

    def call(fn, *args):
        """Return ('ret', value) or ('exc', 'Type: message')."""
        try:
            value = fn(*args)
            if hasattr(value, "__next__"):
                value = list(value)
            return ("ret", value)
        except Exception as exc:  # noqa: BLE001 - the type is the assertion
            return ("exc", f"{type(exc).__name__}: {exc}")

    # --- 1/7 walk_paths: the empty-segments guard ---------------------------
    kind, got = call(gate.walk_paths, {"a": {"b": 1}}, [])
    record(
        "T93a walk_paths with no segments yields nothing instead of raising",
        kind == "ret" and got == [],
        f"  expected ('ret', []), got ({kind!r}, {got!r})",
    )
    # A non-empty call must still work: restoring the guard must not break the
    # only production use, which always passes a split dotted path.
    kind, got = call(gate.walk_paths, {"a": {"b": 1}}, ["a", "b"])
    record(
        "T93a walk_paths still resolves a real path",
        kind == "ret" and got == ["a.b"],
        f"  expected ['a.b'], got ({kind!r}, {got!r})",
    )

    # --- 2/7 walk_keys: the removed helper --------------------------------
    kind, got = call(lambda: hasattr(gate, "walk_keys"))
    record(
        "T93b walk_keys exists again",
        kind == "ret" and got is True,
        f"  expected True, got ({kind!r}, {got!r})",
    )
    kind, got = call(
        lambda: list(gate.walk_keys({"a": {"b": 1}, "c": [{"b": 2}]}, "b"))
    )
    # Direct comparison, not "nothing calls it": the function has a contract and
    # the contract is checkable whether or not a production caller uses it.
    record(
        "T93b walk_keys matches one segment at any depth",
        kind == "ret" and got == ["a.b", "c[0].b"],
        f"  expected ['a.b', 'c[0].b'], got ({kind!r}, {got!r})",
    )

    # --- 3/7 _kind_ok: the unreachable-kind assertion ----------------------
    kind, got = call(gate._kind_ok, "x", "NOT_A_KIND")
    record(
        "T93c _kind_ok refuses a kind outside KINDS",
        kind == "exc" and got.startswith("AssertionError:")
        and "NOT_A_KIND" in got,
        f"  expected AssertionError naming the kind, got ({kind!r}, {got!r})",
    )
    # The restored raise must not fire on the kinds that are legal, or it would
    # turn every valid document into a crash.
    for value, kind_name, want in (
        ("x", "string", True),
        (1, "boolean", False),
        (None, "nullable-string", True),
        ({"a": 1}, "mapping", True),
        (["a"], "sequence", True),
    ):
        kind, got = call(gate._kind_ok, value, kind_name)
        record(
            f"T93c _kind_ok({kind_name}) still answers {want}",
            kind == "ret" and got is want,
            f"  expected {want}, got ({kind!r}, {got!r})",
        )

    # --- 4/7 check_kinds: the non-mapping spec guard -----------------------
    errors: list[str] = []
    kind, got = call(gate.check_kinds, {"k": "v"}, {"fields": {"k": "nope"}}, errors)
    record(
        "T93d a non-mapping schema field is a DM-01 error, not an AttributeError",
        kind == "ret"
        and errors == ["DM-01 schema field k is not a mapping"],
        f"  expected the DM-01 diagnostic, got ({kind!r}, {got!r}, errors={errors})",
    )

    # --- 5/7 check_kinds: the unknown-kind guard ---------------------------
    errors = []
    kind, got = call(
        gate.check_kinds, {"k": "v"}, {"fields": {"k": {"kind": "NOT_A_KIND"}}}, errors
    )
    record(
        "T93e an unknown kind is reported as a schema defect",
        kind == "ret"
        and errors == ["DM-01 schema field k declares unknown kind 'NOT_A_KIND'"],
        f"  got ({kind!r}, {got!r}, errors={errors})",
    )
    # The distinction that matters: without the guard the same input is reported
    # against the *document* value ("k must be NOT_A_KIND"), which sends the
    # reader to the wrong file.
    record(
        "T93e the unknown-kind diagnostic does not blame the document value",
        not any(e.startswith("DM-01 k must be") for e in errors),
        f"  got {errors}",
    )

    # --- 6/7 check_kinds: the unknown items-kind guard ---------------------
    errors = []
    kind, got = call(
        gate.check_kinds,
        {"k": ["a"]},
        {"fields": {"k": {"kind": "sequence", "items": "NOT_A_KIND"}}},
        errors,
    )
    record(
        "T93f an unknown items kind is reported as a schema defect",
        kind == "ret"
        and errors
        == ["DM-01 schema field k declares unknown items kind 'NOT_A_KIND'"],
        f"  got ({kind!r}, {got!r}, errors={errors})",
    )
    record(
        "T93f the unknown-items diagnostic does not blame the document element",
        not any("k[0] must be" in e for e in errors),
        f"  got {errors}",
    )

    # --- 7/7 check_schema_keys: the non-mapping node guard -----------------
    for label, payload in (
        ("a string", "not-a-mapping"),
        ("a list", ["x"]),
        ("None", None),
    ):
        kind, got = call(gate.check_schema_keys, {"fields": payload})
        record(
            f"T93g check_schema_keys reports a fields node that is {label}",
            kind == "ret" and got == ["schema node <root> is not a mapping"],
            f"  expected the not-a-mapping problem, got ({kind!r}, {got!r})",
        )

    # --- Which layer can see what -----------------------------------------
    # R13 boundary 4. This is the fact that made the original measurement look
    # green: `schema()` refuses an unknown kind before `check_kinds()` runs, so
    # the CLI can only ever show the schema-of-schema message. Recording it as a
    # test keeps the claim checkable instead of asserting it in prose.
    #
    # Driven through a temp repo, not the working tree: a test that edits this
    # repository's own schema fails the run it is embedded in if it is killed
    # mid-way, and leaves the checkout dirty.
    def cli_with_schema(body: str) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            (root / "00-governance" / gate.SCHEMA_FILE.split("/")[-1]).write_text(
                body, encoding="utf-8"
            )
            (root / "00-governance" / "a.md").write_text(doc(BASE), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable,
                 str(Path(__file__).resolve().parent / "check_document_management.py"),
                 "--root", str(root)],
                capture_output=True, text=True,
            )
            return proc.returncode, (proc.stdout + proc.stderr)

    # A schema that keeps all four dimensions and the required leaves, so the
    # run reaches check_schema_keys instead of stopping at "no longer declares".
    mutated = (
        'schema_version: "2"\n'
        "fields:\n"
        "  domain:\n    kind: NOT_A_KIND\n    required: true\n"
        "  role:\n    kind: string\n    required: true\n"
        "  lifecycle:\n    kind: mapping\n    required: true\n"
        "    fields:\n"
        "      approval:\n        kind: mapping\n"
        "        fields:\n"
        "          decision_status:\n            kind: string\n"
        "  authority:\n    kind: mapping\n    required: true\n"
        "    fields:\n"
        "      canonical_status:\n        kind: string\n"
        "      normative_status:\n        kind: string\n"
    )
    code, output = cli_with_schema(mutated)
    record(
        "T93h the CLI refuses an unknown kind at the schema layer",
        code == 1
        and f"{gate.SCHEMA_FILE}: schema field domain declares unknown kind 'NOT_A_KIND'"
        in output,
        f"  exit {code}, output {output[-400:]!r}",
    )
    # Stated, not implied: check_kinds' own diagnostic cannot appear here,
    # because the schema-of-schema check runs first and raises SystemExit.
    record(
        "T93h the CLI never reaches check_kinds' unknown-kind branch",
        "declares unknown kind 'NOT_A_KIND'" in output
        and "DM-01 domain must be NOT_A_KIND" not in output,
        f"  output {output[-400:]!r}",
    )
    record(
        "T93h the CLI refusal is a message, not a traceback",
        "Traceback (most recent call last)" not in output,
        f"  output {output[-400:]!r}",
    )

    # The direct-call diagnostic from T93e is what a library caller sees for the
    # same malformed spec. Both are recorded so the difference is a test result
    # rather than a claim in a report.
    errors = []
    kind, got = call(
        gate.check_kinds, {"domain": "architecture"},
        {"fields": {"domain": {"kind": "NOT_A_KIND"}}}, errors
    )
    record(
        "T93h the direct-call layer reports the same defect against the schema",
        kind == "ret"
        and errors == ["DM-01 schema field domain declares unknown kind 'NOT_A_KIND'"],
        f"  got ({kind!r}, {got!r}, errors={errors})",
    )
    record(
        "T93h the two layers disagree on where the defect is reported",
        "declares unknown kind 'NOT_A_KIND'" in output
        and any("declares unknown kind" in e for e in errors)
        and not any("must be NOT_A_KIND" in e for e in errors),
        f"  cli {output[-200:]!r}, direct {errors}",
    )
def run_fault_injection() -> None:
    """T92a-T92d: the gate's own error paths, reached by controlled injection.

    These cases are **not** evidence that any of these failures happens
    naturally in CI, and nothing here fabricates such a claim. Each case
    patches exactly one seam for the duration of one call, delegates every
    other input to the original implementation, and restores the attribute in
    a `finally`.

    Each case also asserts that the inputs it did *not* target still reached
    the real implementation. A patch that swallowed every call would produce
    the same diagnostic while proving nothing about the branch under test --
    which is the failure mode these assertions exist to catch.
    """
    print("fault injection (T92a-T92d, controlled)")

    import check_document_management as gate

    def posix(path) -> str:
        return Path(str(path)).as_posix()

    def git_fixture(tmp: str) -> tuple[Path, str]:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        (root / "00-governance" / "seed.md").write_text(doc(BASE), encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed")
        return root, _git(root, "rev-parse", "HEAD")

    def capture(root: Path, *extra: str) -> tuple[int, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = run_gate(root, *extra)
        return code, out.getvalue() + err.getvalue()

    def _summary_counts(line: str) -> tuple[int, int]:
        """(governed, classified) parsed from the gate's own count line."""
        m = re.search(
            r"GOV-DOC-002: (\d+) governed documents, (\d+) classified", line
        )
        assert m, f"count line not understood: {line!r}"
        return int(m.group(1)), int(m.group(2))

    # T92a: `git()` cannot start the process at all. The caller must refuse
    # with its own diagnostic rather than let the OSError escape as a
    # traceback, and the seam must not swallow git commands it does not target.
    with tempfile.TemporaryDirectory() as tmp:
        root, base = git_fixture(tmp)
        real_run = gate.subprocess.run

        def failing_run(args, *a, **k):
            if args[:1] == ["git"] and "rev-parse" in args:
                raise FileNotFoundError(2, "No such file or directory", "git")
            return real_run(args, *a, **k)

        gate.subprocess.run = failing_run
        try:
            delegated = gate.git(root, "log", "-1", "--format=%H")
            code, text = capture(root, "--require-changed", base)
        finally:
            gate.subprocess.run = real_run

        prefix = "ERROR: incremental changed-path selection failed:"
        refused = [
            line for line in text.splitlines() if line.strip().startswith(prefix)
        ]
        record(
            "T92a git() spawn failure is refused by the caller, not raised",
            code == 1
            and len(refused) == 1
            and "does not resolve to a commit" in refused[0]
            and "Traceback" not in text,
            f"  exit {code}, matching lines {refused}, output {text!r}",
        )
        record(
            "T92a the seam delegates git commands it does not target",
            isinstance(delegated, str) and len(delegated) == 40
            and all(c in "0123456789abcdef" for c in delegated),
            f"  `git log -1 --format=%H` returned {delegated!r} while patched",
        )
        record(
            "T92a subprocess.run is restored after the case",
            gate.subprocess.run is real_run,
            "  the patch outlived its case",
        )

    # T92b: one governed path cannot be resolved while the set is built. It
    # must leave a DM-01 problem AND stay out of the target list -- both sides,
    # because either alone is satisfiable by a wrong implementation.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        victim = root / "00-governance" / "a.md"
        victim.write_text(doc(BASE), encoding="utf-8")

        baseline, _ = gate.collect_governed(root)
        real_resolve = Path.resolve
        targeted: list[str] = []

        def failing_resolve(self, *a, **k):
            if posix(self).endswith("00-governance/a.md"):
                targeted.append(posix(self))
                raise OSError(2, "No such file or directory")
            return real_resolve(self, *a, **k)

        Path.resolve = failing_resolve
        try:
            targets, problems = gate.collect_governed(root)
        finally:
            Path.resolve = real_resolve

        unresolved = [p for p in problems if p.startswith("DM-01 cannot resolve ")]
        survivors = [posix(t) for t in targets]
        record(
            "T92b an unresolvable governed path is reported, not silently dropped",
            len(unresolved) == 1
            and "00-governance/a.md" in posix(unresolved[0])
            and "No such file or directory" in unresolved[0],
            f"  problems {problems}",
        )
        record(
            "T92b the unresolvable path does not enter the target list",
            not any(s.endswith("00-governance/a.md") for s in survivors)
            and len(targets) == len(baseline) - 1,
            f"  {len(baseline)} before, {len(targets)} after: {survivors}",
        )
        expected = [
            posix(b) for b in baseline if not posix(b).endswith("00-governance/a.md")
        ]
        record(
            "T92b the other targets survive the failure, in the same order",
            survivors == expected and len(expected) >= 1,
            f"  expected {expected}, survivors {survivors}",
        )
        record(
            "T92b the injection intercepted exactly one path",
            len(targeted) == 1,
            f"  intercepted {targeted}",
        )
        record(
            "T92b Path.resolve is restored after the case",
            Path.resolve is real_resolve,
            "  the patch outlived its case",
        )

    # T92c: untracked enumeration fails. The two diff calls must still be
    # delegated, or the test would be pinning the diff-failure branch instead.
    with tempfile.TemporaryDirectory() as tmp:
        root, base = git_fixture(tmp)
        real_git = gate.git
        seen: list[list[str]] = []

        def failing_git(r, *args, **k):
            seen.append(list(args))
            if args[:1] == ("ls-files",):
                return None
            return real_git(r, *args, **k)

        gate.git = failing_git
        try:
            try:
                gate.changed_paths(root, base)
                raised = ""
            except ValueError as exc:
                raised = str(exc)
            direct_calls = list(seen)
            code, text = capture(root, "--require-changed", base)
        finally:
            gate.git = real_git

        record(
            "T92c untracked enumeration failure raises the untracked diagnostic",
            raised == "cannot enumerate untracked paths",
            f"  raised {raised!r}",
        )
        record(
            "T92c the failure is not the diff diagnostic",
            "refusing a semantically different diff" not in raised
            and len([c for c in direct_calls if c[:1] == ["diff"]]) == 2
            and [c[:1] for c in direct_calls]
                == [["rev-parse"], ["diff"], ["diff"], ["ls-files"]],
            f"  direct calls {direct_calls}",
        )
        record(
            "T92c the public path turns it into a selection error, not a traceback",
            code == 1
            and "ERROR: incremental changed-path selection failed: "
                "cannot enumerate untracked paths" in text
            and "Traceback" not in text,
            f"  exit {code}, output {text!r}",
        )
        record(
            "T92c git is restored after the case",
            gate.git is real_git,
            "  the patch outlived its case",
        )

    # T92d: one target stops being a regular file between collection and use.
    # The narrow condition is the whole point: every other path must reach the
    # real `Path.is_file()`, and `collect_governed()` must be unaffected.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        victim = root / "00-governance" / "a.md"
        later = root / "00-governance" / "z.md"
        victim.write_text(doc(BASE), encoding="utf-8")
        later.write_text(doc(BASE), encoding="utf-8")

        collected, _ = gate.collect_governed(root)
        base_code, base_text = capture(root)
        base_summary = next(
            line for line in base_text.splitlines() if line.startswith("GOV-DOC-002:")
        )
        real_is_file = Path.is_file
        intercepted: list[str] = []

        def failing_is_file(self, *a, **k):
            intercepted.append(posix(self))
            if posix(self).endswith("00-governance/a.md"):
                return False
            return real_is_file(self, *a, **k)

        Path.is_file = failing_is_file
        try:
            code, text = capture(root)
            after, _ = gate.collect_governed(root)
        finally:
            Path.is_file = real_is_file

        not_a_file = [
            line.strip() for line in text.splitlines() if "DM-01 not a file:" in line
        ]
        accounting = [
            line.strip() for line in text.splitlines()
            if "DM-01 accounting:" in line
        ]
        summary = next(
            line for line in text.splitlines() if line.startswith("GOV-DOC-002:")
        )
        record(
            "T92d a target that is no longer a regular file is reported by path",
            code == 1
            and len(not_a_file) == 1
            and "00-governance/a.md" in posix(not_a_file[0])
            and "Traceback" not in text,
            f"  exit {code}, lines {not_a_file}, output {text!r}",
        )
        # The refusal must not shrink the denominator: the accounting identity
        # still counts the hidden file as governed, so the run cannot report a
        # smaller, cleaner tree after one target was refused.
        record(
            "T92d the refusal does not shrink the governed count",
            len(accounting) == 1
            and "3 classified + 0 unclassified != 4 governed" in accounting[0],
            f"  accounting {accounting}",
        )
        base_total, base_classified = _summary_counts(base_summary)
        patched_total, patched_classified = _summary_counts(summary)
        record(
            "T92d the remaining targets are still processed after the refusal",
            base_code == 0
            and patched_total == base_total
            and patched_classified == base_classified - 1,
            f"  baseline exit {base_code} {base_summary!r}, patched {summary!r}",
        )
        record(
            "T92d collect_governed() is unchanged by the injection",
            [posix(p) for p in after] == [posix(p) for p in collected],
            f"  {len(collected)} before, {len(after)} after",
        )
        record(
            "T92d every other path reaches the real Path.is_file()",
            len([p for p in intercepted if p.endswith("00-governance/a.md")]) == 1
            and any(p.endswith("00-governance/z.md") for p in intercepted),
            f"  intercepted {intercepted}",
        )
        record(
            "T92d Path.is_file is restored after the case",
            Path.is_file is real_is_file,
            "  the patch outlived its case",
        )


# --------------------------------------------------------------------------
# 5z. Bind the gate's reachable unbound emissions (issue #827)
#
# Issue #827 asked one question per error message: if this statement were
# deleted, would any test turn red? A mechanical audit at `origin/main`
# dc826e4e extracted all 99 message literals the gate can emit, replaced each
# emission with `None` in an isolated tree, and ran this suite. 38 came back
# UNBOUND -- the suite stayed green with the statement gone.
#
# Every case below builds the input that makes one of those 38 speak and
# asserts on that message specifically. The pattern is the emission's own
# literal with each `{}` turned into `.+`, so deleting the statement makes the
# case fail *and names the sentence it bound*.
#
# One of the 38 is deliberately not bound, and is not tested here:
# `DM-01 outside the repository root`. Every target reaching that branch comes
# from `collect_governed()`, which yields paths rooted at `root`, and
# `main()` resolves `--root` before scanning; `scan_root()` skips symlinks
# rather than following them. No document, registry or directory layout can
# make `path.relative_to(root)` fail. It is a defensive branch, left in place
# (issue #827 says not to delete dead code in this change) and recorded as
# unreachable in the work item rather than bound by a fabricated test.
# --------------------------------------------------------------------------

def _bind(name: str, emitted: list[str], pattern: str) -> None:
    """Record one case: `pattern` must match an emitted message.

    Matching allows the `<rel>: ` prefix the gate puts on per-document
    errors, so a pattern can be written exactly as the statement spells it.
    """
    try:
        for line in emitted:
            if re.search(r"(?:^|: )" + pattern + r"$", line.strip()):
                record(name, True)
                return
        raise AssertionError(
            f"no emitted message matched {pattern!r}; emitted {emitted!r}"
        )
    except AssertionError as exc:
        record(name, False, f"  AssertionError: {exc}")


def _gate_lines(root: Path, *extra: str) -> list[str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        run_gate(root, *extra)
    return (out.getvalue() + err.getvalue()).splitlines()


def _write_registry(root: Path, body: str) -> None:
    (root / "00-governance" / "document-scope-registry.yaml").write_text(
        'registry_version: "2"\n' + body, encoding="utf-8"
    )


def _revoked(**fields) -> str:
    """BASE with a Revoked decision and exactly the revocation fields given."""
    block = "".join(f"        {key}: {value}\n" for key, value in fields.items())
    return BASE.replace(
        "      decision_status: Draft",
        "      decision_status: Revoked\n      revocation:\n" + block,
    )


def _resolution(omit: str = "", selected: str = "00-governance/a.md") -> str:
    """BASE carrying a Resolved conflict and a resolution block."""
    fields = {
        "resolution_decision_id": '"GOV-CONF-001"',
        "resolved_date": '"2026-11-20"',
        "selected_document": f'"{selected}"',
    }
    fields.pop(omit, None)
    block = "".join(f"      {key}: {value}\n" for key, value in fields.items())
    return BASE.replace(
        "canonical_conflict_status: None",
        "canonical_conflict_status: Resolved\n"
        "    canonical_conflict_resolution:\n" + block,
    )


def run_unbound_emissions() -> None:
    print("unbound emissions (issue #827)")

    # --- document-level: one fixture per message -------------------------

    def doc_bind(name: str, text: str, pattern: str) -> None:
        errors, _ = check_document(FILE, text)
        _bind(name, errors, pattern)

    doc_bind(
        "T94 DM-04 Revoked without revocation_decision_id is named",
        doc(_revoked(revoked_date='"2026-01-01"', revocation_reason='"withdrawn"')),
        r"DM\-04 Revoked requires revocation\.revocation_decision_id",
    )
    doc_bind(
        "T95 DM-04 Revoked without revoked_date is named",
        doc(_revoked(
            revocation_decision_id='"GOV-REV-001"', revocation_reason='"withdrawn"')),
        r"DM\-04 Revoked requires revocation\.revoked_date",
    )
    doc_bind(
        "T96 DM-04 Revoked without revocation_reason is named",
        doc(_revoked(
            revocation_decision_id='"GOV-REV-001"', revoked_date='"2026-01-01"')),
        r"DM\-04 Revoked requires revocation\.revocation_reason",
    )
    doc_bind(
        "T97 DM-06 a blank keyword entry is named",
        doc(CANONICAL.replace("      - entity", '      - ""')),
        r"DM\-06 canonical_scope_keywords entries must be non\-empty strings",
    )
    for omit, rule in (
        ("resolution_decision_id", "resolution_decision_id"),
        ("resolved_date", "resolved_date"),
        ("selected_document", "selected_document"),
    ):
        doc_bind(
            f"T98 DM-11 a resolution without {rule} is named",
            doc(_resolution(omit=omit)),
            rf"DM\-11 resolution requires {rule}",
        )

    # --- repository-level ------------------------------------------------

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "bad.md").write_bytes(
            b"---\ndocument_metadata:\n  domain: \xff\xfe\n---\n"
        )
        _bind(
            "T99 DM-01 a non-UTF-8 governed file is reported by path",
            _gate_lines(root),
            r"DM\-01 not valid UTF\-8: .+",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "a.md").write_text(
            doc(BASE + "\n  bilingual_counterpart:\n    en:\n      - docs/en/x.md"),
            encoding="utf-8",
        )
        _bind(
            "T100 DM-01 a non-string counterpart path is named",
            _gate_lines(root),
            r"DM\-01 .+ bilingual_counterpart\.en must be a string path, got list",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        for name in ("a.md", "b.md"):
            (root / "00-governance" / name).write_text(
                doc(_revoked(
                    revocation_decision_id='"GOV-REV-001"',
                    revoked_date='"2026-01-01"',
                    revocation_reason='"withdrawn"')),
                encoding="utf-8",
            )
        _bind(
            "T101 DM-04 a reused revocation_decision_id is reported",
            _gate_lines(root),
            r"DM\-04 revocation_decision_id .+ reused by .+ and .+",
        )

    # DM-10: a file pinned to a commit that predates it. The commit exists, so
    # the pin resolves; the file is absent from it, so the approval cannot be
    # bound. Both halves matter, and only the second is this message.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed without late.md")
        early = _git(root, "rev-parse", "HEAD")
        (root / "00-governance" / "late.md").write_text(
            doc(APPROVED.replace('"deadbeef"', f'"{early}"')), encoding="utf-8"
        )
        _bind(
            "T102 DM-10 an approval pinned before the file existed is named",
            _gate_lines(root),
            r"DM\-10 .+ did not exist at approved_version .+; the approval "
            r"cannot be bound to that version",
        )

    # DM-11 cross-document: a resolution naming a file that does not declare
    # the scope, and one naming a file that is not the unique Canonical.
    scope_body = BASE.replace("    canonical_conflict_status: None\n", "").replace(
        "canonical_status: Non-Canonical",
        'canonical_status: Candidate\n'
        '    canonical_scope_id: "architecture/dup"\n'
        + "    canonical_conflict_status: Resolved\n"
        "    canonical_conflict_resolution:\n"
        '      resolution_decision_id: "GOV-CONF-001"\n'
        '      resolved_date: "2026-11-20"\n'
        '      selected_document: "SEL"\n',
    )
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "a.md").write_text(
            doc(scope_body.replace("SEL", "00-governance/b.md")), encoding="utf-8")
        (root / "00-governance" / "b.md").write_text(doc(BASE), encoding="utf-8")
        _bind(
            "T103 DM-11 a resolution selecting a non-member of the scope is named",
            _gate_lines(root),
            r"DM\-11 scope .+ resolution selects .+, which does not declare "
            r"this scope",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        for name in ("a.md", "b.md"):
            (root / "00-governance" / name).write_text(
                doc(scope_body.replace("SEL", "00-governance/b.md")),
                encoding="utf-8",
            )
        _bind(
            "T104 DM-11 a resolution selecting a non-Canonical document is named",
            _gate_lines(root),
            r"DM\-11 scope .+ resolution selects .+, which is not the unique "
            r"Canonical document \(.+\)",
        )

    # DM-12 mirror links. Each case below isolates one link defect; the
    # surrounding group is otherwise well formed, so no neighbouring DM-12
    # diagnostic can satisfy the case.
    def mirror(extra: str) -> str:
        return BASE + "\n  bilingual_counterpart:\n" + extra

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "a.md").write_text(
            doc(mirror('    en: "docs/en/nope.md"')), encoding="utf-8")
        _bind(
            "T105 DM-12 a counterpart that does not exist is named",
            _gate_lines(root),
            r"DM\-12 .+: bilingual_counterpart\.en does not exist: .+",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "a.md").write_text(doc(BASE), encoding="utf-8")
        (root / "00-governance" / "b.md").write_text(
            doc(mirror('    en: "00-governance/a.md"')), encoding="utf-8")
        _bind(
            "T106 DM-12 a counterpart outside the mirror root is named",
            _gate_lines(root),
            r"DM\-12 .+: bilingual_counterpart\.en must point under "
            r"docs/en/, got .+",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "a.md").write_text(
            doc(mirror('    en: "00-governance/a.md"')), encoding="utf-8")
        _bind(
            "T107 DM-12 a counterpart pointing at itself is named",
            _gate_lines(root),
            r"DM\-12 .+: bilingual_counterpart\.en points to itself",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "docs" / "en").mkdir(parents=True, exist_ok=True)
        (root / "docs" / "zh-CN").mkdir(parents=True, exist_ok=True)
        (root / "00-governance" / "a.md").write_text(
            doc(CANONICAL + '\n  bilingual_counterpart:\n    en: "docs/en/a.md"\n'),
            encoding="utf-8")
        (root / "docs" / "en" / "a.md").write_text(
            doc(CANONICAL + '\n  bilingual_counterpart:\n'
                            '    source: "00-governance/a.md"\n'),
            encoding="utf-8")
        _bind(
            "T108 DM-12 two Canonical claims in one group are named",
            _gate_lines(root),
            r"DM\-12 .+: both a document and its mirror claim Canonical \(.+\)",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "docs" / "en").mkdir(parents=True, exist_ok=True)
        (root / "docs" / "zh-CN").mkdir(parents=True, exist_ok=True)
        (root / "docs" / "en" / "a.md").write_text(
            doc(mirror('    source: "docs/en/b.md"')), encoding="utf-8")
        _bind(
            "T109 DM-12 a mirror naming a mirror as its source is named",
            _gate_lines(root),
            r"DM\-12 .+: source must be the authoritative file, not a mirror "
            r"\(.+\)",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "docs" / "en").mkdir(parents=True, exist_ok=True)
        (root / "docs" / "zh-CN").mkdir(parents=True, exist_ok=True)
        (root / "00-governance" / "a.md").write_text(
            doc(mirror('    en: "docs/en/a.md"')), encoding="utf-8")
        (root / "docs" / "en" / "a.md").write_text(
            doc(BASE.replace("  role: design-specification", "  role: reference")
                + '\n  bilingual_counterpart:\n    source: "00-governance/a.md"\n'),
            encoding="utf-8")
        _bind(
            "T110 DM-12 a field disagreeing across a group is named",
            _gate_lines(root),
            r"DM\-12 .+: role .+ disagrees with .+ \(.+\)",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "00-governance" / "a.md").write_text(
            doc(BASE), encoding="utf-8")
        (root / "00-governance" / "b.md").write_text(
            doc(BASE.replace(
                "    approval:\n      decision_status: Draft",
                '    bilingual_counterpart:\n      en: "docs/en/b.md"\n'
                "    approval:\n      decision_status: Draft")), encoding="utf-8")
        (root / "docs" / "en").mkdir(parents=True, exist_ok=True)
        (root / "docs" / "zh-CN").mkdir(parents=True, exist_ok=True)
        (root / "docs" / "en" / "b.md").write_text(
            doc(mirror('    source: "00-governance/b.md"')), encoding="utf-8")
        (root / "docs" / "en" / "a.md").write_text(
            doc(mirror('    source: "00-governance/a.md"\n    zh-CN: "docs/en/b.md"')),
            encoding="utf-8")
        _bind(
            "T111 DM-12 a link to a third party's mirror is named",
            _gate_lines(root),
            r"DM\-12 .+ -> .+: neither its source \(.+\) nor a sibling mirror "
            r"of it \(.+\)",
        )

    for label, body, pattern in (
        (
            "T112 DM-13 a document superseding itself is named",
            "    supersession:\n      supersedes:\n        - 00-governance/a.md\n",
            r"DM\-13 .+: a document cannot supersede itself",
        ),
        (
            "T113 DM-13 a non-list supersedes is named",
            "    supersession:\n      supersedes: 00-governance/a.md\n",
            r"DM\-13 .+: supersedes must be a list",
        ),
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            (root / "00-governance" / "a.md").write_text(
                doc(BASE.replace(
                    "    approval:\n      decision_status: Draft",
                    body + "    approval:\n      decision_status: Draft")),
                encoding="utf-8")
            _bind(label, _gate_lines(root), pattern)

    # DM-14 registry shape. Each fixture carries the offending key alone, so
    # the shape error is the only one the case can be satisfied by.
    for label, body, pattern in (
        (
            "T114 DM-14 a backlog entry that is not a mapping is named",
            'governed:\n  - 00-governance\nbacklog:\n  docs: 1\n',
            r"DM\-14 backlog 'docs' must be a mapping with a count",
        ),
        (
            "T115 DM-14 a backlog entry with no reason is named",
            "governed:\n  - 00-governance\nbacklog:\n  docs:\n    documents: 1\n"
            '    reason_zh: "\u5c1a\u672a\u5206\u7c7b"\n',
            r"DM\-14 backlog 'docs' has no reason",
        ),
        (
            "T116 DM-14 a backlog entry with no reason_zh is named",
            "governed:\n  - 00-governance\nbacklog:\n  docs:\n    documents: 1\n"
            '    reason: "not classified yet"\n',
            r"DM\-14 backlog 'docs' has no reason_zh \(GOV\-DOC\-001\)",
        ),
        (
            "T117 DM-14 an excluded entry that is not a mapping is named",
            'governed:\n  - 00-governance\nexcluded:\n  tools: 1\n',
            r"DM\-14 excluded 'tools' must be a mapping with a reason",
        ),
        (
            "T118 DM-14 an excluded entry with no reason_zh is named",
            "governed:\n  - 00-governance\nexcluded:\n  tools:\n"
            '    kind: not-documentation\n    reason: "not documentation"\n',
            r"DM\-14 excluded 'tools' has no reason_zh \(GOV\-DOC\-001\)",
        ),
        (
            "T119 DM-14 an excluded entry with an unknown kind is named",
            "governed:\n  - 00-governance\nexcluded:\n  tools:\n"
            '    kind: whatever\n    reason: "not documentation"\n'
            '    reason_zh: "\u975e\u6587\u6863"\n',
            r"DM\-14 excluded 'tools' must declare kind one of .+, got 'whatever'",
        ),
        (
            "T120 DM-14 a backlog that is not a mapping is named",
            "governed:\n  - 00-governance\nbacklog: 5\n",
            r"DM\-14 .+ backlog must be a mapping",
        ),
        (
            "T121 DM-14 an excluded that is not a mapping is named",
            "governed:\n  - 00-governance\nexcluded: 5\n",
            r"DM\-14 .+ excluded must be a mapping",
        ),
        (
            "T122 DM-14 a governed_files that is not a sequence is named",
            "governed:\n  - 00-governance\ngoverned_files: 5\n",
            r"DM\-14 .+ governed_files must be a sequence",
        ),
        (
            "T123 DM-14 an empty governed list is named",
            "governed:\n",
            r"DM\-14 .+ must declare a non\-empty governed list",
        ),
        (
            "T124 DM-14 a governed root also declared backlog is named",
            'governed:\n  - 00-governance\nbacklog:\n  "00-governance":\n'
            "    documents: 1\n"
            '    reason: "x"\n    reason_zh: "y"\n',
            r"DM\-14 \['00\-governance'\] are both governed and backlog; pick one",
        ),
        (
            "T125 DM-14 a governed root also excluded is named",
            'governed:\n  - 00-governance\nexcluded:\n  "00-governance":\n'
            '    kind: not-documentation\n    reason: "x"\n    reason_zh: "y"\n',
            r"DM\-14 \['00\-governance'\] are both governed\-or\-backlog and "
            r"excluded",
        ),
        (
            "T126 DM-14 a registry disagreeing with NORMATIVE_ROOTS is named",
            "governed:\n  - 00-governance\n",
            r"DM\-14 scope registry and NORMATIVE_ROOTS disagree; "
            r"declared\-only .+, enforced\-only .+",
        ),
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = _repo(tmp)
            _write_registry(root, body)
            _bind(label, _gate_lines(root), pattern)

    # A governed file whose top-level directory is accounted for by nothing.
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        (root / "15-orphan").mkdir()
        (root / "15-orphan" / "x.md").write_text(doc(BASE), encoding="utf-8")
        import check_document_management as gate
        original = gate.GOVERNED_FILES
        gate.GOVERNED_FILES = ("15-orphan/x.md",)
        try:
            emitted = gate.check_scope_registry(root)
        finally:
            gate.GOVERNED_FILES = original
        _bind(
            "T127 DM-14 a governed file in an unaccounted directory is named",
            emitted,
            r"DM\-14 governed file 15\-orphan/x\.md sits in 15\-orphan, which is "
            r"neither governed, backlog nor excluded: declare the directory's "
            r"status first",
        )

    # A symlinked mirror. The registry would otherwise assert that docs/en
    # exists while the scanner refuses to descend into it.
    with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside:
        root = _repo(tmp)
        Path(outside, "a.md").write_text(doc(BASE), encoding="utf-8")
        target = root / "docs" / "en"
        shutil.rmtree(target)
        try:
            target.symlink_to(Path(outside), target_is_directory=True)
        except (OSError, NotImplementedError):
            record(
                "T128 DM-14 a symlinked mirror directory is named", False,
                "  symlinks unavailable on this platform; the case could not run",
            )
        else:
            _bind(
                "T128 DM-14 a symlinked mirror directory is named",
                _gate_lines(root),
                r"DM\-14 bilingual mirror directory docs/en is a symbolic link; "
                r"a mirror must be real content of this repository",
            )



def run_steward_assignment() -> None:
    """DM-15: newly added governed documents need a steward; legacy files remain
    an adoption baseline and are not retroactively blocked.
    """
    print("steward assignment")
    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed")
        base = _git(root, "rev-parse", "HEAD")
        missing = root / "00-governance" / "new-without-steward.md"
        missing.write_text(doc(BASE), encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "add document without steward")
        expect_gate(
            "DM-15 new document without steward fails",
            root, 1, "--require-changed", base,
            msg="00-governance/new-without-steward.md: DM-15",
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed")
        base = _git(root, "rev-parse", "HEAD")
        valid = root / "00-governance" / "new-with-steward.md"
        valid.write_text(
            doc('  steward: "Architecture Governance"\n' + BASE.strip("\n")),
            encoding="utf-8",
        )
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "add document with steward")
        expect_gate(
            "DM-15 new document with steward passes",
            root, 0, "--require-changed", base,
        )

    with tempfile.TemporaryDirectory() as tmp:
        root = _repo(tmp)
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "gate@example.invalid")
        _git(root, "config", "user.name", "gate")
        legacy = root / "00-governance" / "legacy.md"
        legacy.write_text(doc(BASE), encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "seed legacy")
        base = _git(root, "rev-parse", "HEAD")
        legacy.write_text(doc(BASE + "\n# revised prose"), encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "modify legacy")
        expect_gate(
            "DM-15 legacy document modification remains non-blocking",
            root, 0, "--require-changed", base,
        )



def run_m02_optional_approval_identity_fields() -> None:
    """M-02: The gate validates `decision_status`; for `Approved` it requires
    `approved_version`, `approval_scope` and `approval_applicability`, and DM-10
    binds the body hash to `approved_version`. It does not require `approver` or
    `decision_date` to be present, and does not verify that any approval exists.

    This feature test pins the negative boundary: optional identity/date fields
    may be absent without turning a structurally valid Draft document into an
    error. It does not assert that a policy-required approval has occurred.
    """
    with_fields = BASE.replace(
        "decision_status: Draft",
        'decision_status: Draft\n      approver: "reviewer@example.invalid"\n'
        '      decision_date: "2026-11-27"',
    )
    without_fields = with_fields.replace(
        '      approver: "reviewer@example.invalid"\n', ""
    ).replace('      decision_date: "2026-11-27"\n', "")
    errors, _ = check_document(FILE, doc(without_fields))
    record(
        "M-02 does not require approver or decision_date",
        not errors,
        f"  unexpected: {errors}",
    )


def run_security_readme_canonical_status() -> None:
    """The security-governance guide must describe the five files by their
    authoritative `canonical_status: Canonical` frontmatter, not Candidate.

    The README is navigation, not the normative source; Informative/Draft and
    the non-approval/non-conformance disclaimer remain explicit.
    """
    root = Path(__file__).resolve().parents[1]
    names = (
        "global-forget-target-inventory-and-completion-evidence.md",
        "forget-retention-backup-and-erasure-policy.md",
        "principal-actor-and-authorization-contract.md",
        "scope-and-revocation-policy.md",
        "security-and-identity-overview.md",
    )
    readme_paths = (
        root / "09-security-governance" / "README.md",
        root / "docs/en/09-security-governance/README.md",
        root / "docs/zh-CN/09-security-governance/README.md",
    )
    readmes = [path.read_text(encoding="utf-8") for path in readme_paths]
    readme = readmes[0]
    obsolete = ("remain **Candidate / Informative**", "remain Candidate / Informative",
                "五份文档均保持 Candidate / Informative")
    declaration = (
        "Each of the five documents declares `canonical_status: Canonical` in its own frontmatter. "
        "That field is authoritative; this README is a guide, not a normative source."
    )
    disclaimers = (
        "does not ratify Phase 3.x decisions",
        "establish implementation/conformance evidence",
    )
    statuses_ok = True
    details: list[str] = []
    for name in names:
        path = root / "09-security-governance" / name
        metadata = read_metadata(path.read_text(encoding="utf-8"))
        authority = (metadata or {}).get("authority", {})
        approval = (metadata or {}).get("lifecycle", {}).get("approval", {})
        if (authority.get("canonical_status") != "Canonical"
                or authority.get("normative_status") != "Informative"
                or approval.get("decision_status") != "Draft"
                or approval.get("approved_version") is not None):
            statuses_ok = False
            details.append(name)
    ok = (
        all(not phrase in text for text in readmes for phrase in obsolete)
        and declaration in readme
        and all(item in readme for item in disclaimers)
        and statuses_ok
    )
    record(
        "09-security-governance README matches five Canonical frontmatters",
        ok,
        f"  stale wording/status mismatch: {details}; declaration/disclaimer missing",
    )


def main() -> int:
    print("check_document_management self-check")
    run_parser()
    run_fields()
    run_resolver()
    run_repository_rules()
    run_approval_binding()
    run_git_decode_locale()
    run_approval_scope()
    run_scope_key_removal()
    run_dm10_scope()
    run_prose_status_census()
    run_shallow_history()
    run_changed_paths()
    run_path_safety()
    run_body_hash_equivalence()
    run_bilingual_closure()
    run_scope_registry()
    run_kind_contract()
    run_restored_guards()
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
    run_m02_optional_approval_identity_fields()
    run_steward_assignment()
    run_security_readme_canonical_status()
    run_count_vocabulary()
    run_skip_boundary()
    run_policy_assertions()
    run_single_entry_callers()
    run_fault_injection()
    run_unbound_emissions()
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
