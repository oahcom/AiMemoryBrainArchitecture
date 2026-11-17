# Phase 3.8.16 — H Exact-Head C-P0 Projection Regression and CI Closure
# Phase 3.8.16 — H 精确 HEAD C-P0 Projection 回归与 CI 闭环

- Owner perspective: H — BMCP Protocol / Schema / Interoperability
- Status: **39/39 EXACT-HEAD TESTS PASS; LOCAL FULL-PATH L1/L2 EVIDENCE; AUTHORITY CALLBACKS TEST-ONLY; NOT PRODUCTION / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- H Unified 1.2.14 schema Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- CSubmitOutcome 1.0.1 schema Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- H validator core Blob: `eab961a08d41e871f38543b18ee60cf024977414`
- H validator test Blob: `c37c5e2621ebd7bae138f135c5066aa8be7f9926`
- H positive fixture Blob: `f911027c848d21dd36fb87ba64a201a1455787a7`
- H workflow Blob: `4459d19f5b4eea058377d9819e48e81eed5c8c4b`
- Exact H Provider Outcome CI run: `44071354162`
- Exact tested commit: `6dda3c8f82c2f25118d5bdcfe24015cec678895a`
- Exact job: `133998097779` (`provider-outcome`) — **completed / success**
- Test result: **39 tests, 0 failures**
- Predecessor expanded full-path closure: Phase 3.8.15, Blob `60e5eb98a07efcf87bc3f2be6fcf7fedb2196504`
- Provenance: delegated H-role test/evidence work and exact GitHub Actions readback; **not an independent human H Owner signature**.
- English and Chinese are normative peers.

## 1. Exact source and run binding / 精确源与运行绑定

This closure binds the exact H 1.2.14 / CSubmitOutcome 1.0.1 schemas, unchanged H validator core, expanded positive fixture, updated test source and the successful CI run on the same tested commit. The test-source Blob `c37c5e...` is the exact file at commit `6dda3c8...`; it supersedes H test Blob `540056d...` used by Phase 3.8.15.

本闭环精确绑定 H 1.2.14 / CSubmitOutcome 1.0.1 Schema、未变更的 H Validator Core、扩展正向 Fixture、更新后的测试源码，以及同一 Tested Commit 上成功的 CI。Test Source Blob `c37c5e...` 是 Commit `6dda3c8...` 的精确文件，替代 Phase 3.8.15 使用的 `540056d...`。

## 2. Added C-P0 projection regression / 新增 C-P0 Projection 回归测试

The new test `test_32_c_p0_projection_covers_every_member_except_derived_digest_and_signature` verifies:
1. `_p0(record)` contains every CSubmitOutcome member except the two derived/excluded members `payload_digest` and `signature`;
2. no other C object field is silently omitted from the P0 digest projection;
3. the independently recomputed candidate digest equals the fixture's declared `payload_digest`.

新增 Test 32 验证：
1. `_p0(record)` 包含 CSubmitOutcome 全部成员，仅排除派生/排除字段 `payload_digest` 与 `signature`；
2. 不允许其他 C Object 字段被静默排除在 P0 Digest Projection 外；
3. 独立重算的候选 Digest 必须等于 Fixture 声明的 `payload_digest`。

This is a test-only additive change. It does not change H/C schema, C-P0 definition, wire mapping, semantic predicates or owner-authority callback contracts.

该变更仅增加测试，不修改 H/C Schema、C-P0 定义、Wire Mapping、Semantic Predicate 或 Owner Authority Callback 合同。

## 3. Exact CI readback / 精确 CI 读回

GitHub Actions run `44071354162`:
- branch: `session-h-bmcp-protocol`;
- tested commit: `6dda3c8f82c2f25118d5bdcfe24015cec678895a`;
- workflow: H Provider Outcome Conformance;
- job `133998097779`: completed / success;
- raw job log summary: `Ran 39 tests in 9.319s`; `OK`.

The 39 methods comprise 33 H validator unit/full-path methods and six Python/Node C crypto-interoperability methods. This supersedes the predecessor 38-method run for the updated test source.

GitHub Actions Run `44071354162` 在精确 Commit `6dda3c8...` 上完成成功。Raw Job Log 明确记录 `Ran 39 tests in 9.319s` 与 `OK`。39 项由 33 个 H Validator Unit/Full-Path 方法和 6 个 Python/Node C Crypto Interop 方法构成，替代前序 38 项测试结果。

## 4. Evidence ceiling / 证据上限

**PROVEN at local L1/L2 source level:**
- H 1.2.14 and CSubmitOutcome 1.0.1 schema loading;
- full synthetic H envelope + immutable C object schema/semantic/digest path;
- 22 present duplicated wire-field mutation checks from Phase 3.8.15;
- C-P0 member mutation and C sequence namespace mismatch rejection;
- I COMMIT_WON, D exact fence and Storage same-GID/PrepareAttempt callback contradiction tests;
- exact C-P0 projection coverage excluding only payload_digest/signature;
- fail-closed UNKNOWN for unavailable I/D/Storage callbacks and INVALID for explicit contradiction.

**NOT PROVEN:**
- production C/I profile registration, trust roots, key custody, key-status ledger or anti-rollback;
- production C sequencer and provider evidence issuer truth/same-key lookup/provider adapter race/fault;
- real I terminal proof, D lineage/late-discovery/release CAS or Storage same-GID proof;
- outer H envelope signature/integrity and authenticated transport principal;
- live COC quorum, bidirectional RecoveryJoin, Storage linearizable readback or deployment;
- JF-10 completion, Global Forget, physical erasure or production activation.

**本地 L1/L2 已证明：** H/C Schema、合成完整路径、22 个重复 Wire 字段变异、C-P0 成员/Namespace 冲突、I/D/Storage Callback 矛盾、P0 Projection 全字段覆盖，以及 Callback 缺失 UNKNOWN / 矛盾 INVALID。

**仍未证明：** 生产 Profile/Trust/Key/Anti-Rollback、真实 Sequencer/Provider Truth、真实 I/D/Storage Proof、外层 H Envelope 认证、COC Quorum、双向 RecoveryJoin、Storage 线性读回、部署、JF-10 完成、Global Forget、物理擦除或生产激活。

## 5. H disposition / H 侧结论

**Delegated H-role disposition: ACCEPT the exact 39-test local L1/L2 evidence for the pinned H 1.2.14 / C 1.0.1 source set. Production authority, outer-envelope authentication, L3 completeness, COC/Storage durability and deployment remain OPEN. NOT FROZEN.**

This test-only addition does not transfer or create independent C/I/D Owner approval. It does not authorize Gate A/B/C transition, protocol freeze or production activation.

**角色模拟 H 侧结论：** 接受精确 H 1.2.14 / C 1.0.1 源集合的 39 项本地 L1/L2 证据。生产 Authority、外层 Envelope 认证、L3 Completeness、COC/Storage Durability 与部署仍 OPEN，不冻结。

该测试增补不转移或创造独立 C/I/D Owner 批准，也不授权 Gate A/B/C 迁移、协议冻结或生产激活。
