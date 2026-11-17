# Canonical Domain Relationships
# 规范领域关系

- ID: B-REL-001
- Status: CANDIDATE RELATIONSHIP MODEL; owner-owned cardinalities require acceptance
- Sources: core entities Blob 8cb5a674eec8eac1f3c4d83c400dc08d00166f23; relationships/provenance Blob e762f84c59f69de7a44baad2123aed46e1ffea16; identity closure Blob 0a6b78a842e550b58533b797cdfcd2d954ed6826; G Context Blob c1de241ec69834377d9b0e24aa4770a809796d4b.

## 1. Relationship kinds / 关系类型

- **Composition:** child is a constituent of parent and its lifecycle is constrained by parent; does not automatically imply shared physical row.
- **Association:** typed semantic link between independent objects; both identities remain independent.
- **Reference:** typed pointer; does not imply ownership, permission, or composition.
- **Derivation:** target produced from source(s) through a declared process; source/target direction is immutable and traceable.
- **Ownership:** authority/custody relationship defining who may govern lifecycle; distinct from applicability and authorization.
- **Causal:** establishes an evidenced before/after or cause/outcome relation; timestamps alone may be insufficient for concurrency order.
- **Temporal:** states when a relation/assertion holds; separate from record lifecycle and transaction time.

## 2. Core relationship matrix / 核心关系矩阵

| Source → Target | Kind | Cardinality / optionality | Owner | Lifecycle / referential integrity | Forget / deletion semantics | Cross-Tenant / version rules |
|---|---|---|---|---|---|---|
| Memory → MemoryVersion | Composition / version ownership | 1 Memory : 1..N immutable Versions; current pointer exactly 1 after first commit | D; Storage persists | Version immutable; parent Memory stable; version sequence monotonic, no reuse | Forget gates content access across identity/version family and registered descendants; physical erasure separate | Version ref must bind Memory ID + version ID; no cross-tenant alias |
| MemoryVersion → ClaimSnapshot | Composition (candidate) | 1 version : 0..N snapshots; empty only for declared non-propositional kind | B semantics; D canonical; E producer | Immutable snapshot; Claim identity across versions OPEN | Source evidence/claim lineage subject to D/I Forget; no plaintext retention beyond policy | Claim ref and snapshot identity must not be conflated |
| Claim → Evidence | Association | N:M; one Claim needs ≥1 epistemic basis for Verified; Evidence may support/refute multiple Claims | B semantics; E evidence production; I access policy | Link role/strength/time/scope is Claim-relative; link versioned/immutable if assessed | Forget may suppress Evidence and dependent claims; preserve only permitted non-reconstructive metadata | Both ends independently scope-authorized; no implicit cross-tenant support |
| Evidence → Source | Reference / origin association | Each Evidence 1 source_ref; a Source may have 0..N Evidence | E source capture; B type semantics | Typed source identity/version; source may be external/unavailable | Source retention policy controls content; Evidence availability updated without erasing historical existence | Source refs namespaced by issuer/authority; external IDs never canonical IDs |
| Memory → MemorySource | Association (default) | 0..N source links per Memory; each link one source ref + role/locator/scope | B semantics; E produces; D persists | Promote MemorySource to entity only if link itself has independent lifecycle/identity | Link removed/suppressed per Forget; source data handled separately | Typed source version and Scope; no string-only identity |
| Derived Memory → Source Memory / Event | Derivation | Derived target 1..N direct source refs; sources 0..N targets | E production; D lineage/fence | Immutable lineage manifest; preserve transitive ancestry and exact versions | D registers dependencies before visible; source Forget suppresses descendants according to fence | Every source edge independently scoped/authorized; no cross-tenant derivation without I-approved explicit grant |
| Derived Artifact → Provenance | Composition/reference | 1 target : 1..N provenance refs or explicit unavailable reason | B semantics; E producer | Provenance captures method/version/time/input digests; graph cycle policy OPEN | Forget may restrict provenance payload; non-reconstructive audit metadata only | Preserve source namespace and issuer; no unverified model attribution |
| Entity → Relation | Association | Entity 0..N Relations; Relation has exactly two typed endpoints in current binary model | B semantics; Entity/Relation Manager | Endpoint types validated; Relation has own ID, type, direction, qualifiers, Valid Time and evidence | Forget/scope policy applies to endpoints and relation; do not leave dangling disclosure path | Both endpoints independently authorized; explicit cross-scope relation does not grant access |
| Relation → Evidence | Association | N:M | B semantics; E evidence | Evidence support is relation-relative | Same as Claim–Evidence; retain only permitted metadata | Each Evidence dereference separately authorized |
| Principal → ActorRef | Attribution/reference | 1 Principal : 0..N ActorRefs; each ActorRef resolves to 1 Principal and one operation context | B ActorRef type; I Principal validation; H verifier binding | ActorRef immutable per operation; distinct session/delegation context requires distinct ref | Revocation does not rewrite historical ActorRef; current authorization rechecked | Issuer/security-domain namespace required; no cross-tenant implicit identity |
| Principal → Agent/Adapter/Producer | Registered binding association | N:M only through explicit registry mapping | I trust/Principal; C/H/E registry owners | Workload identity distinct from security Principal; instances/epochs separate | Revocation disables new operations; historical attribution retained | No string equality or implicit inheritance; I policy controls scope |
| Scope → Domain Asset | Ownership/applicability association | Asset 1..N role-tagged ScopeRefs; Scope 0..N assets | B type; I/G policy | Ownership Scope and Applicability Scope are distinct roles | Scope closure/revocation restricts access; does not silently delete asset | Fail closed for ambiguous tenant/security-domain mismatch |
| Environment → Scope / Claim / Relation | Reference + temporal qualification | 0..N associations; environment-bound Claim/Relation requires exact EnvironmentRef | B type; I bridge policy; environment registry owner | EnvironmentRef distinct from Environment Scope and revision | Environment retirement does not erase history; bridge access policy-controlled | Cross-environment denied by default absent explicit mapping/authorization |
| Context → ContextVersion | Composition/version ownership | 1 Context : 1..N immutable ContextVersions; current pointer one | G | ContextVersion is desired-state snapshot, immutable; CAS/ChangeSet semantics G-owned | Forget invalidates current-use membership and delivery; historical snapshot audit-only if policy allows | Context scope-bound; never cast to MemoryVersion |
| ContextVersion → ContextEntry | Composition | 1 version : 0..N entries | G | Entry references exact Memory ID + MemoryVersion; membership changes create new ContextVersion | Remove is membership change, not canonical Forget; Forget invalidates affected entries | Source Memory scope checked independently; no scope inheritance |
| ContextVersion → ChangeSet | Association / causal | 0..N ChangeSets; each ChangeSet binds exact base/target digest and outcome | G | Stale base rejected; applied/committed reconciliation run separate from version state | Superseded ChangeSet cannot be replayed as current delivery | Exact ContextVersion references; no cross-scope mutation |
| F Retrieval → G Context | Reference/selection handoff | One retrieval request yields 0..N candidate refs; G selects 0..N | F supplies candidate/rank; G owns membership | Candidate list may be incomplete/truncated; G revalidates canonical refs | Forgotten/suppressed refs cannot be selected or delivered | Scope authorization per ref; F Working Set is not Context |
| Delivery → ContextVersion | Reference | Each Delivery targets exactly one ContextVersion + attempt; version may have 0..N attempts | G; H transports | Attempt immutable; late ACK historical only; no head rollback | Forget/revocation cancels/supersedes and blocks late Applied | Exact Adapter/session/capability binding |
| CSubmitOutcome → Delivery/ContextVersion | Causal/reference | Each outcome binds one exact final request, delivery attempt and ContextVersion; retries preserve operation identity when outcome unknown | C | Immutable provider-boundary evidence; Unknown/InDoubt non-terminal | Must not promote to Applied without G validation; current-use can be invalidated later | Exact request digest, Scope, Environment, Actor/Principal binding |
| G Applied Record → C/H/I/D evidence | Evidence association | Each Applied record references one exact request boundary and required evidence vector | G commits; C/H/I/D issue evidence | Historical Applied immutable; current-use eligibility separate | Forget/revocation invalidates current use, not historical truth | All issuer, scope and authority-specific epochs validated |
| Operation → Protocol Message | Reference/correlation | 1 operation : 0..N protocol messages; each message references one operation/attempt/correlation | Operation owner + H wire | Message is not operation state; ACK bounded to message/action | Deletion/Forget operation state not represented by arbitrary protocol status | Wire reference preserves typed operation identity |
| ForgetOperation → ForgetFence / Targets | Causal/ownership | One operation establishes 0..N target fences; target set immutable per operation version | D; I policy | Fence generation monotonic; target/source/ancestor lineage; barriers tracked | D CanonicalSuppressionComplete distinct from I global completion and physical purge | Scope and target inventory exact; no cross-tenant omission |
| Storage PublicationReceipt → VisibilityPointer | Composition/transaction evidence | Published artifact has one matching authoritative pointer and receipt | Storage | Pointer + receipt + owner outcome atomically committed per proposed JF-10; exact readback required | Private staged bytes never visible; physical purge separate | Receipt binds exact operation/digest/XID/owner boundary; no stale replica inference |

## 3. Referential integrity invariants / 引用完整性不变量

1. Every reference carries a type discriminator and namespace; no implicit casts between entity types.
2. Every Relation endpoint satisfies the registered relation-type endpoint constraints.
3. Every derived object has complete direct/transitive lineage or an explicit unavailable reason; incomplete lineage cannot be published.
4. A derived edge must not point from target to source ambiguously; derivation direction is explicit.
5. Cross-Tenant/Scope/Environment references do not grant access; every endpoint and Evidence dereference is separately authorized.
6. Historical references remain typed and resolvable as historical identity even after retirement/supersession; current-use eligibility is separate.
7. A Context Entry references an exact MemoryVersion; ContextVersion does not replace canonical Memory version.
8. Protocol messages and receipts reference operations but do not become canonical domain entities by name similarity.
9. Deletion/Forget propagation is governed by owner lifecycle and registered dependencies, not generic cascading foreign-key deletion.
10. A missing reference, unavailable authority or ambiguous namespace is UNKNOWN/BLOCKED, not success.

## 4. Cardinality and modeling questions / 基数与建模问题

- Claim↔Evidence may require a first-class assessment entity if link-specific strength, role, time and provenance must be independently revised. Otherwise a typed association value is sufficient.
- Provenance may be a first-class entity when an independently addressable derivation record is required; otherwise typed lineage edges plus immutable target version may suffice. OPEN.
- MemorySource should default to a typed association/value object; standalone Source entity is deferred unless it has independent identity/lifecycle.
- ContextEntry is currently separately identified by G schema; B defers its final entity/value classification to G.
- ForgetOperation and Storage PublicationReceipt are owner-owned operation/evidence objects, not generic Memory children.

## 5. Gate status / 门禁状态

B2 remains IN PROGRESS; B3 remains NOT PASSED. This matrix records candidate semantic relationships. It does not prescribe database foreign keys, cascading deletion, aggregate transaction boundaries, or storage schema.

B2 仍在进行；B3 未通过。本矩阵记录候选语义关系，不规定数据库外键、级联删除、聚合事务边界或存储 Schema。
