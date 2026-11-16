# NVIDIA Context Optimization — System Integration Review

- Owner: A — Principal Integration Architect
- Branch: session-a-integration-2026-11-16
- Date: 2026-11-17
- Status: conceptual architecture decisions recorded; cross-owner contract freeze NOT AUTHORIZED; Rust implementation BLOCKED.

## 1. Executive Summary

**Decision:** adopt F-owned Runtime Observation Archive + G-owned Context Projection, connected by a read-only, revision-pinned Recall Contract. Do not create a second Context subsystem or an independent Observation Service in this phase. A logical subsystem boundary does not imply a separate process, database or crate.

F owns immutable observation capture, archive manifests/revisions, exact bounded reads, recall sessions/cursors/receipts, read budgets, integrity, completeness, cache and F-local suppression. G owns Context membership/selection, Task Semantic State (TSS) as a Context projection, ContextVersion, compaction, fidelity validation, lineage/loss accounting, reconciliation and delivery intent. D owns Canonical Memory and canonical Forget fence; E owns canonical-derived registration and publication gate; I owns Principal/Scope/PermissionEpoch/retention/global Forget policy; H owns BMCP and Adapter protocol; C owns inference-boundary evidence and Agent safety boundary; B owns typed domain and epistemic/temporal semantics.

- DECIDED: ownership split; no second Context subsystem; Archive is not Canonical Memory; typed cursor separation; no bearer authorization; no automatic vectorization; SAC not default.
- CONDITIONAL: F/G Recall Contract, TSS, economic compaction, fidelity validator, lineage/loss ledger, Archive evidence references, F metadata catalog and experiments.
- BLOCKED: Forget races/restore proof; contract freeze; Rust implementation; production retention/topology.
- REJECTED: G-owned Archive storage; F-owned Context decisions; new standalone service now; summary-as-canonical-truth; locator/cursor as authorization; fixed SoL-Pi thresholds; automatic all-observation embeddings; SAC default; Action Fusion in G/F.

P0: New F/G mechanisms are not integrated into an executable end-to-end D producer registration + D ForgetFence + I PermissionEpoch + F suppression + G Context invalidation + H reconnect + C final request boundary proof. This blocks implementation and exposure. Unknown authority or terminal state means fail closed/quarantine, never optimistic success.

## 2. Reviewed Evidence and Exact Revisions

### 2.1 Research artifacts

| Owner | Branch HEAD | Artifact | Blob SHA |
|---|---|---|---|
| G | session-g-memory-context @ 72a8066b4401f9586fe10775d545384b82736f07 | reviews/06-memory-context/nvidia-context-optimization-impact-assessment.md | 3fb9f011e24c93a748442018d48c5954584e4f43 |
| G | same | reviews/06-memory-context/context-optimization-implementation-candidates.md | eadefd4e0fe541ef8479a030a2a99a0d57dbcf8b |
| F | session-f-memory-runtime @ 714fe628fdcfe62b5e6ea901810b779c58ddddb3 | reviews/05-memory-runtime/nvidia-observation-recall-impact-assessment.md | cea136cbfba6629c8b04bce4855febb1c988161c |
| F | same | reviews/05-memory-runtime/observation-archive-interface-candidates.md | 0b5c5b02c5b318c79606328ef1c22d686b8fc8b3 |

All four files were fetched directly and their Blob SHAs match the supplied pins. Branch HEAD and Blob SHA are distinct identities.

### 2.2 A baseline files read

| Path | Blob SHA |
|---|---|
| 00-governance/architecture-invariants.md | 66266667bdbb1cf15a2644fa98db5ecaaf3bb23b |
| 01-system-architecture/responsibility-matrix.md | fbeb6935fe874e6c843c25c3a891d6b3242cbfd3 |
| 02-domain-model/scope-and-permission-model.md | b5215ae27bd65a6c89c185b496f730b6cd52efa9 |
| reviews/integration/typed-cursor-and-watermark-contract.md | 8d62c50f87f7cc2150f1f92eadc3f1b2ecc89af3 |
| reviews/integration/phase-3.6-jf10-canonical-authority-deployment-binding-record.md | c54c21321c8a115f3ea4b6bfed19a96cac8ccffe |
| reviews/integration/phase-3.6-context-runtime-applied-joint-architecture.md | 1123fa6231d91fc8c899cd9fae773cbf23e86143 |
| reviews/integration/phase-3.6-final-architecture-acceptance.md | 16f86859645447f3f4397c5c89c6013c3cce92b5 |
| 07-agent-integration/telemetry-model.md | 9bb4a77e4bd79caaf3e1faeaf77c6b42858998f0 |

### 2.3 Live Owner refs queried

| Owner | Branch | HEAD |
|---|---|---|
| A | session-a-integration-2026-11-16 | fb061aee907c28f7da198e68161ff57ebac160b7 |
| B | session-b-domain-model-phase3 | 861fa9b2c3e1f572336543b15c7dc392493891db |
| C | session-c-agent-integration-2026-11-16 | 2e5776029bc4271c33525f04c7d0f0708e4bbae8 |
| D | session-d-memory-brain-2026-11-16 | 9dd48eddb3c8f91d15dfa6981a7f53cc70bd4bf8 |
| E | session-e-memory-compiler-2026-11-16 | 4402549c39824b89a0dc49973226187c62e056c5 |
| F | session-f-memory-runtime | 714fe628fdcfe62b5e6ea901810b779c58ddddb3 |
| G | session-g-memory-context | 72a8066b4401f9586fe10775d545384b82736f07 |
| H | session-h-bmcp-protocol | 242d8ab5da890181e762561bb3d3a662287fb63c |
| I | session-i-security-governance-2026-11-16 | 1fc3b3293ebf2077edfd6ad253647d382173d9fa |
| Storage | session-storage-consistency-forget-atomicity-2026-11-16 | 8b8c749017bf09d6aa01a7d858b48f910ec5b1bd |

These are discovery-time refs, not Owner approvals. Re-query before any freeze. Targeted current Owner files read include D Forget and cursor semantics, E derived registration, I trust-chain, H Forget/reconnect and C inference boundary. No non-A branch was written.

### 2.4 Evidence grades

Artifact existence and exact file identity are verified. Paper claims remain attributed to G/F and are not AiMemoryBrain benchmark results. Prior Phase 3.6 joint record says Applied Contract was not frozen, H same-version approval pending and CFG/PI suites not run. Prior A acceptance explicitly denied baseline freeze and production readiness while JF-10 remained P0 open. This review does not upgrade those states.

## 3. G/F Research Reconciliation

G's contribution is a forward-looking task state projection, compaction at meaningful boundaries under correctness/economic gates, and recoverable evidence lineage. F's contribution is a governed Runtime substrate for immutable observations and bounded exact recall. These are complementary.

Adopt/adapt: boundary-triggered reevaluation, measured economics, TSS, immutable observation storage, bounded exact recall, deterministic receipt verification, six-axis fidelity, explicit lineage and selective rehydration.

Reject as-is: SoL-Pi numeric defaults, automatic summaries as truth, local filesystem security model, all-observation embedding, and Action Fusion in G/F. Exact quote/hash validation is necessary but does not prove semantic completeness, representativeness, freshness, authorization or epistemic correctness.

## 4. Observation Archive Ownership Decision

| Option | Responsibility/authority | Lifecycle and storage | Security/Forget/recovery | Conflict/cost | Decision |
|---|---|---|---|---|---|
| A: all G | G owns raw archive and Context | Couples evidence retention to Context lifecycle; duplicates Runtime read/cache/index | G duplicates F and I/D enforcement | Conflicts with Runtime and Context separation | REJECTED |
| B: all F | F also decides Context selection/version | Runtime becomes Context authority | Conflicts with G ContextVersion and C/H Applied boundary | Duplicated responsibility | REJECTED |
| C: F archive/recall, G Context selection/version | Each owns its artifact and state | F Archive lifecycle; G Context lifecycle | D/I/H/C retain authority | Fits current architecture with least duplication | DECIDED conceptually; contract CONDITIONAL |
| D: independent Observation Service | New authority and service | New storage/index/retention/migration | New Forget participant, principal and recovery path | No measured need; invariant says logical boundary need not mean process | REJECTED now |

F owns ArchiveObjectManifest, immutable bytes/revisions, hash/source revision, locator, metadata catalog, recall sessions/cursors/receipts, budgets, completeness, cache and F-local suppression. G owns ContextObservationReference, selection, TSS, compaction, ContextVersion and reconciliation. G cannot mutate F Archive lifecycle. F cannot mutate Context. D/I govern Forget and retention; E governs canonical publication; H/C govern protocol and applied boundary.

## 5. F/G Interface Contract Review

### 5.1 Object identity

ArchiveLocator and ContextObservationReference are different objects. ArchiveLocator is an F-issued locator to one immutable object revision and selector coordinate system. ContextObservationReference is a G-owned Context edge pinning the locator, exact source revision/hash and optional range/ReadReceipt. It may contain an excerpt only when the excerpt is bound to exact bytes, range and source revision/hash.

RecallIntent is a formal G→F request candidate. Authenticated actor and trusted scope are resolved by H/I, not trusted from caller fields. ContextVersion is correlation only, not F authority.

ReadReceipt may be cited as a read fact but is not truth, authorization, Canonical Evidence, Context Applied proof or future read grant. ReadCursor is bound to one RecallSession, Archive object revision/hash, source revision and selector plan. It cannot cross ContextVersion or session. A later ContextVersion must open a new authorized session.

A Context entry cannot be deliverable if its required archive source may expire first unless a permitted excerpt is materialized as its own governed derivative. Source revision change creates a new Archive revision; old Context ref becomes STALE and G must create a new ContextVersion after revalidation. F summaries/previews are non-canonical derivatives, default no-LLM, and cannot upgrade Reported/Inferred to Verified.

### 5.2 State transitions

Archive capture: CapturePrepared → Registered/Admitted → StoredImmutable → IndexedOrUnindexed → Active or Quarantined/Suppressed/Expired.

Recall: IntentValidated → SessionOpened → PageRead* → Complete/Partial/Stale/Suppressed/Unavailable/Cancelled/Expired. Each page and final serialization rechecks permission/fence.

Context: Candidate → Validated → IncludedInStagedContext → ContextVersionCommitted → DeliveryPrepared → AppliedEvidenceValidated. Recall completion is not Applied.

### 5.3 Mapping

| Object | Creator | Authority Owner | Consumer | Lifecycle | Permission | Forget |
|---|---|---|---|---|---|---|
| ArchiveObjectManifest | F | F runtime; D/I canonical ancestry/policy | F/G | immutable; active/quarantined/suppressed/expired | I | D if canonical lineage; I retention |
| ArchiveLocator | F | F | G/F | revision-pinned/expiring | every dereference | source/ancestor fence |
| RecallIntent | G | G intent; H/I identity | F | request-scoped | before session/read | target fence |
| RecallSession | F | F | F/G | active/partial/complete/stale/suppressed | every read | D/I |
| ReadBudget | F; G hint | F | F/G | reserved/consumed/released | no grant | cannot bypass fence |
| ReadCursor | F | F | F/G | session/object/selector bound | every continuation | invalidated on fence/revoke |
| ReadReceipt | F | F | G/audit | immutable | later use reauthorized | retention/lineage |
| ObservationRecallResult | F | F facts; G acceptance | G | complete/partial/stale/etc. | final handoff | source lineage |
| CompletenessMetadata | F | F | G | immutable per result | no grant | omission/fence |
| WorkingSetObservationEntry | F | F | F/G | cache projection | every hit | inherits source lineage |
| TSS | G | G Context projection | H/C | ContextVersion-bound | I/D before publish | transitive sources |
| ContextObservationReference | G | G | G/H/C | ContextVersion-bound | I/D at commit/delivery | Archive/source fence |
| Compaction Decision/Fidelity/Lineage | G | G | G/F/D audit | immutable/append-only | governed | transitive source fence |
| ContextVersion linkage | G | G | H/C/F | immutable per Context | current I/D | dependency invalidation |

### 5.4 Failure behavior

Hash/revision mismatch → stale/quarantine. Permission/fence unavailable → fail closed. Budget/timeout/partial index → PARTIAL, never COMPLETE. Cursor mismatch → reject and open a new authorized session. Receipt/fidelity failure → reject candidate and retain prior Context. Context CAS conflict → rebase or abort. F outage does not authorize stale locator use; G outage does not grant F Context selection authority.

## 6. D/E Canonical Authority and Derivative Boundaries

Runtime-only observations are not Canonical Memory. F Archive manifests/blobs/read receipts/catalog/page maps/cache are Runtime assets subject to I policy and D fence when they carry D-covered lineage. Canonical-derived artifacts must be registered with D and pass D/E final publication gate before canonical visibility. G TSS and compacted Context remain G-owned Context projections, not canonical truth, but if they derive from D-covered sources they must participate in D dependency registration/barrier and final suppression checks.

Archive does not blanket-register as a Canonical Memory producer merely because it is an F store. F producer classes/work items that process canonical sources or emit canonical derivatives must register with D before work. D/I must classify the complete producer and target inventory.

Every summary, preview, embedding, normalized form, query index, cache, snapshot, delta and offline copy inherits applicable Scope, Permission, retention and Forget constraints. No Outbox Replay, Index Rebuild, Recall or Context Reconciliation may re-expose forgotten content.

Cursor separation is normative:
- CanonicalCommitCursor: globally ordered per Canonical Memory Authority, D.
- AggregateRevision: per aggregate, D.
- LifecycleEventCursor: per Memory, D.
- IndexWatermark: per index/channel partition, F.
- ForgetFence Generation: independent D namespace.
- PermissionEpoch: independent I policy-domain namespace.
- Archive ReadCursor: one Archive revision/session/selector, F.
- ContextVersion: per Context, G.
No cross-type arithmetic, ordering or substitution.

## 7. I/H/C Security and Applied Context

I defines Principal/Actor/Scope, permission and PermissionEpoch, revocation and retention. D defines canonical Forget. F enforces Runtime Archive checks. G decides Context selection/version. H defines protocol/ACK/reconnect. C proves final request boundary and Agent protected regions.

ArchiveLocator and ReadCursor are not bearer authorization. Recheck current I permission and D fence at candidate lookup, every page, cursor continuation, cache hit, cache-fill publication, final F→G handoff, G commit, delivery and final request submission. Cached authorization is acceptable only under explicit I-approved revocation guarantees; otherwise online revalidation is mandatory.

PermissionEpoch and ForgetFence are independent. Revocation denies actor access; Forget suppresses target lineage. Context Applied must bind exact ContextId/ContextVersion, Adapter/session, boundary/request correlation and capability epoch; Archive lineage remains separately pinned. Recall completion is not Applied.

If Forget/revocation occurs mid-read, cancel session, invalidate cursor, discard staged bytes and block final serialization. If fence advances before cache fill publication, reject fill. If after final request submission, in-flight request is immutable; preserve historical evidence and invalidate future use. Offline reconnect authenticates and fetches current I/D state, suppresses local data first, reconciles G target, then restores only authorized Snapshot.

Brain may modify only Brain-managed region. System/Developer instructions, User content, Agent policy, tools and credentials remain outside Brain authority. TSS is not Agent private state or CoT. Memory/Archive content is untrusted data.

## 8. Dynamic Compaction and TSS

Boundary completion is an evaluation opportunity, not unconditional compaction. Economic decision must include remaining request horizon and uncertainty, token savings, provider cache read/write and cache debt, compaction prompt/output/validation/retry cost, Archive recall and recovery cost, omission probability, repeated compaction overhead/cooldown, latency/deadline and task class. H/C provide actual request/cache telemetry; G owns decision. No SoL-Pi numeric default is adopted.

TSS is a typed, versioned G Context projection: goal/completion criteria, progress, verified outcomes, unresolved work, constraints, relevant entities/environment, decisions, uncertainty, next actions, source references and validity. It is not Canonical Memory, private Agent state or hidden reasoning. Epistemic status is preserved: Reported stays Reported; Inferred stays Inferred; Verified requires independent evidence under B/D/E rules.

Fidelity checks at least goal/progress, constraints/negative conditions, epistemic/fact status, temporal order, provenance/recoverability, Scope/Permission/Forget. Hard vetoes override any aggregate score. Exact quotes/hash are necessary but insufficient. Every compaction records immutable decision, fidelity report, ContextVersion linkage and lineage/loss ledger to original source anchors. No forgotten plaintext is retained solely for audit.

State: ActiveContext(v) → BoundaryObserved → DecisionEvaluated → StagedCompaction → FidelityValidated → DependencyRevalidated → ContextCASCommitted(v+1) → DeliveryPrepared. No-op retains current Context. Generation/validator failure, hard veto, dependency gap or permission/fence change aborts staged work and preserves prior version. Crash before commit leaves non-visible staging; after commit, version is authoritative and delivery reconciles independently.

SAC is independent stress mode for suitable task classes only, not default Agent runtime. Action Fusion is outside G/F and rejected here.

## 9. Forget Atomicity and Recovery — P0

| Race | Linearization/fence | In-flight behavior | Required recovery | Status |
|---|---|---|---|---|
| Forget × Archive Capture | D fence; F admission and final immutable publication gate; I permission | Pre-fence work in D barrier; drain/cancel/suppress | Stable work ID, no late manifest visibility; quarantine uncertainty | BLOCKED: F producer class not accepted |
| Forget × Recall | D fence + I epoch at every page/final handoff | cancel session, discard staged result | invalidate cursor; audit ranges and suppression | BLOCKED: no executable Archive read proof |
| Forget × Cache Fill | D fence at admission and atomic cache publish; I permission | late fill cannot publish | hit revalidation; stale inaccessible | BLOCKED: untested |
| Forget × Compaction | D registration + G CAS/final gate + I | abort staged candidate | re-run only from current authorized sources | BLOCKED: TSS lineage/gate unaccepted |
| Forget × Context Delivery | G target + D/I check; C final request submit boundary | cancel before submit; after submit immutable historical request | H blocks stale ACK/replay; G invalidates current use | BLOCKED: no joined test |
| Forget × Offline Reconnect | I reauth/epoch + D fence before G restore | offline queue remains unknown | suppress first; reconcile; then restore snapshot | BLOCKED: Archive-derived cache test absent |
| Forget × Archive Restore | I policy + D fence high-water before queryability | restored bytes quarantined | replay fence/lineage before reads; missing WAL => quarantine | BLOCKED: no Archive PITR proof |
| Forget × Snapshot/Delta Replay | D barrier + G version CAS + I epoch; H base validation | stop on fence/epoch/base mismatch | authorized snapshot + contiguous replay only | BLOCKED: no Archive lineage replay test |

Each test must prove stable idempotency identity, producer registration before work, named linearization point, current D fence and I epoch, final visibility gate, durable terminal disposition, crash/restore recovery and zero post-fence disclosure. If authoritative state is missing, remain UNKNOWN/IN_DOUBT/QUARANTINED. Deleting cache or receiving an event is not an atomicity proof.

P0 blockers: JF-10 deployment binding remains NOT DESIGNATED; D/I Forget and global completion remain open; F archive producer/target mapping is not accepted; E D/E/Storage atomic registration and publication gate is OPEN/BLOCKING; I trust-chain policy remains governance candidate; no joined executable test covers Archive restore, late fill, compaction and Adapter reconnect.

## 10. Performance and Experimental Design

Groups: (1) Full-History Accumulation; (2) fixed-threshold EoCC-like; (3) boundary-triggered; (4) cost-aware; (5) cost-aware + Observation Archive; (6) group 5 + Evidence Fidelity Validation; (7) SAC independent stress test only.

Metrics: Task Success, Fact Accuracy, Constraint Retention, Evidence Recall Accuracy, Epistemic Status Preservation, Context Token Count, Input/Output Tokens, E2E latency, cache read/write cost, recall cost, compaction cost, recovery cost, archive storage growth, Forget Leakage, False Completeness, P50/P95/P99 latency.

Freeze task set, seeds, model/provider/version, tokenizer, prompts, context window, hardware, runtime, cache/archive/index settings and parameters. Paired comparison on identical tasks/seeds; tuning set isolated from held-out set. Report per-task outcomes, paired deltas, confidence intervals and tail latency. Run ablations and combined stacks. Capability floors must be predeclared; zero unauthorized leakage, false completeness, epistemic upgrades and critical constraint loss are hard gates.

Phase-1 minimum: 30–50 curated tasks spanning long-horizon continuation, rare negative constraints, exact evidence recall, source revision changes, multi-scope isolation, epistemic preservation and Forget races; at least three repeats per task/config. SAC only on selected subset. G owns context metrics; F archive metrics; C/H request/cache telemetry; D/I security/Forget assertions; A protocol and gate aggregation.

## 11. A–I Baseline Impact Matrix

| Owner | Change/dependency | Status |
|---|---|---|
| A | record system boundary, cursor separation, decisions and blockers | DECIDED |
| B | typed refs, Scope, epistemic/temporal preservation | CONDITIONAL |
| C | Archive lineage in request evidence; request/cache telemetry; managed region | CONDITIONAL |
| D | classify F producer classes and G derivatives; fence mapping | BLOCKED |
| E | preserve canonical gate; no F catalog collision | CONDITIONAL |
| F | Archive lifecycle, read/cursor/receipt/cache/completeness/suppression | CONDITIONAL |
| G | Context ref/TSS/compaction/fidelity/lineage/invalidation | CONDITIONAL |
| H | Recall envelope, auth binding, errors, cancellation, reconnect | CONDITIONAL |
| I | classification, retention, authorization, inventory, revocation | BLOCKED |
| Storage | atomic Archive publication/restore and fence recovery | BLOCKED |

## 12. P0/P1 Findings

P0-01: no end-to-end Forget linearization proof for Archive and Context derivatives. P0-02: D/I producer inventory and PermissionEpoch mapping for Archive not accepted. P0-03: Archive restore/PITR cannot reopen reads before authoritative fence/permission reconciliation; no evidence. P0-04: JF-10 deployment NOT DESIGNATED; no production activation/global completion claim.

P1-01: F/G identity, excerpt, cursor and expiry rules not frozen. P1-02: TSS and task class semantics need B/C/D/G agreement. P1-03: economic model lacks project telemetry calibration. P1-04: fidelity hard-veto thresholds need held-out validation. P1-05: metadata index partitioning/retention/ANN require workload evidence. P1-06: H/C request/cache telemetry needs same-version acceptance.

## 13. Final Architecture Decisions

| ID | Decision | Status |
|---|---|---|
| 1 | F-owned Observation Archive boundary | DECIDED conceptually; contract CONDITIONAL |
| 2 | F/G Recall Contract | CONDITIONAL |
| 3 | TSS concept | CONDITIONAL |
| 4 | Dynamic cost-aware compaction | CONDITIONAL |
| 5 | Fidelity Validator | CONDITIONAL |
| 6 | Compaction Lineage/Loss Ledger | CONDITIONAL |
| 7 | ArchiveLocator/ReadReceipt evidence chain | CONDITIONAL |
| 8 | SAC experiment mode | DECIDED; default REJECTED |
| 9 | F logical metadata catalog distinct from E index | DECIDED |
| 10 | Interface design | CONDITIONAL; semantic design only, no freeze |
| 11 | Rust implementation | BLOCKED |
| 12 | New independent Observation Service | REJECTED |
| 13 | Automatic vectorization of every observation | REJECTED |
| 14 | Action Fusion in G/F | REJECTED |

## 14. Required Owner Acceptances

A does not accept for other Owners. Exact-version requests and dependencies are in context-optimization-owner-decision-register.md. Silence, branch existence or acceptance of another contract version is not acceptance.

## 15. Implementation Readiness

Architecture concept accepted with boundaries. System contract is a candidate, not frozen. Semantic interface design may proceed to close gaps. Rust implementation and production readiness are not authorized. No AiMemoryBrain performance result is claimed.

**Final conclusion:** absorb NVIDIA work as governed F Runtime Archive/exact recall, G TSS/Context projection, boundary-triggered cost-aware compaction, fidelity-gated lineage and controlled paired validation. Reject a second Context system, new service now, summary-as-truth, paper-specific defaults, all-observation embeddings, SAC default and Action Fusion in G/F. Forget/authorization/restore proof is the gate.
