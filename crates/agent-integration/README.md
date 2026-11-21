# Agent Integration Reference Model

This crate is a deterministic Rust reference model for two contracts:

1. Adapter operation authorization by capability tier.
2. Rejection of writes to protected request regions and to a frozen inference request.

Run from the repository root:

```sh
cargo test -p agent-integration
```

The test suite contains four unit tests. Test execution status for this delivery: **NOT RUN (execution由派工方完成 / execution by dispatcher)**.

This is not a production Adapter. It performs no real model inference, network transport, persistence, BMCP negotiation, or production telemetry. The model validates operations and returns typed `AdapterError` enum values.

The two implemented inference-boundary cases were selected because `inference-boundary-model.md` marks both as DECIDED: (a) protected regions are not Brain-writable, and (b) a request is immutable after its assembly snapshot is frozen. Version-gap reconciliation remains specified but is intentionally outside this minimal model.
