# Bilingual Architecture Documentation Governance / 中英双语架构文档治理规范

- Document ID: GOV-DOC-BILINGUAL-001
- Version: 1.0
- Status: **MANDATORY PROJECT GOVERNANCE BASELINE / 强制项目治理基线**
- Applies to: All architecture design, architecture changes, technical decisions, protocols, owner proposals, reviews, and acceptance artifacts in this repository.
- Language authority: Chinese and English are co-equal normative presentations. Neither language may silently weaken or strengthen the other.

## 1. Mandatory policy / 强制规范

**Every architecture design or architecture change MUST deliver synchronized Chinese and English documentation as part of the same change set.**

**每一次架构设计或架构变更，都必须在同一个变更交付中同步提供中文和英文文档。**

This requirement applies to, at minimum:
- System and subsystem architecture, component boundaries, responsibility assignments, and deployment topology.
- Domain models, entities, relationships, lifecycle/state machines, invariants, and data contracts.
- Protocols, schemas, wire formats, APIs, error semantics, compatibility rules, and examples.
- Storage, indexing, consistency, transactions, cursors, queues, recovery, and failure handling.
- Security, identity, authorization, privacy, retention, Forget, audit, and threat models.
- Technology choices, ADRs, Rust crate design, resource budgets, benchmarks, and operational procedures.
- Owner proposals, cross-owner reviews, integration decisions, change logs, test plans, conformance reports, and acceptance decisions.

This is not a translation-only task at the end of a project. Bilingual documentation is a first-class architecture deliverable and a required part of the design/review/acceptance lifecycle.

## 2. Required paired artifacts / 必须成对交付的文档

For every normative or architecture-significant document, provide:
1. A Chinese document.
2. An English counterpart.
3. A reciprocal link between the two.
4. The same Document ID and compatible semantic version.
5. The same source revision, decision status, scope, and review state.
6. A record in the documentation coverage register.

For substantial documents, use the repository's paired language structure under docs/zh-CN/ and docs/en/, preserving module/topic paths. Existing root-level Owner specifications may remain source specifications during migration, but they do not satisfy the bilingual requirement until reviewed paired versions exist.

Small code comments, identifiers, machine-generated logs, and source code symbols do not require duplicated bilingual syntax. Their user-facing or normative explanations do.

## 3. Same-change-set rule / 同一变更集规则

A design PR or architecture change is **not ready for review** if either language counterpart is missing or stale.

- Update both language versions in the same branch/PR/commit series.
- A reviewer MUST review semantic parity, not merely spelling or translation quality.
- If a source contract changes, its paired documents and affected glossary entries must change together.
- If a counterpart cannot be completed in the same change set, mark it STALE / 翻译待同步, identify the exact source revision, owner, and blocking reason. The change MUST NOT be accepted as a completed architecture baseline while a normative counterpart is stale.
- Emergency fixes may use a narrowly scoped exception only when explicitly approved by the responsible architecture authority, with a named owner and deadline. The exception does not waive the obligation to complete the counterpart.

## 4. Semantic parity requirements / 语义一致性要求

Chinese and English versions MUST have equivalent:
- Requirements and normative force (MUST, MUST NOT, SHOULD, MAY).
- Architecture meaning, component authority, ownership, trust boundaries, and non-goals.
- State machines, transitions, invariants, transaction/linearization semantics, and failure behavior.
- Schema fields, type names, enum values, protocol identifiers, error codes, version tokens, and examples.
- Decision status, unresolved questions, risks, caveats, limitations, and evidence claims.
- Acceptance criteria, test expectations, and implementation status.

Stable identifiers remain unchanged in both languages: paths, API fields, enum values, type/crate names, protocol constants, ADR IDs, issue IDs, and machine-readable tokens. Explanations may be translated; identifiers must not be renamed for linguistic convenience.

## 5. Decision-status preservation / 决策状态必须一致

The paired documents MUST preserve status exactly. Use the shared status vocabulary:

| Canonical status | 中文 | Meaning |
|---|---|---|
| DECIDED | 已决议 | Approved normative decision, supported by the required decision record. |
| RECOMMENDED | 推荐 | Preferred proposal, not necessarily approved. |
| CANDIDATE | 候选 | A possible design or technology; not binding or frozen. |
| OPEN | 未决 | Unresolved question or dependency. |
| BLOCKED | 阻塞 | An unresolved condition prevents progress or acceptance. |
| TO_VALIDATE | 待验证 | Requires specified prototype, benchmark, test, or evidence. |
| NOT REVIEWED | 尚未审查 | No review evidence is available. |
| STALE | 待同步 | This language version does not yet reflect the identified source revision. |

Translation MUST NOT promote or demote status. For example, CANDIDATE must not become “正式方案”; CONDITIONAL PASS must not become “通过”; NOT IMPLEMENTED must not become “已支持”.

## 6. Owner and reviewer responsibilities / Owner 与审查者责任

Every architecture Owner is responsible for:
- Producing or updating both language versions for their owned architecture artifacts.
- Keeping technical terms aligned with the shared glossary.
- Identifying source documents, exact revisions, and related ADR/issue references.
- Declaring unresolved translation questions rather than guessing.
- Reviewing the paired document after substantive changes.

Reviewers must check:
- Technical semantic equivalence.
- Completeness of constraints, negative requirements, failure cases, and security caveats.
- Stable identifier preservation.
- Status and evidence parity.
- Cross-links, diagrams, tables, and examples.

The integration authority checks repository-wide consistency and coverage. It does not replace the domain Owner's approval of domain semantics.

## 7. Readability requirements / 易读性要求

Bilingual compliance is not satisfied by literal word-for-word translation. Each version must be independently understandable.

Major documents SHOULD follow this progressive structure where applicable:
1. Purpose and one-sentence summary.
2. Scope and non-goals.
3. Responsibilities and non-responsibilities.
4. Context/component diagram.
5. Core concepts and terminology.
6. Main data/control workflows.
7. State machines and invariants.
8. Interfaces and dependencies.
9. Security/trust boundaries.
10. Failure and recovery.
11. Performance/resource constraints.
12. Acceptance criteria, decisions, and open questions.

Explain acronyms on first use. Introduce the reason for a mechanism before its implementation detail. Use concrete examples for subtle distinctions. Keep diagrams focused and explain them in prose. Do not hide important caveats in footnotes or one language only.

## 8. Review gates / 审查门禁

A bilingual architecture change passes documentation governance only when all applicable gates pass:

- **BG-1 Pairing:** Chinese and English artifacts exist and link to each other.
- **BG-2 Metadata:** Document IDs, versions, source revision, owner, and status are present and compatible.
- **BG-3 Semantic parity:** Requirements, state, constraints, examples, and evidence are equivalent.
- **BG-4 Terminology:** Terms match the shared bilingual glossary.
- **BG-5 Readability:** Each language is understandable without requiring the other language.
- **BG-6 Traceability:** ADRs, issues, source paths, commits, and review decisions are traceable.
- **BG-7 Validation:** Internal links, Mermaid diagrams, tables, and referenced artifacts are checked.
- **BG-8 Coverage register:** The documentation status register is updated.

Missing a mandatory gate means REQUEST CHANGES or BLOCKED, not a silent pass.

## 9. Documentation coverage register / 双语覆盖登记表

docs/translation-status.md is the repository-wide coverage register. It MUST be updated in the same change set when:
- A new architecture document is created.
- A document is materially revised.
- A paired translation is completed or becomes stale.
- A document is superseded, split, merged, or retired.

The register must distinguish COMPLETE, PARTIAL, NOT STARTED, STALE, and NOT APPLICABLE. A translated overview does not imply its detailed source specifications are translated.

## 10. Architecture workflow integration / 纳入架构开发流程

Every architecture task prompt and Owner kickoff MUST include this requirement:
- Read the bilingual governance policy and style guide.
- Identify the Chinese and English target paths before design begins.
- Produce both language versions in the same change set.
- Update the glossary and coverage register when needed.
- Submit a bilingual parity checklist with the Owner report.
- Do not mark the architecture deliverable complete while a mandatory counterpart is absent or stale.

The integration/release checklist MUST include the bilingual documentation gates. The same applies to architecture-only changes that do not modify code.

## 11. Exceptions and enforcement / 例外与执行

No Owner may waive this policy unilaterally for their own deliverable. An exception requires an explicit decision by the project integration authority, documented with:
- Reason and affected artifacts.
- Risk of proceeding with one language only.
- Responsible Owner.
- Due date and closure evidence.

Repeated or broad exceptions require a governance review. The default is no exception.

## 12. Scope and effective date / 适用范围与生效

This policy applies to all new work immediately after its approval into the repository's governance baseline. Existing English-only specifications enter the staged migration plan in docs/translation-status.md; they are not falsely represented as already bilingual.

Until each existing document is migrated, the current source specification and approved decision records remain authoritative for technical meaning. Its missing paired language version is a tracked documentation debt, not permission to omit bilingual delivery from new changes.

---
**English and Chinese are co-equal project documentation requirements. / 中英文是本项目同等强制的文档要求。**
