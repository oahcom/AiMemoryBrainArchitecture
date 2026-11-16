# Context Reconciliation

**Status:** DECIDED safety ordering; CANDIDATE workflow implementation  
**Owner:** Session G  
**Related:** INT-P0-02, INT-P0-03, INT-P1-06

## 1. Purpose and sources

Reconciliation compares desired Context with current canonical, permission, temporal, retrieval-freshness and Adapter-delivery reality. It detects drift and creates a new valid Context version or blocks use. It does not change Canonical Memory or decide claim truth.

| Signal | Authority | G behavior |
|---|---|---|
| Memory identity/version/lifecycle | D canonical authority | Re-resolve exact ref and eligible successor |
| Revision/retract/Forget | E event stream plus D/I status | Tombstone immediately; do not wait for index |
| Entity/Relation changes | D | Revalidate affected references/paths |
| Permission/policy revocation | I | Reauthorize each entry and delivery |
| Retrieval completeness/index watermark | F | Mark incomplete/stale; omission is not proof of absence |
| Applied/delivery evidence | H Adapter attestation recorded by G | Compare per-delivery target to per-session applied state |

A stale index is a projection problem, not canonical authority. If F's watermark trails relevant canonical events, mark Stale/ReconcileRequired; validate directly with D or conservatively block affected entries.

## 2. Trigger classes

Canonical revision/supersession; retraction/Forget; Entity merge/split; Relation revision/retraction; evidence/provenance revision or source unavailability; Scope/policy change; permission revocation; entry expiry; Context TTL or environment/session closure; index lag or retrieval truncation; delivery gap/rejection; Adapter restart/capability change; timeout/late Applied ack; periodic audit.

## 3. State distinctions

- **Stale:** known source, index, policy or delivery watermark differs from last reconciled baseline.
- **ReconcileRequired:** a concrete event/ref/permission/delivery gap requires a run; unsafe affected entries are blocked pending outcome.
- **Reconciled:** a run completed for a declared watermark/scope, with affected refs valid, replaced, removed or explicitly unresolved/blocked. This is a run result, not a permanent Context Lifecycle state.
- **Blocked:** authorization, Forget, Scope, integrity or canonical eligibility cannot be established.
- **Closed:** Context lifecycle terminal; reconcile may only perform governed cleanup/audit, not reactivate.

Context Lifecycle may be Active after a successful run. Preserve the Reconciled run record separately; do not add Reconciled to Delivery or Entry lifecycle.

## 4. Reconciliation algorithm

1. Persist trigger ID, source watermark, affected refs, Scope hint, timestamps and correlation.
2. Resolve exact Contexts by canonical IDs and environment/task/Agent Scope; never broad-match names.
3. Install immediate deny/tombstone for Forget, retraction, revocation or invalid environment identity before expensive work.
4. Load Context head, immutable snapshot, pending Change Sets/deliveries and Adapter/session attestations.
5. Reauthorize principal, Context, every Memory/evidence/rendering ref and target Adapter under current policy epoch.
6. Resolve canonical Memory ID/version, lifecycle, successor/superseded/retracted status, Claim/Entity/Relation and provenance through D.
7. Compare E event and F index watermarks; detect delay/truncation. Missing index result is not deletion.
8. Classify each entry: Valid, StaleRevision, Retracted, Forgotten, PermissionRevoked, Expired, ScopeMismatch, SourceUnavailable, Superseded, ConflictChanged or Unknown.
9. Plan compensation: Update to validated successor, Replace, Remove/Expire, compact, defer or Block. Never silently replace a disputed claim with a preferred one.
10. Commit atomic Change Set against current Base Version; on CAS failure reload and recompute.
11. Cancel/supersede pending deliveries, send latest Snapshot/Delta, request adapter clear where required, collect per-target outcomes.
12. Record watermarks, auth epoch, refs examined, operations, unresolved gaps and delivery evidence. Mark run Reconciled only for declared scope/watermark.

## 5. Forget and revocation protocol

### Immediate logical invalidation

On Forget, G:
- persists deny tombstone keyed by canonical memory identity/version family and affected Scope;
- makes matching entries ineligible immediately in reads/planning/delivery, even if historical immutable snapshots still contain refs;
- cancels/supersedes pending Change Sets and deliveries containing target;
- invalidates Snapshot/Delta materializations and caches by Scope + memory ref + policy/Forget epoch;
- blocks new Applied confirmation for deliveries containing target;
- creates clear/quarantine requests for every Adapter/session that may have received target.

Tombstone check is mandatory immediately before delivery and at Adapter application boundary. Historical snapshots are audit-only and never served as current state.

### Adapter states and offline behavior

Track per target Adapter/session: **pending**, **confirmed**, **failed**, **unknown**.
- pending: clear requested/required but not attested.
- confirmed: Adapter attests target removed/quarantined from managed region and local managed cache under declared capability.
- failed: Adapter cannot clear or validation fails; remain blocked and retry/escalate.
- unknown: offline, timeout, lost ack or insufficient visibility.

Offline Adapter remains unknown/pending. On reconnect it authenticates, re-resolves Scope, fetches current Forget/revocation epochs, discards stale cached Snapshot/Delta, applies safe replacement Snapshot/clear set, then attests. It cannot reuse cached Context before reconciliation.

### Completion boundary

G reports Context-side propagation complete only if no active/pending Brain Context/Delivery can expose the target and every known Adapter/session is confirmed cleared/inaccessible. Unknown or failed targets remain explicit exceptions; global result is not confirmed complete. Historical retention is I-governed. G cannot claim external model/provider physical erasure or erase tokens already processed by prior inference. I owns canonical Forget completion and external boundary claims.

## 6. Partial failure and index incompleteness

Reconciliation is a resumable saga; results are per Context and Adapter session. Retries use trigger ID + Scope + target watermark + payload hash. Failed stages retain tombstones; no retry resurrects a blocked entry.

F supplies watermark, completeness, truncation and uncertainty. If incomplete/unknown, preserve coverage gap, do not infer absence, validate existing entries directly with D, schedule re-retrieval after watermark catch-up and mark sufficiency incomplete where required coverage may be missing.

## 7. Audit and decisions

Audit trigger/source/watermark, Context IDs, canonical refs as permitted, policy epoch, affected Adapter sessions, tombstone epoch, classifications, operations, Change Set/version IDs, Delivery IDs, acknowledgements and unresolved failures. Do not log memory plaintext merely to prove cleanup.

- **DECIDED:** D remains canonical authority; indexes are projections; Forget/revocation tombstone wins immediately; reauthorize during reconcile and before delivery/application.
- **CANDIDATE:** event-driven invalidation plus periodic watermark sweep.
- **TO_VALIDATE:** fan-out, propagation lag and reconnect convergence.
- **OPEN:** canonical Forget proof (I); event/watermark schema (E); completeness (F); Adapter clear attestation (H).
