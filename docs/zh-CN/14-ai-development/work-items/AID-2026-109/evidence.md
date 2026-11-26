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
        - "14-ai-development/work-items/AID-2026-109/manifest.yaml"
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "94 个测试名及运行元数据按用户提供的可复现执行记录登记；谓词来自精确 main blob。未声称 CI、生产、分布式后端或 Owner 验收。"
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
    canonical_scope: "AID-2026-109 SQLite 实现测试证据映射与 Gate A/HIR/SC 谓词重判"
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
    en: "docs/en/14-ai-development/work-items/AID-2026-109/evidence.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-109/evidence.md"
---

# AID-2026-109 — SQLite 后端实现证据映射与谓词重判

- Work item：`AID-2026-109`；`id_status: PROVISIONAL`。
- 署名：**user-authorized operator (delegated by account owner)**；日期：**2026-11-26**。仅为委托代理记录，不代表自然人 Owner 签署。
- 取号基线：main `a7e7c64bfd6c6d709a0a7b55358f94b8535815c1`；INDEX 最大编号为 AID-2026-108；分配时 AID-2026-109 不存在于 INDEX/tree、Issue 搜索和分支名中。新分支从该精确 main 创建。
- 前序矩阵：AID-2026-095 / PR #1264；前次刷新 AID-2026-107 / PR #1290。本工作项只更新证据评估，不修改源矩阵。
- 谓词来源：Storage SC 表 `10-storage-consistency/storage-physical-consistency-contract.md` @ `d571f086505b312c40b6ae2e56a868131cfffc78`；HIR 表 `08-bmcp-protocol/h-idempotency-namespace-and-replay-boundary-contract.md` @ `f64dd8f520b98e52a7151619cb279fc0b4c38c89`；AID-095 矩阵 blob `1d162b527eacb96e2cff24eec5fcf5a66014039a`；AID-107 evidence blob `c9a0576eb743e61ced43695d0cfacad4caf7f2e7`。
- 关联 Issue：#1211（Storage 源与实现漂移）及 #1212（A–I + Storage 组合审查），均保持 OPEN。

## 1. 执行结论

本次 SQLite 后端执行为本地 SQLite 事务、CAS、幂等、scope、Forget Fence、可见性、崩溃/重开及部分 WAL 行为提供了有意义的实现证据，但不能满足全部 88 个谓词。

| 评估集合 | PASS | PARTIAL_EVIDENCE | UNCHANGED | 合计 |
|---|---:|---:|---:|---:|
| AID-095 Gate A 矩阵（8 × 9） | 0 | 23 | 49 | 72 |
| Storage SC EVIDENCE_REQUIRED | 0 | 6 | 2 | 8 |
| H 幂等 HIR EVIDENCE_REQUIRED | 0 | 7 | 1 | 8 |
| 合计 72 + 16 | **0** | **36** | **52** | **88** |

没有任何谓词获得 PASS。单机 SQLite 测试不能替代端到端 Owner 边界、已接受的跨资源协调器、生产持久性或完整 H/I 安全检查。所有 72 个 AID-095 矩阵单元的 Gate A 状态仍为 `NOT EVIDENCED`；PARTIAL_EVIDENCE 仅记录局部测试覆盖，不是状态升级。

## 2. 精确执行证据

### 2.1 SQLite 后端运行——用户提供的执行记录

- 环境：WSL2 Ubuntu 24.04；rustup stable 1.100.0；bundled SQLite 构建。
- 精确 HEAD：`a123ea4e414c9f74fa0c576fbd718049a7d9f917`。
- 命令原文：

```sh
cargo test -p memory-storage-sqlite -p memory-event-store-sqlite --no-fail-fast
```

| 字段 | 记录值 |
|---|---|
| Exit code | **0** |
| 测试二进制 | 8 |
| Passed / failed | **99 / 0** |
| stdout 字节数 | 9465 |
| stdout SHA-256 | `a15e3862af4d6cd97a4cd8caf6f133f57e3c3636ba284bdfd5afaa9237ba2952` |
| 本记录中提供的具名测试 | 94（用户提供这些名称；99 个通过项中另有 5 项未在所给清单中逐名列出） |

**可复现前提：**完整克隆中包含精确提交 `a123ea4e414c9f74fa0c576fbd718049a7d9f917`，使用 WSL2 Ubuntu 24.04、rustup stable 1.100.0、相同命令及兼容的 bundled-SQLite 构建依赖。这是用户提供的本地执行记录，不是本工作项独立从 CI 获取的产物。

### 2.2 纯 Rust 层——补充的用户执行记录

- 环境：Windows 主机；MinGW 缺少 `cc1`，MSVC 缺少 `cl.exe`/`link.exe`。
- 精确 HEAD：`44dc21a4970192118ba434801b8ca05702ac582c`。
- 命令原文：

```sh
cargo test -p memory-domain -p memory-storage -p memory-event-store -p bmcp-protocol -p agent-integration --no-fail-fast
```

| 字段 | 记录值 |
|---|---|
| Exit code | **0** |
| 测试二进制 | 15 |
| Passed / failed | **276 / 0** |
| stdout 字节数 | 47066 |
| stdout SHA-256 | `C18EF5FC121EEB9B486000180F52BAE8385385722A369ADDAB873FCF8716D7B9` |

该运行补充纯 Rust 领域/协议/Storage trait 证据。它运行于另一个提交，不能为 SQLite 精确头增加后端证据。

### 2.3 明确的负面构建证据

Windows 主机上的 `cargo test --workspace` 因 `libsqlite3-sys v0.40.0` build script 无法执行 `cc1`（`gcc.exe: fatal error: cannot execute 'cc1'`）而 exit **101**；MSVC 同样缺少 `cl.exe`/`link.exe`。因此该 Windows 主机无法构建：`memory-storage-sqlite`、`memory-event-store-sqlite`、`memory-store`、`memory-compiler`、`memory-context`、`brain-cli`。

| 字段 | 记录值 |
|---|---|
| Exit code | **101** |
| stdout 字节数 | 12456 |
| stdout SHA-256 | `93BCDC26AB0B29CEDBEC56DD11BB735C8050DB18366A3F296B45C699C072C2B2` |

这是 Windows 主机工具链限制，不代表代码或测试失败。因此 SQLite 后端证据是在 WSL2 Linux 上产出，而不是 Windows 本机。

## 3. 证据边界——所有 PARTIAL_EVIDENCE 必须保留的限定

SQLite 运行是 **Linux + bundled SQLite 本地执行**，**不是 CI**，不是分布式后端，不是多副本线性化，也不是生产拓扑。它不证明设备/控制器/文件系统断电语义、生产备份/故障切换 RPO/RTO、独立跨资源协调器验收或 Owner 验收。进程崩溃测试通过不自动等同于物理断电持久性。引用结果时必须保留上述精确 HEAD、命令和 SHA-256。

## 4. 94 个具名测试到谓词的映射

映射采用保守的字面/语义原则：映射到某 ID 代表测试名及描述行为触及该谓词的一部分，不代表谓词通过。映射为空表示仅凭该测试名无法证明任何对应 SC/HIR 谓词。94 个测试名称均原样保留。

| 测试 | 精确测试名 | 涉及的 SC 谓词 | 涉及的 HIR 谓词 | 映射边界 |
|---|---|---|---|---|
| T01 | `committed_payload_survives_process_crash_and_wal_recovery` | SC-04, SC-05, SC-06 | HIR-16 | 覆盖 SQLite WAL/恢复路径的部分行为；未证明设备 flush 顺序、checkpoint 完整协议或 H 协调器恢复。 |
| T02 | `concurrent_appends_preserve_unique_order_and_payload_custody` | SC-08, SC-09 | HIR-08, HIR-14 | 覆盖 SQLite 连接/进程并发或幂等竞争的局部行为；未证明分布式/多副本或 H-owned ledger。 |
| T03 | `concurrent_forget_waits_for_restore_snapshot_lock` | SC-08, SC-09, SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-08, HIR-14, HIR-18 | 覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed 片段；HIR-18 所需 I PermissionEpoch 当前授权重查与独立 D/I anti-rollback 联动未覆盖。 |
| T04 | `crash_after_fence_commit_is_retried_without_resurrection` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed 片段；HIR-18 所需 I PermissionEpoch 当前授权重查与独立 D/I anti-rollback 联动未覆盖。 |
| T05 | `failed_payload_insert_rolls_back_event_payload_and_outbox_rows` | SC-01, SC-02, SC-06 | HIR-06, HIR-16 | 覆盖单资源事务回滚/崩溃切面；未证明完整 Owner write-set、H↔Storage 跨边界协调或物理断电语义。 |
| T06 | `fence_restore_purges_one_scope_from_a_store_built_database` | SC-06, SC-10, SC-11, SC-12, SC-13, SC-02 | HIR-18 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T07 | `forget_fence::tests::concurrent_forget_serializes_behind_restore_fence_lock` | SC-08, SC-09, SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-08, HIR-14, HIR-18 | 覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed 片段；HIR-18 所需 I PermissionEpoch 当前授权重查与独立 D/I anti-rollback 联动未覆盖。 |
| T08 | `forget_fence::tests::crash_after_fence_commit_is_retried_safely_on_restore` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed 片段；HIR-18 所需 I PermissionEpoch 当前授权重查与独立 D/I anti-rollback 联动未覆盖。 |
| T09 | `forget_fence::tests::malformed_scope_refuses_activation_without_partial_change` | SC-06, SC-10, SC-11, SC-12, SC-13, SC-02 | HIR-18 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T10 | `forget_fence::tests::missing_or_corrupt_fence_fails_closed` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed 片段；HIR-18 所需 I PermissionEpoch 当前授权重查与独立 D/I anti-rollback 联动未覆盖。 |
| T11 | `forget_fence::tests::restore_anti_resurrection_purges_only_fenced_scope_across_all_tables` | SC-06, SC-10, SC-11, SC-12, SC-13, SC-02 | HIR-18 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T12 | `live_wal_copy_fails_closed_until_checkpointed` | SC-04, SC-05, SC-06 | HIR-16 | 覆盖 SQLite WAL/恢复路径的部分行为；未证明设备 flush 顺序、checkpoint 完整协议或 H 协调器恢复。 |
| T13 | `malformed_scope_refuses_activation_without_partial_change` | SC-06, SC-10, SC-11, SC-12, SC-13, SC-02 | HIR-18 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T14 | `missing_or_corrupt_fence_fails_closed` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed 片段；HIR-18 所需 I PermissionEpoch 当前授权重查与独立 D/I anti-rollback 联动未覆盖。 |
| T15 | `ordered_read_rejects_payload_and_verified_digest_tampering` | SC-02, SC-07, SC-10, SC-12 | 无对应测试 | 覆盖输入校验、摘要完整性或 scope fail-closed；不证明跨资源协调、权限 epoch 或所有投影重建。 |
| T16 | `payload::tests::duplicate_payload_append_returns_original_receipt_without_duplicate_rows` | SC-08, SC-07 | HIR-02, HIR-14, HIR-05, HIR-16 | 覆盖本地 receipt 持久化/重开/重放；未覆盖 H receipt 全字段、长期 tombstone 或跨资源 crash reconciliation。 |
| T17 | `payload::tests::payload_append_receipt_and_ordered_read_survive_reopen` | SC-07, SC-08 | HIR-05, HIR-16 | 覆盖本地 receipt 持久化/重开/重放；未覆盖 H receipt 全字段、长期 tombstone 或跨资源 crash reconciliation。 |
| T18 | `payload::tests::payload_digest_mismatch_is_rejected_before_append` | SC-02, SC-07, SC-10, SC-12 | 无对应测试 | 覆盖输入校验、摘要完整性或 scope fail-closed；不证明跨资源协调、权限 epoch 或所有投影重建。 |
| T19 | `payload::tests::read_after_fails_closed_on_empty_persisted_scope_list` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T20 | `payload::tests::read_after_fails_closed_on_invalid_persisted_scope_ref` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T21 | `payload::tests::read_after_paginates_interleaved_scope_rows_by_visible_limit` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T22 | `payload::tests::read_after_skips_non_intersecting_scopes_and_limits_visible_rows` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T23 | `payload_persistence_boundary_sizes_survive_reopen` | SC-01 | 无对应测试 | 仅触及 payload 持久化边界/尺寸，不证明同一事务的 CAS、Owner cursor、idempotency、outbox 与 receipt 全写集。 |
| T24 | `restart_preserves_receipt_and_idempotent_payload_replay` | SC-08, SC-07 | HIR-02, HIR-14, HIR-05, HIR-16 | 覆盖本地 receipt 持久化/重开/重放；未覆盖 H receipt 全字段、长期 tombstone 或跨资源 crash reconciliation。 |
| T25 | `restore_anti_resurrection_and_preserves_other_scope` | SC-06, SC-10, SC-11, SC-12, SC-13, SC-02 | HIR-18 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T26 | `tests::abrupt_exit_worker` | 无对应测试 | 无对应测试 | 辅助 worker/进程入口名称本身不声明断言；不能单独映射为通过证据。 |
| T27 | `tests::abrupt_process_exit_rolls_back_entire_uncommitted_commit` | SC-01, SC-02, SC-06 | HIR-06, HIR-16 | 覆盖单资源事务回滚/崩溃切面；未证明完整 Owner write-set、H↔Storage 跨边界协调或物理断电语义。 |
| T28 | `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable` | SC-07, SC-08 | HIR-05, HIR-16 | 覆盖本地 receipt 持久化/重开/重放；未覆盖 H receipt 全字段、长期 tombstone 或跨资源 crash reconciliation。 |
| T29 | `tests::empty_scope_and_missing_payload_identity_are_rejected` | SC-02, SC-10, SC-12, SC-07 | 无对应测试 | 覆盖输入校验、摘要完整性或 scope fail-closed；不证明跨资源协调、权限 epoch 或所有投影重建。 |
| T30 | `tests::f1_forget_memory_hides_current_and_history` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed 片段；HIR-18 所需 I PermissionEpoch 当前授权重查与独立 D/I anti-rollback 联动未覆盖。 |
| T31 | `tests::f10_forget_survives_reopen` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed 片段；HIR-18 所需 I PermissionEpoch 当前授权重查与独立 D/I anti-rollback 联动未覆盖。 |
| T32 | `tests::f2_forget_memory_excludes_from_change_pages` | SC-06, SC-10, SC-11, SC-12, SC-13, SC-02 | HIR-18 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T33 | `tests::f3_forget_memory_rejects_new_commit` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed 片段；HIR-18 所需 I PermissionEpoch 当前授权重查与独立 D/I anti-rollback 联动未覆盖。 |
| T34 | `tests::f4_forget_memory_rejects_prepare_and_publish` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed 片段；HIR-18 所需 I PermissionEpoch 当前授权重查与独立 D/I anti-rollback 联动未覆盖。 |
| T35 | `tests::f5_forget_memory_blocks_idempotency_replay` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed 片段；HIR-18 所需 I PermissionEpoch 当前授权重查与独立 D/I anti-rollback 联动未覆盖。 |
| T36 | `tests::f6_forget_is_idempotent` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed 片段；HIR-18 所需 I PermissionEpoch 当前授权重查与独立 D/I anti-rollback 联动未覆盖。 |
| T37 | `tests::f7_forget_version_only_hides_that_version` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed 片段；HIR-18 所需 I PermissionEpoch 当前授权重查与独立 D/I anti-rollback 联动未覆盖。 |
| T38 | `tests::f8_forget_version_blocks_child_commit` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed 片段；HIR-18 所需 I PermissionEpoch 当前授权重查与独立 D/I anti-rollback 联动未覆盖。 |
| T39 | `tests::f9_forget_memory_sets_lifecycle_state` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖 D/Forget Fence 的 SQLite 局部隐藏、锁、恢复或 fail-closed 片段；HIR-18 所需 I PermissionEpoch 当前授权重查与独立 D/I anti-rollback 联动未覆盖。 |
| T40 | `tests::file_backed_connection_applies_required_sqlite_pragmas` | SC-04 | 无对应测试 | 仅证明配置 pragma 应用，不证明底层设备 flush、WAL commit marker durable ordering。 |
| T41 | `tests::file_db_busy_timeout_bounds_wait_for_long_immediate_transaction` | SC-08, SC-09 | HIR-08, HIR-14 | 只证明本地 busy timeout 等待上界，不构成已选定隔离 profile 或跨节点线性化证据。 |
| T42 | `tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent` | SC-01, SC-02, SC-06, SC-03, SC-09, SC-10 | HIR-06, HIR-16 | 覆盖 CAS、prepare/publish 及本地可见性部分；未覆盖 Owner cursor/outbox/receipt 完整原子写集或已接受的 Storage contract。 |
| T43 | `tests::file_db_nested_savepoint_rollback_preserves_outer_work` | SC-01, SC-02, SC-06 | HIR-06, HIR-16 | 覆盖单资源事务回滚/崩溃切面；未证明完整 Owner write-set、H↔Storage 跨边界协调或物理断电语义。 |
| T44 | `tests::file_db_unwinding_worker_releases_open_transaction_without_partial_state` | 无对应测试 | 无对应测试 | 辅助 worker/进程入口名称本身不声明断言；不能单独映射为通过证据。 |
| T45 | `tests::independent_connections_serialize_conflicting_idempotency_payloads` | SC-08, SC-09 | HIR-08, HIR-14 | 覆盖 SQLite 连接/进程并发或幂等竞争的局部行为；未证明分布式/多副本或 H-owned ledger。 |
| T46 | `tests::multi_process_cas_worker` | 无对应测试 | 无对应测试 | 辅助 worker/进程入口名称本身不声明断言；不能单独映射为通过证据。 |
| T47 | `tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt` | SC-08, SC-09, SC-07 | HIR-08, HIR-14, HIR-05, HIR-16 | 覆盖本地 receipt 持久化/重开/重放；未覆盖 H receipt 全字段、长期 tombstone 或跨资源 crash reconciliation。 |
| T48 | `tests::pending_compile_intent_carries_the_payload_and_envelope_a_compiler_needs` | SC-01, SC-07, SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填的局部实现；不证明 E admission 全写集原子性或 D canonical commit。 |
| T49 | `tests::pending_compile_intent_created_at_matches_the_acceptance_time` | SC-01, SC-07, SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填的局部实现；不证明 E admission 全写集原子性或 D canonical commit。 |
| T50 | `tests::pending_compile_intent_fails_closed_when_stored_payload_is_tampered_with` | SC-01, SC-07, SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填的局部实现；不证明 E admission 全写集原子性或 D canonical commit。 |
| T51 | `tests::pending_compile_intent_is_invisible_when_no_payload_was_stored` | SC-01, SC-07, SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填的局部实现；不证明 E admission 全写集原子性或 D canonical commit。 |
| T52 | `tests::pending_compile_intents_fails_closed_when_stored_bytes_are_tampered` | SC-01, SC-07, SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填的局部实现；不证明 E admission 全写集原子性或 D canonical commit。 |
| T53 | `tests::pending_compile_intents_is_empty_on_a_fresh_store` | SC-01, SC-07, SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填的局部实现；不证明 E admission 全写集原子性或 D canonical commit。 |
| T54 | `tests::pending_compile_intents_is_idempotent_and_does_not_consume` | SC-01, SC-07, SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填的局部实现；不证明 E admission 全写集原子性或 D canonical commit。 |
| T55 | `tests::pending_compile_intents_returns_accepted_events_in_insertion_order` | SC-01, SC-07, SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填的局部实现；不证明 E admission 全写集原子性或 D canonical commit。 |
| T56 | `tests::same_producer_key_and_digest_replay_original_receipt` | SC-08, SC-07 | HIR-02, HIR-14, HIR-05, HIR-16 | 覆盖本地 receipt 持久化/重开/重放；未覆盖 H receipt 全字段、长期 tombstone 或跨资源 crash reconciliation。 |
| T57 | `tests::same_producer_key_with_different_digest_conflicts` | SC-08 | HIR-02, HIR-14 | 覆盖 key/digest 重放或冲突的 Storage/producer 层行为；未证明 H 完整 namespace tuple、tombstone horizon 或 H ledger authority。 |
| T58 | `tests::separate_processes_serialize_competing_file_backed_cas_writers` | SC-08, SC-09 | HIR-08, HIR-14 | 覆盖 SQLite 连接/进程并发或幂等竞争的局部行为；未证明分布式/多副本或 H-owned ledger。 |
| T59 | `tests::sqlite_change_listing_surfaces_corrupt_scope_metadata_instead_of_silently_skipping_it` | SC-02, SC-10, SC-12, SC-07 | 无对应测试 | 覆盖输入校验、摘要完整性或 scope fail-closed；不证明跨资源协调、权限 epoch 或所有投影重建。 |
| T60 | `tests::sqlite_change_pages_filter_scope_before_applying_limit` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T61 | `tests::sqlite_change_pages_with_limit_two_preserve_order_without_skips_or_duplicates` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T62 | `tests::sqlite_denies_fresh_cross_scope_write_without_persisting_any_commit_state` | SC-02, SC-10, SC-12, SC-07 | 无对应测试 | 覆盖输入校验、摘要完整性或 scope fail-closed；不证明跨资源协调、权限 epoch 或所有投影重建。 |
| T63 | `tests::sqlite_does_not_replay_idempotency_key_across_memories` | SC-08, SC-10, SC-12 | HIR-02, HIR-14 | 覆盖 memory/scope 边界下 replay 或 status 行为；不覆盖 H 完整 namespace 或 I/D replay disclosure 授权。 |
| T64 | `tests::sqlite_does_not_replay_idempotency_receipt_before_scope_check` | SC-07, SC-08, SC-02, SC-10, SC-12 | HIR-05, HIR-16, HIR-14 | 覆盖 memory/scope 边界下 replay 或 status 行为；不覆盖 H 完整 namespace 或 I/D replay disclosure 授权。 |
| T65 | `tests::sqlite_filters_nested_claims_by_the_callers_scope` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T66 | `tests::sqlite_hides_entire_multiscope_claim_from_partial_scope_reader` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T67 | `tests::sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup` | SC-08, SC-07, SC-02, SC-10, SC-12 | HIR-02, HIR-14, HIR-05, HIR-16 | 覆盖输入校验、摘要完整性或 scope fail-closed；不证明跨资源协调、权限 epoch 或所有投影重建。 |
| T68 | `tests::sqlite_multiple_preparations_reserve_unique_negative_sequences` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 CAS、prepare/publish 及本地可见性部分；未覆盖 Owner cursor/outbox/receipt 完整原子写集或已接受的 Storage contract。 |
| T69 | `tests::sqlite_prepare_does_not_add_change_log_entries` | SC-01, SC-03, SC-10 | HIR-06 | 覆盖 prepare 不发布/不变更 current pointer 的部分；缺 commit 完整 write set 与外部线性化读证据。 |
| T70 | `tests::sqlite_prepare_hides_version_from_read_version` | SC-02, SC-10, SC-12, SC-01, SC-03 | HIR-06 | 覆盖 prepare 不发布/不变更 current pointer 的部分；缺 commit 完整 write set 与外部线性化读证据。 |
| T71 | `tests::sqlite_prepare_keeps_current_version_unchanged` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 prepare 不发布/不变更 current pointer 的部分；缺 commit 完整 write set 与外部线性化读证据。 |
| T72 | `tests::sqlite_prepare_rejects_idempotency_digest_conflict` | SC-08 | HIR-02, HIR-14 | 覆盖 key/digest 重放或冲突的 Storage/producer 层行为；未证明 H 完整 namespace tuple、tombstone horizon 或 H ledger authority。 |
| T73 | `tests::sqlite_prepare_replay_returns_same_receipt` | SC-08, SC-07 | HIR-02, HIR-14, HIR-05, HIR-16 | 覆盖本地 receipt 持久化/重开/重放；未覆盖 H receipt 全字段、长期 tombstone 或跨资源 crash reconciliation。 |
| T74 | `tests::sqlite_publication_state_honours_scope_and_forget_fences` | SC-06, SC-10, SC-11, SC-12, SC-13, SC-02 | HIR-18 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T75 | `tests::sqlite_publication_state_reports_prepared_hidden_then_published` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T76 | `tests::sqlite_publication_state_returns_none_for_unknown_or_legacy_publication` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T77 | `tests::sqlite_publish_allocates_sequence_only_at_publish_time` | SC-01, SC-02, SC-03, SC-09, SC-10, SC-08 | HIR-06, HIR-14 | 覆盖发布/CAS/replay 部分；缺跨资源协调、H-owned receipt 和 replica read visibility。 |
| T78 | `tests::sqlite_publish_makes_prepared_version_current_and_readable` | SC-02, SC-10, SC-12, SC-01, SC-03, SC-08 | HIR-06, HIR-14 | 覆盖发布/CAS/replay 部分；缺跨资源协调、H-owned receipt 和 replica read visibility。 |
| T79 | `tests::sqlite_publish_rejects_duplicate_publication_and_suppressed_state` | SC-02, SC-10, SC-12, SC-01, SC-03, SC-08 | HIR-06, HIR-14 | 覆盖发布/CAS/replay 部分；缺跨资源协调、H-owned receipt 和 replica read visibility。 |
| T80 | `tests::sqlite_publish_rejects_stale_parent_without_partial_commit` | SC-02, SC-10, SC-12, SC-01, SC-03, SC-09, SC-08 | HIR-06, HIR-14 | 覆盖发布/CAS/replay 部分；缺跨资源协调、H-owned receipt 和 replica read visibility。 |
| T81 | `tests::sqlite_publish_replay_returns_original_receipt` | SC-08, SC-07, SC-01, SC-02, SC-03, SC-10 | HIR-02, HIR-14, HIR-05, HIR-16, HIR-06 | 覆盖发布/CAS/replay 部分；缺跨资源协调、H-owned receipt 和 replica read visibility。 |
| T82 | `tests::sqlite_read_version_keeps_legacy_versions_visible` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T83 | `tests::sqlite_rejects_claim_scope_outside_callers_scope_even_when_parent_contains_it` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T84 | `tests::sqlite_rejects_claims_outside_the_parent_memory_scope` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T85 | `tests::sqlite_rejects_create_outside_requested_scope` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T86 | `tests::sqlite_rejects_empty_idempotency_key_or_request_digest` | SC-08 | HIR-02, HIR-14 | 覆盖 key/digest 重放或冲突的 Storage/producer 层行为；未证明 H 完整 namespace tuple、tombstone horizon 或 H ledger authority。 |
| T87 | `tests::sqlite_rejects_invalid_memory_and_orphan_initial_version_pointer` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 CAS、prepare/publish 及本地可见性部分；未覆盖 Owner cursor/outbox/receipt 完整原子写集或已接受的 Storage contract。 |
| T88 | `tests::sqlite_rejects_invalid_version_fields_before_writing_any_commit_state` | 无对应测试 | 无对应测试 | 名称未对应到 SC/HIR 中某个完整谓词；无对应测试。 |
| T89 | `tests::sqlite_rejects_malformed_nested_claims_before_commit` | 无对应测试 | 无对应测试 | 名称未对应到 SC/HIR 中某个完整谓词；无对应测试。 |
| T90 | `tests::sqlite_rejects_mixed_parent_and_foreign_claim_scopes_before_commit` | SC-02, SC-10, SC-12, SC-07 | 无对应测试 | 覆盖输入校验、摘要完整性或 scope fail-closed；不证明跨资源协调、权限 epoch 或所有投影重建。 |
| T91 | `tests::sqlite_rejects_stale_expected_version` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 CAS、prepare/publish 及本地可见性部分；未覆盖 Owner cursor/outbox/receipt 完整原子写集或已接受的 Storage contract。 |
| T92 | `tests::sqlite_storage_entry_points_reject_empty_and_malformed_scope_sets` | SC-06, SC-10, SC-11, SC-12, SC-13, SC-02 | HIR-18 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T93 | `tests::startup_backfills_compile_intent_for_preexisting_accepted_events` | SC-01, SC-07, SC-15 | 无对应测试 | 覆盖 E compile-intent 数据/顺序/幂等/回填的局部实现；不证明 E admission 全写集原子性或 D canonical commit。 |
| T94 | `tests::status_and_replay_enforce_scope` | SC-02, SC-10, SC-12, SC-08 | HIR-14 | 覆盖 memory/scope 边界下 replay 或 status 行为；不覆盖 H 完整 namespace 或 I/D replay disclosure 授权。 |

## 5. AID-095 全部 72 个 Gate A 检查点重判

本次证据审查的判定词汇：
- **PASS**：具名测试完整覆盖检查点谓词才允许；本次没有任何一格满足。
- **PARTIAL_EVIDENCE**：测试覆盖一个或多个谓词组成部分，但仍缺 Owner、端到端关联、跨资源、副本、安全或运维组成部分。
- **UNCHANGED**：没有对应测试覆盖该检查点的核心谓词。

AID-095 的原始 Gate A 状态列在每一行都保持 `NOT EVIDENCED`。PARTIAL_EVIDENCE 只是证据注释，不是 PASS 或 Gate A 状态升级。

| 流程 | 检查点 | 原 Gate A 状态 | 证据判定 | 对应测试 | 为什么不能 PASS / 仍缺什么 |
|---|---|---|---|---|---|
| F1 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F1 | Request / response | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F1 | Identity / cursor namespace | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F1 | Idempotency scope | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::pending_compile_intents_returns_accepted_events_in_insertion_order`; `tests::same_producer_key_and_digest_replay_original_receipt` | 生产者 key/digest 重放与冲突有测试；缺 E producer namespace、scope-before-replay 全路径及 Owner admission 语义。 |
| F1 | Linearization point | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::pending_compile_intent_created_at_matches_the_acceptance_time`; `tests::pending_compile_intent_fails_closed_when_stored_payload_is_tampered_with`; `tests::pending_compile_intent_is_invisible_when_no_payload_was_stored` | 本地 acceptance/compile-intent 持久化有片段；缺 E Accepted + envelope + digest + compiler state + outbox 同一原子边界证明。 |
| F1 | Durable receipt | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable`; `tests::pending_compile_intent_created_at_matches_the_acceptance_time`; `tests::pending_compile_intents_returns_accepted_events_in_insertion_order` | SQLite receipt reopen/replay 有片段；缺 E-issued receipt 全字段及其与 Accepted 事务的绑定。 |
| F1 | Failure / Unknown | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F1 | Replay / recovery | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::pending_compile_intent_is_invisible_when_no_payload_was_stored`; `tests::pending_compile_intents_fails_closed_when_stored_bytes_are_tampered`; `tests::pending_compile_intents_is_empty_on_a_fresh_store`; `restart_preserves_receipt_and_idempotent_payload_replay` | 启动回填 compile intent、重开后 receipt replay 有片段；缺 E dispatcher/lease/DLQ/Unknown reconciliation。 |
| F1 | Visibility | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::pending_compile_intents_is_idempotent_and_does_not_consume`; `tests::same_producer_key_with_different_digest_conflicts` | 无 payload 时 compile intent 不可见等测试；缺 E/D canonical visibility 及全路径约束。 |
| F2 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F2 | Request / response | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F2 | Identity / cursor namespace | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F2 | Idempotency scope | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt`; `tests::pending_compile_intents_returns_accepted_events_in_insertion_order`; `tests::same_producer_key_and_digest_replay_original_receipt`; `tests::sqlite_multiple_preparations_reserve_unique_negative_sequences` | 同 key/digest replay/conflict 有测试；缺 D canonical operation namespace 与 F consumer dedupe join。 |
| F2 | Linearization point | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent`; `tests::file_db_nested_savepoint_rollback_preserves_outer_work`; `tests::sqlite_publication_state_reports_prepared_hidden_then_published`; `tests::sqlite_publish_rejects_stale_parent_without_partial_commit` | 本地 SQLite transaction/CAS/publish tests 覆盖局部 commit 边界；缺 D canonical cursor/outbox 的同一事务及 F consumption。 |
| F2 | Durable receipt | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable`; `tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt`; `tests::pending_compile_intent_created_at_matches_the_acceptance_time` | durable receipt/reopen/replay tests 覆盖局部 receipt；缺 D-issued cursor/receipt/outbox 完整链路。 |
| F2 | Failure / Unknown | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::abrupt_process_exit_rolls_back_entire_uncommitted_commit`; `tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent`; `tests::file_db_nested_savepoint_rollback_preserves_outer_work` | 事务回滚/中断 commit 有测试；缺 lost response 后 D/F Unknown 查询、reconcile 与无重复消费证明。 |
| F2 | Replay / recovery | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `committed_payload_survives_process_crash_and_wal_recovery`; `restart_preserves_receipt_and_idempotent_payload_replay`; `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable` | SQLite receipt replay/reopen 有测试；缺 D cursor 连续前缀、F consumer dedupe/ack/gap recovery。 |
| F2 | Visibility | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F3 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F3 | Request / response | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F3 | Identity / cursor namespace | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F3 | Idempotency scope | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F3 | Linearization point | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F3 | Durable receipt | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F3 | Failure / Unknown | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F3 | Replay / recovery | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F3 | Visibility | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F4 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F4 | Request / response | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F4 | Identity / cursor namespace | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `payload::tests::read_after_fails_closed_on_empty_persisted_scope_list`; `payload::tests::read_after_fails_closed_on_invalid_persisted_scope_ref`; `tests::f1_forget_memory_hides_current_and_history`; `tests::f7_forget_version_only_hides_that_version` | scope/fence identity tests 覆盖局部 namespace；缺 D operation+generation 与 E/F/G/H/I target ack 的完整身份链。 |
| F4 | Idempotency scope | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::f5_forget_memory_blocks_idempotency_replay`; `tests::f6_forget_is_idempotent` | forget idempotent 与 fence retry 有测试；缺跨 Owner operation+target+generation digest replay。 |
| F4 | Linearization point | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `crash_after_fence_commit_is_retried_without_resurrection`; `forget_fence::tests::crash_after_fence_commit_is_retried_safely_on_restore` | Fence commit 后 crash retry 测试覆盖局部线性化；缺 D 唯一 authority 到所有域的抑制线性化。 |
| F4 | Durable receipt | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F4 | Failure / Unknown | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `forget_fence::tests::malformed_scope_refuses_activation_without_partial_change`; `forget_fence::tests::missing_or_corrupt_fence_fails_closed`; `malformed_scope_refuses_activation_without_partial_change`; `missing_or_corrupt_fence_fails_closed` | malformed/missing/corrupt fence fail-closed 测试覆盖局部拒绝；缺 offline target、外部副本和 Unknown 全面关闭。 |
| F4 | Replay / recovery | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `crash_after_fence_commit_is_retried_without_resurrection`; `forget_fence::tests::crash_after_fence_commit_is_retried_safely_on_restore`; `forget_fence::tests::restore_anti_resurrection_purges_only_fenced_scope_across_all_tables`; `restore_anti_resurrection_and_preserves_other_scope` | Fence crash/reopen/anti-resurrection 有测试；缺所有 E/F/G/H/Storage projection 的 restore/replay。 |
| F4 | Visibility | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::f1_forget_memory_hides_current_and_history`; `tests::f10_forget_survives_reopen`; `tests::f2_forget_memory_excludes_from_change_pages`; `tests::f3_forget_memory_rejects_new_commit`; `tests::f4_forget_memory_rejects_prepare_and_publish`; `tests::f7_forget_version_only_hides_that_version`; `tests::f8_forget_version_blocks_child_commit`; `tests::f9_forget_memory_sets_lifecycle_state`; `tests::sqlite_filters_nested_claims_by_the_callers_scope`; `tests::sqlite_hides_entire_multiscope_claim_from_partial_scope_reader`; `tests::sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup`; `tests::sqlite_multiple_preparations_reserve_unique_negative_sequences`; `tests::sqlite_prepare_does_not_add_change_log_entries`; `tests::sqlite_prepare_hides_version_from_read_version`; `tests::sqlite_prepare_keeps_current_version_unchanged`; `tests::sqlite_prepare_rejects_idempotency_digest_conflict`; `tests::sqlite_prepare_replay_returns_same_receipt`; `tests::sqlite_publication_state_honours_scope_and_forget_fences`; `tests::sqlite_publication_state_reports_prepared_hidden_then_published`; `tests::sqlite_publication_state_returns_none_for_unknown_or_legacy_publication` | 本地 fence 对 read/change/prepare/publish 的隐藏有测试；缺全域读/发布、备份、缓存、replica 和 D-derived projection rebuild。 |
| F5 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F5 | Request / response | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F5 | Identity / cursor namespace | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F5 | Idempotency scope | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F5 | Linearization point | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F5 | Durable receipt | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F5 | Failure / Unknown | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F5 | Replay / recovery | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F5 | Visibility | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F6 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F6 | Request / response | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F6 | Identity / cursor namespace | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F6 | Idempotency scope | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F6 | Linearization point | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F6 | Durable receipt | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F6 | Failure / Unknown | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F6 | Replay / recovery | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F6 | Visibility | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F7 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F7 | Request / response | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F7 | Identity / cursor namespace | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F7 | Idempotency scope | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F7 | Linearization point | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F7 | Durable receipt | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F7 | Failure / Unknown | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F7 | Replay / recovery | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F7 | Visibility | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F8 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F8 | Request / response | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `failed_payload_insert_rolls_back_event_payload_and_outbox_rows`; `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable`; `tests::file_db_nested_savepoint_rollback_preserves_outer_work`; `tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt` | Storage SQLite APIs 的成功/冲突/拒绝行为有局部测试；缺 SC Durable Commit Receipt 完整字段与统一 participant request/response。 |
| F8 | Identity / cursor namespace | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F8 | Idempotency scope | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt`; `tests::pending_compile_intents_returns_accepted_events_in_insertion_order`; `tests::same_producer_key_and_digest_replay_original_receipt`; `tests::sqlite_multiple_preparations_reserve_unique_negative_sequences`; `tests::sqlite_publication_state_reports_prepared_hidden_then_published`; `tests::sqlite_publish_rejects_duplicate_publication_and_suppressed_state` | 同 key/digest replay/conflict 与 CAS 并发有测试；缺 GID+participant 语义和跨资源唯一 terminal result。 |
| F8 | Linearization point | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::abrupt_process_exit_rolls_back_entire_uncommitted_commit`; `tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent`; `tests::file_db_nested_savepoint_rollback_preserves_outer_work`; `tests::sqlite_publication_state_reports_prepared_hidden_then_published`; `tests::sqlite_publish_rejects_stale_parent_without_partial_commit` | SQLite transaction、CAS、prepare/publish 的本地 commit 边界有测试；缺 WAL durable flush/accepted COC terminal decision。 |
| F8 | Durable receipt | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `payload::tests::payload_append_receipt_and_ordered_read_survive_reopen`; `restart_preserves_receipt_and_idempotent_payload_replay`; `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable`; `tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt` | receipt append/reopen/replay 测试有覆盖；缺最小 SC-07 所有字段、COMMITTED/ABORTED/UNKNOWN 与 durability profile 读回。 |
| F8 | Failure / Unknown | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `failed_payload_insert_rolls_back_event_payload_and_outbox_rows`; `tests::abrupt_process_exit_rolls_back_entire_uncommitted_commit`; `tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent`; `tests::file_db_nested_savepoint_rollback_preserves_outer_work`; `tests::file_db_unwinding_worker_releases_open_transaction_without_partial_state` | 回滚、crash、interrupted commit 有覆盖；缺设备级 torn-write/flush、restore activation 和跨资源 Unknown resolution。 |
| F8 | Replay / recovery | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `committed_payload_survives_process_crash_and_wal_recovery`; `live_wal_copy_fails_closed_until_checkpointed`; `restart_preserves_receipt_and_idempotent_payload_replay`; `restore_anti_resurrection_and_preserves_other_scope`; `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable` | WAL reopen、receipt replay、Fence restore 有局部覆盖；缺完整 checkpoint contiguous log、跨资源 GID participant 和 RPO/RTO。 |
| F8 | Visibility | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `payload::tests::read_after_fails_closed_on_empty_persisted_scope_list`; `payload::tests::read_after_fails_closed_on_invalid_persisted_scope_ref`; `payload::tests::read_after_paginates_interleaved_scope_rows_by_visible_limit`; `payload::tests::read_after_skips_non_intersecting_scopes_and_limits_visible_rows`; `tests::sqlite_denies_fresh_cross_scope_write_without_persisting_any_commit_state`; `tests::sqlite_does_not_replay_idempotency_key_across_memories`; `tests::sqlite_filters_nested_claims_by_the_callers_scope`; `tests::sqlite_hides_entire_multiscope_claim_from_partial_scope_reader`; `tests::sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup`; `tests::sqlite_multiple_preparations_reserve_unique_negative_sequences`; `tests::sqlite_prepare_does_not_add_change_log_entries`; `tests::sqlite_prepare_hides_version_from_read_version`; `tests::sqlite_prepare_keeps_current_version_unchanged`; `tests::sqlite_prepare_rejects_idempotency_digest_conflict`; `tests::sqlite_prepare_replay_returns_same_receipt`; `tests::sqlite_publication_state_honours_scope_and_forget_fences`; `tests::sqlite_publication_state_reports_prepared_hidden_then_published`; `tests::sqlite_publication_state_returns_none_for_unknown_or_legacy_publication` | prepare hidden/publish visible、scope/fence read filtering 有覆盖；缺 replica applied position、I PermissionEpoch 与 restore-before-exposure 全路径。 |

## 6. Storage SC-04/05/06/10/12/13/17/18——八条 EVIDENCE_REQUIRED

| ID | 证据判定 | 触及谓词的测试 | 缺失部分 / 不能 PASS 的原因 |
|---|---|---|---|
| SC-04 | **PARTIAL_EVIDENCE** | live_wal_copy_fails_closed_until_checkpointed; committed_payload_survives_process_crash_and_wal_recovery; file_backed_connection_applies_required_sqlite_pragmas | 缺 backend profile 下的 log framing、log-before-data、commit marker 与真实 durable flush/device barrier 证据。 |
| SC-05 | **PARTIAL_EVIDENCE** | live_wal_copy_fails_closed_until_checkpointed; committed_payload_survives_process_crash_and_wal_recovery | 缺 checkpoint position/atomicity、连续有效 WAL 前缀重放及截断/缺口故障注入。 |
| SC-06 | **PARTIAL_EVIDENCE** | abrupt_process_exit_rolls_back_entire_uncommitted_commit; crash_after_fence_commit_is_retried_safely_on_restore; restore_anti_resurrection_purges_only_fenced_scope_across_all_tables; missing_or_corrupt_fence_fails_closed | 缺通用 torn/partial write、所有 crash cut、restore staged-image 原子激活证明。 |
| SC-10 | **PARTIAL_EVIDENCE** | sqlite_prepare_hides_version_from_read_version; sqlite_publication_state_reports_prepared_hidden_then_published; sqlite_publish_makes_prepared_version_current_and_readable; payload::tests::read_after_* | 缺每条权威读路径与 replica applied-position/current Fence 验证；SQLite 单库测试不能证明副本。 |
| SC-12 | **PARTIAL_EVIDENCE** | missing_or_corrupt_fence_fails_closed; malformed_scope_refuses_activation_without_partial_change; payload::tests::read_after_fails_closed_*; tests::f1_forget_memory_* | 缺 D authority 驱动的完整 projection rebuild 及所有读取/发布路径 fail-closed 证据。 |
| SC-13 | **PARTIAL_EVIDENCE** | restore_anti_resurrection_and_preserves_other_scope; forget_fence::tests::restore_anti_resurrection_purges_only_fenced_scope_across_all_tables; crash_after_fence_commit_is_retried_without_resurrection | 只覆盖 D Fence/anti-resurrection 局部路径；缺 I PermissionEpoch、独立 anti-rollback anchor 联动和备份 restore-before-exposure。 |
| SC-17 | **UNCHANGED** | 无对应测试 | 缺跨资源稳定 GID participant、durable prepare/vote/terminal records、单一已接受 coordinator terminal authority 与确定性恢复测试。 |
| SC-18 | **UNCHANGED** | 无对应测试 | 缺备份/副本回滚/failover 的重复 workload 证据、声明的 RPO/RTO 与生产拓扑演练。 |

**明确仍为 EVIDENCE_REQUIRED：**SC-17 没有跨资源 GID participant/已接受协调器测试；SC-18 没有可重复的备份、副本回滚、故障切换或 RPO/RTO workload 证据。SC-04/05/06/10/12/13 只有 SQLite 本地局部证据，未解除 EVIDENCE_REQUIRED 分类。

## 7. HIR-05/06/08/12/14/16/17/18——八条 EVIDENCE_REQUIRED

| ID | 证据判定 | 触及谓词的测试 | 缺失部分 / 不能 PASS 的原因 |
|---|---|---|---|
| HIR-05 | **PARTIAL_EVIDENCE** | payload_append_receipt_and_ordered_read_survive_reopen; restart_preserves_receipt_and_idempotent_payload_replay; concurrent_identical_idempotency_requests_replay_one_durable_receipt | 只覆盖 SQLite receipt durability/reopen；缺 H-owned durable reservation ledger、tombstone retention horizon 与 replay expiry policy 实测。 |
| HIR-06 | **PARTIAL_EVIDENCE** | file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent; sqlite_publish_rejects_stale_parent_without_partial_commit; failed_payload_insert_rolls_back_event_payload_and_outbox_rows | 覆盖 Storage CAS/idempotency/rollback 的局部写集；缺完整 AID-098 Owner write-set、outbox+receipt+cursor 全部同事务以及接受的 Owner mapping。 |
| HIR-08 | **PARTIAL_EVIDENCE** | concurrent_identical_idempotency_requests_replay_one_durable_receipt; independent_connections_serialize_conflicting_idempotency_payloads | 覆盖 SQLite 并发幂等竞争；缺 H-owned ledger 的 namespace 竞争、明确单一 H winner 和 H durable admission receipt。 |
| HIR-12 | **PARTIAL_EVIDENCE** | pending_compile_intents_is_idempotent_and_does_not_consume; pending_compile_intents_returns_accepted_events_in_insertion_order | 覆盖 E pending compile-intent 的幂等读取；缺 H Pending duplicate 返回同一 H receipt 且不触发第二次 logical execution。 |
| HIR-14 | **PARTIAL_EVIDENCE** | same_producer_key_and_digest_replay_original_receipt; same_producer_key_with_different_digest_conflicts; sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup | 覆盖 producer/storage key+digest replay/conflict；缺 H 完整 namespace tuple 下的同一键语义和 H-owned immutable receipt。 |
| HIR-16 | **PARTIAL_EVIDENCE** | committed_payload_survives_process_crash_and_wal_recovery; abrupt_process_exit_rolls_back_entire_uncommitted_commit; restart_preserves_receipt_and_idempotent_payload_replay | 覆盖 SQLite 单资源 crash/reopen/replay；缺 H 与 Storage commit 前后跨边界 reconciliation、同 GID 查询和无重复 domain effect。 |
| HIR-17 | **UNCHANGED** | 无对应测试 | 缺 H Attempt 与 C/G DeliveryAttempt 的 distinct-ID join、C evidence binding、G AppliedAttestation/Applied 独立决策的集成测试。 |
| HIR-18 | **PARTIAL_EVIDENCE** | forget_fence::tests::missing_or_corrupt_fence_fails_closed; tests::f1_forget_memory_hides_current_and_history; tests::f5_forget_memory_blocks_idempotency_replay; tests::f10_forget_survives_reopen | 仅覆盖 D Fence 侧 fail-closed；缺 I PermissionEpoch 当前授权重查、issuer/key status revalidation，以及 D/I anti-rollback anchor 联动。 |

**明确仍为 EVIDENCE_REQUIRED：**HIR-17 没有 H Attempt 到 C/G DeliveryAttempt 映射或 G Applied 证据。HIR-18 只有 D Fence 侧测试；I PermissionEpoch 与当前授权重查未测试。D/I anti-rollback anchor 联动也未测试。

## 8. Gate A 与 Gate B 结论

**Gate A：PARTIAL / OPEN——不变。**72 个 Gate A 单元中完整 PASS 谓词为零。SQLite 证据为部分单元增加了实现层证据，但没有完成任何八流程端到端谓词，也没有满足关闭 Gate A 所需的 Owner 验收与完整组合审查。

原有九项关闭清单保持：
1. main 同步与最终 PR Head 新鲜度——必须在最终 Head 核验。
2. 跨 Owner 角色处置——代理处置与自然人 Owner 验收必须区分。
3. 精确 Head CI——最终 PR Head 上 16 项必需上下文全部成功。
4. 完整八流程 A–I + Storage 组合包及相关 Owner 验收。
5. D/E/F/I 规范根 / IMPL2 处置及精确替代源 pin。
6. Storage 物理合同与完整 SC 证据，包括 SC-17/18。
7. H 幂等/重放与完整 HIR 证据，包括 HIR-17/18。
8. Canonical/EN/ZH-CN 全文语义与源版本 parity。
9. DEC-13 规范批准证据及任何未完成的自然人 Owner/联合验收。

**Gate B：PARTIAL / OPEN（NOT VERIFIED）——不变。**本地 SQLite 测试不能证明部署、生产一致性、分布式/多副本一致性、运维备份/故障切换或生产 RPO/RTO。

## 9. 明确未解决的实现谓词

- **SC-17：**没有稳定的跨资源 GID participant 集合、durable prepare/vote/terminal 记录、单一已接受 terminal-decision authority 或 participant replay/recovery。
- **SC-18：**没有备份/恢复、副本回滚、故障切换、可重复 RPO/RTO profile 或生产拓扑演练。
- **HIR-17：**没有 H Attempt 到 C/G DeliveryAttempt 关联；没有 G AppliedAttestation 或独立 Applied 决策测试。
- **HIR-18：**没有在 replay disclosure 前对 I PermissionEpoch 单调性/当前授权进行重查；D Fence 测试不能满足 I 侧谓词。
- **D/I anti-rollback：**没有 D Fence 与 I PermissionEpoch 在 restore 期间的独立 anchor 联动；没有跨两个 authority 的 pre-Fence/pre-revocation 备份复活测试。
- 两次本地测试均未声称为 CI 证据。

## 10. 非主张与约束

- 本次审查没有任何 PASS。
- `PARTIAL_EVIDENCE` 不会把任何 Gate A 状态提升为 PASS。
- 本证据记录 PR 未修改 runtime、validator 语义、schema、API、DDL、test、workflow、deployment 或生产配置。
- 不声称 Owner 验收或自然人签署。
- #1211 与 #1212 保持 OPEN；本记录不关闭任何 Issue。

## 11. 署名

user-authorized operator (delegated by account owner)；2026-11-26。仅记录委托证据，不伪造自然人 Owner 签署。
