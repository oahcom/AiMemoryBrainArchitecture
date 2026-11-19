# R3 Execution Record 018 (exact-Head re-execution at be9ac983 — B-02 / N-01 closure)

- Timestamp: 2026-11-19T15:41:59Z (UTC)
- Executor: WorkBuddy coordinator (13-20-04), mechanical evidence lane
- Repository: oahcom/AiMemoryBrainArchitecture
- Exact checked-out commit SHA: `be9ac983c56a6e295feeb0a363d47397abdde930`
- Environment: CPython 3.13.14 / Windows / isolated directory outside the working tree
- Exact command: `python -m unittest discover -s <isolated>/reference-model -p 'test_*.py' -v`
- Exit code: 0
- Discovered 103 / pass 103 / fail 0 / error 0 / skip 0; `Ran 103 tests in 0.007s` — `OK`

This record is a **real re-execution** at the exact head `be9ac983`, per the R2 minimal fix (B-02/N-01). It is not a SHA-field patch of record-017. The test suite output is byte-deterministic across runs: this run raw stderr sha256 `619b4428f7a8577bcc9b3393a0dfb1899e3dfb403b0a70ec87eb0e70341c211c` equals the record-017 archive value, which independently corroborates reproducibility.

## Self-reference boundary (declared)

A record stored in commit T cannot cite T as its own checked-out SHA without content-hash circularity. This record is archived in a subsequent docs-only commit whose code files are byte-identical to `be9ac983c56a6e295feeb0a363d47397abdde930`. The run above checked out `be9ac983c56a6e295feeb0a363d47397abdde930` exactly. After this archive commit, the PR head is expected to remain unchanged pending review (head-freeze declaration in the PR thread).

## Code target blobs (fetched from the exact checked-out commit)

| File | Blob | LF bytes | sha256 (LF blob bytes) |
|---|---|---|---|
| `reference-model/r3_contract_model.py` | `771c1fdc6f8a248a7121d165a0b035cebcc9880c` | 55,526 | `8324ec551749c2d50067967e4a445b26a6683008a4fa52e02da02a9976417a15` |
| `reference-model/test_r3_contract.py` | `22b8d81e7738fe66074f9973932a2dbe79fb52ae` | 91,930 | `26c72ceaa636606118ef94013b7515842d51b02b521c3cb0e6ef4303c72308af` |
| `reference-model/forget_model.py` | `cd623d67400c8870a729f79f88a4413f37bb335a` | 10,738 | `bd03f8203cb90429bdaf57c616f0a2e6003952eb6c4e5f304547b6b31de4bc08` |
| `reference-model/test_forget_model.py` | `633e12db094b703b5f4a431950c3df369dababb0` | 12,266 | `e5ab65f49e327a72a7fdc08653de80ab3b26227ea20ec1f1d9d2f190682fe35f` |

Byte basis: raw Git blob bytes (LF). CRLF working-copy figures remain enumerated in manifest `measurement_basis`. Baseline reconciliation (59 original / 93 source-dev / 103 current exact-Head, canonical 103): see record-017 and manifest `baseline_reconciliation`.

## Per-ID result table (expanded, one row per ID)

| Test ID | Expected assertion | Actual result | PASS/FAIL/NOT IMPLEMENTED/NOT RUN | Output reference | Notes |
|---|---|---|---|---|---|
| DFI-001 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_001` |
| DFI-002 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_002` |
| DFI-003 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_003` |
| DFI-004 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_004` |
| DFI-005 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_005` |
| DFI-006 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_006` |
| DFI-007 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_007` |
| DFI-008 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_008` |
| DFI-009 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_009` |
| DFI-010 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_010` |
| DFI-011 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_011` |
| DFI-012 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_012` |
| DFI-013 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_013` |
| DFI-014 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_014` |
| DFI-015 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_015` |
| DFI-016 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_016` |
| DFI-017 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_017` |
| DFI-018 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_018` |
| DFI-019 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_019` |
| DFI-020 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_020` |
| DFI-021 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_021` |
| DFI-022 | Matrix invariant | pass | PASS | raw output block below | `test_DFI_022` |
| I-U011-T01 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T01` |
| I-U011-T02 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T02` |
| I-U011-T03 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T03` |
| I-U011-T04 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T04` |
| I-U011-T05 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T05` |
| I-U011-T06 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T06` |
| I-U011-T07 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T07` |
| I-U011-T08 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T08` |
| I-U011-T09 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T09` |
| I-U011-T10 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T10` |
| I-U011-T11 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T11` |
| I-U011-T12 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T12` |
| I-U011-T13 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T13` |
| I-U011-T14 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T14` |
| I-U011-T15 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T15` |
| I-U011-T16 | U-011 section 8 invariant | pass | PASS | raw output block below | `test_T16` |
| STOR-01 | Fault schedule | pass | PASS | raw output block below | `test_STOR_01_concurrent_suppression_race` |
| STOR-02 | Fault schedule | pass | PASS | raw output block below | `test_STOR_02_replica_lag_failover` |
| STOR-03 | Fault schedule | pass | PASS | raw output block below | `test_STOR_03_stale_worker_old_lease` |
| STOR-04 | Fault schedule | pass | PASS | raw output block below | `test_STOR_04_duplicate_events_outbox_replay` |
| STOR-05 | Fault schedule | pass | PASS | raw output block below | `test_STOR_05_timeout_retry_reconciliation` |
| STOR-06 | Fault schedule | pass | PASS | raw output block below | `test_STOR_06_restore_isolation_reconciliation` |
| STOR-07 | Fault schedule | pass | PASS | raw output block below | `test_STOR_07_missing_manifest_unknown` |
| AUTH-01 | Authorization matrix invariant | pass | PASS | raw output block below | `test_AUTH_01_missing_authorization` |
| AUTH-02 | Authorization matrix invariant | pass | PASS | raw output block below | `test_AUTH_02_invalid_signature` |
| AUTH-03 | Authorization matrix invariant | pass | PASS | raw output block below | `test_AUTH_03_unknown_issuer` |
| AUTH-04 | Authorization matrix invariant | pass | PASS | raw output block below | `test_AUTH_04_expired_authorization` |
| AUTH-05 | Authorization matrix invariant | pass | PASS | raw output block below | `test_AUTH_05_stale_permission_epoch` |
| AUTH-06 | Authorization matrix invariant | pass | PASS | raw output block below | `test_AUTH_06_phase_mutation_is_not_authority` |
| AUTH-07 | Authorization matrix invariant | pass | PASS | raw output block below | `test_AUTH_07_real_nonce_binding` |
| AUTH-08 | Authorization matrix invariant | pass | PASS | raw output block below | `test_AUTH_08_abort_does_not_consume_nonce` |
| AUTH-09 | Authorization matrix invariant | pass | PASS | raw output block below | `test_AUTH_09_nonce_replay_different_key` |
| AUTH-10 | Authorization matrix invariant | pass | PASS | raw output block below | `test_AUTH_10_fresh_nonce_idempotent_reuse` |
| AUTH-11 | Authorization matrix invariant | pass | PASS | raw output block below | `test_AUTH_11_invalid_auth_idempotent_bypass` |
| AUTH-12 | Authorization matrix invariant | pass | PASS | raw output block below | `test_AUTH_12_not_before` |
| AUTH-13 | Authorization matrix invariant | pass | PASS | raw output block below | `test_AUTH_13_caller_epoch_spoof` |
| AUTH-14 | Authorization matrix invariant | pass | PASS | raw output block below | `test_AUTH_14_stale_delegation` |
| FSTOR-01 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_01_all_projection_faults_rollback` |
| FSTOR-02 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_02_retry_after_each_injected_abort` |
| FSTOR-03 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_03_six_member_projection_exactness` |
| FSTOR-04 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_04_corrupt_six_member_cross_reference_rejected` |
| FSTOR-05 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_05_completion_projection_has_no_domain_side_effect` |
| FSTOR-06 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_06_nonce_projection_rebuild_and_replay_rejection` |
| FSTOR-07 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_07_idempotent_retry_has_complete_independent_audit` |
| FSTOR-08 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_08_lifecycle_terminal_invariant_survives_idempotent_retry` |
| FSTOR-09 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_09_authorization_receipt_is_required_and_single_use` |
| FSTOR-10 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_10_cleanup_allows_existing_retry_but_rejects_first_commit` |
| FSTOR-11 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_11_receipt_credential_verification_and_retry_binding` |
| FSTOR-12 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_12_default_verifier_fails_closed` |
| FSTOR-13 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_13_credential_context_binding_is_mandatory` |
| FSTOR-14 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_14_retry_cannot_cross_operation_identity` |
| FSTOR-15 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_15_retry_reaches_completed_phase` |
| FSTOR-16 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_16_reference_fields_must_match_credential` |
| FSTOR-17 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_17_registry_must_hold_the_authoritative_object` |
| FSTOR-18 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_18_published_commit_identity_must_match_registry` |
| FSTOR-19 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_19_missing_credential_is_rejected` |
| FSTOR-20 | Fault schedule / projection exactness | pass | PASS | raw output block below | `test_FSTOR_20_staged_rejects_missing_credential_and_restores_projection` |
| test_suppression_linearizes_memory_and_fence_together | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_cancel_after_suppression_cannot_restore_access | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_domain_completion_is_separate_from_governance | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_unknown_or_unsupported_cross_system_target_blocks_compliance | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_ack_is_not_erase_evidence | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_notify_ack_can_only_satisfy_notify_action | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_bounded_approved_exception_is_derived_projection_only | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_inventory_expansion_invalidates_prior_evaluation | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_unsupported_capability_cannot_claim_erasure | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_stale_lease_cannot_commit_checkpoint | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_idempotency_key_binds_canonical_request | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_backup_restore_must_apply_latest_fence_before_serving | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_context_remove_does_not_change_canonical_lifecycle | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_denied_authorization_never_suppresses | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_domain_completion_rejects_stale_generation_evidence | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_domain_completion_requires_evidence_reference_and_kind | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_unknown_domain_target_blocks_domain_completion | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_cross_system_inventory_expansion_invalidates_governance_only | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_domain_inventory_expansion_reopens_domain_completion | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_idempotency_hash_binds_every_authority_dimension | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_target_outside_sealed_inventory_cannot_be_recorded | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_unapproved_retention_exception_is_non_compliant | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_idempotency_hash_uses_unambiguous_field_encoding | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |
| test_empty_domain_inventory_cannot_claim_completion | Existing assertions unchanged (forget baseline) | pass | PASS | raw output block below | baseline |

## Raw output (verbatim, stderr as captured; stdout empty)

```text
test_ack_is_not_erase_evidence (test_forget_model.ForgetReferenceModelTests.test_ack_is_not_erase_evidence) ... ok
test_backup_restore_must_apply_latest_fence_before_serving (test_forget_model.ForgetReferenceModelTests.test_backup_restore_must_apply_latest_fence_before_serving) ... ok
test_bounded_approved_exception_is_derived_projection_only (test_forget_model.ForgetReferenceModelTests.test_bounded_approved_exception_is_derived_projection_only) ... ok
test_cancel_after_suppression_cannot_restore_access (test_forget_model.ForgetReferenceModelTests.test_cancel_after_suppression_cannot_restore_access) ... ok
test_context_remove_does_not_change_canonical_lifecycle (test_forget_model.ForgetReferenceModelTests.test_context_remove_does_not_change_canonical_lifecycle) ... ok
test_cross_system_inventory_expansion_invalidates_governance_only (test_forget_model.ForgetReferenceModelTests.test_cross_system_inventory_expansion_invalidates_governance_only) ... ok
test_denied_authorization_never_suppresses (test_forget_model.ForgetReferenceModelTests.test_denied_authorization_never_suppresses) ... ok
test_domain_completion_is_separate_from_governance (test_forget_model.ForgetReferenceModelTests.test_domain_completion_is_separate_from_governance) ... ok
test_domain_completion_rejects_stale_generation_evidence (test_forget_model.ForgetReferenceModelTests.test_domain_completion_rejects_stale_generation_evidence) ... ok
test_domain_completion_requires_evidence_reference_and_kind (test_forget_model.ForgetReferenceModelTests.test_domain_completion_requires_evidence_reference_and_kind) ... ok
test_domain_inventory_expansion_reopens_domain_completion (test_forget_model.ForgetReferenceModelTests.test_domain_inventory_expansion_reopens_domain_completion) ... ok
test_empty_domain_inventory_cannot_claim_completion (test_forget_model.ForgetReferenceModelTests.test_empty_domain_inventory_cannot_claim_completion) ... ok
test_idempotency_hash_binds_every_authority_dimension (test_forget_model.ForgetReferenceModelTests.test_idempotency_hash_binds_every_authority_dimension) ... ok
test_idempotency_hash_uses_unambiguous_field_encoding (test_forget_model.ForgetReferenceModelTests.test_idempotency_hash_uses_unambiguous_field_encoding) ... ok
test_idempotency_key_binds_canonical_request (test_forget_model.ForgetReferenceModelTests.test_idempotency_key_binds_canonical_request) ... ok
test_inventory_expansion_invalidates_prior_evaluation (test_forget_model.ForgetReferenceModelTests.test_inventory_expansion_invalidates_prior_evaluation) ... ok
test_notify_ack_can_only_satisfy_notify_action (test_forget_model.ForgetReferenceModelTests.test_notify_ack_can_only_satisfy_notify_action) ... ok
test_stale_lease_cannot_commit_checkpoint (test_forget_model.ForgetReferenceModelTests.test_stale_lease_cannot_commit_checkpoint) ... ok
test_suppression_linearizes_memory_and_fence_together (test_forget_model.ForgetReferenceModelTests.test_suppression_linearizes_memory_and_fence_together) ... ok
test_target_outside_sealed_inventory_cannot_be_recorded (test_forget_model.ForgetReferenceModelTests.test_target_outside_sealed_inventory_cannot_be_recorded) ... ok
test_unapproved_retention_exception_is_non_compliant (test_forget_model.ForgetReferenceModelTests.test_unapproved_retention_exception_is_non_compliant) ... ok
test_unknown_domain_target_blocks_domain_completion (test_forget_model.ForgetReferenceModelTests.test_unknown_domain_target_blocks_domain_completion) ... ok
test_unknown_or_unsupported_cross_system_target_blocks_compliance (test_forget_model.ForgetReferenceModelTests.test_unknown_or_unsupported_cross_system_target_blocks_compliance) ... ok
test_unsupported_capability_cannot_claim_erasure (test_forget_model.ForgetReferenceModelTests.test_unsupported_capability_cannot_claim_erasure) ... ok
test_FSTOR_01_all_projection_faults_rollback (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_01_all_projection_faults_rollback) ... ok
test_FSTOR_02_retry_after_each_injected_abort (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_02_retry_after_each_injected_abort) ... ok
test_FSTOR_03_six_member_projection_exactness (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_03_six_member_projection_exactness) ... ok
test_FSTOR_04_corrupt_six_member_cross_reference_rejected (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_04_corrupt_six_member_cross_reference_rejected) ... ok
test_FSTOR_05_completion_projection_has_no_domain_side_effect (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_05_completion_projection_has_no_domain_side_effect) ... ok
test_FSTOR_06_nonce_projection_rebuild_and_replay_rejection (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_06_nonce_projection_rebuild_and_replay_rejection)
F-OI-01: reconstruct nonce projection from authoritative records. ... ok
test_FSTOR_07_idempotent_retry_has_complete_independent_audit (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_07_idempotent_retry_has_complete_independent_audit)
F-OI-02: retry authorization is audited without a second commit. ... ok
test_FSTOR_08_lifecycle_terminal_invariant_survives_idempotent_retry (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_08_lifecycle_terminal_invariant_survives_idempotent_retry)
F-OI-03: idempotent retry must never restore Forgotten lifecycle. ... ok
test_FSTOR_09_authorization_receipt_is_required_and_single_use (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_09_authorization_receipt_is_required_and_single_use)
F-OI-04: missing or reused receipts are rejected; fresh retry receipt is audited. ... ok
test_FSTOR_10_cleanup_allows_existing_retry_but_rejects_first_commit (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_10_cleanup_allows_existing_retry_but_rejects_first_commit)
F-D-NEW-01: CLEANUP permits a fresh-authorized retry only. ... ok
test_FSTOR_11_receipt_credential_verification_and_retry_binding (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_11_receipt_credential_verification_and_retry_binding)
F-OI-04: reject forged/mismatched credentials and bind valid retry. ... ok
test_FSTOR_12_default_verifier_fails_closed (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_12_default_verifier_fails_closed)
A production-default model must reject every credential. ... ok
test_FSTOR_13_credential_context_binding_is_mandatory (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_13_credential_context_binding_is_mandatory)
F-OI-04: no empty or placeholder value may bypass a binding check. ... ok
test_FSTOR_14_retry_cannot_cross_operation_identity (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_14_retry_cannot_cross_operation_identity)
F-D-NEW-02: an idempotency key is not shareable across operations. ... ok
test_FSTOR_15_retry_reaches_completed_phase (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_15_retry_reaches_completed_phase)
F-D-NEW-01: COMPLETED is also a legitimate retry phase. ... ok
test_FSTOR_16_reference_fields_must_match_credential (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_16_reference_fields_must_match_credential)
F-STOR-20261119-01 / F-OI-04 residual: projection consistency. ... ok
test_FSTOR_17_registry_must_hold_the_authoritative_object (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_17_registry_must_hold_the_authoritative_object)
U-058 (a): identity, not value equality — registry side. ... ok
test_FSTOR_18_published_commit_identity_must_match_registry (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_18_published_commit_identity_must_match_registry)
U-058 (a) complement: the published side of the identity check. ... ok
test_FSTOR_19_missing_credential_is_rejected (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_19_missing_credential_is_rejected)
F-STOR-20261119-01 residual: absent credential, not just mismatch. ... ok
test_FSTOR_20_staged_rejects_missing_credential_and_restores_projection (test_r3_contract.AtomicPublicationFaultInjection.test_FSTOR_20_staged_rejects_missing_credential_and_restores_projection)
F-STOR-20261119-03: real staged rollback, not a direct validator call. ... ok
test_AUTH_01_missing_authorization (test_r3_contract.AuthorizationCommitEntry.test_AUTH_01_missing_authorization) ... ok
test_AUTH_02_invalid_signature (test_r3_contract.AuthorizationCommitEntry.test_AUTH_02_invalid_signature) ... ok
test_AUTH_03_unknown_issuer (test_r3_contract.AuthorizationCommitEntry.test_AUTH_03_unknown_issuer) ... ok
test_AUTH_04_expired_authorization (test_r3_contract.AuthorizationCommitEntry.test_AUTH_04_expired_authorization) ... ok
test_AUTH_05_stale_permission_epoch (test_r3_contract.AuthorizationCommitEntry.test_AUTH_05_stale_permission_epoch) ... ok
test_AUTH_06_phase_mutation_is_not_authority (test_r3_contract.AuthorizationCommitEntry.test_AUTH_06_phase_mutation_is_not_authority) ... ok
test_AUTH_07_real_nonce_binding (test_r3_contract.AuthorizationCommitEntry.test_AUTH_07_real_nonce_binding) ... ok
test_AUTH_08_abort_does_not_consume_nonce (test_r3_contract.AuthorizationCommitEntry.test_AUTH_08_abort_does_not_consume_nonce) ... ok
test_AUTH_09_nonce_replay_different_key (test_r3_contract.AuthorizationCommitEntry.test_AUTH_09_nonce_replay_different_key) ... ok
test_AUTH_10_fresh_nonce_idempotent_reuse (test_r3_contract.AuthorizationCommitEntry.test_AUTH_10_fresh_nonce_idempotent_reuse) ... ok
test_AUTH_11_invalid_auth_idempotent_bypass (test_r3_contract.AuthorizationCommitEntry.test_AUTH_11_invalid_auth_idempotent_bypass) ... ok
test_AUTH_12_not_before (test_r3_contract.AuthorizationCommitEntry.test_AUTH_12_not_before) ... ok
test_AUTH_13_caller_epoch_spoof (test_r3_contract.AuthorizationCommitEntry.test_AUTH_13_caller_epoch_spoof) ... ok
test_AUTH_14_stale_delegation (test_r3_contract.AuthorizationCommitEntry.test_AUTH_14_stale_delegation) ... ok
test_DFI_001 (test_r3_contract.DFI.test_DFI_001) ... ok
test_DFI_002 (test_r3_contract.DFI.test_DFI_002) ... ok
test_DFI_003 (test_r3_contract.DFI.test_DFI_003) ... ok
test_DFI_004 (test_r3_contract.DFI.test_DFI_004) ... ok
test_DFI_005 (test_r3_contract.DFI.test_DFI_005) ... ok
test_DFI_006 (test_r3_contract.DFI.test_DFI_006) ... ok
test_DFI_007 (test_r3_contract.DFI.test_DFI_007) ... ok
test_DFI_008 (test_r3_contract.DFI.test_DFI_008) ... ok
test_DFI_009 (test_r3_contract.DFI.test_DFI_009) ... ok
test_DFI_010 (test_r3_contract.DFI.test_DFI_010) ... ok
test_DFI_011 (test_r3_contract.DFI.test_DFI_011) ... ok
test_DFI_012 (test_r3_contract.DFI.test_DFI_012) ... ok
test_DFI_013 (test_r3_contract.DFI.test_DFI_013)
Sequential fence interleavings only; NOT a concurrency proof. ... ok
test_DFI_014 (test_r3_contract.DFI.test_DFI_014) ... ok
test_DFI_015 (test_r3_contract.DFI.test_DFI_015) ... ok
test_DFI_016 (test_r3_contract.DFI.test_DFI_016) ... ok
test_DFI_017 (test_r3_contract.DFI.test_DFI_017) ... ok
test_DFI_018 (test_r3_contract.DFI.test_DFI_018) ... ok
test_DFI_019 (test_r3_contract.DFI.test_DFI_019) ... ok
test_DFI_020 (test_r3_contract.DFI.test_DFI_020) ... ok
test_DFI_021 (test_r3_contract.DFI.test_DFI_021)
In-memory pre-publication abort; not WAL or crash durability. ... ok
test_DFI_022 (test_r3_contract.DFI.test_DFI_022) ... ok
test_T01 (test_r3_contract.OwnerIU011.test_T01) ... ok
test_T02 (test_r3_contract.OwnerIU011.test_T02) ... ok
test_T03 (test_r3_contract.OwnerIU011.test_T03) ... ok
test_T04 (test_r3_contract.OwnerIU011.test_T04) ... ok
test_T05 (test_r3_contract.OwnerIU011.test_T05) ... ok
test_T06 (test_r3_contract.OwnerIU011.test_T06) ... ok
test_T07 (test_r3_contract.OwnerIU011.test_T07) ... ok
test_T08 (test_r3_contract.OwnerIU011.test_T08) ... ok
test_T09 (test_r3_contract.OwnerIU011.test_T09) ... ok
test_T10 (test_r3_contract.OwnerIU011.test_T10) ... ok
test_T11 (test_r3_contract.OwnerIU011.test_T11) ... ok
test_T12 (test_r3_contract.OwnerIU011.test_T12) ... ok
test_T13 (test_r3_contract.OwnerIU011.test_T13) ... ok
test_T14 (test_r3_contract.OwnerIU011.test_T14) ... ok
test_T15 (test_r3_contract.OwnerIU011.test_T15) ... ok
test_T16 (test_r3_contract.OwnerIU011.test_T16) ... ok
test_STOR_01_concurrent_suppression_race (test_r3_contract.StorageFaults.test_STOR_01_concurrent_suppression_race)
Real two-thread shared-boundary race, not sequential duplicate. ... ok
test_STOR_02_replica_lag_failover (test_r3_contract.StorageFaults.test_STOR_02_replica_lag_failover) ... ok
test_STOR_03_stale_worker_old_lease (test_r3_contract.StorageFaults.test_STOR_03_stale_worker_old_lease) ... ok
test_STOR_04_duplicate_events_outbox_replay (test_r3_contract.StorageFaults.test_STOR_04_duplicate_events_outbox_replay) ... ok
test_STOR_05_timeout_retry_reconciliation (test_r3_contract.StorageFaults.test_STOR_05_timeout_retry_reconciliation) ... ok
test_STOR_06_restore_isolation_reconciliation (test_r3_contract.StorageFaults.test_STOR_06_restore_isolation_reconciliation) ... ok
test_STOR_07_missing_manifest_unknown (test_r3_contract.StorageFaults.test_STOR_07_missing_manifest_unknown) ... ok

----------------------------------------------------------------------
Ran 103 tests in 0.007s

OK
```

## Exact-Head CI cross-references at `be9ac983c56a6e295feeb0a363d47397abdde930`

- `Non-production reference model unit tests` run 44556424744 — success
- `GOV-DOC-001 structural checks` run 44556424766 — success
- `Strict Manifest YAML parse and required-field checks` run 44556424836 — success

## Evidence level

Contract-level reference-model consistency suite only; no production R3 conformance. Production-only gaps remain NOT IMPLEMENTED / NOT RUN per RUNBOOK.

(Coordinator mechanical evidence record | EXEC-RECORD-018 | closes R2 minimal fix B-02/N-01 | 2026-11-19T15:41:59Z)
