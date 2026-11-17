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
