---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-115/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Exact-Head CI, merge and post-merge blob readback remain pending."
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
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-115/gate-performance-and-rust-cache-evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-115/gate-performance-and-rust-cache-evidence.md"
    zh-CN: null
---

# AID-2026-115 — Gate 重复派发消除与 Rust CI 缓存证据

## 目的与授权

本文记录 workflow 级重复派发消除和按 job 隔离的 Rust 构建缓存，不改变 required-check 成员、门禁命令、检查器语义、job 边界或运行时行为。

- 仓库：`oahcom/AiMemoryBrainArchitecture`
- main 基线：`8722a37b0cd72dc550d99c0eaebe9e7556ce2f95`
- 关联 Issue：#1212
- 署名：`user-authorized operator (delegated by account owner)`；这是代理执行证据，不代表自然人 Owner 签署。
- 最终基线复核时：INDEX 最大值为 AID-2026-114；AID-2026-110 至 AID-2026-114 已在 main，AID-2026-116 被开放 PR 占用；AID-2026-115 仍由 PR #1322 唯一占用。

## 已观察基线

任务提供的测量：16 个 required context 分布于 8 个 workflow / 16 个 job，没有 `needs:`，首轮墙钟 57 秒。同一 SHA 曾有 20 条 check-run 对应 16 个 context，其中四个 workflow 各运行两次，墙钟升至 113 秒。此前没有 workflow 级 concurrency，也没有 Rust cache。隔离 Rust 构建耗时：clippy 19 秒、all-target 测试 40 秒、doctest 21 秒；同一 job 的 target 预热后 doctest 仅 3 秒。四处 `fetch-depth: 0` checkout 均为必要条件，保持不变。

## Workflow 并发控制

修改 8 个 workflow：`bilingual-docs.yml`、`branch-freshness.yml`、`document-management.yml`、`gates.yml`、`repository-hygiene.yml`、`runner-admission-policy.yml`、`rust-phase1.yml`、`session-evidence.yml`（均位于 `.github/workflows/`）。

其中 7 个 workflow 使用以下策略，`cancel-in-progress: true`：

```yaml
group: ${{ github.workflow }}-${{ github.event.pull_request.head.sha || github.sha }}
cancel-in-progress: true
```

`session-evidence.yml` 使用相同 group 表达式，但设为 `cancel-in-progress: false`。其验证器也响应 PR 正文 `edited` 事件；不同正文版本可能共享同一 head SHA。允许在途验证完成，可保留每个正文摘要对应的证据，而不是取消较早记录。其余 7 个 workflow 可取消同一精确 SHA 的重复在途执行。使用 PR head SHA 而不是 `github.ref`，避免同一分支连续 push 仅因 ref 相同而互相取消；非 PR 事件回退到 `github.sha`。

## Rust 缓存

以下四个 job 加入 `Swatinem/rust-cache@v2`：

| Job | 现有 toolchain | Shared key |
|---|---|---|
| gates / clippy | stable + clippy | gates-clippy |
| gates / fmt | stable + rustfmt | gates-fmt |
| gates / doctest | stable | gates-doctest |
| rust-phase1 / rust-workspace-test | stable + rustfmt | rust-phase1-workspace-test |

每个 job 在 toolchain 安装后记录实际解析的 `rustc --version`。缓存 key 后缀：

```yaml
key: ${{ hashFiles('Cargo.lock') }}-${{ steps.rust-toolchain-version.outputs.version }}
```

不同 shared-key 隔离各 job 的 target 目录；Cargo.lock 哈希和实际编译器版本共同参与 key，避免复用不兼容缓存。保留现有 `stable` 选择器，同时捕获真实解析版本。

## 显式 job 名称与受保护 context

- `runner-admission-policy.yml`：id `audit`，显式 `name: audit`。
- `rust-phase1.yml`：id `rust-workspace-test`，显式 `name: rust-workspace-test`。

显式 display name 与现有受保护 context 完全一致。job id 与 display-name 字段分别声明，未来内部 ID 改名不会静默改变平台 context。16 个受保护 context 保持不变，无需修改 branch protection。这消除 check-run 名称依赖 GitHub 隐式回退到 job ID 的风险。`check_declared_check_contexts.py` 保持不变。

## 保留的排除项

不合并 job；不改 `fetch-depth`；不改门禁/检查器语义；不增删或重命名 required context；#1212 保持 OPEN；不改 runtime/schema/API/数据库/部署。

## 性能预期

基线为重复派发 113 秒，16 个 context 首轮 57 秒。按要求，重复派发消除且缓存预热后的规划预估约 **38 秒**。这是估算，不是实测或 SLA。缓存命中率目前 **尚未测量**，需在后续精确 Head 的 CI 中观察。

## PR 声明格式

PR 正文的 `Work Item ID` 字段仅填写 `AID-2026-115`；临时状态放在独立章节。历史 Issue #1212 的逐 Issue 映射为 `LEGACY_UNDECLARED` / `N/A`。该格式符合 Session Evidence validator 的字段边界和历史 Issue 合同；未修改 validator 语义。

## 合并后核验

- 实施 PR：[ #1322](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1322)
- Merge commit：`ac301e09799bcc094e015db4e12d2e6ff53d5010`
- 已合并 PR head：`eaf381a9af28ebf86e7ee094f60adaaacc0d97ca`
- 精确 Head required checks：**16/16 SUCCESS**，每个 required context 各一条 check-run。
- 合并后 main blob 回读：**15/15 路径**与 PR head blob SHA 一致。
- Issue #1212 评论：`7194114609`；Issue 保持 OPEN。
- 缓存命中率：**尚未测量**，待下一轮 CI 观察。

### Required context 结果

| Required context | 结论 |
|---|---|
| Rust format (hard gate) | SUCCESS |
| Schema non-empty audit (hard gate) | SUCCESS |
| BMCP protocol index (hard gate) | SUCCESS |
| Rust doctests (hard gate) | SUCCESS |
| Bilingual docs coverage (ratchet) | SUCCESS |
| BMCP conformance suite (hard gate) | SUCCESS |
| Rust clippy (hard gate) | SUCCESS |
| Branch freshness vs base | SUCCESS |
| Session Evidence | SUCCESS |
| rust-workspace-test | SUCCESS |
| Session Evidence self-test (head) | SUCCESS |
| GOV-DOC-002 metadata checks | SUCCESS |
| GOV-DOC-001 structural checks | SUCCESS |
| Repository hygiene (hard gate) | SUCCESS |
| Session Evidence self-test (base) | SUCCESS |
| audit | SUCCESS |

### 合并后 blob 回读

| 路径 | Main blob SHA |
|---|---|
| `.github/workflows/bilingual-docs.yml` | `48c3c88b3899cdf7e10a41d2dac24f8dd820b9e0` |
| `.github/workflows/branch-freshness.yml` | `811370424c7f8d3738a8eaba8f0fd7adfe4f49a8` |
| `.github/workflows/document-management.yml` | `4d49e5d0cd87a395e3f948130be6fe35ce982266` |
| `.github/workflows/gates.yml` | `5844f50c14c63d82864a31503961273cc65a9c77` |
| `.github/workflows/repository-hygiene.yml` | `a11d2a06ac5c23d5f2e51c3a5efb3b0e29c3513b` |
| `.github/workflows/runner-admission-policy.yml` | `82938387a6c1c3acbecd193a70747af50690a731` |
| `.github/workflows/rust-phase1.yml` | `0674e5c40ae4fb0e7fe9df92f6a0504ffbdd3ee0` |
| `.github/workflows/session-evidence.yml` | `8fe7dfa2b02d200f273d8bba6be542cf02d9686c` |
| `14-ai-development/work-items/INDEX.md` | `54134d33919f0c26b7a3ab66f488847a376ede00` |
| `14-ai-development/work-items/AID-2026-115/manifest.yaml` | `6f7cba141f644cad8bbaeb0445430ea976563dd8` |
| `14-ai-development/work-items/AID-2026-115/prompt-v1.md` | `15f98b3702f5b3e69337c98f3ca5dd55c1357ed2` |
| `14-ai-development/work-items/AID-2026-115/session-evidence.md` | `8ecc2a8cf69a82a941ce56737134a34b425697da` |
| `14-ai-development/work-items/AID-2026-115/gate-performance-and-rust-cache-evidence.md` | `9b4dbadc0a9f61ec0b8be5ff274f42a7549fc781` |
| `docs/en/14-ai-development/work-items/AID-2026-115/gate-performance-and-rust-cache-evidence.md` | `ad350a1e087ca3e85bee1bcdb63a6f655e35e657` |
| `docs/zh-CN/14-ai-development/work-items/AID-2026-115/gate-performance-and-rust-cache-evidence.md` | `009ec330f4a4d8fc8fb8f57d4094bdc562bb5dcb` |

## 验证台账

实施 head、16 项精确 Head 结果、merge SHA、合并后 blob SHA 和缓存命中观察均待记录。本合并前快照不声称 CI 已成功或 PR 已合并。
