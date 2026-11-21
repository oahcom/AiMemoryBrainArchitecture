# Agent Integration Reference Model

This crate is a deterministic Rust reference model for:
1. Adapter operation authorization by capability tier.
2. Protected inference-boundary write rejection.
3. Session-scoped context delivery through `ContextDeliveryAdapter`.

Run from the repository root:

```sh
cargo test -p agent-integration
```

The suite contains **eight unit tests**: the four original authorization/boundary tests and four delivery lifecycle tests (successor apply, stale/skipped rejection without mutation, clear/reset, and disconnect/reconnect reporting).

The `InMemoryContextDeliveryAdapter` stores snapshots and connection state only in process memory. It enforces exact-successor versions (starting at 1 for a new or cleared session), records only successful applies, clears applied state on forget/revocation, and reports the last applied version after reconnect.

**NOT IMPLEMENTED:** real transport; per-runtime Agent integration; durable delivery ledger or durable session state; automatic retry/re-delivery; production reconciliation or attestation. Reconnect is not evidence of remote Agent state. No real model inference, provider integration, BMCP negotiation, or production telemetry is performed or claimed.

The version-successor check is not snapshot/delta reconciliation: production gap recovery remains out of scope.
