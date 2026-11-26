---
document_metadata:
  domain: memory-runtime
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
        - "14-ai-development/work-items/AID-2026-113/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Mirror body retained unchanged; semantic parity checked at heading and cross-reference level only."
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
    canonical_scope: "Memory Runtime design specification: runtime-scheduling"
    canonical_scope_id: "memory-runtime/runtime-scheduling"
    canonical_scope_keywords:
      - "admission"
      - "scheduling"
      - "cancellation"
      - "backpressure"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "05-memory-runtime/runtime-scheduling.md"
    en: "docs/en/05-memory-runtime/runtime-scheduling.md"
    zh-CN: null
---
# Memory Runtime Scheduling（记忆运行时调度）

- 文档 ID：F-SCHEDULING-001
- 版本：1.0
- Owner：Session F — MR-04
- 源分支：session-f-memory-runtime
- 源 Blob：ca35d8cddd012c1ff067328ee22177f57c40ae36
- 对应英文：[Memory Runtime Scheduling](../../en/05-memory-runtime/runtime-scheduling.md)
- 状态：安全/Admission 原则已 DECIDED；Scheduling Design 为 CANDIDATE；Resource Budget 为 TO_VALIDATE

## 1. 目的

在保留 Safety、Freshness 和真实 Partial-result 语义的同时，对 Recall/Activation Work 进行调度，并限制 Latency、Resource Use 和 Isolation。

## 2. 范围

拥有 Request Classification、Admission、Retrieval Routing、Parallel Channel Execution、Candidate/Latency Budget、Graph Fan-out、Early Stop、Deduplication、Backpressure、Cancellation、Priority 和 Resource Isolation。

不调度 Agent Plan/Action、Compiler Job、Canonical Commit 或 Context Delivery。

## 3. 职责 / 非职责

Runtime Scheduler 是 Brain 内部的 Execution Coordinator。Agent Intent/Plan/Observation/Outcome 是 Relevance/Priority Signal，不是可以覆盖 Brain Limit、Authorization 或 Policy 的指令。Scheduler 绝不将 Memory Text 解释为可执行控制。

## 4. 输入 / 输出

输入：Authenticated RecallRequest、Resolved Scope/Permission Epoch、Query Class、Deadline、Candidate/Evidence Budget、Required Consistency Fence、Cancellation Token、Policy 和 Resource Configuration。

输出：Admitted/Rejected/Deferred Request、Execution Plan、Channel Outcome、Completeness/Omission、Resource/Timing Metric。

## 5. Request Classification

候选类别：
- P0 Safety/Decision-critical Explicit Recall；
- P1 Interactive Bounded Recall；
- P2 Background/Proactive Refresh；
- P3 Maintenance-like Cache Warmup（仅在单独授权时允许，优先级低）。

Priority 由 Brain Policy 拥有。Caller 提供的 Urgency 是不可信 Hint。Priority Class 不能绕过 Scope Filter、Forget、Quota 或 Fairness。高影响 Classification 可以提高 Evidence/Consistency 要求，不能降低要求。

## 6. Routing / Parallel Execution

根据 Structured/Entity/Lexical/Vector/Graph/Temporal/Provenance 需求规划 Channel。在一个 Request Task Group 内并发执行独立 Channel。每个 Channel 启动前都获得 Scoped Query Predicate 和 Local Budget。Graph Expansion 和 Evidence Dereference 是独立 Child Task，并限制 Fan-out。只有在 Authorization/Canonical Revalidation 后才 Merge。Cancellation 传播到所有 Child Task。

## 7. Candidate 与 Latency Budget

每个 Request 的 Budget 维度：
- 最大 Parallel Channel 数；
- 每个 Channel 和总 Candidate Buffer 的最大 Candidate 数；
- 最大 Graph Depth、Edge Fan-out 和 Visited Node 数；
- 最大 Canonical Revalidation Call 数；
- 最大 Evidence Ref/Bytes 和 Provenance Depth；
- 最大 Reranker Input；
- CPU Work Quota、Memory Bytes 和 Wall-clock Deadline。

所有数值均为 TO_VALIDATE。Budget 耗尽时返回类型化 Partial Result，不得静默截断。Fan-out 前必须取得 Budget Reservation，避免无界推测性工作。

## 8. Early Stop / Completeness

以下情况可停止：Deadline 到期、Required-channel Work 完成、根据已验证标准达到 Candidate Sufficiency、边际收益低于已验证阈值，或发生 Cancellation。

Top-K 列表已填满不代表完整。Response 记录 Required/Executed Channel、Watermark、Omitted Work、Budget Exhaustion、Truncation、Cancellation 和 Canonical Fence Status。

## 9. Backpressure 与 Admission

使用有界 Queue 和 Per-principal/Per-scope Concurrency Limit。压力过大时：
1. Reject 或 Defer 低优先级 Background Work；
2. 在 Key 安全的前提下合并等价 Refresh；
3. 在 Reserved Capacity 内保留 Interactive Request；
4. 在 Principal/Scope 之间执行 Fair Scheduling；
5. 返回类型化 Overloaded/Retry-after Outcome，不包含受保护 Metadata。

一旦报告 Accepted，绝不能丢弃 Request；Recall Admission 不是 Durable Event Acceptance，不得与 Compiler Semantics 混淆。

## 10. Cancellation 与 Supersession

Cancellation 是协作式的，并传播到 Channel Task、Graph Traversal、Evidence Expansion 和 Reranking。Deadline/Cancel 后到达的结果必须丢弃；除非独立验证且 Policy 允许，否则不能填充 Working Set/Cache。

更新的 Request 可以 Supersede Background Refresh，但不能静默取消 Explicit Request。In-flight Forget/Revocation Fence 优先于普通 Cancellation：立即 Suppress Result。

## 11. Priority 与 Resource Isolation

Per-principal/Per-session Quota 防止 Noisy Neighbor 饥饿。Interactive Recall 与 Background Refresh 使用独立 Pool。

CPU 用于 Parsing、Query Planning、Fusion 和 Graph Traversal；RAM 用于有界 Candidate、Working Set 和 Cache；Disk I/O 用于 Structured/Full-text/Vector/Temporal Index；GPU 仅可选用于 Embedding Inference 或可选 Reranking。GPU Queue 饱和不得阻塞 Deterministic Lexical/Structured Recall。默认路径不要求 GPU。

## 12. Scope / Permission

只有完成 Authenticated Identity/Authorization 后才能 Admission。每个 Channel 独立执行 Scope-before-Candidate。Priority 不能扩大 Scope。Queue Entry 携带 Principal、Scope、Policy Epoch、Forget Epoch 和 Expiry。出队和最终 Response 前重新授权；Policy 改变时取消或重新规划。

## 13. Version / Freshness

Scheduler 在整个执行过程中携带 Requested Canonical/Index Fence 和 Per-channel Watermark。它只能在 Deadline 内等待 Publication；否则返回包含准确 Lag 的 Partial。Commit-to-response Boundary 重新检查 Canonical/Forget Status。Stale Channel 不能标记为 Complete。

## 14. Cache 语义

只有在 Principal/Scope/Environment/Permission/Forget Epoch、Query Fingerprint、Config 和 Consistency Fence 完全匹配时，Scheduler 才能合并相同且安全的 Request。共享 In-flight Work 不得混用 Authorization Context。一个 Waiter 的 Cancellation 不能取消其他已授权 Waiter 仍需要的 Shared Work；但仍须对每个 Waiter 的 Response 单独授权。

## 15. 故障处理

Overload → Typed Rejection/Defer；Channel Failure → Partial；Canonical/Auth Failure → 在无法证明安全时 Fail-closed；GPU Failure → Deterministic Non-GPU Route；Disk Saturation → Bounded Retry 或 Partial/Unavailable；Cancellation → 不返回迟到 Response；Scheduler Crash → Request Lost/Failed，绝不伪称 Complete。Retry Policy 必须有界且只允许 Read-only/Idempotent 操作。

## 16. 性能预算

在声明的 Concurrency/Corpus/Hardware 条件下测量 Admission Wait、Queue Age、Per-stage Latency、Parallelism、CPU Time、RAM Peak、Disk IOPS/Latency、GPU/VRAM 和 Cancellation Delay。Benchmark 前不设固定 P95/P99。

TO_VALIDATE：Queue Limit、Reserved Capacity、Fairness Quantum、Graph Budget、GPU Offload Value，以及 12–16 GB VRAM 本地系统的 Resource Envelope。

## 17. 可观测性

按 Priority/Scope Class 跟踪 Queue Depth/Age、Rejected/Deferred Rate、Per-channel Latency、Deadline Miss、Cancellation Propagation、Budget Exhaustion、Graph Fan-out、CPU/RAM/Disk/GPU Saturation、Partial Result 和 Noisy-neighbor Throttling。ID 放在 Trace 中，不放 Metric Label。Log 不包含原始 Memory/Evidence Content 和未授权 Count。

## 18. 接口

H/I 提供 Authenticated Identity、Policy Epoch 和 Authorization；Retrieval Engine 提供 Channel Plan/Candidate Stream；Cache/Working Set 提供 Scoped Read/Invalidation；E 提供 Index Watermark；D 提供 Canonical Fence；G 接收 Result/Completeness/Recommendation。

Typed Outcome 必须区分 Rejected、Overloaded、Cancelled、Partial、Degraded、Complete 和 Unavailable。准确 Wire Code 由 H 拥有。

## 19. 测试场景

Recall Burst；单个 Principal 造成 Noisy Neighbor；Graph Fan-out 对抗性输入；Vector Channel 很慢但 Lexical 成功；GPU 离线；Disk Saturation；ANN 中途 Deadline/Cancel；排队期间 Permission 被撤销；运行期间发生 Forget；Index Watermark 低于 Required Fence；不同 Scope 的相同 Request 不得 Coalesce；Partial Result 绝不标记为 Complete。

## 20. 依赖

D Canonical Read/Fence；E Index Adapter/Watermark；G Context Requirement/Budget Hint；H Request/Cancellation Envelope；I Identity/Permission/Revocation；Storage/Index Engine 和 Telemetry。

## 21. 开放问题

OPEN：Workload Class 和 SLO Target；H Cancellation/Error Code；I Per-principal Quota Identity；E Watermark Semantics。

CANDIDATE：Modular Monolith 内 Async Task Group、按 Class 有界 Queue、Deterministic Fallback。

TO_VALIDATE：Scheduler Policy、Parallelism、Queue Cap、Resource Isolation 和 Hardware Benchmark。

## 22. 数据模型

ScheduledRequest 绑定 request_id、Authenticated Principal、Normalized Scope Ref、Environment/Task/Session Ref、permission_epoch、Forget_epoch、request_class、deadline、cancellation state、required canonical/index fence、Reserved CPU/RAM/Candidate/Evidence Budget 和 correlation_id。

ChannelTask 绑定 channel_id、scoped predicate digest、local candidate/fan-out/time budget、source watermark、task state 和 outcome。

SchedulerLease 记录已 Admission 的 Quota Reservation、Expiry 和 Release State。

这些都是 Runtime Execution Record，不是 Canonical Domain Object，也不是 Agent Planning State。
