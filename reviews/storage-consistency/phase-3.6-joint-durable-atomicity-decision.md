# Phase 3.6 — Storage Joint Architecture Decision: Durable Forget Atomicity

- Decision authority: user-delegated DE-S Joint Architect (ChatGPT acting across D, E and Storage)
- Date: 2026-11-16
- Status: **LOGICAL STORAGE ARCHITECTURE DECIDED / DEPLOYMENT AND IMPLEMENTATION NOT VERIFIED**
- Branch: `session-storage-consistency-forget-atomicity-2026-11-16`
- Scope: physical serialization, durable receipts, dependency completeness, visibility, recovery and storage conformance.

## 1. Selected logical realization

Select one durable, linearizable serialization domain per Canonical Memory authority. It MUST atomically order:
1. producer-class registry version/status changes;
2. producer WorkItem registration and registration sequence allocation;
3. ForgetFence installation and immutable registry-version/high-water snapshot;
4. complete dependency-set registration;
5. final authorization/fence/work/lease revalidation and authoritative visibility commit;
6. barrier-visible terminal disposition.

The same authority must govern both D's Forget control ledger and the authoritative artifact visibility marker. A database transaction is preferred when both records can participate in one transaction. A separate object store may hold large bytes only as private staging; its listing/path is never visibility authority.

## 2. Reject check-then-write and split visibility

The following are invalid:
- read current fence, then independently write a visible artifact;
- allocate registration sequence outside the fence serialization order;
- write queue state before a durable D registration receipt;
- expose object-store bytes before the authoritative visibility record commits;
- commit a gate token in one store and visibility in an unrelated store without a durable coordinator;
- treat an outbox event, index update, cache entry or DLQ state as publication/terminal proof;
- rely on process-local mutexes, eventual consistency or stale replicas for safety decisions.

If a single transaction domain cannot span the fence ledger and visibility marker, the only acceptable alternative is a durable coordinator protocol with idempotent prepare/commit, hidden prepared state, participant recovery, and current fence plus PermissionEpoch revalidation at the final visibility CAS/commit. No prepared artifact may be queryable.

## 3. Durable records and constraints

The implementation MUST provide durable equivalents of:
- ProducerClass registry with version/status and uniqueness;
- ProducerWork ledger keyed by WorkItemId, with immutable request digest, typed registration sequence and receipt;
- ForgetFence record plus immutable BarrierSnapshotReceipt containing registry version and ProducerRegistrationHighWater;
- DependencyRegistration record keyed by ArtifactId/DependencySetDigest, committed only as a complete set;
- Work attempt/lease fencing state with AttemptId and LeaseEpoch;
- PublicationReceipt and authoritative VisibilityPointer/visibility state;
- terminal disposition receipt and barrier accounting;
- transactional outbox with dedupe key and delivery state;
- recovery/checkpoint metadata proving current Forget control state is applied before serving after restore.

Uniqueness/idempotency constraints must make duplicate request replay return the original receipt. A reused idempotency key with a different request digest is a conflict. The system must preserve immutable receipt contents and monotonic fence/lease generations.

## 4. Reader visibility predicate

An artifact is queryable only if its authoritative publication record is committed, its visibility pointer references the exact immutable ArtifactId/digest, the complete dependency registration is committed, and the current applicable ForgetFence/authorization checks permit access. Staging buckets, object-store listings, uncommitted rows, outbox messages, indexes and caches are not sufficient.

Readers must not serve from a stale replica/cache when current fence or permission state cannot be proven. After failover/restore, the service remains closed until the latest durable Forget control ledger, fence generations and visibility decisions have been reconciled. Restoring artifact bytes without the newer control ledger must never resurrect suppressed content.

## 5. Transaction isolation and deployment decision

The logical contract requires serializable behavior (or a formally proven equivalent linearizable coordinator) for the critical operations above. The concrete database engine, version, isolation configuration, replication topology, failover mode and backup/restore implementation remain deployment decisions because no production environment or codebase was supplied. They MUST be selected and recorded before Implementation Verified can be considered.

## 6. Crash/recovery invariants

- Crash before registration commit: no admitted WorkItem and no queue/lease/execute permission.
- Crash after registration commit but before response: retry returns the same receipt.
- Crash during dependency registration: either the complete dependency set is committed or none is publishable.
- Crash before visibility commit: artifact remains private.
- Crash after visibility commit but before ACK/outbox delivery: readback proves Published; replay is idempotent.
- Lease expiry/reassignment: old LeaseEpoch cannot publish or terminalize.
- Fence wins before publication: no visibility commit.
- Publication wins before fence: durable pre-fence publication is reconciled under the installed fence.
- Restore/failover: no serving until current Forget control state is reconciled; stale backup state cannot override newer fences.

## 7. Verification plan (not results)

Execute deterministic two-client races for registration-vs-fence and publish-vs-fence; crash injection before/after each durable commit; duplicate ACK/retry; dependency partial-write; stale lease; coordinator/participant restart; outbox replay; replica lag; failover and backup restore. Assert no unregistered admitted work, no partial dependency visibility, no stale-lease publication, no post-fence publication, no visibility before commit and no resurrection after restore.

Every run must retain engine/version/config, isolation and replication settings, deterministic seed, pause/crash point, request IDs/digests, durable receipts, transaction/lock/CAS trace, authoritative reader snapshots, recovery logs and invariant-checker output.

**No test has been executed by this document.** C01–C20 and the Phase 3.6 storage fault suite remain **NOT RUN**. No production-readiness, global Forget completion or physical-erasure claim is made.
