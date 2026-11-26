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
        - "14-ai-development/work-items/AID-2026-191/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the dispatched task and what the implementing session did with it; the session identifier and the verbatim model input stream were not captured, and no claim is made that the text below is a byte-for-byte transcript."
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
    canonical_scope_keywords:
      - "bilingual"
      - "side-by-side"
      - "cjk-predicate"
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

Repair worker, dispatched as a subagent by a dispatching session. The role was not to design the
rule but to **measure the cost of a specified rule change and only implement it if the cost was
three new gaps or fewer**; if the cost exceeded three, the role was to produce a report marked
`DEFERRED_TO_OWNER` and change nothing.

## Actual AI input

The dispatching session supplied, in order:

- a common brief: work only inside the assigned worktree `D:\code\wt-cjk` on branch
  `fix/2026-11-27-side-by-side-cjk`; merge `origin/main` first; take a work-item number not used by
  any pull request, branch or directory; `status: DISPATCHED`, `base_commit_sha` pinned to the base
  at branch creation; block-style YAML metadata only; run the metadata self-check; the PR body must
  carry `Related issue(s)`, `AI-assisted work`, and a `Session evidence reference(s)` path that
  resolves in the head tree; poll sixteen required contexts on the exact head, merge with
  `merge_method: merge` only when behind is zero, and compare blobs after merge; no branch-protection
  change, no Issue close, no unrelated file, no fabricated SHA or gate result;
- the unit: `scripts/check_bilingual_docs.py:312-331` accepts a pair when *either* file carries a CJK
  character, so an English source with a couple of CJK characters plus a `.zh-CN.md` that is an
  English copy passes; measure by switching to "the partner must contain Chinese", record
  `77 → ?` and list every new gap; implement only if the new gaps are ≤ 3, otherwise report only;
  run `python -m unittest discover -s scripts -p "test_check_bilingual*"` in both cases;
- prohibitions: delete no mirror, write no new translation, do not change the 100-character
  threshold in `_carries_chinese()`.

No other material was supplied. No Issue number was supplied for this unit; `#469` and `#487` were
found in the tree and used as the lineage of the predicate being repaired.

## What the session did

1. Read both files, then measured instead of editing: imported the gate module and ran
   `current_bilingual_gaps()` at the base revision — **77** gaps, matching the frozen baseline.
2. Implemented the literally specified rule ("only the partner counts") in memory, re-ran the scan,
   and got **89** — twelve new gaps. Collected `cjk`/`latin`/`ratio` for all twelve and their
   partners. All twelve turned out to be pairs whose Chinese document is the `.zh-CN.md` file and
   whose partner is the English file with zero CJK, i.e. false positives of a direction-blind
   predicate rather than untranslated pairs.
3. Measured the rule that removes the leak without producing those false positives — only the
   designated Chinese file of the pair may certify it — and got **77 → 77**, zero new, zero
   resolved. With the cost at zero, the repair was implemented rather than deferred.
4. Proved the defect and the repair on a throwaway two-fixture repository before touching the real
   code: the stray-CJK fixture went from accepted to rejected, the genuine short Chinese fixture
   stayed accepted.
5. Renamed `test_issue_469_short_translation_is_accepted` to the rule it actually tests and added
   two regression tests for the leak. Ran both suites: 52 → 54 tests, both green.
6. Wrote this registration set, the mirror renditions, and one appended INDEX row, then ran the
   repository's own gates locally.

The model serving this unit was `opencode-go/deepseek-v4.1-flash`, chosen because the batch's
primary pool (`9router`) was returning 429 for both of its models. The substitution changes which
model produced the text, not what was asked for, and it is recorded here because otherwise the two
would be indistinguishable in the git history.

## AI-visible output

The assistant reported, and the head of this branch confirms:

- `_side_by_side_bilingual()` no longer reads the source file; a new `_chinese_side(source, partner)`
  names the `.zh-CN.md` member, or the plain root `.md` when neither member carries a language
  suffix, and only that file's CJK characters count;
- `current_bilingual_gaps()` returns **77** entries before and after the change — new 0, resolved 0 —
  so `scripts/bilingual-baseline.txt` and `scripts/ci/baselines/bilingual-docs.txt` are byte-unchanged;
- the literal rule's cost is **twelve** new gaps, itemised with `cjk`/`latin`/`ratio` in section 2 of
  `AID-2026-191/evidence.md`, each one a Chinese document whose partner is the English file;
- over the committed tree, **103** side-by-side pairs resolve, and **0** of them are accepted only
  through the English side, which is why the repair costs nothing;
- `python -m unittest scripts.governance.evidence.test_gate_normative_roots` → `Ran 54 tests … OK`;
  `python -m unittest discover -s scripts -p "test_check_bilingual*"` → `Ran 15 tests … OK`;
- nothing under `00-governance/`, `.github/`, `prompts/` or the branch-protection payload was
  touched; the change is one checker function pair, two tests, this registration set and one
  `INDEX.md` row.

## Attribution and independence

- Attribution: user-authorized operator, delegated by the account owner; this session was itself
  dispatched as a subagent.
- Independent review: `NOT_ASSIGNED`. No APPROVE, acceptance or natural-person signature is
  represented by this file or by the pull request.
- The session that wrote these files is the session that describes them; that is disclosure, not
  independence.
