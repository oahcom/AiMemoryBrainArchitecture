# Forget, Retention, Backup and Physical Erasure Policy

- Owner: Session I
- Status: **CANDIDATE global governance contract; D/E/F/G/H implementation and external-recipient proof OPEN**
- Related: INT-P0-03, INT-X-02, INT-X-04, D-REV-P1-003, CT-004, CT-009..014, CT-020.

## 1. Purpose and promises

Forget is a governed cross-system workflow, not a single row deletion. This policy distinguishes:

1. **Immediate logical suppression:** stop all new access, derivation, candidate emission, Context application and restore-based reappearance under a durable fence.
2. **Asynchronous derivative cleanup:** remove or render inaccessible registered derivatives, indexes, caches, Working Sets, summaries, embeddings, exports and downstream copies according to their ownership and capabilities.
3. **Physical erasure:** irrecoverably remove content and recoverable copies from controlled primary storage and backup media according to the approved retention/backup schedule and evidence standard.

These states are separate. `Suppressed` does not mean `Cleaned`; `Cleaned` does not necessarily mean all backups expired; an external provider acknowledgement does not prove its hidden internal copies were physically erased unless the provider supplies an auditable guarantee within its control.

## 2. Authority split

- D owns canonical ForgetOperation identity, target references, canonical fence/generation and dependency inventory contract.
- I owns authorization to initiate/approve Forget, target inventory policy, completion criteria, exception classes, retention/legal hold rules, external-copy policy, audit and erasure evidence requirements.
- E registers compiler work and derived dependencies before publication and suppresses its queued/leased/retry/DLQ/replay outputs.
- F suppresses retrieval candidates, in-flight results, caches, Working Sets, indexes and rebuilds.
- G tombstones Context entries, invalidates snapshots/deltas and blocks stale delivery/Applied.
- H clears/quarantines the managed Adapter region and reports trustworthy capability-bounded acknowledgement; H does not own global completion.
- Storage/backup operators execute primary/replica/backup erasure and restore controls.
- External recipients act under contractual/API obligations; Brain records only verifiable responses.

## 3. Forget operation lifecycle

A request is authenticated and authorized against subject rights, resource ownership, scope, purpose, retention, legal hold and delegation. A request can be denied, narrowed, deferred or approved. A successful approval creates a durable operation linked to D's canonical `ForgetOperationId` and monotonically ordered `ForgetFence`.

Recommended high-level phases:

`Requested → Authorized → SuppressionCommitted → InventorySealed → CleanupInProgress → CompletionEvaluated → Completed | CompletedWithPolicyException | Failed | Cancelled`

The operation phase is not the Memory lifecycle. D's canonical lifecycle semantics remain authoritative. A request cannot be marked completed merely because a canonical Memory lifecycle field changed or a tombstone exists.

### 3.1 Immediate suppression barrier

At the suppression linearization point:
- D atomically commits the Forget fence/suppression record for the affected typed references and Scope.
- Every read/write/derivation/dereference/delivery path checks the fence before disclosure or commit.
- E/F/G/H stop exposing or applying affected content, including in-flight work that has not crossed its irreversible boundary.
- New dependencies cannot be registered against a sealed target without being included in a reopened/reconciled inventory and barrier.
- If any mandatory enforcement domain cannot confirm fence visibility, the global status is `SuppressionPending`, not successful suppression.

The target can be hidden before all replicas/indexes finish cleanup, but no caller may be told that cleanup or physical erasure is complete.

## 4. Required target inventory

The inventory is closed only when all registered producer/consumer/copy domains for the target's lineage and scope are enumerated and their relevant watermarks are accounted for. Inventory categories:

| Category | Examples | Required evidence |
|---|---|---|
| Canonical primary | Memory/Claim/Evidence/Provenance/Entity/Relation payloads and versions | D state + storage deletion/retention result |
| Compiler in-flight | queued, leased, retry, DLQ, replay, model job, staged output | E producer barrier and per-job terminal/fence result |
| Derived artifacts | summaries, compactions, embeddings, entity projections, relation projections | lineage dependency inventory + deletion/suppression watermark |
| Runtime | lexical/ANN/graph/temporal indexes, caches, Working Sets, query caches | F per-partition watermarks and invalidation evidence |
| Context | ContextEntry revisions, snapshots, deltas, delivery ledger, renderings | G reconciliation watermark and stale-delivery cancellation |
| Adapter / Agent integration | local managed region, offline queue, persistent adapter cache | H clear/quarantine ACK, capability and session binding |
| External recipients | exports, webhooks, sync targets, analytics processors, third-party storage | recipient registry, delivery receipt, recipient status/evidence |
| Backups / replicas | replicas, snapshots, WAL/archive logs, object versions, DR copies | backup catalog, expiry/deletion receipt, restore-fence proof |
| Audit / observability | event logs, traces, support bundles, metrics labels | minimization and non-reconstructive audit policy |
| Human exports | user/admin downloads or copied content under disclosed control | notification/recall request; status may remain Unknown |

Every producer and recipient domain must register with a stable target class, owner, scope coverage, supported operations, last processed watermark, online/offline state, retention horizon and evidence capability. An unregistered copy discovered later reopens the inventory and invalidates prior completion claims where policy requires.

## 5. Per-target state machine

Each target has exactly one current status:

- **Pending:** target registered; action not yet attempted or no terminal evidence.
- **Confirmed:** target performed the required action and supplied valid evidence bound to ForgetOperationId, target identity, scope, fence, action and watermark/time.
- **Failed:** action attempted and definitively failed or target reported non-compliance.
- **Unknown:** target unreachable, offline, unsupported, evidence missing/invalid, watermark gap or outcome ambiguous.
- **PolicyException:** residual retention/copy is explicitly allowed by an approved policy exception with scope, reason, approver, expiry/review date and compensating controls.

Unknown/offline is never silently converted to Confirmed. A timeout is Unknown, not Failed or Confirmed. Retrying an Unknown target is required where possible; every attempt is separately recorded.

A target is Confirmed only for the precise claim its evidence supports. For example, an Adapter may confirm its managed region cleared, not that a model provider erased prompts. A backup service may confirm expiry from a backup set, not deletion from all external recipients.

## 6. Barrier, watermark and no-resurrection proof

The global proof is a typed vector, not one scalar:

- canonical ForgetFence / generation (D);
- producer registration epoch and in-flight producer barrier (D/E);
- source/compile work watermark and derivative-registration watermark (E);
- per-index/per-partition publication and suppression watermark (F);
- Context reconciliation / delivery watermark (G);
- Adapter capability epoch, session/delivery clear attestation (H);
- external recipient acknowledgement or exception (I registry);
- backup catalog/expiry/restore watermark (storage);
- audit minimization completion marker (I).

Completion evaluation requires:
1. the target inventory is sealed at a recorded producer-registration epoch;
2. every producer capable of creating a derivative has crossed the barrier or is disabled/revoked;
3. every in-flight operation at or below the barrier is terminal and cannot publish after the fence;
4. every consumer/partition has advanced beyond the required ForgetFence and has no visible stale object;
5. each required external recipient and backup target is Confirmed or an explicitly approved PolicyException;
6. restore/replay paths reapply the fence before content becomes queryable or deliverable;
7. no unresolved Unknown or Failed required target remains;
8. evidence is complete, authentic, scope-bound and independently auditable.

If a producer or consumer is offline, the target stays Unknown/Pending and completion remains blocked unless a specifically authorized PolicyException allows only the stated residual risk. A closed watermark is meaningful only if producer registration is complete and no new producer can bypass it.

## 7. Retention and legal hold

Retention classes are policy metadata set at collection/commit time and re-evaluated when purpose or law changes. Retention must specify data class, owner, trigger, minimum/maximum period, disposition, backup treatment, region and legal basis. I defines governance; storage implements.

A valid legal hold:
- identifies authority, case/reference, scope, affected data classes and start time;
- is approved by authorized Legal/Privacy role distinct from the request operator where feasible;
- blocks physical erasure only for the minimum necessary content;
- does not automatically authorize ordinary retrieval, model prompt inclusion, analytics, export or continued derivation;
- does not cancel immediate logical suppression from ordinary application paths;
- is reviewed periodically and has an explicit release condition.

When a held item is subject to Forget, ordinary access is suppressed while a separately isolated hold copy may be retained under restricted Legal access. That copy is a declared PolicyException target; it must not flow into indexes, Context, training, Agent retrieval or normal backups. On hold release, erasure resumes and evidence is attached.

A retention obligation may require keeping minimum accounting evidence, but not source content by default. If policy/law conflicts are unresolved, status is PolicyException only after authorized counsel/privacy approval; otherwise it remains Pending/Unknown and escalates.

## 8. Backups, replicas and restore

- Backups are encrypted, access-restricted, catalogued, time-bounded and assigned explicit expiry.
- Forget fences and tombstone manifests are stored in a control plane that survives backup restore and is not rolled back with data snapshots.
- Restore must occur into quarantine; before serving reads, replay the current revocation/Forget ledger and suppress or erase affected objects.
- A restore process cannot mark an object visible until policy epoch, ForgetFence and backup inventory are reconciled.
- Immutable/WORM backups are not described as erased before expiry. They remain PolicyException/retained under access controls where legally approved.
- Backup rotation/expiry and cryptographic erasure are evidence-bearing but must state the precise storage layer and key scope affected.
- Key destruction is physical-erasure evidence only if every relevant copy is encrypted solely under that key and no plaintext, derived key, escrow or alternate copy remains.

## 9. External copies and provider limits

Every external recipient must have a registered purpose, data classes, jurisdiction, retention, onward-transfer terms, deletion API/notification path and evidence type. On Forget:
1. stop new exports immediately;
2. send recipient-specific deletion/withdrawal request;
3. record delivery and acknowledgement separately;
4. retry and escalate non-response;
5. preserve only the minimal non-reconstructive audit evidence;
6. classify unreachable/unsupported recipient as Unknown or PolicyException, never Confirmed.

Human copies and undocumented third-party copies may be beyond Brain's technical control. User-facing completion reports must state the boundary and unresolved recipients.

For model/inference providers, I can require minimization, zero-retention or deletion terms where available and record contractual/API assurances. I cannot assert deletion of hidden provider prompts, internal model state, safety/abuse logs, training corpora or undocumented backups without a provider-specific, verifiable guarantee. “Adapter cleared” and “request no longer sent” are not provider physical erasure.

## 10. Physical erasure evidence

A physical-erasure claim identifies:
- exact storage systems, replicas, media/object versions and backup sets in scope;
- content classes and deletion method;
- deletion/crypto-erasure operation and key scope where applicable;
- time, operator/service identity and authorization;
- verified postcondition or expiry proof;
- residual copies and exceptions;
- evidence retention period and limitations.

Physical erasure may be delayed by approved backup rotation or legal hold, but the report must say so. Do not use a tombstone, cache invalidation, index delete request or content digest as proof of physical erasure.

## 11. Completion result

Global result:

- `SuppressionStatus`: Pending | Confirmed | Failed | Unknown
- `CleanupStatus`: Pending | Confirmed | Failed | Unknown | PolicyException
- `PhysicalErasureStatus`: Pending | Confirmed | Failed | Unknown | PolicyException
- `OverallCompletion`: NotComplete | Completed | CompletedWithPolicyException | Failed

`Completed` requires all required targets Confirmed, barriers closed, restore safety proven, and physical erasure confirmed where the policy's promise requires it. `CompletedWithPolicyException` requires each residual target to be explicitly excepted and approved; it must never be displayed as unconditional erasure. A system may report suppression confirmed while cleanup and erasure remain pending.

## 12. Open dependencies

- D must publish durable ForgetOperation ID, fence semantics, producer barrier and dependency inventory.
- E must prove atomic dependency registration and no late derivative publication across queue/lease/retry/DLQ/replay.
- F must expose per-channel/per-partition suppression watermarks and block stale cache/index rebuild.
- G must expose Context reconciliation and delivery cancellation watermarks.
- H must define Adapter clear/quarantine acknowledgement and reconnect gate; H candidate package was reviewed on `session-h-bmcp-protocol` @ `fcc5103399b4c322e52d642cae5a2414969399a7`; its Adapter-local clear/ACK semantics are candidates, not global completion proof.
- Storage must provide backup inventory, restore quarantine, expiry and physical-erasure evidence.
- I policy does not replace any local module implementation or conformance proof.
