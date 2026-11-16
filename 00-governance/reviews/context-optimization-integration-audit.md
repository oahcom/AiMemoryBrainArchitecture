# Context Optimization & Observation Archive — Unified Integration Audit

- Audit ID: P-CONTEXT-ARCHIVE-INTEGRATION-001
- Date: 2026-11-17
- Prepared by: Session P coordinator
- Status: **ARCHITECTURE DIRECTION ACCEPTED AS CANDIDATE; F/G INTERFACE AND CROSS-OWNER CONTRACTS NOT FROZEN**
- Scope: Reconcile NVIDIA research, F/G proposals, A system integration review, TAB-001 constraints and conformance plan. This is not an Owner decision or implementation certification.

## 1. Executive disposition

A's system integration review chooses the right high-level split:

> **F owns a Runtime Observation Archive and exact selective Recall. G owns Context selection, TSS, compaction, fidelity and ContextVersion. They communicate through a read-only, revision-pinned Recall contract.**

This is a logical ownership boundary, not a new independent microservice, database or crate. A explicitly rejects a second Context system, G-owned Archive storage, F-owned Context decisions, automatic embedding of all observations, summary-as-canonical-truth, fixed SoL-Pi economic defaults, SAC as default runtime policy and Action Fusion in G/F.

This is directionally compatible with TAB-001's local-first Rust modular monolith and existing D/E/F/G/H/I authority split. It is **not yet a frozen cross-module contract**:
- F Archive/Recall interface candidates remain PROPOSED / NOT_IMPLEMENTED.
- G Context/TSS/compaction/fidelity candidates remain PROPOSED / conditional.
- A's decision register marks the F/G Recall contract and several dependent decisions CONDITIONAL.
- Exact cross-owner acceptances are pending.
- A's conformance plan is PROPOSED / NOT RUN.
- Forget/authorization/restore P0s block implementation and exposure.

## 2. Exact source pins

### 2.1 A system integration

| Artifact | Branch | Blob |
|---|---|---|
| NVIDIA Context Optimization — System Integration Review | `session-a-integration-2026-11-16` | `b53db1ecb7830a7f1057d09c8ef73aceab942cea` |
| Context Optimization — System Contract Candidates | same | `55257bdf85a56a78df96b797b063bc49d91f5a6d` |
| Context Optimization — Owner Decision and Dependency Register | same | `36581cf286ddf2516f571eb823fddc9cf8707d80` |
| Context Optimization — System Conformance Plan | same | `1c941c3e55be1e539a76ef89f297c168296c7db2` |

A current branch HEAD at review: `6caa6034c92c4d3dcf7b2d34ca899b62c3756f1f`.

### 2.2 F/G research and candidates

| Owner | Artifact | Branch HEAD | Blob |
|---|---|---|---|
| F | NVIDIA Observation Archive, Selective Recall & Retrieval Optimization — Impact Assessment | `714fe628fdcfe62b5e6ea901810b779c58ddddb3` | `cea136cbfba6629c8b04bce4855febb1c988161c` |
| F | Observation Archive Interface Candidates | same | `0b5c5b02c5b318c79606328ef1c22d686b8fc8b3` |
| G | NVIDIA Context Optimization Impact Assessment | `72a8066b4401f9586fe10775d545384b82736f07` | `3fb9f011e24c93a748442018d48c5954584e4f43` |
| G | Context Optimization Implementation Candidates | same | `eadefd4e0fe541ef8479a030a2a99a0d57dbcf8b` |

All F/G research and candidate artifacts explicitly remain PROPOSED / NOT_IMPLEMENTED. Their existence does not authorize implementation or freeze.

### 2.3 Relevant owner technology reviews

- B report blob `473c9bb1b8d010e9e20c16975864be7b2daa3253`, current B branch HEAD `13613ed38965c4961d6eed5eca7c91d31e455f9c`.
- I report blob `3558856fcc109efc6ed1cda3a53ac7900a89fd31`, current I branch HEAD `cdfaf4ebdef3f5cbe6d5a0d2229122930212377c`.
- Both reports explicitly state their execution mode is centralized delegated review by the project integration assistant, not independent human-Owner attestation. Their technical analysis is useful review evidence, but does not substitute for Owner decisions.

## 3. Research interpretation — mechanisms, not copy/paste

### 3.1 NVIDIA long-context paper

F's analysis separates long-horizon interaction history from long-input source material and distinguishes:
- FHA: full-history accumulation; useful as a retained source history where policy permits, but not as the default active inference context.
- EoCC: end-of-conversation compaction; adapt as a G-owned Context operation, with F preserving source references and exact recall.
- SAC: single-action compaction; task-harness option only, not a default F/G or Agent policy.
- Selective Input Reading: adopt as a strong pattern—immutable source preservation plus bounded exact page/range recall.
- SSSM/semantic state: research only; do not create a new authority type or bypass G's Context ownership.

The paper's benchmark results are workload/model/hardware-specific. They do not prove AiMemoryBrain accuracy, cost or latency. Numeric thresholds and cost claims must not be imported as production constants.

### 3.2 NVlabs/SoL-Pi

F distinguishes three mechanisms:
- ObservationPack: adapt stable handles, previews and exact paged recall while preserving raw source bytes and session history.
- Evidence-Preserving Reducer: optionally adapt deterministic quote/hash validation and original-source fallback. A reducer receipt is not truth, Canonical Memory or a Context Version.
- Online Context Compact: G-only adaptation. F may expose recall/cost/working-set signals; G decides compaction and ContextVersion.
- Action Fusion: out of scope for F/G; its local serialization/hash check is not a global cross-module transaction.

Important evidence limitation: F reviewed official project documentation, configuration, compatibility/security material and visible issue/PR history, but states it could not directly checkout/execute the SoL-Pi repository source/tests in this session. It does not claim to have independently run SoL-Pi CI. That limitation is correctly disclosed.

## 4. Ownership and data model boundaries

### F — Runtime Archive / Recall

F's proposed responsibilities:
- immutable ArchiveObject bytes/revisions, content hash and source revision;
- ArchiveObjectManifest, ArchiveLocator and metadata catalog;
- structured, lexical and temporal indexes; ANN only for selected, policy-approved chunks where measured semantic retrieval is useful;
- RecallSession, ReadCursor, ReadReceipt, ReadBudget and CompletenessMetadata;
- exact byte/page/range selectors, explicit coordinate system and EOF;
- integrity/freshness checks, cache/Working Set, quotas and backpressure;
- F-local suppression and cursor/cache invalidation.

F must not create G Context entries/versions, decide semantic truth, promote observations to Canonical Memory or declare I/D Forget complete.

### G — Context / TSS / Compaction

G's proposed responsibilities:
- ContextObservationReference, Context Entry selection and membership;
- typed, versioned TSS as a Context projection, not Canonical Memory, Agent private state or hidden reasoning;
- ContextVersion, ChangeSet, Snapshot/Delta and delivery coordination;
- boundary-triggered, cost-aware compaction decisions;
- six-axis fidelity checks: goal/progress, constraints/negative conditions, epistemic/fact status, temporal order, provenance/recoverability, Scope/Permission/Forget;
- hard vetoes that override any aggregate fidelity score;
- immutable compaction decision, fidelity report, ContextVersion linkage and lineage/loss ledger.

G must not own raw Archive storage or infer Applied/semantic truth from an F receipt.

### Cross-object distinction

- `ArchiveLocator`: F-issued locator to one immutable Archive object revision and selector coordinate system.
- `ContextObservationReference`: G-owned Context edge pinning the locator, exact source revision/hash and optional range/ReadReceipt.
- `ReadCursor`: F session-bound read state; not a bearer permission.
- `ReadReceipt`: evidence that F returned exact bytes/ranges; not proof that the model understood, accepted or used them.
- `TSS`: G-owned state projection; not a new canonical memory type.
- `ContextVersion`: G authority; never minted by F.
- `PermissionEpoch`: I namespace; `ForgetFenceGeneration`: D namespace; `IndexWatermark`: F namespace; `ContextVersion`: G namespace. These values are not interchangeable or numerically comparable.

## 5. Security, Forget and recovery invariants

1. **Scope-before-Candidate:** compile trusted Scope predicates before Archive metadata candidates or payload bytes are exposed; never global-search then application-filter.
2. **Revalidate every boundary:** current I permission and D Forget Fence before metadata exposure, object dereference, every page/range, cursor continuation, cache hit/fill publication, final F→G handoff, G Context commit/delivery and C final request boundary as applicable.
3. **Locator/cursor are not authorization:** no bearer grant from an opaque ID, cursor, ReadReceipt, ContextVersion or caller-supplied scope label.
4. **Exact revision binding:** every excerpt binds object ID/revision, stored-byte hash, source revision, selector/range and encoding coordinate system. No silent cursor rebind to changed source.
5. **Completeness is explicit:** budget/deadline/index gaps return PARTIAL/UNKNOWN, never COMPLETE. Top-k or one page does not prove the entire archive was searched. EOF is explicit.
6. **Derived artifacts inherit constraints:** previews, summaries, embeddings, page maps, indexes, caches, snapshots and offline copies inherit source sensitivity, scope, retention and Forget lineage.
7. **Forget during read:** fence/epoch advancement invalidates cursor/session and suppresses all not-yet-disclosed bytes; cancellation alone is not proof. Previously disclosed bytes cannot be retroactively recalled, but future reads/use must be blocked.
8. **Restore quarantine:** no restore-first-clean-later. Reconcile authoritative I/D state and inventory before serving restored Archive/Context/cache/index data.
9. **No optimistic completion:** unknown authority, missing producer registration, incomplete lineage, uncertain storage publication or stale checkpoint remains UNKNOWN/QUARANTINED.

## 6. Cross-owner decision register — current status

A's register currently marks these decisions as follows:

| Decision | Current status | Required acceptors / dependency |
|---|---|---|
| A-CO-001 F Archive lifecycle/catalog/Recall | DECIDED conceptually / CONDITIONAL contract | F, D, I, G |
| A-CO-002 G Context/TSS/ContextVersion/compaction | DECIDED boundary / CONDITIONAL additions | G, B, C, D, F |
| A-CO-003 F/G Recall contract; locator distinct from Context ref | CONDITIONAL | F/G jointly, B/H/I/D |
| A-CO-004 Locator/cursor not authorization | DECIDED | I/F/H with B/G/C conformance |
| A-CO-005 TSS not private Agent state/CoT or Canonical Memory | CONDITIONAL | G, B/C/D/I |
| A-CO-006 Dynamic cost-aware boundary compaction | CONDITIONAL | G, C/H/F telemetry |
| A-CO-007 Six-axis fidelity validator/hard vetoes | CONDITIONAL | G, B/D/F/I |
| A-CO-008 Compaction Lineage/Loss Ledger | CONDITIONAL | G, D/I/F |
| A-CO-009 ReadReceipt/Archive refs in evidence chain | CONDITIONAL | F/G, B/D/I/H |
| A-CO-010 F metadata catalog distinct from E Canonical Index | DECIDED | F, E/D/I |
| A-CO-011 SAC independent experiment only | DECIDED; default REJECTED | G/C/A/H |
| A-CO-012 No independent Observation Service now | REJECTED | A/F/G/I/Storage |
| A-CO-013 No automatic vectorization of all observations | REJECTED | F/I/D/G |
| A-CO-014 Action Fusion outside G/F | REJECTED | C/Agent Runtime |
| A-CO-015 Semantic interface design may proceed; freeze not authorized | CONDITIONAL | B–I and Storage |
| A-CO-016 Rust implementation | BLOCKED | Frozen contract, P0 proof and tests required |

The register says each Owner must record its decision on its own branch; silence or acceptance of another artifact version is not acceptance. F/G joint Recall has no same-version acceptance yet. A's review is an integration proposal, not a substitute.

## 7. Conformance readiness

A's plan (blob `1c941c3e55be1e539a76ef89f297c168296c7db2`) is **PROPOSED / NOT RUN**. It assigns:
- F: Archive capture, immutable manifests, exact reads, cursor/receipt/completeness.
- G: Context selection/version/TSS/compaction/fidelity.
- D/E: canonical registration/publication/Forget.
- I: identity, authorization, revocation and inventory.
- H: BMCP Recall/ACK/reconnect.
- C: final request boundary/protected regions.
- A: test governance and aggregate gates.

The planned suites cover:
- nominal archive capture, multi-page exact recall, source revision rollover, F→G handoff and Context CAS;
- cursor replay/EOF, scope isolation, revoked permissions, tampered blobs, prompt injection, retention expiry, ANN leakage and stale summary;
- Forget × archive capture/read/cache/compaction/delivery/offline reconnect/restore/snapshot-delta;
- crash after blob write or manifest stage, lost invalidation event, concurrent cursor consumers and source revision races;
- fidelity and epistemic preservation;
- paired performance groups from full history through selective archive, compaction and fidelity validation.

Hard gates include zero unauthorized disclosure, zero false completeness, no epistemic upgrade, no critical constraint loss, exact hash verification and no cursor crossing object revision/hash. Performance tests must use fixed tasks/seeds/model/provider/tokenizer/hardware/config, paired comparisons and held-out sets. No AiMemoryBrain performance result exists yet.

## 8. Principal blockers

| ID | Blocker | Owner set | Why it blocks |
|---|---|---|---|
| CO-P0-01 | No joined Forget linearization proof for Archive + Context derivatives | D/F/G/I/H/C/Storage | Cannot prove no post-fence disclosure or stale restore |
| CO-P0-02 | F producer classes and G derivative inventory not accepted | D/F/G/I/E | Unregistered producer/derived artifact can escape target inventory |
| CO-P0-03 | Archive Restore/PITR and stale fence/permission replay architecture not fully specified | I/D/F/Storage | Restored bytes must remain fenced until authoritative control-state reconciliation; implementation tests are engineering-phase evidence |
| CO-P0-04 | JF-10 COC architecture/recovery protocol not yet accepted as one exact version | A/I/D/C/H/Storage; G where Applied semantics affected | Gate B design is authorized but the Storage protocol is still PROPOSED with COC-REV-001..008 open; F/G cross-authority operations cannot freeze against an unaccepted recovery contract |
| CO-P1-01 | F/G Recall wire/data contract not frozen | F/G/B/H/I/D | No common fields/states/errors/idempotency/compatibility |
| CO-P1-02 | TSS epistemic/temporal/type rules not accepted by B/C/D | B/C/D/G | Context may lose constraints or upgrade epistemic status |
| CO-P1-03 | H/C telemetry and final-request binding not accepted | C/H/G/F | Dynamic compaction economics and final request evidence lack common telemetry |
| CO-P1-04 | Retention, classification, external source rights and key ownership unresolved | I/Storage/F/D | Archive retention and deletion cannot be safely authorized |
| CO-P1-05 | Benchmark calibration/held-out validation absent | A/F/G/C/H | No justified thresholds, page sizes, cache policy or ANN eligibility |

## 9. Required next sequence

1. F and G produce one exact joint Recall contract version: ArchiveLocator vs ContextObservationReference, RecallIntent, RecallSession, ReadCursor, ReadReceipt, Completeness, source revision, budget, errors, cancellation, idempotency and final handoff.
2. B confirms typed refs, temporal/epistemic semantics and non-coercion; C confirms TSS/final-request boundary and telemetry; D confirms producer/derivative registration, lineage and fence linearization; E confirms catalog/index separation and canonical derivative gate.
3. H defines exact authenticated BMCP request/response/error/cancel/reconnect wire mapping; I defines class/retention/authorization/revocation/inventory and restore policy; Storage confirms atomic archive publication, encryption/key and backup/restore boundary.
4. Each Owner accepts/rejects the same exact version on its own branch with exceptions and blob SHA.
5. A updates the owner decision register and gate vector. No interface freeze until all required exact-version acceptances and P0 closure.
6. Only after implementation and pinned build exist, run A's conformance plan. Do not treat design approval as implementation/test pass.
7. Run paired benchmark and ablations; choose page size/cache/ANN/compaction thresholds from measured workload, not paper or SoL-Pi defaults.

## 10. Source freshness caveat

A's integration review cites discovery-time Owner refs that are already stale for some branches:
- A's review table still lists B HEAD `861fa9...`, I HEAD `1fc3b...`, Storage HEAD `8b8c...`; current branch heads are B `13613e...`, I `cdfaf4...`, Storage `e6e578...`.
- F and G research source heads remain `714fe6...` and `72a806...` respectively.
- The B/I technology reports are new branch additions after the reviewed source HEADs; both explicitly disclaim independent human-Owner attestation.
- TAB-001 Owner-specific report coverage is now 6/9 (B/C/F/G/H/I present); A/D/E remain missing. A's context integration review is not a substitute for A's assigned TAB-001 Owner technology review.

A should refresh the integration review's source pin table before any freeze. Session P records this discrepancy but does not rewrite A's Owner record.

## 11. Final verdict

- System-level ownership pattern F Archive + G Context: **DECIDED CONCEPTUALLY**.
- Independent Observation Service: **REJECTED for current phase**.
- F/G Recall contract: **CONDITIONAL / NOT FROZEN**.
- TSS, cost-aware compaction, fidelity, lineage/loss: **CONDITIONAL**.
- Cross-owner exact acceptances: **PENDING**.
- Conformance plan: **SPECIFIED / NOT RUN**.
- Rust implementation: **BLOCKED**.
- Production readiness: **NOT AUTHORIZED**.

This audit is a coordinator's synthesis of Owner-authored proposals and delegated review artifacts. It does not make F/G/B/C/D/E/H/I/Storage decisions on their behalf.


## 12. F/G baseline proposal alignment gap

The current F module baseline proposal Blob `d4756cabda3151999cbe1ddde0adb554458004a1` contains none of the new Observation Archive / ArchiveLocator / RecallSession / ReadCursor / ReadReceipt / CompletenessMetadata concepts. The current G module baseline proposal Blob `fb2eb805be385469b5ab5f25c4ef76f234feb4c2` contains none of the new TSS / ContextObservationReference / dynamic compaction / six-axis fidelity / lineage-loss ledger concepts.

This is not a contradiction in an approved baseline because both files are still PROPOSED. It is a required Owner-authored baseline update before any module baseline adoption. UMR-021 tracks this; Session P does not edit F/G Owner branches.



## 13. Gate B COC protocol dependency — current Phase 3.6.3 specification

Storage has published Phase 3.6.3 COC protocol Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25` on current Storage branch HEAD `fe7debe55da71e655eecfc46f25ec49eae43404a`. This is a substantial architecture specification (Raft/quorum, membership epoch, immutable record envelope, participant registry, linearizable APIs, I/D outage gates, recovery batch, checkpoint/PITR/restore and fault matrix), but exact Owner review is pending.

It is a dependency for F/G's cross-authority Recall and Forget lifecycle, not an implementation. Residual exact-review items include the committed recovery-epoch completion event, H record/schema mapping, repeated cutoff batches, I-owned domain registry authority, external anti-rollback anchor custody and the A Applied package companion pin drift. Gate B spec is published; acceptance remains open; Gate C implementation tests are deferred to engineering. Do not treat the presence of this spec as F/G interface acceptance or conformance evidence.

