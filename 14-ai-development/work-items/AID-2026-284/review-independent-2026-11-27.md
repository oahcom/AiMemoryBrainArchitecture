# Independent Review Record — PR #1449

**Review date:** 2026-11-27  
**PR:** #1449 — `fix(ci): make the blob-pin negative sample and base binding able to fail (AID-2026-284)`  
**Branch:** `fix/aid268-negative-assertion`  
**Work item claimed:** `AID-2026-284`  
**Exact reviewed head:** `26d333d3dcaecc89b27817217702624ad963aa2f`  
**Recorded PR base:** `main@168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab`  
**Current main at review time:** `cb5b3dcd23ff86e10a354bb27b668dce19e95f62`  
**Merge base:** `7fc4ddabe1ea3b216b4536c0f5cb0a0c84306f19`  
**PR state:** OPEN, draft=false, merged=false, mergeable_state=dirty  
**Reviewer:** Independent reviewer; did not implement the change under review.

---

## 1. Review scope and independence

This review evaluates PR #1449 at the exact head SHA recorded above.

The review is based exclusively on the supplied execution evidence, Git object comparisons, workflow inspection, test results, and GitHub REST observations.

The reviewer did not implement the change. No claim is made that the reviewer independently executed the commands. All command outputs below are attributed to the independent reviewer's recorded execution evidence.

The review distinguishes three separate questions:

1. Does the negative assertion actually make the CI step fail when the checker accepts a known-bad sample?
2. Does the resolver bind the scan base to the merge candidate rather than stale event-time metadata?
3. Can this PR be merged into current main without violating repository work-item uniqueness?

The first two questions concern the code fix. The third concerns the actual mergeability and repository integration state.

## 2. Environment and method

**Execution environment**

- Windows 11
- PowerShell
- Python 3.12.12
- PyYAML 6.0.3
- Git for Windows
- No WSL
- Python commands executed with `python -X utf8`
- GitHub REST accessed through the local proxy

**Worktree arrangement**

- Exact reviewed head: scratch worktree at `26d333d3`
- Pre-fix implementation: detached worktree at `7fc4ddab`
- Review branch worktree: based on current main `cb5b3dcd`
- Synthetic PR merge candidate: two-parent commit with parents `cb5b3dcd` and `26d333d3`

**Review methods**

- Compared the PR's three commits against their merge base.
- Executed both newly added unittest suites.
- Executed the negative assertion against the real checker and immutable negative-sample commit.
- Executed the delivered workflow step against both the real checker and a deliberately false-accepting checker.
- Compared pre-fix and delivered workflow behavior using the same false-accepting checker.
- Built an independent adversarial Git fixture for merge-candidate base resolution.
- Compared baseline blob object IDs and baseline item sets.
- Inspected workflow YAML validity and script imports.
- Compared the PR tree against current main and inspected the PR timeline and close/reopen history.

## 3. Per-claim assessment

| Claim | Verdict | Concrete evidence and assessment |
|---|---|---|
| (a) Negative assertion can fail | **PASS** | E3: Running `python -X utf8 scripts/ci/assert_manifest_blob_pin_negative.py --commit 9a2063ae1fa5d905b3817cd4eddba065a06daa73` produced `NEGATIVE_ASSERTION_PASS: immutable sample rejected; manifests=108 pins=168 ok=82 mismatch=86 path_missing=0 incomplete=0`, exit 0. E5: With the checker modified to return 0 unconditionally, the delivered workflow step printed `VIOLATION: negative sample was not rejected; checker exit=0, expected=1` and `VIOLATION: immutable negative sample was not rejected with expected evidence`, exit 1. Restoring the checker restored `STEP_PASS ...`, exit 0. This directly demonstrates that the delivered assertion can fail when the checker silently accepts the known-bad sample. |
| (b) Base resolution binds to the merge candidate | **PASS** | E4: With `GITHUB_EVENT_NAME=pull_request`, `GITHUB_REF=refs/pull/1449/merge`, and `GITHUB_SHA=M`, the delivered step printed `Resolved merge-candidate base: cb5b3dcd23ff86e10a354bb27b668dce19e95f62`. E7: An independent fixture with event-time base B1, advanced target B2, feature head F, and synthetic merge M produced `pr_resolved=e32e1e87f409cb9865e150a5c3f5dda1e288dd8f`, `pr_is_advanced_target=True`, and `pr_is_stale_base0=False`. The resolver therefore uses the first parent of the two-parent merge candidate rather than the stale event-time base. |
| (c) No silent relaxation (baseline byte-identical, mismatch count equal) | **PARTIAL** | E8: `git rev-parse` returned the same baseline blob object ID at both commits: `c0ad3023b45a9f4f56f614d44451e20c5d1910f1`. The baseline item-set comparison reported `baseline_items=91 actual_items=91 stale_in_baseline_not_actual=0 new_in_actual_not_baseline=0` for both head and current main. The checker reported `mismatch=89 path_missing=2` at both head and current main. This supports no baseline relaxation and no change in mismatch count. However, E12 establishes that the workflow still tolerates `base_status == 1`; only the candidate scan is ratcheted. A mismatch introduced only on the base side is therefore not asserted. The broader claim of no silent relaxation is not fully established. |
| (d) Close reason recorded | **PASS** | E10: The 07:33:25Z comment explicitly records closure because the AID-2026-284 carrier directory already existed on main and the PR produced add/add conflicts. The 07:54:58Z comment preserves the duplicate-carrier ruling and specifies merge-first/close-after-superseding-PR policy. The 07:58:01Z owner ruling assigns the negative-sample and base-binding tests to #1451 as supplementary evidence and states that #1449 closes as superseded once #1451 absorbs and proves them on its candidate tree. |
| (e) Scope discipline / stdlib-only / Windows | **PASS** | E1: The three-commit diff changes exactly ten files: one workflow, four work-item documents, one index, two implementation scripts, and two test files. No baseline, checker, or other gate script is modified. E11: Imports are standard-library-only. Both scripts and both test suites ran under Python on Windows. YAML parsing succeeded and identified one job, `repository-hygiene`. E2: The two test suites completed with `Ran 14 tests in 7.759s`, `OK`, exit 0. |

### Claim assessment details

#### (a) Negative assertion

The decisive evidence is E5, not merely the successful execution of the assertion against the real checker.

The checker was deliberately changed to return 0 for the immutable negative sample. The delivered workflow step then failed with exit 1 and an explicit violation message.

This establishes the intended failure behavior for the tested regression scenario.

The assertion's successful result against the unmodified checker is also supported by E3.

#### (b) Merge-candidate base resolution

The delivered workflow derives its base through:

`BASE_SHA="$(python3 scripts/ci/resolve_manifest_blob_pin_base.py)"`

The resolver is invoked under `set -euo pipefail`, so resolver exit 2 aborts the step.

E4 demonstrates the expected first-parent resolution in a PR-shaped execution. E7 independently tests an advanced target branch and confirms that the resolver selects B2 rather than stale B1.

The resolver also fails closed for the tested invalid conditions:

- All-zero push before-SHA sentinel.
- Pull-request event without a two-parent synthetic merge commit.
- Invalid pull-request merge ref.
- Three-parent octopus commit.
- Unknown SHA.
- Shallow clone without available parent information.

Each tested condition returned exit 2.

#### (c) Baseline and mismatch preservation

The baseline blob is byte-identical between reviewed head and current main, as established by the identical Git object ID.

Both commits also have identical baseline item sets and the same checker mismatch and missing-path counts.

However, this is not equivalent to proving that every base-side mismatch is rejected by the workflow.

The workflow still accepts base checker status 1. This is a remaining gate limitation, not a baseline-file modification introduced by this PR.

#### (d) Close reason

The recorded history contains two distinct but consistent rulings:

1. The PR cannot carry a second `AID-2026-284` work-item directory because current main already contains that identifier for a different work item.
2. The supplementary tests are to be absorbed into PR #1451, the designated blob-pin checker carrier.

The latter is an explicit supersession condition, not evidence that #1449 has already been superseded by a merged change.

#### (e) Scope and portability

The PR does not modify the checker implementation or its baseline.

Its implementation changes are confined to the workflow and two new helper scripts, accompanied by their tests and work-item documentation.

The supplied Windows execution evidence establishes compatibility in the stated Windows/Python environment. It does not establish successful execution on GitHub-hosted Ubuntu runners.

## 4. Findings

### F-01 — Critical: PR cannot merge because its work-item identifier collides with current main

**Evidence:** E9, E10.

Current main already contains:

`14-ai-development/work-items/AID-2026-284/`

That directory represents a different work item:

`REQ-04 AC1 scope confirmation superseding the ineffective AC8 exclusion`

Its status is `DISPATCHED`, and its five files include `scope-confirmation.md`.

The reviewed PR introduces another directory under the same identifier, containing four different files:

- `evidence.md`
- `manifest.yaml`
- `prompt-v1.md`
- `session-evidence.md`

The independent merge-tree result is:

```text
CONFLICT (add/add): Merge conflict in 14-ai-development/work-items/AID-2026-284/evidence.md
```

The same add/add conflict is reported for:

- `manifest.yaml`
- `prompt-v1.md`
- `session-evidence.md`

The GitHub REST state independently reports:

`mergeable_state=dirty`

**Impact**

The PR cannot be merged as-is. Its claimed work-item identifier is already occupied by a different carrier on current main.

This is a repository-level identity collision, not a routine content conflict that can be resolved by choosing one side of the same document.

The PR's code fix may be valid while its current carrier is invalid.

**Recommendation**

Do not merge PR #1449 in its current form.

The blob-pin change must be carried by the designated unique work item on the current main lineage. Per the recorded owner ruling, PR #1451 is the sole blob-pin checker carrier.

Transfer the supplementary negative-sample and base-binding tests into #1451, prove them on that PR's own candidate tree, and close #1449 as superseded only after the replacement carrier has absorbed and proven the evidence.

Do not create a second `AID-2026-284` carrier.

### F-02 — Medium: A resolver test is vacuous with respect to its named stale-event-base property

**Evidence:** E12, observation 1.

`test_pull_request_ignores_stale_event_time_base` sets:

`GITHUB_EVENT_PULL_REQUEST_BASE_SHA`

The resolver does not read that environment variable.

The actual event-time base was previously supplied through the workflow expression, not through this variable.

**Impact**

The test passes without establishing the property its name claims to test.

Its success must not be counted as independent evidence that the resolver ignores a real event-time base input.

This does not invalidate the resolver's demonstrated first-parent behavior: `test_pull_request_uses_merge_candidate_first_parent` and the independent adversarial fixture in E7 provide relevant evidence for that behavior.

**Recommendation**

Remove the unused environment variable from the test or replace the test with one that constructs an actual stale event-time base input through the production workflow interface.

The test should fail if the resolver is changed to use the stale event-time base instead of the merge candidate's first parent.

### F-03 — Medium: Base-side checker mismatches remain tolerated

**Evidence:** E12, observation 2.

The modified workflow still tolerates:

`base_status == 1`

Only the candidate scan is ratcheted.

**Impact**

A mismatch introduced only on the resolved base side is not asserted by the workflow.

Consequently, the merge-candidate base resolution improvement does not establish that base-side mismatch regressions are rejected.

This is pre-existing workflow behavior, not a newly introduced baseline modification.

**Recommendation**

Record the base-side mismatch tolerance explicitly as a remaining gate limitation.

If the intended contract is that both base and candidate scans must enforce the ratchet, add an explicit base-side assertion and regression test.

Do not characterize the present workflow as enforcing a two-sided ratchet.

### F-04 — Low: Negative assertion hard-codes checker output details

**Evidence:** E12, observation 3.

The negative assertion hard-codes the summary string and:

`len(mismatches) == 86`

for the immutable negative-sample commit.

**Impact**

A legitimate future change to checker output structure or diagnostic formatting can break the assertion even if the checker still correctly rejects the immutable sample.

This creates an intentional maintenance dependency between the negative fixture and checker output representation.

**Recommendation**

Keep the immutable fixture and its expected rejection behavior.

Document the output-shape dependency and require explicit review whenever the checker output or fixture expectations change.

Where practical, prefer stable structured evidence over formatting-sensitive summary matching, without weakening the requirement that the known-bad sample must be rejected.

### F-05 — Info: Conflicting PRs fail closed before base resolution can complete

**Evidence:** E12, observation 4.

The resolver requires a two-parent synthetic merge commit for pull-request events.

A conflicting PR for which GitHub has not produced a synthetic merge candidate therefore exits 2.

PR #1449 itself currently has a dirty merge state.

**Impact**

The workflow can fail because no merge candidate exists, independently of the blob-pin checker result.

This is fail-closed behavior and does not establish a defect in the resolver's selection of a valid candidate's first parent.

**Recommendation**

Retain the fail-closed behavior unless the repository explicitly defines an alternative trusted base-resolution mechanism for conflicting PRs.

Make the failure reason distinguishable from a blob-pin violation in CI diagnostics.

### F-06 — Info: The negative assertion uses a different Python invocation spelling

**Evidence:** E12, observation 5.

The assertion invokes the checker through `sys.executable`; the surrounding workflow invokes `python3`.

The supplied Ubuntu runner assumption makes these the same interpreter.

**Impact**

No defect was observed.

**Recommendation**

No change required based on the supplied evidence.

## 5. Overall verdict

# NEEDS REVISION

The core code fix verifies against the supplied evidence.

In particular:

- The negative assertion demonstrably fails when the checker accepts the immutable known-bad sample.
- The resolver demonstrably selects the merge candidate's first parent rather than a stale event-time base.
- The new scripts and tests are standard-library-only and passed the supplied Windows execution checks.
- The baseline is byte-identical and mismatch counts are unchanged.

However, **the PR is not mergeable as-is**.

Current main already contains a different work item under `AID-2026-284`. The reviewed PR introduces a second carrier with the same identifier, producing add/add conflicts and a dirty GitHub merge state.

This is a blocking repository-integrity issue regardless of the correctness of the code fix.

The owner has already ruled that the tests are supplementary evidence for #1451, the sole blob-pin checker carrier. That transfer and proof must occur before #1449 can be closed as superseded.

The review also records two remaining quality limitations: a vacuous stale-base test and the continued tolerance of base-side mismatches.

**Disposition:** Do not merge #1449. Preserve its validated technical findings, transfer the supplementary tests into #1451 as directed, and close #1449 as superseded only after the designated replacement carrier has absorbed and proven them.

## 6. Limitations

The following were not executed or established by the supplied evidence:

1. **Real GitHub Actions execution on `ubuntu-latest`.** Workflow YAML parsing and local execution do not establish successful execution in an actual GitHub-hosted runner.
2. **A real GitHub-generated merge candidate.** E4 used a synthetic two-parent merge commit. E7 used an independently constructed Git fixture. Neither is an actual GitHub-generated merge candidate.
3. **Network-dependent fetch behavior.** The review did not establish the behavior of the delivered workflow against a live GitHub fetch under all network and authentication conditions.
4. **Full ratchet gate on Linux.** The complete ratchet gate was not executed on Linux.
5. **Successful merge of PR #1449.** The supplied merge-tree and REST evidence establish that the PR is dirty and has add/add conflicts. No successful merge was demonstrated.
6. **Completion of supersession by PR #1451.** At review time #1451 was OPEN, not merged, and current main did not contain either new helper script.
7. **All possible GitHub event variants.** The resolver's tested fail-closed edge cases are limited to those enumerated in E7.
8. **Behavior under every future checker output change.** The hard-coded negative evidence was validated for the supplied immutable sample and checker output, not for future output formats.

These limitations do not negate the specific positive results established by E2–E8.

## 7. Evidence index

The following commands and operations were recorded as executed by the independent reviewer.

| Evidence | Command or operation | Purpose |
|---|---|---|
| E1 | `git diff --numstat 7fc4ddab 26d333d3` | Establish PR commit scope and changed files. |
| E2 | `python -X utf8 -m unittest scripts/ci/test_resolve_manifest_blob_pin_base.py scripts/ci/test_assert_manifest_blob_pin_negative.py` | Execute both new test suites. |
| E3 | `python -X utf8 scripts/ci/assert_manifest_blob_pin_negative.py --commit 9a2063ae1fa5d905b3817cd4eddba065a06daa73` | Verify rejection of the immutable negative sample by the real checker. |
| E4 | Extract delivered workflow step and execute under Git Bash with a synthetic two-parent merge candidate and PR-shaped environment. | Verify first-parent base selection and normal delivered-step behavior. |
| E5 | Replace checker return expression with `return 0`; execute the same delivered workflow step; restore checker afterward. | Verify that the negative assertion fails when the checker falsely accepts the negative sample. |
| E6 | Extract pre-fix workflow step from `7fc4ddab`; execute with stale base and the same false-accepting checker. | Independently reproduce pre-fix false-green behavior. |
| E7 | Construct independent Git fixture with B1, F, B2, and synthetic M; execute resolver against normal and adversarial conditions. | Verify advanced-target first-parent resolution and fail-closed edge cases. |
| E8 | `git rev-parse <commit>:scripts/ci/baselines/manifest-blob-pins.txt`; execute checker at reviewed head and current main; compare baseline item sets. | Verify baseline blob identity and unchanged mismatch counts. |
| E9 | `git merge-tree --write-tree cb5b3dcd 26d333d3` | Establish current-main add/add conflicts. |
| E9 | Git tree inspection of `14-ai-development/work-items/` on current main. | Establish existing, different AID-2026-284 carrier. |
| E10 | GitHub REST PR timeline and comments. | Establish close/reopen history and owner supersession ruling. |
| E11 | `yaml.safe_load` on modified workflow; inspect script imports; execute scripts and tests under Windows Python. | Verify YAML validity, standard-library-only imports, and Windows compatibility. |
| E12 | Source inspection of resolver tests, workflow status handling, negative assertion, and interpreter invocation. | Record vacuous test, base-side mismatch tolerance, hard-coded evidence, and fail-closed merge-candidate requirement. |

---

**Final disposition: NEEDS REVISION**
