# ADR-RUN-003 — Owner Worker Isolation and Execution Boundary
# ADR-RUN-003 — Owner Worker 隔离与执行边界

- **Status / 状态:** PROPOSED — decision pending / 提案中——待决议
- **Date / 日期:** 2026-11-17
- **Risk / 风险:** R2 read-only documentation pilot; R3 any code execution, repository write, secret access or host mutation / 只读文档试点 R2；任何代码执行、仓库写入、秘密访问或主机变更均为 R3
- **Decision owners / 决策责任:** A — runtime integration; I — security/governance; pilot Owner — task acceptance; Testing/Quality — isolation verification / A 负责 Runtime 集成；I 负责安全治理；试点 Owner 负责任务验收；Testing/Quality 负责隔离验证
- **Related / 关联:** Issue #30; PR #31/#32; ADR-RUN-001; ADR-RUN-002

---

## 1. Context / 背景

The Ubuntu host is a persistent execution environment. A compromised or misbehaving worker must not gain host administration, read unrelated user data, access credentials, interfere with another run, or publish after its lease expires.

Ubuntu 主机是持久化执行环境。被攻陷或行为异常的 Worker 不得获得主机管理权限、读取无关用户数据、访问凭据、干扰其他 Run，或在租约过期后继续发布。

Isolation is not one control. It is the combination of identity separation, filesystem boundaries, process restrictions, network policy, resource limits, credential separation, publication fencing and auditable cleanup.

隔离不是单一控制，而是身份分离、文件系统边界、进程限制、网络策略、资源限制、凭据隔离、发布 fencing 和可审计清理的组合。

This ADR compares execution boundaries for the staged pilot. It does not install containers, alter the Ubuntu host, or authorize arbitrary repository code execution.

本 ADR 比较分阶段试点的执行边界，不代表已安装容器、修改 Ubuntu 主机或授权执行任意仓库代码。

## 2. Threat model / 威胁模型

Protect against / 防护对象：

- Prompt injection or malicious instructions embedded in Issues, PRs, repository files, build output or memory content.
- Malicious or compromised dependencies and build/test scripts.
- Worker process compromise, accidental privilege escalation or runaway resource consumption.
- Cross-run access to worktrees, caches, temporary files and credentials.
- Stale worker publication after lease expiry or reassignment.
- Untrusted fork/PR code reaching persistent host credentials or services.
- Accidental host mutation and deletion outside the run-owned workspace.

- Issue、PR、仓库文件、构建输出或记忆内容中的 Prompt Injection/恶意指令。
- 恶意或受损依赖、构建/测试脚本。
- Worker 进程被攻陷、意外提权或资源失控。
- 跨 Run 访问 Worktree、缓存、临时文件和凭据。
- 租约过期或重新分配后旧 Worker 仍发布。
- 不可信 Fork/PR 代码访问持久主机凭据或服务。
- 对 Run 工作区之外的主机资源进行意外修改或删除。

Out of scope for the first pilot / 首轮试点不覆盖：

- A malicious host root/kernel/hypervisor.
- Physical compromise of the server or cloud control plane.
- Strong isolation between mutually hostile tenants on a shared host.
- Execution of arbitrary untrusted fork code.

- 恶意主机 Root/Kernel/Hypervisor。
- 服务器或云控制面的物理/底层攻陷。
- 同一主机上互不信任租户之间的强隔离。
- 任意不可信 Fork 代码执行。

If the threat model expands to mutually untrusted tenants or arbitrary untrusted code, a single-host systemd sandbox is insufficient; use dedicated VM/microVM or separate hosts.

如果威胁模型扩展到互不信任租户或任意不可信代码，单机 systemd Sandbox 不足；必须使用独立 VM/microVM 或独立主机。

## 3. Options / 方案比较

| Option / 方案 | Isolation strength / 隔离强度 | Operational cost / 运维成本 | Main risks / 主要风险 | Disposition / 结论 |
|---|---|---|---|---|
| Shared Unix account + worktree | Low / 低 | Low / 低 | Cross-run filesystem/process/credential access / 跨 Run 文件、进程和凭据访问 | Reject for concurrent workers / 拒绝并发 Worker 使用 |
| Dedicated Unix identity per worker/run + systemd sandbox | Medium; kernel shared / 中；共享 Kernel | Low–medium / 低至中 | Kernel escape; sandbox configuration mistakes / Kernel Escape、Sandbox 配置错误 | **Preferred initial trusted pilot boundary / 首轮可信试点首选** |
| Rootless OCI container per run (Podman) | Medium–high; kernel shared / 中高；共享 Kernel | Medium / 中 | Container misconfiguration, image/dependency supply chain, host socket exposure / 容器配置、镜像供应链、主机 Socket 暴露 | Candidate for code-execution stage / 代码执行阶段候选 |
| VM/microVM per run | High relative to shared-kernel options / 相对共享 Kernel 方案较高 | High / 高 | Image lifecycle, orchestration and resource overhead / 镜像生命周期、编排和资源开销 | Required candidate for hostile code or stronger tenant isolation / 恶意代码或更强租户隔离候选 |

## 4. Proposed staged decision / 分阶段提议

### Stage A — Read-only documentation pilot / A 阶段：只读文档试点

Use a dedicated non-root service account for the runtime coordinator. Run each worker attempt under a dedicated transient Unix identity or a strictly isolated systemd service scope with:

- `NoNewPrivileges=yes`
- `PrivateTmp=yes`
- `ProtectSystem=strict`
- `ProtectHome=yes` unless a narrowly scoped read-only path is explicitly required
- `PrivateDevices=yes`
- `ProtectKernelTunables=yes`, `ProtectKernelModules=yes`, `ProtectControlGroups=yes`
- `RestrictSUIDSGID=yes`, `LockPersonality=yes`
- `CapabilityBoundingSet=` (empty) and `AmbientCapabilities=` (empty)
- `UMask=0077`
- explicit `ReadWritePaths=` only for the run-owned worktree, scratch directory and required evidence spool
- `RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6` only where required; tighten further after network design
- CPU, memory, task-count, file-size, open-file and wall-clock limits
- explicit system call filtering where supported and tested

为 Runtime Coordinator 使用专用非 Root 服务账号。每次 Worker Attempt 使用专用临时 Unix 身份或严格隔离的 systemd Service Scope，并启用上述系统限制。仅允许访问本 Run Worktree、Scratch 和必要 Evidence Spool。

Stage A is strictly read-only against GitHub. Workers have no GitHub credentials, no App private key, no webhook secret, no model-provider secret, no SSH agent socket, no Docker/Podman socket, no sudo and no access to the user's home directory.

A 阶段对 GitHub 严格只读。Worker 不得持有 GitHub 凭据、App 私钥、Webhook Secret、模型供应商秘密、SSH Agent Socket、Docker/Podman Socket，不得 sudo，也不得访问用户 Home 目录。

### Stage B — Trusted code/test execution / B 阶段：可信代码/测试执行

Only after Stage A passes independent isolation tests, consider a rootless OCI container per run. Requirements:

- Rootless Podman (or equivalent) with no privileged mode.
- No host container-engine socket mounted into the container.
- Read-only, digest-pinned base image; reproducible image build and vulnerability scan.
- Per-run ephemeral container and filesystem; no shared writable cache by default.
- Explicit bind mounts only for the run-owned worktree and bounded output directory.
- Drop all Linux capabilities; no-new-privileges; seccomp and AppArmor/SELinux profile where available.
- Network disabled by default; allowlist only required destinations and ports.
- Resource limits and hard wall-clock timeout.
- No host credentials or long-lived GitHub tokens inside the container.
- Container image and dependency provenance recorded in run evidence.

只有 A 阶段通过独立隔离测试后，才评估每 Run 一个 Rootless OCI Container。不得使用 Privileged 模式、不得挂载主机容器引擎 Socket、使用只读且 Digest Pin 的基础镜像、每 Run 临时文件系统、显式挂载、移除 Linux Capabilities、seccomp/AppArmor/SELinux、默认禁网、资源限制、无主机凭据，并记录镜像/依赖来源。

Rootless containers still share the host kernel. They are not a security boundary against kernel vulnerabilities or a malicious host administrator.

Rootless Container 仍共享主机 Kernel，不能防护 Kernel 漏洞或恶意主机管理员。

### Stage C — Untrusted code / C 阶段：不可信代码

Do not run untrusted fork/PR code on the persistent Ubuntu worker. If a future requirement needs it, use disposable VM/microVM or an isolated external runner pool with no access to the persistent host, Tailnet control plane, App private key, webhook secret or other workers. Destroy the execution environment after the run and preserve only scanned, bounded artifacts.

不得在持久 Ubuntu Worker 上运行不可信 Fork/PR 代码。若未来确有需求，使用一次性 VM/microVM 或隔离外部 Runner Pool，不得访问持久主机、Tailnet 控制面、App 私钥、Webhook Secret 或其他 Worker。Run 后销毁执行环境，只保留经过扫描且有界的 Artifact。

## 5. Identity and filesystem model / 身份与文件系统模型

- Coordinator service identity is separate from worker identities.
- Publication Broker identity is separate from both Coordinator and workers.
- No worker runs as `ubuntu`, root or the account that administers Tailscale/GitHub Runner.
- Each run gets a unique work directory with restrictive ownership and permissions; no shared writable worktree.
- Worktree paths are generated from opaque run IDs, not untrusted branch names.
- Symlinks, path traversal, hard links and archive extraction must be constrained to the run root.
- Worker cannot read `/etc`, home directories, SSH material, systemd credentials or secret-store paths except explicitly granted read-only metadata.
- Caches are either disabled or partitioned by trust domain and content digest; no cross-trust writable cache.
- Cleanup deletes only paths whose ownership and run ID are verified; no recursive deletion based on untrusted input.

- Coordinator、Publication Broker 和 Worker 使用不同身份。
- Worker 不以 `ubuntu`、Root 或管理 Tailscale/GitHub Runner 的账号运行。
- 每个 Run 有唯一工作目录，严格限制所有者和权限，不共享可写 Worktree。
- Worktree 路径由不透明 Run ID 生成，不直接使用不可信 Branch Name。
- 符号链接、路径穿越、硬链接和 Archive 解压必须限制在 Run Root 内。
- Worker 不得读取 `/etc`、Home、SSH 材料、systemd Credentials 或 Secret Store 路径，除非明确授予只读元数据。
- Cache 默认关闭，或按信任域和内容摘要分区；不同信任域不得共享可写 Cache。
- 清理操作必须验证路径所有权和 Run ID；不得根据不可信输入递归删除。

## 6. Process and network controls / 进程与网络控制

- Worker processes must not inherit coordinator/broker environment variables, file descriptors, sockets or credentials.
- Close all non-required file descriptors before exec.
- No interactive shell or arbitrary command channel in production runtime; commands come from a reviewed allowlist tied to work class.
- Do not mount the Tailscale socket or expose `tailscaled` local API to workers.
- Coordinator/Broker outbound network access is restricted to required GitHub API, model endpoint and telemetry destinations; workers have no network by default in the read-only pilot.
- DNS and proxy configuration are controlled; arbitrary user-provided proxy settings are ignored.
- Enforce process count, memory, CPU, disk quota and execution timeout.
- Kill the entire process cgroup on cancellation, lease loss or timeout; do not only kill the parent PID.

- Worker 不继承 Coordinator/Broker 环境变量、文件描述符、Socket 或凭据。
- Exec 前关闭所有非必要文件描述符。
- 生产 Runtime 不提供交互 Shell 或任意命令通道；命令来自绑定 Work Class 的审查白名单。
- 不挂载 Tailscale Socket，不向 Worker 暴露 `tailscaled` Local API。
- Coordinator/Broker 的网络出口限制为 GitHub API、模型 Endpoint 和 Telemetry 必需目标；只读试点 Worker 默认无网络。
- DNS/Proxy 由系统控制，忽略任意用户提供的 Proxy 设置。
- 限制进程数、内存、CPU、磁盘配额和执行时间。
- 取消、租约丢失或超时时，杀死整个 Process Cgroup，不仅杀父 PID。

## 7. Credential and publication boundary / 凭据与发布边界

- Workers never receive GitHub App private keys, webhook secrets, installation tokens, PATs, SSH private keys, Tailscale auth keys or model-provider master keys.
- Model calls, if required, go through a narrowly scoped broker or credential proxy; workers receive only a per-run capability, not a reusable secret.
- Workers produce proposed diffs and evidence in their run-owned output area.
- Publication Broker validates lease/fencing token, work-item state, prompt digest, Owner approval, allowed paths and expected base/head SHA atomically before every mutation.
- Broker rejects symlinks/path escapes and unexpected file types/sizes.
- If atomic fencing cannot be enforced at the side-effect boundary, write-back is disabled and a human applies patches.

- Worker 永远不获得 GitHub App 私钥、Webhook Secret、Installation Token、PAT、SSH 私钥、Tailscale Auth Key 或模型供应商主密钥。
- 如需模型调用，通过最小权限 Broker/凭据代理；Worker 只获得每 Run Capability，不获得可复用秘密。
- Worker 在 Run 专属输出区生成候选 Diff 和证据。
- Publication Broker 每次变更前原子验证租约/fencing token、Work Item 状态、Prompt 摘要、Owner 批准、允许路径和预期 Base/Head SHA。
- Broker 拒绝符号链接/路径逃逸及意外文件类型/大小。
- 若无法在副作用边界强制原子 fencing，则关闭回写，由人类应用 Patch。

## 8. Observability and cleanup / 可观测性与清理

Record / 记录：

- Run ID, Unix UID, systemd unit/scope or container ID, image digest where applicable.
- Resource usage and limit violations.
- Process exit status and bounded action summary.
- Worktree path identity, created files and cleanup result.
- Network policy decision and denied connection counts (not secret payloads).
- Isolation policy version and host/kernel version.

记录 Run ID、Unix UID、systemd Unit/Scope 或 Container ID、镜像 Digest、资源使用和违规、进程退出状态、有界操作摘要、Worktree 身份、文件清单、清理结果、网络策略决策/拒绝计数、隔离策略版本和 Host/Kernel 版本。

Cleanup must be idempotent and bounded. Preserve logs/evidence according to retention policy; delete only run-owned transient data. Failed cleanup moves the run to a quarantine/cleanup-pending state and pages an operator; do not reuse the workspace.

清理必须幂等且有界。按保留策略保存日志/证据，只删除 Run 自有临时数据。清理失败则进入隔离/待清理状态并通知运维；不得复用该 Workspace。

## 9. Acceptance tests / 验收测试

| ID | Scenario / 场景 | Pass condition / 通过条件 |
|---|---|---|
| ISO-01 | UID separation / UID 隔离 | Worker UID differs from coordinator, broker, ubuntu and root / Worker UID 与 Coordinator、Broker、ubuntu、root 不同 |
| ISO-02 | Home/SSH access / Home/SSH 访问 | Worker cannot read user home or SSH material / 无法读取用户 Home 或 SSH 材料 |
| ISO-03 | Credential inheritance / 凭据继承 | No broker/app/webhook/model secret in env, FD or filesystem / 环境、FD、文件系统无秘密 |
| ISO-04 | Worktree isolation / Worktree 隔离 | Run A cannot read/write Run B workspace / Run A 无法读写 Run B |
| ISO-05 | Path traversal / 路径穿越 | Traversal, symlink and hard-link escapes rejected / 拒绝穿越、符号链接和硬链接逃逸 |
| ISO-06 | Privilege escalation / 提权 | sudo, setuid, capabilities and privileged namespace unavailable / sudo、setuid、Capabilities、特权 Namespace 不可用 |
| ISO-07 | Socket isolation / Socket 隔离 | No Docker/Podman/Tailscale/SSH agent sockets exposed / 不暴露相关 Socket |
| ISO-08 | Network default deny / 网络默认拒绝 | Worker outbound blocked unless explicitly allowed / 未明确允许时阻断 Worker 出口 |
| ISO-09 | Resource exhaustion / 资源耗尽 | CPU/memory/disk/pids/time limits enforced / 资源限制生效 |
| ISO-10 | Lease-loss termination / 租约丢失终止 | Entire cgroup/container stopped; stale publish rejected / 整个 Cgroup/Container 停止且旧发布被拒绝 |
| ISO-11 | Untrusted PR / 不可信 PR | Cannot execute on persistent worker / 无法在持久 Worker 执行 |
| ISO-12 | Cleanup ownership / 清理所有权 | Cleanup removes only run-owned paths / 只清理 Run 自有路径 |
| ISO-13 | Reboot recovery / 重启恢复 | No orphan worker or reusable stale lease / 无孤儿 Worker 或可复用旧租约 |
| ISO-14 | Audit redaction / 审计脱敏 | No credentials in logs, metrics, artifacts / 日志、指标、Artifact 无凭据 |

All tests require an independent test operator or CI evidence; author-side assertions are not sufficient.

所有测试必须有独立测试操作者或 CI 证据；作者自述不足以验收。

## 10. Open operational inputs / 运维输入待补

1. Ubuntu distribution/kernel version and cgroup v2 availability.
2. Whether systemd supports the required sandbox directives on the deployed host.
3. Rootless Podman availability and storage/network driver support, if Stage B is pursued.
4. Host CPU/memory/disk budget and maximum concurrent runs.
5. Whether a disposable VM/microVM provider is available for Stage C.
6. Who owns host-level policy, emergency stop and recovery.
7. Whether model calls are proxied or executed by a trusted coordinator service.

部署前需确认 Ubuntu 发行版/Kernel、cgroup v2、systemd Sandbox 指令支持、Rootless Podman 能力、主机资源预算、并发数、VM/microVM 可用性、主机策略负责人/紧急停止/恢复责任，以及模型调用代理方式。

## 11. Decision / 决议

**OPEN — proposed staged model.** Stage A (read-only, dedicated Unix identity + systemd sandbox) is the preferred first pilot boundary, subject to host capability inspection and independent ISO-01..ISO-14 tests. Stage B (rootless per-run OCI) is not approved until Stage A evidence and a separate security review exist. Stage C (untrusted code) is prohibited on the persistent host and requires disposable VM/microVM or an isolated runner pool.

**OPEN——提议的分阶段模型。** A 阶段（只读、专用 Unix 身份 + systemd Sandbox）是首轮试点首选边界，但须先检查主机能力并通过独立 ISO-01..ISO-14 测试。B 阶段（每 Run Rootless OCI）必须等待 A 阶段证据和单独安全审查，不在此批准。C 阶段（不可信代码）禁止在持久主机运行，必须使用一次性 VM/microVM 或隔离 Runner Pool。

No host changes, container installation, service deployment or arbitrary code execution are authorized by this ADR.

本 ADR 不授权任何主机变更、容器安装、服务部署或任意代码执行。

## 12. References / 参考

- [AI-RUN-003 Runtime Architecture](../ai-run-003-event-driven-owner-worker-runtime.en.md)
- [ADR-RUN-001 Durable Store and Transaction Boundaries](ADR-RUN-001-durable-store-and-transaction-boundaries.md)
- [ADR-RUN-002 GitHub App, Webhook Ingress and Secret Management](ADR-RUN-002-github-app-webhook-security-and-secrets.md)
