# Phase 3.8.2 — Storage/D Serialization Topology ADR

- Owner perspective: Storage / Consistency
- Status: **ADR-BLOCKED — CANDIDATE OPTIONS ONLY; NO DEPLOYED TOPOLOGY SELECTED**
- Related: Issue #10 (JF-10 physical realization), Issue #25 (Phase 3.8 visibility gate)
- Language: English and Chinese are normative peers.

## 1. Decision required

Select the physical serialization boundary that makes D ForgetFence admission/publication ordering and Storage final visibility commit linearizable for each Canonical Memory authority.

The logical contract requires:
- D RegisterProducerWork and InstallForgetFence have one D-authoritative order.
- D dependency-set registration and PublicationParticipant admission are complete and fenced.
- Storage PrepareVisibility creates a durable hidden participant before D admission.
- Storage final visibility commit validates the exact current D participant/fence and pre-commit ICommitAuthorizationProof.
- VisibilityPointer, PublicationReceipt, Storage outcome and outbox are atomic.
- Lost ACK and recovery resolve by the same immutable operation/participant tuple.
- UNKNOWN remains private and keeps D/I barriers held.

This ADR does not merge D and Storage semantic authority. Shared physical transaction substrate does not make Storage the owner of D policy or ForgetFence decisions.

## 2. Options

### Option A — One serializable transaction domain per Canonical Memory authority

D's authoritative admission/fence ledger rows and Storage's final visibility pointer/outcome rows participate in one serializable database transaction domain. The database transaction provides the physical serialization substrate; D still defines and signs the semantic D predicates.

Advantages:
- Directly proves the D fence-vs-final-visibility compare-and-commit in one serialization domain.
- Atomic visibility pointer + PublicationReceipt + Storage outcome + outbox.
- Simpler lost-ACK recovery and ledger consistency.

Required conditions:
- D and Storage approve exact schema/row ownership and transaction boundaries.
- All protected read paths use the same canonical authority and cannot serve pre-commit stage objects.
- No stale replica/cache can bypass pointer state.
- Serializable conflict/retry behavior is deterministic and idempotent.
- Database crash/failover/restore preserves commit identity and anti-rollback.
- I remains a separate PolicyDomain sequencer; Storage verifies the exact consumed pre-commit I proof at commit.
- COC remains a separate quorum log; it is not silently folded into the DB transaction or treated as XA.

### Option B — Separate D and Storage services with a durable linearizable coordinator

D and Storage remain physically separate. A coordinator or consensus-backed protocol establishes durable participant preparation, D admission/fence ordering, Storage commit intent, and final outcome with recoverable proof.

Required conditions:
- Coordinator product/profile, quorum topology, durable log and operator ownership are named.
- D and Storage each persist idempotent participant state before ACK.
- Coordinator records a complete immutable participant tuple and cannot issue D/I decisions.
- A durable prepare/commit protocol prevents visibility until both D and I proofs are validated.
- Failover, split-brain fencing, lost ACK and restore continuity are executable and independently verified.
- No process-local mutex, queue order, eventual replica, check-then-write or outbox-only ordering is accepted.

This option is more complex and cannot be accepted by naming a generic coordinator category.

### Option C — Check-then-write / asynchronous event coordination

**REJECTED.** A read of D fence followed by a later independent Storage write has a race. Queue ordering, process mutex, outbox delivery, stale replicas or a detached reusable token do not close it.

## 3. Current evidence and non-inference

Issue #10 records PostgreSQL 18.7 candidate CI evidence for prepared-XID behavior, synchronous standby promotion, physical restore, coordinator crash fixture and TCP response loss. Those are capability probes for pinned test profiles. They do not establish that the project-designated Canonical Authority runtime uses that engine/profile or that D and Storage share the same serialization domain.

The current HRC/JoinProof and Phase 3.8 proposals do not identify:
- the actual Canonical Memory authority deployment and DB adapter path;
- whether D fence/admission ledger and Storage visibility pointer share a transaction domain;
- production cluster/zone/storage durability and failover fencing;
- authoritative read-path enforcement and stale-cache exclusion;
- accountable human production operator/on-call.

Therefore no option is selected by this ADR. Option A is the preferred candidate only if the actual deployment proves it; otherwise Option B requires a separate ADR and proof bundle.

## 4. Decision gates

| Gate | Required evidence | Current status |
|---|---|---|
| T1 Runtime identity | Exact executable, adapter, canonical authority, DB product/version/config and deployment manifest | OPEN |
| T2 D/Storage row boundary | Owner-approved transaction diagram, schemas, lock/serialization keys and semantic owner split | OPEN |
| T3 Linearization | Deterministic tests for D fence-first and publication-participant-first, including final commit race | OPEN |
| T4 I proof | Online/cryptographic verification of consumed ICommitAuthorizationProof at the actual visibility linearization point | OPEN |
| T5 Atomic outcome | Pointer + receipt + outcome + outbox commit/rollback traces | OPEN |
| T6 HA/restore | Primary loss, promotion, old-primary fencing/rejoin, stale replica, PITR, anti-rollback and restore quarantine | OPEN |
| T7 Read-path | No object-store URL/index/cache/read path serves before authoritative pointer commit | OPEN |
| T8 Owner decisions | D, I and Storage exact-version acceptance plus A integration acceptance | OPEN |

No schema freeze, implementation PASS, deployment or production activation follows from this ADR.

## 5. Required deterministic physical tests

1. D Fence commit wins before Storage final visibility commit → no pointer; D participant remains held until authoritative NO_PUBLICATION.
2. D PublicationParticipant admitted first, then Fence → Fence cannot pass unresolved participant; commit/closeout is serialized.
3. I REVOCATION_WON before consumption → no visibility; same operation proves NO_PUBLICATION.
4. I COMMIT_WON before revocation → I holds revocation until Storage terminal outcome.
5. Storage prepare ACK loss → same PublicationOperationId/tuple resolves same hidden participant.
6. D admission ACK loss → same PublicationParticipantRef lookup; no second participant.
7. Visibility commit ACK loss → same operation lookup returns exact immutable outcome.
8. Crash after Storage prepare before D admission → orphan stays hidden/private.
9. Crash after D admission but missing Storage row → UNKNOWN/ledger inconsistency; never abort.
10. Primary loss after prepared participant → same GID/DB incarnation resolution only; no alternate XID.
11. Old primary rejoins after promotion → fenced from writes; no dual visibility.
12. Restore from stale snapshot/PITR point → RESTORE_FENCED until COC/D/I/Storage prefixes and owner high-waters reconcile.
13. Stale replica or cache attempts protected read → reject.
14. Outbox replay after NO_PUBLICATION → cannot publish; terminal outcome immutable.
15. D/I proof mismatch or revoked signer key → no visibility; artifact remains private.

## 6. 中文规范

本 ADR 要解决的是每个 Canonical Memory Authority 内，D ForgetFence 与 Storage 最终可见性提交之间的物理线性化边界。逻辑上要求 D 注册/ForgetFence 有权威顺序，Storage 先持久化隐藏 Participant，D 再准入，I 在独立 PolicyDomain Sequencer 中消费授权，Storage 最终提交时验证 D 当前 Fence/Participant 与提交前 ICommitAuthorizationProof，并原子提交 VisibilityPointer、PublicationReceipt、Outcome 和 Outbox。

候选 A 是每个 Canonical Memory Authority 使用一个 Serializable DB Transaction Domain，D 仍拥有语义权威，Storage 只拥有物理持久化/可见性。候选 B 是 D/Storage 分服务，由持久化线性协调协议证明同样的顺序。Check-then-write、Queue、Process Mutex、Eventual Replica、Outbox-only 协调明确拒绝。

Issue #10 的 PostgreSQL 18.7 CI 仅证明指定测试 Profile 的能力，不证明项目生产 Canonical Authority 已使用该数据库，也不证明 D/Storage 共用事务域。当前真实运行时、DB Adapter、D/Storage 行归属、HA/PITR、旧主隔离、Read Path 和生产运维均未指定。因此本 ADR 不选择 A 或 B；Option A 仅是有条件优先候选，必须由真实部署证据决定。

## 7. Disposition

**ADR-BLOCKED / NO TOPOLOGY SELECTED.** Storage may not claim the Phase 3.8 final visibility boundary is physically realized until T1–T8 are evidenced and independently reviewed.
