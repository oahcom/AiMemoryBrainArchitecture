# Phase 3.8.4 — H Exact Review of C Provider Submit Outcome Contract
# Phase 3.8.4 — H 对 C Provider Submit Outcome 合同的精确审查

- Reviewer: H — BMCP Protocol and Adapter Authentication
- Branch: `session-h-bmcp-protocol`
- Exact C source reviewed: `07-agent-integration/phase-3.8.4-c-normative-provider-submit-outcome-contract.md`
- C source Blob: `819705037da89834e10b6dd2ec6e66c1b8c70886`
- Exact H schema reviewed: `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.8.schema.json`
- H schema Blob: `70b892797d07489936300a26c0dedfafe1d6e746`
- H wire mapping Blob: `b132e6a01bcfe13f92020b9778ee3f7ddbf65753`
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS — STRUCTURAL/WIRE CANDIDATE ONLY**
- English and Chinese are normative peers.

## 1. H decision / H 决议

H accepts the five-value Provider Outcome enum and the C-owned semantic authority boundary in the exact C contract. The schema's `C_PROVIDER_OUTCOME_RECORDED` message family is an appropriate structural carrier for the C outcome reference, digest, provider identity/key, final request boundary, owner admission evidence, participant tuple, provider evidence and explicit COC intent absence.

H does not decide whether a provider actually accepted/rejected a request; C owns that truth. H does not infer Provider Outcome from transport ACK, COC quorum, Storage resolution, I terminality or D clearance.

H 接受精确 C 合同中的五值 Provider Outcome 枚举及 C 自有语义权威边界。Schema 的 `C_PROVIDER_OUTCOME_RECORDED` 消息族适合作为 C Outcome Ref/Digest、Provider/Key、Final Request Boundary、Owner Admission、Participant Tuple、Provider Evidence 和显式 COC Intent 缺失原因的结构载体。

H 不决定 Provider 是否实际接受/拒绝请求；该事实由 C 拥有。H 不得从 Transport ACK、COC Quorum、Storage Resolution、I Terminality 或 D Clearance 推断 Provider Outcome。

## 2. Exact structural mapping / 精确结构映射

| C semantic field | H schema field | H disposition |
|---|---|---|
| CSubmitOutcomeRef / Digest | `c_submit_outcome_ref` / `c_submit_outcome_digest` | ACCEPT |
| Outcome algebra | `provider_outcome` | ACCEPT exact five values |
| Provider identity / adapter / stable key | `provider_ref`, `provider_adapter_ref`, `provider_idempotency_key_ref` | ACCEPT |
| Provider request / receipt | `provider_request_ref`, `provider_receipt_ref` | Conditional by outcome |
| Final request boundary / digest | `final_request_boundary_id`, `request_digest` | ACCEPT |
| Causal transaction / participant tuple | `transaction_ref`, `participant_reservation_ref`, `participant_intent_ref`, `prepared_participant_ref`, `prepare_attempt_ref/generation`, `participant_ledger_ref/version`, `participant_tuple_digest` | ACCEPT as distinct typed references |
| I / D proof references | `i_terminal_decision_ref`, `d_clearance_ref` | ACCEPT as references; semantic verification remains with I/D |
| Storage resolution | `storage_resolution_proof_ref` | ACCEPT as Storage-owned evidence only |
| Provider evidence / lookup / no-handoff | `provider_outcome_evidence_ref`, `provider_lookup_proof_ref`, `provider_no_handoff_proof_ref`, `not_invoked_proof_ref`, `unknown_reason_ref` | ACCEPT; C defines truth conditions |
| C signature | `owner_signature_ref` plus common-envelope profile fields | ACCEPT with C-specific profile requirement |
| C owner ledger/admission | `owner_admission_ref/digest`, `owner_ledger_ref/version`, `owner_local_sequence`, `owner_high_water`, `owner_ledger_root` | ACCEPT |
| COC participant intent | `coc_participant_intent_ref`, `coc_absence_reason` | ACCEPT; null requires explicit non-empty reason |

## 3. Binding amendments / 约束性修订

1. **Outcome conditionality:** structural validation is not semantic proof. C's rules must be enforced: ACCEPTED requires authoritative provider acceptance; REJECTED requires positive no-side-effect/no-handoff proof; NOT_INVOKED requires positive C boundary proof; UNKNOWN/IN_DOUBT requires explicit reason and remains nonterminal.
2. **Profile separation:** protected C-signed outcome messages require a C-approved `signature_profile_id` and exact canonicalization/digest semantics. I's `AIMBA-I-CRYPTO-1.0` is not inherited by C. I trust/key-status verification and C owner-signature projection are separate responsibilities.
3. **Digest equality:** `c_submit_outcome_digest`, `request_digest`, `participant_tuple_digest`, owner admission digest and the referenced evidence digests must be checked for exact equality to the referenced immutable objects. Schema shape alone cannot prove this.
4. **Same-key semantics:** `provider_idempotency_key_ref` must be stable for the exact provider/account/endpoint/model/request scope. A new payload or provider scope cannot reuse the same outcome identity.
5. **COC absence:** `coc_participant_intent_ref=null` requires a reason and does not mean no C owner admission or provider-attempt obligations exist. COC record/commit proof is an independent COC attestation.
6. **No outcome promotion:** HANDOFF_ACCEPTED is not ExecutionStarted, Completed, Full Applied or user delivery. G must consume the exact C outcome under its own predicate.

## 4. L3 reference proof obligations / L3 参考证明义务

H requires reference-model vectors for:
- all five outcomes with valid/invalid conditional fields;
- accepted receipt/provider/request/digest mismatch;
- rejected after possible side effect → reject REJECTED and retain IN_DOUBT;
- null COC intent with absent/empty/missing reason;
- duplicate outcome identity with changed digest;
- same-key lookup unavailable and late evidence enrichment;
- profile missing/wrong-owner/wrong-audience/downgrade;
- valid C outcome but invalid COC quorum proof, and converse.

These are architectural semantic vectors and may run without real providers. No real provider or adapter test is required at this stage.

## 5. Final disposition / 最终结论

**ACCEPT WITH ENUMERATED AMENDMENTS — STRUCTURAL/WIRE CANDIDATE ONLY.**

C Blob `819705037da89834e10b6dd2ec6e66c1b8c70886` is accepted as the C-owned normative semantic source candidate for this exact review. H schema Blob `70b892797d07489936300a26c0dedfafe1d6e746` is accepted as the structural carrier only. H does not claim schema freeze, production crypto approval, independent SDK interoperability, provider execution, runtime conformance or implementation acceptance.

**有条件接受 — 仅结构/Wire 候选。** C 合同作为 C 自有 Provider Outcome 语义源候选被接受；H Schema 仅作为结构载体。H 不声明 Schema 冻结、生产密码学批准、SDK 互操作、Provider 执行、运行时符合性或实现验收。
