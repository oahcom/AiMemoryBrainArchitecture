---
document_metadata:
  domain: agent-integration
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "Owner-delegated direction decision, 2026-11-26"
        - "Work Item AID-2026-088"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Direction decision recorded; exact-version Owner acceptance and normative approval pending."
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
    canonical_status: Candidate
    canonical_scope: "agent-integration decision contract"
    canonical_scope_id: "agent-integration/decision-085"
    canonical_scope_keywords:
      - architecture-decision
      - agent-integration
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: "docs/en/07-agent-integration/applied-evidence-contract.md"
    zh-CN: "docs/zh-CN/07-agent-integration/applied-evidence-contract.md"
---
# C/G Applied Evidence Contract
Decision ID: APPLIED-EVIDENCE-01
Authority: user-authorized operator (delegated by account owner)
Date: 2026-11-26
Owners: C (inference-boundary attestation), G (delivery projection), H (protocol/adapter receipt)
Issues: #1124, #1135, #1180
Status: Direction decided; exact-version C/G/H acceptance pending.

## State ownership and projection
C/H own evidence of what the Adapter actually did at the inference boundary. G owns desired ContextVersion and the G DeliveryIntent/Delivery projection. G must not manufacture Applied from local persistence.

Mapping:
- G Prepared: durable DeliveryIntent exists for an exact ContextVersion.
- G Delivered: payload handoff/transport receipt exists; this does not imply C/H Accepted or Applied.
- C/H Received: Adapter instance received payload; G may store receipt metadata, never Applied.
- C/H Accepted: Adapter validated and accepted payload for application. G retains this as distinct attempt metadata; no additional G lifecycle state is required.
- G Applied: allowed only after G verifies a valid C/H AppliedAttestation for the exact DeliveryAttempt and ContextVersion at the final inference boundary.
- Rejected/Expired/Superseded remain distinct. Timeout/lost ACK is Unknown/Pending, never Applied and not an inferred rejection.

Delivery ID identifies the logical delivery; DeliveryAttempt ID identifies one concrete attempt. Retry creates a new Attempt ID under the same Delivery ID. Supersession creates a new logical Delivery ID or explicit successor relation. Attempt evidence is never overwritten.

## Minimum immutable AppliedAttestation record
~~~yaml
evidence_schema: "applied-attestation/v1"
attestation_id: "<stable unique ID>"
delivery_id: "<logical delivery ID>"
delivery_attempt_id: "<unique attempt ID>"
context_id: "<Context ID>"
context_session_id: "<Context Session ID>"
context_version_id: "<immutable ContextVersion ID>"
context_version_sequence: 42
snapshot_digest:
  algorithm_profile: "<approved canonical digest profile>"
  value: "<digest of exact canonical ordered snapshot bytes>"
managed_region_id: "<managed region identifier>"
managed_region_digest:
  algorithm_profile: "<approved digest profile>"
  value: "<digest of effective managed-region contents>"
agent_instance_id: "<Agent instance>"
adapter_id: "<Adapter>"
adapter_instance_id: "<Adapter instance>"
inference_boundary_id: "<final inference boundary>"
inference_request_id: "<specific inference request>"
applied_at: "<UTC timestamp>"
issuer:
  principal_id: "<authenticated issuer>"
  key_id: "<verification key reference>"
  signature: "<signature or immutable verifier receipt reference>"
verification:
  result: "VERIFIED"
  verifier_id: "<verifier identity>"
  verified_at: "<UTC timestamp>"
~~~

The exact cryptographic algorithm, key lifecycle and transport encoding remain subject to I/H security and protocol specifications. Until those profiles are pinned and independently verifiable, evidence is CANDIDATE and cannot be treated as verified Applied proof. The attestation binds all identity fields to the DeliveryIntent/Attempt and binds both digests to the exact ContextVersion and actual managed inference region. Numeric version alone is insufficient.

## Evidence authority and location
- C/H produce and retain the immutable attestation at the Adapter/inference-boundary evidence source.
- G durably stores an immutable reference and verification outcome in its DeliveryAttempt ledger keyed by (Delivery ID, Attempt ID); G Applied is a projection of verified evidence.
- Attestation digest and issuer/verifier references are retained for audit/replay. G may cache the projection but is not the source of inference truth.
- H transport ACK/receipt and C Adapter Accepted are separate records and cannot be relabeled Applied.
- Local file write, in-memory update, snapshot persistence or Adapter-side storage proves only Stored/Materialized (and possibly Received), never final inference-boundary Applied.

## Verification rules
Before projecting Applied, G verifies: Delivery ID and Attempt ID; Context ID/Session/immutable Version ID/sequence; snapshot digest; Agent/Adapter/instance identities; final boundary and inference request; managed-region ID/digest against actual contents; issuer authenticity/signature or verifier receipt under a pinned security profile; and non-stale status against current Context head, attempt, supersession and Forget/revocation state.

Missing, malformed, mismatched, unverifiable or stale evidence yields Unknown/Rejected according to failure class, never Applied. Historical evidence remains immutable; current-use validity is recomputed.

## Reviewer PASS/FAIL
- AP-01 PASS iff Applied requires C/H attestation from final inference boundary; else FAIL.
- AP-02 PASS iff attestation binds logical Delivery ID and unique Attempt ID; else FAIL.
- AP-03 PASS iff Context/session/immutable Version ID+sequence/snapshot digest match DeliveryIntent; else FAIL.
- AP-04 PASS iff Agent/Adapter/instance/boundary/request identities are bound and validated; else FAIL.
- AP-05 PASS iff managed-region identity and digest are included and verified against actual contents; else FAIL.
- AP-06 PASS iff issuer authenticity and verifier evidence are independently checkable under a pinned security profile; else FAIL.
- AP-07 PASS iff local persistence/materialization/receipt cannot be reported as Applied; else FAIL.
- AP-08 PASS iff Received and Accepted remain distinct from G Delivered and Applied, with Accepted retained as attempt metadata; else FAIL.
- AP-09 PASS iff Unknown/lost ACK stays pending/unknown and retries use distinct Attempt IDs; else FAIL.
- AP-10 PASS iff G Applied is only a projection/reference to immutable C/H evidence and current-use validity is invalidated by supersession/Forget/revocation; else FAIL.
- AP-11 PASS iff EN/ZH-CN mirrors are semantically equivalent; else FAIL.
- AP-12 PASS iff comments exist on #1124/#1135/#1180 and all remain OPEN; else FAIL.

## Authority boundary
C owns inference-boundary truth; H owns protocol transport/receipt; G owns desired Context and delivery projection; I owns identity/trust/key policy; D owns ForgetFence authority. This decision does not add a G lifecycle state, define BMCP wire values, select a cryptographic algorithm or authorize implementation. #1124, #1135 and #1180 remain OPEN until their criteria and required Owner acceptance are satisfied. No runtime/product code, tests, schemas, validators, workflows, deployment or production state is changed.
