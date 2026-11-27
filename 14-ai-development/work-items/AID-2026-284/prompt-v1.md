---
document_metadata:
  domain: ai-development
  role: reference
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
        - "14-ai-development/work-items/AID-2026-284/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Structured capture of the dispatched task contract; not a byte-for-byte platform transcript or frozen prompt snapshot."
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - "manifest-blob-pins"
      - "negative-fixture-assertion"
      - "event-aware-base-resolution"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-284 — Structured task capture

## Capture metadata

- Work item: AID-2026-284
- Date: 2026-11-27
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Issues: #1349 and #1350
- Implementing branch: `fix/aid268-negative-assertion`
- Base commit: `7fc4ddabe1ea3b216b4536c0f5cb0a0c84306f19`
- Fix commit: `ccb22465`
- Prompt status: `RECORDED_NOT_FROZEN`
- Capture provenance: `STRUCTURED_TASK_CAPTURE`

This file is a structured record of the dispatched task contract and its material constraints. It is not represented as a byte-for-byte transcript of the platform prompt, and it is not a frozen prompt snapshot.

## Task

Implement the bounded CI correctness fix associated with issues #1349 and #1350 in `oahcom/AiMemoryBrainArchitecture`.

The change must make the manifest blob-pin negative assertion capable of detecting a false acceptance and must make the workflow select the correct base commit for the event being evaluated.

## Required behavior

1. The immutable negative fixture must be checked by an assertion that verifies the checker rejects it with the expected evidence. A checker invocation that exits successfully without rejecting the fixture must fail the assertion.
2. The base commit used for the workflow's base scan must be resolved from the event context:
   - For `pull_request`, validate the merge-candidate ref and commit, verify that the merge candidate has two parents, and select its first parent.
   - For `push`, use the event's `before` SHA supplied to the resolver.
   - Unsupported events and invalid or unavailable inputs must fail closed.
3. The workflow must use the resolved base SHA for the base measurement and `GITHUB_SHA` for the candidate measurement and ratchet invocation.
4. Preserve the existing repository-hygiene job identity and job name.
5. Do not add a new job, required status context, dependency, or branch-protection change.
6. Do not modify `scripts/ci/baselines/manifest-blob-pins.txt`.
7. Add unit coverage for the resolver and negative assertion.

## Scope

The implementation is limited to:

- `.github/workflows/repository-hygiene.yml`
- `scripts/ci/resolve_manifest_blob_pin_base.py`
- `scripts/ci/assert_manifest_blob_pin_negative.py`
- `scripts/ci/test_resolve_manifest_blob_pin_base.py`
- `scripts/ci/test_assert_manifest_blob_pin_negative.py`

The workflow change replaces the measurement step, changes the ratchet's `--commit` target from `HEAD` to `$GITHUB_SHA`, and adds one self-check step. The workflow's existing job ID and job name remain unchanged.

## Implementation result

The implementation was committed as:

- Commit: `ccb22465`
- Subject: `fix(ci): make the blob-pin negative sample and base binding able to fail (AID-2026-284)`
- Branch: `fix/aid268-negative-assertion`

The fix adds event-aware base resolution and an assertion for the immutable negative sample. The assertion requires the fixture to be rejected with the expected summary and mismatch evidence; an unexpected clean result is a violation.

## Verification contract

Local verification includes:

- Resolver unit tests.
- Negative assertion unit tests.
- Existing blob-pin checker unit tests.
- Offline workflow-step proof comparing the pre-fix and delivered step behavior with a deliberately silent, successful checker.
- Offline base-selection proof comparing the prior event-time-base behavior with the merge-candidate first-parent behavior.
- Verification that the baseline file remains unchanged.

GitHub Actions execution, pull-request review, and Owner acceptance are separate pending events and must not be represented as completed by this capture.
