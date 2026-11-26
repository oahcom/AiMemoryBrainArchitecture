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
        - "14-ai-development/work-items/AID-2026-191/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the request as received, the environment it ran in, and the commands whose output is quoted in evidence.md. No platform session identifier is available, so the session identity is recorded as NOT_RECORDED rather than inferred."
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
---

# Session Evidence — AID-2026-191

## Session role / use case

Repair worker inside a dispatched contract. The assistant was dispatched to give the
77-entry frozen bilingual inventory a single authority, to widen
`check_baseline_copies_agree()` from two copies to every copy, to mark the drifted
81-entry snapshot as a historical record without changing its content, to correct the
two guide passages that quote `baseline=81`, and to add tests that are red for a
divergent copy and green for a consistent set.

The role it performed was repair plus enumeration: the first thing the contract asked
for was a measured inventory of the copies, and that measurement decided the shape of
the check, because the seven carriers are not seven equal lists.

## Actual AI input

The dispatched contract instructed the assistant to:

- work only in the existing worktree `D:\code\wt-reg03` on branch
  `fix/2026-11-27-baseline-copies`, based on main `4326669c`, and never touch the
  shared clone `D:\code\AiMemoryBrainArchitecture`;
- enumerate every carrier of the 77-entry list across the whole repository, by content
  shape rather than by filename, and report path, line count and an entry-by-entry
  verdict against the authority;
- designate `scripts/ci/baselines/bilingual-docs.txt` — the file the ratchet actually
  reads — as the single authority;
- extend `check_baseline_copies_agree()` to cover every copy, printing the two-way
  difference entry by entry as `::error::` and exiting 2;
- mark the drifted copy as a historical snapshot (title change or a
  `> HISTORICAL — not a gate input` line) without deleting it or changing its entries,
  and repoint `ci-gates-and-ratchets.en.md` / `.zh-CN.md` at the authority with a note
  that 81 is a historical value;
- add tests showing that a newly diverging copy is red and that a fully consistent set
  is green;
- confirm `python scripts/check_bilingual_docs.py` still exits 0 and reports
  `77 frozen`;
- allocate an unused `AID-2026-<NNN>` after checking pull-request titles and branches,
  publish the work item with bilingual evidence and one `INDEX.md` row, and merge only
  after 16 of 16 required contexts succeed on the exact head with branch behind == 0.

Prohibited by the same contract: changing any entry of any copy beyond the historical
annotation, regenerating a baseline, touching `current_bilingual_gaps()`, changing
branch protection, closing Issues, or fabricating a SHA, a test output or a gate result.

The environment constraint stated with the contract was that `PYTHONUTF8=1` is required
on this host, because the GBK console codepage breaks decoding of captured `git` output.
A further constraint discovered while working: `git diff BASE...HEAD` sees only
committed state, so the gate had to be run after the commit rather than over a dirty
tree.

The contract text is pinned in `prompt-v1.md` (4717 bytes, SHA-256
`74ec91ce652d56248a5b9e56f390641b2cc9e8fb196070eafbe887b5f74f6fee`). No prompt-library
registration exists for it, so `prompt_status` is `NOT_RECORDED`.

## AI-visible output

The assistant reported, and the repository shows on the head of this branch:

- seven carriers enumerated, at the base commit: two hold the 77 entries exactly
  (`scripts/ci/baselines/bilingual-docs.txt`, `scripts/bilingual-baseline.txt`), one is
  an 803-path governance register that contains all 77
  (`14-ai-development/governance-register/evidence/main-paths.json`), one is the
  83-finding scan record at `568b847c`
  (`00-governance/reports/gov-doc-001-full-scan-2026-11-20.md`), two are the 81-finding
  review snapshot in both languages
  (`reviews/bmcp-architecture-followup/BMCP-ARCH-001.{en,zh-CN}.md`), and one is a
  work-item proposal that mentions 62 of the paths in prose with no list block
  (`14-ai-development/work-items/FIX-2026-P1-T3/tier-confirmation-proposal.yaml`);
- the premise "多 9 / 缺 5" measured as 8 extra and 4 absent: 73 shared, 73 + 8 = 81,
  77 − 4 = 73; the measured pair is what the record uses, and the discrepancy is stated
  rather than smoothed;
- `check_baseline_copies_agree()` now returns 0 errors and 2 notices with six copies
  compared plus a discovery pass over `git ls-files`, where it previously returned 0
  errors with two copies compared; removing either `HISTORICAL — not a gate input`
  marker turns the same call into `::error::` (asserted by
  `test_historical_snapshot_without_marker_fails`);
- the two review snapshots went from 735 to 737 lines each, by heading prefix and one
  blockquote line; no table row, no entry and no count inside them changed;
- `python -m unittest discover -s scripts -p "test_check_bilingual*"` → `Ran 25 tests,
  OK` (was 15); `python -m unittest discover -s tests -p "test_check_bilingual*"` →
  `Ran 7 tests, OK`;
- `gate_ratchet.py` on the authority → `baseline=77 current=77 regressions=0 fixed=0`,
  `PASS`, exit 0; `check_bilingual_docs_full.py` → 77 violations, exit 1, as before;
- the gate itself, run after the commit with `BASE_SHA=origin/main` and
  `HEAD_SHA=` the branch head: `bilingual baseline: 77 frozen, 0 new gaps`, exit 0.

The assistant corrected one of its own choices before committing: the first version of
the historical notice counted every inventory-shaped entry in the file and reported
"100 entries", which is true file-wide but reads as a contradiction of the 81 in the
table and of the annotation it had just written. The notice now says
"file-wide" and reports the same three numbers it measures, so the prose and the
machine output do not disagree about what is being counted.

## Session reference status

NOT_RECORDED

No platform session identifier is available to this session, so `implementing_ai_session`
names the executing model (`opencode-go/deepseek-v4.1-flash`) rather than an
authenticated account, and the prompt snapshot carries
`executed_prompt_provenance: NOT_VERIFIED`. The artifact is a capture of the text as
received, not a signed artefact from the dispatching system.
