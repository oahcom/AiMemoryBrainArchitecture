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


## 8. Architecture-level decision addendum / 架构层决策补充（2026-11-17）

- Decision scope: **logical serialization architecture only**.
- Disposition: **OPTION A SELECTED AS THE NORMATIVE V1 ARCHITECTURE PROFILE; PHYSICAL DEPLOYMENT/ENGINE SELECTION REMAINS L4**.
- This addendum supersedes the previous phrase “NO TOPOLOGY SELECTED” only for the abstract architecture decision. It does not claim a database product, executable deployment, operator or runtime topology has been selected.

### 8.1 Decision / 决策

For v1, each Canonical Memory authority MUST use one logical serializable transaction domain for D's authoritative producer-admission/fence/dependency/publication-participant records and Storage's authoritative hidden participant / final VisibilityPointer / PublicationReceipt / outcome / outbox records.

The transaction domain is the **physical serialization substrate**, not a merged semantic authority:

- D remains the sole semantic authority for ProducerClass, ProducerWork admission, ProducerRegistrationSequence, ForgetFence, lineage/dependency completeness, PublicationParticipantRef and D terminality.
- Storage remains the sole semantic authority for PREPARED_HIDDEN, VisibilityPointer, Storage visibility outcome, PublicationReceipt and outbox durability.
- I remains the sole authority for authentication, PermissionEpoch, authorization, revocation order and I CommitAuthorizationReceipt.
- COC remains a separate quorum-ordered causal/recovery log; it is not silently included in this transaction and does not become I's sequencer or Storage's visibility authority.
- C remains the sole authority for provider handoff/outcome; E remains the compiler lifecycle authority.

每个 Canonical Memory Authority 的 v1 架构 MUST 使用一个逻辑 Serializable Transaction Domain，覆盖 D 的 Producer Admission/Fence/Dependency/PublicationParticipant 权威记录，以及 Storage 的 Hidden Participant / 最终 VisibilityPointer / PublicationReceipt / Outcome / Outbox 权威记录。

该 Transaction Domain 只是**物理序列化底座**，不合并语义权威：D 仍唯一拥有 Producer/Fence/Lineage/PublicationParticipant 语义；Storage 仍唯一拥有 PREPARED_HIDDEN、VisibilityPointer 和 Storage Outcome；I 仍唯一拥有身份/授权/撤销；COC 仍是独立 Quorum Log；C/E 分别保留 Provider 和 Compiler 权威。

### 8.2 Normative operation order / 规范操作顺序

1. D registers the derivative-capable ProducerWorkItem and captures the D admission order before E queues, leases, dereferences protected source data or executes.
2. E creates immutable compiler output in private staging and submits the complete direct/transitive dependency set to D as one immutable completeness unit.
3. Storage persists the exact immutable publication tuple as PREPARED_HIDDEN and returns a durable StorageVisibilityParticipantRef. No public pointer, signed serving URL, index event or cache-visible entry exists.
4. D admits PublicationParticipantRef bound to that exact StorageVisibilityParticipantRef and tuple digest, serialized against D InstallForgetFence. Fence-first rejects; participant-first creates an unresolved barrier participant.
5. I consumes the single-use CommitAuthorizationReceipt in its own PolicyDomain sequencer, bound to the exact D and Storage participant references. Only COMMIT_WON can proceed; REVOCATION_WON forbids visibility; UNKNOWN/IN_DOUBT remains blocked.
6. Storage performs the final serializable transaction. It verifies the exact PREPARED_HIDDEN participant, D participant identity and D fence-order proof (including whether the participant precedes a later pending fence), the consumed I COMMIT_WON proof, exact artifact/version/digest/dependencies/Scope and current attempt/lease. It atomically commits VisibilityPointer, COMMITTED_VISIBLE outcome, PublicationReceipt and outbox.
7. If the final transaction proves no pointer/outcome can exist and no delayed writer can publish, Storage records authoritative NO_PUBLICATION. Ambiguous result remains UNKNOWN and private.
8. D and I independently close their own participants only after reading the same exact Storage COMMITTED_VISIBLE or NO_PUBLICATION outcome. Post-outcome I terminal proof is not a precondition to the Storage commit.

### 8.3 Fence/visibility ordering proof obligation / Fence 与 Visibility 顺序证明

The shared transaction domain must serialize D fence installation and Storage final visibility commit. D's participant admission is also serialized with fence installation.

- If fence installation linearizes before D participant admission, D rejects/quarantines; Storage cannot publish.
- If participant admission linearizes first, the participant is durably present in D's barrier. A later fence may be recorded but cannot become effective past that unresolved participant. The final Storage transaction may complete that already-admitted participant only after validating the exact D ordering proof and I COMMIT_WON proof.
- If Storage final visibility commits first, the immutable publication is part of the pre-fence work set and D/I closeout records the exact outcome.
- If the fence is effective first, or proof ordering is unknown, no visibility pointer is committed.
- There is no valid state in which an admitted participant is absent from the D barrier, or a visible artifact lacks the exact D/I proof pair.

共享 Transaction Domain 必须对 D Fence 安装与 Storage 最终 Visibility Commit 提供序列化。D Participant Admission 也必须与 Fence 安装在同一 D 权威顺序中。

- Fence 先于 Participant Admission：D 拒绝/隔离，Storage 不得发布。
- Participant Admission 先发生：该 Participant 已持久进入 D Barrier；后续 Fence 可登记，但在该 Participant 未终结前不能越过它生效。Storage 只有验证精确 D 顺序证明和 I COMMIT_WON 后才能完成该已准入 Participant。
- Storage Visibility 先提交：不可变发布属于 Fence 前工作集，D/I 按精确结果关闭各自 Barrier。
- Fence 已生效或顺序 UNKNOWN：不得提交 VisibilityPointer。
- 不允许“已准入 Participant 不在 D Barrier”或“可见 Artifact 缺少精确 D/I Proof”的状态。

### 8.4 Explicit non-goals and scope / 明确不包含与范围

- This is one Canonical Memory authority per serialization domain and one I PolicyDomain per JF-10 owner-gate operation. Cross-PolicyDomain atomicity is **NOT SUPPORTED / BLOCKED** in v1.
- The I sequencer and COC quorum log remain independent consistency authorities. No cross-log atomic commit is claimed; unresolved participants remain held until authoritative reconciliation.
- The separate JF-10 PreparedTransactionGID / DB-incarnation same-XID protocol remains a distinct COC ↔ I ↔ Storage bridge. It must not be conflated with StorageVisibilityParticipantRef.
- Option B is not a v1 fallback. It requires a successor ADR that proves an equivalent durable protocol, operator, failure model and all crash/recovery invariants before substitution.
- Option C remains rejected.

### 8.5 Proof assumptions and failure behavior / 证明假设与故障行为

The architecture assumes the selected transaction engine can provide serializable transactions (or a formally equivalent strict-serializable mechanism), durable commit acknowledgement, unique/idempotent operation constraints, atomic pointer/receipt/outcome/outbox commit, and authoritative read-after-commit for the relevant authority.

If any assumption is not met by a future engine, the deployment is non-conforming; it MUST NOT silently weaken to check-then-write, process mutex, queue order, outbox-only or stale-token validation.

Crash before final commit => PREPARED_HIDDEN remains private; same PublicationOperationId/tuple lookup recovers. Crash after commit but before ACK => authoritative readback returns the same immutable COMMITTED_VISIBLE outcome. Lost/ambiguous commit acknowledgement => UNKNOWN until same-operation lookup resolves. Conflicting terminal outcomes => quarantine/integrity incident. Restore or failover with uncertain serialization history => RESTORE_FENCED until D/I/COC/Storage evidence is reconciled.

### 8.6 L1 vs L4 separation / L1 与 L4 分离

**L1 CLOSED BY THIS ADR:** a single serializable transaction domain per Canonical Memory authority is the normative v1 logical topology; D and Storage semantic authorities remain distinct; I and COC remain independent; exact pre/post-commit proof ordering is specified; Option C is rejected and Option B requires a successor proof.

**L4 STILL OPEN:** actual DB product/version/configuration, deployment manifest, operator/on-call, cluster/failure-domain placement, HA/PITR, real read-path enforcement, production key custody, and physical crash/failover/restore drills. These do not invalidate the architecture decision; they are implementation conformance obligations.

**本 ADR 关闭 L1：** 每个 Canonical Memory Authority 使用一个 Serializable Transaction Domain 作为 v1 规范逻辑拓扑；D/Storage 语义权威分离；I 与 COC 保持独立；提交前/后的证明顺序明确；Option C 拒绝，Option B 必须重新提交后继 ADR 证明。

**L4 仍 OPEN：** 实际数据库产品/版本/配置、部署清单、Operator/On-call、集群故障域、HA/PITR、真实读路径、生产密钥托管、物理崩溃/故障切换/恢复演练。这些是实现符合性义务，不否定架构决策本身。

---
