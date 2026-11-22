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
        scheme: git
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-22"
      last_verification_note: "Every measured value in §3 is copied from the log archive of run 44986186138 or from a GitHub Actions API response; every unmeasured value is listed as unverified in §4."
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
    en: "docs/en/14-ai-development/work-items/RUNNER-CAPABILITY-MATRIX-001.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/RUNNER-CAPABILITY-MATRIX-001.md"
---

# RUNNER-CAPABILITY-MATRIX-001 — Self-hosted runner capability and the disposition of 12 `ubuntu-latest` workflows

- **Record type:** Diagnostic work record. No workflow file, no `crates/` source and no gate script is modified by this record.
- **Status:** `Draft` — diagnosis complete, migration not executed.
- **Evidence cut-off:** `main @ 6de4e38c`, 2026-11-22T06:28Z.
- **Runner under test:** `zesu-x64`, labels `[self-hosted, Linux, X64]`, `total_count: 1`.
- **Primary evidence:** run `44986186138` (`Ubuntu Worker - Read-only Diagnostics`, `workflow_dispatch`, conclusion `success`), plus a 882-run Actions API sample covering 2026-11-16 → 2026-11-21.

## 1. Summary

1. **The runner is real, online and enforcing.** Run `44986186138` executed 4 steps and returned host facts (§3). `hooks/guard.log` exists with 9 decision lines; the last one is `ALLOW ref=refs/heads/main event=workflow_dispatch source=env`. `hooks/observe.flag` is **absent**, so L1 admission control is blocking, not log-only.
2. **The decisive constraint is not the label, it is the admission hook.** L1 allows only `GITHUB_REF == refs/heads/main` **and** event ∈ {`push`, `workflow_dispatch`, `schedule`}. Eight of the twelve failing workflows are `pull_request`-triggered. A `pull_request` event carries `refs/pull/N/merge`, so **relabelling those eight cannot make them run** — they will fail with zero steps, exactly like the 2026-11-21 `GOV-DOC-002 metadata checks` failures.
3. **A naive relabel is rejected by the repository's own gate.** Flipping all twelve to `runs-on: [self-hosted, linux, x64]` in a scratch copy makes `scripts/ci/audit_runner_admission.py` exit 1 with **12 violations** (§5.2). The L2 policy already forbids this migration as designed.
4. **`total_count: 1` makes this a serial resource, and the current arrival rate exceeds its capacity.** A successful self-hosted job costs ≈30 s of wall time for ≈3 s of work (measured: 04:41:53 → 04:42:26, steps ran 04:42:05 → 04:42:08). At the observed peak hour (2026-11-17T22: 100 runs, 38 PR synchronisations, 1370 s of measured work) migrating all twelve would need ≈73 min of runner time per 60 min of wall clock — **1.2× over capacity, with unbounded queue growth**. Collapsing each PR synchronisation to one job brings it to ≈32 min/h (53 % utilisation). §8 quantifies this.
5. **Recommendation:** do not migrate all twelve. Merge first, migrate the dependency-free `push`-on-`main` half second, and leave the `pull_request` gates and `runner-admission-policy` where they are until the Owner decides whether the L1 hook may accept same-repository `pull_request` events (§9).

## 2. Method

| Step | What was done | Why it is trustworthy |
|---|---|---|
| Runner inventory | `GET /repos/{o}/actions/runners` | API, not inference |
| Capability probe | Downloaded the log archive of run `44986186138` (`GET .../actions/runs/{id}/logs`, 302 → zip) and read `diagnostics/3_Read-only host diagnostics.txt` | The values are the step's own stdout |
| Failure signature | `GET .../actions/runs/{id}/jobs` for six failing runs on 2026-11-21/22 | Shows `conclusion: failure`, `steps: []`, `runner_name: ""`, `labels: ["ubuntu-latest"]` |
| Guard policy | `14-ai-development/ubuntu-self-hosted-runner-bootstrap.en.md` §4.1 + the `guard.log` line in the probe output | Policy text and runtime decision agree |
| L2 policy behaviour | Copied the 13 workflow files + `audit_runner_admission.py` into `/tmp/sim2`, applied `sed 's/runs-on: ubuntu-latest/runs-on: [self-hosted, linux, x64]/'`, ran the audit | Executed, exit code and 12 `::error::` lines captured |
| Cost model | 882-run Actions API sample; durations = `run_started_at → updated_at` for `conclusion: success`; plus the step timestamps of `44986186138` | Measured, not estimated; the two sources are labelled separately in §8 |

Nothing in this record was inferred from documentation alone where a measurement was available. Where only documentation existed, §4 says so.

## 3. Runner capability matrix

Source of every value in the "measured" rows: log archive of run `44986186138`, step 3, timestamp `2026-11-22T04:42:05Z`.

| Capability | Measured value | Evidence | Verified? |
|---|---|---|---|
| Runner software version | `2.338.2` | `0_diagnostics.txt`, line 1: `Current runner version: '2.338.2'` | Yes |
| Kernel | `Linux 7.0.0-30-generic` | `uname -sr` | Yes |
| Architecture | `x86_64` | `uname -m` | Yes |
| OS / version | `ubuntu` / `26.04` | `/etc/os-release` `ID` + `VERSION_ID` | Yes |
| CPU count | `4` | `nproc` | Yes |
| Memory total | `3.6Gi` | `free -h` | Yes |
| Memory available | `1.4Gi` (used 2.3Gi, buff/cache 1.1Gi) | `free -h` | Yes |
| Swap | `2.0Gi` total, `1.6Gi` used, `389Mi` free | `free -h` | Yes |
| Root filesystem | `/dev/vda3`, `39G` total, `31G` used, **`6.8G` available**, 82 % | `df -h /` | Yes |
| NTP synchronised | `yes` | `timedatectl show -p NTPSynchronized --value` | Yes |
| `tailscaled` | `enabled`, `active` | `systemctl is-enabled` / `is-active` | Yes |
| Host egress service unit | `inactive` (unit name withheld by the workflow) | `systemctl is-active [HOST EGRESS SERVICE]` | Yes (state) / No (identity, by design) |
| L1 admission hook installed | **Yes** — `guard.log` present, `9` lines | `wc -l < hooks/guard.log` | Yes |
| L1 hook is enforcing | **Yes** — `observe.flag` absent, no `WARNING:` line emitted | the step prints `WARNING: observe.flag present — admission control is log-only` only when the flag exists; it did not | Yes |
| Last guard decision | `2026-11-22T04:42:05Z ALLOW ref=refs/heads/main event=workflow_dispatch source=env` | `tail -n 1 hooks/guard.log` | Yes |
| Runner account | `uid=1000(ubuntu) gid=1000(ubuntu)`, groups `1000(ubuntu),4(adm),24(cdrom),**27(sudo)**,30(dip),101(lxd)` | `id` | Yes |
| Bash available | Yes | every step ran `shell: bash`, `-euo pipefail` | Yes |
| `uname` / `free` / `df` / `nproc` / `timedatectl` / `systemctl` / `wc` / `tail` available | Yes | all produced output in step 3 | Yes |
| Job scheduling latency | 8 s queue wait (`created 04:41:53` → `started 04:42:01`) | run `44986186138` job timestamps | Yes (single sample) |
| Fixed cost per job | ≈30 s wall for ≈3 s of work (`started 04:42:01` → `completed 04:42:26`; steps `04:42:05` → `04:42:08`) | run `44986186138` job timestamps | Yes (single sample) |
| Working directory reuse across jobs | Serial (`total_count: 1`), so one workspace is reused; `actions/checkout` cleans the checkout path but not `$HOME` or `/tmp` | `total_count: 1` + `actions/checkout` documented behaviour | Partly — the reuse is certain, the exact cleanup surface is not |
| Rust toolchain (`cargo`, `rustc`) | **not measured** | — | **No** |
| Python 3 present / version | **not measured** (the probe used `bash` only) | — | **No** |
| `rfc8785`, `jsonschema`, `cryptography` installed | **not measured** | — | **No** |
| `cargo` registry cache seeded | **not measured** | — | **No** |
| Node / `npm` present | **not measured** | — | **No** |
| `gh` CLI present | **not measured** | — | **No** |
| Outbound HTTPS egress (PyPI, npm, static.rust-lang.org) | **not measured** — the probe made no network call | — | **No** |
| `sudo` usable without password | **not measured** — the account is in `sudo`, but no `sudo -n true` was run | group membership only | **No** |

### 3.1 What the matrix already rules out

- **`ubuntu 26.04` is not a GitHub-hosted image.** Any workflow that relies on the hosted image's preinstalled toolchain set is relying on something that does not exist here.
- **`6.8G` free on `/` is the binding disk constraint.** A cold `cargo test --workspace --all-targets` of this workspace produced a **1009 MB** target directory (measured locally, §8.4). Six such builds left in the default location fill the remaining space.
- **`1.4Gi` available RAM with `4` cores** is the binding memory constraint for Rust. `cargo test` defaults to one rustc process per core plus one test binary per crate; on a 5 GiB / 16-core reference box the cold build peaked without trouble, but at 1.4 GiB available this is a real OOM risk and must be capped (`CARGO_BUILD_JOBS`), not assumed away.
- **`27(sudo)` group membership plus a job-started hook that only checks ref and event** is exactly the threat model the bootstrap document already names: "A workflow that *is* admitted can `sudo`." That is why the `pull_request` ban is load-bearing and cannot be relaxed for convenience.

## 4. What could not be verified

This list is deliberately longer than the temptation to guess.

| # | Unverified item | Why it matters | How to settle it |
|---|---|---|---|
| U-01 | Rust toolchain presence and version | `rust-phase1.yml` is the single most valuable workflow to migrate (45 s median, 11 successes) and the most expensive to get wrong | Add one `command -v cargo rustc` line to the existing diagnostics workflow; it is a 1-line change to an already-admitted `workflow_dispatch` job |
| U-02 | Python 3 version on the runner | Nine of the twelve workflows are `python3` scripts; `aid-2026-001-*` pin `3.13`, `bilingual-docs` and `document-management` use bare `python3` | Same 1-line probe (`python3 -V`) |
| U-03 | Whether `rfc8785`, `jsonschema`, `cryptography` are preinstalled | Decides whether `h-applied-delivery-evidence-conformance` needs a pip step at all | `python3 -c "import rfc8785, jsonschema, cryptography"` in the probe |
| U-04 | Whether PyPI / npm / `static.rust-lang.org` are reachable | `h-applied` runs `pip install` + `npm ci`; `rust-phase1` uses `dtolnay/rust-toolchain`, which downloads rustup | `curl -sSI https://pypi.org/simple/ -o /dev/null -w '%{http_code}'` etc. Do **not** infer reachability from `tailscaled` being active |
| U-05 | `cargo` registry cache state | A cold registry means `cargo test` also downloads ~290 crates; this dominates the 45 s figure | `du -sh ~/.cargo/registry` in the probe |
| U-06 | Node / `npm` presence | `npm ci` in `h-applied` | `command -v node npm` in the probe |
| U-07 | `gh` CLI presence | `ai-owner-worker-bootstrap-labels` shells out to `gh api` | `command -v gh` in the probe |
| U-08 | Whether `sudo -n` succeeds for `ubuntu` | Group membership is not the same as a working NOPASSWD rule | `sudo -n true; echo $?` — but this is a privilege probe and should be an Owner-approved, audited action, not a routine diagnostic |
| U-09 | Behaviour of `actions/checkout` cleanup on this specific runner build | Determines whether `target/` and `node_modules/` leak between jobs | Run one Rust job twice and compare `df -h /` before and after |
| U-10 | Whether the L1 hook will be extended to same-repository `pull_request` events | This single decision determines whether 8 of 12 workflows can ever run here | Owner decision, §9 |

## 5. The decisive constraint: the L1 admission hook

### 5.1 Policy and runtime agree

`14-ai-development/ubuntu-self-hosted-runner-bootstrap.en.md` §4.1 states the hook fails the job unless `GITHUB_REF` is exactly `refs/heads/main` **and** `GITHUB_EVENT_NAME` ∈ {`push`, `workflow_dispatch`, `schedule`}, failing closed when the ref cannot be resolved. The probe confirms the hook is installed and enforcing (§3).

The failure signature is distinctive and already recorded in the same document:

| Run | Trigger | Guard verdict | Observed job |
|---|---|---|---|
| `44049832708` | `push` → `refs/heads/main` | `ALLOW` | `success`, 4 steps |
| `44050069421` | `push` → `refs/heads/ci/admission-negative-test` | `DENY ref_not_default_branch` | `failure`, steps 2 `Set up runner` failed, step 3 `This step must never execute` **skipped** |
| `44986186138` | `workflow_dispatch` → `main` | `ALLOW` | `success`, 4 steps |

**This is a different signature from the 2026-11-21 failures.** The current `ubuntu-latest` failures show `steps: []` — zero steps exist at all, because no runner ever picked the job up (`runner_name: ""`, `labels: ["ubuntu-latest"]`). A guard-denied job on this runner shows *four* steps with step 2 failing. Anyone reading a future run must distinguish the two, or they will misdiagnose a guard denial as a missing runner.

### 5.2 The repository's own L2 gate already forbids the naive migration

Scratch simulation (`/tmp/sim2`, all 13 files copied, `runs-on` replaced, real audit script):

```
runner admission: 14 self-hosted job(s) audited, 12 violation(s)
exit=1
```

The 12 violations:

| Count | Violation | Workflows |
|---|---|---|
| 8 | `untrusted trigger 'pull_request' is not permitted for self-hosted jobs` | `aid-2026-001-manifest-validation`, `aid-2026-001-reference-model`, `bilingual-docs`, `document-management`, `g-applied-reference-model`, `h-applied-delivery-evidence-conformance`, `publication-protocol-reference-model`, `runner-admission-policy`, `rust-phase1` (9 files, 8 distinct rules fired because `h-applied` also fires a branch rule) |
| 3 | `on.push.branches includes non-main branch` | `abr-forget-cross-owner-model` (`review/architecture-breakthrough-integration-2026-11-18`), `h-applied-delivery-evidence-conformance` (`session-h-bmcp-protocol`), `publication-protocol-reference-model` (`fix/publication-fence-admission-order`) |

**Consequence:** migrating any `pull_request` workflow to this runner is a two-part change — label *and* trigger — and the trigger half changes what the gate protects. That is an Owner decision, not a `runs-on` edit.

### 5.3 A gap in the L2 audit worth reporting

`UNTRUSTED_TRIGGERS` in `scripts/ci/audit_runner_admission.py` is `{pull_request, pull_request_target, issue_comment, workflow_run, workflow_call}`. It does **not** include `issues`. Simulating `ai-owner-worker.yml` alone (which triggers on `issues: [labeled]` and `workflow_dispatch`) yields:

```
runner admission: 2 self-hosted job(s) audited, 0 violation(s)
exit=0
```

So L2 would pass a self-hosted job triggered by `issues`, while L1 would deny it at runtime (event is not in the allowlist) — a silent, zero-step failure with no audit signal. **This record does not change the audit**; it flags that `issues` (and any future event outside L1's allowlist) should be added to `UNTRUSTED_TRIGGERS` so L2 and L1 agree. Until then, treat "L2 passes" as necessary but not sufficient.

## 6. Per-workflow assessment

Legend for **Migration risk**: `sudo` = needs system packages; `net` = downloads dependencies; `cache` = writes large state into a reused workspace; `hosted` = relies on the hosted image's preinstalled tools; `boundary` = security boundary that L1/L2 must hold.

| # | Workflow | Trigger | What it runs | Migration risk | Verdict |
|---|---|---|---|---|---|
| 1 | `abr-forget-cross-owner-model.yml` | `push` → `review/architecture-breakthrough-integration-2026-11-18` (+ path filter) | 3 stdlib `python3` model scripts in `reviews/architecture-breakthrough/integration/model` | **boundary** (non-main ref → guard `DENY`), plus dead scope: branch is 148 commits ahead, last commit 2026-11-18, unmerged | **Delete** |
| 2 | `ai-owner-worker-bootstrap-labels.yml` | `workflow_dispatch` | `gh api` label create/verify, `python3 -c urllib.parse` | `hosted` (`gh` presence unverified, U-07), `net` (writes to the API), needs `issues: write` | **Delete after one confirmation** — idempotent one-shot migration artifact |
| 3 | `ai-owner-worker.yml` | `issues: [labeled]`, `workflow_dispatch` | 2 jobs: `codex` (35 min timeout, agent run, artifact upload) then `publish` (`contents: write`, `pull-requests: write`, pushes a branch and opens a PR) | **boundary** (an admitted job can `sudo`; this job pushes branches), `hosted` (codex CLI), `cache` (agent workspace), 35 min of a serial runner | **Do not migrate** |
| 4 | `aid-2026-001-manifest-validation.yml` | `pull_request`, `push`→`main` | `pip install PyYAML==6.0.2`, strict duplicate-key YAML parse of `AID-2026-001/manifest.yaml` | **boundary** (PR half), `net` (PyPI, wheel for 3.13 unverified, U-04) | **Rework, then migrate the `push` half** |
| 5 | `aid-2026-001-reference-model.yml` | `pull_request`, `push`→`main` | `python3 -m unittest discover` over 196 K of stdlib tests | **boundary** (PR half) — no `net`, no `cache` | **Migrate the `push` half** — cheapest possible first migration |
| 6 | `bilingual-docs.yml` | `pull_request` only (5 activity types) | `python3 scripts/check_bilingual_docs.py`, `fetch-depth: 0` | **boundary** (PR-only → guard always `DENY`), `net` (full clone) | **Merge** into a single governance job; keep off this runner |
| 7 | `document-management.yml` | `pull_request`, `push`→`main` | `scripts/test_check_document_management.py` then `scripts/check_document_management.py --require-changed`, `fetch-depth: 0` | **boundary** (PR half); 3.2 s of local CPU work, no `net`, no `cache` | **Merge**; migrate the `push` half |
| 8 | `g-applied-reference-model.yml` | `pull_request`, `push`→`main` | `python3 -m unittest discover` over 40 K of stdlib tests | **boundary** (PR half) only | **Merge with #5 and #10** |
| 9 | `h-applied-delivery-evidence-conformance.yml` | `push`→`session-h-bmcp-protocol`, `workflow_dispatch`, `pull_request`→`main` | `pip install jsonschema rfc8785 cryptography`, `npm ci`, then 5 `unittest discover` suites | **boundary** (PR half + non-main push), **highest `net` surface** (3 native/wheel deps + npm registry), `cache` (`node_modules`), `hosted` (`rfc8785` may be preinstalled on hosted, unverified here, U-03) | **Rework, then migrate `workflow_dispatch` + `push`→`main` last** |
| 10 | `publication-protocol-reference-model.yml` | `push`→`fix/publication-fence-admission-order`, `pull_request`→`main` | stdlib `unittest` on one test file | **boundary** (both halves: non-main ref and PR), dead scope (branch 202 commits ahead, last commit 2026-11-18) | **Delete the `push` half; merge the PR half into #5/#8** |
| 11 | `runner-admission-policy.yml` | `pull_request`, `push`→`main` | `python3 scripts/ci/audit_runner_admission.py` — the L2 auditor | **boundary, and a conflict of interest**: running the auditor on the audited host lets a workflow change disable its own admission check in the same trust domain | **Do not migrate** — this one is correct where it is |
| 12 | `rust-phase1.yml` | `pull_request`, `push`→`main` | `dtolnay/rust-toolchain@stable` then `cargo test --workspace --all-targets` (11 crates) | **boundary** (PR half), `net` (rustup + ~290 crates), `cache` (**1009 MB** target dir), memory (**1.4 GiB** available vs 4-way parallel rustc), disk (**6.8 GB** free) | **Rework, then migrate the `push` half** — highest payoff, highest cost of getting wrong |

### 6.1 The two things this table makes obvious

- **The `pull_request` half of eight workflows is not a labelling problem.** It is a policy problem. Any plan that says "change `runs-on`" without saying what happens to `pull_request` is not a plan.
- **Four workflows are dead weight independent of the runner.** `abr-forget-cross-owner-model` and the `push` half of `publication-protocol-reference-model` and `h-applied-delivery-evidence-conformance` are scoped to branches that were last touched on 2026-11-18/20 and are 148/202/597 commits divergent from `main`. They have never produced a single run on `main` (`abr`: 0 runs in the 882-run sample). They should be deleted regardless of which runner they would have used.

## 7. Disposition

### 7.1 Delete (4 changes, zero risk, do first)

| Item | Reason |
|---|---|
| `abr-forget-cross-owner-model.yml` (whole file) | Non-main `push` trigger → L1 always `DENY`; branch stale since 2026-11-18; 0 runs in sample |
| `publication-protocol-reference-model.yml` — the `push:` block only | Same; branch stale since 2026-11-18; the PR half is worth keeping |
| `h-applied-delivery-evidence-conformance.yml` — the `push: session-h-bmcp-protocol` block only | Same; branch stale since 2026-11-20 |
| `ai-owner-worker-bootstrap-labels.yml` | One-shot, idempotent; the labels it creates either exist or the pilot is not running |

Net effect: 3 non-main triggers and 1 one-shot removed; no gate loses coverage on `main`.

### 7.2 Merge (do second — this is where the queue time is won)

| Merge | Members | Result |
|---|---|---|
| M-1 `governance-gates` | `bilingual-docs` (PR) + `document-management` (PR + main) + `runner-admission-policy` (PR + main) | One workflow, three jobs (or one job running three scripts). All three are `python3` + `fetch-depth: 0`; none needs a toolchain |
| M-2 `reference-models` | `aid-2026-001-reference-model` + `g-applied-reference-model` + the PR half of `publication-protocol-reference-model` | One job, three `unittest discover` invocations. Zero third-party imports (verified by AST scan: only in-directory modules) |

M-1 alone removes 2 job slots from every `push` to `main` and every PR synchronisation. M-2 removes 2 more from PRs. Neither needs the runner at all — they are pure `ubuntu-latest` restructuring, so they can land before any runner decision.

### 7.3 Rework, then migrate (in this order)

| Order | Workflow (half to migrate) | Work required before the label changes | Why this order |
|---|---|---|---|
| **P1** | `aid-2026-001-reference-model` (`push`→`main`), `g-applied-reference-model` (`push`→`main`) — as M-2 | None beyond the merge. Stdlib only, 236 K of tests | Proves `python3` on the runner with zero dependency risk. If it fails, nothing else was built on the assumption |
| **P2** | `document-management` (`push`→`main`) — as M-1 | None. Stdlib only, 3.2 s local | First real gate on the runner. Establishes the real per-job cost against the 30 s model in §8 |
| **P3** | `aid-2026-001-manifest-validation` (`push`→`main`) | Pre-seed `PyYAML==6.0.2` (a runner-side venv or `pip install --user` behind an allowlisted egress), or replace it with the stdlib duplicate-key check the script already implements around it | First `net` precedent. If egress is blocked, this is where it is discovered — cheaply |
| **P4** | `rust-phase1` (`push`→`main`) | Pin the toolchain instead of `@stable`; set `CARGO_TARGET_DIR` outside the checkout path; cap `CARGO_BUILD_JOBS=2`; add a pre-flight `df -h /` guard | Highest payoff (45 s median, 11 successes) and highest cost of failure (1 GB target, 1.4 GiB RAM, 6.8 GB disk). Only after P1–P3 prove the runner |
| **P5** | `h-applied-delivery-evidence-conformance` (`workflow_dispatch` + `push`→`main`) | Pre-seed `jsonschema`/`rfc8785`/`cryptography`; decide whether `npm ci` is needed on the runner or only the Python half runs there | Last: the widest dependency surface, and the only workflow needing both PyPI and npm |

**Never migrate:** `runner-admission-policy` (the auditor must not share a trust domain with the audited host) and `ai-owner-worker` (an admitted job can `sudo`; this one holds `contents: write` and pushes branches).

### 7.4 If the Owner relaxes L1 instead

If the Owner decides L1 may accept `pull_request` when `GITHUB_HEAD_REPO_FULL_NAME == GITHUB_REPOSITORY` (same-repository PR, no fork), then the eight PR-triggered gates become migratable — but `audit_runner_admission.py` must be updated in the same commit, or L2 will reject the change it is supposed to permit. That is a single coordinated change to the hook, the audit, and the eight workflow files; it is not a per-workflow edit, and it must not be done piecemeal.

## 8. Serial-queue quantification

### 8.1 The cost model

Two measured inputs, kept separate because they come from different machines:

- **Fixed cost per self-hosted job ≈ 30 s.** Run `44986186138`: job `started 04:42:01` → `completed 04:42:26` = 25 s inside the job, of which the only real step ran `04:42:05 → 04:42:08` = 3 s; plus 8 s queue wait before it started. Total `created → completed` = 33 s for 3 s of work.
- **Work time per workflow** — hosted-runner medians from the 882-run sample (`conclusion: success` only). These are cold hosted runs, so they are a *floor*, not an estimate, for a 4-core runner.

| Workflow | Median (hosted) | n |
|---|---|---|
| `Bilingual documentation gate` | 10 s | 165 |
| `Rust Phase 1 Workspace Tests` | 45 s | 11 |
| `AID-2026-001 Manifest Validation` | 12 s | 3 |
| `AID-2026-001 Reference Model Tests` | 11 s | 1 |
| `G Applied Persistence Reference Model` | 10 s | 2 |
| `Publication Protocol Reference Model` | 10 s | 4 |
| `Architecture document management gate` | **no success in sample** (89 failures, 3–4 s, all runnerless) | 0 |
| `Runner admission policy` | **no success in sample** (90 failures) | 0 |
| `H Applied Delivery Evidence Conformance` | **no success in sample** (6 failures) | 0 |

For the three without a hosted success, local CPU time on the 16-core reference box (labelled: **not** the runner):

| Script | Local wall |
|---|---|
| `scripts/check_document_management.py` | 1 239 ms |
| `scripts/test_check_document_management.py` | 1 913 ms |
| `scripts/ci/audit_runner_admission.py` | 79 ms |
| `scripts/check_bilingual_docs.py` | 52 ms |

### 8.2 The arrival rate

From the 882-run sample (2026-11-16 → 2026-11-21, 5 active days):

- **239** distinct `(branch, head_sha)` `pull_request` groups = 239 PR synchronisations, carrying **566** job runs.
- Jobs per synchronisation: 1 → 89 groups, 2 → 40, 3 → 59, 4 → 39, 5 → 8, **6 → 4**.
- Serial work per synchronisation (measured durations, hosted): median **11 s**, p90 **42 s**, max **83 s**, mean 17.4 s.
- **Peak hour `2026-11-17T22:00`: 100 runs, 38 PR synchronisations, 1370 s of measured work.**

### 8.3 Three scenarios, same hour

Capacity of one runner in one hour = `3600 / (30 s overhead + work)`.

| Scenario | Jobs in the peak hour | Serial demand | Capacity | Verdict |
|---|---|---|---|---|
| **All 12 migrated as-is** | 100 | 100 × 30 s + 1370 s = **4 370 s = 73 min** | 3 600 s | **1.2× over. Queue grows without bound.** Capacity 82 jobs/h vs arrival 100/h |
| **M-1 + M-2 merged, all migrated** | 100 − (2 per sync × 38) ≈ 60 | 60 × 30 s + 1370 s ≈ 3 170 s = **53 min** | 3 600 s | 88 % utilisation — survives this hour, no headroom for the next burst |
| **M-1 + M-2 merged, only `push`→`main` halves migrated** | ≈ 3 per `main` push (see §8.5) | ≈ 1–2 min per push | 3 600 s | Comfortable |

**This is the quantitative basis for "do not migrate all twelve."** The overhead alone — before a single test runs — is `38 syncs × 6 jobs × 30 s = 6 840 s = 114 min` per hour in the unmerged case, which is 1.9× the entire capacity of the runner. The 2026-11-17T22:00 hour is a sample peak, not a worst case; a 6-job PR synchronisation burst of 20 pushes in ten minutes would already queue for half an hour.

### 8.4 Disk and memory, quantified

- Cold `cargo test --workspace --all-targets` on `main @ 6de4e38c`: **1009 MB** target directory, 45 crates compiled, 22–32 s on a 16-core / 5 GiB box with a warm `~/.cargo/registry` (319 MB, 290 cached crates).
- The runner has **6.8 GB** free on `/`. Six uncleaned target directories fill it. `actions/checkout` cleans the checkout path, not `$HOME` or `/tmp`; `total_count: 1` means the same host serves the next job.
- The runner has **1.4 GiB** available RAM and **4** cores. The reference box has 16 cores and 5 GiB. A build that is 22–32 s there is not 22–32 s here, and 4-way parallel `rustc` at 1.4 GiB available is an OOM candidate, not a slowdown.
- `Cargo.lock` **is not tracked** (`git ls-files Cargo.lock` → no match; no `.gitignore` entry either). Every run resolves dependency versions afresh, so a cold registry means ~290 crate downloads on every job, and two runs a week apart are not guaranteed to compile the same graph. This is a pre-existing defect that the migration would make more expensive, not a migration risk in itself.

### 8.5 What one `push` to `main` costs today vs after M-1

Today, a `push` to `main` with no path filters triggered fires three workflows: `Runner admission policy`, `Architecture document management gate`, `Rust Phase 1 Workspace Tests` (measured: 25 `main` pushes in the sample, 1–3 jobs each, median 8 s serial on hosted because they ran in parallel).

After M-1 on the self-hosted runner, serialised: `(30 + 0.1) + (30 + 3.2) + (30 + 45..120)` ≈ **140–210 s ≈ 2.5–3.5 min per push**. That is acceptable. It is also why P4 (`rust-phase1`) must come after P1–P3: it is the term that dominates that sum.

## 9. Decisions this record cannot make

| # | Decision | Who | Why it cannot be an engineering default |
|---|---|---|---|
| D-1 | May L1 accept same-repository `pull_request`? | Owner | Relaxing it removes the only control that stops an untrusted trigger from reaching a `sudo`-capable host. `observe.flag` exists as the emergency rollback and was never exercised in production |
| D-2 | Should `runner-admission-policy` ever run on the audited host? | Owner / governance | Self-audit in one trust domain is a structural conflict, not a performance trade-off |
| D-3 | Is `ai-owner-worker` allowed to hold `contents: write` on a host where admitted jobs can `sudo`? | Owner | This is the exact threat the L1 hook was built for; the answer is a risk acceptance, not a label |
| D-4 | Is a second runner funded? | Owner | `total_count: 1` is the root cause of §8. A second runner with `[self-hosted, linux, x64, ai-worker]` would let PR gates and `main` gates run concurrently and would remove the serial constraint entirely |

Until D-1 and D-4 are answered, the correct engineering output is: delete the dead triggers (§7.1), merge the overlapping gates (§7.2), migrate the stdlib `push`-on-`main` halves (§7.3 P1–P2), and stop.

## 10. Reproduction

```bash
# 1. Runner inventory
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/actions/runners"

# 2. Capability probe (log archive of the diagnostics run)
curl -sL -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/actions/runs/44986186138/logs" \
  -o /tmp/logs.zip && unzip -o /tmp/logs.zip -d /tmp/logs
cat "/tmp/logs/diagnostics/3_Read-only host diagnostics.txt"

# 3. Failure signature of a runnerless job (steps == [])
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/actions/runs/44986264084/jobs" \
  | python3 -c 'import json,sys; [print(j["name"],j["conclusion"],len(j["steps"]),j["labels"],repr(j["runner_name"])) for j in json.load(sys.stdin)["jobs"]]'

# 4. Failure signature of a guard-denied job (4 steps, step 2 failed)
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/actions/runs/44050069421/jobs" \
  | python3 -c 'import json,sys; [print([ (s["number"],s["name"],s["conclusion"]) for s in j["steps"]]) for j in json.load(sys.stdin)["jobs"]]'

# 5. The L2 rejection of a naive relabel
rm -rf /tmp/sim2 && mkdir -p /tmp/sim2/.github/workflows /tmp/sim2/scripts/ci
cp .github/workflows/*.yml /tmp/sim2/.github/workflows/
cp scripts/ci/audit_runner_admission.py /tmp/sim2/scripts/ci/
cd /tmp/sim2 && sed -i 's/runs-on: ubuntu-latest/runs-on: [self-hosted, linux, x64]/' .github/workflows/*.yml
python3 scripts/ci/audit_runner_admission.py; echo "exit=$?"   # 12 violations, exit 1
```

## 11. Non-claims

- No workflow file, `crates/` source, gate script or runner configuration was modified by this record.
- No claim is made that the runner can or cannot build Rust, run Node, or reach PyPI (§4 U-01…U-07).
- No claim is made that the twelve workflows are *correct*; only where they can execute.
- `document-management` reports `INCOMPLETE` on `main` today (593 governed documents, 38 classified, 555 unclassified). That is a pre-existing backlog, not a finding of this record, and is recorded here only so a future reader does not attribute it to the migration.
