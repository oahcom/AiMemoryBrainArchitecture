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
        - "AID-2026-267/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Implementation evidence is provisional until exact-Head CI and independent review are recorded."
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
    canonical_scope: "Execution evidence for Issue #134 required/declaration/production gate closure"
    canonical_scope_id: "ai-development/aid-2026-267-required-declared-produced"
    canonical_scope_keywords:
      - "required-contexts"
      - "declared-contexts"
      - "produced-contexts"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# AID-2026-267 — Implementation evidence

## Attribution and authority

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Issue: #134 (remains OPEN)
- Base: `main` at `f18adc9fa1d06837433a09498f5297bf13b35756`
- Branch: `fix/aid-267-required-declared-produced`
- Work Item: `AID-2026-267`, provisional allocation
- Attribution: `user-authorized operator (delegated by account owner)`
- Date: 2026-11-27
- This implements the Owner's existing ruling; it is not a new Owner adjudication or natural-person Owner signature.

## Existing state discovered at base

The checker already read the public `/branches/main` payload and compared
declared/protected sets, but it required equality and did not emit the exact
three-count/two-difference closeout record. Its tests already injected a
required-only context and an exception, but did not assert the unavailable
input/reason or the None return. The existing workflow directly runs the
checker and its unittest module; neither invocation is warn-only.

## Implementation

- The semantic contract is now the inclusion chain `required ⊆ declared ⊆ produced`.
- The checker reports `required_not_declared` and `declared_not_produced`.
- A required-only injected context is a named exit-1 violation.
- An exception or None payload is an exit-2 INCOMPLETE result naming
  `branches/main.protection.required_status_checks.contexts` and the cause.
- Success reports declared, required and produced counts, both empty differences,
  and the required notice format.
- The live API endpoint remains `GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main`;
  no snapshot or new credential is introduced.

## Verification status

- Exact-Head self-test: PENDING CI.
- Live checker on exact PR head: PENDING CI.
- Injected required-only probe: encoded as a deterministic unit test; PENDING CI.
- Injected exception and None probes: encoded as deterministic unit tests; PENDING CI.
- Workflow hard-failure wiring: source readback confirms direct `run: python3 scripts/check_declared_check_contexts.py` and `set -euo pipefail` for the self-test; exact-head workflow run PENDING.
- 16 required contexts: PENDING exact-Head refresh.
- Independent review: NOT ASSIGNED / NOT RECORDED.
- Merge: NOT AUTHORIZED by this task; stop before merge.

## Unresolved

No CI result, independent review, or Owner acceptance is claimed in this record.
