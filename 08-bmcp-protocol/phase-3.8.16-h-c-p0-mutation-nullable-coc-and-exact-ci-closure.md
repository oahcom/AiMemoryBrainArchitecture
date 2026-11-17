# Phase 3.8.16 — H C-P0 Field Mutation, Nullable COC Branch and Exact-Head CI Closure
# Phase 3.8.16 — H C-P0 字段篡改、Nullable COC 分支与精确 HEAD CI 闭环

- Owner: H — BMCP Protocol / Schema / Interoperability
- Status: **64-FIELD LOCAL C-P0 NEGATIVE MATRIX + NULLABLE COC POSITIVE/NEGATIVE PATH PASSED; AUTHORITY CALLBACKS TEST-ONLY; OUTER ENVELOPE AUTH OPEN; NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- H Unified 1.2.14 schema Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- CSubmitOutcome 1.0.1 schema Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- H authority-join mapping Blob: `1cbe74eba69325510d6b1019d971661f965eabf8`
- H validator core Blob: `eab961a08d41e871f38543b18ee60cf024977414`
- H test source Blob: `da1454ed985c84160c4cb6a0462df9d1225fab7f`
- H full positive fixture Blob: `f911027c848d21dd36fb87ba64a201a1455787a7`
- C crypto interop test Blobs: `5559fb7a612c8dd92345ceae3a6aa62f4faae41a` and `a49d588ea6f840927fe21ad8c41cd8089dceac29`
- H workflow Blob: `4459d19f5b4eea058377d9819e48e81eed5c8c4b`
- Exact H Provider Outcome CI run: `44072037563`
- Exact tested commit: `c6faee294e503f32a802ba51f3f3b3eb4bee2cd7`
- Exact job: `134000402978` (`provider-outcome`) — **completed / success**
- Test suite: **42 methods** (36 H validator unit/full-path methods + 6 C crypto interoperability methods).
- Predecessor expanded matrix closure Blob: `60e5eb98a07efcf87bc3f2be6fcf7fedb2196504`
- Provenance: delegated H-role source review and exact CI readback; **not an independent human H Owner signature**.
- English and Chinese are normative peers.

## 1. Exact source set / 精确源文件集合

The H/C schemas, H authority-join mapping and H validator core are unchanged from the previous full-path closure. The test source now binds all 64 present C-P0 members in the synthetic CSubmitOutcome object, excluding only the derived `payload_digest` and `signature` fields. The full fixture includes explicit C, I, D, Storage and COC references.

H/C Schema、H Authority-Join Mapping 和 H Validator Core 与上一 Full-Path Closure 相同。本轮测试源对合成 CSubmitOutcome 对象中全部 64 个现存 C-P0 成员建立逐字段篡改测试，仅排除派生 `payload_digest` 与 `signature`。完整 Fixture 包含显式 C/I/D/Storage/COC 引用。

## 2. New test obligations / 新增测试义务

- Test 32 mutates every one of the 64 present C-P0 fields individually. Where a field is duplicated on the H wire, the wire copy is mutated in lockstep so the test does not pass merely because of a simple wire/object mismatch. Every mutation must still be rejected by schema, semantic, identity or digest validation.
- Test 33 exercises a valid `NOT_INVOKED + PROVEN_NONE` case with no COC participant intent/reservation and an explicit `COCAbsenceReason`. It removes ProviderReceiptRef, adds ProviderNoHandoffProofRef and NotInvokedProofRef, recomputes C-P0 digest and requires the full validator to return VALID when authority test doubles return True.
- Test 34 removes the required C `COCAbsenceReason` member and requires INVALID, proving absent is not equivalent to explicit null/value.

- Test 32：逐一篡改全部 64 个现存 C-P0 字段。若字段在 H Wire 上有重复副本，则同步篡改 Wire 值，避免测试仅因简单 Wire/Object 不一致而通过。每项修改仍必须被 Schema、Semantic、Identity 或 Digest 校验拒绝。
- Test 33：验证有效的 `NOT_INVOKED + PROVEN_NONE` 无 COC Participant Intent/Reservation 分支，并提供明确 `COCAbsenceReason`。移除 ProviderReceiptRef，增加 ProviderNoHandoffProofRef 和 NotInvokedProofRef，重算 C-P0 Digest；当 Authority Test Double 返回 True 时，完整 Validator 必须返回 VALID。
- Test 34：移除必需的 C `COCAbsenceReason` 成员并要求 INVALID，证明 Absent 不等同于显式 Null/Value。

Tests 21–34 use real H/C schemas, the actual `validate_provider_outcome` implementation, actual C semantic predicates and actual C-P0 digest/preimage calculation. No patching of schema validation, semantic validation or digest calculation occurs in these full-path cases.

Tests 21–34 使用真实 H/C Schema、真实 `validate_provider_outcome`、真实 C Semantic Predicate 和真实 C-P0 Digest/Preimage 计算；这些 Full-Path 用例没有 Patch Schema/Semantic/Digest 函数。

## 3. Exact CI readback / 精确 CI 读回

GitHub Actions run `44072037563`:
- branch: `session-h-bmcp-protocol`;
- exact tested commit: `c6faee294e503f32a802ba51f3f3b3eb4bee2cd7`;
- status/conclusion: `completed / success`;
- job `134000402978` (`provider-outcome`): `success`;
- 42 test methods discovered across three Python files: 36 H validator unit/full-path methods and 6 C crypto interoperability methods.

GitHub Actions Run `44072037563` 在精确 Commit `c6faee...` 上完成成功，Job `134000402978` 成功。三个 Python 文件共发现 42 个测试方法：36 个 H Validator Unit/Full-Path 方法与 6 个 C Crypto Interop 方法。

## 4. Evidence ceiling / 证据上限

**PROVEN locally:** H/C schema validation; complete synthetic H envelope + immutable C object path; exact duplicate-field equality; all 64 present C-P0 member mutation rejection; C-P0 digest recomputation; valid nullable COC no-intent NOT_INVOKED branch; absent COC absence-reason rejection; selected C sequence/I COMMIT_WON/D fence/Storage GID callback contradiction behavior.

**NOT PROVEN:** real C signature/key status/sequencer; production Provider issuer truth and same-key lookup; real I/D/Storage proof authentication; complete owner-ledger pagination; external anti-rollback; provider adapter race/fault/Exactly-once; COC quorum; Storage same-GID recovery/visibility; production deployment.

**本地已证明：** H/C Schema、合成 H Envelope + C 不可变对象完整路径、重复字段精确一致、全部 64 个现存 C-P0 成员篡改拒绝、C-P0 Digest 重算、Nullable COC 无 Intent 的 NOT_INVOKED 正向分支、COC Absence Reason 缺失拒绝，以及选定 C Sequence/I COMMIT_WON/D Fence/Storage GID Callback 矛盾行为。

**仍未证明：** 真实 C Signature/Key Status/Sequencer、生产 Provider Issuer/Same-Key Lookup、真实 I/D/Storage Proof 认证、Owner Ledger 完整分页、External Anti-Rollback、Provider Adapter Race/Fault/Exactly-once、COC Quorum、Storage Same-GID Recovery/Visibility 与生产部署。

The Provider Outcome validator does not authenticate the outer H envelope's own `payload_digest`/`signature` or transport principal binding. The outer H gateway/authentication contract must verify these before durable acceptance. C object signature validation is not a substitute for envelope authentication.

Provider Outcome Validator 不认证外层 H Envelope 自身的 `payload_digest`/`signature` 或 Transport Principal Binding。外层 H Gateway/Authentication 合同必须在 Durable Acceptance 前完成验证。C Object Signature 校验不能替代 Envelope Authentication。

## 5. H disposition / H 侧结论

**Delegated H-role disposition: ACCEPT 64-field C-P0 mutation and nullable COC branch as expanded L1/L2 local conformance evidence. Production authority adapters, outer envelope authentication, L3 completeness, COC/Storage durability and deployment remain OPEN. NOT FROZEN.**

This addendum supersedes H Phase 3.8.15's 38-method/22-wire-field evidence scope and the prior Phase 3.8.14 full-path closure for the current H test source. It does not replace C/I/D Owner authority or authorize a gate transition.

**角色模拟 H 侧结论：** 接受 64 字段 C-P0 Mutation 与 Nullable COC 分支作为扩展 L1/L2 本地符合性证据。生产 Authority Adapter、外层 Envelope Authentication、L3 Completeness、COC/Storage Durability 和部署仍 OPEN，不冻结。

本 Addendum 替代 H Phase 3.8.15 的 38 方法/22 Wire 字段证据范围，以及此前 Phase 3.8.14 Full-Path Closure 对当前 H Test Source 的旧绑定。不替代 C/I/D Owner 权威，也不授权 Gate 迁移。

## 6. Explicit non-claims / 明确不声明

No independent human H Owner signature, production profile registration, trust-root activation, KMS/HSM custody, live owner-authority adapters, provider exactly-once, COC quorum durability, Storage same-GID completion, JF-10 completion, Global Forget, physical erasure or production activation is claimed.
