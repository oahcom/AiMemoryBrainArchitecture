# Phase 6 — B-02 H/C Gateway-Attestation and Integrated-Join Delta Review
# 第六阶段 — B-02 H/C Gateway-Attestation 与 Integrated-Join 差异复审

- Repository: oahcom/AiMemoryBrainArchitecture
- Review date: 2026-11-17
- Reviewer perspective: A / integration delta review; delegated analysis, not an independent human Owner signature
- Exact current main base: 901e38ba7b45ed1822eaefddc2da8d765cf8985c
- Branch: review/a-b02-h-c-gateway-join-delta-2026-11-17
- Status: **B-02 PARTIALLY ADVANCED; NOT CLOSED. C ACCEPTED THE CORRECTED ISSUANCE ORDER; H HAS A 1.2.15 RECEIVER-VALIDATOR REFERENCE IMPLEMENTATION AND TESTS; NO 1.2.15 INTEGRATED-MAPPING C ACCEPTANCE OR SAME-BUNDLE STORAGE MANIFEST IS EVIDENCED.**
- English and Chinese are normative peers.

---

## 1. Executive decision / 执行结论

The latest H/C artifacts materially advance gateway attestation:

1. H updated its P0 contract to require the gateway issuer to verify the immutable CSubmitOutcome object, C-P0 digest/signature, sequence namespace, provider evidence and C semantics before creating/signing the H attestation. The receiver independently repeats C verification, and replay reservation/durable ingress commit occurs only after all required owner/currentness checks.
2. C Phase 3.8.27 explicitly accepts this corrected issuance/receiver-validation/durable-acceptance order, while keeping production C key/trust/provider-adapter evidence OPEN.
3. H added a dedicated 1.2.15 Provider Outcome validator, an H gateway-attestation receiver validator, and a 21-case gateway validator test source.

B-02 does not close:
- H exact 1.2.15 mapping 2dc30f... is still the Provider Outcome/schema mapping, not a distinct 1.2.15 integrated authority-join mapping that explicitly supersedes or versions the 1.2.14 integrated mapping.
- C exact integrated-mapping acceptance is for H 1.2.14 / mapping 1cbe74..., not a 1.2.15 successor.
- The 1.2.15 H validator is explicitly a reference integration implementation with trust, signer, origin, key-status, integrity and durable-replay callbacks left as deployment seams. Its tests use callback doubles; the H signature test compares a fixed 86-character string and does not perform Ed25519 cryptographic verification.
- H normative contract requires pre-sign C verification, but the executable code read in this review is the receiver-side validator. No executable gateway issuance/signing pipeline proving C verification precedes H signing was identified in the reviewed H branch tree.
- H conformance workflow still describes H 1.2.14 and its explicit path filters do not name the new 1.2.15 schema or new validator modules. An exact-head successful 1.2.15 CI run was not identified in the evidence read for this review.
- Storage v3.3.0 still binds the H 1.2.14 bundle and prior integrated mapping, not the H 1.2.15 successor.

**Disposition: B-02 = PARTIAL / OPEN.** The corrected sequence is accepted at delegated C-role contract level; integrated 1.2.15 mapping, exact C review, validator/CI review and same-bundle manifest closure remain required.

中文结论：最新 H/C 工件确有实质进展。H 已将“C 对象验证必须先于 H Gateway Attestation 签发”写入规范；C Phase 3.8.27 明确接受修正后的签发/接收/持久化顺序；H 也增加了 1.2.15 Validator 与 21 项测试。但 B-02 仍未关闭：当前 H 1.2.15 Mapping 仍是 Provider Outcome/Schema Mapping，而不是独立版本化的 Integrated Authority-Join Mapping；C 对 Integrated Mapping 的精确接受仍绑定 1.2.14；新 Validator 的信任与签名验证仍依赖部署回调；未发现可证明 C 验证先于 H 签名的可执行 Gateway Issuance Pipeline；CI workflow 仍标注 1.2.14，且缺少本轮 1.2.15 精确 HEAD CI 证据；Storage v3.3.0 也未绑定 1.2.15。因此 B-02 只能判为 PARTIAL / OPEN。

---

## 2. Corrected prior evidence characterization / 对此前证据判断的纠正

Earlier Phase 4/5 wording said C had not reviewed the integrated authority-join mapping. That was too broad and is corrected here.

C Phase 3.8.17 exists and explicitly reviews exact H integrated mapping Blob 1cbe74eba69325510d6b1019d971661f965eabf8, H Unified 1.2.14, CSubmitOutcome 1.0.1, and the H validator/test pins. It accepts the C-owned semantic boundary and the separate I terminal, D Forget clearance and Storage resolution verifier seams as an L1/L2 candidate, subject to enumerated conditions and test-evidence ceilings.

C Phase 3.8.17 does not review H Unified 1.2.15. The correct distinction is:
- 1.2.14 integrated mapping: C review exists and accepts the scoped candidate.
- 1.2.15 Provider Outcome mapping/schema: C schema-shape review exists.
- 1.2.15 integrated authority-join successor: no exact C review was identified.

This correction does not retrospectively close B-02 for 1.2.15.

此前 Phase 4/5 将“C 尚未审查 Integrated Authority-Join Mapping”概括得过宽，本报告予以纠正。C Phase 3.8.17 确实精确审查过 H Integrated Mapping Blob 1cbe74...（H 1.2.14），并接受 C 自有语义边界以及独立 I/D/Storage 验证接口作为 L1/L2 候选，附带明确条件和测试证据上限。该审查不覆盖 H 1.2.15。故正确区分是：1.2.14 Integrated Mapping 已有 C 候选接受；1.2.15 Schema/Provider Outcome Mapping 已有 C Schema Shape 审查；1.2.15 Integrated Mapping 后继仍未见 C 精确审查。

---

## 3. Exact evidence readback / 精确证据读回

| Artifact | Exact SHA / Blob | Scope |
|---|---|---|
| Current main | 901e38ba7b45ed1822eaefddc2da8d765cf8985c | Fresh A review base |
| H branch HEAD | e3e4cab0aab2c68f9db98bd50bc387b1895c3773 | Latest H commit read |
| C branch HEAD | 71047cdb51139ca4080ac67f451e38a48698859d | Latest C commit read |
| H 1.2.15 schema | 860fc4cec658db7d2703cd6adf72aa31a2723f6d | Immutable schema candidate |
| H 1.2.15 Provider Outcome mapping | 2dc30f193d9c4f4bdc05ca4c137103687db28924 | Not the integrated successor |
| H 1.2.15 P0 contract, corrected | 93b83ac35114d20d64579d919c0699886940f0fa | Normative pre-sign C verification order |
| C Phase 3.8.26 schema review file Blob | c5ff68814be49ec5e6e2c081004e7fa058d276fa | 1.2.15 schema-shape review |
| C Phase 3.8.27 ordering review file Blob | 3ca06dbfd7d59483e9604b7a68df924c719f60aa | Accepts corrected order |
| C Phase 3.8.17 integrated mapping review | 36e5b97c55ebc5c01cf1b071957777225f448e64 | Exact C acceptance for 1.2.14 mapping |
| C Phase 3.8.17 validator/CI review | 36a50e6285bef512790583841e77349190076564 | Exact C review for 1.2.14 validator/CI |
| H 1.2.15 gateway validator | 9cc426d4c26deb452f39daff34c1008dd535e969 | Receiver-side reference validator |
| H 1.2.15 Provider Outcome validator | 90a2d4b6f5b05590e3e0a7daecb5a01d9bf525c0 | Semantic validator and owner callback seams |
| H 1.2.15 gateway validator tests | 9a5051b001a6e59d7b71e6dd175e84bb7d01d252 | 21 tests in source |
| H conformance workflow | 4459d19f5b4eea058377d9819e48e81eed5c8c4b | Still labeled 1.2.14; path filters stale |
| Prior integrated H mapping | 1cbe74eba69325510d6b1019d971661f965eabf8 | H Unified 1.2.14 |
| Storage v3.3.0 manifest | c8407c9f10049d65426a3598ad20b6aa70f83c32 | Prior H 1.2.14 bundle |

Relevant H commits read:
- 598278eaab7cf7fc75a806fdb4a10222ef63d60d: updates P0 contract to require C verification before H signing and moves durable ingress after owner/currentness checks.
- 44724bc2f4fce5ca4bdd6cab6b1c9ed63301c204: adds receiver-side H gateway validator reference.
- 719882510acd374ca650cfd57eef0120566cf9b4: adds canonicalization-profile and Ed25519 signature-shape checks.
- e3e4cab0aab2c68f9db98bd50bc387b1895c3773: adjusts test signature fixture and adds profile/encoding negative tests.

Relevant C commit read:
- 71047cdb51139ca4080ac67f451e38a48698859d: adds Phase 3.8.27 exact re-review.

---

## 4. What the new C review accepts / C 新审查实际接受范围

C Phase 3.8.27 accepts the corrected ordering:
1. H authenticates the original C adapter and captures exact raw ingress bytes/context.
2. H verifies immutable CSubmitOutcome schema, C-P0 digest/signature, C sequence namespace, provider evidence and C semantics.
3. Only then may H create/sign its distinct gateway-attestation P0.
4. Receiver independently validates H attestation and C object.
5. Replay reservation and durable ingress acceptance occur only after both authentication domains and required owner/currentness checks pass.

C also requires:
- C object contradiction → INVALID; unavailable C verifier/key status → UNKNOWN; H must not sign.
- C outcome UNKNOWN/IN_DOUBT or unresolved side-effect status remains nonterminal; an audit receipt cannot upgrade it to VALID.
- H signature valid with invalid/unavailable C signature cannot produce semantically valid durable acceptance.
- C signature valid with invalid/unavailable H attestation cannot produce authenticated H ingress acceptance.
- Ambiguous replay reservation/durable commit → UNKNOWN and recovery of the same immutable message/reservation.

The review is delegated C-role output, not an independent human C Owner signature. It does not accept H production keys/trust/provider adapter evidence and does not freeze the schema.

---

## 5. Executable evidence and limits / 可执行证据及其上限

### 5.1 H 1.2.15 receiver validator

The H gateway validator explicitly calls itself a reference integration implementation. H signer/profile, key status, H signature, integrity evidence, identity/delegation, origin receipt and durable ingress are injected callbacks. Missing/unavailable authority evidence returns UNKNOWN. The separate C validator similarly leaves C profile/key/signature, provider evidence, owner ledger, COC, I terminal, D clearance and Storage resolution to callbacks.

The current receiver validator authenticates the H envelope first, then independently validates the C object and the I/D/Storage joins, then invokes durable ingress commit. That is a receiver validation sequence; it does not itself implement the gateway issuer's pre-sign workflow.

### 5.2 Test doubles, not cryptographic proof

The 1.2.15 gateway tests contain 21 test methods. The H signature callback compares the signature field to a fixed "A" repeated 86 times and checks the preimage prefix. The C signature callback in the positive fixture returns True. These are deterministic test doubles. The tests validate orchestration and fail-closed callback handling; they do not cryptographically verify an Ed25519 signature or establish production key custody/trust.

The test test_10_c_signature_must_be_valid_independently_of_h_signature verifies that invalid C signature makes the result INVALID even where the H attestation has already authenticated. That is appropriate for receiver-side verification, but it is not a test that the H issuer refuses to sign before C verification.

### 5.3 Missing issuer-side executable proof

The H P0 contract now normatively requires C verification before H signing. However, the reviewed H branch tree exposes the gateway receiver validator and contract, but no executable issuer/signing entrypoint or test proving this pre-sign order. This remains a specific implementation/test gap, not a claim that the normative contract is wrong.

### 5.4 CI workflow currentness

The current workflow file still labels itself “BMCP Unified 1.2.14 + CSubmitOutcome 1.0.1” and its push path filters explicitly name the 1.2.14 schema and older provider_outcome_validator.py, not the 1.2.15 schema, gateway_attestation_validator.py or provider_outcome_validator_1_2_15.py. The generic conformance-test path is included, but the workflow definition is not yet a clean exact-head 1.2.15 CI contract. No exact successful CI run for H HEAD e3e4cab... was identified in the evidence read here.

---

## 6. Updated B-02 closure checklist / 更新后的 B-02 关闭清单

| Requirement | Status | Required evidence |
|---|---|---|
| C review of H 1.2.14 integrated mapping | **CLOSED AT SCOPED CANDIDATE LEVEL** | C Phase 3.8.17 exact review Blob 36e5... |
| C review of H 1.2.15 schema shape | **CLOSED AT SCOPED CANDIDATE LEVEL** | C Phase 3.8.26 exact review Blob c5ff... |
| C acceptance of corrected pre-sign ordering | **CLOSED AT CONTRACT-ORDER LEVEL** | C Phase 3.8.27 Blob 3ca0... |
| H 1.2.15 Provider Outcome mapping | **PUBLISHED** | H Phase 3.8.21 Blob 2dc30... |
| H 1.2.15 integrated authority-join successor | **OPEN** | Separate exact mapping binding I/D/Storage/COC seams and explicitly versioning 1.2.14 predecessor |
| C review of 1.2.15 integrated successor | **OPEN** | C exact review of that successor Blob and exact validator/test pins |
| H issuer-side pre-sign implementation/test | **OPEN** | Executable C-verification-before-signing entrypoint and negative tests |
| 1.2.15 cryptographic and trust proof | **OPEN** | Real Ed25519 vectors/verifier, I-approved profile/key registry, origin receipt and key-status authority evidence |
| 1.2.15 exact-head CI | **OPEN** | Updated workflow filters, run/commit/job and exact test source pins |
| Storage same-bundle successor manifest | **OPEN** | Storage successor manifest binds 1.2.15 schema, integrated mapping, validator/tests and exact Owner reviews |
| Fresh A same-bundle reconciliation | **OPEN** | Exact Blob readback after all Owner artifacts stabilize |

---

## 7. Ordered next actions / 后续执行顺序

1. H: publish a separate immutable 1.2.15 Integrated Authority-Join Mapping. It must bind the H 1.2.15 schema, CSubmitOutcome 1.0.1, C-P0/H-P0 rules, I terminal, D clearance, Storage resolution, COC evidence, exact validator/test/workflow Blobs, callback inputs/outputs and INVALID/UNKNOWN semantics. Explicitly state how it supersedes or coexists with the 1.2.14 integrated mapping.
2. H: implement or explicitly specify the gateway issuer path and add a test proving C object/schema/digest/signature/semantics are verified before H signs; no H signature or durable ingress on C INVALID/UNKNOWN. Keep receiver-side revalidation as a separate stage.
3. H: update the conformance workflow for 1.2.15 paths and run exact-head CI; pin run, commit, job and source Blobs.
4. C: review the exact 1.2.15 integrated mapping, issuer-side sequence, receiver validator and CI/test Blobs; state ACCEPT / CONDITIONAL ACCEPT / REJECT.
5. I, D: confirm their exact authority seam and currentness/revocation/fence semantics against the successor mapping.
6. Storage: publish a new immutable successor manifest after upstream artifacts stabilize; preserve v3.3.0 as historical candidate evidence.
7. A: perform a fresh exact same-bundle readback and update B-02 and the overall architecture disposition.

Stop if a review references a predecessor Blob, callback authority is self-asserted, C INVALID/UNKNOWN can be signed or committed as valid, replay/commit ambiguity is treated as success, or manifest pins do not match exact artifacts.

---

## 8. Governance boundary / 治理边界

This is an isolated A/integration review branch only. It does not modify main, H/C/I/D/Storage Owner branches, PR #51/#54/#57/#59/#61 or Issue #43. Delegated role artifacts are not independent human Owner signatures. No merge, Gate pass, architecture freeze, protected-path implementation, deployment or production activation is authorized.

**Final disposition: B-02 PARTIAL / OPEN.** Recognize the completed 1.2.14 C integrated-mapping review and the new 1.2.15 C schema/order reviews. Do not overstate them as C acceptance of a 1.2.15 integrated mapping, executable issuer pipeline, production cryptography, exact-head CI or same-bundle Storage manifest.

**最终裁决：B-02 PARTIAL / OPEN。** 应承认 1.2.14 Integrated Mapping 的 C 审查已经完成，也承认 1.2.15 Schema Shape 与签发顺序已有新的 C 审查；但不得将其扩大为 C 已接受 1.2.15 Integrated Mapping、Issuer Pipeline、生产密码学、精确 HEAD CI 或 Storage 同 Bundle Manifest。
