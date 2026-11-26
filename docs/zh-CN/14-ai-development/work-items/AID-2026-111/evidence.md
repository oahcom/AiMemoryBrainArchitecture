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
      last_verification_note: "运行记录是固定提交上的本地 Linux 捕获；raw stdout 哈希仅标识本次捕获，可复现指纹使用文档定义的 exit/count/harness 多重集算法。谓词来自精确 main blob。未声称 CI、current main、生产、分布式后端或 Owner 验收。"
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-111/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-111/evidence.md"
    zh-CN: null
---

# AID-2026-111 — SQLite 后端实现证据映射与谓词重判

- Work item：`AID-2026-111`；`id_status: PROVISIONAL`。
- **编号重分配 / RENUMBERED_FROM：**最初临时编号 AID-2026-109 与 main 上另一工作项冲突；AID-2026-110 已由 PR #1304 预留（且曾由 #1287 使用）。因此本工作项改为 AID-2026-111。PR #1303 已未合并关闭；其分支仅作来源记录。
- 署名：**user-authorized operator (delegated by account owner)**；日期：**2026-11-26**。仅为委托代理记录，不代表自然人 Owner 签署。
- 取号基线：main `a7e7c64bfd6c6d709a0a7b55358f94b8535815c1`；INDEX 最大编号为 AID-2026-108；分配时 AID-2026-111 不存在于 INDEX/tree、Issue 搜索和分支名中。新分支从该精确 main 创建。
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
| stdout SHA-256 | `a15e3862af4d6cd97a4cd8caf6f133f57e3c3636ba284bdfd5afaa9237ba2952` (this capture only) |
| Normalised digest | `92c368733aa89e426d1508a55584a5a4b8f0cc4f9b91aab6723820f6260ca086` |
| 测试名恢复情况 | recovered **94 of 99** passed tests（尽力恢复；libtest 输出交错可能吞掉 `... ok` 后缀） |

**Raw 输出稳定性：**同一提交、同一命令连续执行 5 次，得到 5 个不同的 raw stdout SHA-256。原因包括 libtest 并行完成顺序、时长行、构建耗时，以及 SQLite 子进程继承 stdout 后的输出交错。因此上面的 raw SHA-256 仅标识本次捕获，不是可复现常量。

**Harness 计数（权威）：**按完整 `test result:` 行求和，并剔除 `filtered out > 0` 的子进程行：`26 + 5 + 2 + 6 + 60 = 99`。不得直接数 `test ... ok` 行。测试名清单仅为 best-effort；以 harness 计数为准，不以名字清单为准。

### 2.2 纯 Rust 层——补充的用户执行记录

- 环境：WSL2 Ubuntu 24.04；rustup stable 1.100.0。
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
| stdout SHA-256 | `C18EF5FC121EEB9B486000180F52BAE8385385722A369ADDAB873FCF8716D7B9` (this capture only) |
| Normalised digest | `73d97ed8f536aa06cf483f84e750ddbda610d56e8f5caee501fac6f198934eee` |

该运行补充纯 Rust 领域/协议/Storage trait 证据。它运行于另一个固定提交（`44dc21a4…`），SQLite 与 memory-context 则运行于 `a123ea4e…`；不得将三组描述为同一提交。所给 normalised digest 按 exit code + passed/failed 总数 + 各 harness passed 数多重集排序后计算，不含顺序、时长和进程交错。测试名恢复情况：本证据记录中 **recovered 0 of 276**（未提供清单）；计数以 harness 为准。

### 2.3 Memory-context 组——用户提供的本地汇总执行证据

- 环境：WSL2 Ubuntu 24.04。
- 精确 HEAD：`a123ea4e414c9f74fa0c576fbd718049a7d9f917`（与 SQLite 组相同的固定提交）。
- Passed / failed：**177 / 0**。
- 精确命令、测试二进制数、stdout 字节数、raw stdout SHA-256、各 harness passed 多重集及测试名清单：**所给证据未记录**。
- Normalised digest：**未提供**；仅凭汇总的 `177 passed` 无法推算。

这是固定提交上的本地 Linux 执行，不是 CI，也不是 current `main`。测试名恢复情况：本证据记录中 **recovered 0 of 177**（未提供清单）；测试名清单属于 best-effort，不推断未提供的测试名覆盖。

**Normalised digest 算法（可复现指纹）：**对 `exit code + passed/failed 总数 + 各 harness 块 passed 数多重集排序后` 计算 SHA-256。不包含测试顺序、时长、构建耗时和进程交错。上面的 SQLite 与 pure Rust digest 使用该算法；memory-context 未提供 digest。\n\n### 2.4 明确的负面构建证据

Windows 主机上的 `cargo test --workspace` 因 `libsqlite3-sys v0.40.0` build script 无法执行 `cc1`（`gcc.exe: fatal error: cannot execute 'cc1'`）而 exit **101**；MSVC 同样缺少 `cl.exe`/`link.exe`。因此该 Windows 主机无法构建：`memory-storage-sqlite`、`memory-event-store-sqlite`、`memory-store`、`memory-compiler`、`memory-context`、`brain-cli`。

| 字段 | 记录值 |
|---|---|
| Exit code | **101** |
| stdout 字节数 | 12456 |
| stdout SHA-256 | `93BCDC26AB0B29CEDBEC56DD11BB735C8050DB18366A3F296B45C699C072C2B2` (this capture only) |

这是 Windows 主机工具链限制，不代表代码或测试失败。因此 SQLite 后端证据是在 WSL2 Linux 上产出，而不是 Windows 本机。

## 3. 证据边界——所有 PARTIAL_EVIDENCE 必须保留的限定

三组正向测试均为**固定提交上的本地 Linux 执行**（SQLite 99 与 memory-context 177 位于 `a123ea4e`；pure Rust 276 位于 `44dc21a4`）。它们**不是 CI**，也**不是 current main 上的运行**，不能证明分布式后端、多副本线性化或生产拓扑。SQLite 组具体使用 bundled SQLite。它不证明设备/控制器/文件系统断电语义、生产备份/故障切换 RPO/RTO、独立跨资源协调器验收或 Owner 验收。进程崩溃测试通过不自动等同于物理断电持久性。引用结果时必须分别保留各组自己的精确 HEAD，以及已记录的命令。Raw stdout SHA-256 仅标识本次捕获；跨次可复现比较应使用 normalised digest。

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
| T40 | `tests::file_backed_connection_applies_required_sqlite_pragmas` | SC-04 | 无对应测试 | 仅证明 SQLite pragma 被应用，不证明底层设备 flush、WAL commit marker 或 durable ordering。 |
| T41 | `tests::file_db_busy_timeout_bounds_wait_for_long_immediate_transaction` | SC-09 | 无对应测试 | 只证明本地 busy timeout 等待上界，不构成完整隔离 profile 或跨节点线性化证据。 |
| T42 | `tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent` | SC-01, SC-02, SC-06, SC-08 | HIR-06, HIR-16 | 覆盖单资源 interrupted-commit 后 pointer/log/idempotency 一致性；缺完整 Owner write-set 与 H↔Storage 跨边界恢复。 |
| T43 | `tests::file_db_nested_savepoint_rollback_preserves_outer_work` | SC-02 | 无对应测试 | 覆盖单资源 savepoint rollback 保留外层事务；不证明 crash/WAL 或 H protocol 谓词。 |
| T44 | `tests::file_db_unwinding_worker_releases_open_transaction_without_partial_state` | SC-02, SC-06 | HIR-16 | 覆盖本地 unwind 时事务释放/无部分状态；不证明完整 crash-cut、H recovery 或跨资源 reconciliation。 |
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
| T63 | `tests::sqlite_does_not_replay_idempotency_key_across_memories` | SC-08 | HIR-14 | 覆盖 key 不跨 memory scope 重放；缺 H 完整 namespace tuple 与 H-owned receipt。 |
| T64 | `tests::sqlite_does_not_replay_idempotency_receipt_before_scope_check` | SC-07, SC-08, SC-02, SC-10, SC-12 | HIR-05, HIR-16, HIR-14 | 覆盖 memory/scope 边界下 replay 或 status 行为；不覆盖 H 完整 namespace 或 I/D replay disclosure 授权。 |
| T65 | `tests::sqlite_filters_nested_claims_by_the_callers_scope` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T66 | `tests::sqlite_hides_entire_multiscope_claim_from_partial_scope_reader` | SC-02, SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T67 | `tests::sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup` | SC-02, SC-07, SC-08 | HIR-14 | 覆盖 digest mismatch 对 commit/receipt lookup 冲突；缺 H 完整 namespace tuple 与 H-owned immutable receipt。 |
| T68 | `tests::sqlite_multiple_preparations_reserve_unique_negative_sequences` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 CAS、prepare/publish 及本地可见性部分；未覆盖 Owner cursor/outbox/receipt 完整原子写集或已接受的 Storage contract。 |
| T69 | `tests::sqlite_prepare_does_not_add_change_log_entries` | SC-01, SC-03, SC-10 | HIR-06 | 覆盖 prepare 不发布/不变更 current pointer 的部分；缺 commit 完整 write set 与外部线性化读证据。 |
| T70 | `tests::sqlite_prepare_hides_version_from_read_version` | SC-02, SC-10, SC-12, SC-01, SC-03 | HIR-06 | 覆盖 prepare 不发布/不变更 current pointer 的部分；缺 commit 完整 write set 与外部线性化读证据。 |
| T71 | `tests::sqlite_prepare_keeps_current_version_unchanged` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 prepare 不发布/不变更 current pointer 的部分；缺 commit 完整 write set 与外部线性化读证据。 |
| T72 | `tests::sqlite_prepare_rejects_idempotency_digest_conflict` | SC-08 | HIR-02, HIR-14 | 覆盖 key/digest 重放或冲突的 Storage/producer 层行为；未证明 H 完整 namespace tuple、tombstone horizon 或 H ledger authority。 |
| T73 | `tests::sqlite_prepare_replay_returns_same_receipt` | SC-08, SC-07 | HIR-02, HIR-14, HIR-05, HIR-16 | 覆盖本地 receipt 持久化/重开/重放；未覆盖 H receipt 全字段、长期 tombstone 或跨资源 crash reconciliation。 |
| T74 | `tests::sqlite_publication_state_honours_scope_and_forget_fences` | SC-06, SC-10, SC-11, SC-12, SC-13, SC-02 | HIR-18 | 覆盖本地 scope/read/prepare/publish/visibility 或 fail-closed 片段；未证明所有权威读取路径、replica applied position 或跨域 Fence/PermissionEpoch。 |
| T75 | `tests::sqlite_publication_state_reports_prepared_hidden_then_published` | SC-10, SC-12 | 无对应测试 | 覆盖本地 prepared-hidden/published visibility；缺副本 applied position 与 D/I 全域 currentness。 |
| T76 | `tests::sqlite_publication_state_returns_none_for_unknown_or_legacy_publication` | SC-10, SC-12 | 无对应测试 | 覆盖未知/legacy publication 的本地读行为；缺全权威读路径及副本可见性证明。 |
| T77 | `tests::sqlite_publish_allocates_sequence_only_at_publish_time` | SC-01, SC-02, SC-03, SC-09, SC-10, SC-08 | HIR-06, HIR-14 | 覆盖发布/CAS/replay 部分；缺跨资源协调、H-owned receipt 和 replica read visibility。 |
| T78 | `tests::sqlite_publish_makes_prepared_version_current_and_readable` | SC-02, SC-10, SC-12, SC-01, SC-03, SC-08 | HIR-06, HIR-14 | 覆盖发布/CAS/replay 部分；缺跨资源协调、H-owned receipt 和 replica read visibility。 |
| T79 | `tests::sqlite_publish_rejects_duplicate_publication_and_suppressed_state` | SC-02, SC-10, SC-12, SC-01, SC-03, SC-08 | HIR-06, HIR-14 | 覆盖发布/CAS/replay 部分；缺跨资源协调、H-owned receipt 和 replica read visibility。 |
| T80 | `tests::sqlite_publish_rejects_stale_parent_without_partial_commit` | SC-02, SC-10, SC-12, SC-01, SC-03, SC-09, SC-08 | HIR-06, HIR-14 | 覆盖发布/CAS/replay 部分；缺跨资源协调、H-owned receipt 和 replica read visibility。 |
| T81 | `tests::sqlite_publish_replay_returns_original_receipt` | SC-08, SC-07, SC-01, SC-02, SC-03, SC-10 | HIR-02, HIR-14, HIR-05, HIR-16, HIR-06 | 覆盖发布/CAS/replay 部分；缺跨资源协调、H-owned receipt 和 replica read visibility。 |
| T82 | `tests::sqlite_read_version_keeps_legacy_versions_visible` | SC-10 | 无对应测试 | 仅覆盖本地 legacy-version read visibility；不证明 post-commit replica visibility。 |
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
| F1 | Idempotency scope | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::same_producer_key_and_digest_replay_original_receipt`; `tests::same_producer_key_with_different_digest_conflicts` | 生产者 key/digest 重放与冲突有测试；缺 E producer namespace、scope-before-replay 全路径及 Owner admission 语义。 |
| F1 | Linearization point | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::pending_compile_intent_carries_the_payload_and_envelope_a_compiler_needs`; `tests::pending_compile_intent_created_at_matches_the_acceptance_time`; `tests::startup_backfills_compile_intent_for_preexisting_accepted_events` | 本地 acceptance/compile-intent 持久化有片段；缺 E Accepted + envelope + digest + compiler state + outbox 同一原子边界证明。 |
| F1 | Durable receipt | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable`; `payload::tests::payload_append_receipt_and_ordered_read_survive_reopen`; `tests::same_producer_key_and_digest_replay_original_receipt` | SQLite receipt reopen/replay 有片段；缺 E-issued receipt 全字段及其与 Accepted 事务的绑定。 |
| F1 | Failure / Unknown | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F1 | Replay / recovery | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::startup_backfills_compile_intent_for_preexisting_accepted_events`; `restart_preserves_receipt_and_idempotent_payload_replay`; `committed_payload_survives_process_crash_and_wal_recovery` | 启动回填 compile intent、重开后 receipt replay 有片段；缺 E dispatcher/lease/DLQ/Unknown reconciliation。 |
| F1 | Visibility | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::pending_compile_intent_is_invisible_when_no_payload_was_stored`; `tests::pending_compile_intents_is_empty_on_a_fresh_store` | 无 payload 时 compile intent 不可见等测试；缺 E/D canonical visibility 及全路径约束。 |
| F2 | Issuer | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F2 | Request / response | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F2 | Identity / cursor namespace | NOT EVIDENCED | **UNCHANGED** | 无对应测试 | 94 个测试中没有覆盖此检查点的核心谓词；缺少该 Owner 的端到端契约/执行证据（见缺口清单），不得以相邻 SQLite 行为代替。 |
| F2 | Idempotency scope | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt`; `tests::same_producer_key_and_digest_replay_original_receipt`; `tests::same_producer_key_with_different_digest_conflicts`; `tests::sqlite_prepare_rejects_idempotency_digest_conflict` | 同 key/digest replay/conflict 有测试；缺 D canonical operation namespace 与 F consumer dedupe join。 |
| F2 | Linearization point | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent`; `tests::sqlite_publish_allocates_sequence_only_at_publish_time`; `tests::sqlite_publish_rejects_stale_parent_without_partial_commit` | 本地 SQLite transaction/CAS/publish tests 覆盖局部 commit 边界；缺 D canonical cursor/outbox 的同一事务及 F consumption。 |
| F2 | Durable receipt | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::acceptance_persists_across_reopen_and_receipt_replay_is_stable`; `tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt`; `payload::tests::payload_append_receipt_and_ordered_read_survive_reopen` | durable receipt/reopen/replay tests 覆盖局部 receipt；缺 D-issued cursor/receipt/outbox 完整链路。 |
| F2 | Failure / Unknown | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::abrupt_process_exit_rolls_back_entire_uncommitted_commit`; `tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent`; `tests::file_db_unwinding_worker_releases_open_transaction_without_partial_state` | 事务回滚/中断 commit 有测试；缺 lost response 后 D/F Unknown 查询、reconcile 与无重复消费证明。 |
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
| F8 | Idempotency scope | NOT EVIDENCED | **PARTIAL_EVIDENCE** | `tests::concurrent_identical_idempotency_requests_replay_one_durable_receipt`; `tests::same_producer_key_and_digest_replay_original_receipt`; `tests::same_producer_key_with_different_digest_conflicts`; `tests::sqlite_prepare_rejects_idempotency_digest_conflict`; `tests::sqlite_prepare_replay_returns_same_receipt`; `tests::sqlite_publish_replay_returns_original_receipt` | 同 key/digest replay/conflict 与 CAS 并发有测试；缺 GID+participant 语义和跨资源唯一 terminal result。 |
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

## 7. HIR-05/06/08/12/14/16/17/18——八条 EVIDENCE_REQUIRED

| ID | 证据判定 | 触及谓词的测试 | 缺失部分 / 不能 PASS 的原因 |
|---|---|---|---|
| HIR-05 | **UNCHANGED** | 无对应测试 | 缺 H-owned durable reservation ledger、tombstone retention horizon 与 replay expiry policy；SQLite Storage receipt 不是 H reservation。 |
| HIR-06 | **PARTIAL_EVIDENCE** | file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent; sqlite_publish_rejects_stale_parent_without_partial_commit; failed_payload_insert_rolls_back_event_payload_and_outbox_rows | 覆盖 Storage CAS/idempotency/rollback 局部写集；缺完整 AID-098 Owner write-set、outbox+receipt+cursor 同事务及 Owner 接受的映射。 |
| HIR-08 | **PARTIAL_EVIDENCE** | concurrent_identical_idempotency_requests_replay_one_durable_receipt; independent_connections_serialize_conflicting_idempotency_payloads | 覆盖 SQLite 并发幂等竞争；缺 H-owned ledger namespace 竞争、明确 H winner 与 H durable admission receipt。 |
| HIR-12 | **UNCHANGED** | 无对应测试 | 缺 H Pending duplicate 返回同一 H receipt 且不触发第二次 logical execution；E compile-intent pending 测试不是 H protocol ledger。 |
| HIR-14 | **PARTIAL_EVIDENCE** | same_producer_key_and_digest_replay_original_receipt; same_producer_key_with_different_digest_conflicts; sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup | 覆盖 producer/storage key+digest replay/conflict；缺 H 完整 namespace tuple 下同键语义与 H-owned immutable receipt。 |
| HIR-16 | **PARTIAL_EVIDENCE** | committed_payload_survives_process_crash_and_wal_recovery; abrupt_process_exit_rolls_back_entire_uncommitted_commit; restart_preserves_receipt_and_idempotent_payload_replay | 覆盖 SQLite 单资源 crash/reopen/replay；缺 H 与 Storage commit 前后跨边界 reconciliation、同 GID 查询和无重复 domain effect。 |
| HIR-17 | **UNCHANGED** | 无对应测试 | 缺 H Attempt 与 distinct C/G DeliveryAttempt join、C evidence binding、G AppliedAttestation/Applied 独立决策集成测试。 |
| HIR-18 | **PARTIAL_EVIDENCE** | forget_fence::tests::missing_or_corrupt_fence_fails_closed; tests::f1_forget_memory_hides_current_and_history; tests::f5_forget_memory_blocks_idempotency_replay; tests::f10_forget_survives_reopen | 仅覆盖 D Fence 侧 fail-closed；缺 I PermissionEpoch 当前授权重查、issuer/key status revalidation，以及 D/I anti-rollback anchor 联动。 |

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


### 8.1 从当前 AID-2026-107 延续的 IMPL2 范围裁决

当前 main 上 AID-2026-107 的证据 blob `cce956d97b7a6d969bb3245fe0890905ca6d3979` 记录了 03/04/05/09 Owner 源目录的逐文件处置：缺失的 189 个 Canonical 路径分类为 **5 个 NORMATIVE_ROOT**、**83 个 HISTORICAL_PHASE_RECORD** 和 **101 个 UNDECIDED**。AID-095 的 72 行矩阵部分与本次起草时使用的早期 AID-107 evidence blob 字节完全一致。

因此 Gate A 第 5 项已从无边界的恢复请求变为可执行事项：
- **5 个 NORMATIVE_ROOT** 是单独 Owner 审查恢复 PR 的候选文件；本证据 PR 不恢复这些文件。
- **83 个 HISTORICAL_PHASE_RECORD** 和 **101 个 UNDECIDED** 在没有明确 Owner 裁决前均不得进入 main。没有 Owner 裁决即不得合并这两类文件。
- F 和 I 的规范根缺口仍明确存在：F runtime 根与 I security 根文件仍需 Owner 指认，或明确决定替代源；不得默默用候选 overview 文件替代。
- 这些分类不代表批准、冻结、实现或符合性。

**Gate A 第 5 项：OPEN — 范围已裁决；5 个已识别根文件需由单独 PR 恢复；F/I 源根仍需 Owner 指认或明确替代决定。**

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

user-authorized operator (delegated by account owner)；2026-11-26。仅记录委托证据，不伪造自然人 Owner 签署。| Test | Exact test name | SC predicates touched | HIR predicates touched | Mapping boundary |
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
| T40 | `tests::file_backed_connection_applies_required_sqlite_pragmas` | 无对应测试 | 无对应测试 | 辅助 worker 名称或未覆盖的语义；无对应测试。 |
| T41 | `tests::file_db_busy_timeout_bounds_wait_for_long_immediate_transaction` | SC-09 | 无对应测试 | 只证明 SQLite busy timeout 等待上界，不证明完整隔离 profile 或跨节点线性化。 |
| T42 | `tests::file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent` | SC-01, SC-02, SC-06 | HIR-06, HIR-16 | 覆盖单资源事务回滚/崩溃切面；缺完整 Owner write-set、H↔Storage 协调和物理断电语义。 |
| T43 | `tests::file_db_nested_savepoint_rollback_preserves_outer_work` | SC-02 | 无对应测试 | 只覆盖单资源 savepoint rollback；不覆盖 WAL crash cut 或完整跨表原子写集。 |
| T44 | `tests::file_db_unwinding_worker_releases_open_transaction_without_partial_state` | SC-01, SC-02, SC-06 | HIR-06, HIR-16 | 覆盖单资源事务回滚/崩溃切面；缺完整 Owner write-set、H↔Storage 协调和物理断电语义。 |
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
| T63 | `tests::sqlite_does_not_replay_idempotency_key_across_memories` | 无对应测试 | 无对应测试 | 辅助 worker 名称或未覆盖的语义；无对应测试。 |
| T64 | `tests::sqlite_does_not_replay_idempotency_receipt_before_scope_check` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T65 | `tests::sqlite_filters_nested_claims_by_the_callers_scope` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T66 | `tests::sqlite_hides_entire_multiscope_claim_from_partial_scope_reader` | SC-10, SC-12 | 无对应测试 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T67 | `tests::sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup` | 无对应测试 | 无对应测试 | 辅助 worker 名称或未覆盖的语义；无对应测试。 |
| T68 | `tests::sqlite_multiple_preparations_reserve_unique_negative_sequences` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T69 | `tests::sqlite_prepare_does_not_add_change_log_entries` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T70 | `tests::sqlite_prepare_hides_version_from_read_version` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T71 | `tests::sqlite_prepare_keeps_current_version_unchanged` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T72 | `tests::sqlite_prepare_rejects_idempotency_digest_conflict` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T73 | `tests::sqlite_prepare_replay_returns_same_receipt` | SC-07, SC-08, SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-14, HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T74 | `tests::sqlite_publication_state_honours_scope_and_forget_fences` | SC-06, SC-10, SC-11, SC-12, SC-13 | HIR-18 | 覆盖本地 scope/read/change-page fail-closed；缺全权威读路径、replica applied position、D/I currentness。 |
| T75 | `tests::sqlite_publication_state_reports_prepared_hidden_then_published` | 无对应测试 | 无对应测试 | 辅助 worker 名称或未覆盖的语义；无对应测试。 |
| T76 | `tests::sqlite_publication_state_returns_none_for_unknown_or_legacy_publication` | 无对应测试 | 无对应测试 | 辅助 worker 名称或未覆盖的语义；无对应测试。 |
| T77 | `tests::sqlite_publish_allocates_sequence_only_at_publish_time` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T78 | `tests::sqlite_publish_makes_prepared_version_current_and_readable` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T79 | `tests::sqlite_publish_rejects_duplicate_publication_and_suppressed_state` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T80 | `tests::sqlite_publish_rejects_stale_parent_without_partial_commit` | SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T81 | `tests::sqlite_publish_replay_returns_original_receipt` | SC-07, SC-08, SC-01, SC-02, SC-03, SC-09, SC-10 | HIR-14, HIR-06 | 覆盖 SQLite prepare/publish/CAS 部分；缺完整 Owner write-set、H ledger 及外部/副本可见性。 |
| T82 | `tests::sqlite_read_version_keeps_legacy_versions_visible` | 无对应测试 | 无对应测试 | 辅助 worker 名称或未覆盖的语义；无对应测试。 |
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

## Session role / use case

本轮担任 AID-2026-111 SQLite 实现测试证据的文档作者与证据裁决者。工作限于读取精确源谓词、映射用户提供的测试名称并记录受限的证据分类。未修改 runtime、validator、schema、test、workflow、deployment 或 production。

## Actual AI input

NOT_RECORDED

原始用户消息未逐字保存为仓库文件。已提交的 `prompt-v1.md` 是结构化任务快照，不是完整用户消息的逐字节副本。94 个测试名称及用户提供的执行元数据保存在本证据记录中。

## AI-visible output

创建了本 Canonical 证据记录及 EN、ZH-CN 镜像；将 94 个具名测试映射到 SC/HIR 谓词；重判 72 个 Gate A 单元及 16 条 EVIDENCE_REQUIRED。88 行合计为 0 PASS、34 PARTIAL_EVIDENCE、54 UNCHANGED。Gate A 仍为 PARTIAL / OPEN；Gate B 仍为 PARTIAL / OPEN（NOT VERIFIED）。本记录列明本地运行边界，以及 SC-17/18、HIR-05/12/17/18 和 D/I anti-rollback 未解决缺口。
