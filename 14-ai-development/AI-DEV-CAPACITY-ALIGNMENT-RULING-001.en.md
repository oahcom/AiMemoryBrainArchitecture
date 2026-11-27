---
document_metadata:
  domain: ai-development
  role: decision-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "English rendering of AI-DEV-CAPACITY-ALIGNMENT-RULING-001.md; no independent bilingual parity review is recorded by this block."
    usage_status: Active
    modification_status: Active-Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# AI-DEV-CAPACITY-ALIGNMENT-RULING-001
# Capacity Alignment Ruling: Why Records Consume the Product

- Document ID: AI-DEV-CAPACITY-ALIGNMENT-RULING-001
- Source: [Canonical bilingual source](AI-DEV-CAPACITY-ALIGNMENT-RULING-001.md)
- Source Blob: `e2e931db93f2c019eba6fc21fc2e441218f2e061`
- Translation status: DRAFT — semantically equivalent rendering; the Chinese source remains authoritative
- Version: 1.0
- Status: PROPOSED — pending adoption by the Project Owner or an explicitly authorized governance authority; this record does not assert adoption
- Ruling authority: user-authorized operator (delegated by the account owner), drafting under AID-2026-287; repository-wide normative effect still requires Owner adoption
- Ruling date: 2026-11-27
- Measurement baseline: `main` @ `6306a858`
- Tracking: AID-2026-287 · Issue #1341 · Issue #1349
- Relationship: INTERPRET — interprets the strength allocation of record obligations; amends no upstream normative text
- Review-by: 2026-12-27

---

## 1. Context

This section records only the observations rechecked against `main` at commit `6306a858` on `2026-11-27`. The measurement scope, commands, or classification criteria are stated for each item. No figures, ratios, or inferences outside the six groups of measured facts are introduced here.

### 1.1 Commit Distribution

A total of 3,272 commits were observed in the most recent 30-day window on the `main` branch. They were classified by the top-level paths touched by each commit:

| Top-level path or category | Commit count | Share or recorded value |
|---|---:|---:|
| `14-ai-development` record-class changes | 1,382 | 42% |
| merge/empty commits | 559 | — |
| `.github` + `scripts` | 389 | 12% |
| `docs` | 349 | 11% |
| Architecture chapters | 255 | 8% |
| `crates/` | 201 | 6.1% |
| Other | 137 | — |

Measurement method: the population consists of commits in the most recent 30 days on `main`, classified according to the top-level paths touched by each commit. Merge/empty commits were classified separately and were not assigned to business-code or record-class paths. The counts and percentages above reproduce the baseline remeasurement; they are not recalculated.

### 1.2 Issue Reference Coverage

The baseline contains 168 open issues.

The following eight P0 authorization issues:

- #1128
- #1129
- #1132
- #1133
- #1134
- #1136
- #1138
- #1139

have zero commit references during the most recent 60 days.

Measurement commands:

```bash
git log --grep="#1128" --since="60 days ago"
git log --grep="#1129" --since="60 days ago"
git log --grep="#1132" --since="60 days ago"
git log --grep="#1133" --since="60 days ago"
git log --grep="#1134" --since="60 days ago"
git log --grep="#1136" --since="60 days ago"
git log --grep="#1138" --since="60 days ago"
git log --grep="#1139" --since="60 days ago"
```

Each command returned an empty result.

The zero-reference observation refers only to issue identifiers matched in commit messages by `--grep`. It does not imply that the issues had no comments, discussions, or other forms of activity.

### 1.3 Normative Corpus Membership

The membership sets of the root-level architecture chapters and `docs/en` differ. The measured set relationships are:

| Chapter | Root-level member count | Shared members with English directory |
|---|---:|---:|
| 01 | — | 8 of 11 shared-set members |
| 03 | — | 6 of 13 shared-set members |
| 04 | 43 | Shared-member count not separately provided |
| 06 | 26 | Shared-member count not separately provided |
| 08 | 106 | Shared-member count not separately provided |

The corresponding English-directory member counts are 13 for chapter 04, 12 for chapter 06, and 5 for chapter 08.

Cross-language document-pair measurements:

- Of 169 en/zh document pairs, only 1 pair was byte-for-byte identical.
- There are 11 content-duplicate groups across the repository.

Measurement method: compare the file membership sets of root-level chapters and `docs/en`, compare paired en/zh files by content, and identify repository-wide content-duplicate groups. Membership overlap does not imply content identity, and a content-duplicate group does not imply that the normative corpus membership sets are identical.

### 1.4 Gate Negative Cases and Target Base

Two existing gates have the following implementations.

**`repository-hygiene.yml:65-79`**

Its negative-case assertion requires only:

```text
status > 1
```

Consequently, even if a checker accepts a known-bad commit, the negative-case test can remain green as long as the returned status satisfies that assertion.

**`document-management.yml:36-46`**

Its validation uses:

```text
github.event.pull_request.base.sha
```

rather than the actual target base of the merge candidate.

Measurement method: inspect the negative-case status assertion and base SHA data source at the specified workflow lines. A green workflow result is not treated as equivalent to proof that a checker can reject erroneous input.

### 1.5 End-to-End Execution Chain

The repository contains the following executable tests:

```text
crates/brain-cli/tests/e2e_full_chain.rs
crates/brain-cli/tests/e2e_full_pipeline.rs
```

These tests connect all 12 crates.

Measurement method: inspect the above test files and their end-to-end call chains to establish that an executable cross-crate verification mechanism exists in the repository. This fact does not mean that the authoring session ran these tests or obtained CI execution results.

### 1.6 Product Phase and Exit Criterion

The README states that the product-grade runtime has not yet started.

The ROADMAP places prototype/implementation in Phase 5, the final phase.

The ROADMAP's Phase 3 exit criterion is:

> Every component has a bounded purpose, ownership, contract, and open questions.

Measurement method: inspect the product-grade runtime status statement in the README and the phase definitions and exit descriptions for Phase 3 and Phase 5 in the ROADMAP. This item records the current statements and criteria in those files; it does not infer any deployment state that is not documented.

---

## 2. Diagnosis

### 2.1 Primary Cause: Record Obligations Are Not Risk-Tiered and Therefore Have No Capacity Ceiling

The existing governance practice places changes with different risk levels, impact scopes, and degrees of reversibility into a largely uniform record-production mechanism. Whether a record is required, how complete it must be, and whether it must independently repeat existing information are not governed by an executable proportional relationship to change risk.

Causal chain:

1. Record obligations are not differentiated by risk level.
2. Low-risk, reversible, localized changes carry a record burden similar to that of high-risk, authorization-sensitive, cross-system changes.
3. Record production cannot naturally decrease as risk decreases, and it has no demonstrable stopping condition.
4. Every record-compliance activity can continue generating new files, revisions, and reference relationships.
5. Record production therefore creates a persistent capacity demand that is not bounded by risk.
6. When commit capacity is limited, record-related work can continue occupying commit and review resources without a corresponding mandatory capacity guarantee for product implementation.

This explains why records consume the product: the problem is not that records have no value. It is that record obligations are institutionally unbounded, while product implementation is placed in a later phase and has no executable priority constraint when competing for resources.

The commit distribution in 1.1 directly observes this pattern. The absence of commit references to P0 authorization issues in 1.2 is another observation of the lack of an effective execution link between authorization-sensitive matters and commit activity.

### 2.2 Second Cause: A Split Normative Corpus Creates a Mirror-Maintenance Tax

The root-level architecture chapters and `docs/en` do not form corpus membership sets that are identical. Language-paired documents are also not byte-level mirrors.

Causal chain:

1. The root-level and English directories have different membership sets.
2. Different sets mean that normative coverage, file existence, and maintenance boundaries cannot be inferred from a simple mirror relationship.
3. Cross-language content also cannot be shown to be synchronized merely by relying on byte equality.
4. Every normative change requires additional judgments about which files correspond, which files are independent, and which content has diverged.
5. Maintainers must continuously handle cross-directory and cross-language mapping and consistency issues in addition to the normative content itself.
6. This additional maintenance generates further records, difference explanations, duplicate references, and coordination commits.
7. Normative maintenance expands from content governance into mirror-relationship governance, continuously consuming capacity that could otherwise support product work and executable verification.

This is not merely a duplicate-file problem. Section 1.3 explicitly shows that normative corpus membership is split and that only a limited number of language pairs are byte-identical. Deleting duplicate files alone therefore cannot resolve the questions of membership sets and normative authority boundaries.

### 2.3 Third Cause: Gates Cannot Prove Failure, So Rulings Depend on Documentary Self-Assertion

A negative test case does not, by itself, establish that a gate can reject incorrect input. A gate must prove that it produces the expected rejection for a known erroneous input, rather than merely proving that a process returned a non-zero status.

Causal chain:

1. The negative-case assertion in `repository-hygiene.yml:65-79` checks only `status > 1`.
2. That assertion does not prove that the tested checker rejected a specific known-bad input.
3. `document-management.yml:36-46` also does not use the actual target base of the merge candidate.
4. The existing test structures of both gates fail to establish a complete evidence chain of “erroneous input → correct target base → checker rejection → gate failure.”
5. A green gate cannot serve as sufficient evidence of checker effectiveness.
6. Governance rulings cannot reliably depend on automated execution results and therefore continue relying on documents, summaries, and manual self-assertion.
7. To compensate for insufficient execution evidence, the organization continues producing explanatory records instead of replacing explanatory proof with executable counter-verification.

The end-to-end tests in 1.5 are particularly important: the repository already has an executable verification mechanism spanning all 12 crates. The current problem therefore cannot simply be attributed to the absence of a technical foundation for execution-based verification. The problem is that governance rulings still rely on documents and summaries rather than making executable counter-evidence a valid basis for decisions.

### 2.4 Fourth Cause: The Phase 3 Exit Criterion Is Not Executable and Therefore Fails to Establish a Stage Boundary

The Phase 3 exit criterion describes documentation attributes of components rather than defining an executable determination with explicit pass and failure conditions.

Causal chain:

1. The criterion requires components to have a bounded purpose, ownership, contract, and open questions.
2. These attributes can continue to be expressed by adding explanations, supplementing ownership descriptions, and elaborating contract text.
3. The criterion does not specify which executable behaviors or verification results must exist, nor what observation constitutes failure.
4. Consequently, even when the product-grade runtime has not started, the documentary conditions of Phase 3 can continue to be satisfied or re-described.
5. Phase 3 ceases to function as an effective exit boundary between architectural description and product implementation.
6. Prototype/implementation remains in Phase 5, while product implementation lacks a mandatory stage constraint when competing with further documentation work.
7. Records and architectural descriptions can continue expanding while product implementation remains institutionally deferred.

The issue is not that the documentary attributes of Phase 3 have no value. It is that documentary attributes alone cannot prove that a system possesses the executable capabilities required to enter the implementation stage.

### 2.5 Causal Ordering and Mutual Reinforcement

The causes above are ranked by their explanatory power regarding capacity allocation:

1. **Unbounded record obligations:** directly create persistent, unbounded demand for record-production capacity.
2. **Split normative corpus:** makes record obligations additionally carry the maintenance cost of mirror relationships.
3. **Gates that cannot prove failure:** make records a substitute form of proof when execution evidence is insufficient.
4. **Non-executable phase exit criterion:** allows records and architectural descriptions to continue substituting for implementation-stage results.

These causes are not mutually exclusive. They reinforce one another.

A1 limits the conditions that generate record burdens; A2 limits the objects and authority boundaries of normative maintenance; A3 prevents documentary self-assertion from substituting for executable verification; and A4 prevents continued documentation from substituting for stage exit into implementation.

This diagnosis does not claim that the number of records proves that every record lacks value. Nor does it claim that reducing the number of records will necessarily produce a product. It asserts that the current mechanisms do not demonstrate proportionality between record burden and risk, do not demonstrate that gates can reject erroneous input, and do not demonstrate that the product phase has obtained entry through executable conditions.

---

## 3. Rulings A1–A4

The following four rulings are proposed for adoption. Because this document is in PROPOSED status, none of these rulings automatically changes the repository's current normative requirements before adoption by the Owner or an explicitly authorized governance authority.

### A1. Record-Obligation Tiering by Risk

#### Decision

For work items, decision records, evidence, session evidence, and review roles covering architecture, governance, authorization, implementation, and documentation changes within `14-ai-development`, record obligations must be tiered according to change risk, impact scope, reversibility, and authorization sensitivity. Low-risk, localized, reversible changes must not automatically inherit the full record burden of high-risk changes. Authorization-sensitive, cross-boundary, high-impact, or irreversible changes must not be exempted from necessary evidence merely because record burdens are reduced. This ruling does not alter mandatory record obligations explicitly imposed by upstream normative requirements and does not replace any authorization requirement.

#### Rationale

Section 1.1 shows that record-class commits in `14-ai-development` occupy a substantial share of commit capacity.

Section 1.2 shows that P0 authorization issues have no corresponding commit references within the measured window.

The causal chain in 2.1 explains that a uniform record burden can consume excessive capacity for low-risk changes while failing to ensure effective execution for high-risk matters.

Therefore, record volume cannot serve as a substitute measure of governance quality; record intensity must correspond to risk.

#### Alternatives considered and rejected

**Alternative 1: Continue applying the same comprehensive record requirements to all changes.**

Rejected because uniform requirements do not reflect differences in risk. They cannot explain why low-risk changes must bear the same record costs as high-risk changes, and they provide no capacity ceiling for record production.

**Alternative 2: Eliminate or minimize all record obligations.**

Rejected because this would reduce the obligations of high-risk authorization, irreversible changes, and cross-boundary changes together with ordinary localized changes. It would undermine necessary traceability and would not resolve the lack of an effective execution link for P0 authorization matters.

**Alternative 3: Determine record tiers solely by commit count.**

Rejected because commit count is not risk itself. A small change may involve high-risk authorization, while a large change may be a low-risk mechanical adjustment.

#### Consequences

Upon adoption, newly occurring changes must not automatically bear an undifferentiated comprehensive record burden merely because they belong to a particular document type.

The default evaluation that “more records means better governance” must be abandoned.

The assumption that every work item must use the full documentation structure regardless of risk must be abandoned.

Necessary evidence obligations for high-risk changes must nevertheless remain. Risk tiering cannot be interpreted as a general exemption.

Historical records do not automatically become invalid under this ruling, nor do they automatically receive a retroactive violation finding because their records were either excessive or insufficient.

#### Falsifier

Within the scope of this ruling, if an independent risk classification of all new changes across one complete review window shows that changes at every risk level still bear exactly the same mandatory record requirements, with no observable difference in record burden for low-risk changes, then A1's ruling that risk tiering can establish boundaries for record obligations is falsified.

The observation must cover change risk levels, actual mandatory record fields, and record production. A normative statement declaring that tiering exists, without observable implementation, is not sufficient evidence of compliance.

### A2. Single Normative Source

#### Decision

For architecture, governance, and process specifications and their Chinese and English expressions, each normative requirement must have one identifiable source of normative authority. Other language versions, publication copies, navigation pages, and explanatory materials must not automatically acquire independent normative authority merely because their content is similar or their paths correspond. This ruling does not require deletion of existing language files, does not require all language files to be byte-identical, and does not alter explicitly authorized independent normative scopes.

#### Rationale

Section 1.3 shows that root-level and `docs/en` membership sets differ, that only 1 of 169 en/zh pairs is byte-for-byte identical, and that the repository contains 11 content-duplicate groups.

Section 2.2 explains that differences in membership sets and language content jointly create mapping, synchronization, and authority-identification costs.

What must therefore be unified is the source of normative authority, not the content of every file or the entire directory structure.

#### Alternatives considered and rejected

**Alternative 1: Require all Chinese and English files to remain byte-for-byte identical.**

Rejected because semantic equivalence between language texts does not require byte identity. This approach also fails to resolve differences in corpus membership and normative coverage.

**Alternative 2: Allow root-level and `docs/en` files to serve as independent normative sources.**

Rejected because the same subject may then have different versions, membership, and normative boundaries. Maintainers cannot determine final authority from the path alone.

**Alternative 3: Immediately delete all duplicate or non-mirrored files.**

Rejected because a duplicate group does not mean that every file is a redundant copy, and different membership sets do not mean that one directory can be deleted as a whole. Deletion must be determined by the normative identity and dependency relationships of each specific document.

#### Consequences

Upon adoption, newly created or modified normative requirements must not acquire independent normative authority merely through their language directory, filename, or content similarity.

The default practice of independently maintaining the same normative authority in multiple directories must be abandoned.

Byte equality must be abandoned as the sole criterion for cross-language normative consistency.

Chinese and English texts may retain natural-language differences, but their normative source and correspondence must be identifiable.

Existing files are not automatically deleted because their membership sets differ, nor do they automatically lose authority because their content is duplicated. Their historical status is interpreted according to the normative relationships in effect when they were created.

#### Falsifier

Within the scope of this ruling, if any newly published or revised normative requirement, without explicit independent authorization, is cited by two different files as independent and equally authoritative normative sources during a complete review window, then A2's ruling that a single normative authority can eliminate dual normative authority is falsified.

The determination must be based on document declarations, normative references, and their authorization relationships, not on whether file bytes are identical.

### A3. Every Gate Must Prove It Can Fail

#### Decision

For governance checkers and their required status checks under `.github/workflows/` and `scripts/`, every gate must have a known negative sample appropriate to its checking purpose and must demonstrate that the checker rejects that sample under the correct target base and merge-candidate context. Merely demonstrating a non-zero process status, successful workflow execution, or a green required context does not constitute proof of gate effectiveness. This ruling does not require every ordinary unit test to become a required check and does not change the authorization authority's power to approve gate scope.

#### Rationale

Section 1.4 shows that the negative-case assertion in `repository-hygiene.yml:65-79` checks only `status > 1`, while `document-management.yml:36-46` uses the PR base SHA rather than the actual target base of the merge candidate.

Section 1.5 shows that the repository already has executable end-to-end tests connecting all 12 crates.

Section 2.3 explains that when gates cannot prove failure, green results cannot support governance rulings, and documentary descriptions become substitutes for insufficient execution evidence.

Therefore, the minimum proof obligation for a gate must change from “successful execution” to “demonstrated rejection of known erroneous input.”

#### Alternatives considered and rejected

**Alternative 1: Require only that gates run successfully and produce green status.**

Rejected because successful execution proves only that the execution process completed. It does not prove that the checker rejected erroneous input.

**Alternative 2: Test only whether a script exits with a non-zero status.**

Rejected because arbitrary errors, missing arguments, or internal exceptions may all produce non-zero status. This result cannot distinguish expected rejection from unexpected failure.

**Alternative 3: Continue using manual document and summary reviews as the primary proof of gate effectiveness.**

Rejected because manual descriptions cannot replace end-to-end verification against the actual target base, merge candidate, and known erroneous input. The repository already has an executable testing chain, so documentary self-assertion should not be treated as stronger evidence.

#### Consequences

Upon adoption, a checker without evidence of known-negative-sample rejection must not be considered proven effective solely because its required context is green.

The practice of declaring a negative-case test effective merely because `exit code != 0` must be abandoned.

The assumption that a PR base SHA is automatically equivalent to the actual target base of a merge candidate must be abandoned.

Proof of gate effectiveness must establish a reviewable relationship among the input, target base, checker response, and expected failure result.

This ruling does not mean that all historical green statuses automatically become invalid, nor does it mean that every gate without completed negative-sample proof has already been formally revoked.

#### Falsifier

Within the scope of this ruling, if a required gate declared compliant with this ruling returns success for a known erroneous negative sample that it declares it must reject, and allows that negative sample to receive a passing status during independent retesting, then A3's ruling that a gate can prove its failure capability through negative samples is falsified.

Retesting must use the actual merge-candidate target base applicable to that gate. A failure result obtained using a different base SHA does not rule out an incorrect target base.

### A4. Phase 3 Exit as an Executable Checklist

#### Decision

For the Phase 3 exit criterion in the ROADMAP and the components, architecture, and product capabilities it covers, Phase 3 exit must consist of observable, executable, and reviewable acceptance conditions. Documentation attributes such as a bounded purpose, ownership, contract, and open questions may remain necessary descriptive conditions, but they must not independently constitute sufficient conditions for phase exit. This ruling does not determine when Phase 5 starts and does not equate phase exit automatically with the release of a product-grade runtime.

#### Rationale

Section 1.5 shows that the repository already contains end-to-end tests connecting all 12 crates.

Section 1.6 shows that the README states that the product-grade runtime has not started, that prototype/implementation is placed in Phase 5, and that the Phase 3 exit criterion centers on component documentation attributes.

Section 2.4 explains that an exit criterion based solely on documentation attributes cannot prove executable capability and therefore cannot establish an effective phase boundary.

Therefore, Phase 3 exit must be determinable through actual behavior or repeatable verification results, rather than depending solely on whether component descriptions are complete.

#### Alternatives considered and rejected

**Alternative 1: Retain the existing Phase 3 exit criterion and add more documentation fields.**

Rejected because adding documentation fields does not improve the falsifiability of the criterion. It may instead expand the record burden further.

**Alternative 2: Remove the Phase 3 exit condition entirely.**

Rejected because removing the exit condition would eliminate the explicit boundary between the architecture stage and the implementation stage. It would not resolve the lack of a verifiable entry condition for product implementation.

**Alternative 3: Equate Phase 3 exit with Phase 5 product release.**

Rejected because phase exit and product release are different determinations. The former proves that the stage's results meet the conditions for entering the next stage; the latter additionally involves product runtime and release status.

#### Consequences

Upon adoption, complete component documentation alone cannot serve as evidence that Phase 3 has exited.

The practice of treating “every component has a bounded purpose, ownership, contract, and open questions” as the sole sufficient exit criterion must be abandoned.

Documentation attributes must remain available as architecture governance evidence, but they cannot substitute for end-to-end behavior, interface-contract verification, or other executable acceptance results.

Existing ROADMAP phase records are not retroactively declared incorrect under this ruling. Their historical exit conclusions are interpreted according to the criteria in effect at the time.

#### Falsifier

Within the scope of this ruling, if Phase 3 is formally declared exited while the exit record relies only on documentation attributes and contains no repeatably executable behavioral acceptance or test result as necessary evidence, then A4's ruling that Phase 3 exit must have executable criteria is falsified.

The determination must be based on the actual exit record and its cited acceptance evidence. Merely having end-to-end test files, without incorporating their results into the exit determination, does not satisfy the condition.

---

## 4. Consequences

### 4.1 Short-Term Capacity Effects

Upon adoption of this record, record-class output will decrease in the short term. This is an expected direct consequence of risk tiering and a single normative source, not a goal of reducing file counts for their own sake.

The reduction primarily concerns:

- Comprehensive records repeatedly generated for low-risk, localized, reversible changes.
- Duplicate explanations produced to maintain mirror relationships between multiple directories.
- Explanatory records that merely describe a gate's execution without proving its effectiveness.
- Expanded component descriptions produced solely to satisfy documentation-based phase exit criteria.

The reduction does not apply to necessary authorization evidence, evidence for irreversible changes, genuine execution-failure evidence, or reviewable acceptance results.

This record does not claim that reduced record production will automatically convert commit capacity into product implementation capacity. Whether released capacity actually becomes product implementation must be determined through observable code, test, and runtime behavior.

### 4.2 Practices Outside the New Boundary

Upon adoption, the following newly occurring practices are outside the permitted boundary:

1. Imposing the same comprehensive record burden on every change without distinguishing change risk.
2. Allowing multiple files to serve as independent normative authorities for the same requirement without explicit independent authorization.
3. Treating a non-zero process exit or green workflow status as sufficient proof that a checker can reject erroneous input.
4. Treating complete component documentation fields as the sole sufficient evidence for Phase 3 exit.
5. Substituting additional explanatory documents for executable erroneous-input verification and end-to-end behavioral verification where those forms of verification are available.

These determinations apply to behavior occurring after this record takes effect. Whether historical files constituted violations at their historical points in time remains governed by the upstream requirements and authorization relationships then in effect.

### 4.3 Reinterpretation of Historical Records

Upon adoption, existing records must be interpreted according to the following criteria:

- Record volume reflects historical record-production activity; it does not automatically equal governance quality.
- A file's presence in the root directory or English directory does not automatically prove its normative authority.
- Identical or different en/zh content does not automatically prove semantic equivalence or non-equivalence.
- A historical workflow pass does not automatically prove that its checker could reject known erroneous input.
- Complete historical Phase 3 documentation does not automatically prove the existence of executable phase-exit evidence.
- The existence of historical end-to-end test files does not automatically prove that the corresponding tests were run, passed, or were used in governance rulings.

Historical records must not be retroactively deleted, rewritten, or declared invalid solely because they do not conform to the new interpretive criteria in this record.

### 4.4 Effective Boundary

This record's governance interpretation applies to newly occurring behavior only from the date it is adopted by the Project Owner or an explicitly authorized governance authority.

Before adoption, this document has only PROPOSED decision-record status. It does not constitute a repository normative change, alter required checks, revoke existing authorization, or change the canonical status of any existing file.

This record has no automatic retroactive effect.

---

## 5. Falsifiers

The following table consolidates the independent falsification conditions for each ruling. The observation window describes the scope required for a valid counter-observation; it is not a project schedule.

| Ruling ID | Falsifying observation | Observation window | Adjudicator |
|---|---|---|---|
| A1 | After independent risk classification, all new changes at different risk levels still bear exactly the same mandatory record requirements, with no observable difference in record burden for low-risk changes. | One complete review window covering all applicable new changes within that window. | Independent reviewer |
| A2 | Any new normative requirement is cited by two different files as independent and equally authoritative normative sources without explicit independent authorization. | One complete normative publication and revision review window. | Owner or independent normative reviewer |
| A3 | An independent retest shows that a required gate declared compliant accepts a known erroneous negative sample that it is supposed to reject, using the correct merge-candidate target base, and grants that sample a passing status. | One complete independent negative-sample retest. | Independent gate reviewer |
| A4 | Phase 3 is formally declared exited, but its exit record contains only documentation-attribute evidence and no repeatably executable behavioral acceptance or test result as necessary evidence. | One complete Phase 3 exit review. | Owner or independent phase acceptance reviewer |

Falsification conditions and compliance conditions must be understood separately:

- The absence of a falsification result does not prove that implementation of a ruling is effective.
- Failure to observe a violation does not constitute sufficient positive verification.
- If the required observation data cannot be obtained, the determination must be NOT_VERIFIED rather than automatically passing.
- Falsification must cite actual behavior, execution results, or verifiable normative authority relationships; summary statements alone are insufficient.

---

## 6. What This Record Does Not Decide

### 6.1 Final Risk-Tiering Thresholds

This record does not determine the final names of the risk levels under A1, their numerical thresholds, classification algorithms, or the specific field set required for each level.

Decision authority belongs to the Project Owner or an explicitly authorized governance specification authority. The decision vehicle is a formal governance specification or an authorized normative revision record.

### 6.2 P0 Authorization Implementation

This record does not determine the specific authorization implementation methods, state transitions, permission models, data structures, or security-control designs for #1128, #1129, #1132, #1133, #1134, #1136, #1138, and #1139.

Decision authority belongs to the Project Owner, the authorization authority specified by the relevant issue, or an explicitly designated security governance authority. The decision vehicle is the corresponding issue, authorization specification, and formal decision record.

This record only states that these issues had no commit references during the specified measurement window. It does not infer their final authorization solutions.

### 6.3 Deletion or Retention of Existing Documents

This record does not decide to delete any root-level files, `docs/en` files, content-duplicate groups, or historical records. Nor does it decide to migrate all existing files to a new directory structure.

Decision authority belongs to the Owner responsible for the relevant normative scope or an explicitly authorized documentation governance authority. The decision vehicle is a normative identity determination for the relevant document and its formal change record.

### 6.4 Phase 5 Start Date

This record does not determine when Phase 5 starts, the release order of prototype/implementation, the release date of the product-grade runtime, or its release conditions.

Decision authority belongs to the Project Owner or a product governance authority formally authorized to make phase decisions. The decision vehicle is a formal phase decision record in the ROADMAP.

### 6.5 Staffing and Capacity Allocation

This record does not determine personnel counts, individual responsibility assignments, team organization, time allocation, resource budgets, or execution schedules.

Decision authority belongs to the Project Owner and organizational management roles with the corresponding resource-allocation authority. The decision vehicle is a formal organizational resource decision or project governance record.

### 6.6 Concrete Directory Structure for the Single Normative Source

This record does not determine the specific directory in which the single normative source must reside, nor does it determine whether Chinese or English has priority as the authoring language.

Decision authority belongs to the Project Owner or an explicitly authorized normative architecture authority. The decision vehicle is a normative directory-structure decision and bilingual publication rule.

### 6.7 Concrete Gate Implementation Technology

This record does not determine the negative-sample framework, testing tools, CI job topology, required context names, or specific workflow implementation required by A3.

Decision authority belongs to the governance authority authorized to define repository CI and gate requirements. The decision vehicle is a formal CI governance specification and the corresponding workflow change record.

This record determines only that gate effectiveness must be demonstrable through known erroneous negative samples. It does not prescribe a single technical implementation.

### 6.8 Concrete Phase 3 Acceptance Items

This record does not determine the final items in the executable checklist required by A4, the test scope for each component, performance thresholds, runtime deployment conditions, or acceptance tools.

Decision authority belongs to the Project Owner or an architecture and product governance authority authorized to determine phase acceptance. The decision vehicle is the formal ROADMAP phase-exit standard and corresponding acceptance record.

### 6.9 Existing Normative Validity

This record does not determine whether any existing normative requirement violated the upstream requirements in effect when it was created. It does not retroactively revoke historical approvals, merge results, or authorization decisions.

Decision authority belongs to the Project Owner or an explicitly authorized governance authority with the corresponding normative interpretation and revocation powers. The decision vehicle is an independent normative-conflict ruling or revocation record.

---

## 7. Evidence and Provenance

### 7.1 Measurement Baseline

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Branch: `main`
- Baseline commit: `6306a858`
- Measurement date: `2026-11-27`
- Commit window: most recent 30 days
- Issue-reference window: most recent 60 days
- Measurement methods: classify commits by touched top-level path; inspect issue identifiers in commit messages using `git log --grep`; compare normative corpus file membership sets and file contents; inspect negative-case assertions and base SHA sources at the specified workflow lines; inspect end-to-end test files for the cross-crate execution chain; inspect README and ROADMAP for product-phase declarations and exit criteria.

### 7.2 Evidence Scope

The factual basis of this record is limited to the six groups of measurements listed in Section 1.

The following are not treated as verified facts:

- Other commit statistics not listed here.
- Issue comments, discussions, or review records not listed here.
- CI execution results not listed here.
- End-to-end test execution results not listed here.
- Runtime deployment or product-release states not listed here.
- Owner written approvals or normative adoption results not listed here.
- Independent remeasurement results not listed here.

This record does not equate the existence of a file with test execution, a green workflow with gate effectiveness, or complete documentation with product-phase exit.

### 7.3 Authoring Session Provenance

This document was drafted by an AI authoring session based on the measured facts and explicit writing constraints supplied by the user.

No independent second-party review evidence is available to this session.

This session has no recorded independent verification of all repository bytes.

This session does not provide a verifiable permanent session link or stable session ID.

The following fields are therefore marked:

- Independent reviewer: NOT_VERIFIED
- Independent bilingual review: NOT_VERIFIED
- Stable session ID: NOT_VERIFIED
- Permanent session URL: NOT_VERIFIED
- Owner approval: NOT_VERIFIED
- Repository adoption: NOT_VERIFIED
- CI execution by authoring session: NOT_VERIFIED
- End-to-end test execution by authoring session: NOT_VERIFIED

### 7.4 Sources and Traceability

The repository source locations for this record are:

| Evidence subject | Source location | Evidence type |
|---|---|---|
| Commit distribution | `main` commit history, most recent 30 days, classified by top-level path | Measured statistics |
| P0 issue references | `git log --grep="#<issue>" --since="60 days ago"` | Command results |
| Normative corpus membership | Root-level chapter and `docs/en` file membership sets | File-set comparison |
| Bilingual content and duplicate groups | Paired en/zh files and repository-wide content-duplicate groups | Content comparison |
| Repository hygiene negative cases | `.github/workflows/repository-hygiene.yml:65-79` | Workflow implementation |
| Document management target base | `.github/workflows/document-management.yml:36-46` | Workflow implementation |
| End-to-end execution chain | `crates/brain-cli/tests/e2e_full_chain.rs` | Executable test source |
| Full pipeline execution chain | `crates/brain-cli/tests/e2e_full_pipeline.rs` | Executable test source |
| Product runtime status | `README` | Project status declaration |
| Phase arrangement and exit criterion | `ROADMAP` | Phase definition and criterion |

### 7.5 Evidence Integrity Statement

This record distinguishes among three types of evidence:

1. **Directly measured facts:** the statistics, file relationships, and code locations listed in Section 1.
2. **Causal diagnosis:** the interpretation of governance mechanisms derived from the directly measured facts in Section 2.
3. **Normative rulings:** the proposed requirements for risk tiering, a single normative source, gate failure proof, and executable phase exit in Section 3.

The second category is not a direct measurement result, and the third category is not an already effective repository norm. Any reviewer may present verifiable counter-evidence by repeating the measurement methods in Section 1, examining the causal chains in Section 2, and testing the falsification conditions in Section 3.

Before Owner adoption, this document remains in `Draft`, `PROPOSED`, `Non-Canonical`, and `Informative` status. It records a proposed governance ruling and does not assert approval, merge, review, or CI success.
