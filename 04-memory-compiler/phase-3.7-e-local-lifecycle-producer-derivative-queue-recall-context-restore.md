# Phase 3.7 — E Local Lifecycle: Producer, Derivative, Queue, Recall, Context and Restore

- Owner: E — Memory Compiler
- Branch: `session-e-memory-compiler-2026-11-16`
- Status: **E-local semantic proposal; D/E/Storage publication gate and cross-owner schemas remain OPEN / NOT VERIFIED**
- Scope: source-event ingestion, compiler work, derived artifact production, compiler queues/outboxes, compiler source recall, compiler input context and restore.
- Authority boundary: D owns canonical Memory, ForgetFence, producer registry and dependency inventory; I owns authorization/PermissionEpoch; E owns compilation; F owns runtime retrieval/index projections; G owns user-facing Context and Applied/Delivery; H owns wire/adapter capability; Storage owns agreed durable transaction/visibility realization.

## 1. E's local lifecycle model

E is a derivative producer, not the canonical authority. Accepted input, compiler completion and a locally stored artifact do not make an artifact visible.

| Object | E-local states | Terminal / non-terminal meaning |
|---|---|---|
| Producer intent | Received → Validating → Accepted → RegistrationPending → Registered → Queued → Leased → Running → Staged → DependencyRegistered → GatePending → Published / Suppressed / Rejected | Dead-letter, timeout, lease expiry and worker loss are non-terminal until no-publication disposition is durable |
| Derivation | Planned → Executing → CandidateProduced → Validated → PrivateStaged → LineageBound → PublicationPending → Published / Quarantined / Discarded | Every recompile is a new DerivationRun; prior outputs remain immutable |
| Queue/outbox | Enqueued → Leased → Dispatched → Acked / Retry / DLQ / Cancelled | Queue ACK is not compiler success, canonical commit, publication or D barrier closure |
| Source recall | Requested → Authorized → SourceResolved → EvidenceBound → ReturnedToCompiler / Blocked | Compiler source recall is not user Recall and never bypasses D/I checks |
| Compiler input context | Assembled → ProvenanceChecked → ScopeChecked → Budgeted → FrozenForRun → Consumed / Invalidated | E's run input bundle is not G ContextVersion or F Working Set |
| Restore unit | Discovered → Isolated → PrefixReconciled → LedgerReconciled → ReplayValidated → PrivateRebuilt → PublicationGate → Enabled | No restored staged artifact/outbox is exposed before reconciliation |

## 2. Producer behavior

1. E registers each derivative-capable logical work item with D before queue insertion, lease, source dereference or execution. Required binding: stable ProducerWorkItemId, producer class/identity, CompileIntentId, source EventRef(s)/exact Memory refs, ScopeRefs, complete known lineage, request digest, admission CanonicalCommitCursor, observed ForgetFence and I PermissionEpoch.
2. AcceptedReceiptId proves E durable ingress only; it does not prove D producer registration. Registration uncertainty is resolved by stable WorkItemId+digest.
3. Retry preserves ProducerWorkItemId and request digest; AttemptId and LeaseId change. Recompile creates a new DerivationRunId and immutable output version, with fresh authorization/fence checks and a D-governed registration relation. It cannot escape the original source lineage or Forget barrier.
4. Every terminal outcome is explicit and durable: Published, RejectedBeforeAdmission, CancelledNoPublication, SuppressedByFence, FailedNoPublication or other D-approved disposition. DLQ, timeout, retry exhaustion and process death are not terminal.
5. D's pre-fence producer high-water remains open until D accepts terminal/no-publication evidence. E cannot remove registrations or self-close the barrier.
6. Unknown D/I authority or registration outcome fails closed; do not execute derivative-capable work speculatively.

## 3. Derivative behavior

- Derivatives include normalized claims, extracted entities/relations, evidence spans, summaries, embeddings, provenance edges, compiler proposals, staged canonical candidates, and any durable outbox/cache artifact that can later expose or regenerate source-derived content.
- Each immutable DerivedArtifactRef/version binds ProducerWorkItemId, DerivationRunId, source EventRef and exact source versions, complete transitive lineage, provenance, Scope, policy epoch, schema/model/compiler versions and content digest.
- Keep candidate outputs private/non-queryable until dependencies are durably registered with D and the authoritative publication gate succeeds against the current D fence and I permission.
- A derivative whose dependency set is incomplete, ambiguous or unresolvable is quarantined, not partially published.
- Same dependency-registration key+same digest is idempotent; same key+different digest is conflict. No mutable overwrite of a published artifact; changed output creates a new immutable version.
- Forget/revocation causes immediate logical suppression of affected artifacts, blocks late publication, and initiates governed cleanup. E cannot claim F index purge, G Context removal, physical byte erasure or global completion.

## 4. Queue and outbox behavior

- Queue entries are durable references to registered work, not authorization. The payload binds WorkItemId, digest, source refs, lineage digest, Scope, schema and attempt/lease generation.
- At-least-once dispatch is expected. Stable identity+digest deduplicates; changed digest conflicts. Stale leases cannot publish.
- D registration must precede enqueue. If queue insertion succeeds but registration is uncertain, quarantine and resolve by stable identity; never run.
- Retry/DLQ preserves the open producer registration. A new attempt is not a new logical work item.
- Before execution, source reads, dependency registration and publication, revalidate current I PermissionEpoch and D fence. A final gate must serialize with visibility; local check-then-publish is forbidden.
- Restore quarantines queue/outbox records until COC prefix, D producer ledger/high-water, I policy and Storage participant/visibility records reconcile. Unknown gaps block replay.

## 5. Recall behavior

- E's Recall is narrowly defined as compiler source/evidence resolution: fetch exact authorized EventRef/MemoryVersionRef and provenance required for a specific DerivationRun.
- It is not interactive/user recall, ranking, context delivery or an authorization grant. F owns runtime retrieval; G owns Context selection.
- Every source read is bound to authenticated producer identity, purpose, Scope, I PermissionEpoch and D fence; revalidate source lifecycle and lineage before dereference.
- Resolve exact source revisions. Do not silently float a reference to a newer version or substitute a preferred claim. Superseded/retracted/forgotten/unauthorized sources are blocked or explicitly classified.
- Incomplete source coverage is recorded as incomplete; absence in a search/index result is not proof that a source does not exist.
- Evidence/provenance remains attached through extraction, normalization, consolidation and output. Compiler outputs cannot promote untrusted source text into privileged instructions.

## 6. Context behavior

- E owns only the immutable compiler input bundle for one DerivationRun: selected source refs, evidence/provenance, exact versions, Scope, policy epoch, compiler/model/schema versions, budget and deterministic input digest.
- Freeze the input bundle before execution. Any changed source, permission, fence, schema or model configuration requires a new run identity/input digest and fresh validation.
- This bundle is not G's desired Context, ContextVersion, Snapshot/Delta, Delivery or Applied record, and not F's retrieval Working Set.
- E may request source candidates from F or provide validated derived refs to G; F decides retrieval mechanics, G decides Context membership and delivery. E cannot declare a user-facing recall result or Applied state.
- No cross-Scope mixing. If source provenance or scope is uncertain, do not compile/publish.

## 7. Restore and replay

1. Restore event log, compiler state, staged artifacts, queue/outbox and dependency manifests into quarantine/private storage.
2. Verify Storage restore/participant evidence and reconcile the COC committed prefix, D producer registration/dependency high-waters and I PermissionEpoch/revocation/registry state. These are separate typed authorities.
3. Preserve the same CompileIntentId, ProducerWorkItemId, request digest, PublicationOperationId, PreparedParticipantRef and PreparedTransactionGID where a prepared publication exists. AttemptId/LeaseId may change; immutable transaction tuple may not.
4. Resolve every in-flight item by stable identity. Never infer completion from missing queue message, expired lease, absent receipt or stale replica.
5. Revalidate source revisions, complete lineage, Scope, policy, ForgetFence and model/schema compatibility. Rebuild only private artifacts.
6. Re-register/reconcile dependencies idempotently; final publication must pass the current D/I gate. If pointer/receipt/GID/authority disagree, remain quarantined.
7. Reconcile post-restore events before opening queue consumers or exposing artifacts. Unknown continuity means no replay/no publication.
8. A RestoreReconciliationReceipt is not a PublicationReceipt, D clearance, I authorization, COC terminal decision or global Forget completion.

## 8. Evidence and tests

E emits AcceptedReceipt, producer registration receipt reference, immutable run/attempt identities, source/input digest, dependency receipts, publication operation/result, terminal no-publication disposition, queue state and restore reconciliation outcome. D alone closes its barrier; Storage alone supplies its agreed transaction evidence.

Required tests: register-before-enqueue crash; enqueue-before-ACK; duplicate delivery and changed digest; stale lease publication; retry/DLQ across Forget fence; incomplete transitive lineage; revocation during compilation; gate-vs-fence race; restore with stale prefix/participant ledger; recompile after source supersession; unknown GID resolution. These are required specifications, not claims of executed tests.

## 9. Non-goals / blockers

- E does not own canonical truth, Forget decisions, user-facing Recall, F indexes, G Context/Applied, H ACK or I authorization.
- D/E/Storage atomic registration/dependency/final publication gate remains **BLOCKING** until callable schemas and crash-safe linearization are agreed and verified.
- **No compiler implementation, conformance PASS, production restore or publication activation is claimed.**
