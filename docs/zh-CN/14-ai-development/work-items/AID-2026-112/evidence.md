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
    canonical_status: Non-Canonical
    canonical_scope: "AID-2026-112 supplemental exact-head local implementation-test evidence and conservative SC/HIR rejudgment"
    canonical_scope_id: "ai-development/aid-2026-112-sc-hir-test-evidence-rejudgment"
    canonical_scope_keywords:
      - storage-consistency
      - h-idempotency
      - sqlite
      - memory-context
      - test-evidence
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-112/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-112/evidence.md"
    zh-CN: null
---
# AID-2026-112 — 552 项本地测试证据下的 SC/HIR 逐谓词重判

- Work item: AID-2026-112；id_status: PROVISIONAL。
- Attribution: user-authorized operator (delegated by account owner)；date: 2026-11-26。
- alloc_at_push verified immediately before push: main=57767952f1248e2de616c5dc24ac762ecb3a5a7f; INDEX maximum=AID-2026-111; AID-2026-112 directory and INDEX row absent; id_status=PROVISIONAL.
- 本记录补充已合并的 AID-2026-107，不覆盖其历史结论。
- 36 条 SC/HIR 谓词：27 PARTIAL_EVIDENCE / 9 UNCHANGED / 0 PASS。
- AID-095 的 72 个端到端检查点：72 UNCHANGED / 0 PASS。
- 16 条 EVIDENCE_REQUIRED：12 PARTIAL_EVIDENCE / 4 UNCHANGED / 0 PASS。
- Gate A PARTIAL / OPEN；Gate B PARTIAL / OPEN — NOT VERIFIED。

## 1. 证据口径

只按测试名与谓词字面语义映射；映射不等于完整谓词通过。PASS 要求测试完整覆盖整个谓词，本轮没有任何谓词达到该标准。276 项 pure-Rust 组只有聚合结果，没有逐项名称，故不伪造逐项映射。SQLite 99 项仅提供 94 个名称，另 5 个名称 NOT_RECORDED；memory-context 177 项仅提供 23 个相关名称，另 154 个名称 NOT_RECORDED。

## 2. 117 个具名测试逐项映射

| # | Group | Test name | Predicate mapping | Mapping note |
|---:|---|---|---|---|
| 1 | SQLite | committed_payload_survives_process_crash_and_wal_recovery | SC-04, SC-05, HIR-11, HIR-16 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 2 | SQLite | concurrent_appends_preserve_unique_order_and_payload_custody | SC-09, HIR-08 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 3 | SQLite | concurrent_forget_waits_for_restore_snapshot_lock | SC-09, HIR-08 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 4 | SQLite | crash_after_fence_commit_is_retried_without_resurrection | SC-13, HIR-18 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 5 | SQLite | failed_payload_insert_rolls_back_event_payload_and_outbox_rows | SC-01, SC-02, SC-07, SC-08 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 6 | SQLite | fence_restore_purges_one_scope_from_a_store_built_database | SC-13, HIR-18 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 7 | SQLite | forget_fence::tests::concurrent_forget_serializes_behind_restore_fence_lock | SC-13, HIR-18 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 8 | SQLite | forget_fence::tests::crash_after_fence_commit_is_retried_safely_on_restore | SC-13, HIR-18 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 9 | SQLite | forget_fence::tests::malformed_scope_refuses_activation_without_partial_change | SC-13, HIR-18 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 10 | SQLite | forget_fence::tests::missing_or_corrupt_fence_fails_closed | SC-13, HIR-18 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 11 | SQLite | forget_fence::tests::restore_anti_resurrection_purges_only_fenced_scope_across_all_tables | SC-13, HIR-18 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 12 | SQLite | live_wal_copy_fails_closed_until_checkpointed | SC-04, SC-05, HIR-16 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 13 | SQLite | malformed_scope_refuses_activation_without_partial_change | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 14 | SQLite | missing_or_corrupt_fence_fails_closed | SC-13, HIR-18 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 15 | SQLite | ordered_read_rejects_payload_and_verified_digest_tampering | SC-01, SC-02, SC-07, SC-08 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 16 | SQLite | payload::tests::duplicate_payload_append_returns_original_receipt_without_duplicate_rows | SC-07, SC-08, HIR-10, HIR-14 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 17 | SQLite | payload::tests::payload_append_receipt_and_ordered_read_survive_reopen | SC-07, SC-08, HIR-09, HIR-10, HIR-14 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 18 | SQLite | payload::tests::payload_digest_mismatch_is_rejected_before_append | SC-01, SC-02, SC-07, SC-08 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 19 | SQLite | payload::tests::read_after_fails_closed_on_empty_persisted_scope_list | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 20 | SQLite | payload::tests::read_after_fails_closed_on_invalid_persisted_scope_ref | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 21 | SQLite | payload::tests::read_after_paginates_interleaved_scope_rows_by_visible_limit | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 22 | SQLite | payload::tests::read_after_skips_non_intersecting_scopes_and_limits_visible_rows | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 23 | SQLite | payload_persistence_boundary_sizes_survive_reopen | SC-01, SC-02, SC-07, SC-08 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 24 | SQLite | restart_preserves_receipt_and_idempotent_payload_replay | SC-03, SC-07, SC-08, HIR-10, HIR-14, HIR-16 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 25 | SQLite | restore_anti_resurrection_and_preserves_other_scope | SC-13, HIR-18 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 26 | SQLite | tests::abrupt_exit_worker | 无对应测试 | 测试名不对应任一 SC/HIR 谓词。 |
| 27 | SQLite | tests::abrupt_process_exit_rolls_back_entire_uncommitted_commit | 无对应测试 | 测试名不对应任一 SC/HIR 谓词。 |
| 28 | SQLite | tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable | SC-03, SC-07, SC-08, HIR-09, HIR-10, HIR-14, HIR-16 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 29 | SQLite | tests::empty_scope_and_missing_payload_identity_are_rejected | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 30 | SQLite | tests::f1_forget_memory_hides_current_and_history | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 31 | SQLite | tests::f10_forget_survives_reopen | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 32 | SQLite | tests::f2_forget_memory_excludes_from_change_pages | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 33 | SQLite | tests::f3_forget_memory_rejects_new_commit | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 34 | SQLite | tests::f4_forget_memory_rejects_prepare_and_publish | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 35 | SQLite | tests::f5_forget_memory_blocks_idempotency_replay | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 36 | SQLite | tests::f6_forget_is_idempotent | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 37 | SQLite | tests::f7_forget_version_only_hides_that_version | 无对应测试 | 测试名不对应任一 SC/HIR 谓词。 |
| 38 | SQLite | tests::f8_forget_version_blocks_child_commit | 无对应测试 | 测试名不对应任一 SC/HIR 谓词。 |
| 39 | SQLite | tests::f9_forget_memory_sets_lifecycle_state | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 40 | SQLite | tests::file_backed_connection_applies_required_sqlite_pragmas | SC-04 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 41 | SQLite | tests::file_db_busy_timeout_bounds_wait_for_long_immediate_transaction | SC-09, HIR-08 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 42 | SQLite | tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent | SC-01, SC-02, SC-03, SC-06, HIR-11, HIR-16 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 43 | SQLite | tests::file_db_nested_savepoint_rollback_preserves_outer_work | SC-02 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 44 | SQLite | tests::file_db_unwinding_worker_releases_open_transaction_without_partial_state | SC-02, SC-03, SC-06, HIR-11, HIR-16 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 45 | SQLite | tests::independent_connections_serialize_conflicting_idempotency_payloads | SC-08, HIR-01, HIR-08, HIR-14 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 46 | SQLite | tests::multi_process_cas_worker | 无对应测试 | 测试名不对应任一 SC/HIR 谓词。 |
| 47 | SQLite | tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt | SC-07, SC-08, HIR-08, HIR-12, HIR-14 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 48 | SQLite | tests::pending_compile_intent_carries_the_payload_and_envelope_a_compiler_needs | SC-15 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 49 | SQLite | tests::pending_compile_intent_created_at_matches_the_acceptance_time | SC-15 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 50 | SQLite | tests::pending_compile_intent_fails_closed_when_stored_payload_is_tampered_with | SC-15 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 51 | SQLite | tests::pending_compile_intent_is_invisible_when_no_payload_was_stored | SC-15 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 52 | SQLite | tests::pending_compile_intents_fails_closed_when_stored_bytes_are_tampered | SC-15 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 53 | SQLite | tests::pending_compile_intents_is_empty_on_a_fresh_store | SC-15 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 54 | SQLite | tests::pending_compile_intents_is_idempotent_and_does_not_consume | SC-15 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 55 | SQLite | tests::pending_compile_intents_returns_accepted_events_in_insertion_order | SC-15 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 56 | SQLite | tests::same_producer_key_and_digest_replay_original_receipt | SC-08, SC-15, HIR-02, HIR-14 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 57 | SQLite | tests::same_producer_key_with_different_digest_conflicts | SC-08, SC-15, HIR-02, HIR-14 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 58 | SQLite | tests::separate_processes_serialize_competing_file_backed_cas_writers | SC-09, HIR-08 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 59 | SQLite | tests::sqlite_change_listing_surfaces_corrupt_scope_metadata_instead_of_silently_skipping_it | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 60 | SQLite | tests::sqlite_change_pages_filter_scope_before_applying_limit | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 61 | SQLite | tests::sqlite_change_pages_with_limit_two_preserve_order_without_skips_or_duplicates | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 62 | SQLite | tests::sqlite_denies_fresh_cross_scope_write_without_persisting_any_commit_state | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 63 | SQLite | tests::sqlite_does_not_replay_idempotency_key_across_memories | SC-08, HIR-01, HIR-08, HIR-14 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 64 | SQLite | tests::sqlite_does_not_replay_idempotency_receipt_before_scope_check | SC-07, SC-08, HIR-10, HIR-14 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 65 | SQLite | tests::sqlite_filters_nested_claims_by_the_callers_scope | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 66 | SQLite | tests::sqlite_hides_entire_multiscope_claim_from_partial_scope_reader | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 67 | SQLite | tests::sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup | SC-07, SC-08, HIR-10, HIR-14 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 68 | SQLite | tests::sqlite_multiple_preparations_reserve_unique_negative_sequences | SC-01, SC-03 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 69 | SQLite | tests::sqlite_prepare_does_not_add_change_log_entries | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 70 | SQLite | tests::sqlite_prepare_hides_version_from_read_version | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 71 | SQLite | tests::sqlite_prepare_keeps_current_version_unchanged | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 72 | SQLite | tests::sqlite_prepare_rejects_idempotency_digest_conflict | SC-08, HIR-01, HIR-08, HIR-14 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 73 | SQLite | tests::sqlite_prepare_replay_returns_same_receipt | SC-07, SC-08, HIR-06, HIR-10, HIR-14 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 74 | SQLite | tests::sqlite_publication_state_honours_scope_and_forget_fences | SC-13, HIR-18 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 75 | SQLite | tests::sqlite_publication_state_reports_prepared_hidden_then_published | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 76 | SQLite | tests::sqlite_publication_state_returns_none_for_unknown_or_legacy_publication | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 77 | SQLite | tests::sqlite_publish_allocates_sequence_only_at_publish_time | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 78 | SQLite | tests::sqlite_publish_makes_prepared_version_current_and_readable | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 79 | SQLite | tests::sqlite_publish_rejects_duplicate_publication_and_suppressed_state | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 80 | SQLite | tests::sqlite_publish_rejects_stale_parent_without_partial_commit | SC-10, HIR-06 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 81 | SQLite | tests::sqlite_publish_replay_returns_original_receipt | SC-07, SC-08, HIR-10, HIR-14 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 82 | SQLite | tests::sqlite_read_version_keeps_legacy_versions_visible | SC-10 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 83 | SQLite | tests::sqlite_rejects_claim_scope_outside_callers_scope_even_when_parent_contains_it | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 84 | SQLite | tests::sqlite_rejects_claims_outside_the_parent_memory_scope | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 85 | SQLite | tests::sqlite_rejects_create_outside_requested_scope | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 86 | SQLite | tests::sqlite_rejects_empty_idempotency_key_or_request_digest | SC-08, HIR-01, HIR-08, HIR-14 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 87 | SQLite | tests::sqlite_rejects_invalid_memory_and_orphan_initial_version_pointer | 无对应测试 | 测试名不对应任一 SC/HIR 谓词。 |
| 88 | SQLite | tests::sqlite_rejects_invalid_version_fields_before_writing_any_commit_state | 无对应测试 | 测试名不对应任一 SC/HIR 谓词。 |
| 89 | SQLite | tests::sqlite_rejects_malformed_nested_claims_before_commit | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 90 | SQLite | tests::sqlite_rejects_mixed_parent_and_foreign_claim_scopes_before_commit | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 91 | SQLite | tests::sqlite_rejects_stale_expected_version | SC-02, SC-03 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 92 | SQLite | tests::sqlite_storage_entry_points_reject_empty_and_malformed_scope_sets | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 93 | SQLite | tests::startup_backfills_compile_intent_for_preexisting_accepted_events | SC-15 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 94 | SQLite | tests::status_and_replay_enforce_scope | SC-02, SC-10, HIR-01 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 95 | memory-context | ack_targets_delivery_not_attempt | SC-16, HIR-03, HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 96 | memory-context | ledger_tracks_multiple_attempts_per_delivery | SC-16, HIR-03, HIR-15, HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 97 | memory-context | ledger_rejects_duplicate_attempt_id | HIR-15, HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 98 | memory-context | ledger_rejects_forked_attempt_chain | HIR-15, HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 99 | memory-context | retry_increments_attempt_number_and_links_previous | SC-16, HIR-03, HIR-15, HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 100 | memory-context | zero_max_attempts_is_rejected | 无对应测试 | 测试名不对应任一 SC/HIR 谓词。 |
| 101 | memory-context | pending_delivery_cannot_be_marked_delivered_without_attempt | SC-16, HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 102 | memory-context | superseded_delivery_cannot_be_marked_delivered | SC-16, HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 103 | memory-context | abandoned_delivery_cannot_transition_back_to_delivered | SC-16, HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 104 | memory-context | abandoned_delivery_rejects_ack_for_current_attempt | SC-16, HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 105 | memory-context | abandoned_delivery_rejects_ack_for_obsolete_attempt | SC-16, HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 106 | memory-context | acknowledged_delivery_cannot_be_superseded | SC-16, HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 107 | memory-context | acknowledged_delivery_cannot_record_another_attempt | HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 108 | memory-context | obsolete_attempt_ack_is_counted_as_stale | HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 109 | memory-context | ack_for_current_attempt_is_current | HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 110 | memory-context | ack_for_unknown_delivery_is_unknown | HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 111 | memory-context | normal_delivery_acknowledgement_path | SC-16, HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 112 | memory-context | retry_exhaustion_abandons_delivery | SC-16, HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 113 | memory-context | delivery_states_are_tallied_on_separate_axes_and_never_folded_together | SC-16, HIR-17 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 114 | memory-context | the_delivery_report_carries_counts_only_and_no_delivery_identifiers | 无对应测试 | 测试名不对应任一 SC/HIR 谓词。 |
| 115 | memory-context | delivery_intent_snapshot_json_round_trips_to_equivalent_snapshot | 无对应测试 | 测试名不对应任一 SC/HIR 谓词。 |
| 116 | memory-context | delivery_intent_targets_snapshot_context_version | SC-16 | 名称只支持相关局部行为，不足以满足完整谓词。 |
| 117 | memory-context | delivery_intent_visibility_is_always_private_pending_gate | SC-16 | 名称只支持相关局部行为，不足以满足完整谓词。 |

## 3. SC-01…SC-18 逐谓词重判

| ID | Result | 对应测试名 | 为什么仍非 PASS / 缺失部分 |
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

## 4. HIR-01…HIR-18 逐谓词重判（全 18 条）

本次逐项评估全部 18 条，不仅是原先 8 条 EVIDENCE_REQUIRED。HIR-17 因独立 Attempt ledger 有直接测试而提升为 PARTIAL_EVIDENCE；H↔C/G 的跨域映射仍缺。

| ID | Result | 对应测试名 | 为什么仍非 PASS / 缺失部分 |
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
| HIR-12 | PARTIAL_EVIDENCE | concurrent_identical_idempotency_requests_replay_one_durable_receipt | Generic duplicate replay/idempotent intent is named. Missing H-specific pending duplicate returning original H receipt without second logical execution. |
| HIR-13 | UNCHANGED | No corresponding test | No test proves Failed only after durable authoritative terminal failure; transient/ambiguous errors are not demonstrated. |
| HIR-14 | PARTIAL_EVIDENCE | same_producer_key_and_digest_replay_original_receipt; same_producer_key_with_different_digest_conflicts; sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup | Same-key/same-digest replay and changed-digest conflict are named in producer/Storage paths. Missing exact H namespace and H Duplicate/Conflict terminal receipts. |
| HIR-15 | PARTIAL_EVIDENCE | same_producer_key_and_digest_replay_original_receipt; ledger_tracks_multiple_attempts_per_delivery; retry_increments_attempt_number_and_links_previous | Stable producer key and separately linked delivery attempts are named. Missing integrated H test proving logical key reuse plus fresh H Attempt ID per transport retry. |
| HIR-16 | PARTIAL_EVIDENCE | committed_payload_survives_process_crash_and_wal_recovery; restart_preserves_receipt_and_idempotent_payload_replay; file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent | SQLite commit/reopen/crash persistence is named. Missing H receipt reconciliation before/after Storage commit and no-repeat cross-domain effect. |
| HIR-17 | PARTIAL_EVIDENCE | ack_targets_delivery_not_attempt; ledger_tracks_multiple_attempts_per_delivery; ledger_rejects_forked_attempt_chain; retry_increments_attempt_number_and_links_previous; obsolete_attempt_ack_is_counted_as_stale | Distinct DeliveryAttempt identity, multiple attempts, chain integrity and stale ACK handling are directly named. Missing cross-domain H Attempt ID ↔ C/G DeliveryAttempt mapping and independent G Applied evidence. |
| HIR-18 | PARTIAL_EVIDENCE | missing_or_corrupt_fence_fails_closed; restore_anti_resurrection_purges_only_fenced_scope_across_all_tables; sqlite_publication_state_honours_scope_and_forget_fences | D-Fence fail-closed component is named. Missing I PermissionEpoch freshness, authorization recheck at replay disclosure and joint independent I+D checks. |

## 5. AID-2026-095 的 72 个端到端检查点

九个维度逐行列出。组件/单库测试没有证明跨 Owner 的完整端到端联结，因此所有 72 行保持 NOT EVIDENCED / UNCHANGED。SC/HIR 的 PARTIAL_EVIDENCE 不得晋升为 AID-095 流程 PASS。

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

## 6. 16 条 EVIDENCE_REQUIRED 专门复判

| ID | Original classification | New result | Remaining gap |
|---|---|---|---|
| SC-04 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | 设备级 flush、commit-marker、log-before-data 故障注入 |
| SC-05 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | checkpoint 原子性、连续有效日志前缀重放、gap/truncation |
| SC-06 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | torn/partial record、数据库损坏隔离、restore 激活崩溃安全 |
| SC-10 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | 所有权威读路径、replica applied-position 与 Fence serving gate |
| SC-12 | EVIDENCE_REQUIRED | UNCHANGED | D-derived projection stale/corrupt/underscoped fail-closed 与重建测试；Fence 测试不能代替 projection |
| SC-13 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | restore-before-exposure 的 I PermissionEpoch + 独立 anti-rollback anchors |
| SC-17 | EVIDENCE_REQUIRED | UNCHANGED | 跨资源 GID/COC participants、durable prepare/terminal、单一决策权威 |
| SC-18 | EVIDENCE_REQUIRED | UNCHANGED | backup/replica rollback/failover 的可重复 RPO/RTO |
| HIR-05 | EVIDENCE_REQUIRED | UNCHANGED | H durable reservation 与超过 replay horizon 的 tombstone |
| HIR-06 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | H 与 Storage 精确版本集成及 mutation/CAS/receipt/sequence 完整联结 |
| HIR-08 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | H namespace contenders、reservation-winner recovery、H durable receipt |
| HIR-12 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | H pending duplicate 返回原 H receipt 且不重复执行 |
| HIR-14 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | H namespace 下 Duplicate/Conflict 的精确终态回执 |
| HIR-16 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | Storage commit 前后 crash 的 H receipt reconciliation，且不重复副作用 |
| HIR-17 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | H Attempt ID ↔ C/G DeliveryAttempt ID 跨域映射及 G Applied 独立证据 |
| HIR-18 | EVIDENCE_REQUIRED | PARTIAL_EVIDENCE | I PermissionEpoch/授权重查与 D Fence 独立 fail-closed 联动 |

**按 16 条数据行统计：12 PARTIAL_EVIDENCE / 4 UNCHANGED / 0 PASS。** 原分类继续保持 EVIDENCE_REQUIRED；PARTIAL_EVIDENCE 不等于 PASS，不移除 EVIDENCE_REQUIRED。

## 7. 关键纠错与仍无覆盖项

- SC-01：pending_compile_intent 测试属于 E 的 SC-15，不是 SC-01 完整原子写集证据。
- SC-12：Fence 存在/恢复/防复活不是 D-derived projection stale/corrupt/underscoped 测试；不把 Fence 当 projection。
- SC-07：没有测试名证明 ABORTED receipt 路径。已核事实为 StorageError 没有 ABORTED 变体，PublicationState 只有两态；不得声称 COMMITTED/ABORTED/UNKNOWN 三态已测。
- HIR-17：Attempt ledger、DeliveryAttempt 区分、多次 attempt、链完整性和 stale ACK 有测试；H Attempt ↔ C/G DeliveryAttempt 跨域映射及 G Applied 证据仍缺。
- 仍无覆盖：SC-18 RPO/RTO backup/failover；SC-17 cross-resource GID participants；HIR-18 I PermissionEpoch/authorization recheck；D/I anti-rollback anchor linkage；SC-12 projection fail-closed。
- HIR-01…HIR-18 全部复判，不是只评 8 条 EVIDENCE_REQUIRED。

## 8. 三组执行记录与复现边界

环境：WSL2 Ubuntu 24.04 + rustup stable Rust/Cargo 1.100.0。以下是操作者提供的本地执行记录，本代理未在本会话重跑；不是 CI。可复现前提：完整 Git 克隆、checkout 对应精确 commit、安装 bundled SQLite 构建所需工具链。

| Group | Exact command | HEAD | Exit | Test binaries | Passed / Failed | stdout bytes | stdout SHA-256 |
|---|---|---|---:|---:|---:|---:|---|
| SQLite backend | cargo test -p memory-storage-sqlite -p memory-event-store-sqlite --no-fail-fast | a123ea4e414c9f74fa0c576fbd718049a7d9f917 | 0 | 8 | 99 / 0 | 9465 | a15e3862af4d6cd97a4cd8caf6f133f57e3c3636ba284bdfd5afaa9237ba2952 |
| Pure Rust layer | cargo test -p memory-domain -p memory-storage -p memory-event-store -p bmcp-protocol -p agent-integration --no-fail-fast | 44dc21a4970192118ba434801b8ca05702ac582c | 0 | 15 | 276 / 0 | 47066 | C18EF5FC121EEB9B486000180F52BAE8385385722A369ADDAB873FCF8716D7B9 |
| memory-context | cargo test -p memory-context --no-fail-fast | a123ea4e414c9f74fa0c576fbd718049a7d9f917 | 0 | 11 | 177 / 0 | NOT_RECORDED | 43b2b9b6da6521db9ef53127f1e2a3aff5226c9ef3a50a78f3a65dad6a620eee |

**合计 552 passed / 0 failed**，是三次独立执行的算术合计，不是一次统一运行，也不是去重后的唯一测试数。SQLite 99 项中 5 个测试名未提供；memory-context 177 项中 154 个测试名未提供；pure-Rust 276 项未提供逐项名称。memory-context stdout 字节数未提供，明确标为 NOT_RECORDED。

边界：Linux/WSL2 + bundled SQLite 本地执行，不是 GitHub CI；不是分布式后端；不是多副本线性化；不是生产拓扑；不证明 RPO/RTO、跨资源 GID、I 权限重查或 D/I anti-rollback 锚点联动。PARTIAL_EVIDENCE 只代表具名测试支持局部行为，不是 conformance PASS。

## 9. Gate A / Gate B 与关闭条件

**Gate A：PARTIAL / OPEN（不变）**。72/72 AID-095 flow cells 仍 NOT EVIDENCED；0 PASS；8/8 flows 仍 BLOCKED_WITH_REASON。SC/HIR 层为 27 PARTIAL_EVIDENCE、9 UNCHANGED、0 PASS；16 条 EVIDENCE_REQUIRED 为 12 PARTIAL、4 UNCHANGED、0 PASS。

九项清单沿用 AID-2026-107：
1. Branch freshness：最终 PR Head 对最新 main 的 behind=0 才可满足。
2. 十个跨 Owner 代理处置已记录，但不代表自然人 Owner 签署。
3. Exact-head CI：本 PR 的 16 个必需 context 全部成功前保持 OPEN。
4. A–I + Storage/Consistency 八流程 × 九维度完整审查与 Owner acceptance：OPEN。
5. IMPL2 范围已裁决；5 个 NORMATIVE_ROOT 仍需独立 PR 恢复；F/I README 根需 Owner 指认或明确替代；HISTORICAL_PHASE_RECORD 与 UNDECIDED 未经 Owner 裁决不得进 main。
6. Storage/Consistency：OPEN；SC-04/05/06/10/13 为 PARTIAL，SC-12/17/18 为 UNCHANGED；完整证据与精确版本 Owner disposition 仍缺。
7. H idempotency/replay：OPEN；HIR-06/08/12/14/16/17/18 为 PARTIAL，HIR-05 为 UNCHANGED；H-specific 与跨域证据及 Owner acceptance 仍缺。
8. Canonical/EN/ZH-CN 全包语义和 source revision parity：待独立精确版本核验，OPEN。
9. DEC-13：沿用 AID-2026-096 记录；不推导 #1189 或 Owner acceptance 已完成。

**Gate B：PARTIAL / OPEN — NOT VERIFIED（不变）**。单机 SQLite 测试不建立实现符合性、分布式/生产拓扑、备份恢复或运营证据。

## 10. 明确不在本 PR 内

不修改 runtime、validator、schema、API、DDL、workflow 或 deployment；不恢复 IMPL2 文件；不把 DOCUMENTED_ONLY 或 PARTIAL_EVIDENCE 升级为 PASS；不关闭 #1211 或 #1212。
