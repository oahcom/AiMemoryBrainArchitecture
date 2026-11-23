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
      last_verification_note: "This work record documents a Provenance reference-validation gap; no approval or independent verification is claimed."
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
    source: "14-ai-development/governance-register/GOV-NC-2026-11-22-PROVENANCE-REFERENCE-REVALIDATION-027.md"
    en: "docs/en/14-ai-development/governance-register/GOV-NC-2026-11-22-PROVENANCE-REFERENCE-REVALIDATION-027.md"
    zh-CN: null
---

# GOV-NC-2026-11-22-PROVENANCE-REFERENCE-REVALIDATION-027 — Provenance Reference Revalidation

## 1. 登记信息

| 项目 | 内容 |
|---|---|
| 登记编号 | GOV-NC-2026-11-22-PROVENANCE-REVALIDATION-027 |
| 登记日期 | 2026-11-22 |
| 类别 | VALIDATION_GAP / DOMAIN_TYPE_INTEGRITY |
| 状态 | OPEN |
| 严重性 | REFERENCE INTEGRITY — SERDE BYPASS |
| 影响组件 | `memory-domain`（`Provenance`、`ProvenanceGraph`） |
| 关联登记 | GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026 |
| 实施授权 | NOT AUTHORIZED |
| 关闭条件 | 四类引用字段全部逐项重验，且 Serde 绕过测试通过 |

**编号说明。** 编号 `027` 由「当前已占用最大编号 026 加一」推导，不是由登记流程发放。
推导依据：本目录 `-026` 为最大编号，`025` 为另一份 ADR；全仓与全部远端分支检索 `027` 无占用。
若登记流程要求正式分配，请以上级流程结论替换此编号，本文其余内容不受影响。

## 2. 问题

`Provenance::validate()` 当前校验必填标量字段、lineage 是否存在、以及
`source_version_refs` 相对 `source_refs` 的位置完整性。它**没有**逐项重验下列字段中包含的引用值：

- `source_refs`
- `source_version_refs`
- `actor_ref.actor_id`
- `parent_provenance_refs`

Serde 反序列化可以在不经过领域构造器的情况下构造这些值。因此，
构造器级校验无法证明一个反序列化得到的 `Provenance` 实例含有有效引用。

`ProvenanceGraph::add()` 在插入前调用 `provenance.validate()`。
该入口的完整性因此取决于 `Provenance::validate()` 是否执行了引用级校验。

同一 crate 内的 `EvidenceExtension::validate()` 已经做了逐项重验，并在注释中写明理由
（Serde 派生 `Deserialize` 绕过构造器，载荷可携空串进入构造器永远不会产生的字段）。
`Provenance` 没有得到同等处理。

## 3. 需要完成的工作

1. 查明上述每个引用字段的具体类型与验证 API。
2. 为每个字段定义引用有效性要求，包括嵌套的 `actor_ref.actor_id`。
3. 扩展 `Provenance::validate()`，用各具体类型的权威验证 API 重验每个引用值。
4. 保持既有不变式：
   - `source_refs` 不得为空。
   - `source_version_refs` 存在时长度必须等于 `source_refs.len()`。
   - 显式提供的 `unavailable_reason` 不得为空白。
   - 记录必须提供 parent lineage，或显式说明其缺失。
5. 确保 `ProvenanceGraph::add()` 在修改图之前拒绝无效引用。
6. 增加验收测试：通过反序列化构造非法引用值，证明直接校验与图插入都会拒绝。

## 4. 验收条件

- `source_refs` 每个元素均被重验。
- `source_version_refs` 每个元素均被重验。
- `actor_ref.actor_id` 被重验。
- `parent_provenance_refs` 每个元素均被重验。
- 非法反序列化值无法通过 `Provenance::validate()`。
- 非法反序列化值无法通过 `ProvenanceGraph::add()` 插入。
- 图插入失败时原图保持不变。
- 既有合法 `Provenance` fixture 与 lineage 行为保持有效。

## 5. 范围边界

本登记独立于 Evidence 双 `source_ref` 语义问题
（GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026 §6.5）。
它不定义、也不暗示 `Evidence.source_ref` 与 `EvidenceExtension.source_ref` 之间存在等价关系。

本登记**未**包含在 PR #707 中。PR #707 不修改 `Provenance::validate()`，
也不修改 `ProvenanceGraph::add()`。
