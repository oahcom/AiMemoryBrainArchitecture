---
document_metadata:
  domain: ai-development
  role: guide
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "The clippy rationale in §2.3 was re-measured on 2026-11-23 against the GitHub Actions REST API: rust-phase1.yml now executes clippy on hosted runners, first at run 45037267638. The quoted run ids and step conclusions were read from that API in this session."
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
> **CI runner update — 2026-11-23:** All active workflow jobs now use GitHub-hosted `ubuntu-latest` runners. Any self-hosted runner topology, admission-hook, disk-reclaim, or runner-queue descriptions below are historical and must not be used as current operational instructions. Concretely, since #839 `gates.yml` carries a `pull_request` trigger on `main`, and `scripts/ci/audit_runner_admission.py` reports `GitHub-hosted runner policy: 20 job(s) audited, 0 violation(s)` at exit 0. The active policy is enforced by `.github/workflows/runner-admission-policy.yml`.


# CI gates and ratchets

**Document:** GATE-CI-001
**Status:** ACTIVE — authored and locally verified; see §1 for what has and has
not been observed running
**Related:** GAP-10 Tier 2 item 2 (T2.2), GAP-08, GAP-09, DOC-OPS-001, AI-RUN-002-RUNBOOK

This document states which gates CI runs, which of them are hard gates and which
are ratchets, and what a ratchet baseline means. The workflow is
`.github/workflows/gates.yml`; the ratchet tool is `scripts/ci/gate_ratchet.py`.

## 1. Where these jobs run, and what that costs

**Current state (2026-11-23, #839).** `gates.yml` triggers on `pull_request` to
`main`, on `push` to `main`, and on `workflow_dispatch`, and every one of its
five jobs is `runs-on: ubuntu-latest`. It is a pre-merge gate. The paragraphs
below describe the self-hosted topology it replaced, and they are kept because
they are why the workflow is written the way it is, not because they describe
anything that is running now.

The rest of this section is a historical record. In that topology, every job in
`gates.yml` was pinned to `runs-on: [self-hosted, linux, x64]`, and that was not
a preference. `GET /repos/oahcom/AiMemoryBrainArchitecture/actions/runners`
returned `total_count: 1`: a single runner, `zesu-x64`, labels
`self-hosted, Linux, X64`. GitHub-hosted minutes were blocked by a billing failure
on this account, so a job written `runs-on: ubuntu-latest` was allocated no runner
at all and failed with an **empty `steps` array** — it never reached the first
step. Observed on `main`, 2026-11-22T04:29:56Z, on `GOV-DOC-002 metadata checks`
and `audit`: both `failure`, both with zero steps executed. Twelve of the
thirteen workflows in this repository were in that state. A gate authored on
`ubuntu-latest` here was dead on arrival, so those jobs targeted the one runner
that existed.

### 1.1 What that cost: a post-merge detector, not a pre-merge gate

> **Historical.** This subsection records why `gates.yml` used to be
> `push`-only. The billing block was lifted on 2026-11-22 and the self-hosted
> runner was retired by #839 on 2026-11-23; the workflow now carries a
> `pull_request` trigger (§7.7). Nothing below is current behaviour.

Two controls, both in force at the time, forced the trigger set:

* **L1 (service layer).** The runner's job-started hook (`AI-RUN-002-RUNBOOK`
  §4.1) fails any job whose `GITHUB_REF` is not exactly `refs/heads/main`, or
  whose event is not `push` / `workflow_dispatch` / `schedule`. A job on a
  feature branch is denied before any step runs.
* **L2 (repository layer).** `scripts/ci/audit_runner_admission.py`, enforced by
  `runner-admission-policy.yml`, rejected a non-allowlisted trigger on any
  self-hosted job, a `push` with no `branches:` filter, and `push.branches`
  naming anything but `main`.

  L2 was a **denylist** of known-bad triggers until this change. L1 is an
  **allowlist**. So any trigger on neither list — `issues`, `release`,
  `merge_group`, `discussion`, or whatever GitHub adds next — passed L2 and was
  then silently denied by L1. A green L2 that L1 contradicts is worse than no L2:
  it is an audit reporting safety it does not have. L2 then mirrored L1's allowlist
  (`push`, `workflow_dispatch`, `schedule`), so the two agreed by construction
  rather than by two hand-maintained lists. Verified at the time: a self-hosted job
  on `issues`, `merge_group`, `release` and `discussion` was rejected with
  `trigger '<x>' is not permitted for self-hosted jobs (L1 admits only push,
  schedule, workflow_dispatch)`, while the repository's real workflows audited
  clean at 7 jobs / 0 violations.

  **#839 replaced that script.** With no self-hosted runner left, trigger
  allowlisting has nothing to protect, so `audit_runner_admission.py` now checks
  exactly one thing: every job in every workflow is `runs-on: ubuntu-latest`
  (literal, not dynamic, not a label list containing `self-hosted`). It prints
  `GitHub-hosted runner policy: 20 job(s) audited, 0 violation(s)` and exits 0 on
  current `main`. The `trigger '<x>' is not permitted` message no longer exists.

So `gates.yml` triggered on `push` to `main` and `workflow_dispatch`, and on
nothing else. **It could not gate a pull request.** It converted "a gate is red on
`main` and nobody knows" into "a gate is red on `main` and a check run says so
within minutes". That is the GAP-10 defect and it is what this workflow fixes. It
was not a pre-merge gate, and this document did not claim it was one.

Pre-merge gating then needed one of three things, each an Owner decision rather
than an edit to this workflow:

1. GitHub-hosted minutes restored (billing cleared), or
2. a second runner, so the first is not the only place work can land, or
3. a relaxed L1/L2 policy accepting the risk of running untrusted PR code on a
   sudo-capable host.

Option 1 happened on 2026-11-22, and #839 acted on it: the self-hosted runner is
retired and `gates.yml` gates pull requests on hosted runners. The three-way
trade-off above is closed, not pending.

### 1.2 One runner meant serialisation

> **Historical.** Hosted runners are not a single queue, so the `concurrency`
> group described here was removed with the runner in #839.

A single `concurrency` group, `existing-gates-self-hosted`, with
`cancel-in-progress: false`, made runs queue rather than overlap. Jobs inside a
run queued on the runner by themselves. Every job also carried `timeout-minutes`,
because a wedged job on a one-runner repository blocked every other workflow in
the repository, not just this one. The `timeout-minutes` bound is kept on hosted
runners; the queue it was compensating for is gone.

### 1.3 Self-hosted is not a clean container

> **Historical.** Hosted jobs start from a fresh ephemeral VM, so the workarounds
> below are no longer load-bearing. They are kept because several of them are now
> belt-and-braces rather than necessary.

The jobs were written against that reality rather than assuming a fresh VM:

* **No `sudo`, no host mutation.** Python dependencies go into a throwaway venv
  under `$RUNNER_TEMP`, which the runner wipes between jobs. Nothing is installed
  into the host interpreter. No `rustup` step: the runner is operator-managed and
  a workflow that changes the toolchain would change it for every other job on
  the machine.
* **Dependency install degrades, never skips.** If the venv build or the pip
  install fails, the job falls back to the system interpreter *only if* it
  already satisfies `jsonschema`, `rfc8785`, `cryptography`; otherwise it fails
  with the missing names. A failed install is a warning plus a real run, never a
  silent pass.
* **Warm state is reused only where it is genuinely warm.** `npm ci` is skipped
  when `canonicalize` already resolves, so a `node_modules` already on disk is not
  thrown away. `target/` is the opposite case: `actions/checkout` runs
  `git clean -ffdx` by default, so a `target/` inside `$GITHUB_WORKSPACE` is
  wiped and rebuilt every run. That is correct on a host with 5.6G free — a
  workspace-local `target/` is self-limiting, while one redirected to `/tmp` or
  `$HOME` would leak permanently, because checkout cleans the workspace and not
  the home directory. An earlier draft of this document claimed `target/` was the
  runner's build cache and was never cleaned. That was wrong, and the correction
  is recorded here rather than quietly edited away.
* **`--offline` is deliberately not used.** A cold runner has an empty registry
  cache, and `--offline` would turn a missing crate into a confusing failure. The
  tradeoff is that the `clippy` job needs the crates.io egress the runner already
  has for its other Rust work.

## 2. Jobs

| Job | Gate | Command | Kind |
|---|---|---|---|
| `protocol-index` | BMCP message index vs schema `message_type` constraints | `python3 08-bmcp-protocol/scripts/check_protocol_index.py` | hard gate |
| `conformance` | BMCP conformance suite | `python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance` | hard gate |
| `schema-nonempty` | schema non-empty constraint audit | `python3 08-bmcp-protocol/schemas/test_nonempty_audit.py` | hard gate |
| `bilingual` | GOV-DOC-001 full bilingual coverage scan | `python3 scripts/check_bilingual_docs_full.py` | ratchet |
| `clippy` | Rust lints | `cargo clippy --workspace --all-targets -- -D warnings` | hard gate |

### 2.1 Why `conformance` is a hard gate

The suite needs two dependency sets, and both are installed before it runs:

* `08-bmcp-protocol/tests/conformance/provider_outcome/requirements.txt`
  (`jsonschema`, `rfc8785`, `cryptography`).
* `npm ci` in `08-bmcp-protocol/tests/conformance` (`canonicalize@5.1.0`).

With both installed the suite is fully green on `main`: **585 tests, 27 skipped,
0 failures, 0 errors**. Without the Node install, three cross-language vector
tests error with `ERR_MODULE_NOT_FOUND`. That is a missing dependency, not a red
gate, which is why the install step is part of the job rather than a note.

Because the suite is green, it is a hard gate. Had it been red, it would have
been a ratchet.

### 2.2 Why `schema-nonempty` is a hard gate now, and was a ratchet before

An earlier revision of `gates.yml` wrapped this audit in `gate_ratchet.py` with a
5506-line baseline, because GAP-09 was open: 5506 constraints existed in the
schemas that the bilingual audit inventory did not register.

GAP-09 was closed on `main` by `6897e53c` ("audit the 30 unregistered schemas,
closing GAP-09 gate"), which expanded
`08-bmcp-protocol/schema-nonempty-audit.md` from 135 lines to 5582 and registered
all 5599 constraints across the 32 schemas. The audit now exits 0 on `main`.

A green gate must be a hard gate. Keeping the ratchet would have made the
baseline file a standing exemption: the job would report green while the actual
requirement — no unregistered constraint, ever — went unenforced. So the wrapper,
the baseline file and the `(ratchet)` in the job name were all removed together,
and the job runs the audit directly.

This is the rule, not a special case: **a gate moves from ratchet to hard gate the
day it goes green, in the same change that makes it green.** A ratchet that
outlives its red is an exemption with a schedule attached.

### 2.3 Why `clippy` does not run fmt or tests

`rust-phase1.yml` on `main` already runs
`cargo test --workspace --all-targets --no-fail-fast` and
`python3 scripts/check_fmt.py --expect "$GITHUB_SHA"`. At the time this section
was written that workflow was `rust-self-hosted.yml`; #839 deleted that file and
left the same two commands in `rust-phase1.yml`. Duplicating either here would
be worse than doing nothing:

* **The test counts disagree, and the wrong one looks green.**
  `cargo test --workspace` does not run doctests; `--all-targets` does. Measured
  on the same tree: `--all-targets` → `passed=546 failed=0 ignored=1`, plain
  `--workspace` → `passed=551 failed=0 ignored=1`. The 5-test gap is doctests.
  GAP-10 §7.1 records this exact trap at 371 vs 385. Two workflows reporting
  different totals for the same commit make neither number trustworthy, and the
  version that silently runs less is the one that reports success.
* **Two workflows compiling one workspace on one runner doubles the disk churn**
  on a host whose free space has been shrinking between runs that build nothing
  (§5). Paying that twice to obtain a number that contradicts the other job's
  number is a strictly bad trade.

`cargo clippy --workspace --all-targets -- -D warnings` was kept because it was
genuinely uncovered: `rust-phase1.yml` had clippy, but it is `runs-on:
ubuntu-latest`, which on this account was allocated no runner at all, so it had
never executed. Clippy was the independent value of this job.

**That premise expired on 2026-11-22.** Hosted minutes were restored, and
`rust-phase1.yml` now executes clippy on every `pull_request` that touches
`crates/**` — first observed at run `45037267638`, `2026-11-22T15:15:13Z`, head
`38c3c975`, on runner `GitHub Actions 1000005167`. It also runs on the same
commits as this job: `d238dd4a` and `0dc8f5a2` both show clippy `success` in
this workflow and in `rust-phase1.yml`.

The job is therefore **deliberate redundancy, not unique coverage**. The two are
not interchangeable, and the difference is measured: on `6b97a659` this job's
clippy step was `skipped` after `actions/checkout` failed, while
`rust-phase1.yml`'s clippy on the same commit was `success`. Deleting this job
would leave the clippy verdict resting on one workflow whose availability
depends on billing status, which failed as recently as 2026-11-22. Whether to
pay for two is a trade-off decision, not a comment edit.
`GOV-NC-2026-11-23-EXECUTION-RESTORED-029` records the measurements.

The consequence is stated in the workflow itself: rustfmt and the test suite are
**not** gated by `gates.yml`. They are gated by `rust-phase1.yml`. If that
workflow were ever deleted, the `clippy` job must grow them back — with
`--all-targets`.

## 3. What a ratchet is, and what it is not

`bilingual` is red on `main` today. GAP-08 records how it got there: nothing ran
it, so nothing noticed.

Turning it into a hard gate immediately would paint every pull request red for
reasons no author caused. That does not produce compliance; it produces a check
everybody learns to ignore, which is the failure mode that let the gate reach
`main` red in the first place.

A ratchet instead pins the *exact set* of currently-failing items and fails when
that set changes in either direction:

1. **A failure appears that is not in the baseline** — a regression. Fails.
2. **A baseline item no longer fails** — the baseline is stale. Also fails.

The second rule is the one that keeps a ratchet honest. Without it the baseline
silently absorbs fixed items and becomes a permanent blanket exemption. With it,
fixing an item forces the author to lower the baseline in the same pull request.

**A ratchet is not a green exemption.** The gate is not "allowed to be red"; it
is "required to be no worse, and required to stay honest about it".

There is exactly one ratchet left. That is not a stable state to aim for: every
ratchet is a debt with a name attached, and the goal is for the count to reach
zero. `schema-nonempty` already made that trip (§2.2).

## 4. Baselines

Baselines are files under `scripts/ci/baselines/`, one failing item per line,
`#` starting a comment.

| File | Items | Meaning |
|---|---|---|
| `scripts/ci/baselines/bilingual-docs.txt` | 81 | normative paths with no `en` / `zh-CN` counterpart |

Regenerate a baseline only when the failure set legitimately changed:

```bash
python3 scripts/check_bilingual_docs_full.py \
  | grep -E '^[0-9]{3}\. ' | sed -E 's/^[0-9]{3}\. //' | sed -E 's/ -> .*$//' \
  | sort -u > scripts/ci/baselines/bilingual-docs.txt
```

Run a ratchet locally exactly as CI does:

```bash
python3 scripts/ci/gate_ratchet.py \
  --baseline scripts/ci/baselines/bilingual-docs.txt \
  --format paths \
  --command "python3 scripts/check_bilingual_docs_full.py"
```

Exit `0` means the failure set matches the baseline exactly. Exit `1` means a
regression or a stale baseline; the offending items are printed as
`::error::` annotations.

## 5. Known sharp edges

* **No `rust-toolchain.toml` and no `rustfmt.toml`.** The `clippy` job uses
  whatever `cargo` / `cargo-clippy` the runner has installed and reports the
  versions it found. Lints are a moving target: a clippy release that adds a lint
  can turn the job red without any code change. This is recorded rather than
  hidden. Formatting is not gated here (see §2.3); it is gated by
  `rust-phase1.yml`'s `scripts/check_fmt.py`, which pins the commit SHA it
  expects to be formatted. Pinning the toolchain in-repo would remove the sharp
  edge for both and is the obvious next step.
* **`cargo clippy` needs a C toolchain** for `libsqlite3-sys`. It builds on the
  runner; a local Windows host without `cc1` cannot run it. The failure mode is a
  `cc1` error, not a code defect, and the job reports it verbatim rather than
  masking it.
* **Disk is a real constraint, and its floor is measured, not guessed.** Measured
  at `run 44992270090`: 39G total, 32G used, **5.6G free**, 3.6G RAM, 4 CPUs. The
  runner operator measured a comparable host: `cargo test --workspace
  --all-targets` produces a **1009 MB** `target/` over 45 crates, and
  `~/.cargo/registry` is **319 MB** for 290 crates. Clippy-only is the same
  compilation with a different driver and no test binaries linked, so roughly
  **1.0–1.3 GB** including the registry.

  The `clippy` job therefore has a **disk preflight** that refuses below
  `GATES_MIN_FREE_GB` (default **3**) and warns below 6. The floor was 4 when the
  job also ran `cargo test` and shared one `CARGO_TARGET_DIR` with clippy (an
  estimated 1.7–2.0 GB); it dropped with the test step, because a floor that no
  longer matches the job is a number that lies. Lowering a floor to make a run go
  green is forbidden; lowering it because the job genuinely got smaller is just
  bookkeeping.

  **Watch the trend, not the value.** Two diagnostic runs that compile nothing
  reported ~6.8G and then ~5.6G free: about 1.2 GB accumulated with no build in
  between. On a single runner that drift, not the absolute number, is what
  eventually takes every workflow down at once.

* **Build profile and parallelism are pinned down for the same host.** Job-level
  `CARGO_PROFILE_DEV_DEBUG=0` / `CARGO_PROFILE_TEST_DEBUG=0` drop debuginfo,
  which is the bulk of that 1009 MB and also cuts link-time memory.
  `CARGO_BUILD_JOBS=2` because the host has 4 CPUs but 3.6G RAM: the default
  `-j 4` over 45 crates plus a C compile is a plausible OOM, and an OOM mid-build
  is a worse failure than a slower build.

* **`Cargo.lock` is not tracked in this repository** (absent from
  `git ls-files`, and not in `.gitignore` either — a pre-existing defect). Every
  run therefore re-resolves dependencies: the registry index is refetched and any
  version drift re-downloads, ~290 crates. Committing `Cargo.lock` would cut that
  and make the dependency set reproducible. That is a separate one-line change and
  is **not** made here, because it is outside the CI-wiring scope.
* **`check_bilingual_docs_full.py` reads the working tree**, not `git ls-files`.
  Untracked build output can change its answer locally. CI checks out clean, so
  the CI answer is reproducible; a local answer may not be.
* **The ratchet baseline is only as honest as the reviewer.** A regression fails,
  and a stale baseline also fails, but nothing stops someone from regenerating
  the baseline from a worse tree. The mitigation is that regenerating it is a
  visible diff in a file whose entire purpose is to be read.

## 6. Evidence

Recorded on `6de4e38c` (the commit this work started from):

| Gate | Result at `6de4e38c` |
|---|---|
| `check_protocol_index.py` | exit 0 — `missing=0 extra=0 duplicate_types=0 invalid_rows=0`, `PASS` |
| conformance with both dependency sets | exit 0 — `Ran 585 tests`, `OK (skipped=27)` |
| `test_nonempty_audit.py` | exit 1 — 5506 unregistered constraints (GAP-09, since closed) |
| `check_bilingual_docs_full.py` | exit 1 — 81 uncovered paths (GAP-08) |
| `cargo fmt --all --check` | exit 0 |
| `cargo clippy --workspace --all-targets -- -D warnings` | exit 0 |
| `cargo test --workspace` | exit 0 |
| `gate_ratchet.py` on both baselines | exit 0 — `regressions=0 fixed=0` |

That table is history: it is what the gates looked like when the wiring started,
and it is why `schema-nonempty` was originally a ratchet. It is not what the
workflow looks like now.

### 6.1 Re-measured on the rebased tree

`main` moved while this branch was open (`6897e53c` closed GAP-09; `#627` added
`rust-self-hosted.yml`, deleted later by #839; `7d816980` added fmt+clippy to
`rust-phase1.yml`). Both blockers in §2.2 and §2.3 come from that move.
Re-measured after rebasing:

| Command | Result |
|---|---|
| `python3 08-bmcp-protocol/schemas/test_nonempty_audit.py` | exit 0 — `OK: 32 schemas; 5599 registered constraints; no unregistered or stale entries.` |
| `gate_ratchet.py --baseline .../bilingual-docs.txt` | exit 0 — `baseline=81 current=81 regressions=0 fixed=0`, `PASS` |
| `audit_runner_admission.py` (at rebase time) | exit 0 — `7 self-hosted job(s) audited, 0 violation(s)` |
| `cargo test --workspace --all-targets` (on `main`) | `passed=546 failed=0 ignored=1` |
| `cargo test --workspace` (on `main`) | `passed=551 failed=0 ignored=1` |

The last two rows are the whole argument for §2.3: same commit, same workspace,
five different tests, and only one of the two commands is the one `main` runs. The
audit row is the output at rebase time (2026-11-22); on current `main` the same
script prints `GitHub-hosted runner policy: 20 job(s) audited, 0 violation(s)` and
exits 0.

This is local execution of the commands the workflow runs. It is evidence about
the gates, not about the workflow's execution. §7 records what the workflow
itself has done.

## 7. What was actually observed running

> **Historical record (2026-11-22).** Everything in this section was observed on
> the self-hosted runner **before** #839 retired it on 2026-11-23. The run ids,
> labels and host facts are true records of that topology; none of them describes
> the current GitHub-hosted environment. The current measured output is
> `GitHub-hosted runner policy: 20 job(s) audited, 0 violation(s)`, exit 0 (§1).

### 7.1 The runner accepts work, and the labels match

`workflow_dispatch` of `ubuntu-worker-diagnostics.yml` on `main` produced
**run 44992270090** (`success`):

```
job: diagnostics | completed success
  runner_name: 'zesu-x64'
  labels: ['self-hosted', 'linux', 'x64']
  started: 2026-11-22T06:06:59Z -> completed: 2026-11-22T06:07:25Z
  steps: 4 — Set up job, Set up runner, Read-only host diagnostics, Complete job
```

So `runs-on: [self-hosted, linux, x64]` was the correct selector at the time: a
job written that way was admitted and executed. The environment it reported (the
runner no longer exists; these values are a historical record):

| Fact | Value |
|---|---|
| OS / kernel | Ubuntu 26.04 / Linux 7.0.0-30-generic, x86_64 |
| CPU / RAM | 4 / 3.6Gi |
| Disk on `/` | 39G total, 32G used, **5.6G free** |
| Runner account | `ubuntu`, member of `sudo` |
| L1 hook | installed; `guard.log` present, last line `ALLOW ref=refs/heads/main event=workflow_dispatch` |

### 7.2 L1 really does deny a non-`main` ref (negative test)

The same workflow, dispatched at `ref=feat/t22-ci-gates`, produced **run
44992485707** (`failure`). Its log:

```
##[group]Run '/home/ubuntu/actions-runner/hooks/job-started-guard.sh'
runner admission guard: DENY reason=ref_not_default_branch
```

The guard refused the job before the first user step. That is why `gates.yml`
carried no `pull_request` trigger while the self-hosted runner existed, and it was
measured rather than inferred. It is not current: #839 retired the runner and
`gates.yml` now triggers on `pull_request` to `main` (§1).

### 7.3 L2 really does reject the shape a PR-gating version would need

`scripts/ci/audit_runner_admission.py` against `gates.yml`: **7 self-hosted jobs
audited, 0 violations, exit 0** (5 here plus the then-existing `rust-self-hosted.yml`
and the diagnostics job, both deleted by #839). Against a deliberately wrong probe
workflow it reported exactly the two violations expected, exit 1:

```
::error::.github/workflows/zz-probe.yml:probe: untrusted trigger 'pull_request' is not permitted for self-hosted jobs
::error::.github/workflows/zz-probe.yml:probe: on.push.branches includes non-main branch 'feat/t22-ci-gates'
```

#839 has since replaced that script. With no self-hosted job left, trigger
allowlisting has nothing to protect, so it now checks only that every job in every
workflow is `runs-on: ubuntu-latest`: 20 jobs audited, 0 violations, exit 0 on
current `main`. The probe output above is what the pre-#839 script did, not what
the current one would print.

### 7.4 The step bodies were executed, not just parsed

Every `run:` block was extracted from `gates.yml` and executed with
`bash --noprofile --norc -e -o pipefail` on Linux (Ubuntu 24.04, python 3.12,
cargo 1.95.0, node 22), with `RUNNER_TEMP` set as the runner sets it. Results:

| Job | Step | Result |
|---|---|---|
| `protocol-index` | protocol index | exit 0, `missing=0 extra=0 duplicate_types=0 invalid_rows=0`, `PASS` |
| `conformance` | venv dependency install (the real script) | exit 0, `using venv at /tmp/rt/gates-venv`, venv satisfies `jsonschema`/`rfc8785`/`cryptography` |
| `conformance` | full suite, run through that venv | exit 0, `Ran 585 tests`, `OK (skipped=27)` |
| `schema-nonempty` | hard gate audit | exit 0, `OK: 32 schemas; 5599 registered constraints` |
| `bilingual` | ratchet | exit 0, `baseline=81 current=81 regressions=0 fixed=0` |
| `clippy` | disk preflight | exit 0 on a host with 721G free (see §7.5 for the refusal path) |
| `clippy` | toolchain presence | exit 0, `cargo 1.95.0`, `rustc 1.95.0`, `clippy 0.1.95` |
| `clippy` | `cargo clippy --workspace --all-targets -- -D warnings` | exit 0 |

Two of these are worth calling out because they are the ones that could have been
fake. The venv script was executed as written and produced a working interpreter
with all three pinned imports — on a host whose system python is PEP-668
externally managed, i.e. exactly the situation where "just `pip install`" fails.
And the conformance suite was run *through that venv*, not through whatever
happened to be installed, so the 585-test result is the result the job would get.

The `clippy` rows are from the earlier, larger job (fmt + clippy + test). The fmt
and test steps were removed afterwards (§2.3), so only the disk preflight,
toolchain probe and clippy rows still describe a step that exists. The measured
result of the clippy step is unchanged — it is the same command against the same
tree.

### 7.5 The disk preflight refuses, on purpose, at a measured threshold

The preflight was exercised against simulated filesystems at both floors it has
carried. The floor is 3G now; the warn threshold is 6G:

| Free space | Floor 3, warn 6 (current) |
|---|---|
| 2G | exit 1 — `::error::only 2G free (2597152 KiB), below the 3G floor.` |
| 3G | exit 0 — `::warning::only 3G free; shrinking between runs that build nothing.` |
| 5.6G (the runner's measured value) | exit 0 — warns, because `df` KiB is truncated to whole GiB and 5.6 reports as 5 |
| 6G | exit 0 — silent |
| 9G | exit 0 — silent |

An earlier version of this table showed 5.6G being refused, because the floor was
then 6G. That floor was wrong: the measured cost was 2.0–2.5 GB, so 5.6G was
enough and refusing it would have been a red gate with a false reason. The floor
dropped to 4G then, and to 3G when the test step was removed and the job got
smaller. Both corrections are recorded rather than quietly applied.

The `5.6G` row warning is a truncation artefact, not a real signal: `df -Pk`
reports KiB, the script divides to whole GiB, and 5.6 floors to 5, which is under
the 6G warn line. It exits 0 either way. Leaving the truncation in rather than
rounding up is deliberate — a floor comparison that rounds in the permissive
direction is how a floor stops being a floor.

### 7.6 What was NOT observed at the time of writing

> **Historical (2026-11-22).** This subsection records a state that no longer
> holds: `gates.yml` now lives on `main` (merged in #839) and triggers on
> `pull_request`, so the residue described here is closed. The two probe lines
> below are kept as a record of how dispatch resolution was measured; one of the
> two workflows they name, `ubuntu-worker-diagnostics.yml`, was deleted by #839
> and cannot be dispatched at all now.

At the time of writing, `gates.yml` itself had **no check run on any branch**, and
it could not be triggered on demand from a feature branch: GitHub resolves
`POST /actions/workflows/gates.yml/dispatches` against the **default branch**, and
`gates.yml` did not exist on `main`. Measured then:

```
gates.yml@feat/t22-ci-gates -> HTTP 404 (Not Found)
ubuntu-worker-diagnostics.yml@feat/t22-ci-gates -> HTTP 204 (accepted)
```

The second line was the control: dispatch works for a workflow that *was* on
`main`. The first run of these five jobs therefore depended on the file reaching
`main` — which #839 did by merging it. The evidence in §7.4 remains execution of
the exact step bodies rather than a quoted green check run, and this document does
not present it as one.
