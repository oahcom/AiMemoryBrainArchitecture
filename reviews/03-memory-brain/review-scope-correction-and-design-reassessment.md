# Session D Review Scope Correction & Design Reassessment

- Date: 2026-11-16
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Original review: `reviews/03-memory-brain/three-party-six-dimension-review.md` on `main`
- D branch: `session-d-memory-brain-2026-11-16`
- D design baseline: commit `9dc08c63f6912320e290a963c634748ec44a81c8`
- D review artifact on D branch: `reviews/03-memory-brain/three-party-six-dimension-review.md`
- Reassessment type: branch-aware static architecture reassessment; three simulated specialist perspectives, not three separately staffed reviewers
- Status: **RECLASSIFIED — original repository-delivery FAIL is valid for its stated main-branch baseline, but it is not a valid verdict on the D design itself. D design is CONDITIONALLY ACCEPTABLE as a candidate specification, subject to the findings below.**

---

## 1. Executive decision

The original review explicitly declared `main` as its review baseline and stated that the five D files were absent from that branch. That observation was correct for the branch and time it examined. The report also correctly warned that it was not judging unseen branch contents.

The subsequent branch-aware inspection confirms that all five D deliverables exist on `session-d-memory-brain-2026-11-16`:

1. `03-memory-brain/memory-brain-overview.md`
2. `03-memory-brain/canonical-memory-store.md`
3. `03-memory-brain/memory-lifecycle-manager.md`
4. `03-memory-brain/entity-and-relationship-manager.md`
5. `03-memory-brain/memory-versioning.md`

The branch contains one D delivery commit and is not the same tree as current `main` (the refs have diverged). Therefore:

- The original FAIL remains a valid **main-branch integration/readiness finding at the original review baseline**.
- It must not be reused as evidence that the D architecture itself failed.
- The D branch's own review report is useful design self-review evidence, but it explicitly disclaims independent third-party review status.
- This reassessment reviews the actual D documents. It does not merge branches, modify D source files, approve upstream ADRs, or claim implementation/security/performance tests have passed.

## 2. Evidence and review scope

### 2.1 Confirmed branch facts

- D branch: `session-d-memory-brain-2026-11-16`.
- D design commit previously identified: `9dc08c63f6912320e290a963c634748ec44a81c8`.
- The five D files were fetched successfully from that branch.
- The branch's own review report was also fetched successfully.
- The original review file on `main` was fetched independently. Its declared baseline and missing-file rationale match the branch-visibility issue described above.
- Commit comparison shows the D branch and `main` have diverged; the D branch must not be treated as already integrated into `main`.

### 2.2 What this reassessment does not claim

No Rust implementation, schema migration, database transaction, concurrency, crash recovery, penetration, prompt-injection, Forget erasure, or performance benchmark was executed. All findings are static design findings or explicit unresolved dependencies.

---

## 3. Corrected disposition of the original review

| Original conclusion | Correct interpretation after branch inspection |
|---|---|
| D files missing from `main` | Valid repository visibility/integration finding at the original baseline |
| D is FAIL / Not Reviewable | Valid only for the original `main`-only review scope; not a verdict on D branch design quality |
| INT-P0 / INT-P1 items cannot be verified in D | Superseded for static design coverage where the D branch now provides evidence; still open where the design itself marks them OPEN or requires downstream enforcement |
| D must submit five documents | Already satisfied on the D branch; not yet satisfied on `main` |
| Do not freeze contracts | Still correct for ADR-blocked and OPEN items; not a blanket prohibition on all D candidate contracts |

**Required correction to project status:** Track two separate gates:
1. `D_DESIGN_REVIEW`: this branch-aware reassessment.
2. `D_MAIN_INTEGRATION`: whether the reviewed D commit is integrated into the shared baseline after cross-module review.

Do not collapse these into one PASS/FAIL field.

---

## 4. Six-dimension reassessment

### Dimension 1 — Architecture and responsibility boundaries

**Result: PASS WITH CONDITIONS**

Evidence:
- `memory-brain-overview.md` sections 1–4 and 9–10.
- `canonical-memory-store.md` sections 1–4 and 10.
- `entity-and-relationship-manager.md` sections 1–4 and 10.

The documents consistently place canonical identity, immutable revisions, lifecycle history, typed entity/relation assets and Forget dependency records under Brain authority. E proposes; F reads and projects; G owns ContextVersion/ChangeSet; H owns wire/Adapter; I owns global policy and physical-erasure governance. Brain does not absorb Agent planning, tool execution, prompt construction or environment control. Logical components are not prematurely prescribed as separate services/crates.

Condition:
- Preserve the ownership split. D must not absorb G's Context authority, H's wire contract, or I's global authorization/physical deletion responsibilities.
- Keep D-to-module interfaces at domain-contract level until the owning modules finalize their own transport/API schemas.

### Dimension 2 — Domain model and semantic completeness

**Result: CONDITIONAL PASS**

Strengths:
- Memory, MemoryVersion, Claim, candidate FactRecord, Evidence, ProvenanceRecord, Entity, Relation, ConflictSet, LifecycleEvent and ForgetOperation are distinguished.
- Epistemic status, lifecycle, confidence, trust, evidence strength and relevance are treated as separate dimensions.
- Entity identity is not inferred from display names or aliases.
- Merge/Split and Relation revision/migration preserve historical identity rather than rewriting historical references.
- Fact/Claim remains explicitly ADR-blocked.

Open dependencies:
- INT-P0-01: Fact/Claim ADR remains upstream-governed; D's FactRecord recommendation is a candidate, not a decision.
- DM-005: generic Scope algebra, multi-owner and shared ownership remain open.
- DM-006 / DM-013: minimum typed reference/time schemas, vocabulary registry and schema migration policy need joint closure with B/H/I.
- Claim identity/revision and ConflictSet semantics remain candidate pending the ADR.

No D-local defect is established merely because these upstream decisions remain open. The documents correctly mark them as non-frozen.

### Dimension 3 — Data flow, transaction and historical consistency

**Result: CONDITIONAL PASS — two D-local contract corrections required**

The design includes immutable revisions, CAS, stale-write rejection, idempotency receipts, canonical commit sequence, outbox/replay, rebuildable projections and exact historical references. These are appropriate foundations.

However, the following issues must be resolved before implementation contracts are frozen:

#### D-REV-P1-001 — Lifecycle state vocabulary contradicts across D documents

- Severity: P1
- Evidence:
  - `memory-brain-overview.md`, section 7: says a non-Forgotten Memory may enter “Forgetting” through a governed operation.
  - `memory-lifecycle-manager.md`, sections 6–7: explicitly says temporary Forgetting belongs to `ForgetOperation`, not to the permanent Memory lifecycle state machine.
- Problem: one document makes Forgetting appear to be a Memory lifecycle state; another explicitly excludes it.
- Impact: E/F/G/H may implement incompatible state filters, event handling and Context invalidation behavior.
- Owner: D.
- Dependency: I and E/F/G/H must confirm the cross-module event interpretation.
- Required correction: make all D documents consistent. Recommended rule: Memory lifecycle remains Candidate/Consolidated/Active/Superseded/Archived/Forgotten; in-progress suppression is represented by ForgetOperation state/fence, not a Memory lifecycle state. If an API exposes an effective availability state, name and define it separately from lifecycle.
- Acceptance: one normative state table; no D document describes Forgetting as a Memory lifecycle state; downstream behavior distinguishes lifecycle state from Forget suppression.

#### D-REV-P1-002 — Canonical sequence scope is unresolved

- Severity: P1
- Evidence:
  - `canonical-memory-store.md`, section 5/9: describes a monotonic commit sequence within the canonical authority.
  - `memory-versioning.md`, section 18: leaves open whether sequence scope is per aggregate or a global commit stream.
- Problem: readers cannot tell whether sequence values are globally comparable across aggregates or only locally ordered.
- Impact: change-feed cursors, outbox watermarks, projection checkpoints, replay ordering and cross-aggregate reconciliation may be implemented incompatibly.
- Owner: D, with storage/recovery architecture owner.
- Dependency: E/F consumers of change feed and projection watermarks.
- Required correction: explicitly choose and define (a) global canonical commit sequence, (b) per-aggregate sequence, or (c) both with separate field names and guarantees. Define gap semantics, ordering, transaction visibility and replay cursor behavior.
- Acceptance: Store and Versioning documents use identical normative terminology; a consumer can unambiguously resume after a cursor and determine whether gaps are meaningful.

#### D-REV-P1-003 — Forget completion needs a closed-world derivative barrier

- Severity: P1
- Evidence:
  - `memory-lifecycle-manager.md`, sections 5, 7, 9 and 12: defines dependency snapshots/watermarks, suppression fences, per-target progress and late-arriving derivatives.
  - `memory-brain-overview.md`, sections 8, 12 and 16: assigns external derivative handling to E/F/G/H/I and describes reauthorization.
- Problem: the documents identify late-arriving derivatives, but do not fully specify the condition that prevents a Forget operation from being marked complete while an old in-flight compiler job, replay, offline adapter or delayed projection can still register a newly visible derivative.
- Impact: a completed Forget could be followed by resurrection or re-exposure from a late derivative.
- Owner: D owns canonical fence/dependency semantics; I owns governance completion policy; E/F/G/H own producer/consumer enforcement.
- Dependency: INT-P0-03 across D/E/F/G/H/I.
- Required correction: define a durable Forget fence/generation; require every derivative-producing or replaying operation to check it before commit/publication; define producer registration/acknowledgement or a stable watermark/barrier; late targets must be suppressed before becoming readable; completion requires all required producers to cross the barrier or an explicit policy-approved residual exception.
- Acceptance: a documented race matrix covers Forget vs concurrent commit, delayed compiler output, outbox replay, index rebuild, Context delivery/retry, offline adapter reconnect and backup restore. No path can re-expose data after suppression; completion proof records barrier/watermark and residual exceptions.

### Dimension 4 — Security, Scope and governance

**Result: CONDITIONAL PASS — integration gate remains open**

Strengths:
- Ownership Scope and applicability Scope are distinct from Permission.
- Actor identity is not trusted from model output/display labels.
- Evidence dereference has independent authorization.
- Scope filtering is required before candidate generation and graph expansion.
- Cross-scope Entity merge is prohibited without explicit grant.
- Memory is untrusted data and cannot gain system/developer instruction or tool authority.
- Forget separates logical suppression from physical deletion and disclaims unilateral deletion from third-party model/provider data.

Open cross-module gates:
- INT-P0-02: I must own policy decisions; D defines resource Scope semantics; E/F/G/H must enforce propagation and negative tests.
- INT-P0-03: I must define retention/backup/external-recipient completion policy; E/F/G/H must provide derivative target discovery and acknowledgement.
- INT-P0-04: end-to-end injection tests remain unexecuted.
- INT-P1-03: authenticated Principal/ActorRef issuer/delegation semantics remain jointly owned with H/I/B.

These are not grounds to claim D has implemented end-to-end security. They are correctly marked integration dependencies.

### Dimension 5 — Performance and resource use

**Result: TO_VALIDATE**

D avoids unsupported latency/throughput promises and identifies the right measurement dimensions: version history, CAS contention, outbox lag, graph fan-out/depth, provenance traversal, Merge/Split migration, Forget dependency discovery, temporal queries and projection rebuild.

No benchmark data exists. Do not convert candidate bounds or design intentions into SLO claims. Benchmark on the target local hardware and representative multi-agent/environment workloads after interfaces stabilize.

### Dimension 6 — Evolvability, observability and operations

**Result: CONDITIONAL PASS**

Strengths:
- Opaque stable IDs, immutable revisions, schema version fields, typed refs, migration records, correlation/causation metadata and structured errors are present.
- Failure scenarios cover duplicate retry, stale writer, projection lag, outbox failure, Merge/Split projection failure and Forget worker crash.

Remaining OPEN items:
- DM-013 vocabulary/schema registry, unknown enum policy and compatibility/migration rules.
- ActorRef issuer/delegation and policy-version semantics.
- Provenance DAG vs explicitly allowed bounded cycles.
- Audit retention vs Forget and non-reconstructive tombstone rules.

---

## 5. Consolidated findings and ownership

| Review ID | Severity | Classification | Owner | Dependency | Required outcome |
|---|---|---|---|---|---|
| REVIEW-SCOPE-001 | Process correction | REVIEW_SCOPE_ERROR | Review coordinator | D branch visibility | Separate main integration readiness from D design quality; retain original report as a historically scoped report |
| D-REV-P1-001 | P1 | REAL_DESIGN_DEFECT | D | I/E/F/G/H | Remove Forgetting/lifecycle vocabulary contradiction |
| D-REV-P1-002 | P1 | REAL_DESIGN_DEFECT | D + storage/recovery owner | E/F | Define global vs per-aggregate sequence and watermark semantics |
| D-REV-P1-003 | P1 | CROSS_MODULE_CONTRACT_GAP | D + I; E/F/G/H implement | INT-P0-03 | Define closed-world Forget barrier and late-derivative race handling |
| D-REV-OPEN-001 | P1 gate | UPSTREAM_UNRESOLVED | Architecture Governance + B | INT-P0-01 | Approve Fact/Claim ADR before schema/API freeze |
| D-REV-OPEN-002 | P1 gate | UPSTREAM_UNRESOLVED | B + I + H, D contributor | DM-005 / INT-P1-03 | Close Scope algebra and trusted ActorRef semantics |
| D-REV-OPEN-003 | P1 gate | CROSS_MODULE_CONTRACT_GAP | D + E/F/G/H/I | INT-P0-02/03 | Define and test derivative registration, suppression and acknowledgement boundaries |
| D-REV-OPEN-004 | P2 | TO_VALIDATE | D + storage/recovery owner | DM-007/DM-013 | Validate provenance cycle policy, schema migration and recovery behavior |

Severity describes the design/integration gate, not an assertion that a runtime vulnerability has been experimentally reproduced.

---

## 6. Cross-module status correction

| Issue | Correct status after D branch inspection |
|---|---|
| INT-P0-01 Fact/Claim | OPEN / ADR-BLOCKED. D proposes a FactRecord option; no schema freeze. |
| INT-P0-02 Scope isolation | D domain contract substantially specified; end-to-end enforcement and negative tests OPEN under I/E/F/G/H. |
| INT-P0-03 Forget | D domain workflow substantially specified; closed-world derivative barrier and completion proof need strengthening; end-to-end policy remains I/E/F/G/H. |
| INT-P0-04 Prompt injection | D data-trust contract specified; cross-system adversarial verification OPEN. |
| INT-P1-01 Context ownership | Correctly G-owned. D supplies exact MemoryVersion refs and invalidation signals; G owns ContextVersion/ChangeSet. |
| INT-P1-02 Claim/Conflict/Merge/Split | Claim revision and ConflictSet remain candidate/ADR-dependent; Entity Merge/Split migration is materially specified. |
| INT-P1-03 Actor identity | OPEN with B/H/I; D consumes typed ActorRef and does not own authentication. |
| INT-P1-06 lifecycle/provenance/typed refs | LifecycleEvent authority is specified; sequence semantics and provenance cycle policy remain OPEN; typed refs are candidate pending B/H/I. |

Do not mark an issue CLOSED merely because D has described its side of the contract. Closure requires the designated owners' agreement and acceptance evidence.

---

## 7. Required remediation order

### D-owned corrections before design sign-off
1. Resolve D-REV-P1-001 in overview and lifecycle documents.
2. Resolve D-REV-P1-002 in Store and Versioning documents.
3. Strengthen D-REV-P1-003 with a concrete fence/barrier/late-derivative protocol and race matrix.
4. Recheck all five documents for consistent terminology and ownership after edits.

### Joint decisions before cross-module contract freeze
1. Architecture Governance + B: INT-P0-01 Fact/Claim ADR.
2. B + I + H: Scope algebra and trusted ActorRef/Principal boundary.
3. D + I + E/F/G/H: Forget fence, derivative registration, acknowledgements and completion proof.
4. D + B: provenance DAG/cycle policy and vocabulary/schema compatibility.

### Re-review exit criteria
- No unresolved D-owned P1 contradictions.
- INT-P0-01 remains explicitly ADR-blocked unless formally decided.
- INT-P0-02/03/04 are not falsely marked closed by D-only text; integration owners provide enforcement/test evidence.
- Store/Versioning/ Lifecycle documents agree on commit sequence, lifecycle authority and Forget state semantics.
- No claim of runtime, security or performance validation without actual test evidence.

---

## 8. Final verdict

**D design: CONDITIONAL PASS as a candidate architecture specification.**

**D main integration: NOT YET PASSED.** The reviewed D branch is not yet part of the shared `main` baseline, and downstream modules must not silently assume its candidate contracts are frozen.

**Original review: RETAIN, BUT RECLASSIFY.** It remains an accurate report of missing D files on its declared `main` review baseline. Its FAIL must not be used as a design-quality verdict on the separate D branch.

No D source file, governance baseline, other module document, original review report, or branch ref was modified by this reassessment. This report is an additional correction record only.
