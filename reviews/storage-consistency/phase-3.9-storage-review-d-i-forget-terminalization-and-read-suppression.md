# Phase 3.9-Storage — Storage Review of D/I Forget Terminalization and Read-Suppression Linearization
# Phase 3.9-Storage — Storage 对 D/I Forget 终态化与读抑制线性化的审查

**Status / 状态:** STORAGE-ROLE REVIEW PROPOSAL — CONDITIONAL / Storage 角色审查提案 — 有条件  
**Reviewer perspective / 审查视角:** Storage / Consistency  
**Baseline branch / 基线分支:** `session-storage-consistency-forget-atomicity-2026-11-16`  
**Baseline commit / 基线提交:** `830a559bd2f4ec72608f5a51e1a0b43779f2b989`  
**Review targets / 审查目标:** D Phase 3.9 proposal (PR #66); I/D Phase 3.9-I proposal (PR #68)

> This is a role-simulated Storage review prepared in the same ChatGPT project session. It is not an independent Storage Owner signature, a physical topology approval, an implementation proof or a production acceptance.
>
> 本文件是在同一 ChatGPT 项目会话中模拟 Storage 角色形成的审查，不是独立 Storage Owner 签名、物理拓扑批准、实现证明或生产验收。

---

## 1. Executive disposition / 执行结论

**CONDITIONAL ACCEPTANCE OF THE LOGICAL DIRECTION; CHANGES REQUIRED BEFORE STORAGE CONTRACT ADOPTION.**

**有条件接受逻辑方向；Storage 契约采纳前必须修改并完成验证。**

Storage accepts the architectural separation proposed by D Phase 3.9:

Storage 接受 D Phase 3.9 提出的架构区分：

1. D Fence installation/read suppression is a durable semantic event owned by D.
2. Storage's final visibility commit is a distinct serialization event owned by Storage.
3. A pre-fence PublicationParticipant remains a barrier obligation, but its admission is not a reusable right to publish after a later Fence.
4. Barrier closure can wait for participant terminal evidence while read suppression is already effective.
5. I terminalization authorization is a single-use I-owned receipt, not a D-generated permission and not I global completion.
6. UNKNOWN remains private and blocks completion.

1. D Fence 安装/读抑制是由 D 拥有的持久化语义事件。
2. Storage 最终 Visibility Commit 是由 Storage 拥有的独立序列化事件。
3. Fence 前 PublicationParticipant 仍是 Barrier 义务，但其准入不构成后续 Fence 之后可重复使用的发布权。
4. Barrier 闭合可以等待 Participant 终态证据，而读抑制已经生效。
5. I 终态化授权是 I 所有的单次 Receipt，不是 D 生成的许可，也不是 I 全局完成。
6. UNKNOWN 必须保持私有并阻止完成。

The D Phase 3.9 read-suppression split is a proposed correction to the current D Phase 3.8.11.3 participant-first wording. Storage does **not** treat it as accepted until D and Storage explicitly accept the same exact successor Blob and update the controlling clauses.

D Phase 3.9 的读抑制分离，是对当前 D Phase 3.8 §11.3 Participant-first 措辞的拟议修正。除非 D 与 Storage 明确接受同一精确后继 Blob 并更新控制性条款，否则 Storage **不将其视为已接受**。

---

## 2. Exact baseline contract facts / 精确基线契约事实

The current Storage Phase 3.8 contract states:

当前 Storage Phase 3.8 契约规定：

- Storage owns durable records, transaction isolation/serialization, private staging, authoritative visibility pointer, visibility outcome, outbox and crash/failover/restore mechanics.
- D owns ProducerClass, RegistrationReceipt, ForgetFence, lineage/dependency completeness, PublicationParticipantRef and D terminality.
- I owns authorization/PermissionEpoch/CommitAuthorizationReceipt and revocation ordering.
- `PrepareVisibility` creates a durable `PREPARED_HIDDEN` participant.
- The final `CommitVisibility` transaction is the only visibility linearization point and atomically validates exact Storage participant, current D participant/fence, consumed I publication proof, artifact/version/digest, complete dependency, scope and current attempt/lease.
- If the outcome cannot be proven, Storage retains `UNKNOWN` and the artifact remains private.

- Storage 拥有持久化记录、事务隔离/序列化、私有暂存、权威 Visibility Pointer、Visibility Outcome、Outbox 及 Crash/Failover/Restore 机制。
- D 拥有 ProducerClass、RegistrationReceipt、ForgetFence、Lineage/Dependency 完整性、PublicationParticipantRef 和 D 终态。
- I 拥有授权/PermissionEpoch/CommitAuthorizationReceipt 及撤权排序。
- `PrepareVisibility` 创建持久化 `PREPARED_HIDDEN` Participant。
- 最终 `CommitVisibility` 事务是唯一 Visibility 线性化点，并原子验证精确 Storage Participant、当前 D Participant/Fence、已消费 I Publication Proof、Artifact/Version/Digest、完整 Dependency、Scope 和当前 Attempt/Lease。
- 无法证明结果时，Storage 保持 `UNKNOWN` 且 Artifact 必须私有。

The Storage topology ADR selects Option A as the L1 logical architecture: one serializable transaction domain per Canonical Memory authority. L4 physical engine/deployment remains OPEN. PostgreSQL capability probes are not proof that the project's production authority uses that exact topology.

Storage 拓扑 ADR 将 Option A 选为 L1 逻辑架构：每个 Canonical Memory Authority 一个 Serializable Transaction Domain。L4 物理引擎/部署仍 OPEN。PostgreSQL 能力探测不能证明项目生产 Authority 使用该精确拓扑。

---

## 3. Required correction: separate Fence effect from barrier closeout / 必需修正：Fence 生效与 Barrier 关闭分离

### 3.1 Two independent facts / 两个独立事实

The D/Storage contract MUST represent two separate facts:

D/Storage 契约必须表示两个独立事实：

- **Fence effective:** the durable D Fence commit has linearized. From that point, canonical reads, dereferences, derivative publication, index/cache projection, Context delivery and restore serving must enforce the new Fence. A path that cannot establish current D Fence state fails closed.
- **Barrier closed:** every pre-fence work/publication member has a proven terminal disposition, all required targets are reconciled, and the D proof is durably committed.

- **Fence 已生效：** D Fence 持久化提交已线性化。从该时点起，规范读取、解引用、派生物发布、Index/Cache 投影、Context 交付和 Restore Serving 均必须执行新 Fence。无法确定当前 D Fence 的路径必须 fail closed。
- **Barrier 已闭合：** 所有 Fence 前 Work/Publication Member 均有已证明的终态处置，所有必需目标已核对，且 D 证明已持久化提交。

A pre-fence unresolved participant can keep the Barrier open. It cannot defer Fence effectiveness for reads.

Fence 前未解决 Participant 可以使 Barrier 保持开放，但不得推迟读路径上的 Fence 生效。

### 3.2 Two serialization outcomes / 两种序列化结果

The shared per-authority serialization domain decides whether final visibility or Fence installation linearizes first:

每个 Authority 的共享序列化域决定最终可见性与 Fence 安装谁先线性化：

| First committed event / 先提交事件 | Storage behavior / Storage 行为 | D barrier behavior / D Barrier 行为 |
|---|---|---|
| Final visibility commit before Fence / 最终 Visibility Commit 先于 Fence | Visibility pointer/outcome/outbox commit atomically. / Visibility Pointer/Outcome/Outbox 原子提交。 | New Fence immediately suppresses this artifact and includes it in the captured inventory. / 新 Fence 立即抑制该 Artifact 并纳入捕获 Inventory。 |
| Fence commit before final visibility / Fence Commit 先于最终 Visibility | Reject visibility commit; keep private; later issue NO_PUBLICATION only with positive proof all future publication paths are impossible. / 拒绝 Visibility Commit；保持私有；只有正向证明所有未来发布路径均不可能时才签发 NO_PUBLICATION。 | Participant remains a barrier member until authoritative terminal outcome. / Participant 保持 Barrier Member，直至取得权威终态结果。 |

Participant admission time is not itself the visibility linearization point. An earlier D PublicationParticipantRef does not authorize a later Storage visibility commit after the Fence commit. Storage MUST recheck the current Fence in the same serialization domain as the pointer flip.

Participant 准入时间本身不是 Visibility 线性化点。较早的 D PublicationParticipantRef 不授权 Fence Commit 之后发生的 Storage Visibility Commit。Storage 必须在与 Pointer Flip 相同的序列化域中重新检查当前 Fence。

### 3.3 Read-path enforcement / 读路径执行

The storage-backed canonical read path MUST:

基于 Storage 的规范读取路径必须：

1. resolve the authoritative canonical visibility pointer/state;
2. establish the latest applicable D Fence generation and target/lineage selector;
3. verify the pointer's exact artifact/version/lineage remains eligible under that Fence;
4. fail closed if Fence authority, serialization history, incarnation, lineage or currentness is UNKNOWN;
5. avoid serving directly from object-store keys, signed URLs, stale replicas, cache entries or index events without the authoritative visibility/Fence check.

1. 解析权威规范 Visibility Pointer/State；
2. 确定最新适用 D Fence Generation 及目标/Lineage 选择器；
3. 验证 Pointer 对应的精确 Artifact/Version/Lineage 在该 Fence 下仍然合格；
4. 若 Fence Authority、序列化历史、Incarnation、Lineage 或当前性为 UNKNOWN，则 fail closed；
5. 不得绕过权威 Visibility/Fence 检查，直接从 Object Store Key、Signed URL、过期 Replica、Cache Entry 或 Index Event 提供服务。

The D Fence is authoritative; a Storage read check is an enforcement mechanism, not a new D decision. A cache invalidation ACK is not the source of truth.

D Fence 是权威；Storage 读取检查只是执行机制，不是新的 D 决策。Cache Invalidation ACK 不是事实来源。

---

## 4. LifecycleEvent terminalization storage contract / LifecycleEvent 终态化 Storage 契约

D's `Memory.lifecycle = Forgotten` append is a separate canonical transaction from derivative `CommitVisibility`. Storage must provide a durable atomic append/CAS primitive but cannot decide D semantics or I authorization.

D 的 `Memory.lifecycle = Forgotten` 追加是与 Derivative `CommitVisibility` 分离的规范事务。Storage 必须提供持久化原子 Append/CAS 原语，但不能决定 D 语义或 I 授权。

Proposed logical operation:

建议逻辑操作：

`CommitForgetLifecycleTerminalization`

The transaction MUST atomically:

事务必须原子执行：

- verify the exact D MemoryId/version and expected LifecycleEvent sequence;
- verify the current active D ForgetFenceGeneration and exact target/scope binding;
- verify the current D CanonicalSuppressionProofRef/digest and its invalidation/reopen generation;
- verify the exact I `ForgetTerminalizationAuthorizationReceipt`, including `COMMIT_WON`, nonce, PolicyDomain, event digest, scope, Memory/version, D proof digest and I issuer/key status;
- append the immutable D LifecycleEvent and update the canonical lifecycle projection/outbox in the same transaction, or use a formally equivalent recoverable atomic append protocol;
- persist a durable transaction/outcome identity that D and I can resolve after ACK loss.

- 验证精确 D MemoryId/Version 和预期 LifecycleEvent Sequence；
- 验证当前活动 D ForgetFenceGeneration 及精确目标/Scope 绑定；
- 验证当前 D CanonicalSuppressionProofRef/摘要及其失效/Reopen Generation；
- 验证精确 I `ForgetTerminalizationAuthorizationReceipt`，包括 `COMMIT_WON`、Nonce、PolicyDomain、Event Digest、Scope、Memory/Version、D Proof Digest 和 I Issuer/Key Status；
- 在同一事务中追加不可变 D LifecycleEvent 并更新规范 Lifecycle Projection/Outbox，或使用形式化等价的可恢复原子追加协议；
- 持久化 D/I 在 ACK 丢失后可解析的事务/结果身份。

Storage does not issue the I receipt, cannot choose `COMMIT_WON`, and cannot declare `GlobalForgetCompleted`. I closes its authorization participant only after it verifies D's exact terminalization or no-terminalization outcome.

Storage 不签发 I Receipt，不得选择 `COMMIT_WON`，也不得声明 `GlobalForgetCompleted`。I 只有在验证 D 精确终态化或未终态化结果后，才关闭自己的授权 Participant。

If the I receipt is missing, stale, revoked, invalid, mismatched or UNKNOWN, Storage MUST reject/hold the lifecycle append. If D proof is stale or the expected lifecycle version changed, Storage MUST reject the append without weakening the Fence.

如果 I Receipt 缺失、过期、撤销、无效、不匹配或 UNKNOWN，Storage 必须拒绝/保持 Lifecycle Append。如果 D Proof 过期或预期 Lifecycle Version 已变化，Storage 必须拒绝追加，但不得削弱 Fence。

---

## 5. Crash, retry and recovery obligations / Crash、Retry 与恢复义务

| Failure window / 故障窗口 | Required Storage result / Storage 必须结果 |
|---|---|
| I receipt consumed `COMMIT_WON`, D LifecycleEvent not yet committed / I Receipt 已消费为 COMMIT_WON，D LifecycleEvent 尚未提交 | Persist/resolve the exact in-flight authorization participant; no other event can reuse it. / 持久化/解析精确在途授权 Participant；其他事件不能重用。 |
| Crash before LifecycleEvent commit / LifecycleEvent Commit 前崩溃 | Recovery queries same operation/event digest; do not infer success or revocation. / 恢复查询同一 Operation/Event Digest；不得推断成功或撤权。 |
| LifecycleEvent commit succeeds, ACK lost / LifecycleEvent Commit 成功但 ACK 丢失 | Same event digest resolves the committed event and transaction identity. / 使用同一 Event Digest 解析已提交事件及事务身份。 |
| D proof invalidated before CAS / CAS 前 D Proof 失效 | CAS rejects; active Fence remains; I receives authoritative no-terminalization or UNKNOWN. / CAS 拒绝；活动 Fence 保持；I 收到权威未终态化结果或 UNKNOWN。 |
| I sequencer or key status unavailable / I Sequencer 或 Key Status 不可用 | No terminalization commit; remain UNKNOWN/IN_DOUBT. / 不提交终态化；保持 UNKNOWN/IN_DOUBT。 |
| DB failover/incarnation mismatch / DB Failover/Incarnation 不匹配 | Quarantine until authoritative commit history, anti-rollback and same event identity are proven. / 隔离，直至权威提交历史、防回滚和相同事件身份得到证明。 |
| Restore from stale snapshot / 从过期 Snapshot 恢复 | Restore-fenced; replay current D Fence and I control/revocation state before any serving. / Restore-Fenced；在任何服务前重放当前 D Fence 与 I 控制/撤权状态。 |

UNKNOWN is never converted to NO_PUBLICATION, D_NO_TERMINALIZATION or success by timeout, missing row, process death, expired lease, ACK loss or local cancellation.

不得通过 Timeout、行缺失、进程死亡、Lease 过期、ACK 丢失或本地取消将 UNKNOWN 转换成 NO_PUBLICATION、D_NO_TERMINALIZATION 或成功。

---

## 6. Required Storage conformance tests / 必需 Storage 符合性测试

| Test ID | Scenario / 场景 | Required assertion / 必须断言 |
|---|---|---|
| ST-FG-001 | Fence commit before visibility pointer / Fence 先于 Visibility Pointer | Final pointer transaction rejects; artifact stays private. / 最终 Pointer 事务拒绝；Artifact 保持私有。 |
| ST-FG-002 | Visibility pointer before Fence / Pointer 先于 Fence | Fence commit immediately suppresses reads; artifact is in inventory. / Fence Commit 立即抑制读取；Artifact 纳入 Inventory。 |
| ST-FG-003 | Participant admitted before Fence but unresolved / Participant 先准入但未解决 | Fence read effect is immediate; barrier member remains open. / Fence 读效应立即生效；Barrier Member 保持开放。 |
| ST-FG-004 | Stale read replica/cache / 过期读 Replica/Cache | No protected read can bypass current Fence; UNKNOWN fails closed. / 受保护读取不得绕过当前 Fence；UNKNOWN fail closed。 |
| ST-FG-005 | Exact I receipt at LifecycleEvent CAS / LifecycleEvent CAS 的精确 I Receipt | Wrong tuple, stale key/epoch, revoked or UNKNOWN receipt is rejected. / 元组错误、Key/Epoch 过期、已撤销或 UNKNOWN Receipt 均拒绝。 |
| ST-FG-006 | Atomic LifecycleEvent + projection/outbox / LifecycleEvent 与 Projection/Outbox 原子性 | No half-committed lifecycle event or outbox-visible success. / 不得出现半提交 LifecycleEvent 或 Outbox 可见成功。 |
| ST-FG-007 | ACK loss after terminalization commit / 终态化提交后 ACK 丢失 | Same event digest returns same durable outcome. / 同一 Event Digest 返回同一持久化结果。 |
| ST-FG-008 | DB failover / DB Failover | No dual event sequence, stale Fence, or rollback of committed terminalization. / 不得出现双事件序列、旧 Fence 或已提交终态化回滚。 |
| ST-FG-009 | Restore stale snapshot / 恢复旧 Snapshot | Restore remains quarantined until D/I control continuity is proven. / D/I 控制连续性证明前保持隔离。 |
| ST-FG-010 | Late derivative after D proof / D Proof 后迟到 Derivative | Old proof invalidated; active Fence preserved; Storage never exposes late artifact. / 旧证明失效；活动 Fence 保留；Storage 永不暴露迟到 Artifact。 |

A PASS requires a real run against an identified database/runtime profile and exact commit, with transaction traces, fault injection, durable-row/pointer inspection and recovery output. A logical reference model or mocked callback is not physical Storage conformance.

PASS 必须基于明确数据库/运行时 Profile 和精确 Commit 的真实执行，并保留事务 Trace、故障注入、持久化行/Pointer 检查及恢复输出。逻辑 Reference Model 或 Mock Callback 不构成物理 Storage 符合性。

---

## 7. Existing Storage status and remaining gaps / 现有 Storage 状态与剩余缺口

At the inspected Storage baseline:

在已检查的 Storage 基线：

- Phase 3.8 visibility contract is a logical transaction proposal; physical topology and implementation proof are OPEN.
- Phase 3.8.2 ADR selects L1 logical Option A, but L4 physical engine/deployment remains OPEN.
- T1–T8 remain OPEN: runtime identity, D/Storage row boundary, linearization tests, I proof validation, atomic outcome traces, HA/restore, read-path enforcement and exact Owner decisions.
- The existing Phase 3.8 publication contract covers derivative visibility. It does not by itself prove the proposed dedicated D Forgotten LifecycleEvent CAS path.
- Storage role reviews elsewhere explicitly state that schema/reference-model CI does not prove live owner-ledger enumeration, owner-local currentness CAS, actual topology, JF-10 physical resolution or production atomicity.

- Phase 3.8 Visibility 契约是逻辑事务提案；物理拓扑和实现证明仍 OPEN。
- Phase 3.8.2 ADR 选择 L1 逻辑 Option A，但 L4 物理引擎/部署仍 OPEN。
- T1–T8 仍 OPEN：运行时身份、D/Storage Row 边界、线性化测试、I Proof 验证、原子结果 Trace、HA/Restore、Read Path 执行和精确 Owner 决策。
- 现有 Phase 3.8 Publication 契约覆盖 Derivative Visibility，但它本身不能证明本提案专用 D Forgotten LifecycleEvent CAS 路径。
- 其他 Storage 角色审查明确指出：Schema/Reference Model CI 不证明真实 Owner Ledger 枚举、Owner-local Currentness CAS、实际拓扑、JF-10 物理解析或生产原子性。

---

## 8. Storage decision required / 必需 Storage 决策

Storage can accept this proposal only as a logical contract direction. Before normative adoption, Storage must:

Storage 目前只能将本提案作为逻辑契约方向接受。成为规范前，Storage 必须：

1. review and accept the exact D Phase 3.9 Blob, especially immediate Fence read suppression vs barrier closeout;
2. review and accept the exact I/D Phase 3.9-I receipt schema/semantics;
3. add the lifecycle-terminalization transaction to the Storage row/transaction topology and identify the exact commit boundary;
4. demonstrate I receipt verification and D Fence/proof CAS at that boundary without cross-namespace counter comparison;
5. provide real DB/HA/restore/fault-injection evidence for ST-FG-001..010;
6. record exact Storage Owner decision and any exceptions on this exact Blob.

1. 审查并接受精确 D Phase 3.9 Blob，尤其是 Fence 立即读抑制与 Barrier 关闭的区分；
2. 审查并接受精确 I/D Phase 3.9-I Receipt Schema/语义；
3. 将 Lifecycle-Terminalization 事务加入 Storage Row/Transaction 拓扑并明确精确提交边界；
4. 在该边界证明 I Receipt 验证与 D Fence/Proof CAS，不进行跨命名空间计数器比较；
5. 为 ST-FG-001..010 提供真实 DB/HA/Restore/故障注入证据；
6. 针对本精确 Blob 记录 Storage Owner 决议和任何例外。

Until then: **CONDITIONAL LOGICAL REVIEW / PHYSICAL IMPLEMENTATION NOT VERIFIED / NOT FROZEN**.

在此之前：**逻辑审查有条件接受 / 物理实现未验证 / 未冻结**。

---

## 9. Exact source artifacts / 精确来源制品

Storage baseline branch: `session-storage-consistency-forget-atomicity-2026-11-16` @ `830a559bd2f4ec72608f5a51e1a0b43779f2b989`.

Storage 基线分支：`session-storage-consistency-forget-atomicity-2026-11-16` @ `830a559bd2f4ec72608f5a51e1a0b43779f2b989`。

- `reviews/storage-consistency/phase-3.8-storage-visibility-participant-and-atomic-outcome-contract.md` — Blob `175ee7b1349cfdb79a19898b311a88391ed88010`.
- `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md` — Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`.
- `reviews/storage-consistency/phase-3.7-storage-atomic-producer-registration-dependency-visibility-realization.md` — Blob `2ab899ee37a18ae6c8f2f64dbb82ad6499842060`.
- `reviews/storage-consistency/forget-atomicity-storage-realization-review.md` — Blob `107d21bd2c604ee0b04feff2ee5580e1de9c7fce`.

