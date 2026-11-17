# Phase 3.6.21 — Storage v3.2.11 Exact-Version Bundle Manifest: H 60-Test Outer-Auth Gate
# Phase 3.6.21 — Storage v3.2.11 精确版本 Bundle 清单：H 60 项 Outer-Auth Gate

- Owner perspective: Storage / COC Durable Log and Recovery
- Date: 2026-11-17
- Status: **H 1.2.14 / C 1.0.1 + REFERENCE OUTER-AUTH GATE EXACTLY BOUND; C/H/I/D REVIEWS RECORDED; FRESH A REVIEW REQUIRED; NOT JOINTLY ACCEPTED / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- Predecessor bundle: Storage v3.2.10, Blob `0c1a9c7bceb9a32974e92934a94ca4e8ff9a488e`
- Normative Storage technical body: Storage v3.2.3, Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`
- COC companion §§14–17: Blob `5b950a3a29bd7a5276b92a49a9114d700718b987`
- Provenance: delegated Storage-role coordination artifact; **not an independent human Storage Owner signature**.
- English and Chinese are normative peers.

## 1. Scope and supersession / 范围与替代关系

This manifest supersedes the H authentication/validator/test/CI and C/I/D review pins in Storage v3.2.10. It adds the H outer-envelope authenticated-ingress reference gate and exact 60-test local CI evidence. It does not change the Storage v3.2.3 normative technical body, COC Batch-before-Manifest ordering, JF-10 owner authority semantics or production gate authorization.

本清单替代 Storage v3.2.10 中 H Authentication/Validator/Test/CI 与 C/I/D 复审绑定，新增 H Outer-Envelope Authenticated-Ingress Reference Gate 与精确 60 项本地 CI 证据。不改变 Storage v3.2.3 规范技术正文、COC Batch-before-Manifest 顺序、JF-10 Owner Authority 语义或生产 Gate 授权。

A changed source Blob invalidates any review that pins it. The H outer-auth implementation is reference orchestration only: all verifier callbacks in CI are test doubles; no signer role, outer P0 projection, signature profile, trust root or durable replay implementation is approved.

源 Blob 变化会使绑定该 Blob 的复审失效。H Outer-Auth 实现仅为 Reference Orchestration：CI 中所有 Verifier Callback 均为 Test Double；未批准 Signer Role、Outer P0 Projection、Signature Profile、Trust Root 或 Durable Replay 实现。

## 2. Unchanged Storage / COC normative base / 不变的 Storage / COC 规范基线

| Authority | Artifact | Exact Blob | Binding |
|---|---|---|---|
| Storage | Durable log/recovery protocol v3.2.3 | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Normative S0a–S4, RecoveryBatch, participant union, JF-10 bridge and same-GID recovery |
| COC | COC durable log/recovery companion §§14–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | PreparedParticipant identity, dual-ledger union, record order, digest chain and recovery joins |
| Storage | Batch-before-Manifest amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` | Batch committed before distinct Manifest with exact backlink |
| Storage | R1/R2 successor-round/release ordering addendum | `0477f0329997e42a1cbf6ecb8127c5c01fa47051` | Immutable RecoveryRound and owner-local release order |
| Predecessor | Storage v3.2.10 manifest | `0c1a9c7bceb9a32974e92934a94ca4e8ff9a488e` | Exact 39-test H/C bundle and prior A review |

The S0a–S4 order remains unchanged: owner-local gate freeze → COC quorum prefix freeze → complete COC/owner-admission union → immutable Recovery Cutoff Batch → distinct Participant Manifest with exact backlink → linearizable pair readback → owner-specific reconciliation and release.

S0a–S4 顺序不变：Owner-local Gate Freeze → COC Quorum Prefix Freeze → 完整 COC/Owner Admission Union → 不可变 Recovery Cutoff Batch → 带精确回链的独立 Participant Manifest → Pair Linearizable Readback → Owner-specific Reconciliation/Release。

## 3. Exact current H/C source bundle / 当前精确 H/C 源集合

| Authority | Artifact | Exact Blob / Run | Meaning and evidence ceiling |
|---|---|---|---|
| H | Unified schema 1.2.14 / wire 1.3.0 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Exact current wire schema and D ForgetFenceGeneration high-water carrier |
| H | RecoveryJoin 1.0.2 / RecoveryCutoff 1.0.5 | `4b664e3bce465499bcdfd93796349a4ba7074002` / `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` | Generic membership proof and exact cutoff structure |
| H | C/D/I authority-join mapping | `1cbe74eba69325510d6b1019d971661f965eabf8` | Distinct owner verifier seams; no H substitution |
| H | C/D/I crosswalk review | `90cdadd7d80676c1338965576c955a5f336ad0bc` | Generic RecoveryJoin P0 and owner-digest dereference |
| H | Outer-envelope auth validator | `5c5079765f468eaf40690c0c7cbd6b03275a1ff8` | Reference protected-context, integrity/key/channel/identity/replay orchestration |
| H | Provider Outcome validator | `b8cd692d261df7a31a0f65c3e003693e305f73a2` | H 1.2.14 / C 1.0.1 local schema/semantic/digest validator; explicitly not authenticated ingress alone |
| H | Outer-envelope auth tests | `ddf34e9c30edfc378a9482a30837ce04c4abcf97` | 18 reference callback/ordering/replay tests |
| H | Provider Outcome tests | `da1454ed985c84160c4cb6a0462df9d1225fab7f` | 36 H/C local unit/full-path tests |
| H | Positive full-path fixture | `f911027c848d21dd36fb87ba64a201a1455787a7` | Synthetic H envelope + C object; authority callbacks are test doubles |
| H | C crypto interop test sources | `5559fb7a612c8dd92345ceae3a6aa62f4faae41a` / `a49d588ea6f840927fe21ad8c41cd8089dceac29` | Six Python/Node candidate C crypto interoperability methods |
| H | Exact outer-auth closure Phase 3.8.19 | `860c896a388597a4378eda5aa323f276390acf34` | Exact source/run binding and limits |
| H | Outer-auth gap contract Phase 3.8.18 | `fbb7553b0bd0c7a9714304983882ca2cc1fa9cc1` | Confirms outer P0/signer/profile/trust decisions remain open |
| H | Identity-binding baseline Phase 3.6 | `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248` | Protected transport/session context and I trust boundary |
| H | Exact CI run | `44073888935`, commit `0e212731073b36e4fa9ffda8467e60806da1b380`, job `134006790527` | **60 tests / SUCCESS**; raw log `Ran 60 tests in 12.250s`, `OK` |
| H | Workflow | `4459d19f5b4eea058377d9819e48e81eed5c8c4b` | Provider Outcome unittest discovery |
| C | CSubmitOutcome schema 1.0.1 | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | Immutable C-owned provider outcome record |
| C | Sequence namespace amendment Phase 3.11.1 | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C outcome and CKeyStatusEvent share durable C namespace |
| C | RecoveryJoin P0 crosswalk | `df12af95e6859a389ba71eb1b7dba512b9feb8f6` | C row/digest indirection into generic RecoveryJoin P0 |

## 4. Exact cross-owner review matrix / 精确跨 Owner 复审矩阵

| Owner | Exact review Blob | Decision and scope | Remaining conditions |
|---|---|---|---|
| H | Phase 3.8.19 `860c896a388597a4378eda5aa323f276390acf34` | Accepts reference authenticated-ingress gate and 60-test local interface evidence | Outer P0, signer/profile, production trust, replay durability and gateway deployment OPEN |
| C | Phase 3.8.21 `3668c394f7069aa265614fd0636ae12c3c3b88ba` | Accepts boundary separation only; C object P0/signature remains separate | Outer signer role, P0 allowlist, signature profile and production key lifecycle OPEN |
| I | Phase 3.8.17 `893f24036fa9ccf8e438f3312cec8cb9c7cfeff9` | Accepts tri-state trust/identity/replay callback boundary only | Trust root, signer policy, profile registration, key lifecycle, historical verification, anti-rollback and durable replay OPEN |
| D | Phase 3.8.13 `152627e00b96355e2ff370acd643a51168c4c78c` | Accepts H outer authentication as upstream interface only | D lineage, late discovery, barrier terminality and final release CAS OPEN |
| Storage | This v3.2.11 manifest | Binds exact Storage/H/C/I/D candidate bundle | Bidirectional COC joins, same-GID recovery, quorum durability and linearizable readback OPEN |
| A | Fresh exact integration review | **PENDING** | Must review v3.2.11 and the new outer-auth contract before joint candidate registration |

All H/C/I/D reviews are delegated role simulations and source-level architecture reviews, not independent human Owner signatures or formal governance approvals. No role simulation is counted as independent approval or formal risk acceptance.

H/C/I/D 复审均为委托角色模拟与源级架构审查，不是独立人类 Owner 签署或正式治理批准。任何角色模拟均不得计为独立审批或正式风险接受。

## 5. Exact 60-test meaning / 精确 60 项测试含义

The 60 methods comprise 36 H/C Provider Outcome tests, 18 outer-envelope auth tests and six Python/Node C crypto interop methods. The 18 outer-auth tests exercise:
- strict parse and duplicate-key rejection;
- protected transport context and sender/audience/channel claim comparisons;
- tri-state integrity/key-status/channel/identity callbacks;
- replay NEW/SAME_DIGEST_REPLAY/CONFLICT/UNKNOWN behavior;
- no replay reservation before integrity/key checks succeed;
- no domain validation before outer auth;
- separation of authenticated sender authority from message owner_authority.

60 项包括 36 个 H/C Provider Outcome 测试、18 个 Outer Envelope Auth 测试与 6 个 Python/Node C Crypto Interop 方法。18 项 Outer-Auth 测试覆盖 Strict Parse/Duplicate Key、Protected Transport Context/Claim 比较、Integrity/Key Status/Channel/Identity 三态 Callback、Replay 状态、认证失败前不预留 Replay、Auth 前不调用 Domain Validator，以及 Authenticated Sender Authority 与 Message owner_authority 的分离。

**Evidence ceiling:** all outer-auth callbacks and owner-authority callbacks are deterministic test doubles. The run does not compute a production-approved outer P0, authenticate a production envelope signature, register a signer/profile, validate real I trust/key status, connect real channel binding, persist replay state, or prove gateway deployment. It is reference-interface L1/L2 evidence only.

**证据上限：** 所有 Outer-Auth 与 Owner-Authority Callback 均为确定性 Test Double。该 Run 不计算生产批准的 Outer P0，不认证生产 Envelope Signature，不注册 Signer/Profile，不验证真实 I Trust/Key Status，不连接真实 Channel Binding，不持久化 Replay State，也不证明 Gateway 部署。它仅是 Reference Interface L1/L2 证据。

## 6. Critical semantic boundaries / 关键语义边界

1. Outer envelope digest/signature, C object P0/signature, provider evidence digest, I terminal proof, D clearance, Storage resolution and COC commit proof are separate domains.
2. C's `AIMBA-C-CRYPTO-1.0` is scoped to CSubmitOutcome 1.0.1; it is not automatically an outer-envelope profile.
3. H must not equate `owner_authority` with authenticated sender authority kind. The signer-to-owner relation must be authorized by C/I registry policy.
4. I owns trust root, issuer/Principal resolution, key status/revocation, profile approval and anti-rollback policy.
5. H owns transport integration, protected context acquisition, channel binding and replay protocol mechanics; H cannot approve trust roots or key policy.
6. Same-digest replay returns prior durable result and cannot re-run provider side effects; replay conflict is INVALID; unavailable replay authority is UNKNOWN.
7. Only the authenticated wrapper is a candidate ingress entrypoint. Direct local Provider Outcome validation cannot be treated as authenticated message acceptance.
8. Missing/unavailable owner authority remains UNKNOWN; proven contradiction is INVALID.

## 7. Gate state and non-claims / Gate 状态与非声明

- Storage v3.2.3: normative architecture design body; implementation/deployment not claimed.
- Storage v3.2.11: **EXACT CANDIDATE BUNDLE BOUND; FRESH A REVIEW REQUIRED; NOT JOINTLY ACCEPTED / NOT FROZEN**.
- H/C local Provider Outcome + reference outer-auth interface: **60/60 exact CI PASS**.
- Outer-envelope P0/signature preimage/signer role/profile: **OPEN / NOT APPROVED**.
- Production I trust root, key registry/lifecycle, historical verification and anti-rollback: **OPEN / NOT APPROVED**.
- Real protected transport/channel-binding verifier and durable replay ledger: **NOT IMPLEMENTED / NOT VERIFIED**.
- Production C provider evidence/same-key lookup/adapter race/fault/egress: **OPEN**.
- Real I/D/Storage proof authentication and production authority adapters: **NOT IMPLEMENTED / NOT VERIFIED**.
- Complete owner-ledger pagination, D lineage/late-discovery and final release CAS: **OPEN**.
- Storage bidirectional RecoveryJoin, same-GID recovery, quorum durability and linearizable readback: **OPEN**.
- JF-10 P0: **OPEN**.
- R1 Recovery Cutoff Batch completeness: **OPEN**.
- R2 owner-local gate linearization/release: **OPEN**.
- Gate A Storage architecture: **PARTIAL PASS / OPEN**.
- Gate B COC persistence implementation/deployment: **BLOCKED / NOT IMPLEMENTED**.
- Gate C distributed end-to-end fault injection: **DEFERRED TO ENGINEERING / NOT RUN**.
- Multi-PolicyDomain atomicity: **BLOCKED**.
- Production durable acceptance, provider egress, Provider exactly-once, Full Applied, Global Forget completion and physical Forget: **NOT AUTHORIZED / NOT PROVEN**.
- Production activation: **NOT AUTHORIZED**.

本清单不声称独立人类 Owner 签署、生产 Trust Root/Key Custody、真实 C/D/I Sequencer CAS、生产 Membership Verifier、Provider 认证、通用 Exactly-once、分布式故障注入通过、物理 Forget/擦除、Global Forget Completion 或生产就绪。

## 8. Required next sequence / 后续执行顺序

1. A performs a fresh exact-version integration review of v3.2.11 and every pinned Blob.
2. C/I decide the outer-envelope signer role and whether a distinct envelope signature profile is required; do not reuse C object P0 implicitly.
3. I approves the exact trust/key lifecycle, historical key-status and anti-rollback policy.
4. H publishes the exact outer-envelope P0 field allowlist and signing preimage after C/I decisions; add real cross-language crypto vectors.
5. H integrates production transport/channel verifier and durable replay ledger; fault-test crashes between auth, replay reservation and durable ingress.
6. C/D/Storage complete their own production authority proofs and RecoveryJoin/same-GID/COC durability evidence.
7. Only after independent owner-authoritative evidence closes may the project consider protocol freeze, Gate B/C completion or production activation.

## 9. Provenance / 来源说明

This manifest was authored in delegated Storage-role mode. Exact source Blobs and the H workflow run/job were read from GitHub. This is a version-binding and review-routing artifact, not an independent Storage Owner signature, production cryptographic verification or runtime deployment result.

本清单由协调会话模拟 Storage 角色编写。所有源 Blob 与 H Workflow Run/Job 均从 GitHub 读回。本文件仅是版本绑定与复审路由工件，不是独立 Storage Owner 签名、生产密码学验证或 Runtime 部署结果。
