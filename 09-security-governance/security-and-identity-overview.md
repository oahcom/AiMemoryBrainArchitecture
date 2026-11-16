# Security, Identity & Governance — Overview

- Owner: Session I — Security, Identity & Governance Principal Architect
- Baseline branch/commit: `main` @ `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2`
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
| BMCP envelope | H owns serialization and wire fields | H package not present at inspected ref; dependency OPEN |
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
