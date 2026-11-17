# ARCH-CONVERGENCE-001 — Context Applied & Runtime Execution
# ARCH-CONVERGENCE-001 — Context Applied 与运行时执行合同

- Workstream: D — Context Applied & Runtime Execution
- Status: **DRAFT / CONDITIONAL RUNTIME CONTRACT / NON-NORMATIVE**
- Review anchor: `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Sources: C `session-c-agent-integration-2026-11-16@88992da30331121b81cf2773acab11d921daf281`; F `session-f-memory-runtime@1908ce4d233b20f7cafd00cb679affd01bd15174`; G `session-g-memory-context@763b3d31e910db8fd29c6e4dbaff9273b7fb66b8`; H fetched `session-h-bmcp-protocol@6608cde89d959257db612d8ff8080f631333f3f3`; I `session-i-security-governance-2026-11-16@0d071bf1ee7cc71912398c6ae57e4496e08f44ab`; D `session-d-memory-brain-2026-11-16@194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f`; Storage `session-storage-consistency-forget-atomicity-2026-11-16@830a559bd2f4ec72608f5a51e1a0b43779f2b989`.
- Authority rule: C owns provider handoff/final request evidence; G owns Applied; H owns wire/Adapter evidence; I/D own authorization/Forget; this proposal does not merge those authorities.

## 1. Executive disposition / 执行结论

A memory is **Applied** only when G commits its own durable Applied decision after validating evidence bound to the exact final immutable inference request submitted to the runtime/provider boundary. The evidence must prove complete inclusion of the exact G ContextVersion's declared managed region in that request, under current authorization, Forget and Adapter capability conditions.

The evidence stages are separate:

`ContextPrepared → ContextDelivered → ContextMaterialized → FinalRequestSubmitted → GApplied`

None is an alias for another. Retrieval candidate, prompt candidate, context assembly, transport ACK, local materialization, workflow completion or provider response alone is not Applied.

C's final inference boundary contract defines the exact submit boundary and Full Applied evidence ceiling. G Phase 3.8.22 assigns the durable Applied decision exclusively to G, but labels the contract a design draft requiring cross-owner acceptance. C's Provider Submit Outcome is a C-owned semantic proposal, not shared-wire-frozen. H Applied Delivery Evidence 1.0.0 is a test/conformance candidate; exact C/G/I field mapping and production trust remain open.

只有 G 在验证与实际提交给 Runtime/Provider 的**精确最终不可变请求**绑定的证据后，持久化提交自己的 Applied 决议，才能称为 Applied。证据必须证明 G 指定的精确 ContextVersion 的完整 Managed Region 已包含在该请求中，并且授权、Forget 和 Adapter 能力条件均为当前有效。

各证据阶段相互独立：

`ContextPrepared → ContextDelivered → ContextMaterialized → FinalRequestSubmitted → GApplied`

检索候选、Prompt 候选、Context 组装、Transport ACK、本地物化、Workflow 完成或 Provider 响应都不能单独证明 Applied。

C 的 Final Inference Boundary 合同定义精确提交边界和 Full Applied 证据上限。G Phase 3.8.22 将持久化 Applied 决议唯一归属 G，但明确标注为需要跨 Owner 接受的设计草案。C Provider Submit Outcome 是 C 自有语义提案，尚未共享 Wire 冻结。H Applied Delivery Evidence 1.0.0 是测试/符合性候选；精确 C/G/I 字段映射和生产信任仍未关闭。

## 2. Minimum runtime state model / 最小运行时状态模型

This is an integration sequence. It deliberately does not flatten C, G and H state machines into one success enum.

```text
RecallRequested
  -> IAuthenticatedAndScoped
  -> FScopeFilteredCandidates
  -> DCanonicalAndForgetRevalidated
  -> IAuthorizationRevalidated
  -> GContextVersionCommitted
  -> GDeliveryIntentCommitted
  -> HDeliveryAccepted
  -> HManagedRegionMaterialized
  -> CFinalRequestFrozen
  -> CFinalRequestSubmitted
  -> CProviderOutcomeResolved
  -> HAuthenticatedEvidenceRecorded
  -> GAppliedPredicateEvaluated
  -> GAppliedDecisionCommitted
```

Independent non-success evidence:
- F result may be partial/degraded/unavailable; do not imply Context.
- G delivery may be rejected, superseded, expired, cancelled or unresolved.
- H evidence may be Partial, Bypassed, Unknown or Rejected; only eligible Tier 1 evidence can support Full Applied.
- C provider handoff may be HANDOFF_ACCEPTED, HANDOFF_REJECTED, NOT_INVOKED, UNKNOWN or IN_DOUBT. UNKNOWN and IN_DOUBT are nonterminal.
- G Applied remains absent until G's durable predicate and idempotency checks succeed.

## 3. Exact final-request evidence boundary / 精确最终请求证据边界

### 3.1 What Full Applied means

The final inference request boundary is the last controlled point where:
1. all transformations that can change the inference payload have completed;
2. the exact immutable request representation is fixed;
3. the actual request submission/handoff to the runtime/provider is observed and identified;
4. the submit operation can no longer be mutated/replaced by an uncontrolled caller.

Full Applied means the complete declared target Managed Region is present in that exact submitted request. It does not prove model attention, understanding, memory, use, compliance, response correctness, user delivery or execution completion.

If a platform has no reliable submit hook and actual request ID, Full Applied is not attestable. A pre-submit callback, prompt-builder output, local cache, intermediate buffer, render or delivery ACK is insufficient.

### 3.2 Evidence tiers

| Tier | Observable boundary | Maximum permitted statement |
|---|---|---|
| Tier 1 — Final-request observable | Exact final immutable request, actual submission, request ID, complete region digest, current identity/capability binding | May produce candidate Full Applied evidence for G validation |
| Tier 2 — Managed-region observable | Controlled pre-submit region/materialization; cannot independently prove exact submitted request | Partial or Unknown only; Full Applied forbidden |
| Tier 3 — Transport/basic | Receive/negotiate/deliver or Recall only; no final request observation | Received/Accepted/Delivered/Rejected/Unknown only |
| Unsupported | Boundary, identity, digest or authority cannot be proven | Unsupported/Unknown; no Applied |

Tier is an evidence ceiling, not a vendor label. Each request may be Partial, Bypassed or Unknown even for a Tier 1 integration.

### 3.3 Exact binding dimensions

C's semantic binding tuple is:

`(inference_request_id, agent_instance_id, session_id, context_id, context_version_id, delivery_id, adapter_id, adapter_instance_id, capability_epoch, boundary_id)`

C's Final Request Submission Evidence additionally binds:
- actual runtime/provider-assigned InferenceRequestId;
- final boundary ID/type and evidence profile;
- G ContextId/ContextVersion/DeliveryId/DeliveryAttemptId;
- authenticated Agent/Adapter/runtime/session identities;
- ScopeRef and EnvironmentRef where required;
- exact Managed Region identity, revision, inventory digest and complete content digest;
- PermissionEpoch and I authorization decision reference current at submit;
- D ForgetFence reference/generation and validation reference for represented source lineage;
- H AdapterCapabilityEpoch, negotiated profile, evidence issuer, integrity and schema version;
- submission outcome/time/monotonic sequence, correlation/causation and audit references;
- explicit coverage: COMPLETE/PARTIAL/BYPASSED/UNKNOWN.

Payload identity strings are claims, not credentials. C must not synthesize InferenceRequestId from DeliveryId or infer successful submission from local rendering.

## 4. Authority and evidence contract / 权威与证据合同

| Evidence / state | Issuer and owner | Proves | Does not prove |
|---|---|---|---|
| RetrievalResult | F | Candidate refs, completeness/freshness and channel status under F checks | Context membership or Applied |
| ContextVersion / ChangeSet | G | Immutable desired managed Context state | Delivery or actual request inclusion |
| Delivery intent/attempt | G | G intends to deliver exact ContextVersion | H receipt or Adapter application |
| H delivery receipt | H | Authenticated transport accepted exact delivery attempt | Materialization or Applied |
| Materialization evidence | H Adapter | Exact content placed in declared managed region | Final request inclusion/submission |
| Final Request Submission Evidence | C semantic boundary; H wire/integrity | Exact final request crossed observed submit boundary with region binding | G Applied decision or model attention |
| CSubmitOutcome | C | Provider handoff outcome for exact immutable request/attempt | Model execution completion or G Applied |
| Applied record | G | G accepted complete predicate and committed durable per-request decision | Attention, understanding, correct behavior or global Forget |
| I authorization proof | I | Current authorization/revocation order for bound operation | D Forget or Storage visibility |
| D Forget proof | D | Current fence/lineage/barrier state | I authorization or physical erasure |
| Storage/COC proof | Storage/COC | Same-GID participant and visibility/recovery outcome | G Applied or I policy decision |

## 5. G-owned Full Applied predicate / G 独有 Full Applied 判定

G alone may create or mutate the Applied decision. A Full Applied commit requires one immutable logical Applied identity and a complete evidence revision proving, for the same request and causal transaction:

1. C's immutable authoritative CSubmitOutcome proves determinate successful provider handoff for the exact final request.
2. H authenticated Adapter/Runtime/Delivery evidence is current, integrity-valid and bound to the same request and evidence revision.
3. COC terminal proof identifies the same transaction, participant, reservation, request digest and terminal result, with complete recovery-batch and owner high-water evidence.
4. I authorization/receipt-consumption terminal evidence and D complete-lineage ForgetFence evidence are independently authenticated and ordered by their own authorities.
5. Where JF-10 Storage participation applies, Storage proves same-GID terminal resolution and exact atomic VisibilityPointer/PublicationReceipt or non-publication outcome.
6. G's ContextVersion, Delivery attempt, Scope/Environment, managed-region inventory/digest, identity, session and capability predicates pass at the required linearization point.

No single ACK or owner result is sufficient. In particular:
- H ACK does not write G Applied.
- CSubmitOutcome does not write G Applied.
- I COMMIT_WON is authorization order only.
- D suppression clearance is not global Forget completion.
- Storage PREPARED is not visibility.
- COC quorum commit is not Applied.
- Workflow/job completion is not business completion.

Full Applied is an evidence-backed G business state, not a side effect of an external runtime's callback.

## 6. Provider dispatch and retry / Provider Dispatch 与重试

C owns ProviderAttempt identity, provider idempotency-key scope, final egress gate and CSubmitOutcome. Its outcome algebra is:

| Outcome | Terminal for attempt? | Retry/replay rule |
|---|---:|---|
| HANDOFF_ACCEPTED | Yes, handoff fact only | No second send for same attempt; execution-start is separate |
| HANDOFF_REJECTED | Yes, only if no side effect is proven | New attempt only after fresh I/D/C checks |
| NOT_INVOKED | Yes, only with positive no-handoff proof | New attempt after proof and fresh gates |
| UNKNOWN | No | Suppress retries; reconcile same attempt/provider key |
| IN_DOUBT | No, non-expiring | No new attempt/key; same provider idempotency key and authoritative reconciliation |

Timeout, crash, lost ACK, missing row or provider lookup outage is not proof of NOT_INVOKED. If a side effect may exist, use IN_DOUBT. Unknown outcome never authorizes a second provider call under a new key.

A worker/outbox retry preserves logical DeliveryId/ProviderAttempt identity as specified by the owning contract and creates a new attempt only through the owner's explicit transition. Outbox delivery is at-least-once; stable event/operation identity and digest make consumers idempotent. No transport cursor or workflow ACK advances G Applied.

## 7. Minimum durable work contract / 最小持久化工作合同

The minimum system needs durable records for:
- G Delivery intent, target ContextVersion and DeliveryAttempt;
- H delivery/materialization/final-request observation evidence, with distinct H observation identity;
- C ProviderAttempt and immutable CSubmitOutcome with same-key recovery;
- G Applied decision identity, evidence revision, idempotency digest and terminal status;
- COC/Storage participant reference and same-GID terminal evidence when JF-10 applies;
- outbox/worker delivery intent, attempt/lease and consumer contiguous watermark.

The following identities remain distinct:
- `HDeliveryBindingIdentity = (adapter_instance_ref, runtime_session_ref, delivery_id, delivery_attempt_id, inference_request_id, final_request_boundary_id, adapter_capability_epoch)`
- `HEvidenceIdentity = (HDeliveryBindingIdentity, evidence_kind)`
- `HObservationRecordIdentity = (issuer_ref, sender_authority_ref, sender_subject_ref, message_id, message_nonce, signing_sequence_namespace_ref, signing_record_sequence)`

These three H identities must not be substituted for one another. H's Applied Delivery Evidence 1.0.0 is a separate message family; it does not extend or mutate Unified COC/JF-10/Provider Outcome 1.2.15.

### Crash/retry rules

- Crash before provider dispatch: C must prove NOT_INVOKED before a new attempt.
- Crash after dispatch before callback/evidence: UNKNOWN/IN_DOUBT; reconcile same attempt and provider key.
- Crash after C outcome persistence before ACK: same CSubmitOutcome is read back.
- Crash after H observation persistence before ACK: same observation identity/digest returns original record; changed digest conflicts.
- Crash after all evidence but before G Applied commit: G re-evaluates same immutable evidence revision and same Applied identity; no duplicate Applied record.
- Crash after G Applied commit before response: same Applied identity returns original G record.
- Duplicate provider callback or outbox delivery: idempotent by exact identity/digest.
- PermissionEpoch or ForgetFence advances before the final boundary: stale request is rejected/superseded; a previous authorization or materialization cannot be refreshed into permission.

## 8. MCP / BMCP boundaries / 协议边界

- BMCP/H owns Brain Context delivery, Adapter capability, evidence wire and reconnect behavior. H does not own Context membership (G), Applied (G), provider truth (C), authorization (I) or Forget (D).
- MCP tool invocation is not an authorization grant. Every tool call that reads/writes protected Brain resources must re-enter I's authenticated principal/action/resource/purpose/scope/environment checks and D's current Forget visibility rules.
- An Agent, MCP server, Provider, Adapter or external memory product cannot bypass the Brain-owned authorization boundary by presenting its own role or tenant field.
- The initial vertical slice can use an in-process controlled Adapter/runtime test harness. External MCP/BMCP interoperability is an adapter conformance stage, not a prerequisite for the first canonical Memory commit. Full Applied proof, however, requires an observable final-request submit boundary.

## 9. Executable acceptance definitions / 可执行验收定义

| Test | Adversarial setup | Required assertion |
|---|---|---|
| D-RUN-01 | Candidate retrieved, then I revokes before dispatch | Final request is denied/paused; no Full Applied |
| D-RUN-02 | Candidate retrieved, then D installs ForgetFence before dispatch | F/G/C final boundary suppresses target |
| D-RUN-03 | G ContextVersion changes after delivery queued | Old Delivery attempt is superseded; late ACK cannot set current Applied |
| D-RUN-04 | H Tier 2 materialization only | Full Applied is rejected; Partial/Unknown only |
| D-RUN-05 | Tier 1 exact request with incomplete managed-region digest | Full Applied rejected |
| D-RUN-06 | Final request transformed after pre-submit hook | Old digest/boundary evidence rejected |
| D-RUN-07 | Provider handoff times out after possible side effect | C outcome UNKNOWN/IN_DOUBT; no new provider key |
| D-RUN-08 | Provider callback delivered twice | Same C outcome idempotent; conflicting digest rejected |
| D-RUN-09 | H observation replay same identity/same digest | Original observation ref returned |
| D-RUN-10 | H observation replay same identity/different digest | Conflict; original evidence unchanged |
| D-RUN-11 | CSubmitOutcome accepted but H evidence missing | G Full Applied remains absent |
| D-RUN-12 | H evidence valid but C outcome UNKNOWN | G Full Applied remains absent |
| D-RUN-13 | G crash before Applied transaction commit | No Applied record; same evidence revision may retry |
| D-RUN-14 | G crash after Applied commit before response | Same Applied record returned |
| D-RUN-15 | COC/Storage participant is PREPARED/UNKNOWN | Full Applied blocked; no inference from ACK/quorum |
| D-RUN-16 | MCP tool presents forged Principal/Scope | I PEP denies; no protected data disclosure |
| D-RUN-17 | Duplicate outbox event or worker lease expiry | Stable logical identity; no duplicate delivery/Applied side effect |
| D-RUN-18 | Restore from stale Context/Adapter snapshot after Forget | Reconnect fenced until I/D/G reconciliation |

## 10. Evidence and open blockers / 证据与未决阻塞

### Verified bounded evidence

- C final-request semantic boundary is marked DECIDED, but its evidence profile and H/G/I implementation dependencies remain OPEN.
- C Provider Submit Outcome defines the five-outcome algebra, but its source says proposed for exact Owner review and not shared-wire-frozen.
- G Phase 3.8.22 is a G-owned normative design draft; it explicitly says implementation not verified and cross-owner acceptance required.
- H Applied Delivery Evidence 1.0.0 candidate defines separate binding/evidence/observation identities and strict schema/validator rules. Its CI run 44130722532 reports 11/11 tests passing on exact commit `4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6`; this is candidate conformance only, not production crypto/replay or C/G/I integration.
- PR #92 says C Provider Outcome 19/19 candidate tests pass on its exact head, but C end-to-end Agent/Provider/Tool/Brain tests remain NOT RUN.
- H/C branch tree integrity incident PRs #90/#91 and later restoration pins still require reconciliation. The currently fetched H branch SHA differs from the H restoration SHA cited in the incident/review record. Do not promote schema 1.0.0/1.2.15 based on a mismatched pin.

### Blocking owner decisions

1. C must accept exact G/H Applied identity and final-boundary mapping at exact current blobs.
2. G must accept H Delivery Evidence 1.0.0 exact identity tuple and define exact Applied record persistence/terminal semantics.
3. H must confirm the live branch head, restore history, production crypto/canonicalization/key/trust profile and durable observation replay.
4. I must accept signer/issuer/key trust, PermissionEpoch currentness and authorization evidence binding.
5. D must accept Forget lineage/fence ordering at the final request boundary.
6. Storage/COC must supply exact same-GID terminal resolution when JF-10 participation applies.
7. C/G/H must execute crash-after-dispatch, duplicate callback, replay, stale Context, stale epoch and cross-language conformance on exact pinned commits.

**Workstream D status: SEMANTIC FINAL-REQUEST BOUNDARY DEFINED; FULL APPLIED CROSS-OWNER FREEZE AND RUNTIME EXECUTION NOT VERIFIED.**

No Applied schema is globally frozen. No production Adapter is certified. No model attention/use claim is made. No end-to-end test is claimed as executed.

**D 工作流状态：最终请求语义边界已定义；Full Applied 跨 Owner 冻结和运行时执行尚未验证。**

尚未全局冻结 Applied Schema，尚无生产 Adapter 获得认证，不声明模型注意/使用，也不声称端到端测试已执行。
