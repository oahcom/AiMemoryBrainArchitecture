# Phase 3.5 — Runtime Forget Suppression and Typed Cursor Consumer Contract

- **Owner:** Session F — Memory Runtime Principal Architect
- **Status:** DECIDED runtime safety semantics; cross-module API realization OPEN; backend/cancellation behavior TO_VALIDATE
- **Branch:** `session-f-memory-runtime`
- **Scope:** Retrieval, candidate generation, fusion, freshness, Working Set/cache, index rebuild/backfill/replay, ActivationRecommendation
- **Authority rule:** F consumes D/E/G/H/I/B/C contracts; it does not redefine their authorities or wire formats.
- **Non-claims:** This is a static architecture contract. It is not evidence of implementation, concurrency/fault-injection tests, performance benchmarks or production readiness.

## 1. Authority and safety invariants

| Concern | Authority | F obligation |
|---|---|---|
| Canonical Memory identity/version/lifecycle and canonical commit order | D | Read exact typed references; never infer canonical truth from an index |
| ForgetOperation, ForgetFenceGeneration, producer registry/barrier and canonical suppression | D | Suppress all affected candidate, cache, Working Set and index-derived visibility; register F producer work before derivative-capable work |
| Compiler producer lifecycle and derived registration/publication | E, using D gate | Consume only committed/registered source changes; do not treat E local state or queue state as canonical publication evidence |
| Principal, Scope authorization, PermissionEpoch, revocation and global Forget completion | I | Reauthorize at each disclosure boundary; report only F-local evidence; never claim global completion |
| Context membership/version/reconciliation | G | Emit read-only candidates/recommendations; never mutate ContextVersion or infer Applied |
| BMCP envelope, Adapter clear ACK and reconnect | H | Treat tokens as opaque typed inputs; do not define wire fields or Adapter completion |
| ActorRef/ScopeRef meaning | B | Treat as typed references, not credentials or grants; exact mapping remains subject to B/I approval |
| Agent untrusted-data and final inference boundary | C | Keep Memory data-only; F cannot claim final-request inclusion or Applied |

Hard invariants:

1. **Canonical state wins.** An index, cache, Working Set or recommendation can never override D's current canonical lifecycle/version/Forget state.
2. **Scope-before-Candidate.** No unauthorized or cross-Scope object may enter a Runtime candidate buffer, fusion, reranker, counts, traces that expose existence, cache response or Working Set.
3. **Latest-state-before-disclosure.** Every path that returns protected data revalidates current I authorization/PermissionEpoch and D Forget coverage; stale local epochs do not authorize.
4. **No resurrection.** Rebuild, backfill, replay, cache warming, retry, reconnect or late publication cannot make a forgotten source or descendant visible again.
5. **Fail closed on unknown authority state.** Missing/stale/unavailable fence or permission state blocks affected content; it is not converted to a permissive default.
6. **F-local evidence only.** F can report suppression, invalidation, rebuild and per-partition freshness evidence. I decides global Forget completion and physical-erasure policy.
7. **Recommendation is not application.** ActivationRecommendation is advisory; G alone commits ContextVersion and H/C evidence is required for any Applied statement.

## 2. Cursor Consumer Matrix

All tokens are typed, owner-issued values. F stores and forwards each value unchanged and uses only the owning module's comparison/validation operation. F MUST NOT cast, numerically compare, increment, synthesize, or substitute one token for another.

| Token | Owner / scope | F consumption | May compare/order? | Never proves |
|---|---|---|---|---|
| `CanonicalCommitCursor` | D; one globally ordered sequence per Canonical Memory authority | Pin canonical read snapshots; resume canonical event consumption; record rebuild snapshot/replay positions | Only through D-defined same-authority ordering/continuity semantics | Index application, Forget completion, Context state, physical deletion |
| `AggregateRevision` | D; one aggregate | Pin exact aggregate revision when an object/aggregate is read | Only within the same aggregate identity under D semantics | Cross-aggregate order or global commit order |
| `LifecycleEventCursor` | D; per Memory | Detect/consume lifecycle changes for the exact Memory; maintain per-Memory lifecycle projection | Only within that Memory's lifecycle stream; preserve enclosing CanonicalCommitCursor separately | Aggregate revision, index partition completeness, Forget completion |
| `IndexWatermark` | F; one index/channel partition, with `applied_through: CanonicalCommitCursor` plus coverage/schema versions | Report contiguous canonical prefix accounted for by that exact partition; determine freshness/lag and replay resume point | F may compare same index+partition watermark's applied-through CanonicalCommitCursor using D cursor semantics; never compare watermarks across unrelated partitions as if one scalar | Target absence, cache purge, Forget suppression, Context reconciliation, global completion |
| `ProducerRegistrationSequence` / `ProducerRegistrationHighWater` *(admission evidence, not a cursor)* | D; producer-registration ledger and per-Forget barrier in one D authority | F binds derivative-capable rebuild/backfill/replay work to the durable admission position and determines whether pre-fence work is included in the captured barrier | Only D-defined ordering/membership within the same producer-registration ledger; never compare with CanonicalCommitCursor, IndexWatermark, ForgetFenceGeneration or PermissionEpoch | Canonical commit order, derivative visibility/publication, index freshness, cache purge or global Forget completion |
| `RegistrationReceipt` *(typed admission receipt, not a cursor)* | D; exact `ProducerWorkItemId` + canonical request digest | F must durably resolve it before enqueue, lease, canonical source dereference or execution; lost response is reconciled by stable work ID/digest | Exact receipt identity/idempotency through D's operation; no local inference from queue state | Work completion, publication success, barrier closure or Forget completion |
| `ForgetFenceGeneration` / `ForgetFenceCursor` | D; Forget authority and exact target-set/lineage | Query whether exact target or any source ancestor is covered; bind cache/Working Set entries and invalidation records to observed fence | Only D's fence-coverage/currentness operation; opaque outside D | Commit ordering, index freshness, permission grant, physical erasure |
| `PermissionEpoch` | I; named policy domain/issuer | Bind auth decisions and cache namespaces; revalidate resource/scope access at each boundary | Only I's same-domain epoch validation/continuity semantics | Forget fence ordering, canonical commit order, data deletion |
| `ContextVersion` | G; per Context immutable target | Carry exact read-only target hint/activation correlation if supplied | Only G's version/base/target semantics | Canonical Memory revision, Adapter application, Forget completion |
| Delivery ID / Capability Epoch / Inference Request ID | H/C; delivery, Adapter capability and final request domains | Correlate only where needed for evidence and trace; never use as a Memory cursor | Owner-specific only | Canonical order, Memory freshness, Forget completion |

### 2.1 IndexWatermark rules

- An IndexWatermark is scoped to a named index/channel partition and reports the highest **contiguous** CanonicalCommitCursor prefix for which all relevant changes have been accounted for, including explicit no-op coverage.
- A delayed, failed, missing or schema-incompatible relevant commit stops that partition's watermark before the gap. Out-of-order events may be staged but do not advance the contiguous watermark.
- A multi-partition index is represented by a vector/map of per-partition watermarks, not a fabricated global scalar. A lagging partition cannot be hidden by another partition's progress.
- Watermark coverage/schema version changes are explicit; a schema-incompatible segment is not silently treated as current.
- Watermark >= a required canonical cursor can establish projection freshness for that partition only. It does not bypass canonical validation or the current ForgetFence check.
- Watermark < required cursor means lag. F must use bounded canonical read-through/delta if a D-supported API exists, wait within deadline, or return an explicitly partial/degraded result. If the request requires strict consistency and safe read-through is unavailable, return unavailable/fail closed.
- Never infer Forget completion from a high watermark, a zero-hit query, a successful rebuild, or absence of a target from one partition.

## 3. Retrieval Suppression Matrix

The current Scope, Permission and Forget checks apply throughout the pipeline. A check at request admission is not a reusable authorization for a later disclosure.

| Stage | Required checks and ordering | Fence/revocation race behavior | Observable evidence |
|---|---|---|---|
| Candidate Generation | Authenticate/bind Principal; resolve trusted ScopeRefs and purpose with I; obtain current PermissionEpoch and D fence context; bind Scope predicate inside each candidate-producing backend before emission; register derivative-capable/background F work with D before admission | If current permission/fence cannot be established, do not generate affected candidates. Cancel/deny on a newer epoch/fence before candidate leaves adapter | Request/correlation ID, auth decision ref, scope digest, observed PermissionEpoch/fence ref, backend filter mode, denied-before-emission count only where non-disclosing |
| Index Lookup | Query only a scope-filtered partition/namespace; verify per-partition IndexWatermark and schema/coverage; each hit is an exact Memory/Version ref, not trusted content; no global top-K then application post-filter | Stale or cross-Scope hits are discarded before entering Runtime buffer. If partition watermark is behind, canonical read-through or partial/unavailable; stale fence means no affected hit | Index/partition ID, watermark and required cursor, coverage/schema version, scoped query plan, stale-hit suppression reason |
| Canonical Revalidation | Resolve exact MemoryVersionRef and lineage; read current lifecycle and D fence coverage; independently authorize Memory, Entity, Relation, Evidence and Provenance targets with I | Any forgotten/retracted/ineligible ancestor, permission denial, unknown lineage or unavailable authority suppresses candidate; no “current generation” supplied by caller overrides lineage | Canonical read cursor, exact version refs, lifecycle cursor, fence decision ref, PermissionEpoch decision ref, lineage result |
| Fusion / Deduplication | Only canonical-revalidated authorized candidates enter fusion; dedupe exact (Memory ID, MemoryVersion ID) only; preserve distinct versions/conflicts/evidence roles | A candidate invalidated after channel return is removed before fusion/reranking; no counts/scores/feature leakage from denied candidates | Candidate admission/suppression counts scoped to authorized data, dedupe records, fusion input digest |
| Freshness | Evaluate each channel/partition watermark against required CanonicalCommitCursor; keep freshness separate from ForgetFence and PermissionEpoch; preserve gaps | Lag triggers bounded read-through/wait/partial; a fresh watermark never overrides a newly raised fence or revoked permission | Per-partition observed/required cursor, contiguous/gap status, freshness state, read-through result |
| Reranking | Reranker receives only authorized, canonical-valid candidates and permitted evidence summaries; Memory text is untrusted data, not instructions | Revalidate policy/fence if epoch/fence changed during rerank; drop invalidated candidate and recompute or return partial | Reranker input candidate IDs/digest, policy/fence checkpoint, suppressed-after-rerank count |
| Result Materialization | Resolve exact version and render only authorized fields; reauthorize Evidence/source dereferences independently; sanitize output as data; no unauthorized cache fill | If fence/revocation advances during materialization, cancel or discard affected payload; no stale snippet may be emitted | Materialized refs/digest, evidence authorization outcomes, cancellation reason, exact authority checkpoint |
| Final Return / G Handoff | Immediately before serialization/return/handoff, fetch/validate latest applicable D fence and I permission state (or a proven contiguous authenticated view); verify request not cancelled; return explicit freshness/completeness | If fence/permission advanced after earlier checks, remove all affected content, mark partial/blocked or fail closed. If ordering is unknown, do not return affected content. F never writes ContextVersion | Final fence/auth checkpoint, response digest, suppression count, completeness/freshness vector, handoff correlation |

### 3.1 In-flight request linearization

- Each request carries a cancellation token and the observed policy/fence checkpoints for each affected scope/resource.
- Fence/revocation notification advances the local invalidation generation and cancels affected channel work, cache fills, reranking and materialization. Cancellation is best effort for resource savings, not the safety proof.
- The safety boundary is the final return/handoff gate: revalidate current D fence and I permission after all work and immediately before disclosure. A cancellation that arrives late cannot authorize stale output.
- If the runtime cannot prove whether a request's final disclosure linearized before or after a fence/revocation, it suppresses the affected content and records an ambiguous outcome; it does not guess.
- A request may return unaffected candidates only if each is independently scoped, authorized and outside the fence target/lineage. Otherwise return blocked/unavailable.

## 4. Cache and Working Set Invalidation Contract

### 4.1 Key construction

A protected cache entry is addressable only under a key binding all applicable dimensions:

- authenticated Principal/issuer and tenant/security domain;
- canonical sorted ScopeRef set and exact resource/lineage scope where applicable;
- Agent/Agent Instance, Task, Session and Environment dimensions as required;
- I PermissionEpoch and policy decision/version;
- D ForgetFence reference/generation (opaque typed value; never numerically ordered by F);
- exact MemoryVersionRef / EntityVersionRef or exact index ID + partition + generation/watermark + coverage/schema version;
- normalized query/filter fingerprint and retrieval/activation configuration version;
- temporal validity bucket and Evidence access class where relevant.

Missing identity, Scope, PermissionEpoch, fence or required version/freshness input means **do not cache protected content**. A key is isolation metadata, never authorization. Every hit revalidates current I permission and D fence/lifecycle before payload access or disclosure.

### 4.2 Invalidation triggers and postconditions

| Trigger | Immediate logical action | Physical/cache action | Required evidence |
|---|---|---|---|
| D ForgetFence advances | Mark all covered target/descendant refs unreadable; block candidate and cache return | Evict or quarantine matching hot-memory/entity/query/index-derived entries; remove Working Set refs and materialized snippets or make them irreversibly inaccessible under F control | Operation/fence ref, target-set/lineage digest, affected cache namespaces, invalidation generation, completion/unknown status |
| I PermissionEpoch/revocation changes | Deny access under old decision immediately | Invalidate affected Principal/Scope/resource cache keys and Working Sets; clear or quarantine snippets | Old/new opaque epoch refs, policy-domain and affected target digest, invalidation outcome |
| Canonical version/lifecycle changes | Old version is not silently substituted; apply D lifecycle rules | Invalidate exact-version hot entries and dependent query/recommendation entries | CanonicalCommitCursor, AggregateRevision and/or LifecycleEventCursor kept distinct |
| Index generation/schema/partition changes | Treat entries bound to old generation as stale | Invalidate index-derived query/page caches; rebuild only through registered safe process | Index/partition, old/new generation, watermark and coverage version |
| Session close / environment closure | Namespace becomes unreachable immediately | Destroy or quarantine Working Set and pending fills; no reconnect restoration | Session generation, close reason, cleanup status |

Invalidation is idempotent by stable event/operation ID + target digest + owner namespace. A duplicate invalidation returns the original disposition and does not resurrect or broaden access. A changed digest under the same idempotency identity is a conflict and security/consistency event.

### 4.3 Cache Miss vs Stale Entry

- **Cache Miss:** no entry exists for the exact complete key. Perform a normal authorized source read; a miss is not an error and carries no stale-data implication.
- **Stale Entry:** an entry exists but any bound dimension is obsolete, incomplete, mismatched or cannot be verified (PermissionEpoch, ForgetFence, exact version, watermark/schema, scope, session, environment, expiry). It is never returned. Drop/quarantine it, record a stale-suppression event and re-read only through the normal authorized path.
- **Unavailable Authority:** if current permission/fence/lifecycle cannot be established, do not downgrade stale entry to a miss and serve it; fail closed for affected data.

### 4.4 In-flight fills, cancellation and Working Set clearing

- Cache fill is admitted only after authorization and producer registration where it is derivative-capable or creates a persistent/rebuildable artifact covered by D's producer registry.
- Fence/revocation advances a per-request/session cancellation and invalidation generation. All matching in-flight fills, prefetches, graph expansions and activation computations are cancelled or marked non-publishable.
- A fill completing after invalidation must recheck current fence and permission at its write/visibility boundary; if stale, discard/quarantine and never insert.
- Working Set entries are references first. On Forget/revocation, remove references and materialized snippets from every affected session namespace, mark the namespace generation invalid, and persist only the minimal non-reconstructive suppression marker needed to reject stale restoration.
- If byte purge cannot be proven, F reports local logical suppression/invalidation with residual cleanup status. F does not claim secure media erasure.
- Reconnect/session resume must authenticate and obtain current PermissionEpoch, D ForgetFence and G Context target before restoring any Working Set. Old snapshots are not restored first and “cleaned up later”.

### 4.5 Lost invalidation and recovery

- Event delivery is at-least-once and may be duplicated or lost. Durable D/I authority state is the source of truth, not the invalidation message.
- Every protected cache/Working Set read performs current authority revalidation; this repairs a lost notification before disclosure.
- F periodically/reconnect-triggered reconciles its persisted invalidation checkpoint against the durable D fence/target inventory and I revocation stream/checkpoint. The checkpoint is per authority/domain and records last contiguous observed position; gaps require replay/resync, not optimistic advancement.
- On gap, unavailable authority or unknown target coverage, affected cache namespaces are quarantined until full reconciliation. Do not clear the gap by resetting to latest without a snapshot base/cursor.
- Rebuild of invalidation state is idempotent; duplicate messages cannot reverse a tombstone or reinsert a target.
- TTL is only a capacity/retention optimization. TTL expiry is not a revocation/Forget protocol.

## 5. Index Rebuild, Backfill and Replay Contract

F owns index projections and IndexWatermark, but D owns ForgetFence and producer admission semantics. Index work is derivative-capable and must be registered with D before queueing/execution according to D's F producer-class requirements.

### 5.1 Admission and lineage

Every rebuild/backfill/replay job must carry:

- stable F ProducerWorkItemId registered with D and enabled ProducerClass/registry version;
- exact source snapshot CanonicalCommitCursor and source canonical refs/revisions/lineage digest;
- target ScopeRefs and security-domain binding;
- observed D ForgetFence and I PermissionEpoch (typed separately);
- index ID, partition ID, schema/coverage version, job/run/attempt IDs and idempotency digest;
- replay start/end cursors and a contiguous checkpoint; no consumer transport offset is substituted for CanonicalCommitCursor.

No job may start, lease, retry, DLQ-replay, backfill or publish an index segment until the D RegistrationReceipt is durably resolved. Lost registration response is reconciled by stable work ID/digest; it is not assumed accepted. A rebuild job is not exempt because it is “maintenance”.

### 5.2 Snapshot, replay and visibility

1. Obtain a consistent canonical snapshot at D-issued CanonicalCommitCursor N.
2. Read canonical records at exact versions and preserve source/derivative lineage. Apply current Scope and I permission filters before staging.
3. Exclude records/ancestors covered by current D ForgetFence, Forgotten/retracted/ineligible lifecycle, expired retention or unauthorized Evidence/Provenance. Unknown fence/lineage is quarantined, not included.
4. Replay committed canonical events strictly after N in canonical order. Delivery may be at-least-once; deduplicate by stable event/commit identity. Stage out-of-order events but do not advance contiguous applied-through cursor across a gap.
5. Re-check current D fence and I permission for all staged records/lineage immediately before segment publication/swap. A pre-scan fence snapshot is not publication authority.
6. Publish/swap segment only through the D-defined registered derivative publication boundary and required final fence/permission gate. If the callable D operation/Storage realization is not available, keep output private/quarantined; do not simulate success with a local check-then-swap.
7. Advance the exact partition IndexWatermark only to the highest contiguous CanonicalCommitCursor fully accounted for by the published segment, including explicit no-op coverage. Never advance across missing/failed/schema-incompatible events.
8. After publication, candidate lookup still revalidates canonical version/lifecycle, Scope, PermissionEpoch and latest ForgetFence. A segment watermark never substitutes for those checks.

### 5.3 No-resurrection and rebuild recovery

- A forgotten source or any derivative whose transitive lineage includes it is excluded, even if the source appears in an old snapshot, backup, event replay, stale segment or cache.
- Rebuild cannot create a new Memory ID, new derivative identity or detached lineage to evade an existing fence.
- A late derivative discovered after a prior closed-world proof is suppressed/quarantined and reported as a barrier-integrity violation; F notifies D/I and does not silently advance the watermark as if nothing happened.
- If a fence advances during rebuild, cancel or invalidate the affected staged generation; re-scan/rebuild under the new authority state. Never publish the pre-fence generation.
- If a partition is locally behind, mark only that partition stale/degraded; do not label the whole index current. Other partitions may serve only if their own scope/coverage and current fence/auth checks pass.
- Index rebuild success is not Forget completion, and an empty index result is not evidence of absence/erasure.

## 6. ActivationRecommendation boundary

ActivationRecommendation is an immutable F-authored **proposal** containing candidate refs, exact MemoryVersionRefs, reason codes, relevance/suitability/urgency hints, expiry, budget estimate, completeness/freshness, policy/fence checkpoint and correlation IDs.

It is not:

- a ContextEntry or ContextChangeSet;
- a ContextVersion allocation/commit;
- authority to add/remove/retain Memory in G Context;
- an Adapter delivery or Applied Attestation;
- proof that an Agent saw, attended to, remembered or acted on Memory.

G independently validates current canonical version/lifecycle, Scope, PermissionEpoch, ForgetFence, Context budget and policy before any Context mutation. G may reject, defer, transform or ignore the recommendation. If policy/fence changes after F emits it, the proposal is stale and must be revalidated by G; F cannot preserve its validity by a local score or TTL. H/C own delivery and final inference evidence; F never labels a recommendation Applied.

## 7. Conformance Matrix

The cases below define required behavior and evidence. They are **test specifications**, not claims that tests have run.

| ID / case | Input / injected ordering | Expected result | Forbidden result | Observable evidence |
|---|---|---|---|---|
| F35-01 Fence advances during Retrieval | Request starts at fence F0; channel returns candidate; D commits F1 covering candidate/ancestor before final return | Cancel affected work; candidate removed from fusion/materialization/response; unaffected authorized candidates may return as partial; final D check observes F1 | Returning candidate based on F0, even if cache/index watermark is fresh; claiming complete | F0/F1 refs, fence event correlation, cancellation state, final-check result, suppressed target digest, response completeness |
| F35-02 Permission revoked during Retrieval | Request authorized at I epoch P0; I revokes affected grant to P1 after candidate generation but before materialization/return | Candidate and cached payload denied; final authorization recheck blocks; fail closed if P1 cannot be confirmed | Using P0 until TTL/next request; returning evidence/snippet or existence count | policy-domain/epoch refs, decision IDs, invalidation checkpoint, denial reason, final response digest |
| F35-03 Cache hit contains old Memory | Exact query key hits cached version whose fence, PermissionEpoch, scope or lifecycle is stale | Treat as Stale Entry; drop/quarantine; current authorization/fence check; safe source reread or deny | Treat stale as ordinary hit; serve with warning; assume key alone authorizes | cache key dimensions, mismatch field, stale-suppression metric, canonical/auth recheck |
| F35-04 Index Rebuild reads old data | Snapshot/replay contains a source or descendant now covered by D fence | Exclude/quarantine lineage; do not publish affected staged segment; rebuild under current fence if needed | Publishing old payload under new segment/generation or detached derivative ID | ProducerWorkItemId/RegistrationReceipt, snapshot cursor, fence decision, excluded lineage digest, publication-gate receipt or quarantine |
| F35-05 Watermark lags | Required canonical cursor N; one partition watermark remains at N-k with a gap | Bounded canonical read-through/wait; else explicit partial/degraded/unavailable per consistency requirement; report partition gap | Claiming complete/strong read-your-write; treating watermark as Forget proof | Per-partition watermark, required cursor, gap event IDs, read-through outcome, completeness reason |
| F35-06 Late Derivative | A derivative from pre-fence work is discovered after barrier/proof or appears after current index scan | Suppress immediately; quarantine; notify D/I; register target/lineage and reopen affected reconciliation evidence | Returning/indexing derivative because source scan had finished or its work item was previously terminal | Derivative ref/lineage digest, source work ID, fence ref, barrier-integrity alert, quarantine status |
| F35-07 Cross-Scope Candidate | Backend returns or attempts to return a candidate whose ScopeRef is outside trusted request scopes | Reject inside backend boundary before Runtime candidate buffer; no fusion/reranker/cache/Working Set exposure | Global ANN top-K then app post-filter; count/score/timing disclosure; scope inference from query text | Backend filter plan, denied-before-emission evidence, reranker input digest excluding target, non-disclosing trace |
| F35-08 Reconnect restores old Working Set | Session reconnects with persisted entries from prior PermissionEpoch/fence/ContextVersion | Authenticate; obtain current I epoch and D fence; invalidate/quarantine old set; reconcile G target; restore only currently authorized entries | Restore first then asynchronously clear; replay stale snapshot/delivery | old/new session generation, epoch/fence checkpoints, invalidation receipts, G target version, restored-entry digest |
| F35-09 Duplicate Invalidation | Same event/operation ID + same target digest delivered multiple times, including after restart | Idempotent no-op after first durable disposition; retain tombstone and evidence; no duplicate side effects | Reinsert content, regress fence/checkpoint, duplicate success counted as extra coverage | idempotency key/digest, first and duplicate dispositions, stable invalidation generation |
| F35-10 One Index Partition Lags | Multi-partition index: p1 current, p2 behind/gapped; request spans both | Per-partition freshness; p1 may serve only if independently authorized/fence-safe; p2 uses read-through or returns partial/degraded; global completeness reflects p2 omission | Max(p1,p2) scalar hides p2 lag; claim all partitions current | partition watermark vector, per-partition completeness, replay gap, query plan and response freshness |

### 7.1 Additional required assertions

- Reranker never receives unauthorized, forgotten, revoked or cross-Scope candidates.
- Evidence and Provenance are independently authorized even when parent Memory is readable.
- Late channel completion after cancellation cannot repopulate cache/Working Set or alter an already finalized response.
- A request that cannot establish current D/I authority returns no affected protected payload.
- Rebuild/replay uses stable IDs and idempotency; retry cannot mint new publication rights.
- No F test may assert global Forget completion or physical erasure based solely on F-local state.

## 8. Observability and audit contract

Every request/job/invalidation trace should correlate (without exposing protected content) the following as applicable:

- request/job/work/attempt/run IDs and correlation/causation IDs;
- authenticated Principal binding reference, trusted Scope digest and purpose;
- I PermissionEpoch and authorization decision reference;
- D ForgetOperation/Fence reference and fence-check result;
- CanonicalCommitCursor, AggregateRevision and LifecycleEventCursor as separate typed fields;
- Index ID, partition, IndexWatermark, coverage/schema version and contiguous-gap status;
- cache family, hit/miss/stale distinction, invalidation generation and action result;
- candidate counts only after authorization; suppressed-before-emission events must not reveal protected IDs/counts;
- cancellation, finalization and partial/degraded reasons;
- rebuild snapshot cursor, replay checkpoint, producer registration receipt and publication receipt/quarantine outcome.

Do not log forgotten plaintext, raw sensitive query/evidence, unauthorized IDs, cross-Scope counts or reconstructive cache payloads. Audit evidence is metadata/digests/references and follows I retention rules.

## 9. OPEN / dependency register

| ID | Open item | Owner | F disposition |
|---|---|---|---|
| F35-O1 | D/E/Storage callable API/schema and proven linearization for ProducerWork registration, fence install and final publication gate | D + E + Storage/Consistency | **BLOCKING** for production-safe F rebuild/backfill publication; quarantine if unavailable |
| F35-O2 | D canonical delta/read-through API, exact lineage query and lifecycle snapshot consistency | D | **OPEN**; strict request fails closed or partial per requested consistency |
| F35-O3 | E index event ordering, outbox replay, per-index/partition watermark schema and gap recovery | E + F | **OPEN** until owner schema and consumer tests align |
| F35-O4 | I PermissionEpoch domain/fan-out, revocation stream continuity and propagation SLA | I | **OPEN**; revalidate synchronously or fail closed |
| F35-O5 | I/D fence notification and target-inventory feed/checkpoint API for F reconciliation | I + D | **OPEN**; message loss repaired from durable authority, never assumed absent |
| F35-O6 | G candidate/evidence envelope, Context target hints and reconciliation trigger schema | G | **OPEN**; F emits immutable proposal only |
| F35-O7 | H authenticated session/Adapter binding and opaque token validation surface | H + I + B | **OPEN**; F does not infer identity from payload |
| F35-O8 | B ActorRef/ScopeRef approval and I permission binding across scopes | B + I | **CANDIDATE / OPEN**; no schema freeze |
| F35-O9 | C/H final inference boundary evidence and G Applied mapping | C + H + G | F does not claim Applied; no dependency for Retrieval correctness |
| F35-O10 | ANN backend true pre-filter guarantee; if absent, per-Scope partition or safe exact fallback | F implementation | **TO_VALIDATE**; no post-filter fallback |
| F35-O11 | Cancellation race semantics and final-return linearization under chosen runtime/storage stack | F + Storage/Consistency | **TO_VALIDATE** with concurrency/fault injection |
| F35-O12 | Cache TTL, size, invalidation SLO, per-session budgets, rebuild throughput and P95/P99 | F | **TO_VALIDATE**; no numeric performance claims |

### 9.1 Explicit non-closure

- D's semantic decision for one global CanonicalCommitCursor per Brain authority is consumed; storage implementation and F consumer conformance remain OPEN.
- D's Forget operation semantics are more precise, but D/E/Storage atomic interface and production realization are not proven.
- I's global Forget vector/completion policy remains I-owned; F provides only per-index/cache/Working Set evidence.
- H ACK statuses are Adapter-local and cannot be treated as F index/cache acknowledgements or global completion.
- G ContextVersion is authoritative only within G; F recommendation is not a Context commit.
- C's final-request boundary is not observable by F; F cannot infer model attention or behavior.

## 10. HEAD and source evidence

### 10.1 Dependency branch heads observed during this review

| Owner | Branch | HEAD SHA |
|---|---|---|
| F | `session-f-memory-runtime` | `8b16a3621cbe2be4badac1799822b64824532b25` (review base HEAD) |
| D | `session-d-memory-brain-2026-11-16` | `da8e5882d0b238d765d00b2225b79eea45a483b1` |
| E | `session-e-memory-compiler-2026-11-16` | `c2f14408ba62447c11172d65b93a279fef96d175` |
| I | `session-i-security-governance-2026-11-16` | `5591ad3620ec3f5d74194bd79556dcf3e25bea07` |
| G | `session-g-memory-context` | `3d2c065be863bc1d349faaeece6f6eaa0047abae` |
| H | `session-h-bmcp-protocol` | `1ee65928f123d92a4758b0de09bc8d6df1e46253` |
| C | `session-c-agent-integration-2026-11-16` | `a585307222b0169c007915c25ff8ed0da517f3e4` |
| B | `session-b-domain-model-phase3` | `66adf6bdcf5ec69a146fe75afe20ce3b85af8448` |

HEADs were read from branch-vs-main commit comparisons in this review. They are review-time snapshots, not pinned dependencies; re-read before merge/freeze.

### 10.2 Exact source artifacts read

- Integration baseline: `reviews/integration/phase-3-defghi-cross-module-contract-review.md` on main at review-time.
- D: `03-memory-brain/forget-fence-and-completion-contract.md`; `03-memory-brain/commit-cursor-semantics.md`; `03-memory-brain/forget-fence-operation-and-publication-gate.md`.
- E: `04-memory-compiler/forget-fence-and-derived-registration.md`; `04-memory-compiler/compiler-state-and-producer-admission.md`.
- I: `09-security-governance/forget-retention-backup-and-erasure-policy.md`; `09-security-governance/scope-and-revocation-policy.md`; `09-security-governance/global-forget-target-inventory-and-completion-evidence.md`.
- G: `06-memory-context/context-reconciliation.md`; `06-memory-context/context-versioning.md`.
- H: `08-bmcp-protocol/phase-3-5-identity-applied-ack-reconnect-contract.md`; `08-bmcp-protocol/forget-revocation-and-reconnect.md`; `08-bmcp-protocol/adapter-forget-ack-and-target-binding.md`; `08-bmcp-protocol/message-envelope-and-versioning.md`.
- C: `07-agent-integration/phase-3.5-agent-identity-applied-attestation-untrusted-memory.md`; `07-agent-integration/final-inference-boundary-attestation.md`; `07-agent-integration/security-and-untrusted-memory-boundary.md`.
- B: `02-domain-model/typed-reference-and-scope-semantics.md`.

### 10.3 Verification status

- Static contract review: performed.
- F documentation changes: recorded by the commits listed in the delivery response.
- Repository reread of changed F documents: required after write and recorded in the delivery response.
- Runtime implementation tests, concurrent fence/revocation tests, cache-loss/reconnect tests, index rebuild tests, performance benchmarks and fault injection: **NOT RUN / NOT CLAIMED**.


## 11. Phase 3.5 reprocessing addendum — D/E/I/H alignment

This addendum supersedes the earlier source snapshot and OPEN descriptions only where explicitly updated here. The owner authorities remain unchanged.

### 11.1 Current owner decisions consumed

- **D @ `da8e5882d0b238d765d00b2225b79eea45a483b1`:** operation semantics are DECIDED for `RegisterProducerClass`, `RegisterProducerWork`, `InstallForgetFence`, `CaptureProducerRegistrationHighWater`, `RegisterDerivedDependency`, `PublishDerivedIfFenceCurrent`, `CompleteProducerWork`, `ResolveProducerWork` and `ReconcileForgetBarrier`. These are normative semantic operation names, not callable API/schema claims. Producer registration and fence installation serialize in one D ordering domain; final visibility must serialize with fence installation. Storage transaction/CAS or equivalent recovery realization and cross-owner conformance remain OPEN.
- **E @ `c2f14408ba62447c11172d65b93a279fef96d175`:** F consumes E's private-staging, stable work/run/attempt identity, complete dependency registration, current auth/fence recheck, final publication gate and terminal receipt distinctions. E's detailed contract still cites an older D baseline (`30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6)); D's current operation-level contract above takes precedence. E must refresh that dependency baseline; F does not edit E-owned files.
- **I @ `5591ad3620ec3f5d74194bd79556dcf3e25bea07`:** ProducerDomainInventoryEpoch/TargetInventorySeal/TargetId and global target/component states are I-owned. They are distinct from D ProducerRegistrationHighWater and F IndexWatermark. F supplies exact per-index/per-partition, cache and Working Set suppression/freshness evidence; I alone evaluates target confirmation, exceptions and global completion.
- **H @ `1ee65928f123d92a4758b0de09bc8d6df1e46253`:** Adapter ACK classes remain bounded to exact authenticated Adapter instance/session/Scope/Managed Region/capability slice. SUPPRESSED, LOCAL_BUFFER_CLEARED, LOCAL_CACHE_PURGED, QUEUED_DELIVERY_CANCELLED, FAILED, UNKNOWN and UNSUPPORTED are non-equivalent. H cannot mint I TargetId or declare I Target State. The current H reprocessing contract remains CANDIDATE pending B/C/D/G/I approvals.
- **C @ `a585307222b0169c007915c25ff8ed0da517f3e4`:** Full Applied requires exact final immutable request submission evidence at the trusted boundary and all required identity/context/permission/fence bindings. F does not observe or claim Applied, model attention or behavior.
- **G @ `3d2c065be863bc1d349faaeece6f6eaa0047abae`:** ContextVersion and reconciliation/delivery state remain G-owned. F output is only a candidate/recommendation envelope.
- **B @ `66adf6bdcf5ec69a146fe75afe20ce3b85af8448`:** ActorRef/ScopeRef are typed domain references, not credentials/grants; the domain contract remains CANDIDATE pending required ADR/identity approval.

### 11.2 F index producer protocol

For every derivative-capable or durable/rebuildable F index operation:

1. F's producer class/capability (including rebuild, backfill, replay and recovery) must be registered and ENABLED in D's versioned producer registry before work admission.
2. Allocate/persist one stable `ProducerWorkItemId` and canonical request digest. Call D's semantic `RegisterProducerWork` and obtain/reconcile the durable `RegistrationReceipt` before enqueue, lease, canonical source dereference or execution.
3. Preserve `ProducerRegistrationSequence/HighWater`, `CanonicalCommitCursor`, `ForgetFenceCursor/Generation` and I `PermissionEpoch` as separate typed fields. Retry/lease replacement retains WorkItemId/digest; AttemptId/LeaseId change only as E/D semantics permit.
4. Stage index segment privately. Register complete source/transitive lineage and artifact dependencies through D's `RegisterDerivedDependency` semantic operation. Missing, partial or ambiguous receipt keeps the segment private.
5. Publish/swap only through D's `PublishDerivedIfFenceCurrent` semantic gate bound to the same durable visibility transition. If D/Storage cannot provide the callable operation and atomic/recoverable visibility boundary, quarantine the staged generation; a local check-then-swap is forbidden.
6. Record durable publication outcome and terminal work disposition using D's publication/terminal evidence semantics. Unknown ACK is reconciled by stable operation/work IDs; it is never assumed successful.
7. Advance only the exact partition's IndexWatermark after the visible segment accounts for a contiguous canonical prefix including explicit no-op coverage. No cross-partition max or cursor substitution.

### 11.3 I target-evidence contract for F

F emits evidence only for its own declared producer/consumer surfaces: index ID + partition, cache family/namespace, Working Set/session namespace, rebuild worker and suppression/invalidation checkpoint. Evidence binds ForgetOperationId, I TargetId/inventory seal when supplied by I, exact ScopeRef coverage, D fence reference, relevant I PermissionEpoch, per-partition IndexWatermark/coverage/schema, action/postcondition, attempt, timestamp, authenticated F producer identity and integrity/audit references. F does not create TargetId, seal inventory, decide NotApplicable, mark global component Confirmed or convert a watermark into target absence. A partition gap or unknown coverage is Unknown for the affected target slice.

### 11.4 OPEN items refined

- **F35-O1 remains BLOCKING:** D operation semantics are now explicit, but callable D API/schema, storage transaction/CAS or equivalent prepare/commit/recovery proof, and cross-owner linearization tests are not evidenced.
- **F35-O3 remains OPEN:** E's current contract is candidate and its source baseline still references old D head; E must reconcile current D operations, outbox/replay ordering and F per-partition watermark schema.
- **F35-O4/O5 remain OPEN:** I PermissionEpoch fan-out/currentness, revocation-stream continuity, target inventory feed/seal and per-target evidence acceptance API are not frozen. Reconcile synchronously or quarantine/fail closed.
- **F35-O6 remains OPEN:** G candidate/evidence/reconciliation envelope and Context target hints are not a frozen F interface.
- **F35-O7/O8 remain OPEN:** H/B/I authenticated identity, typed-reference serialization and exact target binding require owner approval; payload labels never substitute.
- **F35-O9 remains non-blocking for Retrieval correctness:** C/H/G Applied evidence is downstream and cannot be inferred by F.
- **F35-O10/O11/O12 remain TO_VALIDATE:** ANN pre-filter implementation, cancellation/final-return race behavior, TTL/capacity/invalidation SLO and performance budgets require actual tests.
- **Additional integration note:** The Phase 3 D/E/H/I cross-module review on main @ `8a6414158c9c056c1638222534e1993d1bbc99d2` remains CONDITIONAL PASS for continued integration only; CR-P1-01, CR-P1-02, CR-P1-05 and identity/target mapping are not freeze-closed.

### 11.5 Verification boundary

This reprocessing is static contract/document review and GitHub read-back only. No concurrent fence/revocation test, cache loss/reconnect test, index rebuild/replay test, ANN pre-filter test, performance benchmark, fault injection or production implementation validation is claimed.


## 12. Re-review snapshot — 2026-11-16

This snapshot supersedes the earlier C branch SHA recorded in §§10.1 and 11.1. The branch was re-read at the following current heads before this F documentation correction:

| Owner | Branch | Re-read HEAD |
|---|---|---|
| A | `session-a-integration-2026-11-16` | `f18c64950a84385bd407752c7188e1bd52029a7b` |
| B | `session-b-domain-model-phase3` | `66adf6bdcf5ec69a146fe75afe20ce3b85af8448` |
| C | `session-c-agent-integration-2026-11-16` | `a585307222b0169c007915c25ff8ed0da517f3e4` |
| D | `session-d-memory-brain-2026-11-16` | `da8e5882d0b238d765d00b2225b79eea45a483b1` |
| E | `session-e-memory-compiler-2026-11-16` | `c2f14408ba62447c11172d65b93a279fef96d175` |
| F | `session-f-memory-runtime` | `badc8b9998236c0075ab32c4ae8dc58c8c51984a` (pre-correction HEAD) |
| G | `session-g-memory-context` | `3d2c065be863bc1d349faaeece6f6eaa0047abae` |
| H | `session-h-bmcp-protocol` | `1ee65928f123d92a4758b0de09bc8d6df1e46253` |
| I | `session-i-security-governance-2026-11-16` | `5591ad3620ec3f5d74194bd79556dcf3e25bea07` |
| Storage/Consistency | `session-storage-consistency-forget-atomicity-2026-11-16` | `3a14550648f21c0bc2725dac38b29e099c2f3196` |
| Integration baseline | `main` | `8a6414158c9c056c1638222534e1993d1bbc99d2` |

The Cursor Consumer Matrix now explicitly includes D ProducerRegistrationSequence/ProducerRegistrationHighWater and RegistrationReceipt as typed producer-admission evidence, not as canonical cursors. This aligns §§5.1–5.2 and 11.2 with the matrix without changing D ownership or inventing a callable API.

The Storage/Consistency branch contains a proposed realization review only; it is not an approved Storage authority or implementation evidence. D/E/Storage shared transaction/linearization and recovery remain OPEN. A's typed-cursor proposal is aligned to D's one-global-per-authority CanonicalCommitCursor decision, while Storage implementation and consumer conformance remain NOT VERIFIED.

The Phase 3 D/E/H/I review on main is a historical coordination baseline at the exact main HEAD above; its Conditional Pass is not a contract-freeze or implementation sign-off. E's current detailed source contract still carries an older D source baseline and requires E-owner reconciliation; F does not edit E-owned files.

**Re-review method:** branch HEAD/API metadata, source artifact fetch/read, static cross-contract comparison, F file fetch/read-back. **Not run:** runtime, concurrent, fault-injection, reconnect, rebuild/replay, ANN pre-filter, security integration or performance tests.
