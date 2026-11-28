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
        - "14-ai-development/work-items/AID-2026-360/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Snapshot bytes are pinned in the adjacent manifest; provenance is recorded as NOT_VERIFIED."
    usage_status: Active
    modification_status: Active-Modified
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
    canonical_scope: "Task input for AID-2026-360: the merge-group candidate validation gap."
    canonical_scope_id: "ai-development/aid-2026-295-prompt-snapshot"
    canonical_scope_keywords:
      - "AID-2026-360"
      - "merge-group candidate"
      - "prompt snapshot"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Executed prompt snapshot - AID-2026-360

Role: implementation session for the merge-group candidate validation gap.

Authoritative specification: `reply-6b07c97e-081917.md` lines 11-199, section 1
(GAP-03) and section 2 (GAP-04). It fixes the three candidate relations and the
per-cell failure-semantics table.

Task as issued to the session:

1. Add one shared candidate resolver module and use it from both
   `.github/workflows/session-evidence.yml` and
   `.github/workflows/bilingual-docs.yml`; no duplicated parsing.
2. Decide the three relations on one candidate tree:
   `B ≼ C` (trusted base is an ancestor of the candidate),
   `∀i H_i ≼ C` (every member head is an ancestor of the candidate),
   `∀i H_i ⋠ B` (no member head is already contained in the base).
3. Read the complete queue membership by paging `Repository.mergeQueue`; a single
   `pr-N` ref of the queue branch is not the merge group.
4. Ancestry is decided through the GitHub Compare API
   (`merge_base_commit.sha` plus `behind_by`), because the verdict job checks out
   the base with a shallow history.
5. Validate every member pull request body against that candidate tree. Evidence
   paths, manifest entries and prompt snapshots are resolved through the
   candidate tree, never through `pr.head.sha`.
6. Keep `INCOMPLETE` (exit 2) distinguishable from `VIOLATION` (exit 1), and emit
   exactly one total verdict line with the `AI-SESSION-EVIDENCE:` prefix; member
   lines must not carry that prefix.
7. Offline tests under `tests/merge_group/`; `python -m unittest discover -s
   tests/merge_group -p "test_*.py" -v` must be OK, and the existing
   `tests/session_evidence` suite must stay green.
8. Do not modify `document-management.yml` or `gates.yml`; do not force, rebase,
   merge, change other pull requests, enable the merge queue, or change branch
   protection.
