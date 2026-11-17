# Phase 3.8.3 — I Exact Review of H I-Crypto Wire Mapping
# Phase 3.8.3 — I 对 H I-Crypto Wire Mapping 的精确版本审查

- Reviewer: I — Security, Identity and Governance
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Review mode: delegated I-role simulation at the user's direction; not an independent human Owner signature.
- Status: **CANDIDATE SECURITY/WIRE COMPOSITION ONLY — NOT CRYPTOGRAPHICALLY FROZEN**
- English and Chinese are normative peers.

## 1. Exact reviewed artifacts / 精确审查对象

| Artifact | Branch | Exact Blob |
|---|---|---|
| I Cryptographic Trust Profile Proposal | `session-i-security-governance-2026-11-16` | `5eeb011032c53c2f7897d699d6f512b26f07d0a2` |
| H I-Crypto Wire Mapping | `session-h-bmcp-protocol` | `c30e8ccbecb75b7e27ddceb0cf088afbbb26f562` |
| H Unified Schema artifact 1.2.7 | `session-h-bmcp-protocol` | `e9748a5b904d2b975e47a32a0cbb31de31636854` |
| I Phase 3.8 Commit Authorization / Revocation Sequencer | `session-i-security-governance-2026-11-16` | `54bab0484bd232a5a258e65e34cc7425288b39a6` |
| H RecoveryJoin schema 1.0.0 | `session-h-bmcp-protocol` | `dd3234aa1c74caf6d0e335875cd96e0b2b64082f` |

## 2. Accepted composition / 接受的组合关系

I accepts the following as a coherent candidate boundary:

1. The profile bundle `AIMBA-I-CRYPTO-1.0` is distinct from `canonicalization_profile_id=RFC8785-JCS-1.0` and `signature_profile_id=AIMBA-ED25519-SHA256-1.0`.
2. The two-stage construction is non-circular: P0 excludes payload_digest; payload_digest is computed over JCS(P0); the final signature projection includes payload_digest.
3. The owner signature, COC quorum attestation and H transport/channel binding are three independent proofs with separate authorities.
4. I's profile applies only to I-authored evidence. C, D, Storage and COC do not inherit I's key authority or key-status lifecycle by sharing the common envelope.
5. The additive schema 1.2.7 field can remain structurally optional for compatibility only if the H semantic validator requires the exact profile IDs for protected I-signed messages and rejects downgrade.
6. Nested I snapshot/receipt/terminal proofs must be dereferenced and verified independently; an outer COC record cannot synthesize I authority.

I 接受以下候选边界：Profile Bundle、Canonicalization Profile 与 Signature Profile 是不同标识；两阶段 Digest/Signature 构造无循环；Owner Signature、COC Quorum Attestation、H Transport Binding 各自独立；I Profile 仅适用于 I 撰写的证据，不继承给 C/D/Storage/COC；Schema 1.2.7 可在结构层保持可选，但受保护 I 消息的 Semantic Validator 必须强制 Profile ID 并拒绝降级；嵌套 I Proof 必须独立解引用验证。

## 3. Blocking amendments / 阻断修订

### I-H-CRYPTO-01 — Exact per-message P0 allowlists

The H mapping defines the projection principle but does not yet enumerate the exact P0 field allowlist for each I-signed object. H must publish exact projections for:
- `OWNER_LOCAL_PENDING_GATE` when `owner_kind=I`;
- `OWNER_LOCAL_GATE_RELEASE` when `owner_kind=I`;
- `JF10_I_TERMINAL_DECISION_OBSERVED`;
- the referenced I owner-snapshot attestation object carried by `owner_snapshot_attestation_ref`;
- any I-signed empty-set or out-of-scope proof used by RecoveryJoin.

A generic "all owner-authored fields" rule is not sufficient for independent implementations.

### I-H-CRYPTO-02 — Stable owner signature reference

If `owner_signature_ref` is included in P0, H must define that it is assigned before signing, immutable, and not derived from the signature bytes. If this cannot be guaranteed, remove it from P0 by an explicit schema-versioned rule and bind the reference in a separate attestation.

### I-H-CRYPTO-03 — Schema and semantic validation split

Schema 1.2.7 adds `signature_profile_id` but leaves it optional structurally. H must add executable semantic checks that:
- require `AIMBA-I-CRYPTO-1.0` bundle resolution, `RFC8785-JCS-1.0` and `AIMBA-ED25519-SHA256-1.0` for I-signed messages;
- reject absent, unknown or mismatched profile IDs;
- reject unknown critical fields and duplicate JSON keys before object materialization;
- verify payload digest and signature using exact P0 allowlists;
- verify referenced I key-status and historical checkpoints.

### I-H-CRYPTO-04 — I key-status and historical trust source

H must call the I-authoritative trust/key-status verification interface and preserve UNKNOWN when it is unavailable. H must not cache a stale ACTIVE state into a later acceptance or infer historical validity from created_at.

### I-H-CRYPTO-05 — Independent implementation vectors

At least two independent implementations must produce byte-identical JCS(P0), payload digest and signature preimage for each I-signed message family. The existing HRC 66/66 candidate pass does not satisfy this requirement.

### I-H-CRYPTO-06 — No cross-owner profile inheritance

H must keep C/D/Storage/COC profile IDs and key-status authorities separate. I's acceptance does not approve their algorithms or key custody.

## 4. Required I security tests / I 安全测试

- I key ACTIVE → RETIRED rotation with historical verification.
- Revocation and compromise effective at exact I sequencer positions.
- Key status unavailable/stale/forked and external anti-rollback anchor unavailable.
- Valid signature under wrong audience, purpose, PolicyDomain, owner boundary or message type.
- Same nonce/same digest idempotency and same nonce/different digest conflict.
- Signature replay against changed artifact/version, D participant, Storage participant, attempt or tuple digest.
- Restore with key-status generation rollback, sequencer gap or missing nonce tombstone.
- Owner signature valid but COC quorum proof invalid, and converse.
- COC quorum record valid but nested I snapshot/terminal proof invalid.

All tests remain **SPECIFIED / NOT RUN** for this exact profile bundle.

## 5. Final I decision / I 最终决议

**ACCEPT WITH ENUMERATED AMENDMENTS** for the candidate composition between I profile Blob `5eeb011032c53c2f7897d699d6f512b26f07d0a2`, H mapping Blob `c30e8ccbecb75b7e27ddceb0cf088afbbb26f562` and H schema Blob `e9748a5b904d2b975e47a32a0cbb31de31636854`.

I does **not** approve production algorithm deployment, trust roots, HSM/KMS ceremony, key rotation intervals, historical trust operation, external anti-rollback anchoring, PolicyDomain sequencer implementation, or TAB-001 freeze. The exact P0 field allowlists and independent implementation vectors remain blocking.

**有条件接受**上述候选组合；但不批准生产算法部署、Trust Root、HSM/KMS 仪式、密钥轮换周期、历史信任运行、外部 Anti-rollback Anchor、PolicyDomain Sequencer 实现或 TAB-001 冻结。精确 P0 字段 Allowlist 和独立实现向量仍是阻断项。
