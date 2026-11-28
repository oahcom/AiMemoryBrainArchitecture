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
        - "14-ai-development/work-items/AID-2026-343/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Task snapshot recorded for traceability; no implementation or independent verification is claimed."
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
    canonical_scope: "Implementation task snapshot for AID-2026-343 DM-12 additional mirrors and source-less group closure."
    canonical_scope_id: "ai-development/aid-2026-343-prompt-snapshot"
    canonical_scope_keywords:
      - "AID-2026-343"
      - "DM-12"
      - "additional mirrors"
      - "source-less group"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-343 — Prompt Snapshot

## 1. Task

Extend GOV-DOC-002 DM-12 so that a source can declare additional mirrors
through `bilingual_counterpart.mirrors`, and a closed mirror group can
explicitly declare that it has no authoritative source through
`source: NO_AUTHORITATIVE_SOURCE` and a non-empty `source_absence_reason`.

## 2. Required behavior

For normal source groups:

- Preserve the `en` and `zh-CN` language slots.
- Add `mirrors` as a sequence of additional mirror paths.
- Require each additional mirror to exist and be classified.
- Require each mirror to declare the same source.
- Require the source to list every mirror that names it.
- Merge `en`, `zh-CN`, and `mirrors` into reverse closure.
- Reject an undeclared third mirror.

For source-less groups:

- Require every member to declare `NO_AUTHORITATIVE_SOURCE`.
- Require the same non-empty `source_absence_reason` on every member.
- Require every member to list every other member.
- Reject a singleton or isolated mirror.
- Require agreement on `domain`, `role`, and
  `authority.normative_status`.

## 3. Non-regression requirements

The change must not:

- Relax DM-12 closure.
- Accept unclassified documents.
- Accept a mirror whose source is another mirror.
- Permit inconsistent metadata.
- Permit two `Canonical` documents in one group.
- Change the four AID-2026-320 documents.
- Add a workflow, job, required context, or branch-protection change.

## 4. Required implementation files

- `scripts/check_document_management.py`
- `scripts/test_check_document_management.py`
- `00-governance/architecture-document-metadata.schema.yaml`
- `00-governance/architecture-document-management-policy.md`
- AID-2026-343's four work-item files and INDEX row.

## 5. Verification contract

The operator must run:

```bash
python scripts/test_check_document_management.py
python scripts/check_document_management.py --require-changed origin/main
```

The operator must record the actual outputs and exit codes. No
implementation, verification, review, merge, or Owner acceptance is
presumed by this task snapshot.

## 6. Identifier migration

The work-item identifier for this package is AID-2026-343.

The migration replaces the previously proposed AID-2026-321 identifier.
All internal work-item paths and self-references must use
`AID-2026-343/`.

The migration does not change the DM-12 technical requirements or
authorize changes to the four AID-2026-320 documents.
