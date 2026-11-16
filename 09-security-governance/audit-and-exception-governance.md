# Audit and Exception Governance

- Owner: Session I
- Status: **CANDIDATE governance policy; legal/privacy approval and operational controls OPEN**
- Related: INT-P0-03, INT-P0-04, INT-X-02, INT-X-07, CT-020.

## 1. Audit objectives

Audit must establish who acted, under what authenticated authority, on which policy/scope generation, what decision was made, which workflow/target states changed and what evidence supports the claim. It must not preserve the content that a Forget operation is intended to remove.

Audit is not a shadow Memory database. Audit records are minimized control-plane evidence, not a source for restoring Memory, reconstructing prompts, re-creating embeddings or inferring forgotten propositions.

## 2. Auditable event classes

- authentication success/failure, issuer/key rotation and credential revocation;
- delegation grant, use, expiry, revocation and break-glass;
- policy decision, denial, indeterminate result and permission epoch advancement;
- Scope binding changes and environment registration changes;
- Accepted receipt and idempotency conflict metadata;
- canonical commit/lifecycle authorization result (D owns canonical lifecycle event);
- Forget request, authorization, suppression fence, target inventory, barrier/watermark, each target attempt/result and completion evaluation;
- legal hold/retention exception approval, review, expiry and release;
- backup creation/restore/expiry/crypto-erasure evidence;
- external recipient notification and acknowledgement;
- Adapter clear/reconnect and Applied attestation metadata;
- security test result, incident, remediation and risk acceptance.

## 3. Non-reconstructive tombstone

### 3.1 Required shape

A tombstone is a minimal control-plane record. Candidate fields:

```text
NonReconstructiveTombstone {
  tombstone_id: random opaque non-semantic ID
  forget_operation_id: opaque workflow reference
  target_class: coarse registered category
  scope_partition_token: non-reversible, access-controlled partition token
  suppression_fence: typed generation reference
  state: Suppressed | CleanupPending | ErasurePending | Exception
  created_at: timestamp
  policy_version: policy reference
  target_status_summary: aggregate counts only
  exception_ref?: opaque approval reference
}
```

It MUST NOT contain:
- forgotten text, source excerpts, prompts, user messages, labels or entity names;
- original object IDs if those IDs or their retained metadata reveal the forgotten subject/content;
- raw content digests, hashes of low-entropy content, embeddings, summaries or provenance edges that permit matching/reconstruction;
- plaintext external URLs, file paths, email addresses, credentials or personal identifiers;
- a copy of the source payload “for audit”.

A digest is not automatically non-reconstructive. Low-entropy content can be dictionary-attacked; stable digests can correlate data across systems. If correlation is required, use random opaque IDs or a keyed token whose key is access-restricted, rotated and separately governed. Do not treat keyed token as proof of deletion.

### 3.2 Separation and access

Tombstones live in a minimal control plane separate from content indexes and retrieval. They are never returned as candidate Memory or Evidence. Only Forget orchestrators, authorized auditors and approved Legal/Privacy roles may query them. Query results reveal only the minimum state required.

A tombstone blocks resurrection; it does not prove content was erased. It must survive backup restore long enough to reapply suppression, but retention of the tombstone itself is separately bounded and justified.

## 4. Audit data minimization and retention

Audit events record:
- event type, random event ID, time and ordering;
- authenticated actor/issuer reference under restricted access;
- action/resource class, decision ID, policy version and permission epoch;
- scope partition token and coarse target category;
- ForgetOperation ID, fence, target class and state transition;
- acknowledgement evidence reference, watermark and verifier identity;
- exception approval reference, reason category and expiry.

Do not log payload bodies, retrieved text, prompt contents, Evidence snippets, raw model output, secrets, credentials or complete object labels. Avoid free-text reason fields; use controlled reason codes and separately protected case references.

Retention is purpose-based and classed:
- security/authentication records: minimum period required for incident investigation and legal compliance;
- authorization/delegation records: period required to prove grant/revocation and investigate misuse;
- Forget evidence: period needed to prove suppression/cleanup/exception and satisfy applicable legal obligations;
- operational traces: shortest useful debugging window, with aggregation/anonymization thereafter.

Exact periods and jurisdictions remain **OPEN** pending Privacy/Legal and deployment data map. Do not invent a universal retention duration. When audit retention conflicts with data-subject erasure, retain only the minimum non-reconstructive evidence under documented legal basis; remove or irreversibly de-link any content-bearing attributes.

## 5. Forget and audit interaction

1. At Forget approval, create a minimal audit event and non-reconstructive tombstone.
2. Do not copy target payload into the audit event or exception ticket.
3. Keep a restricted mapping from operation ID to required target inventory only as long as necessary to execute and prove the workflow; minimize or erase the mapping after obligations expire.
4. Store target-specific evidence as a pointer to a signed, bounded attestation or provider receipt, not a copy of the deleted content.
5. If the attestation itself contains source content or reconstructable digests, redact/minimize it before audit retention.
6. Tombstone retention is independent from Memory lifecycle and physical erasure.
7. Backup restore must restore the suppression control plane first; the tombstone is not a source of content restoration.
8. When all obligations end, expire tombstones/mappings under the approved retention schedule. Retaining an eternal stable identifier is not the default.

## 6. Exception governance

A PolicyException is a narrowly scoped authorization to retain a residual target or accept an unconfirmed target for a declared purpose. It is not a way to relabel Unknown as Confirmed.

Required exception record:
- exception ID and linked ForgetOperation;
- exact target class/scope and residual data category;
- reason code and legal/policy basis;
- what cannot be completed and why;
- approving authority and independent reviewer;
- creation time, expiry/review date and revocation condition;
- access restrictions, encryption, isolation and compensating controls;
- user-facing disclosure requirement;
- evidence that ordinary retrieval, Context delivery, training/export and derivation remain blocked.

### 6.1 Approval matrix

| Exception class | Required approver(s) | Cannot approve alone |
|---|---|---|
| Legal hold | authorized Legal + Privacy/Data Protection + data owner | operator/request handler |
| Backup rotation delay | storage owner + Privacy/Security policy owner | backup job operator |
| External recipient non-response | Privacy/Legal + data owner + Security | integration operator |
| Regulatory minimum audit retention | Legal/Privacy + audit owner | I architect alone |
| Operational availability exception | service owner + Security; Privacy if data retention involved | on-call engineer alone |
| Model provider retention | Legal/Privacy + Security + product/data owner under provider terms | Adapter owner alone |

Approvals must be independent of the operator whose work is being excepted. The I architect can define policy and record a recommendation but cannot unilaterally accept legal, privacy or cross-tenant security risk.

### 6.2 Exception lifecycle

`Proposed → Reviewed → Approved → Active → Expired | Revoked | Superseded`

Unapproved or expired exceptions have no effect. Every exception is scoped, time-limited and reviewed. An expired exception reopens the target as Pending/Unknown and blocks completion until resolved.

## 7. Risk acceptance and escalation

Non-acceptable before release: cross-tenant data disclosure, forged identity accepted, missing revocation check at protected boundary, Forget resurrection after completion, false claim of physical erasure, or audit content that reconstructs forgotten data.

Residual model prompt-injection risk requires acceptance by Agent/product security authority with independent tool/action authorization, monitoring and response procedures. External recipient/backup residuals require Privacy/Legal and data-owner approval. Availability trade-offs may be accepted by the service owner only within a declared data classification and bounded staleness profile.

All accepted risks have an owner, impact, likelihood rationale, mitigations, expiry/review date, affected release and rollback/exit criteria. “Accepted” never means “technically eliminated”.

## 8. Evidence and audit verification

A completion evidence bundle contains:
- ForgetOperation and fence references;
- sealed target inventory version;
- producer registration epoch/barrier proof;
- typed E/F/G/H/storage watermarks and target-specific statuses;
- signed/verified acknowledgements and verifier identity;
- exception approvals, expiry and disclosure status;
- separate suppression, cleanup and physical-erasure conclusions;
- audit minimization result and test version.

It excludes forgotten payload and reconstructive digests. Auditors verify evidence authenticity, binding and completeness, not content by retrieving the forgotten object.

## 9. Open dependencies

- Privacy/Legal must define jurisdiction-specific retention and lawful-basis schedules.
- Storage must define backup media lifecycle, restore quarantine and erasure evidence.
- D/E/F/G/H must expose target-specific acknowledgements and typed watermarks.
- A must register the shared issue states and cross-module evidence format.
- External recipients and model providers must disclose their deletion/retention capabilities; unsupported claims remain Unknown or PolicyException.

---

## Phase 3 targeted remediation — exception and completion evidence controls

A PolicyException used by Global Forget MUST satisfy all of the following:
1. Exact ForgetOperationId, TargetId(s), target class, ScopeRef coverage and residual data class are bound. Broad wildcard exceptions are invalid.
2. The exception identifies the specific unmet action/evidence, why it cannot be completed, legal/policy basis and compensating controls.
3. Approval is by the authority appropriate to the exception class in the matrix above, with an independent reviewer. The target operator and request handler cannot approve their own failure.
4. The record has an effective time, hard expiry, review date, revocation condition, risk owner and user-disclosure obligation. No perpetual exception by default.
5. The exception cannot authorize ordinary retrieval, derivation, Context delivery, Adapter application, training or export of forgotten content. It only governs the explicitly described residual retention/copy.
6. Evidence includes signed approval, policy version, target evidence, risk assessment, controls and audit correlation. I records the decision but does not self-approve legal/privacy risk.

At expiry, the exception ceases to satisfy completion automatically. The target becomes Pending/Unknown, the global operation is Reopened, and any prior CompletedWithPolicyException result is superseded until fresh evidence or a newly approved exception exists.

Global completion audit bundle must separately reference the I ProducerDomainInventoryEpoch/Target Inventory Seal and D ProducerRegistrationHighWater/Work-item Barrier. Audit must not store their values in one untyped "epoch" field. H ACK evidence is retained per Adapter target and per capability action; a roll-up count without enumerated coverage is insufficient.

A completion evaluator records the vector component states (suppression, producer barrier, derived cleanup, runtime/context/adapter, external copy, backup/restore, physical erasure), exact mandatory target set, exceptions and expiry, evidence verifier, evaluation time and policy version. Any newly discovered target, invalidated seal, late derivative, failed restore suppression or expired exception produces an auditable Reopened transition. The previous proof remains as historical/superseded evidence and is never silently overwritten.

