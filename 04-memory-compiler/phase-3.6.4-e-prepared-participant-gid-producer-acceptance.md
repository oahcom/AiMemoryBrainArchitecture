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
    canonical_scope: "E-domain Memory Compiler record phase-3.6.4-e-prepared-participant-gid-producer-acceptance.md; canonical placement pending Owner acceptance."
    canonical_scope_id: "memory-compiler/e-phase-3-6-4-e-prepared-participant-gid-producer-acceptance"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-4-e-prepared-participant-gid-producer-acceptance
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# E Owner — Exact JF-10 Prepared Participant Identity / GID Producer-Boundary Acceptance

- Storage protocol §14 Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- A integration mapping Blob: `a71251704851cacd15f67faa985a5bd50057e92a`
- B typed-reference registry Blob: `b5a169a1f2c2e6db4b7c8f96b127af971ff53f1f`
- H BMCP schema 1.1.1 candidate Blob: `c0bbfc7611a8d88a39cee209831db32b62601fde`
- Decision: **ACCEPT WITH E-OWNED PRODUCER LIFECYCLE CONDITIONS**
- Mode: delegated E-boundary review under user instruction; not independent human sign-off.

E accepts the new prepared participant identity mapping:

1. `PreparedParticipantRef` + `PreparedTransactionGID` bind one immutable `PublicationOperationId`, `RequestDigest`, participant digest, WorkItem/DerivationRun/manifest lineage, exact owner boundary, `CausalOrderDomainRef`, single `PolicyDomainRef` and `CanonicalAuthorityDBRef`.
2. Storage owns allocation/persistence of the stable participant/GID pair. E MUST NOT mint a GID, rotate it per attempt, derive it from AttemptId or replace it after timeout/restart.
3. AttemptId and worker LeaseEpoch may change on retry; PreparedParticipantRef, PreparedTransactionGID, PublicationOperationId, RequestDigest, manifest digest and participant tuple do not.
4. COC prepare-intent commitment must precede Storage PREPARE. E cannot cause a Storage PREPARE or publish artifacts based on preallocation alone.
5. `EngineNativeTransactionXIDRef` is post-PREPARE engine evidence; it is not WorkItemId, PublicationOperationId, artifact ID, authorization or retry identity.
6. D producer registration and barrier admission remain prior to dereference/execution/publication. If a D cutoff wins before COC intent, E's work remains blocked and no PREPARE occurs; if COC intent wins, D tracks the same PreparedParticipantRef in its barrier.
7. Staged artifacts remain private until Storage authoritative same-GID resolution and the atomic VisibilityPointer/PublicationReceipt transaction. A PreparedParticipantReceipt alone is not publication.

Exceptions: no production E ledger, durable queue/outbox, worker lease, artifact store or Storage adapter is implemented; preallocation cancellation and same-GID recovery are NOT RUN. This is design acceptance only; JF-10 runtime P0 remains OPEN.