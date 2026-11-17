# ChatGPT-authenticated Codex channel POC / ChatGPT 认证的 Codex 通道可行性验证

**Status / 状态:** PROPOSED — awaiting PR review and an authorized manual run / 提案中，等待 PR 审查和授权手动运行

## 1. Objective / 目标

Prove the complete model-authentication path on the existing remote Ubuntu self-hosted runner:

`GitHub Actions on Ubuntu → Codex CLI → ChatGPT OAuth (device code) → read-only repository task`

在现有远端 Ubuntu self-hosted runner 上验证完整链路：

`Ubuntu GitHub Actions → Codex CLI → ChatGPT OAuth（设备码）→ 只读仓库任务`

This is **not** an OpenAI API-key integration. The workflow does not define or consume `OPENAI_API_KEY`.

这不是 OpenAI API Key 集成；Workflow 不定义、不读取 `OPENAI_API_KEY`。

## 2. Verified platform facts / 已核实的平台事实

- Codex CLI is included in ChatGPT Free and can authenticate with a ChatGPT account.
- Codex Cloud is not included in Free or Go; do not make Codex Cloud a prerequisite for this POC.
- Codex CLI supports device-code authentication for remote/headless machines via `codex login --device-auth`; device-code login must first be enabled in ChatGPT security settings.
- `codex exec` supports non-interactive CI execution and a read-only sandbox.
- The private repository is accessible through the connected GitHub integration with repository admin/push/pull permissions.
- The existing Ubuntu runner has executed a main-branch workflow successfully as user `ubuntu`; the admission guard denied a feature-branch job. Its current workflow context reported `GITHUB_REF_PROTECTED=false`.

- ChatGPT Free 方案包含 Codex CLI，并支持使用 ChatGPT 账号登录。
- Free / Go 不包含 Codex Cloud，因此本 POC 不依赖 Codex Cloud。
- Codex CLI 支持远端/无头机器使用 `codex login --device-auth` 进行设备码认证；需要先在 ChatGPT 安全设置中启用设备码登录。
- `codex exec` 支持 CI 非交互执行和只读沙箱。
- 当前 ChatGPT GitHub 连接已能访问本私有仓库，并返回 admin/push/pull 权限。
- 现有 Ubuntu Runner 已以 `ubuntu` 用户成功执行 main 分支 Workflow；Admission Guard 已拒绝 feature 分支任务。当前 Workflow 上下文显示 `GITHUB_REF_PROTECTED=false`。

## 3. POC workflow / 验证流程

Workflow: `.github/workflows/chatgpt-codex-channel-poc.yml`

Two manually selected phases:

1. `install-only`: install the official Codex CLI and report its version. No login and no credential creation.
2. `chatgpt-device-auth`: create a temporary `CODEX_HOME`, perform device-code OAuth, confirm the login method, and run one read-only `codex exec --ephemeral` task against the checked-out repository.

两个手动阶段：

1. `install-only`：安装官方 Codex CLI 并报告版本，不登录、不创建凭据。
2. `chatgpt-device-auth`：创建临时 `CODEX_HOME`，执行设备码 OAuth，核验登录方式，并对检出的仓库执行一次只读 `codex exec --ephemeral`。

The device code is short-lived but appears in the private GitHub Actions run log so the account owner can complete authorization. Anyone with access to that repository's Actions logs may be able to see it. Do not run this phase if repository log access is not restricted to trusted people.

设备码有时效，但会显示在私有仓库的 GitHub Actions 日志中，以便仓库所有者完成授权。任何能查看该仓库 Actions 日志的人都可能看到它。如果日志访问权限未限制给可信人员，不要运行认证阶段。

The workflow grants only `contents: read`, disables checkout credential persistence, does not push or create PRs, and does not modify project files. A cleanup step logs out and removes the temporary Codex home even after failure.

Workflow 仅授予 `contents: read`，关闭 checkout 凭据持久化，不推送、不创建 PR、不修改项目文件。清理步骤会在失败时也尝试登出并删除临时 Codex Home。

## 4. Acceptance evidence / 验收证据

A successful run must establish all of the following:

- The runner identity is `VM-0-9-ubuntu` / `ubuntu`.
- Codex CLI installs and reports a version.
- `codex login status` explicitly identifies ChatGPT authentication, not API-key authentication.
- `codex exec` exits successfully in read-only mode and returns `CHATGPT_CODEX_CHANNEL_PROOF_OK`, the repository name, README H1, and Git HEAD.
- No source file is changed and no persistent credential remains after cleanup.

成功运行必须证明：

- Runner 身份为 `VM-0-9-ubuntu` / `ubuntu`。
- Codex CLI 安装成功并输出版本。
- `codex login status` 明确显示 ChatGPT 登录，而非 API Key 登录。
- `codex exec` 在只读模式成功退出，并返回 `CHATGPT_CODEX_CHANNEL_PROOF_OK`、仓库名、README H1 和 Git HEAD。
- 不修改任何源文件，清理后不保留持久化凭据。

## 5. Security gate before persistent operation / 持久化运行前的安全门

**Do not persist ChatGPT OAuth credentials on the current runner yet.**

The existing runner executes as `ubuntu`, can invoke privileged host operations, and the latest verified job reports `GITHUB_REF_PROTECTED=false`. The admission hook is useful but does not replace protected branches, runner isolation, or credential custody controls.

**目前禁止在现有 Runner 上持久化 ChatGPT OAuth 凭据。**

现有 Runner 以 `ubuntu` 用户运行，具备执行特权主机操作的能力；最近核验的 Job 显示 `GITHUB_REF_PROTECTED=false`。Admission Hook 有价值，但不能替代受保护分支、Runner 隔离和凭据托管控制。

Before a persistent A–I worker fleet, require:

1. Main branch protection/ruleset with required review and checks.
2. Dedicated non-sudo worker identity and isolated runner/worktree boundaries.
3. Restricted credential storage, rotation, logout, revocation, and audit evidence.
4. A tested least-privilege GitHub write path for feature branches and draft PRs.
5. Independent security review of prompt injection, untrusted Issue/PR content, command execution, and cross-Owner isolation.

部署持久化 A–I Worker Fleet 前，必须完成：

1. main 分支保护/规则集、必需审查和检查。
2. 无 sudo 的专用 Worker 身份及隔离 Runner/Worktree。
3. 受限凭据存储、轮换、登出、撤销和审计证据。
4. Feature branch / Draft PR 的最小权限 GitHub 写入链路测试。
5. 对提示词注入、不可信 Issue/PR 内容、命令执行和跨 Owner 隔离进行独立安全审查。

## 6. Current decision / 当前决定

The architecture is technically feasible using ChatGPT-authenticated Codex CLI on the remote Ubuntu runner. The ChatGPT-to-GitHub connection is already verified. The remaining unproven step is the actual device-code OAuth login and read-only Codex execution on that runner.

技术路径可行：在远端 Ubuntu Runner 上使用 ChatGPT 账号认证的 Codex CLI。ChatGPT → GitHub 已实际验证。剩余未验证环节是该 Runner 上真实完成设备码 OAuth 登录并执行只读 Codex 任务。

No deployment, persistent login, autonomous source editing, or A–I fleet is claimed by this POC.

本 POC 不代表已部署、已持久登录、已具备自主源码修改能力或 A–I Fleet 已运行。
