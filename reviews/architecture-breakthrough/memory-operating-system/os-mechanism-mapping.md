# OS Mechanism Mapping — Applicability and Failure Boundaries

Status: candidate analogy only. The Brain manages knowledge projections and task context, not physical pages or process address spaces.

| OS mechanism | Useful transfer | Required Brain adaptation | Failure boundary |
|---|---|---|---|
| Virtual memory / page tables | Separate canonical backing assets from task-local materializations; references can be resolved on demand | Canonical Memory is backing authority; F Working Set/G Context are distinct projections | A Memory is semantic knowledge, not an addressable fixed-size page; page fault cannot define relevance or truth |
| Page cache | Cache disposable reads, reclaim under pressure, re-fetch from authoritative source | Cache exact immutable version refs and authorization/fence epochs; misses preserve correctness | Linux page cache does not understand Permission, Forget, provenance or epistemic status |
| Page fault | Explicitly fetch a missing eligible asset on demand | Typed Recall miss / deferred expansion with deadline and completeness result | Do not turn every omitted memory into synchronous expensive retrieval; latency and privacy risks |
| Working set | Bound active task-local hot set | Per Runtime Session/task bounded refs/renderings; G Context remains separate managed inference region | OS working set is locality approximation; semantic importance and cross-task reuse differ |
| Memory pressure / reclaim | Trigger safe degradation and reclaim disposable state | Drop/rebuild F caches first; reduce optional graph/evidence work; defer background refresh; never silently remove required G coverage | Memory-pressure response must not discard canonical state, Forget evidence or protected context requirements |
| LRU/LFU/ARC | Candidate cache replacement heuristics | Apply only to disposable caches; consider frequency decay, recency and scan resistance | Not valid as Context membership policy; rare memories can be crucial, and frequency may encode popularity rather than task value |
| CPU scheduling / WFQ | Fair share, reservations, aging, bounded queues, deadline handling | Per-principal/task resource shares for retrieval and Context planning; interactive/background pools | Importance/urgency cannot bypass permission, Forget, quotas or other tasks' guaranteed floors |
| cgroups | Hard ceilings and pressure isolation | Per-principal/task CPU, memory, fan-out, token and latency quotas | cgroups enforce OS resource usage, not semantic token sufficiency or context coverage |
| NUMA | Keep hot data near consumers when locality has measured value | Optional per-process/index locality tuning only after profiling | Most local-first deployments may not be NUMA-bound; do not create per-agent replicas by analogy |
| Cache hierarchy | Separate durable source, indexes, runtime cache, task context, adapter materialization | Explicit tiers with owner and rebuild/invalidity rules | These are not a single coherent memory hierarchy: G Context is a versioned semantic artifact, not an L2 cache |
| Kubernetes requests/limits | Admission from declared demand; reserve minimum capacity; constrain overuse | Request/reservation/limit/deadline contract and noisy-neighbor protection | K8s scheduler is node placement, not per-memory selection; avoid importing cluster complexity |

## Recommended mapping

1. **Residency is a view, not a new canonical lifecycle.** Represent only local projection states (not resident, cached, in Working Set, staged in Context, applied by Adapter) with owner-specific epochs and evidence. Never store a global "memory is resident" truth.
2. **Page fault becomes a bounded Recall operation.** It returns candidate refs plus freshness/completeness and may be deferred or partial.
3. **Reclaim is class-specific.** F may evict disposable cache/Working Set materialization. G may defer or remove a Context Entry through its own versioned ChangeSet. Neither action deletes canonical Memory.
4. **Memory pressure has a degradation ladder.** Stop speculative refresh → cancel low-priority work → reclaim F cache → reduce optional expansion → ask G to compact or defer optional entries → return insufficient if mandatory coverage still exceeds budget.
5. **Use weighted fair scheduling at the request/task level.** Reserve a minimum for each active principal/task; borrow unused capacity with reclaim at safe boundaries; age queued requests; isolate background work.
6. **Hard gates are outside the scheduler.** Authentication, Scope, I PermissionEpoch, D ForgetFence, canonical lifecycle/version, provenance access and classification are preconditions, not weights.

## Important anti-mappings

- Do not map Forget to page eviction. Forget is an authoritative lifecycle/revocation operation with lineage, inventory and evidence semantics.
- Do not map Archive/Retention to swap. Durable retention and legal/operational deletion are not cache tiers.
- Do not map Context priority P0–P3 to OS process priority. They are inclusion priorities, not privilege.
- Do not map "recently accessed" to "important". A rarely used emergency instruction or a low-frequency preference may matter more than popular trivia.
- Do not use global LRU to decide what the user should remember.
- Do not infer permission from cache residency or index partition membership.

## References

- Linux MM concepts: https://docs.kernel.org/admin-guide/mm/concepts.html
- Linux cgroup v2: https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html
- Linux VM sysctl / NUMA reclaim: https://docs.kernel.org/admin-guide/sysctl/vm.html
- Redis eviction policies: https://redis.io/docs/latest/develop/reference/eviction/
- Kubernetes resource requests/limits: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
