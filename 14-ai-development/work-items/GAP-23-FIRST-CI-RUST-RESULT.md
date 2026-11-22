---
document_metadata:
  domain: ai-development
  role: review-report

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-22"
      last_verification_note: "Every number is read from a named GitHub Actions run: 45013113393 job steps and its passed=670 summary line, 45013278749 job 137180047506 for the clippy failure and its cargo=MISSING lines. Not from a local run and not from a commit message."
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

# GAP-23 — The first CI Rust result this repository has ever had: 670/0/0

**Status:** Closed (measurement complete) · **Area:** CI, `rust-self-hosted.yml`, `gates.yml`
**Measured at:** run `45013113393`, head `97c60bc1`, 2026-11-22T10:34:36Z
**Author:** owner delegate under standing instruction (Issue #564, comment 7074302216)

---

## 1. What happened

`#659` merged at `8a4be6d287` and, on the next push to `main` that touched `crates/**`, the self-hosted workflow ran to completion:

```
run 45013113393  rust-workspace-test  success  runner zesu-x64
  1 Set up job                            success
  2 Set up runner                         success
  3 Run actions/checkout@v4               success
  4 Toolchain                             success   <-- rustup installed Rust on the runner
  5 cargo test --workspace --all-targets  success
  6 cargo fmt --all --check               success
 12 Post Run actions/checkout@v4          success
 13 Complete job                          success
```

A second run at `550bb864` (`45011672799`) also succeeded. This is the first time in this repository's history that a `cargo test` result reached a check run.

## 2. The number

From the workflow's own summary line (`45013113393`, step 5):

```
passed=670 failed=0 ignored=0
```

`ignored=0` is not a rounding. The workflow counts it from `grep '^test result:'` across every test binary, and every binary reports `0 ignored`. That includes `phase2_acceptance.rs`, which `001248d452` cleaned out — the last `#[ignore]` in the repository is gone, not merely suppressed.

## 3. Three earlier claims, and which one this replaces

| source | claimed | at | what happened |
|---|---|---|---|
| `#659` body | `629 passed / 0 failed / 0 ignored` | `3c3f4a2` | measured before `#662` added 12 tests |
| `#662` body | `653 passed / 0 failed / 0 ignored` | `2093e07a` | measured locally, before its own merge |
| **this run** | **`670 / 0 / 0`** | **`97c60bc1`** | CI, after both |

The three numbers are consistent: `629` → `653` (+24 from `#662`'s twelve tests plus the domain-side tests that shipped with them) → `670` (+17 from the commits between). Nobody was wrong; the tree grew.

What is new is that this number came from CI rather than from a developer's machine. Until today every test count in this repository was a local claim. `GAP-10 §7.1` records one of them being wrong — `438/0/9` vs `385/0/10` — because a `--lib` run and an `--all-targets` run were compared as if they measured the same thing. The workflow now pins `--all-targets` for exactly that reason, and its comment says so.

## 4. The conflict this exposes, which is more important than the number

`gates.yml`, added in `9f30610f14` at 10:36:31Z — **two minutes after** the successful Rust run — contains this step:

```yaml
      - name: Require the host Rust toolchain
        run: |
          for c in cargo rustc cargo-clippy cc; do
            ...
          done
          echo "::error::zesu-x64 lacks:$missing -- install on the host out of band (see AI-RUN-002-RUNBOOK), do not install it in this workflow"
```

And its `Rust clippy (hard gate)` job failed on exactly that step (`run 45013278749`, job `137180047506`):

```
cargo=MISSING
rustc=MISSING
cargo-clippy=MISSING
##[error]zesu-x64 lacks: cargo rustc cargo-clippy -- install on the host out of band (see AI-RUN-002-RUNBOOK), do not install it in this workflow
##[error]Process completed with exit code 1
```

So on the same runner, at the same time:

- `rust-self-hosted.yml` installed Rust inside the workflow and **succeeded**.
- `gates.yml` refuses to install Rust inside the workflow, and **failed** because Rust is absent.

One of these policies is wrong, and the evidence says it is the newer one. The successful run is not a theory about whether rustup works on `zesu-x64`; it is the outcome. The clippy job's error message instructs the reader to install Rust "on the host out of band" — but the host has had no Rust for the entire life of this workflow, which is the reason `rust-phase1.yml` never produced a result, and there is no evidence anyone can reach the host.

**This is the finding.** A gate that requires a host prerequisite nobody can satisfy is not a gate; it is a job that fails on every push for a reason unrelated to the code it is supposed to check.

## 5. What `gates.yml` got right, stated before the criticism lands

Four of its five jobs succeeded on the same runner in the same run:

| job | result |
|---|---|
| BMCP conformance suite (hard gate) | success |
| BMCP protocol index (hard gate) | success |
| Schema non-empty audit (hard gate) | success |
| Bilingual docs coverage (ratchet) | success |
| Rust clippy (hard gate) | **failure** — toolchain absent |

Moving the gates off `ubuntu-latest` and onto `[self-hosted, linux, x64]` works. That is the thing `#659` and `GAP-19` were both reaching for and neither delivered: `#659` fixed the Rust workflow, and `gates.yml` fixed the Python gates, and they landed two minutes apart without either knowing about the other.

The only job that fails is the one whose precondition the other workflow proves can be met.

## 6. The fix, which is one block

`gates.yml`'s clippy job needs the same block `rust-self-hosted.yml` already has, with one addition for clippy:

```yaml
      - name: Toolchain
        shell: bash
        run: |
          set -euo pipefail
          if ! command -v cargo >/dev/null 2>&1; then
            curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
              | sh -s -- -y --profile minimal --default-toolchain stable --component clippy
          fi
          . "$HOME/.cargo/env"
          cargo --version
          rustc --version
          cargo clippy --version
```

Three details that are load-bearing, each learned from a failure:

1. **`--component clippy`.** `--profile minimal` does not include clippy. Installing stable without it makes step 5 pass and step 6 fail with `cargo-clippy: command not found`, which reads as "the fix did not work."
2. **`. "$HOME/.cargo/env"` in the clippy step too.** rustup writes to a shell profile that a fresh non-login shell does not source. `rust-self-hosted.yml` repeats this line in all three cargo steps for this reason, and the PR body of `#659` names it as the failure mode it was most likely to be reverted for.
3. **`if ! command -v cargo`.** An image that later ships Rust must not reinstall on every push. This also makes the fix compatible with the host eventually being provisioned properly: if someone does install Rust on `zesu-x64`, the workflow stops downloading it and the "out of band" advice becomes true rather than aspirational.

The `Require the host Rust toolchain` step should be kept, not deleted — but changed from a hard failure into a report of which path was taken:

```yaml
      - name: Report the toolchain source
        shell: bash
        run: |
          set -euo pipefail
          . "$HOME/.cargo/env" 2>/dev/null || true
          for c in cargo rustc cargo-clippy cc; do
            printf '%s=%s\n' "$c" "$(command -v "$c" || echo MISSING)"
          done
```

A log line saying `cargo=/home/runner/.cargo/bin/cargo` instead of `cargo=MISSING` is the evidence that the fix took effect. Keeping the check as a *report* rather than a *gate* is what makes the next failure mean something.

## 7. What this does not fix

- **Hosted-minute billing.** Every `ubuntu-latest` workflow is still dead. `gates.yml` routes around it for five gates; the other nine workflows do not.
- **PR checks.** `rust-self-hosted.yml` and `gates.yml` both trigger on `push: branches: [main]` only. `gates.yml`'s own header explains why: the runner's job-started hook denies any `GITHUB_REF` that is not `refs/heads/main`, and `audit_runner_admission.py` rejects `pull_request` on self-hosted jobs. So these runs are post-merge evidence, not pre-merge gates. `unstable` remains the ceiling for every PR.
- **The DM-01 backlog.** `check_document_management.py --strict` still reports `566`, all `DM-01`, at `1a7e3cddae`. The gate can now run in CI; it has not been wired into `gates.yml` yet, and when it is, the baseline will need a ratchet rather than a hard gate.

## 8. What I said I would do, and whether I did it

In the `#659` ruling I committed to reading the run and reporting three things:

1. **Whether `Toolchain` installs Rust on `zesu-x64` at all.** It does. Step 4 succeeded and step 5 then found `cargo`.
2. **`passed / failed / ignored` from the summary line.** `670 / 0 / 0`.
3. **Whether `cargo fmt --all --check` agrees with the tree.** It does — step 6 succeeded, and `check_fmt.py --expect "$(git rev-parse HEAD)"` pins the SHA it measured, so the pass names the exact tree.

I also said I would not revert on a disagreement with `629/0/0`, because a first real measurement that differs from a local one is information. It did not disagree; it grew, and the growth is accounted for in §3.
