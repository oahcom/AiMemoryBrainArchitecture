# Phase 3.8.17 — H Expanded C-P0 / Nullable Intent 42-Test Exact-Head Closure
# Phase 3.8.17 — H 扩展 C-P0 / Nullable Intent 42 项精确 HEAD 闭环

- Owner perspective: H — BMCP Protocol / Schema / Interoperability
- Status: **42/42 EXACT-HEAD TESTS PASS; EXPANDED LOCAL L1/L2 CONFORMANCE; AUTHORITY CALLBACKS TEST-ONLY; OUTER ENVELOPE AUTH OPEN; NOT PRODUCTION / NOT FROZEN**
- Exact H branch HEAD tested: c6faee294e503f32a802ba51f3f3b3eb4bee2cd7
- H Unified 1.2.14 schema Blob: 09fcd1fa29fe24255fbd87cae79dafb406594a59
- CSubmitOutcome 1.0.1 schema Blob: a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda
- H authority-join mapping Blob: 1cbe74eba69325510d6b1019d971661f965eabf8
- H validator core Blob: eab961a08d41e871f38543b18ee60cf024977414
- H validator test Blob: da1454ed985c84160c4cb6a0462df9d1225fab7f
- H positive full-path fixture Blob: f911027c848d21dd36fb87ba64a201a1455787a7
- H C crypto interop test Blobs: 5559fb7a612c8dd92345ceae3a6aa62f4faae41a and a49d588ea6f840927fe21ad8c41cd8089dceac29
- H Provider Outcome workflow Blob: 4459d19f5b4eea058377d9819e48e81eed5c8c4b
- Exact H Provider Outcome CI run: 44072037563
- Exact tested commit: c6faee294e503f32a802ba51f3f3b3eb4bee2cd7
- Exact job: 134000402978 (provider-outcome) — **completed / success**
- Test result: **42 tests, 0 failures** (36 H validator methods + 6 Python/Node C crypto interop methods)
- Provenance: delegated H-role source/CI review; not an independent human H Owner signature.
- English and Chinese are normative peers.

## 1. Exact source set / 精确源文件集合

This closure binds H Unified 1.2.14, CSubmitOutcome 1.0.1, the unchanged H validator core, current expanded test source, full synthetic H envelope/C object fixture and exact current-head CI. The 42 tests comprise 36 H validator methods and six Python/Node C crypto interoperability methods.

本闭环绑定 H Unified 1.2.14、CSubmitOutcome 1.0.1、未变化的 H Validator Core、当前扩展测试源码、完整合成 H Envelope/C Object Fixture 与精确当前 HEAD CI。42 项测试由 36 个 H Validator 方法与 6 个 Python/Node C Crypto Interoperability 方法组成。

## 2. New C-P0 and nullable COC intent cases / 新增 C-P0 与 Nullable COC Intent 用例

The suite retains the full local H/C schema, semantic and C-P0 digest path and the previous 22-field duplicate-wire mutation matrix. It adds:

- Test 32 (P0 projection): asserts _p0 contains every C object member except derived payload_digest and signature, then recomputes and checks the fixture digest.
- Test 32 (P0 member mutation): iterates every present C-P0 member (at least 60 fields), mutates it while synchronizing any duplicated H wire value, and requires INVALID.
- Test 33: NOT_INVOKED + PROVEN_NONE with null COC participant intent/reservation is VALID only when explicit COCAbsenceReason and the distinct no-handoff/not-invoked proofs are present.
- Test 34: absent COCAbsenceReason is not interchangeable with explicit null; missing required property is INVALID.

The two test methods with numeric prefix test_32_ have different full Python method names; both are present in unittest discovery and both appear in the exact CI log. No test method is overwritten.

本 Suite 保留完整本地 H/C Schema、Semantic、C-P0 Digest 路径与此前 22 字段重复 Wire 变异矩阵，并新增：

- Test 32（P0 Projection）：断言 _p0 包含除派生 payload_digest 与 signature 外的所有 C Object 成员，并重算校验 Fixture Digest。
- Test 32（P0 成员变异）：遍历所有现存 C-P0 成员（至少 60 个字段），逐一变异并同步任何 H 重复 Wire 值，要求 INVALID。
- Test 33：NOT_INVOKED + PROVEN_NONE 且 COC Participant Intent/Reservation 为 null 时，只有提供显式 COCAbsenceReason 及独立 No-Handoff/Not-Invoked Proof 才能 VALID。
- Test 34：COCAbsenceReason 字段缺失不能与显式 null 等同；缺少必需属性为 INVALID。

两个以 test_32_ 开头的测试方法完整 Python 方法名不同；二者均被 unittest discovery 发现并出现在精确 CI Log 中，没有测试方法被覆盖。

## 3. Exact CI evidence / 精确 CI 证据

GitHub Actions run 44072037563 ran on exact commit c6faee294e503f32a802ba51f3f3b3eb4bee2cd7. Job 134000402978 (provider-outcome) completed successfully. Raw job log explicitly records Tests 21–34 and concludes: Ran 42 tests in 26.444s; OK.

GitHub Actions Run 44072037563 在精确 Commit c6faee294e503f32a802ba51f3f3b3eb4bee2cd7 上执行。Job 134000402978（provider-outcome）成功完成。Raw Job Log 明确记录 Test 21–34 执行，并显示 Ran 42 tests in 26.444s; OK。

## 4. Evidence ceiling / 证据上限

**PROVEN at bounded local L1/L2 source level:**
- actual H/C schema loading and complete synthetic envelope/object schema validation;
- exact equality and mutation rejection for all 22 duplicated wire fields present in the fixture;
- local C semantic predicates and C-P0 digest/preimage recomputation;
- C-P0 projection includes all present object fields except payload_digest/signature;
- mutation rejection across every present C-P0 field;
- C sequence namespace mismatch rejection;
- I COMMIT_WON, D exact operation/Fence, Storage DB-incarnation/GID/PrepareAttempt/participant-ledger callback contradiction tests;
- explicit nullable COC participant-intent/absence-reason semantics and NOT_INVOKED proof requirements;
- fail-closed UNKNOWN for unavailable authority callbacks and INVALID for explicit contradictions;
- candidate Python/Node JCS/Ed25519 interoperability vectors.

**NOT PROVEN:**
- production C/I profile registration, trust roots, key custody, key-status ledger, live sequencers or anti-rollback;
- production provider issuer truth, authoritative same-key lookup, adapter send-vs-close, lost-ACK/retry/failover or exactly-once;
- real I terminal proof, I ledger completeness, revocation history or final I currentness CAS;
- real D clearance, complete lineage pagination, late-discovery recovery, barrier terminality or final D release CAS;
- real Storage resolution proof, DB incarnation continuity, same-GID recovery/visibility, COC quorum durability or linearizable Batch/Manifest readback;
- outer H envelope payload_digest/signature authentication and authenticated transport principal binding;
- production deployment, JF-10 completion, Global Forget or physical erasure.

**有限本地 L1/L2 已证明：** 真实 H/C Schema 加载与完整合成 Envelope/Object 校验；Fixture 中 22 个重复 Wire 字段等值与变异拒绝；本地 C Semantic Predicate 和 C-P0 Digest/Preimage 重算；P0 Projection 完整覆盖；所有现存 C-P0 字段变异拒绝；C Namespace 不一致拒绝；I COMMIT_WON、D Operation/Fence、Storage DB/GID/PrepareAttempt/Participant Ledger Callback 矛盾测试；Nullable COC Intent/AbsenceReason 与 NOT_INVOKED Proof 语义；Authority Callback 缺失 UNKNOWN、矛盾 INVALID；候选 Python/Node JCS/Ed25519 Interop。

**仍未证明：** 生产 Profile/Trust/Key/Key Status/Sequencer/Anti-Rollback；Provider Truth/Same-Key Lookup/Send-vs-Close/Retry/Exactly-once；真实 I Proof/Ledger/Revocation/Currentness CAS；真实 D Clearance/完整 Lineage/Late Discovery/Barrier/Release CAS；真实 Storage Proof/DB Incarnation/Same-GID/COC Quorum/Linearizable Readback；外层 H Envelope 认证；生产部署、JF-10、Global Forget 或物理擦除。

The H Provider Outcome validator verifies the C object digest and H/C wire mapping. It does not authenticate the outer H envelope's own payload_digest/signature or transport identity. This remains a separate H gateway/authentication integration obligation.

H Provider Outcome Validator 校验 C Object Digest 与 H/C Wire Mapping，但不认证外层 H Envelope 自身的 payload_digest/signature 或 Transport Identity。这仍是独立 H Gateway/Authentication 集成责任。

## 5. H disposition / H 侧结论

**Delegated H-role disposition: ACCEPT the exact 42-test local L1/L2 evidence for the pinned H 1.2.14 / C 1.0.1 source set. Production authority, outer-envelope authentication, L3 completeness, COC/Storage durability and deployment remain OPEN. NOT FROZEN.**

This supersedes the earlier 39-test closure for the updated test source. It does not transfer or create independent C/D/I Owner approval and does not authorize any Gate transition.

**角色模拟 H 侧结论：** 接受精确 H 1.2.14 / C 1.0.1 源集合的 42 项本地 L1/L2 证据。生产 Authority、外层 Envelope 认证、L3 Completeness、COC/Storage Durability 与部署仍 OPEN，不冻结。

本文件替代此前针对旧 Test Source 的 39 项闭环，不转移或创造独立 C/D/I Owner 批准，也不授权任何 Gate 迁移。

---
**Provenance:** delegated H-role source/CI review in the coordinating session; not an independent human H Owner signature.
