# I Module Baseline & Redlines — PROPOSED

- Proposal ID: I-MBR-001
- Version: 0.1.0
- Status: PROPOSED — NOT APPROVED
- Owner role: I — Security & Governance Architect
- Branch: `session-i-security-governance-2026-11-16`
- Reviewed branch HEAD: `f16a52ebc0bddb707565c0393f378a4baa782e54`
- Date: 2026-11-17
- Template: requested `00-governance/module-baseline-and-redlines-template.md` returned 404 on main and is absent from the reviewed I tree. This proposal follows the requested 14-section structure without claiming template compliance.
- Scope: I security/governance policy authority only. This proposal does not define B typed references, H wire encoding, D canonical ForgetFence, Storage execution, or PGA project approval.

## 1. Module Mission

I owns the security and governance policy plane for AiMemoryBrainArchitecture: Principal and Issuer trust, authenticated actor binding, Permission decisions and PermissionEpoch, delegation, revocation, retention, Global Forget policy and closed-world producer/recipient inventory, Inventory Seal, backup/restore governance, security audit, exception approval requirements and residual-risk accounting.

I defines policy, trust and evidence acceptance criteria. It does not claim that downstream modules have implemented or passed those controls. Security policy acceptance, technical design agreement, runtime conformance, external governance approval and physical erasure are separate gates.

## 2. Ownership Baseline

**I is authoritative for:**
- Issuer trust policy and Principal trust lifecycle.
- Authentication requirements and authenticated actor binding policy.
- Permission decisions, PermissionEpoch authority, delegation and revocation policy/order.
- Retention and Global Forget governance, ProducerDomainInventoryEpoch, target registration policy, TargetInventorySeal, per-target evidence requirements, exception taxonomy and global state evaluation.
- Backup/restore governance, restore quarantine requirements and anti-resurrection acceptance criteria.
- Security audit, integrity, incident evidence and residual-risk register.

**I is not authoritative for:** B's Typed Reference/Scope/Environment type semantics; H's BMCP wire encoding and transport implementation; D's Canonical ForgetOperation/ForgetFence/lineage and per-operation ProducerRegistrationHighWater; G's ContextVersion and Applied record; C's final request evidence; F's index/cache implementation; E's compiler publication; Storage physical deletion/backup execution; PGA external project-wide governance approval.

## 3. Capability Baseline

| Capability | Baseline | Status |
|---|---|---|
| Principal/Issuer trust | Explicit trusted issuer, authenticated Principal resolution, key/credential lifecycle and revocation | POLICY BASELINE; external approval blocked |
| Actor binding | ActorRef attributed by verifier from authenticated context; not caller-minted credential | JOINT TECHNICAL BASELINE; runtime not verified |
| Permission | Operation-bound decision over Principal, Actor, Scope, Environment, resource, action, purpose, audience and policy version | POLICY DESIGN |
| PermissionEpoch | I-owned monotonic policy-domain epoch; consumers revalidate currentness at protected boundary | POLICY DESIGN; execution not tested |
| Delegation | Narrow intersection of parent authority; bounded depth, audience/purpose, expiry and revocation | POLICY CANDIDATE; external approval blocked |
| Revocation | Explicit authority ordering; stale/gapped/unavailable state denies or pauses | POLICY BASELINE; runtime not tested |
| Retention | Separate logical suppression, cleanup, backup expiry and physical erasure | CANDIDATE governance contract |
| Global Forget | Closed-world inventory + immutable seal + D barrier + typed per-target evidence vector | CANDIDATE; inventory not proven closed |
| Backup/Restore | Restore quarantine; replay independent current Forget/revocation ledger before serving | REQUIRED POLICY; no actual evidence |
| Audit | Authenticated, integrity-protected, attributable records with immutable correlation | POLICY BASELINE; implementation not verified |
| Residual risk | Unknown/unsupported/offline targets remain unresolved unless approved scoped exception | POLICY BASELINE; no blanket waiver |

## 4. Domain Ownership

I owns PrincipalTrustPolicy, IssuerTrustPolicy, AuthenticatedActorBindingPolicy, PermissionDecision, PermissionEpoch, DelegationGrant, RevocationEvent/order, RetentionPolicy, GlobalForgetOperationPolicy, ProducerDomainInventoryEpoch, TargetInventorySeal, TargetId registration rules, TargetEvidenceVector, PolicyException, BackupRestoreGovernance, SecurityAuditPolicy and ResidualRiskRecord.

I consumes B's typed PrincipalRef/ActorRef/ScopeRef/EnvironmentRef semantics; H's authenticated transport and wire evidence; D's ForgetOperation/ForgetFence/lineage/work barrier; G's Context invalidation evidence; F's index/cache suppression evidence; E's derivative/producer evidence; C's Adapter/final-request evidence; Storage's backup catalog, restore and physical-erasure evidence. These consumed artifacts do not transfer ownership of their underlying state machines to I.

## 5. Interface Baseline

1. **Authenticated principal:** Protected operations require a verifier-established Principal bound to a trusted Issuer, valid credential/key, audience and authenticated channel. Unknown issuer, invalid signature, expired/revoked credential, collision or ambiguous Principal resolution denies.
2. **Actor attribution:** ActorRef records who/what acted; it is not a credential. The verifier binds it to authenticated Principal, workload/service identity, delegation chain, operation, audience, purpose and session. Caller-supplied ActorRef alone is never authoritative.
3. **Scope and Environment:** ScopeRef is applicability/identity, not permission. B defines typed semantics; I evaluates grants. Missing, ambiguous or retired Scope/Environment fails closed. Cross-Scope and cross-Environment access requires explicit current grants and exact bridge semantics.
4. **Permission decision:** Bind Principal, Actor, operation/resource, role-tagged Scope set, Environment, purpose, audience, delegation chain, policy version, decision ID and current PermissionEpoch. Recheck at admission, protected read, mutation, final publication, delivery and other defined linearization boundaries.
5. **PermissionEpoch:** Opaque, I-owned, partitioned by policy authority. A stale/gapped/unknown epoch or unavailable authority cannot use cached ALLOW. PermissionEpoch is never substituted for D ForgetFenceGeneration, D ProducerRegistrationHighWater, I ProducerDomainInventoryEpoch or F IndexWatermark.
6. **Revocation ordering:** Define authoritative ordering between revocation request, authorization receipt/decision, protected operation commit/visibility and external submission. Uncertain or incomparable ordering blocks protected action; consumers must not invent order from wall-clock timestamps.
7. **Delegation:** Delegated authority is a strict subset of parent authority with exact subject, resource, Scope, Environment, action, audience, purpose, expiry and depth constraints. Parent revocation/expiry invalidates descendants. Cycles, amplification, wildcard and unapproved sub-delegation deny.
8. **Global Forget inventory:** Register every producer, derivative store, retrieval/cache, Context/Adapter, log/audit surface, external recipient, backup/replica/WAL/archive/object version and restore destination capable of holding, deriving, exposing or restoring governed data. Inventory epoch changes on relevant membership/capability/recipient/backup/evidence changes.
9. **Inventory Seal:** Seal canonical ordered target set, target identity/owner, Scope coverage, capabilities, required action/evidence, inventory epoch, digest, signer, timestamp and unresolved gaps. Relevant change or late target invalidates the seal and requires Reopened/reseal.
10. **Per-target evidence:** Bind ForgetOperationId, TargetId, seal ID/version, exact Scope coverage, action, D fence reference, capability/evidence profile, attempt, status, timestamp, authenticated owner/producer, integrity proof, verifier and audit correlation. Unknown is not Confirmed.
11. **Global completion:** Requires valid current seal, D work-item barrier terminal, all mandatory internal/external targets confirmed, no unresolved Unknown/Failed, backup/restore safety and required physical-erasure proof. NotApplicable requires positive absence evidence and independent review. Exceptions require authorized scoped approval and expiry.
12. **Backup/restore:** Backup catalog includes snapshots, replicas, WAL/archive logs, object versions and DR copies. Restore is quarantine-only; before serving/indexing it must replay a current independent Forget/revocation ledger that cannot be rolled back with the data snapshot.
13. **Audit:** Security-sensitive decisions, issuer/key changes, delegation, revocation, policy epochs, inventory/seal changes, target evidence, exceptions and restore actions are attributable, tamper-evident and correlated. Sensitive payloads are minimized/redacted.

## 6. Security Baseline

- No unauthenticated identity can execute protected operations.
- ActorRef is not a credential; ScopeRef is not a permission grant; caller-supplied identity is not authenticated identity.
- Trust is explicit; no trust-on-first-use for unknown issuer/key. Unknown, revoked or ambiguous issuer/Principal fails closed.
- PermissionEpoch currentness is required at protected boundaries. Stale epoch, gap, offline authority or cached ALLOW without current proof denies/pauses.
- Revocation must have an authoritative causal order. In-flight operations with uncertain ordering do not gain permission by racing or retrying.
- Delegation cannot exceed parent grant; expiry/revocation propagates to descendants.
- D Barrier is not Global Inventory. D's per-operation ProducerRegistrationHighWater/WorkItemBarrier and I's ProducerDomainInventoryEpoch/TargetInventorySeal are distinct and both required.
- Adapter ACK cannot establish global Forget. It proves only the exact authenticated target/action/session/region/capability slice.
- Unknown/unsupported/offline target, missing producer domain, late derivative, external recipient or restore path blocks completion unless a properly approved exception applies.
- Inventory Seal is immutable; no producer/recipient/backup path may be silently added, removed or downgraded after sealing. Relevant change reopens the operation.
- Backup restore cannot serve forgotten data. Restore must be quarantined and replay current independent suppression ledger before any access.
- Logical suppression, cleanup, backup expiry, physical erasure and external recipient handling are distinct claims.
- I architect cannot self-approve legal/privacy/security residual risk; PGA/authorized external governance retains project-level authority.

## 7. Module Redlines

| ID | Redline | Required behavior |
|---|---|---|
| I-RL-01 | ActorRef != Credential | Require verifier-authenticated binding |
| I-RL-02 | ScopeRef != Permission | Require explicit operation-bound PermissionDecision |
| I-RL-03 | Caller identity != authenticated identity | Reject payload-only identity and mismatch |
| I-RL-04 | Stale PermissionEpoch != authorization | Deny/pause; no stale cached ALLOW |
| I-RL-05 | Revocation order cannot be guessed | Use authoritative sequencer/order; uncertain order blocks |
| I-RL-06 | D Barrier != Global Inventory | Require both D work barrier and I sealed inventory |
| I-RL-07 | ACK != Global Forget | Evaluate every sealed target and evidence requirement |
| I-RL-08 | Unknown target != success | Unknown/Pending/Failed blocks completion |
| I-RL-09 | Inventory Seal is not mutable metadata | Relevant target/recipient/backup change reopens and reseals |
| I-RL-10 | Backup restore cannot resurrect forgotten data | Quarantine + current independent ledger replay + suppression proof |
| I-RL-11 | Suppressed != physically erased | State each lifecycle/evidence class separately |
| I-RL-12 | Exception != unilateral waiver | Require authorized scoped approvers, expiry and audit |
| I-RL-13 | Policy proposal != governance approval | Preserve GOVERNANCE-BLOCKED until exact approval evidence |
| I-RL-14 | Design != implementation proof | No test, deployment or erasure pass without evidence |

## 8. Forbidden Cross-module Actions

I must not:
- Redefine B Typed Reference, ScopeRef or EnvironmentRef semantics.
- Define H wire encoding, schema field serialization or Adapter transport mechanics.
- Issue, advance, reinterpret or implement D's Canonical ForgetFence or per-operation producer barrier.
- Declare G Applied or decide C final-request submission/provider handoff.
- Claim F index/cache suppression or E derivative publication has executed without owner evidence.
- Treat an Adapter ACK, D barrier, inventory metadata or local tombstone as global completion.
- Seal an inventory with unknown producer/recipient/backup coverage or silently ignore unsupported/offline targets.
- Claim physical erasure based on logical deletion, tombstone, key rotation or unverified backup expiry.
- Approve its own external legal/privacy/security exceptions or substitute its architect role for PGA.
- Change another Owner's branch, main, merge branches, or promote PROPOSED/OPEN to APPROVED.

## 9. Dependency Contracts

| Dependency | Required input/output | Owner | Current disposition |
|---|---|---|---|
| Typed identity and Scope | PrincipalRef/ActorRef/ScopeRef/EnvironmentRef semantics | B | Joint technical baseline; type authority remains B |
| Protocol authentication | Authenticated channel, identity binding, ACK evidence and replay semantics | H | Design baseline and consumer record; H36 NOT RUN |
| Canonical Forget | ForgetOperation, ForgetFence, lineage, producer work barrier | D | D-owned; runtime atomicity and JF-10 proof remain open |
| Context cleanup | Exact Context/snapshot/delta/delivery invalidation evidence | G | G contract exists; G conformance NOT RUN |
| Runtime cleanup | Index/cache/working-set suppression evidence | F | Owner evidence required |
| Compiler cleanup | Derivative producer/work item and publication suppression evidence | E | Owner evidence required |
| Agent/Adapter | Authenticated Agent/Adapter/session and final request/provider evidence | C | Owner evidence required |
| Storage/backup | Backup catalog, restore quarantine, ledger replay and physical erasure | Storage | Design review is not implementation evidence |
| Project governance | External trust, retention, exception and baseline approvals | PGA / authorized governance | GOVERNANCE-BLOCKED |

## 10. Conformance Requirements

Required suites:
- I-TRUST: unknown/revoked issuer, expired credential, Principal collision/alias, forged ActorRef, invalid verifier binding and key rotation/compromise.
- I-DELEG: expired/revoked parent, descendant invalidation, cycle, depth overflow, scope/action/audience/purpose amplification and sub-delegation.
- I-PERM: stale PermissionEpoch/cached ALLOW, epoch gap, authority outage, policy-domain partition and protected-boundary revalidation.
- I-REV: revocation versus admission, publication, delivery, final submission and restore in both causal orders; uncertain order must deny/pause.
- I-SCOPE: cross-Scope and cross-Environment probes, missing/ambiguous refs, exact bridge/grant and side-channel leakage.
- I-INVENTORY: unknown producer discovery, late recipient, inventory epoch bump, seal digest verification, target addition/removal, evidence-contract/capability change and reopen/reseal.
- I-FORGET: D barrier versus I inventory separation, per-target evidence completeness, unsupported/offline target, stale ACK and exception expiry.
- I-BACKUP: backup catalog coverage, snapshot/WAL/archive/replica inventory, restore quarantine, independent ledger replay, forgotten-content suppression and physical-erasure proof.
- I-AUDIT: forged evidence, tampered audit, missing actor, integrity failure, sensitive-data redaction and correlation.
- I-GOV: exact policy hash, approver authority, independent reviewer, scope/jurisdiction, effective time/version, expiry and revocation/supersession.

Existing I36 adversarial matrix is SPECIFIED / NOT RUN. The inspected register states no executable build, command, fixture output, environment or logs were supplied. Pass requires exact build/commit, deterministic fixtures/race schedule, expected/actual output, audit evidence and authorized reviewer sign-off.

## 11. Acceptance Criteria

1. Trust chain, authenticated actor binding, operation-bound permission and PermissionEpoch are explicit and preserve B/H/I ownership.
2. Revocation has an authoritative order and stale/unknown currentness fails closed at every protected boundary.
3. Delegation is bounded, non-amplifying and revoked with parent authority.
4. Global Forget inventory is closed-world, authenticated, versioned and sealed with a canonical digest.
5. I inventory epoch and D work-item barrier remain distinct and both are evidenced.
6. Every required target has action-specific evidence; unknown/unsupported/offline targets block completion absent approved exception.
7. Backup/restore targets are inventoried, quarantined and checked against an independent current Forget/revocation ledger before serving.
8. Logical suppression, cleanup, retention expiry and physical erasure are not conflated.
9. I36 tests execute and pass; governance approvals are separately recorded by authorized bodies.
10. PGA approval is explicit before project-wide governance baseline acceptance.

## 12. Change Authority

I alone changes trust policy, Principal/Issuer admission, authenticated actor binding policy, Permission/PermissionEpoch, delegation, revocation, retention, Global Forget inventory/seal/evidence policy, backup/restore governance, audit and residual-risk criteria. B owns typed domain semantics; H owns wire encoding/transport; D owns canonical ForgetFence; G owns Context/Applied; C owns final-request facts; Storage owns physical persistence/backup execution; PGA/authorized governance approves project-wide policy and exceptions. Cross-boundary changes require exact-version review and authority-specific approval.

## 13. Open Decisions

- I36-GOV-01..10: all GOVERNANCE-BLOCKED in the current approval register; no exact policy hash approval, approver Principal/Issuer, authority basis, effective version/time or approval evidence was located.
- ProducerDomainInventoryEpoch: contract defined, but a signed live ProducerDomainInventory registry snapshot and TargetInventorySeal with canonical digest were not found in the reviewed I branch.
- Global Forget closure: candidate contract exists; D barrier, E/F/G/H/Storage target conformance, external recipient evidence and all target states are not proven closed.
- Backup/restore: policy requires quarantine and independent ledger replay; actual backup catalog, restore exercise, suppression test and physical-erasure evidence not found.
- I36-T01..T20 and H36-01..18: SPECIFIED / NOT RUN.
- B/I/H typed identity: joint technical baseline exists; H design consumer acceptance is recorded, while I's current register contains earlier OPEN rows and later reconciliations. Preserve design-level acceptance only; runtime conformance remains unverified. G/C/F and other consumer acceptance must be checked against their own exact records.
- C/G/H Applied 1.1 package/digest and D causal order: I policy does not decide these; exact authority decisions remain separately required.
- External legal/privacy/security approval and PGA project-level approval: GOVERNANCE-BLOCKED.
- Requested template path: 404 on main and absent from reviewed I tree.

## 14. Explicit Non-Claims

This proposal does not claim I Owner approval, PGA approval, external legal/privacy/security authorization, live issuer deployment, PermissionEpoch enforcement, revocation race correctness, I36/H36 test pass, closed producer/recipient inventory, signed Inventory Seal, Global Forget completion, backup restore safety, physical erasure, external recipient compliance, Storage implementation, or production security certification. A commit proves only publication of this PROPOSED artifact.
