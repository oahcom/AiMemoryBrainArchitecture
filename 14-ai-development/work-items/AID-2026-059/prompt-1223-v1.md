---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "This file records the assignment text one agent received in a multi-agent session. It is transcribed, not captured as a platform payload: the session transport was not recorded, so the digest pinned in the manifest proves the committed file has not changed since it was pinned, not that this is the byte-exact string any model received."
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
---

# Executed prompt snapshot — Issue #1223

## Assignment

Repair the duplicate-line blindness in `scripts/check_declared_check_contexts.py`,
with the minimum diff that works.

The declared-context block in `14-ai-development/PR-GOVERNANCE-001.md` is read by
`declared_contexts()` as a list, then compared to the platform's required contexts
after both sides are collapsed to `set()`. Set difference cannot see multiplicity,
so a name listed twice is invisible: seventeen declared lines pass against a
sixteen-element protected set, and the `::notice::` line reports `17` while the
comparison used `16`.

## Constraints

- Exit code `1`, not `2`. `2` is reserved in this file for `INCOMPLETE` — a
  condition that could not be evaluated at all. A duplicate is a condition that
  was read successfully and is wrong.
- Keep the two existing set-difference directions and their message wording
  unchanged.
- Do not touch `fetch_protected_contexts()` or the `/branches/{branch}` endpoint.
  Issue #1224 requires that endpoint stay as it is; the conditional
  `--protection` form is explicitly forbidden.
- No new dependency. `Counter` is acceptable from the standard library; the
  current guard uses a comprehension instead, which is fine at n=16.
- Do not change `declared_contexts()`'s return type or its `None` semantics:
  callers depend on `None` meaning "block absent", which is `INCOMPLETE`.

## Acceptance

- A named test that fails when the guard is deleted, with `AssertionError` rather
  than a traceback.
- The unmodified sixteen-line block against the unmodified sixteen names still
  returns `0`. Both directions are required; a guard that returns `1` for
  everything would satisfy the first alone.
- Test count for `scripts/test_check_declared_check_contexts.py` rises from 12.
- `tests/session_evidence` does not regress.

## Provenance

This is the assignment as recorded by the orchestrating session. The work was
performed by a delegated implementation agent; the orchestrating session
independently re-ran the mutation and the two-direction check before accepting
it, and those measurements are in the paired session-evidence record.
