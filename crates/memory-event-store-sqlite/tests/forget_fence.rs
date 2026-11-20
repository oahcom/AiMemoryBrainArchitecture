use memory_event_store_sqlite::forget_fence::{ForgetFence, ForgetFenceError};
use rusqlite::{params, Connection};
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::{mpsc, Arc, Barrier};
use std::thread;
use std::time::{Duration, SystemTime, UNIX_EPOCH};

fn temp(name: &str) -> PathBuf {
    let n = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
    std::env::temp_dir().join(format!("forget-fence-it-{name}-{}-{n}", std::process::id()))
}
fn schema(path: &Path) {
    let db=Connection::open(path).unwrap();
    db.execute_batch(
        "PRAGMA foreign_keys=ON;
         CREATE TABLE accepted_events(event_row INTEGER PRIMARY KEY,scope_json TEXT NOT NULL,idempotency_key TEXT NOT NULL);
         CREATE TABLE event_payloads(event_row INTEGER PRIMARY KEY REFERENCES accepted_events(event_row) ON DELETE RESTRICT,payload_bytes BLOB NOT NULL);
         CREATE TABLE compile_outbox(event_row INTEGER PRIMARY KEY REFERENCES accepted_events(event_row) ON DELETE RESTRICT,intent_kind TEXT NOT NULL);"
    ).unwrap();
}
fn event(db: &Connection, key: &str, namespace: &str) {
    let scope=serde_json::json!([{"scope_id":"scope-id","scope_kind":"User","namespace_key":namespace}]).to_string();
    db.execute("INSERT INTO accepted_events(scope_json,idempotency_key) VALUES(?1,?2)",params![scope,key]).unwrap();
    let id=db.last_insert_rowid();
    db.execute("INSERT INTO event_payloads VALUES(?1,?2)",params![id,b"payload".as_slice()]).unwrap();
    db.execute("INSERT INTO compile_outbox VALUES(?1,'compile')",[id]).unwrap();
}
fn fixture() -> (PathBuf,PathBuf,PathBuf,ForgetFence) {
    let root=temp("fixture"); fs::create_dir_all(&root).unwrap();
    let live=root.join("live.sqlite"); let backup=root.join("backup.sqlite"); let fence_path=root.join("fence.sqlite");
    schema(&live);
    { let db=Connection::open(&live).unwrap(); event(&db,"alice","user:alice"); event(&db,"bob","user:bob"); }
    fs::copy(&live,&backup).unwrap();
    let fence=ForgetFence::open(&fence_path).unwrap();
    (live,backup,fence_path,fence)
}
fn counts(path: &Path) -> (i64,i64,i64) {
    let db=Connection::open(path).unwrap();
    (db.query_row("SELECT COUNT(*) FROM accepted_events",[],|r|r.get(0)).unwrap(),
     db.query_row("SELECT COUNT(*) FROM event_payloads",[],|r|r.get(0)).unwrap(),
     db.query_row("SELECT COUNT(*) FROM compile_outbox",[],|r|r.get(0)).unwrap())
}

#[test]
fn restore_anti_resurrection_and_preserves_other_scope() {
    let (live,backup,_,fence)=fixture();
    let first=fence.record_forget("user:alice","sha256:forget").unwrap();
    assert_eq!(fence.record_forget("user:alice","sha256:forget").unwrap(),first);
    assert_eq!(fence.restore_backup(&backup,&live).unwrap(),1);
    assert_eq!(counts(&live),(1,1,1));
    let db=Connection::open(&live).unwrap();
    assert_eq!(db.query_row("SELECT idempotency_key FROM accepted_events",[],|r|r.get::<_,String>(0)).unwrap(),"bob");
    assert_eq!(db.query_row("PRAGMA integrity_check",[],|r|r.get::<_,String>(0)).unwrap(),"ok");
}

#[test]
fn missing_or_corrupt_fence_fails_closed() {
    let (live,backup,fence_path,_)=fixture();
    let missing=ForgetFence::open_existing(temp("missing.sqlite"));
    assert!(matches!(missing,Err(ForgetFenceError::InvalidFence(_))));
    let corrupt_path=temp("corrupt.sqlite");
    Connection::open(&corrupt_path).unwrap().close().unwrap();
    assert!(ForgetFence::open_existing(&corrupt_path).is_err());
    assert_eq!(counts(&live),(2,2,2));
    let valid=ForgetFence::open_existing(&fence_path).unwrap();
    assert!(valid.restore_backup(&backup,&live).is_ok());
}

#[test]
fn malformed_scope_refuses_activation_without_partial_change() {
    let (live,backup,_,fence)=fixture();
    let db=Connection::open(&backup).unwrap();
    db.execute("UPDATE accepted_events SET scope_json='not-json' WHERE idempotency_key='alice'",[]).unwrap();
    assert!(matches!(fence.restore_backup(&backup,&live),Err(ForgetFenceError::InvalidScope(_))));
    assert_eq!(counts(&live),(2,2,2));
}

#[test]
fn crash_after_fence_commit_is_retried_without_resurrection() {
    let (live,backup,_,fence)=fixture();
    fence.record_forget("user:alice","sha256:forget").unwrap();
    assert_eq!(counts(&live),(2,2,2)); // crash before live purge
    assert_eq!(fence.restore_backup(&backup,&live).unwrap(),1);
    assert_eq!(counts(&live),(1,1,1));
}

#[test]
fn concurrent_forget_waits_for_restore_snapshot_lock() {
    let (_,_,fence_path,fence)=fixture();
    let lock=Connection::open(&fence_path).unwrap();
    lock.execute_batch("BEGIN IMMEDIATE").unwrap();
    let worker_fence=fence.clone();
    let (tx,rx)=mpsc::channel();
    let barrier=Arc::new(Barrier::new(2));
    let worker_barrier=barrier.clone();
    let worker=thread::spawn(move || {
        worker_barrier.wait();
        tx.send(worker_fence.record_forget("user:bob","sha256:concurrent")).unwrap();
    });
    barrier.wait();
    assert!(rx.recv_timeout(Duration::from_millis(150)).is_err());
    lock.execute_batch("ROLLBACK").unwrap();
    assert!(rx.recv_timeout(Duration::from_secs(5)).unwrap().is_ok());
    worker.join().unwrap();
}
