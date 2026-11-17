# ARCH-CONVERGENCE-001 — Implementation Roadmap
# ARCH-CONVERGENCE-001 — 实施路线图

- Workstream: E — Runnable Implementation Planning
- Status: **DRAFT / DEPENDENCY-GATED ROADMAP / NO IMPLEMENTATION AUTHORIZATION**
- Baseline: `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Companion: `ARCH-CONVERGENCE-001-MINIMUM-RUNNABLE-ARCHITECTURE.md`

## 1. Executive roadmap / 执行路线摘要

The repository README states implementation has not started by design. No Rust workspace or runnable Brain implementation is claimed in this roadmap.

The earliest useful executable milestone is a **Canonical Core Slice**: authenticated durable ingestion → idempotent acceptance → D producer admission → typed candidate compilation → evidence/provenance validation → atomic D Canonical Commit → outbox replay → authorized canonical retrieval. This milestone is not yet a complete Brain because it does not prove Context Applied.

The earliest **complete Minimum Runnable Brain** must add: D/I Forget and authorization race enforcement → F projection/read suppression → G ContextVersion/Delivery → C exact final request/Provider Outcome → H authenticated evidence → G durable Applied → crash/retry/restore/anti-rollback tests. No earlier compiling skeleton or mock-only demo may be called complete.

README 明确表示实现按设计尚未启动，本路线图不声称已有 Rust Workspace 或可运行 Brain。

最早有价值的可执行里程碑是 **Canonical Core Slice**：认证持久摄取 → 幂等接收 → D Producer Admission → 强类型候选编译 → Evidence/Provenance 校验 → D 原子 Canonical Commit → Outbox 重放 → 授权后的规范检索。该里程碑还不是完整 Brain，因为它不证明 Context Applied。

最早的**完整 Minimum Runnable Brain** 必须进一步实现：D/I Forget 和授权竞争执行 → F 投影/读取抑制 → G ContextVersion/Delivery → C 精确最终请求/Provider Outcome → H 认证证据 → G 持久 Applied → 崩溃/重试/恢复/防回滚测试。更早的可编译骨架或纯 Mock 演示都不能称为完成。

## 2. Phase plan / 阶段计划

| Phase | Work | Prerequisites | Owner(s) | Exit gate |
|---|---|---|---|---|
| P0 — Source freeze | Source inventory, exact branch heads, H/C integrity reconciliation, README path register, bilingual parity | Current main and all relevant Owner refs | A + all Owners | A0: every source pin/status/approval discoverable; H/C refs reconciled |
| P1 — Semantic contracts | Fact/Claim ADR; D canonical transaction; D/Storage anchor row ownership; I PermissionEpoch/Forget; G Applied and C/H mapping | P0 | B + Governance; D + Storage; I; C/G/H | P1: no unowned P0 invariant; exact Owner decisions or explicit blocked state |
| P2 — Schema prerequisites | Typed ID registry, neutral candidate schema, accepted receipt, work/lease, canonical rows, commit receipt/cursor, outbox, fence/barrier, evidence refs, Context/Applied records | P1 contracts; Fact/Claim either decided or typed neutral scope approved | B/D/E/F/G/H/I/Storage | P2: schema/validator/version compatibility and migration plan accepted |
| P3 — Canonical Core Slice | Rust workspace, SQL transaction adapter, durable acceptance, work runner, D canonical store, provenance linkage, outbox and canonical read | P2 + one provisional storage profile with L1 proof | E + D + Storage + B | P3: crash-before/after-commit, duplicate, CAS and outbox tests pass |
| P4 — Forget/Auth safe read and projection | I PEP/PermissionEpoch, D Fence/Producer barrier, E registration/replay, F scope-before-candidate and final revalidation, lexical projection | P3 + I/D/E/F exact interfaces | I + D + E + F + Storage | P4: Forget-ingestion/retrieval/index races and cross-scope tests pass |
| P5 — Context/Applied vertical slice | G ContextVersion/Delivery, H delivery/materialization evidence, C final request and provider outcome, G Applied ledger | P1 Applied exact mapping + P2 schemas + P4 safe retrieval | C + G + H + I + D + Storage | P5: exact final request and Full Applied predicate tests pass |
| P6 — Recovery and restore | Crash hooks, lease fencing, same-key replay, COC/Storage same-GID, backup restore quarantine, current I/D high-waters, anti-rollback | P3–P5; JF-10 owner acceptance | D + I + E + F + G + H + Storage + COC | P6: physical crash/failover/PITR/restore test evidence and no resurrection |
| P7 — Independent acceptance | Full adversarial matrix, bilingual parity, source pin review, security review, independent integration reviewer | P0–P6 | Independent reviewer + all Owners | P7: no unowned critical invariant; all remaining OPEN items have owners/conditions |
| P8 — Measured optimization | Vector, graph, cache, external broker/workflow, service split, model acceleration | P7 baseline and measured workload | Engineering + relevant Owners | P8: each adoption has reproducible trigger evidence and rollback path |

## 3. Documentation prerequisites / 文档前置条件

Before implementation freeze:
1. Merge status is not assumed; each ARCH Draft PR remains a proposal until reviewed.
2. Publish/approve the source-of-truth index and canonical paths; do not bulk-copy Owner branches.
3. B/Governance resolve Fact/Claim or approve a narrow typed-neutral first-slice contract.
4. D/Storage confirm L1 serialization anchor semantics, physical row/record ownership, transaction isolation and final outcome rules.
5. I confirms exact protected-operation tuple, current PermissionEpoch and CommitAuthorizationReceipt integration.
6. D/I/E/F/G/H/Storage accept closed-world Forget and target evidence mapping.
7. C/G/H accept exact final-request/Applied identity and wire mapping.
8. Confirm COC/JF-10 scope and same-GID physical proof applicability.
9. Complete English/Chinese semantic parity for normative docs, schemas, error enums and test cases.

## 4. Contract prerequisites / 契约前置条件

| Contract | Required state before code freeze | Blocking consequence if absent |
|---|---|---|
| B Fact/Claim | Approved ADR or approved typed-neutral boundary | No canonical Claim/Fact identity, schema or wire field |
| D Canonical Store | Exact immutable version, CAS, commit receipt/cursor and atomic write set | No canonical schema or commit implementation |
| D Forget | Producer registry, barrier, dependency lineage, final visibility gate and terminal proof | No derived publication or global completion claim |
| I Authorization | Authenticated tuple, PermissionEpoch, revocation order, fail-closed PEP | No protected read/write/dispatch |
| E Durable Work | AcceptedReceipt, WorkItem identity, attempts/leases, retry/DLQ and registration semantics | No durable compiler execution |
| F Retrieval | Scope-before-candidate, canonical revalidation, index watermark and cache invalidation | No protected retrieval |
| G Applied | Exact Context/Delivery/Applied identity and persistence predicate | No Full Applied claim |
| C Provider | Exact final request, ProviderAttempt, CSubmitOutcome and same-key recovery | No provider handoff success claim |
| H Wire | Exact schema/version, authentication, capability, observation replay and Adapter ACK | No external Adapter evidence acceptance |
| Storage / COC | L1 anchor + L4 engine/profile + same-GID/restore evidence where applicable | No physical atomicity/recovery claim |

## 5. Schema prerequisites / Schema 前置条件

Schema work begins only after the corresponding Owner semantic decisions. Minimum families:
- Domain: typed Actor/Principal/Scope/Environment refs; EventRef; MemoryId/MemoryVersionId; typed evidence/provenance refs; neutral candidate schema if Fact/Claim remains blocked.
- Ingress: idempotency namespace/digest, AcceptedReceipt, CompileIntent, ProducerWorkItem, Attempt/Lease, terminal disposition.
- Canonical: aggregate head, immutable version, lifecycle event, CanonicalCommit receipt/cursor, outbox event.
- Forget: ForgetOperation, target set/lineage, ForgetFence, producer registry/high-water/barrier, dependency registration, target ACK/exception evidence.
- Authorization: I PolicyDomain/PermissionEpoch, authenticated decision and single-use CommitAuthorizationReceipt binding; I retains own ledger semantics.
- Storage: per-authority serialization anchor, prepared participant, VisibilityPointer, PublicationReceipt, outcome, same-GID/DB incarnation and restore proofs.
- Retrieval: projection version/schema, partition-scoped IndexWatermark, completeness and stale/gap metadata.
- Context/Applied: ContextVersion, ChangeSet, Delivery/attempt, H observation identities, C ProviderAttempt/CSubmitOutcome, G Applied identity/evidence revision.
- Protocol: H schema revision, signed envelope, nonce/replay identity, capability epoch, evidence kind/coverage, C/G/I owner refs.

Do not invent a generic status field that collapses owner-specific states. Do not compare cursor/epoch namespaces as generic integers.

## 6. Core implementation sequence / 核心实现顺序

1. Create Rust workspace with dependency direction: domain → core → storage/adapters → app composition.
2. Add migration runner and one per-authority transaction adapter implementing the Storage L1 serialization anchor.
3. Implement I-authenticated request context and fail-closed test PEP; do not expose a permissive fallback.
4. Implement E AcceptedReceipt + idempotency + durable work intent transaction.
5. Implement D producer registry/admission and stable work identity.
6. Implement deterministic typed candidate validation; keep Fact/Claim neutral until ADR gate closes.
7. Implement Evidence/Provenance binding and canonical reference validation.
8. Implement D Canonical Store: immutable MemoryVersion, aggregate-head CAS, lifecycle event, CanonicalCommit receipt/cursor, outbox in one atomic transaction.
9. Implement outbox worker and projection checkpoint with duplicate/out-of-order handling.
10. Implement F structured/lexical retrieval with Scope-before-candidate and final D/I revalidation.
11. Implement D/I Forget and F suppression at reads, writes, retries, cache and projection publication.
12. Implement G ContextVersion/Delivery and C/H exact request evidence.
13. Implement G Applied decision ledger and same-identity recovery.
14. Implement restore quarantine and current COC/I/D/Storage high-water reconciliation.
15. Run independent adversarial acceptance.

## 7. Earliest runnable milestones / 最早可运行里程碑

| Milestone | What exists | What may be claimed | What may NOT be claimed |
|---|---|---|---|
| M0 — Compiling skeleton | Rust crates, interfaces, empty adapters | Build succeeds | No Brain capability or correctness |
| M1 — Canonical Core Slice | Durable accepted ingestion, D canonical commit, evidence refs, outbox and authorized canonical read | One local canonical memory path works under tested profile | No global Forget, full runtime Applied or restore safety |
| M2 — Safe Retrieval Slice | M1 + I current authorization, D fence, F scope-before-candidate and suppression | Tested protected retrieval under defined races | No Adapter Applied or external recipient cleanup |
| M3 — Full Minimum Runnable Brain | M2 + G Context, C final request/provider outcome, H evidence, G Applied, COC/Storage gates | Full vertical slice for the tested profile and declared failure envelope | No production scale/HA/physical erasure beyond tested evidence |
| M4 — Production candidate | M3 + selected L4 deployment, HA/PITR, operator, security review and operational drills | Only the exact tested production candidate profile | No blanket guarantee beyond declared scope |

The earliest *canonical* runnable slice is M1. The earliest *complete Brain* slice is M3, and it cannot be declared before M3/P6 recovery and M7 independent acceptance gates are satisfied.

最早可运行的**规范核心**是 M1；最早完整 Brain 是 M3，且必须在 M3/P6 恢复测试与 P7 独立验收门槛全部满足后才能宣布。

## 8. Automated, integration and recovery test gates / 自动化、集成与恢复测试门槛

### Unit/property
- Typed identity and cursor namespace invariants.
- Same key/same digest idempotency; changed digest conflict.
- CAS, immutable version and lifecycle ordering.
- Scope-before-candidate and no existence leakage.
- Provider outcome algebra and nonterminal UNKNOWN/IN_DOUBT.
- H evidence identity separation and strict unknown-field rejection.

### Integration
- E accepted receipt → D producer admission → canonical commit → outbox → F projection.
- Forget vs producer registration and final publication.
- PermissionEpoch revocation vs retrieval/dispatch/commit.
- G ContextVersion → H delivery/materialization → C final request → G Applied.
- MCP tool read/write re-enters I/D gates.

### Recovery/fault injection
- Kill before/after every durable transaction and ACK.
- Expire lease with old worker still running.
- Duplicate/out-of-order outbox and provider callbacks.
- Crash after provider dispatch before C/G evidence persistence.
- COC failover and same-GID Storage participant resolution.
- Restore old backup with newer I/D/COC high-waters and Forget fence.
- Stale primary rejoin, stale replica/cache read, index rebuild from pre-Forget snapshot.
- Missing/unavailable PDP, signer, policy epoch, fence, inventory seal or owner proof.

A test PASS must be tied to exact code commit, profile, engine version/configuration, fixture, test log and owner scope. Logical reference model PASS is not physical integration PASS.

## 9. Independent acceptance / 独立验收

Independent reviewer must:
- not be the author of the implementation or Owner proposal being reviewed;
- freeze exact Base/Head and read every changed file/blob;
- verify all six non-negotiable authorities;
- execute or independently inspect exact automated tests and fault schedules;
- inspect negative evidence (no pointer, no disclosure, no duplicate effect, no stale restore release);
- verify bilingual semantic parity and schema compatibility;
- report OPEN issues with named Owner, evidence required, closure condition and blocked Gate.

## 10. Product adoption and topology change control / 产品采用与拓扑变更控制

No external product is adopted merely because it exists. Every adoption proposal must include:
1. measured trigger and baseline;
2. capability/authority boundary;
3. failure/retry/Forget/authorization/restore mapping;
4. license/version/SBOM/security review;
5. migration and rollback plan;
6. exact Owner acceptance;
7. reproducible tests and performance evidence.

A physical split is justified only by measured independent scaling, failure isolation, deployment cadence, regulatory boundary or operational ownership—not by A–I labels. A new database/broker/index introduces a new Forget/backup/restore target and must be registered before protected data is copied.

## 11. Roadmap disposition / 路线图结论

- **Current implementation status:** NOT STARTED by repository design; no code is claimed.
- **Current earliest runnable milestone:** M1 can begin after P1/P2 contracts; it is not a complete Brain.
- **Full minimum Brain:** M3 + P6 + P7.
- **Technology selection:** SQLite vs PostgreSQL remains OPEN at L4.
- **Product stack:** no Qdrant/Temporal/Restate/DBOS/Redis/Neo4j/external broker required for the minimum candidate.
- **Architecture freeze:** NOT AUTHORIZED by this roadmap.
- **Implementation authorization:** requires Owner and governance gates.

本路线图不授权架构冻结或生产实现。实现启动必须遵守 Owner 合同、L4 物理证据、P6 恢复测试和 P7 独立验收门槛。
