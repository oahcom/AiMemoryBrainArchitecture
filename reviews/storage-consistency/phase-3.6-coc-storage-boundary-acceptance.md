# Phase 3.6 — Storage/Consistency Review of Causal Order Coordinator and CGH-APPLIED-1.1

- Owner: Storage/Consistency (DE-S joint engineering review; Storage authority boundary only)
- Date: 2026-11-16
- Decision: **CONFIRMED WITH CHANGES — ARCHITECTURE INTERFACE ONLY**
- COC artifact: `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md`
- Exact COC Blob SHA reviewed: `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`
- CGH package: `reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`
- Exact A package Blob SHA reviewed: `4961ffefc0f9920efb8425a9b2a7af42d8f64819`
- Profile: `CausalOrderProfile/1.0`; H candidate: `bmcp.applied-ack/1.1.0`

This is a Storage Owner architecture-interface decision for the exact artifacts above. It is not a named-operator designation, infrastructure deployment approval, production readiness approval, I policy approval, or conformance result.

## 1. Decision

Storage **CONFIRMS WITH CHANGES** the COC proposal as a logical cross-authority causal-order service for the CGH-APPLIED-1.1 submit/forget/revocation workflow, subject to the boundary and blocking conditions below.

Storage confirms the architectural value of:
- quorum-committed append-only order records and linearizable reads for protected C/I/D causal events;
- immutable transaction/participant identity and canonical payload digest;
- fail-closed behavior on minority partition, uncertain prefix, stale read, digest conflict and owner evidence mismatch;
- durable owner-local pending gates when COC is unavailable;
- recovery-cutoff batching without inventing cross-owner order from local clocks;
- complete enumeration/reconciliation of pre-batch ParticipantIntentRefs before I/D local gates reopen;
- non-expiring IN_DOUBT participants and RESTORE_FENCED on unprovable restore;
- coordinator non-interference with I authorization, D ForgetFence, C actual submit evidence and G Applied authority.

The proposed three-voter/two-quorum profile is accepted only as a **design target for evaluation**. Storage does not confirm that three independent failure domains, durable media, encryption/KMS, RPO/RTO, data residency, backup or operational SLO currently exist.

## 2. Mandatory changes and authority boundaries

### 2.1 COC is not the Storage visibility transaction

The COC log is a cross-authority causal-order ledger. It is not:
- the Canonical Memory Authority database;
- the D producer-work/fence/dependency transaction;
- the Storage VisibilityPointer or PublicationReceipt authority;
- an object-store visibility switch;
- a substitute for a transactionally committed Storage owner outcome.

The selected Storage realization remains one durable serializable (or formally proven equivalent) transaction domain per Canonical Memory Authority covering D work admission, registration sequence, fence/high-water snapshot, complete dependency registration, final visibility gate, VisibilityPointer, PublicationReceipt, terminal disposition and transactional outbox. Object/blob bytes remain private until the authoritative visibility transaction commits.

An outbox event from that database to COC, or from COC to Storage, is notification/reconciliation evidence only. It cannot be treated as an atomic commit, a visibility pointer, or proof that the other system committed.

### 2.2 COC is not I's policy-domain sequencer or JF-10 2PC coordinator

I alone owns the policy-domain sequencer, CommitAuthorizationReceipt, revocation order and PermissionEpoch. The Storage JF-10 protocol has an additional I36-SR-02 requirement: the final Storage owner gate must participate in I's approved per-domain commit-order protocol, with a durable prepared Storage participant/XID and recoverable terminal decision.

A COC position, COC reservation, copied I receipt, local receipt-consumption row, or COC terminal proof does not by itself prove that the Storage prepared participant joined I's sequencer/2PC order. Nor does a standalone I COMMIT_WON followed by an unrelated Storage transaction satisfy this requirement.

Therefore the following are separate until I approves an explicit bridge:
1. COC's C/I/D submit causal-order transaction for CGH Applied.
2. I's policy-domain sequencer and owner-gate-participating JF-10 protocol.
3. Storage's per-Canonical-Memory-authority atomic visibility transaction.

No two of these may be collapsed by naming a common transaction ID or copying a receipt. If a protected operation requires all three, the exact cross-protocol binding, ordering authority, prepare/commit participants, recovery authority and crash matrix must be specified by I and accepted by C/D/Storage before activation. Until then the combined operation is BLOCKED/UNKNOWN and bytes remain private.

### 2.3 No split-brain between COC and Canonical Authority DB

The COC log and the per-authority Storage database are distinct consistency domains in the current proposal. The proposal does not yet specify a distributed atomic commit spanning both. Accordingly:
- the COC log cannot be used as a substitute for a serializable transaction over D fence/work and Storage visibility rows;
- a per-authority DB commit cannot be inferred from a COC append or acknowledgement;
- a COC terminal proof must not claim Storage publication or JF-10 completion unless the exact Storage receipt/commit evidence is included and independently verified;
- a Storage PublicationReceipt must not claim CGH Full Applied or cross-authority submit terminality;
- disagreement, missing bridge evidence, stale state or ambiguous commit leaves the combined operation UNKNOWN/IN_DOUBT and fail-closed.

The preferred safe v1 boundary is to keep these protocols separately authoritative and prohibit flows that require an unproven atomic cross-domain transaction. Do not invent a best-effort saga or heuristic compensation as a replacement for the missing safety proof.

## 3. Storage-side realization confirmed unchanged

The following Storage decisions remain in force:
- One transactional DB/linearizable coordinator per Canonical Memory Authority for D and Storage safety-critical rows.
- D fence installation and producer admission serialize in that same authority domain.
- Complete dependency registration is atomic as a completeness unit; partial dependency sets are never publishable.
- Final visibility linearizes only at the authoritative DB transaction which revalidates current D fence, work/attempt/lease, dependency/manifest digest and approved I authorization evidence.
- VisibilityPointer, PublicationReceipt, owner outcome, receipt consumption and outbox are one atomic local outcome.
- Staged object existence, object-store listing, index/cache, stale replica, outbox delivery and process-local state never establish visibility.
- Restore/rebuild remains quarantined until the latest Forget control ledger, owner cursors and visibility decisions are reconciled.
- UNKNOWN/IN_DOUBT participants do not expire, disappear on compaction, or release D/I barriers.

This confirms the logical Storage boundary only. The concrete database product/version, schema, isolation level, replication/failover, prepared-XID capability and restore proof remain unselected/unverified.

## 4. Exact unresolved acceptance and deployment items

| Item | Storage disposition |
|---|---|
| COC logical append-only quorum-log pattern | Confirmed with changes as design target |
| Actual named COC operator/service owner | OPEN — no accountable operator identified |
| Actual voter/failure-domain placement | OPEN — no infrastructure evidence |
| Durable media, quorum commit and linearizable read implementation | OPEN — not deployed or verified |
| Snapshot/checkpoint signing, external rollback protection and total-loss restore | OPEN |
| Retention/compaction for cutoffs and unresolved participants | Semantics confirmed; actual retention policy/configuration OPEN |
| RPO/RTO, SLO, data residency, encryption/KMS and escalation | OPEN |
| Canonical Authority DB engine/version/isolation and HA | OPEN |
| I-approved JF-10 owner-gate 2PC/bridge | BLOCKED — I decision required |
| COC ↔ Storage atomic cross-domain transaction | NOT SPECIFIED; unsupported until proven |
| Production implementation and conformance | NOT VERIFIED / NOT RUN |

Storage cannot name a real service operator, failure-domain topology, DB product, or operational SLO from architecture documents. These require an accountable engineering owner and actual environment evidence; they are not filled by inference.

## 5. Required owner decisions before any combined activation

1. **I:** publish/approve the exact JF-10 owner-gate participation protocol and state whether/how it composes with COC; specify one authoritative order and durable recovery for all required participants.
2. **D:** confirm that COC cutoff/intent evidence is only an external causal-order input and that D's own fence generation, lineage barrier and per-authority DB linearization remain authoritative.
3. **C:** define whether CSubmitOutcome/terminal proof is independent of Storage publication, and how any combined transaction binds the two without implying one from the other.
4. **G:** confirm that Full Applied for the protected final-request flow does not infer Storage publication; if Storage publication is required by a particular Applied predicate, specify its exact owner-issued receipt input.
5. **H:** preserve distinct typed evidence families and reject downgrade/missing bridge evidence; H transport ACK is not commit proof.
6. **Storage engineering operator:** identify actual service owner, COC topology, Canonical Authority DB engine/configuration, prepared transaction support if used, RPO/RTO, backup/restore and key custody.
7. **A:** revise the integration gate to show COC causal ordering, JF-10 I-coordinated prepared publication and per-authority Storage visibility as distinct but explicitly bound protocols; do not label the package Frozen until all bridge semantics and exact owner approvals exist.

## 6. Conformance and implementation status

- JF-10 in-memory reference model: **IMPLEMENTED AS A LOGICAL MODEL ONLY**.
- 15 deterministic unittest methods: **AUTHORED / NOT RUN IN REPOSITORY CI**.
- JF-10 production implementation: **NOT IMPLEMENTED / NOT VERIFIED**.
- Storage C01–C23 and JF10-01..17: **SPECIFIED / NOT RUN**.
- COC-01..16: **SPECIFIED / NOT RUN**.
- COC quorum/restore deployment: **NOT DESIGNATED / NOT DEPLOYED / NOT VERIFIED**.
- I JF-10 owner-gate 2PC acceptance: **BLOCKED / REQUIRED**.
- Combined COC + JF-10 + Storage visibility atomicity: **NOT PROVEN; FAIL CLOSED**.
- Applied Contract Frozen: **NO**.
- Production activation: **NOT AUTHORIZED**.

## 7. Exact source readback

This decision was made after reading the exact A COC and CGH package Blob SHAs in the header and the current Storage Owner artifacts:
- `reviews/storage-consistency/phase-3.6-deployment-selection-and-verification-readiness.md`, Blob `89f8fb36f22a2c1eb7920e0d2941cfcc85652a5c`;
- `reviews/storage-consistency/phase-3.6.2-jf10-cross-authority-recovery-protocol.md`, Blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0`;
- `reviews/storage-consistency/phase-3.6.2-jf10-executable-conformance-plan.md`, current readback recorded by the Storage Owner branch;
- `reviews/storage-consistency/reference_model/README.md`, Blob `91bc63ae3619d851b6a56e178e273c7d9868129e`.

This decision is pinned only to COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea` and A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819`. Any later amendment requires a fresh Storage review.