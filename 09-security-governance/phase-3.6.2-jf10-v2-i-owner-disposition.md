# Phase 3.6.2 — I Owner Disposition: JF-10 v2 Owner-Gate-Participating Durable 2PC

- Owner: Session I — Identity, Security & Governance
- Branch: `session-i-security-governance-2026-11-16`
- Date: 2026-11-16
- Exact proposal reviewed: D/E/Storage JF-10 v2, Blob `d544cc38a922b314e6dc45dd4db76aae6b47f5fc`
- D source: `03-memory-brain/phase-3.6.2-jf10-cross-authority-recovery-protocol.md`
- E source: `04-memory-compiler/phase-3.6.2-jf10-cross-authority-recovery-protocol.md`
- Storage source: `reviews/storage-consistency/phase-3.6.2-jf10-cross-authority-recovery-protocol.md`
- Status: **I ACCEPTS THE SINGLE-POLICY-DOMAIN ARCHITECTURE WITH BINDING CLARIFICATIONS; MULTI-DOMAIN PROFILE BLOCKED; JF-10 P0 OVERALL OPEN**
- This is an I-owned technical architecture disposition under delegated project authority. It is not external governance approval, production policy activation, implementation evidence, or runtime conformance.

## 1. Exact decision

I has reviewed the exact common v2 Blob SHA above on all three D, E and Storage Owner branches. All three readbacks return the same Blob SHA.

**I ACCEPTS the v2 single-policy-domain protocol architecture with the binding requirements in this addendum.** This supersedes I's rejection of the v1 detached sequence (durable I COMMIT_WON followed by an independent Storage visibility transaction).

The decisive correction in v2 is accepted: Storage's actual final visibility gate is represented by a durable prepared participant/XID submitted into the I policy-domain sequencer's owner-final-gate operation. I's coordinator decision is therefore about that exact owner operation, not a detached preflight authorization. The durable I decision controls participant COMMIT/ABORT; Storage visibility remains unpublished until the participant commit and PublicationReceipt are durably confirmed.

This acceptance is **not** a claim that the protocol is implemented, deployable on a selected database, tested, or sufficient to close JF-10. The v2 text's multi-policy-domain all-or-none claim is not accepted as specified; see §7.

## 2. Binding I semantics

### 2.1 Sequenced operation and linearization

For one I policy domain, the sequenced operation MUST be the exact Storage owner-final-gate operation and MUST bind:
- stable PublicationOperationId and canonical immutable RequestDigest;
- exact owner_boundary identifying the Storage VisibilityPointer commit gate;
- durable Storage participant identity, XID and participant digest;
- CommitAuthorizationReceipt ID and decision binding;
- policy_domain_id, PermissionEpoch, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef and DelegationChainRef;
- applicable D ForgetOperationId/fence reference and the exact owner predicate evidence;
- I ProducerDomainInventoryEpoch and InventorySealReceipt identity/digest when required by the effective policy.

The **I coordinator's durable COMMIT decision** is the I policy-domain ordering/linearization record against conflicting revocation. It means that this exact owner-final-gate participant was ordered before the conflicting revocation. It does not mean the Storage participant has committed or that bytes are visible.

A revocation that conflicts with an unresolved earlier prepared owner-final-gate operation MUST NOT pass that unresolved order by assuming abort. It waits for the authoritative coordinator decision/recovery, or remains blocked. Once COMMIT is durable, a later revocation is ordered after that operation and cannot retroactively rewrite its decision. This is not a stale-epoch grace period or reusable permission: it applies only to the exact participant, operation ID, digest and boundary.

### 2.2 Receipt consumption

The canonical I artifact remains `CommitAuthorizationReceipt`; no second permit/capability is introduced.

I MUST atomically persist receipt consumption with the coordinator's durable transaction record and bind both to the participant XID, participant digest, operation ID/digest, owner boundary, decision ID, policy domain, PermissionEpoch and sequencer position. Receipt consumption MUST NOT be finalized by a detached preflight call.

Same operation ID + same digest + same boundary returns the same durable coordinator state/decision and position. Same ID with changed digest, participant identity/XID, owner boundary or any security-bound tuple is a hard conflict. A receipt cannot be consumed a second time to create another owner operation.

### 2.3 Terminal outcomes

- `COMMIT_WON`: I durably committed the coordinator decision for the exact prepared owner participant before the conflicting revocation. Storage MUST forward-commit that exact prepared participant. No visibility claim is allowed until Storage readback confirms the local transaction and PublicationReceipt.
- `REVOCATION_WON`: the conflicting revocation was ordered first; I durably aborts the participant. Storage MUST roll back and prove non-publication.
- `INDETERMINATE_ABORTED`: I durably terminates the operation as non-success because a safe winning order cannot be established. Storage MUST roll back; it MUST NOT reinterpret this as COMMIT_WON.
- `UNKNOWN/IN_DOUBT`: no authoritative terminal decision is yet recoverably established. This is not a terminal outcome. Keep bytes private, retain the participant and locks, and block conflicting revocation progress until recovery resolves the coordinator record. Never infer commit/abort from timeout, absent rows, process death, stale replicas or lost ACKs.

Heuristic participant commit/abort is forbidden. If an I COMMIT decision is durable, recovery must forward-commit the exact participant; if an I ABORT is durable, recovery must roll it back. If participant recovery is unavailable, remain blocked and escalate; do not reverse the coordinator decision.

## 3. Coordinator durability and recovery contract

I accepts the I sequencer acting as the durable coordinator for this single-domain owner-final-gate protocol, subject to these mandatory guarantees:

1. Coordinator log records PREPARE/participant registration and terminal COMMIT/ABORT durably, with monotonic sequence/decision identity.
2. The participant XID and digest, operation ID/digest, receipt consumption, owner boundary and policy-domain ordering position are retained at least through participant resolution and the full audit/recovery horizon.
3. Authenticated lookup is authoritative and linearizable with the policy-domain sequencer; stale replicas/caches are never decision sources.
4. Coordinator failover/restore cannot lose, duplicate, reorder or reverse a durable terminal decision or forget an unresolved participant.
5. A prepared participant survives Storage process restart and coordinator outage with its private bytes and required serialization locks retained. The selected DB must prove this property; an in-memory prepare or ordinary application row is insufficient.
6. A durable COMMIT drives forward recovery; a durable ABORT drives rollback. Participant resolution is idempotent and same-XID only.
7. Conflicting revocation remains pending while the earlier participant is IN_DOUBT. Unrelated policy operations may proceed only if I can prove they do not conflict with the unresolved authorization tuple.
8. No timeout or operator override may convert IN_DOUBT into COMMIT_WON, REVOCATION_WON or NOT_COMMITTED.

If I cannot meet these coordinator guarantees, or Storage cannot retain/recover the prepared participant, this protocol is not deployable and JF-10 remains blocked. Safety takes precedence over availability.

## 4. D fence and Storage authority boundaries

I accepts the v2 separation of authority:
- D alone owns ForgetFence, work/dependency registration and per-operation barrier semantics.
- Storage alone owns VisibilityPointer, PublicationReceipt and reader-visible publication.
- I alone owns PermissionEpoch, authorization/revocation ordering, CommitAuthorizationReceipt, ProducerDomainInventoryEpoch and InventorySealReceipt.
- E remains non-terminal until it verifies the matching durable Storage PublicationReceipt.

The proposed shared Canonical Authority DB serialization locks are a plausible D/Storage mechanism, but **I does not approve D's fence semantics on D's behalf**. D must explicitly accept that:
- fence-first means the prepare observes the committed fence and rejects;
- prepared-participant-first retains the relevant target/lineage serialization locks, so the fence cannot linearize until the participant commits or aborts;
- if the participant commits first, the later fence captures that publication as pre-fence work and the D barrier must account for it;
- an in-doubt participant prevents D from claiming a closed barrier or completed Forget.

Storage must independently prove that VisibilityPointer + immutable PublicationReceipt + owner outcome + receipt-consumption evidence + outbox commit atomically in one local transaction, and that no staging/object-store/outbox state grants visibility.

## 5. Inventory seal is an I-owned precondition, not a local lock assumption

The v2 request digest correctly includes ProducerDomainInventoryEpoch and InventorySealReceipt. However, a Storage-local lock on a copied seal reference does not by itself serialize against changes in I's authoritative inventory registry.

Therefore, when effective policy requires a seal, I's owner-final-gate sequencer MUST validate and bind the current authoritative inventory epoch, seal ID and digest as part of the exact sequenced operation. An inventory change, seal invalidation or late-discovered target that is ordered before the owner gate makes the old seal stale and blocks the operation. If an owner gate is ordered first, the decision must retain the exact seal snapshot and its validity basis for that operation; this does not waive later Global Forget reconciliation or late-discovery reopening.

Until I's authoritative inventory source, registry operator, signer/verifier, epoch/seal lifecycle and conformance are approved, inventory remains CANDIDATE/OPEN and any required missing or unverifiable seal keeps the operation BLOCKED/UNKNOWN. D's ProducerRegistrationHighWater/WorkItemBarrier remains a distinct mandatory proof and cannot be replaced by I's inventory epoch.

## 6. I-side required conformance evidence

The v2 JF10-01..08 and JF10-I-09..13 cases remain required. Add explicit evidence for:
- coordinator durable PREPARE and participant XID registration before I ordering;
- COMMIT/ABORT decision persistence boundary and exact sequencer position;
- conflicting revocation blocked while the participant is IN_DOUBT, then ordered after recovered COMMIT or allowed after recovered ABORT;
- receipt consumption and participant/XID binding atomically persisted exactly once;
- participant loss, database failover, coordinator failover, replica lag and restore without heuristic outcome;
- inventory epoch/seal invalidation racing the owner-final-gate operation;
- proof that a D fence cannot pass an unresolved prepared participant and that the D barrier cannot close early;
- same-key replay, changed digest/boundary/XID conflict, lost ACK and duplicate recovery.

All remain **SPECIFIED / NOT RUN**. Required evidence includes I coordinator log/decision position, participant prepare/commit/rollback trace, Storage transaction proof, D fence/barrier trace, receipt-consumption proof, inventory seal version, build/database/runtime identity, deterministic fault injection and independent owner review. No test PASS is asserted.

## 7. Multi-policy-domain disposition

**BLOCKED — NOT ACCEPTED BY THIS DECISION.**

The v2 statement that multi-policy-domain operations require all-or-none coordination is directionally correct but does not specify the coordinator topology, cross-domain prepare/reservation, global decision durability, lock/order discipline, partial failure recovery or revocation interaction across domains.

Until I publishes a separate normative multi-domain coordinator protocol and conformance plan, a JF-10 operation spanning more than one I policy domain MUST be rejected/paused as BLOCKED/UNKNOWN. It MUST NOT partially commit in one domain, obtain independent per-domain COMMIT_WON results, or proceed on a best-effort aggregate.

## 8. Remaining owner and gate status

| Item | I disposition | Remaining closure authority |
|---|---|---|
| JF-10 v2 single-policy-domain architecture | ACCEPTED WITH BINDING CLARIFICATIONS | D/E/Storage owner acceptance and implementation |
| Multi-policy-domain atomicity | BLOCKED | I to specify; D/E/Storage to consume and test |
| D fence/WorkItemBarrier serialization | I boundary requirement accepted; D decision not inferred | D Owner |
| Storage prepared-XID and atomic visibility transaction | Required; not implementation-approved | Storage Owner |
| E stable operation identity and receipt consumption | Required; not implementation-approved | E Owner |
| I sequencer/coordinator durability and recovery | Required; not implemented/verified | I implementation owner |
| ProducerDomainInventoryEpoch / InventorySeal | CANDIDATE / OPEN | I registry authority and required governance approvers |
| Global Forget Completion / CEV | CANDIDATE / OPEN | I + D/E/F/G/H/Storage + independent governance approvers |
| JF10-01..13 and added cases | SPECIFIED / NOT RUN | I/D/E/Storage test owners |
| I36-GOV-01..10 | GOVERNANCE-BLOCKED | Named authorized governance approvers |
| Fact/Claim ADR-001 | ADR-BLOCKED | Existing ADR authority; unchanged |

JF-10 therefore remains **P0 OPEN** pending owner acknowledgements, implementation, executable crash/recovery conformance and independent review. This addendum does not approve governance, activate production policy, select a concrete database engine/deployment profile, prove global inventory completeness, or claim Global Forget completion.

## 9. Requested next actions

- D: record explicit acceptance or amendments to §4's fence/registration/barrier serialization order.
- E: record explicit acceptance of stable PublicationOperationId/RequestDigest and non-terminal-until-Storage-receipt behavior.
- Storage: record explicit acceptance of durable prepared XID, coordinator-driven recovery, no heuristic outcome, and atomic visibility/receipt transaction; provide concrete DB capability/deployment evidence.
- I implementation owner: provide coordinator log, participant registry, authoritative lookup, retention, failover/restore and revocation-blocking evidence.
- I governance/registry authority: separately resolve ProducerDomainInventoryEpoch/InventorySeal and Global Forget approval dependencies.

Silence, shared Blob identity, or this architecture acceptance must not be interpreted as owner implementation acceptance or governance approval.
