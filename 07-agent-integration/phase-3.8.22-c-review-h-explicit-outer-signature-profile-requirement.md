# Phase 3.8.22 — C Review: H Explicit Outer Signature-Profile Requirement
# Phase 3.8.22 — C 复审：H 外层 Signature-Profile 明确要求

- Owner perspective: C — Provider Outcome Semantic Authority
- H Unified 1.2.14 schema Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- CSubmitOutcome 1.0.1 schema Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- H envelope auth validator Blob: `a863acd01abcb147db2bd23a3b8bb1985d81bc78`
- H Provider Outcome validator Blob: `b8cd692d261df7a31a0f65c3e003693e305f73a2`
- H envelope-auth test Blob: `3469c5268d3558c777ea9f16058e00570517ff54`
- H Provider Outcome test Blob: `da1454ed985c84160c4cb6a0462df9d1225fab7f`
- H Phase 3.8.20 closure Blob: `73543e8e7963f1442931c318542a4249d1c41790`
- H CI run `44075215559`, commit `a36c34897545316942c7cda8da5d8bea7dacec5b`, job `134011346259`: **63 tests / SUCCESS**
- Decision: **ACCEPT EXPLICIT PROFILE-ID PRESENCE AS FAIL-CLOSED GUARD; DO NOT APPROVE PROFILE OR SIGNER**
- Provenance: delegated C-role review; **not an independent human C Owner signature**.

## 1. C object profile remains separate / C Object Profile 保持独立

C's `AIMBA-C-CRYPTO-1.0` remains scoped to the immutable CSubmitOutcome 1.0.1 P0/signature projection. The outer BMCP envelope has a different field set, message domain and P0. C does not approve automatic reuse of the C object profile for the envelope.

C 的 `AIMBA-C-CRYPTO-1.0` 仍仅适用于不可变 CSubmitOutcome 1.0.1 P0/Signature Projection。外层 BMCP Envelope 具有不同字段集合、Message Domain 与 P0。C 不批准将 C Object Profile 自动复用于 Envelope。

## 2. Signature profile identifier / Signature Profile Identifier

C accepts the H gate's requirement that protected owner-signed envelopes carry an explicit non-empty `signature_profile_id`. This prevents the canonicalization profile from being mistaken for a signature profile and avoids payload-only algorithm fallback. The profile identifier is a claim until authenticated against the I-approved key/issuer registry.

C 接受 H Gate 要求受保护 Owner-signed Envelope 携带非空 `signature_profile_id`。这可避免将 Canonicalization Profile 误作 Signature Profile，也避免 Payload-only Algorithm Fallback。Profile Identifier 在通过 I-approved Key/Issuer Registry 认证前仍只是 Claim。

C does not approve the candidate test string, a real signature profile, algorithm, key, trust root or signer role. A missing profile is INVALID; a proven unregistered/mismatched profile is INVALID; unavailable registry/profile status is UNKNOWN.

C 不批准候选测试字符串、真实 Signature Profile、算法、Key、Trust Root 或 Signer Role。缺失 Profile=INVALID；已证明未注册/不匹配=INVALID；Registry/Profile 状态不可用=UNKNOWN。

## 3. Outer signer role remains open / Outer Signer Role 仍 OPEN

The C adapter origin, H gateway attestor and separate attestor remain distinct options. H's reference test proving a gateway signer can be represented by an authorized registry callback is not C approval. C must explicitly approve any signer claim that represents or attests to a C-owned Provider Outcome. The immutable C object signature remains mandatory and independent.

C Adapter Origin、H Gateway Attestor 与独立 Attestor 仍是不同选项。H Reference Test 证明 Gateway Signer 可由授权 Registry Callback 表达，不等于 C 批准。任何代表/证明 C-owned Provider Outcome 的 Signer Claim 均需 C 明确批准。不可变 C Object Signature 仍必须独立存在。

## 4. C decision / C 侧决议

**Delegated C-role decision: ACCEPT the explicit signature_profile_id presence check as a fail-closed interface guard. Outer P0 field allowlist, signature preimage, signer role, profile registration and production C trust remain OPEN. NOT FROZEN.**

**角色模拟 C 侧决议：接受显式 signature_profile_id 存在性检查作为 fail-closed 接口保护。Outer P0 Allowlist、Signature Preimage、Signer Role、Profile Registration 与生产 C Trust 仍 OPEN，不冻结。**
