# H — Phase 3.6 BIH Identity-Trust Consumer Acceptance

- Owner: Session H — BMCP Protocol & Adapter Authentication
- Branch: `session-h-bmcp-protocol`
- Status: **DELEGATED DESIGN-LEVEL CONSUMER ACCEPTANCE RECORDED; RUNTIME CONFORMANCE NOT VERIFIED**
- Scope: H's consumption of BIH identity, authorization and revocation semantics at BMCP authentication, protected-message, ACK and reconnect boundaries.
- This record is a delegated technical owner-side acceptance only. It is not an independent human signature, external I governance approval, global BMCP schema freeze, or runtime/test certification.

## 1. Exact source baseline

| Source | Branch | Artifact | Blob SHA |
|---|---|---|---|
| B | `session-b-domain-model-phase3` | `02-domain-model/phase-3.6-typed-identity-trust-closure.md` | `0a6b78a842e550b58533b797cdfcd2d954ed6826` |
| I | `session-i-security-governance-2026-11-16` | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | `0cbf6bb7480db873790c454817593a9b1c5548ba` |
| I | same | `09-security-governance/phase-3.6-principal-trust-chain-authorization-revocation.md` | `74643a2f374179128d506c3b7e1d22da77119600` |
| H | `session-h-bmcp-protocol` | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248` |
| H | same | `08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md` | `8afb914731a34d8ab44331f54f1f39bfd8ec37ce` |

The acceptance applies to BIH36-JD-01..17 as recorded in the exact B/I/H source baseline above. It does not amend those decisions.

## 2. H acceptance

H accepts the BIH identity-trust semantics for the H-owned BMCP boundary:

1. Protected transport/verifier context, never an untrusted payload mirror, is authoritative for issuer, Principal, workload/Adapter instance, audience and RuntimeSession.
2. PrincipalRef, ActorRef, AgentRef, AdapterRef, ProducerRef, ScopeRef, EnvironmentRef and RuntimeSessionRef remain distinct typed references with their authority/namespace dimensions preserved.
3. ActorRef is verifier-produced, immutable and operation-specific attribution; it is not a credential, grant or bearer capability.
4. Agent, Adapter and Producer identities are distinct registered workload identities. A payload claim cannot establish registration or authentication.
5. Scope bindings are explicit and role-tagged; ScopeRef is not permission. Cross-Scope access requires an explicit current grant. EnvironmentRef is registry-backed; cross-Environment access is denied absent an exact approved bridge/grant.
6. The protected operation binding carries the applicable PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef, DelegationChainRef, policy domain, PermissionEpoch, operation identity and owner boundary.
7. I is the sole logical authority for PermissionEpoch. H transports the opaque epoch unchanged and does not compare it with D ForgetFenceGeneration, G ContextVersion, H AdapterCapabilityEpoch or any other cursor.
8. Revocation, stale/gapped/unknown epoch, unknown issuer, revoked credential, invalid delegation, forged identity, malformed required field, unsupported profile or ambiguous outcome fails closed.
9. A protected irreversible operation's single-use CommitAuthorizationReceipt is bound to the exact operation ID/digest and owner boundary. H may transport authenticated evidence but cannot mint, broaden, reuse or reinterpret the receipt; the owning final commit/disclosure gate must submit it to the I per-domain ordering protocol.
10. H's message integrity and channel/session binding prove transport/message authenticity only; they do not independently prove I authorization, D ForgetFence completion or Storage visibility.
11. ACKs are bound to authenticated Adapter identity and instance, Agent/runtime, fresh RuntimeSessionRef, ActorRef, operation/delivery/forget identity, exact Scope roles, CapabilityEpoch, PermissionEpoch, applicable ForgetFence, evidence digest and immutable ACK ID.
12. Same ACK identity + same digest is idempotent; same identity + different digest is a conflict. Receiver sequence/time is evidence metadata only; D/G/I order authoritative state on their own owner sequencers.
13. Reconnect reauthenticates and revalidates issuer/workload/capability/PermissionEpoch/ForgetFence, suppresses stale state, reconciles journals and only then resumes.
14. Unknown, malformed or unsupported security-critical input never triggers downgrade, payload fallback or inferred success.

## 3. Field-by-field consumer acceptance

| Field / behavior | H accepted semantics | H enforcement / protocol responsibility |
|---|---|---|
| PrincipalRef | I-resolved authenticated subject, bound outside payload | Protected verifier context and claim-mismatch rejection |
| ActorRef | B typed, I-validated, verifier-produced per-operation attribution | H binds to operation/session; caller-minted values rejected |
| ScopeRef | B typed role-tagged scope binding; not a grant | Preserve exact roles; missing/unknown required scope rejects |
| EnvironmentRef | Exact registry-backed environment identity | Preserve when required; no sender suppression or label fallback |
| Producer/Adapter Identity | Distinct registered workload identities, authenticated through protected verifier context | Bind workload/instance and reject payload-only or mismatched claims |
| Authenticated Transport Binding | Protected channel + fresh RuntimeSession + message integrity/canonical digest | Enforce channel/session/audience/nonce/replay binding |
| PermissionEpoch Validation | Opaque I policy-domain token; online currentness proof at protected boundary | Carry unchanged; stale/gapped/unknown/unverifiable blocks |
| Revocation | I sequencer authority; D/G own their respective state ordering | Reauthenticate/revalidate; no local timestamp or H ingress sequence overrides owner order |
| Forged Payload Identity Rejection | Payload identity is a claim only | Reject/quarantine/audit mismatch against protected verifier context |
| Unknown / Unsupported Handling | Fail closed; no downgrade or inferred success | Reject or quarantine before protected content/state transition |

## 4. ACK and reconnect owner boundaries

H accepts transport and evidence-binding obligations, but does not assume downstream semantic authority:
- D alone decides ForgetOperation/ForgetFence and whether a Forget ACK satisfies its barrier.
- G alone decides ContextVersion/Delivery/Applied state.
- I alone decides Principal/Issuer trust, PermissionEpoch and revocation.
- Storage alone decides durable VisibilityPointer/PublicationReceipt visibility.
- H receiver sequence and receipt timestamp are transport evidence only, never substitutes for D/G/I sequencer positions.

A late ACK may be retained as historical evidence but cannot mutate an owner state after that owner's revocation/fence/epoch boundary. Unknown ordering is not success.

## 5. Conformance and governance status

- H36-01..18 and H36-SR additions: **SPECIFIED / NOT RUN**.
- I36 governance approvals I36-GOV-01..10: **GOVERNANCE-BLOCKED**.
- H runtime implementation and conformance: **NOT VERIFIED**.
- C/D/E/F/G/Storage consumer acceptance: remains each Owner's responsibility; this H acceptance does not sign for them.
- JF-10 cross-authority owner-gate protocol: **P0 OPEN**; H does not approve the current split Phase-B/Phase-C candidate as conformant to I36-SR-02.
- Fact/Claim ADR-001: **ADR-BLOCKED**, independent and unchanged.

## 6. Final disposition

H records **design-level consumer acceptance** of BIH36-JD-01..17 for its BMCP authentication, protected-message, ACK and reconnect boundary. This closes only H's owner-side design acceptance evidence gap. It does not close G6 as a whole, H36 execution, external governance, production schema freeze, JF-10, or Phase 3.6 final acceptance.


## 7. 2026-11-19 — exact current H source-pin reaffirmation

The H protocol-binding source pin in §1 is refreshed to the current H Owner branch readback:
- Current protected-operation binding Blob: e7ca5ce4ece5d8fd77fe0760e49a85afa0133248.
- Current H identity-binding conformance-status Blob: 8afb914731a34d8ab44331f54f1f39bfd8ec37ce.
- The prior protected-operation binding Blob 9845c97ac43d7888732afafe12e28850ec02add8 was fetched directly and compared with the current file. All 257 prior lines remain in the current 751-line file; no prior line was removed. The current file adds Phase 3.6.3 Applied wire-profile and Phase 3.6.4 COC successor-candidate material.

**H reaffirms the existing delegated design-level acceptance of BIH36-JD-01..17 only.** The added Applied/COC material is outside this BIH identity-consumer acceptance scope. This pin refresh does not accept or freeze CGH-APPLIED-1.1, does not resolve the eight-family G8 mapping gap, and does not transfer C/G/D/I/B approval.

The existing ceilings remain unchanged:
- H36-01..18 and H36-SR: SPECIFIED / NOT RUN.
- I36-GOV-01..10: GOVERNANCE-BLOCKED.
- H runtime implementation/conformance: NOT VERIFIED.
- Applied Contract Frozen: NO.
- Fact/Claim ADR-001: ADR-BLOCKED.

A may use this refreshed H artifact Blob as current H Owner evidence for the BIH identity-consumer acceptance record. It is not an independent human signature or production schema certification.
