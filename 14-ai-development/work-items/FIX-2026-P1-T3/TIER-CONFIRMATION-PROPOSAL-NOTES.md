# Tier Confirmation Proposal — delivery note

**Work item:** FIX-2026-P1-T3 (bilingual tier classification)
**Status:** PROPOSAL_PENDING_HUMAN_CONFIRMATION
**Baseline:** `9546f78d364b5a1dd1fa2206b34255be9c7fb1a7` (the single commit named in `baseline_commit` inside the YAML; no other revision was scanned)

## What this is

An evidence-based **suggestion table** covering the four directory buckets that `AI-DOC-BILINGUAL-TIERING` v1.0 section 1 marks as `UNKNOWN` / `TIER1_CANDIDATE` (docs/, prompts/, 14-ai-development/, 13-engineering-decisions/). It exists to make human confirmation cheap: each row carries the path, pairing state, a suggested tier, a confidence band and the specific evidence that produced the suggestion.

## What this is NOT

- Not a classification registry. The policy (section 3.1) requires an **approved per-file list** as the sole authority; this file is input to that approval, not the approval.
- Not an automatic promotion. Policy section 3.3 forbids promoting `UNKNOWN` automatically and forbids reporting `UNKNOWN` as PASS. Every row therefore carries `confirmation_record: PENDING`.
- Not a claim that any UNKNOWN has been confirmed. The count of unconfirmed files is unchanged by this delivery.

## Method — fully specified, reproducible

Generator: `14-ai-development/work-items/FIX-2026-P1-T3/generate-tier-proposal.py` (runs `git show origin/main:<path>` per file; no network, no other input). Running it against the baseline reproduces this file. Marker lists are also embedded in the YAML under `marker_families`, so the algorithm survives even if the script is lost.

**Matching rules (exact).**
- Scan window: first **4000 characters** of the file (`scan_window_chars: 4000`).
- Match test: **case-insensitive substring** containment in that window. Not word-boundary, not regex.
- Counting: **distinct marker count** per family — a marker present ten times counts once.
- Document-header detection is the only regex: `^\s*[-*]?\s*\**\s*(Document ID|Status|Version|文档 ID|状态|版本)\s*[:：]` with `(?im)`.
- Rule order is strict first-match-wins; later rules are not evaluated.

| Signal | Markers (verbatim) |
|---|---|
| Normative | `MUST`, `MUST NOT`, `SHALL`, `REQUIRED`, `SHOULD`, `禁止`, `必须`, `不得`, `强制性` |
| Architecture-contract | `interface contract`, `wire contract`, `protocol`, `schema`, `state machine`, `lifecycle`, `security`, `permission boundary`, `architecture decision`, `ADR`, `接口契约`, `协议`, `状态机`, `生命周期`, `安全`, `权限边界`, `架构决策` |
| Ephemeral record | `meeting`, `minutes`, `review record`, `acceptance record`, `会议`, `纪要`, `验收记录`, `评审记录` |
| Document header | regex above |

**Rule order.** index/README navigation → Tier 3 candidate (LOW); `prompts/` → Tier 2-or-3 (MEDIUM); ≥2 ephemeral → Tier 3 (HIGH); arch ≥3 **and** norm ≥3 → Tier 1 candidate (HIGH); header **and** norm ≥1 → Tier 1 candidate (MEDIUM); norm ≥2 → Tier 1 candidate (LOW); otherwise Tier 3 candidate (LOW).

**Pairing detection.** (a) same-directory suffix swap `.en.md` ↔ `.zh-CN.md` ↔ `.md`; (b) `docs/en/` ↔ `docs/zh-CN/` path mirror. A pair whose two sides scan to different tiers is marked `PAIR-DIVERGENT` on both rows and forced to LOW confidence — a translation pair cannot legitimately hold two tiers, so the pair must be confirmed together.

## Distribution (377 files in scope, 162 paired)

| Suggestion | Confidence | Count |
|---|---:|---:|
| TIER1_CANDIDATE | HIGH | 59 |
| TIER1_CANDIDATE | MEDIUM | 159 |
| TIER1_CANDIDATE | LOW | 40 |
| TIER2_OR_TIER3_SUGGESTED | MEDIUM | 37 |
| TIER3_CANDIDATE | LOW | 79 |
| TIER3_SUGGESTED | HIGH | 3 |

`PAIR-DIVERGENT` rows: 24. These are the highest-signal rows in the file — they prove the marker heuristic and the human reading disagree somewhere, which is exactly what a reviewer needs to see.

## Known limits (stated, not hidden)

1. **Baseline drift.** The policy's published counts (Tier 1 = 26, Tier 2 = 10, Tier 3 = 27, directory rules 530, total 593) were computed at `f0a3747b`. origin/main now holds 641 Markdown files and this scope alone holds 377. Drift is a fact of the repository, not an error in the policy; the policy's own section 1 says actual counts govern and any later reference must use the actual baseline with the file-list commit SHA.
2. **Head-only scan.** Only the first 4000 characters are examined. A file whose contract language sits deeper is under-classified — this is the dominant failure mode, and it is one-directional (toward Tier 3).
3. **Substring matching, not semantics.** `SHALL` matches inside "shall not be considered", `schema` matches inside "no schema defined", `安全` matches inside "本项不涉及安全". Negation and quotation are not handled. Symbol-level false positives are expected and are why every row is PENDING.
4. **Rule priority discards information.** First-match-wins means an ephemeral-record file that also contains normative language is scored as Tier 3 (HIGH) with no record of the normative markers. The `evidence` field names only the winning rule.
5. **Read and encoding failures are silent.** `git show` output is decoded UTF-8 with `errors='replace'`. A binary or non-UTF-8 file yields replacement characters, no markers, and therefore a Tier 3 (LOW) row indistinguishable from a genuine negative. Empty files take the same path.
6. **Pair divergence is detected, not resolved.** Where a pair splits tiers, both rows say so, but the table does not pick a winner — that is a semantic decision reserved for the confirming human.
7. **Heuristic, not comprehension.** A reviewer may legitimately reject any row; the `evidence` field exists so rejection is a one-line decision rather than a re-read.
8. **Prompt whitelist is external to this file.** The 27-file AI-prompt inventory referenced by the `prompts/` rule lives in `authorization-manifest.yaml` (`inventory.expected_a_i_prompt_blobs`), not here. This note does not restate it and does not vouch for it.
9. **No Owner assignment.** Policy section 3.1 requires a responsible Owner per record. This delivery cannot supply Owner identity (repository roles remain `NOT_ASSIGNED`, tracked as F-ROLE-ASSIGN). That is precisely why the table stops at PENDING.

## Reviewer-flagged rows (R1 round 1)

Three rows were flagged as likely misclassified. Two are accepted as evidence of limits 2/3 and left as-is with the flag recorded here; one is accepted as a genuine method gap and fixed in wording.

| Row | R1 concern | Disposition |
|---|---|---|
| `docs/en/03-memory-brain/memory-versioning.md` | versioning is potentially an architecture contract; Tier 3 by head-scan may be a miss | **Accepted as limit 2.** The English head is descriptive prose with no normative or contract markers; contract language sits below the 4000-char window. Its `docs/zh-CN/` counterpart scans TIER1_CANDIDATE, so both rows now carry `PAIR-DIVERGENT` and LOW confidence. Reviewer decides the pair. |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-002.md` | an execution record may carry normative acceptance constraints | **Accepted as limit 3.** The file records what was executed; it imposes nothing. Head-scan finds no normative marker. Left TIER3_CANDIDATE / LOW with this note as the dissenting view recorded. |
| `14-ai-development/work-items/AID-2026-009/test-design/NESTED-CLAIM-MULTI-SCOPE-WRITE.md` | header + normative words do not prove an architecture-level constraint | **Accepted as a method gap, fixed in wording.** This is the weakest positive rule (header + ≥1 normative). Its `evidence` string now says so explicitly and instructs semantic verification before confirming; the band stays MEDIUM so it sorts after HIGH rows. Downgrading the rule itself to LOW was rejected: it would move 159 rows, not one. |

## How to close this out

Human confirmation per row (policy section 3.4) → the confirmed rows become the approved per-file list → the policy's UNKNOWN count drops accordingly. Until then the policy's `UNKNOWN` classification and its `BLOCKED` treatment stand unchanged.
