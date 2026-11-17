# Phase 3.6.20 — Storage v3.2.10 Exact-Version Bundle Manifest: H 39-Test C-P0 Closure
# Phase 3.6.20 — Storage v3.2.10 精确版本 Bundle 清单：H 39 项 C-P0 闭环

- Owner perspective: Storage / COC Durable Log and Recovery
- Date: 2026-11-17
- Status: **H 1.2.14 / C 1.0.1 EXACT SOURCE + 39-TEST CI BOUND; C/H/I/D ROLE REVIEWS RECORDED; FRESH A REVIEW REQUIRED; NOT JOINTLY ACCEPTED / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- Predecessor bundle: Storage v3.2.9, Blob `bf323a1682f2bfadc3ff41ea4f86883d678a77e3`
- Normative Storage technical body: Storage v3.2.3, Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`
- COC companion §§14–17: Blob `5b950a3a29bd7a5276b92a49a9114d700718b987`
- Provenance: delegated Storage-role coordination artifact; **not an independent human Storage Owner signature**.
- English and Chinese are normative peers.

## 1. Scope and supersession / 范围与替代关系

This manifest supersedes the H source/test/fixture/CI and C/I/D review pins in Storage v3.2.9. It does not rewrite Storage v3.2.3 S0a–S4, change the COC Batch-before-Manifest order, or silently upgrade any production gate. Storage v3.2.3 remains the normative technical body; v3.2.9 remains the historical predecessor.

本清单替代 Storage v3.2.9 中 H Source/Test/Fixture/CI 与 C/I/D 复审绑定。不改写 Storage v3.2.3 S0a–S4，不改变 COC Batch-before-Manifest 顺序，也不静默提升任何生产 Gate。Storage v3.2.3 仍为规范技术正文；v3.2.9 为历史前序。

A changed Blob invalidates the review that pins it. Paths and branch names alone are not version bindings. This manifest corrects the predecessor's stale H test-source/CI association: run 44069777296 tested commit 9eb06313... and executed 27 tests; it did not test the later 32-method source. H Phase 3.8.15 subsequently bound the 38-method source to run 44070924346. This v3.2.10 binds the successor 39-method source to run 44071354162.

Blob 变化会使绑定该 Blob 的复审失效。路径和分支名本身不是版本绑定。此清单纠正前序 H Test Source/CI 关联错误：Run 44069777296 测试 Commit 9eb06313...，实际执行 27 项，并未测试后续 32-method 源码。H Phase 3.8.15 随后将 38-method 源码绑定到 Run 44070924346。本 v3.2.10 将后继 39-method 源码绑定到 Run 44071354162。

## 2. Unchanged Storage / COC normative base / 不变的 Storage / COC 规范基线

| Authority | Artifact | Exact Blob | Binding |
|---|---|---|---|
| Storage | Durable log/recovery protocol v3.2.3 | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Normative S0a–S4, RecoveryBatch, participant union, JF-10 bridge and same-GID recovery |
| COC | COC durable log/recovery companion §§14–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | PreparedParticipant identity, dual-ledger union, record order, digest chain and recovery joins |
| Storage | Batch-before-Manifest amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` | Batch committed before distinct Manifest with exact backlink |
| Storage | R1/R2 successor-round/release ordering addendum | `0477f0329997e42a1cbf6ecb8127c5c01fa47051` | Immutable RecoveryRound and owner-local release order |
| Predecessor | Storage v3.2.9 manifest | `bf323a1682f2bfadc3ff41ea4f86883d678a77e3` | Historical H source/test and review pins |

The normative S0a–S4 order is unchanged:
1. I/D/C independently close their own gates and freeze request/admission/effect ledgers.
2. COC restores quorum and freezes exact committed prefix P.
3. Construct the complete canonical union of COC participants through P and applicable I/D/C owner-local admissions through independently frozen high-waters.
4. Commit immutable Recovery Cutoff Batch.
5. Commit distinct Participant Manifest strictly after Batch, with exact backlink.
6. Linearizably read back both records and verify prefix, roots, counts, member set, digests, quorum evidence and BatchPosition < ManifestPosition.
7. Only then reconcile participants; each Owner independently issues its own release.

S0a–S4 顺序不变：I/D/C 各自关闭 Gate 并冻结 Request/Admission/Effect Ledger；COC 恢复 Quorum 并冻结精确 Prefix P；构造完整 COC Participant 与 Owner-local Admission Union；先提交不可变 Recovery Cutoff Batch，再提交带精确回链的独立 Participant Manifest；线性读回并验证完整 Pair；之后才能开始 Participant Reconciliation，各 Owner 独立签发自己的 Release。

## 3. Exact current source bundle / 当前精确源集合

| Authority | Artifact | Exact Blob / Run | Meaning and evidence ceiling |
|---|---|---|---|
| H | Unified schema 1.2.14 / wire 1.3.0 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Exact current wire schema and D ForgetFenceGeneration high-water carrier |
| H | Authority-Join mapping Phase 3.8.10 | `1cbe74eba69325510d6b1019d971661f965eabf8` | C object/wire mapping plus separate I/D/Storage verifier seams |
| H | C/D/I crosswalk review Phase 3.8.12 | `90cdadd7d80676c1338965576c955a5f336ad0bc` | Generic RecoveryJoin P0 and owner-digest dereference mapping |
| H | RecoveryJoin 1.0.2 / RecoveryCutoff 1.0.5 | `4b664e3bce465499bcdfd93796349a4ba7074002` / `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` | Closed generic membership proof and exact cutoff structure |
| H | Validator core | `eab961a08d41e871f38543b18ee60cf024977414` | Fail-closed H 1.2.14 / C 1.0.1 validator |
| H | Validator test source | `c37c5e2621ebd7bae138f135c5066aa8be7f9926` | 33 H validator unit/full-path methods including C-P0 projection completeness |
| H | Full positive fixture | `f911027c848d21dd36fb87ba64a201a1455787a7` | Synthetic full H envelope + immutable C object; authority callbacks are test doubles |
| H | C crypto interop test sources | `5559fb7a612c8dd92345ceae3a6aa62f4faae41a` / `a49d588ea6f840927fe21ad8c41cd8089dceac29` | Six Python/Node candidate crypto interoperability methods |
| H | Exact-head CI closure Phase 3.8.16 | `f8aeae206b71f6a6bccd1c41300d40959a5221a8` | Exact source/run/test binding and evidence ceiling |
| H | Provider Outcome workflow | `4459d19f5b4eea058377d9819e48e81eed5c8c4b` | Python unittest discovery over all provider_outcome test_*.py files |
| H | Exact current CI | Run `44071354162`, commit `6dda3c8f82c2f25118d5bdcfe24015cec678895a`, job `133998097779` | **39 tests / success**; 33 H validator + 6 Python/Node C crypto methods |
| C | CSubmitOutcome schema 1.0.1 | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | Immutable C-owned provider outcome, signed sequence namespace |
| C | Sequence namespace amendment Phase 3.11.1 | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C outcome and CKeyStatusEvent share durable C namespace |
| C | RecoveryJoin P0 crosswalk | `df12af95e6859a389ba71eb1b7dba512b9feb8f6` | C row/digest indirection into generic RecoveryJoin P0 |
| C | Exact 39-test rereview Phase 3.8.20 | `9d03dcbcd632a54e2e5f42ab9ac1b92cac3b3b35` | Accepts C-P0 projection completeness regression as L1/L2 candidate |
| I | I P0 allowlist for H 1.2.14 | `44986f5f864bcdc1a79d34978273644d381a68c0` | Exact I common-envelope/proof-family P0 candidate |
| I | Exact 39-test rereview Phase 3.8.16 | `653841c9e7b4a48f7137118a1388a7634bdcd566` | Accepts local test boundary only; outer envelope auth and production I proof remain open |
| D | D RecoveryJoin P0 crosswalk | `c4adf827dd62d44c43b8e871dec4835581508adf` | D owner row/operation/scope/fence/barrier/lineage digest indirection |
| D | Exact 39-test rereview Phase 3.8.12 | `02b74a14c2c5ad35553b41eb7831b6eadceb0ffa` | Accepts local D callback boundary only; lineage and release remain open |
| Storage | This v3.2.10 manifest | Self-reference omitted | Exact bundle/review routing; not independent Storage Owner approval |
| A | Fresh exact integration review | **PENDING** | Must review this exact v3.2.10 manifest; earlier A review does not transfer |

## 4. Exact CI meaning and limitations / CI 精确含义与限制

Run `44071354162` completed successfully on exact commit `6dda3c8f82c2f25118d5bdcfe24015cec678895a`. Raw job log records `Ran 39 tests in 9.319s` and `OK`. The test-source Blob in this manifest is the exact source at that tested commit.

The 39 methods comprise 33 H validator unit/full-path methods and six Python/Node C crypto interoperability methods. Test 32 asserts that the C-P0 projection includes every CSubmitOutcome field except the explicitly derived/excluded `payload_digest` and `signature`, then recomputes and checks the candidate digest.

Run `44071354162` 在精确 Commit 上成功，Raw Job Log 记录 `Ran 39 tests in 9.319s` 和 `OK`。本清单 Test Source Blob 即该 Tested Commit 的精确文件。

39 项包括 33 个 H Validator Unit/Full-Path 方法与 6 个 Python/Node C Crypto Interop 方法。Test 32 断言 C-P0 Projection 包含所有 CSubmitOutcome 字段，仅排除明确派生/排除的 `payload_digest` 与 `signature`，随后重算并验证候选 Digest。

The positive fixture uses deterministic test doubles for all ten authority callbacks. The CI proves local schema loading, local C semantics, object/wire equality, C-P0 digest recomputation, 22 present duplicated-field mutations, namespace and owner-callback contradiction behavior, and fail-closed UNKNOWN/INVALID. It does not authenticate production C/I/D/Storage proofs, the outer H envelope, provider issuer truth, COC quorum, live same-GID Storage resolution or production anti-rollback.

正向 Fixture 的十个 Authority Callback 均为确定性 Test Double。CI 证明本地 Schema、C Semantic、Object/Wire 一致性、C-P0 Digest 重算、22 个重复字段变异、Namespace 与 Owner Callback 矛盾行为，以及 fail-closed UNKNOWN/INVALID。它不认证生产 C/I/D/Storage Proof、外层 H Envelope、Provider Issuer Truth、COC Quorum、实时 Same-GID Storage Resolution 或生产 Anti-Rollback。

## 5. Exact owner review matrix / Owner 精确复审矩阵

| Owner | Exact review Blob | Decision and scope | Remaining conditions |
|---|---|---|---|
| H | Phase 3.8.16 closure `f8aeae...` | Accepts exact 39-test local L1/L2 evidence | Human H adoption; production authority callbacks; outer-envelope authentication; L3 |
| C | Phase 3.8.20 `9d03dc...` | Accepts C-P0 projection/full-path local evidence | Production C trust, provider truth, same-key lookup, adapter race/fault and egress serialization |
| I | Phase 3.8.16 `653841...` | Accepts local test boundary only | Production I verifier, trust/key lifecycle, historical verification, anti-rollback, governance |
| D | Phase 3.8.12 `02b74a...` | Accepts local callback boundary only | Complete lineage, late-discovery, barrier terminality and final release CAS |
| Storage | This manifest | Binds exact Storage/H/C/I/D candidate bundle | Bidirectional COC joins, same-GID recovery, quorum durability and linearizable readback |
| A | No review yet | **PENDING** | Fresh exact-version A integration review required |

All H/C/I/D reviews are delegated role simulations and source-level architecture reviews, not independent human Owner signatures or formal organizational approvals. No role simulation is counted as independent approval or formal risk acceptance.

H/C/I/D 复审均为委托角色模拟与源级架构审查，不是独立人类 Owner 签署或正式组织批准。任何角色模拟均不得计为独立审批或正式风险接受。

## 6. Required semantic and operational joins / 必需语义与运行 Join

1. C `payload_digest` equals H `c_submit_outcome_digest`; C object digest, H envelope digest and provider evidence digest remain separate domains.
2. C `sequence_namespace_ref` equals authenticated CKeyStatusEvent namespace and durable C signing sequencer namespace.
3. I terminal authorization verifies the exact I-signed proof and applicable `COMMIT_WON`; generic terminality is insufficient.
4. D Forget clearance verifies exact FenceGeneration, complete affected lineage/barrier membership and final effect boundary.
5. Storage resolution verifies DB incarnation, GID, PrepareAttempt, participant ledger and same-GID terminal resolution/visibility.
6. Missing authority callback/evidence/currentness/anti-rollback is UNKNOWN; proven contradiction is INVALID.
7. Batch-before-Manifest, exact backlink, digest-domain separation, quorum and linearizable readback remain required.
8. Each Owner's release requires its own final currentness CAS and signed release; Storage/COC cannot release I/D/C gates.
9. Outer H envelope signature/integrity and authenticated transport principal must be verified by a separate H Gateway/Auth step before durable acceptance.
10. Any source Blob change invalidates the affected review and requires a new exact manifest/review.

## 7. Gate state and non-claims / Gate 状态与非声明

- Storage v3.2.3: normative architecture design body; implementation/deployment not claimed.
- Storage v3.2.10: **EXACT CANDIDATE BUNDLE BOUND; FRESH A REVIEW REQUIRED; NOT JOINTLY ACCEPTED / NOT FROZEN**.
- H local full-path schema/semantic/digest/P0 projection conformance: **39/39 exact CI PASS**.
- Production C/I profiles, trust roots, key custody and anti-rollback: **NOT APPROVED / OPEN**.
- Production C provider evidence/same-key lookup/adapter race/fault/egress: **OPEN**.
- Real I/D/Storage proof authentication and production authority adapters: **NOT IMPLEMENTED / NOT VERIFIED**.
- Complete owner-ledger pagination, D lineage/late-discovery and final release CAS: **OPEN**.
- Storage bidirectional RecoveryJoin, same-GID recovery, quorum durability and linearizable readback: **OPEN**.
- JF-10 P0: **OPEN**.
- R1 Recovery Cutoff Batch completeness: **OPEN**.
- R2 owner-local gate linearization/release: **OPEN**.
- Gate A Storage architecture: **PARTIAL PASS / OPEN**; remaining architecture/owner acceptance work is not waived by local CI.
- Gate B COC persistence implementation/deployment: **BLOCKED / NOT IMPLEMENTED**.
- Gate C distributed end-to-end fault injection: **DEFERRED TO ENGINEERING / NOT RUN**.
- Multi-PolicyDomain atomicity: **BLOCKED**.
- Production activation, provider egress, Provider exactly-once, Full Applied, Global Forget completion and physical Forget: **NOT AUTHORIZED / NOT PROVEN**.

本清单不声称独立人类 Owner 签署、生产 Trust Root/Key Custody、真实 C/D/I Sequencer CAS、生产 Membership Verifier、Provider 认证、通用 Exactly-once、分布式故障注入通过、物理 Forget/擦除、Global Forget Completion 或生产就绪。

## 8. Required next sequence / 后续执行顺序

1. A performs a fresh exact-version integration review of this v3.2.10 manifest and every pinned Blob.
2. H implements and separately validates outer-envelope signature/integrity and authenticated transport-principal binding; do not infer it from C object validation.
3. C/I complete production profile/trust/key-status/sequencer/anti-rollback contracts and provider-specific same-key/egress race evidence.
4. D completes executable lineage membership, late-discovery and final release-CAS evidence.
5. Storage proves bidirectional COC participant ↔ I/D/C owner admission joins, same-GID RecoveryJoin, quorum persistence and linearizable Batch/Manifest readback.
6. Only after independent owner-authoritative evidence closes may the project consider protocol freeze, Gate B/C completion or production activation.

## 9. Provenance / 来源说明

This manifest was authored in delegated Storage-role mode. Exact source Blobs and the H workflow run/job were read from GitHub. This is a version-binding and review-routing artifact, not an independent Storage Owner signature, runtime deployment result or production conformance statement.

本清单由协调会话模拟 Storage 角色编写。所有源 Blob 与 H Workflow Run/Job 均从 GitHub 读回。本文件仅是版本绑定与复审路由工件，不是独立 Storage Owner 签名、Runtime 部署结果或生产符合性声明。
