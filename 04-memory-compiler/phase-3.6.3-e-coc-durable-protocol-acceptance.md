---
document_metadata:
  domain: memory-compiler
  role: design-specification
  steward: USER-PRINCIPAL-DELEGATED
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
    canonical_scope: "E-domain Memory Compiler record phase-3.6.3-e-coc-durable-protocol-acceptance.md; canonical placement pending Owner acceptance."
    canonical_scope_id: "memory-compiler/e-phase-3-6-3-e-coc-durable-protocol-acceptance"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-3-e-coc-durable-protocol-acceptance
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# E Owner — Exact COC Durable Protocol Producer-Boundary Acceptance

- Exact Storage protocol Blob: `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`
- A COC architecture Blob: `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- E JF-10 producer acceptance Blob: `4503628cf6f6ea46696ab14e7decd3e408ced19a`
- Decision: **ACCEPT WITH E-OWNED PRODUCER LIFECYCLE CONDITIONS**
- Mode: delegated E-boundary review under user instruction; not independent human sign-off.

E accepts the protocol as the producer lifecycle and recovery-accounting boundary:
1. AcceptedReceipt is durable ingress only; it is not D producer registration, permission to execute or publication.
2. WorkItemId, PublicationOperationId, DerivationRunId, frozen manifest digest, source revision refs and Storage participant/XID remain immutably bound.
3. Retry may change AttemptId/LeaseEpoch but cannot mint a new logical participant, XID, operation ID or manifest digest.
4. D producer registration and complete dependency receipt precede dereference, lease, execution and publication.
5. Artifacts, embeddings, provenance and candidate metadata remain private until Storage authoritative same-XID PublicationReceipt confirms the atomic visibility transaction.
6. COC records producer/participant lifecycle observations only. It does not authorize compiler execution, decide D/I outcomes or publish content.
7. Unknown/in-doubt participants remain open across restart, DLQ, lease expiry and restore; no TTL release.

Exceptions: no production E ledger, queue/outbox, worker lease, artifact store or Storage adapter is implemented; COC/E/D/I end-to-end tests are NOT RUN. This does not claim compiler implementation, production deployment or Global Forget completion.