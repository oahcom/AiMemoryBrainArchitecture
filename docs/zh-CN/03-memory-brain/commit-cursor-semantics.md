---
document_metadata:
  domain: memory-brain
  role: reference
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
        - "14-ai-development/work-items/AID-2026-150/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "仅作机械路径/来源配对更新；ORPHAN_MIRROR_PENDING_DECISION 仍然有效。"
    usage_status: Active
    modification_status: Modified
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---
# Canonical Commit 与 Cursor 语义

- 文档 ID：D-CURSOR-001
- 版本：1.0
- 源分支：session-d-memory-brain-2026-11-16
- 源文件版本：AID-2026-150 已恢复规范源 `03-memory-brain/commit-cursor-semantics.md`；镜像状态仍为 `ORPHAN_MIRROR_PENDING_DECISION`，正式采纳或退役待 D Owner 明确裁决。
- 审查时源分支 HEAD：6b654d5cffaeb71b01f2b0750daa0abc14eb64b3
- 源规范：[`03-memory-brain/commit-cursor-semantics.md`](../../../03-memory-brain/commit-cursor-semantics.md) 已恢复；本 ZH-CN 文档仍非权威，孤儿镜像的正式处置待 D Owner 裁决。
- 对应英文：[Canonical Commit and Cursor Semantics](../../en/03-memory-brain/commit-cursor-semantics.md)
- Owner：Session D — Memory Brain Principal Architect（仅拥有 Canonical Cursor 权威）
- 状态：D 的 Canonical 语义为 DECIDED；Storage Engine 实现和 E/F/G 消费者一致性为 OPEN
- 相关问题：D-REV-P1-002、INT-P1-06、INT-P0-03

## 1. 决议

D 选择：每个 Canonical Memory Authority 使用一个全局有序的 CanonicalCommitCursor，同时保留独立的 Per-Aggregate Revision 和 Per-Memory LifecycleEvent Cursor。不存在 Per-Aggregate Canonical Commit Sequence。该选择明确跨 Aggregate 事务顺序，同时保留本地修订编号。它不意味着多个 Brain Authority 之间存在分布式全局时钟。

## 2. 类型化 Cursor 注册表

| 类型 | 结构（领域级，不是 Wire Schema） | Owner | 排序/证明什么 | 不能证明什么 |
|---|---|---|---|---|
| CanonicalCommitCursor | (brain_authority_id, commit_sequence) | D | 单个 Brain Authority 内成功提交的 Canonical Transaction | Index 应用、Context 状态、Forget 抑制或物理删除 |
| AggregateRevision | (aggregate_type, aggregate_id, revision_sequence) | D | 单个 Aggregate 的不可变修订 | 不同 Aggregate 之间的全局顺序 |
| LifecycleEventCursor | (memory_id, lifecycle_event_sequence, event_id) | D | 单个 Memory 的追加式 Lifecycle Event | 不带 Commit Cursor 时的 Aggregate Revision 或跨 Aggregate 顺序 |
| IndexWatermark | (index_id, partition_id, applied_through: CanonicalCommitCursor, coverage_version, schema_version) | F | 某个 Index Partition 已核算的连续 Canonical Commit 前缀 | 所有目标均已删除/抑制，或 Forget 已完成 |
| ForgetFenceCursor | (forget_operation_id, fence_generation, target_set_digest) | D | 针对精确目标集合/血缘的单调抑制 Fence | Commit 位置、Index 进度、G ContextVersion 或 I Policy Epoch |
| ContextVersion | G 拥有的不可变 Version 引用/序列 | G | 期望的受管 Context 状态 | Canonical Memory Revision 或 Adapter 应用 |
| DeliveryId / AdapterEpoch / InferenceRequestId | H/C 拥有的标识符 | H/C | Delivery 和最终推理边界关联 | Canonical Commit 顺序 |

所列字段是各方达成一致所需的语义组成，不是最终序列化 Schema。B/H/I 必须对齐通用类型化引用和身份定义；只有 H 定义 Wire Encoding。

## 3. Commit 与事务可见性

Canonical Transaction 先校验 Scope/Domain 不变量和期望 Aggregate Head，然后原子提交所有 Canonical Write、新 Aggregate Revision、Aggregate Head 更新、LifecycleEvent 追加（如有）、CanonicalCommit 记录和 Outbox Intent；也可以采用已证明等价的可恢复机制。成功事务在串行化提交顺序中获得一个 Commit Sequence。Cursor 分配和持久化提交属于同一个原子可见性边界。被拒绝、中止或回滚的事务不会获得已提交 Cursor。

在 Cursor N 读取时，可以看到截至 N 的所有 Canonical Transaction 效果，不能看到后续事务。不能只看到一个多对象事务中的部分对象。MemoryVersion 拥有自己的 Per-Memory Revision Sequence，并保存事务 Cursor；EntityVersion 和 RelationRevision 同样如此。

## 4. 缺口、Replay、Resume 与 Outbox

在一个 Authority 内，Canonical Committed Sequence 必须连续。消费者观察到缺口，表示它尚未核算每一笔已提交事务，而不是 Canonical Authority 跳过了某笔已中止事务。消费者持久化最后一个连续应用的 Cursor，并且只能从其后继续。Delivery 采用 At-least-once；稳定 Event/Operation ID 使 Replay 幂等。乱序 Event 可以暂存，但连续 Watermark 不得越过它推进。

Outbox Intent 与 Canonical Data 一起提交。发布可能延迟、重复或重试；发布顺序不能重新定义 Canonical 顺序。消费者自己的 Transport Offset 不是 CanonicalCommitCursor。如果 Event 缺失，消费者请求 Replay/Reconciliation；如果 Canonical History 保留策略导致无法 Replay，则加载带 Base Cursor 的一致 Snapshot，并从该 Cursor 之后继续。任何消费者都不得静默重置到 Latest，同时声称连续性没有中断。

## 5. LifecycleEvent 语义

LifecycleEvent 是追加式、权威的 Lifecycle Transition 记录。其序列按 Memory ID 连续，而不是全局连续。每个 LifecycleEvent 记录其所属的 CanonicalCommitCursor。单个 Memory 的多个 Lifecycle Event 由 LifecycleEventCursor 排序；不同 Memory 之间的事件由 CanonicalCommitCursor 排序。LifecycleProjection 可以重建，并记录最后折叠的 LifecycleEventCursor；该字段不是 Index Watermark。

## 6. IndexWatermark 语义

IndexWatermark 由 F 拥有。它限定在指定 Index/Channel Partition 内，并记录已核算所有相关变更的最高连续 CanonicalCommitCursor，包括明确标记的 No-op/Irrelevant Coverage。如果相关 Commit 延迟、失败或 Schema 不兼容，Watermark 必须停在它之前。重建从一致 Snapshot Cursor 开始，并重放后续 Canonical Commit。Index 在重新检查 Canonical Eligibility 和当前 ForgetFence 之前，不得从某个 Segment 输出候选。

Watermark 只是新鲜度/完整性信号。它不能证明某个目标已经不存在、Cache 已清除、Context 已协调或物理擦除已完成。

## 7. ForgetFence 语义

ForgetFenceCursor 是限定于某个 ForgetOperation 和其 Target Set Digest 的单调 Generation。它在 Admission 时以及 Canonical 可见或下游暴露之前立即检查。它不是从 CanonicalCommitCursor 派生的，尽管 Fence 安装本身有 Commit Cursor 供审计/Replay 使用。Fence Generation 不能用作 LifecycleEvent Sequence、Aggregate Revision 或 IndexWatermark。

## 8. 契约 Owner 矩阵

| 关注点 | D | E | F | G | H | I |
|---|---|---|---|---|---|---|
| CanonicalCommitCursor | 权威 | 消费 D 结果 | 消费 | 消费 | 传输不透明引用 | Policy 可审计 |
| AggregateRevision | 权威 | 引用 | 读取准确修订 | 固定准确 MemoryVersion | 传输不透明引用 | Policy 可审计 |
| LifecycleEventCursor | 权威 | 消费信号 | 消费新鲜度/失效信号 | 消费协调触发 | 传输不透明引用 | Governance 可审计 |
| IndexWatermark | 不拥有 | 单独提供来源/Outbox 进度 | 权威 | 消费 | 不拥有 | 不拥有 |
| ForgetFenceCursor | Canonical 权威 | 执行 Producer Gate | 执行 Retrieval/Index/Cache Gate | 执行 Context/Delivery Gate | 执行 Adapter Reconnect Gate | 单独设置全局 Policy/Permission Epoch |
| ContextVersion | 不拥有 | 不拥有 | 不拥有 | 权威 | 传输 | 不拥有 |

## 9. 故障与验收测试

- 多 Aggregate 原子提交必须整体可见，或完全不可见。
- CAS/Validation 失败不得消耗 Commit Cursor 或 Aggregate Revision。
- Per-Memory LifecycleEventCursor 必须连续且 Replay 结果确定。
- 消费者存在缺口时阻止 Watermark 推进；重复 Replay 必须幂等。
- Snapshot Bootstrap + Exclusive Replay 必须重现相同 Canonical State。
- 同一事务中的两个 Aggregate 共享 Commit Cursor，但拥有独立 Revision。
- IndexWatermark 必须限定于 Partition，不能作为 ForgetFenceCursor 传入。
- Fence 安装具有用于审计的 Commit Cursor，但其 Generation 不由该 Cursor 计算。

**验收状态：** 领域语义已决议；Storage/Recovery 实现和 E/F/G Cursor 一致性仍为 OPEN。本文不声称任何 SLO 或实现结果。
