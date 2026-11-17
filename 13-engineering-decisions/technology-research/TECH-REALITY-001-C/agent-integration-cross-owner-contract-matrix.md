# Cross-owner Contract Matrix / 跨 Owner 契约矩阵

**Rule:** this matrix records observed authority and current evidence; it does not approve another Owner's contract.

| Area | Authority / exact evidence read | C integration requirement | Status / unresolved |
|---|---|---|---|
| B Domain | Main `domain-model-overview.md` Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346`; core entities `8cb5a674eec8eac1f3c4d83c400dc08d00166f23`; epistemic/time `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7`; scope `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | Use B ActorRef/PrincipalRef/ScopeRef/Event/Claim/Evidence/Provenance/time semantics. Request/Attempt/Execution refs must be B-approved typed objects before schema freeze. | Fact/Claim ADR remains ADR-BLOCKED; B PR #55 Draft and B0/B5 not passed. |
| D Lifecycle/Forget | D branch HEAD `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f`; Forget contract Blob `1f0391bc49d007c44ec74165bd33d37412cc7990` | Candidate submission is not lifecycle transition. Candidate/result must revalidate durable Forget fence and lineage at acceptance/commit. Late work cannot resurrect suppressed targets. | D says global completion/physical erasure are I-owned; exact cross-owner execution proof remains open. |
| E Compiler | E branch HEAD `ee098e14747d9915de5b3efb63b3a8dd77f670ed`; local producer Blob `4fb9e58511941f59b4d777336f8f85ad88ecccf1` | Model output is input evidence only; derived-memory production/provenance/queues are E-owned. | Full E source contract and current candidate pipeline not exhaustively read: NOT VERIFIED. |
| F Runtime | F branch HEAD `1908ce4d233b20f7cafd00cb679affd01bd15174`; local runtime Blob `29e9504c75d737c2dd200ebc3306eda555f0b0ac` | Agent treats MemoryRefs as scoped/versioned references; stale references must be invalidated/rejected. Retrieval and activation decisions are F-owned. | Full F reference/cursor contract not exhaustively read: NOT VERIFIED. |
| G Context/Applied | G branch HEAD `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8`; Applied contract Blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a`; Applied Persistence EN/zh-CN `bd297873...` / `82553a47...` | C supplies exact final-request submission evidence. G alone accepts Full Applied predicate and record. Delivered/Materialized/Submitted/Applied/ExecutionStarted remain distinct. | G explicitly: cross-owner freeze BLOCKED; implementation/execution NOT VERIFIED. |
| H BMCP | H Owner branch HEAD `4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6`; Phase 3.8.23 decisions `be308261...` / `641abd9b...`; Phase 3.8.24 candidate decision `36dff0b...`, schema `2ce8776...`, validator `2f6de24...`, tests `bb2bb6c...`. Unified 1.2.15 schema `860fc4...`, gateway validator `9cc426...` and mapping `2dc30f...` are restored in current H tree at new HEAD; the earlier `0277a8b...` snapshot had removed them | CSubmitOutcome semantics and final-request submit boundary are C-owned; H owns wire schema, transport envelope, Adapter/Runtime/Delivery evidence, validator and ACK semantics. H Phase 3.8.24 now implements a separate versioned Applied Delivery Evidence 1.0.0 schema/validator/test candidate. C must review exact final-boundary equality and C/H COutcomeRecord mapping, not author H wire fields. | H 1.2.15 artifacts are restored in current H branch tree at `4e65a2...`; earlier absence at `0277a8...` was a branch-integrity incident now followed by restoration. H Phase 3.8.24 Applied Delivery Evidence 1.0.0 schema/validator/test candidate exists; exact-head CI 11/11 PASS. Candidate-only; callback semantics, durable replay and production trust are not implemented. Wire mapping NOT FROZEN. I trust and Storage successor binding remain open. |
| I Security | I branch HEAD `0d071bf1ee7cc71912398c6ae57e4496e08f44ab`; register Blob `f5fd2558c657f4ef49396a7a00cdbcd0f226f853`; causal authorization Blob `5a5304d48aa912dcf6f817099bd5659371d8cdc8` | Principal, delegation, policy, PermissionEpoch, revocation and tool grants are I-owned. Every protected boundary revalidates current authorization. | Register states candidate; external governance/service deployment and cross-owner acceptance open. |
| Storage | Storage branch HEAD `830a559bd2f4ec72608f5a51e1a0b43779f2b989`; ADR Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`; v3.3.2 manifest `5c614375e10698e4931d83deb57d20321445e068` | Provider outcome and Brain commit/visibility remain separate. Durable retry/receipt/commit evidence must be queried from the owning authority. | Option A selected only as L1 logical serialization profile; v3.3.2 not jointly accepted/frozen and binds H 1.2.14, not 1.2.15. |

## C-REVIEW-001 H delivery evidence delta / H Delivery Evidence 增量

H Phase 3.8.23 (EN Blob `be308261c3e000e712a3cdbd3dbf60507156127b`; zh-CN Blob `641abd9b5a4ed271c3c4b561747c99d7cde79463`) distinguishes the existing Unified 1.2.15 `C_PROVIDER_OUTCOME_RECORDED` Gateway Attestation from Adapter/Runtime Applied Delivery Evidence. It forbids widening the existing P0 allowlist/schema/validator in place. H Phase 3.8.24 has now supplied a separate `bmcp.applied-delivery-evidence` 1.0.0 schema/validator/test candidate (schema Blob `2ce8776...`, validator Blob `2f6de24...`, test Blob `bb2bb6c...`) and exact-head CI 11/11 PASS. This is a test/conformance candidate only: callbacks are injected, durable replay storage and production trust are not implemented, and C/H wire mapping remains NOT FROZEN. C's remaining task is to verify CSubmitOutcome 1.0.1 field duplication and exact `final_request_boundary_id` equality against this H-owned mapping. G and I acceptance, H implementation, I trust registration and Storage binding remain separate gates.

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
H 拥有 Wire Schema、Envelope、Validator、Transport、Adapter/Runtime/Delivery Evidence 和 ACK。当前 H Owner HEAD 为恢复后的 `4e65a2...`（215 blobs），Unified 1.2.15 工件已恢复；Phase 3.8.24 独立 Applied Delivery Evidence 1.0.0 Schema/Validator/Test 候选存在，精确 CI 11/11 通过。该候选不证明生产信任或持久 Replay，C/H Wire Mapping 仍未冻结。C 不得擅自修改 H 字段。

### I — Security
I 拥有 Principal/Delegation Trust、PolicyDomain、PermissionEpoch、Authorization 和 Revocation。I 的治理登记表为 Candidate；文档提交不等于生效批准。

### Storage
Storage 拥有 Durable Commit/Visibility 和恢复机制。Option A 仅选择 L1 逻辑序列化档案；v3.3.2 尚未联合接受/冻结，并仍绑定 H 1.2.14，而不是 H 1.2.15。

本次未建立 C/H/I/Storage 字段级联合 Wire Freeze。CSubmitOutcome 1.0.1 与 H 1.2.15 是不同 Owner 分支上的候选版本。G Applied、D Forget 和 I Authorization 是互相独立的必要条件。C5 维持 BLOCKED/PARTIAL。



## Live H / D / I / Storage delta / H、D、I、Storage 当前增量

### H — BMCP / Provider Outcome
Historical H ancestor `0d36324457e39bd50ad56ae902d477c4ea765b61` contained Unified 1.2.15 schema, mapping, local C Provider Outcome validator and Gateway Attestation validator. Exact historical CI: run 44079842914 = 91/91; run 44079842878 = 288, 22 skipped, 0 failures. A subsequent branch-integrity incident snapshot `0277a8b...` removed these artifacts temporarily; they are restored at current H Owner HEAD `4e65a2...` (215 blobs). A review PR #67 disposition DEFERRED. The bounded tests do not prove production trust, signing issuance, durable replay or live I/D/Storage. C Phase 3.8.27 and I Phase 3.8.23 accept corrected ordering as reference contracts, not production deployment. Storage v3.3.2 still pins H 1.2.14. **Status: local CI PASS; joint wire freeze / production trust OPEN.**

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
H 旧 HEAD `0d363244...` 的 1.2.15 本地 CI 曾通过；之后 `0277a8b...` 出现分支树完整性事件，现已在 H HEAD `4e65a2...` 恢复 Unified 1.2.15 文件。H Phase 3.8.24 Applied Delivery Evidence 1.0.0 候选 CI 11/11 通过，但 Wire Mapping、生产 Trust 和联合 Wire Freeze 仍开放。D/I/Storage 的 Phase 3.9 提案提出“Fence 立即读抑制—Barrier Drain—D Forgotten LifecycleEvent—I 单次授权收据—Storage 原子终态提交”的分离链路，但所有提案均未成为规范。B 分支 Head 已刷新为 8ba14b99，关键领域文件 Blob 与本研究记录一致。跨 Owner Gate 仍未关闭。


## C/H Phase 3.8.24 consumer review snapshot / C/H 3.8.24 消费方审查快照

C Phase 3.8.23 EN/zh-CN decisions (Blobs `4860c627...` / `165d5847...`) accept only C-owned identity semantics against exact G blobs; they explicitly do not accept H wire mapping. H Phase 3.8.24 candidate provides all seven HDeliveryBindingIdentity fields and all seven HObservationRecordIdentity fields, plus a closed evidence_kind enum. However, the candidate schema has only `c_submit_outcome_ref`, `c_outcome_record_ref`, `c_outcome_record_sequence`, and `c_outcome_payload_digest` for C outcome linkage; it does not expose C `issuer_authority_ref` and `sequence_namespace_ref` as first-class C identity members. The H decision does not define whether `c_submit_outcome_ref` resolves an immutable C record carrying those missing fields or how the duplicated C fields are compared. `final_request_boundary_id` must equal C `FinalRequestBoundaryRef` byte-for-byte/opaque-reference equality; H validator only calls an injected `verify_c_final_boundary` callback and current tests stub it to True. C/H mapping is therefore NOT ACCEPTED / NOT VERIFIED pending exact resolution and mismatch vectors.
