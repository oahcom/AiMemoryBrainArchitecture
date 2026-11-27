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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-251/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "CI and post-merge verification pending."
    usage_status: Active
    modification_status: Active-Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Candidate
    canonical_scope: "Work Item manifest schema v1 and read-only inventory validation"
    canonical_scope_id: "ai-development/work-item-manifest-schema-v1"
    canonical_scope_keywords:
      - "work-item"
      - "manifest"
      - "schema"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-251 — Work Item manifest schema

## Scope

Define a machine-readable schema for Work Item manifests under
`14-ai-development/work-items/`. The schema covers required top-level keys,
`documentation` references, the `session_evidence` sequence, and the
`implementation` mapping. The checker reports legacy records without
rewriting or migrating them.

## Files

- Schema: `14-ai-development/work-items/work-item-manifest.schema.yaml`
- Checker: `scripts/ci/check_work_item_manifest_schema.py`
- Workflow: `.github/workflows/gates.yml`

## Baseline

The exact current-tree inventory is 108 Work Item manifest files at base
`f18adc9fa1d06837433a09498f5297bf13b35756`. The validator prints the
compliant/violation counts and every offending path and reason. A successful
workflow run is the authoritative measured output; no local or unexecuted
count is represented as a test result.

## Authority

署名：user-authorized operator (delegated by account owner)
日期：2026-11-27

代理裁决，非自然人 Owner 签署。
