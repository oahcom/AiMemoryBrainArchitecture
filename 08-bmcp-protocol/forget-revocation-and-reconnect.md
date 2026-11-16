# Forget, Revocation and Offline Reconnect

- Status: **CANDIDATE execution boundary; global policy and completion ADR-BLOCKED on I; canonical fence OPEN with D**
- Owner: H (wire notifications, Adapter clearing, reconnect and ACK behavior)
- Related issues: INT-P0-02, INT-P0-03, INT-X-02, INT-X-03, INT-X-04

## 1. Authority boundaries

- D owns canonical ForgetOperation identity, canonical suppression fence and canonical target references.
- I owns authorization/revocation policy, permission epoch, retention, target inventory, global completion criteria, backup/external-copy policy and any physical-erasure policy.
- G owns Context membership/version, removal/tombstoning, snapshot/delta invalidation and delivery supersession.
- H owns message encoding, Adapter managed-region clearing behavior, local queue suppression, reconnect ordering and truthful acknowledgement.
- C/Agent owns reasoning and tool/action authorization.

H cannot declare a global Forget complete. H can report only Adapter-local observations and acknowledgements. Clearing a local managed region does not prove deletion from provider logs, provider-retained prompts, hidden prompt caches, model internals, telemetry copies, backups or third-party systems.

## 2. Notification types

Candidate notification family operations:

| Operation | Meaning | Required authority reference |
|---|---|---|
| `ForgetFenceRaised` | Canonical target is suppressed under a new fence | D ForgetOperation ID + fence; I policy epoch |
| `ManagedRegionInvalidate` | Remove/disable affected entries from current managed Context | G Context ref/version + D fence |
| `DeliveryCancel` | Cancel Prepared/Delivered operations where possible | G delivery ID + superseding target/fence |
| `PermissionRevoked` | Authorization epoch changed; stop protected access | I Principal/permission epoch |
| `AdapterClearRequest` | Request Adapter to clear or render inaccessible managed local state | I/D/G references; policy action defined by I |
| `ReconnectReconcile` | Exchange current fences, policy epoch, Context target and unresolved deliveries | D/G/I authoritative references |
| `ClearAcknowledgement` | Report Adapter-local clear/suppression result | Adapter identity, capability epoch, operation ID |

A notification is not an authorization grant. A payload-supplied ActorRef does not authenticate the sender; transport principal binding and I policy are mandatory.

## 3. Managed-region clearing contract

On a valid, authorized Forget/revocation notification, the Adapter MUST:
1. Verify transport authentication and the I-authorized sender/operation binding.
2. Validate message integrity, expiry, scope and monotonic D/I fence or permission epoch.
3. Immediately mark affected managed entries/versions ineligible for future inference assembly.
4. Remove or cryptographically/render-time disable affected content from Adapter-controlled managed-region buffers, prompt caches and queued Context deliveries to the extent supported by the Adapter's declared capabilities.
5. Cancel or supersede Prepared/Delivered work that has not crossed the inference submission boundary.
6. Prevent any stale Snapshot/Delta, retry, offline queue replay or late ACK from reintroducing the invalidated content.
7. Persist a minimal local suppression marker sufficient to reject stale replay, without retaining reconstructive payload data.
8. Emit a ClearAcknowledgement with per-target status and evidence; if unable to clear, report Failed/Unknown and reason.

Where immediate physical removal from a local storage medium is not supported, Adapter must at minimum suppress access and disclose the limitation. The ACK must distinguish logical suppression from local cache purge and from any stronger storage-erasure claim. H does not define or promise secure media erasure.

## 4. Forget and revocation state distinction

- **Permission revocation** changes whether an actor may access an object/operation. It does not itself mean canonical memory is forgotten.
- **Forget** is a governed operation on canonical memory and applicable derivatives. It is not merely an access-denied response.
- **Context removal** changes G's managed Context membership; it is not canonical Forget.
- **Local clear ACK** is evidence about one Adapter instance and declared managed region only.
- **Global completion** is I's policy decision after D's barrier and all required targets are accounted for.

These are separate state machines. H MUST NOT merge them into a single `deleted=true` flag.

## 5. Fence and epoch ordering

D/I must provide authoritative opaque tokens for Forget fence and permission epoch. H:
- stores and compares tokens only according to an owner-defined comparison/ordering operation;
- MUST NOT mint, increment, numerically compare or infer semantics for these tokens;
- rejects a notification that is provably older than the locally recorded fence/epoch;
- if ordering cannot be established, fails closed and requests reconciliation;
- persists the highest confirmed fence/epoch needed to prevent stale replay across restart.

A notification for a newer fence supersedes older Context deliveries and pending application attestations for affected targets. A late ACK cannot clear or reverse the fence. H reports the local operation result; D/I decide whether it satisfies their global barrier.

## 6. Offline Adapter and reconnect protocol

When offline:
- Adapter marks pending delivery/application outcomes Unknown or Pending; it cannot claim Applied for a new inference request it cannot observe.
- Queued memory deliveries are not automatically safe to replay.
- Local queue retention and encryption are subject to I policy.
- Agent operation may continue without Brain memory according to Agent policy; memory omission is not a failure of Agent safety.

On reconnect, the Adapter MUST execute this order before applying queued context:
1. Re-authenticate transport and bind the peer to I's authenticated Principal.
2. Negotiate protocol version, capabilities and a fresh capability epoch if needed.
3. Fetch/receive current I permission/revocation epoch and D Forget fence for the Adapter's authorized scope.
4. Fetch current G Context target/version and delivery status.
5. Apply Forget/revocation suppression and clear affected managed-region entries/queues first.
6. Reconcile unresolved delivery IDs and ACKs. Mark stale/expired/superseded attempts accordingly.
7. Reject any Snapshot older than current G target or any Delta whose base version is not the exact current Adapter version.
8. If version continuity is unknown or a gap exists, request a full current Snapshot; never replay an unverified chain.
9. Apply only the current authorized Snapshot/Delta and report Prepared/Delivered/Applied at the appropriate evidence level.

No cached Context is restored before steps 1–5 complete.

## 7. Stale snapshot and anti-resurrection rules

- Every Snapshot/Delta is bound to Context ID, G target version, applicable D Forget fence and I permission epoch.
- Snapshot target older than current target: reject as stale.
- Delta base mismatch: reject and request full Snapshot.
- Delivery invalidated by a newer Forget fence or permission epoch: Superseded; never apply.
- Duplicate delivery with identical ID/digest: return prior result; do not reinsert.
- Same idempotency key with different digest: conflict and security/consistency signal.
- Unknown token ordering or unavailable authoritative state: fail closed; hold managed memory as unavailable until reconciliation.
- Late ACK: record historical evidence only if ordering proves the event occurred before invalidation; never reactivate the old target.
- A tombstone or local clear ACK does not establish physical erasure.

## 8. Acknowledgement and target accounting

Candidate per-target ACK values:
- `SUPPRESSED`: target cannot be included in future managed inference requests.
- `LOCAL_BUFFER_CLEARED`: Adapter-controlled volatile managed buffer cleared.
- `LOCAL_CACHE_PURGED`: declared Adapter-controlled cache purge completed.
- `QUEUED_DELIVERY_CANCELLED`: queued delivery cancelled or marked non-replayable.
- `FAILED`: attempted action failed; reason included.
- `UNKNOWN`: Adapter cannot verify result.
- `UNSUPPORTED`: Adapter lacks the relevant capability.

ACK binds operation ID, D fence, I permission epoch, G Context/delivery IDs where relevant, Adapter ID, capability epoch, observed time, evidence profile and integrity metadata. H sends it to D/I/G; it is not a global completion verdict.

I decides which target states satisfy policy. Unknown, offline, unsupported and failed targets remain visible and cannot be silently counted as confirmed.

## 9. Provider and model boundary disclaimer

BMCP/Adapter can control only the integration surfaces under its declared control. It cannot guarantee removal of:
- prompts or requests already transmitted to a model provider;
- provider-retained logs, abuse-monitoring records, backups or caches;
- hidden prompt copies or internal model state;
- model weights or any learned behavior;
- external systems outside the authenticated/managed Adapter boundary.

Any retention/deletion request to an inference provider is a separate provider-governed workflow. H MUST NOT state or imply that Adapter clear equals provider deletion or model forgetting.

## 10. Required race and fault tests

- Forget arrives while a Snapshot is Prepared or Delivered.
- Forget arrives after runtime submission but before ACK; preserve historical evidence without restoring current visibility.
- Permission revocation while Adapter is offline.
- Old permission epoch and old Forget fence replay after restart.
- New fence notification arrives out of order or duplicated.
- Adapter crashes between suppression and ACK; reconnect must re-verify persisted marker.
- Stale Snapshot arrives after a newer Context target.
- Delta base mismatch and missing intermediate version.
- Queue replay after revocation/Forget.
- Late Applied ACK after Superseded/Expired.
- Adapter cannot purge a local cache; must report unsupported/unknown, not success.
- Provider-side retained prompt is outside Adapter control; no physical-deletion assertion is emitted.
