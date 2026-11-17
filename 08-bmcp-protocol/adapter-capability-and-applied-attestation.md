# Adapter Capability and Applied Attestation

- Status: **CANDIDATE — final-request proof profile OPEN with C; authorization binding OPEN with I**
- Owner: H (Adapter SDK, capability negotiation, protocol attestation encoding)
- Related issues: INT-P1-05, INT-X-03, INT-X-04, INT-X-07

## 1. Capability declaration

An Adapter advertises capabilities explicitly; capability is not inferred from product name or transport reachability.

Candidate capability dimensions:
- protocol major/minor range and payload schema IDs;
- supported message families and Snapshot/Delta operations;
- maximum payload size and compression;
- durable local queue support and queue retention horizon;
- idempotent receipt / delivery deduplication;
- managed-region isolation and mutation controls;
- ability to inspect the assembled final request;
- ability to observe successful handoff to the inference runtime;
- ability to correlate request IDs;
- ability to compute a digest over the exact managed region in the final request;
- ability to produce integrity-protected evidence;
- Forget/revocation clearing and offline reconnect behavior;
- supported ACK states and coverage values;
- maximum supported context size and truncation reporting.

Capabilities are versioned by an Adapter capability epoch. A binary/configuration/runtime change that changes the declared capability set MUST create a new epoch and renegotiate. A previous attestation is evaluated against the capability epoch that produced it, not the current one.

## 2. Conformance tiers

### Tier 1 — Final-request observable

Requirements:
- observes the exact final request after all prompt/context assembly and transformations;
- identifies the actual request submitted to the inference runtime;
- can prove managed-region completeness and exact target ContextVersion;
- computes a declared canonical digest over the managed region as submitted;
- correlates request ID, delivery ID, session/context and capability epoch;
- emits integrity-protected evidence that the submission occurred;
- preserves separation from protected instruction, user, Agent policy and tool-authorization regions;
- processes Forget/revocation fences before reuse/reconnect.

Tier 1 may emit Full Applied only when all per-request proof predicates pass. If any predicate fails, it emits Partial, Bypassed or Unknown.

### Tier 2 — Managed-region observable, final submit not observable

Requirements:
- can identify and validate the managed region after local assembly;
- can report complete/partial/bypassed state at its own boundary;
- cannot prove that the exact assembled request was actually submitted to the runtime (e.g. later middleware may mutate or discard it);
- enforces local stale version/fence rejection and region separation.

Tier 2 MUST NOT claim Full Applied. It may report Partial if partial materialization is known; otherwise Unknown. A local buffer digest alone is not final-request proof.

### Tier 3 — Transport/basic integration

Requirements:
- authenticates/negotiates the protocol transport according to configured security integration;
- validates envelope/version and transports messages;
- reports transport delivery, explicit rejection and unknown outcomes;
- does not claim that Context has been applied to an inference request.

Tier 3 MUST NOT emit Applied=Full. It normally reports Delivered, Rejected, Expired, Superseded or Unknown.

## 3. Attestation data model

Candidate attestation structure:

| Field | Required | Purpose |
|---|---|---|
| attestation_id | Required | Unique immutable evidence record |
| delivery_id / attempt_id | Required | Bind to logical delivery and attempt |
| context_ref / target_context_version | Required | Bind to G authoritative target |
| applied_context_version | Required | Actual materialized G version |
| coverage | Required | Full / Partial / Bypassed / Unknown |
| adapter_id / capability_epoch | Required | Identify implementation capability |
| authenticated_transport_principal_ref | Required by I mapping | Reference transport-authenticated identity; not payload-authenticated |
| agent_instance_ref / session_ref | Conditional, C-defined | Bind the execution context |
| inference_request_id | Required for Tier 1 Full | Exact submitted request |
| submission_observed_at | Required for Tier 1 Full | Runtime handoff event time |
| managed_region_digest | Required for Tier 1 Full | Digest of exact managed region in submitted request |
| digest_profile | Required for digest | Canonicalization profile and algorithm |
| final_request_evidence | Required for Tier 1 Full | Runtime submission receipt/hook evidence |
| permission_epoch | I-defined | Authorization epoch at application |
| forget_fence | D/I-defined | Fence current at application |
| protected_region_integrity | Required | Evidence that protected regions were not modified by Adapter application |
| created_at | Required | Attestation creation time |
| integrity | Required | Signature/MAC/reference under approved I security mechanism |

Exact names/types of principal, ActorRef, session, Context and fence fields are OPEN with their owners. This table is not authorization policy.

## 4. Full Applied proof predicate

Let:
- (D) be the logical delivery;
- (C_v) be G's exact target ContextVersion;
- (R) be the final request actually submitted to the inference runtime;
- (M(R)) be the managed memory region extracted from that final request under the negotiated digest profile;
- (E) be the verifiable runtime submission evidence;
- (P) be current I authorization binding/permission epoch;
- (F) be the current applicable D/I Forget fence.

Then Full Applied may be accepted only if:

[
egin{aligned}
FullApplied iff{}&
Version(D)=C_v land Version(M(R))=C_v \
&land Complete(M(R),C_v) land Digest(M(R))=attestedDigest \
&land Correlates(E,R,D,C_v) land Submitted(E,R) \
&land ProtectedRegionsUnchanged(R) \
&land Authorized(P,D) land FenceCurrent(F,D) \
&land CapabilityTier ge Tier1
end{aligned}
]

This is a proof obligation for the integration boundary, not a claim about internal model execution. The inference runtime may later reject, truncate, transform, or process the request in ways beyond Adapter observability; the exact observable handoff point must be declared in the implementation profile.

## 5. Evidence profile and privacy

Candidate evidence components:
- unique runtime request ID;
- timestamp and monotonic local sequence at the submission hook;
- digest of the canonical managed-region bytes/structure;
- digest of the final request envelope where policy permits;
- Adapter build/runtime identity and capability epoch;
- signed attestation or reference to a trusted local submission log.

Privacy rules:
- Do not place raw prompt or full memory text in an ACK by default.
- Prefer digest plus minimal metadata and a policy-controlled evidence reference.
- A digest is not anonymization; low-entropy or guessable content may be dictionary-tested.
- Retention, audit access, signing key lifecycle and external disclosure are I-owned policy.
- A verifier must know the digest canonicalization profile and exactly which bytes/fields were included.
- If the Adapter cannot produce verifiable evidence, report Unknown or Partial; never fabricate proof.

## 6. Protected region invariant

Memory content is untrusted data. The Adapter:
- writes only to an explicitly delimited managed region;
- cannot modify System/Developer instruction regions, user input, Agent policy, tool definitions, credentials or tool authorization;
- cannot translate memory text into executable tool calls or grant capabilities;
- rejects or bypasses delivery if the host API cannot enforce region boundaries;
- records truncation/omission and does not call a partial buffer Full.

The Brain can validate protocol attestations and configured boundary evidence; it cannot guarantee the model ignores malicious natural-language content after inclusion. Prompt-injection residual risk belongs in the I threat model and Agent's action policy.

## 7. Capability negotiation and epoch invalidation

Capability Negotiation includes:
- Adapter identifier and implementation version;
- protocol and payload schema support;
- message family support;
- delivery/ACK semantics;
- conformance tier and individual proof features;
- managed-region boundary mode;
- runtime submission observability;
- digest/signature profile;
- local queue/reconnect behavior;
- payload and context limits.

Capability epoch MUST change if any change could invalidate earlier proof claims: adapter build, inference integration hook, prompt assembly middleware, region isolation behavior, signature key binding, or negotiated features. Attestations remain tied to the epoch used at creation. A tier downgrade invalidates future Full claims; it does not rewrite historical evidence.

## 8. Required conformance tests

1. Full request: exact G version completely included; runtime submission evidence verifies; Full accepted.
2. Internal buffer only: digest exists but no runtime submit observation; Full rejected.
3. Later middleware mutation: submitted region differs from prepared region; Full rejected or Partial.
4. Partial/truncated content: Partial, never Full.
5. Managed region bypassed: Bypassed.
6. Runtime submission uncertain: Unknown.
7. Wrong ContextVersion/delivery/session/capability epoch: reject attestation.
8. Stale permission epoch or Forget fence: reject and suppress application.
9. Duplicate attestation: idempotent replay, no second state transition.
10. Protected-region mutation attempt: application rejected and security event emitted.
11. Adapter tier downgrade/rebuild: new capability epoch required.
12. Tier 2/3 claims Full: conformance failure.

## 9. Ownership and open decisions

- C defines the semantic final-request boundary and Agent-side request correlation.
- G defines Context target/version and what “complete managed region” means for a target.
- I defines authenticated principal binding, permission epoch, signature trust and audit policy.
- H defines SDK interfaces, capability declaration, evidence encoding and protocol validation.
- The inference provider's hidden prompt retention and model internal state are outside H's control and MUST NOT be represented as cleared or verified.


## 10. Forget capability declaration and ACK boundary

Capability Negotiation MUST additionally declare whether the Adapter can: (a) durably suppress selected content from future inference assembly, (b) enumerate/clear volatile managed buffers, (c) enumerate/purge persistent local cache namespaces and partitions, and (d) enumerate/cancel local queued/retry deliveries. Each declaration includes exact Managed Region/session coverage, inventory revision, observability and limitations. A capability bit without an enumerated coverage boundary cannot support a complete-clear claim.

CapabilityEpoch changes whenever Adapter identity/build, runtime hook, Managed Region boundary, queue/cache inventory or relevant clear/apply capability changes. An ACK binds to the exact epoch and cannot be projected onto a replacement Adapter Instance or changed region.

Forget ACK and Applied Attestation are separate evidence families. Applied binds G ContextVersion + Delivery + inference request at the declared final submission boundary. Forget ACK binds ForgetOperation + D fence + I Permission Epoch + local action/Managed Region. Applied does not prove model attention or use; Forget ACK does not prove global Forget completion or provider deletion.

The full status semantics, target mapping and evidence fields are defined in adapter-forget-ack-and-target-binding.md.


## 11. Phase 3.6 exact final-request field mapping — H candidate addendum

- Status: **CANDIDATE — proposed field mapping for C/G review; NOT FROZEN**
- Related exact C source: `07-agent-integration/phase-3.6-final-request-evidence-contract.md`, Blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`.
- Related G source: `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md`, Blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a`.
- H remains owner of wire/evidence encoding and capability negotiation. C remains sole producer of final-request submission evidence. G remains sole authority for Applied acceptance. I and D remain sole authorities for authorization and ForgetFence respectively.

This addendum proposes a field-level mapping to close the candidate gaps identified in the 2026-11-17 C/G/H cross-owner review. It is not an acceptance by C, G, I, D or B, and it does not freeze a schema, signature profile or implementation.

### 11.1 Canonical request and delivery binding

For a Tier 1 final-request attestation, the H candidate field set is:

| H candidate field | Requiredness | Semantic source / rule |
|---|---|---|
| `inference_request_id` | REQUIRED | Actual Runtime/Provider-assigned request ID; never synthesized from DeliveryId |
| `final_request_boundary_id` | REQUIRED | Exact C-observed successful submit boundary identity |
| `final_request_boundary_type` | REQUIRED | Declared hook/submit boundary profile; must identify the observation point |
| `context_id` | REQUIRED | Exact G Context identity |
| `context_version` | REQUIRED | Exact immutable G target version |
| `delivery_id` | REQUIRED | Exact G Delivery identity |
| `delivery_attempt_id` | REQUIRED | Exact non-superseded attempt |
| `materialized_context_version` | REQUIRED | Version actually present in the Adapter managed region; must equal `context_version` for Full |
| `adapter_instance_ref` | REQUIRED | Exact Adapter instance that materialized and observed the request |
| `runtime_instance_ref` | REQUIRED | Runtime instance in which the request was submitted |
| `runtime_session_ref` | REQUIRED | Authenticated Runtime Session binding |

The legacy candidate field `applied_context_version` is ambiguous because H cannot decide G's Applied state. For this profile it is deprecated as a wire name and MUST NOT be interpreted as a G Applied decision. Implementations should use `materialized_context_version`; a compatibility decoder may accept the legacy name only when it is unambiguously mapped to the materialized version and never to an Applied state.

### 11.2 Managed Region completeness and digest

Tier 1 evidence MUST bind all of the following:

- `managed_region_id`: exact managed-region identity;
- `managed_region_revision`: immutable revision observed in the submitted request;
- `managed_region_inventory_digest`: digest of the complete inventory of managed-region segments/entries included by the negotiated profile;
- `managed_region_coverage`: per-request coverage enum `COMPLETE`, `PARTIAL`, `BYPASSED` or `UNKNOWN`;
- `managed_region_digest`: digest of the exact complete region content as embedded in the final submitted request;
- `digest_profile_id`: canonicalization profile identifier and digest algorithm/version;
- `omitted_region_refs` and `unobservable_path_refs`: explicit sets when coverage is not complete, including an explicit empty set for complete coverage where required by the canonical profile.

A digest without region identity, revision, inventory and coverage is insufficient to prove completeness. Full candidate evidence requires `managed_region_coverage=COMPLETE`, exact target/version match, no bypass or unknown path, and equality between the delivered/materialized target and the region observed in the submitted request. Partial, bypassed, unknown or truncated coverage MUST NOT be upgraded to Full by H or G.

### 11.3 Protected identity and authority bindings

The candidate attestation MUST carry verifier-resolved opaque references, not payload-asserted identity values:

- `agent_principal_ref`, `agent_actor_ref`, `agent_instance_ref`;
- `adapter_principal_ref`, `adapter_ref`, `adapter_instance_ref`;
- `runtime_instance_ref`, `runtime_session_ref`;
- `scope_ref` and applicable `environment_ref`.

The authenticated transport principal remains useful transport evidence but MUST NOT substitute for the protected Agent/Adapter/Runtime/Session binding. H preserves exact issuer-namespaced references and verifies the configured authenticated envelope/binding profile; it does not mint Principal, Actor, Scope, Environment or delegation authority.

The following owner-issued authority fields are opaque and must be current at the final submit boundary:

- `permission_epoch_ref` and `permission_decision_ref` — I-issued; H does not define or infer authorization;
- `forget_fence_generation`, `forget_fence_cursor` and `forget_fence_validation_ref` — D-issued; H does not define or infer canonical Forget ordering;
- `adapter_capability_epoch` and negotiated `capability_profile_ref` — H-issued and bound to the exact Adapter instance/session.

An attestation with missing, stale, incomparable, unverifiable or mismatched authority bindings is not eligible for Full. The receiver must not substitute a newer epoch, infer a clear fence, or use payload identity claims as fallback.

### 11.4 Evidence provenance, integrity and correlation

The Tier 1 candidate evidence profile requires:

- `evidence_issuer_ref`;
- `submission_observed_at` and, where the runtime provides it, `submission_monotonic_sequence`;
- `evidence_schema_version`;
- `correlation_ref` and `causation_ref`;
- `audit_ref` or a policy-controlled reference to the immutable evidence record;
- `integrity_proof_ref` under the H/I-approved integrity profile;
- the exact `inference_request_id`, `final_request_boundary_id`, request digest/profile and region digest/profile covered by that proof.

Wall-clock timestamps are descriptive and MUST NOT alone establish ordering between C submission, I revocation and D ForgetFence advancement. Where a common causal order cannot be proven from owner-authoritative evidence, disposition is UNKNOWN and the managed region remains suppressed for future use.

Raw prompt or full memory text MUST NOT be copied into ACK/evidence by default. A digest is not anonymization; evidence retention and disclosure remain subject to I policy.

### 11.5 Per-request coverage and capability ceiling

The negotiated Adapter capability declaration describes maximum supported behavior; the attestation MUST additionally describe actual per-request coverage. The following rules apply:

1. Tier 1 is eligible for candidate Full evidence only when final request observation, successful submit, exact request identity, complete region digest, protected identity binding and current authority bindings are all proven.
2. Tier 2 cannot prove the final transformed request/submit boundary and MUST remain Partial or Unknown.
3. Tier 3 proves transport only and MUST NOT claim Applied=Full.
4. Any per-request bypass, omitted path, truncation, unknown middleware transformation, unsupported region or incomplete inventory prevents Full.
5. CapabilityEpoch is bound to the exact Adapter instance/session and proof profile. A capability downgrade or relevant build/hook/region/integrity change requires a new epoch and renegotiation; old evidence remains bound to its original epoch.

### 11.6 Idempotency, replay and temporal rules

For this candidate profile, evidence identity is scoped to:

`(adapter_instance_ref, runtime_session_ref, delivery_id, delivery_attempt_id, inference_request_id, final_request_boundary_id, evidence_kind, adapter_capability_epoch)`

- Same evidence identity and same canonical payload digest is an idempotent replay and returns the original durable disposition.
- Same evidence identity with a different digest is CONFLICT and quarantined; last-write-wins is forbidden.
- Evidence from a superseded attempt, old Adapter instance or old Runtime Session may be retained as historical evidence only; it cannot roll back G's current Context/Delivery head or be rebound to a replacement session/epoch.
- C alone emits Final Request Submitted evidence. H validates/encodes/transports it; H does not create a substitute submit proof.
- G alone accepts Applied after checking C evidence, H protocol/capability proof, I authorization and D ForgetFence evidence.
- A later Forget/revocation invalidates current-use eligibility without rewriting a historically valid submission/Applied fact. If Forget/revocation precedes submit, Full is rejected. If ordering is unknown, disposition is UNKNOWN and content remains suppressed.
- Execution Started remains a separate Runtime/Provider receipt correlated to the same InferenceRequestId.

### 11.7 Required owner decisions and non-claims

Before this candidate can be frozen:

- C MUST confirm the exact FinalRequestBoundaryId, request/delivery/context mapping, Managed Region completeness profile and evidence provenance.
- G MUST confirm that the H candidate evidence is sufficient for its Applied predicate and that H does not usurp G's Applied authority.
- I MUST confirm Principal/Actor verifier binding, PermissionEpoch/decision references, integrity profile and retention rules.
- D MUST confirm ForgetFence generation/cursor/lineage references and the authoritative ordering evidence.
- B MUST confirm ActorRef/ScopeRef/EnvironmentRef typed semantics.
- H MUST publish the corresponding versioned wire schema/SDK mapping only after the above field semantics are accepted.

All related conformance cases remain **SPECIFIED / NOT RUN** until executable fixtures, deterministic ordering, expected/actual outputs and durable owner evidence are attached. This addendum does not establish H schema freeze, cryptographic approval, interoperability, implementation correctness, C/G/H global freeze, or production readiness.


### 11.8 CGH-APPLIED-1.1 causal-order and recovery-batch evidence bridge — candidate

G's current exact-version decision history includes the CGH-APPLIED-1.1 causal-order profile and a recovery-batch amendment. The Tier 1 evidence mapping above is necessary but not sufficient for that profile. Before H can claim the 1.1 Applied ACK mapping is complete, the H message/evidence profile MUST carry or immutably reference the following owner-issued evidence set:

- `causal_order_profile_ref`, `causal_order_coordinator_ref`, `causal_order_domain_ref`, and `causal_order_transaction_ref`;
- `causal_order_terminal_proof_ref` and its digest, binding the exact transaction, immutable request/participant digest, reservation and determinate terminal outcome;
- `recovery_batch_ref` and `recovery_batch_digest`;
- `pre_batch_participant_set_digest`, `participant_set_completeness_attestation_ref`, and the complete `owner_high_water_attestations` set;
- the complete `participant_reconciliation_entries` set, or an explicitly attested empty set; each entry retains its exact ParticipantIntentRef, causal-order transaction, request digest, and separate I/D/C reconciliation states;
- I-issued `i_authorization_terminal_ref`, `i_sequencer_ref`, `i_sequencer_epoch`, `i_sequencer_position`, `i_decision_digest`, and revocation cutoff evidence or an explicit I-attested absence at terminalization;
- D-issued `d_lineage_coverage_ref`, `d_fence_request_cutoff_ref`, and `d_fence_effective_position`, preserving complete lineage and the distinction between request cutoff and effective fence position;
- where the recovery participant set includes Storage, Storage-issued same-XID resolution and terminal visibility/non-publication proof references required by the applicable Storage contract.

H may authenticate the H envelope, validate message-family/schema integrity and preserve these owner-issued opaque references. H MUST NOT mint or infer COC terminal proof, I authorization outcome, D clearance/fence, C provider outcome, or Storage commit/rollback/visibility. Missing or unknown critical owner evidence remains UNKNOWN/IN_DOUBT and cannot promote Full Applied or release an owner-local gate.

The following ordering domains MUST remain distinct and MUST NOT be compared, coerced or substituted by H:

1. COC causal-order epoch/position/entry digest;
2. I sequencer reference/epoch/position/decision digest;
3. D request cutoff and effective fence position;
4. Storage transaction/resolution position.

COC position orders COC records only. I position is authoritative only within the I policy-domain sequencer. D positions remain D-issued. Storage positions remain Storage-local. Wall-clock timestamps, H receiver sequence, message arrival order, timeout, missing ACK or reconnect cannot establish cross-authority order.

For a recovery-batch profile, the message MUST distinguish a proven empty pre-batch participant set from an absent/incomplete enumeration. A missing participant-set completeness attestation, missing owner high-water proof, incomplete participant reconciliation, unknown I/D/Storage outcome, or mismatched transaction/digest is rejected or held UNKNOWN/IN_DOUBT. COC recovery observation does not itself release I/D owner-local pending gates; only the corresponding owner-signed gate disposition can do so.

This §11.8 is a candidate mapping reservation against G's exact-version CGH-APPLIED-1.1 decision history. It does not claim that the current H JSON Schema/SDK already contains these fields, that COC or recovery-batch infrastructure is deployed, or that JF-10/COC conformance has run. H must publish an exact additive schema version and obtain the relevant C/G/I/D/Storage confirmations before claiming this bridge complete.


### 11.9 Explicit C provider outcome and owner-local gate release bindings — candidate

The recovery-batch mapping in §11.8 MUST explicitly preserve C's provider outcome and the distinction between COC observation and owner-local gate release:

- `c_provider_receipt_ref` and immutable `c_submit_outcome_ref` are C-issued. They bind the actual provider/runtime submit result to the exact InferenceRequestId, FinalRequestBoundaryId, request digest and participant/request identity. A COC observation, H transport ACK, local Adapter receipt or timeout MUST NOT substitute for either reference.
- Where C outcome is ACCEPTED or REJECTED, the corresponding C-issued terminal outcome reference is REQUIRED. Where C outcome is UNKNOWN, the participant remains IN_DOUBT and cannot support Full Applied.
- `participant_terminal_proof_ref` is present only when every required owner outcome is determinate and reconciled; it MUST be absent while any required I/D/C/Storage outcome is PENDING or UNKNOWN.
- If an I or D owner-local pending gate exists, only that owner may emit its own `owner_gate_release_attestation_ref`. H/COC may transport and preserve the reference but MUST NOT emit, infer or synthesize REOPENED. A `REMAINS_CLOSED` disposition is fail-closed and cannot authorize protected admission.
- A COC recovery-batch record or reconciliation observation is not itself an owner gate release, provider success, D clearance, I authorization, or Storage terminal outcome.

Missing C provider receipt/outcome, fabricated terminal proof, owner gate release from the wrong authority, or any attempt to treat UNKNOWN as terminal is rejected or remains UNKNOWN/IN_DOUBT. This candidate mapping does not change the authority ownership or claim that the related recovery/conformance suite has run.
