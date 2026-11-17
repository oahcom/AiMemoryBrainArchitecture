# Phase 3.8.3 — H Wire Mapping for I Cryptographic Profile
# Phase 3.8.3 — H 对 I 密码学配置的 Wire 映射

- Owner: H — BMCP Protocol and Adapter Authentication
- Exact I proposal: `AIMBA-I-CRYPTO-1.0`, Blob `5eeb011032c53c2f7897d699d6f512b26f07d0a2`
- Exact H schema: `bmcp.coc-jf10-unified/1.2.7`, Blob `70b892797d07489936300a26c0dedfafe1d6e746`
- On-wire family version: `schema_version = 1.2.0` (unchanged)
- H decision: **ACCEPT AS WIRE-MAPPING CANDIDATE WITH BLOCKING AMENDMENTS**
- Status: **NOT FROZEN / NOT INTEROPERABILITY-VERIFIED / NOT IMPLEMENTED**
- Provenance: delegated H-role simulation at the user's direction; not an independent human H Owner signature.
- English and Chinese are normative peers.

## 1. H disposition / H 决议

H accepts the I proposal as a candidate cryptographic input and accepts schema artifact 1.2.8 as an additive envelope revision. H does not approve I's algorithm choice, trust roots, key custody, key lifecycle, historical trust or anti-rollback policy. Those remain I/governance decisions.

H accepts the following exact identifiers for the proposed I mapping only:

| Field | Exact value |
|---|---|
| Profile bundle | `AIMBA-I-CRYPTO-1.0` |
| Canonicalization profile | `RFC8785-JCS-1.0` |
| Signature profile | `AIMBA-ED25519-SHA256-1.0` |
| Digest algorithm | `SHA-256` |
| Signature encoding | Base64url without padding |
| JSON canonicalization | RFC 8785 JCS constrained by RFC 7493 I-JSON |

H 将 I 提案接受为候选密码学输入，并接受 Schema Artifact 1.2.7 作为可向后兼容的 Envelope 增量修订。H 不批准 I 的算法选择、Trust Root、Key Custody、Key Lifecycle、历史信任或 Anti-rollback 策略；这些仍由 I/治理决策。

## 2. Schema 1.2.8 exact change / Schema 1.2.7 精确变更

Artifact 1.2.7 adds optional `signature_profile_id` to `$defs.commonEnvelope`. It deliberately keeps the on-wire family `schema_version=1.2.0` unchanged and leaves the new field optional at structural-schema level for compatibility with older message producers.

For protected I-signed records, the semantic validator MUST require all of:
- `canonicalization_profile_id = RFC8785-JCS-1.0`;
- `signature_profile_id = AIMBA-ED25519-SHA256-1.0`;
- `digest_algorithm = SHA-256`;
- `key_id_ref` and immutable `key_version`;
- exact message-family projection and owner authority = I.

Missing `signature_profile_id` is a semantic rejection for a protected I-signed record, even though the additive structural schema can parse a legacy envelope. No downgrade or fallback is permitted.

Artifact 1.2.7 also corrects the stale common-envelope description that referred to artifact revision 1.2.5. The `$id` and title now consistently identify artifact revision 1.2.7. Artifact revision and on-wire family version remain distinct.

Artifact 1.2.7 在 `$defs.commonEnvelope` 增加可选 `signature_profile_id`。为兼容旧消息生产方，Wire Family `schema_version=1.2.0` 保持不变，结构层暂不强制新字段。

但所有受保护的 I 签名记录，Semantic Validator 必须强制要求上述四个精确配置值、Key ID/Version、消息专属 Projection 以及 I Owner Authority。结构 Schema 能解析旧 Envelope，不代表 I 安全语义接受旧 Envelope；缺失 Profile ID 必须拒绝，不得降级。Artifact 1.2.7 同时修正 commonEnvelope 描述中错误引用 1.2.5 的问题。Artifact Revision 与 Wire Family Version 仍是不同概念。

## 3. Owner signature projection / Owner 签名投影

H defines the following deterministic two-stage projection for I-signed records. It is not a generic projection for C, D, Storage or COC signatures.

### 3.1 P0 — owner-authored semantic fields

`P0` contains every immutable owner-authored field defined by the exact message-family schema, including the common envelope identity and trust fields, message-specific payload, typed references, scope, purpose, audience, PolicyDomain, owner generation/high-water/root/count/digest, terminal enum, key ID/version, creation/validity fields and any preassigned stable `owner_signature_ref`.

`P0` excludes:
- `payload_digest` (computed from P0);
- `signature` (the output);
- `integrity_proof_ref` (external proof locator, not semantic content);
- `channel_binding_proof_ref` (transport/session evidence, verified separately);
- coordinator-added fields: `quorum_commit_proof_ref`, `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest`, `coc_previous_entry_digest`.

No other field may be excluded. In particular, `message_nonce`, `audience`, `sender_authority_ref`, `issuer_ref`, `subject_ref`, `owner_authority`, `owner_record_ref`, `policy_domain_ref` when applicable, `canonicalization_profile_id`, `signature_profile_id`, `digest_algorithm`, `key_id_ref`, `key_version` and `created_at` are signed.

### 3.2 Digest and signature construction

1. `P0Bytes = JCS(P0)`.
2. `payload_digest = SHA-256(ASCII("AIMBA-I-PAYLOAD-v1") || 0x00 || P0Bytes)`, lowercase hex.
3. `P = P0 + { payload_digest }`.
4. `PBytes = JCS(P)`.
5. `signature_preimage = ASCII("AIMBA-I-SIGNATURE-v1") || 0x00 || ASCII("AIMBA-I-CRYPTO-1.0") || 0x00 || ASCII(message_type) || 0x00 || PBytes`.
6. `signature = Ed25519.Sign(private_key, signature_preimage)`, Base64url without padding.

The signature and payload digest MUST be recomputed from the exact same P0 projection. A COC commit attestation is verified independently over the coordinator's exact committed record/position and is not inserted into P0 after owner signing.

### 3.3 Nested owner snapshots and referenced proofs

For `COC_RECOVERY_CUTOFF_BATCH` and `PARTICIPANT_SET_RECONCILIATION`, the COC record is not I-signed merely because it contains an I snapshot. The validator MUST dereference `owner_snapshots.I.owner_snapshot_attestation_ref` and verify the I-signed snapshot under the I profile, then independently verify the COC quorum commitment.

Likewise, an I proof referenced by `JF10_BRIDGE_RECONCILIATION_RECORDED` is verified as its own immutable I-signed object. The outer COC record cannot alter, replace or synthesize the I proof.

P0 包含精确 Message Family Schema 定义的所有不可变 Owner-authored 字段，包括 Common Envelope 身份/Trust 字段、消息 Payload、Typed Ref、Scope/Purpose/Audience、PolicyDomain、Owner Generation/High-water/Root/Count/Digest、Terminal Enum、Key ID/Version、时间字段及预先分配的稳定 `owner_signature_ref`。

P0 仅排除 Payload Digest（由 P0 计算）、Signature 输出、外部 Integrity Proof Locator、Transport Channel-binding Evidence，以及签名后由 Coordinator 添加的 Quorum/COC Commit Position/Record/Digest 字段。除此之外不得排除任何字段。Nonce、Audience、Issuer/Subject、Owner Authority、Owner Record Ref、Profile ID、Key ID/Version 等必须签名。

COC Recovery Cutoff Batch 即使包含 I Snapshot，也不因此变成 I 签名记录。Validator 必须独立解引用并验证 I Snapshot Attestation，再独立验证 COC Quorum Commit。JF10 Bridge Reconciliation 中引用的 I Proof 也必须作为独立不可变 I 对象验证；外层 COC Record 不能替换或合成 I Proof。

## 4. Exact I-signed field allowlists / I 签名字段精确 Allowlist

The common I-signed projection fields are exactly:
`schema_id`, `schema_version`, `message_type`, `message_id`, `message_nonce`, `audience`, `sender_authority_ref`, `sender_subject_ref`, `issuer_ref`, `subject_ref`, `owner_authority`, `owner_record_ref`, `policy_domain_ref` when present/applicable, `causal_order_profile_ref`, `causal_order_coordinator_ref`, `causal_order_domain_ref`, `canonicalization_profile_id`, `signature_profile_id`, `digest_algorithm`, `key_id_ref`, `key_version`, and `created_at`.

The common exclusions are exactly `payload_digest`, `signature`, `integrity_proof_ref`, `channel_binding_proof_ref`, `quorum_commit_proof_ref`, `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest`, and `coc_previous_entry_digest`. No other field is excluded.

| I-signed object | Additional fields included in P0 | Required semantic discriminator |
|---|---|---|
| `OWNER_LOCAL_PENDING_GATE` | `owner_kind`, `owner_gate_ref`, `owner_gate_generation`, `request_set_count`, `request_set_digest`, `owner_request_high_water`, `snapshot_generation`, `anti_rollback_anchor_ref`, `owner_signature_ref`, `owner_admission_high_water`, `admission_set_count`, `admission_set_digest`, `request_ledger_root`, `admission_ledger_root` | `owner_kind=I` and `owner_authority=I` |
| `OWNER_LOCAL_GATE_RELEASE` | `owner_kind`, `release_type`, `owner_gate_ref`, `owner_gate_generation`, `recovery_epoch_ref`, `batch_record_ref`, `batch_digest`, `manifest_record_ref`, `manifest_digest`, `owner_request_high_water`, `reconciliation_root`, `owner_signature_ref`, `owner_admission_high_water`, `request_set_digest`, `admission_set_digest`, `request_ledger_root`, `admission_ledger_root`, `batch_position`, `batch_entry_digest`, `manifest_record_position`, `manifest_record_entry_digest` | `owner_kind=I`, `owner_authority=I`, release type is the exact I outage-admission release enum |
| `JF10_I_TERMINAL_DECISION_OBSERVED` | `i_terminal_outcome`, `i_terminal_decision_ref`, `i_sequencer_position`, `commit_authorization_receipt_ref`, `receipt_digest`, `receipt_consumption_proof_ref`, `prepared_participant_ref`, `prepared_transaction_gid`, `database_incarnation_ref`, `prepare_attempt_ref`, `prepare_attempt_generation`, `participant_ledger_ref`, `participant_ledger_version`, `participant_tuple_digest`, `owner_signature_ref` | `owner_authority=I`; terminal enum and same-XID tuple are checked by I semantics |
| I owner snapshot attestation referenced by `owner_snapshot_attestation_ref` | Resolve to the exact immutable I `OWNER_LOCAL_PENDING_GATE`/snapshot attestation record and compare all owner, gate, scope, generation, high-water, count, root, digest and anti-rollback fields | The referenced record must be I-signed and its digest/ref must match the nested COC snapshot |

For the snapshot reference, H must not treat the nested `ownerSnapshot` JSON object as an I signature. The I-signed source object is dereferenced and verified separately. Empty-set and out-of-scope assertions are accepted only when carried by an exact I-signed evidence object whose schema and projection are explicitly pinned; absent or partial evidence remains UNKNOWN.

### 4.1 Owner snapshot attestation binding / Owner Snapshot Attestation 绑定

Schema 1.2.8 adds `owner_snapshot_attestation_digest`. H semantic validation must dereference `owner_snapshot_attestation_ref`, verify the I signature, recompute the referenced immutable object's SHA-256 digest and compare it to this field, then compare owner, gate/scope generation, request/admission high-waters, counts, roots, inventory epoch and anti-rollback anchor to the COC-embedded `ownerSnapshot`. Missing digest, mutable locator, mismatch or unavailable object returns UNKNOWN/INVALID and keeps the recovery gate closed.

### 4.2 COMPLETE_EMPTY and OUT_OF_SCOPE proof schemas / 空集合与范围外证明 Schema

RecoveryJoin schema 1.0.1 defines two separately dereferenced proof objects:

- `$defs.completeEmptyProof`: binds owner authority, REQUEST_SET/ADMISSION_SET, Scope/ScopeGeneration, exact owner ledger/version, ledger query ref, owner-local high-water, `pagination_complete=true`, `count=0`, canonical empty root, key-status generation, anti-rollback anchor, signature profile/ref and proof digest.
- `$defs.outOfScopeProof`: binds exact request/operation identity and digest, target class, Scope/ScopeGeneration, applicability policy, `OUT_OF_SCOPE_WITH_PROOF` decision, reason code, owner ledger/version/high-water, complete query/pagination, key-status generation, anti-rollback anchor, signature profile/ref and proof digest.

For an I proof, `signature_profile_ref` MUST resolve to `AIMBA-ED25519-SHA256-1.0` under bundle `AIMBA-I-CRYPTO-1.0`; the resolved proof is verified with the exact I P0/JCS/Ed25519 construction. A zero count without its matching signed empty proof is UNKNOWN. An OUT_OF_SCOPE disposition without its exact signed proof ref+digest is UNKNOWN. No missing or unavailable evidence is interpreted as empty or out-of-scope.

RecoveryJoin Schema 1.0.1 新增两个独立解引用 Proof Object：
- `completeEmptyProof` 绑定 Owner、Request/Admission Set、Scope/Generation、Owner Ledger/Version、Query Ref、Owner High-water、完整分页、Count=0、Canonical Empty Root、Key Status Generation、Anti-rollback Anchor、Signature Profile/Ref 和 Proof Digest。
- `outOfScopeProof` 绑定 Request/Operation Identity/Digest、Target Class、Scope/Generation、Applicability Policy、OUT_OF_SCOPE 决策、Reason、Owner Ledger/Version/High-water、完整 Query/Pagination、Key Status、Anti-rollback、Signature Profile/Ref 和 Proof Digest。

I Proof 的 `signature_profile_ref` 必须解析到 `AIMBA-ED25519-SHA256-1.0` 与 Bundle `AIMBA-I-CRYPTO-1.0`，并按 I 精确 P0/JCS/Ed25519 规则验签。Count=0 但缺少匹配签名 Empty Proof，或 OUT_OF_SCOPE 缺少精确签名 Proof Ref+Digest，均为 UNKNOWN。缺失/不可用证据绝不能解释为空或范围外。

## 5. Message-family authority mapping / 消息族 Authority 映射

| Message family | Record authority | I profile application |
|---|---|---|
| `COC_RECOVERY_CUTOFF_BATCH` | COC | Verify nested I snapshot attestation separately; verify COC quorum proof separately |
| `PARTICIPANT_SET_RECONCILIATION` | COC | Verify referenced I evidence separately; outer record is not I-signed |
| `OWNER_LOCAL_PENDING_GATE` | `owner_kind` | Apply I profile only when `owner_kind=I`; otherwise use that owner's approved profile |
| `OWNER_LOCAL_GATE_RELEASE` | `owner_kind` | Apply I profile only when `owner_kind=I`; otherwise use that owner's approved profile |
| `RECOVERY_EPOCH_COMPLETED` | COC | COC attestation only; no I authority inference |
| `JF10_PREPARE_INTENT_REGISTERED` | Exact declared owner | Apply I profile only if the signed subrecord is I-authored; do not infer from the message name |
| `JF10_PREPARED_PARTICIPANT_REGISTERED` | Storage | Storage-owned signature/trust profile |
| `JF10_I_TERMINAL_DECISION_OBSERVED` | I | **I profile required** |
| `JF10_STORAGE_PARTICIPANT_RESOLVED` | Storage | Storage-owned signature/trust profile |
| `JF10_BRIDGE_RECONCILIATION_RECORDED` | COC | Verify referenced I/D/C/Storage evidence independently |
| `C_PROVIDER_OUTCOME_RECORDED` | C | C-owned signature/trust profile; provider truth remains C-owned |

The profile MUST NOT be applied to C/D/Storage/COC signatures merely because those records share the common envelope. Each authority must publish its own approved profile or explicitly reference a jointly approved profile without surrendering its key-status authority.

该配置只应用于 I 撰写的记录。C/D/Storage/COC 记录即使共用 Common Envelope，也不得自动套用 I Profile。各 Authority 必须发布自己的批准配置，或明确引用经联合批准的配置，同时保留自己的 Key Status Authority。

## 7. Required H validator behavior / H Validator 强制行为

H semantic validation MUST:

1. Select the profile from authenticated owner authority and exact `signature_profile_id`; never from an untrusted algorithm hint.
2. Enforce duplicate-key rejection before JSON object construction.
3. Reconstruct P0 using the exact message-family allowlist; reject unknown critical fields and ambiguous projection.
4. Recompute payload digest and signature preimage byte-for-byte.
5. Validate Base64url canonical encoding and Ed25519 signature length/verification.
6. Dereference and verify nested I snapshot/receipt/terminal proofs under current and historical I key-status evidence.
7. Keep transport channel-binding and COC quorum verification as independent checks.
8. Return UNKNOWN and block the dependent gate if I key status, historical checkpoint, anti-rollback anchor or referenced proof is unavailable/stale.
9. Reject profile downgrade, key-version substitution, cross-audience replay and message-family substitution.
10. Never treat JSON Schema success as signature, trust, currentness or owner-authority success.

H Semantic Validator 必须按认证 Owner Authority 与精确 Profile ID 选择配置；在构造 JSON Object 前拒绝重复 Key；按消息类型精确 Allowlist 重建 P0；重新计算 Digest/Signature Preimage；验证 Base64url 与 Ed25519；独立验证嵌套 I Proof、Transport Channel Binding 和 COC Quorum；Key Status/历史 Checkpoint/Anti-rollback/Proof 不可用时返回 UNKNOWN 并阻断 Gate；拒绝 Profile 降级、Key Version 替换、跨 Audience Replay 和 Message Family 替换。JSON Schema 通过不等于签名、Trust、Currentness 或 Owner Authority 通过。

## 8. Required exact vectors / 精确测试向量

H must extend the candidate suite with:
- exact P0 extraction for all I-signed message families;
- payload digest excludes only itself and uses the specified domain tag;
- signature preimage includes bundle ID and message type;
- coordinator-added COC fields do not mutate the owner signature but must pass independent quorum verification;
- modified I payload, audience, nonce, key version, owner authority or participant tuple fails verification;
- nested I snapshot reference substitution fails;
- COC outer record with valid quorum proof but invalid nested I signature is rejected;
- valid I signature with stale/revoked/compromised key status returns UNKNOWN/REJECT according to the I ledger boundary;
- missing `signature_profile_id` is structurally parseable only where compatibility permits, but semantically rejected for I protected records;
- two independent implementations produce identical P0 bytes, payload digest and signature preimage.

These vectors are **SPECIFIED / NOT RUN**. The existing HRC/JPF/WIRE/SCHEMA 66/66 result remains a separate test-only candidate result and does not cover this profile mapping.

上述向量目前均为**已定义、未执行**。现有 HRC/JPF/WIRE/SCHEMA 66/66 仍是独立的 Test-only Candidate 结果，不覆盖本 Profile Mapping。

## 9. Blocking amendments / 阻断修订

1. I must issue an exact-version decision on Blob `30967b2c58ef0aaf760a22fe61192e70744d5964`, including algorithm/regulatory suitability and the exact P0 trust semantics.
2. H must publish a separate exact-version decision for schema 1.2.7 Blob `e9748a5b904d2b975e47a32a0cbb31de31636854` and this mapping revision; this document is the H candidate mapping decision, not a second independent signature.
3. I/H must resolve the owner snapshot attestation digest binding and confirm the exact P0 allowlists above against the final schema artifact.
4. At least two independent canonicalization/signature implementations and byte-for-byte vectors must pass.
5. I must approve trust-root/key custody/rotation/compromise/anti-rollback operations and the external checkpoint mechanism.
6. Storage must accept the exact proof-verification contract for its actual visibility linearization point.
7. No profile is production-active until independent human Owner/governance approval and runtime conformance are recorded.

## 10. Final H decision / H 最终决议

I exact review of this mapping: Blob `446109f4867268fe7dca3c7e114346f3c1a74b61` — **ACCEPT WITH ENUMERATED AMENDMENTS**.

**ACCEPT AS WIRE-MAPPING CANDIDATE WITH BLOCKING AMENDMENTS.**

H accepts the additive schema envelope field and the separation between owner signature, COC quorum attestation and transport channel binding. H does not approve I's cryptographic policy or any other owner's signature profile. The projection and vectors remain candidate until the exact I/H decisions and independent implementations are complete.

**作为 Wire Mapping 候选接受，但保留阻断修订。** H 接受新增 Envelope 字段，以及 Owner Signature、COC Quorum Attestation、Transport Channel Binding 的分离。H 不批准 I 的密码学策略或其他 Owner 的签名配置。精确 Projection、独立实现与 I/H 决议完成前，不得冻结或生产启用。
