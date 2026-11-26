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
        - "session-d-memory-brain-2026-11-16@b525e1f8fee2471a131e4a38efda99804045e424:6b37c91033fda21f072e2a3bde6f274663b1e76e"
        - "14-ai-development/work-items/AID-2026-089/manifest.yaml"
        - "14-ai-development/work-items/AID-2026-098/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Restored from the exact source blob without editing the document body. Comparison against AID-2026-089 and AID-2026-098 found no conflicting clause. This does not assert Owner acceptance or implementation conformance."
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
    canonical_scope: "D canonical Memory identity, immutable version, lifecycle event and canonical commit cursor semantics; excludes physical backend implementation and I global policy"
    canonical_scope_id: "memory-brain/canonical-memory-store"
    canonical_scope_keywords:
      - canonical-memory-store
      - memory-version
      - lifecycle-event
      - canonical-commit-cursor
      - forget-fence-authority
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    source: "03-memory-brain/canonical-memory-store.md"
    en: "docs/en/03-memory-brain/canonical-memory-store.md"
    zh-CN: null
---

# 规范记忆存储

**状态：** 权威性与不可变性已决定；详细记录布局和事务实现仍为候选，待工程验证。  
**相关阻塞项：** INT-P0-01、INT-P0-02、INT-P0-03、INT-P0-04、INT-P1-02、INT-P1-06；DM-001..DM-013。

## 1. 目的

持久化 Memory 资产及其类型化链接的权威身份和不可变版本。提供精确历史读取、原子规范提交、生命周期状态权威、来源可见性以及可恢复的变更馈送。它不是向量数据库、事件摄取系统，也不是可变的“最新事实”表。

## 2. 范围

负责 Memory 身份、MemoryVersion、规范 Claim 修订引用（受 ADR 约束）、Entity/Relation 规范引用、Evidence/Provenance 链接、LifecycleEvent、ConflictSet 和规范 Forget 记录。不负责 Event 摄取、抽取、排序、Context 版本、策略评估、物理擦除或外部副本。

## 3. 职责

- 分配稳定的不透明 ID 并强制唯一性。
- 追加不可变的 MemoryVersion 快照；绝不覆盖历史内容。
- 维护受 CAS 保护的当前版本指针和单调提交序列。
- 验证引用、Scope 兼容性、必需证据/来源信息和 schema 版本。
- 通过原子事务或可恢复事务/outbox 提交规范数据和发布意图。
- 支持精确版本读取和双时态“在 T 时有效、到 T2 时已知”的查询。
- 暴露规范变更馈送和可重建投影检查点。

## 4. 非职责

不负责独立事实裁定、抽取、嵌入生成、检索排序、Context 组装、Agent 推理、全局授权策略、备份生命周期或物理删除执行。

## 5. 领域对象

**MemoryIdentity：** memory_id、owner_scope_ref、applicability_scope_refs、created_at、created_by_actor_ref、schema_family、identity_status。ID 稳定且永不复用。

**MemoryVersion：** memory_version_id、memory_id、sequence、parent_version_id、commit_sequence、content_digest、immutable_payload_ref/snapshot、claim_refs、entity_refs、relation_refs、evidence_refs、provenance_refs、lifecycle_projection、change_reason、author_actor_ref、recorded_at、schema_version。所有字段描述固定的已提交快照。lifecycle_projection 仅为便利快照；权威转换历史是 LifecycleEvent。

**CanonicalCommit：** operation_id、idempotency_key、request_digest、expected_version_id、resulting_version_id、commit_sequence、outcome、committed_at。它使重试具有确定性。

**LifecycleEvent：** event_id、memory_id、from_state、to_state、actor_ref、scope_refs、reason、policy_decision_ref、related_version_id、occurred_at、sequence。它是仅追加的生命周期转换唯一权威；当前生命周期状态是该有序事件流的投影。

**OutboxRecord：** event_id、aggregate_ref、aggregate_version、event_kind、payload_ref/digest、created_at、publication_state。它是持久化发布意图，不是第二个规范事实源。

## 6. 数据模型

所有记录均具有类型化 ID、schema_version、所有权 ScopeRef、适用 ScopeRefs、actor/time 元数据，以及内容型记录的 content digest。版本快照以类型化引用而非自由格式 ID 保存规范对象引用。敏感 Evidence 内容可以在更严格授权保护下单独存储；MemoryVersion 仅保存获准的 ContentRef 和完整性摘要。

Claim 和 Fact 持久化在 INT-P0-01 下明确标记为 **ADR-BLOCKED**。获批之前，本文件只允许在非冻结接口中使用中性的 PropositionRef/不透明提案封装；不得根据任一候选方案生成 DDL、公共 schema、稳定跨模块 wire 字段或不可变 Fact/Claim 对象身份。候选修订模型为：稳定 Claim 身份加不可变 ClaimRevision ID，每个修订关联一个或多个 MemoryVersion；在 INT-P1-02 下仍为 **CANDIDATE**。

## 7. 状态机

提交：Draft proposal → Validated → Committed 或 Rejected/Deferred。只有 Committed 才创建 MemoryVersion 并推进当前指针。使用相同幂等键和相同请求摘要重试时返回原提交；相同键但请求摘要不同则返回 IDEMPOTENCY_CONFLICT。

生命周期不是可变列的权威：仅追加的 LifecycleEvent 流才是权威；当前状态是确定性折叠/物化投影。MemoryVersion 可以为高效读取快照记录提交时观察到的生命周期状态，但不能独立改变该状态。

## 8. 操作

CreateMemoryIdentity；CommitVersion(expected_current_version)；ReadCurrent；ReadVersion；ReadAsOf(valid_time, known_by_time)；ListChanges(after_sequence, scope_filter)；ReadLifecycleHistory；RebuildProjection；ResolveIdempotency；AppendLifecycleEvent。

提交序列：

1. 认证并解析 ActorRef 和 ScopeRefs。
2. I 授权操作/资源；Brain 验证 Scope 语义。
3. 验证 schema、期望版本、引用、内容摘要和来源完整性。
4. 验证每个被引用对象均可见且 Scope 兼容。
5. 原子持久化不可变版本、指针更新、幂等记录和 outbox 事件（或等效可恢复提交协议）。
6. 返回提交回执和规范序列。
7. 投影/索引异步消费 outbox 并发布 watermark。

## 9. 不变量

- Memory ID 在各版本间保持稳定且永不复用。
- MemoryVersion 不可变，且至多有一个父版本。
- 当前指针引用同一 Memory 的已提交版本。
- 提交序列在规范权威范围内单调递增。
- 过期的期望版本绝不能覆盖较新版本。
- 必需来源信息与目标版本一同提交，或被明确标记为不可用。
- 未经明确授权共享，不接受跨 Scope 引用。
- 投影延迟不会改变规范事实。
- LifecycleEvent 是唯一的生命周期转换权威（解决 DM-008 候选项）。
- Forget 不会静默改写历史；受治理的擦除可以使载荷不可用，同时仅保留允许的、不可重构内容的墓碑元数据。

## 10. 接口

E 提交候选对象和建议的父/基准引用；Store 返回规范 Memory ID、MemoryVersion ID、提交序列、生命周期决定和 outbox 事件 ID。E 不得写入 Store 内部结构或绕过 Lifecycle Manager。

F 读取当前或精确历史版本，并必须执行 Scope 过滤和显式展开限制。Store 返回规范记录；仅在相关时返回投影 watermark；F 不得将过期投影视为规范事实。

G 引用不可变的 Memory ID + MemoryVersion ID。G 拥有 ContextVersion 和 ChangeSet；Store 不跟踪 Context 生命周期。如果 G 选择读取时取当前版本，则必须在已提交的 Context 条目中固定解析出的版本。

H 仅接收不透明类型化引用；wire 表示由 H 负责。I 提供授权决定/策略版本以及 Forget/Retention 义务。每次调用均带有 actor、scope、idempotency 和 correlation 元数据。

## 11. 错误处理

NOT_FOUND_OR_NOT_VISIBLE；STALE_VERSION；IDEMPOTENCY_CONFLICT；INVALID_REFERENCE；SCOPE_MISMATCH；PERMISSION_DENIED；INVALID_SCHEMA；PROVENANCE_INCOMPLETE；CONTENT_DIGEST_MISMATCH；LIFECYCLE_EVENT_ORDER_ERROR；OUTBOX_LAG；HISTORY_UNAVAILABLE_DUE_TO_FORGET。错误为结构化且避免泄露信息。

## 12. 一致性

规范事务边界包括身份/版本行、当前指针、提交回执、操作涉及的 LifecycleEvent 以及 outbox 意图。如果选定存储无法原子提交所有这些内容，则使用带恢复标记的持久化 prepare/commit 协议；不得将部分提交的版本暴露为规范版本。Outbox 消费者采用至少一次投递；事件 ID 和聚合版本使处理具备幂等性。索引和图投影可从规范记录及保留的事件/来源历史重建。

## 13. 安全 / Scope

在物化查询候选项之前执行 Scope 过滤。Evidence ContentRef 解引用需要独立授权。没有 Scope 和权限检查，基于名称的查找不得返回身份。读取方和投影消费者必须检查 Forget fence/suppression。缓存和索引命名空间包括 principal/scope/environment 以及 policy/grant revision；过期授权应使缓存失效或绕过缓存。Memory 文本是不可信数据（INT-P0-04）。

## 14. 性能考量

仅为候选方案：追加式版本加紧凑的当前状态投影；周期性快照可以加速历史折叠，但仍是派生数据。测量写放大、快照大小、CAS 竞争、outbox 延迟、历史查询成本、Scope 过滤开销和重建吞吐量。限制历史分页，除非显式请求，否则避免加载 Evidence 载荷。

## 15. 可观测性

记录提交序列、父/结果版本、请求摘要、actor/scope ID、correlation/causation、幂等键哈希、事务耗时、CAS 冲突、outbox 年龄、消费者 watermark 和投影重建状态。绝不记录已 Forget 的原始内容或受保护的 Evidence。

## 16. 故障场景

- 提交前崩溃：没有可见版本；可以重试。
- 提交后、响应前崩溃：幂等记录返回原回执。
- Outbox 发布失败：持久化记录可重放。
- 写入方版本过期：拒绝并要求重新读取/协调。
- 投影损坏：从规范源重建；不得从投影修复规范记录。
- 受治理 Forget 后历史载荷缺失：返回明确的 forgotten/unavailable 结果，不得伪造内容。
- 授权服务不可用：对受保护读取和写入 fail closed。

## 17. 依赖

Domain Model（B）提供类型语义；Lifecycle Manager 管理转换；E 提供提案合同；F 提供读取/投影语义；G 固定 MemoryVersion 引用；H 负责 ActorRef/wire 身份；I 负责授权、Forget、保留和擦除策略；Storage/Consistency 负责事务、备份和恢复实现。

## 18. 未决问题

- OPEN：INT-P0-01 ADR 必须在 schema 冻结前解决 Fact/Claim。
- CANDIDATE：稳定 Claim ID + 不可变 ClaimRevision；与 E/F/G 确认。
- OPEN：事务/outbox 实现和原子性保证。
- OPEN：规范序列分区和多租户排序。
- OPEN：Forget 后合法保留/墓碑字段；与 I 协调。
- TO_VALIDATE：存储引擎、快照周期、读写和恢复基准测试。


## Phase 3 修复——规范游标边界（2026-11-16）

本节取代此前对“sequence”“watermark”或“generation”的任何未类型化用法。以下类型彼此不同，**MUST NOT** 相互比较、相加、替代或序列化为一个通用整数：

| 类型 | 权威 / 范围 | 含义和排序 |
|---|---|---|
| `CanonicalCommitCursor` | D Canonical Store；一个 Brain 权威域 | 全局有序的已提交事务位置。仅在原子提交成功时分配。它对规范事务排序，而非聚合修订或下游应用。 |
| `AggregateRevision` | D；单个聚合身份（Memory、Entity、Relation 等） | 在该聚合内单调递增的修订号。不可进行全局比较，也不表示提交流位置。已提交修订同时携带其 `CanonicalCommitCursor`。 |
| `LifecycleEventCursor` | D；单个 Memory 生命周期流 | 元组 `(memory_id, lifecycle_event_sequence, event_id)`；序列在该 Memory 的仅追加生命周期流内连续。每个事件还记录其外层 `CanonicalCommitCursor`。 |
| `IndexWatermark` | F；单个 index/channel/partition | 元组 `(index_id, partition_id, applied_through: CanonicalCommitCursor, coverage/schema metadata)`。表示该分区已核算到所述前缀内的每个规范提交；它不是 D commit cursor，也绝不证明 Forget 完成。 |
| `ForgetFenceCursor` | D 规范 Forget 权威；操作 + 受影响目标集 | 元组 `(forget_operation_id, fence_generation, target_set_digest)`；generation 由 D 单调分配。它建立抑制 epoch，不是提交位置或索引 watermark。 |

ContextVersion 仍由 G 所有，不属于上述任何一种。BMCP delivery/request ID 仍由 H 所有。I 的 permission/revocation epoch 仍由 I 所有。D 合同不定义它们的 wire 编码。

### 规范事务可见性与重放

成功的规范事务会原子地使其规范对象/修订写入、聚合 head CAS 更新、相关 LifecycleEvent 追加、持久化 CanonicalCommit 记录和可恢复 outbox 意图全部可见。事务在提交序列化时恰好获得一个全局有序的 `CanonicalCommitCursor`。已中止/拒绝的事务不获得 cursor；因此提交流不会因回滚的序列分配而产生空洞。按 `as_of` cursor 读取的读者要么观察到整个事务，要么完全看不到。只有持久化提交后 cursor 才可见。

消费者严格从最后一个已持久化应用的 cursor 之后继续。允许重新投递，并且必须通过稳定的事件/操作 ID 实现幂等。消费者不得越过缺失提交、应用失败事务或未知 schema 来推进连续应用前缀。乱序工作可以暂存，但 watermark 必须保持在最后一个连续前缀，直至缺口修复。如果保留历史不再覆盖请求的 cursor，消费者必须从带有基准 cursor 的一致快照启动，再继续重放；不得静默跳到“latest”。Outbox 发布可以延迟、重试，但不能改变规范提交顺序或权威。投影 watermark 只报告应用覆盖范围，不改变规范事实。

### Lifecycle event cursor

LifecycleEvent 序列属于单个 Memory 生命周期流，仅在事件及其外层规范事务提交时分配。消费者观察到序列缺口意味着生命周期事件缺失/未应用，必须重放/协调。事件的 commit cursor 提供跨聚合事务排序；其 lifecycle cursor 提供每个 Memory 内的生命周期顺序。二者互不替代。


## Phase 3 修复——规范提交合同

### Commit cursor 决定

**已决定（D 领域合同）：** `CanonicalCommitCursor` 是单一 Canonical Memory 权威范围内全局有序的 cursor，而不是每个聚合各自的修订号。每个聚合修订仍是独立的 `AggregateRevision`。规范事务记录是连接点：记录 commit cursor 以及该事务创建的精确聚合修订。一个事务可以推进多个聚合 head，同时只获得一个 commit cursor。

只有在所有验证/CAS 检查成功且事务持久化提交之后，才在序列化提交路径中分配 cursor。commit record、不可变写入、head 变更、LifecycleEvent 追加和 outbox 意图原子可见。CAS 被拒绝或事务中止时不消耗 cursor。读者绝不会观察到部分提交的事务。

### 缺口、重放与 outbox

规范已提交流按定义连续。消费者观察到的缺口是运行时缺口（发布缺失、应用失败或历史不可用），不是跳过许可。消费者持久化最后一个连续应用 cursor，使用幂等事件 ID 从该位置之后重放，并在推进前修复缺口。如果历史已过期，则必须使用一致快照及其基准 cursor。Outbox 投递可以延迟、重复或重试；不能重新编号提交。IndexWatermark 由 F 所有，报告一个索引分区已应用的连续规范前缀。它不是 outbox 私有 offset，也不是 ForgetFenceCursor。

### 事务可见性测试

1. MemoryVersion + aggregate head + LifecycleEvent + outbox intent 的提交产生一个 cursor，并且全部同时可见。
2. CAS 失败不产生新修订、事件、outbox intent 或 commit cursor。
3. 持久化提交后、outbox 发布前崩溃，通过重放相同已提交事件 ID 和 cursor 恢复。
4. 重复/乱序投递不会重复产生效果，也不会越过缺失提交推进连续 watermark。
5. cursor N 的快照加上 N 之后的重放，与完整重放产生相同规范状态。
6. 一个事务中提交的两个聚合共享事务 cursor，但保留各自独立的聚合修订。

### 接口

- E 发布/消费自己的持久化 ingress 和 compile cursor；E 仅将 CanonicalCommitCursor 作为 D 的提交结果接收，并在可见前注册派生依赖。
- F 消费 CanonicalCommitCursor 并发布自己的每索引 IndexWatermark；对外暴露前重新验证规范状态和 ForgetFence。
- G 消费 D 生命周期/变更信号和精确 MemoryVersion 引用；G 的 ContextVersion 独立。
- H 传输不透明类型化引用和确认；D 不定义 wire 编码。
- I 提供授权/撤销策略；D 不定义 policy epoch 或全局完成规则。
