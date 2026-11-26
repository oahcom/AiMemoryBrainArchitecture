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
      last_verification_note: "Mirror body retained unchanged; semantic parity checked at heading and cross-reference level only."
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
    canonical_status: Non-Canonical
    canonical_scope: "Memory Runtime design specification: runtime-overview"
    canonical_scope_id: "memory-runtime/runtime-overview"
    canonical_scope_keywords:
      - "runtime-session"
      - "retrieval"
      - "activation"
      - "scheduling"
      - "working-set"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "05-memory-runtime/runtime-overview.md"
    en: null
    zh-CN: "docs/zh-CN/05-memory-runtime/runtime-overview.md"
---
# Memory Runtime Overview

**Owner:** Session F — Memory Runtime  
**Status:** DECIDED for authority/safety boundaries; CANDIDATE for topology; TO_VALIDATE for numeric budgets.  
**Baseline:** main at e443b23f8a179ad12c163722ad93bc646fd3a80a.  
**Phase 3.5 dependency review:** D/E/I/G/H/C/B owner-branch contracts are present and were re-read at the exact heads recorded in `phase-3.5-forget-suppression-and-cursor-consumption.md`（未提交，见 [GAP-01](../../governance/documentation-gaps.md)）. F's consumer semantics are DECIDED; callable cross-module schemas, Storage realization and runtime conformance remain OPEN. No wire schema is frozen by this document.

## 1. Purpose
Memory Runtime is the Brain's bounded online read/activation execution layer. It interprets Recall, authorizes scope, routes retrieval across canonical and derived representations, produces evidence-bearing candidates, recommends activation, and maintains disposable Working Sets/caches. It is not an Agent Runtime, planner, tool executor, canonical store, compiler, or Context Version authority. Default Recall is deterministic and does not synchronously invoke a large LLM.

## 2. Scope
Owns Runtime Session lifecycle, request-local execution state, query interpretation/routing, scope-filtered retrieval, candidate fusion/dedup/ranking, completeness/freshness semantics, activation recommendations, bounded Working Sets/caches, scheduling/admission/cancellation and read-path freshness checks.

Does not own canonical Memory/Claim/Entity/Relation identity, versions, lifecycle or authoritative Forget state (D); compilation, canonical commit or index publication (E); ContextEntry mutation or Context Version (G); permission policy/global retention/audit (I); Agent planning, action selection, tool authorization or prompt policy.

## 3. Responsibilities / Non-Responsibilities
Runtime chooses which authorized memories are useful candidates and recommends activation. It cannot decide whether a Claim is true, settle a Conflict Set, promote a Claim, or declare a memory forgotten. It preserves disputed/retracted/superseded state for G. Canonical Memory is authoritative; indexes, caches and Working Sets are disposable projections. Results reference exact canonical Memory Versions and do not create memories.

## 4. Inputs / Outputs
Inputs: authenticated Principal and resolved Scope context from I/H; Recall request (query text/structured filters, purpose, target context hint, task/session/environment refs, result/evidence budgets, consistency requirement, deadline/cancellation); Agent telemetry as untrusted relevance signals; D canonical metadata and authorized evidence; E commit events, index publication and watermarks; policy/configuration version and resource limits.

Outputs to G/caller: RetrievalResult (request ID, candidates, completeness, freshness vector, warnings/timing); CandidateMemory (Memory ID + immutable Version ID, canonical reference, match channels, score features, lifecycle/epistemic state, validity, provenance refs and evidence summary); ActivationRecommendation (include/defer/exclude, reason codes, urgency/expiry hints and budget estimate); explicit uncertainty/conflict/retraction/evidence-unavailable markers. No output creates or advances Context Version.

## 5. Data Model
RuntimeSession binds opaque session ID, authenticated principal, Agent/instance, user/project/agent/task/session/environment scopes, permission epoch/policy version, generation/cancellation state, bounded Working Set, quotas and expiry. It is not Agent planning state or Memory Context.

RecallRequest is immutable after admission. RetrievalResult is an immutable response snapshot. Candidate references identify exact Memory Version. WorkingSetEntry is a bounded projection/reference with invalidation metadata.

## 6. Routing / Scheduling
Classify as structured lookup, entity-centric, lexical, semantic, temporal, relation traversal, provenance expansion or hybrid. Select deterministic channels from query features and explicit filters. Parallelize within request budgets. Bound graph/evidence work. No LLM required on default path; optional query rewrite is CANDIDATE, disabled by default, never trusted for authorization.

## 7. Request Sequence
    Agent/Adapter -> Runtime: Recall(query, scopes, purpose, budgets)
    Runtime -> I: authenticate, resolve scopes, authorize
    I -> Runtime: principal + policy/permission epoch
    Runtime -> D: current canonical/Forget fence
    Runtime -> E: scope-constrained channel queries
    E -> Runtime: authorized candidate refs + index watermarks
    Runtime -> D/I: revalidate candidate version, lifecycle, Forget and permissions
    Runtime: fuse -> deduplicate -> rank -> completeness -> activation
    Runtime -> Agent/Adapter: RetrievalResult + ActivationRecommendation
    Agent/Adapter -> G: optional proposal; G alone decides Context Version

Decision flow: authenticate/authorize -> resolve trusted scopes -> apply Scope predicate before each candidate generator -> parallel channels -> canonical/Forget validation -> fusion/ranking -> activation -> explicit completeness/freshness response.

## 8. Invariants
1. **Scope-before-Candidate (INT-P0-02):** no unauthorized object enters candidate collections, fusion, reranker, counts, cache response or Working Set.
2. Every graph edge and target node is independently authorized before traversal/retention.
3. Canonical status and Forget fences override all derived projections.
4. Permission revocation invalidates or blocks cached and in-flight results before disclosure.
5. Memory content is untrusted data, never executable instructions (INT-P0-04).
6. Retrieval Result is not ContextEntry and owns no Context Version (INT-P1-01).
7. Conflict, Disputed, Retracted and Superseded states are preserved; Runtime does not adjudicate (INT-P1-02).
8. Provenance and Evidence are separately authorized and budgeted (INT-P1-06).
9. Partial results are never silently represented as complete.
10. Working Set/cache/index are never canonical authority.

## 9. Scope / Permission
Scope is namespace/applicability; Permission is operation authorization. Both are required. Trusted identity/scope is resolved by I/H, not inferred from query text, display names or Agent-supplied labels. Check at ingress, before each channel, each graph edge/target, Evidence dereference, cache return, serialization and G handoff if epoch changed. Authorization service failure is fail-closed.

## 10. Version / Freshness
Each candidate carries Memory ID, exact Memory Version ID, canonical status/version and source generation where available. Each index channel returns watermark/generation. Freshness is per channel/candidate, not one misleading boolean.

If E publication lags canonical commit: satisfy a required fence via bounded canonical delta/read-through or wait within deadline; otherwise return explicitly partial/stale with observed and required generations. Never claim index completeness below the fence. Canonical state remains authoritative.

## 11. Cache Semantics
Cache key includes authenticated principal, normalized Scope set, environment, permission epoch/policy version, query fingerprint, retrieval config version, index generation/freshness fence and canonical/Forget epoch. Cache hits revalidate revocation/Forget and canonical version before disclosure. Sensitive evidence payloads are not cached by default.

## 12. Failure Handling
Auth/policy unavailable: fail closed. Canonical store unavailable: do not trust index-only results for lifecycle/Forget guarantees. Index unavailable: bounded safe canonical fallback or explicit partial/unavailable. Channel timeout: partial with omission. Cancellation: stop fan-out and prevent late result insertion. Version mismatch: discard/retry boundedly or mark stale. Evidence unavailable: retain reference/status, never fabricate excerpt.

## 13. Performance Budget
Budget admission, authorization, canonical validation, per-channel search, graph fan-out, fusion/ranking, evidence expansion and serialization. Bound candidate count, graph depth/fan-out, evidence bytes and wall-clock. Numeric thresholds are TO_VALIDATE on declared CPU/RAM/disk/GPU and representative corpus. No fixed P95/P99 claim.

## 14. Observability
Trace request -> auth checkpoints -> channel spans -> canonical revalidation -> fusion/rank -> activation -> G handoff. Record channel latency, authorized candidate counts, stale suppression, watermarks, partial reasons, cache hit/miss, invalidation, cancellation and saturation. Avoid raw query/evidence and high-cardinality metric labels.

## 15. Interfaces
D -> F: canonical read by ID/exact version; typed refs; lifecycle/epistemic/validity; authorized Evidence/Provenance dereference. E -> F: canonical commit event, projection publication, index watermark, Forget/retraction feed. I -> F: authenticated principal, scope resolution, permission decision/epoch, revocation and Forget fence. F -> G: RetrievalResult, CandidateMemory, ActivationRecommendation, EvidenceSummary, Completeness, Freshness, Memory Version and reason codes.

All are provisional until D/E/G/H/I review. Each needs schema version, correlation ID, auth context, typed errors, retryability, freshness and partial semantics.

## 16. Test Scenarios
Cross-user/Agent/instance/task/environment negative Recall; assert Scope predicate before ANN/lexical/graph candidate materialization; unauthorized graph target; revocation between channel completion and serialization; Forget during query; lagging watermark; disputed/retracted/superseded state; Evidence stricter than Memory; inert prompt-injection content; channel timeout/cancellation never yields false completeness.

## 17. Dependencies
D canonical schema/lifecycle; E canonical commit/index publication/watermarks; G Context contract; H authenticated protocol; I identity, Scope, Permission, revocation and Forget; storage/observability infrastructure.

## 18. Open Questions
OPEN: D canonical read/lifecycle snapshot consistency; E watermark granularity/replay ordering; I permission epoch/revocation SLA; G candidate/evidence payload; H request envelope. CANDIDATE: modular-monolith task groups. TO_VALIDATE: routing quality, channel budgets, cache benefit and local hardware limits.


## Phase 3.5 — Forget and Cursor Integration

The normative F consumer matrix, retrieval-stage suppression matrix, cache/Working Set invalidation contract, index rebuild contract and ten conformance specifications are maintained in [phase-3.5-forget-suppression-and-cursor-consumption.md](../../governance/documentation-gaps.md).

Runtime consumes D's per-authority global CanonicalCommitCursor, per-aggregate AggregateRevision, per-Memory LifecycleEventCursor and ForgetFenceGeneration as separate types; F owns per-index/per-partition IndexWatermark; I owns PermissionEpoch; G owns ContextVersion. These values are not interchangeable. IndexWatermark is only contiguous projection freshness evidence and never proves Forget completion.

Retrieval enforces Scope, current permission and latest applicable Forget Fence at candidate generation, index lookup, canonical validation, fusion, freshness, reranking, materialization and final return. Cache hits and Working Set reuse are reauthorized. Fence/revocation advancement cancels affected in-flight work; final disclosure still requires an authoritative recheck.

F's index rebuild/backfill/replay is derivative-capable work: register before admission under D's Producer Registration contract, replay a contiguous canonical commit prefix, exclude fenced lineage, and use the authoritative final publication gate. If the D/E/Storage gate is unavailable or unresolved, keep the staged generation private/quarantined.

ActivationRecommendation is advisory only. G alone decides Context mutations and ContextVersion; H/C own Adapter/final-request evidence. F does not claim Applied, global Forget completion or physical erasure.


## 19. Phase 3.5 reprocessing — runtime authority checkpoints

- Request admission binds authenticated Principal, trusted owner/applicability ScopeRefs, purpose, I PermissionEpoch (policy-domain/issuer scoped) and current D ForgetFence. Query text and payload-supplied ActorRef/ScopeRef/producer labels are not authority.
- Each candidate-producing adapter enforces Scope and permission before candidate emission. Each exact hit is canonical-revalidated for MemoryVersion, AggregateRevision where relevant, LifecycleEventCursor, source lineage, D fence coverage and independent authorization of Memory, Entity, Relation, Evidence and Provenance.
- Fusion/reranking/materialization accept only revalidated candidates. Any epoch/fence change or unverifiable ordering causes cancellation plus suppression; cancellation is not the safety proof.
- Final response serialization and G handoff perform a current D fence and I authorization checkpoint. No affected content is disclosed when current authority cannot be established.
- Freshness is a per-index/per-partition vector. Each IndexWatermark represents a contiguous prefix of D CanonicalCommitCursor for that partition and explicit coverage/schema version; a lagging partition cannot be masked by another. It never proves target absence, Forget completion or physical erasure.
- F ActivationRecommendation is immutable and advisory. G alone validates and mutates Context/ContextVersion; H/C own Adapter/final-request evidence. F never claims Applied.

Reprocessing source heads: D `da8e5882d0b238d765d00b2225b79eea45a483b1`; E `c2f14408ba62447c11172d65b93a279fef96d175`; I `5591ad3620ec3f5d74194bd79556dcf3e25bea07`; G `3d2c065be863bc1d349faaeece6f6eaa0047abae`; H `1ee65928f123d92a4758b0de09bc8d6df1e46253`; C `35de58ddc93c5f1e554596cdfc430cd6c392d355`; B `66adf6bdcf5ec69a146fe75afe20ce3b85af8448`.
