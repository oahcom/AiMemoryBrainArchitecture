# Memory Resource Manager — Candidate Contract

**Status: CANDIDATE / NOT APPROVED.** This contract is a research proposal. It does not modify F/G contracts or authorize production implementation.

## 1. Authority model

Resource Manager (RM) is a coordination/control-plane component, not a memory authority.

- F owns retrieval, ranking/fusion, ActivationRecommendation, Runtime Session, Working Set and F cache.
- G owns Context membership, ordering, sufficiency, ContextVersion, ChangeSet, compaction and delivery intent.
- D owns canonical Memory identity/version/lifecycle and ForgetFence.
- I owns authorization, PermissionEpoch and governance policy.
- E owns canonical publication/index projection semantics.
- H/C own Adapter and final inference boundary evidence.

RM cannot mint, reinterpret or override any of these decisions.

## 2. MemoryResourceRequest

Required fields:
- request_id, idempotency_key, schema_version;
- principal_ref, policy_domain_ref, tenant_ref;
- agent_ref, agent_instance_ref, session_ref, task_ref, environment_ref (typed opaque refs; requiredness resolved by B/I);
- purpose and resource_class (interactive_recall, context_plan, background_refresh, maintenance);
- requested vector: tokens, bytes, candidate_count, evidence_bytes, graph_nodes/fanout, CPU units, memory bytes, I/O units, max_parallelism;
- latency_deadline and cancellation_ref;
- task_importance and service_class (untrusted hints until policy maps them);
- freshness_requirement and required canonical/index fences;
- access_scope_ref and authorization/Forget epoch references (proof references only; RM must revalidate);
- minimum reservation, maximum cap, borrowable flag, estimated cost and cost-model version.

## 3. ResourceDecision

Fields:
- decision_id, request_id, policy_version, decision_timestamp;
- outcome: admitted | admitted_with_reduction | deferred | rejected | cancelled | expired;
- reservation_id, granted resource vector, queue position/class;
- fairness/aging explanation and competing quota bucket IDs (opaque);
- approved degradation steps and typed omissions;
- owner handoff plan (F retrieval budget, G Context budget, delivery budget);
- decision trace hash/reference, expiry and revalidation points.

No outcome means authorization. No decision means a protected read is denied/deferred, not silently allowed.

## 4. Resource ledger and scheduler

- Resource ledger tracks reservations/usage by principal, task, session, resource class and time window.
- Use weighted fair queueing or deficit round robin across principals first, then tasks within principal; reserve a small guaranteed floor for interactive work and each admitted active task.
- Background refresh and maintenance use separate low-priority pools and may be preempted.
- Unused reservations may be borrowed only with lease/expiry and reclaim at safe stage boundaries.
- Aging prevents starvation; deadline-aware scheduling orders eligible work but cannot bypass quotas or hard gates.
- Per-task max cap prevents one task from monopolizing all capacity.
- If demand exceeds capacity, return explicit deferred/rejected/partial outcome with retry hint; never claim full coverage.
- Reservations are for compute/capacity, not exclusive ownership of a memory item.

## 5. Hard admission gates (non-negotiable)

Before candidate ranking, cache hit, compaction, Context publication or delivery:
1. authenticated Principal and resolved typed Scope;
2. current I authorization / PermissionEpoch;
3. current D ForgetFence and complete applicable lineage;
4. canonical Memory/Version lifecycle, temporal validity and source access;
5. classification and evidence/provenance access;
6. environment/task binding and policy-domain consistency.

Any unknown, stale, missing or unavailable authority state fails closed for protected data. RM only carries opaque references and asks owners to validate. Priority, task value, relevance, budget availability and cache residency are never substitutes.

## 6. Allocation stages

1. Admit request and reserve bounded execution resources.
2. F retrieves scoped candidates; returns channel completeness and per-index/per-partition watermarks.
3. F activation evaluates eligible candidate suitability and emits reasoned proposals.
4. G revalidates candidate identity/version and current D/I authority; builds task requirement profile.
5. RM arbitrates shared CPU/RAM/token/latency envelope and fairness reservation; G remains final Context allocator and sufficiency authority.
6. G commits a versioned Context ChangeSet under its existing commit and D publication gates.
7. H applies at inference boundary; G/C/H evidence semantics remain unchanged.
8. Release/expire reservations; record actual usage and prediction error.

## 7. Failure behavior

- RM unavailable: no protected operation is admitted based on stale RM grants. Optional deterministic static per-principal caps may permit degraded operation only if explicitly configured and still revalidated by F/G/I/D.
- RM ledger unavailable/corrupt: reject/defer new allocations; do not infer capacity.
- Stale request/lease: cancel and reconcile; no late result may populate Working Set/cache or publish Context without current owner checks.
- Cancellation: propagate to child retrieval/evidence tasks; preserve stable request identity and separate attempt identity.
- Over-budget mandatory Context: G reports Insufficient; RM cannot silently truncate mandatory coverage.
- Partial index/authority outage: report typed partial/unknown; never imply completeness.

## 8. Observability and conformance

Metrics: queue wait, admitted/deferred/rejected counts, reservation vs actual vector, per-principal/task share, starvation age, p50/p95/p99 stage latency, budget utilization, candidate/Context coverage, omissions, stale/Forget suppression, cache hit/miss and fairness Jain index.

Conformance: request identity and idempotency; quota isolation; starvation/aging; cancellation; borrowing/reclaim; authority outage fail-closed; Forget during retrieval; permission epoch change; context insufficiency; no cross-scope leakage; restore with stale lease; deterministic replay of allocation ledger.

## 9. Explicit exclusions

RM does not store memory content, own a global Residency state machine, perform cache eviction, alter Canonical Memory, decide retention/Forget, settle conflicts, construct prompts, or authorize Agent actions.
