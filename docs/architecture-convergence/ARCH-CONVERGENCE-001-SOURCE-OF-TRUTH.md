# ARCH-CONVERGENCE-001 — Source of Truth Inventory
# ARCH-CONVERGENCE-001 — 架构规范事实源清单

- Program: ARCH-CONVERGENCE-001
- Workstream: A — Architecture Source of Truth & Contract Inventory
- Status: **DRAFT / EVIDENCE INVENTORY / NON-NORMATIVE**
- Review anchor: `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Inventory date: 2026-11-18
- Rule: This inventory classifies source provenance; it does not approve, amend, supersede, or merge any Owner contract.

## 1. Executive result / 执行摘要

The live `main` ref was read from GitHub as `e52594f181d2edb77448adcfed64a0fbdffaf3aa`. The recursive tree contains 126 entries and is not truncated. PR #89 is Open/Draft/Unmerged. PRODUCT-FIRST-001 PRs #74–#79 are all Open/Draft/Unmerged.

Main contains a small normative/documentation foundation, but it does not contain most detailed Owner specifications named by README. The Owner branches contain substantial specifications and exact-version artifacts, but branch presence is not equivalent to publication on main, approval by governance, or current cross-owner acceptance.

A material correction to PR #89: its report lists `02-domain-model/` as missing from current main. That statement is incorrect. Main contains `02-domain-model/` and six source files. The missing-directory finding must be corrected in any successor integration report.

GitHub main and owner branches are not to be changed by this inventory. All source pins below are read-only observations.

当前 `main` 实时引用为 `e52594f181d2edb77448adcfed64a0fbdffaf3aa`，递归树共 126 个条目且未截断。PR #89 仍为 Open/Draft/Unmerged；PRODUCT-FIRST-001 的 #74–#79 也全部为 Open/Draft/Unmerged。

Main 包含有限的规范与双语文档基础，但 README 声明的大部分 Owner 详细规范并未发布在 Main。Owner 分支中存在大量规范和精确版本材料，但分支存在不等于 Main 已发布、治理已批准或跨 Owner 已接受。

对 PR #89 作出一项重要更正：其报告将 `02-domain-model/` 列为 Main 缺失目录，这是错误的。Main 实际包含该目录及六份源文件。后续整合报告必须更正该目录清单。

本清单仅记录来源和证据状态，不修改 Main 或任何 Owner 分支。

## 2. Frozen GitHub baseline / GitHub 基线

| Item | Verified value |
|---|---|
| Repository | `oahcom/AiMemoryBrainArchitecture` |
| Default branch | `main` |
| Main HEAD | `e52594f181d2edb77448adcfed64a0fbdffaf3aa` |
| Main recursive tree | 126 entries; `truncated=false` |
| README blob | `429e873bd5bf081e10a449b27e3495428e1046f1` |
| Documentation portal blob | `c6420882476fc905ce313d93c809ba4896b2c542` |
| Architecture invariants blob | `33b037318e459ebb73bea33b3186f31a41d5dcfe` |
| Responsibility matrix blob | `fbeb6935fe874e6c843c25c3a891d6b3242cbfd3` |
| Domain overview blob | `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` |
| Main implementation status | README says architecture definition; implementation not started by design |

The exact main SHA was read from `refs/heads/main`, not inferred from PR metadata or historical chat context.

精确 Main SHA 来自实时 `refs/heads/main`，不是从 PR 元数据或历史会话推断。

## 3. Main source classification / Main 来源分类

Classification vocabulary:
- **AUTHORITATIVE** — current main source explicitly states normative authority or an approved baseline within its stated scope.
- **APPROVED** — an explicit approval record is present for the exact scope/version.
- **CANDIDATE** — proposed design or technology; not binding.
- **DRAFT** — work in progress or explicitly non-normative proposal.
- **HISTORICAL** — retained for historical context; not current authority.
- **UNVERIFIED** — provenance, approval, or currentness cannot yet be established.

| Main path | Blob SHA | Classification | Scope / limit |
|---|---|---|---|
| `00-governance/architecture-invariants.md` | `33b037318e459ebb73bea33b3186f31a41d5dcfe` | AUTHORITATIVE | Main normative invariants I-01..I-24 |
| `00-governance/bilingual-documentation-policy.md` | `b51b054b9f1022133666542680df74dfe19de2fb` | AUTHORITATIVE | Bilingual change policy |
| `00-governance/design-principles.md` | `192e6ba6e9287792a02b679dda0d391844270228` | AUTHORITATIVE | Main principles; must be reconciled with B Fact/Claim ADR |
| `01-system-architecture/responsibility-matrix.md` | `fbeb6935fe874e6c843c25c3a891d6b3242cbfd3` | AUTHORITATIVE | Existing logical responsibility matrix; predates detailed Owner branch contracts |
| `01-system-architecture/system-overview.md` | `995a1c5a3815d7e7b81b8d7f2ccc546c91d4c256` | AUTHORITATIVE | High-level architecture baseline |
| `02-domain-model/domain-model-overview.md` | `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` | AUTHORITATIVE | Explicitly says DECIDED baseline; §5 says Claim canonical and Fact a qualified interpretation |
| `02-domain-model/core-entities.md` | `8cb5a674eec8eac1f3c4d83c400dc08d00166f23` | AUTHORITATIVE | Main domain model source; Fact/Claim identity remains subject to ADR |
| `07-agent-integration/*` | See recursive tree | AUTHORITATIVE / scope-limited | Main contains four core integration documents; detailed current C branch contracts are newer and must be separately reconciled |
| `13-engineering-decisions/technology-architecture-blueprint.md` | `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` | CANDIDATE | TAB-001 candidate blueprint; not a technology freeze |
| `docs/README.md`, `docs/translation-status.md` | `c642088...`, `7b15c500...` | AUTHORITATIVE for documentation navigation/status | Reader guides do not replace detailed Owner contracts |
| `README.md`, `ARCHITECTURE_ROADMAP.md` | `429e873...`, `2928936...` | AUTHORITATIVE for repository claims/navigation | README path map currently diverges from actual tree |

The Main recursive tree contains these root directories: `00-governance`, `01-system-architecture`, `02-domain-model`, `07-agent-integration`, `13-engineering-decisions`, `14-ai-development`, `docs`, and `reviews`. It does not contain root detailed specifications for D/E/F/G/H/Storage/I or a root-level test-and-acceptance specification directory.

Main 递归树的根目录仅包含上述治理、系统架构、领域模型、Agent Integration、工程决策、AI 开发、双语文档和 Review 路径。D/E/F/G/H/Storage/I 的详细 Owner 规范未作为完整根级规范目录发布在 Main。

## 4. Owner branch source inventory / Owner 分支来源清单

The following live branch refs were fetched, then their recursive trees were read. These are branch snapshots, not automatically approved mainline contracts.

| Owner | Branch | Head SHA | Blob count | Source evidence |
|---|---|---|---:|---|
| A | `session-a-integration-2026-11-16` | `6e05831d264040e0e3b3359245b1e01ea613b46c` | 128 | Review/integration packages; not a domain Owner contract |
| B | `session-b-domain-model-phase3` | `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | 58 | Domain model, typed references, Fact/Claim ADR proposals |
| C | `session-c-agent-integration-2026-11-16` | `88992da30331121b81cf2773acab11d921daf281` | 136 | Provider Outcome, inference boundary, schemas, vectors and tests |
| D | `session-d-memory-brain-2026-11-16` | `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` | 86 | Canonical Store, lifecycle, versioning, Forget Fence, producer admission |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | 54 | Accepted Receipt, compiler stages, provenance, derived registration |
| F | `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` | 49 | Retrieval, activation, working set, Forget suppression |
| G | `session-g-memory-context` | `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8` | 50 | Context lifecycle/versioning and Applied persistence proposal |
| H | `session-h-bmcp-protocol` | `6608cde89d959257db612d8ff8080f631333f3f3` | 216 | BMCP schemas, validators, conformance vectors and tests; integrity incident must be reconciled |
| I | `session-i-security-governance-2026-11-16` | `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` | 139 | Identity, authorization, PermissionEpoch, Forget inventory and restore governance |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `830a559bd2f4ec72608f5a51e1a0b43779f2b989` | 122 | Storage/COC/JF-10 work is under `reviews/storage-consistency/`; no root `09-storage-and-index/` source tree |

### 4.1 Exact contract status observations

- **B:** `02-domain-model/ADR-001-fact-claim-semantics.md` explicitly says `ADR-BLOCKED`; no formal Architecture Governance decision is recorded. A second ADR artifact also says `ADR-BLOCKED`. Main's Domain Model Overview and governance invariant/principle wording conflict.
- **D:** `03-memory-brain/canonical-memory-store.md` marks authority/immutability DECIDED but detailed record layouts and transaction implementation CANDIDATE. It explicitly leaves Fact/Claim persistence ADR-BLOCKED. D's Forget contract assigns global completion/physical erasure to I and local execution to other Owners.
- **E:** `04-memory-compiler/accepted-receipt-and-idempotency-contract.md` is CANDIDATE; Storage realization, D producer APIs, H envelope and I policy approval remain OPEN.
- **G:** Phase 3.8.22 says G owns the unique durable Applied decision, but labels itself `G-OWNED NORMATIVE DESIGN DRAFT`, implementation not verified, and cross-owner acceptance required. It explicitly disclaims an independent human Owner signature.
- **I:** `global-forget-target-inventory-and-completion-evidence.md` is a CANDIDATE global governance contract; D/E/F/G/H/Storage conformance remains OPEN.
- **Storage:** `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md` selects L1 logical Option A (one serializable transaction domain per Canonical Memory authority) while L4 physical engine/deployment remains OPEN. The artifact is in a review path, not a published root Storage specification directory.
- **H:** Schema 1.2.15 and validator/test material are present on the fetched H branch tree. However, PRs #90/#91 record a severe H/C tree-integrity incident. The H ref currently fetched is `6608cde...`; the incident report references a 7-path H head `0277a8b...` and a restored snapshot beginning `4e65a2...`. These pins are not identical and require explicit reconciliation before H currentness can be declared closed.
- **C:** The live C branch ref `88992da...` matches the restoration head named in PR #92. PR #92 remains Open and targets the C research branch, not main; its declared bounded tests are not end-to-end C/Brain proof.

## 5. README path-map and publication conflicts / 路径映射与发布冲突

| README-declared source path | Main tree | Owner evidence | Finding |
|---|---|---|---|
| `02-domain-model/` | Present | B branch present | PR #89 incorrectly calls it missing |
| `03-memory-brain/` | Missing | D branch present | Owner source unpublished on main |
| `04-memory-compiler/` | Missing | E branch present | Owner source unpublished on main |
| `05-memory-runtime/` | Missing | F branch present | Owner source unpublished on main |
| `06-memory-context/` | Missing | G branch present | Owner source unpublished on main |
| `07-agent-integration/` | Present | C branch has newer expanded package | Main source currentness must be reconciled |
| `08-protocols/` | Missing | H branch uses `08-bmcp-protocol/` | Path naming mismatch |
| `09-storage-and-index/` | Missing | Storage work is under `reviews/storage-consistency/` | Normative source directory absent |
| `10-security-and-governance/` | Missing | I branch's normative files are under `09-security-governance/`; branch also contains a second directory named `10-security-and-governance/` | Path/namespace conflict |
| `11-consistency-and-recovery/` | Missing | COC/JF-10 artifacts mainly in Storage reviews and D/I/H owner artifacts | No single published source root |
| `12-testing-and-acceptance/` | Missing | tests exist in H/C branch trees; main has a reader guide only | Test source publication gap |

The README and docs portal explicitly state that reader guides do not override detailed Owner specifications. The translation status also records detailed source-level translation for multiple Owner specifications as NOT STARTED. A bilingual guide is therefore not evidence of bilingual parity for a normative field/state/schema contract.

README 与文档门户明确规定阅读指南不能覆盖详细 Owner 规范。翻译状态也将多个 Owner 详细规范的源级双语工作标记为 NOT STARTED。因此，存在中英文阅读指南不等于字段、状态机和 Schema 合同已完成双语一致性。

## 6. Related PR evidence / 相关 PR 证据

| PR | Current observed state | Evidence status / significance |
|---|---|---|
| #89 | Open / Draft / Unmerged | PRODUCT-FIRST integration proposal; report blob `3e7f0fc...`; non-normative |
| #74–#79 | All Open / Draft / Unmerged | Six product research proposals; all record no Brain implementation or end-to-end conformance |
| #66 | Open / Draft / Unmerged | D Forget terminalization proposal; based on D branch, not main |
| #68 | Open / Draft / Unmerged | I Forget authorization proposal; based on I branch, not main |
| #71 | Open / Draft / Unmerged | Storage Forget terminalization/read-suppression proposal; based on Storage branch, not main |
| #80–#83 | Open / Draft / Unmerged | Forget model, Memory OS, Memory IR and coordination research |
| #84–#86 | Open / Draft / Unmerged | Breakthrough coordinator and B/C research |
| #87–#88 | Open / Draft / Unmerged | B-02 reconciliation and bounded Forget formal review |
| #90–#91 | Open / Draft / Unmerged | H/C branch-tree integrity incident reviews |
| #92 | Open; non-draft at last metadata read; unmerged | C review/remediation; targets C research branch, not main |
| #93 | Open / Draft / Unmerged | Breakthrough integration; explicitly says not Owner sign-off and no P0 closure |
| #94 | Open / Draft / Unmerged | C workflow path-filter correction; schema-only trigger execution pending |

Open/Draft/mergeable metadata is not approval. A branch or PR is not promoted to APPROVED solely because it contains a decision-shaped document, a green bounded test, or a mergeability flag.

## 7. Missing specification register / 缺失规范登记

| ID | Missing or unresolved source | Impact | Required action |
|---|---|---|---|
| SRC-01 | D/E/F/G/H/I detailed specs not in main | Mainline cannot serve as a complete implementation baseline | Publish or formally link exact Owner snapshots with approvals |
| SRC-02 | Storage root specification directory absent | Storage L1/L4 decision provenance and row ownership difficult to discover | Storage Owner to establish canonical source location and index |
| SRC-03 | README path map conflicts with H/I paths | Broken traceability and ambiguous canonical paths | A + affected Owners approve path-map correction |
| SRC-04 | B Fact/Claim ADR blocked | No stable canonical proposition identity | B + Architecture Governance decision |
| SRC-05 | H/C integrity incident pins differ from fetched refs | Cannot assert exact currentness from incident report alone | H/C Owners reconcile live refs and tree digests |
| SRC-06 | Bilingual detailed Owner parity incomplete | Normative semantics may drift across languages | Per-contract bilingual parity matrix and Owner review |
| SRC-07 | Storage L4 engine/deployment unresolved | No physical transaction authority can be frozen | Storage/D workload, crash and restore evidence |
| SRC-08 | Cross-owner approval records not uniformly discoverable | Cannot distinguish owner draft, delegated draft and accepted contract | Add exact-version approval ledger and consumer acceptance references |

## 8. Contract dependency map / 契约依赖关系（initial）

```text
B Domain semantics (Fact/Claim, typed identities)
  ├── D Canonical Memory identity/version/commit
  │     ├── Storage transaction + visibility + restore
  │     ├── E producer admission / derived registration / publication
  │     └── D Forget Fence / canonical suppression
  ├── F retrieval / activation / indexes / caches
  ├── G ContextVersion / Delivery / Applied ledger
  │     └── C final inference boundary + Provider Outcome
  ├── H BMCP wire / authenticated delivery / evidence transport
  └── I principal / authorization / PermissionEpoch / global Forget

Storage JF-10 / COC durable protocol joins D + E + I + C/H/G recovery evidence.
```

This graph is a dependency hypothesis grounded in the cited Owner documents, not a new authority allocation. Each Owner retains its own contract and state authority.

## 9. Publication and recovery plan / 发布与恢复计划

1. Freeze each Owner branch head and recursive tree digest at the time of review.
2. For every normative contract, record path, Blob SHA, Owner, status, language pair, exact approval evidence, consumer acceptance and supersession relation.
3. Reconcile H/C tree integrity incident against current branch refs before consuming their protocol artifacts.
4. Ask B and Architecture Governance to resolve Fact/Claim ADR; until then use candidate-neutral proposition references only.
5. Ask D/Storage to publish the exact L1/L4 serialization decision, row ownership, database profile and recovery contract in a discoverable canonical path.
6. Ask I/D/E/F/G/H/Storage to close Forget producer/recipient inventory, fence, publication, cleanup, backup/restore and terminal evidence joins.
7. Correct README and docs portal only after Owners agree canonical paths; preserve old paths as redirects or history where required.
8. Build a bilingual source index and CI check for link integrity, exact Blob/commit pins, status parity and required paired-language files.
9. Do not bulk-copy Owner branches into main. Publication must be through Owner-owned Draft PRs and exact approval gates.
10. Keep all unapproved materials CANDIDATE/DRAFT/UNVERIFIED; do not infer APPROVED from branch presence.

## 10. Workstream A disposition / A 工作流结论

**A status: IN PROGRESS — baseline and initial inventory verified; Owner-level approval provenance and several live ref discrepancies remain OPEN.**

A may proceed immediately with source pinning, path reconciliation, bilingual status inventory and conflict registration. A cannot independently approve B Fact/Claim, D/Storage transaction semantics, I global Forget, H wire schemas, or any technology choice.

**No Owner contract is amended. No ADR is approved. No PR is merged. No implementation is authorized by this report.**

**A 状态：进行中——已核验基线和初始来源清单，但 Owner 级审批证据及多个实时引用差异仍未关闭。**

A 可以立即继续来源固定、路径对账、双语状态清单和冲突登记；A 无权独立批准 B Fact/Claim、D/Storage 事务语义、I 全局 Forget、H Wire Schema 或技术选型。

本报告不修改任何 Owner 合同，不批准 ADR，不合并 PR，也不授权实现。
