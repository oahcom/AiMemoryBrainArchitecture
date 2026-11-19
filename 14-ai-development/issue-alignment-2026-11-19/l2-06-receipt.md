# L2-06 — Engineering & Infrastructure 对齐审查

<badge color="warning">READ-ONLY / HOLD</badge> <badge color="info">提交 Owner A</badge>

**审查身份：** Owner A 统筹的 L2 领域对齐会话，不担任基础设施管理员、安全批准者或工程 Owner。

**本轮执行边界：**
- 不创建 PR、Issue，不写 Git。
- 不关闭 Issue，不修改 assignee、标签或 PR 状态。
- 不执行主机操作，不启动 Worker，不创建凭据。
- 不将候选架构、CI 成功或 PR 合并视为生产安全验收。
- 所有尚未取得授权或独立证据的事项保持 OPEN。

## 1. 启动记录

| 项目 | 本轮记录 |
|---|---|
| 仓库 | `oahcom/AiMemoryBrainArchitecture` |
| 申报 main tip | `d61f813cac6780b6bcc5c09536a8e9bee96cc362` |
| 申报 remediation tip | `745c768deca0a5826d436744213bed3beb65cd85` |
| AI-EXEC-001 | v1.1（申报加载版本） |
| AI-EXEC-002 | v1.1（申报加载版本） |
| AI-EXEC-002 v1.2 | PENDING ADOPTION，不作为本轮规范依据 |
| Decision_ID | NOT_CREATED |
| Delta_Scope | L2 工程与基础设施状态核验 |
| 写操作 | NONE |

特别说明：申报的 SHA、规范版本和 Issue 事实是待核验输入，不自动成为已独立验证的证据。下文将区分申报事实、仓库实测和未验证事项。

## 2. 当前阶段的首要边界

`IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE` 是本轮必须尊重的项目方向。

因此：

1. 架构仓库没有生产 Runtime，不构成当前架构设计阶段的自动阻塞。
2. 不应在架构仓库制造 Mock Runtime 或占位代码来满足工程实现指标。
3. 工程实现入口仍然 PENDING。
4. 尚未取得生产实现、构建、部署及安全隔离证据，不得宣称生产符合性或生产就绪。
5. 生产激活仍然 NOT AUTHORIZED，除非取得独立的正式授权。

这意味着必须分别审查架构设计验收和工程阶段启动条件，不能把两者合并成一个 PASS/FAIL。

## 3. 规范加载核验：发现版本冲突

<badge color="danger">RULES VERSION MISMATCH</badge>

已通过 GitHub 读取 `main` 指定 SHA 下的规范文件，发现：

| 规范 | 实际读取结果 |
|---|---|
| AI-EXEC-001 | v1.1，ADOPTED |
| AI-EXEC-002 | v1.2，PENDING ADOPTION |
| AI-EXEC-002 v1.1 | 本次指定路径读取未取得 v1.1 文件内容 |

AI-EXEC-001 文件 Blob SHA：

`b809d770f93f5a2244988f04f68ad913b29f5e76`

AI-EXEC-002 文件 Blob SHA：

`772cee6b9a9a9c510c79adfd85eefd96397573c2`

这与启动声明要求按 v1.1 执行存在证据冲突。不能把文件中记录的 v1.2 状态忽略，也不能仅凭协调方说明认定 v1.1 已经实际加载。

**处理：** 保留用户指定的 v1.1 执行约束作为本会话的操作边界，但将实际仓库规范加载状态登记为 `RULES-LOAD-NOT-VERIFIED`。不据此推定违规，也不自行裁定 v1.2 已获采用。

## 4. 四个绑定 Issue 的初步核验

<text color="secondary" size="xs">以下状态来自 GitHub Issue 实际读取，而不是仅采用责任映射表。</text>

| Issue | 实际状态 | Assignee | 初步结论 |
|---|---|---|---|
| #7 | OPEN | 无 | 工程阶段入口待建立 |
| #26 | OPEN / reopened | 无 | 安全验收阻塞 |
| #37 | OPEN | 无 | 单 Owner Worker 实现需求待启动 |
| #134 | OPEN | oahcom | P0 合并门禁缺陷待修复 |

责任映射 `#7→工程、#26→基础设施、#37→实现、#134→oahcom+治理` 目前只能作为待核验的领域分工线索，不能视为已经完成的正式 Accountable Owner 授权。

尤其需要强调：

- Issue assignee 不等于领域 Accountable Owner。
- Issue #134 指派给 `oahcom`，不能单独证明其获得基础设施安全批准权。
- #26 的历史关闭不能作为安全验收；其当前状态已经是重新打开。
- #37 的实施目标不能覆盖 #7 的工程入口依赖。

## 5. Main 分支与 CI 实测

<badge color="danger">MAIN PROTECTION DISABLED</badge>

GitHub API 已直接回读 `main`：

<box border radius="lg" padding={3} gap={2}>
  **main**

  <title size="lg" color="success">SHA 已吻合</title>
  <text tabularNums size="xs">d61f813cac6780b6bcc5c09536a8e9bee96cc362</text>
  <divider color="subtle"/>
  | 控制 | 实测 |
  |---|---|
  | Default branch | `main` |
  | Repository visibility | Private |
  | Owner 类型 | User |
  | `protected` | `false` |
  | `protection.enabled` | `false` |
  | Required checks enforcement | `off` |
  | Required contexts | 空 |
</box>

Rulesets API 返回 HTTP 403：

`Upgrade to GitHub Pro or make this repository public to enable this feature.`

这与 #26、#134 的历史记录一致。当前仓库形态下，不能把平台级 Branch Protection 当作已经配置的能力。Rulesets 的实际配置状态也不能从 403 推断为不存在。

另一个重要发现：`main` 当前 SHA 的 workflow runs 查询返回空数组，combined status 查询也没有状态记录。这只说明本次查询没有取得该 SHA 的 CI 运行证据，不代表历史 PR 测试失败或通过。

### 5.1 Workflow 存在不等于门禁生效

已读取 `.github/workflows/` 实际目录。当前存在：

- `ai-owner-worker.yml`
- `ai-owner-worker-bootstrap-labels.yml`
- `ubuntu-worker-diagnostics.yml`
- `bilingual-docs.yml`
- 多个 reference-model / conformance workflow。

其中 `bilingual-docs.yml` 定义了 `GOV-DOC-001 structural checks`，但没有平台 required-check 强制保障。

### 5.2 实际 Worker 工作流的边界

当前 `ai-owner-worker.yml` 已有一条 GitHub-hosted 执行路径：

1. 接收 Issue labeled 或手动 dispatch。
2. 使用 `prepare_task.py` 校验任务。
3. 固定 prompt digest。
4. 调用 Codex Action。
5. 限制输出为 Markdown 文件，排除保护路径。
6. 生成 patch artifact。
7. 在另一个 GitHub-hosted job 中发布分支及 PR。

这属于可审查的候选自动化实现，不是完整生产 Worker Fleet。

尤其缺少从该 workflow 本身可以证明的：

- SQLite 持久化 inbox、lease、fencing 和 run ledger；
- 跨任务的全局单 Owner durable claim；
- 持久化 webhook receiver / queue / Coordinator；
- Ubuntu 主机上的安全生产部署；
- 自动化生产激活授权。

不能把 GitHub Actions 的 concurrency 配置当作 SQLite durable lease，也不能把 PR 发布能力当作生产运行时。

相关文件：

- [AI Owner Worker workflow](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/d61f813cac6780b6bcc5c09536a8e9bee96cc362/.github/workflows/ai-owner-worker.yml)
- [Ubuntu diagnostics workflow](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/d61f813cac6780b6bcc5c09536a8e9bee96cc362/.github/workflows/ubuntu-worker-diagnostics.yml)

## 6. Ubuntu Runner 与安全边界

<badge color="warning">SECURITY ACCEPTANCE BLOCKED</badge>

本轮读取了以下两个实际文件：

- `14-ai-development/ubuntu-self-hosted-runner-bootstrap.md`
- `14-ai-development/remote-worker-inventory.yaml`

发现几个必须区分的事实。

### 6.1 主机部署事实

| 项目 | 证据状态 |
|---|---|
| Ubuntu self-hosted runner 曾部署 | 有部署记录 |
| Runner 执行过真实任务 | 有历史记录 |
| 当前 Runner Online | 证据冲突，未独立确认 |
| Dedicated service account | 未满足 |
| 最小权限 | 未证明 |
| passwordless sudo | Runbook 明确记录 |
| L1 admission hook | 有有限测试证据 |
| 完整不可信 PR 隔离 | 未证明 |
| Reboot recovery | NOT_VERIFIED |
| Emergency stop | NOT_VERIFIED |
| 凭据独立轮换验证 | NOT_VERIFIED |
| Worker Runtime | NOT_DEPLOYED |

一个值得特别说明的状态冲突：

- Inventory 保留了 Runner 已注册、曾在线及执行任务的记录。
- Issue #26 的 2026-11-19 12:00Z 平台实测评论则记录 Runner `zesu-x64` 为 `offline`。
- 本次连接无法独立读取 Actions Runner 实时列表。

因此，不能将历史在线状态写成当前在线。

### 6.2 PR #27 的独立核验

实际读取 PR #27：

- 已合并，merge commit：`19ae5ed2b7a0ab613f188a4dc8e75e4f5bc81320`
- 正式 GitHub Reviews API：空数组。
- PR 正文自己声明独立审查缺失。
- PR 正文记录的验收项目仍有 NOT_RUN / NOT_VERIFIED。

因此：

**PR #27 MERGED ≠ Runner SECURITY ACCEPTED。**

此外，#26 已有后续治理裁决：

`RULING-04-A / DEFER`

其效力是将安全验收范围收窄至当前实际运行面，不得将未部署的 Worker 主机或 Runner 虚构为已验收对象。

#26 仍然 OPEN。延期不代表安全验收完成，也不代表原始风险已经消失。

## 7. 十二项工作范围逐项对齐

| 编号 | 工作范围 | 实测结论 | 状态 |
|---|---|---|---|
| 1 | Canonical Runtime Repository | 当前未指定；工程阶段延后绑定 | DEFERRED |
| 2 | Engineering Owner Designation | 没有具名、经授权的工程负责人 | OPEN |
| 3 | Build / CI / Test | 有文档门禁和参考模型 CI，无生产 Runtime 构建入口 | PARTIAL |
| 4 | Ubuntu self-hosted runner | 有历史部署，当前在线状态存在冲突 | NOT VERIFIED |
| 5 | Dedicated service account | 当前运行记录为通用 sudo 账号 | SECURITY BLOCKED |
| 6 | Branch protection / required checks | `main protected=false` | NOT ENFORCED |
| 7 | Webhook / durable queue / Worker Runtime | 未证明实际部署 | DEFERRED |
| 8 | SQLite run ledger / leases / fencing | 设计及历史候选实现不能证明生产部署 | NOT VERIFIED |
| 9 | Prompt version binding | 有 prompt SHA 计算，但发布证据链不完整 | PARTIAL |
| 10 | Untrusted PR isolation | 有 L1 单项拒绝测试，不等于完整隔离 | NOT VERIFIED |
| 11 | Single-Owner pilot | 有候选工作流，无已验证完整试点 | NOT COMPLETED |
| 12 | Exact-Head merge gate | 有 RULING-03 替代治理方案，但平台门禁不存在 | CONDITIONAL |

### 特别发现：Prompt SHA 的证据链不完整

`ai-owner-worker.yml` 中：

- 计算了 `owner-worker.md` 的 SHA-256；
- 将摘要作为 job output；
- publisher job 接收了 `PROMPT_SHA256` 环境变量。

但发布脚本没有实际使用该变量将 prompt 摘要写入 PR 或其他持久化运行证据。

因此，不能仅凭 workflow 中计算过摘要，就宣称已经完成 Prompt ID、版本、SHA 与执行结果之间的持久化绑定。

### 特别发现：参考模型与生产运行时仍然分离

当前仓库 README 明确声明：

- Architecture definition；
- Implementation not started by design。

虽然仓库已有可执行的参考模型测试和 GitHub Actions 工作流，但这些不证明部署了生产数据库、分布式 Coordinator、队列、Worker 或实际 Adapter。

---

## 8. 逐 Issue 领域审查

### 8.1 Issue #7 — Canonical Runtime Repository / Engineering Entry

<badge color="info">DEFERRED TO ENGINEERING PHASE</badge>

**主责及授权依据**

- 领域：Engineering。
- 当前 assignee：无。
- 具名 Accountable Engineering Owner：未确认。
- 项目授权依据：Issue #10 comment `6929585471`。
- `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`。

**当前真实状态**

OPEN。工程阶段入口清单，不是当前架构阶段阻塞项。

**已验证证据**

- README 声明当前是架构定义仓库，尚未开始实现。
- 没有本仓库生产 Runtime 入口。
- Issue #7 comment `7000099898` 已登记 HOLD 和 2026-12-02 复核点。
- 现有 AID 参考模型不能替代生产 Runtime。

**未验证条件**

1. Canonical Runtime Repository URL 和 branch。
2. 工程负责人及模块 Maintainers。
3. 生产 Build / CI / Test 权威来源。
4. 服务拓扑、数据库和部署环境。
5. 合约到实际代码的追踪关系。
6. JF-10、D36、E36、C01–C23、I36、H36 等映射。

**实现前置依赖**

项目授权的工程阶段启动决定、规范代码仓库和负责人。

**允许的最小下一步**

保留现有 Engineering Entry Checklist；待进入工程阶段时补齐上述授权和交接资料。

**停止条件**

不得因为缺少 Runtime Repository 而在架构仓库添加占位实现；不得把参考模型宣布为生产实现。

**验收标准**

工程阶段正式启动前，仓库、分支、Accountable Owner、构建验证体系、部署拓扑和代码追踪责任必须有可复核记录。

**登记**

- Decision_ID：NOT_CREATED（本会话没有新建决策）
- Delta_Scope：工程入口状态澄清
- Relevant_Artifacts：
  - `README.md` @ `d61f813cac6780b6bcc5c09536a8e9bee96cc362`
  - Blob：`2df8396f89886eb1d24b04f1c946a9bcbb2c88e1`
  - Issue #7：<Link url="https://github.com/oahcom/AiMemoryBrainArchitecture/issues/7" title="Issue #7"/>
- Evidence：Issue #10 comment `6929585471`；#7 comments `6962817070`、`7000099898`。
- Unresolved_Findings：工程负责人、代码仓库、工程阶段启动授权尚未登记。

### 8.2 Issue #26 — Ubuntu Runner / Infrastructure Security

<badge color="warning">OPEN — SECURITY ACCEPTANCE BLOCKED / DEFERRED</badge>

**主责及授权依据**

- 领域：Infrastructure + Security。
- 当前 assignee：无。
- Infrastructure/Security Accountable Owner：未具名。
- PR #27 的作者或合并者不自动获得安全批准权。

**当前真实状态**

OPEN，原始安全验收仍然 BLOCKED。

但依据 `RULING-04-A / DEFER`，未部署 Worker 主机不作为当前 dev-baseline 的完成对象，也不构成当前基线的停等点。

**已验证证据**

- PR #27 已合并。
- Reviews API 返回空数组。
- Runbook 记录现有服务账号具有 passwordless sudo。
- Dedicated least-privilege account 未实现。
- 手动只读诊断仍为 NOT_RUN。
- Reboot recovery、Emergency Stop 未验证。
- Inventory 有历史 Runner 执行证据。
- Issue #26 comment `7008275902` 记录 Runner offline 的平台实测。
- `RULING-04-A` 明确不得虚构未部署 Runner 已验收。

**未验证条件**

1. Runner 当前真实在线状态。
2. 独立最小权限账号和 sudo 隔离。
3. Host identity。
4. 凭据轮换。
5. 完整不可信 PR 隔离。
6. Emergency Stop。
7. Reboot/reconnect。
8. 当前运行面的权限边界和故障处理。

**实现前置依赖**

在任何重新启动主机部署时，必须先明确基础设施安全边界和授权；不能从 PR 合并或历史在线记录推导授权。

**允许的最小下一步**

维持当前 DEFER 状态；只进行已有证据的只读归档和冲突核对。

**停止条件**

不得执行真实主机写操作、账号迁移、Runner 重注册、凭据创建或安全配置修改。

**验收标准**

未来重新评估时，必须逐项提供精确运行证据、服务身份、隔离和恢复证据，并区分历史测试与当前状态。

**登记**

- Decision_ID：`RULING-04-A / DEFER`
- Delta_Scope：主机安全验收范围及延期边界
- Relevant_Artifacts：
  - `14-ai-development/ubuntu-self-hosted-runner-bootstrap.md`
  - Commit：`d61f813cac6780b6bcc5c09536a8e9bee96cc362`
  - Blob：`31765d4656831d136a34a0b2e69135d224a04943`
  - `14-ai-development/remote-worker-inventory.yaml`
  - Commit：`d61f813cac6780b6bcc5c09536a8e9bee96cc362`
  - Blob：`7a4d69a42bf73f2607757ba73fb4a3e183c1663c`
  - <Link url="https://github.com/oahcom/AiMemoryBrainArchitecture/issues/26" title="Issue #26"/>
- Evidence：PR #27；Issue #26 comments `6963045846`、`7008275902`、`7008312636`、`7008359218`。
- Unresolved_Findings：账号权限、凭据隔离、Runner 状态、恢复及当前运行面安全证据。

### 8.3 Issue #37 — Executable Single-Owner Worker

<badge color="warning">OPEN — DEFERRED</badge>

**主责及授权依据**

- 领域：Implementation。
- 当前 assignee：无。
- 具名试点 Owner：尚未指定。
- 与 #26（主机安全）和 #30（运行时架构）保持不同交付边界。

**当前真实状态**

OPEN，但不属于当前 dev-baseline 交付范围。

关键核验结果：

- PR #38：CLOSED，未合并。
- PR #38 正文明确：`SUPERSEDED / NOT APPROVED`。
- 拒绝原因：API-key-based Worker 不符合项目要求的执行通道。
- #37 comment `7008358846` 登记 `RULING-04-A / DEFER`。

**已验证证据**

主分支确实存在 `.github/workflows/ai-owner-worker.yml`，但它是 GitHub Actions + Codex Action 的候选执行路径，不是 Issue #37 所要求的完整 Python Worker 服务。

PR #38 曾包含：

- Python Worker；
- SQLite WAL ledger；
- systemd；
- GitHub Issue polling；
- 分支和 PR 发布。

但这些代码没有进入 main，不能算当前生产实现。

此外，#41 的执行通道约束与 API-backed Worker 存在冲突。不能仅靠更改 Issue 描述消除冲突。

**未验证条件**

1. 获准的模型调用执行路径。
2. 单一试点 Owner。
3. SQLite inbox / lease / fencing / run ledger。
4. 幂等和租约恢复。
5. 完整 allowlist 测试。
6. 秘密不泄漏测试。
7. 完整 Issue → Run → PR 端到端证据。

**实现前置依赖**

当前治理延期结束后，重新确认允许的执行通道和试点范围。

**允许的最小下一步**

保留 PR #38 历史审计记录，不复活其实现，不将 ChatGPT 会话模拟成生产 Worker。

**停止条件**

不得配置 API Key、部署 API Worker、启用自动写入或把现有 GitHub workflow 宣称为已验收生产 Worker。

**验收标准**

未来重新启动时，须提供真实可执行代码、GitHub-hosted 测试、幂等/恢复/隔离测试和完整低风险端到端试点。

**登记**

- Decision_ID：`RULING-04-A / DEFER`
- Delta_Scope：Worker 实现交付延期
- Relevant_Artifacts：
  - `.github/workflows/ai-owner-worker.yml`
  - Commit：`d61f813cac6780b6bcc5c09536a8e9bee96cc362`
  - Blob：`346ec4192c2d187ef0cdcb5fd40bab0bb086dfb6`
  - `.github/codex/prompts/owner-worker.md`
  - Commit：`d61f813cac6780b6bcc5c09536a8e9bee96cc362`
  - Blob：`97b865c4250f6546c42473c5a6bc21e903fb0f1f`
  - `scripts/ai_worker/prepare_task.py`
  - Commit：`d61f813cac6780b6bcc5c09536a8e9bee96cc362`
  - Blob：`0499173e302877b4592aed67c2001cda7bd84fb9`
  - <Link url="https://github.com/oahcom/AiMemoryBrainArchitecture/issues/37" title="Issue #37"/>
  - <Link url="https://github.com/oahcom/AiMemoryBrainArchitecture/pull/38" title="PR #38"/>
- Evidence：Issue #37 comments `6943603130`、`7003324137`、`7008358846`。
- Unresolved_Findings：执行通道冲突、试点 Owner、持久化实现和测试证据。

### 8.4 Issue #134 — Merge Gate / Evidence Integrity

<badge color="danger">OPEN — P0</badge>

**主责及授权依据**

- 领域：Repository Governance / Integration。
- 当前 assignee：`oahcom`。
- Repository Owner/Admin：设置操作所需权限角色。
- Integration Owner：合并证据与 exact-head 核验。
- 当前指派不等于已经获得安全批准权。

**当前真实状态**

OPEN，P0。

这里发现了一项比原始 PR #129 更近的直接反证。

<box border radius="lg" padding={3} gap={2}>
  **PR #273 — 最新已核验的红 CI 合并案例**

  <badge color="danger">FAILURE MERGED</badge>

  | 项目 | 实测 |
  |---|---|
  | Exact Head | `5e0a919a9253b8747c59062b87d0a580cd204e54` |
  | Workflow Run | `44491572672` |
  | Job ID | `135448233941` |
  | Job | GOV-DOC-001 structural checks |
  | Conclusion | failure |
  | Merge time | 2026-11-19 09:33:37 UTC |
  | Merge commit | `4c38ae25b71383d661e4179622cafa04b66a046a` |

  直接读取了失败 Job 日志，确认：

  - `docs/en/14-ai-development/AI-EXEC-001.md` 缺少中文对应文件；
  - `docs/en/14-ai-development/AI-EXEC-002.md` 缺少中文对应文件；
  - PR Body 缺少完整双语 Manifest 或合格例外。

  五项错误均实际出现，workflow 最终 FAIL。
  
  [PR #273](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/273) · [Workflow Run](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44491572672)
</box>

这不是 CI 不存在，而是 CI 没有形成不可绕过的合并限制。

**进一步发现：F-07 与 F-08 同时存在**

直接读取 `scripts/check_bilingual_docs.py`：

- `NORMATIVE_ROOTS` 没有 `14-ai-development`。
- `docs/zh-CN/14-ai-development/AI-EXEC-001.md` 不存在。
- `docs/zh-CN/14-ai-development/AI-EXEC-002.md` 不存在。

这意味着规范源目录登记和双语对应关系均存在缺口。

**治理裁决的准确效力**

Issue #134 comment `7008312198` 已登记：

`RULING-03 — F-02 采用路径 A`

有条件接受协调器侧 Exact-Head 门禁作为当前平台能力限制下的治理等价替代。

但它要求每次合并提供五项证据：

1. Exact Head 锁定。
2. 独立审查及 APPROVED 记录。
3. 合并前 main tip 回读。
4. 合并后 main tip 回读。
5. 文件清单及逐文件 Blob SHA 完整性。

该裁决不等于 GitHub Branch Protection 已启用，也不追认历史违规合并。

**未验证条件**

- 后续所有合并是否持续执行五项证据集。
- PR #273 失败合并的完整治理处置。
- 是否存在遗漏的其他红 CI 合并。
- Exact-Head 替代机制是否持续可靠执行。

**实现前置依赖**

当前采用 RULING-03 的协调器侧证据控制；平台能力变化时重新评估 Branch Protection。

**允许的最小下一步**

对后续合并逐笔核验五项证据；保留历史失败记录，不修改历史提交。

**停止条件**

任何缺少独立审查、Head 锁定、合并前后回读或文件完整性证明的合并，都不得宣称符合 RULING-03。

**验收标准**

能够证明未来合并遵守五项证据要求，并完成 PR #273 的失败事实及双语缺口审计处置。

**登记**

- Decision_ID：`RULING-03`
- Delta_Scope：平台级合并门禁与治理等价替代
- Relevant_Artifacts：
  - `.github/workflows/bilingual-docs.yml`
  - Commit：`d61f813cac6780b6bcc5c09536a8e9bee96cc362`
  - Blob：`fbb01f4cf6c1046fb4f3f6f962d1caed921577b2`
  - `scripts/check_bilingual_docs.py`
  - Commit：`d61f813cac6780b6bcc5c09536a8e9bee96cc362`
  - Blob：`25205bbd9ecaf626422db23b46cbae46806cefd6`
  - <Link url="https://github.com/oahcom/AiMemoryBrainArchitecture/issues/134" title="Issue #134"/>
- Evidence：GitHub branch API、PR #273、Run `44491572672`、Job `135448233941`、RULING-03 comment `7008312198`。
- Unresolved_Findings：历史红 CI 合并、F-07、F-08、未来合并证据持续性。

---

## 9. 规范版本及 Artifact 基线登记

这里补充纠正启动记录中的版本说明。

已经找到 v1.1 的实际采用基线，确认用户指定的执行口径有历史依据：

| 规范 | 版本 | 基线状态 | Commit | Blob SHA |
|---|---|---|---|---|
| AI-EXEC-001 | v1.1 | ADOPTED | `2ca77db4c66529394304f0e1e51ba4696544cfb6` | `cb95815627f895e2cf46c4e801b91153b2713f0b` |
| AI-EXEC-002 | v1.1 | ADOPTED | `2ca77db4c66529394304f0e1e51ba4696544cfb6` | `64a85bc8763ba22a88dc791daddae548b93e4f5d` |

当前 main 中：

| 规范 | 当前版本 | 状态 | Blob SHA |
|---|---|---|---|
| AI-EXEC-001 | v1.1 | ADOPTED | `58af59af266b81109269156ea667df1a15edfb7b` |
| AI-EXEC-002 | v1.2 | PENDING ADOPTION | `7f5928a5d16eb12da7621cfb8bd99ca463afd859` |

因此：

- 本轮按照 v1.1 的已采用版本执行。
- v1.2 是 main 中存在的待采用变体，不把它当成已经生效的新规范。
- v1.2 的双语镜像也没有完整落地，PR #273 的实际失败日志对此提供了直接证据。

### 本轮完整 SHA 基线

<text color="secondary" size="xs">Commit SHA 均为完整 40 位。</text>

| 分支 | 实测 SHA | 结果 |
|---|---|---|
| main | `d61f813cac6780b6bcc5c09536a8e9bee96cc362` | <badge color="success">MATCH</badge> |
| remediation/aid-2026-001-forget-contract-closure-2026-11-18 | `745c768deca0a5826d436744213bed3beb65cd85` | <badge color="success">MATCH</badge> |

两者均已通过 GitHub branch API 回读确认，不只是 commit 对象存在。

## 10. 最终 L2 统筹结论

<box border radius="lg" padding={3} gap={3}>
  **领域对齐结果**

  <row align="center" justify="between">
    架构阶段与工程阶段边界
    <badge color="success">已确认</badge>
  </row>
  <row align="center" justify="between">
    工程负责人指定
    <badge color="warning">OPEN</badge>
  </row>
  <row align="center" justify="between">
    Ubuntu Worker 安全验收
    <badge color="warning">DEFERRED</badge>
  </row>
  <row align="center" justify="between">
    Single-Owner Worker
    <badge color="warning">DEFERRED</badge>
  </row>
  <row align="center" justify="between">
    Merge Gate P0
    <badge color="danger">OPEN</badge>
  </row>
  <divider color="subtle"/>
  **综合判定**

  `PARTIAL — ENGINEERING ENTRY DEFERRED / INFRASTRUCTURE SECURITY DEFERRED / P0 GOVERNANCE FINDING OPEN`
</box>

### 统筹意见

1. **#7 不应继续被当成架构阶段的 Runtime 缺失阻塞。** 继续保留工程阶段入口清单。
2. **#26 不应把 Runner Online 或 PR #27 合并当成安全验收。** 按 RULING-04-A 保持延期和 OPEN。
3. **#37 不应复活 PR #38 的 API Worker 实现。** 按 RULING-04-A 保持延期，保留历史审计。
4. **#134 是本组当前最明确的治理缺陷。** 尤其 PR #273 的红 CI 合并，证明仅有 workflow 不足以形成合并限制。RULING-03 可以作为当前条件性替代控制，但不能虚构平台保护。
5. 不新增人工审批停点，不替任何 Owner 任命负责人，不把延期解释为完成。

### 最终登记汇总

| 登记字段 | 结果 |
|---|---|
| Decision_ID | NOT_CREATED（本会话未作新 Owner 决策） |
| Existing_Rulings | RULING-03；RULING-04-A |
| Delta_Scope | L2 Engineering / Infrastructure / Worker / Merge Gate |
| Relevant_Artifacts | 上述 SHA 清单及四个 Issue |
| Evidence | GitHub API、文件 Blob、PR、Workflow Job 日志、Issue 评论 |
| Unresolved_Findings | 工程负责人、Runtime 入口、Runner 安全、Worker 实现、P0 合并治理 |
| Git 写入 | NONE |
| PR / Issue 创建 | NONE |
| Issue 状态修改 | NONE |
| Assignee 修改 | NONE |
| 主机操作 | NONE |

**提交 Owner A 的建议：** 将 #134 作为本轮唯一需要持续跟踪的 P0 治理缺陷；#7、#26、#37 按现有延期裁决管理，不要重新包装成当前 dev-baseline 的生产实现阻塞。

本报告为只读领域对齐结果，不构成 Owner A、Infrastructure Owner、Security Owner 或 Engineering Owner 的批准，也不构成生产部署授权。

---
