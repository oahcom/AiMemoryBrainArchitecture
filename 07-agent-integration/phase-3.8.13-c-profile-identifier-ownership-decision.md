# Phase 3.8.13 — C Profile Identifier Ownership Decision
# Phase 3.8.13 — C Profile Identifier 权属决议

- Owner perspective: C — Provider Outcome semantic and cryptographic authority
- Status: **C-OWNED PROFILE IDENTIFIER CONFIRMED AS CANDIDATE; I NAMING REFERENCE NOT ADOPTED**
- Project phase: **ARCHITECTURE DESIGN**
- CSubmitOutcome 1.0.1 schema: Blob a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda
- C signature projection: Blob 06d9264124d85896ccd44ef7789d9af245d8255b
- C Phase 3.11.1 sequence namespace amendment: Blob 6fa67af110ebbc5ef57ed908bb4880d99c5e46fb
- I crypto profile architecture decision: Blob 56e956dca909af857469427378777705a5d1082a
- H validator core: Blob 0449090a0367576b8b4ac20b1b46897facf9233d
- Provenance: delegated C-role decision; **not an independent human C Owner signature**.

## 1. C-owned profile ID / C 自有 Profile ID

For CSubmitOutcome schema 1.0.1 and the current C signature projection, the C-owned candidate profile identifier is:

**AIMBA-C-CRYPTO-1.0**

This is the exact value required by C schema 1.0.1 and used by the C signature projection and H validator. It is separate from I's AIMBA-I-CRYPTO-1.0 profile and has its own C-P0 projection, C payload/signature domain tags, key namespace and C trust registration decision.

对于 CSubmitOutcome 1.0.1 与当前 C Signature Projection，C 自有候选 Profile ID 为 **AIMBA-C-CRYPTO-1.0**。该值由 C Schema 1.0.1 强制要求，并由 C Signature Projection 与 H Validator 使用。它与 I 的 AIMBA-I-CRYPTO-1.0 分离，具有独立 C-P0 投影、Payload/Signature Domain Tag、Key Namespace 与 C Trust 注册决议。

## 2. I decision naming reference / I 决议中的名称引用

I Phase 3.8.8 §6 mentions AIMBA-C-OUTCOME-CRYPTO-1.0 as a separate C-owned profile candidate. C records that this name is **not adopted** by C schema 1.0.1 and is not an authorized alias for AIMBA-C-CRYPTO-1.0.

This does not criticize I's owner-profile isolation decision. I is correct that C must not inherit I's key authority or signature profile. However, only C may select or rename the C-owned profile identifier.

I Phase 3.8.8 §6 提到 AIMBA-C-OUTCOME-CRYPTO-1.0 作为独立 C Profile 候选。C 明确该名称**未被采纳**，不是 C Schema 1.0.1 的值，也不是 AIMBA-C-CRYPTO-1.0 的别名。

这不影响 I 关于 Owner Profile 隔离的正确决议：C 不得继承 I 的 Key Authority 或 Signature Profile。但只有 C 有权选择或重命名 C 自有 Profile ID。

## 3. Migration rule / 迁移规则

- H and all verifiers MUST use the exact profile ID carried by the C object schema and C signed projection. For C schema 1.0.1 this is AIMBA-C-CRYPTO-1.0.
- No verifier may accept both names as aliases or silently normalize one to the other.
- If C later adopts AIMBA-C-OUTCOME-CRYPTO-1.0, C must publish a successor immutable C schema/profile revision, new P0 and domain-tag contract, migration/dual-verification policy, vectors and H mapping. Old C records remain verified under their original exact profile.
- I profile registration and trust governance remain separate. I may register/approve the C profile only within I's trust-registry authority; it cannot change the C profile ID.

H 与所有 Verifier 必须使用 C 对象 Schema/签名投影声明的精确 Profile ID；C Schema 1.0.1 固定为 AIMBA-C-CRYPTO-1.0。不得将两个名称都接受为别名或静默规范化。若 C 将来采纳 AIMBA-C-OUTCOME-CRYPTO-1.0，必须发布新的不可变 C Schema/Profile 修订、P0/Domain Tag 合同、迁移/双重验证策略、向量和 H Mapping。历史 C 记录仍按原 Profile 验证。I 只负责其 Trust Registry 范围内的注册/信任治理，不能更改 C Profile ID。

## 4. C disposition / C 侧决议

**Delegated C-role decision: CONFIRM AIMBA-C-CRYPTO-1.0 as the sole C candidate profile ID for CSubmitOutcome 1.0.1. AIMBA-C-OUTCOME-CRYPTO-1.0 is NOT ADOPTED.**

The profile remains a candidate pending I trust registration and exact independent vectors. No production key, trust root, key custody or provider conformance is approved.

**角色模拟 C 侧决议：确认 AIMBA-C-CRYPTO-1.0 是 CSubmitOutcome 1.0.1 唯一 C 候选 Profile ID；AIMBA-C-OUTCOME-CRYPTO-1.0 未采纳。** Profile 仍待 I Trust 注册及独立向量验证；未批准生产密钥、Trust Root、Key Custody 或 Provider 一致性。
