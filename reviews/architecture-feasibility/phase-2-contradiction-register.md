# Phase 2 — Contradiction, Ambiguity and Proof-Obligation Register
# 第二阶段 — 矛盾、歧义与证明义务登记册

- Review: ARCH-CONSOL-001 / Issue #43
- Status: OPEN; preliminary exact-version findings
- Severity P0/P1 is a freeze priority, not a claim that production has failed.
- L1 = architecture feasibility; L2 = contract/schema consistency; L3 = reference-model proof; L4 = implementation/deployment validation.

## ARC-01 — D/Storage serialization topology is unresolved
**Severity:** P0 · **Level:** L1 + L3 · **Owners:** D, Storage, I, A

**Evidence:** Storage topology ADR Blob 080433f8e13a500522bc2754da64057edb0ae9d8 is explicitly ADR-BLOCKED / NO TOPOLOGY SELECTED. It presents Option A (one serializable transaction domain per Canonical Memory authority) and Option B (separate D/Storage services plus a durable linearizable coordinator); Option C check-then-write is rejected. Storage Phase 3.8 visibility contract Blob 175ee7b1349cfdb79a19898b311a88391ed88010 defines a logical final visibility transaction but does not select the physical serialization substrate.

**Finding:** The abstract sequence can be coherent, but the final visibility point is not yet grounded in one selected and fully specified serialization topology. A process mutex, queue order, stale replica or independent local CAS is not an acceptable substitute.

**Required closure:** Select A or B as an architecture decision; specify exact serialization domain, D fence/participant hold, I revocation/receipt hold, Storage pointer/outcome/outbox atomicity, read-path authority, retry/idempotency and crash recovery. Provide a deterministic reference model before freeze. Actual deployed database and operator evidence remain L4.

**中文：** Storage 拓扑 ADR 明确为 ADR-BLOCKED / NO TOPOLOGY SELECTED，列出 Option A（每个 Canonical Memory Authority 一个 Serializable Transaction Domain）与 Option B（D/Storage 分离并由持久化线性协调器协调），明确拒绝 Check-then-write。Phase 3.8 定义了逻辑最终可见性事务，但尚未选择物理序列化基础。必须选择 A 或 B，明确序列化域、D/I Hold、Storage Pointer/Outcome/Outbox 原子性、读路径、幂等和恢复语义，并在冻结前提供确定性参考模型。实际部署数据库和运维责任人属于 L4。

## ARC-02 — H wire version 1.2.12 is not yet uniformly adopted
**Severity:** P1 · **Level:** L2 · **Owners:** C, D, H, I, Storage

**Evidence:** H Unified schema 1.2.12 Blob a54f66914a819d77f00c6af04e76453ff9f654ee; RecoveryJoin 1.0.2 Blob 4b664e3bce465499bcdfd93796349a4ba7074002; H R1/R2 crosswalk Blob 8b5b2c37201f7ae821bb5ca71a5101f19e75cf5c. H Provider Outcome semantic validator contract Blob ac800ddbb1fb13aa7eaef415e2282db971d73ff4 is explicitly bound to 1.2.11. C Phase 3.8.6/3.8.8/3.8.9 artifacts bind 1.2.11. D and I Phase 3.8.5 amendments (Blobs 46b6abd94f3396e5eef7d7456f9b62a3865d4ce2 and b56b0c3690f1826f2fc965ec6af5d66a920004ae) adopt 1.2.12 only as candidate amendments. Storage successor manifest Blob 6fc0bedaf5421d1be5a9ab5fb4d8cfab2871d7d7 explicitly calls out this migration gap.

**Finding:** Structural schema revision, semantic validator revision and Owner applicability statements do not yet form one exact bundle. Previous 1.2.11 reviews do not transfer automatically.

**Required closure:** C publishes exact 1.2.12 Provider Outcome mapping; H publishes matching semantic validator and negative vectors; D/I issue fresh exact cross-reviews; Storage refreshes the successor manifest. Keep wire-family version and artifact revision distinct.

**中文：** H 当前结构 Schema 已到 1.2.12，但 Provider Outcome Validator 和 C 合同仍绑定 1.2.11；D/I 对 1.2.12 的采纳只是候选修订。必须由 C 更新精确映射、H 更新 Validator/负向向量、D/I 重新审查、Storage 刷新绑定清单。旧版批准不能自动继承。

## ARC-03 — CSubmitOutcome schema 1.0.1 is not adopted by its contract
**Severity:** P1 · **Level:** L2 · **Owners:** C, H, Storage

**Evidence:** Current C branch schema 1.0.1 Blob a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda; C Phase 3.8.9 schema/conformance contract Blob 2ecdf44cae1bf71e9611dd5367c8f7bcf25dd7ac still binds schema 1.0.0 Blob b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c. Storage v3.2.4 manifest lists the 1.0.0 source as current.

**Finding:** The branch contains a successor schema that is not reflected in the normative contract and cross-owner binding. A validator could therefore accept one object revision while the owner contract describes another.

**Required closure:** C explicitly chooses 1.0.0 or 1.0.1 as the active candidate; updates the conformance contract, projection, vectors and C/H mapping; Storage pins the same exact object schema. Do not silently infer that 1.0.1 supersedes 1.0.0.

**中文：** C 当前分支存在 1.0.1 Schema，但 3.8.9 合同和 Storage 清单仍绑定 1.0.0。必须由 C 明确选择当前候选版本，并同步更新 Conformance、签名投影、Vectors、C/H 映射和 Storage Pin，不得暗中推定新版本自动替代旧版本。

## ARC-04 — Integrated D/E/I/Storage publication race proof is incomplete
**Severity:** P0 · **Level:** L1 + L3 · **Owners:** D, E, I, Storage, H, A

**Evidence:** D Phase 3.8 publication contract Blob 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78; E Phase 3.8 orchestration Blob 475fee41e5eea527af4edefbfe88c58c86967d0a; I Phase 3.8 receipt/sequencer contract Blob 54bab0484bd232a5a258e65e34cc7425288b39a6; Storage Phase 3.8 visibility contract Blob 175ee7b1349cfdb79a19898b311a88391ed88010.

**Finding:** The proposals agree on Storage hidden prepare → D publication participant → I single-use consumption → Storage final visibility commit → D/I closeout. The circular post-commit ITerminalProof dependency has been removed. However, a complete integrated reference model proving both serial orders and all crash/ACK windows was not established by this exact source bundle. H structural tests do not prove the D/I/Storage state machine.

**Required closure:** Model fence-first and participant-first; revocation-first and COMMIT_WON-first; Storage prepare/commit ACK loss; crash before/after every durable boundary; orphan hidden participant; missing participant after confirmed D admission; stale lease; replay; duplicate same-digest and changed-digest conflict; conflicting terminal outcomes. Check D barrier, I revocation hold, Storage pointer/outcome/outbox and artifact visibility after each trace.

**中文：** D/E/I/Storage 对发布顺序的逻辑提案一致，且已消除提交后 ITerminalProof 的循环依赖。但当前精确合同包尚未证明完整集成状态机的双向竞争顺序和所有崩溃/ACK 窗口。必须建立参考模型，覆盖 Fence/Participant、Revocation/COMMIT_WON、Prepare/Commit ACK、各持久化边界崩溃、孤儿隐藏 Participant、缺失 Participant、过期 Lease、重放和冲突终态，并逐步检查 D Barrier、I Revocation Hold、Storage Pointer/Outcome/Outbox 和可见性。

## ARC-05 — Multi-PolicyDomain atomicity is not supported by the current contract
**Severity:** P1 · **Level:** L1 + L2 · **Owners:** I, A, B, D

**Evidence:** I current authorization contract Blob e3b1b5d99eb36ac0b395854d8c19287d2b64b752 defines PermissionEpoch as opaque and local to one I-registered PolicyDomain. The project evidence records Multi-PolicyDomain atomicity as BLOCKED.

**Finding:** Cross-domain actions cannot compare PermissionEpoch values or assume one global authorization sequence. The system must state whether a Memory/Forget operation can span PolicyDomains and what partial-completion semantics apply.

**Required closure:** Define the supported atomicity scope. If only one PolicyDomain is supported per atomic operation, make it a hard contract and specify cross-domain orchestration/partial results. Otherwise design a separate coordinator with explicit failure and recovery semantics.

**中文：** PermissionEpoch 是单个 PolicyDomain 内的不透明值，不得与其他域或 Owner 的序列比较。必须明确一个 Memory/Forget 操作是否可以跨 PolicyDomain；若单次原子操作只支持一个 PolicyDomain，应将其写成强制边界并定义跨域编排/部分完成语义；否则必须另行设计协调协议。

## ARC-06 — Full Applied and Provider Outcome are not one frozen evidence chain
**Severity:** P1 · **Level:** L2 + L3 · **Owners:** C, G, H, I, D

**Evidence:** C Provider Egress Gate Blob a8d1cfc4d2171c9b0a0ced10e53fc6b110479aca; CSubmitOutcome schema 1.0.1 Blob a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda; G lifecycle Blob c1de241ec69834377d9b0e24aa4770a809796d4b; H Unified 1.2.12 Blob a54f66914a819d77f00c6af04e76453ff9f654ee. Issue #3 records Applied Contract Frozen = NO.

**Finding:** The boundaries are conceptually correct: Context delivery, adapter materialization, final immutable inference request, provider handoff, provider acceptance, model execution and user delivery are distinct. But the exact current schema/validator versions and G Full Applied predicate are not yet frozen together.

**Required closure:** Define a single immutable final-request identity after all prompt/context transformations; bind it to G Delivery/ContextVersion, C admission/gate/attempt/outcome, H authenticated adapter evidence, I current authorization and D current Forget/lineage. Explicitly state what Applied proves and does not prove.

**中文：** Context Delivery、Adapter Materialization、最终不可变推理请求、Provider Handoff、Provider Acceptance、模型执行和用户交付必须区分。当前边界理念正确，但 Schema/Validator 版本与 G Full Applied Predicate 尚未精确冻结。必须定义所有 Prompt/Context 转换后的最终请求身份，并绑定 G Delivery/ContextVersion、C Admission/Gate/Attempt/Outcome、H Adapter 证据、I 当前授权和 D Forget/Lineage；明确 Applied 能证明什么、不能证明什么。

## ARC-07 — Fact/Claim semantic decision remains blocked
**Severity:** P1 · **Level:** L2 · **Owner:** B

**Evidence:** B domain overview Blob 4d1debc0ec19b3917f9e76d04bb66da4df4cd346; TAB-001 Blob 7b6f2d139217dbe13ab3a3af31bfbff525f20e71 explicitly preserves Fact/Claim ADR as ADR-BLOCKED.

**Finding:** The broad object model separates Memory and Claim, but the Fact/Claim boundary remains an explicit unresolved domain decision. Dependent schema fields cannot silently settle it.

**Required closure:** B publishes the ADR decision, semantic examples, migration/compatibility implications and a dependent-schema impact list. Until then, mark all dependent fields candidate/open.

**中文：** B 领域模型区分 Memory 与 Claim，但 Fact/Claim 边界仍有明确未决 ADR。依赖字段不得暗中替 B 定案。必须由 B 发布 ADR 决议、语义示例、迁移/兼容影响和依赖 Schema 清单；此前相关字段保持 Candidate/Open。

## ARC-08 — Global Forget and restore anti-resurrection need one composable proof
**Severity:** P1 · **Level:** L1 + L2 + L3 · **Owners:** I, D, E, F, G, H, Storage

**Evidence:** D ForgetFence contract Blob 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5; E/F/G lifecycle Blobs 4fb9e58511941f59b4d777336f8f85ad88ecccf1 / c1de241ec69834377d9b0e24aa4770a809796d4b; I current authorization contract Blob e3b1b5d99eb36ac0b395854d8c19287d2b64b752; Storage v3.2.4 manifest Blob 6fc0bedaf5421d1be5a9ab5fb4d8cfab2871d7d7.

**Finding:** Local rules are strong: every derivative-capable producer registers before work; complete lineage precedes visibility; restore is fenced; queue ACK/DLQ/timeout/missing rows do not imply terminality; indexes and caches are derived; Context removal is not Forget. What remains is one system-wide target/recipient/backup/restore universe and a complete trace proving no stale producer, replay, rebuild or reconnect can resurrect protected content.

**Required closure:** Produce the inventory authority and scope semantics; enumerate producer/recipient/backup/restore classes; distinguish NotApplicable from Unknown; model late-discovered lineage, stale snapshot restore, missing WAL/prefix, old queue replay, index rebuild and offline Adapter reconnect. I owns Global Forget completion; D owns per-memory fence/lineage; Storage and consumers provide only their own evidence.

**中文：** 各模块局部规则较强：派生 Producer 先登记后工作、完整 Lineage 先于可见性、Restore 先隔离、Queue ACK/DLQ/Timeout/行缺失不代表终态、索引/缓存是派生物、Context Remove 不等于 Forget。缺少的是一份系统级 Target/Recipient/Backup/Restore 全量宇宙，以及证明迟到 Producer、重放、重建、重连不能复活受保护内容的完整轨迹。必须明确 Inventory 权威和 Scope，枚举所有类别，区分 NotApplicable 与 Unknown，并覆盖迟发现 Lineage、旧快照恢复、WAL/Prefix 缺失、旧队列重放、索引重建和离线 Adapter 重连。I 管理 Global Forget 完成，D 管理单 Memory Fence/Lineage，其余模块只提供各自证据。

## ARC-09 — Role simulation is not independent Owner/governance approval
**Severity:** Governance gate · **Level:** approval provenance · **Owners:** A and the relevant Owner/governance authorities

**Finding:** The A, C, D and I role artifacts explicitly identify delegated role simulation. They are useful technical review evidence but cannot be described as independent human signatures or external governance approvals.

**Required closure:** Keep simulated technical dispositions and actual Owner/governance decisions in separate columns and records. No silent conversion of a simulated ACCEPT into a formal Owner approval.

**中文：** A/C/D/I 工件明确标记为委托角色模拟。它们可以作为技术分析证据，但不能描述为独立人类签署或外部治理批准。必须分开登记模拟技术意见和真实 Owner/治理决议，禁止将模拟 ACCEPT 自动转换为正式批准。

