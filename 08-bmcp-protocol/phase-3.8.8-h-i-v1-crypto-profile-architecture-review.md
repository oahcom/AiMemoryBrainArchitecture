# Phase 3.8.8 — H Exact Review of I v1 Crypto Profile Architecture Decision
# Phase 3.8.8 — H 对 I v1 Crypto Profile 架构决策的精确审查

- Reviewer: H — BMCP Protocol and Adapter Authentication
- Branch: `session-h-bmcp-protocol`
- Exact I profile decision: `09-security-governance/phase-3.8.8-i-crypto-profile-architecture-decision.md`
- I decision Blob: `f2ac2d2211de91364b56cb8b2c13d38f4b2d4aaf`
- Exact I P0 addendum: Blob `739dc15e3cca33aef3f012f713b988e5528d4ad9`
- H unified schema 1.2.8: Blob `70b892797d07489936300a26c0dedfafe1d6e746`
- H owner snapshot schema: Blob `ecf9971b089ca5fab9a92915663dc913c8ab1ba6`
- Decision: **ACCEPT AS NORMATIVE I V1 WIRE/CRYPTO ARCHITECTURE INPUT; L3 VECTORS REMAIN OPEN**
- English and Chinese are normative peers.

## 1. H decision / H 决议

H accepts I's selection of RFC 8785 JCS constrained by RFC 7493 I-JSON, SHA-256, Ed25519 and canonical unpadded Base64url as the normative v1 I profile architecture input. H accepts the separation of profile bundle ID, canonicalization profile ID and signature profile ID.

H 接受 I 选择 RFC 8785 JCS（受 RFC 7493 I-JSON 约束）、SHA-256、Ed25519 和无 Padding 的规范 Base64url 作为 v1 I Profile 架构输入。H 接受 Profile Bundle ID、Canonicalization Profile ID 和 Signature Profile ID 的分离。

## 2. Exact mapping / 精确映射

- Bundle: `AIMBA-I-CRYPTO-1.0`
- Canonicalization: `RFC8785-JCS-1.0`
- Signature profile: `AIMBA-ED25519-SHA256-1.0`
- Digest: `SHA-256`
- Signature: Ed25519 / RFC 8032
- Payload/signature domain separation: `AIMBA-I-PAYLOAD-v1` and `AIMBA-I-SIGNATURE-v1`
- Exact P0 families: I Phase 3.8.7 §§3–6
- Owner snapshot attestation: H schema `bmcp.i-owner-snapshot-attestation/1.0.0`

H confirms the common envelope projection applies only to the named BMCP message families. Standalone I proof objects use their exact object-specific P0 field lists. COC quorum and transport channel proofs remain independent.

## 3. Binding H conditions / H 约束条件

1. For protected I-signed messages, H semantic validation requires exact bundle/profile/canonicalization/digest IDs even if a legacy structural schema leaves a field optional.
2. H resolves the profile only after authenticated owner authority and I trust registry resolution; payload algorithm hints are never authoritative.
3. H must validate exact per-family P0 extraction, duplicate-key rejection, strict UTF-8/I-JSON and digest/signature reconstruction.
4. H must dereference and validate IOwnerSnapshotAttestation and ensure exact ref/digest/summary equality.
5. H must validate ICompleteEmptyProof and IOutOfScopeProof separately; an empty response is not proof of an empty set.
6. H must independently verify COC quorum fields excluded from I P0.
7. A successor schema adding signed fields requires a successor P0 review; no automatic profile compatibility is inferred.

## 4. L3 status / L3 状态

H 101/101 CI is a bounded candidate test pass and does not prove every P0 family. Full independent Python/Node (or equivalent) byte-identical vectors for all I message/proof families, key lifecycle and anti-rollback negative cases remain L3 OPEN.

## 5. Final H disposition / H 最终结论

**ACCEPT AS NORMATIVE I V1 WIRE/CRYPTO ARCHITECTURE INPUT; L3 VECTORS REMAIN OPEN.**

H accepts the exact I profile decision and P0 projection contract as normative v1 architecture input. This does not approve production trust roots, HSM/KMS, deployment-specific regulatory suitability, live key registry, production semantic validator or production conformance.

**接受为 v1 I Wire/Crypto 规范架构输入；L3 向量仍 OPEN。** 不代表生产 Trust Root、HSM/KMS、部署监管适用性、实时 Key Registry、生产 Semantic Validator 或生产符合性已批准。
