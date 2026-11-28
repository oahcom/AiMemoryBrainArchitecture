---
document_metadata:
  domain: ai-development
  role: work-record
  steward: "user-authorized operator (delegated by account owner)"
  lifecycle:
    approval:
      decision_status: Draft
      approver: NOT_ASSIGNED
      decision_date: "2026-11-28"
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-031/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Repository facts and the reported ratchet failure were supplied as task inputs; coordinator execution and independent verification remain pending."
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
      - "AID-2026-031"
      - "session identity"
      - "session identity ratchet"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Evidence — AID-2026-031

## Purpose

This record documents the registration and proposed correction of the new session-identity ratchet violation on `origin/main`.

## Supplied repository facts

The supplied base commit is:

`f0843a8f38a420883921cfda96b515204967f885`

The reported session-identity checker result on that commit is:

`SESSION IDENTITY: 92 violations, 91 baselined, 1 new`

The inventory summary is:

`SESSION IDENTITY INVENTORY: no_evidence_section=39`

The single new violation is:

`SESSION_UNPARSEABLE 14-ai-development/work-items/AID-2026-297/manifest.yaml#1 RECORDED value 'MIGRATION-POLICY' is not a supported session identifier`

The reported provenance is commit `6c6f8cfe82d615048cd6379642079c946af71303`, associated with PR #1513.

## Required correction

The AID-2026-297 manifest declaration is to be corrected to:

- `implementing_ai_session: NOT_RECORDED`
- `session_reference_status: NOT_RECORDED`

No UUID or `conv_` identifier is available in the supplied evidence. No replacement identifier is invented.

The existing prompt snapshot digest, prompt byte count, provenance field, and session-evidence reference remain unchanged.

The historical `session-evidence.md` is not rewritten. Its statement records what the historical evidence document declared; it is not the authoritative current manifest declaration. Retaining it preserves the historical record while the manifest is corrected.

## Ratchet evidence

Supplied CI observations:

| State | Head | Run | Result |
|---|---|---|---|
| Last green | `3b4bc0039` | `46109215468` | 91 violations, 91 baselined, 0 new |
| First red | `6c6f8cfe8` | `46109393978` | First failure after PR #1513 |
| Current red | `f0843a8f3` | `46109588406` | 92 violations, 91 baselined, 1 new |

Expected post-correction result:

`SESSION IDENTITY: 91 violations, 91 baselined, 0 new`

This expected result is a target, not an executed test result.

## Registration references

The related live tracking issue is #1534, titled:

`AID-2026-328: Remove human label from NOT_RECORDED session sentinel`

It owns the same policy concern: human labels must not be represented as session identifiers.

The new work-item identifier `AID-2026-031` was supplied as available after repository-wide identifier, history, ref, and open-PR checks performed by the coordinator.

## Verification status

Unverified.

The repository facts and prior CI observations above are coordinator-supplied inputs. The authoring session has not executed repository commands, modified the repository, run tests, committed, pushed, or opened a pull request.

The coordinator is responsible for mechanical file writing, gate execution, commit, push, and PR creation. Any actual results must be recorded after execution.

No CI success, merge, independent review, or Owner acceptance is claimed.
