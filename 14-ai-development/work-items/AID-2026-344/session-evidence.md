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
        - "14-ai-development/work-items/AID-2026-344/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Session Evidence structure is aligned to the repository validator; exact-head validation is pending."
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
    canonical_scope: "Implementation-session identity, actual input/output provenance, and validation record for AID-2026-344."
    canonical_scope_id: "ai-development/aid-2026-295-session-evidence"
    canonical_scope_keywords:
      - "AID-2026-344"
      - "merge-group candidate"
      - "session evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Session role / use case

Implementation session for AID-2026-344: close GAP-03 and GAP-04 by validating
the whole merge-group candidate instead of its tail pull request. The session
produced the shared candidate resolver, the merge-group branch of the verdict
script, the two workflow integrations and the offline test suites.

# Actual AI input

The session received the authoritative specification (`reply-6b07c97e-081917.md`,
lines 11-199) and the eight-point task recorded in `prompt-v1.md`. It was asked
for the resolver module, the failure-semantics table, the workflow wiring and the
tests, and it was asked to keep the single-pull-request path unchanged.

The session also received the observed failures of every intermediate revision:
the single-pull-request regression (`tests/session_evidence` 26 failures caused by
`_changed_paths_for_manifest` raising on a missing base), the fixture key
collision that made `gh_tree` return a path string, the missing compare endpoint
in the offline fake API, and the member line that repeated the total verdict
prefix. Each was answered with a corrected function or assertion set, and each
correction was applied verbatim and re-tested.

# AI-visible output

- `scripts/governance/merge_group/candidate.py`: queue paging, prefix resolution,
  the three relations, the failure-semantics table and the `--output`/`--exec`
  entry points.
- `scripts/governance/session_evidence/validate.py`: `IncompleteValidationError`,
  `gh_api`/`gh_tree`/`gh_blob_bytes`/`gh_blob_text`/`gh_compare_paths`,
  `_changed_paths_for_manifest`, `_load_merge_group_contexts`,
  `_run_merge_group_checks`, `_write_merge_group_summary` and the merge-group
  branch of `main`.
- `.github/workflows/session-evidence.yml` and `.github/workflows/bilingual-docs.yml`:
  the candidate resolution step, the self-test steps and the merge-group wiring.
- `tests/merge_group/`: 30 offline tests covering the parser, the relation table,
  the multi-pull-request integration path and the single-pull-request regression.

# Scope of this record

This record states what the session was asked and what it produced. It does not
assert that the evidence is authentic, complete, or produced by the model it
names; the session-evidence gate proves only that the declared files exist in the
head tree and that their bytes are unchanged.
