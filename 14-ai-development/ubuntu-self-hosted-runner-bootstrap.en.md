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
      last_verification_note: "The server-side GitHub Actions Runner was retired by Owner decision; active CI now uses GitHub-hosted ubuntu-latest runners."
    usage_status: Deprecated
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: "The server-side GitHub Actions Runner is retired. This bootstrap procedure is retained only as historical evidence and must not be used to install or restore a server runner."
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

> **RETIRED — 2026-11-23.** Owner decision: this server no longer runs GitHub Actions self-hosted runners. CI uses GitHub-hosted `ubuntu-latest` runners. This file is retained as historical evidence only; do not use it to install, start, or restore a server runner.

# Ubuntu Self-Hosted Runner Bootstrap Runbook

**Document:** AI-RUN-002-RUNBOOK  
**Version:** 1.1 (revised 2026-11-17)  
**Deployment status:** RETIRED 2026-11-23. **Security acceptance:** historical record only.
**Target:** `[HOST IDENTIFIER WITHHELD]`, runner name `[RUNNER IDENTIFIER WITHHELD]`  
**Tracking:** [Issue #26](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/26)  
**Normative architecture statement:** DOC-OPS-001, `docs/zh-CN/14-ai-development/ci-runner-operations.md` and `docs/en/14-ai-development/ci-runner-operations.md`. That pair states the deployed shape, the security boundary, and the admission policy bilingually. This file is the execution procedure.  
**Translation:** TRANSLATED / 中文版已同步（`ubuntu-self-hosted-runner-bootstrap.zh-CN.md`）. This procedure is English-only; the normative decision and the security boundary live in the bilingual DOC-OPS-001 pair and must be read there.

## Revision summary (v1.0 → v1.1)

| Item | v1.0 (planned) | v1.1 (executed and accepted) |
|---|---|---|
| Service account | dedicated `actions-runner` | **`<RUNNER_SERVICE_ACCOUNT>`** (also the login account, passwordless sudo) |
| Install path | `/opt/actions-runner` (0750) | **`<RUNNER_INSTALL_DIR>`** |
| Labels | `ai-worker` | **`self-hosted,linux,x64`** (custom label deferred, see §4.2) |
| Untrusted-trigger isolation | "restrict to trusted dispatches" — human discipline | **enforced in the runner** by a job-started hook (§4.1) |
| Status | PROPOSED | ACTIVE; acceptance evidence in §6 |

The account and path deviations are **recorded but not security-accepted**. Rationale and residual risk are stated below. Do not paraphrase this as "deployed as specified" or as approved risk acceptance.

## 0. Safety preconditions

- Rotate any credential that may have been exposed. Do not reuse it.
- Use the cloud provider's trusted server console or an already-authorized administrative session for bootstrap. No local-PC tunnel is required for the steady-state worker.
- Verify the host identity and OS before installing anything.
- Do not paste passwords, private keys, PATs, runner registration tokens, webhook secrets, or model-provider keys into chat, Git, Issues, PRs, logs, or artifacts.
- Generate the GitHub runner registration token immediately before configuration. It is short-lived; never save it in a file or shell history.
- Keep the runner off untrusted code. As of v1.1 this is **enforced mechanically** by the admission hook in §4.1, not by discipline alone.
- Run the service as a non-root user. Never run the runner service as root. The executed deployment satisfies "non-root" but not "dedicated"; see §0.1.

## 0.1 Accepted deviations

| Deviation | Recorded on (not approval) | Compensating control | Residual risk |
|---|---|---|---|
| Runner service runs as `<RUNNER_SERVICE_ACCOUNT>`, which holds passwordless sudo | 2026-11-17 | L1 admission hook denies every job whose ref is not `refs/heads/main` or whose event is not `push` / `workflow_dispatch` / `schedule` | A workflow that *is* admitted can `sudo`. Containment would need `NoNewPrivileges=yes` or a separate account; neither was implemented |
| Installed under `<RUNNER_INSTALL_DIR>` instead of `/opt/actions-runner` | 2026-11-17 | `.credentials`, `.credentials_rsaparams`, `.runner` are mode 600; the runner directory is 755 and owned by `<RUNNER_SERVICE_ACCOUNT>` | A local user with access to the `<RUNNER_SERVICE_ACCOUNT>` account can read the runner credentials. There are no other interactive accounts on the host today |
| Labels are the platform defaults, not `ai-worker` | 2026-11-17 | The repository has exactly one self-hosted runner; a job cannot land elsewhere | If a second self-hosted runner is registered, restore the custom label first (see §4.2) |

**Security acceptance:** this deviation remains unapproved for security acceptance until the infrastructure/security Owner records an explicit decision. Reassess if any of the following happens — a second self-hosted runner is registered; a second interactive account is created on the host; the repository becomes public; branch protection on `main` is enabled and someone asks to relax the hook.

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

Then the build toolchain. `cargo test --workspace --all-targets` compiles bundled SQLite through `cc::Build`, so a compiler is a precondition for the job the runner exists to run — and a *present* `cc` is not a *working* one. A `gcc` with no `cc1` behind it is found by `command -v` and still dies inside `libsqlite3-sys`. Check presence and capability separately:

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

`cc ... cannot compile` is a provisioning failure, not a dependency bug: install `build-essential` (or set `CC` to a real toolchain) before registering the runner. If `cc` is `MISSING` outright, the same applies — the next `cargo test` would fail inside `libsqlite3-sys`, which reads as a `rusqlite` problem rather than a host problem.

Record non-secret output in the deployment evidence. Confirm architecture before choosing the runner package: **this host is `x86_64`**. A package chosen from an `arch=arm64` page is the wrong artifact; a partially downloaded package additionally fails `tar tzf` and leaves no `config.sh`. Verify both the architecture and the archive hash before extracting.

## 2. Service identity

**As executed:** the runner uses the existing `<RUNNER_SERVICE_ACCOUNT>` account and `<RUNNER_INSTALL_DIR>`. No new account was created. Tighten credential permissions immediately after registration:

```bash
chmod 600 <RUNNER_INSTALL_DIR>/.credentials <RUNNER_INSTALL_DIR>/.credentials_rsaparams <RUNNER_INSTALL_DIR>/.runner
```

**Planned shape, not executed:** `useradd --create-home --shell /bin/bash actions-runner` plus `install -d -o actions-runner -g actions-runner -m 0750 /opt/actions-runner`, with the account kept out of `sudo` and `docker`. Adopting it is a deliberate migration, not a cleanup: it requires re-registration and a short runner outage.

## 3. Obtain the runner package and one-time registration token

1. Open repository **Settings → Actions → Runners → New self-hosted runner**.
2. Select Linux and the architecture confirmed in §1 (`x64` on this host).
3. Download the package and **verify the published SHA256** before extracting.
4. Generate the registration token just-in-time. Treat it as a secret; do not store it.
5. Transfer ownership to the account that runs the service.

Use GitHub's displayed commands for the current runner release rather than pinning an unverified version here.

## 4. Configure the service (as executed)

Tokens are visible to privileged local process inspection while `config.sh` runs; do not claim otherwise. Issue the token immediately before use, disable shell history for that shell, and close it afterwards.

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

The generated unit is `<RUNNER_SERVICE>.service`. Two drop-ins are required; both are load-bearing.

`/etc/systemd/system/<RUNNER_SERVICE>.service.d/proxy.conf`:

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

`...service.d/guard.conf`:

```ini
[Service]
Environment="ACTIONS_RUNNER_HOOK_JOB_STARTED=<RUNNER_INSTALL_DIR>/hooks/job-started-guard.sh"
```

**`runsvc.sh` in this runner version does not read `.env`.** Proxy settings must come from the unit (drop-in), not from `.runner`'s sibling `.env`. Verify by reading the process environment, not by looking at the file:

```bash
PID=$(pgrep -f "Runner.Listener run" | head -1)
sudo tr '\0' '\n' < /proc/$PID/environ | cut -d= -f1 | grep -E '^(HTTP_PROXY|HTTPS_PROXY|http_proxy|https_proxy|NO_PROXY|no_proxy|ACTIONS_RUNNER_HOOK_JOB_STARTED)
```

Egress routing, proxy endpoints, private address ranges and host-local service topology are operator-controlled infrastructure details. Do not record them in this repository; verify them through the access-controlled operations channel. This runbook requires only the approved HTTPS egress policy needed for GitHub Actions.

## 4.1 Admission control (REQUIRED)

This is a service-layer admission control. It reduces untrusted-trigger exposure but does not make a sudo-capable runner isolated or security-accepted. It can be bypassed by changes to the trusted host or runner service configuration.

**L1 — service layer (binding).** `ACTIONS_RUNNER_HOOK_JOB_STARTED` points at `<RUNNER_INSTALL_DIR>/hooks/job-started-guard.sh`. The hook runs before any workflow step and fails the job unless:

- `GITHUB_REF` is exactly `refs/heads/main`, **and**
- `GITHUB_EVENT_NAME` is one of `push`, `workflow_dispatch`, `schedule`.

If the ref cannot be resolved, the job is denied (fail-closed).

Do not assume the hook receives a context file. On runner 2.338.2 the hook is executed as `bash -e <hook>` with no argv and no stdin; the verdict must read the environment the worker exports. An implementation that expects `$1` denies every job — observed on 2026-11-17 as a failed run before the fix.

Artifacts and operators' handles:

| Path | Purpose |
|---|---|
| `<RUNNER_INSTALL_DIR>/hooks/guard.log` | One line per decision: verdict, ref, event, source |
| `<RUNNER_INSTALL_DIR>/hooks/last-decision.txt` | Full record of the last decision (ref, event, `GITHUB_REF_PROTECTED`, run id, actors) |
| `<RUNNER_INSTALL_DIR>/hooks/observe.flag` | Emergency rollback: present ⇒ log only, never block. Create it, investigate, remove it |

**L1 evidence (2026-11-17, this host):**

| Run | Trigger | Verdict | Job |
|---|---|---|---|
| 44049832708 | `push` → `refs/heads/main` | ALLOW | `Succeeded` — first real execution on this runner |
| 44050069421 | `push` → `refs/heads/ci/admission-negative-test` | DENY `ref_not_default_branch` | `Failed` with **zero steps executed** |
| 44050467500 | `push` → `refs/heads/main` | ALLOW | `Succeeded` |

**L2 — repository layer (preventive).** `scripts/ci/audit_runner_admission.py` rejects, for any workflow with a `self-hosted` job: untrusted triggers (`pull_request`, `pull_request_target`, `issue_comment`, `workflow_run`, …), a `push` without a `branches:` filter, `push.branches` naming anything other than `main`, and a `runs-on` that cannot be statically evaluated. `.github/workflows/runner-admission-policy.yml` runs it on a GitHub-hosted runner. Bind it by making that check required on `main`.

**L3 — organization layer (Owner action, not enabled).** Branch protection on `main`, Environments with required approval for self-hosted jobs, and a repository-scoped runner group. Until branch protection exists, `main` itself is unprotected — the hook observed `GITHUB_REF_PROTECTED=false`, so the "trusted branch" is a convention: anyone who can push to `main` can change what will run there.

## 4.2 Custom label (deferred)

`--labels self-hosted,linux,x64` are platform labels. The distinctive `ai-worker` label from v1.0 is not set, because adding or renaming labels requires re-registration with a fresh one-time token. Do this before a second self-hosted runner is registered; until then, prefer `runs-on: [self-hosted, linux, x64]` so workflows match reality.

## 5. Diagnostic workflows

The first workflow MUST be harmless and read-only. Two exist:

- `.github/workflows/runner-guard-selftest.yml` — `push` on its own path plus `workflow_dispatch`; prints execution context and the guard's decision record, and fails if `guard.log` has no `ALLOW ref=refs/heads/main`.
- `14-ai-development/…` diagnostics workflow — `workflow_dispatch` only; reports hostname, OS, architecture, disk, memory, Tailscale service state.

Neither may print environment variables wholesale, read credential stores, upload home directories or workspaces, run issue/PR-supplied scripts, or touch production systems.

## 6. Acceptance evidence

- [x] OS, architecture, resources, time sync and network preflight recorded.
- [x] Host identity verified out-of-band.
- [ ] Disclosed password rotated — operator statement only.
- [ ] Dedicated non-root runner account — **not adopted**; superseded by the accepted deviation in §0.1.
- [x] Runner visible Online with expected labels (`self-hosted,linux,x64`).
- [x] Runner execution/admission self-test succeeded on main push — runs 44049832708 and 44050467500. These runs are not the manual read-only Worker diagnostics workflow.
- [ ] Manual read-only Worker diagnostics workflow (`.github/workflows/ubuntu-worker-diagnostics.yml`) — NOT RUN / NOT EVIDENCED; no matching workflow-dispatch run ID is recorded.
- [ ] Runner service survives reboot and reconnects — `enabled` at boot with the documented start ordering, but **no reboot cycle has been performed**.
- [x] L1 Admission Hook denied the tested feature-branch push before workflow steps (run 44050069421); full untrusted-PR isolation and sudo-capability containment remain pending independent review.
- [x] No secrets in Git, logs, artifacts, Issues or PR comments — reviewed for the files added on 2026-11-17.
- [ ] Emergency stop / runner removal procedure tested — documented only; the guard's `observe.flag` rollback was not exercised in production.

Current security acceptance is **BLOCKED**. Even when every operational box is ticked, the status is only **RUNNER_ONLINE**; it is not proof of security acceptance. It is not proof of 24/7 A–I autonomous operation, durable event processing, independent Owner identity, lease fencing, crash recovery, or end-to-end governance.

## 7. Rollback / emergency stop

1. **Stop execution now:** cancel the run in GitHub, then stop the service: `sudo systemctl stop <RUNNER_SERVICE>.service`.
2. **Suspend the runner:** disable it in repository Settings → Actions → Runners.
3. **Remove the registration:** follow GitHub's documented removal procedure, then delete `<RUNNER_INSTALL_DIR>/.credentials*`.
4. **Loosen the guard (only for diagnosis):** `touch <RUNNER_INSTALL_DIR>/hooks/observe.flag`; remove it as soon as the incident is understood. Leaving it in place silently disables admission control.
5. **Revoke credentials exposed during the incident** (registration token, PAT, SSH password).
6. Preserve sanitized logs (`journalctl -u <unit>`, `<RUNNER_INSTALL_DIR>/_diag/`, `hooks/guard.log`) and record the incident in Issue #26.

## 8. Current status

Deployment is reported active on 2026-11-17, with successful runner execution/admission self-tests and three recorded admission decisions (§4.1). The manual read-only Worker diagnostics workflow has no evidenced run and remains NOT RUN. These are operational observations, not an independent security assessment. Operator-confirmed but not independently re-verified: password rotation. **Not verified:** a reboot cycle, the emergency-stop procedure, and the L3 settings (branch protection, required check, environment approval). The runner's sudo-capable service identity remains a material residual risk. Business pipelines have not run on this runner; the A–I Owner workers remain **NOT DEPLOYED**. **Security acceptance remains BLOCKED pending an explicit infrastructure/security Owner decision and independent evidence.**
