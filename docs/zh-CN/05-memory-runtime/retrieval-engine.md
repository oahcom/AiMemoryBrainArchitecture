# Memory Retrieval Engine（记忆检索引擎）

- 文档 ID：F-RETRIEVAL-001
- 版本：1.0
- Owner：Session F — MR-01
- 源分支：session-f-memory-runtime
- 源 Blob：1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af
- 对应英文：[Memory Retrieval Engine](../../en/05-memory-runtime/retrieval-engine.md)
- 状态：安全语义已 DECIDED；Routing/Fusion 为 CANDIDATE；Scoring/Latency 为 TO_VALIDATE
- Phase 3.5 契约说明：D/E/I/G/H/C/B 候选契约已存在于各自 Owner Branch，并已为本次 Reprocessing 重新读取。F 消费这些类型化语义，但不冻结跨模块 Schema，也不声称实现已 Conform。

## 1. 目的

从异构表示中检索已授权、当前有效、带 Evidence 的 Memory Candidate。Retrieval 不等于 Vector Similarity，也不会自行激活 Context。

## 2. 范围

包括 Query Interpretation、Channel Routing、受 Scope 约束的 Candidate Generation、Canonical Revalidation、Hybrid Fusion、Deduplication、Evidence-aware Ranking、有界 Graph Expansion 和 Completeness Reporting。

不包括 Canonical Persistence/Lifecycle、Index Construction/Publication、Conflict Adjudication、Context Editing 和 Agent Planning。

## 3. 职责 / 非职责

Runtime 拥有执行计划和 Candidate Response。D 拥有 Memory/Version/Claim/Entity/Relation/Evidence Identity 及 Canonical Status。E 拥有 Compilation、Canonical Commit Publication 和 Index Projection。I 拥有 Identity/Authorization。Runtime 不能从 Index Metadata 推断授权，也不能解决 Disputed Claim。

## 4. 输入 / 输出

RecallQuery：Request/Schema ID、Trusted Principal、Purpose、Query Text 和 Structured Predicate、Required Scope/Environment/Task/Session、Time Window/Mode、Entity Ref/Mention、Relation Constraint、Channel Hint、Consistency Fence、Result/Candidate/Evidence Budget、Deadline/Cancellation 和 Runtime Config Version。

RetrievalResult：Result/Request ID、Candidate Ref、Completeness、Omission、按 Channel 的 Freshness、Canonical Fence、Policy Epoch、Timing 和 Warning。CandidateRef：memory_id、memory_version_id、claim_refs、match_channels、Per-channel Feature、Rank Explanation、Lifecycle/Epistemic/Validity、Provenance Ref 和 Evidence Summary。

## 5. 数据模型与 Channel 语义

| Channel | 适用场景 | 来源 | 强制保护 |
|---|---|---|---|
| Structured Field | 精确 ID、Type、Lifecycle、Scope、Validity、Tag | Canonical/Structured Index | Result Materialization 前执行 Authorized Scope Predicate |
| Entity | Canonical Entity ID、Alias、Identity-qualified Mention | Entity Projection/Resolver | Entity、Alias 和目标 Memory 分别执行 Scope 检查 |
| Full Text | 名称、稀有词、精确短语 | Inverted Index | 受控 Query Plan 内进行 Scope/Permission Pre-filter |
| Vector ANN | 改写表达和语义相似性 | Embedding Projection | Filter-aware ANN 或 Per-scope Partition；禁止 Global Top-K 后再 Filter |
| Graph/Relation | 类型化关系和邻域 | Relation Projection | 每一跳都授权每条 Edge 和 Target |
| Temporal | Valid-time、Event-time、Recency、Interval Overlap | Temporal Index/Canonical Field | Interval Candidate 暴露前执行 Scope Predicate |
| Provenance/Evidence | Support/Refutation、Lineage 和 Locator | Canonical Provenance/Evidence | 每次 Evidence/Source Dereference 独立授权 |

### Query Interpretation

规范化语法；提取显式 Filter；将时间表达解析为有界 Interval；通过已授权 Lookup 解析 Entity Mention；识别 Relation/Provenance 需求；分类 Intent。Query Text 是数据，不是 Scheduler/Authorization 指令。Entity Identity 有歧义时必须保持歧义，不得静默合并。

## 6. Scope-before-Candidate — INT-P0-02

**已 DECIDED 的硬性不变量。** 未授权记录不得成为 Fusion、Reranking、Count 或 Activation 使用的 Candidate。

执行步骤：
1. 认证 Principal，并通过 I 解析权威 Scope/Permission Envelope。
2. 根据已解析 Scope 和 Policy Epoch 构建 Trusted Scope Predicate。Caller 原始 Filter 不能授予访问权。
3. 在每个 Backend Query Boundary 内绑定 Predicate；必须在 ANN Traversal 结果输出、Lexical Hit Materialization、Structured Scan Output、Temporal Selection 或 Entity Resolution Output 之前执行。
4. Graph Traversal 在 Expansion 前 Filter Edge Visibility，并在入队前授权每个 Target；每一跳重复检查。
5. 只有已授权 Candidate ID 可以越过 Backend Adapter Boundary，进入 Runtime Candidate Buffer。
6. Ranking 前再次 Canonical Revalidation，重复 Authorization，并验证 Lifecycle/Forget/Version。
7. Cache Return 和 Final Serialization 前重新验证 Policy/Forget Epoch。

禁止：先执行 Global ANN Top-K，再在应用层 Filter。这会遗漏已授权邻居，并通过 Count、Timing、Score、Trace 或 Reranker Input 泄露信息。

如果 ANN 无法保证 Pre-filtering，则使用物理隔离的 Per-scope Index，或安全的 Scoped Exact/Alternate Path。如果两者都无法保证，该 Request 不得使用 ANN。绝不静默改成 Post-filter。

## 7. Candidate Generation 与 Routing

Exact ID/Structured Constraint → Structured；Entity ID/Mention → Entity + Structured；Quoted/Rare Term → Full Text；Paraphrase → ANN；Typed Relation/Path → Graph；When/After/Before/During/Currently → Temporal；Why/Source/Proof → Provenance/Evidence；Mixed Intent → Bounded Hybrid。

可选 Local Model Query Rewrite 为 CANDIDATE，绝非必需、绝不用于推导 Scope，其输出是不可信数据。默认 Routing 不依赖 LLM。

## 8. Fusion、Deduplication 与 Ranking

将已授权结果规范化为 (memory_id, memory_version_id)，保留 Channel Feature。只对完全相同的 Version Ref 去重；不得合并不同 Version、Claim 或 Conflict Alternative。Candidate Fusion 可采用 Reciprocal Rank Fusion 或 Calibrated Feature Fusion（CANDIDATE）；通过离线评估选择。不能假定原始 Channel Score 可直接比较。

Evidence-aware Ranking 保留 Positive/Negative/Qualifying Role、Source Diversity/Common Ancestry、Trust Label、Epistemic Status、Conflict Membership、Lifecycle、Valid-time、Provenance Completeness、Age/Freshness、Channel Feature 和 Uncertainty。Ranking 绝不把 Reported/Inferred/Disputed 升级为 Verified。Retracted/Forgotten Object 由 Canonical Authority 抑制。Superseded Version 只有在显式历史/冲突 Query 中才出现，并必须标记。

## 9. Early Stop 与 Completeness

Deadline/Budget 到达、Required Channel Sufficiency 达成，或边际收益低于基准阈值时，可以 Early Stop。阈值为 TO_VALIDATE。填满 Top-K 不代表完整。

候选 Completeness Enum：complete、partial、degraded、empty_complete、unavailable。必须包含 Omitted Channel、Reason、Channel Watermark、Candidate Budget Exhaustion、Evidence Truncation 和 Cancellation。不得将未授权匹配计数或披露为 Omission。

## 10. Scope / Permission

每个 Candidate-producing Adapter 内都必须执行 Scope Filter。Memory、Entity、Relation、Evidence、Provenance 和 Source Payload 的 Permission 分别适用。Query/Index Cache 不能绕过 Authorization。拒绝时不得披露受保护 ID、Count、Score 或存在性。

## 11. Version / Freshness 与 AR-004

Canonical Store 是权威；Index 是可重建 Projection。E 应按 Partition 发布可解释的 Commit Event Generation/Watermark；准确格式等待 E/I，仍为 OPEN。

对于所需 Canonical Snapshot/Read Position N：只能比较同一 Partition 的 IndexWatermark.applied_through CanonicalCommitCursor 与 N，并使用 D 的同 Authority Cursor 语义。如果 Watermark 覆盖 N，则该 Partition 可以满足 Projection Freshness，但仍需 Canonical/Lifecycle/Scope/Permission/Forget Revalidation。如果 Watermark 滞后或存在 Gap，则使用 D 支持的有界 Canonical Read-through/Delta、在 Deadline 内等待，或明确返回 Partial/Degraded/Unavailable。绝不能将不同 Partition 的 IndexWatermark 当作一个 Scalar 比较，也不能把任何 Watermark 当作 Forget Suppression/Completion Evidence。

出现分歧时，Canonical Status/Version/Forget 优先。Stale/Orphan Index Hit 必须抑制并排队修复。缺失 Index Entry 只能在所请求 Consistency 下明确标记 Partial/Stale 时作为 Omission。Rebuild 重放 Canonical Committed Event，并依据当前 Authority 排除 Forgotten/Retracted/Retention-ineligible Object。

## 12. Cache 语义

Query Cache Key 包含 Principal、Normalized Scope Set、Environment、Permission Epoch、Forget Epoch、Query Fingerprint、Retrieval Config 和 Index Watermark。Cached Payload 在使用前根据 Canonical Version/Lifecycle 和当前 Auth 重新验证。内部 ANN/Lexical Cache 必须分区，确保未授权记录不会影响可观察输出。Commit、Version/Lifecycle Change、Forget、Scope/Grant Change、Environment Closure 和 Generation Advance 都必须触发 Invalidation。

## 13. 故障处理

Channel Failure 相互隔离；只在 Budget 内幂等重试 Read。丢弃 Stale Hit；绝不回退到 Unscoped Query。Graph Timeout 返回有界 Partial Path。Evidence 不可用时返回 Ref/Status。如果 Canonical Status 不可用，就不能声称 Forget-safe Completeness：Fail-closed，或在 Strict Safety Mode 下返回 Unavailable。

## 14. 性能预算

限制 Channel 数量、每个 Channel Candidate 数、总 Candidate Buffer、Graph Depth/Fan-out、Canonical Revalidation Count、Evidence Ref/Bytes、Reranker Input 和 Wall-clock。数值均为 TO_VALIDATE。CPU 用于 Parsing/Fusion/Graph；RAM 用于有界 Buffer/Cache；Disk 用于 Structured/Lexical/Temporal Index；GPU 可选用于 Embedding/Reranking，默认 Recall 不依赖 GPU。

## 15. 可观测性

记录 Per-channel Latency、Authorized Candidate Count、Canonical Suppression、Stale Generation、Graph Node/Edge、Duplicate Rate、Evidence Bytes、Fusion Latency、Completeness Reason 和 Denial。普通日志不得包含未授权 Hit Count 或原始敏感 Query。

## 16. 接口

D：按 ID + Exact Version 进行 Canonical Get/Batch-get；Entity/Relation/Provenance/Evidence Read；Lifecycle/Validity/Current Forget State。

E：Index Adapter、Publication Generation/Watermark、Change Event、Replay/Rebuild Cursor。

I：Principal/Scope Resolution、Per-resource Authorization、Permission Epoch、Revocation/Forget Fence。

G：Immutable Candidate/Evidence/Recommendation Envelope，不修改 Context。

每个接口都需要 Schema Version、Correlation、Policy Epoch、Scope、Typed Error、Freshness 和 Partial Semantics。

## 17. 测试场景

Backend Test 断言 Scope Predicate 在 ANN Candidate ID 离开 Backend 前绑定；Full-text/Structured/Temporal 同样如此。独立拒绝 Graph Edge/Target。Reranker 只接收已授权 Candidate。Count/Error 不泄露禁止对象的存在。测试 Canonical/Index Race、Delayed Publication、Stale Watermark、Replay/Rebuild、Evidence 更严格 Scope、Revocation/Forget 后 Cache Hit、同一 Version 去重但保留 Conflict，以及 Partial Result 准确性。

## 18. 依赖与开放问题

D Canonical Schema/Lifecycle；E Index/Watermark；I Permission/Forget Authority；G Output Envelope；H Request/Auth Envelope。

OPEN：ANN 真正 Pre-filter Semantics、Watermark Granularity、Canonical Delta API、Claim Revision Identity（INT-P1-02）、Provenance Graph Constraint（INT-P1-06）。

TO_VALIDATE：RRF 与 Calibrated Fusion 的比较、Ranking Quality、Graph Budget、Scoped ANN Recall/Latency 和 Hardware Capacity。

## Phase 3.5 — 类型化 Cursor 与 Forget Suppression 补充（规范性补充）

详细 Owner/Consumer Contract 见 [Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract](../../governance/documentation-gaps.md)。本补充在冲突时取代本文更早的临时措辞。

### Typed Cursor Discipline

F 将以下 Owner-issued Type 作为不同类型消费和存储：D CanonicalCommitCursor（每个 Brain Authority 一个全局 Sequence）、D AggregateRevision（Per Aggregate）、D LifecycleEventCursor（Per Memory）、F IndexWatermark（Per Index/Channel Partition，Applied-through 为 D CanonicalCommitCursor）、D ForgetFenceGeneration/ForgetFenceCursor，以及 I PermissionEpoch。G ContextVersion 和 H/C Delivery/Capability/Request ID 也是独立 Namespace。

F 绝不对这些 Token 进行 Cast、Increment、Numeric Compare 或 Substitution。同一 Authority 的 CanonicalCommitCursor 连续性只能按 D 语义解释；AggregateRevision 和 LifecycleEventCursor 仍是局部 Scope。IndexWatermark 只代表单个 Partition 的连续 Freshness/Completeness 前缀，不是 Target Absence Evidence、Forget Suppression、Cache Purge 或 Global Forget Completion。

### Suppression Checkpoint

| Retrieval Stage | F 强制 Gate |
|---|---|
| Candidate Generation | 解析 Authenticated Principal、Trusted ScopeRefs、当前 I PermissionEpoch 和 D Fence；在每个 Backend 内绑定 Scope Predicate 后才输出 Candidate |
| Index Lookup | 查询 Scoped Partition；验证其自身 Watermark/Coverage/Schema；只使用准确 Version Ref；绝不 Global Top-K 后 Post-filter |
| Canonical Revalidation | 解析准确 Version、Lifecycle、Source Lineage 和最新适用 D Fence；分别授权 Memory、Entity、Relation、Evidence、Provenance |
| Fusion | 只接纳已授权且 Canonical-valid Candidate；仅对准确 Memory+Version 去重；保留 Conflict 和不同 Version |
| Freshness | 每个 Partition 独立对照 Required CanonicalCommitCursor 评估 Watermark；Lag 意味着 Read-through/Wait/Partial，不代表 Forget 失败或成功 |
| Reranking | 只有已验证 Candidate/Evidence 能进入 Reranker；Ranking 期间 Permission/Fence 改变时重新检查 |
| Result Materialization | 对准确字段和 Evidence Dereference 重新授权；Fence/Revocation 推进时丢弃受影响 Materialization |
| Final Return / G Handoff | Serialization/Disclosure 前立即重新验证当前 I Permission 和 D Fence；受影响结果取消/丢弃，顺序未知时 Fail-closed |

Fence/Revocation Notification 会取消受影响 In-flight Work 和 Cache Fill，但 Cancellation 本身不是安全证明。Final Return/Handoff 重新检查是强制要求。Request 无法建立当前 Authority State 时，不得披露受影响内容。

ActivationRecommendation 仍只是向 G 提交的 Proposal。它不修改 ContextVersion、不构成 Delivery，也不证明 Applied。

## Phase 3.5 Reprocessing — 当前依赖对齐

本节在与上文不一致时，取代过时的依赖存在性和临时 Cursor 表述。

- D 当前 Owner Decision：每个 BrainAuthority 一个全局有序 CanonicalCommitCursor；另有独立 Per-aggregate AggregateRevision、Per-Memory LifecycleEventCursor，以及单独的 ForgetFenceCursor/Generation。
- D 的 ProducerRegistrationSequence/HighWater 是另一种独立 Ledger Position，不是 Canonical Cursor、Forget Generation、PermissionEpoch 或 IndexWatermark。
- F 的 IndexWatermark 是 Per-index/Per-channel/Per-partition 连续 Applied-through CanonicalCommitCursor Position 的 Vector，并带有明确 Coverage/Schema Version 和 Gap State。
- I 的 PermissionEpoch 在其 Policy-domain/Issuer 内是不透明 Token。F 使用 I 的 Currentness/Authorization Operation，不与 D Token 比较。
- G 的 ContextVersion 属于单个 Context。Retrieval/ActivationRecommendation 对 G 保持只读。
- Candidate Generation 必须在每个 Backend 输出 Candidate 前绑定 Trusted Scope/Permission Filter。Index Hit 保持 Exact Ref，直到 Canonical Version、Lineage、Lifecycle、Current D Fence 和独立 I Authorization 检查全部成功。
- 即使发生 Cancellation 或先前已验证，Final Return/Handoff Checkpoint 仍是强制要求。无法建立当前 Authority Ordering 时，抑制受影响内容。

当前 Source Snapshot：D da8e5882d0b238d765d00b2225b79eea45a483b1；E c2f14408ba62447c11172d65b93a279fef96d175；I 5591ad3620ec3f5d74194bd79556dcf3e25bea07；G 3d2c065be863bc1d349faaeece6f6eaa0047abae；H 1ee65928f123d92a4758b0de09bc8d6df1e46253；C 35de58ddc93c5f1e554596cdfc430cd6c392d355；B 66adf6bdcf5ec69a146fe75afe20ce3b85af8448。
