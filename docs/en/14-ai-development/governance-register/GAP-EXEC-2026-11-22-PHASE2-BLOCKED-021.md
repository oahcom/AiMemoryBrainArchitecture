# GAP-EXEC-2026-11-22-PHASE2-BLOCKED-021

**Register**: GAP-EXEC-2026-11-22-PHASE2-BLOCKED-021
**Nature**: MEASUREMENT_ONLY / TEST_DRAFT_ONLY / NO_IMPLEMENTATION / REQUIRES_INDEPENDENT_REVIEW
**Measured at**: `main = dba34a35` (`CC=zigcc AR=zigar cargo test --workspace --all-targets` → 438 passed / 0 failed / 9 ignored)
**Date**: 2026-11-22
**Author**: coordination session (not an independent reviewer)

---

## 0. What this register is for

The claim "Phase 2/3 domain model: 100% not started" is false, but the way it is
false is worth recording precisely: Phase 2 has **11 acceptance dimensions that
genuinely pass** and **9 that are held behind `#[ignore]`**, each naming the API
it is missing.

That is not "not started". It is "specification written, acceptance written,
implementation not written". The two advance in completely different ways: the
first needs a spec, the second needs an API added against a list.

This register does three things:

1. re-verifies all 9 ignore reasons by measurement (which still hold, which are
   stale);
2. expands each missing API into a decidable gap entry (input, output, refusal
   conditions);
3. gives each a **test draft**, so the implementer does not have to design the
   acceptance after landing the code.

Boundary: **this register contains no implementation code** and does not modify
`phase2_acceptance.rs`. The drafts are prose and pseudocode; the author may adopt
or rewrite them.

---

## 1. Re-verification: 1 stale, 8 hold

### 1.1 `dm2_03`'s ignore reason is false

`#545` (`444deef1`) added `crates/memory-domain/src/claim_identity.rs`, re-exported
via `pub use claim_identity::*` at `lib.rs:7`. It provides exactly the function the
ignore reason says does not exist:

```rust
pub fn classify(prior: &ClaimRevision, candidate: &ClaimRevision) -> ClaimIdentityDecision
```

```
$ cargo test -p memory-domain --lib claim_identity
test result: ok. 19 passed; 0 failed; 0 ignored
```

19 tests cover CI-01, CI-02, CI-03, CI-04, CI-07, CI-08, CI-09, CI-10, CI-11, CI-13,
plus label-only, qualifier ambiguity, multi-dimension ambiguity, scope ambiguity,
cross-Claim, no-fallback, and determinism.

**But `dm2_03` cannot simply drop the ignore**: its body is `unimplemented!()` and
was never written against `classify()`. So this is an **acceptance-file defect**,
not a domain-crate defect.

`CI-05` / `CI-06` / `CI-12` are recorded in the module header as **unreachable**
(`ClaimRevision` has no quantifier, modality or confidence field), not missing.
`SubstantiveQualifier` is the same: the spec's test is semantic, so the
implementation can only report ambiguity. Those three plus `SubstantiveQualifier`
are **structurally unreachable** and must not be counted as gaps.

### 1.2 The other 8, measured one by one

| test | probed symbol | hits in `crates/` | verdict |
|---|---|---:|---|
| `dm2_01` | `ClaimRevisionRegistry`, `register_revision` | 0 | holds |
| `dm2_02` | `AcceptedRevisionState` | 0 | holds |
| `dm2_04` | `ClaimRevisionResolver`, `resolve_claim_head` | 0 | holds |
| `dm2_06` | validated `AuthorizationDecisionRef` | only `pending_i()` | holds |
| `dm2_08` | `RelationTypeRegistry`, `contains_relation_type` | 0 | holds |
| `dm2_09` | `RelationExtension.scope_refs` | struct has no such field | holds |
| `dm2_11` | `Provenance::validate`, `parent_provenance_refs`, `unavailable_reason` | 0 | holds |
| `dm2_12` | `ProvenanceGraph`, `DerivationEdge`, `validate_independent` | 0 | holds |

Corroboration (fields measured in `memory-domain/src/lib.rs`):

```
RelationExtension { subject, object, directionality, qualifiers, valid_time,
                    epistemic_status, evidence_refs, lifecycle_state }
                    <- no scope_refs

Provenance { provenance_id, source_refs, derivation_kind, actor_ref, created_at }
                    <- no source_version_ref / parent_provenance_refs / unavailable_reason
```

Both reasons are accurate.

---

## 2. Gap entries (decidable form)

Each gives: **gap ID / required capability / criterion / refusal condition / dependency**.

### G2-01 — Claim revision uniqueness registry

- **Capability**: cross-revision uniqueness check on `ClaimRevisionRef`.
  `ClaimRevision::validate` checks one value; it cannot detect two revisions using
  the same ID.
- **Criterion**: `register_revision(&mut self, rev: &ClaimRevision) -> Result<(), DomainError>`;
  a second registration of the same `revision_ref` returns `Err`.
- **Refusal**: duplicate `revision_ref`; empty `revision_ref` (already `EmptyId`).
- **Dependency**: none. Pure in-memory, no I/O.

### G2-02 — Accepted-state append-only transition

- **Capability**: distinguish "immutable value" from "not revertible once accepted".
  Only the former exists.
- **Criterion**: state machine `Draft → Accepted` with no out-edge from `Accepted`;
  any transition applied to `Accepted` returns `Err`.
- **Refusal**: `Accepted → Draft`; `Accepted → Accepted` (double accept).
- **Dependency**: none.

### G2-03 — Align the acceptance test with the classifier that already exists (**not a gap, a repair**)

- **Capability**: already present (`classify()`).
- **What is needed**: replace `dm2_03`'s `unimplemented!()` with vector assertions
  against `classify()`, and remove the ignore.
- **Criterion**: 10 of the 13 CIs are reachable (CI-05/06/12 are not), plus the 4
  ambiguity rules.
- **Note**: this is the only entry that **needs no new production API**. It can be
  done at any time by anyone, with no authority decision.
- **Dependency**: none.

### G2-04 — Resolver rejects head substitution

- **Capability**: `FactRevision` already stores an exact `ClaimRevisionRef`, but
  there is no resolver, so "resolution must not upgrade an exact ref to head"
  cannot be proven.
- **Criterion**: `resolve_revision(&self, r: &ClaimRevisionRef) -> Result<&ClaimRevision, _>`;
  when the caller passes the head but the pin is an older revision, the pinned one
  must be returned, never the head.
- **Refusal**: pinned revision absent; pin and head disagree while the caller asks
  for head.
- **Dependency**: G2-01 (a registry is needed to resolve by ID).

### G2-06 — A missing authorization must block Fact publication

- **Capability**: `FactRevision::initial` requires `AuthorizationDecisionRef`, but
  the only public constructor is `pending_i()`, and the type has no "absent" and no
  "validated" state.
- **Criterion**: `AuthorizationDecisionRef` has at least three states
  `Absent` / `Pending` / `Validated`; `FactRevision::validate` returns `Err` on the
  first two.
- **Refusal**: `Absent`, `Pending`.
- **Known conflict**: `fact_with_placeholder_attestor_validates_today` pins the fact
  that "the current placeholder passes". That test must change with this entry, or
  the new criterion and the old test are mutually exclusive.
- **Dependency**: **authority I**. The doc comment on `pending_i()` states it
  "closes only when I defines the contract". This is the only entry hard-blocked by
  an external decision.

### G2-08 — Relation type registry

- **Capability**: `RelationDefinition` describes the allowed endpoints of a single
  `relation_type`, but there is no registry, so a non-empty `relation_type` cannot
  be judged as registered or not.
- **Criterion**: `contains_relation_type(&self, t: &str) -> bool`;
  `RelationExtension::validate` returns `Err` on an unregistered type.
- **Refusal**: an unregistered `relation_type` (non-empty but not in the table).
- **Dependency**: none.

### G2-09 — Time / scope / lifecycle independence

- **Capability**: `RelationExtension` has `valid_time`, `epistemic_status`,
  `lifecycle_state` and no `scope_refs`, so the three cannot be asserted independent.
- **Criterion**: add `scope_refs: Vec<ScopeRef>`; construct three instances each
  changing one dimension, assert the other two are unchanged and `validate()` passes
  for all three.
- **Refusal**: empty `scope_refs` (consistent with `ClaimRevision`'s
  `EmptyRequiredField`).
- **Dependency**: none, but **it is a breaking change**: every `RelationExtension`
  construction site must be updated. The number of sites must be counted before
  implementation.

### G2-11 — Provenance lineage or unavailable reason, one of the two

- **Capability**: `Provenance` has only `provenance_id / source_refs / derivation_kind /
  actor_ref / created_at`. No `source_version_ref`, no `parent_provenance_refs`, no
  `unavailable_reason`, no `validate`.
- **Criterion**: `Provenance::validate` requires either a non-empty
  `parent_provenance_refs` or a non-empty `unavailable_reason`; both empty returns
  `Err`.
- **Refusal**: both empty; both non-empty (mutually exclusive, so a record cannot
  claim lineage and unavailability at once).
- **Dependency**: none.

### G2-12 — Shared ancestry is not independent evidence

- **Capability**: no `ProvenanceGraph` / `DerivationEdge`, so two Evidence records
  cannot be judged as sharing an ancestor.
- **Criterion**: `EvidenceIndependence::validate_independent(&graph, a, b)` returns
  `Err` when a and b share any ancestor.
- **Refusal**: direct shared parent; indirect shared ancestor (transitive closure);
  reflexivity (a against a).
- **Dependency**: G2-11 (the parent edges are needed to build the graph).

---

## 3. Dependency order

```
G2-03  (no dependency, test-only repair)   <- do now, blocks nobody
G2-01  (no dependency)
G2-02  (no dependency)
G2-08  (no dependency)
G2-09  (no dependency, but breaking)
G2-11  (no dependency)
   +-> G2-12  (needs G2-11's parent edges)
G2-04  (needs G2-01)
G2-06  (blocked by authority I)            <- the only hard block
```

**7 of 8 need no external decision at all.** Only `G2-06` needs I to issue the
`AuthorizationDecisionRef` contract. This is the second reason "Phase 2 not started"
is the wrong frame: the doable part is 7/8.

---

## 4. Test drafts

The drafts state **criteria** and **minimum construction**, not implementation.
Once the API lands, the implementer can adopt them directly.

### 4.1 G2-03 (the only draft executable today)

```rust
#[test]
fn dm2_03_ci_classification_vectors() {
    // Reachable dimension: change one field, assert the classification.
    let base = claim_revision("cr-1", "claim-1", &["ev-1"]);

    // CI-01 subject referent
    let mut other_subject = base.clone();
    other_subject.subject = "different".into();
    assert_eq!(
        classify(&base, &other_subject),
        ClaimIdentityDecision::Classified {
            class: ClaimIdentityClass::NewClaim,
            dimension: ChangeDimension::SubjectReferent,
        }
    );

    // CI-09 evidence reordering does not change identity
    let mut reordered = base.clone();
    reordered.evidence_refs.reverse();
    assert_eq!(
        classify(&base, &reordered),
        ClaimIdentityDecision::Classified {
            class: ClaimIdentityClass::NewRevision,
            dimension: ChangeDimension::PresentationOnly,
        }
    );

    // An unreachable dimension must surface as ambiguity, never as NewRevision
    let mut qualifier = base.clone();
    qualifier.qualifiers = vec!["most".into()];
    assert!(matches!(
        classify(&base, &qualifier),
        ClaimIdentityDecision::RequiresGovernedDecision { .. }
    ));
}
```

**Note**: whether field assignment compiles depends on `ClaimRevision` field
visibility. If the fields are private, the draft must be rewritten to construct via
`successor()`. That is an implementation detail, not a criterion question.

### 4.2 G2-01

```rust
#[test]
fn dm2_01_claim_revision_ref_uniqueness_enforced() {
    let mut registry = ClaimRevisionRegistry::new();
    let first = claim_revision("cr-dup", "claim-1", &["ev-1"]);
    let second = claim_revision("cr-dup", "claim-2", &["ev-2"]);

    assert!(registry.register_revision(&first).is_ok());
    assert_eq!(
        registry.register_revision(&second),
        Err(DomainError::DuplicateRevisionRef)
    );
    // A rejected registration must not pollute the registry
    assert!(registry.get(second.revision_ref()).is_none());
}
```

The last line is the **critical assertion**: after a refusal the registry must still
be in its prior state, otherwise the refusal is cosmetic.

### 4.3 G2-02

```rust
#[test]
fn dm2_02_accepted_revision_is_append_only() {
    let mut state = AcceptedRevisionState::draft(claim_revision("cr-1", "claim-1", &["ev-1"]));

    assert!(state.accept().is_ok());
    assert_eq!(state.current(), AcceptedRevisionState::Accepted);

    // no out-edge
    assert!(state.accept().is_err());
    assert!(state.revert().is_err());
    // state unchanged after refusal
    assert_eq!(state.current(), AcceptedRevisionState::Accepted);
}
```

### 4.4 G2-04

```rust
#[test]
fn dm2_04_resolution_rejects_claim_head_substitution() {
    let mut resolver = ClaimRevisionResolver::new();
    resolver.insert(claim_revision("cr-1", "claim-1", &["ev-1"]));
    resolver.insert(claim_revision("cr-2", "claim-1", &["ev-2"])); // head

    let pinned = ClaimRevisionRef::new("cr-1").unwrap();
    let resolved = resolver.resolve_revision(&pinned).unwrap();

    assert_eq!(resolved.revision_ref().as_str(), "cr-1");
    assert_ne!(resolved.revision_ref(), resolver.head_of(ClaimRef::new("claim-1").unwrap()));
}
```

### 4.5 G2-08

```rust
#[test]
fn dm2_08_unregistered_relation_type_rejected() {
    let mut registry = RelationTypeRegistry::new();
    registry.register(RelationDefinition { relation_type: "causes".into(), ..default() });

    assert!(registry.contains_relation_type("causes"));
    assert!(!registry.contains_relation_type("implies"));

    let mut rel = relation_extension("implies");
    assert_eq!(rel.validate(&registry), Err(DomainError::UnregisteredRelationType));
}
```

### 4.6 G2-09

```rust
#[test]
fn dm2_09_relation_time_scope_lifecycle_independent() {
    let base = relation_extension_full();

    let mut time_changed = base.clone();
    time_changed.valid_time = Some(ValidTimeRef::new("2026-06-01T00:00:00Z").unwrap());
    assert_eq!(time_changed.scope_refs, base.scope_refs);
    assert_eq!(time_changed.lifecycle_state, base.lifecycle_state);

    let mut scope_changed = base.clone();
    scope_changed.scope_refs = vec![scope("s2")];
    assert_eq!(scope_changed.valid_time, base.valid_time);
    assert_eq!(scope_changed.lifecycle_state, base.lifecycle_state);

    let mut lifecycle_changed = base.clone();
    lifecycle_changed.lifecycle_state = RelationLifecycleState::Retired;
    assert_eq!(lifecycle_changed.valid_time, base.valid_time);
    assert_eq!(lifecycle_changed.scope_refs, base.scope_refs);

    for r in [&time_changed, &scope_changed, &lifecycle_changed] {
        assert!(r.validate().is_ok());
    }
}
```

All three assertion groups must be present. Asserting one is the usual way to fake
this: proving "it can change" is not proving "it is independent".

### 4.7 G2-11

```rust
#[test]
fn dm2_11_provenance_lineage_or_unavailable_reason_mandatory() {
    // both empty -> refuse
    let bare = Provenance { parent_provenance_refs: vec![], unavailable_reason: None, ..base() };
    assert_eq!(bare.validate(), Err(DomainError::ProvenanceLineageUnaccounted));

    // lineage only -> pass
    let with_parent = Provenance { parent_provenance_refs: vec![prov("p1")], ..base() };
    assert!(with_parent.validate().is_ok());

    // reason only -> pass
    let with_reason = Provenance { unavailable_reason: Some("source purged".into()), ..base() };
    assert!(with_reason.validate().is_ok());

    // both -> refuse (mutually exclusive)
    let both = Provenance {
        parent_provenance_refs: vec![prov("p1")],
        unavailable_reason: Some("source purged".into()),
        ..base()
    };
    assert_eq!(both.validate(), Err(DomainError::ProvenanceLineageAmbiguous));
}
```

### 4.8 G2-12

```rust
#[test]
fn dm2_12_shared_ancestry_not_independent_evidence() {
    // graph: root <- a, root <- b   (a and b share an ancestor)
    let mut graph = ProvenanceGraph::new();
    graph.add(DerivationEdge::new(prov("root"), prov("a")));
    graph.add(DerivationEdge::new(prov("root"), prov("b")));

    assert_eq!(
        EvidenceIndependence::validate_independent(&graph, prov("a"), prov("b")),
        Err(DomainError::SharedAncestry { ancestor: prov("root") })
    );

    // independent branch
    graph.add(DerivationEdge::new(prov("root2"), prov("c")));
    assert!(EvidenceIndependence::validate_independent(&graph, prov("a"), prov("c")).is_ok());

    // reflexive
    assert!(EvidenceIndependence::validate_independent(&graph, prov("a"), prov("a")).is_err());
}
```

**Note**: the error must carry `ancestor`, otherwise the caller cannot explain why
independence failed. An implementation returning only a bool does not meet the
criterion.

---

## 5. What this register does not do

- does not modify `phase2_acceptance.rs`;
- does not add production code;
- does not claim any entry is "implemented";
- does not claim to be an independent review — the author is a coordination
  session, not an independent reviewer;
- does not decide the shape of the I contract for `G2-06` (that is authority I's
  call).

## 6. Re-verification checklist (for a later session to re-derive rather than inherit)

```sh
# 1. ignore count and reasons
grep -n "#\[ignore" crates/memory-domain/tests/phase2_acceptance.rs

# 2. whether each missing API now exists
for s in ClaimRevisionRegistry AcceptedRevisionState ClaimRevisionResolver \
         resolve_claim_head RelationTypeRegistry contains_relation_type \
         ProvenanceGraph DerivationEdge validate_independent; do
  printf '%s %s\n' "$(grep -rc "$s" --include=*.rs crates/ 2>/dev/null | \
    awk -F: '{n+=$2}END{print n+0}')" "$s"
done

# 3. whether the classifier still exists and passes
cargo test -p memory-domain --lib claim_identity

# 4. full run
CC=zigcc AR=zigar cargo test --workspace --all-targets
```

Any non-zero value in step 2 means that entry's ignore reason needs re-checking —
which is exactly how `dm2_03` was found.
