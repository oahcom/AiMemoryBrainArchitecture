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
