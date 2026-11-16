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


## 10. I Owner formal decision — JF-10 prepared participant ↔ COC bridge

### 10.1 Exact versions reviewed

I reviewed the following exact artifacts together:

- A Causal Order Coordinator deployment architecture: `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md`, Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`.
- Common D/E/Storage JF-10 v2 prepared-participant proposal: original common proposal Blob `d544cc38a922b314e6dc45dd4db76aae6b47f5fc`; current D and Storage branch readbacks of the evolved shared recovery contract both Blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0`.
- Existing I JF-10 v2 disposition: Blob `b7b0287cde3922434a560fca90051cc5b418d987`.
- Applicable protocol profile: `CausalOrderProfile/1.0`; H transport target: `bmcp.applied-ack/1.1.0`.

### 10.2 Decision

**I DECISION: ACCEPT WITH BINDING BRIDGE AMENDMENTS — SINGLE I POLICY DOMAIN ONLY.**

I accepts the COC as the cross-owner causal-order log and durable participant-accounting/observation service, subject to the normative bridge below. I does **not** accept COC as a replacement for, replica of, or second writer for the I policy-domain sequencer. I's existing JF-10 decision remains binding: the I policy-domain sequencer is the durable decision coordinator for the prepared Storage participant/XID and the actual owner-final-gate COMMIT/ABORT decision.

This is a deliberate two-authority bridge, not two competing transaction coordinators:

- **COC:** orders cross-owner intents and request cutoffs; records the existence, identity and lifecycle of the JF-10 participant; preserves cross-owner causal references and recovery observations. It never decides the JF-10 XID COMMIT/ABORT.
- **I policy-domain sequencer:** alone consumes the single-use `CommitAuthorizationReceipt`, orders authorization against I revocation, and durably decides COMMIT/ABORT for the exact prepared participant/XID.
- **Storage:** alone executes the exact XID forward-commit or rollback and atomically publishes VisibilityPointer + PublicationReceipt + owner outcome + receipt-consumption evidence + outbox in its local transaction.
- **D:** alone owns ForgetFence, target/lineage registration and barrier/effective-fence semantics. COC positions do not mint D clearance or ForgetFenceGeneration.

The A COC proposal is therefore **not accepted as a complete JF-10 bridge without the amendments in §§10.3–10.8**. The bridge interface is accepted conditionally; deployment and JF-10 closure are not.

### 10.3 Required identity binding and prepare registration

One immutable JF-10 operation tuple MUST bind all of the following without lossy conversion:

- `CausalOrderCoordinatorRef`, `CausalOrderDomainRef`, COC epoch/index/entry digest;
- `CausalOrderTransactionRef` and `ParticipantIntentRef`;
- stable `PublicationOperationId`, canonical `RequestDigest`, exact `owner_boundary`;
- stable Storage participant identity, preallocated XID, participant digest and Canonical Authority DB identity;
- `PolicyDomainRef`, `PrincipalRef`, `ActorRef`, action, `ResourceRef`, purpose, audience, `ScopeBindingSet` digest, `EnvironmentRef`, delegation-chain digest;
- single-use `CommitAuthorizationReceiptRef`, `PermissionEpoch` and I sequencer identity/epoch/position;
- applicable `DForgetFenceRequestRef`, D target/source/ancestor lineage identity and D owner-predicate/clearance evidence;
- when required by effective I policy, authoritative `ProducerDomainInventoryEpoch` and `InventorySealReceiptRef` identity/digest.

Before Storage executes PREPARE, COC MUST durably append a `JF10_PREPARE_INTENT_REGISTERED` record containing the stable operation identity, preallocated XID, participant digest, owner boundary, policy domain, ParticipantIntentRef and exact COC position. This makes the prospective participant visible to any later D fence cutoff and I revocation cutoff even if Storage crashes during PREPARE.

Storage then durably prepares that exact XID, retains the required private bytes and target/lineage serialization locks, and returns an authenticated `PreparedParticipantReceipt` binding the same XID, participant digest, operation ID/digest, DB identity and prepare state. COC MUST append `JF10_PREPARED_PARTICIPANT_REGISTERED` with that Storage-signed receipt before I may decide the owner-final gate. A lost response is recovered by authoritative lookup of the same preallocated XID; no new XID or operation identity is minted on retry.

If COC becomes unavailable after the prepare-intent or after Storage PREPARE, the participant remains private, durable and locked. No I owner-final-gate decision is admitted until the required COC prefix and prepared-participant evidence can be read linearly. Recovery resumes the same XID.

### 10.4 I owner-final-gate decision and receipt consumption

The I owner-final-gate API MUST consume the exact COC-registered prepared participant. Before deciding, I MUST:

1. authenticate COC identity/profile and obtain a linearizable quorum-confirmed read of the exact COC intent, prepare registration and current relevant I/D cutoff prefix;
2. verify exact tuple equality across ParticipantIntentRef, PublicationOperationId, RequestDigest, owner_boundary, participant XID/digest, PolicyDomainRef and all security bindings;
3. validate the current I authorization tuple, PermissionEpoch and single-use CommitAuthorizationReceipt;
4. validate any policy-required authoritative InventorySealReceipt/ProducerDomainInventoryEpoch in I's own authoritative registry/sequencer path, not from a Storage-local cached copy;
5. apply I's own policy-domain sequencer order against revocation and durably persist, in one I coordinator transaction, receipt consumption + participant/XID binding + operation identity/digest + owner boundary + COC position/digest + terminal decision identity and I sequencer position.

The I sequencer is the sole source of I terminality. A COC position, COC reservation, H ACK or Storage PREPARE receipt alone is never an authorization decision. Conversely, a detached I preflight receipt consumption followed by a separate participant transaction is forbidden.

### 10.5 Terminal decision and recovery bridge

The only I terminal outcomes are:

- `COMMIT_WON`: I's durable sequencer decision commits the exact prepared XID before the conflicting revocation. Storage MUST forward-commit that same XID. COC later records the signed I terminal proof as an observed owner decision; that observation is not a second commit.
- `REVOCATION_WON`: I's sequencer orders the conflicting revocation first and durably decides ABORT for that exact XID. Storage MUST roll back the same XID and prove non-publication.
- `INDETERMINATE_ABORTED`: I durably decides non-success/ABORT because a safe winning order cannot be established. Storage MUST roll back and MUST NOT reinterpret it as COMMIT_WON.
- `UNKNOWN/IN_DOUBT`: no authoritative terminal decision is recoverably established. This is not terminal. Retain the prepared XID, private bytes and locks; block conflicting revocation progress and relevant D barrier completion; never infer an outcome from timeout, missing COC row, stale replica, process death or lost ACK.

After a durable I decision, the recovery direction is irrevocable: COMMIT means forward-commit the exact XID; ABORT means roll back the exact XID. Heuristic commit/abort, alternate-XID recovery, or reversing an I terminal decision is forbidden.

If I has durably committed COMMIT but COC is unavailable, Storage MUST still perform/recover the exact forward-commit. COC outage cannot reverse or suspend an already durable I decision. Once COC returns, it records the I-signed decision and Storage's exact PublicationReceipt/rollback proof through idempotent reconciliation. If I's decision is durable but Storage cannot recover the participant, remain blocked and escalate; do not rewrite I's decision.

### 10.6 Cross-log ordering and cutoff rules

COC and I sequencer positions are different typed orders and MUST NOT be numerically compared, lexically compared, merged into a synthetic total order, or substituted for one another. The bridge is the signed immutable tuple carrying both positions and digests.

- D fence cutoff before `JF10_PREPARE_INTENT_REGISTERED`: reject the prepare for the affected lineage; no Storage XID may be prepared.
- Prepare intent before D fence cutoff: D MUST register that prospective/prepared participant in its target/source/ancestor barrier. D cannot make the fence effective or close the barrier until I's exact ABORT/COMMIT and Storage's exact participant resolution are proven and all D lineage obligations are satisfied.
- I revocation cutoff before prepare intent: no affected prepare or receipt consumption is admitted.
- Prepare intent before revocation cutoff but no I terminal decision yet: I may order revocation first and return REVOCATION_WON/ABORT; Storage rolls back.
- I COMMIT_WON before a later revocation: revocation is pending behind that exact participant until Storage resolution and required D barrier accounting are durable. It cannot rewrite the decision.
- If I receives a revocation while COC is unavailable, I's owner-local pending gate remains durable and closed. It does not consume a new receipt or claim a cutoff order until COC records the request and recovery reconciles all earlier participants.
- If D receives a fence while COC is unavailable, D's owner-local pending gate remains durable and closed. It does not admit a later affected prepare or claim effective fence completion until COC records the cutoff and D reconciles all earlier participants.

### 10.7 Required COC bridge records and readback

The COC schema/API MUST add or normatively map these records (names may be aliased only through an explicit versioned mapping):

1. `JF10_PREPARE_INTENT_REGISTERED` — stable operation/XID identity, ParticipantIntentRef, digest, boundary, policy domain and pre-prepare COC position.
2. `JF10_PREPARED_PARTICIPANT_REGISTERED` — Storage-signed PreparedParticipantReceipt and exact XID/digest/DB identity.
3. `I_JF10_TERMINAL_DECISION_OBSERVED` — I-signed CommitAuthorizationReceipt consumption proof, IAuthorizationTerminalRef, decision ID, I sequencer position and same COC/XID/operation tuple.
4. `STORAGE_JF10_PARTICIPANT_RESOLVED` — same-XID commit or rollback proof; on commit, exact PublicationReceipt and visibility transaction identity; on abort, authoritative non-publication proof.
5. `JF10_BRIDGE_RECONCILIATION_RECORDED` — idempotent recovery observations linking COC prefix, I authoritative decision lookup, Storage XID state and D barrier state without synthesizing owner decisions.

COC read APIs MUST return the quorum-confirmed log prefix and all unresolved JF-10 participant registrations for the domain. I read APIs MUST return authoritative linearizable sequencer decision/receipt-consumption state. Storage read APIs MUST return authoritative same-XID prepared/committed/rolled-back state and PublicationReceipt. Stale replicas and caches are never decision sources.

### 10.8 Scope, rejection conditions and required proof

This decision covers only a single I PolicyDomainRef. Multi-policy-domain atomicity remains **BLOCKED / NOT ACCEPTED**; reject or pause such operations as BLOCKED/UNKNOWN. Independent per-domain COMMIT_WON results, partial commit and best-effort aggregation are forbidden.

The bridge MUST fail closed on: missing/unverifiable COC prefix; unregistered or mismatched XID; changed operation digest/boundary/security tuple; duplicate receipt consumption; stale PermissionEpoch or inventory seal; D fence cutoff that wins; unknown lineage; invalid owner signature; coordinator rollback/term reuse; ambiguous participant state; or inability to prove same-XID recovery.

Required new conformance cases (all SPECIFIED / NOT RUN):
- JF10-COC-01: crash after COC prepare-intent registration but before Storage PREPARE; retry uses same operation/XID identity.
- JF10-COC-02: crash after Storage PREPARE but before COC prepared-receipt append; authoritative same-XID lookup repairs the COC record; no second XID.
- JF10-COC-03: D cutoff races prepare-intent registration; exactly one COC order and correct D barrier membership.
- JF10-COC-04: I revocation cutoff races prepare-intent and I owner-final-gate; exactly one I terminal decision, no detached preflight.
- JF10-COC-05: I COMMIT durable, COC unavailable; Storage forward-commits same XID and later COC observation is idempotent.
- JF10-COC-06: I ABORT durable, COC unavailable; Storage rolls back same XID and later observation cannot change decision.
- JF10-COC-07: COC/I log positions differ, leader terms change and ACKs are lost; bridge preserves both typed positions and exact digests without synthetic comparison.
- JF10-COC-08: participant remains IN_DOUBT through I/COC/Storage restart, replica lag and restore; no TTL, heuristic resolution or barrier release.
- JF10-COC-09: Storage PublicationReceipt is durable but COC ACK is lost; authoritative readback records the same receipt, no duplicate visibility.
- JF10-COC-10: required InventorySeal invalidates before/after I owner-final-gate; I validates authoritative currentness and binds exact seal snapshot.

Evidence MUST include COC quorum log positions/digests, I sequencer terminal log/receipt-consumption proof, Storage database/XID transaction traces, D fence/barrier traces, exact build/schema/DB/runtime identities, deterministic fault-injection results and independent review. All cases remain NOT RUN; no runtime pass is claimed.

### 10.9 Formal status

I's formal decision is **ACCEPT WITH BINDING BRIDGE AMENDMENTS for the single-policy-domain JF-10 ↔ COC interface**. The A COC architecture requires the additions in §§10.3–10.7 before it can be considered fully reconciled with I's JF-10 protocol. This does not approve COC deployment, name a Storage operator, approve a concrete database engine, activate external governance, close InventorySeal/Global Forget, or establish implementation/conformance.

JF-10 remains **P0 OPEN**; I/COC/Storage/D conformance remains **SPECIFIED / NOT RUN**; multi-policy-domain atomicity remains **BLOCKED**; production implementation remains **NOT VERIFIED**.

## 11. I exact-version re-acceptance of amended A COC bridge

### 11.1 Exact artifact reviewed

I reviewed the amended A architecture:
- Path: `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md`
- Owner branch: `session-a-integration-2026-11-16`
- Exact Blob SHA: `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- Amendment commit: `78b811ee12499413d6e7a2e03ee5b36e6a0a2f38`
- Incorporated I bridge decision: this artifact §12, including §§12.1–12.8.

### 11.2 Formal I decision

**I DECISION: ACCEPT — EXACT A BLOB a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d, WITH THE BINDING SINGLE-POLICY-DOMAIN LIMITATION.**

I confirms that A §12 now incorporates the material bridge requirements of I §10: COC is an ordering/participant-observation authority and not the JF-10 COMMIT/ABORT decision maker; I's policy-domain sequencer remains the sole durable terminal decision authority; Storage resolves the exact same prepared XID; D retains exclusive ForgetFence/barrier authority; COC and I positions remain distinct typed orders; and the five JF-10 bridge record families and ten JF10-COC conformance cases are specified.

This acceptance is limited to the architecture interface and exact Blob above. It does not waive any requirement in I §10, and does not imply implementation, deployment, operational custody, conformance, governance approval, or production activation.

### 11.3 Conditions and retained blocks

- Scope remains one I PolicyDomainRef. Multi-policy-domain atomicity remains **BLOCKED / NOT ACCEPTED**.
- D must independently accept the prospective participant's fence/barrier membership and cutoff ordering.
- Storage must independently accept durable preallocated-XID preparation, signed PreparedParticipantReceipt, exact-XID recovery and atomic publication/rollback evidence.
- H must decide any required versioned 1.1.0 wire/schema mapping; A's naming of records is not an H schema approval.
- COC-01..12 and JF10-COC-01..10 remain **SPECIFIED / NOT RUN**.
- I sequencer durability, receipt-consumption atomicity, failover/restore and Storage same-XID execution remain **NOT VERIFIED**.
- JF-10 remains **P0 OPEN**. No production or deployment approval is granted.

This exact-version acceptance supersedes no Owner's independent implementation or governance gate. Any material change to A §12 requires renewed I review against the new Blob SHA.
