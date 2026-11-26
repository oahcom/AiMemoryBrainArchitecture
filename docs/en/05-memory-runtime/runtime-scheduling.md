---
document_metadata:
  domain: memory-runtime
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-082"
        - "source branch: session-f-memory-runtime"
        - "source commit: 1908ce4d233b20f7cafd00cb679affd01bd15174"
        - "original source blob: ca35d8cddd012c1ff067328ee22177f57c40ae36"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Exact source Blob pinned; EN mirror body retained; semantic review pending."
    usage_status: Active
    modification_status: Modified
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - bilingual-mirror
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "05-memory-runtime/runtime-scheduling.md"
    en: null
    zh-CN: "docs/zh-CN/05-memory-runtime/runtime-scheduling.md"
---

# Memory Runtime Scheduling

**Owner:** Session F — MR-04  
**Status:** DECIDED safety/admission principles; CANDIDATE scheduling design; TO_VALIDATE resource budgets.

## 1. Purpose
Schedule Recall and activation work with bounded latency, resource use and isolation while preserving safety, freshness and truthful partial-result semantics.

## 2. Scope
Owns request classification, admission, retrieval routing, parallel channel execution, candidate/latency budgets, graph fan-out, early stop, deduplication, backpressure, cancellation, priorities and resource isolation. Does not schedule Agent plans/actions, compiler jobs, canonical commits or Context delivery.

## 3. Responsibilities / Non-Responsibilities
Runtime scheduler is an internal Brain execution coordinator. Agent intent/plan/observation/outcome are signals for relevance and priority, not instructions that can override Brain limits, authorization or policy. Scheduler never interprets memory text as executable control.

## 4. Inputs / Outputs
Input: authenticated RecallRequest, resolved scopes/permission epoch, query class, deadline, candidate/evidence budgets, required consistency fence, cancellation token, policy and resource configuration. Output: admitted/rejected/deferred request, execution plan, channel outcomes, completeness/omissions, resource/timing metrics.

## 5. Request Classification
CANDIDATE classes:
- P0 safety/decision-critical explicit recall;
- P1 interactive bounded recall;
- P2 background/proactive refresh;
- P3 maintenance-like cache warmup (only if separately authorized; low priority).

Priority is Brain policy-owned. Caller-supplied urgency is an untrusted hint. A priority class cannot bypass scope filters, Forget, quotas or fairness. High-impact classification may raise evidence/consistency requirements, not weaken them.

## 6. Routing / Parallel Execution
Plan channels from structured/entity/lexical/vector/graph/temporal/provenance needs. Execute independent channels concurrently under a request task group. Each channel gets scoped query predicate and local budget before it starts. Graph expansion and evidence dereference are separate child tasks with fan-out caps. Merge only after authorization and canonical revalidation. Cancellation propagates to all child tasks.

## 7. Candidate and Latency Budgets
Per request budget dimensions:
- max parallel channels;
- max candidates per channel and total candidate buffer;
- max graph depth, edge fan-out and visited nodes;
- max canonical revalidation calls;
- max Evidence refs, bytes and provenance depth;
- max reranker input;
- CPU work quota, memory bytes and wall-clock deadline.

All numeric values are TO_VALIDATE. Budget exhaustion produces typed partial result, not silent truncation. Budget reservations are acquired before fan-out to avoid unbounded speculative work.

## 8. Early Stop / Completeness
Stop when deadline expires, required-channel work completes, candidate sufficiency is met under validated criteria, marginal gain falls below validated threshold, or cancellation occurs. A top-k full list is not completeness. Response records required vs executed channels, watermarks, omitted work, budget exhaustion, truncation, cancellation and canonical fence status.

## 9. Backpressure and Admission
Use bounded queues and per-principal/per-scope concurrency limits. Under pressure:
1. reject or defer low-priority background work;
2. coalesce equivalent refreshes where key-safe;
3. preserve interactive requests within reserved capacity;
4. apply fair scheduling across principals/scopes;
5. return typed overloaded/retry-after outcome without protected metadata.
Never drop a request after reporting accepted; Recall admission is not durable Event acceptance and must not be confused with Compiler semantics.

## 10. Cancellation and Supersession
Cancellation is cooperative and propagated through channel tasks, graph traversal, evidence expansion and reranking. Late results are discarded after deadline/cancel and cannot populate Working Set/cache unless independently validated and policy permits. A newer request may supersede background refresh, but not silently cancel an explicit request. In-flight Forget/revocation fences override normal cancellation behavior: suppress result immediately.

## 11. Priority and Resource Isolation
Per-principal and per-session quotas prevent noisy-neighbor starvation. Separate interactive Recall from background refresh pools. CPU for parsing, query planning, fusion and graph traversal; RAM for bounded candidates, Working Sets and caches; disk I/O for structured/full-text/vector/temporal indexes; optional GPU for embedding inference or optional reranking only. GPU queue saturation must not block deterministic lexical/structured Recall. No GPU requirement for default path.

## 12. Scope / Permission
Admission occurs only after authenticated identity and authorization. Each channel independently enforces Scope-before-Candidate. Priority cannot broaden Scope. Queue entries carry principal, scopes, policy epoch, Forget epoch and expiry. Recheck authorization when dequeued and before final response; if policy changes, cancel or replan.

## 13. Version / Freshness
Scheduler carries requested canonical/index fence and per-channel watermarks through execution. It may wait for publication only within deadline; otherwise return partial with exact lag. Canonical/Forget status rechecked at commit-to-response boundary. Stale channels cannot be marked complete.

## 14. Cache Semantics
Scheduler can coalesce identical safe requests only when principal/scope/environment/permission/Forget epochs, query fingerprint, config and consistency fence match. Shared in-flight work must not mix authorization contexts. Cancellation of one waiter must not cancel shared work still needed by other authorized waiters; per-waiter response authorization is still required.

## 15. Failure Handling
Overload -> typed rejection/defer; channel failure -> partial; canonical/auth failure -> fail closed where safety cannot be proven; GPU failure -> deterministic non-GPU route; disk saturation -> bounded retry or partial/unavailable; cancellation -> no late response; scheduler crash -> request lost/failed, never false complete. Retry policy is bounded and read-only/idempotent.

## 16. Performance Budget
Measure admission wait, queue age, per-stage latency, parallelism, CPU time, RAM peak, disk IOPS/latency, GPU/VRAM and cancellation delay under declared concurrency/corpus/hardware. Do not set fixed P95/P99 before benchmark. TO_VALIDATE: queue limits, reserved capacity, fairness quantum, graph budgets, GPU offload value and resource envelope for 12–16 GB VRAM local systems.

## 17. Observability
Track queue depth/age by priority and scope class, rejected/deferred rate, per-channel latency, deadline misses, cancellation propagation, budget exhaustion, graph fan-out, CPU/RAM/disk/GPU saturation, partial results and noisy-neighbor throttling. IDs in traces, not metric labels. Logs exclude raw Memory/evidence content and unauthorized counts.

## 18. Interfaces
H/I provide authenticated identity, policy epoch and authorization; Retrieval Engine provides channel plan and candidate streams; Cache/Working Set provides scoped reads and invalidation; E provides index watermarks; D provides canonical fences; G receives result/completeness and recommendation. Typed outcomes must distinguish rejected, overloaded, cancelled, partial, degraded, complete and unavailable. Exact wire codes belong to H.

## 19. Test Scenarios
Burst Recall; one principal noisy-neighbor; graph fan-out adversarial input; slow vector channel while lexical succeeds; GPU offline; disk saturation; deadline/cancel mid-ANN; permission revoked while queued; Forget while running; index watermark below required fence; identical request coalescing with different scope must not share; partial result never reported complete.

## 20. Dependencies
D canonical read/fence; E index adapters/watermarks; G context requirements and budget hints; H request/cancellation envelope; I identity/permission/revocation; storage/index engine and telemetry.

## 21. Open Questions
OPEN: workload classes and SLO targets; H cancellation/error codes; I per-principal quota identity; E watermark semantics. CANDIDATE: async task groups in modular monolith, bounded per-class queues, deterministic fallback. TO_VALIDATE: scheduler policy, parallelism, queue caps, resource isolation and hardware benchmarks.


## 22. Data Model
ScheduledRequest binds request_id, authenticated principal, normalized Scope refs, environment/task/session refs, permission_epoch, Forget_epoch, request_class, deadline, cancellation state, required canonical/index fence, reserved CPU/RAM/candidate/evidence budgets and correlation_id. ChannelTask binds channel_id, scoped predicate digest, local candidate/fan-out/time budgets, source watermark, task state and outcome. SchedulerLease records admitted quota reservation, expiry and release state. These are Runtime execution records, not canonical domain objects or Agent Planning State.
