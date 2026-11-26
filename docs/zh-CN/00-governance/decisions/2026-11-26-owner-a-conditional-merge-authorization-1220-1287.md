---
document_metadata:
  domain: architecture
  role: decision-record
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
        - "00-governance/decisions/2026-11-26-owner-a-conditional-merge-authorization-1220-1287.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Owner A 条件式合并授权记录的简体中文镜像。"
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
    canonical_scope: "Owner A 条件式合并授权 OA-MERGE-2026-11-26-01 的简体中文镜像"
    canonical_scope_id: "governance/owner-a-conditional-merge-authorization-1220-1287/zh-CN"
    canonical_scope_keywords:
      - merge-authorization
      - pr-1220
      - pr-1287
      - mirror
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "00-governance/decisions/2026-11-26-owner-a-conditional-merge-authorization-1220-1287.md"
    en: "docs/en/00-governance/decisions/2026-11-26-owner-a-conditional-merge-authorization-1220-1287.md"
    zh-CN: null
---

# Owner A 条件式合并授权 — PR #1287 与 #1220

- 决策编号：`OA-MERGE-2026-11-26-01`
- 授权主体：`oahcom`（Owner A）
- 授权渠道：Owner A 明确的 GitHub PR 评论
- 适用范围：仅 PR #1287 与 PR #1220
- 要求的合并顺序：#1287，然后 #1220

## 决定

Owner A 有条件授权合并 PR #1287，随后合并 PR #1220，条件是满足授权评论中写明的 exact-head 必需检查与 manifest 条件。

## 生效条件

1. PR #1287 的最终 HEAD SHA 上全部必需检查通过。
2. PR #1287 先于 PR #1220 合并。
3. PR #1220 与合并后的 main 分支重新对齐。
4. PR #1220 的最终 HEAD SHA 上全部必需检查通过。
5. PR #1220 最终的 `manifest.yaml` 的 `prohibitions` 中不含 `DO_NOT_MERGE` 条目。
6. 已约定的恢复归属边界得到保持。

## 审计字段

- Owner A 授权评论地址：https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1220#issuecomment-7193523585
- 授权时间戳：2026-11-26T13:33:49Z
- PR #1287 获授权的最终 HEAD SHA：在合并决策时记录
- PR #1220 获授权的最终 HEAD SHA：在合并决策时记录
- 必需检查证据：在每次合并决策时记录 exact-head 结果
- 合并提交 SHA：每次合并后记录

本记录记录一项条件式授权。它不主张其条件已被满足。

## 委托

本次发布由协调会话依据委托 `OA-DELEGATE-2026-11-26-01` 执行；委托记录发布于 https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1220#issuecomment-7193523076，并归档于 `00-governance/decisions/2026-11-26-owner-a-delegation-2026-11-26.md`。

代理发布：由协调层 ChatGPT 会话依据委托记录 OA-DELEGATE-2026-11-26-01 代 Owner A 发布；非 Owner A 本人亲自发布。
