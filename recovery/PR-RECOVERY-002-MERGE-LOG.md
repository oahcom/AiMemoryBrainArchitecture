# PR-RECOVERY-002 Merge Log / 合并日志

| Time (UTC) | PR | Candidate head | Merge SHA | Result | Evidence |
|---|---|---|---|---|---|
| — | — | — | — | **No PR merged in initial recovery batch** | No candidate satisfied all applicable merge gates |

## Non-merge actions
- Created branch `recovery/pr-recovery-002-baseline-2026-11-18` from frozen main.
- Committed baseline and inventory artifacts to this recovery branch only.
- Posted recovery triage comments on #23, #27, #94, #95 and rolling-intake #104.
- No PR was force-pushed or rebased. PR #27 was updated on its existing branch by two bounded contents commits; #23/#27 were converted to Draft. No PR was closed.
- No main commit was created by this recovery work.

A merge entry may be added only after verifying the merge commit on main and confirming the PR state is merged.

- Converted #23 and #27 to Draft after confirming no merge gates were satisfied.
- Committed bounded #27 branch remediation: redacted operational endpoint/device/path metadata; corrected runbook security-acceptance language; changed service-account deviation to OWNER_REVIEW_REQUIRED. Commits include `09ad79b60c49b0187c9103ba803c08d0a887cb94` and `805d680a33a96b819f32758f7f0187a2c0c449d5`.
- Updated Issue #26 to SECURITY_ACCEPTANCE_BLOCKED and removed endpoint details from its public body.
- Posted evidence-based triage comments to #23, #27, #66, #68, #71, #72 and #94.
- Main remains unchanged at `e52594f181d2edb77448adcfed64a0fbdffaf3aa`. No PR merged; no PR closed.


## Additional live verification — 2026-11-18
- H current branch head `6608cde89d959257db612d8ff8080f631333f3f3` has check-run `semantic-and-wire-tests` completed SUCCESS.
- H Applied Delivery Evidence Conformance run `44130722532` is SUCCESS on exact tested commit `4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6`, parent of the current H evidence commit; it is not a production trust or durable replay proof.
- PR #93 latest head `c6c6e136f3d1c1b24448e28b754bfe083fe1a0f8` has `bounded-model` check completed SUCCESS on exact head. Workflow action refs remain mutable tags and no independent review is present.
- PR #88 has no check-runs on exact head `bf35b322...`; reported model-checking results still require reproducible execution.


## Rolling execution log — 2026-11-18
- Refreshed live portfolio: 76 Open / 72 Draft / 4 Ready; 64 target main / 12 target non-main; main unchanged at `e52594f...`.
- Extended inventory from the frozen 68-PR baseline to include rolling intake #104–#111 (76 rows total in the CSV).
- Added exact-diff triage comments and per-PR decisions for #28, #36, #46–#50, #56–#62, #66–#70, #73–#93, #98–#103 and #104–#111.
- Corrected H/C branch-integrity incident status: current H Owner branch `6608cde...` and C Owner branch `88992da...` have restored trees; the earlier destructive snapshots remain historical incident records. (The separate C research branch `a69007a...` is not the C Owner branch.)
- Verified PR #93 `bounded-model` SUCCESS on exact head `c6c6e136...`; verified H `semantic-and-wire-tests` SUCCESS on current H head `6608cde...`; H Applied Delivery Evidence run `44130722532` SUCCESS on exact tested commit `4e65a2e...`.
- No PR merged or closed. The four Ready PRs #108–#111 have no formal reviews, review threads or check-runs and remain READY_AFTER_REVIEW only.


- Added exact-diff triage comments and inventory classifications for #1, #42, #44, #45, #51, #52, #54, #55, #63, #64, #65, #94 and #95.
- #94 remains blocked on C Owner review and a schema-only trigger execution; no branch or main merge performed.
- #101 explicitly flagged as ARCHITECTURE_CONFLICT because its L1 Option A selected wording conflicts with Storage ADR Blob bb544ba2...; no Storage Owner source change performed.


## Inventory completion checkpoint — 2026-11-18
- The structured inventory now contains 76 rows, one for every live Open PR in the refreshed collection.
- All 76 rows have exactly one primary classification, priority, accountable Owner/role, blocker, merge eligibility and next action.
- Classification distribution: DRAFT_ACTIVE 48; BLOCKED_BY_DEPENDENCY 11; STALE_UNCERTAIN 5; ARCHITECTURE_CONFLICT 4; NEEDS_REBASE 2; SECURITY_REVIEW_REQUIRED 2; READY_AFTER_REVIEW 4.
- Priority distribution: P0 2; P1 55; P2 19.
- Live state at this checkpoint: 76 Open / 72 Draft / 4 Ready; 64 target main / 12 target non-main; main `e52594f181d2edb77448adcfed64a0fbdffaf3aa`.
- No PR merged or closed. Four Ready PRs lack formal reviews and checks; all remain blocked at M7/M6.


- PR #27 received a second repository-side redaction pass on head `27cd318047041e941d78156755dfa885eb41f8df`: removed remaining host/runner identifiers, proxy endpoints/ranges, internal egress service names and diagnostic environment-value output. Exact scan found no routable IPv4/Tailnet hostnames/private-key blocks/GitHub token patterns. No check-runs exist on the new head; host-side security acceptance remains blocked.
- Reclassified all 76 live Open PRs in the CSV with exactly one primary classification, priority, accountable Owner/role, blocker, merge eligibility and next action. Validation found zero missing classifications.

## Verified mainline merges — 2026-11-18

| Time (UTC) | PR | Candidate head | Merge SHA | Result | Evidence |
|---|---|---|---|---|---|
| 2026-11-17T18:09:17Z | #108 Session 2 Phase 0 report | `2d219492c0eb53ec4c7bde800f617b177da6f6b8` | `98fe7235fac8013b00ffa8a129d0f8fed830acf6` | **MERGED — documentation publication; review gap remains** | Live PR state merged; only author-account COMMENTED review |
| 2026-11-17T18:09:36Z | #109 Session 1 Phase 0 report | `e9dda0d8d3e62d7d370892e032cb18a77872e233` | `4bee3e886cc0dec4a8d03817acd180ba979f8ceb` | **MERGED — documentation publication; review gap remains** | Live PR state merged; only author-account COMMENTED review |

These two merges are verified repository facts, but they do **not** demonstrate compliance with the repository's independent-review requirement: each PR's only review record was COMMENTED by `oahcom`, the same account that authored the PR. Their merge is publication of research artifacts, not approval of the reports' proposals, not normative adoption, and not authorization for Phase 1 implementation. A retrospective independent review and governance disposition are required before their recommendations are relied upon.

## Post-merge remediation — 2026-11-18

- Current main: `4bee3e886cc0dec4a8d03817acd180ba979f8ceb`; it is four commits ahead of the previous frozen main and includes the two report files.
- Current portfolio: 74 Open PRs = 72 Draft + 2 Ready; 62 target main / 12 target non-main.
- PR #110 remediation committed on its existing branch; current head `e10cc49e9b7cfc46e30e85d67ca20a8cdc4ca60b`. The report and PR body now treat Codex as research-only under Issue #41 and distinguish the documented read-only retrieval connector from the repository's separate write-capable GitHub App path. Still no independent review or exact-head checks.
- PR #111 remediation committed on its existing branch; current head `adfccc6804c8d32d7bb7110e948146fd57b8632a`. The report now preserves BLOCKER as a finding severity and maps the seven Gate checks to the existing lifecycle/DoR/DoD. Still no independent review or exact-head checks.
- PR #110/#111 remain Ready but are not merge-eligible: the only recorded reviews are author-account COMMENTED reviews on earlier heads; exact-head statuses/check-runs are absent.
- No additional merge was attempted. The 74 open PRs still have zero results for GitHub search qualifiers `review:approved`, `review:changes_requested`, and `review:required`; no currently open PR has a GitHub-approved review evidenced by those queries.

## Recovery-branch synchronization merge — 2026-11-18

| PR | Direction | Merge SHA | Result |
|---|---|---|---|
| #112 | `main` → `recovery/pr-recovery-002-baseline-2026-11-18` | `8b24ad87c0c795b4cf095a54263692d9baed8efe` | **MERGED — recovery-branch maintenance only** |

PR #112 contained exactly the two already-published Session 1 and Session 2 research report files from current main. It merged main into the recovery evidence branch only; it did **not** merge recovery artifacts or any application/architecture changes into main. Post-merge compare confirms the recovery branch is now 79 commits ahead / 0 behind current main, with merge base exactly `4bee3e886cc0dec4a8d03817acd180ba979f8ceb`.

| #113 | `main` → `research/ai-dev-os-001-session-4` | `5f42acb1391a06703f9aa1a7b615f4dd62d5cbea` | **MERGED — Session 4 branch synchronization only** |

PR #113 merged the two already-published Session 1/2 report files from current main into the Session 4 publication branch. It did not merge Session 4 research into main. PR #110 now compares 5 ahead / 0 behind current main and reports mergeable=true; the new exact Head is the synchronization merge SHA above. Independent review of the exact new Head remains outstanding because this recovery session authored the Session 4 remediation.

## C Owner branch integration — PR #94 — 2026-11-18

| PR | Target branch | PR head | Merge SHA | Merge time UTC | Result |
|---|---|---|---|---|---|
| #94 | `session-c-agent-integration-2026-11-16` | `47e41a739de42621452a07e041b64d9826098c4a` | `62c3e799b36c56bd82972a4d7d561f246598deaf` | `2026-11-17T18:45:15Z` | **MERGED — C workflow path-filter correction** |

### Exact validation evidence
- Workflow run on merge commit: [44151236345](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44151236345) — job `c-provider-outcome` SUCCESS; schema and crypto candidate-vector step SUCCESS.
- Controlled schema-only path push: `492998863842f625e3697a0544d566fcbb095b62`; [run 44151284885](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44151284885) — job and target conformance step SUCCESS.
- Restore commit: `a9a587e9f73266c74c84c65fda1beeb4246f5a80`; [run 44151338457](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44151338457) — job and target conformance step SUCCESS.
- Current C Owner branch head was read as `a9a587e9f73266c74c84c65fda1beeb4246f5a80`.
- Diff was one line adding the 1.0.1 schema path to the workflow's `push.paths`; no schema or Provider Outcome semantics changed.
- The only submitted PR review is COMMENTED by `oahcom`, the PR author. The merge is recorded as **MERGED_REVIEW_GAP** for independent-review provenance; successful workflow execution proves the trigger/conformance behavior, not independent Owner approval.
- The temporary schema trigger probe changed only trailing whitespace; original schema content was restored and its blob SHA verified. This must not be described as a schema semantic change.

### Portfolio impact
- Current open portfolio: **73 Open = 71 Draft + 2 Ready**; **62 target main + 11 target non-main**.
- Across the original 76-row tracked inventory, #94/#108/#109 are now merged; #112/#113 were recovery/branch synchronization PRs outside that original inventory and did not alter main application architecture.
- Current tracked classification: DRAFT_ACTIVE 48; BLOCKED_BY_DEPENDENCY 10; STALE_UNCERTAIN 5; ARCHITECTURE_CONFLICT 4; NEEDS_REBASE 2; SECURITY_REVIEW_REQUIRED 2; READY_AFTER_REVIEW 2; MERGED_REVIEW_GAP 3.
- No new merge into main occurred in this checkpoint; #94 targets the C Owner branch only.
