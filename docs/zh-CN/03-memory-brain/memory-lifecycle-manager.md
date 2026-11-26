---
document_metadata:
  domain: memory-brain
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "03-memory-brain/memory-lifecycle-manager.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Bilingual mirror of a candidate root restored by AID-2026-100; content acceptance and semantic parity review remain pending."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Bilingual mirror of 03-memory-brain/memory-lifecycle-manager.md"
    canonical_scope_id: "mirror/03-memory-brain/memory-lifecycle-manager"
    canonical_scope_keywords:
      - mirror
      - candidate
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "03-memory-brain/memory-lifecycle-manager.md"
    en: "docs/en/03-memory-brain/memory-lifecycle-manager.md"
    zh-CN: null
---

# Memory Lifecycle Manager（记忆生命周期管理器）

- 文档 ID：D-LIFECYCLE-001
- 版本：1.0
- 源分支：session-d-memory-brain-2026-11-16
- 源文件版本：DEREFERENCED — 保留历史源 Blob `8b972035b449e1eab546aedc9cc5b30581600c65`；当前仓库不存在可解析的规范性源文件。
- 审查时源分支 HEAD：6b654d5cffaeb71b01f2b0750daa0abc14eb64b3
- 源规范：DEREFERENCED — 原规范源路径 `03-memory-brain/memory-lifecycle-manager.md` 在当前 main tree 中不存在；替代物：[英文对照版](../../en/03-memory-brain/memory-lifecycle-manager.md)（Blob `856d7847261bc625cc089fb0bfa25096c28b4ff4`；仅为对照文本，不是规范性替代源）。
- 对应英文：[Memory Lifecycle Manager](../../en/03-memory-brain/memory-lifecycle-manager.md)
- 状态：状态区分和 Canonical Authority 为 DECIDED；详细策略阈值和部分转换为 OPEN
- 相关问题：INT-P0-02/03/04、INT-P1-02/06；DM-004/007/008/011

## 1. 目的

负责 Canonical Memory 资产受策略治理的状态转换，并维护唯一、可审计的生命周期历史。Lifecycle 描述管理状态，不描述真实性、Confidence、Trust、Relevance 或授权。

## 2. 范围

覆盖 Memory Lifecycle、转换命令、生命周期历史、资格信号、冲突感知转换、Retention/Forget 领域支持，以及与 Entity/Relation 引用的集成。Claim Epistemic Status 与其相关但相互独立。物理擦除和全局授权由 I 拥有。

## 3. 职责

- 校验允许的 Memory Lifecycle 转换。
- 按每种转换要求 Evidence/Provenance 和 Scope 检查。
- 使生命周期状态历史保持追加式，并确定性投影当前状态。
- 阻止 Compiler 提案直接激活或覆盖 Canonical State。
- 将 Supersede、Archive、Retract 和 Forget 与 Canonical Version 及下游失效协调。
- 向 Governance 暴露 Forget Operation 记录和依赖枚举。

## 4. 非职责

不负责 Event Ingestion、Extraction、Retrieval Ranking、Context Planning、全局 Permission Policy、物理删除、Backup 过期、外部模型删除或客观真理裁定。

## 5. 领域对象

- **LifecyclePolicyRef：** 带版本的策略标识和适用范围；阈值由 I 拥有或由策略配置，不得硬编码在程序中。
- **LifecycleEvent：** 不可变转换记录，包含 event_id、目标 Memory ID、from/to state、actor_ref、scope_refs、reason_code、evidence_refs、policy_ref/version、expected_version/state、相关 successor、operation_id、timestamp、sequence、correlation_id。记录谁/什么/为什么/何时，但不复制敏感来源文本。
- **LifecycleProjection：** 派生的当前状态、最后 Event Sequence、资格标志和 Projection Watermark。可重建。
- **ConflictSet：** conflict_set_id、带 Scope 的 Claim Revision 引用、冲突维度、Evidence 引用、Valid Time 重叠、状态（open/resolved/accepted_coexistence）、解决事件和授权主体。它是待 Claim ADR/Revision 语义明确后的候选领域结构。
- **ForgetOperation：** operation_id、request idempotency、目标 TypedObjectRefs、requesting_actor_ref、scope_refs、purpose、authorization_decision_ref/version、policy_ref/version、state、created_at、suppression_at、dependency_snapshot_id/watermark、逐目标结果、retry metadata、residual_exceptions、completion_proof_ref、completed_at。只存工作流元数据，不存已遗忘 Payload。
- **ForgetTarget：** 类型化 target ref、target class、discovered_by、required_action、status、attempts、last_error_code、last_attempt_at、completed_at、proof_ref。Target Class 包括 Canonical Version、Claim Revision、Evidence、Provenance 后代、Entity/Relation 链接、Index/Vector/Graph Projection、Cache、Working Set、Context Entry/ChangeSet、Backup 和外部接收方。

## 6. 数据模型

Memory Lifecycle 词汇：Candidate、Consolidated、Active、Superseded、Archived、Forgotten。Forget Request 首先创建 Operation 和 Suppression Fence；只有在必需 Scope 内目标满足策略完成标准后，Forgotten 才成为终态逻辑状态。临时 Forgetting 状态属于 ForgetOperation，而不是永久 Memory Lifecycle 状态。

必须保持以下维度独立：
- Epistemic Status：Observed、Reported、Inferred、Verified、Disputed、Retracted。
- Confidence：带量表、方法、校准样本群体和评估时间的估计。
- Trust：来源/主体/流程的可信元数据，不代表真理。
- Relevance：依赖任务和时间的效用，由 Runtime/Activation 拥有。
- Evidence Strength：Claim/Evidence 角色评估，不等于 Confidence 或 Source Trust。
- Lifecycle：仅表示管理阶段。

## 7. 状态机

| From | To | 条件 |
|---|---|---|
| Candidate | Consolidated | Schema/Scope 有效；Provenance 完整或明确记录缺口；Entity/Relation 引用有效；已记录重复/冲突评估；Lifecycle Policy 接受 |
| Consolidated | Active | 明确的激活资格和授权；不存在未解决的阻塞性 Governance Fence |
| Active | Superseded | 存在明确后继/替代关系；保留旧有效性/历史和原因 |
| Candidate/Consolidated/Active/Superseded | Archived | Retention 或 Policy 原因；Archive 不等于删除 |
| Archived | Active | 明确恢复权限；重新校验 Scope、Evidence 可用性、当前有效性和冲突；追加 Event，内容变化时创建新 Version |
| 任意非 Forgotten Lifecycle 状态 | Forgotten | I 提供适用治理完成标准后，执行独立且经 I 授权的 Canonical Lifecycle 转换；进行中的 ForgetOperation 不是 Lifecycle State |
| Forgotten | 任意 | 同一身份禁止恢复。后续新信息创建新的 Memory ID |

不得静默发明 Rejected Candidate 作为新 Lifecycle State：它是保留 Candidate 并记录终态决策元数据，还是转为 Archived，仍为 OPEN。Consolidated 是持久状态还是临时策略检查点，也为 OPEN。

Claim Epistemic 变化独立进行。Retraction 记录撤回，不删除 Evidence 或改写先前声明。Correction 根据 INT-P1-02 创建新的 Claim Revision/Successor。一个 Memory 可以包含不同 Epistemic Status 的 Claim。

## 8. 操作

EvaluateCandidate；AcceptCandidate；Consolidate；Activate；Supersede(successor)；Archive；Restore；RetractClaim；OpenConflictSet；ResolveConflict；StartForget；EstablishForgetFence；RegisterForgetProducerWork；DiscoverDependencies；RecordTargetProgress；CloseProducerBarrier；RecordCanonicalSuppressionProof。

所有转换都要求 Expected State/Version 和 Idempotency Key。Compiler 可以请求转换或提供证据，但不能自行授权。异步 Forget 阶段在每个受保护或不可逆步骤前都由 I 重新授权。

## 9. 不变量

- Lifecycle 和 Epistemic Status 永远不能共用一个 Status 字段。
- LifecycleEvent Stream 是唯一权威转换历史；Projection 可重建（DM-008）。
- 不允许静默转换/覆盖；每次变更都有 Actor、Time、Reason、Scope 和 Policy Reference。
- Superseded 内容在 Scope/Retention 允许范围内仍可查询历史。
- Archived 不等于 Forgotten。
- Forget Fence 必须在异步清理前抑制普通读取/激活。
- 只有 Producer Barrier 关闭，且每个必需 Canonical Domain Target 均有 Suppression Confirmation 或明确 I 批准的残余例外时，D 才能记录 CanonicalSuppressionComplete。这不等于全局 Forget 完成、清理完成或物理擦除证明。
- Forget 不保证从已接收数据的第三方模型/供应商处删除内容。
- 记忆文本不得指令或授权工具（INT-P0-04）。

## 10. 接口

- **E：** 提交带 Evidence、Provenance、来源 Epistemic Status、Scope 和 Idempotency 的 Candidate/转换提案；Lifecycle 返回 accept/defer/reject 和 Canonical Lifecycle Event/Version 引用。
- **F：** 消费当前 Lifecycle Projection，在排序前排除/限定资产；必须遵循 Suppression Fence。
- **G：** 接收引用 Superseded/Archived/Forgotten Version 的 Context Entry 失效/协调事件；G 拥有 Context 状态。
- **H：** 只传输类型化 Operation 引用和状态；H 拥有协议 ACK。
- **I：** 拥有 Permission、Retention Policy、Physical Erasure、Backup 和外部边界决策；Brain 提供依赖图和目标状态。

接口携带 ActorRef、ScopeRef、Policy Version、准确 MemoryVersion 和 Correlation ID。

## 11. 错误

INVALID_TRANSITION；STALE_STATE；STALE_VERSION；MISSING_SUCCESSOR；PROVENANCE_INCOMPLETE；CONFLICT_REQUIRES_RECONCILIATION；SCOPE_MISMATCH；PERMISSION_DENIED；FORGET_IN_PROGRESS；FORGET_PARTIAL；TARGET_UNAVAILABLE；POLICY_CHANGED；ALREADY_FORGOTTEN；IDEMPOTENCY_CONFLICT。部分 Forget 必须可恢复并明确显示为 Partial，绝不能当作成功。

## 12. 一致性

LifecycleEvent 追加及其 Canonical Sequence 必须原子完成，或通过 Outbox 可恢复提交。Projection Fold 必须确定性且可重放。ForgetOperation 和逐目标进度是持久化、单调记录；重试不得回退已完成目标。声称清理完成之前，Suppression Fence 必须对 Canonical Read 和所有下游 Projection 可见。依赖发现使用 Snapshot/Watermark，并记录迟到派生物以便后续抑制/清理。

## 13. 安全 / Scope

每个操作都依据已认证 ActorRef、Action、Target Resource、Owner/Applicability ScopeRefs、Purpose、Policy Version 和 Grants 评估。Scope 不代表 Permission。Graph Traversal 检查每条 Edge 和每个 Target。不得泄露未授权依赖是否存在。异步 Worker 重新授权。Forget Audit 不得保留待遗忘 Payload；Tombstone 字段必须不可反向重建，并经 I 批准。

## 14. 性能

Forget 依赖发现和 Graph Traversal 可能长时间运行；使用分页 Cursor、Watermark、有界扇出、进度检查点和背压。分别测量 Suppression Latency 与 Policy Completion Time。Lifecycle Read 使用可重建 Projection，以 Canonical Event Stream 为来源。不得为了达到延迟目标牺牲 Evidence、Scope 检查或历史。

## 15. 可观测性

指标：转换次数/拒绝数、陈旧状态冲突、各 Lifecycle State 的停留时间、Conflict Backlog、Forget Suppression Latency、依赖数量、逐目标完成延迟、重试、未解决例外、Policy 重新授权失败。Event 携带 operation_id、target_ref、actor/scope、stage、attempt、correlation/causation 和 timestamps；不记录已遗忘原始 Payload。

## 16. 故障场景

- Policy Service 不可用：Fail-closed；不执行受保护转换。
- 并发生命周期转换：Expected State/Sequence 只允许一个成功；其他操作协调。
- 依赖图部分不可用：Forget 保持进行中；记录 Unknown Coverage。
- Worker 崩溃：从逐目标检查点恢复；不得不安全地重复破坏性动作。
- Adapter/Cache 离线：Suppression Event 仍然持久化；策略必须定义完成是否等待 ACK，或采用 Expiry/Key Revocation；与 I/G/H 协调，当前 OPEN。
- 外部模型已接收记忆：记录 Recipient/Boundary 和残余例外；Brain 不得声称远端已删除。
- Projection 滞后：Canonical Lifecycle Stream 仍是权威；Runtime 不得激活陈旧状态。

## 17. 依赖

Canonical Store 提供 Lifecycle Event 持久化和 Version；Domain Model 提供 Epistemic/Time/Scope 语义；E 提供 Candidate 提案；F 在排序前过滤；G 使 Context 失效；H 提供已认证操作传输和 Adapter 状态；I 提供 Permission、Retention、Backup 和 Erasure Policy；Provenance Graph 用于依赖发现。

## 18. 开放问题

- OPEN：Consolidated 是持久状态还是临时检查点。
- OPEN：被拒绝 Candidate 的终态语义。
- OPEN：Archived 恢复规则和 Evidence 过期。
- OPEN：离线副本、不可变备份和外部模型供应商的 Forget 完成策略（INT-P0-03 / DM-011）。
- OPEN：Provenance DAG 还是受限环；DAG 是推荐候选，等待领域验证（DM-007）。
- OPEN：ADR 之后的 ConflictSet 语义和 Claim Identity/Revision（DM-003/004）。
- TO_VALIDATE：抑制传播和依赖遍历容量。

## Phase 3 整改 — 操作状态与 Canonical Lifecycle 分离

### 规范性区分

Memory Lifecycle 精确为 Candidate、Consolidated、Active、Superseded、Archived、Forgotten。不存在名为 Forgetting 的 Memory State。Memory Lifecycle 字段 **MUST NOT** 设置为 Operation Phase、Fence State、Visibility State 或 Cleanup State。

ForgetOperation 拥有独立于 Memory Lifecycle 的持久化状态机：

| ForgetOperation 状态 | 含义 |
|---|---|
| Requested | 持久化 Operation ID 和 Idempotency Identity 已存在；I 的授权决策待处理/记录中 |
| FenceEstablished | 单调 Fence Generation 和受影响 Target Set Digest 已持久化提交；覆盖目标的 Canonical Read Fail-closed |
| InventoryOpen | 正在协调依赖清单和 Producer Work Registration |
| BarrierDraining | 所有 Fence 前已登记工作都必须达到带 Fence 的终态；未登记 Producer 不得绕过 Admission |
| TargetReconciliation | 正在收集逐目标 Suppression/Cleanup ACK；Unknown/Failed Target 必须明确保留 |
| CanonicalSuppressionComplete | D 的封闭 Producer Barrier 和 Canonical Domain Suppression Proof 已持久化；不代表全局策略完成或物理擦除 |
| Blocked / Failed | Coverage、授权、依赖或目标证据不足；在安全时保持可恢复 |

不存在由 D 拥有、代表整个系统已经遗忘数据的通用 Complete 状态。I 可以按自身策略附加独立 Governance Completion Attestation。D 只记录该引用，不得伪造它。

### Fence 与 Lifecycle 顺序

1. I 授权并提供适用 Policy/Identity Context；D 创建持久化 Operation Record，并原子安装 Fence Generation。
2. Canonical Read/Write、Dependency Registration 和 Publication Gate 在返回或暴露被覆盖 Target 前检查活动 Fence。
3. D 枚举 Canonical Dependency；只有所有 Fence 前登记的 Producer Work 都终结且所有 Target 均已登记后，才能关闭 Producer Barrier。
4. D 记录逐目标结果和 Canonical Suppression Proof。
5. 只有 I 提供必需 Governance Completion Criterion 后，D 才能追加 LifecycleEvent，将 Memory 转为 Forgotten。该 Event 不是远端物理擦除证据。

### 故障与重试

Fence 安装按 ForgetOperation ID 单调且幂等。Worker 崩溃不能降低 Fence，也不能回退已确认 Target。Unknown Inventory、过期且没有恢复证据的 Producer Lease、不可达必需 Target、Cursor Gap 或缺失 ACK 都会使 Operation 保持 In-progress/Blocked。Retry 从持久化 Registration 和 Target Checkpoint 恢复，不能使用更弱的 Inventory Snapshot 重新开始。

### Cursor 引用

LifecycleEventCursor 为 (memory_id, lifecycle_event_sequence, event_id)，每个已提交 Event 还携带 CanonicalCommitCursor。LifecycleEvent Sequence 按 Memory 连续；CanonicalCommitCursor 对所属事务进行全局排序。LifecycleProjection.last_event_cursor 是 LifecycleEventCursor，绝不是 IndexWatermark。F 的 IndexWatermark 和 D 的 ForgetFenceCursor 仍是不同类型。
