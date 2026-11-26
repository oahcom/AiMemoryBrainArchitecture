---
document_metadata:
  domain: memory-context
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-200/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "GOV-DOC-002 classification of a normative root that carried no front-matter: records domain, role and the status the document states in its own body (Status: G-OWNED NORMATIVE DESIGN DRAFT; IMPLEMENTATION NOT VERIFIED; CROSS-OWNER ACCEPTANCE REQUIRED). Claims no canonical authority (canonical_status stays Non-Canonical) and records no Owner approval. Pre-metadata content blob: 833815e37ac8d7505d93a0a115421dafe3eb08ad."
    usage_status: Active
    modification_status: Modified
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
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md"
    zh-CN: "docs/zh-CN/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md"
---
# Phase 3.8.22 — G Normative Applied Persistence, Idempotency, Crash Recovery and Restore-Fencing Contract

# Phase 3.8.22 — G 规范性 Applied 持久化、幂等、崩溃恢复与 Restore-Fencing 合同

- Owner: G — ContextVersion, Delivery, Applied State and Reconciliation
- Branch: `session-g-memory-context`
- Status: **G-OWNED NORMATIVE DESIGN DRAFT; IMPLEMENTATION NOT VERIFIED; CROSS-OWNER ACCEPTANCE REQUIRED**
- Decision mode: delegated G-role drafting and self-review under the user's instruction; **not an independent human Owner signature**.
- Scope: the durable G Applied decision ledger and its joins to CSubmitOutcome, H evidence, COC participant/terminal evidence, I authorization, D ForgetFence and Storage same-GID resolution.
- This contract supplements, and does not silently amend or replace, the exact G decisions listed in §2. New exact-version C/H/COC/Storage consumer decisions are required before a shared freeze.

## 1. Normative outcome

G owns the unique, durable, per-request Applied decision. Neither C, H, COC, I, D nor Storage may create or mutate G's Applied record.

A Full Applied commit is permitted only when G validates one immutable logical Applied identity and a complete evidence revision proving, for the same request and causal transaction:

1. C's immutable, authoritative CSubmitOutcome proves a determinate successful provider handoff for the exact final request.
2. H's authenticated Adapter/Runtime/Delivery evidence is current, integrity-valid and bound to that exact request and evidence revision.
3. The COC terminal proof identifies the same transaction, participant, reservation, request digest and terminal result, with complete recovery-batch and owner high-water evidence.
4. I's applicable authorization/receipt-consumption terminal evidence and D's complete-lineage ForgetFence evidence are independently authenticated and ordered by their own authorities.
5. Where JF-10 Storage participation applies, Storage proves same-GID terminal resolution and the exact atomic VisibilityPointer/PublicationReceipt or non-publication outcome.
6. G's own ContextVersion, Delivery attempt, Scope/Environment, managed-region inventory/digest, identity, session and capability predicates pass at the required linearization point.

A transport ACK, H validator result, COC quorum/commit, I COMMIT_WON, D clearance, Storage prepared receipt, C provider receipt or CSubmitOutcome alone is never Full Applied.

Full Applied means only that the specified ContextVersion was included in the exact submitted request under the complete predicate. It does not prove model execution started, attention, understanding, recall, behavioral use, response correctness, user delivery, global Forget completion or physical erasure.

## 2. Exact source pins and evidence ceiling

The following artifacts were read from their named owner branches for this draft:

| Evidence family | Exact source | Blob SHA | G use / limit |
|---|---|---|---|
| G Applied / Forget baseline | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` on `session-g-memory-context` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | G lifecycle, predicate, historical/current-use split and CGH-APPLIED-1.1 decisions |
| G JF-10 bridge acceptance | `phase-3.6.2-g-jf10-coc-bridge-applied-evidence-acceptance.md` | `25c1da1f6769165881d217bb0bb492a997e0e14c` | COC/JF-10 evidence is necessary, not G authority |
| G durable COC boundary | `phase-3.6.3-g-coc-durable-protocol-applied-boundary-acceptance.md` | `84c184c2c1476e0cf1b51d56ff80021213ae5b48` | Complete terminal proof and fail-closed recovery boundary |
| G Prepared Participant/GID | `phase-3.6.4-g-prepared-participant-gid-applied-acceptance.md` | `60dc4f43cc03e720e1c2552d77ddabe9947e8e86` | Exact PreparedParticipant/GID/DB incarnation tuple; native XID is observation only |
| G Restore consumer acceptance | `phase-3.6.5-g-restore-reconciliation-consumer-acceptance.md` | `0910fea807b96a896e361cd2722e4c94df55187b` | Restore is not Applied or current-use authorization |
| C CSubmitOutcome 1.0.1 schema | `07-agent-integration/schemas/c-submit-outcome-1.0.1.schema.json` on `session-c-agent-integration-2026-11-16` | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | Immutable C object structure; issuer, ledger, provider truth and joins need semantic verification |
| C normative Provider Submit Outcome | `phase-3.8.4-c-normative-provider-submit-outcome-contract.md` | `819705037da89834e10b6dd2ec6e66c1b8c70886` | Five-outcome algebra, same-key recovery and immutable C attempt semantics |
| C causal-order addendum | `phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `45a48249717c8cddb07ab96197730ef93d406c22` | Causal order and recovery-batch composition |
| C final request evidence | `phase-3.6-final-request-evidence-contract.md` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` | Actual immutable post-transformation request boundary |
| H Unified 1.2.15 schema | `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.15.schema.json` on `session-h-bmcp-protocol` | `860fc4cec658db7d2703cd6adf72aa31a2723f6d` | Candidate wire structure; not the JF-10 Applied ACK schema |
| H 1.2.15 gateway validator | `validators/gateway_attestation_validator.py` | `9cc426d4c26deb452f39daff34c1008dd535e969` | Local gateway-attested ingress/replay validator; production callbacks are deployment seams |
| H 1.2.15 provider validator | `validators/provider_outcome_validator_1_2_15.py` | `90a2d4b6f5b05590e3e0a7daecb5a01d9bf525c0` | Local C-object/schema/semantic validation; does not make G Applied decisions |
| H JF-10 Applied ACK bridge schema | `bmcp.applied-ack-1.1.0-jf10-bridge.schema.json` | `a8a945cc3623c2907003b93625e3c79742150944` | Separate candidate schema family; not interchangeable with H Unified Provider Outcome |

The A recovery-batch package and companion COC architecture accepted by G are respectively Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819` and Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`. These exact references do not prove a deployed coordinator, durable participant service or Storage implementation.

The H 1.2.15 local test/CI result is candidate-level evidence only. Its callback seams use deterministic test doubles. No production trust root, real I/D owner ledger, deployed COC quorum, durable replay service, provider truth, Storage same-GID recovery or multi-replica linearization is claimed.

## 3. Identity model — four non-interchangeable identities

### 3.1 CSubmitOutcome identity (C-owned)

G MUST distinguish the stable logical provider attempt from each immutable C outcome observation:

`CProviderAttemptIdentity = (issuer_authority_ref, sequence_namespace_ref, ProviderAttemptRef, ProviderAttemptGeneration, ProviderRef, ProviderAccountRef, IdempotencyNamespaceRef, IdempotencyKeyRef, RequestDigest)`

`COutcomeRecordIdentity = (issuer_authority_ref, sequence_namespace_ref, record_ref, record_sequence)`

The C object MUST bind the exact `AdapterRef`, `EndpointRef`, API operation, `FinalRequestBoundaryRef`, `RequestDigest`, `ActualInferenceRequestId` when assigned, `CausalOrderTransactionRef`, COC intent/reservation refs, and applicable outcome/evidence refs.

- `CProviderAttemptIdentity` is stable across append-only outcome observations for one logical provider attempt.
- `COutcomeRecordIdentity` identifies one immutable C ledger record. `payload_digest`, `OutcomeEvidenceDigest` and `RequestDigest` are content/integrity values, not identity substitutes.
- Same COutcomeRecordIdentity + same immutable C payload digest is the same record. Same record identity + changed payload digest or changed immutable record tuple is a hard integrity conflict; quarantine it.
- A late receipt or same-key lookup MUST be a new append-only C observation/successor with a new COutcomeRecordIdentity, explicitly linked to the same CProviderAttemptIdentity by C's prior/supersedes/reconciliation references. It MUST NOT rewrite the original C record or create a new provider attempt.
- `UNKNOWN` and `IN_DOUBT` are nonterminal. They MUST retain the same ProviderAttempt and provider idempotency key; no retry-as-new is permitted.

Only C's determinate successful handoff outcome (currently `HANDOFF_ACCEPTED` with all required provider and participant proof) is eligible for Full Applied evaluation. `HANDOFF_REJECTED`, `NOT_INVOKED`, `UNKNOWN` and `IN_DOUBT` cannot produce Full Applied.

### 3.2 H evidence identity (H-owned protocol evidence)

G MUST distinguish the stable H delivery binding from each evidence kind and immutable H ingress observation:

`HDeliveryBindingIdentity = (adapter_instance_ref, runtime_session_ref, delivery_id, delivery_attempt_id, inference_request_id, final_request_boundary_id, adapter_capability_epoch)`

`HEvidenceIdentity = (HDeliveryBindingIdentity, evidence_kind)`

`HObservationRecordIdentity = (issuer_ref, sender_authority_ref, sender_subject_ref, message_id, message_nonce, signing_sequence_namespace_ref, signing_record_sequence)`

These are **proposed normalized consumer tuples**. C and H MUST explicitly confirm exact field names, requiredness, canonicalization and mapping against the current H 1.2.15 schema/validator before shared freeze. G does not claim that the existing H schema or validator has already frozen these tuples.

**Observed mapping gap:** the pinned H 1.2.15 JSON Schema does not expose the complete HDeliveryBindingIdentity as first-class schema properties: `adapter_instance_ref`, `runtime_session_ref`, `delivery_id`, `delivery_attempt_id`, `inference_request_id`, `final_request_boundary_id` and `adapter_capability_epoch` are not present in the schema property set read for this review. The gateway validator's signed P0 allowlist includes `provider_adapter_ref`, `actual_inference_request_id` and `final_request_boundary_id`, but does not itself establish the complete tuple above. H MUST either (a) add and validate the missing fields in a versioned signed P0 mapping, or (b) bind an immutable, authenticated H owner evidence record that carries the complete tuple and has an exact schema/validator mapping. Until C/H accepts that exact mapping, HEvidenceIdentity is a G consumer requirement/proposal, not a frozen H wire contract.

Neither HDeliveryBindingIdentity nor HEvidenceIdentity contains a digest. H P0 digest is immutable content and is compared against HObservationRecordIdentity separately:

- same HObservationRecordIdentity + same H P0 digest + same authenticated immutable receipt/result ref → exact replay; return the original durable H disposition;
- same HObservationRecordIdentity + changed H P0 digest → `CONFLICT`, quarantine both observations, no last-write-wins;
- a new HObservationRecordIdentity may append a successor observation under the same HDeliveryBindingIdentity only when H's authenticated owner ledger explicitly links it to the same delivery binding; the new observation is a new evidence revision, not a new G Applied attempt;
- changed HDeliveryBindingIdentity (for example a new DeliveryAttempt, RuntimeSession or CapabilityEpoch) is a different logical delivery and cannot be rebound to the old Applied attempt.

H ingress replay protection is a separate layer. H's message identity/nonce and H P0 digest protect authenticated envelope ingestion/replay; they are not G Applied identity and are not C ProviderAttempt identity. A successful H `IDEMPOTENT_REPLAY` proves only an authorized replay of the same H ingress result, not a new G Applied commit.

### 3.3 COC participant identity (COC/Storage-owned)

For JF-10 participation, G MUST bind the exact participant tuple:

`COCParticipantIdentity = (CausalOrderTransactionRef, ParticipantIntentRef, ParticipantReservationRef, PreparedParticipantRef, PreparedTransactionGID, CanonicalAuthorityDBRef, DB system/database incarnation, ParticipantTupleDigest)`

Where present, the binding also includes the original prepare timeline/LSN, publication operation/request digest, owner boundary, COC intent position/digest, Storage signer/key version/audience, and exact VisibilityPointer/PublicationReceipt transaction/digest.

- `PreparedParticipantRef` and `PreparedTransactionGID` are stable participant identity/handle.
- Native Storage XID is observed evidence only; it is not a substitute for PreparedTransactionGID or participant identity.
- COC transaction/participant identity is not interchangeable with I sequencer position, D fence generation, G ContextVersion, Delivery cursor or ProviderAttempt generation.
- A COC terminal proof MUST bind the same transaction, participant, reservation, immutable request digest, participant digest, terminal outcome and recovery-batch/owner high-water evidence.
- Missing participant enumeration is not an empty participant set. Missing, incomplete or regressed owner high-water evidence is UNKNOWN and blocks promotion.

### 3.4 G Applied identity (G-owned)

G MUST derive one stable logical identity for the intended Applied fact:

`GAppliedIdentity = (ContextId, ContextVersion, DeliveryId, DeliveryAttemptId, InferenceRequestId, FinalRequestBoundaryId, CProviderAttemptIdentity, HDeliveryBindingIdentity, COCParticipantIdentity)`

The durable unique key is:

`GAppliedIdentityKey = SHA-256("AIMBA-G-APPLIED-IDENTITY-v1\\0" || Canonical(GAppliedIdentity))`

Canonicalization MUST use one explicitly versioned deterministic profile, reject duplicate JSON keys and unknown critical fields, and preserve type distinctions. The canonicalization profile identifier and implementation revision MUST be stored with every record.

The identity key contains no C outcome payload digest, provider receipt digest, H P0 digest, C outcome evidence digest, participant digest or G aggregate digest. Those values are immutable **identity-bound evidence content** and are compared separately. The C `RequestDigest` is the sole digest-valued component of CProviderAttemptIdentity because C defines a changed exact request as a different provider attempt/key scope; it is not the C outcome payload digest or an H/COC evidence digest. This prevents a changed evidence digest from manufacturing a new logical Applied identity.

A different ContextVersion, DeliveryAttempt, InferenceRequestId, final boundary, C outcome identity, H evidence identity or COC participant identity is a different logical Applied attempt. It MUST NOT overwrite or roll back an earlier record.

## 4. Evidence revision and digest-conflict rules

Every evaluation of one GAppliedIdentity MUST reference an immutable evidence revision:

`AppliedEvidenceRevision = (GAppliedIdentityKey, revision_number, EvidenceSetDigest, exact_source_refs)`

`EvidenceSetDigest = SHA-256("AIMBA-G-APPLIED-EVIDENCE-v1\\0" || Canonical(complete evidence set))`

The evidence set MUST include, as applicable:

- exact COutcomeRecordIdentity, its C payload digest, stable CProviderAttemptIdentity, C RequestDigest and provider outcome evidence refs;
- exact H HEvidenceIdentity and HObservationRecordIdentity, H schema artifact revision, H P0 digest, authenticated receipt/result ref, materialization/managed-region inventory and digest;
- exact COC transaction/participant/reservation/GID identity, terminal proof ref/digest, recovery-batch ref/digest, participant completeness and owner high-water vector;
- I decision/receipt/PermissionEpoch proof refs and digests;
- D fence generation, lineage proof, request cutoff and effective position as separate fields and proof refs;
- Storage DB incarnation, same-GID resolution proof, native XID observation, VisibilityPointer/PublicationReceipt or non-publication proof;
- exact G ContextVersion, Delivery attempt, Scope/Environment, Agent/Adapter/Runtime/Session, CapabilityEpoch and predicate-profile revision.

Normative duplicate handling:

| Condition | Required G behavior |
|---|---|
| Same GAppliedIdentityKey + same revision number + same EvidenceSetDigest | Return the original durable disposition and receipt; no second Applied row, no timestamp rewrite |
| Same key + same revision number + different EvidenceSetDigest | Hard conflict; quarantine both evidence sets; never last-write-wins |
| Same HObservationRecordIdentity + changed H P0 digest | H evidence conflict; G MUST NOT promote |
| Same COutcomeRecordIdentity + changed C payload digest or immutable record tuple | C evidence conflict; G MUST NOT promote |
| Same COCParticipantIdentity + changed participant/terminal digest or contradictory terminal result | COC/Storage conflict; G MUST NOT promote |
| New, valid C successor observation or H successor observation explicitly linked to the same CProviderAttemptIdentity/HDeliveryBindingIdentity | Append a new evidence revision; retain the prior revision and disposition; re-evaluate the same GAppliedIdentity, never mint a new attempt identity |
| Late evidence for an already committed Full Applied | Append historical enrichment only; never rewrite the original Applied record or retroactively change the predicate snapshot |

A new evidence revision is permitted only when the source authority has issued a new immutable successor/observation linked to the same original attempt. A caller cannot submit altered bytes under an existing source identity and label them a new revision.

An `UNKNOWN` or `IN_DOUBT` evaluation MUST be durably recorded as a non-Full unresolved disposition under the same GAppliedIdentityKey. Later authoritative evidence may append a successor evidence revision and trigger a new evaluation of that same identity. It MUST NOT create a new ProviderAttempt, provider idempotency key, Delivery attempt or COC participant to escape the unresolved state.

At most one immutable Full Applied commit may exist for one GAppliedIdentityKey. A later revocation/Forget/supersession creates a separate invalidation/current-use event; it does not mutate the historical Applied commit.

## 5. Durable G persistence protocol

The G persistence layer MUST provide a durable uniqueness constraint on `GAppliedIdentityKey` and a second uniqueness constraint on `(GAppliedIdentityKey, revision_number)`. The final Applied table/event stream MUST enforce at most one Full Applied commit per logical identity.

The minimum local atomic commit unit is:

1. insert-or-read the G Applied identity reservation;
2. insert the immutable evidence revision and its source pins/digests;
3. persist the predicate result and exact authority snapshot/cursors;
4. if and only if the full predicate passes, append the immutable Full Applied fact;
5. append the audit/decision event and any local outbox notification;
6. commit all local rows/events atomically.

No partial Applied row may become visible. A database uniqueness conflict is resolved by reading the existing durable identity/revision and applying §4; it is never resolved by overwriting.

Before the final local commit, G MUST revalidate the currentness/linearization predicates against authoritative I, D, COC and Storage evidence, including the applicable Context BaseVersion/CAS and Delivery attempt. If an authority is unavailable, stale or incomparable, the result is UNKNOWN and no Full Applied fact is committed.

G MUST NOT perform a cross-domain comparison of opaque COC, I, D and Storage positions. Each owner validates its own ordering domain and supplies a terminal proof/cutoff relation. G consumes the signed relation for the same participant/request; it does not invent a global numeric order.

## 6. Crash, timeout and retry recovery

| Crash/failure point | Durable state expected | Recovery rule |
|---|---|---|
| Before G identity reservation | No G reservation or Applied fact | Re-submit only the same logical request identity after all gates are rechecked |
| After identity reservation, before evidence revision | Reservation is pending; no Full Applied | Read and resume the same GAppliedIdentityKey; never allocate a second key |
| During local atomic commit, outcome unknown to caller | Either all local rows committed or none | Read by exact GAppliedIdentityKey and revision; if storage read is unavailable, remain UNKNOWN/IN_DOUBT |
| After Full Applied commit, before response/ACK | Immutable Applied fact and audit event exist | Return the original receipt/disposition; do not insert a second fact |
| C provider handoff occurred but C outcome/receipt persistence is missing | C outcome UNKNOWN/IN_DOUBT; G has no Full Applied | C reconciles the same ProviderAttempt and same provider idempotency key; G keeps protected content suppressed |
| COC terminal proof exists but G has not committed | COC terminal proof remains immutable; G identity may be pending | Revalidate exact proof and commit under the same GAppliedIdentityKey |
| COC/provider/Storage authority unavailable | unresolved participant or evidence | No Full Applied; keep required barriers held; no retry-as-new |
| Recovery batch incomplete or owner high-water regressed | batch is not complete | Block new Full Applied and protected current use until authoritative reconciliation completes |

A retry is a read/reconciliation of the same identity, not a new transaction. Automatic SDK retry, transport retry, redirect, account/region/model failover, stream restart or provider re-send MUST NOT bypass C's same-key policy or G's identity reservation.

A timeout, process crash, missing row, lost ACK, empty queue or provider lookup outage is not proof of `NOT_INVOKED`, `HANDOFF_REJECTED`, rollback or safe abort. If a side effect may have occurred, preserve `IN_DOUBT`.

## 7. Restore fencing and rollback resistance

Restore is a trust boundary, not a shortcut to Applied or current-use authorization.

Before restored Context, Delivery, Applied or evidence-ledger data can be served, materialized, replayed or used to commit new Applied facts, G MUST install a durable `GRestoreFence` that blocks affected protected use and new Full Applied promotion.

The restore reconciliation MUST bind at least:

- restored DB incarnation/system/database identity and restore epoch;
- the exact Storage snapshot/checkpoint and restore receipt;
- G Applied ledger checkpoint, sequence/high-water and evidence-revision high-water;
- COC prefix/terminal participant ledger and recovery-batch high-water;
- I PermissionEpoch/revocation terminal high-water;
- D ForgetFence/lineage high-water, including pending cutoff/effective-position state;
- current Context head and Delivery cursor/attempt high-water;
- exact same-GID/participant resolution for every unresolved prepared transaction.

Restore MUST rebuild and verify unique indexes from immutable identity keys and evidence revisions. Duplicate keys with identical digests are deduplicated to the original durable record; same-key/different-digest collisions are quarantined and block the affected scope. Restore MUST NOT mint replacement Applied identities, provider keys, Delivery attempts or COC participant identities to make stale work appear new.

A restored snapshot that predates an I revocation, D ForgetFence, COC participant terminal, Storage publication/rollback or G Applied invalidation is stale. G MUST suppress it and reconcile against current owner high-water. A stale or missing high-water is UNKNOWN, not zero or empty.

The restore fence may be cleared only after a durable, authenticated RestoreReconciliationReceipt proves all required ledgers/prefixes and owner high-water vectors are complete and current, all prepared participants have determinate same-GID terminal resolution, and fresh I/D/current Context/Capability checks pass. G cannot mint I or D proof and cannot clear an owner-local barrier.

No restored Snapshot, Delta, ACK, cache, queue item or historical Applied record may resurrect content covered by a current Forget tombstone. Historical Applied remains historical; current-use remains denied until independently re-authorized and reconciled.

## 8. Forget/revocation race and current-use projection

G MUST keep these order domains distinct:

- C provider attempt/handoff and immutable CSubmitOutcome sequence;
- COC transaction/participant order and terminal proof;
- I policy sequencer decision/receipt and revocation request cutoff;
- D ForgetFence generation, request cutoff and effective position;
- Storage same-GID resolution/publication position;
- G local Applied commit and Context/Delivery version.

Rules:

1. I revocation that wins before applicable receipt consumption blocks provider admission/Full Applied.
2. A prior I terminal COMMIT_WON may remain committed for its exact participant; a later revocation cannot rewrite it but must be honored at its authoritative cutoff.
3. A D Forget request before the participant-intent cutoff rejects admission. A later D fence must account for all prior unresolved participants and cannot be treated as effective past an unresolved participant without D's explicit safe terminal proof.
4. If valid provider submission/Applied linearized before a later effective Forget/revocation, preserve historical Applied and append `InvalidatedForCurrentUse`.
5. If Forget/revocation is ordered before submission, Full Applied is forbidden.
6. If order, lineage, owner high-water or provider outcome is unknown, do not promote Full Applied; suppress protected current use and retain UNKNOWN/IN_DOUBT.
7. Restore, retry or duplicate evidence cannot bypass a Forget/revocation barrier.

Current-use is a separate projection, recalculated before protected use and again before any final request submission. It MUST check current Context head, Delivery status/attempt, I PermissionEpoch/decision, D fence/lineage, Scope/Environment, authenticated identity, RuntimeSession, Adapter CapabilityEpoch and unresolved participant/recovery state. Historical Applied is never itself a current-use authorization.

## 9. Required machine-readable G Applied record fields

The implementation MUST persist at least the following immutable fields (names are logical contract names; a generated schema/SDK mapping remains a separate deliverable):

- `g_applied_identity_key`, `identity_canonicalization_profile`, `identity_schema_revision`;
- exact ContextId/ContextVersion, DeliveryId/DeliveryAttemptId, InferenceRequestId and FinalRequestBoundaryId;
- CProviderAttemptIdentity, COutcomeRecordIdentity, CSubmitOutcomeRef, CSubmitOutcomeDigest, RequestDigest, ProviderAttemptRef/generation and provider idempotency namespace/key refs;
- HDeliveryBindingIdentity, HEvidenceIdentity, HObservationRecordIdentity, H schema artifact revision, H P0 digest, authenticated H receipt/result ref, Adapter/Runtime/Session/CapabilityEpoch;
- COCParticipantIdentity, CausalOrderTransactionRef, ParticipantIntent/Reservation refs, PreparedParticipantRef, PreparedTransactionGID, DB incarnation and ParticipantTupleDigest;
- COC terminal proof, recovery-batch proof, participant-completeness and owner high-water refs/digests;
- I authorization/receipt/PermissionEpoch refs and digest;
- D ForgetFence generation, lineage proof, request cutoff and effective position as distinct fields/refs;
- Storage same-GID terminal proof, native XID observation, VisibilityPointer/PublicationReceipt or non-publication proof;
- Scope/Environment, Agent/Adapter/Runtime identity, managed-region inventory/revision/digest and predicate-profile revision;
- evidence revision number, EvidenceSetDigest, decision disposition, G Applied commit receipt, local ledger sequence/high-water and timestamps;
- restore epoch/fence reference and invalidation/current-use projection events.

Unknown or unavailable proof is represented explicitly as UNKNOWN with a reason and missing-source list. It MUST NOT be represented by empty strings, empty arrays, fabricated zero positions or omitted participant sets.

## 10. Conformance obligations — specified, not run

| ID | Adversarial case | Required result |
|---|---|---|
| G-AP-P01 | Same identity/revision/digest submitted twice | One durable Applied fact; second call returns original receipt |
| G-AP-P02 | Same identity/revision with changed aggregate digest | Conflict/quarantine; no overwrite |
| G-AP-P03 | Same HObservationRecordIdentity with changed H P0 digest | Conflict/quarantine; no Full Applied |
| G-AP-P04 | Same COutcomeRecordIdentity with changed C payload digest | Conflict/quarantine; no Full Applied |
| G-AP-P05 | Same COC participant identity with contradictory terminal digest/outcome | Conflict/UNKNOWN; no Full Applied |
| G-AP-P06 | C UNKNOWN/IN_DOUBT after possible provider side effect | Same ProviderAttempt/key; no Full Applied; barriers held |
| G-AP-P07 | Crash after provider handoff before C outcome persistence | IN_DOUBT; same-key recovery only |
| G-AP-P08 | Crash after G local commit before caller receives response | Read original commit; no second Applied fact |
| G-AP-P09 | Crash during G atomic commit | All-or-none local transaction; resolve by same identity |
| G-AP-P10 | COC terminal proof exists but G commit is pending | Revalidate and commit same G identity |
| G-AP-P11 | Recovery batch omits a pre-batch participant | UNKNOWN; no new Full Applied |
| G-AP-P12 | Owner high-water regresses after restore | Restore fence remains; protected use blocked |
| G-AP-P13 | Restored DB incarnation/GID differs from prepared participant | UNKNOWN/IN_DOUBT; no visibility or Applied promotion |
| G-AP-P14 | Restored snapshot predates D Forget or I revocation | Suppress stale content; no resurrection |
| G-AP-P15 | Valid historical Applied followed by later effective Forget | Preserve historical record; invalidate current use |
| G-AP-P16 | Forget/revocation order relative to provider submit is unknown | UNKNOWN; suppress; no Full Applied |
| G-AP-P17 | Same-key duplicate ACK arrives after Delivery supersession | Historical-only; cannot mutate newer attempt |
| G-AP-P18 | H replay is valid but G Applied predicate is incomplete | No Full Applied; H replay result is not G commit |

Required tests include durable database crash injection, process restart, multi-replica concurrent duplicate submissions, restore from stale checkpoints, owner high-water regression, exact same-GID lookup, and current-use revalidation. Pure unit tests or callback doubles alone do not close production persistence/restore obligations.

## 11. Owner boundaries and acceptance required

- G owns the Applied identity, evidence-revision ledger, Full Applied predicate, durable commit/idempotency, historical/current-use projection and G restore fence.
- C alone owns CSubmitOutcome truth, ProviderAttempt and same-provider-key recovery.
- H alone owns wire schema, authenticated Adapter/Runtime/Delivery evidence, H envelope replay/integrity and CapabilityEpoch.
- COC owns coordinator transaction/participant/terminal/recovery-batch ordering evidence; it cannot mint C/I/D/Storage/G decisions.
- I alone owns PermissionEpoch, authorization and revocation terminal evidence.
- D alone owns canonical ForgetOperation, ForgetFence, lineage, request cutoff and effective position.
- Storage alone owns DB incarnation, same-GID resolution, VisibilityPointer/PublicationReceipt and restore receipts.
- G does not compare opaque positions across owners or infer a missing owner proof.

Before this addendum can be called shared/frozen, the following exact-version acceptances are required:
1. C accepts the exact G identity/evidence-revision join to CSubmitOutcome 1.0.1 and the C causal-order source pins.
2. H accepts the exact HEvidenceIdentity/HDeliveryBindingIdentity tuple and supplies the missing signed-schema/owner-record field mapping to Unified 1.2.15 gateway evidence, including the distinction between H ingress replay and G Applied idempotency.
3. COC/Storage accept the exact participant/GID/terminal/restore bindings and recovery semantics.
4. I and D confirm the owner evidence/cutoff/high-water fields within their authority.
5. G implementation provides generated machine-readable schema/SDK, durable unique indexes, crash/restart/restore tests and independent readback against exact commits.

No approval transfers from H 1.2.14, a prior G consumer review, the CGH-APPLIED-1.1 semantic package, schema-only acceptance or documentation CI. This document is a G-owned design contract, not proof that the implementation exists.

## 12. Current disposition

- G Applied Persistence / Idempotency contract: **SPECIFIED BY THIS G DRAFT; NOT IMPLEMENTED / NOT VERIFIED**.
- Exact CSubmitOutcome 1.0.1 source binding: **PINNED; C exact acceptance of this addendum REQUIRED**.
- H EvidenceIdentity tuple: **PROPOSED; current 1.2.15 schema does not expose all binding fields; H/C exact field-level mapping and schema/owner-record extension REQUIRED**.
- COC Participant/GID join: **G design acceptance exists; COC/Storage implementation and exact addendum acceptance REQUIRED**.
- Crash/restart/restore fencing conformance: **SPECIFIED / NOT RUN**.
- G Applied persistence production proof: **NOT VERIFIED**.
- Global C/G/H Applied freeze: **NO**.
- Production egress/activation: **NOT AUTHORIZED**.

This contract does not claim exactly-once provider side effects, model execution, global Forget completion, physical erasure or production readiness.


## 13. Executable reference-model evidence — 2026-11-18

A bounded, single-node SQLite reference model was added in merged PR [#139](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/139):

- `06-memory-context/reference-model/g_applied_ledger.py`
- `06-memory-context/reference-model/test_g_applied_ledger.py`
- `.github/workflows/g-applied-reference-model.yml`

Exact PR-head run [#44187485388](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187485388) and post-merge main run [#44187595305](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187595305) both completed SUCCESS. The post-merge run is pinned to main commit `af3b0380e35a5834f8b5cdca92dfa0f8fcd8e1bf`; its job log reports **8 tests OK**.

The executable cases cover:
1. a complete positive gate set with C `HANDOFF_ACCEPTED` creating one record;
2. same logical identity + same evidence digest returning the original record;
3. same identity + changed evidence digest producing a durable conflict without overwriting the original;
4. `HANDOFF_REJECTED`, `NOT_INVOKED`, `UNKNOWN` and `IN_DOUBT` never creating Full Applied;
5. missing or failed authority/evidence gates failing closed;
6. close/reopen readback and same-record replay;
7. distinct logical identity producing a distinct record; and
8. rejection of undeclared identity fields.

**Evidence ceiling:** this is a conformance/reference prototype, not the production G runtime or a G Owner implementation acceptance. It uses one local SQLite database and caller-supplied gate booleans. It does not prove multi-replica linearization, distributed restore fencing, current-use revalidation after later I/D changes, real C/H/COC/I/D/Storage authority resolution, cryptographic authentication, or production durability topology. The status in §12 therefore remains unchanged: production G Applied persistence and cross-owner Full Applied are NOT VERIFIED / NOT FROZEN.
