# Phase 3.8.26 — C Exact Review: H Unified 1.2.15 Gateway-Attestation Schema
# Phase 3.8.26 — C 精确复审：H Unified 1.2.15 Gateway-Attestation Schema

- H schema 1.2.15 Blob: `860fc4cec658db7d2703cd6adf72aa31a2723f6d`
- H exact mapping document Blob: `2dc30f193d9c4f4bdc05ca4c137103687db28924`
- H P0 candidate Blob: `a08bff1145dfeccac3e583e065055ca7dfdcb189`
- CSubmitOutcome 1.0.1 Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- C P0 signer/attestation disposition Blob: `65aa82bac678e317325b1673121b92c04121b4f4`
- C P0 exact re-review Blob: `6a5c5c63a12bdfd8ef23f76dcee9ae30ab40db6c`
- Status: **ACCEPT SCHEMA SHAPE WITH C-OWNED SEMANTIC CONDITIONS; VALIDATOR/CI NOT YET REVIEWED**
- Provenance: delegated C-role exact review; not an independent human C Owner signature.

## 1. C schema disposition / C Schema 结论

C accepts the 1.2.15 structural changes as a candidate:
- schema artifact revision advances immutably from 1.2.14 to 1.2.15; wire family remains 1.3.0;
- the C Provider Outcome branch conditionally requires H signature profile, origin transport receipt/digest, original raw-byte digest, original C-side issuer/sender identity, origin auth/channel refs and H signing sequence;
- `owner_authority` is constrained to C for this branch;
- SHA-256 digest fields use 64-character lowercase hex consistent with both H and C schemas;
- `signature_profile_id` is distinct from `canonicalization_profile_id`.

C 接受 1.2.15 结构变更作为候选：
- Schema Artifact Revision 从 1.2.14 不可变升级到 1.2.15，Wire Family 保持 1.3.0；
- C Provider Outcome Branch 条件性要求 H Signature Profile、Origin Transport Receipt/Digest、原始 Raw-Byte Digest、原始 C Issuer/Sender Identity、Origin Auth/Channel Ref 与 H Signing Sequence；
- 该 Branch 将 `owner_authority` 限定为 C；
- SHA-256 Digest 使用 64 字符小写十六进制，与 H/C Schema 一致；
- `signature_profile_id` 与 `canonicalization_profile_id` 明确分离。

## 2. C-owned conditions / C 自有条件

1. The schema's new origin fields are claims/carriers only. H semantic validation must authenticate the origin receipt and compare the original adapter identity to the immutable C object's `AdapterRef` under an explicit registry relation.
2. All C Provider Outcome duplicated wire fields remain exact equality checks against the immutable CSubmitOutcome 1.0.1 object. The C object signature and C key-status chain remain independently required.
3. H must verify the C object schema/digest/signature before issuing its gateway attestation. Authenticated transport alone does not authorize signing a malformed or unauthenticated C object.
4. The H attestation cannot change C `Outcome`, `SideEffectStatus`, ProviderAttempt, gate generation, idempotency namespace/key, request boundary or provider evidence.
5. The schema's `owner_authority=C` constraint does not mean the H gateway is the C owner; H signer identity remains distinct and requires I-approved delegation.
6. A missing/partial origin receipt or unavailable C object/adapter registry returns UNKNOWN; a proven mismatch returns INVALID.

1. 新 Origin 字段仅为 Claim/Carrier。H Semantic Validator 必须认证 Origin Receipt，并通过显式 Registry Relation 将原始 Adapter Identity 与不可变 C Object `AdapterRef` 对账。
2. 所有 C Provider Outcome 重复 Wire Field 仍必须与不可变 CSubmitOutcome 1.0.1 Object 精确相等。C Object Signature 与 C Key Status Chain 仍独立必需。
3. H 必须先验证 C Object Schema/Digest/Signature，才能签发 Gateway Attestation。Transport Authentication 本身不授权为格式错误或未认证 C Object 签名。
4. H Attestation 不得修改 C Outcome、SideEffectStatus、ProviderAttempt、Gate Generation、Idempotency Namespace/Key、Request Boundary 或 Provider Evidence。
5. Schema 的 `owner_authority=C` 不意味着 H Gateway 是 C Owner；H Signer Identity 仍独立，且需 I 批准 Delegation。
6. Origin Receipt 缺失/不完整或 C Object/Adapter Registry 不可用返回 UNKNOWN；已证明不匹配返回 INVALID。

## 3. Required conformance tests / 必需符合性测试

Before C accepts the validator, H must test:
- valid 1.2.15 full envelope and rejection of 1.2.14/1.2.15 revision substitution;
- each of the 12 conditional fields missing individually;
- wrong owner_authority, invalid lowercase-hex digest, malformed signing sequence and date-time;
- origin sender/AdapterRef mismatch and raw-byte digest mismatch;
- every duplicated C wire field mutated independently;
- valid H signature + invalid C signature, and valid C signature + invalid H signature;
- C UNKNOWN/IN_DOUBT remains nonterminal after valid H attestation.

在 C 接受 Validator 前，H 必须测试：完整 1.2.15 Envelope、1.2.14/1.2.15 Revision 替换拒绝、12 个条件字段逐个缺失、Owner Authority 错误、Lowercase-Hex Digest 错误、Signing Sequence/Date-Time 格式错误、Origin Sender/AdapterRef 与 Raw-Byte Digest 不匹配、每个 C 重复字段独立变异、H/C Signature 交叉有效性组合，以及有效 H Attestation 后 C UNKNOWN/IN_DOUBT 仍非终态。

## 4. C disposition / C 侧最终结论

**Delegated C-role decision: ACCEPT H Unified 1.2.15 schema shape as a candidate with the above C-owned conditions. This is not validator conformance, C object signature approval, I profile registration or production ingress approval. NOT FROZEN.**

**角色模拟 C 侧决议：接受 H Unified 1.2.15 Schema Shape 作为候选，但必须满足上述 C 自有条件。此决议不代表 Validator 符合性、C Object Signature 批准、I Profile 注册或生产 Ingress 批准。不冻结。**
