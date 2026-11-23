---
document_metadata:
  domain: ai-development
  role: guide
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "Owner 已决定退役服务器端 GitHub Actions Runner；当前 CI 统一使用 GitHub 托管的 ubuntu-latest Runner。"
    usage_status: Deprecated
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: "服务器端 GitHub Actions Runner 已退役。本引导流程仅保留为历史证据，不得用于安装或恢复服务器 Runner。"
      effective_date: "2026-11-23"
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

> **已退役 — 2026-11-23。** Owner 已决定服务器不再运行 GitHub Actions 自托管 Runner；CI 统一使用 GitHub 托管的 `ubuntu-latest` Runner。本文件仅保留为历史记录，不得据此安装、启动或恢复服务器 Runner。

# Ubuntu 自托管运行器引导运维手册 / Ubuntu Self-Hosted Runner Bootstrap Runbook

**Document:** AI-RUN-002-RUNBOOK  
**Version:** 1.1 (revised 2026-11-17)  
**Deployment status:** RETIRED 2026-11-23. **Security acceptance:** historical record only.
**Target:** `[HOST IDENTIFIER WITHHELD]`, runner name `[RUNNER IDENTIFIER WITHHELD]`  
**Tracking:** [Issue #26](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/26)  
**Normative architecture statement:** DOC-OPS-001、`docs/zh-CN/14-ai-development/ci-runner-operations.md` 和 `docs/en/14-ai-development/ci-runner-operations.md`。这一对文档以双语形式说明了已部署的形态、安全边界和准入策略。本文件是执行流程。  
**Translation:** TRANSLATED / 中文版已同步（本文件即中文版；英文原文见 `ubuntu-self-hosted-runner-bootstrap.en.md`）。规范性决策和安全边界以双语 DOC-OPS-001 文档对为准，必须在其中查阅。

## 修订摘要（v1.0 → v1.1） / Revision summary (v1.0 → v1.1)

| Item | v1.0 (计划) | v1.1 (已执行并接受) |
|---|---|---|
| Service account | 专用 `actions-runner` | **`<RUNNER_SERVICE_ACCOUNT>`**（同时也是登录账户，具有免密码 sudo 权限） |
| Install path | `/opt/actions-runner` (0750) | **`<RUNNER_INSTALL_DIR>`** |
| Labels | `ai-worker` | **`self-hosted,linux,x64`**（自定义标签已推迟，参见 §4.2） |
| Untrusted-trigger isolation | “限制为可信 dispatch”——依赖人工纪律 | **由运行器强制执行**，通过作业启动钩子实现（§4.1） |
| Status | PROPOSED | ACTIVE；验收证据见 §6 |

账户和路径方面的偏差已**记录，但尚未通过安全验收**。其理由和剩余风险如下所述。不得将此描述为“按规范部署”或已批准接受风险。

## 0. 安全前置条件 / 0. Safety preconditions

- 轮换任何可能已经暴露的凭据。不得重复使用。
- 使用云服务提供商可信的服务器控制台，或已经获得授权的管理会话执行引导。对于稳定运行状态下的工作器，不需要本地 PC 隧道。
- 安装任何内容之前，验证主机身份和操作系统。
- 不得将密码、私钥、PAT、运行器注册令牌、Webhook 密钥或模型提供商密钥粘贴到聊天、Git、Issues、PR、日志或构建产物中。
- 在配置前立即生成 GitHub 运行器注册令牌。该令牌有效期很短；绝不得将其保存在文件或 shell 历史记录中。
- 确保运行器不执行不可信代码。截至 v1.1，这一要求通过 §4.1 中的准入钩子**以机械方式强制执行**，而非仅依赖人工纪律。
- 使用非 root 用户运行服务。绝不得以 root 身份运行运行器服务。已执行的部署满足“非 root”要求，但不满足“专用账户”要求；参见 §0.1。

## 0.1 已接受的偏差 / 0.1 Accepted deviations

| Deviation | 记录日期（不代表批准） | 补偿性控制措施 | 剩余风险 |
|---|---|---|---|
| 运行器服务以 `<RUNNER_SERVICE_ACCOUNT>` 身份运行，该账户具有免密码 sudo 权限 | 2026-11-17 | L1 准入钩子拒绝所有 ref 不是 `refs/heads/main`，或事件不是 `push` / `workflow_dispatch` / `schedule` 的作业 | 已获准执行的工作流可以使用 `sudo`。若要实现隔离，需要设置 `NoNewPrivileges=yes` 或使用独立账户；两者均未实施 |
| 安装在 `<RUNNER_INSTALL_DIR>` 下，而非 `/opt/actions-runner` | 2026-11-17 | `.credentials`、`.credentials_rsaparams`、`.runner` 的权限模式均为 600；运行器目录权限模式为 755，所有者为 `<RUNNER_SERVICE_ACCOUNT>` | 能够访问 `<RUNNER_SERVICE_ACCOUNT>` 账户的本地用户可以读取运行器凭据。目前主机上没有其他交互式账户 |
| 标签采用平台默认值，而非 `ai-worker` | 2026-11-17 | 仓库中恰好只有一个自托管运行器；作业无法被分配到其他位置 | 如果注册第二个自托管运行器，必须先恢复自定义标签（参见 §4.2） |

**Security acceptance:** 在基础设施/安全 Owner 明确记录决定之前，这一偏差仍未获得安全验收批准。如果发生以下任何情况，必须重新评估——注册第二个自托管运行器；在主机上创建第二个交互式账户；仓库变为公开仓库；启用 `main` 分支保护且有人要求放宽钩子限制。

## 1. 主机预检 / 1. Host preflight

从 Ubuntu 服务器控制台运行：

```bash
set -eu
hostnamectl
. /etc/os-release
printf 'OS=%s VERSION=%s\n' "$ID" "$VERSION_ID"
uname -m
nproc
free -h
df -h /
timedatectl status
systemctl is-enabled tailscaled
systemctl is-active tailscaled
tailscale status
tailscale ip -4
```

然后是构建工具链。`cargo test --workspace --all-targets` 会通过 `cc::Build` 编译内置 SQLite，因此编译器是运行器存在意义所在的那个作业的前置条件——而 `cc` **存在**不等于**可用**。一个没有 `cc1` 的 `gcc` 能被 `command -v` 找到，却仍在 `libsqlite3-sys` 内部失败。请分别检查存在性与可用性：

```bash
for t in cc gcc pkg-config make; do
  command -v "$t" >/dev/null 2>&1 && printf '%-12s PRESENT\n' "$t" || printf '%-12s MISSING\n' "$t"
done
printf 'int main(void){return 0;}\n' >/tmp/cc-probe.c
if cc /tmp/cc-probe.c -o /tmp/cc-probe 2>/tmp/cc-probe.err; then
  echo "OK: cc compiles and links"
else
  echo "MISSING C TOOLCHAIN: cc is on PATH but cannot compile; see /tmp/cc-probe.err"
fi
rm -f /tmp/cc-probe.c /tmp/cc-probe /tmp/cc-probe.err
```

`cc ... cannot compile` 属于供给失败，不是依赖缺陷：在注册运行器之前安装 `build-essential`（或将 `CC` 指向真实的工具链）。若 `cc` 直接为 `MISSING`，结论相同——下一次 `cargo test` 会在 `libsqlite3-sys` 内部失败，看起来像 `rusqlite` 的问题，而不是主机的问题。

将非密钥输出记录在部署证据中。在选择运行器软件包之前，确认架构：**此主机为 `x86_64`**。从 `arch=arm64` 页面选择的软件包是错误的制品；此外，部分下载的软件包也无法通过 `tar tzf` 检查，并且不会留下 `config.sh`。提取之前，必须同时验证架构和归档文件哈希值。

## 2. 服务身份 / 2. Service identity

**实际执行情况：**运行器使用现有的 `<RUNNER_SERVICE_ACCOUNT>` 账户和 `<RUNNER_INSTALL_DIR>`。没有创建新账户。注册后立即收紧凭据权限：

```bash
chmod 600 <RUNNER_INSTALL_DIR>/.credentials <RUNNER_INSTALL_DIR>/.credentials_rsaparams <RUNNER_INSTALL_DIR>/.runner
```

**计划中的形态，尚未执行：**通过 `useradd --create-home --shell /bin/bash actions-runner` 创建账户，再使用 `install -d -o actions-runner -g actions-runner -m 0750 /opt/actions-runner` 创建目录，同时确保该账户不属于 `sudo` 和 `docker` 组。采用这一方案是一项有意进行的迁移，而不是常规清理：它需要重新注册，并会导致运行器短暂中断。

## 3. 获取运行器软件包和一次性注册令牌 / 3. Obtain the runner package and one-time registration token

1. 打开仓库 **Settings → Actions → Runners → New self-hosted runner**。
2. 选择 Linux 和 §1 中确认的架构（此主机为 `x64`）。
3. 下载软件包，并在提取之前**验证已发布的 SHA256**。
4. 即时生成注册令牌。将其视为密钥；不要保存。
5. 将所有权转交给运行服务的账户。

使用 GitHub 显示的当前运行器版本对应的命令，而不是在此固定一个未经验证的版本。

## 4. 配置服务（实际执行情况） / 4. Configure the service (as executed)

运行 `config.sh` 时，具有特权的本地进程检查可以看到令牌；不得声称情况并非如此。使用前立即签发令牌，在该 shell 中禁用历史记录，并在完成后关闭该 shell。

```bash
./config.sh \
  --url https://github.com/oahcom/AiMemoryBrainArchitecture \
  --token <ONE_TIME_TOKEN> \
  --name <RUNNER_NAME> \
  --labels self-hosted,linux,x64 \
  --work _work \
  --unattended --replace
sudo ./svc.sh install <RUNNER_SERVICE_ACCOUNT>
sudo ./svc.sh start
```

生成的 unit 文件为 `<RUNNER_SERVICE>.service`。必须配置两个 drop-in 文件；两者都具有关键作用。

`/etc/systemd/system/<RUNNER_SERVICE>.service.d/proxy.conf`：

```ini
[Unit]
After=network-online.target
Wants=network-online.target

[Service]
Environment="HTTP_PROXY=http://<LOCAL_PROXY_HOST>:<LOCAL_PROXY_PORT>"
Environment="HTTPS_PROXY=http://<LOCAL_PROXY_HOST>:<LOCAL_PROXY_PORT>"
Environment="http_proxy=http://<LOCAL_PROXY_HOST>:<LOCAL_PROXY_PORT>"
Environment="https_proxy=http://<LOCAL_PROXY_HOST>:<LOCAL_PROXY_PORT>"
Environment="NO_PROXY=localhost,127.0.0.1,::1"
Environment="no_proxy=localhost,127.0.0.1,::1"
```

`...service.d/guard.conf`：

```ini
[Service]
Environment="ACTIONS_RUNNER_HOOK_JOB_STARTED=<RUNNER_INSTALL_DIR>/hooks/job-started-guard.sh"
```

**此版本运行器中的 `runsvc.sh` 不会读取 `.env`。** 代理设置必须来自 unit（drop-in），而不是 `.runner` 同级目录下的 `.env`。必须通过读取进程环境来验证，而不是查看文件：

```bash
PID=$(pgrep -f "Runner.Listener run" | head -1)
sudo tr '\0' '\n' < /proc/$PID/environ | cut -d= -f1 | grep -E '^(HTTP_PROXY|HTTPS_PROXY|http_proxy|https_proxy|NO_PROXY|no_proxy|ACTIONS_RUNNER_HOOK_JOB_STARTED)
```

出口路由、代理端点、私有地址范围和主机本地服务拓扑均属于由操作人员控制的基础设施细节。不得将这些信息记录在此仓库中；应通过受访问控制的运维渠道进行验证。本运维手册仅要求遵循 GitHub Actions 所需的已批准 HTTPS 出口策略。

## 4.1 准入控制（必需） / 4.1 Admission control (REQUIRED)

这是服务层准入控制。它能够降低不可信触发器带来的暴露风险，但不能使具有 sudo 能力的运行器实现隔离，也不能使其获得安全验收。对可信主机或运行器服务配置的更改可能绕过该控制。

**L1 — 服务层（具有约束力）。** `ACTIONS_RUNNER_HOOK_JOB_STARTED` 指向 `<RUNNER_INSTALL_DIR>/hooks/job-started-guard.sh`。该钩子在任何工作流步骤执行之前运行，并在以下条件不满足时使作业失败：

- `GITHUB_REF` 必须严格等于 `refs/heads/main`，**并且**
- `GITHUB_EVENT_NAME` 必须是 `push`、`workflow_dispatch`、`schedule` 之一。

如果无法解析 ref，则拒绝该作业（默认拒绝）。

不要假定钩子会收到上下文文件。在运行器 2.338.2 中，钩子以 `bash -e <hook>` 的形式执行，不带 argv，也没有 stdin；判定结果必须读取工作器导出的环境变量。一个期望通过 `$1` 获取参数的实现会拒绝所有作业——这一问题在 2026-11-17 被观察到，并导致修复前的一次运行失败。

制品和操作人员使用的文件：

| Path | Purpose |
|---|---|
| `<RUNNER_INSTALL_DIR>/hooks/guard.log` | 每项判定记录一行：判定结果、ref、事件、来源 |
| `<RUNNER_INSTALL_DIR>/hooks/last-decision.txt` | 最近一次判定的完整记录（ref、事件、`GITHUB_REF_PROTECTED`、运行 ID、执行者） |
| `<RUNNER_INSTALL_DIR>/hooks/observe.flag` | 紧急回滚：文件存在 ⇒ 仅记录日志，绝不阻止。创建该文件，进行调查，然后将其删除 |

**L1 证据（2026-11-17，此主机）：**

| Run | Trigger | Verdict | Job |
|---|---|---|---|
| 44049832708 | `push` → `refs/heads/main` | ALLOW | `Succeeded` — 此运行器上的首次真实执行 |
| 44050069421 | `push` → `refs/heads/ci/admission-negative-test` | DENY `ref_not_default_branch` | `Failed`，**执行步骤数为零** |
| 44050467500 | `push` → `refs/heads/main` | ALLOW | `Succeeded` |

**L2 — 仓库层（预防性）。** `scripts/ci/audit_runner_admission.py` 会拒绝任何包含 `self-hosted` 作业的工作流中的以下情况：不可信触发器（`pull_request`、`pull_request_target`、`issue_comment`、`workflow_run`、……）；没有 `branches:` 过滤器的 `push`；`push.branches` 指定了 `main` 以外的分支；以及无法进行静态求值的 `runs-on`。`.github/workflows/runner-admission-policy.yml` 在 GitHub 托管的运行器上运行该脚本。通过将此检查设为 `main` 上的必需检查来绑定该策略。

**L3 — 组织层（Owner 操作，尚未启用）。** 在 `main` 上启用分支保护；对自托管作业使用需要审批的 Environments；以及使用仓库范围的运行器组。在分支保护启用之前，`main` 本身不受保护——钩子观察到 `GITHUB_REF_PROTECTED=false`，因此“可信分支”只是一项约定：任何能够向 `main` 推送的人，都可以更改将在该分支上运行的内容。

## 4.2 自定义标签（已推迟） / 4.2 Custom label (deferred)

`--labels self-hosted,linux,x64` 是平台标签。v1.0 中具有区分性的 `ai-worker` 标签尚未设置，因为添加或重命名标签需要使用新的、一次性的令牌重新注册。在注册第二个自托管运行器之前完成此操作；在此之前，优先使用 `runs-on: [self-hosted, linux, x64]`，使工作流与实际情况保持一致。

## 5. 诊断工作流 / 5. Diagnostic workflows

第一个工作流 **MUST** 是无害且只读的。目前存在两个：

- `.github/workflows/runner-guard-selftest.yml` — 在其自身路径上使用 `push`，并支持 `workflow_dispatch`；打印执行上下文和守卫的判定记录，如果 `guard.log` 中不存在 `ALLOW ref=refs/heads/main`，则使工作流失败。
- `14-ai-development/…` 诊断工作流 — 仅支持 `workflow_dispatch`；报告主机名、操作系统、架构、磁盘、内存和 Tailscale 服务状态。

两者均不得完整打印环境变量、读取凭据存储、上传主目录或工作区、运行由 Issue/PR 提供的脚本，或接触生产系统。

## 6. 验收证据 / 6. Acceptance evidence

- [x] 已记录操作系统、架构、资源、时间同步和网络预检结果。
- [x] 已通过带外方式验证主机身份。
- [ ] 已轮换已披露的密码——仅有操作人员声明。
- [ ] 专用非 root 运行器账户——**未采用**；已由 §0.1 中接受的偏差取代。
- [x] 运行器显示为 Online，且具有预期标签（`self-hosted,linux,x64`）。
- [x] 在 main 分支 push 时，运行器执行/准入自测试成功——运行 ID 为 44049832708 和 44050467500。这些运行并非手动只读 Worker 诊断工作流。
- [ ] 手动只读 Worker 诊断工作流（`.github/workflows/ubuntu-worker-diagnostics.yml`）——NOT RUN / 无证据；未记录匹配的 workflow-dispatch 运行 ID。
- [ ] 运行器服务能够在重启后存活并重新连接——启动时已 `enabled`，并采用文档规定的启动顺序，但**尚未执行重启周期测试**。
- [x] L1 准入钩子在工作流步骤执行之前拒绝了经过测试的功能分支 push（运行 ID 44050069421）；完整的不可信 PR 隔离和 sudo 能力约束仍有待独立审查。
- [x] Git、日志、构建产物、Issues 或 PR 评论中不存在密钥——已针对 2026-11-17 新增的文件进行审查。
- [ ] 已测试紧急停止/运行器移除流程——目前仅有文档说明；尚未在生产环境中执行守卫的 `observe.flag` 回滚。

当前安全验收状态为 **BLOCKED**。即使所有运维检查项均已勾选，状态也仅为 **RUNNER_ONLINE**；这不能证明已经通过安全验收。它不能证明 24/7 A–I 自主运行、持久化事件处理、独立 Owner 身份、租约隔离（lease fencing）、崩溃恢复或端到端治理已经实现。

## 7. 回滚/紧急停止 / 7. Rollback / emergency stop

1. **立即停止执行：**在 GitHub 中取消运行，然后停止服务：`sudo systemctl stop <RUNNER_SERVICE>.service`。
2. **暂停运行器：**在仓库 Settings → Actions → Runners 中禁用该运行器。
3. **移除注册：**遵循 GitHub 记录的移除流程，然后删除 `<RUNNER_INSTALL_DIR>/.credentials*`。
4. **放宽守卫（仅用于诊断）：**`touch <RUNNER_INSTALL_DIR>/hooks/observe.flag`；在了解事件情况后立即将其删除。若将其留在原处，准入控制将被静默禁用。
5. **撤销事件期间暴露的凭据**（注册令牌、PAT、SSH 密码）。
6. 保留经过脱敏的日志（`journalctl -u <unit>`、`<RUNNER_INSTALL_DIR>/_diag/`、`hooks/guard.log`），并在 Issue #26 中记录该事件。

## 8. 当前状态 / 8. Current status

据报告，部署于 2026-11-17 处于 ACTIVE 状态，运行器执行/准入自测试已成功，并记录了三项准入判定（§4.1）。手动只读 Worker 诊断工作流没有已证实的运行记录，仍处于 NOT RUN 状态。这些属于运维观察结果，而非独立安全评估。已由操作人员确认但尚未经过独立重新验证的事项：密码轮换。**尚未验证：**重启周期、紧急停止流程，以及 L3 设置（分支保护、必需检查、环境审批）。运行器具有 sudo 能力的服务身份仍然构成重大剩余风险。业务流水线尚未在此运行器上运行；A–I Owner 工作器仍处于 **NOT DEPLOYED** 状态。**安全验收仍为 BLOCKED，等待基础设施/安全 Owner 作出明确决定并提供独立证据。**

本译文由 RD-F08-01（P0）驱动，对照原文 EN，语义一致性待 R1 核验。
