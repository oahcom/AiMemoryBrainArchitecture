---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Restored byte-for-byte from Owner source branch; Owner acceptance remains pending."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Canonical
    canonical_scope: "E-domain Memory Compiler record phase-3.6.2-jf10-reference-model-consumption.md; canonical placement pending Owner acceptance."
    canonical_scope_id: "memory-compiler/e-phase-3.6.2-jf10-reference-model-consumption"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3.6.2-jf10-reference-model-consumption
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---



# E Owner — JF-10 Executable Reference Model Consumption

- Status: **REFERENCE-MODEL MAPPING / OWNER REVIEW REQUIRED**
- Model source: Storage Owner branch, `reviews/storage-consistency/reference_model/jf10_linearization_model.py`
- Scope: logical stable identity and retry semantics only; not production E implementation.

## E-owned behavior represented

The reference model's `ProducerManifest` binds one WorkItemId to one immutable PublicationOperationId and manifest digest. Repeated execution attempts may vary AttemptId without changing publication identity. Rebinding a WorkItemId to another operation or changing its frozen manifest digest is rejected.

This is the logical behavior covered by JF10-E-16. The Storage participant model also carries the immutable operation and manifest digest into the visibility publication.

## Required production mapping

E implementation must identify the durable frozen output/lineage manifest, WorkItemId and PublicationOperationId generation, AttemptId/LeaseEpoch retry fencing, manifest digest canonicalization, and the exact handoff to Storage. E must not claim Published based on producer completion or staged object existence.

## Explicit non-claims

This model does not implement E's durable compiler ledger, artifact store, manifest canonicalization, retry scheduler, lease service, or Storage integration. It does not pass E36 or JF10-E-16. E owner review and production-equivalent evidence remain required.
