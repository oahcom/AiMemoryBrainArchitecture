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
        - "original source blob: d16f8e2e41a6cca81ad285e5f79f075d87e64edb"
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
    source: "04-memory-compiler/consolidation-and-conflict-resolution.md"
    en: "docs/en/04-memory-compiler/consolidation-and-conflict-resolution.md"
    zh-CN: null
---

# 巩固与冲突解决

- 文档 ID：E-CONSOLIDATION-001
- 版本：1.0
- 源分支：session-e-memory-compiler-2026-11-16
- 源 Blob：d16f8e2e41a6cca81ad285e5f79f075d87e64edb
- 对应英文：[Consolidation and Conflict Resolution](../../en/04-memory-compiler/consolidation-and-conflict-resolution.md)
- 状态：禁止静默覆盖、Evidence 保留和 Canonical Authority 边界已 DECIDED；匹配/评分策略为 CANDIDATE；Claim Identity/Revision 和 ConflictSet Schema 为 OPEN
- Owner：Memory Compiler / MC-04
- 集成关系：INT-P0-01/02/03；INT-P1-02/04/06；AR-004

## 1. 目的

将 Candidate Proposition/Memory 与已授权的 Canonical Asset 进行比较，识别重复、相关 Claim、时间共存、Revision 和真实冲突，并为 D 的 Canonical Memory/Lifecycle Authority 生成可审计 Proposal。Consolidation 不是盲目去重；Conflict Detection 也不是 Truth Adjudication。

## 2. 范围

包括 Candidate Grouping、Duplicate Detection、Entity Resolution 协作、Claim Revision Proposal、ConflictSet Proposal、Evidence Comparison、基于 Policy 的 Consolidation Recommendation、Human/Agent Review Routing、Canonical Write Request 准备，以及 Commit 后 Projection Notification。

不包括最终 Claim Identity、ConflictSet Canonical Schema 和 Lifecycle Authority（D）；Entity Merge/Split Authority（D Entity Manager）；Runtime Relevance Ranking（F）；Context Editing（G）；Governance/Retention Authorization（I）。

## 3. 职责

只有完成 Scope/Permission Filter 后才能构建 Candidate Comparison Set；区分 Exact Duplicate、Paraphrase、Related Proposition、Temporal Update、Revision 和 Contradiction；比较 Subject/Predicate/Object/Polarity、Modality、Scope、Environment、Valid-time Overlap、Epistemic Status 和 Evidence；保留 Supporting/Refuting/Qualifying Evidence 及共同来源血缘；请求 Entity Manager 解析 Identity；创建明确的 ConflictSet/ClaimRevision Proposal；不确定或高影响决策交由已授权 Review；提交带 Version Check 的 Canonical Write。

## 4. 非职责

Compiler 不决定 Canonical Truth，不基于 Confidence 将 Claim 提升为 Verified，不静默覆盖既有 Claim，不独立合并 Entity，不删除 Superseded History，不设置最终 Lifecycle State，也不允许 LLM 作出 Authorization/Lifecycle Decision。

## 5. 输入 / 输出

**输入：** CandidateEnvelope 和 ExtractionIR；Evidence/Provenance；已授权 Canonical Candidate Set；Entity/Relation Response；D 当前 Version/Lifecycle State；Scope/Permission Context；Policy 和 Vocabulary Version。

**输出：** ConsolidationProposal；DuplicateAssessment；ClaimRevisionProposal；ConflictSetProposal；EvidenceComparison；EntityResolutionRequest；CanonicalWriteRequest；ReviewTask；Commit/Deferred/Rejected Result；IndexPublicationRequested Event。

## 6. 数据模型

### 6.1 ConsolidationProposal

~~~text
ConsolidationProposal {
  proposal_id: OpaqueId
  scope_refs: ScopeRef[]
  candidate_refs: TypedObjectRef[]
  target_memory_ref: TypedObjectRef?
  proposed_operation: create | append_claim | revise_claim |
                     supersede | relate | split_candidate | defer
  duplicate_assessments: DuplicateAssessment[]
  revision_proposals: ClaimRevisionProposal[]
  conflict_set_proposals: ConflictSetProposal[]
  evidence_comparisons: EvidenceComparison[]
  entity_resolution_refs: TypedObjectRef[]
  expected_canonical_version: VersionRef?
  policy_version: Version
  method_refs: MethodRef[]
  decision_rationale_refs: TypedObjectRef[]
  created_at: Instant
}
~~~

### 6.2 ConflictSetProposal（CANDIDATE；最终 Schema 由 D 拥有）

~~~text
ConflictSetProposal {
  proposal_id: OpaqueId
  scope_refs: ScopeRef[]
  participant_proposition_refs: TypedObjectRef[]
  conflict_dimensions: subject | predicate | object | polarity |
                       temporal_overlap | source_disagreement |
                       modality | scope_incompatibility
  temporal_intersection: TimeInterval?
  supporting_evidence_refs: TypedObjectRef[]
  refuting_evidence_refs: TypedObjectRef[]
  common_ancestry_refs: TypedObjectRef[]
  state: unresolved | review_required | resolved_proposal
  proposed_resolution: retain_both | select_successor | retract |
                       narrow_validity | mark_disputed | no_conflict
  rationale: String
  method_refs: MethodRef[]
}
~~~

最终 Conflict/ConflictSet Identity、Revision 和 Lifecycle 受 INT-P1-02/D 阻塞。本 Proposal 不冻结 D 的 Schema。

### 6.3 ClaimRevisionProposal（CANDIDATE）

~~~text
ClaimRevisionProposal {
  prior_claim_ref: TypedObjectRef
  proposed_claim_ref: TypedObjectRef
  relation: correct | refine | supersede | retract | reinstate
  reason: String
  evidence_refs: TypedObjectRef[]
  expected_claim_or_memory_version: VersionRef
  scope_refs: ScopeRef[]
  temporal_effect: TimeInterval?
  provenance_ref: TypedObjectRef
}
~~~

该结构同时兼容稳定 Claim Identity + 不可变 Revision，或 Successor Claim Identity。必须等待 D 明确策略后再映射。

## 7. Pipeline / 状态机

~~~mermaid
flowchart TD
 A[Candidate + Evidence] --> B[Resolve and authorize Scope]
 B --> C[Generate comparable canonical set]
 C --> D[Entity identity resolution]
 D --> E[Exact / semantic duplicate assessment]
 E --> F[Temporal + epistemic comparison]
 F --> G[Conflict / revision proposal]
 G --> H{Policy confidence and impact}
 H -->|routine safe| I[Prepare Canonical Write]
 H -->|ambiguous/high impact| J[Human or Agent review]
 H -->|insufficient evidence| K[Defer / retain candidate]
 I --> L[D lifecycle + version-checked commit]
 J --> L
 L -->|committed| M[Canonical change outbox]
 L -->|stale/conflict| N[Reload and reconcile]
 M --> O[Index publication request]
~~~

状态：PROPOSED → SCOPE_FILTERED → MATCHED → ASSESSED → REVIEW_PENDING 或 WRITE_PENDING → COMMITTED / DEFERRED / REJECTED / STALE_RECONCILE。每个状态都必须连同 Attempt 和 Policy Version 持久化。

## 8. 不变量

Scope Filter 必须先于 Comparison Set Generation、Graph Expansion、Similarity Search 和 Aggregation。没有明确 Sharing 时，不得合并不同 User 或不兼容 Environment Scope 的数据。相同 Label 或 Embedding Proximity 不能证明 Entity Identity。Intent/Plan/Prediction/Attempted Action 不是 Outcome。如果 Valid-time Interval 不重叠，或 Scope/Modality 不同，则不能推断 Contradiction。冲突 Claim 绝不能静默覆盖。必须考虑 Evidence Ancestry。Confidence 和 Semantic Similarity 不等于 Truth 或 Verification。Canonical Write 使用 D 的 Expected-version/Lifecycle Contract。Canonical Commit 与 Index Visibility 是两个独立里程碑。

## 9. 幂等性

Proposal Identity 来自排序后的 Candidate Ref + Source Digest + Canonical Target/Version + Scope + Policy/Method Version。相同输入返回相同逻辑 Proposal。Canonical Version 或 Policy 改变时创建新的 Proposal Revision。Commit Request 使用稳定 Operation Key；相同 Key/Payload 返回原 Commit；相同 Key/不同 Payload 冲突。Commit Outcome 未知时，重试前必须先向 D 查询。

## 10. 一致性

Consolidation 读取带 Scope 的 Canonical Snapshot/Generation。Candidate Set 记录其 Generation 和 Policy Version。Canonical Write 包含 Expected Target Version 和 Source Lineage。D 原子提交不可变 Memory Version/Current Pointer，以及必需的 Claim/Evidence/Provenance Ref 和 Outbox。如果 Index Publication 失败，Canonical 仍是权威，Index Watermark 保持落后。不假设 D、Model Provider 和 Index 之间存在一个跨域事务；必须使用可恢复 Outbox/Replay。

## 11. 故障恢复

Entity Resolution 有歧义时保留 Hypothesis 并 Defer；Canonical Generation 变化时重建 Comparison Set；Stale Version 触发 Reload/Re-assessment；Conflict Detector 故障时保留 Candidate；Review 故障时保持 Review-pending；Evidence 不可用时降低资格或 Defer；Model 故障时仍可运行确定性检查；Forget Fence 取消 Comparison 并抑制 Proposal/Replay；Commit Outcome 未知时查询 D；Index 故障时保留 Outbox 并重试。

## 12. 安全 / Scope

所有 Candidate/Canonical Participant 在进入 Comparison Set 前必须授权读取。禁止跨 Scope Embedding/Graph Matching。Scope 必须符合 D/I Policy；对依赖 Environment 的 Proposition，Environment Scope 是硬隔离边界。Evidence Ref 需要独立 Permission。异步 Review/Write Worker 必须重新检查 Grant、Revocation Epoch 和 Forget Fence。Review Task 只能披露已授权摘录。Content 始终是不可信数据；Instruction-like Text 不能触发 Review Action、Tool Call 或 Privilege Escalation。

## 13. 性能 / Backpressure

先使用廉价的确定性 Blocking Key（Scope、Entity Ref、Predicate/Type、Time Bucket、Source Identity），再进行有界 Lexical/Semantic Candidate Expansion。限制 Candidate Count、Graph Depth、Fan-out、Model Comparison、Review Queue 和 Per-scope Concurrency。Semantic Similarity 只用于 Candidate Generation。过载时延迟低优先级 Consolidation，但保留 Candidate/Provenance；绝不削弱 Scope Filter。测量 False Duplicate、False Conflict、Missed Conflict、Review Rate、Canonical Conflict Rate、Fan-out、Time-to-commit 和资源使用。阈值为 TO_VALIDATE。

## 14. 可观测性

记录 Proposal ID、Candidate/Target Ref（在 Trace 中保护）、Scope Class、Canonical Generation、Policy/Method Version、Duplicate/Conflict Classification、Evidence Ancestry Summary、Review Status、Expected/Actual Version、Commit Result、Index Generation、Retry 和 Latency。Metric 不应包含高基数 ID 或敏感 Proposition Text。对 Revision/Retraction/Merge Proposal 和 D 最终 Decision，使用 Actor/Reason 进行审计。

## 15. 接口

### 15.1 D — Canonical Write Contract

Candidate Request 字段：request_id、schema_version、actor_ref、scope_refs、environment_scope_ref、operation/idempotency key、expected_memory_version 或 expected_claim_revision、ADR 决议后的 Candidate Object Mapping、entity/relation refs、evidence_refs、provenance_refs、conflict_set_refs/proposals、temporal/epistemic qualifiers、source Event refs、policy/method refs、correlation/causation ID。

D Response：committed/deferred/rejected/stale；Canonical Memory/Version Ref；Claim Revision Ref；Lifecycle Decision/Reason；Commit Generation；Outbox Event Ref。错误：SCOPE_MISMATCH、PERMISSION_DENIED、STALE_VERSION、INVALID_TRANSITION、MISSING_EVIDENCE、PROVENANCE_INCOMPLETE、CONFLICT_REQUIRES_REVIEW、IDEMPOTENCY_CONFLICT、FORGET_FENCE_ACTIVE。

只有 D 决定 Canonical ID、Claim Identity/Revision、ConflictSet Canonical Shape 和 Lifecycle State。Compiler 使用相同 Operation Key 重试；Outcome 未知时重新读取 D。

### 15.2 F — Index Publication

Canonical Commit 时发布 CanonicalCommitCommitted，包含 commit_id、canonical_generation、变更的 Memory/Version/Claim/Entity/Relation Ref、Scope Ref、Change Kind、Provenance Ref 和 Event Schema Version。F 单独 ACK Applied Generation/Watermark。Index Projection 包含 Memory、Entity、Relation；只有获得授权时才包含 Claim/Evidence Metadata。Stale Index Generation 必须可检测；Index 必须可重建。

### 15.3 G — Context Impact Event

发布 MemoryVersionChanged、ClaimRetracted、MemorySuperseded、MemoryArchived、MemoryForgotten、EvidenceRestricted，携带 Canonical Ref、Prior/New Version、Scope、Event Generation、Reason Code 和 Correlation。G 决定受影响 Context Entry 应被 Remove、Replace、Qualify 还是 Replan。Compiler 不修改 Context。

### 15.4 H 和 I

H 接收 Event Accepted 与 Processing State 的区别。I 提供 Authorization Recheck、Forget Fence、Retention Class 和 Deletion Obligation。所有消息都必须有 Versioned Schema、Idempotency、Typed Error 和 Replay Semantics。

## 16. 测试场景

跨 Scope 的同名 Entity；同一个 Agent 位于两个 World；Paraphrase Duplicate 与不同时间 Claim 的区分；时间重叠的矛盾 Claim 创建 ConflictSet；时间不重叠的 Claim 共存；复制的 Evidence 不算独立证据；Entity Manager 拒绝模型建议的错误 Merge；两个并发 Canonical Write；Stale Commit Retry；显式 Retraction 保留历史；Review 期间发生 Forget；Commit 后 Index 故障；Commit 前 Permission 被撤销。

## 17. 依赖

D Canonical Memory/Lifecycle/Entity Manager；B Claim/Epistemic/Time/Provenance Semantics；I Scope/Permission/Forget/Retention；F Index Projection/Watermark；G Context Impact；H Actor/Scope Identity；Evidence/Provenance Store；Storage/Consistency Outbox/Generation Model。

## 18. 开放问题

- OPEN：INT-P0-01 Fact/Claim ADR 和 Output Mapping。
- OPEN：INT-P1-02 Stable Claim ID 与 Successor Revision 的选择，以及 Canonical ConflictSet Model。
- OPEN：INT-P1-06 Lifecycle Authority Record 和 Provenance DAG。
- CANDIDATE：Deterministic Blocking Key + Semantic Candidate Generation + Explicit Review。
- TO_VALIDATE：Duplicate/Conflict Precision 和 Recall、Candidate Fan-out、Human Review Volume/Latency。
- OPEN：获授权的 Human/Agent Adjudicator 及权威 Attestation（D/I）。

## 19. 跨模块接口契约细节（Owner 批准前为 CANDIDATE）

以下是最低语义契约，不替代 D/F/G/H/I 各自拥有的规范。所有消息都必须带 Version、Typed Field、Scope、Correlation，并支持 Replay。

| Consumer / Producer | 必需字段 | Version / Idempotency | Authorization | Errors | Recovery |
|---|---|---|---|---|---|
| D Canonical Write | request_id、schema_version、actor_ref、scope_refs、environment_scope_ref、source_event_refs、candidate refs、entity/relation refs、evidence_refs、provenance_refs、conflict/revision proposal、expected canonical version、operation key、policy/method refs、correlation/causation | Schema + Domain Schema Version；相同 Operation Key/Payload 返回同一 Commit；不同 Payload 冲突 | D/I 在 Commit 前立即授权 Actor、Action、所有 Source/Evidence Ref、Target Scope 和 Forget Fence | SCOPE_MISMATCH、PERMISSION_DENIED、STALE_VERSION、INVALID_TRANSITION、MISSING_EVIDENCE、PROVENANCE_INCOMPLETE、CONFLICT_REQUIRES_REVIEW、IDEMPOTENCY_CONFLICT、FORGET_FENCE_ACTIVE | Timeout 后查询 Operation；Stale 时 Reload/Re-propose；禁止盲目重试 |
| F Index Publication | event_id、schema_version、commit_id、canonical_generation、changed object refs/types、prior/new version refs、scope_refs、change_kind、provenance_refs、recorded_at、correlation/causation | Event Schema Version；commit_id + generation 唯一；Consumer Checkpoint/Watermark 单调 | F 对每个 Projection 按 Scope 和 Object Permission Filter；Evidence Projection 需要独立授权 | INVALID_EVENT、SCOPE_DENIED、STALE_GENERATION、GAP_DETECTED、PROJECTION_UNAVAILABLE | At-least-once Consume；按 event_id/commit_id 去重；从 Durable Canonical Outbox Replay；完整应用后才能 Rebuild Projection/发布 Watermark |
| G Context Impact | event_id、schema_version、canonical_ref、prior/new version、lifecycle/change kind、scope_refs、generation、reason_code、occurred_at、correlation/causation | event_id + canonical generation 唯一；重复 Delivery 为 No-op | G/I 在 Context Read/Write 或 Adapter Delivery 前重新检查当前 Access 和 Forget/Revocation Epoch | UNKNOWN_CONTEXT、SCOPE_DENIED、STALE_CONTEXT、RECONCILIATION_REQUIRED、FORGET_SUPPRESSED | Context Version/Reconciliation 由 G 拥有；E Replay Event；E 不修改 Context；迟到/重复 Event 不得回退 Version |
| H Accepted / Status | schema_version、authenticated producer identity、actor_ref、scope_refs、event/source identity、payload_ref/digest、idempotency_key、source times、retention/sensitivity、correlation/causation；receipt_id/event_id/accepted_at/status | Protocol + Envelope Version；相同 Key/Digest 返回同一 Receipt；不同 Digest 冲突 | H 认证 Producer；I 授权 event.ingest；E 重新检查 Worker Permission | INVALID_ENVELOPE、UNAUTHENTICATED_PRODUCER、SCOPE_INVALID、PERMISSION_DENIED、IDEMPOTENCY_KEY_REUSE_CONFLICT、INGRESS_CAPACITY_EXCEEDED、RETRYABLE_UNAVAILABLE | Receipt Lookup；Durable Outbox 重建 Work；Processing Status 与 Accepted 分开；Replay 保留 Event Identity |
| I Authorization / Forget | principal/actor、action、resource refs、scope_refs、policy/revocation epoch、retention_class、forget_operation_ref、fence_epoch、dependency refs、audit correlation | Governance Policy Version 和 Fence Epoch；重复 Forget 幂等；Stage Progress 单调 | I 是 Policy Authority；E 在 Ingress、每个 Worker Stage、Replay 和 Canonical Commit 执行 Decision | PERMISSION_DENIED、POLICY_UNAVAILABLE、SCOPE_REVOKED、RETENTION_BLOCKED、FORGET_FENCE_ACTIVE、FORGET_IN_PROGRESS | 受保护 Operation Fail-closed；Policy 恢复后暂停/重试 Worker；持久化 Fence 防止复活；只有 I Target Evidence 能证明完成 |

### 19.1 共享 Error 与 Replay 规则

- Error 必须区分永久拒绝、可重试不可用、Stale-version Conflict、Policy Denial、Dependency 缺失和 Projection 部分完成。
- Error Body 不得披露受保护对象是否存在、内容、Identifier 或 Candidate Count。
- 每条异步消息都有稳定 Event/Operation Identity、Attempt Metadata 和 Correlation/Causation。
- 假设 Delivery 为 At-least-once；Consumer 必须去重，并将 Checkpoint 与本地效果一起提交，或采用等价 Inbox/Outbox Protocol。
- Replay 是对既有不可变 Source/Operation Identity 的一次执行尝试，不是重新创建已删除内容的许可。
- Forget Fence 或 Authorization Revocation 必须在下一次受保护 Dereference/Mutation 前，使排队 Work 和缓存 Decision 失效。
- 任何组件都不能根据 Timeout 推断成功。必须按稳定 Operation/Event ID 查询，并向权威 Owner 协调。

### 19.2 所有权与兼容性

D 拥有 Canonical Object Semantics 和 Write Decision；F 拥有 Index Projection/Watermark；G 拥有 Context State；H 拥有 Protocol/Producer Authentication；I 拥有 Policy/Revocation/Retention。E 在这些边界上是 Producer/Consumer，不是第二个 Authority。破坏性语义变更必须执行所属模块的 Version Migration 和跨模块 Conformance Update；只有在不改变必需语义时，才可以忽略未知 Optional Extension Field。

## 20. Durable Receipt、Cursor 与 Forget 补充

- Consolidation 只消费已持久化 Accepted Event Identity 和带版本的 Compiled Candidate。Replay 已有 Receipt 不会创建新 Event；Replay/Recompile 在相同不可变 Source Identity 和当前授权下创建新 Attempt。
- 每次 Comparison Set Read、Entity Resolution、Review Task Creation、Canonical Write Submission 和延迟 Retry，都必须检查当前 D Forget Fence 与 I Authorization Epoch。Stale Lease/Fence Epoch 会抑制 Proposal。
- Canonical Write Operation Identity 在重试期间保持稳定。若 D Response 未知，使用相同 Operation Key 查询 D；绝不创建新 Key 来强制产生第二次 Canonical Effect。
- 只有 D 返回 CanonicalCommitted 及其 Canonical Cursor。E 记录引用，但不分配或解释该 Cursor。只有 F 能确认 Indexed，并推进其 Per-index/Per-partition Watermark。
- Forget Fence 激活后，不能再发布任何源自被遗忘来源的 Candidate、Conflict Proposal、Review Payload 或 Canonical Write Envelope。派生 Dependency Registration 必须先于可见性。
- CandidateProposition/ExtractionIR 到 Canonical Claim 的 Mapping，在 B/Governance 批准前仍为 **ADR-BLOCKED**。
- E 边界候选规范见 [Accepted Receipt and Idempotency Contract](accepted-receipt-and-idempotency-contract.md) 和 [Forget Fence and Derived Registration](forget-fence-and-derived-registration-part1.md)；在 D/H/I/Storage/F Owner 批准接口前，它们仍为 CANDIDATE。
