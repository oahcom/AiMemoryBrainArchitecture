# ADR-RUN-003 — Owner Worker Isolation and Execution Boundary

- Status: PROPOSED — decision pending
- Source: [Canonical bilingual source](ADR-RUN-003-owner-worker-isolation-and-execution-boundary.md)
- Source Blob: `c6a280ad1c9b3b5539780f46ea17dee2478e7a76`
- Translation status: DRAFT — not adopted; the bilingual source remains authoritative
- Date: 2026-11-17
- Risk: R2 read-only documentation pilot; R3 any code execution, repository write, secret access or host mutation
- Decision owners: A — runtime integration; I — security/governance; pilot Owner — task acceptance; Testing/Quality — isolation verification
- Related: Issue #30; PR #31/#32; ADR-RUN-001; ADR-RUN-002

---

## 1. Context

The Ubuntu host is a persistent execution environment. A compromised or misbehaving worker must not gain host administration, read unrelated user data, access credentials, interfere with another run, or publish after its lease expires.

Isolation is not one control. It is the combination of identity separation, filesystem boundaries, process restrictions, network policy, resource limits, credential separation, publication fencing and auditable cleanup.

This ADR compares execution boundaries for the staged pilot. It does not install containers, alter the Ubuntu host, or authorize arbitrary repository code execution.

## 2. Threat model

Protect against:

- Prompt injection or malicious instructions embedded in Issues, PRs, repository files, build output or memory content.
- Malicious or compromised dependencies and build/test scripts.
- Worker process compromise, accidental privilege escalation or runaway resource consumption.
- Cross-run access to worktrees, caches, temporary files and credentials.
- Stale worker publication after lease expiry or reassignment.
- Untrusted fork/PR code reaching persistent host credentials or services.
- Accidental host mutation and deletion outside the run-owned workspace.

Out of scope for the first pilot:

- A malicious host root/kernel/hypervisor.
- Physical compromise of the server or cloud control plane.
- Strong isolation between mutually hostile tenants on a shared host.
- Execution of arbitrary untrusted fork code.

If the threat model expands to mutually untrusted tenants or arbitrary untrusted code, a single-host systemd sandbox is insufficient; use dedicated VM/microVM or separate hosts.

## 3. Options

| Option | Isolation strength | Operational cost | Main risks | Disposition |
|---|---|---|---|---|
| Shared Unix account + worktree | Low | Low | Cross-run filesystem/process/credential access | Reject for concurrent workers |
| Dedicated Unix identity per worker/run + systemd sandbox | Medium; kernel shared | Low–medium | Kernel escape; sandbox configuration mistakes | **Preferred initial trusted pilot boundary** |
| Rootless OCI container per run (Podman) | Medium–high; kernel shared | Medium | Container misconfiguration, image/dependency supply chain, host socket exposure | Candidate for code-execution stage |
| VM/microVM per run | High relative to shared-kernel options | High | Image lifecycle, orchestration and resource overhead | Required candidate for hostile code or stronger tenant isolation |

## 4. Proposed staged decision

### Stage A — Read-only documentation pilot

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

Stage A is strictly read-only against GitHub. Workers have no GitHub credentials, no App private key, no webhook secret, no model-provider secret, no SSH agent socket, no Docker/Podman socket, no sudo and no access to the user's home directory.

### Stage B — Trusted code/test execution

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

Rootless containers still share the host kernel. They are not a security boundary against kernel vulnerabilities or a malicious host administrator.

### Stage C — Untrusted code

Do not run untrusted fork/PR code on the persistent Ubuntu worker. If a future requirement needs it, use disposable VM/microVM or an isolated external runner pool with no access to the persistent host, Tailnet control plane, App private key, webhook secret or other workers. Destroy the execution environment after the run and preserve only scanned, bounded artifacts.

## 5. Identity and filesystem model

- Coordinator service identity is separate from worker identities.
- Publication Broker identity is separate from both Coordinator and workers.
- No worker runs as `ubuntu`, root or the account that administers Tailscale/GitHub Runner.
- Each run gets a unique work directory with restrictive ownership and permissions; no shared writable worktree.
- Worktree paths are generated from opaque run IDs, not untrusted branch names.
- Symlinks, path traversal, hard links and archive extraction must be constrained to the run root.
- Worker cannot read `/etc`, home directories, SSH material, systemd credentials or secret-store paths except explicitly granted read-only metadata.
- Caches are either disabled or partitioned by trust domain and content digest; no cross-trust writable cache.
- Cleanup deletes only paths whose ownership and run ID are verified; no recursive deletion based on untrusted input.

## 6. Process and network controls

- Worker processes must not inherit coordinator/broker environment variables, file descriptors, sockets or credentials.
- Close all non-required file descriptors before exec.
- No interactive shell or arbitrary command channel in production runtime; commands come from a reviewed allowlist tied to work class.
- Do not mount the Tailscale socket or expose `tailscaled` local API to workers.
- Coordinator/Broker outbound network access is restricted to required GitHub API, model endpoint and telemetry destinations; workers have no network by default in the read-only pilot.
- DNS and proxy configuration are controlled; arbitrary user-provided proxy settings are ignored.
- Enforce process count, memory, CPU, disk quota and execution timeout.
- Kill the entire process cgroup on cancellation, lease loss or timeout; do not only kill the parent PID.

## 7. Credential and publication boundary

- Workers never receive GitHub App private keys, webhook secrets, installation tokens, PATs, SSH private keys, Tailscale auth keys or model-provider master keys.
- Model calls, if required, go through a narrowly scoped broker or credential proxy; workers receive only a per-run capability, not a reusable secret.
- Workers produce proposed diffs and evidence in their run-owned output area.
- Publication Broker validates lease/fencing token, work-item state, prompt digest, Owner approval, allowed paths and expected base/head SHA atomically before every mutation.
- Broker rejects symlinks/path escapes and unexpected file types/sizes.
- If atomic fencing cannot be enforced at the side-effect boundary, write-back is disabled and a human applies patches.

## 8. Observability and cleanup

Record:

- Run ID, Unix UID, systemd unit/scope or container ID, image digest where applicable.
- Resource usage and limit violations.
- Process exit status and bounded action summary.
- Worktree path identity, created files and cleanup result.
- Network policy decision and denied connection counts (not secret payloads).
- Isolation policy version and host/kernel version.

Cleanup must be idempotent and bounded. Preserve logs/evidence according to retention policy; delete only run-owned transient data. Failed cleanup moves the run to a quarantine/cleanup-pending state and pages an operator; do not reuse the workspace.

## 9. Acceptance tests

| ID | Scenario | Pass condition |
|---|---|---|
| ISO-01 | UID separation | Worker UID differs from coordinator, broker, ubuntu and root |
| ISO-02 | Home/SSH access | Worker cannot read user home or SSH material |
| ISO-03 | Credential inheritance | No broker/app/webhook/model secret in env, FD or filesystem |
| ISO-04 | Worktree isolation | Run A cannot read/write Run B workspace |
| ISO-05 | Path traversal | Traversal, symlink and hard-link escapes rejected |
| ISO-06 | Privilege escalation | sudo, setuid, capabilities and privileged namespace unavailable |
| ISO-07 | Socket isolation | No Docker/Podman/Tailscale/SSH agent sockets exposed |
| ISO-08 | Network default deny | Worker outbound blocked unless explicitly allowed |
| ISO-09 | Resource exhaustion | CPU/memory/disk/pids/time limits enforced |
| ISO-10 | Lease-loss termination | Entire cgroup/container stopped; stale publish rejected |
| ISO-11 | Untrusted PR | Cannot execute on persistent worker |
| ISO-12 | Cleanup ownership | Cleanup removes only run-owned paths |
| ISO-13 | Reboot recovery | No orphan worker or reusable stale lease |
| ISO-14 | Audit redaction | No credentials in logs, metrics, artifacts |

All tests require an independent test operator or CI evidence; author-side assertions are not sufficient.

## 10. Open operational inputs

1. Ubuntu distribution/kernel version and cgroup v2 availability.
2. Whether systemd supports the required sandbox directives on the deployed host.
3. Rootless Podman availability and storage/network driver support, if Stage B is pursued.
4. Host CPU/memory/disk budget and maximum concurrent runs.
5. Whether a disposable VM/microVM provider is available for Stage C.
6. Who owns host-level policy, emergency stop and recovery.
7. Whether model calls are proxied or executed by a trusted coordinator service.

## 11. Decision

**OPEN — proposed staged model.** Stage A (read-only, dedicated Unix identity + systemd sandbox) is the preferred first pilot boundary, subject to host capability inspection and independent ISO-01..ISO-14 tests. Stage B (rootless per-run OCI) is not approved until Stage A evidence and a separate security review exist. Stage C (untrusted code) is prohibited on the persistent host and requires disposable VM/microVM or an isolated runner pool.

No host changes, container installation, service deployment or arbitrary code execution are authorized by this ADR.

## 12. References

- [AI-RUN-003 Runtime Architecture](../ai-run-003-event-driven-owner-worker-runtime.en.md)
- [ADR-RUN-001 Durable Store and Transaction Boundaries](ADR-RUN-001-durable-store-and-transaction-boundaries.md)
- [ADR-RUN-002 GitHub App, Webhook Ingress and Secret Management](ADR-RUN-002-github-app-webhook-security-and-secrets.md)
