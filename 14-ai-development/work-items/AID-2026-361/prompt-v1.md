---
document_metadata:
  domain: ai-development
  role: reference
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
        - "14-ai-development/work-items/AID-2026-361/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "This is a normalized work-brief reconstruction, not a byte-identical capture of the original platform prompt. Provenance remains NOT_VERIFIED."
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Work brief — AID-2026-361

This file is a normalized reconstruction of the implementation brief available
for this work item. It is not represented as the byte-identical original
platform prompt. The original prompt identifier and version were not recorded;
the executed-prompt provenance therefore remains `NOT_VERIFIED`.

## Objective

Implement a fail-closed review-record integrity ratchet for work-item manifests
in `oahcom/AiMemoryBrainArchitecture`, comparing finding identities in the
invocation's base tree with those in its head tree.

## Scope

- Add the nine-key review contract parser and semantic validation to
  `scripts/ci/check_repository_hygiene.py`.
- Reject malformed, incomplete, ambiguous, or invalid review records.
- Preserve the narrowly accepted legacy bare `review: PENDING` form.
- Compute the ratchet as head finding identities minus base finding identities,
  using `(manifest_path, violation_code)` as the finding identity.
- Keep baseline selection bound to the invocation's `--base` argument.
- Add regression tests, including malformed YAML shapes, parser edge cases,
  base-to-head finding mutations, and merge-history fixtures where applicable.
- Keep the change within the checker and its tests; do not add required CI
  contexts, alter workflows, or change branch protection.

## Verification requirements

- Run the complete repository-hygiene test suite.
- Run the ranged checker against the exact base and head commits.
- Run the M1–M5 mutation sequence: M1–M4 must introduce exactly one target
  finding each; M5 must restore a zero-finding result.
- Record exact tested base/head SHAs and runtime evidence.
- Obtain an independent review of the exact final head before merge.

## Attribution and limitations

The implementation session identifier supplied for this work item is
`6b093317-85b8-83ec-9aa9-91b47ca5f770`. The original platform prompt ID/version
and byte-identical prompt payload are not available in the current record.
This reconstruction must not be described as the original executed prompt.
