# Ubuntu Self-Hosted Runner Bootstrap Runbook

**Document:** AI-RUN-002-RUNBOOK  
**Status:** PROPOSED / operator-executed bootstrap  
**Target:** `ubuntu-primary-01` (`vm-0-9-ubuntu`, Tailscale `100.108.116.118`)  
**Tracking:** [Issue #26](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/26)

This runbook establishes a persistent GitHub Actions execution substrate on the Ubuntu host. It does **not** deploy the complete A–I event-driven worker fleet.

## 0. Safety preconditions

- Rotate the SSH password previously disclosed in chat. Do not reuse it.
- Use the cloud provider's trusted server console or an already-authorized administrative session for bootstrap. No local-PC tunnel is required for the steady-state worker.
- Verify the host identity and OS before installing anything.
- Do not paste passwords, private keys, PATs, runner registration tokens, webhook secrets, or model-provider keys into chat, Git, Issues, PRs, logs, or artifacts.
- Generate the GitHub runner registration token immediately before configuration. It is short-lived; never save it in a file or shell history.
- Initially restrict the runner to trusted workflow dispatches / protected branches. Do not execute fork PR code or untrusted PR workflows on this persistent host.
- Use a dedicated non-root account. Never run the runner service as root.

## 1. Host preflight

Run from the Ubuntu server console:

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

Record non-secret output in the deployment evidence. Confirm architecture before choosing the runner package. Confirm adequate disk and memory before proceeding.

## 2. Create a dedicated service identity

Review the target directory and account policy before running:

```bash
sudo useradd --create-home --shell /bin/bash actions-runner
sudo install -d -o actions-runner -g actions-runner -m 0750 /opt/actions-runner
```

Do not add this account to `sudo`, `docker`, or other privileged groups for the initial pilot.

## 3. Obtain the runner package and one-time registration token

1. Open repository **Settings → Actions → Runners → New self-hosted runner**.
2. Select Linux and the architecture confirmed in Step 1.
3. Follow GitHub's current package download and checksum-verification instructions.
4. Generate the registration token just-in-time. Treat it as a secret and do not store it.
5. Download and verify the package as an administrator, then transfer ownership to `actions-runner`.

Use GitHub's displayed commands for the current runner release rather than pinning an unverified version in this document.

## 4. Configure as a non-root service

As `actions-runner`, configure the runner for this repository with a distinctive label such as `ai-worker`. Supply the one-time token interactively; do not put it in shell command history, process listings, or logs.

Example shape only (replace values interactively; never commit the token):

```bash
./config.sh --url https://github.com/oahcom/AiMemoryBrainArchitecture --token <ONE_TIME_TOKEN> --name ubuntu-primary-01 --labels ai-worker --work _work
```

Install and start the service using the runner's generated service integration, following the current GitHub instructions. Verify the service runs as `actions-runner`, is enabled at boot, and is visible as **Online** in repository Settings → Actions → Runners.

Do not enable broad SSH access from ChatGPT or grant the runner broad administrative credentials as part of this step.

## 5. Initial diagnostic workflow

The first workflow must be harmless and read-only. It may report hostname, OS, architecture, runner labels, disk, memory, and Tailscale service state. It must not:
- print environment variables wholesale;
- inspect credential stores or secret files;
- upload home directories or runner workspaces;
- run arbitrary issue/PR-supplied scripts;
- access production systems or modify repository branches.

Use an explicit `workflow_dispatch` trigger and the `self-hosted` + `ai-worker` labels. Protect workflow changes with review and branch protection.

## 6. Acceptance evidence

Do not mark the host WORKER_ONLINE until all are evidenced:

- [ ] OS, architecture, resources, time sync and network preflight recorded.
- [ ] Host identity verified out-of-band.
- [ ] Disclosed password rotated.
- [ ] Dedicated non-root runner account and directory ownership verified.
- [ ] Runner visible Online with expected labels.
- [ ] Harmless diagnostic workflow succeeds.
- [ ] Runner service survives reboot and reconnects.
- [ ] No secrets in Git, logs, artifacts, Issues or PR comments.
- [ ] Untrusted PR workflows cannot reach this runner or its secrets.
- [ ] Emergency stop / runner removal procedure tested.

Even after these pass, the status is only **RUNNER_ONLINE**. It is not proof of 24/7 A–I autonomous operation, durable event processing, independent Owner identity, lease fencing, crash recovery, or end-to-end governance.

## 7. Rollback / emergency stop

- Disable the runner in GitHub repository Settings → Actions → Runners.
- Stop and disable its system service on Ubuntu.
- Remove the runner registration using the documented GitHub procedure.
- Revoke any credentials exposed during the incident.
- Preserve sanitized logs and record the incident in Issue #26.

## Current status

The operator confirmed Tailscale is enabled and active at `100.108.116.118`. The ChatGPT execution environment is not currently joined to that Tailnet and has not remotely accessed the host. Runner installation and all acceptance checks remain **NOT RUN**.
