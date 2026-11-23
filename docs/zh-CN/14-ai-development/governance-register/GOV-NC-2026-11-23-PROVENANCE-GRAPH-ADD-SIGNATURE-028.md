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
      last_verification_note: "This work record documents a public API signature change and the owner decision it requires; no approval or independent verification is claimed."
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
    source: "14-ai-development/governance-register/GOV-NC-2026-11-23-PROVENANCE-GRAPH-ADD-SIGNATURE-028.md"
    en: "docs/en/14-ai-development/governance-register/GOV-NC-2026-11-23-PROVENANCE-GRAPH-ADD-SIGNATURE-028.md"
    zh-CN: null
---

# GOV-NC-2026-11-23-PROVENANCE-GRAPH-ADD-SIGNATURE-028 — ProvenanceGraph::add 公开签名变更

## 1. 登记信息

| 项目 | 内容 |
|---|---|
| 登记编号 | GOV-NC-2026-11-23-PROVENANCE-GRAPH-ADD-SIGNATURE-028 |
| 登记日期 | 2026-11-23 |
| 类别 | PUBLIC_API_BREAKING_CHANGE |
| 状态 | OPEN |
| 严重性 | DOWNSTREAM COMPILE BREAK |
| 影响组件 | `memory-domain`（`ProvenanceGraph::add`） |
| 关联登记 | GOV-NC-2026-11-22-PROVENANCE-REFERENCE-REVALIDATION-027 |
| 实施授权 | OWNER DECISION REQUIRED |
| 关闭条件 | Owner 对兼容性策略作出裁定，且迁移通告与发布边界已确定 |

**编号说明。** 编号 `028` 由「当前已占用最大编号 027 加一」推导，不是由登记流程发放。
推导依据：本目录 `-027` 为最大编号；全仓与全部远端分支检索 `028` 无占用。
若登记流程要求正式分配，请以上级流程结论替换此编号，本文其余内容不受影响。

## 2. 变更

`ProvenanceGraph::add` 的公开签名由双参数改为单参数。

```rust
// 变更前（基线 6418e9c）
pub fn add(
    &mut self,
    provenance: Provenance,
    parents: &[ProvenanceRef],
) -> Result<(), DomainError>

// 变更后（PR #707，提交 bbd214f）
pub fn add(&mut self, provenance: Provenance) -> Result<(), DomainError>
```

## 3. 行为变更

lineage 现在唯一地来自 `Provenance.parent_provenance_refs`，不再由调用方通过 `parents` 参数提供。
入口新增 `provenance.validate()?` 调用。

变更动机（记录于 `provenance_graph.rs` 函数文档）：双参数会让调用方在记录上声明一套 lineage、在图上声明另一套，两套来源无法同时为真。改为单参数消除了这个冲突源。

## 4. 兼容性影响

按旧签名调用的下游代码将无法编译。

仓库内编译与测试只证明**仓库内**调用点已迁移，不证明下游兼容性。

## 5. 需要 Owner 裁定的事项

1. 该破坏性 API 变更是否在当前发布边界内获得授权。
2. 是否需要兼容层或弃用过渡期。
3. 变更须附带何种迁移通告。

在 Owner 明确裁定前，不得将「仓库内调用点已迁移」表述为「公开 API 兼容性已验证」。

## 6. 范围边界

本登记不替代、也不扩展
GOV-NC-2026-11-22-PROVENANCE-REFERENCE-REVALIDATION-027。

027 的主题是 Provenance 四类引用字段的逐项重验；本登记的主题是公开签名变更及其兼容性授权。
两者独立，不互相吸收。

本登记的变更**已存在于 PR #707 的代码中**（提交 `bbd214f`）。
本登记不主张该变更已被授权；它记录的是「变更已发生、授权待定」这一状态。
