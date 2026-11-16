# Phase 3.6 — CGH-APPLIED-1.1 Causal-Order Successor Decision Package

- Owner: A — Principal Integration Architect
- Status: **A CANDIDATE PACKAGE / OWNER REVIEW REQUIRED / NOT FROZEN**
- Common contract: `CGH-APPLIED-1.1`
- Causal-order profile: `CausalOrderProfile/1.0`
- H schema target: `bmcp.applied-ack/1.1.0`
- Supersedes for new causal-order Full Applied flows: CGH-APPLIED-1.0 only after explicit owner acceptance and migration decision.
- Prior immutable package: `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`, Blob SHA `122b164bcc0760b83bf555072a36fc55631623e1`.
- This candidate does not change, rewrite or retroactively extend any CGH-APPLIED-1.0 Owner decision.

## 1. Purpose and decision requested

This package integrates the C/I/D cross-authority causal-order contracts and H's 1.1.0 wire-schema candidate into one reviewable successor. It requests explicit Owner acceptance, amendment or rejection from B, C, D, G, H, I and the coordinator/Storage operator.

The objective is to prove the relative order of:
- C's actual successful provider/runtime final-submit boundary;
- I's authorization receipt consumption and PermissionEpoch revocation effective point; and
- D's ForgetFence installation and complete target/source/ancestor lineage barrier.

Independent timestamps, local sequence numbers, H receiver ingress order, cached currentness reads and detached preflight ALLOW are not causal proof.

## 2. Authority ownership

| Concern | Sole authority | Contract obligation |
|---|---|---|
| Principal/issuer/delegation, authorization, PolicyDomainRef, PermissionEpoch and revocation | I | Issue and consume single-use CommitAuthorizationReceipt; sequence exact owner gate against revocation |
| ForgetOperation, ForgetFence/Generation, target/source/ancestor lineage and D barrier | D | Bind participant intent to exact lineage; hold fence barrier through unresolved participant |
| Actual immutable final request and successful provider/runtime submit evidence | C | Invoke provider only after durable intent + I/D clearances + reservation; emit immutable CSubmitOutcome |
| ContextVersion, Delivery, Full Applied commit/idempotency and current-use projection | G | Validate all owner evidence and terminal order proof; alone commit Applied |
| BMCP serialization, authentication, ACK, capability and reconnect transport | H | Publish/transport exact versioned schema; preserve owner-issued refs; no authority substitution |
| ActorRef, ScopeRef and EnvironmentRef semantic types | B | Confirm unchanged typed semantics and role-preserving bindings for 1.1 |
| Durable participant registry/order service, HA/failover/restore | Named coordinator/operator with owner acceptance | Supply common durable ordering only; no shadow authorization or Forget authority |

## 3. Normative causal-order protocol candidate

### 3.1 Stable operation and protection-domain binding

Before any provider side effect, C creates a stable `CausalOrderTransactionRef` and obtains a durable `ParticipantIntentRef` from the registered coordinator. The intent binds:

- exact immutable final-request digest and canonicalization profile;
- FinalRequestBoundaryId and InferenceRequestId namespace/reservation correlation;
- ContextId/ContextVersion, DeliveryId/DeliveryAttemptId;
- ManagedRegion identity, inventory, complete digest and source/ancestor lineage-set digest;
- authenticated Issuer/Principal/Actor/Agent/Adapter/runtime/session;
- role-labelled ScopeBindingSet and applicable EnvironmentRef;
- I PolicyDomainRef/PermissionEpoch and I CommitAuthorizationReceipt binding;
- D ForgetOperationRef/ForgetFenceRef/ForgetFenceGeneration and D lineage coverage;
- H CapabilityEpoch and negotiated evidence profile.

The intent is a durable participant registration, **not permission to submit**. Multi-PolicyDomain operations remain BLOCKED unless I provides an all-or-none domain-set protocol. Incomplete/multiple canonical-authority lineage that cannot be atomically represented remains UNKNOWN/UNSUPPORTED.

### 3.2 Owner authorization and fence participation

1. **I:** I validates the complete authorization tuple online and issues a single-use CommitAuthorizationReceipt bound to the exact intent, transaction, boundary and request digest. I consumes it exactly once in its authoritative PolicyDomain sequencer and emits IAuthorizationTerminalRef. The terminal ref binds the applicable IRevocationRequestRef and its request/cutoff position, or explicitly states that no earlier revocation request existed at terminalization. If a revocation request position precedes ParticipantIntentRef, no new intent/receipt is admitted for that affected operation. If intent precedes the revocation request but the receipt is not yet consumed, I may still order revocation first; receipt consumption returns REVOCATION_WON. Outcomes:
   - `COMMIT_WON`: the exact owner gate was ordered before a conflicting revocation request/effective point;
   - `REVOCATION_WON`: revocation was ordered first; C must abort before provider side effect;
   - `UNKNOWN/IN_DOUBT`: no favorable inference.
2. **D:** D binds the same ParticipantIntentRef to the exact ForgetOperation/Fence and complete target/source/ancestor lineage. Every applicable DForgetFenceRequestRef is durably recorded with its coordinator request/cutoff position. If a fence request position precedes the intent, D returns FENCE_WON and denies clearance even if effective fence commit is still draining older participants. If intent precedes the fence request, D includes the participant in the barrier and the later fence remains pending. DParticipantClearanceRef binds the intent, exact lineage inventory version and proof that no earlier fence request/effective fence suppresses it. D terminal evidence separately binds the fence-request cutoff and eventual fence-effective position; these positions must not be conflated.
3. I retains its sequencer and effective-epoch authority. D retains its fence-generation, lineage and barrier authority. Coordinator positions never mint or replace either owner token.

### 3.3 Final reservation and provider boundary

1. The coordinator verifies that the durable ParticipantIntentRef, I receipt/terminal reference and D fence/lineage/clearance references all bind the same transaction, exact digest, final boundary and participant.
2. It finalizes a durable ParticipantReservationRef. No provider call is permitted before this step.
3. C invokes the provider/runtime exactly once under the reservation's stable idempotency/attempt contract.
4. C captures the actual provider receipt and actual InferenceRequestId, then appends immutable CSubmitOutcomeRef:
   - `ACCEPTED` only for observed successful provider/runtime handoff;
   - `REJECTED` only for definitive no-handoff;
   - `UNKNOWN` when the outcome cannot be established.
5. The coordinator emits CausalOrderTerminalProofRef only after C, I and D evidence is durable and reconciled. The proof binds the transaction, ParticipantIntentRef, ParticipantReservationRef, all owner refs, ordered coordinator positions, terminal outcome and exact evidence digests.
6. C emits Final Request Submitted only for successful actual provider handoff plus a determinate terminal proof. A reservation, I COMMIT_WON, D clearance, H receipt or coordinator intent alone is not submission proof.
7. G independently validates the complete C/H/I/D/B/G predicate and is the only authority that commits Applied.

### 3.4 Race semantics

| Race | Required order/result | Applied consequence |
|---|---|---|
| I revocation request before ParticipantIntentRef | No new intent/receipt for the affected operation; REVOCATION_WON | No provider call / no Full |
| ParticipantIntentRef before I revocation request, but receipt not yet consumed | I may order revocation first; receipt consumption returns REVOCATION_WON | C aborts before provider call |
| I receipt consumed as COMMIT_WON before later revocation request | Revocation remains pending behind exact participant until safe terminal outcome | If submit succeeds, historical fact precedes later revocation; current use invalidated |
| D fence request cutoff before ParticipantIntentRef | FENCE_WON; D denies clearance even if effective fence commit is still draining older participants | No provider call / no Full |
| ParticipantIntentRef before D fence request cutoff | D records participant in barrier; fence remains pending until exact C outcome or safe abort is durable | Successful submit may be historical; current use invalidated by later fence |
| Provider success with all owner evidence | CSubmitOutcome ACCEPTED; terminal proof determinate | Candidate Full Applied only after G validation |
| Provider definitive no-handoff | CSubmitOutcome REJECTED; safe ABORTED terminal | No Full; release participant only with immutable proof |
| Provider outcome unknown after timeout/crash | IN_DOUBT; same transaction/participant/provider idempotency key is recovered | No Full; D/I barriers remain open |
| Coordinator outage, rollback, conflicting digest or contradictory owner refs | UNKNOWN/IN_DOUBT; fail closed | No Full; suppress protected content |

I `COMMIT_WON` is an authorization/order outcome for the exact owner gate; it is **not** proof that the provider accepted the request. CSubmitOutcome is a separate C-owned fact. DParticipantClearance is a separate D-owned fact. The coordinator terminal proof binds them but does not replace any owner authority.

### 3.5 Recovery and anti-heuristic rules

- Same CausalOrderTransactionRef and provider idempotency identity are used for recovery after ambiguous outcome; never retry as a new operation.
- No automatic reservation expiry may release I/D barriers while provider outcome is unknown.
- Process death, timeout, lease expiry, lost ACK, queue deletion, worker replacement or coordinator disconnection is not terminal proof.
- Coordinator restore must be monotonic and must not regress terminal positions or clear unresolved participants.
- Conflicting same-ID/different-digest evidence is quarantined; same-ID/same-digest replay is idempotent.
- If any required owner evidence, lineage or exact digest cannot be reconciled, retain UNKNOWN/IN_DOUBT and suppress protected current use.
- Evidence retention must not retain forgotten plaintext merely to preserve proof; keep only permitted non-reconstructive digests and authority references.

## 4. H 1.1.0 wire-schema candidate mapping

H's Owner artifact `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`, Blob `5cbf0bb548a46671054cb22c6fab3c3d007365d4`, now describes `bmcp.applied-ack/1.1.0` as an H-owned schema candidate (not production-frozen/deployed). This candidate package requires H to pin that exact schema artifact and complete all requiredness, canonicalization, crypto, replay, compatibility and conformance details.

Required opaque references include:

- `CausalOrderProfileRef`, `CausalOrderCoordinatorRef`, `CausalOrderTransactionRef`, `CausalOrderPosition`;
- `ParticipantIntentRef`, `ParticipantReservationRef`;
- I `CommitAuthorizationReceiptRef`, `IAuthorizationTerminalRef`, applicable `IRevocationRequestRef` and I request/cutoff position (or explicit no-earlier-request assertion);
- D `DForgetFenceRequestRef` and request/cutoff position, `ForgetFenceRef` and effective position, `ForgetLineageCoverageRef`, `DParticipantClearanceRef` bound to ParticipantIntentRef;
- C `CSubmitOutcomeRef`, actual provider receipt, actual InferenceRequestId and FinalRequestBoundaryId;
- `CausalOrderTerminalProofRef`, terminal outcome and proof digest.

Required message families include `CAUSAL_ORDER_INTENT`, `CAUSAL_ORDER_INTENT_RECEIPT`, `CAUSAL_ORDER_RESERVATION`, `I_AUTHORIZATION_TERMINAL`, `D_FENCE_TERMINAL`, `C_SUBMIT_OUTCOME`, `CAUSAL_ORDER_TERMINAL_PROOF` and `CAUSAL_ORDER_ACK`. Forget Action ACK remains a separate evidence family. H transports and integrity-protects owner-issued references; it does not mint or validate I/D/C/G decisions.

## 5. Conformance required

All cases below remain **SPECIFIED / NOT RUN** until reproducible fixtures, environment/build identity, raw outputs and reviewer evidence are attached.

- CO-01: ParticipantIntent is durable before any provider side effect.
- CO-02: wrong digest, wrong boundary, replayed I receipt or mismatched transaction is rejected.
- CO-03: I revocation request before ParticipantIntentRef blocks intent/receipt admission; provider is never called.
- CO-04: I revocation request after intent but before receipt consumption returns REVOCATION_WON; provider is never called.
- CO-05: D fence request cutoff before intent returns FENCE_WON; no D clearance and no provider call.
- CO-06: D fence request after intent remains pending behind exact participant until submit/abort terminal.
- CO-07: I revocation after COMMIT_WON remains pending until participant terminal outcome.
- CO-08: successful provider submit followed by later fence/revocation preserves history but invalidates current use.
- CO-09: provider outcome unknown after crash; participant IN_DOUBT, no new transaction/retry, barriers remain open.
- CO-10: coordinator failover/restore cannot regress positions or clear participants.
- CO-11: wall-clock/receiver order deliberately inverted; common order and owner terminal evidence remain decisive.
- CO-12: contradictory I/D/C terminal evidence and same-ID/different-digest are quarantined.
- CO-13: incomplete/late-discovered source or ancestor lineage invalidates D clearance.
- CO-14: G rejects a valid transport ACK or I COMMIT_WON without C provider success evidence.
- CO-15: H 1.1.0 rejects unknown critical fields, downgrade to 1.0.0 for Full Applied, malformed opaque refs and missing conditional fields.

C-CO, I-CO, D-CO and H36-CO suites must align with these cases. G must add Applied acceptance/current-use cases for the exact 1.1 evidence set.

## 6. Owner evidence and decision status

| Owner | Current evidence | Status for this candidate |
|---|---|---|
| C | `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`, Blob `f2c5b379cacfedd81500e8496d3053b628e144a0` | C-side specification published; exact A 1.1 package acceptance pending |
| D | `03-memory-brain/phase-3.6-d-forget-fence-causal-participant-barrier-contract.md`, Blob `317a9bc170c5a66720f738bf24bbf93c87385887` | D-side specification published; coordinator/Storage deployment and exact package acceptance pending |
| I | `09-security-governance/phase-3.6-i-commit-authorization-causal-order-contract.md`, Blob `71779133a4f95d63a24c4c7e606af174763366f1` | I-side specification published; service deployment, external governance and exact package acceptance pending |
| H | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`, Blob `5cbf0bb548a46671054cb22c6fab3c3d007365d4` | H 1.1.0 schema candidate described; not production-frozen; exact package acceptance pending |
| G | Existing G exact decision is for CGH-APPLIED-1.0 only | Explicit 1.1 predicate/evidence acceptance required |
| B | Existing B semantic confirmation is for CGH-APPLIED-1.0 only | Confirm whether unchanged typed semantics are accepted for exact 1.1 package |
| Coordinator / Storage operator | No named/deployed operator or production durable service verified | OPEN; topology, store, HA, failover, restore, retention, key trust and SLO acceptance required |

C/D/I specification artifacts do not themselves constitute cross-owner acceptance of this A package. H schema candidate does not constitute deployed wire interoperability. No 1.1 approval is inferred from a 1.0 decision.

## 7. Stop conditions and current gate

Stop and retain BLOCKED if:
- participant intent is not durable before provider side effect;
- I receipt is not single-use and bound to exact operation/digest/boundary;
- D clearance does not cover the complete target/source/ancestor lineage;
- I/D barriers do not survive crash/failover and provider outcome ambiguity;
- provider success is inferred without actual provider receipt;
- coordinator can regress order positions or clear IN_DOUBT participants on restore;
- H wire schema omits required authority references or permits 1.0 downgrade for Full Applied;
- G cannot independently validate all owner evidence;
- tests or implementation claims lack reproducible evidence.

Current status:
- CGH-APPLIED-1.1 package: **A CANDIDATE / OWNER REVIEW REQUIRED**.
- C/D/I causal-order specifications: **PUBLISHED / READ BACK**.
- Exact C/D/I/H/G/B acceptance of this package: **PENDING**.
- H 1.1.0 schema: **OWNER CANDIDATE / NOT PRODUCTION-FROZEN / NOT DEPLOYED**.
- Coordinator and participant registry: **NOT DESIGNATED / NOT DEPLOYED / NOT VERIFIED**.
- C-CO/I-CO/D-CO/H36-CO/G conformance: **SPECIFIED / NOT RUN**.
- Applied Contract Frozen: **NO**.
- Implementation Verified: **NO**.
- Phase 3.6 G10: **BLOCKED**.

No branch merge, production activation, architecture freeze, test PASS or Global Forget completion is authorized by this candidate package.


## 8. A source-pin reconciliation — 2026-11-16

A re-fetched the current C/D/I/H Owner artifacts after the previous candidate publication. The current H schema source pin is now `5cbf0bb548a46671054cb22c6fab3c3d007365d4` (branch `session-h-bmcp-protocol`), superseding the earlier H pin `a23b9a879a3ec0e212645a8247a6797bd0055360`. The normative C/D/I source pins remain C `f2c5b379cacfedd81500e8496d3053b628e144a0`, D `317a9bc170c5a66720f738bf24bbf93c87385887`, and I `71779133a4f95d63a24c4c7e606af174763366f1`. This is a source-reference reconciliation, not a new H acceptance or deployment claim.

The current G Applied contract and B typed-reference confirmation were also re-read. Their published semantic decisions are not an explicit acceptance of this exact CGH-APPLIED-1.1 candidate. G and B exact-version decisions remain required. No C/D/I/H exact-package acceptance is inferred from their component specifications. Coordinator/Storage operator acceptance and deployment remain absent; all causal-order suites remain NOT RUN.
