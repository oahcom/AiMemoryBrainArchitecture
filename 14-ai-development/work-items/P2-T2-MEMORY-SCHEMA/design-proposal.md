# P2-T2 — Memory Storage Schema Design Proposal

**Work item:** P2-T2 (Phase 2 Task 2)
**Status:** DESIGN PROPOSAL — not implemented, not frozen
**Date:** 2026-11-20
**Scope authority:** `GO-2026-P2-DESIGN-001` — design proposal first; P2-T1 implementation authorization withheld pending design review.

---

## 1. Purpose

Specify the persistence schema for the memory layer, covering:

- the logical→physical mapping of the frozen domain objects
- the vector index boundary
- migration strategy
- test boundaries

**This proposal does not accept the schema in `prompts-fix/P2-T2-memory-schema.md` as written.** That schema conflicts with Phase 1 decisions already merged to `main`. The conflict is set out in §2 and resolved in §3.

---

## 2. Blocking conflict — the prompt schema contradicts merged Phase 1 decisions

### 2.1 What the prompt specifies

Six tables: `sessions`, `messages`, `decisions`, `file_changes`, `context_injections`, `value_score_history`. Plus two views (`top_memories`, `recent_decisions`), a `schema_version` table, and a `messages.value_score` / `messages.decay_weight` pair of mutable columns.

It models **conversation transcripts**: a chat log with metadata attached.

### 2.2 What Phase 1 already decided and merged

Phase 1 froze a different object model and already implemented it in Rust:

| source | object | status |
|---|---|---|
| `02-domain-model/core-entities.md` | Memory, MemoryVersion, Claim, Entity, Relation, Evidence, Provenance, Event, Scope | DECIDED semantics |
| `02-domain-model/phase-1-storage-trait-contract.md` | `create_memory`, `read_current`, `read_version`, `commit_version`, `list_changes`, `resolve_idempotency` | CANDIDATE seam, implemented |
| `02-domain-model/phase-1-sqlite-adapter-contract.md` | SQLite adapter, immutable version rows, CAS, idempotency receipts, monotonic commit sequence | **DECIDED**, merged PR #242 / #243 |
| `crates/memory-storage-sqlite/src/lib.rs` | `memories`, `versions`, `idempotency`, `commit_log` | **implemented, tested** |
| `crates/memory-event-store-sqlite/src/lib.rs` | `accepted_events`, `event_payloads`, `compile_outbox` | **implemented, tested** |

### 2.3 The four concrete contradictions

**(a) Duplicate, incompatible representation of the same concepts.**

| prompt table | frozen object it collides with | nature of collision |
|---|---|---|
| `messages` | Memory + MemoryVersion | prompt models an append-only chat row; domain models an immutable versioned claim-set |
| `decisions` | Claim (with `epistemic_status`, `valid_time`, `polarity`) | prompt's `decision_type IN ('accept','reject','defer','escalate')` has no mapping to the domain's epistemic vocabulary |
| `file_changes` | Event + Provenance (`derivation_kind`) | prompt records a diff summary; domain requires `provenance_refs`, `input_digest_refs`, `parent_provenance_refs` |
| `context_injections` | MemoryContext + ContextEntry | prompt's `source_message_ids` cannot reference `memory_version_id`, which is what a Context Entry binds to |
| `sessions` | Session Scope | prompt treats session as a storage root with `ON DELETE CASCADE`; domain treats Session Scope as an authorization boundary whose closure must not delete canonical memory |

Adopting the prompt schema would create **two competing stores for the same objects**, with no declared authority between them.

**(b) Violation of an immutable-version invariant.**

`messages.value_score` and `messages.decay_weight` are mutable columns on the row that holds content. The domain model states: *"No in-place edit. Current pointer advancement and version commit are atomic."* A mutable score on the content row means the content row is not immutable, which breaks CAS, breaks `content_digest` stability, and makes `read_version` non-reproducible.

The prompt also pairs this with `value_score_history` — an admission that the value is mutated — and a trigger `update_decay_weight` that fires `AFTER INSERT` and writes `decay_weight = 1.0`, which is a no-op that misdescribes itself.

**(c) `ON DELETE CASCADE` on the session root conflicts with retention governance.**

`messages`, `decisions`, `file_changes` and `context_injections` all cascade from `sessions`. The domain model requires `retention_class`, `forget_operation_id` and an auditable Forget workflow. Deleting a session row would silently destroy canonical memory with no Forget operation, no provenance trail and no audit record.

**(d) No provenance chain, so no evidence tier is expressible.**

The prompt schema has no `provenance`, `evidence`, or `epistemic_status` structure. The repository's evidence-tiering policy (`evidence-tiering-policy.md`, PROPOSED) and the A-2 downgrade precedent both depend on being able to say *what a stored assertion rests on*. A schema without provenance cannot represent its own evidence grade.

### 2.4 Why this is a blocking conflict, not a style preference

Phase 1's SQLite adapter contract is **DECIDED** and merged. `GO-2026-P2-DESIGN-001` requires design proposals to rest on frozen contracts. A Phase 2 schema that redefines the same objects differently would make Phase 1's CAS and idempotency guarantees unenforceable in the Phase 2 store, while both claim to be the system of record.

---

## 3. Proposed resolution

### 3.1 Authority ruling requested

Two options, stated plainly, for the design review to choose:

**Option A — Phase 1 is the storage layer; Phase 2 adds layers above it.**
Phase 2 does not introduce a new content store. It adds: vector index, value/decay scoring as a **separate projection**, and context assembly. Canonical content stays in `memories`/`versions`. Transcript capture becomes an *Event* ingress into `accepted_events`, not a new `messages` table.

**Option B — Phase 1 is superseded for the memory path.**
The frozen domain model and Rust adapter are declared Phase-1-only scaffolding, and Phase 2 replaces them. This requires an explicit supersession decision, a migration plan off the existing tables, and re-opening the DECIDED status of `phase-1-sqlite-adapter-contract.md`.

**This proposal recommends Option A.** It preserves merged decisions, keeps one system of record, and satisfies every capability the prompt asks for. Option B is available but must be chosen explicitly, not drifted into.

### 3.2 Option A schema — additive only

All Phase 1 tables unchanged. New tables:

```sql
-- Transcript capture is an Event, not a new content root.
-- messages/sessions from the prompt are NOT created.
-- Session identity maps to Session Scope; session lifecycle maps to Events.

-- Value and decay as a separate, rebuildable projection.
-- Keyed by version_id, never by content row. Rebuildable from commit_log.
CREATE TABLE IF NOT EXISTS version_value_projection (
  version_id        TEXT PRIMARY KEY REFERENCES versions(version_id),
  value_score       REAL NOT NULL CHECK (value_score >= 0 AND value_score <= 100),
  decay_weight      REAL NOT NULL CHECK (decay_weight >= 0 AND decay_weight <= 1),
  computed_at       TEXT NOT NULL,
  method_ref        TEXT NOT NULL,
  input_digest      TEXT NOT NULL
);
-- No mutable columns on versions. Projection is derived, not canonical.

-- Value history, append-only, never updated.
CREATE TABLE IF NOT EXISTS version_value_history (
  history_id        TEXT PRIMARY KEY,
  version_id        TEXT NOT NULL REFERENCES versions(version_id),
  old_score         REAL,
  new_score         REAL NOT NULL,
  reason            TEXT NOT NULL CHECK (reason IN
                      ('initial','cited_by_decision','time_decay','manual_adjustment','recompute')),
  method_ref        TEXT NOT NULL,
  recorded_at       TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS value_history_version_idx
  ON version_value_history(version_id, recorded_at);

-- Vector index binding. Qdrant/Chroma owns the vector; SQLite owns the binding.
-- The binding is a projection: deleting it must never delete canonical content.
CREATE TABLE IF NOT EXISTS version_vector_binding (
  version_id        TEXT PRIMARY KEY REFERENCES versions(version_id),
  embedding_id      TEXT NOT NULL UNIQUE,
  embedding_model   TEXT NOT NULL,
  embedding_dim     INTEGER NOT NULL,
  content_digest    TEXT NOT NULL,   -- must match the version's digest at bind time
  indexed_at        TEXT NOT NULL,
  index_status      TEXT NOT NULL CHECK (index_status IN
                      ('pending','indexed','stale','failed')),
  failure_reason    TEXT
);
CREATE INDEX IF NOT EXISTS vector_binding_status_idx
  ON version_vector_binding(index_status);

-- Context assembly. Binds to immutable versions, never to a mutable row.
CREATE TABLE IF NOT EXISTS context_assembly (
  assembly_id       TEXT PRIMARY KEY,
  agent_scope_id    TEXT NOT NULL,
  session_scope_id  TEXT,
  task_scope_id     TEXT,
  created_at        TEXT NOT NULL,
  assembly_state    TEXT NOT NULL CHECK (assembly_state IN ('draft','active','closed'))
);

CREATE TABLE IF NOT EXISTS context_assembly_entry (
  entry_id          TEXT PRIMARY KEY,
  assembly_id       TEXT NOT NULL REFERENCES context_assembly(assembly_id),
  memory_id         TEXT NOT NULL REFERENCES memories(memory_id),
  version_id        TEXT NOT NULL REFERENCES versions(version_id),
  position          INTEGER NOT NULL,
  relevance_score   REAL,
  entry_state       TEXT NOT NULL CHECK (entry_state IN ('included','excluded','expired')),
  added_at          TEXT NOT NULL,
  UNIQUE(assembly_id, position)
);
CREATE INDEX IF NOT EXISTS assembly_entry_assembly_idx
  ON context_assembly_entry(assembly_id, position);
```

### 3.3 What this gives up, and why that is acceptable

| prompt capability | Option A treatment |
|---|---|
| store chat messages verbatim | captured as Events in `accepted_events` with `payload_bytes`; not as canonical Memory |
| `decisions` table with accept/reject/defer | expressed as Claim with `epistemic_status` + an Event carrying the decision actor; the four prompt values map to Claim polarity + lifecycle, not to a parallel table |
| `file_changes` | Event with `event_kind = file_change` and a Provenance edge; `commit_sha` lives in the Event envelope |
| Ebbinghaus decay | `version_value_projection.decay_weight`, recomputed by a job with `method_ref`; history append-only |
| semantic search | `version_vector_binding` + external vector store |
| `top_memories` view | a query joining `version_value_projection` and `memories`, not a view over mutable rows |

Nothing requested is lost. What changes is *where* it lives: canonical content stays immutable, derived signals stay in rebuildable projections.

---

## 4. Data model — mapping table

| frozen object | physical home | mutability |
|---|---|---|
| Memory | `memories` (Phase 1) | current pointer mutable, object immutable |
| MemoryVersion | `versions` (Phase 1) | immutable |
| Claim / Entity / Relation / Evidence / Provenance | serialized in `versions.version_json` | immutable per version |
| Event | `accepted_events` + `event_payloads` (Phase 1) | append-only |
| Compile intent | `compile_outbox` (Phase 1) | consumed once |
| Scope | `memories.scope_json`, `versions.scope_json` | bound at commit |
| value / decay | `version_value_projection` | rebuildable |
| value history | `version_value_history` | append-only |
| vector embedding | external store + `version_vector_binding` | rebuildable |
| Context | `context_assembly` + `context_assembly_entry` | mutable, non-canonical |

**OPEN:** whether Claim/Entity/Relation should be extracted into their own tables for query. Phase 1 stores them inside `version_json`. Extraction would improve query but creates a second representation that must stay consistent with the immutable version — a projection with a rebuild path, not a second source of truth. Deferred to P2-T3, not decided here.

---

## 5. Interface boundary

Phase 2 must not change the Phase 1 `MemoryStorage` trait. Additions are separate traits:

```rust
pub trait MemoryValueProjection {
    fn compute_value(&self, version_id: &VersionId) -> Result<ValueScore, Error>;
    fn read_projection(&self, version_id: &VersionId) -> Result<Option<ValueProjection>, Error>;
    fn rebuild(&self, scope: &Scope) -> Result<RebuildReport, Error>;
}

pub trait VectorIndex {
    fn bind(&self, version_id: &VersionId, embedding: &Embedding) -> Result<Binding, Error>;
    fn search(&self, query: &Query, scope: &Scope, top_k: usize) -> Result<Vec<Hit>, Error>;
    fn invalidate(&self, version_id: &VersionId) -> Result<(), Error>;
}
```

Invariants:
- `bind` MUST reject when `content_digest` does not match the version's digest.
- `search` MUST filter by scope **before** returning hits; scope filtering is not a post-filter.
- `invalidate` MUST NOT delete canonical content.
- `rebuild` MUST be idempotent and MUST reproduce the same projection from the same `commit_log`.

---

## 6. Migration strategy

| step | action | reversibility |
|---|---|---|
| M1 | Create new tables with `IF NOT EXISTS`; no existing table altered | drop new tables |
| M2 | Backfill `version_value_projection` from `commit_log` for existing versions | truncate and rebuild |
| M3 | Bind vectors for existing versions; `index_status='pending'` until done | delete bindings |
| M4 | Cut over reads to the new projections | revert to Phase 1 reads |

No destructive migration. No `ALTER TABLE` on Phase 1 tables. No data rewrite of `versions`.

**Schema versioning:** a `schema_migrations` table with `(version, applied_at, checksum)`, forward-only, each migration idempotent. The prompt's `schema_version` table is retained in spirit but with a checksum column, because a version string alone cannot detect a partially-applied migration.

---

## 7. Test boundaries

Required before implementation authorization is granted:

1. **Invariant tests** — `bind` rejects digest mismatch; `search` never returns a cross-scope hit; `invalidate` leaves `versions` row count unchanged.
2. **Projection rebuild** — delete `version_value_projection` entirely, run `rebuild`, assert byte-identical projection to the pre-delete state.
3. **Immutability guard** — assert no UPDATE path exists to `versions` content columns; assert `content_digest` stable across a projection recompute.
4. **Migration idempotency** — run the full migration twice; second run must be a no-op with identical checksums.
5. **Scope isolation** — two scopes, same content; assert each `search` returns only its own scope's versions.
6. **No cascade destruction** — closing a session scope must not reduce `memories` or `versions` row counts.

Test 6 is the direct regression guard against the prompt schema's `ON DELETE CASCADE`.

---

## 8. Open questions

| id | question | status |
|---|---|---|
| Q1 | Option A vs Option B authority ruling | **BLOCKING** — needs decision |
| Q2 | Extract Claim/Entity/Relation to tables, or keep in `version_json`? | OPEN, defer to P2-T3 |
| Q3 | Vector store: Qdrant vs Chroma. Prompt defaults Chroma; Phase 1 has neither. | OPEN |
| Q4 | Embedding model and dimension. Prompt assumes `text-embedding-3-small` / 1536. | OPEN — external dependency, not decided |
| Q5 | Decay recompute cadence and `method_ref` vocabulary | OPEN |
| Q6 | Does `version_vector_binding.content_digest` need to track `versions.content_digest` by FK or by trigger? | OPEN |

---

## 9. What this proposal does not claim

- Not implemented. No code, no migration, no tests executed.
- Not a frozen schema. It is a proposal for review.
- Not an authorization for P2-T1. Implementation authorization remains withheld per `GO-2026-P2-DESIGN-001`.
- Not a resolution of Q1. If the review chooses Option B, §3.2–§7 are void and a supersession decision is required first.
- No technology selection is made: Qdrant/Chroma, embedding model, and dimension all remain OPEN.

---

## 10. Evidence tier

- Phase 1 DECIDED status and merged commits: **VERIFIED** — read from `02-domain-model/phase-1-sqlite-adapter-contract.md`, `crates/memory-storage-sqlite/src/lib.rs`, `crates/memory-event-store-sqlite/src/lib.rs` on `main`.
- Prompt schema contents: **VERIFIED** — read from `prompts-fix/P2-T2-memory-schema.md`.
- The four contradictions in §2.3: **VERIFIED** by direct comparison of the two sources.
- This proposal's own recommendations: **PROPOSED**, author-authored, not independently reviewed.
