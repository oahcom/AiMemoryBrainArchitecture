# Phase 3.8.19 — H Review: C Outer Envelope Signer/P0 and Wire Mapping Contract
# Phase 3.8.19 — H 复审：C Outer Envelope Signer/P0 与 Wire Mapping 合同

- H authority: BMCP wire protocol, canonical representation and gateway integration
- C exact decision candidate Blob: 6347c9aa80bb48adb2e2e4f318960e14ba16f33e
- H Unified schema 1.2.14 Blob: 09fcd1fa29fe24255fbd87cae79dafb406594a59
- H outer-envelope gap contract Blob: fbb7553b0bd0c7a9714304983882ca2cc1fa9cc1
- Status: **ACCEPT SEPARATE C-ORIGIN ENVELOPE SIGNATURE AS CANDIDATE; H JSON-POINTER MAPPING AND EXECUTABLE VALIDATOR STILL REQUIRED**
- Provenance: delegated H-role review; not an independent human H Owner signature.

## 1. H decision / H 决策

H accepts the C-owned provider adapter as the candidate origin signer for C_PROVIDER_OUTCOME_RECORDED. H will treat the immutable CSubmitOutcome object signature and the outer BMCP envelope signature as separate verification stages and separate P0 projections. H gateway attestation, if implemented, is a separate H-origin receipt only.

H accepts the architectural separation, not the exact projection as a frozen wire contract. The C proposal's field inventory must be converted into an exact JSON-Pointer table derived mechanically from H schema 1.2.14 and the C object schema 1.0.1. The current proposal requires one correction before mapping freeze: its common-envelope P0 inventory omits the serialized `integrity_proof_ref` and `channel_binding_proof_ref` in §§4.1 even though §4.4 says both are included. They must be explicitly listed in the allowlist and test vectors.

H 接受 C-owned Provider Adapter 作为 C_PROVIDER_OUTCOME_RECORDED 候选 Origin Signer。H 将不可变 CSubmitOutcome Object Signature 与外层 BMCP Envelope Signature 作为独立验证阶段、独立 P0 Projection。若实现 H Gateway Attestation，它只能是独立 H-origin Receipt。

H 接受架构分离，但不将精确 Projection 视为已冻结 Wire Contract。C 提案字段 Inventory 必须转换为从 H Schema 1.2.14 与 C Object Schema 1.0.1 机械推导的精确 JSON-Pointer Table。当前提案在 Mapping Freeze 前需要一项修正：§4.1 Common-Envelope P0 Inventory 漏列了序列化的 `integrity_proof_ref` 与 `channel_binding_proof_ref`，尽管 §4.4 声称二者被包含。必须将它们明确列入 Allowlist 与 Test Vector。

## 2. H-owned mapping obligations / H 自有 Mapping 义务

H must publish a derived table for each property in the exact `C_PROVIDER_OUTCOME_RECORDED` branch:
- JSON Pointer;
- source schema path and exact schema artifact revision;
- required/optional/nullability;
- included in outer C-envelope P0 / excluded / derived;
- exact equality rule to the immutable C object when duplicated;
- authority that issues/verifies the referenced object;
- missing/null/mismatch/unavailable disposition;
- whether the property is coordinator-appended after C origin signing.

H must explicitly distinguish:
- outer envelope `payload_digest` / `signature`;
- C object `payload_digest` / `signature`;
- `integrity_proof_ref` and `channel_binding_proof_ref`;
- coordinator-appended COC record/quorum fields.

H 必须针对精确 `C_PROVIDER_OUTCOME_RECORDED` 分支的每个 Property 发布派生表：
- JSON Pointer；
- Source Schema Path 与精确 Schema Artifact Revision；
- Required/Optional/Nullability；
- 是否纳入 Outer C-Envelope P0 / 排除 / 派生；
- 与不可变 C Object 重复时的精确 Equality Rule；
- 引用对象的签发/验证 Authority；
- Missing/Null/Mismatch/Unavailable 处置；
- Property 是否在 C Origin Signing 后由 Coordinator 追加。

H 必须明确区分：
- 外层 Envelope `payload_digest` / `signature`；
- C Object `payload_digest` / `signature`；
- `integrity_proof_ref` 与 `channel_binding_proof_ref`；
- Coordinator 追加的 COC Record/Quorum Field。

## 3. H validator obligations / H Validator 义务

- strict raw parse before JSON materialization; reject duplicate keys and invalid/non-I-JSON values;
- pin exact H schema 1.2.14 and C object schema 1.0.1;
- extract exact C outer P0; recompute digest and verify signature via I-approved C profile registry;
- obtain protected transport principal/session context outside payload;
- validate channel binding against protected session context;
- bind sender_authority_ref, sender_subject_ref, issuer_ref, subject_ref, audience, key_id_ref and key_version to authenticated verifier context;
- authoritative nonce replay/idempotency ledger; unavailable => UNKNOWN;
- independently dereference/verify C object signature and C semantic digest;
- verify all duplicated H/C wire values and owner-specific I/D/Storage/COC evidence;
- return VALID only if every required layer is verified.

- JSON Materialization 前严格 Raw Parse；拒绝 Duplicate Key 与 Invalid/Non-I-JSON Value；
- Pin 精确 H Schema 1.2.14 与 C Object Schema 1.0.1；
- 提取精确 C Outer P0；重算 Digest，并通过 I-approved C Profile Registry 验证 Signature；
- 从 Payload 之外取得 Protected Transport Principal/Session Context；
- 将 Channel Binding 与 Protected Session Context 核对；
- 将 sender_authority_ref、sender_subject_ref、issuer_ref、subject_ref、audience、key_id_ref、key_version 绑定到 Authenticated Verifier Context；
- 使用权威 Nonce Replay/Idempotency Ledger；不可用 → UNKNOWN；
- 独立解引用/验证 C Object Signature 与 C Semantic Digest；
- 验证所有重复 H/C Wire Value 与 Owner-specific I/D/Storage/COC Evidence；
- 仅在每层必需检查均验证通过后返回 VALID。

## 4. H disposition / H 侧结论

**ACCEPT C-origin outer-envelope signature as the candidate architecture. Exact wire mapping, the two missing proof-reference fields in the C allowlist, I profile approval and executable full-path conformance remain OPEN. No H implementation or production authentication is claimed.**
