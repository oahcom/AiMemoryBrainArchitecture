# REQ-10 SQLite commit-path benchmark

## Measured path

The repository's executable reference adapter is `crates/memory-storage-sqlite/src/lib.rs`, implementation `SqliteMemoryStorage::commit_version`. The Rust example in this crate calls that exact method. It measures one sequential writer, one memory, empty-claim versions, SQLite WAL mode and synchronous=FULL.

Each write traverses the adapter's scope validation, JSON encoding, IMMEDIATE transaction, memory/current-version lookup, idempotency lookup, parent-version check, sequence allocation, version insert, memory update, commit-log insert, idempotency receipt insert and transaction commit.

## Rust harness (authoritative)

From repository root:

```sh
cargo run --release -p memory-storage-sqlite --example commit_hot_path -- 1000 100 /tmp/req10-sqlite-hotpath.db
```

Arguments: measured operations, warm-up operations, optional DB path. It prints P50/P95/P99, mean, throughput, Linux process peak RSS, DB/WAL/SHM bytes and process CPU ticks. Percentiles use nearest-rank. The example is Linux-oriented for RSS/CPU counters; those fields report NOT_AVAILABLE where `/proc` is absent.

## SQL mirror fallback

`benchmarks/req10/sqlite_commit_sql_mirror.py` is a standard-library-only fallback that mirrors the adapter's SQL transaction structure. It does **not** invoke the Rust adapter method and must not be described as Rust adapter performance.

```sh
python3 benchmarks/req10/sqlite_commit_sql_mirror.py --samples 1000 --warmup 100
```

## Interpretation

- The Rust example measures the actual reference adapter method; the Python fallback measures a SQL-path mirror only and reports process CPU time (not per-operation CPU attribution).
- Neither measures an integrated product runtime or end-to-end ingestion, compilation, retrieval, context assembly or agent delivery.
- One writer and one memory do not characterize concurrent workloads or capacity/saturation.
- Peak RSS is process high-water RSS, not operation-level allocation attribution.
- CPU ticks are process-wide and not a profiler or hardware-counter attribution.
- No model is invoked; model/token cost for this storage-only path is zero, not a product cost estimate.
- File sizes are a point-in-time DB/WAL/SHM observation, not storage-growth projections.
- Capacity limits, backpressure/degradation, repeatable regression thresholds and production SLOs are OUT-OF-SCOPE(dev-baseline).
- Results depend on hardware, OS, filesystem, SQLite build, compiler and run conditions. Do not use these measurements as production budgets.


## 中文说明

### 测量路径

仓库中已有可执行的 SQLite 参考适配器：`crates/memory-storage-sqlite/src/lib.rs` 的 `SqliteMemoryStorage::commit_version`。Rust 示例直接调用该方法。负载为单写入者、单个 Memory、空 Claims 版本；SQLite 使用 WAL 和 synchronous=FULL。

每次写入包含 Scope 校验、JSON 编解码、IMMEDIATE 事务、当前/父版本检查、幂等查询、版本插入、Memory 更新、commit_log 写入、幂等回执写入及事务提交。

### Rust 基准入口

在仓库根目录运行：

```sh
cargo run --release -p memory-storage-sqlite --example commit_hot_path -- 1000 100 /tmp/req10-sqlite-hotpath.db
```

参数依次为实测操作数、预热操作数和可选数据库路径。输出 P50/P95/P99、平均延迟、吞吐、Linux 进程峰值 RSS、DB/WAL/SHM 文件大小及进程 CPU ticks。百分位采用 nearest-rank 算法。RSS/CPU 计数依赖 Linux `/proc`；不可用时会明确输出 NOT_AVAILABLE。

### SQL 镜像回退入口

`benchmarks/req10/sqlite_commit_sql_mirror.py` 是仅使用 Python 标准库的回退程序，复现适配器 SQL 事务结构。它**不会调用 Rust 适配器方法**，不能将其数据称为 Rust 适配器性能。

```sh
python3 benchmarks/req10/sqlite_commit_sql_mirror.py --samples 1000 --warmup 100
```

### 解释与限制

- Rust 示例测量实际参考适配器方法；Python 回退程序只测量 SQL 路径镜像，并报告进程级 CPU 时间（不是单操作 CPU 归因）。
- 两者均不测量集成产品运行时或摄取、编译、召回、上下文组装、Agent 交付的端到端路径。
- 单写入者和单 Memory 不代表并发负载或容量上限。
- 峰值 RSS 是进程高水位，不是单操作内存分配归因。
- CPU ticks 是进程级计数，不是 profiler 或硬件计数器归因。
- 本路径不调用模型；模型/token 成本为零仅表示该存储路径没有模型调用，不代表产品成本。
- 文件大小是单次 DB/WAL/SHM 观察值，不是长期增长预测。
- 容量、饱和、排队、背压/降级、可重复回归阈值和生产 SLO 均为 OUT-OF-SCOPE(dev-baseline)。
- 结果受硬件、操作系统、文件系统、SQLite 构建、编译器和运行条件影响，不得作为生产预算。
