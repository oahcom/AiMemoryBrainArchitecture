---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "This work record documents Evidence contract conformance findings and proposed work packages; no approval or independent verification is claimed."
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/governance-register/GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026.md"
    en: "docs/en/14-ai-development/governance-register/GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026.md"
    zh-CN: null
---

# GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026 — Evidence Domain Contract Conformance

## 1. 登记信息

| 项目 | 内容 |
|---|---|
| 登记编号 | GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026 |
| 登记日期 | 2026-11-22 |
| 类别 | MIGRATION_DEBT / DOMAIN_CONTRACT_CONFORMANCE |
| 状态 | OPEN |
| 严重性 | CONTRACT CONFORMANCE — STRUCTURAL |
| 权威契约 | `02-domain-model/core-entities.md` §8 |
| 影响组件 | `memory-domain`、`memory-compiler`、`bmcp-protocol` 及其测试 |
| 关联登记 | GOV-NC-2026-11-22-ENUM-BOUNDARY-021；GOV-NC-2026-11-22-PHASE2-RESIDUAL-022 |
| 实施授权 | WP-B 已派发 — `AID-2026-053`（见 §11）；WP-A 未获授权且当前不可实施 |
| 关闭条件 | WP-A 与 WP-B 全部满足，并完成独立验证 |

本登记记录 Evidence 领域实体的实现与权威领域契约之间的系统性符合性缺口。

本登记不构成对既有 crate、公共 API、持久化格式或协议结构实施破坏性迁移的授权。

## 2. 实施范围

本登记包含两个相互关联但必须分别验证的工作包。

### WP-A：Evidence Structure Conformance

处理 Evidence 实体的结构符合性，包括：

1. 契约要求的 13 个字段。
2. `excerpt_ref` 的缺失。
3. `Evidence` 与 `EvidenceExtension` 之间的字段归属和身份重复。
4. 契约字段与实现字段之间的命名差异。
5. `source_ref`、`recorded_at`、`locator`、`observed_at` 的类型差异。
6. `TypedObjectRef`、`Instant`、`Locator`、`ContentRef` 等契约类型的正确落实。

### WP-B：Evidence Enum Conformance

处理：

1. `EvidenceKind` 的完整值域。
2. `EvidenceAvailability` 的完整值域。
3. Serde 序列化与反序列化表示。
4. 旧枚举值的显式迁移策略。
5. 所有构造点、匹配点、协议映射和测试。

两个工作包必须分别通过测试。任何一个工作包完成都不能单独关闭本登记。

## 3. 禁止范围

在获得独立实施授权之前：

- 不修改既有 `crates/` 文件。
- 不修改现有公共结构体和枚举。
- 不删除任何现有枚举变体。
- 不修改既有序列化和反序列化行为。
- 不修改数据库或其他持久化数据。
- 不修改 BMCP 协议 schema。
- 不修改根配置、构建脚本或双语基线。
- 不创建 PR、提交或推送。
- 不将本登记标记为已完成。
- 不把缺乏迁移依据的旧值静默映射为新值。
- 不将本登记的目标结构解释为已经获得实施授权。

上述禁止以「获得独立实施授权之前」为前提。WP-B 已于 2026-11-23 按 §11 派发，该授权仅及于 §11 表格所列范围；WP-A 与其他条目继续有效。

## 4. 问题概述

权威领域契约：

`02-domain-model/core-entities.md` §8，文件第 127–145 行。

该章节定义了一个 Evidence 实体，包含 13 个字段。

契约原文：

```text
## 8. Evidence

| Field | Type / nullable | Meaning and constraint |
|---|---|---|
| evidence_id | OpaqueId, required | Stable identity |
| evidence_kind | Enum, required | source_span, user_statement, document, observation, tool_result, attestation, derived_excerpt |
| source_ref | TypedObjectRef, required | Event/document/external source |
| locator | Locator, nullable | Message span, page, JSON path, time range, environment tick |
| excerpt_ref | ContentRef, nullable | Retained excerpt if permitted |
| observed_at | Instant, nullable | Observation time |
| recorded_at | Instant, required | Brain record time |
| collector_ref | ActorRef, required | Capturing actor/component |
| integrity_digest | String, nullable | Source integrity reference |
| evidential_role | Enum, required | supports, refutes, qualifies, context_only |
| source_reliability_ref | OpaqueId, nullable | Separate source assessment |
| scope_refs | ScopeRef[], required | Evidence access scope |
| availability_state | Enum, required | available, restricted, expired, forgotten, external_unavailable |
```

契约要求一个统一的 Evidence 实体，其身份、来源、定位、摘录、观察时间、记录时间、采集者、完整性、证据角色、来源可靠性、访问范围和可用状态共同构成证据记录。

当前实现将其拆分为 `Evidence` 和 `EvidenceExtension` 两个结构体。

实测实现原文：

```rust
pub struct Evidence {
    pub evidence_id: OpaqueId,
    pub source_ref: OpaqueId,
    pub recorded_at: String,
    pub scope_refs: Vec<ScopeRef>,
    pub role: EvidenceRole,
}

pub struct EvidenceExtension {
    pub evidence_ref: EvidenceRef,
    pub kind: EvidenceKind,
    pub source_ref: EvidenceSourceRef,
    pub locator: Option<String>,
    pub observed_at: Option<TimeValue>,
    pub collector: ActorRef,
    pub integrity_digest: Option<String>,
    pub source_reliability_ref: Option<OpaqueId>,
    pub availability: EvidenceAvailability,
}
```

两个结构体合计 14 个字段。

逐字段比较发现至少四类符合性缺口：字段缺失、字段名称及身份归属不一致、类型不一致、枚举值域不一致。

这不是单纯的命名差异，也不能通过仅修改枚举解决。

## 5. 逐项缺陷及实测依据

### 5.1 契约字段完全缺失

| 契约字段 | 契约类型 | 当前实现 |
|---|---|---|
| excerpt_ref | ContentRef, nullable | 完全不存在 |

`excerpt_ref` 表示在许可条件下保留的证据摘录引用。

不能把 `locator`、`source_ref` 或其他字段解释成它的等价替代品。

该缺失属于结构性符合性缺口。

### 5.2 字段名称和身份归属不一致

| 契约字段 | 当前实现 | 所在结构体 |
|---|---|---|
| evidence_kind | kind | EvidenceExtension |
| collector_ref | collector | EvidenceExtension |
| evidential_role | role | Evidence |
| availability_state | availability | EvidenceExtension |
| evidence_id | evidence_ref | EvidenceExtension；Evidence 同时存在 evidence_id |

前四项需要核实并落实契约字段的统一命名。

第五项不仅是命名问题。

当前：

- `Evidence` 有 `evidence_id: OpaqueId`。
- `EvidenceExtension` 有 `evidence_ref: EvidenceRef`。

这意味着两个结构体各自承载一个身份相关字段。

迁移必须明确唯一 Evidence 身份及扩展信息与该身份的关联方式。

不得在缺乏语义依据时简单地删除其中一个字段或改变其类型。

### 5.3 字段类型不一致

| 契约字段 | 契约要求 | 当前实现 |
|---|---|---|
| source_ref | TypedObjectRef | Evidence 中为 OpaqueId；EvidenceExtension 中为 EvidenceSourceRef |
| recorded_at | Instant | String |
| locator | Locator, nullable | Option<String> |
| observed_at | Instant, nullable | Option<TimeValue> |

其中 `source_ref` 是特别重要的缺口。

当前存在两份来源引用：

```rust
Evidence.source_ref: OpaqueId
EvidenceExtension.source_ref: EvidenceSourceRef
```

`EvidenceSourceRef` 当前为包含 Event、Memory、External 三种变体的枚举。

不能因为该枚举具有来源分类能力，就将其视为与契约 `TypedObjectRef` 已经等价。

迁移必须遵守契约要求的类型语义。

`recorded_at` 必须满足 Instant 语义，而不能仅以任意 String 表示。

`locator` 必须能够表达契约描述的定位类型，包括消息区间、页码、JSON 路径、时间范围及环境 tick。

`observed_at` 必须满足 Instant 语义。

以上四项不能通过字段重命名解决。

### 5.4 EvidenceKind 值域不一致

契约要求：

```text
source_span
user_statement
document
observation
tool_result
attestation
derived_excerpt
```

当前实现：

```rust
pub enum EvidenceKind {
    Document,
    Message,
    Observation,
    Record,
    Dataset,
    Other(String),
}
```

逐项结果：

| 类型 | 值 |
|---|---|
| 契约要求且已存在 | Document、Observation |
| 契约要求但缺失 | SourceSpan、UserStatement、ToolResult、Attestation、DerivedExcerpt |
| 实现额外存在 | Message、Record、Dataset、Other(String) |

该枚举与权威领域值域不一致。

不得根据名称相似性自动映射 Message 到 SourceSpan，也不得将 Record、Dataset 或 Other(String) 任意映射到某个权威值。

所有映射必须具有可审计的语义依据。

### 5.5 EvidenceAvailability 值域不一致

契约要求：

```text
available
restricted
expired
forgotten
external_unavailable
```

当前实现：

```rust
pub enum EvidenceAvailability {
    Available,
    Restricted,
    Unavailable,
    Forgotten,
}
```

逐项结果：

| 类型 | 值 |
|---|---|
| 契约要求且已存在 | Available、Restricted、Forgotten |
| 契约要求但缺失 | Expired、ExternalUnavailable |
| 实现额外存在 | Unavailable |

`Unavailable` 不能被认定为 `Expired` 或 `ExternalUnavailable` 的等价值。

这三种状态可能代表不同事实：

- Expired：证据已过期。
- ExternalUnavailable：外部来源无法取得。
- Unavailable：当前旧实现中的概括性状态，不能单凭名称确定其具体原因。

必须制定显式的历史数据迁移或拒绝加载策略。

## 6. 治理裁定

### 6.1 权威性

`02-domain-model/core-entities.md` §8 是本登记判断 Evidence 领域实体符合性的权威依据。

当前实现不符合该契约。

本登记不授权反向修改契约以迁就现有实现。

### 6.2 单一登记、双工作包

WP-A 与 WP-B 共同构成一个 Evidence 实体符合性问题。

它们可以独立实施、独立验证，但必须共同满足本登记的关闭条件。

不得以 WP-B 的枚举测试通过代替 WP-A 的结构符合性验证。

不得以 WP-A 的结构测试通过代替 WP-B 的值域验证。

### 6.3 旧数据迁移

目前没有充分证据证明所有历史持久化数据均不包含旧枚举值。

任何迁移实施前都必须独立盘点：

- 数据库记录。
- 历史 JSON 和其他序列化数据。
- 测试 fixture。
- 外部协议输入。
- 已发布或保留的历史数据格式。

对于旧值：

1. `Unavailable` 不允许静默转换为 `Expired`。
2. `Unavailable` 不允许静默转换为 `ExternalUnavailable`。
3. `Message`、`Record`、`Dataset`、`Other(String)` 不允许未经语义判定直接映射。
4. 如果无法建立可靠映射，应拒绝加载并报告具体数据位置，或者使用经过批准的显式迁移流程。
5. 兼容读取层不得把旧值继续作为新的权威领域值域。

### 6.4 Serde 与序列化

目标 Enum 的序列化表示必须与领域契约一致。

建议目标表示使用稳定的 snake_case 字符串形式，例如：

- `SourceSpan` → `source_span`
- `UserStatement` → `user_statement`
- `ExternalUnavailable` → `external_unavailable`

是否采用 `#[serde(rename_all = "snake_case")]` 必须在实施阶段与现有 schema、历史格式及协议表示进行核对。

不能只根据当前 Rust 变体名称推断历史 JSON 的实际表示。

结构体字段的改名、合并、类型变更和身份归属调整同样属于序列化兼容性风险，必须纳入迁移计划。

### 6.5 Evidence 双 `source_ref` 语义：维持登记缺口

本节记录裁定原文，与 §5.3 互补。裁定结果是不建立等价关系，因此不添加相等校验。

**Status:** OPEN / NOT_AUTHORIZED

`Evidence.source_ref` (`OpaqueId`) and
`EvidenceExtension.source_ref` (`EvidenceSourceRef`) are distinct representations.
The current contract does not establish that they have equivalent semantics.
`EvidenceSourceRef` classification capability is not evidence of equivalence to
the contract's `TypedObjectRef`.

Do not add an equality check or conversion-based equivalence assertion between
these fields until the authoritative representation and its mapping semantics
are explicitly defined.

The existing `validate_against` check between `evidence_id` and
`extension.evidence_ref` remains unchanged. This does not close the dual
`source_ref` gap.

**Required resolution:** define the authoritative `source_ref` representation,
its contract-level semantics, and any permitted mapping to legacy or extension
representations before implementing cross-field validation.

## 7. 实施要求

### WP-A：结构迁移

执行方必须：

1. 建立契约 13 字段与最终 Rust 模型之间的逐字段映射。
2. 明确 Evidence 唯一身份。
3. 消除 `Evidence` 与 `EvidenceExtension` 之间的身份歧义。
4. 确保 `source_ref` 只有符合契约语义的权威表示。
5. 实现 `excerpt_ref`。
6. 统一契约字段名称。
7. 使 `recorded_at`、`locator`、`observed_at` 满足契约类型。
8. 验证所有必填字段与可空字段。
9. 验证旧序列化数据的兼容或显式拒绝策略。

### WP-B：枚举迁移

执行方必须：

1. 采用契约规定的完整 EvidenceKind 值域。
2. 采用契约规定的完整 EvidenceAvailability 值域。
3. 验证所有构造点和 match 分支。
4. 验证 BMCP 协议映射。
5. 验证 Serde 序列化和反序列化。
6. 制定旧值的显式迁移策略。
7. 不进行没有证据支持的自动值域映射。

## 8. 测试清单

### WP-A 测试

- [ ] Evidence 必须覆盖契约规定的全部 13 个字段。
- [ ] `excerpt_ref` 存在并正确支持 nullable 语义。
- [ ] Evidence 身份唯一且关联关系明确。
- [ ] 不存在两个具有不同语义的权威 `source_ref`。
- [ ] `source_ref` 满足 TypedObjectRef 契约。
- [ ] `recorded_at` 满足 Instant 契约。
- [ ] `locator` 满足 Locator 契约。
- [ ] `observed_at` 满足 Instant nullable 契约。
- [ ] `collector_ref` 满足 ActorRef 契约。
- [ ] `evidential_role` 的值域与契约一致。
- [ ] 必填与可空字段的反序列化行为正确。
- [ ] 旧结构数据的迁移或拒绝行为经过测试。

### WP-B 测试

- [ ] EvidenceKind 恰好覆盖七个契约值。
- [ ] EvidenceKind 不包含未经授权的额外领域值。
- [ ] EvidenceAvailability 恰好覆盖五个契约值。
- [ ] EvidenceAvailability 不包含 Unavailable。
- [ ] 所有构造点已迁移。
- [ ] 所有 match 分支完整。
- [ ] BMCP 协议映射经过验证。
- [ ] Serde 使用稳定且符合契约的字符串表示。
- [ ] 旧 Unavailable 数据不会被静默映射。
- [ ] 旧 EvidenceKind 值具有明确迁移或拒绝策略。

### 集成测试

- [ ] memory-domain 测试通过。
- [ ] memory-compiler 测试通过。
- [ ] bmcp-protocol 测试通过。
- [ ] 跨 crate Evidence 数据流符合统一契约。
- [ ] 序列化往返测试通过。
- [ ] 历史数据迁移测试通过，或明确验证拒绝加载。
- [ ] 没有未经授权的协议和持久化格式变化。

## 9. 关闭条件

本登记只能在以下条件全部满足后关闭：

1. WP-A 全部结构符合性测试通过。
2. WP-B 全部枚举符合性测试通过。
3. 13 个契约字段均有明确实现映射。
4. 两个枚举的完整值域与契约一致。
5. 身份和来源引用不存在歧义。
6. 旧序列化数据具有经过批准的迁移或拒绝加载策略。
7. 所有受影响 crate 的构造点、匹配点和协议映射经过验证。
8. 集成测试通过。
9. 独立审查确认实现符合 §8。
10. 相关变更获得正式实施授权和必要审批。

任意一项未完成，本登记继续保持 OPEN。

## 10. 治理结论

Evidence 当前实现与权威领域契约之间存在结构性符合性缺口。

该缺口包括字段缺失、字段名称与身份归属不一致、字段类型不一致以及两个枚举的值域不一致。

本问题统一登记为 GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026，分为 WP-A 和 WP-B 两个独立验证工作包。

本登记不构成破坏性迁移授权。

在正式授权、完成历史数据盘点及迁移方案审批之前，既有实现保持不变。

**最终状态：OPEN — EVIDENCE DOMAIN CONTRACT CONFORMANCE DEBT.**

## 11. 实施派发（2026-11-23）

| 项目 | 内容 |
|---|---|
| 工作令 | `AID-2026-053`（`14-ai-development/work-items/AID-2026-053/`） |
| 派发依据 | 本登记 §2 WP-B、§7 WP-B、§8 WP-B；裁定 `OWNER-DECISION-EVIDENCE-CONTRACT-001` §8 |
| 实施范围 | `crates/memory-domain/src/lib.rs` 的两个枚举声明，`crates/memory-compiler/src/evidence.rs` 的 `attachment_decision`，及两侧测试 |
| 明确不授权 | WP-A、`Evidence` 与 `EvidenceExtension` 的任何字段变更、`crates/bmcp-protocol/` 的任何改动、本登记关闭 |

**本次只派发 WP-B，因为 WP-B 与 WP-A 的阻塞性质不同。** WP-A 不是「未获授权」，而是**当前不可实施**：`Instant`、`Locator`、`ContentRef` 三个契约类型在全仓 `crates/` 下出现次数为零，`Instant` 另受本登记 §14 的「时间戳精度」未决项约束。授权无法解除这个阻塞，定义才能。

**§7 WP-B 第 4 项测量不到任何对象。** 该项要求「验证 BMCP 协议映射」。`crates/bmcp-protocol/` 确有一个同名 `EvidenceKind`，但它是 `pub mod evidence` 下的四个投递类别（`FINAL_REQUEST_SUBMITTED`、`APPLIED_CONTEXT_OBSERVED`、`EXECUTION_STARTED`、`RECONCILIATION_OBSERVED`）；该 crate 不依赖 `memory-domain`，包外无任何引用，两侧不存在任何转换实现。两个枚举只共享一个名字。因此该项的正确产出是「无映射可验证」这一结论本身，而不是新建一个映射。派发已把该结论写进工作令的硬约束 #1。

**§6.3 与实测的直接冲突，以及它的解决方式。** §6.3 开头称「目前没有充分证据证明所有历史持久化数据均不包含旧枚举值」，并要求实施前独立盘点。实测结果是：`EvidenceExtension` 不出现在任何存储 crate 中，仓库内无 `.db`/`.sqlite` 文件，无 `*.sql` 迁移，两个枚举的四个非契约 `EvidenceKind` 值与 `Unavailable` 的构造点合计一处且位于测试内。所以本仓库不存在需要盘点的旧数据。

但这句话不能靠「我搜过了」来成立，因此本次采用 §6.3 第 4 项自己给出的另一条分支：**无法建立可靠映射时，拒绝加载**。`Unavailable` 不静默转成 `Expired`，也不静默转成 `ExternalUnavailable`，而是让 serde 反序列化失败。这样一来，本登记 §9 第 6 项要求的「经过批准的迁移或拒绝加载策略」以拒绝加载的形态被满足，而 §6.3 第 1、2、3、5 项在实现层不可能被违反——不存在能把旧值带进新值域的路径。

**§3 的禁止项在 WP-B 范围内解除。** §3 的禁止以「获得独立实施授权之前」为前提。本次派发即该授权，但仅及于上表所列范围。§3 的下列条目在 WP-B 范围内不再适用：不修改既有 `crates/` 文件、不修改现有公共枚举、不删除任何现有枚举变体、不修改序列化行为。其余条目继续有效，特别是「不修改 BMCP 协议 schema」「不将本登记标记为已完成」。

**为什么状态不是 CLOSED。** §9 第 10 项要求「正式实施授权和必要审批」，派发不是授权；第 1、3、5 项属于 WP-A，仍全部未满足；第 9 项要求独立审查与 §8 比对，而派发会话不能为自己的产物提供独立证据。这与 `AID-2026-052` 派发本登记 027 时的推理一致。

**残留风险，记录而非掩盖。** `#[serde(rename_all = "snake_case")]` 是线格式变更，本登记正文并未授权线格式变更，授权的是值域。它在此安全，仅因为持久化语料为空——这是对 `86c66ec4` 这一棵树在某一次提交上的测量结论，不是设计的性质。一旦将来出现存储实现，该改名即降级为一次迁移，而 `AID-2026-053` 不是执行该迁移的工具。
