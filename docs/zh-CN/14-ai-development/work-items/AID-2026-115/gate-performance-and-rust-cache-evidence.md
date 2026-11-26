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
    source: "14-ai-development/work-items/AID-2026-115/gate-performance-and-rust-cache-evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-115/gate-performance-and-rust-cache-evidence.md"
    zh-CN: null
---

# AID-2026-115 — Gate 重复派发消除与 Rust CI 缓存证据

## 目的与授权

本文记录 workflow 级重复派发消除和按 job 隔离的 Rust 构建缓存，不改变 required-check 成员、门禁命令、检查器语义、job 边界或运行时行为。

- 仓库：`oahcom/AiMemoryBrainArchitecture`
- main 基线：`17bfc43c2b9f2f9c91cb0eb074580141e701c0b3`
- 关联 Issue：#1212
- 署名：`user-authorized operator (delegated by account owner)`；这是代理执行证据，不代表自然人 Owner 签署。
- 重新核号时：INDEX 最大值为 AID-2026-109；AID-2026-110、111、113、114 已在 main；AID-2026-112、116 已被开放 PR 占用。原临时编号 AID-2026-112 冲突，因此改号为 AID-2026-115。最终承载 PR：#1322。

## 已观察基线

任务提供的测量：16 个 required context 分布于 8 个 workflow / 16 个 job，没有 `needs:`，首轮墙钟 57 秒。同一 SHA 曾有 20 条 check-run 对应 16 个 context，其中四个 workflow 各运行两次，墙钟升至 113 秒。此前没有 workflow 级 concurrency，也没有 Rust cache。隔离 Rust 构建耗时：clippy 19 秒、all-target 测试 40 秒、doctest 21 秒；同一 job 的 target 预热后 doctest 仅 3 秒。四处 `fetch-depth: 0` checkout 均为必要条件，保持不变。

## Workflow 并发控制

修改 8 个 workflow：`bilingual-docs.yml`、`branch-freshness.yml`、`document-management.yml`、`gates.yml`、`repository-hygiene.yml`、`runner-admission-policy.yml`、`rust-phase1.yml`、`session-evidence.yml`（均位于 `.github/workflows/`）。

每个文件使用完全相同的策略：

```yaml
group: ${{ github.workflow }}-${{ github.event.pull_request.head.sha || github.sha }}
cancel-in-progress: true
```

使用 PR head SHA 而不是 `github.ref`，避免同一分支连续 push 仅因 ref 相同而互相取消；非 PR 事件回退到 `github.sha`。8 个 workflow 均按提交隔离；合并资格只针对当前精确 PR head 评估，没有 workflow 被判定为必须保留已被新提交替代的 SHA 的在途执行。

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

## 验证台账

实施 head、16 项精确 Head 结果、merge SHA、合并后 blob SHA 和缓存命中观察均待记录。本合并前快照不声称 CI 已成功或 PR 已合并。
