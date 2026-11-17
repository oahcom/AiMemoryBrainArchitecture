# Three Architecture Alternatives

## Decision framing

The three options are compared against the current F/G ownership model. A "module" means a logical responsibility, not a process, service or crate. No option may weaken Forget, Permission, Security, Authority or exact-version freshness.

## A — Keep separate Retrieval / Activation / Context / Budget

**Shape:** F Retrieval → F Activation Recommendation → G Planner/Budget/Committer → Adapter. F retains scheduler and cache eviction.

- Complexity: low change risk, but overlapping budget/cost/fairness logic remains.
- Correctness: strongest continuity with current owner contracts; duplicated accounting can drift.
- Latency: lowest coordination overhead; repeated plan/estimate cycles possible.
- Throughput: good for independent requests; noisy-neighbor protection depends on F/G local quotas aligning.
- Memory efficiency: good local cache control, weaker global allocation awareness.
- Explainability: clear local decisions but fragmented cross-stage rationale.
- Concurrency: F fair scheduling exists; G concurrent Context capacity sharing needs a bridge.
- Extensibility: each module can evolve independently; new resource types duplicate interfaces.
- Failure recovery: existing F/G recovery boundaries remain; less new shared state.
- Operational cost: lowest migration cost, medium ongoing integration cost.

**Best when:** one or few tasks, modest contention, no evidence that duplicate accounting materially harms performance.

## B — Shared Memory Resource Manager, domain ownership preserved (RECOMMENDED CANDIDATE)

**Shape:** a thin resource-control plane accepts typed requests, reserves budgets, schedules work and emits a decision trace. F still retrieves/ranks/recommends; G still decides Context membership/version/budget sufficiency; D/I remain canonical and security authorities. The manager does not own canonical memory, Context state, cache content or Forget completion.

- Complexity: medium; one shared contract and policy engine, fewer duplicated reservation/fairness mechanisms.
- Correctness: good if manager is advisory/coordinating and all owner gates revalidate; risk if its cached decision is mistaken for authorization.
- Latency: small scheduling overhead; potentially fewer repeated budget negotiations.
- Throughput: better under multi-task contention via reservations and weighted fair queueing.
- Memory efficiency: improves shared token/CPU/RAM/fan-out utilization; cannot guarantee recall quality.
- Explainability: one allocation trace plus owner-specific reasons.
- Concurrency: explicit per-principal/task quotas, reservations, borrowing and starvation controls.
- Extensibility: new resources/policies can be added without merging domain owners.
- Failure recovery: manager outage must fail closed for protected requests or use bounded static reservations; no durable domain state is lost.
- Operational cost: moderate; one policy surface and metrics to maintain.

**Best when:** multiple simultaneous tasks compete for token, CPU, memory, retrieval fan-out or latency budgets.

## C — Full Memory Operating System kernel

**Shape:** a unified kernel owns retrieval, activation, residency, context, budget, eviction and scheduling state.

- Complexity: highest; requires migrating and reconciling F/G state machines and cross-owner boundaries.
- Correctness: potential single policy model, but creates a large trusted computing base and new authority conflicts.
- Latency: possible optimized pipeline; central coordination/locking and serialization can dominate.
- Throughput: can globally optimize, but central scheduler becomes contention point.
- Memory efficiency: theoretical global optimization; risk of overfitting one score across incompatible resource types.
- Explainability: centralized decisions, but complex multi-objective policy may be opaque.
- Concurrency: centralized fairness is possible; one scheduler failure impacts all tasks.
- Extensibility: uniform internal API, but every owner-specific change couples to kernel.
- Failure recovery: new single point of failure; persistent scheduler state, epochs and replay become critical.
- Operational cost: highest implementation, validation and on-call burden.

**Best when:** only after evidence shows B cannot coordinate resources effectively and there is a formally approved owner/authority redesign. Not justified now.

## Comparative score (qualitative; not benchmark data)

| Dimension | A | B | C |
|---|---|---|---|
| Complexity | Low now / medium later | Medium | Very high |
| Correctness | High continuity | High with hard owner gates | Unproven, high blast radius |
| Latency | Best baseline | Small overhead | Uncertain |
| Throughput under contention | Medium | Best expected | Potentially high, central bottleneck |
| Memory efficiency | Local optimization | Shared allocation | Theoretical maximum |
| Explainability | Fragmented | Strong trace | Potentially opaque |
| Concurrency fairness | Partial | Explicit | Centralized |
| Extensibility | Local | Strong | Coupled |
| Recovery | Existing | New control-plane recovery | Major new kernel recovery |
| Operational cost | Low | Medium | Very high |

## Recommendation

Advance **B as an isolated, non-authoritative candidate**. Do not implement C. Keep A as fallback if a real workload fails to demonstrate multi-task contention or measurable duplication. A bounded prototype must compare B against A with identical synthetic workload and report fairness/quality trade-offs, not just aggregate utilization.
