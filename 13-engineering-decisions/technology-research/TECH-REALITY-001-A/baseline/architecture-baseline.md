# Architecture Baseline / 架构基线

- Task: TECH-REALITY-001-A
- Owner: A — Principal System Architect & Integration Architect
- Baseline branch: `main`
- Baseline commit: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Baseline captured: 2026-11-17
- Research branch: `ai/TECH-REALITY-001-A/principal-technology-research`
- Status: **BASELINE CAPTURED — RESEARCH IN PROGRESS / 基线已建立，研究进行中**

## 1. Scope and method / 范围与方法

This baseline was read directly from GitHub at the exact `main` commit above. It records repository metadata, the recursive Git tree, primary governance and architecture documents, TAB-001, documentation coverage status, current pull requests, and open issues. It does not treat a reader guide as a substitute for an owner contract, nor a technology candidate as an approved decision.

本基线直接从 GitHub 按上述精确 `main` 提交读取，覆盖仓库元数据、递归 Git Tree、主要治理与架构文档、TAB-001、双语覆盖状态、当前 PR 和开放 Issue。本研究不以阅读指南代替 Owner 正式契约，也不把技术候选项视为已批准决策。

## 2. Repository snapshot / 仓库快照

| Field | Observed value |
|---|---|
| Repository | `oahcom/AiMemoryBrainArchitecture` |
| Visibility | Private |
| Default branch | `main` |
| HEAD | `b372b62c640a2b656e54b6db62a4ee67d7d8c001` |
| HEAD commit time | 2026-11-17T09:25:41Z |
| Repository pushed_at | 2026-11-17T10:20:31Z |
| Open issues count (repo metadata) | 36 |
| Implementation status in README | Not started by design |
| Current phase in README | System architecture baseline |

## 3. Normative architecture baseline / 规范性架构基线

The following source files were read at the baseline commit. Blob SHAs are the exact GitHub tree entries.

| Area | Source path | Blob SHA | Baseline interpretation |
|---|---|---|---|
| Invariants | `00-governance/architecture-invariants.md` | `33b037318e459ebb73bea33b3186f31a41d5dcfe` | Normative invariants I-01..I-24 |
| Design principles | `00-governance/design-principles.md` | `192e6ba6e9287792a02b679dda0d391844270228` | P-01..P-16 marked DECIDED |
| Bilingual policy | `00-governance/bilingual-documentation-policy.md` | `b51b054b9f1022133666542680df74dfe19de2fb` | GOV-DOC-001 normative; paired docs required |
| System component map | `01-system-architecture/component-map.md` | `ddb7a1571463cadce83d89f62b03526c4f9693e8` | Logical boundaries; not process/crate mandates |
| System overview | `01-system-architecture/system-overview.md` | `995a1c5a3815d7e7b81b8d7f2ccc546c91d4c256` | Brain authority and system responsibilities |
| System boundaries | `01-system-architecture/system-boundaries.md` | `ad9ea5ce00e74dba89d325601677270a50f30926` | Trust, authority and dependency boundaries |
| Data flows | `01-system-architecture/data-flows.md` | `9cc45d2e593c186123ddc43dcdfdf1881017684a` | Ingress, recall, context and Forget flows |
| Component interactions | `01-system-architecture/component-interactions.md` | `07a35c31921d08a3da832a71cd11db99c0f85922` | Cross-subsystem collaboration |
| Responsibility matrix | `01-system-architecture/responsibility-matrix.md` | `fbeb6935fe874e6c843c25c3a891d6b3242cbfd3` | Owner and logical responsibility mapping |
| Quality attributes | `01-system-architecture/system-quality-attributes.md` | `4350733173d29451a8ea4aa6a544de46526b4fd7` | Quality goals; quantitative SLOs not established |
| Domain overview | `02-domain-model/domain-model-overview.md` | `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` | Domain object model |
| Core entities | `02-domain-model/core-entities.md` | `8cb5a674eec8eac1f3c4d83c400dc08d00166f23` | Entity and object definitions |
| Temporal/epistemic semantics | `02-domain-model/epistemic-and-temporal-semantics.md` | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` | Distinct time and epistemic dimensions |
| Lifecycle | `02-domain-model/lifecycle-model.md` | `81c48c928cb5f9c76ca29d493fbd9479079e62f7` | Memory lifecycle and state semantics |
| Scope/permission | `02-domain-model/scope-and-permission-model.md` | `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | Scope distinct from authorization |
| Provenance | `02-domain-model/relationships-and-provenance.md` | `e762f84c59f69de7a44baad2123aed46e1ffea16` | Provenance and relationship semantics |
| Agent integration | `07-agent-integration/agent-integration-overview.md` | `073ff4ddf71fbcaf959107bb06ab724bfa48e63b` | Agent owns reasoning/action; Brain owns memory/context |
| Technology blueprint | `13-engineering-decisions/technology-architecture-blueprint.md` | `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` | TAB-001 v0.1, CANDIDATE, not frozen |
| Roadmap | `ARCHITECTURE_ROADMAP.md` | `29289361973ec4369f067706132190793cd57a6b` | Architecture before implementation |
| Bilingual coverage | `docs/translation-status.md` | `7b15c5000c324729fd16f82f4b247de4e411d51e` | Detailed contract translations remain incomplete |
| AI development standard | `14-ai-development/ai-development-standard.md` | `f46867f97fc1860015adbe2a1f7b8262640c16fd` | Controlled Owner workflow |

## 4. Technology decision status / 技术决策状态

TAB-001 v0.1 explicitly labels itself **CANDIDATE SYSTEM-WIDE BLUEPRINT — NOT A TECHNOLOGY FREEZE**. The following classification is taken from its technology decision register, not inferred from technology popularity.

| ID | Technology area | TAB-001 status | Required evidence / authority |
|---|---|---|---|
| TEC-001 | Rust core language | DECIDED direction | Existing architecture baseline |
| TEC-002 | Tokio async runtime | RECOMMENDED | Runtime prototype and dependency review |
| TEC-003 | SQLite + WAL primary store | CANDIDATE / TO_VALIDATE | D/E Forget race tests, transaction/recovery tests, concurrency benchmark |
| TEC-004 | PostgreSQL multi-writer/remote path | CANDIDATE | Workload threshold and migration comparison |
| TEC-005 | Content-addressed local blob store | RECOMMENDED | Crash consistency, integrity, backup/restore tests |
| TEC-006 | FTS5 / Tantivy lexical search | CANDIDATE | Recall quality, throughput, update/delete and rebuild benchmarks |
| TEC-007 | Embedded ANN / sqlite-vec | OPEN | Recall, latency, memory, update/delete and rebuild evaluation |
| TEC-008 | Moka in-process cache | RECOMMENDED | Generation invalidation and memory-bound tests |
| TEC-009 | ONNX Runtime embeddings | CANDIDATE | Model/operator compatibility and CPU/GPU benchmark |
| TEC-010 | llama.cpp-compatible local LLM | CANDIDATE | Target GPU/context/VRAM and latency benchmark |
| TEC-011 | Capability-based model provider interfaces | RECOMMENDED architecture | Contract and provider conformance |
| TEC-012 | JSON initial protocol encoding | OPEN / H-owned | H schema, compatibility and payload benchmark |
| TEC-013 | HTTP/local IPC transport | OPEN / H-owned | Security, streaming, reconnect and cross-platform tests |
| TEC-014 | tracing + metrics / OTel exporters | RECOMMENDED | Correlation and sensitive-data review |
| TEC-015 | Secrets/crypto | OPEN / I-owned | Threat model, key lifecycle, platform matrix |
| TEC-016 | Local modular monolith + optional inference worker | CANDIDATE | Fault isolation and resource benchmark |
| TEC-017 | Versioned SQL migrations | RECOMMENDED | Upgrade/downgrade/restore tests |
| TEC-018 | Transactional outbox + DB workers | CANDIDATE | Admission/fence linearization and replay/fault tests |

TAB-001 itself declares unresolved: D/E/Storage producer admission/fence/dependency-registration/publication semantics; B Fact/Claim ADR; C/G/H final-request Applied evidence; I cross-owner Forget target evidence; encryption/key custody; and workload/SLO targets.

TAB-001 v0.1 的技术决策登记表明确区分上述状态。该文档同时明确：D/E/Storage 的生产者准入、Fence、依赖登记与发布语义；B 的 Fact/Claim ADR；C/G/H 的最终请求 Applied 证据；I 的跨 Owner Forget 目标证据；加密与密钥托管；以及工作负载/SLO 均未闭合。

## 5. Architecture coverage and implementation status / 架构覆盖与实现状态

| Area | Evidence on baseline main | Status |
|---|---|---|
| Logical system architecture | Detailed English source docs in 01 | Defined at logical level |
| Domain model | Detailed English source docs in 02 | Defined with unresolved semantic decisions |
| D/E/F/G/C/H/I owner detail | Reader guides exist under docs/zh-CN and docs/en; detailed source coverage tracked as incomplete | Partial |
| Storage & Index | Referenced in roadmap/blueprint; no root `09-storage-and-index/` files in baseline tree | Not established as a detailed normative owner specification in this baseline |
| Consistency & Recovery | Detailed concepts in TAB-001/reviews, but no root `11-consistency-and-recovery/` files in baseline tree | Cross-owner details remain open |
| Testing & Acceptance | Reader guides exist; detailed execution remains NOT_RUN/BLOCKED per translation tracker | Plan/guide, not demonstrated implementation |
| Runtime code | README says implementation not started; root tree is architecture/docs/reviews | No Brain production implementation observed in this repository snapshot |
| Rust build manifest | No root `Cargo.toml` observed in baseline tree | No Rust application workspace observed in this repository snapshot |

The repository README describes the project as architecture definition and implementation not started by design. This finding is scoped to this repository snapshot; it does not assert that no prototype exists elsewhere.

README 将项目标为架构定义阶段、按设计尚未开始实现。本结论仅限于该仓库基线快照，不推断其他仓库或外部原型不存在。

## 6. Active GitHub governance context / 当前 GitHub 治理上下文

Open PRs observed at capture time include:
- PR #44 — ARCH-CONSOL-001 system-wide architecture consolidation (open; head `d7a3379fd51660912200a6131bcd037c0f53583c`).
- PR #42 — ChatGPT-native execution model (open; head `0708e25d8e008b1044679ff29ba7ae34977bc08c`).
- PR #36 — bounded Codex Owner worker pilot (open; head `aab5985caa8cee122596878d0db4ff45cfb617d5`).
- PR #35, #34, #33, #32, #31 — AI-RUN-003 runtime design and ADR chain (open; branches are not based directly on main in all cases).
- PR #28 — bilingual architecture coverage completion (open; head `d59ffe7e6bfa1432e03f1dede95fee96fa13d05f`).
- PR #27 — persistent Ubuntu worker endpoint (open).
- PR #23 — AID-2026-001 governance owner review (open).
- PR #1 — Session G Memory Context architecture (open).

Open issues relevant to technology and feasibility include #43 (system-wide consolidation/feasibility), #30 (Owner Worker runtime), #29 (HRC/recovery/topology proof), #25 (D/E/I/Storage producer admission and derivative visibility gate), #21 (F/E/G lifecycle), #20/#19/#18/#17/#16/#15/#14/#13 (Forget/COC/storage consistency review series), #10 (PostgreSQL prepared-XID capability probe), #7 (authoritative runtime repository), #4 (identity/authorization/Forget), #3 (Applied evidence/BMCP), and #2 (compiler publication fence). These issue/PR records are context and blockers, not proof of resolution.

## 7. Baseline findings and risks / 基线发现与风险

1. **Candidate architecture is not an implementation.** The blueprint is comprehensive but its key storage, workflow, retrieval, protocol, security and deployment decisions remain candidates/open/to-validate.
2. **TAB-001 baseline pointer is stale relative to current main.** TAB-001 header names baseline commit `8a6414158c9c056c1638222534e1993d1bbc99d2`; current main is `b372b62c640a2b656e54b6db62a4ee67d7d8c001`. This is a traceability defect to reconcile, not evidence that TAB-001 content is necessarily wrong.
3. **Storage atomicity is the critical feasibility gate.** SQLite WAL is a single-host, single-writer design; it does not itself implement the cross-owner admission/fence/publication proof. PostgreSQL may offer stronger multi-writer/locking options but does not remove the need for a correctly designed transaction protocol.
4. **Logical decomposition is at risk of being mistaken for deployment decomposition.** Existing invariants explicitly say subsystem boundaries do not imply separate process/service/crate.
5. **Detailed source-level bilingual coverage is incomplete.** Translation status explicitly records many detailed specifications as NOT STARTED. Reader guides are not substitutes for the normative source contracts.
6. **No workload measurements are yet approved.** TAB-001's 12–16 GB VRAM is a planning envelope; CPU, host RAM, corpus, concurrency, throughput, retrieval QPS, SLO, RTO and RPO remain unconfirmed.
7. **The project has an open architectural consolidation effort.** PR #44 / Issue #43 must be reviewed for possible changes before finalizing system recommendations.

## 8. Baseline conclusion / 基线结论

**Baseline classification: NOT YET PROVEN.** The logical architecture is sufficiently articulated to conduct a serious technology feasibility study, but the repository baseline does not establish an executable Rust implementation, approved deployment topology, physically proven transaction semantics, measured workload fit, or complete owner-contract closure.

**基线分类：NOT YET PROVEN（尚未证明）。** 现有逻辑架构足以开展严肃的技术可行性研究，但仓库基线尚未证明存在可执行的 Rust 实现、已批准的部署拓扑、经过物理验证的事务语义、经测量的工作负载适配性或完整的 Owner 契约闭环。

## 9. Evidence limitations / 证据限制

- This baseline captures the repository state at one commit; PR heads and issues may move after capture.
- This document does not claim the full diff/content of every open PR has been reviewed.
- Third-party technology implementation evidence is recorded separately in `research-evidence-register.md`.
- No Brain prototype benchmark was run as part of baseline capture (`NOT RUN`).

- 本基线只记录一个精确提交时点；PR Head 和 Issue 后续可能变化。
- 本文件不声称已经审查所有开放 PR 的完整差异。
- 第三方技术实现证据另行登记在 `research-evidence-register.md`。
- 本阶段未运行 Brain 原型基准测试（`NOT RUN`）。

## 10. 完整中文版本 / Chinese Version

### 10.1 基线范围与仓库快照

本基线在 2026-11-17 直接读取 GitHub 的 `main`，精确 HEAD 为 `b372b62c640a2b656e54b6db62a4ee67d7d8c001`。研究分支从该提交创建。仓库是 Private，默认分支为 main。README 明确表示项目处于系统架构基线阶段，按设计尚未开始生产实现。本结论只适用于该仓库快照，不表示其他仓库或外部原型不存在。

### 10.2 已读取的规范文档

| 领域 | 文件 | Blob SHA | 基线判断 |
|---|---|---|---|
| 架构不变量 | `00-governance/architecture-invariants.md` | `33b037318e459ebb73bea33b3186f31a41d5dcfe` | I-01 至 I-24 |
| 设计原则 | `00-governance/design-principles.md` | `192e6ba6e9287792a02b679dda0d391844270228` | P-01 至 P-16 标记 DECIDED |
| 双语规范 | `00-governance/bilingual-documentation-policy.md` | `b51b054b9f1022133666542680df74dfe19de2fb` | GOV-DOC-001，双语文档为规范要求 |
| 系统组件图 | `01-system-architecture/component-map.md` | `ddb7a1571463cadce83d89f62b03526c4f9693e8` | 逻辑边界，不等于进程/Crate 划分 |
| 系统总览 | `01-system-architecture/system-overview.md` | `995a1c5a3815d7e7b81b8d7f2ccc546c91d4c256` | Brain 权威及系统责任 |
| 系统边界 | `01-system-architecture/system-boundaries.md` | `ad9ea5ce00e74dba89d325601677270a50f30926` | 信任、权威与依赖边界 |
| 数据流 | `01-system-architecture/data-flows.md` | `9cc45d2e593c186123ddc43dcdfdf1881017684a` | Ingress、Recall、Context、Forget |
| 组件交互 | `01-system-architecture/component-interactions.md` | `07a35c31921d08a3da832a71cd11db99c0f85922` | 跨子系统协作 |
| 职责矩阵 | `01-system-architecture/responsibility-matrix.md` | `fbeb6935fe874e6c843c25c3a891d6b3242cbfd3` | Owner 与逻辑责任 |
| 质量属性 | `01-system-architecture/system-quality-attributes.md` | `4350733173d29451a8ea4aa6a544de46526b4fd7` | 质量目标存在，量化 SLO 未建立 |
| 领域总览 | `02-domain-model/domain-model-overview.md` | `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` | 领域对象模型 |
| 核心实体 | `02-domain-model/core-entities.md` | `8cb5a674eec8eac1f3c4d83c400dc08d00166f23` | 实体与对象定义 |
| 时间/认知语义 | `02-domain-model/epistemic-and-temporal-semantics.md` | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` | 不同时间和认知维度 |
| 生命周期 | `02-domain-model/lifecycle-model.md` | `81c48c928cb5f9c76ca29d493fbd9479079e62f7` | 记忆生命周期与状态 |
| Scope/权限 | `02-domain-model/scope-and-permission-model.md` | `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | Scope 与 Authorization 分离 |
| Provenance | `02-domain-model/relationships-and-provenance.md` | `e762f84c59f69de7a44baad2123aed46e1ffea16` | 来源与关系语义 |
| Agent 集成 | `07-agent-integration/agent-integration-overview.md` | `073ff4ddf71fbcaf959107bb06ab724bfa48e63b` | Agent 管推理/动作，Brain 管记忆/Context |
| 技术蓝图 | `13-engineering-decisions/technology-architecture-blueprint.md` | `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` | TAB-001 v0.1，CANDIDATE，不是冻结 |
| Roadmap | `ARCHITECTURE_ROADMAP.md` | `29289361973ec4369f067706132190793cd57a6b` | 先架构后实现 |
| 双语覆盖 | `docs/translation-status.md` | `7b15c5000c324729fd16f82f4b247de4e411d51e` | Owner 详细契约双语覆盖不完整 |
| AI 开发规范 | `14-ai-development/ai-development-standard.md` | `f46867f97fc1860015adbe2a1f7b8262640c16fd` | Owner 工作流受治理约束 |

### 10.3 TAB-001 技术决策状态

TAB-001 明确标注为“候选系统级蓝图，非技术冻结”。Rust 是已决定方向；Tokio 为推荐；SQLite+WAL、PostgreSQL、FTS5/Tantivy、ANN、ONNX Runtime、llama.cpp、JSON/HTTP、Moka、Outbox/Worker、模块化单体等均处于候选、推荐或待验证状态，不能因为出现在蓝图中就视为批准。

| ID | 技术领域 | 蓝图状态 | 关键验证 |
|---|---|---|---|
| TEC-001 | Rust | DECIDED 方向 | 现有架构基线 |
| TEC-002 | Tokio | RECOMMENDED | Runtime 原型与依赖审查 |
| TEC-003 | SQLite + WAL | CANDIDATE / TO_VALIDATE | D/E Forget 竞争、事务、恢复与并发测试 |
| TEC-004 | PostgreSQL | CANDIDATE | 工作负载阈值和迁移比较 |
| TEC-005 | 内容寻址 Blob | RECOMMENDED | 崩溃一致性、完整性和备份恢复 |
| TEC-006 | FTS5/Tantivy | CANDIDATE | 检索质量、吞吐、更新删除与重建 |
| TEC-007 | ANN/sqlite-vec | OPEN | Recall、延迟、内存和重建 |
| TEC-008 | Moka | RECOMMENDED | Generation 失效与内存限制 |
| TEC-009 | ONNX Runtime | CANDIDATE | 模型算子与 CPU/GPU 基准 |
| TEC-010 | llama.cpp | CANDIDATE | 目标 GPU、上下文、VRAM 与延迟 |
| TEC-011 | Provider Adapter | RECOMMENDED 架构 | 契约与 Provider Conformance |
| TEC-012 | JSON | OPEN / H-owned | Schema、兼容性与负载基准 |
| TEC-013 | HTTP/IPC | OPEN / H-owned | 安全、流式、重连与跨平台 |
| TEC-014 | tracing/metrics/OTel | RECOMMENDED | 跨模块关联与敏感信息审查 |
| TEC-015 | Secrets/crypto | OPEN / I-owned | 威胁模型、密钥生命周期和平台矩阵 |
| TEC-016 | 模块化单体 + 推理 Worker | CANDIDATE | 故障隔离和资源基准 |
| TEC-017 | SQL Migration | RECOMMENDED | 升级/回滚/恢复测试 |
| TEC-018 | Outbox + DB Worker | CANDIDATE | Admission/Fence 线性化与重放测试 |

### 10.4 实现覆盖与风险

主分支没有根目录 `Cargo.toml`，也没有 Brain Rust 应用工作区；README 说明实现尚未开始。部分 Owner 详细契约、Storage、Consistency、Testing 双语文件仍未完成。TAB-001 的关键未决项包括 D/E/Storage Producer Admission/Fence/Dependency/Publication、B Fact/Claim ADR、C/G/H Applied、I Forget 目标清单、加密与密钥托管，以及真实工作负载/SLO。

### 10.5 基线结论

**NOT YET PROVEN（尚未证明）**。逻辑架构足以支持严肃技术研究，但当前仓库不能证明已有可执行 Rust 实现、正式部署拓扑、物理事务原子性、真实负载适配或完整 Owner 契约闭环。TAB-001 的基线提交为 `8a6414158c9c056c1638222534e1993d1bbc99d2`，早于本次 main HEAD；这是追溯性缺陷，必须在后续 ADR/研究中记录精确提交与 Blob。
