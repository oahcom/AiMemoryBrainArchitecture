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
        - "original source blob: b7a948f014c3ad882a35a18bfc8ce025b26ab85a"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Existing ZH-CN mirror body retained; source Blob pin already matches; semantic parity review pending."
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
      - runtime
      - retrieval
      - activation
      - working-set
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "05-memory-runtime/runtime-overview.md"
    en: "docs/en/05-memory-runtime/runtime-overview.md"
    zh-CN: null
---
# Memory Runtime 总览

- 文档 ID：F-RUNTIME-OVERVIEW-001
- 版本：1.0
- Owner：Session F — Memory Runtime
- 源分支：session-f-memory-runtime
- 源 Blob：b7a948f014c3ad882a35a18bfc8ce025b26ab85a
- 对应英文：[Memory Runtime Overview](../../en/05-memory-runtime/runtime-overview.md)
- 状态：权威/安全边界已 DECIDED；拓扑为 CANDIDATE；数值预算为 TO_VALIDATE
- 基线：main at e443b23f8a179ad12c163722ad93bc646fd3a80a
- Phase 3.5 依赖审查：D/E/I/G/H/C/B Owner 分支契约已存在，并在 phase-3.5-forget-suppression-and-cursor-consumption.md 记录的精确 HEAD 上重新读取。F 的 Consumer Semantics 已 DECIDED；可调用的跨模块 Schema、Storage 实现和 Runtime Conformance 仍为 OPEN。本文不冻结 Wire Schema。

## 1. 目的

Memory Runtime 是 Brain 有界的在线读取/激活执行层。它解释 Recall、授权 Scope、在 Canonical/Derived Representation 之间路由检索、生成带 Evidence 的候选、提出 Activation Recommendation，并维护可丢弃的 Working Set/Cache。

它不是 Agent Runtime、Planner、Tool Executor、Canonical Store、Compiler 或 Context Version Authority。默认 Recall 是确定性的，不会同步调用大型 LLM。

## 2. 范围

拥有 Runtime Session Lifecycle、请求级执行状态、Query Interpretation/Routing、Scope-filtered Retrieval、Candidate Fusion/Dedup/Ranking、Completeness/Freshness Semantics、Activation Recommendation、有界 Working Set/Cache、Scheduling/Admission/Cancellation 和 Read-path Freshness Check。

不拥有 Canonical Memory/Claim/Entity/Relation Identity、Version、Lifecycle 或权威 Forget State（D）；Compilation、Canonical Commit 或 Index Publication（E）；ContextEntry Mutation 或 Context Version（G）；Permission Policy/Global Retention/Audit（I）；Agent Planning、Action Selection、Tool Authorization 或 Prompt Policy。

## 3. 职责 / 非职责

Runtime 选择哪些已授权 Memory 是有用的 Candidate，并提出 Activation Recommendation。它不能判断 Claim 是否真实、解决 ConflictSet、提升 Claim，或宣布 Memory 已 Forgotten。它为 G 保留 Disputed/Retracted/Superseded 状态。Canonical Memory 是权威；Index、Cache 和 Working Set 都是可丢弃 Projection。结果引用准确的 Canonical Memory Version，不创建 Memory。

## 4. 输入 / 输出

输入：来自 I/H 的已认证 Principal 和已解析 Scope Context；Recall Request（Query Text/Structured Filter、Purpose、Target Context Hint、Task/Session/Environment Ref、Result/Evidence Budget、Consistency Requirement、Deadline/Cancellation）；作为不可信 Relevance Signal 的 Agent Telemetry；D Canonical Metadata 和已授权 Evidence；E Commit Event、Index Publication 和 Watermark；Policy/Configuration Version 与 Resource Limit。

输出给 G/Caller：RetrievalResult（Request ID、Candidate、Completeness、Freshness Vector、Warning/Timing）；CandidateMemory（Memory ID + 不可变 Version ID、Canonical Ref、Match Channel、Score Feature、Lifecycle/Epistemic State、Validity、Provenance Ref 和 Evidence Summary）；ActivationRecommendation（include/defer/exclude、Reason Code、Urgency/Expiry Hint 和 Budget Estimate）；明确的 Uncertainty/Conflict/Retraction/Evidence Unavailable Marker。任何输出都不会创建或推进 Context Version。

## 5. 数据模型

RuntimeSession 绑定不透明 Session ID、已认证 Principal、Agent/Instance、User/Project/Agent/Task/Session/Environment Scope、Permission Epoch/Policy Version、Generation/Cancellation State、有界 Working Set、Quota 和 Expiry。它不是 Agent Planning State，也不是 Memory Context。

RecallRequest 在 Admission 后不可变。RetrievalResult 是不可变响应快照。Candidate Ref 指向准确 Memory Version。WorkingSetEntry 是带 Invalidation Metadata 的有界 Projection/Reference。

## 6. Routing / Scheduling

将 Query 分类为 Structured Lookup、Entity-centric、Lexical、Semantic、Temporal、Relation Traversal、Provenance Expansion 或 Hybrid。根据 Query Feature 和显式 Filter 选择确定性 Channel。在 Request Budget 内并行执行。限制 Graph/Evidence 工作。默认路径不需要 LLM；可选 Query Rewrite 为 CANDIDATE，默认禁用，且绝不用于授权判断。

## 7. 请求顺序

    Agent/Adapter -> Runtime: Recall(query, scopes, purpose, budgets)
    Runtime -> I: authenticate, resolve scopes, authorize
    I -> Runtime: principal + policy/permission epoch
    Runtime -> D: current canonical/Forget fence
    Runtime -> E: scope-constrained channel queries
    E -> Runtime: authorized candidate refs + index watermarks
    Runtime -> D/I: revalidate candidate version, lifecycle, Forget and permissions
    Runtime: fuse -> deduplicate -> rank -> completeness -> activation
    Runtime -> Agent/Adapter: RetrievalResult + ActivationRecommendation
    Agent/Adapter -> G: optional proposal; G alone decides Context Version

决策流程：Authenticate/Authorize → Resolve Trusted Scope → 每个 Candidate Generator 前应用 Scope Predicate → 并行 Channel → Canonical/Forget Validation → Fusion/Ranking → Activation → 明确返回 Completeness/Freshness。

## 8. 不变量

1. **Scope-before-Candidate（INT-P0-02）：** 未授权对象不得进入 Candidate Collection、Fusion、Reranker、Count、Cache Response 或 Working Set。
2. Graph Traversal/Retention 前必须独立授权每条 Edge 和 Target Node。
3. Canonical Status 和 Forget Fence 优先于所有 Derived Projection。
4. Permission Revocation 必须在披露前使 Cache 和 In-flight Result 失效或阻断。
5. Memory Content 是不可信数据，绝不是可执行指令（INT-P0-04）。
6. RetrievalResult 不是 ContextEntry，也不拥有 Context Version（INT-P1-01）。
7. 保留 Conflict、Disputed、Retracted、Superseded 状态；Runtime 不裁定（INT-P1-02）。
8. Provenance/Evidence 必须独立授权并纳入 Budget（INT-P1-06）。
9. Partial Result 绝不能静默标记为 Complete。
10. Working Set/Cache/Index 绝不是 Canonical Authority。

## 9. Scope / Permission

Scope 是 Namespace/Applicability；Permission 是 Operation Authorization。二者都必需。Trusted Identity/Scope 由 I/H 解析，不能从 Query Text、Display Name 或 Agent 提供的 Label 推断。在 Ingress、每个 Channel、每条 Graph Edge/Target、Evidence Dereference、Cache Return、Serialization，以及 Epoch 改变后的 G Handoff 时检查。Authorization Service 故障时 Fail-closed。

## 10. Version / Freshness

每个 Candidate 携带 Memory ID、准确 Memory Version ID、Canonical Status/Version，以及可用时的 Source Generation。每个 Index Channel 返回 Watermark/Generation。Freshness 必须按 Channel/Candidate 表示，不能用一个误导性的 Boolean。

如果 E Publication 落后于 Canonical Commit：在有界范围内通过 Canonical Delta/Read-through 满足所需 Fence，或在 Deadline 内等待；否则明确返回 Partial/Stale，并附 Observed/Required Generation。低于 Fence 的 Index 不得声称完整。Canonical State 始终是权威。

## 11. Cache 语义

Cache Key 包含 Authenticated Principal、Normalized Scope Set、Environment、Permission Epoch/Policy Version、Query Fingerprint、Retrieval Config Version、Index Generation/Freshness Fence 和 Canonical/Forget Epoch。Cache Hit 在披露前重新验证 Revocation/Forget 和 Canonical Version。默认不缓存敏感 Evidence Payload。

## 12. 故障处理

Auth/Policy 不可用：Fail-closed。Canonical Store 不可用：不得依赖仅 Index 结果来保证 Lifecycle/Forget。Index 不可用：有界、安全地回退 Canonical，或明确标记 Partial/Unavailable。Channel Timeout：返回带 Omission 的 Partial。Cancellation：停止 Fan-out，并阻止迟到结果插入。Version Mismatch：有限重试/丢弃，或标记 Stale。Evidence 不可用：保留 Ref/Status，绝不伪造 Excerpt。

## 13. 性能预算

对 Admission、Authorization、Canonical Validation、Per-channel Search、Graph Fan-out、Fusion/Ranking、Evidence Expansion 和 Serialization 分别设预算。限制 Candidate Count、Graph Depth/Fan-out、Evidence Bytes 和 Wall-clock。数值阈值必须在声明的 CPU/RAM/Disk/GPU 与代表性 Corpus 上 TO_VALIDATE。不得宣称固定 P95/P99。

## 14. 可观测性

跟踪 Request → Auth Checkpoint → Channel Span → Canonical Revalidation → Fusion/Rank → Activation → G Handoff。记录 Channel Latency、Authorized Candidate Count、Stale Suppression、Watermark、Partial Reason、Cache Hit/Miss、Invalidation、Cancellation 和 Saturation。避免记录原始 Query/Evidence，并避免高基数 Metric Label。

## 15. 接口

D → F：按 ID/准确 Version 进行 Canonical Read；Typed Ref；Lifecycle/Epistemic/Validity；已授权 Evidence/Provenance Dereference。

E → F：Canonical Commit Event、Projection Publication、Index Watermark、Forget/Retraction Feed。

I → F：Authenticated Principal、Scope Resolution、Permission Decision/Epoch、Revocation 和 Forget Fence。

F → G：RetrievalResult、CandidateMemory、ActivationRecommendation、EvidenceSummary、Completeness、Freshness、Memory Version 和 Reason Code。

在 D/E/G/H/I 审查前，以上接口均为 Provisional。每个接口都需要 Schema Version、Correlation ID、Auth Context、Typed Error、Retryability、Freshness 和 Partial Semantics。

## 16. 测试场景

跨 User/Agent/Instance/Task/Environment 的负向 Recall；断言 Scope Predicate 在 ANN/Lexical/Graph Candidate Materialization 前执行；未授权 Graph Target；Channel 完成到 Serialization 之间发生 Revocation；Query 期间发生 Forget；Watermark 滞后；Disputed/Retracted/Superseded State；Evidence 权限严于 Memory；Prompt Injection 内容保持惰性；Channel Timeout/Cancellation 绝不产生虚假的 Completeness。

## 17. 依赖

D Canonical Schema/Lifecycle；E Canonical Commit/Index Publication/Watermark；G Context Contract；H Authenticated Protocol；I Identity、Scope、Permission、Revocation 和 Forget；Storage/Observability Infrastructure。

## 18. 开放问题

OPEN：D Canonical Read/Lifecycle Snapshot Consistency；E Watermark Granularity/Replay Ordering；I Permission Epoch/Revocation SLA；G Candidate/Evidence Payload；H Request Envelope。CANDIDATE：Modular Monolith Task Group。TO_VALIDATE：Routing Quality、Channel Budget、Cache Benefit 和 Local Hardware Limit。

## Phase 3.5 — Forget 与 Cursor 集成

规范性 F Consumer Matrix、Retrieval-stage Suppression Matrix、Cache/Working Set Invalidation Contract、Index Rebuild Contract 和十项 Conformance Specification 维护于 [phase-3.5-forget-suppression-and-cursor-consumption.md](../../governance/documentation-gaps.md)。

Runtime 将 D 的 Per-authority Global CanonicalCommitCursor、Per-aggregate AggregateRevision、Per-Memory LifecycleEventCursor 和 ForgetFenceGeneration 作为独立类型消费；F 拥有 Per-index/Per-partition IndexWatermark；I 拥有 PermissionEpoch；G 拥有 ContextVersion。这些值不可互换。IndexWatermark 只证明连续 Projection Freshness，绝不证明 Forget 完成。

Retrieval 在 Candidate Generation、Index Lookup、Canonical Validation、Fusion、Freshness、Reranking、Materialization 和最终返回时，执行 Scope、当前 Permission 和最新适用 Forget Fence 检查。Cache Hit/Working Set Reuse 也必须重新授权。Fence/Revocation 推进时取消受影响的 In-flight Work；最终披露仍要求权威复核。

F 的 Index Rebuild/Backfill/Replay 属于可产生派生物的 Work：必须依据 D Producer Registration Contract 在 Admission 前登记；重放连续 Canonical Commit Prefix；排除 Fence 覆盖的 Lineage；使用权威 Final Publication Gate。如果 D/E/Storage Gate 不可用或状态未决，必须将 Staged Generation 保持为 Private/Quarantined。

ActivationRecommendation 仅供建议。只有 G 能决定 Context Mutation 和 ContextVersion；H/C 拥有 Adapter/Final-request Evidence。F 不声称 Applied、Global Forget Completion 或 Physical Erasure。

## 19. Phase 3.5 Reprocessing — Runtime 权威检查点

- Request Admission 绑定已认证 Principal、可信 Ownership/Applicability ScopeRefs、Purpose、I PermissionEpoch（按 Policy Domain/Issuer 限定）和当前 D ForgetFence。Query Text 和 Payload 中提供的 ActorRef/ScopeRef/Producer Label 不具有权威性。
- 每个 Candidate-producing Adapter 在 Candidate 输出前执行 Scope/Permission。每个准确 Hit 都要重新验证 MemoryVersion、相关 AggregateRevision、LifecycleEventCursor、Source Lineage、D Fence Coverage，以及 Memory/Entity/Relation/Evidence/Provenance 的独立授权。
- 只有重新验证的 Candidate 才能进入 Fusion/Reranking/Materialization。任何 Epoch/Fence 变化或无法验证的排序都必须触发 Cancellation + Suppression；Cancellation 本身不是安全证明。
- Final Response Serialization 和 G Handoff 都要执行当前 D Fence 和 I Authorization Checkpoint。无法建立当前权威状态时，不披露受影响内容。
- Freshness 是 Per-index/Per-partition Vector。每个 IndexWatermark 表示该 Partition 已应用的 D CanonicalCommitCursor 连续前缀，并带有明确 Coverage/Schema Version；一个 Partition 的滞后不能被另一个掩盖。它绝不证明 Target 不存在、Forget 完成或 Physical Erasure。
- F ActivationRecommendation 不可变且仅供建议。G 独自校验并修改 Context/ContextVersion；H/C 拥有 Adapter/Final-request Evidence。F 永不声称 Applied。

Reprocessing Source Heads：D da8e5882d0b238d765d00b2225b79eea45a483b1；E c2f14408ba62447c11172d65b93a279fef96d175；I 5591ad3620ec3f5d74194bd79556dcf3e25bea07；G 3d2c065be863bc1d349faaeece6f6eaa0047abae；H 1ee65928f123d92a4758b0de09bc8d6df1e46253；C 35de58ddc93c5f1e554596cdfc430cd6c392d355；B 66adf6bdcf5ec69a146fe75afe20ce3b85af8448。
