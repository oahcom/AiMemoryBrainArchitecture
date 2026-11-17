# Issue #20 — v3.2.7 Callback-Seam Currentness Audit v0.3.0
# Issue #20 — v3.2.7 Callback-Seam 当前性审计 v0.3.0

- Status / 状态: **P COORDINATOR CROSS-REVIEW / ROLE SIMULATION ONLY**
- Snapshot date / 快照日期: 2026-11-17
- C HEAD: `8d7298d7f56b1df48229799ff6462a8db634e7ed`
- D HEAD: `188f414fa2c080111325cb52c93f8cd1dc551388`
- H HEAD: `e0d89f1b6dac3bdcf1f0ab4e3f062dd7bc53fdf8`
- I HEAD: `947553e77375a94671523931518e0d9673c4a766`
- Storage HEAD: `19eb636d364c87850afdcd1d87c04c7fe920f115`
- A HEAD: `71dea4964a15d5a770567fdc5be97ef4b054b038`
- P HEAD before this audit: `cc6792652af0aa6b2ca931e1e7e5c851f52db7bd`
- Decision / 结论: **v3.2.7 is a valid candidate bundle, but its H test pin is stale and C/D/I decisions do not yet adopt the current callback seam / current owner proof blobs. Prepare v3.2.8; NOT JOINTLY ACCEPTED / NOT FROZEN.**

## 1. Executive result / 执行结论

The previous exact-version migration has advanced:
- C accepts H Phase 3.8.11 mapping Blob `c196fdc...` with H Unified 1.2.14 and CSubmitOutcome 1.0.1.
- D and I have current-schema reviews against H 1.2.14 and the base mapping.
- H has a separate authority-join mapping for I/D/Storage callbacks and an expanded 27-test Provider Outcome suite.
- Storage has published v3.2.7 as a successor candidate on its own branch.

The remaining problem is not the base C/H field mapping. It is the exact scope of Owner acceptance and test currentness:
1. C's Phase 3.8.16 review accepts H base mapping `c196fdc...`, but does not bind H callback authority mapping `1cbe74e...`, validator `eab961a...`, tests `70a3796...` or the 27-test run.
2. D's current H review `6aca7d0...` pins D crosswalk `bf35b7f...`; current D crosswalk is `c4adf82...`. H has reviewed `c4adf82...`, but D must accept its own current P0 source and callback boundary.
3. I's current H review `fbd44d5...` pins I P0 `35e6843...`; current I P0 is `44986f5...`. H's I review also pins an older I P0. I must re-review its current allowlist and callback.
4. H's Phase 3.8.12 closure `d9c09f0...` pins an older mapping and the earlier 22-test run. H has a newer 27-test run and a separate authority-join mapping; it needs a current closure.
5. Storage v3.2.7 manifest `4435fc0...` pins the earlier H test Blob `53774ac...` and 25-test run `44068247661`. Current H test Blob/run are `70a3796...` / `44068869146` (27 tests).
6. A has not published a fresh integration review of the current v3.2.7/v3.2.8 callback bundle.

**Disposition: ACCEPT AS A COHERENT L1/L2 ARCHITECTURE CANDIDATE WITH ENUMERATED EXACT-BUNDLE BLOCKERS; DO NOT FREEZE.**

## 2. Exact current source set / 当前精确源集合

| Owner | Artifact | Exact Blob / run | Review status |
|---|---|---|---|
| C | CSubmitOutcome 1.0.1 schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | Current |
| C | C sequence namespace amendment | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | Current |
| C | RecoveryJoin P0 crosswalk | `df12af95e6859a389ba71eb1b7dba512b9feb8f6` | Current candidate |
| C | Phase 3.8.16 exact review | `f2d33a8998f8a6906c9bef8be6f9e880c61a0c8c` | Accepts H base mapping `c196fdc...`; not H callback map |
| H | Unified schema 1.2.14 / wire 1.3.0 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Current |
| H | RecoveryJoin 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` | Current |
| H | RecoveryCutoff 1.0.5 | `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` | Current |
| H | Phase 3.8.11 base C mapping | `c196fdc7a9d88e344d37ba2810a9bce1803f8b96` | C reviewed base mapping |
| H | Phase 3.8.10 authority-join mapping | `1cbe74eba69325510d6b1019d971661f965eabf8` | Callback candidate; fresh C/D/I/Storage adoption required |
| H | Provider Outcome validator | `eab961a08d41e871f38543b18ee60cf024977414` | Integration seam; callbacks injected |
| H | Provider Outcome tests | `70a3796446553464e71999f916b76bc22e47da11` | Current 27-test source |
| H | Provider Outcome CI | Run `44068869146`, commit `e0d89f1b6dac3bdcf1f0ab4e3f062dd7bc53fdf8` | **27/27 PASS** |
| H | RecoveryCutoff CI | Run `44068869090`, same commit | **288 total: 266 passed / 22 skipped / 0 failed** |
| H | Current D cross-review | `6d45398885a842b0e5effc860bc97d7ecd3a8435` | H accepts D crosswalk `c4adf82...`; not D Owner acceptance |
| H | Current I cross-review | `7acafcdc38079cdc51965f7b416d547372083965` | Pins I P0 `5c0e204...`; stale to current I P0 |
| D | Current D crosswalk | `c4adf827dd62d44c43b8e871dec4835581508adf` | Current source |
| D | Phase 3.8.8 schema/fence review | `6aca7d020caecf3c69debf614c903bf469583260` | Pins older D crosswalk `bf35b7f...` |
| I | Current Phase 3.8.10 P0 allowlists | `44986f5f864bcdc1a79d34978273644d381a68c0` | Current source |
| I | Phase 3.8.12 schema/P0 review | `fbd44d57bdb4fc15c4c254fcd9d8ac4c58d365fc` | Pins older I P0 `35e6843...` |
| Storage | v3.2.7 successor manifest | `4435fc0340a4fce10751679a95f3b4c821bdae4d` | Candidate; H test/run pins superseded |
| Storage | Normative v3.2.3 technical body | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Remains normative candidate |
| Storage | COC companion §§15–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Batch-before-Manifest / union semantics |
| A | Integration branch HEAD | `71dea4964a15d5a770567fdc5be97ef4b054b038` | No fresh v3.2.7 callback-bundle review found |

## 3. Callback semantics / Callback 语义

H authority-join mapping `1cbe74e...` defines three independent owner-authority callbacks:
- I `verify_i_terminal_decision(envelope, c_object)`: exact I terminal decision, authorization scope, currentness and applicable `COMMIT_WON` proof.
- D `verify_d_clearance(envelope, c_object)`: exact ForgetFenceGeneration, clearance, lineage/barrier and current D fence.
- Storage `verify_storage_resolution_proof(envelope, c_object)`: DB incarnation, GID, PrepareAttempt, participant ledger, same-GID terminal resolution and visibility boundary.

These callbacks cannot be replaced by the COC callback. A proven contradiction returns INVALID; missing/unavailable callback or evidence returns UNKNOWN. H cannot mint C/I/D/Storage truth.

This is a sound contract-level separation, but C/D/I/Storage have not all adopted the exact callback mapping. The 27 tests prove bounded orchestration behavior only.

## 4. CI evidence ceiling / CI 证据上限

- H Provider Outcome run `44068869146`: exact current H head `e0d89f1...`, 27 tests, SUCCESS.
- H RecoveryCutoff run `44068869090`: same commit, 288 tests, 266 passed, 22 skipped, 0 failed.
- The current callback orchestration tests use test doubles and mock schema/semantic/digest primitives. They are not a complete unmocked H envelope + C object end-to-end test.
- No production I/D/Storage callback adapters, provider issuer truth, same-key authoritative lookup, multi-replica C egress linearization, COC quorum deployment or Storage physical topology is proven.

## 5. Required next sequence / 后续顺序

1. H publishes a current closure binding base mapping `c196fdc...`, callback mapping `1cbe74e...`, schema `09fcd1f...`, validator `eab961a...`, tests `70a3796...` and run `44068869146`.
2. C reviews the callback mapping and its effects on C ProviderAttempt/Gate/COC/egress semantics.
3. D re-reviews current D crosswalk `c4adf82...` and H D-clearance callback.
4. I re-reviews current I P0 `44986f5...` and H terminal-decision callback, preserving COMMIT_WON semantics and I's trust authority.
5. Storage refreshes v3.2.7 to v3.2.8 with current test/run and fresh exact Owner decisions; prove bidirectional owner admission/COC joins and same-GID recovery.
6. A reviews that same exact v3.2.8 manifest after C/D/I/H/Storage updates.

## 6. Gate state / Gate 状态

- Base H 1.2.14 × C 1.0.1 mapping: ACCEPTED AS L1/L2 CANDIDATE; not frozen.
- Callback authority mapping: candidate only; affected Owner adoption outstanding.
- Full unmocked validation: NOT RUN.
- Production trust/profile/key custody: OPEN.
- Production owner-ledger pagination/currentness: NOT VERIFIED.
- C provider adapter and same-key lookup: NOT VERIFIED.
- COC quorum / Storage same-GID / visibility deployment: NOT VERIFIED.
- JF-10 P0, R1/R2, Gate B/C, Multi-PolicyDomain, Global Forget, Full Applied and production activation: OPEN / BLOCKED / NOT AUTHORIZED.

## 7. Provenance / 来源说明

This audit is a Session P coordinator cross-review and does not sign for any Owner. Exact Blob identities and workflow results were read from GitHub. It does not authorize merge, production egress, deployment or freeze.

本审计是 Session P 协调者跨审查，不代替任何 Owner 签署。精确 Blob 和 Workflow 结果来自 GitHub 读回，不授权 Merge、生产 Egress、部署或冻结。
