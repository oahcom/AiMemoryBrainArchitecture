# Migration Impact and Staged Adoption

## Recommendation

Do not migrate F/G into a unified kernel. Introduce only a thin shared allocation contract after the architecture research is reviewed. The first phase can be a library/module inside the existing modular-monolith design, not a new service.

## Stage 0 — no architecture change

- Preserve F Retrieval, Activation, Scheduling and Working Set.
- Preserve G Context Planner, Budget Manager, Versioning/Committer and Reconciler.
- Instrument decision IDs, estimated vs actual resource usage, queue wait, task-level allocations and sufficiency outcomes.
- Establish baseline workload and contention measurements.

Exit: demonstrate where resource accounting is duplicated and whether tasks actually starve or exceed shared budgets.

## Stage 1 — shared vocabulary and trace only

Add candidate common value objects: ResourceVector, ResourceRequest, ResourceReservation, ResourceDecision and ResourceUsage. No shared mutable state. F and G remain decision owners for their respective resources.

Exit: bilingual schema review; exact owner acceptance; property tests for identity, accounting and no cross-scope reuse.

## Stage 2 — advisory allocator prototype

Use weighted fair queueing/deficit round robin for CPU, RAM, candidate/fan-out and latency budgets. G still allocates token/byte Context budget. RM may propose per-task token reservation only; G validates and commits. Use in shadow mode against existing decisions.

Exit: measured improvement in starvation/fairness without regression in Recall, task coverage, p95 latency, Forget suppression or authorization.

## Stage 3 — bounded adoption

Adopt RM for admission and reservations only. F retains retrieval/activation/caches; G retains Context sufficiency and commit. Fail closed on stale or unavailable PermissionEpoch/ForgetFence. Static per-principal quotas remain fallback only if explicitly approved.

Exit: concurrency, cancellation, restore, lease expiry, policy change, Forget race and authority-outage conformance.

## Stage 4 — reconsider only with evidence

A broader Memory OS kernel is a separate ADR only if the shared allocator demonstrably cannot coordinate the required resources. It must show lower total complexity and no new critical single point of failure.

## Breaking-change risks

- Resource request schema could become a de facto cross-owner authority surface.
- Token cost estimates may differ from final H tokenizer/rendering; G must charge actual materialized Context cost.
- F/G independent retries can double-reserve unless idempotency and attempt identity are distinct.
- A centralized scheduler can become a bottleneck or outage amplifier.
- Cross-task fairness can conflict with urgent user tasks; service classes must be policy-defined and still bounded.
- New "residency" flags can be mistaken for lifecycle or permission. Avoid global persistent residency.
- Resource pressure must never silently drop required evidence, uncertainty, provenance or P0 context anchors.

## Rollback

Disable RM admission integration and return to F/G local schedulers using conservative per-principal static quotas. Do not roll back or rewrite ContextVersion, canonical Memory, Forget evidence, PermissionEpoch or existing F/G state machines.
