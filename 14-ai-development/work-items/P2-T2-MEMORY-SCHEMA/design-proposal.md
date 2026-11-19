# P2-T2 — Memory Storage Schema Design Proposal

**Work item:** P2-T2 (Phase 2 Task 2)  
**Status:** DESIGN PROPOSAL — not implemented, not frozen  
**Date:** 2026-11-19  
**Scope authority:** `GO-2026-P2-DESIGN-001` — design proposal only; P2-T1 implementation authorization remains withheld.  
**Review basis:** R1 at PR head `9b5446b9b63ff80f6594d0316b6083e986d84769`; this revision addresses R1-B-01 and R1-NB-02 through R1-NB-05. It does not claim R1 approval.

---

## 1. Purpose and boundaries

This proposal describes a Phase 2 persistence design around the Phase 1 SQLite boundary. It separates three responsibilities:

1. **Canonical Memory** — immutable Memory versions and their current pointer.
2. **Transcript capture** — retained source conversations and message-level retrieval metadata. A transcript record is evidence of what was communicated; it is not automatically a canonical Memory or Claim.
3. **Derived intelligence** — value/decay results, vector bindings and context assemblies. These are non-canonical projections or working state.

This is a design proposal, not an adopted architecture decision. In particular:

- Q1 (the authority decision between the original Option A / B and the proposed three-layer alternative) remains OPEN.
- No schema is frozen; no implementation, migration or test execution is authorized.
- No vector provider or embedding model is selected.
- The exact prompt schema source was not retrievable at the R1 target. Statements about its DDL are therefore not treated as verified facts in this revision; see §10.

## 2. Existing Phase 1 boundary

The repository evidence at base `7f8093876729212ef4e83461ba8c2f2cd96582c7` supports the following bounded statements:

| Source | Status and boundary |
|---|---|
| `02-domain-model/core-entities.md` | DECIDED domain semantics; MemoryVersion is immutable; Events retain source/payload/scope/retention metadata; transcript capture is not equated with canonical Memory |
| `02-domain-model/phase-1-sqlite-adapter-contract.md` | DECIDED for the tested local file-backed SQLite profile and stated transaction/CAS/idempotency behaviors only; not a production-readiness or distributed-systems claim |
| `02-domain-model/phase-1-storage-trait-contract.md` | CANDIDATE backend-neutral interface seam; no backend is selected by this document |
| `crates/memory-storage-sqlite` | Implements the Phase 1 MemoryStorage SQLite adapter |
| `crates/memory-event-store-sqlite/src/payload.rs` | Implements payload custody extension with byte retention, SHA-256 digest checking, ordered `read_after`, and scope filtering; it is not a transcript query API |

The Phase 1 SQLite decision is not generalized to production topology, multi-host linearizability, power-loss recovery or other untested guarantees.

## 3. Proposed three-layer model (PROPOSED; Q1 remains OPEN)

The R1 reviewer proposed a three-layer alternative. This revision adopts it as the design direction for further review, **not as a binding Owner decision**.

### 3.1 Canonical Memory

- Keep Phase 1 `memories`, `versions`, `idempotency` and `commit_log` as the canonical Memory persistence boundary.
- A transcript message is not promoted to canonical Memory merely because it is captured.
- A derived Memory or Claim must retain typed, traceable source references to the transcript/Event/evidence from which it was derived.
- MemoryVersion remains immutable; a projection update must not mutate its content or digest.

### 3.2 Transcript capture

Transcript capture is a separate responsibility, with a message-oriented logical model. It must support, at minimum:

- stable session/capture identity and explicit retention scope;
- stable message identity and deterministic message ordering within a session;
- speaker/actor role and source identity;
- message payload bytes or a durable payload reference, with integrity digest;
- tool-call and tool-result relationships, including correlation/parent references;
- edit/revision or deletion/tombstone status where the source protocol exposes it;
- source time and durable capture time, with unknown values represented explicitly;
- scope checks before disclosure and a retention/Forget policy independent of canonical Memory.

The existing Event Store can preserve payload bytes and return ordered Events by sequence. That alone does **not** provide transcript reconstruction, session navigation, speaker filtering or tool-call relationship queries. A transcript adapter/projection must define those semantics explicitly. It may use accepted Events as ingress and preserve the original payload, but it must not claim that generic Event retrieval is already a complete transcript API.

**Deletion boundary:** closing or deleting a transcript session may affect only transcript-owned capture records under the applicable retention policy. It must not cascade into canonical Memory or MemoryVersion. Any derived canonical Memory has its own lifecycle, retention and Forget operation.

### 3.3 Derived intelligence

Value scoring, decay, vector bindings and context assembly are derived/working data, not a second canonical content root.

- Projection rows identify the exact MemoryVersion they describe.
- Projection invalidation or rebuild must not delete canonical Memory.
- External vector objects are non-canonical; SQLite binding metadata must support stale/failed state and invalidation.
- Context entries bind both a Memory and a version, and must prove that the version belongs to that Memory.

## 4. Value/decay projection and rebuild contract

The previous draft claimed that a projection could be deterministically rebuilt from `commit_log` alone. R1 correctly found that unsupported: the commit log identifies committed versions and sequence, but does not itself contain the scoring algorithm, scoring inputs, decay parameters, evaluation clock or all relevant events/configuration.

This proposal therefore **withdraws the same-value deterministic rebuild guarantee**. It distinguishes two different properties:

1. **Structural rebuild (proposed minimum):** projection rows can be deleted and reconstructed as structurally valid records from the declared canonical source set, without changing canonical Memory. This does not promise the same historical numeric score.
2. **Reproducible numeric recomputation (not specified / NOT CLAIMED):** would require immutable, retained scoring inputs; versioned scoring method and parameters; relevant event/citation history; explicit evaluation time; and a deterministic algorithm/runtime contract. These inputs and semantics are not established by the current Phase 1 commit log.

A future design may specify the second property only after it defines and retains that complete source set. A digest identifies data; it is not a substitute for retaining the data. Until then, scores are derived observations with method/input references and timestamps, not guaranteed replay-equivalent values.

## 5. Logical data mapping

| Responsibility | Logical record / current home | Authority |
|---|---|---|
| Canonical Memory | Phase 1 `memories` | canonical |
| Immutable content/version | Phase 1 `versions` | canonical and immutable |
| Canonical commit ordering/idempotency | Phase 1 `commit_log` / `idempotency` | canonical Phase 1 transaction evidence |
| Captured source occurrence | Event Store `accepted_events` + `event_payloads` | captured source; not automatically a transcript API |
| Transcript session/message view | proposed transcript capture adapter/projection over captured source records | transcript responsibility; design still requires detailed schema |
| Value/decay | proposed version-keyed projection | derived; non-canonical |
| Value history | proposed append-only computation history | derived audit/history; semantics still open |
| Vector binding | proposed version-keyed binding to external vector object | derived; non-canonical |
| Context assembly | proposed context and entry records | mutable working state; non-canonical |

Claim/Entity/Relation extraction from `version_json` into query projections remains deferred. Any such projection must preserve the immutable version as its source of truth and define invalidation/rebuild behavior.

## 6. Integrity and consistency requirements

### 6.1 Memory-to-Version relationship

A context entry's separate `memory_id` and `version_id` references are not sufficient merely because each row exists. The write path MUST enforce that the selected version belongs to the selected memory.

Acceptable implementation choices for a later authorized implementation include:

- a composite foreign-key design backed by a corresponding unique key on the version relation; or
- equivalent transactional validation that reads the version's owning `memory_id` and rejects a mismatch in the same transaction that inserts the context entry.

The implementation must include a negative test: an existing version belonging to Memory A cannot be inserted into a context entry naming Memory B. A successful independent existence check for each ID is not enough.

### 6.2 Scope and lifecycle

- Scope authorization/filtering occurs before returning transcript or Memory data.
- Transcript retention and canonical Memory retention are separate policies.
- Session closure does not imply canonical Memory deletion.
- Forget behavior must follow the canonical Memory lifecycle/authorization contract; this proposal does not invent or authorize a new Forget mechanism.
- Projection invalidation must never delete canonical Memory or MemoryVersion.

### 6.3 Event payload limits

The current payload extension demonstrates byte custody, digest validation and ordered event retrieval under its implemented contract. It does not, by itself, establish message-level role semantics, session-oriented navigation, transcript reconstruction or tool-call graph semantics. Those are explicit requirements for the transcript layer, not capabilities claimed as already implemented.

## 7. Interfaces (conceptual; not implementation authorization)

The eventual design may expose separate ports for:

- `TranscriptCapture`: append/capture source messages, read a session transcript in stable order, resolve speaker/tool-call relationships, and apply transcript retention/scope rules.
- `MemoryValueProjection`: read and update version-keyed derived values; expose method/input/evaluation metadata; do not promise reproducible numeric recomputation until §4's source requirements are met.
- `VectorIndex`: bind/search/invalidate version references; scope-filter before disclosure; never own canonical Memory.
- `ContextAssembly`: assemble and read working context while validating Memory-to-Version ownership.

These are conceptual boundaries only. Method signatures, error types, storage DDL and backend selection remain OPEN for a later authorized design iteration.

## 8. Migration and test boundaries

No migration is proposed for execution in this PR. Any future implementation design must be additive to Phase 1 unless a separately authorized supersession decision says otherwise.

Before implementation authorization, the design must specify tests for:

1. transcript session/message ordering and stable pagination;
2. speaker identity, tool-call/tool-result correlation and source payload integrity;
3. scope isolation before transcript disclosure;
4. transcript retention/deletion not cascading into canonical Memory;
5. derived projection invalidation leaving canonical versions unchanged;
6. Memory-to-Version mismatch rejection for context entries;
7. structural projection rebuild, with no claim of historical numeric equivalence;
8. if numeric reproducibility is later claimed: complete immutable source inputs, method/version, parameters and evaluation-time replay tests;
9. migration idempotency and rollback/recovery boundaries.

No tests are claimed as run by this proposal.

## 9. Open questions and decision status

| ID | Question | Status |
|---|---|---|
| Q1 | Adopt the three-layer model, retain the original Option A, or explicitly supersede Phase 1 (original Option B)? | **OPEN — accountable decision required** |
| Q2 | Transcript capture physical schema and relationship to accepted Events | OPEN |
| Q3 | Claim/Entity/Relation query projections | OPEN; defer to P2-T3 |
| Q4 | Vector provider | OPEN; no selection |
| Q5 | Embedding model/dimension | OPEN; no selection |
| Q6 | Numeric scoring inputs, method/version, parameters and evaluation clock | OPEN |
| Q7 | Whether numeric reproducibility will be a requirement or whether structural rebuild is sufficient | OPEN |
| Q8 | Transcript retention/Forget policy details and authority | OPEN |
| Q9 | Exact Memory-to-Version integrity implementation (composite FK or transactional validation) | OPEN |

No option is silently selected. The reviewer’s third-layer proposal is recorded as PROPOSED only; Q1 remains unresolved until the accountable authority records a decision.

## 10. Evidence and source limitations

- `02-domain-model/core-entities.md`: read at base `7f8093876729212ef4e83461ba8c2f2cd96582c7`, Blob `8cb5a674eec8eac1f3c4d83c400dc08d00166f23`.
- `02-domain-model/phase-1-sqlite-adapter-contract.md`: read at the same base, Blob `c472e00f2ef4d00bb71806efc7db72062f4efb58`.
- `02-domain-model/phase-1-storage-trait-contract.md`: read at the same base, Blob `22ca7cd3777e0132e25f084084610f1e90b60d21`; its status is CANDIDATE.
- `crates/memory-event-store-sqlite/src/payload.rs`: read at the same base, Blob `ad22972ba621d5f780467f1bb8712cb962174315`.
- R1 review record: PR #307 comment `7023231264`, reviewed Head `9b5446b9b63ff80f6594d0316b6083e986d84769`.
- `prompts-fix/P2-T2-memory-schema.md`: fetch at the reviewed PR Head returned GitHub 404. Exact source contents are **NOT AVAILABLE / NOT VERIFIED** in this review context. Therefore the earlier draft's detailed description of that prompt, its DDL and its four alleged contradictions is withdrawn as verified evidence. Restore the exact source at a known commit or attach its exact contents before making source-comparison claims.
- The prior proposal's statements “Nothing requested is lost” and “satisfies every capability” are withdrawn as overclaims.

## 11. Non-claims

- Not implemented; no code, schema execution, migration or tests performed.
- Not frozen or accepted.
- Q1 remains OPEN.
- No P2-T1 implementation authorization is granted or implied.
- No vector store or embedding model is selected.
- No human Owner approval, acceptance authority assignment or merge authorization is represented.
