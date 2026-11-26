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
        - "14-ai-development/work-items/AID-2026-188/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
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

# Session Evidence — AID-2026-188

## Session role / use case

Verification worker inside a dispatched repair contract. The assistant was dispatched to
add `"03-memory-brain"` to `NORMATIVE_ROOTS`, synchronise any second root inventory,
register three canonical documents in the document scope registry, leave both frozen
baselines untouched, keep the bilingual gate and the AID-2026-172 unit tests green, and
publish a work item with one `INDEX.md` row as a pull request.

The first three of those goals describe a state that was already present at the stated
base. The assistant therefore measured the state before editing, made no change to any
checker, baseline, registry or mirror, and published the measurement itself as the work
item. The role it performed was verification and premise correction, not repair.

## Actual AI input

The dispatched contract instructed the assistant to:

- work only in the existing worktree `D:\code\wt-norm03` on branch
  `docs/2026-11-26-normative-root-03`, create no worktree, and never delete another
  session's files;
- treat `NORMATIVE_ROOTS` as holding 13 entries that do not include `03-memory-brain`,
  and add that root in the existing format and ordering;
- look for a second root inventory such as `check_bilingual_docs_full.py` and
  synchronise it, or record that only one definition exists;
- change neither baseline's contents and never regenerate them, then run the herald
  gate with `PYTHONUTF8=1` and confirm exit 0 with 77 entries;
- run the AID-2026-172 unit tests, which add 15 cases including
  `check_baseline_copies_agree()` and the baseline write refusal, and must stay green;
- register the three canonical documents in `00-governance/document-scope-registry.yaml`
  in the existing format, adding three entries if `documents:` is exact-equality;
- create a new work item with a block-style YAML metadata block so that
  `read_metadata()` returns a mapping, allocate a number from
  `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls?state=all&per_page=100`, and avoid
  numbers that appeared in any PR title or branch;
- open a pull request containing `Related issue(s): #1212`, `AI-assisted work: YES` and a
  session evidence reference, merge with the `merge` method only after 16 of 16 required
  contexts are green on the exact head with branch behind == 0, and verify blobs after
  the merge;
- make no change to baseline contents, no change to checker decision semantics beyond one
  root entry, no restoration of the other ten canonical documents, no mirror deletion,
  no Issue closure and no force push.

The environment constraints stated with the contract were that `PYTHONUTF8=1` is required
on this host because the GBK console codepage breaks decoding of captured `git` output,
and that an initial `mergeable_state=dirty` produces zero pull-request check runs, so
`git merge --no-ff origin/main` must precede the push rather than a wait.

The contract text is pinned verbatim in `prompt-v1.md` (5934 bytes, SHA-256
`e0741732d3bd920e93729ecbd088cccc9bed2145c0e679891733f0aa804df9d2`). No prompt-library
registration exists for it, so `prompt_status` is `NOT_RECORDED`.

## AI-visible output

The assistant reported, and the repository confirms on the head of this branch:

- the first three goals were already satisfied at base: `NORMATIVE_ROOTS` holds 13
  entries including `03-memory-brain` (`scripts/check_bilingual_docs.py:20`, attributed
  by `git blame` to `6ab36b3697a0994d8de449d2b9c344f23aac0fda`); the measured tuple is
  `13 True 77 77 0 0 []` for root count, membership, gaps, baseline, new, gone and copy
  agreement; `memory-brain gaps` is empty;
- `check_bilingual_docs_full.py` holds no second literal: it imports `NORMATIVE_ROOTS`,
  derives `_DERIVED_ROOTS` from the tree and exits 2 when the two disagree, so only one
  definition exists and nothing needed synchronising;
- the registry already declares `03-memory-brain` as a governed root at line 50 and has
  no `documents:` key at all; `check_document_management.py` reports
  `03-memory-brain: 3/3 classified`, so per-file registration was neither owed nor
  expressible through `governed_files:`, which means "file outside a governed directory";
- no file under `scripts/`, `00-governance/`, `.github/`, `03-memory-brain/` or
  `docs/*/03-memory-brain/` was modified; the change is six new work-item files and one
  appended `INDEX.md` row;
- local gate runs used `PYTHONUTF8=1` and passed: bilingual gate `PASS (7 changed paths
  inspected)`, `check_document_management.py --require-changed 1e9341da`
  `PASS (incremental)`, repository hygiene `new-file admission passed: 6 new path(s)`,
  line endings `0 violations`, manifest parse `93 parsed, 0 failed`, session evidence
  workflow shape `PASS`, governance operation traceability `PASS (7 x 3 mirrors)`,
  traceability `0 errors`;
- unit tests: `Ran 15 tests ... OK` in `scripts/` and `Ran 7 tests ... OK` in `tests/`.

The assistant made three incremental corrections to the pull-request body, each because
the Session Evidence context rejected the previous text: the linked Issue #1212 had to be
declared `LEGACY_UNDECLARED` with `N/A`, the session evidence reference had to be the full
repo-relative path rather than the dispatched short form, and once the path resolved the
validator required this document to carry the `Session role / use case`,
`Actual AI input` and `AI-visible output` sections it now has. Each correction is a
statement about the body text or this document, not about the repository content.

## Session reference status

NOT_RECORDED

No platform session identifier is available to this session, so `implementing_ai_session`
names the executing model (`opencode-go/deepseek-v4.1-flash`) rather than an authenticated
account, and the prompt snapshot carries `executed_prompt_provenance: NOT_VERIFIED`. The
artifact is a verbatim capture of the text as received, not a signed artefact from the
dispatching system.
