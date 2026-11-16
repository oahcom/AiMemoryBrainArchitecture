# Module I — Security & Governance Baseline & Redlines

- Proposal: I-MBR-0.1.0
- Status: **PROPOSED — prepared by Session P for I Owner review/adoption; NOT an I Owner decision**
- Intended Owner: I — Security, Identity & Governance
- Source branch / HEAD: `session-i-security-governance-2026-11-16` @ `f16a52ebc0bddb707565c0393f378a4baa782e54`
- Evidence: `09-security-governance/principal-actor-and-authorization-contract.md` blob `03765efac4bb1153f303ce0030f9e277d602e81d`; `09-security-governance/global-forget-target-inventory-and-completion-evidence.md` blob `9100061fa986fb6676656169de3fcf9fc1c72664`; `09-security-governance/phase-3.6-governance-approval-and-consumer-acceptance-register.md` blob `11c4bfde5de02a684cc6e5df46d1f9676f5a40a5`
- Project PB/PR: P proposal v0.1.0 only, not approved/active.

## 1. Module Mission
Define and govern security subject trust, authorization, delegation, revocation, retention, audit, global Forget target inventory and evidence-based risk/exception policy.

## 2. Ownership Baseline
I owns issuer/principal trust policy, authenticated ActorRef requirements, permission and PermissionEpoch, delegation, revocation ordering, retention, backup/external-recipient governance, ProducerDomainInventoryEpoch, target inventory seal, global Forget completion criteria, audit and residual risk policy. I does not own B type meanings, H wire format, D canonical ForgetFence or G/F/E local execution state.

## 3. Capability Baseline
Authenticate issuer/Principal; resolve operation-scoped actor binding; evaluate permissions over principal/action/resource/audience/purpose/scope; advance revocation epochs; inventory every producer/recipient/backup/restore path; evaluate global completion from scoped evidence; govern exceptions and audit immutable decisions.

## 4. Domain Ownership
I owns security policy and global evidence evaluation. B owns typed reference semantics; H owns transport authentication/wire binding; D owns canonical fence/barrier; E/F/G/H/Storage/external recipients own local execution and evidence.

## 5. Interface Baseline
Permission is a policy decision and is never inferred from ScopeRef. ActorRef is not a credential. Global Forget requires a sealed closed-world producer/recipient inventory and target-state evidence mapped to required action; D work-item barrier, inventory epoch, fence generation and local ACK are distinct.

## 6. Security Baseline
Fail closed on unknown issuer, principal, permission, epoch, delegation, target, inventory gap or ambiguous recovery. Preserve auditability, least privilege, purpose binding, revocation ordering, retention and restore quarantine. No unsupported physical-erasure claim.

## 7. Module Redlines
- I-PR-01 No authorization from caller-supplied identity/reference alone. CRITICAL.
- I-PR-02 No protected operation after revocation/epoch invalidation wins its authoritative order. CRITICAL.
- I-PR-03 No Global Forget completion without closed inventory, sealed epoch and all required target evidence or explicit authorized exception. CRITICAL.
- I-PR-04 No substitution of D barrier for global inventory epoch, or ACK receipt for local action completion. CRITICAL.
- I-PR-05 No retention/backup/restore/external-recipient path omitted from declared governance scope. CRITICAL.
- I-PR-06 No project-level baseline/redline approval by I alone; PGA authority remains separate. HIGH.

## 8. Forbidden Cross-module Actions
I must not redefine B domain types, H wire schemas, D canonical Forget state, E compiler internals, F index behavior or G Context state. I cannot self-approve project governance policy or waive project redlines alone.

## 9. Dependency Contracts
B/I/H typed identity trust; D/E/Storage JF-10 and publication ordering; D producer barrier; F/G/H local suppression/removal/ACK; external recipients and backup/restore operators. Current governance approval register says external approvals GOVERNANCE-BLOCKED, consumer acceptance OPEN and I36 NOT RUN.

## 10. Conformance Requirements
Forged identity; issuer rotation; delegation misuse; stale PermissionEpoch; revocation/commit races; unknown inventory target; producer added after seal; lost/duplicate ACK; external recipient omission; backup restore after Forget; exception expiry; audit tampering; fail-closed recovery.

## 11. Acceptance Criteria
I Owner accepts exact version; B/H accept identity binding; D/E/Storage accept JF-10 policy sequencer and recovery; every target class is inventoried; ACK-to-target-state mapping is accepted; threat/adversarial and restore tests run; external governance approval is separately recorded.

## 12. Change Authority
I Owner decides I security semantics. B/H/D/E/F/G/Storage decide their own implementation and domain boundaries. PGA approves project baseline/redlines; I cannot substitute for PGA.

## 13. Open Decisions
B/I/H exact identity binding and permission wire; I acceptance of JF-10; target state mapping for each recipient/backup/Adapter; inventory seal and producer registration completeness; restore evidence and exception policy; external governance approval and I36 execution.

## 14. Explicit Non-Claims
No PGA appointment, project G0 approval, cross-owner acceptance, global Forget completion, physical erasure, I36 test pass or operational readiness.
