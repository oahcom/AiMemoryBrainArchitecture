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
        - "14-ai-development/work-items/AID-2026-114/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
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
    source: "14-ai-development/work-items/AID-2026-114/gate-performance-and-rust-cache-evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-114/gate-performance-and-rust-cache-evidence.md"
    zh-CN: null
---

# AID-2026-114 — Gate 重复派发消除与 Rust CI 缓存证据

## 目的与授权

本文记录 workflow 级重复派发消除和按 job 隔离的 Rust 构建缓存，不改变 required-check 成员、门禁命令、检查器语义、job 边界或运行时行为。

- 仓库：`oahcom/AiMemoryBrainArchitecture`
- 初始取号基线：`7629b9de5e5832fe486ee72d101c4bc5121015e6`；main 同步后的当前 PR base：`57767952f1248e2de616c5dc24ac762ecb3a5a7f`
- 关联 Issue：#1212
- 署名：`user-authorized operator (delegated by account owner)`；这是代理执行证据，不代表自然人 Owner 签署。
- 编号：INDEX 最大值 109。最初临时编号 AID-2026-112 与开放 PR #1309/#1313/#1316 冲突；AID-2026-113 已由开放 PR #1314 占用。重扫后选定 AID-2026-114。分支名保留最初的 112 作为来源痕迹；规范 Work Item ID 为 114。

## 已观察基线

任务提供的测量：16 个 required context 分布于 8 个 workflow / 16 个 job，没有 `needs:`，首轮墙钟 57 秒。同一 SHA 曾有 20 条 check-run 对应 16 个 context，其中四个 workflow 各运行两次，墙钟升至 113 秒。此前没有 workflow 级 concurrency，也没有 Rust cache。隔离 Rust 构建耗时：clippy 19 秒、all-target 测试 40 秒、doctest 21 秒；同一 job 的 target 预热后 doctest 仅 3 秒。四处 `fetch-depth: 0` checkout 均为必要条件，保持不变。

## Workflow 并发控制

修改 8 个 workflow：`bilingual-docs.yml`、`branch-freshness.yml`、`document-management.yml`、`gates.yml`、`repository-hygiene.yml`、`runner-admission-policy.yml`、`rust-phase1.yml`、`session-evidence.yml`（均位于 `.github/workflows/`）。

其中 7 个 workflow 使用以下策略，`cancel-in-progress: true`：

```yaml
group: ${{ github.workflow }}-${{ github.event.pull_request.head.sha || github.sha }}
cancel-in-progress: true
```

`session-evidence.yml` 使用相同 group 表达式，但设为 `cancel-in-progress: false`。其验证器同时响应 PR 正文 `edited` 和 head `synchronize`；正文修订可能共享同一 head SHA。保留在途执行可留下每个正文摘要对应的证据，而不是取消较早记录。其余 7 个 workflow 对同一精确 SHA 的重复在途执行可取消。使用 PR head SHA 而不是 `github.ref`，避免同一分支连续 push 仅因 ref 相同而互相取消；非 PR 事件回退到 `github.sha`。

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

## 验证台账

Head `a9cfe51bf6ab3e9a1eff2c1c463303c5e6f0e2a4` 的首轮 CI 暴露 GOV-DOC-002 frontmatter 缺陷，以及 PR 正文缺少 Session Evidence 逐 Issue 表；后续提交已修复这些问题。最终修复后仍须重新核验全部 16 项精确 Head context。merge SHA、合并后 blob SHA 和缓存命中观察仍待记录。本合并前快照不声称 CI 已成功或 PR 已合并。
