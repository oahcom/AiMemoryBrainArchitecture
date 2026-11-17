# Phase 3.6.17 — Storage v3.2.7 Successor Exact-Version Bundle Manifest
# Phase 3.6.17 — Storage v3.2.7 后继精确版本 Bundle 清单

- Owner perspective: Storage / COC Durable Log and Recovery
- Date: 2026-11-17
- Status: **H 1.2.14 / C 1.0.1 CANDIDATE BUNDLE BOUND; FRESH OWNER REVIEWS AND A REVIEW REQUIRED; NOT JOINTLY ACCEPTED / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- Predecessor exact bundle: Storage v3.2.6, Blob `dbfa37617d109d5891a067769e858085e2ce547a`
- Normative Storage technical body: Storage v3.2.3, Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`
- COC companion §§15–17: Blob `5b950a3a29bd7a5276b92a49a9114d700718b987`
- Provenance: delegated Storage-role coordination artifact; **not an independent human Storage Owner signature**.

## 1. Scope and supersession / 范围与替代关系

This manifest supersedes only the C/H exact-version candidate pins in Storage v3.2.6 §3 and its H evidence status. It does not rewrite Storage v3.2.3 S0a–S4, alter the COC Batch-before-Manifest order, or transfer earlier Owner decisions to changed Blobs. Storage v3.2.3 remains the normative technical body; v3.2.6 remains the historical predecessor bundle.

本清单仅替代 Storage v3.2.6 §3 中 C/H 精确版本候选绑定及其 H 证据状态。不改写 Storage v3.2.3 S0a–S4，不改变 COC Batch-before-Manifest 顺序，也不将旧 Owner 决议转移到新 Blob。Storage v3.2.3 仍是规范技术正文；v3.2.6 是历史前序 Bundle。

A changed Blob invalidates every review that pins the old Blob. Branch names and paths are not version bindings. No 1.2.13 review transfers to 1.2.14. No C/I/D/H role simulation is an independent human Owner signature.

## 2. Unchanged Storage / COC normative base / 不变的 Storage / COC 规范基线

| Authority | Artifact | Exact Blob | Binding |
|---|---|---|---|
| Storage | Storage durable log/recovery protocol v3.2.3 | 5cee0d58575adc0fb3dd20a5c7ab68c2a2711792 | Normative S0a–S4, RecoveryBatch, participant union, JF-10 bridge, same-GID recovery and evidence boundaries |
| COC | COC durable log/recovery companion §§15–17 | 5b950a3a29bd7a5276b92a49a9114d700718b987 | Dual-ledger union manifest, record order, digest chain and recovery joins |
| Storage | Batch-before-Manifest ordering amendment | 9704d110a06d0c2ee98be960054e0396d0b68546 | Batch committed before distinct Manifest with exact backlink |
| Storage | R1/R2 successor-round/release ordering addendum | 0477f0329997e42a1cbf6ecb8127c5c01fa47051 | Immutable RecoveryRound and owner-local release order |
| Predecessor | Storage v3.2.6 successor bundle | dbfa37617d109d5891a067769e858085e2ce547a | Historical H 1.2.13 / C 1.0.1 candidate bundle |

The v3.2.3 S0a–S4 order remains unchanged:
1. I/D/C close their own gates and freeze their own request/admission/effect ledgers.
2. COC restores quorum and freezes exact committed prefix P.
3. Build the complete canonical union of COC participants through P and applicable I/D/C owner-local admissions through their independently frozen high-waters.
4. Commit immutable Recovery Cutoff Batch.
5. Commit the distinct Participant Manifest strictly after Batch, with exact backlink.
6. Linearly read back both records and verify prefix, roots, counts, member set, digests, quorum evidence and BatchPosition < ManifestPosition.
7. Only then reconcile participants; each Owner independently issues its own release.

## 3. Exact current C/H candidate pair / 当前 C/H 精确候选组合

| Role | Artifact | Exact Blob / run | Meaning and evidence ceiling |
|---|---|---|---|
| H | BMCP Unified schema 1.2.14 / wire 1.3.0 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Current structural schema; D ForgetFenceGeneration and owner gate generation carriers |
| H | RecoveryJoin schema 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` | Owner snapshot membership proof and bidirectional owner-admission join carrier |
| H | RecoveryCutoff schema 1.0.5 | `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` | Recovery cutoff structural family |
| H | Authority-join mapping | `1cbe74eba69325510d6b1019d971661f965eabf8` | Separate I terminal, D Forget clearance and Storage resolution verifier seams |
| H | Exact C object-wire mapping | `c196fdc7a9d88e344d37ba2810a9bce1803f8b96` | Unified 1.2.14 ↔ CSubmitOutcome 1.0.1 mapping |
| H | Validator core | `eab961a08d41e871f38543b18ee60cf024977414` | Actual schema, object identity/equality, local semantic and C-P0 digest validation; injected authority callbacks |
| H | Expanded full-path fixture | `f911027c848d21dd36fb87ba64a201a1455787a7` | Complete synthetic H envelope + immutable C object, with test-only I/D/Storage proof refs |
| H | Expanded validator tests | `da1454ed985c84160c4cb6a0462df9d1225fab7f` | 36 H validator methods; Tests 21–34 include full path, 22-wire-field and 64-P0-field mutation, COC nullable-intent branches |
| H | C crypto interop tests | `5559fb7a612c8dd92345ceae3a6aa62f4faae41a`; `a49d588ea6f840927fe21ad8c41cd8089dceac29` | Six Python/Node candidate JCS/Ed25519 interoperability methods |
| H | Provider Outcome workflow | `4459d19f5b4eea058377d9819e48e81eed5c8c4b` | Exact workflow path filters include current schema, validator and test/fixture directory |
| H | Exact current-head Provider Outcome CI | Run `44072037563`; commit `c6faee294e503f32a802ba51f3f3b3eb4bee2cd7`; job `134000402978` | SUCCESS; raw log: 42 tests, 0 failures (36 H validator + 6 C crypto interop) |
| H | Phase 3.8.17 full-path closure | Blob `82f06005e49505c7b33e72e65387dcd9f991dc01` | Delegated H-role 42-test closure including P0 mutation and nullable COC intent |
| H | Phase 3.8.16 exact CI closure | Blob `431d049184ae4622e1dcac3f71176ab1cfc9aa8b` | Records 64 present C-P0 field mutation, nullable COC positive/negative and exact 42-test CI |
| C | CSubmitOutcome immutable schema 1.0.1 | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | C-owned immutable provider outcome; signed sequence_namespace_ref required |
| C | Sequence namespace amendment | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C outcome record and CKeyStatusEvent share C-owned namespace |
| C | Exact 42-test review | Phase 3.8.20 Blob `61ff3716c9c3d3101a0058963c58f089aa1448b0` | Delegated C-role acceptance of P0 projection/full mutation and nullable COC semantics; production C authority OPEN |
| D | Exact 42-test review | Phase 3.8.12 Blob `2bf4514fe7972b72f6c1f904e461f86488d04cda` | Delegated D-role acceptance of D callback boundary only; lineage/currentness/release OPEN |
| I | Exact 42-test review | Phase 3.8.16 Blob `2851d31e4f8caf48348944b885b493c607ca79e1` | Delegated I-role acceptance of COMMIT_WON callback predicate only; trust/L3/currentness OPEN |

### 3.1 Exact CI and evidence ceiling / 精确 CI 与证据上限

H Provider Outcome CI run `44072037563` executed on exact H commit `c6faee294e503f32a802ba51f3f3b3eb4bee2cd7`, job `134000402978`, and completed SUCCESS. The raw job log explicitly records Tests 21–34 and `Ran 42 tests in 26.444s; OK`. The 42 methods comprise 36 H validator methods and six Python/Node C crypto interoperability methods.

Tests 21–34 use actual H Unified 1.2.14 and CSubmitOutcome 1.0.1 schemas, actual local C semantic predicates and actual C-P0 digest/preimage calculation. They cover full positive and negative envelope/object paths; 22 present duplicated wire fields; all 64 present C-P0 members (excluding only derived payload_digest and signature); C sequence namespace mismatch; I COMMIT_WON; D exact operation/Fence; Storage DB-incarnation/GID/PrepareAttempt/participant-ledger callback predicates; valid NOT_INVOKED with null COC intent/reservation and explicit absence reason; and rejection when COCAbsenceReason is absent rather than explicit null.

The H branch HEAD after the exact run contains two additional documentation-only closure records. The tested schema, validator, test, fixture and workflow Blobs are unchanged. The duplicate numeric prefix test_32_ occurs in two different full Python method names; the exact CI log shows both were executed.

**Evidence ceiling:** all I/D/Storage authority callbacks are deterministic test doubles. The C crypto interop suite verifies candidate JCS/Ed25519 vectors but does not register production trust profiles. The local H/C validator does not authenticate the outer H envelope's own payload_digest/signature or transport principal. This is bounded local L1/L2 source evidence, not production authority authentication, provider exactly-once, COC quorum durability or Storage same-GID deployment.

H Provider Outcome CI Run `44072037563` 在精确 H Commit `c6faee...`、Job `134000402978` 上 SUCCESS。Raw Job Log 明确记录 Test 21–34 执行，并显示 `Ran 42 tests in 26.444s; OK`。42 项由 36 个 H Validator 方法和 6 个 Python/Node C Crypto Interoperability 方法组成。

Test 21–34 使用真实 H Unified 1.2.14 / CSubmitOutcome 1.0.1 Schema、真实本地 C Semantic Predicate 与 C-P0 Digest/Preimage 计算，覆盖完整正负 Envelope/Object 路径、22 个现存重复 Wire 字段、全部 64 个现存 C-P0 成员（仅排除派生 payload_digest 与 signature）、C Namespace 不一致、I COMMIT_WON、D Operation/Fence、Storage DB/GID/PrepareAttempt/Participant Ledger Callback Predicate、显式 Absence Reason 的 Nullable COC NOT_INVOKED 正向分支，以及 COCAbsenceReason 字段缺失而非显式 null 时的拒绝。

H 分支在精确 Run 后新增两份仅文档闭环记录。测试 Schema、Validator、Test、Fixture 与 Workflow Blob 均未改变。两个 test_32_ 数字前缀对应不同完整 Python 方法名；精确 CI Log 显示两者均执行。

**证据上限：** 所有 I/D/Storage Authority Callback 均为确定性 Test Double。C Crypto Interop Suite 验证候选 JCS/Ed25519 向量，但不注册生产 Trust Profile。本地 H/C Validator 不认证外层 H Envelope 自身的 payload_digest/signature 或 Transport Principal。这是有限本地 L1/L2 源级证据，不是生产 Authority Authentication、Provider Exactly-once、COC Quorum Durability 或 Storage Same-GID 部署证明。

## 4. Owner review/adoption matrix / Owner 精确审查与采纳矩阵

| Owner | Exact review artifact / Blob | Exact scope actually reviewed | Current bundle disposition |
|---|---|---|---|
| C | Phase 3.8.20 review, Blob `61ff3716c9c3d3101a0058963c58f089aa1448b0` | Exact H/C schema, validator, 42-test source and fixture; P0 projection, 64-field mutation and nullable COC intent | Delegated C-role acceptance of local L1/L2 C semantics; production C trust, provider evidence, live sequencer and egress OPEN |
| D | Phase 3.8.12 review, Blob `2bf4514fe7972b72f6c1f904e461f86488d04cda` | Exact H 42-test source/fixture; D Fence callback predicate and distinction from Storage callback | Delegated D-role acceptance of local D callback boundary only; D lineage completeness, late discovery, pagination, currentness CAS and release OPEN |
| I | Phase 3.8.16 review, Blob `2851d31e4f8caf48348944b885b493c607ca79e1` | Exact H 42-test source/fixture; I COMMIT_WON callback predicate | Delegated I-role acceptance of local predicate only; I proof authentication, trust roots, key custody, historical verification, anti-rollback and final CAS OPEN |
| H | Phase 3.8.17 closure, Blob `82f06005e49505c7b33e72e65387dcd9f991dc01`; Phase 3.8.16 exact CI closure, Blob `431d049184ae4622e1dcac3f71176ab1cfc9aa8b` | Exact H 42-test CI run 44072037563, current test/fixture and source set | Delegated H-role local L1/L2 closure; authority callbacks TEST-ONLY; outer envelope auth OPEN |
| A | Prior Phase 1.H review Blob `ba9bb7358802edbcf362f487e10ba4d432eb6c3e` | Pins previous manifest Blob `d963322...`, old test `c37c5...`, 39-test CI 44071354162 | **SUPERSEDED / NOT CURRENT** by H 42-test C-P0/nullable-COC expansion; fresh A exact re-review required |
| Storage | This v3.2.7 manifest | Exact-version bundle binding and review routing | Delegated Storage-role artifact, not independent Storage Owner signature |

C/D/I/H reviews are exact delegated role artifacts, not independent human Owner signatures. They review the exact 42-test source and current fixture at bounded domain scope. They do not authenticate production proofs or close any production Gate. A Phase 1.H is stale because H test source and CI changed after its pinned manifest.

C/D/I/H 审查是精确的角色审查工件，不是真正独立人类 Owner 签署。它们以有限领域范围复审了精确 42 项测试源与当前 Fixture，但不认证生产 Proof，也不关闭任何生产 Gate。A Phase 1.H 因 H Test Source 与 CI 在其绑定 Manifest 后变化而过期。

## 5. Required semantic and operational joins / 必需语义与运行 Join

1. C `payload_digest` equals H `c_submit_outcome_digest`; BMCP envelope digest and Provider Outcome Evidence digest remain distinct domains.
2. C `sequence_namespace_ref` must match authenticated CKeyStatusEvent namespace and the durable C signing sequencer.
3. I terminal decision is independently verified; provider invocation authorization requires the applicable I `COMMIT_WON` proof, not merely any I terminal outcome.
4. D Forget clearance independently verifies FenceGeneration, barrier/lineage membership and final effect boundary.
5. Storage resolution independently verifies DB incarnation, GID, PrepareAttempt, participant ledger and same-GID terminal resolution/visibility.
6. Missing authority callback/evidence/currentness/anti-rollback is UNKNOWN; proven contradiction is INVALID.
7. Batch-before-Manifest, exact backlink, digest-domain separation, quorum and linearizable readback remain required.
8. Owner-local release requires each Owner's fresh final currentness CAS and signed release; Storage/COC cannot release I/D/C gates.
9. Any H/C/I/D/Storage Blob change invalidates the affected review and requires a new exact manifest/review.

## 6. Gate state and non-claims / Gate 状态与非声明

- Storage technical architecture v3.2.3: normative candidate body unchanged.
- Storage v3.2.7: **CURRENT EXACT CANDIDATE BUNDLE BOUND; NOT JOINTLY ACCEPTED / NOT FROZEN**.
- H Unified 1.2.14 / CSubmitOutcome 1.0.1 local validator CI: **SUCCESS, 42 tests; complete local schema/semantic/C-P0 path, 22 duplicate wire fields, 64 present P0 members, nullable COC intent and bounded authority callback predicates PASS with TEST-ONLY authority callbacks**.
- Full local H envelope + C object schema/semantic/digest path: **PASS**.
- All present duplicated wire fields in fixture: **22/22 mutation rejection PASS**.
- All present C-P0 members: **64/64 mutation rejection PASS; payload_digest/signature excluded as derived/excluded members**.
- Nullable COC NOT_INVOKED branch with explicit absence reason: **PASS**; absent COCAbsenceReason property: **INVALID**.
- Production I/D/Storage authority callback adapters: **NOT IMPLEMENTED / NOT VERIFIED**.
- Outer H envelope payload_digest/signature and transport-principal authentication: **OPEN / NOT COVERED BY THIS VALIDATOR**.
- JF-10 P0: **OPEN**.
- R1 Recovery Cutoff Batch completeness: **OPEN**.
- R2 owner-local gate linearization/release: **OPEN**.
- Gate A Storage architecture: **PARTIAL PASS / OPEN**.
- Gate B COC persistence deployment: **BLOCKED**.
- Gate C executable end-to-end fault injection: **DEFERRED TO ENGINEERING / NOT RUN**.
- Multi-PolicyDomain atomicity: **BLOCKED**.
- C/I profiles, production trust roots, key custody and anti-rollback: **NOT APPROVED / OPEN**.
- Production activation, production provider egress, Provider exactly-once, Full Applied, Global Forget Completion and physical Forget: **NOT AUTHORIZED / NOT PROVEN**.

本清单不声称生产 Owner 签名、生产 Trust Root/Key Custody、真实 I/D/C Sequencer CAS、生产 Membership Verifier、Provider 认证、通用 exactly-once、分布式故障注入通过、物理 Forget/擦除、Global Forget Completion 或生产就绪。

## 7. Required next sequence / 后续执行顺序

1. A must issue a fresh exact integration review against the final read-back Blob of this v3.2.7 manifest; Phase 1.H is stale.
2. H must implement/verify outer-envelope payload_digest/signature and authenticated transport-principal checks at the H gateway boundary; C object validation is not envelope authentication.
3. H/C must continue strict raw JSON full-path vectors, signature/preimage mismatch, key-status/currentness and anti-rollback coverage.
4. I must connect COMMIT_WON verification to I-authoritative terminal proofs, request/admission ledger, key status/history, PermissionEpoch and final currentness CAS.
5. D must connect Fence/lineage/barrier proof to complete D-authoritative pagination, late-discovery successor snapshot and final D-local CAS.
6. Storage must connect same-GID resolution to DB incarnation, GID, PrepareAttempt, participant ledger, terminal outcome and visibility marker.
7. C must close production provider issuer truth, same-key lookup, adapter send-vs-close, lost ACK/retry/failover and egress linearization.
8. Storage must prove COC quorum persistence, bidirectional RecoveryJoin, exact prefix/readback and owner-local release ordering. CI alone does not change any Gate status.

1. A 必须针对本 v3.2.7 Manifest 最终读回 Blob 发布全新精确集成审查；Phase 1.H 已过期。
2. H 必须在 Gateway 边界实现/验证外层 Envelope payload_digest/signature 与认证 Transport Principal；C Object 校验不是 Envelope Authentication。
3. H/C 必须继续覆盖 Raw JSON Full-Path、Signature/Preimage 不一致、Key Status/Currentness 与 Anti-Rollback。
4. I 必须将 COMMIT_WON 验证连接 I 权威 Terminal Proof、Request/Admission Ledger、Key Status/History、PermissionEpoch 与最终 Currentness CAS。
5. D 必须将 Fence/Lineage/Barrier Proof 连接 D 权威完整分页、Late-Discovery Successor Snapshot 与最终 D-local CAS。
6. Storage 必须将 Same-GID Resolution 连接 DB Incarnation、GID、PrepareAttempt、Participant Ledger、Terminal Outcome 与 Visibility Marker。
7. C 必须关闭生产 Provider Issuer Truth、Same-Key Lookup、Adapter Send-vs-Close、Lost ACK/Retry/Failover 与 Egress Linearization。
8. Storage 必须证明 COC Quorum Persistence、双向 RecoveryJoin、Exact Prefix/Readback 与 Owner-local Release Ordering。CI 本身不改变任何 Gate 状态。

## 8. Provenance / 来源说明

This manifest was authored in delegated Storage-role coordination mode. Exact file Blobs were fetched from their named owner branches and the H workflow run/job logs were read directly. This is a candidate version-binding and review-routing artifact, not an independent Storage Owner signature or runtime deployment result.

本清单由协调会话模拟 Storage 角色编写。精确文件 Blob 来自对应 Owner 分支读取，H Workflow Run/Job Log 已直接核验。本文件仅为候选版本绑定与复审路由工件，不是独立 Storage Owner 签名，也不是 Runtime 部署结果。
