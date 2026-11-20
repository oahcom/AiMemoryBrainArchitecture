# Memory Compiler 总览（记忆编译器）

- 文档 ID：E-COMPILER-001
- 版本：1.0
- 源分支：session-e-memory-compiler-2026-11-16
- 源文件版本：DEREFERENCED — 保留历史源 Blob `35a766fae29c0b8ddf692a6ec062762f0fca29d2`；当前仓库不存在可解析的规范性源文件。
- 审查时源分支 HEAD：a1b8ba129ef7d5f4463bd4229667f0b2bf6d9886
- 源规范：DEREFERENCED — 原规范源路径 `04-memory-compiler/compiler-overview.md` 在当前 main tree 中不存在；替代物：[英文对照版](../../en/04-memory-compiler/compiler-overview.md)（Blob `9f6471b40fbede87c746204221a877806e688520`；仅为对照文本，不是规范性替代源）。
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

- OPEN：INT-P0-01 Fact/Claim ADR；Candidate Proposition 映射仍未冻结。
- OPEN：INT-P1-02 Claim Identity/Revision 和 ConflictSet Canonical Shape。
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
- B Fact/Claim 映射仍为 ADR-BLOCKED。CandidateEnvelope/CandidateProposition 仍属于 Canonical 前的 IR。
- 详细 CANDIDATE 契约见 accepted-receipt-and-idempotency-contract.md 和 forget-fence-and-derived-registration.md。
