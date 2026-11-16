# Project Acceptance Gates — AiMemoryBrainArchitecture

- Version: 0.1.0
- Status: **PROPOSED — NOT APPROVED**
- Gate rule: no gate passes on document/commit count, author self-review or unverified status labels.

## Gate summary

| Gate | Purpose | Proposed approval authority | Current status |
|---|---|---|---|
| G0 Project Governance | Ratify mission, scope, redlines, authority and change control | PGA (appointment OPEN) | BLOCKED / PROPOSED |
| G1 Domain & Ownership | Approve domain semantics, object ownership and authority boundaries | Domain ADR authorities + all affected Module Owners | NOT ASSESSED |
| G2 Contract Closure | Close cross-module contracts and blocking ADRs | All authoritative producer/consumer owners; A records integration disposition | NOT ASSESSED |
| G3 Implementation | Deliver core implementation and module tests | Engineering/Implementation Acceptance Authority + Module Owners | NOT ASSESSED |
| G4 System Conformance | Prove end-to-end, security, Forget, recovery, concurrency and fault behavior | Verification Authority + affected owners; I for security | NOT ASSESSED |
| G5 Operational Readiness | Prove deployability, performance, resources, monitoring and operational controls | Operational Acceptance Authority + PGA for product-level acceptance | NOT ASSESSED |

## G0 — Project Governance

**Entry Criteria**
- Project sponsor/founder identifies the proposed PGA and governance process.
- Baseline, redlines, decision authority, gates and change-control documents are versioned and reviewed.
- All disputed statements are explicitly PROPOSED/OPEN.

**Exit Criteria**
- PGA appointment and approval process recorded with evidence.
- Project Baseline and Redlines explicitly approved by PGA.
- Redline waiver and change-control policy approved.
- Gate authorities, quorum, escalation and appeal process approved.
- Registries reflect exact approved versions and effective date.

**Required Evidence:** signed/attributed governance decision, exact commit and file versions, approval record, registry update, change history.

**Blocking Findings:** PGA unidentified; authority/quorum undefined; redlines or baseline not approved; unresolved conflict with existing authoritative decisions.

**Waiver Policy:** no waiver of PGA appointment or truthful approval evidence. Any transitional waiver must be explicit, narrowly scoped and approved by PGA once appointed.

**Approval Authority:** PGA; currently GOVERNANCE-OPEN.

## G1 — Domain & Ownership

**Entry Criteria:** G0 approved; module baseline submissions cite project baseline version; domain ADR inventory complete.

**Exit Criteria:** each module has approved ownership baseline; canonical domain object authority is unambiguous; non-owner write paths prohibited; Fact/Claim and typed-reference ADRs resolved by their declared authorities; consumers map exact semantics.

**Required Evidence:** owner decisions, ADRs, ownership matrix, schema compatibility analysis, negative unauthorized-operation tests or design-level proof where implementation is not yet in scope.

**Blocking Findings:** unresolved canonical authority, conflicting schemas, unapproved Fact/Claim or identity semantics, module self-approval of external authority.

**Waiver Policy:** no waiver of ownership ambiguity for protected canonical writes; only bounded migration exceptions under PGA + affected owners.

**Approval Authority:** relevant domain ADR authority and all affected Module Owners; A records coordination, not unilateral approval.

## G2 — Contract Closure

**Entry Criteria:** G1 accepted for affected domains; producer and consumer contracts enumerated with version and owner.

**Exit Criteria:** all P0/P1 contract blockers closed or formally excluded from release scope under approved waiver; exact wire/schema/version/ACK/reconnect and cursor/fence semantics aligned; no stale registry entries; compatibility and failure behavior specified.

**Required Evidence:** producer/consumer acceptance records, exact artifact/branch/commit SHAs, contract conformance vectors, migration/versioning plan, open-issue ledger.

**Blocking Findings:** ADR-BLOCKED fields, identity/permission ambiguity, D/E/Storage atomic publication gap, unproven Forget cross-owner mappings, incompatible cursors or state conflation.

**Waiver Policy:** only PGA plus all affected authority owners; security/Forget waiver requires I; no waiver may claim unresolved behavior is closed.

**Approval Authority:** authoritative producer and consumer Module Owners; A coordinates and records.

## G3 — Implementation

**Entry Criteria:** approved contracts and ADRs; implementation plan and ownership; reproducible build/test environment.

**Exit Criteria:** required code paths implemented; module tests pass; error, retry, idempotency, migration and recovery behavior covered; code reviewed; deviations recorded and approved.

**Required Evidence:** code commit SHAs, build logs, test IDs/results, coverage of critical transitions, review records and reproducible instructions.

**Blocking Findings:** missing core paths, unreviewed bypasses, failing critical tests, implementation diverges from contract, no evidence.

**Waiver Policy:** limited feature deferral only by release authority and affected owner; cannot waive security invariants or misrepresent unimplemented behavior.

**Approval Authority:** Engineering/Implementation Acceptance Authority plus relevant Module Owner; Verification Owner confirms evidence.

## G4 — System Conformance

**Entry Criteria:** G3 accepted; integrated candidate version; test fixtures and threat model ready.

**Exit Criteria:** end-to-end contracts pass; scope/auth negative tests pass; prompt-injection and untrusted-memory tests pass; Forget retry/replay/recompile/index/cache/context/reconnect/restore race matrix passes; concurrency and fault injection pass; audit evidence is complete.

**Required Evidence:** reproducible system test reports, fixtures, environment, commit IDs, fault-injection logs, security review and residual risk approvals.

**Blocking Findings:** any unauthorized disclosure/write, Forget resurrection, stale permission acceptance, untrusted instruction elevation, missing target proof or unreproducible test.

**Waiver Policy:** security and Forget residual risk only through explicit I recommendation and PGA + affected owners, with exact targets, expiry and compensating controls. A test failure cannot be waived into a pass.

**Approval Authority:** Verification Authority and affected owners; I for security; PGA for project-level residual risk.

## G5 — Operational Readiness

**Entry Criteria:** G4 accepted; deployment topology, SLOs, support and rollback plans documented.

**Exit Criteria:** performance/resource budgets met on representative hardware/workloads; deployment and upgrade/rollback validated; observability and alerting operational; backup/restore and Forget-after-restore drills pass; retention and incident processes staffed; operational ownership accepted.

**Required Evidence:** benchmark report, capacity plan, deployment/rollback runbook, dashboards/alerts, backup/restore drill, incident exercises, retention/erasure audit and on-call ownership.

**Blocking Findings:** unknown resource envelope, untested restore, missing observability, no rollback, unresolved operational owner or unacceptable residual risk.

**Waiver Policy:** only explicit release-scoped exception by operational authority and PGA; never waive truthful reporting or mandatory legal/security obligations.

**Approval Authority:** Operational Acceptance Authority; PGA for final product-level acceptance.

## Gate state discipline

Use only: PROPOSED, NOT ASSESSED, BLOCKED, CONDITIONAL, PASS, FAILED, SUPERSEDED. PASS must link to evidence and approver. A gate cannot be promoted because downstream documents assume it passed. Historical gate results remain immutable; corrections create a new assessment.
