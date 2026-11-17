# Forget Contract Reference Model (Non-Production)

This directory contains a small executable reference model for the AID-2026-001 Forget contract proposal.

It is intentionally isolated from production architecture and runtime code. The repository baseline inspected for this work contains architecture documents and no src/, tests/, package or service implementation tree. These tests validate only the consistency of this abstract model; they do not establish that any production component implements the contract.

## Run

```
python -m unittest discover -s 14-ai-development/work-items/AID-2026-001/reference-model -v
```

The model uses only the Python standard library. The observed local result: 14/14 model-level tests passed under Python 3.13.5 (2026-11-18). This does not imply production conformance..

## Covered invariants

- Suppression linearization and terminal Forgotten identity
- No cancellation/rollback after suppression
- Separate D-domain completion and I governance assessment
- Unknown targets and generic ACKs do not count as erasure
- Bounded, expiring exceptions produce only a derived public projection
- Inventory expansion invalidates previous completion evaluation
- Stale lease fencing and request idempotency
- Backup restore applies the latest fence before serving
- Context Remove does not mutate canonical lifecycle
- Authorization denial does not install suppression

## Explicit non-guarantees

No concurrency scheduler, database transaction, WAL, distributed replica, Adapter, index, queue, real authorization provider, backup medium or production service is implemented here. DFI-001…DFI-022 still require implementation-specific fixtures and fault-injection tests. This model is a review aid, not a test substitute.
