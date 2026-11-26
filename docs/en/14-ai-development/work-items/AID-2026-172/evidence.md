---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-172/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Records the two-copy baseline comparison, the shrink-only write refusal and the added unit tests; claims no CI result before the pull request runs."
    usage_status: Active
    modification_status: Modified
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
    canonical_scope: "AID-2026-172 bilingual baseline copy consistency check and shrink-only baseline write assertion"
    canonical_scope_id: "ai-development/aid-2026-172-bilingual-baseline-copy-consistency"
    canonical_scope_keywords:
      - bilingual-baseline
      - baseline-drift
      - shrink-only
      - gate-ratchet
      - write-baseline
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-172/evidence.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-172/evidence.md"
---
# AID-2026-172 — Two shrink-only 77-entry baselines with no consistency check

- Work item: AID-2026-172; id_status: PROVISIONAL.
- Attribution: user-authorized operator (delegated by account owner); date: 2026-11-26.
- base_commit_sha: `8722a37b0cd72dc550d99c0eaebe9e7556ce2f95` (`origin/main` when the branch was created).
- Lead result: the two baselines hold the same entry set today; this change makes "they must agree" a decidable failure and makes `--write-baseline` actually refuse to raise the inventory.
- This record claims no CI result, no independent review and no Owner acceptance.

## 1. What was observed

Two frozen gap inventories of 77 identical entries exist, both meaning "may only shrink":

| File | Reader | Read shape |
|---|---|---|
| `scripts/bilingual-baseline.txt` | `scripts/check_bilingual_docs.py` (job: GOV-DOC-001 structural checks) | `read_baseline()`, two-way set difference against `current_bilingual_gaps()` |
| `scripts/ci/baselines/bilingual-docs.txt` | `scripts/ci/gate_ratchet.py` (job: Bilingual docs coverage (ratchet)) | `read_baseline()`, compared with the output of `check_bilingual_docs_full.py` |

- The first file carries three comment lines, the second none; ignoring `#` comments and blank lines, both hold the same 77 entries.
- **No checker compares the two files.** Regenerating either one alone leaves the other unchanged, so one "frozen inventory" answers differently in two places while each gate reads only its own copy.
- `write_baseline()` only checks that the working tree is clean (`git status --porcelain --untracked-files=all`); it does **not** check that the new set is a subset of the old one.
- In `check_bilingual_docs.py`, `"This baseline may only shrink; entries must never be added."` is only a **comment string** written into the file header. Nothing enforces it, so one regeneration raises the baseline over new gaps and nothing blocks it.

## 2. What changed

The change is confined to the existing bilingual structural gate and its self-test: no new job and no new required context.

1. `scripts/check_bilingual_docs.py`
   - Added `CI_BASELINE_PATH`, pointing at `scripts/ci/baselines/bilingual-docs.txt`, with a comment naming `gates.yml` as its ratchet consumer.
   - Extracted `read_baseline_entries(path)`: comment lines and blanks are not entries; returns a set, or `None` when the file is absent.
   - Added `check_baseline_copies_agree()`: reads both sets, fails when either side is missing, otherwise emits both directions of the difference.
   - `main()` calls it after reading the primary baseline: any entry present in only one file is printed as `::error::` (naming the file and the entry), followed by one summary `::error::`, and the process exits 2.
   - `write_baseline()` reads the **previous** set before writing:
     - previous baseline missing → refuse (shrink-only cannot be proven), exit 2;
     - new set contains entries outside the previous set → refuse, print `+ <path>` for each, exit 2, create no temporary file and never `os.replace`;
     - subset (including equal) → write as before.
2. `scripts/test_check_bilingual_docs.py`
   - `run_gate()` now writes the ratchet copy too and accepts `ratchet_baseline` to inject drift.
   - Five consistency cases: identical copies pass, entry only in the primary copy, entry only in the ratchet copy, comments and blanks are not entries, missing ratchet copy fails closed.
   - Three write cases: an added entry is refused with the file untouched, a shrinking set is written, a missing previous baseline is refused.

## 3. Why this prevents silent drift instead of adding a gate

- **The pass condition is unchanged.** The two sets are equal today, so every existing gate reaches the same verdict on the same repository state before and after this change. The only new failure is "the two copies disagree", which is never true on main.
- **No new required context.** The comparison runs inside `GOV-DOC-001 structural checks`; the workflows are untouched, and neither the ratchet's input file nor `gate_ratchet.py` semantics change.
- **No existing judgement semantics change.** `current_bilingual_gaps()`, the contents of both baselines, and the ratchet's regression/stale rules are all preserved.
- **The failure it catches is silent.** When drift happens, both gates keep passing while the frozen inventory has two different answers; that is exactly the state this check turns red.
- **A comment becomes an assertion.** `--write-baseline` was the only path that could raise the baseline, with nothing in the way; it can now only shrink.

## 4. Local verification and boundary

Local runs (Windows, Python 3, worktree based on `8722a37b`):

| Command | Result |
|---|---|
| `python scripts/test_check_bilingual_docs.py` | 15 tests OK (7 existing + 8 new) |
| `python scripts/check_bilingual_docs.py` (BASE=origin/main, HEAD=branch) | passed; no new and no resolved gaps reported |
| `python scripts/ci/test_gate_ratchet.py` | passed (that script is untouched) |

Boundary:

- No baseline entry is edited and no baseline is regenerated.
- The two files are not merged into one: the structural gate and the ratchet deliberately read one copy each, and merging would change the ratchet's wiring.
- No CI green is claimed; the 16 required contexts come from the pull request.

## 5. Not done

- No Issue is closed or edited.
- Branch protection and workflows are untouched.
- No independent review; `review.status = NOT_ASSIGNED`.
