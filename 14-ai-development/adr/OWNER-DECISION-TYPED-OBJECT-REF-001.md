---
document_metadata:
  domain: domain-model
  role: decision-record

  lifecycle:
    approval:
      decision_status: Approved
      approver: "Project Owner (repository owner), converging under standing instruction (Issue #751)"
      decision_date: "2026-11-23"
      approved_version:
        scheme: content-hash
        value: "783f584abdaa30e535072e03d81ab128775d4f0de209f59ef6da9100826aaf73"
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "Issue #751 comment 7097692424"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "Every code reference in §2 was read at main 6b97a659 in this session. The contract text quoted in §1 is 02-domain-model/core-entities.md §8 and §14 at the same commit. The three fields that carry TypedObjectRef are the only three occurrences in the contract, established by grep -n over 02-domain-model/."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Canonical
    canonical_scope: "Owner ruling: the authoritative shape of TypedObjectRef, and the standing prohibition on asserting equivalence between Evidence.source_ref and EvidenceExtension.source_ref until both conform to it."
    canonical_scope_id: domain-model/typed-object-ref
    canonical_scope_keywords:
      - typed-object-ref
      - source-ref
      - evidence-contract
      - object-type-discriminator
    canonical_conflict_status: None
    normative_status: Normative

  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# OWNER-DECISION-TYPED-OBJECT-REF-001 — what `TypedObjectRef` is, and why the two `source_ref` fields are not equivalent

**Status:** DECIDED (owner-proxy decision, 2026-11-23)
**Decided by:** Owner D acting as owner proxy, under the standing instruction that a blocking decision with no human available is to be taken and recorded rather than left open. Same mechanism as `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001`, `D-OWNER-DECISION-CANONICAL-COMMIT-001` and `OWNER-DECISION-BMCP-MCP-DISPATCH-001`.
**Closes:** the "Required resolution" paragraph of `GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026` §6.5.
**Does not close:** that register. Its closing conditions 1–10 are untouched, and condition 9 requires independent review this session cannot supply.

---

## 1. The question, as the register states it

`GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026` §6.5 records:

> **Required resolution:** define the authoritative `source_ref` representation, its contract-level semantics, and any permitted mapping to legacy or extension representations before implementing cross-field validation.

and forbids, until then:

> Do not add an equality check or conversion-based equivalence assertion between these fields.

The register is right to forbid it, and right that the missing piece is a definition rather than a check. What it does not say — because it was written to measure, not to decide — is what the definition should be. That is this document.

## 2. Measured state at `6b97a659`

The contract (`02-domain-model/core-entities.md`) names `TypedObjectRef` in exactly three places:

| line | field | contract type |
|---|---|---|
| 115 | `subject_ref` / `object_ref` | `TypedObjectRef, required` |
| 133 | `source_ref` | `TypedObjectRef, required` |

Its shape is not defined in §8. It appears once, as a candidate, in §14:

> **CANDIDATE:** typed references shaped as object_type + object_id + optional version_id.

So the contract requires a type whose structure is still a candidate. That is the root cause, and it is upstream of the register's §5.3 table.

The implementation has three different answers to the same requirement:

| location | type | carries `object_type`? | carries `version_id`? |
|---|---|---|---|
| `Evidence.source_ref` | `OpaqueId` | no | no |
| `EvidenceExtension.source_ref` | `EvidenceSourceRef` | as an enum variant, not a field | no |
| `TypedObjectRef` | **does not exist** | — | — |

And the three ref types that `EvidenceSourceRef` wraps are all bare newtypes:

```rust
pub struct EventRef(OpaqueId);
pub struct ExternalSourceRef(OpaqueId);
pub struct MemoryRef(OpaqueId);
```

So the register's framing — "are these two representations equivalent?" — understates the problem. Neither conforms to the contract, and the contract's own type was never implemented. An equivalence question between two non-conforming representations has no answer worth having.

## 3. Decision

**D1 — `TypedObjectRef` is frozen at the §14 candidate shape.** Three members, in this order and with these names:

| member | type | required | meaning |
|---|---|---|---|
| `object_type` | enumerated type-kind discriminator | yes | what kind of object is referenced |
| `object_id` | opaque identifier | yes | which object of that kind |
| `version_id` | opaque identifier | no | which version, when the reference is version-specific |

`object_type` is a **field**, not an enum variant. A reference whose kind is encoded only in its Rust variant cannot be compared, sorted, serialised or stored uniformly across kinds, and every consumer must match on the variant to learn something the payload should already have said.

**D2 — the discriminator's value domain is the contract's object-type vocabulary, not the Rust type names.** `EvidenceSourceRef`'s `Event`/`Memory`/`External` are a *source classification*, not an object-type vocabulary, and reusing those three words as `object_type` values would make a classification masquerade as an identity discriminator. This is the specific substitution §5.3 warns against, and it is the reason "the enum has classification capability" is not evidence of equivalence.

**D3 — `version_id` is optional and its absence is meaningful.** Absent means "the reference does not distinguish versions", not "the latest version" and not "unknown". A consumer that needs a version-specific reference must require it; a consumer that does not must not silently read an absent `version_id` as a current pointer. Recording this explicitly prevents the absent field from becoming a de-facto latest-pointer.

**D4 — neither existing field becomes `TypedObjectRef` by renaming.** `OpaqueId` carries no kind, so promoting it to `TypedObjectRef` requires supplying a discriminator that does not exist in the data. `EvidenceSourceRef` carries a classification, so promoting it requires supplying object identity that it does not carry. Both are migrations with data consequences, not type substitutions.

**D5 — the prohibition in §6.5 stands, and now has a stated release condition.** No equality check, no conversion-based equivalence assertion, and no shared `PartialEq` between `Evidence.source_ref` and `EvidenceExtension.source_ref` until **both** are `TypedObjectRef` as defined in D1–D3. When both conform, equivalence is a derived fact about two values of one type and needs no special assertion; before both conform, any assertion compares two things that are not the same kind of thing.

## 4. Why this is a decision and not a preference

Three constraints make the shape forced rather than chosen:

1. **The contract already says `TypedObjectRef`.** The name commits to "typed". A type with no discriminator is not typed, so `OpaqueId` cannot satisfy it however it is renamed.
2. **The same type is required at three fields** (`subject_ref`, `object_ref`, `source_ref`). A relation endpoint and an evidence source must be describable by one shape, or the contract needs three names and has one. §14's candidate is the only shape on record that covers all three.
3. **§14 offers exactly one candidate.** Choosing it is not inventing a contract; it is accepting the one already written and refusing the three ad-hoc alternatives the implementation drifted into.

What this decision *does* choose, and why: `object_type` as a field rather than a variant (D1), and the vocabulary being the contract's rather than the Rust enum's (D2). Both are argued above rather than asserted.

## 5. What this does not authorize

- **No migration.** Old persisted `source_ref` values are not converted by this decision. `GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026` §6.3 requires an independent inventory before any migration, and that inventory has not been performed. D4 says the promotion is a migration precisely so nobody treats it as a rename.
- **No code.** §2's measurements are read-only. Implementing `TypedObjectRef`, or changing either field's type, is a delivery task with acceptance criteria — not this document.
- **No register closure.** Conditions 1–10 of the register remain open. This decision resolves the one paragraph the register asked to have resolved; it satisfies none of the ten conditions by itself.
- **No change to `validate_against`.** The existing check between `evidence_id` and `extension.evidence_ref` is untouched, as §6.5 requires.

## 6. Acceptance criteria for whoever implements D1

1. A `TypedObjectRef` type exists with exactly the three members of D1, in that order.
2. `object_type`'s values come from the contract's object-type vocabulary; a test asserts the mapping explicitly rather than deriving it from Rust variant names (D2).
3. `version_id` absent and `version_id` present are distinguishable in serialised form, and no consumer reads absent as "latest" (D3).
4. `Evidence.source_ref` and `EvidenceExtension.source_ref` are both `TypedObjectRef`, or a finding explains why one of them is not.
5. No `PartialEq`, `From`, or conversion assertion exists between the two fields before condition 4 holds (D5).
6. Every construction site, match site and protocol mapping affected by the type change is enumerated and verified — this is the register's condition 7, and it is the one most likely to be under-counted.
7. `GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026` §6.3's inventory is performed and its result recorded before any persisted value is migrated.

## 7. Independence

Written by the session that measured §2. This is an owner-proxy decision, not an independent review. The register's condition 9 requires independent confirmation that an implementation conforms to §8; this document defines what conformance means, which is a different act, and it cannot also be the confirmation.

Recorded so a later reader can tell which kind of document this is: **a definition, not an acceptance**.
