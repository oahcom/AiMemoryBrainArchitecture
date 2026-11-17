# Phase 3.8.6 — I Exact Review of C Outcome Crypto Profile and P0
# Phase 3.8.6 — I 对 C Outcome Crypto Profile 与 P0 的精确审查

- Reviewer: I — Security, Identity and Governance
- Branch: `session-i-security-governance-2026-11-16`
- Exact C profile/P0 artifact: `07-agent-integration/phase-3.8.6-c-provider-outcome-signature-profile-and-p0.md`
- C profile/P0 Blob: `a9b891a109c47422b2387919a42d25172b6c09e0`
- Exact H schema: unified 1.2.8, Blob `70b892797d07489936300a26c0dedfafe1d6e746`
- I trust authority/profile boundary: I owns issuer identity/key status and historical trust; C owns its outcome semantics/profile projection.
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS — TRUST REGISTRY / PROFILE SEPARATION**
- English and Chinese are normative peers.

## 1. I decision / I 决议

I accepts the C-owned profile bundle `AIMBA-C-OUTCOME-CRYPTO-1.0` as a distinct candidate profile, separate from `AIMBA-I-CRYPTO-1.0`. The use of the same candidate primitive suite (JCS, SHA-256, Ed25519) does not make the profiles interchangeable because owner authority, profile ID, domain separation, message type and P0 projection differ.

I 接受 C 自有 Profile Bundle `AIMBA-C-OUTCOME-CRYPTO-1.0` 作为独立候选配置，与 `AIMBA-I-CRYPTO-1.0` 分离。即使候选基础算法相同（JCS、SHA-256、Ed25519），Owner Authority、Profile ID、Domain Separation、Message Type 与 P0 Projection 不同，两个配置仍不可互换。

## 2. I authority boundary / I 权威边界

- C owns the meaning of HANDOFF_ACCEPTED / HANDOFF_REJECTED / NOT_INVOKED / UNKNOWN / IN_DOUBT and the C-signed P0 projection.
- I owns authenticated C issuer/owner resolution, key ID/version status, revocation/compromise state and historical trust checkpoints.
- H validates the wire envelope, schema, canonicalization and signature mechanics.
- C's profile ID must be registered/authorized under the I trust registry for the C issuer and exact audience/purpose/message family. A payload cannot self-authorize a profile.
- I does not sign or alter C provider evidence, and C cannot mint I trust/key status.

## 3. Binding amendments / 约束性修订

1. The C profile registry entry must bind exact C OwnerAuthorityRef, issuer/principal/workload, audience, purpose, message family `C_PROVIDER_OUTCOME_RECORDED`, key ID/version, profile bundle ID, signature profile ID, canonicalization profile ID, digest algorithm and effective status generation.
2. C's `owner_signature_ref` must be preallocated, immutable and included in P0; it cannot be derived from signature bytes.
3. The C outcome semantic digest and common-envelope payload digest must remain separate as specified; both must be recomputed and checked. No circular field inclusion is permitted.
4. C's P0 must include all C-authored outcome evidence, provider identity/key, request digest, participant tuple, owner admission and explicit COC absence semantics. Only the four coordinator-appended COC fields and explicitly external proof locators may be excluded.
5. Key-status UNKNOWN, historical checkpoint missing, anti-rollback anchor unavailable, wrong owner/audience/purpose or profile downgrade must fail closed.
6. The candidate Ed25519 profile is not a statement of regulatory/FIPS suitability. Any deployment-specific algorithm change requires a separately versioned C profile and exact H/I/C review.

## 4. L3 proof obligations / L3 证明义务

I requires two independent C-specific implementations to match:
- exact C P0 bytes and CSubmitOutcomeDigest;
- common-envelope payload_digest and signature preimage;
- signature verification with the registered C key version;
- rejection for changed request digest, provider key, tuple, issuer, audience, message type or profile;
- COC append invariance for the C signature plus independent COC quorum verification;
- retired/revoked/compromised key and historical checkpoint behavior;
- restore/anti-rollback and stale key-status behavior.

H's current 101/101 candidate suite is not evidence that these C-specific vectors have passed.

## 5. Final I disposition / I 最终结论

**ACCEPT WITH ENUMERATED AMENDMENTS — TRUST REGISTRY / PROFILE SEPARATION.**

I accepts C Blob `a9b891a109c47422b2387919a42d25172b6c09e0` as a distinct C-owned profile candidate. I will resolve issuer/key trust and profile registration, but this decision does not approve production trust roots, HSM/KMS, key custody, production rotation/revocation operation, algorithm regulatory suitability or implementation.

**有条件接受 — Trust Registry/Profile Separation。** I 接受该 Blob 作为 C 自有独立 Profile 候选。I 负责 Issuer/Key Trust 与 Profile Registry 解析，但不批准生产 Trust Root、HSM/KMS、Key Custody、生产轮换/撤销、算法监管适用性或实现。
