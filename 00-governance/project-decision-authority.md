# Project Decision Authority — AiMemoryBrainArchitecture

- Version: 0.1.0
- Status: **PROPOSED — GOVERNANCE-OPEN**
- Rule: roles below are authority classes, not assertions that a particular person or module currently occupies them.

## 1. Authority register

| Role | Authority / responsibility | Limits |
|---|---|---|
| Project Governance Authority (PGA) | Approves project mission/scope baseline, project redlines, exceptions, governance version and G0 | Identity and appointment are OPEN; must be explicitly designated by project sponsor/founder or documented governing body |
| Principal Integration Architect (A) | Maintains cross-module dependency map, compatibility matrix, integration findings and gate evidence coordination | Cannot approve another module's internal authority model or act as PGA by assumption |
| Module Owner (A–I and Storage) | Decides and maintains owned domain/interface semantics; proposes module baseline/redlines; accepts incoming/outgoing contracts within authority | Cannot alter project redlines, approve own project exception or take another module's authority |
| Security/Governance Owner (I) | Defines identity, authorization, delegation, revocation, retention, audit, Forget global policy and security risk recommendations | Cannot approve project baseline/redline changes or waive project redlines alone |
| ADR Decision Authority | Approves a specific ADR according to its declared owner(s), affected authority owners and governance policy | Must be recorded per ADR; no universal ADR authority inferred from A |
| Implementation Owner | Delivers code against approved contracts; reports deviations and implementation evidence | Cannot change normative contract by implementation convenience |
| Verification Owner | Defines/runs independent conformance, integration, security, performance and operational tests; records reproducible evidence | Cannot approve a design outside assigned authority; test pass does not itself approve project policy |

## 2. Current governance appointment

**GOVERNANCE-OPEN:** Repository evidence reviewed for this proposal does not establish a named Project Governance Authority, appointment mechanism, quorum, voting rule or delegated approval policy. The author/account of commits is not proof of governance appointment. A's Principal Integration Architect role does not imply PGA authority.

Required sponsor decision:
1. Name the PGA (person or formally constituted body).
2. Record appointment source, scope, term, successor/delegation and conflict-of-interest handling.
3. Define approval mechanism, quorum/vote threshold, tie-break and emergency procedure.
4. Identify who can ratify baseline/redline versions and waivers.
5. Publish the decision in this file or an authoritative governance charter, with evidence and date.

Until then all project governance artifacts remain PROPOSED; G0 cannot pass as formally approved.

## 3. Decision rights

| Decision/action | Propose | Decide / approve | Required consultation |
|---|---|---|---|
| Project baseline change | Any contributor; A coordinates impact | PGA | A and every affected Module Owner; I for security/privacy |
| Project redline change | Any contributor; I may raise security issue | PGA | All affected owners; I mandatory for security-related change |
| Project redline exception | Affected owner or I | PGA plus directly affected owners; I mandatory for security/Forget/privacy | Verification Owner and impacted consumers |
| Module internal authority model | Relevant Module Owner | Relevant Module Owner under approved project constraints and its ADR rules | A/consumers; I for security impact |
| Cross-module contract | Any affected owner | All authoritative producer/consumer owners; domain owner decides its owned semantics | A coordinates; I for security |
| ADR | ADR author/owner | Explicit ADR Decision Authority declared in ADR; unresolved authority => OPEN | A and affected owners |
| Integration Finding closure | Finding owner proposes | Finding's named authority owner(s), with evidence review; A records integration disposition | A coordinates; Verification Owner for test findings |
| Implementation acceptance | Implementation Owner submits | Designated technical/engineering acceptance authority plus relevant Module Owner | Verification Owner |
| Test/conformance acceptance | Verification Owner submits evidence | Designated Verification/Acceptance Authority and affected owners | A coordinates; I for security |
| Gate transition G0–G5 | Gate coordinator | Authority named for each gate in acceptance-gates.md; PGA for G0/project policy | Required owners and evidence reviewers |

## 4. ADR authority requirements

Each ADR must state: ID, question, owner, decision authority, consulted owners, options, constraints, decision, consequences, status, date, source branch/commit, supersession and consumer migration. For cross-module ADRs, every affected authority owner must explicitly accept its own boundary. If the decision authority is not named or a required owner has not accepted, status remains OPEN/ADR-BLOCKED. A registry or integration review records status; it does not create the decision.

## 5. No implied authority

- A is an integration coordinator, not presumed project sovereign.
- Module Owner decisions bind only the objects and contracts they own.
- I is security-policy owner, not sole project governance authority.
- Repository admin/write permission is not policy appointment.
- Commit authorship, review authorship, file existence and consensus inferred from silence do not constitute approval.
- This proposal itself cannot name its approver.

## 6. Change control

Changes to authority assignments require a governance change request, documented appointment evidence, impact review and PGA approval. Keep prior appointments and delegations in the audit history.
