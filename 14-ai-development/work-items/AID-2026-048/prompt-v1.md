---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null

    evidence_verification:
      verification_status: Unverified

    usage_status: Active
    modification_status: Modified

  authority:
    canonical_status: Canonical
    canonical_scope: "Frozen dispatch prompt for AID-2026-048, the delivery lifecycle and ACK consumer for Memory Context."
    canonical_scope_id: ai-development/aid-2026-045-prompt
    canonical_scope_keywords:
      - aid-2026-045
      - delivery-lifecycle
      - ack-consumer
    canonical_conflict_status: None
    normative_status: Informative
---

# AID-2026-048-PROMPT v1 — Implement the delivery lifecycle and ACK consumer for Memory Context

## User dispatch

Repository: `oahcom/AiMemoryBrainArchitecture`.
Base: `main` at `4a7624da` (observed 2026-11-22).
Task: implement row 97 of `06-memory-context/context-implementation-coverage.md` — "Delivery lifecycle, late ACK and supersession" (`context-versioning.md §9`) — as a state machine and ACK consumer in `crates/memory-context`, on top of the attempt ledger delivered by AID-2026-044, and correct the coverage row in both languages.

## Authorized scope

- Add `crates/memory-context/src/delivery_lifecycle.rs` with `DeliveryState`, `DeliveryRecord`, `DeliveryLifecycle`, `AckOutcome`.
- `DeliveryState` is a five-state machine: `Pending`, `Delivered`, `Acknowledged`, `Superseded`, `Abandoned`. Terminal states reject every outgoing transition.
- `max_attempts` is the maximum number of attempts a delivery may record, the first attempt counted; recording the attempt that reaches the limit moves the delivery to `Abandoned` and returns `Ok`.
- `consume_ack` distinguishes `Accepted`, `Duplicate`, `Late { superseded_by }`, `UnknownDelivery` and `StaleAttempt`, and records each rather than dropping it. An unknown delivery is a normal protocol observation and returns `Ok`, not an error. A duplicate ACK is idempotent and increments the ACK counter.
- An `Abandoned` delivery rejects ACKs for both its current and its obsolete attempts with `ContextError::IneligibleLifecycle`; a terminal state must not be rewritten by an ACK.
- `supersede` requires the replacement delivery to be already enqueued, and rejects superseding an `Acknowledged`, `Superseded` or `Abandoned` delivery.
- Re-export the new public items from `crates/memory-context/src/lib.rs`; do not change existing public type semantics.
- Correct row 97 of `06-memory-context/context-implementation-coverage.md` and `.zh-CN.md`.

## Constraints

Do not modify `build_context` or `delivery_ledger.rs`. Do not implement persistence, transport, a real queue, or a supersession cascade. Do not add `#[ignore]` tests. Do not add dependencies. Keep English and Chinese coverage rows synchronized.

## Verification requested

Run `cargo fmt --all -- --check`, `cargo clippy --workspace --all-targets -- -D warnings`, `cargo test --workspace --all-targets`, `cargo test -p memory-context --test delivery_lifecycle` and the bilingual gate on Windows natively with the Zig toolchain. Record exact outputs. If execution is unavailable, report NOT RUN; do not claim PASS.

## Provenance

Frozen from the user-provided task dispatch in this ChatGPT conversation on 2026-11-22. Raw platform payload bytes and session identifier are not exposed.
