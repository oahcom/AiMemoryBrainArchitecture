---
document_metadata:
  domain: memory-brain
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
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-11-26-SOURCE-RESTORE-02"
        - "Issue #1177"
        - "source commit: b525e1f8fee2471a131e4a38efda99804045e424"
        - "original source blob: b4ed712ac0626ab127cccfd205c50a9013df01fb"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Existing translated companion body preserved; source pin refreshed; semantic parity review pending."
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
    source: "03-memory-brain/memory-brain-overview.md"
    en: "docs/en/03-memory-brain/memory-brain-overview.md"
    zh-CN: null
---

# Memory Brain — 子系统架构

- 文档 ID：D-MEMORY-BRAIN-001
- 版本：1.0
- 源分支：session-d-memory-brain-2026-11-16
- 源文件版本：9ca153df403d09264a50add8ad78bb5a6111c7c0
- 审查时源分支 HEAD：6b654d5cffaeb71b01f2b0750daa0abc14eb64b3
- 源规范：[D 规范源](../../../03-memory-brain/memory-brain-overview.md)（源提交 `b525e1f8fee2471a131e4a38efda99804045e424`；原始源 Blob `b4ed712ac0626ab127cccfd205c50a9013df01fb`）。
- 对应英文：[Memory Brain — Subsystem Architecture](../../en/03-memory-brain/memory-brain-overview.md)
- 状态：权威边界和不变量为 DECIDED；详细对象/操作契约为 CANDIDATE；OPEN 项不具规范约束力
- Owner：Session D — Memory Brain Principal Architecture

## 1. 目的

Memory Brain 是持久化、可寻址 Canonical Memory 资产的逻辑权威，包括 Memory 身份和不可变版本、受 ADR 约束的 Claim/Fact 语义、Entity 身份、类型化 Relation、Evidence 引用、Provenance 血缘、生命周期历史，以及受治理 Forget/Retention 的领域支持。

它独立于任何 Agent、LLM、推理供应商或 Agent 框架保存记忆资产。其 Rust Modular Monolith 是实现目标；逻辑组件代表职责边界，不强制对应独立进程、服务或 Crate。

## 2. 范围

范围内：Canonical Memory Store；身份/版本管理；Claim 和拟议 Fact 模型；Entity 与 Relationship 管理；Lifecycle Manager；历史查询；带 Scope 的资源引用；Provenance 和 Evidence 链接；Forget 依赖发现和操作记录；面向 E/F/G/H/I 的稳定内部契约。

范围外：Event Ingress 和完整编译流水线（E）；检索调度、排序和 Runtime Cache（F）；Context 规划/编辑/投递及 Context 状态机（G）；Agent Adapter 和 BMCP Wire Protocol（H）；全局 Principal 认证、策略评估、物理擦除执行、备份策略和安全治理（I）。

## 3. 职责

- 拥有 Canonical Identity、不可变 Canonical Revision、当前版本指针和历史解释。
- 提交前校验领域不变量；保留 Evidence、Provenance、时间和认知限定。
- 提供 Lifecycle 转换决策和追加式转换历史。
- 仅在明确且兼容的 Scope 内解析 Entity 身份；保留 Merge/Split 历史。
- 存储类型化、带时间、由 Evidence 支持的 Relation。
- 提供 Scope-aware 读取和类型化引用；绝不从 Display String 推断身份。
- 维护持久化 Forget Operation 模型和依赖清单契约，但不声称能控制第三方副本。
- 通过可恢复 Outbox/Change-feed 边界发布 Canonical 变更记录。

## 4. 非职责

Brain 不负责规划、推理、选择行动、调用工具、执行 Skill、控制 Environment、决定 LLM Prompt 或授予工具权限。它不拥有原始 Event 接收、提取算法、Embedding/Index 实现、Runtime 排序、Context 预算、BMCP 序列化、全局授权策略或外部系统的物理删除。

## 5. 领域对象

| 对象 | 含义与身份 |
|---|---|
| Memory | 持久化知识资产身份；在不可变 Memory Version 之间保持稳定。 |
| MemoryVersion | Memory 的 Canonical 内容和引用的不可变已提交快照。 |
| Claim | 关于 Entity、Event 或状态的命题，带认知和时间限定。 |
| FactRecord（CANDIDATE；ADR 阻塞） | 可独立寻址的 Attestation/限定，表示命题满足了声明的验证标准；不宣称形而上学意义上的绝对确定。 |
| Evidence | 支持、反驳或限定命题的来源材料/观察，或受保护的定位引用。 |
| ProvenanceRecord | 不可变派生记录，将目标关联到类型化来源和方法身份。 |
| Entity | 指代对象的稳定身份；显示名称和别名不是身份。 |
| EntityVersion | Entity 身份的不可变描述/档案修订。 |
| Relation | 带类型、有向或明确对称的关联，包含有效性、Evidence、Scope 和修订。 |
| ConflictSet | 不兼容 Claim 及其 Evidence/解决历史的显式集合。 |
| LifecycleEvent | 生命周期转换的追加式权威记录。 |
| ForgetOperation | 用于访问抑制、依赖发现、派生物处理和完成例外的持久化受治理工作流记录。 |
| ScopeRef / ActorRef / TypedObjectRef | 所有跨对象契约中使用的稳定类型化引用。 |

## 6. 数据模型

所有 ID 都是不透明且不承载语义的。UUIDv7 只是候选实现选项。时间戳在相关时保留来源精度和时区；规范化时间点使用 UTC。有效时间区间默认左闭右开 [start,end)。Unknown 必须显式表达。

每个受保护资产携带一个所有权 ScopeRef，以及零个或多个适用范围 ScopeRef。共享通过独立治理的 Grant 表达，不得重写所有权或简单合并 Scope。每个资产还携带创建/记录元数据和 Schema Version。

MemoryVersion 快照包含 Content Digest、父版本、提交序列、作者 ActorRef、原因、不可变 Claim 引用/快照、Entity/Relation 引用、Evidence/Provenance 引用、时间元数据和 Schema Version。它不是代表当前真相的可变数据库行。

## 7. 状态机

Memory Lifecycle：Candidate → Consolidated → Active → Superseded 或 Archived。Active/Superseded 可以转入 Archived。Archived → Active 需要明确恢复授权，以及新的可审计转换/版本。

Forget 不是 Memory Lifecycle 状态或转换。受治理的 ForgetOperation 安装持久化抑制 Fence；满足 I 提供的适用完成标准后，Memory 才能从现有的任意非 Forgotten Lifecycle 状态直接转换到终态 Forgotten。操作进行中的状态绝不能存储在 Memory Lifecycle 字段中。Forget 后不得复活；重新提供的信息必须获得新身份和 Provenance。

Claim Epistemic Status 独立存在：Observed、Reported、Inferred、Verified、Disputed、Retracted。Entity Identity Status 和 Relation Lifecycle 是独立状态机。若 FactRecord 获批，其状态由自己的 ADR 单独定义。Context 和 Delivery 状态属于 G/Sync，而不属于 Brain。

## 8. 操作

核心命令：CreateCandidate；CommitMemoryVersion(expected_version)；ReadMemory(at_version/as_of)；TransitionLifecycle(expected_state/version)；ReviseClaim；RetractClaim；Create/UpdateEntityVersion；ResolveEntity；MergeEntities；SplitEntity；Create/Revise/Retract/SupersedeRelation；CreateConflictSet；TraverseProvenance；StartForget；EnumerateForgetDependencies；RecordForgetTargetProgress；CompleteForget。

每次修改都包含已认证 ActorRef、已解析 ScopeRefs、操作/资源身份、Schema Version、Idempotency Key、Correlation/Causation ID、Reason 和 Expected Version/State。授权由 I 评估；Brain 独立校验语义 Scope 兼容性，并拒绝未解析 Scope。

## 9. 不变量

- Canonical Memory 身份和版本历史由 Brain 拥有（I-01）。
- Event、Memory、Claim、Fact（ADR 解决前）、Entity、Relation、Evidence 和 Context 必须保持区分。
- 不可变版本不得覆盖；过期写入不得静默获胜。
- 每个派生资产都具有类型化 Provenance，或明确说明不可用原因。
- Scope 不等于 Permission；不允许隐式跨 Scope 合并/读取/引用。
- Evidence 访问授权必须独立于 Memory 访问授权。
- Memory 内容是不可信数据，不能成为 System/Developer 指令或工具授权。
- Context 编辑绝不修改 Canonical 资产。
- Lifecycle State 只有一个权威表示（LifecycleEvent Stream 加确定性派生的当前状态；见 Versioning Contract）。
- 必需目标尚未解决时，Forget 不算完成。

## 10. 接口

**E — Compiler 到 Brain：** Candidate Envelope、Claim 提案、Entity/Relation 提案、Evidence/Provenance 引用、ActorRef、ScopeRefs、来源 Epistemic Status、TimeValues、Idempotency Key 和 Schema Version。输出为已接受的 Canonical ID/Version ID 和 Lifecycle 结果，或 Deferred/Rejected 类型化错误。Compiler 提案；Brain 拥有 Canonical 接受和版本。Fact/Claim Schema 仍受 ADR 阻塞（INT-P0-01）。相同 Key/相同 Canonical Payload 返回相同结果；相同 Key/不同 Payload 属于 Conflict。

**F — Runtime 到 Brain：** 带 Scope 过滤的 Canonical Query/Read，明确指定 Version 或 Current-as-of 语义、请求字段、Evidence/Provenance 展开预算。输出 Canonical 引用、Version ID、Lifecycle/Epistemic/Time 限定，以及符合授权安全要求的 Partial Result 标记。Brain 拥有真相和版本；F 拥有调度/排序/缓存。必须在候选物化之前过滤，并重新检查每条 Graph Edge/Target（INT-P0-02）。

**G — Context Manager 到 Brain：** Memory ID + 准确 MemoryVersion ID（或明确请求的当前指针）、Source Refs、Change Reason 和授权上下文。输出不可变 Canonical 引用和内容句柄；G 拥有 ContextVersion/ChangeSet 及其状态机（INT-P1-01）。Context Entry 不得静默跟随会移动的 Current Pointer。

**H — BMCP/Adapter：** 类型化、不透明的 Memory/Version/Entity/Relation 引用和协议安全摘要；H 拥有 Wire Encoding、Actor Authentication Envelope 以及 Delivery/ACK 协议。Brain 不定义 BMCP Wire 字段。Display Name 不是身份。

**I — Governance：** ActorRef、ScopeRef、TypedObjectRef、Action、Purpose、Policy/Grant Version、Forget Request 和 Retention 义务。I 拥有授权决策、审计策略和物理擦除策略；Brain 提供 Canonical 依赖和状态记录。异步 Worker 在受保护/不可逆阶段之前重新授权（INT-P0-02/03）。

每个接口都返回结构化错误：code、可披露时的 object type/ID、field path、invariant ID、retryability、correlation ID 和安全的修复建议。未授权错误不得泄露对象是否存在。

## 11. 错误处理

稳定错误类别：NOT_FOUND_OR_NOT_VISIBLE；SCOPE_UNRESOLVED；SCOPE_MISMATCH；PERMISSION_DENIED；INVALID_TRANSITION；STALE_VERSION；IDEMPOTENCY_CONFLICT；DUPLICATE_ID；INVALID_REFERENCE；EVIDENCE_UNAVAILABLE；PROVENANCE_INCOMPLETE；CONFLICT_REQUIRES_RECONCILIATION；FORGET_IN_PROGRESS；FORGET_PARTIAL；SCHEMA_UNSUPPORTED；INVARIANT_VIOLATION。错误详情必须最小化，以防止对象存在性泄漏和侧信道泄漏。

## 12. 一致性

Canonical Commit、不可变 Version 可见性、Lifecycle 转换记录和 Outbox/Change-feed Entry 必须原子完成，或具有等价的可恢复语义。Index、Graph Projection、Cache 和 Search Document 都是派生且可重建的。Current Pointer 通过 Compare-and-swap 推进。Change-feed 消费者跟踪单调 Canonical Sequence/Watermark，并拒绝陈旧投影。

## 13. 安全 / Scope

身份必须从已认证 ActorRef 和类型化 ScopeRef 解析，绝不能仅依据模型输出、Display Name、Alias 或 Agent 自报 Label。校验 Owner Scope 和每个 Applicability Scope。跨 Scope 引用需要明确 Grant，并独立检查来源/Evidence。读取结果影响 F 排序、Context 组装、计数或缓存之前必须完成 Scope 过滤。Cache Key 必须包含 Principal、Scope 集合、Environment、Policy/Grant Revision 和 Canonical Version/Watermark。Memory 和 Evidence Payload 都是不可信数据；保留来源身份、Epistemic Status、Trust 元数据、Evidence 引用和 Provenance 血缘（INT-P0-04）。

## 14. 性能考虑

尚未冻结任何延迟或吞吐保证。Graph Traversal 必须按深度、节点数量、扇出和 Deadline 限制，并返回明确的截断/不完整标记。可以批量处理授权和类型化引用校验，但不得削弱逐资源语义。测量 Version Snapshot 大小、Commit 放大、Provenance 遍历、时间查询、冲突检测、Merge/Split 迁移和 Forget 依赖发现。Index 始终是投影。

## 15. 可观测性

携带 correlation_id、causation_id、actor_ref、scope_ref IDs、operation_id、idempotency identity、object/version IDs、schema version、canonical sequence、stage、attempt 和 timestamps。指标包括 Commit 延迟、过期写入率、Outbox 滞后、Projection Watermark 滞后、Lifecycle 转换、Conflict Backlog、Provenance 不完整、Scope 拒绝、Forget 抑制延迟和未解决目标。日志不得复制敏感 Payload。

## 16. 故障场景

- Store Commit 成功但发布失败：通过 Outbox Replay 在逻辑上只发布一次；消费者按 Event ID 去重。
- 并发 Version Writer：一个 CAS 获胜；其他写入收到 STALE_VERSION 并进行协调。
- Index 陈旧或不可用：Canonical Read 仍是权威；明确暴露降级状态。
- Permission Service 不可用：受保护操作 Fail-closed。
- Provenance 来源不可用：保留允许的类型化引用和不可用原因；不得伪造来源文本。
- Merge/Split 投影部分失败：Canonical Migration Record 仍是权威；投影可重建。
- Forget Worker 崩溃：从持久化的逐目标进度恢复；不得过早标记完成。
- 第三方模型已经接收数据：记录边界/例外；不得声称远端已删除。

## 17. 依赖

依赖 B Domain Model 提供 Canonical 语义；依赖 E 提供 Source/Event 和提案契约；依赖 F 提供 Scope-first Query 和 Projection 消费；依赖 G 提供准确 Version 引用；依赖 H 提供已认证 Actor 和 Wire 边界；依赖 I 提供授权、保留和物理擦除策略；依赖 Storage/Recovery 架构提供原子 Commit/Outbox 和备份机制。

## 18. 开放问题

- OPEN：INT-P0-01 ADR 批准及其 Fact/Claim 身份/Schema 结果。
- OPEN：通用 Scope Algebra、多 Owner 和共享所有权（DM-005）。
- OPEN：与 H/I 协调的最终 Principal/ActorRef 认证语义（INT-P1-03）。
- OPEN：TimeValue 不确定时间 Schema 和精度规则（DM-006）。
- OPEN：Consolidated 是持久化状态还是评估检查点。
- OPEN：Retention/Backup 密码学擦除保证和外部来源删除（INT-P0-03、DM-011）。
- TO_VALIDATE：存储布局、Snapshot 策略、Graph 扇出/深度预算和本地 Rust 性能。

## Phase 3 整改 — 权威边界澄清

### Memory Lifecycle 与 Forget Operation

Memory Lifecycle 仅包含 Candidate、Consolidated、Active、Superseded、Archived 和 Forgotten。“Forgetting”不是 Lifecycle State、Status 别名或临时 Lifecycle Transition。ForgetOperation 是独立的持久化工作流，具有自己的操作状态和单调 Fence。即时读取抑制是由活动 Fence 派生的有效可用性规则，不是对 Memory Lifecycle 的修改。满足 I 提供的适用治理标准后，通过独立 LifecycleEvent 将 Memory 转换为 Forgotten。Forgotten 对该内容身份而言是终态；真正的新信息必须获得新身份和 Provenance。

### 类型化排序

规范 Cursor 定义、事务可见性和 Replay 规则见 [commit-cursor-semantics.md](commit-cursor-semantics.md)。每个 MemoryVersion 同时携带其 per-Memory AggregateRevision 和 CanonicalCommitCursor。LifecycleEventCursor、IndexWatermark 和 ForgetFenceCursor 是不同类型。ContextVersion 由 G 拥有；协议/Delivery 标识符由 H 拥有；授权 Epoch 和完成策略由 I 拥有。

### Forget 权威边界

D 对持久化 ForgetOperation 身份、目标引用、抑制 Fence/Generation、Canonical 依赖清单、Producer Registration Barrier、目标进度证据和 Canonical Domain 抑制证明拥有权威。D 不授权操作、不决定 Retention/Backup/外部接收方策略、不证明远端物理擦除，也不宣布全系统 Forget 完成。I 提供治理授权和完成策略。E/F/G/H 拥有各自本地执行与确认机制。详细契约见 [forget-fence-and-completion-contract.md](forget-fence-and-completion-contract.md)。

### Fact/Claim

INT-P0-01 仍为 ADR-BLOCKED：经检查的 main 分支没有已批准的 02-domain-model/adr/ADR-001-fact-claim-canonical-model.md。D 文档中的 Claim、ClaimRevision 和 ConflictSet 字段仍只是说明性 CANDIDATE 描述。本次整改没有冻结任何 Schema、DDL、API 或 Wire 结构。
