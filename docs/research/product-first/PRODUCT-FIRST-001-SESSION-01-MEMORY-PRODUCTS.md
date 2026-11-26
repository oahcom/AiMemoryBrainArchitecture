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
- **I:** `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` (not restored on main; see AID-2026-107 §10), Blob `54bab0484bd232a5a258e65e34cc7425288b39a6`. I owns principal/workload/delegation trust, PolicyDomain, authorization, PermissionEpoch, revocation ordering, issuer/key status and authorization terminal proof. Authorization is necessary but not sufficient for visibility.
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


---

# 完整中文对应版本 / Full Chinese Companion

> 本节与前述英文研究正文具有相同的研究结论、能力决策、权威边界和未决事项。英文版本中的产品能力细节、证据状态和限制同样适用于本节；本节不是独立的技术批准。

## 1. 执行摘要

### 1.1 结论

**建议采用“产品辅助、Brain 保持权威”的架构，不建议使用任何单一 Memory 产品替代 Brain。**

最值得研究的产品具有互补性，而不是互相替代：

1. **Graphiti（Apache-2.0）**：最贴近时态实体/关系抽取、Episode 来源关联、事实随时间演化和图混合检索。适合作为派生投影，不是 Canonical Memory Truth。
2. **Mem0（Apache-2.0）**：适合对话事实抽取、记忆更新/去重、向量与元数据检索以及 SDK 集成。其抽象不能替代 Brain 的 Event、Fact、Claim、Evidence 和 Lifecycle 类型契约。
3. **Hindsight（MIT）**：适合完整 Memory Pipeline 对比实验，涵盖 retain/recall/reflect、证据关联 Observation、时态/图/语义检索和 PostgreSQL 部署。其观察和综合结论仍然不是权威事实。
4. **Letta / MemFS**：适合 Agent 自己管理可编辑记忆文件、Git 历史、程序性记忆和自我改进流程，不是通用多 Agent Canonical Memory 权威。
5. **LangMem（MIT）**：可组合的抽取与整合工具包，可与 LangGraph Store 集成；它是算法和工具参考，不是 Brain 治理系统。
6. **Zep Cloud**：提供托管 Context Graph 能力，但服务及其数据库属于专有托管边界，会引入供应商、数据驻留和权威依赖；必须与 Apache-2.0 的 Graphiti 开源库分开评估。

目前没有证据证明任何候选产品同时满足 Canonical Truth、独立 Evidence/Provenance 权威、Authorization/Revocation、Forget Fence、跨系统 Lifecycle 和最终推理请求 Applied Evidence。上述能力仍需 Brain 自己组合并保持权威。

**不建议任何产品直接成为初始 System of Record。** 风险最低的下一步，是在生产架构之外建立一次性、非权威 Adapter 实验，用相同标注语料比较 Graphiti、Mem0 和 Hindsight，同时保留 Brain 自有记录和生命周期权威。

### 1.2 明确不声称

- 本研究没有运行 Brain 原型、性能基准、负载测试、迁移演练、安全审计或端到端符合性测试。
- 不把厂商宣传和厂商基准测试当作独立验证结果。
- 版本信息是研究快照，不是依赖锁定；正式采用前必须重新核验精确 Release/Commit、传递许可证、CVE 和 SBOM。
- 本报告不批准 ADR、不选择数据库或部署拓扑，也不冻结任何 Owner 契约。

## 2. 当前架构基线

### 2.1 精确基线与既有研究

本次从 GitHub 读取的 main HEAD 为 `b3c666e67982cb3d3374e759cfb6552c7765aacb`。README 表明仓库当前是架构定义仓库，Runtime Implementation 尚未开始，这是有意状态。

- PR #45：历史技术研究，仍为 Open/Draft，基线和 Head 属于历史快照。
- PR #56：对 #45 的独立审查，仍为 Open/Draft，结论为 REVISE / NOT YET PROVEN；发现包括源当前性、Restate Server 许可证披露和双语语义一致性问题。
- PR #73：当前源整改包，仍为 Open/Draft；其自身明确说明这是角色模拟的整合/整改，不是真实 Owner 签名或批准。

本报告不重复这些 PR 的整体技术选型工作，而是新增 Mem0、Graphiti/Zep、Letta/MemFS、Hindsight、LangMem 对 14 项 Memory 能力的产品级比较。

### 2.2 产品不得越权的架构不变量

1. Canonical Memory Truth 归 Brain/D 与 Storage，不归产品的 Memory 表、Graph 或 Vector Store。
2. Evidence/Provenance 的语义权威属于 Brain。产品 Source Pointer、Episode ID、Quote 或 Confidence 只是输入材料，不构成来源权威或真实性证明。
3. Principal、PolicyDomain、PermissionEpoch、Authorization 和 Revocation 属于 Owner I。产品的 user_id、tenant_id、bank_id 或 graph_id 不是授权凭证。
4. Forget 权威与 Fence 顺序属于 Owner D/I/Storage。供应商 DELETE API 不是 Forget 协议。
5. Producer Admission、Dependency Inventory、Publication Participation、Lifecycle Terminality 属于 Brain。
6. Context Applied Evidence 权威位于 C/G/H 推理边界。产品返回搜索结果、提交 Agent Memory 文件或声称 Prompt Enriched，都不能证明最终推理请求实际应用了指定上下文。
7. 检索到的 Memory 是不可信数据，不能提升为 System/Developer 指令。
8. Graph、Embedding、Index、Cache、Summary 和产品 Memory Object 应作为可替换派生数据，除非 Brain 的正式契约另有规定。

### 2.3 当前 Owner 契约增量

当前整改分支中读取到的提案证据表明：

- **D** 拥有 ProducerClass 准入、ProducerWork 注册、RegistrationReceipt/Sequence、ForgetFence 顺序、依赖/血缘清单、PublicationParticipant 和终态；精确 Owner 批准、可调用 API 和符合性仍 OPEN。
- **E** 拥有 CompileIntent、Ingress Receipt、不可变输入包、DerivationRun/Attempt/Lease、私有 Stage 和编译恢复编排。Queue ACK 或本地 Published/Completed 标签不是跨 Owner 证明。
- **I** 拥有 Principal/Workload/Delegation 信任、PolicyDomain、Authorization、PermissionEpoch、Revocation 顺序、Issuer/Key 状态和授权终态证明。授权是必要条件，不是可见性的充分条件。
- **Storage** 的 L1 逻辑序列化提案选择一个 Canonical Memory Authority 对应一个逻辑 Serializable Transaction Domain；L4 物理引擎/部署仍 OPEN。不能从中推断采用任何 Memory 产品后端。
- **C/G/H Applied**：Issue #3 仍为 Applied Contract Frozen = NO、Test Executed/Passed = NO/NO、Implementation Verified = NO。
- **B Fact/Claim** 仍为 ADR-BLOCKED。

因此，产品集成只能从派生数据边界开始，不能用产品能力来宣称关闭 D/E/I/Storage 或 Applied 阻塞项。

## 3. 产品能力矩阵结论

状态说明：VERIFIED 表示官方文档/源码支持所述产品行为；PARTIALLY VERIFIED 表示存在相应功能，但完整性或生产保证尚未证明；UNVERIFIED 表示尚未证明满足 Brain 的特定要求。产品功能不等于 Brain 契约证明。

| 产品 | 已观察到的优势 | 关键缺口 | 研究定位 |
|---|---|---|---|
| Mem0 OSS | LLM 事实抽取、更新/去重、SQL 元数据/历史、向量和实体检索、删除 API | 多存储一致性、完整 Evidence 血缘、跨索引/备份 Forget Fence 未证明 | 高价值 Adapter 候选 |
| Graphiti | Episode 增量摄取、实体/关系抽取、时态边、自定义 Ontology、图/语义/BM25 混合检索 | 来源关联不等于来源正确；没有 Brain 授权、Forget 和 Applied 权威 | 语义匹配度最高 |
| Zep Cloud | 托管 Context Graph、Episode/Edge 来源关联、时态检索 | 专有托管服务，数据驻留、导出、删除 SLA 和锁定风险需审查 | 暂缓托管采用 |
| Letta / MemFS | Agent 级记忆文件、Memory Blocks、Git 历史、Dreaming/整合 | 不提供完整事实/证据模型、跨 Agent 授权和全局 Forget | Agent 工作区候选 |
| Hindsight | retain/recall/reflect、Observation 整合、语义/BM25/图/时态检索、重排 | Bank 隔离不等于 I 授权；产品删除不等于跨系统 Forget | 第一波基准候选 |
| LangMem | 热路径工具、后台 Memory Manager、抽取与整合 | 依赖外部 Store；无 Brain Evidence、Forget、Lifecycle 或 Applied 权威 | 算法工具候选 |

### 3.1 Mem0

Mem0 是通用 Agent Memory Layer。官方文档和源码显示其 Memory.add 流程会进行抽取/更新，并提供 Search、History、Update、Delete 和按 Scope 删除能力。其架构组合 SQL Facts/Metadata、Vector Store 和 Entity Store。

此前 PR #45 记录了 Mem0 v2.2.1、Apache-2.0 和源码 Tree SHA `f1791daa86d469249c9b002f62644d58a1eb96a0`，涉及 `mem0/memory/main.py`、`mem0/memory/storage.py` 和 Vector Store Adapter。本 Session 重新读取了官方 API 和架构资料，但没有重新锁定当前最新 Release。

采用建议：**WRAP / EXTEND**。只用于提取或检索派生服务；不能成为 Canonical Store。多存储架构会增加跨存储一致性和删除协调成本。

### 3.2 Graphiti 与 Zep

Graphiti 是开源时态 Context Graph 框架；Zep 是基于 Graphiti 派生图能力的托管 Context 平台。

Graphiti 支持 Text/Message/JSON Episode、实体和关系抽取、时态边、自定义实体/关系类型，以及 Semantic、BM25 和 Graph Traversal 混合检索。Zep 文档说明图由 Entity Nodes、Entity Edges 和 Episodic Nodes 构成；Edge 保存来源 Episode 和有效时间。文档同时明确：Provenance 只识别来源数据，不保证来源或派生事实正确。

此前 PR #45 记录 Graphiti v0.31.2、Apache-2.0、Tree SHA `869c1b279e01a2767a464581e1cb657ce0e39271`，并检查 `graphiti_core/graphiti.py`、`nodes.py`、`edges.py`、Search 和 Driver 实现。本 Session 重新读取了官方 README、文档和 pyproject。当前 pyproject 显示 Python >=3.10、Neo4j 核心依赖，以及 FalkorDB/Neptune/模型供应商可选依赖；Kuzu Extra 因上游项目不再维护而被标记为弃用。

采用建议：Graphiti **EXTEND / WRAP**，只做可替换的时态图投影。Zep Cloud **DEFER**，待托管服务合同、数据驻留、删除和导出条件通过审查后再评估。

### 3.3 Letta / MemFS

Letta Code 使用 Git-backed Memory Filesystem，提供 Agent 级 Memory Blocks 和外部 Memory Files。Agent 可用常规文件工具编辑记忆，并用 Git 查看历史。官方文档描述了 Dreaming 后台整合；Memory 修改提交并重新编译后才会影响后续上下文，不会改变已经开始的当前推理请求。

此前 PR #45 记录 Letta Code v0.34.63、Apache-2.0、Tree SHA `b622fb1bc0941981e08da5ec2b2736d897e9bde1`，检查 `memory-filesystem.ts`、`memory-git.ts` 等源码。当前 Letta 项目说明活跃代码已转至 `letta-ai/letta-code`，旧 Letta V1 API Server 已归档。必须区分 Letta Code、Server、SDK 和 Cloud 的许可证及服务条款。

采用建议：**WRAP** 为 Agent 自有工作区记忆，不作为 Brain Canonical Memory。

### 3.4 Hindsight

Hindsight 提供 retain、recall、reflect 三个核心操作。Retain 摄取对话/文档并抽取事实、实体和关系；Recall 组合 Semantic、BM25、Graph、Temporal 搜索与重排；Reflect 使用 LLM 在记忆上进行综合推理。Observation 文档描述了去重、证据关联和基于新证据的修订。Memory Bank 用于隔离不同 Agent/User/上下文。

本 Session 检查了官方 README、API 方法、异步 Operation、安装、Storage 和 Docker Compose 文档。仓库声明 MIT。生产存储主要使用 PostgreSQL + pgvector，也提供 Oracle AI Database 企业方案；pg0 嵌入式 PostgreSQL 用于开发，不建议生产。支持 REST、Python、Node、Go 和 MCP。精确最新 Release/Commit 和传递依赖许可证仍需锁定。

采用建议：**EXTEND / WRAP**，作为整合与检索的强基准候选或可选派生服务；Observation 不得成为 Canonical Truth，Bank 隔离不能替代 I 的授权，删除不能替代 D/I/Storage 的 Forget Fence。

### 3.5 LangMem 与其他候选

LangMem 提供 Hot-path Memory Tools 和后台 Memory Manager，支持抽取、整合、更新，并集成 LangGraph Store。它是工具包而非独立权威服务。采用建议 **EXTEND** 算法参考，生产集成 **DEFER**，除非 Python/LangGraph Sidecar 的成本得到证明。

Hermes Agent 的 Provider/Memory Adapter 模式可供参考，但它是 Agent Runtime，不是 Brain。LangGraph Store/Checkpointer 可借鉴 Thread State 与跨 Thread Memory 的区分。GraphRAG 更偏静态文档语料，不作为第一波时态 Agent Memory 候选。Qdrant、pgvector、Tantivy 属于检索基础设施，不是 Memory Authority。

## 4. 14 项能力采用决策

| 能力 | 决策 | 中文理由 |
|---|---|---|
| 1. Memory Ingestion | **WRAP** | 用 Adapter 接入对话、消息、JSON 和文档；Brain 自己校验 Principal、Scope、幂等、Admission 和 Accepted Receipt。产品 ACK 不是 Brain 接受证明。 |
| 2. Memory Extraction | **EXTEND** | 使用 Mem0/Graphiti/Hindsight 生成候选；Brain 校验类型、证据、权限和血缘后才允许 Canonical Commit。 |
| 3. Entity Resolution | **EXTEND** | 借用 Graphiti/Mem0/Hindsight 的实体链接；Canonical Entity ID、Merge/Split、Alias 和冲突裁决归 Brain。 |
| 4. Fact / Claim Modeling | **BUILD** | 产品结构不能替代 B 的领域模型；Fact/Claim ADR 仍阻塞。 |
| 5. Temporal Memory | **EXTEND** | 借用 Graphiti 时态边/Hindsight 时间检索；有效时间、记录时间、事件顺序和 Supersession 由 Brain 定义。 |
| 6. Provenance | **BUILD** | Episode、Quote、History 是来源线索；Evidence Identity、完整派生血缘、完整性、授权和保留策略由 Brain 拥有。 |
| 7. Contradiction Detection | **EXTEND** | 产品提出矛盾候选；Brain 保留竞争 Claim、来源、时间和裁决状态，不得静默覆盖。 |
| 8. Memory Consolidation | **EXTEND** | 使用 Observation、Dreaming、Dedup 等生成派生结果；必须保留完整血缘和幂等 Derivation ID，不得删除原始证据或完成 Forget。 |
| 9. Memory Retrieval | **WRAP** | Graphiti/Hindsight/Mem0 可生成候选；Brain 在排序/激活前复查授权、Canonical 状态、时效和 Forget 抑制。 |
| 10. Memory Ranking | **EXTEND** | 可使用产品 Reranker；Brain 决定策略排序和激活，排名不能覆盖授权、Forget 或认知状态。 |
| 11. Forget / Deletion | **BUILD** | 产品 DELETE 仅是下游清理；D/I/Storage 拥有操作身份、授权、目标清单、Fence、Barrier、终态证明、恢复和 Restore Fencing。 |
| 12. Multi-Agent Sharing | **WRAP** | 可利用 Agent Repo、Shared Graph、Bank 或 Scope；Brain/I 决定 Principal、Delegation、Policy 和共享授权。 |
| 13. Memory Lifecycle | **BUILD** | Brain 拥有 ProducerWork、Lease/Fencing、Dependency Registration、Publication Participation、Terminality 和恢复。 |
| 14. Memory Quality Evaluation | **EXTEND** | 借用 LongMemEval 和产品基准工具，但增加 Truth、Provenance、Forget、Authorization、Temporal Leakage 和 Applied 专项指标。 |

本报告没有对 14 项中的任何一项建议将外部产品整体 ADOPT 为系统记录权威。未来若要改变，必须先通过固定版本的独立端到端符合性验证，并取得相关 Owner 明确批准。

## 5. 架构影响与推荐集成方式

建议增加的是**非权威 Product Adapter 边界**，而不是新增产品权威：

1. Brain 按自己的契约接受并持久化标识 Source Event。
2. Adapter 仅发送经过最小化/脱敏的派生数据，并携带稳定 Brain Source/Evidence 引用和 Scope 元数据。
3. 产品执行抽取、图构建、Embedding、整合或检索。
4. Adapter 将产品输出映射为 Brain 的 Typed Proposal；产品原始对象只作为外部引用。
5. Brain 校验 Scope、Authorization、Schema、Source Lineage、Temporal Semantics、Conflict 及当前 Forget/Lifecycle Fence。
6. 只有 Brain 的 Canonical Transaction 可以发布已接受的 Canonical Asset。
7. 检索 Adapter 返回候选 ID/Score/Source Pointer；Brain 在 Context Planning 前重新校验。
8. Forget 向产品传播为下游目标，但 Brain 是否完成取决于权威目标清单和所需确认/协调结果。

第一阶段只比较 Brain SQL+Lexical Baseline、Mem0 OSS、Graphiti、Hindsight。使用固定匿名数据集和相同模型/Token 预算。Letta 与 LangMem 放到第二波，分别评估 Agent Workspace 和 Toolkit 场景。不得把真实敏感数据或 Canonical Write Credential 交给产品。

## 6. 安全、Forget 与 Provenance

### 6.1 安全边界

- Brain Principal/Workload/Delegation 映射为不透明产品 Scope；产品调用者传入的 user_id/bank_id/agent_id/graph_id 不能作为身份凭证。
- 任何受保护读写必须由 I 授权；产品 RBAC 仅作为纵深防御。
- 只发送必要数据；审查模型供应商出站、保留、日志、备份、区域和分包商。
- 所有 Memory、Graph Fact、Summary、Observation 和 Memory File 都是不可信数据，不得进入特权指令通道。
- 在 Ingestion、Extraction、Graph Traversal、Vector Search、Rerank、Reflect 和 Export 的每个阶段测试跨租户泄漏。
- 产品只能使用受限、短期 Adapter Credential，不能获得 Storage/I 签名密钥或 Canonical DB 的无限制权限。

### 6.2 Forget

产品 DELETE 最多只能证明产品在自身语义下接受或完成了本地删除，不能证明：

- 抽取事实、关联实体、图边、Summary、Embedding 和 Cache 全部删除；
- 异步 Job/Retry 已被 Fence，无法重新创建被遗忘数据；
- Replica、Export、Audit Log、Object Store、Snapshot 和 Backup 满足擦除语义；
- 旧索引/副本不会再次返回已 Forget 项；
- Restore 不会从旧 Snapshot 复活数据；
- 下游 Agent Context/Applied 已完成协调。

Adapter 必须绑定 Brain Forget Operation ID 和不可变 Digest，幂等执行，Digest 冲突失败关闭，关闭或隔离相关写入，枚举派生对象和异步 Job，对超时/丢 ACK/部分删除/UNKNOWN 保持未解决状态，并在恢复和重建前重放 Forget/Revocation 状态。

**当前没有候选产品被验证满足这一跨系统协议。Forget 必须 BUILD。**

### 6.3 Provenance 与 Applied

Graphiti Episode 能关联派生 Node/Edge，Hindsight Observation 能关联支持 Memory/Quote，Mem0 History 能追踪记忆变化，Letta Git History 能追踪文件修订。但这些都不等于 Brain Evidence Authority 或完整 Fact-Level Lineage。

Brain 应保存来源 Event/Evidence ID、内容 Digest、允许保留的 Source Span/Quote、Extractor/Model/Prompt Version、Derivation Run ID、产品版本/配置、时间断言、验证结果及 Supersession/Contradiction 链路。此处是研究映射建议，不是擅自新增 B/D 契约。

所有产品都不能证明 Brain Adapter 组装的最终推理请求确实应用了指定上下文。产品的“Memory Returned”“Context Updated”“Prompt Enriched”均不是 C/G/H Final-request Applied Attestation。

## 7. 许可证、部署和成本风险

- **Mem0 OSS：** Apache-2.0；Python；SQL、Vector、Entity Provider；可自托管 REST/Docker。主要风险是多存储一致性、Provider 出站、Python Sidecar 和托管 API 条款。
- **Graphiti：** Apache-2.0；Python >=3.10；Neo4j 核心依赖，FalkorDB/Neptune 等可选；需要图数据库和模型供应商。需注意 Kuzu Extra 已弃用。
- **Zep Cloud：** 专有托管服务；需审查数据驻留、保留、定价、导出、删除 SLA 和供应商锁定。
- **Letta Code：** 既有源码快照记录 Apache-2.0；Node/TypeScript；本地 App Server 或 Cloud；必须分别核查 Code、Server、SDK 和 Cloud 条款。
- **Hindsight：** MIT；Python API；生产 PostgreSQL + pgvector（另有 Oracle 企业方案）；需要模型 Provider、Docker/Helm 和数据库运维。
- **LangMem：** MIT；Python；可集成 LangGraph Store；需要外部存储和模型 Provider。

仓库许可证不等于完整法律意见。必须逐包核查依赖、模型权重、托管服务条款、数据集、SBOM 和 CVE。成本必须通过实验测量 CPU/RAM/磁盘、Token/事件、重试放大、服务数量、P95/P99、删除收敛时间、Backup/Restore 和运维工时。

## 8. 基准测试提案

第一波候选：Brain SQL+Lexical Baseline、Mem0 OSS、Graphiti、Hindsight。数据集覆盖稳定偏好、纠正和事实变化、矛盾来源、实体别名/同名、长对话延迟召回、JSON/自然语言混合、跨 Agent 共享/私有、Forget 后延迟任务和 Restore、Prompt Injection、多语言。

指标包括：

- Extraction Precision/Recall/F1、Unsupported Claim Rate；
- Entity Pairwise Precision/Recall、False Merge/Split；
- Valid-time Accuracy、Point-in-time Query Accuracy；
- Evidence Link Coverage、Source Span Accuracy、Orphan Derivative Rate；
- Contradiction Detection、Silent Overwrite Rate；
- Recall@k、nDCG@k、MRR、Forgotten/Stale Leakage；
- Forget Suppression Time、Late-write Resurrection、Restore Leakage；
- Cross-scope Leakage、Prompt Injection Success；
- P50/P95/P99、吞吐、Token 和每千条事件成本；
- Duplicate/Lost Work、UNKNOWN Recovery、Retry Idempotency。

任何跨 Scope 泄漏、Fence 后发布、权威抑制后仍检索出已 Forget 项或伪造 Applied Proof 都是硬失败。没有项目 SLO 和标注集之前不虚构数值门槛。

## 9. 未决问题与 ADR 建议

未决问题包括：B Fact/Claim Schema；D ProducerWork/ForgetFence API；E 外部抽取任务幂等和恢复；I 产品 Scope 与 Principal 映射；Storage L4 物理拓扑；Evidence 血缘/保留；F 索引/Cache 抑制；C/G/H 最终 Applied 边界；Python Sidecar 可接受性；实际 Workload/SLO/预算；Zep/Hindsight 托管服务数据治理；精确 Release/Commit/SBOM/CVE。

建议提出但不批准：

**ADR-PROPOSAL-001：非权威外部 Memory Projection 与 Adapter 边界。**

建议原则：Brain 是 Canonical Truth、Evidence/Provenance、Authorization、Forget、Lifecycle 和 Context Applied Evidence 的唯一权威；外部产品仅作为可替换抽取、图、整合、排序或检索投影；产品输出是非可信 Proposal/Candidate；所有读写由 Brain 复查 Scope/Authorization/Lifecycle/Forget；产品删除确认不是 Forget 终态证明；产品数据必须可导出和重建，否则显式接受锁定风险。

此 ADR 仍是提案，需 A/B/C/D/E/F/G/H/I/Storage 按影响范围审查，不改变任何 Owner 契约。

## 10. 验收状态

已完成：精确 main HEAD/README、PR #45/#56/#73 核验、扩展产品名单、官方文档与选定源码/元数据检查、14 项能力决策、安全/Forget/Provenance/Applied 分析、基准提案和未决问题。

尚未完成：所有候选精确最新 Release/Commit 锁定；完整源码路径审查和 SBOM/许可证/CVE；Brain Adapter 原型及故障注入；人工标注数据集和 SLO；独立审查本 Draft PR；相关 Owner 对契约接触点的明确接受。

**当前结论：PARTIAL。可进入研究审查和实验规划，不构成生产采用批准。**
