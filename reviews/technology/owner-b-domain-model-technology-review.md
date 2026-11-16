# B — Domain Model Technology Architecture Review

- Document: TAR-B-001
- Owner perspective: B — Domain Model Architect
- Execution mode: centralized delegated review by the project integration assistant; this is not an independent human-owner attestation.
- Branch: `session-b-domain-model-phase3`
- Reviewed branch HEAD: `861fa9b2c3e1f572336543b15c7dc392493891db`
- TAB-001: v0.1, blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`, path `13-engineering-decisions/technology-architecture-blueprint.md`
- Review task pack: blob `5a813edeccf7190d66dfd71a96ca581c48f8a4cb`
- B baseline/redlines: blob `410d6cc62294e1a7ee5efa0cfe4ef496a8179326`
- Fact/Claim ADR-001: blob `a1024938ff5baba069cf128c69496a44e143330c`
- Date: 2026-11-17
- Verdict: **CONDITIONAL PASS — domain technology direction is plausible; canonical schema and wire freeze remain blocked.**

## 1. Executive verdict

TAB-001's Rust + typed domain model + transactional relational metadata + immutable revisions + explicit serialization boundary is a viable candidate direction. It does not yet prove lossless representation of the complete domain. The largest blocker is not SQLite versus PostgreSQL: it is unresolved normative meaning and identity for Fact versus Claim, plus incomplete closure of typed-reference and schema evolution contracts.

B's ADR-001 remains **ADR-BLOCKED**. B's preference for Option A is a recommendation, not a decision. No Fact table, Claim qualification field, API field, or wire representation may be frozen on the strength of that preference.

## 2. R1–R6 assessment

| Dimension | Verdict | Evidence and gap | Impact |
|---|---|---|---|
| R1 Requirements/workload | CONDITIONAL | TAB preserves provenance, scope, temporal/epistemic state and immutable history, but exact field/cardinality/identity constraints must be traced to B contracts. | A schema can compile while silently losing domain distinctions. |
| R2 Boundaries/dependencies | CONDITIONAL | B owns semantics, not D persistence, E extraction, I authorization or H wire. Those boundaries are correctly stated; cross-owner typed-reference mapping still needs conformance fixtures. | Prevents duplicate authority and semantic drift. |
| R3 Technology selection | CONDITIONAL | Serde is reasonable; JSON is inspectable; CBOR/MessagePack remain candidates. Relational core plus bounded JSON payloads is preferable to an untyped document-only model. | No encoding/database choice is normative yet. |
| R4 Resources | NOT MEASURED | No corpus size, relation fan-out, provenance depth, payload distribution, write rate or migration duration measurements were supplied. GPU is not a domain-model dependency. | Storage/index sizing remains open. |
| R5 Recovery | CONDITIONAL | Immutable revisions and explicit references support recovery; schema migration, referential integrity, graph-cycle handling, merge/split replay and backup/restore tests are absent. | Corrupt or partial migration can change semantics. |
| R6 Compatibility | BLOCKED for freeze | Fact/Claim ADR blocked; ScopeRef/ActorRef/Principal and environment/temporal/epistemic mappings must remain typed and distinct across D/E/H/I. | Canonical schema and wire fields cannot freeze. |

## 3. Findings

### TAR-B-P0-001 — Fact/Claim normative model unresolved

- Evidence: ADR-001 blob `a1024938ff5baba069cf128c69496a44e143330c`; status explicitly ADR-BLOCKED. Governance invariants distinguish Fact and Claim while the current domain overview describes Claim as canonical proposition and Fact as a qualification/view.
- Consequence: incompatible canonical identity, revision, provenance and authorization semantics can be encoded by different modules.
- Recommendation: retain both candidate models in schema analysis; obtain formal Governance decision. If separate Fact is selected, require exact ClaimRevisionRef(s), attestor, method/version, evidence, Scope, validity and revocation history. If qualification is selected, governance must explicitly amend I-04/P-04/README and consumer contracts.
- Owner/dependency: Architecture Governance with B, D, I, E and H.
- Closure: signed ADR, updated invariants/terminology/consumer map, migration plan and schema compatibility tests.

### TAR-B-P1-001 — Typed identity namespace enforcement

- Consequence: interchangeable strings or untyped UUIDs can permit cross-domain confusion and invalid comparisons.
- Recommendation: Rust newtypes and serialization validation for ActorRef, PrincipalRef, ScopeRef, EnvironmentRef, MemoryRef, ClaimRef, ClaimRevisionRef, EvidenceRef and all cursor/epoch namespaces. Never numerically compare PermissionEpoch, ForgetFenceGeneration, CanonicalCommitCursor, AggregateRevision, LifecycleEventCursor, IndexWatermark or ContextVersion.
- Closure: compile-time type tests, invalid cross-type decode tests and round-trip fixtures.

### TAR-B-P1-002 — Relational constraints and immutable provenance are underspecified

- Recommendation: normalized identity/revision/reference tables with explicit foreign keys and uniqueness constraints; JSON only for bounded extension/payload fields with schema version. Define provenance edge direction, cycle policy, merge/split history, exact source revision pinning and deletion/Forget behavior.
- Closure: migration and referential-integrity tests, cycle/property tests, merge/split replay fixtures.

### TAR-B-P1-003 — Serialization compatibility is not selected

- Recommendation: keep JSON as a debug/reference encoding candidate; evaluate CBOR/MessagePack only after canonical type schema stabilizes. Preserve unknown-field/version behavior and reject malformed authority-bearing fields. Serde does not itself define compatibility policy.
- Closure: golden vectors, forward/backward decode matrix, unknown-field policy and schema migration tests.

## 4. Technology disposition

| Technology/approach | Disposition | Conditions |
|---|---|---|
| Rust domain crate + newtypes | RECOMMEND | Keep owner semantics in types and validation. |
| Serde | ACCEPT AS CANDIDATE | Add explicit schema/version policy; no implicit semantic defaults. |
| Relational normalized core | RECOMMEND | Preserve identity, revisions, uniqueness, foreign keys and temporal semantics. |
| JSON extension fields | ACCEPT AS CANDIDATE | Not a substitute for typed authority-bearing columns. |
| JSON wire encoding | DEFER | H owns normative BMCP encoding. |
| CBOR / MessagePack | DEFER | Compare size, canonicalization, tooling and compatibility after schema stabilizes. |
| SQLite / PostgreSQL | NEEDS CROSS-OWNER ADR/PROTOTYPE | B requires integrity and migration evidence; D/Storage owns transaction selection. |
| Separate Fact object vs Claim qualification | NEEDS ADR | ADR-001 remains blocked; no implicit choice. |

## 5. Resource and failure/recovery assessment

No benchmark or sizing facts are available. Measure record/revision counts, median/p99 payload size, relation fan-out, provenance depth, write concurrency, migration time and index amplification. Estimate storage as canonical rows + immutable revision history + provenance edges + indexes + blob references; separately measure actual blob bytes and backup duplication.

| Failure | Required recovery behavior | Required test |
|---|---|---|
| Process crash during revision write | Transaction leaves old head or complete new revision; no partial graph | B-REC-01 crash injection |
| Duplicate source reference | Unique constraint/idempotency returns same semantic object | B-REC-02 |
| Schema upgrade interrupted | Migration is atomic/restartable; old version remains readable or rollback is proven | B-MIG-01 |
| Unknown enum/field | Explicit forward-compatibility policy; no unsafe authority default | B-SER-01 |
| Provenance cycle or dangling edge | Reject or quarantine according to declared graph policy | B-GRAPH-01 |
| Fact/Claim migration | No execution until ADR; dual-read/backfill plan must preserve exact history | B-ADR-01 |

## 6. Compatibility and required sequence

1. Governance resolves Fact/Claim ADR.
2. B publishes canonical typed-reference/schema constraints and a field-level consumer map.
3. D confirms canonical identity/revision and cursor mapping; E confirms candidate/proposal mapping; I confirms Principal/Scope authorization mapping.
4. H derives wire schema only after semantic types are stable.
5. Run serialization, property, migration, malformed-input and provenance graph suites.

## 7. Final recommendation and non-claims

Conditionally accept TAB-001's domain technology direction as a candidate. Do not freeze Fact/Claim representation, schema fields, serialization, or database choice. No schema migration, performance benchmark, fuzz test, production persistence, or independent Owner acceptance was executed by this review.