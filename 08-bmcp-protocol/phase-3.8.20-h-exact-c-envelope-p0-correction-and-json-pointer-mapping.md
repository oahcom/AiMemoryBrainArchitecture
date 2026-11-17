# Phase 3.8.20 — H Exact C Envelope P0 Correction and JSON-Pointer Mapping
# Phase 3.8.20 — H 精确 C Envelope P0 修正与 JSON Pointer Mapping

- H authority: BMCP wire protocol and exact schema mapping
- C decision candidate corrected Blob: 310e7e0073d3c32f594bc151f10c249c828ce30f
- C original decision candidate Blob: 6347c9aa80bb48adb2e2e4f318960e14ba16f33e (superseded by correction)
- H Unified schema 1.2.14 Blob: 09fcd1fa29fe24255fbd87cae79dafb406594a59
- CSubmitOutcome 1.0.1 schema Blob: a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda
- H Phase 3.8.19 review Blob: 2a3a995396ee7a56d8fbbb03ec53b5d1d15e1f82
- Status: **P0 FIELD OMISSION CORRECTED; MAPPING CONTRACT CANDIDATE; EXECUTABLE AUTHENTICATION STILL OPEN**
- Provenance: delegated H-role correction and review; not an independent human H Owner signature.

## 1. Correction / 修正

H identified that C Phase 3.8.22 §4.1 described `integrity_proof_ref` and `channel_binding_proof_ref` as included in §4.4 but omitted them from the literal allowlist. C has corrected the exact decision candidate at Blob `310e7e0073d3c32f594bc151f10c249c828ce30f`. This H document binds only the corrected Blob.

Both proof references MUST be included in the C outer-envelope P0. This prevents locator substitution without invalidating the origin signature. Their referenced evidence still requires independent verification; signing a locator is not proof that the evidence is valid.

H 发现 C Phase 3.8.22 §4.1 声称 `integrity_proof_ref` 与 `channel_binding_proof_ref` 在 §4.4 被纳入，但字面 Allowlist 漏列。C 已将精确决策候选修正为 Blob `310e7e0073d3c32f594bc151f10c249c828ce30f`。本 H 文档只绑定修正后的 Blob。

两个 Proof Reference 都必须纳入 C Outer-Envelope P0，防止攻击者替换 Locator 而不触发 Origin Signature 失败。被引用 Evidence 仍需独立验证；签署 Locator 不等于证明 Evidence 有效。

## 2. Exact P0 set / 精确 P0 集合

Outer P0 = exact H commonEnvelope members plus exact C_PROVIDER_OUTCOME_RECORDED branch members, excluding only:
- derived `payload_digest`;
- output `signature`;
- coordinator-appended `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest`, `coc_previous_entry_digest`.

All serialized envelope members `integrity_proof_ref` and `channel_binding_proof_ref` are included. C object P0 remains independent and is not substituted for outer P0.

外层 P0 = 精确 H commonEnvelope 成员 + 精确 C_PROVIDER_OUTCOME_RECORDED 分支成员，仅排除：
- 派生的 `payload_digest`；
- 输出的 `signature`；
- Coordinator 后续追加的 `coc_commit_proof_ref`、`coc_record_ref`、`coc_record_position`、`coc_entry_digest`、`coc_previous_entry_digest`。

所有序列化 Envelope 成员 `integrity_proof_ref` 与 `channel_binding_proof_ref` 均纳入。C Object P0 独立存在，不得替代 Outer P0。

## 3. Exact JSON Pointer inventory / 精确 JSON Pointer Inventory

The H schema is a `oneOf` union. The applicable branch is selected by `/message_type = C_PROVIDER_OUTCOME_RECORDED`, then composed with `/$defs/commonEnvelope`. The exact pointer inventory is:

| JSON Pointer | Source schema | Outer P0 | Notes |
|---|---|---:|---|
| `/schema_id` | commonEnvelope | Yes | constant schema family |
| `/schema_artifact_revision` | commonEnvelope | Yes | exact artifact revision 1.2.14 |
| `/schema_version` | commonEnvelope | Yes | wire family 1.3.0 |
| `/message_type` | commonEnvelope + C branch | Yes | exact C message family |
| `/message_id` | commonEnvelope | Yes | stable identity |
| `/message_nonce` | commonEnvelope | Yes | replay identity |
| `/audience` | commonEnvelope | Yes | exact receiver audience |
| `/sender_authority_ref` | commonEnvelope | Yes | claim bound to protected principal |
| `/sender_subject_ref` | commonEnvelope | Yes | claim bound to protected principal |
| `/issuer_ref` | commonEnvelope | Yes | I-trusted C issuer |
| `/subject_ref` | commonEnvelope | Yes | protected subject |
| `/owner_authority` | commonEnvelope | Yes | must equal C |
| `/owner_record_ref` | commonEnvelope | Yes | C owner record |
| `/policy_domain_ref` | commonEnvelope | If present | exact scope |
| `/causal_order_profile_ref` | commonEnvelope | Yes | COC profile binding |
| `/causal_order_coordinator_ref` | commonEnvelope | Yes | coordinator authority |
| `/causal_order_domain_ref` | commonEnvelope | Yes | COC domain |
| `/canonicalization_profile_id` | commonEnvelope | Yes | exact approved profile |
| `/signature_profile_id` | commonEnvelope | Yes | C envelope profile identifier |
| `/digest_algorithm` | commonEnvelope | Yes | candidate SHA-256 |
| `/integrity_proof_ref` | commonEnvelope | Yes | proof locator signed; proof independently verified |
| `/channel_binding_proof_ref` | commonEnvelope | Yes | locator signed; proof bound to protected session |
| `/key_id_ref` | commonEnvelope | Yes | never trusted from payload alone |
| `/key_version` | commonEnvelope | Yes | immutable key version |
| `/created_at` | commonEnvelope | Yes | signed timestamp claim |
| `/owner_signature_ref` | commonEnvelope | Yes | immutable signer record reference |
| `/payload_digest` | commonEnvelope | No | derived from outer P0 |
| `/signature` | commonEnvelope | No | signature output |
| `/c_submit_outcome_ref` | C branch | Yes | immutable C object locator |
| `/c_submit_outcome_digest` | C branch | Yes | C object digest join |
| `/provider_outcome` | C branch | Yes | outcome enum |
| `/provider_ref` | C branch | Yes if present | provider identity |
| `/provider_adapter_ref` | C branch | Yes if present | C adapter identity |
| `/provider_idempotency_key_ref` | C branch | Yes if present | opaque key reference |
| `/provider_request_ref` | C branch | Yes if present | provider request identity |
| `/provider_receipt_ref` | C branch | Yes if present | provider receipt |
| `/actual_inference_request_id` | C branch | Yes if present | actual provider request ID |
| `/final_request_boundary_id` | C branch | Yes | final request boundary |
| `/request_digest` | C branch | Yes | exact request digest |
| `/transaction_ref` | C branch | Yes | transaction join |
| `/participant_reservation_ref` | C branch | Yes if present | participant reservation |
| `/prepared_participant_ref` | C branch | Yes if present | Storage prepared participant |
| `/prepare_attempt_ref` | C branch | Yes if present | prepare attempt |
| `/prepare_attempt_generation` | C branch | Yes if present | attempt generation |
| `/participant_ledger_ref` | C branch | Yes if present | participant ledger |
| `/participant_ledger_version` | C branch | Yes if present | participant ledger version |
| `/participant_tuple_digest` | C branch | Yes if present | tuple digest |
| `/i_terminal_decision_ref` | C branch | Yes if present | I evidence locator |
| `/d_clearance_ref` | C branch | Yes if present | D evidence locator |
| `/storage_resolution_proof_ref` | C branch | Yes if present | Storage evidence locator |
| `/provider_outcome_evidence_ref` | C branch | Yes | C provider evidence locator |
| `/provider_lookup_proof_ref` | C branch | Yes if present | same-key lookup evidence |
| `/provider_no_handoff_proof_ref` | C branch | Yes if present | no-handoff evidence |
| `/not_invoked_proof_ref` | C branch | Yes if present | not-invoked evidence |
| `/unknown_reason_ref` | C branch | Yes if present | uncertainty reason |
| `/owner_admission_ref` | C branch | Yes | owner admission |
| `/owner_admission_digest` | C branch | Yes | admission digest |
| `/owner_ledger_ref` | C branch | Yes | owner ledger |
| `/owner_ledger_version` | C branch | Yes | ledger version |
| `/owner_local_sequence` | C branch | Yes | local sequence |
| `/owner_high_water` | C branch | Yes | owner high-water |
| `/owner_ledger_root` | C branch | Yes | ledger root |
| `/coc_participant_intent_ref` | C branch | Yes | explicit null vs string |
| `/coc_absence_reason` | C branch | Yes if present | required when intent is null |
| `/coc_commit_proof_ref` | C branch | No | coordinator-appended COC evidence |
| `/coc_record_ref` | C branch | No | coordinator-appended COC evidence |
| `/coc_record_position` | C branch | No | coordinator-appended COC evidence |
| `/coc_entry_digest` | C branch | No | coordinator-appended COC evidence |

Note: H schema marks some C fields optional at the wire level; when present they are signed. Requiredness and semantic outcome constraints still apply exactly as in the schema. Any duplicated value must equal the dereferenced C object byte-semantically after typed JSON parsing; null/absent are never coerced.

说明：H Schema 在 Wire 层将部分 C Field 标为 Optional；一旦存在就必须签名。Requiredness 与 Semantic Outcome Constraint 仍严格遵循 Schema。任何重复值都必须与解引用的 C Object 在 Typed JSON Parsing 后精确相等；Null/Absent 不得 Coerce。

## 4. H implementation sequence / H 实现顺序

1. strict raw parser (duplicate keys, UTF-8, I-JSON);
2. exact H schema pin and branch selection;
3. exact P0 extractor with fail-closed unknown-field handling;
4. SHA-256 digest recomputation and C-envelope profile signature verification through I-authorized registry;
5. protected transport principal and channel-binding verification;
6. nonce replay/idempotency authority;
7. independent C object P0/signature/digest verification;
8. exact duplicate-field equality;
9. I/D/Storage/COC authority proof joins;
10. tri-state VALID/INVALID/UNKNOWN and durable acceptance only after VALID.

## 5. Open conditions / 未决条件

- C profile candidate is not registered; I approval remains OPEN.
- The candidate C profile's P0 includes proof locators, but the actual integrity and channel-binding evidence must be independently verified.
- H has not yet implemented the outer P0 extractor or signature verification in the Provider Outcome validator.
- H has not yet authenticated transport principal or implemented authoritative replay ledger.
- No production Gateway, trust adapter, replay store, or durable ingress path is proven.

## 6. H disposition / H 结论

**Accept the corrected C origin-signer/P0 architecture as a coherent wire candidate. The proof-reference omission is corrected and bound. Exact P0 mapping is now documented; implementation, I profile registration, executable full-path tests, Storage durable-ingress binding and independent Owner acceptance remain OPEN.**
