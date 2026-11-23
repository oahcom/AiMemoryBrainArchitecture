---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "This work record documents a Provenance reference-validation gap; no approval or independent verification is claimed."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/governance-register/GOV-NC-2026-11-22-PROVENANCE-REFERENCE-REVALIDATION-027.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-22-PROVENANCE-REFERENCE-REVALIDATION-027.md"
---

# GOV-NC-2026-11-22-PROVENANCE-REFERENCE-REVALIDATION-027 — Provenance Reference Revalidation

## 1. Registration Information

| Field | Value |
|---|---|
| Registration ID | GOV-NC-2026-11-22-PROVENANCE-REFERENCE-REVALIDATION-027 |
| Registration date | 2026-11-22 |
| Category | VALIDATION_GAP / DOMAIN_TYPE_INTEGRITY |
| Status | OPEN |
| Severity | REFERENCE INTEGRITY — SERDE BYPASS |
| Affected components | `memory-domain` (`Provenance`, `ProvenanceGraph`) |
| Related registration | GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026 |
| Implementation authority | DISPATCHED — `AID-2026-052` (see Section 6); closure still requires independent evidence |
| Closure conditions | All four reference fields revalidated; serde-bypass tests pass |

**Numbering note.** The identifier `027` is derived as "highest currently used number, 026, plus one".
It was not issued by the registration process. Basis: `-026` is the highest number in this
directory and `025` is a separate ADR; a repository-wide and all-branch search found `027`
unused. If the registration process requires a formally assigned number, replace this
identifier with its result; nothing else in this document depends on it.

## 2. Problem

`Provenance::validate()` currently validates required scalar fields, the presence of lineage,
and the positional completeness of `source_version_refs` against `source_refs`. It does **not**
revalidate each reference value contained in:

- `source_refs`
- `source_version_refs`
- `actor_ref.actor_id`
- `parent_provenance_refs`

Serde deserialization can construct these values without going through the domain constructors.
Constructor-level validation therefore cannot establish that a deserialized `Provenance`
instance contains valid references.

`ProvenanceGraph::add()` calls `provenance.validate()` before inserting. The completeness of
that boundary therefore depends on `Provenance::validate()` performing the required
reference-level checks.

Within the same crate, `EvidenceExtension::validate()` already performs per-field
revalidation and states the reason in a comment (serde derives `Deserialize`, which bypasses
the constructors, so a payload can carry an empty string into a field no constructor would
ever have produced). `Provenance` does not receive the same treatment.

## 3. Required work

1. Inspect the concrete types and validation APIs for every reference field listed above.
2. Define the reference validity requirements for each field, including nested `actor_ref.actor_id`.
3. Extend `Provenance::validate()` to revalidate every reference value, using the
   authoritative validation API for its concrete type.
4. Preserve the existing invariants:
   - `source_refs` must not be empty.
   - If `source_version_refs` is present, its length must equal `source_refs.len()`.
   - An explicitly supplied `unavailable_reason` must not be blank.
   - A record must provide parent lineage or an explicit explanation of its absence.
5. Ensure `ProvenanceGraph::add()` rejects invalid references before mutating the graph.
6. Add acceptance tests that construct invalid reference values through deserialization,
   then prove that both direct validation and graph insertion reject them.

## 4. Acceptance criteria

- Every element of `source_refs` is revalidated.
- Every element of `source_version_refs` is revalidated.
- `actor_ref.actor_id` is revalidated.
- Every element of `parent_provenance_refs` is revalidated.
- Invalid deserialized values cannot pass `Provenance::validate()`.
- Invalid deserialized values cannot be inserted through `ProvenanceGraph::add()`.
- A failed graph insertion leaves the original graph unchanged.
- Existing valid `Provenance` fixtures and lineage behavior remain valid.

## 5. Scope boundary

This registration is independent of the Evidence dual `source_ref` semantics issue
(GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026 §6.5).
It does not define or imply equivalence between `Evidence.source_ref` and
`EvidenceExtension.source_ref`.

This registration document is added by PR #707; however, the Provenance per-reference revalidation work specified in this registration is outside that PR's implementation scope.

PR #707 does modify `ProvenanceGraph::add()` and `Provenance::validate()`: the public signature of the former changes from `add(provenance, parents)` to `add(provenance)`, and lineage is now taken from `Provenance.parent_provenance_refs`; the latter replaces the empty-string check on `unavailable_reason` with a whitespace-trimmed check and adds an `IncompleteProvenanceLineage` rejection path when no parents and no `unavailable_reason` are supplied. However, PR #707 does not implement the per-element revalidation required by Section 3 of this registration for the four reference fields: `source_refs`, `source_version_refs`, `actor_ref.actor_id`, and `parent_provenance_refs`.

---

## 6. Dispatch (2026-11-23)

| Field | Value |
|---|---|
| Work item | `AID-2026-052` (`14-ai-development/work-items/AID-2026-052/`) |
| Basis | Sections 3 and 4 of this registration; the owner-proxy read `Provenance::validate()` line by line at `13c6d95d` |
| Implementation scope | `crates/memory-domain/src/lib.rs` and `crates/memory-domain/tests/phase2_acceptance.rs` only |
| Explicitly not authorized | field type changes, a change to `OpaqueId`'s `Deserialize`, serialization contract changes, closure of this registration |

**The four reference groups in Section 3 are not one shape. This is the main finding of the dispatch:**

- `parent_provenance_refs` already has a `validate()` generated by the `ref_ctor!` macro, shared with `ClaimRef`, `EvidenceRef` and three others, so the fourth group needs one call.
- `source_refs`, `source_version_refs` and `actor_ref.actor_id` are bare `OpaqueId` with no validator anywhere in the repository; they need inline emptiness checks, exactly as `EvidenceExtension::validate()` does for `collector.actor_id`.

An implementer who treats all four as the same shape will either add a `validate()` to `OpaqueId` — changing the type surface for every user in the crate — or miss that the fourth group is already covered.

**Why not close this at `OpaqueId`'s `Deserialize`.** That would close this registration immediately while rewriting the serialization contract for every type in the crate, including the fixtures `dm2_11` and the other phase-2 tests deserialize. "Reject at the boundary" and "reject at the point of use" are different decisions, and this registration did not make the first one.

**Why the status is not CLOSED.** This registration requires the serde-bypass test to pass. A session that writes that test cannot supply independent evidence for its own artifact. This is the same reasoning as `AID-2026-051-F3`: this dispatch advances the registration without closing it.
