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
      last_verification_note: "Validation output is transcribed from operator-supplied execution results; PR and commit pins remain pending."
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
    canonical_scope: "Implementation and validation evidence for AID-2026-349."
    canonical_scope_id: "ai-development/aid-2026-349-evidence"
    canonical_scope_keywords:
      - "AID-2026-349"
      - "fail-closed"
      - "bilingual document group"
      - "DM-12"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Evidence — AID-2026-349

## 1. Work-item identity and baseline

- Work Item: `AID-2026-349`
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Base branch: `main`
- Base commit: `f0843a8f3`
- Implementation branch: `fix/2026-11-28-aid349-ac3-failclosed-fixtures`
- Related issue: `#1237`
- Class: `GOV/CI`
- Risk: `R2`

The work item uses AID-2026-349. The earlier planned identifier was unavailable because it is already occupied. The implementation change inventory supplied by the operator contains five repository files; the work-item's four records bring the manifest `scope.files_changed` total to nine.

## 2. Implementation record

### Shared validator

Added:

`scripts/gov_doc_fail_closed.py`

The module exposes:

```python
validate_group(root, registered_files) -> list[str]
```

It reuses the existing `check_document_management` functions:

- `read_metadata()`
- `check_document()`
- `check_scope_and_relations()`

The helper rejects symlinks and non-regular files, unreadable files, metadata parsing failures, missing `document_metadata`, and invalid metadata. It does not run the relationship graph when the registered group is incomplete. It converts only `DM-12 ` relationship errors to `FAIL_CLOSED:` diagnostics. It also provides `report_group()` to report diagnostics to stderr and return 0 or 1.

### Checker integration

Both checkers now use:

```python
def check(
    root: Path,
    *,
    require_group_closure: bool = False,
) -> tuple[int, list[str]]:
```

When `require_group_closure` is true, the checker adds the results of `validate_group(root, FILES)` to its errors.

The default is false to preserve existing content-only synthetic fixtures. Those fixtures have no document front matter and are intended to test the original checker-specific content rules. Requiring metadata by default would break that compatibility contract.

This does not weaken AC3 in CI: both production checker invocations explicitly pass `--require-group-closure`, and each CLI forwards that option to `check()`.

### CI integration

Updated the two checker commands in:

`.github/workflows/bilingual-docs.yml`

The commands now explicitly enable group closure:

```text
python3 scripts/check_owner_namespace_references.py --check --require-group-closure
python3 scripts/check_governance_operation_traceability.py --check --require-group-closure
```

### Fixture coverage

Added:

`tests/test_ac3_fail_closed_fixtures.py`

The eight reported test cases cover:

| # | Group | Fixture | Expected behavior |
|---:|---|---|---|
| 1 | Owner namespace | Complete registered group | Pass; no fail-closed diagnostic |
| 2 | Owner namespace | Missing registered member | Non-empty `FAIL_CLOSED:` diagnostic |
| 3 | Owner namespace | Unclassified member | Non-empty `FAIL_CLOSED:` diagnostic |
| 4 | Governance operation traceability | Complete registered group | Pass; no fail-closed diagnostic |
| 5 | Governance operation traceability | Missing registered member | Non-empty `FAIL_CLOSED:` diagnostic |
| 6 | Governance operation traceability | Unclassified member | Non-empty `FAIL_CLOSED:` diagnostic |
| 7 | Owner namespace | Unreadable member | Targeted `Path.read_text` patch raises `PermissionError`; non-empty `FAIL_CLOSED:` diagnostic |
| 8 | Owner namespace | Source/mirror mismatch | English `component-map.md` mirror points to existing but incorrect `01-system-architecture/system-boundaries.md`; non-empty `FAIL_CLOSED:` diagnostic |

The unreadable fixture uses `unittest.mock.patch`; it does not rely on `chmod` or host filesystem permission behavior.

The source/mirror mismatch fixture changes the mirror's `bilingual_counterpart.source` to a different source that exists in the copied fixture tree. This tests mutual relationship closure rather than simple missing-file detection.

The existing test files were not changed:

- `tests/test_check_owner_namespace_references.py`
- `tests/test_check_governance_operation_traceability.py`

## 3. Actual validation output supplied by the operator

The following command output is reproduced verbatim from the operator's report.

### Combined pytest suite

Command:

```powershell
python -m pytest -q tests/test_ac3_fail_closed_fixtures.py tests/test_check_owner_namespace_references.py tests/test_check_governance_operation_traceability.py
```

Output:

```text
....................................                                     [100%]
36 passed in 0.35s
```

Exit code: `0`

### Owner-namespace checker with group closure required

Command:

```powershell
python scripts/check_owner_namespace_references.py --check --require-group-closure
```

Output:

```text
OWNER NAMESPACE: PASS (15 registered documents scanned)
```

Exit code: `0`

### Governance-operation traceability checker with group closure required

Command:

```powershell
python scripts/check_governance_operation_traceability.py --check --require-group-closure
```

Output:

```text
GOVERNANCE OPERATION TRACEABILITY: PASS (7 operations x 3 mirrors)
```

Exit code: `0`

## 4. Final changed-file inventory

The operator reports exactly five repository implementation, test, and workflow files:

```text
.github/workflows/bilingual-docs.yml
scripts/gov_doc_fail_closed.py
scripts/check_owner_namespace_references.py
scripts/check_governance_operation_traceability.py
tests/test_ac3_fail_closed_fixtures.py
```

The four work-item records are:

```text
14-ai-development/work-items/AID-2026-349/manifest.yaml
14-ai-development/work-items/AID-2026-349/prompt-v1.md
14-ai-development/work-items/AID-2026-349/session-evidence.md
14-ai-development/work-items/AID-2026-349/evidence.md
```

Accordingly, `scope.files_changed` contains nine entries. The two existing checker test files are intentionally excluded because they were not modified.

## 5. Pending pins and delivery evidence

The following values must be filled from the committed branch and actual pull request before the work item is finalized:

- Prompt SHA-256 and byte count.
- Prompt file blob SHA and commit SHA.
- Executed-prompt SHA-256 and byte count, if independently captured.
- Implementation commit SHA.
- Pull request number and URL.
- Any required CI run identifiers or exact-head CI evidence.

Until those values are measured and recorded, the manifest retains `PIN_*` placeholders, `id_status: PROVISIONAL`, `status: DISPATCHED`, and `implementation.status: IN_PROGRESS`.

The AI session reference is recorded as:

`6b08ffa5-bccc-83ec-ae24-ea58c1d913b9`

Executed prompt provenance remains `NOT_VERIFIED`.

## 6. Acceptance status

The operator-reported tests and both checker runs pass with group closure explicitly enabled. The implementation and local validation evidence are therefore recorded as reported above.

The work item remains in progress pending committed-file pinning, pull request creation or confirmation, and any repository-required final CI and manifest-schema checks. No PR number, URL, commit SHA, or unobserved CI result is asserted here.
