# GAP-BASELINE-001 — Key Missing Workload Baseline

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Frozen at: **2026-11-21 15:00 +08:00**
- Measured at commit: `a8fd2b7` (main, after `git pull --ff-only` from a stale `67ab237`)
- This file committed as: `1ad6c2c` (the commit that introduces this document; tree content
  of all measured paths is identical to `a8fd2b7` because this commit adds only this file)

**Baseline authority rule:** when this document and a dispatch prompt name different SHAs,
the dispatch prompt's SHA is authoritative for *which tree to read*. `1ad6c2c` and
`a8fd2b7` differ by exactly one file — this one. All measurements below were taken at
`a8fd2b7` and remain valid at `1ad6c2c`.
- Status: **FROZEN BASELINE — not an acceptance decision**
- Authority: Owner-level dispatch baseline; each Owner retains normative authority in its own scope.

## Why this document exists

Six work areas were named as key missing workload, with percentages (85% / 80% / 90% /
60% / 100% / 100% unimplemented). Those figures were produced against an older tree.
The repository has since advanced 536 commits. This document re-measures each area at
the current base commit so dispatch rests on the tree, not on remembered numbers.

**All prior percentages are superseded by the measurements below.** Where a measurement
contradicts the prior claim, the measurement governs and the contradiction is stated.

## Measured state at commit `a8fd2b7` (= tree of `1ad6c2c`)

### GAP-01 — Memory Compiler core logic

| Item | Measured |
|---|---|
| Owning Owner | **E** (Memory Compiler Architect) |
| Docs | `04-memory-compiler/` exists with 2 files: `phase-1-event-store-contract.md` + `.zh-CN.md` |
| Rust code | **0** — no crate references `compiler`/`Compiler` anywhere under `crates/` |
| Reference model | 0 |
| Prior claim | 85% unimplemented |

**Correction:** the area is not 85% unimplemented — it is **0% implemented as code** and
~10% specified. The two existing files are an event-store contract, not a compiler stage
contract. There is no `crates/memory-compiler`.

Acceptance condition: a compiler stage contract exists naming stages, inputs, outputs,
provenance fields and failure semantics; plus `crates/memory-compiler` (or an equivalent
reference model) whose tests run under the pinned toolchain and report exact pass counts.

### GAP-02 — Memory Context engine

| Item | Measured |
|---|---|
| Owning Owner | **G** (Memory Context Architect) |
| Design docs | 19 `.md` files |
| Rust implementation | `crates/memory-context/src/lib.rs` — **472 lines, 7 `#[test]`** |
| Python reference model | `06-memory-context/reference-model/g_applied_ledger.py` + test |
| Prior claim | 80% unimplemented |

**Correction: the prior claim is wrong.** A real, compiling implementation exists with
deterministic snapshot planning (`ContextBudget`, `ContextIdentity`, delivery intents
that are non-sendable by construction). The area is partially implemented, not 80% absent.

Residual gap: the crate stops before persistence and transport by design. Delivery
intents are non-sendable, so no end-to-end path exists yet.

Acceptance condition: every documented concern (budget/sufficiency, edit operations,
reconciliation, versioning, manager) maps to either an executable model with tests or an
explicit `NOT IMPLEMENTED` row with a stated blocking reason.

### GAP-03 — Agent Integration core

| Item | Measured |
|---|---|
| Owning Owner | **C** (Agent Integration Architect) |
| Design docs | 4 `.md` files |
| Rust code | **0** — no crate references adapter/agent-integration types |
| Tests | **0** |
| Prior claim | 90% unimplemented |

**Correction:** confirmed — nothing executable exists. The `adapter` matches found under
`crates/memory-*` are SQLite adapter naming, unrelated to agent adapters.

Acceptance condition: an adapter capability tier table bound to concrete operations,
plus an executable reference model demonstrating tier enforcement and inference-boundary
rejection, with tests.

### GAP-04 — BMCP full protocol stack

| Item | Measured |
|---|---|
| Owning Owner | **H** (BMCP Protocol Architect) |
| Contracts | 4 `.md` files |
| Schemas | 1 (`bmcp.applied-delivery-evidence-1.0.0.schema.json`) |
| Validators | 1 (`applied_delivery_evidence_validator.py`) |
| Conformance suites | `applied_delivery_evidence` has a test file; `provider_outcome` has **fixtures + requirements.txt only, no test** |
| Rust code | **0** — no crate or tool references BMCP |
| Prior claim | 60% unimplemented |

**Correction:** the area is ~85% unimplemented as code. Only one of two conformance
suites executes; the protocol itself has no runtime implementation.

Acceptance condition: every schema has a validator and an executing conformance suite;
`provider_outcome` fixtures gain a test file; a protocol index enumerates all message
types with implemented/unimplemented status.

### GAP-05 — Phase 2/3 domain model extension

| Item | Measured |
|---|---|
| Owning Owner | **B** (Domain Model Architect) |
| Docs under `02-domain-model/` | 10 `.md` files, all Phase-1 scoped (`phase-1-*` ×4) |
| Rust code | `crates/memory-domain/src/lib.rs` — 679 lines, 13 `#[test]` |
| Phase 2 artefacts | **0** |
| Phase 3 artefacts | **0** |
| Prior claim | 100% not started |

**Correction:** "100% not started" is accurate for Phase 2/3 specifically, but must be
read narrowly — Phase 1 domain model **is** implemented in Rust. The gap is the Phase 2/3
extension, not the domain model as a whole.

Acceptance condition: a Phase 2 domain extension specification with entity, invariant and
migration statements, accepted by Owner B or explicitly blocked with a named dependency.

### GAP-06 — End-to-end tests

| Item | Measured |
|---|---|
| Owning Owner | **A** (Principal Integration Architect) |
| `tests/` at repo root | 2 files: `test_check_bilingual_docs_full.py`, `test_policy_inheritance.py` — both governance, neither cross-module |
| Integration tests | `crates/memory-event-store-sqlite/tests/{forget_fence,resilience}.rs`, `crates/memory-store/tests/sqlite_integration.rs` — each exercises one crate |
| E2E harness | `benchmarks/req10_e2e/` exists with `benchmark.py` + `fixture_runtime.py` |
| E2E actual run | **NOT_MEASURED** — the harness README states "development baseline only. Integrated product-runtime measurements: NOT_MEASURED" and "The fixture is not a substitute for the runtime" |
| Prior claim | 100% not started |

**Correction:** "100% not started" understates the work — a harness contract and protocol
exist. But the harness has **no adapter executing the real product path**, so no
end-to-end test actually runs. The area is ~20% done (harness) / 0% done (real path).

Acceptance condition: at least one test executes a path spanning two or more of
{compiler, context, agent-integration, bmcp} against the real product path and asserts an
observable contract outcome, runnable by a single documented command.

## Corrected summary table

| Gap | Owner | Prior claim | Measured reality | Verdict on prior claim |
|---|---|---|---|---|
| 01 Compiler | E | 85% missing | 0% code, ~10% specified | **Understated** — worse than claimed |
| 02 Context | G | 80% missing | Partial: 472 lines Rust + 7 tests | **Overstated** — real code exists |
| 03 Agent Integration | C | 90% missing | 0% code | Confirmed |
| 04 BMCP | H | 60% missing | ~85% missing as code; 1 of 2 suites executes | **Understated** |
| 05 Phase 2/3 | B | 100% not started | 100% not started (Phase 1 is done) | Confirmed, with scope caveat |
| 06 E2E | A | 100% not started | Harness exists, no real adapter → nothing runs | **Understated** — work has begun |

## Dispatch rules

1. Each gap is dispatched to exactly one Owner conversation. No Owner edits another
   Owner's normative contract.
2. Cross-owner questions are recorded verbatim in the Owner's reply and the Owner stops
   at that boundary. Recording a boundary question is a valid terminal state.
3. No self-approval. Every delivery requires a separate review conversation with frozen
   inputs.
4. Percentages here are measurements at `a8fd2b7` and must be recomputed, not quoted, by
   any later status report.

## Explicit non-claims

- This baseline does not authorize merge, production activation, or closure of any
  finding in the R3 defect register.
- The corrected verdicts above are measurements of *presence in the tree*, not quality
  judgements of the code that exists.

## Post-baseline measurements

Everything above is a measurement at `a8fd2b7` and is left unedited, per dispatch
rule 4. This section records what changed afterwards, so a reader can tell a frozen
baseline from a moving target.

### GAP-01 — the compiler now has an executing admission layer

`GAP-01` above says "0% code". That is no longer true, and the change came from two
commits that were not part of the original dispatch:

| Commit | Content |
|---|---|
| `a730880e` | `crates/memory-compiler` — five typed stages, structured provenance, two distinct admissions, `PREPARED_HIDDEN`, pure Rust, zero dependencies |
| `8c58d4c6` (PR #427) | `src/admission.rs` +1217 lines — producer admission, fence/gate contention, protocol-sequence receipts; crate gains `rusqlite`, `sha2`, `serde` |

Measured on `main` at `8c58d4c6`, tree read back from the API and built in a clean
directory:

```
$ cargo test --offline -p memory-compiler
running 19 tests
test admission::tests::alternative_exit_transitions_are_accepted_and_persisted ... ok
test admission::tests::fence_and_gate_compete_on_one_protocol_sequence_exactly_one_wins ... ok
test admission::tests::final_gate_receipt_binds_observed_fence_and_permission_epoch ... ok
test admission::tests::gate_reports_stale_protocol_when_fence_generation_matches ... ok
test admission::tests::illegal_transition_accept_to_published_is_rejected ... ok
test admission::tests::partial_dependencies_remain_hidden_until_all_edges_are_registered ... ok
test admission::tests::producer_receipt_lookup_and_not_found_are_distinct ... ok
test admission::tests::producer_registration_is_idempotent_and_conflicting_digest_does_not_add_rows ... ok
test tests::extraction_is_deterministic_and_lineaged ... ok
test tests::ingestion_preserves_original_receipt ... ok
test tests::ingestion_requires_durable_receipt_and_intent ... ok
test tests::late_worker_cannot_publish ... ok
test tests::normalization_preserves_upstream_identity ... ok
test tests::publication_requires_second_admission ... ok
test tests::publication_requires_visibility_authorization ... ok
test tests::staged_derivative_is_hidden ... ok
test tests::staging_requires_complete_dependency_closure ... ok
test tests::staging_requires_producer_admission ... ok
test tests::successful_publication_requires_both_admissions ... ok

test result: ok. 19 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.29s
```

Nineteen tests, not eleven. The eight new ones are all admission-layer behaviour.

**Environment note, because it changes how this must be reproduced:** the crate now
depends on `rusqlite`, which needs a C compiler. On the Windows host `gcc` cannot
execute `cc1`, so `libsqlite3-sys` cannot build there at all — this is a host
environment defect, not a crate defect. The run above was executed in WSL2 Ubuntu
with `cargo 1.95.0` / `gcc 13.3.0` and `CARGO_BUILD_JOBS=1` (parallel codegen on the
`/mnt/c` mount exhausts memory). Any future claim about this crate must state which
toolchain produced it.

### GAP-01 — one architecture, not two: Owner E ruling recorded

A second GAP-01 delivery existed as PR #425 (root `04-memory-compiler/`, six stages,
Python reference model, 10 tests). Owner E was asked to adjudicate and returned
`FINAL: DECIDED`:

| Question | Ruling |
|---|---|
| Path convention | `docs/en/` + `docs/zh-CN/` mirrors. Root `.zh-CN.md` suffix is **not** the pattern for new normative documents. |
| Stage inventory | **Five** stages. `Provenance` is a cross-cutting field on every stage output, **not** a sixth stage. |
| Reference implementation | `crates/memory-compiler` (Rust) only. The Python model does not survive as a second executable authority. |

The ruling is `DECIDED FOR CONVERGENCE`, explicitly not `ACCEPTED`, and it does not
grant Owner E any authority over D, I or Storage admission — `PublicationAuthority`
stays an injection boundary, and the seven `PublicationProof` booleans are evidence
inputs E may verify but may not issue.

This ruling was not accepted on assertion. Reproducing `current_bilingual_gaps()` from
`scripts/check_bilingual_docs.py` against both trees showed PR #425 would add **three**
new bilingual gaps (its two contract files plus `reference-model/README.md`, none with
`docs/en` or `docs/zh-CN` counterparts), and `main()` returns 2 on any new gap. `main`
itself has **zero** gaps in that directory. One of the two placements could not
survive the gate; the ruling chose the one that can.

### GAP-06 — first cross-module test exists and executes

PR #444 adds `crates/memory-context/tests/e2e_store_to_context.rs`, spanning
`memory-storage-sqlite` → `memory-store` → `memory-context`. Measured:

```
$ cargo test -p memory-context --test e2e_store_to_context
running 1 test
test sqlite_store_read_current_builds_context_from_persisted_revision ... ok
test result: ok. 1 passed; 0 failed; 0 ignored
```

One test is not an E2E suite, and `benchmarks/req10_e2e/README.md` still says
`NOT_MEASURED` — correctly, because this exercises modules, not the product runtime.
The GAP-06 acceptance condition ("a path spanning two or more modules, single
documented command") is met for the first time.

### GAP-02, GAP-04 — suites now execute

| Gap | Suite | Measured |
|---|---|---|
| 02 | `06-memory-context/reference-model/test_g_context_model.py` (PR #433) | `Ran 15 tests ... OK` |
| 04 | `08-bmcp-protocol/tests/conformance/provider_outcome/test_provider_outcome.py` (PR #436) | `Ran 10 tests ... OK (skipped=5)` |

The five skips in GAP-04 name their own blocker (`requires Owner C authoritative
validator`). Recording a skip with a named dependency is the correct outcome; making
them pass against a local reimplementation would have been a false green.

### What has not changed

- GAP-03 remains 0% code. PR #430 is a candidate specification, `DRAFT`, `approver:
  null`, `normative_status: Informative`.
- GAP-05 remains unimplemented. PR #435 is a specification; the Phase 2 entities,
  revisions and invariants it defines exist in no Rust type.
- No gap is closed. Every number above is a measurement of presence, not a quality
  judgement, and none of it is acceptance.
