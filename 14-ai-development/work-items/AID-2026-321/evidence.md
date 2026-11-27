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
        - "14-ai-development/work-items/AID-2026-321/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "This evidence record defines required verification; no operator execution output has yet been supplied."
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
    canonical_scope: "Implementation and verification evidence for AID-2026-321 DM-12 mirror-group closure extension."
    canonical_scope_id: "ai-development/aid-2026-321-execution-evidence"
    canonical_scope_keywords:
      - "AID-2026-321"
      - "DM-12"
      - "gate verification"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-321 — Evidence

## 1. Required scope

This work item changes only the DM-12 checker, its self-check tests, its
machine-readable schema, its policy description, and its own work-item
records.

The four AID-2026-320 documents are explicitly outside this carrier.

## 2. Required positive evidence

The operator must demonstrate:

- A normal source group with an additional classified mirror passes.
- A reciprocal source-less bilingual pair with a shared reason passes.
- T19 accepts the new schema/gate shape in both directions.

## 3. Required negative evidence

The operator must demonstrate that the gate rejects:

- An undeclared third mirror.
- An additional mirror without metadata.
- A source-less sentinel without a reason.
- A source-less singleton or isolated member.
- Source-less members that do not list every other member.
- Inconsistent `domain`, `role`, or `authority.normative_status`.
- A source-absence reason without the sentinel.
- A source pointer that names a mirror instead of the authoritative source.

## 4. Required commands

```bash
python scripts/test_check_document_management.py
python scripts/check_document_management.py --require-changed origin/main
