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
        - "Canonical source blob 9100061fa986fb6676656169de3fcf9fc1c72664 on session-i-security-governance-2026-11-16"
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
    canonical_scope: "security-governance/global-forget-target-inventory bilingual mirror"
    canonical_scope_id: "security-governance/global-forget-target-inventory"
    canonical_scope_keywords:
      - security-governance
      - bilingual-mirror
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "09-security-governance/global-forget-target-inventory-and-completion-evidence.md"
---
# Global Forget Target Inventory and Completion Evidence Contract

- Owner: Session I — Security, Identity & Governance
- Status: **CANDIDATE global governance contract; D/E/F/G/H/Storage conformance OPEN**
- Related: CR-P1-05, CR-P0-02, INT-P0-02, INT-P0-03, INT-X-02, INT-X-03, CT-004, CT-009..014, CT-020.
- Companion: `forget-retention-backup-and-erasure-policy.md`

## 1. Purpose and ownership

This document defines the I-owned closed-world inventory and the evidence I requires to evaluate global Forget. It does not implement local suppression, queues, indexes, Context versions, wire messages, Adapter SDKs, backup deletion or storage transactions.

- I owns Producer Domain Inventory Epoch, target registration policy, Target Inventory Seal, global evidence vector, exception policy and global state evaluation.
- D owns canonical ForgetOperation, ForgetFence, canonical dependency inventory, producer registration high-water and per-operation work-item barrier.
- E/F/G/H own their respective producer/consumer execution and local evidence.
- Storage/backup operators own backup catalog, restore quarantine, expiry and physical-erasure execution.
- External recipients own their own deletion actions; I records verifiable evidence only.

## 2. Non-interchangeable epochs and barriers

| Name | Authority | Scope | Question answered | Prohibited substitution |
|---|---|---|---|---|
| ProducerDomainInventoryEpoch | I | Global registered producer/recipient domain catalogue, scoped by governance registry | Have all classes and instances capable of creating/holding/delivering/restoring data been enumerated? | Not a work-item sequence or a D barrier |
| ProducerRegistrationHighWater / WorkItemBarrier | D | One ForgetOperation and its registered concrete work items | Which pre-fence work items must reach terminal disposition? | Not a global domain inventory epoch |
| ForgetFenceGeneration | D | Canonical target/lineage suppression namespace | Which canonical suppression generation applies? | Not PermissionEpoch or index watermark |
| PermissionEpoch | I | Policy domain | Is this actor/operation still authorized under current policy? | Not ForgetFenceGeneration |
| IndexWatermark | F | One index/channel partition | How far has that partition published/processed? | Not a global Forget proof |
| ContextVersion | G | Context aggregate | Which desired Context state is current? | Not a Forget or authorization epoch |
| AdapterCapabilityEpoch | H | Adapter instance/capability profile | Which Adapter capabilities were declared/negotiated? | Not proof that a clear action succeeded |

All references are typed opaque values. A verifier uses the issuing authority's comparison/validation operation. Cross-namespace numeric comparison, conversion or equality is invalid.

## 3. Producer Domain Inventory

Every domain capable of creating, transforming, retaining, copying, serving, applying, restoring or exporting a target or its derivative must register before it processes protected data.

A registry entry contains:
- stable, non-recycled TargetId and target class/domain class;
- owner Principal/issuer and accountable owner team;
- authenticated instance identity or explicitly declared singleton identity;
- exact ScopeRef coverage and scope-binding fingerprint;
- capability set, capability version/epoch and supported actions;
- producer/recipient role and lineage relationship;
- online, offline, disabled, revoked or unknown status;
- evidence profile, required acknowledgements, verifier and endpoint contract version;
- retention class, backup/restore relationship, jurisdiction and onward-recipient obligations;
- first/last observed inventory epoch and audit references.

A payload-supplied producer, recipient, Adapter or owner ID is only a claim. Registration is accepted only after authenticating the issuer/Principal and binding the instance to the declared ScopeRef coverage. Untrusted issuer, ambiguous identity, missing owner or unknown scope is a registry gap.

### 3.1 Required domain classes

1. D canonical Memory/ForgetFence and canonical dependency inventory.
2. E ingress producers, compiler workers, queues, leases, retries, DLQ, replay, staged outputs and derived artifacts.
3. F indexes per partition, retrieval materializations, caches, Working Sets and rebuild workers.
4. G Context membership/materializations, snapshots, deltas, ChangeSets, delivery intents and delivery ledger.
5. H Adapter instances, each managed region, local buffers, queues and caches according to independently declared capabilities.
6. External recipients: webhooks, exports, sync services, analytics, model/inference providers and onward recipients.
7. Backups, replicas, snapshots, WAL/archive logs, object versions, disaster-recovery stores and restore destinations.
8. Other derived or copied artifacts: summaries, compactions, embeddings, projections, reports, human/admin exports and support bundles.
9. Audit/observability systems: logs, traces, metrics, incident attachments and non-reconstructive tombstones.

Each independent partition/region/instance/capability surface is separately addressable where its action/evidence can differ. An aggregate entry is valid only with an authenticated, complete member enumeration.

## 4. ProducerDomainInventoryEpoch lifecycle

I increments the epoch whenever a registration, retirement, capability change, scope change, owner/issuer change, new recipient, backup path or evidence-contract change can affect closed-world coverage. The epoch is monotonic only within the I registry authority.

For a Forget operation:
1. I snapshots the current registry epoch and computes a canonical inventory digest.
2. I enumerates all target records applicable to the Forget target/lineage and requested Scope.
3. I seals the enumeration with signer, schema, digest, timestamp, epoch, evidence requirements and unresolved-gap list.
4. The seal is referenced by the Forget operation and every completion evaluation.
5. Relevant registry change or late target discovery invalidates the seal and requires Reopened plus a new seal and evidence reconciliation.

A purely descriptive metadata correction may avoid reopening only if an independent reviewer verifies that target membership, scope, capability and evidence obligations are unchanged. The proof is audited.

## 5. Target Inventory Seal schema

Logical model (not wire encoding):

```text
TargetInventorySeal {
  seal_id
  schema_version
  forget_operation_id
  producer_domain_inventory_epoch
  canonical_inventory_digest
  target_records[]
  enumeration_started_at
  sealed_at
  unresolved_registry_gaps[]
  d_forget_fence_ref?                 // opaque D reference
  d_work_item_barrier_ref?             // opaque D reference, separate
  signer_principal_ref
  issuer_ref
  integrity_proof
  supersedes_seal_id?
  audit_correlation_id
}
```

Each target record includes TargetId, category, domain class, authenticated instance identity, OwnerPrincipal, ScopeRef coverage, capability profile/version, required action, evidence profile, current status and verifier. The seal is immutable. Its digest covers canonical ordering and every target field that affects scope or proof.

Seal invalidation conditions:
- relevant ProducerDomainInventoryEpoch change;
- new producer, recipient, replica, derived target or restore path;
- target identity, owner, scope, capability or evidence-contract change;
- unresolved enumeration gap or registry partition loss;
- issuer/signature verification failure;
- evidence that a target was omitted or misclassified.

A seal proves what I enumerated at a point in time. It does not prove D's work queue drained, a target was cleaned, or a backup was erased.

## 6. Per-target state and evidence

Target state is one of:

- **Pending:** registered; action not completed or evidence not yet evaluated.
- **Confirmed:** the exact required action for this target and scope has valid authenticated evidence.
- **Failed:** attempted action definitively failed or owner reported non-compliance.
- **Unknown:** offline, timeout, unsupported capability, ambiguous outcome, missing/invalid evidence or watermark gap.
- **PolicyException:** residual condition is explicitly approved under the exception policy. It is not a technical success.

Evidence must bind ForgetOperationId, TargetId, inventory seal ID/version, exact ScopeRef coverage, action, relevant D ForgetFence reference, capability/evidence-contract version, attempt ID, status, timestamp, authenticated producer/owner identity, integrity proof, verifier and audit correlation. Include PermissionEpoch for permission-sensitive actions; never use it as a replacement for D's fence.

A retry is a new attempt linked to the prior attempt. Timeout remains Unknown. Contradictory ACKs are audited and resolved by the target owner/verifier; a later positive ACK does not erase a prior failure record.

## 7. Completion Evidence Vector

Global completion is a typed vector:

| Component | Owner evidence | Confirmed only when |
|---|---|---|
| ImmediateAccessSuppression | D fence + local boundary suppression | All mandatory protected access/derive/deliver paths are blocked |
| ProducerBarrierCompletion | D barrier + E/F/G/H work disposition | D confirms every pre-fence item terminal, no registry gap, lease or late publication |
| DerivedArtifactCleanup | E lineage/registration and derivative owner evidence | Every registered derivative target is suppressed/cleaned to required policy level |
| RuntimeContextAdapterSuppression | F per-partition/cache, G reconciliation/delivery, H per-region ACK | Every mandatory consumer target is at/after required fence and cannot expose stale state |
| ExternalCopyHandling | recipient request/receipt/ACK or exception | Each external target is Confirmed or has active approved exception |
| BackupRetentionRestore | backup catalog, retention, quarantine and restore evidence | All backups are isolated and restore-safe; required expiry/erasure is complete or excepted |
| PhysicalErasure | storage/recipient media/key evidence | Applicable physical-erasure standard is independently evidenced |

Each component state is `Pending | Confirmed | Failed | Unknown | PolicyException | NotApplicable`. NotApplicable requires proof from the sealed inventory that the category is absent, plus reviewer approval. Component rollups cannot hide missing partition members.

## 8. H Adapter ACK mapping

| H ACK | Target state mapping | Evidence boundary |
|---|---|---|
| SUPPRESSED | Confirmed only for managed-region access suppression | Exact target cannot enter future managed inference requests; no purge claim |
| LOCAL_BUFFER_CLEARED | Confirmed for named volatile buffer action only | Does not cover persistent caches, queues or provider copies |
| LOCAL_CACHE_PURGED | Confirmed for named Adapter-controlled cache(s) only | Not secure media erasure or other cache/region coverage |
| QUEUED_DELIVERY_CANCELLED | Confirmed for enumerated delivery IDs only | Does not cover already submitted requests or unrelated queues |
| FAILED | Failed | Attempted action definitively failed |
| UNKNOWN | Unknown | Outcome not verifiable |
| UNSUPPORTED | Unknown by default; PolicyException only after explicit approval | Capability absence; never Confirmed |

Mandatory binding: ForgetOperationId, TargetId, authenticated AdapterIdentity and issuer, instance ID, managed-region/cache/queue identity, ScopeRef coverage, D fence reference, PermissionEpoch where relevant, capability epoch/version, ACK type, action/attempt ID, G Context/delivery refs where relevant, observed time, evidence profile/version, integrity proof and reason. Missing binding means Unknown/Failed. An ACK for one action does not imply another action is complete.

Offline Adapter is Unknown/Pending until authenticated reconnect, current permission/fence acquisition, managed-region suppression/clear, delivery reconciliation and a valid target-bound ACK. No implicit success.

## 9. Backup, restore and external-copy evidence

A backup target must report catalog identity, snapshot/replica/WAL coverage, retention expiry, encryption/key scope, isolation state, restore destination controls and deletion/crypto-erasure evidence. Restore is quarantine-only. Before serving or indexing, it must replay the current independent Forget/revocation control ledger and prove affected data remains suppressed or removed. The control ledger cannot be rolled back with the data snapshot.

A backup retained until expiry remains BackupPending or PolicyException, not PhysicallyErased. A main-table delete, tombstone, cache invalidation or restore deny alone is not physical-erasure proof. Key destruction is sufficient only if all relevant copies are encrypted solely under that key and no plaintext, escrow, alternate key or recoverable derivative remains.

External recipient delivery receipt proves only receipt of a request. Deletion/withdrawal ACK must identify the recipient, scope, affected copy class, action, time, onward-transfer handling and evidence assurance. Provider-internal copies beyond verifiable control remain Unknown or a narrowly approved exception; Adapter ACK never proves provider erasure.

## 10. Global state machine

```text
Requested
  -> InventorySealed
  -> SuppressionEstablished
  -> BarrierPending
  -> TargetCleanupPending
  -> ExternalCopyPending
  -> BackupPending
  -> CompletionEvaluated
       -> Completed
       -> CompletedWithPolicyException
       -> Failed
       -> Reopened

Any relevant inventory change, late derivative, restore resurrection,
expired exception or invalidated evidence after completion -> Reopened.
```

| State | Entry / exit criteria |
|---|---|
| Requested | Authenticated request; authorize and bind D operation |
| InventorySealed | I has a signed, gap-free inventory snapshot; relevant changes invalidate it |
| SuppressionEstablished | D fence and mandatory immediate suppression evidence are valid |
| BarrierPending | D work-item barrier remains open until all included work reaches durable terminal disposition |
| TargetCleanupPending | E/F/G/H and other internal targets are reconciled; Pending delivery or stale partition keeps it open |
| ExternalCopyPending | All external recipients are confirmed or explicitly excepted |
| BackupPending | Backup retention/restore safety and required erasure are pending |
| CompletionEvaluated | Current seal, D barrier and all typed evidence are verified |
| Completed | All mandatory targets/components Confirmed; no unresolved Unknown/Failed; restore safe; required physical erasure proven |
| CompletedWithPolicyException | Every residual is explicitly scoped, approved, unexpired and disclosed; all other requirements confirmed |
| Failed | Definitive non-compliance or authorization failure; retry only through audited remediation/reopen |
| Reopened | Prior proof superseded by new target, epoch/seal change, late derivative, expired exception, restore issue or invalid evidence |

Transitions are audit-monotonic. Terminal states are never silently edited. Reopened retains the prior completion proof as historical evidence marked superseded.

## 11. PolicyException minimum approval

A PolicyException requires:
- exact operation, TargetId(s), scope and residual data class;
- unmet action/evidence and why it cannot be completed;
- reason code/legal basis and risk assessment;
- named approving authority and independent reviewer;
- effective time, hard expiry, review date and revocation condition;
- isolation, encryption, access restriction and no-derivation/no-delivery controls;
- risk owner, user-disclosure requirement and signed audit record.

Approval is class-specific: Legal + Privacy for legal hold; Storage owner + Privacy/Security for backup delay; Privacy/Legal + data owner + Security for external non-response; Legal/Privacy + audit owner for regulatory retention; service owner + Security (and Privacy if retention involved) for availability exception; Legal/Privacy + Security + product/data owner for provider retention. Operator/request handler cannot self-approve. I architect alone cannot accept legal/privacy risk.

Expired/revoked exception ceases to satisfy completion and forces Reopened. Unknown is not relabeled Confirmed.

## 12. Required scenario matrix

| ID | Scenario | Allowed state | Forbidden state | Accountable owners | Audit evidence |
|---|---|---|---|---|---|
| I-FGT-01 | Unknown Producer Domain exists | Reopened / Pending Unknown | Completed | I + discovered domain + D | Domain identity, epoch bump, seal invalidation, D barrier reconciliation |
| I-FGT-02 | Fence installed; lease unresolved | BarrierPending | Completed | D + work owner | Work/lease/attempt ID, terminal disposition, barrier proof |
| I-FGT-03 | Inventory changes during Forget | Reopened and resealed | Continue with old seal | I + affected owner | Old/new epoch, inventory diff, new seal |
| I-FGT-04 | H Adapter offline, Clear unconfirmed | Unknown/Pending or approved exception | Confirmed | H + I | Authenticated last-seen, timeout, retry and exception |
| I-FGT-05 | H UNSUPPORTED | Unknown or approved exception | Confirmed | H + I + approver | Capability profile, missing capability, alternative control, approval |
| I-FGT-06 | G Context Delivery Pending | TargetCleanupPending | Completed | G + H | Delivery/Context refs, pending state and reconciliation |
| I-FGT-07 | F watermark behind fence | TargetCleanupPending/Unknown | Confirmed runtime cleanup | F + I | Partition, watermark refs, lag and retry |
| I-FGT-08 | Backup restore contains forgotten target | BackupPending/Failed until quarantined | Visible serving state | Storage + I + D | Restore job, quarantine, ledger replay, suppression test |
| I-FGT-09 | External recipient no ACK | ExternalCopyPending/Unknown or exception | Confirmed | I + recipient owner | Request receipt, retry/escalation and exception |
| I-FGT-10 | PolicyException expires | Reopened | CompletedWithPolicyException | Approver + I + target owner | Expiry/revocation event and renewed proof |
| I-FGT-11 | Permission revocation concurrent with Forget | Deny stale authority; cleanup only under current service authority | Reuse stale ALLOW or merge epochs | I + D/E/F/G/H | Principal/issuer, PermissionEpoch, D fence, decision and race outcome |
| I-FGT-12 | New derivative target discovered after seal | Reopened | Retain old Completed as current | Discovering owner + I + D | Lineage, discovery time, epoch bump, superseded proof |

These are design tests, not executed tests. PASS requires reproducible fixture, test version/environment, expected and actual results, owner sign-off and non-sensitive evidence.

## 13. Completion hard stops

Completed is prohibited while any of the following holds:
- unknown producer/recipient domain or inventory gap;
- relevant inventory seal invalid or superseded;
- D barrier open, lease unresolved, producer registration gap or late derivative;
- missing/stale E/F/G/H evidence, incomplete partition watermark or pending delivery;
- H Adapter offline/Unknown/UNSUPPORTED without valid exception;
- external recipient lacks required ACK/exception;
- backup restore not quarantined or current Forget ledger not replayed;
- physical-erasure claim lacks exact system/media/key-scope proof;
- PolicyException expired/revoked;
- identity, issuer, ScopeRef or PermissionEpoch evidence cannot be verified.

## 14. Relationship to cross-module findings

- **CR-P1-05:** I-side target/evidence/ACK mapping is specified here as a candidate governance contract. D/E/F/G/H implementation evidence remains required.
- **CR-P0-02 / INT-P0-02:** identity semantics are clarified in the I identity contracts; B still owns ActorRef/ScopeRef types and H transport binding. Joint approval is OPEN.
- **INT-P0-03:** remains OPEN. D/E/Storage atomic registration/publication conformance and F/G/H target evidence are not proven by this policy document.
- **B Fact/Claim ADR:** remains ADR-BLOCKED. No schema decision is made here.

## 15. Non-claims

This contract does not prove deployed code, runtime suppression, physical media erasure, recipient compliance, backup expiry, restore safety or security test success. It does not define D's atomic fence implementation, E's scheduling, F's IndexWatermark, G's ContextVersion or H's wire/Adapter implementation.


---

## Phase 3.5 reconciliation addendum

The detailed I-owned identity and two-layer producer inventory mapping is historically described as normative candidate policy in `phase-3.5-global-identity-forget-governance.md` §§2–3 (unsubmitted and not restored; see [documentation gaps](../../governance/documentation-gaps.md)). The following clarifications apply to this inventory contract:

1. I's `ProducerDomainInventoryEpoch` covers the global catalogue of producer/recipient classes and instances. D's `ProducerRegistrationHighWater` / per-operation `WorkItemBarrier` covers concrete admitted work for one ForgetOperation. They are separate mandatory evidence references; neither substitutes for the other.
2. A target inventory entry is not valid merely because a payload or module reports its own ID. Issuer, Principal, instance, ScopeRef coverage and owner must be authenticated and resolved.
3. Required/optional/NotApplicable status is determined by an approved policy taxonomy and the sealed inventory. A target cannot be downgraded to optional after it fails or becomes Unknown. NotApplicable requires positive evidence of absence and independent review.
4. H ACK evidence must bind the authenticated Adapter identity and instance, capability epoch/profile, session-at-ACK, exact ScopeRef coverage, managed region/buffer/cache/queue, operation, target, D fence, action and integrity proof. Evidence validity is action-specific; no universal TTL is assumed.
5. `UNSUPPORTED` remains Unknown unless a valid independent PolicyException exists. It is not a successful clear or purge.
6. Global evaluation must explicitly include ProducerDomainInventoryEpoch, D barrier reference, late-derivative state, external recipient/onward-copy state, backup restore-control state and physical-erasure state. Missing mandatory evidence blocks Completed.
7. Any relevant inventory epoch change, late derivative/recipient/backup route, restore resurrection or expired exception invalidates the prior completion evaluation and requires Reopened/resealed evidence.

No new implementation or runtime test result is asserted by this addendum.
