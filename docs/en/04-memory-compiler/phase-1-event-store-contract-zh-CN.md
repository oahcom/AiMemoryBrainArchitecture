# Phase 1 Event Store Contract

Status: DECIDED semantics / CANDIDATE implementation seam.

The Event Store is the durable custody boundary for source Events. Accepted means Event metadata, payload reference/integrity, idempotency identity, receipt and recoverable processing intent are durably committed. Accepted does not mean compiled, verified, indexed or canonical.

The contract requires explicit Scope, producer identity, payload digest and idempotency key. The SQLite candidate defines the idempotency identity as `(producer_actor_ref, idempotency_key)`: same identity plus same digest returns the original receipt; same identity plus a different digest conflicts. Scope authorization is checked before receipt replay.

The candidate persists the complete envelope, declared payload reference/digest, acceptance time, receipt identity and initial `Pending` processing state in one transaction. It does not store or independently hash payload bytes; payload digest correctness remains an upstream assertion. `replay` returns the original receipt unchanged and does not enqueue or execute work. Queue delivery, processing-state transitions, retention/Forget authorization and schema migration remain outside this adapter.

Replay reuses the original Event identity and recorded acceptance time. Forget/retention checks remain separate policy authority.

The candidate file-backed SQLite adapter uses WAL, synchronous=FULL, foreign_keys=ON and a 5-second busy timeout; in-memory mode retains SQLite's in-memory journal behavior. No queue topology, worker delivery, distributed transaction, throughput target, schema migration or production durability proof is included in this unit.
