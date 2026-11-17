# Phase 3.8.8 — I Architecture Decision: Cryptographic Profile 1.0
# Phase 3.8.8 — I 架构决策：密码学配置 1.0

- Owner: I — Security, Identity and Governance
- Branch: `session-i-security-governance-2026-11-16`
- Profile proposal: `AIMBA-I-CRYPTO-1.0`, Blob `5eeb011032c53c2f7897d699d6f512b26f07d0a2`
- Exact P0 addendum: `phase-3.8.7-i-exact-signed-object-p0-allowlists.md`, Blob `739dc15e3cca33aef3f012f713b988e5528d4ad9`
- H schema 1.2.8: Blob `70b892797d07489936300a26c0dedfafe1d6e746`
- Status: **APPROVED AS V1 ARCHITECTURE PROFILE BASELINE — NOT PRODUCTION-ACTIVE**
- English and Chinese are normative peers.

## 1. Decision / 决议

I selects `AIMBA-I-CRYPTO-1.0` as the normative v1 architecture cryptographic profile for I-authored protected evidence.

This closes the architecture-level question of which canonicalization/digest/signature construction is used by I in v1. It does not activate production keys or claim regulatory/FIPS approval, deployed trust infrastructure, operational key custody or production conformance.

I 选择 `AIMBA-I-CRYPTO-1.0` 作为 v1 I-authored Protected Evidence 的规范密码学配置。

这关闭 I 在 v1 使用何种 Canonicalization/Digest/Signature 构造的架构选择问题；不代表生产密钥已启用、监管/FIPS 已批准、Trust Infrastructure 已部署、Key Custody 已就绪或生产符合性已通过。

## 2. Exact v1 suite / 精确 v1 算法套件

| Concern | Normative v1 choice |
|---|---|
| Profile bundle | `AIMBA-I-CRYPTO-1.0` |
| Canonicalization | RFC 8785 JCS constrained by RFC 7493 I-JSON |
| Digest | SHA-256 |
| Signature | Ed25519 / RFC 8032 |
| Signature encoding | Canonical Base64url without padding |
| Canonicalization profile ID | `RFC8785-JCS-1.0` |
| Signature profile ID | `AIMBA-ED25519-SHA256-1.0` |
| Payload domain tag | `AIMBA-I-PAYLOAD-v1` |
| Signature domain tag | `AIMBA-I-SIGNATURE-v1` |

No algorithm negotiation, silent fallback, legacy downgrade or cross-owner profile inheritance is permitted. Any different algorithm suite requires a separately versioned profile and explicit I/H/affected-Owner review.

禁止算法协商、静默回退、Legacy 降级或跨 Owner Profile 继承。任何不同算法套件必须定义独立版本配置，并经 I/H/受影响 Owner 明确审查。

## 3. Canonical input contract / 规范输入合同

Before canonicalization:
- strict UTF-8 decode; reject BOM and invalid sequences;
- reject duplicate JSON keys before object materialization;
- reject NaN/Infinity, invalid Unicode and non-I-JSON values;
- reject unsafe integer representations;
- preserve absent/null/empty distinctions;
- perform exact message-family semantic validation before signing/verifying;
- do not apply implicit Unicode normalization, locale formatting or array reordering.

Canonicalization is RFC 8785 JCS. The exact per-family P0 projections are those in the I Phase 3.8.7 addendum. A successor schema adding signed fields requires a successor P0 projection decision.

## 4. Two-stage signature construction / 两阶段签名构造

For each exact I message family:
1. Build exact P0 from the approved per-family allowlist.
2. `P0Bytes = JCS(P0)`.
3. `payload_digest = SHA-256(ASCII("AIMBA-I-PAYLOAD-v1") || 0x00 || P0Bytes)`, lowercase hex.
4. `P = P0 + { payload_digest }`.
5. `PBytes = JCS(P)`.
6. `signature_preimage = ASCII("AIMBA-I-SIGNATURE-v1") || 0x00 || ASCII("AIMBA-I-CRYPTO-1.0") || 0x00 || ASCII(message_type) || 0x00 || PBytes`.
7. Ed25519 signs the exact preimage. Signature is 64 bytes; public key is 32 bytes.
8. Base64url encoding is canonical and unpadded.

The signature reference is allocated before signing, immutable and never derived from signature bytes. COC quorum and transport channel proofs remain independent.

## 5. Trust, key lifecycle and anti-rollback architecture / Trust、Key Lifecycle 与 Anti-rollback 架构

I is the unique authority for issuer identity, trust-profile resolution, key ID/version status, PermissionDomain policy and historical trust evaluation.

The I trust registry MUST bind:
- OwnerAuthorityRef and authenticated issuer/principal/workload;
- exact profile bundle, canonicalization profile, signature profile, digest algorithm;
- key ID and immutable key version;
- permitted message families, audience, purpose, PolicyDomain and Scope;
- effective status generation, validity interval and historical checkpoint;
- revocation/compromise event and effective I sequencer position;
- external monotonic anti-rollback checkpoint reference.

Key status values are ACTIVE, RETIRED, REVOKED, COMPROMISED or UNKNOWN.
- ACTIVE: may sign/verify within exact scope and validity.
- RETIRED: no new signatures; historical signatures remain verifiable only against a trusted historical status checkpoint and issuance interval.
- REVOKED: no new acceptance after its authoritative effective position; prior validity is evaluated against the sequenced history.
- COMPROMISED: signatures in the declared compromise interval are rejected/quarantined; if the compromise start cannot be bounded, affected history is UNKNOWN.
- UNKNOWN: fail closed.

Wall-clock timestamps never replace I sequencer position, key-status generation or external anti-rollback anchor. If the registry, historical checkpoint or anti-rollback source is unavailable/stale/forked, dependent protected operations return UNKNOWN.

## 6. Owner profile isolation / Owner Profile 隔离

This profile applies only to I-authored protected evidence. C, D, H, Storage and COC MUST NOT inherit I's key authority by sharing an envelope or using the same primitive algorithms.

C's `AIMBA-C-OUTCOME-CRYPTO-1.0` is a separate C-owned profile candidate. It may use the same primitive suite only with its own message projection, bundle ID, signature profile ID and domain tags, subject to exact C/I/H review. Storage and COC profiles remain separately owned.

本配置仅适用于 I 撰写的受保护证据。C/D/H/Storage/COC 不得因共用 Envelope 或算法原语而继承 I 的密钥权威。C 的 Profile 是独立 C Owner 配置候选。

## 7. Regulatory/deployment boundary / 监管与部署边界

The v1 architecture selects Ed25519. This is not a statement that every future jurisdiction, HSM, FIPS mode or customer deployment permits it. If a deployment requires another approved suite, it must use a new immutable profile and explicit migration/dual-verification policy. Silent downgrade is forbidden.

Actual HSM/KMS, key ceremonies, production key custody, operator/on-call, hardware module certification and deployment-specific regulatory approval are L4/governance obligations. They do not keep the v1 abstract algorithm choice undecided.

v1 架构选择 Ed25519，但不表示所有司法辖区、HSM、FIPS 模式或客户部署都允许。若部署要求其他算法套件，必须使用新的不可变 Profile 和明确迁移/双重验证策略，禁止静默降级。

实际 HSM/KMS、密钥仪式、生产 Key Custody、Operator/On-call、硬件模块认证及部署监管批准属于 L4/治理义务，不再使 v1 抽象算法选择处于未决状态。

## 8. L3 proof obligations / L3 证明义务

The H 101/101 run is bounded candidate evidence for the generic I profile vector path. It does not cover every exact P0 family in the Phase 3.8.7 addendum.

L3 remains OPEN until two independent implementations pass byte-for-byte vectors for:
- OWNER_LOCAL_PENDING_GATE (I);
- OWNER_LOCAL_GATE_RELEASE (I);
- JF10_I_TERMINAL_DECISION_OBSERVED;
- IOwnerSnapshotAttestation;
- ICompleteEmptyProof and IOutOfScopeProof;
- ICommitAuthorizationReceipt and ITerminalProof;
- historical key status, revocation/compromise, anti-rollback and restore negative cases.

## 9. Final I disposition / I 最终结论

**APPROVED AS V1 ARCHITECTURE PROFILE BASELINE — NOT PRODUCTION-ACTIVE.**

The I v1 cryptographic algorithm selection is decided. Exact P0 definitions are published in the Phase 3.8.7 addendum. H semantic mapping, full per-family independent vectors and operational trust/key lifecycle remain separate L2/L3/L4 gates.

**批准为 v1 架构密码学基线 — 非生产启用。** I v1 算法选择已经确定；精确 P0 定义见 Phase 3.8.7。H Semantic Mapping、逐消息族独立向量和运维 Trust/Key Lifecycle 仍是独立 L2/L3/L4 门槛。
