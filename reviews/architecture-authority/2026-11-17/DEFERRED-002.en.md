# Deferred Capabilities Register — DEFERRED-002

- Version: 1.0.0; historical assessment snapshot `6470f25ca23b8d35c06f60be2326867066418d18` (not current main).
- Deferral is not a waiver of core correctness, authorization, consistency, Forget or mandatory Gate requirements.

| ID | Capability deferred | Owner | Risk | Blocking | Permitted scope | Prohibited scope | Closure criteria / evidence | Deadline / Gate |
|---|---|---|---|---|---|---|---|---|
| DEF-01 | Vector/ANN retrieval and vector DB selection | F | Medium | Non-blocking for safe first slice | Synthetic-data benchmark, recall/precision evaluation, resource measurement | Production serving, authoritative ranking, treating vector index as canonical | Labeled eval set; quality/latency/resource report; delete/rebuild/Forget tests; F recommendation and required ADR | Before P2 entry |
| DEF-02 | Reranking and multi-stage retrieval | F | Medium | Non-blocking | Offline experiments on synthetic/non-sensitive fixtures | Production dependency or bypass of permission/fence prefilter | Measured lift vs. baseline and latency budget; negative authorization tests | Before P2 entry |
| DEF-03 | Entity resolution and automatic identity merging | B/D | High | Blocking for automatic merge; manual research allowed | Candidate ontology/algorithm comparison only | Automatic canonical merge or identity mutation | B-owned identity semantics, conflict policy, reversible merge proof and consumer adoption | Before identity-sensitive implementation |
| DEF-04 | Advanced consolidation/conflict-resolution intelligence | B/D/E | High | Blocking for canonical auto-resolution | Offline candidate evaluation | Auto-promoting uncertain claims to canonical truth | B semantics, provenance, uncertainty/conflict policy, correction and rollback evidence | Before P2 production capability |
| DEF-05 | Multiple vector/graph/search backends | F | Medium | Non-blocking | Comparative benchmark only | Multi-backend production complexity without measured demand | Workload-backed ADR and operational budget | Before P2 |
| DEF-06 | Distributed service decomposition, multi-region and autoscaling | Engineering/Storage | High | Blocking for production scale claims | Topology research and load model | Premature microservices, multi-region writes or scale claims | Measured workload, selected topology, failure-domain and DR proof | Before P3 |
| DEF-07 | Multi-PolicyDomain atomicity | I + Storage | Critical | BLOCKED; not accepted | Single-domain design only | Cross-domain transaction or implied atomicity | New I/Storage normative design, security policy, physical topology and independent conformance | Separate future architecture decision |
| DEF-08 | Cross-BrainAuthority atomic publication/Forget transaction | D + Storage + I | Critical | BLOCKED in v1 | Fan out into independent per-BrainAuthority operations; global completion only after each authority's terminal proof and complete inventory | One atomic operation spanning multiple BrainAuthorityRefs; cross-authority atomicity inferred from a global coordinator | Successor normative ADR with explicit scope/coordinator, ordering, partial completion, restore/recovery and independent physical conformance | Separate future architecture decision; before any multi-authority capability |

## Conditionally accepted non-blocking condition

**COND-NB-01 — Defer vector/ANN production capability**

- Problem: production vector retrieval would add index lifecycle, embedding versioning, stale-state, deletion/rebuild and operational state before baseline retrieval value is measured.
- Evidence: X PR #49 rates cross-module state/recovery complexity high and lists vector/ANN as deferrable; F/D/P PR #46 recommends structured + lexical first.
- Risk: Medium; non-blocking for the first safe slice.
- Permitted: synthetic benchmark and labeled evaluation harness only.
- Prohibited: production serving, canonical authority, bypassing permission/Forget prefilters.
- Owner: F.
- Closure criteria: labeled corpus; reproducible recall/precision and latency/resource report; delete/rebuild/Forget negative tests; explicit F recommendation.
- Deadline: before P2 entry.
- Verification: exact dataset/benchmark commit, commands, results, negative test traces and independent readback.
- Risk acceptance rationale: deferral avoids unmeasured state/operations burden and does not weaken core memory correctness.
- Risk acceptance authority: A, limited to scope deferral; F retains retrieval design authority.
- Escalation: if vector retrieval becomes a P0/P1 dependency or is proposed for production before closure, stop that work and return to A + F review.
- Related Gate: P2 capability gate; G5 for technology selection.

All other open Critical correctness/security/authority items remain DEFERRED or BLOCKED, not accepted as residual risk.


## Current main HEAD / 当前 Main HEAD

The current main HEAD independently observed for this publication is `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`. The earlier `6470f25...` / `b372b62...` values are historical assessment snapshots, not current main. This package has not completed a full source-by-source delta audit against current main; G1 remains PARTIAL and all Gate/freeze restrictions remain in force.
