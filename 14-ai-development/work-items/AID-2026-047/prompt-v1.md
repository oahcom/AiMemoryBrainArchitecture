# AID-2026-047-PROMPT v1 — Type the delivery attempt ledger for Memory Context

## User dispatch

Repository: `oahcom/AiMemoryBrainArchitecture`.
Base: `main` at `709914f5` (observed 2026-11-22).
Task: implement row 111 of `06-memory-context/context-implementation-coverage.md` — "Delivery queue attempt identity, retries and ACK separation" (`phase-3.7 §4`) — as domain types in `crates/memory-context`, and correct the coverage row in both languages.

## Authorized scope

- Add `crates/memory-context/src/delivery_ledger.rs` with `DeliveryId`, `DeliveryAttemptId`, `DeliveryAttempt`, `DeliveryAck`, `AckDisposition`, `DeliveryLedger`.
- `DeliveryAttemptId::new` rejects empty and whitespace-only input.
- `DeliveryAttempt::first` and `DeliveryAttempt::retry` model attempt identity and the retry chain; a retry whose predecessor belongs to a different delivery is rejected.
- ACK is issued against a `DeliveryId`, never against a `DeliveryAttemptId`; the type system must make "ACK this attempt" unrepresentable.
- `DeliveryLedger::classify_ack` distinguishes `Accepted`, `Late` (superseded delivery) and `UnknownDelivery`, and never silently drops a late ACK.
- Re-export the new public items from `crates/memory-context/src/lib.rs`; do not change existing public type semantics.
- Correct row 111 of `06-memory-context/context-implementation-coverage.md` and `.zh-CN.md`.

## Constraints

Do not modify `build_context`. Do not implement transport, a real queue, or an ACK consumer (that is row 97, which depends on this row). Do not add `#[ignore]` tests. Do not add dependencies. Do not change the `Display` impl of `ContextError`. Keep English and Chinese coverage rows synchronized.

## Verification requested

Run `cargo fmt --all -- --check`, `cargo clippy --workspace --all-targets -- -D warnings`, `cargo test --workspace --all-targets` and the bilingual gate on Windows natively with `CC=zigcc AR="zig ar"`. Record exact outputs. If execution is unavailable, report NOT RUN; do not claim PASS.

## Provenance

Frozen from the user-provided task dispatch in this ChatGPT conversation on 2026-11-22. Raw platform payload bytes and session identifier are not exposed.
