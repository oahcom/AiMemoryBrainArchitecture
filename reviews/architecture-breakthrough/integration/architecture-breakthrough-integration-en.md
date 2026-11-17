# Architecture Breakthrough Research — Integrated Review & Cross-Examination

- Review ID: ABR-INTEGRATION-001
- Status: **Research integration disposition; not Owner approval, ADR, or architecture freeze**
- Baseline: `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Integration branch: `review/architecture-breakthrough-integration-2026-11-18`
- Inputs: PR #84 (Session 0), #88 (A / Forget), #86 (B / Memory OS), #85 (C / Memory IR)
- Governance tracker: Issue #43
- Scope: cross-review of the four breakthrough submissions only; this is not the full A–I + Storage consolidation required by Issue #43.

## 1. Executive disposition

This research does **not** prove that a new architecture outperforms the current architecture, nor that Forget meets production safety requirements. The integrated findings are:

| Topic | Disposition | Actionable conclusion |
|---|---|---|
| Forget formal verification | **P0 / NOT READY** | Keep cross-D/E/I/Storage publication and recovery safety as the top verification target; extend the model and map it to Owner contracts and physical tests |
| Memory Resource Manager | **CANDIDATE / SHADOW ONLY** | Research only an internal Runtime resource control plane; do not merge F Retrieval/Activation with G Context semantics or create authority over Permission/Forget |
| Memory IR | **CANDIDATE / SHADOW ONLY** | Research only a versioned typed stage contract inside E; do not replace D Canonical Commit or decide B Fact/Claim |
| Overall architecture superiority | **UNRESOLVED** | No end-to-end controlled comparison under identical workloads and safety constraints |
| Architecture freeze | **NOT READY (within this research scope)** | This report does not pass Issue #43 G1–G8 or close any existing P0 / ADR blocker |

Recommended order: **strengthen Forget modeling and cross-module contract evidence first; prepare shadow experiments for B/C in parallel; consider architecture adoption only after measured net benefit and explicit Owner acceptance.**

## 2. Exact baseline and ref topology

### 2.1 Current main

A live compare of `e52594f... ↔ main` returned `identical`. Current main HEAD is therefore:

`e52594f181d2edb77448adcfed64a0fbdffaf3aa`

The compare from `b3c666e...` to `e52594f...` reports 2 commits ahead, 0 behind and 0 changed files. This is a history difference, not demonstrated tree-content drift.

### 2.2 Four research PRs

| PR | Role | Head SHA | PR-recorded base SHA | Compare against current main |
|---|---|---|---|---|
| #84 | Session 0 coordinator | `c6e76b34cbf099d36631b284c9b8a75d778d707f` | `28fb37e21fa4ba2b871f7816fe669128618c063e` | diverged; merge base 28fb37e; main has one later historical commit than the report baseline |
| #85 | C / Memory IR | `c5013d3585d54457f38bef37984645e2055ff7cf` | `b3c666e67982cb3d3374e759cfb6552c7765aacb` | diverged; merge base b3c666e |
| #86 | B / Memory OS | `3892916ce2379f807a0ddcd0039816f6e88ecee1` | `b3c666e67982cb3d3374e759cfb6552c7765aacb` | diverged; merge base b3c666e |
| #88 | A / Forget | `bf35b32295d0d3f337c80c3dc406db0a41de6830` | `e52594f181d2edb77448adcfed64a0fbdffaf3aa` | diverged; merge base b3c666e |

Interpretation:
- All four PRs remain Open / Draft / Unmerged. Mergeability is not architecture approval.
- #84's report still names `28fb37e...` as its baseline; #85/#86/#88 primarily cite `b3c666e...`. This integration uses current main `e52594f...` as its review anchor.
- #88's historical divergence from current main is real. Do not merge it directly or disguise the history by merely changing the base field.
- However, the tree comparison between `b3c666e...` and `e52594f...` reports zero file changes. The submissions can therefore be reviewed against a common content baseline while retaining the history-divergence disclosure.
- Do not retarget, update, or merge the four research PRs; do not modify main or Owner branches.

## 3. Evidence levels and independence

This report distinguishes:
1. **Normative Owner contract:** only the exact version and explicit decision of the accountable Owner is authoritative.
2. **Research report:** supports integration reasoning but does not become normative by submission.
3. **Model/prototype result:** establishes behavior only within its abstraction, inputs and explored scope.
4. **Physical/production evidence:** real database, HA, crash, recovery, service and Adapter validation; no new evidence of this class was produced here.
5. **Owner acceptance:** must be explicit and issued by the authority for the exact version; role simulation cannot substitute for it.

This cross-examination was performed by one assistant session using multiple review perspectives. It is **not organizationally independent Owner approval or third-party independent review**. It must not be represented as sign-off by B/D/E/F/G/H/I/Storage.

## 4. A — Forget: evidence and cross-workstream review

### 4.1 Supported findings

PR #88 reports a Python explicit-state BFS: the safe-rule abstraction explored 606 state/depth pairs through depth 10 with no modeled invariant violation. Five weakened-guard mutants produced shortest counterexamples:
- Stale worker: admit → install_fence → publish
- Admission race: install_fence → admit
- Index rebuild: admit → publish → install_fence → rebuild_index
- Cache refill: admit → publish → install_fence → repopulate_cache
- Stale restore: install_fence → restore

These traces are mutant / weakened-guard counterexamples, not production incident traces and not five defects discovered by the safe model itself.

The A report explicitly concludes **NOT READY** for production. F1/F2/F5/F7 hold conditionally only within the bounded abstraction; F3 has incomplete cross-module proof; F4/F8 are unproven; F6 is only locally closed.

### 4.2 Cross-constraints with B Resource Manager

The Resource Manager must not:
- interpret fairness, task priority or budget reservation as authorization;
- bypass I Permission, D ForgetFence, Scope, Security or Freshness hard gates;
- keep an old Reservation valid across PermissionEpoch / ForgetFenceGeneration changes;
- re-expose suppressed content through reclaim, retry or rescheduling.

Required properties:
- resource decisions govern capacity, queueing and budget only; they grant no access rights;
- F/G revalidate authorization and Fence at their existing protected-read, Context Commit and Delivery boundaries;
- unavailable resource control or unknown control state fails closed for protected tasks;
- Reservations may carry typed control-version references but must not compare values across epoch namespaces.

### 4.3 Cross-constraints with C Memory IR

IR/Compiler must not:
- treat model extraction or IR validation as Canonical Truth;
- publish a derivative before durable Derived Dependency Registration and final Fence/Permission validation;
- reuse historical Forget receipts / Permission outcomes as publication authorization for a new DerivationRun;
- restore a forgotten derivative through incremental compilation caches.

Required properties:
- preserve source version/digest, transform version, provenance and lineage;
- every new DerivationRun re-satisfies current admission, dependency registration, Forget/Permission and publication gates;
- stale workers, stale IR and stale caches may remain only as invisible candidates or audit material; they cannot pass the final disclosure gate.

### 4.4 A P0 closure items

1. D + Storage: one atomic ordering domain for ProducerWork registration, Fence high-water capture, final lineage/Fence validation, and VisibilityPointer + PublicationReceipt commit.
2. I: authoritative Producer/Recipient/Backup/External-copy inventory, epoch/seal, join/leave/change invalidation and Global Forget completion.
3. E: exact Owner contract for Derived Registration and publication; the complete dependency set must be durable before visibility.
4. Storage + I: JF-10 cross-authority crash atomicity and recovery semantics.
5. F/G/H: end-to-end Fence validation for final retrieval disclosure, Context/Applied and Adapter reconnect.
6. Storage/I/D: physical proof that restore cannot roll back control high-waters with an old backup.

**A disposition: P0.** Model results are bounded logical evidence only. They must not be used as a production implementation release gate.

## 5. B — Memory Resource Manager: cross-review

### 5.1 Candidate value to preserve

PR #86's Option B is more restrained than a full Memory OS kernel: one internal Runtime resource control plane consolidating resource accounting, hierarchical budgets, reservations, fair scheduling and reclaim while preserving F/G domain semantics.

Synthetic experiment (30 tasks, 720 candidates, 9,000-token budget):
- Direct Top-K: Recall 0.5333; Precision 0.4741; Jain fairness 0.8325; 1 task starved.
- Rerank + Budget: Recall 0.5417; Precision 0.2863; Jain 0.8141; no starvation.
- Unified RM: Recall 0.5083; Precision 0.2699; Jain 0.8554; no starvation.
- Direct Top-K median 0.095 ms, Rerank + Budget 0.119 ms, and Unified RM 0.306 ms. These are single-threaded local Python microbenchmark values, not service latency.

The experiment therefore shows better fairness and no starvation, but lower Recall/Precision and higher local selection latency. It does **not** support a claim that Unified RM is universally better than the current design.

### 5.2 Integration constraints

- Keep Retrieval and Activation distinct.
- F Working Set / Cache is a disposable Runtime View; G Context is a versioned, governed inference region.
- Context token/byte budget is a semantic constraint, not equivalent to RAM/cache capacity.
- Applied Context is Adapter-side evidence, not Residency.
- Canonical Memory must never be evicted.
- Do not create a global durable Residency lifecycle.
- Resource Manager is a scheduler/capacity coordinator, not a new service or Security/Forget/Canonical Authority.

### 5.3 Experiment gate

Run Shadow Mode first, with no normative or runtime behavior change. Compare distributed budgets against a unified ledger on the same representative real workload and identical hard safety filters:
- Recall / Precision / nDCG / Sufficiency;
- p50/p95/p99 latency;
- token waste, RAM/VRAM peak, cache hit/miss;
- task starvation, Jain fairness and cross-Principal fairness;
- cancellation, deadline miss and partial result;
- latency/rate of rejecting stale Reservations after Forget / Permission revocation.

Pre-register workload, seeds, statistical method, baseline, stop conditions and rollback. Synthetic data remains an algorithm sanity check only.

**B disposition: Option B remains CANDIDATE; Option C (full Memory OS kernel) is not recommended. No architecture specification change before Shadow Mode evidence and Owner acceptance.**

## 6. C — Memory IR: cross-review

### 6.1 Candidate value to preserve

PR #85 proposes a Shadow Typed IR inside E's existing Compiler, not a Compiler rewrite or new Compiler service. It aims to stabilize stage types, source/evidence roles, Scope, temporal/epistemic qualifiers, transformation versions and provenance.

E already has durable acceptance, work items, deterministic normalization, optional model extraction, Evidence/Provenance, candidate/conflict proposals and D-owned canonical commit. IR should reduce stage-DTO ambiguity rather than duplicate these responsibilities.

### 6.2 Critical cross-constraints

- **B Fact/Claim ADR remains ADR-BLOCKED.** Use neutral candidate vocabulary (e.g. AssertionCandidate / opaque proposal); do not freeze canonical Fact/Claim identity, storage schema or wire discriminants.
- **D retains Canonical Commit.** IR emits candidates and validation reports only; it cannot write the canonical store directly.
- **E retains Compiler orchestration.** Shadow IR is an internal stage contract, not a separate service/platform.
- **Forget/Permission precede publication.** A new derivation requires new admission, dependency registration and final publication gates; historical authorization cannot be reused.
- **Provenance cannot be optimized away.** Semantic-preserving optimization records input/output digests, transform version and parent lineage.
- **Version compatibility is explicit.** ir_version/schema_digest/parser/extractor/model/policy/transform versions jointly affect the derivation fingerprint; unknown versions fail closed or quarantine.
- **Incremental recompilation is deterministic.** Recompile only affected lineage when inputs or pass versions change; a cache hit is not proof of current validity.

### 6.3 Evidence limitations

PR #85's prototype uses Python standard library and synthetic fixtures. Its report states: 5 input rows, 4 valid candidates, 1 conflict proposal, deterministic replay, and 3/3 unchanged source-node IDs in the incremental fixture. It does not test LLM behavior, entity resolution, concurrency, crash recovery, Forget, authorization, canonical commit or production caching.

The bounded Direct-vs-IR prototype cannot prove production complexity reduction or improved typing accuracy on real data.

**C disposition: Shadow Typed IR remains CANDIDATE; only a non-authoritative shadow experiment inside E is allowed. Do not change B's ADR, D Canonical Commit or the production Pipeline.**

## 7. Session 0 synthesis re-check

Session 0's three research directions broadly align with A/B/C, but their evidence labels must be read as follows:

1. TLA+ / Alloy: tool choice is CANDIDATE; Session 0's TLA+ skeleton has not run TLC. A's Python BFS is separate bounded-model evidence and must not be described as a TLC result.
2. Resource Manager Option B: candidate, with quality/latency trade-offs in the synthetic experiment; do not describe complexity reduction as proven.
3. Shadow Typed IR: candidate, below formal adoption threshold; Fact/Claim ADR remains blocked.
4. Whether the new architecture is superior: UNRESOLVED.
5. L1 Storage topology: the exact Storage ADR Blob `bb544ba...` §8.6 addendum selects Option A as the normative v1 logical architecture and explicitly supersedes the §3 pre-addendum “no option selected” historical text; the v3.3.2 manifest Blob `5c614375...` also says it corrects the ADR status. L1 logical topology is therefore DECIDED. This is not L4 physical database/HA/recovery proof; L4 remains OPEN. A later finding in A PR #102 that the ADR is internally contradictory must be reconciled against the explicit §8.6 supersession language rather than ignoring that addendum.

## 8. Conflict and risk register

| ID | Severity | Risk / ambiguity | Accountable authority | Status |
|---|---|---|---|---|
| INT-01 | P0 | Atomic ordering of Producer Registration / Fence / Dependency Registration / Visibility Commit unproven | D/E/Storage | OPEN |
| INT-02 | P0 | Completeness of Producer/Recipient/Backup/External-copy inventory and Global Forget completion unproven | I | OPEN |
| INT-03 | P0 | JF-10 crash atomicity across I sequencer and Storage visibility unproven | I/Storage | OPEN |
| INT-04 | P0 | Physical evidence that restore cannot roll back control high-waters is missing | Storage/I/D | OPEN |
| INT-05 | P1 | Consistent Fence enforcement across F/G/H final disclosure, Applied and Adapter reconnect is unverified | F/G/H | OPEN |
| INT-06 | P1 | Resource Manager decisions could be misused as authorization or stale Reservations could survive epoch changes | F/G + I/D | MITIGATION REQUIRED |
| INT-07 | P1 | IR could prematurely freeze B Fact/Claim semantics or bypass D Commit / Forget registration | E + B/D | MITIGATION REQUIRED |
| INT-08 | P1 | Research reports use different historical bases; source pins must be refreshed at every current Owner HEAD | Integration / A | PARTIALLY RESOLVED |
| INT-09 | P1 | B experiment shows fairness gains but Recall/Precision/latency regressions | B + F/G | TO_VALIDATE |
| INT-10 | P1 | C prototype is small and does not prove production gains or concurrency/recovery correctness | C + E | TO_VALIDATE |
| INT-11 | P2 | Session 0 TLA+ skeleton and A Python BFS differ in verification target/coverage and could be conflated | Integration | CLARIFIED |

## 9. Research decisions and prohibited inferences

### DECIDED (review dispositions only)
- Current main review anchor is `e52594f...`.
- All four submissions are Draft/non-normative and do not create architecture approval.
- Cross-module production Forget safety is unproven.
- B/C may not change existing Owner authority boundaries.
- B/C require shadow experiments and accountable Owner acceptance.
- This research closes no Issue #43 gate or P0 blocker.

### CANDIDATE
- TLA+ as the primary Forget concurrency model; Alloy as relational supplement.
- Runtime-internal Resource Manager Option B.
- E-internal Shadow Typed IR.

### UNRESOLVED / ADR-BLOCKED
- Overall superiority of the new architecture over the current one.
- Net benefit of B Resource Manager on real workloads.
- Net benefit of C IR on real data and the full E Pipeline.
- B Fact/Claim ADR.
- Forget P0 and JF-10 / physical recovery proof.

### Prohibited inferences
- A bounded model pass is not an unbounded proof or production safety certification.
- A synthetic benchmark is not evidence of real-user benefit.
- A runnable prototype is not proof of production implementation feasibility.
- Simulated multi-Owner perspectives in this session are not independent Owner signatures.
- Draft PR, mergeability or document existence is not approval.

## 10. Ordered next steps

1. **A / P0:** Extend the Forget model with Producer/Recipient inventory epoch, Admission/Fence/Dependency/Publish, Lease/Attempt, DLQ/Replay, lost ACK, PermissionEpoch, Index/Context/Adapter and Restore high-water. Keep each variable in its authority-local namespace.
2. **D/E/Storage/I:** Provide exact contracts and physical verification plans for INT-01 through INT-04; remain BLOCKED until accountable Owner acceptance.
3. **F/G/H:** Publish a Fence-check matrix and unknown-state behavior for protected reads, Context Commit, Delivery, Applied and Reconnect.
4. **B:** Prepare Shadow Mode workload, metrics, experiment preregistration and rollback; no normative edits or Runtime changes.
5. **C:** Prepare a 20–50 experience IR shadow corpus, schema-evolution tests and deterministic replay; keep neutral candidate vocabulary while Fact/Claim is blocked.
6. **Integration re-review:** Re-pin exact branch/commit/path/blob at every Owner's current HEAD and collect explicit consumer acceptance before deciding whether to create a formal ADR.

## 11. Final conclusion

**Overall disposition: READY FOR FOCUSED RESEARCH / NOT READY FOR ARCHITECTURE FREEZE OR PRODUCTION IMPLEMENTATION.**

The highest-value next step is not to invent a larger unifying abstraction for Memory OS, Compiler and Forget. It is to use the smallest executable, falsifiable evidence to resolve critical ordering across authorities. Potential B/C simplifications must remain subordinate to that safety path rather than introducing new authority layers.

This is an integration review deliverable, not Owner sign-off, not an architecture ADR and not production acceptance.
