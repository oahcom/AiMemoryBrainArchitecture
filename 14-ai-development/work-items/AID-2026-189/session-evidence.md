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
        - "14-ai-development/work-items/AID-2026-189/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Records the dispatched task and what the implementing session did with it; the session identifier and the verbatim model input stream were not captured."
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
      - "ci"
      - "cache"
      - "concurrency"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Session Evidence — AID-2026-189

## Session role / use case

CI repair worker. The assistant was dispatched as a repair worker to finish three leftovers of
AID-2026-115: remove a Rust cache from a job that never compiles, add head-SHA `concurrency` to
two workflows the sweep missed, and record two further defects without repairing them.

## Actual AI input

The dispatching session supplied a worker contract with, in order:

- the fixed working directory `D:\code\wt-ci2` and branch `fix/2026-11-26-ci-leftovers`;
- four measured facts: AID-2026-115 merged as PR #1322 at `ac301e09`; the `fmt` job received a
  cache it cannot hit and went 8s → 21s on at least one run; `h-applied` and
  `publication-protocol` are push+PR dual-trigger and have no `concurrency`;
  `repository-hygiene.yml:149-152` fails a declared-but-unproduced context, and
  `check_declared_check_contexts.py` is one-job-one-context;
- three work items A/B/C, with C explicitly record-only;
- a prohibition list: no job merge, no job rename, no change to
  `check_declared_check_contexts.py` semantics, no `fetch-depth` change, no required-context
  deletion, no Issue close, no branch-protection change, no force push;
- the reporting shape and the merge discipline (sixteen contexts green on the exact head,
  behind = 0, merge method `merge`, blob verified afterwards).

The model serving this unit was `deepseek-v4.1-flash` because the primary upstream
(`9router_hermes`) was returning 429. That substitution is recorded here because it changes
which model produced the edits, not what was asked for.

## What the session did

1. Read the work tree first. It was **not** clean: `gates.yml`,
   `h-applied-delivery-evidence-conformance.yml` and `publication-protocol-reference-model.yml`
   already carried the A/B edits, uncommitted, from an earlier attempt in this branch. They were
   inspected against the brief rather than discarded or re-applied blind, and they matched
   (step removal, two concurrency blocks, head SHA, job sets unchanged). Nothing else was
   deleted.
2. Verified the edits with a YAML parse of both revisions: `jobs` keys identical on all three
   files; `jobs.fmt.steps` 5 → 3 with `clippy`, `doctest` and `rust-workspace-test` caches
   untouched; `concurrency` present on both topic workflows and absent before.
3. Took `AID-2026-189` after observing 170/172/173 merged and 183/186/188 open, and after
   confirming no PR title, remote branch or work-item directory carried 189.
4. Wrote this registration set and one INDEX row, then ran the repository's own gates locally.

## AI-visible output

The assistant reported, and the head of this branch confirms:

- `jobs.fmt` now runs three steps — `actions/checkout@v4`, `dtolnay/rust-toolchain@stable`
  (with `components: rustfmt`) and `Verify repository formatting at this commit` — where the
  base revision ran five; the removed pair is `Record resolved Rust toolchain version` and
  `Cache Rust dependencies and build artifacts` (`Swatinem/rust-cache@v2`, `shared-key:
  gates-fmt`). The three Rust jobs that do compile keep their cache and probe steps;
- a YAML parse of both revisions shows identical `jobs` key lists in all three files:
  `gates.yml` `['protocol-index', 'conformance', 'schema-nonempty', 'bilingual', 'clippy',
  'doctest', 'fmt']`, `h-applied-delivery-evidence-conformance.yml`
  `['applied-delivery-evidence']`, `publication-protocol-reference-model.yml`
  `['publication-protocol-reference-model']` — so no job was added, renamed, merged or removed;
- the two topic workflows carry the top-level block
  `concurrency: {group: ${{ github.workflow }}-${{ github.event.pull_request.head.sha || github.sha }}, cancel-in-progress: true}`
  at the head and no `concurrency` at all at the base revision;
- `check_declared_check_contexts.py` returned `DECLARED CHECK CONTEXTS: PASS` — "16 declared
  check contexts, all produced by a job in .github/workflows and all required on main";
- `check_document_management.py --require-changed origin/main` returned
  `PASS (incremental): no GOV-DOC-002 violations; 496 classified, 446 unclassified`, and the
  metadata parser in that module returns a mapping, not `None` and not a `ParseError`, for
  `evidence.md`, `prompt-v1.md` and `session-evidence.md` — all three use block-style YAML, no
  flow mapping opens on `{`;
- nothing under `scripts/`, `00-governance/`, `tests/` or the branch-protection payload was
  touched; the change is three workflow files, four new work-item files and one appended
  `INDEX.md` row.

This unit was served by `opencode-go/deepseek-v4.1-flash` after both 9router routes returned
429 on three earlier dispatches; the substitution changes which model produced the text, not
what was asked for, and it is recorded here because the earlier attempts are otherwise
indistinguishable from this one in the git history.

## Attribution and independence

- Attribution: user-authorized operator, delegated by the account owner.
- Independent review: NOT_ASSIGNED. No APPROVE, acceptance or natural-person signature is
  represented by this file or by the PR.
- The session that wrote these files is the session that describes them; that is disclosure, not
  independence.
