# Architecture Complexity Assessment — ARCH-CX-002

- Version: 1.0.0; baseline: `main@b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- X source: PR #49, commit `131f91743bd506517ee354d58c277501ca447929`, EN Blob `c509120644d6f7c7223decf3f9f0ee33b0548bb7`, ZH Blob `981a376ddf283ace1e891795c813b17ac4aa3d8b`.
- A disposition: complexity controllability **NOT PROVEN**.

## Five largest complexity bottlenecks

1. Forget → producer admission → dependency/derivative registration → final publication gate. X scores this cross-module chain at 5/5 across its eight dimensions.
2. Global Forget completion across canonical data, derivatives, indexes, caches, contexts, adapters, replicas and backups; these have different proof/terminal semantics.
3. Storage/Consistency transaction, visibility, COC/JF-10 recovery and failover. Storage's module profile is 5/5/5/5/5/5/5/5 with low confidence because L1 Option A is selected but L4 physical engine/deployment remains open.
4. Durable ingress, outbox, lease, retry, replay and canonical cursor coordination across D/E/Storage.
5. Applied/provider outcome composition across C/G/H and I/D authorization/fence evidence.

## Complexity model validation

X uses eight ordinal dimensions (internal, dependency, state, concurrency, recovery, verification, operational, cognitive), scored 1–5. These scores are useful for locating hotspots, not additive project totals, delivery estimates or measured runtime complexity. The highest scores concentrate on D, E, Storage and cross-module Forget/publication. H/I also have substantial responsibility and evidence burden; X appropriately lowers confidence where direct Owner source inspection was incomplete.

## Cross-check and corrections

- Preserve distinct proof objects: Accepted, Compiler Completion, Canonical Commit, Index Applied, Context Applied, Applied, Forget Completion, PublicationReceipt and provider outcome.
- Do not create a service, database, queue, protocol or version boundary for each logical concept without quantified need.
- A local-first Rust modular monolith is the preferred *candidate deployment shape* for first engineering slices. Storage has separately selected L1 Option A (one serializable transaction domain per Canonical Memory authority); actual L4 engine/deployment conformance remains open. This does not merge Owner authority.
- Require each cross-module operation to name one operation ID, authority for each state, finite participant set, linearization point, retry stages, terminal states and recovery action.
- Require every Receipt/Manifest/Applied/Watermark to name issuer, subject, scope, generation/version, durability, freshness and explicit non-claims.
- Derived indexes/caches are never second authorities; stale state must be detectable and rebuildable.
- Complexity reduction must not remove identity, authorization, durable admission, Forget fencing, idempotency, audit, recovery or proof separation.

## Complexity budget and verification threshold

Before any P0/P1 invariant is called verified: direct negative tests, crash-before/crash-after each durable boundary, duplicate/out-of-order/retry/partial-failure/recovery cases, and cross-owner trace correlation are required. Happy-path E2E alone is insufficient.

## Simplification disposition

**MUST PRESERVE:** authority boundaries, typed identity/scope, monotonic fences, idempotency, distinct proof states, recovery/restore, audit, owner-local causal positions.

**CAN SIMPLIFY:** initial physical deployment to modular monolith; one canonical SQL authority domain if Storage/D/I approve and prove it; common operation envelope; rebuildable projections; one I PolicyDomain for the bounded first profile.

**CAN DEFER:** vector/ANN, reranking, graph backend proliferation, multiple providers/backends, multi-PolicyDomain atomicity, distributed service decomposition, advanced autoscaling.

**MUST NOT INTRODUCE:** cross-domain cursor comparison, cache/index as authority, generic Success replacing distinct terminal facts, heuristic JF-10 resolution, process mutex as durable atomicity, microservices without measured need.

## Conclusion

The system is high-complexity and its controllability is **NOT PROVEN**. The architecture can reduce avoidable deployment complexity, but the P0 proof burden remains high. See SYS-RISK-002, DEV-FEAS-002, DEP-DAG-002 and GATE-002.
