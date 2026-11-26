---
document_metadata:
  domain: memory-runtime
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
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-082"
        - "source branch: session-f-memory-runtime"
        - "source commit: 1908ce4d233b20f7cafd00cb679affd01bd15174"
        - "original source blob: b7f5d85468f5262e472769a1991b812ac4a64f5b"
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
    source: "05-memory-runtime/activation-policy-engine.md"
    en: "docs/en/05-memory-runtime/activation-policy-engine.md"
    zh-CN: null
---

# Memory Activation Policy Engine（记忆激活策略引擎）

- 文档 ID：F-ACTIVATION-001
- 版本：1.0
- Owner：Session F — MR-02
- 源分支：session-f-memory-runtime
- 源 Blob：b7f5d85468f5262e472769a1991b812ac4a64f5b
- 对应英文：[Memory Activation Policy Engine](../../en/05-memory-runtime/activation-policy-engine.md)
- 状态：边界语义已 DECIDED；Policy Model 为 CANDIDATE；权重/阈值为 TO_VALIDATE

## 1. 目的

评估已授权的 Retrieval Memory Candidate 对当前 Task/Context 是否有用且安全，并判断应该立即提出、延后提出还是排除。这是为 G 提供的决策支持，不是 Context Editor，也不是 Agent Planner。

## 2. 范围

包括 Eligibility、Relevance/Utility Assessment、Risk-aware Recommendation、Rationale、Budget Estimate、Expiry/Refresh Hint，以及 Conflict/Evidence 保留。

不包括 Truth Adjudication、Canonical Lifecycle Change、Context Version Ownership、Final Prompt Assembly、Agent Planning 和 Tool Authorization。

## 3. 职责 / 非职责

Activation 区分四个维度：
1. **Existence：** Canonical Memory/Version 是否存在。
2. **Relevance：** 是否与当前 Task、Entity、Environment 或 Time 相关。
3. **Context Suitability：** 对当前 Context/Budget 来说是否安全、有用、有效，适合被提出。
4. **Urgency：** 立即提出、延后提出，还是要求显式 Recall。

Memory 可以存在但无关；相关但无效；有效但不适合注入；适合但不紧急。这些判断都不会改变 Canonical Truth。

## 4. 输入 / 输出

输入：已授权 CandidateMemory；Task/Environment/Session Signal；显式 Recall Purpose；G 提供的只读 Context Summary/Version Hint；Budget Hint；Policy/Config Version；Permission 和 Forget Epoch。

输出 ActivationRecommendation：Candidate/Version Ref；Decision（CANDIDATE：recommend_now、recommend_deferred、exclude、require_explicit_recall）；Reason Code 和各因素 Evidence；Urgency/Expiry/Refresh Hint；估算 Token/Byte Cost；未解决 Conflict/Evidence Warning；Policy Version 和 Freshness Timestamp。

G 可以接受、拒绝、转换、压缩或延后。Recommendation 不是 ContextEntry，也不是 Context Version。

## 5. 数据模型

ActivationFeatures：semantic_relevance；entity_match_strength；temporal_relevance/validity；decision_impact/task criticality；risk/sensitivity；context_coverage_gap；lifecycle eligibility；epistemic status；method-qualified confidence；source trust；evidence support/refute/qualify balance；provenance completeness；injection cost；freshness/index lag；duplicate/context-present state。

ActivationDecision：policy_id/version、candidate ref、outcome、reason list、feature snapshot、uncertainty、evaluated_at、expires_at、authorization/Forget epochs。

## 6. Routing / Decision Flow

    Authorized candidates
      -> canonical lifecycle, validity, permission and Forget hard gates
      -> semantic/entity/temporal relevance
      -> decision impact and Context coverage gap
      -> epistemic status, Evidence, trust and provenance
      -> risk, sensitivity and injection cost
      -> policy + budget
      -> recommend now / defer / explicit Recall / exclude

### 因素语义

- Semantic Relevance：相似性/词汇关系，不代表真伪。
- Entity Match：准确 Canonical Identity 的权重高于含糊的名称重叠（权重为 CANDIDATE）。
- Temporal Relevance：与请求/当前 Valid Interval 的重叠和新鲜度；Unknown 仍然保持 Unknown。
- Decision Impact：遗漏该记忆可能造成的预期后果；绝不代表 Authorization。
- Risk：Sensitivity、Harmfulness、Uncertainty、Conflict 和 Injection-risk Indicator。高风险可能需要显式 Review。
- Context Coverage Gap：G Context 是否已包含等价的有效信息；Runtime 只能看到已授权 Summary。
- Validity：来自 D/I 的 Lifecycle、Valid-time、Supersession 和 Forget State。
- Confidence、Trust 和 Evidence 相互独立；Confidence 不是真相，Trust 不是 Permission，Evidence 可以支持/反驳/限定。
- Injection Cost：Token/Byte/Distraction/Latency；低成本不能覆盖安全要求。

## 7. Policy Model 与权重

**DECIDED：** 任何加权分数都不能覆盖 Hard Eligibility Gate。

**CANDIDATE：** 两阶段模型：
1. Hard Gate：Authorization、Forget、Lifecycle、Valid-time、Evidence/Source Access 和 Prohibited-content Policy。
2. Soft Utility Rank：对符合资格的 Candidate，结合 Feature Vector、Task Class 和 Budget 排序。

可以评估 Linear Weighted Score、Learned Ranker 或 Rule Table。所有 Weight/Threshold 都是 CANDIDATE/TO_VALIDATE；没有带标签的 Task Evaluation，就没有规范性的数值权重。保留 Deterministic Baseline 和 Policy Version。默认不使用 LLM Activation，且 LLM 不能覆盖 Hard Gate。

## 8. INT-P0-04 Prompt Injection

Memory Text、Summary、Evidence Excerpt、Entity Label 和 Relation Qualifier 都是不可信数据。Activation 绝不把它们解释为 Command、Tool Request、Policy Change 或 Developer Instruction。保留 Source/Provenance、Source Type、Epistemic/Lifecycle State、Trust/Evidence Role、Sensitivity/Risk Flag 和 Untrusted-data Marker。

恶意 Memory 注入后仍可能影响 LLM；Runtime 无法保证模型服从。Runtime 能做的是不提升其权威性、最小化内容、隔离高风险 Candidate、附加 Provenance Label 并建议 Review。Tool/Action Authorization 仍由 Agent-side Policy 负责。Text Delimiter 不是安全边界。

## 9. Claim / Conflict — INT-P1-02

不得在冲突 Claim 中静默选择胜者。保留 ConflictSet Membership、Support/Refute Evidence、Temporal Applicability 和 Disputed/Retracted/Superseded State。

对于显式 Conflict Query，同时包含双方及紧凑 Evidence Summary。对于范围较窄的当前状态 Task，只有在 D Lifecycle Semantics 判定 Eligible 时，才可推荐当前且非 Disputed 的 View，同时保留 Conflict Marker。歧义具有实质影响时，Defer 或要求 Explicit Recall。

Runtime 不能裁定 Truth，也不能修改 Claim Status。Claim Revision Identity 和 ConflictSet Contract 仍等待 B/D/E，状态 OPEN。

## 10. Scope / Permission

只有已授权 Candidate 才能进入 Policy Evaluation。输出前重新检查 Permission/Forget Epoch。Evidence 的权限可能比 Memory 更严格；不可访问的 Evidence 应标记 Unavailable/Restricted，不能尝试获取。任何 Score 都不能授予访问权。

## 11. Version / Freshness

Recommendation 固定准确 Memory Version 和 Policy Version。如果在 Handoff 前 Canonical Version、Lifecycle、Valid-time、Policy、Permission Epoch 或 Forget Fence 改变，则标记 Stale 并重新评估。Expiry 只是 Hint，不是 Canonical TTL。G 在 Context Commit 前独立校验。

## 12. Cache 语义

Cache Deterministic Feature Computation，Key 包含 Candidate Version、Query/Task Fingerprint、Context Summary Version、Policy Version、Authorization Epoch、Forget Epoch 和 Temporal Time Bucket。

Canonical Version/Lifecycle、Evidence/Provenance Update、Context Version、Policy、Revocation、Forget 和 Environment/Task Change 都必须触发 Invalidation。绝不缓存最终 Context Decision。

## 13. 故障处理

缺少必需安全 Metadata：Fail-closed 或要求 Explicit Recall。可选 Feature Source 故障：只有 Policy 允许时才输出明确的 Uncertainty/Partial Feature Set。G 不可用：不能推断发生了 Context Mutation。未知 Policy Version：拒绝 Activation。

## 14. 性能预算

对 Candidate Feature 执行确定性、有界 CPU 工作。默认路径不进行同步大型 LLM 调用。限制 Candidate、Evidence Summary、Conflict Expansion 和 Token Estimation。可选 Model Classification 必须隔离、异步/Opt-in，状态 TO_VALIDATE；不能延迟 Hard Safety Check。

## 15. 可观测性

跟踪 Outcome、Feature Availability、Policy Version、Reason Code、Stale Rate、False Positive/Negative、Token Cost、Risk Exclusion、Conflict Preservation，以及 G 的 Accept/Reject Feedback。不得记录 Memory Text 或 Evidence Payload。

## 16. 接口

来自 Retrieval：准确 Candidate/Version、Match Feature、Completeness、Freshness、Lifecycle 和 Provenance Ref。

来自 D/I：Validity/Lifecycle、Epistemic Status、Trust Metadata、Current Forget/Permission。

来自 G：只读 Context Summary/Version 和 Budget Hint。

发往 G：ActivationRecommendation 和 Evidence-aware CandidateMemory，包含 Reason、Uncertainty、Version 和 Expiry。

在 G/D/E/I/H 审查前均为 Provisional；必须包含 Schema/Policy Version、Authorization/Forget Epoch 和 Typed Partial/Failure Semantics。

## 17. 测试场景

存在但不相关；相关但已过期；有效但 Disputed；适合但不紧急。高相似度不能覆盖 Scope/Forget/Retraction。Prompt Injection Text 始终是惰性数据。保留 Support 和 Refutation。不得混淆 Trust/Confidence/Relevance。避免重复 Context Version。Handoff 前 Policy/Permission 改变时重新评估。Model Feature 不可用但 Deterministic Path 仍可工作。G Reject 时 F 不产生 Context Mutation。

## 18. 依赖与开放问题

D Lifecycle/Claim/Conflict/Trust；E Freshness/Provenance Update Feed；G Context Summary/Budget/Acceptance；I Risk/Sensitivity Policy 和 Revocation；H Trusted Request Envelope。

OPEN：Policy Scope/Task Taxonomy、ConflictSet Shape、Evidence Rubric、G Context Sufficiency Signal。

TO_VALIDATE：Weight、Threshold、Utility Calibration、Risk Trade-off 和 Activation Benefit。
