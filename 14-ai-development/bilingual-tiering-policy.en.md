# Bilingual Documentation Tiering Policy

- **Document ID:** AI-DOC-BILINGUAL-TIERING
- **Version:** 1.0
- **Status:** PROPOSED (pending formal adoption by the project governance authority)
- **Owner:** Integration Owner (classification rules); respective domain Owners (their documents)
- **Chinese counterpart:** [bilingual-tiering-policy.md](bilingual-tiering-policy.md)
- **Governing references:** GOV-DOC-001, AI-STD-001 §7.1, AI-EXEC-001 §3, AI-EXEC-002 §7.1

## 1. Purpose and Scope

This policy establishes an auditable bilingual-documentation tiering model for the repository. It defines which documents require Chinese and English counterparts, which may optionally be bilingual, and which are Chinese-first. Tiering governs documentation delivery and review; it does not transfer domain decision authority or weaken any bilingual gate imposed by a governing standard.

The classification baseline is derived from a per-file survey of all 593 Markdown files in the repository (`14-ai-development/work-items/FIX-2026-P1-T3/tier-mapping-proposal.yaml`, baseline commit `f0a3747b279bcb83297b4490f5cd0bb3e1dbfc17`, status PROPOSAL):

| Tier | Per-file count | Directory-rule coverage | Language policy | Constraint |
|---|---:|---:|---|---|
| Tier 1 | 26 | — | Mandatory bilingual | Every file requires Chinese and English versions |
| Tier 2 | 10 | — | Optional bilingual | Limited to explicitly allowlisted files |
| Tier 3 | 27 | 192 (reviews/) | Chinese-first | An English version requires Owner confirmation |
| Pending confirmation (UNKNOWN/TIER1_CANDIDATE) | — | 338 (docs/, prompts/, 14-ai-development/, 13-engineering-decisions/) | Human confirmation | UNKNOWN MUST NOT be auto-promoted; treated as BLOCKED |

63 per-file entries + 530 directory-rule files = 593; every Markdown file is accounted for. Directory rules are analytical groupings, not final classifications: files they cover remain UNKNOWN (human confirmation required) or TIER1_CANDIDATE (pending per-file verification) until individually confirmed.

**Relationship to the earlier planning figures (32/15/30):** Before implementation, this policy draft registered planning estimates of Tier 1 = 32, Tier 2 = 15, Tier 3 = 30. Those were design-stage upper-bound targets, not a survey of actual repository files. The implementation-stage per-file survey (baseline `f0a3747b`) produced the actual counts above: Tier 1 = 26, the actual survey result superseding the planning estimate of 32, because several planning candidates failed per-file verification against the Tier 1 architecture-contract criteria; Tier 2 = 10, the actual survey result superseding the planning estimate of 15, because the allowlist was tightened under the same criteria; Tier 3 per-file = 27, the actual survey result superseding the planning estimate of 30, with meeting/acceptance records scattered under recovery/, scripts/, and the repository root brought into the per-file inventory. This section supersedes the planning figures; all future references MUST use the actual baseline, anchored to the commit SHA of the per-file inventory.

These counts do not authorize adding, removing, or reclassifying files. Actual path membership MUST be established by an authorized per-file classification inventory. Classification MUST NOT be inferred solely from directory, extension, filename, or automated heuristics.

## 2. Tier Definitions

### 2.1 Tier 1 — Mandatory Bilingual (26 per-file baseline entries)

1. Every Tier 1 file MUST have both Chinese and English counterparts. Both versions MUST be created or updated in the same change set.
2. The two versions MUST preserve equivalent normative meaning, obligation strength, decision status, stable identifiers, examples, and link relationships.
3. A missing counterpart or material semantic divergence means the deliverable is NOT DONE and MUST block the affected delivery from becoming ACCEPTED. Workload, translation delay, or a classifier result is not grounds for waiver.
4. **Tier 1 MUST NOT be downgraded.** Any proposal to move a Tier 1 file to Tier 2, Tier 3, or a lower-obligation category is invalid unless the project governance authority formally changes this policy and its classification baseline through a separate, explicit normative revision. An ordinary Owner confirmation, script output, or one-off task approval cannot authorize a downgrade.
5. Chinese and English files SHOULD link to each other and record their common source revision or change-set identifier.

### 2.2 Tier 2 — Optional Bilingual, Allowlist Only (10 allowlisted files at baseline)

1. Tier 2 applies only to explicitly approved allowlisted paths (10 registered at baseline). A file outside that allowlist MUST NOT be assigned to Tier 2 based on similar purpose, directory location, or an author's judgment.
2. For an allowlisted file, its responsible Owner MAY decide whether an English counterpart is useful based on audience, maintenance cost, and usage. If bilingual versions are provided, semantic parity and reciprocal links remain required.
3. **Optional bilingual status in Tier 2 NEVER waives the bilingual gate for architecture-semantic changes.** Whenever a change affects or may affect architectural meaning, interfaces/protocols, data models, state machines, authorization boundaries, cross-module contracts, or system behavior, the authoritative Chinese and English documentation MUST be updated together under GOV-DOC-001, AI-STD-001 §7.1, and AI-EXEC-002 §7.1—even if the file is in Tier 2.
4. Tier 2 is not an exception to higher-level bilingual requirements and MUST NOT be used to label an architecture-semantic change as “translation optional.”
5. Changes to the allowlist require a traceable Owner/governance approval record. Scripts MUST NOT add or remove allowlisted paths automatically.

### 2.3 Tier 3 — Chinese-First (27 per-file baseline entries, plus 192 files under the reviews/ directory rule)

1. Chinese is the default authoritative language for Tier 3 files. An English-speaking audience or availability of automated tooling does not, by itself, create a translation requirement.
2. Whether to create or maintain an English counterpart **MUST be explicitly confirmed by the responsible Owner**. Record the confirmer, scope, intended audience, and maintenance responsibility.
3. An Owner's confirmation that no English version is needed means only that the file remains Chinese-first under its current classification. It does not waive an architecture-semantic bilingual gate or any other governing requirement.
4. If a Tier 3 change affects architectural meaning, the necessary authoritative Chinese and English documents MUST still be updated under governing standards. Where appropriate, identify the affected normative document as Tier 1 or another suitable category and use the formal reclassification process. A Tier 3 label MUST NOT block a required bilingual update.

## 3. Classification Authority and Unknown Classifications (F1)

1. The approved per-file inventory is the sole source of truth for classification. Each record MUST include at least: repository-relative path, Tier, language obligation, responsible Owner, approval basis/record, and inventory version or commit SHA.
2. Automated checks MAY validate known classifications, path coverage, and rule consistency. They MUST NOT infer or silently fill missing classifications.
3. **An unknown classification MUST be reported as `UNKNOWN` and wait for human confirmation.** The tool MUST show the path and pending-confirmation status. It MUST NOT default the file to Tier 2 or Tier 3, automatically repair its classification, or report UNKNOWN as PASS.
4. An authorized Owner or governance delegate MUST make the human classification decision and update the per-file inventory. Until then, the classification gate is BLOCKED / NEEDS_CONFIRMATION.
5. File additions, moves, renames, deletions, or responsibility changes require revalidation. A path change MUST NOT silently inherit a previous classification without an audit record.

## 4. Bilingual Parity and Review

For files requiring bilingual versions, and files whose architecture-semantic changes trigger the bilingual gate, reviewers MUST compare both languages against the same source revision:

- normative meaning and obligation strength (MUST/SHOULD/MAY);
- stable IDs, field names, API/protocol identifiers, and status values;
- decision status, Owner, exception conditions, and closure criteria;
- examples, commands, configuration keys, paths, and references;
- reciprocal links, version/source markers, and change scope.

A material difference, missing counterpart, or unverifiable common source revision is FAIL / BLOCKED. “The translation is broadly equivalent” is not a substitute for evidence. Translation-only changes MUST NOT introduce decisions or alter normative strength.

## 5. Reclassification and Exceptions

1. Reclassification among Tier 1, the Tier 2 allowlist, and Tier 3 MUST use a formal change record stating rationale, affected files, proposer, approver, effective version, and migration plan.
2. Tier 1 MUST NOT be downgraded through an ordinary exception. Where a governing standard permits temporary STALE handling, the authorized governance body MUST formally approve it and record the temporary authoritative version, Owner, tracking Issue, and expiry date. Such an exception does not change the Tier 1 classification.
3. Tier 2 allowlist status MUST NOT be interpreted as a waiver for architecture-semantic bilingual updates.
4. The responsible Owner decides whether a Tier 3 English counterpart is created. If classification is disputed or the Owner is unknown, report UNKNOWN and escalate; implementers MUST NOT decide on the Owner's behalf.

## 6. Delivery Records and Acceptance

Every substantive change governed by this policy SHOULD record:

- changed paths, before/after Tiers, and approval basis;
- Chinese/English paths and their common source revision;
- parity results for meaning, identifiers, status, examples, and links;
- UNKNOWN entries, human confirmer, and confirmation record;
- outstanding items, responsible Owner, and objective closure criteria.

NOT RUN, UNKNOWN, missing, or unconfirmed states MUST NOT be treated as PASS. Tier 1 bilingual completeness, the Tier 2 architecture-semantic bilingual gate, and Tier 3 Owner confirmation all require traceable evidence.

## 7. Relationship to Governing Standards

This policy governs documentation classification and execution. It does not replace GOV-DOC-001, AI-STD-001, AI-EXEC-001, AI-EXEC-002, or any domain Owner contract. In case of conflict, governing standards and formal governance decisions prevail. This policy MUST NOT be used to weaken bilingual obligations for architecture-semantic changes, independent review, acceptance, or release gates.

## 8. Effective Date

This document remains PROPOSED until formally adopted by the governance authority. The adoption record MUST identify the approver, effective date, adopted per-file classification inventory version, and its SHA. All automation MUST comply with this policy, especially human confirmation for UNKNOWN, the non-downgradability of Tier 1, and the architecture-semantic bilingual gate.

The blank form for the adoption record is `14-ai-development/work-items/ADOPTION-EVIDENCE-2026-P1/adoption-record-template.md`; the assembly of ready and missing evidence is `adoption-evidence-dossier.md` in the same directory. Both are preparation material: neither constitutes adoption, and neither may be cited as adoption or as proof that an approver exists.
