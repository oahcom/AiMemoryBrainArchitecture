//! Durable, external ForgetFence and fail-closed restore activation gate.
//!
//! The fence database MUST live outside the event-store backup/restore set.
//! Restore holds an IMMEDIATE transaction on that database from preflight
//! through atomic activation, serializing concurrent Forget operations.
use rusqlite::{params, Connection, OptionalExtension, TransactionBehavior};
use std::collections::HashSet;
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicU64, Ordering};
use std::time::{Duration, SystemTime, UNIX_EPOCH};

static STAGE_ID: AtomicU64 = AtomicU64::new(0);

#[derive(Debug)]
pub enum ForgetFenceError {
    Sqlite(rusqlite::Error),
    Io(std::io::Error),
    InvalidFence(&'static str),
    InvalidScope(i64),
    MissingSchema(&'static str),
    Integrity(String),
}
impl From<rusqlite::Error> for ForgetFenceError {
    fn from(value: rusqlite::Error) -> Self { Self::Sqlite(value) }
}
impl From<std::io::Error> for ForgetFenceError {
    fn from(value: std::io::Error) -> Self { Self::Io(value) }
}
impl std::fmt::Display for ForgetFenceError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Sqlite(e) => write!(f, "fence SQLite error: {e}"),
            Self::Io(e) => write!(f, "restore I/O error: {e}"),
            Self::InvalidFence(s) => write!(f, "Forget fence unavailable: {s}"),
            Self::InvalidScope(id) => write!(f, "event {id} has malformed ScopeRef metadata"),
            Self::MissingSchema(s) => write!(f, "backup schema missing {s}"),
            Self::Integrity(s) => write!(f, "staged SQLite integrity_check failed: {s}"),
        }
    }
}
impl std::error::Error for ForgetFenceError {}

#[derive(Clone, Debug)]
pub struct ForgetFence { path: PathBuf }

impl ForgetFence {
    /// Open or initialize the independently durable fence database.
    pub fn open(path: impl AsRef<Path>) -> Result<Self, ForgetFenceError> {
        let path = path.as_ref().to_path_buf();
        if let Some(parent) = path.parent() { fs::create_dir_all(parent)?; }
        let db = Self::connect(&path)?;
        db.execute_batch(
            "PRAGMA journal_mode=WAL;
             PRAGMA synchronous=FULL;
             CREATE TABLE IF NOT EXISTS forget_fence(
               namespace_key TEXT PRIMARY KEY,
               fence_seq INTEGER NOT NULL UNIQUE CHECK(fence_seq > 0),
               reason_digest TEXT NOT NULL,
               recorded_at TEXT NOT NULL
             );
             CREATE TABLE IF NOT EXISTS fence_meta(
               singleton INTEGER PRIMARY KEY CHECK(singleton=1),
               next_seq INTEGER NOT NULL CHECK(next_seq > 0)
             );
             INSERT OR IGNORE INTO fence_meta(singleton,next_seq) VALUES(1,1);"
        )?;
        Ok(Self { path })
    }

    /// Open an already provisioned fence store without creating or repairing it.
    /// Missing or malformed metadata is an error, never an empty-fence fallback.
    pub fn open_existing(path: impl AsRef<Path>) -> Result<Self, ForgetFenceError> {
        let path = path.as_ref().to_path_buf();
        if !path.is_file() {
            return Err(ForgetFenceError::InvalidFence("fence database is missing"));
        }
        let db = Self::connect(&path)?;
        db.execute_batch("BEGIN IMMEDIATE;")?;
        let checked = load_fences(&db);
        let _ = db.execute_batch("ROLLBACK;");
        checked?;
        Ok(Self { path })
    }

    fn connect(path: &Path) -> Result<Connection, ForgetFenceError> {
        let db = Connection::open(path)?;
        db.busy_timeout(Duration::from_secs(10))?;
        db.execute_batch("PRAGMA synchronous=FULL; PRAGMA foreign_keys=ON;")?;
        Ok(db)
    }

    /// Persist a monotonic fence before any live-data purge. Repeated Forget is idempotent.
    pub fn record_forget(&self, namespace_key: &str, reason_digest: &str) -> Result<i64, ForgetFenceError> {
        if namespace_key.trim().is_empty() || reason_digest.trim().is_empty() {
            return Err(ForgetFenceError::InvalidFence("namespace and reason digest are required"));
        }
        let db = Self::connect(&self.path)?;
        let tx = db.unchecked_transaction_with_behavior(TransactionBehavior::Immediate)?;
        let existing: Option<i64> = tx.query_row(
            "SELECT fence_seq FROM forget_fence WHERE namespace_key=?1",
            [namespace_key], |r| r.get(0)
        ).optional()?;
        if let Some(seq) = existing { tx.commit()?; return Ok(seq); }
        let next: i64 = tx.query_row(
            "SELECT next_seq FROM fence_meta WHERE singleton=1", [], |r| r.get(0)
        ).optional()?.ok_or(ForgetFenceError::InvalidFence("fence_meta row missing"))?;
        if next <= 0 { return Err(ForgetFenceError::InvalidFence("next_seq is not positive")); }
        let now = SystemTime::now().duration_since(UNIX_EPOCH).unwrap_or_default().as_nanos().to_string();
        tx.execute("INSERT INTO forget_fence VALUES(?1,?2,?3,?4)",
            params![namespace_key, next, reason_digest, now])?;
        tx.execute("UPDATE fence_meta SET next_seq=?1 WHERE singleton=1", [next + 1])?;
        tx.commit()?;
        Ok(next)
    }

    /// Restore backup -> staging -> fence purge -> integrity check -> atomic activation.
    /// No connection to the live database may be open during activation.
    pub fn restore_backup(&self, backup: impl AsRef<Path>, live: impl AsRef<Path>) -> Result<usize, ForgetFenceError> {
        let backup = backup.as_ref();
        let live = live.as_ref();
        let fence_db = Self::connect(&self.path)?;
        fence_db.execute_batch("BEGIN IMMEDIATE;")?;
        let fences = match load_fences(&fence_db) {
            Ok(value) => value,
            Err(error) => { let _ = fence_db.execute_batch("ROLLBACK;"); return Err(error); }
        };

        let parent = live.parent().unwrap_or_else(|| Path::new("."));
        fs::create_dir_all(parent)?;
        let nonce = STAGE_ID.fetch_add(1, Ordering::Relaxed);
        let stage = parent.join(format!(".forget-restore-{}-{nonce}.sqlite", std::process::id()));
        let result = (|| {
            fs::copy(backup, &stage)?;
            let staged_db = Self::connect(&stage)?;
            validate_schema(&staged_db)?;
            let tx = staged_db.unchecked_transaction_with_behavior(TransactionBehavior::Immediate)?;
            let mut stmt = tx.prepare("SELECT event_row,scope_json FROM accepted_events")?;
            let rows = stmt.query_map([], |r| Ok((r.get::<_, i64>(0)?, r.get::<_, String>(1)?)))?;
            let mut doomed = Vec::new();
            for row in rows {
                let (id, scope_json) = row?;
                let keys = parse_scope_keys(id, &scope_json)?;
                if keys.iter().any(|key| fences.contains(key)) { doomed.push(id); }
            }
            drop(stmt);
            for id in &doomed {
                tx.execute("DELETE FROM compile_outbox WHERE event_row=?1", [id])?;
                tx.execute("DELETE FROM event_payloads WHERE event_row=?1", [id])?;
                tx.execute("DELETE FROM accepted_events WHERE event_row=?1", [id])?;
            }
            tx.commit()?;
            let check: String = staged_db.query_row("PRAGMA integrity_check", [], |r| r.get(0))?;
            if check != "ok" { return Err(ForgetFenceError::Integrity(check)); }
            drop(staged_db);

            // The fence write lock remains held through the single-file activation point.
            for suffix in ["-wal", "-shm"] {
                let sidecar = PathBuf::from(format!("{}{}", live.display(), suffix));
                if sidecar.exists() { fs::remove_file(sidecar)?; }
            }
            fs::rename(&stage, live)?;
            Ok(doomed.len())
        })();
        if stage.exists() { let _ = fs::remove_file(&stage); }
        let _ = fence_db.execute_batch("ROLLBACK;");
        result
    }
}

fn load_fences(db: &Connection) -> Result<HashSet<String>, ForgetFenceError> {
    let next: i64 = db.query_row(
        "SELECT next_seq FROM fence_meta WHERE singleton=1", [], |r| r.get(0)
    ).optional()?.ok_or(ForgetFenceError::InvalidFence("metadata row missing"))?;
    if next <= 0 { return Err(ForgetFenceError::InvalidFence("next_seq invalid")); }
    let mut stmt = db.prepare("SELECT namespace_key,fence_seq,reason_digest FROM forget_fence")?;
    let rows = stmt.query_map([], |r| Ok((
        r.get::<_, String>(0)?, r.get::<_, i64>(1)?, r.get::<_, String>(2)?
    )))?;
    let mut fences = HashSet::new();
    for row in rows {
        let (key, seq, digest) = row?;
        if key.trim().is_empty() || digest.trim().is_empty() || seq <= 0 || seq >= next {
            return Err(ForgetFenceError::InvalidFence("fence row malformed or sequence inconsistent"));
        }
        if !fences.insert(key) {
            return Err(ForgetFenceError::InvalidFence("duplicate fence namespace"));
        }
    }
    Ok(fences)
}

fn validate_schema(db: &Connection) -> Result<(), ForgetFenceError> {
    for table in ["accepted_events", "event_payloads", "compile_outbox"] {
        let found: Option<String> = db.query_row(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?1",
            [table], |r| r.get(0)
        ).optional()?;
        if found.is_none() { return Err(ForgetFenceError::MissingSchema(table)); }
    }
    Ok(())
}

fn parse_scope_keys(row: i64, encoded: &str) -> Result<Vec<String>, ForgetFenceError> {
    let value: serde_json::Value = serde_json::from_str(encoded).map_err(|_| ForgetFenceError::InvalidScope(row))?;
    let entries = value.as_array().filter(|a| !a.is_empty()).ok_or(ForgetFenceError::InvalidScope(row))?;
    let mut keys = Vec::with_capacity(entries.len());
    for entry in entries {
        let valid_id = entry.get("scope_id").and_then(serde_json::Value::as_str)
            .map(|s| !s.trim().is_empty()).unwrap_or(false);
        let valid_kind = entry.get("scope_kind").and_then(serde_json::Value::as_str)
            .map(|s| !s.trim().is_empty()).unwrap_or(false);
        let key = entry.get("namespace_key").and_then(serde_json::Value::as_str)
            .filter(|s| !s.trim().is_empty()).ok_or(ForgetFenceError::InvalidScope(row))?;
        if !valid_id || !valid_kind { return Err(ForgetFenceError::InvalidScope(row)); }
        keys.push(key.to_owned());
    }
    Ok(keys)
}

#[cfg(test)]
mod tests {
    use super::*;
    use rusqlite::params;
    use std::sync::{mpsc, Arc, Barrier};
    use std::thread;

    fn temp(name: &str) -> PathBuf {
        let n = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        std::env::temp_dir().join(format!("forget-fence-{name}-{}-{n}", std::process::id()))
    }
    fn schema(path: &Path) {
        let db = Connection::open(path).unwrap();
        db.execute_batch(
            "PRAGMA foreign_keys=ON;
             CREATE TABLE accepted_events(event_row INTEGER PRIMARY KEY,scope_json TEXT NOT NULL,idempotency_key TEXT NOT NULL);
             CREATE TABLE event_payloads(event_row INTEGER PRIMARY KEY REFERENCES accepted_events(event_row) ON DELETE RESTRICT,payload_bytes BLOB NOT NULL);
             CREATE TABLE compile_outbox(event_row INTEGER PRIMARY KEY REFERENCES accepted_events(event_row) ON DELETE RESTRICT,intent_kind TEXT NOT NULL);"
        ).unwrap();
    }
    fn event(db: &Connection, key: &str, namespace: &str) {
        let scope = serde_json::json!([{"scope_id":"id","scope_kind":"User","namespace_key":namespace}]).to_string();
        db.execute("INSERT INTO accepted_events(scope_json,idempotency_key) VALUES(?1,?2)", params![scope,key]).unwrap();
        let id = db.last_insert_rowid();
        db.execute("INSERT INTO event_payloads VALUES(?1,?2)", params![id,b"payload".as_slice()]).unwrap();
        db.execute("INSERT INTO compile_outbox VALUES(?1,'compile')", [id]).unwrap();
    }
    fn fixture() -> (PathBuf, PathBuf, PathBuf, ForgetFence) {
        let root = temp("fixture"); fs::create_dir_all(&root).unwrap();
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
    fn restore_anti_resurrection_purges_only_fenced_scope_across_all_tables() {
        let (live,backup,_,fence)=fixture();
        fence.record_forget("user:alice","sha256:forget").unwrap();
        assert_eq!(fence.restore_backup(&backup,&live).unwrap(),1);
        assert_eq!(counts(&live),(1,1,1));
        let db=Connection::open(&live).unwrap();
        let key:String=db.query_row("SELECT idempotency_key FROM accepted_events",[],|r|r.get(0)).unwrap();
        assert_eq!(key,"bob");
        assert_eq!(db.query_row("PRAGMA integrity_check",[],|r|r.get::<_,String>(0)).unwrap(),"ok");
    }

    #[test]
    fn missing_or_corrupt_fence_fails_closed() {
        let (live,backup,_,_)=fixture();
        let absent=ForgetFence { path: temp("missing-fence.sqlite") };
        assert!(absent.restore_backup(&backup,&live).is_err());
        let corrupt_path=temp("corrupt-fence.sqlite");
        Connection::open(&corrupt_path).unwrap().close().unwrap();
        let corrupt=ForgetFence { path: corrupt_path };
        assert!(corrupt.restore_backup(&backup,&live).is_err());
        assert_eq!(counts(&live),(2,2,2));
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
    fn crash_after_fence_commit_is_retried_safely_on_restore() {
        let (live,backup,_,fence)=fixture();
        fence.record_forget("user:alice","sha256:forget").unwrap();
        // Simulate process loss before the live-store purge; retry uses durable fence.
        assert_eq!(counts(&live),(2,2,2));
        assert_eq!(fence.restore_backup(&backup,&live).unwrap(),1);
        assert_eq!(counts(&live),(1,1,1));
    }

    #[test]
    fn concurrent_forget_serializes_behind_restore_fence_lock() {
        let (_,_,fence_path,fence)=fixture();
        let lock=Connection::open(&fence_path).unwrap();
        lock.execute_batch("BEGIN IMMEDIATE").unwrap();
        let worker_fence=fence.clone();
        let (tx,rx)=mpsc::channel();
        let barrier=Arc::new(Barrier::new(2));
        let worker_barrier=barrier.clone();
        let worker=thread::spawn(move || {
            worker_barrier.wait();
            let result=worker_fence.record_forget("user:bob","sha256:concurrent");
            tx.send(result).unwrap();
        });
        barrier.wait();
        assert!(rx.recv_timeout(Duration::from_millis(150)).is_err());
        lock.execute_batch("ROLLBACK").unwrap();
        assert_eq!(rx.recv_timeout(Duration::from_secs(5)).unwrap().unwrap(),1);
        worker.join().unwrap();
    }
}
