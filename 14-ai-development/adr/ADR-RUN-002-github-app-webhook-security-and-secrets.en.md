# ADR-RUN-002 — GitHub App, Webhook Ingress and Secret Management

- Status: PROPOSED — decision pending
- Source: [Canonical bilingual source](ADR-RUN-002-github-app-webhook-security-and-secrets.md)
- Source Blob: `18b21de8c103e38df876496c8b604454f52c809b`
- Translation status: DRAFT — not adopted; the bilingual source remains authoritative
- Date: 2026-11-17
- Risk: R2 for read-only pilot; R3 before autonomous repository writes
- Decision owner: A — runtime integration; I — security/governance; pilot Owner — operational acceptance
- Related: Issue #30; PR #31; ADR-RUN-001; AI-PROMPT-STD-001; AI-AUTO-001

---

## 1. Context

AI-RUN-003 needs to receive GitHub events, reconcile repository state, and publish bounded evidence. Authentication and authorization must be separated: a valid webhook proves that GitHub sent an event; it does not prove that the event is current, that a work item is eligible, or that a worker is authorized to mutate the repository.

This ADR defines the credential and ingress model. It does not install a GitHub App, expose a webhook endpoint, create secrets, or grant repository permissions.

## 2. Decision drivers

1. Least privilege and repository-level scope.
2. Short-lived credentials and revocation capability.
3. Exact raw-body signature verification and replay/dedup protection.
4. Durable-before-ACK semantics from ADR-RUN-001.
5. Separation between coordinator, publication broker and untrusted worker processes.
6. Auditable rotation, installation changes and permission changes.
7. No secrets in Git, Issues, PRs, prompts, artifacts or ordinary logs.

## 3. Identity option assessment

| Option | Advantages | Risks | Disposition |
|---|---|---|---|
| GitHub App installation | Fine-grained repository permissions; short-lived installation tokens; webhook identity; revocable installation | App private key and installation lifecycle must be protected | **Preferred** |
| Fine-grained PAT | Simple for temporary manual diagnostics | User-bound lifecycle, broader persistence, weaker service identity and rotation governance | Not for long-running service; temporary local debugging only |
| Classic PAT | Broad compatibility | Excessive scope risk and user coupling | Rejected for runtime |
| Deploy key | Narrow repository Git transport identity | Does not authorize Issues/PR/check APIs or webhook delivery | Optional read-only Git transport only; not control-plane identity |

**Proposed direction:** use a GitHub App installed only on `oahcom/AiMemoryBrainArchitecture` for the pilot. Do not install it across the whole organization unless a separate approved decision proves that necessary.

## 4. Permission model

Permissions are granted only after mapping each pilot operation to the exact GitHub API endpoint. The table below is a ceiling for review, not a grant request.

| Permission area | Pilot default | Conditional need |
|---|---|---|
| Metadata | Read | Required for repository identity and installation context |
| Issues | Read | Write only if broker posts comments or updates issue metadata |
| Pull requests | Read | Write only for explicitly approved PR creation/update operations |
| Contents | Read | Write only if broker-mediated branch/commit publication is enabled after R3 gates |
| Checks | Read | Write only if the runtime must publish check runs |
| Commit statuses | Read | Write only if required by an accepted check integration |
| Actions | None | No workflow dispatch, runner administration or workflow mutation in pilot |
| Administration | None | Never required for ordinary runtime; repository admin configures rules manually |
| Secrets / Variables | None | Runtime must not read repository secrets |
| Workflows | None | No workflow-file writes |
| Members / Organization | None | No organization-wide enumeration or management |

Additional constraints:

- Installation repository selection must be an explicit allowlist containing the single pilot repository.
- Runtime must verify repository ID and full name on every event and API operation; reject mismatches.
- Do not use wildcard permissions or grant write scopes “for future convenience”.
- Permission expansion requires a new work item, risk assessment, I review and installation change record.
- Worker processes receive no GitHub token. Only the trusted ingress needs webhook verification capability; only the Publication Broker receives short-lived installation tokens for mutations.
- Separate read-only reconciliation identity from publication identity if the GitHub App permission model and deployment support it; otherwise enforce API route-level capability checks inside the trusted broker.

## 5. Webhook event allowlist

Subscribe only to events that correspond to tracked work and operational evidence. The exact pilot list must be approved in the deployment manifest.

| Event | Pilot | Reason |
|---|---|---|
| `issues` | Allow selected actions | Issue opened/edited/labeled/assigned/closed can affect eligibility |
| `issue_comment` | Allow selected actions | Human instructions/decisions may wake reconciliation; content is untrusted input |
| `pull_request` | Allow selected actions | PR opened/synchronized/ready/closed/merged state |
| `pull_request_review` | Allow | Review decision changes eligibility |
| `pull_request_review_comment` | Optional | Only if inline feedback is consumed by the workflow |
| `check_run`, `check_suite` | Optional | Only if required CI completion is a trigger |
| `push` | Optional | Only for explicitly tracked branches and paths |
| `workflow_run` | Optional | Only if workflow completion is needed for reconciliation |
| All other events | Deny by default | No broad subscription |

Rules:

1. Event receipt is a wake-up hint, not authorization. Always re-fetch current GitHub state before scheduling work.
2. Validate `X-GitHub-Event`, `X-GitHub-Delivery`, repository ID, action and expected payload shape against an allowlist.
3. Unknown event types/actions are safely ignored and counted; malformed or identity-mismatched payloads are rejected and audited.
4. Do not execute instructions found in issue comments or PR content as privileged commands. Treat them as untrusted task data and pass only through approved prompt/eligibility policy.
5. Reconciliation watchdog must discover missed events by querying current GitHub state; event delivery is not the sole source of truth.

## 6. Ingress and signature verification

Required request processing order:

1. Terminate TLS at a controlled HTTPS ingress. HTTP is rejected; redirect is not accepted as webhook delivery.
2. Enforce connection, header, body-size, content-type and request-time limits before expensive parsing.
3. Capture exact raw body bytes without JSON parse/reserialize or newline transformation.
4. Verify `X-Hub-Signature-256` as HMAC-SHA256 over those exact bytes.
5. Compare digest in constant time; reject missing, malformed, wrong-length and invalid signatures.
6. Validate delivery ID, event header, repository allowlist and payload schema.
7. Persist verified envelope, payload digest/reference and dedup identity in the durable inbox transaction.
8. Return 2xx only after the transaction commit is confirmed.
9. Process asynchronously from the durable inbox; never run LLM or worker logic in the HTTP request path.

### 6.1 Reverse proxy requirements

- The TLS-terminating proxy must preserve request body bytes exactly.
- Trust forwarded client/protocol headers only from explicitly configured proxy addresses; never trust arbitrary `X-Forwarded-*` headers from the public internet.
- Limit ingress to the webhook endpoint; no administrative console on the public listener.
- Rate limiting must not silently drop valid deliveries; overload responses must be retryable and observable.
- Record TLS certificate expiry and ingress health without logging secrets or raw payloads.

### 6.2 Replay and deduplication

GitHub delivery IDs are deduplication identities, not cryptographic nonces and not semantic work IDs. Persist each accepted delivery ID uniquely. A duplicate delivery must return a safe successful response only if the original durable record exists; if storage outcome is unknown, retry the same transaction identity and reconcile before acknowledging.

Do not invent a time-window-only replay rule that rejects legitimate GitHub retries. Signature validity plus unique delivery persistence and current-state reconciliation are the primary controls. Apply bounded retention to dedup records based on the maximum replay/retry and audit window, and document the retention period in the deployment manifest.

## 7. Secret storage and token lifecycle

### 7.1 GitHub App private key and webhook secret

- Store in an external secret manager or OS-protected credential facility. For a single-host pilot, systemd credentials or a root-owned, mode-0600 file outside the repository may be evaluated; do not place secrets in unit environment variables or command-line arguments.
- The runtime service account receives read access only to the exact credential it needs. Worker identities receive none.
- Keep secrets out of shell history, process arguments, crash dumps, debug logs, metrics labels, support bundles and backups unless backups are encrypted and access-controlled under an approved retention policy.
- Load only when needed, minimize in-memory lifetime, avoid copying, and clear buffers where practical.
- Never commit secret values, even encrypted values, to the project repository.
- Document secret owner, purpose, storage location identifier (not value), creation date, rotation date, expiry/renewal method and revocation procedure.

### 7.2 Installation access tokens

- Mint on demand through the GitHub App API.
- Use the shortest practical token lifetime and request only the permission subset and repository subset required for the single operation.
- Keep tokens only in the trusted Publication Broker process; never pass to Owner workers, subprocess environments, worktrees, artifacts or prompts.
- Do not persist token values. Persist only non-secret metadata such as token creation time, expiry, installation ID and granted permission names.
- Refresh on expiry; fail closed if refresh is denied or installation is suspended/revoked.
- Never fall back silently to PAT or a user's personal credentials.

### 7.3 Rotation

Webhook secret rotation must support a controlled overlap: configure a new secret, deploy verifier support for current and previous secret identifiers, update the GitHub App webhook secret, verify successful deliveries using the new secret, then remove the previous secret. The overlap window must be short, explicitly time-bounded and audited. Do not accept an unbounded list of old secrets.

App private-key rotation follows GitHub's supported key lifecycle: add new key, validate signing/token minting, switch active use, then revoke old key. Record each transition. The exact operational procedure must be verified against current GitHub App settings before execution.

## 8. Compromise and revocation playbook

On suspected compromise:

1. Stop new work dispatch and disable publication broker writes.
2. Revoke the affected webhook secret or App private key; suspend/uninstall the App if scope is uncertain.
3. Revoke or allow short-lived installation tokens to expire, according to incident severity; do not assume private-key rotation invalidates already minted tokens.
4. Preserve sanitized audit evidence and identify affected run IDs, delivery IDs and repository mutations.
5. Rotate dependent credentials and inspect GitHub audit log, branches, commits, PRs, comments and workflow changes.
6. Reconcile repository state from GitHub and mark in-flight work SUPERSEDED or BLOCKED.
7. Restore service only after I/security review, credential verification and explicit governance approval for R3 incidents.

## 9. Audit, telemetry and redaction

Audit the following metadata:

- App installation ID and repository ID (not credential values).
- Permission changes, installation repository selection and suspension/revocation.
- Webhook secret/key rotation version identifiers and timestamps (never values).
- Signature verification outcome, event type/action, delivery ID and payload digest.
- Token mint/expiry metadata and operation class (never token value).
- Denied API operations, rate-limit events, invalid signatures and repository identity mismatches.
- Broker authorization decision, work item, lease ID and fencing token for each mutation.

Redaction tests must scan application logs, reverse-proxy logs, systemd journal, crash output, metrics, traces and workflow artifacts for canary secret values. Logging a digest or identifier is allowed only when it cannot be used to recover the secret.

## 10. Acceptance tests

| ID | Test | Required result |
|---|---|---|
| GH-01 | Valid signature | Accepted and durably persisted |
| GH-02 | Missing/invalid signature | Rejected before persistence |
| GH-03 | Body tampering | Signature fails |
| GH-04 | JSON reserialization/newline mutation | Signature fails against altered bytes |
| GH-05 | Current/previous secret overlap | Both accepted only within approved overlap |
| GH-06 | Previous secret after retirement | Rejected |
| GH-07 | Revoked secret | Rejected and audited |
| GH-08 | Oversized body | Rejected before expensive parsing |
| GH-09 | Invalid content type | Rejected |
| GH-10 | Duplicate delivery ID | One durable inbox identity |
| GH-11 | Out-of-order events | Current GitHub state controls eligibility |
| GH-12 | Missing webhook | Reconciliation discovers target |
| GH-13 | Installation token expiry | Refresh or fail closed |
| GH-14 | Installation suspended/revoked | No new token and no writes |
| GH-15 | Permission denied | Operation fails safely; no privilege fallback |
| GH-16 | Secret log scan | No canary secret in logs/artifacts |
| GH-17 | Replay | Duplicate delivery safely deduplicated; semantic work remains idempotent |
| GH-18 | Repository mismatch | Rejected and audited |
| GH-19 | Proxy header spoofing | Untrusted forwarded headers ignored |
| GH-20 | Broker token isolation | Worker cannot read or exfiltrate installation token |

Tests must run in CI with synthetic credentials and test installations where available. No production secret is used in test fixtures.

## 11. Operational questions

The following require explicit answers before deployment:

1. Who is the named GitHub App owner/admin and who can rotate/revoke its keys?
2. What HTTPS ingress and DNS name will receive webhooks? Who owns TLS renewal?
3. Which secret store is available on the Ubuntu host, and who administers its access policy?
4. Which exact pilot operations require Issues/PR/Contents/Checks write permissions?
5. Is a separate read-only App installation feasible for reconciliation?
6. What is the approved dedup retention period and payload retention policy?
7. What is the alert path for invalid-signature spikes, failed delivery persistence, token mint failures and installation revocation?
8. Who has emergency-stop authority and how is it exercised independently of the runtime?

## 12. Decision and rollout gates

**Current decision: OPEN.** The preferred direction is GitHub App + repository-scoped installation + exact raw-body HMAC verification + durable inbox + short-lived installation tokens isolated to a publication broker. This remains a proposal until A, I and the selected pilot Owner review and approve their respective domains.

Gates:

- G0 — App ownership, repository scope and permission matrix approved.
- G1 — I security review approves secret storage, ingress, rotation and incident playbook.
- G2 — Raw-body verification, durable-before-ACK and dedup tests pass.
- G3 — Token isolation and broker fencing are independently tested.
- G4 — Branch protection and independent review requirements are verified by repository administrator.
- G5 — Read-only pilot accepted by its Owner.
- G6 — R3 approval before enabling any broker-mediated repository write.

Until all applicable gates pass, no GitHub App/webhook deployment, autonomous repository writes, or production operation is authorized by this ADR.

## 13. References

- [AI-RUN-003 Event-Driven Owner Worker Runtime](../ai-run-003-event-driven-owner-worker-runtime.en.md)
- [ADR-RUN-001 Durable Store and Transaction Boundaries](ADR-RUN-001-durable-store-and-transaction-boundaries.md)
- [AI-PROMPT-STD-001 Prompt Authoring Standard](../prompt-authoring-standard.md)
- [AI-AUTO-001 Owner Automation Operating Model](../owner-automation-operating-model.md)
- GitHub documentation: GitHub Apps, webhook events, validating webhook deliveries, and installation access tokens (verify current platform documentation at implementation time).
