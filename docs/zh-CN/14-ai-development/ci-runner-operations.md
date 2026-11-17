# AI Memory Brain — CI 自托管 Runner 运维设计

- 文档 ID：DOC-OPS-001
- 版本：1.1（2026-11-17 修订：接受运行身份偏差，新增服务层准入校验）
- 对应英文：[CI Self-Hosted Runner Operations](../../en/14-ai-development/ci-runner-operations.md)
- 依据：2026-11-17 在云端主机 zesu 上的实际部署与实测数据（主机地址不在本仓库记录），源修订见本文末
- 状态：**运维设计说明**，描述一个**已部署并运行**的实例；实测数字为该日的单次测量，不构成性能承诺；准入控制已由 L1 钩子在服务层强制执行（第 4 节），首次真实执行证据见第 14 节

## 1. 目的

说明本仓库的持续集成**在哪台机器上跑、流量怎么出去、出故障怎么恢复**。它不是架构规范，不改变任何 Owner 契约；它解释的是"验证证据从哪来"这一层基础设施。

读者对象：需要判断"CI 失败是代码问题还是环境问题"的工程师，以及接手这台机器的人。

## 2. 一句话概括

在本仓库的 CI 无法依赖 GitHub 托管 Runner 满足网络可达性的前提下，采用**一台自托管 Runner + 本机分流代理**的结构：Runner 只负责执行任务，所有出网流量由本机 sing-box 决定走哪条链路，代理的默认出口是 Cloudflare WARP 隧道。

## 3. 范围与非目标

**范围内**

- 自托管 Runner 的部署形态、标签、服务化方式。
- 出口网络的拓扑、分流规则，以及"为什么不能直连"的实测依据。
- 故障判据、恢复动作、回滚路径。
- 安全边界：运行身份、凭据位置、监听地址、权限。

**非目标**

- 不定义 CI 流水线的阶段划分、缓存策略或矩阵构建。
- 不承诺吞吐。免费 WARP 带宽具有明显的时段抖动（第 12 节给出实测区间）。
- 不涉及源码构建环境（工具链版本、交叉编译目标），这些由 workflow 自身决定。
- 不替代 GitHub 侧的权限模型。Runner 以仓库级注册运行，其可见范围由注册时的仓库决定。

## 4. 与本仓库既有引导规程的关系

本仓库已有一份 Runner 引导规程 `AI-RUN-002-RUNBOOK`（`14-ai-development/ubuntu-self-hosted-runner-bootstrap.md`，位于 `infra/remote-worker-bootstrap-2026-11-17` 分支，跟踪 Issue #26），状态为 **ACTIVE / operator-executed（v1.1，2026-11-17 修订）**。

本文档记录的是该规程的**实际执行结果**。两者的部署形态**存在偏差**，必须显式记录，不能用"已按规程执行"含混过去：

| 维度 | AI-RUN-002-RUNBOOK 拟定 | 实际部署 |
|---|---|---|
| 运行身份 | 专用账号 `actions-runner` | `ubuntu`（与该机登录账号相同） |
| 安装路径 | `/opt/actions-runner`（`0750`，属主 `actions-runner`） | `~/actions-runner` |
| 标签 | `ai-worker` | `self-hosted,linux,x64` |
| 权限边界 | 明确禁止加入 `sudo` / `docker` 组 | `ubuntu` 具备**免密 sudo** |
| 目标主机 | `ubuntu-primary-01` | 同一主机（`vm-0-9-ubuntu`） |
| 状态 | PROPOSED | 已部署并在线 |

**偏差的实际后果**：workflow 以 `ubuntu` 身份执行，而该账号可无密码提权到 root，因此**任何在这台主机上执行的 workflow 都等价于该主机的 root 权限**。

**决策（DECIDED，2026-11-17，Owner）**：**不回退**账号形态。把 `AI-RUN-002-RUNBOOK` 修订为 v1.1 接受现状，并把准入限制从"靠人遵守"改为**服务层强制**。理由：回退只能把"root 等价"换成"同一主机上的普通用户"，而账号能否提权并非主要风险面——**主要风险面是"workflow 能不能在这台主机上开始执行"**。有效的控制点是准入判定，不是账号名。

**三层准入校验**：

| 层 | 机制 | 落点 | 强制力 |
|---|---|---|---|
| L1 服务层 | `ACTIONS_RUNNER_HOOK_JOB_STARTED` 钩子读 `GITHUB_REF` 与 `GITHUB_EVENT_NAME`，仅放行 `refs/heads/main` 上的 `push`、`workflow_dispatch`、`schedule`，其余在**任何步骤执行前**失败 | 主机 `~/actions-runner/hooks/job-started-guard.sh`，经 systemd drop-in 注入 | **强制**：在 runner 内部判定，改 workflow 改变不了判定 |
| L2 仓库层 | 工作流审计：`self-hosted` 与 `pull_request` / `pull_request_target` / `issue_comment` / `workflow_run` 等事件的组合、无分支约束的 `push`、无法静态判定的 `runs-on` 表达式，一律判失败 | `.github/workflows/runner-admission-policy.yml` + `scripts/ci/audit_runner_admission.py` | 预防性：需设为必需状态检查才具约束力 |
| L3 组织层 | 分支保护、Environment 必须审批、Runner group 限仓 | GitHub 仓库设置 | 需 Owner 在设置界面启用；本文不代为声明已启用 |

**L1 的实测依据**（2026-11-17，同一台主机）：

| 场景 | 结果 |
|---|---|
| `push` → `refs/heads/main`（run 44049832708） | ALLOW，job `Succeeded` |
| `push` → `refs/heads/ci/admission-negative-test`（run 44050069421） | DENY `ref_not_default_branch`，job `Failed`，**零个步骤执行** |
| 钩子的上下文来源 | 该版 runner 以 `bash -e <hook>` 调用，无参数、无 stdin；判定依据来自 worker 导出的 `GITHUB_*` 环境变量 |

**残余风险（已接受，不再是未决事项）**：

1. 钩子只管"job 能否开始"，不管"job 里做什么"，步骤内仍可 `sudo`。收敛需 `NoNewPrivileges=yes` 或独立账号，两者都会改变现有 job 能力，本轮**未实施**。
2. `main` 目前**未启用分支保护**（钩子实测 `GITHUB_REF_PROTECTED=false`），"受信分支"因此是事实约定而非平台强制。启用分支保护前，能推送 `main` 的人可直接改变待执行的 workflow，L1 只认 ref、不会拦。
3. 钩子 fail-closed：钩子脚本或 `python3` 不可用时所有 job 失败。回滚开关为 `hooks/observe.flag`（存在时仅记录、不拦截）。

## 5. 组件与职责

| 组件 | 位置 / 单元名 | 职责 | 不负责 |
|---|---|---|---|
| Runner 监听器 | `~/actions-runner`，`actions.runner.oahcom-AiMemoryBrainArchitecture.zesu-x64.service` | 领取任务、执行 workflow、回报状态 | 不做任何网络策略决策 |
| 代理前置 | `sing-box.service`，`127.0.0.1:17891`（mixed 入站） | 唯一的路由与出口选择点 | 不感知任务语义 |
| WARP 隧道 | `warp-usque.service`，`127.0.0.1:2085` | 提供默认出口（MASQUE over QUIC） | 不做分流 |
| 备用出口池 | sing-box 的 `auto` 组（订阅节点，`urltest` 择优） | WARP 不可用时兜底 | 不作为默认 |
| 直连出口 | sing-box 的 `direct` 组 | `api.github.com`、国内镜像站、私有网段 | 不承载大文件下载 |

**职责边界的一句话**：Runner 不知道网络怎么走，代理不知道任务是什么。二者只通过环境变量 `HTTP_PROXY` / `HTTPS_PROXY` 连接。这条边界的价值在于——网络故障可以在不动 Runner、不动任务定义的情况下排查和切换。

## 6. 上下文与出口拓扑

```
GitHub
  │
  ├─ api.github.com ───────────── 直连（共享出口 IP 会触发 403 限流，见 8.3）
  │
  └─ github.com / codeload.github.com / release-assets / ghcr.io
        │
        ▼
   sing-box  127.0.0.1:17891   ← Runner 的 HTTP(S)_PROXY 指向这里
        │  route.final = pick
        ├─ warp   默认：usque → CF WARP（免费，不计订阅流量）
        ├─ auto   备用：订阅节点池，urltest 自动择优
        └─ direct 国内镜像站 / .cn / 私有网段 / api.github.com
        │
   Runner.Listener（系统用户 ubuntu，标签 self-hosted,linux,x64）
```

启动顺序由 systemd 依赖固定：`warp-usque` → `sing-box` → `actions.runner.*`。这个顺序是**必须**的：Runner 启动时若代理尚未监听，除注册通道外的所有出网请求都会直接失败。

## 7. 为什么不能直连（实测依据）

该主机位于中国大陆的云机房。部署当天（2026-11-17）对 GitHub 各端点做了直连测量：

| 端点 | 直连表现 | 结论 |
|---|---|---|
| `api.github.com` | HTTP 200 / 0.47 s | 可用，作为直连项 |
| `codeload.github.com`（action 包） | 约 39 KB/s | 不可用 |
| `release-assets`（release 下载） | 3 分钟 0 字节 | 不可用 |
| `git clone`（41 MB 仓库） | 60 秒未完成 | 不可用 |

**关键判断**：API 可达不等于 CI 可用。只测 `api.github.com` 会得出"网络没问题"的错误结论；决定性证据来自 `codeload` 与 `release-assets`——它们才是每个 job 真正要下载的东西。

因此"直连"在本仓库的 CI 场景下**不构成可选方案**，除非将来换到可直连的机房。

## 8. 出口选择的五条硬约束

以下五条都是**实测得出、踩过之后才写下的**。它们是本设计的约束，不是建议。

### 8.1 该主机的 TCP 443 MASQUE 被重置，只能走 QUIC

**看起来像**：WARP 的 MASQUE 既有 UDP 也有 TCP 两种承载，任选其一即可。
**实际是**：该主机上 TCP 443 的 MASQUE 连接被 `connection reset by peer`。空 SNI、`consumer-masque.cloudflareclient.com`、`www.cloudflare.com` 三种 SNI 均被拒。

**约束**：隧道**必须**使用默认 QUIC（UDP 443），**禁止**加 `--http2`。换机器部署时应先各发一条 QUIC 探针和一条 H2 探针，用能通的那条，不要把本机的配方当作通用结论。

### 8.2 必须关闭隧道内 IPv6（`-S`）

**看起来像**：IPv6 可选，关不关无所谓。
**实际是**：不加 `-S` 时 WARP 分配 IPv6 出口，`github.com` 首字节时间 15–24 秒；加 `-S` 后降到 4–6 秒，`release-assets` 吞吐从 286 KB/s 升到 580 KB/s。

**约束**：`ExecStart` **必须**保留 `-S`。这是本设计里单点收益最大的一项配置。

### 8.3 `api.github.com` 必须直连

**看起来像**：全部流量走代理最省事。
**实际是**：代理出口是**共享 IP**，匿名 API 配额早已被其他用户耗尽，返回 `403 rate limit exceeded`；同一时刻直连是 200。

**约束**：分流规则 `domain_suffix: ["api.github.com"] → direct` **禁止**删除。删除后 Runner 的注册心跳与 API 调用会整体失败。

### 8.4 代理必须由 systemd 注入，不能靠 `.env`

**看起来像**：在 `~/actions-runner/.env` 写 `HTTP_PROXY` 就会被读取。
**实际是**：本 Runner 版本的 `runsvc.sh` 不加载 `.env`，进程环境里查不到代理变量。**必须**用 systemd drop-in（`/etc/systemd/system/actions.runner.*.d/proxy.conf`）注入，job 子进程才会继承。

### 8.5 分流规则必须内置于配置生成器

**看起来像**：配置生成器只负责节点，分流规则可以事后手工补。
**实际是**：订阅刷新会重新生成整个配置文件，手工补的规则会被冲掉，`api.github.com` 立刻回到 403。此问题已实际发生一次。

**约束**：分流规则**必须**写在生成器里，随配置一起产出；**禁止**依赖运行期手工修改。

## 9. 主要流程

### 9.1 首次部署

1. 确认主机架构，取对应包并**校验 SHA256**。架构选错或包不完整是最常见的起步失败（本实例曾出现"页面按 arm64 生成命令、实际机器是 x86_64、下载到 450 KB 坏包"的三重错误，症状是解压报 `unexpected EOF` 且没有 `config.sh`）。
2. `config.sh --unattended --labels self-hosted,linux,x64` 注册到仓库。
3. `svc.sh install` 装成 systemd 服务，`enable` 开机自启。
4. 建立出口链路（第 6 节的三个单元），按依赖顺序启动。
5. 用 drop-in 注入代理环境变量。
6. 验收（第 13 节）。

### 9.2 订阅刷新（备用池维护）

订阅中的节点地址与凭据会轮换。刷新流程为：拉取订阅 → 用生成器重建配置（**保留** WARP 出口与分流规则）→ `sing-box check` 语法校验 → 替换配置 → 重启 → 自检 `api.github.com` 与 `github.com` 两个端点。校验失败时**不得**替换正在运行的配置。

### 9.3 切换出口

出口组通过 Clash API 切换（`warp` / `auto` / 具体节点 / `direct`），切换不需要重启任何单元。这是把"出口选择"与"服务生命周期"解耦的主要收益。

### 9.4 节点池的确定方式

**延迟不等于吞吐。** 实测中延迟排名靠前的节点真实下载只有 55 KB/s；最终入池的节点是吞吐 1–1.3 MB/s 的七个美国西海岸节点。因此定池**必须**以实测吞吐为准，延迟仅用于初筛。

## 10. 故障与恢复

| 症状 | 判据 | 动作 |
|---|---|---|
| Runner 连不上 GitHub | `warp-usque` 日志异常 / 隧道断开 | 重启 `warp-usque`，5 秒后自动重连 |
| WARP 完全不可用 | 设备 token 被吊销（日志 403 / invalid token） | 重新 `register`。**会覆盖设备配置，先备份** |
| TTFB 异常升高（>30 s） | `ExecStart` 中 `-S` 丢失 | 补回 `-S` 并重启 |
| `api.github.com` 返回 403 | 直连分流规则丢失 | 重新生成配置（见 8.5），而非手工改配置 |
| 备用池失效 | 节点全超时 | 刷新订阅 + 重测吞吐 + 重定池 |
| CI 明显变慢 | 无错误，仅慢 | 切到 `auto` 对照，判断是 WARP 抖动还是任务本身变重 |

**恢复动作的通用原则**：先确认"哪一层坏了"（隧道 / 代理 / 分流 / Runner），再动那一层。跨层重启会掩盖根因。

## 11. 安全与信任边界

- 代理入站**只监听** `127.0.0.1`，不对外暴露任何端口。
- WARP 设备配置（含私钥与 access token）、订阅地址、Clash API 密钥均为 `600`，**禁止**入库、禁止出现在文档或日志中。
- Runner 以非 root 身份运行；但如第 4 节所述，该身份**具备免密 sudo**，因此"非 root"不等于"无提权"。这是本实例已知且未修复的边界缺陷。
- 本机的出口是一个**共享公网 IP**。两个后果：对目标站点的请求会被计入他人的配额与信誉；本机不应被视为具备稳定身份的出口。
- 隧道由第三方非官方客户端建立。升级前**必须**先在临时端口验证注册与连接可用，再替换现网二进制。

## 12. 性能与资源预算

2026-11-17 实测（单次测量，非承诺）：

| 项目 | 数据 |
|---|---|
| `git clone` 41 MB | 17 s，约 2.4 MB/s |
| `api.github.com` | 0.27 s（直连） |
| `codeload` 单流 | 约 120 KB/s |
| `release-assets` 5 MB | 300–580 KB/s |

**必须声明的非保证**：

1. 免费 WARP 带宽存在明显抖动，同一组参数两次测量可相差 4 倍。为抖动调参（例如改 MTU）无法获得稳定收益；实测中 MTU 1280 与 1360 的差异完全被抖动掩盖，而 1420 直接不通（PMTU 黑洞），因此保持默认 1280。
2. `git` 协议因多流复用，吞吐显著高于单流 `curl`。用单流 `curl` 的低值判断"CI 不可用"会误判。
3. 主机资源：4 vCPU / 3.6 GB 内存 / 根分区 39 GB（已用约 28 GB，71–73%）。`_work` 目录随任务增长，**必须**定期清理；磁盘不是无限资源，也不是本设计的容量保障。

## 13. 验收标准

一台 runner 视为可用，**必须**同时满足：

1. 服务 `active` 且 `enabled`（开机自启）。
2. 日志出现 `Listening for Jobs`，GitHub 仓库页 Runner 状态为 Online。
3. 经代理访问 `api.github.com` 返回 200（验证分流未失效）。
4. `codeload` 能完整下载一个 action 包（验证大文件链路）。
5. 一次真实 `git clone` 能完成（验证多流与重定向链路）。
6. 准入钩子已启用，且 `guard.log` 中存在 `ALLOW ref=refs/heads/main` 记录（验证 L1 未被绕过）。

前四项与第 6 项是必要条件，**第 5 项才是充分条件**——只有它能同时覆盖 TLS、重定向到 `release-assets` / `objects.githubusercontent.com`、多流复用三个失败点。

## 14. 决策、未决事项与引用

**已决议（本实例）**

- 出口默认 WARP，订阅节点池降为备用。理由：WARP 免费且不计订阅流量，订阅出口为共享 IP 且消耗配额。
- 分流：`api.github.com` 与国内镜像站直连，其余走代理。理由见 8.3。
- 标签固定为 `self-hosted,linux,x64`，workflow 中**禁止**写 `arm64`（该主机为 x86_64）。
- 运行身份偏差**接受并固化**（第 4 节）：不回退账号形态，由 L1 钩子在服务层强制“仅 `refs/heads/main` 可执行”；决策日 2026-11-17，对应规程 v1.1。
- 不为抖动调参，保持 MTU 默认值。

**未决（OPEN）**

- **业务流水线尚未在本 Runner 上执行。** 已完成的首次真实执行是 `Runner Guard Self-Test`（2026-11-17，run 44049832708，结论 `Succeeded`），它验证的是“取值—执行—回传”链路，**不等于**本仓库 CI 流水线通过。
- 磁盘增长速率未知，未设定清理阈值与告警。在设定之前，容量风险由人工巡检承担。
- 备用节点池的有效期取决于订阅可用性，未做自动切换（当前需人工判断后切换）。此为有意为之：自动切换会在 WARP 抖动时造成无意义的反复切换。

**引用**

- 双语文档规范：[GOV-DOC-001](../../../00-governance/bilingual-documentation-policy.md)
- Runner 引导规程：`AI-RUN-002-RUNBOOK`，`14-ai-development/ubuntu-self-hosted-runner-bootstrap.md`（分支 `infra/remote-worker-bootstrap-2026-11-17`），跟踪 [Issue #26](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/26)
- 部署实例的完整运维记录（含脚本清单、逐节点测速数据）：归档于另一仓库 `auto-swicth-ip` 的 `docs/gh-runner-zesu-20261117.md`；本文件只保留与本仓库 CI 相关的结论。
- 源修订：本文件依据 2026-11-17 的部署状态与实测撰写；该实例的主机、网络与版本信息记录在 `RUNNER-OPS.md`（部署方工作副本，不入库）。
