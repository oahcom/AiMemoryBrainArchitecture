# Runtime Working Set and Cache

**Owner:** Session F — MR-03  
**Status:** DECIDED authority/isolation semantics; CANDIDATE cache topology; TO_VALIDATE sizing/TTL.

## 1. Purpose
Define bounded, disposable runtime-local state that accelerates Recall without becoming Canonical Memory or bypassing Scope, Permission, Forget or version checks.

## 2. Scope
Owns Runtime Working Set, session isolation, hot-memory/entity/query/index caches, key construction, invalidation, TTL, capacity eviction and cache observability. Does not own canonical persistence, index publication, Context Version, Agent Planning State, global authorization policy or physical deletion.

## 3. Responsibilities / Non-Responsibilities
Working Set is a bounded set of active references and optionally authorized materialized snippets used during a Runtime Session. It is not the full memory database, durable user profile, Context, or Agent plan. Cache is an optimization only: cache miss must preserve correctness; cache hit must not weaken correctness.

## 4. Inputs / Outputs
Inputs: RuntimeSession trusted identity/scopes, exact Memory Version refs, authorized candidate/evidence metadata, permission/Forget epochs, index watermarks, canonical change events and invalidation events. Outputs: authorized cache hit or miss; Working Set snapshot for the same session; invalidation/eviction events; metrics. No cache API returns unvalidated protected content.

## 5. Data Model
WorkingSet: runtime_session_id, session_generation, principal_ref, normalized_scope_digest, environment_scope_id, permission_epoch, forget_epoch, entries[], byte/entry budget, created_at, expires_at.

WorkingSetEntry: memory_id, memory_version_id, scope_digest, source_generation, lifecycle snapshot, provenance refs, optional bounded rendering, inserted_at, last_accessed_at, expiry, invalidation generation. Store references preferentially; materialized content is optional and separately access-controlled.

Cache families:
- Hot Memory Cache: exact Memory Version metadata/rendering; key includes memory_id + version_id + scope/auth epochs.
- Entity Cache: canonical entity identity/profile version and authorized aliases; entity scope and policy epochs included.
- Query Cache: query fingerprint + principal/scope/environment + policy/Forget epoch + retrieval config + index watermarks + consistency fence.
- Index Cache: backend-local posting/vector/graph/temporal pages; must be physically partitioned or enforce safe scoped access semantics.

## 6. Session Isolation
Each Runtime Session has its own Working Set namespace. No implicit sharing across Agent, Agent Instance, Task, Session or Environment. Cross-session reuse is permitted only in lower-level caches when the key fully partitions principal, scopes, environment, permission/Forget epochs and exact versions, and every read is reauthorized. Session close destroys the Working Set namespace or makes it unreachable pending bounded cleanup.

## 7. Cache Key
A cache key must bind every dimension that can change visibility or semantics:
- authenticated principal/tenant;
- ownership and applicability Scope set (canonical sorted IDs, not display names);
- Agent/instance/session/task/environment dimensions as required;
- permission policy version and revocation epoch;
- Forget/tombstone epoch;
- exact Memory/Entity version or index generation/watermark;
- normalized query fingerprint and filters;
- retrieval/activation policy configuration version;
- temporal bucket where time changes validity;
- evidence access class where evidence is cached.

If any required dimension is unavailable, do not cache the protected result. A cache key is not itself authorization; hits always pass current authorization and canonical/Forget validation.

## 8. Invalidation and Forget — INT-P0-03
Forget is a logical access barrier before asynchronous physical cleanup. When I/D publishes a durable Forget fence:
1. Advance the relevant Forget epoch/tombstone visibility.
2. Block candidate generation and cache return for the target immediately, including in-flight results.
3. Remove or quarantine target references/materialized data from all affected Working Sets.
4. Cancel or mark stale in-flight retrieval/activation tasks; before response/G handoff recheck fence.
5. Invalidate hot-memory, entity, query and index-derived cache entries; if physical purge is delayed, deny reads by fence.
6. Persist invalidation progress and report per-target status; do not claim global physical erasure from Runtime.
7. Rebuild/index replay must consult canonical Forget state and tombstones so forgotten content cannot resurrect.

Runtime does not own Forget completion. It reports suppression, cache/Working Set invalidation and residual status to I. Tombstone retention is governed by I/D and must not preserve forgotten content beyond policy.

## 9. Permission Revocation
On revocation epoch change, affected entries become unreadable immediately, even if physical eviction is asynchronous. Revalidate before returning cache hit, before Working Set reuse, before evidence dereference and before G handoff. If current policy epoch cannot be obtained, fail closed. Revocation may be narrower than a whole session; invalidation identifies affected principal/scope/resource dimensions.

## 10. Memory Version Change / Lifecycle
A new canonical version invalidates exact-version hot entries and query results dependent on the old version. Old immutable versions may remain accessible only if canonical policy permits historical reads. Lifecycle transition (superseded, retracted, archived, forgotten) invalidates derived recommendations; Forget is always suppressive. Index generation changes invalidate or age out index-dependent query entries.

## 11. TTL and Capacity Eviction
TTL is an optimization bound, not a substitute for revocation or Forget. Use separate candidate TTLs by cache family and sensitivity; all are CANDIDATE/TO_VALIDATE. Capacity eviction may use LRU/LFU/segmented policy, but must never evict authoritative data because none is owned here. On eviction, correctness falls back to authorized source reads. Working Set has strict per-session and global byte/entry limits with admission control.

## 12. Failure Handling
Invalidation event loss is repaired through epoch/fence comparison on every read. Cache service failure degrades to uncached retrieval. Stale cache entry is discarded, not returned with warning if it could disclose forbidden data. Session identity mismatch or scope ambiguity clears access. Partial invalidation status is observable and fail-closed for affected targets.

## 13. Performance Budget
Bound memory by per-session bytes/entries, global cache bytes, entry size, query cardinality, and in-flight fills. Avoid caching large Evidence payloads. CPU spent hashing keys/validating epochs is measured; RAM is budgeted; disk cache is optional and encrypted/partitioned under I policy; GPU memory is not used for Runtime cache. Numeric limits/TTL are TO_VALIDATE.

## 14. Observability
Metrics: hit/miss/eviction by cache family, invalidation lag, stale-entry suppression, Working Set size/age, per-session quota pressure, invalidation failures, cache rebuild, and epoch mismatch. Never expose unauthorized object counts or content. Audit Forget/revocation invalidation state transitions with correlation IDs and policy-safe resource refs.

## 15. Interfaces
D supplies canonical version/lifecycle and Forget state; E supplies index generation and publication events; I supplies permission/revocation and Forget fences; G may provide read-only Context version to avoid duplicate proposals but not its authoritative entries; Runtime Scheduler controls session teardown/cancellation. Event payloads require resource/scope refs, epochs, generation, idempotency, schema version and retry semantics.

## 16. Test Scenarios
Cross-session and cross-environment key collision; same query under different principal/policy epoch; permission revoked after cache fill; Forget while query is in flight; cache service down; invalidation event lost but epoch advanced; Memory version changed; stale index cache after rebuild; session close; capacity eviction; no forgotten memory reappears after index rebuild/replay.

## 17. Dependencies
D canonical version/lifecycle/Forget identifiers; E index generation and rebuild feed; G Context read-only hints; H authenticated session identity; I policy epoch/revocation/Forget contract and storage protection.

## 18. Open Questions
OPEN: I's revocation epoch scope and propagation SLA; D/E Forget tombstone format and retention; G's minimal context summary; H session identity semantics. CANDIDATE: in-memory per-session Working Set + shared but strictly partitioned read-through caches. TO_VALIDATE: TTL, eviction algorithm, memory limits and hit-rate benefit on target hardware.
