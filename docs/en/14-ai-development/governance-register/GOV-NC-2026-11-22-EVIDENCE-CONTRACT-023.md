# GOV-NC-2026-11-22-EVIDENCE-CONTRACT-023 — Evidence Domain Contract Conformance

## 1. Registration Information

| Item | Value |
|---|---|
| Registration ID | GOV-NC-2026-11-22-EVIDENCE-CONTRACT-023 |
| Registration Date | 2026-11-22 |
| Category | MIGRATION_DEBT / DOMAIN_CONTRACT_CONFORMANCE |
| Status | OPEN |
| Severity | CONTRACT CONFORMANCE — STRUCTURAL |
| Authoritative Contract | `02-domain-model/core-entities.md` §8 |
| Affected Components | `memory-domain`, `memory-compiler`, `bmcp-protocol`, and their tests |
| Related Registrations | GOV-NC-2026-11-22-ENUM-BOUNDARY-021; GOV-NC-2026-11-22-PHASE2-RESIDUAL-022 |
| Implementation Authorization | NOT AUTHORIZED |
| Closure Requirement | Both WP-A and WP-B must satisfy all requirements and pass independent verification |

This registration records systematic conformance gaps between the Evidence domain implementation and its authoritative domain contract.

This registration does not authorize breaking changes to existing crates, public APIs, serialized representations, or persistent data formats.

## 2. Scope of Implementation

This registration contains two related work packages that must be verified independently.

### WP-A: Evidence Structure Conformance

Address structural conformance of the Evidence entity, including:

1. The 13 fields required by the contract.
2. The missing `excerpt_ref` field.
3. Field ownership and duplicate identity across `Evidence` and `EvidenceExtension`.
4. Naming differences between contract fields and implementation fields.
5. Type mismatches involving `source_ref`, `recorded_at`, `locator`, and `observed_at`.
6. Correct implementation of contract types including `TypedObjectRef`, `Instant`, `Locator`, and `ContentRef`.

### WP-B: Evidence Enum Conformance

Address:

1. The complete `EvidenceKind` value set.
2. The complete `EvidenceAvailability` value set.
3. Serde serialization and deserialization representations.
4. Explicit migration policies for legacy enum values.
5. All construction sites, match expressions, protocol mappings, and tests.

Both work packages must pass their respective tests. Completion of either work package alone does not close this registration.

## 3. Prohibited Scope

Until separate implementation authorization is granted:

- Do not modify existing files under `crates/`.
- Do not modify existing public structs or enums.
- Do not remove any existing enum variants.
- Do not change existing serialization or deserialization behavior.
- Do not modify databases or other persistent data.
- Do not modify BMCP protocol schemas.
- Do not modify root configuration, build scripts, or the bilingual baseline.
- Do not create pull requests, commits, or pushes.
- Do not mark this registration as completed.
- Do not silently map legacy values without migration evidence.
- Do not interpret the target model in this registration as implementation authorization.

## 4. Problem Overview

Authoritative domain contract:

`02-domain-model/core-entities.md` §8, lines 127–145.

This section defines a single Evidence entity containing 13 fields.

Contract source:

```text
## 8. Evidence

| Field | Type / nullable | Meaning and constraint |
|---|---|---|
| evidence_id | OpaqueId, required | Stable identity |
| evidence_kind | Enum, required | source_span, user_statement, document, observation, tool_result, attestation, derived_excerpt |
| source_ref | TypedObjectRef, required | Event/document/external source |
| locator | Locator, nullable | Message span, page, JSON path, time range, environment tick |
| excerpt_ref | ContentRef, nullable | Retained excerpt if permitted |
| observed_at | Instant, nullable | Observation time |
| recorded_at | Instant, required | Brain record time |
| collector_ref | ActorRef, required | Capturing actor/component |
| integrity_digest | String, nullable | Source integrity reference |
| evidential_role | Enum, required | supports, refutes, qualifies, context_only |
| source_reliability_ref | OpaqueId, nullable | Separate source assessment |
| scope_refs | ScopeRef[], required | Evidence access scope |
| availability_state | Enum, required | available, restricted, expired, forgotten, external_unavailable |
```

The contract requires one unified Evidence entity. Its identity, source, locator, excerpt, observation time, recording time, collector, integrity information, evidential role, source reliability, access scope, and availability state jointly constitute the evidence record.

The current implementation splits this entity into two structs: `Evidence` and `EvidenceExtension`.

Measured implementation:

```rust
pub struct Evidence {
    pub evidence_id: OpaqueId,
    pub source_ref: OpaqueId,
    pub recorded_at: String,
    pub scope_refs: Vec<ScopeRef>,
    pub role: EvidenceRole,
}

pub struct EvidenceExtension {
    pub evidence_ref: EvidenceRef,
    pub kind: EvidenceKind,
    pub source_ref: EvidenceSourceRef,
    pub locator: Option<String>,
    pub observed_at: Option<TimeValue>,
    pub collector: ActorRef,
    pub integrity_digest: Option<String>,
    pub source_reliability_ref: Option<OpaqueId>,
    pub availability: EvidenceAvailability,
}
```

The two structs contain 14 fields in total.

Field-by-field comparison identifies at least four classes of conformance gaps: missing fields, inconsistent field names and identity ownership, type mismatches, and enum value-set mismatches.

This is not merely a naming discrepancy and cannot be resolved by changing enums alone.

## 5. Individual Defects and Measured Evidence

### 5.1 Contract Field Completely Missing

| Contract Field | Contract Type | Current Implementation |
|---|---|---|
| excerpt_ref | ContentRef, nullable | Completely absent |

`excerpt_ref` represents a retained excerpt reference when retention is permitted.

Neither `locator`, `source_ref`, nor another field may be treated as its equivalent replacement.

This is a structural conformance gap.

### 5.2 Inconsistent Field Names and Identity Ownership

| Contract Field | Current Implementation | Struct |
|---|---|---|
| evidence_kind | kind | EvidenceExtension |
| collector_ref | collector | EvidenceExtension |
| evidential_role | role | Evidence |
| availability_state | availability | EvidenceExtension |
| evidence_id | evidence_ref | EvidenceExtension; Evidence also contains evidence_id |

The first four items require verification and consistent implementation of the contract field names.

The fifth item is not merely a naming issue.

Currently:

- `Evidence` contains `evidence_id: OpaqueId`.
- `EvidenceExtension` contains `evidence_ref: EvidenceRef`.

This means that two structs each carry an identity-related field.

Migration must establish a unique Evidence identity and define how extension information is associated with that identity.

Neither field may be mechanically removed or have its type changed without semantic justification.

### 5.3 Field Type Mismatches

| Contract Field | Contract Requirement | Current Implementation |
|---|---|---|
| source_ref | TypedObjectRef | OpaqueId in Evidence; EvidenceSourceRef in EvidenceExtension |
| recorded_at | Instant | String |
| locator | Locator, nullable | Option<String> |
| observed_at | Instant, nullable | Option<TimeValue> |

`source_ref` is a particularly important gap.

Two source references currently exist:

```rust
Evidence.source_ref: OpaqueId
EvidenceExtension.source_ref: EvidenceSourceRef
```

`EvidenceSourceRef` is currently an enum containing three variants: Event, Memory, and External.

The fact that this enum classifies source categories does not establish that it is equivalent to the contract's `TypedObjectRef`.

Migration must preserve the type semantics required by the contract.

`recorded_at` must satisfy Instant semantics rather than being represented by an arbitrary String.

`locator` must support the structured locator semantics described by the contract, including message spans, page numbers, JSON paths, time ranges, and environment ticks.

`observed_at` must satisfy nullable Instant semantics.

These four mismatches cannot be resolved through field renaming.

### 5.4 EvidenceKind Value-Set Mismatch

Required by the contract:

```text
source_span
user_statement
document
observation
tool_result
attestation
derived_excerpt
```

Current implementation:

```rust
pub enum EvidenceKind {
    Document,
    Message,
    Observation,
    Record,
    Dataset,
    Other(String),
}
```

Comparison:

| Classification | Values |
|---|---|
| Required by contract and already implemented | Document, Observation |
| Required by contract but missing | SourceSpan, UserStatement, ToolResult, Attestation, DerivedExcerpt |
| Extra implementation values | Message, Record, Dataset, Other(String) |

The enum does not conform to the authoritative domain value set.

Message must not be automatically mapped to SourceSpan based on name similarity. Record, Dataset, and Other(String) must not be arbitrarily mapped to an authoritative value.

All mappings require auditable semantic justification.

### 5.5 EvidenceAvailability Value-Set Mismatch

Required by the contract:

```text
available
restricted
expired
forgotten
external_unavailable
```

Current implementation:

```rust
pub enum EvidenceAvailability {
    Available,
    Restricted,
    Unavailable,
    Forgotten,
}
```

Comparison:

| Classification | Values |
|---|---|
| Required by contract and already implemented | Available, Restricted, Forgotten |
| Required by contract but missing | Expired, ExternalUnavailable |
| Extra implementation value | Unavailable |

`Unavailable` cannot be treated as equivalent to either `Expired` or `ExternalUnavailable`.

These states may represent different facts:

- Expired: the evidence has expired.
- ExternalUnavailable: the external source cannot be retrieved.
- Unavailable: a generalized state in the current legacy implementation whose specific cause cannot be determined from its name alone.

An explicit historical-data migration or load-rejection policy is required.

## 6. Governance Ruling

### 6.1 Authority

`02-domain-model/core-entities.md` §8 is the authoritative basis for determining Evidence domain conformance.

The current implementation does not conform to this contract.

This registration does not authorize changing the contract to accommodate the existing implementation.

### 6.2 One Registration, Two Work Packages

WP-A and WP-B jointly constitute one Evidence entity conformance issue.

They may be implemented and verified independently, but both must satisfy this registration's closure requirements.

Passing WP-B enum tests cannot substitute for WP-A structural conformance verification.

Passing WP-A structural tests cannot substitute for WP-B value-set verification.

### 6.3 Legacy Data Migration

There is currently insufficient evidence to establish that all historical persistent data is free of legacy enum values.

Before implementation, an independent inventory is required for:

- Database records.
- Historical JSON and other serialized data.
- Test fixtures.
- External protocol inputs.
- Published or retained historical data formats.

For legacy values:

1. `Unavailable` must not be silently converted to `Expired`.
2. `Unavailable` must not be silently converted to `ExternalUnavailable`.
3. `Message`, `Record`, `Dataset`, and `Other(String)` must not be mapped without semantic assessment.
4. If a reliable mapping cannot be established, loading must be rejected with the specific data location reported, or an explicitly approved migration procedure must be used.
5. A compatibility reader must not preserve legacy values as part of the new authoritative domain value set.

### 6.4 Serde and Serialization

The target enum serialization representation must conform to the domain contract.

A stable snake_case string representation is recommended, for example:

- `SourceSpan` → `source_span`
- `UserStatement` → `user_statement`
- `ExternalUnavailable` → `external_unavailable`

Whether `#[serde(rename_all = "snake_case")]` is adopted must be verified against existing schemas, historical formats, and protocol representations during implementation.

Historical JSON representations must not be inferred solely from current Rust variant names.

Struct field renaming, merging, type changes, and identity ownership changes also create serialization compatibility risks and must be included in the migration plan.

## 7. Implementation Requirements

### WP-A: Structural Migration

The implementation owner must:

1. Establish a field-by-field mapping between the 13 contract fields and the final Rust model.
2. Define the unique Evidence identity.
3. Eliminate identity ambiguity between `Evidence` and `EvidenceExtension`.
4. Ensure that `source_ref` has one authoritative representation conforming to the contract semantics.
5. Implement `excerpt_ref`.
6. Standardize contract field names.
7. Ensure that `recorded_at`, `locator`, and `observed_at` satisfy their contract types.
8. Verify all required and nullable fields.
9. Verify compatibility or explicit rejection of legacy serialized data.

### WP-B: Enum Migration

The implementation owner must:

1. Adopt the complete `EvidenceKind` value set specified by the contract.
2. Adopt the complete `EvidenceAvailability` value set specified by the contract.
3. Verify all construction sites and match expressions.
4. Verify BMCP protocol mappings.
5. Verify Serde serialization and deserialization.
6. Establish an explicit migration policy for legacy values.
7. Avoid automatic value mappings unsupported by evidence.

## 8. Test Checklist

### WP-A Tests

- [ ] Evidence covers all 13 contract fields.
- [ ] `excerpt_ref` exists and correctly supports nullable semantics.
- [ ] Evidence identity is unique and its association model is explicit.
- [ ] No two semantically different authoritative `source_ref` fields remain.
- [ ] `source_ref` satisfies the TypedObjectRef contract.
- [ ] `recorded_at` satisfies the Instant contract.
- [ ] `locator` satisfies the Locator contract.
- [ ] `observed_at` satisfies the nullable Instant contract.
- [ ] `collector_ref` satisfies the ActorRef contract.
- [ ] `evidential_role` conforms to the contract value set.
- [ ] Deserialization behavior for required and nullable fields is correct.
- [ ] Migration or rejection behavior for legacy structural data is tested.

### WP-B Tests

- [ ] EvidenceKind contains exactly the seven contract values.
- [ ] EvidenceKind contains no unauthorized additional domain values.
- [ ] EvidenceAvailability contains exactly the five contract values.
- [ ] EvidenceAvailability does not contain Unavailable.
- [ ] All construction sites are migrated.
- [ ] All match expressions are exhaustive.
- [ ] BMCP protocol mappings are verified.
- [ ] Serde uses stable string representations conforming to the contract.
- [ ] Legacy Unavailable data is never silently mapped.
- [ ] Legacy EvidenceKind values have explicit migration or rejection policies.

### Integration Tests

- [ ] memory-domain tests pass.
- [ ] memory-compiler tests pass.
- [ ] bmcp-protocol tests pass.
- [ ] Cross-crate Evidence data flows conform to the unified contract.
- [ ] Serialization round-trip tests pass.
- [ ] Historical-data migration tests pass, or explicit load rejection is verified.
- [ ] No unauthorized protocol or persistent-format changes are introduced.

## 9. Closure Conditions

This registration may be closed only after all the following conditions are satisfied:

1. All WP-A structural conformance tests pass.
2. All WP-B enum conformance tests pass.
3. All 13 contract fields have explicit implementation mappings.
4. Both enums conform to their complete authoritative value sets.
5. Identity and source-reference semantics are unambiguous.
6. Historical serialized data has an approved migration or load-rejection policy.
7. Construction sites, match expressions, and protocol mappings across all affected crates are verified.
8. Integration tests pass.
9. Independent review confirms conformance with §8.
10. Related changes receive formal implementation authorization and required approvals.

If any condition remains incomplete, this registration must remain OPEN.

## 10. Governance Conclusion

The current Evidence implementation has structural conformance gaps against the authoritative domain contract.

These gaps include a missing field, inconsistent field names and identity ownership, type mismatches, and value-set mismatches in both enums.

This issue is consolidated under GOV-NC-2026-11-22-EVIDENCE-CONTRACT-023 and divided into two independently verified work packages: WP-A and WP-B.

This registration does not authorize destructive migration.

The existing implementation must remain unchanged until formal authorization is granted, historical data is inventoried, and the migration plan is approved.

**Final Status: OPEN — EVIDENCE DOMAIN CONTRACT CONFORMANCE DEBT.**
