# F — Memory Runtime Technology Architecture Review

- Document: TAR-AI-001 / TAB-001 v0.1
- Owner: F — Memory Runtime Architect
- Branch: `session-f-memory-runtime`
- Reviewed branch HEAD: **PENDING exact parent-SHA verification during report publication**. Branch existence and branch-local file reads were verified; the GitHub file reader returned blob SHAs but not the resolved ref commit SHA.
- Review date: 2026-11-17
- Report version: 1.0
- Verdict: **CONDITIONAL PASS**
- Review mode: static, branch-aware document review; no implementation or benchmark certification.

## 1. Executive Summary

TAB-001's Runtime direction is viable as a local-first, modular Rust subsystem: structured filtering and lexical retrieval first, optional ANN/reranking later, disposable per-session Working Sets, and cache hits revalidated against current authorization and Forget state. F's ownership boundary is clear: F owns retrieval, ranking/fusion, freshness/completeness, Working Set/cache and ActivationRecommendation; it does not own Canonical Memory Version or G's ContextVersion.

Conditional acceptance is limited to architecture direction. The first implementation must not freeze an index technology, numerical latency/SLO, cache TTL/capacity, or cross-module Forget completion semantics until representative workloads and D/E/I contracts are available. The current branch read confirms strong cache/Working Set suppression semantics, but the full five-document F design package and exact current branch HEAD were not independently enumerated by the available GitHub interface in this review. Phase 2's branch-aware reconciliation records five F documents and an F branch-local Conditional Pass at design commit `dad5deb6bfaa2df9956930d0b1372df354112567`; that is a historical design baseline, not proof of the current branch HEAD.

### Blocking findings

- **F-TAR-P1-001 — Index publication contract and typed watermark vector:** F must consume D's per-authority CanonicalCommitCursor without owning it, and expose F-owned per-index/per-partition IndexWatermark with gap/coverage semantics. A single maximum watermark is insufficient.
- **F-TAR-P1-002 — Forget/revocation race closure:** cache/index suppression is directionally sound, but F cannot claim anti-resurrection closure while D/E/Storage's producer admission, dependency registration and final publication gate remain OPEN.
- **F-TAR-P1-003 — Candidate technology selection is not evidence-backed:** FTS5/Tantivy/ANN candidates require workload benchmarks and deterministic rebuild/fence tests; no measured result was found.
- **F-TAR-P1-004 — Retrieval completeness and cross-channel authorization:** every candidate-producing backend must filter before candidate emission, including graph edges, Evidence and Provenance dereference; a late response filter is insufficient.

## 2. Review Scope and Evidence

### Reviewed sources

| Source | Ref / Blob SHA | Use |
|---|---|---|
| TAB-001 | main; blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` | Candidate stack, ownership, cursor and index rules |
| TAR-AI-001 | main; blob `5a813edeccf7190d66dfd71a96ca581c48f8a4cb` | F-specific workload, channel and report requirements |
| Phase 2 D/E/F/G reconciliation | main; blob `3cd31abeac88703de5b9a0b29bea5d82cd5fdee7` | Branch-aware F design baseline and cross-module findings |
| Phase 3 D/E/H/I contract review | main; blob `edaccb802e0425f2d47bd4b613fab4dfde107144` | D cursor, D/E atomic gate, I/F Forget vector dependency |
| F Runtime Working Set and Cache | F branch; blob `a934491950c876701e8ac592a0e6aaea983b44e3` | Cache keys, session isolation, invalidation, fail-closed behavior |

Phase 2 records F branch design commit `dad5deb6bfaa2df9956930d0b1372df354112567` and five design documents. The exact current branch HEAD was not exposed by the branch/file operations used here; it is not represented as verified. The other F design filenames were not independently resolved in this read and are treated as secondary evidence through the Phase 2 reconciliation, not as newly fetched artifacts.

### Scope boundaries

Included: retrieval channels, candidate admission, fusion/ranking, freshness, IndexWatermark, Working Set/cache, scheduling, session isolation, Forget/revocation, resource sizing, recovery and D/E/G/H/I compatibility.

Excluded: canonical persistence/MemoryVersion (D), compiler derivative publication (E), Context membership/version/delivery intent (G), wire schema (H), global authorization policy and global Forget completion (I).

## 3. Six-Dimension Review Matrix

| Dimension | Verdict | Finding |
|---|---|---|
| R1 Requirements & workload fit | CONDITIONAL | Workload dimensions are identified, but corpus size, query mix, selectivity, update/delete rate, top-k, recall and p95/p99 targets are unquantified. |
| R2 Dependencies & boundaries | CONDITIONAL | F/D/E/G/I ownership is consistent; typed cursor and final publication gate remain cross-owner dependencies. |
| R3 Candidate selection | OPEN / TO_VALIDATE | FTS5, Tantivy, sqlite-vec and usearch/HNSW are candidates only; no reproducible benchmark selects one. |
| R4 Resource constraints | OPEN / TO_VALIDATE | Bounded memory policy exists; numeric RAM/disk/CPU budgets and peak-concurrency measurements are absent. GPU contention with embeddings/reranking is not measured. |
| R5 Failure recovery & safety | CONDITIONAL | Cache miss degrades safely; stale/unverifiable entries are quarantined. Index partial outage, rebuild, tombstone compaction and fence races need executable evidence. |
| R6 Interface compatibility | CONDITIONAL | F must consume D's global per-authority cursor and preserve F-owned per-partition watermarks; G consumes completeness vectors, not a scalar. |

## 4. Component Dependency Analysis

1. **D → F:** D is authoritative for immutable Memory identity/version, lifecycle, canonical commit order and Forget fence. F consumes typed references and revalidates canonical lifecycle/fence; it MUST NOT mint or advance CanonicalCommitCursor or ForgetFenceGeneration.
2. **E → F:** E's committed publication feed is an input to indexers. F's IndexWatermark is per channel/partition and cannot be substituted for E source sequence or D CanonicalCommitCursor.
3. **I → F:** I supplies authenticated Principal/Scope authorization and PermissionEpoch/revocation policy. Scope filtering is not authorization. If I's current decision is unavailable, protected retrieval/cache access fails closed.
4. **F → G:** F returns RetrievalResult and ActivationRecommendation with exact MemoryVersion refs, per-channel completeness, gaps, scores/rationale and typed watermark vector. G alone creates ContextEntry/ContextVersion/ChangeSet.
5. **H/C → F:** authenticated session/Agent context and query boundary arrive through integration; payload identifiers are not proof of identity.
6. **F internal:** candidate generation → authorization/scope filter before candidate exposure → canonical/Forget revalidation → fusion/ranking → optional rerank → response-boundary revalidation → G handoff. No unauthorized candidate may influence ranking, summaries or activation.

## 5. Candidate Technology Comparison

| Candidate | Strengths | Risks / limits | Disposition |
|---|---|---|---|
| SQL structured filters | Strong Scope/lifecycle/temporal predicates; colocated with SQLite metadata | Query planning and joins may dominate at scale; ANN integration is separate | RECOMMEND as mandatory first channel |
| SQLite FTS5 | Minimal operations, transactional adjacency, easy local deployment | Tokenization/ranking limits; update/delete and large-corpus behavior require measurement | RECOMMEND first lexical prototype |
| Tantivy | Rust-native, configurable analyzers/ranking, independent index lifecycle | Separate index durability/rebuild/consistency; extra operational surface | CANDIDATE if FTS5 misses measured targets |
| sqlite-vec | Colocated vector search and simpler deployment | Extension maturity, filtered ANN semantics, delete/rebuild and packaging risk | CANDIDATE; validate before adoption |
| usearch/HNSW | Embedded ANN, fast approximate retrieval | Recall/filter trade-offs, memory footprint, update/delete/tombstone and deterministic rebuild | CANDIDATE; defer until embedding workload is stable |
| Reranker | Potential relevance gain | Adds model latency/VRAM and may create GPU contention | DEFER; optional and never on correctness-critical path |

Decision rule: start with structured SQL + FTS5 and a canonical revalidation path. Add ANN only when measured task quality/latency justifies it. Compare recall@k, NDCG or task-level relevance, p50/p95/p99, memory/bytes per vector, update/delete cost, rebuild time, filter selectivity, and Forget suppression latency on identical fixtures.

## 6. Resource Budget Analysis

No benchmark values are claimed. Define a workload envelope before sizing:

- Retrieval QPS = interactive sessions × queries/session × query rate.
- Candidate work = QPS × channels × candidate fan-out.
- Index storage = canonical indexed bytes + lexical postings + vector_count × dimensions × bytes_per_dimension × index_overhead.
- Cache RAM = sum(cache-family entry_count × measured mean/peak entry_bytes), capped by per-session and global quotas.
- Working Set RAM = active_sessions × per-session byte cap; references should be preferred over copied payloads.
- In-flight memory = concurrent retrievals × (candidate buffer + rerank input + response buffer).
- Disk headroom must include active indexes + rebuild staging + WAL/temporary files + backup/restore workspace.

Required controls: per-session and global byte/item limits, queue bounds, admission control, cancellation on session close/revocation/Forget, cache-fill coalescing only for identical full authorization/freshness keys, and backpressure on background index work. Local 12–16 GB VRAM is not a Runtime cache budget; embedding/reranking must coordinate with the optional LLM worker and default to bounded/sequential GPU admission.

## 7. Failure & Recovery Matrix

| Failure | Authority / recovery source | Required behavior | Proposed test |
|---|---|---|---|
| SQLite/metadata store unavailable | D canonical store + durable index checkpoint | Do not claim currentness; fail closed for protected stale paths | F-REC-01 |
| FTS/Tantivy/ANN channel lag or missing partition | F per-channel watermark + D canonical state | Return explicit Partial/Unknown completeness or safe bounded wait; never infer absence | F-REC-02 |
| Index rebuild after Forget | D fence + canonical history; I target policy | Rebuild excludes fenced lineage; staged generation stays invisible until validated | F-FRG-01 |
| Cache invalidation notification lost | Durable D/I epochs | Every read revalidates; checkpoint gap quarantines namespace | F-FRG-02 |
| Forget during retrieval/cache fill | D fence | Cancel/invalidate in-flight work and recheck before G handoff | F-FRG-03 |
| Permission revocation during cache hit | I PermissionEpoch | Reauthorize before content access; fail closed if authority unavailable | F-SEC-01 |
| Adapter/session reconnect | H/C authenticated session + G reconciliation | Do not restore old Working Set before current fence/permission reconciliation | F-RCN-01 |
| Process crash during index publication | F generation/watermark and D/E committed feed | Resume from durable checkpoint; partial generation remains non-authoritative | F-REC-03 |
| Disk full / rebuild staging failure | Canonical store remains authoritative | Preserve old safe index only if fence-current; otherwise mark unavailable | F-REC-04 |

## 8. Interface Compatibility Findings

- D's CanonicalCommitCursor is one globally ordered sequence per Canonical Memory Authority. F consumes it as an opaque typed cursor; it is not an IndexWatermark.
- IndexWatermark must be a vector keyed by index/channel/partition and include generation, contiguous coverage, gaps, schema and checkpoint semantics.
- ForgetFenceGeneration is not a cursor and is not numerically compared with PermissionEpoch or ContextVersion.
- F's cache key must bind Principal/security domain, ScopeRefs, Environment, Session dimensions, PermissionEpoch, ForgetFence, exact Memory/Entity version or index generation/watermark, query fingerprint, retrieval config and temporal/evidence access class.
- F's cache document explicitly requires stale entries to be dropped/quarantined, never served; TTL is only an optimization.
- G must receive completeness metadata and watermark vectors. F cannot declare Context sufficient or Applied.
- D/E/Storage producer-registration and publication linearization remains OPEN; F can suppress and report, not close D/E global barrier.
- B Fact/Claim and typed ActorRef/ScopeRef semantics remain OPEN/ADR-BLOCKED; index schema and filter fields must not be frozen around assumed semantics.

## 9. Blocking Findings

| ID | Severity | Finding | Required closure |
|---|---|---|---|
| F-TAR-P1-001 | P1 | Canonical cursor ↔ index watermark mapping lacks verified executable feed contract | D/E/F/A typed-cursor conformance vectors and gap/replay tests |
| F-TAR-P1-002 | P1 | D/E atomic admission/fence/dependency/publication gate remains OPEN | D/E/Storage race contract; F late-index-publication fence test |
| F-TAR-P1-003 | P1 | Search technology not selected against workload | FTS5/Tantivy/ANN benchmark with identical corpus and Forget/rebuild fixtures |
| F-TAR-P1-004 | P1 | All channel pre-candidate authorization and completeness not evidenced in implementation | Negative tests for SQL/FTS/ANN/graph/evidence/provenance and response boundary |
| F-TAR-P2-001 | P2 | RAM/disk/cache sizing and TTL/eviction thresholds unmeasured | Representative workload benchmark and resource telemetry |

## 10. Required ADRs

1. ADR-F-001: first vertical-slice retrieval channel selection (structured + FTS5 baseline; criteria for Tantivy).
2. ADR-F-002: vector index admission criteria, filtered ANN semantics, delete/tombstone and rebuild.
3. ADR-F-003: typed IndexWatermark shape, partition coverage and cursor-to-index causal mapping, jointly coordinated with D/E/A.
4. ADR-F-004: cache family budgets, eviction, TTL and disk-cache policy, subject to I data classification.

## 11. Required Prototypes and Tests

- Structured + FTS5 vertical slice with exact Scope-before-candidate semantics.
- Tantivy comparison harness; ANN comparison only after embeddings and corpus are stable.
- Per-channel/per-partition watermark checkpoint and gap/replay simulator.
- Forget/revocation race injection during candidate generation, ranking, cache fill, index publish and rebuild.
- Property tests for typed cursor namespace separation, cache key non-collision, idempotent invalidation and no tombstone regression.
- Multi-session isolation and adversarial cross-scope/evidence/provenance fixtures.
- Benchmarks: corpus size, selectivity, QPS, top-k, update/delete, p50/p95/p99, recall/quality, RAM/disk, rebuild duration and 12–16 GB VRAM contention profile.

## 12. Verdict

**CONDITIONAL PASS** for the candidate Runtime architecture direction. F may proceed with a structured + lexical prototype and retain ANN/reranking as candidates. Do not freeze index backend, resource SLOs, cache thresholds or Forget completion semantics. P1 findings above block implementation sign-off and system-wide Forget conformance.

## 13. Evidence and Exact SHAs

- TAB-001 blob: `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`
- TAR-AI-001 blob: `5a813edeccf7190d66dfd71a96ca581c48f8a4cb`
- Phase 2 reconciliation blob: `3cd31abeac88703de5b9a0b29bea5d82cd5fdee7`
- Phase 3 D/E/H/I review blob: `edaccb802e0425f2d47bd4b613fab4dfde107144`
- F Working Set/cache blob: `a934491950c876701e8ac592a0e6aaea983b44e3`
- F design baseline commit recorded by Phase 2: `dad5deb6bfaa2df9956930d0b1372df354112567` (not asserted to be current HEAD)
- Branch current HEAD: pending exact commit-parent verification; no fabricated SHA.
- No runtime, fault-injection, security, or performance tests executed in this review.
