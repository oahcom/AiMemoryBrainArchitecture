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

/// 空 OpaqueId 的元组字段是 crate 私有，集成测试只能经 serde 造出非法值。
fn empty_id() -> OpaqueId {
    serde_json::from_str("\"\"").unwrap()
}

fn with_empty_ref(value: serde_json::Value, field: &str) -> serde_json::Value {
    let mut value = value;
    value[field] = json!("");
    value
}

fn claim_revision(revision: &str, claim: &str, evidence: &[&str]) -> ClaimRevision {
    ClaimRevision {
        revision_ref: ClaimRevisionRef::new(id(revision)).unwrap(),
        claim_ref: ClaimRef::new(id(claim)).unwrap(),
        subject_ref: id("subject"),
        predicate: "has_value".into(),
        object_value: "blue".into(),
        polarity: "affirm".into(),
        asserted_at: "2026-01-01T00:00:00Z".into(),
        scope_refs: vec![scope("s1")],
        qualifiers: vec![],
        evidence_refs: evidence.iter().map(|e| id(e)).collect(),
    }
}

fn fact_revision() -> FactRevision {
    FactRevision {
        revision_ref: FactRevisionRef::new(id("fr-1")).unwrap(),
        fact_ref: FactRef::new(id("fact-1")).unwrap(),
        claim_revision_ref: ClaimRevisionRef::new(id("cr-1")).unwrap(),
        evidence_refs: vec![id("ev-1")],
        provenance_refs: vec![id("prov-1")],
        scope_refs: vec![scope("s1")],
        attestor_ref: id("attestor-1"),
        method: "independent_review".into(),
        method_version: "1.0".into(),
        authorization_decision_ref: id("authz-1"),
        established_at: "2026-01-02T00:00:00Z".into(),
    }
}

// ---------------------------------------------------------------- DM2-01

#[test]
fn dm2_01_stable_claim_ref_across_revisions() {
    // 证据变化（CI-09）→ 新 revision，ClaimRef 必须不变。
    let first = claim_revision("cr-1", "claim-1", &["ev-1"]);
    let second = claim_revision("cr-2", "claim-1", &["ev-1", "ev-2"]);

    assert!(first.validate().is_ok());
    assert!(second.validate().is_ok());
    assert_eq!(first.claim_ref, second.claim_ref);
    assert_ne!(first.revision_ref, second.revision_ref);

    // 修订是追加而非覆盖：旧 revision 的证据集合原样保留。
    assert_eq!(first.evidence_refs, vec![id("ev-1")]);
    assert_eq!(second.evidence_refs.len(), 2);

    // 校验必须拒绝空 revision_ref，而不是静默接受一个不可引用的 revision。
    let broken: ClaimRevision = serde_json::from_value(with_empty_ref(
        serde_json::to_value(&first).unwrap(),
        "revision_ref",
    ))
    .unwrap();
    assert_eq!(broken.validate(), Err(DomainError::EmptyId));

    // 校验必须拒绝空 scope 集合。
    let mut no_scope = first.clone();
    no_scope.scope_refs.clear();
    assert_eq!(
        no_scope.validate(),
        Err(DomainError::EmptyRequiredField("scope_refs"))
    );
}

#[test]
#[ignore = "blocked: 没有 revision registry / append-only store，ClaimRevisionRef 的全局唯一性与复用检测属于 D 的 canonical 存储语义 (B-P2-XO-02)，domain 层无处表达"]
fn dm2_01_claim_revision_ref_uniqueness_enforced() {
    unimplemented!()
}

// ---------------------------------------------------------------- DM2-02

#[test]
#[ignore = "blocked: ClaimRevision 没有 parent_revision_ref 字段，无法表达「非初始 revision 恰有一个同 ClaimRef 父节点、初始 revision 无父」"]
fn dm2_02_revision_parent_mismatch_rejected() {
    unimplemented!()
}

#[test]
#[ignore = "blocked: 没有 accepted/immutable 状态表示，也没有可变路径；不可变性由 &self 与无 setter 在编译期保证，运行时无可观测的失败模式"]
fn dm2_02_accepted_revision_is_append_only() {
    unimplemented!()
}

// ---------------------------------------------------------------- DM2-03

#[test]
#[ignore = "blocked: 没有 CI-01..CI-13 分类器（无 classify API、DomainError 无 AmbiguousIdentityClassification 变体）；实现分类属于 Phase 2 实现授权范围，契约 §7 明确未冻结"]
fn dm2_03_ci_classification_vectors() {
    unimplemented!()
}

// ---------------------------------------------------------------- DM2-04

#[test]
fn dm2_04_fact_pins_exact_claim_revision_not_head() {
    // claim-1 已有更新的 head (cr-2)，但 FactRevision 仍精确指向旧 revision cr-1。
    let head = claim_revision("cr-2", "claim-1", &["ev-2"]);
    let pinned_old = claim_revision("cr-1", "claim-1", &["ev-1"]);

    let mut fact = fact_revision();
    fact.claim_revision_ref = pinned_old.revision_ref.clone();
    assert!(fact.validate().is_ok());

    assert_eq!(fact.claim_revision_ref, pinned_old.revision_ref);
    assert_ne!(fact.claim_revision_ref, head.revision_ref);

    // 序列化往返不得把精确引用"升级"为 head。
    let round: FactRevision =
        serde_json::from_str(&serde_json::to_string(&fact).unwrap()).unwrap();
    assert_eq!(round.claim_revision_ref.as_str(), "cr-1");

    // 空的精确引用必须被拒绝，不得被解释为"取当前 head"。
    let broken: FactRevision = serde_json::from_value(with_empty_ref(
        serde_json::to_value(&fact).unwrap(),
        "claim_revision_ref",
    ))
    .unwrap();
    assert_eq!(broken.validate(), Err(DomainError::EmptyId));
}

#[test]
#[ignore = "blocked: 没有 ClaimRef -> ClaimRevision 的解析 API，无法证明解析器拒绝 head 替换（只能证明值类型保存了精确引用）"]
fn dm2_04_resolution_rejects_claim_head_substitution() {
    unimplemented!()
}

// ---------------------------------------------------------------- DM2-05

#[test]
fn dm2_05_fact_identity_distinct_and_pins_exact_refs() {
    let fact = fact_revision();
    assert!(fact.validate().is_ok());

    // Fact 身份独立于它引用的 ClaimRevision：换 pin 不改 FactRef。
    let mut repinned = fact.clone();
    repinned.claim_revision_ref = ClaimRevisionRef::new(id("cr-other")).unwrap();
    assert_eq!(repinned.fact_ref, fact.fact_ref);
    assert_ne!(repinned.claim_revision_ref, fact.claim_revision_ref);

    // Evidence 必须非空且精确。
    let mut no_evidence = fact.clone();
    no_evidence.evidence_refs.clear();
    assert_eq!(
        no_evidence.validate(),
        Err(DomainError::EmptyRequiredField("evidence_refs"))
    );

    // Provenance 必须非空且精确。
    let mut no_provenance = fact.clone();
    no_provenance.provenance_refs.clear();
    assert_eq!(
        no_provenance.validate(),
        Err(DomainError::EmptyRequiredField("provenance_refs"))
    );

    let mut empty_evidence = fact.clone();
    empty_evidence.evidence_refs = vec![empty_id()];
    assert_eq!(empty_evidence.validate(), Err(DomainError::EmptyId));

    let mut empty_provenance = fact.clone();
    empty_provenance.provenance_refs = vec![empty_id()];
    assert_eq!(empty_provenance.validate(), Err(DomainError::EmptyId));
}

// ---------------------------------------------------------------- DM2-06

#[test]
fn dm2_06_missing_authorization_ref_blocks_fact_publication() {
    let fact = fact_revision();
    assert!(fact.validate().is_ok());

    // 缺失 I 授权决策引用 → 不可进入 canonical 发布。
    let mut missing = fact.clone();
    missing.authorization_decision_ref = empty_id();
    assert_eq!(missing.validate(), Err(DomainError::EmptyId));

    // 有引用即可通过 domain 校验；引用在 I 语义上是否有效属 B-P2-XO-01 未冻结范围。
    let mut present = fact.clone();
    present.authorization_decision_ref = id("authz-2");
    assert!(present.validate().is_ok());
}

// ---------------------------------------------------------------- DM2-07

#[test]
#[ignore = "blocked: Entity 只有 entity_id/entity_type/canonical_label/scope_refs，没有 alias、identity status、merge/split lineage 字段，也没有身份解析 API；「标签相同不合并身份」在当前模型中无任何可失败路径"]
fn dm2_07_label_alias_does_not_merge_identity() {
    unimplemented!()
}

// ---------------------------------------------------------------- DM2-08

#[test]
#[ignore = "blocked: Relation 的端点是无类型 OpaqueId、relation_type 是裸 String、没有 Relation::validate 也没有关系词汇表 registry，无法表达「端点类型不被关系定义允许」与「未注册关系类型」"]
fn dm2_08_invalid_relation_endpoint_and_unregistered_type_rejected() {
    unimplemented!()
}

// ---------------------------------------------------------------- DM2-09

#[test]
#[ignore = "blocked: Relation 只有 relation_type/端点/scope_refs，没有 valid time、epistemic status、relation lifecycle 字段，三个维度无法在模型中区分"]
fn dm2_09_relation_time_scope_lifecycle_independent() {
    unimplemented!()
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
#[ignore = "blocked: Evidence 没有 availability 字段、没有 kind/collector/integrity，也没有 Evidence::validate；「至少一个 ScopeRef」「availability 显式表示」均无法校验"]
fn dm2_10_evidence_availability_and_scope_enforced_independently() {
    unimplemented!()
}

// ---------------------------------------------------------------- DM2-11

#[test]
#[ignore = "blocked: Provenance 只有 provenance_id/source_refs/derivation_kind/actor_ref/created_at，没有 Provenance::validate、没有 source version、没有 parent lineage、没有 unavailable reason 字段"]
fn dm2_11_provenance_lineage_or_unavailable_reason_mandatory() {
    unimplemented!()
}

// ---------------------------------------------------------------- DM2-12

#[test]
#[ignore = "blocked: 没有 ancestry/derivation graph 结构，也没有 Evidence 去重或独立性判定 API，无法表达「共同祖先的重复派生不构成独立佐证」"]
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
        actor_ref: ActorRef { actor_id: id("actor-1") },
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
