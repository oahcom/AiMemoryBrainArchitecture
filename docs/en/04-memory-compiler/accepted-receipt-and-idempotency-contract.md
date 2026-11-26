---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-110/restore-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Existing language mirror; only GOV-DOC-002 frontmatter is added. Body bytes are preserved."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Accepted Receipt, Compiler Completion and Idempotency Contract"
    canonical_scope_id: "memory-compiler/accepted-receipt-idempotency"
    canonical_scope_keywords:
      - "accepted-receipt-idempotency"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "04-memory-compiler/accepted-receipt-and-idempotency-contract.md"
    en: null
    zh-CN: "docs/zh-CN/04-memory-compiler/accepted-receipt-and-idempotency-contract.md"
---
# Accepted Receipt, Compiler Completion and Idempotency Contract

- Document ID: E-RECEIPT-001
- Version: 1.0
- Source branch: session-e-memory-compiler-2026-11-16
- Source revision: DEREFERENCED — historical source blob `5ca77a5b48e69afb3bc81429baf538be7dce4d46` retained; no current normative source path exists.
- Source: DEREFERENCED — original normative path `04-memory-compiler/accepted-receipt-and-idempotency-contract.md` is absent from the current main tree; alternative: [surviving Chinese counterpart](../../zh-CN/04-memory-compiler/accepted-receipt-and-idempotency-contract.md) (blob `fa8c005a6b8c599c10e71150fb2056d5685e76fd`; translation only, not an authoritative substitute).
- Chinese counterpart: [Accepted Receipt、Compiler 完成与幂等契约](../../zh-CN/04-memory-compiler/accepted-receipt-and-idempotency-contract.md)
- Status: CANDIDATE E contract; Storage realization, D producer APIs, H envelope and I policy approval remain OPEN

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


---

## Phase 3.5 Revalidation — Receipt State Matrix and Replay

| State / evidence | Durable fact established | Does not establish | Recovery rule |
|---|---|---|---|
| DurableIngestion | Immutable EventRef and payload bytes/reference/digest are durably stored and integrity-checked | AcceptedReceipt, compile intent/start or canonical effect unless separately committed | Recover by EventRef+payload digest; orphan private payload is not accepted work |
| Accepted / AcceptedReceipt | Event + immutable payload ref/digest + authenticated idempotency row + AcceptedReceipt + CompileIntent/outbox committed atomically or by proven recoverable WAL | D ProducerWork registration, CompileStarted, CandidateProduced, CanonicalCommit, dependency registration or Published | Same authenticated namespace/key/digest returns original receipt and IDs; changed digest conflicts |
| CompileStarted | Named DerivationRunId/AttemptId began after D admission and fresh auth/fence checks | Candidate, canonical commit or publication | Recover same WorkItem/CompileIntent; new AttemptId only for a new execution |
| CandidateProduced | Candidate/staged artifact and provenance checkpoint exist in private staging | Runtime visibility, canonical commit, complete dependency inventory or publication | Resolve same artifact/version and dependency operation IDs; never expose staging |
| CanonicalCommit | D CanonicalCommitReceipt confirms canonical transaction and returns D-issued CanonicalCommitCursor | Derived publication, F indexing, G Context or Forget completion | Resolve same canonical operation identity after lost ACK |
| DerivedDependencyRegistered | D inventory durably records complete artifact/source/parent edge set and position | Visibility or publish-gate success | Resolve same DependencyRegistrationId+digest; partial/unknown remains private |
| DerivedArtifactPublished | D final gate + atomic visibility boundary has durable PublicationReceipt and visibility commit identity | F IndexWatermark, G ContextVersion, global Forget completion or physical erasure | Resolve same PublicationOperationId+digest; ambiguous result remains private |
| CompilerTerminal | D ProducerWorkTerminalReceipt accounts for every output and proves no attempt can publish later | Forget barrier drained unless D ReconcileForgetBarrier says so | Resolve same WorkItemId+terminal digest; conflict is immutable |

### Duplicate submission and replay

- Candidate idempotency namespace remains pending B/H/I agreement: authenticated issuer + Principal + ProducerIdentity + security domain + validated Scope binding + operation family + caller key. Payload ActorRef/ProducerId/ScopeRef are claims, never authentication.
- Same namespace/key + same semantic digest returns original AcceptedReceiptId, EventRef, CompileIntentId, ProducerWorkItemId and current authorized status; no second event, registration, compile or canonical side effect.
- Same namespace/key + different digest returns IDEMPOTENCY_CONFLICT and leaves original immutable.
- Unknown receipt commit is resolved using the same namespace/key/digest; do not mint a new key, return optimistic success or dispatch duplicate work.
- Receipt lookup is authorization-checked; another Principal cannot enumerate receipt existence or payload metadata.
- Outbox/DLQ replay preserves EventRef, CompileIntentId and ProducerWorkItemId; AttemptId changes only for a new execution. Replay after Forget is reauthorized and re-fenced; it cannot reconstruct forgotten payload.
- Recompile is not duplicate Accepted submission: new linked DerivationRunId, no new AcceptedReceipt, and OPEN-RECOMPILE-01 governs child WorkItem re-admission.
- Lost D registration/dependency/publication/terminal ACKs use the original operation ID/digest. UNKNOWN keeps artifact private and work barrier-open.

Canonical digest profile, typed identity serialization, retention horizon and post-Forget receipt disclosure remain OPEN with B/H/I/Storage. No wire schema or retention duration is frozen.


### Typed cursor and fence-generation namespace — explicit E contract

| Token | Owner and scope | E treatment |
|---|---|---|
| CanonicalCommitCursor | D; one globally ordered sequence per Canonical Memory authority | Store the exact D-issued value only after successful canonical commit. |
| AggregateRevision | D; independent sequence per aggregate | Store separately with its aggregate identity; never use as global commit order. |
| LifecycleEventCursor | D; independent append-only stream per Memory | Store only when a lifecycle event exists; preserve its Memory scope. |
| IndexWatermark | F; per index/channel partition, applied-through CanonicalCommitCursor | E supplies source/outbox events but never allocates or advances it. |
| ForgetFenceGeneration | D; monotonic generation in the ForgetFence namespace, bound through ForgetFenceCursor to ForgetOperationId and target-set digest | Treat as a fence token, not a commit cursor or work-registration sequence. Validate freshness only through D semantics. |
| ProducerRegistrationSequence / ProducerRegistrationHighWater | D; producer-work ledger and one Forget barrier cutoff | Store separately; never substitute for CanonicalCommitCursor or ForgetFenceGeneration. |
| PermissionEpoch | I; policy/security domain | Revalidate through I; never compare numerically with D fence generation. |
| ContextVersion | G; managed Context | Opaque downstream reference; E does not allocate it. |

No arithmetic, numeric comparison, coercion or token substitution is permitted across these namespaces. In particular, a fence installation may itself carry an installation CanonicalCommitCursor for audit, but that cursor does not define or replace ForgetFenceGeneration.


---

## Phase 3.6 — Receipt Semantics and Durable Recovery

### 1. Receipt stages are independent evidence

| Stage | Receipt/evidence | What it proves | What it does not prove |
|---|---|---|---|
| Accepted | AcceptedReceipt | E durably accepted the authenticated logical submission under the declared ingress contract | Payload bytes durable unless the receipt contract explicitly includes that profile; D producer admission; compile start; candidate; canonical commit; dependency registration; publication |
| Durable Ingestion | DurableIngestionReceipt / immutable EventRef + payload digest and storage durability evidence | Source bytes/reference and ingress metadata are durably recoverable under the declared storage profile | Accepted, queued, compile started or any canonical/derived effect |
| Compile Started | CompileStarted evidence bound to WorkItemId, DerivationRunId, AttemptId, LeaseId | A named admitted attempt began after current authorization/fence checks | Candidate produced, dependency registered, canonical commit or publication |
| Candidate Produced | CandidateProduced evidence | A candidate/IR/provenance checkpoint exists privately for the named run | Staging visibility, dependency completeness, canonical commit or publication |
| Dependency Registered | D DependencyRegistrationReceipt | Complete artifact/version and required lineage edges are durably recorded in D inventory | Final gate passed or artifact visible |
| Canonical Commit | D CanonicalCommitReceipt + CanonicalCommitCursor | D committed the named canonical mutation | Derived artifact publication, index application, Context activation or global Forget completion |
| Derived Artifact Published | D/Storage PublicationReceipt + visibility commit identity | Exact artifact/version passed final gate and became visible at the atomic visibility commit | Canonical commit unless separately referenced; F IndexWatermark; G ContextVersion; global Forget completion or physical erasure |

**CompilerCompletionReceipt** is an E roll-up referencing whichever stage receipts actually exist. It cannot upgrade CandidateProduced into DependencyRegistered, CanonicalCommit or Published. Each stage is append-only and independently resolvable.

### 2. ACK semantics

- Transport ACK / HTTP 2xx / queue ACK proves only the transport or queue's stated receipt.
- Accepted is returned only after the E acceptance linearization point (Event + immutable payload ref/digest + idempotency row + AcceptedReceipt + CompileIntent/outbox) is durable under the declared transaction/WAL profile.
- Durable Ingestion is separate when payload durability precedes metadata acceptance or uses a separate storage system.
- RegistrationReceipt proves D admission only.
- DependencyRegistrationReceipt proves complete dependency registration only.
- PublicationReceipt proves the atomic visibility transition only.
- F IndexAppliedAcknowledgement proves only the named F partition's contiguous applied prefix.

### 3. Unknown outcomes and retry identity

For every operation, timeout/lost ACK is UNKNOWN, not failure or success. Recovery uses the original operation ID and canonical request digest:

- Accepted: authenticated idempotency namespace + caller key + semantic digest.
- Producer registration: WorkItemId + registration digest.
- Lease: WorkItemId + AttemptId + LeaseId/lease epoch.
- Dependency registration: DependencyRegistrationId + dependency digest.
- Canonical commit: D canonical operation ID + request digest.
- Publication: PublicationOperationId + publication digest.
- Terminal completion: WorkItemId + terminal digest.

Same identity + same digest returns the original immutable receipt/outcome. Same identity + changed digest is a conflict. No timeout recovery mints a replacement WorkItemId or PublicationOperationId.

### 4. Crash / replay matrix

| Failure | Recovery behavior | Visibility/barrier rule |
|---|---|---|
| Accepted ACK lost | Resolve same idempotency namespace/key/digest and return original AcceptedReceipt if committed | Do not duplicate Event, receipt or CompileIntent |
| Durable ingestion ACK lost | Resolve EventRef/payload digest and storage durability record | Orphan staged payload is not accepted work |
| Worker crash | Expire/revoke lease; preserve WorkItemId; create new AttemptId/LeaseId after current auth/fence recheck | Old attempt cannot publish; work remains barrier-open |
| Lease expiry | Treat old lease as invalid, not work terminal; resolve D state before takeover | No barrier closure |
| Duplicate attempt | Enforce attempt/lease epoch and one active publication identity; stale attempt is rejected at final gate | No double publication |
| DLQ replay | Same WorkItemId, new AttemptId/LeaseId; fresh auth/fence checks and same D registration | DLQ remains barrier-open until terminal receipt |
| Outbox replay | At-least-once dispatch using stable outbox event/operation identity; resolve D receipt before action | No duplicate logical work |
| Recompile | Same WorkItemId and original source lineage; new DerivationRunId and immutable artifact version; current auth/fence checks | Cannot reset fence applicability or receipt stage |
| Dependency partial commit | Resolve same DependencyRegistrationId/digest; finish complete set or quarantine | No partial visibility |
| Canonical commit ACK lost | Resolve same D canonical operation ID/digest | Never issue a second canonical mutation |
| Publication ACK lost | Resolve same PublicationOperationId/digest; distinguish committed/aborted/unknown | Unknown remains private; committed returns original PublicationReceipt |
| Crash after final transaction commit before local state update | Read authoritative visibility marker + PublicationReceipt by stable operation ID | If committed, reconcile local state; never republish |
| Crash during separate-store prepare/commit | Recover coordinator and all participant records idempotently; prepared remains hidden until committed | No visibility from a prepare record or stale token |
| Restore/rebuild | Quarantine projections/staging; replay current fence/permission control state before serving | No resurrection |

### 5. Terminal and reconciliation

A work item is not terminal merely because a worker returned, queue entry disappeared, lease expired, retry budget exhausted or a local completion event was written. E submits CompleteProducerWork only after every run, attempt, staged artifact, dependency registration, canonical operation, publication operation, outbox and DLQ replay path is resolved. D ProducerWorkTerminalReceipt is required before E marks D barrier disposition terminal.

### 6. Conformance status

The Phase 3.6 cases in `phase-3.6-producer-publication-conformance.md` are **NOT RUN**. Documentation and repository readback do not establish transaction correctness, no-resurrection behavior or runtime fault safety.
