//! MC-03 Evidence Manager.
//!
//! Normative source: `02-domain-model/core-entities.md` §8 (Evidence)
//! and `02-domain-model/phase-2-domain-extension.md` §3.5 (Evidence).
//!
//! This module manages evidence registration and attachment eligibility.
//! It does not assess truth, infer source reliability, calculate independent
//! support, or maintain a second provenance/ancestry model.
//!
//! Evidence identity, role, and scope are owned by the domain `Evidence`.
//! Source details and availability are owned by `EvidenceExtension`.
//! `Evidence::validate_against` is the domain enforcement point for the
//! relationship between those two records.
//!
//! Four invariants drive the design:
//!
//! 1. **Re-registration is idempotent.** Registering the same Evidence and
//!    extension under the same identity yields `AlreadyPresent`; a different
//!    payload under that identity is rejected.
//! 2. **Domain validation is authoritative.** The registry validates the
//!    Evidence and its extension through `Evidence::validate_against`.
//! 3. **Unavailable evidence is not attachable.** Restricted, unavailable,
//!    and forgotten evidence are deferred with an explicit reason.
//! 4. **Provenance validation belongs to the Domain layer.** This registry
//!    does not duplicate provenance validation, store provenance records,
//!    or maintain a parallel ancestry graph.

use std::collections::BTreeMap;

use memory_domain::{DomainError, Evidence, EvidenceAvailability, EvidenceExtension, OpaqueId};

// ---------------------------------------------------------------------------
// Registration outcomes

/// Why an Evidence record was not added to the registry.
///
/// Every variant is a decision, not a failure: the caller keeps the record
/// and decides what to do. Nothing here mutates canonical state.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum EvidenceRejection {
    /// The Evidence or its extension violates a domain invariant.
    InvalidRecord(DomainError),
    /// Same identity, different content. Registering both would make the
    /// evidence identity ambiguous, so the second record is refused.
    IdentityConflict { evidence_id: OpaqueId },
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum RegistrationOutcome {
    Registered,
    AlreadyPresent,
    Rejected(EvidenceRejection),
}

// ---------------------------------------------------------------------------
// Registry

/// A registered Evidence record and its domain extension.
///
/// The Evidence owns its identity, role, and scope. The extension owns the
/// source details and availability. The registry does not introduce another
/// representation of either record.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct EvidenceEntry {
    pub evidence: Evidence,
    pub extension: EvidenceExtension,
}

/// An append-only Evidence registry.
///
/// Entries are keyed by the canonical `Evidence.evidence_id`. Re-registering
/// an identical entry is idempotent; a different entry under the same ID is
/// rejected rather than overwriting the original.
#[derive(Clone, Debug, Default)]
pub struct EvidenceRegistry {
    evidence: BTreeMap<OpaqueId, EvidenceEntry>,
}

impl EvidenceRegistry {
    pub fn new() -> Self {
        Self::default()
    }

    /// Register an Evidence record and its extension.
    ///
    /// The domain's `validate_against` method is the single validation
    /// authority for the Evidence/extension pair.
    pub fn register_evidence(
        &mut self,
        evidence: Evidence,
        extension: EvidenceExtension,
    ) -> RegistrationOutcome {
        if let Err(error) = evidence.validate_against(&extension) {
            return RegistrationOutcome::Rejected(EvidenceRejection::InvalidRecord(error));
        }

        let evidence_id = evidence.evidence_id.clone();
        let entry = EvidenceEntry {
            evidence,
            extension,
        };

        if let Some(existing) = self.evidence.get(&evidence_id) {
            return if existing == &entry {
                RegistrationOutcome::AlreadyPresent
            } else {
                RegistrationOutcome::Rejected(EvidenceRejection::IdentityConflict { evidence_id })
            };
        }

        self.evidence.insert(evidence_id, entry);
        RegistrationOutcome::Registered
    }

    /// Return a registered Evidence entry by its canonical identity.
    pub fn get_evidence(&self, id: &OpaqueId) -> Option<&EvidenceEntry> {
        self.evidence.get(id)
    }

    /// Whether an Evidence identity is registered.
    pub fn contains_evidence(&self, id: &OpaqueId) -> bool {
        self.evidence.contains_key(id)
    }

    /// Number of registered Evidence entries.
    pub fn evidence_count(&self) -> usize {
        self.evidence.len()
    }

    /// Decide whether a Claim may cite this Evidence.
    ///
    /// Restricted, unavailable, and forgotten evidence is deferred. The
    /// registry retains the record and reports why it cannot be attached.
    pub fn attachment_decision(&self, evidence_id: &OpaqueId) -> AttachmentDecision {
        let Some(entry) = self.evidence.get(evidence_id) else {
            return AttachmentDecision::UnknownEvidence {
                evidence_id: evidence_id.clone(),
            };
        };

        match &entry.extension.availability {
            EvidenceAvailability::Available => AttachmentDecision::Attach,
            EvidenceAvailability::Unavailable => AttachmentDecision::Defer {
                reason: "unavailable: source payload is not retained".into(),
            },
            // No scope comparison happens here: this function is given only an
            // evidence id, so claiming the evidence is narrower than the citing
            // Claim would assert something it never checked.
            EvidenceAvailability::Restricted => AttachmentDecision::Defer {
                reason: "restricted: evidence is not currently attachable".into(),
            },
            EvidenceAvailability::Forgotten => AttachmentDecision::Defer {
                reason: "forgotten: source was erased under a forget fence".into(),
            },
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum AttachmentDecision {
    Attach,
    Defer { reason: String },
    UnknownEvidence { evidence_id: OpaqueId },
}
