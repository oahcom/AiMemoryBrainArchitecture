# H Module Baseline & Redlines — PROPOSED

- Proposal ID: H-MBR-001
- Version: 0.1.0
- Status: PROPOSED — NOT APPROVED
- Owner role: H — BMCP Protocol Architect
- Branch: `session-h-bmcp-protocol`
- Reviewed branch HEAD: `08cca6341c3c44ad8502c215eba2b1941a8febb7`
- Date: 2026-11-17
- Template: requested `00-governance/module-baseline-and-redlines-template.md` returned 404 on main and is absent from the reviewed H tree. This proposal uses the requested 14-section structure; no template compliance is claimed.
- Scope: H protocol authority only. This proposal does not decide B domain types, I identity trust/permission, G Applied, C final-request facts, D ForgetFence or PGA governance approval.

## 1. Module Mission

H owns the Brain Memory Communication Protocol (BMCP) normative wire contract and transport-facing semantics between Brain services and heterogeneous Agent Adapters: wire envelope, protocol/schema versioning, compatibility, capability negotiation, delivery receipts, ACK semantics, reconnect, idempotency, replay protection and transport binding.

H defines what a message means on the wire and what an authenticated Adapter can attest within its declared target/session/region/capability scope. H does not own the desired Context state, final inference request, authorization policy, canonical Forget, or global completion.

## 2. Ownership Baseline

**H is authoritative for:**
- BMCP envelope, message families, schema IDs and protocol version policy.
- Required/optional/unknown field behavior and compatibility negotiation.
- Encoding/transport binding semantics and authenticated channel requirements.
- Adapter capability declaration, capability profile/version and CapabilityEpoch lifecycle.
- Delivery receipt and ACK evidence taxonomy, correlation, idempotency and replay behavior.
- Reconnect/resume rules and stale-session rejection.
- Protocol conformance vectors and wire-level validation.

**H is not authoritative for:** B typed domain/reference semantics; I Principal/Issuer trust, PermissionDecision, PermissionEpoch or revocation order; G Context membership/version/Applied record; C final-request submission/provider handoff/execution facts; D ForgetFence/lineage/work barrier; I Global Forget inventory/seal/completion; Storage durable transaction implementation; PGA project governance.

## 3. Capability Baseline

| Capability | Baseline | Status |
|---|---|---|
| Wire envelope | Explicit message type, schema/protocol version, correlation, idempotency, authenticated context binding | DECIDED design |
| Versioning | Negotiated compatible profile; no silent major downgrade | DECIDED design |
| Schema compatibility | Unknown optional fields may be ignored only where profile permits; unknown critical/required fields fail closed | DECIDED design |
| Adapter capability | Explicit Tier 1/2/3 and per-region observability/clear capabilities | DECIDED design |
| Delivery receipt | Proves protocol receipt within authenticated target/session scope only | DECIDED |
| ACK semantics | Typed action-specific evidence; never infer broader state | DECIDED |
| Reconnect | Fresh authentication, current PermissionEpoch/fence, capability and reconciliation before resume | DECIDED |
| Idempotency/replay | Stable operation ID + digest; same identity/digest replay idempotent; changed digest conflict | DECIDED design |
| Transport binding | Payload claims compared with authenticated verifier/channel context | JOINT TECHNICAL BASELINE; runtime NOT VERIFIED |
| Applied ACK schema | 1.1.0 JSON schema candidate exists; concrete global freeze remains OPEN pending exact-version owner decisions and conformance | OPEN |

## 4. Domain Ownership

H owns BMCP envelope and schema identifiers, ProtocolVersion, SchemaVersion, MessageType, CorrelationId, IdempotencyKey, DeliveryReceipt, ACK family/status, CapabilityProfile, CapabilityEpoch, AdapterSession binding, replay/nonce/correlation semantics and transport binding metadata.

H transports and validates references without redefining them: PrincipalRef, ActorRef, ProducerRef, AdapterRef, ScopeRef, EnvironmentRef, PermissionEpoch, ForgetFence/Generation, ContextVersion, DeliveryId, InferenceRequestId and FinalRequestBoundaryId remain typed by their owning modules (B/I/D/G/C). H must preserve type identity and namespace boundaries in serialization.

## 5. Interface Baseline

1. **Envelope:** Every protected message carries protocol/schema identity, message family, stable message/correlation IDs, idempotency identity/digest where applicable, authenticated session/channel binding and explicit target scope. Payload identity is never authentication.
2. **Identity binding:** Principal, Actor, Producer, Adapter, Scope and Environment claims are checked against verifier-established authenticated context. Caller-supplied identity fields cannot create a Principal or permission grant. Missing, ambiguous or mismatched required bindings reject/quarantine.
3. **Permission:** PermissionEpoch is carried as an opaque typed value. H does not decide whether it is current; I is authority. Protected operations require current verifier/policy proof at the relevant boundary; stale/gapped/unavailable epoch fails closed.
4. **Capability negotiation:** Adapter declares protocol/schema profiles, Tier 1/2/3 observability, final-request visibility, managed-region inventory, persistence, clear/suppress, local buffer/cache purge and queued-delivery cancellation capabilities. Each capability includes exact Adapter instance, session/region coverage, revision and limitations.
5. **CapabilityEpoch:** Changes when Adapter identity/build, runtime hook, managed-region boundary, queue/cache inventory or relevant apply/clear capability changes. Evidence cannot transfer to replacement Adapter or changed region.
6. **Delivery and ACK:** Distinguish receipt, materialization, final request submission evidence transport, Applied result, execution-start observation and Forget action ACK. Each binds exact target, Adapter, session, region, capability epoch, message ID, digest, timestamp and authenticated channel evidence.
7. **Idempotency:** Same key + same canonical digest returns the same terminal result without repeating side effects. Same key + different digest returns IDEMPOTENCY_CONFLICT and does not mutate state. ACK replay across sessions is historical only and cannot mutate current state.
8. **Reconnect:** Authenticate anew; re-resolve identity and Scope/Environment; obtain current I PermissionEpoch and D fence; renegotiate capability; reject stale session/ACK; reconcile G Context; clear/suppress stale managed region before resuming.
9. **Unknown fields:** Unknown critical/required field, unsupported major version, missing requiredness profile, duplicate-key/canonicalization ambiguity or incompatible schema must reject safely. Unknown optional fields are accepted only when explicitly declared safe by the negotiated profile.

## 6. Security Baseline

- Payload declaration does not authenticate identity; authenticated transport/verifier binding is mandatory for protected operations.
- ActorRef is not a credential; ScopeRef is not a permission grant.
- Caller-supplied identity is not authenticated identity; mismatch is reject/quarantine + audit.
- Unknown/revoked Issuer, expired credential/delegation, stale PermissionEpoch, invalid audience/purpose, cross-Scope/Environment without explicit grant and unsupported protected capability fail closed.
- Revocation order and current PermissionEpoch are I-owned. H must preserve and enforce the I decision at the protocol boundary without inventing ordering.
- Replay protection binds message/ACK to exact authenticated Adapter, session, audience, target, nonce/sequence and digest. Old-session evidence cannot be projected to a new session.
- Unknown Target, unsupported action, partial coverage, missing capability or ambiguous status is Unknown/blocked, never success.
- ACK claims are bounded to Adapter/Session/Target/Region/CapabilityEpoch and exact action. No ACK means global Forget.
- Forget action ACK and Applied evidence use distinct message families, schemas and status enums.
- Transport integrity (signature/MAC/channel binding) protects evidence; it does not elevate the sender's authority beyond I/G/C/D ownership.

## 7. Module Redlines

| ID | Redline | Required behavior |
|---|---|---|
| H-RL-01 | Payload != identity | Verify against authenticated channel/principal context |
| H-RL-02 | Receipt != Materialized | Separate receipt and managed-region observation |
| H-RL-03 | Delivered != Applied | No transport ACK can promote G Applied |
| H-RL-04 | Applied != Execution Started | Preserve separate C/Runtime evidence |
| H-RL-05 | ACK != Global Forget | Scope ACK to exact target/action/region/session |
| H-RL-06 | No stale ACK replay | Bind to current authenticated session and idempotency digest |
| H-RL-07 | No changed-digest replay | Reject as IDEMPOTENCY_CONFLICT without state mutation |
| H-RL-08 | No silent major downgrade | VERSION_UNSUPPORTED; do not weaken authentication |
| H-RL-09 | Unknown critical field fails closed | No dropping required security or target fields |
| H-RL-10 | Capability claims need coverage | No bit-only or unbounded clear/apply claims |
| H-RL-11 | Capability epoch is instance-bound | No evidence transfer across Adapter replacement |
| H-RL-12 | Unknown target is not ignored | Explicit Unknown/Unsupported/Failed status |
| H-RL-13 | Forget ACK != Applied ACK | Distinct schemas, enums and state machines |
| H-RL-14 | No authority takeover | H transports evidence; owning module decides its semantics |

## 8. Forbidden Cross-module Actions

H must not:
- Define B's Typed Reference, Scope or Environment semantics.
- Authenticate an identity merely because the payload contains PrincipalRef/ActorRef/ProducerRef.
- Decide I Permission, issuer trust, delegation eligibility, PermissionEpoch currentness or revocation ordering.
- Decide G ContextVersion, Context membership, Applied predicate, Applied history or current-use eligibility.
- Decide C final request submission, provider receipt, model use or Execution Started.
- Create/advance D ForgetFence or declare a canonical barrier drained.
- Declare a target inventory complete, accept exceptions or declare Global Forget complete.
- Convert Adapter ACK into proof of external-provider erasure or physical deletion.
- Mark H36 or any conformance suite passed without executable evidence.
- Modify other Owner branches, main, or merge branches as part of this proposal.

## 9. Dependency Contracts

| Dependency | Required input/output | Owner | Current disposition |
|---|---|---|---|
| Domain/typed identity | Typed Principal/Actor/Scope/Environment/Producer/Adapter references | B | Joint design baseline; B remains type authority |
| Trust and permission | Authenticated Principal, issuer, PermissionDecision, PermissionEpoch, revocation | I | Joint technical baseline; external governance blocked; I36 not run |
| Context and Applied | ContextVersion, Delivery, G Applied result and exact evidence requirements | G | G accepted CGH-APPLIED-1.1 evidence semantics; H must reconcile exact package/digest |
| Final request | Immutable final-request submission/provider receipt | C | C owns factual evidence |
| Canonical Forget | ForgetFence, lineage, barrier and causal order | D | D authority; H only carries scoped evidence |
| Global inventory | TargetId, inventory seal, action/evidence profile and exception | I | Candidate policy; seal/completion not evidenced |
| Storage | Durable idempotency/receipt/recovery and security event audit | Storage | Implementation proof not established |
| Governance | External trust, retention, cross-scope and exception approvals | PGA / authorized governance bodies | GOVERNANCE-BLOCKED |

## 10. Conformance Requirements

Required suites:
- H-ENV: required envelope fields, schema IDs, canonicalization, duplicate-key and malformed payload rejection.
- H-VERS: compatible minor evolution, unknown optional fields, unknown critical fields, unsupported major version and downgrade attempts.
- H-AUTH: forged Principal/Actor/Producer/Adapter, unknown/revoked issuer, expired credential/delegation, payload/channel mismatch and missing Scope/Environment.
- H-PERM: stale/gapped PermissionEpoch, revocation races and policy authority unavailable.
- H-CAP: Tier 1/2/3 truthfulness, final-request visibility, managed-region enumeration, CapabilityEpoch change and replacement Adapter.
- H-ACK: exact target/session/region/action binding; distinct receipt/materialization/applied/forget ACK; partial/unknown/unsupported handling.
- H-IDEM: same ID/same digest replay, same ID/changed digest conflict, nonce reuse, ACK collision and replay across sessions/audiences.
- H-REC: reconnect during revocation, stale ACK, lost ACK, offline Adapter, capability downgrade and current snapshot reconciliation.
- H-APPLIED: wire representation of exact G target, C final request, I authorization and D fence evidence without assuming any owner's decision.
- H-FORGET: suppression, local buffer clear, local cache purge and queued delivery cancellation as distinct target actions; no global inference.
- H-COC: schema validation and deterministic causal-order/terminal proof transport for the 1.1 recovery bridge.

Existing H36-01..18 and H36-SR race additions are specified but NOT RUN. Passing requires executable fixtures, exact build/commit, commands, expected/actual outputs, logs, deterministic race ordering and Owner review.

## 11. Acceptance Criteria

1. Wire message families and evidence scopes are explicit and versioned.
2. Every protected identity is verifier-bound; payload identity mismatch rejects.
3. ACKs are idempotent, digest-bound, session-bound and target/action-scoped.
4. Unknown critical/incompatible schema and unsupported target fail closed.
5. Capability declarations are instance/region/epoch-bound and accurately describe observability.
6. Receipt, Materialized, Final Request Submitted, Applied, Execution Started and Forget ACK remain distinct.
7. H's exact-version decisions identify the same Applied contract package and digest accepted by C/G, with I/D/B authority evidence retained.
8. H36 and wire conformance execute and pass before runtime acceptance; no pass is claimed here.
9. Owner acceptance is distinct from proposal commit and external governance approval.

## 12. Change Authority

H alone changes BMCP envelope, schema, protocol compatibility, capability negotiation, transport binding, receipt/ACK semantics, reconnect, idempotency and replay protocol. B owns typed reference semantics; I owns trust/authorization; G owns Context/Applied; C owns final-request evidence; D owns ForgetFence; I owns global inventory; PGA owns project governance approval. Cross-boundary changes require exact-version impact review and explicit decisions from affected owners.

## 13. Open Decisions

- Concrete BMCP Applied schema freeze: OPEN. H branch contains `bmcp.applied-ack/1.1.0` JSON Schema candidate (Blob `a8a945cc3623c2907003b93625e3c79742150944`), but H's current formal exact-package decision explicitly says concrete versioned schema is not frozen and Applied Contract Frozen = NO.
- C/G/H exact Applied package version and digest alignment: OPEN. G's 1.1 acceptance and H's existing exact decision must be reconciled against the same A package Blob and schema digest; no implicit upgrade from H's earlier decision.
- H BIH identity consumer design acceptance: recorded in H's dedicated consumer acceptance artifact and I's later reconciliation; this is design acceptance only, not H36 runtime proof.
- H36-01..18 and H36-SR-02/03/04/05/07: SPECIFIED / NOT RUN.
- H adapter capability runtime evidence, transport authentication implementation and cross-language interoperability: TO_VALIDATE.
- I36 runtime tests, global Forget inventory seal, backup/restore proof and external approvals: OPEN / BLOCKED.
- D/Storage causal-order and persistence realization: TO_VALIDATE.
- Requested template path: 404 on main and absent from reviewed H tree.

## 14. Explicit Non-Claims

This proposal does not claim H Owner formal approval of CGH-APPLIED-1.1, concrete 1.1 schema freeze, production transport implementation, Adapter conformance, H36/I36 test pass, authenticated identity deployment, Global Forget completion, physical erasure, backup restore safety, project governance approval or production readiness. Publication of this proposal is not protocol approval.
