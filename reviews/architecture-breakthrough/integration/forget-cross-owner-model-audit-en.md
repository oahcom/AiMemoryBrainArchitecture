# ABR-INTEGRATION-005 — Independent Review of the Forget Cross-Owner Bounded Model

- Review ID: ABR-INTEGRATION-005
- Model: reviews/architecture-breakthrough/integration/model/forget_cross_owner_model.py
- Model Blob: d45807b0b165e53aa6e92d211c221cc93b46ca60
- Test Blob: 64ee823eb1d3d81e020e73ef97817208326f42b5
- README Blob: c7dc620b3486e496de1792147cbf441a51cb3af0
- Historical CI: run 44136327645, SUCCESS at exact tested commit 89a680bbad7246952d51c61c137b0c3611f52a06. This is not a CI claim for the later report commit.
- D source: session-d-memory-brain-2026-11-16 / 03-memory-brain/forget-fence-operation-and-publication-gate.md, Blob 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5
- I source: session-i-security-governance-2026-11-16 / 09-security-governance/global-forget-target-inventory-and-completion-evidence.md, Blob 9100061fa986fb6676656169de3fcf9fc1c72664
- Storage source: session-storage-consistency-forget-atomicity-2026-11-16 / reviews/storage-consistency/phase-3.7-storage-atomic-producer-registration-dependency-visibility-realization.md, Blob 2ab899ee37a18ae6c8f2f64dbb82ad6499842060

## 1. Disposition

The cross-owner model materially improves on Session A's single-work-item abstraction. It explicitly covers D Admission/Fence High-water, E Work/Attempt/Lease/Dependency, I PermissionEpoch and revocation ordering, Storage Visibility, F Read Disclosure, Inventory Gap, Restore High-water and Lost-ACK Receipt Replay. The model and regression suite have a recorded bounded CI PASS: 27,472 state/depth pairs through depth 14, with 11 weakened-guard mutants producing counterexamples.

**Disposition: ACCEPT AS A BOUNDED RESEARCH MODEL WITH CONDITIONS; NOT A SYSTEM-WIDE FORGET PROOF.**

Three material gaps must be resolved before the current global_complete state is used as architecture acceptance evidence.

### M-01 — Global completion abstraction overclaims

The complete_global transition checks only Fence, barrier, inventory_complete and absence of an open I participant. It does not check I's full typed evidence vector, target cleanup, F/G/H consumer suppression, external-copy disposition, backup/restore safety, physical-erasure evidence or PolicyException validity.

I's current Global Forget contract requires all mandatory targets/components to be Confirmed, no unresolved Unknown/Failed, restore safety and required physical-erasure evidence. The model README correctly discloses several of these as not modeled, but the global_complete name can be mistaken for I's Completed state.

**Required:** Rename it to an explicitly scoped predicate such as core_barrier_ready, or model I's full typed evidence vector, CompletedWithPolicyException, Failed, Reopened and evidence invalidation.

### M-02 — No normal terminal path for registered-but-never-started work

A valid prefix exists in which a WorkItem is durably registered and then fenced before any run or I participant exists.

In that state:
- terminalize rejects because i_decision is NONE;
- resolve_no_publication rejects because no I participant is open;
- close_barrier rejects because the WorkItem is not TERMINAL;
- the only modeled way to set REVOCATION_WON is an actual revoke action, which must not be fabricated merely to clear work.

**Required:** D/E/Storage must define and authorize a durable cancel_before_execution / no_publication_proof, including identity, idempotency and stale-worker fencing. A may model it only after the Owner contract exists. Alternatively, explicitly state that the barrier remains open until an external authoritative terminal proof arrives and model that input.

This is a liveness/recovery gap, not a discovered safety-invariant counterexample. Do not weaken fail-closed behavior to fix it.

### M-03 — Only one Fence generation is modeled

install_fence rejects a second Fence. The model does not explore overlapping Forget operations, multiple target sets, maximum applicable generation, per-operation barriers, late-discovered lineage or independent reconciliation.

The README already excludes overlapping targets. Therefore this run proves nothing about multi-Forget composition or monotonicity.

## 2. What the model does support

Within its declared abstraction and assumptions, it provides useful evidence for:
- Admission-first versus Fence-first ordering;
- Publication-first versus Fence-first ordering;
- I COMMIT_WON versus revocation-first;
- Dependency Registration as a precondition for Visibility;
- UNKNOWN I participant blocking barrier closure;
- DLQ not being terminal;
- Inventory Gap reopening a previously closed barrier;
- final Read Gate blocking stale-cache disclosure;
- Restore requiring replay of the modeled D-local Fence High-water;
- Lost ACK not rolling back a durable receipt;
- shortest counterexamples for 11 deliberately weakened guards.

The stale_cache negative control is valuable: stale cache bytes alone are not disclosure if the final Read Gate blocks them. The stale_cache_disclosure mutant demonstrates the actual forbidden read after Fence/revocation.

## 3. Comparison with live Owner contracts

### D terminality / barrier

The live D contract requires timeout, lost ACK, expired lease, missing receipt, registry gap, DLQ state or unavailable current Fence/Permission to remain unresolved and block barrier closure. Every output must have a durable published receipt or a durable suppressed/quarantined disposition that cannot later publish. All dependency/publication operations must be resolved; no retry, DLQ replay, delayed worker, outbox or staged publisher may still publish; no unknown ACK/participant or inventory gap may remain. Only then may D commit its terminal receipt and close the barrier item.

The model captures many of these conditions but has no normal terminal proof for a registered item that never starts. M-02 is a missing transition/authority input, not a request to weaken fail-closed behavior.

### I global completion

The live I contract distinguishes the D per-operation work-item barrier, I ProducerDomainInventoryEpoch/sealed producer-recipient inventory, and per-target evidence for E/F/G/H, external copies, backup/restore and physical erasure. Its state machine includes CompletionEvaluated, Completed, CompletedWithPolicyException, Failed and Reopened.

I prohibits Completed while a D barrier is open, a lease is unresolved, inventory is incomplete, required E/F/G/H evidence is missing/stale, delivery is pending, Adapter state is Unknown, external recipients lack ACK/exception, restore is unsafe, or required physical-erasure evidence is absent.

The model's inventory_complete Boolean is not an I Inventory Seal, and global_complete is not I's Completed. The scope boundary must be explicit in naming.

### Storage / JF-10

The Storage contract requires distinct D and I participants bound to the same Storage Visibility Participant and PublicationOperationId/digest. UNKNOWN keeps both authority barriers open and the artifact private. The current model abstracts I/Storage outcomes but does not model actual prepared transaction IDs, WAL/MVCC/2PC recovery, independent D/I/Storage durable ledgers, or crash injection at every prepare/commit boundary. It cannot close JF-10.

## 4. Required model work

| ID | Required change | Owner | Acceptance evidence |
|---|---|---|---|
| M-01 | Rename global_complete to a scoped core predicate, or add I typed evidence vector, CompletedWithPolicyException, Failed, Reopened and evidence invalidation | A models; I owns semantics | Any missing/Unknown/stale mandatory component blocks I Completed |
| M-02 | Add pre-execution cancel/no-publication proof with authority, durable identity, idempotency and late-worker fencing | D/E/Storage; A models only after contract | Registered → fenced → never started → durable no-publication terminal proof → barrier closure; stale worker cannot publish |
| M-03 | Model at least two overlapping Forget operations, target/lineage sets, independent barriers and maximum applicable D generation | D/I; A models | Permutation tests prove one operation cannot lower/erase another's Fence or completion obligations |
| M-04 | Add crash cut points around Registration, Dependency Commit, D participant admission, I receipt consume, Storage prepare/visibility commit, outcome propagation and D/I closure | Storage/D/I | Crash/restart matrix; UNKNOWN remains private and barriers open until exact participant resolution |
| M-05 | Separate liveness/fairness from safety invariants; define which transitions require external Owner responses and which may remain blocked indefinitely | D/E/I/Storage | Explicit progress assumptions and bounded deadlock/recovery tests; fairness must never turn UNKNOWN into success |

## 5. Interpretation

- Existing bounded CI PASS: **VALID ONLY FOR THAT EXACT MODEL AND TEST SUITE**.
- Session A's 606 state/depth-pair model: a useful smaller historical abstraction; expanded for selected cross-owner cases by this model, not invalidated.
- Cross-owner model: **CONDITIONAL RESEARCH EVIDENCE**.
- D/E/I/Storage contract composition: **PARTIALLY MODELED; OWNER ACCEPTANCE AND PHYSICAL REALIZATION OPEN**.
- JF-10 / physical crash atomicity: **NOT PROVEN**.
- Global Forget completion: **NOT SUFFICIENTLY MODELED; NOT PROVEN**.
- Architecture freeze: **NOT READY**.

Keep the existing model and historical CI record. Before a Gate relies on it, address M-01, obtain D/E/Storage authority for M-02, add M-03 multi-operation tests, keep M-04 assigned to Storage/D/I physical validation, and review M-05 separately.

This report is a same-session audit of the integration model, not independent D/E/I/Storage Owner approval. It changes no Owner authority contract and authorizes no implementation, merge, deployment or production activation.


## M-02 exact Owner-contract refinement (subsequent source read)

After reading the current E source, M-02 must be narrowed. It would be inaccurate to say that Owner documents contain no no-publication terminal semantics:

- Current E source Blob: `00e37ba56596e710513c8d0568acd79141d9101b`. Its status is explicitly **CANDIDATE E enforcement contract**; D/E/Storage atomic registration and final publication gate are OPEN/BLOCKING.
- E §3.2 defines `Cancelled / Rejected` as a durable terminal disposition with no publication possible and a recorded cancellation/suppression reason; D receives terminal evidence.
- E §7's Producer terminal acknowledgement remains **OPEN — D response schema + reconciliation semantics**.
- Current D source Blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` §3.5/state machine requires suppression/quarantine to terminalize only with durable no-publication evidence and proof that no attempt can later publish.
- D §3.5 requires terminal disposition to commit durably in the D barrier ledger; lease expiry, queue deletion, worker shutdown and DLQ parking are not terminal.

The precise M-02 finding is therefore: **E has candidate Cancelled/Rejected semantics and D has a durable no-publication terminality requirement; however, the exact receipt/schema/authority mapping, authority to trigger pre-execution cancellation, same-WorkItemId idempotency, late-worker fencing and D barrier-ledger linearization remain OPEN.** The current model has no transition mapping this candidate E state into an accepted D terminal receipt. A must not promote E's candidate semantics into D acceptance.

Remediation: E Owner confirms the complete evidence emitted by pre-execution Cancelled/Rejected; D Owner confirms how it becomes a D terminal disposition; Storage confirms no publish-capable participant/outbox remains. Only then should A add the exact contract to the model and test registered → fenced → cancelled-before-run → durable D terminal receipt → barrier closure, including stale-worker rejection.
