# A Independent Source Audit — ABR-INTEGRATION-001
# Review ABR-AUDIT-007

- Main baseline: `e52594f181d2edb77448adcfed64a0fbdffaf3aa` (Tree `7096e0bc3fdc9a390fccff388f9261522fa424f2`)
- Integration PR #93 head: `0f3ba5293add8d6147a4375796b04c8bc6ae75e1`
- Research inputs: PR #84 `c6e76b34cbf099d36631b284c9b8a75d778d707f`; PR #85 `c5013d3585d54457f38bef37984645e2055ff7cf`; PR #86 `3892916ce2379f807a0ddcd0039816f6e88ecee1`; PR #88 `bf35b32295d0d3f337c80c3dc406db0a41de6830`.
- Disposition: **APPROVED_WITH_CONDITIONS for research integration accuracy only; NOT an architecture approval.**
- Scope: read-only source-level verification of the integration report against original source code, experiment reports, fixtures and model artifacts.

## 1. Executive result

The core integrated dispositions are supported:
- Forget evidence is bounded logical exploration, not TLC, unbounded proof or production evidence.
- Resource Manager Option B is a conditional fairness candidate with quality/latency trade-offs, not a universal improvement.
- Memory IR is a small synthetic design probe, not production Compiler evidence.
- Overall architecture superiority remains unresolved.
- No Owner sign-off, Gate closure, architecture freeze or production authorization follows.

One reproducibility defect was found in PR #93: the integrated report quotes Resource Manager latency values that do not match the current exact source report pinned in PR #86. PR #93 also omits exact Blob pins for several decisive model/prototype/fixture artifacts from its evidence ledger. These do not overturn the high-level conclusions, but must be corrected before the integration report is treated as an exact reproducible evidence package.

## 2. Exact source pins independently re-read

### Forget / PR #88
| Artifact | Blob |
|---|---|
| Python bounded model `forget-formal-verification/model/forget_model.py` | `8e75f2978a0b85b3f0311ac0a189d40125b8d461` |
| F1–F8 invariant disposition | `14eb422c4ac7763d4682adacacd50b42b34fda6c` |
| Model checking results | `2082e4a547dbe76c319d58bdd75022ccc532b6e2` |
| State machine | `4868832dab421f6d76caf4d3366da68e960abe99` |
| Counterexample catalog | `254ab3c7c467ab9acfcae88ffe1dc92d1045e3aa` |
| Remediation proposals | `9baef6654783182dc825f34a6d35426286541a66` |

### Session 0 / PR #84
| Artifact | Blob |
|---|---|
| TLA+ skeleton `forget-model/ForgetModel.tla` | `8b069efcafaf0d7ab7e42f3c4953ad3f4836cb29` |
| TLC config `forget-model/ForgetModel.cfg` | `0e6e1bf9321a22afd856a4592efb3d23146d0119` |

### Resource Manager / PR #86
| Artifact | Blob |
|---|---|
| Benchmark source `memory-operating-system/prototype.py` | `72b9f493b58cb42791c39cde5a78f2163235002e` |
| Benchmark report `prototype-and-benchmarks.md` | `2053e4de179c80878fbdeee4f4874de5ad04057c` |

### Memory IR / PR #85
| Artifact | Blob |
|---|---|
| Prototype `prototype/memory_ir_prototype.py` | `bd27e93e90aceacf1857ebdf56b97e59ae34eb32` |
| Synthetic input fixture `prototype/sample_experiences.json` | `657268696ed95a481bf2836e9750fd59183d83e3` |
| Prototype README | `f2a293a084942cbc77b7f9025b6e4d442757a56d` |
| Direct-vs-IR report | `087212cb9713d37d91fce8943efaf6d80249b87c` |

The PR #93 evidence ledger currently pins key narrative reports but does not list these underlying executable/source/fixture Blob SHAs. Add them so readers can reproduce the actual evidence rather than relying on report summaries.

## 3. Finding ABR-007-01 — Resource Manager latency mismatch

**Severity:** P1 (reproducibility / evidence accuracy)  
**Owner:** PR #93 integration author; PR #86 experiment author for source clarification  
**Blocking:** YES for declaring the integration evidence ledger exact; NO for the high-level research-only conclusion.

PR #86's current benchmark report Blob `2053e4de...` records:
- Direct Top-K median selection latency: **0.095 ms**
- Rerank + Budget: **0.119 ms**
- Unified RM: **0.306 ms**

PR #93's English integrated report states Direct Top-K **0.099 ms** and Unified RM **0.324 ms**. These values are not the values in the exact current PR #86 report Blob. The integrated report's qualitative statement (approximately 3.3x local prototype latency) remains directionally correct, but the exact values are inconsistent.

Required correction:
1. Use the values from the pinned PR #86 report, or explicitly identify a different benchmark run/source and pin its code, parameters, output and commit.
2. Keep the caveat that this is a single-threaded local Python microbenchmark, not service latency.
3. Preserve the result trade-off: Unified RM has zero starved tasks and the best Jain task-coverage fairness, but lower Recall/Precision/token efficiency and higher local latency than Direct Top-K.
4. Do not call this evidence of production capacity, system-wide efficiency or net product benefit.

## 4. Finding ABR-007-02 — Forget evidence is bounded and guard-dependent

**Severity:** P1 (scope/claim boundary)  
**Owner:** A/Forget research author and PR #93 integration author  
**Blocking:** YES for any formal-proof or production-safety claim; NOT blocking the research-only candidate disposition.

The Python model has one state record with one admission/work item, one Fence generation, one publication, one index/cache projection, one receipt and one restore. Its state counter counts `(State, depth)` pairs, not globally unique semantic states. The model's safe result depends on guards/assumptions encoded in `step()`; the mutants deliberately remove individual guards.

The model's `violates()` predicate checks only the encoded safety conditions. It does not prove liveness, fairness, arbitrary dependency closure, concurrent multi-operation behavior or implementation refinement. The result file correctly labels it bounded abstraction only.

The Session 0 TLA+ module is a separate skeleton. It has finite Producers/Artifacts/Targets and invariants for suppression, register-before-visible, barrier soundness and high-water. Its CFG is present, but neither the report nor repository evidence establishes that TLC was executed. The Restore action sets a model variable from currentControlGeneration; it is not a physical backup/PITR rollback campaign.

Required correction/continuation:
- Keep the exact bounded Python result and TLA+ skeleton evidence separate.
- Do not label either as a TLC pass or production proof.
- Extend the model with multi-producer leases/attempts, DLQ/replay, lost ACK around each durable boundary, multiple overlapping Forget operations, PermissionEpoch, I inventory seal/change, derived dependency DAGs, G/H/F projections, Storage prepared participants, split-brain/failover and restore rollback.
- Add liveness/fairness properties only after the relevant environment/fairness assumptions are explicit.
- Define refinement mapping from model variables/actions to exact D/E/I/Storage/F/G/H Owner contracts and executable tests.

## 5. Finding ABR-007-03 — Memory IR experiment is a five-row synthetic shape probe

**Severity:** P2 (evidence scope)  
**Owner:** C research author / PR #93 integration author  
**Blocking:** NO for candidate/shadow-only classification; YES for claims of production quality, type accuracy or complexity reduction.

The exact fixture has five rows: four well-formed, one missing source_id. It includes two conflicting lives_in values and two other assertions. The prototype uses a deterministic synthetic rule extractor, zero model calls, no entity resolution and no persistent cache. It demonstrates deterministic output, stage-local diagnostics and stable IDs for unaffected rows under one edit. It does not demonstrate LLM extraction quality, semantic correctness, concurrency, durable incremental compilation, crash recovery, Forget/Permission or D Canonical Commit.

The report correctly says the direct baseline is deliberately compact and the experiment is not a statistically valid benchmark. Preserve that qualification; do not interpret the IR's additional metadata as proof of net complexity reduction.

Required next evidence:
- 20–50 approved representative, anonymized or synthetic edge-case fixtures with documented coverage rationale;
- property-based tests for temporal interval boundaries, scope isolation, malformed inputs, provenance graph closure, version migration and invalidation;
- deterministic replay across parser/extractor/IR/transform version changes;
- explicit tests that old Forget/Permission receipts cannot authorize a new derivation;
- shadow comparison inside E with D commit untouched, measuring stage diagnostics, provenance completeness, CPU/memory, cache invalidation and operator burden.

## 6. Integrated conclusion and disposition

The following conclusions remain supported:
- Forget: P0 / NOT READY for production; logical model evidence is bounded and conditional.
- Resource Manager Option B: CANDIDATE / SHADOW ONLY; fairness is a product trade-off, not a free efficiency gain.
- Memory IR: CANDIDATE / SHADOW ONLY inside E; no B Fact/Claim ADR or D Canonical Commit authority change.
- Architecture superiority: UNRESOLVED.
- Issue #43 G1–G8 and existing P0 blockers remain open.

**ABR-AUDIT-007 disposition: APPROVED_WITH_CONDITIONS for research integration accuracy only.** Conditions:
1. Correct the RM latency figures or pin a separate exact run.
2. Add exact Blob pins for Python model, TLA+ skeleton/config, RM prototype/report and IR prototype/fixture/report.
3. Keep bounded model, synthetic benchmark, prototype and physical production evidence in separate evidence classes.
4. Re-read source pins whenever an Owner branch advances.

No Owner contract is amended. No PR is merged, no Gate is released, and no production authorization is granted.
