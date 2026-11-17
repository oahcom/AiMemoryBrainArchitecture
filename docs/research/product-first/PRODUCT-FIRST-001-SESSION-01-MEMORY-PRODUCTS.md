# PRODUCT-FIRST-001 — Session 01: AI Memory Product Adoption Research
# AI Memory 产品采用研究

- Task: `PRODUCT-FIRST-001`
- Session: `01`
- Owner role: AI Memory Product Adoption Research Owner
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Baseline: `main@b3c666e67982cb3d3374e759cfb6552c7765aacb`
- Research date: 2026-11-18
- Status: **PARTIALLY VERIFIED — OFFICIAL DOC/SOURCE INSPECTION; NO BRAIN PROTOTYPE OR BENCHMARK**
- Decision status: **PROPOSALS ONLY — NO ADR APPROVED, NO TECHNOLOGY FROZEN**

---

## 1. Executive Summary / 执行摘要

### 1.1 Conclusion / 结论

**Recommendation: use product-assisted, Brain-authoritative architecture; do not replace the Brain with any single memory product.**

**建议：采用“产品辅助、Brain 保持权威”的架构；不建议用任何单一 Memory 产品替代 Brain。**

The strongest candidates are complementary rather than interchangeable:

1. **Graphiti (Apache-2.0)** is the most relevant open-source candidate for temporal entity/relation extraction, episode-linked provenance, temporal fact evolution and graph/hybrid retrieval. It is a candidate derivative projection, not Canonical Memory Truth.
2. **Mem0 (Apache-2.0)** is a useful candidate for conversational fact extraction, memory update/deduplication, vector/metadata retrieval and SDK integration. Its abstraction is not a substitute for Brain's typed Event/Fact/Claim/Evidence/Lifecycle contracts.
3. **Hindsight (MIT)** is a strong candidate for a complete memory-pipeline experiment: retain/recall/reflect, evidence-linked observations, temporal/graph/semantic retrieval, and PostgreSQL-centered deployment. Its observations remain non-authoritative.
4. **Letta / MemFS** is valuable for agent-owned editable memory files, Git history, procedural memory and self-improvement workflows. It is not a general multi-agent canonical memory authority.
5. **LangMem (MIT)** is a composable extraction/consolidation toolkit with LangGraph Store integration. It is a useful algorithm reference, not a Brain governance system.
6. **Zep Cloud** offers managed context-graph operations, but its service/database is proprietary and introduces vendor/data-residency/authority dependency. Evaluate separately from Apache-2.0 Graphiti.

No candidate has been shown to provide the complete conjunction of Canonical Truth + independently governed Evidence/Provenance + authorization/revocation + Forget fencing + cross-system lifecycle + final inference-boundary Applied evidence. These remain Brain-owned composition and authority boundaries.

**No product is recommended as the initial system-of-record.** The lowest-risk next step is a disposable, non-authoritative adapter spike comparing Graphiti, Mem0 and Hindsight against the same labeled corpus, while keeping Brain-owned records and lifecycle authoritative.

### 1.2 Decision snapshot / 决策摘要

| Capability | Proposed strategy | Status |
|---|---|---|
| Memory ingestion | WRAP | Candidate |
| Memory extraction | EXTEND | Candidate |
| Entity resolution | EXTEND | Candidate |
| Fact / Claim modeling | BUILD | Owner B authority; Fact/Claim ADR remains blocked |
| Temporal memory | EXTEND | Candidate Graphiti/Hindsight projection |
| Provenance | BUILD | External lineage is evidence input only |
| Contradiction detection | EXTEND | Candidate proposals, Brain adjudicates |
| Memory consolidation | EXTEND | Candidate asynchronous proposals |
| Memory retrieval | WRAP | Candidate search backends |
| Memory ranking | EXTEND | Candidate rerankers; Brain applies policy |
| Forget / deletion | BUILD | D/I/Storage authority; products are downstream targets only |
| Multi-Agent sharing | WRAP | Brain scope/auth policy remains authoritative |
| Memory lifecycle | BUILD | Brain Owner D/E/I/Storage contracts |
| Memory quality evaluation | EXTEND | Product tooling + Brain-specific conformance suite |

### 1.3 Explicit non-claims / 非声明

- No benchmark, prototype, load test, migration rehearsal, security audit or Brain end-to-end conformance test was run.
- Public product claims and vendor benchmarks are not treated as independently verified performance results.
- Product release/version statements are snapshots, not dependency pins. Exact release tags, transitive licenses, CVEs and SBOMs must be rechecked before adoption.
- This report does not approve an ADR, select a database/deployment topology, or freeze any Owner contract.

---

## 2. Current Architecture Baseline / 当前架构基线

### 2.1 Exact project baseline / 精确项目基线

- Current main HEAD read from GitHub: `b3c666e67982cb3d3374e759cfb6552c7765aacb`.
- README read from `main`: repository status is Architecture Definition; implementation status is Not Started by Design.
- PR #45: historical technology research, open Draft, base `b372b62c640a2b656e54b6db62a4ee67d7d8c001`, head `6c7c5919c1b50f38c4d24be679a3885ee3c15b97`.
- PR #56: independent review of #45, open Draft; verdict REVISE / NOT YET PROVEN; findings include currentness, Restate Server license disclosure and semantic parity.
- PR #73: current-source remediation package, open Draft; explicitly a role-simulated integration/remediation artifact, not real Owner signatures or approvals. Its remediation source was read from branch `remediation/TECH-REALITY-001-A-multi-owner-2026-11-18`, including D/E/I/Storage boundaries, Applied status and product-relevant constraints.

The previous PRs are treated as prior evidence, not copied as a substitute for this product-specific comparison. This report adds a focused evaluation of Mem0, Graphiti/Zep, Letta/MemFS, Hindsight and LangMem, mapping them to the 14 requested capabilities.

### 2.2 Architecture invariants that products must not override / 产品不得覆盖的架构不变量

1. Canonical Memory Truth belongs to Brain/D + Storage, not a product's memory table, graph or vector store.
2. Evidence/Provenance authority is a Brain-owned semantic contract. A product's source pointer, episode ID, quote or confidence score is an input artifact, not proof of authority or truth.
3. Authorization, principal identity, policy domain, permission epoch and revocation belong to Owner I. A product's user_id, tenant_id, bank_id or graph_id is not authorization.
4. Forget authority and fence ordering belong to Owner D/I/Storage and associated producer/consumer contracts. A vendor DELETE endpoint is not a Forget protocol.
5. Lifecycle authority, producer registration, dependency inventory, publication participation and terminality remain Brain-owned.
6. Context Applied Evidence authority remains at the C/G/H inference boundary. A memory product returning search results or an agent storing a memory file does not prove the exact context was applied to the final inference request.
7. Retrieved memory is untrusted data, never system/developer instruction authority.
8. Indexes, graph projections, embeddings, caches, summaries and product memory objects must be replaceable derivatives unless an explicit Brain-owned contract says otherwise.

### 2.3 Current-source contract delta / 当前契约增量

The current remediation branch records the following exact proposal evidence and limitations:

- **D:** `03-memory-brain/phase-3.8-d-publication-participant-and-terminal-contract.md`, Blob `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78`. D owns ProducerClass eligibility, ProducerWork admission, RegistrationReceipt/sequence, ForgetFence ordering, dependency/lineage inventory, publication participant and terminality. Exact Owner approval, callable API and conformance remain OPEN.
- **E:** `04-memory-compiler/phase-3.8-e-publication-orchestration-retry-recovery-contract.md`, Blob `475fee41e5eea527af4edefbfe88c58c86967d0a`. E owns compile intent, ingress receipt, immutable input bundle, DerivationRun/Attempt/Lease, private staging and compiler recovery orchestration. Queue ACK or local Published/Completed labels are not cross-owner proof.
- **I:** `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md`, Blob `54bab0484bd232a5a258e65e34cc7425288b39a6`. I owns principal/workload/delegation trust, PolicyDomain, authorization, PermissionEpoch, revocation ordering, issuer/key status and authorization terminal proof. Authorization is necessary but not sufficient for visibility.
- **Storage:** logical contract Blob `175ee7b1349cfdb79a19898b311a88391ed88010`; topology ADR Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`. L1 logical serialization Option A is selected in the proposal; L4 physical engine/deployment remains OPEN. This does not select any product backend.
- **C/G/H Applied:** Issue #3 remains Applied Contract Frozen = NO; Test Executed/Passed = NO/NO; Implementation Verified = NO. Candidate schemas/CI do not prove production adapter or final-request Applied.
- **B Fact/Claim** remains ADR-BLOCKED.

**Interpretation:** product integration can begin only behind a derivative boundary and cannot be used to close D/E/I/Storage or Applied blockers.

---

## 3. Product Capability Matrix / 产品能力矩阵

Legend: **V = VERIFIED from inspected official documentation/source for the stated behavior; P = PARTIALLY VERIFIED (behavior exists, but completeness/production guarantee is not proven); U = UNVERIFIED for Brain-specific requirements.** A product feature is not a Brain contract proof.

| Product | Ingestion / extraction | Entity & temporal graph | Provenance / contradiction | Retrieval / ranking | Forget / governance | Multi-agent / lifecycle | Fit |
|---|---|---|---|---|---|---|---|
| Mem0 OSS | V: add pipeline, LLM fact extraction, update/dedup flows | P: entity store/graph features; not full bitemporal authority | P: history and metadata; U: complete evidence lineage and authoritative conflict adjudication | V: vector + metadata/search ecosystem; P: ranking depends on configuration | P: memory delete/history APIs; U: cross-index/backup/restore Forget fencing | P: user/agent/app/run scopes; U: Brain producer/lifecycle/Applied | High as adapter candidate |
| Graphiti | V: episode ingestion and incremental graph extraction | V: temporal edges, entity nodes, custom ontology, hybrid graph search | V: episode-linked provenance; P: temporal invalidation; U: authority/epistemic truth | V: graph + semantic + BM25 hybrid retrieval | U: Brain-wide Forget and downstream deletion guarantees | P: graph/subject boundaries; U: authorization and applied proof | Highest semantic overlap |
| Zep Cloud | V: managed ingestion of messages/text/JSON/documents | V: managed Context Graph built with Graphiti | V: episode source links and temporal edge validity; U: Brain authority | V: managed retrieval/context APIs | P: service governance features; U: exact Brain fence/erasure proof | P: user/shared graph model; U: cross-owner lifecycle | Managed option, higher lock-in |
| Letta / MemFS | V: agent-editable files, memory blocks, Git-backed changes | U: not a temporal entity graph product | P: Git history gives revisions; U: fact-level evidence lineage | P: file/context retrieval and agent tools | P: file deletion/history controls; U: Forget propagation to derivatives/backups | V: agent-scoped memory repository; U: Brain multi-agent authorization | High for agent workspace |
| Hindsight | V: retain extracts facts/entities/relations; async operations | V: entity graph, temporal links and temporal recall | P: observations linked to supporting memories/quotes; U: canonical evidence authority | V: semantic, BM25, graph, temporal retrieval + reranking | P: bank-level isolation and admin operations; U: D/I fence and downstream erasure | P: banks/tags/tenants; U: Brain lifecycle/Applied | High for benchmark |
| LangMem | V: extraction and background memory manager | P: store-dependent structured memories; not dedicated temporal graph | P: memory updates/consolidation; U: complete provenance authority | P: LangGraph Store search integration | U: no Brain Forget protocol | P: thread/store scoping; U: Brain lifecycle | Useful toolkit, not system |

### 3.1 Mem0 / 记忆抽象与工具链

**Position:** general-purpose memory layer for agents and applications. OSS implementation provides Python APIs, provider abstractions, SQL metadata/history and vector-store integration; platform API adds managed REST operations.

**Observed capabilities:** `Memory.add()` drives extraction/update flows; search and history APIs; individual and scoped deletion; entity and vector integrations. Official architecture describes SQL facts/metadata plus vector and entity stores. API documentation exposes add/search/get/update/delete/history and delete-by-filter operations.

**Source inspection:** prior PR #45 research recorded Mem0 v2.2.1, Apache-2.0, source snapshot tree `f1791daa86d469249c9b002f62644d58a1eb96a0`, with `mem0/memory/main.py`, `mem0/memory/storage.py` and vector-store adapters inspected. This session independently read official source/documentation for the current API and architecture; exact currently latest release is not re-pinned in this session.

**Data/persistence:** SQL facts/metadata/history, vector store and entity store can be configured; the multi-store topology creates cross-store consistency and deletion coordination work.

**Fit and gaps:** good for a disposable extraction/search subsystem or Python sidecar. Does not model the full Brain typed distinction among Event, Fact, Claim, Evidence, Entity, Relation, ContextVersion and Applied evidence. No public evidence proves D/I fences across SQL, vector/entity stores, caches, replicas and backups.

**License/deployment:** Apache-2.0 for OSS repository; Python runtime and model/vector-provider dependencies. Self-hosted REST/Docker options exist; managed Platform API is a separate service and commercial offering. Audit each dependency and hosted-service terms independently.

**Decision:** WRAP / EXTEND only; do not adopt as canonical store.

### 3.2 Graphiti / Zep / 时态知识图谱

**Position:** Graphiti is an open-source temporal context-graph framework; Zep is the managed context platform built around Graphiti-derived graph artifacts.

**Observed capabilities:** Graphiti ingests episodes (text/message/JSON), extracts entities and relationships, models facts as temporal edges, supports custom entity/edge types, and combines semantic, BM25 and graph traversal retrieval. Zep's current documentation describes nodes, edges and episodic nodes; edges retain source episode references and validity timestamps. Documentation explicitly cautions that provenance identifies source data but does not establish correctness.

**Source inspection:** PR #45 recorded Graphiti v0.31.2, Apache-2.0, source tree `869c1b279e01a2767a464581e1cb657ce0e39271`; inspected `graphiti_core/graphiti.py`, `nodes.py`, `edges.py`, search and driver operations. Current official docs were re-read in this session. Its `pyproject.toml` identifies `graphiti-core` 0.31.2, Apache-2.0, Python >=3.10, with Neo4j required dependency and optional FalkorDB/Neptune/provider extras. Upstream deprecates the Kuzu extra because upstream Kuzu is unmaintained.

**Data/persistence:** graph database drivers include Neo4j, FalkorDB and Neptune; LLM/embedding providers add runtime/network/cost dependencies. Graphiti is a library that the adopter operates. Zep Cloud abstracts Graphiti and uses its proprietary Konig graph service.

**Fit and gaps:** closest to Brain's temporal entity/relation and episode provenance needs. However, its episode lineage is not equivalent to Brain Evidence authority; temporal edge invalidation is not a global Forget fence; graph identity resolution is not Brain's canonical identity merge/split governance; graph query results are not authorization or Applied proof. Treat graph as a projection and candidate generator.

**License/deployment:** Graphiti Apache-2.0; Python plus graph DB and LLM/embedding provider. Zep managed service is proprietary/commercial; contract, retention, data residency, deletion and export terms need legal/operational review.

**Decision:** EXTEND/WRAP Graphiti for optional temporal graph projection; DEFER Zep Cloud pending managed-service and data-governance review.

### 3.3 Letta / MemFS / Agent state memory

**Position:** stateful agent platform. Letta Code uses a Git-backed memory filesystem (MemFS), memory blocks and external memory files. The agent can inspect/edit memory using ordinary filesystem and Git operations.

**Observed capabilities:** durable agent-scoped memory files, in-context vs external-memory placement, Git history/sync, background dreaming/consolidation and explicit teach/remember workflows. Changes become active through commit/recompile semantics rather than changing a request already in flight.

**Source inspection:** PR #45 recorded Letta Code v0.34.63, Apache-2.0, source tree `b622fb1bc0941981e08da5ec2b2736d897e9bde1`, with `src/agent/memory-filesystem.ts`, `memory-git.ts` and context modules inspected. Current official Letta repository/docs state the active code is in `letta-ai/letta-code`; the former Letta V1 API server is archived. Verify exact license for the selected release and distinguish Letta Code from Letta server/cloud service.

**Data/persistence:** agent-owned Git repository projected to a local checkout; cloud agents keep memory with agent state/conversations/configuration. File/commit identity is not a typed claim/evidence schema.

**Fit and gaps:** valuable for agent workspaces, procedural memory, project notes and human-readable editable memory. Not a shared canonical multi-agent store, not fact/claim adjudication, not an evidence registry, and not a system-wide Forget authority.

**License/deployment:** Letta Code source snapshot recorded Apache-2.0 in prior research; current Letta platform/cloud terms and separate SDK/package licenses require exact version audit. Node/TypeScript runtime; local App Server or cloud deployment options.

**Decision:** WRAP for agent-specific workspace memory; do not adopt as Brain canonical memory.

### 3.4 Hindsight / retain–recall–reflect

**Position:** complete agent-memory service focused on learning from long-running interactions rather than only storing conversation snippets.

**Observed capabilities:** retain accepts conversations/documents/facts and runs extraction; recall combines semantic, BM25, graph and temporal strategies with reranking; reflect synthesizes responses from memories. Observations are described as deduplicated, evidence-grounded consolidations with supporting-memory references/quotes and refinement when new evidence contradicts or extends prior observations. Banks provide isolation.

**Source inspection:** official repository README, API method docs, operation docs, installation/storage docs, Docker Compose and source architecture guides were read. Repository advertises MIT license. Inspected docs identify PostgreSQL + pgvector (or Oracle AI Database for enterprise), embedded pg0 for development, REST/Python/Node/Go clients and MCP; PostgreSQL is the principal production storage design. Current exact release tag/commit and complete transitive package license set were not pinned during this session.

**Fit and gaps:** strong candidate for comparative evaluation of consolidation, evidence-linked observations and multi-channel retrieval. It still makes product-specific memory/bank objects and autonomous synthesis decisions; those are proposals/derivatives, not Brain's canonical facts. Bank-level isolation does not replace I policy authorization. Deleting a bank or memory is not proof every derivative, worker, embedding, cache, backup and external context copy has been fenced and reconciled.

**License/deployment:** MIT at repository level; production deployment requires PostgreSQL and a supported vector extension per current install docs (documentation pages differ in stated production minor-version minimum; verify exact release requirements). Embedded pg0 is positioned for development, not production. LLM/embedding/reranker provider calls can dominate cost and data egress.

**Decision:** EXTEND/WRAP for benchmark and optional memory-projection service; never as Canonical Truth.

### 3.5 LangMem / memory manager toolkit

**Position:** composable toolkit for extracting, updating and consolidating agent memories; integrates with LangGraph Store while offering functional primitives for other stores.

**Observed capabilities:** hot-path memory tools and background memory manager; extraction/consolidation/update; LangGraph integration. It is a toolkit rather than a turnkey independent Brain authority service.

**Source inspection:** official GitHub README and integration docs were inspected. MIT license is indicated by the repository; exact current package release, source SHA and transitive license set remain to be pinned before adoption.

**Fit and gaps:** useful to compare extraction and consolidation strategies or borrow workflow patterns. Requires Python/LangGraph ecosystem and storage integration. No native Brain-grade evidence, Forget, lifecycle or final-request Applied contract.

**Decision:** EXTEND as optional algorithm/tooling reference; DEFER production integration until Python sidecar cost is justified.

### 3.6 Other products considered / 其他候选

- **Hermes Agent:** useful Agent-owned provider/memory adapter patterns, not a Brain service; prior PR #45 source research found MIT/Python, SQLite session backup and provider isolation. Do not conflate agent memory with canonical memory.
- **LangGraph Store/checkpointer:** useful distinction between thread checkpoint state and cross-thread long-term store; not a complete memory governance system.
- **Microsoft GraphRAG:** relevant for static corpus graph indexing but less directly suited to incremental temporal personal/agent memory than Graphiti; defer unless document-corpus synthesis becomes a separate requirement.
- **Qdrant / pgvector / Tantivy:** retrieval infrastructure rather than memory products. Candidate indexes only; cannot own canonical state or Forget.
- **Zep Cloud:** assessed separately from Graphiti due proprietary hosted data/control-plane boundary.

---

## 4. Capability-by-Capability Adoption Decisions / 逐项能力采用决策

| # | Capability | Decision | Candidate contribution | Brain-owned boundary / rationale |
|---:|---|---|---|---|
| 1 | Memory Ingestion | **WRAP** | Mem0/Graphiti/Hindsight adapters normalize raw conversations, messages, JSON and documents | Brain validates scope, principal, source identity, idempotency, admission and durable accepted receipt. Product ingest ACK is not Brain acceptance. |
| 2 | Memory Extraction | **EXTEND** | Mem0 extraction; Graphiti episode-to-entity/edge; Hindsight retain | Run as untrusted proposal generation. Brain validates typed schema, evidence linkage, policy and provenance before canonical commit. |
| 3 | Entity Resolution | **EXTEND** | Graphiti entity linking; Mem0 entity store; Hindsight entity extraction | Brain owns canonical Entity IDs, merge/split, alias history, collision resolution and evidence-based identity decision. Product IDs are external references only. |
| 4 | Fact / Claim Modeling | **BUILD** | Product output may seed candidate statements | B owns domain semantics; Fact/Claim ADR is blocked. Do not force products' triplets or flat memory records into canonical ontology. |
| 5 | Temporal Memory | **EXTEND** | Graphiti temporal edges; Hindsight temporal links/ranking | Brain owns valid-time/record-time semantics, supersession, event ordering and temporal truth policy. Product temporal fields are projection metadata until mapped. |
| 6 | Provenance | **BUILD** | Episodes, quotes, memory history and source IDs can be ingested as evidence references | Brain owns Evidence identity, integrity, authorization, retention and complete derivation lineage. Product provenance can be incomplete/truncated or mutable. |
| 7 | Contradiction Detection | **EXTEND** | Hindsight observations and Graphiti temporal invalidation; Mem0 update/conflict flows | Products generate contradiction candidates; Brain preserves competing claims, source/effective times and adjudication status. Never silently overwrite a canonical conflict. |
| 8 | Memory Consolidation | **EXTEND** | Hindsight observations/mental models; Letta dreaming; Mem0 dedup/update | Consolidation creates proposed derivatives with full lineage and idempotent derivation identity. It cannot delete source evidence or finalize Forget. |
| 9 | Memory Retrieval | **WRAP** | Graphiti/Hindsight hybrid search; Mem0 vector/metadata search; Tantivy/pgvector as separate infra | Search results are candidates. Brain must revalidate authorization, canonical status, freshness, temporal constraints and Forget suppression before ranking/activation. |
| 10 | Memory Ranking | **EXTEND** | Product rerankers, Hindsight fusion, Graphiti hybrid ranking | Brain owns policy-aware ranking/activation and source quality weighting. Rank cannot override permission, Forget or epistemic state. |
| 11 | Forget / Deletion | **BUILD** | Product delete APIs can be downstream cleanup adapters | D/I/Storage own request identity, authorization, target inventory, fence, barriers, terminal proof, retry/reconciliation and restore fencing. Product DELETE is not completion evidence. |
| 12 | Multi-Agent Memory Sharing | **WRAP** | Letta agent repositories; Graphiti shared graphs; Mem0 agent/app scopes; Hindsight banks/tags | Brain/I own tenant, principal, delegation, policy and share authorization. No product scope ID is a permission token. |
| 13 | Memory Lifecycle | **BUILD** | Product jobs/operations can execute derivative work | Brain owns ProducerWork admission, leases/fencing, dependency registration, publication participation, terminality and lifecycle recovery. |
| 14 | Memory Quality Evaluation | **EXTEND** | LongMemEval and product benchmark harnesses | Brain adds truth/provenance/Forget/authorization/temporal leakage/Applied-specific metrics. Vendor leaderboard is not Brain acceptance. |

### 4.1 Why not ADOPT as system-of-record? / 为什么不直接 ADOPT 为系统记录权威？

ADOPT is not recommended for any of the 14 semantic capabilities as a wholesale system-of-record transfer. The candidates expose valuable mechanisms, but their abstractions are optimized for their own product contract. The Brain contract includes independent authority domains and cross-owner proof requirements not established by a memory API.

No adoption should be described as “replace Memory Brain” unless a future independent, exact-version conformance campaign proves every authority boundary, race, failure and recovery path and the relevant Owners explicitly approve it.

---

## 5. Architecture Impact / 架构影响

### 5.1 Recommended integration shape / 建议集成形态

Use a **non-authoritative Product Adapter boundary**:

1. Brain accepts and durably identifies the source event under its own contract.
2. Adapter emits a redacted/minimized derivative payload to the selected product, with a stable Brain source/evidence reference and explicit scope metadata.
3. Product performs extraction, graph building, embedding, consolidation or retrieval.
4. Adapter maps product outputs to typed Brain proposal objects; raw product objects remain external references.
5. Brain validates scope, authorization, schema, source lineage, temporal semantics, conflicts and current Forget/lifecycle fences.
6. Only Brain's canonical transaction can publish an accepted canonical asset.
7. Retrieval adapter returns candidate IDs/scores/source pointers; Brain revalidates before context planning.
8. Forget propagates to the product as a downstream target, but Brain completion depends on authoritative target inventory and required acknowledgements/reconciliation.

The adapter must be replaceable. Product-specific IDs, schemas and embeddings must not leak into the canonical domain model except as explicitly typed external references.

### 5.2 Minimum first experiment / 最小实验

**Do not integrate all products.** Build a disposable offline harness outside the production architecture:

- One fixed, anonymized dataset with conversation episodes, structured JSON, corrections, temporal changes, contradictions, aliases, scoped sharing and Forget requests.
- Run Graphiti, Mem0 and Hindsight on the same input with pinned versions/configuration.
- Store raw source records and expected labels in the harness, not in product-managed truth.
- Export each product's extracted memories/edges/observations and retrieval results.
- Score outputs against a Brain-owned gold set.
- Simulate a Forget target and verify only product cleanup behavior; do not claim this proves Brain Forget.
- No product receives real secrets, production personal data or canonical write credentials.

Letta and LangMem should be second-wave comparisons for agent workspace and toolkit-specific use cases, not added to the first experiment.

### 5.3 Data authority matrix / 数据权威矩阵

| Data object | Authoritative owner | Product role |
|---|---|---|
| Raw accepted Event | Brain / E + D + Storage contracts | Optional source copy/episode |
| Canonical Fact/Claim | Brain / B + D + Storage | Candidate extraction only |
| Canonical Entity identity | Brain / B/D | Entity resolution proposal |
| Evidence identity and lineage | Brain-owned Evidence contract | Source pointer/quote input |
| Temporal validity and supersession | Brain domain contract | Candidate temporal edge |
| Embedding/vector/graph index | Brain runtime/index policy | Rebuildable projection |
| Authorization / revocation | I | No authority |
| Forget operation/fence/terminal proof | D/I/Storage | Downstream deletion target |
| Agent memory files | Agent/Letta workspace | Optional agent-local projection |
| ContextVersion / Applied proof | G/C/H contract | No authority |
| Quality score / rank | Brain evaluation/runtime policy | Signal only |

---

## 6. Security / Forget / Provenance Analysis / 安全、遗忘与溯源分析

### 6.1 Security boundary / 安全边界

- **Identity:** map authenticated Brain principal/workload/delegation to an opaque product scope. Never accept caller-supplied `user_id`, `bank_id`, `agent_id` or `graph_id` as proof of identity.
- **Authorization:** I authorizes the operation before any protected product read/write. Product-side RBAC is defense-in-depth, not the source of truth.
- **Data minimization:** send only minimum required text/metadata. Evaluate provider egress, model retention, telemetry, logs, backups, region and subprocessors.
- **Prompt injection:** all returned memories, graph facts, summaries, observations and memory files are untrusted data. They must not be interpolated into privileged instruction channels.
- **Cross-tenant leakage:** test every filter at ingestion, extraction, graph traversal, vector search, reranking, reflect and export—not just top-level bank/user partitioning.
- **Credential isolation:** products receive scoped short-lived adapter credentials, never Storage/I signing keys, D/I authority credentials or unrestricted canonical DB access.

### 6.2 Forget semantics / Forget 语义

A product DELETE endpoint can at most prove that a product accepted or completed a local deletion request under its own documented semantics. It does not prove:

- all extracted facts, linked entities, graph edges, summaries, embeddings and cached results were removed;
- all asynchronous jobs and retries are fenced against re-creating the forgotten data;
- replicas, exports, audit logs, object stores, snapshots and backups satisfy the requested erasure semantics;
- no stale retrieval replica can return a forgotten item;
- a restore cannot resurrect data from an older snapshot;
- all downstream Agent Context/Applied state was reconciled.

Required adapter behavior:

1. Accept Brain Forget operation ID + immutable digest + scope/target reference.
2. Make deletion idempotent; same operation ID with different digest is a hard conflict.
3. Close/hold product write admission for the affected scope or quarantine product outputs until Brain confirms fence state.
4. Enumerate product-native derivatives and asynchronous jobs where possible.
5. Delete/suppress and reconcile each derivative; retain an auditable result with exact product version/tenant/scope.
6. Treat timeout, lost ACK, partial delete and unknown state as unresolved—not success.
7. Recheck the fence before accepting any late extraction or consolidation output.
8. Restore/rebuild must replay Brain Forget/revocation state before product data can be queried.

**No current candidate is verified to satisfy this cross-product protocol.** Forget remains BUILD.

### 6.3 Provenance / 溯源

Graphiti and Hindsight provide the most useful source-linked derivative models:

- Graphiti episode nodes connect extracted nodes/edges to source episodes; source links support traceability but do not prove source correctness.
- Hindsight observations can reference supporting memories and quotes, supporting evidence display and consolidation audit.
- Mem0 history tracks memory changes, but memory history is not the same as a complete derivation graph.
- Letta Git history tracks file revisions, not fact-level source lineage.

Brain should preserve at least: source Event/Evidence ID, content digest, source span/quote where permitted, extractor/model/prompt version, derivation run ID, product/version/config, temporal assertions, validation result, and supersession/contradiction links. These are proposed mapping fields, not a new B/D contract.

### 6.4 Applied boundary / Context Applied

None of the products observes or proves the exact final inference request assembled by the Brain Adapter. A product may report “memory returned”, “context updated”, “agent memory committed” or “prompt enriched”; none is the C/G/H final-request Applied attestation. Product integration must be downstream of Brain ContextVersion planning and must not write Applied evidence.

---

## 7. License and Deployment Risks / 许可证与部署风险

| Product | Repository license evidence | Deployment / dependencies | Main risks |
|---|---|---|---|
| Mem0 OSS | Apache-2.0 | Python; SQL + vector/entity providers; optional REST/Docker; hosted Platform separate | Python sidecar, multi-store consistency, provider egress, hosted API terms, transitive license review |
| Graphiti | Apache-2.0 | Python >=3.10; Neo4j core dependency; optional FalkorDB/Neptune and LLM/embedding extras | Graph DB operations, provider calls, Python integration, deprecated Kuzu path, data duplication |
| Zep Cloud | Proprietary managed service (service terms govern) | Hosted Context Graph/Konig; API integration | Vendor lock-in, data residency/retention, pricing, export/deletion SLA, service dependency |
| Letta Code | Apache-2.0 in prior source snapshot | Node/TypeScript; local App Server or cloud; Git-backed storage | Agent runtime coupling, repository sync/backup, cloud-vs-local semantics, package/service license separation |
| Hindsight | MIT repository license | Python API; PostgreSQL + pgvector (or Oracle enterprise option); model provider; Docker/Helm | DB operations, model cost/egress, worker recovery, PostgreSQL extension compatibility, release/transitive license pinning |
| LangMem | MIT repository license | Python; LangGraph Store optional integration; LLM provider | LangChain ecosystem coupling, Store semantics/persistence supplied externally, release pin incomplete |

### 7.1 License controls / 许可证控制

- Repository license is not a complete legal opinion. Audit all packages, model weights, hosted service terms, datasets and transitive dependencies.
- Separate OSS client/library license from hosted platform/server terms.
- Prior technology research identified Restate Server as BSL 1.1 with an Additional Use Grant; its Rust SDK MIT license does not change the server license. Do not assume a permissive SDK makes a server dependency permissive.
- No legal review or SBOM scan was executed for this report.

### 7.2 Operational cost model / 运维成本模型

Measure, do not guess:

- CPU/RAM/disk and graph/vector index footprint per 10k/100k/1M source events;
- extraction and embedding tokens per event, retries and model-call amplification;
- database + graph store + vector store + worker + broker service count;
- p50/p95/p99 ingest completion, recall latency and deletion convergence;
- backup size, restore time, index rebuild time and post-restore suppression lag;
- operator effort: upgrades, schema migration, provider outage, worker stuck jobs, tenant export and incident response.

A “single memory API” can conceal multiple backing stores and asynchronous pipelines. Prefer a smaller topology unless measured quality or scale requires more.

---

## 8. Benchmark Proposal / 基准测试提案

### 8.1 Benchmark design / 基准设计

**Wave 1 candidates:** Brain baseline (SQL + lexical, no product), Mem0 OSS, Graphiti, Hindsight. All run on the same hardware, model provider, corpus and token budget. Product-managed cloud is a separate cost/data-residency track.

**Dataset strata:**

1. Stable user preference and profile facts.
2. Corrections and changed facts with valid-time boundaries.
3. Contradictory statements from different sources and confidence levels.
4. Entity aliases, homonyms, merge/split ambiguity.
5. Long conversations with delayed relevant details.
6. Structured JSON and unstructured message mixtures.
7. Cross-agent shared/private scopes and attempted cross-scope retrieval.
8. Forget requests followed by delayed jobs, stale index queries and restore simulation.
9. Prompt-injection strings embedded in memory content.
10. Multilingual and mixed-language names/text.

### 8.2 Metrics / 指标

| Dimension | Metric |
|---|---|
| Extraction | Fact precision/recall/F1; unsupported-claim rate; omission rate |
| Entity resolution | Pairwise precision/recall; false merge and false split rate |
| Temporal | Valid-time accuracy; point-in-time query accuracy; supersession correctness |
| Provenance | Evidence-link coverage; source-span accuracy; orphan derivative rate |
| Contradiction | Detection precision/recall; silent-overwrite rate; conflict preservation |
| Retrieval | Recall@k, nDCG@k, MRR, answer-support precision, stale/forgotten leakage |
| Ranking | Relevance and source-quality calibration; policy violation count |
| Forget | Time to suppression; late-write resurrection count; stale replica leakage; restore leakage |
| Security | Cross-scope retrieval leakage; prompt-injection success rate; unauthorized export count |
| Operations | p50/p95/p99 latency, throughput, model tokens, cost per 1k events |
| Lifecycle | Duplicate work, lost work, unknown outcome recovery, retry idempotency |
| Applied | Brain-owned only; verify product cannot fabricate or bypass final-request evidence |

### 8.3 Gate criteria / Gate 验收门槛

- Any cross-scope leakage, post-fence publication, forgotten-item retrieval after authoritative suppression, or fabricated Applied proof is a **hard fail**.
- Extraction quality must be compared against a human-labeled gold set; no vendor leaderboard alone passes.
- Product must support export and reproducible rebuild, or lock-in is explicitly accepted.
- Deletion semantics and backup/restore behavior must be documented and fault-tested before any production data.
- No product is eligible for production integration until exact version, license, threat model, adapter contract and rollback plan are reviewed.

No numeric threshold is set because project SLOs, dataset and risk appetite have not been approved.

---

## 9. Open Questions / 未决问题

| ID | Question | Owner / decision authority | Closure evidence |
|---|---|---|---|
| PF-01 | What is the canonical B Fact/Claim representation and what candidate fields may be mapped? | B | Approved exact-version schema/ADR; Fact/Claim blocker resolved |
| PF-02 | What exact D ProducerWork/ForgetFence API and linearization points govern product adapter writes? | D | Owner-approved contract + race/fault conformance |
| PF-03 | What is the E ingress/derivation identity and retry protocol for external extraction jobs? | E | Exact idempotency/lease/staging/recovery contract |
| PF-04 | What I principal/scope mapping and revocation checks apply to product tenants/banks/graphs? | I | Owner-approved identity mapping and negative/race tests |
| PF-05 | Which Storage topology and transaction boundary is available to commit canonical proposals? | Storage + D/E | L4 decision and physical proof; do not infer from product backend |
| PF-06 | What constitutes complete Evidence lineage and retention for product-derived observations? | B/D/I | Evidence contract and deletion/retention policy |
| PF-07 | How does the Brain Adapter enforce retrieval suppression across product indexes and caches? | F + D/I | Stale-index, race and restore tests |
| PF-08 | What exact final inference boundary emits Applied proof? | C/G/H | Frozen contract, executable adapter evidence and tests |
| PF-09 | Is Python sidecar acceptable for initial local-first deployment and target platforms? | A + engineering owner | Measured packaging/latency/resource and security evidence |
| PF-10 | What workload profile, corpus, SLO, data residency and budget govern product selection? | Project authority | Approved benchmark envelope and operational constraints |
| PF-11 | Is managed Zep/Hindsight service acceptable for sensitive source data? | I + legal/security authority | Data-processing, region, retention, export and deletion review |
| PF-12 | What is the exact release/tag/commit and full license/SBOM for each chosen product? | Research + release/security | Reproducible dependency manifest, SBOM, license and CVE audit |

### 9.1 ADR recommendation / ADR 建议

**ADR-PROPOSAL-001 (proposed only): Non-authoritative External Memory Projection and Adapter Boundary.**

Proposed decision statement:

- Brain remains sole authority for Canonical Memory Truth, Evidence/Provenance semantics, Authorization, Forget, Lifecycle and Context Applied evidence.
- External memory products may be used only as replaceable extraction, graph, consolidation, ranking or retrieval projections behind an adapter.
- Product outputs are untrusted proposals/candidates and cannot publish canonical state.
- All reads and writes are revalidated against Brain scope, authorization, lifecycle and Forget state.
- Product deletion acknowledgements are downstream evidence, never Brain Forget terminal proof.
- Product data must be exportable/rebuildable; otherwise lock-in and non-rebuildability require explicit risk acceptance.

This ADR is **not approved** and should be reviewed by A/B/C/D/E/F/G/H/I/Storage as applicable. It does not alter their contracts.

---

## 10. Acceptance Criteria / 验收标准

This research session is complete for Draft submission only when all of the following are satisfied:

- [x] Exact main HEAD and README baseline captured.
- [x] PR #45, #56 and #73 read and their statuses/limitations recorded.
- [x] Product scope expanded beyond Mem0/Zep/Letta to Graphiti, Hindsight and LangMem.
- [x] Official documentation and selected source files/implementation metadata inspected.
- [x] Fourteen capability adoption decisions recorded.
- [x] Authority boundary, Forget, provenance, security and Applied risks explicitly analyzed.
- [x] Benchmark plan and open questions recorded.
- [ ] Exact latest release/tag/commit re-pinned for every candidate.
- [ ] Complete source-code path review and package/transitive SBOM/license/CVE audit for every finalist.
- [ ] Brain adapter prototype and fault-injection suite executed.
- [ ] Human-labeled benchmark corpus and project workload/SLO approved.
- [ ] Independent review of this exact Draft PR completed.
- [ ] Relevant Owners explicitly accept any proposed contract touchpoints.

**Current result: PARTIAL — suitable for review and planning, not production adoption.**

**当前结果：部分完成——可进入研究审查和实验规划，不构成生产采用批准。**

---

## Appendix A — Primary official sources / 官方一手来源

### Mem0
- Repository: https://github.com/mem0ai/mem0
- Core implementation: https://github.com/mem0ai/mem0/blob/main/mem0/memory/main.py
- Architecture: https://github.com/mem0ai/mem0/blob/main/skills/mem0/references/architecture.md
- API reference: https://github.com/mem0ai/mem0/blob/main/skills/mem0/references/api-reference.md
- OSS REST API: https://github.com/mem0ai/mem0/blob/main/docs/open-source/features/rest-api.mdx

### Graphiti / Zep
- Graphiti repository: https://github.com/getzep/graphiti
- Graphiti README: https://github.com/getzep/graphiti/blob/main/README.md
- Graphiti package/dependencies/license: https://github.com/getzep/graphiti/blob/main/pyproject.toml
- Zep Graph overview: https://help.getzep.com/graph-overview
- Adding Episodes: https://help.getzep.com/graphiti/core-concepts/adding-episodes
- Graphiti overview: https://help.getzep.com/graphiti/getting-started/overview

### Letta
- Letta repository: https://github.com/letta-ai/letta
- Letta Code repository: https://github.com/letta-ai/letta-code
- Memory & dreaming: https://docs.letta.com/configuration/memory
- MemFS docs source: https://github.com/letta-ai/letta-docs-md/blob/main/concepts/memfs/index.md
- Memory filesystem implementation: https://github.com/letta-ai/letta-code/blob/main/src/agent/memory-filesystem.ts

### Hindsight
- Repository: https://github.com/vectorize-io/hindsight
- API methods: https://github.com/vectorize-io/hindsight/blob/main/skills/hindsight-docs/references/developer/api/main-methods.md
- Best practices: https://github.com/vectorize-io/hindsight/blob/main/skills/hindsight-docs/references/best-practices.md
- Installation: https://github.com/vectorize-io/hindsight/blob/main/skills/hindsight-docs/references/developer/installation.md
- Storage: https://github.com/vectorize-io/hindsight/blob/main/hindsight-docs/docs/developer/storage.md
- Operations: https://github.com/vectorize-io/hindsight/blob/main/skills/hindsight-docs/references/developer/api/operations.md
- External PostgreSQL compose: https://github.com/vectorize-io/hindsight/blob/main/docker/docker-compose/external-pg/docker-compose.yaml

### LangMem
- Repository and README: https://github.com/langchain-ai/langmem
- LangGraph persistence: https://docs.langchain.com/oss/python/langgraph/persistence

---

## Appendix B — Evidence status / 证据状态

| Claim group | Status | Reason |
|---|---|---|
| Project main HEAD / README | VERIFIED | Direct GitHub readback in this session |
| PR #45/#56/#73 metadata and stated status | VERIFIED | Direct GitHub PR readback; PR descriptions treated as claims, not proof |
| Current D/E/I/Storage/Applied boundaries | PARTIALLY VERIFIED | Exact current remediation branch artifacts read; role-simulated proposal, not Owner acceptance |
| Mem0 documented API and architecture | PARTIALLY VERIFIED | Official docs/source inspected; exact latest release not re-pinned |
| Graphiti temporal/episode behavior and package metadata | VERIFIED for documented/library behavior | Official docs, README and pyproject inspected; no Brain conformance |
| Zep managed service behavior | PARTIALLY VERIFIED | Official docs inspected; commercial contract and operational guarantees not audited |
| Letta MemFS behavior | PARTIALLY VERIFIED | Official docs and source path inspected; exact release/license boundaries require audit |
| Hindsight retain/recall/reflect and storage | PARTIALLY VERIFIED | Official repo/docs/source guides inspected; exact current release/dependency lock not pinned |
| LangMem behavior | PARTIALLY VERIFIED | Official README inspected; release/source and transitive dependency review incomplete |
| Any product's Brain-grade Forget/Applied/security authority | UNVERIFIED | No candidate-specific end-to-end proof; cannot infer from marketing/API documentation |
| Performance, cost, production suitability | UNVERIFIED | No comparable workload benchmark run |
