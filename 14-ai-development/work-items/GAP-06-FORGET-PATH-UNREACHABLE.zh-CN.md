# GAP-06 — Forget fence 尚未接入 MemoryStore 读取门禁

**状态：** Open — 需要 engineering phase 架构裁定  
**领域：** GAP-06 / Memory 生命周期 / forget 语义  
**Owner 轨道：** Owner A（E2E Test Architecture）

## 缺口陈述

当前没有公开的 forget API 能把 `ForgetFence` 的 namespace fence 语义接到 `MemoryStore` 的读取门禁上，因此记录 fence 并不会阻止该 namespace 下的 Memory 被读取。

## 不可达证据

仓库 API 搜索命令：

```sh
grep -rn "pub fn.*forget" crates/memory-store/src/lib.rs crates/memory-storage/src/lib.rs
```

**结果：零命中。** Round 7 交接中 Owner 提供了这条精确命令及零命中结果，作为独立仓库核验；本文记录该证据，不冒称本会话重新执行了本地 shell 命令。

Event-store fence 是一套独立机制：`ForgetFence::record_forget(namespace_key, reason_digest)` 使用自己的数据库连接持久化 namespace fence。其 restore 操作只在恢复 event-store 表时应用 fence；它不会修改 Memory 记录，也不会被 `MemoryStorage::read_current` 或 `MemoryStore::read_current` 查询。

因此，当前负向路径测试保留一个被 ignore 的目标 forget E2E；另有一条反向测试固定当前可观察行为：即使记录了 fence，MemoryStore 仍然可以读取该 Memory。

## 2. fence 的当前读者

本轮执行的仓库搜索命令：

```sh
grep -RIn 'load_fences' crates/memory-event-store-sqlite crates/memory-store crates/memory-storage crates/memory-storage-sqlite
grep -RInE 'FROM[[:space:]]+forget_fence|INTO[[:space:]]+forget_fence|UPDATE[[:space:]]+forget_fence' crates/memory-event-store-sqlite crates/memory-store crates/memory-storage crates/memory-storage-sqlite
grep -RIn 'restore_backup' crates
```

Rust 生产代码的命中集中在 `crates/memory-event-store-sqlite/src/forget_fence.rs`：

- `record_forget` 会先执行 `SELECT fence_seq FROM forget_fence WHERE namespace_key=?1`，使重复写入具备幂等性；不存在时才插入记录。这是写入路径上的去重读取，不是 Memory 读取门禁。
- `open_existing` 调用 `load_fences` 检查现有 fence 数据库；它会读取并校验记录，但不会对 live Memory 读取实施门禁。
- `restore_backup` 调用 `load_fences`；后者执行 `SELECT namespace_key,fence_seq,reason_digest FROM forget_fence`。得到的 namespace 集合用于扫描备份中的 `accepted_events.scope_json`，并在激活恢复文件前，从 `accepted_events`、`event_payloads` 和 `compile_outbox` 清除匹配事件。

**结论：fence 有真实的执行读取者，但仅限 event-store 备份恢复路径。** `MemoryStore` 或 `MemoryStorage` 的正常读取路径没有读取 fence 表。因此缺口不只是某个 Store 方法少了一次调用：fence 根本尚未进入 Memory 读取边界。`tests/forget_fence.rs` 的五条集成测试覆盖恢复行为、校验/失败关闭、非法 scope、fence 提交后的重试和并发记录；它们并未证明 Memory 读取受 fence 约束。

Round 8 的行为探测器命名为 `forget_api_absence_is_detectable`。它故意断言记录 fence 后 Memory revision 仍可读取。按当前分离架构，该测试应保持绿色；Memory 读取门禁接入 fence 后，它必须转红。届时删除这条当前行为固定测试，并启用 `forgotten_memory_is_excluded_from_context`。

## 三个候选实现方向

### (a) 在 `MemoryStore` 增加 `forget(namespace_key, reason)`，内部转调 `ForgetFence`

调用者会获得直观的 Store 层操作，但 Store 必须协调 event-store fence 与 Memory storage。要保证正确性，需要共享连接或跨 crate 的事务/提交协议；否则 fence 可能已经提交，而 Memory 读取门禁仍然不知道它。该方案是跨 crate 改动，并带来非平凡的原子性和失败顺序问题。

### (b) 在 MemoryStorage 读取路径强制检查 fence

在 storage 读取边界返回当前 revision 前查询权威 namespace fence，并为所有其他读取路径定义同一规则。这样把强制执行放在真正返回数据的边界，而不是依赖每个调用者记得先调用 Store 层前置方法。代价是读取时增加 fence 查询，并要求 Memory store 与 fence writer 之间具有明确的共享数据库/schema 或等价的原子可见性契约。

### (c) 保持不可达，等待 engineering phase 裁定

不增加半成品 API，也不把 event-store restore 冒充为 Memory forget 操作。保留目标 E2E 的 ignore，并将此项明确登记为需要 engineering phase 裁定。后果是 ignored E2E 会长期存在；在裁定落地前，系统不提供 Memory 级 forget 保证。

## 推荐方案

**推荐 (b)：在 MemoryStorage 读取边界强制执行 fence。** 正确性属性是“被 fence 的 namespace 不能产出可读的 Memory revision”，因此检查应位于数据返回前的最后一个共同边界。只增加 Store 层方法可能被直接使用 Storage 的调用者或未来新增的读取入口绕过；读取边界不变量更难绕过，也提供了统一 fail-closed 位置。实现前必须先解决 Memory 数据库如何原子地观察 fence（共享 SQLite 数据库/连接，或明确定义的等价机制）；本 work item 不授权采用存在竞态窗口的临时第二数据库查询。

## 建议实现改动面（本 work item 尚未授权实施）

若获得实施授权，我会选择方向 (b)，由 storage adapter 强制执行读取不变量，而不是由调用方做先检查再读取：

1. 在 `crates/memory-store/src/lib.rs` 增加 `MemoryStore::forget_namespace(namespace_key, reason_digest)`。它校验非空参数并委托 storage port；自身不能实现“先检查、再读取”的两步流程。
2. 在 `crates/memory-storage/src/lib.rs` 的 `MemoryStorage` trait 增加持久化 namespace fence 的记录操作，并明确规定 `read_current` 和 `read_version` 都必须拒绝被 fence 的 namespace。`MemoryStore::read_current` 和 `read_revision` 已分别经由这两个 trait 方法读取。
3. 在 `crates/memory-storage-sqlite/src/lib.rs` 实现记录和强制检查：SQLite adapter 必须在 revision 读取的同一 storage 边界内作出 fence 判定，并定义事务/锁策略。禁止先单独查询一次、再无保护地读取。
4. 重构 `crates/memory-event-store-sqlite/src/forget_fence.rs`，暴露基于调用方连接/事务的记录和查询原语（例如 `record_forget_in` 与 `is_fenced_in`），同时保留 restore 调用方现有的路径 API。adapter 必须使用同一个权威 fence 状态，并提供原子可见性策略；仅增加一个内部另开连接的公开 `is_fenced` 不足以消除竞态。

主要改动文件预计为：`crates/memory-store/src/lib.rs`、`crates/memory-storage/src/lib.rs`、`crates/memory-storage-sqlite/src/lib.rs`、`crates/memory-event-store-sqlite/src/forget_fence.rs`，另需 adapter 和跨 crate 测试。这只是实施改动面说明，不构成实施授权。

## 关闭条件

只有以下条件全部满足，才能关闭本项：

1. 存在公开且有文档的契约，将持久化 namespace fence 与 MemoryStorage 读取连接起来，并定义 fence 状态缺失、损坏或不可用时的行为。
2. 所有可能返回 Memory revision 的公开读取路径都执行该契约；被 fence 的 namespace 不再返回可读 revision（或返回有类型的拒绝），绝不返回 fence 前的 revision。
3. 对 fence 记录与并发读取之间的原子性/可见性有明确设计，并在相关 storage adapter 边界具备测试。
4. 反向测试 `forget_api_absence_is_detectable` 改为断言已强制执行的行为，或由明确的替代回归测试取代；目标 E2E `forgotten_memory_is_excluded_from_context` 取消 ignore 并通过。
5. 相关 crate 测试和 workspace 验证在合并后的实现上通过。

在上述条件全部满足前，保持本 work item 开放，并保留两条测试作为当前契约与目标契约的可执行文档。
