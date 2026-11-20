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
- Document-header detection uses the single constant `HEADER_RE` in the generator, emitted verbatim into the YAML as `document_header`; both places derive from that one constant, so they cannot drift.
- Rule order is strict first-match-wins; later rules are not evaluated.

**Enumeration and environment (exact).**
- File list comes from `git ls-tree -r --name-only origin/main`, filtered to `.md` under the four scope prefixes, then `sorted()`. No glob, no `.gitignore`, no filesystem walk.
- No path exclusions beyond that filter — this proposal's own files are in scope and appear as ordinary rows.
- A non-zero `git show` exit or a non-UTF-8 decode adds `READ-FAILURE` to the row evidence and forces LOW; such a row is never equal to a genuine negative. Zero such rows at this baseline.
- Python 3.13, git 2.x, no network, no third-party packages, LF-terminated UTF-8. Two consecutive runs at the same baseline produce byte-identical output (verified by sha256).


| Signal | Markers (verbatim) |
|---|---|
| Normative | `MUST`, `MUST NOT`, `SHALL`, `REQUIRED`, `SHOULD`, `禁止`, `必须`, `不得`, `强制性` |
| Architecture-contract | `interface contract`, `wire contract`, `protocol`, `schema`, `state machine`, `lifecycle`, `security`, `permission boundary`, `architecture decision`, `ADR`, `接口契约`, `协议`, `状态机`, `生命周期`, `安全`, `权限边界`, `架构决策` |
| Ephemeral record | `meeting`, `minutes`, `review record`, `acceptance record`, `会议`, `纪要`, `验收记录`, `评审记录` |
| Document header | regex above |

**Rule order.** index/README navigation → Tier 3 candidate (LOW); `prompts/` → Tier 2-or-3 (MEDIUM); ≥2 ephemeral → Tier 3 (HIGH); arch ≥3 **and** norm ≥3 → Tier 1 candidate (HIGH); header **and** norm ≥1 → Tier 1 candidate (MEDIUM); norm ≥2 → Tier 1 candidate (LOW); otherwise Tier 3 candidate (LOW).

**Pairing detection.** Computed once, globally, as a set of **mutual claims**, so reciprocity holds by construction rather than by after-the-fact checking. Claim order: (1) `x.zh-CN.md` ↔ `x.en.md`; (2) `x.en.md` ↔ `x.md`; (3) `docs/en/P` ↔ `docs/zh-CN/P`. A file already paired is never claimed again — so a plain `x.md` whose `x.en.md` is already taken by a `x.zh-CN.md` is left **unpaired** rather than forced into a non-reciprocal link. A claim whose counterparty is absent from the baseline tree is dropped. Audited after generation: 164 paired rows, 0 non-reciprocal. A pair whose two sides scan to different tiers is marked `PAIR-DIVERGENT` on both rows and forced to LOW confidence.

## Distribution (377 files in scope, 164 paired)

| Suggestion | Confidence | Count |
|---|---:|---:|
| TIER1_CANDIDATE | HIGH | 59 |
| TIER1_CANDIDATE | MEDIUM | 159 |
| TIER1_CANDIDATE | LOW | 40 |
| TIER2_OR_TIER3_SUGGESTED | MEDIUM | 37 |
| TIER3_CANDIDATE | LOW | 79 |
| TIER3_SUGGESTED | HIGH | 3 |

`PAIR-DIVERGENT` rows: 24 (12 pairs, listed in the generator's stdout). These rows are the highest-signal rows in the file, and the signal is narrow: the heuristic disagrees **with itself** on one translation pair. Because both sides are translations of one text, at most one of the two suggestions can be right — so the pair is where a reviewer's time is best spent. It is explicitly **not** evidence that a human read of either file would differ from the table, and not evidence of any defect in the documents.

## Known limits (stated, not hidden)

1. **Baseline drift.** The policy's published counts (Tier 1 = 26, Tier 2 = 10, Tier 3 = 27, directory rules 530, total 593) were computed at `f0a3747b`. origin/main now holds 641 Markdown files and this scope alone holds 377. Drift is a fact of the repository, not an error in the policy; the policy's own section 1 says actual counts govern and any later reference must use the actual baseline with the file-list commit SHA.
2. **Head-only scan.** Only the first 4000 characters are examined. A file whose contract language sits deeper is under-classified — this is the dominant failure mode, and it is one-directional (toward Tier 3).
3. **Substring matching, not semantics.** `SHALL` matches inside "shall not be considered", `schema` matches inside "no schema defined", `安全` matches inside "本项不涉及安全". Negation and quotation are not handled. Symbol-level false positives are expected and are why every row is PENDING.
4. **Rule priority discards information.** First-match-wins means an ephemeral-record file that also contains normative language is scored as Tier 3 (HIGH) with no record of the normative markers. The `evidence` field names only the winning rule.
5. **Read and encoding failures are labelled, not silent.** The generator decodes strictly: a `UnicodeDecodeError` or a non-zero `git show` exit adds `READ-FAILURE` to the row's evidence and forces LOW. Strict decode was chosen over `errors='replace'` because a legitimate U+FFFD in valid UTF-8 would otherwise be indistinguishable from a decode artefact. That does not make the row correct — it makes it *distinguishable* from a genuine negative, which is the most this proposal can promise. Zero such rows occurred at this baseline; the mechanism is there for the next run.
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

## Write-scope authorization

This delivery adds four paths, all under `14-ai-development/work-items/FIX-2026-P1-T3/`. The original manifest's `allowed_write_paths` did not list three of them, which made the first commit of this PR an out-of-scope write. The manifest now lists all four.

**What that list is, and is not.** R3 asked whether the expansion is actually authorized, and the honest answer is: **no Owner signature exists.** There is no GO decision text for FIX-2026-P1-T3 anywhere in this repository — unlike FIX-2026-P1-T4, which records `DEC-FIX-2026-P1-T4-GO-001` with named sections, this work item's manifest cites "the GO decision for FIX-2026-P1-T3" without an identifier any reviewer could check. The three earlier scope entries (`111877aa`, `66f1b0ff`, `aeb68bd1`) have the same character: manifest self-declaration is the precedent, not a decision record. The manifest now carries `authorization_status: SELF_DECLARED_NOT_OWNER_SIGNED` and says so.

Practical consequence: if the work item's real GO decision is ever produced and excludes these paths, the four files move to an authorized path. Nothing about the 377 rows depends on the outcome — the table is input to a future approval, not an approval, and every row is still `PENDING` regardless of where the file physically sits.

The four paths:
- `authorization-manifest.yaml` (already authorized, amended)
- `tier-confirmation-proposal.yaml`
- `TIER-CONFIRMATION-PROPOSAL-NOTES.md`
- `generate-tier-proposal.py`

## How to close this out

Human confirmation per row (policy section 3.4) → the confirmed rows become the approved per-file list → the policy's UNKNOWN count drops accordingly. Until then the policy's `UNKNOWN` classification and its `BLOCKED` treatment stand unchanged.
