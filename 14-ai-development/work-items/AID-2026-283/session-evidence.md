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
        - "14-ai-development/work-items/AID-2026-283/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Local execution only; no CI run recorded yet."
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
      - "session-evidence"
      - "work-item-uniqueness"
      - "implementation-provenance"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# AID-2026-283 — AI session evidence

## Session identity

Work item: AID-2026-283

Repository: oahcom/AiMemoryBrainArchitecture

Role: L1 triage owner + L2 implementation session

Session date: 2026-11-26

## AI-assisted work

YES.

AI assistance was used for:

- Defect analysis.
- Contract correction.
- Implementation design.
- Regression-test design.
- Mutation-test specification.
- Documentation and evidence authoring.

## Source evidence

The implementation is based on the supplied independent audit facts:

- Existing checker uses merge-base-relative introduced directories.
- Update-branch advances merge-base.
- The second PR can consequently report PASS with introduced=0.
- Different filenames avoid add/add conflicts.
- Existing five tests do not establish the required post-update rejection.
- AID-2026-279 is already merged.
- The required context remains GOV-DOC-002 metadata checks.

## Decision record

The claim is based on candidate-side historical introduction, not the current merge-base difference.

Non-merge commits in base..head are examined relative to their first parents.

This prevents the Update-branch merge commit from manufacturing claims by importing directories from base.

Candidate HEAD existence is also required, preventing deleted directories from remaining active claims.

## Validation record

Baseline test count: 5

Added test count: 3

Expected total: 8

Actual test output:

__TEST_OUTPUT__

Actual mutation output:

__MUTATION_OUTPUT__

## Changed files

- scripts/ci/check_work_item_uniqueness.py
- scripts/ci/test_work_item_uniqueness.py
- manifest.yaml
- prompt-v1.md
- evidence.md
- session-evidence.md

## Prompt integrity

SHA-256: 52ae82d320606c703a47c215b019a136d01530d7b38f775ab5c64f5b2154de76

Byte count: 2751

The delivery operator must calculate these values from the final prompt-v1.md bytes and update both this file and manifest.yaml.

## Review and delivery

Owning Issue: #1403

Pull Request: __PR__

Head SHA: __HEAD_SHA__

Merge SHA: __MERGE_SHA__

Required context: GOV-DOC-002 metadata checks
