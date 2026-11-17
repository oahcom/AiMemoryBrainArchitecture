# Phase 3.8.10 — C Wire Amendment: Provider Outcome on Unified 1.2.12 / RecoveryJoin 1.0.2
# Phase 3.8.10 — C Wire 修订：Unified 1.2.12 / RecoveryJoin 1.0.2 Provider Outcome

- Owner perspective: C — Agent Integration / Provider Egress and Outcome Authority
- Status: **C-ROLE CANDIDATE AMENDMENT / H EXACT CROSS-REVIEW REQUIRED / PROFILE NOT REGISTERED / NOT FROZEN**
- Supersedes the H 1.2.11 applicability references in C Phase 3.8.6/3.8.7/3.8.8/3.8.9 only for the candidate mapping specified here.
- CSubmitOutcome contract Blob: `2ecdf44cae1bf71e9611dd5367c8f7bcf25dd7ac`.
- CSubmitOutcome JSON Schema Blob: `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c`.
- Exact H Unified 1.2.12 Blob: `a54f66914a819d77f00c6af04e76453ff9f654ee`.
- Exact H RecoveryJoin 1.0.2 Blob: `4b664e3bce465499bcdfd93796349a4ba7074002`.
- Reviewed Storage successor manifest Blob: `6fc0bedaf5421d1be5a9ab5fb4d8cfab2871d7d7`.
- Provenance: coordinator-authored C-role simulation; not independent human C Owner approval.

## 1. C wire adoption / C Wire 采纳

C adopts H Unified 1.2.12 as the candidate envelope schema for `C_PROVIDER_OUTCOME_RECORDED`, and RecoveryJoin 1.0.2 as the candidate structural carrier for C owner-snapshot membership proofs. This does not freeze the wire or register the C signature profile. C remains sole authority for provider outcome semantics and actual transport evidence.

C 采纳 H Unified 1.2.12 作为 `C_PROVIDER_OUTCOME_RECORDED` 候选 Envelope Schema，采纳 RecoveryJoin 1.0.2 作为 C Membership Proof 候选结构载体。但这不构成 Wire Freeze，也不代表 C 签名配置已注册。Provider Outcome 语义与真实 Transport 证据仍由 C 独占。

## 2. Unified 1.2.12 envelope mapping / Unified 1.2.12 Envelope 映射

For `C_PROVIDER_OUTCOME_RECORDED`, H 1.2.12 carries the following fields. They are equality-checked projections of the immutable C object where the corresponding member exists; the immutable C object remains authoritative:

| H 1.2.12 envelope field | CSubmitOutcome 1.0.0 object member |
|---|---|
| `c_submit_outcome_ref` | `record_ref` / immutable CSubmitOutcomeRef |
| `c_submit_outcome_digest` | canonical payload digest of the exact immutable object |
| `provider_outcome` | exact C outcome enum |
| `provider_ref` | `ProviderRef` |
| `provider_adapter_ref` | `AdapterRef` |
| `provider_idempotency_key_ref` | `IdempotencyKeyRef` |
| `provider_request_ref` | `ProviderRequestRef` |
| `provider_receipt_ref` | `ProviderReceiptRef` |
| `actual_inference_request_id` | `ActualInferenceRequestId`, when present |
| `final_request_boundary_id` | `FinalRequestBoundaryRef` |
| `request_digest` | `RequestDigest` |
| `transaction_ref` | `CausalOrderTransactionRef` |
| `participant_intent_ref` / `participant_reservation_ref` | paired COC ParticipantIntent/Reservation refs; both present or both absent with explicit absence reason under C object semantics |
| `provider_outcome_evidence_ref` | C-authenticated provider/runtime evidence ref |
| `provider_lookup_proof_ref` | same-key lookup proof for the original attempt, when applicable |
| `provider_no_handoff_proof_ref` / `not_invoked_proof_ref` | authoritative no-handoff / NOT_INVOKED evidence |
| `unknown_reason_ref` | explicit UNKNOWN/IN_DOUBT reason |
| `owner_admission_ref/digest` | exact CAdmissionRef and CAdmissionDigest |
| `owner_ledger_ref/version/local_sequence/high_water/root` | exact C owner ledger identity and frozen C-local membership fields |
| `owner_signature_ref` | external C signature reference |
| `coc_commit_proof_ref`, `coc_record_ref/position`, `coc_entry_digest` | independently authoritative COC proof/record/position/digest; not C provider truth |
| `i_terminal_decision_ref`, `d_clearance_ref`, `storage_resolution_proof_ref` | independently authoritative I/D/Storage evidence refs |

The H envelope does not inline every C P0 member. In particular, `CGateGeneration`, `ProviderAttemptRef/Generation`, `ProviderAccountRef`, `EndpointRef`, `RegionRef`, `IdempotencyNamespaceRef`, adapter build and provider capability digest are resolved through the immutable C object. H MUST dereference `c_submit_outcome_ref`, verify the exact object schema/profile and digest, and compare every duplicated envelope field with the corresponding object member. Missing dereference, missing required duplicate, digest mismatch, conflicting tuple or unknown C key status is INVALID or UNKNOWN according to the precise verifier result; it must never be treated as success.

The immutable C object is authoritative for C outcome truth. H envelope fields are typed transport projections, not a second source of truth. A valid C signature alone does not prove provider receipt issuer trust, C ledger inclusion, C gate linearization or provider-specific idempotency.

## 3. RecoveryJoin 1.0.2 C membership mapping / C Membership Proof 映射

The generic `ownerSnapshotMembershipProof` fields map to C:
- `owner_kind=C`;
- `owner_authority_ref` = C Adapter/ProviderAccount authority;
- `owner_ledger_ref/version`, `owner_entry_ref/digest`, `owner_admission_ref` = exact C owner ledger and row identity;
- `owner_sequence_namespace/local_sequence/high_water` = C-local row sequence and applicable frozen high-water;
- `owner_ledger_root`, `owner_snapshot_ref/digest`, `owner_snapshot_attestation_ref/digest` = complete C snapshot evidence;
- `owner_gate_ref/generation` = C Egress Gate and CGateGeneration;
- `scope_ref/generation/binding_digest` = provider/account/adapter/endpoint/region and operation scope;
- `operation_identity_ref/digest`, `request_digest` = exact provider operation and immutable final request;
- `anti_rollback_anchor_ref`, `key_status_generation`, `signature_profile_ref`, `key_id`, `key_version`, `canonicalization_profile_ref`, `digest_profile_ref` = C-owned proof trust and signing metadata;
- `proof_digest`, `signature_ref` = derived proof digest and external C signature ref.

The exact C row's immutable `owner_entry_ref` and `owner_entry_digest` MUST bind the full typed C admission/reservation/provider-attempt/outcome tuple, including ProviderAttemptRef/Generation, provider/account/adapter/endpoint/region, idempotency namespace/key, request digest, transport phase and C outcome evidence. C's owner-authoritative verifier MUST resolve that row and validate the complete tuple. The RecoveryJoin payload is included in `owner_snapshot_membership_proofs`; the matching admission binding MUST carry the exact `owner_snapshot_membership_proof_ref` and `owner_snapshot_membership_proof_digest`. H cannot validate C completeness by inspecting schema shape alone.

## 4. Outcome and send safety / Outcome 与发送安全

The final transport-owning C Adapter MUST serialize CommitEgress and CloseEgressGate through one durable C sequencer. Before any irreversible handoff it validates current CGateGeneration, exact request digest, C admission/attempt, COC reservation, I `COMMIT_WON` for the exact operation and D clearance/current Fence. Close-first proves NOT_INVOKED with zero bytes; send-admission-first captures the attempt in the frozen in-flight set. Ambiguous handoff remains UNKNOWN/IN_DOUBT and same-key lookup refers to the original attempt. No retry-as-new-operation.

C alone issues immutable CSubmitOutcome from actual provider evidence or authoritative same-key lookup. H/COC/Storage/I/D cannot synthesize provider success.

## 5. Signature and trust profile / 签名与信任配置

The candidate profile `AIMBA-C-CRYPTO-1.0` remains **PROPOSED / NOT REGISTERED**. This amendment does not approve production key custody, trust roots, rotation, revocation, anti-rollback or provider evidence issuer trust. I owns registration and key governance; C owns C P0 and provider outcome truth; H owns wire verification and interop.

## 6. Required H exact cross-review / H 精确交叉审查要求

H must review:
1. the exact field mapping above against H Unified 1.2.12;
2. C object dereference, digest preimage and duplicate-field equality;
3. C owner membership proof payload and RecoveryJoin 1.0.2 proof ref/digest joins;
4. UNKNOWN/INVALID distinctions for missing object, missing verifier, incomplete C ledger query, unknown key status, invalid provider evidence and ambiguous handoff;
5. positive/negative vectors for all outcome families and every duplicated-field mutation;
6. explicit proof that no H or COC record can mint provider outcome.

## 7. Status / 状态

- H Unified 1.2.12 envelope shape: **ADOPTED AS CANDIDATE**.
- RecoveryJoin 1.0.2 membership shape: **ADOPTED AS CANDIDATE, subject to C owner-row verifier**.
- C object mapping in this amendment: **PROPOSED; H EXACT CROSS-REVIEW REQUIRED**.
- C crypto profile registration/trust: **OPEN / NOT REGISTERED**.
- Provider-specific idempotency, production adapter, durable sequencer and race/fault execution: **NOT VERIFIED**.
- Independent C Owner signature and wire freeze: **NOT PROVIDED**.
