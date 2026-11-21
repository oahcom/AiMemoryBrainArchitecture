use memory_domain::{Memory, MemoryLifecycle, MemoryVersion, OpaqueId, ScopeKind, ScopeRef};
use memory_storage::{CommitRequest, MemoryStorage};
use memory_storage_sqlite::SqliteMemoryStorage;
use std::{env, fs, path::PathBuf, time::Instant};

fn id(value: impl Into<String>) -> OpaqueId { OpaqueId::new(value).expect("valid id") }
fn scope() -> ScopeRef {
    ScopeRef { scope_id: id("bench-user"), scope_kind: ScopeKind::User, namespace_key: "bench:user".into() }
}
fn memory() -> Memory {
    Memory {
        memory_id: id("bench-memory"), memory_kind: "knowledge".into(), scope_refs: vec![scope()],
        current_version_id: None, lifecycle_state: MemoryLifecycle::Candidate,
        retention_class: "default".into(), sensitivity: "normal".into(),
        created_at: "now".into(), updated_at: "now".into(),
    }
}
fn version(n: u64, parent: Option<OpaqueId>) -> MemoryVersion {
    MemoryVersion {
        memory_version_id: id(format!("bench-v{n}")), memory_id: id("bench-memory"),
        version_number: n, parent_version_id: parent, created_at: "now".into(),
        author_kind: "benchmark".into(), change_reason: "REQ-10 SQLite commit benchmark".into(),
        claims: vec![], entity_refs: vec![], relation_refs: vec![], source_refs: vec![],
        provenance_refs: vec![], content_digest: format!("digest-{n}"), schema_version: "1".into(),
    }
}
fn percentile(sorted: &[u128], p: f64) -> u128 {
    let rank = ((p * sorted.len() as f64).ceil() as usize).max(1);
    sorted[rank - 1]
}
fn peak_rss_kib() -> Option<u64> {
    let status = fs::read_to_string("/proc/self/status").ok()?;
    status.lines().find_map(|line| {
        let value = line.strip_prefix("VmHWM:")?.split_whitespace().next()?;
        value.parse().ok()
    })
}
fn process_cpu_ticks() -> Option<u64> {
    let stat = fs::read_to_string("/proc/self/stat").ok()?;
    let tail = stat.rsplit_once(") ")?.1;
    let fields: Vec<&str> = tail.split_whitespace().collect();
    Some(fields.get(11)?.parse::<u64>().ok()? + fields.get(12)?.parse::<u64>().ok()?)
}
fn file_size(path: impl AsRef<std::path::Path>) -> u64 {
    fs::metadata(path).map(|m| m.len()).unwrap_or(0)
}
fn main() -> Result<(), String> {
    let args: Vec<String> = env::args().collect();
    let samples: usize = args.get(1).and_then(|v| v.parse().ok()).unwrap_or(1_000);
    let warmup: usize = args.get(2).and_then(|v| v.parse().ok()).unwrap_or(100);
    if samples == 0 { return Err("samples must be greater than zero".into()); }
    let db = PathBuf::from(args.get(3).cloned().unwrap_or_else(|| "/tmp/req10-sqlite-hotpath.db".into()));
    for suffix in ["", "-wal", "-shm"] {
        let _ = fs::remove_file(format!("{}{}", db.display(), suffix));
    }

    let mut store = SqliteMemoryStorage::open(&db).map_err(|e| format!("{e:?}"))?;
    let visible_scope = scope();
    store.create_memory(memory(), std::slice::from_ref(&visible_scope)).map_err(|e| format!("{e:?}"))?;

    for n in 1..=warmup {
        let parent = if n == 1 { None } else { Some(id(format!("bench-v{}", n - 1))) };
        store.commit_version(CommitRequest {
            memory_id: id("bench-memory"),
            expected_current_version: parent.clone(),
            new_version: version(n as u64, parent),
            idempotency_key: format!("bench-op-{n}"),
            request_digest: format!("bench-digest-{n}"),
        }, std::slice::from_ref(&visible_scope)).map_err(|e| format!("{e:?}"))?;
    }

    let cpu_start = process_cpu_ticks();
    let started = Instant::now();
    let mut latencies = Vec::with_capacity(samples);
    for n in (warmup + 1)..=(warmup + samples) {
        let parent = if n == 1 { None } else { Some(id(format!("bench-v{}", n - 1))) };
        let request = CommitRequest {
            memory_id: id("bench-memory"),
            expected_current_version: parent.clone(),
            new_version: version(n as u64, parent),
            idempotency_key: format!("bench-op-{n}"),
            request_digest: format!("bench-digest-{n}"),
        };
        let one = Instant::now();
        store.commit_version(request, std::slice::from_ref(&visible_scope)).map_err(|e| format!("{e:?}"))?;
        latencies.push(one.elapsed().as_nanos());
    }
    let elapsed = started.elapsed();
    let cpu_ticks = process_cpu_ticks().zip(cpu_start).map(|(end, start)| end.saturating_sub(start));
    let mut sorted = latencies.clone();
    sorted.sort_unstable();
    let mean_us = latencies.iter().sum::<u128>() as f64 / samples as f64 / 1_000.0;
    let throughput = samples as f64 / elapsed.as_secs_f64();
    let rss = peak_rss_kib();
    drop(store);

    let db_bytes = file_size(&db);
    let wal_bytes = file_size(format!("{}-wal", db.display()));
    let shm_bytes = file_size(format!("{}-shm", db.display()));
    println!("benchmark=SqliteMemoryStorage::commit_version");
    println!("adapter=repository crates/memory-storage-sqlite");
    println!("sqlite_version={} journal_mode=WAL synchronous=FULL", rusqlite::version());
    println!("samples={samples} warmup={warmup} concurrency=1 dataset=one_memory_empty_claims");
    println!("elapsed_ms={:.3} throughput_ops_per_sec={throughput:.2}", elapsed.as_secs_f64() * 1_000.0);
    println!("latency_us p50={} p95={} p99={} mean={mean_us:.2}",
        percentile(&sorted, 0.50), percentile(&sorted, 0.95), percentile(&sorted, 0.99));
    match rss {
        Some(kib) => println!("peak_rss_kib={kib} peak_rss_mib={:.2}", kib as f64 / 1_024.0),
        None => println!("peak_rss=NOT_AVAILABLE (Linux /proc/self/status unavailable)"),
    }
    println!("storage_bytes db={db_bytes} wal={wal_bytes} shm={shm_bytes} total={}", db_bytes + wal_bytes + shm_bytes);
    match cpu_ticks {
        Some(ticks) => println!("process_cpu_ticks={ticks} cpu_seconds_at_100hz={:.3}", ticks as f64 / 100.0),
        None => println!("process_cpu=NOT_AVAILABLE"),
    }
    println!("model_calls=0 token_cost=0 (storage-only path; no model invoked)");
    Ok(())
}
