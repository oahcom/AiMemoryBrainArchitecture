# Phase 3.9 — D Forget Terminal Semantics and Fence/Publication Linearization Closure Proposal
# Phase 3.9 — D Forget 终态语义与 Fence/Publication 线性化闭合提案

**Status / 状态:** PROPOSAL — NOT NORMATIVE / 提案 — 尚非规范  
**Owner / 责任方:** D (semantic authority), with mandatory Storage and I concurrence / D（语义权威），必须取得 Storage 与 I 会签  
**Review baseline / 审查基线:** `session-d-memory-brain-2026-11-16` @ `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f`  
**Purpose / 目的:** Resolve review findings D-001, D-002 and D-003 without silently superseding existing controlling contracts. / 在不暗中替代现有控制性契约的前提下，解决 D-001、D-002、D-003。

> This document is a proposed closure package. It does not amend the controlling D contracts until D approves the exact blob and Storage/I approve the cross-owner clauses. No implementation, test execution, production behavior, or global/physical erasure is claimed.
>
> 本文档是拟议闭合包。在 D 批准精确 Blob 且 Storage/I 批准跨 Owner 条款之前，不修改现行控制性 D 契约。本文件不声称已完成实现、测试执行、生产行为变更、全局 Forget 或物理擦除。

---

## 1. Normative separation of four outcomes / 四类结果的规范隔离

The following terms are distinct nominal outcomes. No event, API field, UI label, metric or receipt may substitute one for another.

以下术语代表四种不同的名义结果。任何事件、API 字段、UI 标签、指标或 Receipt 均不得相互替代。

| Term / 术语 | Sole authority / 唯一权威 | Minimum meaning / 最低含义 | Explicitly does not mean / 明确不代表 |
|---|---|---|---|
| `CanonicalSuppressionComplete` | D | D's closed producer/derivative barrier is proven; all required canonical targets are suppression-confirmed or carry an exact I-approved residual exception. / D 已证明 Producer/Derivative Barrier 闭合；所有必需规范目标均已确认抑制，或具有精确的 I 批准残余例外。 | Global Forget, cleanup everywhere, backup erasure, provider erasure, physical erasure. / 全局 Forget、全域清理、备份擦除、Provider 擦除、物理擦除。 |
| `Memory.lifecycle = Forgotten` | D, subject to I's current governance criterion | An immutable LifecycleEvent commits the canonical Memory identity to its terminal logical state. / 不可变 LifecycleEvent 将规范 Memory 身份提交为逻辑终态。 | Physical deletion or proof that every external copy is erased. / 物理删除或所有外部副本均已擦除的证明。 |
| `GlobalForgetCompleted` | I | I's policy evaluator attests that all in-scope governance obligations are satisfied or covered by explicitly permitted exceptions. / I 的策略评估器证明所有范围内治理义务均已满足或由明确允许的例外覆盖。 | A D-local lifecycle event or a single module ACK. / D 本地生命周期事件或单一模块 ACK。 |
| `PhysicalErasureConfirmed` | Each relevant storage/copy authority, governed by I | The responsible authority provides scoped, verifiable evidence for its own physical-erasure obligation. / 相应责任方为其物理擦除义务提供有范围、可验证的证据。 | Inference from suppression, tombstone, key unavailability, timeout or logical deletion. / 从抑制、墓碑、密钥不可用、超时或逻辑删除推断。 |

### 1.1 LifecycleEvent rule / LifecycleEvent 规则

D may append `Memory.lifecycle = Forgotten` only when both conditions hold:

D 只有在以下两个条件同时满足时，才可追加 `Memory.lifecycle = Forgotten`：

1. D has a current, durable `CanonicalSuppressionComplete` proof for the exact Memory identity/version family, scope and ForgetOperation.
2. I supplies a current, authenticated governance decision that explicitly authorizes the D lifecycle terminalization under the applicable policy version and permission epoch.

The LifecycleEvent MUST carry typed references to both proofs and their exact digests. It MUST NOT copy forgotten payload. The event records logical terminalization, not physical erasure.

LifecycleEvent 必须携带上述两项证明的类型化引用及精确摘要，不得复制被遗忘内容。该事件记录逻辑终态化，不代表物理擦除。

If either proof is stale, revoked, unknown, scope-mismatched or digest-mismatched at the commit point, the event MUST NOT commit. The operation remains blocked/resumable; the fence is not rolled back.

如果任一证明在提交点已过期、撤销、未知、Scope 不匹配或摘要不匹配，则不得提交该事件。Operation 保持阻塞/可恢复状态；Fence 不得回滚。

---

## 2. One monotonic ForgetOperation phase machine / 唯一单调 ForgetOperation 阶段机

Memory lifecycle and ForgetOperation phase are separate types. The Memory lifecycle remains:

Memory 生命周期与 ForgetOperation 阶段属于不同类型。Memory 生命周期仍为：

`Candidate → Consolidated → Active → Superseded / Archived → Forgotten`

The ForgetOperation phase is proposed as the following single monotonic sequence:

ForgetOperation 阶段建议统一为以下单调序列：

| Phase / 阶段 | Entry condition / 进入条件 | Exit condition / 退出条件 |
|---|---|---|
| `REQUESTED` | Durable operation ID and scoped idempotency identity are committed. / 持久化 Operation ID 与有范围的幂等身份已提交。 | I authorization and request binding are resolved. / I 授权及请求绑定已确定。 |
| `AUTHORIZATION_PENDING` | Current I decision is being obtained or refreshed. / 正在获取或刷新 I 当前决策。 | Valid current decision → coverage evaluation; denied/revoked → pre-fence rejection. / 当前有效决策进入覆盖评估；拒绝/撤销则 Fence 前拒绝。 |
| `COVERAGE_BLOCKED` | Target/producer/lineage coverage cannot yet be proven. / 尚不能证明目标、Producer 或 Lineage 覆盖完整。 | Coverage proof complete → fence installation; otherwise remain blocked. / 覆盖证明完整后安装 Fence，否则保持阻塞。 |
| `FENCE_INSTALLED` | Fence generation, request scope, target selector and producer-registration high-water are atomically committed. / Fence Generation、请求 Scope、目标选择器和 Producer Registration High-water 原子提交。 | Inventory and pre-fence participants reconciled. / Inventory 与 Fence 前 Participant 完成核对。 |
| `INVENTORY_RECONCILIATION` | Durable target inventory and lineage closure are being reconciled. / 正在核对持久化目标 Inventory 和 Lineage 闭包。 | Complete inventory snapshot/watermark → barrier drain. / 完整 Inventory Snapshot/Watermark 进入 Barrier Drain。 |
| `BARRIER_DRAINING` | Every pre-fence registered producer/publication participant is accounted for. / 正在核算所有 Fence 前已注册 Producer/Publication Participant。 | Every member has an authoritative terminal disposition; no gaps/unknowns. / 每个成员均有权威终态处置，无缺口、无未知。 |
| `TARGET_RECONCILIATION` | Per-target suppression/cleanup acknowledgements and permitted exceptions are reconciled. / 正在核对逐目标抑制/清理 ACK 与允许的例外。 | Every required target has suppression confirmation or exact I-approved exception. / 每个必需目标均已确认抑制或具有精确 I 批准例外。 |
| `CANONICAL_SUPPRESSION_COMPLETE` | D proof is durably committed and binds exact closed-world evidence. / D 证明已持久化提交并绑定精确闭世界证据。 | Terminal D phase; later discovery invalidates proof and creates a successor reconciliation epoch, never rolls back the active fence. / D 终态阶段；迟到发现使证明失效并创建后继核对 Epoch，但绝不回滚活动 Fence。 |

**Non-phase conditions / 非阶段条件**

- `BLOCKED` is an execution condition attached to the current phase, with a typed reason and retry/recovery policy; it is not a competing phase.
- `FAILED_PRE_FENCE` and `CANCELLED_PRE_FENCE` are terminal request outcomes permitted only before `FENCE_INSTALLED`.
- After `FENCE_INSTALLED`, cancellation/rollback is forbidden. Failures remain blocked/recoverable; an operator cannot lower the fence to make the operation appear complete.
- A post-fence permanent policy exception is not an implicit success. It requires an exact I-owned exception reference and remains visible in the proof.

- `BLOCKED` 是附着于当前阶段的执行条件，必须有类型化原因及重试/恢复策略，不是竞争性的阶段。
- `FAILED_PRE_FENCE` 与 `CANCELLED_PRE_FENCE` 仅允许在 `FENCE_INSTALLED` 之前作为终态请求结果。
- `FENCE_INSTALLED` 之后禁止取消或回滚。失败保持阻塞/可恢复；操作者不得降低 Fence 以制造完成假象。
- Fence 后的永久策略例外不构成隐式成功，必须引用精确的 I 所有者例外，并在证明中保持可见。

### 2.1 Field typing / 字段类型

Replace ambiguous generic completion fields in the D Forget contract with typed fields:

D Forget 契约中含义模糊的通用完成字段应替换为类型化字段：

- `d_canonical_suppression_proof_ref`
- `canonical_suppression_completed_at`
- `global_forget_attestation_ref` (I-owned reference only; D cannot mint it)
- `physical_erasure_evidence_refs[]` (external authority references only; D cannot mint them)
- `lifecycle_terminal_event_ref`
- `phase`, `execution_condition`, `blocked_reason_code`

The schema MUST reject a generic D-owned `complete`, `completion_proof_ref` or `completed_at` when its meaning is not explicitly typed.

当含义未被明确类型化时，Schema 必须拒绝 D 所有的通用 `complete`、`completion_proof_ref` 或 `completed_at` 字段。

---

## 3. Fence linearization and immediate read suppression / Fence 线性化与立即读抑制

This section is a mandatory D/Storage joint decision. It proposes separating the **read-suppression effect** from the **barrier-drain completion** so an unresolved pre-fence publication participant cannot keep ordinary reads exposed indefinitely.

本节必须由 D/Storage 联合决策。建议将**读抑制生效**与**Barrier Drain 完成**分离，避免未决的 Fence 前发布 Participant 无限期维持普通读取暴露。

### 3.1 Proposed linearization point / 建议线性化点

The linearization point is the durable commit of `InstallForgetFence` in the shared authoritative ordering domain. That commit MUST atomically bind:

线性化点为共享权威排序域中 `InstallForgetFence` 的持久化提交。该提交必须原子绑定：

- ForgetOperationId and normalized request digest;
- target selector, target-set digest and exact Scope;
- new monotonic ForgetFenceGeneration;
- ProducerClass registry version and ProducerRegistrationSequence high-water;
- inventory snapshot/watermark and barrier generation;
- authenticated requester and current I authorization decision reference/version.

- ForgetOperationId 与规范化请求摘要；
- 目标选择器、目标集合摘要及精确 Scope；
- 新的单调 ForgetFenceGeneration；
- ProducerClass Registry 版本及 ProducerRegistrationSequence High-water；
- Inventory Snapshot/Watermark 与 Barrier Generation；
- 经认证的请求者及 I 当前授权决策引用/版本。

At this commit, the active fence becomes effective for canonical reads and all managed projection/delivery paths. Any path unable to establish the latest applicable fence MUST fail closed for affected targets. A stale cache, delayed invalidation message or unresolved publication participant MUST NOT authorize ordinary reads.

在该提交点，活动 Fence 对规范读取及所有受管理投影/交付路径立即生效。任何无法确定最新适用 Fence 的路径都必须对受影响目标 fail closed。过期缓存、延迟失效消息或未决发布 Participant 均不得授权普通读取。

### 3.2 Publication participant ordering / Publication Participant 排序

A PublicationParticipant admitted before the Fence is included in the captured barrier. Its earlier admission is **not** a durable right to publish after the Fence.

Fence 之前准入的 PublicationParticipant 必须纳入所捕获的 Barrier。其较早的准入**不构成** Fence 之后发布的永久权利。

There are exactly two visibility outcomes:

可见性只有两种合法结果：

1. Storage visibility commit linearizes before the Fence commit: the exact artifact may be visible before the Fence, but it must be included in the captured inventory and immediately suppressed by the newly effective Fence.
2. Fence commit linearizes before Storage visibility commit: Storage's final visibility gate MUST reject the commit and keep the artifact private; D records authoritative no-publication only after all retry/outbox/replay/delayed-publisher paths are proven unable to publish later.

1. Storage Visibility Commit 先于 Fence Commit 线性化：精确 Artifact 可在 Fence 前可见，但必须纳入捕获的 Inventory，并由新生效的 Fence 立即抑制。
2. Fence Commit 先于 Storage Visibility Commit 线性化：Storage 最终 Visibility Gate 必须拒绝提交并保持 Artifact 私有；只有证明所有 Retry/Outbox/Replay/Delayed Publisher 路径均不可能再发布后，D 才能记录权威 No-Publication。

A participant admitted before the Fence but not yet resolved remains an open barrier member. It delays `CanonicalSuppressionComplete`, but MUST NOT delay read suppression. `UNKNOWN / IN_DOUBT` keeps the barrier open and artifact private.

Fence 前已准入但尚未解决的 Participant 仍是开放的 Barrier Member。它可以延迟 `CanonicalSuppressionComplete`，但不得延迟读抑制。`UNKNOWN / IN_DOUBT` 保持 Barrier 开放并使 Artifact 保持私有。

### 3.3 Required race outcomes / 必测竞争结果

| Race / 竞争 | Required result / 必须结果 |
|---|---|
| Fence commit wins before final visibility commit / Fence 先于最终可见性提交 | Publish rejected; private artifact; barrier member resolves only with authoritative no-publication. / 拒绝发布；Artifact 保持私有；仅凭权威 No-Publication 解决 Barrier Member。 |
| Visibility commit wins before Fence / 可见性提交先于 Fence | Artifact is in the fence inventory and immediately suppressed at Fence commit. / Artifact 纳入 Fence Inventory，并在 Fence 提交时立即抑制。 |
| Participant admitted first, Storage outcome UNKNOWN / Participant 先准入，Storage 结果 UNKNOWN | Fence may be installed and read suppression takes effect; barrier remains open; no publication permission is inferred. / 可安装 Fence 并立即生效读抑制；Barrier 保持开放；不得推断具有发布许可。 |
| Stale read cache / 读取缓存过期 | Fail closed until current fence is established; cache invalidation ACK is not the source of truth. / 在确定当前 Fence 前 fail closed；缓存失效 ACK 不是事实来源。 |
| Crash after Storage prepare, before D participant admission / Storage Prepare 后、D Participant 准入前崩溃 | Storage artifact remains private; recovery joins by stable ID/digest; missing/ambiguous state is UNKNOWN. / Storage Artifact 保持私有；恢复时按稳定 ID/摘要 Join；缺失或歧义状态为 UNKNOWN。 |
| Late derivative after proof / 证明后迟到 Derivative | Immediately suppress; invalidate affected closed-world proof; create successor inventory/barrier epoch; never lower fence. / 立即抑制；使相关闭世界证明失效；创建后继 Inventory/Barrier Epoch；绝不降低 Fence。 |

---

## 4. Lifecycle terminalization CAS / 生命周期终态化 CAS

The `Forgotten` LifecycleEvent commit MUST be a compare-and-set over the following exact tuple:

`Forgotten` LifecycleEvent 提交必须对以下精确元组执行 Compare-and-Set：

`(MemoryId, MemoryVersion, ForgetOperationId, ScopeDigest, ForgetFenceGeneration, CanonicalSuppressionProofDigest, IAuthorizationDecisionId, PolicyVersion, PermissionEpoch, RevocationWatermark)`

The transaction MUST verify:

事务必须验证：

1. the Memory is not already terminalized under a conflicting operation;
2. the active fence generation is current and has not been rolled back;
3. the D suppression proof is current, complete and bound to the exact target/scope;
4. I's authorization decision is authenticated, unrevoked and current at commit time;
5. no policy/permission epoch change invalidates the decision;
6. the LifecycleEvent sequence/version expected by the caller is still current.

1. Memory 尚未被冲突 Operation 终态化；
2. 活动 Fence Generation 当前有效且未回滚；
3. D 抑制证明当前有效、完整并绑定精确目标/Scope；
4. I 授权决策已认证、未撤销且在提交时仍然有效；
5. 没有策略/权限 Epoch 变化使该决策失效；
6. 调用方期望的 LifecycleEvent Sequence/Version 仍为当前值。

Any failed or unknown predicate aborts the LifecycleEvent transaction. It does not clear the fence or turn the operation into success.

任何条件失败或未知都必须中止 LifecycleEvent 事务；不得清除 Fence，也不得把 Operation 转成成功。

---

## 5. Required executable evidence / 必需的可执行证据

The following are release-blocking tests, not merely documentation examples. Each result must record repository commit SHA, test command, fixture digest, environment/runtime version, exit code and machine-readable output.

以下是阻止 Release 的必需测试，不是文档示例。每项结果必须记录仓库 Commit SHA、测试命令、Fixture 摘要、环境/运行时版本、退出码和机器可读输出。

| Test ID | Scenario / 场景 | Required assertion / 必须断言 |
|---|---|---|
| D-FORGET-001 | Four terminal terms / 四种终态 | No D state/event/API can imply I global completion or physical erasure. / D 状态、事件或 API 均不得暗示 I 全局完成或物理擦除。 |
| D-FORGET-002 | Phase transition model / 阶段迁移 | Only declared monotonic transitions; cancellation impossible after fence. / 仅允许声明的单调迁移；Fence 后无法取消。 |
| D-FORGET-003 | Fence-first race / Fence 优先 | No later visibility commit; artifact remains private. / 后续可见性提交被拒绝；Artifact 保持私有。 |
| D-FORGET-004 | Publication-first race / Publication 优先 | Earlier visible artifact is inventoried and suppressed at Fence commit. / 先前可见 Artifact 被纳入 Inventory 并在 Fence 提交时抑制。 |
| D-FORGET-005 | Long UNKNOWN / 长期 UNKNOWN | Read suppression remains effective; barrier does not close. / 读抑制持续有效；Barrier 不得闭合。 |
| D-FORGET-006 | Stale cache / 过期缓存 | Affected reads fail closed. / 受影响读取 fail closed。 |
| D-FORGET-007 | Authorization revoke race / 授权撤销竞争 | Revocation before LifecycleEvent CAS prevents Forgotten commit. / LifecycleEvent CAS 前撤销授权将阻止 Forgotten 提交。 |
| D-FORGET-008 | Late derivative / 迟到派生物 | Prior proof invalidated; fence remains monotonic. / 旧证明失效；Fence 保持单调。 |
| D-FORGET-009 | Retry/DLQ/replay / 重试与回放 | No unregistered replay can publish; unknown member blocks completion. / 未注册回放不能发布；未知成员阻止完成。 |
| D-FORGET-010 | Restore/anti-rollback / 恢复与防回滚 | Restored state cannot expose a forgotten target using stale fence state. / 恢复状态不能利用旧 Fence 暴露已遗忘目标。 |

A test is PASS only when the test actually ran against the claimed commit and the output is retained. A test matrix, pseudocode, review statement or CI configuration without a run is NOT EVIDENCE.

只有测试确实在所声明 Commit 上执行且保留输出，才能标记 PASS。测试矩阵、伪代码、审查声明或没有运行记录的 CI 配置均不构成证据。

---

## 6. Owner decisions required / 必须取得的 Owner 决策

| Owner | Required exact-version decision / 必需的精确版本决策 |
|---|---|
| D | Approve four-outcome vocabulary, phase machine, field typing, LifecycleEvent CAS and D proof invalidation semantics. / 批准四类结果词汇、阶段机、字段类型、LifecycleEvent CAS 和 D 证明失效语义。 |
| Storage | Approve shared ordering-domain interpretation and the two visibility-vs-fence race outcomes; prove commit serialization and recovery behavior. / 批准共享排序域解释及两种可见性/Fence 竞争结果；证明提交序列化和恢复行为。 |
| I | Approve governance completion vocabulary, authorization-currentness tuple, exception binding and policy/permission epoch semantics. / 批准治理完成词汇、授权当前性元组、例外绑定及策略/权限 Epoch 语义。 |
| H | Confirm consumer behavior: current fence required; stale/unknown verifier result fails closed; ACK never substitutes for D proof. / 确认消费侧行为：必须取得当前 Fence；验证器过期/未知时 fail closed；ACK 永不替代 D 证明。 |
| A / Integration Reviewer | Verify exact blob identities, cross-owner compatibility, bilingual semantic parity and test evidence; reviewer must not be the author/implementer of the reviewed changes. / 核验精确 Blob 身份、跨 Owner 兼容性、双语语义一致性和测试证据；审查者不得是被审查改动的作者/实现者。 |

No row is accepted by silence, presence of a related document, or another Owner's approval. Each approval must cite the same exact proposal blob SHA and identify accepted clauses and exceptions.

任何一方不得因沉默、存在相关文档或另一 Owner 已批准而被视为接受。每项批准必须引用同一精确提案 Blob SHA，并标明接受条款和例外。

---

## 7. Exit criteria / 退出条件

D-001 through D-003 may be marked CLOSED only after:

只有满足以下条件，D-001 至 D-003 才能标记 CLOSED：

- the controlling D documents are updated or explicitly reference the accepted successor;
- D, Storage and I decisions are recorded against the same exact version;
- H consumer behavior is confirmed against that version;
- schema and contract tests enforce the typed outcomes and monotonic phase machine;
- all D-FORGET-001 through D-FORGET-010 tests have reproducible execution evidence;
- an independent non-implementing reviewer accepts the exact remediation head.

- 控制性 D 文档已更新，或明确引用获接受的后继版本；
- D、Storage、I 的决定均绑定同一精确版本；
- H 已针对该版本确认消费行为；
- Schema 与契约测试强制执行类型化结果和单调阶段机；
- D-FORGET-001 至 D-FORGET-010 均有可复现执行证据；
- 不参与实现的独立审查者接受精确整改 Head。

Until all criteria are met, the disposition remains **PROPOSAL / CHANGES REQUIRED / NOT FROZEN**. No merge, deployment, global Forget completion or physical-erasure claim follows from this proposal.

在全部条件满足之前，处置状态保持 **PROPOSAL / CHANGES REQUIRED / NOT FROZEN**。本提案不构成合并、部署、全局 Forget 完成或物理擦除声明。

---

## 8. Source documents / 来源文档

This proposal is based on the following exact D-branch files at baseline commit `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f`:

本提案基于基线 Commit `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` 中以下精确 D 分支文件：

- `03-memory-brain/memory-lifecycle-manager.md` — blob `8b972035b449e1eab546aedc9cc5b30581600c65`
- `03-memory-brain/forget-fence-and-completion-contract.md` — blob `1f0391bc49d007c44ec74165bd33d37412cc7990`
- `03-memory-brain/forget-fence-operation-and-publication-gate.md` — blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`
- `03-memory-brain/phase-3.6.6-d-forget-semantic-authority-addendum.md` — blob `a384ffb4fff7de9b35ba6b3011d2779ad529573d`
- `03-memory-brain/phase-3.6-joint-forget-linearization-decision.md` — blob `1b6a312ecffd3947bbb4df59f902242482c98a40`
- `03-memory-brain/phase-3.7-d-producer-class-registry-eventref-ingress-and-participant-intent.md` — blob `4c01713bc8793a8926ef18b625b72d132572173d`
- `03-memory-brain/phase-3.8-d-publication-participant-and-terminal-contract.md` — blob `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78`
- `03-memory-brain/phase-3.8.8-d-review-storage-serialization-anchor.md` — blob `cb1e71730c6fd1fe5eed5c643d2fd59eceba008a`
- `03-memory-brain/phase-3.8.9-d-review-h-forget-clearance-verifier-seam.md` — blob `53613f383d064d25ac9f34a00e457f86730f16bf`

