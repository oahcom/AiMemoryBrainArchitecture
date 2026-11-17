# TECH-REALITY-001-A — Independent Technology Architecture Review
# 独立技术架构审查报告

- Review ID: `TECH-REALITY-001-A-IR-001`
- Target PR: [#45](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/45)
- Target branch: `ai/TECH-REALITY-001-A/principal-technology-research`
- Reviewed PR HEAD: `6c7c5919c1b50f38c4d24be679a3885ee3c15b97`
- PR base recorded: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Review branch: `review/TECH-REALITY-001-A-independent-review-2026-11-17`
- Review date: 2026-11-17
- Reviewer mode: separate ChatGPT session/context; not the producer session
- Independence limitation: session/context separation only; this is not a different model, provider, organization, or human reviewer.
- Overall verdict: **REVISE**
- Feasibility verdict: **NOT YET PROVEN**
- Architecture freeze recommendation: **NOT READY**

---

## 1. Executive disposition / 总体裁决

**REVISE — the research package is useful and generally cautious, but it is not current enough to support an architecture-level technology disposition.**

The package correctly avoids claiming that a candidate stack, prototype, benchmark, production deployment, or ADR has been approved. Its central **NOT YET PROVEN** conclusion is appropriate. Its strongest technical principles are also sound: preserve canonical authority, keep retrieval indexes as projections, distinguish workflow durability from domain transactions, keep Forget and Applied semantics project-owned, and avoid premature service proliferation.

However, independent re-fetch found material freshness and evidence issues:

1. The research baseline is historical. Current `main` is 26 commits ahead of the pinned baseline. The research PR still targets the old base SHA and GitHub currently reports it as not mergeable.
2. The Owner branch snapshot in the research is stale. Compared with the recorded branch heads in `owner-technology-review-synthesis.md`, the live branches are ahead by B +1, C +28, D +24, E +1, F +1, G +3, H +69, I +26 and Storage +21 commits. The live D/E/I/Storage Phase 3.7 proposals materially refine the publication and recovery order.
3. The Restate Server license row records API metadata as `NOASSERTION`, but the exact repository `LICENSE` file is BSL 1.1 and contains a restriction on a Public Restate Platform Service. This is a material adoption constraint missing from the recommendation.
4. The Owner dependency register still uses an over-broad “D/Storage serialization topology remains ADR-BLOCKED” description without distinguishing the logical v1 serialization profile selected by the Storage ADR addendum from the still-open physical realization and JF-10 integration.
5. The handoff has malformed paths for required files 13 and 14 (extra closing parentheses), and the README repeats section number 9.

These findings do not invalidate the package's cautious overall conclusion. They do prevent acceptance of its claim to be a current system-wide technology reality snapshot.

**REVISE — 研究包有价值，且整体保持谨慎，但当前版本不足以支持系统架构层面的技术结论。**

研究正确地避免声称候选技术栈、原型、基准测试、生产部署或 ADR 已获批准；**NOT YET PROVEN** 总结论合理。保留 Canonical Authority、将检索索引视为投影、区分 Workflow Durability 与领域事务、由项目自身承担 Forget/Applied 语义、避免过早拆分服务等原则也成立。

但独立重新读取发现了实质性的当前性和证据问题：

1. 研究基线已是历史基线。当前 `main` 比固定基线领先 26 个提交；研究 PR 仍以旧 SHA 为 Base，GitHub 当前报告其不可合并。
2. 研究中的 Owner 分支快照已过期。与 `owner-technology-review-synthesis.md` 记录的分支 HEAD 相比，当前分支分别领先：B +1、C +28、D +24、E +1、F +1、G +3、H +69、I +26、Storage +21。当前 D/E/I/Storage Phase 3.7 提案已经实质细化 Publication/Recovery 顺序。
3. Restate Server 许可证行只记录 API 元数据 `NOASSERTION`，但精确仓库 `LICENSE` 实际为 BSL 1.1，并限制 Public Restate Platform Service。这是技术栈建议遗漏的重大采用条件。
4. Owner Dependency Register 仍笼统写着“D/Storage serialization topology remains ADR-BLOCKED”，没有区分 Storage ADR 补充条款已选择的逻辑 v1 序列化档案，与仍开放的物理实现和 JF-10 集成。
5. Handoff 第 13、14 项路径多出右括号；README 还重复使用第 9 节编号。

这些发现不推翻研究包谨慎的总体结论，但阻止将当前版本接受为“最新系统技术现实快照”。

## 2. Exact review baseline / 精确审查基线

### 2.1 PR state

- PR #45: open, Draft, not merged.
- Head: `6c7c5919c1b50f38c4d24be679a3885ee3c15b97`.
- Base SHA: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`.
- Changed files: 14.
- Submitted GitHub reviews: 0.
- Inline review threads: 0.
- The current PR metadata reports `mergeable=false`.

### 2.2 Current main drift

A direct compare of the pinned baseline against `main` reports:

- `main` is **26 commits ahead**, 0 behind, relative to `b372b62c640a2b656e54b6db62a4ee67d7d8c001`.

The historical baseline document is not itself wrong for recording what was observed on 2026-11-17. The problem is that the package and PR are still presented as a current research snapshot without a current-main impact analysis. Preserve the historical baseline, but add a separate current-main delta review and retarget/rebase the research PR only after its conclusions are reconciled.

### 2.3 Owner branch drift

Direct compare from the Owner HEADs recorded in the research synthesis to the current named Owner branches reports:

| Owner | Commits ahead of recorded snapshot | Review consequence |
|---|---:|---|
| B | 1 | Re-check Fact/Claim and typed identity assumptions |
| C | 28 | Re-check final request, provider outcome and adapter boundary |
| D | 24 | Re-check EventRef admission, publication participant and Forget ordering |
| E | 1 | Re-check queue/lease/private-stage and publication ordering |
| F | 1 | Re-check retrieval projection and current filtering requirements |
| G | 3 | Re-check Context/Delivery/Applied dependencies |
| H | 69 | Re-check exact wire schemas, RecoveryJoin/RecoveryCutoff and current CI status |
| I | 26 | Re-check revocation, current authorization and publication receipt semantics |
| Storage | 21 | Re-check logical serialization profile, Phase 3.7 physical proposal and JF-10 gates |

These are commit-drift measurements, not a claim that every intervening commit changes the technology recommendation. They prove that the prior snapshot cannot be treated as current without reading the changed artifacts.

## 3. Findings / 审查发现

### P1-01 — Current-main and Owner-source freshness is insufficient

**Affected research files**
- `README.md` Blob `e69498b4945213e797e9c7ba1ab5a4a3080c2b6a`, lines 82–85, 153–171.
- `owner-technology-review-synthesis.md` Blob `1a683a265d8fba0cbfbdf0bb3bdd3e25a12a767a`, lines 7–21, 166–176.
- `research-evidence-register.md` Blob `f314ccbe88a294aeebdfc43ee57942ec623b84ee`, lines 89–104, 208–221.
- `independent-review-handoff.md` Blob `9a65b3648f349453b0abbd81fba6f67b2dfeccb6`, lines 38–54.

**Independent evidence**
- Current `main` is 26 commits ahead of the stated baseline.
- Current Owner branches have advanced by the counts in §2.3.
- Issue #25 now records corrected current D/E/I/Storage source pins:
  - D Blob `4c01713bc8793a8926ef18b625b72d132572173d`
  - E Blob `4fb9e58511941f59b4d777336f8f85ad88ecccf1`
  - I Blob `e3b1b5d99eb36ac0b395854d8c19287d2b64b752`
  - Storage Blob `2ab899ee37a18ae6c8f2f64dbb82ad6499842060`
- Issue #3 remains open and explicitly says Applied Contract Frozen = NO, Test Executed/Passed = NO/NO, Implementation Verified = NO.

**Impact**
The technology matrix, topology comparison, recommendations and owner dependency map are not yet reconciled against the current source authority. This is a freshness blocker, not proof that the candidate conclusions are false.

**Required correction**
1. Preserve the original historical baseline and its exact pins.
2. Add a current-main delta section against the latest main commit.
3. Re-read the current B–I and Storage artifacts that changed, recording exact branch, commit, path and Blob SHA.
4. Recompute the dependency register and technology impact; mark unchanged findings as re-confirmed only when their controlling sources were re-read.
5. Keep all stale TAR reports as historical/delegated design inputs, not current approval.

**Disposition: OPEN / blocks acceptance.**

### P1-02 — Storage Phase 3.7 physical publication protocol is not integrated into the research package

**Affected research files**
- `technology-capability-matrix.md` Blob `a03981d6dc5e01cd4f5830292f4270403b9cc6fd`, lines 3–10 and 60–90 (Storage update and critical gaps).
- `technology-recommendation.md` Blob `cc2269dfd5d95fe85089287e1be9579bddce1ef2`, lines 30–35, 113–116, 158–160, 213.
- `owner-technology-review-synthesis.md` Blob `1a683a265d8fba0cbfbdf0bb3bdd3e25a12a767a`, lines 166–202.
- `owner-dependency-register.md` Blob `58fd1ecb1ef318de92a2ad9fa3ab9147ec2999a5`, lines 39–45 and 83–95.

**Current source readback**
- D Phase 3.7 Blob `4c01713bc8793a8926ef18b625b72d132572173d`: §9–11, especially lines 68–128. D requires a shared serialization domain for producer registration, fence, dependency, publication and terminalization. The crash-window correction requires a durable hidden Storage participant **before** D admits its PublicationParticipantRef.
- E Phase 3.7 Blob `4fb9e58511941f59b4d777336f8f85ad88ecccf1`: §11, lines 204–218. The final corrected sequence is Storage hidden participant → D PublicationParticipantRef → I single-use receipt → Storage final visibility commit → D/I close after the same authoritative Storage outcome. E §11 explicitly supersedes its earlier §10 ordering.
- I Phase 3.7 Blob `e3b1b5d99eb36ac0b395854d8c19287d2b64b752`: §8–9, lines 28–91. I requires the exact durable StorageVisibilityParticipantRef before consuming its single-use CommitAuthorizationReceipt; UNKNOWN/IN_DOUBT keeps the authorization participant and affected revocation unresolved.
- Storage Phase 3.7 Blob `2ab899ee37a18ae6c8f2f64dbb82ad6499842060`: status line 4 says **PROPOSED PHYSICAL REALIZATION; not selected, implemented or conformance-verified**. §2 begins at line 21; §9/§11–13 define the D/I barrier composition, exact participant identity and crash-window correction; lines 257–277 preserve Storage-first ordering and require exact-owner re-review.

**Impact**
The research currently highlights Storage v3.2.6 successor bundle and PostgreSQL 18.7 capability dossier. Those are relevant but do not replace the latest D/E/I/Storage Phase 3.7 cross-owner publication proposal. The package must not imply that the logical v1 transaction-domain profile or the JF-10 prepared-XID engine tests prove this later producer/derivative visibility protocol.

**Required correction**
- Add the four current Phase 3.7 exact pins to the Owner synthesis and evidence register.
- Explicitly distinguish: (a) Storage ADR logical v1 serialization profile, (b) proposed Phase 3.7 physical operation order, (c) bounded PostgreSQL engine capability tests, and (d) absent Brain application conformance.
- Keep the Phase 3.7 proposal status OPEN / NOT SELECTED / NOT IMPLEMENTED / NOT CONFORMANCE-VERIFIED until exact Owner approvals and deterministic race/crash/failover/restore tests exist.
- Reconcile the required order consistently across the technology matrix, recommendation and dependency register.

**Disposition: OPEN / blocks acceptance.**

### P1-03 — Restate Server license is materially under-reported

**Affected research files**
- `research-evidence-register.md` Blob `f314ccbe88a294aeebdfc43ee57942ec623b84ee`, lines 17–18 and 130–131.
- `mature-project-research.md` Blob `115f47af30183235f9bfbd096ff02e860c230204`, §3.3 and §11.1 addendum.
- `technology-recommendation.md` Blob `cc2269dfd5d95fe85089287e1be9579bddce1ef2`, Stack 2/3 workflow rows.

**Independent source**
- Restate repository `restatedev/restate`, pinned source commit `f0cfcae2b935cfe6f80de9a72a180f976da1c66c`, root `LICENSE` Blob `82a68338267bbde13cf9b0a04682778284ef3f35`.
- The file identifies **Business Source License 1.1**, states it is not an Open Source license, and includes an Additional Use Grant that prohibits a “Public Restate Platform Service” as defined in the license. It changes to Apache-2.0 four years after release, subject to the license terms.

**Impact**
Recording the GitHub API's `NOASSERTION` field is not a substitute for inspecting the canonical license file. The candidate recommendation omits a licensing boundary that may determine whether Restate is suitable for a future third-party managed service.

**Required correction**
- Record Restate Server as BSL 1.1 (not open source) and explain the additional-use restriction and change-license schedule.
- Keep Restate Rust SDK license separate from Restate Server license; the SDK's MIT license does not change the server's license.
- Add a product/business-model trigger: if the Brain is ever offered as a public managed platform to third-party developers, obtain legal review before selecting Restate Server.
- Do not collapse API metadata `NOASSERTION` into “license unknown” after the canonical LICENSE has been inspected.

**Disposition: OPEN / blocks acceptance of the Restate option comparison.**

### P2-01 — Storage serialization status wording is too broad

**Affected file**
- `owner-dependency-register.md` Blob `58fd1ecb1ef318de92a2ad9fa3ab9147ec2999a5`, lines 39–45 and 83–95.

The statement “D/Storage serialization topology remains ADR-BLOCKED” is not precise enough. The research's own README and topology comparison say the Storage ADR addendum selected one logical Serializable Transaction Domain per Canonical Memory authority as the v1 serialization architecture profile. The live Phase 3.7 physical realization remains a proposal, not selected or proven.

**Required correction**
Replace the broad label with two separate status fields:
- Logical v1 serialization architecture profile: selected by Storage ADR addendum (record exact current ADR Blob).
- Physical transaction/participant realization, D/I bridge and JF-10 runtime: OPEN / NOT PROVEN / NOT AUTHORIZED as applicable.

**Disposition: OPEN / terminology correction.**

### P2-02 — Handoff required-file paths are malformed

**Affected file**
- `independent-review-handoff.md` Blob `9a65b3648f349453b0abbd81fba6f67b2dfeccb6`, required-file list around lines 20–36.

The entries for items 13 and 14 contain an extra closing parenthesis in the path:
- `owner-technology-review-synthesis.md)`
- `independent-review-handoff.md)`

The actual filenames in the PR are valid and were independently read. Correct the handoff list so a future reviewer can copy/paste the exact paths without manual interpretation.

**Disposition: OPEN / clerical but review-process relevant.**

### P2-03 — Document section numbering and bilingual parity need a final normalization pass

**Affected files**
- `README.md` Blob `e69498b4945213e797e9c7ba1ab5a4a3080c2b6a`, lines 146–153: section number 9 is reused for two separate sections.
- `mature-project-research.md` Blob `115f47af30183235f9bfbd096ff02e860c230204`: duplicate section number 9 and duplicate section number 11 appear in the heading sequence.
- `research-evidence-register.md` Blob `f314ccbe88a294aeebdfc43ee57942ec623b84ee`: late Storage refresh is numbered as another section 7 after section 8.

All 14 files contain bilingual material, and the sampled critical English/Chinese clauses generally preserve the same authority and fail-closed intent. However, this review does **not** certify line-by-line semantic parity across every paragraph. The duplicated numbering and append-only updates make omissions and precedence harder to detect.

**Required correction**
- Normalize heading numbering.
- Produce a bilingual parity checklist for every normative table, status, exception, ordering rule and non-claim.
- Specifically verify that the E §11 crash-window correction is mirrored in Chinese and is clearly marked as superseding §10. The current E source does so; preserve this explicit precedence.
- Do not mark bilingual parity fully verified until the checklist is complete.

**Disposition: OPEN / documentation quality.**

## 4. File-by-file disposition / 逐文件审查登记

The following are the exact research-branch Blob SHAs independently fetched at PR HEAD `6c7c5919c1b50f38c4d24be679a3885ee3c15b97`.

| # | File | Blob SHA | Review result |
|---:|---|---|---|
| 1 | `README.md` | `e69498b4945213e797e9c7ba1ab5a4a3080c2b6a` | REVISE — stale-currentness framing; duplicate §9; update Storage/Owner snapshot |
| 2 | `baseline/architecture-baseline.md` | `ad62c4568bf641b02872c805dca1aeb9bd5a8202` | ACCEPT AS HISTORICAL — retain exact captured baseline; add current-main delta |
| 3 | `mature-project-research.md` | `115f47af30183235f9bfbd096ff02e860c230204` | REVISE — update current Owner mapping; normalize numbering; incorporate license finding |
| 4 | `technology-capability-matrix.md` | `a03981d6dc5e01cd4f5830292f4270403b9cc6fd` | REVISE — reconcile current Phase 3.7 operation order and status |
| 5 | `deployment-topology-comparison.md` | `b5269966b5a073371a50ea675aee87c23306835d` | ACCEPT WITH CONDITIONS — scores are explicitly estimates; SQLite/JF-10 boundary must remain explicit |
| 6 | `architecture-complexity-audit.md` | `ab49c7003b00279999d8a986bb54be7433c689ac` | ACCEPT WITH FINDINGS — authority/receipt taxonomy is useful; re-check current Owner contracts |
| 7 | `rust-ecosystem-assessment.md` | `4e1601975d9bf3a30fc779f00a6130294bd9ef61` | ACCEPT WITH CONDITIONS — candidate-only caveats are sound; full advisory/license/platform audits remain NOT RUN |
| 8 | `workload-model.md` | `726ed06a80d52bcb0a1e12bff82d6f20e73469ca` | ACCEPT WITH CONDITIONS — values are clearly assumptions, not requirements/SLOs |
| 9 | `technology-recommendation.md` | `cc2269dfd5d95fe85089287e1be9579bddce1ef2` | REVISE — refresh owner constraints and Restate license boundary |
| 10 | `owner-dependency-register.md` | `58fd1ecb1ef318de92a2ad9fa3ab9147ec2999a5` | REVISE — logical vs physical Storage status; refresh current exact pins |
| 11 | `research-evidence-register.md` | `f314ccbe88a294aeebdfc43ee57942ec623b84ee` | REVISE — Restate server license; update Storage Phase 3.7 pins/currentness |
| 12 | `open-questions.md` | `b83dbee047c84f0c80b19fc3ec5350ec4fbc3f90` | ACCEPT WITH CONDITIONS — blockers are appropriately preserved; refresh references/status against live sources |
| 13 | `owner-technology-review-synthesis.md` | `1a683a265d8fba0cbfbdf0bb3bdd3e25a12a767a` | REVISE — branch-head snapshot stale; refresh B–I/Storage and Phase 3.7 |
| 14 | `independent-review-handoff.md` | `9a65b3648f349453b0abbd81fba6f67b2dfeccb6` | REVISE — malformed file paths; clarify evidence freshness and required current source pins |

## 5. Technical claim checks / 技术主张核验

### Supported within stated limits

- SQLite WAL: one writer; same-host shared-memory constraint; not a multi-host transaction substrate.
- Temporal: durable Event History and replay; workflow determinism and external Activity boundaries remain relevant.
- NATS JetStream: durable delivery/replay and ACK semantics do not remove application-level idempotency.
- Qdrant: filtered ANN/HNSW is a retrieval mechanism, not the Brain authorization boundary or canonical authority.
- Cedar: embedded policy evaluation does not own Principal issuance, revocation propagation, or Brain-specific audit.
- OpenTelemetry Rust: per-signal stability differs; do not describe all signals as equally stable.
- PostgreSQL prepared-XID CI: bounded engine capability evidence only; not Brain D/I/COC integration or production deployment.
- The recommendation to begin with structured/lexical retrieval and make vector infrastructure conditional on labeled evaluation is appropriately conservative.

### Corrections / limits

- Restate Server: BSL 1.1, not merely `NOASSERTION`; see P1-03.
- Current Storage Phase 3.7: the latest cross-owner proposal requires Storage hidden participant first, then D publication participant, then I receipt consumption, then final Storage visibility commit. It is not implemented or accepted yet.
- Profile S + SQLite: keep it as a narrow local prototype hypothesis only. It is not evidence that SQLite alone satisfies the independent I sequencer / JF-10 prepared-participant recovery profile.
- Rust ecosystem: the table correctly distinguishes SDK, FFI and service boundaries, but it is not a reproducible lockfile or full dependency audit. The report explicitly says `cargo-audit`, `cargo-deny`, SBOM, cross-platform CI and benchmarks were not run.

## 6. Bilingual semantic parity / 双语语义一致性

**Result: PARTIAL PASS — not fully certified.**

- All 14 files include English and Chinese content.
- Critical authority boundaries sampled in D, E, I and Storage Phase 3.7 preserve the same essential ownership and fail-closed behavior.
- E §11 explicitly supersedes the earlier D-first ordering in §10; the Chinese section also says it supersedes §10. This is a valid precedence correction, not an unresolved contradiction.
- Full paragraph-by-paragraph equivalence across all 14 files was not established in this pass. Repeated section numbering and appended updates create a material risk of drift.

No claim of full bilingual semantic equivalence should be made until a structured parity checklist is completed and independently read back.

## 7. CI, prototype and proof boundary / CI 与实现证明边界

The research's repeated non-claims are appropriate. This review found no basis to upgrade any of the following:
- Brain prototype: NOT RUN.
- Brain workload benchmark: NOT RUN.
- End-to-end D/E/Storage publication/Forget conformance: NOT PROVEN.
- C/G/H Applied end-to-end conformance: NOT PROVEN; Issue #3 remains open.
- Full JF-10 runtime / COC bridge: OPEN / NOT PROVEN.
- Production deployment and activation: NOT AUTHORIZED.
- Full security audit, dependency advisory scan and cross-platform build matrix: NOT RUN.
- Independent Owner approval of all current branches: NOT ESTABLISHED.

Bounded CI capability evidence must remain scoped to the exact source commit, engine version, fixture and test run. It must not be promoted to Brain integration or production evidence.

## 8. Required remediation sequence / 必须整改顺序

1. **P1 — Refresh currentness:** update the current-main delta and all changed Owner pins; do not merely update the date.
2. **P1 — Reconcile Storage Phase 3.7:** bind current D/E/I/Storage exact artifacts and the corrected Storage-first publication order; preserve proposal/open status.
3. **P1 — Correct Restate license:** inspect and cite canonical server LICENSE separately from SDK license; update stack comparisons.
4. **P2 — Correct Storage status wording:** distinguish logical serialization profile from physical implementation/JF-10 proof.
5. **P2 — Fix handoff paths and section numbering.**
6. **P2 — Complete bilingual parity checklist.**
7. Re-run independent review against the corrected exact PR HEAD. Do not treat this report as automatic acceptance of a future revision.

## 9. Final decision / 最终决定

**Overall: REVISE.**  
**Feasibility: NOT YET PROVEN.**  
**Architecture freeze: NOT READY.**

The package is a useful research foundation, not an accepted current technology baseline. The three P1 findings must be closed before acceptance. No Owner-owned semantics are decided by this review; B Fact/Claim, C/G/H Applied, I security/governance and Storage physical topology remain with their respective authorities.

**总体：REVISE（需修订）。**  
**工程可行性：NOT YET PROVEN（尚未证明）。**  
**架构冻结：NOT READY（不具备条件）。**

该研究包可以作为后续工作的研究基础，但尚不能作为已接受的当前技术基线。三个 P1 必须在接受前关闭。本审查不代替任何 Owner 决定；B Fact/Claim、C/G/H Applied、I Security/Governance 和 Storage 物理拓扑仍由各自权威负责。
