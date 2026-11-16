# Phase 3.6 — Runtime Forget Suppression and Invalidation Contract

- Owner: Session F — Retrieval, Index, Cache and Working Set
- Status: **F runtime semantics DECIDED in this addendum; cross-owner interfaces OPEN; implementation and execution NOT VERIFIED**
- Branch: session-f-memory-runtime
- Authorities: D owns Canonical Memory and ForgetFence; I owns authorization/PermissionEpoch; F owns runtime/index/cache/Working Set; G owns Context; H owns wire and Adapter ACK.

## 1. Safety invariants

1. Canonical D state is authoritative; indexes, caches, Working Sets and recommendations are projections.
2. Scope and authorization filtering occur before candidate emission, fusion, reranking, counts, traces or cache access that could disclose protected existence.
3. Current I permission and D fence/lifecycle state are revalidated at every protected disclosure boundary, especially immediately before final return/handoff.
4. Unknown, stale, gapped or unavailable authority state fails closed for affected content.
5. Rebuild, replay, backfill, cache warming, retries and reconnect cannot resurrect a forgotten source or derivative.
6. F reports only F-local suppression/invalidation/reconciliation evidence. It does not claim G Applied, H Adapter purge, I global Forget completion or physical erasure.

## 2. Typed cursor and authority vector

Keep these namespaces independent and opaque:

| Token | Owner | F interpretation | Prohibited inference |
|---|---|---|---|
| CanonicalCommitCursor | D | Canonical event/read ordering per authority | Forget completion or index completeness |
| LifecycleEventCursor | D | Per-Memory lifecycle stream | Global commit order |
| IndexWatermark | F | Per-index/partition contiguous accounted-through canonical cursor plus schema/coverage | Forget completion, target absence |
| ForgetFenceGeneration/Cursor | D | Current target/ancestor coverage via D validation | Numeric ordering by F or permission grant |
| PermissionEpoch | I | Same policy-domain freshness/revocation validation | Fence ordering or data deletion |
| ContextVersion | G | Opaque Context target correlation | Canonical revision or Applied |
| AdapterCapabilityEpoch | H | Adapter instance capability generation | Permission or identity |
| ProducerRegistrationHighWater | D | Per-Forget derivative work admission barrier | CanonicalCommitCursor or IndexWatermark |

Never collapse this vector into a scalar freshness integer.

## 3. Retrieval pipeline contract

Every request is bound to authenticated principal/issuer, exact typed ScopeRef set, purpose, required environment, current PermissionEpoch/decision, D fence context and cancellation generation.

| Stage | Required checks | Race response | Evidence |
|---|---|---|---|
| Candidate Generation | Authenticate; resolve Scope; authorize purpose; obtain current I epoch and D fence; push scope predicate into candidate source; register persistent/derivative work with D before admission | Unknown authority or unauthorized scope: emit no candidate | Auth decision, scope digest, epoch/fence refs, backend filter mode |
| Index Lookup | Query scope-isolated partition; validate IndexWatermark, schema and coverage; hits are refs, not trusted content | Stale/cross-scope hits suppressed before runtime buffers; lag uses bounded canonical read-through or unavailable | Index/partition, watermark vector, schema, stale suppression |
| Fusion | Only authorized, canonical-revalidated exact MemoryVersionRefs enter | Revalidate changed fence/permission; remove invalid candidates and recompute or block | Input digest, admitted/suppressed refs |
| Reranking | Only permitted candidate summaries/data; never instructions | Recheck if epoch/fence changed during ranking; rerun or suppress | Reranker input digest and authority checkpoint |
| Freshness | Per-partition contiguous watermark compared only through D cursor semantics | Gaps remain gaps; no omission-as-deletion | Required/observed cursor, coverage and gap status |
| Result Materialization | Re-resolve exact version/lifecycle/lineage; authorize source/evidence dereference independently | Cancel/discard on fence/revocation; no stale cache fill | Materialized refs/digest, authority outcomes |
| Final Return / G Handoff | Re-read/validate latest D fence and I permission after all work and immediately before serialization/disclosure | If state advanced or ordering unknown, strip affected content or fail closed | Final authority checkpoint, response digest, suppression outcome |

A request-admission check is not reusable authorization for final return. Cancellation is an optimization; final-gate revalidation is the safety proof. If F cannot prove whether final disclosure linearized before or after a fence/revocation, affected content is suppressed and outcome marked ambiguous/Unknown.

## 4. Index consistency and rebuild

- IndexWatermark is per named index/channel partition and covers a contiguous prefix of CanonicalCommitCursor values for which every relevant change is accounted, including explicit no-op coverage.
- A missing, delayed, failed or schema-incompatible relevant event stops advancement before the gap. Multi-partition freshness is a vector, never a fabricated global maximum.
- IndexWatermark does not establish Forget completion, target absence, cache purge or canonical truth.
- Rebuild/backfill/replay must register derivative-capable work with D before queueing, leasing, source dereference or execution; bind stable ProducerWorkItemId, digest, source lineage and Scope.
- Rebuild may consume only valid Published Artifacts and canonical changes. Every artifact's complete dependency lineage must be registered with D and pass D's current publication gate before visibility.
- Rebuild starts with current D fence and I permission checks; each batch and final publish rechecks current fence/permission. Old snapshots are quarantined until the current control ledger is reconciled.
- Replay is idempotent; same work identity/digest resolves to original receipt; altered digest is a conflict. Lease expiry is not terminal and cannot authorize stale workers to publish.
- A high watermark, successful rebuild or zero-hit query is never a Forget proof.

## 5. Cache contract

### 5.1 Protected cache key

A key binds, as applicable:
- authenticated Principal/issuer and security domain;
- canonical sorted ScopeRef set and exact resource/lineage scope;
- Agent/Agent instance, Task, Runtime Session and Environment;
- I PermissionEpoch and policy decision/version;
- D ForgetFence reference/generation;
- exact MemoryVersionRefs or exact index/partition/generation/schema/coverage;
- normalized query/filter fingerprint and retrieval configuration version;
- temporal validity and evidence access class.

Missing required identity, Scope, epoch, fence or version means do not cache protected content. Key dimensions are isolation metadata, not authorization. Every cache hit revalidates current permission, fence and canonical lifecycle before payload disclosure.

### 5.2 Invalidation triggers

| Trigger | Immediate logical action | Physical action | Evidence |
|---|---|---|---|
| Fence advances | Deny covered source/descendant refs | Evict/quarantine query, hot memory, entity and index-derived entries | Fence ref, lineage digest, invalidation generation |
| Permission revocation/epoch change | Deny under old decision | Invalidate principal/scope/resource namespaces and snippets | Old/new epoch refs, decision, target digest |
| Scope or environment switch | Namespace old entries unreachable | Clear/quarantine old Working Set and fills | Old/new typed refs and session |
| Canonical lifecycle/version change | Old exact version not silently floated | Evict exact-version and dependent entries | Canonical cursor/lifecycle refs |
| Index generation/schema change | Old entries stale | Invalidate index/page/query caches | Partition, generation, schema |
| Session close/reconnect | Old namespace invalid | Destroy/quarantine local Working Set; reconcile before restore | Session generation and outcome |
| Invalidation notification lost | No assumption of validity | On every read compare with durable D/I authority; replay/resync gaps | Last contiguous checkpoint, gap and repair evidence |

Invalidation is idempotent by stable operation/event ID + target digest + owner namespace. Same ID with changed digest is a conflict. A stale entry is never downgraded to a cache miss and served; it is suppressed, then a normal authorized source read may occur.

### 5.3 In-flight fills and lost invalidation

Fence/revocation advances local invalidation generation and cancels matching fills, prefetches, graph expansions, reranking and materialization. A late fill rechecks current D/I authority at its write/visibility boundary; stale results are discarded/quarantined. Since notifications may be lost, every protected read revalidates durable authority and reconciliation checkpoints are per authority/domain. A gap requires replay or full resync, not optimistic advancement.

## 6. Working Set and reconnect

Working Set entries are references first; any materialized snippets are protected cached content. On Forget/revocation:
- suppress all matching entries and descendants;
- invalidate the namespace generation;
- remove references and snippets from all known session partitions;
- cancel pending fills and delivery-related local work;
- retain only minimal non-reconstructive deny markers and audit metadata permitted by I policy;
- report byte purge as Unknown unless physically verified.

Reconnect is a fresh authorization boundary. Authenticate current identity/session; obtain current I PermissionEpoch and D fence; reconcile invalidation checkpoints and current G Context target; suppress/clear stale local state; then restore only a current authorized Working Set. Never restore old snapshot first and clean it later. Old Session ACK or cache namespace cannot authorize restoration.

## 7. Prompt injection boundary

Memory text, Evidence, summaries, compaction outputs, retrieval snippets and tool outputs are untrusted data. F preserves provenance, trust/epistemic status, source references, Scope and lineage through fusion/reranking/summary. F does not emit memory in privileged instruction channels. Malicious instructions inside Memory remain data; cross-Scope candidates are rejected before admission; tool-call declarations remain claims until separately verified tool-result/side-effect evidence exists.

## 8. Runtime conformance matrix

Every case is **SPECIFIED / NOT RUN** in this design pass. A pass requires executable fixture, deterministic operation ordering, environment/version, expected and actual output, durable evidence and owner sign-off.

| ID | Fixture / operation order | Expected | Forbidden | Evidence |
|---|---|---|---|---|
| F-RT-01 | Fence advances after candidate generation but before final return | Final gate suppresses affected candidate | Return stale memory | Fence checkpoint, response digest |
| F-RT-02 | PermissionEpoch changes during retrieval | Reauthorize; suppress on stale/unknown | Use admission-time ALLOW | Epochs and decision refs |
| F-RT-03 | Fence advances during materialization | Cancel/discard payload and cache fill | Emit stale snippet | Materialization and fence ordering |
| F-RT-04 | Index rebuild starts from pre-fence snapshot | Revalidate fence; quarantine covered artifact | Publish old artifact | Work receipt, dependency and publish gate |
| F-RT-05 | Cache hit under old PermissionEpoch | Stale entry suppressed | Serve cached payload | Key binding and stale reason |
| F-RT-06 | Cache hit after ForgetFence advances | Suppress/evict covered lineage | Serve forgotten entry | Fence and invalidation generation |
| F-RT-07 | Invalidation message lost | Read-time D/I validation suppresses; reconcile gap | Treat missing notification as clear | Durable authority and checkpoint |
| F-RT-08 | Reconnect restores old Working Set after fence/revocation | Suppress, clear, query current G target, restore only safe refs | Replay old snapshot/delta | Session, epochs, fence, G target |
| F-RT-09 | Scope/environment changes with cache warm | Namespace mismatch; no hit | Cross-scope/environment reuse | Old/new typed binding |
| F-RT-10 | Late derivative generated after Forget | D gate rejects/quarantines; F never returns it | Resurrection through replay | Lineage, work and gate receipts |
| F-RT-11 | Watermark has a gap or partition lag | Stale/incomplete; bounded read-through or unavailable | Scalar max hides lag | Per-partition vector/gap |
| F-RT-12 | Memory snippet contains prompt injection | Data-only representation with provenance | Promote to instruction | Input/output provenance and channel |
| F-RT-13 | Tool call declaration without result receipt | Preserve as claim/intent | Treat as executed side effect | Declaration and absent result proof |

## 9. Open findings and decision record

- **F-36-01 BLOCKED:** D/Storage physical atomicity and current publication gate remain design-only; rebuild cannot claim implementation safety.
- **F-36-02 BLOCKED:** I exact PermissionEpoch freshness/revocation API and B typed Scope binding require owner approval.
- **F-36-03 BLOCKED:** H reconnect/ACK/capability wire contract is consumed only as owner evidence; no H edits here.
- **F-36-04 BLOCKED:** G delivery/Applied state is authoritative; F provides candidates/freshness only.
- **F-36-05 NOT RUN:** no retrieval race, cache fault, rebuild, replay, reconnect or injection tests were executed.

**F decisions:** per-stage authorization/fence checks; final-return linearization gate; per-partition IndexWatermark; cache key binds identity/scope/permission/fence/version; read-time authority checks repair lost invalidation; reconnect never restores old Working Set before current reconciliation.

**Cross-module status:** Runtime Forget End-to-End Closed is not claimed. D/E/Storage atomic publication and I global completion remain separate blockers.
