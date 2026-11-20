# Tier Confirmation Proposal — delivery note

**Work item:** FIX-2026-P1-T3 (bilingual tier classification)
**Status:** PROPOSAL_PENDING_HUMAN_CONFIRMATION
**Baseline:** `9546f78d364b5a1dd1fa2206b34255be9c7fb1a7` (origin/main at generation time)

## What this is

An evidence-based **suggestion table** covering the four directory buckets that `AI-DOC-BILINGUAL-TIERING` v1.0 section 1 marks as `UNKNOWN` / `TIER1_CANDIDATE` (docs/, prompts/, 14-ai-development/, 13-engineering-decisions/). It exists to make human confirmation cheap: each row carries the path, pairing state, a suggested tier, a confidence band and the specific evidence that produced the suggestion.

## What this is NOT

- Not a classification registry. The policy (section 3.1) requires an **approved per-file list** as the sole authority; this file is input to that approval, not the approval.
- Not an automatic promotion. Policy section 3.3 forbids promoting `UNKNOWN` automatically and forbids reporting `UNKNOWN` as PASS. Every row therefore carries `confirmation_record: PENDING`.
- Not a claim that any UNKNOWN has been confirmed. The count of unconfirmed files is unchanged by this delivery.

## Method (reproducible / rejectable)

For each file, the first 4000 characters were scanned for four marker families:

| Signal | Markers |
|---|---|
| Normative | `MUST`, `MUST NOT`, `SHALL`, `REQUIRED`, `SHOULD`, `禁止`, `必须`, `不得`, `强制性` |
| Architecture-contract | `interface contract`, `wire contract`, `protocol`, `schema`, `state machine`, `lifecycle`, `security`, `permission boundary`, `architecture decision`, `ADR` + Chinese equivalents |
| Ephemeral record | `meeting`, `minutes`, `review record`, `acceptance record`, `会议`, `纪要`, `验收记录`, `评审记录` |
| Document header | `Document ID` / `文档 ID`, `Status` / `状态`, `Version` / `版本` |

Rules applied in order: index/README navigation files → Tier 3 candidate (LOW); `prompts/` → Tier 2-or-3 (MEDIUM, the 27-file whitelist is already enumerated in the work-item manifest); ≥2 ephemeral markers → Tier 3 (HIGH); architecture + normative ≥3 each → Tier 1 candidate (HIGH); document header + ≥1 normative → Tier 1 candidate (MEDIUM); ≥2 normative only → Tier 1 candidate (LOW); otherwise Tier 3 candidate (LOW).

## Distribution (377 files in scope)

| Suggestion | Confidence | Count |
|---|---:|---:|
| TIER1_CANDIDATE | HIGH | 59 |
| TIER1_CANDIDATE | MEDIUM | 170 |
| TIER1_CANDIDATE | LOW | 29 |
| TIER2_OR_TIER3_SUGGESTED | MEDIUM | 37 |
| TIER3_CANDIDATE | LOW | 79 |
| TIER3_SUGGESTED | HIGH | 3 |

Pairing state in scope: 20 of 377 files already have a counterpart.

## Known limits (stated, not hidden)

1. **Baseline drift.** The policy's published counts (Tier 1 = 26, Tier 2 = 10, Tier 3 = 27, directory rules 530, total 593) were computed at `f0a3747b`. origin/main now holds 641 Markdown files and this scope alone holds 377. The drift is a fact of the repository, not an error in the policy; the policy's own section 1 says actual counts govern and any later reference must use the actual baseline with the file-list commit SHA.
2. **Head-only scan.** Only the first 4000 characters are examined. A file whose contract language sits deeper will be under-classified. MEDIUM/LOW rows are the ones a reviewer should look at first.
3. **Heuristic, not semantic.** Marker presence is not comprehension. A reviewer may legitimately reject any row; the `evidence` field is there so rejection is a one-line decision rather than a re-read.
4. **No Owner assignment.** Policy section 3.1 requires a responsible Owner per record. This delivery cannot supply Owner identity (repository roles remain `NOT_ASSIGNED`, tracked as F-ROLE-ASSIGN). That is precisely why the table stops at PENDING.

## How to close this out

Human confirmation per row (policy section 3.4) → the confirmed rows become the approved per-file list → the policy's UNKNOWN count drops accordingly. Until then the policy's `UNKNOWN` classification and its `BLOCKED` treatment stand unchanged.
