# PR-RECOVERY-002 Dependency Graph / 依赖图

**Baseline:** main `e52594f181d2edb77448adcfed64a0fbdffaf3aa`; frozen initial inventory 68 PRs.  
**Status:** provisional; edges are derived from live PR base refs and explicit PR descriptions. Revalidate after every parent integration.

## Confirmed stacked PR edges / 已确认堆叠关系

| Parent | Child | Relationship | Evidence |
|---|---|---|---|
| #31 | #32 | Hard stacked-base dependency | #32 base = branch/head of #31 |
| #32 | #33 | Hard stacked-base dependency | #33 base = branch/head of #32 |
| #33 | #34 | Hard stacked-base dependency | #34 base = branch/head of #33 |
| #34 | #35 | Hard stacked-base dependency | #35 base = branch/head of #34 |
| #44 | #51 | Hard stacked-base dependency | #51 base = branch/head of #44 |
| #51 | #54 | Hard stacked-base dependency | #54 base = branch/head of #51 |
| #42 | #72 | Hard stacked-base dependency | #72 base = branch/head of #42 |
| #69 | #92 | Hard branch dependency | #92 targets #69 branch |

## Owner-branch dependencies / Owner 分支依赖

| PR | Base branch | Relationship | Required action |
|---|---|---|---|
| #94 | `session-c-agent-integration-2026-11-16` | C Owner branch dependency | C Owner review; run schema-only workflow trigger |
| #66 | `session-d-memory-brain-2026-11-16` | D Owner branch dependency | D acceptance; reconcile with I/Storage proposals |
| #68 | `session-i-security-governance-2026-11-16` | I Owner branch dependency | I acceptance; preserve I authority |
| #71 | `session-storage-consistency-forget-atomicity-2026-11-16` | Storage Owner branch dependency | Storage acceptance; resolve Option A ADR contradiction first |

## Cross-Owner contract dependencies / 跨 Owner 合同依赖

- #101 (B canonical transaction) depends on B/D/E/Storage semantic alignment; B Fact/Claim remains ADR-BLOCKED according to its own description and linked review evidence.
- #103 (C Forget/auth/recovery safety) requires C/D/I/Storage and relevant F/G/H acceptance for its stated contract boundaries.
- #104 (D Context Applied/runtime) requires exact C/G/H/I/D/Storage review of the field and evidence joins; no Owner may accept another Owner's authority.
- #102 is an A source-refresh report, not a substitute for the underlying Owner decisions.
- #95's slice-entry proposal is blocked by the Storage Option A source contradiction documented in #102.

## Integration rules / 集成规则

1. Merge/integrate parents before children only after each parent's own gates pass.
2. After each parent merge, refresh main, retarget/update the child, inspect the complete new diff and rerun checks.
3. Do not infer that a branch is safe because GitHub reports `mergeable=true`.
4. Treat dependencies to Owner branches as unresolved until the accountable Owner accepts the exact source revision.
5. Do not merge non-main-target PRs into main by changing their base merely to reduce backlog.

## Unknown edges

All other PR relationships remain **NOT YET VERIFIED** until changed-file overlap, commit ancestry, linked Issues, and semantic contract dependencies are inspected. This graph is not a complete semantic dependency proof.


## Additional verified overlap / supersession candidates
- PR #23 and PR #28 have a **shared-file conflict**: both modify `14-ai-development/README.md`, `ai-development-standard.md`, `iteration-lifecycle.md` and `prompt-and-evidence-template.md`. Treat as a coordinated integration boundary; neither can be independently merged without re-reading the combined result.
- PR #47 and PR #49 are **duplicate/supersession candidates**, not confirmed duplicates: both are X bilingual complexity assessments from 2026-11-17 against the same main SHA and share the same NOT PROVEN conclusion, but differ in detail and structure. Require author designation of canonical artifact.
- PR #48 and PR #50 are **duplicate/supersession candidates** for the R system-wide risk assessment; exact content and source-delta comparison plus explicit author disposition are required before closing either.
- PR #45 and PR #56 have a review relationship (TECH-REALITY-001-A research and its independent-review PR); verify exact source/head pins and review provenance before treating #56 as a dependency-satisfying review.


## A/B review artifact lineage
- #57 and #58 → candidate predecessor/superseded packages → #60 broader A assessment. Explicit A canonicalization needed; do not close without owner decision.
- #59 → B→A currentness review; must reconcile to #60 and latest B/C/H/Storage exact artifacts.
- #61 → B-02 C/H 1.2.15 delta; currentness + independent review pending.
- #62 → historical R/X/F/D/P delta → #65 later B5/current-source refresh. #65 itself now needs current-main and branch-tip re-pin.
- #56 → review report concerning #45; does not count as formal approval until an authorized distinct reviewer submits a review on the target PR.


## B-02 / H 1.2.15 dependency chain
- #67 and #70 are A coordination/review artifacts, not Owner acceptance.
- Required chain: H issuer pre-sign path + 1.2.15 integrated authority-join successor → C exact executable/mapping review + I trust/registration review + D Forget/currentness seam review → Storage immutable successor manifest → A same-bundle exact readback.
- Existing Storage v3.3.2 manifest binds H 1.2.14, not 1.2.15. Do not promote 1.2.15 or reinterpret v3.3.2 until successor manifest and all exact reviews exist.
- #69 C research is a separate research stream; its cross-owner matrix creates review dependencies, not automatic runtime dependency or approval.


## Product adoption research lineage
- #74–#77 are separate PRODUCT-FIRST-001 research sessions, all pinned to historical `b3c666e...`; no product or technology is approved/frozen.
- #76 Cedar PDP spike requires I fail-closed semantics and security review; #77 agent runtime requires H/C boundary review; #75 execution substrate must remain separate from Brain domain truth; #74 memory products remain derivative-only.
- Author-account COMMENTED records are not independent reviews. Research adoption cannot satisfy implementation/architecture gates by itself.


## Architecture breakthrough research dependencies
- #80 formal Forget verification depends on exact D ForgetFence, Storage visibility/restore, I authorization and publication/derivative contracts; proof scope must include concurrency, crash, retry and restore.
- #81 Memory OS alternatives must map current Retrieval/Activation/Context/Budget/Eviction owners and preserve their authority; no architecture/module consolidation without Owner decisions.
- #82 Memory IR/Compiler depends on B Fact/Claim semantics and C consumer mapping; B remains ADR-BLOCKED, so no canonical identity decision can be inferred.


## Architecture breakthrough coordination
- #83 is coordination only; does not prove the four research streams completed.
- #84 Forget TLA+ model must be checked with TLC and reconciled to exact current D/Storage/I contracts; coordinate with #80 rather than duplicate proof work.
- #85 IR prototype depends on B Fact/Claim semantics and C/E consumer review; shadow-only candidate until B decision.
- #86 resource-manager candidate depends on F/G Owner review and workload evidence; no authority consolidation.
- #87 overlaps #67/#70 B-02 coordination reports; merge evidence into one canonical report only after A/source Owner confirmation and exact branch-tip refresh.


## Live owner branch integrity recheck — 2026-11-18
- The earlier H/C mass-deletion event is no longer present in current refs. H `6608cde...` tree: 248 entries; C `a69007a...` tree: 147 entries; recursive results are not truncated.
- H compare from last reviewed complete head `0d363244...`: 7 ahead / 0 behind, 8 added / 0 removed. C compare from last reviewed complete head `71047cdb...`: diverged 63 ahead / 167 behind, 65 added / 3 modified / 0 removed.
- Current main remains `e52594f...`. H/C compare against main contains additions only (H 182 added / 0 removed; C 17 added / 0 removed).
- Treat #90/#91 as historical incident records; current tree restoration does not itself establish Owner incident acknowledgment, semantic source correctness, or acceptance. Refresh exact H/C blobs before using prior conclusions.


## Remaining historical integration lineage
- #1 is the G Owner package; #44→#51→#54 is the architecture-consolidation stack.
- #42 is a ChatGPT-native execution proposal with explicit channel-governance tension against #23/#31/#36 and Issue #41; requires Session 0 resolution.
- #45/#56/#73 are TECH-REALITY-001-A research/review/remediation lineage.
- #55/#65/#102 are B domain research, B5 audit and current-source reconciliation lineage; B5 remains blocked.
- #63/#64 are historical A review artifacts; do not treat as current G1/B-02 source-of-truth.
- #94 is a C Owner branch workflow fix, not a mainline PR; #95 is a non-authorizing readiness proposal.


## Live dependency refresh — 2026-11-18 (live refresh)

**Live collection source:** GitHub REST `GET /pulls?state=open&per_page=100`, fetched in this refresh.
- Open PRs: **74** (72 Draft, 2 Ready: #110 and #111).
- Target distribution: **62 target main / 12 target non-main**.
- Current main/base SHA observed from the live PR collection: `4bee3e886cc0dec4a8d03817acd180ba979f8ceb`.
- PR #110 current head: `5f42acb1391a06703f9aa1a7b615f4dd62d5cbea`; PR #111 current head: `369ba052e747a9623aa0150eda6398fad8255b6e`. Both target main at the current main SHA. These are Ready-for-review, not approved or merge-eligible.
- This refresh confirms the existing eight stacked-base edges below by exact live `base.ref` matching another open PR's `head.ref`; it does not prove semantic acceptance or merge safety.

### Exact live stacked-base edges / 当前精确堆叠边

| Parent | Child | Live child base ref | Evidence class |
|---|---|---|---|
| #31 | #32 | `infra/ai-run-003-runtime-plan` | HARD — child base ref equals #31 head branch |
| #32 | #33 | `infra/ai-run-003-adr-run-002` | HARD — child base ref equals #32 head branch |
| #33 | #34 | `infra/ai-run-003-adr-run-003` | HARD — child base ref equals #33 head branch |
| #34 | #35 | `infra/ai-run-003-adr-run-004-005` | HARD — child base ref equals #34 head branch |
| #44 | #51 | `review/arch-consol-001-system-wide-2026-11-17` | HARD — child base ref equals #44 head branch |
| #51 | #54 | `review/arch-consol-002-protocol-alignment-2026-11-17` | HARD — child base ref equals #51 head branch |
| #42 | #72 | `design/chatgpt-native-execution-model` | HARD — child base ref equals #42 head branch |
| #69 | #92 | `research/tech-reality-001-c` | HARD — child base ref equals #69 head branch |

### Live non-main Owner/review branch targets / 非主干 Owner 分支目标

These are **branch-target dependencies**, not PR-parent edges. They must not be retargeted to main merely to clear the queue.

| PR | Live base branch | Required gate |
|---|---|---|
| #94 | `session-c-agent-integration-2026-11-16` | C Owner review; schema-only workflow path-filter test |
| #66 | `session-d-memory-brain-2026-11-16` | D Owner acceptance and D/I/Storage contract reconciliation |
| #68 | `session-i-security-governance-2026-11-16` | I Owner acceptance; preserve I security authority |
| #71 | `session-storage-consistency-forget-atomicity-2026-11-16` | Storage Owner acceptance; resolve source ADR contradiction |
| #92 | `research/tech-reality-001-c` | Parent #69 exact research branch; validate current C research head |
| #72 | `design/chatgpt-native-execution-model` | Parent #42 exact design branch; resolve governance/execution boundary first |
| #51 | `review/arch-consol-001-system-wide-2026-11-17` | Parent #44 exact review branch |
| #54 | `review/arch-consol-002-protocol-alignment-2026-11-17` | Parent #51 exact review branch |
| #32–#35 | AI-RUN-003 predecessor branches | Preserve parent-first integration and revalidate every child diff after each parent |

### Refresh interpretation and remaining audit work

1. The 8 hard stacked edges above are mechanically confirmed from live PR metadata. They are not a claim that every parent is accepted; all five AI-RUN-003 PRs and the architecture-consolidation stack remain independently gated.
2. The #66/#68/#71 trio is a **cross-Owner agreement set**, not a linear stack. D, I and Storage must accept the same exact successor contract/blob set before integration.
3. Existing known shared-file conflict #23/#28 remains a coordinated integration boundary; both diffs must be reviewed together before either can be accepted.
4. Existing duplicate/supersession candidates remain unresolved: #47/#49, #48/#50, and #57/#58 relative to #60. Similar titles or conclusions are not sufficient to close a PR; require exact diff comparison and explicit canonical-owner disposition.
5. #45/#56 review lineage remains an evidence/provenance relationship, not a proven PR dependency or formal approval. A review artifact is not a submitted independent review on the target PR.
6. Semantic contract dependencies listed above remain confidence-tagged hypotheses until exact changed-file diffs, linked Issues, current Owner source Blobs and required reviewer decisions are reconciled.
7. The historical inventory CSV remains a frozen/rolling record with metadata-first rows; this live snapshot does not retroactively certify every row. Full 74-PR changed-file overlap scan, exact-head CI/review reconciliation, and semantic dependency verification remain outstanding.
8. No PR was merged, closed, retargeted, or approved by this refresh.


## Non-main target correction — 2026-11-18

**Policy clarification:** a non-main base branch is not itself a merge blocker. PRs should normally merge into their declared target branch when that branch is the intended integration boundary and the target Owner's required gates are satisfied. Do not retarget to `main` merely to reduce backlog.

Live recheck after the previous inventory refresh:
- PR #94 is now **CLOSED / MERGED** into `session-c-agent-integration-2026-11-16`; it is no longer an open backlog item. Its merge destination was the C Owner branch, not main.
- The remaining non-main-target open PRs are #92, #72, #71, #68, #66, #54, #51, #35, #34, #33 and #32.
- Each of those PRs currently reports GitHub `mergeable_state=clean` and `mergeable=true` at the time of this check. This is a technical conflict signal only; it does not establish review approval, checks, Owner acceptance, or policy compliance.
- All 11 remaining non-main PRs are Draft and have no requested reviewers in the live PR metadata. Treat them as not yet merge-authorized until the relevant independent review and Owner acceptance are recorded.

### Correct non-main integration treatment
- #32–#35: eligible to merge **into their immediate parent branches** only after each child is independently reviewed and its parent dependency is already present; process in order, not in parallel.
- #51 and #54: eligible to merge into their predecessor review branches after exact-head review; preserve the #44→#51→#54 sequence and do not retarget to main.
- #72: merge destination remains the #42 design branch; do not merge before #42's governance boundary and exact-head blockers are resolved.
- #92: merge destination remains the #69 research branch; it does not constitute C Owner approval.
- #66/#68/#71: their D/I/Storage Owner branches are valid destinations. Merge into each respective Owner branch only after that Owner accepts the exact proposal and the cross-Owner contract agreement is reconciled. A clean merge state alone is insufficient.
- #94: already merged to the C Owner branch; remove it from open backlog and verify post-merge workflow evidence separately.

**Revised classification:** non-main target = intended integration destination, not a blocker by itself. Actual blockers are missing Owner decision, independent review, checks, unresolved parent dependency, or contract conflict.


## Non-main branch integration execution — verified 2026-11-18

**Execution result: all 12 non-main-target PRs are now merged into their declared target branches.** No PR in this set was retargeted to main. Verification used GitHub PR metadata after the merge operations; each item reports `state=closed` and `merged=true`.

| PR | Target branch | Merge commit |
|---|---|---|
| #94 | `session-c-agent-integration-2026-11-16` | `62c3e799b36c56bd82972a4d7d561f246598deaf` |
| #92 | `research/tech-reality-001-c` | `69783fea3507ac9913ab4eae75441e4232fa017d` |
| #72 | `design/chatgpt-native-execution-model` | `890fba6185c655d9e6e99ca2a7e9cf1e9b6e62e7` |
| #71 | `session-storage-consistency-forget-atomicity-2026-11-16` | `f6887cc9ea5bfa5293c1bc47e9f10e582830cba3` |
| #68 | `session-i-security-governance-2026-11-16` | `ea949896f891f0a08ef5fe9358edadc8a49e546f` |
| #66 | `session-d-memory-brain-2026-11-16` | `7e6d0b133dae88f442665e7b05a54060e047647e` |
| #54 | `review/arch-consol-002-protocol-alignment-2026-11-17` | `044f84f204463ac5a974b0d40129e76fe5ce0dc9` |
| #51 | `review/arch-consol-001-system-wide-2026-11-17` | `f117bbdcdd3d25937e78abb4c619f654584e8492` |
| #35 | `infra/ai-run-003-adr-run-004-005` | `44626eade4862ea2c903c77064745da8021eb82f` |
| #34 | `infra/ai-run-003-adr-run-003` | `b2b4fe1a20750d5cad66b5485f920edd63b57f6e` |
| #33 | `infra/ai-run-003-adr-run-002` | `362e3a55959aa4c3ce4e751cae0bbeaba0db811e` |
| #32 | `infra/ai-run-003-runtime-plan` | `4d2145b778d12a474a73313e722ec07ded83c467` |

The four AI-RUN-003 stacked PRs were integrated leaf-to-root (#35, #34, #33, #32); the architecture-consolidation stack was integrated leaf-to-root (#54, #51). GitHub initially rejected stale expected-head attempts for #34/#32/#51 after child merges updated their branch refs; the exact new heads were fetched and those merges then succeeded. All final PR states were re-read and confirmed.

**Important:** these merges integrate proposal/research content into the designated non-main branches. They do not imply that proposals became normative, that Owner approval was granted, or that any content was merged to `main`. The main branch remained at `4bee3e886cc0dec4a8d03817acd180ba979f8ceb` in the post-merge verification.
