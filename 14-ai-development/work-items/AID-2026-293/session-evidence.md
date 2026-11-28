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
        - "14-ai-development/work-items/AID-2026-293/manifest.yaml"
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
    canonical_scope: "Implementation-session identity, actual input/output provenance, and validation record for AID-2026-293."
    canonical_scope_id: "ai-development/aid-2026-293-session-evidence"
    canonical_scope_keywords:
      - "AID-2026-293"
      - "work-item registry validator"
      - "registry schema"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Session Evidence — AID-2026-293

## Session role / use case

Implementation session for the canonical work-item registry validator. The work
package adds the registry record schema verbatim from the specification, a
read-only validator that reads registry blobs from a Git tree, its regression
suite, and the CI job that runs it. Repository changes are applied in an
isolated worktree (`D:\code\_aimb\wt-validator`) and pushed to a feature branch;
no claim is made that any check ran before it did.

## Actual AI input

The implementation sub-session received the work package prompt snapshotted at
`14-ai-development/work-items/AID-2026-293/prompt-v1.md`, whose exact byte count
and SHA-256 are pinned in the manifest. Its binding parts:

- The only authority for the validator behaviour is `reply-6b07c97e-080615.md`
  lines 3–335 (§1 of the registry validator specification), and the only
  authority for the record schema is `reply-6b07c97e-182004.md` lines 24–747.
  Both are used verbatim: the schema bytes are copied, not re-derived, and no
  rule is added that the specification does not state.
- The following behaviours are mandatory and each needs its own case: reading
  `work_item_id` from file content rather than from a directory name; one ID on
  two paths as `VIOLATION`; parse failure as fail-closed with the
  specification's own classification; schema failures for enum range,
  `additionalProperties`, a missing-state record carrying `value`, a `KNOWN`
  without `value`, and an invalid `work_item_id`; prompt pin verification
  against committed bytes; the INDEX anti-silent-row-loss mechanism; the JSONL
  output and exit-code contract.
- `check_manifest_blob_pins.py` is adjudicated by §1.4, not by preference.
- No registry data file is migrated in this change; that is phase C.

## AI-visible output

The session produced, in the candidate tree:

- `00-governance/schemas/work-item-registry.schema.json`, byte-for-byte the
  JSON body of the specification (16042 bytes, LF only, SHA-256
  `aeed9eae06468493b298924e7f7bad7b2604dbd71e3bb046727c6434f7acd5ed`).
- `scripts/ci/check_work_item_registry.py`, the validator, placed beside the
  other `scripts/ci/check_*.py` gates because the specification names that path.
- `scripts/ci/test_check_work_item_registry.py`, 33 cases over throwaway Git
  repositories.
- One new job in `.github/workflows/gates.yml` that runs the suite and then the
  validator against the candidate tree.
- One narrow admission rule in `scripts/ci/check_repository_hygiene.py` for the
  schema's exact path, because JSON is admitted only at named configuration
  paths and the schema could not land without it.

The session also recorded a conflict it could not resolve by preference: the
work package forbids touching `INDEX.md`, while `scripts/check_traceability.py`
T-04 fails on a manifest that exists on disk but is not indexed. One row was
added, and the conflict is reported rather than hidden.
