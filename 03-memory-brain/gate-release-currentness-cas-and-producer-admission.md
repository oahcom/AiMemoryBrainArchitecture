# Canonical Gate Release Currentness CAS and Producer Admission Proof
# Canonical Gate Release 当前性 CAS 与 Producer Admission 证明

**Owner:** D — Memory Brain Architect  
**Status:** PROPOSED D-owned canonical semantics; I governance mapping and Storage realization OPEN.  
**Related:** forget-fence-and-completion-contract.md; commit-cursor-semantics.md.

## 1. Purpose / 目的

D must prove that a Canonical Producer Gate release is current when it becomes effective, and every admitted work item is accounted for when a Forget fence closes admission.

Invariant: no publication-capable producer work may be admitted unless its admission is durably registered in the same linearizable ordering domain as Forget-fence installation/closure. No release may commit against stale fence, producer inventory, dependency inventory or authorization state.

## 2. Typed currentness snapshot / 强类型当前性快照

CanonicalGateCurrentnessVector MUST bind:
- canonical_authority_id, producer_gate_id and gate_revision;
- producer_class_id, producer registry version and registry digest;
- exact source Memory refs/revisions and complete lineage digest;
- target-set digest and ScopeRefs;
- applicable ForgetOperationId and latest ForgetFenceCursor/generation for every source lineage member, or an authority-issued fence-snapshot digest;
- dependency-inventory revision/digest;
- producer registration sequence high-water and unresolved-work summary;
- CanonicalCommitCursor/snapshot cursor assumptions;
- I authorization-decision reference, PermissionEpoch and policy revision;
- proposal ID, nonce, schema/profile version and expiry.

CanonicalCommitCursor, ForgetFenceGeneration, PermissionEpoch, ProducerRegistrationSequence, registry version, dependency-inventory revision and GateRevision are distinct typed namespaces. Unknown latest fence state for any lineage member means fail closed.

## 3. Prepare and final Currentness CAS / Prepare 与最终 CAS

Prepare reads the authoritative vector and emits an immutable proposal; it does not open the gate or authorize work.

CommitCanonicalGateRelease(proposal_id, expected_gate_revision, expected_vector_digest) MUST be a single linearizable CAS serialized with RegisterProducerWork, InstallForgetFence, CloseCanonicalProducerGate and relevant producer-registry/dependency-inventory mutations.

At commit it compares gate state/revision, producer registry version/digest, dependency inventory revision/digest, latest applicable fences and target digests, registration high-water/unresolved work, canonical authority/cursor assumptions, I decision/PermissionEpoch/policy revision, scope/lineage digests, expiry and one-use nonce. Success atomically changes gate state/revision and persists CanonicalGateReleaseReceipt binding the complete vector/evidence digests. Any mismatch returns typed CURRENTNESS_CONFLICT and leaves the gate closed. No silent rebase. Checking only GateRevision or ForgetFenceGeneration is insufficient.

## 4. Producer Admission / Producer 在途准入

RegisterProducerWork is the admission operation; queue insertion or lease acquisition is not.

It atomically verifies OPEN gate and expected revision, latest fence for every source/ancestor, current I authorization, exact source revisions/scope/target digest, then allocates monotonic ProducerRegistrationSequence and durably persists WorkItemId, AttemptId, producer class, source refs/revisions, lineage digest, scope, idempotency/request digest, gate/release receipt, observed fence vector, PermissionEpoch and status. The in-flight ledger increment and registration receipt are atomic.

Registration commit is the admission linearization point. No extraction, transformation, replay, lease ownership or publication-capable processing starts before durable registration.

If registration wins against fence installation, its sequence is included in the immutable producer_registration_barrier. If fence installation wins, ordinary work for covered lineage is rejected/quarantined; only explicitly typed cleanup work may be admitted, and it cannot publish.

## 5. In-flight terminal dispositions / 在途终态

An admission remains in-flight until a durable disposition proves one of:
- COMMITTED_VISIBLE: dependency edges were registered before visibility and final publication CAS validated current fence and permission;
- CANCELLED_NO_PUBLISH;
- SUPPRESSED_QUARANTINED;
- FAILED_PARKED with publication disabled;
- RESOLVED_BY_RECONCILIATION proving one of the above.

LEASE_EXPIRED, QUEUE_DELETED, WORKER_LOST, RETRY_SCHEDULED, DLQ_PARKED and TIMEOUT are not terminal. Retries preserve source lineage and are registered as linked attempts/work. They never renew publication rights; every replay rechecks current fence and permission.

## 6. Fence capture and publication / Fence 捕获与发布

RegisterProducerWork and InstallForgetFence share one linearizable ordering domain. Fence installation atomically captures producer-registration high-water and closed-world producer registry version for the covered target lineage.

- Registration sequence at or below captured high-water: pre-fence work, included in barrier.
- Fence installation first: ordinary admission rejected/quarantined.
- Unregistered work capable of publishing is forbidden.
- Unknown producer class, sequence gap, unresolved attempt or untracked side channel blocks barrier closure.
- Producer-registry updates racing fence capture serialize; a new class is included or fence capture fails closed.

Pre-fence admission is not publication permission. PublishDerivedIfCurrent atomically validates work/attempt registration, complete durable dependency edges, source lineage, scope, latest ForgetFence, current I PermissionEpoch/decision, expected canonical revision and gate policy at the same visibility boundary that makes the artifact retrievable/indexable/deliverable. Check-then-write and cached tokens are insufficient. Unknown currentness leaves output private/quarantined.

## 7. Proof bundle / 证明包

CanonicalProducerAdmissionProof binds release receipt/vector digest, registry version/digest, captured registration high-water, every pre-fence admission or contiguous sequence range, terminal disposition receipts, dependency-inventory revision, derivative registration receipts, final publication CAS or non-publication outcome, latest fence/target digest and I decision/PermissionEpoch. It proves no gaps, unknown classes, unresolved work or untracked publication path. It contains identifiers/digests, never forgotten plaintext.

## 8. Race matrix / 竞争测试

1. Fence advances between release Prepare and Commit: CAS fails.
2. Producer registry/inventory changes between Prepare and Commit: CAS fails.
3. Release commit races producer admission: either admission is registered under committed OPEN revision or rejected.
4. Admission races fence installation: exactly one order; included in barrier or rejected.
5. New producer class races fence capture: included or capture fails closed.
6. Queue insertion before registration cannot start work.
7. Lease expires while work remains: barrier remains open.
8. Retry/DLQ/replay races fence: final publication rechecks current fence.
9. Fence advances after expensive processing: final visibility CAS rejects.
10. Dependency registration cannot lag artifact visibility.
11. Crash after registration: recovery discovers and resolves in-flight record.
12. Crash after staging: output remains private pending currentness.
13. Crash after commit before response: idempotent resolution returns original outcome.
14. Unknown class, sequence gap or side channel blocks proof.
15. Late derivative discovery invalidates prior closed-world proof and reopens reconciliation.

## 9. Ownership and status / Owner 与状态

D owns canonical gate, producer registration ordering, fence snapshot/high-water, dependency barrier and canonical proof semantics. I owns authorization, PermissionEpoch, policy, exception and global Forget criteria. E/F/G/H own their producer-specific admission and terminal evidence. Storage/Consistency must prove the linearizable/crash-recovery realization. C Provider Egress Gate is a separate boundary; D producer admission never authorizes network egress.

**PROPOSED.** No Storage realization, executable tests or end-to-end Forget completion is claimed.


## 10. Cross-authority PermissionEpoch validation / 跨权威 PermissionEpoch 校验

D cannot claim a single atomic CAS over an I-owned PermissionEpoch when D and I use independent authorities. A D-local transaction that merely reads an I decision and later commits is a TOCTOU race.

The implementation MUST use either a shared linearizable sequencer, a proven distributed transaction/consensus protocol, or an I-owned revocation barrier/fencing protocol. Under the barrier profile, I revocation is PENDING until every D/E/F/G/H/C enforcement point required by the closed-world inventory has durably installed the newer PermissionEpoch/fence and acknowledged that older permits are rejected. Only then may I mark the revocation EFFECTIVE. D's producer admission and final visibility commit must reject any fencing epoch below the latest installed epoch at that same local linearization point.

A bounded authorization lease is permitted only as a separately named weaker policy profile with explicit maximum stale window and clock/partition assumptions; it is not immediate revocation. If D cannot establish current permission/fencing epoch, producer admission and publication fail closed.


## 11. Controlling alignment with D Phase 3.6.7–3.8

**This section is a controlling alignment note.** The detailed D Forget Gate and publication semantics remain in the existing owner contracts phase-3.6.7-d-owner-local-gate-admission-release-amendment.md, phase-3.6.8-d-cross-boundary-fencing-terminalization-amendment.md, phase-3.7-d-producer-class-registry-eventref-ingress-and-participant-intent.md, and phase-3.8-d-publication-participant-and-terminal-contract.md. This document MUST NOT create a second D gate, second D receipt family or alternate admission order.

### 11.1 D-local currentness CAS only

D's final DGateRelease CAS is linearizable only over D-owned state: D Gate ref/revision, ForgetOperationRef, ForgetFenceGeneration, D request/work/producer/publication high-waters, D barrier snapshot generation/root, D producer-registry projection and D anti-rollback anchor. It atomically revalidates those values and writes the D-signed DGateReleaseReceipt only after all D-local release predicates are satisfied.

I ProducerDomainInventoryEpoch, I IGateGeneration and PermissionEpoch are not D counters and are never compared numerically or claimed to be atomically mutated by D. D binds exact I-signed current inventory/authorization proof refs, digests, relevant entry mappings and policy decision identity in a DReconciliationTuple. Missing, stale, contradictory or unverifiable I evidence blocks D release. If a newer I inventory epoch reveals a previously omitted producer/work mapping, D reopens the affected barrier and invalidates the prior snapshot/closure proof.

D outage-gate release is typed OUTAGE_ADMISSION_RELEASE_ONLY. It does not clear the effective Forget Fence, authorize protected source dereference, grant I permission or authorize provider egress. Every protected read, admission and final publication boundary still enforces current D Fence and applicable I authorization. The I COMMIT_WON/REVOCATION_WON decision is consumed only for the exact operation and cannot be inferred from a D receipt.

### 11.2 Canonical derivative publication order

For canonical derivative visibility, the controlling Phase 3.8 order is:
1. E/producer prepares immutable private stage and complete dependency evidence.
2. Storage persists exact StorageVisibilityParticipantRef as PREPARED_HIDDEN; no read path can expose it.
3. D admits exact PublicationParticipantRef in the D Fence/Barrier domain, bound to the exact Storage participant, request/tuple digest, WorkItem, lineage, scope, attempt/lease and complete dependencies.
4. I consumes a single-use CommitAuthorizationReceipt in its own PolicyDomain Sequencer, bound to the same immutable operation and both exact participant refs.
5. Storage final visibility transaction verifies current D participant/fence and the consumed I proof and atomically commits visibility pointer, immutable outcome/receipt and outbox.
6. D and I terminalize their own participants only after authoritative Storage outcome readback.

D admission is an ordering hold, not visibility permission. UNKNOWN/IN_DOUBT remains private and keeps the relevant barriers open. The physical D/Storage serialization topology remains ADR-BLOCKED until Storage T1–T8 are evidenced; this semantic contract does not select a database or claim runtime atomicity.

### 11.3 D admission race and release proof

RegisterProducerWork and InstallForgetFence remain one D-authoritative ordering domain. Fence-first rejects/quarantines affected later work; registration-first includes the durable registration in the captured barrier. The D snapshot must include registered work even if COC registration/ACK is absent, plus exact producer/work high-waters and complete member root. Late-discovered pre-fence work reopens the barrier; unknown ordering is UNKNOWN, never resolved by wall-clock timestamps.

A D terminal disposition is accepted only with authoritative proof: PUBLISHED_BEFORE_FENCE, CANCELLED_NO_OUTPUT, SUPPRESSED_QUARANTINED or FAILED_PARKED_NO_PUBLISH under the existing D contract. Lease expiry, queue deletion, worker loss, timeout, DLQ or missing COC row is not terminal. D release is invalidated by any high-water/root/registry/lineage/anti-rollback change before commit.

### 11.4 Required cross-owner conformance

1. Fence CAS wins before RegisterProducerWork: no protected admission/execute/publish.
2. RegisterProducerWork wins: exact receipt and sequence are in the immutable fence barrier despite lost caller/COC ACK.
3. New I inventory epoch reveals a pre-fence producer: D reopens the barrier.
4. Storage hidden participant exists but D admission fails: participant remains private and resolvable by same ID/digest.
5. D admission succeeds but Storage participant cannot be read back: UNKNOWN/integrity incident; never abort by assumption.
6. I REVOCATION_WON: Storage cannot publish; prove NO_PUBLICATION.
7. I COMMIT_WON: exact participant remains in-flight until Storage terminal outcome.
8. D fence advances after expensive work but before visibility: final Storage visibility CAS rejects stale D participant/fence.
9. Restore replays stale work: D Gate remains closed until current Fence/high-waters and Storage/I evidence reconcile.
10. D release candidate becomes stale before final local CAS: reject and rebuild snapshot.

**Disposition:** D semantic alignment is specified against the controlling Phase 3.6.7–3.8 contracts. Storage topology, I proof interoperability, callable API, executable race tests and independent D acceptance remain OPEN. No physical linearizability or Forget completion is claimed.

### 中文规范摘要

D 的 Gate Release 仅对 D 自己的 Gate/Fence/High-water/Barrier/Registry/Anti-rollback 状态执行最终 CAS；I 的 Epoch 不属于 D 的计数器，只能通过 I 签名的精确证明和 DReconciliationTuple 关联。D 的 outage release 不清除 Forget Fence，也不授权 I、C 或 Storage 的操作。Canonical derivative 发布严格遵循 Storage 隐藏 Prepare → D PublicationParticipant Admission → I 单次 CommitAuthorizationReceipt 消费 → Storage 最终 Visibility Commit → D/I 各自终态化。D/Storage 物理事务域仍受 Storage ADR 阻塞。
