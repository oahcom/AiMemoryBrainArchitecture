# E1–E8 Engineering Entry Gate Measurement

**测量日期：** 2026-11-21  
**测量对象：** 工程准入包 E1–E8  
**记录性质：** 证据状态测量，不构成 Owner 裁定或授权  
**规则：** E1–E8 为合取条件；缺失或仅凭推断的字段均不得视为满足。

## §1 逐项测量表

| Gate | 当前实测状态 | 证据（精确到仓库路径/commit/SHA/Issue 评论 ID） | 缺口（缺什么才算满足） | 应供方 |
|---|---|---|---|---|
| E1 — Canonical Runtime repository and active branch | `PARTIALLY-EVIDENCED` | 用户提供并实测：开发仓库 `https://github.com/oahcom/AiMemoryBrain`，默认分支 `main`，当前 HEAD 为 `2a20ba1181509106532bbd4fc156bdc45f2f2101`。GitHub 仓库元数据确认默认分支为 `main`；该 commit 可读取，提交记录为合并 PR #14。`AiMemoryBrain/AiMemoryBrain/Cargo.toml`（仓库内路径 `AiMemoryBrain/Cargo.toml`）确认 crate 名称 `d_unicode_validator`、edition `2024`。架构仓 Issue #7 评论 `7021990583` 记录了此前的 implementation binding 延期和工程准入要求。 | 缺少仓库内权威的 **repository purpose and authority record**：明确该仓库是 Canonical Runtime、其用途与边界、指定分支及其授权来源，并与架构仓 Issue #7 的工程阶段交接记录一致。仓库 URL、分支和 HEAD 本身不能替代该权威记录。 | Project authority |
| E2 — Engineering responsibility | `NOT ESTABLISHED` | 本轮可读取的 Issue #7 评论 `7021990583` 要求指定 accountable engineering lead 和各模块 maintainers；评论列出了需负责的范围，但没有提供完整、可核验的具名任命清单。未取得满足 E2 要求的仓库内权威任命载体。 | 需要具名 engineering lead，以及 D Runtime、Producer Registration Ledger、ForgetFence、Storage integration 和 CI 的具名 maintainers；需记录各自职责范围、授权依据及接受责任的证据。不能从提交者、评论者或工具账户身份推定任命。 | Engineering leadership |
| E3 — Write and custody authority | `PARTIALLY-EVIDENCED` | 用户口头授权（无仓库内载体）：①「https://github.com/oahcom/AiMemoryBrain 这个就是开发的仓库，需要什么跟我说」；②「代码必须在远端43服务器开发哈」；③「我觉得你不用自己弄，让ChatGPT弄，它更稳对项目更了解」。用户提供的 ruleset 实测：规则集 `27711552`「保护分支」要求 status check `Governance structural checks`，`bypass_actors: []`，`current_user_can_bypass: never`。这些信息分别表明用户表达了开发仓库和远端开发环境意向，以及当前 ruleset 没有 bypass actor；它们不等于仓库内可审计的路径写入与 custody 授权记录。 | 缺少仓库内明确授权载体，列明 D Owner / implementers 获准写入的仓库、分支、目录和文件范围，写入方式、审查/合并责任及 custody 边界；还需提供相应 maintainer 权限的可核验证据。口头授权不能替代可审计的授权记录；ruleset 的 bypass 限制也不能被解释为已授予绕过权限。 | Project authority + repository administrator |
| E4 — Persistence and serialization boundary | `NOT ESTABLISHED` | 本轮未取得可证明 authoritative Producer Registration Ledger/store、transaction domain、durability/WAL boundary、linearization point 和 recovery owner 的权威仓库载体。Issue #7 评论 `7021990583` 将 build/deployment/topology 等工程阶段事实列为待提供事项，但不能据此推定具体持久化边界。 | 需要明确权威 Producer Registration Ledger/store、事务域、持久化与 WAL 边界、线性化点、故障恢复责任人；应由权威设计记录、存储配置/实现路径及可验证的恢复证据共同支撑。SQLite 或其他参考模型不能单独满足该门。 | D Owner + Storage Owner + engineering lead |
| E5 — Callable authority surface | `NOT ESTABLISHED` | 本轮未取得已接受的 D-002 proof pack 中五个 D operational operations 的完整、权威定义及实现绑定证据。未将通用接口、schema 或 validator 推定为可调用的 authority surface。 | 需要逐项给出五个操作的精确名称、request/response 类型、认证 principal、错误与 UNKNOWN 语义、操作责任人，并与已接受的 D-002 proof pack 对应。 | D Owner |
| E6 — Build and verification custody | `PARTIALLY-EVIDENCED` | 用户提供的独立实测：仓库 `oahcom/AiMemoryBrain`，HEAD `2a20ba1181509106532bbd4fc156bdc45f2f2101`；crate 路径 `AiMemoryBrain/`，Rust `d_unicode_validator`，edition 2024；`cargo build --offline --lib` 和 `cargo build --offline --tests` 在 `CARGO_TARGET_DIR` 下离线成功；`cargo test --offline` 为 89 passed / 0 failed / 0 ignored（74 lib + 3 + 1 + 7 + 3 + 1）。本轮读取 `.github/workflows/governance-gate.yml`：只有 `Governance Gate` workflow，job `Governance structural checks`，执行 `python3 scripts/governance_gate.py`，工作目录为 `AiMemoryBrain`。该 workflow 是治理结构检查，不是 build/test workflow。新增 CI 证据：开发仓库 `.github/workflows/build-and-test.yml` 已通过 PR #15 落地，merge commit `480ce4e6cf53225fc381f83725fec3bbcf13f73c`；`Build and Test` run_id `44880135760`，conclusion `success`，9 个业务步骤全部 success；artifact `build-test-evidence-56f642b6cbcb628eeba9bc94ccd850be81bb1778`，4599 字节，90 天保留；`Governance Gate` run_id `44880135506`，conclusion `success`。 | CI 已存在并成功运行一次，但仍缺：该 CI 被正式纳入准入包、artifact 留存责任人与保留策略的书面确认、以及跨多次提交的稳定性证据（目前仅一次 run） | Engineering leadership |
| E7 — Deployment and trust boundary | `NOT ESTABLISHED` | 本轮未取得权威服务拓扑、principal/key registry、密钥轮换/撤销、网络/传输、replicas、backup/restore 和 operator boundary 的完整证据。Issue #7 评论 `7021990583` 将 deployed service topology and environments 列为工程准入前需提供的事实。 | 需要可审计的部署拓扑与环境清单，覆盖 coordinator、canonical DB、object store、index/cache、queues、replicas、backup/restore、recipient adapters；同时记录 principal/key registry、轮换与撤销机制、网络/传输边界及 operator 权限边界。 | Engineering leadership + D Owner + Storage Owner |
| E8 — Traceability | `NOT ESTABLISHED` | 本轮未取得 D-002 与 D 1.3.1 条款到实际实现路径、测试、fault hooks 和 operational evidence 的完整 contract-to-code map。Issue #7 评论 `7021990583` 要求提供 contract-to-code traceability owner/process 和实际模块、fault hooks、executable tests 的映射，但该要求本身不是映射已完成的证据。 | 需要逐条映射 D-002 与 D 1.3.1 条款到实现文件/模块、可执行测试、故障注入点和运行证据；明确映射维护责任人、更新流程及独立核验方式。 | D Owner + engineering lead |

### 测量说明

1. `PARTIALLY-EVIDENCED` 表示存在可识别的部分证据，但至少一个准入必需字段仍缺失；不得按满足处理。
2. `NOT ESTABLISHED` 表示本轮没有取得足以证明该门满足的证据，不等于断言相关事实绝对不存在。
3. E1 的仓库 URL、默认分支和精确 HEAD 已有证据，但缺少 repository purpose and authority record，因此不能标记 `ESTABLISHED`。
4. E3 的用户口头授权和 ruleset 状态均如实记录；口头授权没有仓库内载体，且 ruleset 没有 bypass actor，因此不能标记 `ESTABLISHED`。
5. E6 的命令级构建/测试结果来自用户提供的独立实测；本轮读取到的 CI workflow 只执行治理结构检查，没有 build/test workflow，因此不能标记 `ESTABLISHED`。
6. 对 E2、E4、E5、E7、E8，本轮没有取得满足准入要求的权威证据，不以角色推断、接口猜测、参考实现或搜索缺失替代证据。

### 本轮新增证据（2026-11-21）

以下为截至本次测量时点（2026-11-21）新增取得的开发仓库 CI 证据：

- 开发仓库 `oahcom/AiMemoryBrain` 的 `.github/workflows/build-and-test.yml` 已通过 PR #15 落地，merge commit 为 `480ce4e6cf53225fc381f83725fec3bbcf13f73c`。
- `Build and Test` workflow run_id `44880135760`，conclusion 为 `success`，9 个业务步骤全部 success。
- 成功运行生成 artifact：`build-test-evidence-56f642b6cbcb628eeba9bc94ccd850be81bb1778`，大小 4599 字节，保留期 90 天。
- 同一测量时点，`Governance Gate` workflow run_id `44880135506`，conclusion 为 `success`。
- 上述 CI 事实补充了 E6 的自动化构建与测试证据，但**不改变 E6 的 `PARTIALLY-EVIDENCED` 状态**。该 CI 尚未正式纳入工程准入包，artifact 留存责任人与保留策略尚无书面确认，且目前只有一次成功 run，尚无跨多次提交的稳定性证据。

## §2 合取结论

E1–E8 是合取条件，必须八项全部达到 `ESTABLISHED` 才能满足工程准入。

本轮测量结果为：

- `PARTIALLY-EVIDENCED`：E1、E3、E6。
- `NOT ESTABLISHED`：E2、E4、E5、E7、E8。
- `ESTABLISHED`：无。

**当前 E1–E8 未全部 ESTABLISHED，因此工程准入未满足。**

本文件只记录现有证据和缺口，不宣布可以开工，不授予任何开发权限，也不将部分证据转换为授权或准入通过。

## §3 与 G8 的关系

`g8-seven-conditions-evidence-map.md` §二的判定为：**G8 七项条件全部是架构验收前置，无一为开发开工准入。**

`development-readiness-register.md` 第 50 行记录 G8 为 `NOT READY`，并标记 `DOES-NOT-BLOCK`。

据此，G8 与 E1–E8 属于不同口径：

- G8 衡量架构验收前置条件是否满足；其 `NOT READY` 不构成开发推进的阻塞。
- E1–E8 衡量工程实施准入包是否具备；其合取规则要求八项全部 `ESTABLISHED`。
- 因此，**G8 NOT READY 不构成开发推进的阻塞**，但这不改变本轮 E1–E8 尚未全部满足的测量结论。
- 不得把 G8 的 `DOES-NOT-BLOCK` 解释为 E1–E8 已满足，也不得把 E1–E8 的未满足反向改写为 G8 的状态变化。

## §4 本轮不改变的事项

本轮仅形成 E1–E8 证据测量记录，不改变以下事项：

- 不改变 G8 `NOT READY`。
- 不改变架构 `NOT ACCEPTED`。
- 不改变任何 finding 状态、严重级别、责任归属或处置状态。
- 不构成开发开工授权。
- 不构成生产授权或生产激活授权。
- 不构成角色任命、maintainer 任命或权限授予。
- 不构成配额解冻或任何资源额度变更。
- E1–E8 仍未全部满足；任何状态变更均须由相应责任方提供可审计证据，并按既有治理流程处理。

## §5 复现方式

以下命令用于核验本记录引用的仓库、commit、文件、workflow 和 Issue 评论。命令本身不改变仓库状态。

### 5.1 核验开发仓库、默认分支和当前 HEAD

```bash
gh api repos/oahcom/AiMemoryBrain \
  --jq '{full_name, default_branch, html_url}'

git clone https://github.com/oahcom/AiMemoryBrain.git
cd AiMemoryBrain
git fetch origin main
git checkout main
git rev-parse HEAD
git rev-parse origin/main
git show --no-patch --format=fuller 2a20ba1181509106532bbd4fc156bdc45f2f2101
```

将 `git rev-parse HEAD` 与本记录所引用的目标 commit 比较；若远端 main 已前进，应同时记录新 HEAD，不得把新 HEAD 冒充为本次测量基线。

### 5.2 核验 crate 与工具链信息

```bash
cd AiMemoryBrain
sed -n '1,100p' Cargo.toml
rustc --version
cargo --version
```

### 5.3 重跑离线构建和测试

```bash
cd AiMemoryBrain
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/aimemorybrain-target}"

cargo build --offline --lib
cargo build --offline --tests
cargo test --offline
```

记录执行环境、实际命令、退出码、测试总数、passed/failed/ignored 数量及目标 commit。历史测试数字应以实际重跑输出为准。

### 5.4 核验 workflow 清单与治理 workflow 内容

```bash
gh api repos/oahcom/AiMemoryBrain/actions/workflows \
  --jq '.workflows[] | {name, path, state}'

gh api repos/oahcom/AiMemoryBrain/contents/.github/workflows/governance-gate.yml \
  --jq '.download_url'
```

读取 workflow 文件：

```bash
gh api repos/oahcom/AiMemoryBrain/contents/.github/workflows/governance-gate.yml \
  --jq '.content' | base64 -d
```

逐项确认是否存在实际执行 `cargo build`、`cargo test` 或等效 build/test 的 workflow，以及是否留存构建产物和对应 SHA。仅有治理结构检查不能计为 build/test CI。

### 5.5 核验 Issue #7 与指定评论

```bash
gh api repos/oahcom/AiMemoryBrainArchitecture/issues/7 \
  --jq '{number, title, state, body}'

gh api repos/oahcom/AiMemoryBrainArchitecture/issues/7/comments \
  --paginate \
  --jq '.[] | select(.id == 7021990583) | {id, html_url, body}'
```

指定评论的直接链接：

`https://github.com/oahcom/AiMemoryBrainArchitecture/issues/7#issuecomment-7021990583`

### 5.6 核验 ruleset 与 bypass 配置

```bash
gh api repos/oahcom/AiMemoryBrain/rulesets/27711552
```

核对规则集名称、要求的 status checks、`bypass_actors` 和当前用户 bypass 能力。若当前凭证无读取权限，应记录为无法独立读取，不得将权限错误解释为规则集不存在。

### 5.7 核验架构仓 G8 与 readiness register 载体

```bash
git -C ../AiMemoryBrainArchitecture fetch origin main
git -C ../AiMemoryBrainArchitecture show \
  origin/main:14-ai-development/work-items/AID-2026-010/g8-seven-conditions-evidence-map.md

git -C ../AiMemoryBrainArchitecture show \
  origin/main:14-ai-development/development-readiness-register.md
```

核对 G8 evidence map §二与 readiness register 第 50 行的原文和当前版本。若仓库路径或分支布局发生变化，应先定位当前权威文件路径，再记录实际读取位置；不得根据文件名推断内容。

---

本记录是截至测量日期的证据状态快照。后续若责任方补充权威载体、可复现运行记录或权限证据，应以新的测量记录或正式治理变更更新状态，不应追溯性地把本轮未取得的证据标记为已存在。
