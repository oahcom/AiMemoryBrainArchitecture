---
document_metadata:
  domain: security-governance
  role: design-specification
  steward: "user-authorized operator (delegated by account owner)"
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "Canonical source blob f14cb2149ca3f817229533005ab89dbdc7f0b3a8 on session-i-security-governance-2026-11-16"
        - "AID-2026-109 bilingual source mirror; translation parity not implied"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "English mirror body is copied from the canonical source; semantic translation is not applicable to this English counterpart."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "security-governance/forget-retention-backup-erasure bilingual mirror"
    canonical_scope_id: "security-governance/forget-retention-backup-erasure"
    canonical_scope_keywords:
      - security-governance
      - bilingual-mirror
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "09-security-governance/forget-retention-backup-and-erasure-policy.md"
---
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

---

## Phase 3 targeted remediation — global target inventory and evidence vector

**Status: CANDIDATE I governance contract.** This section refines the global policy; it does not implement D/E/F/G/H mechanisms or close INT-P0-03.

### 12. Two independent inventory/barrier authorities

Two values MUST remain distinct and MUST NOT be numerically compared, merged, or substituted:

- **ProducerDomainInventoryEpoch (I-owned):** monotonically versioned snapshot of the registered producer/recipient domain catalogue, including domain classes, registered instances, scope coverage, owner, capabilities and evidence obligations. It answers whether the global closed-world set of places that can create, retain, deliver or restore a target is complete.
- **ProducerRegistrationHighWater / WorkItemBarrier (D-owned):** the per-Forget fence snapshot of concrete registered work items and attempts admitted before the fence. It answers which individual work items must reach terminal disposition before D can close its barrier.

The I epoch is a catalogue revision, not a work sequence. D's barrier is a Forget-operation-specific work boundary, not a catalogue revision. A higher I epoch does not prove D work drained; a closed D barrier does not prove all producer/recipient domains were inventoried.

Every global completion bundle MUST bind both values independently:
`inventory_epoch_ref + inventory_seal_digest` and `D_forget_fence_ref + producer_registration_barrier_ref`, each with its issuer/owner, version, scope, timestamp and evidence reference. No arithmetic comparison is permitted.

### 13. Inventory epoch change during Forget

At seal time, I records the active ProducerDomainInventoryEpoch and a canonicalized inventory digest. While an operation is open:
1. A domain registration, capability expansion, scope expansion, new recipient, new backup/restore path or discovered producer increments the I inventory epoch.
2. If the change can affect the Forget target or its lineage, the operation transitions to **Reopened** (or remains pre-completion pending), the old seal becomes superseded for completion, and newly affected targets are enumerated.
3. The owner of the newly registered domain supplies its target-specific evidence contract; no target is assumed complete because it was absent from the previous seal.
4. I emits a new inventory seal version and completion evaluation restarts against the new seal and the still-distinct D barrier.
5. If a new producer is discovered after a prior completion, completion is invalidated and the operation is Reopened. An incident/audit event is mandatory.

The only permitted non-reopening change is a proven metadata-only catalogue edit that cannot change target coverage, capability, scope or evidence obligations; I must record the proof and reviewer.

### 14. Target Inventory Seal

A seal is a signed, immutable snapshot, not a permanent assertion that the universe can never change. It contains:
- `seal_id`, schema version, ForgetOperationId, inventory epoch and parent/superseded seal reference;
- sorted target identities and a digest over the canonical representation;
- registry source/version and enumeration timestamp;
- target owner, category/type, instance identity, exact ScopeRef coverage and scope-binding fingerprint;
- capability set and capability version, required actions/evidence profile;
- target status at seal time and any unresolved registration gaps;
- D fence reference and D barrier reference as separate opaque typed references when available;
- signer/verifier identity, integrity metadata and audit correlation.

Seal validity is invalidated by: a relevant producer-domain epoch change; a newly discovered target; target identity/owner/scope/capability/evidence-contract change; inventory enumeration gap; scope expansion; invalid signature; or evidence that the seal omitted an active domain. A seal does not close D's barrier and is not itself cleanup evidence.

### 15. Target identity and record

Each target record has a stable, non-recycled `TargetId` and at minimum:
- target type/category and domain class;
- stable instance identity (or a declared singleton logical target);
- accountable OwnerPrincipal/owner team and operational contact;
- exact ScopeRef set / coverage rule and scope fingerprint;
- capability set, capability epoch/version and supported action semantics;
- required evidence profile and verifier;
- registry state, online/disabled/revoked state and last inventory epoch;
- current target state and per-attempt evidence references;
- retention class, backup/external-copy status and jurisdiction where applicable.

Target identity is not merely a hostname or display name. It is bound to the authenticated owner/issuer and registered instance. Unknown target identity, ambiguous scope, untrusted issuer or missing owner is **Unknown** and blocks completion.

### 16. Minimum global target classes

| Target class | Minimum target coverage | Owner | Required completion evidence |
|---|---|---|---|
| D canonical | Canonical Memory/versions, ForgetFence and canonical dependency inventory | D | Fence installation proof, exact target-set binding, D work-item barrier reference, terminal disposition for all pre-fence work, canonical suppression proof |
| E producer | Ingress producers, compiler queues, leases, retries, DLQ, replay, staged outputs and derived artifacts | E | Producer/work registration receipt, compile/replay terminal watermark, derivative/dependency registration watermark, no late publication proof |
| F runtime | Each lexical/ANN/graph/temporal/evidence/provenance index partition, cache namespace and Working Set | F | Per-partition suppression/publication watermark, cache/Working Set invalidation evidence, stale candidate rejection proof |
| G context | Context entries, snapshots, deltas, ChangeSets, delivery ledger and pending deliveries | G | Reconciliation watermark, invalidated snapshot/delta evidence, delivery cancellation/supersession/completion disposition |
| H adapter | Each Adapter instance × managed region × relevant scope; local queues and caches separately where capabilities differ | H | ACK bound to Adapter identity, capability epoch, managed-region identity, scope, fence and operation; per-capability evidence |
| External recipient | Every registered export, webhook, sync, analytics, model provider and onward recipient | I registry; recipient executes | Delivery receipt plus recipient-specific deletion/withdrawal ACK or valid exception; onward-copy disclosure |
| Backup/replica/restore | Primary replicas, snapshots, WAL/archive, object versions, DR and restore destinations | Storage/backup owner | Catalog coverage, retention/expiry or erasure proof, restore quarantine and suppression-ledger replay evidence |
| Other derived target | Summaries, compactions, embeddings, projections, exports, search copies and newly registered derivatives | Creating domain owner | Lineage/dependency registration, suppression/cleanup watermark and no-recreation proof |
| Audit/observability | Traces, logs, metrics, support bundles and non-reconstructive tombstones | I + platform owner | Minimization scan/attestation, retention disposition, no reconstructive payload or digest |

Where a target class has multiple partitions, instances, regions or independent capability surfaces, each independently addressable unit is a target. Aggregated evidence is acceptable only if it cryptographically enumerates the covered members and proves no gaps.

### 17. Completion Evidence Vector (CEV)

The global result is a versioned vector, not a Boolean. Every component is typed and independently owned:

| Vector component | Meaning | Owner | Evidence required |
|---|---|---|---|
| `immediate_access_suppression` | Ordinary protected access, derivation, retrieval and delivery are blocked | D + local boundary owners | D fence + local suppression attestations |
| `producer_barrier_completion` | All pre-fence work items terminal and no bypass/late publication | D (barrier); E/F/G/H implement | D barrier reference, terminal dispositions, producer inventory completeness and late-output checks |
| `derived_artifact_cleanup` | Registered derivative lineage suppressed/cleaned | E and derivative owners | E registration/replay/derived watermarks and per-target cleanup evidence |
| `runtime_context_adapter_suppression` | F indexes/caches/Working Sets, G Context/delivery, H managed regions cannot expose forgotten target | F/G/H | Per-partition F watermarks; G reconciliation/delivery dispositions; H per-region ACKs |
| `external_copy_handling` | External recipients have acknowledged, failed, remain unknown, or are excepted | I + recipient | Recipient-specific request/receipt/ACK, onward-copy scope and exception reference |
| `backup_retention_restore` | Backup copies are isolated, retention-bounded, restore-suppressed and eventually expired/erased | Storage + I | Backup catalog, retention/expiry, restore-quarantine test, suppression-ledger replay, erasure proof if required |
| `physical_erasure` | Controlled copies/media have met the applicable irreversible-erasure standard | Storage/recipient + I policy | Exact systems/media/key scope, method, operator, postcondition/expiry and residual-copy statement |

Each component is represented as `Pending | Confirmed | Failed | Unknown | PolicyException | NotApplicable`, with NotApplicable permitted only when the sealed inventory proves the class is absent and the verifier approves the rationale. Component records include owner, target set, scope, typed watermark/reference, evidence digest, verifier, timestamp and policy version.

**Completed** requires all mandatory components Confirmed, all mandatory targets Confirmed, both I inventory seal and D barrier valid, no unresolved Unknown/Failed, and physical erasure Confirmed wherever the declared completion promise requires it. **CompletedWithPolicyException** is permitted only when each residual target is covered by an active, approved, unexpired exception and all non-excepted components are Confirmed. It is never described as physical erasure of excepted data.

A policy may expose separate milestone reports (e.g. AccessSuppressed, CleanupComplete, BackupDispositionComplete, PhysicalErasureComplete). It MUST NOT collapse them into one undifferentiated "deleted" result.

### 18. D/E/F/G/H evidence contracts consumed by I

- **D:** I consumes D's canonical ForgetOperation/fence reference, target-set digest, producer registration high-water/work-item barrier, dependency inventory reconciliation, terminal dispositions, and canonical suppression proof. I does not define D's atomicity or barrier internals.
- **E:** I consumes producer-class registration references, compile/replay watermarks, lease/retry/DLQ terminal evidence and derived dependency-registration/publication evidence. E's watermark cannot replace D's barrier.
- **F:** I consumes a distinct suppression/publication watermark for every relevant index/channel partition and cache/Working Set disposition. I does not define IndexWatermark.
- **G:** I consumes Context reconciliation, immutable snapshot/delta invalidation and each delivery's cancelled/superseded/completed/unknown disposition. A pending delivery remains unresolved.
- **H:** I consumes Adapter-local ACKs only for the exact registered Adapter target and capability surface. H ACK is never a global completion signal.
- **Storage:** I consumes catalog/restore/expiry/erasure proof; a main-table delete or logical tombstone is not physical-erasure proof.

A target evidence item must bind ForgetOperationId, TargetId, exact ScopeRef coverage, relevant D fence reference, inventory seal version, action, capability/evidence contract version, attempt ID, result, time, integrity/authentication metadata and verifier. PermissionEpoch is included when the action is permission-sensitive; it is not substituted for ForgetFence generation.

### 19. H ACK → target state mapping

| H ACK | I target disposition | What it proves | What it does NOT prove / next requirement |
|---|---|---|---|
| `SUPPRESSED` | At most `Confirmed` for immediate managed-region access suppression, if all bindings and capability scope verify | Target will not include affected content in future managed inference requests | Does not prove buffer/cache purge, queued cancellation, provider deletion or physical erasure; those remain separate target actions |
| `LOCAL_BUFFER_CLEARED` | `Confirmed` only for the declared volatile buffer-clear action | Adapter-controlled volatile managed buffer was cleared | Does not prove persistent cache purge, all queues, other regions or provider copies |
| `LOCAL_CACHE_PURGED` | `Confirmed` only for named cache(s) and declared purge capability | Adapter-controlled cache purge for the exact cache scope | Does not prove other caches/queues, external provider or media-level secure erasure unless separately attested |
| `QUEUED_DELIVERY_CANCELLED` | `Confirmed` only for named queued delivery IDs | Named queued delivery cannot be replayed under that Adapter contract | Does not prove already submitted requests or unrelated queues/deliveries cleared |
| `FAILED` | `Failed` for attempted target action | Action failed with authenticated reason evidence | Retry/escalation required; cannot satisfy completion |
| `UNKNOWN` | `Unknown` | Outcome cannot be established | Offline, timeout, ambiguous state or missing evidence blocks completion unless a valid narrow exception is approved |
| `UNSUPPORTED` | `Unknown` by default; `PolicyException` only after explicit approval | Adapter lacks the capability | Never Confirmed. Register an alternate control/disable the Adapter or approve a scoped residual-risk exception |

Mandatory H binding fields: ForgetOperationId, exact TargetId, authenticated AdapterIdentity/Principal and issuer, Adapter instance, managed-region/cache/queue identity, ScopeRef coverage, D ForgetFence reference (opaque), I PermissionEpoch reference where relevant, capability epoch/version, ACK type, action/attempt ID, delivery/Context refs where relevant, observed time, evidence profile/version, integrity/authentication proof and result reason. Missing or mismatched binding makes the ACK **Unknown** or **Failed**, not Confirmed.

One ACK can confirm only one action/capability surface. Multiple ACKs may be required for one Adapter target (e.g. suppression + buffer clear + cache purge + queued cancellation). Offline reconnect must authenticate, obtain current policy/fence, clear/reconcile before use; no ACK means Unknown/Pending.

### 20. Backup and external-copy completion semantics

Backup copies may remain physically present during an approved retention interval only when they are encrypted, catalogued, access-isolated, unavailable to ordinary runtime, and governed by a finite expiry/rotation deadline. The Forget/revocation control plane must survive independently of the backup snapshot. Restore is quarantine-only until the current Forget and permission ledgers have been replayed and all affected objects are suppressed or removed. A restore test must prove that forgotten targets cannot be queried, indexed, delivered or exported before release.

A retained backup is **BackupPending** or an explicitly approved **PolicyException**, never PhysicallyErased. At expiry, storage supplies catalog-specific deletion/crypto-erasure proof. Key destruction counts only if no plaintext, escrow, alternate key, replica or derived recoverable copy exists. External recipients are separately inventoried; an outbound delivery receipt is not a deletion ACK. A non-responsive recipient remains Unknown unless an approved exception exists.

### 21. Global Forget state machine

| State | Entry condition | Exit condition | Required audit evidence / failure recovery |
|---|---|---|---|
| Requested | Authenticated request received | Authorization approved and D operation linked, or denied | Request/actor/scope/decision; denied requests terminate as Failed/Rejected outside completion |
| InventorySealed | I enumerated domains and signed Target Inventory Seal | Immediate suppression evidence accepted | Seal digest, epoch, targets, scope and verifier; relevant catalogue change invalidates seal |
| SuppressionEstablished | D fence installed and mandatory read/derive/delivery paths report suppression | Producer barrier evaluation starts | D fence ref + per-boundary suppression; missing confirmation stays Pending/Unknown |
| BarrierPending | D barrier exists and pre-fence work remains | All required work terminal and D proof accepted | D work-item barrier, lease/retry/DLQ states; recover unresolved work, never time out to success |
| TargetCleanupPending | Barrier terminal; derived/runtime/context/adapter targets enumerated | All required cleanup targets Confirmed or excepted | E/F/G/H target evidence; retries and reopen on late derivative |
| ExternalCopyPending | External recipient targets exist and deletion/withdrawal requests sent | All required recipients Confirmed or approved exceptions | Recipient request/receipt/ACK, escalation and exception audit |
| BackupPending | Backup/replica/restore targets exist or retention period remains | Required restore safety and retention/erasure disposition complete | Backup catalog, isolation, expiry, restore test and physical-erasure evidence |
| CompletionEvaluated | All evidence vectors assembled against current seal and D barrier | Completed, CompletedWithPolicyException, Failed or Reopened | Signed evaluation snapshot; any missing/invalid/expired evidence returns to relevant pending state |
| Completed | All mandatory targets/components Confirmed; no active exception needed | Terminal unless later discovery invalidates proof | Immutable proof bundle; post-completion discovery forces Reopened |
| CompletedWithPolicyException | All non-excepted requirements Confirmed; every residual has active approved exception | Exception resolved/expired (then Reopened) or new review | Approval, scope, rationale, expiry, risk owner, controls and disclosure |
| Failed | Definitive non-compliance or policy denial prevents completion | Remediation/retry explicitly reopens operation | Failure reason, target, attempt, owner; never silently reset |
| Reopened | New target/domain, inventory seal invalidation, late derivative, restore resurrection or expired exception | New seal and re-evaluation; returns to appropriate pending state | Prior proof retained as superseded, new reason/epoch/targets recorded |

Transitions are monotonic in audit history. A terminal state is not silently edited. A later target discovery, inventory epoch change affecting coverage, invalid ACK, expired exception, failed restore suppression or evidence-integrity failure creates a new evaluation and Reopened state. Reopened does not erase the prior result; it marks the previous result superseded for current assurance.

### 22. Global completion hard stops

The following MUST prevent Completed:
- unknown/unregistered producer domain or recipient with plausible target coverage;
- invalid or superseded inventory seal;
- D barrier not closed, unresolved lease/work item, registration gap or late derivative;
- missing required E/F/G/H evidence or stale/partition-incomplete watermark;
- G pending delivery or H offline/unknown/unsupported target without valid exception;
- external recipient without required ACK/exception;
- backup restore path not quarantined or Forget ledger not replayed;
- physical erasure claimed without storage/media/key-scope evidence;
- expired/revoked PolicyException;
- permission/issuer/identity binding cannot be verified for a required action.

### 23. Phase 3 test cases (design acceptance; execution not claimed)

| Test | Scenario | Allowed final state | Forbidden state | Owner(s) | Required audit evidence |
|---|---|---|---|---|---|
| I-FGT-01 | Unknown Producer Domain at Forget | Reopened or Pending/Unknown | Completed | I + discovered domain + D | Unknown domain record, epoch change, new seal, D barrier reconciliation |
| I-FGT-02 | Fence installed with unresolved lease | BarrierPending | Completed / Barrier closed | D + lease owner | Work ID, lease/attempt, terminal disposition and D barrier proof |
| I-FGT-03 | I inventory changes during Forget | Reopened + new InventorySealed | Continue using old seal as complete | I + affected owner | Old/new epoch, diff, invalidation reason, new target evidence |
| I-FGT-04 | H Adapter offline, Clear cannot be confirmed | Unknown/Pending or approved narrow PolicyException | Confirmed / unconditional Completed | H + I | Last authenticated session, timeout, target identity, retry and exception if any |
| I-FGT-05 | H returns UNSUPPORTED | Unknown or approved PolicyException after alternate control review | Confirmed | H + I + risk approver | Capability declaration, unsupported action, alternative control and approval |
| I-FGT-06 | G Context Delivery remains Pending | TargetCleanupPending | Completed | G + H | Delivery ID, Context ref/version, pending reason and reconciliation attempts |
| I-FGT-07 | F IndexWatermark has not crossed required fence | TargetCleanupPending/Unknown | Runtime cleanup Confirmed | F + I | Partition ID, observed/required watermark refs, lag and retry |
| I-FGT-08 | Backup restore attempts to restore forgotten memory | BackupPending or Failed until quarantined/suppressed | Visible/restored to serving path | Storage + I + D | Restore job, quarantine proof, ledger replay, suppressed object count |
| I-FGT-09 | External recipient has no ACK | ExternalCopyPending/Unknown or approved exception | Confirmed / unconditional Completed | I + recipient owner | Request receipt, retry/escalation, non-response and exception |
| I-FGT-10 | PolicyException expires | Reopened / Pending/Unknown | Continue CompletedWithPolicyException | Approver + I + target owner | Expiry event, revoked exception, renewed evidence or new approval |
| I-FGT-11 | Permission revocation races Forget | Deny protected work; Forget continues under separately authorized operation or pauses if authority invalid | Reuse stale ALLOW / merge PermissionEpoch with fence generation | I + D/E/F/G/H | Principal/issuer, old/new PermissionEpoch, Forget fence, decision and in-flight outcome |
| I-FGT-12 | New derived target discovered after seal | Reopened; new target and seal | Retain prior Completed as current | Discovering owner + I + D | Derivation lineage, discovery time, epoch bump, invalidated proof and cleanup evidence |

These are specification-level cases only. No PASS is claimed without executable fixtures, environment, expected/actual output, test artifact and owner sign-off.



---

## Phase 3.5 governance reconciliation

The authoritative I-owned Producer/Recipient Domain Inventory, ACK-to-Target mapping and Global Forget Completion Vector are historically referenced in `phase-3.5-global-identity-forget-governance.md` §§3–5 and the detailed target contract. The referenced document is unsubmitted and not restored; see [documentation gaps](../../governance/documentation-gaps.md).

For avoidance of doubt:
- I's global `ProducerDomainInventoryEpoch` and D's per-Forget `ProducerRegistrationHighWater` / `WorkItemBarrier` are separate and both required.
- H ACKs are target/action-bounded evidence, not global completion and not physical-erasure proof.
- Unknown, Failed, Unsupported, stale, missing or contradictory evidence for a mandatory target blocks Completed.
- A sealed inventory is invalidated by relevant epoch changes, late derivative/recipient discovery or restore resurrection.
- Backup restore is quarantine-first and must apply the current independent Forget/revocation control ledger before any restored content is served, indexed, delivered or used for inference.
- External recipient request receipt proves delivery of a request only. Provider-internal and onward copies remain Unknown absent verifiable target-bound evidence or an approved narrow exception.
- Physical erasure remains a separate result requiring media/key-scope evidence under the applicable retention and jurisdiction policy.

All policy decisions remain subject to the OPEN register. This document does not claim that any target has actually been cleared, any backup expired, or any content physically erased.
