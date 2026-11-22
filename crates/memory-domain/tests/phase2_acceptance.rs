//! Phase 2 领域模型验收测试 (DM2-01..DM2-14)。
//!
//! 契约：`02-domain-model/phase-2-domain-extension.md` §6 "Required Phase 2 test inventory"。
//!
//! 纪律：当前类型系统无法表达的条目一律 `#[ignore]` 并写明缺口，不写恒真断言充数。
//! 一个 DM2 条目若只有部分维度可表达，则拆成「通过的子维度」+「ignore 的缺口」两条。

use memory_domain::*;
use serde_json::json;

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).unwrap()
}

fn scope(value: &str) -> ScopeRef {
    ScopeRef {
        scope_id: id(value),
        scope_kind: ScopeKind::User,
        namespace_key: format!("user:{value}"),
    }
}

fn claim_revision(revision: &str, claim: &str, evidence: &[&str]) -> ClaimRevision {
    ClaimRevision::initial(
        ClaimRevisionRef::new(revision).unwrap(),
        ClaimRef::new(claim).unwrap(),
        "subject".into(),
        "has_value".into(),
        "blue".into(),
        "affirm".into(),
        vec![],
        EpistemicStatus::Observed,
        TimeValue::Unknown,
        evidence
            .iter()
            .map(|value| EvidenceRef::new(*value).unwrap())
            .collect(),
        vec![ProvenanceRef::new("prov-claim").unwrap()],
        "2026-01-01T00:00:00Z".into(),
        "initial".into(),
        vec![scope("s1")],
    )
    .unwrap()
}

fn fact_revision_with_pin(pin: &str) -> FactRevision {
    FactRevision::initial(
        FactRef::new("fact-1").unwrap(),
        FactRevisionRef::new("fr-1").unwrap(),
        vec![ClaimRevisionRef::new(pin).unwrap()],
        vec![EvidenceRef::new("ev-1").unwrap()],
        vec![ProvenanceRef::new("prov-1").unwrap()],
        scope("s1"),
        AttestorRef::pending_i(),
        AuthorizationDecisionRef::pending_i(),
        "independent_review".into(),
        "1.0".into(),
        FactOutcome::Attested,
        "independent review supports the pinned claim".into(),
        CanonicalCommitRef::pending_d(),
        None,
    )
    .unwrap()
}

fn fact_revision() -> FactRevision {
    fact_revision_with_pin("cr-1")
}

fn claim_revision_json_with(
    value: &ClaimRevision,
    field: &str,
    replacement: serde_json::Value,
) -> ClaimRevision {
    let mut json = serde_json::to_value(value).unwrap();
    json[field] = replacement;
    serde_json::from_value(json).unwrap()
}

fn fact_revision_json_with(
    value: &FactRevision,
    field: &str,
    replacement: serde_json::Value,
) -> FactRevision {
    let mut json = serde_json::to_value(value).unwrap();
    json[field] = replacement;
    serde_json::from_value(json).unwrap()
}

// ---------------------------------------------------------------- DM2-01

#[test]
fn dm2_01_stable_claim_ref_across_revisions() {
    // 证据变化（CI-09）→ 新 revision，ClaimRef 必须不变。
    let first = claim_revision("cr-1", "claim-1", &["ev-1"]);
    let second = claim_revision("cr-2", "claim-1", &["ev-1", "ev-2"]);

    assert!(first.validate().is_ok());
    assert!(second.validate().is_ok());
    assert_eq!(first.claim_ref(), second.claim_ref());
    assert_ne!(first.revision_ref(), second.revision_ref());

    // 修订是追加而非覆盖：旧 revision 的证据集合原样保留。
    assert_eq!(first.evidence_refs(), &[EvidenceRef::new("ev-1").unwrap()]);
    assert_eq!(second.evidence_refs().len(), 2);

    // 校验必须拒绝空 revision_ref，而不是静默接受一个不可引用的 revision。
    let broken = claim_revision_json_with(&first, "revision_ref", json!(""));
    assert_eq!(broken.validate(), Err(DomainError::EmptyId));

    // 校验必须拒绝空 scope 集合。
    let no_scope = claim_revision_json_with(&first, "scope_refs", json!([]));
    assert_eq!(
        no_scope.validate(),
        Err(DomainError::EmptyRequiredField("scope_refs"))
    );
}

#[test]
fn dm2_01_claim_revision_ref_uniqueness_enforced() {
    let first = claim_revision("cr-1", "claim-1", &["ev-1"]);
    let first_ref = first.revision_ref().clone();

    let mut registry = ClaimRevisionRegistry::new();

    // 1. Registering the initial revision succeeds.
    assert_eq!(registry.register_revision(first.clone()), Ok(()));
    assert!(registry.contains(&first_ref));
    assert_eq!(registry.len(), 1);
    assert_eq!(registry.get(&first_ref), Some(&first));

    // 2. Reusing the same revision reference is rejected.
    assert_eq!(
        registry.register_revision(first.clone()),
        Err(DomainError::StaleVersion)
    );
    assert_eq!(registry.len(), 1);

    // 3. A revision whose parent has not been registered is rejected.
    let missing_parent = claim_revision_json_with(
        &claim_revision("cr-2", "claim-1", &["ev-1", "ev-2"]),
        "parent_revision_ref",
        json!("cr-missing"),
    );

    assert_eq!(
        registry.register_revision(missing_parent),
        Err(DomainError::InvalidParent)
    );
    assert_eq!(registry.len(), 1);

    // 4. A revision whose parent belongs to a different claim is rejected.
    let wrong_claim = claim_revision_json_with(
        &claim_revision("cr-3", "claim-2", &["ev-1", "ev-2"]),
        "parent_revision_ref",
        json!("cr-1"),
    );

    assert_eq!(
        registry.register_revision(wrong_claim),
        Err(DomainError::InvalidParent)
    );
    assert_eq!(registry.len(), 1);

    // 5. A successor of the same claim with the correct parent succeeds.
    let successor = claim_revision_json_with(
        &claim_revision("cr-4", "claim-1", &["ev-1", "ev-2"]),
        "parent_revision_ref",
        json!("cr-1"),
    );
    let successor_ref = successor.revision_ref().clone();

    assert_eq!(registry.register_revision(successor.clone()), Ok(()));
    assert!(registry.contains(&successor_ref));
    assert_eq!(registry.len(), 2);
    assert_eq!(registry.get(&successor_ref), Some(&successor));
}

// ---------------------------------------------------------------- DM2-02

#[test]
fn dm2_02_revision_parent_mismatch_rejected() {
    let parent = claim_revision("cr-parent", "claim-a", &["ev-1"]);
    let wrong_claim = ClaimRef::new("claim-b").unwrap();
    let result = ClaimRevision::successor(
        ClaimRevisionRef::new("cr-child").unwrap(),
        wrong_claim,
        &parent,
        "subject".into(),
        "has_value".into(),
        "green".into(),
        "affirm".into(),
        vec![],
        EpistemicStatus::Observed,
        TimeValue::Unknown,
        vec![EvidenceRef::new("ev-2").unwrap()],
        vec![ProvenanceRef::new("prov-2").unwrap()],
        "2026-01-02T00:00:00Z".into(),
        "correction".into(),
        vec![scope("s1")],
    );
    assert_eq!(result.unwrap_err(), DomainError::InvalidParent);
}

#[test]
fn dm2_02_accepted_revision_is_append_only() {
    let first = claim_revision("cr-1", "claim-1", &["ev-1"]);

    // 1. An initial revision can be accepted.
    let accepted = AcceptedRevisionState::accept(first.clone()).unwrap();

    assert_eq!(accepted.revision().revision_ref(), first.revision_ref());
    assert_eq!(accepted.revision(), &first);

    // Capture the complete serialized representation before appending.
    let old_bytes_before = serde_json::to_vec(accepted.revision()).unwrap();

    // Build a correction as a distinct successor revision.
    let successor = ClaimRevision::successor(
        ClaimRevisionRef::new("cr-2").unwrap(),
        first.claim_ref().clone(),
        &first,
        first.subject().to_owned(),
        first.predicate().to_owned(),
        "green".into(),
        first.polarity().to_owned(),
        first.qualifiers().to_vec(),
        first.epistemic_status().clone(),
        first.valid_time().clone(),
        vec![EvidenceRef::new("ev-2").unwrap()],
        first.provenance_refs().to_vec(),
        "2026-01-02T00:00:00Z".into(),
        "correction".into(),
        first.scope_refs().to_vec(),
    )
    .unwrap();

    // 2. Append returns both the preserved old state and the new state.
    let (preserved_old, appended) = accepted.append_successor(successor).unwrap();

    // 3. The old revision is byte-for-byte identical after the append.
    let old_bytes_after = serde_json::to_vec(accepted.revision()).unwrap();
    let preserved_bytes = serde_json::to_vec(preserved_old.revision()).unwrap();

    assert_eq!(old_bytes_before, old_bytes_after);
    assert_eq!(old_bytes_before, preserved_bytes);

    // 4. The new state points to the successor, not the old revision.
    assert_eq!(appended.revision().revision_ref().as_str(), "cr-2");
    assert_eq!(
        appended.revision().parent_revision_ref(),
        Some(first.revision_ref())
    );
    assert_eq!(appended.revision().object(), "green");

    // 5. The previous state still points to cr-1 and retains its old content.
    assert_eq!(
        preserved_old.revision().revision_ref(),
        first.revision_ref()
    );
    assert_eq!(preserved_old.revision().object(), "blue");
    assert_eq!(
        preserved_old.revision().evidence_refs(),
        first.evidence_refs()
    );

    // The appended revision has distinct serialized content.
    let new_bytes = serde_json::to_vec(appended.revision()).unwrap();
    assert_ne!(old_bytes_before, new_bytes);
}

// ---------------------------------------------------------------- DM2-03

#[test]
fn dm2_03_ci_classification_vectors() {
    let prior = claim_revision("cr-1", "claim-1", &["ev-1"]);
    let candidate = || claim_revision("cr-2", "claim-1", &["ev-1"]);

    let classified = |class, dimension| ClaimIdentityDecision::Classified { class, dimension };

    // CI-01: a different subject referent creates a NewClaim.
    assert_eq!(
        classify(
            &prior,
            &claim_revision_json_with(&candidate(), "subject", json!("different subject"))
        ),
        classified(
            ClaimIdentityClass::NewClaim,
            ChangeDimension::SubjectReferent
        )
    );

    // CI-01 label-only branch: trim + lowercase normalization makes these
    // subjects equivalent, so the change is LabelOnly rather than NewClaim.
    assert_eq!(
        classify(
            &prior,
            &claim_revision_json_with(&candidate(), "subject", json!(" SUBJECT "))
        ),
        classified(ClaimIdentityClass::NewRevision, ChangeDimension::LabelOnly)
    );

    // CI-02: predicate change creates a NewClaim.
    assert_eq!(
        classify(
            &prior,
            &claim_revision_json_with(&candidate(), "predicate", json!("holds"))
        ),
        classified(ClaimIdentityClass::NewClaim, ChangeDimension::Predicate)
    );

    // CI-03: object change creates a NewClaim.
    assert_eq!(
        classify(
            &prior,
            &claim_revision_json_with(&candidate(), "object", json!("red"))
        ),
        classified(ClaimIdentityClass::NewClaim, ChangeDimension::Object)
    );

    // CI-04: polarity change creates a NewClaim.
    assert_eq!(
        classify(
            &prior,
            &claim_revision_json_with(&candidate(), "polarity", json!("negate"))
        ),
        classified(ClaimIdentityClass::NewClaim, ChangeDimension::Polarity)
    );

    // CI-07: valid_time change creates a NewClaim.
    assert_eq!(
        classify(
            &prior,
            &claim_revision_json_with(
                &candidate(),
                "valid_time",
                serde_json::to_value(TimeValue::Instant("2026-05-01T00:00:00Z".into())).unwrap()
            )
        ),
        classified(
            ClaimIdentityClass::NewClaim,
            ChangeDimension::TemporalQualifier
        )
    );

    // CI-08: a scope-only change creates a NewClaim.
    assert_eq!(
        classify(
            &prior,
            &claim_revision_json_with(
                &candidate(),
                "scope_refs",
                serde_json::to_value(vec![scope("s2")]).unwrap()
            )
        ),
        classified(ClaimIdentityClass::NewClaim, ChangeDimension::Scope)
    );

    // CI-09: evidence change creates a NewRevision.
    assert_eq!(
        classify(
            &prior,
            &claim_revision_json_with(&candidate(), "evidence_refs", json!(["ev-2"]))
        ),
        classified(ClaimIdentityClass::NewRevision, ChangeDimension::Evidence)
    );

    // CI-10: provenance change creates a NewRevision.
    assert_eq!(
        classify(
            &prior,
            &claim_revision_json_with(&candidate(), "provenance_refs", json!(["prov-other"]))
        ),
        classified(ClaimIdentityClass::NewRevision, ChangeDimension::Provenance)
    );

    // CI-11: epistemic status change creates a NewRevision.
    assert_eq!(
        classify(
            &prior,
            &claim_revision_json_with(
                &candidate(),
                "epistemic_status",
                serde_json::to_value(EpistemicStatus::Verified).unwrap()
            )
        ),
        classified(
            ClaimIdentityClass::NewRevision,
            ChangeDimension::EpistemicStatus
        )
    );

    // CI-13: changing revision_reason alone does not change proposition
    // identity. classify() intentionally ignores revision_reason and therefore
    // classifies this as PresentationOnly / NewRevision.
    assert_eq!(
        classify(
            &prior,
            &claim_revision_json_with(
                &candidate(),
                "revision_reason",
                json!("presentation metadata changed")
            )
        ),
        classified(
            ClaimIdentityClass::NewRevision,
            ChangeDimension::PresentationOnly
        )
    );

    // Multiple substantive dimensions must require a governed decision.
    // Here both predicate and object change; neither dimension takes priority.
    let multiple = claim_revision_json_with(
        &claim_revision_json_with(&candidate(), "predicate", json!("holds")),
        "object",
        json!("red"),
    );

    assert_eq!(
        classify(&prior, &multiple),
        ClaimIdentityDecision::RequiresGovernedDecision {
            reason: AmbiguousReason::MultipleSubstantiveDimensions {
                dimensions: vec![ChangeDimension::Predicate, ChangeDimension::Object],
            },
        }
    );

    // A qualifier change is semantically ambiguous: the classifier cannot
    // determine whether it changes the proposition's truth conditions.
    let qualifier_change =
        claim_revision_json_with(&candidate(), "qualifiers", json!(["during-2026"]));

    assert_eq!(
        classify(&prior, &qualifier_change),
        ClaimIdentityDecision::RequiresGovernedDecision {
            reason: AmbiguousReason::QualifierSubstantivenessUnprovable,
        }
    );

    // CI-05, CI-06 and CI-12 are intentionally not exercised with fabricated
    // vectors:
    // - CI-05 Quantifier: ClaimRevision has no quantifier field.
    // - CI-06 Modality: ClaimRevision has no modality field.
    // - CI-12 ConfidenceAssessment: ClaimRevision has no confidence field.
    //
    // These are model-reachability limitations, not missing classifier
    // branches. The corresponding ChangeDimension enum variants exist, but
    // there is no ClaimRevision input field to change and classify.
}

// ---------------------------------------------------------------- DM2-04

#[test]
fn dm2_04_fact_pins_exact_claim_revision_not_head() {
    // claim-1 已有更新的 head (cr-2)，但 FactRevision 仍精确指向旧 revision cr-1。
    let head = claim_revision("cr-2", "claim-1", &["ev-2"]);
    let pinned_old = claim_revision("cr-1", "claim-1", &["ev-1"]);
    let fact = fact_revision_with_pin(pinned_old.revision_ref().as_str());
    assert!(fact.validate().is_ok());
    assert_eq!(
        fact.claim_revision_refs(),
        &[pinned_old.revision_ref().clone()]
    );
    assert_ne!(fact.claim_revision_refs()[0], *head.revision_ref());

    // 序列化往返不得把精确引用"升级"为 head。
    let round: FactRevision = serde_json::from_str(&serde_json::to_string(&fact).unwrap()).unwrap();
    assert_eq!(round.claim_revision_refs()[0].as_str(), "cr-1");

    // 空的精确引用必须被拒绝，不得被解释为"取当前 head"。
    let broken = fact_revision_json_with(&fact, "claim_revision_refs", json!([""]));
    assert_eq!(broken.validate(), Err(DomainError::EmptyId));
}
#[test]
fn dm2_04_resolution_rejects_claim_head_substitution() {
    let first = claim_revision("cr-1", "claim-1", &["ev-1"]);
    let first_ref = first.revision_ref().clone();

    let second = claim_revision_json_with(
        &claim_revision("cr-2", "claim-1", &["ev-1", "ev-2"]),
        "parent_revision_ref",
        json!("cr-1"),
    );
    let second_ref = second.revision_ref().clone();

    let claim_ref = first.claim_ref().clone();

    let mut resolver = ClaimRevisionResolver::new();

    // 1. Register the initial revision and its successor.
    assert_eq!(resolver.register_revision(first.clone()), Ok(()));
    assert_eq!(resolver.register_revision(second.clone()), Ok(()));

    // The current head is cr-2.
    assert_eq!(
        resolver.resolve_head(&claim_ref).unwrap().revision_ref(),
        &second_ref
    );

    // 2. Exact resolution of cr-1 must return cr-1, not the newer cr-2.
    assert_eq!(
        resolver.resolve(&first_ref).unwrap().revision_ref(),
        &first_ref
    );
    assert_ne!(
        resolver.resolve(&first_ref).unwrap().revision_ref(),
        &second_ref
    );

    // 3. Exact resolution of cr-2 returns cr-2.
    assert_eq!(
        resolver.resolve(&second_ref).unwrap().revision_ref(),
        &second_ref
    );

    // 4. A FactRevision pin to cr-1 remains bound to cr-1 even though
    // the current head of claim-1 is cr-2.
    let fact = fact_revision_json_with(&fact_revision(), "claim_revision_refs", json!(["cr-1"]));

    assert_eq!(fact.claim_revision_refs(), std::slice::from_ref(&first_ref));

    for pinned_ref in fact.claim_revision_refs() {
        let resolved = resolver.resolve(pinned_ref).unwrap();
        assert_eq!(resolved.revision_ref(), &first_ref);
        assert_ne!(resolved.revision_ref(), &second_ref);
    }

    // 5. An unknown exact revision reference must not fall back to the head.
    let missing_ref = ClaimRevisionRef::new("cr-missing").unwrap();

    assert_eq!(
        resolver.resolve(&missing_ref),
        Err(DomainError::MissingClaimRevision)
    );

    // 6. Explicit anti-substitution check:
    // pinned=cr-1, current head=cr-2. The API must return cr-1.
    let exact = resolver.resolve_exact(&first_ref, &second_ref).unwrap();

    assert_eq!(exact.revision_ref(), &first_ref);
    assert_ne!(exact.revision_ref(), &second_ref);
}

// ---------------------------------------------------------------- DM2-05

#[test]
fn dm2_05_fact_identity_distinct_and_pins_exact_refs() {
    let fact = fact_revision();
    assert!(fact.validate().is_ok());

    // Fact 身份独立于它引用的 ClaimRevision：不同 pin 不改 FactRef。
    let repinned = fact_revision_with_pin("cr-other");
    assert_eq!(repinned.fact_ref(), fact.fact_ref());
    assert_ne!(repinned.claim_revision_refs(), fact.claim_revision_refs());

    // Evidence 必须非空且精确。
    let no_evidence = fact_revision_json_with(&fact, "evidence_refs", json!([]));
    assert_eq!(
        no_evidence.validate(),
        Err(DomainError::MissingFactEvidence)
    );

    // Provenance 必须非空且精确。
    let no_provenance = fact_revision_json_with(&fact, "provenance_refs", json!([]));
    assert_eq!(
        no_provenance.validate(),
        Err(DomainError::MissingFactProvenance)
    );

    let empty_evidence = fact_revision_json_with(&fact, "evidence_refs", json!([""]));
    assert_eq!(empty_evidence.validate(), Err(DomainError::EmptyId));

    let empty_provenance = fact_revision_json_with(&fact, "provenance_refs", json!([""]));
    assert_eq!(empty_provenance.validate(), Err(DomainError::EmptyId));
}

#[test]
fn dm2_05_fact_revision_accepts_multiple_exact_claim_revision_pins() {
    let first = ClaimRevisionRef::new("cr-1").unwrap();
    let second = ClaimRevisionRef::new("cr-2").unwrap();
    let fact = FactRevision::initial(
        FactRef::new("fact-multi").unwrap(),
        FactRevisionRef::new("fr-multi").unwrap(),
        vec![first.clone(), second.clone()],
        vec![EvidenceRef::new("ev-multi").unwrap()],
        vec![ProvenanceRef::new("prov-multi").unwrap()],
        scope("s1"),
        AttestorRef::pending_i(),
        AuthorizationDecisionRef::pending_i(),
        "joint_review".into(),
        "1.0".into(),
        FactOutcome::Attested,
        "both independently authorized dependencies are required".into(),
        CanonicalCommitRef::pending_d(),
        None,
    )
    .unwrap();
    assert!(fact.validate().is_ok());
    assert_eq!(fact.claim_revision_refs(), &[first, second]);
}

// ---------------------------------------------------------------- DM2-06

#[test]
#[ignore = "blocked: FactRevision::initial 强制要求 AuthorizationDecisionRef，但当前唯一公开构造是 AuthorizationDecisionRef::pending_i()；类型没有 absent/validated-I-issued 状态，无法证明缺失授权被拒绝。Round 4 的 fact_with_placeholder_attestor_validates_today 固定了当前占位符可通过的事实"]
fn dm2_06_missing_authorization_ref_blocks_fact_publication() {
    unimplemented!()
}

// ---------------------------------------------------------------- DM2-07

#[test]
fn dm2_07_label_alias_does_not_merge_identity() {
    let mut left = EntityIdentityExtension {
        entity_ref: EntityRef::new("entity-left").unwrap(),
        status: EntityIdentityStatus::Resolved,
        aliases: vec![],
        external_identifiers: vec![],
        merge_lineage: None,
        split_successor_refs: vec![],
    };
    let right = EntityIdentityExtension {
        entity_ref: EntityRef::new("entity-right").unwrap(),
        status: EntityIdentityStatus::Resolved,
        aliases: vec![],
        external_identifiers: vec![],
        merge_lineage: None,
        split_successor_refs: vec![],
    };
    left.add_alias(EntityAlias {
        value: "same label".into(),
        language: Some("en".into()),
    })
    .unwrap();
    assert_ne!(left.entity_ref, right.entity_ref);
    assert_eq!(left.aliases[0].value, "same label");
    assert!(left.merge_lineage.is_none());
    assert!(right.merge_lineage.is_none());
}

// ---------------------------------------------------------------- DM2-08

#[test]
fn dm2_08_invalid_relation_endpoint_rejected() {
    let extension = RelationExtension {
        subject: RelationEndpoint::Entity(EntityRef::new("entity-1").unwrap()),
        object: RelationEndpoint::Fact(FactRef::new("fact-1").unwrap()),
        directionality: RelationDirectionality::Directed,
        qualifiers: vec![],
        valid_time: Some(ValidTimeRef::Unknown),
        epistemic_status: EpistemicStatus::Observed,
        evidence_refs: vec![EvidenceRef::new("ev-1").unwrap()],
        lifecycle_state: RelationLifecycleState::Active,
        scope_refs: vec![],
    };
    let definition = RelationDefinition {
        relation_type: "owns".into(),
        allowed_subject_kinds: vec![RelationEndpointKind::Entity],
        allowed_object_kinds: vec![RelationEndpointKind::Entity],
    };
    assert_eq!(
        extension.validate(&definition),
        Err(DomainError::InvalidRelationEndpoint)
    );

    let empty_type = RelationDefinition {
        relation_type: String::new(),
        ..definition
    };
    let compatible = RelationExtension {
        object: RelationEndpoint::Entity(EntityRef::new("entity-2").unwrap()),
        ..extension
    };
    assert_eq!(
        compatible.validate(&empty_type),
        Err(DomainError::EmptyRequiredField("relation_type"))
    );
}

#[test]
fn dm2_08_unregistered_relation_type_rejected() {
    let definition = RelationDefinition {
        relation_type: "owns".into(),
        allowed_subject_kinds: vec![RelationEndpointKind::Entity],
        allowed_object_kinds: vec![RelationEndpointKind::Fact],
    };

    let mut registry = RelationTypeRegistry::new();

    // 1. A registered relation type with compatible endpoints is accepted.
    registry.register(1, definition.clone()).unwrap();

    assert!(registry.contains_relation_type("owns"));
    assert_eq!(registry.version("owns"), Some(1));
    assert_eq!(registry.lookup("owns"), Some(&definition));

    let compatible = RelationExtension {
        subject: RelationEndpoint::Entity(EntityRef::new("entity-1").unwrap()),
        object: RelationEndpoint::Fact(FactRef::new("fact-1").unwrap()),
        directionality: RelationDirectionality::Directed,
        qualifiers: vec![],
        valid_time: Some(ValidTimeRef::Unknown),
        epistemic_status: EpistemicStatus::Observed,
        evidence_refs: vec![EvidenceRef::new("ev-1").unwrap()],
        lifecycle_state: RelationLifecycleState::Active,
        scope_refs: vec![],
    };

    assert_eq!(
        registry.validate_against_registry("owns", &compatible),
        Ok(())
    );

    // 2. An unregistered relation type is rejected.
    assert!(!registry.contains_relation_type("contains"));

    assert_eq!(
        registry.validate_against_registry("contains", &compatible),
        Err(DomainError::InvalidRelationEndpoint)
    );

    // 3. Registering the same relation type twice is rejected.
    let duplicate = RelationDefinition {
        relation_type: "owns".into(),
        allowed_subject_kinds: vec![RelationEndpointKind::Entity],
        allowed_object_kinds: vec![RelationEndpointKind::Entity],
    };

    assert_eq!(
        registry.register(2, duplicate),
        Err(DomainError::InvalidRelationEndpoint)
    );

    // 4. A registered relation type with incompatible endpoints is rejected.
    let incompatible = RelationExtension {
        subject: RelationEndpoint::Fact(FactRef::new("fact-2").unwrap()),
        ..compatible
    };

    assert_eq!(
        registry.validate_against_registry("owns", &incompatible),
        Err(DomainError::InvalidRelationEndpoint)
    );
}

// ---------------------------------------------------------------- DM2-09

#[test]
fn dm2_09_relation_time_scope_lifecycle_independent() {
    let scope_a = ScopeRef {
        scope_id: id("scope-a"),
        scope_kind: ScopeKind::Project,
        namespace_key: "namespace-a".into(),
    };
    let scope_b = ScopeRef {
        scope_id: id("scope-b"),
        scope_kind: ScopeKind::Session,
        namespace_key: "namespace-b".into(),
    };

    let base = RelationExtension {
        subject: RelationEndpoint::Entity(EntityRef::new("entity-1").unwrap()),
        object: RelationEndpoint::Fact(FactRef::new("fact-1").unwrap()),
        directionality: RelationDirectionality::Directed,
        qualifiers: vec![],
        valid_time: Some(ValidTimeRef::Unknown),
        epistemic_status: EpistemicStatus::Observed,
        evidence_refs: vec![EvidenceRef::new("ev-1").unwrap()],
        lifecycle_state: RelationLifecycleState::Proposed,
        scope_refs: vec![scope_a.clone()],
    };

    // 1. 只改变 valid_time。
    let time_changed = RelationExtension {
        valid_time: Some(ValidTimeRef::AllTime),
        ..base.clone()
    };

    assert_eq!(time_changed.valid_time, Some(ValidTimeRef::AllTime));
    assert_eq!(time_changed.scope_refs, base.scope_refs);
    assert_eq!(time_changed.lifecycle_state, base.lifecycle_state);

    // 2. 只改变 scope_refs。
    let scope_changed = RelationExtension {
        scope_refs: vec![scope_b.clone()],
        ..base.clone()
    };

    assert_eq!(scope_changed.scope_refs, vec![scope_b]);
    assert_eq!(scope_changed.valid_time, base.valid_time);
    assert_eq!(scope_changed.lifecycle_state, base.lifecycle_state);

    // 3. 只改变 lifecycle_state。
    let lifecycle_changed = RelationExtension {
        lifecycle_state: RelationLifecycleState::Active,
        ..base.clone()
    };

    assert_eq!(
        lifecycle_changed.lifecycle_state,
        RelationLifecycleState::Active
    );
    assert_eq!(lifecycle_changed.valid_time, base.valid_time);
    assert_eq!(lifecycle_changed.scope_refs, base.scope_refs);

    // 4. 生命周期状态与认知状态是不同类型（规格 §3.4：不是 MemoryLifecycle 或 Claim epistemic status）。
    let _: RelationLifecycleState = RelationLifecycleState::Proposed;
    let _: EpistemicStatus = EpistemicStatus::Observed;
}

// ---------------------------------------------------------------- DM2-10

#[test]
fn dm2_10_evidence_role_is_closed_to_four_allowed_values() {
    // role 只能是 supports / refutes / qualifies / context-only 四者之一。
    for role in ["Supports", "Refutes", "Qualifies", "ContextOnly"] {
        assert!(
            serde_json::from_value::<EvidenceRole>(json!(role)).is_ok(),
            "role {role} 应被接受"
        );
    }
    // 置信度、provenance 或其它拼写都不是合法 role。
    for bad in ["Confidence", "Provenance", "supports", "Supports ", ""] {
        assert!(
            serde_json::from_value::<EvidenceRole>(json!(bad)).is_err(),
            "role {bad:?} 不应被接受"
        );
    }
}

#[test]
fn dm2_10_evidence_availability_and_scope_enforced_independently() {
    let base = EvidenceExtension {
        evidence_ref: EvidenceRef::new("ev-1").unwrap(),
        kind: EvidenceKind::Document,
        source_ref: EvidenceSourceRef::External(ExternalSourceRef::new("source-1").unwrap()),
        locator: Some("doc://1".into()),
        observed_at: Some(TimeValue::Unknown),
        collector: ActorRef {
            actor_id: id("collector"),
        },
        integrity_digest: "sha256:abc".into(),
        availability: EvidenceAvailability::Available,
        scope_refs: vec![scope("s1")],
    };
    assert!(base.validate().is_ok());
    let restricted = EvidenceExtension {
        availability: EvidenceAvailability::Restricted,
        ..base.clone()
    };
    let forgotten = EvidenceExtension {
        availability: EvidenceAvailability::Forgotten,
        ..base.clone()
    };
    assert_ne!(restricted.availability, forgotten.availability);
    let no_scope = EvidenceExtension {
        scope_refs: vec![],
        ..base
    };
    assert_eq!(
        no_scope.validate(),
        Err(DomainError::EmptyRequiredField("scope_refs"))
    );
}

// ---------------------------------------------------------------- DM2-11

#[test]
#[ignore = "blocked: Provenance 当前字段仅为 provenance_id/source_refs/derivation_kind/actor_ref/created_at；没有 Provenance::validate、source_version_ref、parent_provenance_refs 或 unavailable_reason"]
fn dm2_11_provenance_lineage_or_unavailable_reason_mandatory() {
    unimplemented!()
}

// ---------------------------------------------------------------- DM2-12

#[test]
#[ignore = "blocked: 当前无 ProvenanceGraph / DerivationEdge 类型，也无 EvidenceIndependence::validate_independent 或 ancestry traversal API；不能判定两条 Evidence 是否共享祖先"]
fn dm2_12_shared_ancestry_not_independent_evidence() {
    unimplemented!()
}

// ---------------------------------------------------------------- DM2-13

#[test]
fn dm2_13_unknown_time_not_promoted() {
    let temporal = TemporalRef {
        occurred_at: TimeValue::Instant("2026-01-01T00:00:00Z".into()),
        valid_time: TimeValue::Unknown,
    };

    // 往返后 Unknown 仍是 Unknown：不得被反序列化成 Instant/Interval（"无始无终"）。
    let round: TemporalRef =
        serde_json::from_str(&serde_json::to_string(&temporal).unwrap()).unwrap();
    assert_eq!(round, temporal);
    assert_eq!(round.valid_time, TimeValue::Unknown);

    // 点断言保持点语义，不扩张为臆造的时长。
    match round.occurred_at {
        TimeValue::Instant(ref at) => assert_eq!(at, "2026-01-01T00:00:00Z"),
        ref other => panic!("point assertion 被扩张为 {other:?}"),
    }

    // 未知不等于空区间：二者必须是不同的值。
    assert_ne!(
        TimeValue::Unknown,
        TimeValue::Interval {
            start: String::new(),
            end: String::new()
        }
    );
}

// ---------------------------------------------------------------- DM2-14

/// Phase 1 `Claim` 的线格式快照。任何新增必填字段、改名或 deny_unknown_fields 都会让它反序列化失败。
const LEGACY_CLAIM_JSON: &str = r#"{
    "claim_id": "c1",
    "subject_ref": "s1",
    "predicate": "has_value",
    "object_value": "blue",
    "polarity": "affirm",
    "epistemic_status": "Observed",
    "confidence": null,
    "temporal_ref": null,
    "asserted_at": "2026-01-01T00:00:00Z",
    "scope_refs": [{"scope_id": "s1", "scope_kind": "User", "namespace_key": "user:s1"}],
    "qualifiers": [],
    "evidence_refs": ["ev-1"]
}"#;

#[test]
fn dm2_14_phase1_serialization_remains_compatible() {
    let claim: Claim = serde_json::from_str(LEGACY_CLAIM_JSON).unwrap();
    assert_eq!(claim.claim_id.as_str(), "c1");
    assert_eq!(claim.epistemic_status, EpistemicStatus::Observed);
    assert_eq!(claim.scope_refs.len(), 1);
    assert_eq!(claim.evidence_refs, vec![id("ev-1")]);

    // 往返稳定（序列化不丢字段、不引入新必填项）。
    let round: Claim = serde_json::from_str(&serde_json::to_string(&claim).unwrap()).unwrap();
    assert_eq!(round, claim);

    // 其余 Phase 1 核心类型同样保持可往返。
    let memory_version = MemoryVersion {
        memory_version_id: id("v1"),
        memory_id: id("m1"),
        version_number: 1,
        parent_version_id: None,
        created_at: "2026-01-01T00:00:00Z".into(),
        author_kind: "test".into(),
        change_reason: "initial".into(),
        claims: vec![claim],
        entity_refs: vec![id("e1")],
        relation_refs: vec![],
        source_refs: vec![id("src-1")],
        provenance_refs: vec![id("prov-1")],
        content_digest: "digest".into(),
        schema_version: "1".into(),
    };
    assert!(memory_version.validate().is_ok());
    assert_eq!(
        serde_json::from_str::<MemoryVersion>(&serde_json::to_string(&memory_version).unwrap())
            .unwrap(),
        memory_version
    );

    let event = Event {
        event_id: id("evt-1"),
        event_kind: "observation".into(),
        source_id: id("src-1"),
        recorded_at: "2026-01-01T00:00:00Z".into(),
        scope_refs: vec![scope("s1")],
        occurred_at: Some(TimeValue::Unknown),
        idempotency_key: None,
        payload_ref: "payload".into(),
        classification: "observed".into(),
        schema_version: "1".into(),
        retention_class: "default".into(),
    };
    assert_eq!(
        serde_json::from_str::<Event>(&serde_json::to_string(&event).unwrap()).unwrap(),
        event
    );

    let evidence = Evidence {
        evidence_id: id("ev-1"),
        source_ref: id("src-1"),
        recorded_at: "2026-01-01T00:00:00Z".into(),
        scope_refs: vec![scope("s1")],
        role: EvidenceRole::Supports,
    };
    assert_eq!(
        serde_json::from_str::<Evidence>(&serde_json::to_string(&evidence).unwrap()).unwrap(),
        evidence
    );

    let provenance = Provenance {
        provenance_id: id("prov-1"),
        source_refs: vec![id("src-1")],
        derivation_kind: "direct_capture".into(),
        actor_ref: ActorRef {
            actor_id: id("actor-1"),
        },
        created_at: "2026-01-01T00:00:00Z".into(),
    };
    assert_eq!(
        serde_json::from_str::<Provenance>(&serde_json::to_string(&provenance).unwrap()).unwrap(),
        provenance
    );

    let memory_source = MemorySource {
        memory_source_id: id("ms-1"),
        source_ref: id("src-1"),
        source_role: "primary".into(),
    };
    assert_eq!(
        serde_json::from_str::<MemorySource>(&serde_json::to_string(&memory_source).unwrap())
            .unwrap(),
        memory_source
    );
}
