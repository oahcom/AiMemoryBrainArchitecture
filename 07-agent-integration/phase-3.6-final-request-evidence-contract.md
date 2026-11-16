# Phase 3.6 — Final Request Evidence Contract

- Owner: Session C — Agent Integration, Telemetry and Final Request Boundary
- Status: **C semantic decisions recorded; C/G/H cross-owner freeze BLOCKED; implementation and execution NOT VERIFIED**
- Branch: session-c-agent-integration-2026-11-16
- Authority: C owns production of Agent-side final-request submission evidence. H owns wire/ACK/capability protocol. G owns Context Applied state. I owns authorization. D owns Forget fence.

## 1. Evidence-stage vocabulary

These stages are distinct and MUST NOT be collapsed:

| Stage | Meaning | Authoritative evidence | Does not prove |
|---|---|---|---|
| Context Prepared | G created an immutable authorized target version and delivery intent | ContextVersion, ChangeSet, DeliveryId/attempt intent | Sent, received, materialized or applied |
| Context Delivered | H transport endpoint accepted the exact delivery attempt | Authenticated H delivery receipt | Managed-region installation |
| Context Materialized | Adapter placed the exact content in its declared Brain-managed region | Adapter-local materialization evidence, region identity and digest | Final request inclusion or submission |
| Final Request Submitted | Exact immutable post-transformation inference request crossed the observed submit boundary | C-produced, integrity-protected submission evidence bound to actual request and boundary | Model attention, understanding or execution start |
| Applied | G accepted the complete C/H evidence under the Applied predicate | G authoritative Applied record | Model attention, understanding, memory use or correct behavior |
| Execution Started | Runtime/provider reports execution start for that request | Runtime/provider execution-start receipt, correlated to InferenceRequestId | Completion, response correctness or memory use |

A Delivered ACK is not Materialized. Materialized is not Final Request Submitted. Submission is not Applied until G validates it. Applied is not Execution Started.

## 2. C Final Request Submission Evidence

C emits a per-request immutable evidence record only when its integration can observe the actual final immutable request after all transformations and the successful handoff to the inference runtime/provider.

Required fields:

- `InferenceRequestId`: actual request identifier assigned by the runtime/provider boundary, not a locally invented correlation token.
- `FinalRequestBoundaryId` and boundary type: exact hook/submit boundary and evidence profile.
- `ContextId`, `ContextVersion`, `DeliveryId`, `DeliveryAttemptId`: exact G target and attempt.
- Authenticated `AgentPrincipal/AgentRef`, Agent instance, `AdapterPrincipal/AdapterRef`, Adapter instance, Runtime instance and Runtime Session; all resolved from protected authenticated bindings, not payload claims.
- Exact `ScopeRef`, `EnvironmentRef` where required, and Managed Region identifier/inventory.
- Canonicalized Managed Region content digest and digest algorithm/version; digest covers the complete region content as actually embedded in the final request.
- `PermissionEpoch` and authorization decision reference, validated for this request boundary.
- `ForgetFenceGeneration/Cursor` and D validation reference for all source lineage represented in the region.
- `AdapterCapabilityEpoch`, negotiated capability profile and conformance profile version.
- Submission outcome, boundary timestamp/monotonic sequence where available, evidence issuer, integrity/signature/key reference, schema version, correlation/causation and audit reference.
- Coverage declaration: complete, partial, bypassed or unknown; exact omitted/unobservable request paths and region coverage.

C MUST NOT synthesize an InferenceRequestId from a DeliveryId, claim a successful submit from a local render, or infer execution start from submission.

## 3. Evidence integrity, immutability and invalidation

1. Evidence is append-only and immutable after issuance. Corrections are new superseding records linked to the original; no in-place rewrite.
2. Evidence integrity is verified against the authenticated Adapter/runtime issuer and the agreed H wire integrity profile. Payload identity strings alone are not credentials.
3. Digest canonicalization, signing keys, replay protection, schema IDs and wire encoding remain subject to H/C final agreement; until then they are candidate integration details.
4. A record is ineligible for Full Applied if any identity binding, request ID, region digest, delivery attempt, ContextVersion, Scope/Environment, PermissionEpoch, ForgetFence or CapabilityEpoch is missing, stale, unverifiable or mismatched.
5. Permission revocation, fence advancement, scope/environment change, capability epoch change, session replacement, delivery supersession, expiry or a newer Context head invalidate current-use eligibility. They do not erase a historically valid submission fact.
6. A historical Applied record remains an audit fact after Forget/revocation; it must be marked no-longer-current for subsequent use and must never seed a later request without fresh authorization and reconciliation.
7. Evidence retention must not retain forgotten plaintext merely to preserve proof. Keep only the minimum non-reconstructive digest, typed references and audit metadata permitted by I policy.

## 4. Capability ceilings

| Integration tier | Observable evidence | Permitted claim |
|---|---|---|
| Tier 1 — Full inference boundary | Exact final immutable request, actual submit, request ID, complete Managed Region digest and current authority bindings | May produce candidate Full Applied evidence for G validation |
| Tier 2 — Middleware | Controlled middleware materialization/insertion; final transformations or actual submit not fully observable | Partial/Unknown only; MUST NOT claim Full Applied |
| Tier 3 — Events/Recall | Event and Recall receipts only; no proactive final-request boundary | No Applied claim |
| Unsupported/Limited | Boundary, identity, digest or authority checks cannot be demonstrated | Explicit Unsupported/Limited; no Full Applied |

Tier is a demonstrated evidence ceiling, not a product label or declaration. Bypass paths must be enumerated per request. A local rendered prompt, middleware callback or transport ACK is insufficient for Tier 1.

## 5. G Applied Acceptance Predicate (C producer side)

C supplies evidence; G alone accepts Applied. Candidate Full Applied requires all of the following:

1. Exact ContextVersion matches G's immutable target.
2. DeliveryId and DeliveryAttempt match the active, non-superseded G attempt.
3. InferenceRequestId is actual, unique in its runtime domain and bound to the observed final boundary.
4. Agent, Adapter, runtime and session identities are authenticated, registered, current and mutually bound.
5. Managed Region identity and exact complete content digest match the delivered target.
6. ScopeRef and required EnvironmentRef exactly match the authorized Context.
7. PermissionEpoch and authorization decision are current at the submission boundary.
8. ForgetFenceGeneration is current for all source lineage at the submission boundary.
9. CapabilityEpoch is current and supports full final-boundary observation.
10. Final Request Submitted evidence is complete, integrity-valid, non-replayed, immutable and causally ordered after delivery/materialization.
11. No supersession, revocation, fence, scope, session or capability invalidation linearized before the submission boundary.
12. H protocol evidence required to authenticate delivery/Adapter identity and evidence transport is valid.

Missing or ambiguous fields fail closed to Partial/Unknown/Rejected. G MUST NOT infer Full Applied from a combination of weaker receipts.

## 6. Ordering, late evidence and idempotency

- ACK/evidence identity is scoped to Adapter instance + Runtime Session + DeliveryId + attempt + evidence kind + digest.
- Exact duplicate evidence is idempotent and returns the original disposition.
- Same identity with a different digest is a conflict; quarantine and emit a security/consistency event.
- Late evidence for a superseded attempt may establish a historical fact only. It cannot move G's current Applied pointer backward.
- Evidence from an old Runtime Session or Adapter instance cannot be rebound to a new session/capability epoch.
- A late ACK cannot roll back a newer ContextVersion or delivery.
- If submission occurred before a later Forget/revocation, preserve historical truth and mark current-use invalid. If fence/revocation linearized before submission, reject Full Applied.
- If ordering cannot be proven, status is Unknown and protected content remains suppressed.

## 7. Prompt injection and memory trust boundary

All Memory, Evidence, summaries, compacted text, retrieval snippets, observations and tool outputs are untrusted data. They MUST remain structurally separated from system/developer instructions, user input, tool definitions, tool authorization and Agent policy. Context content may describe an action but cannot authorize or execute it.

Provenance, source identity, Scope, trust/epistemic status, lifecycle and transformation lineage survive summary/compaction. A summary is a derived untrusted artifact, not a trust upgrade. Cross-Scope material is rejected before candidate admission and again before final request submission. A tool-call declaration is an intent/claim; only a separately authenticated tool result/side-effect receipt can establish execution.

## 8. C conformance matrix

All cases below are **SPECIFIED / NOT RUN** unless a future run attaches executable fixture, environment, expected/actual output and reproducible artifacts.

| ID | Fixture and operation order | Expected | Forbidden | Evidence |
|---|---|---|---|---|
| C-FR-01 | Tier 1; prepare, deliver, materialize, submit exact request | Candidate Full evidence for G | Mark Applied before G acceptance | Request ID, region digest, boundary proof |
| C-FR-02 | Materialize region; no submit event | Materialized only | Final Request Submitted / Applied | Materialization receipt; absent submit proof |
| C-FR-03 | Middleware cannot see final transform/submit | Partial/Unknown | Full Applied | Tier profile, bypass coverage |
| C-FR-04 | Final request digest differs from delivered region | Reject Full Applied | Digest mismatch ignored | Both digests and canonicalization profile |
| C-FR-05 | Permission revoked during final assembly before submit | Block/omit region; no Full Applied | Stale ALLOW promoted | Epoch/decision and boundary ordering |
| C-FR-06 | Fence advances before final submit | Suppress region; no Full Applied | Pre-fence materialization submitted | Fence proof and submit attempt |
| C-FR-07 | Valid submit then later revocation | Historical evidence retained; current-use invalid | Erase history or reuse old permission | Submission ordering and new epoch |
| C-FR-08 | Duplicate evidence, same digest | Idempotent original result | Duplicate promotion | Evidence ID/digest |
| C-FR-09 | Same evidence identity, altered digest | Conflict/quarantine | Last-write-wins | Both digests, security event |
| C-FR-10 | Old session ACK arrives after reconnect | Historical only or rejected | Rebind to new session | Old/new session and capability epoch |
| C-FR-11 | Summary contains malicious instruction | Treated as untrusted data | Instruction privilege escalation | Provenance/trust labels and region boundary |
| C-FR-12 | Tool call declaration without tool receipt | Intent only | Claim tool execution/side effect | Call declaration and absent result receipt |

## 9. Open findings and decision record

- **C-36-01 (BLOCKED):** H wire schema, signature/integrity, ACK and capability epoch exact mapping require H approval.
- **C-36-02 (BLOCKED):** G Applied state transitions and historical/current-use projection require G acceptance.
- **C-36-03 (BLOCKED):** I PermissionEpoch decision freshness/revocation semantics and B typed Scope/Actor binding require owner approval.
- **C-36-04 (BLOCKED):** D ForgetFence currentness and E/Storage durable publication/lineage evidence remain upstream dependencies.
- **C-36-05 (NOT RUN):** no executable Agent/Adapter final-boundary test evidence supplied in this design pass.

**C decisions:** stage separation; C is final-request evidence producer; exact final immutable request and actual submit are required for candidate Full evidence; Tier 2/3 cannot claim Full Applied; Memory remains untrusted data; historical Applied is retained but cannot be reused after invalidation.

**Cross-module status:** C/G/H Applied contract is not Frozen. This file specifies C's producer contract only and does not alter H wire or G state authority.
