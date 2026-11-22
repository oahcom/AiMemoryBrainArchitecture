---
document_metadata:
  domain: governance
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-22"
      last_verification_note: "Every run id, job id, step list and log line quoted here was fetched from the Actions API at main @ 456d4d55aa. The 100-run conclusion tally is a direct count, not a sample."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

# GAP-19 — CI has two independent failures, and only one of them is billing

**Status:** Open — two fixes, both mechanical, neither requires a code change
**Area:** CI / governance
**Measured at:** `main @ 456d4d55aa`, `2026-11-22T08:49Z`
**Closes into:** #650, #480, #352 (they describe the same two causes with one name)

---

## 1. The claim, and why it is half wrong

#650 says: *"All CI jobs fail in 1-3s with zero steps executed — no PR can go green."*

Both halves are false as stated, and the truth is worse than the claim, because it looks like two problems and is actually one problem with a misleading second symptom.

Measured over the last **100** workflow runs on `main`:

```
conclusions: {'failure': 99, None: 1}
successes:   0
```

Zero. Not "some flaky" — zero successes in the last hundred. That part of the claim is right.

But "zero steps executed" is false. One workflow executes steps and fails on its own merits.

## 2. The two causes, separated by the `steps` array

The discriminator is `jobs[].steps` in the Actions API. A job that was never scheduled has an **empty** array. A job that ran has entries.

### Cause A — hosted runners are billing-blocked

Run `45003544720`, job `137150051414`, `GOV-DOC-002 metadata checks`, `runs-on: ubuntu-latest`:

```
conclusion: failure
runner_name: (empty)
steps: 0
```

Its single check-run annotation, quoted:

> `The job was not started because recent account payments have failed or your spending limit needs to be increased. Please check the 'Billing & plans' section in your settings`

`steps: 0` plus an empty `runner_name` means no machine was ever assigned. The 4-second duration is queue rejection, not a test. **Every** gate workflow in this repository is pinned to `ubuntu-latest`:

| workflow | `runs-on` | can ever run? |
|---|---|---|
| `document-management.yml` | `ubuntu-latest` | no |
| `bilingual-docs.yml` | `ubuntu-latest` | no |
| `runner-admission-policy.yml` | `ubuntu-latest` | no |
| `rust-phase1.yml` | `ubuntu-latest` | no |
| `h-applied-delivery-evidence-conformance.yml` | `ubuntu-latest` | no |
| `g-applied-reference-model.yml` | `ubuntu-latest` | no |
| `aid-2026-001-*.yml` | `ubuntu-latest` | no |
| `publication-protocol-reference-model.yml` | `ubuntu-latest` | no |
| `rust-self-hosted.yml` | `[self-hosted, linux, x64]` | **yes — see Cause B** |

This is not fixable in the repository. It requires the account owner to resolve billing. #480 and #352 say so correctly and have said so for some time.

### Cause B — the self-hosted runner has no Rust toolchain

Run `45001611071`, job `rust-workspace-test`, `runs-on: [self-hosted, linux, x64]`:

```
conclusion: failure
runner_name: zesu-x64
steps: 8
   1 Set up job                        -> success
   2 Set up runner                     -> success
   3 Run actions/checkout@v4           -> success
   4 Toolchain                         -> failure
   5 cargo test --workspace --all-targets -> skipped
   6 cargo fmt --all --check           -> skipped
  12 Post Run actions/checkout@v4      -> success
  13 Complete job                     -> success
```

The log, in full, for the failing step:

```
/home/ubuntu/actions-runner/_work/_temp/....sh: line 2: cargo: command not found
##[error]Process completed with exit code 127
```

`rust-self-hosted.yml` exists precisely because Cause A blocks everything else. Its own header comment says so:

> `rust-phase1.yml` therefore has never executed a single test in this repository's history … Self-hosted minutes are not billed, so this is the only path by which a Rust test result can reach a check run.

That reasoning is correct. The workflow then fails at `cargo --version`, because the runner is registered and online but has no Rust toolchain installed. The runner itself is healthy — `zesu-x64`, `status: online`, `busy: false`, labels `['self-hosted', 'Linux', 'X64']` — and checkout succeeded, so the network and the workspace are fine.

**This one is fixable, and it is the only path to a green check run on this account today.**

## 3. Why this matters more than the count

The gate has been reporting verdicts nobody has read for the length of the billing outage. That is how 9 governed files reached `main` with no `document_metadata` (GAP-17), and how two PRs merged while asserting opposite things about the same field (GAP-EXEC-024).

A repository where every check is red has no signal. A repository where every check is red *and nobody notices the redness is uniform* has worse than no signal: it has the appearance of enforcement.

## 4. Fix B, exactly

Two options. Either is sufficient; the first is smaller.

**Option 1 — install the toolchain in the workflow.** Add one step before `Toolchain`, and make `Toolchain` a real check rather than the thing that discovers the absence:

```yaml
      - name: Install Rust toolchain
        shell: bash
        run: |
          set -euo pipefail
          if ! command -v cargo >/dev/null 2>&1; then
            curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
              | sh -s -- -y --profile minimal --default-toolchain stable
          fi
          . "$HOME/.cargo/env"
          cargo --version
          rustc --version
```

Two details that are not incidental:

- `if ! command -v cargo` makes the step idempotent, so a future runner image that already has Rust does not reinstall it on every push.
- `. "$HOME/.cargo/env"` must be in **every** step that uses cargo, because `rustup` writes to a shell profile that a fresh non-login shell does not source. `cargo test` and `cargo fmt --all --check` need the same line. Without it, step 5 fails with the same `command not found` after step 4 succeeds, and the fix looks like it did not work.

**Option 2 — install Rust on the host.** `apt install cargo rustc` or a system-wide rustup. This makes every workflow work without per-step sourcing, but it is host state that no file in the repository records, so the next runner re-registration loses it silently. Option 1 is preferred for that reason alone.

Also worth adding, independent of either option: a step that fails loudly if `cargo` is missing, *before* the expensive checkout-to-test path. The current workflow spends a checkout discovering an environment fact that `command -v cargo` answers in a millisecond.

## 5. What fix B does and does not buy

It buys:

- The first real `cargo test --workspace --all-targets` result this repository has ever had.
- A `cargo fmt --all --check` result, which no workflow has ever produced (the header comment says so, and it is correct — `rust-phase1.yml` and this file both only ran tests).
- A green check run on `main`, which is the precondition for noticing when a red one means something.

It does not buy:

- PR gating. `rust-self-hosted.yml` is `push: branches: [main]` only, and that restriction is binding, not stylistic — the runner's job-started hook denies any job whose `GITHUB_REF` is not exactly `refs/heads/main` (§4.1 L1), and `scripts/ci/audit_runner_admission.py` rejects `pull_request` on self-hosted jobs (§4.1 L2). Do not "fix" that by adding `pull_request`. It will be denied before any step runs, which is what happened on run `44988094101`.
- Documentation-gate coverage. `document-management.yml` and `bilingual-docs.yml` are hosted-only and stay blocked until billing clears. A `main`-push run of the doc gate on self-hosted would be possible, but it is a separate decision: it would run after merge, not before, and a post-merge gate is an audit, not a gate. Worth doing, but do not describe it as restoring enforcement.

## 6. Order of operations

1. **Fix B** (this document's §4). Smallest change, unblocks a real test result, no billing dependency.
2. **Fix A** (account owner, billing). Not a repository change; nothing here can substitute for it.
3. **Then** decide whether the doc gates move to self-hosted on `main` push. That decision needs a number nobody has yet: how long `check_document_management.py --strict` takes on the full tree. Measured elsewhere as ~560 errors over ~600 governed documents; if it is minutes, a post-merge audit is cheap and worth having.

## 7. What this document does not claim

- It does not claim the 99 failures are all billing. It claims **the ones with `steps: 0`** are, and that the ones with non-empty `steps` are not. The sample above is one of each; a full triage of 100 runs would be better evidence and has not been done.
- It does not claim fixing B makes CI green. It makes **one** workflow green, on `main` push, for Rust tests and formatting. Everything else stays blocked.
- It does not claim the self-hosted runner is trustworthy for arbitrary code. It runs on `main` only, by hook and by audit script, and this document does not propose changing that.
