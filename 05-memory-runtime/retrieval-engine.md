---
document_metadata:
  domain: memory-runtime
  role: design-specification
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
        - "14-ai-development/work-items/AID-2026-113/manifest.yaml"
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
    canonical_scope: "Memory Runtime design specification: retrieval-engine"
    canonical_scope_id: "memory-runtime/retrieval-engine"
    canonical_scope_keywords:
      - "recall"
      - "routing"
      - "fusion"
      - "ranking"
      - "completeness"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/05-memory-runtime/retrieval-engine.md"
    zh-CN: "docs/zh-CN/05-memory-runtime/retrieval-engine.md"
---
# Memory Retrieval Engine

**Owner:** Session F — MR-01  
**Status:** DECIDED safety semantics; CANDIDATE routing/fusion; TO_VALIDATE scoring and latency.  
**Phase 3.5 contract note:** D/E/I/G/H/C/B candidate contracts are present on their owner branches and were re-read for this reprocessing. F consumes their typed semantics without freezing cross-module schemas or claiming implementation conformance.

## 1. Purpose
Retrieve authorized, current, evidence-bearing Memory candidates from heterogeneous representations. Retrieval is not synonymous with vector similarity and does not itself activate Context.

## 2. Scope
Includes query interpretation, channel routing, scope-constrained candidate generation, canonical revalidation, hybrid fusion, deduplication, evidence-aware ranking, bounded graph expansion and completeness reporting. Excludes canonical persistence/lifecycle, index construction/publication, conflict adjudication, Context editing and Agent planning.

## 3. Responsibilities / Non-Responsibilities
Runtime owns execution plan and candidate response. D owns Memory/Version/Claim/Entity/Relation/Evidence identity and canonical status. E owns compilation, canonical commit publication and index projections. I owns identity/authorization. Runtime cannot infer authorization from index metadata or resolve disputed claims.

## 4. Inputs / Outputs
RecallQuery: request/schema IDs, trusted principal, purpose, query text and structured predicates, required scopes/environment/task/session, time window/mode, entity refs/mentions, relation constraints, channel hints, consistency fence, result/candidate/evidence budgets, deadline/cancellation and runtime config version.

RetrievalResult: result/request IDs, candidate refs, completeness, omissions, freshness by channel, canonical fence, policy epoch, timings and warnings. CandidateRef: memory_id, memory_version_id, claim_refs, match_channels, per-channel features, rank explanation, lifecycle/epistemic/validity, provenance refs and evidence summary.

## 5. Data Model and Channel Semantics

| Channel | Best for | Source | Mandatory guard |
|---|---|---|---|
| Structured field | exact IDs, types, lifecycle, scope, validity, tags | canonical/structured index | authorized scope predicate before result materialization |
| Entity | canonical entity IDs, aliases, identity-qualified mentions | entity projection/resolver | entity, alias and target Memory independently scoped |
| Full text | names, rare terms, exact phrases | inverted index | scope/permission pre-filter in controlled query plan |
| Vector ANN | paraphrase and semantic similarity | embedding projection | filter-aware ANN or per-scope partition; never global top-k then filter |
| Graph/relation | typed relationships and neighborhoods | relation projection | authorize every edge and target at every hop |
| Temporal | valid-time, event-time, recency and interval overlap | temporal index/canonical fields | scope predicate precedes interval candidate exposure |
| Provenance/evidence | support/refutation, lineage and locators | canonical provenance/evidence | independently authorize every Evidence/source dereference |

### Query interpretation
Normalize syntax; extract explicit filters; resolve time expressions to bounded intervals; resolve entity mentions through authorized lookup; detect relation/provenance needs; classify intent. Query text is data, not scheduler or authorization instructions. Ambiguous entity identity remains ambiguous; never silently merge.

## 6. Scope-before-Candidate — INT-P0-02
**DECIDED hard invariant.** No unauthorized record may become a candidate consumed by fusion, reranking, counts or activation.

Execution:
1. Authenticate principal and resolve authoritative Scope/Permission envelope with I.
2. Compile trusted scope predicate from resolved scopes and policy epoch. Raw caller filters cannot grant access.
3. Bind predicate inside each backend query boundary before ANN traversal result emission, lexical hit materialization, structured scan output, temporal selection or entity resolution output.
4. Graph traversal filters edge visibility before expansion and authorizes each target before enqueueing; repeat each hop.
5. Only authorized candidate IDs cross backend adapter boundary into Runtime candidate buffer.
6. Canonical revalidation repeats authorization and verifies lifecycle/Forget/version before ranking.
7. Revalidate policy/Forget epoch before cache return and final serialization.

Prohibited: global ANN top-K followed by application-side filtering. This can omit authorized neighbors and leak via counts, timing, scores, traces or reranker input.

If ANN cannot guarantee pre-filtering, use physically partitioned per-scope indexes or a safe scoped exact/alternate path. If neither is guaranteed, ANN is unavailable for that request. Never silently post-filter.

## 7. Candidate Generation and Routing
Exact ID/structured constraints -> structured. Entity IDs/mentions -> entity + structured. Quoted/rare terms -> full text. Paraphrase -> ANN. Typed relation/path -> graph. When/after/before/during/currently -> temporal. Why/source/proof -> provenance/evidence. Mixed intent -> bounded hybrid.

Optional query rewriting via local model is CANDIDATE, never required, never used to derive Scope, and its output is untrusted. Default route has no LLM dependency.

## 8. Fusion, Deduplication and Ranking
Canonicalize authorized results to (memory_id, memory_version_id), retaining channel features. Deduplicate exact version refs only; do not collapse distinct versions, claims or conflict alternatives. Candidate fusion may use Reciprocal Rank Fusion or calibrated feature fusion (CANDIDATE); select by offline evaluation. Raw channel scores are not assumed comparable.

Evidence-aware ranking retains positive/negative/qualifying roles, source diversity/common ancestry, trust labels, epistemic status, conflict membership, lifecycle, valid-time, provenance completeness, age/freshness, channel features and uncertainty. Ranking never upgrades Reported/Inferred/Disputed to Verified. Retracted/Forgotten objects are suppressed by canonical authority. Superseded versions appear only for explicit historical/conflict queries and are labelled.

## 9. Early Stop and Completeness
Early stop when deadline/budget reached, required-channel sufficiency achieved, or marginal gain below benchmarked threshold. Thresholds TO_VALIDATE. Filling top-k is not proof of completeness.

Completeness enum CANDIDATE: complete, partial, degraded, empty_complete, unavailable. Include omitted channels, reasons, channel watermarks, candidate-budget exhaustion, evidence truncation and cancellation. Unauthorized matches are never counted or disclosed as omissions.

## 10. Scope / Permission
Scope filtering is mandatory inside each candidate-producing adapter. Permission applies independently to Memory, Entity, Relation, Evidence, Provenance and source payload. Query/index caches cannot bypass authorization. Denial does not disclose protected IDs, counts, scores or existence.

## 11. Version / Freshness and AR-004
Canonical Store is authority; indexes are rebuildable projections. E should publish committed events with interpretable generation/watermark per partition; exact format OPEN pending E/I.

For required canonical snapshot/read position N: compare only the same partition's IndexWatermark.applied_through CanonicalCommitCursor with N using D's same-authority cursor semantics. If the watermark covers N, the partition may satisfy projection freshness subject to canonical/lifecycle/Scope/Permission/Forget revalidation. If it lags or has a gap, use a D-supported bounded canonical read-through/delta, wait within deadline, or return explicitly partial/degraded/unavailable. Never compare IndexWatermarks across partitions as one scalar, and never treat any watermark as Forget suppression/completion evidence.

On disagreement, canonical status/version/Forget wins. Stale/orphan index hits are suppressed and queued for repair. Missing index entries may cause omission only when marked partial/stale under requested consistency. Rebuild replays canonical committed events and excludes Forgotten/retracted/retention-ineligible objects according to current authority.

## 12. Cache Semantics
Query cache key includes principal, normalized scope set, environment, permission epoch, Forget epoch, query fingerprint, retrieval config and index watermark. Cached payloads are revalidated against canonical version/lifecycle and current auth. Internal ANN/lexical caches must be partitioned so unauthorized records cannot affect observable output. Invalidate on commit, version/lifecycle change, Forget, scope/grant change, environment closure and generation advance.

## 13. Failure Handling
Channel failures isolated; retry idempotent reads only within budget. Stale hits dropped; never fall back to unscoped query. Graph timeout returns bounded partial paths. Evidence unavailable returns reference/status. If canonical status is unavailable, no Forget-safe completeness claim: fail closed or return unavailable under strict safety mode.

## 14. Performance Budget
Bound channels, per-channel candidates, total candidate buffer, graph depth/fan-out, canonical revalidation count, evidence refs/bytes, reranker input and wall-clock. Numeric values TO_VALIDATE. CPU for parsing/fusion/graph; RAM for bounded buffers/cache; disk for structured/lexical/temporal indexes; GPU optional for embedding/reranking and never required for default Recall.

## 15. Observability
Per-channel latency, authorized candidate counts, canonical suppression, stale generation, graph nodes/edges, duplicate rate, evidence bytes, fusion latency, completeness reasons and denials. No unauthorized hit counts or raw sensitive query in ordinary logs.

## 16. Interfaces
D: canonical get/batch-get by ID + exact version; entity/relation/provenance/evidence reads; lifecycle/validity/current Forget state. E: index adapters, publication generation/watermark, change events, replay/rebuild cursor. I: principal/scope resolution, per-resource auth, permission epoch, revocation/Forget fence. G: immutable candidate/evidence/recommendation envelope, no Context mutation. Every interface requires schema version, correlation, policy epoch, scopes, typed error, freshness and partial semantics.

## 17. Test Scenarios
Backend tests assert scope predicate bound before ANN candidate IDs leave backend; same for full-text/structured/temporal. Graph edge/target denied independently. Reranker receives only authorized candidates. Counts/errors reveal no forbidden existence. Test canonical/index race, delayed publication, stale watermark, replay/rebuild, stricter Evidence scope, cache hit after revocation/Forget, dedup same version but preserve conflicts, and accurate partial result.

## 18. Dependencies and Open Questions
D canonical schema/lifecycle; E index/watermark; I permission/Forget authority; G output envelope; H request/auth envelope. OPEN: ANN true pre-filter semantics, watermark granularity, canonical delta API, Claim revision identity (INT-P1-02), Provenance graph constraints (INT-P1-06). TO_VALIDATE: RRF vs calibrated fusion, ranking quality, graph budgets, scoped ANN recall/latency and hardware capacity.


## Phase 3.5 — Typed Cursor and Forget Suppression Addendum (normative supplement)

The detailed owner/consumer contract is in [Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract](phase-3.5-forget-suppression-and-cursor-consumption.md). This supplement supersedes any earlier provisional wording in this file where the two differ.

### Typed cursor discipline

F consumes and stores these as distinct owner-issued types: D `CanonicalCommitCursor` (one global sequence per Brain authority), D `AggregateRevision` (per aggregate), D `LifecycleEventCursor` (per Memory), F `IndexWatermark` (per index/channel partition, applied through a D CanonicalCommitCursor), D `ForgetFenceGeneration/ForgetFenceCursor`, and I `PermissionEpoch`. G `ContextVersion` and H/C delivery/capability/request identifiers are additional independent namespaces.

F never casts, increments, numerically compares or substitutes these tokens. Same-authority CanonicalCommitCursor continuity is interpreted only under D semantics; AggregateRevision and LifecycleEventCursor remain locally scoped. IndexWatermark is a contiguous freshness/completeness prefix for one partition only. It is not target-absence evidence, Forget suppression, cache purge or global Forget completion.

### Suppression checkpoints

| Retrieval stage | Mandatory F gate |
|---|---|
| Candidate Generation | Resolve authenticated Principal, trusted ScopeRefs, current I PermissionEpoch and D fence; bind Scope predicate inside every backend before candidate emission |
| Index Lookup | Query scoped partition; validate its own watermark/coverage/schema; exact version refs only; never global top-K then post-filter |
| Canonical Revalidation | Resolve exact version, lifecycle, source lineage and latest applicable D fence; authorize Memory, Entity, Relation, Evidence and Provenance independently |
| Fusion | Admit only authorized, canonical-valid candidates; dedupe exact Memory+Version only; preserve conflicts and distinct versions |
| Freshness | Evaluate each partition watermark independently against required CanonicalCommitCursor; lag means read-through/wait/partial, not Forget failure/success |
| Reranking | Only validated candidates/evidence enter reranker; recheck if permission/fence changed during ranking |
| Result Materialization | Reauthorize exact fields and Evidence dereferences; discard affected materialization if fence/revocation advances |
| Final Return / G Handoff | Revalidate current I permission and D fence immediately before serialization/disclosure; cancel/drop affected results or fail closed when ordering is unknown |

Fence/revocation notifications cancel affected in-flight work and cache fills, but cancellation is not the safety proof. The final return/handoff recheck is mandatory. If the request cannot establish current authority state, it must not disclose affected content.

ActivationRecommendation remains a proposal to G. It does not mutate ContextVersion, constitute delivery, or prove Applied.


## Phase 3.5 reprocessing — current dependency alignment

This section supersedes stale dependency-presence and provisional cursor wording above where inconsistent.

- D's current owner decision is one globally ordered `CanonicalCommitCursor` per BrainAuthority, with independent per-aggregate `AggregateRevision`, per-Memory `LifecycleEventCursor`, and separate `ForgetFenceCursor/Generation`.
- D's `ProducerRegistrationSequence/HighWater` is a further distinct ledger position. It is not a canonical cursor, Forget generation, PermissionEpoch or IndexWatermark.
- F's `IndexWatermark` is a vector of per-index/per-channel/per-partition contiguous applied-through CanonicalCommitCursor positions, with explicit coverage/schema versions and gap state.
- I's `PermissionEpoch` is opaque within its policy-domain/issuer. F uses I's currentness/authorization operation; it does not compare it with D tokens.
- G's `ContextVersion` is per Context. Retrieval and ActivationRecommendation remain read-only with respect to G.
- Candidate generation must bind trusted Scope and Permission filters inside each backend before candidate emission. Index hits remain exact refs until canonical version, lineage, lifecycle, current D fence and independent I authorization checks succeed.
- The final return/handoff checkpoint is mandatory even after cancellation or earlier validation. If current authority ordering cannot be established, suppress affected content.

Current source snapshot: D `da8e5882d0b238d765d00b2225b79eea45a483b1`; E `c2f14408ba62447c11172d65b93a279fef96d175`; I `5591ad3620ec3f5d74194bd79556dcf3e25bea07`; G `3d2c065be863bc1d349faaeece6f6eaa0047abae`; H `1ee65928f123d92a4758b0de09bc8d6df1e46253`; C `35de58ddc93c5f1e554596cdfc430cd6c392d355`; B `66adf6bdcf5ec69a146fe75afe20ce3b85af8448`.
