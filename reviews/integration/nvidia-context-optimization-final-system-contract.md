# NVIDIA Context Optimization — Final System Contract (Conditional Integration Baseline)

- Owner: A — Principal Integration Architect
- Status: **CONDITIONAL / NOT API, WIRE OR STORAGE FREEZE**
- Authority rule: each Owner remains authoritative for its own domain objects and transitions

## 1. Contract scope

This document reconciles accepted architectural boundaries into one system-level contract. It is not a substitute for detailed Owner schemas, the D/E/Storage COC durable protocol, I governance approvals or executable conformance.

A logical boundary does not imply a separate process, service, database or crate. No implicit dual-writer is permitted. A cross-owner workflow coordinates authorities, but each state has exactly one authoritative writer and an explicit receipt/linearization protocol.

## 2. Authority and write matrix

| Object / state | Authoritative Owner | Permitted writers | Explicitly prohibited |
|---|---|---|---|
| Domain identity, typed reference meaning, Scope/epistemic/time vocabulary | B | B defines semantic contract; issuing module creates its own typed IDs | F/G/H inventing domain meaning or treating refs as grants |
| Canonical Memory identity/revision/lifecycle | D | D canonical Memory authority | F Archive or G Context promoting its projection to canonical truth |
| Canonical ForgetOperation, ForgetFence, canonical producer/dependency barrier | D | D only through accepted D gate | I/F/G/E independently advancing or overriding D fence |
| Principal, Actor, issuer trust, PermissionEpoch, revocation, retention, global inventory and policy | I | I policy authority | D substituting fence for permission; caller-supplied scope as authority |
| ArchiveObjectManifest, immutable Archive bytes/revisions, ArchiveLocator | F | F Archive runtime | G rewriting F manifest/blob/locator lifecycle |
| RecallSession, ReadCursor, ReadReceipt, ReadBudget accounting, completeness, Archive cache | F | F runtime | G/H/C mutating F session or cursor state |
| ContextObservationReference, Context membership/selection, ContextVersion, TSS, compaction, fidelity, lineage/loss, DeliveryIntent | G | G Context authority | F changing Context selection/version; D/H inventing Context state |
| Canonical Derived Registration / compiler WorkItem / publication request and compiler lifecycle | E, subject to D registration and Storage durable gate | E creates compiler work and submits complete immutable dependency set; D/Storage decide canonical gate/visibility under accepted protocol | E local state, outbox, object existence or I receipt alone creating visibility |
| Storage VisibilityPointer, PublicationReceipt, durable owner outcome and reader-visible publication | Storage for the Canonical Authority deployment, coordinated with D/E/I | Storage participant commits only under accepted D/I/Storage protocol | E/F/G/I bypassing Storage visibility authority |
| BMCP schema, message family, transport ACK, cursor wire envelope, reconnect | H | H defines/version-controls protocol | ACK being treated as Applied or publication |
| Agent/Adapter final request boundary evidence, managed-region integrity | C | C produces/validates boundary evidence; G alone accepts Applied | Transport ACK, ReadReceipt or materialization alone asserting Applied |
| Applied state for a Context delivery | G | G applies its per-request acceptance predicate using C/H/I/D evidence | C/H/F/D independently setting G Applied state |
| Cross-owner integration register and gate aggregation | A | A records evidence and status | A approving another Owner's policy, domain semantics or implementation evidence |

## 3. Identity, version and semantic distinctions

### 3.1 Domain and evidence

- **Observation:** source-qualified occurrence/record. It is not automatically a proposition, canonical Memory or verified fact.
- **Evidence:** typed provenance/attestation relation to an exact source, version and range; its strength is limited to the attestation actually recorded.
- **Derived Summary:** immutable derived artifact with its own identity/version, derivation profile, exact source revision set and lineage; it cannot silently upgrade epistemic status.
- **Canonical Memory:** D-governed canonical asset with D-owned identity, revision and Forget lifecycle.
- B's domain vocabulary governs typed identity, Scope, observed/recorded/source-valid time, epistemic status and provenance semantics.

### 3.2 Archive and Context references

- **ArchiveObjectManifest / ArchiveLocator (F):** locator pins one immutable Archive object revision, content hash, source identity/revision and selector coordinate system. It is not a credential, authorization grant or proof of currentness.
- **ContextObservationReference (G):** ContextVersion-bound edge to an exact ArchiveLocator/source revision and optional exact range/receipt. It is not the ArchiveLocator and cannot mutate F Archive state.
- Source revision change does not retarget an old reference. Old reference becomes STALE; G must validate and commit a new ContextVersion.
- Locator, receipt and cursor are never bearer authorization.

### 3.3 Recall and cursor

- **RecallIntent (G→F):** bounded purpose/selector/scope correlation request. Authenticated Principal and trusted Scope are resolved through H/I; caller claims are not authority.
- **RecallSession / ReadCursor (F):** cursor is subordinate to one session, principal/security domain, trusted scope, permission/fence checkpoint, exact Archive object/revision/hash, selector digest and coordinate system. It cannot cross session, object, revision, principal, scope, ContextVersion or changed authorization/fence checkpoint.
- **ReadReceipt (F):** immutable fact describing exact returned bytes/range and recorded checks. It does not prove semantic truth, G selection, Context commit, delivery, Applied or future read permission.
- **Completeness:** COMPLETE only when the declared bounded selector/range was fully executed with verified bytes and no undisclosed omission. Budget exhaustion, timeout, partial page/index lag or omitted channel is PARTIAL/DEGRADED; revision change is STALE; policy/fence denial is SUPPRESSED; authority/integrity uncertainty is UNKNOWN/UNAVAILABLE.

### 3.4 Context and compaction

- **TSS:** G-owned typed, versioned Context projection, not Canonical Memory, Agent private state or chain-of-thought.
- **ContextVersion:** G-owned per-Context immutable version; no F/H/D arithmetic or authority interpretation.
- **Compaction:** boundary completion triggers evaluation, not unconditional compaction. Candidate must pass economic measurement, fidelity hard vetoes, transitive lineage, current D/I checks and Context CAS before becoming visible.
- Fidelity checks preserve goal/progress, constraints and negative conditions, epistemic status, temporal order, provenance/recoverability and Scope/Permission/Forget. Hard vetoes override aggregate scores.
- CompactionLineage/LossLedger map retained and omitted information to original source anchors, reasons, validation and rehydration pointers. Do not retain forgotten plaintext solely for audit.

### 3.5 Agent delivery and Applied

The stages are separate:
1. F Returned: exact Recall result/page/receipt/completeness.
2. G Selected: immutable ContextVersion, source refs, compaction lineage and DeliveryIntent.
3. H Delivered / Adapter Materialized: transport receipt and managed-region state.
4. C Final Request Submitted: exact final request boundary, request ID, ContextVersion, managed-region digest, Adapter capability/session and current authority evidence.
5. G Applied: G evaluates the per-request predicate. It does not claim model attention, comprehension or use.

Tier-2 evidence may be Partial/Unknown. Tier-3 transport-only evidence cannot claim Full Applied. Historical Applied evidence does not automatically authorize current use after supersession, Forget or revocation.

### 3.6 Canonical-derived registration and publication

- F Archive metadata catalog is not E's canonical index.
- G TSS/compaction is not automatically canonical-derived publication.
- A G/F/E artifact becomes a D-covered derivative when the accepted producer/lineage classification says it derives from D-covered canonical lineage or is submitted as a canonical derived artifact. This classification inventory remains an Owner task.
- E submits a complete immutable dependency/output manifest; D validates Forget fence/barrier and dependency coverage; I authorization must be current; Storage VisibilityPointer + PublicationReceipt is the sole reader-visible publication authority under the accepted durable protocol.
- Staging, compiler completion, object existence, local receipt, outbox or I authorization alone never make data visible.

## 4. Lifecycle and state transitions

| Workflow | State progression |
|---|---|
| Archive capture | CapturePrepared → Registered/Admitted → StoredImmutable → IndexedOrUnindexed → Active; alternatives: Quarantined / Suppressed / Expired |
| Recall | IntentValidated → SessionOpened → PageRead* → Complete / EmptyComplete / Partial / Degraded / Stale / Suppressed / Unavailable / Unknown / Cancelled / Expired |
| Context | Candidate → Validated → Staged → ContextVersionCommitted (CAS) → DeliveryPrepared → Applied / Partial / Unknown / Superseded |
| Compaction | BoundaryObserved → DecisionEvaluated → StagedCandidate → FidelityValidated → DependencyRevalidated → ContextCASCommitted; failure leaves prior version authoritative |
| Canonical publication | WorkRegistered → ManifestFrozen → GatePrepared → I/D/Owner Gate Resolved → Storage Visibility Commit → PublicationReceipt Confirmed; ambiguous outcome remains IN_DOUBT/private |
| Reconnect | Authenticated → Current I/D state fetched → Local suppression → Context/delivery reconciliation → Fresh Snapshot or contiguous Delta → Restore managed region |
| Restore | RestoreStarted → Quarantined → Integrity/WAL validated → Independent D/I controls read → Inventory/lineage reconciled → Owner receipts → Queryable; any gap remains RESTORE_FENCED |

Each state machine is owner-local. Another Owner's event is evidence/input, not authority to mutate the receiving Owner's state without its accepted transition.

## 5. Security, Forget and retention

I defines Principal, issuer trust, Scope authorization, PermissionEpoch, revocation, retention and global inventory/policy. D defines ForgetOperation, ForgetFence generation, canonical lineage and producer barrier. These are independent typed authorities.

Every protected boundary rechecks current applicable I permission and D fence: capture admission and final Archive publication; each Recall page and final serialization; cursor continuation; cache hit and atomic cache-fill publication; Context stage/commit; compaction; delivery; reconnect; final request submission; canonical publication; restore release.

- Revocation denies future actor access.
- Forget suppresses target lineage and derived copies according to D/I policy.
- Neither authority substitutes for the other.
- Cached ALLOW, stale epoch grace, offline lease, locator possession, ReadReceipt replay or caller-provided Scope cannot bypass current checks.
- Unknown authority state means deny/quarantine.
- If a fence wins before a visibility gate, the operation must not become visible.
- If final request submission historically won before later Forget/revocation, preserve that immutable historical fact but invalidate future use; if causal order is unknown, outcome is UNKNOWN and content stays suppressed.

## 6. Concurrency, idempotency and errors

Each operation has a stable logical operation/request/work/delivery ID and immutable request/dependency digest. Retries use a new AttemptId but retain the logical ID. Same key + same digest returns/reconciles the authoritative prior outcome. Same key + different digest is IDEMPOTENCY_CONFLICT. No retry creates a second publication participant or silently changes the bound XID.

CanonicalCommitCursor (D), AggregateRevision (D), LifecycleEventCursor (D), IndexWatermark (F), ForgetFence Generation (D), PermissionEpoch (I), Archive ReadCursor (F), ContextVersion (G) and COC sequence tokens occupy distinct namespaces. No cross-type max, ordering, arithmetic, coercion or substitution.

| Condition | Required outcome |
|---|---|
| Source/object/context revision changed | STALE |
| Permission denied/epoch stale | REVOKED / DENIED |
| Forget fence blocks lineage | FORGOTTEN / SUPPRESSED |
| Budget/timeout/partial page/index lag | PARTIAL / DEGRADED, never COMPLETE |
| Cursor binding mismatch | INVALID_CURSOR |
| Same idempotency key, changed digest | IDEMPOTENCY_CONFLICT |
| Delta base mismatch | CONTEXT_BASE_MISMATCH |
| Timeout/crash/ambiguous terminal state | UNKNOWN / IN_DOUBT |
| Hash/manifest/WAL/control-ledger mismatch | QUARANTINED / RESTORE_FENCED |
| Fidelity hard veto | REJECTED_FIDELITY; preserve prior ContextVersion |
| Delivery ACK without C proof/G predicate | Delivered or Unknown, never Applied |

Exact enum names, numeric codes and wire encodings remain H-owned schema work and are not frozen here.

## 7. Recovery contract

JF-10 v2 / COC bridge has architecture-level owner acceptance for the single-I-PolicyDomain profile with enumerated exceptions. It is not implemented or production-conformant.

The required safety boundary is one immutable operation ID/digest/boundary/security tuple; one exact prepared Storage XID and participant digest; I sequencer decision ordered against revocation; D fence and producer/dependency serialization retained; only the exact XID may recover; VisibilityPointer, PublicationReceipt, owner outcome and receipt-consumption record become visible atomically in Storage; IN_DOUBT retains private bytes and required locks; restore reconciles I terminal decision, D fence/lineage, owner ledger/cursor and Storage participant before readers reopen.

The selected logical deployment profile is not a designated production database. PostgreSQL 18.7 CI capability results do not prove the project's live Canonical Authority deployment.

## 8. Evidence and version compatibility

Every conformance evidence bundle pins repository, branch, commit SHA, build/image digest, database/coordinator version/configuration, test ID, seed/fixture, fault point, Principal/Scope, I PermissionEpoch, D fence generation, inventory epoch/seal, source/manifest/dependency digest, operation/XID, receipt IDs, trace IDs, authoritative readback, expected/actual result and independent reviewer.

Compatibility rules (proposal pending H/B schema acceptance):
- wire schema has explicit major/minor and immutable schema ID;
- major version changes are incompatible unless explicit migration is accepted;
- unknown required type/field/enum fails closed;
- optional additive fields may be ignored only under H's accepted negotiation profile;
- cursors are opaque and bound to schema/session/security/source versions; no cross-version reuse;
- old ContextVersion or stale snapshot/delta requires reconciliation, not implicit upgrade;
- persisted-state migration preserves authority owner, identity, version, lineage, fences and idempotency records;
- no compatibility shim turns UNKNOWN/PARTIAL into success or infers authorization.

## 9. Contract disposition

This is the conditional integrated contract. It does not freeze field names, API/IDL, wire schema, database schema, retention durations, performance thresholds, production topology or implementation.
