//! Claim identity classification, per `02-domain-model/domain-model-overview.md` §2.4.
//!
//! Pure and deterministic: no I/O, no clocks, no randomness. Same inputs always produce
//! the same decision, as required by the authorization invariant.
//!
//! `ClaimRevision` carries no quantifier, modality or confidence field, so CI-05, CI-06
//! and CI-12 are not directly reachable. A qualifier may carry them, and the spec's test
//! for a substantive qualifier ("does it change truth conditions") is semantic, not
//! syntactic — so any real qualifier change is reported as ambiguous rather than guessed.
//!
//! Ambiguity never degrades to `NewRevision`: the spec states "It MUST NOT silently
//! select NEW_REVISION as a fallback."

use crate::ClaimRevision;

#[derive(serde::Serialize, serde::Deserialize, Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub enum ClaimIdentityClass {
    NewClaim,
    NewRevision,
}

/// One row of the §2.4 classification table, plus the two rules that refine it.
#[derive(serde::Serialize, serde::Deserialize, Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub enum ChangeDimension {
    /// CI-01
    SubjectReferent,
    /// CI-02
    Predicate,
    /// CI-03
    Object,
    /// CI-04
    Polarity,
    /// CI-05 — not reachable: `ClaimRevision` has no quantifier field.
    Quantifier,
    /// CI-06 — not reachable: `ClaimRevision` has no modality field.
    Modality,
    /// CI-07
    TemporalQualifier,
    /// CI-08
    Scope,
    /// CI-09
    Evidence,
    /// CI-10
    Provenance,
    /// CI-11
    EpistemicStatus,
    /// CI-12 — not reachable: `ClaimRevision` has no confidence field.
    ConfidenceAssessment,
    /// CI-13
    PresentationOnly,
    /// Substantive qualifier rule.
    SubstantiveQualifier,
    /// Identity resolution rule: displayed label changed, referent unchanged.
    LabelOnly,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum ClaimIdentityDecision {
    Classified {
        class: ClaimIdentityClass,
        dimension: ChangeDimension,
    },
    /// Ambiguity MUST NOT fall back to `NewRevision`. This variant is the
    /// governed-decision requirement made representable.
    RequiresGovernedDecision { reason: AmbiguousReason },
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum AmbiguousReason {
    /// Two or more dimensions changed at once; the spec does not define precedence
    /// among them.
    MultipleSubstantiveDimensions { dimensions: Vec<ChangeDimension> },
    /// A qualifier changed and the implementation cannot prove whether it is
    /// substantive: the spec's test is semantic, not syntactic.
    QualifierSubstantivenessUnprovable,
    /// The resolved referent may or may not have changed.
    ReferentResolutionUncertain,
    /// Scope changed together with something else.
    ScopeChangeAccompaniedByOtherChange,
}

/// Classify the change from `prior` to `candidate` for one Claim.
///
/// `prior.claim_ref()` and `candidate.claim_ref()` must be equal: the contract is
/// "classify a change to one Claim". A different `ClaimRef` means the caller asked a
/// different question (two distinct Claims, or an unrecorded identity resolution), so the
/// answer is a governed decision rather than a silent guess.
pub fn classify(prior: &ClaimRevision, candidate: &ClaimRevision) -> ClaimIdentityDecision {
    if prior.claim_ref() != candidate.claim_ref() {
        return governed(AmbiguousReason::ReferentResolutionUncertain);
    }

    // Substantive qualifier rule: the test is whether truth conditions changed, which is
    // not decidable here. Only a provably presentation-only difference is downgraded.
    if !same_multiset(
        &normalised(prior.qualifiers()),
        &normalised(candidate.qualifiers()),
    ) {
        return governed(AmbiguousReason::QualifierSubstantivenessUnprovable);
    }

    let mut dims: Vec<ChangeDimension> = Vec::new();

    if prior.subject() != candidate.subject() {
        // Identity resolution rule: a label-only change does not create a new Claim.
        // Only a normalised-equal difference is provably label-only; anything else is
        // treated as a referent change (CI-01).
        let dim = if normalised_one(prior.subject()) == normalised_one(candidate.subject()) {
            ChangeDimension::LabelOnly
        } else {
            ChangeDimension::SubjectReferent
        };
        push(&mut dims, dim);
    }
    if prior.predicate() != candidate.predicate() {
        push(&mut dims, ChangeDimension::Predicate);
    }
    if prior.object() != candidate.object() {
        push(&mut dims, ChangeDimension::Object);
    }
    if prior.polarity() != candidate.polarity() {
        push(&mut dims, ChangeDimension::Polarity);
    }
    if prior.epistemic_status() != candidate.epistemic_status() {
        push(&mut dims, ChangeDimension::EpistemicStatus);
    }
    if prior.valid_time() != candidate.valid_time() {
        push(&mut dims, ChangeDimension::TemporalQualifier);
    }
    if !same_multiset(prior.evidence_refs(), candidate.evidence_refs()) {
        push(&mut dims, ChangeDimension::Evidence);
    }
    if !same_multiset(prior.provenance_refs(), candidate.provenance_refs()) {
        push(&mut dims, ChangeDimension::Provenance);
    }
    if !same_multiset(prior.scope_refs(), candidate.scope_refs()) {
        push(&mut dims, ChangeDimension::Scope);
    }

    match dims.len() {
        0 => ClaimIdentityDecision::Classified {
            class: ClaimIdentityClass::NewRevision,
            dimension: ChangeDimension::PresentationOnly,
        },
        1 => {
            let dimension = dims[0];
            ClaimIdentityDecision::Classified {
                class: class_of(dimension),
                dimension,
            }
        }
        _ if dims.contains(&ChangeDimension::Scope) => {
            governed(AmbiguousReason::ScopeChangeAccompaniedByOtherChange)
        }
        _ => governed(AmbiguousReason::MultipleSubstantiveDimensions { dimensions: dims }),
    }
}

fn governed(reason: AmbiguousReason) -> ClaimIdentityDecision {
    ClaimIdentityDecision::RequiresGovernedDecision { reason }
}

fn class_of(dimension: ChangeDimension) -> ClaimIdentityClass {
    match dimension {
        ChangeDimension::SubjectReferent
        | ChangeDimension::Predicate
        | ChangeDimension::Object
        | ChangeDimension::Polarity
        | ChangeDimension::Quantifier
        | ChangeDimension::Modality
        | ChangeDimension::TemporalQualifier
        | ChangeDimension::Scope
        | ChangeDimension::SubstantiveQualifier => ClaimIdentityClass::NewClaim,
        ChangeDimension::Evidence
        | ChangeDimension::Provenance
        | ChangeDimension::EpistemicStatus
        | ChangeDimension::ConfidenceAssessment
        | ChangeDimension::PresentationOnly
        | ChangeDimension::LabelOnly => ClaimIdentityClass::NewRevision,
    }
}

fn push(dims: &mut Vec<ChangeDimension>, dim: ChangeDimension) {
    if !dims.contains(&dim) {
        dims.push(dim);
    }
}

fn normalised_one(value: &str) -> String {
    value.trim().to_lowercase()
}

fn normalised(values: &[String]) -> Vec<String> {
    values.iter().map(|value| normalised_one(value)).collect()
}

/// Order-insensitive equality: reference sets are sets, not sequences.
fn same_multiset<T: PartialEq>(left: &[T], right: &[T]) -> bool {
    if left.len() != right.len() {
        return false;
    }
    let mut used = vec![false; right.len()];
    left.iter().all(|item| {
        match right
            .iter()
            .enumerate()
            .position(|(index, other)| !used[index] && item == other)
        {
            Some(index) => {
                used[index] = true;
                true
            }
            None => false,
        }
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{
        ClaimRef, ClaimRevisionRef, EpistemicStatus, EvidenceRef, OpaqueId, ProvenanceRef,
        ScopeKind, ScopeRef, TimeValue,
    };

    fn ev(value: &str) -> EvidenceRef {
        EvidenceRef::new(value).unwrap()
    }

    fn prov(value: &str) -> ProvenanceRef {
        ProvenanceRef::new(value).unwrap()
    }

    #[derive(Clone)]
    struct Draft {
        subject: String,
        predicate: String,
        object: String,
        polarity: String,
        qualifiers: Vec<String>,
        epistemic_status: EpistemicStatus,
        valid_time: TimeValue,
        evidence_refs: Vec<EvidenceRef>,
        provenance_refs: Vec<ProvenanceRef>,
        scope_id: String,
    }

    impl Default for Draft {
        fn default() -> Self {
            Self {
                subject: "alice".into(),
                predicate: "owns".into(),
                object: "bike".into(),
                polarity: "+".into(),
                qualifiers: Vec::new(),
                epistemic_status: EpistemicStatus::Observed,
                valid_time: TimeValue::Unknown,
                evidence_refs: Vec::new(),
                provenance_refs: Vec::new(),
                scope_id: "s1".into(),
            }
        }
    }

    impl Draft {
        fn with(mut self, edit: impl FnOnce(&mut Self)) -> Self {
            edit(&mut self);
            self
        }

        fn revision(&self, revision_ref: &str) -> ClaimRevision {
            self.revision_for(revision_ref, "c1")
        }

        fn revision_for(&self, revision_ref: &str, claim_ref: &str) -> ClaimRevision {
            ClaimRevision::initial(
                ClaimRevisionRef::new(revision_ref).unwrap(),
                ClaimRef::new(claim_ref).unwrap(),
                self.subject.clone(),
                self.predicate.clone(),
                self.object.clone(),
                self.polarity.clone(),
                self.qualifiers.clone(),
                self.epistemic_status.clone(),
                self.valid_time.clone(),
                self.evidence_refs.clone(),
                self.provenance_refs.clone(),
                "2026-01-01T00:00:00Z".into(),
                "initial".into(),
                vec![ScopeRef {
                    scope_id: OpaqueId::new(self.scope_id.clone()).unwrap(),
                    scope_kind: ScopeKind::User,
                    namespace_key: format!("user:{}", self.scope_id),
                }],
            )
            .unwrap()
        }
    }

    fn classified(class: ClaimIdentityClass, dimension: ChangeDimension) -> ClaimIdentityDecision {
        ClaimIdentityDecision::Classified { class, dimension }
    }

    fn change(prior: Draft, candidate: Draft) -> ClaimIdentityDecision {
        classify(&prior.revision("r1"), &candidate.revision("r2"))
    }

    #[test]
    fn ci_01_subject_referent_change_is_new_claim() {
        let decision = change(
            Draft::default(),
            Draft::default().with(|d| d.subject = "bob".into()),
        );
        assert_eq!(
            decision,
            classified(
                ClaimIdentityClass::NewClaim,
                ChangeDimension::SubjectReferent
            )
        );
    }

    #[test]
    fn ci_02_predicate_change_is_new_claim() {
        let decision = change(
            Draft::default(),
            Draft::default().with(|d| d.predicate = "rents".into()),
        );
        assert_eq!(
            decision,
            classified(ClaimIdentityClass::NewClaim, ChangeDimension::Predicate)
        );
    }

    #[test]
    fn ci_03_object_change_is_new_claim() {
        let decision = change(
            Draft::default(),
            Draft::default().with(|d| d.object = "car".into()),
        );
        assert_eq!(
            decision,
            classified(ClaimIdentityClass::NewClaim, ChangeDimension::Object)
        );
    }

    #[test]
    fn ci_04_polarity_change_is_new_claim() {
        let decision = change(
            Draft::default(),
            Draft::default().with(|d| d.polarity = "-".into()),
        );
        assert_eq!(
            decision,
            classified(ClaimIdentityClass::NewClaim, ChangeDimension::Polarity)
        );
    }

    #[test]
    fn ci_07_temporal_qualifier_change_is_new_claim() {
        let decision = change(
            Draft::default(),
            Draft::default()
                .with(|d| d.valid_time = TimeValue::Instant("2026-05-01T00:00:00Z".into())),
        );
        assert_eq!(
            decision,
            classified(
                ClaimIdentityClass::NewClaim,
                ChangeDimension::TemporalQualifier
            )
        );
    }

    #[test]
    fn ci_07_interval_endpoint_change_is_new_claim() {
        let prior = Draft::default().with(|d| {
            d.valid_time = TimeValue::Interval {
                start: "a".into(),
                end: "b".into(),
            }
        });
        let candidate = Draft::default().with(|d| {
            d.valid_time = TimeValue::Interval {
                start: "a".into(),
                end: "c".into(),
            }
        });
        assert_eq!(
            classify(&prior.revision("r1"), &candidate.revision("r2")),
            classified(
                ClaimIdentityClass::NewClaim,
                ChangeDimension::TemporalQualifier
            )
        );
    }

    #[test]
    fn ci_08_scope_only_change_is_new_claim() {
        let decision = change(
            Draft::default(),
            Draft::default().with(|d| d.scope_id = "s2".into()),
        );
        assert_eq!(
            decision,
            classified(ClaimIdentityClass::NewClaim, ChangeDimension::Scope)
        );
    }

    #[test]
    fn ci_09_evidence_change_is_new_revision() {
        let candidate = Draft::default().with(|d| d.evidence_refs = vec![ev("e1")]);
        assert_eq!(
            change(Draft::default(), candidate),
            classified(ClaimIdentityClass::NewRevision, ChangeDimension::Evidence)
        );
    }

    #[test]
    fn ci_09_evidence_reordering_is_not_a_new_claim() {
        let prior = Draft::default().with(|d| d.evidence_refs = vec![ev("e1"), ev("e2")]);
        let candidate = Draft::default().with(|d| d.evidence_refs = vec![ev("e2"), ev("e1")]);
        let decision = change(prior, candidate);
        assert_eq!(
            decision,
            classified(
                ClaimIdentityClass::NewRevision,
                ChangeDimension::PresentationOnly
            )
        );
        assert_ne!(
            decision,
            classified(ClaimIdentityClass::NewClaim, ChangeDimension::Evidence)
        );
    }

    #[test]
    fn ci_10_provenance_change_is_new_revision() {
        let candidate = Draft::default().with(|d| d.provenance_refs = vec![prov("p1")]);
        assert_eq!(
            change(Draft::default(), candidate),
            classified(ClaimIdentityClass::NewRevision, ChangeDimension::Provenance)
        );
    }

    #[test]
    fn ci_11_epistemic_status_change_is_new_revision() {
        let candidate = Draft::default().with(|d| d.epistemic_status = EpistemicStatus::Verified);
        assert_eq!(
            change(Draft::default(), candidate),
            classified(
                ClaimIdentityClass::NewRevision,
                ChangeDimension::EpistemicStatus
            )
        );
    }

    #[test]
    fn ci_13_identical_proposition_is_presentation_only_new_revision() {
        let prior = Draft::default().revision("r1");
        let candidate = Draft::default().revision("r2");
        assert_eq!(
            classify(&prior, &candidate),
            classified(
                ClaimIdentityClass::NewRevision,
                ChangeDimension::PresentationOnly
            )
        );
    }

    #[test]
    fn identity_label_only_change_is_new_revision() {
        let candidate = Draft::default().with(|d| d.subject = "  Alice ".into());
        assert_eq!(
            change(Draft::default(), candidate),
            classified(ClaimIdentityClass::NewRevision, ChangeDimension::LabelOnly)
        );
    }

    #[test]
    fn qualifier_change_requires_governed_decision() {
        let candidate = Draft::default().with(|d| d.qualifiers = vec!["during-2026".into()]);
        assert_eq!(
            change(Draft::default(), candidate),
            ClaimIdentityDecision::RequiresGovernedDecision {
                reason: AmbiguousReason::QualifierSubstantivenessUnprovable
            }
        );
    }

    #[test]
    fn two_substantive_dimensions_require_governed_decision() {
        let candidate = Draft::default().with(|d| {
            d.polarity = "-".into();
            d.object = "car".into();
        });
        match change(Draft::default(), candidate) {
            ClaimIdentityDecision::RequiresGovernedDecision {
                reason: AmbiguousReason::MultipleSubstantiveDimensions { dimensions },
            } => assert_eq!(
                dimensions,
                vec![ChangeDimension::Object, ChangeDimension::Polarity]
            ),
            other => panic!("expected governed decision, got {other:?}"),
        }
    }

    #[test]
    fn scope_change_with_other_change_requires_governed_decision() {
        let candidate = Draft::default().with(|d| {
            d.scope_id = "s2".into();
            d.evidence_refs = vec![ev("e1")];
        });
        assert_eq!(
            change(Draft::default(), candidate),
            ClaimIdentityDecision::RequiresGovernedDecision {
                reason: AmbiguousReason::ScopeChangeAccompaniedByOtherChange
            }
        );
    }

    #[test]
    fn different_claim_ref_requires_governed_decision() {
        let prior = Draft::default().revision("r1");
        let candidate = Draft::default().revision_for("r2", "c2");
        assert_eq!(
            classify(&prior, &candidate),
            ClaimIdentityDecision::RequiresGovernedDecision {
                reason: AmbiguousReason::ReferentResolutionUncertain
            }
        );
    }

    #[test]
    fn ambiguity_never_falls_back_to_new_revision() {
        // domain-model-overview.md §2.4 Authorization invariant:
        // "It MUST NOT silently select NEW_REVISION as a fallback."
        // Evidence plus epistemic status both changed: the class could plausibly be read
        // as NewRevision, which is exactly the fallback the spec forbids.
        let candidate = Draft::default().with(|d| {
            d.evidence_refs = vec![ev("e1")];
            d.epistemic_status = EpistemicStatus::Verified;
        });
        let decision = change(Draft::default(), candidate);
        assert!(
            matches!(
                decision,
                ClaimIdentityDecision::RequiresGovernedDecision { .. }
            ),
            "ambiguity must require a governed decision, got {decision:?}"
        );
        assert_ne!(
            decision,
            classified(ClaimIdentityClass::NewRevision, ChangeDimension::Evidence)
        );
    }

    #[test]
    fn classify_is_deterministic() {
        let prior = Draft::default().revision("r1");
        let candidate = Draft::default()
            .with(|d| d.predicate = "rents".into())
            .revision("r2");
        assert_eq!(classify(&prior, &candidate), classify(&prior, &candidate));
    }
}
