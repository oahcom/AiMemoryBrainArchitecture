# I Owner Confirmation — PermissionEpoch and Protected Authorization Conditions (Phase 3.6)

- Owner: Session I — Identity, Security & Governance
- Branch: `session-i-security-governance-2026-11-16`
- Date: 2026-11-16
- Decision class: **FORMAL I OWNER TECHNICAL CONTRACT CONFIRMATION**
- Status: **CONFIRMED AS NORMATIVE I TECHNICAL BASELINE; EXTERNAL GOVERNANCE PROFILE APPROVAL STILL BLOCKED**
- Controlling BIH decision set: `BIH36-JD-10..13`
- Controlling I policy artifact: `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md`, Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`
- A integration package reviewed: `reviews/integration/phase-3.6-identity-trust-joint-architecture.md`, Blob `a45ae90b318a79bf009d14f4d917611881e9e214`
- Related I JF-10 v2 decision: `09-security-governance/phase-3.6.2-jf10-v2-i-owner-disposition.md`, Blob `b7b0287cde3922434a560fca90051cc5b418d987`

## 1. Formal I confirmation

I formally confirms the following as the normative I-owned technical contract for Phase 3.6:

**PermissionEpoch is an opaque, monotonically advancing authorization-state token issued and controlled solely by I within one explicit I-registered policy domain. Every protected consumer must establish authoritative currentness and evaluate the complete authorization tuple at its own enforcement boundary. A stale, gapped, unknown, incomparable, unverifiable or indeterminate epoch/decision means DENY or PAUSE; it never means ALLOW.**

This confirms the I-owned technical policy decision in BIH36-JD-10..13 and resolves any ambiguity about whether PermissionEpoch is merely an optional wire hint: it is a mandatory currentness input whenever the operation is protected by I authorization policy. H transports it unchanged; H does not validate policy currentness or authorize.

This confirmation is an I Owner technical decision under delegated project authority. It is not a signed external governance approval, policy activation for a jurisdiction, production epoch-service deployment, or runtime conformance claim.

## 2. PermissionEpoch authority and namespace

1. I is the sole logical issuer and authority for PermissionEpoch and the authoritative policy-domain epoch stream.
2. Each epoch belongs to exactly one explicit, I-registered `PolicyDomainRef` / policy_domain_id. Domain identity is registry-assigned and deterministic; consumers cannot derive it from labels or concatenate arbitrary fields.
3. Epochs are opaque and monotonically advancing within that domain. Consumers must not parse token internals to infer ordering; ordering/currentness comes from the authoritative I sequencer/epoch service.
4. Epochs from different policy domains are incomparable. A multi-domain operation requires current proof for every affected domain and an I-approved atomic all-or-none coordinator. Without that capability, deny/pause; never partially authorize.
5. PermissionEpoch is not PrincipalRef, credential version, session generation, CapabilityEpoch, ContextVersion, ForgetFenceGeneration, Storage commit cursor or any other counter/token.
6. I retains the authoritative mapping of policy domain, epoch, policy version/digest, commit sequence, effective point, invalidation reason and affected selectors/obligations, with integrity-protected audit history.

## 3. Epoch advancement conditions

I must advance every affected policy domain when a committed change can alter whether a protected operation is permitted, including:
- issuer/key trust, suspension, compromise, revocation, credential eligibility or audience/domain constraints;
- Principal registration, status, linking, retirement or security-relevant binding;
- delegation creation, narrowing, parent-chain change, expiry, revocation or sub-delegation profile;
- grant, role, action, resource, purpose, audience, obligation or administrative/break-glass policy;
- Scope membership/ownership/status, cross-Scope grant or inheritance policy;
- Environment registration/status, cross-Environment bridge/federation or trust mapping;
- Producer, Agent, Adapter, recipient or workload-instance registration, authorization, replacement or revocation;
- policy rule/version, data classification, retention or other authorization-relevant constraint;
- emergency security response or detected epoch-stream continuity/integrity failure.

A true no-op metadata change may avoid epoch advancement only when I can demonstrate that authorization outcomes cannot change; the change remains auditable. Multi-domain changes advance each affected domain and require all-domain currentness.

## 4. Complete protected authorization conditions

For every protected operation, I confirms the authorization decision binds and evaluates the complete tuple:

`(IssuerRef, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ownership ScopeRef, applicability ScopeRef set, applicable EnvironmentRef, DelegationChainRef, PolicyDomainRef, PermissionEpoch, authenticated workload/instance, RuntimeSessionRef)`

The following conditions are mandatory:

### 4.1 Authentication and identity
- Protected transport/verifier context is the source of authenticated issuer, Principal, workload/instance, audience and session. Payload identity fields are claims only.
- Issuer/key trust, credential type, signature/attestation, audience, validity window, revocation and trust-domain constraints must validate.
- Principal resolution is issuer-scoped and unambiguous; no payload-driven auto-registration, subject-only global lookup or trust-on-first-use.
- ActorRef is verifier-produced, immutable and bound to the exact operation/session and validated delegation/acting-for context. Caller-minted or mismatched ActorRef is rejected.
- Producer/Agent/Adapter/recipient identities are distinct registered workload identities and must match protected verifier bindings.

### 4.2 Delegation
- Every delegation link must be valid, current, issuer-verifiable, within time bounds, non-revoked and bound to exact parties, actions, resources, Scope/Environment, audience and purpose.
- Effective authority is the strict intersection of grantor authority, delegate eligibility and every parent grant. No amplification, cycles, grantor fallback or represented-Principal fallback.
- Sub-delegation remains disabled unless a separately approved profile explicitly enables it.

### 4.3 Scope and Environment
- Ownership Scope and applicability Scope are evaluated independently. Applicability is not a grant.
- Cross-Scope access requires an explicit current grant naming exact source/target ScopeRefs, action, resource, purpose, audience and expiry.
- Cross-Environment access is denied by default; an exact source/target EnvironmentRef bridge, relation, operation/resource, provenance, validity and explicit I authorization are required.
- No hierarchy, tenant label, project membership, shared Agent, session similarity, wildcard or display label implies permission.
- Every endpoint and Evidence/Provenance dereference is separately authorized.

### 4.4 Action/resource/purpose/audience and obligations
- The action and ResourceRef must be registered/recognized and authorized for this Principal/Actor/delegation.
- Purpose and audience are explicit, policy-checked and bound to the operation; audience mismatch denies.
- Obligations, retention/classification constraints, expiry, jurisdiction and break-glass requirements are evaluated before ALLOW.
- Missing, malformed, unresolved, mismatched or unknown security-critical inputs yield DENY/INDETERMINATE, never permissive defaults.

### 4.5 Final-boundary currentness and commit authorization
- Before protected execution and again at irreversible commit/disclosure for high-risk actions, the owner obtains an online authoritative current decision/PermissionEpoch from I.
- A cache TTL, event delivery, local high-water mark or previously observed ALLOW is not proof of currentness.
- Offline authorization leases, stale-epoch grace and cached ALLOW without online currentness proof are prohibited in this Phase 3.6 profile.
- A protected irreversible operation uses a single-use I `CommitAuthorizationReceipt` bound to policy domain, PermissionEpoch, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef, DelegationChainRef, operation ID, immutable payload/request digest, owner boundary and I decision.
- The exact owner final gate must submit that receipt into the same I policy-domain linearizable sequencer that orders revocation. A detached preflight ALLOW is insufficient.
- If operation commit is sequenced first, I records COMMIT_WON for that exact operation; if revocation is sequenced first, receipt is rejected and outcome is REVOCATION_WON; if order/decision cannot be established, UNKNOWN/IN_DOUBT remains blocked and no success is reported.
- For JF-10 v2, I's COMMIT decision binds the prepared Storage participant/XID and exact owner boundary. It is not reader-visible publication; Storage must commit and read back PublicationReceipt.

## 5. Revocation and in-flight semantics

1. Revocation becomes effective at the I policy-domain sequencer's durable committed epoch-advance point, not at request arrival, wall-clock timestamp, cache invalidation delivery or local consumer receipt.
2. Every affected domain emits ordered invalidation events. Consumers track the highest contiguous applied epoch; gaps, out-of-order events, unavailable subscribers or offline state require authoritative online revalidation.
3. If revocation wins before the operation's protected commit/disclosure linearization point, the operation must be denied/cancelled/quarantined. No stale receipt, cached ALLOW or offline lease may override.
4. If the exact operation's owner-final-gate COMMIT is durably sequenced first, a later revocation cannot retroactively rewrite that exact terminal decision. This is not permission for later operations or a reusable grace period; all later operations must validate the new epoch.
5. An unresolved earlier JF-10 prepared participant is UNKNOWN/IN_DOUBT; a conflicting revocation must not pass it by assuming abort. Recover the durable coordinator decision or remain blocked.
6. Already-disclosed information cannot be recalled. I records residual disclosure and initiates applicable recipient/retention/forget reconciliation.
7. PermissionEpoch and D ForgetFenceGeneration are independent. Where both apply, both are checked at their respective final boundaries; one never substitutes for the other.

## 6. Required consumer behavior

| Consumer | Mandatory I contract consumption |
|---|---|
| H / BMCP | Carry PermissionEpoch and authenticated operation tuple unchanged; bind it to message/ACK/session; reject missing/stale/unknown evidence according to protocol; never decide authorization |
| C | Validate final-request identity, purpose/audience and authorization evidence at submission/disclosure boundary |
| D | Consume current I authorization independently of D ForgetFence; retain separate authority and ordering |
| E | Validate producer/Actor/Scope/Environment and current I epoch at admission and final publication |
| F | Filter before candidate generation and revalidate current epoch at final return/cache/rebuild |
| G | Validate recipient/action/Scope/Environment and current epoch at delivery/apply/reconnect; keep Applied semantics G-owned |
| Storage | Validate exact current authorization/receipt at final visibility gate and persist I sequencer outcome with participant proof |
| A | Record exact evidence and gate status only; no policy or consumer approval by inference |

Upstream ALLOW is not a transferable blanket capability. Each owner enforces the I contract at its own protected boundary.

## 7. Governance and implementation distinction

The technical semantics above are confirmed by I Owner. The following remain **GOVERNANCE-BLOCKED** until named authorized approvers issue exact versioned approvals: issuer admission/federation; Principal taxonomy and cross-issuer linking; delegation eligibility/depth/subdelegation; cross-Scope grants; cross-Environment bridge; PermissionEpoch service profile/freshness/revocation SLA; revocation effective-point/in-flight profile; administrative/break-glass; ActorRef attribution policy; registry/Inventory Seal authority.

Required governance evidence remains: approver PrincipalRef and authority/delegation, decision ID, exact policy text/hash, scope/jurisdiction, effective version/time, signature/governed record, expiry/review and supersession conditions. No approver is invented and no governance approval is claimed.

Implementation/conformance also remains unverified: epoch service/coordinator deployment, linearizable lookup, durable sequencer, propagation and cache invalidation, failure/recovery behavior, and I36/H36/JF10 conformance. I36 and H36 cases remain SPECIFIED / NOT RUN until executable build, fixtures, logs and independent review are attached.

## 8. Explicit disposition

- PermissionEpoch authority/domain/monotonicity/currentness: **I OWNER CONFIRMED**.
- Epoch advancement and invalidation semantics: **I OWNER CONFIRMED**.
- Complete authorization tuple and default-deny conditions: **I OWNER CONFIRMED**.
- No offline lease/stale-epoch grace in Phase 3.6: **I OWNER CONFIRMED**.
- Revocation effective point and protected-operation race semantics: **I OWNER CONFIRMED**.
- JF-10 v2 prepared-participant binding: **I OWNER CONFIRMED** per the cited I JF-10 disposition.
- External governance activation/approval: **BLOCKED**.
- Production implementation and runtime conformance: **NOT VERIFIED / NOT RUN**.
- Fact/Claim ADR-001: **ADR-BLOCKED**, unchanged.

This addendum is the formal I technical confirmation requested by the A closure plan. It does not sign external governance approvals, select a production implementation, or claim any test pass.
