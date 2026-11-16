# I36-GOV-01..10 — Consolidated Conservative Governance Decision Proposal

- Owner: I — Security & Governance
- Branch: `session-i-security-governance-2026-11-16`
- Date: 2026-11-17
- Status: **PROPOSAL ONLY / NOT APPROVED / NOT EFFECTIVE**
- Governing source: `09-security-governance/governance-decision-register.md`
- Companion: `09-security-governance/phase-3.5-global-identity-forget-governance.md`

## 1. Purpose and non-approval

This proposal consolidates the ten outstanding I36 governance decisions into a conservative initial policy profile so the authorized governance body can review one coherent package. It does not approve or activate any policy. The I governance register remains authoritative; all I36-GOV-01..10 remain GOVERNANCE-BLOCKED until the required authorized approval record is created.

## 2. Recommended initial policy profile

| Decision | Recommended default | Explicitly prohibited / fallback | Required approvers |
|---|---|---|---|
| I36-GOV-01 Trusted Issuer Registry | Local explicit allowlist; issuer-scoped identity; onboarding requires owner, purpose, trust basis, key lifecycle, rotation and compromise procedure. | No implicit federation or trust-on-first-use. Unknown/untrusted issuer is denied. | Identity Governance + Security Governance; issuer owner; Privacy/Legal where jurisdictional. |
| I36-GOV-02 Delegation | Delegation disabled by default. If enabled, require signed exact-scope/action/audience/purpose/expiry grant; maximum depth 1; no sub-delegation; parent revocation invalidates child grants. | No wildcard audience, indefinite grant, implicit inheritance or unbounded delegation chain. | Security Governance + Identity Governance; Legal where agency/consent applies. |
| I36-GOV-03 Cross-Scope grants | Deny cross-Scope by default. Allow only explicit exact source/target ScopeRef, action, resource, purpose and expiry grants. | No inferred parent/child scope inheritance or implicit sharing algebra. | Security/Architecture Governance + B + data/tenant owner. |
| I36-GOV-04 Cross-Environment grants | Deny cross-Environment by default. Require registry-backed EnvironmentRef and explicit bridge grant with exact endpoints, action and expiry. | No implicit environment federation or name-based environment equivalence. | Security/Architecture Governance + environment owner + data/tenant owner. |
| I36-GOV-05 Revocation semantics | Revocation takes effect at the next protected commit/visibility/delivery/Applied boundary after I's durable terminal decision. Revalidate current authorization at every protected boundary. In-flight ambiguous side effects remain IN_DOUBT. | No stale cached ALLOW, no implicit offline lease, no rollback of PermissionEpoch. Already-disclosed information is not claimed retractable; record residual handling. | Security Governance + D/E/F/G/H/C owners + service owner; Privacy/Legal for disclosure/retention. |
| I36-GOV-06 PermissionEpoch | I is the logical authority; monotonic per PolicyDomainRef; current sequencer/ledger is authoritative. Initial profile requires online freshness at protected boundary and fail-closed on I outage. | No cross-domain numeric comparison, no consumer-minted epoch, no bounded stale authorization until separately approved. | Security Governance + identity/policy platform owner + all consumers. |
| I36-GOV-07 Unsupported Adapter/Producer | Unsupported, offline, stale or unverifiable capability maps to Unknown and blocks protected use/Forget completion. Require explicit alternative control and scoped exception if operation must proceed. | No inferred ACK, no automatic downgrade to optional, no bypass by another unregistered Adapter. | Security Governance + H + service/product owner; Privacy/Legal where data leaves control. |
| I36-GOV-08 Global Forget exceptions | Default no exception. Any exception must be target/scope/action-specific, reasoned, signed, independently approved, hard-expiring and disclosed as residual risk. Backup retention is BackupPending until expiry/erasure; external provider non-response remains Unknown. | No operator self-approval, no timeout-as-success, no blanket exception, no physical-erasure claim without media/key/copy evidence. | Privacy/Legal + Security Governance + data owner + Storage/recipient owner. |
| I36-GOV-09 Principal resolution | Stable PrincipalRef is issuer-scoped. Alias/collision migration requires verified issuer assertion and explicit reviewed mapping; ambiguous identities are denied. No automatic merge. | No name/email-only identity merge, no silent alias reuse, no collision overwrite. | Identity Governance + Security Governance; issuer owner for migration evidence. |
| I36-GOV-10 ActorRef / Principal binding | ActorRef is verifier-produced per operation and cryptographically bound to authenticated PrincipalRef/IssuerRef, producer/Adapter instance, ScopeRef, EnvironmentRef, session, audience and current PermissionEpoch. | No caller-minted ActorRef, no payload ID as authentication, no reuse across operation/session/authority. | Identity/Security Governance + H/I verifier control owners; B validates type semantics. |

## 3. Shared approval and enforcement requirements

Every approved row must record:

1. Exact decision ID and exact policy text/hash being approved.
2. Approver PrincipalRef and IssuerRef, role/authority basis and authentication evidence.
3. Independent reviewer where required; conflict-of-interest check.
4. Scope, environment, jurisdiction, affected data classes, services and user population.
5. Effective policy version/time, expiry/review date, revocation/supersession conditions.
6. Evidence references: tests, issuer/registry manifests, threat analysis, owner conformance and operational runbook.
7. Exact consumer obligations and enforcement point for D/E/F/G/H/C/Storage.

Technical owner acceptance, a Git commit, an architecture recommendation or a user instruction to continue engineering work is not a governance approval.

## 4. Required negative conformance before activation

- Unknown issuer, revoked issuer key, stale key version and issuer collision.
- Delegation depth overflow, audience/purpose mismatch, expired grant and parent revocation.
- Cross-Scope and cross-Environment access without exact grant.
- Revocation racing canonical commit, compiler publication, index/cache retrieval, context delivery and provider submit.
- PermissionEpoch rollback, stale cache, offline I authority and sequencer failover.
- Forged ActorRef/ProducerRef/AdapterRef and payload/transport identity mismatch.
- Unsupported/offline Adapter, missing ACK, request receipt mistaken for delete ACK and late reconnect.
- Inventory epoch change, newly discovered producer/recipient/backup, incomplete seal and omitted target.
- External recipient no response, backup retention, restore resurrection and expired PolicyException.

All tests must run against identified builds and real enforcement boundaries. Reference-model tests are supporting evidence only.

## 5. Explicit current disposition

- I36-GOV-01..10: **GOVERNANCE-BLOCKED / NOT APPROVED**.
- This proposal: **RECOMMENDED DEFAULTS / NOT EFFECTIVE**.
- No trusted issuer/federation, cross-scope/environment grant, offline lease, exception class or Global Forget completion threshold is activated by this document.
- Global Forget Completion remains OPEN / NOT COMPLETED.
- No physical erasure or legal/privacy risk acceptance is claimed.

## 6. Required governance action

The authorized governance body must approve, reject or amend each exact row and create the required approval record in the Governance Decision Register. Until that occurs, the safe defaults in this proposal are design recommendations only; runtime must continue to fail closed on unresolved authority.