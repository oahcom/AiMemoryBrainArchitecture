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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "Every run id, head SHA, runner name and step conclusion in this register was read from the GitHub Actions REST API in this session. No figure is carried over from another register. The register claims no approval and no independent review."
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
    source: "14-ai-development/governance-register/GOV-NC-2026-11-23-EXECUTION-RESTORED-029.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-23-EXECUTION-RESTORED-029.md"
---

# GOV-NC-2026-11-23-EXECUTION-RESTORED-029 — The execution side is restored, and two present-tense claims of 005 with it

- Register ID: GOV-NC-2026-11-23-EXECUTION-RESTORED-029
- Status: `OPEN` / `MEASUREMENT_ONLY` / platform capability restored, the documents that cite the opposite premise are not yet corrected
- Measured at: 2026-11-23T10:40Z
- Measurement base: `main = 20902c48` (main advanced from `68fa85a4` to `20902c48` during collection; every run below is cited with its head SHA, so nothing depends on where `main` currently sits)
- Preceding registers: `GOV-NC-2026-11-20-CI-NOT-EXECUTED-005` (the zero-execution window), `GOV-NC-2026-11-21-GATE-CLOSURE-020` (§5 counter-claim), `GAP-EXEC-2026-11-22-MEASUREMENT-REPRODUCIBILITY-023` (§5 item 1)
- Author: owner-proxy session. **Not** an independent reviewer, **not** the accountable owner.

---

## 1. Conclusion first

Register 005 recorded a historical window: 36 hours in which gate logic executed **0 times**. The facts of that window are unchanged by this register.

But 005's status line is present tense ("the execution side is entirely absent"), and several live documents cite that state as current fact and have made **design decisions that are still in force** on the strength of it. As of 2026-11-22T15:15:13Z that premise no longer holds:

| | first real execution | run | head | runner |
|---|---|---|---|---|
| self-hosted | 2026-11-22T10:17:02Z | `45011672799` | `550bb864` | `zesu-x64` |
| GitHub-hosted | 2026-11-22T15:15:13Z | `45037267638` | `38c3c975` | `GitHub Actions 1000005167` |

Both reached `cargo test --workspace --all-targets` and returned `success`. The GitHub-hosted one also executed `cargo clippy --workspace --all-targets -- -D warnings` and `check_fmt.py`.

So this register is not "005 is wrong". It is "the present-tense part of 005 has expired, and the present-tense judgements that depend on it were not updated with it".

---

## 2. The trade that was paid for, and what it now covers

`ci-gates-and-ratchets.en.md` §2.3 gives the reason why the `clippy` job in `gates.yml` runs clippy only, and neither fmt nor the tests:

> `cargo clippy --workspace --all-targets -- -D warnings` is kept because it is genuinely uncovered: `rust-phase1.yml` has clippy, but it is `runs-on: ubuntu-latest`, which on this account is allocated no runner at all, so **it has never executed**. Clippy is the independent value of this job.

The first half of that sentence was once true, which is why the conclusion — duplicating it would be a losing trade — once held. The premise has now inverted: `rust-phase1.yml`'s clippy does execute, and it executes **on the same commit as `gates.yml`'s clippy**.

Measured (same commit, same command, two successes):

| commit | `gates.yml` clippy | `rust-phase1.yml` clippy |
|---|---|---|
| `d238dd4a` | `success` | `success` |
| `0dc8f5a2` | `success` | `success` |

A counter-example shows why this is not "the two agree, so it does not matter": on `6b97a659` the `gates.yml` clippy job failed at `actions/checkout` with the clippy step `skipped`, while `rust-phase1.yml`'s clippy on the same commit was `success`. The same command reached different availability through two workflows, which means they are not two copies of one thing — they are one that works and one that depends on a more brittle precondition.

**This register does not argue for deleting the clippy job in `gates.yml`.** Deleting it would turn "two legs" into "one leg that depends on billing status", and billing status failed as recently as 11-22. What this register argues is narrower: that comment can no longer serve as the reason. It now describes **deliberate redundancy**, not "the only coverage". Those two states call for different trade-offs, and the trade-off is not a comment edit.

---

## 3. The second claim refuted: the precondition for pre-merge gating

The header comment of `gates.yml` states:

> Pre-merge gating needs one of: GitHub-hosted minutes restored, a second runner, or a relaxed L1/L2 policy — each an Owner decision, not an edit here.

The first of the three is satisfied. And it needs no new workflow: `rust-phase1.yml` already triggers on `pull_request`, path-filtered to `Cargo.toml` / `Cargo.lock` / `crates/**` / `scripts/check_fmt.py` / itself, and runs on GitHub-hosted runners.

Measured: run `45155022673`, `2026-11-23T10:19:21Z`, head `72cc25fe`, event `pull_request`, runner `GitHub Actions 1000005710`, with `check_fmt` / `clippy` / `cargo test --workspace --all-targets` all `success`.

**Conclusion: this repository now has a working pre-merge Rust gate**, covering pull requests that touch `crates/**`. This is not a capability I added; it is an existing workflow that began working once billing was restored. The narrower claim in `gates.yml` — that *that* workflow cannot gate a pull request — remains true, because it is self-hosted and bound by L1/L2. What is refuted is the larger judgement that pre-merge gating is unreachable on this account.

This one has a direct consequence. Both AID-2026-052 and AID-2026-053 say "the workspace suite belongs to CI; a local multi-gigabyte `target/` is not a contribution". While that judgement was false, the sentence was an **IOU that could not be honoured** — CI would not run. It is honoured now, and it is honoured through a pre-merge path that reads `crates/**` changes.

---

## 4. The third claim: what verdict `gates.yml` actually produces on `main`

Conclusion distribution over the most recent 73 push-triggered `gates.yml` runs:

| conclusion | count |
|---|---|
| `failure` | 31 |
| `cancelled` | 23 |
| `success` | 18 |
| `queued` | 1 |

`cancelled` is neither failure nor pass — it is **no verdict**. The cause is `gates.yml`'s concurrency group: one runner means serialisation, and GitHub keeps one running plus one pending run per group, cancelling older pending runs when pushes arrive in a burst.

So roughly 31% (23/73) of pushes to `main` received no conclusion from `gates.yml` at all. This is the **same class of defect as 005 with a different cause**: 005 was "the run exists but the steps did not execute"; this is "the run was cancelled, so no step could exist". The governance meaning is identical — that commit has no automated conclusion — and only one of the two has ever been registered.

---

## 5. What needs correcting (this register does not correct it)

| file | location | claim | status |
|---|---|---|---|
| `14-ai-development/ci-gates-and-ratchets.en.md` | §2.3 | `rust-phase1` "has never executed" | false |
| `14-ai-development/ci-gates-and-ratchets.zh-CN.md` | §2.3 | "因此从未执行过" | false |
| `.github/workflows/gates.yml` | header comment, clippy job comment | `ubuntu-latest` is allocated no runner | false |
| `.github/workflows/rust-self-hosted.yml` | header comment | hosted minutes are blocked by billing failure | false |
| `GOV-NC-2026-11-20-CI-NOT-EXECUTED-005` | status line | "the execution side is entirely absent" | true within the window, false as present tense |
| `GAP-EXEC-2026-11-22-MEASUREMENT-REPRODUCIBILITY-023` | §5 item 1 | "CI has never executed a test" | false |
| `GOV-NC-2026-11-21-GATE-CLOSURE-020` | §5 | "does not claim CI ever executed" | a qualifier scoped to that round; historically true, must not be cited as current |

The first two and the workflow comments are **present-tense** claims, and a reader takes them as current fact; they should be corrected. 005 and 023 are **historical registers with stated measurement points**; their bodies should not be rewritten. They should carry a dated note pointing at this register rather than having "never" edited into "once".

`gates.yml` and `rust-self-hosted.yml` are workflow files. This register does not modify them — a comment correction and the question of whether the job should exist are two different things, and the second needs a trade-off decision about the billing dependency.

---

## 6. What this register does not claim

- **It does not claim 005's counts are wrong.** In those 36 hours gate logic really did execute 0 times, and no count in that window changes here.
- **It does not claim the gates are now trustworthy.** Executed is not passed, and passed is not sufficient coverage. The 23 `cancelled` runs in §4 are precisely the gap between "the execution side works" and "the verdict side is reliable".
- **It does not claim the duplicate clippy should be deleted.** See the end of §2.
- **It does not claim the restoration is permanent.** Billing failed as recently as 11-22; this register records a fact at a point in time and says explicitly that it may invert again. Any authorization that depends on "CI will run" should say so.
- **It does not claim this measurement was independently reviewed.** Every figure comes from read-only GitHub Actions API queries, reproducible by anyone, but a reproducer is not an independent reviewer.

---

## 7. Reproduction

For any run, read `runner_name` and `steps[].conclusion` for every job at `/repos/{repo}/actions/runs/{id}/jobs`:

```text
runner_name == ""            -> no runner allocated (005 layer 3)
steps == []                  -> no step executed (005 layer 4 is 0)
steps[*].conclusion == skip  -> that step did not execute; its job's failure is not a substantive gate failure
run.conclusion == cancelled   -> no verdict (this register §4)
```

Every run id this register cites appears in the tables of §1, §2, §3 and §4, and can be re-read directly.
