---
document_metadata:
  domain: security-governance
  role: architecture-guide
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "RECONSTRUCTED_FROM_MIRROR: docs/en/09-security-governance/security-governance-guide.md @ 061c5847b3df879eeaf3c71e5eae0bfa162b276a"
        - "Existing ZH-CN mirror: docs/zh-CN/09-security-governance/security-governance-guide.md @ 372d27c79dc79d09bcdb0f142c979efdba1c2b6e"
        - "AID-2026-109: canonical root reconstructed because source branch contains no guide blob"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Canonical body copied byte-for-byte from existing EN mirror; existing EN/ZH-CN mirrors unchanged. No I Owner acceptance or normative promotion asserted."
    usage_status: Active
    modification_status: Modified
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
    canonical_scope: "Informative I Security, Identity and Governance architecture guide; not detailed policy approval"
    canonical_scope_id: "security-governance/architecture-guide"
    canonical_scope_keywords:
      - security-governance
      - identity
      - authorization
      - forget
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: "docs/en/09-security-governance/security-governance-guide.md"
    zh-CN: "docs/zh-CN/09-security-governance/security-governance-guide.md"
  provenance:
    classification: RECONSTRUCTED_FROM_MIRROR
    source_branch: "session-i-security-governance-2026-11-16 @ 8abddf814467b271344a9814613a6b7ca6a446c6"
    source_branch_guide: NOT_FOUND
---
# Security, Identity & Governance — Architecture Guide

- Document ID: DOC-SEC-001
- Version: 1.0
- Owner: I — Security, Identity & Governance
- Source: I owner branch, security/identity overview, authorization and Forget/retention policies
- Chinese counterpart: [安全、身份与治理架构指南](../../zh-CN/09-security-governance/security-governance-guide.md)
- Status: CANDIDATE global governance contract; not production security certification

## 1. Security is end-to-end

Security is not established by one query filter, cache key, tombstone, or Adapter acknowledgement. It depends on authenticated identity, explicit Scope, policy decisions, reauthorization at trust boundaries, revocation propagation, Forget barriers, and verifiable evidence.

I owns global identity/authorization policy, delegation and revocation, retention, audit governance, backup/external-copy policy, cross-system Forget governance evaluation policy, evidence-acceptance criteria, and physical-erasure requirements. D alone owns canonical Forget lifecycle semantics and the D-domain completion predicate. I's cross-system governance evaluation MUST NOT redefine D's canonical states or declare D-domain completion. D/E/F/G/H/C retain their local enforcement mechanisms and boundary-specific evidence.

## 2. Three governance planes

| Plane | Purpose |
|---|---|
| Identity plane | Establish who/what is acting and which producer/service is bound to that actor |
| Decision plane | Evaluate actor, action, resource, ownership/applicability Scope, delegation, policy, consent/retention, and current epochs |
| Enforcement/evidence plane | D/E/F/G/H enforce at owned boundaries; I governs cross-system revocation, retention, audit, and Forget completion |

No identity, Scope, trust level, epoch, or authorization result is trusted merely because it appears in a payload.

## 3. Principal, ActorRef, and ProducerIdentity

- Principal is an authenticated security subject: human, Agent, service, workload, Adapter, or registered external recipient.
- ActorRef identifies the Principal performing an operation and preserves its authority/delegation chain.
- ProducerIdentity binds a producer instance to an authenticated Principal, issuer, credential, source kind, permitted event families, security domain, and revocation/credential epoch.
- Issuer is the trusted authority that minted or attested a credential/delegation.
- Delegation is bounded authority exercised by a delegate on behalf of a grantor.
- ScopeRef identifies a domain namespace/ownership or applicability reference; it is not Permission.
- Permission is allow/deny for a named action on a resource under policy.
- PermissionEpoch invalidates stale authorization decisions and leases.
- ForgetFence is D's canonical suppression generation; it is not PermissionEpoch.

Exact typed-reference semantics and wire fields remain subject to B/I/H joint approval. A caller-constructed ActorRef is not proof of authentication; H must bind the authenticated transport principal and I defines the trust policy.

## 4. Scope and authorization

A request carries resolved typed Scope bindings for the dimensions required by its action/resource class, such as tenant, user, project, Agent, Agent instance, task, session, and environment.

Missing required dimensions are deny/indeterminate, never wildcard. Display names, model names, user-provided IDs, and free-form payload claims are not identity credentials. Default deny applies to ungranted operations.

Permission must be checked at ingress, canonical read, Evidence/source dereference, mutation, lifecycle transition, activation/context delivery, export/sharing, Forget, audit, and asynchronous worker execution. Queued authorization is not permanent: workers re-check current policy before protected or irreversible stages.

## 5. Forget is a cross-system workflow

Forget is not one row deletion. The governance model separates:

1. Immediate logical suppression: stop new access, derivation, candidate emission, Context application, and restore-based reappearance under a durable fence.
2. Asynchronous derivative cleanup: remove or render inaccessible registered derivatives, indexes, caches, Working Sets, summaries, embeddings, exports, and downstream copies according to ownership/capability.
3. Physical erasure: irrecoverably remove content and recoverable copies from controlled primary storage and backup media under approved retention/backup schedules and evidence standards.

Suppressed does not mean Cleaned. Cleaned does not necessarily mean all backups have expired. An external acknowledgement does not prove erasure of hidden provider copies unless an auditable guarantee covers them.

## 6. Forget authority split

| Owner | Responsibility |
|---|---|
| D | Canonical ForgetOperation, target references, Forget Fence/generation, dependency inventory contract |
| I | Initiation/approval authority, cross-system target inventory policy, governance evidence-acceptance criteria, policy exceptions, legal hold, retention, backup/external-copy rules, audit and erasure evidence; does not define D-domain completion |
| E | Compiler work/derivative registration, queue/lease/retry/DLQ/replay suppression and publication gate |
| F | Retrieval candidates, in-flight reads, cache/Working Set, index/rebuild suppression |
| G | Context entries, snapshots/deltas, delivery invalidation and reconciliation |
| H/C | Adapter managed-region clearing/quarantine, offline reconnect and truthful capability-bounded ACK |
| Storage/backup operators | Primary/replica/backup erasure and restore controls |
| External recipients | Contractual/API actions; Brain records only verifiable responses |

## 7. Forget lifecycle and evidence

A request is authenticated and authorized against subject rights, resource ownership, Scope, purpose, retention, legal hold, and delegation. It may be denied, narrowed, deferred, or approved.

Recommended phases are Requested → Authorized → SuppressionCommitted → InventorySealed → CleanupInProgress → CompletionEvaluated → Completed / CompletedWithPolicyException / Failed / Cancelled.

The operation phase is not the Memory lifecycle. A tombstone or canonical state change alone does not prove global completion.

The global governance result is a per-target evidence vector, not a single boolean. D supplies the canonical D-domain operation state and predicate; I evaluates cross-system evidence and policy compliance without rewriting D's state. The vector must distinguish suppression, derivative cleanup, controlled-storage erasure, backup expiry, external-recipient acknowledgement, and approved residual exceptions. UNKNOWN, FAILED, or UNSUPPORTED targets cannot silently become success.

## 8. Security threats and untrusted memory

Memory, Evidence, summaries, and model-produced extraction are untrusted data. They must never become instruction authority or alter policy. The system needs adversarial testing for prompt injection, cross-Scope retrieval, identity spoofing, replay, stale authorization, Forget races, and unauthorized Evidence dereference.

Logs and metrics must avoid leaking protected content or sensitive identifiers. Audit metadata and source content have separate retention/erasure rules.

## 9. Failure and recovery

- Identity/permission service unavailable: fail closed for protected operations.
- Unknown issuer/key, invalid signature, wrong audience, expired or revoked credential: reject.
- PermissionEpoch changes: reauthorize queued/leased work before execution.
- Forget fence cannot be observed by a mandatory domain: status remains SuppressionPending.
- Offline Adapter: target remains unknown until reconnect and reconciliation.
- External recipient gives no verifiable response: do not claim physical deletion.
- Backup restore: enforce Forget fences before restored data becomes queryable or deliverable.
- Legal hold/retention conflict: defer or deny under policy and record the reason.

## 10. Current limitations and validation

This is a CANDIDATE governance contract, not a production security certification. Principal/ActorRef/ScopeRef and permission binding require joint B/H/I approval. Global producer inventory epoch and D per-work-item barrier are separate mechanisms and must be reconciled. H ACK classes require an explicit mapping to I's per-target state/evidence. D/E/Storage atomic publish gating, F anti-resurrection, G/H Adapter clearing, backup/restore and external-copy proof remain open.

Validation must include identity spoofing, delegation expiry/revocation, cross-Scope denial, stale permission epoch, Forget race/fault injection, backup restore, external recipient exceptions, and zero unauthorized disclosure.

See the [I owner branch](https://github.com/oahcom/AiMemoryBrainArchitecture/tree/session-i-security-governance-2026-11-16/09-security-governance) for detailed candidate governance contracts.


## 11. Joined Forget contract proposal — pending D/I approval

The bilingual joined contract proposal is recorded at `14-ai-development/work-items/AID-2026-001/forget-lifecycle-joined-contract-proposal-v1.md`. The related [Owner D/I authority matrix](../../../14-ai-development/work-items/AID-2026-001/owner-d-i-forget-authority-matrix.md) is also a proposal; neither artifact is normative until D and I approve the exact same version/SHA.

D owns canonical Memory lifecycle, ForgetOperation/Fence semantics and the D-domain completion predicate. I owns authentication/authorization, privacy/retention/legal-hold policy, cross-system inventory policy, evidence-acceptance criteria and the cross-system governance assessment. I must not rewrite D's canonical state or predicate; D must not waive I policy or declare cross-system governance compliance. Each executor reports only its own capability-bounded action and evidence.

The cross-system governance assessment is separate from D-domain completion. `CompletedWithPolicyException` is a derived public projection only when D has independently recorded `Completed` and I has recorded `CompliantWithException`. Unknown, failed, unsupported or unaccounted-for mandatory targets block I's `Compliant` assessment. Neither a tombstone nor an ACK proves physical erasure.

**Status:** PROPOSED / D-I APPROVAL PENDING / R3 TESTS NOT RUN.

## 12. Attestor Authorization Contract

### 12.1 Authority boundary

I is the sole governance authority responsible for determining whether an Attestor is authorized to perform a declared Attestation operation.

D MUST NOT independently determine whether an Attestor has governance authority.

D validates and persists the authorization decision reference supplied by I. D does not mint, broaden, or reinterpret I authorization.

### 12.2 Fact and FactRevision binding

Every FactRevision MUST bind to:

- Exact FactRef and FactRevisionRef.
- Exact ClaimRevisionRef values being attested.
- Exact EvidenceRef values.
- Exact ProvenanceRef values.
- ScopeRef and applicable visibility constraints.
- Valid-time interval and recorded/commit-time references.
- Attestor principal identity.
- Authorization decision reference.
- Attestation Method identifier and immutable Version.
- Attestation outcome, rationale, and correction/revocation lineage.

A FactRevision MUST NOT silently follow a Claim's latest revision.

### 12.3 Required authorization decision

Each authorization decision MUST bind:

1. Attestor principal identity: stable authenticated PrincipalRef, not a display name or self-asserted ActorRef.
2. Authorization Scope: exact ScopeRef and permitted resource/action boundary.
3. Attestation Method and Version: exact registered method identifier and immutable version.
4. Validity: effective-from, expiry, and applicable authorization epoch.
5. Revocation: revocation identity, effective ordering, currentness, and handling of in-flight attestations.
6. Delegation: explicit ALLOWED or PROHIBITED decision.
7. Decision identity: immutable AuthorizationDecisionRef and policy/version reference.

8. **Unique Attestation Operation Binding:** Each authorization decision MUST bind to exactly one immutable `AttestationOperationRef`. The binding MUST identify the exact `FactRef` and `FactRevisionRef` targeted by that operation.

9. **Exact Claim and Evidence Binding:** Each authorization decision MUST bind to the complete, exact set of `ClaimRevisionRef` values and `EvidenceRef` values used by the authorized operation. The sets MUST be unambiguous and immutable for that operation. The decision MUST NOT authorize an unspecified, subsequently expanded, substituted, or implicitly resolved set of claims or evidence. The decision MUST also bind the exact `ProvenanceRef` values when provenance references form part of the operation's attested input.

10. **Single-Use Consumption and Replay Protection:** Each authorization decision MUST be consumable by exactly one `AttestationOperationRef`. Its consumption state MUST distinguish an unused decision from a decision consumed by its uniquely bound operation. Once consumed, the decision MUST NOT authorize another operation, FactRevision, target, ClaimRevision set, or Evidence set. Reuse of the same `AuthorizationDecisionRef` by a second operation MUST fail closed, regardless of Scope compatibility, Method/Version compatibility, or validity period.

11. **Idempotent Submission:** Repeated submission of the same `AttestationOperationRef` with the same exact target, ClaimRevision set, Evidence set, and authorization decision MUST be treated as an idempotent replay and MUST return the original committed result. It MUST NOT create another FactRevision, another authorization consumption, or another independent attestation result. A submission using the same operation reference with any different bound identity or content MUST fail closed. A different operation reference MUST NOT inherit the original operation's authorization consumption.

12. **Revocation and Fresh Authorization:** Revocation MUST NOT restore or release a consumed authorization decision for reuse. Any subsequent attestation requiring authorization after revocation MUST use a fresh `AuthorizationDecisionRef` bound to a new unique `AttestationOperationRef`. A fresh decision MUST NOT be interpreted as reuse, renewal, or reassignment of the revoked or previously consumed decision.

The decision MUST also retain its issuing authority and decision provenance.

Delegation is NOT_ALLOWED by default.

Every authorization decision MUST explicitly declare ALLOWED or PROHIBITED.

If Delegation is ALLOWED, the complete delegation chain, delegating principal, delegated principal, authority, Scope, Method restrictions, delegation depth, expiry, and revocation conditions MUST be verifiable.

An Attestor MUST NOT derive delegation authority from its own authorization.

### 12.4 Fail-closed behavior

Missing, ambiguous, expired, revoked, or unverifiable authorization MUST fail closed.

A Method identifier without its exact Version is insufficient.

Changing a Method or Version MUST NOT silently broaden an existing authorization.

### 12.5 Authorization change and historical FactRevision

A later authorization change MUST NOT silently rewrite a committed FactRevision.

The authorization decision and its validity at the original attestation commit remain part of historical audit evidence.

If the Attestor's authority is revoked or materially changed, subsequent attestations MUST use a fresh authorization decision.

Existing FactRevisions MUST be evaluated under the applicable revocation policy.

They may be marked challenged, invalidated for current use, or superseded through a new governed transition.

Their original immutable contents MUST NOT be overwritten.

The relationship between the original authorization decision and any subsequent review decision MUST remain traceable.

### 12.6 D responsibility: verification and persistence

Before committing a FactRevision, D MUST:

1. Obtain the I AuthorizationDecisionRef.
2. Verify that the reference is resolvable and authentic under the applicable governance contract.
3. Verify Attestor principal identity.
4. Verify Scope compatibility.
5. Verify exact Method/Version authorization.
6. Verify authorization validity at the relevant evaluation time.
7. Verify that authorization was not revoked at that time.
8. Verify all delegation conditions when Delegation is explicitly ALLOWED.
9. Bind the exact authorization decision reference to the FactRevision.
10. Persist the decision reference and verification outcome in the auditable commit record.

11. **Unique Operation Binding Verification:** D MUST verify that the `AuthorizationDecisionRef` is bound to exactly one `AttestationOperationRef` and that the current attestation submission presents that exact operation reference.

12. **Exact Target Verification:** D MUST verify that the `FactRef` and `FactRevisionRef` bound by the authorization decision exactly match the target of the current submission. Any missing, ambiguous, substituted, or mismatched target reference MUST fail closed.

13. **Exact Claim and Evidence Set Verification:** D MUST verify that the complete `ClaimRevisionRef` set and `EvidenceRef` set bound by the authorization decision exactly match the sets presented by the current submission. D MUST also verify the exact `ProvenanceRef` set when provenance references form part of the authorized operation's attested input. Missing, additional, substituted, ambiguous, or otherwise mismatched members MUST fail closed.

14. **Authorization Consumption Verification:** D MUST verify that the authorization decision has not previously been consumed by another operation. An unused decision MAY be consumed only by its uniquely bound `AttestationOperationRef`. If the decision is already consumed, D MUST accept only an idempotent replay of that same operation with identical bound identities and content, returning the original committed result without creating another FactRevision or consuming the decision again. Any other reuse, competing consumption, or conflicting replay MUST fail closed.

15. **Binding and Consumption Integrity:** D MUST verify that the authorization decision's operation binding, target binding, ClaimRevision set, Evidence set, and consumption state remain consistent throughout commit processing. A mismatch or unverifiable state MUST fail closed. D MUST NOT infer authorization from Scope compatibility, Method/Version compatibility, or validity alone when any operation-binding or consumption requirement is unsatisfied.

D performs these checks as contract-compliance and reference-integrity verification. D MUST NOT independently reassess, replace, or override I's governance eligibility judgment, authorization decision, or authority as the sole governance decision-maker.

D MUST preserve the exact AuthorizationDecisionRef, Attestor principal reference, Method/Version, Scope, authorization context, evidence digest/reference, commit sequence, and FactRevision lineage.

D MUST reject an attestation with missing authorization evidence or an authorization reference that cannot be resolved and validated.

D verifies contract compliance and reference integrity. It does not replace I's governance judgment.

**Semantic Contract and Implementation-Conformance Boundary**

The operation-binding, exact-target, exact-input, single-use consumption, replay-protection, and idempotent-submission requirements in this section are semantic contract requirements and an implementation-conformance gate. They MUST NOT be interpreted as approval of any Schema, DDL, Public API, storage model, persistence mechanism, or implementation-specific data representation. This contract does not prescribe or select a storage implementation, physical data structure, transaction mechanism, or wire format. It does not introduce a new governance role or transfer governance decision authority. I remains the sole governance decision authority for authorization decisions. D verifies the resulting contract compliance and reference integrity without assuming or exercising I's governance authority. No Schema, DDL, Public API, production key, Trust Root, or cryptographic Profile is approved by these requirements.

### 12.7 Method correctness boundary

Attestation Method identity proves which declared procedure was invoked. It does not prove that the procedure is correct.

Confidence is an assessment value, not an authorization grant and not a Fact creation mechanism.

Verified is an epistemic status, not a substitute for Attestor authorization.

No production key, Trust Root, cryptographic profile, public authorization schema, DDL, or public API is approved by this semantic contract.
