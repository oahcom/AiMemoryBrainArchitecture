---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-349/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Prompt snapshot integrity pins are to be measured from the committed file."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Executed user instruction snapshot for AID-2026-349: add fail-closed validation of registered bilingual document groups and require it in CI."
    canonical_scope_id: "ai-development/aid-2026-349-prompt"
    canonical_scope_keywords:
      - "AID-2026-349"
      - "fail-closed"
      - "bilingual document group"
      - "DM-12"
      - "require_group_closure"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-349 — Fail-closed validation for bilingual document groups

## Authorization and execution boundary

Repository: `oahcom/AiMemoryBrainArchitecture`

Work Item: `AID-2026-349`

Issue: `#1237`

Base branch: `main`

Base commit: `f0843a8f3`

Implementation branch: `fix/2026-11-28-aid349-ac3-failclosed-fixtures`

Date: `2026-11-28`

Class: `GOV/CI`

Risk: `R2`

This work item adds fail-closed validation for the registered document groups checked by the owner-namespace and governance-operation traceability checkers. The authorized operator applies the changes, runs the commands, records their actual output, and prepares the pull request. AI-generated specifications and records do not independently establish repository state or command execution.

## Established design decisions

### 1. Shared validator

Add `scripts/gov_doc_fail_closed.py` with:

```python
validate_group(root, registered_files) -> list[str]
```

The helper must reuse the existing `check_document_management` implementation:

- `read_metadata()`
- `check_document()`
- `check_scope_and_relations()`

Do not introduce a separate YAML metadata parser or a parallel DM-12 relationship implementation.

The helper must reject symlinks and non-regular files, detect unreadable files and metadata parsing failures, require `document_metadata`, and reject invalid metadata. When the registered group is incomplete, it must not run the relationship graph. Only `DM-12 ` relationship errors from `check_scope_and_relations()` are elevated and wrapped as `FAIL_CLOSED:` diagnostics. The helper also provides `report_group()` to report diagnostics to stderr and return status 0 or 1.

### 2. Checker API and compatibility boundary

Both:

- `scripts/check_owner_namespace_references.py`
- `scripts/check_governance_operation_traceability.py`

must expose:

```python
def check(
    root: Path,
    *,
    require_group_closure: bool = False,
) -> tuple[int, list[str]]:
```

When `require_group_closure` is true, the checker extends its errors with:

```python
validate_group(root, FILES)
```

When false, the checker preserves its existing content-only behavior.

The default is deliberately `False` for compatibility with existing synthetic unit fixtures that contain only document bodies and do not include GOV-DOC-002 front matter. Those fixtures exercise the checkers' original content-specific behavior; requiring group metadata by default would conflate that behavior with a separate group-closure gate and break the established fixture contract.

This compatibility default does not weaken the production CI gate. Both CI invocations must explicitly pass `--require-group-closure`, and the CLI must pass that flag through to `check()`. Thus AC3 group closure is mandatory in CI while legacy direct calls and body-only tests remain compatible.

### 3. CLI and CI

Both checkers must expose a `--require-group-closure` `store_true` option.

The two steps in `.github/workflows/bilingual-docs.yml` must invoke:

```powershell
python3 scripts/check_owner_namespace_references.py --check --require-group-closure
python3 scripts/check_governance_operation_traceability.py --check --require-group-closure
```

The CI workflow must not rely on the default value of the Python API or omit the explicit flag. The production gate is the workflow invocation with group closure enabled.

### 4. Four fail-closed categories

Each negative fixture must assert that the returned diagnostics contain a non-empty entry beginning with `FAIL_CLOSED:`.

1. **Missing member:** a registered group member does not exist.
2. **Unreadable member:** reading a registered member fails, simulated with `unittest.mock.patch` so that `Path.read_text` raises `PermissionError` only for the selected target. Do not rely on `chmod` or host filesystem permission behavior.
3. **Unclassified or invalid metadata:** a member lacks `document_metadata`, or its metadata cannot be parsed or fails the existing document-management validation.
4. **Source/mirror mutual closure mismatch:** a mirror points to an existing but incorrect source document, so the registered source/mirror relationship does not close. The fixture changes the English `component-map.md` mirror's `bilingual_counterpart.source` to the different, existing `01-system-architecture/system-boundaries.md` source.

Positive fixtures must establish that complete valid owner-namespace and governance-operation groups produce no fail-closed diagnostics.

## Scope

Changed files:

- `.github/workflows/bilingual-docs.yml`
- `scripts/gov_doc_fail_closed.py`
- `scripts/check_owner_namespace_references.py`
- `scripts/check_governance_operation_traceability.py`
- `tests/test_ac3_fail_closed_fixtures.py`
- `14-ai-development/work-items/AID-2026-349/manifest.yaml`
- `14-ai-development/work-items/AID-2026-349/prompt-v1.md`
- `14-ai-development/work-items/AID-2026-349/session-evidence.md`
- `14-ai-development/work-items/AID-2026-349/evidence.md`

The existing test files `tests/test_check_owner_namespace_references.py` and `tests/test_check_governance_operation_traceability.py` are not changed. Their body-only fixtures remain valid through the default compatibility mode.

## Acceptance criteria

1. The shared helper reuses the existing document-management metadata and DM-12 validation functions.
2. Missing, unreadable, unclassified/invalid-metadata, and source/mirror closure failures produce non-empty `FAIL_CLOSED:` diagnostics.
3. An incomplete group does not proceed to relationship-graph validation.
4. Both checker APIs support the keyword-only `require_group_closure` argument with default `False`.
5. Both CLIs expose and forward `--require-group-closure`.
6. Both bilingual-docs CI checker invocations explicitly enable group closure.
7. The positive and negative fixtures pass on Windows PowerShell without depending on filesystem permission changes.
8. Existing content-only tests remain unchanged and pass.
9. No existing document's canonical authority or status is changed.

## Required validation

Run on the implementation branch from the repository root:

```powershell
python -m pytest -q tests/test_ac3_fail_closed_fixtures.py tests/test_check_owner_namespace_references.py tests/test_check_governance_operation_traceability.py
python scripts/check_owner_namespace_references.py --check --require-group-closure
python scripts/check_governance_operation_traceability.py --check --require-group-closure
```

Record the exact stdout and exit status for each command. Do not infer a pass from the intended implementation or from a different branch or commit.

## Provenance and completion

The implementing AI session reference is:

`6b08ffa5-bccc-83ec-ae24-ea58c1d913b9`

The session reference is recorded. Executed-prompt provenance remains `NOT_VERIFIED` until the exact executed prompt bytes and their SHA-256 are independently pinned.

The work item remains `DISPATCHED`, with `id_status: PROVISIONAL` and `implementation.status: IN_PROGRESS`, until the operator completes the repository's required identity, commit, pull-request, and evidence pinning process.
