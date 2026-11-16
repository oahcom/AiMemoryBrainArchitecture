# Phase 3.6 — B/I/H Identity Trust, Authorization & BMCP Joint Architecture Closure

- Owners: B Domain Model, I Identity/Security/Governance, H BMCP Protocol
- Date: 2026-11-16
- State: **JOINT TECHNICAL BASELINE ACCEPTED; GOVERNANCE BLOCKED; CONSUMER ACCEPTANCE PARTIAL; I36/H36 NOT RUN**
- Normative baseline: BIH36-JD-01..17, preserved without redesign.
- Fact/Claim ADR-001: **ADR-BLOCKED**, independently unchanged.
- This is delegated joint architecture acceptance and evidence reconciliation, not external governance approval, consumer sign-off, production schema freeze, implementation sign-off or test pass.

## 1. Branch-aware source baseline

Owner branches were queried independently; `main` is not treated as the source of truth. Controlling artifacts read:
- A: `reviews/integration/phase-3.6-final-closure-plan.md` (Blob `c3eeec18362d3b0a7756be4e75aa36ea3eed8f23`) and `phase-3.6-closure-tracking.md` (latest read Blob `7d1c6a0d5e946041b5e7cbf3b47e598de55cb93f`).
- B: `02-domain-model/phase-3.6-typed-identity-trust-closure.md` (Blob `0a6b78a842e550b58533b797cdfcd2d954ed6826`), `typed-reference-registry.md` (Blob `af23ca9e019ab067a5f8ff62da902d4a419db3f3`) and `phase-3.6-identity-trust-approval-and-consumer-status.md` (Blob `a9f902f9e8aa1752f5726f690c7568bd4babbe21`).
- I: `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` (Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`) and `phase-3.6-governance-approval-and-consumer-acceptance-register.md` (Blob `11c4bfde5de02a684cc6e5df46d1f9676f5a40a5`).
- H: `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` (Blob `9845c97ac43d7888732afafe12e28850ec02add8`), `phase-3.6-identity-binding-consumer-conformance-status.md` (Blob `8afb914731a34d8ab44331f54f1f39bfd8ec37ce`) and `phase-3.6-h36-live-closure-addendum.md` (Blob `e94d39b9977fca61af50bb697f29116d707b3439`).

A's current closure plan preserves the BIH delegated technical baseline and directs only governance approval, consumer acceptance and I36/H36 execution. A's tracking record confirms G5 blocked, G6 partial/blocked, G7 not run and overall freeze not authorized. Later Owner commits must trigger a fresh read before further closure decisions.

## 2. Typed Identity Model — B authority

All Refs are typed, namespace-qualified selectors, not proof of authentication, registration, authorization or possession of credentials. Canonical serialization carries a type discriminator and authority/issuer namespace. Malformed, ambiguous, duplicate-key and cross-type encodings fail closed. IDs are immutable, never recycled, and resolve only through authoritative registries.

| Type | Uniqueness / semantics | Namespace, lifecycle and resolution |
|---|---|---|
| PrincipalRef | Stable subject identity, unique by validated IssuerRef + trust/security domain + tenant + principal kind + issuer subject. | I-authorized registry; stable across credential rotation; never recycled; resolve only after issuer validation. |
| IssuerRef | Trust authority identity, distinct from key/certificate identity. | I trust-domain namespace; admitted/suspended/compromised/revoked/retired lifecycle; no TOFU or transitive trust. |
| ActorRef | Immutable verifier-produced per-operation attribution binding resolved Principal, issuer, operation/session and validated delegation/acting-for context. | Trusted verifier operation namespace; historical attribution retained; caller cannot mint or reuse as Principal alias. |
| ScopeRef | Stable ownership/applicability/data boundary. | Scope authority namespace; role-tagged bindings distinguish owner, applicability, source, target and evidence/provenance. Hierarchy is not a grant. |
| EnvironmentRef | Execution/deployment/security environment, not Scope or display label. | Environment Registry Authority namespace; exact source/target bridge mapping and lifecycle. |
| ProducerIdentity / ProducerRef | Registered producer workload/application and concrete instance. | I registry; authenticated workload, issuer, instance, lineage and revocation; not a human/agent Actor. |
| AdapterIdentity / AdapterRef | Registered recipient/Adapter application and concrete instance. | I registry and H authenticated session binding; replacement creates a new instance identity, no old-session inheritance. |
| DelegationRef | Immutable grant/chain reference. | I grant namespace; parent chain, parties, action/resource, exact boundaries, audience, purpose, validity, subdelegation and revocation. |
| PermissionEpoch | Opaque monotonic I policy-state token within one explicit policy domain. | I sole logical authority; cross-domain values incomparable; currentness obtained from I. |

AgentRef, RuntimeSessionRef, ResourceRef, CapabilityEpoch and D ForgetFenceGeneration remain distinct types. No implicit cast or substitution.

**Required distinctions:** Principal identifies the subject; credential authenticates a claim about it; Actor records operation attribution. Producer identifies the emitting workload; Actor identifies who/what acted. Scope controls data ownership/applicability; Environment identifies execution boundary. Identity resolution is not authorization. These distinctions are normative.

## 3. Trust chain and I authorization

Trust chain: protected transport/verifier context → validate IssuerRef/key/audience against locally admitted I trust registry → issuer-scoped Principal resolution → authenticated Agent/Producer/Adapter workload and concrete instance resolution → verifier-generated ActorRef → complete DelegationChainRef validation → current PermissionEpoch → operation authorization.

Unknown, suspended, compromised, revoked, expired or unverifiable issuer/key fails closed and invalidates dependent sessions/decisions. No subject-only global lookup, payload-driven registration, TOFU or implicit cross-issuer linking.

I owns trusted issuer admission, Principal resolution policy, workload registration, delegation, grants, authorization, revocation, PermissionEpoch, Scope isolation, Environment bridge policy, retention and Global Forget policy. Operation owners enforce I's decision at their own protected boundary.

Authorization binds:
`(PrincipalRef, ActorRef, IssuerRef, action, ResourceRef, purpose, audience, ownership ScopeRef, applicability ScopeRef set, applicable EnvironmentRef, DelegationChainRef, policy domain, PermissionEpoch, authenticated workload/instance, RuntimeSessionRef)`.
Missing, unresolved, mismatched, stale or indeterminate members mean DENY/PAUSE. Recheck at irreversible commit/disclosure; upstream ALLOW is not transferable.

- Scope hierarchy, shared Agent, project membership, tenant labels or session similarity never grant access. Cross-Scope requires explicit current grant naming exact source/target Scope, action, resource, purpose and audience. Every endpoint and evidence/provenance dereference is separately authorized.
- Cross-Environment is denied by default. Exact registered source/target EnvironmentRefs, bridge relation, action/resource/purpose/provenance/validity and I authorization are required. Environment Registry Authority must be formally designated.
- Global Forget requires authenticated requester/continuity Principal and I authorization over exact operation, target, Scope, purpose, audience and jurisdiction. Unauthorized attempts are denied before target enumeration, fence creation or mutation and are audited. Obligation remains durable if requester is later revoked.
- Offline/stale authorization leases are prohibited in this baseline. A bounded lease requires a separate approved I governance profile.

## 4. Delegation, revocation and PermissionEpoch

Delegation is a signed, issuer-verifiable chain binding grantor, delegate, represented subject, permitted actions/resources, exact Scope/Environment, audience, purpose, validity, parent and subdelegation policy. Effective authority is strict intersection of grantor authority, delegate eligibility and every parent grant. No cycles, amplification, grantor fallback or depth overflow. Subdelegation remains disabled absent an approved profile.

I is sole logical issuer/currentness authority for PermissionEpoch. It is opaque and monotonic per policy domain; cross-domain epochs are incomparable. Relevant issuer/key, Principal, grant/delegation, Scope/Environment bridge, Producer/Adapter and policy changes advance the affected domain. Consumers check currentness at every protected boundary; inability to establish currentness pauses/denies. No cached ALLOW or offline continuation.

Revocation is effective at I's policy-domain sequencer committed epoch. Uncommitted work is denied/cancelled/quarantined if revocation wins before its protected commit/disclosure point. Already-disclosed information cannot be recalled retroactively; it triggers recipient/retention/forget workflows. I PermissionEpoch and D ForgetFence are independent and both checked where required.

## 5. BMCP identity binding — H authority

- **Envelope/requiredness:** versioned envelope carries message ID, nonce, type/operation, audience, RuntimeSessionRef, typed identity selectors, role-tagged Scope bindings, applicable EnvironmentRef, PermissionEpoch and operation-specific delivery/context/forget references. H's versioned Operation Requiredness Registry is keyed by protocol major/message type/operation; sender cannot self-declare applicability.
- **Authentication:** protected verifier/transport context is authoritative for IssuerRef, PrincipalRef, ActorRef, workload/instance, audience and session. AuthenticationContextRef is opaque verifier-internal, never a public Ref or sender field. Credentials/private keys never enter payload.
- **Channel/message integrity:** channel binding is tied to negotiated secure transport, protocol family/major, server identity and fresh RuntimeSessionRef. Message integrity proof binds channel binding, session, message ID/nonce, audience, major, canonicalization profile, digest algorithm and canonical message digest. Integrity alone is not issuer trust or authorization.
- **Payload claims:** Principal/Actor/Producer/Adapter fields are claims/selectors only; mismatch with protected context or registry is rejected/quarantined and audited.
- **ACK:** binds authenticated issuer/principal, Adapter app and concrete instance, Agent/runtime instance, fresh session, verifier-resolved ActorRef, exact Scope roles, applicable EnvironmentRef, exact Delivery/ContextVersion/attempt or ForgetOperation/target, CapabilityEpoch, PermissionEpoch, applicable ForgetFence, action/region/coverage, immutable ACK ID and evidence digest. H verifies protocol binding; G owns Applied semantics; D owns Forget completion; I owns revocation.
- **Ordering/idempotency:** trusted receiver receipt sequence—not Adapter wall-clock—feeds owner sequencers. Same stable ACK namespace+digest is idempotent; same namespace+different digest is conflict. Tombstones cover replay, offline queue, operation retention and revocation/fence horizons; unbounded horizon means indefinite retention.
- **Capability:** capability is registered per Adapter instance and versioned by CapabilityEpoch. Unsupported required capability returns explicit Unsupported/Unknown; no silent fallback or false Applied. Capability changes invalidate/revalidate outstanding deliveries.
- **Reconnect:** fresh authentication → issuer validation → Principal/workload resolution → capability negotiation → current PermissionEpoch → current ForgetFence → stale-state suppression → delivery/ACK journal reconciliation → final-boundary authorization → resume. Old-session ACKs remain historical. Replacement Adapter instance gets new identity/session.
- **Replay/versioning:** nonce/replay window, canonicalization and major-version checks; channel/session/audience mismatch, duplicate keys, malformed refs, unknown critical fields/enums, unsupported requiredness and downgrade fail closed.

## 6. Consumer Contract Mapping

Acceptance requires an explicit Owner-authored statement against exact artifact version/digests, fields, semantics, negative cases and enforcement boundary. A code reference or test specification is not acceptance.

| Consumer | Required contract / enforcement | Evidence state |
|---|---|---|
| C | Principal/Actor/Agent/RuntimeSession, Producer/Adapter, Scope/Environment, epoch/revocation and final-request/disclosure boundary. | **OPEN**; no explicit BIH acceptance located. |
| D | Principal/Actor/Producer, action/resource/Scope/Environment, epoch and separate ForgetFence at canonical mutation/commit. | **DESIGN-ACCEPTED** by D Owner artifact; implementation/tests NOT RUN. |
| E | Producer class/instance, lineage, Actor/Scope, inventory epoch/seal and permit at admission/final publication. | **DESIGN-ACCEPTED**; E36 NOT RUN. |
| F | Identity/Scope filtering before candidate generation; current epoch at final return/cache/rebuild. | **OPEN**. |
| G | Authenticated Adapter/session ACK, ContextVersion/Delivery attempt, Scope/Environment, PermissionEpoch, CapabilityEpoch and ForgetFence at Applied transition/reconnect. | **OPEN**. |
| Storage | Authenticated commit context, Scope, inventory seal, current PermissionEpoch and fence/manifest/dependency at durable visibility. | **DESIGN-ACCEPTED**; deployment/implementation proof NOT RUN. |
| H | Envelope, verifier context, channel binding, requiredness, ACK and reconnect. | **DESIGN-ACCEPTED** at H boundary; H36 NOT RUN. |
| A | Evidence registry and status reconciliation only. | Registrar only; cannot approve for consumers. |

C/F/G must return exact accepted version/digest, field mapping, verifier inputs, Scope/Environment and epoch/revocation behavior, negative cases, failure mode and Owner-authorized acceptance record. D/E/H/Storage design acceptance must not be relabeled runtime acceptance.

## 7. Governance Approval Matrix

All I36-GOV-01..10 remain **GOVERNANCE-BLOCKED**. Required evidence for each: named approver PrincipalRef and authority/delegation, decision ID, exact policy text/hash, scope/jurisdiction, effective version/time, signature/governed record, expiry/review and supersession.

| ID | Decision | Required authority and evidence | State |
|---|---|---|---|
| GOV-01 | Trusted issuer admission/federation, trust domains, key compromise | Named Security Governance approver; issuer/key lifecycle profile | BLOCKED |
| GOV-02 | Principal taxonomy/registration/cross-issuer linking | Identity Governance; namespace/linking policy | BLOCKED |
| GOV-03 | Delegation eligibility, depth, acting-for, subdelegation | Security Governance; signed grant/revocation profile | BLOCKED |
| GOV-04 | Cross-Scope sharing/inheritance/break-glass | Data/Scope Governance; exact source/target/action/resource/purpose/audience | BLOCKED |
| GOV-05 | Cross-Environment bridge/federation | Environment Governance; named Registry Authority and mapping/policy | BLOCKED |
| GOV-06 | PermissionEpoch domains, freshness, lease/staleness and revocation SLA | Security Governance; effective epoch profile/SLA | BLOCKED |
| GOV-07 | Revocation effective point/in-flight semantics | Security Governance plus C/D/E/F/G/H boundary acknowledgements | BLOCKED |
| GOV-08 | Administrative/break-glass | Independent approver; reason, dual control, scope, expiry, audit | BLOCKED |
| GOV-09 | Principal Resolution and cross-issuer subject mapping | Identity Governance; exact resolution/registry policy | BLOCKED |
| GOV-10 | ActorRef/Principal binding | Security/Identity Governance; verifier issuance/attribution policy | BLOCKED |

No formal Environment Registry Authority or complete Producer/Recipient/Backup InventorySealReceipt was evidenced. I must publish ProducerDomainInventoryEpoch, canonical digest, complete member enumeration, authenticated owner/instance IDs, Scope, capabilities, lineage, backup/export/restore map, gaps/exclusions and approved exceptions. Until sealed, completeness is UNKNOWN and Global Forget completion cannot be claimed. The joint team cannot invent approvers or approve on their behalf.

## 8. I36/H36 Architecture Verification — specified, not executed

I36-01..20 and H36-01..18 plus H36-SR additions are existing specifications. These architecture traces define expected behavior, not test results.

| Case | Preconditions / message sequence | Expected rejection and state effect | Evidence required |
|---|---|---|---|
| Forged PrincipalRef | Protected channel resolves P1; payload claims P2. | Reject mismatch before use; no mutation/disclosure; audit. | Verifier context, payload digest, rejection code, audit. |
| Forged ActorRef | Caller submits arbitrary or replayed ActorRef. | Reject caller-minted or operation/session-mismatched attribution; no state change. | Verifier issuance/binding record and denial log. |
| Forged ProducerIdentity | Payload names Q but authenticated workload maps elsewhere/nowhere. | Reject before enqueue/compile/publish; no receipt or visible artifact. | Attestation, registry lookup, admission result, no-publication proof. |
| Unknown Issuer | Issuer absent from admitted registry. | Deny before Principal resolution; no TOFU/auto-registration/session. | Registry version, trust decision, denial. |
| Revoked Issuer | Issuer/key revoked during active sessions/work. | Advance epoch; deny new work, invalidate dependent sessions; pause/cancel uncommitted work. | Revocation receipt, epoch, session invalidation and boundary traces. |
| Expired Delegation | Parent/child grant expired/revoked or chain invalid. | Deny entire chain; no grantor/represented-subject fallback. | Signed chain, validity/parent checks, denial. |
| Stale PermissionEpoch | Request/ACK has older or incomparable epoch. | Deny/pause before protected boundary; no cached ALLOW/commit/disclosure/Applied. | I current epoch and consumer comparison trace. |
| Cross-Scope | No exact current source/target grant. | Deny before candidate/record/evidence/count disclosure; no wildcard/hierarchy inference. | Role-tagged Scope, grant lookup and no-disclosure evidence. |
| Cross-Environment | Bridge absent/stale/mismatched. | Deny cross-environment operation; no label fallback. | Registry authority/mapping and denial. |
| Revocation race | Work staged; revoke commits before final publish/disclosure/ACK. | Revocation wins; private stage stays private; cancel/quarantine. Epoch and fence advance only in their own authorities. | Sequencer order, visibility trace, private-stage proof, receipts. |
| Old-session ACK | Prior RuntimeSession or replaced Adapter ACK arrives after reconnect. | Historical evidence only; no current-state mutation or rollback. | Old/new session IDs, receiver order, idempotency evidence, unchanged state. |
| Reconnect during revocation | Transport drops; revocation commits; old session attempts resume. | Suppress stale state; fresh trust/epoch/fence/capability/journal checks required; no resume until complete. | Ordered reconnect trace and fresh verifier context. |
| Unauthorized Forget | Requester unauthenticated or lacks exact Global Forget grant. | Deny before target enumeration/fence/mutation; audit attempt. | Auth tuple/current policy and proof of no target mutation. |
| Incomplete producer inventory | Producer/recipient/backup missing or unknown recipient found. | Seal withheld/invalidated; completeness UNKNOWN; Global Forget cannot COMPLETE. | Enumeration, owner attestations, digest/seal, exceptions and reconciliation. |

Additional H36 cases: lost ACK retry (same namespace+digest returns original receipt); late ACK (historical only after revocation/fence); duplicate ACK (same digest idempotent, different digest conflict); out-of-order/superseded ACK (owner sequencer rejects rollback); Unsupported Adapter (explicit Unsupported/Unknown, no false Applied); CapabilityEpoch change (revalidate/cancel outstanding delivery); channel-binding mismatch, cross-session/audience replay, nonce reuse, duplicate-key canonicalization, missing requiredness profile, suppressed applicable EnvironmentRef and protocol downgrade (fail closed before state change).

**Execution evidence:** I36-01..20 are SPECIFIED / NOT RUN; I36-T01..T20 ledger has no build/runner/command/log. H36-01..18 and H36-SR additions are SPECIFIED / NOT RUN; no executable environment, fixture, actual output, logs or reviewer evidence. No case is PASS or FAIL.

## 9. Joint acceptance and authority boundaries

B/I/H jointly accept BIH36-JD-01..17 as the same delegated technical baseline. B owns types/namespace/Actor/Scope semantics; I owns trust/policy/authorization/epoch/revocation/retention/Global Forget; H owns wire/protocol/transport/ACK/replay/reconnect. C/D/E/F/G/Storage own their enforcement and final acceptance boundaries. A records evidence and gate states only.

This is not an independent signature by an external approver, governance activation, consumer sign-off, production schema freeze or runtime conformance.

## 10. Remaining decisions and gate disposition

1. I/Security Governance: approve GOV-01..10 with complete evidence; designate Environment Registry Authority.
2. I + all inventory owners: seal Producer/Recipient/Backup inventory and publish permit/revocation serialization contract.
3. C/F/G: provide explicit version-pinned acceptance/rejection and consumer field mappings.
4. D/E/H/Storage: preserve design acceptance and separately provide implementation/conformance evidence.
5. I/H and boundary owners: execute I36/H36 on identified builds with deterministic fixtures, commands, expected/actual outputs, logs, receipts and reviewer sign-off.
6. A: refresh all Owner refs/Blob SHAs after deliveries; update gates only from exact evidence.

| A gate | Disposition |
|---|---|
| G4 BIH Technical Agreement | **CONDITIONAL PASS** — joint acceptance of JD-01..17 |
| G5 BIH Governance Approval | **BLOCKED** — GOV-01..10 not approved |
| G6 BIH Consumer Acceptance | **PARTIAL/BLOCKED** — D/E/H/Storage design accepted; C/F/G open |
| G7 BIH Test Verification | **NOT RUN** — I36/H36 |
| G10 Overall Implementation Readiness | **BLOCKED** |

Fact/Claim ADR-001 remains ADR-BLOCKED. No schema freeze, production readiness, security certification, Global Forget completion or test pass is claimed.
