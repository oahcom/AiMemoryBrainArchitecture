# Root-first Development Priority Roadmap — PRIORITY-002

- Version: 1.0.0; baseline `b372b62c640a2b656e54b6db62a4ee67d7d8c001`.
- Status: planning recommendation only; not implementation or Gate authorization.

## Unified priority

| Priority | Work | Owner | Entry/exit evidence | Gate |
|---|---|---|---|---|
| P0-01 | Name runtime repo, accountable engineering lead, maintainers, build/CI and contract-to-code traceability | Project authority/A coordinates | Canonical repo/branch; named RACI; reproducible build and CI; ownership accepted | G5/G7; Issue #7 |
| P0-02 | Close domain identity, Fact/Claim, evidence and temporal semantics | B; consumers accept | Approved B ADR; exact Blob; typed cases; consumer adoption | G2/G3 |
| P0-03 | Close I security governance, trust, revocation and closed-world inventory | I + external authorities | Signed I36-GOV-01..10 decisions; InventorySealReceipt; target/backup/recipient enumeration | G2/G4 |
| P0-04 | Close D/E/I/Storage admission, lineage, Forget fence and visibility composition | D/E/I/Storage | Exact Owner decisions; both race orders; crash/ACK-loss/stale lease; hidden-on-UNKNOWN | G3/G4 |
| P0-05 | Complete L4 physical DB/COC/JF-10 proof for the selected L1 Option A logical profile | Storage + A/COC + I/D | Gate A complete; Gate B persistent COC; Gate C fault campaign; same-XID proof | JF-10 A/B/C |
| P0-06 | Close C/G/H final-request, provider outcome and Applied contract | C/G/H + I/D consumers | Exact contract approvals; provider close-vs-send; same idempotency key; negative conformance | G2/G4 |
| P0-07 | Bounded durable ingress → canonical commit/cursor vertical slice | E/D/Storage; engineering lead | Durable ACK, outbox, idempotent replay, canonical cursor atomicity, recovery proof; only after P0-02..05 | implementation entry |
| P0-08 | Safe structured/lexical retrieval and Forget-safe index/cache rebuild | F + D/I/Storage | Permission/fence before ranking; stale projection suppression; rebuild/restore proof | implementation verification |
| P1 | Context delivery, Adapter integration and historical/current Applied handling | G/C/H + I/D | exact Applied predicate and provider outcome; version/reconnect/late evidence tests | applied workflow |
| P2 | Vector/ANN, reranking, entity resolution, consolidation and conflict-resolution intelligence | F/D/E/B | labeled evaluation set, measurable benefit, bounded resources, Owner ADRs | deferred capability entry |
| P3 | High concurrency, distributed scale-out, advanced autoscaling and multi-region operations | Engineering/Storage/I | measured workload and proven need; deployment/DR ADR and fault evidence | production scale gate |

P0 is not one monolithic phase. P0-01..06 are authority and proof prerequisites; P0-07..08 are bounded implementation work only after their named dependencies are satisfied.

## First-release shape

Prefer a local-first Rust modular monolith with logical Owner boundaries, one bounded I PolicyDomain, one canonical authority/transaction domain if approved by Storage/D/I, structured + lexical retrieval, rebuildable projections and a narrow Adapter. This is a candidate profile, not a technology freeze.

## Explicit sequencing rules

- No production-data retrieval before permission and Forget suppression are enforced.
- No canonical publication before D/E/I/Storage atomicity is specified and proven.
- No Applied status before C/G/H final-request and provider-side-effect semantics are accepted and tested.
- No multi-PolicyDomain atomicity in the first profile.
- No vector/reranker/graph feature may displace unresolved P0 correctness work.

See DEP-DAG-002, DEFERRED-002, READINESS-002 and GATE-002.
