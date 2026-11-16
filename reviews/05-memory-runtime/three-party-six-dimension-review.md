# Session F — Three-Party / Six-Dimension Architecture Review

- Review target: Session F Memory Runtime design documents.
- Review date: 2026-11-16.
- Review type: static architecture self-review against repository A/B/C baseline; not independent external sign-off, code audit, benchmark or penetration test.
- Status: **Conditional Pass — suitable for cross-session integration review; not a frozen implementation or wire contract.**
- Baseline commit: e443b23f8a179ad12c163722ad93bc646fd3a80a.

## 1. Review scope and evidence
Reviewed the repository README, roadmap, governance invariants/principles/terminology, system architecture and quality attributes, domain model and scope/provenance/lifecycle semantics, A/B/C integration review, and A/B/C specialist review reports. The checkout contains no 03-memory-brain or 04-memory-compiler directories and no G/H/I detailed contracts. D/E/G/H/I fields and methods in F documents are therefore provisional. No claim is made that runtime behavior has been implemented or tested.

## 2. Six-dimension review

### 2.1 Architecture and responsibility boundaries
**Pass with conditions.** Runtime is separated from Agent planning, Compiler writes, Canonical Store authority and G Context Version authority. Retrieval returns candidates; Activation recommends; G decides Context edits. Working Set is disposable and distinct from Context and canonical assets. Modular monolith remains compatible with I-21.

**Residual:** G must confirm whether it consumes activation proposals directly or via an intermediate candidate envelope. D must confirm canonical read/lifecycle APIs. Do not implement cross-boundary assumptions before contract review.

### 2.2 Retrieval model and activation correctness
**Pass with conditions.** Structured, entity, full-text, vector ANN, graph/relation, temporal and provenance/evidence channels are represented. Vector is not privileged as the sole source. Candidate fusion preserves exact Memory Version and conflict alternatives. Activation separates existence, relevance, suitability and urgency; hard safety gates cannot be overridden by score.

**Residual:** Query routing, RRF/calibrated fusion, evidence weighting, context coverage and policy thresholds need labelled evaluation. Claim revision/Conflict Set identity is unresolved (INT-P1-02).

### 2.3 Data flow and consistency
**Pass with conditions.** Canonical authority wins over projections. Per-channel watermark/freshness and bounded canonical read-through/wait/partial semantics address AR-004. Stale hits are suppressed and repaired; index rebuild is based on canonical committed state and current Forget status.

**Residual:** E must define commit event ordering, watermark partitioning, outbox/replay and canonical delta API. A single scalar watermark may be insufficient for sharded/independent indexes. This is OPEN, not assumed solved.

### 2.4 Scope, security and Forget
**Pass at design-invariant level; implementation unverified.** INT-P0-02 explicitly filters within each candidate generator before ANN/lexical/structured/temporal result materialization, and reauthorizes graph edges and targets. Reranker sees authorized candidates only. Cache keys include principal/scope/environment/policy epoch. Revocation and Forget fences suppress cached and in-flight results before disclosure. INT-P0-03 prevents index replay resurrection. INT-P0-04 treats Memory as inert untrusted data and preserves provenance/trust/risk metadata.

**Residual:** True pre-filter guarantees depend on selected ANN/lexical/graph backend. I must define policy epochs, revocation timing, Forget operation/tombstone and audit semantics. Prompt injection remains a model-behavior residual risk; no guarantee of model obedience is claimed.

### 2.5 Latency, throughput and resources
**Pass with conditions.** Candidate count, graph fan-out, evidence expansion, wall-clock, concurrency, cache size and queues are bounded dimensions. CPU/RAM/disk/GPU responsibilities are separated; default Recall does not need LLM/GPU. Partial/degraded results expose budget exhaustion.

**Residual:** All numeric budgets, P95/P99 and local GPU suitability remain TO_VALIDATE. Benchmark representative structured/lexical/vector/graph/temporal mixes and cross-scope distributions before selecting thresholds.

### 2.6 Evolvability and observability
**Pass with conditions.** Provisional contracts carry schema/config/policy versions, exact Memory Version, watermarks, completeness and correlation. Trace path covers authorization, channels, canonical validation, fusion, activation and G handoff. Metrics avoid raw payloads and high-cardinality IDs.

**Residual:** H owns wire/error compatibility; I owns audit/privacy rules; E owns index generation/replay; G owns Context schema. Add property tests and fault injection after these contracts stabilize.

## 3. Forced integration issue status

| Issue | F design response | Status |
|---|---|---|
| INT-P0-02 Scope-before-Candidate | pre-filter inside every candidate-producing backend; graph edge + target authorization; reranker isolation; non-leaking counts/errors; scoped cache keys and epoch revalidation | **DESIGNED / implementation TO_VALIDATE** |
| INT-P0-03 Forget | durable fence suppresses candidate generation, cache/Working Set and in-flight work; canonical state wins during index lag/rebuild | **DESIGNED / I+D+E contract OPEN** |
| INT-P0-04 Prompt Injection | memory/evidence treated as untrusted data; preserve provenance/trust/epistemic/risk; no tool authority; residual model risk explicit | **DESIGNED / end-to-end controls OPEN** |
| INT-P1-01 Context Version | F returns immutable RetrievalResult and ActivationRecommendation; no ContextEntry/version ownership | **BOUNDARY DECIDED / G contract OPEN** |
| INT-P1-02 Claim / Conflict | preserve revisions, Conflict Set, support/refute evidence and epistemic state; no adjudication | **SEMANTICS CANDIDATE / B+D+E contract OPEN** |
| INT-P1-06 Provenance | evidence/provenance refs retained; budgeted expansion; independent authorization and availability markers | **DESIGNED / D+E lineage contract OPEN** |
| AR-004 Canonical/Index inconsistency | watermarks, required fences, bounded read-through/wait/partial, canonical revalidation and replay suppression | **CANDIDATE / E+I recovery contract OPEN** |

## 4. Three reviewer perspectives

### Principal Architect
Boundary model is coherent: F owns online retrieval execution and activation recommendation, not memory truth or Context version. The main risk is prematurely treating provisional D/E/G/I interfaces as stable.

### Engineering / Performance Reviewer
The plan is implementable as modular-monolith components with bounded async task groups. Backend pre-filter semantics, per-partition watermarks, cancellation and cache invalidation need prototypes and integration tests. No numerical latency promise is justified yet.

### Security / Reliability Reviewer
The most important property is not ranking quality but preventing unauthorized candidates from crossing backend boundaries. Cache keys alone are insufficient; read-time reauthorization and durable Forget fences are required. Prompt-injection risk is mitigated, not eliminated.

## 5. Acceptance tests required before implementation sign-off
1. Backend-level proof that Scope predicates run before candidate emission for ANN, full-text, structured and temporal paths.
2. Graph traversal reauthorizes each edge and target; reranker receives no denied candidates.
3. Counts, score distributions, errors and traces reveal no unauthorized existence.
4. Revocation and Forget fences suppress in-flight, cached and Working Set results.
5. Canonical/index lag returns exact freshness and partial semantics; rebuild cannot resurrect Forgotten content.
6. Disputed/retracted/superseded Claims retain epistemic state and evidence.
7. Evidence source permission is checked independently.
8. Context Version remains G-owned; F cannot mutate it.
9. Default Recall succeeds without LLM/GPU dependency.
10. Fault injection covers timeout, cancellation, lost invalidation, delayed index publication and concurrent permission changes.
11. Benchmark report records hardware, corpus, scopes, query mix, concurrency, cache state, percentile methodology and correctness labels.

## 6. Decision register

- **DECIDED:** Runtime is read/activation execution layer, not Agent Runtime.
- **DECIDED:** Canonical Memory is authority; Index/Cache/Working Set are rebuildable/disposable projections.
- **DECIDED:** Scope-before-Candidate is a hard invariant, not a reranking filter.
- **DECIDED:** Forget/revocation fences override stale indexes and caches.
- **DECIDED:** Retrieval Result is distinct from ContextEntry/Context Version.
- **CANDIDATE:** RRF or calibrated hybrid fusion; async task groups; per-session Working Set plus partitioned shared caches.
- **TO_VALIDATE:** all numeric budgets, score weights, thresholds, ANN engine guarantees, P95/P99 and resource envelopes.
- **OPEN:** D/E/G/H/I exact contracts; watermark/fence shape; permission epoch/revocation SLA; Conflict Set and provenance graph schemas.

## 7. Final review verdict
**Conditional Pass.** F architecture is internally coherent and respects the A/B/C governance baseline. It is ready for cross-session D/E/G/I integration review, but not for schema/wire freeze or implementation claims. All open dependencies must be resolved by their owning sessions; this review does not close their INT issues.
