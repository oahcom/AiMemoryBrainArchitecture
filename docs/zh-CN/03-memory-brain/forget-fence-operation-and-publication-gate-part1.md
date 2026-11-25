# Forget Fence 原子性、Producer Admission 与 Publication Gate — 第 1 部分

- 文档 ID：D-FORGET-GATE-001-P1
- 源分支：session-d-memory-brain-2026-11-16
- 源文件版本：DEREFERENCED — 保留历史源 Blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`；当前仓库不存在可解析的规范性源文件。
- 对应英文：[Part 1 — Forget Fence Atomicity, Producer Admission and Publication Gate](../../en/03-memory-brain/forget-fence-operation-and-publication-gate-part1.md)
- 源规范：DEREFERENCED — 原规范源路径 `03-memory-brain/forget-fence-operation-and-publication-gate.md` 在当前 main tree 中不存在；替代物：[英文对照版](../../en/03-memory-brain/forget-fence-operation-and-publication-gate-part1.md)（Blob `a090c79ff79de0c88d309281fcc6edfce4ac91ca`；仅为对照文本，不是规范性替代源）。
- 覆盖源规范第 1–5 节

## 1. 规范性不变量

1. 在获得持久化 ProducerWork Registration Receipt 之前，任何具备派生能力的 Producer 都不得 Enqueue、Lease、解引用受保护 Source Payload、执行、Retry、DLQ Replay 或 Publish。
2. Producer Class 必须先在带版本的 Registry 中登记并启用，才能 Admission。未知、禁用、未登记或 Registry 不完整的 Class 必须 Fail-closed。
3. ProducerWork Registration 与 Fence Installation 必须参与受影响 Brain Authority 和 Source Lineage 的同一个可线性化排序域。
4. 与 Fence Installation 并发的 Registration，要么在 Fence Snapshot 之前提交并纳入 Barrier，要么排在 Fence 之后并被拒绝/隔离。不能存在已 Admission、未核算但仍能发布的 Work。
5. Artifact 可见之前，完整 Dependency Registration 必须持久化。部分或结果不确定的 Registration 必须使 Artifact 保持 Private。
6. 最新适用 ForgetFence 必须在 Artifact 从 Private 变为 Visible 的同一原子/可线性化边界检查。先读取 Fence、稍后在没有共享 Fence 的情况下消费一次性 Token，不足以保证安全。
7. Final Gate 必须独立重新验证 PermissionEpoch。ForgetFenceGeneration 和 PermissionEpoch 是不同类型、不同 Namespace；禁止数值排序、比较或转换。
8. Retry 和 Lease 替换必须保留 ProducerWorkItemId 与 Lineage；AttemptId/LeaseId 只标识执行，不产生新的 Admission Authority。Recompile 使用新的 DerivationRunId 和明确关联的 Child/Re-admission 决策，不能使用无关联 Work Identity。
9. Timeout、ACK 丢失、Lease 过期、Receipt 缺失、Registry Gap、DLQ 状态，或无法获取最新 Fence/Permission，均表示未解决，必须阻止 Publication/Barrier Closure。
10. DLQ Replay、Restore、Rebuild、Backfill 和 Re-index 必须复用或明确关联原 Source Lineage，并在可见前重新检查当前 Fence/Permission。

## 2. 类型化身份与证据词汇

| 类型 | Owner / 范围 | 语义 |
|---|---|---|
| ProducerClass | D Registry；稳定 Class Identity + Contract Version | 已登记的、具有派生能力的 Producer 类别 |
| ProducerRegistryVersion | D | Producer Class Registry 及启用/禁用状态的不可变版本 |
| ProducerWorkItemId | D Ledger | 跨 Retry/Lease 变化的一个逻辑派生 Work Item |
| RegistrationReceipt | D | 持久化 Admission 结果，绑定 Work ID、Request Digest、Class、Source Lineage/Scope、Registry Version 和 Registration Sequence |
| ProducerRegistrationSequence / HighWater | D Ledger | Producer Work Ledger 中的单调位置；不是 Canonical Cursor、Fence Generation 或 Permission Epoch |
| ForgetFenceGeneration | D Forget Authority | ForgetFence Namespace 中的单调 Generation |
| ForgetFenceCursor | D | 类型化 Tuple：(ForgetOperationId, ForgetFenceGeneration, TargetSetDigest)；Installation CanonicalCommitCursor 是独立审计证据 |
| PermissionEpoch | I | I Policy Namespace 中不透明的授权/撤销 Epoch |
| DerivedArtifactRef/version | E Artifact Identity；登记在 D Inventory | 不可变 Staged Derivative 身份/版本 |
| DependencyRegistrationId / Receipt | D Inventory | 稳定幂等身份和持久化 Artifact/Source Lineage 证据 |
| PublicationOperationId / Receipt | D Gate 语义 | 稳定幂等身份和最终可见性结果 |
| CanonicalCommitCursor | D；单个 Brain Authority | Commit 排序/审计 Cursor；不是 Fence 或 Registration Sequence |
| AttemptId / LeaseId / DerivationRunId | E | Attempt、Lease 和派生执行身份；不能替代 WorkItemId |

ProducerRegistrationSequence、CanonicalCommitCursor、AggregateRevision、LifecycleEventCursor、ForgetFenceGeneration、PermissionEpoch、IndexWatermark 和 ContextVersion 之间禁止进行算术运算、数值比较、类型转换或相互替代。D 根据准确 Target Lineage 评估类型化 Fence 覆盖/新鲜度；I 评估当前 Permission 是否有效。

## 3. 操作契约

以下名称是规范性语义操作，不表示对应公共 API 名称或 Wire Schema 已经存在。每个操作都必须返回持久化 Receipt 或类型化非成功结果。Request Digest 根据规范化后的类型化字段计算。

### 3.1 RegisterProducerClass

- **输入：** 已认证 Producer Owner Binding；ProducerClassId；Owner/Module；Contract/Schema Version；允许的 Source Reference Class；声明的 Derivative/Output Class；Scope/Security Domain 约束；能力（production、replay、rebuild、cleanup-only）；Idempotency Key 和 Canonical Request Digest。
- **输出：** ProducerClassRegistrationReceipt；ProducerRegistryVersion；ENABLED、DISABLED 或 QUARANTINED 状态；生效的 Registry Sequence。
- **幂等：** 相同 Owner + Class ID + Version + Digest 返回原 Receipt。相同 Identity 但 Digest 不同，返回 IDEMPOTENCY_CONFLICT。将 Class 绑定到不同 Owner/Capability Set，需要显式新版本和 Supersession。
- **错误：** UNKNOWN_OWNER、AUTHENTICATION_REQUIRED、CLASS_CONFLICT、UNSUPPORTED_SCHEMA、REGISTRY_INCOMPLETE、POLICY_DENIED。
- **线性化点：** 在 D 权威 Registry 中持久化 Commit Registry Version/Status。Work Admission 必须观察到已提交的 Enabled Version。
- **规则：** 未知 Class 绝不能隐式 Admission。禁用 Class 会阻止新 Work，但不删除既有 Registration；已有 Work 仍留在 Barrier 中直至 Terminal。Registry 完整性未知时，Forget Proof 保持开放。

### 3.2 RegisterProducerWork

- **输入：** ProducerWorkItemId；ProducerClassId + Registry Version；已认证 ProducerIdentity Binding 引用（由 H/I 校验，不接受 Payload 声明）；Source EventRef 和/或带准确 Revision 的 Canonical TypedObjectRef；Source/Transitive Lineage Digest 或获批的不透明 Token；ScopeRefs；ForgetOperation/Correlation/Causation Ref；Admission CanonicalCommitCursor 或 D 定义的 Genesis；已观察 ForgetFenceCursor；当前 PermissionEpoch/Authorization Decision Ref；Schema Version；Canonical Request Digest；可选初始 AttemptId/LeaseId。
- **输出：** RegistrationReceipt，绑定身份字段、ProducerRegistrationSequence、ProducerRegistryVersion、Admission 时观察到的 Fence、ACCEPTED/REJECTED/QUARANTINED/CLEANUP_ONLY Disposition，以及持久化 Lookup Key。
- **幂等：** 相同 WorkItemId + 相同 Canonical Digest 返回相同 Receipt/Sequence。相同 ID + 不同 Digest 返回 IDEMPOTENCY_CONFLICT，不能修改原 Registration。Retry 不创建第二条逻辑 Registration。
- **错误：** UNKNOWN_PRODUCER_CLASS、CLASS_DISABLED、FENCE_CLOSED、FENCE_UNKNOWN、PERMISSION_STALE_OR_DENIED、SCOPE_INVALID、SOURCE_LINEAGE_INVALID、REGISTRY_INCOMPLETE、IDEMPOTENCY_CONFLICT。
- **线性化点：** 在与 InstallForgetFence 使用同一排序域的 D Ledger 中持久化插入/接受 Work Row。Sequence 只能在此时分配。
- **Admission 规则：** 如果活动 Fence 覆盖任何 Source Ancestor，普通派生 Work 必须拒绝或隔离。调用方提供当前 Generation 并不能使已遗忘祖先重新具备资格。Fence 后只允许接纳 Suppression/Cleanup Work，不得发布普通派生物。
- **仅有 EventRef 的 Ingress：** Registration 可以早于 Canonical MemoryRef 创建。D 记录 EventRef/不透明 Lineage Token、Producer、Scope 和 Security Binding。Canonical Ref 可用后，E 必须在 Dependency Registration/Publication 前追加并链接准确 Ref/Revision。缺少 MemoryRef 不代表可以省略 Lineage。

### 3.3 InstallForgetFence

- **输入：** 持久化 ForgetOperationId；I Authorization Decision Ref；准确 Target TypedObjectRef/Version Family；ScopeRefs；Target Set Digest；Idempotency Key + Request Digest；适用时的 Expected Fence State。
- **输出：** 持久化 ForgetFenceCursor；安装时的 CanonicalCommitCursor；捕获的 ProducerRegistryVersion；捕获的 ProducerRegistrationHighWater；Target Inventory Snapshot/Watermark；Fence Receipt 和可恢复 Outbox Intent。
- **幂等：** 相同 Operation + 相同 Target/Request Digest 返回相同 Receipt/Generation。相同 Operation ID 但 Target Digest 改变，返回 IDEMPOTENCY_CONFLICT。重复 Delivery 不分配新 Generation。
- **错误：** AUTHORIZATION_REQUIRED、TARGET_SET_INVALID、IDEMPOTENCY_CONFLICT、FENCE_STATE_CONFLICT、REGISTRY_INCOMPLETE、SERIALIZATION_RETRY_EXHAUSTED。
- **线性化点：** 一个持久化 Canonical Transaction/Serializable Commit，在同一个 Admission/Fence 排序顺序下使 Fence 生效并捕获 Producer Registration High-water。Installation CanonicalCommitCursor 是审计顺序，不是 Fence Generation。
- **原子效果：** 抑制 Target Lineage 的普通读取/发布；分配下一个 D FenceGeneration；持久化 Target Digest 和准确 Ref；捕获 ProducerRegistrationHighWater/ProducerRegistryVersion；持久化 Inventory Snapshot/Watermark 和 Outbox Intent。
- **规则：** 如果不能证明 Registry 完整，已知 Target 可以被抑制，但 Barrier 状态必须是 BLOCKED_REGISTRY_INCOMPLETE；不得声称 Canonical Suppression 已完成。

### 3.4 CaptureProducerRegistrationHighWater

- **输入：** ForgetOperationId + ForgetFenceCursor；Expected Registry Version；可选 Reconciliation Checkpoint。
- **输出：** 不可变 BarrierSnapshotReceipt，包含捕获的 High-water、Registry Version、Target Digest、Fence Generation 和 Ledger Consistency Proof/Ref。
- **幂等：** 相同 Fence + Snapshot Key 返回相同 Receipt。重复 Capture 不得推进该 Fence 的 Barrier。后续 Reconciliation Checkpoint 必须显式带版本，不能抹除未解决条目。
- **错误：** FENCE_NOT_INSTALLED、FENCE_MISMATCH、REGISTRY_INCOMPLETE、LEDGER_GAP、SNAPSHOT_UNAVAILABLE。
- **线性化点：** 与 Fence Installation Transaction/Version 绑定的一致 Snapshot Read。如果无法证明它对应安装时的 Serialization Point，必须返回 Unavailable，不能返回近似 High-water。
- **规则：** 这不是第二个 Admission Cutoff。InstallForgetFence 已建立不可变 Cutoff；Capture 只负责取回/验证它。

### 3.5 RegisterDerivedDependency

- **输入：** DependencyRegistrationId；DerivedArtifactRef/Version；ProducerWorkItemId；DerivationRunId；AttemptId/LeaseId；ProducerClass；准确 Source Ref/Revision 和 EventRef；直接 Parent Artifact Ref + Dependency Receipt Ref；完整 Lineage Digest；ProvenanceRef；ScopeRefs；已观察 ForgetFenceCursor；当前 PermissionEpoch/Authorization Ref；Schema Version 和 Canonical Digest。
- **输出：** DependencyRegistrationReceipt，包含 Inventory Position、Artifact/Version、Work/Run/Attempt、Source/Parent Ref 和 Digest、Scope、Fence Observation、Permission Evidence Ref，以及 REGISTERED/REJECTED/QUARANTINED 状态。
- **幂等：** 相同 DependencyRegistrationId + 相同 Digest 返回原 Receipt。相同 ID + 不同 Digest 返回 IDEMPOTENCY_CONFLICT。相同不可变 Artifact/Version 和 Lineage 返回相同 Receipt；Lineage 变化必须创建新的不可变 Artifact Version 和 Registration Identity。
- **错误：** WORK_NOT_REGISTERED、WORK_TERMINAL、SOURCE_FENCED、FENCE_UNKNOWN、PERMISSION_STALE_OR_DENIED、LINEAGE_INCOMPLETE、SCOPE_MISMATCH、ARTIFACT_ID_CONFLICT、IDEMPOTENCY_CONFLICT。
- **线性化点：** 在 D Inventory 中持久化 Commit Artifact Dependency Record 和全部必需 Edge。如果 Inventory 跨 Store，必须使用已证明的持久化 Prepare/Commit 协议；部分 Edge Set 不构成成功 Registration。
- **可见性规则：** Receipt 是必要条件，但不足以单独使 Artifact 可见。只有 PublishDerivedIfFenceCurrent 提交 Visibility 后，Artifact 才可见。

### 3.6 PublishDerivedIfFenceCurrent

- **输入：** PublicationOperationId；DerivedArtifactRef/Version；ProducerWorkItemId；DerivationRunId；AttemptId/LeaseId；ProducerClass；全部 DependencyRegistrationReceipt ID 和 Lineage Digest；ScopeRefs；已观察 ForgetFenceCursor；当前 I PermissionEpoch + Authorization Decision Ref；RegistrationReceipt；Request Digest；Private Staging Object/Version Ref。
- **输出：** 持久化 PublicationReceipt，绑定 WorkItem/Attempt、Class、Source MemoryVersion/Revision Ref、ScopeRefs、RegistrationReceipt、观察到及权威判定的 Fence、PermissionEpoch Decision Ref、Artifact Identity、完整 Dependency Evidence、Visibility Commit ID/Cursor，以及 PUBLISHED、REJECTED_FENCED、REJECTED_PERMISSION、REJECTED_INCOMPLETE 或 QUARANTINED Disposition。
- **幂等：** 相同 PublicationOperationId + 相同 Digest 返回原 Receipt/Outcome。相同 Key + 不同 Digest 返回 IDEMPOTENCY_CONFLICT。ACK 丢失时按同 Operation ID 查询；不确定 Commit 时绝不创建新 Key。
- **错误：** DEPENDENCY_NOT_DURABLE、REGISTRATION_NOT_DURABLE、WORK_NOT_ACTIVE、ATTEMPT_STALE、LEASE_STALE、FENCE_ADVANCED_OR_COVERS_ANCESTOR、FENCE_UNKNOWN、PERMISSION_EPOCH_STALE_OR_REVOKED、SCOPE_MISMATCH、ARTIFACT_ALREADY_PUBLISHED、IDEMPOTENCY_CONFLICT、STORAGE_ATOMICITY_UNAVAILABLE。
- **线性化点：** 单个持久化 Visibility Commit；在该点校验当前 D Fence 和 Dependency/Registration State、I Authorization 是否当前有效，并使 Artifact 可见。Fence Installation 与该 Commit 必须在同一个 Consistency Domain 串行化。如果 Publish 获胜，Artifact 在 Fence 前可见，且必须纳入 Dependency/Barrier Inventory；如果 Fence 获胜，Publication 被拒绝。成功 Gate Receipt 不能先于独立 Visibility Write。
- **Storage 要求：** 首选语义是一个 Atomic Transaction/CAS 同时覆盖 Gate Validation 和 Visibility Marker。如果 Store 分离，Storage/Consistency 必须定义并证明等价协议：持久化 Hidden Prepare；Fence/Permission Validation 绑定 Prepare；Commit Token/Record 与 Visibility CAS 原子消费；Recovery 使不确定 Artifact 保持隐藏；Fence Installation 与同一个 Commit Decision 串行化。Fence 推进后仍可重放的 Token，或未协调的 Check-then-write，均无效。
- **Permission 规则：** 按 I 的权威语义检查 PermissionEpoch 当前有效性/相等性；绝不与 FenceGeneration 做数值比较。如果 I 无法在 Visibility Boundary 提供当前 Decision，则 Fail-closed。
- **Lineage 规则：** 检查每个 Source Ancestor 和 Target Scope，而不只是直接 Parent/Artifact ID。新的 Artifact ID 或 Recompile 不能重置 Lineage 资格。

### 3.7 CompleteProducerWork

- **输入：** ProducerWorkItemId；最终 AttemptId/LeaseId；Disposition；所有 Output Artifact Ref 和 Dependency/Publication Receipt；适用时的 Canonical Commit Ref；Terminal Reason/Error Class；证明不会再有 Attempt 发布的证据；Producer Owner Binding；Request Digest。
- **输出：** ProducerWorkTerminalReceipt；Barrier Ledger State；未解决 Output 数量；Reconciliation Cursor。
- **幂等：** 相同 Work ID + 相同 Terminal Digest 返回相同 Receipt。冲突的 Terminal Digest 返回 TERMINAL_CONFLICT；禁止静默覆盖/降级。
- **错误：** WORK_UNKNOWN、WORK_NOT_REGISTERED、OUTPUT_UNRECONCILED、PUBLICATION_UNKNOWN、LEASE_STILL_VALID、REPLAY_STILL_POSSIBLE、TERMINAL_CONFLICT、EVIDENCE_INCOMPLETE。
- **线性化点：** 验证 Evidence 后，在 D Barrier Ledger 中持久化 Commit Terminal Disposition。Lease Expiry、Queue Deletion、Worker Shutdown 和 DLQ Parking 都不是 Terminal Evidence。
- **规则：** Terminal Disposition 必须单调。后来发现派生物/Publication 时，当前 Barrier Proof 失效并重新打开 Reconciliation，但不改写历史。

### 3.8 ResolveProducerWork

- **输入：** ProducerWorkItemId + 原始 Registration Digest；可选 AttemptId/LeaseId；DependencyRegistrationId 和/或 PublicationOperationId；调用方 Correlation ID。
- **输出：** 权威 RegistrationReceipt、Dependency Receipt、PublicationReceipt、Terminal Receipt、当前 Lease/Attempt 状态和 Barrier Membership。
- **幂等：** 只读且可重复；Lookup 不创建 Work，也不推进 Fence。
- **错误：** WORK_UNKNOWN、DIGEST_MISMATCH、RECEIPT_NOT_RETAINED、AUTHORIZATION_REQUIRED、LEDGER_UNAVAILABLE。
- **线性化点：** 从权威 Ledger/Receipt Store 的指定 Snapshot 进行一致读取。如果无法确定当前状态，返回 UNKNOWN；调用方继续 Fail-closed。
- **规则：** Recovery 复用原 ID/Digest。仅有 Timeout 既不代表成功，也不代表失败。

### 3.9 ReconcileForgetBarrier

- **输入：** ForgetOperationId + ForgetFenceCursor；BarrierSnapshotReceipt；Registry Version；Dependency Inventory Snapshot/Cursor；Reconciliation Checkpoint；Target Inventory/Watermark；Terminal/Publication Receipt。
- **输出：** BarrierReconciliationReceipt，包含准确 High-water、纳入 Work 数、Terminal 数、Open/Expired/DLQ/Unknown 数、Dependency Inventory Watermark、迟到派生物数量、未解决 Registry Gap，以及 DRAINED、OPEN_WORK、OPEN_DEPENDENCY、REGISTRY_GAP、LATE_DERIVATIVE 或 UNKNOWN Disposition。
- **幂等：** 相同 Snapshot/Checkpoint 返回相同确定性 Receipt。新 Evidence 创建追加式 Reconciliation Receipt；旧 Receipt 仍可审计。
- **错误：** FENCE_UNKNOWN、SNAPSHOT_MISMATCH、LEDGER_GAP、DEPENDENCY_INVENTORY_GAP、REGISTRY_INCOMPLETE、RECONCILIATION_UNAVAILABLE。
- **线性化点：** 在明确版本化 Checkpoint 上，对 Barrier Ledger、Dependency Inventory 和 Target Inventory 进行一致 Read/Snapshot。DRAINED 只对这些不可变 Checkpoint 有效；后来发现 Fence 前 Work 或迟到派生物时，当前完成状态失效，必须重新协调。
- **规则：** 只有 D 可以声明 D-local Canonical Barrier 结果。I 决定它是否足以支持 Global Forget；它不是 Physical Erasure Evidence。

## 4. Registration/Fence/Publish 状态转换

ProducerClass：UNREGISTERED → ENABLED → DISABLED 或 QUARANTINED。新 Admission 要求 ENABLED；既有 Work 继续跟踪。

ProducerWork：ABSENT → REGISTERED → QUEUED → LEASED → RUNNING → STAGED → DEPENDENCY_REGISTERED → PUBLISH_PENDING → PUBLISHED → TERMINAL。Retry 使用相同 WorkItemId 和新的 AttemptId 返回 QUEUED。DLQ 保持 Barrier-open。Lease Expiry 是 Attempt Condition，不是 Terminal。只有具备持久化“不再发布”证据时，Suppression/Quarantine 才可终结。Recompile 创建新的 DerivationRunId，并明确链接原始 Lineage。

Forget：REQUESTED → FENCE_INSTALLED + 不可变 BarrierSnapshot → BARRIER_OPEN → BARRIER_DRAINED → TARGET_RECONCILIATION → D_CANONICAL_SUPPRESSION_PROVEN。Registry Gap、迟到派生物、未知 Lease/Publication 或缺失 Dependency 都会阻止/重新打开 Proof。

Publish：PRIVATE_STAGED → DEPENDENCIES_DURABLE → FINAL_GATE_PENDING →（Fence + Permission + Visibility 原子提交）→ VISIBLE。任何拒绝都保持 Private/Quarantined。不存在“Gate 已批准，Artifact 稍后才可见”的中间许可状态。

## 5. Registration/Fence 竞争：只有两种合法结果

Registration 与 Fence Installation **MUST** 在共享 D Consistency Boundary 或正式证明等价的机制上串行化。

| 串行化获胜者 | 必需结果 | Barrier Membership | Publication 资格 |
|---|---|---|---|
| RegisterProducerWork 先提交 | Durable Receipt，Sequence 为 s；Fence 捕获 High-water H >= s | 纳入不可变的 Fence 前 Barrier | 只能继续到 Final Gate；若 Fence 覆盖 Source，必须在 Publication 前抑制 |
| InstallForgetFence 先提交 | Fence 生效并捕获 H；后续 Registration 观察到 Fence | 不得作为普通派生 Work Admission；拒绝/隔离或仅 Cleanup-only | 不允许普通 Publication |
| 并发/结果不明确 | 按稳定 ID/Digest 解析；由权威顺序决定上述两种结果之一 | 仅当 Registration Commit 早于 Fence Point 时纳入 | Unknown 保持 Private，不能 Publish |

不存在一种合法结果可以让已接受 Registration 不在捕获的 High-water 中。也不存在一种合法结果可以让 Fence 后针对被覆盖 Source 的普通 Work 获得 Accepted。如果实现无法证明哪一个 Operation 先线性化，则必须返回/保留 UNKNOWN，并在 Reconciliation 前阻止 Execution/Publication。
