# CI 门禁与棘轮

**文档：** GATE-CI-001
**状态：** 生效 —— 已编写并在本地验证；§1 说明哪些已被观测运行、哪些没有
**相关：** GAP-10 Tier 2 item 2（T2.2）、GAP-08、GAP-09、DOC-OPS-001、AI-RUN-002-RUNBOOK

本文说明 CI 运行哪些门禁、其中哪些是硬门禁、哪些是棘轮，以及棘轮基线的含义。
工作流为 `.github/workflows/gates.yml`，棘轮工具为 `scripts/ci/gate_ratchet.py`。

## 1. 这些 Job 在哪里运行，以及代价是什么

`gates.yml` 中每个 Job 都固定在 `runs-on: [self-hosted, linux, x64]`。

这不是偏好问题。`GET /repos/oahcom/AiMemoryBrainArchitecture/actions/runners` 返回
`total_count: 1`：只有一个 runner，名为 `zesu-x64`，标签为 `self-hosted, Linux, X64`。
本账户的 GitHub 托管分钟数因账单失败被阻断，所以写成 `runs-on: ubuntu-latest` 的 Job
**根本分配不到 runner**，并且以**空的 `steps` 数组**失败——它连第一步都到不了。2026-11-22T04:29:56Z
在 `main` 上的 `GOV-DOC-002 metadata checks` 与 `audit` 两个 Job 即为实例：都是 `failure`，
都是零步骤执行。本仓库 13 个工作流里有 12 个处于这个状态。在这里用 `ubuntu-latest` 编写的门禁
是死胎，因此这些 Job 指向唯一存在的那个 runner。

### 1.1 代价：这是合并后探测器，不是合并前门禁

两条已经生效的控制共同限定了触发条件：

* **L1（服务层）。** runner 的 job-started 钩子（`AI-RUN-002-RUNBOOK` §4.1）会让任何
  `GITHUB_REF` 不等于 `refs/heads/main`、或事件不是 `push` / `workflow_dispatch` / `schedule`
  的 Job 失败。功能分支上的 Job 在任何步骤执行前即被拒绝。
* **L2（仓库层）。** `scripts/ci/audit_runner_admission.py`（由 `runner-admission-policy.yml`
  强制执行）拒绝任何自托管 Job 使用 `pull_request`，拒绝没有 `branches:` 过滤器的 `push`，
  以及拒绝 `push.branches` 中出现 `main` 以外的分支。

因此 `gates.yml` 只在 `push` 到 `main` 与 `workflow_dispatch` 时触发，别无其他。
**它无法对 pull request 设卡。** 它把"门禁在 `main` 上红着而无人知道"变成"门禁在 `main` 上红着，
并且几分钟内就有 check run 说出来"。这就是 GAP-10 的缺陷，也正是本工作流修掉的东西。
它不是合并前门禁，本文也不宣称它是。

合并前设卡需要以下三者之一，且都是 Owner 决策，而不是对本工作流的一次编辑：

1. GitHub 托管分钟数恢复（账单清除），或
2. 第二个 runner，使第一个不再是工作唯一可落地的位置，或
3. 放宽 L1/L2 策略，接受在一台具备 sudo 能力的主机上运行不可信 PR 代码的风险。

### 1.2 一个 runner 意味着串行化

单一 `concurrency` 组 `existing-gates-self-hosted`，配 `cancel-in-progress: false`，使多次运行
排队而不是重叠。同一次运行内的 Job 会自行在 runner 上排队。每个 Job 还带 `timeout-minutes`，
因为在一个单 runner 仓库里，一个卡死的 Job 阻塞的是整个仓库的每一个工作流，而不只是这一个。

### 1.3 自托管不是干净容器

这些 Job 是针对这一现实写的，而不是假设一台全新虚拟机：

* **不用 `sudo`，不改主机。** Python 依赖装进 `$RUNNER_TEMP` 下的一次性 venv，runner 会在 Job
  之间清掉它。宿主解释器不被写入任何东西。没有 `rustup` 步骤：runner 由运维管理，一个会改动
  工具链的工作流会改动这台机器上其他所有 Job 看到的工具链。
* **依赖安装会降级，但从不跳过。** 若 venv 创建或 pip 安装失败，Job 会退回系统解释器，
  **前提是**它已满足 `jsonschema`、`rfc8785`、`cryptography`；否则带着缺失的包名失败。
  安装失败是"一条 warning 加一次真实运行"，绝不是静默通过。
* **热状态被复用，但不被信任。** 当 `canonicalize` 已可解析时跳过 `npm ci`，不白白丢弃已热的
  `node_modules`。`target/` 永不清洗——在单 runner 上它是唯一的构建缓存——但没有任何东西依赖它存在。
* **刻意不用 `--offline`。** 冷 runner 的 registry 缓存是空的，`--offline` 会把"缺 crate"
  变成一条令人困惑的失败。代价是 `rust` Job 需要 runner 为其他 Rust 工作本就具备的 crates.io 出口。

## 2. Job 清单

| Job | 门禁 | 命令 | 类型 |
|---|---|---|---|
| `protocol-index` | BMCP 消息索引 vs schema `message_type` 约束 | `python3 08-bmcp-protocol/scripts/check_protocol_index.py` | 硬门禁 |
| `conformance` | BMCP 一致性测试套件 | `python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance` | 硬门禁 |
| `schema-nonempty` | schema 非空约束审计 | `python3 08-bmcp-protocol/schemas/test_nonempty_audit.py` | 棘轮 |
| `bilingual` | GOV-DOC-001 双语文档全量扫描 | `python3 scripts/check_bilingual_docs_full.py` | 棘轮 |
| `rust` | 格式、lint、测试 | `cargo fmt --all --check`、`cargo clippy --workspace --all-targets -- -D warnings`、`cargo test --workspace` | 硬门禁 |

### 2.1 为什么 `conformance` 是硬门禁

该套件需要两组依赖，二者都在运行前安装：

* `08-bmcp-protocol/tests/conformance/provider_outcome/requirements.txt`
  （`jsonschema`、`rfc8785`、`cryptography`）。
* 在 `08-bmcp-protocol/tests/conformance` 下执行 `npm ci`（`canonicalize@5.1.0`）。

两组依赖齐备后，该套件在 `main` 上完全通过：**585 个测试，跳过 27 个，0 失败，0 错误**。
若不安装 Node 依赖，三个跨语言向量测试会以 `ERR_MODULE_NOT_FOUND` 报错。那属于缺少依赖，
而不是门禁本身是红的——这正是把安装步骤写进 Job、而不是写成一句备注的原因。

因为该套件是通过的，所以它是硬门禁。若它是红的，它就会是棘轮。

## 3. 棘轮是什么，不是什么

`schema-nonempty` 与 `bilingual` 目前在 `main` 上是红的。GAP-09 与 GAP-08 记录了它们
如何变成这样：没有任何东西运行它们，因此没有任何东西发现它们。

立刻把它们变成硬门禁，会让每个 pull request 因作者并未造成的原因变红。这不会产生合规，
只会产生一个人人都学会忽略的检查——而这正是当初让这些门禁红着进入 `main` 的失效模式。

棘轮改为钉住**当前失败项的确切集合**，并在该集合朝任一方向变化时失败：

1. **出现了不在基线中的失败** —— 回归。失败。
2. **基线中的某项不再失败** —— 基线已过期。同样失败。

第二条规则是让棘轮保持诚实的关键。没有它，基线会悄悄吸收已修复的项，变成永久的
一揽子豁免。有了它，修复某项就迫使作者在同一个 pull request 中下调基线。

**棘轮不是绿色豁免。** 它不是说门禁"允许是红的"，而是说"必须不比基线更差，并且必须
对此保持诚实"。

## 4. 基线

基线是 `scripts/ci/baselines/` 下的文件，每行一个失败项，`#` 开始注释。

| 文件 | 项数 | 含义 |
|---|---|---|
| `scripts/ci/baselines/schema-nonempty.txt` | 5506 | 未登记在双语审计清单中的 schema 约束 |
| `scripts/ci/baselines/bilingual-docs.txt` | 81 | 缺少 `en` / `zh-CN` 对应件的规范路径 |

仅在失败集合确实发生变化时重新生成基线：

```bash
python3 08-bmcp-protocol/schemas/test_nonempty_audit.py \
  | sort -u > scripts/ci/baselines/schema-nonempty.txt

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

* **没有 `rust-toolchain.toml`，也没有 `rustfmt.toml`。** `rust` Job 使用 runner 上已安装的
  `cargo` / `rustfmt`，并打印它实际找到的版本，因此某个改变格式化的 rustfmt 版本可能在没有代码
  改动的情况下让 `cargo fmt --all --check` 变红。这一点被记录而不是被隐藏：`main` 上的格式漂移
  本身就是 GAP-10 中反复出现的回归，所以该 Job 是硬门禁。在仓库内固定工具链可以消除这个锋利
  边缘，是显而易见的下一步。
* **`cargo clippy` 与 `cargo test` 需要 C 工具链**（用于 `libsqlite3-sys`）。它们在 runner 上
  可以构建；没有 `cc1` 的本地 Windows 主机无法运行。其失效形态是一条 `cc1` 错误而非代码缺陷，
  Job 会原样报出而不是掩盖它。
* **`check_bilingual_docs_full.py` 读取工作树**，而不是 `git ls-files`。未跟踪的构建产物会
  改变它在本地的答案。CI 是干净检出，因此 CI 的答案是可复现的；本地答案未必是。
* **棘轮的诚实度取决于评审者。** 回归会失败，过期基线也会失败，但没有东西能阻止有人从一棵更差的
  树上重新生成基线。缓解措施是：重新生成它会是某个文件的可见 diff，而那个文件存在的全部目的就是
  被阅读。

## 6. 证据

在 `6de4e38c`（本项工作所基于的提交）上记录：

| 门禁 | 结果 |
|---|---|
| `check_protocol_index.py` | 退出 0 —— `missing=0 extra=0 duplicate_types=0 invalid_rows=0`，`PASS` |
| 两组依赖齐备的 conformance | 退出 0 —— `Ran 585 tests`，`OK (skipped=27)` |
| `test_nonempty_audit.py` | 退出 1 —— 5506 个未登记约束（GAP-09） |
| `check_bilingual_docs_full.py` | 退出 1 —— 81 个未覆盖路径（GAP-08） |
| `cargo fmt --all --check` | 退出 0 |
| `cargo clippy --workspace --all-targets -- -D warnings` | 退出 0 |
| `cargo test --workspace` | 退出 0 |
| 两个基线上的 `gate_ratchet.py` | 退出 0 —— `regressions=0 fixed=0` |

这是对工作流所运行命令的本地执行，且在与工作流相同的提交上。它是关于门禁的证据，不是关于工作流
执行的证据。§7 记录工作流自身做了什么。
