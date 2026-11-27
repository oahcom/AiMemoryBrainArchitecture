# AID-2026-287 — Executed Prompt Snapshot v1

This document is a structured snapshot of the prompt used for a four-part
delivery. It is not a verbatim transcript of the original conversation.
The original prompt bytes are retained on the conversation side; this file
records the task scope, constraints, and supplied factual inputs in a
reconstructable structured form.

The recorded ChatGPT session identifier is
`6b0939f9-7c6c-83ec-b7dc-6b043f15578c` (chatgpt.com).

Prompt provenance: NOT_VERIFIED. This snapshot does not independently prove
the exact original prompt bytes or establish a verified cryptographic identity
between this structured representation and the original conversation input.

## 1. Target

Produce six files under `14-ai-development/` and one corresponding work-item
INDEX entry.

The six files are:

1. `14-ai-development/AI-DEV-CAPACITY-ALIGNMENT-RULING-001.md`
2. `14-ai-development/AI-DEV-CAPACITY-ALIGNMENT-RULING-001.en.md`
3. `14-ai-development/work-items/AID-2026-287/manifest.yaml`
4. `14-ai-development/work-items/AID-2026-287/prompt-v1.md`
5. `14-ai-development/work-items/AID-2026-287/evidence.md`
6. `14-ai-development/work-items/AID-2026-287/session-evidence.md`

The existing file to modify is:

- `14-ai-development/work-items/INDEX.md`

The work item is `AID-2026-287`.

The intended branch, not yet created, is
`docs/aid-287-capacity-alignment-ruling`.

The measurement baseline is `origin/main` at
`460f437eb3496e10737b9ef20f4b816e34d155c4`.

The associated issues are `#1341` and `#1349`.

The work item has not been committed, pushed, or opened as a pull request.
The pull request is to be created by the persistence operator after pushing.

## 2. Measured facts supplied

All measurements below were supplied as established facts rechecked on
2026-11-27 against `main` at `6306a858`. They must not be independently
recalculated, expanded, or replaced with invented figures.

### 2.1 Commit distribution

The most recent 30-day window on `main` contains 3,272 commits.

Classification by touched top-level path:

- `14-ai-development` record-class commits: 1,382 (42%).
- merge/empty commits: 559.
- `.github` + `scripts`: 389 (12%).
- `docs`: 349 (11%).
- Architecture chapters: 255 (8%).
- `crates/`: 201 (6.1%).
- Other: 137.

### 2.2 Issue references

There are 168 open issues.

The following eight P0 authorization issues have zero commit references
within the most recent 60 days:

- #1128
- #1129
- #1132
- #1133
- #1134
- #1136
- #1138
- #1139

Measurement command for each issue:

`git log --grep="#<issue-number>" --since="60 days ago"`

Each of the eight commands returned an empty result. This measures commit
message references only and does not establish the absence of other issue
activity.

### 2.3 Normative corpus membership

The root-level architecture chapters and `docs/en` have different membership
sets.

- Chapter 01: 8 shared members out of 11.
- Chapter 03: 6 shared members out of 13.
- Chapter 04: root 43 versus English 13.
- Chapter 06: root 26 versus English 12.
- Chapter 08: root 106 versus English 5.

Across 169 en/zh document pairs, only 1 pair is byte-for-byte identical.

There are 11 content-duplicate groups across the repository.

Membership overlap, byte equality, and content duplication must remain
distinct concepts in the diagnosis.

### 2.4 Gate negative cases and target base

`repository-hygiene.yml:65-79` asserts only `status > 1` for its negative
sample. A checker accepting a known-bad commit can therefore still leave
this assertion green.

`document-management.yml:36-46` uses
`github.event.pull_request.base.sha` rather than the actual target base of
the merge candidate.

These observations must not be described as proof that the gates are
effective.

### 2.5 End-to-end execution chain

The repository contains executable tests:

- `crates/brain-cli/tests/e2e_full_chain.rs`
- `crates/brain-cli/tests/e2e_full_pipeline.rs`

These connect all 12 crates.

The existence of these tests establishes an available executable verification
chain, not that the authoring session ran them or that CI passed.

### 2.6 Product phase and exit criterion

The README declares that the product-grade runtime has not started.

The ROADMAP places prototype/implementation in Phase 5, the final phase.

The Phase 3 exit criterion states:

"Every component has a bounded purpose, ownership, contract, and open
questions."

This criterion can be satisfied indefinitely through documentary completion
without establishing executable product capability.

## 3. Shape constraints

### 3.1 Chinese source

The Chinese decision record must contain YAML frontmatter with the supplied
document metadata, followed by a title and decision-record header.

The header must identify:

- Document ID and version.
- PROPOSED status, without claiming adoption.
- Ruling authority and delegated drafting capacity.
- Ruling date: 2026-11-27.
- Measurement baseline: `main` @ `6306a858`.
- Tracking: AID-2026-287, Issue #1341, Issue #1349.
- Relationship: INTERPRET.
- Review-by: 2026-12-27.
- Language authority and the absence of independent bilingual review.

### 3.2 English counterpart

The English file must be semantically equivalent to the Chinese source.

It must preserve all section numbers, ruling identifiers, measurements,
alternatives, consequences, falsification conditions, excluded decisions,
and NOT_VERIFIED declarations.

The English source metadata must identify the Chinese source and retain
`{{SOURCE_BLOB}}` literally as the source blob placeholder.

The Chinese source remains authoritative. No independent bilingual parity
review may be claimed.

### 3.3 Required section structure

Both decision records must contain the following sections in this order:

1. Context.
2. Diagnosis.
3. Rulings A1-A4.
4. Consequences.
5. Falsifiers.
6. What this record does not decide.
7. Evidence and provenance.

The Chinese file uses bilingual section headings. The English counterpart
uses English-only section headings.

### 3.4 Four fixed rulings

The ruling identifiers and subjects must remain fixed:

- A1: Record-obligation tiering by risk.
- A2: Single normative source.
- A3: Every gate must prove it can fail.
- A4: Phase 3 exit as an executable checklist.

Every ruling must contain all five elements:

1. Decision — an executable determination with explicit applicability and
   exclusions.
2. Rationale — references to measured facts and causal diagnosis.
3. Alternatives considered and rejected — at least two alternatives and
   reasons for rejection.
4. Consequences — immediate consequences, including what must be abandoned.
5. Falsifier — an observable and measurable condition that would disprove
   the ruling.

### 3.5 Falsification and provenance

Each falsifier must identify an observable triggering result and a clear
measurement boundary.

The consolidated falsification table must identify the ruling, falsifying
observation, observation window, and adjudicator role.

Adjudicators must be described by role, not personal name.

The evidence section must distinguish direct measurements, causal diagnosis,
and proposed normative decisions.

It must explicitly identify unverified session, review, adoption, and
execution claims as NOT_VERIFIED where applicable.

## 4. Hard prohibitions

- Do not turn the decision record into a task list, TODO list, assignment
  table, milestone schedule, or implementation plan.
- Do not use next-step, pending-task, or scheduling language in the ruling.
- Do not claim that the ruling has been adopted, approved, merged, reviewed,
  accepted, or passed CI.
- Do not claim that end-to-end tests were executed by the authoring session.
- Do not invent, extrapolate, or independently recalculate numerical
  measurements.
- Do not change the supplied baseline, dates, issue identifiers, or
  session identifier.
- Do not modify or delete existing normative documents.
- Do not treat historical records as automatically invalid under the
  proposed ruling.
- Do not equate a green gate with proof of failure capability.
- Do not equate documentary completeness with executable phase exit.
- Do not claim independent bilingual review without recorded evidence.

## 5. Output contract

Each requested file must be emitted as a complete standalone file body.

Use the exact file boundary convention:

`<<<FILE: relative/path>>>`

followed by the complete file contents, and terminate with:

`<<<END>>>`

Each boundary line must occupy its own line and appear exactly once for
its corresponding file.

The file body must be suitable for byte-for-byte persistence. No explanatory
preface, commentary, or material outside the file boundaries is permitted.

If a file is too long to deliver in one response, end at a complete section
boundary with `<<<CONTINUE>>>`. Continuation content must preserve the same
file identity and complete the remaining body without duplication.

YAML files must remain parseable by a standard YAML parser. Literal
placeholders intended for persistence-time substitution must remain
unchanged unless explicitly instructed otherwise.

The prompt snapshot is structured documentation rather than a verbatim
transcript. It must not be represented as a byte-identical original prompt.

## 6. Delivery sequence

The delivery consists of four parts, in this exact order:

1. Chinese source decision record:
   `14-ai-development/AI-DEV-CAPACITY-ALIGNMENT-RULING-001.md`
2. English counterpart:
   `14-ai-development/AI-DEV-CAPACITY-ALIGNMENT-RULING-001.en.md`
3. Work-item metadata and structured prompt snapshot:
   `14-ai-development/work-items/AID-2026-287/manifest.yaml`
   `14-ai-development/work-items/AID-2026-287/prompt-v1.md`
4. Evidence, session evidence, and work-item index entry:
   `14-ai-development/work-items/AID-2026-287/evidence.md`
   `14-ai-development/work-items/AID-2026-287/session-evidence.md`
   `14-ai-development/work-items/INDEX.md`

The four-part delivery sequence records the order of artifact production.
It does not assert that the files have been persisted, committed, pushed,
reviewed, or accepted.
