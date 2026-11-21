---
document_metadata:
  domain: security-governance
  role: decision-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope: null
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/adr/OWNER-DECISION-DOC-BACKLOG-COUNT-001.md"
        - "Issue #305 comment 7042461592"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-21"
      last_verification_note: "Bilingual mirror of the canonical Owner decision record."
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
    canonical_scope: "Governance decision: docs backlog count correction"
    canonical_scope_id: "security-governance/docs-backlog-count-correction"
    canonical_scope_keywords:
      - document-scope
      - backlog
      - dm-14
      - inventory
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    source: "14-ai-development/adr/OWNER-DECISION-DOC-BACKLOG-COUNT-001.md"
    en: "docs/en/14-ai-development/adr/OWNER-DECISION-DOC-BACKLOG-COUNT-001.md"
    zh-CN: "docs/zh-CN/14-ai-development/adr/OWNER-DECISION-DOC-BACKLOG-COUNT-001.md"
---

# OWNER DECISION — DOCUMENT BACKLOG COUNT CORRECTION

- Decision ID: OWNER-DECISION-DOC-BACKLOG-COUNT-001
- Date: 2026-11-21 UTC
- Authority: Project Owner delegate under Issue #305 comment 7042461592
- Independence: INDEPENDENCE_UNVERIFIABLE; no independent human signature is claimed.

## Decision

The live repository count for the architecture-document backlog under docs/ (excluding docs/en, docs/zh-CN, and docs/governance/documentation-gaps.md) is **27**, not 26.

The registry count and the corresponding GOV-DOC-002 explanatory text are corrected to 27. This is a factual inventory correction only. It does not change the declared scope, the governed roots, the excluded directories, DM-14, or any classification rule.

The count was observed directly by the local GOV-DOC-002 checker on the PR #438 worktree. The checker reported 27 documents on disk and rejected the registry's declared count of 26.

## Mirror treatment

The machine-authoritative registry remains 00-governance/document-scope-registry.yaml. The docs/en and docs/zh-CN YAML copies are non-authoritative documentation mirrors only; repository tooling must continue to read the root registry. They are included solely to satisfy the repository's bilingual change-pairing contract.

## Acceptance and limits

- The root registry declares 27 docs backlog documents.
- The policy's English and Chinese count statements are corrected to 27.
- GOV-DOC-002 remains active and normative after this factual correction.
- No source code, CI workflow, test code, or Runtime implementation is changed.
- The local verification is a structural document-management check, not a claim that GitHub Actions ran or passed.
