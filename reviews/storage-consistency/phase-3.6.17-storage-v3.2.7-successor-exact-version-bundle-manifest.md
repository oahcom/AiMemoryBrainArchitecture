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
| H | Full positive envelope + C object fixture | `c80247a6ecfbb4a29ff0993e8e2aea4829d00626` | Synthetic TEST-ONLY full envelope/object fixture |
| H | Validator tests | `dccf8c099c18807ec072870d32604d0912209f01` | 26 H validator methods, including unmocked local full-path tests 21–25 |
| H | Provider Outcome workflow | `4459d19f5b4eea058377d9819e48e81eed5c8c4b` | Path filters include current H schema, validator and fixture/test directory |
| H | Exact full-path CI | Run `44069941327`; commit `ba2c9341fee4eb9ca9e665c74bdd37b4675dd251`; job `133993324484` | SUCCESS; 32 tests total: 26 H validator + 6 Python/Node C crypto interop |
| H | Full-path closure record | Blob `5f487321b273ede41a7c23c3f94b6c0625968439` | Delegated H-role closure; local schema/semantic/digest path PASS; production callbacks TEST-ONLY |
| C | CSubmitOutcome immutable schema 1.0.1 | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | C-owned immutable provider outcome; signed sequence_namespace_ref required |
| C | Sequence namespace amendment | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C outcome record and CKeyStatusEvent share C-owned namespace |
| C | Full-path exact review | Blob `4be9c1cd8f116086bab58340f07e38ddfc223e21` | Delegated C-role acceptance of local H/C schema/semantic/digest path; production C trust/egress OPEN |
| D | Full-path exact review | Blob `ccdae9b45affb23c6741b5cceb27004b35a8e03e` | Delegated D-role acceptance of D callback boundary; lineage, pagination and release CAS OPEN |
| I | Full-path exact review | Blob `7c65650a37c8c0f270451fb0419e93259fc38151` | Delegated I-role acceptance of I terminal callback boundary; trust/L3/currentness OPEN |

### 3.1 Meaning of H full-path CI / H Full-Path CI 的含义

H Provider Outcome CI run `44069941327` completed SUCCESS on exact commit `ba2c9341fee4eb9ca9e665c74bdd37b4675dd251`, job `133993324484`. The job log explicitly records tests 21–25 executing and `Ran 32 tests ... OK`: 26 H validator test methods and six Python/Node C crypto interoperability methods.

The positive full-path test loads actual H Unified 1.2.14 and CSubmitOutcome 1.0.1 schemas plus the synthetic envelope/object fixture, then calls `validate_provider_outcome` without patching schema validation, semantic validation or C-P0 digest/preimage computation. Negative tests prove a duplicated `provider_ref` mismatch returns INVALID, a changed C payload digest fails recomputation, missing I/D/Storage callbacks return UNKNOWN, and a False I/D/Storage callback returns INVALID.

Current H branch HEAD `c22e8f2c00f289666eb77c2c37e0a791233f50ef` is three commits ahead of the tested commit; comparison shows documentation-only changes. The current schema, validator, full-path test and fixture Blobs are byte-identical to the exact CI inputs.

**Evidence ceiling:** all authority-dependent callbacks in the positive fixture are deterministic test doubles. The C crypto interop suite separately tests candidate JCS/Ed25519 vectors, but this full-path fixture does not authenticate production C signature/key status, provider issuer truth, I/D/Storage proofs, live owner ledgers, COC quorum or Storage same-GID resolution. This is a full local schema/semantic/C-P0 digest validation path, not production authority conformance.

H Provider Outcome CI Run `44069941327` 在精确 Commit `ba2c9341fee4eb9ca9e665c74bdd37b4675dd251`、Job `133993324484` 上 SUCCESS。Job Log 明确记录 Test 21–25 执行，并显示 `Ran 32 tests ... OK`：26 个 H Validator 测试方法和 6 个 Python/Node C Crypto Interoperability 测试方法。

正向 Full-Path Test 加载真实 H Unified 1.2.14、CSubmitOutcome 1.0.1 Schema 与合成 Envelope/Object Fixture，调用真实 `validate_provider_outcome`，没有 Patch Schema、Semantic 或 C-P0 Digest/Preimage 计算。负向测试证明 Wire `provider_ref` 不一致为 INVALID、C Payload Digest 变异重算失败、缺少 I/D/Storage Callback 为 UNKNOWN、False Callback 为 INVALID。

当前 H HEAD `c22e8f2c00f289666eb77c2c37e0a791233f50ef` 相对测试 Commit 仅有三项文档变更；当前 Schema、Validator、Full-Path Test 与 Fixture Blob 均与 CI 输入字节一致。

**证据上限：** 正向 Fixture 中所有 Authority-dependent Callback 均为确定性 Test Double。C Crypto Interop 套件另行测试候选 JCS/Ed25519 向量，但 Full-Path Fixture 不认证生产 C Signature/Key Status、Provider Issuer Truth、I/D/Storage Proof、实时 Owner Ledger、COC Quorum 或 Storage Same-GID Resolution。这是完整本地 Schema/Semantic/C-P0 Digest 验证路径，不是生产 Authority Conformance。

## 4. Owner review/adoption matrix / Owner 精确审查与采纳矩阵

| Owner | Exact review artifact / Blob | Exact scope actually reviewed | Current bundle disposition |
|---|---|---|---|
| C | Phase 3.8.18 full-path review, Blob `4be9c1cd8f116086bab58340f07e38ddfc223e21` | Exact H schema `09fcd1...`, C schema `a631bc...`, mapping `1cbe74...`, validator `eab961...`, test `dccf8...`, fixture `c80247...` | Delegated C-role acceptance of local schema/semantic/digest path as L1/L2 candidate; production C trust, provider evidence and egress OPEN |
| D | Phase 3.8.10 full-path review, Blob `ccdae9b45affb23c6741b5cceb27004b35a8e03e` | Exact H schema, mapping, validator, test and fixture Blobs above; D clearance callback boundary | Delegated D-role acceptance of local callback boundary only; lineage completeness, late discovery, pagination, currentness CAS and production release OPEN |
| D | Phase 3.8.9 mapping review, Blob `40fee15d7e42d68da231ea161896f85df2921669` | Exact authority-join mapping `1cbe74...` and D P0/crosswalk | D proof-carrier/mapping candidate; no production verifier or release proof |
| I | Phase 3.8.14 full-path review, Blob `7c65650a37c8c0f270451fb0419e93259fc38151` | Exact H schema, mapping, I P0 `44986f...`, validator, test and fixture Blobs above | Delegated I-role acceptance of local callback boundary only; production trust roots, key custody, historical verification, anti-rollback, L3 and final I CAS OPEN |
| I | Phase 3.8.13 mapping review, Blob `34b29f405d4e8ceb1a039666bfe84518f62355f8` | Exact authority-join mapping `1cbe74...`, RecoveryJoin 1.0.2 and I P0 | I terminal-proof carrier/P0 compatibility accepted as L1/L2 candidate; trust/L3/production OPEN |
| H | Phase 3.8.14 full-path closure, Blob `5f487321b273ede41a7c23c3f94b6c0625968439` | Exact H/C schemas, mapping, validator, test, fixture and CI 44069941327 | Delegated H-role local full-path closure; authority callbacks TEST-ONLY |
| A | Prior Phase 1.F review, Blob `85cd97bb66461440c7c08c4397e6cd496217b6fd` | Pins obsolete manifest Blob `4435fc...`, earlier H test Blob `53774...`, CI 44068247661 | **SUPERSEDED / NOT CURRENT**. Fresh A review required against final current manifest Blob |
| Storage | This v3.2.7 manifest | Exact-version bundle binding and review routing | Delegated Storage-role artifact, not independent Storage Owner signature |

C/D/I/H reviews above are exact delegated role artifacts and evidence of domain-boundary review, not independent human Owner signatures. C Phase 3.8.18, D Phase 3.8.10 and I Phase 3.8.14 specifically pin the current full-path test and fixture Blobs. A's previous Phase 1.F review is stale because it pins an earlier manifest Blob and earlier H test/CI evidence.

上述 C/D/I/H 审查是精确的角色审查工件，可证明领域边界审查范围，但不是独立人类 Owner 签署。C Phase 3.8.18、D Phase 3.8.10、I Phase 3.8.14 均精确绑定当前 Full-Path Test 与 Fixture Blob。A 先前 Phase 1.F Review 因绑定旧 Manifest Blob 与旧 H Test/CI 证据而过期。

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
- H Unified 1.2.14 / CSubmitOutcome 1.0.1 full local validator CI: **SUCCESS, 32 tests; complete local schema/semantic/C-P0 digest path PASS with TEST-ONLY authority callbacks**.
- Full unmocked H envelope + C object positive path and bounded negative/tri-state tests: **PASS**.
- Full mutation matrix for every duplicated wire field, exact identity/digest joins, stale/currentness branches and production authority verification: **OPEN**.
- Production I/D/Storage authority callback adapters: **NOT IMPLEMENTED / NOT VERIFIED**.
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

1. A must issue a fresh exact integration review against the final read-back Blob of this v3.2.7 manifest; the old Phase 1.F review is stale.
2. H must expand negative vectors to every duplicated wire field, exact C identity/digest, C sequence namespace/key-status mismatch, rollback/fork and malformed raw JSON cases.
3. I must bind the terminal verifier to I-authoritative proof, request/admission ledger, PermissionEpoch, currentness and COMMIT_WON semantics; missing evidence remains UNKNOWN.
4. D must bind the clearance verifier to complete lineage membership, FenceGeneration, barrier root/terminality, late-discovery successor snapshot and final D-local CAS.
5. Storage must bind same-GID resolution to DB incarnation, GID, PrepareAttempt, participant ledger, authoritative terminal resolution and visibility marker.
6. C must separately close provider issuer truth, same-key lookup, adapter send-vs-close, lost ACK, retry/replay and multi-replica egress fault cases.
7. Storage must prove COC quorum persistence, bidirectional RecoveryJoin, exact prefix/readback and owner-local release ordering. A fresh A review does not close R1/R2 or any production Gate.

1. A 必须针对本 v3.2.7 Manifest 最终读回 Blob 发布全新精确集成审查；旧 Phase 1.F 已过期。
2. H 必须扩展负向向量，覆盖每个重复 Wire 字段、C Identity/Digest、C Sequence Namespace/Key Status 不一致、Rollback/Fork 与 Raw JSON 错误。
3. I 必须将 Terminal Verifier 绑定 I 权威 Proof、Request/Admission Ledger、PermissionEpoch、Currentness 与 COMMIT_WON 语义；缺失证据仍为 UNKNOWN。
4. D 必须将 Clearance Verifier 绑定完整 Lineage Membership、FenceGeneration、Barrier Root/Terminality、Late-Discovery 后继 Snapshot 与最终 D-local CAS。
5. Storage 必须将 Same-GID Resolution 绑定 DB Incarnation、GID、PrepareAttempt、Participant Ledger、权威终态 Resolution 与 Visibility Marker。
6. C 必须独立关闭 Provider Issuer Truth、Same-Key Lookup、Adapter Send-vs-Close、Lost ACK、Retry/Replay 与多副本 Egress Fault。
7. Storage 必须证明 COC Quorum Persistence、双向 RecoveryJoin、Exact Prefix/Readback 与 Owner-local Release Ordering。A 新审查不关闭 R1/R2 或任何生产 Gate。

## 8. Provenance / 来源说明

This manifest was authored in delegated Storage-role coordination mode. Exact file Blobs were fetched from their named owner branches and the H workflow run/job logs were read directly. This is a candidate version-binding and review-routing artifact, not an independent Storage Owner signature or runtime deployment result.

本清单由协调会话模拟 Storage 角色编写。精确文件 Blob 来自对应 Owner 分支读取，H Workflow Run/Job Log 已直接核验。本文件仅为候选版本绑定与复审路由工件，不是独立 Storage Owner 签名，也不是 Runtime 部署结果。
