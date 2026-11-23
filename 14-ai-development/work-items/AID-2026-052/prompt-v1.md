---
document_metadata:
  domain: ai-development
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "Every claim in §2 was read at main 13c6d95d in this session: Provenance's nine fields and validate()'s full body from crates/memory-domain/src/lib.rs; the OpaqueId newtype and its derived Deserialize from the same file; the ref_ctor! macro that generates ProvenanceRef::validate; EvidenceExtension::validate's element-by-element revalidation and its comment naming the serde bypass; and the existing provenance_with(field, replacement) serde helper at phase2_acceptance.rs:977."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative

  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# TASK — revalidate the four Provenance reference fields so a deserialized record cannot bypass the constructor

`main` is at `13c6d95d`.

`Provenance::validate()` checks lengths and presence. It does not check the *contents* of a single
reference. `OpaqueId` derives `Deserialize` on a tuple struct, so `""` deserializes into an id that
`OpaqueId::new` would have rejected. The sibling type `EvidenceExtension` already revalidates every
reference element by element and says why in a comment. `Provenance` never got the same treatment.

That is the whole of `GOV-NC-2026-11-22-PROVENANCE-REFERENCE-REVALIDATION-027`.

---

## 1. Hard constraints

**#0 — The sibling type is the specification.** `EvidenceExtension::validate()` in
`crates/memory-domain/src/lib.rs` is the pattern to follow, including its comment about serde
bypassing constructors. Do not invent a different validation style for `Provenance`; two
revalidation idioms in one crate is a new defect, not a fix.

**#1 — Do not change `Provenance`'s field types or field order.** `source_refs` and
`source_version_refs` are `Vec<OpaqueId>` and must stay that way. Changing them to `TypedObjectRef`
is a different register (`GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026` §6.5, ruled in
`OWNER-DECISION-TYPED-OBJECT-REF-001`) and is explicitly out of scope here.

**#2 — Do not make `OpaqueId`'s `Deserialize` strict.** A custom `Deserialize` impl that rejects
empty ids on the way in would fix this symptom by changing the serialization contract for every type
in the crate — thirty-odd call sites and every fixture. Validate at the point of use, as
`EvidenceExtension` does. The serde-bypass test must still be able to *construct* the bad value;
that is what makes it a test.

**#3 — Do not break the eight mutations `dm2_11` already asserts.** That test pins the
lineage-or-reason rule across eight cases. Your change adds checks; it must not reorder them in a way
that changes which error a currently-passing case returns.

**#4 — `ProvenanceGraph::add` must reject before mutating.** It already calls `provenance.validate()?`
before touching `self`, and works on a clone. Keep that property and prove it: a refused insert must
leave the graph unchanged.

**#5 — Report only commands you actually ran, with real output and real exit codes.** `NOT RUN` is a
valid answer. Do not report a green suite you did not observe.

**#6 — Do not run the full workspace suite as your evidence.** `cargo test -p memory-domain` is
enough. The repository's CI runs the workspace; a local 3 GB `target/` is not a contribution.

---

## 2. Measured state at `13c6d95d`

`Provenance`, from `crates/memory-domain/src/lib.rs`:

```rust
pub struct Provenance {
    pub provenance_id: OpaqueId,
    pub source_refs: Vec<OpaqueId>,              // field 1 of the four
    pub derivation_kind: String,
    pub actor_ref: ActorRef,                     // field 3, via actor_ref.actor_id
    pub created_at: String,
    pub source_version_refs: Vec<OpaqueId>,      // field 2
    pub parent_provenance_refs: Vec<ProvenanceRef>, // field 4
    pub unavailable_reason: Option<String>,
    pub method_version: Option<String>,
}
```

`validate()` in full — note that it checks `source_refs` for *emptiness of the vector* and
`source_version_refs` for *length agreement*, and never inspects an element:

```rust
pub fn validate(&self) -> Result<(), DomainError> {
    if self.provenance_id.as_str().is_empty() {
        return Err(DomainError::EmptyId);
    }
    for (field, value) in [
        ("derivation_kind", &self.derivation_kind),
        ("created_at", &self.created_at),
    ] {
        if value.is_empty() {
            return Err(DomainError::EmptyRequiredField(field));
        }
    }
    if self.source_refs.is_empty() {
        return Err(DomainError::EmptyRequiredField("source_refs"));
    }
    if self.unavailable_reason.as_deref().is_some_and(|r| r.trim().is_empty()) {
        return Err(DomainError::EmptyRequiredField("unavailable_reason"));
    }
    if self.parent_provenance_refs.is_empty() && self.unavailable_reason.is_none() {
        return Err(DomainError::IncompleteProvenanceLineage);
    }
    if !self.source_version_refs.is_empty()
        && self.source_version_refs.len() != self.source_refs.len()
    {
        return Err(DomainError::InvalidVersionNumber);
    }
    Ok(())
}
```

The bypass, from the same file:

```rust
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct OpaqueId(String);   // Deserialize writes straight into the field; new() is not called
```

`ProvenanceRef` and its siblings come from a macro, and **each already has a `validate()`**:

```rust
ref_ctor!(ClaimRef, ClaimRevisionRef, FactRef, FactRevisionRef, EvidenceRef, ProvenanceRef);
// generates: pub fn validate(&self) -> Result<(), DomainError>
```

So field 4 has a per-element validator available today. Fields 1 and 2 are bare `OpaqueId`, which
has no `validate()` — `EvidenceExtension` handles the same situation with an inline
`as_str().is_empty()` check. Field 3 is the same pattern on `actor_ref.actor_id`.

The precedent, `EvidenceExtension::validate()`:

```rust
/// Every reference is re-validated even though the constructors reject
/// empty values, because serde derives `Deserialize` for these types and
/// bypasses the constructors: a payload can carry `""` straight into a
/// field that no constructor would ever have produced.
pub fn validate(&self) -> Result<(), DomainError> {
    self.evidence_ref.validate()?;
    match &self.source_ref {
        EvidenceSourceRef::Event(r) => r.validate()?,
        EvidenceSourceRef::Memory(r) => r.validate()?,
        EvidenceSourceRef::External(r) => r.validate()?,
    }
    if self.collector.actor_id.as_str().is_empty() { return Err(DomainError::EmptyId); }
    ...
}
```

The test scaffolding already exists. `crates/memory-domain/tests/phase2_acceptance.rs:977`:

```rust
fn provenance_with(field: &str, replacement: serde_json::Value) -> Provenance {
    let mut value = json!({ ... all nine fields ... });
    value[field] = replacement;
    serde_json::from_value(value).unwrap()
}
```

It is local to `dm2_11`. It injects by field name through `serde_json`, which is exactly how an
illegal reference must be constructed — do not build the bad values with struct literals, because a
struct literal that reaches an empty `OpaqueId` has to go through a helper that may itself validate,
and then you are testing your helper.

---

## 3. The work

Extend `Provenance::validate()` to revalidate all four reference groups, in the
`EvidenceExtension` idiom:

1. every element of `source_refs` — reject empty;
2. every element of `source_version_refs` — reject empty;
3. `actor_ref.actor_id` — reject empty;
4. every element of `parent_provenance_refs` — call its existing `validate()`.

Preserve every existing check and the order that `dm2_11`'s eight mutations depend on. The
positional-length rule for `source_version_refs` stays; per-element checks are additional, not a
replacement.

Then add acceptance tests. They belong beside `dm2_11` in `phase2_acceptance.rs`, and they must
prove *both* halves of each case:

| test | direct `validate()` | `ProvenanceGraph::add` |
|---|---|---|
| empty element in `source_refs` | rejects | rejects |
| empty element in `source_version_refs` | rejects | rejects |
| empty `actor_ref.actor_id` | rejects | rejects |
| empty `parent_provenance_refs` element | rejects | rejects |
| valid record | accepts | inserts |

And one graph-integrity test: after a refused insert, the graph is unchanged — the same identity
inserts cleanly afterwards, and `ancestors()` still returns what it did before.

---

## 4. Acceptance criteria

1. All four reference groups are revalidated, one test per group, named so a reader can map test to
   group without reading the body.
2. Each test constructs its illegal value **through `serde_json`**, not through a constructor.
3. Each illegal value is rejected by `Provenance::validate()` **and** by `ProvenanceGraph::add`.
4. A refused `add` leaves the graph unchanged, proven by re-inserting the same identity successfully
   and by an `ancestors()` comparison.
5. `dm2_11` still passes with all eight mutations unchanged.
6. Existing valid `Provenance` fixtures still validate; no fixture needs editing to pass.
7. `cargo test -p memory-domain` passes; state the passed/failed/ignored counts you observed.
8. `cargo fmt --check` and `cargo clippy -p memory-domain` clean.
9. `git diff` shows no change to `OpaqueId`'s derives and no change to any field type.

---

## 5. What this does not close

`GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026` §6.5 asks whether `Evidence.source_ref` and
`EvidenceExtension.source_ref` are equivalent. That is ruled separately and is not touched here:
this work does not make the two fields conform to `TypedObjectRef`, and it must not add an
equality check between them. See `OWNER-DECISION-TYPED-OBJECT-REF-001`.

The register's closing condition also asks that the serde-bypass test pass. A session that writes
the test cannot supply independent evidence that the test is the right test. Per the same reasoning
as `AID-2026-051`, this dispatch advances 027 without closing it; the register stays `OPEN` until
someone else signs it. Do not mark it closed.

---

## 6. Provenance

Dispatched by the owner-proxy session that read `Provenance::validate()` in full at `13c6d95d`,
confirmed that all four reference groups are unchecked, found that `EvidenceExtension` already
implements the required idiom two hundred lines away, and found that the serde-injection helper the
tests need already exists at `phase2_acceptance.rs:977`. The measurements are in §2, so this prompt
does not ask you to re-derive them.
