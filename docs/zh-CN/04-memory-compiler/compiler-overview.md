---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope: null
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "04-memory-compiler/compiler-overview.md @ 0e966b81179c459842f63fb689698bc1c63fb42a"
        - "OWNER-DECISION-FACT-CLAIM-001, merged PR #446"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-21"
      last_verification_note: "Canonical source restored and bilingual mirror reconciled to the merged Owner semantic decision; concrete schemas remain unfrozen."
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
    canonical_scope: "Memory Compiler design-specification: compiler-overview"
    canonical_scope_id: "memory-compiler/compiler-overview"
    canonical_scope_keywords:
      - candidate-ir
      - canonical-schema
      - fact
      - claim
      - identity
      - lifecycle
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "04-memory-compiler/compiler-overview.md"
    en: "docs/en/04-memory-compiler/compiler-overview.md"
    zh-CN: "docs/zh-CN/04-memory-compiler/compiler-overview.md"
---

# Memory Compiler 总览（记忆编译器）

- 规范源：[compiler-overview.md](../../../04-memory-compiler/compiler-overview.md)
- 规范源 Blob：0e966b81179c459842f63fb689698bc1c63fb42a

- 文档 ID：E-COMPILER-001
- 版本：1.1
- 源分支：session-e-memory-compiler-2026-11-16
- 对应英文：[Memory Compiler Overview](../../en/04-memory-compiler/compiler-overview.md)
- 状态：所有权/安全不变量为 DECIDED；阶段拓扑/编排为 CANDIDATE；模型路由/吞吐/资源预算为 TO_VALIDATE
- Owner：Session E — Memory Compiler
- 基线：截至 2026-11-16 的 A/B/C 架构和领域语义
- 集成依赖：INT-P0-01/02/03/04；INT-P1-02/04/06；AR-004

## 1. 目的

Memory Compiler 将已可靠接收的来源 Event 和登记的来源材料，转换为可追溯的 Candidate Memory/Claim/Entity/Relation 资产；在 Canonical Authority 决策后，再协调 Canonical Commit 和下游 Projection 发布。它是可恢复的语义转换系统，不是简单的 LLM→Vector Database 快捷通道。

Compiler 保证来源身份、Scope、Evidence 链接、派生方法、时间限定、Epistemic Status 和 Idempotency 能够贯穿各个阶段。它不声称已接收输入一定真实，也不保证编译必然产生 Memory。

## 2. 范围

范围内：Event-to-Work 编排、确定性规范化、模型辅助提取、分类、实体解析协作、Evidence/Provenance 创建、巩固、冲突提案、Canonical Write 协调、Retry、Replay，以及 Index/Context Invalidation 通知。

范围外：Canonical Memory Schema 权威和 Lifecycle Policy（D）；Retrieval 调度/排序/Runtime Cache（F）；Context Version 所有权（G）；Agent Adapter/BMCP Wire 权威（H）；全局身份/Permission/Retention Policy（I）；物理 Index 实现。

## 3. 职责

- 消费持久化 Event Ref 和可恢复 Compile Intent。
- 生成具有不可变 Source Ref 和阶段血缘的 Candidate Object。
- 在任何 Source Dereference、Extraction、Entity Matching、Merge 或 Write 之前执行 Scope Filter。
- 使确定性阶段不依赖 LLM 可用性。
- 仅将模型推理用作可选、有界、带版本的转换。
- 与 Entity/Relation Manager 和 Canonical/Lifecycle Authority 协调，但绝不夺取其权威。
- 保留冲突和 Revision；绝不静默覆盖。
- 通过单调 Generation 发布 Canonical Commit 和 Projection Publication Event。

## 4. 非职责

Compiler 不会自行认证不可信 Agent 声明；不决定外部动作权限；不定义 Fact 是否为独立对象；不定义 Canonical Claim Identity/Revision；不决定最终 Lifecycle State；不拥有 Runtime Ranking 或 Context；不保证模型真实；也不承诺超出 I 治理策略范围的物理擦除。

## 5. 输入 / 输出

**输入：** Accepted EventRef、SourceRef/ContentRef、已认证 ActorRef、已解析 ScopeRef 集合、Permission Decision Context、Schema Version、来源时间戳、Idempotency Identity、Retention Class、Source Trust Metadata、Correlation/Causation ID，以及可选 Extraction Policy/Model Profile。

**输出：** Stage Receipt；CandidateEnvelope；Evidence/Provenance Ref；Entity/Relation Proposal；ConflictSet Proposal；CanonicalWriteRequest；CanonicalCommitResult；IndexPublicationRequested；MemoryVersionChanged / ClaimRevisionChanged / ClaimRetracted / MemoryForgotten 通知；结构化可重试/永久错误。

Compilation 可以产生 NO_CANDIDATE、PENDING_EVIDENCE、REVIEW_REQUIRED、DEFERRED 或 REJECTED，而不影响 Accepted 的持久性保证。

## 6. 数据模型

### 6.1 CompilerWorkItem（逻辑候选结构）

~~~text
CompilerWorkItem {
  work_id: OpaqueId
  event_ref: TypedObjectRef
  scope_refs: ScopeRef[]
  actor_ref: ActorRef
  ingress_receipt_ref: TypedObjectRef
  idempotency_scope: IdempotencyScope
  source_digest: Digest
  schema_version: Version
  pipeline_version: Version
  stage: CompilerStage
  state: WorkState
  attempt: u32
  lease_epoch: u64
  authorization_epoch: VersionRef?
  forget_fence_epoch: VersionRef?
  correlation_id: OpaqueId
  causation_id: OpaqueId?
  created_at: Instant
  updated_at: Instant
}
~~~

### 6.2 CandidateEnvelope（CANDIDATE；不是 Canonical Schema）

~~~text
CandidateEnvelope {
  candidate_id: OpaqueId
  source_event_refs: TypedObjectRef[]
  scope_refs: ScopeRef[]
  environment_scope_ref: ScopeRef?
  modality: SourceModality
  propositions: CandidateProposition[]
  entity_mentions: EntityMention[]
  relation_proposals: RelationProposal[]
  evidence_drafts: EvidenceDraft[]
  provenance_draft: ProvenanceDraft
  temporal_qualifications: TimeQualification[]
  source_epistemic_basis: EpistemicBasis
  extraction_method: MethodRef
  uncertainty: UncertaintyRecord[]
  unresolved_questions: String[]
  schema_status: "candidate-unfrozen"
}
~~~

CandidateProposition 有意不预先决定 Fact/Claim 对象身份。它记录命题结构、Modality、Polarity、Subject/Object 假设、Evidence 指针、来源 Epistemic Basis 和限定条件。映射到 D 获批的 Claim/Fact ADR 属于独立 Adapter 层。INT-P0-01 解决前不冻结任何 Canonical Output Schema。

### 6.3 Stage Receipt

每个阶段记录 Input/Output Digest 或引用、Stage Version、确定性/模型辅助模式、Actor/Method、开始/完成时间、Attempt、Authorization/Fence Epoch，以及终态/可重试结果。普通日志不得复制原始来源 Payload。

## 7. Pipeline / 状态机

~~~mermaid
flowchart TD
 A[Source Event / Document / Telemetry] --> B[Durable Ingress + Receipt]
 B --> C[Scope & Permission Recheck]
 C --> D[Deterministic Normalize / Classify]
 D --> E[Extract Candidates]
 E --> F[Entity Resolution Collaboration]
 F --> G[Evidence Creation]
 G --> H[Provenance Construction]
 H --> I[Candidate Memory]
 I --> J[Consolidation / Duplicate Detection]
 J --> K[Conflict Detection / Revision Proposal]
 K --> L[Canonical Write Contract]
 L --> M{D / Lifecycle decision}
 M -->|commit| N[Canonical Commit + Outbox]
 M -->|defer/review| O[Persist Candidate / Review State]
 M -->|reject| P[Reasoned Rejection]
 N --> Q[Index Publication Event]
~~~

| 阶段 | 默认执行方式 | 模型使用 |
|---|---|---|
| Envelope 校验、Digest、Idempotency、Scope 绑定 | 确定性 | 不要求模型 |
| 文本解码、结构解析、时间戳保留 | 确定性 | 仅可选辅助解析 |
| Modality/Event 分类 | 规则优先；不确定项进入队列 | 可选 Classifier |
| Entity/Relation Mention 提取 | 混合 | 可选模型 |
| Candidate Proposition 提取 | 混合 | 可选模型 |
| Evidence Locator 校验/Digest | 确定性 | 模型可以建议 Span，Validator 必须核验 |
| Provenance 构建 | 根据 Stage Receipt 确定性生成 | 模型不得编造血缘 |
| Scope 兼容性/授权 | 确定性策略执行 | 绝不委托模型 |
| Dedup/Conflict Candidate 生成 | 确定性过滤 + 可选语义相似度 | 模型可提案，不裁决 |
| Canonical Commit | 由 D/Lifecycle 拥有的事务 | 绝不委托模型 |

Work State：RECEIVED → READY → LEASED → STAGE_RUNNING → STAGE_COMMITTED → READY(next stage) → PROPOSAL_READY → CANONICAL_PENDING → COMMITTED / DEFERRED / REJECTED / DEAD_LETTER。Lease 不是 Canonical Transaction Lock。每个阶段必须先提交幂等结果，再推进持久化 Cursor。

## 8. 不变量

1. Accepted Event 的持久性不依赖 Compiler/LLM 是否可用。
2. Event、Evidence、Candidate Proposition、Memory 和 Claim 不是同义对象。
3. 任何阶段都不得在授权 Scope 外读取或关联数据。
4. 每个派生命题都必须链接来源 Evidence/Provenance，或明确说明不可用原因。
5. 没有 Outcome Evidence 时，Plan/Intent/Prediction/Pending/Attempted 不得成为已完成结果。
6. 来源内容是不可信数据，不能改变工具权限、系统策略或 Compiler 配置。
7. 模型输出是不可信提案，永远不是 Permission 或 Canonical Decision。
8. Canonical Write 使用 Expected Version 和 D 批准的语义。
9. 冲突必须明确保留；禁止语义层面的 Last-write-wins 覆盖。
10. Index 是派生数据；Canonical Commit 和 Index Visibility 是不同阶段。

## 9. 幂等性

每个 Stage Key 由稳定 Work Identity + Stage Name/Version + Input Digest + Scope Identity 派生。相同 Key/相同 Input 返回先前 Stage Receipt。相同 Key/不同 Input 属于 Integrity Conflict。模型阶段持久化准确的 Model/Provider/Profile/Prompt Template Version 和规范化 Output Digest；非确定性重执行创建新的 Attempt/Revision，不覆盖旧结果。Canonical Commit 使用 D 的 Idempotency/Expected Version 契约。

## 10. 一致性

Event Log 和 Compile Intent/Outbox 在 Ingress 时原子提交。Stage Output 和下一阶段调度使用原子 Stage-result/Outbox 边界或等价可恢复 Journal。Candidate Record 不是 Canonical。D 拥有 Canonical Version/Current Pointer 原子性。Canonical Commit Notification 通过事务性 Outbox 发布；Index Worker 只有在应用对应 Canonical Generation 后才发布 Watermark。

## 11. 故障恢复

- 重启后从最后一个已提交 Stage Receipt 恢复。
- 模型不可用时 Work 保持 Pending；可行的确定性阶段继续执行。
- 无效/不支持输入按原因隔离；已接收原始 Event 仍按 Retention 保留。
- 多次永久失败进入 DLQ；操作员 Replay 创建新 Attempt，同时保留旧 Receipt。
- Canonical Conflict 触发 Reload/Reconcile，绝不盲目覆盖。
- Replay 时来源缺失，标记 Unavailable；不得伪造摘录。
- Forget Fence 必须在后续受保护读写前使排队/已租用 Work 失效。

## 12. 安全 / Scope

在 Ingress、每次 Worker Lease、每次 Source Dereference、Entity Candidate Search、Consolidation Set 构建、Canonical Write 和 Replay 时解析并授权 Scope。过滤必须先于 Candidate Generation、Ranking、Aggregation 和 Graph Expansion。Evidence 具有独立读取授权。异步 Worker 重新检查当前 Principal、Permission Version、Revocation/Forget Fence 和 Target Scope。Cache Key 绑定 Scope、Environment、Actor Class、Policy/Revocation Epoch 和 Source Version。不得信任模型生成的 Scope。

## 13. 性能 / 背压

**CANDIDATE：** 为关键结果、普通交互事件、批量导入和低优先级遥测建立逻辑独立队列/通道。在模块化单体中，它们可以共享物理存储。对 Payload 大小、Queue Bytes、并发模型任务、Entity Fanout、Graph Depth、Retry Count 和 Per-Scope Quota 设上限。

过载时：若不能保证持久化容量，必须在 Accepted 前拒绝；Accepted 之后必须保留持久化 Work，并延迟低优先级编译；只允许合并明确声明为可替换的遥测，不得伪造完整历史。数值预算必须在声明硬件/工作负载下 TO_VALIDATE。

## 14. 可观测性

跟踪 Acceptance Latency、Backlog Bytes/Age、各 Stage Latency、确定性/模型辅助比例、模型队列等待、Retry/DLQ Rate、Canonical Commit Lag、Index Watermark Lag、Scope Denial 数量、Forget Fence Cancel 数量、Candidate-to-Commit 转化率、无依据 Claim Rate 和 Provenance Coverage。Trace 从 Ingress 贯穿 Canonical/Index Event。指标标签不得包含原始 Prompt、Source Payload、凭据或敏感摘录。

## 15. 接口

- **H / BMCP → E：** 已校验 Ingress Envelope 和 Accepted Receipt；E 消费已认证 ActorRef/已解析 Scope，但不定义 Wire Name。
- **D ← E：** Candidate Memory / Canonical Write / Conflict 和 Revision Proposal；D 拥有 Canonical Schema 和决策。
- **F ← E/D：** 带 Generation、类型化 Ref、变更对象类别和 Scope 的 Canonical Commit/Index Publication Event。
- **G ← D/E：** MemoryVersion Changed、Claim Retracted/Superseded、Lifecycle Changed、Forget Suppression Event。
- **I ↔ E：** 授权复查、Forget Fence、Retention Class、删除依赖登记、审计安全 Tombstone。
- **Consistency/Storage：** Outbox、Replay Cursor、Canonical Generation、Index Watermark、Backup 和 Recovery 契约。

所有跨模块消息都携带 Schema Version、Actor/Scope Context、Correlation/Causation；状态变更操作还要携带 Idempotency，并明确错误/重试语义。

## 16. 测试场景

Accepted 前/后 LLM 故障；Event+Outbox Commit 后崩溃；重复 Stage Dispatch；相同 Key/不同 Digest；仅含 Plan 的输入；跨 Scope Entity Match；Queue 后执行前 Permission 被撤销；Lease 期间发生 Forget；Index 故障期间 Canonical Commit；Source 过期后的 Replay；包含工具/策略指令的恶意文档。

## 17. 依赖

A/B/C 基线；D Canonical Memory/Lifecycle 契约；H Producer Identity/Ingress Envelope；I Permission、Retention、Forget 和 Revocation Epoch；F Projection 要求；G Context Invalidation 语义；Storage/Consistency Outbox/Recovery；有界模型推理调度器。

## 18. 开放问题

- RESOLVED：Fact/Claim 语义及 I1 身份/修订选择已由 OWNER-DECISION-FACT-CLAIM-001（PR #446 已合并）采纳。
- OPEN：D 的 Canonical ClaimRevision/ConflictSet 字段 Schema、Lifecycle Contract 和 Consumer Pins；语义身份/修订模型已决定，但具体 Schema 未冻结。
- OPEN：INT-P1-06 Provenance Cycle Policy 和 Lifecycle Authority Event。
- CANDIDATE：Queue Lane、Model Routing、Deterministic-first 阈值、Stage Journal。
- TO_VALIDATE：12–16 GB VRAM 本地模型辅助提取质量/成本、吞吐和积压恢复。
- OPEN：Ingress Idempotency Receipt 和 Replay Metadata 的精确保留期限，与 I 协同。

## 19. Phase 3 可靠接收与 Forget 集成补充

- Pipeline 消费 E 持久化 Accepted Receipt 和 Compile Intent Record。Accepted 仅代表数据接管/持久化，不等于 Processed、Compiled、CanonicalCommitted 或 Indexed。模型故障和传输响应丢失后 Receipt/Idempotency 仍然保留。
- Stage Result 和下一阶段 Intent 必须通过原子 Stage-result/Outbox 边界或等价可恢复 Journal 持久化。每次 Replay/Recompile 都是基于不可变 Event Identity 的新 Attempt，并根据 I 当前 Permission Epoch 和 D Forget Fence 重新授权。
- CompilerWorkItem Lease 中的 authorization_epoch 和 forget_fence_epoch 是 Owner 签发的不透明 Token。E 不得创建、数值比较，或将它们替代为 Source Event Cursor、D Canonical Commit Cursor、F Index Watermark 或 ContextVersion。
- E 必须在输出可见前登记每个在途 Producer/Run 和每个派生依赖。D/I 权威 Barrier/Publication Gate 必须将 Registration 与 Forget 串行化；本地预检查不足以关闭 Check-then-publish 竞争窗口。
- H BMCP Envelope 和 I Principal/ActorRef 契约是候选依赖。H 传输 Owner 定义的 Idempotency Namespace/Key/Digest；I 定义已认证 Producer Binding、安全域身份、PermissionEpoch 和 Policy。
- Owner 已批准 Fact/Claim 语义为 Option A + I1。精确 E-to-D/I Canonical Mapping 仍为 Candidate；CandidateEnvelope/CandidateProposition 继续保持 Pre-canonical IR。
- 详细 CANDIDATE 契约见 accepted-receipt-and-idempotency-contract.md 和 forget-fence-and-derived-registration-part1.md。

## 20. 架构阶段补充——Candidate IR 与 Canonical Schema 边界

**状态：** E 所有的架构契约扩展 / PROPOSED。本节采用 OWNER-DECISION-FACT-CLAIM-001 已批准的语义和身份选择；不冻结跨 Owner Schema，也不授权 Runtime 实施。

### 20.1 Candidate IR 不等于 Canonical Record

Candidate IR 是 Compiler 自有、带版本的中间表示，用于记录从已接收来源提取了什么，以及该提取如何派生。它是私有、暂定、带 Provenance 且不具权威性的表示。CandidateEnvelope、ExtractionIR 和 CandidateProposition 是该 Pre-canonical 表示在不同阶段的相关视图，不是 Canonical Memory、Claim、Fact、Entity 或 Relation Record 的别名。

输入边界是已可靠接收的来源包：不可变 EventRef/SourceRef/ContentRef、精确 Source Digest、Accepted Receipt 和 Compile Intent 引用、由所属 Ingress/Security 契约提供的可信 ActorRef/ScopeRefs、来源元数据，以及固定版本的 Extraction/Pipeline Policy。缺少 Source Identity、Digest 和可信 Scope Context 的任意字符串，不足以构成权威 Compile 操作的输入。

Candidate IR 必须直接保留或通过不可变引用保留：

- 原始 Source Identity、精确 Digest、Source Schema/Content Type、Locale 和 Source Time Metadata；Source Bytes 保留在受治理的来源位置，不得复制进普通日志。
- 绑定到精确不可变来源表示的 Source Span/Locator；当偏移量依赖 Encoding/Normalization Version 时，必须同时绑定这些版本。
- 原始 Surface Text/Value 与规范化 Hypothesis 分开保存；Normalization 不得覆盖来源表示。
- Modality、Polarity、Source Epistemic Basis、Temporal Qualification、Scope 和 Environment Qualification。
- Entity Mention、Relation Hypothesis（不得分配 Canonical Identity）、Proposition 的 Subject/Predicate/Object Hypothesis 和 Qualifier。
- Evidence/Provenance 引用或草稿、Extraction Method/Profile/Version、Stage Receipt、Uncertainty、Ambiguity、Unresolved Field，以及明确的 Unsupported/Unavailable 原因。
- 在安全可保留时保留非语义来源元数据和未知扩展内容。如果输入字段无法表示或安全保留，Compilation 必须将其报告为 Unsupported/Unresolved 或隔离 Candidate；不得静默丢弃。

Candidate-local ID 只标识 Candidate/Stage 工件，不得伪装成 D 签发的 Canonical ID，也不得复用为 Canonical Identity。

### 20.2 Candidate 校验不变量

Validation 不能被简化为非空检查。Candidate 只有满足以下条件才在结构上有效：

1. 必需的 Source、Digest、Schema/Pipeline Version 和可信 Scope 引用存在且类型正确。
2. 每个 Source、Evidence、Provenance 和 Stage Receipt 引用都能解析到预期的精确不可变版本，或携带明确的 Unavailable 原因。
3. 每个 Source Span 均位于精确 Source Bytes/Segment 边界内，并绑定 Source Digest、Encoding 和 Normalization Profile。
4. Candidate-local ID 在声明的 Namespace 内唯一；Typed Reference 和 Relation Endpoint 的类型兼容。
5. Modality、Polarity、Epistemic Basis、Time Precision/Zone、Confidence/Uncertainty 和 Optional Value 使用声明的类型及有效范围；Unknown 必须显式表达，不得伪造默认值。
6. Scope/Environment Metadata 来自可信 Ingress/Security Context，而非 Source Text 或 Model Output。
7. Provenance 将每个派生命题关联到 Source Evidence，或明确记录缺失 Evidence 的原因；Model Output 不得编造 Lineage。
8. Original Value、Normalized Value、Qualifier、Metadata、Uncertainty 和 Unresolved Content 必须可恢复。
9. 任何 Candidate State 都不得暗示 CanonicalCommitted、Published、Indexed、Verified、Authorized 或 Forget-complete。

Validation Report 必须通过稳定 Error Code 和 Field/Path/Reference 定位每项失败，并区分 Invalid、Incomplete、Unsupported、Stale-authority 和 Transient-unavailability。部分提取只有在每个已输出字段独立满足不变量时，才能产生 PARTIAL/REVIEW_REQUIRED Candidate；无效字段不得静默省略。

### 20.3 Candidate 生命周期与错误

Candidate 工件和 Stage Receipt 按逻辑 Attempt 追加保存。同一 Work 和相同 Input Digest 的 Retry 必须幂等；Source Bytes、Policy、Parser/Model Profile 或 Schema Version 改变时，创建带明确 Lineage 的新 Attempt/Revision。Recompile 不得修改早先 Candidate，也不得重置 Root Producer-work Identity。

Compiler 可以返回有原因的结果，例如 NO_CANDIDATE、PARTIAL、REVIEW_REQUIRED、DEFERRED、REJECTED 或 QUARANTINED。这些是 Compiler Outcome，不是 D Lifecycle State。Candidate Retention、受保护内容访问和删除受 I Policy 及适用的 D/I Forget Fence 约束；Lease 过期、Timeout、Receipt 缺失或 Authority 状态未知，均不代表成功或终态证明。

错误类别包括：EMPTY_INPUT；MALFORMED_SOURCE；UNSUPPORTED_CONTENT_TYPE/SCHEMA_VERSION；MISSING_REQUIRED_FIELD；DIGEST_OR_SPAN_MISMATCH；INVALID_TYPED_REFERENCE；SCOPE_MISMATCH；AMBIGUOUS_OR_UNRESOLVED；MISSING_EVIDENCE_OR_PROVENANCE；IDEMPOTENCY_CONFLICT；STALE_PERMISSION_EPOCH；FORGET_FENCE_BLOCKED；CANONICAL_VERSION_CONFLICT；ADR_MAPPING_BLOCKED；SERIALIZATION_PROFILE_UNSUPPORTED；RETRYABLE_DEPENDENCY_UNAVAILABLE。错误详情不得向无权调用者泄露受保护内容或对象是否存在。

## 21. Canonical Schema 边界与权威归属

Canonical Schema 由已批准的领域模型和相应领域 Owner 契约定义，而不是由 Candidate IR 字段名、E 的提案、Storage Adapter 或 Serializer 定义。相关来源契约包括 D 的 Canonical Memory Store 和 Memory Versioning、B 的 Fact/Claim 决策记录、I 的 Authorization/Retention/Forget Policy，以及 H 独立拥有的 Wire Serialization 规则。

权威分工如下：

| 事项 | 权威归属 | Compiler 约束 |
|---|---|---|
| Canonical Memory/Claim/Fact/Entity/Relation Identity 分配及 Canonical Version/Lifecycle | D，且受已批准领域语义约束 | E 只提交 Proposal 并消费 D 签发的引用/结果；不得创建、重写或替代 Canonical ID |
| Canonical Commit、Expected-version Check、Lifecycle Transition 和 Canonical Cursor | D | E 通过 D 所有的契约提交请求；不得直接写 Canonical Store |
| Forget Fence 语义、Producer Barrier、Lineage Inventory 和最终 Canonical Publication 顺序 | D，与 I 和 Storage 协同 | E 提供完整 Source/Derivative Lineage 并遵守权威 Gate；本地预检查不构成发布授权 |
| Authentication、Authorization、PermissionEpoch、Revocation、Retention 和 Global Forget Policy/Completion | I | E 消费 Owner 签发的当前授权 Context/Receipt；不得创建、替代性比较或覆盖 PermissionEpoch |
| H Wire Envelope 和外部协议序列化 | H | E 内部 Candidate Serialization 不是 Wire Contract |
| 持久化物理事务/可见性实现 | Storage/Consistency，依其责任 Owner 契约 | E 不得从本地 Receipt 或 Queue ACK 声称原子性或可见性 |

Compiler 权限：E 可以在获准范围内持久化自有 Accepted-work Bookkeeping、Candidate Artifact、Stage Receipt 和私有 Staging Output。E 可以提交 CanonicalWriteRequest 并记录 D 的权威响应。E 不得直接写入或覆盖 Canonical Schema、分配 Canonical Identity、选择最终 Lifecycle、伪造 CanonicalCommitCursor、创建 PermissionEpoch/ForgetFence Token，或在 D/I/Storage Publication Gate 满足前暴露派生工件。

OWNER-DECISION-FACT-CLAIM-001 选择 Option A + I1：Claim 是稳定命题线程，具有不可变 ClaimRevision；Fact 是独立受治理的 Attestation，具有不可变 FactRevision 并绑定精确 ClaimRevisionRef。该决策解决语义和身份选择，但不冻结字段级 Schema、DDL、Public API、H Wire Field、D ConflictSet Shape 或 Storage Layout。CandidateProposition/CandidateEnvelope 继续保持中立 Pre-canonical IR。Canonical Mapping 仍须等待 D 的 Schema/Lifecycle Contract、I 的 Authorization/Attestor Policy、H 的 Wire Contract 和 Consumer Acceptance 完成版本 Pin；禁止启发式映射。

## 22. Fact/Claim 映射——Owner 语义决策已采纳，Schema 边界仍开放

Fact 和 Claim 在 Candidate Model 中必须保持语义区分：

- **Claim Candidate：**来源提出、报告、推断、争议或撤回的命题，不保证为真。Subject/Predicate/Object Hypothesis、Polarity、Modality、Qualifier、Scope、Time、Epistemic Basis 和 Evidence Lineage 必须显式保留。
- **Fact/Attestation Candidate：**对精确 Proposition/Revision 可能作出的裁定/证明，候选引用包括 Attestor、Method/Version、Evidence、Scope、Validity 和 Decision History。这只是概念候选；E 不定义或实例化 Canonical Fact Identity/Lifecycle。
- **CandidateProposition：**中立的 Extraction IR。Owner 决策已选择独立、具有 Identity 的 Fact Attestation 与 Claim Proposition；E 仍不得签发 Canonical Identity 或实例化 Canonical Fact。

必须按状态层次读取当前来源，不能将其压平。Owner 决策 OWNER-DECISION-FACT-CLAIM-001 已在 PR #446 合并（merge commit ad5ca81a32b413aef3f9b5bccd06030aabde8275），选择 Option A + I1。该决策取代 B ADR 对语义问题的未决结论；旧 B ADR 保留为历史证据。本决策不批准字段级 Schema、DDL、Public API、Wire Payload 或 Runtime Mapping。精确消费者实现映射、迁移/兼容和符合性仍为 Candidate，直至责任工件完成版本 Pin 和审查。D Memory Versioning §17/Claim Freeze Gate 继续要求先对账消费者契约，再冻结具体 ClaimRevision/ConflictSet Schema 和字段。历史 PR #194 曾将 Claim Identity 恢复为 OPEN；之后 AID-2026-014 Commit 记录了 Convergence，同时保留实现验收/Schema Gate。E 必须保留这一差异，不得推断 Schema 已获批准。

候选方案：

| 方案 | 含义 | 对 D 的影响 | 对 I 的影响 | 状态 |
|---|---|---|---|---|
| A — 独立 Fact Attestation Object | Fact 拥有独立 Canonical Identity/Revision，并绑定精确 ClaimRevisionRef、授权 Attestor、Method、Evidence、Scope 和 Validity | 需要 D 定义 Fact 与 Claim Revision 的 Identity、Lifecycle、Versioning、Reference Integrity 和 Forget Dependency 规则 | 需要 I 批准 Attestor Authorization、PermissionEpoch 复核、Evidence Access/Retention 和 Global Forget Policy | **Owner 已批准语义方向（PR #446）；精确 Mapping 仍为 Candidate** |
| B — Fact 是精确 ClaimRevision 的限定 View | 不创建独立 Fact Identity；View/Qualification 从精确 Claim Revision 和声明的 Predicate 派生 | Identity/Storage 复杂度较低，但 D 必须定义 View 的精确 Revision 和 Lifecycle 语义 | I 仍管理 Authorization、Policy 和 Evidence Retention；View 不得暗示 Permission 或 Truth | 未选择；仅可由后续替代 Owner 决策重新打开 |
| N — 保持中立 Pre-canonical Mapping | 将 CandidateProposition 和 Attestation Evidence 保留为 Candidate-only Reference；暂不映射 Canonical Fact/Claim | 决策前不创建新的 D Identity 或 Lifecycle | 不推断 Attestation Authority；来源访问仍受 I 当前控制 | **D/I/H 消费者与 Schema 门禁关闭前 E 必须采用** |

E 不负责选择领域语义。Owner 已批准 Option A + I1 作为语义方向。因此，在责任 D/I/H 消费者契约、迁移/兼容和符合性证据完成版本 Pin 并经审查前，E 必须继续输出中立 CandidateProposition，不得执行 Canonical Fact/Claim Mapping。文本相似度、Extraction Confidence 或模型“Fact”标签永远不能授予 Canonical Identity 或 Attestation Authority。

### 22.1 正式 Owner 裁决请求

- **DECISION_REQUEST_ID：**MC-ADR-FACT-CLAIM-001
- **MODULE：**Memory Compiler
- **ISSUE_OR_ADR：**B-ADR-FACT-CLAIM-001；INT-P0-01；来源：13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/fact-claim-identity-adr.md
- **DECISION_REQUIRED：**使 B-ADR-FACT-CLAIM-001 与 Owner 选择的 Option A + I1 语义方向对齐；完成 B/D/E/F/G/H/I 消费者映射与验收；定义 Identity 改变和仅 Revision 改变的条件，以及 Candidate 到 Canonical Boundary 的规则。精确 Schema 批准仍是独立后续门禁。
- **CURRENT_FACTS：**CandidateProposition 仍是中立 Pre-canonical IR。Owner 语义决策 `OWNER-DECISION-FACT-CLAIM-001` 已批准并合并（main Blob `d59756a8eb454480804c482ca03c68345ab5abf2`；PR #446 merge commit `ad5ca81a32b413aef3f9b5bccd06030aabde8275`）。B ADR 已被取代为当前语义决策请求并保留为历史证据。完整 Fact/Claim Schema、DDL、Public API 和 Wire Contract 均未获批准；精确消费者映射仍为 Candidate，等待版本 Pin 和审查。
- **CONFLICTING_CONTRACTS：**历史 B-ADR-FACT-CLAIM-001 建议/状态；D Memory Versioning 的消费者契约/Schema Freeze Gate；Domain Model 已批准的 DECIDED 语义；E Extraction and Normalization 映射；历史 PR #194 的 OPEN 更正及之后被 AID-2026-014 Convergence Commit 替代的记录。
- **OPTIONS：**A + I1 已被选为语义方向；在 B ADR §8 消费者/Schema 门禁关闭前，E 仍必须在 Pre-canonical Boundary 采用 N。只有后续替代 Owner 决策才能重新打开 B 方案。
- **RECOMMENDED_OPTION：**保留中立 CandidateProposition 并推迟 Canonical Mapping；不得将语义选择视为已批准 Schema。
- **IMPACT_ON_D：**任何获批 Canonical ID、不可变 Revision、Lifecycle Transition、Expected-version Commit、Reference Integrity 和 Forget Dependency Closure 均必须由 D 拥有。E 生成的 Identity 不可接受。
- **IMPACT_ON_I：**I 必须定义/接受 Attestor Authorization、当前 PermissionEpoch/Revocation Check、Source/Evidence Access、Sensitivity/Retention 和 Global Policy 影响。E 不得创建或豁免 Authorization。
- **FORGET_FENCE_IMPACT：**任何选定的 Fact/Claim Object 及其全部 Evidence/Provenance Derivative 必须纳入 D 的权威 Producer/Dependency Inventory 和 D/I Fence/Publication 顺序。Fence 状态未知或过期时阻止发布；不得发生 Fence 后派生内容可见或复活。
- **RUNTIME_IMPLEMENTATION_IMPACT：**Mapping Code、Canonical Fact/Claim Serialization、Schema/DDL、跨模块 Wire Field 和 Mapping Conformance Test 继续阻塞。Runtime 只有在独立 Engineering-phase Entry Authorization 和 Owner Contract 获批后，才能实现中立 Candidate IR 行为。
- **REQUIRED_AUTHORITY：**Owner 语义选择已在合并的 PR #446 获批；在 Canonical Mapping 或 Schema 冻结前，B/D/E/F/G/H/I 消费者工件仍须完成版本 Pin 和审查；A 更新 Integration Registry 和 Consumer Pin；Storage、H 分别负责 Persistence 与 Wire Contract。
- **OWNER_DECISION：**SEMANTIC_DIRECTION_SELECTED_OPTION_A_I1；CROSS_OWNER_SCHEMA_ACCEPTANCE_PENDING
- **EVIDENCE：**Owner Decision `OWNER-DECISION-FACT-CLAIM-001` main Blob `d59756a8eb454480804c482ca03c68345ab5abf2`；PR #446 merge `ad5ca81a32b413aef3f9b5bccd06030aabde8275`；当前 main `c138654c942dc93b5a36eccb2ff0e41452156429`；历史 B-ADR-FACT-CLAIM-001；docs/en/03-memory-brain/memory-versioning.md §17/Claim Freeze Gate；02-domain-model/domain-model-overview.md §§10–13；已合并 PR #194 及其后续 AID-2026-014 替代 Commit；docs/en/04-memory-compiler/extraction-and-normalization.md；Issue #7 Defer 记录。
- **FOLLOW_UP_ACTIONS：**B 对账 ADR 状态/来源 Pin；D 发布精确 Canonical Identity/Lifecycle Mapping；I 记录 Attestor Authorization/Retention/Forget Acceptance；F/G/H 记录精确消费者映射与兼容性；Storage 发布 Persistence Acceptance；A 更新 Integration Registry/Pins；E 在全部证据存在前保持中立 Candidate IR；精确决策 Pin 完成前，被阻塞测试保持阻塞。

## 23. 端到端 Compiler 生命周期与数据流

| 阶段 | 输入 → 输出 | Owner | 前置条件与权威 | 失败/重试与数据状态 |
|---|---|---|---|---|
| Raw Source / Durable Ingress | Source Bytes 或引用 + Metadata → 不可变 EventRef、Accepted Receipt、Compile Intent | H/I 负责已认证 Envelope 和 Policy；E 负责 E 自有 Ingress 语义；Durable Store 负责接管 | 已认证 Producer、Resolved Scope、Idempotency 和 Durable Acceptance | Accepted 前：拒绝且不得声称接管。Accepted 后：保留 Durable Source/Work；按稳定 Identity Retry |
| Candidate IR | Accepted Source Bundle → ExtractionIR/CandidateEnvelope 和 Stage Receipt | E | Source Digest/Version、当前 Access Context、固定 Parser/Policy；不创建 Canonical Identity | Partial/Unresolved 必须显式表达；相同 Digest 幂等重试；输入/Method 改变则新建 Attempt |
| Validation | Candidate + Trusted Validation Context → Field-addressed ValidationReport | E，消费 D/I 引用 | Structural/Provenance/Scope 检查；受保护读取或边界检查时，必须检查 I 当前 Permission 和 D Fence | Invalid 在修正前为永久失败；Authority/Fence 过期时 Fail-closed；临时依赖不可用可重试 |
| Mapping Decision | 有效中立 Candidate → 获批 Mapping Instruction 或 ADR_MAPPING_BLOCKED | B 决定语义；D 接受 Canonical Mapping；I 约束授权；E 负责适配 | 精确获批 ADR 和已 Pin 的 D/I Consumer Contract | ADR 阻塞在决策改变前不可重试；不得启发式映射 |
| Canonical Schema Boundary | CanonicalWriteRequest → D 签发 Canonical ID/Revision/Commit Result，或有原因的 Defer/Reject | D；I/Storage 在各自边界参与 | D Expected-version/Lifecycle 规则；I 当前 PermissionEpoch；D/I Forget Fence；完整 Dependency 和 Storage Visibility Protocol | 显式返回 Conflict/Defer/Reject；结果未知时用稳定 Operation Key 查询；E 不伪造成功 |
| Candidate Serialization | 有效 Candidate IR + 固定 Profile → 确定性 Candidate Bytes + Digest | E 负责内部 Candidate Format；H 负责 Wire；D/Storage 负责 Canonical Persistence Format | 有版本的 Profile 和无损可表示性；Canonical Schema 仍由独立权威管理 | 不支持的 Profile/Field 显式失败；相同输入/Profile 得到相同 Bytes；往返保留语义内容 |

Pipeline 摘要：Raw Memory/Source → Durable Accepted Boundary → Candidate IR → Structural/Provenance Validation → Mapping Decision → D-owned Canonical Schema Boundary → 独立治理的 Serialization/Persistence。Mapping 阻塞时可以作为有效私有 Candidate 结果结束；不得通过回退路径自动提升。

## 24. 未来 Runtime 的语言无关接口契约

以下内容是语义契约，不是 Rust Signature、冻结的 API Schema 或实施授权。

### 当前 Workspace Rust 参考流水线——main 回读

当前 Workspace 确实包含 `crates/memory-compiler/src/lib.rs`（main `f23906dc75256a6ffb90051a6c0888d0dd247e62`，Blob `7476835ca770c1522b4b405f7c74e517eab894e5`，614 行）。模块头明确说明它是纯 Rust 参考流水线，没有 Database、Network、Model Provider 或 Authorization 实现；生产权威集成仅定义为 Trait，尚未实现。

- `MemoryCompiler<A>::compile()` 已存在，并组合 Ingestion、Extraction、Normalization、Staging 和 PublicationGate。
- 当前源码没有公开的 `MemoryCompiler::validate()` 或 `MemoryCompiler::serialize()`。下文的 `validate` / `serialize` 是目标语义契约，不是当前可调用 API。
- `PublicationAuthority` 是注入式 Trait；该 Crate 没有生产 D/Storage/I 权威实现。
- `lib.rs` 内有 11 个 Rust 单元测试。`cargo test -p memory-compiler` 在本地 Checkout `7a926e57091a1b11277fa936cb75a6f215712164` 上通过 11/11；`crates/memory-compiler` 与所引用 main 提交内容完全一致。这些测试只覆盖参考流水线，不满足完整 MC-AT 矩阵。
- 原派发中的旧路径 `src/memory/compiler.rs` 和 `tests/compiler_test.rs` 不存在；当前 Workspace 实际路径是上述 Crate。

这是实际参考代码和测试证据，不是生产集成，也不授权扩展 Runtime 行为。

### compile

- **输入：**AcceptedSourceBundle，包含不可变 Source/Event/Content Reference、Digest、Accepted Receipt 和 Compile Intent Reference、可信 ActorRef/ScopeRefs、Source Metadata，以及固定版本的 Compile Policy/Profile。
- **输出：**CompileResult，包含 Candidate Reference、Stage Receipt、明确的完整性/结果状态和字段定位诊断；不暗示 Canonical Record。
- **错误：**Malformed/Empty/Unsupported Input、Missing Source、Scope Denial、Stale PermissionEpoch、Forget Fence Block、Idempotency Conflict、Unresolved Ambiguity、Missing Evidence、ADR Mapping Block 和 Retryable Dependency Failure。
- **不变量：**相同稳定 Work Identity + 相同 Digest/Profile 必须幂等；Digest/Profile 改变则创建新 Attempt/Revision；不得静默丢弃有效来源信息；Accepted 不等于 Compiled 或 CanonicalCommitted。
- **副作用：**可以创建 E 所有的 Work/Stage/Candidate Record 和私有 Staging Artifact；不得直接写 Canonical Record 或暴露 Derivative。
- **权限/幂等：**使用 Owner 签发的当前 Authorization/Fence Evidence；稳定 Producer-work Identity 跨 Retry/Replay 保持；发布由 D/I/Storage Gate 管辖。
- **依赖模块：**H Ingress Identity/Envelope；I Authorization/PermissionEpoch；D Producer Registration、Canonical Identity/Lifecycle 和 Forget Fence；Storage Durability/Visibility；B Fact/Claim ADR。

### validate

- **输入：**CandidateEnvelope/ExtractionIR、精确 Source/Evidence Reference，以及在受保护读取或边界检查时携带不透明 Owner 当前 Authorization/Fence Evidence 的 Validation Context。
- **输出：**ValidationReport，Disposition 为 VALID、PARTIAL、INVALID、UNSUPPORTED、STALE_AUTHORITY 或 BLOCKED_BY_ARCHITECTURE_DECISION，并为每项 Finding 提供稳定 Error Code + Field/Path/Reference。
- **错误：**Required Field/Type/Range Violation、Digest/Span Mismatch、Unresolved Required Reference、Scope Mismatch、Missing Provenance、Invalid Modality/Time/Metadata、Stale Permission/Fence、Identity/Lifecycle Conflict 和 ADR Block。
- **不变量：**Validation 不得提升 Epistemic Status、Canonical Lifecycle、Identity、Permission 或 Truth；它校验 Candidate Semantics，并报告外部权威结果，不得自行签发。
- **副作用：**不得执行 Canonical Mutation、Permission Grant、Fence Update 或删除 Candidate Field；任何 Diagnostic/Audit Write 都必须独立标识并具备幂等性。
- **权限/幂等：**相同 Candidate 和相同 Authority Snapshot 的重复 Validation 结果稳定；Authority Snapshot 改变时产生不同 Validation Result。
- **依赖模块：**E Candidate Rules；B Epistemic/Domain Semantics；D Canonical/Lifecycle/Fence Predicates；I 当前 Authorization/PermissionEpoch；H Typed Envelope Reference。

### serialize

- **输入：**已验证 Candidate IR 对象，以及显式固定版本的 CandidateSerializationProfile。
- **输出：**确定性 Bytes、Profile/Version Identifier 和 Content Digest；输出是 Candidate Artifact，不是 Canonical Schema Record，也不是 H Wire Message。
- **错误：**Unsupported Profile/Version、Required Field 不可表示、Duplicate/Invalid Key、Invalid Numeric/Time Value、Encoding Failure 和 Unknown Required Extension。
- **不变量：**相同语义 Candidate + 相同 Profile 必须生成字节完全一致的输出；decode(encode(candidate)) 必须保留全部必需字段、Metadata、Reference、Uncertainty 和 Extension；未知的必需语义必须失败，不得消失。
- **副作用：**纯转换；不得分配 Identity、写 Canonical、作 Authorization Decision、Publication 或外部副作用。
- **权限/幂等：**Serialization 可确定性重复执行；受保护内容只有在 Recipient/Scope 获得授权且符合 I Retention/Handling Policy 时才能序列化。
- **依赖模块：**E Candidate Schema/Profile；B Domain Semantics；I Data Handling/Retention；仅在另行请求外部 Wire Mapping 时依赖 H；Canonical Persistence Encoding 依赖 D/Storage。

**Serialization Profile 状态：**内部 Candidate Format 和 Canonicalization Profile 为 CANDIDATE，尚未冻结。选定 Profile 必须定义 UTF-8 处理、对象 Key 确定性排序、稳定 Enum Token、Numeric/Time Encoding、Optional Field 表达、Collection Ordering、Extension Handling 和 Schema Version Compatibility。Unicode Code Point 与原始 Surface Form 必须保留；Normalization 必须显式且带版本，禁止隐式有损改写。任何 Serializer 均不得静默省略未知或不支持的 Source Metadata。H Wire Encoding 和 D/Storage Canonical Persistence 是独立契约。

## 25. Runtime 验收计划——架构测试矩阵

以下仍是计划验收矩阵场景，不是已执行的矩阵结果。另有当前 Workspace Rust 参考 Crate 的 11/11 单元测试通过，如上所述；该结果不满足或改写任何 MC-AT 行。本阶段仍未授权生产 Runtime 集成。

| ID | 场景 | 必须断言 | 状态 |
|---|---|---|---|
| MC-AT-01 | 有效 Accepted Source → Candidate | 生成 Candidate IR 和 Stage Lineage；不暗示 Canonical Status | PLANNED_NOT_RUN |
| MC-AT-02 | 空输入 | 显式 EMPTY_INPUT；不得返回空的成功 Candidate | PLANNED_NOT_RUN |
| MC-AT-03 | 格式错误的 Source/Encoding | 稳定字段定位错误；不得 Panic 或静默截断 | PLANNED_NOT_RUN |
| MC-AT-04 | 缺少必需 Source/Digest/Scope Metadata | 精确路径 Reject 或 Quarantine；不得猜测默认值 | PLANNED_NOT_RUN |
| MC-AT-05 | Unicode、CJK、组合字符和 Emoji | 在固定 Profile 下保留源 Code Point 并往返一致 | PLANNED_NOT_RUN |
| MC-AT-06 | Metadata 和 Optional Field | 保留 Source Time、Locale、Trust、Retention、Qualifier、Uncertainty 和 Optional Value | PLANNED_NOT_RUN |
| MC-AT-07 | 未知 Extension/Source Field | 无损保留，或显式 Unsupported/Quarantine | PLANNED_NOT_RUN |
| MC-AT-08 | 无效 Digest/Source Span | 拒绝超出精确 Source Bytes 或 Digest 不匹配的 Span | PLANNED_NOT_RUN |
| MC-AT-09 | Fact/Claim 语义与身份模型 | 验证消费 Option A + I1 决策；Canonical 字段映射仍等待 D/I/H 契约 | BLOCKED_BY_SCHEMA_CONTRACT |
| MC-AT-10 | Claim Identity/Revision Schema Mapping | 仅在 D Canonical Schema、Lifecycle 和 Consumer Pins 完成后验证 | BLOCKED_BY_SCHEMA_CONTRACT |
| MC-AT-11 | Canonical Identity Conflict | E 不创建/覆盖 Identity；D Conflict 原样上报 | PLANNED_NOT_RUN — 需要 D Fixture |
| MC-AT-12 | Lifecycle Conflict | E 不选择 Lifecycle；保留 D Conflict/Defer | PLANNED_NOT_RUN — 需要 D Fixture |
| MC-AT-13 | PermissionEpoch Mismatch/Revocation | Fail-closed；过期授权不得读取、发布或披露 | PLANNED_NOT_RUN — 需要 I Fixture |
| MC-AT-14 | Forget Fence Race/Conflict | Fence-first 阻止；结果模糊/未知时保持私有；禁止 Fence 后发布 | PLANNED_NOT_RUN — 需要 D/I/Storage Fixture |
| MC-AT-15 | 稳定 Serialization | 相同 Candidate/Profile 生成字节完全一致的 Bytes 和 Digest | PLANNED_NOT_RUN |
| MC-AT-16 | Serialization Round Trip | Decode/Encode 保留语义字段、Metadata、Reference、Unicode 和 Extension | PLANNED_NOT_RUN |
| MC-AT-17 | 不得静默丢失信息 | 前后字段清单一致，或每项损失都有显式 Error/Unresolved Reason | PLANNED_NOT_RUN |
| MC-AT-18 | Idempotency Replay | 相同 Key/Digest 返回既有 Receipt；相同 Key/不同 Digest 为 Conflict | PLANNED_NOT_RUN |
| MC-AT-19 | Policy/Model 变更后的 Recompile | 新建 Attempt/Revision；旧 Candidate 和 Receipt 保持不可变 | PLANNED_NOT_RUN |
| MC-AT-20 | 伪造 Span/Instruction 的 Model Output | 拒绝伪造 Locator；嵌入式指令仅作为惰性来源数据 | PLANNED_NOT_RUN |

未来 Runtime 证据包必须包含精确 Source/Head SHA、可复现命令、测试输出/CI Run、Fixtures、失败路径覆盖和独立回读。两个消费者映射阻塞测试不得通过 Mock Data、Candidate-only Test 或 Owner 沉默改标为 PASS。

## 26. Runtime 实施入口前置条件

Issue #7 在 GitHub 最新状态为 CLOSED AS SUPERSEDED；其控制性 Implementation Binding 仍为 DEFERRED_TO_ENGINEERING_PHASE。本架构工作不会重新打开 Issue #7、改变其状态或授权实施。

生产 Runtime/Conformance 工作开始前，Project Authority 和 Accountable Engineering Leadership 必须登记：(1) Canonical Runtime Repository 和 Active Branch，或经授权的创建决定；(2) D/E/F/G/H/I/Storage 及协调组件的具名工程 Owner/Maintainer；(3) 可复现 Build/CI/Test 命令和权威 Artifact SHA；(4) Deployed Topology、Environment、Database、Queue、Index、Replica 和 Backup/Restore；(5) Contract-to-code Traceability 责任人；(6) 每项实现所需的精确 B/D/I/H/Storage 决策和 Interface Pin；(7) Retry、Concurrency、Permission Revocation、Forget Race、Visibility Uncertainty 和 Restore 的可执行 Fault Hook 与验收 Fixture。

在获得这些授权之前，本契约仅属于架构准备。不得声称存在 Runtime Code、占位实现、生产数据访问/写入、Test PASS、生产 Conformance 或生产激活。

## 27. 架构完成边界与剩余决策

E 所有的 Candidate IR、Validation、compile/validate/serialize 语义、生命周期流程和测试计划已在此形成可审查提案。Owner 已在合并的 PR #446 批准 Option A + I1 语义方向。B ADR 已被取代为当前语义决策请求并保留为历史证据；在 Canonical Mapping 或 Schema 冻结前，精确 D/I/Storage/H 消费者契约仍需版本 Pin、对账和审查。跨 Owner Mapping 的完整架构状态仍为 PARTIAL。当前 Compiler Overview 足以承载验收矩阵，因此不创建新的独立规范文件，也不擅自引入新的规范文件位置。
