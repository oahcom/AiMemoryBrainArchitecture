# Phase 3.8.10 — H Unified 1.2.14 / CSubmitOutcome 1.0.1 Authority-Join Mapping
# Phase 3.8.10 — H Unified 1.2.14 / CSubmitOutcome 1.0.1 权威 Join 映射

- Owner perspective: H — BMCP Protocol / Schema and Interoperability
- Project phase: ARCHITECTURE DESIGN
- Disposition: **CANDIDATE MAPPING WITH EXPLICIT TEST-ONLY AUTHORITY SEAMS / NOT FROZEN**
- Wire family: `bmcp.coc-jf10-unified`, wire version `1.3.0`, artifact revision `1.2.14`
- H Unified schema Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- CSubmitOutcome schema 1.0.1 Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- C sequence namespace amendment Blob: `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb`
- I review of C 1.0.1 namespace Blob: `0d78e5b2bfcf66cae6b757314cead84b9c942601`
- H validator Blob: `eab961a08d41e871f38543b18ee60cf024977414`
- H validator test Blob: `70a3796446553464e71999f916b76bc22e47da11`
- H conformance workflow Blob: `4459d19f5b4eea058377d9819e48e81eed5c8c4b`
- C candidate CI: `44059935858`, SUCCESS, 19 tests (C source construction only; not production trust).
- H exact callback-seam CI: `44068869146`, SUCCESS, 27 tests, tested commit `e0d89f1b6dac3bdcf1f0ab4e3f062dd7bc53fdf8`.
- Provenance: delegated H-role work performed at the user's direction; **not an independent human H Owner signature**.

## 1. Version authority and supersession

This mapping binds the exact H Unified 1.2.14 schema and CSubmitOutcome 1.0.1 object schema. H 1.2.12/1.2.13 mappings are historical and must not be used as current pins for this bundle. The exact schema artifact revision is 1.2.14; the wire-family version remains 1.3.0. A loaded schema URI/version check is necessary but does not itself pin immutable content. The deployment schema loader must verify the expected Blob/content digest from an approved release manifest.

本映射绑定 H Unified 1.2.14 与 CSubmitOutcome 1.0.1 的精确 Schema。H 1.2.12/1.2.13 映射仅为历史版本，不得作为本 Bundle 的当前绑定。Schema 工件修订为 1.2.14，Wire 协议族版本仍为 1.3.0。加载 URI/版本检查并不等于不可变内容绑定；部署 Schema Loader 仍必须验证批准发布清单中的 Blob/内容摘要。

## 2. Immutable C object and wire equality

CSubmitOutcome 1.0.1 remains the sole immutable semantic source for C-owned provider submission facts. H validates the full C object against the exact C schema, dereferences `c_submit_outcome_ref`, checks `c_submit_outcome_digest == payload_digest`, recomputes the C-P0 digest, and applies the exact field mapping implemented by `WIRE_TO_C` in the pinned H validator.

The duplicate equality map covers immutable identity/digest, outcome, provider and adapter identity, idempotency key, final request boundary, request digest, causal transaction, provider evidence/request/receipt/lookup/no-handoff/not-invoked/unknown references, actual inference request identity, C admission and owner-ledger identity/version/sequence/high-water/root, COC participant intent/reservation and absence reason. If a non-null C object member is represented on the wire, omission or inequality is INVALID. Null and absent are not interchangeable.

CSubmitOutcome 1.0.1 是 C 自有 Provider Submit 事实的唯一不可变语义来源。H 必须解引用 `c_submit_outcome_ref`，按精确 C Schema 校验完整对象，检查 `c_submit_outcome_digest == payload_digest`，重新计算 C-P0 摘要，并执行当前 H Validator 的 `WIRE_TO_C` 精确字段映射。

字段重复映射覆盖不可变身份/摘要、Outcome、Provider/Adapter 身份、幂等键、最终请求边界、请求摘要、因果事务、Provider 证据/请求/Receipt/Lookup/No-Handoff/Not-Invoked/Unknown 引用、实际推理请求身份、C Admission 与 Owner Ledger 身份/版本/序列/High-Water/Root、COC Participant Intent/Reservation 和 Absence Reason。C 对象中非空且应由 Wire 表示的字段不得遗漏或不一致；Null 与 Absent 不可互换。

## 3. Distinct authority domains — no callback substitution

The validator now exposes three additional, independent authority callbacks. They are separate from the COC join callback and from one another:

| Authority seam | Callback | Required proof responsibility |
|---|---|---|
| I Security/Governance | `verify_i_terminal_decision(envelope, c_object)` | Resolve the exact I terminal decision; verify issuer, digest, XID/request/PolicyDomain scope, monotonic terminal state and currentness. For any provider invocation authorization, prove the required I `COMMIT_WON` result; a different terminal result must not be treated as permission. |
| D Memory Brain / Forget | `verify_d_clearance(envelope, c_object)` | Resolve the exact D clearance and Forget fence generation; verify affected lineage/barrier membership, scope, generation and that no fence/late-work condition blocks the effect. |
| Storage | `verify_storage_resolution_proof(envelope, c_object)` | Resolve the exact Storage proof; verify DB incarnation, GID/transaction identity, prepare attempt and participant ledger, authoritative same-GID terminal resolution and visibility boundary. |

A callback returns `True` only when its own authority has authenticated the exact evidence and established either (a) the required proof and join, or (b) authoritative non-applicability for this exact operation. `False` means a proven contradiction and yields INVALID. `None`, an exception, missing callback, unavailable source or unverifiable reference yields UNKNOWN. A COC callback cannot stand in for I, D or Storage.

Validator 新增三个独立权威回调，彼此独立，也不能由 COC Join 回调替代：

- I 回调验证精确 I Terminal Decision、签发者、摘要、XID/请求/PolicyDomain 范围、单调终态与当前性。凡涉及 Provider Invocation 授权，必须证明要求的 I `COMMIT_WON`；其他终态不得被当作许可。
- D 回调验证精确 D Clearance 与 Forget Fence Generation、受影响 Lineage/Barrier 成员、范围和代次，确认 Fence 或迟到工作条件未阻止效果。
- Storage 回调验证精确 Storage Proof、DB Incarnation、GID/事务身份、Prepare Attempt、Participant Ledger、权威 Same-GID 终态解析及可见性边界。

只有对应权威已认证精确证据并证明必要条件（或该操作确实不适用）时才可返回 `True`。确定矛盾返回 `False` 并导致 INVALID；`None`、异常、回调缺失、来源不可用或引用无法验证均导致 UNKNOWN。COC 回调不能代替 I、D 或 Storage。

## 4. Test evidence and its ceiling

The new tests exercise the actual `validate_provider_outcome` orchestration function with schema, semantic and digest primitives patched to deterministic test doubles. They prove that the I, D and Storage callbacks are distinct required seams, that all three can participate in a VALID orchestration result when test doubles return True, and that omitting all three produces UNKNOWN rather than VALID.

**They do not constitute an end-to-end valid H envelope + C object fixture test.** Schema validation, semantic predicates, canonicalization/digest recomputation, signature verification and the owner evidence contents are not jointly exercised by these orchestration tests. The test doubles are not production trust authorities. Exact H Provider Outcome CI run `44068869146` completed successfully on commit `e0d89f1b6dac3bdcf1f0ab4e3f062dd7bc53fdf8`: 27 tests passed, 0 failed. The tested validator and test Blobs are exactly `eab961a08d41e871f38543b18ee60cf024977414` and `70a3796446553464e71999f916b76bc22e47da11`. The exact run includes the I/D/Storage callback-seam tests and current C sequence namespace tests. This is bounded CI evidence for the new callback orchestration, not end-to-end proof validation.

新增测试通过确定性 Test Double 调用真实的 `validate_provider_outcome` 编排函数，但对 Schema、语义与摘要基础函数进行了 Mock。它们证明 I、D、Storage 是三个独立必需接口；当三个 Test Double 均返回 True 时可以参与 VALID 编排；缺少三者时结果为 UNKNOWN，而不是 VALID。

**这些测试并不是完整有效 H Envelope + C Object Fixture 的端到端测试。** 它们没有联合执行 Schema 校验、语义谓词、规范化/摘要重算、签名验证和 Owner 证据内容验证。Test Double 不是生产信任权威。必须先在精确 HEAD 上运行 CI，才能声称新增回调获得了有限 CI 证据。

## 5. Remaining blockers

1. Build a complete positive H envelope + CSubmitOutcome 1.0.1 fixture and pass it through the unmocked full validator.
2. Add negative full-path mutations for each duplicated wire field, C-P0 digest, C sequence namespace, I terminal decision, D Fence/Clearance, Storage same-GID resolution and stale/currentness evidence.
3. Bind authenticated verifier implementations to I/D/Storage owner-authoritative ledgers, key registries and durable currentness sources. The current callbacks are interfaces only.
4. Obtain fresh exact-Blob C, I, D and H Owner decisions for the 1.2.14/1.0.1 bundle. Existing 1.2.13 or earlier decisions do not transfer.
5. Keep C/I profiles NOT REGISTERED unless I completes separate trust-root, key-custody, lifecycle and anti-rollback approval.
6. Do not infer provider idempotency, COC quorum durability, deployed Storage recovery or production runtime conformance from these documents/tests.

## 6. Gate boundary

This is an architecture candidate mapping and bounded local test seam only. It does not close R1/R2, JF-10 P0, Gate A, Gate B, Gate C or Multi-PolicyDomain atomicity. Production activation, production provider egress, Full Applied and Global Forget Completion remain NOT AUTHORIZED.


## 7. Current 27-test evidence / 当前 27 项测试证据

The latest exact H Provider Outcome Conformance run is `44068869146`, tested commit `e0d89f1b6dac3bdcf1f0ab4e3f062dd7bc53fdf8`, job `133989610753`, SUCCESS. It reports **27 tests passed, 0 failed**. The test source Blob is `70a3796446553464e71999f916b76bc22e47da11`; the validator core remains Blob `eab961a08d41e871f38543b18ee60cf024977414`; H schema remains Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`.

The 27-test suite includes: strict canonical JSON/digest checks; CSubmitOutcome 1.0.1 and C sequence namespace; H 1.2.14 schema pin and D ForgetFenceGeneration high-water; I/D/Storage verifier callback separation; full validator orchestration requiring all three authority seams; missing I/D/Storage evidence returning UNKNOWN rather than VALID; and rejection of wrong loaded schema URIs. Callback orchestration uses deterministic test doubles for underlying authority proofs. It is not an end-to-end real owner-ledger, trust-root, D fence, Storage same-GID or production proof campaign.

**中文：** 最新 H Provider Outcome Conformance Run `44068869146`，精确 Commit `e0d89f1b6dac3bdcf1f0ab4e3f062dd7bc53fdf8`，Job `133989610753`，SUCCESS，**27 项通过、0 失败**。精确测试 Blob `70a3796446553464e71999f916b76bc22e47da11`，Validator Blob `eab961a08d41e871f38543b18ee60cf024977414`，H Schema Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`。覆盖规范 JSON/Digest、C 1.0.1 与 Sequence Namespace、H 1.2.14/D Fence High-Water、I/D/Storage 三个独立回调、完整编排要求三个权威接口、缺失证据返回 UNKNOWN、错误 Schema URI 拒绝。回调底层使用确定性 Test Double；不等于真实 Owner Ledger、Trust Root、D Fence、Storage Same-GID 或生产证明。
