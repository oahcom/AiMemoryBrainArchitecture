# Session role / use case

IMPLEMENTER. Implement WO-01 for REQ-01 / Issue #262: make `rust-workspace-test`
run for every pull request targeting `main`, declare the two new required check
contexts in `PR-GOVERNANCE-001` §7, and preserve every existing governance gate.

This work item does **not** perform the branch-protection update and does **not**
run the deliberately-failing-head experiment. Both are separate platform actions
that follow the merge of this pull request.

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

Two production files changed, both already on the pull request branch:

```
.github/workflows/rust-phase1.yml              43 -> 38 lines
14-ai-development/PR-GOVERNANCE-001.md         6 lines changed
```

The workflow change removes `pull_request.paths` and keeps `push.paths`, so every
pull request targeting `main` now produces a `rust-workspace-test` result. The
job title is unchanged, so the check context name is still the job id.

The §7 change raises the declared required-context count from twelve to fourteen,
appends `rust-workspace-test` and `Session Evidence` to the machine-read
declaration block, and updates the English and Chinese prose in the same file.

Verification actually run on the pull request branch, at the stated head:

```
python3 scripts/check_declared_check_contexts.py
    ::notice::14 declared check contexts, all produced by a job in .github/workflows
    DECLARED CHECK CONTEXTS: PASS
```

One check result was observed on the pull request rather than asserted:

```
rust-workspace-test   completed   success
```

That result is evidence that the trigger change works. It is **not** evidence
that the context is required, and it is **not** evidence that a failing required
check blocks a merge. Both of those remain unproven until branch protection is
updated and the deliberately-failing-head experiment has actually been run.

# Limitations

The Session Evidence gate validates evidence structure and file integrity. It
does not independently establish that this narrative is true or complete.

Two properties of this delivery are stated here rather than left for a reader to
discover:

1. **A checks-cannot-block claim is still outstanding.** `PR-GOVERNANCE-001` §7
   records that the deliberately-failing-head experiment has not been run. This
   work item does not run it either; it prepares the conditions under which it
   can be run.
2. **Configuration drift between the declaration and branch protection has no
   machine gate.** `scripts/check_declared_check_contexts.py` checks that every
   declared context is produced by a job. It does not read branch protection, so
   a declaration naming fourteen contexts while the platform requires twelve
   would pass every automated check in this repository.
