# Session 3 — Engineering Planning Council Report

- Report ID: EPC-2026-11-17
- Version: 0.1
- Status: **CANDIDATE ENGINEERING ASSESSMENT — NOT IMPLEMENTATION AUTHORIZATION**
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Review branch: `review/session-3-engineering-planning-2026-11-17`
- Review date: 2026-11-17
- Baseline: `main`; the latest repository commit returned by GitHub search was `b372b62c640a2b656e54b6db62a4ee67d7d8c001`. PR #46 returned `base_sha` confirming the `main` baseline for this PR as `b372b62c640a2b656e54b6db62a4ee67d7d8c001`; therefore the report's main baseline SHA is **VERIFIED (at PR creation)**. This SHA does not imply that `main` remains unchanged afterward.
- Key source blobs: TAB-001 `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`; System Overview `995a1c5a3815d7e7b81b8d7f2ccc546c91d4c256`; Component Map `ddb7a1571463cadce83d89f62b03526c4f9693e8`; Architecture Invariants `33b037318e459ebb73bea33b3186f31a41d5dcfe`; GOV-DOC-001 `b51b054b9f1022133666542680df74dfe19de2fb`; Roadmap `29289361973ec4369f067706132190793cd57a6b`.
- Method: live GitHub reads of Issues #43, #25, #29, #10, #3, #7, #4, #5, PR search results, source documents and recent commits.
- Independence note: F/D/P are three separately structured analytical roles simulated in this session. They are not three independent humans or Owner approvals. Their cross-examination is analytical evidence only.

## 0. Executive disposition

**Overall: FEASIBLE_WITH_CONDITIONS / PARTIALLY VERIFIED.** The logical architecture can plausibly be implemented as a local-first Rust modular monolith, but the current repository does not prove that the complete system is ready to enter implementation. The most fundamental blockers are not retrieval algorithms or model choice; they are (1) no designated canonical implementation repository and accountable engineering owner (Issue #7), (2) unresolved authority-owned contracts and external governance decisions, (3) unproven D/E/I/Storage producer-admission, Forget-fence, dependency-registration and visibility linearization, (4) unresolved C/G/H final-request Applied evidence, and (5) no selected production Storage/COC topology with complete physical proof.

This report is a planning assessment, not a schema freeze, implementation authorization, Owner approval, deployment decision, or Gate release. Issue #43 remains the controlling system-wide consolidation work item. This report is an engineering-planning workstream under #43, not a duplicate issue.

## 1. Evidence baseline and status discipline

### 1.1 Directly observed facts

- README identifies the repository as **Architecture definition** and implementation as **Not started by design**.
- TAB-001 v0.1 is explicitly **CANDIDATE SYSTEM-WIDE BLUEPRINT — NOT A TECHNOLOGY FREEZE**.
- TAB-001 recommends a modular Rust monolith, local transactional storage, content-addressed blobs, rebuildable indexes, bounded cache, and optional isolated inference. Database, vector index, transport, crypto, deployment and quantitative capacity remain candidate/open/TO_VALIDATE.
- The component map explicitly says its logical components do not mandate 16 services, processes or crates.
- GOV-DOC-001 requires Chinese and English counterparts in the same change set with semantic/status parity.
- Issue #7 says the architecture repository is not the runtime implementation repository; no canonical runtime repository or accountable implementation owner is designated in that issue.
- Issue #25 keeps the D/E/I/Storage publication composition and exact-owner decisions open.
- Issue #29 records a 101-test candidate/reference-model result in its latest visible portion, while explicitly leaving production adapters, real COC/owner ledgers, currentness CAS, physical JF-10, topology and physical fault campaign open. Candidate tests are not production proof.
- Issue #3 states Applied Contract Frozen = NO; tests executed/passed = NO/NO; implementation verified = NO.
- Issues #4/#5 preserve Global Forget inventory/governance approval blockers.
- Issue #10 reports Gate A PARTIAL PASS / OPEN; Gate B and C remain blocked; JF-10 P0 remains open and production activation unauthorized.

### 1.2 Status meanings

- **VERIFIED** — directly supported by current repository evidence at the stated scope.
- **PARTIALLY VERIFIED** — some evidence exists, but scope or exact currentness is incomplete.
- **NOT PROVEN** — plausible or specified, but no adequate reproducible proof.
- **BLOCKED** — a known unmet prerequisite prevents the next gate or acceptance.
- Module feasibility: **FEASIBLE**, **FEASIBLE_WITH_CONDITIONS**, **NOT_PROVEN**, **BLOCKED**.

A green candidate reference-model test suite does not establish deployed correctness. A document or role-simulated review does not establish independent Owner approval. A technology recommendation does not establish a selected technology.

## 2. F — Engineering Feasibility

### 2.1 Engineering Feasibility Matrix

Effort is relative engineering complexity, not person-days. Confidence reflects how well the scope is understood, not delivery certainty.

| Area | Verdict | Complexity | Confidence | Evidence / condition |
|---|---|---:|---|---|
| B Domain Model | FEASIBLE_WITH_CONDITIONS | L | Medium | Typed identity/Fact-Claim decisions and ADR-001 remain open; do not freeze dependent schemas. |
| D Canonical Brain | FEASIBLE_WITH_CONDITIONS | XL | Medium-low | Lifecycle/cursor concepts exist; producer admission, Forget fence and visibility boundary require exact D/Storage proof. |
| E Compiler | FEASIBLE_WITH_CONDITIONS | L–XL | Medium-low | Durable ingress and staged work model plausible; register-before-queue, lineage and recovery integration remain open. |
| F Runtime | FEASIBLE | L | Medium | Structured + lexical first is viable; vector/reranker are safely deferrable. Must consume authoritative authorization/fence filtering. |
| G Context | FEASIBLE_WITH_CONDITIONS | L–XL | Medium-low | Versioned context model plausible; Applied/late evidence and delivery boundary remain unresolved. |
| C Agent Integration | FEASIBLE_WITH_CONDITIONS | L–XL | Medium-low | Adapter boundary is implementable; final request boundary and provider side-effect outcomes remain unapproved/unproven. |
| H BMCP | FEASIBLE_WITH_CONDITIONS | L | Medium | Typed versioned protocol feasible; schema/canonicalization/crypto/interoperability profiles not frozen. |
| I Security & Governance | BLOCKED for policy closure; FEASIBLE_WITH_CONDITIONS for enforcement mechanisms | XL | Medium | I36-GOV-01..10 and Global Forget inventory approvals remain governance-blocked. Do not invent policy. |
| Storage & Consistency | BLOCKED for production topology; FEASIBLE_WITH_CONDITIONS for prototype | XL | Medium | PostgreSQL 18.7 probes are bounded candidate capability evidence; deployed topology, COC persistence and full physical proof remain open. |
| Index & Cache | FEASIBLE_WITH_CONDITIONS | M–L | Medium | Derived-only authority model is clear; rebuild, stale suppression, Forget and migration proof required. |
| Observability & Operations | FEASIBLE_WITH_CONDITIONS | M–L | Medium-low | Metrics and operational duties described; actual runbooks, operator, RPO/RTO and deployment boundary not designated. |
| End-to-end integration | NOT_PROVEN | XL | Low | No complete integrated implementation/conformance evidence; key cross-owner contracts remain open. |

### 2.2 Directly prototypeable vs. not implementation-ready

**Can be prototyped without claiming architecture closure:**
1. Rust workspace skeleton and domain-independent ports/adapters.
2. Typed error/result conventions, tracing correlation, configuration and diagnostics.
3. Read-only structured/lexical retrieval against synthetic fixtures.
4. Blob-store crash-consistency experiment isolated from canonical publication.
5. FTS5/Tantivy and vector-index benchmark harnesses using synthetic/non-sensitive corpora.
6. Model-provider interface and isolated worker spike, with no authority over durable ingress or canonical state.
7. Deterministic reference-model tests for already specified invariants.

**Must not be represented as production implementation or frozen contracts:**
- Canonical commit/visibility transaction, producer admission and Forget fence race.
- Global Forget target inventory/completion.
- Final-request Applied or provider side-effect semantics.
- COC/JF-10 recovery topology and cross-authority crash coupling.
- Production crypto/trust profile, Principal mapping, or unresolved B Fact/Claim semantics.

### 2.3 Technical feasibility risks

| Risk | Severity | Why fundamental | Required proof |
|---|---|---|---|
| No implementation repo/engineering owner | P0 | No accountable place to build, run, version or maintain runtime | A/project authority names repo, branch, owner, maintainers, build/CI and deployment scope (Issue #7). |
| Atomic admission/fence/publication | P0 | A race can resurrect forgotten or unauthorized derived memory | D/E/I/Storage-approved linearization contract plus serial-order, crash, ACK-loss, stale-fence and restore tests (Issue #25). |
| JF-10 Storage/COC coupling | P0 | In-doubt participants must not be heuristically released; visibility/authorization recovery must survive crashes | Selected topology, durable COC, same participant/XID identity, failover/restore and physical fault suite (Issue #10/#29). |
| Applied evidence boundary | P0 | Delivery or ACK cannot be mistaken for actual final-request application | C/G/H exact contract, provider side-effect serialization, Adapter conformance and independent Owner approval (Issue #3). |
| Global Forget governance | P0 | Unknown producers/recipients/backups cannot be silently treated as complete | I-approved closed-world inventory, signed authority and per-target completion evidence (Issue #4/#5). |
| B identity and Fact/Claim | P1 | Wrong identity/epistemic semantics infect all downstream schema and authorization | B-owned ADR and exact typed mapping before dependent schema freeze. |
| Technology overcommitment | P1 | Premature DB/vector/transport choices can cause expensive redesign | Narrow reproducible experiments and ADR decisions; no blanket stack freeze. |
| Resource envelope unknown | P1 | 12–16 GB VRAM is only a planning envelope; host RAM/CPU/GPU/storage/corpus/concurrency unknown | Declare target hardware and benchmark workload; measure p95/p99, RSS, VRAM, disk/WAL and queue age. |
| Recovery/testing underestimated | P1 | Happy-path tests cannot prove crash safety, replay, stale leases, restore or failover | Deterministic state-machine + fault-injection harness with independent review. |

### 2.4 Effort breakdown

| Work package | Relative size | Confidence | Main drivers |
|---|---:|---|---|
| Authority/contract closure and exact source pinning | XL | Medium | Multiple Owners, source drift, approvals, semantics and bilingual parity |
| Storage/COC prototype and physical proof | XL | Low | Transactions, durable coordinator, failover, restore, crash/ACK-loss |
| Core Rust domain + persistence + ingress vertical slice | L–XL | Medium-low | Typed domain, migration, durable acceptance, outbox, idempotency |
| Compiler state machine + provenance + recovery | L–XL | Medium-low | Work leases, staging, lineage, replay, Forget barrier |
| Security/Forget enforcement | XL | Low | I-owned policy, inventory, revocation, cross-owner evidence |
| Context/Adapter/Applied vertical slice | L–XL | Low | Versioning, protocol, provider boundary, late/unknown evidence |
| Basic structured/lexical retrieval | M–L | Medium | SQL filters, FTS, relevance dataset, permission/fence prefilter |
| Vector/reranker/model enhancement | L–XL | Low | Model/data choice, VRAM scheduling, retrieval evaluation |
| Production operations and recovery | XL | Low | Deployment owner, backup/PITR, monitoring, RPO/RTO, runbooks |

No calendar estimate or staffing estimate is made because team size, skill distribution, availability, target hardware and engineering ownership are not established. These sizes must not be converted into dates without those inputs.

### 2.5 Resource and environment requirements

Before implementation commitment:
- Named canonical runtime repository and accountable engineering lead.
- Rust toolchain/version policy, reproducible Cargo workspace, locked dependencies and migration strategy.
- CI for deterministic unit/property/integration tests; physical capability tests separated from ordinary CI.
- Declared OS, CPU, host RAM, GPU model/VRAM, storage medium, filesystem and backup target.
- Declared single-user/multi-user boundary, Agent concurrency, corpus size, blob retention and read/write profile.
- Isolated disposable environment for crash/failover/restore tests; no production fault injection without explicit authorization.
- Secret/key management and test-data redaction policy from I authority.
- Operator, backup/restore owner and incident path before production acceptance.

### 2.6 Required proof-of-feasibility experiments

| Experiment | Minimum result | Gate |
|---|---|---|
| POF-01 SQLite vs PostgreSQL transaction model | Exact write/locking semantics, contention, restart recovery, migration and backup comparison | Storage decision input |
| POF-02 Producer admission vs Forget fence | Both serial orders; crash before/after durable boundaries; no resurrection; unknown fail-closed | P0 architecture proof |
| POF-03 Durable ingress/outbox/lease/replay | ACK only after durable acceptance; duplicate, stale lease, crash, retry and DLQ idempotency | Core slice entry |
| POF-04 Canonical cursor atomicity | Canonical state and cursor recover as one logical commit | Core slice entry |
| POF-05 JF-10 COC/Storage topology | Same participant/XID identity across commit/abort, leader loss, lost ACK, stale primary, restore | Storage/COC gate |
| POF-06 C/G/H Applied boundary | Final request boundary and provider side-effect close-vs-send; no false Applied | Adapter gate |
| POF-07 Forget/recovery/index rebuild | Restore and rebuild never expose suppressed data; stale index/cache fail closed | Security gate |
| POF-08 FTS/vector quality | Labeled query set, recall/precision, latency, memory, update/delete and rebuild | Retrieval enhancement gate |
| POF-09 Model resource isolation | OOM/unavailable model does not lose ingress or block canonical recovery; measured VRAM/CPU/RSS | Optional model gate |
| POF-10 Full local lifecycle | Install, migration, backup, restore, diagnostics, disk-full and upgrade | Local acceptance gate |

## 3. D — Dependency and Critical Path

### 3.1 Architecture Decision Dependency DAG

```text
A0 Project authority: runtime repo + engineering owner
 ├─ B0 Domain identity / Fact-Claim ADR
 ├─ I0 Governance / inventory / trust decisions
 ├─ D0 Canonical lifecycle + cursor authority
 ├─ C/G/H0 Final-request / Applied / provider boundary
 └─ Storage0 transaction + COC topology
       └─ D/E/I/Storage0 atomic admission-fence-dependency-visibility contract
             └─ A integration disposition (without replacing Owner authority)
                   └─ Architecture implementation-entry decision
```

Ordering constraints:
- B identity and Fact/Claim decisions precede dependent schema/type freeze.
- I policy decisions precede authorization, inventory, revocation and Global Forget enforcement.
- D/E/I/Storage participant semantics must be mutually consistent before publication implementation.
- C/G/H final-request semantics must be resolved before Applied implementation.
- Storage topology and JF-10 proof must precede production consistency claims.
- Technology ADRs must follow owner contracts and experiments, not precede them.

### 3.2 Implementation Dependency DAG

```text
P0-0: implementation repo / accountable owner / reproducible build
  -> P0-1: frozen-enough domain types + shared contracts (B/A/H, owner decisions)
  -> P0-2: storage ports + durable transaction/identity model (Storage/D)
  -> P0-3: durable ingress + outbox + work ledger (E)
  -> P0-4: canonical lifecycle + cursor + evidence (D)
  -> P0-5: producer admission / Forget fence / lineage / visibility gate (D/E/I/Storage)
  -> P0-6: authorized read + structured/lexical retrieval (F)
  -> P0-7: Context plan/version/delivery (G/H)
  -> P0-8: final request / Applied proof (C/G/H + I/D)
  -> P0-9: recovery, restore, rebuild and end-to-end conformance
  -> production acceptance (separate operational gate)
```

This is a logical dependency chain, not a requirement that all code be written serially. Interfaces, fixtures, test harnesses and isolated experiments can be prepared in parallel.

### 3.3 Verification Dependency DAG

```text
Source exact pins + owner authority evidence
  -> contract consistency review
  -> model/schema validators and negative tests
  -> component tests
  -> cross-owner contract tests
  -> crash/race/replay/restore/failover tests
  -> independent review of evidence
  -> local deployment acceptance
  -> production operational acceptance
```

A lower-layer test cannot substitute for a higher layer: schema validation != semantic conformance; reference-model tests != physical DB proof; CI capability != deployed topology; Adapter ACK != model comprehension.

### 3.4 Dependency Register

| ID | Upstream → Downstream | Type | Required artifact / owner | Closure evidence | Blocking condition / parallelism |
|---|---|---|---|---|---|
| DEP-01 | Project authority → runtime build | Hard + External | Runtime repo, lead, maintainers, build/CI; A/project authority | Issue #7 answered with exact repo/branch/owner | Blocks implementation start; docs/prototype prep can proceed |
| DEP-02 | B domain semantics → all schemas | Hard + Ordering | B ADR and typed identity contracts; B | Exact B decision + consumer map | Blocks dependent schema freeze; independent benchmarks parallel |
| DEP-03 | I governance → auth/Forget enforcement | Hard | I36-GOV decisions + InventorySeal; I | Signed authority/policy evidence, target completeness | Blocks policy closure/production Forget; non-policy harness prep parallel |
| DEP-04 | D/E/I/Storage → publication | Hard | Atomic admission/fence/lineage/visibility contract; D/E/I/Storage | Exact owner dispositions + crash/race evidence | Blocks publication implementation/acceptance |
| DEP-05 | Storage topology → JF-10 | Hard + External | Selected DB/coordinator/topology and runbook; Storage/A | Actual topology, durable COC, failover/restore proof | Blocks production consistency; isolated DB comparisons parallel |
| DEP-06 | C/G/H (+I/D) → Applied | Hard | Final-request boundary, schema, provider outcome, permission/fence evidence | Exact owner decisions + adapter/provider conformance | Blocks Applied claims |
| DEP-07 | Durable ingress → compiler | Hard | Event receipt + durable work/outbox contract; E/Storage | Crash/replay/idempotency proof | Blocks reliable Compiler |
| DEP-08 | Canonical commit → indexes | Hard | Canonical event/cursor + outbox contract; D/Storage | Atomic commit + replay watermark proof | Blocks authoritative indexing; F benchmark on fixtures parallel |
| DEP-09 | Authorized retrieval → Context | Hard | Permission/fence prefilter and typed candidate contract; I/F/D | Negative tests for leakage and stale suppression | Blocks production context assembly |
| DEP-10 | Context version → delivery | Hard | G context version and H wire contract | Gap/replay/reconnect conformance | Blocks delivery acceptance |
| DEP-11 | Restore proof → service exposure | Hard + Evidence | Backup manifest, current governance replay, anti-rollback; Storage/I/D | Restore isolation and high-water proof | Blocks restored data exposure |
| DEP-12 | Bilingual source parity → architecture PR acceptance | Hard + Evidence | GOV-DOC-001 paired files; all authors/A | semantic parity report, exact source revisions | Blocks docs acceptance, not isolated experiments |
| DEP-13 | Target hardware/workload → performance SLO | Evidence | Hardware/corpus/concurrency profile; A/F/Engineering | Reproducible benchmark manifest | Blocks SLO claims, not functional prototypes |

### 3.5 Critical Path Analysis

**Critical path (root-first):** identify implementation authority → close B/I/D/E/C/G/H/Storage owner-owned semantic prerequisites → select and prove Storage/COC topology → prove durable ingress and canonical commit → prove atomic Forget/publication gate → prove authorized retrieval and context delivery → prove final-request Applied → run full crash/recovery/restore/failover campaign → independent review → local/production gates.

The greatest uncertainty is concentrated in cross-authority Storage/COC/Forget/Applied correctness, not in vector search or model inference. Calendar duration cannot be calculated until engineering capacity and external decision latency are known.

### 3.6 Parallelizable workstreams

Can proceed without releasing architecture gates:
1. FTS5 vs Tantivy and vector candidate benchmarks on synthetic fixtures.
2. Rust workspace/build conventions, typed error/tracing conventions, test harness skeleton in a separately authorized implementation repository (not this architecture repository).
3. Storage engine capability comparisons in disposable test environments.
4. Failure matrix expansion and deterministic state-machine model tests.
5. Hardware/workload inventory and benchmark dataset design.
6. Bilingual docs, source pin ledger and exact-owner question preparation.
7. Adapter test harness and BMCP compatibility tests using explicitly marked candidate contracts only.

Do not proceed into authoritative implementation: canonical visibility transaction, production authorization/Forget, final Applied claims, Global Forget completion or production topology activation.

## 4. P — Root-first Development Priority

### 4.1 Root-first Priority Matrix

| Priority | Work | Why it is root-level | Complexity | Risk reduction | Owner |
|---|---|---|---:|---|---|
| P0-01 | Designate implementation repo, accountable engineering owner, maintainers and build evidence | Without a place/owner, no delivery can be owned or verified | M | Critical | A/project authority |
| P0-02 | Close B identity + Fact/Claim and canonical domain prerequisites | All schemas, authorization and lineage depend on domain truth | L | Critical | B |
| P0-03 | Close I governance, inventory and authorization prerequisites | Unknown producer/recipient/backup cannot be treated as safe or complete | XL | Critical | I + external authorities |
| P0-04 | Prove D/E/I/Storage admission–fence–dependency–visibility atomicity | Prevents forgotten/unauthorized work from becoming visible | XL | Critical | D/E/I/Storage |
| P0-05 | Select and physically prove Storage/COC/JF-10 topology | Prevents heuristic recovery, split brain and false terminality | XL | Critical | Storage/A + D/I |
| P0-06 | Close C/G/H final-request and Applied boundary | Prevents delivery/ACK from being misreported as Applied | XL | Critical | C/G/H + I/D |
| P0-07 | Durable ingress, outbox, canonical commit and recovery vertical slice | Proves the Brain can accept and preserve source data correctly | L–XL | Very high | E/D/Storage |
| P0-08 | Security-filtered structured/lexical retrieval and Forget-safe rebuild | First useful read path without premature vector complexity | M–L | High | F + I/D/Storage |
| P1-01 | Context version/delivery/reconnect vertical slice | Completes useful read-to-Agent path after contracts are closed | L–XL | High | G/H/C |
| P1-02 | Full cross-owner conformance and fault campaign | Proves serial order, crash, replay, restore and unknown behavior | XL | Very high | A + all relevant Owners |
| P1-03 | Backup/restore, migration, diagnostics and operator readiness | Makes local system recoverable and maintainable | L–XL | High | Storage/A/Engineering + I |
| P2-01 | Vector retrieval, hybrid ranking, reranker | Improves recall quality after trustworthy canonical data and evaluation exist | L–XL | Medium | F |
| P2-02 | Model-assisted extraction, entity resolution and summarization quality | Adds intelligence but cannot substitute for provenance and deterministic gates | L–XL | Medium | E/F + B |
| P2-03 | Multi-agent concurrency and larger corpus scaling | Scale after workload proves need | L–XL | Medium | Engineering/Storage/F |
| P3-01 | Distributed services, Kafka, Kubernetes, hosted vector DB | Adds operational burden before need is measured | XL | Low initially | A/Engineering |
| P3-02 | Advanced autonomous agent planning/tool execution | Outside Brain's core boundary | XL | None to core memory correctness | Separate product boundary |

### 4.2 Priority item inputs and exits

| ID | Inputs / root dependency | Gate | Completion evidence / exit |
|---|---|---|---|
| P0-01 | Project authority response; Issue #7 | No implementation entry before owner designation | Repo URL/default branch, named accountable lead/maintainers, build and CI command, code-to-contract traceability |
| P0-02 | B exact source + consumer dependencies | Blocks dependent schema/type freeze | B decision/ADR with typed identifiers, Fact/Claim semantics, consumer acceptance and bilingual parity |
| P0-03 | I governance authority and target inventory | Blocks production authorization/Forget claims | I36-GOV decisions, InventorySeal, target/backup/recipient coverage, explicit exceptions and approval evidence |
| P0-04 | D/E/I/Storage exact owner artifacts | Blocks canonical publication | Both serial orders, crash/ACK-loss, stale lease/fence, complete dependency registration, hidden-on-UNKNOWN |
| P0-05 | Storage candidate profile, A COC design, operator environment | Blocks production consistency | Actual DB/coordinator selected, same participant/XID, quorum/failover/restore/old-primary fencing, physical test traces |
| P0-06 | C/G/H contracts + I/D evidence | Blocks Applied status | Final request boundary, provider side-effect outcome, schema/crypto/interoperability and Adapter conformance |
| P0-07 | P0-01..05 sufficient contract closure | Blocks useful end-to-end write path | Durable ACK, replay-safe work, canonical commit+cursor atomicity, provenance and recovery |
| P0-08 | P0-02..05 + canonical fixtures | Blocks safe recall | Scope/Permission/fence enforced before ranking; stale index/cache cannot leak; rebuild suppression proof |
| P1-01 | P0-06 and P0-08 | Blocks applied-context workflow | Version gap, delivery, reconnect, stale permission/fence and exact Applied evidence |
| P1-02 | All critical contracts and physical topology | Blocks system acceptance | Reproducible test matrix and independent review, with unknown states fail-closed |
| P1-03 | Runtime deployment boundary and operator | Blocks production acceptance | Restore drill, migration, disk-full, monitoring, runbooks, RPO/RTO and named on-call |
| P2-01 | Stable canonical dataset + labeled eval set | Retrieval quality gate | Precision/recall/latency/memory/update/delete/rebuild benchmark |
| P2-02 | Provenance and deterministic compiler stages | Quality gate | Model proposals never become facts without policy; quality measured against human-labeled set |
| P2-03 | Measured workload threshold | Scale gate | Load test and cost/latency evidence justify scale change |
| P3-01 | Measured multi-node need and operator capacity | Separate architecture decision | ADR plus operational and failure-domain evidence |
| P3-02 | Separate product decision | Outside core Brain scope | Explicit scope/authority change |

### 4.3 Preventing easy-feature bias

- Every sprint/work package must identify the P0 gate it reduces or state that it is a bounded parallel experiment.
- P2/P3 features cannot displace unresolved P0 work solely because they are easier to demo.
- Maintain a visible “P0 evidence debt” list: missing authority, exact artifact, experiment, owner, or independent review.
- No feature is “done” because a UI/demo works if data authority, permission, Forget and recovery are unproven.
- Reserve capacity for test harnesses, fault injection and evidence review; do not allocate all effort to feature code.
- A may coordinate sequencing but cannot decide B/I/D/E/C/G/H/Storage semantics for those Owners.

## 5. Development Phase Roadmap

| Phase | Purpose | Allowed work | Entry gate | Exit gate |
|---|---|---|---|---|
| 0 — Authority & evidence closure | Establish who builds what and which contracts control | Issue #7 closure; exact source pins; Owner decisions; bilingual parity; dependency ledger | Current architecture review | Named repo/lead; no hidden authority ambiguity; blockers assigned |
| 1 — Feasibility spikes | Reduce high-risk technical unknowns before implementation | POF-01..10, harnesses, synthetic data, DB/COC experiments | Disposable environment and accountable spike owners | Reproducible results; ADR decisions or explicit BLOCKED outcomes |
| 2 — Core durable vertical slice | Prove reliable source acceptance and canonical memory | Domain types, durable ingress/outbox, canonical lifecycle/cursor, provenance | B/D/E/Storage contracts sufficiently closed; Storage prototype accepted | Crash/replay/idempotency tests; no false Accepted/Committed |
| 3 — Safe retrieval & context | Prove authorized retrieval and context synchronization | Structured/lexical retrieval, context version, BMCP candidate integration | I authorization + Forget filtering; C/G/H contracts | No leakage; reconnect/version-gap behavior; Applied remains distinct |
| 4 — Forget & recovery conformance | Prove atomic suppression and restore safety | D/E/I/Storage publication gate, COC/JF-10, index/cache rebuild, fault suite | Selected topology and owner approvals | All P0 race/crash/failover/restore cases pass; unknown remains fail-closed |
| 5 — Local operational acceptance | Prove install, maintain, recover | Migration, backup/restore, diagnostics, monitoring, resource budgets | Core vertical slices + conformance | Named operator, runbooks, measured RPO/RTO and resource envelope |
| 6 — Quality and scale | Improve memory usefulness and capacity | Vector, reranking, model assistance, multi-agent scale | Reliable baseline + labeled evaluation + measured demand | Quality/cost/latency improvement reproducible; no invariant regression |

No phase duration is assigned. Phase transitions are evidence-gated, not calendar-gated.

## 6. Deferred Features Register

| Feature | Priority | Reason for deferral | Re-entry condition |
|---|---|---|---|
| Vector ANN and reranking | P2 | Lexical/structured baseline can validate data correctness first; vector choice depends on corpus and recall metrics | Labeled eval set and measured lexical gap |
| Advanced local LLM extraction/summarization | P2 | Model output is probabilistic and cannot repair unresolved provenance/domain semantics | Stable source/evidence contracts and measured model quality/resource profile |
| Multi-model concurrent GPU inference | P2 | 12–16 GB VRAM planning envelope is constrained and hardware unknown | Actual GPU benchmark and admission scheduler |
| Multi-user/distributed deployment | P2/P3 | No workload or operational owner proves need; increases failure domains | Concurrency/availability requirement and operator capability |
| Kafka/Kubernetes/microservices | P3 | Explicitly not required by initial local-first blueprint | Measured bottleneck and ADR showing benefit outweighs operational cost |
| Hosted vector database | P3 | Conflicts with local-first baseline absent justified need | Data residency/security decision and scale evidence |
| Autonomous Agent planner/tool execution | P3/out of scope | Brain is memory infrastructure, not an Agent framework | Separate product scope and authority |
| Physical erasure guarantees | Not a feature shortcut | Logical tombstone or primary-row delete is not proof of backup/export/recipient erasure | I-approved inventory and verifiable per-target erasure evidence |

## 7. Resource and Effort Assessment

- Team size, skills, availability, delivery capacity and budget are **UNKNOWN**. No staffing or calendar plan is asserted.
- TAB-001's 12–16 GB VRAM is a planning envelope, not a confirmed machine profile. Host RAM, CPU, GPU model, storage, OS, corpus and concurrency remain unknown.
- TAB-001 suggests 16 GB host RAM as minimal functional testing, 32 GB as preferred initial local development/acceptance, and 64 GB+ for larger corpus/concurrency; these are planning tiers, not guarantees.
- Correctness-critical transactions, crash recovery, security, Forget and Applied evidence need senior systems/storage/security expertise; Rust fluency alone is insufficient.
- Required capabilities include Rust async/concurrency, transactional databases, distributed-systems failure reasoning, protocol/schema evolution, security/identity, retrieval evaluation, test automation and operations.
- The project should not assume a single developer can safely make all Owner decisions. Role simulation by one model/session is not independent approval.

## 8. Three-role Cross-examination

### F reviews D
**Challenge:** D's DAG risks making all contract closure appear fully serial. Storage engine comparisons, harness scaffolding, FTS/vector benchmarks, resource inventory and bilingual evidence work can proceed in parallel without releasing gates. Conversely, D must include external governance and engineering-owner dependencies, not just code-module edges.

**Disposition:** D's graph is accepted with the parallel workstreams in §3.6. Critical path remains cross-owner semantics and physical Storage/COC proof.

### D reviews P
**Challenge:** P must not schedule a “durable vertical slice” before D/E/Storage admission, canonical cursor, and I authorization boundaries are precise enough. Nor can retrieval begin with production data before authorization and Forget suppression are enforced. P0-07 is therefore conditional on P0-02..05.

**Disposition:** P0-07 is explicitly downstream of root contract and Storage proof. P0-08 requires pre-ranking authorization/fence filtering.

### P reviews F
**Challenge:** F's effort estimates could accidentally prioritize a broad XL architecture-closure effort without identifying the smallest risk-reducing proof. The project needs narrow experiments with crisp exits, not an attempt to implement every module at once. F must also count the cost of independent review and bilingual parity.

**Disposition:** Effort is decomposed into proof packages and vertical slices; XL items are not a single monolithic work package.

### Additional risks identified by each role
- F: staffing and operator capability are unknown; no feasibility claim about delivery date can be made.
- D: exact main HEAD and source freshness need a machine-verifiable source pin ledger; current connector search does not expose branch HEAD directly.
- P: easy-to-demo vector/model features may crowd out P0 safety and authority work; use gate-linked allocation.

### Conflicts requiring A decision
1. The initial implementation topology (SQLite modular monolith) is a candidate, while Issue #10 JF-10 work uses PostgreSQL 18.7 physical capability probes. These are not necessarily contradictory: local MVP vs. production JF-10 topology may differ, but A/Storage must explicitly define whether a single topology is required and how semantic guarantees transfer. Do not silently choose either.
2. TAB-001 proposes a local-first single-node starting point, while the current cross-owner publication/COC contract implies stronger serialization and durable coordinator needs. A must decide whether first release scope excludes those capabilities or whether they are mandatory in the first vertical slice; cannot reduce safety semantics by implication.
3. The repository is architecture-only, while several issues discuss implementation and physical tests. A/project authority must decide whether to create/identify a separate runtime repo and how evidence links across repos.

## 9. Open Questions for A

1. What is the canonical runtime implementation repository, default branch, accountable engineering lead and maintainer set? (Issue #7)
2. Is the first product single-user/local-only, or must the first release support multiple users/Agents and remote adapters?
3. Are Forget atomicity, authorization revocation, final-request Applied and JF-10 mandatory in the first usable release, or are there explicitly isolated capability tiers? No safety weakening is implied.
4. Must the first release use one Storage/COC topology? How do SQLite local prototype and PostgreSQL 18.7 JF-10 evidence relate?
5. Who owns the deployed physical environment, operator/on-call, backup/PITR, RPO/RTO and key custody?
6. What hardware is the target baseline (OS, CPU, host RAM, GPU/VRAM, disk, filesystem)?
7. What corpus, event rate, Agent concurrency, read/write ratio, retention and latency targets define the first benchmark?
8. What is the governance path and approver for B Fact/Claim, I36-GOV-01..10, Global Forget and C/G/H Applied?
9. Which exact Owner branches/commits are authoritative for each dependency at each gate? How will freshness be automatically rechecked?
10. What constitutes implementation entry: all P0 owner decisions, selected Storage topology, or an explicitly bounded prototype exception?

## 10. Final Acceptance

| Question | Verdict | Rationale |
|---|---|---|
| Is the current architecture implementable in principle? | PARTIALLY VERIFIED — FEASIBLE_WITH_CONDITIONS | Candidate Rust modular-monolith direction is plausible; several critical contracts/topology are open. |
| Is the complete system ready for implementation now? | BLOCKED | Runtime repo/owner absent; P0 owner contracts and physical proofs incomplete. |
| Fundamental critical path? | VERIFIED at dependency level | Authority → domain/security/transaction contracts → Storage/COC proof → durable core → Forget/publication → authorized retrieval/context → Applied → full recovery/operations. |
| Highest root-first priorities? | VERIFIED as planning recommendation | P0-01..P0-08 in §4. |
| What must be completed first? | BLOCKED until owner decisions | Issue #7, B semantics, I governance/inventory, D/E/I/Storage atomicity, Storage/COC topology, C/G/H Applied boundary. |
| What can run in parallel? | VERIFIED as bounded preparation | Synthetic retrieval benchmarks, harnesses, Storage candidate probes, hardware inventory, docs/source pinning. |
| What must be deferred? | VERIFIED as recommendation | Vector/reranker, advanced model intelligence, distributed stack and Agent planner/tool execution. |
| Most important engineering blocker? | BLOCKED | No designated runtime implementation repository/accountable engineering owner; after that, P0 cross-authority atomicity and JF-10 topology proof. |

**Recommendation to A:** keep architecture and implementation gates separate. First close ownership and authority gaps; then run the narrow P0 proof experiments; only then authorize a bounded core vertical slice. Do not interpret this report or the PR as Gate PASS, Owner approval, implementation start, production readiness, or permission to merge.

## 11. Source Register

- Repository README.md — Blob `429e873bd5bf081e10a449b27e3495428e1046f1`.
- `14-ai-development/README.md` — Blob `9593fd66f2b830748d826d754ce3e6da00e6f144`.
- `docs/README.md` — Blob `c6420882476fc905ce313d93c809ba4896b2c542`.
- TAB-001 — Blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`.
- Architecture Roadmap — Blob `29289361973ec4369f067706132190793cd57a6b`.
- System Overview — Blob `995a1c5a3815d7e7b81b8d7f2ccc546c91d4c256`.
- Component Map — Blob `ddb7a1571463cadce83d89f62b03526c4f9693e8`.
- Architecture Invariants — Blob `33b037318e459ebb73bea33b3186f31a41d5dcfe`.
- GOV-DOC-001 — Blob `b51b054b9f1022133666542680df74dfe19de2fb`.
- Issue #43 — System-wide architecture consolidation.
- Issue #25 — D/E/I/Storage producer admission and publication gate.
- Issue #29 — HRC/RecoveryJoin and physical topology proof.
- Issue #10 — JF-10 sequential gates.
- Issue #3 — C/G/H Applied contract.
- Issue #7 — Runtime implementation repository and engineering owner.
- Issues #4/#5 — I governance and Global Forget approvals.

Source freshness limitation: the listed Blob SHAs are exact for the fetched `main` files at review time; Owner-branch exact artifacts are not exhaustively rebound in this session. This is a system-level planning report and must not replace per-Owner exact-source approval.
