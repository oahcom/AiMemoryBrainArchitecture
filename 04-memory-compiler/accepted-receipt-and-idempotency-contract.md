# Accepted Receipt, Compiler Completion and Idempotency Contract

**Status:** CANDIDATE E contract; durable Storage realization, D producer APIs, H envelope and I policy approval remain OPEN.
**Owner:** Session E — Memory Compiler.
**Integration:** INT-P1-03, INT-P1-04, INT-P1-06, INT-X-01, INT-X-06.
**Authority:** E owns durable ingress receipt and compiler execution evidence. D owns Producer Admission ledger, canonical commit and CanonicalCommitCursor. F owns IndexWatermark. H owns wire/transport binding. I owns identity, authorization, PermissionEpoch, retention and global Forget policy.

## 1. Evidence is deliberately split

These evidence objects prove different facts and MUST NOT be collapsed into one Accepted/Success boolean.

| Evidence | Issuer / owner | What it proves | What it does not prove |
|---|---|---|---|
| AcceptedReceipt | E | Immutable source Event, payload ref/digest, idempotency record and compile intent are durably recoverable | D admission, compiler completion, canonical commit, dependency registration, publication or indexing |
| ProducerRegistrationReceipt | D | Stable ProducerWorkItem is durably admitted into D's producer ledger/barrier inventory | Work ran, output exists, dependency edges registered, or publication succeeded |
| CompilerCompletionReceipt | E | A named compile run reached a durable terminal compiler outcome with stage/provenance refs | Canonical Memory committed or derived output visible |
| CanonicalCommitReceipt | D | D accepted canonical transaction and committed canonical effects; includes D CanonicalCommitCursor and exact aggregate revision refs | Derived projection/index applied, Context updated or physical erasure |
| DerivedRegistrationReceipt | D (or D-designated authoritative ledger) | Specific derived artifact/source dependency registrations are durably present in D dependency inventory | Artifact is visible or final publication allowed |
| PublicationReceipt | Final gate authority; D/Storage ownership of receipt schema remains OPEN | Exact artifact/version passed final gate and atomic visibility transition committed | F IndexWatermark advanced or G ContextVersion changed |
| IndexAppliedAcknowledgement | F | Named index/channel partition durably accounted for a canonical prefix and returns its typed IndexWatermark | Forget completion or physical deletion |

A transport ACK, HTTP 2xx, queue enqueue, AcceptedReceipt, CompilerCompletionReceipt, D RegistrationReceipt or local database commit is not a substitute for another row.

## 2. Accepted semantics and ingress linearization

`Received` means bytes reached a process and may be volatile. `Accepted` occurs only after immutable EventRef, verified immutable payload reference/digest, idempotency record, AcceptedReceipt and durable CompileIntent/outbox are committed atomically or through a proven recoverable WAL.

Preferred transaction:
1. Authenticate transport context and resolve trusted ProducerIdentity through H/I; validate payload claims against it.
2. Authorize ingress under current I policy and PermissionEpoch; resolve B-typed ScopeRefs and security domain.
3. Persist immutable payload bytes/reference and verify digest before metadata commit.
4. In one transaction, persist Event, payload reference/digest, idempotency uniqueness row, AcceptedReceipt and CompileIntent/outbox.
5. Commit. This commit is the Accepted linearization point. Only then return receipt.
6. Dispatch at least once; queue delivery is not a second acceptance.

If payload storage and metadata DB are separate, the immutable payload is durably staged and verified first; metadata transaction references it. A crash can leave an orphan staged blob but cannot expose an Accepted event pointing to missing/mutable bytes. WAL alternative must have a durable commit marker binding all acceptance records. Exact Storage product/replication/fsync requirements remain OPEN.

## 3. Idempotency and authenticated namespace

Candidate namespace:

`(issuer_ref, authenticated_principal_ref, producer_identity_ref, security_domain_ref, validated_scope_binding, operation_family, caller_idempotency_key)`

- Principal and ProducerIdentity derive from authenticated transport/security context, never payload self-assertion.
- ScopeRef is B's typed domain reference; Scope does not grant permission. I decides the authorized scope binding and whether/how a canonicalized ScopeRef set participates in the namespace.
- Security domain is an I-governed isolation boundary; it is not inferred from arbitrary payload text.
- Event/operation family prevents collision between distinct semantics.
- Caller key remains stable across reconnects/retries for one logical submission.

The semantic request digest includes immutable payload bytes/digest, event family/schema, trusted producer binding, validated Scope/security-domain binding, source/environment identity and semantically relevant source time/content type. It excludes transport attempt, retry time and trace-only metadata. Algorithm and canonicalization profile are versioned; H's wire canonicalization remains CANDIDATE.

| Existing key | Digest | Result |
|---|---|---|
| None | Valid | Create one Event, receipt and compile intent |
| Existing | Same canonical semantic digest | Return original receipt/Event/intent/work identity and current status; no duplicate side effect |
| Existing | Different digest | Idempotency conflict; preserve original |
| Forget/retention tombstone | Any replay | Policy-safe suppress/reject; never reconstruct payload or work |

Receipt replay reads the original record; it does not rerun compilation, renew retention or bypass current authorization/Forget. A controlled recompile is a new DerivationRunId and must pass current I/D checks.

## 4. Compiler completion is a separate state machine

Compiler work lifecycle and D barrier mapping are defined normatively for E in `compiler-state-and-producer-admission.md`. Key rule: D registration must be durable before E queues, leases or executes derivative-capable work. E tracks Accepted, Queued, Leased, Running, Staged, DependencyRegistered, Retry, DeadLettered and Terminal; D tracks admission, barrier membership, dependency receipts and terminal disposition. DLQ/lease expiry is not terminal.

A CompilerCompletionReceipt binds:
- CompileIntentId, ProducerWorkItemId, DerivationRunId and final AttemptId;
- EventRef and source lineage digest/reference;
- compiler/extractor/normalizer/consolidator/model/prompt/schema versions;
- stage outcomes, provenance references and terminal disposition;
- any DerivedRegistrationReceipt IDs, PublicationReceipt IDs and CanonicalCommitReceipt reference, each as separate optional evidence;
- observed PermissionEpoch and ForgetFenceCursor as historical observations, not current authorization;
- completion time, structured result/error and idempotency digest.

Candidate-only compilation may complete without CanonicalCommitReceipt or PublicationReceipt. It remains a compiler output and is not automatically a Canonical Claim/Fact.

## 5. Typed cursor and epoch use

| Field | Correct type / owner | E rule |
|---|---|---|
| Source ingress position | SourceEventCursor / E | Per declared source/ingress partition; only for acceptance replay |
| Canonical transaction position | CanonicalCommitCursor / D | One globally ordered sequence per Canonical Memory authority; store only D-returned value |
| Object revision | AggregateRevision / D | Independent monotonic revision per aggregate; not globally comparable |
| Lifecycle transition position | LifecycleEventCursor / D | Per Memory lifecycle stream; store separately from commit cursor |
| Projection progress | IndexWatermark / F | Per index/channel/partition, applied-through CanonicalCommitCursor; E never allocates it |
| Forget suppression generation | ForgetFenceCursor / D | Operation + target-set digest + generation; not a stream cursor |
| Authorization freshness | PermissionEpoch / I | Independent policy/principal/security namespace; recheck at protected boundaries |
| Context state | ContextVersion / G | Opaque downstream dependency; E does not create or increment it |

A SourceEventCursor, outbox dispatch offset, AttemptId, AggregateRevision, LifecycleEventCursor, IndexWatermark, ForgetFenceCursor, PermissionEpoch or ContextVersion MUST NOT be copied into CanonicalCommitCursor. A CanonicalCommitCursor is assigned only at D's successful canonical transaction commit. D's contract states committed positions are contiguous within one Brain authority; rejected/aborted transactions receive no cursor.

## 6. Retry, replay and unknown outcomes

- At-least-once queue delivery is assumed. Stable EventRef/CompileIntentId/ProducerWorkItemId dedupe logical work; AttemptId is new per retry.
- Retry, DLQ requeue, operator replay and recompile all reauthenticate and recheck current PermissionEpoch, Scope, retention and latest applicable ForgetFence.
- A replay preserves source EventRef and original acceptance receipt; it cannot use a fresh queue message or new attempt to escape a prior fence.
- If D admission/registration/commit/publication response is lost, query by the same stable operation identity and digest. Do not create a new key or infer success from timeout.
- If D canonical commit succeeded but E lost ACK, query D by stable canonical operation key and record the exact original CanonicalCommitReceipt.
- If publication outcome is unknown, keep artifact private until PublicationOperationId lookup proves committed success.
- DLQ remains registered and barrier-open while replay/publication is possible. Only a durable terminal disposition can close it.
- Dedup retention must cover supported retry, lease, DLQ, operator recovery and audit horizons; numeric duration and tombstone expiry remain I-owned OPEN decisions.

## 7. Cross-module identity and permission

H requires authenticated transport principal binding. Payload `producer_id`, `ActorRef`, `agent_id` and `scope_ref` are claims/selectors, not credentials. I's candidate ProducerIdentity binds authenticated Principal/issuer, registered producer/application, workload/instance, credential validity/epoch, permitted event families, security domain and revocation state. E requires mismatch rejection/quarantine and never treats payload ProducerId as authentication.

ActorRef and ScopeRef use B/I typed semantics. PermissionEpoch is I-owned; authorization is checked at ingress, before protected source/evidence/provenance dereference, before sensitive stage commits, before D write submission and at final publication. If principal, permission, Scope, security domain or Forget state is unknown, fail closed.

H/I/B packages are CANDIDATE; this document consumes their semantics without freezing wire fields or security policy.

## 8. Conformance plan (NOT RUN)

1. Same key/same digest under same authenticated namespace returns one AcceptedReceipt/EventRef/CompileIntentId.
2. Same key/different digest conflicts without mutation.
3. Lost acceptance ACK returns original receipt; no duplicate work.
4. Accepted does not imply D Producer Registration or Compiler Completion.
5. Compiler completion without canonical commit has no CanonicalCommitCursor.
6. D canonical commit receipt has one D-issued global-per-authority CanonicalCommitCursor and independent AggregateRevision/LifecycleEventCursor.
7. F IndexWatermark is only recorded after F acknowledgement.
8. ACK loss for D registration, canonical commit, dependency registration or publication is recovered by stable operation lookup.
9. Revoked permission or advanced ForgetFence blocks retry/replay/recompile and late result.
10. DLQ and expired lease remain barrier-open until terminal disposition.
11. Staged artifact is never consumer-visible before D registration receipts and final PublicationReceipt.
12. B ADR remains ADR-BLOCKED; no candidate IR auto-promotes to Canonical Claim/Fact.

**Acceptance:** design contract only. Storage atomicity, D callable APIs, runtime behavior and conformance results remain unverified.



---
## Phase 3.5 — Receipt State Matrix and Recovery Refinement

### 1. Independent evidence states

| State/evidence | Durable fact established | Does NOT establish | Recovery owner |
|---|---|---|---|
| Accepted / AcceptedReceipt | Immutable event/payload reference+digest, idempotency record and CompileIntent/outbox are durable | D ProducerWork registration, compile start, candidate output, canonical commit, dependency registration or publication | E |
| DurableIngestion | Source bytes/reference and ingress metadata are durably recoverable under declared storage profile | Compile has started or completed | E/Storage |
| CompileStarted | A named DerivationRunId/AttemptId began after D admission and current auth/fence checks | Candidate exists or any canonical effect occurred | E |
| CandidateProduced | A named candidate/staged artifact and provenance checkpoint exist privately | Runtime visibility, canonical commit, dependency completeness or publication | E |
| CanonicalCommit | D CanonicalCommitReceipt confirms canonical transaction commit with D-issued CanonicalCommitCursor | Derived artifact publication, index application or Forget completion | D |
| DerivedDependencyRegistered | D dependency inventory durably records exact artifact/source edges | Artifact is visible or publication gate passed | D / designated inventory owner |
| DerivedArtifactPublished | Final gate and atomic visibility transition have durable PublicationReceipt | Canonical commit, F index watermark, G ContextVersion or global Forget completion | D/Storage ownership OPEN; E reconciles |

Accepted is a custody/receipt assertion only. It must never be described as compiled, saved to memory, committed or published.

### 2. Receipt and idempotency identity

- AcceptedReceiptId is immutable for one accepted logical submission.
- CallerIdempotencyKey is scoped by authenticated issuer + Principal + ProducerIdentity + security domain + validated Scope binding + operation family. Exact canonical ScopeRef encoding remains B/I/H OPEN.
- SemanticRequestDigest binds immutable payload bytes/digest, event/schema family, authenticated producer binding, validated scope/security domain and semantic source/environment identity. It excludes retry count, transport attempt, timestamp of retry and trace-only metadata.
- CompileIntentId and ProducerWorkItemId are persisted and returned/recovered with the original receipt. A retry does not mint a new logical work ID.
- AttemptId is new for each execution attempt; DerivationRunId is new for each distinct recompile/run lineage.
- Receipt lookup must be authorization-checked; one Principal/Scope must not learn another submitter's receipt existence or payload metadata.

### 3. Duplicate submission and replay matrix

| Condition | Required result | Side effects |
|---|---|---|
| First valid key + digest | Commit one AcceptedReceipt/Event/CompileIntent | One logical submission |
| Duplicate key + same semantic digest | Return original AcceptedReceiptId, EventRef, CompileIntentId, ProducerWorkItemId and current state | No duplicate event, intent or D registration |
| Duplicate key + different semantic digest | Idempotency conflict; original record unchanged | No new compile or canonical effect |
| Duplicate arrives while receipt commit outcome unknown | Resolve by same key/digest; do not create a second key | Hold dispatch until resolution |
| Duplicate after compilation started/completed | Return original receipt plus current evidence references/status | Do not implicitly rerun compile |
| Explicit recompile | New DerivationRunId, current authorization/fence checks, linked to original source and intent; D work-registration shape remains OPEN | New run only; no new AcceptedReceipt |
| Replay after Forget | Policy-safe suppress/reject; do not reconstruct payload or derivative; keep audit metadata non-reconstructive | No visibility or resurrection |
| Receipt tombstone retained after payload expiry/Forget | Return only policy-safe non-content status if authorized | Never recreate Event bytes or compile intent |

### 4. Lost acknowledgement and crash recovery

| Lost/ambiguous boundary | Recovery key | Mandatory behavior |
|---|---|---|
| Accepted transaction ACK | authenticated idempotency namespace + semantic digest | Query existing receipt; do not duplicate acceptance |
| D RegisterProducerWork ACK | ProducerWorkItemId + request digest | No enqueue/lease/run until D lookup returns durable accepted receipt or definitive rejection |
| Compile start/outbox ACK | CompileIntentId + outbox event ID | At-least-once replay; preserve same logical work identity |
| Dependency registration ACK | DependencyRegistrationId + request digest | Keep artifact private; query/resume same registration |
| Publication ACK | PublicationOperationId + request digest | Keep artifact private until committed PublicationReceipt is found |
| D CanonicalCommit ACK | stable canonical operation/idempotency key + digest | Query D and record original CanonicalCommitReceipt/Cursor; never issue a new semantic commit |
| CompleteProducerWork ACK | ProducerWorkItemId + terminal request digest | Barrier remains unresolved locally until D confirms terminal acknowledgement |

A process crash at any boundary must recover from durable intent + stable operation key. Timeouts and lost ACKs are UNKNOWN, never success. No recovery path changes the source lineage, idempotency namespace or fence applicability.

### 5. Cursor namespace reaffirmation

E persists the D-issued CanonicalCommitCursor unchanged as one global sequence per Canonical Memory authority. AggregateRevision remains independently scoped per aggregate; LifecycleEventCursor remains per Memory lifecycle stream; IndexWatermark remains F-owned per index/channel partition; ForgetFenceGeneration remains a D fencing namespace; PermissionEpoch remains I authorization freshness. No numeric comparison, coercion or cursor substitution is permitted across these namespaces.

### 6. OPEN receipt decisions

- OPEN-REC-01: Storage transaction/WAL durability, replication and crash-recovery profile for AcceptedReceipt + payload ref + idempotency row + CompileIntent/outbox.
- OPEN-REC-02: canonical semantic digest algorithm/canonicalization version and B/H typed identity/scope serialization.
- OPEN-REC-03: idempotency/tombstone retention horizon and post-Forget disclosure-safe response policy (I-owned).
- OPEN-REC-04: exact D lookup operations/error codes for producer registration, dependency registration, publication and terminal completion.
- OPEN-REC-05: recompile registration shape (child work item vs new registered item) remains D-owned.



---
## Phase 3.5 Addendum — Producer Ledger Receipt Types

D's ProducerRegistrationReceipt carries ProducerRegistryVersion and ProducerRegistrationSequence. The latter is a per-D producer-ledger ordering token used to prove inclusion in the Forget barrier. It is not the CanonicalCommitCursor and must never be stored in that field or interpreted as a canonical commit position.

InstallForgetFence captures ProducerRegistryVersion + ProducerRegistrationHighWater at its fence-installation linearization point. CaptureProducerRegistrationHighWater returns an immutable BarrierSnapshotReceipt verifying that same cutoff; repeated capture cannot move it. E records both receipt identities and the D snapshot version used for terminal reconciliation.

ResolveProducerWork is the read-only recovery path after lost registration/dependency/publication/terminal ACK. It uses the original stable WorkItemId and registration digest, with optional AttemptId/LeaseId and operation IDs. A missing/ambiguous result is UNKNOWN, not a reason to mint a new work or publication key.

ReconcileForgetBarrier returns D's local barrier disposition and unresolved counts at explicit immutable checkpoints. E supplies complete evidence but does not declare the barrier drained itself. A later-discovered derivative or ledger gap requires a new append-only reconciliation checkpoint and invalidates any prior current proof.

The receipt evidence matrix is therefore extended with:
- ProducerClassRegistrationReceipt + ProducerRegistryVersion;
- ProducerRegistrationReceipt + ProducerRegistrationSequence;
- ForgetFenceCursor + installation CanonicalCommitCursor;
- BarrierSnapshotReceipt + ProducerRegistrationHighWater;
- DependencyRegistrationReceipt + dependency inventory position;
- PublicationReceipt + visibility commit identity;
- ProducerWorkTerminalReceipt + D barrier reconciliation cursor.

All of these remain distinct typed evidence objects. None is interchangeable with AggregateRevision, LifecycleEventCursor, IndexWatermark, ForgetFenceGeneration, PermissionEpoch or ContextVersion.



---
## Phase 3.5 Addendum — Receipt OPEN Item Correction

D's normative operation document now specifies semantic lookup and receipt behavior for RegisterProducerClass, RegisterProducerWork, InstallForgetFence, CaptureProducerRegistrationHighWater, RegisterDerivedDependency, PublishDerivedIfFenceCurrent, CompleteProducerWork, ResolveProducerWork and ReconcileForgetBarrier. Therefore OPEN-REC-04 is narrowed: D semantic lookup identities, receipt classes and error outcomes are specified; callable API/transport schemas, authentication serialization and wire error mapping remain OPEN under OPEN-API-01. Storage/Consistency atomic visibility and recovery remain OPEN under OPEN-STORAGE-01.

The AcceptedReceipt's own durable commit profile remains separately OPEN under OPEN-REC-01. D producer-ledger receipt durability does not substitute for the E ingress transaction, and an AcceptedReceipt does not imply a D ProducerRegistrationReceipt.
