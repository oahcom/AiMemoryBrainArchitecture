# Module Baseline & Redlines Template

- Module: `<A–I>`
- Baseline ID / version: `<MODULE-PB-x / 0.1.0>`
- Status: **PROPOSED — owner approval pending**
- Owner / decision authority:
- Branch / exact HEAD SHA:
- Source artifact paths + blob SHAs:
- Project Baseline version consumed:
- Project Redlines version consumed:

## 1. Module Mission
Purpose, users/consumers, value and explicit non-goals.

## 2. Ownership Baseline
Owned authority, decision rights, write/read authority, lifecycle and source of truth. Identify who may propose, commit, revoke and attest.

## 3. Capability Baseline
Required capabilities, inputs/outputs, state transitions, failure behavior and capability limits.

## 4. Domain Ownership
Owned objects/fields/identifiers/state; non-owned objects; schema/ADR references; unresolved semantics. Do not decide another module's domain.

## 5. Interface Baseline
Producer/consumer contracts, exact version, transport/API/schema, ordering/idempotency, ACK semantics, errors, retries, compatibility and deprecation.

## 6. Security Baseline
Authenticated Principal/ActorRef binding, Scope vs Permission, delegation, revocation/epoch, untrusted data, provenance, retention, Forget and audit requirements inherited from project redlines.

## 7. Module Redlines
For each rule: ID, normative rule, scope, forbidden/allowed behavior, violation example, severity, detection method, remediation, approver, exception policy. Module redlines may be stricter, never weaker than project redlines.

## 8. Forbidden Cross-module Actions
List non-owned data/objects, prohibited direct writes, bypass paths, unauthorized state transitions and required owner APIs.

## 9. Dependency Contracts
Upstream/downstream owner, contract ID/version/status, dependency evidence, acceptance state and unresolved conditions. OPEN dependencies stay OPEN.

## 10. Conformance Requirements
Positive/negative cases, boundary tests, race/failure/replay cases, security tests, evidence format and reproducibility.

## 11. Acceptance Criteria
Entry/exit criteria, measurable tests, required evidence, blocking findings, acceptance authority and explicit non-claims.

## 12. Change Authority
Who can propose, decide and approve module changes; cross-module consultation; ADR authority; emergency changes; migration/rollback.

## 13. Open Decisions
ID, question, owner/authority, options, blockers, affected consumers, due condition and status (OPEN / ADR-BLOCKED / TO_VALIDATE).

## 14. Evidence and Version History
Exact branch and full commit SHA; artifact blob SHA; review date; tests/results; approver and approval evidence; prior versions and supersession. Never cite stale SHAs as current HEAD.

## Required declaration
`This module baseline is subordinate to the approved Project Baseline and Project Redlines. It does not approve non-owned semantics, resolve an external ADR, or claim implementation/test acceptance without evidence.`
