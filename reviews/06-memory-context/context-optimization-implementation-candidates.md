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
| G-CO-17 | Determine whether ObservationRef is a Context Entry ref, F locator, or independently owned object | DECIDED (G-local bounded disposition; see § Decision G-CO-17) | Existing Context Entry/source refs | B, D, F, I for any future archive-backed member type |
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

## Decision G-CO-17 — Archive-only reference boundary (G-local)

**Status:** DECIDED — bounded G-owned semantic disposition; no implementation or shared-interface freeze.

**Decision (2026-11-19):**

1. **F `ArchiveLocator` is an F-owned retrieval locator**, not a Canonical `MemoryVersionRef`, not a G `ContextEntry` membership identity, and never an authorization grant.
2. **F `ObservationRecallResult` is bounded recall evidence**, not a Context mutation, ContextVersion, or membership grant. Its exact archive object revision/hash/source revision/range/ReadReceipt, provenance, completeness/freshness and omission state remain F-returned evidence.
3. **G `ObservationRef` (if/when its proposed typed metadata contract is adopted) is provenance metadata only**. It may annotate the source/evidence lineage of a separately eligible ContextEntry; it does not itself create membership or make archive bytes a canonical fact.
4. **Direct archive-only references are ineligible for G Context membership.** The current Context membership path remains an exact, independently resolvable and currently authorized canonical `MemoryVersionRef`, with complete D lineage/producer registration and final publication gate plus current I classification/authorization/retention/Forget controls. An archive-only observation may become eligible only if D independently admits it as a canonical Memory version through its own governed process; an F locator, archive manifest, excerpt or receipt alone cannot do so.
5. **Fail-closed source handling:** before each F read, F must revalidate current I permission and applicable D Forget fence. Expired locator, source revision/hash mismatch, revocation, Forget/fence, corruption, unavailability, incomplete/partition-gap evidence or unknown authority means the archive evidence is unavailable/suppressed/partial, never silently fresh or complete. G must not create/update a Context membership from that result. If archive evidence was used to support a canonical ContextEntry, G re-evaluates that entry's evidence sufficiency and marks it stale/blocked or removes/replaces the affected provenance reference as appropriate; no silent substitution or resurrection.
6. This is a **permanent exclusion of direct F archive locator/recall-result membership under the current G membership model**, not a blanket exclusion of archive-derived information if D later canonicalizes it, and not a decision on F's storage/retention implementation, D's canonical admission/lineage, or I's policy.

**Alternatives considered:**
- (A) Admit ArchiveLocator/ObservationRecallResult directly as a Context member: rejected because it would create a non-canonical membership path whose source expiry, lineage, Forget and authorization gates are not established by G's current ContextEntry contract.
- (B) Keep the binary membership question indefinitely OPEN: rejected because G owns Context membership semantics and the current baseline already requires canonical refs; indefinite ambiguity would leave F unable to close its response boundary.
- (C) Treat archive content as canonical by implication or locator possession: rejected because F explicitly states archive manifests are not Canonical Memory and locator is not a bearer credential or grant.

**Evidence pins (read-only source evidence):**
- G baseline branch HEAD `0f77ffbe956c5f93df295c436fcb0a750629d595`; G lifecycle source `06-memory-context/phase-3.7-g-local-lifecycle-producer-derivative-queue-recall-context-restore.md`, Blob `c1de241ec69834377d9b0e24aa4770a809796d4b`; G Context architecture `06-memory-context/context-architecture.md`, Blob `56fcc0ea112d423ef69a3f00e9d626bf4230ca0e`; G Context edit operations Blob `10c94e85dfe89d20dcdb202cafc2bef767f076fc`.
- F branch HEAD `1908ce4d233b20f7cafd00cb679affd01bd15174`; F archive candidate `reviews/05-memory-runtime/observation-archive-interface-candidates.md`, Blob `0b5c5b02c5b318c79606328ef1c22d686b8fc8b3`. F §3–5 says archive manifests are not canonical, ArchiveLocator is not a grant, and RecallIntent is not a Context mutation; §10 says ObservationRecallResult has no ContextVersion/mutation instruction; §14 assigns membership to G and lists expiry/invalidation questions.
- Cross-owner confirmation: F Issue #21 comment #7020865219 confirms compatibility with the recall-only/non-member boundary but explicitly does not approve a future archive-backed Context type or close the future typed contract.

**Decision boundary / remaining candidates:** G-CO-07 remains PROPOSED (typed provenance metadata contract); G-CO-08 remains NEEDS_CROSS_OWNER_APPROVAL (bounded exact-range recall); G-CO-16 remains OPEN (classification/retention mapping); G-CO-20 remains OPEN (durable archive owner/retention/deletion/range-read guarantees). D/I/F/Storage approvals remain independent for any future archive-backed member type. This G-local disposition does not claim their approval.

**Verification ceiling:** source comparison and exact Blob/branch pins only. No code, tests, CI or production behavior changed or verified. This record is a design decision, not implementation evidence.

## Governance statement

All entries remain candidate-level **except the explicitly bounded G-CO-17 disposition above**. No other item is DECIDED, frozen, implemented, or authorized for Rust changes. The two research deliverables remain research outputs only.