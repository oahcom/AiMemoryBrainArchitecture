//! F-PR258-RESILIENCE-01: file-backed payload custody and failure-mode tests.
//! These tests exercise the public SQLite adapter API, with deliberate database
//! fault injection for tamper detection and an explicit failed-payload-insert rollback
//! assertion across accepted_events, event_payloads, and compile_outbox.

use memory_domain::{OpaqueId, ScopeKind, ScopeRef};
use memory_event_store::{EventClassification, EventEnvelope, EventStoreError};
use memory_event_store_sqlite::{PayloadEventStoreExt, SqliteEventStore};
use rusqlite::Connection;
use sha2::{Digest, Sha256};
use std::path::{Path, PathBuf};
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).unwrap()
}

fn scope() -> ScopeRef {
    ScopeRef {
        scope_id: id("resilience-scope"),
        scope_kind: ScopeKind::User,
        namespace_key: "user:resilience-scope".into(),
    }
}

fn digest(bytes: &[u8]) -> String {
    format!("sha256:{:x}", Sha256::digest(bytes))
}

fn envelope(key: &str, bytes: &[u8]) -> EventEnvelope {
    EventEnvelope {
        event_kind: "observation".into(),
        source_type: "resilience-test".into(),
        source_id: id("resilience-source"),
        producer_actor_ref: id("resilience-actor"),
        scope_refs: vec![scope()],
        event_time: None,
        payload_ref: format!("payload://{key}"),
        payload_digest: digest(bytes),
        classification: EventClassification::Observed,
        idempotency_key: key.into(),
        retention_class: "default".into(),
        correlation_id: id("resilience-correlation"),
    }
}

fn db_path(label: &str) -> PathBuf {
    let nonce = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    std::env::temp_dir().join(format!(
        "f-pr258-{label}-{}-{nonce}.sqlite",
        std::process::id()
    ))
}

fn cleanup(path: &Path) {
    let _ = std::fs::remove_file(path);
    let _ = std::fs::remove_file(path.with_extension("sqlite-wal"));
    let _ = std::fs::remove_file(path.with_extension("sqlite-shm"));
}

#[test]
fn payload_persistence_boundary_sizes_survive_reopen() {
    let path = db_path("sizes");
    let payloads: Vec<Vec<u8>> = vec![
        Vec::new(),
        vec![0xA5],
        (0..=255).cycle().take(64 * 1024).collect(),
        (0..=255).cycle().take(1024 * 1024).collect(),
    ];

    {
        let mut store = SqliteEventStore::open(&path).unwrap();
        for (index, bytes) in payloads.iter().enumerate() {
            store
                .accept_with_payload(envelope(&format!("size-{index}"), bytes), bytes, &[scope()])
                .unwrap();
        }
    }

    let store = SqliteEventStore::open(&path).unwrap();
    let recovered = store.read_after(0, payloads.len() + 1, &[scope()]).unwrap();
    assert_eq!(recovered.len(), payloads.len());
    for (event, expected) in recovered.iter().zip(payloads.iter()) {
        assert_eq!(&event.payload_bytes, expected);
        assert_eq!(event.envelope.payload_digest, digest(expected));
        assert_eq!(event.receipt.payload_digest, digest(expected));
    }
    cleanup(&path);
}

#[test]
fn ordered_read_rejects_payload_and_verified_digest_tampering() {
    let path = db_path("tamper");
    let (payload_row, digest_row) = {
        let mut store = SqliteEventStore::open(&path).unwrap();
        let first = store
            .accept_with_payload(
                envelope("tamper-bytes", b"original-bytes"),
                b"original-bytes",
                &[scope()],
            )
            .unwrap();
        let second = store
            .accept_with_payload(
                envelope("tamper-verified", b"original-digest"),
                b"original-digest",
                &[scope()],
            )
            .unwrap();
        (first.event_id, second.event_id)
    };

    let connection = Connection::open(&path).unwrap();
    let row_id = |event_id: &OpaqueId| {
        event_id
            .as_str()
            .strip_prefix("event:")
            .unwrap()
            .parse::<i64>()
            .unwrap()
    };
    connection
        .execute(
            "UPDATE event_payloads SET payload_bytes = ?1 WHERE event_row = ?2",
            rusqlite::params![b"modified-bytes".as_slice(), row_id(&payload_row)],
        )
        .unwrap();
    connection
        .execute(
            "UPDATE event_payloads SET verified_digest = ?1 WHERE event_row = ?2",
            rusqlite::params![
                "sha256:0000000000000000000000000000000000000000000000000000000000000000",
                row_id(&digest_row)
            ],
        )
        .unwrap();
    drop(connection);

    let store = SqliteEventStore::open(&path).unwrap();
    assert_eq!(
        store.read_after(0, 10, &[scope()]),
        Err(EventStoreError::PayloadIntegrityMismatch)
    );
    cleanup(&path);
}

#[test]
fn restart_preserves_receipt_and_idempotent_payload_replay() {
    let path = db_path("restart");
    let original = {
        let mut store = SqliteEventStore::open(&path).unwrap();
        store
            .accept_with_payload(
                envelope("restart-key", b"stable-payload"),
                b"stable-payload",
                &[scope()],
            )
            .unwrap()
    };

    let mut reopened = SqliteEventStore::open(&path).unwrap();
    let replay = reopened
        .accept_with_payload(
            envelope("restart-key", b"stable-payload"),
            b"stable-payload",
            &[scope()],
        )
        .unwrap();
    assert_eq!(replay, original);

    let recovered = reopened.read_after(0, 10, &[scope()]).unwrap();
    assert_eq!(recovered.len(), 1);
    assert_eq!(recovered[0].receipt, original);
    assert_eq!(recovered[0].payload_bytes, b"stable-payload");
    cleanup(&path);
}

#[test]
fn concurrent_appends_preserve_unique_order_and_payload_custody() {
    const WRITERS: usize = 6;
    let path = db_path("concurrent");
    let barrier = std::sync::Arc::new(std::sync::Barrier::new(WRITERS));
    let mut workers = Vec::new();

    for index in 0..WRITERS {
        let worker_path = path.clone();
        let worker_barrier = barrier.clone();
        workers.push(std::thread::spawn(move || {
            let mut store = SqliteEventStore::open(worker_path).unwrap();
            let bytes = format!("concurrent-payload-{index}").into_bytes();
            worker_barrier.wait();
            store
                .accept_with_payload(
                    envelope(&format!("concurrent-key-{index}"), &bytes),
                    &bytes,
                    &[scope()],
                )
                .unwrap()
        }));
    }

    for worker in workers {
        worker.join().expect("writer thread panicked");
    }

    let store = SqliteEventStore::open(&path).unwrap();
    let events = store.read_after(0, WRITERS + 1, &[scope()]).unwrap();
    assert_eq!(events.len(), WRITERS);
    assert!(events
        .windows(2)
        .all(|pair| pair[0].sequence < pair[1].sequence));
    let mut recovered: Vec<Vec<u8>> = events
        .into_iter()
        .map(|event| event.payload_bytes)
        .collect();
    recovered.sort();
    let mut expected: Vec<Vec<u8>> = (0..WRITERS)
        .map(|index| format!("concurrent-payload-{index}").into_bytes())
        .collect();
    expected.sort();
    assert_eq!(recovered, expected);
    cleanup(&path);
}

#[test]
fn failed_payload_insert_rolls_back_event_payload_and_outbox_rows() {
    let path = db_path("rollback");
    let store = SqliteEventStore::open(&path).unwrap();

    // Force the second durable write in accept_with_payload to fail after the
    // accepted_events insert has executed inside the same SQLite transaction.
    let connection = Connection::open(&path).unwrap();
    connection
        .execute_batch(
            "CREATE TRIGGER reject_event_payload
         BEFORE INSERT ON event_payloads
         BEGIN
             SELECT RAISE(ABORT, 'injected payload insert failure');
         END;",
        )
        .unwrap();
    drop(connection);

    let mut store = store;
    assert_eq!(
        store.accept_with_payload(
            envelope("rollback-key", b"rollback-payload"),
            b"rollback-payload",
            &[scope()],
        ),
        Err(EventStoreError::TransactionUnavailable)
    );
    drop(store);

    let connection = Connection::open(&path).unwrap();
    let accepted: i64 = connection
        .query_row("SELECT COUNT(*) FROM accepted_events", [], |row| row.get(0))
        .unwrap();
    let payloads: i64 = connection
        .query_row("SELECT COUNT(*) FROM event_payloads", [], |row| row.get(0))
        .unwrap();
    let outbox: i64 = connection
        .query_row("SELECT COUNT(*) FROM compile_outbox", [], |row| row.get(0))
        .unwrap();
    assert_eq!((accepted, payloads, outbox), (0, 0, 0));
    drop(connection);
    cleanup(&path);
}

#[test]
fn committed_payload_survives_process_crash_and_wal_recovery() {
    // The child test commits with WAL/FULL, then aborts without dropping the
    // SQLite connection. The parent reopens the same file and verifies recovery.
    if std::env::var_os("F_PR258_CRASH_CHILD").is_some() {
        let path = PathBuf::from(std::env::var_os("F_PR258_CRASH_PATH").unwrap());
        let mut store = SqliteEventStore::open(&path).unwrap();
        store
            .accept_with_payload(
                envelope("crash-committed", b"wal-durable-payload"),
                b"wal-durable-payload",
                &[scope()],
            )
            .unwrap();
        std::process::abort();
    }

    let path = db_path("wal-crash");
    let status = Command::new(std::env::current_exe().unwrap())
        .arg("--exact")
        .arg("committed_payload_survives_process_crash_and_wal_recovery")
        .arg("--nocapture")
        .env("F_PR258_CRASH_CHILD", "1")
        .env("F_PR258_CRASH_PATH", &path)
        .status()
        .unwrap();
    assert!(
        !status.success(),
        "crash child unexpectedly exited successfully"
    );

    let store = SqliteEventStore::open(&path).unwrap();
    let recovered = store.read_after(0, 10, &[scope()]).unwrap();
    assert_eq!(recovered.len(), 1);
    assert_eq!(recovered[0].payload_bytes, b"wal-durable-payload");
    assert_eq!(
        recovered[0].envelope.payload_digest,
        digest(b"wal-durable-payload")
    );
    cleanup(&path);
}
