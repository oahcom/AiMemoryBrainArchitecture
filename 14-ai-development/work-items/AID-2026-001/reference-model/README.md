# Forget Contract Reference Model (Non-Production)

This directory contains a small executable reference model for the AID-2026-001 Forget contract proposal.

It is intentionally isolated from production architecture and runtime code. The repository baseline inspected for this work contains architecture documents and no src/, tests/, package or service implementation tree. These tests validate only the consistency of this abstract model; they do not establish that any production component implements the contract.

## Run

```
python -m unittest discover -s 14-ai-development/work-items/AID-2026-001/reference-model -v
```

The model uses only the Python standard library. Historical baseline: 14/14 model-level tests passed under Python 3.13.5 (2026-11-18), before the expanded regression cases below. This historical result is not the current suite count and does not imply production conformance.

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


## Expanded regression suite

The current standard-library suite contains 24 model-level unit tests. A dedicated GitHub Actions workflow checks out the exact pull-request head SHA (or the pushed commit SHA on main) and runs this suite when the reference-model files change.

This CI is deliberately scoped to the in-memory reference model. A green run proves only that this abstract model's tests passed. It does not prove production authentication, authorization, persistence, concurrency, replica, index, cache, queue, adapter, context, backup or restore behavior. DFI-001…DFI-022 remain NOT EVIDENCED against production components until the authoritative runtime repository and accountable implementation owners are identified and tested.

The 24 model-level cases are not a substitute for Owner D/Owner I approvals, independent specialist review, independent integration review, full Manifest/schema validation or architecture acceptance.


### Model review correction

The regression suite now also rejects vacuous D-domain completion when the sealed canonical target inventory is empty. Without this guard, Python's `all([])` semantics would allow a zero-target operation to appear D-domain complete. This is a reference-model correction only; production inventory completeness still requires implementation-level proof.
