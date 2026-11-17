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

## Additional Owner-branch merges discovered in live closed-PR census — 2026-11-18

These 11 PRs were already closed/merged in the current GitHub state. They target non-main Owner/runtime/research branches and do not advance main directly. The formal PR review API returned zero submitted review records for every one of them.

| PR | Target branch | Merge SHA | Merged UTC | Review evidence |
|---|---|---|---|---|
| #32 | `infra/ai-run-003-runtime-plan` | `4d2145b778d12a474a73313e722ec07ded83c467` | 2026-11-17T18:51:51Z | No submitted review records |
| #33 | `infra/ai-run-003-adr-run-002` | `362e3a55959aa4c3ce4e751cae0bbeaba0db811e` | 2026-11-17T18:50:57Z | No submitted review records |
| #34 | `infra/ai-run-003-adr-run-003` | `b2b4fe1a20750d5cad66b5485f920edd63b57f6e` | 2026-11-17T18:51:47Z | No submitted review records |
| #35 | `infra/ai-run-003-adr-run-004-005` | `44626eade4862ea2c903c77064745da8021eb82f` | 2026-11-17T18:50:50Z | No submitted review records |
| #51 | `review/arch-consol-001-system-wide-2026-11-17` | `f117bbdcdd3d25937e78abb4c619f654584e8492` | 2026-11-17T18:51:55Z | No submitted review records |
| #54 | `review/arch-consol-002-protocol-alignment-2026-11-17` | `044f84f204463ac5a974b0d40129e76fe5ce0dc9` | 2026-11-17T18:51:03Z | No submitted review records |
| #66 | `session-d-memory-brain-2026-11-16` | `7e6d0b133dae88f442665e7b05a54060e047647e` | 2026-11-17T18:51:18Z | No submitted review records |
| #68 | `session-i-security-governance-2026-11-16` | `ea949896f891f0a08ef5fe9358edadc8a49e546f` | 2026-11-17T18:51:22Z | No submitted review records |
| #71 | `session-storage-consistency-forget-atomicity-2026-11-16` | `f6887cc9ea5bfa5293c1bc47e9f10e582830cba3` | 2026-11-17T18:51:26Z | No submitted review records |
| #72 | `design/chatgpt-native-execution-model` | `890fba6185c655d9e6e99ca2a7e9cf1e9b6e62e7` | 2026-11-17T18:51:10Z | No submitted review records |
| #92 | `research/tech-reality-001-c` | `69783fea3507ac9913ab4eae75441e4232fa017d` | 2026-11-17T18:51:14Z | No submitted review records |

These are recorded as `MERGED_REVIEW_GAP`, not as approved architecture decisions. Retrospective Owner/independent review is required to establish whether the merged branch content is acceptable, still proposal-only, or needs corrective follow-up.

## Main merge — PR #110 Session 4 research publication

| PR | Target | PR head | Merge SHA | Merged UTC | Review/check evidence |
|---|---|---|---|---|---|
| #110 | `main` | `5f42acb1391a06703f9aa1a7b615f4dd62d5cbea` | `4a0acc1608f0909bafb64ac90f0a724b8223d546` | 2026-11-17T18:56:12Z | Only author-account COMMENTED review on earlier head `ab6b5c2...`; no combined status contexts or PR workflow runs on merge SHA |

PR #110 is merged into main. Its report contains the corrected Issue #41 boundary and connector distinction, but the merge did not satisfy the independent-review evidence requirement. The merge is irreversible; retrospective independent review and governance disposition are required before relying on its recommendations. Current main HEAD is now `4a0acc1608f0909bafb64ac90f0a724b8223d546`.

## Rebase and recovery package normalization

- PR #111 was replayed onto current main `4a0acc1608f0909bafb64ac90f0a724b8223d546` without changing its report blob. New head: `9a7ba7ac8cfc6d3de0d732bb7e677ff2288a4ca5`; compare: 1 commit ahead / 0 behind; one report file only. No status/check evidence or independent approval.
- PR #105 recovery package was compacted/rebased onto the same main commit. The eight artifact files were preserved and the branch history was reduced to a single new commit at the time of rebase; later evidence updates may advance its self-referential head. No application or architecture files are changed by #105.
- Current live portfolio after #110 merge: **61 Open = 60 Draft + 1 Ready (#111)**; all 61 open PRs target main. The 76-row inventory consists of 61 Open and 15 Merged.
