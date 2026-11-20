# P2-T1 implementation gates — conformance map

**Work item:** P2-T2 (Phase 2 Task 2)
**Purpose:** map each gate in `DEC-P2-T2-Q1-001` §8 to the part of this work item that addresses it, and name what is missing.
**Status:** derived artefact. Introduces no new design, closes no open question, grants no authorisation.

---

## 1. Why this document exists

`DEC-P2-T2-Q1-001` §8 lists seven gates between the Option C decision and P2-T1 implementation authorisation, and ends: *"Until these gates are satisfied, P2-T1 remains `BLOCKED` for implementation authorisation."*

The Q1 ruling recorded in §2f further directed that **gates 1, 2, 3 and 5** be treated as bounded engineering work. Gates 4, 6 and 7 involve authorities or decisions this work item cannot supply.

That instruction is only actionable if it is clear, gate by gate, what already addresses it and what does not. This document supplies that map. It is a reading of existing material, not an addition to it.

---

## 2. Gate 1 — canonical persistence boundary

> Specify how P2-T1 writes canonical memories and versions through the Phase 1 boundary, preserving immutable versions, CAS and atomic pointer advancement.

| addressed by | how |
|---|---|
| `02-domain-model/phase-1-sqlite-adapter-contract.md` | DECIDED. Enumerates the persistence behaviours P2-T1 must use: immutable version rows, current-version CAS, idempotency receipts, monotonic commit sequence, atomic transaction. |
| `crates/memory-storage/src/lib.rs` — `MemoryStorage` | The trait P2-T1 writes through. `commit_version(CommitRequest, &[ScopeRef])` with `expected_current_version` is the CAS. `CommitRequest` carries `memory_id`, `expected_current_version`, `new_version`, `idempotency_key`, `request_digest`. |
| `crates/memory-storage-sqlite/src/lib.rs` | The implemented adapter. `commit_version`, `read_current`, `read_version`, `resolve_idempotency`, `list_changes`. Four tables: `memories`, `versions`, `idempotency`, `commit_log`. |
| design-proposal §11 | States Phase 2 must **not** change the `MemoryStorage` trait; additions are separate traits. |
| design-proposal §8.4 / §12 | Declares the one proposed Layer 1 modification, the additive unique index `versions_memory_version_uq`, and the Q11 dependency. |

**Residual gap.** §11 forbids changing `MemoryStorage` and lists the new traits, but does not state which Phase 1 call P2-T1 makes *first* in each canonical write path, nor the ordering guarantee between `commit_version` and the transcript-capture write that cites it. That ordering is a design decision for P2-T1's own contract, not something this proposal can fix by assumption.

**Blocked by:** nothing at design level. This is gate-1 engineering work that P2-T1 itself performs.

---

## 3. Gate 2 — transcript capture contract

> Event ingestion, ordering, role filtering, thread reconstruction, tool-call pairing, idempotency, provenance, lifecycle. It must be independently retrievable without treating the transcript as canonical memory.

| addressed by | how |
|---|---|
| design-proposal §7.1 | `transcript_session`, `transcript_message`, `transcript_tool_call`, `memory_source_link`. Ordering by `seq_no`, never `created_at`. Bytes stay in `event_payloads`; the transcript row is an index over `accepted_events(event_row)`. |
| design-proposal §7.2 | The six retrieval operations: `read_session`, `read_by_role`, `read_thread`, `read_tool_calls`, `read_tool_result`, `reconstruct`. |
| design-proposal §11 | `TranscriptCapture` trait with those six methods, plus invariants on framing and tool-call cardinality. |
| design-proposal §13 tests 9–14, 19–21 | Ordering, cardinality, thread integrity, framing, no-cascade, tool-state transitions, result rebinding. |
| `crates/memory-event-store-sqlite/src/payload.rs` | `PayloadEventStoreExt::accept_with_payload` and `read_after(after_sequence, limit, scope)`. The ingestion and ordered-read primitives the capture layer builds on. |

**Residual gap.** *Lifecycle* is the weakest column. The proposal constrains transitions (`tool_state`, `edit_state`) and deletion, but does not define the session lifecycle transitions themselves — what states a `transcript_session` passes through, who may close it, and whether closure is reversible. Retention classes are likewise constrained but not defined (Q8).

**Blocked by:** Q8 for retention periods and classes. Session lifecycle states are not Q8 and are not supplied here.

---

## 4. Gate 3 — derived projection semantics

> Source dependencies, projection versions, rebuild behaviour, stale-data handling, failure recovery. Qdrant must not silently become an alternative canonical system of record.

| addressed by | how |
|---|---|
| design-proposal §8.1 | `scoring_method` with `algorithm_spec_ref`, `algorithm_spec_sha256`, `numeric_semantics`; append-only by trigger. |
| design-proposal §8.2 | `score_input` — the declared input set — with `UNIQUE (version_id, input_id)` and append-only triggers; corrections inserted with `corrects_input_id`. |
| design-proposal §8.3 | Three rebuild tiers: `structural`, `exact`, `unreconstructable`. Exact is conditional and recorded `NOT VERIFIED`. |
| design-proposal §8.4 | `version_value_history`, `context_assembly_entry` with composite FKs, `version_vector_binding`. |
| design-proposal §11 | `MemoryValueProjection` and `VectorIndex` traits, with the invariant that `invalidate` must not delete canonical content. |
| design-proposal §13 tests 1–8, 15–18 | Digest binding, scope isolation, non-destructive invalidation, all three rebuild tiers, immutability, composite integrity, provenance. |

**Residual gap.** *Failure recovery* is named in the gate and only partly addressed. §12 gives a forward-only idempotent migration path; it does not state what a rebuild does when it is interrupted partway, whether `rebuild_state` is set before or after the score row is written, or how a partial rebuild is distinguished from an interrupted one. Q10 records that exact-value rebuild remains `CONDITIONAL` / `NOT VERIFIED`.

**Blocked by:** nothing at design level for the structural tier. Exact-value tier needs a worked example that does not exist here.

---

## 5. Gate 4 — resolve applicable outstanding decisions

> Q11–Q14 through their appropriate authorities. Q12 in particular cannot be closed by this record's assumption.

**Not addressed, and not addressable here.** Current state, from §14:

| question | state | needs |
|---|---|---|
| Q11 | RE-POSED, OPEN | the capacity owning the Phase 1 contract — not identified |
| Q12 | PROSPECTIVE YES, RETROSPECTIVE NO | the bound-owning capacity — `NOT_ASSIGNED` |
| Q13 | `RECOMMENDED`, adapter-level | formal adoption by an appropriate authority |
| Q14 | `BUSINESS_RULE_NOT_SUPPLIED` | the owner of `recompute`'s semantics |
| Q8 | `POLICY_INPUT_ABSENT` | retention policy |
| Q9 | `SEMANTIC_DECISION_REQUIRED` | authoritative determination on `impact_level` |

No engineering act closes any of these. Issue #305 records the root cause: no governance act has established who may hold `acceptance_authority`, and `00-governance/reports/bilingual-baseline-remediation-report.md` line 931 already records the same finding as `OUT-OF-SCOPE(dev-baseline)` rather than simulating it.

---

## 6. Gate 5 — implementation acceptance criteria and tests

> Duplicate event delivery, out-of-order delivery, partial failure, restart/recovery, concurrent updates, projection rebuilding, provenance integrity, context-injection correctness.

Phase 1 already carries executable tests for several of these criteria. They are **not** Phase 2 tests and were not written against the Layer 2 or Layer 3 schema, but they establish that the underlying store behaves correctly under exactly the conditions this gate names. Counting them as absent would have been wrong; counting them as satisfying the gate would also be wrong.

| criterion | Phase 1 evidence (exists, executable) | Phase 2 status |
|---|---|---|
| duplicate event delivery | `memory-event-store-sqlite/src/payload.rs:285` — `duplicate_payload_append_returns_original_receipt_without_dup`; `lib.rs:324` — `same_producer_key_and_digest_replay_original_receipt`; `lib.rs:339` — `same_producer_key_with_different_digest_conflicts` | not specified at transcript layer |
| out-of-order delivery | `memory-storage-sqlite/src/lib.rs:1511` — change pages preserve order without skips or duplicates | covered — §7.1 `seq_no`, test 11 |
| partial failure | **none** | **not covered** |
| restart/recovery | `resilience.rs:139` — `restart_preserves_receipt_and_idempotent_payload_replay`; `resilience.rs:204` — `committed_payload_survives_process_crash_and_wal_recovery`; `memory-storage-sqlite/src/lib.rs:496` — `sqlite_committed_state_survives_close_and_reopen`; `:554` — `abrupt_process_exit_rolls_back_entire_uncommitted_commit` | not specified at transcript layer |
| concurrent updates | `resilience.rs:162` — `concurrent_appends_preserve_unique_order_and_payload_custody` (6 writers, barrier-synchronised); `memory-storage-sqlite/src/lib.rs:579` — `independent_connections_serialize_competing_compare_and_swap_writers` | not specified at transcript layer |
| projection rebuilding | **none** | covered — tests 4–6 |
| provenance integrity | **none** | covered — tests 15, 17, 18 |
| context-injection correctness | **none** | **not covered** |

### Correction to a first reading of this gate

A first draft of this document stated that four of eight criteria were unaddressed. That was wrong, and wrong in a specific way worth recording: it was written from the Phase 2 proposal alone, without checking whether Phase 1 already carried the evidence. Three of the four claimed gaps — duplicate delivery, restart/recovery, concurrent updates — have executable Phase 1 tests behind them.

The corrected reading is narrower:

- **One genuine gap: partial failure.** No test anywhere in the tree asserts behaviour on a half-applied transcript insert. Phase 1's crash tests prove atomic rollback of an *uncommitted* commit; they do not cover a commit that succeeded while the transcript row citing it did not.
- **One genuine gap: context-injection correctness.** `context_assembly_entry` exists with composite FKs and test 8, but nothing asserts that the injected context is the one the assembly intended. That needs a definition of "intended" before a test can exist.
- **Three criteria have Phase 1 evidence but no Phase 2 test.** Duplicate delivery, restart/recovery and concurrent updates work at the store layer; whether they still hold once a transcript row must be written alongside is untested and unspecified.

That third category is the substantive work, not the first two. It is not a matter of writing a test — it is a matter of deciding what the transcript write does when the canonical commit has already succeeded.

None of this is blocked on authority. All of it is blocked on work not done.

---

## 7. Gate 6 — separate P2-T1 implementation authorisation

Not obtainable here. The authorisation requires an implementation Owner accepting the target contract, scope, test obligations and failure boundaries against an exact artefact version. `accountable_owner` and `acceptance_authority` are `NOT_ASSIGNED`; Issue #305 records why, and the remedy is a governance act this work item cannot perform.

---

## 8. Gate 7 — normal convergence chain

Partially available. Implementation, verification, review and merge are executable. **Owner acceptance** within that chain is not, for the same reason as gate 6.

---

## 9. Summary

| gate | design coverage | blocked by |
|---|---|---|
| 1 canonical persistence | substantial; write-path ordering unspecified | nothing at design level |
| 2 transcript capture | substantial; session lifecycle and retention undefined | Q8 for retention; lifecycle states not supplied |
| 3 derived projection | substantial; failure recovery and interruption semantics missing | nothing for structural tier; exact tier `NOT VERIFIED` |
| 4 outstanding decisions | **none** | authority — Issue #305 |
| 5 acceptance criteria and tests | Phase 1 evidence for 3 of 8 criteria; 2 genuine gaps; 3 criteria untested at Phase 2 | work not done, not authority |
| 6 implementation authorisation | none | authority — Issue #305 |
| 7 convergence chain | partial | Owner acceptance unavailable |

The gates that can be advanced by engineering are 1, 2, 3 and 5, which is what the Q1 ruling said. Of those, the substantive gap is the interaction between gates 1 and 5: three gate-5 criteria are proven at the store layer and unproven once a transcript write must accompany a canonical commit. That question — what happens when `commit_version` succeeds and the `transcript_message` insert does not — is a design question with no answer in this work item, and it needs no authority to answer.

Second substantive gap, gate 2: session lifecycle states. Retention periods are Q8 and blocked; the states themselves are not, and are simply unwritten.

---

## 10. What this document does not claim

- Not that any gate is satisfied. It maps coverage and names gaps.
- Not that the design is adequate. Coverage is not correctness; none of the 21 tests were written or run.
- Not that the residual gaps are the only gaps. They are the ones visible against the gate text.
- Not a substitute for the review rounds recorded in §2–§2f. Those examined the document; this examines its relation to a list written elsewhere.
- No governance state changes. `DESIGN_ACCEPTANCE` `NOT_GRANTED`, `IMPLEMENTATION_AUTHORIZATION` `NOT_GRANTED`, `GOVERNANCE_STATUS` `BLOCKED`, `acceptance_authority` `NOT_ASSIGNED`.

**Evidence tier:** the gate text and the cited sections are `VERIFIED` — read from the merged tree. The judgement that a section "addresses" a gate is `PROPOSED` — an author reading, not a review finding.
