# Mature Mechanism Comparison

| Mechanism | Mature component can provide | Memory Brain invariant that remains domain-owned |
|---|---|---|
| PostgreSQL MVCC | Snapshot semantics, row versions, transactional visibility, WAL durability | Define canonical authority, serialization key, Fence/admission/publication transaction membership and read predicate |
| SERIALIZABLE transactions | Detect/reject serialization anomalies among transactions in one DB | Ensure all relevant records and final visibility gate share that transaction; retry without changing semantic identity |
| Row lock / advisory lock / CAS | Serialize a target/authority-local critical section or guard a version | Define lock scope, monotonic generation, stale-worker rejection and prohibit cross-domain token comparisons |
| Fencing token | Reject stale lease holders when protected resource checks token | D owns token meaning; every writer enforces it at final commit, not only admission |
| Distributed lease | Temporary ownership and liveness coordination | Lease expiry is not terminal evidence; stale workers remain fenced; unresolved work blocks barrier |
| Transactional Outbox | Atomically persist state change and notification intent | Outbox is not visibility authority; delivery does not prove downstream suppression |
| Temporal / durable workflow | Durable orchestration, retries, timers, recovery and workflow history | Workflow completion cannot replace D barrier proof, I inventory, target ACK or Storage commit receipt |
| Tombstone + compaction | Logical deletion marker and eventual physical cleanup | Tombstone retention, lineage closure, restore replay and read-path suppression are domain semantics |
| Backup/PITR generation | Restore point, WAL continuity, timeline metadata and recovery mechanics | Current Forget/authorization high-water must survive backup rollback and gate service release |
| Index watermark | Contiguous indexing progress | Watermark is not Forget proof; every candidate is revalidated against canonical Fence |

Recommendation: use a mature transactional database for single-authority serialization and durable ledger, subject to measured isolation/HA behavior. Use a durable workflow engine for orchestration and retries, not as visibility source of truth. Keep D Forget semantics, I inventory/authorization policy, F disclosure rules, G Applied meaning and H ACK scope as domain contracts.

No product automatically solves closed-world producer/recipient inventory, lineage completeness, semantic idempotency, Global Forget policy or what counts as inference-visible disclosure.
