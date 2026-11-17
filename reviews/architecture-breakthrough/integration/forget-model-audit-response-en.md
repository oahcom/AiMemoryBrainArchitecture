# ABR-INTEGRATION-006 — Forget Model Audit Remediation & Two-Operation Extension

- Review ID: ABR-INTEGRATION-006
- Related model audit: ABR-INTEGRATION-005 (follow-up review artifact on the PR #93 branch)
- Scope: M-01/M-02 corrections in the single-operation cross-owner model; bounded two-operation extension for M-03; M-04/M-05 remain open.
- CI: run [44141001299](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44141001299), SUCCESS, tested commit `33db9554bb2b9a6aecdfabf16250c98dc88e272b`.

## 1. Results summary

| Item | Current result | Disposition |
|---|---|---|
| Single-operation model | 28,383 state/depth pairs, max depth 14, 13 weakened-guard mutants, 15 unittest cases | BOUNDED PASS |
| Two-operation model | 2,425 state/depth pairs, max depth 12, 5 mutants, 7 unittest cases | BOUNDED PASS |
| Combined CI | Both model scripts and both unittest suites pass | SUCCESS |
| M-01 | `global_complete` renamed to `core_barrier_ready`, explicitly not I GlobalForget Completed | CLOSED within model scope |
| M-02 | External durable no-publication proof input added; no proof means no terminalization; stale Worker cannot revive | CLOSED within model scope; Owner contract OPEN |
| M-03 | Two overlapping operations, shared target, independent generation/barrier/receipt, late-target reopen | Partially covered; bounded two-operation model only |
| M-04 | Real durable participants / prepared transactions / crash cut points | OPEN |
| M-05 | Safety versus liveness/fairness and progress assumptions | OPEN |

## 2. M-01 — Preventing an overclaim of Global Forget Completed

The single-operation model renamed the state/action to `core_barrier_ready` / `mark_core_barrier_ready`. It means only that the D/I core-barrier conditions in this finite abstraction hold. It does not mean:
- I ProducerDomainInventoryEpoch is sealed;
- all mandatory E/F/G/H targets are confirmed;
- external recipients / Backup / Restore / Physical Erasure are complete;
- I's typed evidence vector is satisfied;
- I `Completed` / `CompletedWithPolicyException` has been reached.

M-01's naming/scope ambiguity is closed within the current model. I Global Forget Completed remains unmodeled and unproven.

## 3. M-02 — External terminal proof for registered-but-never-started work

The model adds an abstract `record_no_publication_proof` input. It is accepted only after Fence installation, for a registered but never-run WorkItem, with no lease, no I participant and no visible Artifact. Only then may the model terminalize the item and close the barrier.

The model also adds:
- `cancel_without_proof` mutant: terminalization without proof, producing a counterexample;
- `stale_worker_after_cancel` mutant: an old Worker resumes after cancellation proof, producing a counterexample;
- corresponding invariants and regression tests.

**Important:** this is an abstract external-authority evidence input, not a new Cancel API invented or approved by this session. E Cancelled/Rejected remains CANDIDATE; the exact E→D terminal-ack schema/reconciliation, D barrier receipt, Storage no-publish participant and late-worker-fencing contracts remain OPEN. D/E/Storage must define the exact contract first; model pass is not Owner acceptance.

## 4. M-03 — Two-operation overlap model

A separate `overlapping_forget_model.py` models two overlapping Forget operations with intersecting target sets:
- Operation 1 targets: `{a, shared}`
- Operation 2 targets: `{shared, b}`
- both allocate distinct operation generations from the same D-local durable generation counter;
- each has an independent terminal-evidence namespace, barrier and receipt generation;
- the shared target requires terminal evidence under each operation identity;
- late target discovery creates a successor generation for only the affected operation, reopens only that barrier and makes its prior receipt non-current.

No invariant violation was found in 2,425 state/depth pairs. Five weakened-guard mutants produce shortest counterexamples:
1. generation reuse;
2. one operation closing the other's barrier;
3. cross-operation reuse of shared-target evidence;
4. late target failing to reopen its barrier;
5. one operation's receipt incorrectly closing the other's barrier.

This advances M-03 from “not covered” to “bounded evidence for two-operation composition properties”. It does not prove arbitrary numbers of overlapping Forget requests, arbitrary target DAGs, multiple concurrent Producers/Workers, cross-Scope behavior or physical recovery.

## 5. Reproducible CI

[GitHub Actions run 44141001299](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44141001299) at commit `33db9554...` executed:
- single-operation model: 28,383 state/depth pairs, 13 mutants;
- single-operation unittest: 15 tests, PASS;
- two-operation model: 2,425 state/depth pairs, 5 mutants;
- two-operation unittest: 7 tests, PASS.

Historical failed run `44139591931` resulted from the stale expected state count after adding transitions. Later run `44140051181` and current combined run `44141001299` pass. The historical failure is retained, not deleted or hidden.

## 6. Prohibited inferences

- The two-operation finite model is not an unbounded concurrency proof.
- The model generation counter is not a universal numeric clock across Owner namespaces; it expresses only D-local generation monotonicity.
- Two-operation barrier closure is not I Global Forget Completed.
- The abstract no-publication proof is not evidence that a real D terminal receipt, Storage durable participant or stale-worker fencing has been implemented.
- CI PASS is not real DB/WAL/MVCC/2PC, HA/PITR, split-brain, crash/restart or physical-erasure acceptance.
- M-04/M-05, JF-10 and Global Forget typed completion remain OPEN / NOT PROVEN.

## 7. Next steps

1. D/E/Storage: define the exact schema, authority, same-WorkItemId idempotency, participant closure and stale-worker rejection for pre-execution Cancelled/Rejected → durable D terminal receipt.
2. I: define inventory epoch, target set, reopen and Global completion evidence joins for overlapping Forget operations.
3. Storage/D/I: include every real prepare/commit/visibility/receipt/authority-closure durable boundary in a crash-cut matrix.
4. A: after Owner contracts land, extend the multi-operation model to more targets, late lineage and concurrent events; model M-05 separately.

This is a bounded-model research deliverable, not Owner sign-off, does not close any Issue #43 Gate, and authorizes no production implementation or deployment.
