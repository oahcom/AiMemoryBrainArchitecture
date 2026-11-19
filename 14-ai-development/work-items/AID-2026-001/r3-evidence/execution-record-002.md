# R3 Execution Record 002 (Coordinator Local Execution)

- Timestamp: 2026-11-19 11:44:49 (UTC+8)
- Executor: WorkBuddy coordinator (Git Bash / Python 3.13.14)
- Command: `python -m unittest discover -v` (cwd: reference-model/)
- Commit under test: `6f90fbc5a19a69eb4c276564cf2496174a4b2f05` (parent `26fb0347a6b148c7bb87e46412f8f35a8892e4fd`)
- Model blob: `3dcde767ec5c878e66a105d536ad9e3e22620cb2` (20,059 bytes, sha256 4dcd92e8baa45b94…)
- Test blob: `07270582e000b3bef97ea1b5abc16ad859c80269` (17,762 bytes, sha256 43f0a4358e59a0ed…)

## Result

Ran 59 tests in 0.002s
OK
Exit code: 0

## Provenance

- Code content authored by ChatGPT session `6afe6dad-62a0-83e8-bdf5-c048f5b476d0` (U-047), including a self-discovered T15 erratum (`completion_projection_allowed` no longer calls `domain_complete`) applied before commit.
- Commit made by coordinator (delivery-mode change: session delivers file content, coordinator commits — avoids session-side Git Tree failures seen in U-045/046).
- Test execution by coordinator on local Python 3.13.14. No fabricated output.

## Evidence level (honest)

Contract-level reference model consistency evidence. NOT production runtime persistence proof.
DFI-021 model tests passing is NOT real Crash/Failover/WAL evidence.
18 production-level gaps (real WAL receipts, real replica inventories, real backup restores, etc.) remain NOT IMPLEMENTED / NOT RUN.

## stdout (raw)

```
(empty — unittest writes to stderr)
```

## stderr (raw, unittest writes here)

```
test_ack_is_not_erase_evidence (test_forget_model.ForgetReferenceModelTests.test_ack_is_not_erase_evidence) ... ok
test_backup_restore_must_apply_latest_fence_before_serving (test_forget_model.ForgetReferenceModelTests.test_backup_restore_must_apply_latest_fence_before_serving) ... ok
test_bounded_approved_exception_is_derived_projection_only (test_forget_model.ForgetReferenceModelTests.test_bounded_approved_exception_is_derived_projection_only) ... ok
test_cancel_after_suppression_cannot_restore_access (test_forget_model.ForgetReferenceModelTests.test_cancel_after_suppression_cannot_restore_access) ... ok
test_context_remove_does_not_change_canonical_lifecycle (test_forget_model.ForgetReferenceModelTests.test_context_remove_does_not_change_canonical_lifecycle) ... ok
test_denied_authorization_never_suppresses (test_forget_model.ForgetReferenceModelTests.test_denied_authorization_never_suppresses) ... ok
test_domain_completion_is_separate_from_governance (test_forget_model.ForgetReferenceModelTests.test_domain_completion_is_separate_from_governance) ... ok
test_idempotency_key_binds_canonical_request (test_forget_model.ForgetReferenceModelTests.test_idempotency_key_binds_canonical_request) ... ok
test_inventory_expansion_invalidates_prior_evaluation (test_forget_model.ForgetReferenceModelTests.test_inventory_expansion_invalidates_prior_evaluation) ... ok
test_notify_ack_can_only_satisfy_notify_action (test_forget_model.ForgetReferenceModelTests.test_notify_ack_can_only_satisfy_notify_action) ... ok
test_stale_lease_cannot_commit_checkpoint (test_forget_model.ForgetReferenceModelTests.test_stale_lease_cannot_commit_checkpoint) ... ok
test_suppression_linearizes_memory_and_fence_together (test_forget_model.ForgetReferenceModelTests.test_suppression_linearizes_memory_and_fence_together) ... ok
test_unknown_or_unsupported_cross_system_target_blocks_compliance (test_forget_model.ForgetReferenceModelTests.test_unknown_or_unsupported_cross_system_target_blocks_compliance) ... ok
test_unsupported_capability_cannot_claim_erasure (test_forget_model.ForgetReferenceModelTests.test_unsupported_capability_cannot_claim_erasure) ... ok
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
test_DFI_013 (test_r3_contract.DFI.test_DFI_013) ... ok
test_DFI_014 (test_r3_contract.DFI.test_DFI_014) ... ok
test_DFI_015 (test_r3_contract.DFI.test_DFI_015) ... ok
test_DFI_016 (test_r3_contract.DFI.test_DFI_016) ... ok
test_DFI_017 (test_r3_contract.DFI.test_DFI_017) ... ok
test_DFI_018 (test_r3_contract.DFI.test_DFI_018) ... ok
test_DFI_019 (test_r3_contract.DFI.test_DFI_019) ... ok
test_DFI_020 (test_r3_contract.DFI.test_DFI_020) ... ok
test_DFI_021 (test_r3_contract.DFI.test_DFI_021) ... ok
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
test_STOR_01_concurrent_suppression_race (test_r3_contract.StorageFaults.test_STOR_01_concurrent_suppression_race) ... ok
test_STOR_02_replica_lag_failover (test_r3_contract.StorageFaults.test_STOR_02_replica_lag_failover) ... ok
test_STOR_03_stale_worker_old_lease (test_r3_contract.StorageFaults.test_STOR_03_stale_worker_old_lease) ... ok
test_STOR_04_duplicate_events_outbox_replay (test_r3_contract.StorageFaults.test_STOR_04_duplicate_events_outbox_replay) ... ok
test_STOR_05_timeout_retry_reconciliation (test_r3_contract.StorageFaults.test_STOR_05_timeout_retry_reconciliation) ... ok
test_STOR_06_restore_isolation_reconciliation (test_r3_contract.StorageFaults.test_STOR_06_restore_isolation_reconciliation) ... ok
test_STOR_07_missing_manifest_unknown (test_r3_contract.StorageFaults.test_STOR_07_missing_manifest_unknown) ... ok

----------------------------------------------------------------------
Ran 59 tests in 0.002s

OK
```
