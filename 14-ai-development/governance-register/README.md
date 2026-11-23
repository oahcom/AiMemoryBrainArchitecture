---
document_metadata:
  domain: ai-development
  role: index
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "This file is an index of governance-register entries; it does not independently approve or establish the authority of indexed records."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# 治理缺陷登记中心

**中文正本**：本文件
**英文对照**：[`README.en.md`](README.en.md)
**状态**：`OPEN` — 本目录下除 `-028` 外的登记均未解决。`-028` 已由 `OWNER-DECISION-RELEASE-BOUNDARY-001` 裁定关闭，残留移交裁定文书 §8。

本目录存放持续跟踪的治理缺陷登记。登记是一个被跟踪的缺陷，不是一次性报告。观察到符合性问题时开立，随证据积累更新，仅当纠正措施被验证后才关闭。

这里**不是**记录验收、批准或审查结论的地方。此处任何内容都不授予、不移交、不暗示任何治理权限。

## 登记清单

| 编号 | 标题 | 严重度 | 状态 | 规模 |
|---|---|---|---|---|
| `GOV-NC-2026-11-20-DIRECT-MAIN-001` | 直接推送 `main` | High | `OPEN` / `NOT_REMEDIATED` | 53 个 commit |
| `GOV-NC-2026-11-20-SELF-AUTH-002` | 授权链 / 自我发布委派 | Critical | `OPEN` / `NOT_REMEDIATED` | 1 份文书、7 次关闭 |
| `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` | 裁定后无审查合并 | High | `OPEN` / `NOT_REMEDIATED` | 4 个 PR（#390 / #394 / #395 / #402） |
| `GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004` | 验收条件未满足即关闭 | High | `OPEN` / `NOT_REMEDIATED` | 1 个 Issue（#384），4/10 条 AC 不满足 |
| `GOV-NC-CONVERGENCE-2026-11-20` | 治理收敛定义与执行边界 | — | `ACTIVE` / `RECORDED_NOT_PREVENTED` | 3 个层次 |
| `GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026` | Evidence 领域契约符合性 | High | `OPEN` / `WP-B DISPATCHED`（`AID-2026-053`）；WP-A 不可实施 | 1 个实体，2 个工作包；WP-A 缺三个契约类型定义 |
| `GOV-NC-2026-11-22-PROVENANCE-REFERENCE-REVALIDATION-027` | Provenance 引用重验 | High | `OPEN` / `DISPATCHED`（`AID-2026-052`） | 4 类引用字段，形态不同 |
| `GOV-NC-2026-11-23-PROVENANCE-GRAPH-ADD-SIGNATURE-028` | `ProvenanceGraph::add` 公开签名变更 | High | `CLOSED-BY-RULING` / 分类已更正 | 1 个公开签名，2 处引证勘误 |
| `GOV-NC-2026-11-23-UNREACHABLE-GUARD-030` | 017 已修但其守卫变为死代码，且 014 的修复使该套件 24 项失效 | High | `OPEN` / `MEASUREMENT_ONLY` | 1 个恒真守卫，167 个文件退出配对，24 项失效且无 workflow 运行 |
| `GOV-NC-2026-11-23-EXECUTION-RESTORED-029` | 执行侧恢复，005 的现在时断言失效 | High | `OPEN` / `MEASUREMENT_ONLY` | 2 条首次执行，3 条被反证的现在时断言 |

## 证据

机器可读证据位于 [`evidence/`](evidence/)。JSON 文件是**单一权威副本**，不翻译、不摘要、不由人工重新生成。散文文档以文件名引用它们。

| 文件 | 内容 | 采集基准 |
|---|---|---|
| `evidence/direct-main-commits.json` | 第二轮复检区间内的 12 个直推 commit 及其 PR 归属 | `main @ a7d12fe983` |
| `evidence/direct-main-commits-p2.json` | 第三轮区间 `c099816f...ee9b3031` 的 4 个 commit | `main @ ee9b3031` |
| `evidence/direct-main-commits-p3.json` | 第四轮区间 `ee9b3031...1a0dc911` 的 11 个 commit | `main @ 1a0dc911` |
| `evidence/direct-commit-filesets.json` | 第三/四轮新增直推 commit 的逐 commit 文件集 | `main @ 1a0dc911` |
| `evidence/attribution-1491856051.json` | author email `1491856051` 全部 20 个 commit 及 PR 归属 | `main @ 1a0dc911` |
| `evidence/merge-gate-evidence.json` | PR #390 / #394 / #395 的门禁字段（reviews、checks、耗时） | 2026-11-21T03:00Z |
| `evidence/number-domain-scan.json` | AID 编号在 `main` 与 346 个分支上的占用情况 | `main @ a7d12fe983` |
| `evidence/issue-closures.json` | Issue #345–#351 的关闭评论 | 2026-11-20T17:00Z |
| `evidence/main-paths.json` | `main` 全部 803 个 blob 路径，用于白名单比对 | `main @ a7d12fe983` |

**注**：`main-paths.json` 采集于 `main @ a7d12fe983`（803 blob）。第四轮复检时 `main` 已至 `1a0dc911`（826 blob）。目录集比对结论仍成立，但引用该文件时应注明其采集基准不是当前 head。

## 四类失效

| # | 失效 | 载体 | 登记 |
|---|---|---|---|
| 1 | 变更未经 PR 进入 `main` | 53 个 commit | `DIRECT-MAIN-001` |
| 2 | 裁定变更的权力由被裁定一方自己发布 | Issue #305 文书 | `SELF-AUTH-002` |
| 3 | PR 存在但门禁未满足即合并 | PR #390 / #394 / #395 | `MERGE-AFTER-RULING-003` |
| 4 | Issue 在自定 AC 未满足时被关闭 | Issue #384 | `AC-UNMET-CLOSURE-004` |

四者叠加：直推产生证据（1），自我发布的授权接受该证据（2），走完 PR 形式但绕过其门禁（3），最后以未执行的 AC 关闭追踪 Issue（4）。

## 收敛状态

`GOV-NC-CONVERGENCE-2026-11-20` 定义治理收敛的三个层次，当前状态为 **`RECORDED_NOT_PREVENTED`**（已记录，未阻止）：

- **层次一 记录收敛**：已达成。四类失效均有可检索、可复现的登记。
- **层次二 平台能力决策**：等待 Owner。唯一载体 Issue #283。
- **层次三 行为约束**：即日生效，约束本会话，不冒充技术保护。

`RECORDED_NOT_PREVENTED` 不得升级为 `REMEDIATED`，直到平台能力决策作出并实施，或出现足够时长的无强制自愿遵守记录。

## 一个必须记录的边界

第 3 类失效的纠正措施 M-3（平台强制 `reviews>=1` + 必需检查成功）已被证明**在当前 GitHub 计划下不可执行**：

```
PUT /repos/.../branches/main/protection -> 403
    "Upgrade to GitHub Pro or make this repository public to enable this feature."
```

持有 `admin: true` 仍返回 403，说明这不是权限问题，是私有仓库 + 低版本计划的能力缺失。

因此本目录**不主张**技术手段可以阻止同类事件再次发生。在计划升级或仓库公开之前，唯一防线是合并者自愿，而三次实测表明自愿没有发生。

`#396` 已并入 `#283`（`PLATFORM-RESIDUAL`）作为该能力的唯一载体。

## 披露

四份登记、本索引，以及它们描述的 commit、合并与关闭动作，均归属于同一 GitHub 账号（`oahcom`）。这种同一性正是 `SELF-AUTH-002` 的实质内容，在此明确披露，不作淡化。

建立缺陷登记不是治理行为，不授予任何验收权限。它把一个缺陷记录在案，交由真正持有该权限的主体处置。

## 相关

- [Issue #384](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/384) — 双语门禁白名单错配。**已重开**，收窄至 AC-1 / AC-4 / AC-5 / AC-9
- [Issue #400](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/400) — `EMBEDDED_BILINGUAL_SOURCES` 未审计的豁免面
- [Issue #401](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/401) — AC-5 旁路检测修复任务
- [Issue #283](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/283) — 平台层 required-check 强制（`PLATFORM-RESIDUAL`）
- [Issue #352](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/352) — CI 因配额耗尽不可用
- `14-ai-development/PR-GOVERNANCE-001.md` §3（PR 强制）、§4（exact-Head）、§5（独立审查）
- `00-governance/bilingual-documentation-policy.md`
