# AI-REQTRACE-001 — GitHub Requirement Traceability Standard

- **Document ID:** AI-REQTRACE-001
- **Version:** 1.1
- **Status:** PROPOSED
- **Effective Date:** NOT_EFFECTIVE
- **Owner:** Project Owner (to be confirmed)
- **Maintainer:** Integration Owner (proposed)
- **Scope:** Repository-wide
- **Language:** English normative master
- **Companion:** AI-REQTRACE-001.zh-CN.md (semantic-equivalent edition)

## 1. Purpose

This standard establishes a GitHub-native mechanism for recording, identifying, managing and tracing long-term project requirements. It ensures that requirements do not exist only in conversations; each approved umbrella requirement has a stable GitHub identity; original intent remains preserved; execution is traceable through Work Items, child Issues, Pull Requests, commits and verification evidence; fulfillment is distinct from implementation activity; and duplicate carriers and unnecessary Issue/PR proliferation are prevented.

This standard introduces no independent database, custom orchestrator or script-based hard-blocking system. GitHub Issues, Pull Requests, repository documents, existing Work Item records and established workflows remain the authoritative operational infrastructure.

## 2. Normative Language and Adjudicated Decisions

MUST, MUST NOT, SHOULD, SHOULD NOT and MAY express requirement strength. AI-generated proposals do not constitute Owner approval. Registration, acceptance, execution and fulfillment are distinct.

The REQ-TRACE Phase 0 adjudication is binding and settled. This standard implements, and does not reopen, these seven decisions: (1) five requirement dimensions; (2) five fixed primary labels; (3) requirement lifecycle; (4) original evidence preservation; (5) PR reference semantics; (6) the bounded initial registration exception; and (7) separation of requirement and execution identities.

## 3. Authority and Parent Standards

This standard operates under existing governance and Owner authority. Relevant standards include AI-STD-001, AI-PROC-001, AI-EXEC-001, AI-EXEC-002, PR-GOVERNANCE-001, AI-ARCH-002, GOV-DOC-001 and AI-PROMPT-STD-001 where applicable.

If conflict is identified: preserve the authority hierarchy; record the conflict; do not silently supersede another normative document; submit it for Owner or authorized governance adjudication; and update affected standards through an auditable PR. This standard does not independently amend any parent standard.

## 4. Requirement Identity and Dimensions

### 4.1 Umbrella Requirement

An Umbrella Requirement is a durable, long-term project requirement representing a coherent direction, objective or user expectation that may require multiple execution units and deliveries. It is not a single implementation task, PR, AI session, temporary defect report or technical decision by itself.

### 4.2 Canonical identity

Each approved umbrella requirement MUST have one canonical GitHub Issue. The Requirement ID and Issue number jointly identify the requirement. The Requirement ID MUST remain stable when the Issue title or implementation changes. The Requirement ID identifies the enduring requirement; an AID identifies an execution unit; a session and prompt identify execution provenance. These identities MUST NOT substitute for one another.

An AID MUST reference the applicable Requirement ID and Issue number. A requirement MAY have multiple AIDs, child Issues and PRs; an AID or child Issue MAY contribute to multiple requirements. Every relationship MUST state its actual contribution; no artificial one-to-one mapping is required.

### 4.3 Five adjudicated dimensions

The initial five dimensions are fixed:
- REQ-01 — Risk Assessment
- REQ-02 — Technology Selection
- REQ-03 — PR Governance
- REQ-04 — Architecture Breakthrough
- REQ-05 — Documentation Management

These are requirement dimensions, not lifecycle states or execution tasks. Future dimensions are not created by relabeling this adjudicated initial set; any extension requires explicit Owner/governance authorization and an auditable change to this standard.

## 5. Fixed Primary Labels

The five fixed primary labels are exact:
- `requirement/risk`
- `requirement/tech-selection`
- `requirement/pr-governance`
- `requirement/architecture-breakthrough`
- `requirement/documentation`

Each umbrella requirement Issue MUST carry exactly one of these as its primary requirement-dimension label. The mapping is respectively REQ-01 through REQ-05 in the order listed above. Labels classify the requirement; they do not grant authority, establish acceptance or replace lifecycle status. Other non-dimension labels may be used where repository policy permits, but MUST NOT be treated as additional primary dimension labels.

## 6. Original Intent and Evidence Preservation

Every requirement Issue MUST contain an **Original Requirement Evidence** section. It MUST preserve supplied original user wording verbatim; identify the source conversation ID; record the original date when verified; use NOT_RECORDED when the date or complete source wording is unavailable; distinguish direct quotations from historical summaries; and preserve previous wording when the requirement contract is revised.

AI-generated summaries MUST NOT be presented as original user quotations. Corrected or expanded contracts MUST retain prior wording and record change history. Missing evidence MUST be disclosed, never reconstructed as a quotation.

## 7. Requirement Issue Structure

Each umbrella requirement Issue MUST contain: (1) Metadata; (2) Original Requirement Evidence; (3) Requirement Contract; (4) Intent and Expected Outcomes; (5) Scope and Exclusions; (6) Acceptance Criteria; (7) Current Requirement Status; (8) Related AID Work Items; (9) Related Child Issues; (10) Related Pull Requests; (11) Decisions and Evidence; (12) Change History; and (13) Governance Notes.

Unknown values MUST be explicitly marked NOT_RECORDED, NOT_CONFIRMED or NOT_ASSIGNED. Unknown information MUST NOT be fabricated.

## 8. Requirement Lifecycle

The supported requirement states are exactly: RECORDED, PROPOSED, ACCEPTED, ACTIVE, SATISFIED, DEFERRED, REJECTED and SUPERSEDED. Registration does not imply acceptance. Acceptance requires explicit Owner authorization. Activation requires an identifiable execution path. Satisfaction requires evidence and explicit Owner acceptance. Deferred requirements remain traceable and record a reason and resumption condition. Superseded requirements link to their replacement. Rejected requirements preserve historical intent and rejection rationale.

### 8.1 Explicit transition rules (v1.1 clarification)

The normal transitions are:
- NOT YET REGISTERED → RECORDED: canonical Issue and minimum metadata/evidence section created; this is registration only.
- RECORDED → PROPOSED: requirement contract and acceptance criteria drafted.
- PROPOSED → ACCEPTED: explicit Owner authorization recorded; or PROPOSED → REJECTED with Owner rationale.
- ACCEPTED → ACTIVE: accountable Owner and identifiable execution path recorded; or ACCEPTED → DEFERRED with reason and resumption condition.
- ACTIVE → SATISFIED: evidence linked and Owner acceptance explicitly recorded; or ACTIVE → DEFERRED with reason and resumption condition.
- DEFERRED → ACCEPTED or ACTIVE: resumption condition reviewed and Owner/authorized decision recorded.
- RECORDED, PROPOSED, ACCEPTED, ACTIVE or DEFERRED → SUPERSEDED: replacement Requirement ID/Issue and Owner rationale recorded.
- DEFERRED → REJECTED: Owner rejection rationale recorded.

No other transition is implied. A rejected or superseded requirement is terminal; correction requires a new auditable decision and, where materially new intent exists, a new requirement rather than silently reopening history. Reopening SATISFIED requires an explicit Owner correction record, evidence explaining why prior satisfaction no longer holds, and a recorded transition to ACTIVE or DEFERRED.

GitHub Issue open/closed status is a separate carrier lifecycle and MUST NOT substitute for requirement status. Closing an Issue does not itself mean SATISFIED; a closed carrier may continue to hold historical traceability.

## 9. Work Items and Child Issues

The requirement layer records long-term intent, scope, authority and fulfillment status. The Work Item layer records independently identifiable execution units, responsibilities, prompts, evidence and closeout. Existing AID conventions and canonical `work-items/INDEX.md` remain authoritative. An AID MUST reference its applicable Requirement ID and Issue number.

Child Issues record bounded decisions, investigations, defects and deliverables. A child Issue SHOULD identify its parent Requirement Issue, relevant AID, accountable role, expected output, acceptance criteria, dependencies and evidence requirements.

Relationships are many-to-many where appropriate. One requirement MAY have multiple AIDs and child Issues; one AID or child Issue MAY contribute to multiple requirements. State the actual contribution for each relationship.

## 10. Pull Request Traceability

### 10.1 Required references

Every substantive PR MUST identify its primary Requirement Issue; additional relevant Requirement Issues; related AID Work Item; related child Issue(s), where applicable; session and prompt identity under AI-EXEC-002; exact PR Head SHA; and verification/review evidence.

### 10.2 Reference semantics

Use `Refs #N` for umbrella Requirement Issues and for incomplete child Issues. Use `Closes #N` only for completed child Issues. A PR MUST NOT use automatic closing keywords (including `Closes`, `Fixes` or `Resolves`) against an umbrella Requirement Issue. References are traceability links, not lifecycle decisions.

### 10.3 Contribution and closure

A PR MUST explain the requirement it contributes to, concrete change, acceptance criterion addressed, supporting evidence and remaining work. PR merge MUST NOT automatically mark an umbrella requirement SATISFIED or close its canonical Issue. Requirement satisfaction requires the separate evidence and Owner acceptance in §8.

## 11. Anti-Proliferation and Initial Registration Exception

Before creating a requirement Issue, the creator MUST search for an existing canonical requirement. A new AI session, prompt version, PR, commit, routine subtask, discussion update or status transition MUST NOT create a new umbrella requirement. Reuse existing Issues and AID records.

A new requirement requires demonstrably distinct long-term intent, duplicate checking, defined scope, explicit Owner authorization and recorded rationale.

The initial five-issue historical registration set (REQ-01 through REQ-05) is a bounded, one-time exception to ordinary prospective registration/authorization sequencing, solely to register the five adjudicated historical dimensions and preserve their provenance. It does not waive canonical identity, evidence, exact primary labels or lifecycle recording; it does not authorize additional umbrella requirements, nor does it authorize unrelated Issue or PR proliferation. Any future requirement follows the normal authorization and duplicate-check process.

## 12. Integration with Existing Governance

### 12.1 AI-EXEC-001

Execution planning MUST identify the requirement being served before substantive work begins. Requirement identity supplements, and does not replace, Work Item identity.

### 12.2 AI-EXEC-002

Session identity MUST preserve existing Work Item ID, Prompt ID, Prompt Version and prompt-file commit SHA conventions. Requirement ID is an additional traceability dimension and MUST NOT replace any existing identity field.

### 12.3 PR-GOVERNANCE-001

PR-GOVERNANCE-001 governs PR creation, review, integration and merge evidence. This standard governs requirement identity and requirement-to-delivery relationships. They are complementary. Exact-Head checks, review independence, five dispositions and target-branch rules remain governed by PR-GOVERNANCE-001.

### 12.4 AI-ARCH-002, AI-PROC-001 and GOV-DOC-001

Architecture requirements and architecture decisions MUST remain distinct; a requirement does not authorize a specific architecture decision. Requirement identification, registration, refinement, execution, review and fulfillment SHOULD follow the established project process. This standard and its companion MUST follow existing documentation structure, manifest and bilingual semantic-parity requirements.

If any integration clause conflicts with an adopted parent standard, the parent authority hierarchy controls until an authorized adjudication resolves it.

## 13. Owner Authority and Decision Records

Only the designated authority may accept, reject or declare fulfillment of a requirement. AI sessions MAY propose scope, acceptance criteria, technical alternatives, execution plans and fulfillment evidence. AI sessions MUST NOT silently convert a proposal into an accepted decision.

Every material Owner decision MUST record the decision, authority, date, rationale, evidence, and affected requirements/documents.

## 14. Manual Operational Compliance

This standard is implemented through dispatch-header requirements, PR templates, GitHub Issue templates, AID registration conventions, Work Item index updates, human review and closeout. No script-based hard-blocking mechanism is assumed. GitHub native references and labels MAY be used. GitHub Projects MAY be used if adopted, but MUST NOT become the sole source of requirement truth.

The absence of platform-enforced controls MUST be disclosed accurately. Templates, labels, comments and AI self-review MUST NOT be represented as hard merge gates unless the live repository configuration proves enforcement.

## 15. Acceptance of This Standard

This document remains PROPOSED until Owner review, conflict resolution, review of required template/index changes, PR creation under existing governance, applicable exact-Head checks, required independent review and explicit Owner adoption are recorded. A merged document MUST NOT be represented as Owner-adopted without the applicable authority and evidence.

## 16. Initial Rollout

The initial rollout covers registration of the five historical umbrella requirements; preservation of supplied source wording and provenance; canonical Requirement IDs; primary labels; links to existing AIDs, Issues and relevant PRs; dispatch and PR template updates where separately authorized; Work Item index conventions; traceability audit; and recording unmapped historical work.

This standard's adoption PR does not itself authorize unrelated implementation PRs or automatically satisfy any umbrella requirement.

## 17. Change History

| Version | Status | Change |
|---|---|---|
| 1.0 | PROPOSED | Initial GitHub requirement traceability design (supplied baseline). |
| 1.1 | PROPOSED | Clarified the exact primary-label mapping; made lifecycle transitions explicit, including terminal/reopen handling; bounded the five-item historical registration exception; clarified that PR references never close umbrella requirements; and stated the non-substitution rule for Requirement IDs, AIDs and session/prompt identities. The seven Phase 0 adjudicated decisions are unchanged. |

## 18. Adoption Record

- Owner Decision: PENDING
- Decision Date: NOT_RECORDED
- Adoption Evidence: NOT_RECORDED
- Effective Date: NOT_EFFECTIVE
- Related PR: PENDING
- Bilingual Manifest: COMPLETE (paired edition supplied in this change; semantic review remains subject to independent review)
