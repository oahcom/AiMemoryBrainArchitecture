# Phase 3.6 — I Six-Dimension Self-Review

- Review authority: Joint BIH Decision Architect, under the user's explicit delegation.
- Subject: I — Security, Identity & Governance.
- Reviewed branch: `session-i-security-governance-2026-11-16`
- Reviewed contract: `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md`
- Reviewed contract blob: `ed05d2d5eafce86d1e21006208f1ba09f6aa5d43`
- Review result: **CONDITIONAL PASS — policy architecture is coherent; operational currentness and governance gates remain unresolved.**
- Scope: design/document review only; no runtime tests executed.

## 1. Responsibility and authority boundary — PASS
I correctly owns issuer trust, Principal/Producer registration, delegation, authorization, revocation and PermissionEpoch. B owns Ref meaning; H owns BMCP transport/wire; operation owners enforce at final boundaries.

## 2. Identity and type semantics — PASS WITH FINDING
The trust chain distinguishes transport authentication, issuer validation, Principal resolution, delegation, Actor resolution, Scope authorization and epoch validation. Payload fields cannot reconstruct trust.

**I36-SR-01 — P1:** Principal registry resolution must specify collision and alias behavior when an issuer rotates keys, changes subject format, or two issuers assert the same external subject. JD-03 provides a composite key but the policy contract does not define explicit link/unlink, merge prohibition and audit-preserving migration behavior. Never merge Principals merely because subjects match.

## 3. Trust and authentication chain — PASS WITH FINDING
Trust is explicit, non-transitive and deny-first. Credential validation covers issuer, key, audience, tenant/domain, subject, validity and revocation. Delegation is bounded by intersection and revocation advances affected epochs.

**I36-SR-02 — P1:** Revocation propagation is conceptual; there is no concrete consistency contract for authoritative epoch read versus revocation commit (linearization point, read-your-writes, quorum/partition behavior, maximum propagation delay). High-risk operations fail closed on uncertainty, but exact consistency guarantees are needed before implementation acceptance.

## 4. Authorization and boundary control — PASS WITH FINDINGS
The complete authorization tuple, explicit Scope/Environment grants, default deny, independent endpoint authorization and distinction from ForgetFence are sound.

**I36-SR-03 — P1:** Policy-domain derivation is illustrative rather than canonical. Define deterministic domain identity, domain migration, multi-domain operation evaluation and atomicity when one operation spans several policy domains.

**I36-SR-04 — P1:** JD-12 removes offline/stale leases from the current technical baseline, but the earlier PermissionEpoch section still describes an I-issued bounded lease path. Reconcile normative text so implementers cannot treat a lease as active without a governance profile.

## 5. Protocol and lifecycle — CONDITIONAL
The policy requires every consumer to revalidate at its own boundary, differentiates PermissionEpoch from ForgetFence and requires reconnect reauthentication.

**I36-SR-05 — P1:** In-flight revocation is delegated to owner-defined irreversible commit/disclosure points. I must define the revocation decision token/epoch proof each owner checks at that point, plus audit evidence for “revocation won” versus “operation committed first.”

## 6. Failure semantics and evidence — CONDITIONAL
Fail-closed outcomes and 15 adversarial scenarios are specified. Governance approvals are correctly blocked and no runtime PASS is claimed.

**I36-SR-06 — P0 DOCUMENT CONSISTENCY:** Section 9 still calls I's document “an I policy proposal” and says formal I approval remains open, while the joint-decision section adopts the delegated BIH technical baseline. Correct state: I technical policy design is decided by delegated joint decision; governance approvals remain GOVERNANCE-BLOCKED; this does not claim an external approver or independent I-session signature.

**I36-SR-07 — P1:** Add tests for epoch-read/revocation-commit races, cross-domain partial failure, issuer subject collision and key rotation overlap/rollback.

## Final disposition
- Six-dimension result: **CONDITIONAL PASS**.
- P0: reconcile stale I Owner Decision and Cross-module Agreement status with the joint technical decision.
- P1: specify epoch consistency/linearization, policy-domain derivation and multi-domain evaluation, lease precedence, in-flight revocation proof, Principal alias migration and missing adversarial tests.
- Governance approvals remain GOVERNANCE-BLOCKED; no approver or policy activation is inferred.
- Runtime tests remain NOT RUN; ADR-001 remains ADR-BLOCKED.
