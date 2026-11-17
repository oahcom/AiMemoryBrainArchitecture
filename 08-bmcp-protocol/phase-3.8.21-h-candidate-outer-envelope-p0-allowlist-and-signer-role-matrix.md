# Phase 3.8.21 — H Candidate Outer-Envelope P0 Allowlist and Signer-Role Decision Matrix
# Phase 3.8.21 — H 候选 Outer-Envelope P0 Allowlist 与 Signer-Role 决策矩阵

- Owner perspective: H — BMCP Protocol / Envelope Authentication
- Status: **EXACT 67-FIELD P0 CANDIDATE; SIGNER ROLE / PROFILE / CRYPTOGRAPHY NOT APPROVED; C/I REVIEW REQUIRED; NOT FROZEN**
- H Unified 1.2.14 schema Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- H outer-auth validator Blob: `a863acd01abcb147db2bd23a3b8bb1985d81bc78`
- H Provider Outcome validator Blob: `b8cd692d261df7a31a0f65c3e003693e305f73a2`
- H envelope-auth test Blob: `3469c5268d3558c777ea9f16058e00570517ff54`
- H Phase 3.8.20 closure Blob: `73543e8e7963f1442931c318542a4249d1c41790`
- C review of explicit profile requirement: `f74f80ec11af2f329c2947ff1e790fa3b0181b57`
- I review of explicit profile requirement: `7785f7a8ab242816fb36d42e91fdd34e65aae4fb`
- H schema P0 field count: **67** (all C_PROVIDER_OUTCOME_RECORDED common + branch properties, de-duplicated, excluding only outer `payload_digest` and outer `signature`)
- Provenance: delegated H-role candidate construction; **not an independent H/C/I Owner decision**.
- English and Chinese are normative peers.

## 1. Exact scope / 精确范围

This P0 candidate is only for H Unified 1.2.14 `C_PROVIDER_OUTCOME_RECORDED`. It is not a generic P0 rule for other message types. The exact allowlist is derived from the 1.2.14 commonEnvelope and C Provider Outcome branch properties, de-duplicated. Unknown properties are forbidden by the schema and MUST be rejected, never silently omitted.

本 P0 候选仅适用于 H Unified 1.2.14 的 `C_PROVIDER_OUTCOME_RECORDED`，不是其他 Message Type 的通用 P0 规则。精确 Allowlist 来自 1.2.14 commonEnvelope 与 C Provider Outcome Branch 的 Properties，去重后形成。Schema 禁止未知属性，必须拒绝，不得静默遗漏。

The P0 object contains every present allowlisted field except the two outer-envelope derived/excluded fields:
- `payload_digest` — computed from the P0 object;
- `signature` — detached signature over the signature preimage.

The following are NOT excluded: C `c_submit_outcome_digest`, C `owner_signature_ref`, `integrity_proof_ref`, `channel_binding_proof_ref`, `key_id_ref`, `key_version`, `signature_profile_id`, and all I/D/Storage/COC join references.

P0 对象包含全部已出现的 Allowlist 字段，仅排除两个外层派生/排除字段：
- `payload_digest`：由 P0 对象计算；
- `signature`：对 Signature Preimage 的 Detached Signature。

以下字段**不得排除**：C `c_submit_outcome_digest`、C `owner_signature_ref`、`integrity_proof_ref`、`channel_binding_proof_ref`、`key_id_ref`、`key_version`、`signature_profile_id` 及全部 I/D/Storage/COC Join Reference。

## 2. Exact 67-field allowlist / 精确 67 字段 Allowlist

The following is the complete, closed P0 field inventory. A field is included only when present in the JSON object; a schema-permitted explicit null remains a present JSON null. An absent optional property remains absent. No defaults, aliasing, coercion or null/absent normalization are permitted.

以下为完整闭合的 P0 字段清单。字段仅在 JSON Object 中存在时纳入；Schema 允许的显式 Null 保持 JSON Null；可选字段 Absent 则继续 Absent。禁止默认值、别名、强制转换或 Null/Absent 归一化。

### Protocol and message identity / 协议与消息身份

`schema_id`, `schema_version`, `message_type`, `message_id`, `message_nonce`, `audience`, `sender_authority_ref`, `sender_subject_ref`

### Issuer, subject, owner and policy claims / Issuer、Subject、Owner 与 Policy 声明

`issuer_ref`, `subject_ref`, `owner_authority`, `owner_record_ref`, `policy_domain_ref`, `causal_order_profile_ref`, `causal_order_coordinator_ref`, `causal_order_domain_ref`

### Outer cryptographic metadata and integrity references / 外层密码学元数据与完整性引用

`canonicalization_profile_id`, `digest_algorithm`, `integrity_proof_ref`, `channel_binding_proof_ref`, `key_id_ref`, `key_version`, `created_at`, `owner_signature_ref`, `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest`, `coc_previous_entry_digest`, `signature_profile_id`, `schema_artifact_revision`

### C Provider Outcome object and provider-boundary evidence / C Provider Outcome 对象与 Provider 边界证据

`c_submit_outcome_ref`, `c_submit_outcome_digest`, `provider_outcome`, `provider_ref`, `provider_adapter_ref`, `provider_idempotency_key_ref`, `provider_request_ref`, `provider_receipt_ref`, `actual_inference_request_id`, `final_request_boundary_id`, `request_digest`, `transaction_ref`, `participant_reservation_ref`

### COC / Storage / I / D participant and resolution joins / COC / Storage / I / D Participant 与 Resolution Join

`prepared_participant_ref`, `prepare_attempt_ref`, `prepare_attempt_generation`, `participant_ledger_ref`, `participant_ledger_version`, `participant_tuple_digest`, `i_terminal_decision_ref`, `d_clearance_ref`, `storage_resolution_proof_ref`, `provider_outcome_evidence_ref`, `provider_lookup_proof_ref`, `provider_no_handoff_proof_ref`, `not_invoked_proof_ref`, `unknown_reason_ref`, `owner_admission_ref`

### C owner admission and ledger membership / C Owner Admission 与 Ledger Membership

`owner_admission_digest`, `owner_ledger_ref`, `owner_ledger_version`, `owner_local_sequence`, `owner_high_water`, `owner_ledger_root`, `coc_participant_intent_ref`, `coc_absence_reason`

<text color="secondary" size="xs">Total: 67 unique fields. Excluded outer fields: payload_digest, signature.</text>

## 3. Candidate digest and signature construction / 候选 Digest 与 Signature 构造

The following domain-separated construction is a proposal for C/I review, not a registered profile:

```text
P0 = object containing the exact present fields in the 67-field allowlist

payload_digest =
  lowercase_hex(
    SHA-256(
      UTF8("AIMBA-BMCP-ENVELOPE-PAYLOAD-v1\0")
      || RFC8785_JCS(P0)
    )
  )

signature_projection = P0 plus:
  "payload_digest": payload_digest

signature_preimage =
  UTF8("AIMBA-BMCP-ENVELOPE-SIGNATURE-v1\\0")
  || RFC8785_JCS(signature_projection)

# signature_profile_id and message_type are already members of P0
signature = Sign(registered_profile_key, signature_preimage)
```

候选 Digest 与 Signature 构造建议采用独立 Domain Tag，供 C/I 审查，尚未注册：
- Payload Digest 使用 `AIMBA-BMCP-ENVELOPE-PAYLOAD-v1`；
- Signature Preimage 使用 `AIMBA-BMCP-ENVELOPE-SIGNATURE-v1`；
- P0 与签名投影均使用 RFC8785 JCS；
- Digest 使用 SHA-256；
- Signature Algorithm/Encoding/Key Type 由经批准的 Signature Profile 决定，当前不冻结；
- `signature_profile_id` 必须来自认证 Registry，并包含在 P0；
- `payload_digest` 不进入自身 P0，但进入 Signature Projection；
- `signature` 不进入 P0 或自身 Signature Preimage。

CSubmitOutcome 1.0.1's `payload_digest` and signature use a separate C-owned profile/domain. The outer envelope digest and signature MUST NOT reuse the C object digest, signature preimage or domain tag. The same primitive (e.g. SHA-256/JCS/Ed25519) may only be reused under a separately approved envelope profile with distinct domain separation and P0.

CSubmitOutcome 1.0.1 的 `payload_digest` 与 Signature 使用独立 C-owned Profile/Domain。Outer Envelope Digest/Signature 不得复用 C Object Digest、Signature Preimage 或 Domain Tag。即使复用相同基础原语（如 SHA-256/JCS/Ed25519），也必须使用独立批准的 Envelope Profile、不同 Domain Separation 与 P0。

## 4. Signer-role alternatives / Signer Role 备选方案

| Option | Outer signer | Envelope sender claims | C object signature | Required approval / trade-off |
|---|---|---|---|---|
| A — Origin signer | C adapter/origin | C adapter | Separate C object signature | C approves a separate envelope profile; I registers C key/role; no automatic C profile reuse |
| B — Gateway attestor | H gateway | H gateway; `owner_authority=C`; subject/owner relationship via registry | C signature remains mandatory | H signs only transport/receipt attestation after authenticating C object and protected C channel; I registers H gateway; C approves attestation semantics |
| C — Independent attestor | Dedicated attestor | Attestor identity | C signature remains mandatory | New trust principal, availability and custody domain; I and C approvals required |

### H recommendation (candidate only) / H 建议（仅候选）

H recommends **Option B — H gateway attestor** as the preferred architecture candidate if the system requires a gateway-created BMCP envelope:
- C signs the immutable CSubmitOutcome object and remains the sole authority for provider outcome truth.
- H gateway verifies the C object signature and protected C transport/session, then signs the outer envelope under a distinct H gateway envelope profile.
- The outer signature attests only to the exact envelope, C object digest/reference, authenticated ingress context, audience and channel binding; it does not attest to provider truth or replace C's signature.
- `sender_authority_ref`/`sender_subject_ref` identify the H gateway; `owner_authority=C` identifies the C-owned domain record. I's registry must explicitly authorize this sender-to-owner relationship.
- The H gateway profile/key is I-governed; H cannot self-register or self-approve it.

H 建议优先评估 **Option B — H Gateway Attestor**，前提是 BMCP Envelope 由 Gateway 构造：
- C 签署不可变 CSubmitOutcome Object，并仍是 Provider Outcome Truth 的唯一权威；
- H Gateway 验证 C Object Signature 与 Protected C Transport/Session 后，以独立 H Gateway Envelope Profile 签署外层 Envelope；
- 外层签名仅证明精确 Envelope、C Object Digest/Reference、Authenticated Ingress Context、Audience 与 Channel Binding，不证明 Provider Truth，也不替代 C Signature；
- `sender_authority_ref`/`sender_subject_ref` 标识 H Gateway；`owner_authority=C` 标识 C-owned Domain Record。I Registry 必须明确授权该 Sender-to-Owner 关系；
- H Gateway Profile/Key 由 I 治理，H 不得自行注册或批准自身。

This is a recommendation, not an H/C/I decision. Option A remains viable if C explicitly wants the C adapter to sign the outer envelope. H MUST NOT silently assume either option.

以上只是建议，不是 H/C/I 决议。若 C 明确希望 C Adapter 签署外层 Envelope，Option A 仍可行。H 不得静默假设任何一种方案。

## 5. Exact semantic joins / 精确语义 Join

1. `owner_record_ref` and `c_submit_outcome_ref` are separate claims unless C defines an exact equality/indirection rule; no string-equality assumption.
2. `owner_signature_ref` binds the C object signature; outer `signature` binds the envelope only.
3. `key_id_ref`/`key_version`/`signature_profile_id` identify the outer signer, not the C object signer. The C object signer is authenticated through the C object and its C-owned profile.
4. `owner_authority`, `subject_ref`, sender authority and sender subject are bound through I-approved registry policy; do not equate sender role with owner authority.
5. `channel_binding_proof_ref` is in P0 and must also resolve against protected transport/session context.
6. `integrity_proof_ref` is in P0; the referenced proof must bind to the same raw envelope digest and profile.
7. `c_submit_outcome_digest` is the C object digest; `payload_digest` is the outer envelope digest. They are never interchangeable.
8. `coc_commit_proof_ref`, COC record/position/entry/previous-entry digests, I terminal, D clearance and Storage resolution remain owner/COC facts and must be independently authenticated.

## 6. Required C/I decision / 必需 C/I 决策

C must decide:
- whether Option A or B (or C) is acceptable;
- whether the outer envelope may attest only transport/receipt or also an origin claim;
- the exact relationship between C object `owner_signature_ref`, `owner_record_ref` and envelope sender identity;
- whether the proposed P0 field inventory includes every C-owned fact required for envelope integrity.

I must decide:
- trust root and issuer/signer registry authority;
- signer-to-owner authorization and delegation policy;
- profile identifier registration and cryptographic algorithm/encoding;
- key status, rotation, revocation, compromise and historical verification;
- anti-rollback and durable replay ledger trust/retention.

H must not register a profile, choose a trust root, claim signer authorization or freeze this P0 without those decisions.

C 必须决定 Option A/B/C、Outer Envelope 可声明的 Attestation 范围、C Object Signature/Owner Record/Envelope Sender 的关系，以及 P0 是否覆盖全部必需 C 事实。I 必须决定 Trust Root、Issuer/Signer Registry、Signer-to-Owner Authorization、Profile/Algorithm/Encoding、Key Lifecycle、Historical Verification、Anti-Rollback 与 Durable Replay Trust/Retention。未经这些决策，H 不得注册 Profile、选择 Trust Root、声称 Signer 获授权或冻结 P0。

## 7. H disposition / H 侧结论

**Delegated H-role decision: SUBMIT the exact 67-field P0 and signer-role alternatives for C/I review. Option B is the recommended candidate only. No P0/profile/signer role is approved or frozen. Production envelope authentication and durable acceptance remain BLOCKED.**

**角色模拟 H 侧决议：提交精确 67 字段 P0 与 Signer Role 备选方案供 C/I 审查。Option B 仅为推荐候选。不批准或冻结任何 P0/Profile/Signer Role。生产 Envelope Authentication 与 Durable Acceptance 仍 BLOCKED。**

---
**Provenance:** delegated H-role candidate design in the coordinating session; not an independent human H Owner decision or C/I security approval.
