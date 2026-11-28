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
        - "14-ai-development/work-items/AID-2026-333/manifest.yaml"
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Implementation, local test execution and live race qualification remain pending."
    usage_status: Active
    modification_status: Modified
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
      - "work-item-uniqueness"
      - "strict-branch-protection"
      - "duplicate-merge"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Session Evidence — AID-2026-333

## Session role / use case

Implementation and acceptance-ruling session for Issue #1341, specifically acceptance row 6.

Related records:

- Issue #1341 — serialized work-item uniqueness.
- PR #1477 — tree-only uniqueness checker.
- PR #1497 — independent review identifying the race.

## Actual AI input

The user supplied:

1. The measured round-one duplicate-claim experiments.
2. The current tree-only checker and its ten-test suite.
3. The current GOV-DOC-002 workflow.
4. The measured branch-protection configuration.
5. The measured absence of repository rulesets and merge queue.
6. The attempted merge-queue ruleset POST and its HTTP 422 response.
7. The repository visibility and owner-type measurements.
8. The constraints on checker ancestry, test execution, and required-context wiring.

The initial merge-queue recommendation was withdrawn after the user supplied the repository eligibility and API rejection evidence.

## AI-visible ruling

The selected prevention mechanism is strict required-status-check branch protection.

The supplementary detector is separate from the original tree-only checker. It compares both parents of a two-parent merge commit against their merge base and reports duplicate AID claims with both parent identities.

The existing uniqueness checker is not modified.

The owner-side strict setting is not accessible to the workflow token and cannot be proven by a repository code change.

## Implementation deliverables

The proposed changes are:

- `scripts/ci/check_work_item_merge_race.py`
- `scripts/ci/test_work_item_uniqueness.py`
- `.github/workflows/document-management.yml`
- `14-ai-development/work-items/AID-2026-333/manifest.yaml`
- `14-ai-development/work-items/AID-2026-333/evidence.md`
- `14-ai-development/work-items/AID-2026-333/session-evidence.md`
- `14-ai-development/work-items/INDEX.md`

## Executed-prompt provenance

The three-round operator prompt snapshot is retained at
`14-ai-development/work-items/AID-2026-333/prompt-v1.md`.

Measured content identity:

- SHA-256: `3a81f756bbd5753c7ceb25ceb8d8069cd2456707b30fde1d8e52c77e0872c9bb`
- Bytes: `33792`
- Git blob object ID: `fb028579b8ab747f6853d016f41b625ccec93035`

The manifest's top-level prompt fields pin the exact file bytes by digest
and Git blob object ID. This establishes content identity, not independent
verification of execution-time provenance. `executed_prompt_provenance`
therefore remains `NOT_VERIFIED`.

## Verification status

The original round-one experiment results are supplied by the user and recorded in evidence.md.

The proposed new test results are expected values, not execution claims.

The operator must record the actual test output and actual GitHub protection response before changing this record's verification status.

## Boundary

No branch-protection setting was changed by this session.

No merge queue was configured.

No live GitHub two-PR race qualification was performed by this session.

No Owner acceptance or Issue #1341 closure is claimed.
