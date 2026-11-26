---
document_metadata:
  domain: security-governance
  role: design-specification
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
        - "Source branch session-i-security-governance-2026-11-16 @ 8abddf814467b271344a9814613a6b7ca6a446c6; original blob 26a990e44709d8604ae515a2a63b510400fd8471"
        - "AID-2026-109 — bounded restoration provenance; no Owner approval asserted"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Original source body bytes are preserved after this metadata block. Restoration does not grant normative approval, cross-owner acceptance or implementation conformance."
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
    canonical_scope: "Informative overview of I security, identity, authorization and cross-domain authority boundaries"
    canonical_scope_id: "security-governance/security-identity-overview"
    canonical_scope_keywords:
      - security
      - identity
      - authorization
      - forget
      - governance
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---
# Security, Identity & Governance — Overview

- Owner: Session I — Security, Identity & Governance Principal Architect
- Baseline branch/commit: `main` @ `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2`
- Reviewed module baselines:
  - B: `main` @ `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` — `02-domain-model/domain-model-overview.md`, `core-entities.md`, `scope-and-permission-model.md`.
  - C: `main` @ `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` — Agent integration, telemetry, inference-boundary and Adapter capability-tier documents.
  - D: `session-d-memory-brain-2026-11-16` @ `9dc08c63f6912320e290a963c634748ec44a81c8`.
  - E: `session-e-memory-compiler-2026-11-16` @ `54df136d1e410af834461950e3c61c5c80abd6ad`.
  - F: `session-f-memory-runtime` @ `dad5deb6bfaa2df9956930d0b1372df354112567`.
  - G: `session-g-memory-context` @ `3d2c065be863bc1d349faaeece6f6eaa0047abae`.
  - H: `session-h-bmcp-protocol` @ `fcc5103399b4c322e52d642cae5a2414969399a7` — six candidate BMCP design documents reviewed.
- Governance baseline: all three files under `00-governance/` on the stated main baseline.
- Status: **CANDIDATE architecture policy; not an approved production security policy or implementation certification**
- Related issues: INT-P0-02, INT-P0-03, INT-P0-04, INT-P1-03, INT-P1-04, INT-P1-05, INT-X-02, INT-X-03, INT-X-04, INT-X-06, INT-X-07, D-REV-P1-003.
- Authority: I owns global identity/authorization policy, delegation/revocation, retention, audit governance, backup/external-copy policy, global Forget completion policy and physical-erasure requirements. D/E/F/G retain local mechanisms; H owns wire encoding; C owns Agent-side boundary semantics.

## 1. Executive position

Security is an end-to-end property of authenticated identity, explicit Scope, policy decisions, reauthorization at trust boundaries, revocation propagation, Forget barriers, and verifiable evidence. A local query filter, cache key, tombstone, or Adapter acknowledgement alone is not proof of system-wide safety.

The design separates three planes:

1. **Identity plane:** establishes who/what is acting and which producer or service is bound to that actor.
2. **Decision plane:** evaluates an authenticated actor's requested action against resource, ownership Scope, applicability Scope, delegation, policy, consent/retention constraints and current epochs.
3. **Enforcement/evidence plane:** D/E/F/G/H enforce the decision at their owned boundaries; I governs cross-system revocation, retention, audit and Forget completion.

No identity, permission, Scope binding, trust level, epoch or authorization result is accepted merely because it appears in a payload.

## 2. Normative vocabulary and separation

| Concept | Meaning | Authority |
|---|---|---|
| Principal | Authenticated security subject: human, Agent, service, workload or external recipient | I policy; identity provider/credential issuer authenticates |
| ActorRef | Typed reference to the Principal acting in one operation, optionally through a delegation chain | B typed-reference semantics; I binding policy |
| ProducerIdentity | Authenticated source/producer instance bound to a Principal and credential/issuer | I + H transport binding; C telemetry semantics |
| Issuer | Trusted authority that minted/attested a credential or delegation | I trust registry |
| Delegation | Bounded, time-limited authority exercised by a delegate on behalf of a grantor | I |
| ScopeRef | Domain namespace/ownership or applicability reference | B defines domain meaning; I decides permission |
| Permission | Allow/deny for a named action on a resource under policy | I |
| PermissionEpoch | Monotonic authorization generation used to invalidate stale decisions/leases | I |
| ForgetFence | D-owned canonical suppression generation for affected objects/scopes | D owns canonical state; I owns global completion policy |
| ContextVersion | Desired managed Context state | G |
| Delivery / Applied | Delivery and Adapter application evidence | G semantic authority; H execution/wire; C final request semantics |

Authentication answers *who presented a verifiable identity*. Authorization answers *may that Principal perform this action now*. Ownership Scope answers *which namespace owns the object*. Applicability Scope answers *where/for whom the object may be relevant*. These questions must never be collapsed into one field.

## 3. Global security invariants

- **SG-01 — Authenticated binding:** Principal and ProducerIdentity originate from a trusted authentication channel; payload identity is only a claim to compare, never an authenticator.
- **SG-02 — Scope is not permission:** matching Scope is necessary but insufficient for access.
- **SG-03 — No implicit inheritance:** tenant/user/project/Agent/task/session/environment scope membership is explicit and versioned. No wildcard or parent-scope access is inferred.
- **SG-04 — Least privilege:** grants are action/resource/scope/audience/time bounded; delegation cannot amplify authority.
- **SG-05 — Reauthorize at boundaries:** every materialization, dereference, commit, delivery and final inference boundary uses current policy/epochs.
- **SG-06 — Fail closed:** unknown identity, unavailable policy, stale epoch, missing scope binding, ambiguous ownership, expired delegation or unverifiable revocation state denies protected access.
- **SG-07 — Forget wins:** an active Forget suppression fence overrides stale index, cache, Context snapshot, Adapter state, replay and backup restore.
- **SG-08 — Completion is evidence-based:** Unknown/offline is not Confirmed. Completion requires inventory closure, barriers and target evidence or explicit approved PolicyException.
- **SG-09 — Honest erasure claims:** logical suppression, derivative cleanup, backup expiry and physical erasure are separate outcomes.
- **SG-10 — Data is not instruction:** Memory, Evidence, Provenance, Entity labels, summaries and compactions remain untrusted data.
- **SG-11 — Minimize audit:** audit evidence must not retain forgotten content or allow its reconstruction.
- **SG-12 — No provider overclaim:** I cannot certify deletion from an external model provider's hidden prompt, internal state, safety logs or undocumented backups.

## 4. Decision status and cross-module issues

| Topic | I position | Status / owner |
|---|---|---|
| Principal / ActorRef / ProducerIdentity | Define authenticated subject and provenance chain | CANDIDATE; I + H + B |
| Ownership vs applicability Scope | Preserve B's domain distinction; authorization remains separate | CANDIDATE; B + I |
| Permission decision / epoch | Versioned, expiring, audience-bound decision; deny on stale epoch | CANDIDATE; I |
| Reauthorization points | Required at ingress through final inference boundary | CANDIDATE; all boundary owners |
| Forget suppression/cleanup/erasure | Three independent states with global inventory and barrier | CANDIDATE; D + I, E/F/G/H implement |
| Fact / Claim model | I consumes B's typed references; does not adjudicate model | **ADR-BLOCKED INT-P0-01** |
| BMCP envelope | H owns serialization and wire fields | H candidate package exists on `session-h-bmcp-protocol` @ `fcc5103399b4c322e52d642cae5a2414969399a7`; its identity and Forget fields remain dependent on I/D/C and are not frozen |
| Applied | C/G/H define evidence; no proof of model attention | CANDIDATE |
| External provider erasure | Contractual/API evidence only; hidden internal state outside control | Residual risk |

## 5. Security decision contract (logical, not wire)

A policy decision has the logical tuple:

`Decision = (decision_id, effect, subject_ref, actor_ref, action, resource_ref, ownership_scope_ref, applicability_scope_refs, policy_version, permission_epoch, delegation_chain_ref, audience, obligations, issued_at, expires_at, reason_code, correlation_id)`

Effects are `ALLOW`, `DENY`, or `INDETERMINATE`. Only ALLOW is usable. DENY and INDETERMINATE both block protected work; callers may expose a disclosure-safe reason. Obligations may require evidence minimization, purpose limitation, no-export, step-up authentication, redaction, retention class, or additional approval.

This is a semantic contract only. H decides how any decision context is transported/encoded; I does not define BMCP wire fields.

## 6. Required boundary reauthorization

| Boundary | Required check | Enforcement owner |
|---|---|---|
| Ingress / Accepted receipt | Authenticate producer; bind payload producer claim; authorize ingest and retention | H/C/I semantics; E enforcement |
| Compile / source dereference | Recheck actor, producer, source Scope, purpose, retention and current epoch before reading or deriving | E |
| Canonical commit / lifecycle | Reauthorize mutation, expected version, owner Scope, delegation and Forget fence at commit linearization point | D |
| Retrieval / candidate generation | Scope/permission filter before candidate exposure; canonical and fence revalidation | F + D |
| Evidence / Provenance dereference | Independently authorize each protected source/content ref; no inherited access from parent Memory | E/F + D |
| Context planning/edit/reconciliation | Reauthorize every entry and its exact MemoryVersion; apply Forget and policy epochs | G + D |
| Delivery / Adapter apply | Reauthorize recipient, session, environment, target Context and delivery immediately before apply | G/H |
| Final inference boundary | Recheck revocation/fence and managed-region eligibility for exact request/session/context/delivery | H/C with G and I policy |
| Export / backup / restore | Check retention, destination, encryption, region, recipient and Forget ledger before copy/restore | I + storage |

## 7. Threat and trust assumptions

Trust anchors are configured issuer keys/metadata, authenticated transport identity, protected credential stores, policy authority, durable epoch/fence storage and independently controlled audit approval. A compromised issuer, policy authority, signing key or enforcement runtime is a high-severity trust-root compromise; cryptographic binding does not cure a compromised root.

All external input, model output, retrieved text, evidence, labels, provenance descriptions and adapter payloads are untrusted. Integrity hashes detect alteration, not truth or benign intent. Prompt-injection defense is layered containment and reduced authority, not a guarantee of model immunity.

## 8. Governance gates and non-claims

Before implementation sign-off, owners must supply conformance evidence for the matrix in `threat-model-and-adversarial-test-plan.md`, plus storage/backup recovery evidence. Architecture documents are candidate specifications, not proof that deployed code enforces them.

I does not implement local D/E/F/G Forget mechanisms, does not define H wire serialization, does not control Agent tool authorization, and cannot promise external LLM-provider internal physical erasure. Risk acceptance is governed in `audit-and-exception-governance.md`.

---

## Phase 3 targeted remediation status — 2026-11-16

I has added the candidate governance contract `global-forget-target-inventory-and-completion-evidence.md` and refined the existing Forget, identity, scope/revocation and audit/exception policies.

Current I-owned outcomes:
- ProducerDomainInventoryEpoch is explicitly separated from D's ProducerRegistrationHighWater / per-Forget WorkItemBarrier; no numeric comparison or substitution is permitted.
- Target Inventory Seal, stable TargetId, target coverage, seal invalidation/reopening and target evidence binding are specified.
- Global Completion Evidence Vector separates immediate suppression, producer barrier, derived cleanup, runtime/context/adapter suppression, external copies, backup/restore and physical erasure.
- All seven H ACK classes are mapped to bounded target actions. Offline, UNKNOWN and UNSUPPORTED remain Unknown by default.
- PermissionEpoch, ForgetFenceGeneration, IndexWatermark, ContextVersion and AdapterCapabilityEpoch remain separate typed namespaces.
- PolicyException requires target/scope binding, appropriate independent approver, rationale, expiry, risk owner, compensating controls and audit evidence. Expiry reopens the operation.
- Twelve I-FGT test scenarios are specified; none are claimed executed.

**Open gates:** INT-P0-02 remains OPEN pending B typed-reference and H transport alignment. B Fact/Claim remains ADR-BLOCKED. INT-P0-03 remains OPEN pending D/E/Storage atomic registration/publication conformance and F/G/H implementation evidence. This document set is candidate governance policy, not implementation certification.



## Phase 3.5 governance alignment

The authoritative Phase 3.5 I-owned mapping is recorded in `phase-3.5-global-identity-forget-governance.md`; decision approval status is tracked in `governance-decision-register.md`.

- Principal/Issuer/ProducerIdentity/AdapterIdentity are authenticated and issuer-bound; ActorRef/ScopeRef remain B-owned typed references.
- Every protected operation revalidates current authorization at its boundary; old Context, cached ALLOW, lease or session is not a perpetual grant.
- I Producer/Recipient Domain Inventory and its `ProducerDomainInventoryEpoch` are distinct from D's per-Forget WorkItemBarrier / ProducerRegistrationHighWater.
- H ACKs are target/action/capability/session/Scope/managed-region bounded; UNKNOWN and UNSUPPORTED are not success.
- Global Forget completion is a typed evidence vector spanning D/E/F/G/H, external recipients, backup/restore and physical erasure.
- All Phase 3.5 policy decisions remain Proposed/OPEN pending their named approvers. This documentation does not certify implementation or deletion.
