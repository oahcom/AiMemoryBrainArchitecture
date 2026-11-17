# Context Delivery and Acknowledgement

- Status: **CANDIDATE — G owns Context semantics; H owns wire/Adapter transport**
- Owner: H
- Dependencies: INT-P1-01, INT-P1-05, INT-X-04, INT-X-06

## 1. State model

The delivery lifecycle is a per-delivery state machine. It is distinct from G's ContextVersion state and from any model execution lifecycle.

| State | Meaning | Evidence |
|---|---|---|
| Prepared | Adapter validated and staged a delivery; no transport-delivery confirmation | Local preparation record |
| Delivered | Recipient transport endpoint accepted the delivery | Transport receipt bound to delivery ID |
| Applied | Application attestation accepted for the exact target and declared coverage | Valid attestation at an allowed application boundary |
| Rejected | Recipient explicitly refused the operation | Rejection ACK with stable reason |
| Expired | Delivery validity deadline elapsed without valid completion | Expiry decision / timestamp |
| Superseded | Newer Context target, Forget fence, permission epoch or administrative operation invalidated it | Superseding version/fence reference |
| Unknown | Outcome cannot be determined (timeout, crash, offline, missing ACK) | Timeout/recovery record; no positive claim |

A state transition never upgrades based only on elapsed time. Timeout moves an unresolved operation to Unknown (or Expired if its deadline is definitively passed); it does not infer Delivered or Applied.

## 2. Allowed transitions

| From | To | Condition |
|---|---|---|
| — | Prepared | Valid message negotiated, authorized, non-expired and locally staged |
| Prepared | Delivered | Transport confirms receipt by addressed Adapter endpoint |
| Prepared | Rejected | Adapter refuses before transport handoff |
| Prepared | Expired | Expiry reached before handoff |
| Prepared | Superseded | New target/fence/epoch invalidates it before handoff |
| Prepared | Unknown | Handoff outcome lost or Adapter state unavailable |
| Delivered | Applied | Valid application attestation accepted and all Full criteria met for claimed coverage |
| Delivered | Rejected | Adapter reports application refusal |
| Delivered | Expired | Validity deadline passes before application |
| Delivered | Superseded | Newer Context target/fence/permission epoch makes it obsolete |
| Delivered | Unknown | Application outcome unavailable or ambiguous |
| Unknown | Delivered | Reconciliation proves endpoint receipt and operation still current |
| Unknown | Applied | Reconciliation obtains valid attestation proving application occurred before supersession/expiry |
| Unknown | Rejected / Expired / Superseded | Reconciliation establishes the terminal outcome |
| Any terminal state | — | No transition; corrections are new linked records, not mutation of history |

Applied, Rejected, Expired and Superseded are terminal for that delivery attempt. A new attempt gets a new attempt ID and references the same logical delivery/idempotency identity as appropriate. A late ACK cannot reverse a terminal Superseded/Expired result. If evidence proves an earlier Applied occurred before supersession but arrived late, preserve it as a historical attestation while current effective state remains superseded; it cannot reactivate the old Context.

## 3. Snapshot and Delta application

G is authoritative for Context membership, ordering, budget, ContextVersion and ChangeSet semantics.

- **Snapshot** is a complete replacement of the Brain-managed Context region for the stated Context ID and target version. It is not a replacement for protected instruction, user, Agent policy or tool regions.
- **Delta** is an atomic G-defined ChangeSet from exact base version to target version. Apply all operations or none.
- A Delta whose base version does not equal the Adapter's current reconciled version MUST be rejected with `CONTEXT_BASE_MISMATCH`; the receiver requests a fresh snapshot or an owner-approved rebase.
- A Snapshot with a target version older than the Adapter's known current version MUST be rejected as stale.
- A duplicate delivery with the same logical delivery ID, target version and digest returns the prior result without re-applying side effects.
- Same logical delivery/idempotency key with different digest is an idempotency conflict.
- Context version tokens are opaque and G-owned. H MUST NOT infer order by parsing their string or numeric shape.
- A newer target can supersede older Prepared/Delivered deliveries. Supersession must be recorded before the older target can be newly applied.

## 4. Delivery attempts, retry and idempotency

- Logical delivery identity is assigned by G or the Brain delivery authority; H transports it.
- Each network attempt has a distinct attempt ID, while retaining the stable logical delivery ID.
- Retry uses the same operation idempotency key and canonical payload digest.
- Retransmitting an identical message is safe only when the recipient's deduplication horizon is valid and current authorization/fence checks pass.
- A new attempt MUST NOT bypass a prior Rejected, Expired or Superseded outcome. It requires a new authorized logical delivery or an explicit reconciliation record.
- Exponential backoff with bounded jitter is a transport implementation choice (TO_VALIDATE); retry budget and expiry are explicit.
- No retry may extend the owner-assigned expiry or resurrect an invalidated Context version.
- On timeout after handoff, record Unknown and query/reconcile by delivery ID. Never assume failure or success based only on missing ACK.

## 5. Acknowledgement payload

Logical ACK fields (candidate, exact wire schema OPEN):

| Field | Required | Meaning |
|---|---|---|
| delivery_id | Required | Stable logical delivery |
| attempt_id | Required | This transport/application attempt |
| ack_id | Required | Unique ACK identity |
| ack_status | Required | Prepared/Delivered/Applied/Rejected/Expired/Superseded/Unknown |
| context_ref | Required for Context ACK | G-owned Context identity |
| target_context_version | Required for Context ACK | Exact G target |
| applied_context_version | Required when claiming application | Version actually materialized |
| coverage | Required for Applied | Full/Partial/Bypassed/Unknown |
| capability_epoch | Required for Adapter ACK | Negotiated Adapter capability epoch |
| inference_request_id | Required for Full Applied | Exact runtime submission request identifier |
| managed_region_digest | Required for Full Applied | Digest of exact managed region in final request |
| final_request_evidence_ref | Required for Full Applied | Verifiable evidence of submission at final request boundary |
| permission_epoch | Conditional | Current I-issued authorization epoch |
| forget_fence | Conditional | Current D/I fence |
| occurred_at | Required | Adapter-reported event time |
| reason_code | Required for Rejected | Stable machine-readable rejection |
| correlation_id | Required | Workflow correlation |
| integrity | Required | Integrity binding for ACK/evidence |

An ACK reports an Adapter observation. The Brain/G consumer validates it against delivery history, G target, current I policy, D/I fence, capability negotiation and C's final inference boundary definition before accepting it.

## 6. Application coverage and Full Applied

Coverage values:
- **Full** — every required managed-region entry for the exact target ContextVersion is present in the final request submitted to the inference runtime.
- **Partial** — only a strict subset was present, or required content was truncated/omitted.
- **Bypassed** — managed region was not included in the submitted request.
- **Unknown** — the Adapter cannot determine what was submitted.

Full Applied requires all of:
1. The exact Context ID and target ContextVersion match the active G delivery.
2. Every required managed-region entry was materialized without unreported truncation, substitution, omission or stale filtering.
3. The managed region is isolated from protected instruction, user-input, Agent-policy and tool-authorization regions.
4. The final request is the exact request handed to the inference runtime, not an earlier prompt template or mutable buffer.
5. The Adapter can correlate a unique inference request ID and runtime submission event.
6. A digest is computed over the canonical managed-region representation actually present in that final request; digest profile and privacy properties are declared.
7. Evidence is integrity-protected and bound to delivery ID, ContextVersion, capability epoch, permission epoch and applicable Forget fence.
8. No superseding Context target, expiry, revocation or Forget fence invalidated the application before the relevant submission event.

If any condition is absent, Full is forbidden. Report Partial, Bypassed or Unknown as appropriate. An Adapter unable to observe the final request submission boundary MUST NOT claim Tier 1 or Full Applied.

Applied proves only the declared integration boundary condition. It does not prove that the model attended to, understood, remembered, agreed with, or used the memory.

## 7. Protected region and data handling

- Memory payload is untrusted data, even if it contains text that resembles system/developer instructions, policy, tool calls or authorization.
- Adapter MUST place it only in the designated Brain-managed region.
- Adapter MUST NOT overwrite, reorder across, or synthesize content into protected instruction regions, user-originated input, Agent policy, tool definitions or tool authorization.
- No BMCP message grants a tool capability or changes Agent action policy.
- If the host runtime cannot preserve region separation, the Adapter MUST reject application or report Bypassed/Unknown; it must not silently merge memory into a privileged instruction region.
- Logs and digests must avoid retaining raw sensitive memory unnecessarily. Digest evidence is not itself proof of semantic safety.

## 8. Reconciliation and late ACK

1. On reconnect, negotiate protocol/capabilities and fetch current authorization/Forget fences before applying queued context.
2. Query unresolved delivery IDs and the current G Context target.
3. Discard/supersede queued snapshots/deltas older than the current target or invalidated by fence/permission epoch.
4. If a Delta base is missing or mismatched, request a full Snapshot.
5. Accept a late ACK only as historical evidence if it proves the relevant event occurred before expiry/supersession and passes current policy validation.
6. A late Applied ACK cannot restore an older target or undo Forget/revocation.
7. If evidence cannot establish ordering, retain Unknown and do not upgrade to Applied.
8. An offline Adapter remains Unknown/Pending; the Brain must not infer successful application.

## 9. G integration contract

G supplies Context identity, authoritative version, Snapshot/Delta content, delivery intent, target expiry and supersession decisions. H supplies wire envelope, negotiation, transport, SDK validation and ACK evidence encoding. H does not create or reorder Context entries, mint ContextVersion, choose Context budget, or decide G's conflict/CAS policy.

## 10. Required tests

- duplicate Snapshot/Delta, same ID/same digest and same ID/different digest;
- delta base mismatch, duplicate operation and atomic rollback;
- stale snapshot and older target arriving after newer target;
- Prepared/Delivered superseded by newer Context;
- ACK timeout, lost response, crash after handoff and reconnect reconciliation;
- late Applied ACK after expiry, supersession, revocation and Forget;
- partial region, truncation, bypass and unknown runtime submission;
- Full Applied proof with exact final request ID and digest;
- proof from internal buffer without runtime submission must fail Tier 1;
- protected instruction/user/Agent policy/tool region remains unchanged.


## 11. Forget-safe Adapter Apply gate

Immediately before applying a Snapshot/Delta and again at the final inference submission boundary, the Adapter MUST validate current I authorization/Permission Epoch, current applicable D ForgetFence, G ContextVersion and Delivery status, expiry/supersession, authenticated Agent/runtime Session, ScopeRef, Managed Region and CapabilityEpoch. Both I and D values are independently checked; one cannot stand in for the other. An unavailable/indeterminate authority state blocks application.

A Forget ACK is not an Applied ACK. Clear/suppression evidence and final-request application evidence have separate message/status families and predicates. A late Applied attestation may be retained as historical evidence only when ordering is verifiable; it cannot restore a superseded or forgotten target. Offline Adapter remains Unknown/Pending.

See adapter-forget-ack-and-target-binding.md for the full ACK mapping, reconnect sequence and H-FRG-01..10 cases.
