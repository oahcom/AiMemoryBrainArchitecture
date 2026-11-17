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
