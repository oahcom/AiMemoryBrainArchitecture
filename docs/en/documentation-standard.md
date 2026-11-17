# Bilingual Architecture Documentation Standard

- Standard ID: DOC-STD-001
- Version: 1.0
- Status: PROPOSED — requires Architecture Governance approval
- Applies to: every architecture, domain, protocol, security, engineering, decision, review and operational design artifact in this repository.

## 1. Normative rule

Every new or materially revised architecture/design artifact MUST have both an English and a Simplified Chinese edition in the same change set. Neither language is optional. Both editions carry the same document ID, semantic version, status, owner, source revision, decision state, issue references and normative force.

A change is not documentation-complete until both editions are updated, cross-linked and checked for semantic parity. A missing or materially stale translation is a review finding and blocks document acceptance where the change affects a contract, invariant, security rule, data model, protocol, decision or implementation requirement.

## 2. Canonical paths

- English: `docs/en/<domain>/<document-name>.md`
- Simplified Chinese: `docs/zh-CN/<domain>/<document-name>.md`
- Navigation: `docs/README.md` and its Chinese counterpart `docs/zh-CN/README.md`.

Existing source-owner documents and review reports remain preserved at their established paths. The bilingual documentation set is a reader-facing, linked edition; it does not silently replace or mutate owner branch artifacts.

## 3. Language and terminology

- English is the shared cross-owner terminology baseline for identifiers, protocol fields, code symbols, state names, enum values, error codes and schema names.
- Simplified Chinese is a complete technical edition, not a short summary. Preserve all requirements, qualifications, tables, examples, equations, error names, open issues and acceptance criteria.
- Keep normative keywords (MUST, MUST NOT, SHOULD, MAY), identifiers, code symbols, state names and exact field names unchanged where translation could alter interoperability.
- Maintain a project glossary for domain terms. Translate explanatory prose, but do not translate code identifiers or wire values.
- Avoid ambiguous literal translations; define a term once and use it consistently.

## 4. Required document metadata

Every edition MUST state: document ID; title; version; status (DECIDED/CANDIDATE/OPEN/ADR-BLOCKED/IMPLEMENTED/VERIFIED as applicable); owner; source path and exact source commit/blob; counterpart link; related ADR/issue IDs; last reviewed revision.

Do not claim implementation, test execution, performance measurement, external review or governance approval without evidence. Preserve the distinction between design decision, candidate proposal, open question, implementation and verified behavior.

## 5. Readability and structure

Use a stable outline where relevant:
1. Purpose and intended reader
2. Scope and non-responsibilities
3. Terms and domain model
4. Responsibilities and ownership boundaries
5. Architecture/components and dependencies
6. Data and state models
7. Interfaces/contracts
8. Invariants and security constraints
9. Normal flows and lifecycle
10. Failure/recovery and concurrency
11. Performance/resource assumptions and validation plan
12. Observability
13. Acceptance/conformance tests
14. Open decisions, dependencies and change history

Start each document with a short plain-language abstract and an explicit status. Explain why a component exists before detailing fields. Separate normative rules from rationale and examples. Expand acronyms on first use. Use tables for comparisons and ownership matrices; use sequence diagrams only when they clarify ordering or concurrency. Avoid unexplained acronym chains and giant paragraphs.

## 6. Cross-language parity checklist

Before review/merge, verify:
- same sections and requirement coverage;
- same MUST/MUST NOT/SHOULD/MAY force;
- same state transitions, field names, types, units and enum values;
- same ownership, dependency and interface boundaries;
- same failure modes, retry/idempotency and recovery behavior;
- same security/privacy/Forget semantics;
- same examples, tables, formulas and acceptance tests;
- same OPEN/DECIDED/ADR-BLOCKED status;
- links resolve within repository and both editions identify the same source revision.

Translation may improve explanation but MUST NOT add, weaken or remove a normative requirement. If a source is ambiguous or contradictory, record the ambiguity in both editions; do not silently resolve it during translation.

## 7. Change workflow

1. Author or revise the English and Chinese editions together.
2. Update metadata and source revision references.
3. Update the navigation index and glossary if needed.
4. Run link/path checks and cross-language parity review.
5. Ask the owning architect to confirm technical meaning; ask an independent reviewer for security/protocol/data-model changes.
6. Commit both editions and index updates in one coherent change.
7. Re-read the committed files and verify exact paths, commit and blob identities.
8. Only then report the documentation work as complete.

## 8. Exceptions

A temporary exception requires an explicit, time-bounded Architecture Governance decision with owner, rationale, affected documents, risk and remediation date. An English-only or Chinese-only document is otherwise non-conforming.

## 9. Acceptance

This standard itself remains PROPOSED until approved by Architecture Governance. Once approved, bilingual completeness becomes a repository-level review gate. It does not approve the technical content of any document, close ADRs, or establish implementation evidence.
