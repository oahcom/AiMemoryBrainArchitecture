---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "Every command and count in the output section was run on this branch. The required-context count of fifteen was read from the live branch-protection payload on 2026-11-25, and the absence of rust-workspace-test on #1024 was read from that pull request's own check runs."
    usage_status: Active
    modification_status: Unchanged
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

# Session role / use case

IMPLEMENTER. Implement stage A of WO-01 for REQ-01 / Issue #262: make
`rust-workspace-test` run on every pull request targeting `main`, so that the
context exists on every Head before anyone makes it required.

This work item deliberately does **not** change `14-ai-development/PR-GOVERNANCE-001.md`,
does **not** apply the branch-protection update, and does **not** run the
deliberately-failing-head experiment. The first was in the original scope and was
removed; see "Scope revision" below. The other two are separate platform actions.

# Actual AI input

Two classes of input exist for this session and they are not interchangeable.

**Committed, byte-exact.** `prompt-v1.md` in this directory is the consolidated
instruction set for the delivered change, assembled from the two ruling rounds
that produced it. It is the file the manifest pins by digest.

**Recorded, not committed.** The session was driven by two prompt files held
outside the repository. Their sizes are recorded so a reader can ask for the
originals rather than trust a summary:

| # | prompt file | bytes | what it asked for |
|---|---|---:|---|
| 1 | `144-req01-r30-wo01.md` | 9,821 | exact patch spec for the workflow trigger, the §7 declaration, the protection payload and the experiment protocol |
| 2 | `145-req01-r31-prbody.md` | 7,044 | compliant PR body and evidence carrier, after three gates rejected the first attempt |

`prompt-v1.md` was assembled after the session from those files. The manifest
therefore records `executed_prompt_provenance: NOT_VERIFIED`: the digest proves
the committed file has not changed since it was pinned, not that it is
byte-for-byte what the ruling session received.

Two standing directives governed the whole session and are reproduced verbatim
because the acceptance criteria are stated against them:

> 你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可。

> 不能自己动手写代码。

# AI-visible output

One production file changed:

```
.github/workflows/rust-phase1.yml              43 -> 38 lines
```

The `pull_request` trigger no longer filters on changed paths; `push.paths` is
untouched; the job id is untouched, so the produced check context is still
`rust-workspace-test`.

Two governance records are added, and one index row:

```
14-ai-development/work-items/AID-2026-061/manifest.yaml
14-ai-development/work-items/AID-2026-061/prompt-v1.md
14-ai-development/work-items/AID-2026-061/session-evidence-wo01.md
14-ai-development/work-items/INDEX.md          one existence row
```

Verification actually run on the pull request branch, at the stated head:

```
python3 scripts/check_declared_check_contexts.py
    ::notice::12 declared check contexts, all produced by a job in .github/workflows
    DECLARED CHECK CONTEXTS: PASS

python3 scripts/ci/check_repository_hygiene.py --base <merge-base> --head <head>
    Work-item index membership version=2026-11-24.7 directories=49 linked=49
    Work-item manifest consistency version=2026-11-24.7 ... violations=0
    Repository new-file admission passed: 3 new path(s) checked.
```

The declared-context count in that output is twelve because this branch does not
touch §7. Twelve is also what §7 says on `main`, and it is **not** what the
platform requires. That gap is measured under "Limitations".

One check result was observed on the pull request rather than asserted:

```
rust-workspace-test   completed   success
```

That result is evidence that the trigger change works on this Head, which is one
that touches `.github/workflows/rust-phase1.yml` and therefore matched the old
filter as well. It is **not** evidence that the context is required, and it is
**not** evidence that a failing required check blocks a merge.

# Scope revision

The original scope of this work item also rewrote `PR-GOVERNANCE-001` §7 from
twelve declared contexts to fourteen. Pull request #1018 was closed unmerged at
`2026-11-25T01:58:46Z` with an Owner ruling that the document half must not land
before the platform half, on the ground that the document would then claim an
enforcement the platform did not have.

The close was accepted and the scope was narrowed to the workflow trigger alone.
The reasons the narrowing is a split rather than an abandonment:

1. The platform cannot safely gain `rust-workspace-test` first. On `2026-11-25`
   the required set held fifteen contexts, and a merged docs-only pull request
   (#1024, six markdown files, none under `crates/`) produced exactly those
   fifteen check runs — `rust-workspace-test` was absent from its Head. Making
   that context required before the trigger change lands would leave every
   pull request that does not touch `crates/**` waiting forever on a check that
   is never scheduled.
2. The document half is not abandoned, only deferred. It is gated on a
   measurement that can only be taken after the protection payload has been
   changed, and it must state the measured count with a date.

The consequence is recorded rather than hidden: `prompt-v1.md` still asks for the
§7 edit, because it is a snapshot of what the ruling session was asked for and is
not rewritten after the fact. The delivered change is narrower than the prompt.
That divergence is this section.

# Limitations

The Session Evidence gate validates evidence structure and file integrity. It
does not independently establish that this narrative is true or complete.

Three properties of this delivery are stated here rather than left for a reader
to discover:

1. **`main` already understated the required set.** `PR-GOVERNANCE-001` §7
   declares twelve required contexts. The live protection payload on
   `2026-11-25` returned fifteen: the twelve plus `Session Evidence`,
   `Session Evidence self-test (base)` and `Session Evidence self-test (head)`.
   This work item does not fix that and does not claim it is fixed.
   **Superseded, `2026-11-25` (Issue #1029):** the count in §7 is no longer
   twelve and this paragraph is not a dated measurement of anything, so it
   must not be read as a current count. §7 is the only carrier of the number;
   read it, do not quote this sentence. The delta it described is closed —
   §7 now declares sixteen and the platform requires sixteen.
2. **A checks-cannot-block claim is still outstanding.** §7 records that the
   deliberately-failing-head experiment has not been run. This work item does not
   run it either; it prepares the condition under which the context can be made
   required without deadlocking pull requests.
   **Superseded, `2026-11-25` (Issue #1029, PR #1038):** the experiment has
   been run. PR #1038 added one always-failing `#[test]` at head `b5cf4f25`;
   `PUT /repos/oahcom/AiMemoryBrainArchitecture/pulls/1038/merge` returned
   HTTP 405 with `Required status check "rust-workspace-test" is failing.`
   and the pull request was closed unmerged. `PR-GOVERNANCE-001.md:288`
   records it as passed and dated `2026-11-25`. The boundary that record
   states applies here too: the experiment proves the normal path on that
   date with that payload, not that a bypass route or a renamed job behaves
   the same, and it must be re-run after any material change to the
   protection configuration or to the producing workflows — so this paragraph
   is a record of the state before the change, not a current claim.
3. **Configuration drift between the declaration and branch protection had no
   machine gate.** `scripts/check_declared_check_contexts.py` checks that every
   declared context is produced by a job. It did not read branch protection, so
   a declaration naming twelve contexts while the platform required fifteen
   passed every automated check in this repository.
   **Superseded, `2026-11-25` (Issue #1029):** that script now compares the
   declared set to `GET /branches/main` in both directions and exits 2
   (INCOMPLETE) when the payload cannot be read, so this gap is closed and the
   sentence above describes the state before the change.
