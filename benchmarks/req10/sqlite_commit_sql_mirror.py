#!/usr/bin/env python3
"""REQ-10 reference SQLite commit transaction SQL-path mirror.

This measures the SQL transaction shape of the repository adapter, not the Rust
adapter method itself. The Rust example is the authoritative in-repository
harness; use this mirror only when the Rust toolchain/dependencies cannot run.
"""
import argparse, json, os, platform, resource, sqlite3, statistics, tempfile, time

def percentile(values, p):
    rank = max(1, int((p * len(values)) + 0.999999999))
    return values[rank - 1]

def run(path, samples, warmup):
    conn = sqlite3.connect(path, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=FULL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript("""
    CREATE TABLE memories(memory_id TEXT PRIMARY KEY, scope_json TEXT NOT NULL, current_version_id TEXT, memory_json TEXT NOT NULL);
    CREATE TABLE versions(version_id TEXT PRIMARY KEY, memory_id TEXT NOT NULL REFERENCES memories(memory_id), version_number INTEGER NOT NULL, parent_version_id TEXT, scope_json TEXT NOT NULL, version_json TEXT NOT NULL, commit_sequence INTEGER NOT NULL UNIQUE);
    CREATE TABLE idempotency(idempotency_key TEXT PRIMARY KEY, memory_id TEXT NOT NULL REFERENCES memories(memory_id), request_digest TEXT NOT NULL, receipt_json TEXT NOT NULL);
    CREATE INDEX versions_memory_idx ON versions(memory_id, version_number);
    CREATE TABLE commit_log(commit_sequence INTEGER PRIMARY KEY, memory_id TEXT NOT NULL REFERENCES memories(memory_id), version_id TEXT NOT NULL UNIQUE REFERENCES versions(version_id));
    """)
    scope = [{"scope_id":"bench-user","scope_kind":"User","namespace_key":"bench:user"}]
    scope_json = json.dumps(scope, separators=(",",":"))
    memory = {"memory_id":"bench-memory","memory_kind":"knowledge","scope_refs":scope,"current_version_id":None,
              "lifecycle_state":"Candidate","retention_class":"default","sensitivity":"normal","created_at":"now","updated_at":"now"}
    conn.execute("INSERT INTO memories VALUES(?,?,?,?)", ("bench-memory",scope_json,None,json.dumps(memory,separators=(",",":"))))
    def commit(n):
        version_id, parent_id = f"bench-v{n}", None if n == 1 else f"bench-v{n-1}"
        digest, key = f"digest-{n}", f"bench-op-{n}"
        version = {"memory_version_id":version_id,"memory_id":"bench-memory","version_number":n,"parent_version_id":parent_id,
                   "created_at":"now","author_kind":"benchmark","change_reason":"REQ-10 SQLite commit path","claims":[],
                   "entity_refs":[],"relation_refs":[],"source_refs":[],"provenance_refs":[],"content_digest":digest,"schema_version":"1"}
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT scope_json,current_version_id FROM memories WHERE memory_id=?",("bench-memory",)).fetchone()
        assert row is not None and row[1] == parent_id
        assert conn.execute("SELECT COUNT(*) FROM idempotency WHERE idempotency_key=?",(key,)).fetchone()[0] == 0
        if parent_id is not None:
            assert conn.execute("SELECT version_json FROM versions WHERE version_id=?",(parent_id,)).fetchone() is not None
        sequence = conn.execute("SELECT COALESCE(MAX(commit_sequence),0)+1 FROM commit_log").fetchone()[0]
        assert sequence == n
        conn.execute("INSERT INTO versions VALUES(?,?,?,?,?,?,?)",
                     (version_id,"bench-memory",n,parent_id,row[0],json.dumps(version,separators=(",",":")),sequence))
        memory["current_version_id"] = version_id
        conn.execute("UPDATE memories SET current_version_id=?,memory_json=? WHERE memory_id=?",
                     (version_id,json.dumps(memory,separators=(",",":")),"bench-memory"))
        conn.execute("INSERT INTO commit_log VALUES(?,?,?)",(sequence,"bench-memory",version_id))
        receipt = {"memory_id":"bench-memory","resulting_version_id":version_id,"commit_sequence":sequence,"idempotency_key":key}
        conn.execute("INSERT INTO idempotency VALUES(?,?,?,?)",
                     (key,"bench-memory",digest,json.dumps(receipt,separators=(",",":"))))
        conn.execute("COMMIT")
    for n in range(1,warmup+1): commit(n)
    latencies, started = [], time.perf_counter()
    for n in range(warmup+1,warmup+samples+1):
        one = time.perf_counter_ns(); commit(n); latencies.append(time.perf_counter_ns()-one)
    elapsed = time.perf_counter()-started
    latencies.sort()
    sizes = {}
    for suffix in ("","-wal","-shm"):
        p = path+suffix
        sizes[suffix or "db"] = os.path.getsize(p) if os.path.exists(p) else 0
    print(f"runner=Python {platform.python_version()} platform={platform.platform()}")
    print(f"sqlite_version={sqlite3.sqlite_version} journal_mode=WAL synchronous=FULL")
    print(f"samples={samples} warmup={warmup} concurrency=1 dataset=one_memory_empty_claims")
    print(f"elapsed_ms={elapsed*1000:.3f} throughput_ops_per_sec={samples/elapsed:.2f}")
    print("latency_us p50={:.1f} p95={:.1f} p99={:.1f} mean={:.1f}".format(
        percentile(latencies,.50)/1000,percentile(latencies,.95)/1000,percentile(latencies,.99)/1000,statistics.mean(latencies)/1000))
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(f"peak_rss_kib={peak} peak_rss_mib={peak/1024:.2f}")
    print(f"storage_bytes db={sizes['db']} wal={sizes['-wal']} shm={sizes['-shm']} total={sum(sizes.values())}")
    print("model_calls=0 token_cost=0 (no model invoked)")
    conn.close()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--samples",type=int,default=1000)
    parser.add_argument("--warmup",type=int,default=100)
    parser.add_argument("--db",default=None)
    args=parser.parse_args()
    path=args.db or tempfile.mktemp(prefix="req10-sqlite-",suffix=".db")
    for suffix in ("","-wal","-shm"):
        try: os.remove(path+suffix)
        except FileNotFoundError: pass
    run(path,args.samples,args.warmup)

if __name__ == "__main__": main()
