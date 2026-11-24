---
document_metadata:
  domain: ai-development
  role: guide
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
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "§2.3 的 clippy 理由已按 2026-11-23 的 GitHub Actions REST API 重新测量：rust-phase1.yml 现已在托管 runner 上执行 clippy，首次为 run 45037267638。所引 run id 与步骤结论均于本次会话从该 API 读取。"
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
    source: null
    en: null
    zh-CN: null
---
> **CI Runner 更新 — 2026-11-23：** 所有活动工作流现统一使用 GitHub 托管的 `ubuntu-latest` Runner。下文涉及自托管 Runner 拓扑、准入 Hook、磁盘回收或 Runner 队列的描述均为历史记录，不得作为当前运维指令。具体而言：自 #839 起，`gates.yml` 带 `main` 上的 `pull_request` 触发器，`scripts/ci/audit_runner_admission.py` 输出 `GitHub-hosted runner policy: 20 job(s) audited, 0 violation(s)` 并以退出码 0 结束。当前策略由 `.github/workflows/runner-admission-policy.yml` 强制检查。


# CI 门禁与棘轮

**文档：** GATE-CI-001
**状态：** 生效 —— 已编写并在本地验证；§1 说明哪些已被观测运行、哪些没有
**相关：** GAP-10 Tier 2 item 2（T2.2）、GAP-08、GAP-09、DOC-OPS-001、AI-RUN-002-RUNBOOK

本文说明 CI 运行哪些门禁、其中哪些是硬门禁、哪些是棘轮，以及棘轮基线的含义。
工作流为 `.github/workflows/gates.yml`，棘轮工具为 `scripts/ci/gate_ratchet.py`。

## 1. 这些 Job 在哪里运行，以及代价是什么

**当前状态（2026-11-23，#839）。** `gates.yml` 在 `main` 上由 `pull_request` 触发，也在 `push` 到
`main` 时触发，另加 `workflow_dispatch`；其五个 Job 全部为 `runs-on: ubuntu-latest`。它是合并前门禁。
以下段落描述的是它所替换掉的自托管拓扑；保留这些内容是因为它们解释了工作流为什么写成现在这样，而不是
因为它们描述着任何正在运行的东西。

本节其余部分是历史记录。在那套拓扑下，`gates.yml` 中每个 Job 都固定在
`runs-on: [self-hosted, linux, x64]`，而且这不是偏好问题。
`GET /repos/oahcom/AiMemoryBrainArchitecture/actions/runners` 当时返回
`total_count: 1`：只有一个 runner，名为 `zesu-x64`，标签为 `self-hosted, Linux, X64`。
本账户的 GitHub 托管分钟数曾因账单失败被阻断，所以写成 `runs-on: ubuntu-latest` 的 Job
**根本分配不到 runner**，并且以**空的 `steps` 数组**失败——它连第一步都到不了。2026-11-22T04:29:56Z
在 `main` 上的 `GOV-DOC-002 metadata checks` 与 `audit` 两个 Job 即为实例：都是 `failure`，
都是零步骤执行。本仓库 13 个工作流里有 12 个当时处于这个状态。在这里用 `ubuntu-latest` 编写的门禁
当时是死胎，因此那些 Job 指向唯一存在的那个 runner。

### 1.1 代价：它是合并后探测器，不是合并前门禁

> **历史。** 本小节记录的是 `gates.yml` 过去只由 `push` 触发的原因。账单阻断于 2026-11-22 解除，
> 自托管 runner 于 2026-11-23 由 #839 退役；该工作流现在带 `pull_request` 触发器（见 §1）。
> 以下内容均非当前行为。

两条当时生效的控制共同限定了触发条件：

* **L1（服务层）。** runner 的 job-started 钩子（`AI-RUN-002-RUNBOOK` §4.1）会让任何
  `GITHUB_REF` 不等于 `refs/heads/main`、或事件不是 `push` / `workflow_dispatch` / `schedule`
  的 Job 失败。功能分支上的 Job 在任何步骤执行前即被拒绝。
* **L2（仓库层）。** `scripts/ci/audit_runner_admission.py`（由 `runner-admission-policy.yml`
  强制执行）当时拒绝任何自托管 Job 使用不在白名单中的触发器，拒绝没有 `branches:` 过滤器的 `push`，
  以及拒绝 `push.branches` 中出现 `main` 以外的分支。

  在这次改动之前，L2 是一份**黑名单**，而 L1 是**白名单**。于是任何两张表都没列到的触发器——
  `issues`、`release`、`merge_group`、`discussion`，以及 GitHub 以后新加的——都会通过 L2，然后被 L1
  静默拒绝。一个被 L1 否定的绿色 L2 比没有 L2 更糟：那是一份宣称自己具备它并不具备的安全性的审计。
  L2 随后镜像了 L1 的白名单（`push`、`workflow_dispatch`、`schedule`），两者靠构造保持一致，而不是靠
  两张手工维护的表。当时已验证：自托管 Job 挂 `issues`、`merge_group`、`release`、`discussion` 都会被
  拒，报 `trigger '<x>' is not permitted for self-hosted jobs (L1 admits only push, schedule,
  workflow_dispatch)`；而仓库里真实的工作流审计是 7 个 Job / 0 违规。

  **#839 替换了那个脚本。** 自托管 runner 已不存在，触发器白名单没有东西可保护，所以
  `audit_runner_admission.py` 现在只检查一件事：每个工作流里的每个 Job 都是
  `runs-on: ubuntu-latest`（字面量，不是动态值，也不是含 `self-hosted` 的标签列表）。它在当前
  `main` 上打印 `GitHub-hosted runner policy: 20 job(s) audited, 0 violation(s)` 并退出 0。
  `trigger '<x>' is not permitted` 这条消息已不存在。

因此 `gates.yml` 当时只在 `push` 到 `main` 与 `workflow_dispatch` 时触发，别无其他。
**它无法对 pull request 设卡。** 它把"门禁在 `main` 上红着而无人知道"变成"门禁在 `main` 上红着，
并且几分钟内就有 check run 说出来"。这就是 GAP-10 的缺陷，也正是本工作流修掉的东西。
它当时不是合并前门禁，本文当时也不宣称它是。

当时合并前设卡需要以下三者之一，且都是 Owner 决策，而不是对本工作流的一次编辑：

1. GitHub 托管分钟数恢复（账单清除），或
2. 第二个 runner，使第一个不再是工作唯一可落地的位置，或
3. 放宽 L1/L2 策略，接受在一台具备 sudo 能力的主机上运行不可信 PR 代码的风险。

选项 1 已于 2026-11-22 发生，而 #839 据此行动：自托管 runner 已退役，`gates.yml` 在托管 runner 上
对 pull request 设卡。上面那个三选一的取舍已经关闭，不再悬而未决。

### 1.2 一个 runner 当时意味着串行化

> **历史。** 托管 runner 不是单一队列，所以这里描述的 `concurrency` 组已随 runner 在 #839 中移除。

单一 `concurrency` 组 `existing-gates-self-hosted`，配 `cancel-in-progress: false`，使多次运行
排队而不是重叠。同一次运行内的 Job 会自行在 runner 上排队。每个 Job 还带 `timeout-minutes`，
因为在一个单 runner 仓库里，一个卡死的 Job 阻塞的是整个仓库的每一个工作流，而不只是这一个。
`timeout-minutes` 这一限制在托管 runner 上保留；它当初补偿的那个队列已经不存在了。

### 1.3 自托管不是干净容器

> **历史。** 托管 Job 从全新的临时虚拟机启动，所以下面的绕行做法不再承重。它们被保留，是因为其中
> 好几条现在只是双保险，而不是必需的。

这些 Job 是针对这一现实写的，而不是假设一台全新虚拟机：

* **不用 `sudo`，不改主机。** Python 依赖装进 `$RUNNER_TEMP` 下的一次性 venv，runner 会在 Job
  之间清掉它。宿主解释器不被写入任何东西。没有 `rustup` 步骤：runner 由运维管理，一个会改动
  工具链的工作流会改动这台机器上其他所有 Job 看到的工具链。
* **依赖安装会降级，但从不跳过。** 若 venv 创建或 pip 安装失败，Job 会退回系统解释器，
  **前提是**它已满足 `jsonschema`、`rfc8785`、`cryptography`；否则带着缺失的包名失败。
  安装失败是"一条 warning 加一次真实运行"，绝不是静默通过。
* **只在真正热的地方复用热状态。** 当 `canonicalize` 已可解析时跳过 `npm ci`，不白白丢弃已在
  磁盘上的 `node_modules`。`target/` 是相反的情形：`actions/checkout` 默认执行 `git clean -ffdx`，
  所以位于 `$GITHUB_WORKSPACE` 内的 `target/` 每次运行都会被清掉并重建。在一台只剩 5.6G 的主机上
  这是正确的——工作区内的 `target/` 是自限的，而被指到 `/tmp` 或 `$HOME` 的那个会永久泄漏，因为
  checkout 清的是工作区，不是家目录。本文早期草稿曾声称 `target/` 是 runner 的构建缓存、永不清洗。
  那是错的，这里记录这次更正，而不是把它悄悄改掉。
* **刻意不用 `--offline`。** 冷 runner 的 registry 缓存是空的，`--offline` 会把"缺 crate"
  变成一条令人困惑的失败。代价是 `clippy` Job 需要 runner 为其他 Rust 工作本就具备的 crates.io 出口。

## 2. Job 清单

| Job | 门禁 | 命令 | 类型 |
|---|---|---|---|
| `protocol-index` | BMCP 消息索引 vs schema `message_type` 约束 | `python3 08-bmcp-protocol/scripts/check_protocol_index.py` | 硬门禁 |
| `conformance` | BMCP 一致性测试套件 | `python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance` | 硬门禁 |
| `schema-nonempty` | schema 非空约束审计 | `python3 08-bmcp-protocol/schemas/test_nonempty_audit.py` | 硬门禁 |
| `bilingual` | GOV-DOC-001 双语文档全量扫描 | `python3 scripts/check_bilingual_docs_full.py` | 棘轮 |
| `clippy` | Rust lint | `cargo clippy --workspace --all-targets -- -D warnings` | 硬门禁 |

### 2.1 为什么 `conformance` 是硬门禁

该套件需要两组依赖，二者都在运行前安装：

* `08-bmcp-protocol/tests/conformance/provider_outcome/requirements.txt`
  （`jsonschema`、`rfc8785`、`cryptography`）。
* 在 `08-bmcp-protocol/tests/conformance` 下执行 `npm ci`（`canonicalize@5.1.0`）。

两组依赖齐备后，该套件在 `main` 上完全通过：**585 个测试，跳过 27 个，0 失败，0 错误**。
若不安装 Node 依赖，三个跨语言向量测试会以 `ERR_MODULE_NOT_FOUND` 报错。那属于缺少依赖，
而不是门禁本身是红的——这正是把安装步骤写进 Job、而不是写成一句备注的原因。

因为该套件是通过的，所以它是硬门禁。若它是红的，它就会是棘轮。

### 2.2 为什么 `schema-nonempty` 现在是硬门禁，之前是棘轮

`gates.yml` 的早期版本把这个审计包在 `gate_ratchet.py` 里，配一份 5506 行的基线，因为当时 GAP-09
是开着的：schema 里存在 5506 条约束，而双语审计清单没有登记它们。

GAP-09 已在 `main` 上由 `6897e53c`（"audit the 30 unregistered schemas, closing GAP-09 gate"）
关闭：该提交把 `08-bmcp-protocol/schema-nonempty-audit.md` 从 135 行扩到 5582 行，登记了 32 个
schema 里的全部 5599 条约束。现在该审计在 `main` 上退出 0。

**绿了的门禁必须是硬门禁。** 继续保留棘轮，等于把基线文件变成一份长期豁免：Job 会报绿，而真正的
要求——永远不允许出现未登记的约束——根本没有被执行。因此包装器、基线文件和 Job 名里的 `(ratchet)`
三者一起删掉，Job 直接运行审计。

这是规则，不是特例：**门禁在变绿的那一天、由让它变绿的那同一个改动，从棘轮升为硬门禁。**
比它的红活得更久的棘轮，就是一份带排期的豁免。

### 2.3 为什么 `clippy` 不跑格式和测试

`main` 上的 `rust-phase1.yml` 已经在跑
`cargo test --workspace --all-targets --no-fail-fast` 与
`python3 scripts/check_fmt.py --expect "$GITHUB_SHA"`。本小节写作时该工作流是
`rust-self-hosted.yml`；#839 删除了那个文件，同样的两条命令留在 `rust-phase1.yml` 里。
在这里重复其中任何一项，都比什么都不做更糟：

* **两边的测试数会对不上，而且看起来绿的那个是错的。**
  `cargo test --workspace` 不跑 doctest，`--all-targets` 会跑。在同一棵树上实测：`--all-targets`
  → `passed=546 failed=0 ignored=1`，纯 `--workspace` → `passed=551 failed=0 ignored=1`。
  差的 5 个就是 doctest。GAP-10 §7.1 记录过同一个陷阱，当时是 371 vs 385。两个工作流对同一个提交
  报出不同的总数，等于两个数字都不可信，而**少跑却报成功**的那个恰恰是错的那个。
* **两个工作流在唯一一台 runner 上编译同一个 workspace，磁盘翻倍。**
  而这台主机的可用空间在**不构建**的运行之间都在缩（见 §5）。花两倍代价去换一个和另一个 Job
  互相矛盾的数字，是严格亏本的交易。

保留 `cargo clippy --workspace --all-targets -- -D warnings`，曾因为它是真正无人覆盖的：
`rust-phase1.yml` 里有 clippy，但它是 `runs-on: ubuntu-latest`，在本账户下当时根本分配不到
runner，因此从未执行过。clippy 曾是这个 Job 的独立价值。

**该前提已于 2026-11-22 失效。** 托管分钟恢复后，`rust-phase1.yml` 现在对每个触及 `crates/**`
的 `pull_request` 执行 clippy——首次观测为 run `45037267638`，`2026-11-22T15:15:13Z`，head
`38c3c975`，runner `GitHub Actions 1000005167`。它还会与本 Job 在**同一提交**上同时执行：
`d238dd4a` 与 `0dc8f5a2` 在本工作流与 `rust-phase1.yml` 中均为 clippy `success`。

因此这个 Job 现在是**刻意的冗余，而不是唯一覆盖**。两者不等价，差别是实测出来的：在
`6b97a659` 上，本 Job 在 `actions/checkout` 失败后 clippy 步骤为 `skipped`，而同一提交的
`rust-phase1.yml` clippy 为 `success`。删掉本 Job，clippy 结论就只剩一条依赖计费状态的工作流，
而计费状态在 2026-11-22 刚刚失败过一次。是否为两条腿付账是取舍决定，不是改注释能解决的。
测量见 `GOV-NC-2026-11-23-EXECUTION-RESTORED-029`。

后果已写进工作流本身：rustfmt 与测试套件**不**由 `gates.yml` 设卡，它们由 `rust-phase1.yml`
设卡。若那个工作流被删除，`clippy` Job 必须把它们加回来——并且要带 `--all-targets`。

## 3. 棘轮是什么，不是什么

`bilingual` 目前在 `main` 上是红的。GAP-08 记录了它如何变成这样：没有任何东西运行它，
因此没有任何东西发现它。

立刻把它变成硬门禁，会让每个 pull request 因作者并未造成的原因变红。这不会产生合规，
只会产生一个人人都学会忽略的检查——而这正是当初让该门禁红着进入 `main` 的失效模式。

棘轮改为钉住**当前失败项的确切集合**，并在该集合朝任一方向变化时失败：

1. **出现了不在基线中的失败** —— 回归。失败。
2. **基线中的某项不再失败** —— 基线已过期。同样失败。

第二条规则是让棘轮保持诚实的关键。没有它，基线会悄悄吸收已修复的项，变成永久的
一揽子豁免。有了它，修复某项就迫使作者在同一个 pull request 中下调基线。

**棘轮不是绿色豁免。** 它不是说门禁"允许是红的"，而是说"必须不比基线更差，并且必须
对此保持诚实"。

现在只剩一个棘轮。这不是应该追求的状态：每一个棘轮都是一笔记了名字的债，目标是把数量降到零。
`schema-nonempty` 已经走完了这段路（§2.2）。

## 4. 基线

基线是 `scripts/ci/baselines/` 下的文件，每行一个失败项，`#` 开始注释。

| 文件 | 项数 | 含义 |
|---|---|---|
| `scripts/ci/baselines/bilingual-docs.txt` | 81 | 缺少 `en` / `zh-CN` 对应件的规范路径 |

仅在失败集合确实发生变化时重新生成基线：

```bash
python3 scripts/check_bilingual_docs_full.py \
  | grep -E '^[0-9]{3}\. ' | sed -E 's/^[0-9]{3}\. //' | sed -E 's/ -> .*$//' \
  | sort -u > scripts/ci/baselines/bilingual-docs.txt
```

像 CI 那样在本地运行棘轮：

```bash
python3 scripts/ci/gate_ratchet.py \
  --baseline scripts/ci/baselines/bilingual-docs.txt \
  --format paths \
  --command "python3 scripts/check_bilingual_docs_full.py"
```

退出码 `0` 表示失败集合与基线完全一致。退出码 `1` 表示存在回归或基线过期；违规项会以
`::error::` 注解形式打印。

## 5. 已知的锋利边缘

* **没有 `rust-toolchain.toml`，也没有 `rustfmt.toml`。** `clippy` Job 使用 runner 上已安装的
  `cargo` / `cargo-clippy`，并打印它实际找到的版本。lint 是移动靶：某个 clippy 版本新增一条 lint
  就可能在没有代码改动的情况下让该 Job 变红。这一点被记录而不是被隐藏。格式不在此处设卡
  （见 §2.3），它由 `rust-phase1.yml` 的 `scripts/check_fmt.py` 设卡，后者会钉住它期望被
  格式化的那个提交 SHA。在仓库内固定工具链可以同时消除两者的锋利边缘，是显而易见的下一步。
* **`cargo clippy` 需要 C 工具链**（用于 `libsqlite3-sys`）。它在 runner 上可以构建；没有 `cc1`
  的本地 Windows 主机无法运行。其失效形态是一条 `cc1` 错误而非代码缺陷，Job 会原样报出而不是掩盖它。
* **磁盘是真实约束，而它的下限是实测出来的，不是猜的。** 在 `run 44992270090` 实测：39G 总量，
  已用 32G，**只剩 5.6G**，内存 3.6G，4 核。runner 运维在一台可比主机上实测：`cargo test
  --workspace --all-targets` 在 45 个 crate 上产出 **1009 MB** 的 `target/`，`~/.cargo/registry`
  在 290 个 crate 上是 **319 MB**。只跑 clippy 是同一批编译换一个 driver、且不链接测试二进制，
  含 registry 约 **1.0–1.3 GB**。

  因此 `clippy` Job 带一道**磁盘预检**，在低于 `GATES_MIN_FREE_GB`（默认 **3**）时拒绝，低于 6 时
  警告。该下限曾是 4，因为那时 Job 还跑 `cargo test` 并与 clippy 共用同一个 `CARGO_TARGET_DIR`
  （估算 1.7–2.0 GB）；测试步骤删掉后下限也随之下降——一个与 Job 不再匹配的下限是一个说谎的数字。
  为了跑绿而调低下限是禁止的；因为 Job 确实变小而调低，只是把账记对。

  **看趋势，不要只看数值。** 两次什么都不编译的诊断运行分别报告约 6.8G 和约 5.6G 可用：在没有任何
  构建的情况下累积了约 1.2 GB。在单 runner 上，最终一次性打死所有工作流的是这个漂移，而不是绝对值。

* **构建 profile 与并行度针对同一台主机钉死。** Job 级 `CARGO_PROFILE_DEV_DEBUG=0` /
  `CARGO_PROFILE_TEST_DEBUG=0` 去掉 debuginfo，那是那 1009 MB 里的大头，顺带降低链接内存。
  `CARGO_BUILD_JOBS=2`，因为主机 4 核但只有 3.6G 内存：默认 `-j 4` 在 45 个 crate 加一个 C 编译，
  是现实的 OOM 候选，而构建中途 OOM 比慢一点的构建是更糟的失败。

* **`Cargo.lock` 在本仓库未被跟踪**（`git ls-files` 无匹配，`.gitignore` 里也没写——既有缺陷）。
  因此每次运行都重新解析依赖：registry index 重拉、版本漂移就重下，约 290 个 crate。提交
  `Cargo.lock` 能砍掉这部分并让依赖集可复现。那是独立的一行改动，**不在此处做**，因为它超出 CI 接线
  的范围。
* **`check_bilingual_docs_full.py` 读取工作树**，而不是 `git ls-files`。未跟踪的构建产物会
  改变它在本地的答案。CI 是干净检出，因此 CI 的答案是可复现的；本地答案未必是。
* **棘轮的诚实度取决于评审者。** 回归会失败，过期基线也会失败，但没有东西能阻止有人从一棵更差的
  树上重新生成基线。缓解措施是：重新生成它会是某个文件的可见 diff，而那个文件存在的全部目的就是
  被阅读。

## 6. 证据

在 `6de4e38c`（本项工作起步时的提交）上记录：

| 门禁 | `6de4e38c` 上的结果 |
|---|---|
| `check_protocol_index.py` | 退出 0 —— `missing=0 extra=0 duplicate_types=0 invalid_rows=0`，`PASS` |
| 两组依赖齐备的 conformance | 退出 0 —— `Ran 585 tests`，`OK (skipped=27)` |
| `test_nonempty_audit.py` | 退出 1 —— 5506 个未登记约束（GAP-09，现已关闭） |
| `check_bilingual_docs_full.py` | 退出 1 —— 81 个未覆盖路径（GAP-08） |
| `cargo fmt --all --check` | 退出 0 |
| `cargo clippy --workspace --all-targets -- -D warnings` | 退出 0 |
| `cargo test --workspace` | 退出 0 |
| 两个基线上的 `gate_ratchet.py` | 退出 0 —— `regressions=0 fixed=0` |

那张表是历史：它是接线工作开始时的门禁状态，也是 `schema-nonempty` 最初被做成棘轮的原因。
它不是工作流现在的样子。

### 6.1 在 rebase 后的树上重新实测

本分支打开期间 `main` 前进过（`6897e53c` 关闭了 GAP-09；`#627` 加入了 `rust-self-hosted.yml`——
该文件后来由 #839 删除；`7d816980` 给 `rust-phase1.yml` 加了 fmt+clippy）。§2.2 与 §2.3 的两个
阻塞项都来自这次前进。rebase 后重新实测：

| 命令 | 结果 |
|---|---|
| `python3 08-bmcp-protocol/schemas/test_nonempty_audit.py` | 退出 0 —— `OK: 32 schemas; 5599 registered constraints; no unregistered or stale entries.` |
| `gate_ratchet.py --baseline .../bilingual-docs.txt` | 退出 0 —— `baseline=81 current=81 regressions=0 fixed=0`，`PASS` |
| `audit_runner_admission.py`（rebase 当时） | 退出 0 —— `7 self-hosted job(s) audited, 0 violation(s)` |
| `cargo test --workspace --all-targets`（在 `main` 上） | `passed=546 failed=0 ignored=1` |
| `cargo test --workspace`（在 `main` 上） | `passed=551 failed=0 ignored=1` |

最后两行就是 §2.3 的全部论据：同一提交、同一 workspace、五个不同的测试，而两条命令里只有一条是
`main` 真正在跑的那条。审计那一行是 rebase 当时（2026-11-22）的输出；在当前 `main` 上，同一个脚本
打印 `GitHub-hosted runner policy: 20 job(s) audited, 0 violation(s)` 并退出 0。

这是对工作流所运行命令的本地执行。它是关于门禁的证据，不是关于工作流执行的证据。
§7 记录工作流自身做了什么。

## 7. 实际观测到什么

> **历史记录（2026-11-22）。** 本节所有观测都是在 #839 于 2026-11-23 退役自托管 runner **之前**、
> 针对那个 runner 做的。run id、标签与主机参数都是那套拓扑的真实记录；其中没有任何一条描述当前的
> GitHub 托管环境。当前的实测输出是 `GitHub-hosted runner policy: 20 job(s) audited, 0 violation(s)`，
> 退出 0（见 §1）。

### 7.1 runner 会接活，标签也对得上

对 `main` 派发 `ubuntu-worker-diagnostics.yml`，得到 **run 44992270090**（`success`）：

```
job: diagnostics | completed success
  runner_name: 'zesu-x64'
  labels: ['self-hosted', 'linux', 'x64']
  started: 2026-11-22T06:06:59Z -> completed: 2026-11-22T06:07:25Z
  steps: 4 —— Set up job、Set up runner、Read-only host diagnostics、Complete job
```

当时 `runs-on: [self-hosted, linux, x64]` 是正确的选择器：这样写的 Job 会被接纳并执行。它报告的
环境（该自托管 runner 已不存在，这些数值仅作历史记录）：

| 事实 | 值 |
|---|---|
| OS / 内核 | Ubuntu 26.04 / Linux 7.0.0-30-generic，x86_64 |
| CPU / 内存 | 4 核 / 3.6Gi |
| `/` 磁盘 | 39G 总量，已用 32G，**只剩 5.6G** |
| runner 账号 | `ubuntu`，属于 `sudo` 组 |
| L1 钩子 | 已安装；`guard.log` 存在，末行 `ALLOW ref=refs/heads/main event=workflow_dispatch` |

### 7.2 L1 确实会拒绝非 `main` 的 ref（负向测试）

同一个工作流，以 `ref=feat/t22-ci-gates` 派发，得到 **run 44992485707**（`failure`）。日志：

```
##[group]Run '/home/ubuntu/actions-runner/hooks/job-started-guard.sh'
runner admission guard: DENY reason=ref_not_default_branch
```

钩子在第一个用户步骤之前就拒绝了该 Job。这正是 `gates.yml` 在自托管 runner 存在期间不带
`pull_request` 触发器的原因，而且当时这是实测而非推断。它不是当前状态：#839 退役了该 runner，
`gates.yml` 现在带 `main` 上的 `pull_request` 触发器（见 §1）。

### 7.3 L2 确实会拒绝一个「PR 设卡版」所需的形态

`scripts/ci/audit_runner_admission.py` 对 `gates.yml`：**审计 7 个自托管 Job，0 违规，退出 0**
（当时是这里 5 个加上已被 #839 删除的 `rust-self-hosted.yml` 与既有的 diagnostics Job）。
对一个故意写错的探针工作流，它报出的正是预期的两条违规，退出 1：

```
::error::.github/workflows/zz-probe.yml:probe: untrusted trigger 'pull_request' is not permitted for self-hosted jobs
::error::.github/workflows/zz-probe.yml:probe: on.push.branches includes non-main branch 'feat/t22-ci-gates'
```

该脚本此后由 #839 改写：自托管 Job 已不存在，白名单审批无从谈起，它现在只检查每个工作流里的每个 Job
都是 `runs-on: ubuntu-latest`，在当前 `main` 上审计 20 个 Job、0 违规并退出 0。上面的探针输出是
改写前脚本的行为记录，不是当前脚本会输出的内容。

### 7.4 步骤体是被执行过的，不只是被解析过

`gates.yml` 里每一个 `run:` 块都被抽出来，在 Linux（Ubuntu 24.04、python 3.12、cargo 1.95.0、
node 22）上以 `bash --noprofile --norc -e -o pipefail` 执行，并按 runner 的方式设置了
`RUNNER_TEMP`。结果：

| Job | 步骤 | 结果 |
|---|---|---|
| `protocol-index` | 协议索引 | 退出 0，`missing=0 extra=0 duplicate_types=0 invalid_rows=0`，`PASS` |
| `conformance` | venv 依赖安装（真实脚本） | 退出 0，`using venv at /tmp/rt/gates-venv`，venv 满足 `jsonschema`/`rfc8785`/`cryptography` |
| `conformance` | 通过该 venv 跑完整套件 | 退出 0，`Ran 585 tests`，`OK (skipped=27)` |
| `schema-nonempty` | 硬门禁审计 | 退出 0，`OK: 32 schemas; 5599 registered constraints` |
| `bilingual` | 棘轮 | 退出 0，`baseline=81 current=81 regressions=0 fixed=0` |
| `clippy` | 磁盘预检 | 在 721G 可用的主机上退出 0（拒绝路径见 §7.5） |
| `clippy` | 工具链存在性 | 退出 0，`cargo 1.95.0`、`rustc 1.95.0`、`clippy 0.1.95` |
| `clippy` | `cargo clippy --workspace --all-targets -- -D warnings` | 退出 0 |

其中两项值得单独点出，因为它们是唯一可能被伪造的部分。venv 脚本是按原文执行的，并在一个系统 python
受 PEP-668 外部管理的主机上产出了具备三个固定导入的可用解释器——也就是「直接 `pip install` 会失败」
的那个场景。而 conformance 套件是**通过那个 venv** 跑的，不是通过碰巧已安装的东西跑的，所以 585 这个
结果是该 Job 会得到的结果。

`clippy` 这几行来自更早那个更大的 Job（fmt + clippy + test）。fmt 与 test 步骤随后被删除（§2.3），
所以只有磁盘预检、工具链探测和 clippy 这三行仍然描述着实际存在的步骤。clippy 步骤的实测结果没有变化
——同一棵树上的同一条命令。

### 7.5 磁盘预检会拒绝，这是故意的，而且阈值是实测出来的

预检对模拟文件系统做过实测。当前下限 3G，警告线 6G：

| 可用空间 | 下限 3、警告 6（当前） |
|---|---|
| 2G | 退出 1 —— `::error::only 2G free (2597152 KiB), below the 3G floor.` |
| 3G | 退出 0 —— `::warning::only 3G free; shrinking between runs that build nothing.` |
| 5.6G（runner 的实测值） | 退出 0 —— 会告警，因为 `df` 的 KiB 被截断为整 GiB，5.6 报成 5 |
| 6G | 退出 0 —— 静默 |
| 9G | 退出 0 —— 静默 |

本表早期版本显示 5.6G 会被拒绝，因为当时下限是 6G。那个下限是错的：实测该 Job 的成本是
2.0–2.5 GB，所以 5.6G 够用，拒绝它只会造出一个理由不成立的红门禁。下限随后降到 4G，又在删掉测试
步骤、Job 变小之后降到 3G。两次更正都被记录下来了，不是悄悄改掉的。

`5.6G` 那行的告警是截断造成的假象，不是真实信号：`df -Pk` 报的是 KiB，脚本除成整 GiB，5.6 向下取整
成 5，低于 6G 的警告线。两种情况都是退出 0。保留这种截断而不向上取整是刻意的——一个朝宽松方向取整的
下限比较，就是下限不再是下限的开始。

### 7.6 写作时仍未被观测到的

> **历史（2026-11-22）。** 本小节记录的是一个已不再成立的状态：`gates.yml` 现已在 `main` 上
> （#839 合并），并带 `pull_request` 触发器，所以这里残留的问题已经关闭。下面两行探针保留下来，
> 作为「派发解析是如何被实测的」记录；其中被点名的 `ubuntu-worker-diagnostics.yml` 已被 #839 删除，
> 现在根本无法派发。

写作当时，`gates.yml` 自身**在任何分支上都还没有 check run**，而且它无法从功能分支按需触发：GitHub 会针对
**默认分支**解析 `POST /actions/workflows/gates.yml/dispatches`，而当时 `gates.yml` 不在 `main` 上。
当时实测：

```
gates.yml@feat/t22-ci-gates -> HTTP 404 (Not Found)
ubuntu-worker-diagnostics.yml@feat/t22-ci-gates -> HTTP 204 (accepted)
```

第二行当时是对照：对一个**确实在** `main` 上的工作流，派发是成功的。因此这五个 Job 的首次运行取决于
该文件能否到达 `main`——#839 通过把它合并进去做到了这一点。§7.4 的证据仍然是「对精确步骤体的执行」，
而不是一条被引用出来的绿色 check run，本文也不把它当作那样来呈现。
