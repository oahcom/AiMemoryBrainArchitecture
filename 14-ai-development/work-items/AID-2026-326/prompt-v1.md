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
        - "14-ai-development/work-items/AID-2026-326/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Prompt snapshot is an authoring reference. Exact transmission provenance has not been independently verified."
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
    canonical_scope: "Implementation instructions for AID-2026-326 required-context execution auditing."
    canonical_scope_id: "ai-development/aid-2026-326-prompt-snapshot"
    canonical_scope_keywords:
      - "AID-2026-326"
      - "prompt"
      - "execution-audit"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Prompt v1 — AID-2026-326

## Task

Implement Issue #1469: actual execution verification for the sixteen
required PR check contexts.

The existing declared-context checker proves:

required ⊆ declared ⊆ produced

The produced set is static workflow metadata. It does not establish that
a required check actually ran and produced a judgment on the current
pull-request head.

## Required implementation

Create:

- `scripts/ci/check_required_context_execution.py`
- `scripts/ci/test_check_required_context_execution.py`
- `.github/workflows/required-context-execution.yml`

The checker must:

1. Accept `--pr`, optional `--repo`, `--json`, `--retries` and
   `--retry-delay`.
2. Read the PR head SHA, mergeable_state and draft.
3. Retry `mergeable_state=unknown`, default five retries at five
   seconds each. Persistent unknown is INCOMPLETE, exit 2.
4. Read check-runs for the exact head SHA.
5. Parse all required contexts at runtime from the
   `declared-check-contexts` fenced block in
   `14-ai-development/PR-GOVERNANCE-001.md`.
6. Select the latest run for each context by maximum `started_at`,
   never by API response order.
7. Distinguish:
   - EXECUTED: all sixteen latest runs completed successfully.
   - ABSENT: at least one required context has no run.
   - STALE: mergeable_state is dirty.
   - FAILED: a latest completed run has a non-success conclusion.
   - INCOMPLETE: API evidence is unreadable, unknown persists, or
     a latest run is not completed.
8. Support `GITHUB_TOKEN` and `GH_TOKEN`.
9. Never interpret authentication or API failures as missing checks.
10. Produce human-readable per-context results or machine-readable
    JSON containing verdict, head_sha, mergeable_state, missing,
    failed, pending, stale and retries_used.

Exit codes:

- EXECUTED: 0
- ABSENT / STALE / FAILED: 1
- INCOMPLETE: 2

## Required tests

Use unittest and inject the API function. No network access.

Cover:

1. Sixteen successful contexts.
2. One absent context.
3. Dirty mergeability.
4. Persistent unknown and retry count.
5. Older failure plus newer success, with reversed list order.
6. API exception.
7. In-progress run.
8. Completed failure distinct from absence.

Additional tests may cover token absence, parser failure and head
mutation during retry.

## Workflow boundary

The workflow must use `workflow_dispatch` with a required PR-number
input.

It must not be added to required_status_checks.

Do not modify:

- `14-ai-development/PR-GOVERNANCE-001.md`
- `scripts/check_declared_check_contexts.py`
- `scripts/test_check_document_management.py`
- branch protection configuration

Do not introduce another required context.

## Evidence and delivery discipline

Provide the four work-item records and one INDEX registration row.

All three Markdown records must have distinct canonical_scope_id
values, bilingual_counterpart and the delegated steward field.

The manifest must record the implementing session and prompt snapshot
fields. Session and prompt provenance remain NOT_VERIFIED unless
independently established.

Do not claim that commands, tests, repository writes or API probes
were executed unless actual execution evidence is available.

The supplied baseline is:

`31c1e5d83e7dad326dbd4b69d4a8e19534718ff1`

The prompt snapshot hash and byte count are deliberately left for
the delivery operator to calculate from the finalized file bytes.
