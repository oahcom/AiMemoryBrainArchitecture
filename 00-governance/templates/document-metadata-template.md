---
document_metadata:
  domain: security-governance
  role: reference
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    normative_status: Informative
    canonical_conflict_status: None
---

# Document metadata template / 文档元数据模板

Copy the block below into the top of a governed Markdown file and edit the values. The contract it
must satisfy is `00-governance/architecture-document-metadata.schema.yaml`.

将下面的块复制到受治理 Markdown 文件顶部并修改取值。其必须满足的契约见
`00-governance/architecture-document-metadata.schema.yaml`。

Every REQUIRED leaf must be present: a dimension that exists but declares no state is not a
classification.

每个 REQUIRED 叶子都必须存在：存在但不声明状态的维度不构成分类。

## The block / 待复制块

```yaml
---
document_metadata:
  domain: architecture              # REQUIRED, closed enum (13 values)
  role: design-specification        # REQUIRED, closed enum (9 values)

  lifecycle:
    approval:
      decision_status: Draft        # REQUIRED
      approver: null
      decision_date: null
      approved_version:             # REQUIRED when decision_status: Approved
        scheme: git                 # git | content-hash
        value: null
      approval_scope:
        type: Full-document         # the only value DM-10 honours
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null              # REQUIRED and non-null when decision_status: Revoked

    evidence_verification:
      verification_status: Unverified   # REQUIRED
      last_verified_date: null
      last_verification_note: null

    usage_status: Active            # REQUIRED
    modification_status: Unchanged  # REQUIRED

    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null

    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null

  authority:
    canonical_status: Non-Canonical # REQUIRED
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None # REQUIRED
    canonical_conflict_resolution: null
    normative_status: Informative   # REQUIRED
---
```

## Rules that are easy to get wrong / 容易写错的规则

- `superseded_by` MUST NOT be written by hand. It is derived (DM-08).
- A document under `docs/en/` or `docs/zh-CN/` MUST declare `bilingual_counterpart.source` (DM-12).
- A mirror group MUST agree on `domain`, `role` and `normative_status`, and at most one member is
  `Canonical` (DM-12).
- `canonical_conflict_status: Under-Review` requires `canonical_status: Candidate`; a document in
  conflict state MUST NOT be `Canonical` (DM-11).
- Every path value is a normalised repository-relative path: no absolute paths, no `..`, no
  backslashes, no repeated `./`. A violation is an error, never silently rewritten.

- `superseded_by` 禁止手写，属派生字段（DM-08）。
- 位于 `docs/en/` 或 `docs/zh-CN/` 下的文档必须声明 `bilingual_counterpart.source`（DM-12）。
- 同一镜像组内的 `domain`、`role`、`normative_status` 必须一致，且最多一份为 `Canonical`（DM-12）。
- `canonical_conflict_status: Under-Review` 要求 `canonical_status: Candidate`；冲突态文档禁止为
  `Canonical`（DM-11）。
- 所有路径值均为规范化的仓库相对路径：禁止绝对路径、`..`、反斜杠、重复的 `./`。违规即报错，
  绝不静默改写。
