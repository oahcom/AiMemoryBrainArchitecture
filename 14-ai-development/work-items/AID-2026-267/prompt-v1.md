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
        - "AID-2026-267/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Structured prompt scope snapshot; not a byte-for-byte raw chat capture."
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
    canonical_scope: "Structured scope snapshot for AID-2026-267"
    canonical_scope_id: "ai-development/aid-2026-267-prompt"
    canonical_scope_keywords:
      - "issue-134"
      - "gate-contract"
      - "implementation-scope"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# AID-2026-267 — Prompt snapshot

Prompt status: RECORDED_NOT_FROZEN
Provenance: USER_AUTHORIZED_DELEGATED_REQUEST
Capture type: structured scope snapshot, not a byte-for-byte chat export.

## Requested outcome

Implement Issue #134's remaining P0 closure condition in
oahcom/AiMemoryBrainArchitecture: enforce required ⊆ declared ⊆ produced in
scripts/check_declared_check_contexts.py.

## Mandatory behavior

- Read the live branch payload through GET /repos/{owner}/{repo}/branches/{branch},
  using protection.required_status_checks.contexts; do not use /protection.
- Reuse declared_contexts().
- Exit 0 only when every required context is declared and every declared context
  is produced; print declared, required and produced counts and both empty diffs.
- Exit 1 and name a context required by the branch but absent from the document.
- Preserve exit 1 for a declared context not produced by any workflow.
- Exit 2 and name the unavailable input and reason when the payload cannot be
  read, is None, or lacks the required field.
- Test injected payloads, including a required-only context and unavailable
  payload; do not depend on live branch state for probes.
- Keep the existing workflow invocation hard-failing; no warn-only or || true.
- Do not add a snapshot, secret, scheduled task, new workflow job, or change
  branch protection.
- Open a PR related to #134, include Session Evidence fields, and stop before
  merge for independent review.
