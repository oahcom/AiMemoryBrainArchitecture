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
| Main HEAD | `b372b62c640a2b656e54b6db62a4ee67d7d8c001` |
| HEAD commit message | `docs: remove superseded runner operations tracking row` |
| HEAD commit date | 2026-11-17T09:25:41Z |
| Repository README Blob | `429e873bd5bf081e10a449b27e3495428e1046f1` |
| Roadmap Blob | `29289361973ec4369f067706132190793cd57a6b` |
| Existing B branch | `session-b-domain-model-phase3` |
| New research branch | `research/domain-reality-001-b`, created from exact main HEAD |

The HEAD was independently read through the repository's recent commit listing and exact commit fetch. The commit diff only removes a superseded CI runner operations row from `docs/translation-status.md`; it does not change domain contracts.

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

## 5. Relevant PRs and issues / 相关 PR 与 Issue

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

## 6. Existing B branch comparison / 既有 B 分支比较

The existing `session-b-domain-model-phase3` branch was inspected. Its `domain-model-overview.md`, `core-entities.md`, `epistemic-and-temporal-semantics.md`, `lifecycle-model.md`, and `relationships-and-provenance.md` returned the same Blob SHAs as current main. Its `scope-and-permission-model.md` returned Blob `6a9c47031ca3ecfd47b2f7d7419b2df8d808329b`, whereas main has `b5215ae27bd65a6c89c185b496f730b6cd52efa9`.

既有 `session-b-domain-model-phase3` 分支已检查。其 domain overview、core entities、epistemic/temporal、lifecycle、relationships/provenance 五个文件与当前 main 返回相同 Blob SHA；但其 `scope-and-permission-model.md` Blob 为 `6a9c47031ca3ecfd47b2f7d7419b2df8d808329b`，main 当前 Blob 为 `b5215ae27bd65a6c89c185b496f730b6cd52efa9`。

The old branch head SHA and complete branch diff were not returned by the branch-search operation and are NOT VERIFIED here. The branch must not be assumed current or overwritten. The new research branch is isolated.

旧分支 HEAD SHA 和完整分支 Diff 未由分支搜索接口返回，因此此处标记 NOT VERIFIED。不得假定旧分支是最新版本或覆盖它。新研究分支保持隔离。

## 7. Material semantic conflicts / 重大语义冲突

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

## 8. Missing definitions / 缺失定义

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

## 9. Baseline confidence / 基线置信度

**MEDIUM** for the identified main-branch domain source set and listed Blob pins. **LOW / NOT VERIFIED** for exhaustive cross-owner normative contracts, all relevant PR/Issue history, branch HEADs not exposed by the current listing, and runtime implementation.

对已识别的 main 分支领域源文件及其 Blob Pin，置信度为 **MEDIUM**；对穷尽跨 Owner 规范契约、所有相关 PR/Issue 历史、当前分支列表未提供的分支 HEAD，以及运行时实现，置信度为 **LOW / NOT VERIFIED**。

## 10. Gate B0 disposition / B0 门禁结论

**B0 = PARTIAL / NOT PASSED.** Repository identity, main HEAD, major domain source files, bilingual guide pins, shared invariants, responsibility matrix, glossary, and selected relevant PR/issues are verified. Full Owner normative contract inventory, exhaustive related PR/Issue audit, exact PR diffs/commits/blob pins and source-level semantic reconciliation are still required.

**B0 = PARTIAL / NOT PASSED。** 已核验仓库身份、main HEAD、主要领域源文件、双语指南 Pin、共享不变量、责任矩阵、术语表及部分相关 PR/Issue。完整 Owner 规范契约清单、穷尽相关 PR/Issue 审计、PR 精确 Diff/Commit/Blob Pin 和源级语义协调仍未完成。

No final domain freeze, schema freeze, downstream implementation authorization, or ACCEPTED status is claimed.

不宣称领域最终冻结、Schema 冻结、下游实现授权或 ACCEPTED 状态。
