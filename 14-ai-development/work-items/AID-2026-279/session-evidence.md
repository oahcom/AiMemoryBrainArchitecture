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
        - "14-ai-development/work-items/AID-2026-279/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "This record distinguishes the GitHub Actions test execution from local execution, which was not performed."
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

# Session Evidence — AID-2026-279

## Session role / use case

S6-A implementation session. Implement the serialized merge-time work-item uniqueness gate selected by Issue #1341 using GitHub API operations only. No local working tree or local Python execution is claimed.

## Actual AI input

The user supplied the complete implementation contract for Issue #1341, including:
- reject a newly introduced AID work-item directory if that identifier exists on the latest target branch;
- accept additive files beneath an existing AID directory;
- use exit codes 0 PASS, 1 VIOLATION, 2 INCOMPLETE;
- wire the checker and its explicit self-test into the existing GOV-DOC-002 required job;
- preserve the 16 required contexts and avoid branch-protection changes, new jobs, blob-pin files, and repository-hygiene workflow changes;
- record raw execution evidence, open-PR impact, serialization, and merge verification.

## AI-visible output

The session authored scripts/ci/check_work_item_uniqueness.py and scripts/ci/test_work_item_uniqueness.py, wired both into the existing GOV-DOC-002 job, and created the AID-2026-279 manifest, evidence, prompt snapshot, this session evidence, and one INDEX row.

The checker computes candidate-introduced work-item directories from merge-base to candidate HEAD, then tests occupancy against the latest target base. The tests build isolated temporary Git histories and exercise unoccupied, occupied, additive, incomplete, and deterministic race-replay cases. Real stdout is produced by the required GitHub Actions job, not by local execution in this session.

No Owner acceptance, independent review, branch-protection mutation, or merge is claimed.
