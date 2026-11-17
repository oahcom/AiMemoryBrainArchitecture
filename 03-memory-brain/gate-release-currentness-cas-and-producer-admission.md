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
