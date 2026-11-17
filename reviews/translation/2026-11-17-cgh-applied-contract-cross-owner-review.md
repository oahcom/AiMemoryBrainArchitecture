# C/G/H Phase 3.6 Applied Contract Cross-Owner Review

- Review date: 2026-11-17
- Review scope: C Final Request Evidence, G Applied/Forget/Reconciliation, H Adapter Capability/Applied Attestation
- Review mode: independent source-to-source semantic and field-level review
- Non-goal: this is not Owner approval, wire freeze, implementation verification, conformance execution, or production acceptance.

## 1. Exact source baseline

| Owner | Source path | Branch | Exact source Blob SHA | Source disposition |
|---|---|---|---|---|
| C | `07-agent-integration/phase-3.6-final-request-evidence-contract.md` | `session-c-agent-integration-2026-11-16` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` | C semantic decisions recorded; C/G/H freeze BLOCKED; implementation/execution NOT VERIFIED |
| G | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `session-g-memory-context` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | G semantic decisions recorded; C/G/H freeze BLOCKED; implementation/execution NOT VERIFIED |
| H | `08-bmcp-protocol/adapter-capability-and-applied-attestation.md` | `session-h-bmcp-protocol` | `ed6b43a29aa368d772c701ffc83309a5aadf3c00` | CANDIDATE; final-request proof profile OPEN with C; authorization binding OPEN with I |

Blob SHAs are exact file identities, not branch HEADs, approval signals, or implementation evidence.

## 2. Cross-owner semantic alignment

### 2.1 Six-stage lifecycle — ALIGNED

All three contracts preserve the same distinct lifecycle:

`Prepared → Delivered → Materialized → Final Request Submitted → Applied → Execution Started`

- C produces immutable per-request Final Request Submitted evidence only after the exact post-transformation request crosses the observed successful runtime/provider submit boundary.
- H capability tier determines what the Adapter can observe. Tier 2/3, bypassed or unknown coverage cannot claim Full.
- G alone validates the complete predicate and commits the authoritative per-request Applied record.
- Execution Started requires a separate runtime/provider receipt correlated to the same InferenceRequestId.

No contract permits transport receipt, materialization, submission, Applied, and execution-start to be collapsed. Applied does not prove model attention, understanding, recall, behavioral use, correctness, or successful completion.

### 2.2 Historical truth and current-use — ALIGNED

C and G agree that a historically valid submission/Applied fact is append-only. A later Forget, revocation, scope/session/capability change invalidates current-use eligibility but does not rewrite the historical fact. If Forget/revocation linearizes before submission, Full Applied is rejected. If ordering is unprovable, the result is Unknown and affected content remains suppressed.

H's capability epoch rule is compatible: prior attestations remain tied to the epoch that produced them; downgrade does not rewrite history but prevents future Full claims.

### 2.3 Duplicate and late evidence — ALIGNED AT SEMANTIC LEVEL

C and G require exact identity+digest replay to be idempotent and same identity with changed digest to become conflict/quarantine. Late ACK/evidence cannot roll back a newer ContextVersion/Delivery attempt or be rebound across Adapter instance, Runtime Session, or CapabilityEpoch. H requires immutable attestation and capability-epoch binding, but its candidate field model does not yet define the complete common identity tuple or replay-journal wire mapping.

### 2.4 Forget boundary — ALIGNED, H FIELD MAPPING INCOMPLETE

G owns Applied and current-use invalidation; D owns ForgetFence; I owns authorization/PermissionEpoch; H owns protocol/ACK/capability; C owns final-request evidence. Forget ACK and Applied Attestation are distinct evidence families. Context Remove is not Canonical Forget. G's reconnect sequence reauthenticates and revalidates I/D/G/H authority before any old Snapshot/Delta can be restored.

## 3. H candidate field-level gaps against C/G

The H source is explicitly CANDIDATE and says the final-request proof profile is OPEN with C. The following are mapping gaps, not permission to invent wire fields in a translation:

| Finding | H candidate state | C/G required binding | Required disposition |
|---|---|---|---|
| H36-AP-01 — boundary identity | H has `inference_request_id` and generic `final_request_evidence`; no explicit `FinalRequestBoundaryId` or boundary type in the candidate table | C requires actual runtime-assigned InferenceRequestId plus exact FinalRequestBoundaryId/boundary type; G requires both request and boundary identity | H must publish/accept an exact mapping; OPEN |
| H36-AP-02 — target identity | H uses `context_ref / target_context_version`, `delivery_id / attempt_id`, and `applied_context_version` | C/G require ContextId, exact ContextVersion, DeliveryId and DeliveryAttemptId, with attempt non-superseded | Define canonical field mapping and distinguish target version from actually materialized version; OPEN |
| H36-AP-03 — managed-region completeness | H requires `managed_region_digest` and `digest_profile` | C/G require exact region identity, inventory/revision, complete coverage and digest of the region actually embedded in the submitted request | Add or normatively reference inventory/revision/coverage evidence; digest alone is insufficient; OPEN |
| H36-AP-04 — authority vector | H table leaves `permission_epoch` I-defined and `forget_fence` D/I-defined | C/G require current PermissionEpoch + authorization decision and D ForgetFenceGeneration/Cursor + lineage validation at final submit | Preserve owner-issued typed references and define exact H transport binding without H minting authority; OPEN |
| H36-AP-05 — authenticated identity | H lists `authenticated_transport_principal_ref` and explicitly says it is not payload-authenticated; Agent/session refs are conditional/C-defined | C/G require verifier-resolved Agent/Adapter/Runtime/Session identities and protected bindings, not payload claims | Clarify protected verifier context and exact issuer/instance/session binding; OPEN |
| H36-AP-06 — evidence provenance | H has `created_at`, `integrity`, and candidate submission evidence | C additionally requires evidence issuer, boundary timestamp/monotonic sequence where available, schema version, correlation/causation and audit reference | H/C must define required versus conditional provenance fields and integrity profile; OPEN |
| H36-AP-07 — tier semantics | H Tier 1/2/3 broadly matches C capability ceilings | C also treats bypass/unknown request paths and exact omitted/unobservable coverage as non-Full | Ensure per-request coverage and bypass enumeration are part of the accepted evidence, not only Adapter capability declaration; OPEN |

These are material blockers to an exact field-level C/H/G binding. The H candidate must not be silently upgraded by its English/Chinese companion.

## 4. Owner authority boundaries — PRESERVED

- C: sole producer of final-request submission evidence; does not mutate Applied.
- G: sole authority for Context Applied state and current-use projection.
- H: protocol schema, ACK/capability negotiation, evidence encoding and validation; does not decide Applied or mint I/D authority.
- I: Principal/Actor authorization, PermissionEpoch, revocation and security/integrity policy.
- D: ForgetOperation, ForgetFence, lineage coverage and ordering.
- B: typed Actor/Scope/Environment references.
- Runtime/provider: actual request identity, successful submit boundary and separate execution-start receipt.

No cross-owner acceptance is inferred from another Owner's decision.

## 5. Findings and disposition

- **PASS — lifecycle semantics:** six-stage separation and non-claims align.
- **PASS — historical/current-use semantics:** later invalidation preserves history and blocks reuse.
- **PASS — duplicate/late evidence semantics:** C/G semantic rules align; H wire replay identity remains OPEN.
- **BLOCKED — H/C exact wire mapping:** H36-AP-01..07 require explicit H/C resolution and exact-version approval.
- **BLOCKED — authority integration:** I/D/B authority confirmations remain independent prerequisites.
- **NOT RUN — conformance:** C-FR-01..12, G-36-01..15 and H Adapter conformance cases have no executable run evidence in this review.
- **NOT VERIFIED — implementation:** no runtime/Adapter/provider implementation or production evidence is accepted here.

## 6. Required next actions

1. H Owner publishes a revised Adapter Capability/Applied Attestation candidate (or explicit exact-version mapping addendum) that resolves H36-AP-01..07 against C's exact Final Request evidence and G's Applied predicate.
2. C confirms the revised final-boundary/evidence mapping; G confirms the Applied consumer mapping. Their decisions must pin the same exact package/source Blob, not merely a filename or branch.
3. I and D separately confirm their authority fields and ordering/currentness semantics; B confirms typed references.
4. Only after source alignment, produce complete EN/zh-CN companions pinned to exact Owner Blob SHAs, then run semantic parity review.
5. Keep C/G/H freeze BLOCKED and all implementation/conformance statuses NOT VERIFIED / NOT RUN until their own evidence gates pass.

**Conclusion:** The six-stage architecture is semantically aligned, but H's current Adapter Capability/Applied Attestation candidate is not yet a complete field-level contract for C's final-request proof and G's Applied acceptance. Translation must not conceal this gap.


## 7. H candidate revision follow-up — 2026-11-17

After this review identified H36-AP-01..07, H's Owner branch added §11 to `adapter-capability-and-applied-attestation.md`. The live exact Blob is now `db59b63e322d7255b8b400f47859dcac32bb3027`; the previously reviewed `ed6b43a29aa368d772c701ffc83309a5aadf3c00` is superseded for currentness. The addendum proposes explicit request/boundary identity, target/attempt mapping, region inventory/coverage, verifier-bound identity, I/D authority references, provenance, per-request bypass coverage, replay identity and temporal rules.

Disposition: **candidate gap response drafted, not closed**. C and G have not accepted this exact Blob; I/D/B authority confirmations, H wire schema, generated SDK/interoperability, and conformance remain OPEN / NOT RUN. The six-stage semantic alignment finding remains valid; the seven field-mapping findings are now addressed by a proposal but are not marked RESOLVED until owner acceptance.

## 8. H recovery-batch amendment follow-up — 2026-11-17

H's candidate source was further updated with §11.8. Current exact H source Blob: `0dca3dc5463a02be0e19524811afbae87795baf5` (supersedes `db59b63e322d7255b8b400f47859dcac32bb3027`). The §11.8 proposal addresses the CGH-APPLIED-1.1 recovery-batch evidence expected by G: COC terminal proof, recovery-batch and participant-set completeness, owner high-water attestations, participant reconciliation, I terminal/revocation evidence, D lineage/cutoff/effective-position evidence, and Storage same-XID terminal evidence.

**New finding H36-AP-08 — OPEN:** the candidate mapping is now described, but the H wire schema/SDK and exact ACK message-family binding have not been updated or generated. H must preserve COC, I, D and Storage ordering domains as distinct; missing owner evidence remains UNKNOWN/IN_DOUBT. G's recovery-batch acceptance is exact-version and conditional; H cannot infer COC deployment or owner gate release. C/G/I/D/Storage confirmation and schema/conformance remain pending.

The §11.8 response is a candidate proposal only. H36-AP-01..08 are not marked RESOLVED until the corresponding owners accept the exact common package and the versioned H schema mapping is produced. C/G/H freeze remains BLOCKED.

## 9. H provider-outcome / owner-gate clarification — 2026-11-17

H's candidate source now includes §11.9 and has current exact Blob `74be8374a67da385a5f0f8e34c7aef2b38b72bcf`. It explicitly binds C-issued provider receipt and immutable CSubmitOutcome, preserves UNKNOWN/IN_DOUBT, requires participant terminal proof only after all owner outcomes are determinate, and reserves owner-local gate release attestations to the respective I or D authority.

**New finding H36-AP-09 — OPEN:** the candidate text now reserves the correct evidence/authority boundaries, but the exact H wire message-family schema/SDK mapping and consumer acceptance remain absent. C/G/I/D/Storage must confirm the exact common version; no H ACK or COC observation may substitute for C provider outcome or I/D owner-signed gate release. H36-AP-01..09 remain OPEN pending exact-version owner decisions and schema/conformance evidence.

## 10. C exact-version recovery-batch acceptance gap — 2026-11-17

**New finding C36-AP-01 — OPEN:** C's live Phase 3.6 source remains Blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`. It contains C's Issue #3 acceptance for the exact CGH-APPLIED-1.0 package and C's Issue #6 BIH consumer acceptance, but it does not contain an explicit C Owner acceptance of G's later CGH-APPLIED-1.1 recovery-batch amendment, nor a complete exact-version CSubmitOutcome/provider-receipt mapping against that recovery profile.

G's current source explicitly requires actual C provider receipt and immutable CSubmitOutcome as part of the 1.1 causal-order/recovery predicate. H §§11.8–11.9 now propose carrying C-issued references, but an H proposal cannot substitute for C's own producer decision or provider evidence contract.

Required: C must publish an exact-version decision or source addendum pinning the same A/COC package version and defining the C-issued provider receipt/CSubmitOutcome, conditional terminal reference, UNKNOWN/IN_DOUBT behavior and causal binding to InferenceRequestId/FinalRequestBoundaryId/request digest/participant identity. Until then, H36-AP-09 and C36-AP-01 remain OPEN; no 1.1 cross-owner acceptance is inferred.

## 11. Correction — C exact-version acceptance located in separate Owner contract

The earlier C36-AP-01 finding is **RESOLVED at the C source-decision level**. The review initially examined C's Final Request Evidence contract only and did not include C's separate cross-authority causal-order contract. Re-read of `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` on `session-c-agent-integration-2026-11-16` returned exact Blob `45a48249717c8cddb07ab96197730ef93d406c22`.

That C Owner artifact explicitly records **ACCEPT WITH ENUMERATED EXCEPTIONS** for the exact CGH-APPLIED-1.1 recovery-batch amendment, pinning A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819` and companion COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`. It requires C-issued CSubmitOutcome, actual provider receipt, actual InferenceRequestId/FinalRequestBoundaryId, immutable request digest, UNKNOWN/IN_DOUBT handling and same-key recovery. C's JF-10 Issue #8 bridge decision is also recorded with exact artifact pins and enumerated C-owned conditions.

A complete EN/zh-CN pair and targeted parity review were added:
- `docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`
- `docs/zh-CN/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`
- [EN review](2026-11-17-c-submit-causal-order-bilingual-review.md) / [中文 review](2026-11-17-c-submit-causal-order-bilingual-review.zh-CN.md)

This correction does not resolve H36-AP-09: H's versioned wire message-family Schema/SDK mapping and C/G/I/D/Storage consumer interoperability remain open. It also does not imply coordinator deployment, Provider implementation verification, or C-CO/JF-10 test execution.
