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
        - "14-ai-development/work-items/AID-2026-251/evidence.md"
        - "Issue #266"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Incremental AC4 repair; Actions evidence is recorded after the run."
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
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - "work-item-manifest"
      - "AC4"
      - "documentation-reference"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-251 AC4 incremental repair evidence

## Scope and carrier

This is an incremental repair to AID-2026-251, not a new Work Item. No AID-2026-291 directory or other new Work Item identifier is created. The existing AID-2026-251 manifest is not rewritten; this file records only this repair's changes and measured results.

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Baseline main at branch creation: `31b305d7c8665d0496cea00d2b0acb6626bde072`
- Independent review pin supplied for the R2 fact package: `6f597e2dd8b6e879bf7539aa16b88a39504d9c49`
- Historical cohort tree: `e47dd6f0`
- Repair branch: `fix/aid-2026-251-ac4-repair`
- Related issue: #266
- Attribution: user-authorized operator (delegated by account owner)
- Date: 2026-11-27
- Authority: 代理裁决，非自然人 Owner 签署

PR #1366 is not the carrier for this repair. It is intentionally untouched: no commit was pushed to it, its metadata/body were not changed, and it was not closed. Its unrelated #265 association and mergeability state are not altered by this work.

## Design decision: parser option A

Option A was selected. The GOV-DOC YAML subset parser now accepts only a flat sequence item mapping such as `- path: value` followed by sibling `relationship: value` entries at the sequence item's child indentation. Duplicate keys and malformed pairs are rejected. Nested mappings and nested sequences remain unsupported. This is the narrowest parser extension that accepts the documentation record shape without broadening the YAML language generally.

A dedicated regression script, `scripts/test_check_document_management_sequence_mapping.py`, checks the schema-style sequence-of-mapping input, nested metadata parsing, and continued rejection of nested mapping structures.

## AC4 schema and checker changes

- `documentation` remains required and must contain at least one mapping.
- Each entry requires `path` and `relationship`.
- Paths must be repository-relative and must exist in the selected Git tree (`git ls-tree -r --name-only`).
- The `.md` suffix restriction is removed. `.py`, `.yaml`, and other real repository paths are accepted.
- Relationships include `code` and `schema` in addition to the prior values.
- Session evidence names accept `session-evidence*.md`.
- The checker separates AC4 documentation findings from other schema findings, pins a legacy baseline tree, rejects newly introduced violations with exit 1, and allows only reductions against the pinned legacy finding set.
- The existing `work-item-manifest-schema` workflow job is replaced in place and runs the parser regression, AC4 fixture tests, the checker, and the cohort batch report.

## Historical cohort migration

The cohort is the 83 manifest paths in tree `e47dd6f0`: 82 `AID-2026-*` manifests plus `FIX-2026-P1-T1/manifest.yaml`. Only a new top-level `documentation` block is appended to each cohort manifest. The entries are selected from paths already referenced by that same manifest and verified against the pinned current-main tree at branch creation. No other manifest fields are rewritten.

`AID-2026-030` points to its actual `.py` deliverable, `scripts/verification/sqlite_process_conformance.py`, with relationship `code`; no Markdown deliverable is invented.

The four logical migration batches are positions 1–21, 22–42, 43–63, and 64–83 in the pinned cohort ordering. The Actions batch report records before/after AC4 violation counts and the per-manifest list. Exact run output is appended below only after it is observed from GitHub Actions.

## Session role / use case

Role: delegated implementation operator repairing the existing AID-2026-251 contract and migrating its pinned historical cohort.

Use case: close #266 AC4 by ensuring every historical cohort Work Item has a non-empty, real, tree-resolvable documentation reference and that the parser and CI gate accept and enforce that shape.

## Actual AI input

The user supplied R2 as the authoritative ruling: repair AID-2026-251 rather than open a new AID; use branch `fix/aid-2026-251-ac4-repair`; leave PR #1366 untouched; choose parser option A; require non-empty documentation, Git-tree path existence, removal of the `.md` restriction, a failing exit code for new violations, and migrate the 83-manifest cohort using only paths already referenced by each manifest.

## AI-visible output

The assistant created the repair branch from main, extended the parser narrowly, revised the schema and checker, replaced the existing workflow job with a hard-gate invocation plus regression tests, and appended documentation references to the 83 cohort manifests. GitHub commit and Actions results are recorded in the verification section after they are fetched.

## Verification results

Pending GitHub Actions execution. No check result, exit code, required-context state, merge SHA, or post-merge blob verification is claimed until observed.
