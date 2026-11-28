# AID-2026-293 Prompt Snapshot v1

Prepare one documentation-only carrier for Issue #262 in `oahcom/AiMemoryBrainArchitecture`, using exact baseline `31c1e5d83e7dad326dbd4b69d4a8e19534718ff1`.

Scope is limited to AC3, AC4, AC6 and AC8.

Requirements:
- Preserve existing risk and complexity document content except for precise append-only patches.
- AC3: each of ten risk evidence cells must ultimately contain either a parseable `path:line` with an adjacent verbatim quote, or `NO_EVIDENCE_FOUND` with an actually executed search command and exact search scope.
- AC4: add four named dimensions (change surface, coupling, irreversibility, concurrency/state), a 1–5 rubric, scores for every module and a per-row `path:line` or `EVIDENCE_GAP`. Retain the historical eight-number column.
- AC6: provide a directly runnable Python checker, data file and unittest suite. Include one inline negative fixture for each of seven rules. Exit codes: 0 pass, 1 rule violation, 2 invalid arguments/input.
- AC8: provide bilingual review templates with baseline blob SHAs, `PENDING_INDEPENDENT_REVIEW`, and `TO_BE_FILLED_BY_INDEPENDENT_REVIEWER`. Do not self-sign.
- Add work-item manifest, evidence, session evidence, prompt snapshot and one INDEX registration row.
- PR body must identify Issue #262, AI assistance, bilingual manifest, per-AC evidence/status and explicit non-claims.

No repository writes, Issue edits, PR creation or merge are authorized by this prompt snapshot. Unexecuted searches/tests and independent review must remain pending.
