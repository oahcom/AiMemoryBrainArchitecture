# Phase 3.8.6 — H Exact Review of C Outcome Crypto Profile and P0
# Phase 3.8.6 — H 对 C Outcome Crypto Profile 与 P0 的精确审查

- Reviewer: H — BMCP Protocol and Adapter Authentication
- Branch: `session-h-bmcp-protocol`
- Exact C profile/P0 artifact: `07-agent-integration/phase-3.8.6-c-provider-outcome-signature-profile-and-p0.md`
- C profile/P0 Blob: `44641b4b01d721c47e08ae9380ffe645bb3ccda0`
- H schema 1.2.8 Blob: `70b892797d07489936300a26c0dedfafe1d6e746`
- H crypto mapping Blob: `b132e6a01bcfe13f92020b9778ee3f7ddbf65753`
- Decision: **ACCEPT AS C-SPECIFIC CRYPTO PROFILE CANDIDATE WITH ENUMERATED AMENDMENTS**
- English and Chinese are normative peers.

## 1. H decision / H 决议

H confirms the C profile is distinct from I's profile by bundle ID, signature-profile ID, message-type domain separation, owner authority and P0 projection. The candidate construction is compatible with H's common envelope and the 1.2.8 `C_PROVIDER_OUTCOME_RECORDED` message family.

H confirms the C P0 field list maps to the 1.2.8 schema properties. The four COC-attached fields are excluded from the C owner signature and must be independently verified under COC quorum authority.

H 确认 C Profile 通过 Bundle ID、Signature Profile ID、Message-Type Domain Separation、Owner Authority 和 P0 Projection 与 I Profile 区分。候选构造与 H Common Envelope 及 1.2.8 的 `C_PROVIDER_OUTCOME_RECORDED` 消息族兼容。

H 确认 C P0 字段清单映射到 1.2.8 Schema Properties。四个 COC 附加字段从 C Owner Signature 排除，并必须由 COC Quorum Authority 独立验证。

## 2. Schema alignment / Schema 对齐

C P0 includes every C-owned semantic field in the exact schema, including:
- C outcome identity/digest and five-value enum;
- Provider/Adapter/idempotency key/request/receipt;
- final request boundary and request digest;
- transaction/participant/attempt/ledger tuple;
- I/D/Storage evidence references;
- provider outcome/lookup/no-handoff/not-invoked/unknown evidence;
- C owner admission/ledger/high-water/root;
- COC participant intent and explicit absence reason;
- stable preassigned owner_signature_ref and exact profile/key/envelope fields.

The only exclusions are payload_digest, signature, external integrity/channel proof locators and the COC appended quorum/record fields. H found no schema property omitted from the C profile allowlist except message_type, which is included in the common-envelope list.

## 3. Binding H amendments / H 约束性修订

1. H semantic validation MUST enforce `AIMBA-C-OUTCOME-CRYPTO-1.0`, `RFC8785-JCS-1.0`, `AIMBA-C-ED25519-SHA256-1.0` and SHA-256 for protected C outcome records; the structural schema's optional `signature_profile_id` is not sufficient.
2. H must reject I profile IDs on C outcome messages unless an explicit future joint profile is approved by C/I/H.
3. H must enforce exact P0 extraction, canonical duplicate-key rejection, digest equality and signature verification.
4. H must independently verify COC quorum proof and must not include COC appended fields in C's owner-signed P0.
5. H must verify null-vs-absent COC intent semantics and require a non-empty absence reason when the intent is null.
6. H must not infer Provider Outcome truth from a valid C signature alone; C's evidence semantics still apply.

## 4. L3 vector requirements / L3 向量要求

C-specific Python/Node (or equivalent independent) vectors are required for the exact P0, C semantic digest, common payload digest, signature preimage, signature verification, COC append invariance, optional/null fields, and negative profile/audience/owner/tuple mutations. Existing H 101/101 CI covers the I profile candidate path and does not close C-specific vectors.

## 5. Final H disposition / H 最终结论

**ACCEPT AS C-SPECIFIC CRYPTO PROFILE CANDIDATE WITH ENUMERATED AMENDMENTS.**

C profile/P0 Blob `a9b891a109c47422b2387919a42d25172b6c09e0` is accepted as a structurally coherent candidate for H schema 1.2.8. This is not production cryptographic approval, trust-root approval, cross-language C vectors, schema freeze or runtime conformance.

**接受为 C 专属密码学候选，并保留修订。** 该 Blob 与 H Schema 1.2.8 结构一致；不代表生产密码学批准、Trust Root 批准、C 跨语言向量通过、Schema 冻结或运行时符合性。
