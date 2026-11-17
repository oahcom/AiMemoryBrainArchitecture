# Phase 3.8.10 — I Scope Clarification: C-Owned Profile Identifier
# Phase 3.8.10 — I 范围澄清：C 自有 Profile Identifier

- Owner perspective: I — Security, Identity and Governance
- Status: **I PROFILE ISOLATION CONFIRMED; C PROFILE NAME DEFERRED TO C OWNER**
- Project phase: **ARCHITECTURE DESIGN**
- I crypto profile architecture decision: Blob 56e956dca909af857469427378777705a5d1082a
- C profile identifier ownership decision: Blob 5067dadb9c646a054d78f03c56e635facc36311a
- CSubmitOutcome 1.0.1 schema: Blob a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda
- C signature projection: Blob 06d9264124d85896ccd44ef7789d9af245d8255b
- Provenance: delegated I-role clarification; **not an independent human I Owner signature**.

## 1. Clarification / 澄清

I Phase 3.8.8 §6's mention of AIMBA-C-OUTCOME-CRYPTO-1.0 was an illustrative candidate name intended only to express that C must have a profile separate from I. It was not an I decision selecting, renaming, registering or authorizing a C profile identifier.

C has confirmed that CSubmitOutcome 1.0.1 and the current C signature projection use AIMBA-C-CRYPTO-1.0 as the sole C-owned candidate identifier. I recognizes C's decision.

I Phase 3.8.8 §6 提及 AIMBA-C-OUTCOME-CRYPTO-1.0，仅是表达 C 必须拥有独立于 I 的 Profile 的示例候选名称，不是 I 对 C Profile ID 的选择、重命名、注册或授权。

C 已确认 CSubmitOutcome 1.0.1 与当前 C Signature Projection 使用 AIMBA-C-CRYPTO-1.0 作为唯一 C 自有候选标识。I 尊重并确认 C 的权属决议。

## 2. Authority boundary / 权威边界

- I selects and governs AIMBA-I-CRYPTO-1.0 for I-authored protected evidence.
- C alone selects the C-owned profile identifier, C-P0, C domain tags, and C signature projection.
- I may register, trust, reject or revoke C keys/profile material within I's trust registry and governance remit; I cannot rename the C profile or alter C's signed semantic projection.
- H must validate the exact profile ID in the immutable C object and the C-owned schema; no aliasing or silent fallback.
- A must bind the exact C and I profile identifiers separately in any integration manifest.

- I 为 I-authored Protected Evidence 选择并治理 AIMBA-I-CRYPTO-1.0；
- C 独占选择 C Profile ID、C-P0、C Domain Tag 与 C Signature Projection；
- I 可在 Trust Registry/治理范围内注册、信任、拒绝或撤销 C Key/Profile Material，但不能重命名 C Profile 或修改 C 签名语义投影；
- H 必须验证不可变 C 对象与 C Schema 中的精确 Profile ID，不得别名或静默回退；
- A 在集成清单中必须分别绑定 C 与 I 的精确 Profile ID。

## 3. Status / 状态

- I v1 architecture profile: **APPROVED AS V1 ARCHITECTURE BASELINE — NOT PRODUCTION-ACTIVE**.
- C profile identifier AIMBA-C-CRYPTO-1.0: **C-OWNED CANDIDATE — NOT I-REGISTERED**.
- AIMBA-C-OUTCOME-CRYPTO-1.0: **NON-NORMATIVE EXAMPLE ONLY; NOT ADOPTED**.
- C trust registration, key custody, historical key status, anti-rollback and production verification: **OPEN**.

## 4. I disposition / I 侧决议

**Delegated I-role decision: ACCEPT C's profile ownership clarification. No I profile change is made.**

**角色模拟 I 侧决议：接受 C 的 Profile 权属澄清；I 自身 Profile 不作变更。** I v1 Profile 仍非生产启用；C Profile 仍待 I Trust 注册及部署治理。
