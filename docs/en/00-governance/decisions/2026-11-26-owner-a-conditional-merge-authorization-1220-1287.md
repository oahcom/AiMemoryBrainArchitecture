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
      last_verification_note: "English mirror of an Owner A conditional merge authorization record."
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
    canonical_scope: "English mirror of Owner A conditional merge authorization OA-MERGE-2026-11-26-01"
    canonical_scope_id: "governance/owner-a-conditional-merge-authorization-1220-1287/en"
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
    en: null
    zh-CN: "docs/zh-CN/00-governance/decisions/2026-11-26-owner-a-conditional-merge-authorization-1220-1287.md"
---

# Owner A Conditional Merge Authorization — PR #1287 and #1220

- Decision ID: `OA-MERGE-2026-11-26-01`
- Authorization principal: `oahcom` (Owner A)
- Authorization channel: Owner A's explicit GitHub PR comment
- Scope: PR #1287 and PR #1220 only
- Required merge order: #1287, then #1220

## Decision

Owner A conditionally authorizes the merge of PR #1287 followed by PR #1220, subject to the exact-head required-check and manifest conditions stated in the authorization comment.

## Activation conditions

1. All required checks pass on PR #1287's final HEAD SHA.
2. PR #1287 is merged before PR #1220.
3. PR #1220 is reconciled against the resulting main branch.
4. All required checks pass on PR #1220's final HEAD SHA.
5. PR #1220's final `manifest.yaml` contains no `DO_NOT_MERGE` entry in `prohibitions`.
6. The agreed restoration ownership boundary is preserved.

## Audit fields

- Owner A authorization comment URL: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1220#issuecomment-7193523585
- Authorization timestamp: 2026-11-26T13:33:49Z
- PR #1287 authorized final HEAD SHA: record at merge decision
- PR #1220 authorized final HEAD SHA: record at merge decision
- Required-check evidence: record exact-head results at each merge decision
- Merge commit SHAs: record after each merge

This record documents a conditional authorization. It does not assert that its conditions have already been satisfied.

## Delegation

The publication was executed by the coordinating session under delegation `OA-DELEGATE-2026-11-26-01`; the delegation record is published at https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1220#issuecomment-7193523076 and filed at `00-governance/decisions/2026-11-26-owner-a-delegation-2026-11-26.md`.

代理发布：由协调层 ChatGPT 会话依据委托记录 OA-DELEGATE-2026-11-26-01 代 Owner A 发布；非 Owner A 本人亲自发布。

