---
document_metadata:
  domain: memory-compiler
  role: design-specification
  steward: USER-PRINCIPAL-DELEGATED
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Restored byte-for-byte from Owner source branch; Owner acceptance remains pending."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Canonical
    canonical_scope: "E-domain Memory Compiler record phase-3.6-bih-identity-consumer-acceptance.md; canonical placement pending Owner acceptance."
    canonical_scope_id: "memory-compiler/e-phase-3-6-bih-identity-consumer-acceptance"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-bih-identity-consumer-acceptance
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# Phase 3.6 — BIH Identity Trust Consumer Acceptance (DE-S Owner-Side)

- Status: **DESIGN-LEVEL ACCEPTANCE RECORDED; RUNTIME CONFORMANCE NOT VERIFIED**
- Authority boundary: this record accepts the B/H typed-identity and authenticated-transport semantics for the named DE-S consumer boundary. It does not approve I governance policy, alter I's consumer register, or claim implementation/test completion.
- B source: `02-domain-model/phase-3.6-typed-identity-trust-closure.md`, Blob `0a6b78a842e550b58533b797cdfcd2d954ed6826`, branch `session-b-domain-model-phase3`.
- H source: `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`, Blob `9845c97ac43d7888732afafe12e28850ec02add8`, branch `session-h-bmcp-protocol`.
- I source: `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md`, Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`; I addendum Blob `1f5d2e4aba7afa75c0696f3c8f025b0cb903e0ad`.
- Joint technical decisions: BIH36-JD-01..17. I governance approvals remain GOVERNANCE-BLOCKED; I's own register still lists this consumer as OPEN until the Owner's acceptance and evidence are recorded through the I process.

## 1. Explicit design acceptance

The DE-S consumer accepts the following semantic rules for its boundary:

1. Typed references retain their discriminator, issuer/authority namespace and security-domain dimensions. No conversion among PrincipalRef, ActorRef, AgentRef, AdapterRef, ProducerRef, ScopeRef or EnvironmentRef is permitted.
2. A payload-supplied identity is an untrusted claim/selector. Authentication comes from H's protected verifier/transport context; I resolves issuer, Principal and registered workload bindings. A caller-created ActorRef is never authentication.
3. ActorRef is immutable, verifier-produced, operation-specific attribution. It is not a credential, grant, reusable Principal alias or bearer token.
4. Scope bindings are explicit, role-tagged and resolved against authoritative registries. ScopeRef does not grant permission. Cross-Scope access requires an explicit current grant. Cross-Environment access is denied by default; no label, coordinate, tenant or project similarity fallback is allowed.
5. Every protected operation binds the full applicable authorization tuple: PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ownership/applicability Scope bindings, applicable EnvironmentRef, DelegationChainRef, policy domain and PermissionEpoch, plus authenticated workload/session context and the owner-local safety fence.
6. I is the sole logical authority for PermissionEpoch. Epochs are opaque and comparable only within their policy domain. Stale, gapped, unknown, incomparable or unverifiable epochs block the operation. Offline/stale authorization leases and cached ALLOW without online currentness proof are prohibited by this baseline.
7. PermissionEpoch and D ForgetFence/ForgetFenceGeneration are independent namespaces and independent checks; neither substitutes for the other.
8. Unknown security-critical fields, malformed or duplicate refs, unsupported major versions, missing required bindings, forged/mismatched identity claims and ambiguous outcomes fail closed. Unsupported capability is not success and cannot be silently downgraded.
9. A protected irreversible operation uses a single-use I `CommitAuthorizationReceipt` bound to policy domain, PermissionEpoch, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef, DelegationChainRef, operation ID, operation payload digest, owner boundary and decision ID. The owner submits it at its final commit gate and records the receipt/decision/sequencer evidence.
10. Revocation and the owner commit are ordered by the I policy-domain sequencer. `COMMIT_WON` means the authorization operation won that ordering; it does not by itself prove that the owner's data became visible. `REVOCATION_WON` rejects the operation. `INDETERMINATE_ABORTED` is never success and requires fail-closed recovery.

## 2. Consumer field mapping and boundary obligations

| Required field / behavior | Accepted semantic meaning | DE-S enforcement point | Required negative behavior |
|---|---|---|---|
| PrincipalRef | I-resolved authenticated subject, never payload-authenticated | D canonical mutation admission; E ingress and publication | unresolved, revoked or mismatched => deny/quarantine |
| ActorRef | H/I verifier-produced per-operation attribution | D mutation attribution; E work and publish attribution | caller-minted, stale-session or mismatched => reject |
| Producer/Adapter identity | registered workload/application identity separately bound to Principal | E ingress/work admission; D registration/work admission; Storage receipt context | forged/unregistered/replaced instance => reject/quarantine |
| ScopeRef | authoritative typed Scope identity with explicit roles | D target/mutation scope; E source/work/dependency scope | missing, ambiguous or implicit inheritance => deny |
| EnvironmentRef | authoritative Environment identity, not display label | D/E only where operation profile requires environment binding | unresolved registry or unapproved crossing => deny |
| Authenticated transport binding | protected H verifier context, outside untrusted payload | E ingress; D receives trusted operation context only through authenticated internal boundary | payload mirror cannot override verifier context |
| PermissionEpoch | current I policy-domain epoch | E ingress where protected; mandatory E final publication and D protected mutation boundaries | stale/gap/offline/unknown => pause/deny |
| Revocation | sequencer-ordered I revocation, rechecked at irreversible owner boundary | D canonical commit; E final publish gate | revocation wins or uncertain => abort/no visibility |
| Forged payload identity rejection | compare claims with verifier and authoritative registry binding | E ingress and D mutation admission | mismatch => reject, audit, no fallback |
| Unknown/Unsupported handling | fail closed; no inferred capability or evidence | all DE-S protected boundaries | remain blocked/Unknown; never mark success |

## 3. Boundary-specific acceptance

### E — Producer ingress / compiler publication boundary

E accepts the BIH semantics for authenticated producer ingress, work execution and derived publication:

- At ingress, resolve the authenticated Principal and registered ProducerRef/AdapterRef from protected H verifier context and I registries; payload producer identifiers are claims only.
- Bind every admitted work item to the authenticated producer/workload, ActorRef, exact Scope/Environment context where required, immutable work identity and provenance.
- Revalidate current I PermissionEpoch and relevant D ForgetFence at the final visibility linearization boundary; an upstream ALLOW or ingress-time check is not a transferable publication capability.
- Submit the single-use I `CommitAuthorizationReceipt` to the final E publication gate, bound to the exact operation ID, payload digest and E owner boundary. The final gate participates in the same policy-domain commit ordering against revocation.
- E must not interpret `COMMIT_WON` as proof of Storage visibility. Storage's durable VisibilityPointer + PublicationReceipt transaction remains the visibility authority.
- Record receipt/decision/sequencer evidence alongside E work/dependency/publication identity. A lost response or indeterminate sequencer result follows the same operation ID/digest recovery path; E must not mint a new operation ID to bypass an unknown result.
- ProducerDomainInventoryEpoch / TargetInventorySeal is I-owned global inventory; E's producer registration and work/dependency ledgers are local evidence and cannot replace the global seal.

**E design disposition:** ACCEPTED for semantic consumption, conditional on I governance approval and implementation evidence. **E runtime conformance: NOT VERIFIED.**

### 4. Inventory Seal / Global Forget dependencies

E recognizes I's `ProducerDomainInventoryEpoch` and `TargetInventorySeal` as the global inventory authority covering producer classes, compiler workers, queues, retries, DLQ, replay, staging, derived artifacts, external recipients and restore paths. E's own producer/work registration cannot prove global membership completeness. Unknown producer, late target, invalid seal, epoch change, unsupported recipient or offline evidence keeps the operation open/Unknown and blocks a closed-world completion claim.

### 5. Outstanding evidence and gates

- I governance approval for GOV-01..10 remains blocked; this acceptance does not satisfy it.
- I-owned consumer register remains OPEN until I records/recognizes this exact E Owner artifact.
- JF-10 cross-authority recovery remains P0 OPEN pending I disposition of the exact shared protocol and durable lookup/replay/receipt-consumption guarantees.
- No executable E ingress/compiler/publication implementation, integration test command, database transaction proof or fault-injection evidence is asserted here.
- Required next verification: forged producer/Adapter rejection; issuer/Principal mismatch; stale/gapped PermissionEpoch; revocation-before-commit and commit-before-revocation ordering; receipt single-use and digest conflict; dependency/fence race; crash before/after Storage visibility commit; lost-ACK forward recovery; no publication on unknown/unsupported/offline paths.

**Final state:** E design-level acceptance only. No governance approval, runtime PASS, JF-10 closure or Phase 3.6 Gate passage is claimed.
