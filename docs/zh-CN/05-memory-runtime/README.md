---
document_metadata:
  domain: "memory-runtime"
  role: "guide"
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
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-083"
        - "copied from ZH-CN guide docs/zh-CN/05-memory-runtime/memory-runtime-guide.md blob 0e0df43de9c55f8e41d6ed596d50471798fb23cc"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Exact-name ZH-CN mirror alias created from the existing F guide; semantic alignment reviewed; Non-Canonical/Informative."
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
    canonical_status: "Non-Canonical"
    canonical_scope: "ZH-CN mirror of memory-runtime/runtime-architecture-guide"
    canonical_scope_id: "memory-runtime/runtime-architecture-guide"
    canonical_scope_keywords:
      - "runtime"
      - "retrieval"
      - "working-set"
      - "forget-suppression"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "05-memory-runtime/README.md"
    en: "docs/en/05-memory-runtime/README.md"
    zh-CN: null
---

> **重建说明：** 本文件是根候选文档 `05-memory-runtime/README.md` 的简体中文镜像。根文件根据 AID-2026-083 记录的英文镜像 `docs/en/05-memory-runtime/memory-runtime-guide.md`（blob `a45b868efe1367fb9934c17191109d8d87f48fab`）反推重建；未找到权威根源 blob。本镜像状态为 **Non-Canonical / Informative**。

# 记忆运行时架构指南

- 文档 ID：DOC-RUNTIME-001
- 版本：1.0
- Owner：F — Memory Runtime
- 源规范：F Owner 分支中的 Runtime 总览和消费者契约
- 对应英文：[Memory Runtime Architecture Guide](../../en/05-memory-runtime/README.md)
- 状态：解释性指南；拓扑为 CANDIDATE，数值预算为 TO_VALIDATE，消费者 Schema 仍为 OPEN

## 1. 目的

Memory Runtime 是 Brain 有界的在线读取与激活层。它接收 Recall 请求，解析授权和 Scope，在权威及派生表示中检索，返回带证据的候选记忆，建议哪些内容可以激活，并维护可丢弃的 Runtime Working Set 和缓存。

它不是 Agent Runtime、规划器、工具执行器、Canonical Store、Compiler，也不拥有 Context Version。默认 Recall 应是确定性的，不得同步依赖大型 LLM。

## 2. 权威边界

F 负责：
- Runtime Session 生命周期和请求局部执行状态。
- Query 解释与检索路由。
- 按 Scope 过滤候选、融合、去重和排序。
- 完整性/新鲜度语义以及类型化 Index Watermark 消费。
- Activation Recommendation 和有界 Working Set/Cache。
- 调度、准入、取消以及读取路径的新鲜度检查。

F 不拥有 Canonical Memory/Claim/Entity/Relation 身份、版本、生命周期或权威 Forget 状态（D）；不负责编译和 Canonical/Index 发布（E）；不修改 ContextEntry 或 ContextVersion（G）；不制定全局 Permission/Retention/Audit 策略（I）；不负责 Agent 规划或外部行动授权。

## 3. 读取路径

~~~text
Recall Request + 认证 Principal / Scope
        ↓
授权和当前策略上下文
        ↓
Query 解释与检索路由
        ↓
优先执行 Scope 过滤
        ↓
结构化 / 词法 / 语义 / 时间 / 关系候选
        ↓
融合、去重、新鲜度和完整性评估
        ↓
带 Evidence 的 RetrievalResult
        ↓
向 G / 调用方提供 ActivationRecommendation
~~~

必须在排序、聚合或可能泄漏受保护信息的结果计数之前执行 Scope 和授权过滤。结果引用精确的不可变 Canonical Memory Version。检索不会创建 Memory，也不会推进 ContextVersion。

## 4. RetrievalResult 不等于 ActivationRecommendation

RetrievalResult 说明检索到了什么、使用了什么查询和一致性条件，并包含候选引用、Evidence 摘要、匹配通道、新鲜度/完整性指标及不确定性警告。

ActivationRecommendation 建议 include、defer 或 exclude，并提供原因码、紧迫程度/过期提示和预算估算。它不是 Context 编辑操作。G 拥有 Context 成员、排序、版本和 Delivery Intent。

Telemetry 是不可信的相关性信号，不授予访问权限，也不能证明所声称的任务结果确实发生。

## 5. Working Set 和缓存

Working Set 与 Cache 是有界、可丢弃的派生投影，不是权威记忆。它们必须按认证身份、Scope、Policy/Permission Epoch 和相关 Forget Generation 隔离，并设置明确的容量、TTL、准入、淘汰和可观测性约束。

Cache Hit 不得绕过当前授权或 Forget 抑制。失效机制和 Generation 检查必须防止过期缓存回填、在途读取或索引重建重新引入已遗忘或已撤销内容。

## 6. 新鲜度、Cursor 和 Watermark

F 消费 D 的 CanonicalCommitCursor，以及每个 Partition 的 IndexWatermark 契约。Cursor 命名空间必须保持类型化，不得压缩成一个通用整数。Watermark 只能证明某个 Index Partition 已处理的连续 Canonical Commit 前缀；它不证明 Forget 已完成或内容已物理删除。

Runtime 结果应明确暴露新鲜度和完整性，不能把过期或部分结果静默呈现为完整结果。

## 7. Forget 抑制与防复活

F 必须：
- 按当前 Forget Generation 取消或安全结束在途检索。
- 在候选返回或激活前抑制受影响内容。
- 使用 Generation 感知检查失效 Working Set 和 Cache。
- 防止延迟 Cache Fill 恢复旧内容。
- 仅从经过当前 Forget Fence 和策略过滤的 Canonical 数据重建索引。
- 跟踪每个 Index Watermark 并暴露延迟/失败。
- 在读取边界重新检查当前授权。

目标是零未授权信息或已遗忘内容泄漏。必须通过竞态、崩溃、索引重建和缓存失效测试证明，不能从某个单元测试通过推断全系统安全。

## 8. 故障与降级

| 情况 | 预期行为 |
|---|---|
| Vector Index 不可用 | 使用允许的替代通道，或返回部分/不可用状态 |
| LLM 不可用 | 默认 Recall 不依赖大型模型推理，仍可继续 |
| Index 落后 | 暴露新鲜度/完整性，不得声称结果完全最新 |
| Permission 服务不可用 | 受保护读取 Fail Closed |
| Forget Generation 在读取期间变化 | 返回结果前重新校验并抑制 |
| Cache 失效延迟 | Generation 检查阻止旧内容被提供 |
| Worker 或 Query 超时 | 取消有界任务并返回明确超时/部分状态 |

## 9. 性能与资源控制

F 必须限制 Query 并发、Fan-out、候选数量、Evidence 展开量、Working Set 容量、Cache 内存、索引访问和取消延迟。数值限制在明确硬件和代表性语料上实测之前均为 TO_VALIDATE。应跟踪 p50/p95/p99 延迟、检索召回/质量、索引延迟、缓存命中率、内存使用以及取消/撤销传播时间。

## 10. 接口和不保证事项

输入包括认证 Principal 和解析后的 Scope、Recall 查询/过滤/用途、任务/会话/环境引用、Evidence/结果预算、Deadline/Cancellation、不可信 Telemetry、D Canonical Metadata、E Commit/Publication Event、Index Watermark 和当前策略配置。

输出包括 RetrievalResult、带精确 Version ID 的 CandidateMemory 引用、Evidence/Provenance 摘要、完整性/新鲜度向量、警告和 ActivationRecommendation。

F 不保证真实性、外部行动授权、Context 已应用、模型理解或全局 Forget 已完成。

## 11. 仍需验证

- Scope-first Retrieval 和零跨 Scope 泄漏。
- Cursor/Watermark 缺口、延迟与恢复。
- Forget 与在途读取、Cache Fill、Index Rebuild 的竞态。
- Permission 撤销和 Policy Epoch 变化。
- 内存、Fan-out、并发和取消的有界性。
- 代表性检索质量及 p95/p99 测量。

详细 Runtime 契约见 [F Owner 分支](https://github.com/oahcom/AiMemoryBrainArchitecture/tree/session-f-memory-runtime/05-memory-runtime)。
