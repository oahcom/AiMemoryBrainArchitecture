---
document_metadata:
  domain: domain-model
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
        - "14-ai-development/work-items/AID-2026-190/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "为原本无 front-matter 的镜像补 GOV-DOC-002 分类：仅记录 domain、role、状态与规范源路径（依据正文自述：Status: DECIDED semantics unless marked otherwise）；不主张规范权威，也不证明与源语义对等。补元数据前正文 blob：c9af1f47abd1072427b59b759edcbe6581ec5c3a。"
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
    canonical_conflict_status: None
    normative_status: Normative
  bilingual_counterpart:
    source: "02-domain-model/core-entities.md"
    en: "docs/en/02-domain-model/core-entities.md"
    zh-CN: null
---
# 核心领域实体

- 文档 ID：DOMAIN-ENTITIES-001
- 版本：1.0
- 源规范：[规范性原文](../../../02-domain-model/core-entities.md)
- 源版本： c1afadee6289318f7a19d87fcba2cdb50b7131aa
- 对应英文：[Core Domain Entities](../../en/02-domain-model/core-entities.md)
- 状态：除非另有明确标记，否则语义为 DECIDED
- Owner：Memory Domain Model（MB-01）

**目的：** 定义逻辑 Schema 和字段约束，不定义数据库 DDL 或 Wire Format。

## 1. Schema 约定

ID 是不透明且不承载业务语义的标识符。**CANDIDATE：** UUIDv7 或其他可排序的不透明标识符；算法不具规范约束力。时间戳使用 UTC 时间点；在相关时保留来源精度/时区。区间默认采用左闭右开形式 [start, end)。Required 表示有效持久化对象必须提供。Unknown 必须显式表达，不得编造。Canonical Version 不可变。枚举演进必须满足 Schema/Version 兼容要求。

## 2. Event（事件）

Event 是被捕获的发生、观察、报告或状态转换。

| 字段 | 类型/是否可空 | 含义与约束 |
|---|---|---|
| event_id | OpaqueId，必填 | 稳定唯一身份 |
| event_kind | String/enum，必填 | 带版本的事件词汇 |
| source_type | Enum，必填 | user、agent、environment_adapter、external_system、document、system |
| source_id | OpaqueId/String，必填 | 来源身份；不是认证凭据 |
| payload_ref | ContentRef，必填 | 保留的 Payload 或声明的外部来源 |
| event_time | TimeValue，可空 | 事件发生时间；未知时为 null |
| recorded_at | Instant，必填 | 可靠接收时间，不可变 |
| scope_refs | ScopeRef[]，必填 | 已解析的 Scope |
| environment_scope_id | OpaqueId，可空 | 依赖环境时必填 |
| idempotency_key | String，条件必填 | 来源/操作范围内可重试接收的唯一性标识 |
| classification | Enum，必填 | observed、reported、planned、predicted、attempted、outcome、administrative、unknown |
| schema_version | String，必填 | Envelope 版本 |
| retention_class | String，必填 | Governance 策略选择器 |
| integrity_digest | String，可空 | Payload 完整性引用 |

Accepted 不代表已验证真实性。Planned/Predicted 不是 Outcome。同一个 Idempotency Key 对应不同 Payload Digest 时属于 Conflict。

## 3. Memory（记忆资产）

| 字段 | 类型/是否可空 | 含义与约束 |
|---|---|---|
| memory_id | OpaqueId，必填 | 跨版本稳定，永不复用 |
| memory_kind | String/enum，必填 | preference、episodic、procedural-description、semantic、environment-state 等 |
| label | String，可空 | 展示标签，不是身份 |
| scope_refs | ScopeRef[]，必填 | 所有权/适用范围边界 |
| primary_environment_scope_id | OpaqueId，可空 | 相关时明确的环境锚点 |
| current_version_id | OpaqueId，首次提交后必填 | 当前不可变版本 |
| lifecycle_state | Enum，必填 | Candidate、Consolidated、Active、Superseded、Archived、Forgotten |
| created_at / updated_at | Instant，必填 | Canonical 创建时间/当前指针更新时间 |
| retention_class | String，必填 | 保留策略 |
| sensitivity | Enum，必填 | public-within-scope、internal、sensitive、restricted |
| supersedes_memory_id | OpaqueId，可空 | 明确的前驱记忆 |
| forget_operation_id | OpaqueId，可空 | Governance 工作流引用 |

一个 Memory 可以包含多个 Claim。若 Claim 集合为空，必须声明这是非命题型 Memory。Lifecycle 不代表真实性状态。

## 4. Memory Version（记忆版本）

| 字段 | 类型/是否可空 | 含义与约束 |
|---|---|---|
| memory_version_id | OpaqueId，必填 | 不可变版本身份 |
| memory_id | OpaqueId，必填 | 所属 Memory |
| version_number | PositiveInteger，必填 | 在单个 Memory 内单调递增，永不复用 |
| parent_version_id | OpaqueId，可空 | 仅初始版本允许为空 |
| created_at | Instant，必填 | 提交时间 |
| author_kind / author_ref | Enum + ActorRef，必填 | compiler、lifecycle_manager、authorized_user、governance、migration |
| change_reason | Enum/string，必填 | extraction、consolidation、correction、verification、retraction、migration |
| claims | ClaimSnapshot[]，必填 | 不可变命题集合 |
| entity_refs / relation_refs | OpaqueId[]，必填 | 明确的类型化引用 |
| provenance_refs | OpaqueId[]，必填 | 来源血缘或明确的不可用原因 |
| content_digest | String，必填 | Canonical 语义内容摘要 |
| schema_version | String，必填 | Domain Schema 版本 |

禁止原地编辑。当前指针推进和版本提交必须原子完成。竞争写入必须携带期望的 Parent/Current Version。

## 5. Claim

Claim 是规范命题身份。

Claim 使用稳定 ClaimRef，并具有不可变 ClaimRevision 记录。

ClaimRevision 标识一个准确的断言状态，并保留 Parent、命题、Epistemic Status、Valid Time、Evidence 引用、Provenance 引用和 Scope。

Claim 身份分类遵循 DOMAIN-MODEL-001 §2.4。

## 5A. Fact 与 FactRevision

Fact 是独立的受治理 Attestation 对象。

FactRevision 不可变，并引用准确的 ClaimRevisionRef、Evidence、Provenance、Scope、Attestor、Method/Version 和 I AuthorizationDecisionRef。

Fact 不是 Verified Claim 的别名，也不是客观真理标志。

本逻辑实体定义不批准 DDL 或物理 Schema。
## 6. Entity（实体）

| 字段 | 类型/是否可空 | 含义与约束 |
|---|---|---|
| entity_id | OpaqueId，必填 | 稳定且永不复用 |
| entity_type | String/enum，必填 | person、organization、project、agent、device、place、artifact、environment、concept |
| canonical_label | String，必填 | 首选展示名称 |
| aliases | AliasRecord[]，必填 | 带时间和 Scope 限定的别名 |
| identity_status | Enum，必填 | provisional、resolved、merged、split、retired |
| scope_refs | ScopeRef[]，必填 | 命名空间 |
| external_identifiers | ExternalId[]，必填 | 带命名空间的标识符；唯一性受 Scope 限定 |
| created_at | Instant，必填 | 创建时间 |
| current_version_id | OpaqueId，必填 | 当前身份/档案版本 |
| merged_into_entity_id | OpaqueId，可空 | 合并时必填 |
| identity_evidence_refs | OpaqueId[]，必填 | 身份解析证据或暂定原因 |

名称相同不能证明身份相同。Merge/Split 必须保留 Redirect、历史和可审计的引用迁移记录。

## 7. Relation（关系）

| 字段 | 类型/是否可空 | 含义与约束 |
|---|---|---|
| relation_id | OpaqueId，必填 | 稳定关系身份 |
| relation_type | String，必填 | 受控的类型化词汇 |
| subject_ref / object_ref | TypedObjectRef，必填 | 类型化端点 |
| directionality | Enum，必填 | directed、symmetric、inverse-paired |
| qualifiers | TypedMap，必填 | 角色、模态、环境、来源 |
| valid_time | TimeInterval，可空 | 声明的有效区间 |
| epistemic_status | Enum，必填 | 认知状态词汇 |
| evidence_refs | OpaqueId[]，必填 | 支持/反驳引用 |
| scope_refs | ScopeRef[]，必填 | 适用范围/可见范围 |
| lifecycle_state | Enum，必填 | proposed、active、superseded、retracted |
| created_at | Instant，必填 | 记录创建时间 |

Relation Type 必须声明允许的端点类型、逆向/对称语义和唯一性约束。共同出现不等于 Relation。

## 8. Evidence（证据）

| 字段 | 类型/是否可空 | 含义与约束 |
|---|---|---|
| evidence_id | OpaqueId，必填 | 稳定身份 |
| evidence_kind | Enum，必填 | source_span、user_statement、document、observation、tool_result、attestation、derived_excerpt |
| source_ref | TypedObjectRef，必填 | Event/Document/外部来源 |
| locator | Locator，可空 | 消息片段、页码、JSON Path、时间范围、环境 Tick |
| excerpt_ref | ContentRef，可空 | 策略允许时保留的摘录 |
| observed_at | Instant，可空 | 观察时间 |
| recorded_at | Instant，必填 | Brain 记录时间 |
| collector_ref | ActorRef，必填 | 捕获该证据的 Actor/组件 |
| integrity_digest | String，可空 | 来源完整性引用 |
| evidential_role | Enum，必填 | supports、refutes、qualifies、context_only |
| source_reliability_ref | OpaqueId，可空 | 独立的来源可靠性评估 |
| scope_refs | ScopeRef[]，必填 | Evidence 访问范围 |
| availability_state | Enum，必填 | available、restricted、expired、forgotten、external_unavailable |

Evidence 不是 Confidence 分数。仅有一个可变 URL 不能保证证据持久可靠。

## 9. Provenance 与 Memory Source

Provenance 字段：provenance_id（必填）、target_ref（必填）、source_edges（必填）、derivation_kind（必填：direct_capture、extraction、normalization、summarization、consolidation、inference、human_correction、migration）、method_ref（必填）、derived_at（必填）、input_digest_refs（必填）、parent_provenance_refs（必填）、unavailable_reason（可空，但不完整时必填）。

Memory Source 字段：memory_source_id、source_ref（尽可能使用类型化且带版本的引用）、source_role（primary、supporting、contradicting、context）、locator、scope_refs、created_at。除 locator 外均为必填。

Method Reference 描述处理过程，不证明结果正确。

## 10. Memory Context 与 Context Entry

Memory Context 字段：context_id、agent_scope_id、current_context_version、lifecycle_state、created_at、updated_at（必填）；task_scope_id、session_scope_id、environment_scope_id（可空）。

Context Entry 字段：context_entry_id、context_id、canonical_memory_id、memory_version_id、rendering_ref、position、entry_state、added_at、source_refs（必填）；expires_at（可空）。MCM 拥有 Context Version 和 Entry 状态。Entry 变更不得修改 Canonical 对象。

## 11. Agent Scope 与 Environment Scope

Agent Scope 字段：agent_scope_id、agent_id、owner_scope_id、scope_policy_ref、created_at、status（必填）；agent_instance_id 可空。

Environment Scope 字段：environment_scope_id、environment_kind、environment_identity、tenant_or_project_scope_id、created_at、status（必填）；parent_environment_scope_id 和 environment_version_ref 可空。它必须区分不同世界、存档、模拟运行、租户和不兼容的状态域。

## 12. 输入、输出、工作流与一致性

状态变更提案必须携带 Actor、Scope、Schema Version、可重试时使用的 Idempotency Key，以及 Provenance。校验返回类型化对象或结构化错误：code、object_type、object_id、field_path、invariant_id、retryable。

工作流：解析 Scope → 授权 → 校验语义 → 验证引用 → 提交不可变记录/版本 → 发布变更事件。提交前失败不得留下部分 Canonical 修改。提交后投影失败通过 Outbox/Replay 修复。过期版本写入必须拒绝；相同 Digest 的重复 Idempotency 请求返回之前结果；相同 Key 配不同 Digest 时拒绝。

## 13. 安全、性能与验收

在披露前按 Scope 过滤对象和引用。Evidence 的访问限制可以比 Memory 更严格。不可信内容不得作为可执行内容或具有指令权威。

**TO_VALIDATE：** 校验和序列化成本、引用扇出、Provenance 遍历性能。测试覆盖缺失字段、未知 Enum、重复 ID、过期 Version、跨 Scope 引用、无效 Relation 端点、缺少 Evidence 的 Verified，以及 Context Entry 修改隔离。

## 14. 开放决策

- **OPEN：** ID 策略、时间戳精度、跨版本 Claim 身份。
- **OPEN：** 可扩展词汇表注册机制的精确定义。
- **CANDIDATE：** 类型化引用采用 object_type + object_id + 可选 version_id 结构。
- **TO_VALIDATE：** 高扇出情况下 Schema 和 Provenance 性能。
