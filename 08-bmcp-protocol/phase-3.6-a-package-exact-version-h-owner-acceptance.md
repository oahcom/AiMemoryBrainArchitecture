# H Owner Addendum — Formal Acceptance of A's Exact Phase 3.6 BIH Decision Package

- Owner: Session H — BMCP Protocol & Adapter Authentication
- Branch: `session-h-bmcp-protocol`
- Decision date: 2026-11-16
- Decision: **ACCEPTED WITH BINDING H-OWNED PROTOCOL BOUNDARIES**
- Exact A package reviewed: `reviews/integration/phase-3.6-identity-trust-joint-architecture.md`
- A package Blob SHA: `a45ae90b318a79bf009d14f4d917611881e9e214`
- A closure plan: `reviews/integration/phase-3.6-final-closure-plan.md`, Blob `c3eeec18362d3b0a7756be4e75aa36ea3eed8f23`
- A tracking register: `reviews/integration/phase-3.6-closure-tracking.md`, Blob `7d1c6a0d5e946041b5e7cbf3b47e598de55cb93f`
- H normative protocol source: `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`, Blob `9845c97ac43d7888732afafe12e28850ec02add8`
- Existing H consumer acceptance: `08-bmcp-protocol/phase-3.6-bih-identity-trust-consumer-acceptance.md`, Blob `ccbac2d30234df9b910565a7326d100d11a6494e`

## 1. Formal H decision

H has reviewed A's exact BIH joint architecture package at Blob `a45ae90b318a79bf009d14f4d917611881e9e214`, together with A's closure plan/tracking versions above and H's own normative protocol and consumer-acceptance artifacts.

**H ACCEPTS A's exact Phase 3.6 BIH decision package for the H-owned BMCP envelope, protected authentication binding, channel/message integrity binding, ACK transport/evidence binding, capability negotiation and reconnect protocol responsibilities, subject to the binding clarifications in this addendum.**

No item is rejected at the architecture-contract level. The clarifications below delimit H's acceptance; they are not silent changes to A's package and do not transfer I/B/C/D/G authority to H.

This is a delegated H Owner technical decision. It is not an independent human signature, external governance approval, production schema freeze, implementation approval or runtime conformance result.

## 2. H acceptance by decision area

| A package area | H disposition | H-owned acceptance boundary |
|---|---|---|
| Distinct typed Ref identities and namespace dimensions | ACCEPT | Preserve typed discriminators and authority/issuer namespaces in BMCP encoding; H does not redefine B types |
| Protected verifier context outside untrusted payload | ACCEPT | Authenticated issuer, Principal, Actor, workload/instance, audience and session come from protected verifier context; payload mirrors remain claims |
| Issuer/Principal/workload resolution | ACCEPT | H binds verifier context and registered Adapter instance; I remains sole trust/Principal/authorization authority |
| ActorRef operation attribution | ACCEPT | H carries/binds verifier-resolved immutable operation/session ActorRef; caller-minted ActorRef is rejected; B/I retain semantics/validation |
| Scope and Environment binding | ACCEPT | Preserve explicit role-tagged ScopeRef set and applicable EnvironmentRef; no label fallback, wildcard or inferred grant; I authorizes |
| PermissionEpoch and authorization tuple | ACCEPT | Carry opaque I-issued PermissionEpoch unchanged and bind it to the exact operation; H does not mint, compare or authorize it |
| D ForgetFence separation | ACCEPT | Carry ForgetFence independently from PermissionEpoch; H never compares, converts or substitutes either token |
| CommitAuthorizationReceipt / protected owner gate | ACCEPT | H may transport protected receipt evidence only; H cannot mint, consume, broaden, reuse or reinterpret it; I and operation owner define/execute ordering |
| ACK binding and replay | ACCEPT | Bind authenticated Adapter/instance/session, Actor, Scope, operation/delivery identity, CapabilityEpoch, PermissionEpoch, applicable D fence, action/coverage, immutable ACK ID and digest |
| Reconnect order | ACCEPT | Fresh authentication, issuer/principal/workload validation, capability negotiation, current PermissionEpoch, current D fence, suppression, journal reconciliation, final-boundary authorization, then resume |
| Fail-closed/versioning | ACCEPT | Unknown critical fields, malformed refs, duplicate keys, unsupported requiredness/major version, downgrade and indeterminate ordering fail closed |

## 3. Binding clarifications and limits

1. **No wire-schema freeze.** A's package is an accepted logical architecture and field/behavior contract. H still owns exact BMCP field spelling, serialization/canonicalization, requiredness registry, protocol major/minor negotiation and cryptographic profile. Candidate logical field names do not become frozen wire names by this acceptance.
2. **Protected authentication is not payload signing alone.** Message integrity/channel binding proves integrity and channel/session binding only; it does not establish issuer trust, Principal registration, Actor validity or authorization.
3. **No authorization in H.** H does not make ALLOW decisions. It transports authenticated evidence and enforces protocol rejection; I decides trust, PermissionEpoch, authorization and revocation.
4. **No owner-state authority in H.** H receiver sequence/timestamp is transport evidence only. D decides ForgetFence/barrier, G decides ContextVersion/Delivery/Applied, Storage decides VisibilityPointer/PublicationReceipt, and I decides PermissionEpoch/revocation order.
5. **Currentness at use boundary.** H's successful receipt or message validation cannot be reused as a blanket authorization. Each owning consumer validates current policy/fence/state at its own protected boundary.
6. **JF-10 v2 is separate.** This acceptance does not accept Storage's prepared-XID implementation or close JF-10. H has no authority to accept D's fence semantics, Storage's transaction realization or I's coordinator implementation. H's transport duties are limited to preserving/binding the exact operation and receipt metadata.
7. **Governance remains external.** I36-GOV-01..10, including PermissionEpoch profile/freshness and revocation SLA, remain subject to named authorized governance approval. H's acceptance does not activate them.

## 4. H-specific remaining obligations

- Maintain versioned Operation Requiredness Registry keyed by protocol major/message type/operation; sender cannot self-declare applicability.
- Bind message integrity to negotiated protected channel, protocol family/major, server identity, fresh RuntimeSessionRef, message ID/nonce, audience, canonicalization profile, digest algorithm and canonical message digest.
- Bind ACK evidence to authenticated instance/session and exact operation/version/attempt; same ID+same digest is idempotent; same ID+different digest is conflict.
- Keep old-session, post-revocation, superseded or ambiguously ordered ACKs historical only; never mutate newer owner state.
- Negotiate per-instance CapabilityEpoch; unsupported required capability returns explicit Unsupported/Unknown, never silent fallback or false Applied.
- Reconnect only after fresh auth, current I epoch, current D fence, stale-state suppression and G journal reconciliation.
- Retain non-sensitive evidence sufficient to correlate protocol version, Adapter instance/tier, CapabilityEpoch, issuer/key fixture, authenticated principal class, policy domain/epoch, fence, expected/actual result and reviewer.

## 5. Verification and gate state

- H design acceptance of A's exact package: **ACCEPTED**.
- H wire/schema freeze: **NOT APPROVED**.
- H implementation: **NOT VERIFIED**.
- H36-01..18 and H36-SR additions: **SPECIFIED / NOT RUN**.
- External I governance approval: **GOVERNANCE-BLOCKED**.
- C/F/G acceptance: remains with their respective Owners.
- G6 overall consumer acceptance: **NOT CLOSED**.
- G7 H36/I36 verification: **NOT RUN**.
- Fact/Claim ADR-001: **ADR-BLOCKED**, unchanged.
- JF-10: **P0 OPEN**, unchanged by this H decision.

## 6. A integration instruction

A may record H's exact-version design acceptance using the A package Blob SHA above and this H addendum's Blob SHA/commit. A must not infer runtime conformance, schema freeze, I governance approval or acceptance by any other consumer.
