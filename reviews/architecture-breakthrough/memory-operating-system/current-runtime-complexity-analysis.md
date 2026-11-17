# Current Memory Runtime Complexity Analysis

- Status: RESEARCH / CANDIDATE ONLY — not an Owner decision or implementation authorization.
- Baseline: main `b3c666e67982cb3d3374e759cfb6552c7765aacb`; F `session-f-memory-runtime` HEAD `1908ce4d233b20f7cafd00cb679affd01bd15174`; G `session-g-memory-context` HEAD `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8`.
- Control: Issue #43. F/G source artifacts were read from their owner branches; this report does not replace them.

## Executive finding

The current design has meaningful separation, not merely accidental duplication. F owns Recall execution, retrieval, ranking/fusion, activation recommendations, request scheduling and disposable Working Sets/caches. G owns desired Context membership, ordering, multi-dimensional budget/sufficiency, immutable Context versions and delivery intent. D/E/I/H/C retain canonical, publication, authorization, adapter and inference-boundary authority.

The duplication risk is concentrated in *resource decisions and their signals*: F candidate/latency/CPU/RAM budgets, F Working Set/cache capacity and eviction, F activation cost/urgency, G token/byte/count/latency budget, G tier reserves, G compaction and deferred entries, plus C/H boundary telemetry. They use overlapping concepts (cost, urgency, freshness, deadline, capacity) but govern different resources and different state owners.

## Observed source facts

1. F RetrievalResult is a discovery/evidence result; ActivationRecommendation is a proposal to include/defer/exclude. Neither creates G Context membership.
2. F scheduler already defines bounded admission, per-principal/per-scope concurrency, interactive/background pools, quotas, cancellation, backpressure and fairness as candidate mechanisms.
3. F Working Set is a disposable, session-isolated view/cache, not Canonical Memory, G Context or Agent planning state. Cache hit must revalidate current authorization and Forget.
4. G Budget Manager already uses a vector: tokens, bytes, entry/ref counts, relation/provenance bounds, latency, refresh, CPU and compaction cost. Sufficiency is task-specific and multidimensional, not Top-K.
5. G consumes F candidates as immutable proposals, then re-resolves canonical version/lifecycle and I/D authorization/fence. G owns Context membership/version.
6. G's Context budget and F's runtime memory budget are not the same resource: one limits a managed inference region; the other bounds transient execution and cache memory.
7. Existing F anti-resurrection tests are logical reference-model tests, not physical adapter, production topology or performance proof. Existing F technology review explicitly leaves index backend and numeric limits to benchmark.

## Complexity map

| Concern | F authority | G authority | Duplication risk | Proposed treatment |
|---|---|---|---|---|
| Candidate discovery | Retrieval/routing/fusion | Consumes candidates | Low | Keep F |
| Candidate suitability | Activation recommendation | Accept/reject/transform membership | Medium | F explains candidate utility; G makes Context decision |
| Token/byte budget | Cost estimate only | Managed-region hard budget | Medium | Shared typed cost model; G remains final allocator |
| CPU/RAM/fan-out/deadline | Runtime scheduler | Planning/commit/delivery latency constraints | Medium | Shared resource envelope; separate stage budgets |
| Working Set/cache | F owns | G owns Context snapshots/cache effects | Medium | Keep F transient view; no duplicate Context store |
| Eviction | F disposable cache/WS | G defers/removes entries/compacts Context | High semantic confusion | Name separately: cache reclaim vs Context membership change |
| Freshness | F index/channel watermarks | G sufficiency/source freshness | Medium | Pass typed vectors; never collapse watermarks |
| Forget/Permission | Enforce current D/I decision | Enforce in Context and delivery | High risk if centralized incorrectly | Hard gates remain D/I-owned; RM cannot override |
| Residency | F local cache state | G Context lifecycle and H applied state | High if globalized | No global durable residency state |

## Main design smells / open questions

- A candidate may be ranked by F, rejected by G, re-retrieved by F, and then re-ranked without a shared reason/decision record. Preserve separate authorities but add a common decision trace ID and explicit feedback.
- A token estimate can be charged at F and again at G. Define cost ownership and accounting: F estimate is advisory; G charges committed Context tokens against the target tokenizer/rendering profile.
- "Eviction" currently risks conflating cache deletion, Working Set removal, Context deferral, Context entry removal and canonical Forget. These must never share a command or terminal state.
- Per-request fairness exists in F scheduling but G context capacity may be competed for by concurrent tasks. A task-level reservation ledger can bridge the allocation gap without taking over either module's domain state.
- The source documents do not prove measured duplication, latency or utilization in a representative workload. Do not claim current architecture is inefficient without a benchmark.

## Baseline verdict

Current F/G split is conceptually sound. The best target is not C-style consolidation of all responsibilities; it is a thin, shared resource-allocation contract and scheduler policy that coordinates resource requests, reservations and fairness while leaving retrieval, activation semantics, Context state and safety authority with their owners.

## Exact source pins

- F Retrieval: `05-memory-runtime/retrieval-engine.md`, Blob `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af`.
- F Activation: `05-memory-runtime/activation-policy-engine.md`, Blob `b7f5d85468f5262e472769a1991b812ac4a64f5b`.
- F Scheduling: `05-memory-runtime/runtime-scheduling.md`, Blob `ca35d8cddd012c1ff067328ee22177f57c40ae36`.
- F Working Set: `05-memory-runtime/working-set-and-cache.md`, Blob `a934491950c876701e8ac592a0e6aaea983b44e3`.
- G Context Architecture: `06-memory-context/context-architecture.md`, Blob `56fcc0ea112d423ef69a3f00e9d626bf4230ca0e`.
- G Budget: `06-memory-context/context-budget-and-sufficiency.md`, Blob `a2f96a88f3123862ea263da11366dda4207d5b0a`.
- G Manager: `06-memory-context/context-manager.md`, Blob `ecc0549137a1738c197d02d12d94a1eb971ed6b5`.
- B Domain Model: `02-domain-model/domain-model-overview.md`, Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346`.
- F logical test: `tests/anti_resurrection/test_f_runtime_model.py`, Blob `c2575327a75577923440ef770d42122218a1e091`.
