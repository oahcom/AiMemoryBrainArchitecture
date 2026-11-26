---
document_metadata:
  domain: domain-model
  role: decision-record

  lifecycle:
    approval:
      decision_status: Approved
      approver: "Owner I acting as owner proxy under the standing instruction to decide blocking development-baseline contracts rather than leave them open"
      decision_date: "2026-11-21"
      approved_version:
        scheme: git
        value: "c9a6394d738f7cbc25d93c116a724080e6444ee3"
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "PR #595 / commit c9a6394d738f7cbc25d93c116a724080e6444ee3"
        - "Issue #763 comment #7097007415"
      revocation: null

    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: null

    usage_status: Active
    modification_status: Pending-Reapproval

    supersession:
      supersedes: []
      supersession_reason: null

  authority:
    canonical_status: Canonical
    canonical_scope: "The I Owner-proxy authorization contract governing authorization-decision and attestor references, including the two permitted development-baseline issuer identifiers and the separate deterministic encodings, records, and validators for the two record families."
    canonical_scope_id: domain-model/authorization-decision-and-attestor-reference-contract
    canonical_scope_keywords:
      - authorization-decision
      - attestor-reference
      - attestation-subject-v1
      - issuer-allowlist
      - i-owner-proxy
      - i-attestor-proxy
    canonical_conflict_status: Resolved
    canonical_conflict_resolution:
      resolution_decision_id: GOV-CANON-2026-002
      resolved_date: "2026-11-23"
      selected_document: "14-ai-development/work-items/I-OWNER-DECISION-AUTHORIZATION-DECISION-001.md"
      resolution_evidence:
        - "Owner Decision #001 §2.3, original decision dated 2026-11-21: separate AttestationSubjectV1 encoding, record, and validator; same I issuer allowlist."
        - "I Owner-proxy ruling, Issue #763 comment #7097007415: i-owner-proxy/dev-baseline-v1 for authorization-decision records and i-attestor-proxy/dev-baseline-v1 for attestation records."
        - "PR #802 / merge commit 3046c848: dated clarification appended to §2.3 without replacing the original wording or changing the original decision date."
        - "RULING-031 §7.4: explicitly records that the Owner-proxy interpretation controls and that the section-scoped amendment does not supersede the entire Owner Decision."
    normative_status: Normative
---

# I-OWNER-DECISION-AUTHORIZATION-DECISION-001 — Authorization decision reference, record and validation

**Status:** DECIDED (owner-proxy decision, development baseline)  
**Decided by:** Owner I acting as owner proxy under the standing instruction to decide blocking development-baseline contracts rather than leave them open  
**Decision date:** 2026-11-21  
**Baseline:** PR base snapshot `main` at `b47bd97cc40a80cd1f50674838fad04590f740b1`; the supplied source fact pack was measured at `b093b59f`  
**Scope:** Phase 2 authorization evidence; `FactRevision.authorization_decision_ref` and the paired I-owned attestor reference

## 1. Decision

**I freezes a content-bearing, outcome-bearing `AuthorizationDecisionRef` issued by the sole I owner-proxy development-baseline issuer, backed by an append-only `authorization_decisions` record in the `AdmissionStore` SQLite database and checked by a record-backed validator; `AttestorRef` is a separate but structurally parallel I-issued attestation contract, not an authorization decision.**

The durable record, not a caller-created reference or legacy pending marker, is the authority fact. A candidate reference alone never grants publication authority. The dev-baseline issuer is an explicit logical trust anchor, not a production cryptographic identity.

## 2. The reference type

### 2.1 Frozen content

An issued authorization decision carries:

- `decision_id: OpaqueId`: non-empty unique identifier;
- `issuer: IssuerId`: restricted in dev-baseline to `i-owner-proxy/dev-baseline-v1`;
- `subject_digest: OpaqueId`: lowercase 64-character SHA-256 digest of the exact immutable subject being authorized;
- `issued_at: String`: RFC 3339 UTC timestamp generated at issuance;
- `decision_kind: AuthorizationDecisionKind`: terminal disposition.

The decision kind has exactly three values:

```rust
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum AuthorizationDecisionKind {
    Approved,
    Denied,
    Conditional,
}
```

These outcomes are materially distinct. `Conditional` means approval depends on constraints already included in the immutable subject being digested; it is not permission to maintain an unbound mutable condition list. The validator confirms the recorded decision and subject binding; the consuming policy gate decides whether the kind permits a transition. Only `Approved` satisfies an unconditional authorization requirement.

The subject uses a deterministic, versioned `AuthorizationDecisionSubjectV1` encoding shared by issuance and validation. It includes subject kind, stable identity, revision identity, operation/purpose and all decision-relevant immutable content. The `authorization_decision_ref` field itself is excluded (or normalized to the legacy pending value) to avoid a self-referential digest. JSON serialization order is not a digest format.

### 2.2 Rust type shape

> **Amended 2026-11-22 15:52 +0800 — see the amendment at the end of this document.** The two-state `AuthorizationDecisionRefState` below is superseded by `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` D2 (`Absent` / `Placeholder` / `Issued`). The rest of this section — `AuthorizationDecisionData`, the shared `IssuerId`, field validation, private state — stands.

**D's `IssuerId` and I's `IssuerId` are the same Rust type**, defined once in `memory-domain` and shared across owner contracts; do not create an I-specific duplicate. The allowlists remain owner-specific: this contract accepts exactly `i-owner-proxy/dev-baseline-v1`, while D's contract accepts exactly `d-owner-proxy/dev-baseline-v1`.

The following is normative. Private state prevents struct-literal construction. The public candidate constructor does not issue authority; only the matching durable row can make the candidate validate.

```rust
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AuthorizationDecisionData {
    pub decision_id: OpaqueId,
    pub issuer: IssuerId,
    pub subject_digest: OpaqueId,
    pub issued_at: String,
    pub decision_kind: AuthorizationDecisionKind,
}

#[derive(Clone, Debug, Eq, PartialEq)]
enum AuthorizationDecisionRefState {
    Pending,
    Issued(AuthorizationDecisionData),
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AuthorizationDecisionRef {
    state: AuthorizationDecisionRefState,
}

impl AuthorizationDecisionRef {
    /// Legacy/uncommitted marker; never authorization evidence.
    pub const fn pending_i() -> Self {
        Self { state: AuthorizationDecisionRefState::Pending }
    }

    /// Constructs a candidate only; the matching durable row is still required.
    pub fn from_issued_data(data: AuthorizationDecisionData) -> Result<Self, DomainError> {
        validate_authorization_decision_data(&data)?;
        Ok(Self { state: AuthorizationDecisionRefState::Issued(data) })
    }

    pub fn is_pending(&self) -> bool {
        matches!(self.state, AuthorizationDecisionRefState::Pending)
    }

    pub fn data(&self) -> Option<&AuthorizationDecisionData> {
        match &self.state {
            AuthorizationDecisionRefState::Pending => None,
            AuthorizationDecisionRefState::Issued(data) => Some(data),
        }
    }
}
```

Validation MUST reject empty IDs, a non-allowlisted issuer, a digest not exactly 64 lowercase hexadecimal characters, a non-RFC-3339-UTC timestamp, or an unknown decision kind. The allowlist contains exactly `i-owner-proxy/dev-baseline-v1`. If existing domain errors cannot express malformed data, E may add a narrowly scoped `DomainError` variant in its implementation PR; this decision adds no variant.

### 2.3 AttestorRef: same envelope pattern, distinct evidence contract

**`AttestorRef` and `AuthorizationDecisionRef` are two contracts, not aliases or interchangeable evidence.** An attestor reference answers “who attested this subject”; an authorization decision answers “what did I decide about this subject”. An attestation is not an authorization grant, and an authorization decision is not an attestation. Their identical `pending_i()` placeholders and I ownership require both to leave the placeholder-only state in the same implementation tranche.

Normative parallel attestor shape:

```rust
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AttestorData {
    pub attestation_id: OpaqueId,
    pub issuer: IssuerId,
    pub subject_digest: OpaqueId,
    pub issued_at: String,
}

#[derive(Clone, Debug, Eq, PartialEq)]
enum AttestorRefState { Pending, Issued(AttestorData) }

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AttestorRef { state: AttestorRefState }

impl AttestorRef {
    pub const fn pending_i() -> Self {
        Self { state: AttestorRefState::Pending }
    }
    pub fn from_issued_data(data: AttestorData) -> Result<Self, DomainError> {
        validate_attestor_data(&data)?;
        Ok(Self { state: AttestorRefState::Issued(data) })
    }
    pub fn is_pending(&self) -> bool {
        matches!(self.state, AttestorRefState::Pending)
    }
    pub fn data(&self) -> Option<&AttestorData> {
        match &self.state {
            AttestorRefState::Pending => None,
            AttestorRefState::Issued(data) => Some(data),
        }
    }
}
```

Attestor data uses a separately named deterministic `AttestationSubjectV1` encoding and its own record/validator. It uses the same I issuer allowlist. E must not substitute `validate_attestor` for `validate_authorization_decision`.

**Dated clarification — 2026-11-23 (I Owner-proxy ruling, Issue #763 comment #7097007415).** For purposes of this section, “the same I issuer allowlist” means one I-controlled trust-authorization policy that admits exactly two development-baseline issuer identifiers: `i-owner-proxy/dev-baseline-v1` for authorization-decision records and `i-attestor-proxy/dev-baseline-v1` for attestation records. The identifiers are distinct; each record family retains its own separately named deterministic encoding, record, and validator. “Same” refers to the controlling I authorization policy, not to equality of the issuer strings. This dated clarification supplements the decision dated 2026-11-21 and does not change that original decision date. The related implementation-invariant ruling is recorded in `14-ai-development/adr/OWNER-RULING-ATTESTOR-ISSUER-SEPARATION-031.md`; it supplements the implementation context for this decision and does not replace or supersede this Owner Decision.

### 2.4 Serialization is part of the contract

The current unit structs `AuthorizationDecisionRef(())` and `AttestorRef(())` serialize as unit values (JSON `null`). A normally derived struct/enum would change the legacy placeholder representation and is forbidden.

Implement custom Serde for both:

- Pending serializes with `serialize_unit_struct("AuthorizationDecisionRef")` or `serialize_unit_struct("AttestorRef")`, respectively, preserving the existing unit/null representation;
- issued authorization serializes as an object with exactly `decision_id`, `issuer`, `subject_digest`, `issued_at`, `decision_kind`;
- issued attestor serializes as an object with exactly `attestation_id`, `issuer`, `subject_digest`, `issued_at`;
- deserialization accepts the legacy unit representation as Pending and accepts issued objects only after validation;
- unknown/missing/duplicate fields, unknown decision kinds and malformed values are deserialization errors; never coerce malformed issued data to Pending.

This is tagged-by-shape compatibility, not a new enum tag on the legacy representation. Test JSON and every other supported Serde format.

## 3. The durable record

### 3.1 Location and minimum schema

Both I records live in the same SQLite database managed by `memory-compiler::admission::AdmissionStore`, but in independent append-only tables. They do not share D's `canonical_commits`: D's row records canonical commitment; I's row records authorization. Attestation is distinct again.

```sql
CREATE TABLE IF NOT EXISTS authorization_decisions (
    decision_id      TEXT PRIMARY KEY NOT NULL,
    issuer_id        TEXT NOT NULL,
    subject_digest   TEXT NOT NULL,
    issued_at        TEXT NOT NULL,
    decision_kind    TEXT NOT NULL,
    signature        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS i_attestations (
    attestation_id   TEXT PRIMARY KEY NOT NULL,
    issuer_id        TEXT NOT NULL,
    subject_digest   TEXT NOT NULL,
    issued_at        TEXT NOT NULL,
    signature        TEXT NOT NULL
);
```

Minimum field semantics:

- IDs are the exact non-empty `OpaqueId` strings in the domain references;
- `issuer_id` is the exact I issuer literal;
- `subject_digest` is the lowercase SHA-256 digest;
- `issued_at` is RFC 3339 UTC;
- `decision_kind` is exactly `Approved`, `Denied` or `Conditional` (authorization table only);
- `signature` is empty only in dev-baseline and reserved for the production signature envelope.

Rows are immutable. A duplicate ID with byte-identical fields is an idempotent replay. The same ID with any differing field is an integrity conflict and MUST return an error. No update-in-place or delete API is authorized. Separate primary-key namespaces prevent an attestation ID being confused with a decision ID.

### 3.2 Writer, reader, atomicity and ordering

The I owner-proxy issuer is the only logical writer. The compiler publication authority is a reader/validator, not a writer. E implements SQLite operations behind AdmissionStore.

The authorization decision logically precedes a D canonical commit that relies on it: I records its decision for the immutable subject/operation; D may subsequently record canonical commitment for the accepted immutable revision. The records remain independent and are related through their subject binding/workflow; neither record ID substitutes for the other. A canonical commit does not create, imply or upgrade an authorization decision. Both validators compare against the same canonical subject digest when the workflow requires authorization of that exact committed subject.

Issuance is atomic: an issued reference must not escape before its record transaction commits. Any retained cursor is only an untrusted lookup selector and must resolve to the same decision ID; it is not authority evidence.

### 3.3 Crate boundary

> **Amended 2026-11-22 15:52 +0800 — see the amendment at the end of this document.** The phrase "reject Pending" in the second paragraph is **narrowed** by `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` D3 and by `OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025` §1: under the three-state type the domain presence gate rejects `Absent` and must **NOT** reject `Placeholder`. "Pending" here named everything that was not issued; that set split in two, and only one half is absence. Everything else in this section — the crate boundary itself, and the rule that only the `AdmissionStore`-backed validator establishes durable authority — stands.

Domain types and deterministic subject encodings belong in `memory-domain`, which remains SQLite-independent. Tables, insert/read operations and record-backed validators belong in `memory-compiler` behind `AdmissionStore`, matching D's layering. The publication authority calls validators and propagates errors; it must not write records or synthesize I decisions.

The validator is **not** a `FactRevision::validate()` responsibility. Domain validation may validate candidate field syntax and reject Pending, but only the compiler's AdmissionStore-backed validator can establish durable existence and authority. Structural validation must not claim a candidate reference is issued.

## 4. The validator

### 4.1 Contract

The authorization validator is a read-only AdmissionStore operation:

```rust
pub fn validate_authorization_decision(
    &self,
    reference: &AuthorizationDecisionRef,
    expected_subject_digest: &OpaqueId,
) -> Result<bool, AuthorizationDecisionValidationError>;

// Read the already-validated recorded kind from the same immutable record;
// this accessor is not itself an authority check. Publication may proceed
// only when validation returned Ok(true) AND the recorded kind is Approved.
pub fn authorization_decision_kind(
    &self,
    reference: &AuthorizationDecisionRef,
) -> Result<AuthorizationDecisionKind, AuthorizationDecisionValidationError>;
```

The boolean validator preserves D's three-outcome contract exactly. The recorded kind remains a separately inspectable field and MUST be checked by the publication consumer: only Approved satisfies an unconditional authorization requirement. The concrete error may use an existing compiler/admission error or a new compiler error added by E. This decision adds no `DomainError` variant.

The attestor counterpart is separate:

```rust
pub fn validate_attestor(
    &self,
    reference: &AttestorRef,
    expected_subject_digest: &OpaqueId,
) -> Result<(), AttestorValidationError>;
```

### 4.2 Three outcomes

- **`Ok(true)`**: issued reference; durable row exists and is readable; stored ID, issuer, digest, timestamp and kind exactly match the reference; issuer is allowlisted; and stored subject digest equals the expected subject digest. The consumer MUST additionally require the recorded `decision_kind == Approved`; a valid Denied or Conditional record is not an unconditional grant.
- **`Ok(false)`**: the durable row exists and is readable, issuer and reference metadata are valid and match the row, but the stored subject digest does not equal the expected subject digest. This is a content mismatch, not an authority failure.
- **`Err(...)`**: pending reference; missing row; unreadable database; unsupported/unverifiable issuer; malformed/corrupt record; reference/record metadata mismatch; or any other failure to establish authority.

**A missing authorization record is always Err, never a denial result.** This follows `memory-compiler/src/lib.rs:519-521`: authority failures remain errors, not publication dispositions. A denial is a recorded I decision; absence is failure to establish that I decided anything.

### 4.3 dm2_06 semantics

> **Amended 2026-11-22 15:52 +0800 — see the amendment at the end of this document.** The assignment of `dm2_06` below is superseded by `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` §4: `dm2_06` lives at `crates/memory-domain/tests/phase2_acceptance.rs:606`, which cannot reach `memory-compiler`, so the compiler-layer `Err` described here is unreachable at that path. The text below describes the compiler-layer authority contract, which stands, and which now needs its own test.

`dm2_06_missing_authorization_ref_blocks_fact_publication` must exercise the **Pending reference** path and assert a propagated authority `Err`, not `Ok(false)`. The field is required and non-optional; there is no `None` state. An issued candidate with no durable row is also Err. A recorded Denied decision is a separate negative-disposition test, not the missing-authorization test.

This distinction prevents a known negative decision from being conflated with missing authority and follows the compiler's authority-error rule. The validator returns Ok(true) only for a matching subject, Ok(false) only for a readable subject-digest mismatch, and Err for missing/unverifiable authority. E must separately require the recorded kind to be Approved.

## 5. Phase 1 compatibility

**`dm2_14_phase1_serialization_remains_compatible` MUST continue to pass unchanged.** Each legacy pending value keeps its existing unit/null Serde representation via §2.4. Issued representations are additive.

No Phase 1 field is renamed, removed, made optional or reordered. If dm2_14 does not cover nested authorization and attestor references, E adds focused regression assertions for both legacy pending representations and round-trips; do not weaken or replace dm2_14.

## 6. Migration

1. Keep both `AuthorizationDecisionRef::pending_i()` and `AttestorRef::pending_i()` as explicit legacy/pre-issuance constructors; neither validates as authority.
2. Existing persisted unit values deserialize as Pending. Do not backfill fabricated IDs, issuers, digests, timestamps, kinds or records.
3. Proposal/pre-authorization constructors may continue creating pending values. I issuance replaces them with issued references only after the corresponding durable record commits.
4. Update consumers so neither pending type can feed successful publication authorization. Structural FactRevision validation rejects pending evidence where issued evidence is required; AdmissionStore independently rejects it.
5. Keep `FactRevision.authorization_decision_ref` and `FactRevision.attestor_ref` required and non-optional. Do not migrate them to `Option`; Pending is the explicit legacy state.
6. Keep the two evidence kinds distinct in APIs, persistence, serialization and tests.

## 7. What this does not decide

Explicitly **OUT-OF-SCOPE(dev-baseline)** and not blockers:

- production-grade digital signatures, algorithms or canonical signing envelopes;
- private-key generation/custody/rotation/revocation, HSM or external KMS;
- independent human approval or human-held signing identity;
- cross-host issuer authentication, network verification or distributed consensus;
- production policy for conditional approvals beyond binding conditions into the immutable subject digest;
- physical SQLite path, backup/restore, replication, retention or storage-engine migration.

In dev-baseline, `i-owner-proxy/dev-baseline-v1` is the logical trust anchor and `signature = ''` is the explicit no-cryptography marker. This is not cryptographic unforgeability or an adversarial production security claim.

**Production replacement path:** before production security claims or externally exposed publication, replace the dev-baseline issuer with a governed I identity and signed decision/attestation envelopes; define canonical signing bytes, algorithms, key custody/rotation/revocation and trust-root distribution; store and verify signatures in the same append-only lifecycle; reject empty signatures outside dev-baseline; and add tests for invalid signatures, revoked keys, replay, tampering, issuer rollover and decision-kind downgrade. This requires a separate explicit production decision.

## 8. Closure criteria

> **Amended 2026-11-22 15:52 +0800 — see the amendment at the end of this document.** Criterion 1 below still describes the **two-state** `Pending/Issued` shape; `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` D2 replaced it with `Absent` / `Placeholder` / `Issued`, so read criterion 1's "private Pending/Issued state" as that three-state shape. Criterion 12 below still says the assertion must be "the propagated authority `Err`"; the end-of-document amendment changes **which assertion satisfies it** — ADR-001 §4's two domain-layer assertions on `FactRevision::validate()`, not a compiler-layer `Err`, because `dm2_06` cannot reach `memory-compiler` from `crates/memory-domain/tests/phase2_acceptance.rs:606`. The obligation itself survives; only its satisfaction changed. Criteria 2–11 and 13 are unchanged.

E may mark this contract implemented only when:

1. `AuthorizationDecisionRef` carries the five fields in §2.1 with private Pending/Issued state and the shared `IssuerId`; only the I allowlist is accepted.
2. `AuthorizationDecisionKind` represents Approved, Denied and Conditional; only Approved satisfies unconditional authorization.
3. `AttestorRef` is independently content-bearing with its own Pending/Issued state, data, serialization, record and validator; it is not conflated with authorization.
4. Both legacy `pending_i()` constructors preserve exact unit/null serialization; malformed issued forms fail closed.
5. `dm2_14_phase1_serialization_remains_compatible` passes unchanged, with focused legacy-pending regression assertions for both types where needed.
6. Both `authorization_decisions` and `i_attestations` exist in AdmissionStore with append-only/idempotent-conflict semantics.
7. Issuance and validation share deterministic subject encodings; no issued reference escapes before record commit.
8. Authorization tests cover valid Approved/Denied/Conditional records; Pending => Err; missing row => Err; issuer/metadata mismatch => Err; subject digest mismatch => Err; malformed row and SQLite read failure => Err.
9. Attestor tests independently cover matching record and pending/missing/mismatched/unreadable cases as errors.
10. Authority errors propagate through publication authority without conversion to a successful authorization or false publication disposition.
11. `FactRevision::validate()` does not claim a pending placeholder is issued authority; durable authority is established only by AdmissionStore validation.
12. **E MUST delete the `#[ignore]` on `dm2_06_missing_authorization_ref_blocks_fact_publication` and replace `unimplemented!()` with a real assertion that missing/pending authorization is rejected with the propagated authority Err.** The current ignore comment becomes stale once this contract is implemented; update it in E's test implementation, not in this documentation-only decision PR.
13. No production `.rs` change is part of this decision record; implementation and tests are delivered by E in a separate implementation PR.

**Finding / impact / recommendation:** public `pending_i()` placeholders currently let structurally valid FactRevision values carry no verifiable I authorization or attestation (finding); treating a placeholder or caller-created candidate as authority can permit publication without an I-issued decision (impact); implement distinct record-backed I authorization and attestation contracts in AdmissionStore, preserve legacy pending serialization, and retain cryptographic hardening as an explicit production replacement (recommendation).

## Amendment — supersession by `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001`, taken 2026-11-22 15:52 +0800

This document (`c9a6394d`, 2026-11-22 12:54 +0800) and `14-ai-development/adr/OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001.md` (`986c42bc`, 2026-11-22 13:41 +0800) were both recorded `DECIDED` by an owner proxy 47 minutes apart. ADR-001 said `Supersedes: nothing` while contradicting this document in two places. That was false, and it left two contradictory normative documents with no adjudication. The adjudication is recorded here and in ADR-001 §8.

**Two clauses of this document are superseded. Everything else stands.**

### Superseded

1. **§2.2's two-state `AuthorizationDecisionRefState { Pending, Issued(..) }`** is superseded by ADR-001 D2 (`Absent` / `Placeholder` / `Issued(AuthorizationDecisionRef)`). The two-state enum cannot represent absence: `pending_i()` is a value that exists, so there is no shape in §2.2 that means "no authorization was recorded" — which is precisely the condition `dm2_06` must prove is rejected. ADR-001 is later and the type state is its explicit subject.

2. **§4.3's assignment of `dm2_06`** is superseded by ADR-001 §4. `dm2_06_missing_authorization_ref_blocks_fact_publication` lives at `crates/memory-domain/tests/phase2_acceptance.rs:606`. `crates/memory-domain/Cargo.toml` declares `serde` and `serde_json` only; it does not depend on `memory-compiler`, and the dependency direction is the reverse. The propagated authority `Err` §4.3 requires cannot be produced at that path. §4.3 as written is not a strict requirement but an unreachable one; `dm2_06` becomes ADR-001 §4's two assertions on `FactRevision::validate()`.

### Narrowed

3. **§3.3's "Domain validation may validate candidate field syntax and reject Pending"** is narrowed by ADR-001 D3: under the three-state type, the domain presence gate rejects `Absent` and **must NOT reject `Placeholder`**. "Pending" in §3.3 named everything that was not issued; under D2 that splits into two states, and only one of them is absence. Rejecting `Placeholder` at the domain gate would move the authenticity question into the presence gate.

### Unchanged, and still required

- **§4.1 and §4.2, the whole validator contract.** `validate_authorization_decision` returning `Ok(true)` / `Ok(false)` on subject-digest mismatch / `Err` for missing authority stands exactly as written, including "a missing authorization record is always `Err`, never a denial result". ADR-001 does not touch it.
- **§3.3's compiler-layer validator behind `AdmissionStore`.** Superseding §4.3 removes the `dm2_06` assignment, not the gate. ADR-001 D6's domain presence gate and this document's compiler authenticity gate answer different questions and both exist.
- **The compiler-layer validator now needs its own test**, at a location that can reach `memory-compiler`. It is not `dm2_06`, must not be named `dm2_06`, and must not be counted toward `dm2_06`'s closure.
- §1, §2.1, §2.3, §2.4, §3.1, §3.2, §5, §6, §7, and closure criteria 1–13 except as item 1 depends on §2.2's shape and item 12 depends on §4.3's assignment.

Closure criterion 12 requires deleting the `#[ignore]` and replacing `unimplemented!()` with a real assertion. That obligation survives; what changes is which assertion satisfies it — ADR-001 §4's two domain-layer assertions, not a compiler-layer `Err`.
