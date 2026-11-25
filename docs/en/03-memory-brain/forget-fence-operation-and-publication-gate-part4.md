# Forget Fence Atomicity — Part 4: JF-10 / COC Owner Decisions

- Document ID: D-FORGET-GATE-001-P4
- Source revision: d3ddfff9500d9138d643989e8496d99b8d9ed79e
- Source: [canonical D source](../../../03-memory-brain/forget-fence-operation-and-publication-gate.md) (source commit `b525e1f8fee2471a131e4a38efda99804045e424`; original source blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`).
- Chinese counterpart: [第 4 部分 — JF-10 / COC Owner 决议](../../zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate-part4.md)

## Phase 3.6.2 — D owner acceptance of revised JF-10 v2

**Status: D ACCEPTS THE D-OWNED SERIALIZATION AND FENCE PREDICATES IN THE DE-S v2 PROPOSAL; I ACCEPTANCE AND IMPLEMENTATION REMAIN OPEN.**

D confirms the following as normative D-side requirements for the proposed owner-gate-participating 2PC protocol:

1. D's ForgetOperation, ForgetFence, ProducerClass/ProducerWork ledger, Dependency inventory, BarrierSnapshotReceipt and canonical suppression proof remain D-owned.
2. For each Canonical Memory Authority, RegisterProducerWork, RegisterDerivedDependency, InstallForgetFence and the Storage publication participant serialize on the same durable authority/target-lineage ordering rows. The fence transaction atomically persists its strictly increasing FenceGeneration, immutable target digest, ProducerRegistryVersion, ProducerRegistrationHighWater, BarrierSnapshotReceipt and installation CanonicalCommitCursor.
3. ProducerRegistrationHighWater is scoped to the ProducerWork registration ledger for that Canonical Memory Authority. CanonicalCommitCursor is a separate per-Brain-authority commit-order/audit cursor. Neither is interchangeable with FenceGeneration, PermissionEpoch or I ProducerDomainInventoryEpoch.
4. A prepared Storage participant retains the D fence/lineage serialization locks until I's durable coordinator decision is recovered and the Storage participant commits or aborts. Fence-first means publication prepare rejects; participant-first means fence installation cannot pass the unresolved participant. A timeout is UNKNOWN, not permission to publish or close a barrier.
5. The D final predicate rechecks every source ancestor and target, exact dependency completeness, WorkItem/Attempt/Lease fencing and the latest applicable fence at the participant boundary. I COMMIT_WON never overrides a D fence.
6. ForgetOperation phases remain Requested, FenceEstablished, InventoryOpen, BarrierDraining, TargetReconciliation, CanonicalSuppressionComplete, Blocked and Failed. D may declare CanonicalSuppressionComplete only when its own captured barrier is terminal, all required D-domain targets have suppression proof or an exact I-approved residual exception, and no D-owned unknown/gap/late derivative remains. This is not I Global Forget Completion or physical erasure.
7. A late derivative, newly discovered producer, registry gap or restored stale task invalidates/reopens the relevant D proof and creates an audited reconciliation obligation; it never silently reuses a prior completion checkpoint.

D accepts the v2 protocol only as a proposed cross-authority design subject to I's exact owner-gate review. D does not define I's sequencer implementation, approve I inventory/authorization/exception policy, select a concrete database engine, or claim runtime conformance.


### D36 §9 rows 11–13 — offline rejoin, inventory epoch change and stale task recovery

| Source ID | Test name | Required result | Status |
|---|---|---|---|
| D36 §9 row 11 | Offline producer rejoin after fence | Rejoining worker resolves its original registered WorkItemId and current fence before source access; stale task is rejected/quarantined; offline/unknown producer evidence does not close I global inventory | NOT RUN |
| D36 §9 row 12 | I inventory epoch changes during Forget | D's local ProducerRegistrationHighWater remains unchanged; I seal becomes stale/reopened; no global completion until I issues a replacement seal and all newly applicable targets are reconciled | NOT RUN |
| D36 §9 row 13 | Old Compiler task resumes after CanonicalSuppressionComplete | Current D fence suppresses it before publication; stable WorkItemId/lineage is preserved; any late derivative invalidates/reopens prior D proof and is audited | NOT RUN |

These cases extend the original D36 §9 matrix; they do not renumber or weaken rows 1–10.


## Phase 3.6.2 — D confirmation of Forget ordering at the Applied submission boundary

D reviewed A's pinned C/G/H Applied Contract package (Blob SHA `61d961c32138fd875069e8cbac4696bb031447c0`) and confirms the following D-owned semantics:

1. D issues and validates the authoritative ForgetOperation/Fence identity, generation/cursor, target digest and lineage coverage. A consumer must resolve the latest applicable fence for every relevant source ancestor and target; an observed token without complete lineage/currentness proof is insufficient.
2. The final request submission boundary is a protected disclosure boundary. The applicable D fence must be checked in a causal/linearizable ordering with the actual submit event, not inferred by comparing opaque token values or independent wall-clock timestamps.
3. If the successful submit is ordered before the applicable fence installation, D's later fence does not rewrite that historical submit fact; G may retain a historically valid Applied fact only if C's immutable submit evidence and I's authorization ordering are independently proven. Current-use eligibility is immediately invalidated by the fence.
4. If fence installation is ordered before submit, the request is stale/ineligible and must not be promoted to Full Applied; the managed region remains suppressed.
5. If submit/fence ordering, lineage coverage or fence currentness is unknown or incomparable, the result is Unknown and suppressed. No Full Applied promotion is permitted.
6. A D fence receipt proves only D-owned fence/lineage facts. It does not prove I authorization, H Adapter purge, G Applied, global Forget completion, backup deletion or physical erasure.
7. A committed fence/suppression obligation is not rolled back by later requester revocation; subsequent cleanup must proceed under a currently authorized I service/continuity principal. D does not define or approve that I principal policy.

**D disposition:** **APPROVE D-OWNED FENCE/LINEAGE SEMANTICS WITH AUTHORITY RESERVATIONS** for the exact A package. I authorization and D/E/Storage executable linearization remain separate blockers. D36 and DE-S fault/race suites remain **SPECIFIED / NOT RUN**; no implementation or end-to-end completion is claimed.

## Phase 3.6.2 — D exact-version acceptance of JF-10 prepared participant ↔ COC bridge

**Reviewed exact A artifact:** `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md`, A branch `session-a-integration-2026-11-16`, Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`, §12.1–12.8.

**D DECISION: ACCEPT — D-OWNED FENCE/BARRIER SEMANTICS FOR THIS EXACT A BLOB, WITH AUTHORITY RESERVATIONS.**

D accepts the bridge's prospective-participant ordering and barrier requirements as consistent with D's existing fence contract, subject to these binding D interpretations:

1. A quorum-committed `JF10_PREPARE_INTENT_REGISTERED` before a D fence cutoff makes the prospective participant a member of the affected target/source/ancestor barrier, even if Storage PREPARE or the signed prepared receipt has not yet been registered.
2. A D fence cutoff ordered before prepare-intent registration rejects the affected prepare; no Storage XID may be prepared for that lineage.
3. D retains exclusive authority over ForgetOperation, ForgetFence, target/lineage registration, ProducerRegistrationHighWater, BarrierSnapshotReceipt, D fence generation and effective-fence/suppression completion. COC records and positions are evidence of cross-owner ordering; they do not mint D state or clear D obligations.
4. A pre-cutoff participant remains in the D barrier until the I sequencer's exact terminal decision and Storage's same-XID commit/rollback resolution are authoritatively proven and all D lineage obligations are satisfied.
5. An unresolved or ambiguous participant keeps the barrier open. COC/I/Storage outage, timeout, missing row, stale replica or lost ACK cannot release the participant or permit effective fence completion.
6. D and COC positions are typed, separate orders. D does not compare opaque values or infer order from wall-clock time; D consumes the authenticated bridge tuple and its own canonical fence/lineage evidence.

This is D's exact-version architecture acceptance for D-owned fence/barrier semantics only. It does not approve I's sequencer implementation, Storage's database/XA capability, COC deployment/operator, H schema, implementation, conformance or production activation. D36 and JF10-COC-01..10 remain NOT RUN. JF-10 remains P0 OPEN; multi-policy-domain atomicity remains BLOCKED.


## Phase 3.6.2 — D exact acceptance of complete JF-10 ↔ COC decision bundle

**Decision:** **ACCEPT WITH ENUMERATED EXCEPTIONS**, limited strictly to D-owned ForgetFence, producer registration, dependency inventory, lineage and barrier semantics for the single-I-PolicyDomain JF-10 v2 profile. This decision is not I authorization approval, Storage capability certification, C provider approval, H production schema freeze, or production implementation acceptance.

### Exact bundle reviewed
- A COC architecture: `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- I JF-10 v2 Owner disposition: `8069ff86988396442c8d9dc3fd58653683abe2f3`
- D/E/Storage common JF-10 v2 recovery protocol: `94679897e84a6f58fd8b9467b5249e1a885cb0b0`
- C bridge Owner contract: `45a48249717c8cddb07ab96197730ef93d406c22`
- D fence/barrier Owner contract: `5a56c406578fdf257509315eb3f6f3f75456116c`
- Storage realization / participant contract: `55c01f4512f2e3d8aac767dd004e768ae073178e`
- H bridge wire mapping Owner contract (current branch readback): `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`
- H JSON Schema candidate: `a8a945cc3623c2907003b93625e3c79742150944`

### D-owned accepted semantics
1. A quorum-committed COC prepare-intent registered before the D fence cutoff is a prospective D barrier participant, even before Storage's prepared receipt is registered. A D cutoff before prepare-intent rejects the affected prepare.
2. The same preallocated XID/participant identity remains bound through Storage PREPARE, I terminal decision and same-XID commit/rollback resolution. A changed XID, digest, owner boundary or lineage binding is a conflict.
3. Participant-first retains D target/lineage serialization and keeps the D barrier open until I terminal evidence, Storage same-XID resolution, C provider outcome where required, and D lineage obligations are authoritative. Fence-first rejects. There is no third order.
4. UNKNOWN/IN_DOUBT, COC outage, missing log prefix, stale replica, lost ACK, missing participant row or incomplete owner proof cannot release the barrier or establish CanonicalSuppressionComplete.
5. D retains sole authority over ForgetOperation, ForgetFence, ProducerRegistrationHighWater, BarrierSnapshotReceipt, target/ancestor coverage and D completion. COC/I/Storage positions are distinct typed evidence; D does not compare them or infer order from wall-clock time.
6. The outage recovery batch and owner-local pending-gate rules are accepted only as fail-closed coordination evidence. D may reopen its local gate only after durable cutoff, complete pre-batch participant reconciliation and D owner high-water verification.
7. Acceptance is limited to one I PolicyDomain. Multi-PolicyDomain atomicity remains BLOCKED / NOT ACCEPTED.

### Enumerated exceptions / closure conditions
- This is architecture/interface acceptance only. D APIs, durable ledger, locks, participant recovery, COC deployment and production conformance are NOT VERIFIED.
- Storage must prove the selected DB's actual prepared-XID/lock retention, same-XID restart/failover recovery and atomic visibility transaction. D does not select or certify a DB engine.
- I owns the sequencer, receipt consumption, PermissionEpoch and revocation effective point; D's acceptance does not certify I implementation or external governance.
- C provider idempotency/outcome, H generated schema/parser/SDK interoperability, and COC consensus/quorum durability remain separately owned and unverified.
- D36, JF10-01..13, Storage crash/fault and cross-owner conformance remain NOT RUN. JF-10 P0 remains OPEN; no production activation or merge is authorized.
