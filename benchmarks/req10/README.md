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

- The Rust example measures the actual reference adapter method; the Python fallback measures a SQL-path mirror only.
- Neither measures an integrated product runtime or end-to-end ingestion, compilation, retrieval, context assembly or agent delivery.
- One writer and one memory do not characterize concurrent workloads or capacity/saturation.
- Peak RSS is process high-water RSS, not operation-level allocation attribution.
- CPU ticks are process-wide and not a profiler or hardware-counter attribution.
- No model is invoked; model/token cost for this storage-only path is zero, not a product cost estimate.
- File sizes are a point-in-time DB/WAL/SHM observation, not storage-growth projections.
- Capacity limits, backpressure/degradation, repeatable regression thresholds and production SLOs are OUT-OF-SCOPE(dev-baseline).
- Results depend on hardware, OS, filesystem, SQLite build, compiler and run conditions. Do not use these measurements as production budgets.
