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
    canonical_scope: "E-domain Memory Compiler record phase-3.6.2-e-jf10-coc-bridge-producer-acceptance.md; canonical placement pending Owner acceptance."
    canonical_scope_id: "memory-compiler/e-phase-3.6.2-e-jf10-coc-bridge-producer-acceptance"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3.6.2-e-jf10-coc-bridge-producer-acceptance
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---



# E Owner — Exact JF-10 ↔ COC Bridge Producer-Lifecycle Acceptance

- Owner: E — Memory Compiler
- Branch: `session-e-memory-compiler-2026-11-16`
- Decision mode: delegated E-boundary review performed centrally under the user's instruction to accept the remaining work; not an independent human signature.
- A COC architecture: `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md`, Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- D/E/Storage common JF-10 protocol: Blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0`
- Storage exact JF-10 bundle acceptance: `reviews/storage-consistency/forget-atomicity-storage-realization-review.md`, Blob `107d21bd2c604ee0b04feff2ee5580e1de9c7fce`
- D fence/publication gate: Blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`
- I JF-10 v2 disposition: Blob `8069ff86988396442c8d9dc3fd58653683abe2f3`
- E compiler state/admission baseline: Blob `e59f517fff161ab882aa0ddc4a5bda513964ae1a`
- E Forget fence/derived registration baseline: Blob `00e37ba56596e710513c8d0568acd79141d9101b`
- Date: 2026-11-17
- Decision: **ACCEPT WITH ENUMERATED CONDITIONS — E PRODUCER LIFECYCLE ONLY**

## 1. Decision

E accepts the exact JF-10 ↔ COC bridge as the producer-side lifecycle contract for a compiler-originated derived publication. E's acceptance is limited to stable producer identity, immutable manifest/digest binding, retry/lease behavior, D registration/dependency participation, and E's interpretation of Storage publication receipts. E does not decide I authorization, D ForgetFence, Storage XID commit/rollback, C provider outcome, H wire encoding or COC consensus.

## 2. E-owned requirements

1. Durable source acceptance and AcceptedReceipt are not D producer registration, permission to execute, or publication.
2. One immutable producer operation binds WorkItemId, PublicationOperationId, DerivationRunId, frozen manifest digest, canonical source revision references, exact owner boundary and applicable D lineage/fence identity. Same identity + same digest is idempotent; same identity + changed digest is a hard conflict.
3. Retry may create a new AttemptId/LeaseEpoch but MUST preserve WorkItemId, PublicationOperationId, manifest digest and the preallocated Storage participant/XID binding. Retry MUST NOT mint a new logical participant to escape an unresolved barrier.
4. E MUST durably register producer work with D before lease, dereference, execution or derived publication. D's authoritative receipt, not E's local queue or cache, establishes barrier membership.
5. E keeps staged artifacts, blobs, embeddings, provenance edges and candidate metadata private until D confirms complete dependency registration and Storage returns the authoritative same-operation/same-XID PublicationReceipt.
6. E may report PUBLISHED only after authoritative Storage readback proves atomic VisibilityPointer + PublicationReceipt + owner outcome + receipt-consumption evidence + outbox commit. A COC observation, I COMMIT_WON, D clearance, Storage prepared receipt or worker success alone is insufficient.
7. UNKNOWN/IN_DOUBT preserves the same operation identity and private bytes; no TTL, lease expiry, queue deletion, DLQ movement or worker restart releases D's barrier or makes the artifact visible.
8. Recompile creates a new DerivationRunId only under the same root/source lineage and current D/I checks. It cannot reset the original Forget cutoff, change the participant digest or omit previously registered dependencies.

## 3. E acceptance of bridge interaction

E accepts that COC is a causal-order and participant-accounting service. It may record E/producer participant lifecycle observations, but it does not authorize the compiler, decide D barrier completion, decide I authorization or publish the Storage artifact. E consumes exact owner-issued references without coercing their typed namespaces.

Where a compiler-originated operation is protected by the single-I-PolicyDomain JF-10 profile, it must bind one PolicyDomainRef. Multi-policy-domain atomicity remains BLOCKED / NOT ACCEPTED; E rejects or quarantines a request that cannot be represented within the accepted single-domain profile.

## 4. Exceptions and retained blocks

- E has not demonstrated a production compiler ledger, D registration client, durable queue/outbox, worker lease service, artifact store or Storage adapter.
- No actual end-to-end E/D/Storage/I COC participant was executed.
- Storage's PostgreSQL 18.7 CI evidence qualifies the pinned engine capabilities and isolated reference fixtures only; it is not E adapter integration proof.
- H's 1.1.0 schema candidate is not generated/interoperability-tested and does not constitute E wire acceptance.
- I's external governance approvals, ProducerDomainInventoryEpoch/InventorySeal and Global Forget completion remain OPEN.
- JF-10 remains P0 OPEN for integrated implementation/conformance; this E design acceptance does not close it.

## 5. Required conformance

Required E tests: duplicate AcceptedReceipt; same WorkItemId with changed digest; crash before/after D registration ACK; retry with new AttemptId but stable PublicationOperationId/XID; expired lease cannot publish; partial dependency set remains private; D fence before/after registration; I revocation before/after owner-final gate; Storage PREPARE/COMMIT/ROLLBACK ACK loss; restore with unresolved participant; same-XID readback; late derivative after fence; and recompile cannot escape the original barrier.

A PASS requires executable E producer/manifest ledger, integrated D/I/Storage/COC services, deterministic fault injection, authoritative readback and independent review. This document is architecture/interface acceptance only; no implementation, test pass, deployment or production activation is claimed.