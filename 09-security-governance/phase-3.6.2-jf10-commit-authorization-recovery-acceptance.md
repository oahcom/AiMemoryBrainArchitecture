# Phase 3.6.2 — I Acceptance of JF-10 Commit Authorization Recovery Interface

- Owner: Session I — Security, Identity & Governance
- Branch: `session-i-security-governance-2026-11-16`
- Status: **I-OWNED TECHNICAL INTERFACE ACCEPTED WITH BINDING CLARIFICATIONS**
- Scope: I policy-domain sequencer, PermissionEpoch, revocation ordering, and CommitAuthorizationReceipt only.
- Source proposal: D/E/Storage `phase-3.6.2-jf10-cross-authority-recovery-protocol.md`, Blob `0f016e4220b4b4b37a99c12c1a6a94ed480040a7`.
- This is a technical interface decision under the delegated BIH/Phase 3.6 engineering authority. It is **not** external Security/Identity Governance approval, production policy activation, implementation evidence, or D/Storage acceptance.

## 1. Decision

I **ACCEPTS the I-owned portion** of the JF-10 candidate subject to the normative clarifications in this record.

I accepts these requirements:
1. A durable, terminal I sequencer outcome is keyed by a stable operation identity and the exact immutable request digest.
2. I exposes authenticated authoritative lookup/replay for that exact key.
3. Same key + same digest returns the identical durable outcome; same key + different digest is a hard conflict.
4. The terminal authorization-order outcome is durably retained and recoverable across response loss, process restart, replica lag, failover and restore.
5. `COMMIT_WON`, `REVOCATION_WON`, and `INDETERMINATE_ABORTED` are distinct terminal outcomes. Unknown/unavailable state is not converted to a terminal success or to `NOT_COMMITTED`.
6. `COMMIT_WON` is an I authorization-order result only. It is not a Storage publication receipt, owner commit, VisibilityPointer update, or reader-visible success.

This acceptance is limited to I's authority. D must still define and accept ForgetFence ordering at the owner visibility boundary; Storage must accept and implement its local atomic visibility/recovery transaction; E must consume only the durable Storage PublicationReceipt. JF-10 remains OPEN overall until those owner decisions, implementation and conformance evidence are complete.

## 2. Canonical I credential and terminology

The canonical I-issued artifact name is **CommitAuthorizationReceipt**.

If the DE-S documents use `AuthorizationCommitPermit`, that term MUST be treated as a legacy label for this exact same I artifact only after the field mapping below is adopted. It MUST NOT denote a second credential, a transferable capability, or an independent authorization decision.

The receipt is single-use for the first sequencer decision transition. It is bound to the exact:
`(policy_domain_id, PermissionEpoch, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef, DelegationChainRef, operation_id, operation_payload_digest, owner_boundary, decision_id)`.

For JF-10:
- `operation_id` MUST equal the stable `PublicationOperationId`.
- `operation_payload_digest` MUST equal the canonical `RequestDigest` over the complete immutable publication request, including the owner boundary and all security-relevant D/E/Storage bindings.
- `owner_boundary` MUST identify the exact Storage visibility-commit boundary, not a generic "publish" label.
- The same operation ID MUST never be reused with a different digest or changed security-relevant binding.

A receipt reference is not proof that the sequencer decision was durably recorded. Consumers must retrieve/verify the terminal I outcome.

## 3. Retry, replay and receipt consumption

The first valid request atomically consumes the receipt and creates the durable terminal sequencer decision. Thereafter:
- same `PublicationOperationId` + same `RequestDigest`: return the already-recorded terminal outcome and its original sequencer position; do not consume the receipt again and do not create a second decision;
- same operation ID + different digest or changed bound tuple: reject as a hard conflict, audit, and never overwrite the original decision;
- unknown operation or unresolved I persistence state: return `UNKNOWN/PENDING`; do not mint a replacement operation ID or claim non-commit;
- a new receipt cannot be used to escape an unresolved prior operation with the same logical publication intent.

The I lookup MUST be authenticated, authoritative and linearizable with respect to the policy-domain sequencer. A stale replica/cache is not an acceptable decision source.

## 4. Exact meaning of the terminal outcomes

The I sequencer totally orders the authorization decision against revocation within the applicable policy domain:
- `COMMIT_WON`: the exact bound operation's authorization decision was durably ordered before any conflicting revocation event. This ordering fact is irrevocable and remains queryable for recovery.
- `REVOCATION_WON`: revocation was ordered first; the operation is denied and MUST NOT become visible.
- `INDETERMINATE_ABORTED`: I cannot safely establish a winning authorization order and has durably terminated the operation as non-success. It MUST NOT be reinterpreted as `COMMIT_WON`.

A later PermissionEpoch advance does not rewrite an already durable `COMMIT_WON` ordering fact or make its sequencer position disappear. The owner may finish forward recovery only for that exact operation/digest and only if every non-I owner predicate remains valid. This is not a general stale-epoch grace period, reusable lease, or permission for a new operation. A new operation must obtain fresh current authorization.

This distinction is mandatory: I orders authorization against revocation; Storage separately orders physical visibility; D separately orders ForgetFence. These are three different authorities and linearization records.

## 5. Failure and recovery guarantees required from I

The I implementation must provide:
1. atomic persistence of receipt consumption and terminal sequencer outcome;
2. a unique constraint over the operation identity within its policy domain;
3. durable retention of terminal outcome, immutable request digest, receipt ID, decision ID, PermissionEpoch and sequencer position for at least the full owner recovery/audit horizon;
4. authenticated lookup by operation ID + digest, returning the exact original outcome and position;
5. deterministic conflict on changed digest/binding;
6. failover/restore that cannot lose, reorder, duplicate or silently reverse a terminal decision;
7. explicit behavior for crash before persistence, crash after persistence but before response, replica lag and sequencer failover.

If I cannot provide these properties, the JF-10 protocol is not accepted as implementable on the proposed interface; a formally specified durable distributed transaction/2PC protocol with participant recovery is required. No cache, local ALLOW, stale epoch or wall-clock inference may substitute.

## 6. Boundary conditions not accepted on I's behalf

The following remain explicit owner actions and are not resolved by this I decision:
- **D:** define how a ForgetFence installed after I `COMMIT_WON` but before Storage visibility commit is serialized against the visibility pointer transaction; the fence must win where its authoritative order precedes owner visibility commit.
- **Storage:** prove that its authoritative decision barrier and one local transaction atomically commit VisibilityPointer, PublicationReceipt, owner outcome, receipt-consumption record and outbox; prove stale replica/restore behavior.
- **E:** persist the same operation ID/digest and remain non-terminal until the matching durable Storage PublicationReceipt is verified.
- **I implementation owner:** supply sequencer persistence, lookup, retention, failover and restore evidence.
- **D/E/Storage/I:** execute JF10-01..08 with build/runtime/database identities, deterministic fault injection, raw traces, expected/actual results and independent review.

In particular, I `COMMIT_WON` MUST NOT be interpreted as publication success. A D fence win, failed Storage transaction, changed digest, invalid lease, incomplete dependencies or unknown owner state still prevents visibility.

## 7. Governance and gate state

This technical interface acceptance does not approve I36-GOV-01..10 or any I35 governance decision. External approval still requires the named authorized approver, authority basis, exact policy text/hash, scope/jurisdiction, effective version/time, expiry/review and durable evidence.

- I36-GOV-01..08, I36-GOV-09 and I36-GOV-10: **GOVERNANCE-BLOCKED**.
- I authorization/revocation implementation: **NOT VERIFIED**.
- JF-10 implementation and conformance: **NOT IMPLEMENTED / NOT RUN**.
- Inventory seal and Global Forget completion: **NOT EVIDENCED**.
- Fact/Claim ADR-001: **ADR-BLOCKED**, independent and unchanged.

## 8. Conformance additions

The JF10-01..08 proposal cases remain required. Add:
- **JF10-I-09:** same operation ID/digest retry after receipt consumption returns the identical terminal result and sequencer position without second consumption.
- **JF10-I-10:** same operation ID with changed digest or any security-bound tuple conflicts and cannot alter the original decision.
- **JF10-I-11:** I crashes immediately before versus immediately after terminal decision persistence; recovery must distinguish the two only through authoritative lookup, never timeout inference.
- **JF10-I-12:** revocation follows a durable `COMMIT_WON`; recovery returns the original ordering fact while a different/new operation is denied under the advanced PermissionEpoch.
- **JF10-I-13:** failover/restore with replica lag cannot lose or duplicate receipt consumption, terminal outcome or sequencer position.

All cases are **SPECIFIED / NOT RUN** until an executable I sequencer and integrated DE-S harness exist.

## 9. Final disposition

I's technical interface portion of JF-10 is **ACCEPTED WITH THE BINDING CLARIFICATIONS ABOVE**. JF-10 as a cross-owner protocol remains **P0 OPEN**. No implementation, governance approval, consumer acceptance, deployment selection, test pass, Global Forget completion or Phase 3.6 final acceptance is claimed.
