# Memory Operating System — Architecture Research

**Disposition: B is the recommended candidate; no formal architecture change is approved.**

## Thesis

The project does not need a full Memory OS kernel. It may benefit from a shared resource-control plane that allocates bounded compute, cache, retrieval and context capacity across concurrent tasks. This control plane must not become the authority for memory identity, access, Forget, Context membership or model application.

## Findings

1. Retrieval and Activation remain distinct. Retrieval answers "what eligible candidates were found, with what evidence and completeness?" Activation answers "which candidates should be recommended now, deferred, excluded or explicitly recalled?" G owns final Context membership.
2. Context Budget and cache Eviction share resource accounting concepts but not semantics. G's budget is a task-specific semantic coverage constraint; F eviction reclaims disposable cache/Working Set projections. A common ResourceVector is useful; a shared eviction state machine is not.
3. Working Memory should remain a Runtime View, not a new canonical store. F Working Set is session-scoped/disposable; G Context is a separately versioned managed inference region; Agent planning state is separate again.
4. Residency is useful only as ephemeral projection metadata. Do not introduce a durable global residency state machine. Canonical lifecycle, index generation, cache presence, Working Set membership, Context membership and Adapter application are separate dimensions.
5. Concurrent tasks need per-principal/task reservations, weighted fair scheduling, minimum floors, bounded borrowing, aging, deadlines and cancellation. No task may consume all shared capacity.
6. One task cannot starve others if the allocator reserves a guaranteed floor and enforces per-task caps. Borrowed capacity must be reclaimable at safe stage boundaries.
7. Forget, Permission, Security, Scope and Authority are pre-ranking hard gates. Unknown/stale authority state blocks protected use. Resource priority is never permission.
8. Importance changes should update soft utility and future reservations with hysteresis; never mutate canonical lifecycle or retroactively change already committed immutable Context versions.
9. Different resource classes need distinct policies: interactive Recall, explicit Recall, context planning, background refresh, cache reclaim, compaction and maintenance.
10. Module count falls only if the shared allocator replaces duplicated reservation/fairness logic. A full kernel would likely increase trusted complexity and cross-module state coupling.

## Three alternatives

- A: retain F/G separate modules. Lowest migration risk; local budgets can drift.
- B: shared Memory Resource Manager, preserve F/G domain owners. Best balance under contention.
- C: full Memory OS kernel. Highest complexity, broadest blast radius and new single point of failure.

## Candidate resource contract

MemoryResourceRequest declares typed identity/scope, task class, deadline, freshness, budget vector, min reservation, max cap, cancellation and owner-validated permission/Forget references. ResourceDecision grants/reduces/defers/rejects with reservation, resource vector and explainable fairness trace. It is not an authorization token.

## Safety and failure model

The allocator is not authoritative. F/G revalidate D/I at each protected read, Context commit and delivery boundary. If RM is unavailable, new protected work is deferred/rejected unless an explicitly approved bounded static policy applies. No stale grant may outlive permission or Forget changes. Canonical Memory and Context state remain recoverable independently.

## Quantitative prototype

A fixed-seed synthetic experiment with 30 tasks, 720 candidates and 9,000-token shared budget found:
- Direct Top-K: recall .5333, precision .4741, Jain fairness .8325, one starved task.
- Rerank+Budget: recall .5417, precision .2863, Jain fairness .8141, no starvation.
- Unified RM: recall .5083, precision .2699, Jain fairness .8554, no starvation.

RM improved fairness but reduced recall/precision and increased local selection latency (0.324 ms median vs 0.099 ms Top-K). This is a synthetic algorithm experiment only, not real user or production evidence.

## Final recommendation

Keep A as the current architecture. Advance B only as a shadow-mode candidate after baseline instrumentation and owner review. Do not implement C. Preserve all F/G/D/E/I/H/C authority boundaries and all existing Forget/Permission constraints.
