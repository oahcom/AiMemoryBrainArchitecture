# Cross-owner Contract Matrix / 跨 Owner 契约矩阵

**Rule:** this matrix records observed authority and current evidence; it does not approve another Owner's contract.

| Area | Authority / exact evidence read | C integration requirement | Status / unresolved |
|---|---|---|---|
| B Domain | Main `domain-model-overview.md` Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346`; core entities `8cb5a674eec8eac1f3c4d83c400dc08d00166f23`; epistemic/time `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7`; scope `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | Use B ActorRef/PrincipalRef/ScopeRef/Event/Claim/Evidence/Provenance/time semantics. Request/Attempt/Execution refs must be B-approved typed objects before schema freeze. | Fact/Claim ADR remains ADR-BLOCKED; B PR #55 Draft and B0/B5 not passed. |
| D Lifecycle/Forget | D branch HEAD `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f`; Forget contract Blob `1f0391bc49d007c44ec74165bd33d37412cc7990` | Candidate submission is not lifecycle transition. Candidate/result must revalidate durable Forget fence and lineage at acceptance/commit. Late work cannot resurrect suppressed targets. | D says global completion/physical erasure are I-owned; exact cross-owner execution proof remains open. |
| E Compiler | E branch HEAD `ee098e14747d9915de5b3efb63b3a8dd77f670ed`; local producer Blob `4fb9e58511941f59b4d777336f8f85ad88ecccf1` | Model output is input evidence only; derived-memory production/provenance/queues are E-owned. | Full E source contract and current candidate pipeline not exhaustively read: NOT VERIFIED. |
| F Runtime | F branch HEAD `1908ce4d233b20f7cafd00cb679affd01bd15174`; local runtime Blob `29e9504c75d737c2dd200ebc3306eda555f0b0ac` | Agent treats MemoryRefs as scoped/versioned references; stale references must be invalidated/rejected. Retrieval and activation decisions are F-owned. | Full F reference/cursor contract not exhaustively read: NOT VERIFIED. |
| G Context/Applied | G branch HEAD `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8`; Applied contract Blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a`; Applied Persistence EN/zh-CN `bd297873...` / `82553a47...` | C supplies exact final-request submission evidence. G alone accepts Full Applied predicate and record. Delivered/Materialized/Submitted/Applied/ExecutionStarted remain distinct. | G explicitly: cross-owner freeze BLOCKED; implementation/execution NOT VERIFIED. |
| H BMCP | H Owner branch HEAD `6608cde89d959257db612d8ff8080f631333f3f3`; Phase 3.8.23 decisions `be308261...` / `641abd9b...`; Phase 3.8.24 candidate decision EN/zh-CN `f193113...` / `2c612ff...`, schema `2ce8776...`, validator `2f6de24...`, tests `bb2bb6c...` (code unchanged from tested commit `4e65a2...`). Unified 1.2.15 schema `860fc4...`, gateway validator `9cc426...` and mapping `2dc30f...` are restored in current H tree at new HEAD; the earlier `0277a8b...` snapshot had removed them | CSubmitOutcome semantics and final-request submit boundary are C-owned; H owns wire schema, transport envelope, Adapter/Runtime/Delivery evidence, validator and ACK semantics. H Phase 3.8.24 now implements a separate versioned Applied Delivery Evidence 1.0.0 schema/validator/test candidate. C must review exact final-boundary equality and C/H COutcomeRecord mapping, not author H wire fields. | H 1.2.15 artifacts are restored in current H branch tree at `4e65a2...`; earlier absence at `0277a8...` was a branch-integrity incident now followed by restoration. H Phase 3.8.24 Applied Delivery Evidence 1.0.0 schema/validator/test candidate exists; exact-head CI 11/11 PASS. Candidate-only; callback semantics, durable replay and production trust are not implemented. Wire mapping NOT FROZEN. I trust and Storage successor binding remain open. |
| I Security | I branch HEAD `0d071bf1ee7cc71912398c6ae57e4496e08f44ab`; register Blob `f5fd2558c657f4ef49396a7a00cdbcd0f226f853`; causal authorization Blob `5a5304d48aa912dcf6f817099bd5659371d8cdc8` | Principal, delegation, policy, PermissionEpoch, revocation and tool grants are I-owned. Every protected boundary revalidates current authorization. | Register states candidate; external governance/service deployment and cross-owner acceptance open. |
| Storage | Storage branch HEAD `830a559bd2f4ec72608f5a51e1a0b43779f2b989`; ADR Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`; v3.3.2 manifest `5c614375e10698e4931d83deb57d20321445e068` | Provider outcome and Brain commit/visibility remain separate. Durable retry/receipt/commit evidence must be queried from the owning authority. | Option A selected only as L1 logical serialization profile; v3.3.2 not jointly accepted/frozen and binds H 1.2.14, not 1.2.15. |

## C-REVIEW-001 H delivery evidence delta / H Delivery Evidence 增量

H Phase 3.8.23 (EN Blob `be308261c3e000e712a3cdbd3dbf60507156127b`; zh-CN Blob `641abd9b5a4ed271c3c4b561747c99d7cde79463`) distinguishes the existing Unified 1.2.15 `C_PROVIDER_OUTCOME_RECORDED` Gateway Attestation from Adapter/Runtime Applied Delivery Evidence. It forbids widening the existing P0 allowlist/schema/validator in place. H Phase 3.8.24 has now supplied a separate `bmcp.applied-delivery-evidence` 1.0.0 schema/validator/test candidate (schema Blob `2ce8776...`, validator Blob `2f6de24...`, test Blob `bb2bb6c...`) and exact-head CI 11/11 PASS. This is a test/conformance candidate only: callbacks are injected, durable replay storage and production trust are not implemented, and C/H wire mapping remains NOT FROZEN. C's remaining task is to verify CSubmitOutcome 1.0.1 field duplication and exact `final_request_boundary_id` equality against this H-owned mapping. Separately, C's Phase 3.8.22 source-level addendum finds G's claim that `final_request_boundary_id` is absent from H Unified 1.2.15 to be incorrect: it is present in the C Provider Outcome schema branch and Gateway P0 allowlist; `actual_inference_request_id` is also present, but is not automatically an alias for G's `inference_request_id`. G and I acceptance, H implementation, I trust registration and Storage binding remain separate gates.

H Phase 3.8.23 将现有 Unified 1.2.15 Gateway Attestation 与 Adapter/Runtime Applied Delivery Evidence 区分，并禁止原地扩大旧 P0。H Phase 3.8.24 已提供独立 `bmcp.applied-delivery-evidence` 1.0.0 Schema/Validator/Test 候选，精确 Head CI 11/11 通过；但校验依赖注入回调，未实现生产信任或持久 Replay。C/H Wire Mapping 仍未冻结。C 仍需针对 CSubmitOutcome 1.0.1 核验字段重复和 `final_request_boundary_id` 精确相等；G/I 接受、H 实现、I Trust 注册和 Storage 绑定是独立 Gate。

## Identity and time field rules / 身份与时间字段规则
- IDs are opaque, non-semantic. Never use display names as identity.
- Event time, Provider event time, Brain recorded_at and receipt/commit time are separate.
- TraceId, CorrelationId, RequestId, AttemptId, OperationId, SessionId and ProviderOperationId are never aliases.
- Typed references do not authenticate a principal or grant permission.
- A missing source time is UNKNOWN/NOT_REPORTED as appropriate, not fabricated from local receipt time.

## Reconciliation conclusion / 对账结论
No field-level joint C/H/I/Storage wire freeze is established by this pass. CSubmitOutcome 1.0.1 and H Unified 1.2.15 are versioned candidates in separate owner branches. G Applied remains blocked; D Forget and I authorization are separate mandatory predicates. C5 is **BLOCKED / PARTIAL** until exact-version Owner decisions and consumer conformance are recorded.


## 完整中文版本

### B — Domain Model
B 拥有 ActorRef、PrincipalRef、ScopeRef、Event、Claim、Evidence、Provenance 和时间语义。C 必须使用 B 的类型，不得自行冻结 Request/Attempt/Execution 领域类型。Fact/Claim ADR 仍阻塞，B PR #55 仍为 Draft。

### D — Memory Lifecycle/Forget
D 拥有规范 ForgetOperation、Fence、Canonical Suppression 和生命周期。候选提交不是生命周期转换；迟到结果必须重新检查 Fence 和 Lineage。D 不负责 I 的 Global/Physical Forget 完成策略。

### E — Compiler
E 拥有派生记忆生产和 Provenance 流程。模型输出只是输入来源，不是派生记忆的最终权威。E 当前特定生产合同未完整核验，NOT VERIFIED。

### F — Runtime
F 拥有 Retrieval、Activation、Working Set 和 Memory Reference 有效性。Agent 必须处理 Stale Reference，不能绕过 F 的引用失效机制。

### G — Context/Applied
G 拥有 ContextVersion、Applied Predicate 和 Applied Record。G 当前 HEAD 为 `763b3d...`；Applied Persistence EN/zh-CN Blobs 为 `bd297873...` / `82553a47...`。C 提供最终请求提交证据，H 提供独立的 Adapter/Runtime/Delivery Evidence，I 提供授权，D 提供 Forget Fence。G 明确表示跨 Owner 冻结阻塞，执行未验证。

### H — BMCP
H 拥有 Wire Schema、Envelope、Validator、Transport、Adapter/Runtime/Delivery Evidence 和 ACK。当前 H Owner HEAD 为 `6608cde...`（216 blobs；Schema/Validator/Test 代码与测试 Head `4e65a2...` 相同），Unified 1.2.15 工件已恢复；Phase 3.8.24 独立 Applied Delivery Evidence 1.0.0 Schema/Validator/Test 候选存在，精确 CI 11/11 通过。该候选不证明生产信任或持久 Replay，C/H Wire Mapping 仍未冻结。C 不得擅自修改 H 字段。

### I — Security
I 拥有 Principal/Delegation Trust、PolicyDomain、PermissionEpoch、Authorization 和 Revocation。I 的治理登记表为 Candidate；文档提交不等于生效批准。

### Storage
Storage 拥有 Durable Commit/Visibility 和恢复机制。Option A 仅选择 L1 逻辑序列化档案；v3.3.2 尚未联合接受/冻结，并仍绑定 H 1.2.14，而不是 H 1.2.15。

本次未建立 C/H/I/Storage 字段级联合 Wire Freeze。CSubmitOutcome 1.0.1 与 H 1.2.15 是不同 Owner 分支上的候选版本。G Applied、D Forget 和 I Authorization 是互相独立的必要条件。C5 维持 BLOCKED/PARTIAL。



## Live H / D / I / Storage delta / H、D、I、Storage 当前增量

### H — BMCP / Provider Outcome
Historical H ancestor `0d36324457e39bd50ad56ae902d477c4ea765b61` contained Unified 1.2.15 schema, mapping, local C Provider Outcome validator and Gateway Attestation validator. Exact historical CI: run 44079842914 = 91/91; run 44079842878 = 288, 22 skipped, 0 failures. A subsequent branch-integrity incident snapshot `0277a8b...` removed these artifacts temporarily; they are restored at H Owner HEAD `4e65a2...` and current docs HEAD `6608cde...` (216 blobs). A review PR #67 disposition DEFERRED. The bounded tests do not prove production trust, signing issuance, durable replay or live I/D/Storage. C Phase 3.8.27 and I Phase 3.8.23 accept corrected ordering as reference contracts, not production deployment. Storage v3.3.2 still pins H 1.2.14. **Status: local CI PASS; joint wire freeze / production trust OPEN.**

### D/I/Storage — Phase 3.9 Forget proposal
D PR #66, I PR #68 and Storage PR #71 propose a common terminalization path:
- D's durable ForgetFence linearization and immediate canonical read suppression are separated from later barrier drain.
- D alone appends the canonical Forgotten LifecycleEvent after validating current Fence/proof and a single-use I authorization receipt.
- I receipt returns COMMIT_WON, REVOCATION_WON or UNKNOWN/IN_DOUBT, bound to exact Memory/version/Scope/Fence/proof/Event digest.
- Storage final transaction checks current D Fence and exact I receipt; UNKNOWN retains private state.
These are proposals only; D/I/Storage exact-owner concurrence, implementation and physical proof remain open.

### B current branch
B PR #55 branch head is now `8ba14b99f1c303d9a368eb65178b0d79d507f2ff`; the eight key model/identity/state/temporal/invariant/matrix/conflict files were re-read at this current branch ref and their Blob SHAs match the pins in the baseline. B0/B5 status remains not passed.

### 中文结论
H 旧 HEAD `0d363244...` 的 1.2.15 本地 CI 曾通过；之后 `0277a8b...` 出现分支树完整性事件，现已在 H HEAD `4e65a2...` 恢复 Unified 1.2.15 文件，并在当前文档 Head `6608cde...` 保持完整。H Phase 3.8.24 Applied Delivery Evidence 1.0.0 候选 CI 11/11 通过，但 Wire Mapping、生产 Trust 和联合 Wire Freeze 仍开放。D/I/Storage 的 Phase 3.9 提案提出“Fence 立即读抑制—Barrier Drain—D Forgotten LifecycleEvent—I 单次授权收据—Storage 原子终态提交”的分离链路，但所有提案均未成为规范。B 分支 Head 已刷新为 8ba14b99，关键领域文件 Blob 与本研究记录一致。跨 Owner Gate 仍未关闭。


## C/H Phase 3.8.24 consumer review snapshot / C/H 3.8.24 消费方审查快照

C Phase 3.8.23 EN/zh-CN decisions (Blobs `4860c627...` / `165d5847...`) accept only C-owned identity semantics against exact G blobs; they explicitly do not accept H wire mapping. H Phase 3.8.24 candidate provides all seven HDeliveryBindingIdentity fields and all seven HObservationRecordIdentity fields, plus a closed evidence_kind enum. However, the candidate schema has only `c_submit_outcome_ref`, `c_outcome_record_ref`, `c_outcome_record_sequence`, and `c_outcome_payload_digest` for C outcome linkage; it does not expose C `issuer_authority_ref` and `sequence_namespace_ref` as first-class C identity members. The H decision does not define whether `c_submit_outcome_ref` resolves an immutable C record carrying those missing fields or how the duplicated C fields are compared. `final_request_boundary_id` must equal C `FinalRequestBoundaryRef` byte-for-byte/opaque-reference equality; H validator only calls an injected `verify_c_final_boundary` callback and current tests stub it to True. C/H mapping is therefore NOT ACCEPTED / NOT VERIFIED pending exact resolution and mismatch vectors.


---

## Phase 3.8.22 G / H 1.2.15 field-level reconciliation (2026-11-18)

This addendum records a source-level comparison, not a C/H Owner mapping decision or wire freeze.

### Exact source pins

| Authority | Artifact | Exact Blob | Evidence boundary |
|---|---|---|---|
| G | Phase 3.8.22 Applied Persistence / Idempotency / Crash / Restore contract | `bd297873bc1e593280484a43cb44b56058d9c4ff` | G-owned normative design draft; implementation not verified; cross-owner acceptance required |
| H | Unified COC/JF-10 Schema 1.2.15 | `860fc4cec658db7d2703cd6adf72aa31a2723f6d` | Candidate schema; not interchangeable with Applied ACK bridge schema |
| H | Gateway Attestation Validator 1.2.15 | `9cc426d4c26deb452f39daff34c1008dd535e969` | Reference integration validator; trust, issuer, transport, key-status and durable replay callbacks are deployment seams |
| H | Provider Outcome Validator 1.2.15 | `90a2d4b6f5b05590e3e0a7daecb5a01d9bf525c0` | Local schema/semantic validation; not production ingress trust or G Applied authority |
| H | Applied ACK 1.1.0 JF-10 bridge schema | `a8a945cc3623c2907003b93625e3c79742150944` | Separate schema family; cannot fill gaps in Unified Provider Outcome by implication |

### HDeliveryBindingIdentity field mapping

| G semantic member | H Unified 1.2.15 exact field | Source-level result | Requiredness / authority | Mapping disposition |
|---|---|---|---|---|
| `adapter_instance_ref` | None found | Not a first-class property in pinned schema or gateway validator | G requires an adapter-instance identity; H must identify authoritative issuer and immutable evidence carrier | UNAVAILABLE; H decision required |
| `runtime_session_ref` | None found | Not a first-class property in pinned schema or gateway validator | G requires runtime-session binding; do not borrow a similarly named field from another schema family | UNAVAILABLE; H decision required |
| `delivery_id` | None found | Not a first-class property in pinned schema or gateway validator | G requires stable delivery identity | UNAVAILABLE; H decision required |
| `delivery_attempt_id` | None found | Not a first-class property in pinned schema or gateway validator | G requires delivery-attempt identity | UNAVAILABLE; H decision required |
| `inference_request_id` | `actual_inference_request_id` exists; exact `inference_request_id` does not | Schema and gateway validator contain `actual_inference_request_id`; no automatic alias semantics established | C/H must define whether actual request ID is the authoritative inference request identity, including lifecycle/assignment semantics | UNRESOLVED; no implicit alias |
| `final_request_boundary_id` | `final_request_boundary_id` | Present in schema and gateway validator | Must bind the same immutable final request boundary used by C final-request evidence | EXACT NAME PRESENT; semantic/issuer binding still requires C/H acceptance |
| `adapter_capability_epoch` | None found | Not a first-class property in pinned schema or gateway validator | G requires capability epoch binding to prevent stale capability evidence | UNAVAILABLE; H decision required |
| Additional observed H field | `provider_adapter_ref` | Present in schema/validator | H-owned provider adapter reference | NOT EQUIVALENT by default to `adapter_instance_ref`; explicit H mapping required |

**Important correction:** G Phase 3.8.22 currently describes `final_request_boundary_id` as absent from H Unified 1.2.15. Exact Blob inspection shows it is present in both schema and gateway validator. The absence of the exact field name `inference_request_id` remains true; the present `actual_inference_request_id` must not be silently treated as an alias. Five other proposed HDeliveryBindingIdentity fields remain absent as first-class Unified 1.2.15 fields.

### Identity and evidence separation

- `CProviderAttemptIdentity` is C-owned stable logical provider-attempt identity; it is not the C outcome record identity.
- `COutcomeRecordIdentity` identifies an immutable C ledger observation; a late receipt is a successor observation, not a mutation of the original record.
- `HDeliveryBindingIdentity` is a proposed normalized consumer tuple; its exact wire mapping remains unresolved as above.
- `HEvidenceIdentity` and `HObservationRecordIdentity` remain H-owned evidence/observation identities and require explicit H source fields and authenticated issuer/sequence semantics.
- `COCParticipantIdentity` is COC/Storage-owned; native database XID is not a substitute for PreparedTransactionGID or participant identity.
- `GAppliedIdentity` is G-owned and binds the stable identities; payload/evidence digests belong to immutable evidence revisions and must not manufacture a new logical Applied identity.
- H Unified 1.2.15 and H Applied ACK 1.1.0 JF-10 bridge are distinct schema families. Neither may be silently substituted for the other.

### Required joint closure

1. H publishes or identifies an exact, authenticated, immutable evidence carrier for the five unavailable HDeliveryBindingIdentity fields, or versions explicit fields into a successor schema and validator.
2. C/H decide the exact mapping and semantics of `actual_inference_request_id` versus G's `inference_request_id`; no alias is inferred by C.
3. H confirms exact `final_request_boundary_id` semantic binding and issuer/evidence provenance.
4. G corrects the overbroad missing-field statement in Phase 3.8.22 through a successor revision; this matrix does not edit G-owned normative text.
5. C/H/G/I/Storage review exact successor Blob SHAs and publish explicit consumer acceptance. Storage v3.3.2's H 1.2.14 pin remains a separate blocking version conflict until a successor manifest is accepted.
6. Production trust roots, key custody/rotation/revocation, authenticated ingress ordering, durable replay and end-to-end Applied execution remain NOT VERIFIED.

### 中文对账结论

本附录是基于源码的字段级核验，不构成 C/H Owner 映射决议或 Wire Freeze。

- G Phase 3.8.22 精确 Blob：`bd297873bc1e593280484a43cb44b56058d9c4ff`，状态仍为规范设计草案、实现未验证、需要跨 Owner 接受。
- H Unified 1.2.15 Schema Blob：`860fc4cec658db7d2703cd6adf72aa31a2723f6d`；Gateway Validator Blob：`9cc426d4c26deb452f39daff34c1008dd535e969`；Provider Validator Blob：`90a2d4b6f5b05590e3e0a7daecb5a01d9bf525c0`。它们提供候选结构和有界本地验证，不代表生产信任或 G Applied 权威。
- H Unified 1.2.15 中确实存在 `actual_inference_request_id` 和 `final_request_boundary_id`。G 将后者也判定为缺失是不准确的，应由 G 后继修订纠正。
- 精确字段 `inference_request_id` 不存在。不得未经 C/H 决议将其视为 `actual_inference_request_id` 的别名。
- `adapter_instance_ref`、`runtime_session_ref`、`delivery_id`、`delivery_attempt_id`、`adapter_capability_epoch` 五个字段仍未作为 Unified 1.2.15 一等属性出现。虽然 `provider_adapter_ref` 存在，但不能默认等价于 `adapter_instance_ref`。
- H Applied ACK 1.1.0 JF-10 Bridge 是独立 Schema Family，不能替代 Unified Provider Outcome。
- 必须由 H 给出五个缺失字段的精确认证证据载体或发布后继 Schema/Validator；C/H 明确决定 Inference Request ID 映射；G 修订其字段缺失描述；C/H/G/I/Storage 对精确后继 Blob 做消费者接受。
- Storage v3.3.2 仍绑定 H 1.2.14 的版本冲突未解决。生产 Trust、密钥托管/轮换/撤销、认证入口顺序、持久化重放和端到端 Applied 执行仍未验证。

本附录不关闭 C-CON-002/003/004/014，不批准技术选型，不冻结 Schema，不授权生产部署，也不关闭任何 Gate。
