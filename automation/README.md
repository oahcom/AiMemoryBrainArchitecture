# Executable Owner Worker MVP / 可执行 Owner Worker 最小版本

## English

This is executable code, not a deployed service. It polls open GitHub Issues carrying both `ai-ready` and `owner-a`, persists claims in SQLite WAL, invokes the OpenAI Responses API, and opens a Draft PR.

The model may create Markdown files only below `automation/owner-output/`. It cannot write source code, workflows, credentials, or policies. The worker does not execute generated content and never merges. Every output PR requires CI and independent review.

Configure `GITHUB_TOKEN`, `GITHUB_REPOSITORY`, and `OPENAI_API_KEY` out-of-band in `/etc/ai-owner-worker/worker.env`. The GitHub token should be repository-scoped with only Issues read/write, Contents read/write, and Pull Requests write. Keep the env file root-owned and readable only by the service group. Never commit real credentials.

From a trusted checkout of the reviewed and merged revision, run `sudo automation/scripts/install-owner-worker.sh`, populate `/etc/ai-owner-worker/worker.env`, then run `sudo systemctl enable --now ai-owner-worker`. Inspect with `systemctl status ai-owner-worker` and `journalctl -u ai-owner-worker`. Do not install from an unreviewed PR.

## 中文

这是可执行代码，**不是已部署服务**。程序轮询同时具有 `ai-ready` 和 `owner-a` 标签的开放 GitHub Issue，将任务认领写入 SQLite WAL，调用 OpenAI Responses API，并创建 Draft PR。

模型只能在 `automation/owner-output/` 下创建 Markdown 文件，不能写项目源代码、Workflow、凭据或治理策略。Worker 不执行生成内容，也不会自动合并。每个输出 PR 都必须通过 CI 和独立审查。

在服务器外部安全配置 `/etc/ai-owner-worker/worker.env` 中的 `GITHUB_TOKEN`、`GITHUB_REPOSITORY` 和 `OPENAI_API_KEY`。GitHub Token 应限定在本仓库，并仅授予 Issues 读写、Contents 读写和 Pull Requests 写权限。环境文件由 root 持有，仅服务组可读。真实凭据绝不能提交到 Git。

必须从已审查并合并的可信版本执行：`sudo automation/scripts/install-owner-worker.sh`，然后安全填写 `/etc/ai-owner-worker/worker.env`，最后执行 `sudo systemctl enable --now ai-owner-worker`。使用 `systemctl status ai-owner-worker` 和 `journalctl -u ai-owner-worker` 检查状态。不得从未经审查的 PR 安装。

## Current limitations / 当前限制

- Single pilot Owner only; no A–I fleet.
- Output is restricted to Markdown artifacts; project-source implementation is not yet enabled.
- The process requires externally provisioned GitHub and model credentials.
- The worker has not been installed or started on the Ubuntu host.
- No autonomous merge, destructive action, or production readiness is claimed.
