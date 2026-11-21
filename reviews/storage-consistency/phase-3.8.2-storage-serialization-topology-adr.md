# Phase 3.8.2 — Storage/D Serialization Topology ADR

- Owner perspective: Storage / Consistency
- Status: **L1 LOGICAL TOPOLOGY SELECTED — OPTION A; L4 PHYSICAL ENGINE/DEPLOYMENT OPEN**
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

**Historical pre-addendum disposition — superseded for L1 only.** Before §8, no topology was selected. Section 8 selects Option A as the normative v1 logical architecture; physical engine/deployment remains L4 OPEN.


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


### 8.7 Concrete per-authority serialization anchor / 每 Authority 具体序列化锚点

The shared serializable transaction domain MUST expose one durable `CanonicalAuthoritySerializationAnchor` per `BrainAuthorityRef`. This is the concrete common serialization point; a general claim that D and Storage happen to use the same database is insufficient.

**Anchor identity and physical record / 锚点身份与物理记录**

- Primary key: exact `BrainAuthorityRef`; one anchor per Canonical Memory authority and its `SerializationDomainRef`.
- Physical record: `AuthoritySerializationAnchorRef`, `BrainAuthorityRef`, `SerializationDomainRef`, `DatabaseIncarnationRef`, monotonic `serialization_revision`, `last_transition_ref`, `last_transition_kind`, `last_transition_digest`.
- Append-only transition record: `SerializationTransitionRef`, `AuthoritySerializationAnchorRef`, committed `serialization_revision`, transition kind, issuing owner ref, immutable operation/participant ref and digest.
- The anchor and transition record are Storage-owned physical serialization metadata. They do not grant Storage D-policy authority or mint a D/I/C/COC owner receipt. D signs and validates D semantics; Storage controls only the physical transaction substrate.

**Required protected transitions / 必须使用锚点的受保护状态变更**

Every following transition MUST update the same per-authority anchor row and append its transition record in the same database transaction as its owner-authoritative record:

1. D ProducerWork admission/registration before E queue, lease, protected-source dereference or execution.
2. D complete direct/transitive dependency-set registration.
3. D PublicationParticipant admission.
4. D InstallForgetFence / advance of D ForgetFenceGeneration.
5. Storage final VisibilityPointer + COMMITTED_VISIBLE outcome + PublicationReceipt + outbox commit.
6. Storage authoritative NO_PUBLICATION terminal outcome when it closes the same publication operation.

Storage PREPARED_HIDDEN is durable and private. It may be written before D admission without advancing the serialization anchor because it cannot create a serving pointer; D admission still must win the anchor order before any final visibility commit. Any later transition that can affect D fence/participant/publication order MUST use the anchor.

**Transaction protocol / 事务协议**

For each protected transition:

1. Begin a transaction in the selected per-authority serialization domain at SERIALIZABLE isolation (or a formally proven equivalent).
2. Resolve the exact `BrainAuthorityRef`, `SerializationDomainRef` and `DatabaseIncarnationRef`; lock the unique anchor row for update.
3. Read the current `serialization_revision` and all relevant D/Storage owner state from the authoritative primary.
4. Validate the owner-specific preconditions and immutable operation/participant tuple. A physical anchor lock is not an owner authorization.
5. CAS-update the anchor from expected revision `r` to `r+1`; append a unique `SerializationTransitionRef` with the exact transition digest; write the D or Storage owner-authoritative record(s) in the same transaction.
6. Commit. The transaction commit is the linearization point for this transition. A serialization failure aborts the entire transaction; retry only with the same immutable transition ref and digest.
7. On lost ACK, resolve by the stable `SerializationTransitionRef` and exact digest from the durable transition table. Same ref/same digest returns the same committed result; same ref/different digest is an integrity incident. Never mint a new owner identity to escape an ambiguous commit.

**Linearization outcomes / 线性化结果**

- D Fence transaction commits first: later D admission or Storage final-visibility transaction observes the committed fence and is denied/quarantined; no VisibilityPointer is created.
- D participant/dependency admission commits first: its exact row is in D's barrier/snapshot; a later Fence must include and reconcile it. Fence cannot become effective past unresolved admitted work.
- Storage final-visibility transaction commits first: the artifact is a pre-fence visible participant; the later Fence snapshot must include it and D/I closeout must use the same immutable Storage outcome.
- Dependency registration commits first: the complete dependency set is included in the fence/barrier snapshot. Fence commits first: later dependency expansion is rejected or quarantined; no partial set is published.
- UNKNOWN serialization history, stale anchor incarnation, uncertain failover or missing transition record => RESTORE_FENCED / UNKNOWN; never infer order from timestamps, queue order, XID, or owner counters.

**Nominal type boundary / 名义类型边界**

`serialization_revision` is a physical monotonic revision local to one `SerializationDomainRef` / `BrainAuthorityRef`. It is NOT equal or comparable to:
- D `ForgetFenceGeneration`, D `owner_gate_generation` or D `barrier_generation`;
- I `PermissionEpoch`, InventoryEpoch or PolicyDomain position;
- C `sequence_namespace_ref` / record sequence;
- COC quorum position or RecoveryCutoff position;
- Storage prepared participant attempt, `PreparedTransactionGID` or `EngineNativeXIDRef`.

`AuthoritySerializationAnchorRef`, `SerializationTransitionRef` and `SerializationRevision` are nominally distinct from `SerializationDomainRef`, `BrainAuthorityRef`, `StorageAuthorityRef`, owner receipts and all semantic epochs/generations. A string representation does not erase the type.

**Availability and performance boundary / 可用性与性能边界**

There is one anchor per Canonical Memory authority, not one global anchor for the whole installation. The single row may be a contention point; this is an explicit v1 correctness-first tradeoff. Partitioning/sharding the anchor is forbidden until a successor proof demonstrates non-overlapping fence/participant/publication domains and preserves cross-scope ordering. Throughput/latency benchmarks and DB-engine selection are L4, not assumed.

The deployment MUST provide one authoritative writer/primary for this anchor, durable commit acknowledgement, old-primary fencing, authoritative read-after-commit and restore/failover continuity of the anchor plus append-only transition records. If a future engine cannot provide these properties, Option A is non-conforming; Option B requires a successor ADR and proof. No process mutex, queue ordering, stale replica, or check-then-write may substitute.

**中文规范：**

每个 `BrainAuthorityRef` 必须有一个持久化 `CanonicalAuthoritySerializationAnchor`，作为 D 与 Storage 的共同物理序列化点。仅仅声称“使用同一个数据库”不够。

锚点以 BrainAuthorityRef 为主键，绑定 SerializationDomainRef、DatabaseIncarnationRef、单调 serialization_revision、最后 Transition Ref/Kind/Digest；每次受保护变更还必须在同一事务内追加不可变 SerializationTransition 记录。锚点与 Transition 是 Storage 拥有的物理序列化元数据，不授予 Storage D Policy 权威，也不签发 D/I/C/COC Owner Receipt。

D Producer Admission/Registration、完整 Dependency Registration、D PublicationParticipant Admission、D InstallForgetFence/ForgetFenceGeneration 推进、Storage 最终 VisibilityPointer/Outcome/Receipt/Outbox Commit、Storage NO_PUBLICATION 终态，均必须在同一个 per-authority Transaction Domain 中更新同一锚点并写入对应 Owner 记录。PREPARED_HIDDEN 是私有持久状态，不产生服务指针，可以先于 D Admission 写入；但它不能绕过锚点顺序进入可见状态。

每个受保护事务必须：使用 SERIALIZABLE（或已证明等价机制）；锁定唯一锚点；读取权威主库中的 D/Storage 状态；验证 Owner 自己的语义前置条件；通过 CAS 将 revision 从 r 推进到 r+1；同事务写入 Transition 与 Owner Record；最后提交。事务提交是线性化点。序列化失败必须整体回滚，并使用同一个不可变 Transition Ref/Digest 幂等重试。Lost ACK 必须按 Transition Ref/Digest 查回，不能创建新 Owner Identity。

Fence 先提交，则后续 Admission/Visibility 被拒绝；Admission/Dependency 先提交，则必须进入后续 Fence Snapshot/Barrier；Storage Visibility 先提交，则属于 Fence 前可见工作集；Dependency 先提交，则完整依赖集进入 Barrier。顺序 UNKNOWN、旧主未隔离、锚点 Incarnation 不确定或 Transition Record 缺失时必须 RESTORE_FENCED/UNKNOWN，不得用时间戳、Queue 顺序、XID 或 Owner Counter 推断。

SerializationRevision 只属于一个 SerializationDomain/BrainAuthority，是物理单调 Revision；不得与 D Fence/Gate/Barrier Generation、I Permission/Inventory/PolicyDomain Position、C Sequence Namespace、COC Quorum Position、PreparedTransactionGID 或 EngineNativeXID 比较。每个 Canonical Memory Authority 独立一个锚点。单行热点是 v1 正确性优先取舍；没有 successor proof 不得分片。单主、旧主隔离、持久 ACK、读后写和恢复连续性均属于 Option A 必须满足的部署条件；无法满足时 Option A 不符合规范，Option B 必须提交后继 ADR。

### 8.8 Claim/Fact canonical commit integration / Claim/Fact 规范提交集成

This addendum integrates ClaimRevision and FactRevision
into the existing L1 logical transaction protocol.

It does NOT select a new storage topology.

The D canonical commit and Storage publication
participant protocol MUST preserve the following order:

- D commits canonical Claim/Fact revisions and their
  required authorization/dependency references.
- E publishes no canonical derivative before D's
  canonical decision and dependency registration.
- Storage persists the exact publication tuple as
  PREPARED_HIDDEN.
- D admits the exact PublicationParticipant against
  the current ForgetFence.
- I supplies the applicable single-use commit
  authorization decision.
- Storage performs the final protected visibility
  transaction.
- G commits a new public ContextVersion only after
  the applicable authoritative visibility outcome.

Producer Admission and PublicationParticipant Admission
are distinct, ordered operations within the same protected
production and publication lifecycle.

Producer Admission establishes the exact Producer/ProducerWork
participant before dependency-set registration and D canonical
commit.

PublicationParticipant Admission is a subsequent operation.
It admits the exact PublicationParticipant bound to the
StorageVisibilityParticipantRef and publication tuple digest,
after D canonical commit and durable Storage persistence of
the exact publication tuple as PREPARED_HIDDEN.

The two admissions MUST NOT be treated as the same operation
or as interchangeable participant records.

Producer Admission MUST precede complete dependency-set
registration and canonical commit.

PublicationParticipant Admission MUST follow canonical
commit and PREPARED_HIDDEN persistence.

Both admissions MUST be serialized against the same
authoritative per-BrainAuthorityRef ordering anchor. The
"ForgetFence/Admission ordering anchor" and the
"per-BrainAuthorityRef serialization anchor" MUST denote
the same authoritative ordering anchor; neither name may
be interpreted as a separate lock or transaction domain.

The complete direct and transitive dependency closure
established by Producer Admission MUST be durably persisted
before the corresponding participant barrier may be
resolved or completed. A Fence MUST NOT complete that
participant barrier until the complete dependency closure
has been durably persisted. This is the same normative
constraint specified in Extraction §19.2, not a second
independent mechanism.

The observable completion predicate is:
DependencyClosurePersisted(P) = TRUE if and only if the
authoritative durable dependency-registration record for
Producer participant P identifies the complete direct and
transitive dependency set, records completeness as COMPLETE,
has a persisted closure digest matching that exact set,
and is confirmed by authoritative read-after-commit.
A participant barrier MUST be resolved or completed only
when this predicate is TRUE. UNKNOWN dependencies, missing
dependency records, incomplete closure records, unavailable
authoritative reads, and dependency-persistence failures
MUST NOT be treated as success. The dependency closure
MUST NOT be narrowed to complete the barrier earlier.

For each admission, successful admission and durable recording
of the exact participant identity MUST form one indivisible
operation within the authoritative Transaction Domain.

A successful Producer Admission does not constitute
PublicationParticipant Admission.

PublicationParticipant Admission MUST preserve and bind to
the dependency closure already established for the committed
canonical revisions. It MUST NOT independently redefine
or narrow that closure.

This is an implementation-conformance gate, not an
unresolved normative ordering choice.

The existing per-BrainAuthorityRef serialization
anchor remains the L1 ordering mechanism for protected
D/Storage transitions.

No separate process-local transaction or eventual
message delivery is allowed to substitute for that
ordering.

**中文规范：**

本补充将 ClaimRevision 和 FactRevision
纳入既有 L1 逻辑事务协议。

本补充不选择新的 Storage 拓扑。

D 规范提交与 Storage Publication Participant
协议必须保持以下顺序：

- D 提交规范 Claim/Fact Revision 及其必需授权/依赖引用。
- D 完成规范决策与依赖登记之前，
  E 不得发布规范派生对象。
- Storage 将准确 Publication Tuple 持久化为 PREPARED_HIDDEN。
- D 针对当前 ForgetFence 准入准确 PublicationParticipant。
- I 提供适用的一次性 Commit Authorization 决定。
- Storage 执行最终受保护 Visibility Transaction。
- 只有在适用权威 Visibility Outcome 确认后，
  G 才能提交新的公开 ContextVersion。

Producer Admission 与 PublicationParticipant Admission
是同一受保护生产和发布生命周期中的两个不同且有序的操作。

Producer Admission 在 dependency-set registration 和
D canonical commit 之前，建立准确的 Producer/ProducerWork
participant 身份。

PublicationParticipant Admission 是后续操作。
它在 D canonical commit 和 Storage 将准确的 publication
tuple 持久化为 PREPARED_HIDDEN 之后，准入准确的
PublicationParticipant，并将其绑定到
StorageVisibilityParticipantRef 和 publication tuple digest。

不得将两个准入操作视为同一个操作，
也不得将两个 participant 记录相互替代。

Producer Admission 必须先于完整 dependency-set registration
和 canonical commit。

PublicationParticipant Admission 必须发生在 canonical commit
和 PREPARED_HIDDEN 持久化之后。

两个准入操作必须针对同一个权威 per-BrainAuthorityRef
排序锚点进行串行化。这里的
“ForgetFence/Admission ordering anchor”与
“per-BrainAuthorityRef serialization anchor”
MUST 指同一个权威排序锚点；不得将任一名称解释为
独立锁或独立事务域。

Producer Admission 所建立的完整 direct 和 transitive
dependency closure MUST 在对应 participant barrier
被判定为 resolved 或完成之前持久化完毕。只有完整依赖闭包
已经持久化，Fence 才 MUST 可完成该 participant barrier。
这与 Extraction §19.2 规定的是同一规范约束，
不是第二个独立机制。

可观察的完成谓词为：
DependencyClosurePersisted(P) = TRUE 当且仅当权威持久化
dependency-registration record 明确标识 Producer participant P
的完整 direct 和 transitive dependency set，完整性状态为
COMPLETE，已持久化 closure digest 与该准确集合匹配，
且权威 read-after-commit 已确认该记录。只有该谓词为 TRUE，
participant barrier MUST 才可被判定为 resolved 或完成。
UNKNOWN dependency、缺失 dependency record、不完整 closure
record、不可用的权威读取及 dependency persistence failure
MUST NOT 被视为成功。MUST NOT 通过缩减 dependency closure
使 barrier 提前完成。

对于每次准入，准入成功与对准确 participant identity
的持久化记录，必须在权威 Transaction Domain 内
构成一个不可分操作。

Producer Admission 成功不代表
PublicationParticipant Admission 成功。

PublicationParticipant Admission 必须保留并绑定已经为
已提交规范 Revision 建立的 dependency closure。
不得独立重新定义或缩减该依赖闭包。

这是一个 implementation-conformance gate，
不是尚未解决的规范排序选择。

现有 per-BrainAuthorityRef Serialization Anchor
仍然是受保护 D/Storage 转换的 L1 排序机制。

不得使用独立进程内事务或最终一致消息传递
替代该排序机制。
