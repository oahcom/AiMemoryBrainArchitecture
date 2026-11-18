# Phase 1 SQLite Adapter 契约

状态：DECIDED——仅限 Phase 1 SQLite 持久化边界，不构成生产就绪证据。

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

## 决策：Phase 1 持久化边界

针对已验证的本地文件型 SQLite 配置，作出 DECIDED 决策：
- 文件数据库连接启用 WAL、synchronous=FULL、foreign_keys=ON 和 5 秒 Busy Timeout。
- 已提交的 MemoryVersion 及其 Current Pointer、Idempotency Receipt、单调 Change Sequence，在关闭连接并重新打开数据库后仍然存在。
- 当独立子进程在同一个 Immediate Transaction 中写入 Version Row、Current Pointer、Commit Log 和 Idempotency Receipt、但尚未执行 COMMIT 就被终止时，重新打开数据库后不可见任何上述未提交效果。
- Version/Current Pointer/Commit Log/Idempotency 写入集合属于同一个原子事务边界。

证据：
- PR #242 已合入 main：Merge Commit `aa711289785395d2efa202e34def64c393ee0ac7`。
- 验证提交 `4a3e06fd263e9dbd1056179dceb3cb21b17e330f` 是 PR #242 合并提交的后代，包含 SQLite 持久化测试以及独立连接 CAS/幂等竞争测试。
- Rust Workspace CI：Run ID `44259233587`（Run #25），Job `rust-workspace-test`，执行 `cargo test --workspace --all-targets`——SUCCESS。
- GOV-DOC-001：Run ID `44259233358`（Run #405），Job `GOV-DOC-001 structural checks`——SUCCESS。

## 明确限制

本决策仅覆盖 Phase 1 行为及 GitHub Actions 所测本地文件系统/运行环境，不构成以下能力证明：
- 断电、内核崩溃、存储控制器缓存、介质损坏或 Backup/Restore 恢复；
- 跨进程或多主机线性一致性、分布式协调或生产部署拓扑；
- 生产就绪或生产级持久性 SLO。

独立连接 CAS 和幂等竞争测试是在同一进程内使用不同 SQLite Connection 实例完成的测试。其范围及后续跟踪由 PR #244 单独承载；这些测试不扩大本决策的范围，也不构成跨进程并发结论。

Memory 和 MemoryVersion 的序列化只是工程表示。Claim 跨 MemoryVersion 身份仍保持 OPEN，本 Adapter 不偷偷关闭该决策。

## 事务模型

Writer 使用 SQLite Immediate Transaction。提交边界包括 Version Row、Current Pointer、Commit Log 和 Idempotency Receipt。失败或未提交的事务必须回滚。

文件数据库连接启用 WAL 和 synchronous=FULL。内存数据库连接使用 synchronous=FULL，但保留 SQLite 内存 Journal 行为。每个连接均启用 foreign_keys=ON 和 5 秒 Busy Timeout。

## 验证清单

Rust Workspace CI 工作流 `.github/workflows/rust-phase1.yml` 执行 `cargo test --workspace --all-targets`。

SQLite Adapter 测试覆盖：
- 内存数据库 round-trip、幂等、stale-version 和 Scope 边界；
- 关闭连接并重新打开数据库后，已提交状态仍然存在，包括 Current Pointer、Idempotency Receipt 和 Change Sequence；
- 两个独立 SQLite 连接并发提交同一 Expected Current Version 时，CAS 只允许一个写入成功，另一个得到 StaleVersion；
- 两个独立 SQLite 连接并发提交完全相同的 Idempotency Key/Digest/请求时，两者返回同一个持久化 Receipt，且只产生一条 Change Record；
- 在同一个事务已写入 Version Row、Current Pointer、Commit Log 和 Idempotency Receipt、但尚未提交时，强制终止进程；重新打开数据库后，这些未提交的部分效果必须全部不可见。

双连接竞争测试验证的是同一进程内两个独立 SQLite Connection 的写入串行化和幂等重放，不构成跨进程/多主机线性一致性证明。

强制进程退出测试验证的是当前受测本地文件系统/运行环境下，SQLite 对未提交事务的进程终止恢复能力。它不构成断电、内核崩溃、存储控制器缓存、介质损坏、Backup/Restore 或多进程线性一致性证明。
