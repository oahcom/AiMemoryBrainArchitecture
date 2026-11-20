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

**Residual gap.** The *state vocabulary* exists — `design-proposal.md:433` defines `session_state TEXT NOT NULL CHECK (session_state IN ('open','closed','abandoned'))`. What is missing is the lifecycle **contract**: which transitions are permitted, who or what may close a session, whether `closed` and `abandoned` are terminal, how `ended_at` must correspond to `session_state`, and whether messages may still be captured after closure. Retention periods and classes are separately absent (Q8).

**Blocked by:** Q8 for retention. The transition and ownership semantics are not Q8 and are simply unwritten — but see §9 on who may adopt them.

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

**Residual gap (tier 3).** *Failure recovery* is named in the gate and only partly addressed. §12 gives a forward-only idempotent migration path; it does not state what a rebuild does when it is interrupted partway, whether `rebuild_state` is set before or after the score row is written, or how a partial rebuild is distinguished from an interrupted one. Q10 records that exact-value rebuild remains `CONDITIONAL` / `NOT VERIFIED`.

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
| duplicate event delivery | `memory-event-store-sqlite/src/payload.rs:285` — `duplicate_payload_append_returns_original_receipt_without_dup`; `lib.rs:324` — `same_producer_key_and_digest_replay_original_receipt`; `lib.rs:339` — `same_producer_key_with_different_digest_conflicts` | `PROVEN — PHASE 1 STORE LAYER`; `UNPROVEN — PHASE 2 INTEGRATION` |
| out-of-order delivery | **none** — the change-page test at `memory-storage-sqlite/src/lib.rs:1511` asserts ordered *retrieval* with limit and scope filtering, which is not delivery order | retrieval ordering specified (test 11); out-of-order **arrival** handling `UNVERIFIED ABSENCE` |
| partial failure | **none** | `UNVERIFIED ABSENCE` |
| restart/recovery | `resilience.rs:139` — `restart_preserves_receipt_and_idempotent_payload_replay`; `resilience.rs:204` — `committed_payload_survives_process_crash_and_wal_recovery`; `memory-storage-sqlite/src/lib.rs:496` — `sqlite_committed_state_survives_close_and_reopen`; `:554` — `abrupt_process_exit_rolls_back_entire_uncommitted_commit` | `PROVEN — PHASE 1 STORE LAYER`; `UNPROVEN — PHASE 2 INTEGRATION` |
| concurrent updates | `resilience.rs:162` — `concurrent_appends_preserve_unique_order_and_payload_custody` (6 writers, barrier-synchronised); `memory-storage-sqlite/src/lib.rs:579` — `independent_connections_serialize_competing_compare_and_swap_writers` | `PROVEN — PHASE 1 STORE LAYER`; `UNPROVEN — PHASE 2 INTEGRATION` |
| projection rebuilding | **none** | specified, not implemented or run |
| provenance integrity | **none** | specified, not implemented or run |
| context-injection correctness | **none** | `UNVERIFIED ABSENCE`; intended-context semantics undefined |

### Two corrections of this document's own earlier readings

**First correction — the gap count.** A first draft said four of eight criteria were unaddressed. That was written from the Phase 2 proposal alone, without checking the tree. Three of the four claimed gaps — duplicate delivery, restart/recovery, concurrent updates — have executable Phase 1 tests behind them.

**Second correction — the overcorrection.** The response to the first correction then classified out-of-order delivery as covered, citing test 11. It is not covered. Test 11 asserts that `read_session` returns `seq_no` order *after* sequence numbers have been assigned; that is retrieval ordering, not how the capture layer handles events arriving in a different order from their intended sequence. The Phase 1 change-page test at `:1511` is also ordered retrieval with limit and scope filtering. No test in the inspected tree asserts delivery-order handling.

So the honest classification has three tiers, not two:

| tier | classification | meaning |
|---|---|---|
| 1 | `PROVEN — PHASE 1 STORE LAYER` | positive evidence establishes the specifically tested store behaviour |
| 2 | `UNPROVEN — PHASE 2 INTEGRATION` | store-level evidence exists; Phase 2 integration behaviour not established |
| 3 | `UNVERIFIED ABSENCE` | no relevant test located in the inspected tree; exhaustive absence not established |

**Tiers 1 and 2 are not competing classifications.** A behaviour can be proven at the store layer and simultaneously unproven at Phase 2, and the mapping keeps both visible rather than letting one stand for the other. A store-level idempotency test does not establish end-to-end idempotency once Phase 2 introduces its own commit, retry and transcript interactions.

Applying it:

- **Tier 1 + 2 together** — duplicate delivery, restart/recovery, concurrent updates. The Phase 1 tests exist and run and prove the tested store operation. None of them involves a transcript write accompanying a canonical commit, so none establishes the Phase 2 path that did not exist when they were written.
- **Specified, not implemented, not run** — projection rebuilding, provenance integrity, retrieval ordering.
- **Tier 3** — partial failure, out-of-order *arrival*, context-injection correctness. No test evidence was located. That is not the same as saying those behaviours are untested; it says their coverage status has not been established.

The substantive work is tier 1+2's open question: what happens when `commit_version` succeeds and the `transcript_message` insert citing it does not. That is a design question, and per §10 it is not one engineering may settle unilaterally.

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
| 2 transcript capture | substantial; state vocabulary exists, transition and ownership semantics undefined | Q8 for retention; transitions need adoption (§10) |
| 3 derived projection | substantial; failure recovery and interruption semantics missing | nothing for structural tier; exact tier `NOT VERIFIED` |
| 4 outstanding decisions | **none** | authority — Issue #305 |
| 5 acceptance criteria and tests | 3 `PROVEN — PHASE 1 STORE LAYER` / `UNPROVEN — PHASE 2 INTEGRATION`; 3 specified but unrun; 3 `UNVERIFIED ABSENCE` | work not done; adoption authority for the atomicity contract |
| 6 implementation authorisation | none | authority — Issue #305 |
| 7 convergence chain | partial | Owner acceptance unavailable |

The gates that can be advanced by engineering are 1, 2, 3 and 5, which is what the Q1 ruling said. Of those, the substantive gap is the interaction between gates 1 and 5: three gate-5 criteria are proven at the store layer and unproven once a transcript write must accompany a canonical commit.

Second substantive gap, gate 2: session lifecycle transitions. The state vocabulary exists; the transition and ownership semantics do not.

---

## 10. What engineering may start without authority, and what it may not adopt

The Q1 ruling directed that gates 1, 2, 3 and 5 be treated as bounded engineering work. That authorises investigation. It does not confer authority to settle every normative design choice arising from the investigation, and this document does not claim otherwise.

The distinction, stated plainly:

| act | may a session do it? |
|---|---|
| identify failure modes in the commit/transcript interaction | yes |
| investigate transaction boundaries; produce several candidate contracts | yes |
| test the candidates; recommend one | yes |
| declare which consistency and recovery contract is **binding** | no — a design decision, not a test-writing exercise |
| propose a session state machine | yes |
| adopt it as the authoritative lifecycle rule | no — it would silently become a business rule |

Applied to the two gaps this document identifies:

- **The atomicity question** — what happens when `commit_version` succeeds and the `transcript_message` insert does not — can be investigated and specified in alternatives. Selecting which alternative governs needs an authority that is `NOT_ASSIGNED`. A session cannot close that question by writing a document.
- **Session lifecycle transitions** — the state machine can be proposed. Adopting it as authoritative has the same problem.

So the accurate statement is not "none of this is blocked on authority". It is: **the investigation is not blocked; the adoption is.** A session can move these questions from "unasked" to "asked with named alternatives". It cannot move them to "settled".

That is still worth doing, and it is why this map separates *work not done* from *decision not available*. The first column is large. The second is not empty.

---

## 11. What this document does not claim

- Not that any gate is satisfied. It maps coverage and names gaps.
- Not that the design is adequate. Coverage is not correctness; none of the 21 tests were written or run.
- Not that the residual gaps are the only gaps. They are the ones visible against the gate text in the inspected tree.
- Not a complete search. The citations were verified by script — ten positive matches, zero failures — but verifying that ten citations exist says nothing about whether other relevant tests exist elsewhere. Absence claims here read "no existing test identified in the inspected tree", not "no test exists".
- Not an authority to adopt. See §10.
- Not a substitute for the review rounds recorded in §2–§2f. Those examined the document; this examines its relation to a list written elsewhere.
- No governance state changes. `DESIGN_ACCEPTANCE` `NOT_GRANTED`, `IMPLEMENTATION_AUTHORIZATION` `NOT_GRANTED`, `GOVERNANCE_STATUS` `BLOCKED`, `acceptance_authority` `NOT_ASSIGNED`.

**Evidence tier:** the gate text and the cited sections are `VERIFIED` — read from the merged tree, citations script-checked. The judgement that a section "addresses" a gate is `PROPOSED` — an author reading, not a review finding. The absence of tests for partial failure, out-of-order arrival and context-injection correctness is `UNVERIFIED ABSENCE` in the tiered sense defined in §6 — no relevant test was located in the inspected tree, and exhaustive absence was not established. The distinction between that and *the behaviour is untested* is the whole point of the tier.
