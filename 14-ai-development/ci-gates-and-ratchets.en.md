# CI gates and ratchets

**Document:** GATE-CI-001
**Status:** ACTIVE — authored and locally verified; see §1 for what has and has
not been observed running
**Related:** GAP-10 Tier 2 item 2 (T2.2), GAP-08, GAP-09, DOC-OPS-001, AI-RUN-002-RUNBOOK

This document states which gates CI runs, which of them are hard gates and which
are ratchets, and what a ratchet baseline means. The workflow is
`.github/workflows/gates.yml`; the ratchet tool is `scripts/ci/gate_ratchet.py`.

## 1. Where these jobs run, and what that costs

Every job in `gates.yml` is pinned to `runs-on: [self-hosted, linux, x64]`.

That is not a preference. `GET /repos/oahcom/AiMemoryBrainArchitecture/actions/runners`
returns `total_count: 1`: a single runner, `zesu-x64`, labels
`self-hosted, Linux, X64`. GitHub-hosted minutes are blocked by a billing failure
on this account, so a job written `runs-on: ubuntu-latest` is allocated no runner
at all and fails with an **empty `steps` array** — it never reaches the first
step. Observed on `main`, 2026-11-22T04:29:56Z, on `GOV-DOC-002 metadata checks`
and `audit`: both `failure`, both with zero steps executed. Twelve of the
thirteen workflows in this repository are in that state. A gate authored on
`ubuntu-latest` here is dead on arrival, so these jobs target the one runner that
exists.

### 1.1 What that costs: this is a post-merge detector, not a pre-merge gate

Two controls, both already in force, force the trigger set:

* **L1 (service layer).** The runner's job-started hook (`AI-RUN-002-RUNBOOK`
  §4.1) fails any job whose `GITHUB_REF` is not exactly `refs/heads/main`, or
  whose event is not `push` / `workflow_dispatch` / `schedule`. A job on a
  feature branch is denied before any step runs.
* **L2 (repository layer).** `scripts/ci/audit_runner_admission.py`, enforced by
  `runner-admission-policy.yml`, rejects `pull_request` on any self-hosted job, a
  `push` with no `branches:` filter, and `push.branches` naming anything but
  `main`.

So `gates.yml` triggers on `push` to `main` and `workflow_dispatch`, and on
nothing else. **It cannot gate a pull request.** It converts "a gate is red on
`main` and nobody knows" into "a gate is red on `main` and a check run says so
within minutes". That is the GAP-10 defect and it is what this workflow fixes. It
is not a pre-merge gate, and this document does not claim it is one.

Pre-merge gating needs one of three things, each an Owner decision rather than an
edit to this workflow:

1. GitHub-hosted minutes restored (billing cleared), or
2. a second runner, so the first is not the only place work can land, or
3. a relaxed L1/L2 policy accepting the risk of running untrusted PR code on a
   sudo-capable host.

### 1.2 One runner means serialisation

A single `concurrency` group, `existing-gates-self-hosted`, with
`cancel-in-progress: false`, makes runs queue rather than overlap. Jobs inside a
run queue on the runner by themselves. Every job also carries `timeout-minutes`,
because a wedged job on a one-runner repository blocks every other workflow in
the repository, not just this one.

### 1.3 Self-hosted is not a clean container

The jobs are written against that reality rather than assuming a fresh VM:

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
* **Warm state is reused, not trusted.** `npm ci` is skipped when `canonicalize`
  already resolves, so a warm `node_modules` is not thrown away. `target/` is
  never cleaned — on one runner it is the only build cache there is — but nothing
  depends on it being present.
* **`--offline` is deliberately not used.** A cold runner has an empty registry
  cache, and `--offline` would turn a missing crate into a confusing failure. The
  tradeoff is that the `rust` job needs the crates.io egress the runner already
  has for its other Rust work.

## 2. Jobs

| Job | Gate | Command | Kind |
|---|---|---|---|
| `protocol-index` | BMCP message index vs schema `message_type` constraints | `python3 08-bmcp-protocol/scripts/check_protocol_index.py` | hard gate |
| `conformance` | BMCP conformance suite | `python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance` | hard gate |
| `schema-nonempty` | schema non-empty constraint audit | `python3 08-bmcp-protocol/schemas/test_nonempty_audit.py` | ratchet |
| `bilingual` | GOV-DOC-001 full bilingual coverage scan | `python3 scripts/check_bilingual_docs_full.py` | ratchet |
| `rust` | formatting, lints, tests | `cargo fmt --all --check`, `cargo clippy --workspace --all-targets -- -D warnings`, `cargo test --workspace` | hard gate |

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

## 3. What a ratchet is, and what it is not

`schema-nonempty` and `bilingual` are red on `main` today. GAP-09 and GAP-08
record how they got there: nothing ran them, so nothing noticed.

Turning them into hard gates immediately would paint every pull request red for
reasons no author caused. That does not produce compliance; it produces a check
everybody learns to ignore, which is the failure mode that let the gates reach
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

## 4. Baselines

Baselines are files under `scripts/ci/baselines/`, one failing item per line,
`#` starting a comment.

| File | Items | Meaning |
|---|---|---|
| `scripts/ci/baselines/schema-nonempty.txt` | 5506 | schema constraints absent from the bilingual audit inventory |
| `scripts/ci/baselines/bilingual-docs.txt` | 81 | normative paths with no `en` / `zh-CN` counterpart |

Regenerate a baseline only when the failure set legitimately changed:

```bash
python3 08-bmcp-protocol/schemas/test_nonempty_audit.py \
  | sort -u > scripts/ci/baselines/schema-nonempty.txt

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

* **No `rust-toolchain.toml` and no `rustfmt.toml`.** The `rust` job uses whatever
  `cargo` / `rustfmt` the runner has installed and reports the versions it found,
  so a rustfmt release that changes formatting can turn `cargo fmt --all --check`
  red without any code change. This is recorded rather than hidden: formatting
  drift on `main` is itself a recurring regression in GAP-10, so the job is a
  hard gate. Pinning the toolchain in-repo would remove the sharp edge and is the
  obvious next step.
* **`cargo clippy` and `cargo test` need a C toolchain** for `libsqlite3-sys`.
  They build on the runner; a local Windows host without `cc1` cannot run them.
  The failure mode is a `cc1` error, not a code defect, and the job reports it
  verbatim rather than masking it.
* **Disk is the binding constraint on this runner.** Measured at
  `run 44992270090`: 39G total, 32G used, **5.6G free**, 3.6G RAM, 4 CPUs. A
  workspace build of 11 crates with a C dependency writes a `target/` that does
  not fit. Filling the disk would break every other workflow in the repository,
  because there is one runner. The `rust` job therefore has a **disk preflight**
  that refuses to start below `GATES_MIN_FREE_GB` (default 10) and reports the
  free space. The threshold is a floor, not a target: raise it, never lower it to
  make a run go green. This is why `rust` may be red on this runner for a reason
  that is not a code defect — the job says so explicitly instead of failing
  somewhere inside `cargo`.
* **`check_bilingual_docs_full.py` reads the working tree**, not `git ls-files`.
  Untracked build output can change its answer locally. CI checks out clean, so
  the CI answer is reproducible; a local answer may not be.
* **The ratchet baseline is only as honest as the reviewer.** A regression fails,
  and a stale baseline also fails, but nothing stops someone from regenerating
  the baseline from a worse tree. The mitigation is that regenerating it is a
  visible diff in a file whose entire purpose is to be read.

## 6. Evidence

Recorded on `6de4e38c` (the commit this work is based on):

| Gate | Result |
|---|---|
| `check_protocol_index.py` | exit 0 — `missing=0 extra=0 duplicate_types=0 invalid_rows=0`, `PASS` |
| conformance with both dependency sets | exit 0 — `Ran 585 tests`, `OK (skipped=27)` |
| `test_nonempty_audit.py` | exit 1 — 5506 unregistered constraints (GAP-09) |
| `check_bilingual_docs_full.py` | exit 1 — 81 uncovered paths (GAP-08) |
| `cargo fmt --all --check` | exit 0 |
| `cargo clippy --workspace --all-targets -- -D warnings` | exit 0 |
| `cargo test --workspace` | exit 0 |
| `gate_ratchet.py` on both baselines | exit 0 — `regressions=0 fixed=0` |

This is local execution of the commands the workflow runs, on the same commit the
workflow is based on. It is evidence about the gates, not about the workflow's
execution. §7 records what the workflow itself has done.

## 7. What was actually observed running

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

So `runs-on: [self-hosted, linux, x64]` is the correct selector: a job written
that way is admitted and executes. The environment it reported:

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

The guard refused the job before the first user step. This is why `gates.yml`
cannot carry a `pull_request` trigger, and it is measured rather than inferred.

### 7.3 L2 really does reject the shape a PR-gating version would need

`scripts/ci/audit_runner_admission.py` against `gates.yml`: **6 self-hosted jobs
audited, 0 violations, exit 0** (5 here plus the pre-existing diagnostics job).
Against a deliberately wrong probe workflow it reported exactly the two
violations expected, exit 1:

```
::error::.github/workflows/zz-probe.yml:probe: untrusted trigger 'pull_request' is not permitted for self-hosted jobs
::error::.github/workflows/zz-probe.yml:probe: on.push.branches includes non-main branch 'feat/t22-ci-gates'
```

### 7.4 The step bodies were executed, not just parsed

Every `run:` block was extracted from `gates.yml` and executed with
`bash --noprofile --norc -e -o pipefail` on Linux (Ubuntu 24.04, python 3.12,
cargo 1.95.0, node 22), with `RUNNER_TEMP` set as the runner sets it. Results:

| Job | Step | Result |
|---|---|---|
| `protocol-index` | protocol index | exit 0, `missing=0 extra=0 duplicate_types=0 invalid_rows=0`, `PASS` |
| `conformance` | venv dependency install (the real script) | exit 0, `using venv at /tmp/rt/gates-venv`, venv satisfies `jsonschema`/`rfc8785`/`cryptography` |
| `conformance` | full suite, run through that venv | exit 0, `Ran 585 tests`, `OK (skipped=27)` |
| `schema-nonempty` | ratchet | exit 0, `baseline=5506 current=5506 regressions=0 fixed=0` |
| `bilingual` | ratchet | exit 0, `baseline=81 current=81 regressions=0 fixed=0` |
| `rust` | disk preflight | exit 0 on a host with 721G free (see §7.5 for the refusal path) |
| `rust` | toolchain presence | exit 0, `cargo 1.95.0`, `rustc 1.95.0`, `rustfmt 1.9.0-stable`, `clippy 0.1.95` |
| `rust` | `cargo fmt --all --check` | exit 0 |
| `rust` | `cargo clippy --workspace --all-targets -- -D warnings` | exit 0 |
| `rust` | `cargo test --workspace` | exit 0, `passed=508 failed=0 ignored=1` |

Two of these are worth calling out because they are the ones that could have been
fake. The venv script was executed as written and produced a working interpreter
with all three pinned imports — on a host whose system python is PEP-668
externally managed, i.e. exactly the situation where "just `pip install`" fails.
And the conformance suite was run *through that venv*, not through whatever
happened to be installed, so the 585-test result is the result the job would get.

### 7.5 The disk preflight refuses, on purpose

The preflight was exercised against three simulated filesystems:

| Free space | Outcome |
|---|---|
| 5.6G (the runner's measured value) | `::error::only 5G free, below the 6G floor…`, exit 1 |
| 8G | `::warning::only 8G free…`, exit 0 |
| 20G | silent, exit 0 |

So on this runner **as it stands today the `rust` job will be red**, at the disk
check, before it touches `cargo`. That is the intended behaviour and it is the
honest outcome: 5.6G cannot hold a workspace build of 11 crates including a C
dependency, and filling the one runner's disk would take down every other
workflow in the repository. The remedy is an operator reclaiming space, not an
edit to this file.

### 7.6 What is still NOT observed

`gates.yml` itself has **no check run on any branch yet**, and it cannot be
triggered on demand from a feature branch: GitHub resolves
`POST /actions/workflows/gates.yml/dispatches` against the **default branch**, and
`gates.yml` does not exist on `main`. Measured:

```
gates.yml@feat/t22-ci-gates -> HTTP 404 (Not Found)
ubuntu-worker-diagnostics.yml@feat/t22-ci-gates -> HTTP 204 (accepted)
```

The second line is the control: dispatch works for a workflow that *is* on
`main`. So the first run of these five jobs happens on the first push to `main`
after this branch merges — or immediately if someone with push rights to `main`
cherry-picks the file there. Until then, the evidence in §7.4 is execution of the
exact step bodies, not of the workflow, and this document does not present it as
a green check run.

