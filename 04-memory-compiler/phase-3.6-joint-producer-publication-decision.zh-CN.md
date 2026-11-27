---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "从 Owner 源分支恢复；Owner 接受仍待定。"
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
    canonical_status: Canonical
    canonical_scope: "E 域 Memory Compiler 记录 phase-3.6-joint-producer-publication-decision.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-phase-3-6-joint-producer-publication-decision"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-joint-producer-publication-decision
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# Phase 3.6 — E 联合架构决策：生产者工作与发布强制执行

- 决策权威：由用户委托的 DE-S 联合架构师（ChatGPT 同时承担 D、E 与 Storage 职责）
- 日期：2026-11-16
- 状态：**已记录联合架构决策 / 实现尚未验证**
- 分支：`session-e-memory-compiler-2026-11-16`
- 范围：E 所有的生产者生命周期、执行尝试、租约、派生、依赖注册和发布强制执行。

## 1. 身份模型

| 身份 | 含义 | 重试/重放/恢复规则 |
|---|---|---|
| `WorkItemId` | 向 D 注册的稳定根生产者义务 | 重试、DLQ 重放、重新投递和工作器恢复期间复用 |
| `AttemptId` | 一次执行尝试 | 每次重试/重放执行都生成新值 |
| `LeaseEpoch` | 工作器所有权的 fencing 代次 | 重新分配时递增；过期代次不得暂存、发布或终结 |
| `DerivationRunId` | 一次编译器派生/重新编译运行 | 每次重新编译都生成新值 |
| `ArtifactId` | 不可变输出身份 | 实质上产生新输出时生成新值；内容摘要不可变 |
| `DependencySetDigest` | 完整且不可变的血缘/依赖集合 | 变更必须取得新的依赖注册回执 |

对同一义务重新编译时保留根 `WorkItemId`，并创建新的 `DerivationRunId`。若重新编译被独立调度，E 必须在入队/租约/执行之前向 D 注册子 WorkItem。子项与根项关联，并参与同一根屏障的计数。E 不得创建新的、未关联的根项来规避 fence。

## 2. 必需生命周期

`Accepted → Registered → Queued → Leased → Running → StagedPrivate → DependenciesRegistered → PublishGatePending → Published`

终结处置与队列状态分开。 `DLQ`、`LeaseExpired`、`WorkerLost`、`RetryPending` 和 `StagedPrivate` 都不是终态。一个根项可能有多个输出/子项；只有在每个已声明输出和后代都具有持久化终态处置，且没有任何执行尝试仍可发布时，根项才成为终态。

E 必须在入队、租约、执行、源解引用或暂存之前取得 D 的持久化 ProducerRegistrationReceipt。响应丢失时，应使用相同幂等键和请求摘要重试；必须返回原回执或确定性冲突。

## 3. 依赖与发布协议

1. 构建完整、不可变的依赖集合，包括传递性源血缘和类型化 Scope 引用。
2. 仅将字节暂存到私有、不可查询的位置。
3. 将完整依赖集合作为一个持久化完整性单元向 D/Storage 注册。部分注册永远不能用于发布。
4. 向最终门禁提交根 WorkItemId、AttemptId、LeaseEpoch、DerivationRunId、ArtifactId、摘要、依赖回执、血缘和 Scope。
5. 协调器执行最终 fence、授权、工作/租约和依赖检查，并以原子方式提交权威可见性转换及 PublicationReceipt。
6. 只有提交之后，E 才能确认 Published 或通知下游消费者。Outbox 投递是至少一次且必须幂等；单独一条 outbox 消息永远不能建立可见性。

任何 E 本地缓存、较早的门禁令牌、成功的暂存事件或对象存储目录列表都不能建立发布状态。

## 4. 重试、重放与恢复

- 重试/重放保留 WorkItemId，创建新的 AttemptId，并取得当前 LeaseEpoch。
- 重新编译保留根 WorkItemId，创建新的 DerivationRunId，并在执行前注册任何被独立调度的子项。
- 相同幂等键和摘要的重复请求返回原持久化回执。
- 相同键但摘要不同属于冲突，必须 fail closed。
- 工作器恢复必须查询持久化工作/租约状态；进程内存和队列中存在任务都不是权威。
- 过期工作器即使完成计算，在 LeaseEpoch 被替换后也不能注册依赖、发布或终结。
- DLQ 是运维路由状态，不是“发布不可能发生”的证明。

## 5. 终态

只有在所有输出、重试、重放、子派生和发布尝试均被持久化记账后，E 才能请求根项终态处置。D 记录屏障可见的终态回执。未解决或未知的提交结果仍保持 pending，并从持久化回执对账；绝不能乐观地标记为终态。

## 6. 验证边界

本决策依据用户明确委托 D/E/Storage 职责给同一联合架构师的授权，解决 E 的架构映射。它不声称存在可执行生产者 API、原子依赖存储、已部署的可见性门禁、租约 fencing 实现或通过的 E36 测试。所有运行时/故障测试仍为 **NOT RUN**。
