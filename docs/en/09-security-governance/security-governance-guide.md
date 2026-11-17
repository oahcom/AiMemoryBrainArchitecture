# Security, Identity & Governance — Architecture Guide

- Document ID: DOC-SEC-001
- Version: 1.0
- Owner: I — Security, Identity & Governance
- Source: I owner branch, security/identity overview, authorization and Forget/retention policies
- Chinese counterpart: [安全、身份与治理架构指南](../../zh-CN/09-security-governance/security-governance-guide.md)
- Status: CANDIDATE global governance contract; not production security certification

## 1. Security is end-to-end

Security is not established by one query filter, cache key, tombstone, or Adapter acknowledgement. It depends on authenticated identity, explicit Scope, policy decisions, reauthorization at trust boundaries, revocation propagation, Forget barriers, and verifiable evidence.

I owns global identity/authorization policy, delegation and revocation, retention, audit governance, backup/external-copy policy, global Forget completion policy, and physical-erasure requirements. D/E/F/G/H/C retain their local enforcement mechanisms and boundary-specific evidence.

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
| I | Initiation/approval authority, target inventory policy, completion criteria, exceptions, legal hold, retention, backup/external-copy rules, audit and erasure evidence |
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

The global result is a per-target evidence vector, not a single boolean. It must distinguish suppression, derivative cleanup, controlled-storage erasure, backup expiry, external-recipient acknowledgement, and approved residual exceptions. UNKNOWN, FAILED, or UNSUPPORTED targets cannot silently become success.

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


## 11. Joined Forget contract alignment proposal — pending D/I approval

The bilingual joined contract proposal is recorded at `14-ai-development/work-items/AID-2026-001/forget-lifecycle-joined-contract-proposal-v1.md`. This is a proposal and does not supersede this CANDIDATE governance guide until D and I approve the exact same version/SHA.

Proposed I-owned decisions:
- current authorization, delegation/revocation, subject and Scope eligibility, purpose, consent, retention and legal-hold policy;
- global target-inventory policy, mandatory target classes, inventory sealing and re-evaluation triggers;
- global completion aggregation, approved residual exceptions, audit integrity and truthful public status.

D retains canonical Memory lifecycle, ForgetOperation and ForgetFence semantics. I does not redefine `Forgotten` or the canonical linearization event. D does not grant authorization, waive retention/legal hold, or unilaterally declare global completion. E/F/G/H/C/Storage/external recipients provide only their own capability-bounded execution evidence.

The operation phase is separate from Memory lifecycle. A durable `SuppressionCommitted` event may place the Memory in terminal `Forgotten` while cleanup remains asynchronous. `Completed` requires all mandatory targets to have verified terminal evidence. Unknown, failed, unsupported or unaccounted-for mandatory targets block `Completed`. `CompletedWithPolicyException` requires explicit I approval, bounded residuals, compensating controls, an accountable owner and expiry/review; it is not physical-erasure proof.

**Status:** PROPOSED / D-I APPROVAL PENDING / R3 TESTS NOT RUN.
