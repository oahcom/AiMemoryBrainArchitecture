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

## ARC-02 — H 1.2.14 exact mapping and same-manifest adoption remain open
**Severity:** P1 · **Level:** L2 · **Owners:** C, H, D, I, Storage

**Evidence:** H Unified 1.2.14 Blob 09fcd1fa29fe24255fbd87cae79dafb406594a59; RecoveryJoin 1.0.2 Blob 4b664e3bce465499bcdfd93796349a4ba7074002; RecoveryCutoff 1.0.5 Blob 75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7; CSubmitOutcome 1.0.1 Blob a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda. H Provider Outcome mapping Blob 7739d8159b32702024583669f40974a80801782b; H integrated authority-join mapping Blob 1cbe74eba69325510d6b1019d971661f965eabf8. C Phase 3.8.16 review commit 8d7298d7f56b1df48229799ff6462a8db634e7ed accepts the Provider Outcome mapping but pins H schema Blob fee452efb99ab4fe0ceccb347c46eeef1521bd28, whereas current H schema and H mapping pin 09fcd... (the two schema blobs differ only in descriptive revision text). Storage v3.2.7 manifest Blob 4435fc0340a4fce10751679a95f3b4c821bdae4d binds the integrated mapping but still requires fresh Owner reviews and A integration review.

**Finding:** L1/L2 version migration substantially exists. The remaining blocker is that C has not yet reviewed the integrated authority-join mapping used by Storage, and C's exact schema pin differs from H's current Blob. The bundle is not jointly accepted.

**Required closure:** C reviews exact integrated mapping 1cbe... and corrects the schema pin to 09fcd...; H confirms current C/D/I exact source set; D/I/Storage bind the same successor manifest; H callback tests must not be represented as unmocked end-to-end authority proof.

**中文：** 当前 L1/L2 版本迁移已基本形成：H 1.2.14、RecoveryJoin 1.0.2、RecoveryCutoff 1.0.5、CSubmitOutcome 1.0.1 均有精确工件；H 也分别有 Provider Outcome Mapping 与集成 Authority-Join Mapping。剩余阻断是 C 尚未审查 Storage 使用的集成 Mapping，且 C 最新审查的 H Schema Blob 与 H 当前精确 Blob 不一致。Storage v3.2.7 仍是候选 Bundle，尚未联合接受。

## ARC-03 — CSubmitOutcome 1.0.1 is selected as proposed current revision; joint adoption remains open
**Severity:** P2 · **Level:** L2 · **Owners:** C, H, I, Storage

**Evidence:** C Phase 3.11.1 amendment Blob 6fa67af110ebbc5ef57ed908bb4880d99c5e46fb explicitly supersedes 1.0.0 for new records; schema Blob a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda; I namespace review Blob 0d78e5b2bfcf66cae6b757314cead84b9c942601; H Provider Outcome mapping Blob 7739d8159b32702024583669f40974a80801782b. Storage v3.2.7 binds C 1.0.1.

**Finding:** C's proposed immutable version selection is explicit; 1.0.0 is historical, not silently upgraded. The remaining issue is same-manifest review and that C's Phase 3.8.16 review has not reviewed the integrated H authority-join mapping.

**Required closure:** Keep 1.0.0 historical; bind C 1.0.1 schema/amendment/vectors in the successor manifest and obtain C/H/D/I exact reviews against that same manifest. Production C/I profiles remain unregistered until I governance gates pass.

**中文：** C Phase 3.11.1 已明确 1.0.1 是新记录的候选不可变版本，1.0.0 保留为历史；I 已审查 Sequence Namespace，H 已映射 1.0.1，Storage v3.2.7 也绑定 1.0.1。剩余问题是同一 Manifest 的联合审查，以及 C 尚未审查集成 H Authority-Join Mapping。生产 C/I Profile 仍须等待 I Governance Gate。

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

## ARC-10 — COC and JF-10 are separate protocols; composition remains gated
**Severity:** P1 · **Level:** L1 + L2 + L3 · **Owners:** A/COC, I, D, C, H, Storage

**Evidence:** Storage v3.2.3 Blob 5cee0d58575adc0fb3dd20a5c7ab68c2a2711792 explicitly labels the JF-10 same-XID bridge as separately gated and says prior COC disposition does not approve automatic COC↔JF-10 composition. COC companion Blob 5b950a3a29bd7a5276b92a49a9114d700718b987 defines its own quorum log, Recovery Cutoff Batch/Manifest and restore protocol. Issue #10 reports Gate A PARTIAL PASS after five PostgreSQL 18.7 capability CI classes; Gate B persistent COC and Gate C fault-injection remain BLOCKED.

**Finding:** COC quorum positions, I PolicyDomain positions, D fence positions and Storage prepared GID/XID are different authorities and identities. COC may record and join owner evidence but cannot make I/D/C decisions or act as the JF-10 coordinator. A prior COC acceptance or a PostgreSQL capability test cannot close the separately governed JF-10 bridge.

**Required closure:** Keep COC quorum prefix/batch/manifest, I terminal decision, D fence, C provider outcome and Storage same-GID resolution separate. Obtain fresh exact I/D/C/Storage/H bridge decisions; prove the COC outage/recovery batch and JF-10 same-XID state machine independently; then prove their exact join without cross-domain counter comparison or authority synthesis. Gate B/C remain later physical/operational gates.

**中文：** Storage v3.2.3 明确将 JF-10 Same-XID Bridge 设为单独门禁，既有 COC 决议不代表自动批准 COC↔JF-10 组合。COC 自己拥有 Quorum Log、Recovery Cutoff Batch/Manifest 和恢复协议。Issue #10 的 Gate A 在五类 PostgreSQL 18.7 能力 CI 后为 PARTIAL PASS；持久化 COC 的 Gate B 与故障注入 Gate C 仍 BLOCKED。COC Quorum Position、I PolicyDomain Position、D Fence Position 和 Storage Prepared GID/XID 属于不同权威/身份。COC 只能记录和 Join Owner 证据，不能代替 I/D/C 决议，也不能成为 JF-10 Coordinator。必须保持这些状态机分离，取得 I/D/C/Storage/H 精确桥接决议，分别证明 COC Outage/Recovery 与 JF-10 Same-XID 状态机，再证明它们的精确 Join；不得跨域比较计数器或合成权威。

## ARC-09 — Role simulation is not independent Owner/governance approval
**Severity:** Governance gate · **Level:** approval provenance · **Owners:** A and the relevant Owner/governance authorities

**Finding:** The A, C, D and I role artifacts explicitly identify delegated role simulation. They are useful technical review evidence but cannot be described as independent human signatures or external governance approvals.

**Required closure:** Keep simulated technical dispositions and actual Owner/governance decisions in separate columns and records. No silent conversion of a simulated ACCEPT into a formal Owner approval.

**中文：** A/C/D/I 工件明确标记为委托角色模拟。它们可以作为技术分析证据，但不能描述为独立人类签署或外部治理批准。必须分开登记模拟技术意见和真实 Owner/治理决议，禁止将模拟 ACCEPT 自动转换为正式批准。


## ARC-11 — RecoveryJoin generic membership proof does not yet express C/D owner-specific P0
**Severity:** P0 · **Level:** L1 + L2 · **Owners:** C, D, H, I

**Exact evidence:**
- H RecoveryJoin 1.0.2 `ownerSnapshotMembershipProof` Blob `4b664e3bce465499bcdfd93796349a4ba7074002` is a closed generic object with common owner/ledger/snapshot/gate/scope/operation/key fields.
- I owner membership proof contract Blob `88209bbea0ab600880c5c630cfe83af31ee16dd7` defines a P0 that matches the generic shape (excluding derived `proof_digest` and external `signature_ref`).
- C owner membership proof contract Blob `5e37185610869951c3b392c9ad143a72b4c702ac` additionally says its P0 binds adapter/provider-account/egress-gate identity, idempotency namespace/key, reservation/attempt/outcome and receipt/lookup evidence.
- D owner membership proof contract Blob `d80dabe7210e681bc4e2290355a38f8b67be9ddd` additionally says its P0 binds ForgetOperationRef, target/source/ancestor lineage, ForgetFenceGeneration, affected-lineage membership, barrier generation/root and dependency closure.
- The generic H schema has `additionalProperties=false` and no explicit C/D typed payload union or canonical dereference rule that proves those extra fields are committed by the owner entry/operation/scope digests.

**Finding:** I's generic P0 can be expressed in RecoveryJoin 1.0.2, but the C/D owner contracts enumerate more signed semantics than the H generic schema serializes. The architecture has not decided whether C/D details are (a) explicit typed C/D proof variants in a successor RecoveryJoin schema, or (b) committed through exact owner-entry/operation/scope digests with a normative no-loss dereference map. Do not silently drop C/D fields or claim current RecoveryJoin 1.0.2 proves them.

**Required closure:** C, D, H and I must select one representation; publish exact field-to-digest mapping or typed owner-discriminated schemas; prove each owner P0's exact canonical preimage and signature projection; add negative vectors for missing/extra/mismatched owner-specific fields; then re-run all owner reviews against exact successor Blobs.

**中文：** RecoveryJoin 1.0.2 的 `ownerSnapshotMembershipProof` 是封闭的通用对象，I 的 P0 与之匹配；但 C/D 自有合同还要求签名绑定 Adapter/Provider/Idempotency/Reservation/Outcome/Receipt，以及 ForgetOperation/Lineage/FenceGeneration/Barrier/Dependency Closure 等字段。H Schema 设置 `additionalProperties=false)，却没有 C/D 类型化 Payload Union，也没有规范的 Digest 解引用映射证明这些字段都被无损承诺。必须由 C/D/H/I 决定采用 Owner 类型化 Proof Variant，或明确将专属字段承诺到 Owner Entry/Operation/Scope Digest，并完成精确 P0 与负向向量验证。不得静默丢弃 C/D 字段。

## ARC-12 — D ForgetFenceGeneration is absent from the current H D high-water projection
**Severity:** P0 · **Level:** L1 + L2 · **Owners:** D, H, COC, Storage, A

**Exact evidence:**
- D Forget Fence contract `03-memory-brain/forget-fence-and-completion-contract.md` Blob `1f0391bc49d007c44ec74165bd33d37412cc7990` defines a canonical `fence_generation` / `ForgetFenceCursor`.
- D Gate Release contract Blob `7f2861d9441b9be6c8e69f41fd0276636be483a8` requires final CAS over both D Gate revision and `ForgetFenceGeneration`, separately from barrier snapshot generation/root.
- H Unified 1.2.13 Blob `8e7f6a6c9663388863db88548f9c37d0fdb1bd97` `ownerSpecificHighWatersD` exposes producer-registration, WorkItem, Attempt, `barrier_generation` and `barrier_root`, but no explicit `forget_fence_generation`.
- D review Blob `84196906cad92367a60c79a74dd241fd80abb96c` confirms the D-owned FenceGeneration and Barrier fields are distinct, but its H schema pin predates the metadata-only schema correction and does not resolve this missing field.

**Finding:** D GateGeneration, ForgetFenceGeneration and BarrierGeneration are separate D-owned values. H must not alias them or infer equivalence. The current H RecoveryCutoff/ownerSnapshot shape does not expose an explicit D ForgetFenceGeneration field in the owner-specific high-water union.

**Required closure:** D and H must define an explicit typed `forget_fence_generation` field (or provide a formally proven exact mapping to an existing field, with D Owner approval), bind it into the D snapshot attestation and membership proof, and add stale-fence / barrier-generation substitution vectors. Any schema change requires a successor exact H artifact and fresh D/H/COC/Storage review.

**中文：** D 的 GateGeneration、ForgetFenceGeneration 与 BarrierGeneration 是不同的 D 自有状态。H 1.2.13 的 D High-Water Union 只有 Producer/WorkItem/Attempt High-Water、BarrierGeneration 和 BarrierRoot，没有明确 ForgetFenceGeneration。不得将三者别名化。D/H 必须增加精确类型字段，或由 D Owner 正式证明现有字段等价，并将其绑定到 Snapshot Attestation、Membership Proof 和 Stale-Fence/Barrier 替换测试。

## ARC-13 — I common-envelope P0 omitted schema_artifact_revision (CLOSED AT L1 CONTRACT)
**Severity:** P1 · **Level:** L1 · **Owners:** I, H

**Resolution evidence:** I successor P0 addendum Blob `5c0e2049513d391dfc118f4f629a5ec95de456d6` adds required `schema_artifact_revision` to the common I-signed P0; H review Blob `c16063197766a495feb98776c7516ebcbe4b7441` confirms exact H Unified 1.2.13 common-envelope coverage and aligns the owner-membership `signature_ref` exclusion with I's original proof contract.

**Residual:** L3 differential P0 vectors, I profile registration, production trust/key custody and anti-rollback remain OPEN; this closure is only the L1 field-contract omission.

**中文：** I 后继 P0 Blob `5c0e2049513d391dfc118f4f629a5ec95de456d6` 已将必需 `schema_artifact_revision` 纳入 I Common Envelope P0；H 复审 Blob `c16063197766a495feb98776c7516ebcbe4b7441` 确认与 H Unified 1.2.13 对齐，并修正 Membership Proof 的 `signature_ref` 排除规则。L1 字段合同关闭，但 L3 差分向量、Profile 注册、生产信任/密钥托管及 Anti-Rollback 仍 OPEN。
