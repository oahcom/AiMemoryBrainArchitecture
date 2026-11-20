# 治理缺陷登记中心

**中文正本**：本文件
**英文对照**：[`README.en.md`](README.en.md)
**状态**：`OPEN` — 本目录下所有登记均未解决。

本目录存放持续跟踪的治理缺陷登记。登记是一个被跟踪的缺陷，不是一次性报告。观察到符合性问题时开立，随证据积累更新，仅当纠正措施被验证后才关闭。

这里**不是**记录验收、批准或审查结论的地方。此处任何内容都不授予、不移交、不暗示任何治理权限。

## 登记清单

| 编号 | 标题 | 严重度 | 状态 | 规模 |
|---|---|---|---|---|
| `GOV-NC-2026-11-20-DIRECT-MAIN-001` | 直接推送 `main` | High | `OPEN` / `NOT_REMEDIATED` | 45 个 commit |
| `GOV-NC-2026-11-20-SELF-AUTH-002` | 授权链 / 自我发布委派 | Critical | `OPEN` / `NOT_REMEDIATED` | 1 份文书、7 次关闭 |

## 证据

机器可读证据位于 [`evidence/`](evidence/)。JSON 文件是**单一权威副本**，不翻译、不摘要、不由人工重新生成。散文文档以文件名引用它们。

| 文件 | 内容 | 采集基准 |
|---|---|---|
| `evidence/direct-main-commits.json` | 第二轮复检区间内的 12 个直推 commit 及其 PR 归属 | `main @ a7d12fe983` |
| `evidence/number-domain-scan.json` | AID 编号在 `main` 与 346 个分支上的占用情况 | `main @ a7d12fe983` |
| `evidence/issue-closures.json` | Issue #345–#351 的关闭评论 | 2026-11-20T17:00Z |
| `evidence/main-paths.json` | `main` 全部 803 个 blob 路径，用于白名单比对 | `main @ a7d12fe983` |

## 为什么存在

2026-11-20 观察到两项相互独立的失效：

1. **变更未经 PR 进入 `main`。** `PR-GOVERNANCE-001` §3 规定合并目标为 `main` 时必须创建 PR，唯一例外是合并目标为非 `main` 分支。45 个 commit 不落入该例外。见 `DIRECT-MAIN-001`。

2. **裁定那些变更的权力，由被裁定的一方自己发布。** 委派文书与关闭动作携带同一 GitHub 账号标识。见 `SELF-AUTH-002`。

两者叠加：直推产生证据，自我发布的授权接受该证据，七个战略需求关闭裁定中有四个引用的证据载体从未经过任何门禁。

## 披露

两份登记、本索引，以及它们描述的 commit 与关闭动作，均归属于同一 GitHub 账号（`oahcom`）。这种同一性正是 `SELF-AUTH-002` 的实质内容，在此明确披露，不作淡化。

建立缺陷登记不是治理行为，不授予任何验收权限。它把一个缺陷记录在案，交由真正持有该权限的主体处置。

## 相关

- [Issue #384](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/384) — 双语门禁白名单错配，命中 8/15，静默放行
- [Issue #352](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/352) — CI 因配额耗尽不可用
- `14-ai-development/PR-GOVERNANCE-001.md` §3（PR 强制）、§4（exact-Head）、§5（独立审查）
- `00-governance/bilingual-documentation-policy.md`
