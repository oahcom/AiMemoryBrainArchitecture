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
        - "14-ai-development/work-items/AID-2026-150/manifest.yaml"
        - "14-ai-development/work-items/AID-2026-242/evidence.md"
        - "Source branch session-d-memory-brain-2026-11-16 @ b525e1f8fee2471a131e4a38efda99804045e424"
        - "AID-2026-089 / PR #1232 — D-only logical Fence authority"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Historical source restored; §17 Fence-owner wording is explicitly superseded by AID-2026-089. Candidate only; no D Owner acceptance, cross-owner acceptance, implementation or production conformance is asserted."
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
    canonical_scope: "D canonical Memory identity, immutable version, lifecycle and canonical commit/change-feed semantics (historical candidate; Fence boundary controlled by AID-2026-089)"
    canonical_scope_id: "memory-brain/canonical-memory-store"
    canonical_scope_keywords:
      - canonical-memory-store
      - memory-version
      - canonical-commit-cursor
      - index-watermark
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "03-memory-brain/canonical-memory-store.md"
    en: "docs/en/03-memory-brain/canonical-memory-store.md"
---
# Canonical Memory Store（权威记忆存储）

> **恢复／权威冲突声明——仅供参考，不具规范效力。** 本历史源文件除本声明及 GOV-DOC-002 元数据外，按原始字节保留。其 §17 依赖句将“Forget Fence”归于 I。该表述与 AID-2026-089 冲突；AID-2026-089 已由 PR #1232 合并（合并提交 `d914e8a1f8a1ba24c21c41a9249489d544388185`）：D 是 ForgetOperation 身份／状态及 ForgetFence Generation／Cursor 的唯一逻辑签发权威；Storage 本地 Fence 行只能是源自 D、可重建的投影；I 负责授权、全局政策及 Global Forget Completion。该边界以 AID-2026-089 为准。不得将 §17 解读为 I 拥有 Fence 签发权，或 Storage 拥有独立 Fence 权威。本恢复文件仍是 Draft／Informative 候选文件，不是已批准的规范性合同。

## 1. 目的

持久化 Memory 资产及其类型化链接的权威身份和不可变版本。提供精确历史读取、原子 Canonical Commit、Lifecycle 状态权威、Provenance 可见性和可恢复变更流。它不是向量数据库、事件接收系统，也不是可变的“最新事实”表。

## 2. 范围

拥有 Memory Identity、MemoryVersion、受 ADR 约束的 Canonical Claim Revision 引用、Entity/Relation Canonical 引用、Evidence/Provenance 链接、LifecycleEvent、ConflictSet 和 Canonical Forget 记录。不拥有 Event Ingestion、Extraction、Ranking、Context Version、Policy Evaluation、Physical Erasure 或外部副本。

## 3. 职责

- 分配稳定的不透明 ID 并强制唯一性。
- 追加不可变 MemoryVersion Snapshot；绝不覆盖历史内容。
- 维护受 CAS 保护的 Current Version Pointer 和单调 Commit Sequence。
- 校验引用、Scope 兼容性、必需 Evidence/Provenance 和 Schema Version。
- 通过原子事务或可恢复 Transaction/Outbox 提交 Canonical Data 和发布意图。
- 支持精确版本读取和双时态查询：“在 T 时有效，并在 T2 时已知”。
- 暴露 Canonical Change Feed 和可重建的 Projection Checkpoint。

## 4. 非职责

不负责独立裁定真伪、提取、Embedding 生成、检索排序、Context 组装、Agent 推理、全局授权策略、备份生命周期或物理删除执行。

## 5. 领域对象

- **MemoryIdentity：** memory_id、owner_scope_ref、applicability_scope_refs、created_at、created_by_actor_ref、schema_family、identity_status。ID 稳定且永不复用。
- **MemoryVersion：** memory_version_id、memory_id、sequence、parent_version_id、commit_sequence、content_digest、immutable_payload_ref/snapshot、claim_refs、entity_refs、relation_refs、evidence_refs、provenance_refs、lifecycle_projection、change_reason、author_actor_ref、recorded_at、schema_version。它是固定的已提交快照。lifecycle_projection 仅为便利字段；LifecycleEvent 才是权威。
- **CanonicalCommit：** operation_id、idempotency_key、request_digest、expected_version_id、resulting_version_id、commit_sequence、outcome、committed_at。用于确定性重试。
- **LifecycleEvent：** event_id、memory_id、from_state、to_state、actor_ref、scope_refs、reason、policy_decision_ref、related_version_id、occurred_at、sequence。它是追加式生命周期转换唯一权威；当前状态是该有序流的投影。
- **OutboxRecord：** event_id、aggregate_ref、aggregate_version、event_kind、payload_ref/digest、created_at、publication_state。它是持久化发布意图，不是第二个 Canonical Truth 来源。

## 6. 数据模型与 ADR 边界

所有记录都有类型化 ID、schema_version、所有权 ScopeRef、适用 ScopeRefs、Actor/Time 元数据；有内容的记录还具有 Content Digest。Version Snapshot 使用类型化引用指向 Canonical 对象，不使用自由格式 ID。敏感 Evidence 内容可以在更严格授权控制下单独存储；MemoryVersion 只保存获准的 ContentRef 和完整性 Digest。

Claim 和 Fact 持久化在 INT-P0-01 下明确为 **ADR-BLOCKED**。在正式批准之前，未冻结接口只允许使用中性的 PropositionRef/不透明提案 Envelope。不得从任一备选方案生成 DDL、公共 Schema、稳定跨模块 Wire 字段或不可变 Fact/Claim 对象身份。候选修订模型：稳定 Claim Identity 加不可变 ClaimRevision ID，每个 Revision 关联一个或多个 MemoryVersion；在 INT-P1-02 下仍为 CANDIDATE。

## 7. Commit 状态机

Draft Proposal → Validated → Committed 或 Rejected/Deferred。只有 Committed 才会创建 MemoryVersion 并推进 Current Pointer。相同 Idempotency Key/相同 Request Digest 返回原 Commit；相同 Key/不同 Digest 返回 IDEMPOTENCY_CONFLICT。

Lifecycle 不是可变列权威：追加式 LifecycleEvent Stream 才是权威；当前状态由该流确定性折叠/物化得到。MemoryVersion 可以为高效读取快照记录提交时观察到的 Lifecycle State，但不能独立修改它。

## 8. 操作与提交顺序

操作：CreateMemoryIdentity；CommitVersion(expected_current_version)；ReadCurrent；ReadVersion；ReadAsOf(valid_time, known_by_time)；ListChanges(after_sequence, scope_filter)；ReadLifecycleHistory；RebuildProjection；ResolveIdempotency；AppendLifecycleEvent。

提交顺序：
1. 认证/解析 ActorRef 和 ScopeRefs。
2. I 授权操作/资源；Brain 校验 Scope 语义。
3. 校验 Schema、Expected Version、引用、Content Digest 和 Provenance 完整性。
4. 验证每个引用对象可见且 Scope 兼容。
5. 原子持久化不可变 Version、Pointer 更新、Idempotency Record 和 Outbox Event，或采用等价可恢复提交协议。
6. 返回 Commit Receipt 和 Canonical Sequence。
7. Projection/Index 异步消费 Outbox 并发布 Watermark。

## 9. 不变量

- Memory ID 在不同 Version 之间稳定且永不复用。
- MemoryVersion 不可变，最多只有一个 Parent。
- Current Pointer 必须指向同一个 Memory 的已提交 Version。
- Commit Sequence 在 Canonical Authority 内单调递增。
- 过期 Expected Version 不得覆盖新版本。
- 必需 Provenance 与目标 Version 一起提交，或明确标记不可用。
- 没有明确授权共享时，不接受跨 Scope 引用。
- Projection 滞后不改变 Canonical Truth。
- LifecycleEvent 是唯一状态转换权威（解决 DM-008 候选）。
- Forget 不得静默改写历史；受治理擦除可以使 Payload 不可用，同时只保留允许且不可反向重建内容的 Tombstone 元数据。

## 10. 接口

- **E：** 提交 Candidate Object 和 Proposed Parent/Base Reference；Store 返回 Canonical Memory ID、MemoryVersion ID、Commit Sequence、Lifecycle Decision 和 Outbox Event ID。E 不得写 Store 内部，也不得绕过 Lifecycle Manager。
- **F：** 读取当前或精确历史版本，必须使用 Scope Filter 和明确展开限制。Store 返回 Canonical Record；仅在相关时提供 Projection Watermark。F 不得把陈旧 Projection 当作 Canonical。
- **G：** 引用不可变 Memory ID + MemoryVersion ID。G 拥有 ContextVersion/ChangeSet；Store 不跟踪 Context Lifecycle。如果 G 选择 Read 时读取 Current，必须在已提交 Context Entry 中固定解析出的 Version。
- **H：** 只接收不透明类型化引用；Wire 表示由 H 拥有。
- **I：** 提供授权决策/Policy Version 和 Forget/Retention 义务。

每次调用都携带 Actor、Scope、Idempotency 和 Correlation 元数据。

## 11. 错误

NOT_FOUND_OR_NOT_VISIBLE；STALE_VERSION；IDEMPOTENCY_CONFLICT；INVALID_REFERENCE；SCOPE_MISMATCH；PERMISSION_DENIED；INVALID_SCHEMA；PROVENANCE_INCOMPLETE；CONTENT_DIGEST_MISMATCH；LIFECYCLE_EVENT_ORDER_ERROR；OUTBOX_LAG；HISTORY_UNAVAILABLE_DUE_TO_FORGET。错误必须结构化且符合信息披露安全要求。

## 12. 一致性

Canonical Transaction 边界包含 Identity/Version 行、Current Pointer、Commit Receipt、操作包含时的 Lifecycle Event，以及 Outbox Intent。如果所选 Storage 无法原子提交全部内容，必须使用带恢复标记的持久化 Prepare/Commit 协议；不得将部分提交的 Version 暴露为 Canonical。Outbox Consumer 采用 At-least-once；Event ID 和 Aggregate Version 保证处理幂等。Index 和 Graph Projection 可由 Canonical Record 加保留的 Event/Provenance History 重建。

## 13. 安全 / Scope

在物化 Query Candidate 之前执行 Scope Filter。Evidence ContentRef 解引用需要独立授权。基于 Name 的查询在没有 Scope/Permission 检查时不能返回身份。Read 和 Projection Consumer 必须检查 Forget Fence/Suppression。Cache/Index 命名空间包含 Principal/Scope/Environment 和 Policy/Grant Revision；过期 Grant 必须使 Cache 失效或绕过 Cache。Memory 文本是不可信数据（INT-P0-04）。

## 14. 性能考量

**CANDIDATE：** 采用追加式 Version 加紧凑 Current Projection；周期性 Snapshot 可以加速历史折叠，但仍属于派生数据。测量写放大、Snapshot 大小、CAS 竞争、Outbox 滞后、历史查询成本、Scope Filter 开销和重建吞吐。限制历史分页；除非明确请求，不加载 Evidence Payload。

## 15. 可观测性

记录 Commit Sequence、Parent/Result Version、Request Digest、Actor/Scope ID、Correlation/Causation、Idempotency Key Hash、事务耗时、CAS Conflict、Outbox Age、Consumer Watermark 和 Projection Rebuild 状态。绝不记录已遗忘原文或受保护 Evidence。

## 16. 故障场景

- Commit 前崩溃：没有可见 Version；可以重试。
- Commit 后、响应前崩溃：Idempotency Record 返回原 Receipt。
- Outbox 发布失败：持久化记录通过 Replay 恢复。
- 过期 Writer：拒绝并要求重新读取/协调。
- Projection 损坏：从 Canonical Source 重建；不得从 Projection 修复 Canonical Record。
- 受治理 Forget 后历史 Payload 缺失：返回明确的 Forgotten/Unavailable 结果，不得伪造内容。
- 授权服务故障：受保护读写 Fail-closed。

## 17. 依赖

依赖 B 的类型语义；Lifecycle Manager 的状态转换；E 的提案契约；F 的读取/Projection 语义；G 固定的 MemoryVersion 引用；H 的 ActorRef/Wire 身份；I 的授权、Forget Fence、Retention 和 Erasure Policy；Storage/Consistency 的事务、备份和恢复实现。

## 18. 开放问题

- OPEN：INT-P0-01 ADR 必须在 Schema Freeze 前解决 Fact/Claim。
- CANDIDATE：稳定 Claim ID + 不可变 ClaimRevision；需与 E/F/G 确认。
- OPEN：Transaction/Outbox 实现及原子性保证。
- OPEN：Canonical Sequence 分区和多租户排序。
- OPEN：Forget 后合法的 Retention/Tombstone 字段；与 I 协调。
- TO_VALIDATE：Storage Engine、Snapshot 周期、读写和恢复基准。

## Phase 3 整改 — 规范 Cursor 边界

以下是不同类型，**MUST NOT** 将它们比较、相加、替代，或序列化成一个通用整数：

| 类型 | 权威/范围 | 含义与排序 |
|---|---|---|
| CanonicalCommitCursor | D Canonical Store；单个 Brain Authority | 全局有序的已提交事务位置；仅在成功原子提交时分配；排序 Canonical Transaction，不排序 Aggregate Revision 或下游应用 |
| AggregateRevision | D；单个 Aggregate Identity | 单个 Aggregate 内单调递增的 Revision；不可全局比较；已提交 Revision 同时携带 CanonicalCommitCursor |
| LifecycleEventCursor | D；单个 Memory Lifecycle Stream | (memory_id, lifecycle_event_sequence, event_id)；在单个 Memory Stream 内连续；每个 Event 也记录所属 CanonicalCommitCursor |
| IndexWatermark | F；单个 Index/Channel/Partition | (index_id, partition_id, applied_through: CanonicalCommitCursor, coverage/schema metadata)；仅表示 Partition 覆盖进度，绝不是 Forget Proof |
| ForgetFenceCursor | D；Operation + 受影响 Target Set | (forget_operation_id, fence_generation, target_set_digest)；单调抑制 Epoch，不是 Commit Position 或 Index Watermark |

ContextVersion 仍由 G 拥有。BMCP Delivery/Request ID 仍由 H 拥有。I 的 Permission/Revocation Epoch 仍由 I 拥有。D 不定义这些字段的 Wire Encoding。

### Canonical Transaction 可见性与 Replay

成功的 Canonical Transaction 原子暴露 Canonical Write/Revision、Aggregate Head CAS 更新、LifecycleEvent 追加、CanonicalCommit Record 和可恢复 Outbox Intent。它在 Commit Serialization 时获得唯一一个全局有序 CanonicalCommitCursor。中止/拒绝的事务不获得 Cursor；因此回滚的序列分配不会在已提交 Canonical Stream 中造成空洞。按 As-of Cursor 读取时，必须观察到整个事务或完全看不到。Cursor 只有在持久化提交后才可见。

Consumer 严格从最后一个持久化应用的 Cursor 之后恢复。允许重新投递，但必须按稳定 Event/Operation ID 保证幂等。Consumer 不得越过缺失 Commit、应用失败或未知 Schema 推进连续前缀。乱序工作可以暂存，但 Watermark 必须停留在最后一个连续前缀，直到缺口修复。如果保留历史已不覆盖请求 Cursor，则加载带 Base Cursor 的一致 Snapshot，再继续；不得静默跳到 Latest。Outbox 发布可以延迟/重试，但不能改变 Canonical 顺序。Projection Watermark 只报告应用覆盖情况，不能改变 Canonical Truth。

### Lifecycle Event Cursor

LifecycleEvent Sequence 属于单个 Memory Stream，只有在 Event 和所属 Canonical Transaction 提交时才分配。Consumer 观察到 Sequence 缺口，意味着存在缺失/未应用 Lifecycle Event，需要 Replay/Reconciliation。Commit Cursor 提供跨 Aggregate 事务顺序；Lifecycle Cursor 提供 Per-Memory 顺序。二者不能互相替代。

## Phase 3 整改 — Canonical Commit 契约

**DECIDED（D 领域契约）：** CanonicalCommitCursor 在单个 Canonical Memory Authority 内全局有序，不是 Per-Aggregate Revision。AggregateRevision 保持独立。Canonical Transaction Record 将 Commit Cursor 与该事务创建的准确 Aggregate Revision 关联起来。一个事务可以推进多个 Aggregate Head，但只获得一个 Commit Cursor。

只有在 Validation/CAS 成功且事务已持久化提交后，Cursor 才能在串行化提交路径中分配。Commit Record、不可变写入、Head 变更、LifecycleEvent 追加和 Outbox Intent 必须原子可见。被拒绝的 CAS/中止事务不消耗 Cursor。读取方永远不能看到部分提交。

### Gap、Replay 与 Outbox

Canonical Committed Stream 按定义连续。Consumer 观察到的 Gap 是运维缺口，不是跳过的许可。Consumer 持久化最后一个连续应用 Cursor，使用幂等 Event ID 从其后 Replay，并在推进前修复缺口。若历史已过期，必须使用一致 Snapshot 和 Base Cursor。Outbox Delivery 可以延迟、重复或重试，但不能重新编号 Commit。IndexWatermark 由 F 拥有，报告单个 Index Partition 已应用的连续 Canonical 前缀。它既不是 Outbox 私有 Offset，也不是 ForgetFenceCursor。

### Transaction Visibility 测试

1. MemoryVersion + Aggregate Head + LifecycleEvent + Outbox Intent 提交时产生一个 Cursor，并且全部同时可见。
2. CAS 失败不产生新 Revision、Event、Outbox Intent 或 Commit Cursor。
3. 持久化提交后、Outbox 发布前崩溃，必须通过重放相同已提交 Event ID/Cursor 恢复。
4. 重复/乱序 Delivery 不得重复产生效果，也不得越过缺失 Commit 推进连续 Watermark。
5. Cursor N 的 Snapshot 加上 N 之后的 Replay，必须得到与完整 Replay 相同的 Canonical State。
6. 同一事务提交的两个 Aggregate 共享事务 Cursor，但保留各自独立 Revision。

### 接口

- E 发布/消费自己的持久化 Ingress/Compile Cursor；只将 CanonicalCommitCursor 作为 D 的 Commit Result 接收，并在可见前登记派生依赖。
- F 消费 CanonicalCommitCursor 并发布每个 Index 自己的 IndexWatermark；暴露前重新验证 Canonical State 和 ForgetFence。
- G 消费 D Lifecycle/Change Signal 和准确 MemoryVersion 引用；G 的 ContextVersion 独立。
- H 传输不透明类型化引用和 ACK；D 不定义 Wire Encoding。
- I 提供授权/撤销策略；D 不定义 Policy Epoch 或全局完成规则。