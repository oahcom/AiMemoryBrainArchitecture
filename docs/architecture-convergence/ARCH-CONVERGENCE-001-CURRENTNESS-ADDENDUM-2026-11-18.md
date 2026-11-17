# ARCH-CONVERGENCE-001 — Currentness Addendum (2026-11-18)
# ARCH-CONVERGENCE-001 — 当前性补充记录（2026-11-18）

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Review baseline: `main@6c325804027b88de1014ab3364cdda7e0c023ba6`
- Main commit date: 2026-11-17T21:29:04Z
- Main tree: `68b855373b46ed780d615be0e184f62042c16f52` (665 entries; recursive tree not truncated)
- Status: **DRAFT / CURRENTNESS CORRECTION / NON-NORMATIVE**
- Purpose: supersede stale live-status and source-tree observations in earlier ARCH-CONVERGENCE-001 documents.
- Authority: this addendum changes no Owner contract, ADR, schema, implementation Gate, or production authorization.

本文件用于修正 ARCH-CONVERGENCE-001 早期文档中的过期实时状态与来源树观察，不改变任何 Owner 契约、ADR、Schema、实现 Gate 或生产授权。

## 1. Executive correction / 执行摘要

The A–E workstream proposals and their integration synthesis are already merged into `main`. They must not be re-created or described as still-open Draft PRs.

At the inventory snapshot used for this addendum, the original ARCH-CONVERGENCE-001 workstream PRs were no longer open. PR-RECOVERY-002's merged audit (#118) recorded 73 merged and 16 closed-unmerged PRs at its audit snapshot. Subsequent focused publication PRs #121 and #124 were opened after that snapshot; #121 has since merged and #124 is this currentness addendum. Draft PR #122 was superseded and closed. The repository is not waiting for the original ARCH-CONVERGENCE-001 documentation PRs to merge.

ARCH-CONVERGENCE-001 remains **architecturally unresolved and not implementation-authorized**. Publication/merge of proposal documents is not Owner approval, ADR approval, Gate passage, or executable correctness evidence.

A–E 五个工作流提案及其整合文件已经合入 `main`，不得重新创建，也不得继续描述为尚未合并的 Draft PR。

本补充文件所用清单快照中，ARCH-CONVERGENCE-001 原工作流 PR 已不再开放。PR-RECOVERY-002 的已合并审计 #118 在其审计快照中记录了 73 个已合并 PR 和 16 个关闭未合并 PR。此后又创建了聚焦发布 PR #121 和 #124；#121 已随后合并，#124 即本当前性补充 PR。Draft PR #122 已被替代并关闭。当前问题不是等待原 ARCH-CONVERGENCE-001 文档 PR 合并。

ARCH-CONVERGENCE-001 在架构层面仍未解决，也未获实现授权。提案文档发布/合并不等于 Owner 批准、ADR 批准、Gate 通过或可执行正确性证明。

## 2. Exact PR disposition / PR 精确状态

| Workstream | PR | Merge commit | Disposition |
|---|---:|---|---|
| PRODUCT-FIRST unified review | #89 | `59769e109212eda813c75ae538bf8a22b9c4a222` | MERGED — research synthesis only |
| A — Source of Truth | #99 | `9ebcfaf0a76a9152662a18d8a20b9e299a348cdd` | MERGED — inventory proposal only |
| B — Canonical Transaction | #101 | `4e3cd1556b7ce18118148a87409d0e9c0343acd0` | MERGED — conditional contract proposal only |
| C — Forget/Auth/Recovery | #103 | `2118741fcad6bcde2c9bcdfd4dbecc42403df252` | MERGED — conditional safety proposal only |
| D — Context Applied/Runtime | #104 | `b0acc289663d99797c7b12ae60ce97b80266ea41` | MERGED — conditional runtime proposal only |
| E — Minimum Runnable Architecture | #106 | `e571a0f69b22ff5f565286981de839cd8eab515a` | MERGED — implementation plan, not authorization |
| Integration synthesis + adversarial matrix | #107 | `e6adb447911403bd319ee8a9f7bc9014180e1d81` | MERGED — interim integration only |
| C/G/H Applied consumer audit | #119 | `431468a9066f6fe68d9c514f3603ab1a603146ff` | MERGED — audit publication; findings remain open |
| B domain post-merge reconciliation | #120 | `6c325804027b88de1014ab3364cdda7e0c023ba6` | MERGED — status reconciliation; B gates remain open |

All above PR metadata was re-read from GitHub. At this addendum's frozen baseline, PR #120's merge commit was the `main` HEAD and PR #119's merge commit was its direct parent. PR #121 was merged later and advanced main.

上述 PR 状态均按本补充文件冻结基线从 GitHub 元数据读取。该基线时 PR #120 的合并提交是 `main` HEAD，PR #119 的合并提交是其直接父提交；PR #121 随后合并并推进了 main。

## 3. Frozen-baseline source-tree correction / 冻结基线来源树修正

At the frozen baseline `main@6c325804027b88de1014ab3364cdda7e0c023ba6`, the recursive tree had 665 entries and was not truncated. The following README-mapped roots were present or absent at that baseline:

| Path | Frozen-baseline observation |
|---|---|
| `02-domain-model/` | PRESENT |
| `06-memory-context/` | PRESENT |
| `03-memory-brain/` | ABSENT |
| `04-memory-compiler/` | ABSENT |
| `05-memory-runtime/` | ABSENT |
| `08-protocols/` | ABSENT |
| `08-bmcp-protocol/` | ABSENT |
| `09-storage-and-index/` | ABSENT |
| `09-security-governance/` | ABSENT |
| `10-security-and-governance/` | ABSENT |
| `11-consistency-and-recovery/` | ABSENT |
| `12-testing-and-acceptance/` | ABSENT |

This corrects the earlier ARCH-CONVERGENCE-001 source inventory and PRODUCT-FIRST integration snapshot where they claimed `02-domain-model/` was absent. `08-bmcp-protocol/` was absent at this frozen baseline but was published later by PR #121. Remaining absent roots continue to be a discoverability/publication issue, but absence of a README-mapped root does not prove that the corresponding Owner branch contract does not exist.

在冻结基线 `main@6c325804027b88de1014ab3364cdda7e0c023ba6` 的 665 项递归树中，`02-domain-model/` 与 `06-memory-context/` 存在；当时 `08-bmcp-protocol/` 尚不存在，后由 PR #121 发布。其余所列规范根目录在该冻结基线中缺失。这修正了早期文档错误地声称 `02-domain-model/` 不存在的记录。目录缺失属于规范可发现性/发布问题，但不能据此推断对应 Owner 分支不存在相关契约。

## 4. Newer blocking evidence / 后续新增阻塞证据

### 4.1 PR #119 — C/G/H Applied consumer audit

PR #119 was merged as a documentation-only audit. Its disposition is **REQUEST CHANGES / CANDIDATE ONLY / APPLIED FREEZE BLOCKED**. The original #119 audit findings are now at different remediation stages:

- **H-ADE-001 — duplicate JSON object members (P0):** #121 subsequently published a candidate validator using `object_pairs_hook` to reject duplicates at all nesting depths, with top-level and nested negative tests. GitHub Actions run [#44180944513](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44180944513) ran on PR #121's exact Head `0c878b7b5a14dcc5a417f006818920d96254eaab` (`pull_request`, run number 9) and completed **SUCCESS**. The `applied-delivery-evidence` job and the schema/semantic conformance test step both succeeded. This verifies the bounded reference test suite, not H Owner acceptance or production closure.
- **H-ADE-003 — replay-time authorization (P0):** #121 subsequently published a tri-state `verify_current_replay_authorization` adapter callback before replay-result disclosure, with denial/UNKNOWN/exception tests. The callback is only an adapter seam; it does not implement I PermissionEpoch/authorization, key registry, audience/scope or D ForgetFence ledgers. The exact PR-head CI run #44180944513 passed, but Owner wiring to real I/D authority ledgers and production integration remain pending.
- **H-ADE-002 — CSubmitOutcome 1.0.1 immutable resolver/equality (P0):** remains open; no real cross-schema fixture/mutation proof or exact C/G acceptance is established.
- **P1:** G has not published an exact consumer successor decision for the separate H Applied Delivery Evidence 1.0.0 family.
- **P0:** G durable Applied persistence, crash/restart, multi-replica idempotency and restore conformance remain specified, not implemented/run.

**Consequences:** no Full Applied, shared wire freeze, Gate release or production activation. H's earlier 11-test CI is not cross-owner or production proof. PR #121's 16-test candidate suite did have an exact-head CI run: #44180944513 completed SUCCESS on `0c878b7b5a14dcc5a417f006818920d96254eaab`. This is candidate conformance evidence only, not cross-owner or production proof.

### 4.2 PR #120 — B domain post-merge reconciliation

PR #120 confirms PR #55 is merged and its research package is present on main, but this does not constitute Fact/Claim approval. Its recorded status remains:

- B0: PARTIAL / NOT PASSED
- B1: IN PROGRESS
- B2: IN PROGRESS / NOT PASSED
- B3: NOT PASSED
- B4: NOT READY
- B5: BLOCKED / NOT PASSED
- B6: INDEPENDENT_REVIEW_PENDING

The review listing recorded 10 COMMENTED and zero APPROVED reviews. B Fact/Claim Option A has no formal Architecture Governance approval; D Claim Identity Option A is a separate candidate. No Claim/Fact/ClaimRevision/ConflictSet schema is frozen.

### 4.3 Integrated priority update

The immediate implementation blockers remain:

1. B Fact/Claim governance decision and exact consumer contract.
2. D/Storage physical transaction write-set, row ownership, serialization and L4 engine/recovery proof.
3. I/D revocation/Forget ordering, closed-world derivative inventory, backup/restore and anti-rollback.
4. C/H/G exact Applied identity mapping, replay-time authorization, durable G Applied persistence and restore.
5. Owner source publication/path canonicalization and bilingual normative parity.

These are not resolved by the merge of #89 or #99–#107.

## 5. Correct interpretation of the ten ARCH-CONVERGENCE artifacts / 十份收敛交付物的正确解释

The ten files under `docs/architecture-convergence/` are already present on main. They are **DRAFT / NON-NORMATIVE proposals** anchored to the historical baseline `e52594f...`. Their historical baseline and PR-state statements must be interpreted as audit-time observations, not current status.

This addendum is the status overlay frozen at `main@6c325804027b88de1014ab3364cdda7e0c023ba6`. PR #121 later advanced main to `ab1fa87d74ca4a632155aa19569533ea560109d5`; the frozen baseline remains an audit-time reference. This addendum does not silently rewrite the historical record or promote the ten documents to normative contracts.

`docs/architecture-convergence/` 下十份文件已经存在于 main，但仍为 **DRAFT / NON-NORMATIVE** 提案，且锚定历史基线 `e52594f...`。其中关于历史基线和 PR 状态的陈述只能理解为当时的审计快照，不能当作当前状态。

本补充文件是冻结于 `main@6c325804027b88de1014ab3364cdda7e0c023ba6` 的状态覆盖层。PR #121 后续将 main 推进至 `ab1fa87d74ca4a632155aa19569533ea560109d5`；本文件的冻结基线仍仅作为审计时参考。本补充文件不会悄悄改写历史记录，也不会把十份文档升级为规范契约。

## 6. Next execution order / 下一步执行顺序

1. **A/source governance:** canonicalize Owner source roots and exact branch/blob provenance; publish a bilingual source index without copying candidate contracts into normative locations.
2. **B:** obtain the formal Fact/Claim governance decision; until then retain candidate-neutral proposition semantics and keep schema freeze blocked.
3. **D + Storage + I:** resolve the exact transaction/write-set and revocation/Forget sequencing contract; keep physical L4 profile open until real recovery evidence exists.
4. **C + G + H + I + D + Storage:** complete H-ADE-002 CSubmitOutcome resolver/equality, G's exact H 1.0.0 consumer decision and durable G Applied persistence; run the #121 16-test candidate suite on an exact Head; wire the replay authorization callback to real I/D authority; then independently re-review exact schema/validator/test/CI pins.
5. **Executable proof:** run the adversarial matrix against a real selected database/profile; distinguish model tests, single-process tests, multi-process races, restore tests and end-to-end Applied proof.
6. **Only then:** issue a new integration decision and implementation authorization request. Do not infer authorization from document publication or PR merge.

## 7. Non-decisions and governance / 未作出的决定与治理边界

- No Owner contract is approved or replaced by this addendum.
- No B Fact/Claim option or schema is approved.
- No SQLite/PostgreSQL L4 engine is selected.
- No Full Applied or shared wire freeze is approved.
- No Forget global terminality or backup-restore anti-rollback claim is accepted.
- No implementation, release, production Gate or production activation is authorized.
- A merged documentation PR records evidence; it does not close the underlying technical finding.



## 8. Subsequent candidate publication / 后续候选发布

After the frozen baseline above, PR #121 merged at `ab1fa87d74ca4a632155aa19569533ea560109d5`. It publishes the H Applied Delivery Evidence 1.0.0 schema, reference validator, 16-test candidate suite, hardening addendum and PR-triggered workflow. The PR body initially stated that tests had not run, but GitHub Actions subsequently recorded run [#44180944513](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44180944513) on the exact PR Head `0c878b7b5a14dcc5a417f006818920d96254eaab`; the run completed successfully, including the conformance test step. This supersedes the stale NOT RUN note in the PR body. The merge remains candidate publication only.

PR #121 advances H-ADE-001 and H-ADE-003 from “no candidate remediation” to “candidate code and negative tests published; exact CI and Owner integration pending.” It does not close the production/Owner findings. H-ADE-002, G consumer acceptance, G durable persistence/restore, production crypto/trust, and C/G/H/I/D/Storage acceptance remain open.

PR #121 合并提交为 `ab1fa87d74ca4a632155aa19569533ea560109d5`，发布了 H Applied Delivery Evidence 1.0.0 Schema、参考 Validator、16 项候选测试、加固补充文件和 PR 触发工作流。PR 正文最初记载测试尚未运行，但 GitHub Actions 随后对精确 PR Head `0c878b7b5a14dcc5a417f006818920d96254eaab` 执行了 [Run #44180944513](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44180944513)，并成功完成，包括 Schema/语义符合性测试步骤。本证据修正 PR 正文中过时的 NOT RUN 说明，但此次合并仍仅为候选发布。

PR #121 将 H-ADE-001 和 H-ADE-003 从“没有候选修复”推进到“候选代码与负向测试已发布；精确 CI 与 Owner 集成待完成”。它不关闭生产/Owner 层发现。H-ADE-002、G 消费者验收、G Durable Persistence/Restore、生产密码学/信任，以及 C/G/H/I/D/Storage 接受仍开放。


## 9. Latest mainline currentness / 最新主线当前性 — 2026-11-18

This section supersedes any interpretation of §3 as describing today's main tree. After PR #124 merged, the current main HEAD is `e8d5e5e374627ac0c472d2bb179e8e940cc6a6de`. The H Applied Delivery Evidence candidate directory `08-bmcp-protocol/` is present on main following PR #121; §3 records only the earlier frozen baseline and must not be read as the current tree state.

PR #124 merged the corrected currentness overlay at `e8d5e5e374627ac0c472d2bb179e8e940cc6a6de`. Draft PR #125 attempted another copy of this addendum from the pre-#124 baseline and contained stale/currentness inconsistencies; it is superseded by this mainline refresh and must not be merged.

No new Owner or governance acceptance is recorded by this refresh. B0-B6 remain as recorded in §4.3. H-ADE-001/H-ADE-003 candidate code remains NOT VERIFIED pending exact-head CI and Owner integration; H-ADE-002, G consumer acceptance, durable G Applied persistence/restore and production trust remain open. No Full Applied, wire freeze, Gate release or production activation is authorized.

PR #124 合并后的当前 main HEAD 为 `e8d5e5e374627ac0c472d2bb179e8e940cc6a6de`。PR #121 发布的 `08-bmcp-protocol/` 现已存在于 main；§3 仅记录较早冻结基线，不应再被理解为当前目录树状态。

PR #124 已合并修正后的当前性补充记录，合并提交为 `e8d5e5e374627ac0c472d2bb179e8e940cc6a6de`。Draft PR #125 从 #124 合并前的旧基线再次复制该补充文件，存在当前性陈述不一致，现由本主线刷新取代，不应合并。

本次刷新没有新增 Owner 或治理验收。B0-B6 维持 §4.3 所记录状态。H-ADE-001/H-ADE-003 候选代码仍待精确 Head CI 与 Owner 集成验证；H-ADE-002、G 消费者验收、G Applied 持久化/恢复和生产信任仍开放。不得据此批准 Full Applied、Wire Freeze、Gate Release 或生产启用。
