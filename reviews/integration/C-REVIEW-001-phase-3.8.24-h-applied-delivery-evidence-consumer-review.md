# C-REVIEW-001 Addendum — Phase 3.8.24 H Applied Delivery Evidence 1.0.0 Consumer Review
# C-REVIEW-001 补充审查 — Phase 3.8.24 H Applied Delivery Evidence 1.0.0 消费方审查

- Repository: `oahcom/AiMemoryBrainArchitecture`
- C Owner branch reviewed: `session-c-agent-integration-2026-11-16@88992da30331121b81cf2773acab11d921daf281`
- H Owner branch reviewed: `session-h-bmcp-protocol@4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6`
- G contract reviewed: `06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` Blob `bd297873bc1e593280484a43cb44b56058d9c4ff`
- C/G decision: `07-agent-integration/phase-3.8.23-c-exact-review-g-applied-persistence-identity.md` Blob `4860c627b4d7e84e23fb39ad83411674f3b88c7b`
- H decision: Phase 3.8.23 Blob `be308261c3e000e712a3cdbd3dbf60507156127b`
- H candidate: Phase 3.8.24 Blob `36dff0b2ca17773ebc2ef0252d17b2632ffe1b06`
- H schema: `bmcp.applied-delivery-evidence-1.0.0.schema.json` Blob `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608`
- H validator: Blob `2f6de24eea737cf75a16ead7495bea4627bb1bb4`
- H tests: Blob `bb2bb6c94cc73293f736c6dcd450ab32bffc6ee5`
- H CI: run `44130722532`, 11 tests, 0 failures
- C CI: run `44129914790`, 19 tests, 0 failures
- Status: **H IDENTITY SHAPE ACCEPTED AS A CANDIDATE; C OUTCOME FIELD MAPPING NOT ACCEPTED / NOT VERIFIED; NO WIRE FREEZE**

## 1. Executive decision / 总体决议

H has made substantive progress. The H Owner tree is restored, and Phase 3.8.24 now supplies a separate Applied Delivery Evidence 1.0.0 schema, reference validator, test suite and successful exact-head CI. This is the correct architectural separation from Unified 1.2.15's `C_PROVIDER_OUTCOME_RECORDED` Gateway Attestation. The two message families must not be conflated or merged into one widened P0 allowlist.

C accepts the *shape* of H-owned `HDeliveryBindingIdentity`, `HEvidenceIdentity` and `HObservationRecordIdentity` as a test/conformance candidate. C does **not** accept the exact COutcomeRecord linkage or final-request boundary equality as proven. The H validator delegates those checks to injected callbacks; current tests stub all callbacks as successful and do not consume a real CSubmitOutcome 1.0.1 record.

**Disposition: REQUEST CHANGES for C/H field mapping; keep H 1.0.0 candidate and both PRs Draft.** This is a delegated C-role technical review, not an independent human C Owner signature.

H 已有实质进展：H Owner 文件树已恢复，Phase 3.8.24 提供独立的 Applied Delivery Evidence 1.0.0 Schema、参考 Validator、测试和精确 Head CI。该设计正确地区分了 Unified 1.2.15 的 `C_PROVIDER_OUTCOME_RECORDED` Gateway Attestation；两种消息族不得混为一体，也不得原地扩大旧 P0 Allowlist。

C 接受 H 所有的 `HDeliveryBindingIdentity`、`HEvidenceIdentity`、`HObservationRecordIdentity` 身份结构作为测试候选，但不接受 COutcomeRecord 连接和最终请求边界相等性已经得到证明。H Validator 将这些检查委托给注入回调；当前测试把所有回调都模拟为成功，并未消费真实 CSubmitOutcome 1.0.1 记录。

**结论：C/H 字段映射 REQUEST CHANGES；H 1.0.0 候选及相关 PR 继续保持 Draft。** 本文是委托 C 角色技术审查，不是独立人类 C Owner 签署。

## 2. Exact field crosswalk / 精确字段对照

### 2.1 H-owned identity fields — candidate accepted

| H field | H identity role | C review |
|---|---|---|
| `adapter_instance_ref` | Adapter instance | Present; opaque exact ref |
| `runtime_session_ref` | Authenticated Runtime Session | Present; must be authenticated, not inferred from connection |
| `delivery_id` | G Delivery | Present; must resolve to G-issued identity |
| `delivery_attempt_id` | G Delivery Attempt | Present; must resolve to exact non-superseded attempt |
| `inference_request_id` | Runtime/Provider inference request | Present; must not be synthesized from DeliveryId |
| `final_request_boundary_id` | C final submit boundary | Present; exact equality to C `FinalRequestBoundaryRef` is mandatory |
| `adapter_capability_epoch` | H Adapter capability epoch | Present; must bind exact Adapter instance/session/profile |

The schema also contains the seven HObservationRecordIdentity members: `issuer_ref`, `sender_authority_ref`, `sender_subject_ref`, `message_id`, `message_nonce`, `signing_sequence_namespace_ref`, `signing_record_sequence`. `evidence_kind` is a closed enum, correctly separating evidence slots from delivery identity.

C accepts these as H-owned candidate shapes, with the explicit condition that the H and G owner resolvers authenticate and resolve them. Schema presence alone is not identity authentication.

### 2.2 C-owned fields — incomplete normative mapping

CSubmitOutcome 1.0.1 defines:

`COutcomeRecordIdentity = (issuer_authority_ref, sequence_namespace_ref, record_ref, record_sequence)`

The immutable C record also includes `FinalRequestBoundaryRef`, `payload_digest`, `ProviderAttemptRef`, `ProviderAttemptGeneration`, `ProviderRef`, `ProviderAccountRef`, idempotency namespace/key refs, `RequestDigest`, `Outcome` and `SideEffectStatus`.

H 1.0.0 currently exposes:

| H field | Possible C source | Review status |
|---|---|---|
| `c_submit_outcome_ref` | A reference to the immutable CSubmitOutcome record | **UNDEFINED**: reference target, resolver and identity semantics not specified |
| `c_outcome_record_ref` | C `record_ref` | Candidate mapping; equality not implemented/tested |
| `c_outcome_record_sequence` | C `record_sequence` | Candidate mapping; equality not implemented/tested |
| `c_outcome_payload_digest` | C `payload_digest` | Candidate mapping; equality not implemented/tested |
| `final_request_boundary_id` | C `FinalRequestBoundaryRef` | Required exact equality; callback only, no mismatch test |
| C `issuer_authority_ref` | No direct H field | Missing unless resolved from `c_submit_outcome_ref` |
| C `sequence_namespace_ref` | No direct H field | Missing unless resolved from `c_submit_outcome_ref` |

Important distinction: H `issuer_ref` and `signing_sequence_namespace_ref` identify the H observation signer and H signing sequence. They are **not** aliases for C `issuer_authority_ref` and C `sequence_namespace_ref`.

H may avoid duplicating every C field if `c_submit_outcome_ref` is normatively defined as an immutable, authenticated, resolvable CSubmitOutcome 1.0.1 record reference. If H keeps the duplicated fields, the validator must compare them against the resolved C record and fail closed on any mismatch. The current Phase 3.8.24 document/schema does not define this resolution contract.

### 2.3 Exact equality obligations / 精确相等义务

At minimum, H's C consumer validation must enforce:

- `c_outcome_record_ref == C.record_ref`
- `c_outcome_record_sequence == C.record_sequence`
- `c_outcome_payload_digest == C.payload_digest`
- `final_request_boundary_id == C.FinalRequestBoundaryRef`
- The resolved C record's `issuer_authority_ref` and `sequence_namespace_ref` are authenticated and retained as part of the full COutcomeRecordIdentity.
- `c_submit_outcome_ref` resolves to that same immutable C record, not a caller-supplied display name or arbitrary URI.
- C record outcome/side-effect semantics are consumed from C authority; H does not reinterpret or mint Provider Outcome truth.

No case folding, URI rewriting, display-name matching, string normalization or fallback to H issuer/sequence fields is permitted.

## 3. Validator and CI evidence / Validator 与 CI 证据

H's validator exposes the following injected authority callbacks:
- `verify_profile_registration`
- `verify_key_status`
- `verify_signature`
- `verify_protected_identity_binding`
- `verify_c_final_boundary`
- `verify_g_delivery_binding`
- `verify_capability_epoch`
- `commit_observation`

The tri-state behavior is directionally correct: False => INVALID; unavailable/exception/None => UNKNOWN. The test module verifies schema closure, required H delivery fields, Tier-1 coverage, context-version equality, digest mutation, identity-domain separation, UNKNOWN trust behavior, invalid signature, same-digest replay and changed-digest conflict.

However:
1. The positive fixture injects all callbacks as `True`; it does not verify real C or G records.
2. The replay callback is a test stub returning NEW/SAME_DIGEST_REPLAY/CONFLICT; no durable H observation ledger is implemented.
3. `canonical_p0_bytes` uses deterministic sorted-key JSON for local tests, explicitly not the production H canonicalization profile.
4. No cross-schema vector loads C's actual 1.0.1 fixture and proves the duplicated H fields match it.
5. No negative vector mutates only `final_request_boundary_id`, C issuer, C sequence namespace, C record ref, C record sequence or C payload digest and expects rejection.

H run `44130722532` passed **11/11** tests. This is valid bounded reference-validator evidence, not proof of production cryptographic trust, durable replay, C/H service integration, or I registration.

C run `44129914790` passed **19/19** C Provider Outcome candidate tests. These are C schema/semantic and test-only crypto vector checks, not C/H integration tests or real Provider execution.

## 4. Required remediation / 必须整改

### H-owned
1. Update Phase 3.8.24 with a normative `c_submit_outcome_ref` resolution contract, or add explicit C issuer and sequence namespace fields.
2. Define the canonical one-to-one mapping for all duplicated C fields and the immutable C record resolver trust boundary.
3. Implement `verify_c_final_boundary` against the resolved C record and exact `FinalRequestBoundaryRef`; no placeholder callback acceptance.
4. Add cross-owner fixtures using CSubmitOutcome 1.0.1 positive vectors and mismatch vectors for every duplicated field.
5. Preserve H's tri-state fail-closed behavior and keep production crypto/durable replay explicitly separate until implemented.

### C-owned
1. Publish a C consumer crosswalk confirming the exact source field semantics and the fact that H cannot change C Provider Outcome truth.
2. Add C-side compatibility tests once H's immutable resolver/mapping is published.
3. Fix the C workflow path filter omission: include `07-agent-integration/schemas/c-submit-outcome-1.0.1.schema.json`. A Draft C-owned CI-only PR #94 carries this one-line correction; schema-only trigger execution is pending.

### G/I/Storage-owned
- G must independently accept the H Delivery/Context binding and Applied evidence predicate.
- I must approve signer/profile/key registry, trust roots, canonicalization and anti-rollback.
- Storage must bind the exact H schema/validator/vector/CI and I profile in a reviewed successor manifest. Existing Storage v3.3.2 binding to H 1.2.14 is not silently upgraded by this candidate.

## 5. Gate disposition / Gate 处置

| Gate | Status | Reason |
|---|---|---|
| HDeliveryBindingIdentity shape | <badge>ACCEPT CANDIDATE</badge> | All seven fields present |
| HObservationRecordIdentity shape | <badge>ACCEPT CANDIDATE</badge> | All seven fields present |
| HEvidenceIdentity / evidence_kind | <badge>ACCEPT CANDIDATE</badge> | Closed evidence enum |
| COutcomeRecordIdentity mapping | <badge>NOT ACCEPTED</badge> | C issuer/namespace resolution absent or undefined |
| FinalRequestBoundary equality | <badge>NOT VERIFIED</badge> | Injected callback; no negative mismatch vector |
| H local reference conformance | <badge>PASS 11/11</badge> | Exact H branch CI |
| C local candidate conformance | <badge>PASS 19/19</badge> | Exact C branch CI |
| Durable H observation replay | <badge>NOT IMPLEMENTED</badge> | Mock callback only |
| Production trust / I registration | <badge>NOT REGISTERED</badge> | Candidate profiles only |
| C/H interoperability | <badge>BLOCKED</badge> | Exact cross-schema mapping and tests absent |
| Global G Applied / Storage freeze | <badge>BLOCKED</badge> | Separate Owner decisions and implementation remain open |

No merge, schema freeze, production activation, Provider/Adapter egress authorization or Full Applied acceptance is requested.

## 6. Exact evidence links / 精确证据链接

- C Owner restored HEAD: https://github.com/oahcom/AiMemoryBrainArchitecture/commit/88992da30331121b81cf2773acab11d921daf281
- H Owner restored HEAD: https://github.com/oahcom/AiMemoryBrainArchitecture/commit/4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6
- H Phase 3.8.24 candidate: https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-h-bmcp-protocol/08-bmcp-protocol/phase-3.8.24-h-applied-delivery-evidence-1.0.0-schema-validator-candidate.md
- H schema: https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-h-bmcp-protocol/08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json
- H validator: https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-h-bmcp-protocol/08-bmcp-protocol/validators/applied_delivery_evidence_validator.py
- H CI run: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44130722532
- C CI run: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44129914790
- C workflow fix PR #94: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/94
- C review remediation PR #92: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/92
