# P2-T2 — Memory Storage Schema Design Proposal

**Work item:** P2-T2 (Phase 2 Task 2)
**Revision:** R5 — revised against independent R4 review of head `bdb19ac0`; R5 confirmation round recorded (§2d)
**Status:** DESIGN PROPOSAL — not implemented, not frozen, not approved
**Review state:** `BLOCKED` — recorded independent-review disposition `REQUEST CHANGES` at R4; no R6 requested at R5. GitHub records no submitted review object for this PR.
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

This revision answers R1-B-01 through R1-NB-05 (§2), the seven items R2 required (§2a), the four findings R3 raised (§2b), and the one residual R4 found (§2c). It records Q1 as decided under the dev-baseline Architecture Owner role (§4), and does **not** claim resolution by an accountable human authority. It does not claim the schema is frozen and does not authorize implementation.

**Status supported by this document:** `BLOCKED — awaiting accountable authority assignment and governance decisions`. No revision of this document can close Q11 or Q12; they require an authority that is `NOT_ASSIGNED`. Q1 was decided by a decision record, not by revision, but that decision did not constitute acceptance by an accountable human authority; `acceptance_authority` remains `NOT_ASSIGNED` for Q1. See §4 and `DEC-P2-T2-Q1-001.md`.

No identified NF-R3-02 engineering-specification residue remains. DDL executability and regression behavior remain `UNVERIFIED`.

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

## 2a. R2 disposition

R2 was reviewed at head `aed58ad0` and returned `REQUEST CHANGES`, with R1-NB-04 closed and four new findings. Recorded on PR #307, comment `7023510140`.

| item | R2 ruling | disposition in R3 |
|---|---|---|
| R1-B-01 **(A)** algorithm identity ≠ reproducibility | still open | **Corrected.** `scoring_method` gains `algorithm_spec_ref`, `algorithm_spec_sha256` and a constrained `numeric_semantics`. A label without a retrievable spec text that hashes to the recorded value cannot support the exact tier. §8.1 |
| R1-B-01 **(B)** append-only not enforced on `score_input` | still open | **Corrected.** UPDATE and DELETE triggers added, matching the registry. Corrections become new rows via `corrects_input_id`. §8.2 |
| R1-NB-02 tool-call cardinality | partially closed | **Corrected.** `tool_call_id` removed from `transcript_message`; `transcript_tool_call` holds `(session_id, tool_call_id)` with `(emitting_message_id, call_index)` unique. §7.1 |
| R1-NB-02 reconstruction boundaries | partially closed | **Corrected.** `byte_length` stored per message and cross-checked; `reconstruct` returns frames with `byte_offset` / `byte_length` plus per-frame re-hash. §7.1, §7.2 |
| R1-NB-03 boundary — additive index is still a Layer 1 modification | technically corrected, boundary unresolved | **Accepted and corrected.** The index is now described as a Layer 1 modification. Both readings of the boundary are stated with the adapter-level fallback; the choice is Q11, not asserted. §8.4 |
| R1-NB-05 appendix provenance | partially closed | **Accepted without argument.** An appendix is reviewable but cannot authenticate its own origin. §16 records the limit; the remedy is stated. |
| R2-NF-01 tool-call and thread integrity | OPEN | **Corrected.** Composite self-reference on `(session_id, message_id)` forces parent and child into one session; a trigger forces a tool result's parent to be an assistant message. §7.1 |
| R2-NF-02 history provenance integrity | OPEN | **Corrected.** Two composite foreign keys: `(method_id, method_version)` → `scoring_method`, `(version_id, input_id)` → `score_input`. §8.4 |
| R2-NF-03 reconstruction framing | OPEN | **Corrected.** Same fix as R1-NB-02 boundaries. §7.2 |
| R2-NF-04 score-input immutability | OPEN | **Corrected.** Same fix as R1-B-01 (B). §8.2 |
| Q10 — rebuild posture | ruled: tiered preferred | **Recorded as ruled for tiered; exact value conditional and NOT VERIFIED.** §8.3, §14 |
| Disclosure A — two concurrent drafts | acceptable | **No change.** §0 retained. |
| Disclosure B — in-memory schema execution | **not acceptable as authorized activity**; `DISCLOSED SCOPE DEVIATION` | **Accepted as a deviation, not defended.** §17 rewritten: the check is recorded as a deviation, its authority is not claimed, and the question is escalated as Q12. |
| Disclosure C — no rebase | acceptable for review, update before integration | **Accepted.** No rebase performed in R3 either; the integration caveat is carried in §12. |

R3 does not challenge any R2 ruling. Where R2 said a thing was still open, R3 either fixes it or names what remains; it does not argue the ruling down.

---

## 2b. R3 disposition

R3 was reviewed at head `fb1f59de` and returned `REQUEST CHANGES` with four new findings. Recorded on PR #307, comment `7023884586`.

R3 closed three of the seven R2 items outright and was ruled partial on three. Those rulings are accepted as given.

| finding | R3 severity | disposition in R4 |
|---|---|---|
| NF-R3-01 nullable history provenance — `input_id IS NULL` reachable for any `reason` | BLOCKING | **Corrected.** `CHECK` binds the NULL exemption to `initial` and `time_decay` only. §8.4 |
| NF-R3-02 tool-call relational integrity — emitter role, result role, result parent, later UPDATE bypass | BLOCKING | **Corrected.** Four constraints: emitter-is-assistant, result-is-child-tool, `transcript_message_role_frozen`, `tool_call_identity_frozen` + `tool_call_state_transition`. §7.1 |
| NF-R3-03 cross-version correction reference | NON-BLOCKING | **Corrected.** `corrects_input_id` becomes a composite `(version_id, corrects_input_id)` reference. §8.2 |
| NF-R3-04 governance evidence inconsistency — manifest says `DISCLOSED_SCOPE_DEVIATION`, §17 said `DISCLOSED_INTERPRETATION`; §17 said thirteen tests, §13 listed sixteen | NON-BLOCKING | **Corrected, and it was my error.** §17 now states one classification, names the earlier contradiction rather than erasing it, and no longer repeats a test count. |

Two residues are recorded rather than closed: whether a `completed` call must carry a result (Q13), and whether `recompute` truly requires a single input (Q14). Both were flagged by R3 as questions R3 could not settle either.

R4 does not claim that NF-R3-01 and NF-R3-02 are *verified* fixed. They are fixed in the specification. The R3 DDL was never executed, and neither is the R4 DDL — Q12 remains open. What can be checked by reading is that the constraint text now exists and says what the prose says it says.

---

## 2c. R4 disposition — and why this is the last engineering round

R4 was reviewed at head `bdb19ac0` and returned `REQUEST CHANGES` with one residual defect and an explicit recommendation to stop the ordinary revision cycle. Recorded on PR #307, comment `7024484706`.

| finding | R4 ruling | disposition in R5 |
|---|---|---|
| NF-R3-01 nullable history provenance | `CLOSED IN SPECIFICATION` | unchanged |
| NF-R3-02 tool-call relational integrity | `OPEN — BLOCKING`, one UPDATE bypass remains | **Corrected.** `result_message_id` was absent from the frozen column list and its validation trigger is `BEFORE INSERT` only, so a valid call could be re-pointed after the fact. `tool_call_result_binding_guarded` now refuses reassignment, refuses clearing, and repeats the role/parent predicate on the single permitted `NULL → valid` transition. §7.1 |
| NF-R3-03 cross-version correction | `CLOSED IN SPECIFICATION` | unchanged |
| NF-R3-04 governance evidence inconsistency | `CLOSED` | unchanged |
| Q13 — completed call must carry a result | ruled a **separate open question**, not part of NF-R3-02 | kept separate and open; R5 does not close it, so closing it can never be read as closing NF-R3-02 |
| Q14 — does `recompute` need a single input | stricter branch **accepted provisionally**, question stays open | unchanged; §14 records it as provisional, not as a business requirement |

**This is the last engineering round.** R4's own recommendation, adopted here: one concrete correction remained, it is made, and no further full revision will be produced against open governance questions. Q1, Q11 and Q12 are not engineering defects. Another iteration cannot reach them. Q1 was subsequently reached by a decision record rather than by iteration (`DEC-P2-T2-Q1-001`, merge `d8e5bebb`); Q11 and Q12 remain unreached because the authority that could reach them is `NOT_ASSIGNED`. Q1's decision likewise did not constitute acceptance by an accountable human authority; `acceptance_authority` remains `NOT_ASSIGNED` for Q1.

The status this document supports is `BLOCKED — awaiting accountable authority assignment and governance decisions`. It does not support `APPROVE`.

---

## 2d. R5 confirmation — and what it does not say

R5 was a confirmation round, not a full revision review, at head `70a68b08`. Recorded on PR #307, comment `7024485207`.

| item | R5 ruling |
|---|---|
| NF-R3-02 residual | `CLOSED IN SPECIFICATION` |
| no-op `UPDATE OF result_message_id` semantics | `NO DEFECT FOUND` |
| new defect introduced by the R4 → R5 correction | `NONE IDENTIFIED` |
| ordinary revision cycle | `STOP` |
| R6 requested | no |

On the no-op question: SQLite fires `UPDATE OF <col>` on the column appearing in the `SET` clause, not on the value changing, so `SET result_message_id = result_message_id` does fire the guard. The predicates were reviewed against that and behave correctly across all six transition cases, including two `NULL`s being treated as no change because `IS NOT` is NULL-safe. The clearing branch is redundant with the reassignment branch; R5 rules that not a correctness defect.

**What R5 does not say:** it does not approve PR #307, and it does not close any governance question. Its explicit final determination is that the engineering correction is complete, the design is not approved, the governance blockers remain open, and the revision cycle stops.

### 2e. Two distinctions this document now carries

R5 asked for two audit-accuracy qualifications, both adopted.

**Review outcome terminology.** The recorded disposition is `REQUEST CHANGES`, but GitHub's review-submission endpoint returns no submitted review objects for this PR. Every review outcome R1–R5 is therefore a discussion record, not GitHub's formal submitted-review state. `REQUEST CHANGES` is described in this document as the *recorded independent-review disposition* and nothing more.

**Residue wording.** The phrase "engineering residue: none outstanding" would read as a statement about executability. The adopted wording is:

> No identified NF-R3-02 engineering-specification residue remains. DDL executability and regression behavior remain UNVERIFIED.

The distinctions preserved throughout:

- `CLOSED IN SPECIFICATION` is not `VERIFIED`.
- `BLOCKED` is not `APPROVED`.
- `REQUEST CHANGES` is not a governance decision.
- `NOT_ASSIGNED` cannot be filled by engineering participation.
- `NOT_GRANTED` cannot be inferred from a design review.

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

R1 ruled that escalating the authority conflict was correct, and that the binary framing in R1 was too narrow. The question is therefore restated with three answers.

**Q1 was DECIDED after this section was written, and this section is preserved as it stood rather than rewritten.** The ruling is recorded in `DEC-P2-T2-Q1-001.md` against baseline `049906a9`, merged at `d8e5bebb`: **`OPTION_C`, disposition `ACCEPT-WITH-CONDITIONS`.** The three options below are kept because the choice is only auditable if the alternatives it displaced are still visible. What that ruling closes is the architecture question and nothing else — not the DDL, not Q11–Q14, not Q8/Q9, not design acceptance, not implementation authorization.

**Option A — Phase 1 is the store; transcript capture is Event ingress only.**
No new content tables. Messages become `accepted_events` with payloads. Fewest tables, one system of record, but no message-level query model without building it on top of a generic event stream (R1: material architectural loss unless a transcript capture interface is added).

**Option B — Phase 1 is superseded for the memory path.**
The frozen domain model and Rust adapter become Phase-1-only scaffolding. Requires an explicit supersession decision, a migration off the existing tables, and re-opening the DECIDED status of `phase-1-sqlite-adapter-contract.md`. R1 found no evidence that justifies this.

**Option C — three layers, separate transcript capture (R1's recommendation).**
Phase 1 stays authoritative for canonical memory. Transcript capture becomes its own governed layer with its own retrieval contract. Derived signals become rebuildable projections with declared source dependencies.

**This proposal recommended Option C.** R1 recorded it as `PROPOSED`; a review recommendation is not an authority ruling. The choice was subsequently ruled in favour of Option C by `DEC-P2-T2-Q1-001` (§4 status above), occupying a dev-baseline Architecture Owner role held by a session. That ruling states its own limits: no human Owner signature, no appointment as `acceptance_authority`, no independent human expert review, no production-grade acceptance. `acceptance_authority` remains `NOT_ASSIGNED`. What is settled is the architecture direction; what is not settled is whether the direction has been accepted by any accountable human authority, because there is none.

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
  byte_length       INTEGER NOT NULL CHECK (byte_length >= 0),
  token_count       INTEGER,
  parent_message_id TEXT,
  edit_state        TEXT NOT NULL DEFAULT 'original'
                      CHECK (edit_state IN ('original','edited','redacted')),
  created_at        TEXT NOT NULL,
  retention_class   TEXT NOT NULL,
  UNIQUE (session_id, seq_no),
  UNIQUE (session_id, message_id),          -- target key for the composite self-reference
  FOREIGN KEY (session_id, parent_message_id)
    REFERENCES transcript_message(session_id, message_id)  -- R2-NF-01: parent in same session
);

CREATE INDEX IF NOT EXISTS transcript_message_order_idx
  ON transcript_message(session_id, seq_no);
CREATE INDEX IF NOT EXISTS transcript_message_role_idx
  ON transcript_message(session_id, role, seq_no);
CREATE INDEX IF NOT EXISTS transcript_message_thread_idx
  ON transcript_message(session_id, parent_message_id);

-- R2-NF-01: an assistant message may emit several tool calls. One row per call.
CREATE TABLE IF NOT EXISTS transcript_tool_call (
  session_id          TEXT NOT NULL,
  tool_call_id        TEXT NOT NULL,        -- provider-assigned
  call_index          INTEGER NOT NULL,     -- order within the emitting message
  emitting_message_id TEXT NOT NULL,
  result_message_id   TEXT,
  tool_name           TEXT,
  tool_state          TEXT NOT NULL DEFAULT 'emitted'
                        CHECK (tool_state IN ('emitted','completed','failed')),
  PRIMARY KEY (session_id, tool_call_id),
  UNIQUE (emitting_message_id, call_index),
  FOREIGN KEY (session_id, emitting_message_id)
    REFERENCES transcript_message(session_id, message_id),
  FOREIGN KEY (session_id, result_message_id)
    REFERENCES transcript_message(session_id, message_id)
);

CREATE INDEX IF NOT EXISTS tool_call_emitter_idx
  ON transcript_tool_call(emitting_message_id, call_index);

-- A tool result's parent MUST be an assistant message (R2-NF-01). CHECK cannot
-- express this; a trigger can.
CREATE TRIGGER IF NOT EXISTS transcript_message_tool_parent_role
BEFORE INSERT ON transcript_message
WHEN NEW.role = 'tool'
BEGIN
  SELECT RAISE(ABORT, 'tool message parent must be an assistant message')
  WHERE NOT EXISTS (
    SELECT 1 FROM transcript_message
    WHERE session_id = NEW.session_id
      AND message_id = NEW.parent_message_id
      AND role = 'assistant');
END;

-- NF-R3-02 (1): the emitter must be an assistant message.
CREATE TRIGGER IF NOT EXISTS tool_call_emitter_is_assistant
BEFORE INSERT ON transcript_tool_call
BEGIN
  SELECT RAISE(ABORT, 'tool call emitter must be an assistant message')
  WHERE NOT EXISTS (
    SELECT 1 FROM transcript_message
    WHERE session_id = NEW.session_id
      AND message_id = NEW.emitting_message_id
      AND role = 'assistant');
END;

-- NF-R3-02 (2,3): the result must be a tool message whose parent IS the emitter.
CREATE TRIGGER IF NOT EXISTS tool_call_result_is_child_tool
BEFORE INSERT ON transcript_tool_call
WHEN NEW.result_message_id IS NOT NULL
BEGIN
  SELECT RAISE(ABORT, 'tool call result must be a tool message parented by the emitter')
  WHERE NOT EXISTS (
    SELECT 1 FROM transcript_message
    WHERE session_id = NEW.session_id
      AND message_id = NEW.result_message_id
      AND role = 'tool'
      AND parent_message_id = NEW.emitting_message_id);
END;

-- NF-R3-02 (4): the guarded columns of an existing message cannot be changed
-- to bypass the two triggers above.
CREATE TRIGGER IF NOT EXISTS transcript_message_role_frozen
BEFORE UPDATE OF role, parent_message_id, session_id ON transcript_message
BEGIN
  SELECT RAISE(ABORT, 'role, parent_message_id and session_id are immutable on a captured message');
END;

-- The same for a call once recorded: emitter, index and session are frozen.
CREATE TRIGGER IF NOT EXISTS tool_call_identity_frozen
BEFORE UPDATE OF session_id, emitting_message_id, call_index, tool_call_id
  ON transcript_tool_call
BEGIN
  SELECT RAISE(ABORT, 'tool call identity is immutable; record a new call instead');
END;

-- NF-R3-02 residual (R4): result_message_id was writable, so a valid call could
-- be re-pointed at an unrelated message and the INSERT-only check never ran again.
-- Lifecycle permitted: NULL -> a valid child tool message, exactly once.
CREATE TRIGGER IF NOT EXISTS tool_call_result_binding_guarded
BEFORE UPDATE OF result_message_id ON transcript_tool_call
BEGIN
  -- (a) no reassignment once bound
  SELECT RAISE(ABORT, 'result_message_id cannot be reassigned once bound')
  WHERE OLD.result_message_id IS NOT NULL
    AND NEW.result_message_id IS NOT OLD.result_message_id;

  -- (b) unbinding is not permitted either
  SELECT RAISE(ABORT, 'result_message_id cannot be cleared once bound')
  WHERE OLD.result_message_id IS NOT NULL
    AND NEW.result_message_id IS NULL;

  -- (c) a new binding must satisfy the same role/parent rule as at INSERT
  SELECT RAISE(ABORT, 'tool call result must be a tool message parented by the emitter')
  WHERE NEW.result_message_id IS NOT NULL
    AND OLD.result_message_id IS NULL
    AND NOT EXISTS (
      SELECT 1 FROM transcript_message
      WHERE session_id = NEW.session_id
        AND message_id = NEW.result_message_id
        AND role = 'tool'
        AND parent_message_id = NEW.emitting_message_id);
END;

-- And tool_state may only advance, never regress or reopen.
CREATE TRIGGER IF NOT EXISTS tool_call_state_transition
BEFORE UPDATE OF tool_state ON transcript_tool_call
WHEN NOT (
  (OLD.tool_state = 'emitted'   AND NEW.tool_state IN ('completed','failed')) OR
  (OLD.tool_state = 'completed' AND NEW.tool_state = 'completed') OR
  (OLD.tool_state = 'failed'    AND NEW.tool_state = 'failed'))
BEGIN
  SELECT RAISE(ABORT, 'illegal tool_state transition');
END;
```

`event_row` is `NOT NULL` and references `accepted_events(event_row)`, the actual primary key in the merged Event Store. A transcript message is not a copy of the bytes — it is an index over an accepted Event. Bytes live once, in `event_payloads`. This is the R1-NB-02 correction: byte preservation was always adequate; what was missing was the retrieval structure, which is what this table supplies.

`content_sha256` is validated against `event_payloads.verified_digest` at insert. A mismatch is rejected, not repaired.

`byte_length` is stored rather than inferred. R2-NF-03 is right that concatenation alone cannot recover boundaries: a payload of `ab` followed by `c` is byte-identical to `a` followed by `bc`. Storing the length makes reconstruction unambiguous without re-parsing payload contents, and `byte_length` is cross-checked against the stored payload at insert.

`tool_call_id` is **removed** from `transcript_message`. R2-NF-01 is correct that a single column cannot represent one assistant message emitting several tool calls. The relationship now lives in `transcript_tool_call`, keyed `(session_id, tool_call_id)`, with `(emitting_message_id, call_index)` unique so the emission order inside one message is itself deterministic. Both sides of the relation are composite foreign keys on `(session_id, message_id)`, so a call and its result cannot span two sessions.

**NF-R3-02 — the call/emitter/result relation is now enforced, and R3's version was not.** R3 was right: the composite foreign keys only proved the messages existed in one session. They did not prove that the emitter was an assistant message, that the result was a tool message, that the result's parent was the emitter, or that those columns could not be changed afterwards to slip past the trigger. All four are now constrained:

1. `tool_call_emitter_is_assistant` — refuses a call whose emitter is not `role='assistant'`.
2. `tool_call_result_is_child_tool` — refuses a `result_message_id` that is not `role='tool'` **and** parented by that same emitter.
3. The same trigger carries condition 3, since `parent_message_id = NEW.emitting_message_id` is checked in the same predicate.
4. `transcript_message_role_frozen` — `role`, `parent_message_id` and `session_id` are immutable after insert, so a message cannot be re-roled into compliance afterwards. `tool_call_identity_frozen` does the same for the call row, and `tool_call_state_transition` allows `emitted → completed|failed` and forbids regression or reopening.

One honest limit: these are `BEFORE INSERT` checks plus column freezes. They enforce the relation at the moment of writing and prevent later drift through the guarded columns.

**NF-R3-02 residual, found at R4 and closed here.** R4 was right that `result_message_id` was not in the frozen column list, and that `tool_call_result_is_child_tool` is `BEFORE INSERT` only. The resulting sequence was real: insert a valid call, bind a valid result, then `UPDATE result_message_id` to an unrelated assistant message in the same session. The composite foreign key proved only that the target existed in the session, not that it was a tool message parented by the emitter.

`tool_call_result_binding_guarded` closes it with three refusals:

- reassignment once bound (`OLD` non-NULL → different `NEW`) is refused
- clearing once bound (`OLD` non-NULL → `NEW` NULL) is refused
- the one permitted transition, `NULL` → a valid result, repeats the same role-and-parent predicate as the insert check

So the permitted lifecycle is exactly what R4 asked for: initial `NULL` if asynchronous capture is intended, one transition to a valid child tool message, no reassignment, no invalid role or parent relationship.

Still open, and deliberately so: whether a call in `tool_state='completed'` must carry a non-NULL `result_message_id`. That is Q13 — lifecycle semantics, not relational integrity — and R4 ruled it must stay separate so that closing it is never mistaken for closing NF-R3-02.

### 7.2 Retrieval contract

The gap R1 identified was that ordered event retrieval is not transcript retrieval. These are the operations Layer 2 must expose. They are specified here; they are not implemented.

| operation | semantics |
|---|---|
| `read_session(session_id, after_seq, limit)` | messages ordered by `seq_no` ascending; stable, no clock dependence |
| `read_by_role(session_id, role, after_seq, limit)` | same ordering, role-filtered |
| `read_thread(message_id)` | the message plus its `parent_message_id` ancestor chain, oldest first; all rows share one `session_id` by constraint |
| `read_tool_calls(session_id, message_id)` | **all** calls emitted by one assistant message, ordered by `call_index`, each with its `result_message_id` if present |
| `read_tool_result(session_id, tool_call_id)` | the result message plus the emitting message, resolved through `transcript_tool_call` |
| `reconstruct(session_id)` | framed payload bytes, one frame per message, ordered by `seq_no` |
| `source_events(session_id)` | the `accepted_events` rows backing this session, for provenance export |

Ordering is by `seq_no`, never by `created_at`. Capture clocks are not assumed monotonic across channels.

**Reconstruction framing (R2-NF-03).** `reconstruct` does not return a bare concatenation. It returns:

```
ReconstructedTranscript {
  session_id,
  total_bytes,
  frames: [ { message_id, seq_no, role, byte_offset, byte_length, content_sha256 } ],
  buffer: [u8]           // frames[i].buffer[byte_offset .. byte_offset+byte_length]
}
```

with the invariants that `byte_offset` is the running sum of preceding `byte_length`s, that the final offset plus length equals `total_bytes`, and that every frame's slice re-hashes to its `content_sha256`. A caller can therefore cut any single message out losslessly, and a mismatch is detectable rather than silently produced.

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
  method_id             TEXT NOT NULL,
  method_version        INTEGER NOT NULL,
  algorithm             TEXT NOT NULL,     -- label, e.g. 'ebbinghaus_v1'
  algorithm_spec_ref    TEXT NOT NULL,     -- R2 A: normative spec identity, immutable
  algorithm_spec_sha256 TEXT NOT NULL,     -- R2 A: digest of that spec text
  params_json           TEXT NOT NULL,     -- the parameters themselves, not a digest
  params_sha256         TEXT NOT NULL,
  numeric_semantics     TEXT NOT NULL      -- R2 A: rounding / precision / order
                          CHECK (numeric_semantics IN ('f64_ieee754','f64_ieee754_round6','decimal_exact')),
  registered_at         TEXT NOT NULL,
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

A method version is never edited or deleted. A changed parameter set is a new `method_version`.

**R2 finding A — algorithm identity is not algorithm reproducibility.** The reviewer is right: `ebbinghaus_v1` is a label, and two implementations carrying it can differ in arithmetic, rounding, intermediate precision and evaluation order. Three columns are added so the label is no longer the whole identity:

- `algorithm_spec_ref` + `algorithm_spec_sha256` — the normative specification the label names, and its digest. A label without a retrievable spec that hashes to the recorded value cannot support the exact-value tier.
- `numeric_semantics` — a constrained vocabulary (`f64_ieee754`, `f64_ieee754_round6`, `decimal_exact`). Two implementations agreeing on spec but differing on rounding are not the same method.

This does not make the value reproducible by itself; it makes the *identity* of the computation falsifiable. The exact tier in §8.3 now requires a spec digest that matches, not merely a matching label.

### 8.2 Declared score inputs

```sql
CREATE TABLE IF NOT EXISTS score_input (
  input_id      TEXT PRIMARY KEY,
  version_id    TEXT NOT NULL REFERENCES versions(version_id),
  input_kind    TEXT NOT NULL CHECK (input_kind IN
                  ('initial','citation','decision','clock_tick','manual_adjustment')),
  source_kind   TEXT NOT NULL CHECK (source_kind IN ('event','claim','commit','operator')),
  source_ref    TEXT NOT NULL,
  weight        REAL,
  observed_at   TEXT NOT NULL,
  recorded_at   TEXT NOT NULL,
  corrects_input_id TEXT,                  -- R2 B: corrections are new rows
  UNIQUE (version_id, input_kind, source_kind, source_ref),
  UNIQUE (version_id, input_id),            -- R2-NF-02: parent key for value_history
  FOREIGN KEY (version_id, corrects_input_id)
    REFERENCES score_input(version_id, input_id)   -- NF-R3-03: same-version correction
);

CREATE INDEX IF NOT EXISTS score_input_version_idx
  ON score_input(version_id, observed_at);

-- R2-NF-04 / R2 B: append-only is enforced, not asserted.
CREATE TRIGGER IF NOT EXISTS score_input_immutable
BEFORE UPDATE ON score_input
BEGIN
  SELECT RAISE(ABORT, 'score_input is append-only; record a correction as a new row');
END;

CREATE TRIGGER IF NOT EXISTS score_input_no_delete
BEFORE DELETE ON score_input
BEGIN
  SELECT RAISE(ABORT, 'score_input is append-only; record a correction as a new row');
END;
```

Each row is an input that a score actually consumed: a citation event, a decision event, a clock tick, an operator adjustment, the initial creation. This table is the difference between "a digest points at something" and "the something is on disk".

**R2 finding B — append-only was prose, not an invariant.** Correct. Two triggers now enforce it, matching what the registry already does. A wrong historical input is corrected by inserting a new row with `corrects_input_id` pointing at the row it supersedes; the original stays, and the pair is visible. Historical mutation is refused by the database rather than by convention.

Note the honest limit: enforcement prevents *later* mutation. It does not prove the *original* set was complete. A row that was never recorded cannot be conjured, and §8.3's `unreconstructable` tier is where that shows up.

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
| **Exact value** | `value_score`, `decay_weight` and `weighted_score` are byte-identical after rebuild. | iff the `scoring_method` row exists **and its `algorithm_spec_sha256` matches a retrievable spec**, **and** `numeric_semantics` is identical, **and** the `score_input` set is unchanged (recomputed `input_set_digest` matches), **and** `evaluated_at` is supplied as recorded. **Status: CONDITIONAL — design objective, not substantiated.** See below. |
| **Unreconstructable** | Reported as `unreconstructable` with the missing dependency named. Never silently defaulted, never approximated. | the `score_input` set is incomplete, or the projection's `(method_id, method_version)` is not in the registry, or `evaluated_at` was never recorded |

A missing method row and an incomplete input set are both reachable: the composite foreign key guarantees a method row exists **at insert time**, not that the historical input set is complete. A rebuild is a read of the past, and the past can be under-recorded.

The third row is the point. A rebuild that cannot reproduce a value must say so. A rebuild that quietly substitutes a default is worse than no rebuild, because it manufactures false confidence in a derived number.

**The exact-value tier is not substantiated, and this revision does not claim it is.** R2's ruling: retain it as a conditional design objective, do not adopt a blanket `NOT CLAIMED` posture, and do not claim the complete numeric source set has been proven. R3 accepts that ruling as stated. What is now specified is the *condition under which the claim would be true* — matching spec digest, matching numeric semantics, unchanged input set, recorded evaluation clock — not the evidence that it is true. Establishing it needs a worked example: one version, one method, one recorded score, recomputed by an independent implementation and compared byte for byte. That is not in this proposal, and no test in §13 was run.

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
  history_id     TEXT PRIMARY KEY,
  version_id     TEXT NOT NULL REFERENCES versions(version_id),
  old_score      REAL,
  new_score      REAL NOT NULL,
  reason         TEXT NOT NULL CHECK (reason IN
                   ('initial','cited_by_decision','time_decay','manual_adjustment','recompute')),
  method_id      TEXT NOT NULL,
  method_version INTEGER NOT NULL,
  input_id       TEXT,
  recorded_at    TEXT NOT NULL,
  FOREIGN KEY (method_id, method_version)
    REFERENCES scoring_method(method_id, method_version),      -- R2-NF-02
  FOREIGN KEY (version_id, input_id)
    REFERENCES score_input(version_id, input_id),              -- R2-NF-02
  -- NF-R3-01: the NULL exemption is bound to the reasons that justify it.
  CHECK (
    (reason IN ('initial','time_decay')          AND input_id IS NULL)
    OR
    (reason IN ('cited_by_decision','manual_adjustment','recompute') AND input_id IS NOT NULL)
  )
);

CREATE INDEX IF NOT EXISTS value_history_version_idx
  ON version_value_history(version_id, recorded_at);
```

Two composite foreign keys close R2-NF-02 for the non-NULL case, and the `CHECK` closes the NULL case.

**NF-R3-01 — the NULL exemption is now bound to reason.** R3 was right: the composite foreign key uses SQLite's NULL semantics correctly, but nothing stopped `reason='cited_by_decision'` or `reason='manual_adjustment'` from being recorded with `input_id IS NULL`, which is exactly the provenance hole the FK was meant to close. The `CHECK` above makes the exemption reachable only for `initial` and `time_decay`.

One judgement call is recorded rather than hidden: `recompute` is constrained to require an `input_id`. The reviewer explicitly flagged that whether `recompute` genuinely must reference a single input is a business question, not something a schema proposal can settle. The constraint takes the stricter branch, and if the business answer is that a recompute may legitimately have no single input, the fix is to add `recompute` to the nullable set — a one-line change, visible in the `CHECK`, not a silent default.

Two other composite keys close the rest:

- `(method_id, method_version) → scoring_method` — a history row cannot name a method version that does not exist.
- `(version_id, input_id) → score_input` — an input cannot be claimed by a different version's history.

**NF-R3-03 — corrections are same-version.** `corrects_input_id` was a single-column reference, so a version-A input could claim to correct a version-B input and nothing refused it. It is now a composite `(version_id, corrects_input_id) → score_input(version_id, input_id)`, with `NULL` retained for rows that correct nothing. SQLite does not enforce a composite foreign key when any component is `NULL`, which is the intended behaviour for non-correction rows rather than an oversight.

The `(version_id, input_id)` parent key requires a matching unique key on `score_input`. `input_id` is already the primary key, so `(version_id, input_id)` is unique by construction; §8.2 gains `UNIQUE (version_id, input_id)` to give the constraint a real target.

```sql
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

-- This IS a modification to a Layer 1 table. It adds no column and rewrites no row,
-- but it changes the schema of `versions` and must not be described as no change.
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

**R1-NB-03 boundary, resolved explicitly (R2 required item 4).** R2 ruled this correct in technique and unresolved in boundary: an additive index is still a modification to the Layer 1 schema — not a column alteration, but not literally zero modification — and the proposal must not describe it as though it were no modification. Accepted, and the earlier wording is corrected in place.

The boundary is resolved by choosing the reading, not by asserting one:

| reading of the boundary | is `versions_memory_version_uq` allowed? | what this proposal does |
|---|---|---|
| prohibits modifying existing Layer 1 **columns and tables** | yes — no column added, no row rewritten, no `ALTER TABLE` | the design as written |
| prohibits **any** Phase 1 schema modification | no | fall back to the alternative below |

The alternative, if the stricter reading governs: drop the index and the composite foreign key, and enforce the same invariant in the adapter — read the version's owning `memory_id` and reject a mismatch inside the same transaction that inserts the context entry. That is strictly weaker, because the guarantee then lives in application code rather than in the database, and any writer bypassing the adapter can violate it. §13.8 requires the negative test either way, so the weaker path is still testable.

This proposal **recommends the index** and states plainly that it is a Layer 1 modification. Which reading controls is not mine to decide; §14 carries it as Q11 rather than as a settled fact. Describing the index as "index-only, no Layer 1 change" — as the previous revision did — was wrong.

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
    fn read_tool_calls(&self, session_id: &SessionId, message_id: &MessageId)
        -> Result<Vec<ToolCall>, Error>;
    fn read_tool_result(&self, session_id: &SessionId, tool_call_id: &str)
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
- `read_tool_calls` MUST return all calls emitted by one message in `call_index` order; there is no single-call form, because one message may emit many.
- `reconstruct` MUST return framed output, not bare bytes; a frame whose slice does not re-hash to its `content_sha256` MUST be reported as corrupt rather than returned.

---

## 12. Migration strategy

| step | action | reversibility |
|---|---|---|
| M1 | Create Layer 2 and Layer 3 tables with `IF NOT EXISTS`; add `versions_memory_version_uq` index | drop new tables and index |
| M2 | Backfill `transcript_*` from existing `accepted_events` where a session mapping is recorded | truncate; Layer 2 is not canonical |
| M3 | For each existing version, insert an `initial` `score_input` row so that scores have a declared input set | delete inserted rows |
| M4 | Register a `scoring_method` row per algorithm with its spec digest and numeric semantics; without these no projection may claim `exact` | delete inserted rows |
| M5 | Compute projections; every row starts `rebuild_state='partial'` (no historical `evaluated_at` exists for pre-migration versions) | drop projections |
| M6 | Bind vectors; `index_status='pending'` until the external index confirms | delete bindings |
| M7 | Cut over reads | revert to Phase 1 reads |

No destructive migration. No `ALTER TABLE` on Layer 1 tables. No rewrite of `versions`. One Layer 1 modification is proposed and declared as such: the additive unique index `versions_memory_version_uq` (§8.4). It adds no column and rewrites no row, but it does change the schema of a Layer 1 table, and it is listed here as a modification rather than as no change.

**Integration caveat (R2, disclosure C).** This branch is not rebased onto current main. R2 verified that the intervening commits touch `remote-worker-inventory.yaml` and the runbook pair only, none of which this proposal depends on, and ruled a forced rebase unnecessary for the design review. The branch must be updated against current main before the PR is treated as fully integrated or merged. GitHub's `mergeable` field does not substitute for that check.

Note M4 honestly: pre-migration versions cannot reach `exact` rebuild state, because their evaluation clock was never recorded. They stay `partial` permanently unless an operator supplies a reconstructed clock, which would then be an `operator` `score_input` row and visible as such.

**Schema versioning:** a `schema_migrations` table with `(version, applied_at, checksum)`, forward-only, each migration idempotent. The prompt's `schema_version` is kept in spirit with a checksum column added, because a version string alone cannot detect a partially-applied migration.

---

## 13. Test boundaries

Required before implementation authorization is granted. These are specified, not run.

1. **Vector digest binding** — `bind` rejects a `version_sha256` that does not match stored `version_json`.
2. **Scope isolation** — two scopes, identical content; each `search` returns only its own scope's versions.
3. **Invalidation is non-destructive** — `invalidate` leaves `versions` row count unchanged and sets `index_status='stale'`, `binding_epoch` incremented.
4. **Rebuild — exact tier** — with the spec digest matching, `score_input` set unchanged and `evaluated_at` supplied, drop and rebuild produces byte-identical scores and a matching `input_set_digest`.
5. **Rebuild — unreconstructable tier** — delete `score_input` rows for a version (simulating an under-recorded history), run rebuild, assert `rebuild_state='unreconstructable'` with the missing dependency named, and assert no `value_score` was written.
6. **Rebuild — partial tier on migration** — pre-migration versions rebuild to `partial`, never `exact`, and never silently to `exact`.
7. **Method immutability** — `UPDATE` and `DELETE` on `scoring_method` both abort.
8. **Composite integrity** — insert a `context_assembly_entry` with a `version_id` belonging to a different `memory_id`; assert refused.
9. **No cascade destruction** — delete a `transcript_session` that has messages; assert refused. Then delete a `transcript_message` that has a `memory_source_link`; assert refused.
10. **Canonical row counts** — closing and retiring sessions leaves `memories` and `versions` row counts unchanged.
11. **Transcript ordering** — insert messages out of `created_at` order with valid `seq_no`; assert `read_session` returns `seq_no` order.
12. **Tool-call cardinality (R2-NF-01)** — one assistant message emits three tool calls with distinct `tool_call_id` and `call_index` 1..3; assert `read_tool_calls` returns all three in order, and that inserting a fourth with duplicate `call_index` is refused.
13. **Tool-call thread integrity (R2-NF-01)** — assert a `tool` message whose parent is a `user` message is refused by the trigger, and that a `transcript_tool_call` referencing a `result_message_id` in a different `session_id` is refused by the composite foreign key.
14. **Reconstruction framing (R2-NF-03)** — reconstruct a session of three messages and assert `frames[i].byte_offset` is the running sum of preceding `byte_length`s, that the last offset plus length equals `total_bytes`, and that each frame slice re-hashes to its `content_sha256`. Include a boundary case where two adjacent payloads would be ambiguous under naive concatenation (`"ab"` then `"c"` versus `"a"` then `"bc"`).
15. **History provenance (R2-NF-02)** — assert a `version_value_history` row naming an unregistered `(method_id, method_version)` is refused, and one naming an `input_id` belonging to a different `version_id` is refused.
16. **Score-input immutability (R2-NF-04)** — `UPDATE` and `DELETE` on `score_input` both abort; a correction inserted with `corrects_input_id` succeeds and leaves the corrected row intact.
17. **Nullable history provenance (NF-R3-01)** — a `version_value_history` row with `reason='cited_by_decision'` and `input_id IS NULL` is refused; the same row with `input_id` set is accepted; `reason='initial'` with `input_id IS NULL` is accepted.
18. **Cross-version correction (NF-R3-03)** — a `score_input` row for version A with `corrects_input_id` pointing at an input of version B is refused.
19. **Tool-call relational integrity (NF-R3-02)** — assert all four refusals: a call whose emitter is a `user` message; a call whose `result_message_id` is an assistant message; a call whose result is a `tool` message parented by a *different* assistant message; and an `UPDATE` that re-roles a captured message or re-points its `parent_message_id`.
20. **Tool-state transitions (NF-R3-02)** — `emitted → completed` accepted; `completed → emitted` refused; `failed → completed` refused.
21. **Result rebinding (NF-R3-02 residual)** — bind a valid result, then attempt `UPDATE result_message_id` to (a) an unrelated assistant message in the same session, (b) a tool message parented by a *different* assistant, (c) NULL. All three refused. Then assert the one permitted transition `NULL → valid child tool message` succeeds exactly once.

Tests 4–7 and 16 are the regression guards for R1-B-01. Tests 9–10 guard R1-NB-04. Test 8 guards R1-NB-03. Tests 11–14 guard R1-NB-02 / R2-NF-01 / R2-NF-03. Test 15 guards R2-NF-02. Tests 17–20 guard NF-R3-01 / NF-R3-02 / NF-R3-03. Test 21 guards the NF-R3-02 residual found at R4.

These tests were not written and not run. Neither the R2 nor the R3 DDL was executed — see §17.

---

## 14. Open questions

| id | question | status |
|---|---|---|
| Q1 | Option A vs B vs C — which architecture | **DECIDED as `OPTION_C` / `ACCEPT-WITH-CONDITIONS`**, recorded in `DEC-P2-T2-Q1-001.md` against baseline `049906a9` (merge `d8e5bebb`). Ruling capacity: dev-baseline Architecture Owner role, session-held — not an accountable human authority, and `acceptance_authority` remains `NOT_ASSIGNED`. Closes the architecture question only. |
| Q2 | Extract Claim/Entity/Relation to tables, or keep in `version_json`? | OPEN, defer to P2-T3 |
| Q3 | Vector store: Qdrant vs Chroma. Prompt defaults Chroma; Phase 1 has neither. | OPEN |
| Q4 | Embedding model and dimension. Prompt assumes `text-embedding-3-small` / 1536. | OPEN — external dependency |
| Q5 | Decay and scoring algorithms and parameters, and recompute cadence | OPEN — required before any score can reach `exact` |
| Q6 | Is `version_sha256` maintained by trigger or by adapter? | OPEN — adapter is the current assumption |
| Q7 | Stale-binding recovery procedure, including external index rebuild after an outage | OPEN |
| Q8 | Transcript retention classes and their default periods | OPEN — this proposal constrains deletion, it does not define the policy |
| Q9 | Whether `impact_level` should get a typed home or be dropped | OPEN |
| Q10 | Does numeric reproducibility stay a requirement, or is structural rebuild sufficient? | **REVIEW RULING (R2): tiered preferred.** Structural and unreconstructable tiers accepted; exact-value retained as a design objective, **CONDITIONAL and NOT VERIFIED**. This is a review ruling on a review question, not an owner decision on Q1. |
| Q11 | Does the Layer 1 boundary prohibit modifying Layer 1 tables, or only their columns? | **OPEN — controls whether `versions_memory_version_uq` is admissible at all.** §8.4 states both branches and the fallback. Not mine to decide. |
| Q12 | Is the in-memory DDL check an acceptable reading of the `no schema execution` bound? | **OPEN — requires the authority that issued the bound.** R2 classified it `DISCLOSED SCOPE DEVIATION`, not authorized activity, and stated an engineering reviewer cannot grant retrospective authorization. `acceptance_authority` is `NOT_ASSIGNED`; no session can supply this. |
| Q13 | Must a `tool_state='completed'` call carry a non-NULL `result_message_id`? | OPEN — lifecycle semantics, not relational integrity. R4 ruled it must stay separate so that resolving it is never mistaken for closing NF-R3-02. |
| Q14 | Does `recompute` genuinely require a single `input_id`? | OPEN — the `CHECK` in §8.4 takes the stricter branch; R4 accepted that as a provisional choice while keeping the business question open. If a recompute may legitimately have no single input, `recompute` moves to the nullable set. |

---

## 15. What this proposal does not claim

- Not implemented. No code, no migration, no test executed.
- Not a frozen schema. It is a proposal for review.
- Not an authorization for P2-T1. Implementation authorization remains withheld per `GO-2026-P2-DESIGN-001`.
- **Not a resolution of Q1 by an accountable authority.** The architecture direction was decided as `OPTION_C` by `DEC-P2-T2-Q1-001`, occupying a dev-baseline Architecture Owner role held by a session. That ruling claims no human signature, no `acceptance_authority` appointment, and no production-grade acceptance. What is settled is the direction; what remains unsettled is whether any accountable human authority has accepted it, because there is none.
- **Not a substantiated exact-value rebuild.** The conditions are specified; the evidence is not. Q10 is recorded as ruled for a tiered posture, with exact value `CONDITIONAL` and `NOT VERIFIED`.
- **Not authorized schema execution.** The one in-memory DDL check is recorded as `DISCLOSED SCOPE DEVIATION`, not as compliant activity; Q12 escalates the authority question.
- **Not a verified fix for NF-R3-01 / NF-R3-02.** The constraints are specified. Neither the R3 nor the R4 DDL was executed, so what is asserted is that the constraint text exists and matches the prose — not that SQLite enforces it as intended.
- **Not authenticated prompt provenance.** Appendix A is a copy; its origin is `UNVERIFIED`.
- No technology selection: Qdrant/Chroma, embedding model and dimension remain OPEN.
- No claim that the prompt schema is unusable. Its tensions are real; its contradictions with Phase 1 are not established as necessary.
- No claim of approval by any accountable authority. `acceptance_authority` is `NOT_ASSIGNED`.
- No claim that the R3 DDL applies — it was not executed. §17's probe result is evidence about the R2 DDL only.

---

## 16. Evidence tier

| item | tier |
|---|---|
| Phase 1 DECIDED status, merged commits, observed table definitions | **VERIFIED** — read at base `7f8093876729212ef4e83461ba8c2f2cd96582c7`; `core-entities.md` blob `8cb5a674`, `phase-1-sqlite-adapter-contract.md` blob `c472e00f`, `phase-1-storage-trait-contract.md` blob `22ca7cd3`, `payload.rs` blob `ad22972b`. R1 independently confirmed the same tables. |
| Trait contract status | **VERIFIED** — the file states `CANDIDATE`; this document relies only on the narrower SQLite-boundary claim |
| Prompt schema contents | **VERIFIED as embedded text at this document's head** — reproduced in Appendix A. Its **original-source verbatim provenance is UNVERIFIED**: R2 independently fetched the repository path at the reviewed head and got `404`, so an appendix is reviewable evidence but cannot authenticate its own origin. R2's ruling accepted the appendix as a valid self-containment remedy and withheld the `VERIFIED` upgrade. That limit is not contested here. The remedy, if independent authentication is required, is to commit the prompt file at a known commit — which needs a write path this manifest does not contain. |
| §5 tensions | **CORROBORATED, author assessment** — R1 ruled the stronger form `OVERSTATED`; the downgraded form is retained as tension, not contradiction |
| R1 findings and dispositions | **VERIFIED** — transcribed from the R1 reply, recorded on PR #307 |
| Recommendations in §6–§12 | **PROPOSED** — author-authored, subject to R2 review |
| Q1 decision, disposition and the merge that recorded it | **VERIFIED** — `DEC-P2-T2-Q1-001.md` and merge `d8e5bebb` are on `main` and readable. |
| Any claim that Q1 was resolved by an accountable human authority | **NOT MADE** — the ruling occupies a session-held dev-baseline role and says so itself; `acceptance_authority` is `NOT_ASSIGNED`. |

---

## 17. Disclosed scope deviation — in-memory DDL check

**R2 classified this as `DISCLOSED SCOPE DEVIATION`, not authorized activity.** That ruling is accepted without argument. This section does not defend the check; it records it, records what it found, and escalates the authority question.

What was done: the DDL in §7 and §8 was executed against an ephemeral in-memory SQLite database (`sqlite3` 3.53.1), preceded by `CREATE TABLE` statements copied from the merged Phase 1 crates so that foreign keys resolve against the real key shapes. Nothing was written to disk, no migration was applied, no repository artefact was created or changed.

Why it was done: to find out whether the document is internally coherent before spending a review round on it.

Why that reason does not make it authorized: `authorization-manifest.yaml` records `no schema execution` among the design-only bounds, and an in-memory database is still a database against which schema execution occurred. The earlier revision advanced the reading that the bound covers persistent stores and repository paths. R2 declined to accept that reading as established by the authorization text, and an engineering reviewer cannot grant retrospective authorization. Both points stand.

The manifest's formal classification of this event is `DISCLOSED_SCOPE_DEVIATION`. **Correction (NF-R3-04):** an earlier revision of this section stated that the manifest records the event as `DISCLOSED_INTERPRETATION`. That was wrong — the manifest was updated to `DISCLOSED_SCOPE_DEVIATION` and this paragraph was not updated with it. The reviewer is right that an audit trail must not give one event two classifications. `DISCLOSED_SCOPE_DEVIATION` is the single recorded status, here and in the manifest, and the question is carried as **Q12**.

What it found, reported as author-reported and not independently reproduced:

- All design DDL blocks apply against the real Phase 1 key shapes.
- Constraint probes behaved as specified: the composite `(memory_id, version_id)` foreign key refuses a mismatched pair; deleting a `transcript_session` that has messages is refused; deleting a `transcript_message` carrying a `memory_source_link` is refused; `UPDATE` and `DELETE` on `scoring_method` are refused; a projection referencing an unregistered `(method_id, method_version)` is refused.
- One real defect, found before review: the first draft of `transcript_message` referenced `accepted_events(event_id)`, and the merged Event Store's primary key is `event_row INTEGER`. The draft would not have compiled. §7.1 now uses `event_row`.

In R3 this check was **not** repeated. The tables changed, so the earlier result does not carry forward as evidence about the current DDL; it is evidence about the R2 DDL only. Whether the R3 DDL applies is an open question for an authorized implementation phase, not something this revision asserts. The prior probes are `AUTHOR-REPORTED`, and R2 declined to upgrade them, which is the correct tier.

What this does not establish:

- Not an implementation. There is no code beyond the document.
- Not a test suite. None of §13's tests were written or run; the ad-hoc probes are not those tests. (The count is stated once, in §13, and is not repeated here — an earlier revision said "thirteen" while §13 listed sixteen, which NF-R3-04 correctly flagged.)
- Not evidence about performance, concurrency, WAL behaviour, or behaviour under the Phase 1 adapter's transaction discipline.
- Not evidence that the R3 DDL applies at all — the R3 tables were not exercised.
- Not evidence that the design satisfies any capability in §9.

---

## Appendix A — prompt schema DDL, embedded copy

**Provenance limit, stated up front.** This appendix is a copy. It is reviewable as text, and it is what R1-NB-05 asked for, but it cannot authenticate its own origin: the source path `prompts-fix/P2-T2-memory-schema.md` is not present in the repository at any reviewed head, and both R1 and R2 independently received `404` for it. R2 therefore accepted the appendix as a self-containment remedy while withholding the `VERIFIED` upgrade, and that tier stands uncontested.

Anyone who needs authenticated provenance must obtain the source file at a known commit — which requires a write path beyond this manifest's two allowed files — or compare this appendix against their own copy.

The copy below is exact as supplied in this session. It is evidence, not adopted design: where it conflicts with §7–§8, §7–§8 govern.

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
