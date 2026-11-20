# Context Versioning and Change Sets

**Status:** DECIDED invariants; CANDIDATE object encoding and serialization policy  
**Owner:** Session G  
**Related:** INT-P1-01, INT-P1-05, C review P2-05/P2-06

## 1. Guarantees

A Context Version is immutable and identifies one complete desired managed-region state. Each Context has one authoritative monotonically increasing sequence. Every committed Change Set identifies Base Version and Target Version. Concurrent mutations cannot silently overwrite; commit uses CAS or equivalent per-Context serialization. Snapshot and Delta represent the same target state; Delta is not independently authoritative. Adapter Applied is separate from Context head.

## 2. Context Version Object

| Field | Meaning |
|---|---|
| context_version_id | Globally unique opaque immutable version ID |
| context_id | Owning Context |
| sequence | Monotonic per-Context integer; never reused |
| parent_version_id | Immediate prior version; null only for genesis |
| snapshot_ref / snapshot_hash | Immutable complete entry snapshot and canonical digest |
| schema_version | Context domain schema |
| scope_fingerprint | Non-reversible binding to resolved Scope/identity/policy epoch |
| canonical_watermarks | Per-source/partition canonical revision watermark |
| policy_epoch | Authorization/policy epoch used at commit |
| committed_change_set_id | Change Set that created this version |
| committed_at | Brain commit time |
| actor_ref / reason | Authenticated principal/service and rationale |
| entry_count / budget_summary | Reproducible aggregate metadata |

Snapshot contains complete ordered Entry state and required membership tombstones. Payloads remain immutable refs or governed projections; permissions are rechecked at every use.

## 3. ContextEntry Version

An Entry is versioned inside each immutable Context Version. Stable identity is scoped to Context; each appearance has an entry revision:
- entry_id, context_id;
- memory_id and exact memory_version (never implicit latest);
- rendering_ref/projection_schema_version;
- tier, priority, position;
- activation_reason and activation_correlation_refs;
- epistemic_status, lifecycle_state, trust and classification;
- source_refs/evidence_refs (typed and permission-checked);
- content_hash, token_estimate, byte_size;
- activated_at, expires_at, valid_time;
- entry_revision, created_by_change_set_id, last_changed_by_change_set_id;
- entry_state and invalidation_reason.

A version pin prevents silent content drift but does not override retraction, Forget or permission revocation.

## 4. ContextChangeSet Object

| Field | Meaning |
|---|---|
| change_set_id | Unique immutable mutation request ID |
| context_id | Target Context |
| base_version | Exact expected Context Version |
| target_version | Allocated only after successful commit |
| operations | Ordered typed operations with stable operation IDs |
| reason | Trigger/business rationale, not arbitrary instruction |
| actor_ref | Authenticated caller/service |
| created_at | Request creation time |
| idempotency_key | Scoped retry identity |
| payload_hash | Hash of normalized request |
| policy_epoch | Authorization epoch checked |
| status | Prepared, Committed, Rejected, Conflict or Aborted |
| correlation_id / causation_id | Cross-system trace linkage |
| result_ref | Immutable operation result/diagnostics |

Target Version is absent before commit; callers cannot guess it from Base+1.

## 5. MemoryContext required object

Required fields: context_id, scope, agent_instance_id, task_id, environment_id, context_version, applied_version, status, budget, created_at, updated_at, expires_at.

Required semantic extensions: agent_id, session_id, principal_scope_ref, project_scope_ref, purpose/profile, schema_version, policy_epoch, canonical_watermarks, last_reconciled_at.

The applied_version field is only a convenience projection. Authoritative application history is per ContextDelivery/Adapter/Context Session/Inference Request; one Context may have multiple consumers at different versions.

## 6. ContextDelivery required object

Required fields: delivery_id, context_id, change_set_id, base_version, target_version, status, timestamps and error.

Semantic extensions: adapter_id, agent_instance_id, agent_context_session_id, inference_request_id, capability_epoch/tier, applied_coverage, managed_region_hash, final_request_hash or privacy-safe attestation ref, boundary_id/timestamp, correlation_id, forget_clear_state and application authorization epoch.

Applied requires explicit Adapter confirmation that the exact target version is completely materialized in the controlled managed region and that this region belongs to the final request submitted to inference runtime. If Adapter cannot observe that final request boundary, it MUST report Unknown or lower capability; it MUST NOT claim Tier 1. A digest is insufficient unless H/C define canonicalization, capture and correlation.

## 7. Snapshot and Delta

- **Snapshot:** complete desired state at Target Version. Required for genesis, gap recovery, unknown base, capability change or unsafe Delta reconciliation. Every canonical reference still requires current authorization.
- **Delta:** ordered operations from exact Base to Target, with base/target hashes, operation IDs and schema version. Apply atomically; duplicate Delivery ID returns prior outcome. Base mismatch rejects and requests Snapshot.
- Delta is not best effort: unknown operation, missing entry, hash mismatch or authorization failure rejects the whole update by default.
- Replaying a Change Set into a different head requires re-planning and a new Change Set, not blind replay.

## 8. CAS, concurrency and idempotency

Recommended initial policy: serialize commits per Context, with CAS on Base Version as a defensive check.

1. Normalize request and compute payload hash.
2. Resolve idempotency key within principal + context + operation family/retention window.
3. Existing key + same hash returns original result/Target Version.
4. Existing key + different hash returns IDEMPOTENCY_KEY_REUSE.
5. Verify current head equals Base Version; else BASE_VERSION_MISMATCH and re-read/replan.
6. Validate all operations against one staged snapshot.
7. Atomically commit Change Set, immutable Version, audit and outbox.
8. Advance head once; no partial commit.

No automatic merge is assumed. Safe rebase is a new Change Set after re-reading canonical and policy state.

## 9. Delivery lifecycle and late acknowledgements

Prepared → Delivered → Applied; alternatives: Rejected, Expired, Superseded.
- Prepared: package materialized/authorized, not confirmed sent.
- Delivered: transport/receiver receipt only.
- Applied: explicit proof satisfies §6.
- Rejected: Adapter refused/validation failed.
- Expired: TTL elapsed before valid application.
- Superseded: newer target replaces it before application.

Timeout is Unknown, not Rejected or Applied. Query by Delivery ID. Late Applied for a superseded version is historical evidence but cannot roll desired head backward; latest Snapshot may be required before next inference.

## 10. Rollback, supersede and replay

Committed versions are never mutated/deleted to roll back. Rollback is a new compensating Change Set after reauthorization/current canonical validation. Supersede creates a new version and marks obsolete undelivered deliveries Superseded. Replay rebuilds the chain from snapshots/Change Sets/audit/outbox; it never reuses stale authorization or bypasses Forget tombstones.

## 11. Applied coverage

- **Full:** complete target version in managed region; exact final request boundary observed; request/session/capability correlation valid.
- **Partial:** identified subset applied; never equivalent to full-version Applied.
- **Bypassed:** inference proceeded without Brain-managed region or used unmanaged fallback.
- **Unknown:** insufficient visibility, timeout, lost evidence, offline Adapter or ambiguous boundary.

Only Full may set Delivery status Applied under strict semantics. Partial/Bypassed/Unknown are non-Applied coverage outcomes. Applied does not establish model attention or use.

## 12. Decision register

- **DECIDED:** immutable versions, monotonic sequence, one authoritative head, explicit base/target, CAS/serialization, atomic Change Set, replayable audit.
- **DECIDED:** Applied ties delivery + session + request + capability epoch + final boundary proof.
- **CANDIDATE:** serialized writer per Context plus CAS.
- **TO_VALIDATE:** snapshot/delta size, hash canonicalization, retry retention and contention.
- **OPEN:** proof/digest fields (C/H); canonical revision watermark schema (D/E/F).


## 13. Phase 3.5 typed cursor, producer and attestation extensions

### 13.1 Typed cursor registry consumed by G

| Field/reference | Authority | Semantics and constraint |
|---|---|---|
| CanonicalCommitCursor | D | One Brain-authority commit ordering cursor; source for canonical reconciliation, not a Context sequence |
| ForgetFenceCursor | D | Opaque tuple identifying ForgetOperation, fence generation and target-set digest |
| ProducerRegistrationSequence / ProducerRegistrationHighWater | D | D producer work ledger admission order and per-operation barrier cutoff |
| ProducerRegistryVersion | D | Version of enabled producer classes |
| PermissionEpoch | I | Opaque policy-domain authorization/revocation epoch with currentness validation |
| ProducerDomainInventoryEpoch | I | Global producer/recipient inventory revision |
| TargetInventorySeal / TargetId | I | Immutable inventory seal and stable target identity; G never creates either |
| IndexWatermark | F, per index and partition | Contiguous canonical publication coverage for that exact partition |
| ContextVersion sequence | G, per Context | Desired Context state ordering only |
| DeliveryId / DeliveryAttemptId | G | Logical delivery identity and distinct attempt identity |
| CapabilityEpoch | H | Adapter instance capability/proof epoch |
| InferenceRequestId / FinalRequestBoundaryId | C/H | Actual final request and boundary evidence |

These values are opaque, typed and authority-scoped. No arithmetic, max(), comparison or cursor substitution across namespaces is valid. In particular, F's maximum partition watermark cannot stand in for a vector of per-partition watermarks, D's ProducerRegistrationHighWater cannot stand in for CanonicalCommitCursor, and I's inventory epoch cannot stand in for D's per-Forget work barrier.

### 13.2 Producer work and artifact publication fields

For derivative-capable G work, retain:
- producer_class_id and producer_registry_version;
- producer_work_item_id and canonical_request_digest;
- registration_receipt_ref and producer_registration_sequence;
- attempt_id / lease_id and derivation_run_id where applicable;
- source_memory_refs with exact MemoryVersionRefs and transitive lineage digest/ref;
- scope_refs and context_id;
- observed_forget_fence_cursor and canonical_commit_cursor;
- permission_epoch and authorization_decision_ref;
- derived_artifact_ref/version, dependency_registration_receipt_refs;
- publication_operation_id/receipt_ref and visibility disposition;
- complete/unknown dependency and terminal-work disposition.

G's producer work registration precedes queueing, leasing, protected source dereference and execution. Retry preserves WorkItemId/digest. D's semantic operation receipts are owner-controlled; this document does not invent their wire or storage schema.

### 13.3 Protected visibility and storage atomicity

#### Normative source and lineage

This section is the canonical root-level normative
source for G Claim/Fact protected visibility.

The bilingual EN/ZH Claim/Fact Context Visibility
Addendum is merged into this section. Its normative
requirements are not an independent competing
protocol.

The paired EN/ZH documents MUST remain synchronized
with this section. If textual drift occurs, this
root section controls until the paired documents
are corrected.

Lineage: the merged requirements originate from
the Phase 3.8.27 G Claim/Fact Context Visibility
Addendum and the AID-2026-014 R5 correction.

#### 1. Ownership and exact references

The logical Context commit remains G-owned and
creates one immutable ContextVersion.

A ContextVersion referencing ClaimRevision,
FactRevision or derived artifacts MUST bind exact
immutable revision references and the applicable
ForgetFenceCursor.

G MUST NOT substitute a current Claim head for
a pinned ClaimRevisionRef.

#### 2. Required protected ordering

The shared protected publication order is:

1. Resolve authorization and Scope.
2. Evaluate D Forget Fence and perform Producer
   Admission under the serialized admission boundary.
3. Durably register the complete dependency set.
4. Stage E artifacts privately.
5. Commit canonical ClaimRevision/FactRevision.
6. Associate dependency registration and
   Publication Intent with the committed revisions.
7. Complete E publication idempotently.
8. Advance Storage visibility only after required
   canonical and dependency evidence is confirmed.
9. Commit G ContextVersion using exact canonical
   revision references.
10. Mark logical completion only after all
    required visibility conditions are satisfied.

#### 3. T17 — Fence-first

If a Forget Fence linearizes before Producer
Admission, the affected work MUST NOT be admitted.

No staging, canonical commit, publication intent,
E publication or Storage visibility transition
may bypass the Fence decision.

#### 4. T18 — Participant-first

Once Producer Admission successfully linearizes,
the exact operation MUST be durably recorded
as an authoritative participant.

Successful Producer Admission and durable recording of
the exact admitted participant MUST form one indivisible
operation under the authoritative serialized
Fence/Admission boundary.

A subsequent Forget Fence MUST NOT linearize or complete
its participant-barrier evaluation until the admitted
participant record is durably visible to that barrier.

Participant recording failure MUST prevent Admission
from reporting success.

A Fence MUST NOT ignore an admitted operation whose
participant recording is incomplete or unresolved.

UNKNOWN MUST remain non-final.

Recovery MUST use the original Operation identity.

The Fence MUST record an auditable completion or
suppression disposition for every admitted participant.

The six-component protected publication failure
matrix in D memory-versioning.md §16.1 is normative
for G ContextVersion commits derived from
protected Claim/Fact content.

G MUST NOT commit or expose a ContextVersion
before the corresponding participant-barrier
and Storage visibility conditions are resolved.

A later Forget Fence MUST NOT silently skip,
erase or misclassify that participant.

The Fence/Admission barrier MUST account for
the participant and preserve its exact identity,
dependency closure and auditable disposition.

The final completion or suppression decision
MUST follow the declared Forget policy.

UNKNOWN MUST remain non-final until the
authoritative outcome is resolved.

#### 5. G protected commit requirements

G MUST:

- Revalidate current I authorization.
- Revalidate the applicable D Forget Fence.
- Verify all referenced Claim/Fact revisions.
- Verify complete dependency-registration receipts.
- Verify exact Storage visibility outcome where
  the Context includes a published artifact.
- Commit the immutable ContextVersion through
  the protected visibility protocol.
- Publish only after authoritative commit resolution.

G MUST NOT expose a new ContextVersion based only
on a local pre-check followed by an independent,
unprotected head update.

#### 6. Historical visibility

A ContextVersion committed before a later Forget
does not grant perpetual access.

Historical Context reads and replay MUST
re-evaluate current authorization and Forget
suppression.

A forgotten ClaimRevision MUST NOT be disclosed
through an existing FactRevision or historical
ContextVersion.

#### 7. UNKNOWN and recovery

UNKNOWN commit or lost acknowledgement MUST
remain non-final.

Recovery MUST resolve the same operation and
exact ContextVersion identity.

No retry may create duplicate visible
ContextVersion state.

Recovery MUST reconcile Fence, Admission,
dependency registration, canonical commit,
E publication, Storage visibility and G state.

Recovery MUST NOT manufacture a successful
terminal state from missing evidence.

#### 8. Physical realization gate

The physical transaction/CAS or equivalent
recoverable prepare/commit realization spanning
G visibility and D's final gate MUST be specified
and independently proven by D and Storage/
Consistency before public visibility is enabled.

Until that proof exists, G may stage privately
but MUST NOT expose the artifact, advance the
public head or send a delivery.

This is an implementation-conformance gate,
not an unresolved normative ordering choice.

This section does not claim that an API or
production implementation already exists.

#### 9. Storage boundary

The existing Storage L1 decision remains unchanged.

This protocol defines logical ordering, protected
publication and observable consistency.

It does not select or approve a physical database,
deployment topology, HA/PITR strategy or Storage
L4 design.

Storage L4 remains OPEN / NOT APPROVED.

### 13.4 Applied attestation evidence

G Delivery records consume H evidence stages separately: DELIVERED (transport endpoint receipt), MANAGED_REGION_MATERIALIZED (local region postcondition) and FINAL_REQUEST_SUBMITTED (exact immutable request crossed the trusted handoff boundary). EXECUTION_STARTED is later runtime lifecycle evidence and is not required to define Applied.

Full Applied requires C's final-request predicates and an H evidence record binding all of:
- exact ContextRef and immutable target ContextVersion;
- stable DeliveryId and unique DeliveryAttemptId;
- authenticated Adapter Principal/Instance and Agent Principal/Agent/Instance;
- Runtime Instance/Session and exact InferenceRequestId;
- FinalRequestBoundaryId and verifiable final-submission evidence;
- ManagedRegion ID/revision/inventory and FULL coverage;
- CapabilityEpoch, current I PermissionEpoch/authorization decision;
- applicable D ForgetFenceCursor for all included source lineage;
- exact Managed Region digest plus versioned canonicalization/digest profile;
- protected-region integrity evidence and timestamp/anti-replay identity.

The digest is scoped to the declared managed region extracted from the final immutable request; it excludes System/Developer/User content, credentials and unrelated prompt content. A digest alone is not proof. Missing/stale/unverifiable fields force Partial, Bypassed or Unknown, never Full. Tier 2/3 cannot claim Full unless C's same final-boundary conformance predicates are demonstrably met; otherwise the Adapter reports its lower-tier coverage.

### 13.5 Delivery identity and state

DeliveryId is stable across retransmission of one logical delivery; DeliveryAttemptId is unique for each attempt. InferenceRequestId is unique per actual submitted inference invocation; a retry that creates a new inference invocation receives a new request ID and new final-submission evidence. ACK identity/digest is immutable; same identity plus same digest is idempotent, same identity plus different digest is conflict.

Delivery lifecycle includes Prepared, Delivered, Applied, Rejected, Expired, Superseded and Unknown. Unknown represents timeout, crash, offline or ambiguous outcome; it is not success. A late Applied ACK may be retained as historical evidence only if its ordering is provable before expiry/supersession/fence/revocation; it cannot restore current Context or roll the desired head backward.


## 14. Phase 3.5 — Normative invalidation and evidence alignment

### 14.1 Context invalidation matrix

The matrix distinguishes logical eligibility from immutable audit retention. “Invalidate” means the object MUST NOT be used to plan, deliver, replay or apply protected content; it does not mean the historical record is physically erased.

| Trigger | ContextEntry | ContextVersion / Snapshot | Delta | Delivery / Pending Delivery | Applied Context Reference |
|---|---|---|---|---|---|
| D ForgetFence covers source or transitive lineage | Immediately deny/tombstone matching entry; no new inclusion | Any version whose snapshot contains affected lineage becomes non-serving; retain only governed non-reconstructive audit metadata | Any delta adding/updating/reordering a covered entry is invalid for apply; reject replay | Prepared/Delivered attempts become Superseded or Cancelled where supported; no further apply; already-submitted outcome remains historical | Mark Invalidated for current use; retain historical attestation, never current |
| I PermissionEpoch revocation/denial or epoch gap | Block affected entry and all protected dereference; do not infer canonical Forget | Version may remain structurally valid but is unauthorized/non-serving under old epoch; rebuild only after fresh authorization | Reject until current authorization and exact base are re-established | Pending attempt is cancelled/superseded; offline/unknown remains Unknown, never Applied | Mark AuthorizationStale/Unknown; old Applied evidence remains historical only |
| Canonical supersession/revision/retraction from D | Mark StaleRevision/Superseded/Retracted as authoritative result dictates; pin exact old ref, do not silently float to latest | Affected snapshot becomes stale for current planning; rebuild if successor is explicitly validated | Delta based on old source/version is invalid for apply; create new delta from current safe base | Pending delivery superseded; late ACK cannot make old target current | Mark Stale/Invalidated for current use; preserve historical proof |
| Scope change, scope retirement or binding mismatch | Block entry until exact ownership/applicability scopes re-resolve and authorize | Old scope fingerprint cannot authorize new scope; create new version after full reauthorization | Reject if scope fingerprint/base/recipient differs | Pending delivery cancelled/superseded; do not retarget an old delivery | Mark ScopeStale/Unknown; new session/target needs new attestation |
| F IndexWatermark lag, truncation or retrieval incompleteness | Existing exact refs must be checked against D/I; do not remove merely because absent from index | Mark source coverage Stale/ReconcileRequired; no completeness claim | No delta may infer deletion from omission | Do not publish a delivery whose correctness depends on incomplete candidate coverage | Applied history unchanged; current eligibility independently checked |
| Adapter capability/session/managed-region change | Entry may remain desired if still authorized | Version remains immutable; delivery package may require re-materialization | Re-negotiate/rebuild against exact current base and schema | Old attempt is not upgraded; new attempt uses current CapabilityEpoch | Old evidence remains bound to old session/region/CapabilityEpoch; new apply requires new evidence |
| Context Remove (G operation) | Membership tombstone in the new ContextVersion | Old version remains immutable; new version omits membership | Old delta/snapshot that re-adds it is rejected/superseded | Pending delivery containing removed membership is superseded | Historical Applied reference remains historical; it does not become Canonical Forget |

Rules:
1. Forget suppression and permission denial take effect before reconciliation work; no read/plan/edit/snapshot/delta/replay/delivery/apply path may wait for a new ContextVersion.
2. Canonical supersession and Scope change require exact owner resolution; G does not invent successor identity or broaden Scope.
3. A Context Remove changes only G membership. It MUST NOT create a D ForgetOperation, advance a D ForgetFence, or be reported as canonical deletion.
4. Historical ContextVersion, ChangeSet, Delivery and ACK records are retained only under I policy and must not retain reconstructive forgotten plaintext.
5. A new safe ContextVersion is a new immutable version with a new sequence, parent=head observed at commit, freshly authorized exact refs, current typed authority vector and new dependency/publication receipts. Never mutate an old version or reset sequence.

### 14.2 Delivery state machine and evidence

Logical DeliveryId identifies one desired delivery. DeliveryAttemptId identifies one transmission/application attempt. A retry may reuse DeliveryId but MUST use a distinct attempt identity whenever a new attempt is created. A new InferenceRequestId is required for each actual inference invocation.

| State | Entry condition / minimum evidence | Allowed next states | Forbidden interpretation |
|---|---|---|---|
| Prepared | Immutable target version and package staged privately; current authorization/fence checked; D dependency registration and final visibility gate evidence available before visibility/send | Delivered, Rejected, Expired, Superseded | Not sent; not Applied |
| Delivered | H/transport receiver receipt bound to DeliveryId + AttemptId + receiver/session; transport receipt persisted | Applied, Rejected, Expired, Superseded, Unknown | Not proof of managed-region materialization or final inference submission |
| Applied | C final-request predicates plus H integrity-protected evidence bind exact full target to final immutable request; G validates all fields and currentness | Terminal for that attempt; later invalidation creates a separate invalidation/currentness state, not retroactive mutation | Never inferred from Delivered, HTTP success, local buffer write, pre-submit hook or digest alone |
| Rejected | Authenticated negative ACK / validation failure with reason and attempt identity | New attempt only after correction and current reauthorization; otherwise terminal for attempt | Not retryable success; must not advance applied reference |
| Expired | Deadline elapsed before valid Full Applied; time source and expiry evidence recorded | New DeliveryId or explicitly authorized fresh attempt after rebuilding current target | Timeout alone is Unknown; expiration cannot be converted to Applied by late ACK |
| Superseded | Newer Context target, ForgetFence, permission revocation, scope/capability change invalidates attempt before valid application | Terminal for attempt; create a new delivery from current safe version | Cannot return to Prepared/Delivered/Applied-current |
| Unknown | Timeout, crash, offline Adapter, lost ACK or insufficient evidence; query/reconcile required | Applied only if valid evidence proves application occurred before invalidation and all ordering is provable; otherwise Rejected/Expired/Superseded after reconciliation | Never success; no current Applied pointer |

State transitions are per attempt and monotonic in the audit log. A late ACK is accepted as historical evidence only when its authenticated event time/sequence and authority ordering prove it occurred before Expired, Superseded, ForgetFence or revocation. If ordering cannot be proven, preserve Unknown and block current use. A late ACK for an old target MUST NOT overwrite the Context head, current Applied reference, or a newer attempt's state.

### 14.3 Applied Evidence Mapping (G consumes C/H; does not define their wire)

G may set an attempt to Full Applied only when all rows below are present, integrity-valid, mutually consistent and current at the final submission boundary.

| Evidence dimension | Required binding / source | G validation |
|---|---|---|
| Context | Exact ContextRef + immutable ContextVersion ID/sequence + target snapshot hash | Must equal the delivery target; target cannot be inferred from current head |
| Delivery | DeliveryId + unique DeliveryAttemptId + payload digest + attempt status | Same logical delivery and exact attempt; dedupe repeated ACKs |
| Agent/Adapter identity | Authenticated Agent Principal/instance and Adapter Principal/instance; issuer/transport binding | Match registered recipient, not payload self-assertions |
| Runtime | Runtime instance + authenticated Runtime Session | Session must be exact and valid for the request |
| Inference request | Exact InferenceRequestId + FinalRequestBoundaryId | Must identify the actual immutable request crossing trusted handoff |
| Managed region | ManagedRegion ID/revision/inventory + FULL coverage | Must be the declared G-managed region; no unrelated prompt regions included |
| Permission | I PermissionEpoch + authorization decision/reference | Current and authorized at final submission; no stale/gapped epoch |
| Forget | D ForgetFenceCursor/Generation applicable to all source lineage | Current and no covered source in target; opaque owner validation only |
| Content integrity | Exact managed-region digest + versioned canonicalization/digest profile | Digest matches extracted managed region; digest alone is insufficient |
| Capability | H CapabilityEpoch + negotiated capability profile | Matches the Adapter instance/session and proof tier |
| Final boundary | C final-request attestation and H transport/integrity evidence | Proves final immutable request was submitted, not merely prepared or buffered |
| Anti-replay | ACK/attestation identity, monotonic sequence/nonce, timestamp and integrity proof | Duplicate same identity+digest is idempotent; same identity+different digest is conflict |

Coverage outcomes:
- **Full:** every target entry and required managed-region component is present; all evidence rows validate. Only this maps to Applied.
- **Partial:** an identified subset is present; record exact coverage but do not set Applied.
- **Bypassed:** inference proceeded without the Brain-managed region or via unmanaged fallback; do not set Applied.
- **Unknown:** evidence missing, stale, contradictory, unverifiable, offline or boundary-unobservable; do not set Applied.

Applied proves boundary inclusion only. It does not prove model attention, comprehension, use, response quality or behavioral compliance. Capability tier alone cannot upgrade evidence: if C's final-boundary predicates are not demonstrably met, record Partial/Bypassed/Unknown.

### 14.4 Invalidation of an already Applied reference

Applied is an immutable historical observation, not a permanent authorization lease. When Forget, Permission Revocation, Canonical Supersession, Scope Change or capability/session discontinuity occurs:
- preserve the original attestation and its exact target/request/session binding as historical evidence;
- mark its reference in the current-use projection Invalidated with the trigger, authority token and effective observation time;
- prevent the old Applied reference from satisfying a later inference request or current delivery requirement;
- require a fresh ContextVersion and new DeliveryAttempt/InferenceRequest/Applied evidence for any replacement;
- never rewrite history to claim the old request was not submitted.

### 14.5 Idempotency and commit invariants

- ChangeSet idempotency is scoped by authenticated Principal + Context + operation family + key/retention window. Same key/same normalized payload hash returns the original outcome and TargetVersion; same key/different hash is IDEMPOTENCY_KEY_REUSE.
- Delivery ACK idempotency is scoped by authenticated Adapter instance + DeliveryId + AttemptId + ACK identity. Same identity/same digest returns the prior outcome; same identity/different digest is a conflict/security signal.
- Repeated ACKs do not create a new Applied record or alter the current pointer.
- Context head advances once per successfully committed ChangeSet. A stale BaseVersion returns conflict and requires re-read/re-plan; no implicit merge.
- The G head/version visibility transition for canonical-derived artifacts remains gated by D's dependency registration and PublishDerivedIfFenceCurrent semantics. The physical transaction/recoverable realization is governed by §13.3 as a subordinate constraint: the ordering is normative and DECIDED, while the physical realization remains an implementation-conformance gate that D and Storage/Consistency MUST specify and independently prove before public visibility is enabled. Until that proof exists, stage privately and do not publish/send. §13.3 controls this relationship; this subsection does not restate it as an open normative choice.
