# Phase 3.6.1 — Storage Joint Defect Closure Addendum

- Authority: user-delegated DE-S Joint Architect; Storage realization semantics
- Status: **LOGICAL REALIZATION CONTRACT RECORDED / DEPLOYMENT AND IMPLEMENTATION NOT VERIFIED**
- Applies with and refines `phase-3.6-joint-durable-atomicity-decision.md`.

## 1. JF-01 — Persist independent inventory dimensions

Persist and bind, without conflation:
- I `ProducerDomainInventoryEpoch` + inventory digest + InventorySealReceipt;
- D `ProducerRegistryVersion`;
- D `ProducerRegistrationHighWater`;
- D `ForgetFenceGeneration`.

FenceSnapshotReceipt must immutably bind all values, ForgetOperationId, target-set digest, authority ID and commit cursor. Storage enforces referential integrity and monotonicity; it cannot manufacture I's inventory seal. Missing, stale or mismatched inventory evidence blocks closed-world barrier completion.

## 2. JF-02 — Authorization commit freshness

The physical commit must consume a verifiable I AuthorizationCommitPermit bound to exact principal/action/resource/scope/lineage/work/attempt/lease/dependency/fence values, PermissionEpoch, revocation watermark, policy version, audience, expiry and nonce.

The deployment must provide a revocation-vs-publication serialization guarantee: same atomic authority, or an I-issued linearizable commit fencing grant whose validity cannot overlap an effective revocation, or an equivalently proven distributed commit protocol. A plain signed snapshot with an unchecked expiry is insufficient if revocation can take effect before visibility commit. If no such protocol exists, final commit is denied. Storage records the permit ID/epoch/watermark in PublicationReceipt but does not decide I policy.

## 3. JF-03 — Output manifest durability

Add immutable `OutputManifest` and `OutputManifestVersion` records keyed by root WorkItemId, with digest, declared output slots/ArtifactIds, expected cardinality or closed-discovery marker, child WorkItems and frozen status. Unique constraints prevent mutation of a frozen version. A changed output set creates a new version and invalidates prior completeness/terminal receipts.

Dependency registration is complete only for the exact frozen manifest version/digest. Each ArtifactId has its own visibility commit; root terminality is a separate transaction requiring all final-manifest outputs, descendants and attempts to be terminal and no unresolved commit outcome. Do not require simultaneous multi-artifact visibility unless a separate product contract explicitly demands it.

## 4. JF-04 — Outcome-unknown protocol and receipt lookup

Every mutating operation persists idempotency key, immutable request digest, operation state and receipt in its linearization domain. Provide an authoritative linearizable `GetOperationOutcome(key,digest)` returning exactly one of:
- `COMMITTED(receipt, commitCursor)`;
- `REJECTED(rejectionReceipt, commitCursor)`;
- `NOT_COMMITTED(proof/authoritative absence at a read barrier)`;
- `UNKNOWN` when safe resolution is not currently possible.

A transport timeout is always UNKNOWN. Retry is allowed only with the same key/digest after NOT_COMMITTED or as an idempotent replay. Same key/different digest is CONFLICT. The API must not report NOT_COMMITTED from a stale replica or before the read barrier has passed the operation's possible commit point. Unknown state blocks terminality and publication acknowledgement.

## 5. JF-05 — Reader and materialization consistency

The authoritative visibility pointer/record is the sole publication authority. Every query, retrieval, reference-resolution, index, cache, materialized view, export and downstream read must either:
- perform a linearizable visibility/fence/authorization check at the read's response-finalization point; or
- consume a formally fenced snapshot/token whose validity is guaranteed through response finalization and is invalidated/serialized against fence installation.

Asynchronous invalidation alone is insufficient. Indexes may return candidate IDs but final response filtering must revalidate current authority. Stale replicas must not answer safety decisions. If authority is unavailable, affected results are omitted/denied. Cache keys and index generations include authority, scope and fence generation, but generation-keying alone does not replace final validation.

## 6. JF-06 — Restore monotonicity and service gate

The authoritative Forget control ledger must survive independently of ordinary artifact snapshot rollback, or be replayed from a durable monotonic log with verified continuity. Restore procedure:
1. enter RecoveryQuarantined; disable reads of affected artifacts and all publication;
2. restore data and control records into isolated state;
3. obtain authoritative control-ledger watermark and replay through it;
4. reconcile ForgetOperation, FenceGeneration, InventorySeal, barrier snapshots/high-waters, work/lease/attempt, output manifests, dependency registrations, visibility/publication receipts, terminal receipts and I permission/revocation watermark references;
5. verify no generation/cursor regression, missing receipt, digest mismatch or stale visible pointer;
6. issue immutable RecoveryReconciliationReceipt;
7. only then reopen read/publication traffic.

If continuity cannot be proven, remain quarantined. Restoring old artifacts without newer Forget control state must never make them visible.

## 7. Required durable constraints and operation ordering

The selected logical coordinator must enforce:
- uniqueness of idempotency keys and immutable request digests;
- monotonic fence, registry, inventory and lease generations;
- complete dependency set tied to frozen manifest version;
- atomic authoritative visibility transition plus PublicationReceipt;
- durable terminal disposition only after all outputs/attempts and unknown outcomes resolve;
- idempotent recovery lookup for every commit whose ACK can be lost;
- restore watermark barrier before serving.

The single-transaction model is selected only if the actual D ledger and visibility authority share one atomic serialization domain. Otherwise the deployment must supply the durable coordinator protocol above, including participant recovery and final current-fence/authorization validation. No vendor or topology is assumed.

## 8. Verification boundary

C01–C20 plus explicit authorization-revocation race, manifest-mutation race, read-response-vs-fence race, outcome-unknown recovery, and restore rollback tests are required. Record engine/version/configuration, isolation/replication settings, deterministic seeds, commit/lock/CAS traces, receipt IDs, read snapshots and recovery logs. None have been run. Storage deployment selection, production configuration and fault-injection evidence remain OPEN; no Implementation Verified or Production Ready claim is permitted.


## 9. Round-1 self-review closure — JF-07 / JF-08

### JF-07 — Serialize output-manifest transitions with terminality

The coordinator's linearized operation set MUST include output declaration, close-discovery, manifest freeze, manifest reopen/version advance and root terminal disposition. A frozen manifest version is immutable. Freeze/reopen operations carry a WorkItemId, version, digest and idempotency key and are admitted only while the root is non-terminal. Terminal disposition conditionally commits against the exact frozen version/digest and proves no pending manifest mutation, child registration or unknown outcome exists. If mutation commits first, terminalization cannot commit against the old version; if terminalization commits first, later mutation is rejected. Any later independent work must be registered as a linked child obligation. This removes the post-terminal output race.

### JF-08 — Outcome absence must be linearizably proven

`GetOperationOutcome` may return NOT_COMMITTED only after a decision barrier ordered after the operation's possible commit point, resolving any in-flight transaction, coordinator decision and participant prepare/commit record for that key. Return the barrier cursor/epoch and durable proof reference with NOT_COMMITTED. An absent row on a lagging replica, a query racing an in-flight transaction, timeout or unavailable coordinator returns UNKNOWN. If a participant outcome is unresolved, the coordinator must preserve prepared state as hidden and keep the operation UNKNOWN; it must not guess abort. This barrier rule applies to registration, fence, dependency, publication and terminal operations.


### JF-09 — Gate commit compares current inventory seal and manifest version

The visibility transaction MUST compare the exact current frozen OutputManifestVersion/digest and applicable current InventorySealReceipt / ProducerDomainInventoryEpoch against the values bound to dependency registration and the publication request. These checks occur inside the visibility linearization boundary. A manifest reopen/version advance or inventory epoch advance before commit makes the old dependency receipt/gate stale and the artifact remains private until refreshed evidence is committed. This comparison is separate from, and in addition to, fence generation, PermissionEpoch permit, WorkItem/Attempt/Lease and dependency digest validation.
