# Phase 3.6.22 — Storage v3.2.11 Exact-Version Bundle: 64-Field C-P0 and Nullable COC Closure
# Phase 3.6.22 — Storage v3.2.11 精确版本 Bundle：64 字段 C-P0 与 Nullable COC 闭环

- Owner perspective: Storage / COC Durable Log and Recovery
- Date: 2026-11-17
- Status: **H 1.2.14 / C 1.0.1 EXACT SOURCE + 42-TEST CI BOUND; C/H/I/D/STORAGE ROLE REVIEWS RECORDED; FRESH A REVIEW REQUIRED; NOT JOINTLY ACCEPTED / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- Immediate predecessor: Storage v3.2.10 expanded bundle, Blob `4e2261dfceee5606fa73c08caadf0829acaa5fa0`
- Earlier v3.2.10 candidate manifest: Blob `0c1a9c7bceb9a32974e92934a94ca4e8ff9a488e`
- Predecessor A review Phase 1.J: Blob `c97b1801a24c1e0a1a0167595b1b464cee22cf6e` (historical; does not transfer)
- Normative Storage technical body v3.2.3: Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`
- COC companion §§15–17: Blob `5b950a3a29bd7a5276b92a49a9114d700718b987`
- Storage per-authority serialization topology ADR: Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`
- Provenance: delegated Storage-role successor manifest; **not an independent human Storage Owner signature**.
- English and Chinese are normative peers.

## 1. Scope and supersession / 范围与替代关系

This manifest supersedes the H test/fixture/CI and C/H/I/D/Storage review pins in Storage v3.2.10. It binds the expanded 64-field C-P0 mutation suite, nullable COC no-intent NOT_INVOKED positive case, and exact current-head CI run. It does not rewrite Storage v3.2.3 S0a–S4, change the COC Batch-before-Manifest order, or upgrade any production gate.

本清单替代 Storage v3.2.10 中 H Test/Fixture/CI 与 C/H/I/D/Storage 复审绑定，纳入扩展 64 字段 C-P0 Mutation、Nullable COC No-Intent NOT_INVOKED 正向案例与精确当前 HEAD CI。它不改写 Storage v3.2.3 S0a–S4，不改变 COC Batch-before-Manifest 顺序，也不提升任何生产 Gate。

A changed Blob invalidates reviews that pin its predecessor. Paths, branch names and version labels are not version bindings. The current candidate pair remains H Unified 1.2.14 / wire 1.3.0 and immutable CSubmitOutcome 1.0.1. Local full-path CI is not production authority verification.

Blob 变化会使绑定旧版本的审查失效。路径、分支名和版本标签不是版本绑定。当前候选版本对仍为 H Unified 1.2.14 / Wire 1.3.0 与不可变 CSubmitOutcome 1.0.1。本地 Full-Path CI 不等于生产权威验证。

## 2. Unchanged Storage / COC normative base / 不变的 Storage / COC 规范基线

| Authority | Artifact | Exact Blob | Binding |
|---|---|---|---|
| Storage | Durable log/recovery protocol v3.2.3 | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Normative S0a–S4, RecoveryBatch, participant union, JF-10 bridge and same-GID recovery |
| COC | Durable log/recovery companion §§15–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Dual-ledger union, prepared-participant identity, record order, digest chain and recovery joins |
| Storage | Batch-before-Manifest amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` | Batch committed before distinct Manifest with exact backlink |
| Storage | R1/R2 successor-round/release ordering addendum | `0477f0329997e42a1cbf6ecb8127c5c01fa47051` | Immutable RecoveryRound and owner-local release order |
| Storage | Per-authority serialization topology ADR | `bb544ba2f346bdc130d524bd5c7310d86f367988` | One durable CanonicalAuthoritySerializationAnchor per BrainAuthorityRef; L1 logical topology only |
| Predecessor | Storage v3.2.10 expanded manifest | `4e2261dfceee5606fa73c08caadf0829acaa5fa0` | Historical 38-method/22-wire-field source and review pins |

The normative S0a–S4 order remains unchanged:
1. I/D/C independently close their own gates and freeze request/admission/effect ledgers.
2. COC restores quorum and freezes exact committed prefix P.
3. Construct the complete canonical union of COC participants through P and applicable I/D/C owner-local admissions through independently frozen high-waters.
4. Commit immutable Recovery Cutoff Batch.
5. Commit distinct Participant Manifest strictly after Batch, with exact backlink.
6. Linearizably read back both records and verify prefix, roots, counts, member set, digests, quorum evidence and BatchPosition < ManifestPosition.
7. Only then reconcile participants; each Owner independently issues its own release.

## 3. Exact current H/C protocol and source bundle / 当前 H/C 协议与源文件精确 Bundle

| Authority | Artifact | Exact Blob / Run | Meaning and evidence ceiling |
|---|---|---|---|
| H | BMCP Unified schema 1.2.14 / wire 1.3.0 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Current exact wire schema; includes distinct D ForgetFenceGeneration high-water |
| H | RecoveryJoin 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` | Generic owner membership proof envelope and bidirectional joins |
| H | RecoveryCutoff 1.0.5 | `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` | Exact recovery cutoff structural family |
| H | Authority-Join mapping Phase 3.8.10 | `1cbe74eba69325510d6b1019d971661f965eabf8` | Exact H 1.2.14 × C 1.0.1 mapping and separate C/I/D/Storage verifier seams |
| H | Provider Outcome validator core | `eab961a08d41e871f38543b18ee60cf024977414` | Exact C object dereference/equality, C-P0 digest and tri-state orchestration |
| H | Current Provider Outcome test source | `da1454ed985c84160c4cb6a0462df9d1225fab7f` | 36 H validator methods, including 64-field C-P0 matrix and nullable COC path |
| H | Full positive H envelope + C object fixture | `f911027c848d21dd36fb87ba64a201a1455787a7` | Synthetic fixture with explicit C/I/D/Storage/COC references |
| H | C crypto interop test sources | `5559fb7a612c8dd92345ceae3a6aa62f4faae41a` / `a49d588ea6f840927fe21ad8c41cd8089dceac29` | Six Python/Node candidate crypto interop methods |
| H | Provider Outcome workflow | `4459d19f5b4eea058377d9819e48e81eed5c8c4b` | Pinned Python and Node/JCS dependencies; unittest discovery |
| H | Phase 3.8.16 exact-head closure | `431d049184ae4622e1dcac3f71176ab1cfc9aa8b` | Binds exact 64-field test source and run |
| H | Exact current CI | Run `44072037563`, commit `c6faee294e503f32a802ba51f3f3b3eb4bee2cd7`, job `134000402978` | Completed / success; 42 methods across three Python files |
| C | CSubmitOutcome immutable schema 1.0.1 | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | C-owned immutable provider outcome; signed sequence_namespace_ref |
| C | CSubmitOutcome 1.0.1 fixture vectors | `c447f8c2908469c52cb52a448101495a331277c5` | Ten candidate schema/semantic vectors |
| C | C sequence namespace amendment Phase 3.11.1 | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C record_sequence and CKeyStatusEvent event_sequence share durable C namespace |
| C | C RecoveryJoin P0 crosswalk | `df12af95e6859a389ba71eb1b7dba512b9feb8f6` | C owner entry/digest indirection into generic RecoveryJoin P0 |
| C | C expanded C-P0/nullable COC review Phase 3.8.20 | `461a8148089bd3c190c623da5ca05263ba8b1f97` | Accepts local 64-field C-P0 mutation and nullable NOT_INVOKED branch as L1/L2 candidate |
| I | I P0 allowlist current Blob | `44986f5f864bcdc1a79d34978273644d381a68c0` | Exact I common/proof-family P0 candidate |
| I | I final H callback/RecoveryJoin review | `a1c8c3cdedfb5ba6258e4db025b294d989a834e4` | Accepts H 1.2.14/RecoveryJoin and I callback boundary as L1/L2 candidate |
| I | I expanded C-P0/nullable COC/envelope-auth review | `1171f82f3d5bac58a6d105bcc18de649b7398385` | Accepts local I callback predicate; outer envelope authentication remains OPEN |
| D | D RecoveryJoin P0 crosswalk | `c4adf827dd62d44c43b8e871dec4835581508adf` | D operation/scope/fence/barrier/lineage digest indirection |
| D | D expanded nullable COC/P0 review | `8f064d29f4868ad5ad598aa49f12bf7709b9a993` | Accepts local D callback boundary; real lineage/release remains OPEN |
| Storage | Storage expanded nullable COC/same-GID review | `403450ed7c5d784491c66ea99f909669df962995` | Accepts synthetic Storage callback tuple only; real same-GID remains OPEN |

### 3.1 Exact CI and test meaning / 精确 CI 与测试含义

Run `44072037563` completed successfully on exact commit `c6faee294e503f32a802ba51f3f3b3eb4bee2cd7`, job `134000402978`. The suite contains 42 test methods: 36 H validator unit/full-path methods and six C crypto interoperability methods.

Tests 21–34 load real H/C schemas and the synthetic full fixture, then call the actual validator without patching schema, semantic or C-P0 digest/preimage primitives. They cover:
- all 22 present duplicated H wire fields, one mutation at a time;
- all 64 present C-P0 members, one mutation at a time, synchronizing duplicated wire values where applicable;
- synchronized C-P0 + wire member mutation while retaining the old digest;
- C sequence namespace mismatch through the key-status test callback;
- I COMMIT_WON vs REVOCATION_WON callback predicate;
- exact D operation/Fence reference and Storage DB-incarnation/GID/PrepareAttempt/participant-ledger callback predicates;
- valid NOT_INVOKED + PROVEN_NONE with no COC intent/reservation and explicit absence reason;
- rejection of an absent COCAbsenceReason member.

Run `44072037563` 在精确 Commit `c6faee...` 上成功，Job `134000402978` 成功。套件共 42 个测试方法：36 个 H Validator Unit/Full-Path 方法和 6 个 C Crypto Interop 方法。

Test 21–34 加载真实 H/C Schema 与合成 Full Fixture，调用真实 Validator，不 Patch Schema/Semantic/C-P0 Digest/Preimage 基础函数。覆盖 22 个现存 H Wire 重复字段、64 个现存 C-P0 成员、同步修改 Wire/C-P0 后保留旧 Digest、C Sequence Namespace、I COMMIT_WON/REVOCATION_WON、D Operation/Fence、Storage DB Incarnation/GID/PrepareAttempt/Participant Ledger、有效无 COC Intent 的 NOT_INVOKED 分支，以及 COCAbsenceReason 缺失拒绝。

The authority callbacks remain deterministic test doubles. They do not authenticate production C/I/D/Storage proof payloads. The outer H envelope's own payload_digest/signature and authenticated transport principal are not verified by this Provider Outcome validator; H Gateway/Auth must verify them before durable acceptance. C object signature verification is not outer envelope authentication.

Authority Callback 仍是确定性 Test Double，不认证生产 C/I/D/Storage Proof Payload。外层 H Envelope 自身 payload_digest/signature 与 Authenticated Transport Principal 不由此 Provider Outcome Validator 验证；H Gateway/Auth 必须在 Durable Acceptance 前完成认证。C Object Signature 验证不等于外层 Envelope Authentication。

## 4. Owner review matrix / Owner 复审矩阵

| Owner | Exact review Blob | Decision and scope | Remaining conditions |
|---|---|---|---|
| H | Phase 3.8.16 closure `431d049...` | Accepts 64-field C-P0 matrix and nullable COC path as L1/L2 local evidence | Outer envelope auth, production callbacks, L3 and deployment remain OPEN |
| C | Phase 3.8.20 review `461a814...` | Accepts C-P0 mutation and nullable NOT_INVOKED semantics | Production C profile/trust/sequencer/provider evidence and egress safety |
| I | Phase 3.8.16 review `1171f82...` | Accepts I callback predicate and nullable COC branch; explicitly flags envelope auth | Production I verifier/trust/key custody/revocation/anti-rollback and envelope auth |
| D | Phase 3.8.12 review `8f064d...` | Accepts D callback boundary and confirms nullable COC does not bypass D fence | Full lineage, late discovery, barrier terminality and release CAS |
| Storage | Phase 3.8.5 review `403450...` | Accepts nullable COC and same-GID callback as local interface evidence | Real DB incarnation/GID recovery, COC quorum and linearizable readback |
| A | No review of this v3.2.11 manifest yet | **PENDING** | Fresh exact-version A integration review required; v3.2.10 A reviews do not transfer |

All C/H/I/D/Storage reviews in this coordinating workflow are delegated role simulations, not independent human Owner signatures or formal organizational approvals. They establish technical review scope only.

本协调工作流中的 C/H/I/D/Storage 复审均为角色模拟，不是独立人类 Owner 签署或正式组织批准，仅界定技术复审范围。

## 5. Storage joins and gate obligations / Storage Join 与 Gate 义务

1. C `payload_digest` equals H `c_submit_outcome_digest`; BMCP envelope digest and Provider Outcome Evidence digest remain distinct domains.
2. C `sequence_namespace_ref` equals authenticated CKeyStatusEvent namespace and durable C sequencer namespace.
3. I terminal authorization independently verifies the exact I proof and required `COMMIT_WON`; generic terminality is insufficient.
4. D Forget clearance independently verifies FenceGeneration, complete affected lineage/barrier membership and final effect boundary.
5. Storage resolution independently verifies DB incarnation, GID, PrepareAttempt, participant ledger and same-GID terminal resolution/visibility.
6. Missing callback/evidence/currentness/anti-rollback is UNKNOWN; proven contradiction is INVALID.
7. Batch-before-Manifest, exact backlink, digest-domain separation, quorum and linearizable readback remain required.
8. Each Owner's release requires its own final currentness CAS and signed release; Storage/COC cannot release I/D/C gates.
9. Outer H envelope digest/signature/transport identity must be authenticated by H Gateway/Auth before durable acceptance.
10. Any source Blob change invalidates affected reviews and requires a new exact manifest/review.

## 6. Gate state and non-claims / Gate 状态与非声明

- Storage v3.2.3: normative design body unchanged.
- Storage v3.2.11: **EXACT CANDIDATE BUNDLE BOUND; NOT JOINTLY ACCEPTED / NOT FROZEN**.
- H local schema/semantic/C-P0 full-path and nullable COC conformance: **42/42 test methods on exact CI run 44072037563**.
- Outer H envelope authentication: **OPEN**.
- Real production C/I/D/Storage authority adapters: **NOT IMPLEMENTED / NOT VERIFIED**.
- Production C profile/key status/provider truth/same-key lookup/egress safety: **OPEN**.
- Production I trust root/key custody/revocation/anti-rollback: **NOT APPROVED / OPEN**.
- D lineage completeness/late discovery/final release CAS: **OPEN**.
- Storage bidirectional RecoveryJoin/same-GID recovery/COC quorum/linearizable readback: **OPEN**.
- JF-10 P0: **OPEN**.
- R1 Recovery Cutoff Batch completeness: **OPEN**.
- R2 owner-local gate linearization/release: **OPEN**.
- Gate A Storage architecture: **PARTIAL PASS / OPEN**.
- Gate B COC persistence deployment: **BLOCKED / NOT IMPLEMENTED**.
- Gate C distributed end-to-end fault injection: **DEFERRED / NOT RUN**.
- Multi-PolicyDomain atomicity: **BLOCKED**.
- Provider egress/Exactly-once, Full Applied, Global Forget completion, physical Forget and Production Activation: **NOT AUTHORIZED / NOT PROVEN**.

## 7. Required next sequence / 后续执行顺序

1. A performs a fresh exact-version integration review of this v3.2.11 manifest and all pinned Blobs.
2. H implements and independently tests outer-envelope payload digest/signature, integrity proof, channel binding and authenticated transport-principal binding.
3. Replace deterministic I/D/Storage callbacks with owner-authoritative proof verifiers and currentness/anti-rollback sources.
4. C completes production C profile registration, key-status/sequencer trust and provider-specific issuer/same-key/adapter race evidence.
5. D executes complete lineage pagination, late-discovery fault campaign and final D-local release CAS.
6. Storage proves bidirectional COC participant ↔ I/D/C owner admission joins, same-GID RecoveryJoin, quorum persistence and linearizable Batch/Manifest readback.
7. Only after independent owner-authoritative evidence closes may the project consider protocol freeze, Gate B/C completion or production activation.

## 8. Provenance / 来源说明

This manifest was authored in delegated Storage-role mode. Exact source Blobs and the H workflow run/job were read from GitHub. It is a version-binding and review-routing artifact, not an independent Storage Owner signature, runtime deployment result or production conformance statement.

本清单由协调会话模拟 Storage 角色编写。所有源 Blob 与 H Workflow Run/Job 均从 GitHub 读回。本文件仅为版本绑定与复审路由工件，不是独立 Storage Owner 签名、Runtime 部署结果或生产符合性声明。
