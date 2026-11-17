# Cross-owner Contract Matrix / 跨 Owner 契约矩阵

**Rule:** this matrix records observed authority and current evidence; it does not approve another Owner's contract.

| Area | Authority / exact evidence read | C integration requirement | Status / unresolved |
|---|---|---|---|
| B Domain | Main `domain-model-overview.md` Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346`; core entities `8cb5a674eec8eac1f3c4d83c400dc08d00166f23`; epistemic/time `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7`; scope `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | Use B ActorRef/PrincipalRef/ScopeRef/Event/Claim/Evidence/Provenance/time semantics. Request/Attempt/Execution refs must be B-approved typed objects before schema freeze. | Fact/Claim ADR remains ADR-BLOCKED; B PR #55 Draft and B0/B5 not passed. |
| D Lifecycle/Forget | D branch HEAD `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f`; Forget contract Blob `1f0391bc49d007c44ec74165bd33d37412cc7990` | Candidate submission is not lifecycle transition. Candidate/result must revalidate durable Forget fence and lineage at acceptance/commit. Late work cannot resurrect suppressed targets. | D says global completion/physical erasure are I-owned; exact cross-owner execution proof remains open. |
| E Compiler | E branch HEAD `ee098e14747d9915de5b3efb63b3a8dd77f670ed`; local producer Blob `4fb9e58511941f59b4d777336f8f85ad88ecccf1` | Model output is input evidence only; derived-memory production/provenance/queues are E-owned. | Full E source contract and current candidate pipeline not exhaustively read: NOT VERIFIED. |
| F Runtime | F branch HEAD `1908ce4d233b20f7cafd00cb679affd01bd15174`; local runtime Blob `29e9504c75d737c2dd200ebc3306eda555f0b0ac` | Agent treats MemoryRefs as scoped/versioned references; stale references must be invalidated/rejected. Retrieval and activation decisions are F-owned. | Full F reference/cursor contract not exhaustively read: NOT VERIFIED. |
| G Context/Applied | G branch HEAD `3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe`; Applied contract Blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | C supplies exact final-request submission evidence. G alone accepts Full Applied predicate and record. Delivered/Materialized/Submitted/Applied/ExecutionStarted remain distinct. | G explicitly: cross-owner freeze BLOCKED; implementation/execution NOT VERIFIED. |
| H BMCP | H branch HEAD `0d36324457e39bd50ad56ae902d477c4ea765b61`; schema 1.2.15 Blob `860fc4cec658db7d2703cd6adf72aa31a2723f6d`; mapping Blob `2dc30f193d9c4f4bdc05ca4c137103687db28924` | CSubmitOutcome semantics are C-owned; H owns wire schema, transport envelope, validator and ACK semantics. No C field renaming or H schema authorship by C. | 1.2.15 is candidate, not frozen; exact validator/CI and trust proof open. |
| I Security | I branch HEAD `0d071bf1ee7cc71912398c6ae57e4496e08f44ab`; register Blob `f5fd2558c657f4ef49396a7a00cdbcd0f226f853`; causal authorization Blob `5a5304d48aa912dcf6f817099bd5659371d8cdc8` | Principal, delegation, policy, PermissionEpoch, revocation and tool grants are I-owned. Every protected boundary revalidates current authorization. | Register states candidate; external governance/service deployment and cross-owner acceptance open. |
| Storage | Storage branch HEAD `830a559bd2f4ec72608f5a51e1a0b43779f2b989`; ADR Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`; v3.3.2 manifest `5c614375e10698e4931d83deb57d20321445e068` | Provider outcome and Brain commit/visibility remain separate. Durable retry/receipt/commit evidence must be queried from the owning authority. | Option A selected only as L1 logical serialization profile; v3.3.2 not jointly accepted/frozen and binds H 1.2.14, not 1.2.15. |

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
G 拥有 ContextVersion、Applied Predicate 和 Applied Record。C 提供最终请求提交证据，H 提供 Wire/ACK，I 提供授权，D 提供 Forget Fence。G 明确表示跨 Owner 冻结阻塞，执行未验证。

### H — BMCP
H 拥有 Wire Schema、Envelope、Validator、Transport 和 ACK。H Unified 1.2.15 Blob 为 860fc4...，Mapping Blob 为 2dc30f...，均为候选；C 不得擅自修改 H 字段。

### I — Security
I 拥有 Principal/Delegation Trust、PolicyDomain、PermissionEpoch、Authorization 和 Revocation。I 的治理登记表为 Candidate；文档提交不等于生效批准。

### Storage
Storage 拥有 Durable Commit/Visibility 和恢复机制。Option A 仅选择 L1 逻辑序列化档案；v3.3.2 尚未联合接受/冻结，并仍绑定 H 1.2.14，而不是 H 1.2.15。

本次未建立 C/H/I/Storage 字段级联合 Wire Freeze。CSubmitOutcome 1.0.1 与 H 1.2.15 是不同 Owner 分支上的候选版本。G Applied、D Forget 和 I Authorization 是互相独立的必要条件。C5 维持 BLOCKED/PARTIAL。
