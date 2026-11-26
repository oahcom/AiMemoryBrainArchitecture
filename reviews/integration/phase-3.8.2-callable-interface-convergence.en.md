# Phase 3.8.2 — D/E/I/Storage Callable Interface Convergence

- Work item: Issue #25
- Status: **CANDIDATE / OWNER REVIEW REQUIRED; NOT FROZEN**
- Owner perspective: A — integration contract proposal
- Source of truth: exact owner branch blobs and RFC-IDE-001 v1.0.0 listed below
- This document defines a logical call surface and dependency wiring. It does not define H wire encoding, cryptographic profiles, physical topology, or production activation.

## 1. Scope and non-duplication

This increment turns the existing Phase 3.8.1 candidate operation matrix into an owner-callable boundary and makes the unresolved call/response seams explicit. It does not reimplement SQLite Event Store, Compile Intent Outbox, Scope isolation tests, the Publication Protocol reference model, or the idempotency identity RFC.

- PR #245: SQLite durable Event acceptance adapter — merged.
- PR #246: transactional Compile Intent Outbox — merged; intent persistence only, not dispatch or execution.
- PR #247: Phase 1 SQLite persistence boundary evidence — merged.
- PR #251: RFC-IDE-001 v1.0.0 — Draft/Open; cited as a proposal, not an approved decision.

## 2. Exact inputs reviewed

| Owner | Branch | Artifact | Blob |
|---|---|---|---|
| D | `session-d-memory-brain-2026-11-16` | `03-memory-brain/phase-3.7-d-producer-class-registry-eventref-ingress-and-participant-intent.md` | `4c01713bc8793a8926ef18b625b72d132572173d` |
| E | `session-e-memory-compiler-2026-11-16` | `04-memory-compiler/phase-3.7-e-local-lifecycle-producer-derivative-queue-recall-context-restore.md` | `4fb9e58511941f59b4d777336f8f85ad88ecccf1` |
| I | `session-i-security-governance-2026-11-16` | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` (not restored on main; see AID-2026-107 §10) | `e3b1b5d99eb36ac0b395854d8c19287d2b64b752` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `reviews/storage-consistency/phase-3.7-storage-atomic-producer-registration-dependency-visibility-realization.md` | `2ab899ee37a18ae6c8f2f64dbb82ad6499842060` |
| A candidate surface | `session-a-integration-2026-11-16` | `reviews/integration/phase-3.8.1-a-contract-surface-and-exact-pin-refresh.md` | `ad5450ea35f6dabc7de1ffa1ea63661f2e500064` |
| Idempotency RFC | PR #251, `rfc/idempotency-identity-tuple-2026-11-18` | `reviews/contracts/RFC-IDE-001-idempotency-identity-tuple.en.md` | `0f42db17325ba5402b7d8000fad8ce11aeadfbc4` |
| Idempotency RFC | PR #251, same branch | `reviews/contracts/RFC-IDE-001-idempotency-identity-tuple.zh-CN.md` | `3cd023ff1293b5d3ac8b7fdd5f8ddd9ef9598a1a` |

These are exact source pins, not independent Owner signatures. Any changed source blob invalidates the corresponding review until re-read.

## 3. Authority and call ownership

| Boundary | Callable authority | Caller / consumer | Must not be inferred from |
|---|---|---|---|
| Producer class + work admission, ForgetFence, dependency completeness, publication participant and producer terminality | D | E invokes; Storage verifies D evidence at visibility commit | E AcceptedReceipt, queue ACK, Storage row, I receipt |
| Compile intent, queue, attempt/lease, derivation, private stage, output inventory and orchestration | E | Compiler worker/runtime | D registration as proof of I permission; outbox row as execution permission |
| Current authorization, PolicyDomain sequencer, revocation ordering and I closeout | I | E requests at protected boundaries; Storage validates pre-commit proof | cached ALLOW, stale PermissionEpoch, D clearance |
| Durable hidden participant, transaction/serialization, authoritative visibility pointer/outcome and recovery | Storage | E orchestrates; D/I consume outcome | object existence, object-store URL, queue/outbox delivery, transport ACK |
| Canonical wire names, encoding, signatures, key lifecycle and interoperability | H (future gate) | all adapters | this logical proposal |

No adapter may mint another owner's receipt, terminal state, epoch, participant reference or authorization. Numeric positions from D, I and Storage are incomparable.

## 4. Typed operation surface (logical API; candidate)

The following names are stable logical operation proposals, not frozen Rust traits, HTTP endpoints, or wire schemas. All references are opaque nominal types. Every command carries a request digest over its immutable canonical input; every query resolves the same operation identity.

### D-owned operations

- `D.register_producer_work(ProducerWorkRegistration) -> RegistrationResult`
  - Input: stable `ProducerWorkItemId`, authenticated ProducerIdentity binding, ProducerClassId/version, EventRef and known source refs, exact Scope, approved lineage token/digest, request digest.
  - Success: durable `DRegistrationReceipt` + D-local ProducerRegistrationSequence.
  - E may enqueue/lease/execute only after a durable success. EventRef-only ingress is permitted under D §8; it grants no protected payload-read permission.
- `D.install_forget_fence(ForgetFenceRequest) -> FenceResult`
  - Success: immutable fence, registry version, captured producer-registration high-water and inventory snapshot reference.
- `D.register_derived_dependency_set(CompleteDependencySet) -> DependencyResult`
  - E supplies the full direct/transitive set and exact source revisions/Scope; D validates lineage and current fence.
  - Success only after the complete immutable set commits; partial sets have no complete receipt.
- `D.admit_publication(PublicationTuple, StorageVisibilityParticipantRef) -> DPublicationParticipantRef`
  - Requires Storage's already durable PREPARED_HIDDEN participant, complete dependencies, current attempt/lease and D fence admission.
  - Success: D-owned `DPublicationParticipantRef`; this is a barrier hold, not visibility permission.
- `D.close_publication_participant(DPublicationParticipantRef, StorageOutcomeProof) -> DTerminalReceipt`
  - Accepts only exact `COMMITTED_VISIBLE` or authoritative `NO_PUBLICATION` for the same tuple.
- `D.complete_producer_work(WorkItemId, FinalOutputInventory) -> ProducerTerminalReceipt`
  - D closes the barrier only after all outputs, retries, delayed publishers and unknown outcomes are accounted.

### E-owned operations

- `E.accept_compile_intent(CompileIntent) -> EAcceptedReceipt`: durable local ingress only.
- `E.register_work_with_d(WorkItemId, RequestDigest) -> DRegistrationReceipt`: resolve D admission before queueing.
- `E.enqueue_registered_work(DRegistrationReceipt) -> QueueReceipt`: reject missing, stale or unresolved D evidence.
- `E.acquire_attempt(WorkItemId) -> AttemptLease`: allocate attempt/lease generation; stale generations cannot mutate dependencies or publish.
- `E.stage_derivative_privately(AttemptLease, Artifact) -> PrivateStageRef`: no serving locator or visibility.
- `E.submit_complete_dependencies(AttemptLease, CompleteDependencySet) -> DDependencyReceipt`.
- `E.publish_derivative(PublicationTuple) -> PublicationResolution`: orchestrates Storage prepare → D admission → I consume → Storage commit → D/I closeout; never treats its own receipt as an owner decision.
- `E.complete_work(WorkItemId, FinalOutputInventory) -> ProducerTerminalReceipt`: delegates D terminal decision; E cannot close D's barrier itself.

### Storage-owned operations

- `Storage.prepare_visibility(PublicationTuple) -> StorageVisibilityParticipant`
  - Atomically persists the immutable tuple and hidden private participant before D admission.
  - Same operation + same tuple digest returns the same participant; changed digest conflicts.
- `Storage.commit_visibility(StorageVisibilityParticipantRef, DPublicationParticipantRef, ICommitAuthorizationProof) -> StorageVisibilityOutcome`
  - The pre-commit I proof is the consumed single-use `ICommitAuthorizationProof` / `ICommitAuthorizationProof`, not the post-commit `ITerminalProof`.
  - The authoritative commit validates exact D participant/current fence and exact I proof while atomically installing the visibility pointer and immutable outcome.
- `Storage.resolve_visibility(PublicationOperationId, TupleDigest) -> StorageVisibilityOutcome`
  - Lost ACK, crash, failover and restore resolve the same operation. UNKNOWN stays private; no age/missing-row inference.
- `Storage.prove_no_publication(StorageVisibilityParticipantRef) -> NoPublicationProof`
  - Only when Storage can prove no pointer was installed and no delayed publisher/outbox/retry can install one later.

### I-owned operations

- `I.consume_commit_authorization(AuthorizationRequest) -> ICommitAuthorizationProof`
  - Single-use consumption in the authoritative PolicyDomain sequencer; binds authenticated subject/delegation, action, purpose, audience, Scope, Environment, PolicyDomain/current PermissionEpoch, artifact/version, PublicationOperationId/tuple digest and exact D + Storage participant refs.
  - Returns authority-derived `COMMIT_WON`, `REVOCATION_WON` or `UNKNOWN/IN_DOUBT`; caller cannot supply the result.
- `I.close_publication_authorization(ICommitAuthorizationProof, StorageOutcomeProof) -> ITerminalProof`
  - Post-Storage-outcome closeout only. COMMIT_WON holds later applicable revocation until exact Storage terminal outcome; UNKNOWN holds.
- I must expose an authoritative resolution query for a consumed receipt after response loss. Re-consuming a nonce is not a substitute for resolving its original sequencer result.

## 5. Mandatory publication call order

1. E accepts the CompileIntent locally; this is not permission to dispatch.
2. E obtains durable D RegistrationReceipt before queue, lease, protected read or execution.
3. E executes under a current AttemptId/LeaseId, stages outputs privately and completes the exact dependency set with D.
4. Storage durably prepares a hidden `StorageVisibilityParticipantRef` bound to the immutable publication tuple.
5. D admits a `DPublicationParticipantRef` bound to that exact durable Storage participant.
6. I consumes a single-use `ICommitAuthorizationProof` in its own PolicyDomain sequencer, bound to both participant refs and the same tuple.
7. Storage commits visibility using the exact D current-participant/fence proof and the pre-commit I `ICommitAuthorizationProof`; it atomically writes the authoritative visibility pointer and outcome.
8. D and I independently close their participants only after reading the same authoritative Storage outcome: `COMMITTED_VISIBLE` or proven `NO_PUBLICATION`.
9. E/D close producer work only after all output and retry/replay paths are terminally accounted.

This order is Storage hidden durable participant → D admission → I receipt consumption → Storage visibility commit → D/I closeout. It supersedes stale D-first sequences.

## 6. Idempotency, retry and identity separation

Use RFC-IDE-001 v1.0.0 (PR #251 Draft) for producer append namespace and receipt replay semantics:

`(ProducerIdentity, Scope, IdempotencyKey)` plus exact Digest equality.

Do not duplicate or reinterpret that contract here. In particular:
- authorization is rechecked before any Receipt disclosure, including replay;
- same namespace + same Digest returns the original Receipt;
- same namespace + changed Digest is immutable conflict;
- cross-Scope key reuse is an independent namespace, not a cross-Scope receipt lookup;
- ProducerIdentity composition, digest canonicalization and Receipt retention remain at the RFC's stated CANDIDATE / TO_VALIDATE status.

Publication uses a separate immutable operation identity: `PublicationOperationId + PublicationTupleDigest`. It is not the producer's IdempotencyKey. Same operation + same tuple resolves the same participant/outcome; same operation + changed tuple is `IMMUTABLE_IDENTITY_CONFLICT`. A new publication attempt after authoritative `NO_PUBLICATION`, or after changing artifact/version, dependency set, Scope, source revision or attempt/lease tuple, receives a new PublicationOperationId and fresh participant identities and D/I checks. AttemptId/LeaseId may rotate for retries of the same logical work; they may not be substituted into an already committed publication tuple.

Nominally distinct: ProducerIdentity, ScopeRef, IdempotencyKey, ProducerWorkItemId, DerivationRunId, AttemptId, LeaseId, PublicationOperationId, DPublicationParticipantRef, ICommitAuthorizationProof, StorageVisibilityParticipantRef, Storage PreparedParticipantRef/GID, C ParticipantIntentRef and ITerminalProof.

## 7. Resolution and failure contract

Every mutating call must have a same-identity resolution query. Transport timeout is not a state transition.

| Outcome | Meaning | Required caller behavior |
|---|---|---|
| REJECTED | authoritative denial | no downstream capability |
| QUARANTINED | required identity/lineage/Scope evidence incomplete | no queue/lease/execute/visibility |
| IMMUTABLE_IDENTITY_CONFLICT | same operation identity, changed digest/tuple | stop; never overwrite original |
| FENCE_WON | D fence ordered first | no publication |
| REVOCATION_WON | I revocation ordered first | no publication |
| STALE_ATTEMPT | Attempt/Lease generation superseded | worker cannot mutate/publish |
| INCOMPLETE_DEPENDENCY_SET | direct/transitive set incomplete | no complete receipt, no publication |
| UNKNOWN / IN_DOUBT | terminal outcome cannot be proven | keep private; keep admitted barriers open; resolve same ID |
| COMMITTED_VISIBLE | authoritative Storage visibility commit | D/I may close after exact proof validation |
| NO_PUBLICATION | authoritative proof of no current or future visibility | D/I may close after exact proof validation |

DLQ, lease expiry, process death, queue deletion, missing row, lost ACK, stale replica and timeout are never terminal evidence.

## 8. Dependency registration and activation gate

A runtime composition root may register adapters only by explicit typed capabilities:
- D: producer admission, fence, dependency, publication participant and terminal APIs;
- E: intent ingress, queue/lease/attempt, staging, orchestration and inventory;
- I: current protected-boundary authorization, single-use sequencer and closeout/resolution;
- Storage: hidden prepare, atomic visibility commit, authoritative outcome resolution and restore-safe no-publication proof.

Startup/readiness must fail closed if any required capability is absent, points to a test/fake adapter in a production profile, or lacks an owner-approved contract version. The Compile Intent Outbox is not a Dispatcher. No worker is started merely because the outbox row exists. A partial adapter set may support local non-protected tests only and must not expose derivative execution or serving.

H wire adapters and canonicalization/signature profiles remain a separate dependency; this logical API does not freeze them.

## 9. Required owner decisions and conformance

| Owner | Required exact decision on current Blob |
|---|---|
| D | Operation names/input-output types, registration/fence linearization, complete dependency receipt, Storage-first publication admission, terminalization and replay/error mapping |
| E | CompileIntent/WorkItem/Attempt/Lease identity, call order, same-operation recovery vs new publication after NO_PUBLICATION, no stale §10 order |
| I | Authorization request vs consumed receipt vs post-commit ITerminalProof as distinct types; nonce resolution; issuer/key/policy currentness; revocation hold and commit proof validity |
| Storage | Prepare-before-D-admission, atomic validation of D current proof + pre-commit I proof, visibility pointer/outcome atomicity, authoritative NO_PUBLICATION, physical topology and restore |
| H | canonical bytes, digest/profile identifiers, signatures, key status/rotation/revocation, version negotiation and cross-language vectors |

Required deterministic tests: register-vs-fence both orders; EventRef-only admission; D ACK loss; complete-dependency crash; Storage prepare crash; D admission missing-participant rejection; I revocation-vs-consumption both orders; Storage visibility ACK loss; stale lease; same-ID changed-tuple conflict; NO_PUBLICATION with delayed publisher/outbox; restore with mismatched or missing owner ledger. Assertions must include durable rows, visibility pointer, D barrier, I revocation hold and exact retry identities.

## 10. Explicit contradictions / blockers

1. **E stale ordering:** E §10 still states D admission before Storage prepare and describes I terminal proof as a precondition to the Storage commit. E §11 explicitly supersedes that sequence with Storage prepare before D admission. E must remove or prominently mark the stale §10 wording so implementers cannot select the wrong order.
2. **Storage proof-stage ambiguity:** Storage §12 still says final commit validates an I “terminal proof”. A's current candidate mapping and the required causal order distinguish the consumed pre-commit `ICommitAuthorizationProof/ICommitAuthorizationProof` from post-commit `ITerminalProof`. Storage and I must explicitly accept the pre-commit proof type for visibility commit; ITerminalProof is closeout only.
3. **Callable API not frozen:** D/E/I/Storage source artifacts specify semantic obligations but do not yet publish a jointly accepted, exact typed method/DTO/query surface. The signatures in this proposal remain CANDIDATE.
4. **No physical topology proof:** Storage's shared serializable domain is a proposal; no selected/deployed topology or crash/failover/restore conformance PASS is claimed.
5. **No independent Owner approvals:** A role-simulated review is not a D/E/I/Storage signature. Each owner must decide against the exact Blob above.

## 11. Status and non-claims

- **CANDIDATE:** this callable logical API and dependency-composition proposal.
- **OPEN:** exact D/E/I/Storage Owner acceptance, H wire profile, physical transaction topology, live adapters and cross-owner conformance.
- **TO_VALIDATE:** runtime registration/readiness behavior, crash/failover/restore, multi-process serialization, proof verification and retry/expiry race tests.
- **DECIDED:** only previously approved repository decisions; this proposal does not promote RFC-IDE-001's Draft semantics or any owner proposal to repository-wide DECIDED.

No API implementation, schema freeze, independent Owner signature, CI conformance PASS, production dispatch, Compiler execution, production activation, global Forget completion or physical erasure is claimed.
