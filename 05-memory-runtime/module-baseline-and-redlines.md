# F Module Baseline & Redlines — Memory Runtime

**Proposal ID:** DEF-G0-F-001  
**Owner:** F — Memory Runtime Architect  
**Status:** PROPOSED — Owner Review Required  
**Version:** 0.1.0  
**Branch:** `session-f-memory-runtime`  
**Authority:** F owns retrieval/runtime projections and F-local suppression evidence only.

## 1. Module Mission

F retrieves authorized, current, evidence-bearing Memory candidates from canonical and derived representations and maintains safe runtime-local projections, indexes, caches and Working Sets. Retrieval is not canonical truth, Context mutation or authorization. F must prevent unauthorized or forgotten content from entering candidate buffers or crossing any disclosure boundary, and must prevent rebuild/replay/reconnect from resurrecting forgotten material.

## 2. Ownership Baseline

F owns:
- Retrieval request planning, channel routing, candidate generation orchestration, fusion, deduplication, ranking and completeness reporting.
- Index projection implementation and per-index/channel/partition IndexWatermark.
- Runtime query/embedding/lexical cache, Working Set and in-flight retrieval/materialization/fill lifecycle.
- F-local invalidation, suppression, cancellation, eviction/quarantine, rebuild/backfill/replay and reconciliation checkpoints.
- F-local evidence for candidate suppression, index freshness, cache/Working Set invalidation and retrieval outcomes.

F does not own Canonical Memory identity/revisions/lifecycle/CanonicalCommitCursor/ForgetFence/producer barrier (D), compiler derivation/publication (E), PermissionEpoch/authorization/global Forget policy (I), Context/ContextVersion/Applied (G), Adapter wire/reconnect acknowledgement (H), or final inference-boundary inclusion (C).

## 3. Capability Baseline

1. Scope- and permission-constrained structured, entity, full-text, ANN, graph, temporal and provenance/evidence retrieval.
2. Scope and authorization predicates bound inside every candidate-producing backend before candidate emission.
3. Canonical revalidation of exact MemoryVersion, lifecycle, lineage and current ForgetFence before fusion and disclosure.
4. Evidence-aware ranking that preserves epistemic status, conflict alternatives, provenance and validity.
5. Per-index/channel/partition contiguous IndexWatermark with coverage/schema and explicit gap state.
6. Bounded canonical read-through or explicit partial/degraded/unavailable outcomes when projections lag.
7. Cache and Working Set isolation by principal, scope, environment, permission epoch, ForgetFence and exact version/generation.
8. Cancellation/invalidation of affected in-flight work and final authority recheck before cache fill/write and final return.
9. Rebuild/backfill/replay registered with D before derivative-capable work and fenced against resurrection.
10. Reconnect as a fresh authorization boundary; reconcile current D/I state before restoring any old Working Set.
11. F-local suppression/cleanup evidence without claiming D canonical completion, G Applied, H purge, I global Forget or physical erasure.

Routing/fusion thresholds, ranking weights, ANN implementation and latency budgets remain CANDIDATE/TO_VALIDATE.

## 4. Domain Ownership

| Domain object | Owner | F obligation |
|---|---|---|
| Canonical Memory / MemoryVersion / lifecycle | D | Resolve exact typed refs; canonical state wins |
| CanonicalCommitCursor | D | Consume unchanged; per-authority canonical order |
| LifecycleEventCursor | D | Consume per-Memory lifecycle stream |
| ForgetFenceCursor/Generation | D | Resolve latest applicable target/ancestor fence |
| ProducerRegistrationHighWater | D | Register F derivative-capable work before admission |
| Index projection / IndexWatermark | F | Contiguous per-index/channel/partition accounted-through canonical cursor |
| Cache / Working Set / in-flight Retrieval | F | Invalidate, cancel, quarantine and revalidate |
| PermissionEpoch / authorization | I | Consume current authorization independently of D fence |
| ContextVersion / Applied | G | Read-only correlation; never mutate or claim |
| Compiler Published Artifact | E/Storage gate | Consume only owner-confirmed publication evidence |
| Adapter clear/reconnect evidence | H | Consume opaque evidence; no wire or ACK authority |

## 5. Interface Baseline

### 5.1 Typed cursor mapping

Keep these types separate and opaque:
- `CanonicalCommitCursor`: D's authority-local order of successful canonical transactions.
- `LifecycleEventCursor`: D's per-Memory append-only lifecycle order, with enclosing canonical commit reference.
- `IndexWatermark`: F-owned per-index/channel/partition contiguous applied-through CanonicalCommitCursor plus coverage/schema identity and gap state.
- `ForgetFenceCursor`: D-owned operation/generation/target-digest token, independent of canonical commit position.
- `PermissionEpoch`: I-owned policy-domain freshness/revocation token.
- `ProducerRegistrationHighWater`: D-owned producer ledger position, distinct from all above.
- `ContextVersion`: G-owned context version, not a retrieval or canonical cursor.

F never casts, increments, numerically compares, synthesizes or substitutes tokens across namespaces. A multi-partition IndexWatermark is a vector, never a fabricated global maximum. A watermark proves only contiguous projection accounting, not target absence, Forget suppression, cache purge or completion.

### 5.2 Scope-before-candidate retrieval

Authenticate the trusted principal and resolve I authorization, exact ScopeRefs, purpose, environment and current PermissionEpoch before candidate generation. Bind trusted scope predicates inside each backend boundary before ANN traversal results, lexical hits, structured rows, temporal results, entity matches or graph expansion can enter F's candidate buffer. Graph traversal authorizes each edge and target before enqueue/expansion at every hop. Evidence, Provenance, Entity and Relation references are independently authorized.

Global ANN top-K followed by application-side filtering is forbidden because unauthorized candidates can affect recall, counts, scores, timing, traces or reranker input. If the backend cannot guarantee safe pre-filtering, use scope-isolated partitions or a safe alternate path; otherwise that channel is unavailable for the request.

### 5.3 Canonical revalidation and retrieval stages

Before fusion, validate exact MemoryVersionRef, current D lifecycle and ForgetFence/lineage, and I permission. Only authorized canonical-valid exact versions enter fusion/reranking. Deduplicate exact Memory+Version only; preserve distinct revisions, claims and conflict alternatives. Revalidate after reranking/materialization if permission or fence could have changed. Immediately before final serialization/disclosure or G handoff, re-read current I permission and D fence. Cancellation is an optimization; final authority checkpoint is the safety proof. Unknown/incomparable order suppresses affected content.

### 5.4 IndexWatermark and freshness

Each named index/channel/partition advances only across a contiguous prefix of D CanonicalCommitCursor values for which every relevant change is accounted, including explicit no-op coverage. Delayed/failed/schema-incompatible relevant events stop advancement before the gap. Compare a partition watermark only against a required canonical cursor from the same D authority under D's semantics. If lagged, use bounded canonical read-through/delta if supported and authorized; otherwise return explicit partial/degraded/unavailable. Never infer deletion from absence or high watermark.

### 5.5 Cache and Working Set

Cache keys bind authenticated principal/issuer/security domain, exact sorted ScopeRefs and resource lineage, Environment, Agent/Task/RuntimeSession where applicable, I PermissionEpoch/decision, D ForgetFence, exact MemoryVersionRefs or index partition/generation/schema/coverage, query/filter fingerprint, retrieval config and validity. These dimensions are isolation metadata, not authorization. Every protected cache hit and materialized snippet revalidates current I/D authority and canonical lifecycle.

Working Sets contain canonical references first; materialized snippets remain protected cached content. On fence/revocation, suppress affected refs/descendants, advance local invalidation generation, cancel in-flight fills/prefetch/graph expansion/reranking/materialization, evict or quarantine cache and Working Set entries, and retain only minimal non-reconstructive deny markers allowed by I policy. A late fill must recheck D/I at its final write/visibility boundary and be discarded if stale.

### 5.6 Producer registration, rebuild and replay

Before F queues, leases, reads protected sources for, or executes any derivative-capable index rebuild/backfill/replay/materialization, F registers the producer class/work with D and receives durable registration evidence. Stable work ID/digest and source/ancestor lineage survive retry. Lease expiry, queue deletion, replay, rebuild or cache warming cannot escape D's producer barrier. Consume only owner-confirmed E Published artifacts and D canonical events. Rebuild begins with current D fence and I permission, quarantines old snapshots until control-ledger reconciliation, and rechecks current authority per batch and before publication. No pre-fence snapshot or delayed event may resurrect a forgotten target/descendant.

### 5.7 Reconnect and G handoff

Reconnect is a fresh auth boundary: authenticate current session, obtain current I PermissionEpoch and D fence, reconcile F invalidation checkpoints and G's current target state, suppress/clear stale Working Set and in-flight fills, then restore only current authorized refs. Never restore old snapshot first and clean later. ActivationRecommendation is read-only and advisory; G alone commits ContextVersion and Applied state.

## 6. Security Baseline

- Scope and permission filtering occurs before any candidate, count, score, trace, cache hit or reranker input can disclose protected existence.
- Authorize Memory, Entity, Relation, Evidence, Provenance and source dereference independently.
- Revalidate I authorization/PermissionEpoch and D fence/lineage at candidate admission, protected dereference, cache hit/fill/write, final materialization and final return.
- Fail closed for stale, missing, gapped, unavailable or incomparable authority evidence.
- Do not expose unauthorized IDs, counts, scores, snippets or existence through errors/telemetry.
- Treat retrieved Memory, Evidence, summaries and tool outputs as untrusted data, not instructions.
- Do not log protected source content, credentials or sensitive query payloads in ordinary metrics.

## 7. Module Redlines

1. No unauthorized or cross-Scope record may enter candidate buffers, fusion, reranking, counts, traces, cache response or Working Set.
2. Never perform global ANN top-K then post-filter.
3. Canonical state and D ForgetFence override index/cache/Working Set/recommendation state.
4. IndexWatermark is not CanonicalCommitCursor, ForgetFenceCursor, PermissionEpoch, ProducerRegistrationHighWater or proof of absence/deletion.
5. F-local suppression is not D CanonicalSuppressionComplete or I Global Forget.
6. Final return/handoff must revalidate current I permission and D fence; cancellation alone is insufficient.
7. Cache key dimensions never replace authorization; every hit revalidates.
8. Invalidation notification loss cannot be interpreted as no change; reconcile durable authority and checkpoint gaps.
9. Rebuild/backfill/replay/reconnect/cache warming cannot resurrect forgotten content.
10. F cannot write Canonical Memory, publish E artifacts, mutate G Context, decide I authorization or claim C final inference inclusion.
11. Unknown authority state never defaults to ALLOW or stale local token.
12. No implementation/test/benchmark claim without executable evidence.

## 8. Forbidden Cross-module Actions

- D: F consumes canonical/fence/lineage authority; it cannot mint or mutate canonical state or D completion.
- E: F consumes only E/Storage-confirmed publication events; cannot publish compiler derivatives or treat E local state as Published.
- G: F emits candidates/recommendations only; cannot mutate ContextVersion, delivery or Applied.
- I: F consumes authorization/PermissionEpoch and policy outputs; cannot grant permission, mint epochs or define Global Forget.
- H/C: F consumes authenticated/transport and inference-boundary evidence; cannot redefine BMCP or claim final request inclusion.
- Storage: F cannot certify atomic visibility, prepared transactions or physical deletion.

## 9. Dependency Contracts

| Dependency | Provider | Required contract | Current status |
|---|---|---|---|
| Canonical identity/version/lifecycle/cursor/fence | D | Exact typed reads, current fence/lineage, canonical authority | Domain semantics DECIDED; APIs/implementation not verified |
| Compiler artifacts and publication events | E + Storage | Only durable Published receipts and replayable canonical events | Contract consumed; gate implementation NOT VERIFIED |
| Permission/Scope/PermissionEpoch | I | Current per-resource authorization and revocation freshness | Policy authority external; implementation NOT VERIFIED |
| Typed Actor/Scope refs | B | Stable typed identities and applicability | Owner confirmation required where open |
| Context target/Applied | G | Read-only current ContextVersion and handoff contract | G-owned |
| Adapter reconnect/clear | H | Authenticated current session and opaque clear evidence | H-owned |
| Inference final boundary | C | Final submission ordering and data-only memory semantics | C-owned |

## 10. Conformance Requirements

All existing F-RT-01..13 and joint CFG-01..20 / PI-01..08 remain SPECIFIED / NOT RUN until executable evidence exists. Required coverage:
- Scope predicate is enforced inside every backend before candidate emission.
- Unauthorized entity/edge/target/evidence denied independently.
- PermissionEpoch changes during retrieval and during final materialization.
- ForgetFence advances after candidate generation but before final return.
- Invalidation message lost; read-time authority check suppresses and checkpoint replay repairs.
- Cache hit under old PermissionEpoch or advanced fence is suppressed.
- Late cache fill/prefetch/reranker result after invalidation is discarded.
- IndexWatermark gap, lag and schema mismatch cannot advance or imply deletion.
- Rebuild/backfill/replay from pre-fence snapshot cannot publish forgotten source/descendant.
- F work registration precedes rebuild admission and remains in D barrier through retry/DLQ.
- Reconnect cannot restore old Working Set before current D/I/G reconciliation.
- G recommendation remains non-mutating and is not Applied.
- Final return checkpoint suppresses on unknown or incomparable D/I order.

## 11. Acceptance Criteria

F G0 proposal is acceptable only when:
1. All 14 required sections are present and ownership boundaries explicit.
2. Cursor vector and IndexWatermark mapping match D's typed cursor semantics.
3. Scope-before-candidate and final return authorization/fence gates are mandatory.
4. Cache, Working Set, in-flight work and rebuild/replay/reconnect have explicit suppression behavior.
5. D registration is required for derivative-capable F work.
6. Tests and implementation claims are accurately labelled NOT RUN/NOT VERIFIED where appropriate.
7. F Owner reviews and explicitly accepts an exact version; this proposal itself remains PROPOSED.

## 12. Change Authority

F alone changes retrieval planning, candidate/ranking/fusion, index projection implementation, IndexWatermark, cache, Working Set, in-flight retrieval and F-local invalidation. D alone changes canonical and Forget authority; E alone changes compiler lifecycle and artifact publication; I alone changes authorization/PermissionEpoch/global policy; G owns Context; H owns BMCP/Adapter; C owns final inference boundary. Cross-owner contracts require exact-version acceptance by affected Owners.

## 13. Open Decisions

- D/F callable canonical read/fence validation API and linearizable final-return ordering evidence.
- D producer class/work registration API and F rebuild/replay producer-class inventory.
- E/Storage publication receipt/event schema and replay retention.
- I PermissionEpoch currentness, per-resource authorization and service/continuity principal behavior.
- B typed Scope/Actor identity mapping and cross-scope/environment grants.
- G Context target lookup/handoff and Applied separation.
- H reconnect/clear ACK and session-generation wire contract.
- ANN backend pre-filter guarantees, index partition granularity, canonical read-through API.
- Ranking/fusion model, calibrated thresholds, latency, memory/cache and graph fan-out budgets (TO_VALIDATE).

## 14. Explicit Non-Claims

This proposal is architecture baseline only. It does not claim retrieval/index/cache/Working Set/in-flight invalidation implementation, backend pre-filter proof, cancellation correctness, cache physical purge, rebuild/replay safety tests, reconnect tests, ranking quality, performance benchmarks, production readiness, D canonical suppression completion, G Applied, H Adapter purge, I Global Forget completion or physical erasure. F-RT-01..13 and CFG/PI suites remain SPECIFIED / NOT RUN unless separately evidenced.

## Evidence

- F branch starting HEAD: `6cdc23f0835ea9576867f7cd1ac145e57f598c4b`
- `05-memory-runtime/retrieval-engine.md` Blob: `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af`
- `05-memory-runtime/phase-3.5-forget-suppression-and-cursor-consumption.md` Blob: `99f950f9fabe97969b5ad580c9c80e52930a1423`
- `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md` Blob: `ce59252dbbdc5d10d016704797e9ba12d5a941bd`
- D canonical cursor contract: `03-memory-brain/commit-cursor-semantics.md` Blob `4688a0ca487bf4d853c7f0220408abe8d743d159`
- D exact JF-10 v2 decision: D branch HEAD `1460fbd17ee38ea4044dc6c75cfe49039c7fc585`
