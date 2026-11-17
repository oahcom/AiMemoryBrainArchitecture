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
| P0-05 | Complete Option A A-01..A-05 L1/L2 clarifications, exact D acceptance, independent restore anti-rollback, then L3 and L4 proofs | Storage + A/COC + I/D | Gate A complete; Gate B persistent COC; Gate C fault campaign; same-XID proof | JF-10 A/B/C |
| P0-06 | Close C/G/H final-request, provider outcome and Applied contract | C/G/H + I/D consumers | Exact contract approvals; provider close-vs-send; same idempotency key; negative conformance | G2/G4 |
| P0-07 | Bounded durable ingress → canonical commit/cursor vertical slice | E/D/Storage; engineering lead | Durable ACK, outbox, idempotent replay, canonical cursor atomicity, recovery proof; only after P0-02..05 | implementation entry |
| P0-08 | Safe structured/lexical retrieval and Forget-safe index/cache rebuild | F + D/I/Storage | Permission/fence before ranking; stale projection suppression; rebuild/restore proof | implementation verification |
| P1 | Context delivery, Adapter integration and historical/current Applied handling | G/C/H + I/D | exact Applied predicate and provider outcome; version/reconnect/late evidence tests | applied workflow |
| P2 | Vector/ANN, reranking, entity resolution, consolidation and conflict-resolution intelligence | F/D/E/B | labeled evaluation set, measurable benefit, bounded resources, Owner ADRs | deferred capability entry |
| P3 | High concurrency, distributed scale-out, advanced autoscaling and multi-region operations | Engineering/Storage/I | measured workload and proven need; deployment/DR ADR and fault evidence | production scale gate |

P0 is not one monolithic phase. P0-01..06 are authority and proof prerequisites; P0-07..08 are bounded implementation work only after their named dependencies are satisfied.

## Additional root-first blockers

- B protocol bundle currentness (H/D/C/I/Storage) is a P0/P1 freeze prerequisite: v3.2.9 is stale; Storage v3.3.0 or equivalent must bind the current exact Owner/CI set and be accepted by all relevant Owners and A.
- Option A must not be called L1 closed until A-01..A-05 are adopted and D's exact Storage ADR decision is recorded. L3 and L4 remain separate proofs.

## First-release shape

Prefer a local-first Rust modular monolith with logical Owner boundaries, one bounded I PolicyDomain, one canonical authority/transaction domain if approved by Storage/D/I, structured + lexical retrieval, rebuildable projections and a narrow Adapter. This is a candidate profile, not a technology freeze.

## Explicit sequencing rules

- No production-data retrieval before permission and Forget suppression are enforced.
- No canonical publication before D/E/I/Storage atomicity is specified and proven.
- No Applied status before C/G/H final-request and provider-side-effect semantics are accepted and tested.
- No multi-PolicyDomain atomicity in the first profile.
- No vector/reranker/graph feature may displace unresolved P0 correctness work.

See DEP-DAG-002, DEFERRED-002, READINESS-002 and GATE-002.


## Source freshness / assessed baseline

This assessment's source-evidence baseline is pinned to main commit `b372b62c640a2b656e54b6db62a4ee67d7d8c001`. At publication, the observed main HEAD is `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f` (a later revert commit); this later HEAD is not silently substituted for the assessed baseline. Before any Gate closure or freeze decision, refresh every cited Owner artifact and repeat the delta review against that HEAD. The Storage L1 topology source is separately pinned to Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`, branch `session-storage-consistency-forget-atomicity-2026-11-16`; §8 selects Option A for L1, while L4 physical conformance remains OPEN.
