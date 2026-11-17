# ARCH-CONVERGENCE-001 — Integration Synthesis & Cross-Workstream Review
# ARCH-CONVERGENCE-001 — 集成综合与跨工作流审查

- Program: ARCH-CONVERGENCE-001
- Status: **DRAFT / INTERIM INTEGRATION REVIEW / NON-NORMATIVE**
- Review anchor: `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Scope: A–E proposal integration, conflict reconciliation, dependency order and gate disposition.
- This document is not the final independent acceptance review. No Owner contract, ADR, schema, technology or production Gate is approved by this document.

## 1. Executive disposition / 执行结论

The five workstreams have produced useful and substantially compatible proposals, but the architecture is **not yet converged and is not implementation-authorized**.

The strongest common architecture is a single deployable Rust modular monolith, retaining A–I as logical authority boundaries; one Canonical Memory transaction domain per Brain authority; a narrow SQL durable-work/outbox substrate; canonical typed records; derived lexical projections; and replaceable runtime/provider/protocol adapters. SQLite and PostgreSQL remain alternative L4 profiles. No external product is approved as a canonical authority.

The proposals correctly refuse to solve the blocked B Fact/Claim model with arbitrary JSON, to treat workflow ACK as business completion, to infer Applied from retrieval or delivery, or to equate local Forget suppression with global physical erasure.

The remaining blockers are not cosmetic documentation gaps. They concern (a) Evidence/Provenance ownership, (b) B Fact/Claim semantics, (c) the cross-authority ordering between D/Storage, I's revocation sequencer and COC, (d) physical L4 transaction/recovery proof, (e) closed-world Forget inventory and restore, and (f) exact C/H/G Applied evidence mapping. These prevent a correct end-to-end Brain claim.

**Disposition: continue contract resolution and owner acceptance; do not begin a full Brain implementation or freeze schemas.** A narrowly scoped Canonical Core prototype may be planned only after B's neutral-candidate boundary, D/Storage write set and I/D admission gates are explicitly accepted for that profile.

五个工作流已经形成有价值且大体兼容的提案，但架构**尚未收敛，也未获实现授权**。

当前最一致的架构方向是：单一可部署 Rust 模块化单体，A–I 保持逻辑权威边界；每个 Brain Authority 一个 Canonical Memory 事务域；采用窄范围 SQL Durable Work/Outbox；保留强类型规范记录、派生词法投影和可替换的 Runtime/Provider/Protocol Adapter。SQLite 与 PostgreSQL 仍是 L4 候选 Profile。没有外部产品获批成为规范权威。

各提案正确地拒绝用任意 JSON 绕过 B 的 Fact/Claim 阻塞、将 Workflow ACK 当作业务完成、从检索或投递推断 Applied，或把本地 Forget 抑制等同于全局物理擦除。

剩余阻塞不是文档形式问题，而是 Evidence/Provenance 归属、Fact/Claim 语义、D/Storage 与 I 撤销序列器及 COC 之间的跨权威排序、L4 物理事务/恢复证明、Forget 封闭世界清单与恢复，以及 C/H/G Applied 精确证据映射。这些问题阻止系统宣称端到端正确。

**处置：继续合同解决和 Owner 接受；不得启动完整 Brain 实现或冻结 Schema。** 只有 B 中立候选边界、D/Storage 写集合以及 I/D Admission Gate 针对目标 Profile 得到明确接受后，才可规划范围受限的 Canonical Core 原型。

## 2. Refreshed GitHub baseline / 已刷新 GitHub 基线

### 2.1 Repository and PR state

| Item | Live observation |
|---|---|
| Repository | `oahcom/AiMemoryBrainArchitecture` |
| Default branch | `main` |
| Main HEAD | `e52594f181d2edb77448adcfed64a0fbdffaf3aa` |
| PR #89 PRODUCT-FIRST integration | Open / Draft / Unmerged |
| PRODUCT-FIRST PRs #74–#79 | All Open / Draft / Unmerged |
| ARCH-CONVERGENCE #99 A | Open / Draft / Unmerged |
| ARCH-CONVERGENCE #101 B | Open / Draft / Unmerged |
| ARCH-CONVERGENCE #103 C | Open / Draft / Unmerged |
| ARCH-CONVERGENCE #104 D | Open / Draft / Unmerged |
| ARCH-CONVERGENCE #106 E | Open / Draft / Unmerged |

The five ARCH workstream PR heads recorded in their PR bodies are:

| Workstream | PR | Branch | Proposal commit |
|---|---:|---|---|
| A — Source of Truth | #99 | `arch-convergence-001/workstream-a-source-of-truth` | `63c0fd869d8685d3bc1768aba0ec2d50b0f4f84f` |
| B — Canonical Transaction | #101 | `arch-convergence-001/workstream-b-canonical-transaction` | `89659270efb379b4a04d851bcdc95c50fafa23e4` |
| C — Forget/Auth/Recovery | #103 | `arch-convergence-001/workstream-c-forget-auth-recovery` | `669a24deefe1195187915014f70a2d97f71e0ebf` |
| D — Context Applied/Runtime | #104 | `arch-convergence-001/workstream-d-context-applied-runtime` | `bf3ac0e76ae060ff118cc0e6545cd188c3e85205` |
| E — Minimum Runnable Architecture | #106 | `arch-convergence-001/workstream-e-minimum-runnable-architecture` | `53dc4f4cf564a60d584e171ff0921f2ed0f236b2` |

All five target `main`. These PRs are documentation proposals; their existence and GitHub mergeability do not constitute Owner approval.

### 2.2 Product research status

PR #74 Memory Products, #75 Durable Execution, #76 Security/Governance, #77 Agent Runtime, #78 Storage/Search and #79 Architecture Simplification all remain Draft research proposals. PR #89 remains a Draft integration proposal. None is treated as merged, approved or as a technology freeze.

### 2.3 Source correction and branch integrity

- PR #89's report says `02-domain-model/` is missing from main. This is factually incorrect: main contains `02-domain-model/` and six files. Preserve #89 as historical Draft; correct the claim only in a successor report.
- H's historical tree-collapse incident is recovered at the live branch-tree level. PR #90's current re-read identifies live H HEAD `6608cde89d959257db612d8ff8080f631333f3f3`, seven commits ahead of intact baseline `0d36324457e39bd50ad56ae902d477c4ea765b61`, with the destructive incident snapshot absent from current ancestry. The current tree has 248 entries; the source inventory's 216 figure is a blob count, not the same metric. Applied Evidence CI 11/11 is tied to `4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6`; H tip differs by documentation-only changes, so do not call the run literally attached to current HEAD.
- C's historical tree-collapse incident is likewise recovered at live branch-tree level. Current C HEAD is `88992da30331121b81cf2773acab11d921daf281`; compare from incident snapshot `a5dff993e5c2928a28deb777c41023cfe923366f` is one commit ahead with the restored 136-blob tree. C Provider Outcome 19/19 is bounded candidate conformance, not C/Brain end-to-end proof.
- PR #92 says H identity tuple shape is a candidate, but exact COutcomeRecord and final-boundary mapping is NOT ACCEPTED / NOT VERIFIED. It also records a G source discrepancy concerning `final_request_boundary_id`; G must correct/resolve its own contract rather than having the integration layer silently reinterpret it.
- PR #94's C workflow path-filter correction remains Draft; schema-only trigger execution is pending. Do not claim that trigger path is proven.

## 3. Cross-workstream architecture that is mutually supportable / 可共同支持的架构

### 3.1 Authority map

| Authority | Owner | Integration rule |
|---|---|---|
| Domain meaning and typed Fact/Claim semantics | B + Architecture Governance decision | Fact/Claim remains blocked; neutral typed candidate only |
| Canonical Memory identity, immutable versions, lifecycle and canonical Forget fence | D | D owns semantic truth; no product/workflow/store may replace it |
| Physical serialization, visibility, outbox and restore mechanics | Storage | Implements D's semantic contract; does not acquire domain truth |
| Ingestion receipt, compiler attempts, producer work and provenance preparation | E | Durable acceptance is not canonical truth; publication requires D/Storage gate |
| Retrieval/index/cache and activation | F | Derived only; current D/I checks before candidate emission and final disclosure |
| ContextVersion, delivery intent and durable Applied decision | G | Only G writes Applied; evidence must be bound to exact request and current authority state |
| Provider attempt, final egress and provider handoff outcome | C | Handoff outcome is not model completion or G Applied |
| BMCP wire, Adapter capability and authenticated evidence transport | H | Transport/Adapter evidence is not G Applied or Brain authorization |
| Principal, authorization, revocation, PermissionEpoch and global Forget policy | I | PDP product is evaluator only; errors fail closed |
| COC/JF-10 consistency/recovery evidence | COC + Storage with relevant Owners | Separate authority/log; no silent folding into SQL or G Applied |

### 3.2 Canonical transaction minimum

The B proposal's minimum atomic set is the right candidate boundary: canonical object/version writes, aggregate-head CAS, required typed evidence/provenance references (or explicitly permitted unavailability reason), lifecycle append where applicable, canonical commit receipt/idempotency result, D CanonicalCommitCursor, and durable outbox intent. Readers must observe all or none.

Storage L1 Option A is a logical decision only: one serializable transaction domain per Canonical Memory authority. L4 engine/version/configuration/deployment, anchor-row implementation, read path, HA/PITR and restore proof remain OPEN. No SQLite/PostgreSQL selection follows from L1.

A critical cross-log issue remains: I's PermissionEpoch/revocation sequencer and COC's quorum/recovery log are distinct authorities. The final D/Storage commit cannot pretend to include those remote logs in one ordinary SQL ACID transaction. Owners must define the exact single-use receipt issue/consume ordering, durable operation identity, crash reconciliation, and outcomes when I/COC is unavailable or indeterminate. A detached Permit, stale epoch, timeout or workflow ACK cannot substitute for that protocol.

### 3.3 Forget and visibility

Keep these outcomes distinct:
1. D Fence established and canonical-domain reads/publications suppressed.
2. Owner-specific work, projection, cache, context, Adapter and recipient cleanup reconciled.
3. I evaluates closed-world producer/recipient/backup inventory and authorized exceptions for global completion.
4. Physical erasure evidence is separately issued by the authority capable of proving the relevant storage/recipient copy.

Fence installation must be ordered against producer registration and final visibility. All work must be registered before lease/execute/retry/DLQ/replay/publication. Any unknown work or target keeps the relevant barrier open. Restore starts quarantined and requires fresh COC/I/D/Storage high-water and participant proofs before serving.

### 3.4 Context Applied

The stage names remain separate: retrieval candidate → ContextVersion → delivery → materialization → exact final request submitted → G Applied. Only G may commit Applied. Full Applied requires the same immutable identity/revision to join C's actual submit outcome, H's authenticated Adapter/final-request evidence, I authorization currentness, D Forget currentness, and COC/Storage terminal evidence where the transaction profile requires it. No model attention/use claim is implied.

## 4. Consolidated conflict register / 综合冲突登记

All entries remain OPEN unless the closure evidence is explicitly recorded. Priority is an integration Gate classification, not a unilateral Owner severity change.

| ID | Conflict / missing contract | Accountable owner(s) | Gate | Required closure evidence |
|---|---|---|---|---|
| INT-001 | Evidence/Provenance semantic record authority and write API are split across B semantics, E binding and D canonical persistence | B, D, E, Architecture Governance | P0 | One explicit authority statement, record identity, write path, mutation/immutability rules and consumer acceptance |
| INT-002 | Fact/Claim canonical semantics remain ADR-BLOCKED and conflict with parts of main domain/governance wording | B + Architecture Governance; D/E/F/G/H consulted | P0 | Approved ADR or formally approved neutral-only first-slice boundary; exact downstream mappings |
| INT-003 | D/Storage L1 logical serializable domain lacks exact production row/anchor ownership and L4 engine/profile | D + Storage | P0 | Exact schema/row ownership, engine/version/config, isolation/locking proof, crash/failover/PITR/restore tests |
| INT-004 | I PermissionEpoch/revocation sequencer, D/Storage canonical commit and COC quorum log are separate authorities with no proven cross-log commit protocol | I, D, Storage, COC; C consulted | P0 | Single-use receipt ordering/consumption, stable operation identity, durable recovery state machine and fault-injection evidence |
| INT-005 | Forget closed-world inventory, producer/recipient registration and global completion are candidate/incomplete | I + D + E/F/G/H/Storage | P0 | Sealed complete inventory, high-water coverage, target evidence, exception governance and restore anti-rollback proof |
| INT-006 | G Full Applied exact field/identity mapping across C/H/I/D/Storage/COC is not accepted end-to-end | G + C + H + I + D + Storage + COC | P0 | Exact pinned schema crosswalk, corrected G source, signed/authenticated evidence trust, same-request test and durable G commit |
| INT-007 | CSubmitOutcome 1.0.1 / H Unified 1.2.15 / Applied Delivery Evidence 1.0.0 / Storage recovery bundle compatibility not frozen as one manifest | C + H + Storage; G/I review | P0 | Exact compatible bundle manifest, schema/validator hashes, cross-language vectors and exact-head CI |
| INT-008 | ProducerWorkItemId ownership/issuance is expressed as D ledger / E consumer; interface and admission ordering need one exact API | D + E + Storage | P0 | Issuer, namespace, digest, registration receipt, lease fencing and retry/DLQ/replay semantics accepted |
| INT-009 | Main source publication and README path map diverge from Owner branch source roots; detailed normative contracts absent from main | A + each Owner + Governance | P1 | Canonical paths/index, exact version pins, redirects/history and publication approval |
| INT-010 | PR #89 contains an incorrect missing-directory claim for `02-domain-model/` | PRODUCT-FIRST integration owner / A | P1 | Successor report correction; retain #89 as historical draft |
| INT-011 | A conflict register's H incident status is stale relative to PR #90 live re-read; tree metrics need explicit distinction | A + H | P1 | A updates CF-009 from unreconciled to recovered-at-live-tree; retain CI-currentness caveat |
| INT-012 | C/H tree recovery is not equivalent to production trust or exact current-head integration acceptance | C + H | P1 | Exact-head workflow evidence and crypto/key/replay/Adapter/restore integration tests |
| INT-013 | Bilingual parity for detailed Owner contracts, schemas, validators and error/state enums remains incomplete | All Owners + A | P1 | Per-file semantic parity checklist, exact paired blobs and Owner review |
| INT-014 | SQLite local and PostgreSQL server profile cannot be chosen without workload and physical recovery evidence | Storage + D + Engineering | P1 | Representative benchmark, concurrency profile, HA/PITR, backup/restore, ops and rollback comparison |
| INT-015 | Cedar is only a candidate evaluator; I must own wrapper, PEP and fail-closed semantics | I + Security Governance | P1 | I-approved wrapper, error/unknown vectors, epoch freshness and revocation tests |
| INT-016 | Product research proposals do not authorize adoption or transfer Brain authority | Relevant product Owners + Governance | P1 | Product-specific ADR, measured benchmark, security/license review, adapter conformance and rollback trigger |
| INT-017 | Durable SQL work/outbox, E work lifecycle, D producer barrier and Storage visibility are related but distinct state machines | E + D + Storage | P0 | Exact crosswalk of logical work, attempt, lease, registration, publication and terminal states |
| INT-018 | Restore proofs from COC/I/D/Storage are proposed but physical restore/anti-rollback is unexecuted | COC + I + D + Storage | P0 | Physical old-backup restore drill, stale high-water rejection, same-GID resolution, quarantine and read-disable evidence |
| INT-019 | F retrieval final-read/currentness, cache and index rebuild gates have logical-model evidence but no production-equivalent service proof | F + D + I + Storage | P0 | Real concurrent read/fence/revoke/index rebuild/cache fill tests, per-partition watermark gap handling |
| INT-020 | Context delivery/reconnect and provider dispatch retry need same-attempt reconciliation across H/C/G | C + G + H | P0 | Crash after dispatch, lost ACK, duplicate callback, stale ContextVersion, reconnect and replay tests |

## 5. Workstream dependency and execution order / 工作流依赖与执行顺序

The workstreams may research independently, but their normative closure order is dependency-constrained:

1. **A — source freeze (first and continuous):** correct the inventory, pin exact current refs/Blobs/CI, record approval status, fix stale incident statements and identify canonical document paths. No downstream proposal may rely on a branch snapshot without a currentness pin.
2. **B + C — parallel contract resolution:** B resolves Fact/Claim or obtains governance approval for a typed-neutral first slice; C resolves Forget/auth/recovery safety with I/D/Storage/COC. These are independent in semantic scope but share D/Storage ordering assumptions.
3. **D — runtime/Applied integration:** after C and the C/G/H/I/D/Storage identity crosswalk is accepted, freeze the exact final-request evidence predicate and durable G Applied state. F safe retrieval is a prerequisite to G context assembly.
4. **E — technology and implementation plan:** consume the accepted B/C/D contracts and Storage L1/L4 decision; do not choose a DB, crate boundary or product before the required evidence.
5. **Independent integration acceptance:** reviewers not authoring the proposals verify all authority boundaries, exact pins, adversarial tests, bilingual parity and unresolved-risk register.

This ordering does not mean the Owner PRs should be merged in that order. Owner acceptance and governance approval must occur on their own authoritative branches/processes; this integration PR only records dependencies.

## 6. Provisional technology disposition / 暂定技术处置

| Capability | Proposal | Status / condition |
|---|---|---|
| Canonical domain, Memory, lifecycle, Evidence/Provenance | BUILD | Brain authority; Fact/Claim and evidence ownership blockers first |
| Authorization authority and Forget | BUILD | I/D owned; no product authority delegation |
| Durable execution | WRAP narrow SQL work/outbox | Requires E/D/Storage identity and fencing acceptance |
| Retrieval | BUILD structured + native lexical first | F final revalidation; vector/graph/cache deferred |
| PDP evaluator | WRAP Cedar candidate | Only after I approves wrapper; fail closed |
| Agent/Provider runtime | WRAP one replaceable adapter | Exact C boundary/outcome acceptance |
| BMCP | WRAP/retain H protocol | Exact H/C/G/I wire/trust acceptance |
| Storage | L1 logical transaction domain; L4 undecided | SQLite/PostgreSQL both candidates |
| Workflow engine / external broker | DEFER | Adopt only on measured scale/recovery need |
| Vector DB / graph DB / distributed cache | DEFER | Must demonstrate recall/latency benefit exceeding added consistency/Forget/restore cost |
| Microservices / per-Owner DBs/crates | DEFER | Logical boundaries do not justify distribution |

## 7. Gate disposition / Gate 状态裁定

| Gate | Current disposition | Why |
|---|---|---|
| G0 — Source baseline | PARTIALLY SATISFIED | Main and principal Owner refs pinned; A inventory needs corrections/currentness refresh |
| G1 — Domain semantics | BLOCKED | Fact/Claim ADR and Evidence ownership unresolved |
| G2 — Canonical transaction | LOGICAL CONTRACT CANDIDATE; PHYSICAL BLOCKED | L1 selected; L4, row ownership, cross-log I/COC protocol and physical tests open |
| G3 — Forget/Auth safety | BLOCKED | Global inventory, recipient proof, physical restore and integrated races open |
| G4 — Context Applied | BLOCKED | Exact C/H/G/I/D/Storage mapping and runtime/restore tests not accepted |
| G5 — Technology topology | PROPOSAL READY FOR OWNER REVIEW | Modular monolith and minimal dependencies coherent; DB/product selection open |
| G6 — Runnable Brain | NOT BUILT / NOT VERIFIED | Repository README says implementation has not started; no implementation/test result claimed |
| G7 — Independent acceptance | NOT STARTED | Workstream proposals are not independent acceptance; Owner and independent review evidence pending |

## 8. Required Owner decision packet / Owner 决议清单

The next review cycle must request these precise decisions, not generic approval:

- **B + Governance:** approve/reject Fact/Claim ADR-001; if blocked, explicitly approve the exact typed-neutral CandidateProposition boundary and prohibit canonical FactRef/ClaimRef creation.
- **B/D/E:** identify Evidence/Provenance record authority, identity issuer, immutable fields, and canonical write path.
- **D + Storage:** approve exact canonical atomic write set, per-authority anchor row, producer registration/fence/visibility serialization and UNKNOWN recovery semantics.
- **I + D + Storage + COC:** define the receipt/epoch/fence/quorum ordering and recovery protocol without claiming a cross-log ACID transaction.
- **I + D + E/F/G/H/Storage:** close Forget producer/recipient/backup inventory and target evidence; specify exception governance.
- **C + G + H + I + D + Storage + COC:** exact-review all Applied identity fields and final-request evidence, resolve G's source discrepancy, and pin one compatible schema bundle.
- **Storage + Engineering:** run the SQLite/PostgreSQL profile comparison against the same conformance suite before L4 selection.
- **A + all Owners:** correct source inventory/path-map and complete bilingual normative parity ledger.

## 9. Evidence ceiling and non-claims / 证据上限与不作出的声明

- This integration review is documentation-only and non-normative.
- No ARCH PR or PRODUCT-FIRST PR is merged or approved by this review.
- No Fact/Claim ADR, Evidence authority assignment, L4 DB, Cedar deployment, BMCP schema bundle or Applied wire mapping is frozen.
- C 19/19 and H 11/11 are bounded candidate conformance evidence at their cited commits, not production or end-to-end proof.
- F 19/19 is a deterministic in-memory anti-resurrection reference model, not a real database/index/cache concurrency or restore test.
- PR #88 bounded formal model results are not unbounded proof or production implementation.
- Storage JF-10 conformance plan is test design unless an exact run artifact says otherwise.
- No physical crash/failover/PITR/old-backup restore campaign is claimed.
- No Rust workspace, executable Brain, end-to-end vertical slice or production deployment is claimed.
- No global Forget completion or model-attention/usage claim is made.

**Interim integration disposition: ARCHITECTURE PROPOSAL IS COHERENT AT THE LOGICAL TOPOLOGY LEVEL, BUT P0 CONTRACT AND PHYSICAL-PROOF GATES REMAIN OPEN. NOT READY FOR IMPLEMENTATION FREEZE OR FULL BRAIN ACCEPTANCE.**

**阶段性集成结论：逻辑拓扑层面的架构提案基本一致，但 P0 合同与物理证明 Gate 仍未关闭。尚未达到实现冻结或完整 Brain 验收条件。**
