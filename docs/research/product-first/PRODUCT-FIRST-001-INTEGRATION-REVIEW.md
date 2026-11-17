# PRODUCT-FIRST-001 — Unified Integration & Independent Review
# PRODUCT-FIRST-001 — 统一整合与独立审查

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Role: Principal Product-First Architecture Owner
- Review date: 2026-11-18
- Review branch base: `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Status: **INTEGRATION REVIEW / NON-NORMATIVE / DRAFT**
- Decision status: **PROPOSED; NO ADR APPROVED; NO TECHNOLOGY FROZEN; NO IMPLEMENTATION AUTHORIZED**
- Scope: PRODUCT-FIRST-001 Sessions 01–06, current-main drift, cross-session conflicts, build-vs-buy decisions, acceptance gates.

---

## 1. Executive decision / 执行结论

**Overall recommendation: retain the Brain's semantic authorities; simplify the first physical deployment to one modular Rust monolith, one selected transactional authority, one SQL-backed durable-work mechanism, one policy-decision implementation, and no mandatory external vector/graph/cache/broker/workflow services. Adopt mature products behind narrow replaceable adapters only after a measured requirement and conformance evidence.**

**总体建议：保留 Brain 的语义权威；首期物理部署简化为一个模块化 Rust 单体、一个经选型的事务权威、一个 SQL 持久化工作机制、一个策略决策实现；不强制引入外部向量库、图数据库、缓存集群、消息总线或通用 Workflow 服务。成熟产品只能通过窄接口、可替换 Adapter 接入，并且必须先有可测量需求和符合性证据。**

This is a consolidation of research proposals, not an architecture approval. The six sessions provide useful desk research, but none supplies a runnable Brain adapter, representative benchmark, integrated fault-injection result, production security audit, or end-to-end Forget/Applied conformance proof.

本报告整合的是研究提案，不是架构批准。六个会话提供了有价值的案头研究，但没有交付可运行的 Brain Adapter、代表性基准、集成故障注入结果、生产安全审计，或端到端 Forget/Applied 符合性证明。

### Proposed top-level dispositions

| Area | Proposed disposition | Decision boundary |
|---|---|---|
| Brain domain semantics, Canonical Truth, Evidence/Provenance, Lifecycle, Forget | **BUILD / KEEP AUTHORITATIVE** | Non-delegable Brain/Owner authority |
| External memory extraction and retrieval | **WRAP / EXTEND** | Candidate generators and derived projections only |
| Temporal graph | **DEFER deployment; SPIKE only if needed** | Graphiti is optional projection, not truth |
| Durable execution | **WRAP** | SQL outbox/work table + bounded workers first |
| Temporal / Restate / DBOS | **DEFER** | Trigger only on demonstrated long-running, multi-host orchestration needs |
| Primary database | **TO_VALIDATE** | SQLite local profile vs PostgreSQL server profile; Storage L4 remains OPEN |
| Lexical search | **WRAP existing SQL engine first** | FTS5 or PostgreSQL FTS, selected by profile and corpus |
| Vector search | **DEFER / EXTEND later** | pgvector first evaluation; Qdrant only if measured scale/isolation need |
| Authorization PDP | **CANDIDATE: Cedar** | No adoption until fail-closed wrapper and conformance tests |
| OPA / OpenFGA | **DEFER** | Require demonstrated cross-service policy or relationship-graph need |
| Agent runtime | **DEFER product commitment; one bounded SPIKE** | LangGraph conditional candidate; no Brain-owned Agent framework |
| MCP | **ADOPT SELECTIVELY** | Tool ecosystem edge only; BMCP remains H-owned |
| Cache / broker / graph DB / search cluster | **DEFER** | Not part of mandatory first deployment |

---

## 2. GitHub baseline and evidence integrity / GitHub 基线与证据完整性

### 2.1 Current repository baseline

The repository API and `main` branch were refreshed during this review.

- Current `main` HEAD: `e52594f181d2edb77448adcfed64a0fbdffaf3aa`.
- Commit message: `revert accidental A review document on main; restore protected branch tree`.
- Current recursive Git tree: 126 entries; not truncated.
- README status: Architecture definition; implementation not started by design.
- TAB-001: v0.1, **CANDIDATE SYSTEM-WIDE BLUEPRINT — NOT A TECHNOLOGY FREEZE**.
- TAB-001 continues to recommend a modular Rust monolith, local-first operability, and deferral of distributed infrastructure until measured requirements justify it.

### 2.2 Current-main source-tree limitation

The current recursive tree does not contain the root-level normative directories listed by README for the detailed domain/runtime/protocol/storage/security/recovery/test specifications, including:

- `02-domain-model/`
- `03-memory-brain/`
- `04-memory-compiler/`
- `05-memory-runtime/`
- `06-memory-context/`
- `08-protocols/`
- `09-storage-and-index/`
- `10-security-and-governance/`
- `11-consistency-and-recovery/`
- `12-testing-and-acceptance/`

The README still maps these directories as the detailed documentation source of truth. This is a repository currentness / publication gap, not evidence that the corresponding Owner contracts do not exist. Session reports cite Owner-branch blobs and PRs for some of those contracts. Those branch blobs must remain explicitly identified as candidate or branch evidence until their authority, approval and exact-currentness are independently established.

**Consequence:** no product recommendation in this report may claim that a detailed Owner contract is present in current `main` merely because a Session report cited a branch Blob. The affected contract must be pinned to its live authoritative branch/PR and Owner disposition before implementation.

### 2.3 Six research PR inventory

All six PRODUCT-FIRST-001 PRs were found as Open/Draft and were based on the same historical main SHA `b3c666e67982cb3d3374e759cfb6552c7765aacb`, not the current HEAD above.

| Session | PR | Head SHA | Report scope | Review status |
|---|---:|---|---|---|
| 01 | [#74](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/74) | `ca754250b7ae349e54b2136b49a0414b4a4eaf36` | Memory products | Draft research |
| 02 | [#75](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/75) | `bf4c400ffc7489a2c3d063d296b2aad4361cbcea` | Durable execution | Draft research |
| 03 | [#78](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/78) | `3ca3e6d70c106c41a94cf28ed49c55b54a499893` | Storage/search | Draft research |
| 04 | [#76](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/76) | `77e542e0565c1bafa9d68996da68005a0b9fba72` | Security/governance | Draft research |
| 05 | [#77](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/77) | `eaebbaa631d5bb66fd0ba58bfc5f16f0f81b6096` | Agent runtime/integration | Draft research |
| 06 | [#79](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/79) | `b63f9188387a5b88a4ad690c9d9c47dbecb542f5` | Simplification/build-vs-buy | Draft research |

The six PRs each add one bilingual report. Their own declarations consistently state that no Brain prototype, representative workload benchmark, production security audit, or end-to-end conformance run is claimed.

### 2.4 Material review finding: Session 06 inventory is stale

Session 06 report says that individually verifiable final reports for Sessions 01–05 were not located in accessible prior-session records. However, PRs #74–#78 exist and were available in the repository PR inventory when this integration review was performed. Session 06's statement is therefore not a reliable inventory of repository deliverables and must be corrected or treated as stale. Its simplification recommendations remain reviewable, but its claimed dependency review was incomplete.

### 2.5 Evidence classification

- **VERIFIED:** repository metadata, current main SHA/tree, README/TAB-001 content, six PR metadata and report contents read back from GitHub.
- **PARTIALLY VERIFIED:** product capabilities described in the six reports from official docs/source inspection; cross-session architectural consistency.
- **UNVERIFIED:** exact latest release pins and full transitive SBOM/license/CVE review; Brain-specific workload performance; adapter correctness; end-to-end Forget/restore; Applied proof; production operational suitability.
- **NOT AUTHORIZED:** merge, technology freeze, Owner-contract replacement, production activation.

---

## 3. Cross-session reconciliation / 跨会话结论对账

### 3.1 Areas of agreement

1. **One semantic authority, many replaceable projections.** All memory, search, graph, runtime and workflow products must remain subordinate to Brain-owned authority.
2. **Logical A–I boundaries do not imply microservices or one crate per Owner.** Session 06's modular-monolith direction matches TAB-001 and Sessions 02/03/05.
3. **One transactional authority per Canonical Memory Authority.** Storage/D serialization semantics cannot be split merely to align with team or product boundaries.
4. **Derived indexes are rebuildable and Forget-aware.** A search/vector/graph/cache hit must be revalidated against canonical authorization, visibility and Forget state.
5. **Execution completion is not business completion.** A workflow ACK, job completion or queue delivery cannot establish Canonical Commit, Provider side effect, Context Applied or Forget terminality.
6. **Authorization, revocation and Forget are distinct authorities.** PDP evaluation, PEP enforcement, permission epoch, canonical Forget fence and storage visibility remain separately governed.
7. **BMCP remains the Brain protocol.** MCP may be used selectively at the external tool ecosystem edge through explicit adapters.

### 3.2 Reconciled decisions

| Capability | Final integrated proposal | Rationale / stop condition |
|---|---|---|
| Memory ingestion | **WRAP** | Adapter validates Brain identity/scope/admission; product ACK is not Accepted evidence |
| Memory extraction | **EXTEND** | Mem0/Graphiti/Hindsight may emit candidates; Brain validates and commits |
| Entity resolution | **EXTEND** | Reuse candidate linking; canonical identity merge/split remains Brain-owned |
| Fact/Claim semantics | **BUILD** | B owns domain semantics; Fact/Claim ADR remains blocked |
| Temporal graph | **DEFER / SPIKE** | Graphiti only if temporal graph queries outperform typed relational baseline |
| Provenance | **BUILD** | Episode/quote/history is source lineage input, not canonical Evidence authority |
| Contradiction handling | **EXTEND** | Products propose conflicts; Brain preserves competing claims and adjudicates |
| Consolidation | **EXTEND** | Derived output only; preserve immutable lineage and idempotent derivation identity |
| Retrieval | **WRAP** | Search returns candidates; Brain revalidates before disclosure/activation |
| Ranking | **EXTEND** | Product rerankers are advisory; policy and activation remain Brain-owned |
| Forget/deletion | **BUILD** | Product delete APIs cannot prove fencing, downstream completion or restore safety |
| Multi-agent sharing | **WRAP** | Product scopes are not principals or authorization grants |
| Lifecycle | **BUILD** | Producer admission, dependency registration, terminality and recovery remain Brain-owned |
| Quality evaluation | **EXTEND** | Add Brain-specific truth, lineage, Forget, authorization and Applied metrics |
| Durable jobs | **WRAP** | SQL outbox/work table, leases, attempts, bounded Tokio workers first |
| General workflow engine | **DEFER** | Adopt only with evidence of long-running, multi-host orchestration complexity |
| Primary persistence | **TO_VALIDATE** | Choose exactly one profile/engine per authority after Storage L4 and workload tests |
| Lexical search | **WRAP** | Native FTS first; compare tokenizer/relevance on multilingual labeled corpus |
| Vector search | **DEFER** | pgvector is first evaluation candidate after lexical baseline; Qdrant only if justified |
| Policy evaluation | **CANDIDATE: Cedar** | Fail-closed wrapper and I-owned activation/revocation required |
| Agent runtime | **DEFER / one SPIKE** | LangGraph only if actual workload warrants Python runtime; no Brain Agent framework |
| Tool protocol | **ADOPT SELECTIVELY MCP** | I authorization and sandbox still required; H owns BMCP |

---

## 4. Architecture decisions and product choices / 架构决策与产品选型

### 4.1 Memory products

- **Graphiti:** strongest candidate for temporal entity/relation graph projection and episode-linked source lineage. Do not deploy as canonical truth. Its graph database and Python runtime are additional operational components; keep it out of the minimal topology until graph-specific query value is measured.
- **Mem0 OSS:** candidate extraction/search adapter. Its SQL/vector/entity-store composition can create cross-store consistency and deletion work. Do not adopt the full stack as a canonical backend.
- **Hindsight:** strongest integrated comparative pipeline candidate for a controlled benchmark (retain/recall/reflect, semantic/BM25/graph/temporal retrieval, PostgreSQL-centered storage). Its bank isolation and observation lineage do not replace Brain authorization or Evidence authority.
- **Letta/MemFS:** use as reference or optional Agent-owned workspace. Avoid dual writable canonical memory.
- **LangMem:** algorithm/toolkit reference; defer production dependency unless a Python/LangGraph boundary is already justified.
- **Zep Cloud:** defer pending commercial terms, data residency, export, retention, deletion SLA and lock-in review.

**Benchmark scope:** compare the SQL/lexical Brain baseline against at most two isolated candidates in the first experiment. Recommended first comparison: Hindsight as an integrated pipeline candidate and Graphiti as a temporal-graph-specific candidate. Mem0 should be evaluated as an extraction/retrieval adapter rather than another complete deployed stack. Do not deploy all three as simultaneous authorities or production services.

### 4.2 Storage and search profiles

Session 03 correctly distinguishes two deployment profiles rather than proposing dual active writers:

- **Embedded/local profile:** SQLite + WAL + FTS5 + local content-addressed payloads; suitable only for single-host authority semantics after crash/backup/restore proof.
- **Server profile:** PostgreSQL + native FTS + optional pgvector; preferred server candidate, not an approved engine.

These are alternatives, not a multi-database topology for one authority. The Storage L4 ADR must select the exact engine, version, configuration, deployment, backup/restore and read-path semantics. The current TAB-001's SQLite-first prototype direction is compatible with testing an embedded profile; it does not approve SQLite as the final server topology.

Do not add Qdrant, Tantivy, LanceDB, Redis, Neo4j or an external search cluster to the first runnable slice. First measure SQL lexical retrieval, multilingual tokenization, recall/latency and update/delete/rebuild. If vector value is demonstrated, test pgvector first. Add a separate Qdrant service only if measured filtered ANN scale, isolation or operational needs cannot be met economically in the selected SQL profile.

### 4.3 Durable execution

Start with one narrow SQL-backed work ledger/outbox and bounded worker pool in the modular monolith. Persist attempt, lease, retry schedule, fencing token and terminal execution evidence as required by the relevant approved contracts. Do not create a general workflow language/engine.

- **Temporal:** future candidate for many long-lived, multi-service workflows, durable timers, operator recovery and cross-service orchestration.
- **Restate:** future candidate for durable RPC/Virtual Objects; separately assess Server BSL 1.1 terms and operational authority.
- **DBOS:** spike only. The Session 02 report identifies Rust 0.6 as pre-production and PostgreSQL-dependent; do not infer SQLite support for the Rust SDK from other language SDKs.

The SQL work mechanism must not absorb or redefine D Forget fences, Storage canonical visibility, C Provider side-effect evidence, C/G/H Applied persistence, or I authorization/revocation.

### 4.4 Security and policy evaluation

Cedar is the only initial PDP candidate worth a bounded Rust prototype. It is not approved for production.

**Mandatory wrapper rule:** Cedar policy-evaluation errors must fail closed at the Brain adapter boundary. The report's documented skip-on-error behavior means an individual policy error can be ignored during evaluation; therefore a naive wrapper must not accidentally allow a different Permit to mask an evaluation error. The wrapper must distinguish deny, no-match and evaluation error, and treat error/unknown input as deny. Validate this behavior with explicit conformance vectors and fault injection.

I retains principal/workload/delegation trust, PolicyDomain, policy activation/version, PermissionEpoch, revocation ordering, and audit evidence. Cedar is only a candidate evaluator. OPA is deferred until multi-language/distributed policy bundles or infrastructure policy justify its extra runtime. OpenFGA is deferred until measured ReBAC graph complexity justifies tuple projection, synchronization and a second service. Do not introduce Cedar + OPA + OpenFGA as a multi-engine stack.

### 4.5 Agent runtime and protocol

- No Brain-owned general Agent runtime, planner, tool marketplace, or generic Tool Registry in the first scope.
- LangGraph is a conditional isolated runtime spike, not a Brain Core dependency. Its Python boundary, checkpoint replay and tool-side-effect idempotency must be tested.
- Hermes and Letta are product references or optional external Agent hosts; isolate their tools and memory.
- MCP may be adopted selectively for tool discovery/invocation. MCP is not authorization, sandboxing, canonical memory, BMCP or Applied proof.
- BMCP remains H-owned. Bridge only through explicit semantic mapping; never silently drop identity, Scope, authorization, ContextVersion, ACK, Applied or Forget semantics.
- Start with one Runtime Adapter, not several for speculative portability.

---

## 5. Non-delegable authority matrix / 不可委托权威矩阵

| Authority | Owner / authority | Product role | Prohibited substitution |
|---|---|---|---|
| Canonical Memory Truth | Brain domain / D + Storage per contracts | Candidate/projection only | Product memory table, graph or vector DB as truth |
| Evidence / Provenance | Brain-owned Evidence semantics | Source pointers and lineage inputs | Episode ID, quote or Git history as canonical proof |
| Authorization | I | PDP library candidate / PEP integration | user_id, tenant_id, agent_id, vector filter or product RBAC as grant |
| Forget | D / I / Storage according to owned contracts | Downstream purge target | DELETE success as Forget terminality |
| Lifecycle | Brain Owners and producer contracts | Work execution only | Workflow completion as lifecycle terminal proof |
| Context Applied Evidence | C/G/H inference boundary | Runtime supplies observations | Search hit, prompt assembly, queue ACK or checkpoint as Applied |

Any integration that violates this matrix is rejected regardless of benchmark performance.

---

## 6. First implementation sequence / 首期实现顺序

This is a proposed sequence for planning, not authorization to start protected implementation.

1. **Restore source-of-truth discoverability.** Reconcile README's normative directory map with current `main`; publish or link the exact authoritative bilingual Owner contracts and record branch/Blob/approval status.
2. **Close domain and storage prerequisites.** Resolve B Fact/Claim ADR; obtain D/Storage physical transaction and row-ownership agreement; finish Storage L4 engine/profile decision; establish I authorization and revocation integration contract.
3. **Define one vertical slice.** One Brain ingress → durable acceptance → deterministic compile work → canonical commit → lexical retrieval → authorization recheck → one Agent Adapter request. Keep all external product adapters disabled initially.
4. **Prove failure behavior.** Retry/idempotency, lease expiry, concurrent producer admission, Forget fence race, late publication, index rebuild, restore anti-rollback and fail-closed authorization.
5. **Add one product experiment at a time.** Hindsight/Graphiti/Mem0 as non-authoritative candidate pipelines; Cedar PDP; LangGraph only if workload evidence supports it.
6. **Decide by evidence.** Every adoption requires exact package/image/commit pin, SBOM/license/CVE review, operational model, benchmark against baseline, threat model, migration/rollback, Forget/restore conformance and relevant Owner approval.

---

## 7. Mandatory acceptance gates / 强制验收门禁

| Gate | Required evidence | Current status |
|---|---|---|
| G0 — Source currentness | All relied-on Owner contracts pinned to current authoritative branch/PR and approval state; README path map reconciled | **OPEN** |
| G1 — Domain semantics | B Fact/Claim ADR and relevant D/E/C/G/H/I contracts resolved and approved | **OPEN / BLOCKED** |
| G2 — Transaction authority | Exact D/Storage transaction domain, row ownership, visibility and crash/race proof | **OPEN** |
| G3 — Physical Storage L4 | Engine/version/config/deployment, backup/PITR, restore and anti-rollback | **OPEN** |
| G4 — Forget | Fence/admission/publication/index/cache/backup/restore race and recovery conformance | **NOT PROVEN** |
| G5 — Authorization | Principal binding, fail-closed PDP/PEP, PermissionEpoch and revocation race tests | **NOT PROVEN** |
| G6 — Applied | Exact final-request Applied contract, test and implementation evidence | **NOT PROVEN** |
| G7 — Product suitability | Reproducible labeled benchmark and fault tests against baseline | **NOT RUN** |
| G8 — Supply chain | Exact versions, SBOM, transitive licenses, CVEs, service terms | **NOT COMPLETE** |
| G9 — Operations | Deployment, backup, restore, observability, runbooks, RPO/RTO and cost | **NOT COMPLETE** |
| G10 — Independent acceptance | Separate review of exact candidate implementation and bilingual semantic parity | **PENDING** |

No gate is passed by this research consolidation. No product adoption or implementation is approved by this report.

---

## 8. Contradictions, risks and required corrections / 冲突、风险与必须修正事项

| ID | Finding | Required correction / closure |
|---|---|---|
| PF-I-01 | All six sessions used historical base `b3c666e...`; current main is `e52594f...` | Refresh every source pin and rerun a current-main delta review before normative decisions |
| PF-I-02 | Session 06 says Sessions 01–05 reports were not located, despite PRs #74–#78 | Correct Session 06 inventory and rerun its cross-session reconciliation |
| PF-I-03 | README maps detailed Owner source directories that are absent from current main tree | Publish/link authoritative specs or amend path map under bilingual governance |
| PF-I-04 | Session 01 suggests comparing multiple memory systems; Session 03/06 seek minimal deployment | Keep comparisons isolated and non-authoritative; do not deploy all candidates together |
| PF-I-05 | Cedar evaluator error semantics can be miswrapped | Require explicit fail-closed adapter semantics and conformance vectors |
| PF-I-06 | Storage SQLite/PostgreSQL profile choice remains unresolved | Do not treat either as selected; Storage L4 must decide based on workload and recovery proof |
| PF-I-07 | Workflow products may be mistaken for domain lifecycle/transaction authorities | Keep SQL execution ledger separate from canonical transaction, Forget, Provider and Applied evidence |
| PF-I-08 | MCP and BMCP have different scope and ownership | Keep BMCP normative; MCP bridge must preserve semantic fields or reject mapping |
| PF-I-09 | Product docs/benchmarks are not Brain-specific proof | Pin exact artifacts and run same corpus, same model/token budget, same failure suite |
| PF-I-10 | No benchmark thresholds or production workload profile supplied | Product owner must define corpus, SLO, data residency, retention and cost envelope before selection |

---

## 9. Final recommendation / 最终建议

**The project should not buy its way out of unresolved domain semantics, and should not build generic infrastructure that mature products already provide.** Build the unique Brain authority and correctness protocols; reuse commodity execution, policy, retrieval and Agent capabilities behind adapters. Minimize first deployment components, then scale only when a measured workload or conformance gap requires it.

**项目不应试图用采购产品绕过尚未解决的领域语义，也不应重复自研成熟产品已经提供的通用基础设施。** 应自研 Brain 独有的权威和正确性协议；通过 Adapter 复用通用执行、策略、检索和 Agent 能力。首期物理组件应尽量少，只有当真实负载或符合性缺口有测量证据时才扩展。

### Proposed ADRs (not approved)

1. **ADR-PF-001 — Non-authoritative Product Adapter & Projection Boundary.** All external memory/runtime/search products are replaceable, untrusted candidates/projections; Brain revalidates authorization, canonical state, lifecycle and Forget before visibility.
2. **ADR-PF-002 — Minimal Modular-Monolith Deployment Profile.** One deployable Rust modular monolith, one selected transactional authority, SQL-backed durable work, one policy implementation; no mandatory broker/cache/vector/graph/workflow service.
3. **ADR-PF-003 — Conditional Product Adoption Gates.** Define measurable triggers and mandatory evidence for Memory, Workflow, Search, PDP and Agent Runtime product adoption.

Each ADR requires affected Owner review (A–I and Storage as applicable), bilingual parity, exact source pins, and formal governance approval. These proposals do not change Owner contracts.

### Explicit non-decisions

- No final SQLite vs PostgreSQL decision.
- No Qdrant, Neo4j, Tantivy, LanceDB, Redis or external search cluster adoption.
- No Temporal, Restate or DBOS production adoption.
- No Cedar production adoption.
- No LangGraph production dependency.
- No external product as Canonical Memory or Evidence authority.
- No merge, release, architecture freeze, Gate pass or production activation.

---

## 10. 中文执行摘要 / Chinese executive summary

本次统一审查确认六份研究方向总体一致：**保留 Brain 自身语义权威，减少物理基础设施数量，先构建可验证的最小闭环，再按测量结果引入成熟产品。**

首期建议：

1. 一个模块化 Rust 单体；A–I 是逻辑权威边界，不要求拆成微服务或一 Owner 一 Crate。
2. 一个事务权威；SQLite/WAL 是本地单机候选，PostgreSQL 是服务端候选，必须由 Storage L4 和实际负载验证后选其一。
3. 一个 SQL Outbox/Work Table + 有界 Worker；暂不引入通用 Workflow Engine。
4. 先做 SQL 原生词法检索；向量、图、外部搜索服务均延后。
5. Cedar 只作为 Rust PDP 原型候选，必须在 Brain Adapter 层做到错误即拒绝；OPA/OpenFGA 暂缓。
6. MCP 只用于外部工具生态；BMCP 继续由 H 负责。
7. Memory 产品只生成候选和派生投影；Graphiti/Hindsight/Mem0 只能隔离比较，不能成为 Canonical Truth。
8. Forget、Evidence、Authorization、Lifecycle、Context Applied 均不得委托给产品。

**当前最大阻塞不是缺少更多产品，而是当前 main 的详细 Owner 契约可发现性、B Fact/Claim、D/Storage 物理事务合同、Storage L4、Forget/Restore、Authorization/Revocation 和 Applied 证据尚未形成完整可验证闭环。** 因此本报告的最终处置为：研究整合完成；架构与产品采用仍待 Owner 审批及验证。

