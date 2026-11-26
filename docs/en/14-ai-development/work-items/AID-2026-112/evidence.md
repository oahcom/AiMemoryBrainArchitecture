---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-112/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Local WSL2 records mapped conservatively by test name; 36 SC/HIR predicates: 27 PARTIAL_EVIDENCE, 9 UNCHANGED, 0 PASS; all 72 AID-095 flow cells remain NOT EVIDENCED."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Canonical
    canonical_scope: "AID-2026-112 supplemental exact-head local implementation-test evidence and conservative SC/HIR rejudgment"
    canonical_scope_id: "ai-development/aid-2026-112-sc-hir-test-evidence-rejudgment"
    canonical_scope_keywords: [storage-consistency, h-idempotency, sqlite, memory-context, test-evidence]
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: "docs/en/14-ai-development/work-items/AID-2026-112/evidence.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-112/evidence.md"
---
# AID-2026-112 — SC/HIR predicate rejudgment against 552 local test passes

- Work item: AID-2026-112; id_status: PROVISIONAL.
- Attribution: user-authorized operator (delegated by account owner); date: 2026-11-26.
- alloc_at_push verified immediately before push: main=57767952f1248e2de616c5dc24ac762ecb3a5a7f; INDEX maximum=AID-2026-111; AID-2026-112 directory and INDEX row absent; id_status=PROVISIONAL.
- This supplements merged AID-2026-107 without rewriting its historical result.
- 36 SC/HIR predicates: 27 PARTIAL_EVIDENCE / 9 UNCHANGED / 0 PASS.
- AID-095 72 end-to-end checkpoints: 72 UNCHANGED / 0 PASS.
- 16 EVIDENCE_REQUIRED rows: 12 PARTIAL_EVIDENCE / 4 UNCHANGED / 0 PASS.
- Gate A PARTIAL / OPEN; Gate B PARTIAL / OPEN — NOT VERIFIED.

## 1. Evidence rules

Map only by literal test-name and predicate semantics. A mapping is not full predicate satisfaction. PASS requires named tests to cover the entire predicate; none meets that threshold. The 276 pure-Rust group is aggregate-only, with no individual names. Of 99 SQLite passes, 94 names were supplied and five are NOT_RECORDED. Of 177 memory-context passes, 23 relevant names were supplied and 154 are NOT_RECORDED.

## 2. Per-test mapping of all 117 supplied names

| # | Group | Test name | Predicate mapping | Mapping note |
|---:|---|---|---|---|
| 1 | SQLite | committed_payload_survives_process_crash_and_wal_recovery | SC-04, SC-05, HIR-16 | Name supports only the named local behavior, not the complete predicate. |
| 2 | SQLite | concurrent_appends_preserve_unique_order_and_payload_custody | SC-09, HIR-08 | Name supports only the named local behavior, not the complete predicate. |
| 3 | SQLite | concurrent_forget_waits_for_restore_snapshot_lock | SC-09, HIR-08 | Name supports only the named local behavior, not the complete predicate. |
| 4 | SQLite | crash_after_fence_commit_is_retried_without_resurrection | SC-13, HIR-18 | Name supports only the named local behavior, not the complete predicate. |
| 5 | SQLite | failed_payload_insert_rolls_back_event_payload_and_outbox_rows | SC-01, SC-02, SC-07, SC-08 | Name supports only the named local behavior, not the complete predicate. |
| 6 | SQLite | fence_restore_purges_one_scope_from_a_store_built_database | SC-13, HIR-18 | Name supports only the named local behavior, not the complete predicate. |
| 7 | SQLite | forget_fence::tests::concurrent_forget_serializes_behind_restore_fence_lock | SC-13, HIR-18 | Name supports only the named local behavior, not the complete predicate. |
| 8 | SQLite | forget_fence::tests::crash_after_fence_commit_is_retried_safely_on_restore | SC-13, HIR-18 | Name supports only the named local behavior, not the complete predicate. |
| 9 | SQLite | forget_fence::tests::malformed_scope_refuses_activation_without_partial_change | SC-13, HIR-18 | Name supports only the named local behavior, not the complete predicate. |
| 10 | SQLite | forget_fence::tests::missing_or_corrupt_fence_fails_closed | SC-13, HIR-18 | Name supports only the named local behavior, not the complete predicate. |
| 11 | SQLite | forget_fence::tests::restore_anti_resurrection_purges_only_fenced_scope_across_all_tables | SC-13, HIR-18 | Name supports only the named local behavior, not the complete predicate. |
| 12 | SQLite | live_wal_copy_fails_closed_until_checkpointed | SC-04, SC-05, HIR-16 | Name supports only the named local behavior, not the complete predicate. |
| 13 | SQLite | malformed_scope_refuses_activation_without_partial_change | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 14 | SQLite | missing_or_corrupt_fence_fails_closed | SC-13, HIR-18 | Name supports only the named local behavior, not the complete predicate. |
| 15 | SQLite | ordered_read_rejects_payload_and_verified_digest_tampering | SC-01, SC-02, SC-07, SC-08 | Name supports only the named local behavior, not the complete predicate. |
| 16 | SQLite | payload::tests::duplicate_payload_append_returns_original_receipt_without_duplicate_rows | SC-07, SC-08, HIR-10, HIR-14 | Name supports only the named local behavior, not the complete predicate. |
| 17 | SQLite | payload::tests::payload_append_receipt_and_ordered_read_survive_reopen | SC-07, SC-08, HIR-10, HIR-14 | Name supports only the named local behavior, not the complete predicate. |
| 18 | SQLite | payload::tests::payload_digest_mismatch_is_rejected_before_append | SC-01, SC-02, SC-07, SC-08 | Name supports only the named local behavior, not the complete predicate. |
| 19 | SQLite | payload::tests::read_after_fails_closed_on_empty_persisted_scope_list | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 20 | SQLite | payload::tests::read_after_fails_closed_on_invalid_persisted_scope_ref | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 21 | SQLite | payload::tests::read_after_paginates_interleaved_scope_rows_by_visible_limit | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 22 | SQLite | payload::tests::read_after_skips_non_intersecting_scopes_and_limits_visible_rows | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 23 | SQLite | payload_persistence_boundary_sizes_survive_reopen | SC-01, SC-02, SC-07, SC-08 | Name supports only the named local behavior, not the complete predicate. |
| 24 | SQLite | restart_preserves_receipt_and_idempotent_payload_replay | SC-07, SC-08, HIR-10, HIR-14 | Name supports only the named local behavior, not the complete predicate. |
| 25 | SQLite | restore_anti_resurrection_and_preserves_other_scope | SC-13, HIR-18 | Name supports only the named local behavior, not the complete predicate. |
| 26 | SQLite | tests::abrupt_exit_worker | No corresponding test | No SC/HIR predicate corresponds to this test name. |
| 27 | SQLite | tests::abrupt_process_exit_rolls_back_entire_uncommitted_commit | No corresponding test | No SC/HIR predicate corresponds to this test name. |
| 28 | SQLite | tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable | SC-07, SC-08, HIR-10, HIR-14 | Name supports only the named local behavior, not the complete predicate. |
| 29 | SQLite | tests::empty_scope_and_missing_payload_identity_are_rejected | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 30 | SQLite | tests::f1_forget_memory_hides_current_and_history | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 31 | SQLite | tests::f10_forget_survives_reopen | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 32 | SQLite | tests::f2_forget_memory_excludes_from_change_pages | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 33 | SQLite | tests::f3_forget_memory_rejects_new_commit | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 34 | SQLite | tests::f4_forget_memory_rejects_prepare_and_publish | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 35 | SQLite | tests::f5_forget_memory_blocks_idempotency_replay | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 36 | SQLite | tests::f6_forget_is_idempotent | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 37 | SQLite | tests::f7_forget_version_only_hides_that_version | No corresponding test | No SC/HIR predicate corresponds to this test name. |
| 38 | SQLite | tests::f8_forget_version_blocks_child_commit | No corresponding test | No SC/HIR predicate corresponds to this test name. |
| 39 | SQLite | tests::f9_forget_memory_sets_lifecycle_state | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 40 | SQLite | tests::file_backed_connection_applies_required_sqlite_pragmas | SC-04 | Name supports only the named local behavior, not the complete predicate. |
| 41 | SQLite | tests::file_db_busy_timeout_bounds_wait_for_long_immediate_transaction | SC-09, HIR-08 | Name supports only the named local behavior, not the complete predicate. |
| 42 | SQLite | tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent | SC-02, SC-03, SC-06, HIR-11, HIR-16 | Name supports only the named local behavior, not the complete predicate. |
| 43 | SQLite | tests::file_db_nested_savepoint_rollback_preserves_outer_work | SC-02 | Name supports only the named local behavior, not the complete predicate. |
| 44 | SQLite | tests::file_db_unwinding_worker_releases_open_transaction_without_partial_state | SC-02, SC-03, SC-06, HIR-11, HIR-16 | Name supports only the named local behavior, not the complete predicate. |
| 45 | SQLite | tests::independent_connections_serialize_conflicting_idempotency_payloads | SC-08, HIR-01, HIR-08, HIR-14 | Name supports only the named local behavior, not the complete predicate. |
| 46 | SQLite | tests::multi_process_cas_worker | No corresponding test | No SC/HIR predicate corresponds to this test name. |
| 47 | SQLite | tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt | SC-07, SC-08, HIR-10, HIR-14 | Name supports only the named local behavior, not the complete predicate. |
| 48 | SQLite | tests::pending_compile_intent_carries_the_payload_and_envelope_a_compiler_needs | SC-15 | Name supports only the named local behavior, not the complete predicate. |
| 49 | SQLite | tests::pending_compile_intent_created_at_matches_the_acceptance_time | SC-15 | Name supports only the named local behavior, not the complete predicate. |
| 50 | SQLite | tests::pending_compile_intent_fails_closed_when_stored_payload_is_tampered_with | SC-15 | Name supports only the named local behavior, not the complete predicate. |
| 51 | SQLite | tests::pending_compile_intent_is_invisible_when_no_payload_was_stored | SC-15 | Name supports only the named local behavior, not the complete predicate. |
| 52 | SQLite | tests::pending_compile_intents_fails_closed_when_stored_bytes_are_tampered | SC-15 | Name supports only the named local behavior, not the complete predicate. |
| 53 | SQLite | tests::pending_compile_intents_is_empty_on_a_fresh_store | SC-15 | Name supports only the named local behavior, not the complete predicate. |
| 54 | SQLite | tests::pending_compile_intents_is_idempotent_and_does_not_consume | SC-15 | Name supports only the named local behavior, not the complete predicate. |
| 55 | SQLite | tests::pending_compile_intents_returns_accepted_events_in_insertion_order | SC-15 | Name supports only the named local behavior, not the complete predicate. |
| 56 | SQLite | tests::same_producer_key_and_digest_replay_original_receipt | SC-08, SC-15, HIR-02, HIR-14 | Name supports only the named local behavior, not the complete predicate. |
| 57 | SQLite | tests::same_producer_key_with_different_digest_conflicts | SC-08, SC-15, HIR-02, HIR-14 | Name supports only the named local behavior, not the complete predicate. |
| 58 | SQLite | tests::separate_processes_serialize_competing_file_backed_cas_writers | SC-09, HIR-08 | Name supports only the named local behavior, not the complete predicate. |
| 59 | SQLite | tests::sqlite_change_listing_surfaces_corrupt_scope_metadata_instead_of_silently_skipping_it | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 60 | SQLite | tests::sqlite_change_pages_filter_scope_before_applying_limit | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 61 | SQLite | tests::sqlite_change_pages_with_limit_two_preserve_order_without_skips_or_duplicates | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 62 | SQLite | tests::sqlite_denies_fresh_cross_scope_write_without_persisting_any_commit_state | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 63 | SQLite | tests::sqlite_does_not_replay_idempotency_key_across_memories | SC-08, HIR-01, HIR-08, HIR-14 | Name supports only the named local behavior, not the complete predicate. |
| 64 | SQLite | tests::sqlite_does_not_replay_idempotency_receipt_before_scope_check | SC-07, SC-08, HIR-10, HIR-14 | Name supports only the named local behavior, not the complete predicate. |
| 65 | SQLite | tests::sqlite_filters_nested_claims_by_the_callers_scope | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 66 | SQLite | tests::sqlite_hides_entire_multiscope_claim_from_partial_scope_reader | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 67 | SQLite | tests::sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup | SC-07, SC-08, HIR-10, HIR-14 | Name supports only the named local behavior, not the complete predicate. |
| 68 | SQLite | tests::sqlite_multiple_preparations_reserve_unique_negative_sequences | SC-01, SC-03 | Name supports only the named local behavior, not the complete predicate. |
| 69 | SQLite | tests::sqlite_prepare_does_not_add_change_log_entries | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 70 | SQLite | tests::sqlite_prepare_hides_version_from_read_version | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 71 | SQLite | tests::sqlite_prepare_keeps_current_version_unchanged | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 72 | SQLite | tests::sqlite_prepare_rejects_idempotency_digest_conflict | SC-08, HIR-01, HIR-08, HIR-14 | Name supports only the named local behavior, not the complete predicate. |
| 73 | SQLite | tests::sqlite_prepare_replay_returns_same_receipt | SC-07, SC-08, HIR-10, HIR-14 | Name supports only the named local behavior, not the complete predicate. |
| 74 | SQLite | tests::sqlite_publication_state_honours_scope_and_forget_fences | SC-13, HIR-18 | Name supports only the named local behavior, not the complete predicate. |
| 75 | SQLite | tests::sqlite_publication_state_reports_prepared_hidden_then_published | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 76 | SQLite | tests::sqlite_publication_state_returns_none_for_unknown_or_legacy_publication | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 77 | SQLite | tests::sqlite_publish_allocates_sequence_only_at_publish_time | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 78 | SQLite | tests::sqlite_publish_makes_prepared_version_current_and_readable | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 79 | SQLite | tests::sqlite_publish_rejects_duplicate_publication_and_suppressed_state | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 80 | SQLite | tests::sqlite_publish_rejects_stale_parent_without_partial_commit | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 81 | SQLite | tests::sqlite_publish_replay_returns_original_receipt | SC-07, SC-08, HIR-10, HIR-14 | Name supports only the named local behavior, not the complete predicate. |
| 82 | SQLite | tests::sqlite_read_version_keeps_legacy_versions_visible | SC-10 | Name supports only the named local behavior, not the complete predicate. |
| 83 | SQLite | tests::sqlite_rejects_claim_scope_outside_callers_scope_even_when_parent_contains_it | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 84 | SQLite | tests::sqlite_rejects_claims_outside_the_parent_memory_scope | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 85 | SQLite | tests::sqlite_rejects_create_outside_requested_scope | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 86 | SQLite | tests::sqlite_rejects_empty_idempotency_key_or_request_digest | SC-08, HIR-01, HIR-08, HIR-14 | Name supports only the named local behavior, not the complete predicate. |
| 87 | SQLite | tests::sqlite_rejects_invalid_memory_and_orphan_initial_version_pointer | No corresponding test | No SC/HIR predicate corresponds to this test name. |
| 88 | SQLite | tests::sqlite_rejects_invalid_version_fields_before_writing_any_commit_state | No corresponding test | No SC/HIR predicate corresponds to this test name. |
| 89 | SQLite | tests::sqlite_rejects_malformed_nested_claims_before_commit | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 90 | SQLite | tests::sqlite_rejects_mixed_parent_and_foreign_claim_scopes_before_commit | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 91 | SQLite | tests::sqlite_rejects_stale_expected_version | SC-02, SC-03 | Name supports only the named local behavior, not the complete predicate. |
| 92 | SQLite | tests::sqlite_storage_entry_points_reject_empty_and_malformed_scope_sets | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 93 | SQLite | tests::startup_backfills_compile_intent_for_preexisting_accepted_events | SC-15 | Name supports only the named local behavior, not the complete predicate. |
| 94 | SQLite | tests::status_and_replay_enforce_scope | SC-02, SC-10, HIR-01 | Name supports only the named local behavior, not the complete predicate. |
| 95 | memory-context | ack_targets_delivery_not_attempt | SC-16, HIR-03, HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 96 | memory-context | ledger_tracks_multiple_attempts_per_delivery | SC-16, HIR-03, HIR-15, HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 97 | memory-context | ledger_rejects_duplicate_attempt_id | HIR-15, HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 98 | memory-context | ledger_rejects_forked_attempt_chain | HIR-15, HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 99 | memory-context | retry_increments_attempt_number_and_links_previous | SC-16, HIR-03, HIR-15, HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 100 | memory-context | zero_max_attempts_is_rejected | No corresponding test | No SC/HIR predicate corresponds to this test name. |
| 101 | memory-context | pending_delivery_cannot_be_marked_delivered_without_attempt | SC-16, HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 102 | memory-context | superseded_delivery_cannot_be_marked_delivered | SC-16, HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 103 | memory-context | abandoned_delivery_cannot_transition_back_to_delivered | SC-16, HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 104 | memory-context | abandoned_delivery_rejects_ack_for_current_attempt | SC-16, HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 105 | memory-context | abandoned_delivery_rejects_ack_for_obsolete_attempt | SC-16, HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 106 | memory-context | acknowledged_delivery_cannot_be_superseded | SC-16, HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 107 | memory-context | acknowledged_delivery_cannot_record_another_attempt | HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 108 | memory-context | obsolete_attempt_ack_is_counted_as_stale | HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 109 | memory-context | ack_for_current_attempt_is_current | HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 110 | memory-context | ack_for_unknown_delivery_is_unknown | HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 111 | memory-context | normal_delivery_acknowledgement_path | SC-16, HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 112 | memory-context | retry_exhaustion_abandons_delivery | SC-16, HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 113 | memory-context | delivery_states_are_tallied_on_separate_axes_and_never_folded_together | SC-16, HIR-17 | Name supports only the named local behavior, not the complete predicate. |
| 114 | memory-context | the_delivery_report_carries_counts_only_and_no_delivery_identifiers | No corresponding test | No SC/HIR predicate corresponds to this test name. |
| 115 | memory-context | delivery_intent_snapshot_json_round_trips_to_equivalent_snapshot | No corresponding test | No SC/HIR predicate corresponds to this test name. |
| 116 | memory-context | delivery_intent_targets_snapshot_context_version | SC-16 | Name supports only the named local behavior, not the complete predicate. |
| 117 | memory-context | delivery_intent_visibility_is_always_private_pending_gate | SC-16 | Name supports only the named local behavior, not the complete predicate. |

## 3. SC-01…SC-18 predicate-by-predicate rejudgment

| ID | Result | Supporting test names | Why not PASS / missing part |
|---|---|---|---|
| SC-01 | PARTIAL_EVIDENCE | failed_payload_insert_rolls_back_event_payload_and_outbox_rows; file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent; abrupt_process_exit_rolls_back_entire_uncommitted_commit | Only selected rollback/write-set parts are named. Missing one transaction test covering immutable payload/version, CAS pointer, Owner cursor, idempotency, outbox and receipt together. Compile-intent tests are SC-15. |
| SC-02 | PARTIAL_EVIDENCE | sqlite_denies_fresh_cross_scope_write_without_persisting_any_commit_state; sqlite_rejects_invalid_version_fields_before_writing_any_commit_state; file_db_nested_savepoint_rollback_preserves_outer_work | Selected validation and rollback cases are named. Missing exhaustive rejection matrix proving no partial visible write and no success receipt for every abort. |
| SC-03 | PARTIAL_EVIDENCE | committed_payload_survives_process_crash_and_wal_recovery; acceptance_persists_across_reopen_and_receipt_replay_is_stable; file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent | Commit/reopen and interrupted commit are named. Missing proof durable commit is the sole linearization point for all participants/coordinator outcomes. |
| SC-04 | PARTIAL_EVIDENCE | committed_payload_survives_process_crash_and_wal_recovery; live_wal_copy_fails_closed_until_checkpointed; file_backed_connection_applies_required_sqlite_pragmas | WAL recovery/copy guard/configuration are named. Missing device flush barrier, log-before-data ordering, framing and commit-marker fault injection. |
| SC-05 | PARTIAL_EVIDENCE | live_wal_copy_fails_closed_until_checkpointed; committed_payload_survives_process_crash_and_wal_recovery | Checkpoint gating and WAL recovery are named. Missing checkpoint-position/atomicity and contiguous valid-prefix replay/gap/truncation tests. |
| SC-06 | PARTIAL_EVIDENCE | abrupt_process_exit_rolls_back_entire_uncommitted_commit; file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent; ordered_read_rejects_payload_and_verified_digest_tampering | Rollback and selected tamper cases are named. Missing torn/partial record injection, database corruption quarantine and crash-safe restore activation. |
| SC-07 | PARTIAL_EVIDENCE | payload_append_receipt_and_ordered_read_survive_reopen; duplicate_payload_append_returns_original_receipt_without_duplicate_rows; acceptance_persists_across_reopen_and_receipt_replay_is_stable | Receipt persistence/replay is named. Missing all minimum receipt fields and COMMITTED/ABORTED/UNKNOWN outcomes. No named ABORTED path; StorageError has no ABORTED variant and PublicationState has only two states. |
| SC-08 | PARTIAL_EVIDENCE | concurrent_identical_idempotency_requests_replay_one_durable_receipt; sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup; sqlite_does_not_replay_idempotency_key_across_memories | Same-key replay, digest conflict and scope separation are named. Missing complete GID+participant+digest identity and all participant/backend combinations. |
| SC-09 | PARTIAL_EVIDENCE | independent_connections_serialize_conflicting_idempotency_payloads; separate_processes_serialize_competing_file_backed_cas_writers; file_db_busy_timeout_bounds_wait_for_long_immediate_transaction | SQLite connection/process serialization is named. Missing selected isolation profile and coverage of every declared conflicting-operation class. |
| SC-10 | PARTIAL_EVIDENCE | sqlite_publish_makes_prepared_version_current_and_readable; sqlite_prepare_hides_version_from_read_version; sqlite_change_pages_filter_scope_before_applying_limit; f1_forget_memory_hides_current_and_history | Selected local read visibility, prepared hiding and scope filtering are named. Missing all authoritative read paths and replica applied-position/current-Fence serving checks. |
| SC-11 | UNCHANGED | No corresponding test | No test proves D is sole logical Fence issuer, projection carries D cursor/generation, or Storage has no local Fence sequence. |
| SC-12 | UNCHANGED | No corresponding test | Fence/restore tests are not projection tests. Missing stale/corrupt/underscoped D-derived projection fail-closed and D-authority rebuild tests. |
| SC-13 | PARTIAL_EVIDENCE | restore_anti_resurrection_purges_only_fenced_scope_across_all_tables; crash_after_fence_commit_is_retried_safely_on_restore; restore_anti_resurrection_and_preserves_other_scope | D-Fence anti-resurrection/restore retry is named. Missing I PermissionEpoch and independent anti-rollback anchors before restore exposure. |
| SC-14 | UNCHANGED | No corresponding test | No test proves D owns canonical identity/cursor/outbox semantics while Storage only persists supplied values. |
| SC-15 | PARTIAL_EVIDENCE | pending_compile_intent_carries_the_payload_and_envelope_a_compiler_needs; pending_compile_intent_created_at_matches_the_acceptance_time; pending_compile_intents_is_idempotent_and_does_not_consume; startup_backfills_compile_intent_for_preexisting_accepted_events | E compile-intent payload/time/idempotence/backfill is named. Missing full accepted-event/compiler-state/outbox atomicity and explicit non-conflation with D canonical commit. |
| SC-16 | PARTIAL_EVIDENCE | ack_targets_delivery_not_attempt; ledger_tracks_multiple_attempts_per_delivery; pending_delivery_cannot_be_marked_delivered_without_attempt; superseded_delivery_cannot_be_marked_delivered; delivery_intent_targets_snapshot_context_version | G delivery/attempt separation, guarded Delivered transition and ContextVersion targeting are named. Missing proof Storage receipt cannot promote G Delivered/Applied and G Applied has independent durable evidence. |
| SC-17 | UNCHANGED | No corresponding test | Single-file SQLite multi-process CAS is not cross-resource GID participation. Missing stable participants, durable prepare/terminal, deterministic multi-resource replay and one terminal authority. |
| SC-18 | UNCHANGED | No corresponding test | No backup/replica rollback/failover or repeatable RPO/RTO evidence. |

## 4. HIR-01…HIR-18 predicate-by-predicate rejudgment (all 18)

All 18 HIR predicates are assessed, not only the eight previously classified EVIDENCE_REQUIRED. HIR-17 is now PARTIAL_EVIDENCE because a distinct Attempt ledger is directly tested; the cross-domain H↔C/G mapping remains missing.

| ID | Result | Supporting test names | Why not PASS / missing part |
|---|---|---|---|
| HIR-01 | PARTIAL_EVIDENCE | sqlite_does_not_replay_idempotency_key_across_memories; sqlite_does_not_replay_idempotency_receipt_before_scope_check; sqlite_storage_entry_points_reject_empty_and_malformed_scope_sets | Scope isolation/scope-before-replay are named. Missing full H tuple: protocol domain, authority, resolved scope, operation kind, key profile and opaque key. |
| HIR-02 | PARTIAL_EVIDENCE | same_producer_key_and_digest_replay_original_receipt; same_producer_key_with_different_digest_conflicts | Producer-key reuse/digest binding is named in producer/storage path. Missing exact H logical-operation key retention across H retries/reconnections. |
| HIR-03 | PARTIAL_EVIDENCE | ack_targets_delivery_not_attempt; ledger_tracks_multiple_attempts_per_delivery; retry_increments_attempt_number_and_links_previous | Distinct delivery-attempt ledger is named. Missing proof H Attempt is excluded from H dedupe identity while Agent/session remain bound attributes. |
| HIR-04 | UNCHANGED | No corresponding test | No test exercises unambiguous namespace encoding or cross-domain alias/collision isolation. |
| HIR-05 | UNCHANGED | No corresponding test | No test proves durable H reservation and tombstone retention beyond replay horizon. |
| HIR-06 | PARTIAL_EVIDENCE | file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent; sqlite_publish_rejects_stale_parent_without_partial_commit; sqlite_prepare_replay_returns_same_receipt | Selected Storage CAS/idempotency/receipt behavior is named. Missing H-to-Storage integration and full mutation/version/CAS/receipt/sequence join. |
| HIR-07 | UNCHANGED | No corresponding test | No test proves H admission durable unique-reservation LP separately from Storage domain-effect LP. |
| HIR-08 | PARTIAL_EVIDENCE | concurrent_identical_idempotency_requests_replay_one_durable_receipt; independent_connections_serialize_conflicting_idempotency_payloads; separate_processes_serialize_competing_file_backed_cas_writers | Concurrent SQLite idempotency/CAS is named. Missing H namespace contenders, H reservation winner recovery and durable H receipt. |
| HIR-09 | PARTIAL_EVIDENCE | payload_append_receipt_and_ordered_read_survive_reopen; acceptance_persists_across_reopen_and_receipt_replay_is_stable | Durable receipt persistence/replay only. Missing H namespace, digest, logical operation, first/current Attempt, boundary, issuer and proof-reference bindings. |
| HIR-10 | PARTIAL_EVIDENCE | acceptance_persists_across_reopen_and_receipt_replay_is_stable; duplicate_payload_append_returns_original_receipt_without_duplicate_rows; restart_preserves_receipt_and_idempotent_payload_replay | Stable receipt replay is named. Missing append-only H receipt transition/history immutability assertions. |
| HIR-11 | PARTIAL_EVIDENCE | abrupt_process_exit_rolls_back_entire_uncommitted_commit; committed_payload_survives_process_crash_and_wal_recovery; file_db_unwinding_worker_releases_open_transaction_without_partial_state | Selected crash/rollback outcomes are named. Missing H timeout/unavailable resolver/unverifiable evidence staying Unknown/Pending. |
| HIR-12 | PARTIAL_EVIDENCE | concurrent_identical_idempotency_requests_replay_one_durable_receipt; pending_compile_intents_is_idempotent_and_does_not_consume | Generic duplicate replay/idempotent intent is named. Missing H-specific pending duplicate returning original H receipt without second logical execution. |
| HIR-13 | UNCHANGED | No corresponding test | No test proves Failed only after durable authoritative terminal failure; transient/ambiguous errors are not demonstrated. |
| HIR-14 | PARTIAL_EVIDENCE | same_producer_key_and_digest_replay_original_receipt; same_producer_key_with_different_digest_conflicts; sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup | Same-key/same-digest replay and changed-digest conflict are named in producer/Storage paths. Missing exact H namespace and H Duplicate/Conflict terminal receipts. |
| HIR-15 | PARTIAL_EVIDENCE | same_producer_key_and_digest_replay_original_receipt; ledger_tracks_multiple_attempts_per_delivery; retry_increments_attempt_number_and_links_previous | Stable producer key and separately linked delivery attempts are named. Missing integrated H test proving logical key reuse plus fresh H Attempt ID per transport retry. |
| HIR-16 | PARTIAL_EVIDENCE | committed_payload_survives_process_crash_and_wal_recovery; restart_preserves_receipt_and_idempotent_payload_replay; file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent | SQLite commit/reopen/crash persistence is named. Missing H receipt reconciliation before/after Storage commit and no-repeat cross-domain effect. |
| HIR-17 | PARTIAL_EVIDENCE | ack_targets_delivery_not_attempt; ledger_tracks_multiple_attempts_per_delivery; ledger_rejects_forked_attempt_chain; retry_increments_attempt_number_and_links_previous; obsolete_attempt_ack_is_counted_as_stale | Distinct DeliveryAttempt identity, multiple attempts, chain integrity and stale ACK handling are directly named. Missing cross-domain H Attempt ID ↔ C/G DeliveryAttempt mapping and independent G Applied evidence. |
| HIR-18 | PARTIAL_EVIDENCE | missing_or_corrupt_fence_fails_closed; restore_anti_resurrection_purges_only_fenced_scope_across_all_tables; sqlite_publication_state_honours_scope_and_forget_fences | D-Fence fail-closed component is named. Missing I PermissionEpoch freshness, authorization recheck at replay disclosure and joint independent I+D checks. |

## 5. Rejudgment of the 72 AID-2026-095 end-to-end checkpoints

Each of the nine dimensions for each flow is listed. Component/single-store tests do not prove complete cross-Owner composition; all 72 rows remain NOT EVIDENCED / UNCHANGED. SC/HIR PARTIAL_EVIDENCE must not be promoted to AID-095 flow PASS.

| Flow | Checkpoint | Previous | Rejudgment | Reason |
|---|---|---|---|---|
| F1 — Event ingress → durable acceptance → Compiler admission | Issuer | NOT EVIDENCED | UNCHANGED | Only E compile-intent component tests are named; no complete C ingress → E acceptance → H admission request/identity/receipt join. |
| F1 — Event ingress → durable acceptance → Compiler admission | Request / response | NOT EVIDENCED | UNCHANGED | Only E compile-intent component tests are named; no complete C ingress → E acceptance → H admission request/identity/receipt join. |
| F1 — Event ingress → durable acceptance → Compiler admission | Identity / cursor namespace | NOT EVIDENCED | UNCHANGED | Only E compile-intent component tests are named; no complete C ingress → E acceptance → H admission request/identity/receipt join. |
| F1 — Event ingress → durable acceptance → Compiler admission | Idempotency scope | NOT EVIDENCED | UNCHANGED | Only E compile-intent component tests are named; no complete C ingress → E acceptance → H admission request/identity/receipt join. |
| F1 — Event ingress → durable acceptance → Compiler admission | Linearization point | NOT EVIDENCED | UNCHANGED | Only E compile-intent component tests are named; no complete C ingress → E acceptance → H admission request/identity/receipt join. |
| F1 — Event ingress → durable acceptance → Compiler admission | Durable receipt | NOT EVIDENCED | UNCHANGED | Only E compile-intent component tests are named; no complete C ingress → E acceptance → H admission request/identity/receipt join. |
| F1 — Event ingress → durable acceptance → Compiler admission | Failure / Unknown | NOT EVIDENCED | UNCHANGED | Only E compile-intent component tests are named; no complete C ingress → E acceptance → H admission request/identity/receipt join. |
| F1 — Event ingress → durable acceptance → Compiler admission | Replay / recovery | NOT EVIDENCED | UNCHANGED | Only E compile-intent component tests are named; no complete C ingress → E acceptance → H admission request/identity/receipt join. |
| F1 — Event ingress → durable acceptance → Compiler admission | Visibility | NOT EVIDENCED | UNCHANGED | Only E compile-intent component tests are named; no complete C ingress → E acceptance → H admission request/identity/receipt join. |
| F2 — D Canonical Commit → atomic outbox / receipt → F consumer | Issuer | NOT EVIDENCED | UNCHANGED | Local SQLite CAS/read-write tests do not cover D canonical commit through F consumer cursor, outbox, dedupe and acknowledgement. |
| F2 — D Canonical Commit → atomic outbox / receipt → F consumer | Request / response | NOT EVIDENCED | UNCHANGED | Local SQLite CAS/read-write tests do not cover D canonical commit through F consumer cursor, outbox, dedupe and acknowledgement. |
| F2 — D Canonical Commit → atomic outbox / receipt → F consumer | Identity / cursor namespace | NOT EVIDENCED | UNCHANGED | Local SQLite CAS/read-write tests do not cover D canonical commit through F consumer cursor, outbox, dedupe and acknowledgement. |
| F2 — D Canonical Commit → atomic outbox / receipt → F consumer | Idempotency scope | NOT EVIDENCED | UNCHANGED | Local SQLite CAS/read-write tests do not cover D canonical commit through F consumer cursor, outbox, dedupe and acknowledgement. |
| F2 — D Canonical Commit → atomic outbox / receipt → F consumer | Linearization point | NOT EVIDENCED | UNCHANGED | Local SQLite CAS/read-write tests do not cover D canonical commit through F consumer cursor, outbox, dedupe and acknowledgement. |
| F2 — D Canonical Commit → atomic outbox / receipt → F consumer | Durable receipt | NOT EVIDENCED | UNCHANGED | Local SQLite CAS/read-write tests do not cover D canonical commit through F consumer cursor, outbox, dedupe and acknowledgement. |
| F2 — D Canonical Commit → atomic outbox / receipt → F consumer | Failure / Unknown | NOT EVIDENCED | UNCHANGED | Local SQLite CAS/read-write tests do not cover D canonical commit through F consumer cursor, outbox, dedupe and acknowledgement. |
| F2 — D Canonical Commit → atomic outbox / receipt → F consumer | Replay / recovery | NOT EVIDENCED | UNCHANGED | Local SQLite CAS/read-write tests do not cover D canonical commit through F consumer cursor, outbox, dedupe and acknowledgement. |
| F2 — D Canonical Commit → atomic outbox / receipt → F consumer | Visibility | NOT EVIDENCED | UNCHANGED | Local SQLite CAS/read-write tests do not cover D canonical commit through F consumer cursor, outbox, dedupe and acknowledgement. |
| F3 — F Retrieval / Index / Watermark / Scan Coverage | Issuer | NOT EVIDENCED | UNCHANGED | No corresponding F index generation, contiguous watermark, D cursor catch-up or gap-rebuild tests. |
| F3 — F Retrieval / Index / Watermark / Scan Coverage | Request / response | NOT EVIDENCED | UNCHANGED | No corresponding F index generation, contiguous watermark, D cursor catch-up or gap-rebuild tests. |
| F3 — F Retrieval / Index / Watermark / Scan Coverage | Identity / cursor namespace | NOT EVIDENCED | UNCHANGED | No corresponding F index generation, contiguous watermark, D cursor catch-up or gap-rebuild tests. |
| F3 — F Retrieval / Index / Watermark / Scan Coverage | Idempotency scope | NOT EVIDENCED | UNCHANGED | No corresponding F index generation, contiguous watermark, D cursor catch-up or gap-rebuild tests. |
| F3 — F Retrieval / Index / Watermark / Scan Coverage | Linearization point | NOT EVIDENCED | UNCHANGED | No corresponding F index generation, contiguous watermark, D cursor catch-up or gap-rebuild tests. |
| F3 — F Retrieval / Index / Watermark / Scan Coverage | Durable receipt | NOT EVIDENCED | UNCHANGED | No corresponding F index generation, contiguous watermark, D cursor catch-up or gap-rebuild tests. |
| F3 — F Retrieval / Index / Watermark / Scan Coverage | Failure / Unknown | NOT EVIDENCED | UNCHANGED | No corresponding F index generation, contiguous watermark, D cursor catch-up or gap-rebuild tests. |
| F3 — F Retrieval / Index / Watermark / Scan Coverage | Replay / recovery | NOT EVIDENCED | UNCHANGED | No corresponding F index generation, contiguous watermark, D cursor catch-up or gap-rebuild tests. |
| F3 — F Retrieval / Index / Watermark / Scan Coverage | Visibility | NOT EVIDENCED | UNCHANGED | No corresponding F index generation, contiguous watermark, D cursor catch-up or gap-rebuild tests. |
| F4 — Forget Fence → E/F/G/H/Storage visibility and cleanup | Issuer | NOT EVIDENCED | UNCHANGED | SQLite Fence/restore components are named, but no D+I authority and per-target E/F/G/H/Storage acknowledgement chain. |
| F4 — Forget Fence → E/F/G/H/Storage visibility and cleanup | Request / response | NOT EVIDENCED | UNCHANGED | SQLite Fence/restore components are named, but no D+I authority and per-target E/F/G/H/Storage acknowledgement chain. |
| F4 — Forget Fence → E/F/G/H/Storage visibility and cleanup | Identity / cursor namespace | NOT EVIDENCED | UNCHANGED | SQLite Fence/restore components are named, but no D+I authority and per-target E/F/G/H/Storage acknowledgement chain. |
| F4 — Forget Fence → E/F/G/H/Storage visibility and cleanup | Idempotency scope | NOT EVIDENCED | UNCHANGED | SQLite Fence/restore components are named, but no D+I authority and per-target E/F/G/H/Storage acknowledgement chain. |
| F4 — Forget Fence → E/F/G/H/Storage visibility and cleanup | Linearization point | NOT EVIDENCED | UNCHANGED | SQLite Fence/restore components are named, but no D+I authority and per-target E/F/G/H/Storage acknowledgement chain. |
| F4 — Forget Fence → E/F/G/H/Storage visibility and cleanup | Durable receipt | NOT EVIDENCED | UNCHANGED | SQLite Fence/restore components are named, but no D+I authority and per-target E/F/G/H/Storage acknowledgement chain. |
| F4 — Forget Fence → E/F/G/H/Storage visibility and cleanup | Failure / Unknown | NOT EVIDENCED | UNCHANGED | SQLite Fence/restore components are named, but no D+I authority and per-target E/F/G/H/Storage acknowledgement chain. |
| F4 — Forget Fence → E/F/G/H/Storage visibility and cleanup | Replay / recovery | NOT EVIDENCED | UNCHANGED | SQLite Fence/restore components are named, but no D+I authority and per-target E/F/G/H/Storage acknowledgement chain. |
| F4 — Forget Fence → E/F/G/H/Storage visibility and cleanup | Visibility | NOT EVIDENCED | UNCHANGED | SQLite Fence/restore components are named, but no D+I authority and per-target E/F/G/H/Storage acknowledgement chain. |
| F5 — C/H Applied evidence → G Applied decision | Issuer | NOT EVIDENCED | UNCHANGED | memory-context tests cover G delivery/attempt constraints, not C/H cross-domain IDs, G Applied decision or Storage receipt isolation. |
| F5 — C/H Applied evidence → G Applied decision | Request / response | NOT EVIDENCED | UNCHANGED | memory-context tests cover G delivery/attempt constraints, not C/H cross-domain IDs, G Applied decision or Storage receipt isolation. |
| F5 — C/H Applied evidence → G Applied decision | Identity / cursor namespace | NOT EVIDENCED | UNCHANGED | memory-context tests cover G delivery/attempt constraints, not C/H cross-domain IDs, G Applied decision or Storage receipt isolation. |
| F5 — C/H Applied evidence → G Applied decision | Idempotency scope | NOT EVIDENCED | UNCHANGED | memory-context tests cover G delivery/attempt constraints, not C/H cross-domain IDs, G Applied decision or Storage receipt isolation. |
| F5 — C/H Applied evidence → G Applied decision | Linearization point | NOT EVIDENCED | UNCHANGED | memory-context tests cover G delivery/attempt constraints, not C/H cross-domain IDs, G Applied decision or Storage receipt isolation. |
| F5 — C/H Applied evidence → G Applied decision | Durable receipt | NOT EVIDENCED | UNCHANGED | memory-context tests cover G delivery/attempt constraints, not C/H cross-domain IDs, G Applied decision or Storage receipt isolation. |
| F5 — C/H Applied evidence → G Applied decision | Failure / Unknown | NOT EVIDENCED | UNCHANGED | memory-context tests cover G delivery/attempt constraints, not C/H cross-domain IDs, G Applied decision or Storage receipt isolation. |
| F5 — C/H Applied evidence → G Applied decision | Replay / recovery | NOT EVIDENCED | UNCHANGED | memory-context tests cover G delivery/attempt constraints, not C/H cross-domain IDs, G Applied decision or Storage receipt isolation. |
| F5 — C/H Applied evidence → G Applied decision | Visibility | NOT EVIDENCED | UNCHANGED | memory-context tests cover G delivery/attempt constraints, not C/H cross-domain IDs, G Applied decision or Storage receipt isolation. |
| F6 — I Authorization / PermissionEpoch / revocation | Issuer | NOT EVIDENCED | UNCHANGED | No I PermissionEpoch monotonicity, pre-submit authorization recheck, revocation race or replay-disclosure recheck test. |
| F6 — I Authorization / PermissionEpoch / revocation | Request / response | NOT EVIDENCED | UNCHANGED | No I PermissionEpoch monotonicity, pre-submit authorization recheck, revocation race or replay-disclosure recheck test. |
| F6 — I Authorization / PermissionEpoch / revocation | Identity / cursor namespace | NOT EVIDENCED | UNCHANGED | No I PermissionEpoch monotonicity, pre-submit authorization recheck, revocation race or replay-disclosure recheck test. |
| F6 — I Authorization / PermissionEpoch / revocation | Idempotency scope | NOT EVIDENCED | UNCHANGED | No I PermissionEpoch monotonicity, pre-submit authorization recheck, revocation race or replay-disclosure recheck test. |
| F6 — I Authorization / PermissionEpoch / revocation | Linearization point | NOT EVIDENCED | UNCHANGED | No I PermissionEpoch monotonicity, pre-submit authorization recheck, revocation race or replay-disclosure recheck test. |
| F6 — I Authorization / PermissionEpoch / revocation | Durable receipt | NOT EVIDENCED | UNCHANGED | No I PermissionEpoch monotonicity, pre-submit authorization recheck, revocation race or replay-disclosure recheck test. |
| F6 — I Authorization / PermissionEpoch / revocation | Failure / Unknown | NOT EVIDENCED | UNCHANGED | No I PermissionEpoch monotonicity, pre-submit authorization recheck, revocation race or replay-disclosure recheck test. |
| F6 — I Authorization / PermissionEpoch / revocation | Replay / recovery | NOT EVIDENCED | UNCHANGED | No I PermissionEpoch monotonicity, pre-submit authorization recheck, revocation race or replay-disclosure recheck test. |
| F6 — I Authorization / PermissionEpoch / revocation | Visibility | NOT EVIDENCED | UNCHANGED | No I PermissionEpoch monotonicity, pre-submit authorization recheck, revocation race or replay-disclosure recheck test. |
| F7 — Global Forget inventory → per-target evidence → I completion | Issuer | NOT EVIDENCED | UNCHANGED | No full target inventory, external-copy/backup, per-target terminal evidence or I global-completion proof. |
| F7 — Global Forget inventory → per-target evidence → I completion | Request / response | NOT EVIDENCED | UNCHANGED | No full target inventory, external-copy/backup, per-target terminal evidence or I global-completion proof. |
| F7 — Global Forget inventory → per-target evidence → I completion | Identity / cursor namespace | NOT EVIDENCED | UNCHANGED | No full target inventory, external-copy/backup, per-target terminal evidence or I global-completion proof. |
| F7 — Global Forget inventory → per-target evidence → I completion | Idempotency scope | NOT EVIDENCED | UNCHANGED | No full target inventory, external-copy/backup, per-target terminal evidence or I global-completion proof. |
| F7 — Global Forget inventory → per-target evidence → I completion | Linearization point | NOT EVIDENCED | UNCHANGED | No full target inventory, external-copy/backup, per-target terminal evidence or I global-completion proof. |
| F7 — Global Forget inventory → per-target evidence → I completion | Durable receipt | NOT EVIDENCED | UNCHANGED | No full target inventory, external-copy/backup, per-target terminal evidence or I global-completion proof. |
| F7 — Global Forget inventory → per-target evidence → I completion | Failure / Unknown | NOT EVIDENCED | UNCHANGED | No full target inventory, external-copy/backup, per-target terminal evidence or I global-completion proof. |
| F7 — Global Forget inventory → per-target evidence → I completion | Replay / recovery | NOT EVIDENCED | UNCHANGED | No full target inventory, external-copy/backup, per-target terminal evidence or I global-completion proof. |
| F7 — Global Forget inventory → per-target evidence → I completion | Visibility | NOT EVIDENCED | UNCHANGED | No full target inventory, external-copy/backup, per-target terminal evidence or I global-completion proof. |
| F8 — Storage atomicity / durability / crash / restore | Issuer | NOT EVIDENCED | UNCHANGED | SQLite tests cover selected single-store transaction/WAL/crash behavior, not the full end-to-end predicate or production recovery. |
| F8 — Storage atomicity / durability / crash / restore | Request / response | NOT EVIDENCED | UNCHANGED | SQLite tests cover selected single-store transaction/WAL/crash behavior, not the full end-to-end predicate or production recovery. |
| F8 — Storage atomicity / durability / crash / restore | Identity / cursor namespace | NOT EVIDENCED | UNCHANGED | SQLite tests cover selected single-store transaction/WAL/crash behavior, not the full end-to-end predicate or production recovery. |
| F8 — Storage atomicity / durability / crash / restore | Idempotency scope | NOT EVIDENCED | UNCHANGED | SQLite tests cover selected single-store transaction/WAL/crash behavior, not the full end-to-end predicate or production recovery. |
| F8 — Storage atomicity / durability / crash / restore | Linearization point | NOT EVIDENCED | UNCHANGED | SQLite tests cover selected single-store transaction/WAL/crash behavior, not the full end-to-end predicate or production recovery. |
| F8 — Storage atomicity / durability / crash / restore | Durable receipt | NOT EVIDENCED | UNCHANGED | SQLite tests cover selected single-store transaction/WAL/crash behavior, not the full end-to-end predicate or production recovery. |
| F8 — Storage atomicity / durability / crash / restore | Failure / Unknown | NOT EVIDENCED | UNCHANGED | SQLite tests cover selected single-store transaction/WAL/crash behavior, not the full end-to-end predicate or production recovery. |
| F8 — Storage atomicity / durability / crash / restore | Replay / recovery | NOT EVIDENCED | UNCHANGED | SQLite tests cover selected single-store transaction/WAL/crash behavior, not the full end-to-end predicate or production recovery. |
| F8 — Storage atomicity / durability / crash / restore | Visibility | NOT EVIDENCED | UNCHANGED | SQLite tests cover selected single-store transaction/WAL/crash behavior, not the full end-to-end predicate or production recovery. |

## 6. Dedicated rejudgment of the 16 EVIDENCE_REQUIRED rows

| ID | Original classification | New result | Remaining gap |
|---|---|---|---|
| SC-04 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | Device flush, commit-marker and log-before-data fault injection |
| SC-05 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | Checkpoint atomicity and contiguous valid-prefix replay/gap/truncation |
| SC-06 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | Torn/partial records, corruption quarantine, crash-safe restore activation |
| SC-10 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | Every authoritative read path, replica applied-position and Fence serving gate |
| SC-12 | EVIDENCE_REQUIRED | UNCHANGED | D-derived projection stale/corrupt/underscoped fail-closed and rebuild tests; Fence tests are not projection tests |
| SC-13 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | I PermissionEpoch plus independent anti-rollback anchors before restore exposure |
| SC-17 | EVIDENCE_REQUIRED | UNCHANGED | Cross-resource GID/COC participants, durable prepare/terminal records, one decision authority |
| SC-18 | EVIDENCE_REQUIRED | UNCHANGED | Repeatable RPO/RTO evidence for backup/replica rollback/failover |
| HIR-05 | EVIDENCE_REQUIRED | UNCHANGED | Durable H reservation and tombstone beyond replay horizon |
| HIR-06 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | Exact H/Storage integration and complete mutation/CAS/receipt/sequence join |
| HIR-08 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | H namespace contenders, reservation-winner recovery, durable H receipt |
| HIR-12 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | H pending duplicate returns original H receipt without duplicate execution |
| HIR-14 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | Exact Duplicate/Conflict terminal receipts in H namespace |
| HIR-16 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | H receipt reconciliation across crashes before/after Storage commit without repeating effect |
| HIR-17 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | Cross-domain H Attempt ID ↔ C/G DeliveryAttempt mapping and independent G Applied evidence |
| HIR-18 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | Independent fail-closed linkage of I PermissionEpoch/authorization recheck and D Fence |

Count by 16 data rows: 12 PARTIAL_EVIDENCE / 4 UNCHANGED / 0 PASS. Original classifications remain EVIDENCE_REQUIRED. PARTIAL_EVIDENCE is not PASS and does not remove EVIDENCE_REQUIRED.

## 7. Corrections and explicit non-coverage

- SC-01: pending_compile_intent tests belong to E's SC-15, not SC-01's complete atomic write-set predicate.
- SC-12: Fence presence/restore/anti-resurrection tests are not D-derived projection stale/corrupt/underscoped tests. Fence is not relabelled as projection.
- SC-07: no test name demonstrates an ABORTED receipt path. The checked fact is that StorageError has no ABORTED variant and PublicationState has only two states; do not claim COMMITTED/ABORTED/UNKNOWN three-state coverage.
- HIR-17: Attempt ledger, DeliveryAttempt separation, multiple attempts, chain integrity and stale ACK handling are named; cross-domain H Attempt ↔ C/G DeliveryAttempt mapping and G Applied evidence are still missing.
- Still uncovered: SC-18 RPO/RTO backup/failover; SC-17 cross-resource GID participants; HIR-18 I PermissionEpoch/authorization recheck; D/I anti-rollback-anchor linkage; SC-12 projection fail-closed.
- All HIR-01…HIR-18 were rejudged, not only eight EVIDENCE_REQUIRED rows.

## 8. Three execution records and reproduction boundary

Environment: WSL2 Ubuntu 24.04 + rustup stable Rust/Cargo 1.100.0. These are operator-supplied local execution records; this agent did not rerun them in this session. They are not CI. Reproduction requires a complete Git clone, checkout of the exact commit, and the local toolchain needed to build bundled SQLite.

| Group | Exact command | HEAD | Exit | Test binaries | Passed / Failed | stdout bytes | stdout SHA-256 |
|---|---|---|---:|---:|---:|---:|---|
| SQLite backend | cargo test -p memory-storage-sqlite -p memory-event-store-sqlite --no-fail-fast | a123ea4e414c9f74fa0c576fbd718049a7d9f917 | 0 | 8 | 99 / 0 | 9465 | a15e3862af4d6cd97a4cd8caf6f133f57e3c3636ba284bdfd5afaa9237ba2952 |
| Pure Rust layer | cargo test -p memory-domain -p memory-storage -p memory-event-store -p bmcp-protocol -p agent-integration --no-fail-fast | 44dc21a4970192118ba434801b8ca05702ac582c | 0 | 15 | 276 / 0 | 47066 | C18EF5FC121EEB9B486000180F52BAE8385385722A369ADDAB873FCF8716D7B9 |
| memory-context | cargo test -p memory-context --no-fail-fast | a123ea4e414c9f74fa0c576fbd718049a7d9f917 | 0 | 11 | 177 / 0 | NOT_RECORDED | 43b2b9b6da6521db9ef53127f1e2a3aff5226c9ef3a50a78f3a65dad6a620eee |

Total: 552 passed / 0 failed is the arithmetic sum of three separate runs, not one unified run and not a deduplicated unique-test count. Five SQLite test names were not supplied; 154 memory-context names were not supplied; the 276 pure-Rust tests have no individual names supplied. memory-context stdout byte length was not supplied and is recorded as NOT_RECORDED.

Boundary: local Linux/WSL2 + bundled SQLite, not GitHub CI; not a distributed backend; not multi-replica linearizability; not a production topology. No RPO/RTO, cross-resource GID, I authorization recheck or D/I anti-rollback linkage is proved. PARTIAL_EVIDENCE means only that a local behavior is supported by a named test, not conformance PASS.

## 9. Gate A / Gate B and closure conditions

Gate A: PARTIAL / OPEN (unchanged). All 72 AID-095 flow cells remain NOT EVIDENCED; 0 PASS; all eight flows remain BLOCKED_WITH_REASON. SC/HIR layer: 27 PARTIAL_EVIDENCE, 9 UNCHANGED, 0 PASS. The 16 EVIDENCE_REQUIRED rows: 12 PARTIAL, 4 UNCHANGED, 0 PASS.

Nine-item checklist carried forward from AID-2026-107:
1. Branch freshness: satisfied only after final PR Head is checked against latest main.
2. Ten cross-Owner proxy dispositions are recorded, not natural-person Owner signatures.
3. Exact-head CI: OPEN until all 16 required contexts succeed on this PR's exact Head.
4. Complete A–I + Storage/Consistency eight-flow × nine-dimension review and Owner acceptance: OPEN.
5. IMPL2 scope adjudicated; five NORMATIVE_ROOTs still need separate restoration PRs; F/I README roots need Owner identification or explicit replacement. HISTORICAL_PHASE_RECORD and UNDECIDED stay out of main without Owner ruling.
6. Storage/Consistency: OPEN; SC-04/05/06/10/13 PARTIAL, SC-12/17/18 UNCHANGED; complete evidence and exact-version Owner dispositions still missing.
7. H idempotency/replay: OPEN; HIR-06/08/12/14/16/17/18 PARTIAL, HIR-05 UNCHANGED; H-specific and cross-domain evidence plus Owner acceptance still missing.
8. Full Canonical/EN/ZH-CN semantic and source-revision parity: pending independent exact-version verification, OPEN.
9. DEC-13: carry forward AID-2026-096; do not infer #1189 or Owner acceptance complete.

Gate B: PARTIAL / OPEN — NOT VERIFIED (unchanged). Single-machine SQLite tests do not establish implementation conformance, distributed/production topology, backup recovery or operational evidence.

## 10. Explicitly out of scope

No runtime, validator, schema, API, DDL, workflow or deployment changes; no IMPL2 restoration; do not promote DOCUMENTED_ONLY or PARTIAL_EVIDENCE to PASS; do not close #1211 or #1212.
