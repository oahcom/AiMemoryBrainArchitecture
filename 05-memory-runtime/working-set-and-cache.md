---
document_metadata:
  domain: memory-runtime
  role: design-specification
  steward: "user-authorized operator (delegated by account owner)"
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-140/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Source blob provenance and mirror pairing were checked; semantic parity was reviewed at heading and cross-reference level only."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Canonical
    canonical_scope: "Memory Runtime design specification: working-set-and-cache"
    canonical_scope_id: "memory-runtime/working-set-and-cache"
    canonical_scope_keywords:
      - "working-set"
      - "cache"
      - "invalidation"
      - "forget"
      - "isolation"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/05-memory-runtime/working-set-and-cache.md"
    zh-CN: "docs/zh-CN/05-memory-runtime/working-set-and-cache.md"
---
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
WorkingSet: runtime_session_id, session_generation, principal_ref, normalized_scope_digest, environment_scope_id, permission_epoch_ref + policy_domain/issuer, forget_fence_ref + forget_fence_generation, entries[], byte/entry budget, created_at, expires_at.

WorkingSetEntry: memory_id, memory_version_id, scope_digest, permission_epoch_ref, forget_fence_ref/generation, source_index_partition/generation where applicable, lifecycle snapshot, provenance refs, optional bounded rendering, inserted_at, last_accessed_at, expiry, F-local invalidation generation. Store references preferentially; materialized content is optional and separately access-controlled.

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
- I PermissionEpoch reference plus its policy-domain/issuer binding (opaque; validated only by I);
- D ForgetFence reference/generation and applicable target/lineage coverage (opaque; validated only by D);
- exact Memory/Entity version or index generation/watermark;
- normalized query fingerprint and filters;
- retrieval/activation policy configuration version;
- temporal bucket where time changes validity;
- evidence access class where evidence is cached.

If any required dimension is unavailable, do not cache the protected result. A cache key is not itself authorization; hits always pass current authorization and canonical/Forget validation.

## 8. Invalidation and Forget — INT-P0-03
Forget is a logical access barrier before asynchronous physical cleanup. When I/D publishes a durable Forget fence:
1. Observe the durable D ForgetFence reference/generation and mark every covered target/descendant unreadable. Only D advances ForgetFenceGeneration; F advances only its own local invalidation generation.
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


## 19. Routing / Scheduling
Working Set admission occurs only after request authorization and session binding. Retrieval may populate it only with candidates that passed Scope-before-Candidate and canonical/Forget revalidation. Scheduler enforces per-session/global entry and byte budgets before insertion, prioritizes interactive work over background warming, and cancels fills on session close, revocation or Forget. Cache fills are coalesced only when the complete authorization/freshness key matches; otherwise requests execute in isolated namespaces.


## Phase 3.5 — Forget Fence and Permission Invalidation Addendum (normative supplement)

The detailed contract and conformance cases are in [Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract](../docs/governance/documentation-gaps.md) (unsubmitted and not restored; see [documentation gaps](../docs/governance/documentation-gaps.md)). This addendum supersedes earlier provisional wording where inconsistent.

### Required cache/Working Set binding

Every protected cache key and Working Set namespace binds, as applicable: authenticated Principal/issuer/security domain; canonical ScopeRef set; Agent/instance/task/session/environment; I PermissionEpoch; D ForgetFence reference/generation; exact Memory/Entity version or index+partition+generation+watermark+coverage/schema; query/filter fingerprint; retrieval configuration; temporal validity and Evidence access class. Missing required dimensions means no protected cache admission. The key is not authorization: every hit revalidates current I permission and D fence/lifecycle.

### Invalidation postconditions

- **Forget:** immediately deny target and descendant/lineage reads; evict or quarantine hot-memory/entity/query/index-derived entries; remove or render inaccessible matching Working Set refs/snippets; cancel in-flight retrieval/fills; recheck at fill publication and final return.
- **Permission revocation:** immediately deny old-epoch access; invalidate affected Principal/Scope/resource namespaces and Working Sets even if physical eviction is delayed.
- **Duplicates:** same event/operation ID + same target digest is idempotent; changed digest is a conflict. No duplicate can regress a tombstone or restore an entry.
- **Lost notifications:** durable D/I state is authoritative. Every read revalidates; reconnect/anti-entropy reconciles contiguous checkpoints. A gap or unavailable authority quarantines affected namespaces until resync.
- **Reconnect:** authenticate, obtain current I PermissionEpoch and D fence, reconcile G Context target, then restore only eligible entries. Never restore old Working Set first and clean later.

### Cache Miss vs Stale Entry

A **Cache Miss** means no entry exists for the complete key and permits a normal authorized source read. A **Stale Entry** exists but any authorization, fence, scope, version, watermark/schema, session or environment dimension is outdated or unverifiable; it must be dropped/quarantined and never returned. If D/I authority is unavailable, do not downgrade a stale hit to a miss and serve it.

TTL is an optimization only; it is not a Forget or revocation mechanism. F-local invalidation evidence does not establish global completion or physical erasure.


## Phase 3.5 reprocessing — typed invalidation and target evidence

This section supersedes any generic use of “Forget epoch” above: F does not mint or advance D's fence.

1. Every protected cache key and Working Set namespace binds the authenticated Principal/security domain, canonical owner/applicability ScopeRefs, required Agent/instance/task/session/environment dimensions, I PermissionEpoch domain/issuer, D ForgetFence reference/generation, exact MemoryVersion/EntityVersion or index+partition+generation+coverage/schema/watermark, and query/config/temporal/evidence dimensions as applicable.
2. The key is never authorization. A hit must validate current I permission and D target/lineage fence before payload access, then canonical version/lifecycle and independent Evidence/Provenance authorization.
3. On Forget, F increments only its own invalidation generation, blocks the target/descendants, evicts or quarantines matching hot/entity/query/index-derived entries, clears or makes unreachable matching Working Set references/snippets, cancels matching in-flight work/fills, and prevents late fill publication. On revocation, the same logical deny applies to the affected Principal/Scope/resource namespace.
4. A notification is an optimization. Durable D fence/target state and I PermissionEpoch/revocation state are authoritative. Lost/gapped checkpoints quarantine affected namespaces until snapshot-plus-contiguous-replay reconciliation; never reset a checkpoint to “latest” without a verified snapshot base.
5. Reconnect order is authenticate → obtain current I PermissionEpoch → obtain current D ForgetFence → reconcile G Context target/delivery state → invalidate old Working Set → restore only independently reauthorized, non-fenced exact versions. Restore-first/clean-later is forbidden.
6. I owns TargetId and the sealed closed-world inventory. F reports per-index/per-partition watermark, coverage/schema, suppression/invalidation checkpoint, affected scope/lineage digest and local residual status; F does not mint TargetId or mark I's global target/component Confirmed.
7. A Cache Miss means no entry for the complete key and permits a normal authorized read. A Stale Entry exists but one or more bound dimensions are obsolete, mismatched, incomplete or unverifiable; it is dropped/quarantined and never served. If D/I authority is unavailable, do not downgrade stale to miss and serve it.
8. Duplicate invalidation with the same owner namespace + operation/event ID + target digest is idempotent. Same idempotency identity with a changed digest is a conflict; neither duplicate nor retry may restore content or regress a tombstone.
