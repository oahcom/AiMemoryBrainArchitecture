# Phase 1 SQLite Adapter 契约

状态：CANDIDATE 工程实现；不构成生产就绪证据。

## 范围

将 Phase 1 MemoryStorage Trait 实现到 SQLite，包括：
- 显式 Schema 初始化；
- 不可变 Version Row；
- Current-Version CAS；
- Idempotency Receipt 持久化；
- 单调 Commit Sequence；
- Version/Current Pointer/Commit Log/Idempotency 的原子事务；
- 带 Scope Filter 的读取与变更列表；
- 文件数据库使用 WAL Journal Mode、每连接 synchronous=FULL，以及 5 秒 Busy Timeout。

## 明确限制

本 Adapter 不实现 Event Store、Lifecycle Manager、Forget 擦除、分布式协调、Backup/PITR、多进程线性一致性证明、断电/介质损坏证明或生产部署拓扑。

Memory 和 MemoryVersion 的序列化只是工程表示。Claim 跨 MemoryVersion 身份仍保持 OPEN，本 Adapter 不偷偷关闭该决策。

## 事务模型

Writer 使用 SQLite Immediate Transaction。提交边界包括 Version Row、Current Pointer、Commit Log 和 Idempotency Receipt。事务失败必须回滚。

文件数据库连接启用 WAL 和 synchronous=FULL。内存数据库连接使用 synchronous=FULL，但保留 SQLite 内存 Journal 行为。每个连接均启用 foreign_keys=ON 和 5 秒 Busy Timeout。

## 验证

Rust Workspace CI 工作流 `.github/workflows/rust-phase1.yml` 执行 `cargo test --workspace --all-targets`。

SQLite Adapter 测试覆盖：
- 内存数据库 round-trip、幂等、stale-version 和 Scope 边界；
- 关闭连接并重新打开数据库后，已提交状态仍然存在，包括 Current Pointer、Idempotency Receipt 和 Change Sequence；
- 在同一个事务已写入 Version Row、Current Pointer、Commit Log 和 Idempotency Receipt、但尚未提交时，强制终止进程；重新打开数据库后，这些未提交的部分效果必须全部不可见。

强制进程退出测试验证的是当前受测本地文件系统/运行环境下，SQLite 对未提交事务的进程终止恢复能力。它不构成断电、内核崩溃、存储控制器缓存、介质损坏、Backup/Restore 或多进程线性一致性证明。

