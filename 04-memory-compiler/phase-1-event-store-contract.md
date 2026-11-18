# Phase 1 Event Store Contract

Status: DECIDED semantics / CANDIDATE implementation seam.

The Event Store is the durable custody boundary for source Events. Accepted means Event metadata, payload reference/integrity, idempotency identity, receipt and recoverable processing intent are durably committed. Accepted does not mean compiled, verified, indexed or canonical.

The contract requires explicit Scope, producer identity, payload digest and idempotency key. Same identity plus same digest returns the original receipt; same identity plus a different digest conflicts.

Replay reuses the original Event identity and recorded acceptance time. Forget/retention checks remain separate policy authority.

No SQLite implementation, queue topology, distributed transaction, throughput target or production durability proof is included in this unit.
