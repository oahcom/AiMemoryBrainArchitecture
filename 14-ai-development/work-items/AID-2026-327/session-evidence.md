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
        - "14-ai-development/work-items/AID-2026-327/session-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Implementation proposal recorded. Runtime tests and full-tree verification have not been executed by this session."
    usage_status: Active
    modification_status: Original
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
    canonical_scope: "Implementation and verification record for AID-2026-327."
    canonical_scope_id: "ai-development/aid-2026-327-session-evidence"
    canonical_scope_keywords:
      - "AID-2026-327"
      - "issue-1463"
      - "manifest-blob-pins"
      - "prompt-sha256"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "USER-PRINCIPAL-DELEGATED"
---

# AID-2026-327 — Session Evidence

## 1. Work identity

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Issue: `#1463`
- Base branch: `main`
- Base commit: `efbdebfaa9fede98c9f2501e2fb941f344d0ca03`
- Work item: `AID-2026-327`
- Class: `GATE/TEST`
- Risk: `R1`

The assigned task is to repair the manifest prompt SHA-256
reader so that both top-level and nested prompt declarations are
actually checked against committed Git object bytes.

## 2. Session role

This session performed the implementation-design and source-authoring
role.

The task was to produce:

1. A complete replacement for
   `scripts/ci/check_manifest_blob_pins.py`.
2. A complete replacement for
   `scripts/ci/test_check_manifest_blob_pins.py`.
3. Six required regression cases.
4. Work-item metadata and this evidence record.
5. An INDEX registration row.
6. An operator execution sequence.

The implementation session identifier was not supplied by the
platform. No external session identity is claimed.

## 3. Established baseline facts

The supplied repository evidence establishes:

- There are 135 top-level work-item manifests.
- 68 declare top-level `prompt_sha256`.
- 3 use nested `prompt: {prompt_file, prompt_sha256}`.
- No manifest uses both forms.
- The existing checker reads the nested mapping but does not read
  the top-level digest field.
- Injecting an incorrect top-level digest into AID-2026-001 did not
  change the existing checker result.
- Injecting an incorrect nested digest into AID-2026-025 increased
  the mismatch count and produced a failure.
- Among 63 manifests with explicit prompt file and digest declarations,
  30 were consistent and 33 were inconsistent on the supplied
  origin/main measurement.
- The supplied evidence associates 32 stale declarations with the
  historical `44b57170^` prompt blob state.

These are supplied baseline facts, not new measurements performed
by this authoring session.

## 4. Normative implementation decisions

### 4.1 Top-level declaration

A top-level `prompt_sha256` pairs with:

1. The same manifest's top-level `prompt_file`, when that key exists.
2. Otherwise, the conventional
   `14-ai-development/work-items/<AID>/prompt-v1.md` path.

An explicitly declared missing file is a failure. The checker must
not silently replace it with the conventional fallback.

A missing conventional fallback is also a failure.

### 4.2 Nested declaration

The nested form continues to use:

- `prompt.prompt_file`
- `prompt.prompt_sha256`
- `prompt.prompt_bytes`

The nested SHA-256 and byte-count semantics remain independent.

### 4.3 Coverage

The checker tracks:

- Non-empty prompt SHA-256 declarations.
- Prompt SHA-256 declarations for which committed bytes were
  successfully retrieved and actually compared.

The two counts must be equal.

An unmatched declaration produces a `PROMPT_COVERAGE` failure
containing both counts.

### 4.4 Unknown fields

Unrecognized prompt digest spellings, including `prompt_digest`,
must fail closed and identify the field name.

### 4.5 Scope preservation

The work does not:

- Modify `gate_ratchet.py`.
- Modify historical manifest digest values.
- Add workflows.
- Add required status-check contexts.
- Treat missing files as successful comparisons.

## 5. Expected regression tests

All six required cases below are EXPECTED (not executed).

| Test | Expected result |
|---|---|
| T1 top-level correct digest | PASS, exit 0 |
| T2 top-level wrong digest | FAIL, exit 1 |
| T3 top-level missing file | FAIL, exit 1 |
| T4 nested wrong digest | FAIL, exit 1 |
| T5 unknown digest field | FAIL, exit 2 |
| T6 declaration/comparison mismatch | FAIL, exit 2 |

Additional fallback tests cover both an existing and a missing
conventional prompt-v1.md.

The existing Git blob, cross-commit, SHA-256 and byte-count tests
must remain passing.

## 6. Historical debt

The reader repair will expose historical inconsistencies that the
previous checker silently failed to inspect.

Based on the supplied measurements, at least 33 additional genuine
mismatches are expected.

These failures must not be eliminated by changing existing manifest
digest values as part of Issue #1463.

Before enabling this enforcement as a blocking CI condition, the
repository must either:

1. Repay the historical digest debt; or
2. Use a ratchet whose baseline anchoring has already been
   implemented and verified under Issue #1462.

A ratchet without a trustworthy baseline anchor is not an acceptable
substitute for complete validation.

## 7. Files in scope

- `scripts/ci/check_manifest_blob_pins.py`
- `scripts/ci/test_check_manifest_blob_pins.py`
- `14-ai-development/work-items/AID-2026-327/manifest.yaml`
- `14-ai-development/work-items/AID-2026-327/session-evidence.md`
- `14-ai-development/work-items/INDEX.md`

No other file is authorized for modification by this work item.

## 8. Verification status

The complete source files and test proposals are supplied for
operator application.

The following have NOT been executed by this session:

- T1 through T6.
- The conventional fallback positive and negative tests.
- The full existing test suite.
- The top-level error-digest injection.
- The nested error-digest injection.
- The coverage assertion negative construction.
- Full-tree verification on the exact main commit.
- CI workflow execution.

No PASS, CI success, merge, or Owner acceptance is claimed.

The operator must preserve actual command output and return codes
as execution evidence.

## 9. Acceptance boundary

The implementation may advance to IMPLEMENTED only after:

1. The six mandatory regression tests pass.
2. Existing tests pass.
3. Full-tree declaration and comparison counts are recorded.
4. Top-level and nested injection experiments both fail as expected.
5. The coverage assertion experiment fails as expected.
6. The final diff contains only authorized files.
7. No historical digest values or ratchet implementation have
   been changed.

Until these conditions are met, implementation status remains
IN_PROGRESS.
