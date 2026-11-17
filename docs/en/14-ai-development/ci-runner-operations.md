# AI Memory Brain — CI Self-Hosted Runner Operations

- Document ID: DOC-OPS-001
- Version: 1.1 (revised 2026-11-17: run-identity deviation accepted, service-layer admission added)
- Chinese counterpart: [CI 自托管 Runner 运维设计](../../zh-CN/14-ai-development/ci-runner-operations.md)
- Basis: Actual deployment and measurements on cloud host zesu on 2026-11-17 (the host address is not recorded in this repository); source revision recorded at the end of this document
- Status: **Operations design note** describing one **deployed and running** instance. Measured numbers are single measurements from that day and are not performance commitments. Admission control is enforced at the service layer by the L1 hook (section 4); first-execution evidence is in section 14

## 1. Purpose

Explain **which machine runs this repository's continuous integration, how its traffic leaves that machine, and how to recover it**. This is not an architecture specification and changes no Owner contract; it explains the infrastructure layer that produces verification evidence.

Audience: engineers who need to decide whether a CI failure is a code problem or an environment problem, and anyone taking over this machine.

## 2. One-sentence summary

Because this repository's CI cannot rely on GitHub-hosted runners for network reachability, it uses **one self-hosted runner plus a local routing proxy**: the runner only executes jobs, all egress is decided by a local sing-box instance, and the proxy's default outbound is a Cloudflare WARP tunnel.

## 3. Scope and non-goals

**In scope**

- Deployment shape, labels, and service packaging of the self-hosted runner.
- Egress topology, routing rules, and the measured evidence for "why direct access does not work".
- Failure criteria, recovery actions, and rollback paths.
- Security boundaries: run identity, credential locations, listen addresses, privileges.

**Non-goals**

- Does not define pipeline stages, caching strategy, or build matrices.
- Does not guarantee throughput. Free WARP bandwidth fluctuates noticeably by time of day (measured range in section 12).
- Does not cover the source build environment (toolchain versions, cross-compilation targets); workflows own those.
- Does not replace GitHub's permission model. The runner is registered at repository scope, and that registration determines its visibility.

## 4. Relationship to the existing bootstrap runbook

The repository already contains a runner bootstrap runbook, `AI-RUN-002-RUNBOOK` (`14-ai-development/ubuntu-self-hosted-runner-bootstrap.md`, on branch `infra/remote-worker-bootstrap-2026-11-17`, tracked by Issue #26), with status **ACTIVE / operator-executed (v1.1, revised 2026-11-17)**.

This document records the **actual result of executing that runbook**. The two **diverge** on deployment shape, and the divergence must be recorded explicitly rather than glossed over with "deployed as specified":

| Dimension | AI-RUN-002-RUNBOOK planned | Actual deployment |
|---|---|---|
| Run identity | Dedicated account `actions-runner` | `ubuntu` (the same account used for login) |
| Install path | `/opt/actions-runner` (`0750`, owner `actions-runner`) | `~/actions-runner` |
| Labels | `ai-worker` | `self-hosted,linux,x64` |
| Privilege boundary | Explicitly prohibited from the `sudo` / `docker` groups | `ubuntu` has **passwordless sudo** |
| Target host | `ubuntu-primary-01` | The same host (`vm-0-9-ubuntu`) |
| Status | PROPOSED | Deployed and online |

**Practical consequence of the divergence**: workflows execute as `ubuntu`, and that account can escalate to root without a password, so **any workflow that executes on this host is equivalent to root on it**.

**Decision (DECIDED, 2026-11-17, Owner)**: do **not** roll back the account shape. Revise `AI-RUN-002-RUNBOOK` to v1.1 accepting the deployed shape, and move admission control from human discipline to **service-layer enforcement**. Rationale: rolling back would only turn "root-equivalent" into "an unprivileged account on the same host", while whether that account can escalate is not the main risk surface — **the main risk surface is whether a workflow starts executing on this host at all**. The effective control point is the admission verdict, not the account name.

**Three admission layers**:

| Layer | Mechanism | Location | Enforceability |
|---|---|---|---|
| L1 service | An `ACTIONS_RUNNER_HOOK_JOB_STARTED` hook reads `GITHUB_REF` and `GITHUB_EVENT_NAME` and admits only `push`, `workflow_dispatch`, and `schedule` on `refs/heads/main`; everything else fails **before any step runs** | Host `~/actions-runner/hooks/job-started-guard.sh`, injected via a systemd drop-in | **Enforced**: decided inside the runner; editing a workflow cannot change the verdict |
| L2 repository | Workflow audit: a `self-hosted` job combined with `pull_request`, `pull_request_target`, `issue_comment`, `workflow_run`, or similar events, an unfiltered `push`, or a statically unevaluable `runs-on` expression fails the check | `.github/workflows/runner-admission-policy.yml` + `scripts/ci/audit_runner_admission.py` | Preventive: binding only once configured as a required status check |
| L3 organization | Branch protection, Environments with required approval, repository-scoped runner groups | GitHub repository settings | Requires the Owner to enable it in the UI; this document does not claim it is enabled |

**L1 evidence** (2026-11-17, same host):

| Scenario | Result |
|---|---|
| `push` to `refs/heads/main` (run 44049832708) | ALLOW, job `Succeeded` |
| `push` to `refs/heads/ci/admission-negative-test` (run 44050069421) | DENY `ref_not_default_branch`, job `Failed`, **zero steps executed** |
| Where the hook gets its context | This runner version invokes `bash -e <hook>` with no argv and no stdin; the verdict uses the `GITHUB_*` environment exported by the worker |

**Residual risk (accepted; no longer an open item)**:

1. The hook governs only whether a job may start, not what it does; steps can still `sudo`. Tightening that requires `NoNewPrivileges=yes` or a separate account, both of which change existing job capabilities and were **not** implemented in this round.
2. `main` currently has **no branch protection** (the hook observed `GITHUB_REF_PROTECTED=false`), so "trusted branch" is a factual convention rather than a platform guarantee. Until branch protection is enabled, anyone who can push to `main` can change the workflow that will run; L1 only checks the ref and will not stop it.
3. The hook is fail-closed: if the hook script or `python3` is unavailable, every job fails. The rollback switch is `hooks/observe.flag` (present = log only, never block).

## 5. Components and responsibilities

| Component | Location / unit name | Responsibility | Not responsible for |
|---|---|---|---|
| Runner listener | `~/actions-runner`, `actions.runner.oahcom-AiMemoryBrainArchitecture.zesu-x64.service` | Claim jobs, execute workflows, report status | Any network policy decision |
| Proxy front end | `sing-box.service`, `127.0.0.1:17891` (mixed inbound) | The single routing and egress-selection point | Job semantics |
| WARP tunnel | `warp-usque.service`, `127.0.0.1:2085` | Provides the default egress (MASQUE over QUIC) | Routing decisions |
| Fallback egress pool | sing-box `auto` group (subscription nodes, `urltest` selection) | Backstop when WARP is unavailable | Not a default |
| Direct egress | sing-box `direct` group | `api.github.com`, domestic mirrors, private ranges | Bulk downloads |

**The boundary in one sentence**: the runner does not know how the network is routed, and the proxy does not know what the job is. They connect only through `HTTP_PROXY` / `HTTPS_PROXY`. The value of this boundary is that a network fault can be diagnosed and switched without touching the runner or the job definitions.

## 6. Context and egress topology

```
GitHub
  │
  ├─ api.github.com ───────────── direct (a shared egress IP triggers 403 rate limiting, see 8.3)
  │
  └─ github.com / codeload.github.com / release-assets / ghcr.io
        │
        ▼
   sing-box  127.0.0.1:17891   ← the runner's HTTP(S)_PROXY points here
        │  route.final = pick
        ├─ warp   default: usque → CF WARP (free, does not consume subscription quota)
        ├─ auto   fallback: subscription node pool, urltest picks the best
        └─ direct domestic mirrors / .cn / private ranges / api.github.com
        │
   Runner.Listener (system user ubuntu, labels self-hosted,linux,x64)
```

Startup order is fixed by systemd dependencies: `warp-usque` → `sing-box` → `actions.runner.*`. This order is **MUST**: if the runner starts before the proxy is listening, every outbound request except the registration channel fails immediately.

## 7. Why direct access does not work (measured evidence)

The host sits in a cloud data center in mainland China. Direct measurements against GitHub endpoints on the deployment day (2026-11-17):

| Endpoint | Direct behavior | Conclusion |
|---|---|---|
| `api.github.com` | HTTP 200 / 0.47 s | Usable; kept as a direct route |
| `codeload.github.com` (action packages) | ~39 KB/s | Not usable |
| `release-assets` (release downloads) | 0 bytes in 3 minutes | Not usable |
| `git clone` (41 MB repository) | Not finished after 60 s | Not usable |

**Key judgment**: API reachability does not mean CI is usable. Testing only `api.github.com` leads to the wrong conclusion that "the network is fine". The decisive evidence comes from `codeload` and `release-assets` — those are what every job actually downloads.

Direct access therefore **does not constitute an option** for this repository's CI unless the machine moves to a data center with direct reachability.

## 8. Five hard constraints on egress selection

All five were established by measurement, after being hit in practice. They are constraints of this design, not suggestions.

### 8.1 This host resets MASQUE over TCP 443; only QUIC works

**Looks like**: WARP's MASQUE is carried over both UDP and TCP, so either works.
**Actually**: MASQUE over TCP 443 on this host is terminated with `connection reset by peer`. Empty SNI, `consumer-masque.cloudflareclient.com`, and `www.cloudflare.com` were all rejected.

**Constraint**: the tunnel **MUST** use the default QUIC transport (UDP 443) and **MUST NOT** enable `--http2`. When deploying to a new machine, send one QUIC probe and one H2 probe first and use whichever works; do not treat this host's recipe as a general conclusion.

### 8.2 In-tunnel IPv6 must be disabled (`-S`)

**Looks like**: IPv6 is optional and irrelevant.
**Actually**: without `-S`, WARP assigns an IPv6 egress address and `github.com` time-to-first-byte is 15–24 s; with `-S` it drops to 4–6 s, and `release-assets` throughput rises from 286 KB/s to 580 KB/s.

**Constraint**: `ExecStart` **MUST** keep `-S`. This is the single highest-value setting in this design.

### 8.3 `api.github.com` must go direct

**Looks like**: routing everything through the proxy is simplest.
**Actually**: the proxy egress is a **shared IP** whose anonymous API quota is already exhausted by other users, returning `403 rate limit exceeded`, while the same request direct returns 200.

**Constraint**: the routing rule `domain_suffix: ["api.github.com"] → direct` **MUST NOT** be removed. Removing it breaks the runner's registration heartbeat and all API calls.

### 8.4 The proxy must be injected by systemd, not by `.env`

**Looks like**: writing `HTTP_PROXY` into `~/actions-runner/.env` is enough.
**Actually**: `runsvc.sh` in this runner version does not load `.env`, and the proxy variables are absent from the process environment. A systemd drop-in (`/etc/systemd/system/actions.runner.*.d/proxy.conf`) **MUST** be used so job child processes inherit them.

### 8.5 Routing rules must live in the config generator

**Looks like**: the generator only handles nodes, and routing rules can be patched in afterwards by hand.
**Actually**: a subscription refresh regenerates the whole config file, discarding hand-patched rules, and `api.github.com` immediately returns 403 again. This happened in practice once.

**Constraint**: routing rules **MUST** be produced by the generator together with the config; runtime hand-editing **MUST NOT** be relied upon.

## 9. Main workflows

### 9.1 First deployment

1. Confirm the host architecture, fetch the matching package, and **verify its SHA256**. A wrong architecture or an incomplete download is the most common bootstrap failure (this instance hit a triple error: the page generated an arm64 command, the machine was x86_64, and the downloaded package was a 450 KB corrupt archive whose symptom was `unexpected EOF` on extract with no `config.sh` present).
2. Register with `config.sh --unattended --labels self-hosted,linux,x64`.
3. Install as a systemd service with `svc.sh install` and `enable` it for boot.
4. Build the egress chain (the three units in section 6) and start them in dependency order.
5. Inject the proxy environment variables via the drop-in.
6. Run acceptance (section 13).

### 9.2 Subscription refresh (fallback pool maintenance)

Node addresses and credentials in the subscription rotate. The refresh flow is: fetch the subscription → rebuild the config with the generator (**preserving** the WARP egress and routing rules) → `sing-box check` syntax validation → replace the config → restart → self-check the `api.github.com` and `github.com` endpoints. If validation fails, the running config **MUST NOT** be replaced.

### 9.3 Switching egress

Egress groups are switched through the Clash API (`warp` / `auto` / a specific node / `direct`) without restarting any unit. This decoupling of "egress choice" from "service lifecycle" is the main benefit of the design.

### 9.4 How the node pool is determined

**Latency is not throughput.** In measurement, top-ranked nodes by latency delivered only 55 KB/s of real download throughput; the seven nodes finally admitted to the pool delivered 1–1.3 MB/s. Pool admission **MUST** therefore be based on measured throughput; latency is only a coarse screen.

## 10. Failure and recovery

| Symptom | Criterion | Action |
|---|---|---|
| Runner cannot reach GitHub | Abnormal `warp-usque` log / tunnel down | Restart `warp-usque`; it reconnects automatically after 5 s |
| WARP fully unavailable | Device token revoked (log shows 403 / invalid token) | Re-run `register`. **This overwrites the device config; back it up first** |
| Abnormally high TTFB (>30 s) | `-S` missing from `ExecStart` | Restore `-S` and restart |
| `api.github.com` returns 403 | Direct routing rule lost | Regenerate the config (see 8.5) instead of editing it by hand |
| Fallback pool dead | All nodes time out | Refresh subscription, re-measure throughput, re-select the pool |
| CI notably slower | No errors, only latency | Switch to `auto` for comparison to separate WARP jitter from heavier jobs |

**General recovery principle**: first identify *which layer* failed (tunnel / proxy / routing / runner), then touch only that layer. Cross-layer restarts hide the root cause.

## 11. Security and trust boundaries

- The proxy inbound **only** listens on `127.0.0.1`; no port is exposed externally.
- The WARP device config (containing the private key and access token), the subscription URL, and the Clash API secret are all `600`. They **MUST NOT** enter the repository, appear in documentation, or appear in logs.
- The runner does not run as root; but as described in section 4, its account **has passwordless sudo**, so "non-root" does not mean "cannot escalate". This is a known and unfixed boundary defect of this instance.
- This machine's egress is a **shared public IP**. Two consequences: requests to target sites consume other users' quota and reputation, and the machine must not be treated as an egress with a stable identity.
- The tunnel is established by a third-party, non-official client. Before upgrading it, registration and connectivity **MUST** be validated on a temporary port, and only then should the production binary be replaced.

## 12. Performance and resource budget

Measured on 2026-11-17 (single measurements, not commitments):

| Item | Data |
|---|---|
| `git clone`, 41 MB | 17 s, about 2.4 MB/s |
| `api.github.com` | 0.27 s (direct) |
| `codeload`, single stream | about 120 KB/s |
| `release-assets`, 5 MB | 300–580 KB/s |

**Non-guarantees that must be stated**:

1. Free WARP bandwidth fluctuates strongly; two runs with identical parameters can differ by 4x. Tuning for jitter (for example changing MTU) yields no stable gain: in measurement the difference between MTU 1280 and 1360 was entirely masked by jitter, and 1420 does not work at all (PMTU black hole), so the default 1280 is kept.
2. The `git` protocol multiplexes streams and is therefore much faster than single-stream `curl`. Judging "CI is unusable" from a low single-stream `curl` number is a misjudgment.
3. Host resources: 4 vCPU / 3.6 GB RAM / 39 GB root filesystem (about 28 GB used, 71–73%). The `_work` directory grows with jobs and **MUST** be cleaned periodically; disk is neither unlimited nor a capacity guarantee of this design.

## 13. Acceptance criteria

A runner is considered usable only when **all** of the following hold:

1. The service is `active` and `enabled` (starts on boot).
2. The log shows `Listening for Jobs`, and the repository's Runner page shows Online.
3. `api.github.com` through the proxy returns 200 (routing rule still effective).
4. `codeload` can download one action package completely (bulk-transfer path).
5. One real `git clone` completes (multiplexed and redirected path).
6. The admission hook is installed and `guard.log` contains an `ALLOW ref=refs/heads/main` decision (proves L1 was not bypassed).

Items 1–4 and 6 are necessary conditions; **item 5 alone is sufficient** — only it covers all three failure points at once: TLS, the redirect to `release-assets` / `objects.githubusercontent.com`, and stream multiplexing.

## 14. Decisions, open items, and references

**Decided (this instance)**

- Egress defaults to WARP; the subscription node pool is demoted to fallback. Rationale: WARP is free and consumes no subscription quota, while the subscription egress is a shared IP that consumes quota.
- Routing: `api.github.com` and domestic mirrors go direct, everything else goes through the proxy. Rationale in 8.3.
- Labels are fixed at `self-hosted,linux,x64`; workflows **MUST NOT** use `arm64` (the host is x86_64).
- The run-identity deviation is **accepted and locked in** (section 4): the account shape is not rolled back, and the L1 hook enforces “only `refs/heads/main` may execute” at the service layer. Decided 2026-11-17; runbook v1.1.
- No tuning for jitter; the default MTU is kept.

**Open**

- **No business pipeline has executed on this runner yet.** The first real execution is `Runner Guard Self-Test` (2026-11-17, run 44049832708, `Succeeded`), which validates the fetch-execute-report chain and is **not** evidence that this repository's CI pipeline passes.
- Disk growth rate is unknown; no cleanup threshold or alerting is configured. Until then, capacity risk is carried by manual inspection.
- The fallback pool's validity depends on subscription availability; there is no automatic switching policy (switching is currently a manual decision). This is deliberate: automatic switching would cause pointless flapping whenever WARP jitters.

**References**

- Bilingual documentation policy: [GOV-DOC-001](../../../00-governance/bilingual-documentation-policy.md)
- Runner bootstrap runbook: `AI-RUN-002-RUNBOOK`, `14-ai-development/ubuntu-self-hosted-runner-bootstrap.md` (branch `infra/remote-worker-bootstrap-2026-11-17`), tracked by [Issue #26](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/26)
- Full operations record of the deployment instance (script inventory, per-node throughput data): archived in another repository, `auto-swicth-ip`, as `docs/gh-runner-zesu-20261117.md`. This document keeps only the conclusions relevant to this repository's CI.
- Source revision: written from the deployment state and measurements of 2026-11-17. That instance's host, network, and version details are recorded in `RUNNER-OPS.md` (deployer working copy, not committed).
