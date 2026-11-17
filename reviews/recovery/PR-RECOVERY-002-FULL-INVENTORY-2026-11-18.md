# PR-RECOVERY-002 — Full Pull Request Inventory & Recovery Closeout
# PR 积压恢复 — 全量 PR 盘点与恢复结项

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Snapshot date: 2026-11-18
- Main HEAD: `43203675389b7cb351587e465ab3acbb6e165efd`
- Main tree: `d37df990fcb59827b8f55c57065cd8c15434fd09`
- Inventory source: GitHub REST pulls API, `state=all`, pages 1–2, `per_page=100`; 107 PR records returned.
- This is a metadata-complete inventory and a disposition register. It is not a claim that every historical diff has undergone a fresh line-by-line code review.

## 1. Executive result / 执行结果

| Metric | Result |
|---|---:|
| Total PR records | 107 |
| Merged | 87 |
| Closed, not merged | 20 |
| Closed Drafts, not merged | 17 |
| Open PRs after recovery actions | 0 |
| Current merge candidates | 0 (no open PRs) |

The repository currently has no open PRs. This does not mean all project work is complete: closed-unmerged PRs remain historical/superseded/rejected artifacts, and Issue #26 remains OPEN / SECURITY_ACCEPTANCE_BLOCKED.

仓库当前没有开放 PR。这不代表项目工作全部完成：未合并关闭的 PR 仍作为历史、替代、拒绝或验证记录保留；Issue #26 仍为 OPEN / SECURITY_ACCEPTANCE_BLOCKED。

## 2. Targeted recovery items / 指定项目整改

### PR #121 — H Applied Delivery Evidence 1.0.0
- Already merged before this recovery execution. Merge commit: `ab1fa87d74ca4a632155aa19569533ea560109d5`; final PR head: `0c878b7b5a14dcc5a417f006818920d96254eaab`.
- Follow-up PR #136 merged the H-to-C resolver `record_ref` equality guard; exact-head H conformance run #44184689270 reports 30 tests OK.
- PR #133 merged the exact-head 29-test evidence correction for PR #131 / run #44182801145.
- These are bounded reference-validator/conformance results only. Production trust roots, live C/I/D ledgers, durable replay, G persistence/restore, cross-owner approvals and Full Applied remain unproven.
- No further change to the already merged PR #121 is possible/necessary; remaining blockers belong to successor work items.

### PR #23 — AID-2026-001 governance package
- Closed unmerged intentionally; unique artifacts were published by merged PR #116.
- Remaining shared-file changes were not replayed because newer main versions superseded them.
- PR #23 comments #6958704123 and #6962343810 record the disposition. No unique artifact currently identified as lost.

### PR #27 — Ubuntu worker endpoint
- Merged, but merge is not security acceptance.
- Issue #26 was closed as `completed` despite its own body retaining `SECURITY_ACCEPTANCE_BLOCKED` and unverified security gates.
- Recovery action: Issue #26 reopened with state_reason `reopened`; bilingual recovery checklist/comment ID `6962327308`.
- Outstanding: dedicated least-privilege service account, branch protection/rulesets and required checks, runner-group/environment restrictions, reboot recovery, emergency stop, independent credential-rotation verification, untrusted-PR isolation and accountable Security/Infrastructure Owner acceptance.
- Do not claim secure worker acceptance or continuous A–I operation.

### PR #135 — stale AID reconciliation duplicate
- Superseded by merged PR #137; PR #137 merge commit is current main HEAD.
- Recovery action: PR #135 closed unmerged, with supersession evidence in comment #6962346475.

## 3. Dependency / base-branch topology

PRs are grouped by their declared target branch. A non-main base is a branch-level dependency and must not be confused with a mainline merge request.

- `design/chatgpt-native-execution-model`: #72
- `infra/ai-run-003-adr-run-002`: #33
- `infra/ai-run-003-adr-run-003`: #34
- `infra/ai-run-003-adr-run-004-005`: #35
- `infra/ai-run-003-runtime-plan`: #32
- `main`: #1, #22, #23, #27, #28, #31, #36, #38, #40, #42, #44, #45, #46, #47, #48, #49, #50, #52, #53, #55, #56, #57, #58, #59, #60, #61, #62, #63, #64, #65, #67, #69, #70, #73, #74, #75, #76, #77, #78, #79, #80, #81, #82, #83, #84, #85, #86, #87, #88, #89, #90, #91, #93, #95, #98, #99, #100, #101, #102, #103, #104, #105, #106, #107, #108, #109, #110, #111, #114, #115, #116, #117, #118, #119, #120, #121, #122, #123, #124, #125, #126, #127, #128, #129, #131, #132, #133, #135, #136, #137
- `recovery/pr-recovery-002-baseline-2026-11-18`: #112
- `research/ai-dev-os-001-session-4`: #113
- `research/tech-reality-001-c`: #92
- `review/arch-consol-001-system-wide-2026-11-17`: #51
- `review/arch-consol-002-protocol-alignment-2026-11-17`: #54
- `session-c-agent-integration-2026-11-16`: #94, #97
- `session-d-memory-brain-2026-11-16`: #66
- `session-h-bmcp-protocol`: #96
- `session-i-security-governance-2026-11-16`: #68
- `session-storage-consistency-forget-atomicity-2026-11-16`: #12, #71

Important rule: PRs targeting Owner/research/recovery branches are not candidates for direct mainline merge. Integrate the branch-level work only through its owning branch's approved path, or create a bounded publication PR with explicit provenance and review.

## 4. All-PR inventory / 全量 PR 清单

| PR | State | Base branch | Head (12 chars) | Recovery disposition |
|---|---|---|---|---|
| [#1](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1) | CLOSED / NOT MERGED | `main` | `ed6ad0b316b7` | Superseded by #117; 18 core artifacts already identical on main; remaining useful deltas published in #117. |
| [#12](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/12) | CLOSED / NOT MERGED (draft at closure) | `session-storage-consistency-forget-atomicity-2026-11-16` | `b58d7c5a87c5` | Validation-only PR; explicitly no merge requested; targeted Storage Owner branch. Preserve as historical CI evidence, not a mainline integration PR. |
| [#22](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/22) | MERGED | `main` | `cd01b5a963ac` | Merged; integration fact only, does not imply domain acceptance. |
| [#23](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/23) | CLOSED / NOT MERGED | `main` | `b6b9d2662729` | Superseded by merged #116; unique governance artifacts published there; closed unmerged intentionally. |
| [#27](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/27) | MERGED | `main` | `27cd31804704` | Merged; deployment record only. Security acceptance incomplete; linked #26 reopened. |
| [#28](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/28) | MERGED | `main` | `c77a78037435` | Merged; integration fact only, does not imply domain acceptance. |
| [#31](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/31) | MERGED | `main` | `4d2145b778d1` | Merged; integration fact only, does not imply domain acceptance. |
| [#32](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/32) | MERGED | `infra/ai-run-003-runtime-plan` | `362e3a55959a` | Merged; integration fact only, does not imply domain acceptance. |
| [#33](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/33) | MERGED | `infra/ai-run-003-adr-run-002` | `aba96fcaf7c7` | Merged; integration fact only, does not imply domain acceptance. |
| [#34](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/34) | MERGED | `infra/ai-run-003-adr-run-003` | `44626eade486` | Merged; integration fact only, does not imply domain acceptance. |
| [#35](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/35) | MERGED | `infra/ai-run-003-adr-run-004-005` | `6711b37464d6` | Merged; integration fact only, does not imply domain acceptance. |
| [#36](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/36) | MERGED | `main` | `aab5985caa8c` | Merged; integration fact only, does not imply domain acceptance. |
| [#38](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/38) | CLOSED / NOT MERGED (draft at closure) | `main` | `1fde67380696` | Rejected/superseded execution-channel design; API-key-based worker not approved. |
| [#40](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/40) | CLOSED / NOT MERGED (draft at closure) | `main` | `83531c140380` | Rejected/superseded Codex CLI POC; not approved for use. |
| [#42](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/42) | MERGED | `main` | `890fba6185c6` | Merged; integration fact only, does not imply domain acceptance. |
| [#44](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/44) | MERGED | `main` | `f117bbdcdd3d` | Merged; integration fact only, does not imply domain acceptance. |
| [#45](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/45) | MERGED | `main` | `6c7c5919c1b5` | Merged; integration fact only, does not imply domain acceptance. |
| [#46](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/46) | MERGED | `main` | `8b9ff8efa92a` | Merged; integration fact only, does not imply domain acceptance. |
| [#47](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/47) | CLOSED / NOT MERGED (draft at closure) | `main` | `d556c127ebe8` | Superseded by merged #49; duplicate complexity report. |
| [#48](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/48) | CLOSED / NOT MERGED (draft at closure) | `main` | `cfcc8f20e2bd` | Superseded by merged #50; duplicate system-wide risk report. |
| [#49](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/49) | MERGED | `main` | `131f91743bd5` | Merged; integration fact only, does not imply domain acceptance. |
| [#50](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/50) | MERGED | `main` | `a5dd7eed7fba` | Merged; integration fact only, does not imply domain acceptance. |
| [#51](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/51) | MERGED | `review/arch-consol-001-system-wide-2026-11-17` | `044f84f20446` | Merged; integration fact only, does not imply domain acceptance. |
| [#52](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/52) | MERGED | `main` | `2727bd8544f8` | Merged; integration fact only, does not imply domain acceptance. |
| [#53](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/53) | CLOSED / NOT MERGED (draft at closure) | `main` | `6470f25ca23b` | Superseded by later canonical A assessment #60. |
| [#54](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/54) | MERGED | `review/arch-consol-002-protocol-alignment-2026-11-17` | `208c5e84f64e` | Merged; integration fact only, does not imply domain acceptance. |
| [#55](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/55) | MERGED | `main` | `e9554bd36bb2` | Merged; integration fact only, does not imply domain acceptance. |
| [#56](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/56) | MERGED | `main` | `20e65134e1e0` | Merged; integration fact only, does not imply domain acceptance. |
| [#57](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/57) | CLOSED / NOT MERGED (draft at closure) | `main` | `d354ec419377` | Superseded by merged #60. |
| [#58](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/58) | CLOSED / NOT MERGED (draft at closure) | `main` | `dbec207ecbc1` | Superseded by merged #60. |
| [#59](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/59) | MERGED | `main` | `26fd171f5585` | Merged; integration fact only, does not imply domain acceptance. |
| [#60](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/60) | MERGED | `main` | `bd0e99fcb141` | Merged; integration fact only, does not imply domain acceptance. |
| [#61](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/61) | MERGED | `main` | `4726d93bb54f` | Merged; integration fact only, does not imply domain acceptance. |
| [#62](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/62) | MERGED | `main` | `7b6f00b5ce7d` | Merged; integration fact only, does not imply domain acceptance. |
| [#63](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/63) | MERGED | `main` | `2f3519c8dd43` | Merged; integration fact only, does not imply domain acceptance. |
| [#64](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/64) | MERGED | `main` | `4d6f3391dc23` | Merged; integration fact only, does not imply domain acceptance. |
| [#65](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/65) | MERGED | `main` | `1a0e36517e78` | Merged; integration fact only, does not imply domain acceptance. |
| [#66](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/66) | MERGED | `session-d-memory-brain-2026-11-16` | `4d1a04449cdb` | Merged; integration fact only, does not imply domain acceptance. |
| [#67](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/67) | MERGED | `main` | `abd84746e1e6` | Merged; integration fact only, does not imply domain acceptance. |
| [#68](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/68) | MERGED | `session-i-security-governance-2026-11-16` | `a71985e360c7` | Merged; integration fact only, does not imply domain acceptance. |
| [#69](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/69) | MERGED | `main` | `69783fea3507` | Merged; integration fact only, does not imply domain acceptance. |
| [#70](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/70) | MERGED | `main` | `a7de8c673e61` | Merged; integration fact only, does not imply domain acceptance. |
| [#71](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/71) | MERGED | `session-storage-consistency-forget-atomicity-2026-11-16` | `65c03872cb1e` | Merged; integration fact only, does not imply domain acceptance. |
| [#72](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/72) | MERGED | `design/chatgpt-native-execution-model` | `3bd943ad6ef2` | Merged; integration fact only, does not imply domain acceptance. |
| [#73](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/73) | CLOSED / NOT MERGED | `main` | `6517868afe52` | Superseded/decomposed: research merged via #45; unique Owner remediation artifacts via #114. |
| [#74](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/74) | MERGED | `main` | `ca754250b7ae` | Merged; integration fact only, does not imply domain acceptance. |
| [#75](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/75) | MERGED | `main` | `bf4c400ffc74` | Merged; integration fact only, does not imply domain acceptance. |
| [#76](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/76) | MERGED | `main` | `77e542e0565c` | Merged; integration fact only, does not imply domain acceptance. |
| [#77](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/77) | MERGED | `main` | `eaebbaa631d5` | Merged; integration fact only, does not imply domain acceptance. |
| [#78](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/78) | MERGED | `main` | `3ca3e6d70c10` | Merged; integration fact only, does not imply domain acceptance. |
| [#79](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/79) | MERGED | `main` | `b63f9188387a` | Merged; integration fact only, does not imply domain acceptance. |
| [#80](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/80) | CLOSED / NOT MERGED (draft at closure) | `main` | `21e9a755f793` | Closed draft; research superseded by merged formal-verification package #88. |
| [#81](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/81) | CLOSED / NOT MERGED (draft at closure) | `main` | `8c6cef4c6338` | Closed draft; research superseded by merged Memory OS assessment #86. |
| [#82](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/82) | CLOSED / NOT MERGED (draft at closure) | `main` | `89970923d62f` | Closed draft; research superseded by merged Memory IR assessment #85. |
| [#83](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/83) | MERGED | `main` | `ec17fcfcec8e` | Merged; integration fact only, does not imply domain acceptance. |
| [#84](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/84) | MERGED | `main` | `c6e76b34cbf0` | Merged; integration fact only, does not imply domain acceptance. |
| [#85](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/85) | MERGED | `main` | `c5013d3585d5` | Merged; integration fact only, does not imply domain acceptance. |
| [#86](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/86) | MERGED | `main` | `3892916ce237` | Merged; integration fact only, does not imply domain acceptance. |
| [#87](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/87) | MERGED | `main` | `0d75dd495855` | Merged; integration fact only, does not imply domain acceptance. |
| [#88](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/88) | MERGED | `main` | `bf35b32295d0` | Merged; integration fact only, does not imply domain acceptance. |
| [#89](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/89) | MERGED | `main` | `4960c8b93562` | Merged; integration fact only, does not imply domain acceptance. |
| [#90](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/90) | MERGED | `main` | `0dc8444d590c` | Merged; integration fact only, does not imply domain acceptance. |
| [#91](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/91) | MERGED | `main` | `55c60a11aede` | Merged; integration fact only, does not imply domain acceptance. |
| [#92](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/92) | MERGED | `research/tech-reality-001-c` | `104d288d1be8` | Merged; integration fact only, does not imply domain acceptance. |
| [#93](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/93) | MERGED | `main` | `9408a5dfb879` | Merged; integration fact only, does not imply domain acceptance. |
| [#94](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/94) | MERGED | `session-c-agent-integration-2026-11-16` | `47e41a739de4` | Merged; integration fact only, does not imply domain acceptance. |
| [#95](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/95) | MERGED | `main` | `a1b500e7331e` | Merged; integration fact only, does not imply domain acceptance. |
| [#96](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/96) | CLOSED / NOT MERGED (draft at closure) | `session-h-bmcp-protocol` | `56168d6d58ba` | Temporary H branch recovery proposal; superseded by newer H Owner branch head; do not merge. |
| [#97](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/97) | CLOSED / NOT MERGED (draft at closure) | `session-c-agent-integration-2026-11-16` | `15f7eb55e941` | Temporary C branch recovery proposal; superseded by newer C Owner branch head; do not merge. |
| [#98](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/98) | MERGED | `main` | `6e0218bb5ab5` | Merged; integration fact only, does not imply domain acceptance. |
| [#99](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/99) | MERGED | `main` | `63c0fd869d86` | Merged; integration fact only, does not imply domain acceptance. |
| [#100](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/100) | MERGED | `main` | `dd7acb425585` | Merged; integration fact only, does not imply domain acceptance. |
| [#101](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/101) | MERGED | `main` | `89659270efb3` | Merged; integration fact only, does not imply domain acceptance. |
| [#102](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/102) | MERGED | `main` | `a4c9e30be141` | Merged; integration fact only, does not imply domain acceptance. |
| [#103](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/103) | MERGED | `main` | `669a24deefe1` | Merged; integration fact only, does not imply domain acceptance. |
| [#104](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/104) | MERGED | `main` | `bf3ac0e76ae0` | Merged; integration fact only, does not imply domain acceptance. |
| [#105](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/105) | MERGED | `main` | `a164f1c27732` | Merged; integration fact only, does not imply domain acceptance. |
| [#106](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/106) | MERGED | `main` | `53dc4f4cf564` | Merged; integration fact only, does not imply domain acceptance. |
| [#107](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/107) | MERGED | `main` | `1e26d0a427c4` | Merged; integration fact only, does not imply domain acceptance. |
| [#108](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/108) | MERGED | `main` | `2d219492c0eb` | Merged; integration fact only, does not imply domain acceptance. |
| [#109](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/109) | MERGED | `main` | `e9dda0d8d3e6` | Merged; integration fact only, does not imply domain acceptance. |
| [#110](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/110) | MERGED | `main` | `5f42acb1391a` | Merged; integration fact only, does not imply domain acceptance. |
| [#111](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/111) | MERGED | `main` | `9a7ba7ac8cfc` | Merged; integration fact only, does not imply domain acceptance. |
| [#112](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/112) | MERGED | `recovery/pr-recovery-002-baseline-2026-11-18` | `4bee3e886cc0` | Merged; integration fact only, does not imply domain acceptance. |
| [#113](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/113) | MERGED | `research/ai-dev-os-001-session-4` | `4bee3e886cc0` | Merged; integration fact only, does not imply domain acceptance. |
| [#114](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/114) | MERGED | `main` | `25bd8a1563af` | Merged; integration fact only, does not imply domain acceptance. |
| [#115](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/115) | MERGED | `main` | `4ed91dc3e049` | Merged; integration fact only, does not imply domain acceptance. |
| [#116](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/116) | MERGED | `main` | `ab21fa2c317b` | Merged; integration fact only, does not imply domain acceptance. |
| [#117](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/117) | MERGED | `main` | `19ae26671ab8` | Merged; integration fact only, does not imply domain acceptance. |
| [#118](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/118) | MERGED | `main` | `333ee980aa72` | Merged; integration fact only, does not imply domain acceptance. |
| [#119](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/119) | MERGED | `main` | `de1d0c6a0c19` | Merged; integration fact only, does not imply domain acceptance. |
| [#120](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/120) | MERGED | `main` | `069984b5c391` | Merged; integration fact only, does not imply domain acceptance. |
| [#121](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/121) | MERGED | `main` | `0c878b7b5a14` | Merged; integration fact only, does not imply domain acceptance. |
| [#122](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/122) | CLOSED / NOT MERGED (draft at closure) | `main` | `b346204a614e` | Superseded by corrected publication PR #124. |
| [#123](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/123) | CLOSED / NOT MERGED (draft at closure) | `main` | `3fbcf6fcccf1` | Superseded by corrected publication PR #124. |
| [#124](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/124) | MERGED | `main` | `60ef4aeef5d6` | Merged; integration fact only, does not imply domain acceptance. |
| [#125](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/125) | CLOSED / NOT MERGED (draft at closure) | `main` | `adac91d953e6` | Superseded by current-main refresh PR #126/#124. |
| [#126](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/126) | MERGED | `main` | `c022fe2f4c61` | Merged; integration fact only, does not imply domain acceptance. |
| [#127](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/127) | CLOSED / NOT MERGED (draft at closure) | `main` | `3759c2be1f1a` | Superseded by corrected source refresh; do not merge stale snapshot. |
| [#128](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/128) | MERGED | `main` | `c56fbeb78d66` | Merged; integration fact only, does not imply domain acceptance. |
| [#129](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/129) | MERGED | `main` | `6622f65bea43` | Merged; integration fact only, does not imply domain acceptance. |
| [#131](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/131) | MERGED | `main` | `40c52edb97f1` | Merged; integration fact only, does not imply domain acceptance. |
| [#132](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/132) | MERGED | `main` | `c5e16e224f7e` | Merged; integration fact only, does not imply domain acceptance. |
| [#133](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/133) | MERGED | `main` | `a79443858674` | Merged; integration fact only, does not imply domain acceptance. |
| [#135](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/135) | MERGED | `main` | `1ca57512cdc0` | Superseded by merged #137; closed during this recovery. |
| [#136](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/136) | MERGED | `main` | `fe69b105a44e` | Merged; integration fact only, does not imply domain acceptance. |
| [#137](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/137) | MERGED | `main` | `a0dd00168899` | Merged; integration fact only, does not imply domain acceptance. |

## 5. Merge and protection assessment / 合并与保护评估

- Main branch API reports `protected=false`; `protection.enabled=false`; required status-check enforcement is off.
- Direct branch-protection endpoint returned HTTP 403 (integration lacks access), so repository Rulesets could not be independently inspected. Do not infer that no Rulesets exist.
- Because Main is not protected by the legacy branch-protection setting, do not treat GitHub's mergeability flag as a substitute for required review/CI/Owner gates. Administrative policy must be configured and verified by an authorized administrator.
- No PR is currently open, therefore no current PR can be merged in this snapshot.

## 6. Explicit unresolved work / 未关闭事项

1. Issue #26 remains OPEN / SECURITY_ACCEPTANCE_BLOCKED. It must not be closed until each applicable security gate has evidence and accountable Owner acceptance.
2. PR #121's candidate package remains non-production. PR #136 and #133 improve bounded reference evidence only.
3. PR #23, #27, #121 and #135 now have recovery comments documenting actual status and evidence boundaries.
4. The 21 closed-unmerged PRs remain in GitHub history. Their disposition is recorded above; do not reopen a PR solely because it is not merged.
5. The inventory does not assert a fresh file-by-file semantic review of all 107 PR diffs. Historical merged changes require targeted audit only when current-main defects or traceability gaps identify a reason.

## 7. Recovery verdict / 恢复结论

**PR QUEUE: EMPTY. / PR 队列：已清空。**

**PROJECT ACCEPTANCE: NOT COMPLETE. / 项目验收：未完成。**

This recovery closes the stale open-PR queue by reconciling the remaining duplicate PR #135. It does not convert merges into approvals, close Issue #26, pass architecture gates, or authorize production activation.

本次恢复通过关闭已被 PR #137 取代的重复 PR #135 清空开放 PR 队列；不把合并事实转换为 Owner 批准，不关闭 Issue #26，不宣称架构 Gate 通过，也不授权生产激活。
