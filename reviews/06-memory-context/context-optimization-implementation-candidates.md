# Context Optimization Implementation Candidates

**Owner:** G — Memory Context Architect  
**Branch:** `session-g-memory-context`  
**Status:** Candidate register only; no implementation or interface freeze  
**Assessment date:** 2026-11-17

This register is independent from the research assessment. Every item is a proposed candidate and is explicitly marked with its governance state. No item changes the current G baseline.

## Status legend

- **PROPOSED** — G recommends investigation/design; not accepted or implemented.
- **OPEN** — unresolved design question; evidence/owner decision required.
- **NEEDS_CROSS_OWNER_APPROVAL** — cannot progress to DECIDED without named owner approval.
- **NOT_IMPLEMENTED** — explicitly not implemented in this branch/research phase.

## Candidate register

| ID | Candidate | Status | Existing G home | Required dependencies |
|---|---|---|---|---|
| G-CO-01 | Boundary-triggered compaction reevaluation (completed subtask, verified milestone, phase transition, pause/handoff, window pressure) | PROPOSED | Context Planner / Budget Manager | C boundary event; F completeness |
| G-CO-02 | Dynamic economic decision record: removable tokens, memo size, write/cache cost, remaining horizon, growth, recovery cost, uncertainty, reason | PROPOSED | Budget Manager | C/H cost telemetry; F recall cost |
| G-CO-03 | Conservative horizon and recovery-cost model; safety veto and hysteresis/cooldown | PROPOSED | Budget Manager | F recall availability; H cache/latency |
| G-CO-04 | Task Semantic State (TSS) typed projection: goal, progress, evidence, decisions, constraints, uncertainty, failures, artifacts, next work | PROPOSED | Context Entry / Context Version projection | B schema; C boundary and state handoff |
| G-CO-05 | TSS revision and lineage linkage to ContextVersion, parent state, source set, compaction profile | PROPOSED | Context Versioning | D lineage and publication gate |
| G-CO-06 | Six-axis fidelity report and hard rejection/quarantine outcomes | PROPOSED | Compact operation / Context Sufficiency | D evidence refs; I Scope/permission; F source recall |
| G-CO-07 | Context Observation Reference typed metadata contract | PROPOSED | Context Entry source refs | B, C/H, F, D/Storage, I |
| G-CO-08 | Bounded exact range recall with hash/revision revalidation and audit | NEEDS_CROSS_OWNER_APPROVAL | Context Entry / Reconciler | F retrieval semantics; D/Storage durable object; I authorization |
| G-CO-09 | Compaction lineage/loss ledger: exact source membership, hashes, omissions, algorithm/profile, validator outcome | PROPOSED | Compact operation / ContextVersion | D producer/dependency receipts |
| G-CO-10 | New immutable ContextVersion for each successful non-no-op compaction | PROPOSED | Context Versioning / ChangeSet | D final publication gate; Storage |
| G-CO-11 | Reject stale Snapshot/Delta/replay if source revision, permission, Forget fence, target version or base hash is stale | PROPOSED | Reconciler / Delivery Coordinator | D, E, H, I |
| G-CO-12 | Extend Forget invalidation to TSS, observation archives, recall handles, compacted derivatives, caches, queues, Snapshot/Delta and offline Adapter state | NEEDS_CROSS_OWNER_APPROVAL | Reconciler / Forget integration | D, E, F, H, I, Storage |
| G-CO-13 | Paired benchmark suite for FHA/EoCC/dynamic compaction/ObservationRef/TSS-SAC stress mode | PROPOSED | Context Sufficiency / test harness | A acceptance; C/F/H instrumentation |
| G-CO-14 | Frozen held-out evaluation with capability floor and isolated test feedback | NEEDS_CROSS_OWNER_APPROVAL | Architecture validation process | A + independent evaluator |
| G-CO-15 | Candidate receipt generation with exact quote/hash verification and original-output fallback | PROPOSED | Compact operation | F source retrieval; I remote processing policy |
| G-CO-16 | TSS and observation data classification/retention policy mapping | OPEN | Context Entry / Reconciler | I, D/Storage |
| G-CO-17 | Determine whether ObservationRef is a Context Entry ref, F locator, or independently owned object | OPEN | Existing Context Entry/source refs | B, D, F, I |
| G-CO-18 | Define C/H boundary event schema and declared-vs-verified completion | OPEN | Context Planner input contract | C, H |
| G-CO-19 | Define cache-write/prefix-discontinuity and recovery-cost telemetry | OPEN | Budget Manager input contract | H, C, F |
| G-CO-20 | Define durable archive owner, retention, deletion and range-read guarantees | OPEN | No new G module proposed | D/Storage/I |

## Explicit non-candidates / exclusions

| Item | Status | Rationale |
|---|---|---|
| Direct import of SoL-Pi numerical thresholds/default parameters | NOT_IMPLEMENTED | Experimental Pi configuration is not a Brain production profile |
| Action Fusion implementation in G | NOT_IMPLEMENTED | Action execution/tool orchestration is outside G ownership |
| New standalone Observation Service or index | NOT_IMPLEMENTED | No demonstrated need; F owns retrieval/indexing and G has existing source-ref fields |
| Canonical Memory mutation by compaction | NOT_IMPLEMENTED | TSS/compaction is a Context projection, not a canonical fact |
| Treating summaries as verified facts | NOT_IMPLEMENTED | Violates epistemic/evidence boundaries |
| SAC as default Agent execution mode | NOT_IMPLEMENTED | SAC changes action granularity; only a stress-test candidate |
| Bypassing D producer registration/final publication gate | NOT_IMPLEMENTED | Violates derivative publication and Forget fence contract |
| Bypassing I permission checks on recall/cache | NOT_IMPLEMENTED | Stable reference is not authorization |
| Weakening H final-boundary Applied proof | NOT_IMPLEMENTED | Delivery/compaction does not prove Adapter application |

## Suggested sequencing

1. **Design-only:** G-CO-01 through G-CO-06, extending existing Budget Manager/Compact/TSS projection semantics.
2. **Contract alignment:** G-CO-07, G-CO-08, G-CO-16 through G-CO-20 with B/C/D/F/H/I/Storage.
3. **Safety closure:** G-CO-09 through G-CO-12, with D/Storage publication and Forget gate demonstrated before implementation.
4. **Validation:** G-CO-13 through G-CO-15 after interface owners approve instrumentation and frozen evaluation design.

## Governance statement

All entries remain candidate-level. **Nothing in this register is DECIDED, frozen, implemented, or authorized for Rust changes.** The two deliverables are research outputs only.