# Module B — Domain Model Baseline & Redlines

- Module: B — Domain Model Architect
- Proposal version: 0.1.0
- Status: **PROPOSED — B Owner review required; not APPROVED**
- Owner branch: `session-b-domain-model-phase3`
- Prepared against observed branch tip: `0cf703a3fec9921aeb8e6252a8ac4708b8b723b3`
- Scope: logical domain semantics, typed references, object identity, temporal/epistemic qualification and domain conformance
- Template note: `00-governance/module-baseline-and-redlines-template.md` was not found in the live governance directory. This proposal uses the repository's existing DECIDED / CANDIDATE / OPEN / TO_VALIDATE vocabulary and preserves this template gap as OPEN.

## 1. Purpose and authority

B defines the logical meanings, identity semantics, typed relationships, field constraints, cardinalities, temporal and epistemic interpretation, scope binding rules and cross-object invariants of the Brain domain model.

B does not own:
- I's authentication, issuer trust, authorization, delegation policy, PermissionEpoch or global governance;
- H's BMCP wire encoding, envelope, serialization, transport or Adapter protocol;
- D's Canonical Commit, canonical persistence, Memory authority or Forget operation;
- E's durable ingestion, extraction algorithm, producer admission or publication gate;
- F's retrieval/ranking/index/cache execution;
- G's Context membership, ContextVersion, Applied or reconciliation state;
- C's Agent telemetry, final-request evidence or protected-region enforcement;
- Storage DDL, transaction implementation, deployment or recovery.

B may define the meaning of a typed reference; it cannot turn that reference into authentication, permission, transport encoding or persistence behavior.

## 2. Status vocabulary and evidence discipline

- **DECIDED** — explicit B-owned normative logical semantics in an existing B artifact.
- **PROPOSED / CANDIDATE** — B recommendation or candidate requiring the relevant authority's decision.
- **OPEN** — unresolved semantic, compatibility or consumer question.
- **ADR-BLOCKED** — blocked by a required formal ADR decision; no downstream inference may bypass it.
- **TO_VALIDATE** — requires schema conformance, consumer tests or implementation evidence.
- **NOT RUN** — test specification exists without reproducible execution.

Artifact existence is not Owner approval, governance approval, implementation or conformance. A consumer mapping is not consumer acceptance unless the consumer Owner explicitly accepts the exact version.

## 3. Canonical domain baseline

### 3.1 DECIDED logical concepts

The following are distinct domain concepts:
- Event — captured occurrence, observation, report or transition; not automatically objective truth.
- Memory — retained, addressable knowledge asset; not a truth guarantee.
- Memory Version — immutable snapshot of a Memory; current-pointer mechanics belong to canonical storage authority.
- Claim — proposition about an Entity, Event or state, qualified by epistemic and temporal metadata.
- Entity — identity-bearing referent, not a mention string.
- Relation — typed association with endpoint, scope and optional validity interval.
- Evidence — source material or observation that supports, refutes or qualifies a Claim/Relation.
- Provenance — origin and derivation lineage.
- Memory Source — typed lineage edge from a derived asset to an exact source/version where possible.
- Memory Context and Context Entry — task-oriented scoped selection and its references; not a second canonical Memory.
- Agent Scope and Environment Scope — logical ownership/applicability namespaces.

A single universal status field is prohibited. Epistemic status, lifecycle state, temporal qualification, confidence, relevance, trust and evidence strength are orthogonal.

### 3.2 DECIDED object invariants

1. Event is not Memory; Evidence is not Claim.
2. Claim is a proposition, not its source.
3. Memory identity remains stable across immutable versions.
4. Unknown is explicit; it is not fabricated or interpreted as timeless.
5. Derived assets preserve source and derivation lineage, or explicitly record why provenance is unavailable.
6. Intent, plan, prediction and pending action do not imply completed outcomes.
7. Relations are typed; co-occurrence alone is not a Relation.
8. Scope is not permission.
9. Context Entry does not own or mutate Canonical Memory.
10. Context Remove is not Forget.
11. Conflicting Claims retain evidence and resolution history.
12. Confidence, Trust, Relevance and Evidence Strength are not interchangeable.

## 4. Fact / Claim semantic conflict — mandatory ADR boundary

**ADR-001 remains ADR-BLOCKED. This proposal does not resolve it.**

The current repository contains a normative conflict:
- Governance invariants/design principles and README distinguish Fact and Claim.
- Current Domain Model Overview describes Claim as the canonical proposition object and Fact as a qualified interpretation rather than a separate object.
- ADR-001 documents two candidate options and recommends Option A, but records no named formal decision authority, approver, decision timestamp, approved option or approval artifact.

B's Option A recommendation is a recommendation only. Option B is also not approved. Until the designated Architecture Governance authority records a formal ADR decision:
- no separate canonical Fact identity/schema/API may be frozen;
- no consumer may assume a stable FactRef or FactRevision contract;
- E must retain neutral candidate proposition/extraction representations;
- D must not freeze canonical Fact/Claim persistence shape based on either option;
- F/G/H must not freeze dependent fields or wire contracts;
- C telemetry remains source/producer evidence, not Fact attestation;
- dependent mapping remains candidate or blocked.

Any proposal-dependent content MUST be labelled ADR-BLOCKED, not DECIDED.

## 5. Typed reference baseline

### 5.1 Reference classes and semantics

| Reference | B semantic responsibility | Explicit non-meaning |
|---|---|---|
| PrincipalRef | Typed reference to a security subject | Not proof of authentication; I owns trust/policy |
| IssuerRef | Typed reference to an identity/assertion issuer | Not automatically trusted |
| ActorRef | Per-operation attribution tying a Principal to authenticated context and optional Agent/Adapter/Producer/delegation refs | Not a credential, permission or bearer token |
| AgentRef | Logical Agent identity | Not Agent instance, Principal or Adapter |
| AdapterRef | Registered Adapter/application/instance reference | Not the logical Agent |
| ProducerRef | Typed source/workload identity reference | Payload producer ID is not authentication |
| ScopeRef | Ownership or applicability namespace | Not Permission or access grant |
| EnvironmentRef | Authoritative environment/world/save/simulation identity | Not free-text label or environment version |
| DelegationChainRef | Typed reference to a separately verifiable bounded delegation chain | Not identity conversion or inherited unrestricted authority |
| PermissionDecision / PermissionEpoch | Policy decision and policy-domain epoch as consumed typed values | I-owned semantics; not B-created authorization |

### 5.2 Actor binding rules

- ActorRef attribution MUST preserve the authenticated PrincipalRef, trusted IssuerRef and verifier-owned authentication-context reference, with optional AgentRef, AdapterRef, ProducerRef and DelegationChainRef.
- Payload-supplied ActorRef/PrincipalRef/AgentRef/AdapterRef/ProducerRef/issuer/scope/environment values are claims, not proof.
- Receiving boundaries compare claims with authenticated H transport/session/workload bindings and I authoritative registries.
- A mismatch, unknown issuer, unresolved reference, expired/revoked delegation or ambiguous binding fails closed.
- Delegation is a bounded, verifiable grant chain; effective authority is the intersection of grantor authority and delegated action/resource/scope/audience/purpose/time constraints.
- Exact serialization is H-owned and remains OPEN until H's schema decision.

### 5.3 Scope rules

- ScopeRef identifies an ownership or applicability boundary; authorization is a separate I policy decision over Principal, action, resource, purpose, audience and resolved Scope.
- Ownership Scope and applicability Scope are distinct roles; a set of ScopeRefs is not an implicit union or visibility expansion.
- Parent/child, cross-tenant and cross-environment relationships do not imply permission.
- Missing required Scope dimensions are not wildcards.
- Scope resolution and authorization must be checked at each protected operation boundary.

### 5.4 Environment rules

Environment identity is a typed, authoritative binding. Free-text world/project/save labels are not sufficient where isolation matters. Environment-dependent Events, Evidence, Claims and Relations must preserve the exact environment association and relevant version/time. Cross-environment mapping requires explicit authorized mapping; consumers must reject or quarantine ambiguous environment identity.

## 6. Epistemic, temporal, evidence and provenance baseline

- Claim epistemic states currently defined in B artifacts: Observed, Reported, Inferred, Verified, Disputed and Retracted. These do not determine Memory lifecycle.
- Memory lifecycle vocabulary: Candidate, Consolidated, Active, Superseded, Archived and Forgotten. Lifecycle policy/execution belongs to the Lifecycle Manager and governance authority; B defines meanings only.
- Event time, observed time, recorded time and valid time are distinct. Preserve source precision, timezone/clock quality and Brain recorded time where applicable.
- Temporal intervals are explicit; missing interval does not mean timeless.
- Evidence supports, refutes or qualifies a proposition; it is not itself a truth score.
- Provenance identifies exact sources, versions, transformations, methods and input digests. Copies of one source do not become independent corroboration.
- Corrections/retractions preserve history and lineage; retraction is not physical erasure or Forget.
- Evidence-strength rubric and numeric scoring remain TO_VALIDATE; no normative formula is introduced here.

## 7. Domain interface contracts

| Contract | Logical input/output obligation | Authority boundary / status |
|---|---|---|
| Event envelope | Stable event identity, kind, source, payload/source ref, times, Scope/Environment, classification, schema version and conditional idempotency | B semantics DECIDED; E/H own durable receipt and wire encoding |
| Memory / MemoryVersion | Stable Memory identity, immutable version, parent/version lineage, Claim snapshots, typed refs, provenance and digest | B logical semantics DECIDED; D owns canonical commit/storage |
| Claim | Subject, predicate, typed value, polarity, epistemic/temporal qualification, evidence basis, Scope and provenance | Claim concept DECIDED; Fact split ADR-BLOCKED |
| Entity / Relation | Typed identity and endpoints, vocabulary, cardinality, scope, temporal validity and lifecycle | B defines domain meaning; entity/relation manager owns execution |
| Evidence / Provenance | Source ref, locator, times, role, scope, integrity and derivation lineage | B defines logical contract; E/D own processing and canonicalization |
| Actor / Scope / Environment refs | Typed refs and resolution semantics | B type meaning; I trust/authorization; H transport; C/D/E validate at their boundaries |
| Lifecycle | Separate asset lifecycle from Claim epistemic status | B state meanings DECIDED; lifecycle manager/governance executes |
| Context references | ContextEntry references canonical versions without owning them | G owns Context membership/version/Applied; B defines referenced object semantics |

No B logical field definition is a database DDL or BMCP wire schema.

## 8. Security and privacy redlines

1. No domain object or reference can grant authority by its presence or shape.
2. ActorRef is attribution, not authentication; ScopeRef is boundary, not permission.
3. Payload IDs and self-reported issuer/Agent/Adapter/Producer labels are untrusted claims until validated.
4. Unknown or mismatched identity/scope/environment fails closed; never silently coerce to an untyped string or wildcard.
5. Evidence authenticity does not prove proposition truth.
6. Model confidence, repetition, extraction score or generated summary cannot alone create Verified Claim or Fact.
7. Provenance and trust labels cannot be silently dropped during compaction, summarization or transformation.
8. Cross-scope or cross-environment references cannot be resolved by convenience fallback.
9. Retention, privacy, erasure and Forget policy are I/D/governance-owned; B does not promise physical erasure.
10. Canonical storage, transaction and version-pointer atomicity are D/Storage-owned; B does not claim persistence behavior.

## 9. Conformance and validation requirements

B domain conformance MUST verify:
- required fields, types, nullability, enum values and version compatibility;
- typed reference resolution and namespace separation;
- Event/Memory/Claim/Evidence/Provenance non-aliasing;
- immutable MemoryVersion and exact parent/current-version semantics at the consuming boundary;
- temporal distinctions and explicit unknown values;
- Claim epistemic status independent from Memory lifecycle;
- typed Relation endpoint/cardinality/scope/valid-time constraints;
- evidence/provenance lineage completeness or explicit unavailable reason;
- ActorRef/PrincipalRef/ScopeRef/EnvironmentRef separation and fail-closed invalid cases;
- Fact/Claim-dependent validation is blocked or candidate-only until ADR-001 is formally decided.

Required negative cases include forged ActorRef, payload Principal mismatch, unknown Issuer, expired delegation, ScopeRef treated as permission, missing Scope, cross-Scope resolution, EnvironmentRef mismatch, unknown temporal bounds, plan promoted to outcome, Evidence promoted to truth, duplicate-source evidence counted independently, stale Claim revision, and unauthorized lifecycle/Forget mutation.

Test reports must include schema/version, fixture, operation order, expected/actual result, exact source/build SHA, reproducible command, logs and Owner review. Specifications without execution are NOT RUN. No implementation or test pass is claimed by this proposal.

## 10. Acceptance criteria

B proposal is ready for B Owner review when:
1. Domain object definitions and invariants are explicit and internally consistent.
2. Logical domain semantics are separated from storage, wire, policy and runtime execution.
3. Typed reference meanings and non-authorities are explicit.
4. Scope and permission, identity and authentication, evidence and truth are distinct.
5. Epistemic, temporal and lifecycle dimensions remain orthogonal.
6. ADR-001 is visibly ADR-BLOCKED and no downstream Fact/Claim freeze is inferred.
7. Interfaces name producer/consumer/authority boundaries.
8. Conformance and negative-test requirements are reproducible.
9. OPEN and TO_VALIDATE items are retained rather than silently resolved.

## 11. Change authority and compatibility

- B may change B-owned logical object semantics, typed reference meanings, field constraints, cardinalities, temporal/epistemic definitions and domain invariants through versioned B decisions.
- B may propose but cannot approve Fact/Claim governance changes, I authorization policy, H wire encoding, D canonical commit or G Applied semantics.
- Breaking logical changes require impact analysis, versioned migration semantics and explicit acceptance by affected consumers.
- Existing canonical identity/revision history must not be silently rewritten.
- B must not edit I/H/C/D/E/F/G Owner artifacts to manufacture cross-owner acceptance.

## 12. Open / blocked / validation register

| ID | Item | Status | Required authority / evidence |
|---|---|---|---|
| B-G0-01 | Canonical governance template absent at requested path | OPEN | Governance Owner to publish/identify canonical template |
| B-G0-02 | Fact/Claim separate-object versus qualified-view decision | ADR-BLOCKED | Designated Architecture Governance authority; formal ADR-001 record |
| B-G0-03 | Principal/Actor/Issuer trust and authorization binding | OPEN | I policy and H authenticated transport; exact B/I/H acceptance |
| B-G0-04 | Typed ScopeRef cross-scope and cross-environment policy alignment | OPEN / cross-owner | I/Governance registry and consumer decisions |
| B-G0-05 | EnvironmentRef authoritative registry and issuer | OPEN | Environment Registry Authority designation; I trust binding |
| B-G0-06 | Exact H wire encoding for typed refs | OPEN | H-owned schema and versioned compatibility decision |
| B-G0-07 | D canonical IDs, persistence and version commit mechanics | OPEN / external | D canonical authority and Storage realization |
| B-G0-08 | Evidence strength/independence rubric | TO_VALIDATE | Domain use cases and reproducible evaluation |
| B-G0-09 | Consumer schema conformance across C/D/E/F/G/H/I | TO_VALIDATE / NOT RUN | Consumer-owned tests and exact-version acceptance |
| B-G0-10 | Lifecycle thresholds, retention/backup/erasure policy | OPEN | Lifecycle/governance and I/D authority |

## 13. Evidence inspected

- B branch: `session-b-domain-model-phase3`, observed pre-write HEAD `0cf703a3fec9921aeb8e6252a8ac4708b8b723b3`.
- `02-domain-model/ADR-001-fact-claim-semantics.md` Blob `a1024938ff5baba069cf128c69496a44e143330c`.
- `02-domain-model/domain-model-overview.md` Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346`.
- `02-domain-model/core-entities.md` Blob `8cb5a674eec8eac1f3c4d83c400dc08d00166f23`.
- `02-domain-model/typed-reference-registry.md` Blob `08af297cb010f7e6ac5e3f29daa4469be112e12e`.
- `02-domain-model/typed-reference-and-scope-semantics.md` Blob `e9a6bd21e06bc02a5208619f5a949217860b1c00`.
- `02-domain-model/relationships-and-provenance.md` Blob `e762f84c59f69de7a44baad2123aed46e1ffea16`.
- `02-domain-model/lifecycle-model.md` Blob `81c48c928cb5f9c76ca29d493fbd9479079e62f7`.
- `02-domain-model/principal-actor-binding-mapping.md` Blob `bbbef919e1e2ffe158cda8d9b2c5e718efaae969`.

## 14. Proposal disposition

**PROPOSED 0.1.0.** This is a B-owned logical domain baseline proposal, not an Architecture Governance decision, not an I authorization policy, not an H wire schema, not a D canonical storage decision, and not implementation or conformance approval. ADR-001 remains **ADR-BLOCKED**.
