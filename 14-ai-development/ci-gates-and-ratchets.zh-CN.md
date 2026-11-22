# CI 门禁与棘轮

**文档：** GATE-CI-001
**状态：** 生效 —— 已编写并在本地验证；尚未被观测到实际运行（见 §1）
**相关：** GAP-10 Tier 2 item 2（T2.2）、GAP-08、GAP-09、DOC-OPS-001、AI-RUN-002-RUNBOOK

本文说明 CI 运行哪些门禁、其中哪些是硬门禁、哪些是棘轮，以及棘轮基线的含义。
工作流为 `.github/workflows/gates.yml`，棘轮工具为 `scripts/ci/gate_ratchet.py`。

## 1. 这些 Job 尚未运行，本文不宣称它们运行过

`gates.yml` 中每个 Job 都固定在 `ubuntu-latest`。在本账户上，GitHub 托管运行分钟数
因账单失败被阻断：`main` 的分支保护返回 `403`，每个 check run 都带有注解
*"the job was not started because recent account payments have failed"*。
因此 `rust-phase1.yml` 在本仓库历史中从未执行过一个测试。

本项工作的状态确切地是：**工作流文件正确，且其中每一条命令都已在本地执行并记录了输出。**
这里没有任何内容是某个 check run 变绿的证据。请不要那样理解。

这些 Job 刻意**不**迁移到自托管 runner，有两条具约束力的规则阻止这么做：

* **L1（服务层）：** runner 的 job-started 钩子拒绝任何 ref 不是 `refs/heads/main` 的 Job。
  `pull_request` Job 在任何步骤执行前即以 `ref_not_default_branch` 被拒绝。
* **L2（仓库层）：** `scripts/ci/audit_runner_admission.py` 拒绝任何自托管 Job 使用 `pull_request`。

只能在合并之后运行的门禁不是门禁。因此这些 Job 留在托管 runner 上；当账单阻断解除时
它们会开始运行。

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

* **没有 `rust-toolchain.toml`，也没有 `rustfmt.toml`。** `rust` Job 使用
  `dtolnay/rust-toolchain@stable`，因此某个改变格式化的 rustfmt 版本可能在没有代码改动的情况下
  让 `cargo fmt --all --check` 变红。这一点被记录而不是被隐藏：`main` 上的格式漂移本身就是
  GAP-10 中反复出现的回归，所以该 Job 是硬门禁。固定工具链可以消除这个锋利边缘，是显而易见的
  下一步。
* **`cargo clippy` 需要 C 工具链**（用于 `libsqlite3-sys`）。它在托管 runner 上可以构建；
  没有 `cc1` 的本地 Windows 主机无法运行它。
* **`check_bilingual_docs_full.py` 读取工作树**，而不是 `git ls-files`。未跟踪的构建产物会
  改变它在本地的答案。CI 是干净检出，因此 CI 的答案是可复现的；本地答案未必是。

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

这是对工作流所运行命令的本地执行，不是一次绿色的 check run。见 §1。
