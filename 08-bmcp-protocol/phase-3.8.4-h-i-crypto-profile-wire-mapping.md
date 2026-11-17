# Phase 3.8.4 — H Wire Mapping for I Cryptographic Profile
# Phase 3.8.4 — H 对 I 密码学配置的 Wire 映射

- Owner: H — BMCP Protocol and Adapter Authentication
- Exact I proposal: `AIMBA-I-CRYPTO-1.0`, Blob `5eeb011032c53c2f7897d699d6f512b26f07d0a2`
- Exact H schema: `bmcp.coc-jf10-unified/1.2.11`, Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40`
- Exact H RecoveryJoin schema 1.0.1: Blob `f94e01cf30b4c59fca24cb4ccd8b76a0db8ca95c`
- Exact signed schema artifact revision: `schema_artifact_revision = 1.2.11`; on-wire family version: `schema_version = 1.3.0`
- H decision: **ACCEPT AS WIRE-MAPPING CANDIDATE WITH BLOCKING AMENDMENTS**
- Status: **NOT FROZEN / NOT INTEROPERABILITY-VERIFIED / NOT IMPLEMENTED**
- Provenance: delegated H-role simulation at the user's direction; not an independent human H Owner signature.
- English and Chinese are normative peers.

## 1. H disposition / H 决议

H accepts the I proposal as a candidate cryptographic input and accepts schema artifact 1.2.11 as a breaking wire-family revision: the exact artifact revision is now a required signed common-envelope field and the wire version advances to 1.3.0. H does not approve I's algorithm choice, trust roots, key custody, key lifecycle, historical trust or anti-rollback policy. Those remain I/governance decisions.

H accepts the following exact identifiers for the proposed I mapping only:

| Field | Exact value |
|---|---|
| Profile bundle | `AIMBA-I-CRYPTO-1.0` |
| Canonicalization profile | `RFC8785-JCS-1.0` |
| Signature profile | `AIMBA-ED25519-SHA256-1.0` |
| Digest algorithm | `SHA-256` |
| Signature encoding | Base64url without padding |
| JSON canonicalization | RFC 8785 JCS constrained by RFC 7493 I-JSON |

H 将 I 提案接受为候选密码学输入，并接受 Schema Artifact 1.2.11 作为破坏性 Wire Family 修订：精确 Artifact Revision 成为必填且参与签名的 Common Envelope 字段，Wire Version 升级至 1.3.0。H 不批准 I 的算法选择、Trust Root、Key Custody、Key Lifecycle、历史信任或 Anti-rollback 策略；这些仍由 I/治理决策。

## 2. Schema 1.2.11 exact change / Schema 1.2.11 精确变更

Artifact 1.2.8 introduced optional `signature_profile_id` in `$defs.commonEnvelope` and the owner snapshot attestation digest. Artifact 1.2.11 retains those fields, makes the snapshot attestation digest mandatory, adds required `schema_artifact_revision=1.2.11`, and advances the wire family to `schema_version=1.3.0`. The new artifact-revision field is structurally required and is included in the I P0 projection for unified-schema messages.

For protected I-signed records, the semantic validator MUST require all of:
- `canonicalization_profile_id = RFC8785-JCS-1.0`;
- `signature_profile_id = AIMBA-ED25519-SHA256-1.0`;
- `digest_algorithm = SHA-256`;
- `key_id_ref` and immutable `key_version`;
- exact message-family projection and owner authority = I.

Missing `signature_profile_id` is a semantic rejection for a protected I-signed record, even though the additive structural schema can parse a legacy envelope. No downgrade or fallback is permitted.

Artifact 1.2.11 makes artifact and wire versions independently explicit and signed. The `$id`, `schema_artifact_revision` and `schema_version` must agree with the exact resolved artifact and protocol family; mismatch or downgrade is rejected.

Artifact 1.2.8 曾在 `$defs.commonEnvelope` 增加可选 `signature_profile_id` 与 Owner Snapshot Attestation Digest。Artifact 1.2.11 保留这些字段，将 Snapshot Attestation Digest 设为必填，新增必填 `schema_artifact_revision=1.2.11`，并将 Wire Family 升级为 `schema_version=1.3.0`。新 Artifact Revision 字段在结构层强制要求，并纳入 Unified Schema 消息的 I P0 Projection。

但所有受保护的 I 签名记录，Semantic Validator 必须强制要求上述四个精确配置值、Key ID/Version、消息专属 Projection 以及 I Owner Authority。结构 Schema 能解析旧 Envelope，不代表 I 安全语义接受旧 Envelope；缺失 Profile ID 必须拒绝，不得降级。Artifact 1.2.11 将 Artifact Version 与 Wire Version 分别显式化并纳入签名。`$id`、`schema_artifact_revision` 与 `schema_version` 必须与解析到的精确工件及协议族一致；不一致或降级必须拒绝。

## 2.1 Exact artifact and wire version binding / Artifact 与 Wire Version 精确绑定

The unified schema requires both `schema_artifact_revision=1.2.11` and `schema_version=1.3.0`. They are distinct, mandatory common-envelope fields. The artifact revision identifies the exact H schema artifact selected by the receiver; the wire version identifies the protocol-family contract. Both are owner-authored immutable identity fields and MUST be included in I P0 for all I-signed unified-schema message families.

RecoveryJoin 1.0.2 remains a separate schema artifact. Its nested `completeEmptyProof` and `outOfScopeProof` projections are governed by their own exact H field maps and are not assigned the unified schema's artifact revision.

统一 Schema 强制要求 `schema_artifact_revision=1.2.11` 与 `schema_version=1.3.0`。两者是不同且必填的 Common Envelope 字段：Artifact Revision 标识接收方解析的精确 H Schema 工件；Wire Version 标识协议族合同。两者均属于 Owner-authored 不可变身份字段，必须纳入所有 I 签名 Unified Schema 消息的 P0。

RecoveryJoin 1.0.2 是独立 Schema 工件，其嵌套 `completeEmptyProof` 与 `outOfScopeProof` 使用各自精确 H Field Map，不继承 Unified Schema 的 Artifact Revision。

## 3. Owner signature projection / Owner 签名投影

H defines the following deterministic two-stage projection for I-signed records. It is not a generic projection for C, D, Storage or COC signatures.

### 3.1 P0 — owner-authored semantic fields

`P0` contains every immutable owner-authored field defined by the exact message-family schema, including `schema_artifact_revision`, `schema_version`, the common envelope identity and trust fields, message-specific payload, typed references, scope, purpose, audience, PolicyDomain, owner generation/high-water/root/count/digest, terminal enum, key ID/version, creation/validity fields and any preassigned stable `owner_signature_ref`.

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
| `OWNER_LOCAL_GATE_RELEASE` | `owner_kind`, `release_type`, `owner_gate_ref`, `owner_gate_generation`, `recovery_epoch_ref`, `batch_record_ref`, `batch_digest`, `manifest_record_ref`, `manifest_content_digest`, `owner_request_high_water`, `reconciliation_root`, `owner_signature_ref`, `owner_admission_high_water`, `request_set_digest`, `admission_set_digest`, `request_ledger_root`, `admission_ledger_root`, `batch_position`, `batch_entry_digest`, `manifest_record_position`, `manifest_record_entry_digest` | `owner_kind=I`, `owner_authority=I`, release type is the exact I outage-admission release enum |
| `JF10_I_TERMINAL_DECISION_OBSERVED` | `i_terminal_outcome`, `i_terminal_decision_ref`, `i_sequencer_position`, `commit_authorization_receipt_ref`, `receipt_digest`, `receipt_consumption_proof_ref`, `prepared_participant_ref`, `prepared_transaction_gid`, `database_incarnation_ref`, `prepare_attempt_ref`, `prepare_attempt_generation`, `participant_ledger_ref`, `participant_ledger_version`, `participant_tuple_digest`, `owner_signature_ref` | `owner_authority=I`; terminal enum and same-XID tuple are checked by I semantics |
| I owner snapshot attestation referenced by `owner_snapshot_attestation_ref` | Resolve to the exact immutable I `OWNER_LOCAL_PENDING_GATE`/snapshot attestation record and compare all owner, gate, scope, generation, high-water, count, root, digest and anti-rollback fields | The referenced record must be I-signed and its digest/ref must match the nested COC snapshot |

For the snapshot reference, H must not treat the nested `ownerSnapshot` JSON object as an I signature. The I-signed source object is dereferenced and verified separately. Empty-set and out-of-scope assertions are accepted only when carried by an exact I-signed evidence object whose schema and projection are explicitly pinned; absent or partial evidence remains UNKNOWN.

### 4.1 Owner snapshot attestation binding / Owner Snapshot Attestation 绑定

Schema 1.2.8 introduced `owner_snapshot_attestation_digest`; schema 1.2.11 makes it required. H semantic validation must dereference `owner_snapshot_attestation_ref`, verify the I signature, recompute the referenced immutable object's SHA-256 digest and compare it to this field, then compare owner, gate/scope generation, request/admission high-waters, counts, roots, inventory epoch and anti-rollback anchor to the COC-embedded `ownerSnapshot`. Missing digest, mutable locator, mismatch or unavailable object returns UNKNOWN/INVALID and keeps the recovery gate closed.

### 4.2 COMPLETE_EMPTY and OUT_OF_SCOPE proof schemas / 空集合与范围外证明 Schema

RecoveryJoin schema 1.0.1 defines two separately dereferenced proof objects:

- `$defs.completeEmptyProof`: binds owner authority, REQUEST_SET/ADMISSION_SET, Scope/ScopeGeneration, exact owner ledger/version, ledger query ref, owner-local high-water, `pagination_complete=true`, `count=0`, canonical empty root, key-status generation, anti-rollback anchor, signature profile/ref and proof digest.
- `$defs.outOfScopeProof`: binds exact request/operation identity and digest, target class, Scope/ScopeGeneration, applicability policy, `OUT_OF_SCOPE_WITH_PROOF` decision, reason code, owner ledger/version/high-water, complete query/pagination, key-status generation, anti-rollback anchor, signature profile/ref and proof digest.

For an I proof, `signature_profile_ref` MUST resolve to `AIMBA-ED25519-SHA256-1.0` under bundle `AIMBA-I-CRYPTO-1.0`; the resolved proof is verified with the exact I P0/JCS/Ed25519 construction. A zero count without its matching signed empty proof is UNKNOWN. An OUT_OF_SCOPE disposition without its exact signed proof ref+digest is UNKNOWN. No missing or unavailable evidence is interpreted as empty or out-of-scope.

For both proof definitions, the exact I P0 projection is every schema-defined proof field except `proof_digest` (computed from P0). `signature_ref` is included only as a stable preallocated locator and MUST NOT be derived from signature bytes. Compute `proof_digest = SHA-256(ASCII("AIMBA-I-PAYLOAD-v1") || 0x00 || JCS(P0))`; then sign the projection plus proof_digest using the I signature preimage, with fixed message types `I_COMPLETE_EMPTY_PROOF` and `I_OUT_OF_SCOPE_PROOF` respectively. The schema's `signature_profile_ref` must resolve to the exact I signature profile and key-status generation. A proof ref/digest mismatch is INVALID; missing query, pagination, high-water, key status or anti-rollback evidence is UNKNOWN.

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

1. I must issue a fresh exact-version decision on the updated mapping and review the exact profile Blob `5eeb011032c53c2f7897d699d6f512b26f07d0a2`; algorithm/regulatory suitability remains a separate I/governance decision.
2. H must publish a separate exact-version decision for schema 1.2.11 Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40`, RecoveryJoin 1.0.2 Blob `f94e01cf30b4c59fca24cb4ccd8b76a0db8ca95c` and this mapping revision.
3. I/H must confirm the exact snapshot attestation digest binding, empty-set/out-of-scope proof references and P0 allowlists above against the final schema artifacts.
4. At least two independent canonicalization/signature implementations and byte-for-byte vectors must pass.
5. I must approve trust-root/key custody/rotation/compromise/anti-rollback operations and the external checkpoint mechanism.
6. Storage must accept the exact proof-verification contract for its actual visibility linearization point.
7. No profile is production-active until independent human Owner/governance approval and runtime conformance are recorded.

## 10. Final H decision / H 最终决议

I exact review of the prior mapping revision R3: Blob `b132e6a01bcfe13f92020b9778ee3f7ddbf65753`; I review Blob `93afe9c9e06d20de5ce1c2a0f676b4785123fbcf` accepted the prior 1.2.8 bundle with amendments — **ACCEPT WITH ENUMERATED AMENDMENTS**. This revised mapping requires a fresh I exact-version review.

**ACCEPT AS WIRE-MAPPING CANDIDATE WITH BLOCKING AMENDMENTS.**

H accepts the additive schema envelope field and the separation between owner signature, COC quorum attestation and transport channel binding. H does not approve I's cryptographic policy or any other owner's signature profile. The projection and vectors remain candidate until the exact I/H decisions and independent implementations are complete.

**作为 Wire Mapping 候选接受，但保留阻断修订。** H 接受新增 Envelope 字段，以及 Owner Signature、COC Quorum Attestation、Transport Channel Binding 的分离。H 不批准 I 的密码学策略或其他 Owner 的签名配置。精确 Projection、独立实现与 I/H 决议完成前，不得冻结或生产启用。


## 11. Phase 3.8.4 exact-version amendment / 精确版本修订

### Exact vector evidence

- H unified schema 1.2.11 Blob: `4f1e103ab4b2ac961d77179dba0b65093532ea40`
- I crypto vector Blob: `4657f0c81e9c8692d29ac183380f3d7e074a4e4c`
- I Python/Node vector test now includes the artifact/wire version fields in the three unified-schema I P0 families.
- `OWNER_LOCAL_GATE_RELEASE` P0 now signs `manifest_content_digest` separately from `manifest_record_entry_digest`; the ambiguous `manifest_digest` field is removed.
- The fixed Ed25519 seed remains TEST-ONLY. The vector run proves cross-language deterministic test behavior, not production key custody or trust approval.

### H disposition

**ACCEPT AS WIRE-MAPPING CANDIDATE WITH BLOCKING AMENDMENTS.** This is a delegated H-role simulation, not an independent human H Owner signature. I must review this exact mapping and vector bundle. No production cryptographic freeze, deployment or Storage acceptance is implied.

**作为 Wire Mapping 候选接受，但保留阻断修订。** 本决议是协调会话的 H 角色模拟，不是独立人工 H Owner 签署。I 必须审查本精确 Mapping 与 Vector Bundle。不代表生产密码学冻结、部署或 Storage 接受。


## 12. Owner snapshot membership proof wire mapping / Owner Snapshot Membership Proof Wire 映射

The companion RecoveryJoin schema is now 1.0.2, Blob `4b664e3bce465499bcdfd93796349a4ba7074002`. It defines `ownerSnapshotMembershipProof` as a separate owner-authored proof payload and requires every admissionJoin and noParticipantDisposition to bind its immutable proof ref/digest.

The wire payload includes owner kind/authority, issuer/subject/audience/purpose, exact ledger/version/entry/admission identity, owner-local namespace/sequence/high-water, ledger root, immutable snapshot and attestation refs/digests, gate/scope generations, operation/request identity, anti-rollback anchor, key-status generation, signature profile/key/version, canonicalization/digest profile, proof digest and signature ref.

H owns only the typed schema and reference mapping. I/D/C independently own their proof P0, key trust, signature and completeness semantics. A schema-valid proof is not accepted until the relevant owner authority verifies its signature and exact snapshot inclusion. Missing verifier result is UNKNOWN; mismatched owner/entry/root/snapshot/high-water/scope is INVALID.

RecoveryJoin 1.0.2 does not inherit Unified Schema artifact revision 1.2.11 or wire 1.3.0. It remains an independently pinned companion artifact.

配套 RecoveryJoin Schema 升级为 1.0.2，Blob `4b664e3bce465499bcdfd93796349a4ba7074002`。它将 `ownerSnapshotMembershipProof` 定义为独立 Owner-authored Proof Payload，并要求每个 admissionJoin 与 noParticipantDisposition 绑定不可变 Proof Ref/Digest。

Wire Payload 包含 Owner Kind/Authority、Issuer/Subject/Audience/Purpose、精确 Ledger/Version/Entry/Admission 身份、Owner-local Namespace/Sequence/High-water、Ledger Root、Snapshot/Attestation Ref/Digest、Gate/Scope Generation、Operation/Request 身份、Anti-rollback Anchor、Key-status Generation、Signature Profile/Key/Version、Canonicalization/Digest Profile、Proof Digest 与 Signature Ref。

H 只拥有 Typed Schema 与引用映射。I/D/C 分别拥有自己的 Proof P0、Key Trust、Signature 与 Completeness 语义。Schema 有效不代表 Proof 已接受；相关 Owner Authority 必须验证签名与精确 Snapshot Inclusion。缺少 Verifier 结果为 UNKNOWN；Owner/Entry/Root/Snapshot/High-water/Scope 不匹配为 INVALID。

RecoveryJoin 1.0.2 不继承 Unified Schema Artifact Revision 1.2.11 或 Wire 1.3.0，仍是独立绑定的配套工件。
