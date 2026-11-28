---
document_metadata:
  domain: ai-development
  role: work-record
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-350/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Figures in this record were produced by operator-run commands on 2026-11-28 against origin/main 73b3ebbee; no independent reproduction is claimed."
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
    canonical_scope: "Record for AID-2026-350; this record does not establish normative requirements or acceptance."
    canonical_scope_id: "ai-development/aid-2026-350-record"
    canonical_scope_keywords:
      - "AID-2026-350"
      - "runtime invariant"
      - "owner decision"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-350 — Evidence

Base: `origin/main` `73b3ebbee1a77b05e361990e0fd9f0911e00f097`.

## E1 — the three code positions

```
crates/agent-integration/src/lib.rs:462   pub enum DeliveryState { ... }
crates/agent-integration/src/lib.rs:474   is_terminal -> Applied | Rejected | Expired | Superseded
crates/memory-context/src/delivery_lifecycle.rs:36   pub enum DeliveryState { ..., Acknowledged, Superseded, Abandoned }
crates/memory-context/src/delivery_lifecycle.rs:53   is_terminal -> Acknowledged | Superseded | Abandoned
crates/memory-context/src/delivery_lifecycle.rs:305  record.state = DeliveryState::Acknowledged;
crates/memory-compiler/src/admission.rs:665          register_producer_work -> state_json = Accepted
crates/memory-compiler/src/admission.rs:578          fn transition_work_state
crates/memory-compiler/src/lib.rs:653-656            PublicationDisposition::Suppressed
```

## E2 — the adjudication

An independent reviewing session adjudicated all three on 2026-11-28:

- drift-03: real defect, HIGH. Minimal boundary is that ACK records transport
  confirmation and must not be read as application success. Unifying the two
  enums is a larger change and out of this defect's scope.
- drift-04: real defect, HIGH. No production path advances `Accepted` to a
  terminal state, so a lost or failed worker leaves the item permanently
  `Accepted`.
- tests-01: real defect. A generic operation-level suppression does not satisfy
  the extraction-and-normalization requirement, which demands the rejected
  participant identity, the `StorageVisibilityParticipantRef` and the
  publication tuple identity.

Each conclusion ended with an Owner decision as the blocking condition. That is
the finding this record makes citable.

## E3 — what this record deliberately does not contain

- No implementation proposal, no recommended option, no code.
- No assertion that a decision exists, that an approval was granted, or that the
  defects are closed.
- No new normative requirement: the file is `normative_status: Informative`.

## E4 — gate results

```
check_document_management.py --require-changed origin/main   PASS (incremental)
check_bilingual_docs.py                                      PASS
check_traceability.py --index-only                           PASS, 0 errors
```

## E5 — what is not claimed

No CI run, review verdict or acceptance decision is claimed. The three defects
remain HIGH and open.
