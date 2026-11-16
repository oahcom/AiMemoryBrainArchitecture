# B — Domain Model Technology Architecture Review

- Document: TAR-B-001
- Review date: 2026-11-17
- Owner boundary: B — Domain Model Architect
- Execution: centralized delegated static architecture review; not an independent human-owner attestation.
- Branch: `session-b-domain-model-phase3`
- **Reviewed branch HEAD:** `a5bf20b57ebb3db849f91c555b658f9a2ee09851`
- TAB-001 main HEAD: `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f`; blueprint blob: `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`
- TAR-AI-001 task blob: `5a813edeccf7190d66dfd71a96ca581c48f8a4cb`
- Roadmap main blob: `29289361973ec4369f067706132190793cd57a6b`
- B baseline blob: `410d6cc62294e1a7ee5efa0cfe4ef496a8179326`
- B core entities blob: `8cb5a674eec8eac1f3c4d83c400dc08d00166f23`
- B Fact/Claim consumer map blob: `dd45a37199c9b69ab6b68f65e051a484a04691d4`
- B typed-reference semantics blob: `e9a6bd21e06bc02a5208619f5a949217860b1c00`
- B formal Actor/Scope/Environment mapping blob: `3a1e77889cd9a90cd5822d9f0cb3437880868706`
- ADR-001 current blob: `df77e4a93cb8fef689ae7c828888d960cbf381d6`
- B COC type-boundary review blob: `e92ad97ac92469ece2bcd0f7ca6f822966f00232`
- Existing report blob replaced: `473c9bb1b8d010e9e20c16975864be7b2daa3253`

## Executive Summary

**Verdict: CONDITIONAL PASS.** TAB-001's Rust-first, typed-domain, transactional-relational direction is suitable for continued prototyping. It is not yet a lossless, freeze-ready implementation specification. The decisive blocker is still Fact/Claim canonical identity and semantics: ADR-001 remains explicitly ADR-BLOCKED. B's newer formal approval of ActorRef, ScopeRef and EnvironmentRef *semantic mapping* is a real owner decision, but it does not approve I's trust policy, H's wire encoding, database keys, or all consumer field paths.

The architecture should prefer normalized typed relational identity/revision/reference tables, immutable revision snapshots, explicit schema versions and bounded extension payloads. Serde is a viable Rust serialization framework, not a schema-evolution policy. JSON, CBOR and MessagePack remain encoding candidates. SQLite/PostgreSQL selection belongs with D/Storage and requires integrity/migration evidence. No technology is frozen by this review.

## Review Scope

Reviewed TAB-001 §2–§10 and the TAR-AI-001 requirements against B's current branch, especially core entities, typed references, ActorRef/ScopeRef/EnvironmentRef formal confirmation, Fact/Claim consumer mapping and both ADR-001 copies. Cross-checked the current main Phase 3 D/E/H/I review and roadmap. This is a static document review; no code, DDL, migration, benchmark, fuzz test or database was executed.

## Six-Dimension Review Conclusions

| Dimension | Verdict | Assessment |
|---|---|---|
| 1. Technical requirements & workload fit | CONDITIONAL | Domain model captures typed identity, immutable MemoryVersion, provenance, temporal/epistemic qualifiers and explicit Scope. Exact cardinalities, graph constraints, payload distributions and workload envelope still need field-level implementation mapping. |
| 2. Component dependencies & boundaries | CONDITIONAL | B owns semantic types; D owns canonical persistence/commit; E emits neutral proposals; I authorizes; H serializes wire contracts. This is a sound separation. Consumers must not mint B-owned canonical identities or treat typed refs as authorization. |
| 3. Candidate technology selection | CONDITIONAL | Rust newtypes + relational core + immutable revisions are recommended. Serde/JSON are candidates; CBOR/MessagePack are deferred. DB and wire encoding remain outside B's freeze authority. |
| 4. Resource constraints | NOT MEASURED | Need object/revision counts, relation fan-out, provenance depth, payload/blob distributions, index amplification, read/write concurrency and migration/backup windows. GPU/VRAM is not a B-domain dependency. |
| 5. Failure recovery & operational safety | CONDITIONAL | Immutable history and explicit refs support recovery, but migration atomicity, dangling references, graph cycles, entity merge/split replay, digest verification and Forget-aware historical reads need executable tests. |
| 6. Interface & compatibility | CONDITIONAL / ADR BLOCKED | ActorRef/ScopeRef/EnvironmentRef semantics have B formal approval; exact consumer schemas remain owner-bound. Fact/Claim identities, revisions, D persistence mapping and H wire fields remain blocked pending ADR-001. |

## Component Dependency Analysis

- **B → D:** B supplies typed semantic identities, invariants and revision meaning; D allocates canonical IDs, persists immutable versions, enforces references and commit ordering. B does not prescribe D's SQL schema or transaction implementation.
- **E → B/D:** E retains CandidateProposition/ExtractionIR with source digest, span, scope, modality and uncertainty. It submits proposals; it must not assign canonical Claim/Fact IDs.
- **I → B/H:** B's ActorRef is immutable, verifier-produced attribution; ScopeRef is ownership/applicability identity, not a grant. I owns trust, delegation, authorization and revocation. H owns authenticated transport binding and wire representation.
- **F/G:** consume stable typed references and exact immutable version refs; they cannot infer Fact/Claim identity before ADR approval.
- **Graph/storage boundary:** provenance and relation edges require explicit direction, endpoint type rules, cycle policy, exact revision pinning and scope validation. Do not store authority-bearing references as unvalidated strings in JSON blobs.

No logical component boundary implies a separate process, crate or database. A Rust domain crate with ports to D storage and H protocol adapters is a reasonable candidate.

## Candidate Technology Comparison

| Concern | Candidate A | Alternative | Trade-offs / recommendation |
|---|---|---|---|
| Domain types | Rust newtypes/enums | Plain strings/UUIDs | Newtypes prevent accidental cross-type substitution at compile time; more conversion boilerplate. Recommend newtypes for every authority-bearing ref/cursor/epoch. |
| Canonical persistence | Normalized SQL tables + FK/unique constraints | Document-only JSON store | SQL enforces identity, uniqueness and referential integrity; JSON-only is flexible but weakens typed joins, constraints and migration safety. Recommend relational core with bounded JSON extension fields. |
| Serialization | Serde + versioned JSON | CBOR / MessagePack | JSON is inspectable and easy to debug; larger payloads and canonical digest ambiguity need care. CBOR/MessagePack can reduce size but complicate canonicalization/tooling. Keep all as candidates until schema stabilizes and golden-vector tests compare them. |
| Schema evolution | Explicit schema_version + ordered migrations | Implicit serde defaults / ad hoc field additions | Explicit migrations are auditable and testable; more operational work. Reject silent defaults for security/domain-critical fields. |
| Provenance graph | Relational edge tables + typed refs | Embedded graph DB | Relational tables fit local deployment and transactional edge writes; graph DB adds operations and cross-store atomicity. Start relational unless traversal benchmarks prove otherwise. |
| IDs | Opaque UUIDv7 candidate | Content-derived IDs | UUIDv7 aids locality but leaks ordering; content hashes conflate identity with content and break revision identity. Keep algorithm OPEN; IDs must remain opaque and non-semantic. |
| Database engine | SQLite WAL / PostgreSQL | Embedded KV (RocksDB) | B requires FK/unique constraints and migration safety. SQLite minimizes local ops but single-writer; PostgreSQL handles concurrent writers and mature tooling but adds service/admin cost; KV shifts constraints/transactions into app code. D/Storage must decide after equivalent conformance tests. |

## Resource Budget Analysis

No measured figures are available. Size from:
- canonical storage = identities + immutable revisions + typed relation/provenance edges + indexes + idempotency/audit metadata;
- blob storage = sum of retained source payload bytes plus replication/backup generations;
- graph working memory = active traversal frontier × edge fan-out × visited-set overhead;
- migration budget = full-table rewrite/read amplification + index rebuild + backup overlap.

Benchmark at representative small/medium/large corpus sizes and high fan-out/deep provenance fixtures. Measure p50/p95/p99 typed-reference lookup, graph expansion, commit contention, migration duration, disk amplification and restore time. Do not derive capacities from the 12–16 GB VRAM envelope; B does not require inference in its correctness path.

## Failure & Recovery Matrix

| Failure | Required safe behavior | Required evidence |
|---|---|---|
| Crash during MemoryVersion commit | Old head or complete new revision only; cursor/head never partially advance | Transaction crash injection |
| Duplicate reference / idempotent retry | Same identity+digest returns same object; changed digest conflicts | Unique-key/property tests |
| Dangling or cross-authority ref | Reject/quarantine; no string fallback | Typed decode and FK tests |
| Provenance cycle / invalid endpoint | Reject or explicit quarantined state under declared graph policy | Graph property/fuzz tests |
| Interrupted schema migration | Atomic/restartable migration; restore/rollback path proven | Migration fault injection on copied DB |
| Unknown enum/schema field | Explicit compatibility behavior; no permissive authority default | Golden forward/backward decode matrix |
| Entity merge/split replay | Preserve historical refs and deterministic redirects; no silent rewrite | Replay fixtures |
| Forget against historical payload | Ref may remain auditable while payload dereference is suppressed under I policy | Forget-aware read tests |

## Interface Compatibility Findings

1. ADR-001 remains **ADR-BLOCKED** in the current B branch copy `02-domain-model/adr/ADR-001-fact-claim-canonical-model.md` (blob `df77e4a93cb8fef689ae7c828888d960cbf381d6`). A second legacy copy `02-domain-model/ADR-001-fact-claim-semantics.md` (blob `a1024938ff5baba069cf128c69496a44e143330c`) also exists; duplicate-document drift should be resolved by B/Governance, not by this review.
2. B has formally approved semantic mapping for ActorRef, ScopeRef and EnvironmentRef (blob `3a1e77889cd9a90cd5822d9f0cb3437880868706`). H wire names/serialization and I authorization policy are not thereby approved.
3. Keep BrainAuthority namespace explicit. MemoryRef is identity-only; MemoryVersionRef is exact immutable content. ClaimRef/ClaimRevisionRef remain conditional on ADR-001.
4. Do not coerce CanonicalCommitCursor, AggregateRevision, LifecycleEventCursor, ForgetFenceGeneration, PermissionEpoch, ProducerDomainInventoryEpoch, IndexWatermark, ContextVersion, AdapterCapabilityEpoch or COC positions.
5. Typed reference existence does not grant permission to dereference; I authorization is separate.

## Blocking Findings

- **P0 — TAR-B-P0-001:** Fact/Claim identity and canonical model unresolved (ADR-001). Blocks canonical schema/DDL/API/wire freeze.
- **P1 — TAR-B-P1-001:** Exact consumer field paths and schema compatibility policy need a versioned field-level registry and cross-owner fixtures.
- **P1 — TAR-B-P1-002:** Relational constraints, provenance graph cycle policy, merge/split lineage and exact source revision pinning are incomplete.
- **P1 — TAR-B-P1-003:** Serialization encoding/canonical digest/version compatibility not selected or tested.
- **P2 — TAR-B-P2-001:** Duplicate ADR file paths can drift; designate one canonical ADR path and supersede/archive the other through B/Governance.

## Required ADRs

1. Resolve ADR-001 Fact/Claim identity and governance terminology conflict.
2. Schema evolution and compatibility ADR: version policy, unknown-field/enum handling, canonicalization/digest rules, migration and rollback.
3. Domain ID strategy ADR only if UUIDv7 vs alternative affects privacy, ordering, portability or storage layout.
4. Database ADR belongs to D/Storage; B provides integrity/migration requirements but does not choose the engine.
5. Wire encoding ADR belongs to H after semantic schema and typed refs are approved.

## Required Prototypes and Tests

- Rust newtype compile-fail tests for cross-ref/cursor substitution.
- Serde round-trip and malformed/unknown field tests for all domain types.
- JSON vs CBOR vs MessagePack size/canonical digest/compatibility golden vectors.
- SQL schema prototype with FK/unique/check constraints and immutable revision enforcement.
- Provenance graph cycle, endpoint typing, fan-out and merge/split property tests.
- Forward/backward schema migration, interrupted migration, backup/restore and Forget-aware dereference tests.
- No prototype/test listed above is claimed executed.

## Verdict

**CONDITIONAL PASS** — domain technology direction is plausible for a local-first Rust implementation, but Fact/Claim canonical identity and schema freeze remain blocked. B's ActorRef/ScopeRef/EnvironmentRef semantic approval is acknowledged within its precise authority boundary only.

## Evidence and Exact SHAs

All source references below are the exact files inspected; commit SHA is the reviewed owner-branch HEAD unless marked main.

| Source | Commit SHA | Blob SHA |
|---|---|---|
| TAB-001 main | `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f` | `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` |
| TAR-AI-001 tasks main | `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f` | `5a813edeccf7190d66dfd71a96ca581c48f8a4cb` |
| Roadmap main | `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f` | `29289361973ec4369f067706132190793cd57a6b` |
| B core entities | `a5bf20b57ebb3db849f91c555b658f9a2ee09851` | `8cb5a674eec8eac1f3c4d83c400dc08d00166f23` |
| B typed-reference semantics | `a5bf20b57ebb3db849f91c555b658f9a2ee09851` | `e9a6bd21e06bc02a5208619f5a949217860b1c00` |
| B formal Actor/Scope/Environment mapping | `a5bf20b57ebb3db849f91c555b658f9a2ee09851` | `3a1e77889cd9a90cd5822d9f0cb3437880868706` |
| B Fact/Claim consumer map | `a5bf20b57ebb3db849f91c555b658f9a2ee09851` | `dd45a37199c9b69ab6b68f65e051a484a04691d4` |
| B ADR-001 canonical path | `a5bf20b57ebb3db849f91c555b658f9a2ee09851` | `df77e4a93cb8fef689ae7c828888d960cbf381d6` |
| B COC type review | `a5bf20b57ebb3db849f91c555b658f9a2ee09851` | `e92ad97ac92469ece2bcd0f7ca6f822966f00232` |

This report is a design review only. It does not approve TAB-001, select a database/encoding, or claim implementation/test evidence.
