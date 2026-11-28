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
        - "14-ai-development/work-items/AID-2026-352/manifest.yaml"
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
    canonical_scope: "Implementation-session identity, actual input/output provenance, and validation record for AID-2026-352."
    canonical_scope_id: "ai-development/aid-2026-352-session-evidence"
    canonical_scope_keywords:
      - "AID-2026-352"
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

# Session Evidence - AID-2026-352

## Session role / use case

Implementation session for Issue #266 AC4 and AC6. The work package does not
re-model either acceptance criterion: AC4 already has a normative carrier
(`documentation` in the work-item manifest schema) and AC6 already has DM-13 for
the forward `supersedes` edge. What was missing was data on one side and a
reverse artifact on the other. This session backfills the missing data and adds
the missing reverse-index artifact and its rule.

Repository changes were applied in an isolated worktree (`C:\tmp\p352`) cut
from `origin/main`; no claim is made that any check ran before it did.

## Actual AI input

The implementation sub-session received the task prompt snapshotted at
`14-ai-development/work-items/AID-2026-352/prompt-v1.md`, whose byte count and
SHA-256 are pinned in the manifest. The adjudication that decided the shape of
this change was produced by the ChatGPT session `6b0a1b12-1ddc-83ec-a062-a1ba87fe6020`
in two replies (`reply-6b0a1b12-142939.md`, `reply-6b0a1b12-151518.md`). Its
binding parts:

- AC4 needs no schema change. The acceptance predicates are the five already
  implemented in `validate_against_schema()`: `documentation` present, non-empty
  sequence, `path` and `relationship` per item, repository-relative path that
  exists in the Git tree, `relationship` inside the closed enum.
- No rule may require a reference outside the work-item's own directory: the
  criterion says "relevant documents", not "external documents".
- `AID-2026-284`'s six free-text `relationship` values are violations of the
  existing enum, and its self-reference to its own `manifest.yaml` is not a
  relevant document. Both are corrected; the enum is not widened.
- AC6 chooses option C: `archival_reference` is NOT re-interpreted as a
  supersession back-reference and is not backfilled (769 declared, 0 non-null,
  and the value was never read by any rule).
- AC6's real structural gap is that the policy declares `superseded_by` to be
  CI-derived and repository-policy forbids hand-writing it, yet no generator
  exists. DM-16 is added: a deterministic reverse index generated from the
  full-tree `supersedes` graph, checked as a committed artifact.

## AI-visible output

- `scripts/backfill_work_item_documentation.py`: appends a `documentation`
  block to the 35 manifests that lacked one, from an explicit per-work-item
  mapping (no path guessing). `--dry-run` / `--apply` / `--rollback`, byte
  idempotence asserted after writing.
- 35 `manifest.yaml` files under `14-ai-development/work-items/`, each gaining
  only the appended block.
- `14-ai-development/work-items/AID-2026-284/manifest.yaml`: six enum
  violations and one self-reference removed.
- `scripts/generate_supersession_index.py` and
  `14-ai-development/reports/supersession-index.json`: the DM-16 generator and
  its committed output (two edges, both directions resolved).
- `scripts/check_document_management.py`: `check_supersession_index()`, wired
  after `check_scope_registry()`; DM-13 is untouched.
- `scripts/test_check_document_management.py`: three DM-16 cases (missing
  reverse edge, stale artifact, current artifact) and the fixture change that
  lets a synthetic repository carry the artifact.

## Verification

Commands actually run, with their exit codes, are recorded in the pull request
body. Nothing in this file asserts a result that the PR does not also carry as
command output.

## Explicit non-claims

- AC4 is not claimed to be fully satisfied repository-wide: 119 manifests still
  carry other schema violations (mostly `session_evidence`), unchanged here.
- AC6 is not claimed to close Issue #1257 or the `archival_reference` question;
  that block remains declared-and-unused by decision C.
- No baseline JSON was edited to absorb a new finding.
