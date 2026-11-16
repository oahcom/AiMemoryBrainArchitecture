# Context Optimization — Owner Decision and Dependency Register

- Owner: A — Principal Integration Architect
- Branch: session-a-integration-2026-11-16
- Status: A decision record; cross-owner acceptances pending unless exact-version evidence is recorded.
- Silence, branch existence or acceptance of a different artifact is not acceptance.

## 1. Decision register

| Decision ID | Decision | Status | Responsible Owner | Required Acceptors | Dependency | Evidence | Blocking Condition | Next Action |
|---|---|---|---|---|---|---|---|---|
| A-CO-001 | F owns Runtime Archive capture, immutable revisions, metadata catalog and bounded Recall | DECIDED conceptually / CONDITIONAL contract | F | D, I, G | D producer inventory; I retention/authorization | F report SHA cea136cbfba6629c8b04bce4855febb1c988161c; candidate SHA 0b5c5b02c5b318c79606328ef1c22d686b8fc8b3 | No F/D/I class/target acceptance | F submits lifecycle/target classification; D/I accept |
| A-CO-002 | G owns Context selection, ContextObservationReference, TSS, ContextVersion and compaction | DECIDED boundary / CONDITIONAL additions | G | B, C, D, F | typed refs, epistemic rules, source lineage | G report SHA 3fb9f011e24c93a748442018d48c5954584e4f43; candidate SHA eadefd4e0fe541ef8479a030a2a99a0d57dbcf8b | no cross-owner addendum | G publishes addendum |
| A-CO-003 | F/G Recall Contract; locator and Context ref distinct | CONDITIONAL | F/G jointly | B, H, I, D | auth intent, source revision, completeness | F candidate §§5–14; A contract candidates | no same-version acceptance | F/G create joint revision and accept |
| A-CO-004 | Locator/cursor are not authorization | DECIDED | I/F/H | B, G, C | principal/scope/PermissionEpoch | F candidate; I trust-chain contract | any implementation treats as grant | add negative tests and errors |
| A-CO-005 | TSS is G Context projection, not Canonical Memory/private Agent state/CoT | CONDITIONAL | G | B, C, D, I | task identity, epistemic status, lineage/scope | G report/candidates | no B/C/D acceptance | G submits exact TSS semantics |
| A-CO-006 | Dynamic cost-aware boundary compaction | CONDITIONAL | G | C, H, F | request/cache/recall/recovery telemetry | G research | no project calibration/held-out results | G defines decision record; C/H/F telemetry |
| A-CO-007 | Six-axis fidelity validator with hard vetoes | CONDITIONAL | G | B, D, F, I | epistemic/temporal/provenance/scope/Forget | G candidates | axes/thresholds unaccepted | G/B define vetoes and negative suite |
| A-CO-008 | Compaction Lineage/Loss Ledger | CONDITIONAL | G | D, I, F | transitive lineage and audit retention | G candidates; D Forget contract | derivative inventory open | D/G/I decide registration/retention |
| A-CO-009 | ReadReceipt/Archive refs may be evidence-chain components | CONDITIONAL | F/G | B, D, I, H | exact range/hash, receipt semantics | F candidates | receipt mistaken for truth/grant/Applied | F/G/B define semantics |
| A-CO-010 | F logical metadata catalog distinct from E Canonical Index | DECIDED | F | E, D, I | namespace, lineage, suppression | F report; D cursor contract | catalog bypasses canonical gate | F/E/D confirm separation |
| A-CO-011 | SAC as independent experiment only | DECIDED; default REJECTED | G/C | A, C, H | task-class validation | G report | SAC becomes default execution | prohibit default; selected stress subset |
| A-CO-012 | No independent Observation Service now | REJECTED | A | F, G, I, Storage | measured need before revisit | invariant I-21 | service split without workload case | keep logical F capability |
| A-CO-013 | No automatic vectorization of all observations | REJECTED | F | I, D, G | measured benefit and policy opt-in | F report | all-content embeddings without policy | structured/full-text first |
| A-CO-014 | Action Fusion outside G/F | REJECTED | C/Agent Runtime | A, C | action execution semantics | G report | G/F claims execution authority | separate Agent/Runtime review |
| A-CO-015 | Semantic interface design may proceed; freeze not authorized | CONDITIONAL | A | B–I, Storage | owner acceptances and P0 closure | A system contract candidates | schema labelled frozen prematurely | request owner decisions |
| A-CO-016 | Rust implementation not authorized | BLOCKED | A | B–I, Storage | frozen contract; Forget/recovery proof; tests | A review; JF-10 binding record | P0-01..04 open | close P0 and rerun gate |

## 2. Required Owner acceptances

Each Owner responds on its own branch; no cross-branch edits or merges are authorized by this register.

| Owner | Exact acceptance requested | Files/revisions | Minimum decision |
|---|---|---|---|
| B | typed ArchiveObjectRef/ContextObservationReference, Scope, time and epistemic preservation | A system contract candidates; G candidate SHA eadefd4e0fe541ef8479a030a2a99a0d57dbcf8b | accept/reject vocabulary and invariants |
| C | TSS not private Agent state/CoT; final request evidence binds ContextVersion and Archive lineage; request/cache telemetry | A candidates; 07-agent-integration/inference-boundary-model.md SHA 56b9e2e51804f8977797851a2cc41b6ebb7f2338 | confirm boundary and evidence |
| D | F producer classes and G derivative inventory; ForgetFence/dependency registration | 03-memory-brain/forget-fence-and-completion-contract.md SHA 1f0391bc49d007c44ec74165bd33d37412cc7990; commit cursor semantics SHA 4688a0ca487bf4d853c7f0220408abe8d743d159 | classify runtime-only vs canonical-derived; gate |
| E | F catalog not Canonical Index; canonical derivatives through D/E final gate | 04-memory-compiler/forget-fence-and-derived-registration.md SHA 00e37ba56596e710513c8d0568acd79141d9101b | confirm boundary and replay tests |
| F | Archive lifecycle, Recall session/cursor/receipt, completeness/cache/suppression | F report SHA cea136cbfba6629c8b04bce4855febb1c988161c; candidate SHA 0b5c5b02c5b318c79606328ef1c22d686b8fc8b3; A contract | accept/modify F responsibility and add D/I proof |
| G | Context ref, TSS, compaction, fidelity, lineage/loss and invalidation | G report SHA 3fb9f011e24c93a748442018d48c5954584e4f43; candidate SHA eadefd4e0fe541ef8479a030a2a99a0d57dbcf8b; A contract | accept/modify G semantics and preserve version authority |
| H | BMCP Recall envelope/errors/cancellation, typed refs, reconnect/no bearer tokens | 08-bmcp-protocol/forget-revocation-and-reconnect.md SHA 695909360782987781e259187041618f495f1c8c; A contract | define wire mapping and exact schema acceptance |
| I | Principal/Scope/PermissionEpoch, Archive class/retention/inventory/revocation/restore | I trust-chain artifact on current I branch; A contract | decide policy, revocation freshness and offline limits |
| Storage | atomic Archive publication, backup/restore/PITR fence replay | A contract and D/E contracts | physical assumptions and executable recovery proof |

## 3. Acceptance protocol

1. A publishes documents on A branch only.
2. Each Owner reads exact A commit and Blob SHA.
3. Each Owner records ACCEPT, ACCEPT WITH CONDITIONS or REJECT on its own branch with rationale and exact A SHA.
4. Multi-owner contracts require all named approvals on the same version.
5. A re-queries all heads and file SHAs, reconciles objections and publishes a new revision if needed.
6. Only after P0 closure and relevant acceptances may A consider interface freeze. Rust implementation requires a separate gate.
7. No merge is authorized here.

## 4. Current global disposition

System architecture pattern DECIDED. F/G contract freeze NOT APPROVED. D/I Forget and authorization integration BLOCKED. H/C transport and Applied binding CONDITIONAL / NOT FROZEN. Rust implementation BLOCKED. Production activation NOT AUTHORIZED.
