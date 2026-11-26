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
        - "14-ai-development/work-items/AID-2026-111/manifest.yaml"
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Execution records are pinned local Linux captures; raw stdout hashes identify captures only, while supplied normalised digests use the documented exit/count/harness-multiset algorithm. Repository source predicates were independently read from exact main blobs. No CI, current-main, production, distributed backend or Owner acceptance is claimed."
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
    canonical_scope: "AID-2026-111 exact SQLite implementation test evidence mapping and Gate A/HIR/SC rejudgment"
    canonical_scope_id: "ai-development/aid-2026-109-sqlite-evidence-rejudgment"
    canonical_scope_keywords:
      - sqlite
      - implementation-evidence
      - gate-a
      - storage-consistency
      - idempotency
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/work-items/AID-2026-111/evidence.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-111/evidence.md"
---

# AID-2026-111 — SQLite implementation evidence mapping and predicate rejudgment

- Work item: `AID-2026-111`; `id_status: PROVISIONAL`.
- **Renumbering / RENUMBERED_FROM:** the initial provisional allocation AID-2026-109 collided with a different item now on main; AID-2026-110 was already reserved by PR #1304 (and had a prior historical use in #1287). This work item is therefore AID-2026-111. PR #1303 was closed unmerged; its branch is provenance only.
- Attribution: **user-authorized operator (delegated by account owner)**; 2026-11-26. Delegated proxy record only; no natural-person Owner signature is represented.
- Allocation baseline: main `e3a134de856bbb58581fd688462c9c0282631270`; INDEX maximum was AID-2026-108; AID-2026-111 absent from INDEX/tree, Issue search and branch-name search at allocation. AID-2026-109 and AID-2026-110 were occupied at the rescan; AID-2026-111 was free. New branch created from `e3a134de856bbb58581fd688462c9c0282631270`; synchronized again with main `248cef62410cb4a412efb2d83326a1ce32345765` before exact-head checks.
- Prior matrix: AID-2026-095 / PR #1264; prior refresh AID-2026-107 / PR #1290. This item supersedes only the evidence assessment, not the source artifacts.
- Source predicates: Storage SC table `10-storage-consistency/storage-physical-consistency-contract.md` @ `d571f086505b312c40b6ae2e56a868131cfffc78`; HIR table `08-bmcp-protocol/h-idempotency-namespace-and-replay-boundary-contract.md` @ `f64dd8f520b98e52a7151619cb279fc0b4c38c89`; AID-095 matrix blob `1d162b527eacb96e2cff24eec5fcf5a66014039a`; current AID-107 evidence blob `cce956d97b7a6d969bb3245fe0890905ca6d3979` (72-row matrix section byte-identical to prior source); AID-108 correction manifest blob `1164fb16a65c2a252697751dce76fa9584a36165`.
- Related Issues: #1211 (Storage source/implementation drift) and #1212 (A–I + Storage composition). Both remain OPEN.

## 1. Executive result

The supplied SQLite backend execution is meaningful implementation evidence for local SQLite transaction, CAS, idempotency, scope, Forget Fence, visibility, crash/reopen and selected WAL behaviors. It does **not** establish all 88 predicates.

| Assessment set | PASS | PARTIAL_EVIDENCE | UNCHANGED | Total |
|---|---:|---:|---:|---:|
| AID-095 Gate A matrix (8 × 9) | 0 | 23 | 49 | 72 |
| Storage SC EVIDENCE_REQUIRED | 0 | 6 | 2 | 8 |
| H idempotency HIR EVIDENCE_REQUIRED | 0 | 5 | 3 | 8 |
| Combined 72 + 16 | **0** | **36** | **52** | **88** |

No predicate receives PASS. A local SQLite test is not a substitute for an end-to-end Owner boundary, an accepted cross-resource coordinator, production durability, or a full H/I security check. All 72 AID-095 matrix cells remain NOT EVIDENCED as their underlying Gate A state; PARTIAL_EVIDENCE records test coverage of a subset, not a state promotion.

## 2. Exact execution evidence

### 2.1 SQLite backend run — user-supplied execution record

- Environment: WSL2 Ubuntu 24.04; rustup stable 1.100.0; bundled SQLite build.
- Exact HEAD: `a123ea4e414c9f74fa0c576fbd718049a7d9f917`.
- Command (verbatim):

```sh
cargo test -p memory-storage-sqlite -p memory-event-store-sqlite --no-fail-fast
```

| Field | Recorded value |
|---|---|
| Exit code | **0** |
| Test binaries | 8 |
| Passed / failed | **99 / 0** |
| stdout bytes | 9465 |
| stdout SHA-256 | `a15e3862af4d6cd97a4cd8caf6f133f57e3c3636ba284bdfd5afaa9237ba2952` (this capture only) |
| Normalised digest | `92c368733aa89e426d1508a55584a5a4b8f0cc4f9b91aab6723820f6260ca086` |
| Test-name recovery | recovered **94 of 99** passed tests (best-effort; interleaved libtest output can swallow `... ok` suffixes) |

**Raw-output stability:** the same command on the same commit was run five times and produced five different raw stdout SHA-256 values. Parallel libtest completion order, duration lines, build timing, and SQLite child-process stdout interleaving make raw stdout non-deterministic. The raw SHA-256 above therefore pins this capture only; it is not a reproducible constant.

**Harness count (authoritative):** sum complete `test result:` lines and exclude child-process rows with `filtered out > 0`: `26 + 5 + 2 + 6 + 60 = 99`. Do not count `test ... ok` lines. The test-name list is best-effort; harness counts, not the name inventory, are authoritative.

### 2.2 Pure Rust layer — supplementary user-supplied run

- Environment: WSL2 Ubuntu 24.04; rustup stable 1.100.0.
- Exact HEAD: `44dc21a4970192118ba434801b8ca05702ac582c`.
- Command (verbatim):

```sh
cargo test -p memory-domain -p memory-storage -p memory-event-store -p bmcp-protocol -p agent-integration --no-fail-fast
```

| Field | Recorded value |
|---|---|
| Exit code | **0** |
| Test binaries | 15 |
| Passed / failed | **276 / 0** |
| stdout bytes | 47066 |
| stdout SHA-256 | `C18EF5FC121EEB9B486000180F52BAE8385385722A369ADDAB873FCF8716D7B9` (this capture only) |
| Normalised digest | `73d97ed8f536aa06cf483f84e750ddbda610d56e8f5caee501fac6f198934eee` |

This supplements pure-Rust domain/protocol/storage trait evidence. It ran on **a different pinned commit** (`44dc21a4…`) from the SQLite and memory-context runs (`a123ea4e…`); do not describe the three groups as running on one commit. The supplied normalised digest is computed from exit code + passed/failed totals + the sorted multiset of per-harness passed counts, excluding ordering, durations and process interleaving. The test-name inventory was not supplied for this group; harness counts remain authoritative.

### 2.3 Memory-context group — supplied aggregate local execution evidence

- Environment: WSL2 Ubuntu 24.04.
- Exact HEAD: `a123ea4e414c9f74fa0c576fbd718049a7d9f917` (same pinned commit as the SQLite group).
- Passed / failed: **177 / 0**.
- Exact command, test-binary count, stdout byte count, raw stdout SHA-256, per-harness passed multiset, and test-name inventory: **NOT_RECORDED in the supplied evidence**.
- Normalised digest: **NOT_SUPPLIED**; it cannot be derived from the aggregate `177 passed` count alone.

This is a pinned-commit local Linux execution, not CI and not current `main`. The test-name inventory is best-effort; where no inventory was supplied, no test-name coverage is inferred.

### 2.4 Explicit negative build evidence

On the Windows host, `cargo test --workspace` exited **101** because `libsqlite3-sys v0.40.0` build script could not execute `cc1` (`gcc.exe: fatal error: cannot execute 'cc1'`); MSVC also lacked `cl.exe`/`link.exe`. The following packages therefore could not be built on that Windows host: `memory-storage-sqlite`, `memory-event-store-sqlite`, `memory-store`, `memory-compiler`, `memory-context`, `brain-cli`.

| Field | Recorded value |
|---|---|
| Exit code | **101** |
| stdout bytes | 12456 |
| stdout SHA-256 | `93BCDC26AB0B29CEDBEC56DD11BB735C8050DB18366A3F296B45C699C072C2B2` (this capture only) |

This is a toolchain limitation on the Windows host, not evidence that the code or tests fail. SQLite backend evidence was therefore produced on WSL2 Linux, not Windows.

## 3. Evidence boundary — mandatory qualification for every PARTIAL_EVIDENCE

All three positive test groups are **pinned-commit local Linux executions** (SQLite 99 and memory-context 177 at `a123ea4e`; pure Rust 276 at `44dc21a4`). They are **not CI**, are **not runs on current `main`**, and do not establish a distributed backend, multi-replica linearizability, or production topology. The SQLite group specifically uses bundled SQLite. It does not prove device/controller/filesystem power-loss semantics, production backup/failover RPO/RTO, independent cross-resource coordinator acceptance, or Owner acceptance. A passing process-crash test does not automatically prove physical power-loss durability. Any use of these results must retain each group’s own exact HEAD and command where recorded. Raw stdout SHA-256 values are capture-only; use the normalised digest for reproducible comparison.

## 4. Test-name-to-predicate mapping (94 supplied names)

The mapping below is deliberately conservative and lexical/semantic: a mapped ID means the test name and described behavior touch part of that predicate, not that the predicate passes. An empty mapping means no corresponding SC/HIR predicate is evidenced by that test name alone. Full test names are preserved exactly.

| Test | Exact test name | SC predicates touched | HIR predicates touched | Mapping boundary |
|---|---|---|---|---|
| T01 | `committed_payload_survives_process_crash_and_wal_recovery` | SC-04, SC-05, SC-06 | HIR-16 | 覆盖 SQLite WAL/recovery 局部行为；不证明设备 flush、完整 checkpoint 协议或 H↔Storage 跨边界恢复。 |
| T02 | `concurrent_appends_preserve_unique_order_and_payload_custody` | SC-01, SC-09 | 无对应测试 | 覆盖 append ordering/concurrency 局部行为；不证明 Owner write-set 完整性或分布式线性化。 |
| T03 | `concurrent_forget_waits_for_restore_snapshot_lock` | SC-06, SC-10, SC-11, SC-12, SC-13, SC-09 | HIR-18 | 覆盖 SQLite restore lock 的并发序列化和 D Fence 一侧；缺 I 授权重查。 |
| T04 | `crash_after_fence_commit_is_retried_without_resurrection` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 只覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed；HIR-18 缺 I PermissionEpoch 当前授权重查及 D/I anti-rollback 联动。 |
| T05 | `failed_payload_insert_rolls_back_event_payload_and_outbox_rows` | SC-01, SC-02, SC-06 | HIR-06, HIR-16 | 覆盖单资源事务回滚/崩溃切面；缺完整 Owner write-set、H↔Storage 协调和物理断电语义。 |
| T06 | `fence_restore_purges_one_scope_from_a_store_built_database` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T07 | `forget_fence::tests::concurrent_forget_serializes_behind_restore_fence_lock` | SC-06, SC-10, SC-11, SC-12, SC-13, SC-09 | HIR-18 | 覆盖 SQLite restore lock 的并发序列化和 D Fence 一侧；缺 I 授权重查。 |
| T08 | `forget_fence::tests::crash_after_fence_commit_is_retried_safely_on_restore` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 只覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed；HIR-18 缺 I PermissionEpoch 当前授权重查及 D/I anti-rollback 联动。 |
| T09 | `forget_fence::tests::malformed_scope_refuses_activation_without_partial_change` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T10 | `forget_fence::tests::missing_or_corrupt_fence_fails_closed` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 只覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed；HIR-18 缺 I PermissionEpoch 当前授权重查及 D/I anti-rollback 联动。 |
| T11 | `forget_fence::tests::restore_anti_resurrection_purges_only_fenced_scope_across_all_tables` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T12 | `live_wal_copy_fails_closed_until_checkpointed` | SC-04, SC-05, SC-06 | HIR-16 | 覆盖 SQLite WAL/recovery 局部行为；不证明设备 flush、完整 checkpoint 协议或 H↔Storage 跨边界恢复。 |
| T13 | `malformed_scope_refuses_activation_without_partial_change` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T14 | `missing_or_corrupt_fence_fails_closed` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 只覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed；HIR-18 缺 I PermissionEpoch 当前授权重查及 D/I anti-rollback 联动。 |
| T15 | `ordered_read_rejects_payload_and_verified_digest_tampering` | SC-02, SC-07 | 无对应测试 | 覆盖输入校验/摘要完整性/scope 拒绝的部分；不证明完整 transaction/restore/权限谓词。 |
| T16 | `payload::tests::duplicate_payload_append_returns_original_receipt_without_duplicate_rows` | SC-07, SC-08 | HIR-14 | 覆盖 Storage/producer receipt replay；不证明 H receipt/namespace 或 tombstone horizon。 |
| T17 | `payload::tests::payload_append_receipt_and_ordered_read_survive_reopen` | SC-07, SC-08 | 无对应测试 | 覆盖 SQLite receipt reopen/replay；不是 H-owned receipt 或 H tombstone 证据。 |
| T18 | `payload::tests::payload_digest_mismatch_is_rejected_before_append` | SC-02, SC-07 | 无对应测试 | 覆盖输入校验/摘要完整性/scope 拒绝的部分；不证明完整 transaction/restore/权限谓词。 |
| T19 | `payload::tests::read_after_fails_closed_on_empty_persisted_scope_list` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T20 | `payload::tests::read_after_fails_closed_on_invalid_persisted_scope_ref` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T21 | `payload::tests::read_after_paginates_interleaved_scope_rows_by_visible_limit` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T22 | `payload::tests::read_after_skips_non_intersecting_scopes_and_limits_visible_rows` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T23 | `payload_persistence_boundary_sizes_survive_reopen` | SC-01 | 无对应测试 | 只触及 payload 持久化边界/尺寸，不证明 CAS、Owner cursor、idempotency、outbox 与 receipt 全写集。 |
| T24 | `restart_preserves_receipt_and_idempotent_payload_replay` | SC-07, SC-08 | HIR-14 | 覆盖 SQLite receipt reopen/replay；不是 H-owned receipt 或 H tombstone 证据。 |
| T25 | `restore_anti_resurrection_and_preserves_other_scope` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T26 | `tests::abrupt_exit_worker` | 无对应测试 | 无对应测试 | 辅助 worker 名称或未覆盖的语义；无对应测试。 |
| T27 | `tests::abrupt_process_exit_rolls_back_entire_uncommitted_commit` | SC-01, SC-02, SC-06 | HIR-06, HIR-16 | 覆盖单资源事务回滚/崩溃切面；缺完整 Owner write-set、H↔Storage 协调和物理断电语义。 |
| T28 | `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable` | SC-07, SC-08 | 无对应测试 | 覆盖 SQLite receipt reopen/replay；不是 H-owned receipt 或 H tombstone 证据。 |
| T29 | `tests::empty_scope_and_missing_payload_identity_are_rejected` | SC-10, SC-12, SC-02, SC-07 | 无对应测试 | 覆盖输入校验/摘要完整性/scope 拒绝的部分；不证明完整 transaction/restore/权限谓词。 |
| T30 | `tests::f1_forget_memory_hides_current_and_history` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 只覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed；HIR-18 缺 I PermissionEpoch 当前授权重查及 D/I anti-rollback 联动。 |
| T31 | `tests::f10_forget_survives_reopen` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 只覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed；HIR-18 缺 I PermissionEpoch 当前授权重查及 D/I anti-rollback 联动。 |
| T32 | `tests::f2_forget_memory_excludes_from_change_pages` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T33 | `tests::f3_forget_memory_rejects_new_commit` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 只覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed；HIR-18 缺 I PermissionEpoch 当前授权重查及 D/I anti-rollback 联动。 |
| T34 | `tests::f4_forget_memory_rejects_prepare_and_publish` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 只覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed；HIR-18 缺 I PermissionEpoch 当前授权重查及 D/I anti-rollback 联动。 |
| T35 | `tests::f5_forget_memory_blocks_idempotency_replay` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 只覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed；HIR-18 缺 I PermissionEpoch 当前授权重查及 D/I anti-rollback 联动。 |
| T36 | `tests::f6_forget_is_idempotent` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 只覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed；HIR-18 缺 I PermissionEpoch 当前授权重查及 D/I anti-rollback 联动。 |
| T37 | `tests::f7_forget_version_only_hides_that_version` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 只覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed；HIR-18 缺 I PermissionEpoch 当前授权重查及 D/I anti-rollback 联动。 |
| T38 | `tests::f8_forget_version_blocks_child_commit` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 只覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed；HIR-18 缺 I PermissionEpoch 当前授权重查及 D/I anti-rollback 联动。 |
| T39 | `tests::f9_forget_memory_sets_lifecycle_state` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 只覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed；HIR-18 缺 I PermissionEpoch 当前授权重查及 D/I anti-rollback 联动。 |
| T40 | `tests::file_backed_connection_applies_required_sqlite_pragmas` | SC-04 | 无对应测试 | 仅证明 SQLite pragma 被应用，不证明底层设备 flush、WAL commit marker 或 durable ordering。 |
| T41 | `tests::file_db_busy_timeout_bounds_wait_for_long_immediate_transaction` | SC-09 | 无对应测试 | 只证明本地 busy timeout 等待上界，不构成完整隔离 profile 或跨节点线性化证据。 |
| T42 | `tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent` | SC-01, SC-02, SC-06, SC-08 | HIR-06, HIR-16 | 覆盖单资源 interrupted-commit 后 pointer/log/idempotency 一致性；缺完整 Owner write-set 与 H↔Storage 跨边界恢复。 |
| T43 | `tests::file_db_nested_savepoint_rollback_preserves_outer_work` | SC-02 | 无对应测试 | 覆盖单资源 savepoint rollback 保留外层事务；不证明 crash/WAL 或 H protocol 谓词。 |
| T44 | `tests::file_db_unwinding_worker_releases_open_transaction_without_partial_state` | SC-02, SC-06 | HIR-16 | 覆盖本地 unwind 时事务释放/无部分状态；不证明完整 crash-cut、H recovery 或跨资源 reconciliation。 |
| T45 | `tests::independent_connections_serialize_conflicting_idempotency_payloads` | SC-08, SC-09 | HIR-08, HIR-14 | 覆盖 SQLite 连接/请求并发幂等竞争；不证明 H-owned ledger 的完整 namespace 与 H admission authority。 |
| T46 | `tests::multi_process_cas_worker` | 无对应测试 | 无对应测试 | 辅助 worker 名称或未覆盖的语义；无对应测试。 |
| T47 | `tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt` | SC-08, SC-09 | HIR-08, HIR-14 | 覆盖 SQLite 连接/请求并发幂等竞争；不证明 H-owned ledger 的完整 namespace 与 H admission authority。 |
| T48 | `tests::pending_compile_intent_carries_the_payload_and_envelope_a_compiler_needs` | SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填局部实现；不证明 E admission 完整原子边界。 |
| T49 | `tests::pending_compile_intent_created_at_matches_the_acceptance_time` | SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填局部实现；不证明 E admission 完整原子边界。 |
| T50 | `tests::pending_compile_intent_fails_closed_when_stored_payload_is_tampered_with` | SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填局部实现；不证明 E admission 完整原子边界。 |
| T51 | `tests::pending_compile_intent_is_invisible_when_no_payload_was_stored` | SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填局部实现；不证明 E admission 完整原子边界。 |
| T52 | `tests::pending_compile_intents_fails_closed_when_stored_bytes_are_tampered` | SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填局部实现；不证明 E admission 完整原子边界。 |
| T53 | `tests::pending_compile_intents_is_empty_on_a_fresh_store` | SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填局部实现；不证明 E admission 完整原子边界。 |
| T54 | `tests::pending_compile_intents_is_idempotent_and_does_not_consume` | SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填局部实现；不证明 E admission 完整原子边界。 |
| T55 | `tests::pending_compile_intents_returns_accepted_events_in_insertion_order` | SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填局部实现；不证明 E admission 完整原子边界。 |
| T56 | `tests::same_producer_key_and_digest_replay_original_receipt` | SC-08 | HIR-02, HIR-14 | 覆盖 producer key 同 digest replay / 异 digest conflict；不覆盖 H 完整 namespace tuple、Attempt 规则或 H ledger。 |
| T57 | `tests::same_producer_key_with_different_digest_conflicts` | SC-08 | HIR-02, HIR-14 | 覆盖 producer key 同 digest replay / 异 digest conflict；不覆盖 H 完整 namespace tuple、Attempt 规则或 H ledger。 |
| T58 | `tests::separate_processes_serialize_competing_file_backed_cas_writers` | SC-09 | 无对应测试 | 覆盖本地多进程 CAS writers 序列化；不是多节点/多副本线性化。 |
| T59 | `tests::sqlite_change_listing_surfaces_corrupt_scope_metadata_instead_of_silently_skipping_it` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T60 | `tests::sqlite_change_pages_filter_scope_before_applying_limit` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T61 | `tests::sqlite_change_pages_with_limit_two_preserve_order_without_skips_or_duplicates` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T62 | `tests::sqlite_denies_fresh_cross_scope_write_without_persisting_any_commit_state` | SC-10, SC-12, SC-02, SC-07 | 无对应测试 | 覆盖输入校验/摘要完整性/scope 拒绝的部分；不证明完整 transaction/restore/权限谓词。 |
| T63 | `tests::sqlite_does_not_replay_idempotency_key_across_memories` | SC-08 | HIR-14 | 覆盖 key 不跨 memory scope 重放；缺 H 完整 namespace tuple 与 H-owned receipt。 |
| T64 | `tests::sqlite_does_not_replay_idempotency_receipt_before_scope_check` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T65 | `tests::sqlite_filters_nested_claims_by_the_callers_scope` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T66 | `tests::sqlite_hides_entire_multiscope_claim_from_partial_scope_reader` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T67 | `tests::sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup` | SC-02, SC-07, SC-08 | HIR-14 | 覆盖 digest mismatch 对 commit/receipt lookup 冲突；缺 H 完整 namespace tuple 与 H-owned immutable receipt。 |
| T68 | `tests::sqlite_multiple_preparations_reserve_unique_negative_sequences` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T69 | `tests::sqlite_prepare_does_not_add_change_log_entries` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T70 | `tests::sqlite_prepare_hides_version_from_read_version` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T71 | `tests::sqlite_prepare_keeps_current_version_unchanged` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T72 | `tests::sqlite_prepare_rejects_idempotency_digest_conflict` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T73 | `tests::sqlite_prepare_replay_returns_same_receipt` | SC-07, SC-08, SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-14, HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T74 | `tests::sqlite_publication_state_honours_scope_and_forget_fences` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T75 | `tests::sqlite_publication_state_reports_prepared_hidden_then_published` | SC-10, SC-12 | 无对应测试 | 覆盖本地 prepared-hidden/published visibility；缺副本 applied position 与 D/I 全域 currentness。 |
| T76 | `tests::sqlite_publication_state_returns_none_for_unknown_or_legacy_publication` | SC-10, SC-12 | 无对应测试 | 覆盖未知/legacy publication 的本地读行为；缺全权威读路径及副本可见性证明。 |
| T77 | `tests::sqlite_publish_allocates_sequence_only_at_publish_time` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T78 | `tests::sqlite_publish_makes_prepared_version_current_and_readable` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T79 | `tests::sqlite_publish_rejects_duplicate_publication_and_suppressed_state` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T80 | `tests::sqlite_publish_rejects_stale_parent_without_partial_commit` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T81 | `tests::sqlite_publish_replay_returns_original_receipt` | SC-07, SC-08, SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-14, HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T82 | `tests::sqlite_read_version_keeps_legacy_versions_visible` | SC-10 | 无对应测试 | 仅覆盖本地 legacy-version read visibility；不证明 post-commit replica visibility。 |
| T83 | `tests::sqlite_rejects_claim_scope_outside_callers_scope_even_when_parent_contains_it` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T84 | `tests::sqlite_rejects_claims_outside_the_parent_memory_scope` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T85 | `tests::sqlite_rejects_create_outside_requested_scope` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T86 | `tests::sqlite_rejects_empty_idempotency_key_or_request_digest` | SC-02, SC-07 | 无对应测试 | 覆盖输入校验/摘要完整性/scope 拒绝的部分；不证明完整 transaction/restore/权限谓词。 |
| T87 | `tests::sqlite_rejects_invalid_memory_and_orphan_initial_version_pointer` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T88 | `tests::sqlite_rejects_invalid_version_fields_before_writing_any_commit_state` | SC-02, SC-07 | 无对应测试 | 覆盖输入校验/摘要完整性/scope 拒绝的部分；不证明完整 transaction/restore/权限谓词。 |
| T89 | `tests::sqlite_rejects_malformed_nested_claims_before_commit` | SC-02, SC-07 | 无对应测试 | 覆盖输入校验/摘要完整性/scope 拒绝的部分；不证明完整 transaction/restore/权限谓词。 |
| T90 | `tests::sqlite_rejects_mixed_parent_and_foreign_claim_scopes_before_commit` | SC-10, SC-12, SC-02, SC-07 | 无对应测试 | 覆盖输入校验/摘要完整性/scope 拒绝的部分；不证明完整 transaction/restore/权限谓词。 |
| T91 | `tests::sqlite_rejects_stale_expected_version` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T92 | `tests::sqlite_storage_entry_points_reject_empty_and_malformed_scope_sets` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T93 | `tests::startup_backfills_compile_intent_for_preexisting_accepted_events` | SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填局部实现；不证明 E admission 完整原子边界。 |
| T94 | `tests::status_and_replay_enforce_scope` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |

## 5. Rejudgment of all 72 AID-095 Gate A checkpoints

Verdict vocabulary for this evidence review:
- **PASS** requires the named tests to cover the complete checkpoint predicate. None does.
- **PARTIAL_EVIDENCE** means one or more predicate components are exercised, while a named Owner, end-to-end join, cross-resource, replica, security or operational component remains missing.
- **UNCHANGED** means no corresponding test covers the checkpoint's core predicate.

The AID-095 state column remains `NOT EVIDENCED` for every row. PARTIAL_EVIDENCE is an evidence annotation only and is not a PASS or Gate A state promotion.

| Flow | Checkpoint | Prior Gate A state | Evidence verdict | Corresponding tests | Why not PASS / what remains |
|---|---|---|---|---|---|
| F1 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F1 | Request / response | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F1 | Identity / cursor namespace | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F1 | Idempotency scope | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::same_producer_key_and_digest_replay_original_receipt`; `tests::same_producer_key_with_different_digest_conflicts` | Producer-key/digest replay and conflict are tested; the E producer namespace, full scope-before-replay path, and Owner admission semantics are missing. |
| F1 | Linearization point | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::pending_compile_intent_carries_the_payload_and_envelope_a_compiler_needs`; `tests::pending_compile_intent_created_at_matches_the_acceptance_time`; `tests::startup_backfills_compile_intent_for_preexisting_accepted_events` | Local acceptance/compile-intent persistence is partially exercised; there is no proof that E Accepted, envelope, digest, compiler state, and outbox share one atomic boundary. |
| F1 | Durable receipt | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable`; `payload::tests::payload_append_receipt_and_ordered_read_survive_reopen`; `tests::same_producer_key_and_digest_replay_original_receipt` | SQLite receipt reopen/replay is partially exercised; the complete E-issued receipt fields and their binding to the Accepted transaction are missing. |
| F1 | Failure / Unknown | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F1 | Replay / recovery | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::startup_backfills_compile_intent_for_preexisting_accepted_events`; `restart_preserves_receipt_and_idempotent_payload_replay`; `committed_payload_survives_process_crash_and_wal_recovery` | Startup compile-intent backfill and receipt replay after reopen are partially exercised; E dispatcher, lease, DLQ, and Unknown reconciliation are missing. |
| F1 | Visibility | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::pending_compile_intent_is_invisible_when_no_payload_was_stored`; `tests::pending_compile_intents_is_empty_on_a_fresh_store` | The test that hides a compile intent when no payload exists covers one local visibility rule; E/D canonical visibility and all-path enforcement are missing. |
| F2 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F2 | Request / response | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F2 | Identity / cursor namespace | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F2 | Idempotency scope | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt`; `tests::same_producer_key_and_digest_replay_original_receipt`; `tests::same_producer_key_with_different_digest_conflicts`; `tests::sqlite_prepare_rejects_idempotency_digest_conflict` | Same-key/digest replay and conflict are tested; the D canonical-operation namespace and F-consumer deduplication join are missing. |
| F2 | Linearization point | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent`; `tests::sqlite_publish_allocates_sequence_only_at_publish_time`; `tests::sqlite_publish_rejects_stale_parent_without_partial_commit` | Local SQLite transaction/CAS/publish tests cover part of the commit boundary; the single transaction containing the D canonical cursor/outbox and F consumption are missing. |
| F2 | Durable receipt | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable`; `tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt`; `payload::tests::payload_append_receipt_and_ordered_read_survive_reopen` | Durable receipt/reopen/replay tests cover a local receipt subset; the complete D-issued cursor/receipt/outbox chain is missing. |
| F2 | Failure / Unknown | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::abrupt_process_exit_rolls_back_entire_uncommitted_commit`; `tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent`; `tests::file_db_unwinding_worker_releases_open_transaction_without_partial_state` | Transaction rollback/interrupted-commit behavior is tested; D/F Unknown lookup after a lost response, reconciliation, and proof of no duplicate consumption are missing. |
| F2 | Replay / recovery | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `committed_payload_survives_process_crash_and_wal_recovery`; `restart_preserves_receipt_and_idempotent_payload_replay`; `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable` | SQLite receipt replay/reopen is tested; the D-cursor contiguous prefix, F-consumer dedupe/acknowledgement, and gap recovery are missing. |
| F2 | Visibility | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F3 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F3 | Request / response | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F3 | Identity / cursor namespace | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F3 | Idempotency scope | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F3 | Linearization point | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F3 | Durable receipt | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F3 | Failure / Unknown | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F3 | Replay / recovery | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F3 | Visibility | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F4 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F4 | Request / response | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F4 | Identity / cursor namespace | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `payload::tests::read_after_fails_closed_on_empty_persisted_scope_list`; `payload::tests::read_after_fails_closed_on_invalid_persisted_scope_ref`; `tests::f1_forget_memory_hides_current_and_history`; `tests::f7_forget_version_only_hides_that_version` | Scope/Fence identity tests cover a local namespace fragment; the complete identity chain across D operation+generation and E/F/G/H/I target acknowledgements is missing. |
| F4 | Idempotency scope | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::f5_forget_memory_blocks_idempotency_replay`; `tests::f6_forget_is_idempotent` | Forget idempotency and Fence retry are tested; cross-Owner operation+target+generation digest replay is missing. |
| F4 | Linearization point | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `crash_after_fence_commit_is_retried_without_resurrection`; `forget_fence::tests::crash_after_fence_commit_is_retried_safely_on_restore` | The post-Fence-commit crash retry test covers a local linearization fragment; suppression linearization from D's sole authority across all domains is missing. |
| F4 | Durable receipt | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F4 | Failure / Unknown | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `forget_fence::tests::malformed_scope_refuses_activation_without_partial_change`; `forget_fence::tests::missing_or_corrupt_fence_fails_closed`; `malformed_scope_refuses_activation_without_partial_change`; `missing_or_corrupt_fence_fails_closed` | Malformed/missing/corrupt Fence fail-closed tests cover local rejection; offline targets, external replicas, and comprehensive Unknown closure are missing. |
| F4 | Replay / recovery | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `crash_after_fence_commit_is_retried_without_resurrection`; `forget_fence::tests::crash_after_fence_commit_is_retried_safely_on_restore`; `forget_fence::tests::restore_anti_resurrection_purges_only_fenced_scope_across_all_tables`; `restore_anti_resurrection_and_preserves_other_scope` | Fence crash/reopen/anti-resurrection is tested; restore/replay across all E/F/G/H/Storage projections is missing. |
| F4 | Visibility | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::f1_forget_memory_hides_current_and_history`; `tests::f10_forget_survives_reopen`; `tests::f2_forget_memory_excludes_from_change_pages`; `tests::f3_forget_memory_rejects_new_commit`; `tests::f4_forget_memory_rejects_prepare_and_publish`; `tests::f7_forget_version_only_hides_that_version`; `tests::f8_forget_version_blocks_child_commit`; `tests::f9_forget_memory_sets_lifecycle_state`; `tests::sqlite_filters_nested_claims_by_the_callers_scope`; `tests::sqlite_hides_entire_multiscope_claim_from_partial_scope_reader`; `tests::sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup`; `tests::sqlite_multiple_preparations_reserve_unique_negative_sequences`; `tests::sqlite_prepare_does_not_add_change_log_entries`; `tests::sqlite_prepare_hides_version_from_read_version`; `tests::sqlite_prepare_keeps_current_version_unchanged`; `tests::sqlite_prepare_rejects_idempotency_digest_conflict`; `tests::sqlite_prepare_replay_returns_same_receipt`; `tests::sqlite_publication_state_honours_scope_and_forget_fences`; `tests::sqlite_publication_state_reports_prepared_hidden_then_published`; `tests::sqlite_publication_state_returns_none_for_unknown_or_legacy_publication` | Local Fence hiding across read/change/prepare/publish is tested; global read/publication paths, backups, caches, replicas, and D-derived projection rebuild are missing. |
| F5 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F5 | Request / response | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F5 | Identity / cursor namespace | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F5 | Idempotency scope | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F5 | Linearization point | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F5 | Durable receipt | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F5 | Failure / Unknown | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F5 | Replay / recovery | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F5 | Visibility | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F6 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F6 | Request / response | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F6 | Identity / cursor namespace | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F6 | Idempotency scope | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F6 | Linearization point | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F6 | Durable receipt | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F6 | Failure / Unknown | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F6 | Replay / recovery | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F6 | Visibility | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F7 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F7 | Request / response | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F7 | Identity / cursor namespace | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F7 | Idempotency scope | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F7 | Linearization point | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F7 | Durable receipt | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F7 | Failure / Unknown | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F7 | Replay / recovery | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F7 | Visibility | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F8 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F8 | Request / response | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `failed_payload_insert_rolls_back_event_payload_and_outbox_rows`; `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable`; `tests::file_db_nested_savepoint_rollback_preserves_outer_work`; `tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt` | Local Storage SQLite API success/conflict/rejection behavior is tested; the full SC Durable Commit Receipt fields and unified participant request/response are missing. |
| F8 | Identity / cursor namespace | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | No supplied test covers this checkpoint's core predicate; the relevant Owner's end-to-end contract and execution evidence are missing (see the gap list). Adjacent SQLite behavior cannot substitute. |
| F8 | Idempotency scope | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt`; `tests::same_producer_key_and_digest_replay_original_receipt`; `tests::same_producer_key_with_different_digest_conflicts`; `tests::sqlite_prepare_rejects_idempotency_digest_conflict`; `tests::sqlite_prepare_replay_returns_same_receipt`; `tests::sqlite_publish_replay_returns_original_receipt` | Same-key/digest replay/conflict and CAS concurrency are tested; GID+participant semantics and one cross-resource terminal result are missing. |
| F8 | Linearization point | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::abrupt_process_exit_rolls_back_entire_uncommitted_commit`; `tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent`; `tests::file_db_nested_savepoint_rollback_preserves_outer_work`; `tests::sqlite_publication_state_reports_prepared_hidden_then_published`; `tests::sqlite_publish_rejects_stale_parent_without_partial_commit` | Local SQLite transaction, CAS, and prepare/publish commit boundaries are tested; WAL durable flush and an accepted COC terminal decision are missing. |
| F8 | Durable receipt | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `payload::tests::payload_append_receipt_and_ordered_read_survive_reopen`; `restart_preserves_receipt_and_idempotent_payload_replay`; `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable`; `tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt` | Receipt append/reopen/replay is tested; the complete SC-07 minimum fields, COMMITTED/ABORTED/UNKNOWN distinction, and durability-profile readback are missing. |
| F8 | Failure / Unknown | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `failed_payload_insert_rolls_back_event_payload_and_outbox_rows`; `tests::abrupt_process_exit_rolls_back_entire_uncommitted_commit`; `tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent`; `tests::file_db_nested_savepoint_rollback_preserves_outer_work`; `tests::file_db_unwinding_worker_releases_open_transaction_without_partial_state` | Rollback, crash, and interrupted commit are covered; device-level torn-write/flush, restore activation, and cross-resource Unknown resolution are missing. |
| F8 | Replay / recovery | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `committed_payload_survives_process_crash_and_wal_recovery`; `live_wal_copy_fails_closed_until_checkpointed`; `restart_preserves_receipt_and_idempotent_payload_replay`; `restore_anti_resurrection_and_preserves_other_scope`; `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable` | WAL reopen, receipt replay, and Fence restore are partially covered; complete checkpoint/contiguous-log behavior, cross-resource GID participants, and RPO/RTO are missing. |
| F8 | Visibility | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `payload::tests::read_after_fails_closed_on_empty_persisted_scope_list`; `payload::tests::read_after_fails_closed_on_invalid_persisted_scope_ref`; `payload::tests::read_after_paginates_interleaved_scope_rows_by_visible_limit`; `payload::tests::read_after_skips_non_intersecting_scopes_and_limits_visible_rows`; `tests::sqlite_denies_fresh_cross_scope_write_without_persisting_any_commit_state`; `tests::sqlite_does_not_replay_idempotency_key_across_memories`; `tests::sqlite_filters_nested_claims_by_the_callers_scope`; `tests::sqlite_hides_entire_multiscope_claim_from_partial_scope_reader`; `tests::sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup`; `tests::sqlite_multiple_preparations_reserve_unique_negative_sequences`; `tests::sqlite_prepare_does_not_add_change_log_entries`; `tests::sqlite_prepare_hides_version_from_read_version`; `tests::sqlite_prepare_keeps_current_version_unchanged`; `tests::sqlite_prepare_rejects_idempotency_digest_conflict`; `tests::sqlite_prepare_replay_returns_same_receipt`; `tests::sqlite_publication_state_honours_scope_and_forget_fences`; `tests::sqlite_publication_state_reports_prepared_hidden_then_published`; `tests::sqlite_publication_state_returns_none_for_unknown_or_legacy_publication` | Prepared-hidden/published-visible and scope/Fence read filtering are covered; replica applied position, I PermissionEpoch, and full restore-before-exposure paths are missing. |

## 6. Storage SC-04/05/06/10/12/13/17/18 — all eight EVIDENCE_REQUIRED rows

| ID | Evidence verdict | Tests touching predicate | Missing half / why no PASS |
|---|---|---|---|
| SC-04 | **PARTIAL_EVIDENCE** | live_wal_copy_fails_closed_until_checkpointed; committed_payload_survives_process_crash_and_wal_recovery; file_backed_connection_applies_required_sqlite_pragmas | Missing: log framing, log-before-data ordering, commit marker, and actual durable flush/device-barrier evidence under a declared backend profile. |
| SC-05 | **PARTIAL_EVIDENCE** | live_wal_copy_fails_closed_until_checkpointed; committed_payload_survives_process_crash_and_wal_recovery | Missing: checkpoint position/atomicity, replay of a contiguous valid WAL prefix, and truncation/gap fault injection. |
| SC-06 | **PARTIAL_EVIDENCE** | abrupt_process_exit_rolls_back_entire_uncommitted_commit; crash_after_fence_commit_is_retried_safely_on_restore; restore_anti_resurrection_purges_only_fenced_scope_across_all_tables; missing_or_corrupt_fence_fails_closed | Missing: generic torn/partial writes, all crash cuts, and atomic activation of a staged restore image. |
| SC-10 | **PARTIAL_EVIDENCE** | sqlite_prepare_hides_version_from_read_version; sqlite_publication_state_reports_prepared_hidden_then_published; sqlite_publish_makes_prepared_version_current_and_readable; payload::tests::read_after_* | Missing: verification on every authoritative read path and replica applied-position/current-Fence checks; single-database SQLite tests cannot prove replica behavior. |
| SC-12 | **PARTIAL_EVIDENCE** | missing_or_corrupt_fence_fails_closed; malformed_scope_refuses_activation_without_partial_change; payload::tests::read_after_fails_closed_*; tests::f1_forget_memory_* | Missing: a complete D-authority-driven projection rebuild and fail-closed evidence across every read/publication path. |
| SC-13 | **PARTIAL_EVIDENCE** | restore_anti_resurrection_and_preserves_other_scope; forget_fence::tests::restore_anti_resurrection_purges_only_fenced_scope_across_all_tables; crash_after_fence_commit_is_retried_without_resurrection | Only local D Fence/anti-resurrection paths are covered; I PermissionEpoch, independent anti-rollback-anchor linkage, and backup restore-before-exposure are missing. |
| SC-17 | **UNCHANGED** | 无对应测试 | Missing: stable cross-resource GID participants, durable prepare/vote/terminal records, one accepted coordinator terminal authority, and deterministic recovery tests. |
| SC-18 | **UNCHANGED** | 无对应测试 | Missing: repeatable backup/replica rollback/failover workload evidence, declared RPO/RTO, and production-topology exercises. |

## 7. HIR-05/06/08/12/14/16/17/18 — all eight EVIDENCE_REQUIRED rows

| ID | Evidence verdict | Tests touching predicate | Missing half / why no PASS |
|---|---|---|---|
| HIR-05 | **UNCHANGED** | 无对应测试 | Missing: an H-owned durable reservation ledger, tombstone retention horizon, and replay-expiry policy; a SQLite Storage receipt is not an H reservation. |
| HIR-06 | **PARTIAL_EVIDENCE** | file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent; sqlite_publish_rejects_stale_parent_without_partial_commit; failed_payload_insert_rolls_back_event_payload_and_outbox_rows | Covers parts of Storage CAS/idempotency/rollback; missing the complete AID-098 Owner write-set, outbox+receipt+cursor in one transaction, and accepted Owner mapping. |
| HIR-08 | **PARTIAL_EVIDENCE** | concurrent_identical_idempotency_requests_replay_one_durable_receipt; independent_connections_serialize_conflicting_idempotency_payloads | Covers concurrent SQLite idempotency contention; missing contention in the H-owned ledger namespace, an explicit H winner, and an H durable admission receipt. |
| HIR-12 | **UNCHANGED** | 无对应测试 | Missing: an H Pending duplicate returning the same H receipt without a second logical execution; E compile-intent pending tests are not the H protocol ledger. |
| HIR-14 | **PARTIAL_EVIDENCE** | same_producer_key_and_digest_replay_original_receipt; same_producer_key_with_different_digest_conflicts; sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup | Covers producer/Storage key+digest replay/conflict; missing same-key semantics under the full H namespace tuple and an H-owned immutable receipt. |
| HIR-16 | **PARTIAL_EVIDENCE** | committed_payload_survives_process_crash_and_wal_recovery; abrupt_process_exit_rolls_back_entire_uncommitted_commit; restart_preserves_receipt_and_idempotent_payload_replay | Covers single-resource SQLite crash/reopen/replay; missing cross-boundary reconciliation around H and Storage commit, same-GID lookup, and proof of no repeated domain effect. |
| HIR-17 | **UNCHANGED** | 无对应测试 | Missing integration tests joining H Attempt to distinct C/G DeliveryAttempt, binding C evidence, and independently deciding G AppliedAttestation/Applied. |
| HIR-18 | **PARTIAL_EVIDENCE** | forget_fence::tests::missing_or_corrupt_fence_fails_closed; tests::f1_forget_memory_hides_current_and_history; tests::f5_forget_memory_blocks_idempotency_replay; tests::f10_forget_survives_reopen | Only D Fence-side fail-closed behavior is covered; missing I PermissionEpoch/current-authorization recheck, issuer/key-status revalidation, and D/I anti-rollback-anchor linkage. |

## 8. Gate A and Gate B disposition

**Gate A: PARTIAL / OPEN — unchanged.** There are zero complete PASS predicates in the 72-cell Gate A matrix. The SQLite evidence adds partial implementation evidence to selected cells, but does not complete any eight-flow end-to-end row or provide the Owner acceptance and full composition needed to close Gate A.

The existing nine-item closeout list remains:
1. Main synchronization and exact-head freshness — must be checked at final PR Head.
2. Cross-Owner role dispositions — proxy dispositions remain distinct from natural-person Owner acceptance.
3. Exact-head CI — all 16 required contexts must succeed on the final PR Head.
4. Complete eight-flow A–I + Storage composition package and relevant Owner acceptance.
5. D/E/F/I normative roots / IMPL2: **OPEN — scope adjudicated; 5 NORMATIVE_ROOT candidates require a separate restoration PR; 83 HISTORICAL_PHASE_RECORD and 101 UNDECIDED paths stay out of main without Owner ruling; F/I root identification or explicit replacement decision remains open.**
6. Storage physical contract plus complete SC evidence, including SC-17/18.
7. H idempotency/replay plus complete HIR evidence, including HIR-17/18.
8. Full Canonical/EN/ZH-CN semantic and source-revision parity.
9. DEC-13 normative approval evidence and any outstanding natural-person Owner/joint acceptance.

**Gate B: PARTIAL / OPEN (NOT VERIFIED) — unchanged.** Local SQLite tests do not establish deployment, production conformance, distributed/multi-replica consistency, operational backup/failover or production RPO/RTO.


### 8.1 IMPL2 scope ruling carried forward from current AID-2026-107

AID-2026-107 current-main evidence blob `cce956d97b7a6d969bb3245fe0890905ca6d3979` records the file-level disposition for the 03/04/05/09 Owner-source trees: 189 missing Canonical paths are classified as **5 NORMATIVE_ROOT**, **83 HISTORICAL_PHASE_RECORD**, and **101 UNDECIDED**. The 72-row AID-095 matrix section is byte-identical to the earlier AID-107 evidence blob used when this review was drafted.

Gate A item 5 is therefore actionable, not an unbounded restore request:
- **5 NORMATIVE_ROOT** files are candidates for a separate Owner-reviewed restoration PR; this evidence PR does not restore them.
- **83 HISTORICAL_PHASE_RECORD** and **101 UNDECIDED** files do not enter main without explicit Owner ruling. No Owner ruling means no merge for either class.
- F and I source-root gaps remain explicit: the F runtime root and I security root artifacts still require Owner identification or an explicit replacement decision; candidate overview files are not silently substituted.
- These classifications do not imply approval, freeze, implementation, or conformance.

**Gate A item 5: OPEN — scope adjudicated; 5 identified roots to restore in a separate PR; F/I source artifacts still require Owner identification or an explicit replacement decision.**

## 9. Explicit unresolved implementation predicates

- **SC-17:** no stable cross-resource GID participant set, durable prepare/vote/terminal records, single accepted terminal-decision authority or participant replay/recovery.
- **SC-18:** no backup/restore, replica rollback, failover, repeatable RPO/RTO profile or production-topology exercise.
- **HIR-17:** no H Attempt-to-C/G DeliveryAttempt join; no G AppliedAttestation or independent Applied decision test.
- **HIR-18:** no I PermissionEpoch monotonicity/current authorization recheck before replay disclosure; D Fence tests do not satisfy the I half.
- **D/I anti-rollback:** no independent anchor linkage across D Fence and I PermissionEpoch during restore; no pre-Fence/pre-revocation backup resurrection test spanning both authorities.
- No CI evidence is claimed for either local test run.

## 10. Non-claims and constraints

- No PASS is assigned in this review.
- `PARTIAL_EVIDENCE` does not change any Gate A state to PASS.
- No runtime, validator semantics, schema, API, DDL, test, workflow, deployment or production configuration was changed by this evidence-record PR.
- No Owner acceptance or natural-person signature is claimed.
- #1211 and #1212 remain OPEN; this record does not close either Issue.

## 11. Attribution

user-authorized operator (delegated by account owner); 2026-11-26. Delegated evidence recording only; no natural-person Owner signature is fabricated.
## Session role / use case

Documentation author and evidence adjudicator for the SQLite implementation-test evidence supplied for AID-2026-111. The work reads exact source predicates, maps the supplied test names, and records bounded evidence classifications. No runtime, validator, schema, test, workflow, deployment or production change was made.

## Actual AI input

NOT_RECORDED

The original user message was not preserved verbatim as a repository artifact. The committed `prompt-v1.md` is a structured task snapshot, not a byte-for-byte transcript of the complete user message. The 94 test names and the supplied execution metadata are preserved in this evidence record.

## AI-visible output

Created this Canonical evidence record and its EN and ZH-CN counterparts, mapped 94 supplied test names to SC/HIR predicates, rejudged 72 Gate A cells and 16 EVIDENCE_REQUIRED rows, and recorded 0 PASS, 34 PARTIAL_EVIDENCE and 54 UNCHANGED across the combined 88 rows. Gate A remains PARTIAL / OPEN; Gate B remains PARTIAL / OPEN (NOT VERIFIED). The exact local-run limitations and unresolved SC-17/18, HIR-05/12/17/18 and D/I anti-rollback gaps are recorded above.
