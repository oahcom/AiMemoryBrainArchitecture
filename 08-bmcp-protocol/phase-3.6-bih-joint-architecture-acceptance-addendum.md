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
