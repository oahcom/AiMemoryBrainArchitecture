# Phase 2 Domain Extension Specification

- Work Item: GAP-05 / GAP-BASELINE-001
- Owner: B — Domain Model Architect
- Status: PROPOSED — specification only; not implementation, schema freeze, or acceptance
- Baseline: `1ad6c2cf67a228f597fcbe1c7149c328ecbf38e9`
- Language pair: this document and `phase-2-domain-extension.zh-CN.md` are normative semantic peers

## 1. Decision and scope

Phase 1 is implemented as a bounded minimal domain core. Phase 2 is justified because the Phase 1 domain corpus and downstream G contract require immutable assertion revisions and richer canonical referents/lineage than the current Rust model exposes.

This is a **narrow extension of the existing model**, not a replacement of Phase 1 and not a claim that all concepts in the older domain overview are approved for immediate implementation.

Phase 2 covers:

1. Claim identity separated from immutable ClaimRevision state.
2. Independent Fact / FactRevision attestation concepts, subject to the D/I boundary decisions in §8.
3. Complete domain-level identity and typed association semantics for Entity and Relation.
4. Evidence records and explicit Claim/Relation evidence roles.
5. Explicit Provenance lineage and typed MemorySource associations.
6. Temporal precision sufficient to distinguish occurrence, recording, and validity without inventing certainty.

Phase 2 does **not** cover Phase 3, runtime retrieval/ranking, compiler extraction, context planning/version lifecycle, BMCP wire schemas, Storage DDL/transaction mechanics, authorization policy, cryptographic trust, or physical Forget implementation.



### Phase classification caveat

All ten files present in `02-domain-model/` at the baseline are Phase-1-scoped; none names Phase 2. The six foundational model documents describe a broader logical schema, while `phase-1-domain-model-freeze.md` deliberately freezes the smaller minimum implementation loop. Therefore, the Phase 2 label in this proposal is the GAP-05 delivery grouping for domain concepts not represented by the current Rust crate; it is **not** a claim that the source documents originally classified those concepts as Phase 2. Existing DECIDED semantics are carried forward, not re-decided. OPEN/CANDIDATE items remain open. Where a concept is described as Phase 1 in the broader logical schema but omitted from the minimum freeze and Rust model, this is recorded as an implementation/representation gap rather than silently rewriting the Phase 1 decision history.

## 2. Evidence-based gap assessment

| Missing or under-modelled concept | Where required | Phase 1 state | Phase 2 disposition |
|---|---|---|---|
| ClaimRevision and exact ClaimRevisionRef | `domain-model-overview.md` §2.4; `06-memory-context/context-versioning.md` §§13.2–13.3 requires exact immutable ClaimRevision references | `Claim` currently combines proposition and assertion state; no separate revision type | IN SCOPE |
| Fact and FactRevision | Domain overview §3.15; G Context Versioning §13.3 requires exact FactRevision references | No Rust types | IN SCOPE, with D/I decision gate |
| Entity identity metadata and lifecycle | `core-entities.md` §6; relationships/provenance and lifecycle docs | `Entity` has only ID, type, label and scopes | IN SCOPE as an extension of Entity |
| Typed Relation semantics | `core-entities.md` §7; `relationships-and-provenance.md` §§2–3 | `Relation` has string type, opaque endpoints and scopes only | IN SCOPE as an extension of Relation |
| Evidence source/locator/availability and link role | `core-entities.md` §8; relationships/provenance §4 | `Evidence` has source, recorded time, scopes and role; lacks kind, locator, observed time, collector, integrity and availability | IN SCOPE as an extension |
| Provenance derivation graph and MemorySource | `core-entities.md` §9; relationships/provenance §5 | `Provenance` is a flat record; `MemorySource` exists but is minimal | IN SCOPE as an extension |
| Temporal precision and explicit valid-time semantics | `epistemic-and-temporal-semantics.md` §§5–6 | `TimeValue` is string-based Instant/Interval/Unknown; no precision, timezone, certainty or source phrase | IN SCOPE as an extension |
| Context identity, budget, ContextVersion, delivery and reconciliation | `06-memory-context/`; GAP-02 | G-owned; `MemoryContext` and `ContextEntry` already exist in Phase 1 | NOT B SCOPE; G owns semantics |
| Producer ledger namespace, ForgetFence currentness and watermarks | `08-bmcp-protocol/owner-snapshot-namespace-and-fence-currentness-contract.md` | No matching domain types; these are D/H/I authority and BMCP protocol concerns | NOT B SCOPE |
| Permission, Attestor authorization, security principal and trust root | `scope-and-permission-model.md`; BMCP currentness contract | Phase 1 deliberately separates Scope from Permission | NOT B SCOPE; I owns security decisions |

The G contract is a concrete downstream dependency: a ContextVersion that references ClaimRevision or FactRevision must pin the exact immutable revision, and must not follow a current Claim head. It does not transfer ContextVersion semantics to B.

The BMCP contract's ProducerWork Registration Ledger Namespace and ForgetFence Currentness Proof are not missing domain entities. They are protocol/governance constructs with explicit D/H/I ownership. B must not create shadow domain types for them.

## 3. Phase 2 domain definitions

### 3.1 Claim identity and ClaimRevision

**Claim** is the stable identity of a proposition. It contains ClaimRef and the Scope identity to which that proposition belongs. It is not itself a mutable assertion state.

**ClaimRevision** is one immutable assertion state for a Claim. It contains ClaimRevisionRef, ClaimRef, optional exact parent ClaimRevisionRef, proposition fields (subject, predicate, object, polarity and substantive qualifiers), epistemic status, valid-time reference, Scope references, Evidence references, Provenance references, assertion time, and correction/revision reason.

**Invariants (testable):**

- Every ClaimRevision references exactly one existing ClaimRef.
- Every ClaimRevisionRef identifies exactly one immutable revision and is never reused.
- A non-initial revision has exactly one parent revision belonging to the same ClaimRef; the initial revision has no parent.
- A revision never mutates after acceptance; correction appends a new revision.
- CI-01 through CI-08 in DOMAIN-MODEL-001 §2.4 classify substantive proposition changes as NEW_CLAIM, with explicit lineage; CI-09 through CI-13 classify evidence/provenance/status/assessment/editorial changes as NEW_REVISION, preserving ClaimRef.
- A Scope change never silently transfers ClaimRef; it requires a new ClaimRef and explicit lineage.
- Ambiguous identity classification is rejected for governed resolution; it must not silently default to NEW_REVISION.
- Downstream references (including G ContextVersion) resolve exact ClaimRevisionRef only; no semantic-similarity or latest-head substitution.

**Relationship to Phase 1:** Claim is refined, not removed. ClaimRevision is new. Existing Claim fields that describe assertion state move to the revision representation; stable proposition identity remains on Claim.

### 3.2 Fact and FactRevision

**Fact** is an independently identifiable governed Attestation. It is neither a Claim with higher confidence nor a synonym for Verified Claim.

**FactRevision** is an immutable revision of that Attestation. It binds exact FactRef and FactRevisionRef; exact ClaimRevisionRef values; exact EvidenceRef and ProvenanceRef values; ScopeRef; valid-time and recorded/commit-time references; Attestor reference; exact Attestation Method identifier/version; I AuthorizationDecisionRef; outcome, rationale and correction/revocation lineage.

**Invariants (testable):**

- FactRef and FactRevisionRef are distinct from ClaimRef and ClaimRevisionRef.
- Every FactRevision pins one or more exact ClaimRevisionRef values; it never follows a Claim's current head. The plural set is required by `domain-model-overview.md` §8.1, item 3 (Shared Fact visibility): "A FactRevision linked to multiple ClaimRevisions may remain visible only if every disclosed dependency is independently authorized and not suppressed by an applicable Forget decision." Empty sets are rejected by `FactRevision::validate`.
- Every FactRevision pins exact EvidenceRef and ProvenanceRef values and one Scope identity.
- Confidence alone and Verified status alone cannot create a Fact.
- Correction, withdrawal or reassessment appends a FactRevision; prior revisions are not overwritten.
- A FactRevision with missing or unresolved required authorization reference is not eligible for accepted canonical publication.
- A shared Fact does not confer access to its linked ClaimRevision, Evidence or Provenance.

**Relationship to Phase 1:** Both types are new. They do not replace Claim or Evidence.

**RESOLVED SEMANTIC DECISION — retraction of a pinned ClaimRevision (see `domain-model-overview.md` §3.16, `OWNER-DECISION-FACT-RETRACTION-001`):** Before this ruling the normative sources did not decide the disposition of a FactRevision when one of its exact pinned ClaimRevision values was later assigned `Retracted`. `epistemic-and-temporal-semantics.md` §§2 and 9 define append-only Claim status transitions and preservation of the historical assertion; `domain-model-overview.md` §3.15 and `OWNER-DECISION-FACT-CLAIM-001` §§2 and 5 require exact immutable ClaimRevision pins but did not specify propagation to Fact. **Candidate 3 is selected**: the original FactRevision is retained unchanged and a successor FactRevision is appended with `outcome: FactOutcome::Revoked` and a non-empty `correction_or_revocation_reason`. This requires no new types, because `FactOutcome::Revoked`, `parent_revision_ref` and `correction_or_revocation_reason` already exist and `FactRevision::successor()` already enforces same-`FactRef` parentage. Candidate 1 is excluded by §8.1 item 3 (Fact visibility is already conjunctive over all disclosed dependencies); candidate 2 is excluded by this section's prohibition on a mutable `retracted` field and by the append-only revision invariant. Retraction is not Forget: a revoked FactRevision stays historically readable, whereas a forgotten Memory becomes unreadable. Propagation is not automatic. Still undefined: the trigger, the scope (one or all pinned ClaimRevisions), mixed-dependency treatment, and read-path behavior.

**PENDING CROSS-OWNER DECISION:** I must define/approve Attestor principal identity, authorization decision semantics, and the security meaning of the authorization reference. D must confirm the canonical commit, revision, and Forget/dependency semantics for Fact/FactRevision. Until both decisions bind the same exact contract version, these fields are semantic placeholders only; no implementation may infer authorization or canonical acceptance.

### 3.3 Entity identity

Entity remains an identity-bearing referent and is extended with identity status, aliases, scoped external identifiers, identity evidence, current identity/profile version reference, and merge/split lineage references.

**Invariants (testable):**

- EntityRef is opaque, typed, stable and never reused.
- Display label, alias, mention text, or embedding similarity alone never proves identity equality.
- External identifiers are namespaced and uniqueness is evaluated only within the declared namespace and applicable Scope.
- A resolved referent change is not a label correction: it requires a new Entity identity and explicit lineage.
- Merge/split preserves source identities and an auditable redirect/reference-migration record; historical references are not silently rewritten.
- A merged Entity must identify its successor; a split must identify the resulting identities and the governed allocation of references.
- Identity status and Memory lifecycle are independent.

**Relationship to Phase 1:** Entity is extended in place at the semantic level. No separate EntityVersion type is mandated by this specification; immutable identity/profile revision storage is a D/Storage decision.

**PENDING CROSS-OWNER DECISION:** D must decide how Entity identity changes and merge/split lineage are committed and how canonical references are migrated without rewriting immutable history.

### 3.4 Relation

Relation remains a typed association and is extended with typed endpoints, directionality, structured qualifiers, optional valid time, epistemic status, Evidence references, and relation lifecycle state.

**Invariants (testable):**

- Both endpoints are typed references and each endpoint type is allowed by the registered relation definition.
- Relation type, directionality, inverse/symmetry behavior and uniqueness are validated against a versioned vocabulary.
- Co-occurrence or embedding similarity never creates a Relation.
- Missing valid time means unspecified/unknown, not timeless.
- Cross-scope relation references require explicit sharing authorization; Scope compatibility does not itself grant permission.
- proposed, active, superseded and retracted are distinct relation lifecycle states; they are not MemoryLifecycle or Claim epistemic status.
- Retraction/supersession preserves history and reason; no in-place semantic rewrite.

**Relationship to Phase 1:** Relation is extended in place. The relation vocabulary registry and physical graph representation are not defined here.

**PENDING CROSS-OWNER DECISION:** D must confirm canonical persistence/version and reference consistency for Relation changes. I owns authorization for cross-scope references. The exact relation vocabulary governance process remains OPEN within B's domain scope and is not frozen here.

### 3.5 Evidence

Evidence remains source material or an observation that supports, refutes, qualifies, or contextualizes a Claim/Relation. Extend it with evidence kind, typed source reference, optional locator/content reference, observed time, collector ActorRef, integrity digest, source reliability reference, and availability state.

**Invariants (testable):**

- Every Evidence has one stable EvidenceRef, one typed source reference, at least one ScopeRef and a recorded-at value.
- Evidence role is explicit and limited to supports, refutes, qualifies or context-only.
- Evidence is not a confidence score or a Provenance record.
- A mutable external URL alone is not durable retained evidence.
- Source payload unavailable/restricted/forgotten is represented explicitly; missing content is never reconstructed or fabricated.
- Evidence visibility is independently authorized and may be narrower than the associated Memory or Claim.
- Evidence additions do not change Claim identity; they create a ClaimRevision when the assertion's evidence state changes.

**Relationship to Phase 1:** Evidence is extended in place. Existing EvidenceRole variants remain semantically valid.

**PENDING CROSS-OWNER DECISION:** I owns access/authorization and privacy classification for protected source payloads. D owns canonical retention and Forget dependency handling. B does not define either policy.

### 3.6 Provenance and MemorySource

Provenance is an explicit derivation-lineage record. Extend it with target reference, typed/versioned source edges, derivation kind, method/component version reference, derived-at time, input digest references, parent Provenance references, and explicit unavailable reason.

MemorySource is a typed association between a MemoryVersion/derived asset and one source, with source role, optional locator, Scope and creation time.

**Invariants (testable):**

- Every derived canonical revision has at least one complete lineage path or an explicit unavailable reason accepted by its governing policy.
- Every source edge identifies the source object and exact version when versioned sources exist.
- Provenance explains origin/derivation; Evidence supplies supporting material. They are not interchangeable.
- Method/model identity is process metadata, never proof of correctness.
- Missing source material is marked unavailable; it is never fabricated.
- Provenance history is append-only; correction adds lineage rather than rewriting prior provenance.
- MemorySource does not turn source material into the resulting Memory and does not imply permission to read the source.
- Duplicate derivatives with common ancestry do not become independent corroborating Evidence merely by duplication.

**Relationship to Phase 1:** Provenance and MemorySource are extended; MemorySource already exists in Rust but is under-modelled.

**PENDING CROSS-OWNER DECISION:** D must confirm atomic/recoverable commit and Forget dependency semantics for provenance edges and MemorySource references. E owns compiler derivation-method and input-digest production; B does not define E's pipeline.

### 3.7 Temporal semantics

Extend TimeValue/TemporalRef to preserve explicit precision, timezone, certainty, source expression, and the distinction between Event Time, Recorded At, Valid Time, and (if adopted by D) canonical commit/transaction time.

**Invariants (testable):**

- Unknown time is explicit and never treated as timeless.
- Event Time, Recorded At, Valid Time and retention time are distinct axes and cannot substitute for one another.
- Approximate or source-reported time retains its source expression and uncertainty; normalization cannot invent precision.
- Valid intervals use the declared half-open convention [start, end) where interval semantics apply.
- A point assertion has point semantics; it is not expanded to an invented duration.
- A failed parse preserves source text and produces an explicit unknown/un-normalized value.
- Temporal changes are revisioned; prior valid-time history is not overwritten.

**Relationship to Phase 1:** TimeValue and TemporalRef are extended; existing Instant/Interval/Unknown variants require a compatibility mapping.

**PENDING CROSS-OWNER DECISION:** D must decide whether canonical commit/transaction time is represented in the domain object or only in canonical storage metadata. F owns temporal query behavior; this specification does not define retrieval semantics.

### 3.16 RESOLVED: Retraction propagation to pinned FactRevision

**Status: RESOLVED by `OWNER-DECISION-FACT-RETRACTION-001` — candidate 3 (append a suppressing revision) is selected.**

Ruling provenance: GitHub Issue #265, comment 7064801226 — https://github.com/oahcom/AiMemoryBrainArchitecture/issues/265#issuecomment-7064801226

A FactRevision pins exact ClaimRevisionRef values. When a pinned ClaimRevision is subsequently assigned `Retracted`, the FactRevision MUST NOT be modified or deleted, and its pinned `ClaimRevisionRef` values MUST NOT be rewritten. The governed response is to append a successor FactRevision with `outcome = FactOutcome::Revoked`, `parent_revision_ref` pointing at the prior revision, and a non-empty `correction_or_revocation_reason`. This requires no new types: `FactOutcome::Revoked`, `parent_revision_ref` and `correction_or_revocation_reason` already exist, and `FactRevision::successor()` already enforces same-`FactRef` parentage.

Candidate 1 (continue visible) is excluded by `domain-model-overview.md` §8.1 item 3, which already makes Fact visibility conjunctive over every disclosed dependency. Candidate 2 (mark invalid) is excluded by this section's prohibition on a mutable `retracted` field and by the append-only revision invariant in §3.15 and `epistemic-and-temporal-semantics.md` §§2 and 9.

Retraction is not Forget: a revoked FactRevision remains historically readable and auditable, whereas a forgotten Memory becomes unreadable. Propagation is not automatic; no implementation may infer a disposition from a ClaimRevision reaching `Retracted` without an explicit authorized call.

Still deliberately undefined: the trigger (which actor or process propagates, under what authority), the scope (one or all pinned ClaimRevisions), mixed-dependency treatment, and read-path behavior. Implementations MUST NOT add a `retracted` field to FactRevision, MUST NOT mutate an existing FactRevision to represent a retraction, and MUST NOT select or infer any of the four undefined items locally.

## 4. Phase 2 exclusions and ownership boundary

The following are deliberately not added to `memory-domain` by this specification:

- G-owned ContextIdentity, ContextBudget, ContextVersion, ChangeSet, delivery intent, reconciliation or applied-delivery lifecycle. Existing MemoryContext/ContextEntry remain bounded Phase 1 domain references; G owns context behavior.
- H-owned BMCP messages, wire fields, schema versions, ProducerWork Registration Ledger namespace and delivery/fence proof representations.
- D-owned Canonical Memory Authority, commit cursor, ForgetFence state machine, producer admission ledger, persistence transaction protocol and physical Forget semantics.
- I-owned principals, authentication identities, credentials, grants, permission policy, Attestor authorization, privacy and trust-root decisions.
- E-owned compiler stages, extraction, inference, model/method execution and derived-memory production.
- F-owned retrieval, ranking, activation and temporal query execution.

ScopeRef remains a domain applicability/namespace reference. It is not an authorization grant. The OPEN scope-composition algebra is not silently decided by this extension.

## 5. Migration impact on Phase 1 Rust model

The baseline `crates/memory-domain/src/lib.rs` is 679 lines with 13 unit tests. This specification does not modify it. The following existing declarations/validation/tests are affected by a future authorized implementation:

| Existing code area | Required future change |
|---|---|
| `Claim` struct and `Claim::validate` | Separate stable proposition identity from immutable ClaimRevision assertion fields; add revision-parent and exact-reference validation |
| `MemoryVersion.claims` and `MemoryVersion::validate` | Replace or version the embedded Claim snapshot representation with exact immutable ClaimRevision references/snapshots; coordinate canonical persistence with D |
| `Entity` struct | Add identity status, aliases, scoped external identifiers, identity evidence and merge/split lineage |
| `Relation` struct | Replace untyped endpoint IDs with typed references; add directionality, qualifiers, valid time, epistemic/lifecycle state and Evidence references |
| `Evidence` and `EvidenceRole` | Add kind, typed source, locator, observed/recorded times, collector, integrity and availability |
| `Provenance` and `MemorySource` | Add typed target/source edges, derivation method/version, input digests, parent lineage and explicit unavailability |
| `TimeValue` and `TemporalRef` | Add precision/timezone/certainty/source phrase and explicit valid-time representation without conflating recorded time |
| `DomainError` | Add deterministic errors for invalid typed references, revision parent/identity mismatch, invalid relation endpoints, ambiguous identity classification and incomplete lineage |
| constructors and 13 existing tests | Update fixtures and add invariant tests; preserve Phase 1 behavior and regression coverage |

No line-level patch is prescribed because implementation is not authorized. The migration must preserve existing serialized data or use an explicitly versioned conversion. Legacy Claim records may be mapped to an initial ClaimRevision only when proposition identity and history are unambiguous. Ambiguous records must be quarantined for governed resolution; they must not be auto-merged or silently assigned a new identity.

## 6. Required Phase 2 test inventory

The eventual implementation must provide deterministic tests for at least:

- DM2-01: stable ClaimRef across revisions and unique ClaimRevisionRef.
- DM2-02: invalid/mismatched revision parent rejected; accepted revisions are immutable.
- DM2-03: all CI-01–CI-13 classification vectors produce the specified NEW_CLAIM/NEW_REVISION outcome.
- DM2-04: exact ClaimRevisionRef resolution; no current-head substitution.
- DM2-05: Fact and Claim identities are distinct; FactRevision pins exact ClaimRevision/Evidence/Provenance.
- DM2-06: missing or invalid I authorization reference prevents Fact publication (after I decision is frozen).
- DM2-07: Entity label alias does not merge identity; referent change requires new identity and lineage.
- DM2-08: invalid typed Relation endpoint and unregistered relation type are rejected.
- DM2-09: Relation time/scope/lifecycle dimensions remain independent.
- DM2-10: Evidence role, availability and source scope are enforced independently.
- DM2-11: Provenance source/version lineage or explicit unavailable reason is mandatory.
- DM2-12: common source ancestry is not counted as independent Evidence.
- DM2-13: unknown/approximate time is not promoted to exact or timeless validity.
- DM2-14: Phase 1 serialization/migration compatibility and all 13 Phase 1 regression tests remain valid.

These are acceptance requirements for future implementation, not claims that tests have been written or run.

## 7. Decisions intentionally left open

- Relation vocabulary registry governance and compatibility/versioning.
- Formal Scope composition algebra.
- Fuzzy/approximate time canonical representation details.
- Whether Entity profile revisions require a first-class EntityVersion type.
- Provenance DAG cycle/compaction policy.
- Physical Schema, DDL, serialization and public API.
- D canonical commit/Forget integration.
- I security/Attestor authorization contract.
- H wire mapping and schema.
- Implementation and conformance status.

## 8. Cross-owner decision register

| ID | Exact question | Responsible Owner(s) | Exit condition |
|---|---|---|---|
| B-P2-XO-01 | What exact domain-side Attestor reference may B store, and what I-issued AuthorizationDecisionRef proves the Attestor is authorized for this Fact/Scope/Method? | I (security authority), B (domain binding) | I publishes/accepts the security-side reference contract; B and I agree the exact version/SHA; D confirms canonical persistence reference handling |
| B-P2-XO-02 | What canonical commit, immutable revision, dependency registration and Forget semantics apply to ClaimRevision/FactRevision and their Evidence/Provenance edges? | D, with B | D accepts the exact domain reference/commit boundary and dependency/Forget handling; B records the agreed binding without changing D's contract |
| B-P2-XO-03 | How are Entity merge/split identity lineage and historical typed-reference migration committed without rewriting immutable history? | D, with B | D confirms canonical commit/history mechanism; B freezes only the domain-side meaning |
| B-P2-XO-04 | How are Relation cross-scope references authorized and how do policy decisions bind to the typed endpoints? | I, with B | I defines authorization binding; B preserves Scope semantics without defining grants |
| B-P2-XO-05 | Is canonical commit/transaction time part of the domain temporal object or storage-only metadata? | D, with B | D gives an explicit decision; B aligns TemporalRef without assuming storage semantics |

All five rows are **PENDING CROSS-OWNER DECISION**. No security, canonical persistence, Forget, or wire semantics are unilaterally decided here.

## 9. Phase boundary and status

Phase 2 implementation status at this branch:

| Specification row | Status | Executable proof |
|---|---|---|
| ClaimRef / ClaimRevisionRef / ClaimRevision | TYPED | `dm2_01_claim_revision_parent_must_belong_to_same_claim`; `dm2_02_claim_revision_is_append_only_and_immutable` serializes the parent before/after successor append and proves byte-identical preservation; restored Phase 1 assertions: `claim_revision_ref_constructs_and_validates`, `claim_revision_ref_rejects_empty_id`, `claim_revision_constructs_and_preserves_stable_identity_across_revisions`, `claim_revision_rejects_empty_scope_and_empty_reference`; compile-fail doctests prove cross-ref mixing and mutation are rejected |
| FactRef / FactRevisionRef / Fact / FactRevision | TYPED | `dm2_03_fact_refs_are_distinct_and_fact_pins_exact_claim_revision`; `dm2_09_fact_pinning_does_not_follow_claim_head_after_append` appends Claim revision 2 and resolves the Fact's unchanged exact revision-1 pin; `dm2_04_fact_cannot_be_constructed_without_claim_evidence_provenance`; restored Phase 1 assertions: `fact_revision_ref_constructs_and_validates_independently`, `fact_revision_ref_rejects_empty_id`, `fact_revision_constructs_and_binds_exact_claim_revision_and_authorization`, `fact_revision_rejects_missing_method_scope_and_empty_references`; `fact_with_placeholder_attestor_validates_today` pins the known temporary placeholder window; compile-fail doctest proves confidence/Verified alone cannot construct Fact |
| ClaimRef / FactRef construction | TYPED | Restored Phase 1 assertions: `claim_ref_constructs_and_validates`, `claim_ref_rejects_empty_id`, `fact_ref_constructs_and_validates_independently`, `fact_ref_rejects_empty_id`; `all_macro_generated_refs_reject_empty_id` exercises empty-ID rejection for all ten macro-generated ref types; constructor and post-deserialization empty-ID validation are both covered |
| Entity identity extension | TYPED | `dm2_05_entity_merge_requires_successor_lineage_but_alias_does_not` proves A redirects to B, B does not redirect to A, and A's aliases/scoped external identifiers are migrated to B |
| Relation typed endpoints and valid-time distinction | TYPED | `dm2_06_relation_endpoint_kind_is_checked_against_definition` rejects (Entity, Claim) under an (Entity, Entity) vocabulary; `dm2_08_unknown_valid_time_is_not_timeless` |
| Evidence extension | TYPED | `dm2_07_evidence_extension_requires_integrity_and_scope` |
| Provenance graph expansion | NOT TYPED | Only the `ProvenanceRef` newtype exists; no expanded Provenance record or DAG validation |
| MemorySource expansion | NOT TYPED | Explicitly out of scope for this implementation round |
| Temporal precision/timezone/certainty expansion | NOT TYPED | Only Relation's Unknown-versus-AllTime valid-time distinction is typed/tested |
| I authorization and Attestor semantics | PLACEHOLDER ONLY — KNOWN CONSTRUCTION WINDOW | `pending_i()` is public; `FactRevision::validate` cannot distinguish the placeholder from a real I-issued reference. `fact_with_placeholder_attestor_validates_today` deliberately records this behavior; closing it requires I's contract and non-forgeable validated refs |
| D canonical commit semantics | PLACEHOLDER ONLY — KNOWN CONSTRUCTION WINDOW | `pending_d()` is public; `FactRevision::validate` cannot distinguish it from a real D-issued commit reference. Closing it requires D's contract and non-forgeable validated refs |
| Fact disposition after pinned ClaimRevision retraction | RESOLVED | `OWNER-DECISION-FACT-RETRACTION-001` selects candidate 3: append a successor FactRevision with `FactOutcome::Revoked`. No `retracted` field is added and no existing FactRevision is mutated. Propagation trigger, scope, mixed-dependency treatment and read-path behavior remain undefined |

The Entity, Relation and Evidence Phase 1 structs remain source-compatible; their Phase 2 semantics are represented by additive extension records. Claim remains unchanged; ClaimRevision is additive. Fact construction requires a complete initial FactRevision and its required I/D placeholders.

- Phase 1: implemented bounded core; this implementation does not reopen its accepted invariants.
- Phase 2: the listed rows are TYPED only to the extent shown above; NOT TYPED rows remain open. The implementation is not accepted and requires independent review.
- Phase 3: NOT ASSESSED and NOT CLAIMED COMPLETE.

The code and tests are present on this branch. Test execution is reported separately; no self-approval or acceptance is claimed.
## 10. References

All repository sources below were read at baseline `1ad6c2cf67a228f597fcbe1c7149c328ecbf38e9`:

- `02-domain-model/domain-model-overview.md`
- `02-domain-model/core-entities.md`
- `02-domain-model/relationships-and-provenance.md`
- `02-domain-model/epistemic-and-temporal-semantics.md`
- `02-domain-model/lifecycle-model.md`
- `02-domain-model/scope-and-permission-model.md`
- `02-domain-model/phase-1-domain-model-freeze.md`
- `02-domain-model/phase-1-memory-store.md`
- `02-domain-model/phase-1-sqlite-adapter-contract.md`
- `02-domain-model/phase-1-storage-trait-contract.md`
- `crates/memory-domain/src/lib.rs`
- `06-memory-context/context-versioning.md`
- `06-memory-context/context-architecture.md`
- `08-bmcp-protocol/owner-snapshot-namespace-and-fence-currentness-contract.md`
- `14-ai-development/work-items/GAP-BASELINE-001.md`
- `14-ai-development/prompts/owners/B/owner-session-v2.md`
- `14-ai-development/prompts/global/chatgpt-session-contract-v1.md`
