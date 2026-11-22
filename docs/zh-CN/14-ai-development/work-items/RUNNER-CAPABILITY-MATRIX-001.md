---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-22"
      last_verification_note: "第 3 节的每个实测值都抄自 run 44986186138 的日志归档或 GitHub Actions API 响应；每个未测量项都在第 4 节列为未验证。"
    usage_status: Active
    modification_status: Modified
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
    source: "14-ai-development/work-items/RUNNER-CAPABILITY-MATRIX-001.md"
    en: "docs/en/14-ai-development/work-items/RUNNER-CAPABILITY-MATRIX-001.md"
---

# RUNNER-CAPABILITY-MATRIX-001 —— 自建 runner 的真实能力与 12 个 `ubuntu-latest` workflow 的处置

- **记录类型：** 诊断工作记录。本记录不修改任何 workflow 文件、`crates/` 源码或门禁脚本。
- **状态：** `Draft` —— 诊断完成，迁移未执行。
- **证据截止：** `main @ 6de4e38c`，2026-11-22T06:28Z。
- **被测 runner：** `zesu-x64`，标签 `[self-hosted, Linux, X64]`，`total_count: 1`。
- **主要证据：** run `44986186138`（`Ubuntu Worker - Read-only Diagnostics`，`workflow_dispatch`，结论 `success`），外加覆盖 2026-11-16 至 2026-11-21 的 882 条 Actions API 运行样本。

## 1. 结论摘要

1. **runner 是真实存在、在线、且在强制执行的。** run `44986186138` 执行了 4 个 step 并返回了主机事实（第 3 节）。`hooks/guard.log` 存在，有 9 行决策记录，最后一行是 `ALLOW ref=refs/heads/main event=workflow_dispatch source=env`。`hooks/observe.flag` **不存在**，因此 L1 准入控制处于阻断模式，不是只记录日志。
2. **决定性约束不是标签，是准入钩子。** L1 只允许 `GITHUB_REF == refs/heads/main` **且** 事件属于 {`push`, `workflow_dispatch`, `schedule`}。12 个失效 workflow 里有 8 个由 `pull_request` 触发。`pull_request` 事件的 ref 是 `refs/pull/N/merge`，所以**给这 8 个改标签不可能让它们跑起来** —— 它们会以零 step 失败，和 2026-11-21 的 `GOV-DOC-002 metadata checks` 一模一样。
3. **朴素改标签会被本仓库自己的门禁否决。** 在临时副本里把 12 个全改成 `runs-on: [self-hosted, linux, x64]`，`scripts/ci/audit_runner_admission.py` 退出码 1，报 **12 处违规**（第 5.2 节）。L2 策略在设计上就已经禁止这次迁移。
4. **`total_count: 1` 使这是串行资源，而当前到达率超过其容量。** 一个成功的 self-hosted job 花约 30 秒墙钟，只为做约 3 秒的活（实测：04:41:53 → 04:42:26，step 实际运行 04:42:05 → 04:42:08）。在观测到的峰值小时（2026-11-17T22:00：100 次运行、38 次 PR 同步、1370 秒实测工作量），全迁需要每 60 分钟墙钟配约 73 分钟 runner 时间 —— **超出容量 1.2 倍，队列无界增长**。把每次 PR 同步压成 1 个 job 后降到约 32 分钟/小时（利用率 53%）。第 8 节给出量化。
5. **建议：** 不要全迁。先合并，再迁无依赖的 `push`→`main` 那一半，`pull_request` 门禁与 `runner-admission-policy` 原地保留，等 Owner 裁定 L1 钩子是否可接受同仓库 `pull_request`（第 9 节）。

## 2. 方法

| 步骤 | 做了什么 | 为何可信 |
|---|---|---|
| runner 清单 | `GET /repos/{o}/actions/runners` | 来自 API，非推断 |
| 能力探测 | 下载 run `44986186138` 的日志归档（`GET .../actions/runs/{id}/logs`，302 跳转到 zip），读 `diagnostics/3_Read-only host diagnostics.txt` | 值是 step 自己的 stdout |
| 失败签名 | 对 2026-11-21/22 的 6 个失败 run 调 `GET .../actions/runs/{id}/jobs` | 显示 `conclusion: failure`、`steps: []`、`runner_name: ""`、`labels: ["ubuntu-latest"]` |
| 钩子策略 | `14-ai-development/ubuntu-self-hosted-runner-bootstrap.en.md` 第 4.1 节 + 探测输出里的 `guard.log` 行 | 策略文本与运行时决策一致 |
| L2 策略行为 | 把 13 个 workflow 文件与 `audit_runner_admission.py` 复制到 `/tmp/sim2`，执行 `sed 's/runs-on: ubuntu-latest/runs-on: [self-hosted, linux, x64]/'`，再跑审计 | 实际执行，捕获退出码与 12 条 `::error::` |
| 成本模型 | 882 条运行样本；时长取 `conclusion: success` 的 `run_started_at` → `updated_at`；外加 `44986186138` 的 step 时间戳 | 实测而非估算；两个来源在第 8 节分开标注 |

凡有测量手段的地方，本记录都没有仅凭文档推断。只有文档的地方，第 4 节明确说明。

## 3. runner 能力矩阵

下表中所有「实测」行的来源：run `44986186138` 日志归档，step 3，时间戳 `2026-11-22T04:42:05Z`。

| 能力项 | 实测值 | 证据来源 | 是否已验证 |
|---|---|---|---|
| runner 软件版本 | `2.338.2` | `0_diagnostics.txt` 第 1 行：`Current runner version: '2.338.2'` | 是 |
| kernel | `Linux 7.0.0-30-generic` | `uname -sr` | 是 |
| 架构 | `x86_64` | `uname -m` | 是 |
| 操作系统 / 版本 | `ubuntu` / `26.04` | `/etc/os-release` 的 `ID` + `VERSION_ID` | 是 |
| CPU 核数 | `4` | `nproc` | 是 |
| 内存总量 | `3.6Gi` | `free -h` | 是 |
| 内存可用 | `1.4Gi`（已用 2.3Gi，buff/cache 1.1Gi） | `free -h` | 是 |
| Swap | 总 `2.0Gi`，已用 `1.6Gi`，剩 `389Mi` | `free -h` | 是 |
| 根分区 | `/dev/vda3`，总 `39G`，已用 `31G`，**可用 `6.8G`**，82% | `df -h /` | 是 |
| NTP 同步 | `yes` | `timedatectl show -p NTPSynchronized --value` | 是 |
| `tailscaled` | `enabled`、`active` | `systemctl is-enabled` / `is-active` | 是 |
| 主机 egress 服务单元 | `inactive`（单元名被 workflow 隐去） | `systemctl is-active [HOST EGRESS SERVICE]` | 状态已验证 / 身份按设计未验证 |
| L1 准入钩子已装 | **是** —— `guard.log` 存在，`9` 行 | `wc -l < hooks/guard.log` | 是 |
| L1 钩子在阻断 | **是** —— `observe.flag` 不存在，未打印 `WARNING:` | 该 step 仅在 flag 存在时打印 `WARNING: observe.flag present — admission control is log-only`；它没有打印 | 是 |
| 最后一条守卫决策 | `2026-11-22T04:42:05Z ALLOW ref=refs/heads/main event=workflow_dispatch source=env` | `tail -n 1 hooks/guard.log` | 是 |
| runner 账户 | `uid=1000(ubuntu) gid=1000(ubuntu)`，组 `1000(ubuntu),4(adm),24(cdrom),**27(sudo)**,30(dip),101(lxd)` | `id` | 是 |
| bash 可用 | 是 | 每个 step 都以 `shell: bash`、`-euo pipefail` 运行 | 是 |
| `uname` / `free` / `df` / `nproc` / `timedatectl` / `systemctl` / `wc` / `tail` 可用 | 是 | step 3 全部有输出 | 是 |
| job 调度延迟 | 排队 8 秒（`created 04:41:53` → `started 04:42:01`） | run `44986186138` 的 job 时间戳 | 是（单样本） |
| 每 job 固定开销 | 约 30 秒墙钟换约 3 秒实际工作（`started 04:42:01` → `completed 04:42:26`；step 运行于 `04:42:05` → `04:42:08`） | run `44986186138` 的 job 时间戳 | 是（单样本） |
| 跨 job 工作目录复用 | 串行（`total_count: 1`），因此复用同一工作区；`actions/checkout` 清理 checkout 路径，但不清理 `$HOME` 与 `/tmp` | `total_count: 1` + `actions/checkout` 的既定行为 | 部分 —— 复用是确定的，清理范围不确定 |
| Rust 工具链（`cargo`、`rustc`） | **未测量** | — | **否** |
| Python 3 是否存在 / 版本 | **未测量**（探测只用了 `bash`） | — | **否** |
| `rfc8785`、`jsonschema`、`cryptography` 是否已装 | **未测量** | — | **否** |
| `cargo` registry 缓存是否已预热 | **未测量** | — | **否** |
| Node / `npm` 是否存在 | **未测量** | — | **否** |
| `gh` CLI 是否存在 | **未测量** | — | **否** |
| 出站 HTTPS 连通性（PyPI、npm、static.rust-lang.org） | **未测量** —— 探测没有发起任何网络请求 | — | **否** |
| `sudo` 是否免密可用 | **未测量** —— 账户在 `sudo` 组，但未运行 `sudo -n true` | 仅组成员资格 | **否** |

### 3.1 矩阵已经排除的可能

- **`ubuntu 26.04` 不是 GitHub 托管镜像。** 任何依赖托管镜像预装工具链的 workflow，依赖的是这里不存在的东西。
- **`/` 上 6.8G 可用是硬性的磁盘约束。** 本 workspace 冷跑 `cargo test --workspace --all-targets` 产出 **1009 MB** 的 target 目录（本地实测，第 8.4 节）。默认位置留下 6 次这样的构建就填满剩余空间。
- **可用内存 1.4Gi、4 核** 是 Rust 的硬性内存约束。`cargo test` 默认每核一个 rustc 进程、每 crate 一个测试二进制；在 5 GiB / 16 核参考机上冷构建没有触顶，但在 1.4 GiB 可用内存下这是真实的 OOM 风险，必须限制（`CARGO_BUILD_JOBS`），不能假设不存在。
- **`27(sudo)` 组成员资格，加上只检查 ref 与事件的 job-started 钩子**，正是 bootstrap 文档已经点名的威胁模型：「被放行的 workflow 可以 `sudo`」。这就是 `pull_request` 禁令是承重结构、不能为方便而放松的原因。

## 4. 无法验证项清单

这份清单刻意比「猜一个值」的诱惑更长。

| # | 未验证项 | 为何重要 | 如何落实 |
|---|---|---|---|
| U-01 | Rust 工具链是否存在及版本 | `rust-phase1.yml` 是最值得迁的 workflow（中位 45 秒、11 次成功），也是最容易搞错的一个 | 在已有的诊断 workflow 里加一行 `command -v cargo rustc`；对一个已放行的 `workflow_dispatch` job 只改 1 行 |
| U-02 | runner 上 Python 3 的版本 | 12 个 workflow 里有 9 个是 `python3` 脚本；`aid-2026-001-*` 钉 `3.13`，`bilingual-docs` 与 `document-management` 用裸 `python3` | 同一次探测加 `python3 -V` |
| U-03 | `rfc8785`、`jsonschema`、`cryptography` 是否预装 | 决定 `h-applied-delivery-evidence-conformance` 是否还需要 pip 步骤 | 探测里加 `python3 -c "import rfc8785, jsonschema, cryptography"` |
| U-04 | PyPI / npm / `static.rust-lang.org` 是否可达 | `h-applied` 跑 `pip install` + `npm ci`；`rust-phase1` 用 `dtolnay/rust-toolchain`，会下载 rustup | `curl -sSI https://pypi.org/simple/ -o /dev/null -w '%{http_code}'` 等。**不要**因为 `tailscaled` 是 active 就推断可达 |
| U-05 | `cargo` registry 缓存状态 | registry 冷意味着 `cargo test` 还要下载约 290 个 crate，这会主导那个 45 秒 | 探测里加 `du -sh ~/.cargo/registry` |
| U-06 | Node / `npm` 是否存在 | `h-applied` 的 `npm ci` | 探测里加 `command -v node npm` |
| U-07 | `gh` CLI 是否存在 | `ai-owner-worker-bootstrap-labels` 直接调用 `gh api` | 探测里加 `command -v gh` |
| U-08 | `ubuntu` 的 `sudo -n` 是否成功 | 组成员资格不等于存在可用的 NOPASSWD 规则 | `sudo -n true; echo $?` —— 但这是权限探测，应由 Owner 批准并留痕，不能作为例行诊断 |
| U-09 | 该 runner 构建上 `actions/checkout` 的清理行为 | 决定 `target/` 与 `node_modules/` 是否跨 job 泄漏 | 连跑两次 Rust job，前后各取一次 `df -h /` 对比 |
| U-10 | L1 钩子是否会扩展到同仓库 `pull_request` | 这一个决定就决定了 12 个里 8 个能否在这里跑 | Owner 决策，第 9 节 |

## 5. 决定性约束：L1 准入钩子

### 5.1 策略与运行时一致

`14-ai-development/ubuntu-self-hosted-runner-bootstrap.en.md` 第 4.1 节规定：除非 `GITHUB_REF` 恰为 `refs/heads/main` **且** `GITHUB_EVENT_NAME` 属于 `push`、`workflow_dispatch`、`schedule`，钩子就让 job 失败；ref 无法解析时 fail-closed。探测确认钩子已装且在阻断（第 3 节）。

失败签名很有辨识度，且同一份文档里已有记录：

| Run | 触发 | 守卫判定 | 观测到的 job |
|---|---|---|---|
| `44049832708` | `push` → `refs/heads/main` | `ALLOW` | `success`，4 个 step |
| `44050069421` | `push` → `refs/heads/ci/admission-negative-test` | `DENY ref_not_default_branch` | `failure`，step 2 `Set up runner` 失败，step 3 `This step must never execute` **skipped** |
| `44986186138` | `workflow_dispatch` → `main` | `ALLOW` | `success`，4 个 step |

**这与 2026-11-21 那批失败是不同签名。** 当前 `ubuntu-latest` 的失败显示 `steps: []` —— 一个 step 都不存在，因为没有任何 runner 接手（`runner_name: ""`、`labels: ["ubuntu-latest"]`）。被守卫拒绝的 job 在这台 runner 上显示 **4 个** step 且 step 2 失败。将来读运行记录的人必须区分这两者，否则会把守卫拒绝误诊成 runner 缺失。

### 5.2 本仓库自己的 L2 门禁已经禁止朴素迁移

临时模拟（`/tmp/sim2`，复制全部 13 个文件，替换 `runs-on`，跑真实审计脚本）：

```
runner admission: 14 self-hosted job(s) audited, 12 violation(s)
exit=1
```

12 处违规：

| 数量 | 违规 | workflow |
|---|---|---|
| 9 | `untrusted trigger 'pull_request' is not permitted for self-hosted jobs` | `aid-2026-001-manifest-validation`、`aid-2026-001-reference-model`、`bilingual-docs`、`document-management`、`g-applied-reference-model`、`h-applied-delivery-evidence-conformance`、`publication-protocol-reference-model`、`runner-admission-policy`、`rust-phase1` |
| 3 | `on.push.branches includes non-main branch` | `abr-forget-cross-owner-model`（`review/architecture-breakthrough-integration-2026-11-18`）、`h-applied-delivery-evidence-conformance`（`session-h-bmcp-protocol`）、`publication-protocol-reference-model`（`fix/publication-fence-admission-order`） |

**后果：** 把任何 `pull_request` workflow 迁到这台 runner，都是两部分改动 —— 标签**和**触发器，而触发器那一半改变了门禁所保护的东西。那是 Owner 决策，不是一次 `runs-on` 编辑。

### 5.3 一处值得报告的 L2 审计缺口

`scripts/ci/audit_runner_admission.py` 里的 `UNTRUSTED_TRIGGERS` 是 `{pull_request, pull_request_target, issue_comment, workflow_run, workflow_call}`，**不含** `issues`。单独模拟 `ai-owner-worker.yml`（触发于 `issues: [labeled]` 与 `workflow_dispatch`）得到：

```
runner admission: 2 self-hosted job(s) audited, 0 violation(s)
exit=0
```

也就是说，L2 会放行一个由 `issues` 触发的 self-hosted job，而 L1 会在运行时拒绝它（事件不在白名单）—— 一次静默的零 step 失败，审计上没有任何信号。**本记录不修改该审计**；它指出 `issues`（以及将来任何不在 L1 白名单内的事件）应加入 `UNTRUSTED_TRIGGERS`，使 L2 与 L1 一致。在此之前，请把「L2 通过」当作必要但不充分。

## 6. 逐 workflow 评估

**迁移风险**图例：`sudo` = 需系统包；`net` = 需下载依赖；`cache` = 向被复用的工作区写入大状态；`hosted` = 依赖托管镜像预装工具；`boundary` = L1/L2 必须守住的安全边界。

| # | workflow | 触发方式 | 它跑什么 | 迁移风险 | 建议 |
|---|---|---|---|---|---|
| 1 | `abr-forget-cross-owner-model.yml` | `push` → `review/architecture-breakthrough-integration-2026-11-18`（含路径过滤） | `reviews/architecture-breakthrough/integration/model` 下 3 个纯标准库 `python3` 模型脚本 | **boundary**（非 main ref → 守卫 `DENY`），外加死范围：分支领先 148 个提交，最后提交 2026-11-18，未合并 | **删除** |
| 2 | `ai-owner-worker-bootstrap-labels.yml` | `workflow_dispatch` | `gh api` 创建/校验标签，`python3 -c urllib.parse` | `hosted`（`gh` 是否存在未验证，U-07）、`net`（写 API）、需 `issues: write` | **确认一次后删除** —— 幂等的一次性迁移产物 |
| 3 | `ai-owner-worker.yml` | `issues: [labeled]`、`workflow_dispatch` | 2 个 job：`codex`（35 分钟超时、agent 运行、上传 artifact），然后 `publish`（`contents: write`、`pull-requests: write`，推分支并开 PR） | **boundary**（被放行的 job 可以 `sudo`；这个 job 会推分支）、`hosted`（codex CLI）、`cache`（agent 工作区）、占用串行 runner 35 分钟 | **不要迁** |
| 4 | `aid-2026-001-manifest-validation.yml` | `pull_request`、`push` → `main` | `pip install PyYAML==6.0.2`，对 `AID-2026-001/manifest.yaml` 做严格重复键 YAML 解析 | **boundary**（PR 那一半）、`net`（PyPI；3.13 的 wheel 未验证，U-04） | **改造后迁 `push` 那一半** |
| 5 | `aid-2026-001-reference-model.yml` | `pull_request`、`push` → `main` | 对 196 K 纯标准库测试跑 `python3 -m unittest discover` | **boundary**（PR 那一半）—— 无 `net`、无 `cache` | **迁 `push` 那一半** —— 成本最低的首个迁移 |
| 6 | `bilingual-docs.yml` | 仅 `pull_request`（5 种活动类型） | `python3 scripts/check_bilingual_docs.py`，`fetch-depth: 0` | **boundary**（仅 PR → 守卫永远 `DENY`）、`net`（全量克隆） | **合并**进单个治理 job；留在这台 runner 之外 |
| 7 | `document-management.yml` | `pull_request`、`push` → `main` | 先 `scripts/test_check_document_management.py`，再 `scripts/check_document_management.py --require-changed`，`fetch-depth: 0` | **boundary**（PR 那一半）；本地 3.2 秒 CPU 工作，无 `net`、无 `cache` | **合并**；迁 `push` 那一半 |
| 8 | `g-applied-reference-model.yml` | `pull_request`、`push` → `main` | 对 40 K 纯标准库测试跑 `python3 -m unittest discover` | 仅 **boundary**（PR 那一半） | **与 5、10 合并** |
| 9 | `h-applied-delivery-evidence-conformance.yml` | `push` → `session-h-bmcp-protocol`、`workflow_dispatch`、`pull_request` → `main` | `pip install jsonschema rfc8785 cryptography`、`npm ci`，再跑 5 个 `unittest discover` 套件 | **boundary**（PR 那一半 + 非 main push），**`net` 面最大**（3 个原生/wheel 依赖 + npm registry）、`cache`（`node_modules`）、`hosted`（`rfc8785` 在托管环境可能预装，这里未验证，U-03） | **改造后最后迁 `workflow_dispatch` + `push`→`main`** |
| 10 | `publication-protocol-reference-model.yml` | `push` → `fix/publication-fence-admission-order`、`pull_request` → `main` | 对单个测试文件跑标准库 `unittest` | **boundary**（两半都是：非 main ref 与 PR），死范围（分支领先 202 个提交，最后提交 2026-11-18） | **删掉 `push` 那一半；PR 那一半并入 5 与 8** |
| 11 | `runner-admission-policy.yml` | `pull_request`、`push` → `main` | `python3 scripts/ci/audit_runner_admission.py` —— L2 审计器本身 | **boundary，且有利益冲突**：在被审计的主机上跑审计器，等于让 workflow 改动能在同一信任域里关掉自己的准入检查 | **不要迁** —— 它待在原地是正确的 |
| 12 | `rust-phase1.yml` | `pull_request`、`push` → `main` | `dtolnay/rust-toolchain@stable`，再 `cargo test --workspace --all-targets`（11 个 crate） | **boundary**（PR 那一半）、`net`（rustup + 约 290 个 crate）、`cache`（**1009 MB** target 目录）、内存（可用 **1.4 GiB** 对 4 路并行 rustc）、磁盘（**6.8 GB** 可用） | **改造后迁 `push` 那一半** —— 收益最高，搞错的代价也最高 |

### 6.1 这张表暴露的两件事

- **8 个 workflow 的 `pull_request` 那一半不是标签问题。** 是策略问题。任何只说「改 `runs-on`」却不说 `pull_request` 怎么办的方案，都不是方案。
- **有 4 个 workflow 与 runner 无关地就是死重量。** `abr-forget-cross-owner-model`，以及 `publication-protocol-reference-model` 与 `h-applied-delivery-evidence-conformance` 的 `push` 那一半，都绑定在 2026-11-18 或 2026-11-20 之后未再触碰、与 `main` 分别偏离 148、202、597 个提交的分支上。它们在 `main` 上从未产生过一次运行（`abr` 在 882 条样本里 0 次）。无论用哪台 runner，它们都该删。

## 7. 处置建议

### 7.1 应删（4 处改动，零风险，最先做）

| 项 | 理由 |
|---|---|
| `abr-forget-cross-owner-model.yml`（整个文件） | 非 main `push` 触发 → L1 永远 `DENY`；分支自 2026-11-18 起停滞；样本内 0 次运行 |
| `publication-protocol-reference-model.yml` —— 仅 `push:` 块 | 同上；分支自 2026-11-18 起停滞；PR 那一半值得保留 |
| `h-applied-delivery-evidence-conformance.yml` —— 仅 `push: session-h-bmcp-protocol` 块 | 同上；分支自 2026-11-20 起停滞 |
| `ai-owner-worker-bootstrap-labels.yml` | 一次性、幂等；它创建的标签要么已存在，要么试点没在跑 |

净效果：去掉 3 个非 main 触发器和 1 个一次性 workflow；`main` 上没有任何门禁失去覆盖。

### 7.2 合并（第二个做 —— 排队时间就是在这里省出来的）

| 合并 | 成员 | 结果 |
|---|---|---|
| M-1 `governance-gates` | `bilingual-docs`（PR）+ `document-management`（PR 与 main）+ `runner-admission-policy`（PR 与 main） | 一个 workflow、三个 job（或一个 job 跑三个脚本）。三者都是 `python3` + `fetch-depth: 0`，都不需要工具链 |
| M-2 `reference-models` | `aid-2026-001-reference-model` + `g-applied-reference-model` + `publication-protocol-reference-model` 的 PR 那一半 | 一个 job、三次 `unittest discover`。第三方 import 为零（AST 扫描确认：只有同目录模块） |

仅 M-1 就为每次 `push`→`main` 与每次 PR 同步去掉 2 个 job 槽位；M-2 再从 PR 上去掉 2 个。两者都完全不需要这台 runner —— 它们是纯粹的 `ubuntu-latest` 重构，因此可以在任何 runner 决策之前落地。

### 7.3 改造后迁（按此顺序）

| 顺序 | workflow（要迁的那一半） | 改标签前需要做的事 | 为何是这个顺序 |
|---|---|---|---|
| **P1** | `aid-2026-001-reference-model`（`push`→`main`）、`g-applied-reference-model`（`push`→`main`）—— 作为 M-2 | 除合并外无需其他改动。纯标准库，236 K 测试 | 以零依赖风险证明 runner 上的 `python3` 可用。若失败，其他一切都没有建立在假设之上 |
| **P2** | `document-management`（`push`→`main`）—— 作为 M-1 | 无需。纯标准库，本地 3.2 秒 | runner 上的第一个真实门禁。用实测校准第 8 节那个 30 秒模型 |
| **P3** | `aid-2026-001-manifest-validation`（`push`→`main`） | 预置 `PyYAML==6.0.2`（runner 侧 venv 或经白名单 egress 的 `pip install --user`），或改用脚本里已实现的纯标准库重复键检查 | 首个 `net` 先例。如果 egress 被挡，这里就是发现它的地方 —— 而且很便宜 |
| **P4** | `rust-phase1`（`push`→`main`） | 钉住工具链而非 `@stable`；让 `target/` 留在 checkout 路径内（`actions/checkout` 默认 `git clean -ffdx`，因此自限；路径之外是永久泄漏）；限制 `CARGO_BUILD_JOBS=2`；加一个 `df -h /` 前置守卫 | 收益最高（中位 45 秒、11 次成功），失败代价也最高（1 GB target、1.4 GiB 内存、6.8 GB 磁盘）。必须在 P1–P3 证明 runner 之后 |
| **P5** | `h-applied-delivery-evidence-conformance`（`workflow_dispatch` + `push`→`main`） | 预置 `jsonschema`/`rfc8785`/`cryptography`；决定 runner 上是否需要 `npm ci`，还是只跑 Python 那一半 | 最后：依赖面最宽，也是唯一同时需要 PyPI 与 npm 的 workflow |

**永不迁：** `runner-admission-policy`（审计器不能与被审计主机共享信任域）与 `ai-owner-worker`（被放行的 job 可以 `sudo`；这个持有 `contents: write` 并推分支）。

### 7.4 如果 Owner 选择放松 L1

若 Owner 决定 L1 可以在 `GITHUB_HEAD_REPO_FULL_NAME == GITHUB_REPOSITORY` 时接受 `pull_request`（同仓库 PR、无 fork），那么 8 个 PR 触发的门禁就变得可迁 —— 但 `audit_runner_admission.py` 必须在同一次提交里同步更新，否则 L2 会否决它本该放行的改动。这是对钩子、审计、8 个 workflow 文件的一次协同改动；不是逐 workflow 编辑，也不能分次做。

## 8. 串行约束的量化

### 8.1 成本模型

两个实测输入，分开列，因为来自不同机器：

- **每 self-hosted job 固定开销约 30 秒。** run `44986186138`：job `started 04:42:01` → `completed 04:42:26` = job 内 25 秒，其中唯一真实 step 运行于 `04:42:05` → `04:42:08` = 3 秒；此前还有 8 秒排队。`created` → `completed` 共 33 秒，换 3 秒工作。
- **每个 workflow 的工作时长** —— 882 条样本中托管 runner 的中位数（只取 `conclusion: success`）。这些是冷的托管运行，因此对 4 核 runner 而言是**下限**，不是估计。

| workflow | 中位数（托管） | n |
|---|---|---|
| `Bilingual documentation gate` | 10 秒 | 165 |
| `Rust Phase 1 Workspace Tests` | 45 秒 | 11 |
| `AID-2026-001 Manifest Validation` | 12 秒 | 3 |
| `AID-2026-001 Reference Model Tests` | 11 秒 | 1 |
| `G Applied Persistence Reference Model` | 10 秒 | 2 |
| `Publication Protocol Reference Model` | 10 秒 | 4 |
| `Architecture document management gate` | **样本内无成功**（89 次失败，3–4 秒，全部无 runner） | 0 |
| `Runner admission policy` | **样本内无成功**（90 次失败） | 0 |
| `H Applied Delivery Evidence Conformance` | **样本内无成功**（6 次失败） | 0 |

对没有托管成功记录的那三个，给出 16 核参考机上的本地 CPU 时间（标注：**不是** runner）：

| 脚本 | 本地墙钟 |
|---|---|
| `scripts/check_document_management.py` | 1 239 ms |
| `scripts/test_check_document_management.py` | 1 913 ms |
| `scripts/ci/audit_runner_admission.py` | 79 ms |
| `scripts/check_bilingual_docs.py` | 52 ms |

### 8.2 到达率

来自 882 条运行样本（2026-11-16 至 2026-11-21，5 个活跃日）：

- **239** 个不同的 `(branch, head_sha)` `pull_request` 组 = 239 次 PR 同步，承载 **566** 次 job 运行。
- 每次同步的 job 数：1 个 → 89 组，2 个 → 40，3 个 → 59，4 个 → 39，5 个 → 8，**6 个 → 4**。
- 每次同步的串行工作量（实测时长，托管）：中位 **11 秒**，p90 **42 秒**，最大 **83 秒**，均值 17.4 秒。
- **峰值小时 `2026-11-17T22:00`：100 次运行、38 次 PR 同步、1370 秒实测工作量。**

### 8.3 同一小时下的三种情景

单 runner 一小时容量 = `3600 / (30 秒开销 + 工作量)`。

| 情景 | 峰值小时 job 数 | 串行需求 | 容量 | 判定 |
|---|---|---|---|---|
| **12 个全按原样迁移** | 100 | 100 × 30 秒 + 1370 秒 = **4 370 秒 = 73 分钟** | 3 600 秒 | **超载 1.2 倍，队列无界增长。** 容量 82 job/小时，到达 100/小时 |
| **M-1 与 M-2 合并后全迁** | 100 −（2/同步 × 38）≈ 60 | 60 × 30 秒 + 1370 秒 ≈ 3 170 秒 = **53 分钟** | 3 600 秒 | 利用率 88% —— 这一小时能撑过，但对下一波没有余量 |
| **M-1 与 M-2 合并后，只迁 `push`→`main` 那一半** | 每次 `main` push 约 3 个（见 8.5） | 每次 push 约 1–2 分钟 | 3 600 秒 | 宽裕 |

**这就是「不该全迁」的量化依据。** 仅开销本身 —— 一个测试都没跑之前 —— 在未合并情形下是 `38 次同步 × 6 job × 30 秒 = 6 840 秒 = 114 分钟`每小时，是这台 runner 全部容量的 1.9 倍。`2026-11-17T22:00` 是样本峰值，不是最坏情况；一次 6 job 的 PR 同步、十分钟内推 20 次，就已经要排队半小时。

### 8.4 磁盘与内存的量化

- 在 `main @ 6de4e38c` 上冷跑 `cargo test --workspace --all-targets`：target 目录 **1009 MB**，编译 45 个 crate，在 16 核 / 5 GiB、`~/.cargo/registry` 已预热（319 MB、290 个缓存 crate）的机器上耗时 22–32 秒。
- runner 上 `/` 可用 **6.8 GB**。六个未清理的 target 目录就填满它。`actions/checkout` 清理 checkout 路径，不清理 `$HOME` 或 `/tmp`；`total_count: 1` 意味着下一 job 仍由同一台主机服务。
- runner 可用内存 **1.4 GiB**、**4** 核。参考机是 16 核 5 GiB。在那里 22–32 秒的构建，在这里不会是 22–32 秒；而 4 路并行 `rustc` 配 1.4 GiB 可用内存，是 OOM 候选，不是「慢一点」。
- `Cargo.lock` **未被跟踪**（`git ls-files Cargo.lock` 无匹配；`.gitignore` 里也没有对应条目）。每次运行都重新解析依赖版本，因此 registry 冷时每个 job 要下载约 290 个 crate，且相隔一周的两次运行不保证编译同一张依赖图。这是既有缺陷；迁移会让它更贵，但它本身不是迁移风险。

### 8.5 一次 `push`→`main` 今天 vs M-1 之后

今天，一次不带路径过滤的 `push`→`main` 会触发三个 workflow：`Runner admission policy`、`Architecture document management gate`、`Rust Phase 1 Workspace Tests`（实测：样本内 25 次 `main` push，每次 1–3 个 job，托管上并行，串行中位 8 秒）。

M-1 之后在 self-hosted 上串行化：`(30 + 0.1) + (30 + 3.2) + (30 + 45..120)` ≈ **140–210 秒，即每次 push 2.5–3.5 分钟**。可以接受。这也正是 P4（`rust-phase1`）必须排在 P1–P3 之后的原因：它是这个和式里的主导项。

## 9. 本记录无法做出的决策

| # | 决策 | 谁 | 为何不能作为工程默认值 |
|---|---|---|---|
| D-1 | L1 是否可以接受同仓库 `pull_request`？ | Owner | 放松它就移除了唯一阻止不可信触发器抵达具备 `sudo` 能力主机的控制。`observe.flag` 是应急回滚手段，且从未在生产中演练过 |
| D-2 | `runner-admission-policy` 是否应跑在被审计主机上？ | Owner / 治理 | 同一信任域内自我审计是结构性冲突，不是性能权衡 |
| D-3 | `ai-owner-worker` 是否允许在被放行 job 可 `sudo` 的主机上持有 `contents: write`？ | Owner | 这正是 L1 钩子为之而建的威胁；答案是风险接受，不是改标签 |
| D-4 | 是否出资增加第二台 runner？ | Owner | `total_count: 1` 是第 8 节的根因。一台带 `[self-hosted, linux, x64, ai-worker]` 的第二 runner 能让 PR 门禁与 `main` 门禁并发，从而彻底消除串行约束 |

在 D-1 与 D-4 有答案之前，正确的工程产出是：删掉死触发器（7.1）、合并重叠门禁（7.2）、迁移纯标准库的 `push`→`main` 那一半（7.3 的 P1 与 P2），然后停手。

## 10. 复现

```bash
# 1. runner 清单
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/actions/runners"

# 2. 能力探测（诊断 run 的日志归档）
curl -sL -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/actions/runs/44986186138/logs" \
  -o /tmp/logs.zip && unzip -o /tmp/logs.zip -d /tmp/logs
cat "/tmp/logs/diagnostics/3_Read-only host diagnostics.txt"

# 3. 无 runner job 的失败签名（steps == []）
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/actions/runs/44986264084/jobs" \
  | python3 -c 'import json,sys; [print(j["name"],j["conclusion"],len(j["steps"]),j["labels"],repr(j["runner_name"])) for j in json.load(sys.stdin)["jobs"]]'

# 4. 被守卫拒绝 job 的失败签名（4 个 step，step 2 失败）
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/actions/runs/44050069421/jobs" \
  | python3 -c 'import json,sys; [print([(s["number"],s["name"],s["conclusion"]) for s in j["steps"]]) for j in json.load(sys.stdin)["jobs"]]'

# 5. L2 对朴素改标签的否决
rm -rf /tmp/sim2 && mkdir -p /tmp/sim2/.github/workflows /tmp/sim2/scripts/ci
cp .github/workflows/*.yml /tmp/sim2/.github/workflows/
cp scripts/ci/audit_runner_admission.py /tmp/sim2/scripts/ci/
cd /tmp/sim2 && sed -i 's/runs-on: ubuntu-latest/runs-on: [self-hosted, linux, x64]/' .github/workflows/*.yml
python3 scripts/ci/audit_runner_admission.py; echo "exit=$?"   # 12 处违规，退出码 1
```

## 11. 非声明

- 本记录未修改任何 workflow 文件、`crates/` 源码、门禁脚本或 runner 配置。
- 不声称 runner 能否构建 Rust、运行 Node 或访问 PyPI（第 4 节 U-01 至 U-07）。
- 不声称这 12 个 workflow 是**正确**的；只声称它们能在哪里执行。
- `document-management` 今天在 `main` 上报 `INCOMPLETE`（593 个受治理文档、38 个已分类、555 个未分类）。这是既有积压，不是本记录的发现；此处记录仅为避免将来读者把它归因于本次迁移。
