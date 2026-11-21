---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope: null
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "Frozen baseline measured at a8fd2b7; file introduced by 1ad6c2c"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Historical frozen measurements; this bilingual remediation does not remeasure implementation state."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/work-items/GAP-BASELINE-001.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/GAP-BASELINE-001.md"
---

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
