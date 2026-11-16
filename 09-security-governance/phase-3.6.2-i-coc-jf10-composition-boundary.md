# Phase 3.6.2 — I Disposition: COC and JF-10 Composition Boundary

- Owner: Session I — Security, Identity & Governance
- Date: 2026-11-16
- Decision: **COC ACCEPTED AS CGH CROSS-AUTHORITY ORDER INPUT WITH I-OWNED EVIDENCE; NO AUTOMATIC JF-10 COMPOSITION**
- Exact A CGH package reviewed: `4961ffefc0f9920efb8425a9b2a7af42d8f64819`
- Exact A COC architecture reviewed: `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`
- Exact Storage boundary review: `a589d983ac145244962c22e5da3a55427aa35ff8`
- Exact I JF-10 v2 disposition: `b7b0287cde3922434a560fca90051cc5b418d987`

This is an I technical authority-boundary disposition. It is not external Security/Governance approval, production policy activation, deployment acceptance, or implementation/conformance evidence.

## 1. Decision

I accepts the COC architecture as the common causal-order evidence service for the exact CGH-APPLIED-1.1 submit/forget/revocation flow, subject to the constraints below.

I retains exclusive authority over:
- PolicyDomainRef, authorization decision and CommitAuthorizationReceipt;
- receipt consumption and IAuthorizationTerminalRef;
- PermissionEpoch and revocation semantics;
- ProducerDomainInventoryEpoch and InventorySealReceipt;
- issuer/key trust and I-owned signer/verifier lifecycle.

For the CGH flow, COC may durably record I-issued revocation-request references, request cutoffs, I authorization terminal evidence and the cross-authority transaction's causal-order positions. COC may validate issuer identity/integrity and exact binding as an infrastructure consumer, but it MUST NOT mint, alter, infer or reverse an I authorization or PermissionEpoch decision.

I accepts the outage safety rule: when COC is unavailable, I durably suspends affected receipt issuance/consumption and retains an owner-local pending gate. I reopens only after the complete recovery batch is committed and I has reconciled all affected pre-batch participants and verified its owner high-water. The COC recovery batch does not order I and D requests by their owner-local clocks.

## 2. COC position is not automatically the I policy-domain sequencer position

The COC architecture currently specifies a common append-only order log for C/I/D causal events. The JF-10 v2 protocol separately specifies an I-owned policy-domain sequencer/coordinator that durably records the owner-final-gate 2PC decision and participant XID.

These are not interchangeable merely because both expose durable positions or because an I reference is copied into a COC entry.

For CGH-APPLIED-1.1:
- the COC position is the common cross-authority causal-order position;
- IAuthorizationTerminalRef remains an I-issued terminal authority fact;
- the I owner sequencer remains authoritative for authorization/revocation and PermissionEpoch;
- COC stores/verifies the I evidence but does not create it.

A future implementation MAY use one physical consensus substrate for both services only if I approves a concrete state-machine/namespace/transaction design proving that the I-owned sequencer decision is durably committed, linearizable per PolicyDomain, independently authenticated and recoverable. Shared physical infrastructure alone does not merge the authorities or make a COC position an I decision.

## 3. JF-10 remains a separate I owner-gate protocol

I's exact JF-10 v2 decision remains:
- single-policy-domain owner-gate-participating durable 2PC architecture ACCEPTED WITH BINDING CLARIFICATIONS;
- multi-policy-domain atomicity BLOCKED;
- JF-10 P0 overall OPEN pending D/E/Storage acceptance, implementation and tests.

The JF-10 I sequencer orders the exact Storage owner-final-gate participant/XID against revocation. The Storage VisibilityPointer and PublicationReceipt remain the only publication authority. A standalone I COMMIT_WON is not visibility.

The CGH COC does not replace or satisfy:
- I's JF-10 coordinator PREPARE/COMMIT/ABORT decision log;
- durable prepared Storage participant/XID and lock retention;
- exact I owner-gate/receipt-consumption atomicity;
- Storage local atomic VisibilityPointer + PublicationReceipt transaction;
- D fence/lineage serialization at the Storage visibility boundary.

Conversely, a JF-10 Storage PublicationReceipt does not prove C provider submission or G Full Applied.

## 4. Composition rule

The current architecture is accepted as two distinct protocol domains:
1. **CGH COC:** C/I/D causal order for actual provider submission, Forget/revocation cutoffs and G Applied evidence.
2. **JF-10:** I-coordinated owner-gate 2PC for D/E/Storage protected publication within one I policy domain.

No automatic cross-protocol atomicity is approved. If a future operation requires both protocols as one indivisible protected action, I requires a new exact-version joint protocol that specifies:
- stable cross-protocol operation identity and immutable digest/boundary binding;
- which sequencer is the single ordering authority, or how two authoritative logs are atomically coordinated;
- participant PREPARE/COMMIT/ABORT membership and durable decision ownership;
- D fence participation and lineage high-water interaction;
- C actual provider outcome and Storage publication outcome as distinct facts;
- crash/partition/failover/restore matrix, lookup and recovery authority;
- revocation behavior while either participant is IN_DOUBT;
- no heuristic commit/abort, no timeout release, and no partial success.

Until that protocol is accepted by I, D, C, G and Storage, any combined operation is BLOCKED/UNKNOWN. Do not use a saga, outbox, copied receipt, shared transaction label or common log name to imply atomicity.

## 5. Exact review of recovery-batch amendment

I accepts the current recovery-batch safety semantics for CGH:
- I/D owner-local pending gates are durable while COC is unavailable;
- recovery-cutoff batch records all owner-known outage requests without inventing cross-owner order;
- every affected pre-batch ParticipantIntentRef is enumerated;
- I independently reconciles its receipt/revocation terminal state for each applicable participant;
- I's high-water and terminal evidence are monotonic;
- I local gate remains closed if any request, participant, prefix, terminal evidence or owner high-water cannot be proven.

The H schema addendum at H Owner artifact `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`, Blob `d2759386ab1cd4e5518fdb1820e2ad7044ad1871`, is a transport candidate only. It does not change I semantics or constitute I crypto/key-governance approval.

## 6. Open I requirements

- I policy-domain sequencer and receipt service implementation, persistence, authoritative lookup, failover and restore: NOT VERIFIED.
- Any shared physical substrate between COC and I sequencer: NOT SELECTED / NOT APPROVED.
- JF-10 v2 prepared participant/XID implementation and integrated recovery: NOT IMPLEMENTED / NOT VERIFIED.
- ProducerDomainInventoryEpoch and InventorySeal authority/closure: CANDIDATE / OPEN.
- I36-GOV-01..10: GOVERNANCE-BLOCKED; this document is not external approval.
- I-CO, COC-01..16, JF10-01..17 and related consumer conformance: SPECIFIED / NOT RUN.
- Multi-policy-domain atomic authorization: BLOCKED.
- Global Forget completion and production activation: NOT APPROVED.

## 7. Final disposition

I accepts COC as the CGH cross-authority causal-order evidence service only within the exact A artifacts pinned above. I does not approve an automatic COC↔JF-10 composition. JF-10 remains separately governed by the I owner-gate-participating 2PC decision. Any future combined operation requires a new joint protocol and exact Owner decisions. No implementation, production deployment, governance approval or test pass is claimed.
