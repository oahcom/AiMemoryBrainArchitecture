# Phase 3.6 — C/G/H Applied Contract Freeze Decision Package

- Owner: Session A — Principal Integration Architect
- Status: DECISION REQUEST ISSUED BY A; C/G/H APPROVALS NOT YET RECORDED
- Related plan: reviews/integration/phase-3.6-cross-owner-freeze-and-executable-closure-plan.md
- Scope: Applied Evidence, BMCP ACK/wire mapping, capability and reconnect semantics.
- Authority: C owns final-request evidence; G owns ContextVersion/Delivery/Applied; H owns BMCP wire/ACK/capability/session protocol; I owns authorization; D owns ForgetFence; B owns typed-reference semantics.

## 1. Decision requested

C, G and H are requested to review this exact package and record one explicit decision in their own authority-controlled branch:
- APPROVE — exact package version accepted with no unresolved normative issue in that owner's authority.
- APPROVE WITH ENUMERATED EXCEPTIONS — list exact clauses, replacement text, compatibility impact and closure condition.
- REJECT — identify the conflicting clause and provide a replacement proposal.
- CANDIDATE / NO APPROVAL — review incomplete; freeze remains blocked.

Silence, file presence, readback, A synthesis or another Owner's approval is not approval. A cannot sign for C/G/H. This package does not modify Owner files.

## 2. Owner artifacts read

| Owner | Artifact | Blob SHA | Disposition |
|---|---|---|---|
| C | 07-agent-integration/phase-3.6-final-request-evidence-contract.md | 8db1140f0dd19fe9267e3f2b44a9c1be75a6c32b | Producer semantics; cross-owner freeze blocked |
| G | 06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md | 8f6b215de7b78bf0eec2281359d3e039e7c8d5f4 | Applied authority; freeze blocked |
| H | 08-bmcp-protocol/adapter-forget-ack-and-target-binding.md | 5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8 | Candidate; subject to I/D/G/B approval |
| H | 08-bmcp-protocol/adapter-capability-and-applied-attestation.md | ed6b43a29aa368d772c701ffc83309a5aadf3c00 | Capability/attestation proposal |
| H | 08-bmcp-protocol/forget-revocation-and-reconnect.md | 695909360782987781e259187041618f495f1c8c | Candidate execution boundary; I/D dependencies open |
| H | 08-bmcp-protocol/phase-3-5-identity-applied-ack-reconnect-contract.md | fetched from H branch | Explicitly Candidate, not frozen wire schema |

These are artifact-level read observations, not a new common branch baseline. Embedded historical HEAD tables are not treated as current tips.

## 3. Canonical lifecycle proposed

| Stage | Authority | Evidence | Does not prove |
|---|---|---|---|
| Prepared | G | Immutable Context target/version and Delivery intent | Transport |
| Delivered | H | Authenticated receipt for exact DeliveryId and attempt | Materialization |
| Materialized | Adapter/H; consumed by C | Exact Managed Region, revision and digest | Final request inclusion |
| Final Request Submitted | C | Immutable post-transformation request crossed actual runtime/provider submit boundary | G Applied or execution start |
| Applied | G | G validates predicate and appends per-request Applied fact | Model attention, comprehension or use |
| Execution Started | Runtime/provider | Start receipt bound to InferenceRequestId | Completion or correctness |

Transport ACK, Forget ACK, Final Request Submitted evidence and G Applied are separate evidence families. H receipt does not prove final submission. C evidence does not mutate G state. G alone commits Applied. No claim may exceed demonstrated Adapter capability.

## 4. Canonical semantic field mapping proposed

| Semantic field | C producer | G authority | H representation | Owner/validation |
|---|---|---|---|---|
| Context identity/version | ContextId, ContextVersion | Immutable G target | ContextRef, opaque ContextVersion | G issues; B validates ref semantics where applicable |
| Delivery | DeliveryId, DeliveryAttemptId | Exact active attempt | DeliveryId, attempt ID | G issues; H authenticates receipt |
| Inference request | Actual InferenceRequestId | Same request ID | inference_request_id | Runtime assigns; C correlates; H cannot synthesize |
| Final submit boundary | FinalRequestBoundaryId and boundary type | Exact boundary ref | Evidence ref plus boundary claim | C defines; H encodes/verifies |
| Agent/Adapter/runtime/session | Authenticated principals, refs, instances and session | Same binding | Authenticated Agent/Adapter/Runtime/Session tuple | I trust; B typed refs; H session binding |
| Principal/Issuer/Actor | Protected authenticated binding | Authoritative identity refs | Principal, Issuer, ActorRef | I trust; B types; H transport binding |
| Scope/Environment | ScopeRef, required EnvironmentRef | Exact authorized refs | Typed ScopeRef/EnvironmentRef | B semantics; I authorization |
| Managed region | Region ID, revision, inventory | Exact expected target | ManagedRegionRef, revision, inventory version | H/Adapter boundary; G target expectation |
| Content integrity | Complete region digest and algorithm/version | Exact digest equality | managed_region_digest + canonicalization profile | C measures final request; H integrity envelope |
| Authorization | PermissionDecision ref + PermissionEpoch | Current I decision/epoch | permission_epoch + decision ref | I issues and validates |
| Forget authority | ForgetFenceGeneration/Cursor + lineage | Current D fence for all lineage | Opaque D fence + operation/lineage refs | D issues and validates |
| Capability | AdapterCapabilityEpoch + profile | Current epoch and evidence tier | Capability set + capability_epoch | H negotiates/issues |
| C submission evidence | Immutable evidence ID, issuer, digest | Evidence ref and verification | final_request_evidence_ref + integrity envelope | C issues; H transports/verifies |
| H delivery proof | H receipt ref | Required H receipt | ACK ID/status/integrity/correlation | H owns |
| G Applied receipt | Not produced by C | Immutable Applied record ID | Optional G-defined response | G owns |
| Execution start | Runtime/provider receipt | Separate lifecycle evidence | Separate event/receipt | Runtime/provider authority |

PermissionEpoch, ForgetFenceGeneration, ContextVersion, CapabilityEpoch, DeliveryAttemptId and RuntimeSession are distinct typed namespaces. They must never be numerically compared, substituted or copied across fields.

## 5. H wire decisions required

H must provide a concrete versioned schema, not prose alone:
1. Message families and schema IDs for Delivery receipt, Materialization evidence, Final Request Submitted evidence transport, Applied result/receipt and Execution Started.
2. Exact separate enums for Forget action ACKs and Applied evidence dispositions. Forget statuses SUPPRESSED, LOCAL_BUFFER_CLEARED, LOCAL_CACHE_PURGED, QUEUED_DELIVERY_CANCELLED, FAILED, UNKNOWN and UNSUPPORTED cannot be reused as Applied statuses.
3. Exact authenticated identity tuple: Principal, Issuer, ActorRef, Agent, Adapter instance, Runtime instance, Session, ScopeRef, EnvironmentRef and ManagedRegion.
4. Opaque token encodings and owner validation APIs for ContextVersion, PermissionEpoch, ForgetFenceGeneration and CapabilityEpoch.
5. Integrity/signature/MAC profile, issuer/key ID, key rotation, audience, expiry, replay nonce/sequence, canonicalization and digest profile.
6. Duplicate, same-ID/different-digest conflict, retry, out-of-order, late ACK, old session, replaced Adapter and reconnect semantics.
7. Capability negotiation schema and epoch-bump conditions, including build, final-submit hook, region isolation, digest profile and coverage inventory changes.
8. Unknown field/enum, schema downgrade, stale key and incomparable-token fail-closed behavior.
9. Durable evidence journal and ACK replay semantics; transport delivery is not action completion.
10. Explicit evidence ceiling where actual immutable final request and successful submit are not observable.

H's candidate Forget ACK proposal is action-scoped; it does not by itself freeze the Applied evidence wire family.

## 6. C decisions required

C must confirm the exact final immutable request and successful submit boundary per integration tier; runtime/provider InferenceRequestId assignment and uniqueness domain; FinalRequestBoundaryId and causal binding to delivery/materialization; complete digest coverage and canonicalization; truncation/omission/bypass detection; authenticated source of all identity/session/scope fields; evidence immutability and correction/supersession; Tier 2/3 evidence ceiling; and the exact versioned schema consumed by H/G.

## 7. G decisions required

G must confirm per-request/attempt/session Applied identity (not scalar applied_version); full acceptance predicate; G commit point and idempotency key; historical Applied versus current-use projection; late evidence after Forget/revocation; pre-submit invalidation and ambiguous ordering; supersession/duplicate/altered-digest/old-session outcomes; required H evidence fields versus transport metadata; and whether a historically valid Applied fact can be recorded after later invalidation while immediately being non-current for use.

## 8. Mandatory temporal decision

C/G currently require authority to be current at the submission boundary, while G may receive evidence later. The joint contract must separate:
- Historical submission fact: did the exact request cross the submit boundary before or after ForgetFence/PermissionEpoch transition?
- Current-use eligibility: is the historical Applied context still eligible now?

| Ordering | Historical result | G record | Current-use |
|---|---|---|---|
| Submit precedes Forget/revocation | Valid if all predicates and ordering proof pass | May append historical Applied even if evidence arrives later | Invalidated after transition |
| Forget/revocation precedes submit | Stale/ineligible | Reject Full; retain rejection/audit evidence | Suppressed |
| Ordering ambiguous | Unknown | No Full promotion | Suppressed |
| Valid submit then session/capability replacement | Historical fact remains bound to old session/epoch | Never rebind | New session requires fresh evidence |
| Valid submit then Context supersession | Historical fact remains for old target | Cannot become current pointer | Old target non-serving |

Independent wall-clock timestamps are insufficient. Require a trusted monotonic sequence, shared serialization/authority receipt or another explicitly approved causal proof. Otherwise Unknown and suppress.

## 9. Proposed Full Applied predicate

G may append historical Full Applied only when all are true:
1. Exact ContextId, ContextVersion, DeliveryId and attempt match a G-issued target.
2. Actual InferenceRequestId and FinalRequestBoundaryId bind the exact request.
3. Agent, Adapter, Runtime and Session are authenticated and mutually bound to C/H evidence.
4. Principal/Issuer/ActorRef, ScopeRef and required EnvironmentRef are typed, trusted and authorized under I/B.
5. ManagedRegion identity/revision/inventory matches the delivered target.
6. Complete region digest and canonicalization profile match the region in the submitted request.
7. C evidence is immutable, integrity-valid, non-replayed and within demonstrated capability.
8. H delivery/identity/capability evidence is valid for exact attempt/session.
9. I PermissionDecision/PermissionEpoch and D ForgetFence/lineage ordering are proven at submission boundary.
10. No pre-submit supersession, revocation, fence, scope/environment change, session replacement or capability downgrade invalidated the request.
11. Coverage is complete; no unknown bypass, truncation, omission or lineage gap exists.

G must separately recompute current-use eligibility against current Context head, I permission, D fence, scope, session and capability. Later invalidation cannot rewrite historical truth or leave old content eligible.

## 10. Conformance package — specified, not run

| ID | Scenario | Required assertion |
|---|---|---|
| CGH-01 | Complete Tier 1 flow | G accepts Full only after C/H/I/D predicates |
| CGH-02 | Materialized, no final submit | Materialized only; no Applied |
| CGH-03 | Submitted, no G commit | FinalRequestSubmitted only |
| CGH-04 | Submit before Forget; evidence arrives after | Preserve historical fact if ordering proven; current-use invalid |
| CGH-05 | Forget before submit | Reject Full; suppress |
| CGH-06 | Submit/fence order unprovable | Unknown; no Full; suppress |
| CGH-07 | Permission epoch changes before submit | Block/Unknown; no stale Full |
| CGH-08 | Permission epoch changes after submit before acceptance | Historical/current-use split follows approved rule |
| CGH-09 | Capability epoch changes after submit | Preserve old-epoch history; no rebinding |
| CGH-10 | Tier downgrade or submit-hook bypass | Partial/Unknown/Unsupported; never Full |
| CGH-11 | Duplicate same digest | Idempotent exact prior disposition |
| CGH-12 | Same identity, changed digest | Conflict/quarantine; no last-write-wins |
| CGH-13 | Old Session ACK after reconnect | Historical only or rejected; never rebound |
| CGH-14 | Context superseded before submit | Reject current Full |
| CGH-15 | Unknown schema/enum/key/issuer or stale key | Fail closed |
| CGH-16 | Cross-Scope or wrong Environment | Reject before materialization/submission |
| CGH-17 | Truncated/partial managed region | Partial; no Full |
| CGH-18 | Memory attempts privileged instruction/tool injection | Untrusted data; no policy/tool authority |
| CGH-19 | Forget ACK presented as Applied proof | Reject category mismatch |
| CGH-20 | Transport ACK presented as submit proof | Reject category mismatch |

Required evidence: schema versions, stable typed IDs, issuer/key refs, controlled operation order, C evidence, H ACK, G validation/Applied record, D/I authority receipts, build identity, raw logs and reproducible runner.

## 11. Explicit approval ledger

| Owner | Decision | Exact artifact/version | Exceptions | Approver evidence |
|---|---|---|---|---|
| C | PENDING | PENDING | PENDING | PENDING |
| G | PENDING | PENDING | PENDING | PENDING |
| H | PENDING | PENDING | PENDING | PENDING |
| I — predicate confirmation | PENDING | PENDING | PENDING | PENDING |
| D — fence ordering confirmation | PENDING | PENDING | PENDING | PENDING |
| B — typed reference confirmation | PENDING | PENDING | PENDING | PENDING |

## 12. A integration decision and stop conditions

A proposes the lifecycle in §3, field mapping in §4, separate evidence families, and the historical/current-use split in §8. This is an integration proposal, not an Owner decision.

Applied Contract Frozen remains NO until C/G/H explicitly approve the same version and D/I/B confirm their authority predicates. Test Executed, Test Passed and Implementation Verified remain NO until reproducible evidence exists.

Stop and retain BLOCKED if any required owner has not approved; a field lacks a named authority; ordering relies only on incomparable wall clocks; evidence tier exceeds observability; ACK categories are conflated; or test/implementation claims lack raw evidence.

## 13. Next actions

1. C reviews lifecycle, field mapping, temporal rule and producer evidence schema.
2. G reviews Applied predicate, historical/current-use semantics and commit/idempotency behavior.
3. H supplies concrete versioned wire schema, integrity, replay, capability and reconnect mapping.
4. I confirms PermissionDecision/PermissionEpoch currentness, issuer/key trust and revocation ordering.
5. D confirms ForgetFence token semantics, lineage coverage and authoritative ordering proof.
6. B confirms typed ActorRef/ScopeRef/EnvironmentRef mapping and namespace rules.
7. A re-reads Owner decisions, records exact blob SHAs, resolves discrepancies and updates the integration finding.

No Owner branch is modified by this package. No approval is implied. No branch merge is authorized.

---

## 14. Live Owner evidence reconciliation — 2026-11-16

This addendum updates the evidence table without changing A's authority boundary or granting approval by implication.

### Exact Owner readbacks

| Owner | Current artifact Blob | Evidence-backed disposition | Still required |
|---|---|---|---|
| C | `07-agent-integration/phase-3.6-final-request-evidence-contract.md` — `45cab0f9c538fa653ac9e3ca8ddba3dee1b8383b` | C semantic portion accepted with enumerated exceptions; C/G/H freeze remains BLOCKED | Explicit C approval/rejection of this exact A package and the exact common Applied schema version |
| G | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` — `6513932991fdbe13231b26e43440fc2c4fcbf7fa` | G semantic portion accepted with exceptions; G remains sole Applied authority; C/G/H freeze remains BLOCKED | Explicit G approval/rejection of this exact A package and exact common schema/predicate |
| H | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` — `9845c97ac43d7888732afafe12e28850ec02add8` | H BIH technical baseline decided; H accepted exact A BIH package in issue #6 comment 6919218061 | Concrete versioned Applied/Delivery/ACK wire schema; explicit H decision on this C/G/H Applied package |
| B | Formal typed mapping Blob `729a706860b1259115816265e847a29683c3c233` (issue #3 comment 6919299226) | B approves B-owned ActorRef/ScopeRef/EnvironmentRef semantic mapping | Consumer field-path mapping remains C/G/H; no wire approval implied |
| I | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` — `0cbf6bb7480db873790c454817593a9b1c5548ba` | BIH technical policy design decided; I36-GOV-01..10 remain governance blocked | Explicit predicate confirmation for this exact Applied schema and external governance approvals |
| D | Current D owner fence contract and JF-10 common protocol | D owns fence/lineage semantics; no A-package decision recorded in this package ledger | Explicit exact-version fence/order confirmation for the Applied submission boundary |

### Coordination trail

- Issue #3 updated with exact current refs and per-owner remaining decisions; A comment `6919370891`.
- Issue #6 updated with C/F/G current refs and BIH consumer acceptance request; A comment `6919372132`.
- B's formal type mapping and H's exact BIH package acceptance are separate decisions; neither freezes the C/G/H wire contract.

### Current freeze disposition

**Applied Contract Frozen = NO.** C and G have accepted their own semantic portions with exceptions, but neither has approved the exact common package/schema. H's exact BIH package acceptance is not a versioned Applied wire schema decision. B's typed mapping is confirmed. I/D confirmations and explicit C/G/H package decisions remain outstanding. No tests executed or implementation verified by this addendum.
