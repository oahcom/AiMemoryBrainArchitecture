# Architecture Complexity Audit / 架构复杂度审计

- Task: TECH-REALITY-001-A | Owner A | Date: 2026-11-17
- Status: **EVIDENCE-BASED FINDINGS; OWNER DECISIONS PRESERVED / 基于证据的发现；保留 Owner 决策权**

## 1. Audit principle / 审计原则

Complexity is not measured by document count alone. A typed cursor, receipt or coordinator may be necessary when it represents a distinct fact or authority. The audit flags duplicate semantics, hidden shared state, unnecessary physical separation, or a proof burden that exceeds demonstrated requirements. It does not remove required invariants to simplify diagrams.

复杂度不能只按文档数量衡量。当 Typed Cursor、Receipt 或 Coordinator 表达不同事实或权威时，它可能是必要的。本审计关注语义重复、隐藏共享状态、不必要的物理拆分，或超出已证明需求的证明负担；不会为了简化图表而删除必要不变量。

## 2. Findings / 审计发现

### CA-01 — Logical subsystem count can be mistaken for process/crate count
- Evidence: `00-governance/architecture-invariants.md` I-21; `01-system-architecture/component-map.md`; TAB-001 §10.1.
- Finding: The blueprint lists a 14-crate candidate map and multiple logical subsystems, while the invariant explicitly says a subsystem boundary does not imply a separate process/service/crate. Creating every crate/service at once would front-load interface, versioning and deployment costs.
- Impact: A, B–I, Storage, Release.
- Alternative: Start with a single application workspace and a small number of cohesive crates (domain/contracts, storage, application/runtime); split by measured dependency/cycle/build/team pressure.
- Limitation: A monolith still needs explicit module APIs and owner authority.
- Decision owner: A coordinates; each domain Owner confirms boundary.
- Risk: Medium; over-design if interpreted as mandatory.

### CA-02 — Multiple coordinators require a single operation authority map
- Evidence: TAB-001 process diagram lists Forget Coordinator, Transaction/Outbox Coordinator, Compiler Workers, Application composition; component map includes governance and synchronization responsibilities.
- Finding: These names can represent separate orchestration responsibilities, but their authority over state transitions, retries, leases and terminal status is not yet mapped to one operation/owner matrix. Multiple orchestration components may accidentally write the same state or independently infer completion.
- Alternative: One application composition root and one durable work state machine per work domain; coordinators issue commands, while the owning authority commits state.
- Required proof: For every operation identify command owner, state owner, transaction owner, retry owner and evidence owner.
- Decision owner: A + D/E/G/I/Storage.
- Risk: High until the authority map is explicit.

### CA-03 — Typed cursors are not automatically redundant
- Evidence: TAB-001 §9 explicitly distinguishes CanonicalCommitCursor, AggregateRevision, LifecycleEventCursor, IndexWatermark, ContextVersion, PermissionEpoch and ForgetFenceGeneration.
- Finding: These values represent different ordering/authority domains. Collapsing them to one timestamp or integer would be a correctness regression, not simplification.
- Alternative: Keep distinct nominal types; reduce only duplicated storage fields or duplicated receipt wrappers when they prove the same fact.
- Decision owner: D/F/G/I/H/Storage by owned namespace; A maps cross-owner use.
- Risk: Critical if collapsed; medium if storage representation is verbose.

### CA-04 — Receipt taxonomy may proliferate without proof ownership
- Evidence: TAB-001 distinguishes Accepted, Compiled, Canonical Committed, Indexed, Delivered and Applied; Forget uses a typed evidence vector; BMCP ACK states are H-owned.
- Finding: The distinctions are semantically necessary, but duplicate receipts may appear if every module stores a second copy of the same external fact. No complete fact-to-authority ledger is established in TAB-001 alone.
- Alternative: Define one authoritative record per fact, consumers store references/watermarks/observations, and receipts carry exact subject, version, issuer, boundary and evidence class.
- Limitation: A downstream observation may be necessary for audit and must not be erased merely to reduce rows.
- Decision owner: A/H with C/D/E/F/G/I/Storage.
- Risk: High.

### CA-05 — Database transaction may replace some local coordination protocols, but not cross-owner semantics
- Evidence: TAB-001 §9 lists several operations whose SQL realization is TO_VALIDATE/OPEN; SQLite/PostgreSQL provide transactions within one database.
- Finding: Event + outbox, canonical revision + cursor, and context edit + version increment should be tested as single SQL transactions. This can eliminate unnecessary in-process distributed commit abstractions if records share one authority DB.
- Alternative: Use one transaction and constraints for each local atomic group; use explicit durable state machine/outbox for external effects.
- Non-negotiable: Producer admission vs Forget fence and derivative publication must have a defined linearization point; a read-check-write protocol is insufficient.
- Decision owner: Storage + D/E/G; A coordinates.
- Risk: Critical.

### CA-06 — External workflow/broker infrastructure is not yet justified
- Evidence: TAB-001 explicitly defers Kafka/Kubernetes/microservices; repository README says implementation not started; no workload/SLO data.
- Finding: Adding Temporal, Restate, NATS, Kafka or Redpanda before establishing the DB-backed worker envelope adds a second durable authority and more failure cases.
- Alternative: Start with SQL outbox + leased worker; benchmark queue age, recovery and retry load. Compare Temporal/Restate only if long-running workflows require durable timers, independent worker scaling or operator visibility beyond the local design.
- Limitation: DB workers require careful claim/lease/fencing and can become contention hotspots.
- Decision owner: E, Storage, A.
- Risk: Medium-high.

### CA-07 — Multiple search engines may be premature
- Evidence: TAB-001 §4.3 keeps SQL structured filters, FTS5/Tantivy, ANN and reranker as separate candidates; vector is not mandatory for first slice.
- Finding: Running SQL + Tantivy + Qdrant + separate reranker from day one duplicates indexing, deployment, backup, watermark and Forget suppression paths.
- Alternative: SQL filters + FTS5 first; add one vector projection only after labeled retrieval evaluation demonstrates material quality gain. Compare Tantivy if FTS5 tokenization/ranking/scale is inadequate.
- Limitation: FTS5 Chinese tokenization/segmentation may be insufficient; test Chinese, English and mixed corpora before decision.
- Decision owner: F with D/Storage/I.
- Risk: Medium-high.

### CA-08 — Graph database is not implied by graph-shaped domain
- Evidence: B domain model uses Entity/Relation/Provenance; Graphiti implements graph-specific extraction and graph DB drivers, but current project does not require graph-native traversal scale evidence.
- Finding: Entity and Relation can be represented in relational tables and indexed joins for initial workloads. Graph DB adds another persistence authority and backup/Forget target.
- Alternative: relational entity/relation tables with typed IDs and explicit merge/split history; benchmark recursive traversal.
- Decision owner: B/D/F/Storage.
- Risk: Medium.

### CA-09 — Authorization engine may be an unnecessary service boundary initially
- Evidence: TAB-001 §4.7 leaves crypto/identity OPEN; OpenFGA architecture is a server + DB + API boundary; Cedar is embeddable Rust.
- Finding: A separate OpenFGA/SpiceDB/OPA service adds a network and consistency boundary before policy language, identity and revocation semantics are settled.
- Alternative: I-owned policy contract plus embedded Cedar evaluation spike; compare a service only if relationship tuples, central administration or multi-service enforcement require it.
- Limitation: Cedar does not supply identity issuance, revocation distribution or audit operations.
- Decision owner: I.
- Risk: Medium-high.

### CA-10 — Context synchronization and Agent integration must not be collapsed
- Evidence: invariants I-09..I-11, I-17..I-18; Agent integration overview separates Brain Context authority from Adapter applied version.
- Finding: G ContextVersion, H delivery protocol and C final-request Adapter evidence are distinct authorities. A generic "sync coordinator" that owns all three would blur the boundary.
- Alternative: G owns Context version/change; H owns wire delivery/ACK schema; C owns Adapter final-request behavior; A maps end-to-end proof.
- Decision owner: G/H/C.
- Risk: Critical if collapsed.

### CA-11 — COC and JF-10 should not be described as one automatically composed transaction
- Evidence: Issue #43 and PR #44 body explicitly state COC recovery-cutoff and JF-10 prepared-participant bridge are separate protocols; automatic composition is not approved; Storage topology ADR and JF-10 gates remain blocked.
- Finding: Treating them as one solved distributed transaction overstates the current evidence.
- Alternative: Keep separate protocol models and prove the bridge, participant identity, prepared-XID behavior and recovery ordering under the selected physical topology.
- Decision owner: Storage/Consistency, A/I and relevant Owners.
- Risk: Critical.

### CA-12 — Technology blueprint traceability needs currentness control
- Evidence: TAB-001 header baseline commit `8a6414158c9c056c1638222534e1993d1bbc99d2`; current main HEAD at capture `b372b62c640a2b656e54b6db62a4ee67d7d8c001`.
- Finding: A blueprint with a stale baseline pointer can cause later reviewers to assess superseded contracts.
- Alternative: Every research/ADR records both source task baseline and exact live branch/commit/blob pins; add a currentness check before acceptance.
- Decision owner: A.
- Risk: Medium-high.

## 3. Complexity reduction candidates / 可简化候选

| Candidate | Simplification | Must preserve |
|---|---|---|
| Crate map | Consolidate candidate crates until build/dependency pressure justifies split | Domain ports and owner authority |
| Event processing | SQL outbox + worker before broker | durable acceptance, idempotency, fencing, replay |
| Search | FTS5 first; vector later by measured gain | authorization/Forget suppression and rebuild |
| Authorization | Embedded policy evaluation before service | I-owned identity, revocation, fail-closed |
| Context/ACK | One authority record per distinct fact | G version, H delivery, C Applied evidence |
| Coordinator layer | One state owner per work domain | exact commit point and recovery evidence |

## 4. What must not be simplified away / 不得削减的复杂度

- Separate Event, Memory, Fact/Claim, Entity, Relation and Evidence semantics.
- Canonical Memory vs Memory Context vs Applied Context.
- Typed time, revisions, cursors, epochs and generations.
- Scope vs Permission and independently authorized Evidence dereference.
- Accepted vs Compiled vs Canonical Committed vs Indexed vs Delivered vs Applied.
- Forget barrier and anti-resurrection coverage across replay, index, cache, context, adapter, external recipients and restore.
- Exact final-request Applied boundary and the rule that Applied does not prove model comprehension.
- Unknown/ambiguous evidence remains unknown and blocks completion.

## 5. Audit disposition / 审计结论

There is meaningful opportunity to reduce *physical* and *operational* complexity, but little basis to remove the core semantic distinctions. The largest avoidable complexity risk is premature distribution (services, brokers, multiple indexes and authorization services) before workload evidence and transaction proof. The largest correctness risk is not "too many modules"; it is unclear ownership/linearization for cross-owner state transitions.

## 6. 完整中文版本 / Chinese Version

### 6.1 审计原则

复杂度不能只按文档数量衡量。Typed Cursor、Receipt 或 Coordinator 若表达不同事实和权威，就可能是必要的。本审计只标记语义重复、共享状态不清、物理拆分不必要或证明成本超过实际需求的设计，不会删除 Forget、Security、Evidence、Canonical Truth 等核心不变量。

### 6.2 发现清单

1. **CA-01 逻辑模块不等于进程/Crate 数。** 架构不变量 I-21 和组件图明确逻辑边界不强制独立进程、服务或 Crate。建议先使用一个 Rust Workspace 和少量内聚 Crate，待依赖循环、构建或团队边界有实测压力再拆分。风险中。
2. **CA-02 多个 Coordinator 需要统一操作权威映射。** Forget Coordinator、Transaction/Outbox Coordinator、Compiler Worker 和 Application Composition 的职责可能不同，但谁拥有状态、事务、重试、Lease 和终态证据尚未完整映射。建议每个工作域只设一个状态权威；Coordinator 发命令，不自行写入其他 Owner 的状态。风险高。
3. **CA-03 Typed Cursor 不应被误判为重复。** CanonicalCommitCursor、AggregateRevision、LifecycleEventCursor、IndexWatermark、ContextVersion、PermissionEpoch、ForgetFenceGeneration 属于不同顺序/权威域。合并成时间戳或整数会破坏正确性。保留 Nominal Type，只消除重复存储或重复包装。风险严重。
4. **CA-04 Receipt 体系可能膨胀。** Accepted、Compiled、Canonical Committed、Indexed、Delivered、Applied 和 Forget Evidence 代表不同事实，但需要建立“事实—唯一权威—Receipt—引用”台账，避免多个模块重复保存同一外部事实。风险高。
5. **CA-05 部分本地协调协议可由 DB Transaction 替代。** Event+Outbox、Canonical Revision+Cursor、Context Edit+Version 可在同一事务域时用 SQL 事务和约束完成。但 Producer Admission 与 Forget Fence、依赖注册与最终发布仍必须证明线性化，不能使用 Check-then-write。风险严重。
6. **CA-06 Broker/Workflow 服务尚未被工作负载证明必要。** Kafka、Redpanda、NATS、Temporal、Restate 都增加第二持久化权威。先测 DB Outbox/Lease Worker 的队列年龄、恢复和重试；只有长期 Timer、独立 Worker 或可观测性需求超过本地方案时再引入。风险中高。
7. **CA-07 多套搜索引擎可能过早。** SQL + Tantivy + Qdrant + Reranker 会重复建立索引、备份、Watermark 和 Forget 抑制路径。建议先 SQL 结构过滤 + FTS5；中文/混合语料实测不足再比较 Tantivy；ANN 只在 Recall 有明显收益时增加。风险中高。
8. **CA-08 图形领域不等于必须用图数据库。** Entity/Relation 可先用关系表和递归查询，图数据库增加持久化权威与 Forget 目标。只有遍历基准证明需要时再引入。风险中。
9. **CA-09 授权服务可能是过早服务边界。** OpenFGA/SpiceDB/OPA 增加网络一致性边界。可先由 I 保持语义权威，评估嵌入式 Cedar；但 Cedar 不负责身份签发、撤销传播或审计。风险中高。
10. **CA-10 Context 同步与 Agent 集成不能合并。** G ContextVersion、H Delivery/ACK、C Final Request Applied 是不同权威。不能由通用 Sync Coordinator 混合持有。风险严重。
11. **CA-11 COC 与 JF-10 不是自动组合的单事务。** COC Recovery Cutoff 和 JF-10 Prepared Participant 是两个独立协议，必须证明桥接、Participant Identity、Prepared-XID 和恢复顺序。风险严重。
12. **CA-12 技术蓝图基线指针过期。** TAB-001 声明的基线提交早于当前 main HEAD。后续研究必须同时 Pin 原始任务基线、当前分支 HEAD 和具体 Blob。风险中高。

### 6.3 可简化项与不可削减项

可简化：Crate 数量、先用 SQL Outbox 再引入 Broker、先用 FTS5 再评估向量、先嵌入式 Policy 再考虑服务、每个事实只保留一个权威 Receipt。

不得简化：Event/Memory/Fact/Claim/Entity/Relation/Evidence 的领域区别；Canonical Memory 与 Context/Applied Context 的区别；Typed Time/Revision/Cursor/Epoch；Scope 与 Permission；Accepted/Compiled/Committed/Indexed/Delivered/Applied；Forget 对 Replay/Index/Cache/Context/Adapter/Provider/Backup/Restore 的防复活覆盖；最终请求 Applied 边界；Unknown 必须阻止完成。

### 6.4 审计结论

有较大机会降低**物理与运维复杂度**，但没有依据删除核心语义区别。最大可避免复杂度是过早引入服务、Broker、多索引和授权服务；最大正确性风险不是模块太多，而是跨 Owner 状态迁移的权威和线性化点不清。
