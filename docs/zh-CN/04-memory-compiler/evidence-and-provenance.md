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
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-082"
        - "source branch: session-e-memory-compiler-2026-11-16"
        - "source commit: ee098e14747d9915de5b3efb63b3a8dd77f670ed"
        - "original source blob: 38bcacafa89ebe7b3eedb6f38d174e0c6a1f3963"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Exact source Blob pinned; translated body retained; semantic parity review pending."
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
    canonical_scope_keywords:
      - bilingual-mirror
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "04-memory-compiler/evidence-and-provenance.md"
    en: "docs/en/04-memory-compiler/evidence-and-provenance.md"
    zh-CN: null
---

# 证据与来源血缘

- 文档 ID：E-EVIDENCE-001
- 版本：1.0
- 源分支：session-e-memory-compiler-2026-11-16
- 源 Blob：38bcacafa89ebe7b3eedb6f38d174e0c6a1f3963
- 对应英文：[Evidence and Provenance](../../en/04-memory-compiler/evidence-and-provenance.md)
- 状态：可追溯性、授权和 Forget 义务已 DECIDED；Graph 表示为 CANDIDATE；最终 DAG/Reference Contract 等待 D/I，状态 OPEN
- Owner：Memory Compiler / MC-03
- 集成关系：INT-P0-02/03/04；INT-P1-02/06；DM-006/007/010/011

## 1. 目的

为每个 Compiler 产生的 Candidate，以及由此被接受的每个 Canonical Asset，创建并维护可验证的 Source Link 和 Derivation Lineage。Evidence 回答哪些来源材料支持、反驳或限定某个 Proposition。Provenance 回答某个 Target 是如何派生的。二者都不是 Truth Score。

## 2. 范围

包括 Evidence Identity Proposal、Source Ref/Locator 校验、Source Span 保留、Evidence-to-Proposition Role Link、Provenance Node/Edge、Method/Model Lineage、Source Trust Metadata 传播、Access Control 检查、Lineage Traversal、Dependency Registration，以及感知 Forget 的失效处理。

不包括 D 最终 Canonical Evidence/Claim Schema、I 的 Policy/Physical Deletion Authority、Canonical Store Transaction 实现、Source Truth Adjudication 和外部 Provider Erasure Guarantee。

## 3. 职责

将每个 Evidence Item 绑定到类型化、带版本的 Source Ref（若可用）；保留 Locator、Source Digest、Collector、Recorded/Observed Time 和 Scope；区分 Support/Refutation/Qualification/Context-only Role；记录 Transformation Method/Version/Input Digest/Parent Provenance；保留共同来源血缘；独立执行 Evidence Authorization；为 Forget 登记 Derivation Dependency；如实标记 Unavailable/Restricted/Expired/Forgotten Source。

## 4. 非职责

Evidence Manager 不判断 Proposition 为真，不将 Source Trust 转换为 Claim Verification，不决定 Fact/Claim Identity，不分配最终 Lifecycle，不拥有 Canonical Entity Identity，也不能违反 I 的 Forget Policy 保留内容。

## 5. 输入 / 输出

**输入：** Source Event/Document/Tool/Environment Ref、Source Digest/Version、已验证 Span/Locator、CandidateProposition/RelationHypothesis、ScopeRefs、Actor/Collector、Method Receipt、Trust Metadata、Retention/Sensitivity 和 Evidential Role。

**输出：** EvidenceDraft/Canonical Evidence Proposal、EvidenceLink、ProvenanceNode/Edge、Dependency Registration、Lineage Query Result、结构化 Access/Unavailable Result，以及 Forget Impact Ref。

## 6. 数据模型

### 6.1 Evidence（与 B 对齐的逻辑 Proposal）

~~~text
Evidence {
  evidence_id: OpaqueId
  evidence_kind: source_span | user_statement | document | observation |
                 tool_result | attestation | derived_excerpt
  source_ref: TypedObjectRef
  source_version_ref: TypedObjectRef?
  locator: Locator?
  excerpt_ref: ContentRef?
  source_digest: Digest?
  observed_at: TimeValue?
  recorded_at: Instant
  collector_ref: ActorRef
  evidential_role: supports | refutes | qualifies | context_only
  source_reliability_ref: TypedObjectRef?
  scope_refs: ScopeRef[]
  availability_state: available | restricted | expired | forgotten | external_unavailable
  retention_class: RetentionClass
  sensitivity: Sensitivity
}
~~~

### 6.2 Locator 与 EvidenceLink

~~~text
Locator =
  MessageSpan(message_ref, byte_or_token_range, encoding_version)
  | DocumentLocation(document_ref, page, block_or_char_range)
  | JsonPath(source_ref, canonical_path)
  | MediaRange(source_ref, start_time, end_time, track_ref?)
  | EnvironmentTick(environment_ref, tick_or_frame, observation_ref)
  | StructuredField(source_ref, field_path)

EvidenceLink {
  target_ref: TypedObjectRef
  evidence_ref: TypedObjectRef
  role: supports | refutes | qualifies | context_only
  strength_assessment: MethodQualifiedScore?
  asserted_by: ActorRef
  scope_refs: ScopeRef[]
  created_at: Instant
}
~~~

Strength 针对特定 Target-Evidence Link，由 Method 限定，并且不同于 Source Trust 或 Claim Confidence。本文不冻结任何数值评分标准。

### 6.3 Provenance Node / Edge

~~~text
ProvenanceNode {
  provenance_id: OpaqueId
  target_ref: TypedObjectRef
  derivation_kind: direct_capture | extraction | normalization |
                   summarization | consolidation | inference |
                   human_correction | verification | migration
  method_ref: MethodRef
  derived_at: Instant
  input_digest_refs: DigestRef[]
  unavailable_reason: String?
  scope_refs: ScopeRef[]
  pipeline_version: Version
}
ProvenanceEdge {
  provenance_id: OpaqueId
  source_ref: TypedObjectRef
  source_role: primary | supporting | contradicting | context
  locator_ref: TypedObjectRef?
  parent_provenance_ref: TypedObjectRef?
}
~~~

一次 Derivation 有一个 Target 和一个或多个声明的 Source Edge；也可以使用 Policy 允许的明确 Unavailable Reason。Method Ref 描述处理过程，不证明结果正确。

## 7. Pipeline / 状态机

~~~mermaid
flowchart TD
 S[Source Event / Document] --> L[Resolve source + immutable version]
 L --> A[Authorize source and Scope]
 A --> V[Validate locator / digest]
 V --> E[Create Evidence + role links]
 E --> P[Create Provenance node and parent edges]
 P --> D[Register dependency edges]
 D --> C[Attach to candidate / canonical transaction]
 C --> X[Publish lineage/change event]
~~~

Evidence 状态：DRAFT → VALIDATED → PERSISTED → RESTRICTED / EXPIRED / FORGOTTEN / EXTERNAL_UNAVAILABLE。Provenance 状态采用追加方式；纠正时追加 Node/Edge 或明确 Superseding Metadata，绝不改写历史。

## 8. 不变量

每个派生 Memory/Claim/Relation 都有可追溯 Evidence/Provenance，或明确的 Unavailability Reason；Source/Locator 必须针对准确的不可变 Source Version/Digest 校验；单独一个可变 URL 不是持久化 Evidence；Evidence Role 针对特定 Target；保留共同来源血缘；Evidence Authorization 独立；Provenance 不得遍历未授权 Scope；Model Output 不能伪造 Span/Digest/Actor/Lineage；Forget Metadata 不得保留被禁止的内容；在 Canonical 使用前必须声明 Cycle Policy。

## 9. 幂等性

Evidence Identity 来源于 Source Identity/Version + Locator + Digest + Scope + Evidence Kind。相同 Identity/Digest 复用记录；Digest 改变代表新的 Source Version 或 Integrity Conflict，绝不能覆盖。Provenance Node Identity 来源于 Target Proposal/Version + Derivation Kind + Method Version + 有序 Input Digest。重复执行 Stage 返回原 Node。Method/Input 改变时创建新 Node，并链接到之前的 Lineage。

## 10. 一致性

Evidence Record 和 Target Link 必须与 Candidate/Canonical Version 原子提交，或采用 Outbox Protocol，防止 Target 已提交但必需 Lineage 缺失。声明 Derivation 完成前，Provenance Dependency Edge 必须持久化。如果 Canonical Store 与 Provenance Store 分离，Canonical Transaction 必须包含持久化 Pending-lineage Marker；必需 Provenance 提交前不得使 Target 可见。Projection 故障从 Canonical Change Log 修复。

## 11. 故障恢复

- Source Bytes 缺失：保留 Typed Source Ref/Digest，并标记 Unavailable。
- Locator 不匹配：拒绝 Link。
- Evidence 持久化失败：Defer Candidate。
- Provenance Edge 失败：阻止完成/发布。
- External URL 改变：绝不静默替换。
- Forget Fence：抑制 Dereference 并取消下游 Job。
- Replay：在允许范围内复用原始 Source Identity/Digest。
- Graph Read 部分完成：明确返回 Incomplete Status。

## 12. 安全 / Scope

在 Source Fetch、Locator Resolution、Lineage Traversal 或 Dependency Expansion 之前，必须对每个 Source/Edge 授权。Graph Traversal 和 Count Aggregation 前执行 Scope Filter。除非 I 明确授权 Declassification，Derived Summary 不得继承比 Source Policy 更宽的访问权限。Locator Path、Message ID、Page Number 和 Environment Coordinate 可能敏感。Memory Read 不意味着 evidence.read。Worker 在每次受保护 Dereference/Commit 前重新检查 Permission 和 Forget Fence。

Prompt Injection Provenance 保留 Source Type、Trust Label、Untrusted-content Classification、Extraction Method 和 Source Span。这有助于审计，但不代表内容安全。Evidence 永远不是可执行指令或 Tool Authorization。检测是启发式且不完整；下游 Model 仍可能受到影响。

## 13. 性能 / Backpressure

限制 Lineage Depth、Fan-out、Page Size 和 Dependency Traversal Time。使用带 Continuation Watermark 的分页 Traversal，并显式标记 Partial Result。Metadata 足够时避免预先加载 Source Content。Cache Key 包含 Principal/Scope/Policy Epoch 和 Source Version；Revocation/Forget 使 Cache 失效。测量 Provenance Coverage、Traversal Depth/Fan-out、Dependency Discovery Duration、Incomplete Lineage、Duplicate Ancestry 和 Forget Residual Count。数值边界为 TO_VALIDATE。

## 14. 可观测性

跟踪 source_ref → evidence_id → provenance_id → candidate_id → canonical version。记录 Method/Model/Rule Version、Digest、Role、Locator Validation Result、Availability State、Authorization Decision Ref、Graph Generation、Retry 和 Error。不得记录 Excerpt Content 或敏感 Locator String。指标包括 Lineage Completeness、Evidence Access Denial、Unavailable Source Rate、Graph Depth/Fan-out、Dependency Queue Age 和 Deletion Progress。

## 15. 接口

- **Extraction → Evidence：** Source Span/Locator、Source Digest/Version、Proposition Ref、Role Hypothesis、Scope 和 Method Receipt。
- **Evidence → D：** Typed Evidence Ref 和 Source Availability；最终 Object Contract 由 D 拥有。
- **Evidence → Consolidation：** 针对 Target 的 Support/Refute/Qualify Link、共同来源血缘、Trust Metadata 和 Provenance。
- **D → F：** Canonical Evidence/Provenance Ref 和 Generation；F 不得暴露未授权 Source。
- **E/D → I：** Dependency Registration 和 Forget-impact Enumeration；Policy、Access Barrier 和 Physical Deletion 由 I 拥有。
- **G：** 接收 Forget/Retraction/Supersession Notification，以协调 Context Ref。
- **Storage/Consistency：** Target + Lineage 原子可见性和可 Replay Outbox。

## 16. 测试场景

Source Span 精确性；同一 Source 的重复副本不能算独立 Evidence；Evidence 对不同 Claim 分别支持/反驳；Replay 时 Source 不可用；Memory Read 已授权但 Evidence Dereference 被拒绝；跨 Scope Lineage Traversal；Provenance Cycle 拒绝；Lineage 部分响应；Target Proposal 与 Lineage Commit 之间崩溃；Lineage Expansion 期间发生 Forget；Source Digest 变化；恶意内容作为数据保留。

## 17. 依赖

B Domain Model 的 Reference/Time/Scope Semantics；D Canonical Object/Version Contract；I Policy/Retention/Forget；H Authenticated ActorRef；Extraction IR；Entity/Relation Manager；Storage/Outbox；F Projection 和 G Context Invalidation Consumer。

## 18. 开放问题

- OPEN：INT-P1-06/DM-007 DAG 与受限 Cycle 语义；推荐默认严格无环 Derivation Graph，Lineage 中不允许 Cycle Edge。
- OPEN：与 D 对齐 Typed Locator/ContentRef 最终 Schema。
- CANDIDATE：Evidence Identity 和 Provenance Node Identity 公式。
- TO_VALIDATE：Lineage Depth/Fan-out Limit、Traversal Latency 和 Dependency Discovery Completeness。
- OPEN：Source Content 被遗忘后 Digest 和最小 Tombstone 的 Retention Policy。

## 19. Durable Dependency Registration 与 Forget 补充

- 每个 Evidence、EvidenceLink、ProvenanceNode/Edge、Excerpt、Normalized Artifact 和 Derived Summary 都必须保留传递性 Source Lineage，或使用 I 批准的不可逆 Dependency Token。
- Dependency Registration 是 Publication Prerequisite，不是事后补充 Metadata。先将 Output 私有暂存，持久化 Provenance，向 D-owned Forget Inventory/Barrier 登记所有 Source Dependency，重新验证 Fence，最后才能让对象可见。
- Provenance Edge 本身不能证明 D Completion Barrier 已核算某个在途 Producer。E 必须登记 Producer/Run，并取得持久化 Dependency Registration ACK。
- Source Content、Excerpt Ref、原始 Payload Hash 和可逆 Payload URI 不得复制到 Forget Tombstone。Tombstone 只包含 I 允许的最少、不可反向重建的 Suppression Evidence。
- Fence 激活时，阻止对已遗忘 Source 的 Dereference/Lineage Expansion；将 Descendant 标记为 Suppressed/Restricted。Traversal 不完整或不可达时必须报告 Pending/Unknown，绝不能报告 Complete。
- Visibility Gate、Race Protocol 和 Failure Matrix 见 [Forget Fence and Derived Registration](forget-fence-and-derived-registration-part1.md)。Physical Erasure 和 Global Completion 仍由 I 拥有。

## 20. Phase 3 Producer Registration、Cursor 与可见性对齐

本附录消费 D 版本 30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6，不冻结跨模块 Schema。

- Compiler Run 产生的每个 Evidence/Provenance Node/Edge 都是派生物。它首先持久化到 Private Staging；在所有直接/传递 Dependency 都取得 D Durable DerivedRegistrationReceipt，且最终 Publication Gate 成功之前，Runtime/其他 Consumer 都不能 Query/Traverse。
- Lineage Record 绑定 EventRef、Source Version Ref、Provenance Parent Ref、DerivationRunId、ProducerWorkItemId、准确 ScopeRefs、Lineage Digest、已观察 ForgetFenceCursor 和 PermissionEpoch。Observed Epoch 只是历史证据，不是之后的 Publish Authorization。
- SourceEventCursor 仍是 E 的 Ingress Partition Position。CanonicalCommitCursor 是 D 在单个 Brain Authority 内全局有序的已提交事务位置。AggregateRevision 按 Aggregate 计算。LifecycleEventCursor 按 Memory 计算。IndexWatermark 由 F 拥有，并以 CanonicalCommitCursor 表示已应用位置。ForgetFenceCursor 和 PermissionEpoch 属于不同 Namespace。Provenance 中不得使用无类型的通用 cursor 或 generation 字段承载这些值。
- D 确认 Canonical Commit 时，Provenance 分别记录返回的 CanonicalCommitCursor 和准确 AggregateRevision Ref。只有实际存在 Lifecycle Event 时才记录 LifecycleEventCursor。仅 Candidate 的 Extraction/Provenance 不具有这些 Canonical 字段。
- Provenance 持久化本身不等于 Dependency Registration。本地 Edge 不是 D Registration Receipt。任何 D Registration 缺失/部分完成/状态未知，都会使完整派生 Lineage 保持 Private/Non-visible。
- E Storage Staging、D Dependency Inventory、D Final Gate 和 Storage Visibility 之间的原子关系仍为 **OPEN / BLOCKING**。如果无法在一个 Transaction 中串行化，或无法使用经过证明的可恢复 Prepare/Commit Protocol，则 E 不得暴露 Lineage 或派生物。

一致性场景（NOT RUN）：Provenance Edge 部分登记；重复 Registration ACK 丢失；Lineage Staging 与 Gate 之间发生 Forget；Traversal 期间 PermissionEpoch 改变；派生物的派生物祖先抑制；拒绝 Cursor Type 替换。
