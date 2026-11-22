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
