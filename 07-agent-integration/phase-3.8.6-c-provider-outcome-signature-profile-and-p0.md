# Phase 3.8.6 — C Provider Outcome Signature Profile and Exact P0 Projection
# Phase 3.8.6 — C Provider Outcome 签名配置与精确 P0 投影

- Owner: C — Agent Integration / Provider Outcome
- Branch: `session-c-agent-integration-2026-11-16`
- Applies to: C-authored `CSubmitOutcome` and `C_PROVIDER_OUTCOME_RECORDED` only.
- Exact H schema target: unified 1.2.8, Blob `70b892797d07489936300a26c0dedfafe1d6e746`.
- Exact C semantic source: `phase-3.8.4-c-normative-provider-submit-outcome-contract.md`, Blob `819705037da89834e10b6dd2ec6e66c1b8c70886`.
- Status: **C-OWNED CRYPTO PROFILE CANDIDATE — NOT APPROVED / NOT FROZEN / NOT IMPLEMENTED**
- English and Chinese are normative peers.

## 1. Profile identifiers / 配置标识

| Concern | Exact candidate value |
|---|---|
| Profile bundle | `AIMBA-C-OUTCOME-CRYPTO-1.0` |
| Canonicalization profile | `RFC8785-JCS-1.0` |
| Signature profile | `AIMBA-C-ED25519-SHA256-1.0` |
| Digest | `SHA-256` |
| Signature | `Ed25519 / RFC 8032` |
| Signature encoding | Base64url without padding |
| Canonical JSON | RFC 8785 JCS constrained by RFC 7493 I-JSON |
| Payload domain tag | ASCII `AIMBA-C-OUTCOME-PAYLOAD-v1` |
| Signature domain tag | ASCII `AIMBA-C-OUTCOME-SIGNATURE-v1` |

This is a C-owned profile identifier and semantic projection. It deliberately does **not** reuse I's profile bundle `AIMBA-I-CRYPTO-1.0` or signature profile `AIMBA-ED25519-SHA256-1.0`, even though the candidate primitive suite is the same. The owner authority, message projection, domain separation and key-status binding remain distinct.

这是 C 自有的配置标识和语义投影。即使候选基础算法相同，也**不复用** I 的 `AIMBA-I-CRYPTO-1.0` Bundle 或 `AIMBA-ED25519-SHA256-1.0` Signature Profile。Owner Authority、消息投影、Domain Separation 和 Key Status Binding 均保持独立。

## 2. C outcome semantic digest / C Outcome 语义摘要

Define `CO0` as the C-owned semantic body of one CSubmitOutcome, containing every present C message field listed in §3, except:
- `c_submit_outcome_digest` itself;
- the common envelope fields;
- the coordinator-appended COC proof fields `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest`.

Then:

`CSubmitOutcomeDigest = SHA-256(ASCII("AIMBA-C-OUTCOME-PAYLOAD-v1") || 0x00 || JCS(CO0))`

The digest is lowercase 64-character hexadecimal. The digest binds the immutable provider outcome body, including outcome enum, request digest, provider identity/key, owner admission, participant tuple and provider evidence references. Absent, null, empty string, empty array and empty object remain distinct. No defaulting, coercion or field dropping is permitted.

`CSubmitOutcomeDigest` is not the H common-envelope `payload_digest`. The former identifies the C semantic outcome body; the latter is computed over the complete signed P0 projection in §3. This distinction avoids digest self-reference and permits the same C semantic outcome to be carried by a versioned envelope only under an explicit compatibility rule.

`CSubmitOutcomeDigest` 是 C 语义 Outcome Body 的摘要，不等于 H Common Envelope 的 `payload_digest`。前者标识 C 语义结果，后者覆盖完整签名 P0 投影。两者严格区分，避免摘要自引用。

## 3. Exact signed P0 allowlist / 精确签名 P0 白名单

The signed P0 is the exact `C_PROVIDER_OUTCOME_RECORDED` message projection, with the following allowlist.

### 3.1 Common envelope fields included in P0

Include every present field from this exact list:
- `schema_id`, `schema_version`, `message_type`, `message_id`, `message_nonce`, `audience`;
- `sender_authority_ref`, `sender_subject_ref`, `issuer_ref`, `subject_ref`, `owner_authority`, `owner_record_ref`;
- `policy_domain_ref` when applicable;
- `causal_order_profile_ref`, `causal_order_coordinator_ref`, `causal_order_domain_ref`;
- `canonicalization_profile_id`, `signature_profile_id`, `digest_algorithm`;
- `key_id_ref`, `key_version`, `created_at`, `owner_signature_ref`.

### 3.2 C outcome fields included in P0

Include every present field from this exact list:
- `c_submit_outcome_ref`, `c_submit_outcome_digest`, `provider_outcome`;
- `provider_ref`, `provider_adapter_ref`, `provider_idempotency_key_ref`;
- `provider_request_ref`, `provider_receipt_ref`, `actual_inference_request_id`;
- `final_request_boundary_id`, `request_digest`, `transaction_ref`;
- `participant_reservation_ref`, `participant_intent_ref`, `prepared_participant_ref`;
- `prepare_attempt_ref`, `prepare_attempt_generation`, `participant_ledger_ref`, `participant_ledger_version`, `participant_tuple_digest`;
- `i_terminal_decision_ref`, `d_clearance_ref`, `storage_resolution_proof_ref`;
- `provider_outcome_evidence_ref`, `provider_lookup_proof_ref`;
- `provider_no_handoff_proof_ref`, `not_invoked_proof_ref`, `unknown_reason_ref`;
- `owner_admission_ref`, `owner_admission_digest`, `owner_ledger_ref`, `owner_ledger_version`, `owner_local_sequence`, `owner_high_water`, `owner_ledger_root`;
- `coc_participant_intent_ref`, `coc_absence_reason` (the null-vs-string distinction is signed).

### 3.3 Exact exclusions from P0

Exclude only:
- `payload_digest` (computed over P0);
- `signature` (signature output);
- `integrity_proof_ref` (external proof locator, verified independently);
- `channel_binding_proof_ref` (transport/session proof, verified independently);
- `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest` (COC-appended quorum/record evidence, verified independently).

No other field may be excluded. Unknown critical fields, duplicate JSON keys, schema ambiguity or projection mismatch are rejected. COC fields are excluded from the C owner signature because C signs its immutable outcome before the coordinator appends its independent record/quorum attestation; the COC proof does not alter C's signed semantic truth.

不得排除其他字段。未知 Critical Field、重复 JSON Key、Schema 歧义或投影不一致必须拒绝。COC Proof 字段从 C Owner Signature 排除，是因为 C 先签署不可变 Outcome，随后 Coordinator 追加独立 Record/Quorum Attestation；COC Proof 不得改变 C 已签署的语义事实。

## 4. Two-stage payload/signature construction / 两阶段摘要与签名构造

1. Construct exact P0 from §3.
2. `P0Bytes = JCS(P0)`.
3. `payload_digest = SHA-256(ASCII("AIMBA-C-OUTCOME-PAYLOAD-v1") || 0x00 || P0Bytes)`, lowercase hex.
4. `P = P0 + { payload_digest }`.
5. `PBytes = JCS(P)`.
6. `signature_preimage = ASCII("AIMBA-C-OUTCOME-SIGNATURE-v1") || 0x00 || ASCII("AIMBA-C-OUTCOME-CRYPTO-1.0") || 0x00 || ASCII("C_PROVIDER_OUTCOME_RECORDED") || 0x00 || PBytes`.
7. `signature = Ed25519.Sign(C_private_key, signature_preimage)`.
8. Encode signature as canonical Base64url without padding.

`owner_signature_ref` MUST be allocated before signing, immutable and not derived from signature bytes. `coc_commit_proof_ref` and related COC fields are attached after C signing and are checked through COC quorum verification, not C's owner signature.

## 5. Trust and authority / Trust 与权威

- C owns the meaning and signed P0 projection of its Provider Outcome.
- I's authoritative trust registry resolves the authenticated C issuer/owner identity and key status/historical checkpoint; I does not create or rewrite C outcome.
- C's profile bundle and signature profile are separate typed references; H must reject missing/unknown/wrong-owner/wrong-audience/downgraded profile.
- H validates wire structure, canonicalization and signature projection; G validates Applied semantics; Storage/COC validate their own independent proofs.
- A valid C signature proves only that the trusted C authority signed this outcome. Provider truth still requires the C-defined authoritative provider evidence class.

## 6. L3 vector obligations / L3 向量义务

At minimum, create two independent implementations (Python and Node.js or equivalent) and compare byte-for-byte:
- exact P0 extraction with all optional-field combinations;
- JCS P0 bytes and payload digest;
- final signature preimage;
- Ed25519 verification;
- null vs absent COC intent;
- same outcome digest vs envelope payload digest distinction;
- changed request digest, provider key, participant tuple, audience, message type, key version and owner authority must fail;
- COC proof append must not change the owner P0/signature, while invalid COC quorum must still fail overall verification;
- duplicate keys, non-I-JSON, invalid UTF-8, NaN/Infinity and noncanonical Base64url must reject.

Existing H 101/101 CI covers the I candidate profile fixed-vector path only. It does not establish these C-specific vectors.

## 7. Decision boundary / 决策边界

**C decision:** adopt the above as the C-owned cryptographic profile candidate and exact C outcome P0 definition for review.

**Not approved:** production cryptographic algorithm suitability, trust root, key custody, HSM/KMS, rotation/revocation deployment, historical key archive, anti-rollback anchor, provider-specific evidence adapters, production signatures or runtime conformance.

**C 决议：** 将上述配置作为 C 自有密码学候选，并将精确 C Outcome P0 定义为后续审查基线。

**尚未批准：** 生产算法适用性、Trust Root、Key Custody、HSM/KMS、轮换/撤销部署、历史 Key Archive、Anti-rollback Anchor、Provider 证据 Adapter、生产签名或运行时符合性。
