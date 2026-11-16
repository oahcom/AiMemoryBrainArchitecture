# CGH-APPLIED-1.0 — Cross-Authority Final-Submit Causal Ordering Proposal

- Owner: A — Principal Integration Architecture
- Status: **INTEGRATION PROPOSAL / OWNER DECISION REQUIRED / NOT APPROVED**
- Common contract: `CGH-APPLIED-1.0`
- Exact A package: `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`
- Exact A package Blob SHA: `122b164bcc0760b83bf555072a36fc55631623e1`
- Decision scope: C final-submit boundary + I PermissionEpoch/revocation + D ForgetFence/lineage ordering; H transports evidence; G consumes it.
- Authority boundary: this proposal does not amend I, D, C, G or H Owner contracts. C/I/D must explicitly accept, amend or reject the proposed ordering protocol before it is normative.

## 1. Problem statement

C, I and D have confirmed their individual semantics for the exact CGH-APPLIED-1.0 package, but those confirmations do not establish a common production order among:

1. C's actual successful provider/runtime final-submit boundary;
2. I's durable PermissionEpoch advancement / revocation effective point; and
3. D's durable ForgetFence installation for the complete target/source/ancestor lineage.

I and D tokens are independent opaque namespaces. Sender timestamps, local monotonic clocks, H receiver ingress sequence, cached currentness reads and independently allocated cursors cannot prove a cross-authority total order. If order is not proven, the result must remain UNKNOWN and G must not commit Full Applied.

## 2. Required invariant

For one Full Applied candidate, the system must establish exactly one of these outcomes:

- **SUBMIT_WON:** the exact final request was successfully handed to the provider/runtime while the required I authorization and D fence/lineage state were current; every later revocation/fence transition is ordered after this terminal submit outcome. G may consider historical Full Applied only after validating all other predicates.
- **AUTHORITY_TRANSITION_WON:** I revocation/epoch advance or D fence installation was ordered before the final-submit gate. C must not submit protected content under the stale state; no Full Applied is eligible.
- **ABORTED:** the final-submit attempt is authoritatively proven not to have crossed the provider boundary. The reservation is released; a waiting authority transition may then become effective.
- **IN_DOUBT:** process/provider outcome or causal ordering cannot be established. No Full Applied; suppress protected current use; preserve durable recovery evidence. Never infer success or abort from timeout, process death, lease expiry or missing callback.

A later transition never rewrites a previously terminal SUBMIT_WON historical fact. It does invalidate subsequent current-use eligibility.

## 3. Proposed mechanism: durable shared ordering gate with owner-controlled participants

A common durable ordering service (name provisional: `AppliedBoundaryOrderCoordinator`) provides one linearization domain for a narrowly scoped protection domain. It is not an additional policy authority: I retains authorization/PermissionEpoch authority; D retains ForgetFence/lineage authority; C retains final-submit evidence authority; G retains Applied state authority.

### 3.1 Protection-domain key

The order key must be registry-resolved and bind:

- one I `PolicyDomainRef`;
- one D `CanonicalMemoryAuthorityRef`;
- exact target and complete source/ancestor lineage-set digest;
- one G `ContextId/ContextVersion/DeliveryId/DeliveryAttemptId`;
- the applicable EnvironmentRef and role-labelled ScopeBindingSet;
- the operation's stable `AppliedBoundaryOperationId`.

This Phase 3.6 profile is single-PolicyDomain. Multi-PolicyDomain operations remain BLOCKED/REJECTED. If the exact protected region spans multiple CanonicalMemoryAuthority domains and no atomic cross-domain ordering is available, it must remain UNKNOWN/UNSUPPORTED; do not silently widen the coordinator's transaction scope.

### 3.2 Events in the shared durable order

The coordinator durably sequences, at minimum:

- `I_PERMISSION_EPOCH_ADVANCE` — I-authorized epoch transition, including revocation;
- `D_FORGET_FENCE_INSTALL` — D-authorized fence installation with complete lineage/high-water evidence;
- `FINAL_SUBMIT_GATE_PREPARE` — C requests the exact final-boundary reservation;
- `FINAL_SUBMIT_GATE_SUBMIT_WON` — C supplies authoritative provider/runtime success receipt and actual InferenceRequestId;
- `FINAL_SUBMIT_GATE_ABORTED` — C supplies definitive proof that no provider handoff occurred;
- `FINAL_SUBMIT_GATE_IN_DOUBT` — outcome cannot be authoritatively resolved.

Each event binds the protection-domain key, owner authority reference, stable operation ID, immutable request/evidence digest, prior owner cursor(s), coordinator sequence, schema version and integrity evidence. Owner services validate and sign/authorize their own events; the coordinator must not mint I or D tokens.

### 3.3 Two-phase final-submit gate

1. **PREPARE:** immediately before provider handoff, C submits the exact immutable request digest, runtime/session identity, InferenceRequestId allocation context, FinalRequestBoundaryId, G target/delivery, I authorization tuple/PermissionEpoch and D fence/lineage references. I and D independently validate their current authoritative state. The coordinator durably reserves the order slot and records the owner-validated snapshots.
2. **Reservation held:** competing I revocation/epoch-advance and D fence-install events for this protection domain cannot be declared ordered after the gate without resolving the reservation. They must wait for a terminal outcome or invoke the explicit fail-closed IN_DOUBT path. This reservation is not an ALLOW token and cannot be replayed or reused.
3. **Provider handoff:** C invokes the actual provider/runtime boundary using the exact request bound in PREPARE. A local render, middleware buffer, transport ACK or caller claim is not success evidence.
4. **Terminalization:** C submits the provider-issued success receipt and actual InferenceRequestId to commit `SUBMIT_WON`, or definitive no-handoff evidence to commit `ABORTED`. The terminal decision is immutable and idempotently bound to the same operation and digest.
5. **G acceptance:** G verifies the complete C evidence, H authenticated transport evidence, I receipt/currentness, D fence/lineage and coordinator order proof before appending its own Applied record. Coordinator success alone is not G Applied.

If the process crashes or provider result is ambiguous after PREPARE, recovery queries the provider by stable idempotency/correlation key and replays the same operation/XID-equivalent participant identity. If neither success nor no-handoff can be proven, commit IN_DOUBT; no heuristic success/abort.

### 3.4 Authority transition participation

- I must make PermissionEpoch advancement/revocation effective only at an I-authorized durable event in the common order domain, or provide an equally strong atomic adapter proving the same serialization. A cached epoch read is insufficient.
- D must make ForgetFence installation effective only at a D-authorized durable event in the common order domain, with its complete target/source/ancestor lineage and D-local barrier state bound. D's local fence generation remains D-owned.
- A fence/revocation that wins before PREPARE prevents protected submission.
- A PREPARE reservation that wins first must terminalize as SUBMIT_WON or ABORTED before the competing authority transition is assigned its effective order.
- IN_DOUBT forces fail-closed suppression and explicit recovery; it cannot be converted into a favorable order by timeout or operator guess.

This is a material integration dependency: it may require changes to I and D effective-transition paths and a shared durable ordering service. A's proposal does not assert that such a service currently exists or is deployed.

## 4. Evidence contract and H transport requirements

The owner-issued final evidence bundle should expose opaque, versioned references (exact H wire names remain H-owned):

- `AppliedBoundaryOperationId`;
- `AppliedOrderDomainRef` and `AppliedOrderSequence`;
- `FinalSubmitGateReceiptRef` and terminal outcome;
- I `CommitAuthorizationReceiptRef`, PolicyDomainRef, PermissionEpoch and I sequencer terminal-order proof reference;
- D `ForgetFenceReceiptRef`, ForgetFenceGeneration, complete lineage-set digest and D validation/order proof reference;
- C FinalRequestBoundaryId, actual InferenceRequestId, provider/runtime success receipt reference, complete ManagedRegion digest and canonicalization profile;
- G ContextId/ContextVersion/DeliveryId/DeliveryAttemptId;
- authenticated Adapter/Runtime/RuntimeSession, ActorRef, role-labelled ScopeBindingSet, applicable EnvironmentRef and H CapabilityEpoch;
- immutable evidence digest, issuer/key references, anti-replay identity, schema/profile versions and supersession link.

H transports and integrity-protects these references; H does not mint, validate or reinterpret I/D authority receipts. H receiver sequence and TLS/channel binding remain transport evidence, not the cross-authority ordering authority.

## 5. Failure, recovery and retention rules

| Failure point | Required durable result | Full Applied |
|---|---|---|
| Before PREPARE | No reservation; no submit claim | Forbidden |
| PREPARE rejected by I or D | AUTHORITY_TRANSITION_WON / denied gate with owner evidence | Forbidden |
| PREPARE durable, crash before provider call | Recover same operation; prove no handoff before ABORTED | Forbidden until resolved |
| Provider success, terminal record committed | SUBMIT_WON with provider receipt and exact digest | Candidate only; G still validates |
| Provider definitively rejects/no handoff | ABORTED | Forbidden |
| Provider outcome cannot be proven | IN_DOUBT; suppress and recover | Forbidden |
| I revocation or D fence wins before PREPARE | Transition effective first; reject gate | Forbidden |
| I/D transition races with held PREPARE | Transition waits for terminalization or fail-closed IN_DOUBT | No ambiguous promotion |

The durable journal stores only the minimum non-reconstructive evidence needed for ordering, audit and recovery. It must not retain forgotten plaintext merely to preserve proof. Retention, erasure and access policy remain I/D/Storage authority decisions.

## 6. Required owner decisions (not yet obtained)

### C
- Can every Tier-1 provider integration hold a durable PREPARE reservation before the exact successful handoff and return a provider-authenticated terminal receipt?
- What stable provider idempotency/correlation key permits crash recovery without duplicate submission?
- Which integrations cannot guarantee this and must remain Tier 2/Unknown?

### I
- Will I make revocation/PermissionEpoch effective transitions participate in this shared order domain while retaining I issuance and policy authority?
- What exact CommitAuthorizationReceipt and sequencer proof reference must be consumed at PREPARE and terminalization?
- What are HA, quorum, failover, rollback and IN_DOUBT recovery requirements?

### D
- Will D make ForgetFence installation participate in the same order domain while retaining D generation, lineage and barrier authority?
- How are canonical-authority transaction ordering, producer/work barrier and complete ancestor lineage bound to the common event?
- What is the fail-closed behavior if the ordering service is unavailable?

### H
- Publish the concrete versioned Applied/FinalRequestSubmitted schema with the opaque receipt/order-proof references above, conditional requiredness, unknown-critical-field behavior, canonicalization, replay and compatibility rules.
- Keep Forget Action ACK and Applied evidence/result as separate message families.
- Do not treat H receiver sequence as the C/I/D cross-authority order.

### G
- Confirm the exact minimum evidence and terminal outcome required before G commits Full Applied and the current-use projection.

## 7. Alternatives considered

1. **Wall-clock timestamps / independent local sequence numbers:** rejected; cannot prove cross-authority order.
2. **H receiver ingress order:** rejected; proves only transport arrival, not provider submission or owner-authority transition order.
3. **Preflight I ALLOW + cached D fence read:** rejected; check-then-submit race remains.
4. **Common durable order gate with owner-controlled participants:** proposed for joint decision; requires explicit I/D/C acceptance and production design.
5. **Distributed transaction across I and D participants:** possible alternative only if it supplies the same durable prepare, lock retention, terminal decision, recovery and exact C boundary binding. Must be evaluated against JF-10 prepared-XID/IN_DOUBT constraints; no assumption of implementation.

## 8. Acceptance and stop conditions

This proposal is not normative until C, I and D issue explicit owner decisions against this exact proposal Blob and A records a reconciled decision. H must then publish the corresponding exact schema version and G must accept the evidence mapping.

Until then:
- C-submit/D-fence/PermissionEpoch total order: **OPEN / NOT ESTABLISHED**.
- Cross-authority coordinator: **PROPOSED / NOT IMPLEMENTATION-VERIFIED**.
- Full Applied on ambiguous order: **FORBIDDEN**.
- Applied Contract Frozen: **NO**.
- CGH/I36/H36 conformance: **NOT RUN**.
- Production implementation: **NOT VERIFIED**.
- No branch merge or architecture freeze is authorized.
