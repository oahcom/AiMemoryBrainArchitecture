//! ForgetFence against a database that `SqliteEventStore::open` actually created.
//!
//! `tests/forget_fence.rs` builds its fixture schema by hand (3 columns per table),
//! so it never exercises the production 8-column `accepted_events` with its UNIQUE
//! constraint, `event_payloads.verified_digest`, or `compile_outbox.created_at`.
//! `ForgetFence::validate_schema` only checks table names, so drift between the two
//! schemas is invisible there. This test drives the real adapter end to end and
//! asserts the schema is byte-identical before and after a fence restore.

use memory_domain::{OpaqueId, ScopeKind, ScopeRef};
use memory_event_store::{EventClassification, EventEnvelope};
use memory_event_store_sqlite::forget_fence::{ForgetFence, ForgetFenceError};
use memory_event_store_sqlite::{PayloadEventStoreExt, SqliteEventStore};
use rusqlite::Connection;
use sha2::{Digest, Sha256};
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};

fn temp(name: &str) -> PathBuf {
    let n = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    std::env::temp_dir().join(format!(
        "forget-fence-real-{name}-{}-{n}.sqlite",
        std::process::id()
    ))
}

fn cleanup(path: &Path) {
    let _ = fs::remove_file(path);
    let _ = fs::remove_file(path.with_extension("sqlite-wal"));
    let _ = fs::remove_file(path.with_extension("sqlite-shm"));
}

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).unwrap()
}

fn scope(namespace: &str) -> ScopeRef {
    ScopeRef {
        scope_id: id(namespace),
        scope_kind: ScopeKind::User,
        namespace_key: namespace.into(),
    }
}

fn digest(bytes: &[u8]) -> String {
    format!("sha256:{:x}", Sha256::digest(bytes))
}

fn envelope(producer: &str, key: &str, namespace: &str, bytes: &[u8]) -> EventEnvelope {
    EventEnvelope {
        event_kind: "observation".into(),
        source_type: "forget-fence-real-schema".into(),
        source_id: id("real-source"),
        producer_actor_ref: id(producer),
        scope_refs: vec![scope(namespace)],
        event_time: None,
        payload_ref: format!("payload://{key}"),
        payload_digest: digest(bytes),
        classification: EventClassification::Observed,
        idempotency_key: key.into(),
        retention_class: "default".into(),
        correlation_id: id("real-correlation"),
    }
}

/// Schema text of the three tables the fence touches, as SQLite recorded it.
fn schema_of(path: &Path) -> Vec<(String, String)> {
    let db = Connection::open(path).unwrap();
    let mut stmt = db
        .prepare(
            "SELECT name, sql FROM sqlite_master
             WHERE type='table' AND name IN ('accepted_events','event_payloads','compile_outbox')
             ORDER BY name",
        )
        .unwrap();
    let rows = stmt
        .query_map([], |r| Ok((r.get::<_, String>(0)?, r.get::<_, String>(1)?)))
        .unwrap()
        .collect::<Result<Vec<_>, _>>()
        .unwrap();
    rows
}

fn namespaces(path: &Path) -> Vec<String> {
    let db = Connection::open(path).unwrap();
    let mut stmt = db
        .prepare("SELECT scope_json FROM accepted_events ORDER BY event_row")
        .unwrap();
    let rows = stmt
        .query_map([], |r| r.get::<_, String>(0))
        .unwrap()
        .collect::<Result<Vec<_>, _>>()
        .unwrap();
    rows.iter()
        .map(|json| {
            let parsed: Vec<ScopeRef> = serde_json::from_str(json).unwrap();
            parsed[0].namespace_key.clone()
        })
        .collect()
}

fn rows(path: &Path, table: &str) -> i64 {
    Connection::open(path)
        .unwrap()
        .query_row(&format!("SELECT COUNT(*) FROM {table}"), [], |r| r.get(0))
        .unwrap()
}

#[test]
fn fence_restore_purges_one_scope_from_a_store_built_database() {
    let live = temp("live");
    let backup = temp("backup");
    let fence_path = temp("fence");

    // 1. A real SqliteEventStore creates the production schema; no hand-built DDL.
    {
        let mut store = SqliteEventStore::open(&live).unwrap();
        store
            .accept_with_payload(
                envelope("actor-alice", "alice-1", "user:alice", b"alice-1"),
                b"alice-1",
                &[scope("user:alice")],
            )
            .unwrap();
        store
            .accept_with_payload(
                envelope("actor-alice", "alice-2", "user:alice", b"alice-2"),
                b"alice-2",
                &[scope("user:alice")],
            )
            .unwrap();
        store
            .accept_with_payload(
                envelope("actor-bob", "bob-1", "user:bob", b"bob-1"),
                b"bob-1",
                &[scope("user:bob")],
            )
            .unwrap();
        store
            .accept_with_payload(
                envelope("actor-bob", "bob-2", "user:bob", b"bob-2"),
                b"bob-2",
                &[scope("user:bob")],
            )
            .unwrap();
    } // drop closes the connection, checkpointing WAL into the main file.

    assert_eq!(
        (
            rows(&live, "accepted_events"),
            rows(&live, "event_payloads"),
            rows(&live, "compile_outbox")
        ),
        (4, 4, 4)
    );
    let schema_before = schema_of(&live);
    assert_eq!(
        schema_before.len(),
        3,
        "production schema must expose all three tables"
    );

    // 2. Snapshot the real database file.
    fs::copy(&live, &backup).unwrap();

    // 3. Fence one namespace only, then restore the snapshot through the fence.
    let fence = ForgetFence::open(&fence_path).unwrap();
    assert_eq!(
        fence
            .record_forget("user:alice", "sha256:forget-alice")
            .unwrap(),
        1
    );
    assert_eq!(
        fence.restore_backup(&backup, &live).unwrap(),
        2,
        "both alice rows must be purged"
    );

    // 4. The adapter can still open the restored file: schema survived the purge.
    let mut reopened = SqliteEventStore::open(&live).unwrap();

    // 5. Fence semantics on the real schema.
    assert_eq!(
        namespaces(&live),
        vec!["user:bob".to_string(), "user:bob".to_string()]
    );
    assert_eq!(
        (
            rows(&live, "accepted_events"),
            rows(&live, "event_payloads"),
            rows(&live, "compile_outbox")
        ),
        (2, 2, 2)
    );
    let check: String = Connection::open(&live)
        .unwrap()
        .query_row("PRAGMA integrity_check", [], |r| r.get(0))
        .unwrap();
    assert_eq!(check, "ok");

    // 6. No schema drift: the fence must not have reshaped the tables it edited.
    assert_eq!(
        schema_of(&live),
        schema_before,
        "fence restore changed the production schema"
    );

    // 7. The restored database is still writable through the real adapter.
    reopened
        .accept_with_payload(
            envelope("actor-carol", "carol-1", "user:carol", b"carol-1"),
            b"carol-1",
            &[scope("user:carol")],
        )
        .unwrap();
    assert_eq!(rows(&live, "compile_outbox"), 3);

    drop(reopened);
    for path in [&live, &backup, &fence_path] {
        cleanup(path);
    }
}

/// Executable record of a WAL hazard in the restore path.
///
/// `SqliteEventStore` runs in WAL mode, so a live database's committed rows sit in
/// the `-wal` sidecar, not the main file. `ForgetFence::restore_backup` stages its
/// input with `fs::copy(backup, stage)`, which copies ONE file. A backup taken from a
/// live store is therefore a table-less database. The fence fails closed on it
/// (`validate_schema` -> `MissingSchema`) instead of activating a silently empty
/// store, which is the correct direction — but it means the operator's backup step
/// must checkpoint first. This test pins both halves of that contract.
#[test]
fn live_wal_copy_fails_closed_until_checkpointed() {
    let live = temp("wal-live");
    let backup = temp("wal-backup");
    let checkpointed = temp("wal-backup-checkpointed");
    let fence_path = temp("wal-fence");

    let mut store = SqliteEventStore::open(&live).unwrap();
    store
        .accept_with_payload(
            envelope("actor-alice", "alice-1", "user:alice", b"alice-1"),
            b"alice-1",
            &[scope("user:alice")],
        )
        .unwrap();
    store
        .accept_with_payload(
            envelope("actor-bob", "bob-1", "user:bob", b"bob-1"),
            b"bob-1",
            &[scope("user:bob")],
        )
        .unwrap();
    // The store is deliberately NOT dropped: committed rows are still in -wal.
    let wal_sidecar = PathBuf::from(format!("{}-wal", live.display()));
    assert!(
        wal_sidecar.is_file(),
        "expected a -wal sidecar while the store is open"
    );

    // Copy only the main database file, exactly as restore_backup's staging step would.
    fs::copy(&live, &backup).unwrap();

    let fence = ForgetFence::open(&fence_path).unwrap();
    fence
        .record_forget("user:alice", "sha256:forget-alice")
        .unwrap();

    // Fail closed on the un-checkpointed copy, with the typed schema error.
    let error = fence.restore_backup(&backup, &live).unwrap_err();
    assert!(
        matches!(error, ForgetFenceError::MissingSchema("accepted_events")),
        "expected MissingSchema(accepted_events), got {error:?}"
    );
    // A refused activation must leave the live database untouched.
    assert_eq!(
        rows(&live, "accepted_events"),
        2,
        "failed restore must not modify live data"
    );

    // Checkpointing first makes the single-file copy a complete database.
    let busy: i64 = Connection::open(&live)
        .unwrap()
        .query_row("PRAGMA wal_checkpoint(TRUNCATE)", [], |r| r.get(0))
        .unwrap();
    assert_eq!(
        busy, 0,
        "checkpoint was blocked; the copy would still be incomplete"
    );
    fs::copy(&live, &checkpointed).unwrap();

    assert_eq!(fence.restore_backup(&checkpointed, &live).unwrap(), 1);
    assert_eq!(namespaces(&live), vec!["user:bob".to_string()]);

    drop(store);
    for path in [&live, &backup, &checkpointed, &fence_path] {
        cleanup(path);
    }
}
