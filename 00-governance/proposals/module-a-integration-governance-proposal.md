# Module A — Integration Governance Baseline & Redlines

- Proposal: A-MBR-0.1.0
- Status: **PROPOSED — prepared by Session P for A Owner review/adoption; NOT an A Owner decision**
- Intended Owner: A — Principal Integration Architect
- Source branch / HEAD: `session-a-integration-2026-11-16` @ `2059f27bffa5f0aeecb50108440fe177515b09ff`
- Source evidence: `00-governance/architecture-invariants.md` blob `66266667bdbb1cf15a2644fa98db5ecaaf3bb23b`; `reviews/integration/contract-registry.md` blob `b15a87e9e259de74df600defbdd449772b9b3daa`; `reviews/integration/phase-3.6-final-architecture-acceptance.md` blob `16f86859645447f3f4397c5c89c6013c3cce92b5`
- Template: `00-governance/module-baseline-and-redlines-template.md`
- Project PB/PR consumed: P proposal v0.1.0 only; not approved/active.

## 1. Module Mission
Coordinate architecture integration across A–I; maintain dependency, contract, decision, finding and evidence traceability; reconcile branch-aware baseline snapshots and prepare gate evidence. A is not the product's canonical data authority or the project's sovereign governance authority.

## 2. Ownership Baseline
A owns integration coordination artifacts: cross-module dependency map, compatibility/contract register, integration finding lifecycle, branch/evidence freshness register and gate-readiness synthesis. A may classify evidence and request decisions; it cannot create another Owner's decision.

## 3. Capability Baseline
Required: discover owner branches and exact HEADs; pin artifact path/blob SHA; distinguish Artifact Exists / Owner Decision / Cross-module Agreement / Implementation Evidence; track version-specific consumer acceptance; record OPEN blockers and evidence expiry; publish non-destructive integration reports. Failure to retrieve/verify evidence yields UNKNOWN/NOT REVIEWED, never inferred success.

## 4. Domain Ownership
A owns no canonical Memory, domain schema, Principal/Permission, ContextVersion, BMCP wire or Forget completion semantics. B owns domain semantics; C telemetry/final-request semantics; D canonical Memory/ForgetFence; E compiler lifecycle/publication; F runtime/index/cache; G Context; H protocol/Adapter; I security/global policy.

## 5. Interface Baseline
A consumes exact Owner artifacts and records producer/consumer contract ID, version, branch HEAD, blob SHA, decision status, affected consumers and acceptance evidence. Registry status must not upgrade source status. A report's source snapshot must be explicit and immutable.

## 6. Security Baseline
Preserve least privilege and evidence integrity. Never treat commit author, branch write permission, silence, file existence or A registry entry as authority/approval. Do not expose secrets in evidence. Security/Forget/privacy conflicts require I and affected Owner review.

## 7. Module Redlines
- A-PR-01 No authority laundering: A MUST NOT approve or rewrite another module's owned semantics. Detect by decision-owner/path audit; severity CRITICAL.
- A-PR-02 No status inflation: artifact presence or review completion MUST NOT become APPROVED/ACTIVE or implementation PASS. Detect status/source cross-check; CRITICAL.
- A-PR-03 No stale-baseline claim: every reconciliation MUST pin full branch HEAD and artifact blob SHA; stale/unknown snapshots are labeled. Detect freshness audit; HIGH.
- A-PR-04 No false closure: findings close only with named authority decision and required reproducible evidence. Detect closure ledger audit; CRITICAL.
- A-PR-05 No implied PGA: A coordination role MUST NOT be represented as project governance appointment. Detect authority register review; CRITICAL.

## 8. Forbidden Cross-module Actions
No editing/approving B–I domain contracts on their behalf; no schema/wire invention; no declaring implementation/test pass from static review; no merging Owner branches as a coordination shortcut.

## 9. Dependency Contracts
A consumes all Owner decisions; cross-module acceptance requires every affected authority owner. Known OPEN items include B Fact/Claim ADR; B/I/H typed identity and permission binding; D/E/Storage JF-10 atomic publication/recovery; F/G/H Applied evidence; I Global Forget inventory/ACK/restore mapping.

## 10. Conformance Requirements
Test branch HEAD freshness, blob pinning, registry/source status consistency, missing artifact handling, stale commit handling, owner-consent closure, and negative cases for unauthorized status upgrades.

## 11. Acceptance Criteria
A Owner confirms scope and decision rights; registry has live full HEADs; every row cites source artifacts; unresolved items remain OPEN; independent reviewers can reproduce the snapshot. This is not system implementation acceptance.

## 12. Change Authority
A Owner may decide A's coordination procedures. Project governance rules require PGA under formal charter; cross-module contract decisions require affected Owners. A cannot waive project redlines.

## 13. Open Decisions
PGA appointment/quorum; evidence freshness TTL; finding severity/closure quorum; gate evidence owner; source of truth when Owner artifacts conflict; A acceptance of this exact proposal.

## 14. Explicit Non-Claims
No claim of project authority, contract freeze, implementation completion, G0 approval, branch merge or system readiness.


## Live Owner update — 2026-11-17

A's current Owner branch advanced during this Session P pass to `7d73102576660fb602376c7ce2f2522a0a8b29ad` (commit: `A: record JF-10 bundle decision closure and Gate A transition`). This proposal's original source snapshot is therefore not the latest A HEAD; A Owner must re-review against the new tip before adoption.

The new A integration record says Issue #9 is closed at the decision layer after D and Storage each published exact-bundle Owner decisions. It records D's acceptance as limited to D-owned ForgetFence/barrier semantics and Storage's acceptance as architecture/participant interface only. Issue #10 Gate A remains active: Storage must identify the actual DB product/version/configuration and accountable operator and prove prepared-XID/lock-retention/same-XID recovery and atomic visibility. Gate B persistent COC and Gate C fault injection remain blocked. JF-10 P0 remains OPEN; multi-PolicyDomain remains BLOCKED.

A's latest record also preserves the separate Applied contract issue: C/G/H common Applied schema version/digest and exact approvals remain unresolved; architecture baseline freeze remains NOT AUTHORIZED. A Owner should refresh this proposal's branch HEAD and registry source pins before deciding it.
