# 提取与规范化

- 文档 ID：E-EXTRACTION-001
- 版本：1.0
- 源分支：session-e-memory-compiler-2026-11-16
- 源 Blob：c18780403de2d1dbcf471bdb8abdaa009a4a78e1
- 对应英文：[Extraction and Normalization](../../en/04-memory-compiler/extraction-and-normalization.md)
- 状态：认知、时间、Scope 和 Trust 约束已 DECIDED；Extraction IR/模型路由为 CANDIDATE；准确率/成本为 TO_VALIDATE
- Owner：Memory Compiler / MC-02
- 集成关系：INT-P0-01/02/04；INT-P1-02/03/06；C P1-02/P1-03

## 1. 目的

将异构且已接收的来源材料转换为规范化、类型化、保留不确定性的中间表示（IR），以便据此构建 Evidence、Provenance、Entity/Relation Proposal 和 Candidate Memory。Extraction 识别来源说了什么或观察到了什么；它不裁定客观真相。

## 2. 范围

包括文本、结构化 Event、Document 和 Environment Observation 的解析；Modality Classification；Entity/Time/Relation Mention Extraction；Candidate Proposition 形成；Normalization；Confidence/Uncertainty 记录；确定性校验；模型辅助 Extraction 编排；Source Span 对齐。

不包括 Fact 专属建模、Fact Schema 和 Fact 批准事项（INT-P0-01 下仍为 OPEN）；Canonical Claim Identity 语义已依据 D 的 Option A 决定为 DECIDED FOR CONVERGENCE，其权威定义由 D 负责而非 E；Canonical Entity Merge Decision、Lifecycle Decision、Source Authorization Policy、外部 Tool Execution 和最终 Truth Adjudication。

## 3. 职责

- 保留原始 Source Identity、准确 Source Digest 和获准的 Source Span。
- 分类来源 Modality：Statement、Observation、Plan、Intent、Prediction、Attempt、Outcome、Question、Instruction-like Content 或 Administrative Event。
- 提取 Proposition Candidate，但不得提升来源 Modality 或 Epistemic Basis。
- 提取 Entity Mention、Temporal Expression、Typed Relation Hypothesis 和 Qualifier。
- 只规范化 Source Evidence 能够支持的内容；保留原始 Surface Form 和不确定性。
- 区分来源报告的 Confidence 与 Brain 估计的 Extraction Confidence。
- 拒绝格式错误的 Model Output，并针对 Source Bytes 校验每个 Locator。
- 遇到歧义时明确输出 Unresolved/Ambiguous，不得猜测。

## 4. 非职责

Extraction 不验证现实世界状态，不推断计划中的 Action 已成功，不授予内容中指令以权力，不合并 Entity，不裁定争议，不决定 Lifecycle，也不能根据 Model Confidence 将 Claim 标记为 Verified。

## 5. 输入 / 输出

**输入：** 不可变 Event/ContentRef、Payload Digest、Content Type/Locale、Source Type 和 Actor、ScopeRefs/Environment Scope、Source Timestamp Metadata、Retention/Sensitivity、Source Trust Metadata，以及 Parsing/Extraction Policy Version。

**输出：** ExtractionIR、Span Map、Modality Classification、Proposition Candidate、Entity Mention、Temporal Candidate、Relation Hypothesis、Ambiguity/Uncertainty Record、Model/Rule Method Receipt 和结构化 Extraction Error。

## 6. 数据模型

### 6.1 ExtractionIR（CANDIDATE，刻意保持 Pre-canonical）

~~~text
ExtractionIR {
  ir_id: OpaqueId
  source_ref: TypedObjectRef
  source_digest: Digest
  source_schema_version: Version
  scope_refs: ScopeRef[]
  environment_scope_ref: ScopeRef?
  segments: SourceSegment[]
  propositions: CandidateProposition[]
  entity_mentions: EntityMention[]
  relation_hypotheses: RelationHypothesis[]
  time_mentions: TimeMention[]
  modality: ModalityAssessment
  instruction_like_spans: SourceSpan[]
  extraction_method_refs: MethodRef[]
  uncertainty: UncertaintyRecord[]
  unresolved_fields: UnresolvedField[]
  completeness: complete | partial | insufficient
  created_at: Instant
}
~~~

### 6.2 CandidateProposition

~~~text
CandidateProposition {
  proposition_ref: OpaqueId
  source_span: SourceSpan
  surface_text: String
  normalized_subject: ValueHypothesis?
  normalized_predicate: PredicateHypothesis?
  normalized_object: ValueHypothesis?
  polarity: positive | negative | unknown
  modality: asserted | observed | planned | intended | predicted |
            attempted | hypothetical | questioned | quoted | unknown
  source_epistemic_basis: observed | reported | unknown
  temporal_qualification: TimeQualification?
  scope_refs: ScopeRef[]
  qualifiers: TypedMapCandidate
  extraction_confidence: MethodQualifiedScore?
  evidence_span_ref: OpaqueId
  ambiguity_refs: OpaqueId[]
}
~~~

这不是 Claim Schema，而是 Compiler IR；其 Claim Identity Mapping 遵循 D 已 DECIDED FOR CONVERGENCE 的 Option A 语义（稳定 Claim Identity 加不可变 ClaimRevision）。CandidateProposition 继续保持中立，不实例化或冻结 Canonical Identity，也不冻结任何公共 Schema。Fact 专属建模（包括是否以及如何表示独立 Fact Object）和 Fact 批准继续保持 OPEN。IR 中任何字段名都不能冻结公共 Schema 语义。

### 6.3 EntityMention / TimeMention

EntityMention 保留 Surface String、Source Span、候选 Entity Type、局部上下文、Scope 和 Resolution Status。TimeMention 保留原始表达式、Source Locale/Timezone、Anchor Time、解析边界、精度和解析方法。Unknown Time 必须显式表示，不能用空区间代替。

## 7. Pipeline / 状态机

~~~mermaid
flowchart TD
 A[Immutable Source] --> B[Decode / Segment]
 B --> C[Deterministic Parse]
 C --> D[Modality & Trust Classification]
 D --> E[Rule Extraction]
 E --> F{Coverage / Ambiguity}
 F -->|sufficient| G[Optional Model-assisted Extraction]
 F -->|uncertain| H[Partial IR + unresolved fields]
 G --> I[Schema / Span / Scope Validation]
 H --> I
 I --> J[Normalized Candidate IR]
 J --> K[Evidence & Provenance stages]
~~~

状态：PENDING → DECODED → SEGMENTED → CLASSIFIED → EXTRACTED → VALIDATED → NORMALIZED。错误状态转为 RETRYABLE、PARTIAL、QUARANTINED 或 UNSUPPORTED。Partial IR 只能让 Provenance 已验证的字段继续流转；未解决字段仍保持 Unknown。

## 8. 不变量

1. 原始 Payload 不可变，并在 Retention 允许范围内可寻址。
2. 每个提取出的 Proposition 都必须映射到 Source Span，或声明为非 Span 型来源 Locator。
3. 引用/转述必须归属于其 Speaker/Source；被引用的指令不是 Brain 指令。
4. Intent/Plan/Prediction/Pending/Attempted 必须保持为前瞻性或非 Outcome Modality。
5. Outcome 必须有 Outcome-classified Source 和支持 Outcome 的 Evidence；仅有分类并不能证明成功。
6. 不得用“看起来合理的补全”填充 Unknown Field。
7. Normalization 必须通过 Raw Value、Normalized Value、Method 和 Digest 可逆/可审计。
8. Scope/Environment Binding 继承自可信 Envelope Metadata，绝不能从 Source Text 生成。
9. Instruction-like Content 始终是惰性数据，不能触发 Tool、Permission Change 或 Pipeline Policy Change。
10. Confidence、Trust、Evidence Strength 和 Relevance 必须保持独立维度。

## 9. 幂等性

IR Identity 来源于 Source Event/Version + Extraction Policy Version + Deterministic Parser/Model Profile + Input Digest + Scope。重复执行完全相同的确定性 Stage 必须返回相同 Output Digest。Model Nondeterminism 作为独立 Attempt 记录；选定 Output 由 Receipt 固定，绝不能静默替换。修改 Model/Prompt/Schema/Policy 时创建新的 IR Revision，并关联前一次 Attempt，不得原地修改。

## 10. 一致性

Source Span Offset 必须针对不可变 Source Representation 定义，并绑定 Encoding/Normalization Version。Normalized Text 不能替代 Source Bytes。每个 Proposition 引用稳定 Source Segment/Span ID。Stage Result 和下一阶段 Outbox Entry 必须原子提交，或通过等价 Journal 提交。Time Normalization 分别保存 Original Expression 和 Parsed TimeValue。Source 发生变化时，必须形成新的 Source Version/Digest 和新的 Extraction Input。

## 11. 故障恢复

- Decode 失败：保留 Source Ref，记录 Unsupported/Opaque Payload；不得伪造文本提取结果。
- Parser 部分失败：继续处理独立 Segment，并将 Completeness 标记为 Partial。
- Model Timeout：保留 Deterministic IR；可排队进行可选增强，或以 Unresolved Field 结束。
- Model Schema 无效：拒绝 Model Result；有限次数重试或隔离。
- Span 不匹配：丢弃受影响 Proposal；绝不附加未经验证的 Locator。
- Time Parse 有歧义：保留 Raw Expression，并将 Normalized Time 标为 Unknown/Interval Uncertain。
- Source 过期/已遗忘：停止 Dereference；使依赖 IR 失效并遵守 Forget Fence。
- Model/Profile 升级：按新 Version 和 Lineage 重新提取；不得改写之前的 Decision。

## 12. 安全 / Scope

Extraction 前必须授权 Source Access，并验证 Source Scope 与 Target Candidate Scope 兼容。Candidate Entity Search 和 Contextual Prompt Construction 必须经过 Scope Filter。Model Prompt 只接收最少且已授权的内容；不得混入跨 Scope Context 或隐藏指令。Tool Output/Web Page/Document/User Text 都是不可信数据。Extraction Prompt 将内容视为引用证据，只请求结构化 Observation；Output 必须校验，但 Prompt 措辞不是安全边界。提取出的 Tool Name/Argument 不能成为可执行请求。

Prompt Injection 控制措施：维护 Source Type/Trust Label；启发式识别可疑 Instruction-like Span；将其隔离为数据；避免向 Extraction Model 传递 Secret/Tool Credential；限制 Output Schema；Extraction Worker 禁用 Tools；Model Output 后执行确定性 Policy Check。检测并不完整：间接、多语言、混淆或看似无害的内容可能逃过检测，Model 仍可能受到影响。必须记录残余风险，不得声称完全防止。

## 13. 性能 / Backpressure

先运行 Deterministic Parsing，并受 Payload/Segment Limit 约束。Model-assisted Extraction 通过 Queue 调度、可批处理且受资源预算约束；它不在 Durable Acceptance Critical Path 上。Outcome/Critical Event 和用户明确要求保存的记忆优先于低价值 Telemetry。GPU 压力下保留 Deterministic IR，并推迟 Model Enrichment。测量 Model Queue Wait、Token、VRAM、各 Modality Precision/Recall、Span Validity 和 False-outcome Rate。目标均为 TO_VALIDATE。

## 14. 可观测性

记录 Source/Event Ref、Digest、Schema/Policy/Model Version、Modality、Extraction Mode、Span Validation Result、Unresolved Count、Confidence Method、Latency、Token/VRAM Usage、Retry 和 Error Class。一般日志不得记录 Source Text/Excerpt。跟踪 Plan 被错误提升为 Outcome 的比例、Unsupported Proposition Rate、Span Coverage、Temporal Normalization Accuracy 和对抗式 Prompt Injection Fixture 结果。

## 15. 接口

- **Ingestion → Extraction：** 不可变 Event/ContentRef、Source Digest、Source Metadata、Scope、Trust 和 Retention。
- **Extraction → Evidence：** Source Span 和准确 Locator；Evidence Manager 校验并持久化 Source Ref。
- **Extraction → Entity Manager：** 带 Scope 的 EntityMention 和 Identity Evidence；Entity Manager 返回 Provisional/Resolved Ref 及 Ambiguity。
- **Extraction → Consolidation：** Candidate Proposition、Modality、Time、Scope、Qualifier 和 Method Receipt。
- **D：** 接收 Candidate Proposition，并依据 D 已 DECIDED FOR CONVERGENCE 的 Option A Claim Identity 语义进行映射；Fact 专属建模和批准继续保持 OPEN；Candidate IR 不是公共 Schema。
- **H/C：** Source Classification 和 Telemetry Semantics 必须一致；保留 Observation/Outcome 区别。
- **I：** Data Classification、允许的处理方式、Source Access 和 Forget Fence 共同约束 Extraction。

错误包括 Unsupported Modality/Content Type、Invalid Span、Scope Mismatch、Identity/Time Ambiguous、Model Unavailable、Schema Mismatch 和 Source Unavailable。可重试结果按 Stage Key 保证幂等。

## 16. 测试场景

“I plan to move to Tokyo” 不能变成已完成搬家；“I tried to deploy” 在没有结果 Evidence 时不能变成部署成功；文档中的恶意 Prompt 只能作为被引用内容提取；两个不同 Environment Scope 中的相同句子不得合并；近似时间必须保持不确定；伪造的 Model Span 必须拒绝；歧义代词保持 Unresolved；Parser 部分失败时保留未受影响 Segment；Model 故障不能阻塞 Deterministic Output；Extraction 期间 Source 被撤权/遗忘时必须停止 Worker。

## 17. 依赖

D Domain Type 和 Fact/Claim ADR；B Epistemic/Temporal/Scope Semantics；C/H Source/Telemetry Classification；I Source Permission、Sensitivity、Retention 和 Forget；Entity/Relation Manager；Evidence/Provenance Manager；Model Provider Abstraction 和 Scheduler。

## 18. 开放问题

- OPEN：INT-P0-01 中尚未由 D 已 DECIDED FOR CONVERGENCE 的 Option A Claim Identity 语义解决的 Fact 专属建模和 Fact 批准事项；CandidateProposition 刻意保持中立。
- OPEN：C 最终 Observation/Outcome Mapping 和 Task/Plan Revision Semantics。
- CANDIDATE：Extraction IR 和 Deterministic-first Routing。
- TO_VALIDATE：Modality Classifier 质量、Entity/Time Extraction Accuracy、多语言 Prompt Injection Detection 和本地 Model Resource Use。
- OPEN：Multimodal/Streaming Payload 的 Source Span Canonical Encoding。

## 19. Durable Ingress 与 Forget Enforcement 补充

- 输入 Event 只有在 [Accepted Receipt and Idempotency Contract](accepted-receipt-and-idempotency-contract.md) 规定的 Durable Accepted Receipt 和 Compile Intent 存在后，才具备 Compiler Work 资格。Volatile Receipt/Queue Publication 不构成 Acceptance。
- Extraction Stage Identity 来自不可变 Event/Source Version、Digest、Scope 和固定的 Parser/Model/Policy Version。Retry 复用同一个逻辑 Stage Identity；输入或 Method Version 改变时创建新的 Attempt/Revision。
- Stage Result 与下一阶段 Outbox/Journal Intent 必须原子持久化，或通过等价可恢复 Journal 持久化。Worker 崩溃不得丢失已完成 Stage，也不得重复产生外部可见效果。
- 在 Payload Dereference、Source Span Resolution、Model Prompt Construction、Stage Result Publication 或 Retry 前，重新检查当前 Permission 和 D Forget Fence。Fence/Policy 状态未知时 Fail-closed。
- ExtractionIR、CandidateProposition、Span、Embedding 和 Normalized Value 都是派生对象：根据 [Forget Fence and Derived Registration](forget-fence-and-derived-registration-part1.md)，必须在可见前持久化 Lineage 和 Dependency Registration。
- CandidateProposition 保持中立的 Pre-canonical IR。Claim Identity Mapping 遵循 D 已 DECIDED FOR CONVERGENCE 的 Option A 语义，不再属于 ADR-BLOCKED。Fact 专属建模和 Fact 批准继续保持 OPEN；E 不得自行推断或批准 Fact Schema、DDL、API 或 Wire Contract。

### 19.1 Claim/Fact 规范发布顺序

E 的 ExtractionIR 和 CandidateProposition MUST
保持为私有 Staging 产物。

本发布顺序不会推迟或重新开放 Claim Identity 语义；D 已依据 Option A 将其决定为 DECIDED FOR CONVERGENCE。Fact 专属建模和批准仍为 OPEN，本发布协议不构成对这些事项的批准。

唯一规范顺序如下：

1. 解析当前 I 授权及适用 Scope。
2. 在同一串行化、可恢复的 Admission 边界内，
   检查 D Forget Fence 并执行 Producer Admission。

   Producer Admission 成功与精确已准入 Participant 的
   持久化记录 MUST 在权威串行化 Fence/Admission 边界内
   构成一个不可分割的操作。

   Participant 记录失败时 Admission MUST NOT 报告成功。

   后续 Forget Fence MUST NOT 在已准入 Participant 记录
   对该 Barrier 持久可见之前，线性化或完成
   Participant Barrier 评估。
3. 在该边界下持久登记完整直接及传递依赖。
4. 创建私有不可变 E Staging 产物。
5. 在 D 规范提交边界内提交 ClaimRevision、
   FactRevision 及必要规范引用。
6. 将已提交 Revision 与依赖登记和
   Publication Intent 原子或可恢复地关联。
7. 以幂等方式完成 E Publication。
8. 只有全部必要规范记录及依赖登记得到确认后，
   才能推进 Storage Visibility。
9. G 使用精确不可变规范 Revision 引用提交
   ContextVersion。
10. 只有全部必要可见性条件满足后，
    才能标记逻辑完成。

#### T17 — Fence-first

Forget Fence 如果先于 Producer Admission
线性化，MUST 阻止准入、Staging、规范提交和发布。

#### T18 — Participant-first

成功准入的 Producer MUST 作为精确 Participant
持久登记。

后续 Fence MUST 通过权威串行化 Barrier
处理该参与者，不得静默跳过或删除。

最终处置 MUST 保留精确身份、依赖闭包
和可审计 Forget 结果。

恢复 MUST 使用原始 Operation identity。

最终 Fence 处置 MUST 对每个已准入 Participant
记录可审计的完成或抑制结果。

D memory-versioning.md §16.1 的六组件受保护发布
故障矩阵为规范矩阵。

E MUST 保持 D 的 Fence/Admission Participant Barrier，
MUST NOT 引入独立发布顺序。

UNKNOWN 在解析前保持非最终状态。

在受保护发布条件满足之前，E 不得暴露
看似规范的 Claim/Fact、Index Event、
公开 Artifact 或 Serving Reference。

Staging 不代表规范接收。

E 不拥有规范 Claim/Fact 身份，
也不拥有 I 治理授权。

### 19.2 Producer Admission 与 PublicationParticipant Admission

Producer Admission 与 PublicationParticipant Admission
是同一受保护生产和发布生命周期中的两个不同且有序的准入阶段。

不得将二者视为别名、等价操作或可以互换的准入决定。

Producer Admission 将准确的 Producer/ProducerWork 身份
准入规范生产生命周期。

按照 §19.1 的规定，它必须发生在依赖集合登记和
规范 Revision 提交之前。

PublicationParticipant Admission 将准确的
PublicationParticipant 准入发布流程，并将其绑定到相应的
StorageVisibilityParticipantRef 和 publication tuple digest。

只有在 D 已提交适用的规范 Revision，且 Storage 已将准确的
publication tuple 持久化为 PREPARED_HIDDEN 之后，
才允许执行 PublicationParticipant Admission。

Producer Admission 成功不得被解释为
PublicationParticipant Admission 成功。

两个准入阶段必须保持以下顺序：

1. Producer Admission，以及对准确准入 Producer participant
   的持久化记录。
2. 完整 direct 和 transitive dependency set 的持久化登记。
3. Canonical ClaimRevision/FactRevision 提交及必需的规范引用。
4. 将准确的 Storage publication tuple 持久化为 PREPARED_HIDDEN。
5. 针对当前 ForgetFence 执行 PublicationParticipant Admission。
6. 后续受保护的可见性处理。

PublicationParticipant Admission 必须绑定准确的已提交
publication identity，不得创建、替换、缩减或独立重新定义
在 Producer Admission 和 dependency-set registration
阶段建立的 dependency closure。

两个准入阶段都必须针对权威 ForgetFence/Admission
排序锚点进行串行化。

对于每个准入阶段，准入成功与对准确准入 participant
的持久化记录，必须在权威串行化 Transaction Domain
内构成一个不可分操作。

如果对应的 participant 记录失败或尚未持久可见，
Admission 不得报告成功。

后续 Forget Fence 不得越过对应的、尚未解决的
已准入 participant barrier。

后续 Fence 必须通过权威串行化 barrier
处理每一个成功准入的 participant。

不得静默跳过、删除或替换任一 participant identity。

实现必须保留 Producer Admission 与
PublicationParticipant Admission 之间的区别，
包括各自的 participant identity、持久化记录、执行顺序、
dependency closure 和最终 Forget outcome。

这是一个 implementation-conformance gate，
不是尚未解决的规范排序选择。

#### Storage 边界

既有 Storage L1 决策保持不变。

本协议不批准 Storage L4。
