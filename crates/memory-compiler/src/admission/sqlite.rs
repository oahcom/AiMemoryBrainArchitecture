//! Optional SQLite implementation of the admission store port.
use super::*;
use rusqlite::{params, Connection, OptionalExtension, Transaction, TransactionBehavior};
use std::{path::Path, time::Duration};

/// Local SQLite-backed producer admission ledger.
pub struct SqliteAdmissionStore {
    connection: Connection,
}

impl SqliteAdmissionStore {
    /// Open a durable WAL-backed admission database, as required by §4.1–§4.3.
    pub fn open(path: impl AsRef<Path>) -> Result<Self, AdmissionError> {
        let connection = Connection::open(path)?;
        connection.busy_timeout(Duration::from_secs(5))?;
        connection.execute_batch("PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;")?;
        let store = Self { connection };
        store.initialize()?;
        Ok(store)
    }

    /// Open an in-memory admission database for isolated conformance tests (§4.1–§4.3).
    pub fn in_memory() -> Result<Self, AdmissionError> {
        let connection = Connection::open_in_memory()?;
        connection.busy_timeout(Duration::from_secs(5))?;
        connection.execute_batch(
            "PRAGMA synchronous=FULL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;",
        )?;
        let store = Self { connection };
        store.initialize()?;
        Ok(store)
    }

    fn initialize(&self) -> Result<(), AdmissionError> {
        self.connection.execute_batch(
            "CREATE TABLE IF NOT EXISTS admission_meta (
                singleton INTEGER PRIMARY KEY CHECK(singleton=1),
                fence_generation INTEGER NOT NULL CHECK(fence_generation>=0),
                protocol_sequence INTEGER NOT NULL CHECK(protocol_sequence>=0)
             );
             INSERT OR IGNORE INTO admission_meta(singleton,fence_generation,protocol_sequence) VALUES(1,0,0);
             CREATE TABLE IF NOT EXISTS producer_work (
                ledger_sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                work_item_id TEXT NOT NULL UNIQUE,
                request_digest TEXT NOT NULL,
                request_json TEXT NOT NULL,
                receipt_json TEXT NOT NULL,
                state_json TEXT NOT NULL
             );
             CREATE TABLE IF NOT EXISTS dependency_edges (
                ledger_sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                dependency_id TEXT NOT NULL UNIQUE,
                artifact_ref TEXT NOT NULL,
                artifact_version TEXT NOT NULL,
                work_item_id TEXT NOT NULL,
                request_digest TEXT NOT NULL,
                request_json TEXT NOT NULL,
                receipt_json TEXT NOT NULL
             );
             CREATE INDEX IF NOT EXISTS dependency_artifact_idx
                ON dependency_edges(artifact_ref,artifact_version);
             CREATE TABLE IF NOT EXISTS publication_receipts (
                publication_id TEXT PRIMARY KEY,
                artifact_ref TEXT NOT NULL,
                artifact_version TEXT NOT NULL,
                request_digest TEXT NOT NULL,
                receipt_json TEXT NOT NULL
             );"
        )?;
        Ok(())
    }

    /// Resolve the E-state to D barrier meaning defined by §3.
    pub fn barrier_meaning(state: WorkState) -> BarrierMeaning {
        match state {
            WorkState::Received | WorkState::Validating | WorkState::Accepted => {
                BarrierMeaning::NoAdmissionImplied
            }
            WorkState::DRegistrationPending | WorkState::UnknownReconciliation => {
                BarrierMeaning::OutcomeUnknownFailClosed
            }
            WorkState::Registered | WorkState::Queued => BarrierMeaning::DurableRegistrationOpen,
            WorkState::Leased => BarrierMeaning::DurableRegistrationOpenLeaseTelemetry,
            WorkState::Running | WorkState::CandidatePrivate => {
                BarrierMeaning::DurableRegistrationOpenExecutionTelemetry
            }
            WorkState::StagedPrivate => BarrierMeaning::DurableRegistrationOpenPrivateStaging,
            WorkState::DependencyRegistrationPending => {
                BarrierMeaning::DependencyInventoryMustBeComplete
            }
            WorkState::DependencyRegistered => BarrierMeaning::DependenciesDurableArtifactHidden,
            WorkState::PreparedHidden => BarrierMeaning::DependenciesDurableArtifactHidden,
            WorkState::PublicationGatePending => {
                BarrierMeaning::PublicationDecisionPendingArtifactHidden
            }
            WorkState::Published => BarrierMeaning::PublicationReceiptDurable,
            WorkState::RetryQueued | WorkState::DlqParked => {
                BarrierMeaning::NonTerminalReplayRemainsPossible
            }
            WorkState::SuppressedQuarantined => {
                BarrierMeaning::SuppressedNoPublicationEvidenceRequired
            }
            WorkState::Rejected | WorkState::Cancelled | WorkState::Terminal => {
                BarrierMeaning::TerminalEvidenceRequiresDValidation
            }
        }
    }

    /// Return the complete legal transition relation defined by §2.
    pub fn legal_transition(from: WorkState, to: WorkState) -> bool {
        super::legal_transition(from, to)
    }

    /// Persist a legal lifecycle transition, rejecting all edges outside §2.
    pub fn transition_work_state(
        &mut self,
        work_item_id: &OpaqueId,
        next: WorkState,
    ) -> Result<(), AdmissionError> {
        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)?;
        let state_json: String = tx
            .query_row(
                "SELECT state_json FROM producer_work WHERE work_item_id=?1",
                [work_item_id.as_str()],
                |row| row.get(0),
            )
            .optional()?
            .ok_or(AdmissionError::NotFound)?;
        let current: WorkState = decode(&state_json)?;
        if !Self::legal_transition(current, next) {
            return Err(AdmissionError::InvalidTransition {
                from: current,
                to: next,
            });
        }
        tx.execute(
            "UPDATE producer_work SET state_json=?1 WHERE work_item_id=?2",
            params![encode(&next)?, work_item_id.as_str()],
        )?;
        tx.commit()?;
        Ok(())
    }

    /// Register one logical ProducerWorkItem idempotently, as required by §4.1.
    pub fn register_producer_work(
        &mut self,
        request: ProducerRegistrationRequest,
    ) -> Result<ProducerRegistrationReceipt, AdmissionError> {
        validate_producer_request(&request)?;
        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)?;
        if let Some((digest, receipt_json)) = tx
            .query_row(
                "SELECT request_digest,receipt_json FROM producer_work WHERE work_item_id=?1",
                [request.producer_work_item_id.as_str()],
                |row| Ok((row.get::<_, String>(0)?, row.get::<_, String>(1)?)),
            )
            .optional()?
        {
            if digest != request.request_digest {
                return Err(AdmissionError::IdempotencyConflict);
            }
            let receipt = decode(&receipt_json)?;
            tx.commit()?;
            return Ok(receipt);
        }
        let request_json = encode(&request)?;
        tx.execute(
            "INSERT INTO producer_work(work_item_id,request_digest,request_json,receipt_json,state_json) VALUES(?1,?2,?3,'',?4)",
            params![request.producer_work_item_id.as_str(), request.request_digest, request_json, encode(&WorkState::Accepted)?]
        )?;
        let sequence = tx.last_insert_rowid() as u64;
        let receipt = ProducerRegistrationReceipt {
            receipt_id: OpaqueId::new(format!("producer-registration:{sequence}"))
                .map_err(|_| AdmissionError::InvalidInput("receipt id"))?,
            producer_work_item_id: request.producer_work_item_id.clone(),
            request_digest: request.request_digest.clone(),
            ledger_sequence: sequence,
            disposition: RegistrationDisposition::Accepted,
        };
        tx.execute(
            "UPDATE producer_work SET receipt_json=?1 WHERE work_item_id=?2",
            params![encode(&receipt)?, request.producer_work_item_id.as_str()],
        )?;
        tx.commit()?;
        Ok(receipt)
    }

    /// Look up the durable ProducerRegistrationReceipt by ProducerWorkItemId (§4.1).
    pub fn producer_receipt(
        &self,
        work_item_id: &OpaqueId,
    ) -> Result<ProducerRegistrationReceipt, AdmissionError> {
        let value: String = self
            .connection
            .query_row(
                "SELECT receipt_json FROM producer_work WHERE work_item_id=?1",
                [work_item_id.as_str()],
                |row| row.get(0),
            )
            .optional()?
            .ok_or(AdmissionError::NotFound)?;
        decode(&value)
    }

    /// Count producer ledger rows, exposing the idempotency invariant for §4.1 tests.
    pub fn producer_ledger_count(&self) -> Result<u64, AdmissionError> {
        let count: i64 =
            self.connection
                .query_row("SELECT COUNT(*) FROM producer_work", [], |row| row.get(0))?;
        Ok(count as u64)
    }

    /// Register one artifact dependency edge idempotently; incomplete sets remain hidden (§4.2).
    pub fn register_dependency(
        &mut self,
        request: DependencyRegistrationRequest,
    ) -> Result<DependencyRegistrationReceipt, AdmissionError> {
        validate_dependency_request(&request)?;
        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)?;
        if let Some((digest, receipt_json)) = tx
            .query_row(
                "SELECT request_digest,receipt_json FROM dependency_edges WHERE dependency_id=?1",
                [request.dependency_registration_id.as_str()],
                |row| Ok((row.get::<_, String>(0)?, row.get::<_, String>(1)?)),
            )
            .optional()?
        {
            if digest != request.request_digest {
                return Err(AdmissionError::IdempotencyConflict);
            }
            let receipt = decode(&receipt_json)?;
            tx.commit()?;
            return Ok(receipt);
        }
        let work_exists: bool = tx.query_row(
            "SELECT EXISTS(SELECT 1 FROM producer_work WHERE work_item_id=?1)",
            [request.producer_work_item_id.as_str()],
            |row| row.get(0),
        )?;
        if !work_exists {
            return Err(AdmissionError::NotFound);
        }
        let receipt_id = format!(
            "dependency-registration:{}",
            request.dependency_registration_id.as_str()
        );
        let receipt = DependencyRegistrationReceipt {
            receipt_id: OpaqueId::new(receipt_id)
                .map_err(|_| AdmissionError::InvalidInput("dependency receipt id"))?,
            dependency_registration_id: request.dependency_registration_id.clone(),
            artifact_ref: request.artifact_ref.clone(),
            artifact_version: request.artifact_version.clone(),
            request_digest: request.request_digest.clone(),
        };
        tx.execute(
            "INSERT INTO dependency_edges(dependency_id,artifact_ref,artifact_version,work_item_id,request_digest,request_json,receipt_json) VALUES(?1,?2,?3,?4,?5,?6,?7)",
            params![request.dependency_registration_id.as_str(), request.artifact_ref.as_str(), request.artifact_version.as_str(), request.producer_work_item_id.as_str(), request.request_digest, encode(&request)?, encode(&receipt)?]
        )?;
        tx.commit()?;
        Ok(receipt)
    }

    /// Return whether all declared dependency edges exist; never treats a partial set as visible (§4.2).
    pub fn dependencies_complete(
        &self,
        artifact_ref: &OpaqueId,
        artifact_version: &OpaqueId,
    ) -> Result<bool, AdmissionError> {
        let mut statement = self.connection.prepare(
            "SELECT request_json FROM dependency_edges WHERE artifact_ref=?1 AND artifact_version=?2"
        )?;
        let rows = statement.query_map(
            params![artifact_ref.as_str(), artifact_version.as_str()],
            |row| row.get::<_, String>(0),
        )?;
        let mut required = None;
        let mut count = 0_u32;
        for row in rows {
            let request: DependencyRegistrationRequest = decode(&row?)?;
            if let Some(expected) = required {
                if expected != request.required_dependency_count {
                    return Err(AdmissionError::InvalidInput(
                        "inconsistent dependency count",
                    ));
                }
            } else {
                required = Some(request.required_dependency_count);
            }
            count += 1;
        }
        Ok(required.map(|n| count >= n).unwrap_or(false))
    }

    /// Read the current local fence generation and protocol sequence (§4.3).
    pub fn observe_fence(&self) -> Result<FenceInstallReceipt, AdmissionError> {
        self.connection
            .query_row(
                "SELECT fence_generation,protocol_sequence FROM admission_meta WHERE singleton=1",
                [],
                |row| {
                    Ok(FenceInstallReceipt {
                        fence_generation: row.get::<_, i64>(0)? as u64,
                        protocol_sequence: row.get::<_, i64>(1)? as u64,
                    })
                },
            )
            .map_err(AdmissionError::from)
    }

    /// Install a fence only if the observed protocol sequence is current (§4.3).
    pub fn install_fence(
        &mut self,
        expected_protocol_sequence: u64,
    ) -> Result<FenceInstallReceipt, AdmissionError> {
        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)?;
        let current = read_meta(&tx)?;
        if current.protocol_sequence != expected_protocol_sequence {
            return Err(AdmissionError::StaleProtocol {
                expected: expected_protocol_sequence,
                actual: current.protocol_sequence,
            });
        }
        let next = FenceInstallReceipt {
            fence_generation: current.fence_generation + 1,
            protocol_sequence: current.protocol_sequence + 1,
        };
        tx.execute(
            "UPDATE admission_meta SET fence_generation=?1,protocol_sequence=?2 WHERE singleton=1",
            params![next.fence_generation as i64, next.protocol_sequence as i64],
        )?;
        tx.commit()?;
        Ok(next)
    }

    /// Execute the final gate in the same SQLite serialization domain as fence installation (§4.3).
    ///
    /// This local implementation atomically persists the publication decision and
    /// consumes the observed protocol sequence. It is not a D service API and does
    /// not establish a cross-service Storage visibility transaction.
    ///
    /// Validation order is deliberate: the fence generation is checked before the
    /// protocol sequence, so a concurrent fence installation always surfaces as
    /// `StaleFence` rather than `StaleProtocol`. Callers must not depend on which
    /// counter moved to distinguish the two races; both mean "re-observe and retry".
    pub fn final_publication_gate(
        &mut self,
        request: PublicationGateRequest,
    ) -> Result<PublicationReceipt, AdmissionError> {
        validate_publication_request(&request)?;
        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)?;
        if let Some((digest, receipt_json)) = tx.query_row(
            "SELECT request_digest,receipt_json FROM publication_receipts WHERE publication_id=?1",
            [request.publication_operation_id.as_str()],
            |row| Ok((row.get::<_, String>(0)?, row.get::<_, String>(1)?))
        ).optional()? {
            if digest != request.request_digest { return Err(AdmissionError::IdempotencyConflict); }
            let receipt = decode(&receipt_json)?;
            tx.commit()?;
            return Ok(receipt);
        }
        let meta = read_meta(&tx)?;
        if meta.fence_generation != request.observed_fence_generation {
            return Err(AdmissionError::StaleFence {
                expected: request.observed_fence_generation,
                actual: meta.fence_generation,
            });
        }
        if meta.protocol_sequence != request.observed_protocol_sequence {
            return Err(AdmissionError::StaleProtocol {
                expected: request.observed_protocol_sequence,
                actual: meta.protocol_sequence,
            });
        }
        let work_exists: bool = tx.query_row(
            "SELECT EXISTS(SELECT 1 FROM producer_work WHERE work_item_id=?1)",
            [request.producer_work_item_id.as_str()],
            |row| row.get(0),
        )?;
        if !work_exists {
            return Err(AdmissionError::NotFound);
        }

        let mut statement = tx.prepare(
            "SELECT receipt_json FROM dependency_edges WHERE artifact_ref=?1 AND artifact_version=?2"
        )?;
        let rows = statement.query_map(
            params![
                request.artifact_ref.as_str(),
                request.artifact_version.as_str()
            ],
            |row| row.get::<_, String>(0),
        )?;
        let mut stored_ids = Vec::new();
        for row in rows {
            let receipt: DependencyRegistrationReceipt = decode(&row?)?;
            stored_ids.push(receipt.receipt_id);
        }
        drop(statement);
        if !Self::dependencies_complete_tx(&tx, &request.artifact_ref, &request.artifact_version)? {
            return Err(AdmissionError::DependencySetIncomplete);
        }
        let mut provided = request.dependency_receipt_ids.clone();
        stored_ids.sort_by(|a, b| a.as_str().cmp(b.as_str()));
        provided.sort_by(|a, b| a.as_str().cmp(b.as_str()));
        if stored_ids != provided {
            return Err(AdmissionError::ReceiptMismatch);
        }

        let next_sequence = meta.protocol_sequence + 1;
        let receipt = PublicationReceipt {
            receipt_id: OpaqueId::new(format!(
                "publication:{}",
                request.publication_operation_id.as_str()
            ))
            .map_err(|_| AdmissionError::InvalidInput("publication receipt id"))?,
            publication_operation_id: request.publication_operation_id.clone(),
            artifact_ref: request.artifact_ref.clone(),
            artifact_version: request.artifact_version.clone(),
            producer_work_item_id: request.producer_work_item_id.clone(),
            dependency_receipt_ids: provided,
            fence_generation: meta.fence_generation,
            permission_epoch: request.permission_epoch.clone(),
            protocol_sequence: next_sequence,
            visible: true,
        };
        tx.execute("INSERT INTO publication_receipts(publication_id,artifact_ref,artifact_version,request_digest,receipt_json) VALUES(?1,?2,?3,?4,?5)",
            params![request.publication_operation_id.as_str(), request.artifact_ref.as_str(), request.artifact_version.as_str(), request.request_digest, encode(&receipt)?])?;
        tx.execute(
            "UPDATE admission_meta SET protocol_sequence=?1 WHERE singleton=1",
            [next_sequence as i64],
        )?;
        tx.commit()?;
        Ok(receipt)
    }

    fn dependencies_complete_tx(
        tx: &Transaction<'_>,
        artifact_ref: &OpaqueId,
        artifact_version: &OpaqueId,
    ) -> Result<bool, AdmissionError> {
        let mut statement = tx.prepare("SELECT request_json FROM dependency_edges WHERE artifact_ref=?1 AND artifact_version=?2")?;
        let rows = statement.query_map(
            params![artifact_ref.as_str(), artifact_version.as_str()],
            |row| row.get::<_, String>(0),
        )?;
        let mut required = None;
        let mut count = 0_u32;
        for row in rows {
            let request: DependencyRegistrationRequest = decode(&row?)?;
            if let Some(expected) = required {
                if expected != request.required_dependency_count {
                    return Err(AdmissionError::InvalidInput(
                        "inconsistent dependency count",
                    ));
                }
            } else {
                required = Some(request.required_dependency_count);
            }
            count += 1;
        }
        Ok(required.map(|n| count >= n).unwrap_or(false))
    }

    /// Report whether an artifact has a committed local publication receipt (§4.2–§4.3).
    pub fn is_artifact_visible(
        &self,
        artifact_ref: &OpaqueId,
        artifact_version: &OpaqueId,
    ) -> Result<bool, AdmissionError> {
        let count: i64 = self.connection.query_row(
            "SELECT COUNT(*) FROM publication_receipts WHERE artifact_ref=?1 AND artifact_version=?2",
            params![artifact_ref.as_str(), artifact_version.as_str()], |row| row.get(0)
        )?;
        Ok(count > 0)
    }

    /// Count dependency ledger rows for idempotency and partial-registration checks (§4.2).
    pub fn dependency_ledger_count(&self) -> Result<u64, AdmissionError> {
        let count: i64 =
            self.connection
                .query_row("SELECT COUNT(*) FROM dependency_edges", [], |row| {
                    row.get(0)
                })?;
        Ok(count as u64)
    }

    /// Retrieve the committed PublicationReceipt by PublicationOperationId (§4.3).
    pub fn publication_receipt(
        &self,
        operation_id: &OpaqueId,
    ) -> Result<PublicationReceipt, AdmissionError> {
        let value: String = self
            .connection
            .query_row(
                "SELECT receipt_json FROM publication_receipts WHERE publication_id=?1",
                [operation_id.as_str()],
                |row| row.get(0),
            )
            .optional()?
            .ok_or(AdmissionError::NotFound)?;
        decode(&value)
    }

    /// Compute a stable SHA-256 digest for a serializable request payload (§4.1–§4.3).
    pub fn request_digest<T: Serialize>(request: &T) -> Result<String, AdmissionError> {
        let bytes = serde_json::to_vec(request)?;
        Ok(format!("{:x}", Sha256::digest(bytes)))
    }
}

fn read_meta(tx: &Transaction<'_>) -> Result<FenceInstallReceipt, AdmissionError> {
    tx.query_row(
        "SELECT fence_generation,protocol_sequence FROM admission_meta WHERE singleton=1",
        [],
        |row| {
            Ok(FenceInstallReceipt {
                fence_generation: row.get::<_, i64>(0)? as u64,
                protocol_sequence: row.get::<_, i64>(1)? as u64,
            })
        },
    )
    .map_err(AdmissionError::from)
}

impl AdmissionStore for SqliteAdmissionStore {
    fn transition_work_state(
        &mut self,
        id: &OpaqueId,
        next: WorkState,
    ) -> Result<(), AdmissionError> {
        SqliteAdmissionStore::transition_work_state(self, id, next)
    }
    fn register_producer_work(
        &mut self,
        request: ProducerRegistrationRequest,
    ) -> Result<ProducerRegistrationReceipt, AdmissionError> {
        SqliteAdmissionStore::register_producer_work(self, request)
    }
    fn producer_receipt(
        &self,
        id: &OpaqueId,
    ) -> Result<ProducerRegistrationReceipt, AdmissionError> {
        SqliteAdmissionStore::producer_receipt(self, id)
    }
    fn producer_ledger_count(&self) -> Result<u64, AdmissionError> {
        SqliteAdmissionStore::producer_ledger_count(self)
    }
    fn register_dependency(
        &mut self,
        request: DependencyRegistrationRequest,
    ) -> Result<DependencyRegistrationReceipt, AdmissionError> {
        SqliteAdmissionStore::register_dependency(self, request)
    }
    fn dependencies_complete(
        &self,
        artifact: &OpaqueId,
        version: &OpaqueId,
    ) -> Result<bool, AdmissionError> {
        SqliteAdmissionStore::dependencies_complete(self, artifact, version)
    }
    fn observe_fence(&self) -> Result<FenceInstallReceipt, AdmissionError> {
        SqliteAdmissionStore::observe_fence(self)
    }
    fn install_fence(&mut self, sequence: u64) -> Result<FenceInstallReceipt, AdmissionError> {
        SqliteAdmissionStore::install_fence(self, sequence)
    }
    fn final_publication_gate(
        &mut self,
        request: PublicationGateRequest,
    ) -> Result<PublicationReceipt, AdmissionError> {
        SqliteAdmissionStore::final_publication_gate(self, request)
    }
    fn is_artifact_visible(
        &self,
        artifact: &OpaqueId,
        version: &OpaqueId,
    ) -> Result<bool, AdmissionError> {
        SqliteAdmissionStore::is_artifact_visible(self, artifact, version)
    }
    fn dependency_ledger_count(&self) -> Result<u64, AdmissionError> {
        SqliteAdmissionStore::dependency_ledger_count(self)
    }
    fn publication_receipt(&self, id: &OpaqueId) -> Result<PublicationReceipt, AdmissionError> {
        SqliteAdmissionStore::publication_receipt(self, id)
    }
    fn work_state(&self, id: &OpaqueId) -> Result<WorkState, AdmissionError> {
        let value: String = self
            .connection
            .query_row(
                "SELECT state_json FROM producer_work WHERE work_item_id=?1",
                [id.as_str()],
                |row| row.get(0),
            )
            .optional()?
            .ok_or(AdmissionError::NotFound)?;
        decode(&value)
    }
}