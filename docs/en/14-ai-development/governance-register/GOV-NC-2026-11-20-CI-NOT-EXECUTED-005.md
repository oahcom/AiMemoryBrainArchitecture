# GOV-NC-2026-11-20-CI-NOT-EXECUTED-005 — Register of 36 consecutive hours with zero gate executions

- Register ID: GOV-NC-2026-11-20-CI-NOT-EXECUTED-005
- Status: `ACCEPTED` / `CI_NOT_EXECUTED` / execution side entirely absent (Owner ruling, 2026-11-21)
- Observed at: 2026-11-21T04:10Z (last data pull)
- Subject: repository `oahcom/AiMemoryBrainArchitecture`, `main` and every PR on it
- Related: #352 (temporary quota rule), #281 / PR-GOVERNANCE-001-ENFORCEMENT v1.2 (compensating-evidence rule for platform check unavailability), #405 (self-hosted alternative attempt), #403 / #402 (merge instances in this round)

## 1. Why this is registered separately

The three preceding registers record, respectively: direct pushes bypassing PR, merges without review after a ruling, and a wrong AC verdict. All three share a premise that was never written down on its own — **not once did the repository's structural gate actually run while those merges happened**.

"CI is red" and "CI never ran" are different states. The first says the code has a problem. The second says **no automated conclusion exists at all**. This register is only about the second: counting "zero executions" at run granularity, and writing its consequences as a checkable account.

It does not re-derive the cause (#352 does that) and does not re-analyse the alternatives (#405 does that). It answers one question: how many gate verdicts did the platform issue in this interval.

## 2. Decision rule (same P7 rule already in use)

For any run, read `/repos/{repo}/actions/runs/{id}/jobs`:

| Shape | Verdict |
|---|---|
| `steps` is an empty array and `runner_name` is the empty string | `NOT_EXECUTED` |
| A runner was assigned, but the failure is at `Set up runner` and every project step is `skipped` | `NOT_EXECUTED` (gate logic never ran) |
| Project steps executed and returned a `conclusion` | `EXECUTED` |

`conclusion: failure` is not by itself evidence of `EXECUTED`. There is no entailment from `failure` to "the tests failed".

### 2.1 Five layers that must stay separate

The Owner's ruling of 2026-11-21 requires this register to distinguish five things explicitly:

| Layer | What it is | What the facts say for this window |
|---|---|---|
| 1 | the CI platform produced a run | yes, 362 |
| 2 | the run was assigned a `conclusion` | yes: 348 `failure`, 13 `skipped`, 1 `success` |
| 3 | whether a runner started | 345 never started; 3 started and failed at `Set up runner` |
| 4 | **whether the gate logic actually executed** | **0 times** |
| 5 | the gate's result after execution | does not exist (layer 4 is 0) |

Layer 2 contains one `success`, but a `conclusion` alone **cannot establish that the gate logic ran**; and the 3 self-hosted runs in layer 3 must not be read as "self-hosting rescues CI", because every project step was `skipped`.

**This register's conclusion supports one governance fact only — layer 4 is zero.** It must not be used to claim the repository's gate itself passes or fails. Any exact-head local execution (such as #419's compensating evidence) is a manual substitute at layer 5, not CI execution evidence.

## 3. Boundary: the last real execution and the first empty one

| | Run | Time | Conclusion | steps | runner |
|---|---|---|---|---|---|
| Last real execution | `44559466007` (Bilingual documentation gate) | 2026-11-19T15:51:14Z | `success` | 5 | `GitHub Actions 1000002033` |
| First empty execution | `44563397286` (GOV-DOC-001 structural checks) | 2026-11-19T16:12:11Z | `failure` | **0** | `''` |

Verbatim check-run annotation on `44563397286`:

```
The job was not started because recent account payments have failed or your
spending limit needs to be increased. Please check the 'Billing & plans'
section in your settings
```

The same annotation repeats on every empty run from 2026-11-19T16:12 to 2026-11-21T04:10. It is not test feedback.

**Boundary conclusion: after 2026-11-19T16:12:11Z this repository produced no further gate verdict.**

## 4. Full census (per run, not sampled)

Five consecutive pages of `/actions/runs?per_page=100`, covering 2026-11-18T12:56:35Z → 2026-11-21T04:10:03Z, 500 runs total.

Distribution after the boundary:

| Metric | Value |
|---|---|
| Runs at/after boundary | 362 |
| `failure` | 348 |
| `skipped` | 13 (all `issues` events, `AI Owner Worker`) |
| `success` | 1 |
| **Of the `failure` runs, individually re-read** | **348 / 348** |
| → `NOT_EXECUTED` (`steps=[]`, `runner=''`) | **345** |
| → runner assigned, failed at `Set up runner`, all project steps `skipped` | **3** |
| → gate logic actually executed and returned a conclusion | **0** |

The three exceptions deserve their own table, because they were once read as "self-hosted can rescue CI":

| Run | Workflow | Runner | Failing step | Project steps |
|---|---|---|---|---|
| `44862136704` | Rust Phase 1 Workspace Tests | `zesu-x64` | 2 `Set up runner` | all `skipped` |
| `44862136705` | Bilingual documentation gate | `zesu-x64` | 2 `Set up runner` | all `skipped` |
| `44862537055` | Bilingual documentation gate | `zesu-x64` | 2 `Set up runner` | all `skipped` |

All three are refused at step 2; from step 3 onward (checkout, check script) everything is `skipped`. **Not one line of the gate ran.**

The single `success` is not a gate either:

| Run | Workflow | Trigger | Runner | steps |
|---|---|---|---|---|
| `44861020897` | `ubuntu-worker-diagnostics.yml` | `workflow_dispatch` on `main` (actor `oahcom`) | `zesu-x64` (`self-hosted, linux, x64`) | 4 (Set up job / Set up runner / Read-only host diagnostics / Complete job) |

It proves the self-hosted runner is alive and can run a `workflow_dispatch`. It proves no PR's compliance.

## 5. What was merged in this interval

PRs with `merged_at >= 2026-11-19T16:12:11Z`: **85** (#289 … #408, every one authored by `oahcom`).

| Metric | Value |
|---|---|
| Total merged | 85 |
| With an `APPROVED` review | **0** |
| Review events in the whole window | 36, **all `COMMENTED`, all from `oahcom`** (author = merger) |
| With no review of any kind | **64** |
| Merged before the #352 ruling (2026-11-20T09:03:35Z) | 42 |
| Merged after it | 43 |

**Not one review in this window came from a second account.** This is not "the review comments were weak"; in this interval the repository had no second reviewing subject at all.

## 6. This register's own first sample: PR #409 is red under the gate

This is the one time in this round the gate really ran — executed by me locally against the exact Head, not in CI.

| Item | Value |
|---|---|
| PR | #409 (this register ships with it) |
| Gate script blob | `ce072be30a9d9d53c6f4e4add3b9cbc59f192d25` (24404 B; identical blob at BASE and HEAD) |
| BASE | `423fb4b7e62f…` (rebuilt locally as `26b702fd8864…`) |
| HEAD | `ccd19ecd91f0…` (rebuilt locally as `f3df9d670fc8…`) |
| First execution | `::error::Normative source files changed but PR body lacks 'BILINGUAL-MANIFEST: COMPLETE' or a fully documented 'BILINGUAL-EXCEPTION: APPROVED'.` / `EXIT=1` |

In other words: **the first version of PR #409's body makes the gate exit 1.** On a day when CI worked, that defect would have been caught within a minute of opening. During the 36 hours of zero execution it could only be found by a human running the script locally at exact Head — and without this register nobody would have run it.

That yields a reusable conclusion: while the gate executes zero times, **the only detection channel still working is "someone voluntarily runs it locally at exact Head"**. #281 already wrote that channel down as a rule (PR-GOVERNANCE-001-ENFORCEMENT v1.2 §1, "Platform check unavailability") and named run `44563397286` on the same day at 16:57Z — 45 minutes after empty executions began. The rule exists, the channel works, but it is **voluntary**, and its output never enters the `checks` field.

## 7. Boundary between fact and inference

Facts (each recomputable, see §8):
- The two runs in §3: time, steps, runner, verbatim annotation.
- Every count in §4: 362 / 348 / 345 / 3 / 1 / 0.
- Every count in §5: 85 / 0 / 36 / 64 / 42 / 43.
- §6's command, inputs, output, exit code.

Inferences (**not** made here):
- This register does not rule on whether the 85 merges were governance violations. `#352` rule 1 already removed CI results from the merge criteria; under that rule the merges were permitted. Whether rule 2's "locally re-checkable evidence" was satisfied each time is a reviewer's judgement, not this register's.
- It does not rule on the correctness of the merged code. No evidence, no conclusion — that is precisely the state this register documents.
- It does not read `NOT_EXECUTED` as `PASS`, nor as `FAIL`.

## 8. How to recount

```bash
# 1) runs after the boundary
GET /repos/oahcom/AiMemoryBrainArchitecture/actions/runs?per_page=100&page=1..5

# 2) per-run verdict
GET /repos/oahcom/AiMemoryBrainArchitecture/actions/runs/{id}/jobs
#   steps == [] and runner_name == ""  -> NOT_EXECUTED

# 3) verbatim annotation
GET /repos/oahcom/AiMemoryBrainArchitecture/check-runs/{job_id}/annotations

# 4) merges and reviews
GET /repos/oahcom/AiMemoryBrainArchitecture/pulls?state=closed&per_page=100
GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/{n}/reviews

# 5) the §6 local reproduction
BASE_SHA=<base> HEAD_SHA=<head> PR_BODY="$(cat pr_body.txt)" \
  python scripts/check_bilingual_docs.py; echo "EXIT=$?"
```

## 9. Dispositions requested (no decision taken on the Owner's behalf)

| ID | Requirement | Owner of the action |
|---|---|---|
| R-1 | Until recovery, every PR created after 2026-11-19T16:12:11Z must have its `checks` recorded as `NOT_EXECUTED`; never as "tests passed" or "tests failed" | Done by this register |
| R-2 | Choosing the recovery channel (paid hosted / public repo / self-hosted post-merge `push` per runbook §4.1 option 4 / status quo) is the Owner's decision; #405 already wrote the boundary of all four | Owner |
| R-3 | Whether rule 2/5 of #352 was satisfied for each of the 85 merges needs one independent sample review; this register does not replace it | Independent review |
| R-4 | `checks: failure` must not be cited as evidence anywhere in the REQ-06…REQ-12 acceptance chain; any citation must state the run id and the `NOT_EXECUTED` verdict | Acceptance chain |

## 10. Relation to the existing registers

- **GOV-NC-2026-11-20-MERGE-AFTER-RULING-003**: the check on #403 at merge was `failure`; this register establishes that the `failure` was `NOT_EXECUTED`, not a gate rejection. The instance count stays frozen at 4 per the Owner ruling; this register does not change it.
- **GOV-NC-2026-11-20-DIRECT-MAIN-001**: the 62 direct pushes also fall inside the zero-execution window. That register's conclusion (direct push bypasses the PR channel) is unchanged, but its implicit premise that push-triggered workflows still check does not hold.
- **GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004**: the AC-5 correction rests on three local re-measurements and is independent of CI; this register does not affect it.

**Register status**: `ACCEPTED` / `CI_NOT_EXECUTED` / gate logic actually executed in 36 hours: **0** / merges in the same window: **85** / of which `APPROVED`: **0**

Owner ruling (2026-11-21): the statistics, the boundary and the `NOT_EXECUTED` classification are accepted. It also states explicitly that **this register may stand as a governance fact but must not be used to claim the repository's gate itself passes or fails**; #419's local exact-head run is compensating evidence, not CI execution evidence.
