//! Production `PublicationAuthority` for the compiler publication gate.
//!
//! This type is an adapter, not a decider. `OWNER-DECISION-PUBLICATION-RECORD-001`
//! designates two durable records as *the* publication record (D1):
//!
//! 1. the admission ledger row written by `AdmissionStore`, and
//! 2. the storage `publication_preparations` row for the same publication.
//!
//! The adapter reads exactly those two records and reports what they say (D2).
//! It never computes, infers, defaults or substitutes a flag. Three of the eight
//! proof fields have no authoritative issuer yet, so they are reported `false`
//! (D3); `compiler-stage-contract.md` §8 states "E MUST NOT implement substitute
//! authorization decisions".

use memory_domain::OpaqueId;
use memory_storage::{MemoryStorage, PublicationState};

use crate::admission::AdmissionStore;
use crate::{
    map_admission_error, CompilerError, ProducerWorkItemId, PublicationAuthority, PublicationProof,
    StagedDerivative, WorkerLease,
};

/// Adapts the durable admission ledger and the storage preparation row into a
/// `PublicationProof`.
///
/// The admission store is owned rather than borrowed so this value can be moved
/// into `MemoryCompiler`, which owns its own handle to the same database. Both
/// handles read committed rows only; the adapter never writes.
pub struct AdmissionPublicationAuthority<'a> {
    admission: AdmissionStore,
    storage: &'a dyn MemoryStorage,
    producer_work_item_id: OpaqueId,
}

impl<'a> AdmissionPublicationAuthority<'a> {
    pub fn new(
        admission: AdmissionStore,
        storage: &'a dyn MemoryStorage,
        producer_work_item_id: ProducerWorkItemId,
    ) -> Self {
        Self {
            admission,
            storage,
            producer_work_item_id: producer_work_item_id.as_opaque_id().clone(),
        }
    }

    /// Resolve `canonical_commit_confirmed` from the durable record (§4.3).
    ///
    /// The cursor is only a lookup selector and the reference is only a
    /// candidate; the durable row decides. A reference that is still pending
    /// makes no commit claim at all, so the adapter answers `false` rather than
    /// asking the validator to adjudicate a non-claim. Any validator failure is
    /// an authority failure and is propagated unchanged.
    fn canonical_commit_confirmed(
        &self,
        staged: &StagedDerivative,
        producer_request: &crate::admission::ProducerRegistrationRequest,
    ) -> Result<bool, CompilerError> {
        let reference = &producer_request.canonical_commit_ref;
        if reference.is_pending() {
            return Ok(false);
        }
        let cursor = producer_request
            .admission_canonical_commit_cursor
            .as_ref()
            .ok_or(CompilerError::MissingCanonicalCommit)?;
        let expected = crate::canonical_subject_digest(&staged.provenance)?;
        self.admission
            .validate_canonical_commit(cursor, reference, &expected)
            .map_err(CompilerError::CanonicalCommitNotEstablished)
    }
}

impl PublicationAuthority for AdmissionPublicationAuthority<'_> {
    fn obtain_proof(
        &mut self,
        staged: &StagedDerivative,
        lease: &WorkerLease,
    ) -> Result<PublicationProof, CompilerError> {
        // The producer identity and the scope boundary come from the durable
        // admission request, never from a caller-supplied boolean or enum.
        let producer_request = self
            .admission
            .producer_request(&self.producer_work_item_id)
            .map_err(map_admission_error)?;

        let producer_admitted = self
            .admission
            .is_producer_registered(&producer_request.producer_identity)
            .map_err(map_admission_error)?;

        // The same artifact identity mapping the compiler applies before it
        // calls the gate: derivative id -> artifact ref, publication id ->
        // artifact version.
        let artifact_ref = OpaqueId::new(staged.derivative_id.0.clone())
            .map_err(|_| CompilerError::InvalidIdentity)?;
        let artifact_version = OpaqueId::new(staged.publication_id.0.clone())
            .map_err(|_| CompilerError::InvalidIdentity)?;
        let dependency_closure_complete = self
            .admission
            .dependencies_complete(&artifact_ref, &artifact_version)
            .map_err(map_admission_error)?;

        // D4: the hidden state is durable already, so it is read rather than
        // withheld. Any failure to read the designated record is an authority
        // failure, which `PublicationGate` propagates as an error.
        let storage_prepared_hidden = self
            .storage
            .publication_state(
                staged.publication_id.0.as_str(),
                &producer_request.scope_refs,
            )
            .map_err(|_| CompilerError::AdmissionStoreFailure)?
            == Some(PublicationState::PreparedHidden);

        // D-OWNER-DECISION-CANONICAL-COMMIT-001 §4.3: the only permitted source of
        // `canonical_commit_confirmed`. `Ok(true)` confirms; `Ok(false)` is a
        // subject-content mismatch and leaves the flag false; `Err` is an
        // authority failure and is propagated unchanged, never converted to
        // `false` or to a publication disposition.
        let canonical_commit_confirmed =
            self.canonical_commit_confirmed(staged, &producer_request)?;

        Ok(PublicationProof {
            publication_id: staged.publication_id.clone(),
            generation: lease.generation,
            producer_admitted,
            dependency_closure_complete,
            storage_prepared_hidden,
            canonical_commit_confirmed,
            // OWNER-DECISION-PUBLICATION-RECORD-001 D3: no authoritative issuer
            // exists for these flags, so the production adapter reports them as
            // `false` and lets the gate return `Blocked`. They must not be
            // inferred, defaulted or copied from the test-only authorities that
            // hardcode `true`.
            publication_participant_admitted: false,
            protected_visibility_authorized: false,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::admission::{
        DependencyRegistrationRequest, ProducerRegistrationRequest, RegistrationDisposition,
    };
    use crate::{
        CompilerError, Identity, NormalizedIR, Provenance, PublicationDisposition, PublicationGate,
        StageName, StagingInput, StagingStage, Visibility,
    };
    use memory_domain::{Memory, MemoryLifecycle, MemoryVersion, ScopeKind, ScopeRef};
    use memory_storage::PrepareRequest;
    use memory_storage_sqlite::SqliteMemoryStorage;

    fn id(value: &str) -> OpaqueId {
        OpaqueId::new(value).unwrap()
    }

    fn identity(value: &str) -> Identity {
        Identity(value.into())
    }

    fn scope() -> ScopeRef {
        ScopeRef {
            scope_id: id("scope-1"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:scope-1".into(),
        }
    }

    fn memory() -> Memory {
        Memory {
            memory_id: id("memory-1"),
            memory_kind: "knowledge".into(),
            scope_refs: vec![scope()],
            current_version_id: None,
            lifecycle_state: MemoryLifecycle::Candidate,
            retention_class: "default".into(),
            sensitivity: "normal".into(),
            created_at: "now".into(),
            updated_at: "now".into(),
        }
    }

    fn version() -> MemoryVersion {
        MemoryVersion {
            memory_version_id: id("version-1"),
            memory_id: id("memory-1"),
            version_number: 1,
            parent_version_id: None,
            created_at: "now".into(),
            author_kind: "test".into(),
            change_reason: "test".into(),
            claims: vec![],
            entity_refs: vec![],
            relation_refs: vec![],
            source_refs: vec![],
            provenance_refs: vec![],
            content_digest: "digest-version-1".into(),
            schema_version: "1".into(),
        }
    }

    fn producer_request() -> ProducerRegistrationRequest {
        ProducerRegistrationRequest {
            producer_work_item_id: id("work-1"),
            producer_class: "compiler".into(),
            producer_identity: id("producer-identity"),
            source_refs: vec![id("event-1")],
            source_lineage_digest: "lineage-1".into(),
            scope_refs: vec![scope()],
            operation_id: id("operation-1"),
            correlation_id: id("correlation-1"),
            causation_id: None,
            admission_canonical_commit_cursor: Some(id("commit-cursor-1")),
            canonical_commit_ref: memory_domain::CanonicalCommitRef::pending_d(),
            observed_fence_cursor: id("fence-observation-0"),
            permission_epoch: id("permission-epoch-1"),
            request_digest: "producer-request-digest-1".into(),
            producer_schema_version: "v1".into(),
        }
    }

    fn dependency_request() -> DependencyRegistrationRequest {
        DependencyRegistrationRequest {
            dependency_registration_id: id("dependency-1"),
            artifact_ref: id("derivative-1"),
            artifact_version: id("publication-1"),
            producer_work_item_id: id("work-1"),
            derivation_run_id: id("run-1"),
            source_ref: id("event-1"),
            source_version: None,
            provenance_ref: id("provenance-1"),
            scope_refs: vec![scope()],
            lineage_digest: "lineage-1".into(),
            required_dependency_count: 1,
            request_digest: "dependency-request-digest-1".into(),
        }
    }

    fn lease() -> WorkerLease {
        WorkerLease {
            operation_id: identity("operation-1"),
            worker_id: identity("worker-1"),
            generation: 1,
        }
    }

    fn staged() -> StagedDerivative {
        StagedDerivative {
            derivative_id: identity("derivative-1"),
            publication_id: identity("publication-1"),
            event_id: identity("event-1"),
            values: vec!["value".into()],
            dependency_ids: vec![identity("event-1")],
            dependency_closure_digest: "event-1".into(),
            visibility: Visibility::Hidden,
            provenance: Provenance {
                source_event_id: identity("event-1"),
                source_payload_digest: "sha256:test".into(),
                payload_digest_algorithm: "sha256".into(),
                canonicalization_version: "raw-v1".into(),
                stage_output_id: identity("derivative-1"),
                upstream_outputs: vec![],
                compiler_version: crate::COMPILER_VERSION.into(),
                parameter_digest: "dependency-closure:event-1".into(),
                stage_name: StageName::Staging,
                attempt_generation: 1,
            },
        }
    }

    fn admitted_store() -> AdmissionStore {
        admitted_store_with(
            Some(id("commit-cursor-1")),
            memory_domain::CanonicalCommitRef::pending_d(),
        )
    }

    fn admitted_store_with(
        cursor: Option<OpaqueId>,
        reference: memory_domain::CanonicalCommitRef,
    ) -> AdmissionStore {
        let mut admission = AdmissionStore::in_memory().unwrap();
        admission
            .register_producer(&id("producer-identity"), "registry-digest-1")
            .unwrap();
        let mut request = producer_request();
        request.admission_canonical_commit_cursor = cursor;
        request.canonical_commit_ref = reference;
        let receipt = admission.register_producer_work(request).unwrap();
        assert_eq!(receipt.disposition, RegistrationDisposition::Accepted);
        admission.register_dependency(dependency_request()).unwrap();
        admission
    }

    /// A fully admitted store whose request carries a reference backed by a real
    /// `canonical_commits` row for exactly the derivative `staged()` describes.
    fn admitted_store_with_issued_record(issued_at: &str) -> AdmissionStore {
        let subject = crate::canonical_subject_digest(&staged().provenance).unwrap();
        let mut admission = AdmissionStore::in_memory().unwrap();
        admission
            .register_producer(&id("producer-identity"), "registry-digest-1")
            .unwrap();
        let commit_id = id("commit-1");
        let reference = admission
            .issue_canonical_commit(
                &commit_id,
                &memory_domain::IssuerId::new(memory_domain::DEV_BASELINE_ISSUER).unwrap(),
                &subject,
                issued_at,
            )
            .unwrap();
        let mut request = producer_request();
        request.admission_canonical_commit_cursor = Some(commit_id);
        request.canonical_commit_ref = reference;
        let receipt = admission.register_producer_work(request).unwrap();
        assert_eq!(receipt.disposition, RegistrationDisposition::Accepted);
        admission.register_dependency(dependency_request()).unwrap();
        admission
    }

    fn storage_with_prepared_hidden() -> SqliteMemoryStorage {
        let mut storage = SqliteMemoryStorage::in_memory().unwrap();
        storage.create_memory(memory(), &[scope()]).unwrap();
        storage
            .prepare_version(
                PrepareRequest {
                    memory_id: id("memory-1"),
                    expected_current_version: None,
                    new_version: version(),
                    idempotency_key: "prepare-op-1".into(),
                    request_digest: "prepare-digest-1".into(),
                    publication_id: "publication-1".into(),
                    generation: 1,
                },
                &[scope()],
            )
            .unwrap();
        storage
    }

    #[test]
    fn adapter_reports_sourced_flags_and_leaves_unsourced_flags_false() {
        let admission = admitted_store();
        let storage = storage_with_prepared_hidden();
        let mut authority = AdmissionPublicationAuthority::new(
            admission,
            &storage,
            ProducerWorkItemId::new(id("work-1")),
        );

        let proof = authority.obtain_proof(&staged(), &lease()).unwrap();

        assert!(
            proof.producer_admitted,
            "ledger holds a producer_registry row"
        );
        assert!(
            proof.dependency_closure_complete,
            "ledger holds the complete dependency set"
        );
        assert!(
            proof.storage_prepared_hidden,
            "storage holds a PreparedHidden row for this publication"
        );

        // OWNER-DECISION-PUBLICATION-RECORD-001 D3. These three carry no
        // authoritative issuer, so the adapter may only report `false`.
        assert!(!proof.canonical_commit_confirmed);
        assert!(!proof.publication_participant_admitted);
        assert!(!proof.protected_visibility_authorized);
        assert_eq!(proof.publication_id, identity("publication-1"));
        assert_eq!(proof.generation, 1);
    }

    /// GAP-12 closure criterion 3: a caller-supplied cursor alone must not be able
    /// to produce `canonical_commit_confirmed == true` in any `PublicationProof`.
    ///
    /// The two facts are deliberately separated. Staging accepts the run because a
    /// cursor was recorded (D6.2 renamed that precondition to say so); the
    /// production adapter still refuses to call the commit confirmed (D6.1).
    #[test]
    fn caller_supplied_cursor_does_not_confirm_canonical_commit() {
        let admission = admitted_store();

        let recorded_cursor = admission
            .producer_request(&id("work-1"))
            .unwrap()
            .admission_canonical_commit_cursor;
        assert!(
            recorded_cursor.is_some(),
            "the fixture must actually persist a caller-supplied cursor"
        );

        let storage = storage_with_prepared_hidden();
        let mut authority = AdmissionPublicationAuthority::new(
            admission,
            &storage,
            ProducerWorkItemId::new(id("work-1")),
        );

        let proof = authority.obtain_proof(&staged(), &lease()).unwrap();

        assert!(
            !proof.canonical_commit_confirmed,
            "a caller-supplied cursor is not evidence of a confirmed canonical commit (D6.3)"
        );
    }

    #[test]
    fn staging_accepts_a_recorded_cursor_without_calling_the_commit_confirmed() {
        let staged = StagingStage::run(
            StagingInput {
                normalized: NormalizedIR {
                    event_id: identity("event-1"),
                    values: vec!["value".into()],
                    provenance: Provenance {
                        source_event_id: identity("event-1"),
                        source_payload_digest: "sha256:test".into(),
                        payload_digest_algorithm: "sha256".into(),
                        canonicalization_version: "raw-v1".into(),
                        stage_output_id: identity("derivative-1"),
                        upstream_outputs: vec![],
                        compiler_version: crate::COMPILER_VERSION.into(),
                        parameter_digest: "dependency-closure:event-1".into(),
                        stage_name: StageName::Normalization,
                        attempt_generation: 1,
                    },
                },
                derivative_id: identity("derivative-1"),
                publication_id: identity("publication-1"),
                dependency_ids: vec![identity("event-1")],
                dependency_closure_complete: true,
                producer_admitted: true,
                canonical_commit_cursor_recorded: true,
            },
            1,
        )
        .expect("a recorded cursor satisfies the renamed staging precondition");

        assert_eq!(staged.derivative_id, identity("derivative-1"));
        assert_eq!(
            staged.visibility,
            Visibility::Hidden,
            "staging yields a hidden derivative; it never publishes"
        );
    }

    #[test]
    fn staging_rejects_a_run_with_no_recorded_cursor() {
        let error = StagingStage::run(
            StagingInput {
                normalized: NormalizedIR {
                    event_id: identity("event-1"),
                    values: vec!["value".into()],
                    provenance: Provenance {
                        source_event_id: identity("event-1"),
                        source_payload_digest: "sha256:test".into(),
                        payload_digest_algorithm: "sha256".into(),
                        canonicalization_version: "raw-v1".into(),
                        stage_output_id: identity("derivative-1"),
                        upstream_outputs: vec![],
                        compiler_version: crate::COMPILER_VERSION.into(),
                        parameter_digest: "dependency-closure:event-1".into(),
                        stage_name: StageName::Normalization,
                        attempt_generation: 1,
                    },
                },
                derivative_id: identity("derivative-1"),
                publication_id: identity("publication-1"),
                dependency_ids: vec![identity("event-1")],
                dependency_closure_complete: true,
                producer_admitted: true,
                canonical_commit_cursor_recorded: false,
            },
            1,
        )
        .expect_err("staging must still refuse when no cursor was recorded");

        assert_eq!(error, CompilerError::MissingCanonicalCommit);
    }

    #[test]
    fn gate_returns_blocked_not_published_for_the_production_adapter() {
        let admission = admitted_store();
        let storage = storage_with_prepared_hidden();
        let mut authority = AdmissionPublicationAuthority::new(
            admission,
            &storage,
            ProducerWorkItemId::new(id("work-1")),
        );

        let outcome = PublicationGate::run(staged(), &lease(), 1, &mut authority).unwrap();

        assert_eq!(
            outcome.disposition,
            PublicationDisposition::Blocked,
            "a missing authoritative issuer blocks publication; it must not publish"
        );
        assert_eq!(outcome.derivative.visibility, Visibility::Hidden);
    }

    #[test]
    fn adapter_fails_rather_than_defaults_when_the_ledger_has_no_record() {
        let admission = AdmissionStore::in_memory().unwrap();
        let storage = SqliteMemoryStorage::in_memory().unwrap();
        let mut authority = AdmissionPublicationAuthority::new(
            admission,
            &storage,
            ProducerWorkItemId::new(id("work-1")),
        );

        // An absent ledger row is not "not admitted"; it is an authority that
        // cannot answer, and the adapter reports it as an error.
        assert_eq!(
            authority.obtain_proof(&staged(), &lease()),
            Err(CompilerError::MissingProducerAdmission)
        );
    }

    #[test]
    fn adapter_reports_storage_prepared_hidden_false_without_a_preparation_row() {
        let admission = admitted_store();
        let mut storage = SqliteMemoryStorage::in_memory().unwrap();
        storage.create_memory(memory(), &[scope()]).unwrap();
        let mut authority = AdmissionPublicationAuthority::new(
            admission,
            &storage,
            ProducerWorkItemId::new(id("work-1")),
        );

        let proof = authority.obtain_proof(&staged(), &lease()).unwrap();

        assert!(proof.producer_admitted);
        assert!(proof.dependency_closure_complete);
        assert!(
            !proof.storage_prepared_hidden,
            "no preparation row exists for this publication id"
        );
    }

    /// §4.3 + §8 criteria 9 and 11: a validated record confirms the commit, and
    /// because `publication_participant_admitted` and
    /// `protected_visibility_authorized` still have no issuer (GAP-13) the gate
    /// reports `Suppressed`, not `Published`.
    #[test]
    fn a_validated_record_confirms_the_commit_and_the_gate_still_suppresses() {
        let admission = admitted_store_with_issued_record("2026-11-22T00:00:00Z");
        let storage = storage_with_prepared_hidden();
        let mut authority = AdmissionPublicationAuthority::new(
            admission,
            &storage,
            ProducerWorkItemId::new(id("work-1")),
        );

        let proof = authority.obtain_proof(&staged(), &lease()).unwrap();
        assert!(
            proof.canonical_commit_confirmed,
            "only a validated Ok(true) may set the flag"
        );
        assert!(!proof.publication_participant_admitted);
        assert!(!proof.protected_visibility_authorized);

        let outcome = PublicationGate::run(staged(), &lease(), 1, &mut authority).unwrap();
        assert_eq!(outcome.disposition, PublicationDisposition::Suppressed);
        assert_eq!(
            outcome.derivative.visibility,
            Visibility::Hidden,
            "Suppressed never publishes"
        );
    }

    /// A reference that names a real row but a subject digest that does not match
    /// the derivative is `Ok(false)`: the flag stays false and the gate blocks.
    #[test]
    fn a_subject_mismatch_leaves_the_flag_false_and_blocks() {
        let mut admission = admitted_store_with_issued_record("2026-11-22T00:00:00Z");
        // Re-issue under a different commit id and point the request at it, so the
        // row exists and matches the reference but not this derivative's subject.
        let other_subject = OpaqueId::new("f".repeat(64)).unwrap();
        let other = admission
            .issue_canonical_commit(
                &id("commit-2"),
                &memory_domain::IssuerId::new(memory_domain::DEV_BASELINE_ISSUER).unwrap(),
                &other_subject,
                "2026-11-22T00:00:00Z",
            )
            .unwrap();
        let mut request = producer_request();
        request.producer_work_item_id = id("work-2");
        request.request_digest = "producer-request-digest-2".into();
        request.admission_canonical_commit_cursor = Some(id("commit-2"));
        request.canonical_commit_ref = other;
        admission.register_producer_work(request).unwrap();

        let storage = storage_with_prepared_hidden();
        let mut authority = AdmissionPublicationAuthority::new(
            admission,
            &storage,
            ProducerWorkItemId::new(id("work-2")),
        );

        let proof = authority.obtain_proof(&staged(), &lease()).unwrap();
        assert!(
            !proof.canonical_commit_confirmed,
            "a subject mismatch is Ok(false), not confirmation"
        );
        let outcome = PublicationGate::run(staged(), &lease(), 1, &mut authority).unwrap();
        assert_eq!(outcome.disposition, PublicationDisposition::Blocked);
    }

    /// A reference naming no row at all is an authority failure: it must surface
    /// as an error, never as `false` and never as a disposition.
    #[test]
    fn a_missing_record_surfaces_as_an_error_from_the_adapter() {
        let mut admission = admitted_store();
        let orphan = memory_domain::CanonicalCommitRef::from_issued_data(
            memory_domain::CanonicalCommitData {
                commit_id: id("commit-never-issued"),
                issuer: memory_domain::IssuerId::new(memory_domain::DEV_BASELINE_ISSUER).unwrap(),
                subject_digest: crate::canonical_subject_digest(&staged().provenance).unwrap(),
                issued_at: "2026-11-22T00:00:00Z".into(),
            },
        )
        .unwrap();
        let mut request = producer_request();
        request.producer_work_item_id = id("work-3");
        request.request_digest = "producer-request-digest-3".into();
        request.admission_canonical_commit_cursor = Some(id("commit-never-issued"));
        request.canonical_commit_ref = orphan;
        admission.register_producer_work(request).unwrap();

        let storage = storage_with_prepared_hidden();
        let mut authority = AdmissionPublicationAuthority::new(
            admission,
            &storage,
            ProducerWorkItemId::new(id("work-3")),
        );

        assert_eq!(
            authority.obtain_proof(&staged(), &lease()),
            Err(CompilerError::CanonicalCommitNotEstablished(
                crate::admission::CanonicalCommitValidationError::RecordMissing
            ))
        );
    }
}
