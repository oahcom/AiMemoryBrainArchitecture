# Phase 3.7 — F Local Lifecycle: Producer, Derivative, Queue, Recall, Context and Restore

- Owner: F — Memory Runtime
- Branch: `session-f-memory-runtime`
- Status: **F-local semantic proposal; cross-owner interfaces and implementation remain OPEN / NOT VERIFIED**
- Scope: runtime retrieval, indexes, caches, Working Sets, runtime-owned derived projections, and reconnect/restore.
- Authority boundary: D owns canonical Memory, ForgetFence, producer registry and lineage; I owns authorization/PermissionEpoch; E owns compiler production; G owns Context and Applied/Delivery; H owns adapter transport/capability; Storage owns durable transaction/visibility evidence.

## 1. F's local lifecycle model

F is a consumer and projection maintainer, not a canonical Producer of Memory. F may itself create runtime-local derivatives (index segments, embeddings, query caches, entity/graph projections, summaries used only as retrieval aids, Working Set entries); those remain non-authoritative and must carry exact source lineage and Scope.

| Object | F-local states | Terminal / non-terminal meaning |
|---|---|---|
| Runtime ProducerWork | Requested → AuthorityChecked → DRegistered (when derivative-capable) → Queued → Leased → Running → Completed / Suppressed / Failed | Lease expiry, timeout, worker loss and DLQ are non-terminal until durable no-more-publication disposition is established |
| Runtime Derivative | Planned → BuildingPrivate → LineageRegistered → GatePending → VisibleProjection → Invalidated / Quarantined → Retired | VisibleProjection is only an F projection; never canonical truth or Forget completion |
| Queue item | Enqueued → Leased → Running → Acked / RetryScheduled / Quarantined / Cancelled | Queue ACK means local handling only; it does not prove indexing completeness or D barrier closure |
| Recall request | Admitted → CandidateSearch → AuthorityFiltered → CanonicalRevalidated → Ranked → FinalGate → Returned / Suppressed / Unknown | Only exact, current, authorized refs can cross FinalGate |
| Working Set / F Context | Created → PopulatedByRefs → Materialized → Active → Invalidated → Cleared / Quarantined | F Working Set is not G ContextVersion and has no Applied semantics |
| Restore unit | Discovered → Isolated → AuthorityReconciled → ReplayValidated → Rebuilt → GateEnabled | Never serve restored bytes before current I/D reconciliation |

## 2. Producer behavior

1. Every F activity that can create, retain, publish or later dereference a derivative is classified and registered with D before enqueue, lease, source dereference or execution.
2. Producer identity is stable across retries: producer class, ProducerWorkItemId, request digest, source refs/revisions, transitive lineage, Scope, admission cursor, observed D fence and I PermissionEpoch. AttemptId and LeaseId are separate and rotate on retry.
3. Pure read-only recall that creates no durable derivative may use the read authorization path; prefetch, cache fill, index build, graph expansion and retained summaries are derivative-capable and require producer registration.
4. Registration timeout is UNKNOWN: resolve by stable identity/digest; never create a new identity to bypass a barrier.
5. D fence installation captures its own producer high-water. Pre-fence work remains accounted until durable terminal/no-publication evidence; post-fence work referencing covered lineage is rejected or quarantined.
6. F cannot invent D receipts, close D's barrier, or claim global Forget completion.

## 3. Derivative behavior

- Every index row/vector/segment, cache entry, graph edge, retrieval summary and persisted Working Set snippet carries exact source/version references, Scope, lineage digest, producer identity, schema/index generation and authority provenance.
- Build into a private generation. Register complete direct and transitive dependencies with D before visibility.
- Final publication/activation must be serialized with D's latest fence and current I permission. If the cross-owner gate is unavailable or ambiguous, keep the generation private/quarantined.
- A derivative is invalidated when any covered source/ancestor is forgotten, permission is revoked, scope changes, source version is superseded, or schema/generation becomes incompatible.
- Rebuild/replay from old snapshots must re-check every source and lineage against current D/I state; successful rebuild and zero search hits are not Forget evidence.
- Physical byte erasure is a separate capability/evidence; F reports logical suppression and its own cleanup evidence only.

## 4. Queue behavior

- Queue records are durable work references, not authority. A queue message contains stable WorkItemId/digest and references to registered source/lineage, not unguarded plaintext as its authority.
- Delivery is at-least-once safe: same identity+digest is idempotent; same identity with changed digest is conflict. Attempt/lease generation fences stale workers.
- Lease expiry, queue deletion, retry exhaustion or dead-lettering never closes a D producer registration.
- Before every lease/run and before every projection visibility transition, refresh current I permission and D fence. Cancel is best-effort; final visibility gate is mandatory.
- Queue restore first quarantines all messages, reconciles producer ledger/high-waters and tombstones, then replays only eligible work. Unknown continuity blocks replay.

## 5. Recall behavior

- Authenticate principal, exact Scope, purpose and environment; obtain current I PermissionEpoch/decision and D fence context before candidate admission.
- Push scope filters into candidate generation; indexes return refs, not trusted content. Suppress stale/cross-scope candidates before buffers, fusion, counts, traces or reranking.
- Re-resolve exact Memory version, lifecycle, lineage and permission through D/I before materialization and again immediately before final return/handoff.
- IndexWatermark is partition-local and contiguous; gaps mean stale/incomplete, never deletion. Missing hit is not proof of absence.
- If authorization/fence/currentness is unknown, suppress affected content and return an explicit incomplete/unknown outcome; never serve stale cache as fallback.
- F does not claim G Context Applied, H adapter purge, C execution, or global Forget completion.

## 6. Context behavior

- F owns only its runtime Working Set and retrieval-local context. It may retain refs and, where authorized, protected snippets; every item remains scoped, versioned and lineage-bound.
- G's ContextId/ContextVersion, desired membership, Delivery and Applied records are external typed inputs to F, never aliases for F cache generation or IndexWatermark.
- F may provide candidate refs, freshness/completeness and materialization evidence to G. G decides Context membership and Applied; F cannot promote a candidate to Context or infer delivery.
- On scope/session/environment switch, invalidate namespace and prevent cross-context cache reuse. Revalidate permission and fence on every protected read.

## 7. Restore and reconnect

1. Restore indexes, caches, queues and Working Sets into an isolated/quarantined namespace.
2. Verify Storage restore evidence and reconcile COC committed prefix plus current I PermissionEpoch/registry and D ForgetFence/lineage/producer high-water; these authorities remain distinct.
3. Replay tombstones/fences through required high-waters; invalidate stale IndexWatermarks and all unproven cache generations.
4. Reconcile each queue item against D registration and current I/D state; stale attempts cannot publish.
5. Rebuild private index generations from eligible canonical sources, register lineage, and pass the current final gate before enabling reads.
6. Reauthenticate reconnecting runtime/session; clear or quarantine old Working Set before restoring a fresh one. Never restore then clean.
7. If any authority, prefix, lineage or participant continuity is unknown, keep affected partitions/queues/contexts suppressed. RestoreReconciliationReceipt is not IndexWatermark, D clearance, I authorization or Forget completion.

## 8. Required evidence and tests

F emits per-partition watermark/coverage, producer registration references, derivative lineage digest, queue disposition, cache/Working Set invalidation generation, recall suppression counts and restore reconciliation outcome. It must not overstate byte deletion or cross-owner completion.

Required tests: fence-vs-build race; revocation-vs-final-return race; duplicate/changed-digest queue delivery; lease expiry and stale worker; lost invalidation; partition gap; pre-fence snapshot rebuild; restore with stale replica; reconnect with old Working Set; unknown D/I authority. Tests are specifications until actually executed.

## 9. Non-goals / blockers

- No canonical Memory writes or Forget decisions.
- No ownership of G ContextVersion/Applied, H ACK, C execution, I policy, or D barrier.
- D/E/Storage atomic register-before-visible interface remains a blocking dependency where a derivative can become externally visible.
- **No runtime implementation, conformance PASS, physical erasure proof or production activation is claimed.**
