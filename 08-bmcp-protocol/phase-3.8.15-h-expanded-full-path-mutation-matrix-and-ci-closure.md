# Phase 3.8.15 — H Expanded Full-Path Mutation Matrix and Exact-Head CI Closure
# Phase 3.8.15 — H 扩展 Full-Path Mutation Matrix 与精确 HEAD CI 闭环

- Owner: H — BMCP Protocol / Schema / Interoperability
- Status: **EXPANDED LOCAL FULL-PATH CONFORMANCE PASS; ALL OWNER AUTHORITY CALLBACKS REMAIN TEST-ONLY; NOT PRODUCTION / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- H Unified schema 1.2.14 Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- CSubmitOutcome 1.0.1 schema Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- H authority-join mapping Blob: `1cbe74eba69325510d6b1019d971661f965eabf8`
- H validator core Blob: `eab961a08d41e871f38543b18ee60cf024977414`
- H expanded test source Blob: `540056d7c4f290c31290b17c264c69cfd76b1cb2`
- H full positive fixture Blob: `f911027c848d21dd36fb87ba64a201a1455787a7`
- C crypto interop test Blobs: `5559fb7a612c8dd92345ceae3a6aa62f4faae41a` and `a49d588ea6f840927fe21ad8c41cd8089dceac29`
- H workflow Blob: `4459d19f5b4eea058377d9819e48e81eed5c8c4b`
- Exact H Provider Outcome CI run: `44070924346`
- Exact tested commit: `77a9d5e2e716ba33387f0beb1195f864ed8ac54f`
- Exact job: `133996627914` (`provider-outcome`) — **completed / success**
- Test suite: **38 methods** (32 H validator unit/full-path methods + 3 legacy C crypto interop + 3 C 1.0.1 crypto interop).
- Predecessor H full-path closure Blob: `804bfd3214b015c80340575c1eb467d756ad0699`
- Provenance: delegated H-role source review and exact CI readback; **not an independent human H Owner signature**.
- English and Chinese are normative peers.

## 1. Exact source and fixture delta / 精确源文件与 Fixture 变化

The full positive fixture now includes explicit test-only references for:
- I terminal decision: `I/terminal/COMMIT_WON/operation-41`;
- D clearance: `D/clearance/forget-op-41/fence-19`;
- Storage resolution: `Storage/resolution/gid/pg-inc-7/gid-41`;
- Storage PreparedParticipant, PrepareAttempt/generation, participant ledger/version and tuple digest.

The H/C schemas and H validator core are unchanged. Only the fixture and H test source changed in this iteration.

完整正向 Fixture 新增仅用于测试的 I Terminal、D Clearance、Storage Resolution、PreparedParticipant、PrepareAttempt/Generation、Participant Ledger/Version 和 Tuple Digest 引用。H/C Schema 与 H Validator Core 未改变，本轮仅修改 Fixture 和 H Test Source。

## 2. Expanded negative matrix / 扩展负向矩阵

The exact test source adds:
- Test 26: mutate every present duplicated H wire field represented in `WIRE_TO_C`, one at a time, while retaining the immutable C object; each mutation must return INVALID. The fixture currently supplies 22 duplicated wire fields for this matrix.
- Test 27: mutate a C-P0 member and its duplicated H wire value together while preserving the old C payload digest; actual digest recomputation must return INVALID.
- Test 28: mutate C `sequence_namespace_ref`, recompute C-P0 digest and matching H C digest, then have the key-status verifier test double reject the namespace; result must be INVALID.
- Test 29: a test callback rejects an I `REVOCATION_WON` reference where provider invocation requires `COMMIT_WON`.
- Test 30: a test callback rejects a D clearance bound to another operation/FenceGeneration.
- Test 31: a test callback rejects a Storage resolution proof bound to another database incarnation/GID or mismatched PrepareAttempt/participant ledger.

精确测试新增：
- Test 26：逐一篡改 `WIRE_TO_C` 中 Fixture 实际存在的每个 H Wire 重复字段，保留不可变 C Object；每项必须 INVALID。当前 Fixture 为此矩阵提供 22 个重复字段。
- Test 27：同时篡改 C-P0 成员及对应 H Wire 字段，但保留旧 C Payload Digest；真实 Digest 重算必须 INVALID。
- Test 28：篡改 C `sequence_namespace_ref`，重算 C-P0 Digest 并同步 H C Digest，再由 Key Status Test Double 拒绝该 Namespace；结果必须 INVALID。
- Test 29：当 Provider Invocation 需要 `COMMIT_WON` 时，Test Callback 拒绝 I `REVOCATION_WON`。
- Test 30：Test Callback 拒绝绑定其他 Operation/FenceGeneration 的 D Clearance。
- Test 31：Test Callback 拒绝绑定其他 DB Incarnation/GID 或不匹配 PrepareAttempt/Participant Ledger 的 Storage Resolution Proof。

Tests 21–31 use real H/C JSON Schemas, the actual `validate_provider_outcome` implementation, actual C semantic predicates and actual C-P0 digest recomputation. No patching of schema validation, semantic validation or digest/preimage calculation occurs in these tests.

Tests 21–31 使用真实 H/C JSON Schema、真实 `validate_provider_outcome`、真实 C Semantic Predicate 和真实 C-P0 Digest 重算；没有 Patch Schema/Semantic/Digest/Preimage 函数。

## 3. Exact CI readback / 精确 CI 读回

GitHub Actions run `44070924346`:
- branch: `session-h-bmcp-protocol`;
- exact tested commit: `77a9d5e2e716ba33387f0beb1195f864ed8ac54f`;
- status/conclusion: `completed / success`;
- job `133996627914` (`provider-outcome`): `success`;
- successful steps include pinned Python dependencies, Node.js 22, pinned JCS oracle and the full H Provider Outcome unittest discovery.

GitHub Actions Run `44070924346` 在精确 Commit `77a9d5e...` 上完成成功，Job `133996627914` 成功。Workflow 完成固定 Python 依赖、Node.js 22、JCS Oracle 与 H Provider Outcome 全量 unittest discovery。

## 4. Evidence ceiling / 证据上限

**PROVEN at local L1/L2 source level:**
- exact H 1.2.14 / C 1.0.1 schema loading;
- complete synthetic H envelope + immutable C object schema validation;
- exact wire/object equality for all present duplicate fields;
- C semantic predicates and C-P0 digest recomputation;
- per-present-field wire mutation rejection;
- C-P0 member mutation rejection after synchronized wire mutation;
- fail-closed callback orchestration for I/D/Storage, including UNKNOWN for missing callback and INVALID for explicit contradiction.

**NOT PROVEN:**
- production C signature/key-status/sequencer authentication;
- real provider evidence issuer truth, authoritative same-key lookup, adapter race/fault behavior or exactly-once;
- real I terminal proof, I trust root, key custody, revocation history or external anti-rollback;
- real D clearance, complete lineage pagination, late-discovery recovery or final D release CAS;
- real Storage proof, database-incarnation continuity, same-GID recovery, COC quorum durability or linearizable Batch/Manifest readback;
- production H envelope signature/integrity verification and authenticated transport principal binding by the outer H gateway;
- production deployment, JF-10 completion, Global Forget or physical erasure.

**本地 L1/L2 源级已证明：** H/C Schema 加载、合成 H Envelope + C Object 完整 Schema 校验、所有现存重复字段的精确 Join、C Semantic Predicate、C-P0 Digest 重算、逐字段 Wire Mutation 拒绝、同步 Wire 修改后的 C-P0 成员篡改拒绝，以及 I/D/Storage Callback 缺失 UNKNOWN、矛盾 INVALID。

**仍未证明：** 生产 C Signature/Key Status/Sequencer；Provider Truth/Same-Key Lookup/Adapter Race/Exactly-once；真实 I Trust/Revocation/Anti-Rollback；真实 D Clearance/完整 Lineage/Late Discovery/Release CAS；真实 Storage Same-GID/COC Quorum/Linearizable Readback；外层 H Gateway 的 Envelope Signature/Integrity 与 Transport Principal Binding；生产部署、JF-10、Global Forget 或物理擦除。

The H Provider Outcome validator verifies the C object digest and the H/C wire mapping. This test suite does not claim to authenticate the outer H envelope's own `payload_digest`/`signature` or transport identity; that remains an explicit H gateway/authentication integration obligation under the envelope contract. Do not infer envelope authentication from C object signature validation.

H Provider Outcome Validator 校验 C Object Digest 与 H/C Wire Mapping。本测试套件不声称认证外层 H Envelope 自身的 `payload_digest`/`signature` 或 Transport Identity；该责任仍属于 H Gateway/Authentication 集成合同。不得从 C Object Signature 验证推导出 Envelope 已认证。

## 5. H disposition / H 侧结论

**Delegated H-role disposition: ACCEPT expanded local full-path and 22-field duplicate-mutation suite as stronger L1/L2 conformance evidence. All production authority callbacks, outer-envelope authentication, L3 completeness, COC/Storage durability and deployment gates remain OPEN. NOT FROZEN.**

This addendum supersedes H Phase 3.8.14's earlier 32-method/5-full-path-test evidence scope and H Phase 3.8.13's callback-seam-only CI status for the current source set. It does not replace C/I/D Owner truth or authorize a gate transition.

**角色模拟 H 侧结论：** 接受扩展本地 Full-Path 与 22 字段重复项篡改测试，作为更强的 L1/L2 符合性证据。生产 Authority Callback、外层 Envelope Authentication、L3 Completeness、COC/Storage Durability 和部署 Gate 仍 OPEN，不冻结。

本 Addendum 替代 H Phase 3.8.14 的旧 32 方法/5 个 Full-Path Test 证据范围，以及 H Phase 3.8.13 的仅 Callback-Seam CI 状态。不替代 C/I/D Owner 事实，也不授权 Gate 迁移。

## 6. Explicit non-claims / 明确不声明

No independent human H Owner signature, production profile registration, trust-root activation, KMS/HSM custody, live owner-authority adapters, provider exactly-once, COC quorum durability, Storage same-GID completion, JF-10 completion, Global Forget, physical erasure or production activation is claimed.
