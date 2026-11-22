# D-OWNER-DECISION-CANONICAL-COMMIT-001 — Canonical commit reference, record and validation

**Status:** DECIDED (owner-proxy decision, development baseline)
**Decided by:** Owner D acting as owner proxy under the standing instruction to decide blocking development-baseline contracts rather than leave them open
**Decision date:** 2026-11-22
**Baseline:** `main` at `b093b59fe83052aa3e359b819b0bc3fc26ac8dd0`
**Scope:** GAP-12 §5 step 2; development-baseline semantics only

## 1. Decision

**D freezes a content-bearing `CanonicalCommitRef` issued by the D owner-proxy development-baseline issuer, backed by an append-only `canonical_commits` record in the AdmissionStore SQLite database and checked by a record-backed three-outcome validator; this baseline issuer is an explicit development trust anchor, not a production cryptographic identity.**

The durable record, not the caller-supplied admission cursor and not the reference alone, is the fact. The cursor remains an untrusted lookup claim. A successful validation is the only permitted source of `PublicationProof.canonical_commit_confirmed = true`.

## 2. The reference type

### 2.1 Frozen content

A committed reference carries:

- `commit_id: OpaqueId`: non-empty unique identifier for this canonical commit;
- `issuer: IssuerId`: the issuer identity, restricted in dev-baseline to the one literal `d-owner-proxy/dev-baseline-v1`;
- `subject_digest: OpaqueId`: lowercase 64-character SHA-256 digest of the canonical commit subject;
- `issued_at: String`: RFC 3339 UTC timestamp generated at issuance.

The subject is the exact immutable domain revision being committed, identified by its subject kind and stable/revision identifiers. The digest input is the versioned `CanonicalCommitSubjectV1` encoding: a domain-defined, deterministic, length-prefixed UTF-8 field sequence containing subject kind, subject identity, revision identity, and the canonical payload bytes. The `canonical_commit_ref` field itself is excluded from those payload bytes (equivalently, normalized to the legacy pending value) to avoid a self-referential digest. E must implement this encoding once and share it between issuance and validation; JSON object serialization order is not a substitute for this encoding.

### 2.2 Rust type shape

The following is the normative public shape. The private state prevents struct-literal construction. The public candidate constructor is available across the `memory-domain` / `memory-compiler` crate boundary, but it does not issue authority: only the D issuer's durable row can make the candidate validate. `IssuerId` is a validated newtype using the existing `OpaqueId` validation convention.

```rust
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct IssuerId(OpaqueId);

impl IssuerId {
    pub fn new(value: impl Into<String>) -> Result<Self, DomainError> {
        Ok(Self(OpaqueId::new(value)?))
    }

    pub fn as_str(&self) -> &str {
        self.0.as_str()
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CanonicalCommitData {
    pub commit_id: OpaqueId,
    pub issuer: IssuerId,
    pub subject_digest: OpaqueId,
    pub issued_at: String,
}

#[derive(Clone, Debug, Eq, PartialEq)]
enum CanonicalCommitRefState {
    Pending,
    Issued(CanonicalCommitData),
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CanonicalCommitRef {
    state: CanonicalCommitRefState,
}

impl CanonicalCommitRef {
    /// Explicit legacy/uncommitted marker. This is never commit evidence.
    pub const fn pending_d() -> Self {
        Self {
            state: CanonicalCommitRefState::Pending,
        }
    }

    /// Construct a candidate reference after validating its fields.
    /// This does not issue a commit or establish authority; the matching
    /// durable canonical_commits row is required by the validator.
    pub fn from_issued_data(data: CanonicalCommitData) -> Result<Self, DomainError> {
        validate_commit_data(&data)?;
        Ok(Self {
            state: CanonicalCommitRefState::Issued(data),
        })
    }

    pub fn is_pending(&self) -> bool {
        matches!(self.state, CanonicalCommitRefState::Pending)
    }

    pub fn data(&self) -> Option<&CanonicalCommitData> {
        match &self.state {
            CanonicalCommitRefState::Pending => None,
            CanonicalCommitRefState::Issued(data) => Some(data),
        }
    }
}
```

`validate_commit_data` MUST reject empty IDs, an issuer outside the dev-baseline allowlist, a digest not encoded as exactly 64 lowercase hexadecimal characters, and a timestamp that is not RFC 3339 UTC. The issuer allowlist contains exactly `d-owner-proxy/dev-baseline-v1` in this baseline.

### 2.3 Serialization is part of the contract

The current unit struct `CanonicalCommitRef(())` serializes as the unit value (JSON `null`). Replacing it with a normally derived struct or enum would change the legacy placeholder representation and is not allowed.

Implement custom Serde for the new type:

- `Pending` serializes using `serialize_unit_struct("CanonicalCommitRef")`, preserving the existing unit/null representation;
- `Issued` serializes as a named object with exactly `commit_id`, `issuer`, `subject_digest`, and `issued_at`;
- deserialization accepts the legacy unit representation as `Pending`, and accepts the issued object only when every required field validates;
- unknown/missing issued fields, duplicate fields, and malformed values are deserialization errors; never coerce malformed issued data to `Pending`.

This is a tagged-by-shape compatibility rule, not an enum tag added to the old representation. E must test JSON compatibility and the repository's other supported Serde formats before merging. No caller can turn `Pending` into evidence: validators reject it.

## 3. The durable record

### 3.1 Location and minimum schema

The canonical record lives in the same SQLite database managed by `memory-compiler::admission::AdmissionStore`, in a new append-only table. It is not stored by treating `producer_work.request_json` or its cursor field as the record.

Minimum logical DDL:

```sql
CREATE TABLE IF NOT EXISTS canonical_commits (
    commit_id       TEXT PRIMARY KEY NOT NULL,
    issuer_id       TEXT NOT NULL,
    subject_digest  TEXT NOT NULL,
    issued_at       TEXT NOT NULL,
    signature       TEXT NOT NULL
);
```

Field semantics:

- `commit_id`: exact `OpaqueId` string referenced by `CanonicalCommitRef`;
- `issuer_id`: exact issuer literal;
- `subject_digest`: exact SHA-256 subject digest;
- `issued_at`: exact RFC 3339 UTC timestamp;
- `signature`: empty string in dev-baseline only; reserved for the production signature envelope.

Rows are immutable. A duplicate `commit_id` with byte-identical fields is an idempotent replay; the same ID with any differing field is an integrity conflict and MUST return an error. No update-in-place or delete API is authorized by this decision.

### 3.2 Writer, reader and atomicity

The D owner-proxy issuer is the only logical writer. The compiler publication authority is a reader/validator, not a writer. E implements the SQLite operations behind the existing AdmissionStore boundary.

The record insertion MUST be atomic with the durable commit operation for the subject revision. A reference must not escape as issued until the record transaction commits. The admission cursor remains a caller-supplied claim and may continue to be persisted as such. Its value is only a lookup selector: it must resolve to the same `commit_id` as the reference. The validator then loads the record and compares the stored fields with the reference and the expected subject digest. Neither the cursor nor the reference alone establishes existence.

The current test constructor uses an in-memory SQLite connection. That is suitable for tests but is not durable across process restart. The production AdmissionStore connection MUST use its durable database configuration for this table; E must not describe an in-memory-only row as durable. This decision selects the logical database/table, not a filesystem path or deployment topology.

## 4. The validator

### 4.1 Contract

The validator is a read-only AdmissionStore operation with this logical signature:

```rust
pub fn validate_canonical_commit(
    &self,
    cursor: &OpaqueId,
    reference: &CanonicalCommitRef,
    expected_subject_digest: &OpaqueId,
) -> Result<bool, CanonicalCommitValidationError>;
```

The concrete error may be represented by an existing compiler/admission error or by a new error variant introduced by E. If a new variant is required, E adds it in the implementation PR; this decision does not add a `DomainError` variant.

### 4.2 Three outcomes

- **`Ok(true)`**: the reference is issued; cursor equals its `commit_id`; a durable row exists; the stored commit ID, issuer, digest and timestamp exactly match the reference; the issuer is on the dev-baseline allowlist; and the stored subject digest equals `expected_subject_digest`.
- **`Ok(false)`**: the durable row exists and is readable, the issuer and reference metadata are valid and match the row, but the stored subject digest does not equal the expected subject digest. This is a content mismatch, not an authority failure.
- **`Err(...)`**: pending reference; missing row; unreadable database; cursor/reference identity mismatch; unsupported or unverifiable issuer; malformed/corrupt record; metadata mismatch; or any other failure to establish authority.

**A missing record is always `Err`, never `Ok(false)`.** This follows the compiler contract at `memory-compiler/src/lib.rs:519-521`: authority failures remain errors and must not be reinterpreted as a publication disposition.

### 4.3 Runtime properties and integration

Validation is local and synchronous: it requires neither network access nor a clock. Issuance obtains `issued_at` from the issuer's clock; validation checks its syntax and exact equality with the stored record but does not decide freshness. The production adapter replaces the hard-coded `canonical_commit_confirmed: false` with this validator result. It propagates `Err` unchanged; only `Ok(true)` sets the proof flag true; `Ok(false)` leaves the flag false and allows the existing gate to return `Blocked`.

The compiler MUST NOT infer confirmation from cursor presence, cursor persistence, staging state, `pending_d()`, or test-only authorities.

## 5. Phase 1 compatibility

**`dm2_14_phase1_serialization_remains_compatible` MUST continue to pass unchanged.** The legacy pending value keeps its existing unit/null Serde representation through the custom serializer/deserializer described in §2.3. The new issued representation is additive and appears only for newly issued references.

No Phase 1 field is renamed, removed, made optional, or reordered as a migration shortcut. If the current `dm2_14` test does not exercise the nested canonical reference representation, E must add a focused regression assertion for the legacy `pending_d()` serialized bytes/value and deserialization round-trip; do not weaken or replace `dm2_14`.

## 6. Migration of existing pending references

The four cited source positions (main at the decision baseline: `lib.rs:824, 842, 878, 914`) are not four semantically distinct stored fields. Inspection shows one persisted `canonical_commit_ref` field on `FactRevision`, threaded through the `initial`, `successor`, and internal `new` constructor paths. All have the same meaning: the canonical commit reference for that immutable revision. There is no field-semantic conflict that prevents one type.

Migration is therefore:

1. Keep `CanonicalCommitRef::pending_d()` and its legacy serialized representation.
2. Existing persisted values deserialize as `Pending`; they remain explicitly uncommitted and MUST NOT validate.
3. Existing constructor call sites may continue passing `pending_d()` while creating pre-commit/proposal objects. The D issuer replaces that value with an issued reference only after the revision's durable commit record is inserted.
4. No bulk backfill may invent commit IDs, issuer identities, timestamps, digests, or records for historical pending values. Historical values remain pending unless a real baseline issuance operation commits them.
5. No pending reference may flow into publication authorization as confirmation.

The current main source labels the field on `FactRevision` (not `ClaimRevision`). The four line positions are one field plus constructor parameter/forwarding sites, not four independent domain fields. This factual correction does not change the migration: the same type is used consistently through the construction path.

## 7. What this does not decide

The following are explicitly **OUT-OF-SCOPE(dev-baseline)** and are not blockers for this contract:

- production-grade digital signatures or selection of a cryptographic signature algorithm;
- private-key generation, custody, rotation, revocation, hardware security modules (HSM), or external KMS integration;
- independent human approval or a human-held signing identity;
- cross-host issuer authentication or network-based verification.

In dev-baseline, `d-owner-proxy/dev-baseline-v1` is a designated logical trust anchor and `signature = ''` is the explicit no-cryptography marker. This is not a claim that the record is cryptographically unforgeable or suitable for adversarial production environments. It is a bounded development authority decision, not a simulated signature.

**Production replacement path:** before production security claims or externally exposed publication, replace the dev-baseline issuer with a governed D issuer identity and signed commit envelope; define the algorithm, canonical signing bytes, key custody/rotation/revocation policy and trust-root distribution; store and verify the signature in the same append-only record lifecycle; reject empty signatures outside dev-baseline; and add conformance tests for invalid signatures, revoked keys, replay, tampering and issuer rollover. This production security profile requires its own explicit decision and is not silently implied here.

This decision also does not select a physical SQLite file path, backup/restore policy, replication topology, retention policy, or a general storage engine migration.

## 8. Closure criteria

E may mark GAP-12 step 2 implemented only when all of the following are evidenced:

1. `CanonicalCommitRef` carries the four fields in §2 and has a validated issuer type; a caller may construct a candidate reference, but it cannot validate without the matching D-issued durable record.
2. `pending_d()` remains available and serializes byte/value-compatibly with the legacy unit representation; malformed issued representations fail closed.
3. `dm2_14_phase1_serialization_remains_compatible` passes unchanged, with a focused legacy-pending serialization regression test if needed.
4. `canonical_commits` exists in AdmissionStore's SQLite schema with the minimum fields and append-only/idempotent-conflict behavior in §3.
5. Production uses a file-backed/durable AdmissionStore connection for canonical commit records; in-memory test storage is not represented as durable.
6. Issuance and the subject digest use the same deterministic `CanonicalCommitSubjectV1` encoding; the reference is returned only after the record transaction commits.
7. Validator tests cover: valid matching record => `Ok(true)`; readable matching record with subject mismatch => `Ok(false)`; missing row, pending ref, cursor mismatch, issuer mismatch, malformed row and SQLite read failure => `Err`.
8. Authority errors propagate through `AdmissionPublicationAuthority` without conversion to `false` or `PublicationDisposition`.
9. `PublicationProof.canonical_commit_confirmed` is sourced only from validator `Ok(true)`; cursor presence/round-trip alone cannot set it.
10. No `pending_d()` path feeds publication authorization as evidence.
11. The existing publication disposition remains unchanged for false proof flags: the gate returns `Blocked`; no other proof flag is inferred or modified by this decision.
12. No production `.rs` change is part of this decision record; implementation and tests are delivered by E in a separate implementation PR.

**Finding / impact / recommendation:** the existing placeholder and unvalidated cursor cannot establish a canonical commit (finding); treating either as confirmation would violate D2/D3 and permit a false `Published` result (impact); implement this record-backed dev-baseline contract and retain cryptographic hardening as an explicit production replacement (recommendation).
