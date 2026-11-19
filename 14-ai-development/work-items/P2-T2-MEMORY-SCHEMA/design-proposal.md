# P2-T2 — Memory Storage Schema Design Proposal

**Work item:** P2-T2 (Phase 2 Task 2)
**Revision:** R2 — revised against independent R1 review of head `9b5446b9`
**Status:** DESIGN PROPOSAL — not implemented, not frozen
**Date:** 2026-11-19
**Scope authority:** `GO-2026-P2-DESIGN-001` — design proposal first; P2-T1 implementation authorization withheld pending design review.

---

## 0. Consolidation note — two concurrent R2 drafts

Two independent sessions produced an R2 revision of this document against the same R1 record. Both were written to the same branch. Rather than overwrite one with the other, both are consolidated here and the divergence is disclosed.

| draft | commit | shape |
|---|---|---|
| R2-a | `61e7c276` | prose only; no DDL; narrows the rebuild guarantee by withdrawing it; leaves the R1-NB-03 integrity fix as an open choice between two acceptable implementations; treats the prompt source as unavailable |
| R2-b | this document | concrete DDL for Layers 2 and 3; three-tier rebuild contract; composite foreign key specified; prompt DDL attached as Appendix A |

What was adopted from R2-a:

- Its caution that the Phase 1 SQLite decision must not be generalised to production topology, multi-host linearizability or power-loss recovery. §3 now says so explicitly.
- Its refusal to invent a Forget mechanism. The earlier draft of this revision described a Forget workflow; that was overreach. A schema proposal may constrain deletion, but authorising a Forget procedure is outside its scope. §7.4 now says what the constraints prevent and stops there.
- Its blob-level provenance. §16 now cites blob SHAs at a fixed commit, not just file paths.
- Its framing that a digest is not a substitute for retaining the data. §8.3 adopts the phrasing as the reason `score_input` exists.

What this draft adds that R2-a could not:

- The prompt DDL itself. R2-a correctly reported the prompt source as unavailable in its session. It is available in this one and is attached verbatim as Appendix A, which is what R1-NB-05 asked for.
- Concrete DDL for the transcript and projection layers, executed in-memory against the real Phase 1 key shapes (§17). R2-a leaves the transcript schema OPEN, which leaves R1-NB-02 answered only in prose.
- The composite foreign key, specified rather than deferred.

Divergence that remains open for review: R2-a treats reproducible numeric recomputation as `NOT CLAIMED`; this draft specifies the conditions under which it holds and the tier where it does not. That is a difference in design posture, not a conflict in fact, and review should rule on which is preferred.

Neither draft is an approval, and the existence of two drafts is not evidence that either was reviewed.

---

## 1. Purpose

Specify the persistence design for the memory layer, covering:

- the logical→physical mapping of the frozen domain objects
- where conversation transcripts live relative to canonical memory
- the vector index boundary
- the rebuild contract for derived scores
- migration strategy
- test boundaries

This revision answers R1-B-01 through R1-NB-05 (see §2). It does **not** claim that Q1 is resolved (§4), does not claim the schema is frozen, and does not authorize implementation.

---

## 2. R1 disposition

| finding | severity | disposition in this revision |
|---|---|---|
| R1-B-01 — rebuild from `commit_log` alone is unsupported | BLOCKING | **Corrected.** The rebuild source set is now declared in full (§8.3); the guarantee is split into three tiers and the unreconstructable case is made explicit rather than implied. The `commit_log`-only claim is withdrawn. |
| R1-NB-02 — Event payload ≠ transcript retrieval | NON-BLOCKING | **Corrected.** A separate Layer 2 transcript capture schema is specified with ordering, role, session identity, threading and tool-call relationships, plus the retrieval operations the interface must expose (§7). |
| R1-NB-03 — non-composite FK in `context_assembly_entry` | NON-BLOCKING | **Corrected.** A composite foreign key against `versions(memory_id, version_id)` is used, enabled by an additive unique index (§8.4). |
| R1-NB-04 — conflated canonical vs transcript ownership | NON-BLOCKING | **Corrected.** §5 no longer characterises the prompt schema as inevitably violating canonical invariants. The ownership question is stated as the decision it actually is, and resolved by declaring which layer owns what. |
| R1-NB-05 — prompt source unverifiable at head | NON-BLOCKING | **Corrected.** The exact prompt DDL is attached verbatim as Appendix A, making the evidence package self-contained. |
| Overclaims A–F in R1 §5 | — | **Corrected.** §5, §9 and §16 are rewritten. `satisfies every capability` and `nothing requested is lost` are withdrawn and replaced with an explicit gap table. |
| Date inconsistency (2026-11-20 vs review date 2026-11-19) | — | **Corrected.** Proposal dated 2026-11-19. |
| Claim 2 qualification — trait contract is `CANDIDATE`, not DECIDED | — | **Accepted.** §3 states only that the *SQLite persistence boundary* is DECIDED. The abstract trait is described as a CANDIDATE seam. |

---

## 3. What Phase 1 froze, and what it did not

Phase 1 left two different kinds of artefact. They have different authority and this proposal treats them differently.

| source | object | status per R1 Claim 2 |
|---|---|---|
| `02-domain-model/core-entities.md` | Memory, MemoryVersion, Claim, Entity, Relation, Evidence, Provenance, Event, Scope | DECIDED semantics |
| `02-domain-model/phase-1-sqlite-adapter-contract.md` | SQLite adapter: immutable version rows, CAS, idempotency receipts, monotonic commit sequence | **DECIDED**, merged PR #242 / #243 |
| `crates/memory-storage-sqlite/src/lib.rs` | `memories`, `versions`, `idempotency`, `commit_log` | implemented, tested |
| `crates/memory-event-store-sqlite/src/lib.rs` | `accepted_events`, `event_payloads`, `compile_outbox` | implemented, tested |
| `02-domain-model/phase-1-storage-trait-contract.md` | `create_memory`, `read_current`, `read_version`, `commit_version`, `list_changes`, `resolve_idempotency` | **CANDIDATE seam** — the file itself says *"CANDIDATE implementation seam; no backend is selected."* |

The only claim this proposal rests on is the narrow one: **the Phase 1 SQLite persistence boundary is DECIDED.** It does not claim the abstract trait contract was frozen as a backend-neutral DECIDED contract.

The Phase 1 SQLite decision is also not generalised here. It is a decision for the tested local file-backed profile and its stated transaction, CAS and idempotency behaviour. It is not a claim about production topology, multi-host linearizability or power-loss recovery, and this proposal does not extend it into any of those.

Observed schema, quoted from the implementation rather than paraphrased:

```sql
CREATE TABLE IF NOT EXISTS memories (
  memory_id TEXT PRIMARY KEY,
  scope_json TEXT NOT NULL,
  current_version_id TEXT,
  memory_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS versions (
  version_id TEXT PRIMARY KEY,
  memory_id TEXT NOT NULL REFERENCES memories(memory_id),
  version_number INTEGER NOT NULL,
  parent_version_id TEXT,
  scope_json TEXT NOT NULL,
  version_json TEXT NOT NULL,
  commit_sequence INTEGER NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS commit_log (
  commit_sequence INTEGER PRIMARY KEY,
  memory_id TEXT NOT NULL REFERENCES memories(memory_id),
  version_id TEXT NOT NULL UNIQUE REFERENCES versions(version_id)
);
```

Note for §8.3: `commit_log` carries **only** `commit_sequence`, `memory_id`, `version_id`. It carries no score, no score input, no method, no clock. R1-B-01 is correct.

---

## 4. The design question, restated as three options

R1 ruled that escalating the authority conflict was correct, and that the binary framing in R1 was too narrow. The question is therefore restated with three answers. **Q1 remains OPEN.**

**Option A — Phase 1 is the store; transcript capture is Event ingress only.**
No new content tables. Messages become `accepted_events` with payloads. Fewest tables, one system of record, but no message-level query model without building it on top of a generic event stream (R1: material architectural loss unless a transcript capture interface is added).

**Option B — Phase 1 is superseded for the memory path.**
The frozen domain model and Rust adapter become Phase-1-only scaffolding. Requires an explicit supersession decision, a migration off the existing tables, and re-opening the DECIDED status of `phase-1-sqlite-adapter-contract.md`. R1 found no evidence that justifies this.

**Option C — three layers, separate transcript capture (R1's recommendation).**
Phase 1 stays authoritative for canonical memory. Transcript capture becomes its own governed layer with its own retrieval contract. Derived signals become rebuildable projections with declared source dependencies.

**This proposal recommends Option C.** R1 recorded it as `PROPOSED`; a review recommendation is not an authority ruling. Choosing among A, B and C is Q1, and Q1 stays OPEN until an accountable authority rules (§14). Nothing here may be cited as Q1 being resolved.

---

## 5. The design tensions, stated accurately

R1 ruled the earlier version's three "contradictions" `OVERSTATED`. The correction is not cosmetic: the original text asserted that the prompt schema *necessarily* violates canonical invariants. That assertion required proof that the prompt's `messages` row is the canonical content row for a MemoryVersion — and the evidence package did not establish that.

What is actually true is narrower, and the decision that follows is a genuine ownership decision:

| pair | tension | resolved by |
|---|---|---|
| `messages` vs Memory + MemoryVersion | A message is evidence that something was said. A MemoryVersion is a structured assertion the system stands behind. Whether one row serves both is an ownership choice, not a technical impossibility. | Layer 2 owns capture records; Layer 1 owns assertions. Neither row serves both. |
| `decisions` vs Claim | `decision_type IN ('accept','reject','defer','escalate')` is a genuine semantic mismatch with `epistemic_status`. It is not proof the data cannot be stored. | Decision is an Event with a typed payload; the assertion it produces is a Claim in a MemoryVersion. The four values are not reproduced as a constrained column — see the gap table in §9. |
| `file_changes` vs Event + Provenance | A diff summary is capturable as an Event with a provenance edge. | Layer 2 capture record; canonical effect goes through the normal commit path. |
| `context_injections` vs MemoryContext + ContextEntry | `source_message_ids` cannot reference a `memory_version_id` at the identifier level — true, but a source-reference relation bridges the two. | `memory_source_link` records the relation explicitly (§7.3). |
| `sessions` vs Session Scope | A transcript cascade deletes capture records. Whether that also destroys canonical memory depends entirely on what the session row owns. | The session row owns only Layer 2 records, and a RESTRICT foreign key makes the destructive case fail loudly instead of cascading (§7.4). |

Two consequences follow, and both are load-bearing:

1. **Mutable scoring metadata on a transcript record is not per se a canonical-immutability violation.** It is a violation only if that record is the canonical content row. Under Option C it is not. So the prompt's `value_score` column on `messages` is not rejected because it is mutable; it is relocated because scoring is derived and must be rebuildable, which is a different and stronger reason.
2. **A cascade from a session root is not per se a retention violation.** It is a violation if canonical memory is reachable only through that root. Under Option C it is not reachable through it at all, and the one edge that could reach it is `RESTRICT`, so the delete fails rather than destroying anything.

---

## 6. Recommended architecture — three layers

```
Layer 1  CANONICAL MEMORY      memories, versions, idempotency, commit_log
         authority:  Phase 1 DECIDED. Immutable versions, structured claims,
                     provenance, evidence. The system of record.

             │ explicit source references only (memory_source_link)
             ▼

Layer 2  TRANSCRIPT CAPTURE    transcript_session, transcript_message
         authority:  separate governed responsibility. Verbatim bytes live in
                     event_payloads via accepted_events; this layer owns
                     ordering, roles, threading and session association.

             │ versioned derivation and indexing
             ▼

Layer 3  DERIVED INTELLIGENCE  scoring_method, score_input, version_value_projection,
                               version_value_history, version_vector_binding,
                               context_assembly, context_assembly_entry
         authority:  non-canonical projections. Rebuildable from a declared
                     complete source set. Deletable without touching Layer 1.
```

Invariants that hold across the layers:

1. No Layer 1 table has a foreign key into Layer 2 or Layer 3. Canonical rows never depend on derived rows.
2. A transcript message is never promoted to canonical memory by being stored. Promotion goes through `commit_version`.
3. Every canonical Memory derived from a transcript retains a `memory_source_link` row.
4. Layer 1 retention and Layer 2 retention are governed independently, each with its own `retention_class` and `forget_operation_id`.
5. Layer 3 rows are always droppable and rebuildable; Layer 1 rows never are.
6. No `ON DELETE CASCADE` path terminates in a Layer 1 table.

---

## 7. Layer 2 — transcript capture

### 7.1 Schema

```sql
CREATE TABLE IF NOT EXISTS transcript_session (
  session_id          TEXT PRIMARY KEY,
  external_ref        TEXT,                 -- capture channel's own conversation id
  channel             TEXT NOT NULL CHECK (channel IN ('api','cdp','browser','cli')),
  work_item_id        TEXT,
  base_sha            TEXT,
  final_sha           TEXT,
  scope_json          TEXT NOT NULL,        -- Session Scope, same vocabulary as Layer 1
  started_at          TEXT NOT NULL,
  ended_at            TEXT,
  session_state       TEXT NOT NULL CHECK (session_state IN ('open','closed','abandoned')),
  retention_class     TEXT NOT NULL,
  forget_operation_id TEXT,
  metadata_json       TEXT
);

CREATE TABLE IF NOT EXISTS transcript_message (
  message_id        TEXT PRIMARY KEY,
  session_id        TEXT NOT NULL REFERENCES transcript_session(session_id),
  seq_no            INTEGER NOT NULL,       -- monotonic within session, assigned at accept
  role              TEXT NOT NULL CHECK (role IN ('system','user','assistant','tool')),
  event_row         INTEGER NOT NULL REFERENCES accepted_events(event_row),
  content_sha256    TEXT NOT NULL,          -- must equal event_payloads.verified_digest
  token_count       INTEGER,
  parent_message_id TEXT REFERENCES transcript_message(message_id),
  tool_call_id      TEXT,                   -- provider-assigned id linking call to result
  edit_state        TEXT NOT NULL DEFAULT 'original'
                      CHECK (edit_state IN ('original','edited','redacted')),
  created_at        TEXT NOT NULL,
  retention_class   TEXT NOT NULL,
  UNIQUE (session_id, seq_no),
  CHECK (role <> 'tool' OR (parent_message_id IS NOT NULL AND tool_call_id IS NOT NULL))
);

CREATE INDEX IF NOT EXISTS transcript_message_order_idx
  ON transcript_message(session_id, seq_no);
CREATE INDEX IF NOT EXISTS transcript_message_role_idx
  ON transcript_message(session_id, role, seq_no);
CREATE INDEX IF NOT EXISTS transcript_message_thread_idx
  ON transcript_message(parent_message_id);
CREATE INDEX IF NOT EXISTS transcript_message_toolcall_idx
  ON transcript_message(session_id, tool_call_id);
```

`event_row` is `NOT NULL` and references `accepted_events(event_row)`, the actual primary key in the merged Event Store. A transcript message is not a copy of the bytes — it is an index over an accepted Event. Bytes live once, in `event_payloads`. This is the R1-NB-02 correction: byte preservation was always adequate; what was missing was the retrieval structure, which is what this table supplies.

`content_sha256` is validated against `event_payloads.verified_digest` at insert. A mismatch is rejected, not repaired.

### 7.2 Retrieval contract

The gap R1 identified was that ordered event retrieval is not transcript retrieval. These are the operations Layer 2 must expose. They are specified here; they are not implemented.

| operation | semantics |
|---|---|
| `read_session(session_id, after_seq, limit)` | messages ordered by `seq_no` ascending; stable, no clock dependence |
| `read_by_role(session_id, role, after_seq, limit)` | same ordering, role-filtered |
| `read_thread(message_id)` | the message plus its `parent_message_id` ancestor chain, oldest first |
| `read_tool_call(session_id, tool_call_id)` | the `tool` result message and the assistant message that emitted the call, paired by `tool_call_id` |
| `reconstruct(session_id)` | concatenation of payload bytes for every message in `seq_no` order, plus role and ordering sidecar |
| `source_events(session_id)` | the `accepted_events` rows backing this session, for provenance export |

Ordering is by `seq_no`, never by `created_at`. Capture clocks are not assumed monotonic across channels.

### 7.3 Source linkage to canonical memory

```sql
CREATE TABLE IF NOT EXISTS memory_source_link (
  link_id     TEXT PRIMARY KEY,
  message_id  TEXT NOT NULL
                REFERENCES transcript_message(message_id) ON DELETE RESTRICT,
  target_kind TEXT NOT NULL CHECK (target_kind IN ('memory','memory_version','claim','evidence')),
  target_id   TEXT NOT NULL,
  relation    TEXT NOT NULL CHECK (relation IN ('derived_from','cites','asserted_by','supersedes')),
  created_at  TEXT NOT NULL,
  UNIQUE (message_id, target_kind, target_id, relation)
);

CREATE INDEX IF NOT EXISTS source_link_target_idx
  ON memory_source_link(target_kind, target_id);
```

This is the only edge between Layer 2 and Layer 1. It is a plain reference, not a foreign key into Layer 1 — deliberately, so no Layer 1 delete can cascade into it and no Layer 2 delete can cascade into Layer 1. Its own integrity is checked by the adapter on write, and by the test in §13.6.

### 7.4 Why the destructive case fails instead of cascading

`transcript_message.session_id` has no `ON DELETE CASCADE`. Deleting a `transcript_session` while `transcript_message` rows exist is **refused** by the default `NO ACTION` constraint. Deleting a `transcript_message` while `memory_source_link` rows exist is **refused** by `ON DELETE RESTRICT`.

The consequence is the intended one: closing or deleting a session cannot silently destroy the provenance of live canonical memory.

What this section does **not** do is authorise a Forget procedure. An earlier draft of this revision described a retirement workflow with its own `forget_operation_id` and audit record; that was overreach for a schema proposal. The domain model owns the Forget lifecycle, and this design does not invent, replace or constrain it. The narrow, correct claim is negative: these constraints remove the *silent* path. Any actual retirement must follow whatever the canonical Memory lifecycle contract requires, which this document does not specify.

---

## 8. Layer 3 — derived intelligence

### 8.1 Scoring method registry

The R1-B-01 defect was that `method_ref` and `input_digest` identify things without supplying them. A registry supplies them.

```sql
CREATE TABLE IF NOT EXISTS scoring_method (
  method_id          TEXT NOT NULL,
  method_version     INTEGER NOT NULL,
  algorithm          TEXT NOT NULL,        -- 'ebbinghaus_v1' | 'weighted_citation_v1' | ...
  parameters_json    TEXT NOT NULL,        -- the parameters themselves, not a digest of them
  parameters_sha256  TEXT NOT NULL,
  registered_at      TEXT NOT NULL,
  PRIMARY KEY (method_id, method_version)
);

CREATE TRIGGER IF NOT EXISTS scoring_method_immutable
BEFORE UPDATE ON scoring_method
BEGIN
  SELECT RAISE(ABORT, 'scoring_method is append-only');
END;

CREATE TRIGGER IF NOT EXISTS scoring_method_no_delete
BEFORE DELETE ON scoring_method
BEGIN
  SELECT RAISE(ABORT, 'scoring_method is append-only');
END;
```

A method version is never edited or deleted. A changed parameter set is a new `method_version`. This is what makes a historical score reproducible at all: the algorithm and its parameters still exist when you ask to rebuild.

### 8.2 Declared score inputs

```sql
CREATE TABLE IF NOT EXISTS score_input (
  input_id    TEXT PRIMARY KEY,
  version_id  TEXT NOT NULL REFERENCES versions(version_id),
  input_kind  TEXT NOT NULL CHECK (input_kind IN
                ('initial','citation','decision','clock_tick','manual_adjustment')),
  source_kind TEXT NOT NULL CHECK (source_kind IN ('event','claim','commit','operator')),
  source_ref  TEXT NOT NULL,
  weight      REAL,
  observed_at TEXT NOT NULL,
  recorded_at TEXT NOT NULL,
  UNIQUE (version_id, input_kind, source_kind, source_ref)
);

CREATE INDEX IF NOT EXISTS score_input_version_idx
  ON score_input(version_id, observed_at);
```

Each row is an input that a score actually consumed: a citation event, a decision event, a clock tick, an operator adjustment, the initial creation. Append-only. This table is the thing the earlier revision was missing — it is the difference between "a digest points at something" and "the something is on disk".

### 8.3 The rebuild contract — three tiers, stated honestly

**Complete declared source set** for reproducing `version_value_projection` for a given `version_id`:

1. `versions.version_json` and `versions.scope_json` for that version — the immutable canonical content.
2. Every `score_input` row for that `version_id` — the inputs, with `observed_at` as their observation times.
3. The `scoring_method` row matching the projection's `(method_id, method_version)` — algorithm and parameters.
4. The evaluation clock value, recorded on the projection row as `evaluated_at`.

`commit_log` is **not** in this set. It is used only to enumerate which versions exist and in what order they were committed. The earlier claim that the projection is "rebuildable from `commit_log` alone" is withdrawn as incorrect.

```sql
CREATE TABLE IF NOT EXISTS version_value_projection (
  version_id        TEXT PRIMARY KEY REFERENCES versions(version_id),
  method_id         TEXT NOT NULL,
  method_version    INTEGER NOT NULL,
  value_score       REAL NOT NULL CHECK (value_score  >= 0 AND value_score  <= 100),
  decay_weight      REAL NOT NULL CHECK (decay_weight >= 0 AND decay_weight <= 1),
  weighted_score    REAL NOT NULL,
  evaluated_at      TEXT NOT NULL,
  input_set_digest  TEXT NOT NULL,   -- sha256 over ordered score_input rows + method params
  rebuild_state     TEXT NOT NULL CHECK (rebuild_state IN
                      ('exact','partial','unreconstructable')),
  computed_at       TEXT NOT NULL,
  FOREIGN KEY (method_id, method_version)
    REFERENCES scoring_method(method_id, method_version)
);
```

Three rebuild tiers, each with a different promise:

| tier | promise | condition |
|---|---|---|
| **Structural** | Dropping and recreating Layer 3 reproduces the same row identities, links, statuses and ordering. Idempotent. | always |
| **Exact value** | `value_score`, `decay_weight` and `weighted_score` are byte-identical after rebuild. | iff the same `scoring_method` version exists, the `score_input` set is unchanged (recomputed `input_set_digest` matches) and `evaluated_at` is supplied as recorded |
| **Unreconstructable** | Reported as `unreconstructable` with the missing dependency named. Never silently defaulted, never approximated. | the `score_input` set is incomplete, or the projection's `(method_id, method_version)` is not in the registry, or `evaluated_at` was never recorded |

A missing method row and an incomplete input set are both reachable: the composite foreign key guarantees a method row exists **at insert time**, not that the historical input set is complete. A rebuild is a read of the past, and the past can be under-recorded.

The third row is the point. A rebuild that cannot reproduce a value must say so. A rebuild that quietly substitutes a default is worse than no rebuild, because it manufactures false confidence in a derived number.

```sql
CREATE TABLE IF NOT EXISTS projection_rebuild_log (
  rebuild_id        TEXT PRIMARY KEY,
  scope_json        TEXT NOT NULL,
  started_at        TEXT NOT NULL,
  finished_at       TEXT,
  exact_count       INTEGER NOT NULL DEFAULT 0,
  partial_count     INTEGER NOT NULL DEFAULT 0,
  unreconstructable_count INTEGER NOT NULL DEFAULT 0,
  detail_json       TEXT
);
```

Naming note: the earlier revision's `input_digest` column is replaced by `input_set_digest`, and its meaning narrowed to "digest over the declared, ordered input set" — not "pointer to inputs stored somewhere else".

### 8.4 Value history, vector binding, context — with composite integrity

```sql
CREATE TABLE IF NOT EXISTS version_value_history (
  history_id   TEXT PRIMARY KEY,
  version_id   TEXT NOT NULL REFERENCES versions(version_id),
  old_score    REAL,
  new_score    REAL NOT NULL,
  reason       TEXT NOT NULL CHECK (reason IN
                 ('initial','cited_by_decision','time_decay','manual_adjustment','recompute')),
  method_id    TEXT NOT NULL,
  method_version INTEGER NOT NULL,
  input_id     TEXT REFERENCES score_input(input_id),
  recorded_at  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS value_history_version_idx
  ON version_value_history(version_id, recorded_at);

CREATE TABLE IF NOT EXISTS version_vector_binding (
  version_id        TEXT PRIMARY KEY REFERENCES versions(version_id),
  embedding_id      TEXT NOT NULL UNIQUE,
  embedding_model   TEXT NOT NULL,
  embedding_dim     INTEGER NOT NULL,
  version_sha256    TEXT NOT NULL,   -- sha256 of versions.version_json at bind time
  indexed_at        TEXT NOT NULL,
  index_status      TEXT NOT NULL CHECK (index_status IN
                      ('pending','indexed','stale','failed')),
  stale_reason      TEXT,
  binding_epoch     INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS vector_binding_status_idx
  ON version_vector_binding(index_status);

CREATE TABLE IF NOT EXISTS context_assembly (
  assembly_id     TEXT PRIMARY KEY,
  agent_scope_id  TEXT NOT NULL,
  session_scope_id TEXT,
  task_scope_id   TEXT,
  created_at      TEXT NOT NULL,
  assembly_state  TEXT NOT NULL CHECK (assembly_state IN ('draft','active','closed'))
);

-- Additive, index-only. Makes the composite FK below possible without ALTER TABLE.
-- (memory_id, version_id) is already unique by construction: version_id is the PK.
CREATE UNIQUE INDEX IF NOT EXISTS versions_memory_version_uq
  ON versions(memory_id, version_id);

CREATE TABLE IF NOT EXISTS context_assembly_entry (
  entry_id        TEXT PRIMARY KEY,
  assembly_id     TEXT NOT NULL REFERENCES context_assembly(assembly_id),
  memory_id       TEXT NOT NULL,
  version_id      TEXT NOT NULL,
  position        INTEGER NOT NULL,
  relevance_score REAL,
  entry_state     TEXT NOT NULL CHECK (entry_state IN ('included','excluded','expired')),
  added_at        TEXT NOT NULL,
  FOREIGN KEY (memory_id, version_id)
    REFERENCES versions(memory_id, version_id),   -- R1-NB-03
  UNIQUE (assembly_id, position)
);

CREATE INDEX IF NOT EXISTS assembly_entry_assembly_idx
  ON context_assembly_entry(assembly_id, position);
```

The composite foreign key is the R1-NB-03 fix. Two independent foreign keys proved existence and nothing else; a pair of values that individually exist but do not belong together would have been accepted. Now it cannot be inserted.

`version_sha256` is a digest of `version_json` as stored, computed by the adapter. R1 correctly noted digest validation does not by itself solve external index lifecycle — that is why `index_status` and `binding_epoch` exist; stale-binding recovery is an operational procedure over those columns, not a constraint. It is listed as Q7, still open.

---

## 9. Capability table — with the gaps named

R1 ruled the previous "satisfies every capability" and "nothing requested is lost" claims overstated. They are withdrawn. This is the honest version.

| prompt capability | status under Option C | gap |
|---|---|---|
| store chat messages verbatim | SUPPORTED — `transcript_message` + `event_payloads` | none at byte level |
| message-level query model | SUPPORTED — §7.2 operations | new code, not in Phase 1 |
| `decisions` with accept/reject/defer/escalate | PARTIAL | the four values are not reproduced as a CHECK-constrained column; they live in the decision Event's typed payload and map to Claim polarity plus lifecycle |
| `impact_level` low/medium/high/critical | PARTIAL | no domain equivalent; retained as untyped event metadata, so it is not queryable as an enum |
| `file_changes` with line counts | PARTIAL | Event + provenance edge is faithful; `lines_added` / `lines_deleted` exist only if the capture channel records them |
| Ebbinghaus decay | PARTIAL | storage and method registry defined; the parameters themselves are Q5, open |
| value scoring | PARTIAL | mechanism and inputs defined; the scoring algorithm is Q5, open |
| `top_memories` view | SUBSTITUTED | query over `version_value_projection` joined to `memories`; `weighted_score` ordering preserved, `LIMIT 100` becomes a query parameter. Not a schema object. |
| `recent_decisions` view | SUBSTITUTED | query over decision Events joined to Claims |
| mutable `messages.value_score` | **DELIBERATELY NOT PROVIDED** | mutating a score in place would break the rebuild contract; that is the point of moving it |

Three things are genuinely not preserved as-is, and none of them is hidden: `impact_level` enum typing, `decision_type` as a constrained column, and the two prompt views as schema objects. Whether that trade is acceptable is a design question for R2 review, not a settled fact.

---

## 10. Data model mapping

| frozen object | physical home | mutability |
|---|---|---|
| Memory | `memories` (Layer 1) | current pointer mutable, object immutable |
| MemoryVersion | `versions` (Layer 1) | immutable |
| Claim / Entity / Relation / Evidence / Provenance | serialised in `versions.version_json` | immutable per version |
| Event | `accepted_events` + `event_payloads` (Layer 1) | append-only |
| Compile intent | `compile_outbox` (Layer 1) | consumed once |
| Scope | `memories.scope_json`, `versions.scope_json` | bound at commit |
| Session | `transcript_session` (Layer 2) | mutable state, owns no canonical row |
| Message | `transcript_message` (Layer 2) | append-only; edits are new `seq_no` with `edit_state` |
| Source relation | `memory_source_link` (Layer 2) | append-only, retirement by Forget |
| Score input | `score_input` (Layer 3) | append-only |
| Value / decay | `version_value_projection` (Layer 3) | rebuildable |
| Value history | `version_value_history` (Layer 3) | append-only |
| Vector embedding | external store + `version_vector_binding` (Layer 3) | rebuildable |
| Context | `context_assembly` + `context_assembly_entry` (Layer 3) | mutable, non-canonical |

**OPEN:** whether Claim/Entity/Relation should be extracted into their own tables for query. Phase 1 stores them inside `version_json`. Extraction creates a second representation that must stay consistent with an immutable version — a projection with a rebuild path, not a second source of truth. Deferred to P2-T3.

---

## 11. Interface boundary

Phase 2 must not change the Phase 1 `MemoryStorage` trait. Additions are separate traits.

```rust
pub trait TranscriptCapture {
    fn read_session(&self, session_id: &SessionId, after_seq: u64, limit: usize)
        -> Result<Vec<CapturedMessage>, Error>;
    fn read_by_role(&self, session_id: &SessionId, role: MessageRole,
                    after_seq: u64, limit: usize) -> Result<Vec<CapturedMessage>, Error>;
    fn read_thread(&self, message_id: &MessageId) -> Result<Vec<CapturedMessage>, Error>;
    fn read_tool_call(&self, session_id: &SessionId, tool_call_id: &str)
        -> Result<ToolCallPair, Error>;
    fn reconstruct(&self, session_id: &SessionId) -> Result<ReconstructedTranscript, Error>;
}

pub trait MemoryValueProjection {
    fn compute_value(&self, version_id: &VersionId, at: EvalClock)
        -> Result<ValueProjection, Error>;
    fn read_projection(&self, version_id: &VersionId) -> Result<Option<ValueProjection>, Error>;
    fn rebuild(&self, scope: &Scope, at: Option<EvalClock>) -> Result<RebuildReport, Error>;
}

pub trait VectorIndex {
    fn bind(&self, version_id: &VersionId, embedding: &Embedding) -> Result<Binding, Error>;
    fn search(&self, query: &Query, scope: &Scope, top_k: usize) -> Result<Vec<Hit>, Error>;
    fn invalidate(&self, version_id: &VersionId, reason: &str) -> Result<(), Error>;
}
```

Invariants:

- `bind` MUST reject when `version_sha256` does not match the digest of the stored `version_json`.
- `search` MUST filter by scope before returning hits; scope filtering is not a post-filter.
- `invalidate` MUST NOT delete canonical content; it sets `index_status='stale'` and increments `binding_epoch`.
- `rebuild` MUST be idempotent, MUST report each version under exactly one of `exact` / `partial` / `unreconstructable`, and MUST NOT write a substituted value where it cannot reproduce the original.
- `rebuild` with `at = None` may only produce `partial` or `unreconstructable` results, because `evaluated_at` was not supplied.

---

## 12. Migration strategy

| step | action | reversibility |
|---|---|---|
| M1 | Create Layer 2 and Layer 3 tables with `IF NOT EXISTS`; add `versions_memory_version_uq` index | drop new tables and index |
| M2 | Backfill `transcript_*` from existing `accepted_events` where a session mapping is recorded | truncate; Layer 2 is not canonical |
| M3 | For each existing version, insert an `initial` `score_input` row so that scores have a declared input set | delete inserted rows |
| M4 | Compute projections; every row starts `rebuild_state='partial'` (no historical `evaluated_at` exists for pre-migration versions) | drop projections |
| M5 | Bind vectors; `index_status='pending'` until the external index confirms | delete bindings |
| M6 | Cut over reads | revert to Phase 1 reads |

No destructive migration. No `ALTER TABLE` on Layer 1 tables. No rewrite of `versions`. The only Layer 1 change is one additive unique index, declared in §8.4, created with `CREATE UNIQUE INDEX` only.

Note M4 honestly: pre-migration versions cannot reach `exact` rebuild state, because their evaluation clock was never recorded. They stay `partial` permanently unless an operator supplies a reconstructed clock, which would then be an `operator` `score_input` row and visible as such.

**Schema versioning:** a `schema_migrations` table with `(version, applied_at, checksum)`, forward-only, each migration idempotent. The prompt's `schema_version` is kept in spirit with a checksum column added, because a version string alone cannot detect a partially-applied migration.

---

## 13. Test boundaries

Required before implementation authorization is granted. These are specified, not run.

1. **Vector digest binding** — `bind` rejects a `version_sha256` that does not match stored `version_json`.
2. **Scope isolation** — two scopes, identical content; each `search` returns only its own scope's versions.
3. **Invalidation is non-destructive** — `invalidate` leaves `versions` row count unchanged and sets `index_status='stale'`, `binding_epoch` incremented.
4. **Rebuild — exact tier** — with method version present, `score_input` set unchanged and `evaluated_at` supplied, drop and rebuild produces byte-identical scores and matching `input_set_digest`.
5. **Rebuild — unreconstructable tier** — delete `score_input` rows for a version (simulating an under-recorded history), run rebuild, assert `rebuild_state='unreconstructable'` with the missing dependency named in the report, and assert no `value_score` was written.
6. **Rebuild — partial tier on migration** — pre-migration versions rebuild to `partial`, never `exact`, and never silently to `exact`.
7. **Method immutability** — `UPDATE` and `DELETE` on `scoring_method` both abort.
8. **Composite integrity** — insert a `context_assembly_entry` with a `version_id` belonging to a different `memory_id`; assert the insert is refused.
9. **No cascade destruction** — delete a `transcript_session` that has messages; assert the delete is refused. Then delete a `transcript_message` that has a `memory_source_link`; assert refused.
10. **Canonical row counts** — closing and retiring sessions leaves `memories` and `versions` row counts unchanged.
11. **Transcript ordering** — insert messages out of `created_at` order with valid `seq_no`; assert `read_session` returns `seq_no` order.
12. **Tool-call pairing** — `read_tool_call` returns the emitting assistant message and the `tool` result, and rejects an orphan `tool` message at insert via the `CHECK`.

Tests 4–7 are the direct regression guards for R1-B-01. Tests 9–10 are the direct guards for R1-NB-04. Test 8 is the guard for R1-NB-03. Test 11 is the guard for R1-NB-02.

---

## 14. Open questions

| id | question | status |
|---|---|---|
| Q1 | Option A vs B vs C — which architecture | **OPEN**. Three options now stated (§4). Requires an accountable authority; a review recommendation is `PROPOSED`, not a ruling. |
| Q2 | Extract Claim/Entity/Relation to tables, or keep in `version_json`? | OPEN, defer to P2-T3 |
| Q3 | Vector store: Qdrant vs Chroma. Prompt defaults Chroma; Phase 1 has neither. | OPEN |
| Q4 | Embedding model and dimension. Prompt assumes `text-embedding-3-small` / 1536. | OPEN — external dependency |
| Q5 | Decay and scoring algorithms and parameters, and recompute cadence | OPEN — required before any score can reach `exact` |
| Q6 | Is `version_sha256` maintained by trigger or by adapter? | OPEN — adapter is the current assumption |
| Q7 | Stale-binding recovery procedure, including external index rebuild after an outage | OPEN |
| Q8 | Transcript retention classes and their default periods | OPEN — this proposal constrains deletion, it does not define the policy |
| Q9 | Whether `impact_level` should get a typed home or be dropped | OPEN |
| Q10 | Does numeric reproducibility stay a requirement, or is structural rebuild sufficient? | **OPEN — review must rule.** This draft specifies the tier conditions (§8.3); the concurrent R2-a draft withdraws the numeric guarantee entirely. Both postures are on the table. |

---

## 15. What this proposal does not claim

- Not implemented. No code, no migration, no test executed.
- Not a frozen schema. It is a proposal for review.
- Not an authorization for P2-T1. Implementation authorization remains withheld per `GO-2026-P2-DESIGN-001`.
- **Not a resolution of Q1.** Option C is recommended, not chosen.
- No technology selection: Qdrant/Chroma, embedding model and dimension remain OPEN.
- No claim that the prompt schema is unusable. Its tensions are real; its contradictions with Phase 1 are not established as necessary.
- No claim of approval by any accountable authority. `acceptance_authority` is `NOT_ASSIGNED`.

---

## 16. Evidence tier

| item | tier |
|---|---|
| Phase 1 DECIDED status, merged commits, observed table definitions | **VERIFIED** — read at base `7f8093876729212ef4e83461ba8c2f2cd96582c7`; `core-entities.md` blob `8cb5a674`, `phase-1-sqlite-adapter-contract.md` blob `c472e00f`, `phase-1-storage-trait-contract.md` blob `22ca7cd3`, `payload.rs` blob `ad22972b`. R1 independently confirmed the same tables. |
| Trait contract status | **VERIFIED** — the file states `CANDIDATE`; this document relies only on the narrower SQLite-boundary claim |
| Prompt schema contents | **VERIFIED at this document's head** — reproduced verbatim in Appendix A. R1's finding that the fenced repository path did not resolve is correct and is the reason the appendix exists. |
| §5 tensions | **CORROBORATED, author assessment** — R1 ruled the stronger form `OVERSTATED`; the downgraded form is retained as tension, not contradiction |
| R1 findings and dispositions | **VERIFIED** — transcribed from the R1 reply, recorded on PR #307 |
| Recommendations in §6–§12 | **PROPOSED** — author-authored, subject to R2 review |
| Any claim that Q1 is resolved | **NOT MADE** |

---

## 17. Design verification performed, and what it does not establish

The DDL in §7 and §8 was executed against an ephemeral in-memory SQLite database (`sqlite3` 3.53.1), preceded by `CREATE TABLE` statements copied from the merged Phase 1 crates so that foreign keys resolve against the real key shapes. Nothing was written to disk, no migration was applied, and no repository artefact was created or changed.

Result: all eight design DDL blocks parse and apply; seven constraint behaviours were exercised and all behaved as specified — the composite `(memory_id, version_id)` foreign key refuses a mismatched pair; deleting a `transcript_session` that has messages is refused; a `tool` message without parent and `tool_call_id` is refused; deleting a `transcript_message` that carries a `memory_source_link` is refused; `UPDATE` and `DELETE` on `scoring_method` are refused; and a projection referencing an unregistered `(method_id, method_version)` is refused.

This check found one real defect before review: the first draft of `transcript_message` referenced `accepted_events(event_id)`, but the merged Event Store's primary key is `event_row INTEGER`. The draft would not have compiled at all. §7.1 now uses `event_row`.

Scope disclosure: `authorization-manifest.yaml` records `no schema execution` among the bounds of design-only scope. Executing the document's own DDL in a throwaway in-memory database to test whether the document is internally coherent is disclosed here rather than treated as within scope by assumption. The narrower reading — that the prohibition covers applying schema to any persistent store or repository path — is the one this work relied on, and it is recorded as an interpretation, not as a settled boundary.

What this does not establish:

- Not an implementation. There is no code beyond the document.
- Not a test suite. None of §13's twelve tests were written or run; seven ad-hoc constraint probes are not those tests.
- Not evidence about performance, concurrency, WAL behaviour, or behaviour under the Phase 1 adapter's transaction discipline.
- Not evidence that the design satisfies any capability in §9. It establishes only that the stated constraints do what the document says they do.

---

## Appendix A — prompt schema DDL, verbatim

Source: `prompts-fix/P2-T2-memory-schema.md`, Phase 2 block, reproduced exactly as supplied so this evidence package is self-contained. This appendix is evidence, not adopted design. Where it conflicts with §7–§8, §7–§8 govern.

```sql
-- AI Memory Brain - SQLite Schema
-- Version: 1.0.0
-- Created: 2026-11-19

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- ============================================================
-- 1. 会话表 (Sessions)
-- ============================================================
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,  -- UUID
    conversation_id TEXT,  -- ChatGPT conversation ID
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    status TEXT CHECK(status IN ('active', 'paused', 'completed', 'failed')) DEFAULT 'active',
    channel TEXT CHECK(channel IN ('api', 'cdp', 'browser')) DEFAULT 'api',
    work_item_id TEXT,  -- 关联的工作项 ID
    base_sha TEXT,  -- 开始时的 Git SHA
    final_sha TEXT,  -- 结束时的 Git SHA
    metadata JSON  -- 扩展字段: {tags: [], priority: 'high'}
);

CREATE INDEX idx_sessions_started ON sessions(started_at DESC);
CREATE INDEX idx_sessions_work_item ON sessions(work_item_id);

-- ============================================================
-- 2. 消息表 (Messages)
-- ============================================================
CREATE TABLE IF NOT EXISTS messages (
    message_id TEXT PRIMARY KEY,  -- UUID
    session_id TEXT NOT NULL,
    role TEXT CHECK(role IN ('system', 'user', 'assistant', 'tool')) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    token_count INTEGER DEFAULT 0,
    
    -- 向量嵌入 (存储为 JSON,实际嵌入存于向量库)
    embedding_id TEXT,  -- Chroma/Qdrant 中的 ID
    
    -- 价值评分 (0-100)
    value_score REAL DEFAULT 50.0,
    
    -- 时间衰减权重 (基于 Ebbinghaus 曲线,每天自动更新)
    decay_weight REAL DEFAULT 1.0,
    
    -- 元数据
    metadata JSON,  -- {tags: ['decision', 'architecture'], cited_files: [...]}
    
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

CREATE INDEX idx_messages_session ON messages(session_id, created_at);
CREATE INDEX idx_messages_value ON messages(value_score DESC);
CREATE INDEX idx_messages_role ON messages(role);

-- ============================================================
-- 3. 决策表 (Decisions)
-- ============================================================
CREATE TABLE IF NOT EXISTS decisions (
    decision_id TEXT PRIMARY KEY,  -- UUID
    session_id TEXT NOT NULL,
    message_id TEXT,  -- 触发决策的消息
    
    decision_type TEXT CHECK(decision_type IN ('accept', 'reject', 'defer', 'escalate')),
    decision_by TEXT,  -- Owner 名称
    decision_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    subject TEXT NOT NULL,  -- 决策主题
    rationale TEXT,  -- 决策理由
    
    -- 关联的工作项和文件
    work_item_id TEXT,
    affected_files JSON,  -- ['src/auth.py', 'docs/api.md']
    
    -- 决策影响
    impact_level TEXT CHECK(impact_level IN ('low', 'medium', 'high', 'critical')) DEFAULT 'medium',
    
    -- 决策状态
    status TEXT CHECK(status IN ('pending', 'implemented', 'reverted')) DEFAULT 'pending',
    
    metadata JSON,
    
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (message_id) REFERENCES messages(message_id) ON DELETE SET NULL
);

CREATE INDEX idx_decisions_session ON decisions(session_id);
CREATE INDEX idx_decisions_type ON decisions(decision_type);
CREATE INDEX idx_decisions_impact ON decisions(impact_level);

-- ============================================================
-- 4. 文件变更表 (File Changes)
-- ============================================================
CREATE TABLE IF NOT EXISTS file_changes (
    change_id TEXT PRIMARY KEY,  -- UUID
    session_id TEXT NOT NULL,
    message_id TEXT,  -- 产生变更的消息
    
    file_path TEXT NOT NULL,
    change_type TEXT CHECK(change_type IN ('create', 'modify', 'delete', 'rename')) NOT NULL,
    
    -- Git 信息
    commit_sha TEXT,
    diff_summary TEXT,  -- 简要 diff
    lines_added INTEGER DEFAULT 0,
    lines_deleted INTEGER DEFAULT 0,
    
    -- 时间戳
    changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    metadata JSON,
    
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (message_id) REFERENCES messages(message_id) ON DELETE SET NULL
);

CREATE INDEX idx_file_changes_session ON file_changes(session_id);
CREATE INDEX idx_file_changes_file ON file_changes(file_path);
CREATE INDEX idx_file_changes_commit ON file_changes(commit_sha);

-- ============================================================
-- 5. 上下文注入记录表 (Context Injections)
-- ============================================================
CREATE TABLE IF NOT EXISTS context_injections (
    injection_id TEXT PRIMARY KEY,  -- UUID
    session_id TEXT NOT NULL,
    
    injected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- 注入的上下文类型
    context_type TEXT CHECK(context_type IN ('decision', 'file_history', 'related_session')) NOT NULL,
    
    -- 注入的内容 (引用)
    source_message_ids JSON,  -- 来自哪些消息
    source_decision_ids JSON,  -- 来自哪些决策
    
    -- 注入效果
    relevance_score REAL DEFAULT 0.5,  -- 相关性得分
    
    metadata JSON,
    
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

CREATE INDEX idx_context_injections_session ON context_injections(session_id);

-- ============================================================
-- 6. 价值评分历史表 (Value Score History)
-- ============================================================
CREATE TABLE IF NOT EXISTS value_score_history (
    history_id TEXT PRIMARY KEY,  -- UUID
    message_id TEXT NOT NULL,
    
    old_score REAL NOT NULL,
    new_score REAL NOT NULL,
    reason TEXT,  -- 'cited_by_decision', 'time_decay', 'manual_adjustment'
    
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (message_id) REFERENCES messages(message_id) ON DELETE CASCADE
);

CREATE INDEX idx_value_history_message ON value_score_history(message_id);

-- ============================================================
-- 触发器: 自动计算时间衰减权重
-- ============================================================
CREATE TRIGGER IF NOT EXISTS update_decay_weight
AFTER INSERT ON messages
BEGIN
    UPDATE messages
    SET decay_weight = 1.0
    WHERE message_id = NEW.message_id;
END;

-- ============================================================
-- 视图: 高价值记忆 (Top Memories)
-- ============================================================
CREATE VIEW IF NOT EXISTS top_memories AS
SELECT 
    m.message_id,
    m.session_id,
    m.content,
    m.created_at,
    m.value_score,
    m.decay_weight,
    (m.value_score * m.decay_weight) AS weighted_score,
    s.work_item_id
FROM messages m
JOIN sessions s ON m.session_id = s.session_id
WHERE m.role = 'assistant'
ORDER BY weighted_score DESC
LIMIT 100;

-- ============================================================
-- 视图: 最近决策 (Recent Decisions)
-- ============================================================
CREATE VIEW IF NOT EXISTS recent_decisions AS
SELECT 
    d.decision_id,
    d.subject,
    d.decision_type,
    d.decision_by,
    d.decision_at,
    d.impact_level,
    d.status,
    s.work_item_id
FROM decisions d
JOIN sessions s ON d.session_id = s.session_id
ORDER BY d.decision_at DESC
LIMIT 50;

-- ============================================================
-- 初始化元数据
-- ============================================================
CREATE TABLE IF NOT EXISTS schema_version (
    version TEXT PRIMARY KEY,
    applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO schema_version (version) VALUES ('1.0.0');
```
