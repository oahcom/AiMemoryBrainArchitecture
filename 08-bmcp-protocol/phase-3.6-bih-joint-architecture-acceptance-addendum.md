# H Owner Addendum — Phase 3.6 BIH Joint Architecture Acceptance

- Branch: `session-h-bmcp-protocol`
- Controlling artifact: `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` (Blob `9845c97ac43d7888732afafe12e28850ec02add8`)
- Status: **H protocol binding jointly accepted; global BMCP schema freeze NOT CLAIMED; consumer acceptance partial; H36 NOT RUN**
- Joint report: `reviews/integration/phase-3.6-identity-trust-joint-architecture.md` on A branch.

H jointly accepts BIH36-JD-01..17 as the shared delegated baseline. H retains authority over envelope, field encoding, versioning, protected transport integration, Operation Requiredness Registry, ACK wire binding, replay, capability negotiation and reconnect ordering.

Protected verifier/transport context—not payload claims—determines IssuerRef, PrincipalRef, ActorRef, authenticated workload/instance, audience and RuntimeSessionRef. AuthenticationContextRef remains verifier-internal and is never a public Ref or sender field. Channel binding and message integrity are required but do not establish I trust or authorization.

ACK binds authenticated issuer/principal, Adapter application/instance, Agent/runtime instance, fresh session, ActorRef, exact Scope roles, applicable EnvironmentRef, exact Delivery/ContextVersion/attempt or ForgetOperation/target, CapabilityEpoch, PermissionEpoch, applicable ForgetFence, action/region/coverage, immutable ACK ID and evidence digest. H verifies protocol binding; G owns Applied semantics; D owns Forget completion; I owns revocation.

ACK uses trusted receiver ordering and stable idempotency namespace. Same key+digest is idempotent; same key+different digest is conflict. Late, stale, superseded or old-session ACKs are historical only. Reconnect performs fresh authentication, issuer/workload resolution, capability negotiation, current PermissionEpoch and ForgetFence checks, stale-state suppression, journal reconciliation and final-boundary authorization before resume. Unknown requiredness, missing applicable fields, malformed refs, duplicate canonical keys, unsupported critical fields/enums, replay, channel/session/audience mismatch and major-version downgrade fail closed. Unsupported Adapter/capability cannot produce false delivery or Applied success.

D/E/H/Storage design acceptance is recorded; C/F/G remain OPEN. H does not sign for other consumers. H36-01..18 and mandatory H36-SR additions are SPECIFIED / NOT RUN; no executable environment, command, fixture, actual result, logs or reviewer evidence is supplied. This is not global BMCP schema freeze, runtime conformance, security certification or independent governance approval. Fact/Claim ADR-001 remains ADR-BLOCKED.

H follow-through: maintain versioned Operation Requiredness Registry; implement/test channel binding, nonce/replay, canonicalization, ACK idempotency and receiver ordering; execute H36/H36-SR including ACK/revocation races, capability downgrade and Adapter replacement reconnect; obtain C/F/G acceptance; do not claim schema freeze until the versioned wire package and required approvals are pinned.


## Phase 3.6.2 — H decision on the pinned C/G/H Applied Contract package

- Reviewed A package: `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`
- Exact package Blob SHA: `61d961c32138fd875069e8cbac4696bb031447c0`
- H disposition: **APPROVE WITH ENUMERATED EXCEPTIONS — H-owned protocol binding only**.

H accepts the package's separation of Delivery receipt, Materialization, C Final Request Submitted evidence, G Applied, and Runtime Execution Started; the authenticated Adapter/Agent/runtime/session binding; independent PermissionEpoch, ForgetFenceGeneration and CapabilityEpoch namespaces; target/action-bound ACK semantics; and the rule that old-session, stale, replayed or late ACKs cannot rebind or roll back current state.

H exceptions and limits:

1. Package §§4–5 are accepted as a semantic mapping/request, **not as a frozen wire schema**. Exact schema IDs, field names, canonical encoding, requiredness profiles, signature/MAC and key lifecycle, nonce/replay profile, durable journal, ACK enum encoding, receiver ordering and capability negotiation remain H-owned implementation artifacts. The current H binding file explicitly describes logical candidate names, not frozen serialization.
2. H transports and verifies C submission evidence but does not create or certify the final immutable provider request, successful submit boundary or complete managed-region digest. C owns those facts.
3. H does not decide the Full Applied predicate, append G Applied, or determine current-use eligibility. G owns Applied state; C owns submission evidence.
4. H does not issue I authorization or PermissionEpoch, nor D ForgetFence/lineage authority. Missing, stale, incomparable or unverified authority remains deny/Unknown and cannot be repaired by an H ACK.
5. H36 and the added ACK/revocation/reconnect race cases remain **SPECIFIED / NOT RUN**. This decision is not implementation verification, security certification, global BMCP schema freeze or independent governance approval.

**Decision consequence:** H has now recorded an explicit decision against the exact A package Blob SHA above, with enumerated H-owned exceptions. This does not close the package: I authorization and D fence predicates still require their owner confirmations, and B's semantic mapping confirmation is recorded separately. C/G/H semantic acceptance is now recorded with exceptions; **Applied Contract Frozen remains NO** until the versioned H wire package and I/D authority predicates meet the A closure criteria.
