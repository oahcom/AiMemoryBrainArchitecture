# Phase 3.8.7 — I Exact Signed-Object P0 Allowlists and Attestation Contracts
# Phase 3.8.7 — I 精确签名对象 P0 白名单与证明合同

- Owner: I — Security, Identity and Governance
- Branch: `session-i-security-governance-2026-11-16`
- Profile candidate: `AIMBA-I-CRYPTO-1.0`, Blob `5eeb011032c53c2f7897d699d6f512b26f07d0a2`
- H unified schema 1.2.8: Blob `70b892797d07489936300a26c0dedfafe1d6e746`
- H RecoveryJoin schema 1.0.1: Blob `f94e01cf30b4c59fca24cb4ccd8b76a0db8ca95c`
- Status: **I-OWNED NORMATIVE P0 PROJECTION CANDIDATE — EXACT FIELDS DEFINED; PROFILE/PRODUCTION APPROVAL SEPARATE**
- English and Chinese are normative peers.

## 1. Purpose / 目的

This addendum closes the previously open I-H-CRYPTO-01 requirement by defining exact per-message signed projections. It supersedes the generic phrase “all owner-authored semantic fields” for the exact message families below.

本补充通过定义逐消息签名投影，关闭此前 I-H-CRYPTO-01 的字段白名单缺口。对于下列精确消息族，本文件取代“所有 Owner-authored Semantic Fields”这种泛化表述。

## 2. Common I-signed P0 envelope / I 签名对象通用 P0 Envelope

For the BMCP message families in §§3.1–3.3 only, the common P0 envelope includes every present field from this exact allowlist. The referenced proof objects in §§4–6 (IOwnerSnapshotAttestation, ICompleteEmptyProof, IOutOfScopeProof, ICommitAuthorizationReceipt and ITerminalProof) are standalone I-signed proof objects and use only their own exact P0 field lists; they do not inherit BMCP common-envelope fields unless a future exact schema version explicitly wraps them in such an envelope.

- `schema_id`
- `schema_version`
- `message_type`
- `message_id`
- `message_nonce`
- `audience`
- `sender_authority_ref`
- `sender_subject_ref`
- `issuer_ref`
- `subject_ref`
- `owner_authority`
- `owner_record_ref`
- `policy_domain_ref` when applicable
- `causal_order_profile_ref`
- `causal_order_coordinator_ref`
- `causal_order_domain_ref`
- `canonicalization_profile_id`
- `signature_profile_id`
- `digest_algorithm`
- `key_id_ref`
- `key_version`
- `created_at`
- `owner_signature_ref` when the message family uses the common owner signature reference

Common exclusions for the BMCP message families in §§3.1–3.3:
- `payload_digest` (computed from P0);
- `signature` (signature output);
- `integrity_proof_ref` and `channel_binding_proof_ref` (external integrity/transport locators verified separately);
- `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest`, `coc_previous_entry_digest` (COC-appended quorum/record evidence verified independently).

No other common field may be excluded. In particular, message ID, nonce, audience, sender/issuer/subject, owner authority, owner record, PolicyDomain, causal-order profile/coordinator/domain, canonicalization/signature profile, digest algorithm, key ID/version, creation time and stable owner_signature_ref are signed.

所有 I 签名对象均使用以上通用 P0 字段白名单。不得排除其他通用字段。COC 追加的 Quorum/Record 证据由 COC 独立验证，不改变 Owner 已签署的语义投影。

## 3. Exact message-family projections / 精确消息族投影

### 3.1 `OWNER_LOCAL_PENDING_GATE` when `owner_kind=I`

P0 = common envelope + exactly these message-specific fields:
- `owner_kind` (must equal `I`);
- `owner_gate_ref`;
- `owner_gate_generation`;
- `request_set_count`;
- `request_set_digest`;
- `owner_request_high_water`;
- `snapshot_generation`;
- `anti_rollback_anchor_ref`;
- `owner_admission_high_water`;
- `admission_set_count`;
- `admission_set_digest`;
- `request_ledger_root`;
- `admission_ledger_root`.

The four COC fields listed in §2 exclusions are not in P0.

### 3.2 `OWNER_LOCAL_GATE_RELEASE` when `owner_kind=I`

P0 = common envelope + exactly:
- `owner_kind` (must equal `I`);
- `release_type`;
- `owner_gate_ref`;
- `owner_gate_generation`;
- `recovery_epoch_ref`;
- `batch_record_ref`;
- `batch_digest`;
- `manifest_record_ref`;
- `manifest_digest`;
- `owner_request_high_water`;
- `reconciliation_root`;
- `owner_admission_high_water`;
- `request_set_digest`;
- `admission_set_digest`;
- `request_ledger_root`;
- `admission_ledger_root`;
- `batch_position`;
- `batch_entry_digest`;
- `manifest_record_position`;
- `manifest_record_entry_digest`.

The four COC fields listed in §2 exclusions are not in P0.

### 3.3 `JF10_I_TERMINAL_DECISION_OBSERVED`

P0 = common envelope + exactly:
- `i_terminal_outcome`;
- `i_terminal_decision_ref`;
- `i_sequencer_position`;
- `commit_authorization_receipt_ref`;
- `receipt_digest`;
- `receipt_consumption_proof_ref`;
- `prepared_participant_ref`;
- `prepared_transaction_gid`;
- `database_incarnation_ref`;
- `prepare_attempt_ref`;
- `prepare_attempt_generation`;
- `participant_ledger_ref`;
- `participant_ledger_version`;
- `participant_tuple_digest`;
- stable `owner_signature_ref`.

The four COC fields listed in §2 exclusions are not in P0.

## 4. Referenced I owner snapshot attestation / I Owner Snapshot Attestation 引用对象

The H 1.2.8 `ownerSnapshot` object is a COC-carried summary. It is **not itself the I signature object**. Its `owner_snapshot_attestation_ref` and `owner_snapshot_attestation_digest` point to the separate I-signed object `IOwnerSnapshotAttestation/1.0`.

The I-signed attestation P0 contains exactly:
- `attestation_ref`;
- `owner_authority_ref` (must be I);
- `snapshot_ref`;
- `snapshot_digest` (digest of the underlying I ledger snapshot, not this attestation);
- `request_high_water`, `request_count`, `request_set_digest`, `request_ledger_root`;
- `admission_high_water`, `admission_count`, `admission_set_digest`, `admission_ledger_root`;
- `owner_ledger_root`;
- `owner_specific_high_waters` containing exactly `receipt_issue_high_water`, `receipt_consume_high_water`, `inventory_epoch_ref`, `registry_snapshot_digest`, `relevant_entry_set_root`;
- `gate_ref`, `gate_generation`, `scope_generation`;
- `anti_rollback_anchor_ref`;
- `request_enumeration_status`, `admission_enumeration_status`;
- `request_ledger_query_ref`, `request_pagination_complete`;
- `admission_ledger_query_ref`, `admission_pagination_complete`;
- `key_status_generation`;
- `request_complete_empty_proof_ref`, `admission_complete_empty_proof_ref`;
- `inventory_epoch_ref`, `registry_snapshot_digest`, `relevant_entry_set_root`;
- `signature_profile_ref`, stable `signature_ref`, `issued_at`.

The outer `owner_snapshot_attestation_digest` equals the digest of this signed attestation projection and is not included inside itself. The attestation's `snapshot_digest` is distinct: it commits to the underlying owner-ledger snapshot. The COC summary fields MUST exactly match the corresponding signed attestation fields; mismatch is a hard rejection.

H 1.2.8 的 `ownerSnapshot` 是 COC 携带的摘要，不是 I 签名对象本身。其 `owner_snapshot_attestation_ref` 和 `owner_snapshot_attestation_digest` 指向独立 I 签名对象 `IOwnerSnapshotAttestation/1.0`。上列字段构成该对象精确 P0。外层 Attestation Digest 不得包含自身；底层 Snapshot Digest 与 Attestation Digest 是不同摘要。COC 摘要必须与签名 Attestation 对应字段完全一致。

## 5. I RecoveryJoin proof projections / I RecoveryJoin 证明投影

### 5.1 `ICompleteEmptyProof/1.0`

P0 = exactly:
- `proof_ref`;
- `owner_authority_ref` (must be I);
- `set_kind`;
- `scope_ref`;
- `scope_generation`;
- `owner_ledger_ref`;
- `owner_ledger_version`;
- `ledger_query_ref`;
- `owner_high_water`;
- `pagination_complete`;
- `count`;
- `canonical_empty_root`;
- `key_status_generation`;
- `anti_rollback_anchor_ref`;
- `signature_profile_ref`;
- stable `signature_ref`;
- `issued_at`.

Exclude only `proof_digest` from P0; compute it as SHA-256 over the domain-separated JCS(P0). The signature projection includes P0 plus `proof_digest`.

### 5.2 `IOutOfScopeProof/1.0`

P0 = exactly:
- `proof_ref`;
- `owner_authority_ref` (must be I);
- `request_ref`;
- `operation_identity_ref`;
- `operation_digest`;
- `target_class_ref`;
- `scope_ref`;
- `scope_generation`;
- `applicability_policy_ref`;
- `decision`;
- `reason_code`;
- `owner_ledger_ref`;
- `owner_ledger_version`;
- `owner_high_water`;
- `ledger_query_ref`;
- `pagination_complete`;
- `key_status_generation`;
- `anti_rollback_anchor_ref`;
- `signature_profile_ref`;
- stable `signature_ref`;
- `issued_at`.

Exclude only `proof_digest` from P0; compute it as SHA-256 over the domain-separated JCS(P0). The signature projection includes P0 plus `proof_digest`.

The RecoveryJoin schema's `ownerEvidence` and `ownerSnapshot` wrappers are references/summaries. They are not a substitute for dereferencing and verifying these exact I-signed proof objects.

## 6. CommitAuthorizationReceipt and ITerminalProof / 授权 Receipt 与 Terminal Proof

### 6.1 `ICommitAuthorizationReceipt/1.0`

The exact P0 contains:
- `authorization_receipt_ref`, `nonce`;
- `policy_domain_ref`, `policy_version`, `permission_epoch`;
- `issuer_ref`, `issuer_key_id_ref`, `issuer_key_version`, `issuer_key_status_ref`;
- `principal_ref`, `actor_ref`, `workload_ref`, `delegation_chain_digest`;
- `action`, `resource_ref`, `resource_version`, `resource_content_digest`;
- `purpose`, `audience`, `scope_binding_set_digest`, `environment_ref`;
- `owner_boundary`, `final_visibility_gate_ref`;
- `publication_operation_id`, `publication_tuple_digest`;
- exact `d_publication_participant_ref`, exact `storage_visibility_participant_ref`;
- `sequencer_position`, `consumption_result`;
- `issued_at`, `consumed_at`, `first_consumption_accept_before` when used;
- `canonicalization_profile_id`, `signature_profile_id`, `digest_algorithm`, `key_id_ref`, `key_version`, stable `owner_signature_ref`.

The consumption result is sequencer-generated. It is not caller-selectable. Only COMMIT_WON can be a pre-commit proof for Storage visibility.

### 6.2 `ITerminalProof/1.0`

The exact P0 contains:
- `terminal_proof_ref`;
- `authorization_receipt_ref`, `receipt_digest`;
- `policy_domain_ref`, `permission_epoch`;
- `publication_operation_id`, `publication_tuple_digest`;
- exact `d_publication_participant_ref`, exact `storage_visibility_participant_ref`;
- `storage_outcome` (COMMITTED_VISIBLE or NO_PUBLICATION only);
- `storage_outcome_digest`, `storage_authority_ref`, `storage_incarnation_ref`;
- `i_terminal_sequencer_position`;
- `key_status_generation`, `anti_rollback_anchor_ref`;
- `issued_at`, `canonicalization_profile_id`, `signature_profile_id`, `digest_algorithm`, `key_id_ref`, `key_version`, stable `owner_signature_ref`.

UNKNOWN/IN_DOUBT MUST NOT produce ITerminalProof. ITerminalProof is post-Storage-outcome closeout evidence and is never a precondition to the Storage commit that creates that outcome.

## 7. Deterministic projection algorithm / 确定性投影算法

For each object family:
1. Validate exact schema/version and owner authority.
2. Reject duplicate JSON keys before object materialization; decode UTF-8 strictly; reject non-I-JSON.
3. Select the exact family P0 allowlist in §§3–6. Reject unknown critical fields and any unlisted field unless the exact schema version explicitly adds it through a reviewed successor projection.
4. Construct P0 without mutating source bytes or normalizing Unicode.
5. Compute domain-separated SHA-256 digest over JCS(P0).
6. Add digest to the final signature projection and compute the Ed25519 preimage under `AIMBA-I-CRYPTO-1.0` and exact message type.
7. Verify signature and then dereference nested proofs and current/historical key status separately.
8. Verify COC quorum proof independently; COC-appended fields are not part of I P0.
9. Any missing, unknown, stale, forked or mismatched authority/proof returns UNKNOWN and blocks the dependent gate.

## 8. Exact exclusions and anti-circularity / 精确排除与反循环

- `payload_digest`, `proof_digest` and any attestation digest are never included in the P0 value from which they are computed.
- `signature` bytes are never included in their own preimage.
- `owner_signature_ref` / `signature_ref` are allocated before signing and are not derived from signature bytes.
- COC record/quorum fields are appended after owner signing and verified independently.
- A referenced snapshot digest never equals its attestation digest by implication; they identify different objects.

## 9. L3 proof obligations / L3 证明义务

The exact P0 projections require at least two independent implementations to produce byte-identical JCS(P0), digest and signature preimage for every family above. Negative vectors must mutate each signed field, each excluded field, null/absent combinations, owner, audience, profile, key version, PolicyDomain, participant tuple and COC quorum proof independently.

The existing H 101/101 candidate CI verifies a bounded I-profile vector set, not every exact P0 family above. Full per-family vector coverage remains L3 OPEN until added and passed.

## 10. Final I disposition / I 最终结论

This addendum defines the exact I P0 allowlists and referenced attestation contracts needed for an exact H review. It supersedes the generic projection wording for the named message families.

It does **not** by itself approve production trust roots, algorithm regulatory suitability, key custody, HSM/KMS, rotation/compromise ceremony, live sequencer deployment, external anti-rollback infrastructure or production conformance.

本补充定义了精确 I P0 白名单及引用证明合同，供 H 进行精确审查，并取代指定消息族的泛化投影表述。

本文件不代表生产 Trust Root、算法监管适用性、Key Custody、HSM/KMS、轮换/泄露仪式、实时 Sequencer 部署、外部 Anti-rollback 基础设施或生产符合性已获批准。


## 11. Scope correction / 范围修正

The common envelope in §2 applies only to the three BMCP message families in §§3.1–3.3. Standalone referenced proof objects in §§4–6 do not inherit fields such as `schema_id`, `message_nonce`, `causal_order_coordinator_ref` or `owner_signature_ref` unless their own exact schema explicitly defines them. Their signed projections are exactly the object-specific field lists in their sections, including the preassigned `signature_ref` where listed.

第 2 节 Common Envelope 仅适用于 §§3.1–3.3 的三个 BMCP Message Family。§§4–6 的独立引用 Proof Object 不自动继承 `schema_id`、`message_nonce`、`causal_order_coordinator_ref` 或 `owner_signature_ref` 等字段，除非其自身精确 Schema 明确规定。它们的签名投影严格采用各自章节列出的对象专属字段，包括预分配的 `signature_ref`。

