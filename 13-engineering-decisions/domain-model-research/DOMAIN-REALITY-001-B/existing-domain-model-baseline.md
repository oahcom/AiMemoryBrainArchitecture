# DOMAIN-REALITY-001-B — Existing Domain Model Baseline
# DOMAIN-REALITY-001-B — 现有领域模型基线审计

- Report ID: DOMAIN-REALITY-001-B
- Status: PARTIAL VERIFIED BASELINE — NOT A COMPLETE B0 PASS
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Default branch: `main`
- Baseline HEAD: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Research branch: `research/domain-reality-001-b`
- Research branch base: the exact baseline HEAD above
- Access date: 2026-11-17

## 1. Executive finding / 执行摘要

The repository has a substantial pre-existing domain model. The root `02-domain-model/` specifications define Event, Memory, Memory Version, Claim, Entity, Relation, Evidence, Provenance, Memory Source, Memory Context, Context Entry, Agent Scope and Environment Scope. The model explicitly separates epistemic status from lifecycle state, Scope from Permission, and domain semantics from storage/wire/algorithm choices.

仓库已经存在较完整的领域模型。`02-domain-model/` 源规范定义了 Event、Memory、Memory Version、Claim、Entity、Relation、Evidence、Provenance、Memory Source、Memory Context、Context Entry、Agent Scope 和 Environment Scope。模型明确区分认知状态与生命周期状态、Scope 与 Permission，以及领域语义与存储/协议/算法实现选择。

However, the source set is not internally ready for a new freeze. The Fact/Claim relationship is explicitly identified as ADR-BLOCKED in the bilingual guide and is still called DECIDED in the root overview, while the guide says older wording must not freeze downstream schemas. Claim identity across Memory versions, uncertain-time representation, scope algebra, relation vocabulary governance, provenance graph cycles, and several lifecycle transitions remain OPEN/CANDIDATE/TO_VALIDATE. A's current architecture assessment also lists the B Fact/Claim ADR as a blocker.

但是，现有来源集尚不适合重新冻结。双语指南明确将 Fact/Claim 关系标记为 ADR-BLOCKED，而根目录总览仍将其表述为 DECIDED；指南同时要求不得使用旧表述冻结下游 Schema。Claim 跨 Memory 版本身份、不确定时间表示、Scope 代数、关系词汇治理、Provenance 图循环以及若干生命周期转换仍为 OPEN/CANDIDATE/TO_VALIDATE。A 当前架构评估也将 B Fact/Claim ADR 列为阻塞项。

## 2. Repository and branch evidence / 仓库与分支证据

| Item | Verified value |
|---|---|
| Repository | `oahcom/AiMemoryBrainArchitecture` |
| Visibility | Private |
| Default branch | `main` |
| Original main HEAD at research start | `b372b62c640a2b656e54b6db62a4ee67d7d8c001` |
| Current main HEAD after branch-isolation correction | `901e38ba7b45ed1822eaefddc2da8d765cf8985c` |
| HEAD commit message | `revert(domain): remove research-only bilingual audit from main` |
| HEAD commit date | 2026-11-17T09:25:41Z |
| Repository README Blob | `429e873bd5bf081e10a449b27e3495428e1046f1` |
| Roadmap Blob | `29289361973ec4369f067706132190793cd57a6b` |
| Existing B branch | `session-b-domain-model-phase3` |
| New research branch | `research/domain-reality-001-b`, created from exact main HEAD |

The original HEAD was independently read through the repository's recent commit listing and exact commit fetch. After the branch-isolation correction, current main HEAD is `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`; it consists of explicit cleanup commits deleting the 13 research paths that had been mistakenly written there. All 13 current-main path readbacks returned NOT_FOUND. The research branch merge-base remains the original `b372b62...`; the cleanup history was not rewritten.

HEAD 已通过仓库最近提交列表和精确 Commit 读取核验。该提交 Diff 仅从 `docs/translation-status.md` 移除一条已废止的 CI Runner 运维登记，不涉及领域契约修改。

## 3. Domain source documents / 领域源文档

All following files were fetched from `main`; the SHA values are Git Blob SHAs.

| Path | Blob SHA | Observed status / finding |
|---|---|---|
| `02-domain-model/domain-model-overview.md` | `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` | DECIDED baseline; Fact treated as qualified Claim; several OPEN items |
| `02-domain-model/core-entities.md` | `8cb5a674eec8eac1f3c4d83c400dc08d00166f23` | Field-level logical definitions; opaque IDs; Claim, Entity, Relation, Evidence, Provenance, Context |
| `02-domain-model/epistemic-and-temporal-semantics.md` | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` | Core distinctions DECIDED; calibration and uncertain time partly OPEN |
| `02-domain-model/lifecycle-model.md` | `81c48c928cb5f9c76ca29d493fbd9479079e62f7` | State vocabulary DECIDED; thresholds/transitions OPEN |
| `02-domain-model/relationships-and-provenance.md` | `e762f84c59f69de7a44baad2123aed46e1ffea16` | Core semantics DECIDED; graph representation and compaction CANDIDATE/OPEN |
| `02-domain-model/scope-and-permission-model.md` | `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | Scope/Permission separation DECIDED; policy/inheritance edge cases OPEN |

Bilingual domain guide:
- Chinese `docs/zh-CN/02-domain-model/domain-model-guide.md`: Blob `a9f53a453aec25c47c58c4aea75adc43c83028d3`.
- English `docs/en/02-domain-model/domain-model-guide.md`: Blob `8a19cebacf5aefb0aded5fdbfeaff406291a5cf1`.

Additional shared source pins:
- `00-governance/architecture-invariants.md`: `33b037318e459ebb73bea33b3186f31a41d5dcfe`.
- `01-system-architecture/responsibility-matrix.md`: `fbeb6935fe874e6c843c25c3a891d6b3242cbfd3`.
- `docs/glossary/architecture-glossary.md`: `394ad3822c1bd437662e1d6e46d06d9f412c6ee9`.
- `14-ai-development/ai-development-standard.md`: `f46867f97fc1860015adbe2a1f7b8262640c16fd`.
- `README.md`: `429e873bd5bf081e10a449b27e3495428e1046f1`.
- `ARCHITECTURE_ROADMAP.md`: `29289361973ec4369f067706132190793cd57a6b`.

## 4. Cross-owner guide pins / 跨 Owner 指南 Pin

These are explanatory guides on main, not substitutes for Owner branch normative contracts:

| Owner | Chinese guide Blob | English guide Blob |
|---|---|---|
| D | `fa3f0fbe1ccc551a7805d4d5c670b588d2471be7` | `bb63d28d6243524193c2f9c2fc2e19774aaf08fd` |
| E | `84af043e306c54114e1129141ebe128f153c74e6` | `24e34121fb7e61ed89a9cb010c2f69bbd1902812` |
| F | `0e0df43de9c55f8e41d6ed596d50471798fb23cc` | `a45b868efe1367fb9934c17191109d8d87f48fab` |
| G | `87686788903dd7593844761e119d9fbecded6323` | `29385171ade4414257467b370becf690564d2095` |
| C | `b68f90f70ccf0c79bc8063e70b9a084b605ba9bf` | `c4e076887634a9e8e46df076efb0f4b70d816e0a` |
| H | `fb25bbd1c1c90871c9d9682992ca6bcd8098c661` | `228d28671955c977f653bef5b537554e431f9137` |
| I | `57423eaab9053f7b59869a493fedec583601f7fb` | `3d3fa33c016c1c601374bab1e621cfec8b2b403d` |

## 5. Current Owner branch heads / 当前 Owner 分支 HEAD

The following exact branch refs were read from GitHub on 2026-11-17. These are live branch HEAD commits, not claims that every file in each branch has been exhaustively reviewed.

| Owner | Branch | HEAD Commit SHA | Latest commit message |
|---|---|---|---|
| B | `session-b-domain-model-phase3` | `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | B: approve serialization anchor nominal type boundary |
| C | `session-c-agent-integration-2026-11-16` | `2e8414f361b0b5d7de959be8a971aadc9e62d6a9` | C: review H authenticated ingress reference gate and exact 60-test evidence |
| D | `session-d-memory-brain-2026-11-16` | `76fcc92225666a11893b7241825261319edb621e` | D: review H outer envelope auth boundary and preserve D authority |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | E: review per-authority Storage serialization anchor |
| F | `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` | F: review per-authority Storage serialization anchor |
| G | `session-g-memory-context` | `3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe` | review(g): refresh exact C/H pins to 38-test full-path closure |
| H | `session-h-bmcp-protocol` | `8e24342048d29ef29195b153b8b9ec53ba7c75d9` | docs(h): correct C envelope P0 and publish exact JSON pointer mapping |
| I | `session-i-security-governance-2026-11-16` | `2afe0e17f8c0929d9e642ccbe2cad112b5fd43a9` | docs(owner-review): review C outer envelope signer and trust/wire boundary |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `431138e7c7af8bee716f3d8dcbc20114c046bd36` | Storage: bind H outer-auth reference gate, 60-test CI and C/I/D reviews |
| A | `session-a-integration-2026-11-16` | `9bdf938b980413f592a4db9fe94f4bf2c299fb01` | docs(architecture): assess outer envelope authentication as blocking integration gap |

## 6. Relevant PRs and issues / 相关 PR 与 Issue

| Record | Observed state | Relevance |
|---|---|---|
| PR #53 — Final architecture engineering assessment | CLOSED, NOT MERGED (closed 2026-11-17T11:17:07Z) | A outcome DEFERRED / ARCHITECTURE_NOT_READY; Fact/Claim ADR, I36 governance, JF-10 and C/G/H Applied/provider evidence remain blockers |
| PR #52 — B→A protocol convergence and Storage topology review | OPEN / DRAFT | B protocol convergence is candidate, not frozen; H Unified 1.2.14 / wire 1.3.0 + CSubmitOutcome 1.0.1 candidate pair; exact-pin gaps remain; A L1 topology conditional, L4 physical realization OPEN |
| PR #42 — ChatGPT-native execution model | Open PR result | Contains Owner B v2 responsibility distinction: domain identity vs security identity; governance decision and fresh review requirements |
| Issue #3 | Open | C/G/H Applied evidence & BMCP wire contract; explicitly requests B typed ActorRef/ScopeRef/EnvironmentRef mapping |
| Issue #5 | Open | I36 governance approvals; Principal taxonomy, cross-issuer identity and ActorRef binding affect B/I boundary |
| Issue #7 | Open | Canonical runtime implementation repository and accountable owner remain unresolved; no runtime implementation evidence in this architecture repo |

Additional live issue evidence: #3 OPEN; exact CGH-APPLIED-1.1 recovery-batch owner decisions C/D/G/H/I/B are recorded with enumerated exceptions and Storage has confirmed the architecture interface with changes, but Applied Contract Frozen remains NO, production implementation/conformance NOT VERIFIED, and JF-10 P0 remains OPEN. #5 OPEN (I36-GOV-01..10 governance approvals); #6 CLOSED after C/F/G BIH consumer ACCEPT WITH ENUMERATED EXCEPTIONS and H ACCEPTED on exact BIH package Blob a45ae90b318a79bf009d14f4d917611881e9e214; #7 OPEN (runtime implementation repository/owner unresolved); #10 OPEN (JF-10 P0 physical prepared-XID/COC/fault proof); #11 OPEN (A–I baseline/redlines rollout); #21 OPEN (F/E/G local lifecycle reconciliation); #43 OPEN (system-wide consolidation). Issues #2 and #13 remain relevant to D/E/Storage publication and COC/Storage recovery evidence. These issue states were read from live GitHub on 2026-11-17.

This is a relevant-record sample, not a claim that every related PR/Issue has been exhaustively enumerated. Search and exact source review remain outstanding before B0 can pass.

这是相关记录样本，不代表已经穷尽所有相关 PR/Issue。B0 通过前仍需完成搜索与精确源文件审查。

## 7. Existing B branch comparison / 既有 B 分支比较

The existing `session-b-domain-model-phase3` branch was inspected. Its `domain-model-overview.md`, `core-entities.md`, `epistemic-and-temporal-semantics.md`, `lifecycle-model.md`, and `relationships-and-provenance.md` returned the same Blob SHAs as current main. Its `scope-and-permission-model.md` returned Blob `6a9c47031ca3ecfd47b2f7d7419b2df8d808329b`, whereas main has `b5215ae27bd65a6c89c185b496f730b6cd52efa9`.

既有 `session-b-domain-model-phase3` 分支已检查。其 domain overview、core entities、epistemic/temporal、lifecycle、relationships/provenance 五个文件与当前 main 返回相同 Blob SHA；但其 `scope-and-permission-model.md` Blob 为 `6a9c47031ca3ecfd47b2f7d7419b2df8d808329b`，main 当前 Blob 为 `b5215ae27bd65a6c89c185b496f730b6cd52efa9`。

The old branch head SHA and complete branch diff were not returned by the branch-search operation and are NOT VERIFIED here. The branch must not be assumed current or overwritten. The new research branch is isolated.

旧分支 HEAD SHA 和完整分支 Diff 未由分支搜索接口返回，因此此处标记 NOT VERIFIED。不得假定旧分支是最新版本或覆盖它。新研究分支保持隔离。

## 8. Material semantic conflicts / 重大语义冲突

### B-BASE-001 — Fact / Claim authority mismatch
- Root overview Blob `4d1debc...` says Claim is canonical and Fact is a qualified interpretation, marked DECIDED.
- Bilingual guide Blobs `a9f53a...` / `8a19ce...` explicitly say the Fact/Claim ADR remains ADR-BLOCKED and prohibit downstream schema freeze.
- A PR #53 also lists the B Fact/Claim ADR as unresolved.
- Severity: BLOCKING for Fact/Claim-dependent schema and cross-owner contract freeze.
- Authority: B proposes domain semantics; final ADR/governance path and A registry requirements must be confirmed. No unilateral resolution in this baseline.

### B-BASE-002 — Domain identity vs security identity
- Domain Entity identity and I Principal/ActorRef/ProducerIdentity are different semantic concerns.
- Main domain source defines Entity as identity-bearing referent; I guide defines Principal as authenticated security subject and ActorRef as operation actor binding.
- B must define typed reference/namespace mapping; I retains authentication, trust and authorization authority.
- Severity: HIGH; blocking only contracts that lack a safe typed mapping.

### B-BASE-003 — Scope / Tenant / Workspace / Environment boundaries
- Existing domain source defines Agent Scope and Environment Scope; I guide names tenant/user/project/Agent/session dimensions; system overview distinguishes sessions, environments and Agents.
- Exact canonical Scope taxonomy, ownership vs applicability, Tenant vs Workspace and cross-tenant reference rules need Owner I and A reconciliation.
- Severity: HIGH; fail-closed until resolved.

### B-BASE-004 — Applied / Recorded / Committed / Visible / Published
- Architecture invariant I-10 says context delivery is Applied only after explicit Adapter acknowledgement; I-18 limits ACK to protocol-level application and not model comprehension.
- H/C integration material distinguishes delivery ACK from final-request Applied proof. A PR #53 retains C/G/H Applied/provider proof as a blocker.
- B should define vocabulary boundaries; C/G/H own exact final request/provider proof; Storage owns durable visibility/commit.
- Severity: BLOCKING for cross-module Applied contract freeze; B cannot decide execution proof.

### B-BASE-005 — Forget / Deleted / Forgotten / Purged
- Domain guide describes Forgotten as governed Forget committed, access denied and cleanup/de-identification tracked.
- I guide distinguishes suppression, derivative cleanup and physical erasure; D owns canonical ForgetOperation/Fence; I owns global completion policy; Storage/backup operators own physical erasure.
- A PR #53 lists Forget anti-resurrection and physical publication/Forget proof as blockers.
- Severity: BLOCKING for claims of global completion or physical purge; domain vocabulary can be clarified without usurping D/I/Storage.

## 9. Missing definitions / 缺失定义

- Canonical typed reference grammar and namespace scope across modules: OPEN / NOT YET PINNED.
- Claim identity policy across Memory versions: OPEN in domain overview.
- Explicit temporal uncertainty model and bitemporal applicability: OPEN / TO_VALIDATE.
- Canonical Tenant vs Workspace vs Project vs Environment Scope relationship: OPEN.
- Exact Fact/Claim decision and schema consequences: BLOCKED.
- Stable mapping of B domain Actor/Scope/Environment references to I authenticated Principal and H wire identity: OPEN.
- Exact Applied vocabulary and proof authority split across C/G/H/Storage: OPEN at system level.
- Lifecycle terminality and re-entry/reappearance semantics under Forget, Superseded, Invalidated and Purged: requires D/I/Storage authority reconciliation.
- Owner-local source contract inventory and exact version pins for all A/C/D/E/F/G/H/I/Storage: NOT COMPLETE.
- Exhaustive related PR/Issue inventory and full diffs: NOT VERIFIED.
- Runtime implementation repository and executable conformance evidence: NOT VERIFIED; Issue #7 remains open.

## 10. Baseline confidence / 基线置信度

**MEDIUM** for the identified main-branch domain source set and listed Blob pins. **LOW / NOT VERIFIED** for exhaustive cross-owner normative contracts, all relevant PR/Issue history, branch HEADs not exposed by the current listing, and runtime implementation.

对已识别的 main 分支领域源文件及其 Blob Pin，置信度为 **MEDIUM**；对穷尽跨 Owner 规范契约、所有相关 PR/Issue 历史、当前分支列表未提供的分支 HEAD，以及运行时实现，置信度为 **LOW / NOT VERIFIED**。

## 12. Full Chinese baseline mirror / 中文基线完整对照

### 12.1 仓库与分支证据

| 项目 | 已核验值 | 中文说明 |
|---|---|---|
| Repository | oahcom/AiMemoryBrainArchitecture | 本次研究仓库。 |
| Visibility | Private | 私有仓库。 |
| Default branch | main | 默认分支。 |
| 原始研究基线 HEAD | b372b62c640a2b656e54b6db62a4ee67d7d8c001 | 创建 B 研究分支时的历史祖先。 |
| 分支隔离纠正后的当前 main HEAD | 8c0c5b11abf56a6f580fcf2a99c8043d3057da4f | 已通过显式删除提交从 main 清除误写研究文件；main 历史未重写。 |
| Repository README Blob | 429e873bd5bf081e10a449b27e3495428e1046f1 | 当前仓库 README 的精确内容版本。 |
| Roadmap Blob | 29289361973ec4369f067706132190793cd57a6b | 当前路线图的精确内容版本。 |
| Existing B branch | session-b-domain-model-phase3 | 原 B Owner 分支；不得与本研究分支混同。 |
| Research branch | research/domain-reality-001-b | 从精确历史基线建立的独立研究分支。 |

### 12.2 领域源文件 Pin

以下文件均从 main 读取；SHA 为 Git Blob SHA。

| 文件 | Blob SHA | 中文观察结论 |
|---|---|---|
| domain-model-overview.md | 4d1debc0ec19b3917f9e76d04bb66da4df4cd346 | 基线定义部分 DECIDED；Fact 被描述为限定 Claim；仍有多个 OPEN 项。 |
| core-entities.md | 8cb5a674eec8eac1f3c4d83c400dc08d00166f23 | 定义逻辑字段和不透明 ID；包含 Claim、Entity、Relation、Evidence、Provenance、Context。 |
| epistemic-and-temporal-semantics.md | 8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7 | 核心区分 DECIDED；校准和不确定时间仍部分 OPEN。 |
| lifecycle-model.md | 81c48c928cb5f9c76ca29d493fbd9479079e62f7 | 状态词汇 DECIDED；阈值/转换仍 OPEN。 |
| relationships-and-provenance.md | e762f84c59f69de7a44baad2123aed46e1ffea16 | 核心语义 DECIDED；图表示和压缩仍 CANDIDATE/OPEN。 |
| scope-and-permission-model.md | b5215ae27bd65a6c89c185b496f730b6cd52efa9 | Scope 与 Permission 分离 DECIDED；策略/继承边界情况仍 OPEN。 |

双语领域指南：
- 中文：docs/zh-CN/02-domain-model/domain-model-guide.md，Blob a9f53a453aec25c47c58c4aea75adc43c83028d3。
- 英文：docs/en/02-domain-model/domain-model-guide.md，Blob 8a19cebacf5aefb0aded5fdbfeaff406291a5cf1。

共享来源：
- 架构不变量：00-governance/architecture-invariants.md，Blob 33b037318e459ebb73bea33b3186f31a41d5dcfe。
- 责任矩阵：01-system-architecture/responsibility-matrix.md，Blob fbeb6935fe874e6c843c25c3a891d6b3242cbfd3。
- 架构术语表：docs/glossary/architecture-glossary.md，Blob 394ad3822c1bd437662e1d6e46d06d9f412c6ee9。
- AI Development Standard：14-ai-development/ai-development-standard.md，Blob f46867f97fc1860015adbe2a1f7b8262640c16fd。

### 12.3 跨 Owner 指南 Pin

这些是 main 上的说明性指南，不能替代 Owner 分支规范契约。

| Owner | 中文指南 Blob | 英文指南 Blob |
|---|---|---|
| D | fa3f0fbe1ccc551a7805d4d5c670b588d2471be7 | bb63d28d6243524193c2f9c2fc2e19774aaf08fd |
| E | 84af043e306c54114e1129141ebe128f153c74e6 | 24e34121fb7e61ed89a9cb010c2f69bbd1902812 |
| F | 0e0df43de9c55f8e41d6ed596d50471798fb23cc | a45b868efe1367fb9934c17191109d8d87f48fab |
| G | 87686788903dd7593844761e119d9fbecded6323 | 29385171ade4414257467b370becf690564d2095 |
| C | b68f90f70ccf0c79bc8063e70b9a084b605ba9bf | c4e076887634a9e8e46df076efb0f4b70d816e0a |
| H | fb25bbd1c1c90871c9d9682992ca6bcd8098c661 | 228d28671955c977f653bef5b537554e431f9137 |
| I | 57423eaab9053f7b59869a493fedec583601f7fb | 3d3fa33c016c1c601374bab1e621cfec8b2b403d |

### 12.4 相关 PR / Issue 中文状态

| 记录 | 读取时状态 | 对 B 的影响 |
|---|---|---|
| PR #53 | CLOSED / NOT MERGED | A 结论为 DEFERRED / ARCHITECTURE_NOT_READY；Fact/Claim ADR、I36 治理、JF-10 和 C/G/H Applied/Provider 证据仍阻塞。 |
| PR #52 | OPEN / DRAFT | B 协议收敛仍是候选，未冻结；H Unified 1.2.14 / Wire 1.3.0 + CSubmitOutcome 1.0.1 为候选配对；L4 物理实现 OPEN。 |
| PR #42 | Open PR result | 包含 B v2 责任区分：领域身份与安全身份不同；治理决定和新审查要求仍适用。 |
| Issue #3 | OPEN | C/G/H Applied 证据与 BMCP Wire 契约；要求 B 提供 ActorRef/ScopeRef/EnvironmentRef 类型映射。 |
| Issue #5 | OPEN | I36 治理批准；Principal 分类、跨 Issuer 身份和 ActorRef 绑定影响 B/I 边界。 |
| Issue #6 | CLOSED | C/F/G 对精确 BIH Package 作设计级消费者验收，带列明例外；G 后继 Blob 需重新确认。 |
| Issue #7 | OPEN | 规范 Runtime 实现仓库和负责 Engineering Owner 未确定。 |
| Issue #10 | OPEN | JF-10 P0 数据库/COC 物理能力与故障恢复未建立。 |
| Issue #11 | OPEN | A–I 基线/Redline 推进仍待完成。 |
| Issue #21 | OPEN | F/E/G 局部生命周期协调仍开放。 |
| Issue #43 | OPEN | 系统级整合控制 Issue；A 仍推迟架构冻结。 |

以上为相关记录子集，不代表已穷尽所有 PR/Issue。B0 通过前仍需完整搜索和读取相关 Diff/Commit/Blob。

### 12.5 重大语义冲突中文摘要

**B-BASE-001 — Fact / Claim 权威不一致：** 根 Overview 将 Fact 描述为限定 Claim 并标记 DECIDED；架构不变量 I-04 要求 Fact 保持不同领域概念；双语 Guide 将 Fact/Claim ADR 保持 ADR-BLOCKED，并禁止下游 Schema 冻结。当前仅能暂时确认概念区分；Fact 是否独立对象/类型，还是限定 Claim 表示，仍 OPEN。严重级别：Schema 冻结 BLOCKING。权威：B 提出领域语义；A 登记；D/E 验收下游影响。

**B-BASE-002 — 领域身份与安全身份：** Domain Entity 身份与 I Principal/ActorRef/ProducerIdentity 是不同语义问题。B 定义类型化引用/命名空间映射；I 保留认证、信任和授权权威。严重级别 HIGH；缺少安全类型映射的契约不得继续。

**B-BASE-003 — Scope / Tenant / Workspace / Environment：** 现有领域源定义 Agent Scope 和 Environment Scope；I 指南使用 Tenant/User/Project/Agent/Session 等维度。规范 Scope 分类、Ownership 与 Applicability、Tenant 与 Workspace 关系及跨 Tenant 引用规则仍需 I/A 协调。未解决前必须 Fail Closed。严重级别 HIGH。

**B-BASE-004 — Applied / Recorded / Committed / Visible / Published：** 架构不变量 I-10 要求 Adapter acknowledgement，但 H/C 资料区分 Delivery ACK 和 Final-request Applied 证明。B 定义词汇边界；C/G/H 拥有最终请求/Provider 证明；Storage 拥有持久可见性/提交。I-10 应澄清 ACK 是必要但不充分条件。严重级别 BLOCKING。

**B-BASE-005 — Forget / Deleted / Forgotten / Purged：** D 拥有规范 ForgetOperation/Fence；I 拥有全局完成策略；Storage/备份操作方拥有物理擦除。逻辑抑制不等于物理 Purge。声称全局完成或物理擦除前必须有目标级证据。严重级别 BLOCKING。

### 12.6 缺失定义中文对照

- 跨模块规范类型化引用语法和命名空间范围：OPEN / NOT YET PINNED。
- Claim 跨 Memory Version 的身份策略：OPEN。
- 时间不确定性模型和双时态适用范围：OPEN / TO_VALIDATE。
- Tenant / Workspace / Project / Environment Scope 关系：OPEN。
- 精确 Fact/Claim 决策及 Schema 后果：BLOCKED。
- B Domain Actor/Scope/Environment 引用到 I Authenticated Principal 和 H Wire Identity 的稳定映射：OPEN。
- C/G/H/Storage 之间 Applied 词汇和证明权威拆分：系统级 OPEN。
- Forget、Superseded、Invalidated、Purged 下的终态性与重新出现语义：需 D/I/Storage 协调。
- A/C/D/E/F/G/H/I/Storage 所有 Owner 的局部规范契约和精确版本 Pin：NOT COMPLETE。
- 相关 PR/Issue 穷尽清单及完整 Diff：NOT VERIFIED。
- Runtime 实现仓库和可执行一致性证据：NOT VERIFIED；Issue #7 仍 OPEN。

### 12.7 基线置信度与 B0 结论

对已识别 main 分支领域源文件及所列 Blob Pin 的置信度为 **MEDIUM**；对穷尽跨 Owner 规范契约、全部相关 PR/Issue 历史、未暴露 HEAD 的分支以及 Runtime 实现，置信度为 **LOW / NOT VERIFIED**。

**B0 = PARTIAL / NOT PASSED。** 已核验仓库身份、main HEAD、主要领域源文件、双语指南 Pin、共享不变量、责任矩阵、术语表和部分相关 PR/Issue。仍需补齐完整 Owner 规范契约、穷尽 PR/Issue Diff、精确 Commit/Blob Pin 和源级语义协调。Phase 3.8 新证据另增加阻塞性身份/信任问题：H 1.2.14 外层认证仅为 Reference Gate；C Signer/P0 为候选；I Crypto Suite/Trust 注册未批准；Storage v3.2.11 未联合接受/冻结；A 明确记录阻塞缺口。

不宣称最终领域冻结、Schema 冻结、下游实现授权或 ACCEPTED。PR #53 已 CLOSED / NOT MERGED，A 决定为 DEFERRED / ARCHITECTURE_NOT_READY；PR #52 仍 OPEN / DRAFT。

## 11. Gate B0 disposition / B0 门禁结论

**B0 = PARTIAL / NOT PASSED.** Repository identity, main HEAD, major domain source files, bilingual guide pins, shared invariants, responsibility matrix, glossary, and selected relevant PR/issues are verified. Full Owner normative contract inventory, exhaustive related PR/Issue audit, exact PR diffs/commits/blob pins and source-level semantic reconciliation are still required. New Phase 3.8 current branch-head evidence adds a material blocking identity/trust issue: H 1.2.14 outer-envelope authentication is reference-only, C signer/P0 is candidate, I cryptographic suite/trust registration is not approved, Storage v3.2.11 is not jointly accepted/frozen, and A explicitly records a blocking gap.

**B0 = PARTIAL / NOT PASSED。** 已核验仓库身份、main HEAD、主要领域源文件、双语指南 Pin、共享不变量、责任矩阵、术语表及部分相关 PR/Issue。完整 Owner 规范契约清单、穷尽相关 PR/Issue 审计、PR 精确 Diff/Commit/Blob Pin 和源级语义协调仍未完成。

No final domain freeze, schema freeze, downstream implementation authorization, or ACCEPTED status is claimed. PR #53 is CLOSED / NOT MERGED; its A decision is DEFERRED / ARCHITECTURE_NOT_READY. PR #52 remains OPEN / DRAFT.

不宣称领域最终冻结、Schema 冻结、下游实现授权或 ACCEPTED 状态。


## 13. Full Chinese peer for Owner branch and semantic conflict evidence / Owner 分支与语义冲突证据完整中文对照

### 13.1 当前 Owner 分支 HEAD 与最近提交

以下 HEAD 是 2026-11-17 读取时的分支快照，不代表所有分支文件均已穷尽审查，也不构成 Owner 对本 B 研究包的批准。

| Owner | 分支 | HEAD Commit SHA | 最近提交说明（中文） |
|---|---|---|---|
| B | `session-b-domain-model-phase3` | `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | B：批准 Storage Serialization Anchor 的名义类型边界。 |
| C | `session-c-agent-integration-2026-11-16` | `2e8414f361b0b5d7de959be8a971aadc9e62d6a9` | C：复审 H 认证入口 Reference Gate 及精确 60 项测试证据。 |
| D | `session-d-memory-brain-2026-11-16` | `76fcc92225666a11893b7241825261319edb621e` | D：复审 H 外层 Envelope 认证边界并保持 D 权威。 |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | E：复审每 Authority Storage Serialization Anchor。 |
| F | `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` | F：复审每 Authority Storage Serialization Anchor。 |
| G | `session-g-memory-context` | `3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe` | G：刷新 C/H 精确 Pin，以支持 38 项 Full-path Closure。 |
| H | `session-h-bmcp-protocol` | `8e24342048d29ef29195b153b8b9ec53ba7c75d9` | H：修正 C Envelope P0，并发布精确 JSON Pointer 映射。 |
| I | `session-i-security-governance-2026-11-16` | `2afe0e17f8c0929d9e642ccbe2cad112b5fd43a9` | I：复审 C 外层 Envelope Signer 与 Trust/Wire 边界。 |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `431138e7c7af8bee716f3d8dcbc20114c046bd36` | Storage：绑定 H 外层认证 Reference Gate、60 项 CI 和 C/I/D 复审。 |
| A | `session-a-integration-2026-11-16` | `9bdf938b980413f592a4db9fe94f4bf2c299fb01` | A：将外层 Envelope 认证评估为阻塞性集成缺口。 |

这些是历史观察值；最终决策前必须重新读取实时 Ref 和精确 Blob。不能把 HEAD 快照等同于 Owner 批准或独立复审。

### 13.2 相关 PR 与 Issue 的完整影响说明

| 记录 | 读取时状态 | 对 B 的具体影响 |
|---|---|---|
| PR #53 — 最终架构工程评估 | CLOSED / NOT MERGED | A 的结论为 DEFERRED / ARCHITECTURE_NOT_READY；Fact/Claim ADR、I36 治理、JF-10 以及 C/G/H Applied/Provider 证据仍是阻塞项。 |
| PR #52 — B→A 协议收敛与 Storage 拓扑审查 | OPEN / DRAFT | B 协议收敛只是候选，未冻结；H Unified 1.2.14 / Wire 1.3.0 与 CSubmitOutcome 1.0.1 为候选配对；仍存在精确 Pin 缺口；A 对 L1 拓扑是有条件接受，L4 物理实现仍 OPEN。 |
| PR #42 — ChatGPT-native 执行模型 | Open | 包含 B v2 责任区分：领域身份与安全身份不同；治理决定及新审查要求仍适用。 |
| Issue #3 | OPEN | C/G/H Applied 证据与 BMCP Wire 契约；明确要求 B 提供 ActorRef/ScopeRef/EnvironmentRef 类型化映射。 |
| Issue #5 | OPEN | I36 治理批准未完成；Principal 分类、跨 Issuer 身份和 ActorRef 绑定影响 B/I 边界。 |
| Issue #7 | OPEN | 规范 Runtime 实现仓库和负责 Owner 未确定；本架构仓库没有 Runtime 实现证据。 |
| Issue #10 | OPEN | JF-10 P0 的 Prepared-XID、COC 物理能力及故障证明未建立。 |
| Issue #11 | OPEN | A–I 基线与 Redline 推进尚未完成。 |
| Issue #21 | OPEN | F/E/G 局部生命周期协调仍开放。 |
| Issue #43 | OPEN | 系统级整合控制 Issue 仍开放；架构冻结尚未获准。 |

Issue #3 虽已有 C/D/G/H/I/B 的精确 CGH-APPLIED-1.1 Recovery-batch 决策，并列出例外，Storage 也确认了经过修改的架构接口，但 Applied Contract Frozen 仍为 NO；生产实现/符合性未验证，JF-10 P0 仍开放。Issue #6 的关闭仅表示 C/F/G 对精确 BIH Package 的设计级消费者验收（带列明例外），以及 H 的精确验收；不代表 I36 治理批准或 Runtime 认证。Issue #7 仍开放，负责 Runtime 仓库/Owner 未确定。Issue #10 仍开放，物理 Prepared-XID/COC/故障证明未完成。Issue #11、#21、#43 仍开放。Issue #2 与 #13 仍与 D/E/Storage Publication 和 COC/Storage Recovery 证据有关。以上状态是 2026-11-17 的读取快照，不得当作永久状态。

### 13.3 既有 B Owner 分支比较

已检查既有 `session-b-domain-model-phase3` 分支。其 `domain-model-overview.md`、`core-entities.md`、`epistemic-and-temporal-semantics.md`、`lifecycle-model.md` 和 `relationships-and-provenance.md` 与当时 main 对应文件具有相同 Blob SHA。其 `scope-and-permission-model.md` Blob 为 `6a9c47031ca3ecfd47b2f7d7419b2df8d808329b`，而 main 对应 Blob 为 `b5215ae27bd65a6c89c185b496f730b6cd52efa9`。

分支搜索未返回旧分支 HEAD SHA 和完整 Branch Diff，因此这两项必须标记 NOT VERIFIED。不得假定旧分支当前或覆盖它。本研究分支 `research/domain-reality-001-b` 与旧 B Owner 分支隔离。

### 13.4 五项重大语义冲突完整中文说明

**B-BASE-001 — Fact / Claim 权威不一致（BLOCKING）**

- 根 Overview Blob `4d1debc...` 将 Claim 定义为规范对象，并把 Fact 视为带限定的 Claim 解释，状态标记 DECIDED。
- 双语 Guide Blobs `a9f53a...` / `8a19ce...` 明确声明 Fact/Claim ADR 仍为 ADR-BLOCKED，并禁止下游 Schema 冻结。
- A PR #53 也将 B Fact/Claim ADR 列为未解决项。
- 严重性：阻塞所有依赖 Fact/Claim 的 Schema 和跨 Owner 契约冻结。
- 权威：B 提出领域语义；必须确认最终 ADR/治理路径及 A Registry 要求。本基线不得单方面解决。

**B-BASE-002 — 领域身份与安全身份（HIGH）**

- Domain Entity 身份与 I Principal/ActorRef/ProducerIdentity 属于不同语义问题。
- Main 领域源将 Entity 定义为具有身份的指称对象；I 指南将 Principal 定义为经过认证的安全主体，将 ActorRef 定义为操作行为者绑定。
- B 必须定义类型化引用/命名空间映射；I 保留认证、信任和授权权威。
- 严重性：HIGH；只有缺少安全类型映射的具体契约被阻塞，不能泛化为所有领域模型均无效。

**B-BASE-003 — Scope / Tenant / Workspace / Environment 边界（HIGH）**

- 现有领域源定义 Agent Scope 和 Environment Scope；I 指南使用 Tenant/User/Project/Agent/Session 等维度；系统概览区分 Session、Environment 和 Agent。
- 规范 Scope 分类、Ownership 与 Applicability、Tenant 与 Workspace 的关系，以及跨 Tenant 引用规则仍需 I 与 A 协调。
- 未解决前必须 Fail Closed；不得通过隐式继承或字符串别名扩大访问范围。

**B-BASE-004 — Applied / Recorded / Committed / Visible / Published（BLOCKING）**

- 架构不变量 I-10 要求 Context Delivery 具有明确 Adapter Acknowledgement 后才可称 Applied；I-18 限制 ACK 只代表协议层应用，不代表模型理解。
- H/C 集成资料进一步区分 Delivery ACK 与 Final-request Applied 证明；A PR #53 仍将 C/G/H Applied/Provider Proof 列为阻塞。
- B 负责词汇边界；C/G/H 负责精确 Final Request/Provider Proof；Storage 负责持久可见性/提交。
- I-10 必须澄清 ACK 是必要条件但不充分；不得仅凭 ACK 推导 Applied。
- 严重性：跨模块 Applied 契约冻结 BLOCKING；B 无权替代执行证明。

**B-BASE-005 — Forget / Deleted / Forgotten / Purged（BLOCKING）**

- 领域 Guide 将 Forgotten 描述为受治理 Forget 已提交、访问被拒绝，且清理/去标识过程有跟踪记录。
- I Guide 区分 Suppression、派生清理和物理擦除；D 拥有规范 ForgetOperation/Fence；I 拥有全局完成策略；Storage/备份操作方拥有物理擦除。
- A PR #53 将 Forget Anti-resurrection 和物理 Publication/Forget Proof 列为阻塞项。
- 严重性：声称 Global Completion 或 Physical Purge 前必须满足 BLOCKING 证据；领域词汇可以澄清，但不得取代 D/I/Storage 权威。

### 13.5 缺失定义与基线置信度补充

以下定义仍缺失或未固定：跨模块类型化引用语法与 Namespace Scope；Claim 跨 Memory Version 身份策略；时间不确定性模型与双时态适用范围；Tenant/Workspace/Project/Environment Scope 关系；Fact/Claim 精确决策及 Schema 后果；B Domain Actor/Scope/Environment 到 I Authenticated Principal 与 H Wire Identity 的稳定映射；C/G/H/Storage Applied 词汇与证明权威拆分；Forget、Superseded、Invalidated、Purged 的终态性及重新出现语义；所有 A/C/D/E/F/G/H/I/Storage Owner-local 契约和精确版本 Pin；穷尽 PR/Issue 清单及完整 Diff；Runtime 实现仓库和可执行符合性证据。

对已识别 main 领域源文件及 Blob Pin 的置信度为 MEDIUM；对穷尽跨 Owner 规范契约、全部 PR/Issue 历史、未暴露 HEAD 的分支以及 Runtime 实现的置信度为 LOW / NOT VERIFIED。B0 仍为 PARTIAL / NOT PASSED。

本补充不授予领域冻结、Schema 冻结、下游实现授权或 ACCEPTED 状态。
