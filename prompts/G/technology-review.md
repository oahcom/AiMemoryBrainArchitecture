# Owner G — Technology Architecture Review Prompt

- Prompt ID: OWNER-G-TAR-001
- Version: 1.0
- Status: PROPOSED REVIEW PROMPT
- Task: TAR-AI-001
- Source: `reviews/technology/phase-1-a-i-technology-architecture-review-tasks.md`
- Source blob SHA: f77daebe2f85d8e32f7a1c5b2bd71650415fdaae

## Mandatory global rules

Read `prompts/global-project-developer.md`, `prompts/global-architecture-reviewer.md`, `prompts/global-bilingual-documentation.md`, `prompts/G/owner-charter.md` and GOV-DOC-001 before work. Refresh current branch heads, blueprint and all source SHAs. This prompt does not approve TAB-001 or freeze a technology.

## Common review requirements

## 3. Common review requirements — all owners

Each owner must independently assess all six dimensions below. A dimension may be marked NOT APPLICABLE only with a reason tied to the owner’s actual boundary.

### R1 — Technical requirements and workload fit
- Identify functional, non-functional, consistency, security, latency, throughput, availability, durability, and operability requirements.
- Map each requirement to a component, interface, technology capability, and verification method.
- Identify omitted requirements, assumptions, and unquantified requirements.
- Distinguish hard invariants from performance preferences.

### R2 — Component dependencies and boundaries
- Check upstream/downstream dependencies, ownership, authority, and data flow.
- Identify cyclic dependencies, duplicate authority, hidden shared state, implicit synchronous coupling, and missing interfaces.
- Verify that logical components are not incorrectly equated with crates, processes, services, or databases.
- Identify dependencies that could make optional inference, indexing, or Adapter availability block correctness-critical paths.

### R3 — Candidate technology selection
For every relevant candidate named in TAB-001:
- Assess fitness for the actual workload and contract semantics.
- Identify alternatives and comparison criteria.
- Assess ecosystem maturity, Rust integration, platform support, licensing/operations, persistence semantics, migration path, and lock-in.
- Mark each technology as recommendation, candidate, unresolved decision, or already-decided project constraint.
- State what evidence is needed before selection.

Do not approve a technology merely because it is named in the blueprint. Do not introduce a new dependency without explaining why existing candidates are insufficient.

### R4 — Resource constraints
- Review CPU, host RAM, GPU VRAM, disk, I/O, concurrency, queue, cache, index, and model assumptions relevant to the owner.
- Explicitly account for the 12–16 GB VRAM planning envelope.
- Identify peak-memory, burst, contention, backpressure, and resource-exhaustion risks.
- Give measurable sizing formulas or workload dimensions where exact numbers are unavailable.
- Separate estimates from measured data. No invented benchmarks or SLOs.

### R5 — Failure recovery and operational safety
Review process crash, host restart, partial writes, database unavailable, disk full, worker lease expiry, retries, duplicate delivery, stale replay, index rebuild, cache invalidation, model OOM/unavailable, Adapter offline/reconnect, backup restore, and upgrade/migration as relevant.

For each critical transition, state durable authority, linearization/commit point, idempotency and retry behavior, recovery source of truth, fail-open/fail-closed behavior, observability/operator evidence, and required fault-injection tests.

### R6 — Interface and compatibility
- Verify compatibility with current owner contracts and adjacent owner interfaces.
- Identify wire/schema/version/cursor/epoch/identifier mismatches.
- Distinguish transport identity from payload claims.
- Identify forward/backward compatibility and rolling-upgrade concerns.
- Do not reinterpret CanonicalCommitCursor, AggregateRevision, LifecycleEventCursor, IndexWatermark, ContextVersion, PermissionEpoch, ProducerDomainInventoryEpoch, and ForgetFenceGeneration as interchangeable.

## Project-wide constraints

## 4. Project-wide constraints to preserve

Every owner must explicitly assess the impact of these constraints:

1. Brain remains Agent- and model-independent; it does not become an Agent planner or tool executor.
2. Canonical Memory, Memory Context, and Applied Context are separate authorities/states.
3. Accepted Event, compiled Candidate, Canonical Commit, indexed representation, delivered Context, and Adapter Applied are distinct states.
4. Model output is a proposal, not Canonical Truth.
5. Scope and Permission are separate; untrusted memory/evidence/summaries are data, not instructions.
6. Durable ingress and canonical recovery cannot depend on an LLM being available.
7. Indexes and caches are derived, rebuildable, and cannot override canonical authority or Forget suppression.
8. Forget must prevent replay, recompile, late derivative publication, index rebuild, Context delivery, Adapter reconnect, and backup restore from resurrecting forgotten content.
9. D’s selected semantic decision is one globally ordered CanonicalCommitCursor per Canonical Memory Authority. Other revisions, cursors, epochs, and generations remain separate typed namespaces. Storage realization and crash recovery still require evidence.
10. D/E/Storage producer admission versus Forget fence installation, dependency registration, and publication gate remain open until a concrete atomic/linearizable operation contract and race/fault tests exist.
11. B’s Fact/Claim ADR remains ADR-BLOCKED unless a current formal governance decision is found. Do not infer approval from an owner preference.
12. H owns BMCP normative wire/protocol decisions; I owns security/governance policy; C owns Agent integration requirements and Adapter-side conformance; G owns Context version/change/delivery authority; F owns retrieval/runtime activation; D owns Canonical Memory authority; E owns compilation and staged derivative workflow.
13. TAB-001 is a candidate blueprint, not a technology freeze. Owners may accept, conditionally accept, reject, or request changes to individual recommendations without changing unrelated decision statuses.

## Owner-specific assignment

### G — Memory Context Owner
- Branch: session-g-memory-context
- Report: reviews/technology/owner-g-memory-context-technology-review.md

Review Context planning, edits, versioning, reconciliation, delivery, and budget.
- Persistence for ContextVersion, ChangeSet, ContextEntry, snapshots, deltas, delivery attempts, ACKs, and reconciliation state.
- G remains sole Context version/change authority; F retrieval recommendations and H transport cannot become Context authority.
- Optimistic concurrency/base_version, idempotent edits, ordering, compaction, expiry, replacement, remove, and full-snapshot fallback.
- Delivery queue durability, stale/superseded deliveries, Adapter offline/reconnect, capability downgrade, and exact Applied evidence.
- Token budgeting across model context windows, tokenizers, managed-region limits, and safety headroom.
- Context rendering/encoding, untrusted-data isolation, source references through compaction, deterministic reconstruction.
- Forget invalidation of entries, snapshots, deltas, pending deliveries, and reconnect state.
- Concurrent Agent sessions and independent Contexts sharing canonical memory.
- Tests for version gaps, concurrent edits, duplicate delivery, lost/stale ACK, offline Adapter, budget overflow, and Forget during delivery.

Required conclusion: Does the design preserve one authoritative Context version sequence? What is durable versus recomputable? What exact Adapter evidence permits G to mark Applied?

## Required report and evidence

Submit the report only on the assigned Owner branch and path stated in the source task. Include all six dimensions, candidate disposition, alternatives, workload assumptions, resource estimates versus measurements, failure/recovery matrix, compatibility, ADR/prototype/test needs, exact reviewed SHAs, bilingual change manifest, verdict and explicit no-claim statement. Read back the report and provide final branch HEAD SHA.

本任务必须遵守 GOV-DOC-001：任何架构语义、技术决策或验收条件变化均须同一变更集更新中英文文档，并登记双语覆盖情况。
