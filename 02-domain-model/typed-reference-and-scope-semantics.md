# Typed Reference and Scope Semantics

- **Status:** CANDIDATE domain contract; normative only after dependent ADR/identity approvals
- **Owner:** Memory Domain Model (B)
- **Related issues:** INT-P0-01, INT-P0-02, INT-P1-02, INT-P1-03, INT-P1-06, DM-005, DM-006
- **Branch:** `session-b-domain-model-phase3`
- **Base:** `main@8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2`

## 1. Purpose and boundaries

This document defines logical identity, namespace, version pinning and lifecycle meaning for domain references. It does not define database keys, physical partitions, wire serialization, token formats, authorization grants or storage implementation.

- B owns the meaning and uniqueness boundary of domain references.
- D owns canonical Memory persistence, commit mechanics, lifecycle transition authority and canonical object storage behavior.
- E owns source acceptance, extraction and proposal generation.
- F owns indexes, retrieval projections, freshness and activation recommendations.
- G owns Memory Context membership and ContextVersion.
- H owns wire representation and authenticated transport binding.
- I owns authentication/authorization policy, delegation, revocation, retention and Forget completion policy.

A typed reference is an address to a domain identity, not proof that the caller may read or mutate the target.

## 2. Namespace model

### 2.1 Brain authority namespace

Every canonical object reference is interpreted inside one stable **BrainAuthority namespace**. The namespace is the logical authority boundary that issues canonical IDs. An opaque ID is unique within that authority namespace and is never reused for a different object. If a deployment has multiple independent Brain authorities, the authority namespace is part of the reference identity; IDs from separate authorities are not comparable or implicitly linkable.

### 2.2 Scope is not the ID namespace

Scope is an explicit domain relationship attached to an object. It qualifies ownership and applicability but is not used as a substitute for identity uniqueness.

- Object identity remains stable if an object's applicability Scope set changes through an authorized domain operation.
- Moving or sharing an object across scopes does not silently mint a new identity; it creates an auditable scope-binding change/version as defined by the owning aggregate.
- A reference's optional Scope hint is a validation/disambiguation constraint, never an authorization grant.
- Tenant/user/project boundaries may be represented as Scope kinds, but B does not define physical tenant partitioning.

### 2.3 Common reference envelope

A typed reference conceptually contains:

- `authority_namespace`: Brain authority that issued the identity;
- `object_id`: opaque, non-semantic, never-reused ID;
- `object_type`: fixed by the reference type, not caller-controlled free text;
- `version_id`: required for immutable version/revision refs; absent for stable identity refs;
- `scope_hint`: optional resolved ScopeRef for validation/context, not permission;
- `schema_family/version`: interpretation compatibility metadata where needed.

H owns encoding. The above is semantic content, not a prescribed JSON/protobuf envelope.

## 3. Typed references

### 3.1 MemoryRef

- **Target:** stable canonical Memory identity.
- **Uniqueness:** `(BrainAuthority, memory_id)`; globally unique within one BrainAuthority, not derived from content or Scope.
- **Version:** no version pin; resolves identity only. Use MemoryVersionRef for immutable content.
- **Scope:** the target has one owner Scope and zero or more applicability ScopeRefs. Reference visibility is evaluated for the exact object and operation.
- **Lifecycle:** identity persists across MemoryVersions. Superseded/Archived remain historical identities. Forgotten identity is not reused; content access may be suppressed/unavailable under I's policy.

### 3.2 MemoryVersionRef

- **Target:** one immutable committed Memory snapshot.
- **Uniqueness:** `(BrainAuthority, memory_version_id)`; must resolve to exactly one MemoryRef and sequence.
- **Version:** version identity is intrinsic; reference MUST NOT resolve through a moving current pointer. Include/resolve parent version and commit sequence for history.
- **Scope:** inherits the Memory's explicit owner/applicability binding at that version; scope changes are represented in version/history, not silently inferred.
- **Lifecycle:** immutable and never rewritten. It may be superseded by a later MemoryVersion; historical reads remain exact subject to Forget/retention. A forgotten payload can become unavailable without reassigning the ref.

### 3.3 ClaimRef

- **Target:** stable Claim identity/thread, only if the Fact/Claim ADR approves a Claim identity.
- **Uniqueness:** `(BrainAuthority, claim_id)`; stable across ClaimRevisions, not text-hash based and not reused.
- **Version:** no revision pin. It identifies the proposition thread only. Do not use it where exact asserted content matters.
- **Scope:** Claim carries owner/applicability ScopeRefs; reference checks exact target visibility. Scope changes do not alter claim_id but require an auditable revision/binding event.
- **Lifecycle:** stable identity across corrections, refinements and retractions; terminal Forget restrictions do not permit ID reuse.

### 3.4 ClaimRevisionRef

- **Target:** one immutable revision of one Claim.
- **Uniqueness:** `(BrainAuthority, claim_id, claim_revision_id)`; revision ID is unique within Claim, and the composite is unambiguous across authorities.
- **Version:** mandatory exact revision ID and monotonic per-Claim sequence; one parent except genesis. No floating “latest” semantics.
- **Scope:** must be compatible with the Claim identity and revision's explicit ScopeRefs; never broadens access by inheritance.
- **Lifecycle:** immutable after commit. A correction, epistemic change, validity correction or retraction appends a new revision; old refs remain historically meaningful subject to Forget.

### 3.5 EntityRef

- **Target:** stable identity-bearing Entity.
- **Uniqueness:** `(BrainAuthority, entity_id)`.
- **Version:** no pin; use EntityVersionRef if a consumer needs exact descriptive attributes. This document does not create an unrequested new normative ref type, but exact entity version references remain a D-owned canonical need.
- **Scope:** identity is never inferred from label. Owner/applicability scopes constrain resolution and traversal.
- **Lifecycle:** Provisional/Resolved/Merged/Split/Retired states do not reuse IDs. Merge creates explicit redirect/migration records; historical EntityRef continues to identify the original identity.

### 3.6 EvidenceRef

- **Target:** stable Evidence identity.
- **Uniqueness:** `(BrainAuthority, evidence_id)`; Evidence identity policy may use source/version + locator + digest + Scope + kind to detect duplicates, but the issued ID remains opaque and stable.
- **Version:** Evidence content/source binding MUST be immutable or point to an exact source version/digest. Changed source bytes/digest create a new Evidence identity/version or explicit integrity-conflict record, never overwrite evidence silently.
- **Scope:** Evidence has its own ScopeRefs and may be more restricted than the Claim/Memory it supports. Access to Claim does not imply access to Evidence.
- **Lifecycle:** availability may be available, restricted, expired, forgotten or external_unavailable. The reference may remain for audit while dereference is denied/unavailable.

### 3.7 ScopeRef

- **Target:** one registered Scope identity.
- **Uniqueness:** `(BrainAuthority, scope_id)`; Scope kind is part of validated metadata, not a caller-selected namespace.
- **Version:** stable identity; if containment/attributes change, a Scope descriptor revision or versioned change record is required. No consumer may assume a mutable parent pointer is historically constant.
- **Scope binding:** ScopeRef denotes a domain namespace/ownership/applicability context; it does not carry grants.
- **Lifecycle:** active, suspended, closed or retired descriptor states may constrain new domain associations. Historical refs remain resolvable under retention rules; closed/retired IDs are never reused.

### 3.8 ActorRef

- **Target:** stable actor/principal subject identity as resolved by authenticated identity infrastructure.
- **Uniqueness:** `(issuer, subject_id)` within the declared identity federation, bound to a BrainAuthority mapping where necessary. Display name, email string, Agent-supplied payload ID or model-generated label is not an identity key.
- **Version:** stable subject identity; authentication credential/key rotation and delegation changes are identity/security events, not new domain actor identities unless issuer/subject identity changes.
- **Scope:** ActorRef may be associated with multiple scopes, but association does not grant access.
- **Lifecycle:** active, disabled, revoked or unknown identity status is resolved by H/I identity services; B defines only the reference meaning. Historical attribution remains distinct from present authorization.

### 3.9 EventRef

- **Target:** one immutable accepted source Event identity.
- **Uniqueness:** `(BrainAuthority, event_id)); producer-local IDs are namespaced by authenticated producer/source identity and mapped to the Brain-issued EventRef.
- **Version:** Event payload is immutable for a given digest/version. Corrections are new EventRefs or explicit correction events linked to the original; no in-place mutation.
- **Scope:** Scope and Environment Scope are captured from trusted ingress metadata; source text cannot self-assign them.
- **Lifecycle:** accepted, processing, processed, quarantined, expired or forgotten are separate ingestion/retention states; these are not Claim epistemic statuses. EventRef remains an audit identity even if payload dereference becomes unavailable.

## 4. TimeValue and TimeInterval

TimeValue and TimeInterval are typed domain values, not globally addressable object identities.

### 4.1 TimeValue

A TimeValue represents a source-aware temporal bound or point:

- normalized instant or bounded uncertainty range;
- precision/granularity (tick, second, day, month, year, approximate);
- timezone/offset or explicit unknown timezone;
- certainty/uncertainty qualifier;
- original source phrase and locale where available;
- source EventRef/EvidenceRef or other origin reference;
- normalization method/version.

A TimeValue is not an ID. Equal normalized instants with different precision/source uncertainty are not necessarily semantically interchangeable. Unknown is explicit; it is not zero, infinity, or “all time”.

### 4.2 TimeInterval

A TimeInterval is a pair of TimeValue bounds plus boundary semantics:

- start and end bounds may be known, approximate, or explicitly unknown/unbounded;
- default interval convention is half-open `[start, end)`, unless a domain vocabulary explicitly requires otherwise;
- start after end is invalid unless the domain explicitly models an inverse/uncertain interval;
- missing interval means “validity not specified/unknown”, not “always valid”;
- unbounded start/end is distinct from unknown start/end;
- original expression and normalization uncertainty must remain traceable.

Event Time, Recorded At, Commit/Transaction Time, and Valid Time remain separate clocks.

## 5. Scope domain semantics

### 5.1 Scope definition

A Scope is a named, identity-bearing domain namespace that declares where an object belongs, is applicable, or is interpreted. Scope supports partitioning of identity resolution, provenance traversal, relationship validity, environment separation and context assembly.

A Scope is **not**:
- a permission, role, grant, ACL, policy decision or authenticated principal;
- proof that an actor may read/write objects in it;
- a security filter implementation or physical storage partition;
- a ContextVersion or a task instruction.

### 5.2 Scope kinds

Candidate registered kinds include:

- `system`: Brain authority-level namespace;
- `tenant`: tenant/customer boundary;
- `user`: user-owned domain;
- `project`: project/workspace boundary;
- `agent`: logical Agent identity;
- `agent_instance`: one Agent runtime instance;
- `task`: one task/work item;
- `session`: one interaction session;
- `environment`: one world, save file, simulation, device or isolated environment state.

The vocabulary is registry-versioned. Unknown kinds are not silently coerced to a broader Scope.

### 5.3 Containment

Candidate containment semantics:

- A Scope may have at most one **containment parent** in the canonical Scope tree; roots are BrainAuthority/system scopes.
- Containment means namespace organization and lifecycle ownership only. It does not imply permission inheritance or resource visibility.
- Cross-cutting membership (for example, one Agent participates in multiple projects) is represented by explicit typed association records, not multiple containment parents.
- Parent/child cycles are invalid. Reparenting is an auditable Scope descriptor change; historical parent relationships remain available through versioned history.
- An object has one owner ScopeRef and zero or more applicability ScopeRefs. Ownership and applicability are distinct relationships.

### 5.4 Inheritance and composition

The word “inheritance” is restricted to domain metadata and validation:

- A child Scope may inherit descriptive defaults or vocabulary constraints from its parent when the Scope-kind registry explicitly allows it.
- A child Scope does **not** inherit grants, roles, permissions, read visibility, write authority, retention exceptions or authorization decisions.
- Parent Scope membership does not automatically make child-scoped resources visible to parent-scoped queries or sibling scopes.
- Applicability across multiple scopes is explicit. Where a proposition is environment-dependent, its Environment Scope is mandatory and incompatible environment scopes cannot be merged or compared as if identical.
- Scope composition for a domain operation is an explicit set/relationship constraint; it is not an authorization expression. I defines whether a principal may perform the operation.

### 5.5 Ownership and applicability

- **Owner Scope:** exactly one primary ownership namespace for a canonical object unless a future governance-approved shared-ownership model says otherwise.
- **Applicability Scopes:** zero or more scopes in which the proposition/object is meaningful or intended to apply.
- A child-scope object does not automatically become an owner-scope object.
- Sharing across owner scopes requires an explicit domain sharing/link record and I authorization. A reference hint is never a share grant.
- Scope mismatch is a domain validation outcome; Permission Denied is an authorization outcome. They are distinct errors and must not be conflated.

## 6. Cross-module consumer rules

- **D:** stores stable identity and exact immutable version refs; validates reference existence, type, scope compatibility and parent/version lineage. D owns commit mechanics and lifecycle authority.
- **E:** carries source EventRef, ScopeRefs and Environment Scope from trusted ingress; uses candidate refs until mapping is approved; never creates canonical ClaimRef by text hash.
- **F:** filters candidate generation by trusted Scope context before candidate exposure; keys projections/caches by exact refs and relevant scope/policy epochs; revalidates canonical refs and marks lag/incompleteness explicitly. F owns retrieval, not identity.
- **G:** pins exact MemoryVersionRef in Context entries; never stores a floating MemoryRef as proof of content version. G owns ContextVersion and membership only.
- **H:** serializes these semantics into versioned wire forms and binds ActorRef to authenticated transport identity; B does not define wire format.
- **I:** resolves authorization, grants, revocation, retention and Forget policy. ScopeRef alone never authorizes.

## 7. Validation and conformance cases

1. Same opaque object ID in two BrainAuthority namespaces is not the same object.
2. Same display label in two Scopes does not prove Entity identity.
3. Moving an object applicability Scope does not silently mint a new identity.
4. Child Scope does not inherit a parent Permission or make sibling resources visible.
5. EvidenceRef may be inaccessible while MemoryRef is readable.
6. MemoryRef cannot substitute for MemoryVersionRef in a historical/pinned Context read.
7. ClaimRef cannot substitute for ClaimRevisionRef in a conflict, correction or as-of result.
8. Event producer-local ID collision is resolved by authenticated producer namespace.
9. Unknown time is not unbounded time; approximate time preserves precision/uncertainty.
10. Retired Scope IDs and forgotten object IDs are never reused.
11. Scope mismatch and Permission Denied are distinct validation/authorization outcomes.
12. Cross-environment candidate matching is rejected absent an explicit compatible domain relation and I authorization.

## 8. Dependencies and open items

- **ADR-BLOCKED:** ClaimRef/ClaimRevisionRef are conditional on ADR-001; no canonical Claim identity is authorized while INT-P0-01 remains blocked.
- **OPEN with I/H:** ActorRef issuer, federation, authenticated principal binding, delegation and revocation epochs.
- **OPEN with D:** exact version/revision reference envelopes, object lifecycle history and canonical identity allocation mechanics.
- **OPEN with H:** wire serialization and schema evolution.
- **OPEN with I:** Scope/Permission evaluation and retention/Forget policy.
- **TO_VALIDATE:** high-cardinality Scope composition, historical reference resolution and provenance traversal limits.

## 9. Source baseline and provenance

| Source | Branch/ref | Commit SHA | Blob SHA |
|---|---|---|---|
| Governance invariants | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `66266667bdbb1cf15a2644fa98db5ecaaf3bb23b` |
| Governance principles | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `192e6ba6e9287792a02b679dda0d391844270228` |
| Terminology | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `9b287ebe027ae01128baf164952ce15aad050638` |
| Domain model documents (all six) | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | See ADR-001 source table for each blob SHA |
| D canonical store | `session-d-memory-brain-2026-11-16` | `9dc08c63f6912320e290a963c634748ec44a81c8` | `4e4db0ed8847d060d235a1dedb394dfd4bda317d` |
| D versioning | `session-d-memory-brain-2026-11-16` | `9dc08c63f6912320e290a963c634748ec44a81c8` | `c32e58f7a845a9b075e68eb1c93f63649996d580` |
| D entity/relationship manager | `session-d-memory-brain-2026-11-16` | `9dc08c63f6912320e290a963c634748ec44a81c8` | `5688ef4fa682bc3e81aad5a9939e19ffc41ddf57` |
| E extraction/normalization | `session-e-memory-compiler-2026-11-16` | `54df136d1e410af834461950e3c61c5c80abd6ad` | `438f0c795fbcf8ed2c5e05615f1b96aa448efe85` |
| E consolidation/conflict | `session-e-memory-compiler-2026-11-16` | `54df136d1e410af834461950e3c61c5c80abd6ad` | `bac3123d02e726ecffd8eb73ada515dea566e7e6` |

**Branch-awareness:** D/E references were inspected from their own unmerged branches and exact commits. They are not described as main content.
