# Canonical State Semantics
# 规范状态语义

- ID: B-STATE-001
- Status: CANDIDATE VOCABULARY BASELINE; Owner-specific state machines remain authoritative
- Source pins: Domain lifecycle Blob `81c48c928cb5f9c76ca29d493fbd9479079e62f7`; epistemic/temporal Blob `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7`; D Forget contract Blob `1f0391bc49d007c44ec74165bd33d37412cc7990`; C submit contract Blob `45a48249717c8cddb07ab96197730ef93d406c22`; Storage JF-10 protocol Blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0`.

## 1. Governing rule / 总原则

There is no universal cross-system `status` field. Status belongs to a typed subject and a named state machine. The same word on different object types does not imply the same transition, authority, evidence or terminality.

全系统不存在通用的 `status` 字段。状态必须属于明确类型的对象和指定状态机。不同对象类型上的同名状态，不代表相同转换、权威、证据或终态属性。

At minimum keep these dimensions separate:
- Claim epistemic standing;
- Memory lifecycle;
- Entity identity resolution;
- Relation lifecycle;
- Evidence availability;
- ForgetOperation phase;
- compiler work/attempt state;
- Context version/entry state;
- protocol delivery/acknowledgement;
- authorization decision and PermissionEpoch;
- storage transaction/visibility outcome;
- audit/governance decision.

## 2. Domain-owned state dimensions / 领域状态维度

| Subject | Vocabulary evidenced in source | Meaning and owner |
|---|---|---|
| Claim epistemic status | Observed, Reported, Inferred, Verified, Disputed, Retracted | Basis/standing of proposition; B defines semantics; E supplies derivation evidence; lifecycle manager preserves history |
| Memory lifecycle | Candidate, Consolidated, Active, Superseded, Archived, Forgotten | Management stage of canonical asset; B defines valid semantics; D owns canonical lifecycle execution |
| Entity identity status | provisional, resolved, merged, split, retired | Identity resolution/redirect state; Entity & Relationship Manager; identity rules need B/I reconciliation |
| Relation lifecycle | proposed, active, superseded, retracted | State of typed relation; B semantics and entity/relation manager execution |
| Evidence availability | available, restricted, expired, forgotten, external_unavailable | Whether evidence content/reference is available under policy; Evidence/Provenance owner + I policy |
| Scope status | active, suspended, closed, revoked | Namespace availability; I/Governance registry authority; B defines scope reference semantics |

### 2.1 Claim epistemic status is not Memory lifecycle

A Memory can be Active while containing Disputed Claims. An Archived Memory can contain a Verified Claim. A Retraction preserves the historical assertion and records authority/reason; it is not a deletion of historical evidence. Confidence alone cannot promote a Claim to Verified.

### 2.2 Forgotten is not a ForgetOperation phase

D's canonical Memory lifecycle vocabulary includes Forgotten. D's separate ForgetOperation phases include Requested, FenceEstablished, InventoryOpen, BarrierDraining, TargetReconciliation, CanonicalSuppressionComplete, Blocked and Failed. D explicitly states that “Forgetting” is not a Memory state. I separately owns global completion criteria and physical-erasure governance. The lifecycle transition to Forgotten is appended only when I's applicable criterion is met; it is not physical-erasure evidence.

## 3. Other owner state domains / 其他 Owner 状态域

| Subject | Examples | Authority boundary |
|---|---|---|
| Compiler work | CompileIntent, ProducerWorkItem, DerivationRun, Attempt, Lease, retry/DLQ/replay and terminal outcomes | E owns compiler-internal work/attempt state; D owns producer registration/barrier semantics |
| Context | ContextVersion, ChangeSet, entry states, reconciliation and historical Applied/current-use eligibility | G owns Context semantics and Applied state; exact current contract needs readback |
| Protocol delivery | Accepted/Rejected/Unknown, Delivery ACK, reconnect and capability epochs | H owns wire/transport ACK; transport ACK is not final Applied proof |
| Provider submit | CSubmitOutcome accepted/rejected/unknown/in-doubt | C alone records actual provider boundary outcome; unknown is not success or safe retry |
| Authorization | Allow/Deny/Indeterminate and PermissionEpoch | I owns policy, currentness, revocation order |
| Storage transaction | Prepared, owner commit/abort, outcome unknown | Storage owns physical participant outcome; exact XID recovery |
| Publication | VisibilityPointer, PublicationReceipt, Published | Storage owns durable visibility and publication receipt |
| Governance | Approved/Denied/Deferred/Exception etc. | I/governance authority; B cannot infer external approval |

## 4. Critical execution vocabulary / 关键执行词汇

| Term | Canonical semantic meaning | What it does NOT prove | Authority |
|---|---|---|---|
| Recorded | A fact/evidence/decision has been durably recorded by its owning system, with an authoritative record reference | It does not prove an external side effect, context application, transaction commit, or reader visibility | Record-owning module |
| Applied | The declared target operation crossed its exact application boundary and has the owner-required evidence; for Context, exact Adapter/final-request proof is required by approved contract | Transport ACK, buffer digest, reservation, or delivery receipt alone does not prove final request Applied; does not prove model comprehension | G validates/commits Context Applied; C proves final provider submit; H transports proof |
| Committed | The owning transaction/authority durably committed the defined state change and can resolve it after recovery | It does not universally imply indexing, Context application, or reader visibility in unrelated projections | Transaction/authority owner |
| Visible | The object is eligible for reader disclosure through the authoritative visibility mechanism after policy/scope checks | Staged bytes, queue/outbox state, object-store path, I COMMIT_WON alone, or local compiler state do not make it visible | Storage visibility authority; reader enforcement also applies |
| Published | The Storage-owned visibility transaction committed and the exact PublicationReceipt/VisibilityPointer can be authoritatively read back; E may then terminalize its work as Published | I COMMIT_WON alone, E local state, ACK or staged bytes do not prove Published | Storage owns publication; E consumes receipt |
| Acknowledged | A recipient/adapter reports the specific protocol action covered by its ACK class | Does not prove any stronger operation than that ACK's declared coverage | H/recipient |
| Superseded | A successor replaces an object for current use while historical identity/version remains retained subject to policy | Does not imply deletion or invalidity of every historical assertion | Domain object's lifecycle owner |
| Invalidated | A specified result/claim/proof/lease is no longer eligible under a named invalidation rule | Does not erase history or necessarily alter parent object's lifecycle | Owner of invalidated artifact/state |
| Deleted | A defined logical record/content reference has been removed under a stated deletion operation | Does not prove all replicas, backups, exports or derivatives are physically erased | Deleting subsystem / Storage |
| Forgotten | D canonical Memory lifecycle state after governed Forget criterion; ordinary content access is denied and cleanup tracked | Does not itself prove global completion or physical erasure | D, gated by I policy |
| Purged | A specified physical retention target has passed its approved erasure criterion with target-scoped evidence | Cannot be claimed from tombstone, suppression, or missing row | Storage/backup operator under I policy |

Chinese terminology:
- Recorded：已记录（持久记录事实），不是“已应用”或“已提交”。
- Applied：已应用（跨越明确的应用边界并具备规定证明）。
- Committed：已提交（所属事务/权威已持久提交）。
- Visible：可见（通过权威可见性机制可供读取）。
- Published：已发布（Storage 发布提交及精确 Receipt 已确认）。
- Acknowledged：已确认/已应答（仅覆盖 ACK 声明的范围）。
- Forgotten：已遗忘（D 的规范生命周期状态，不等于物理擦除）。
- Purged：已清除/物理擦除（特定目标达到批准的擦除标准）。

## 5. Ordering semantics / 顺序语义

Do not define one universal total order among Recorded, Applied, Committed, Visible and Published. Their relationship depends on the operation and authority.

不得为 Recorded、Applied、Committed、Visible、Published 规定全系统通用的全序关系。它们之间的关系取决于具体操作和权威。

Verified constraints from current source:
1. A source/evidence record may be Recorded before any downstream Claim/Memory is committed.
2. A Context delivery ACK is weaker than Applied; Applied requires the G/C/H owner-defined evidence chain and must bind the actual final request boundary where Full Applied is claimed.
3. In the Storage JF-10 candidate, I's COMMIT_WON is an authorization-order decision, not publication. Storage must resolve the same XID and atomically commit VisibilityPointer + PublicationReceipt + outcome + outbox; only after authoritative receipt readback may Storage return PUBLISHED.
4. The visibility pointer is the Storage publication authority. Outbox delivery is notification/reconciliation only.
5. If the result is unknown or in doubt, keep bytes private; do not infer commit/abort from timeout, row absence, stale replica, missing ACK or process death.

Items 2–5 are owner-specific contracts/candidates and must not be promoted to a universal domain transition machine.

## 6. State machine requirements / 状态机要求

Only entities with genuine independent lifecycle require a state machine. A state machine must name:
- subject type and state dimension;
- initial/terminal states;
- allowed and forbidden transitions;
- preconditions and authority;
- required transition evidence;
- idempotency key and same-key/different-payload behavior;
- failure/unknown semantics;
- recovery and replay behavior;
- supersession/retention behavior.

No new state machine is introduced for every metadata field. State names without a subject type and owner are invalid as normative contracts.

## 7. Blocking issues / 阻塞问题

- **B-STATE-001:** Fact/Claim ADR remains BLOCKED; epistemic status cannot settle object identity.
- **B-STATE-002:** Memory lifecycle and D ForgetOperation phase are distinct; all owner docs and schemas must preserve that split.
- **B-STATE-003:** Applied predicate remains cross-owner OPEN; B cannot define final request proof or G Applied commit.
- **B-STATE-004:** I COMMIT_WON vs Storage Published distinction is critical to JF-10; implementation and conformance NOT VERIFIED.
- **B-STATE-005:** Forgotten vs Deleted vs Purged/global completion remains D/I/Storage split; do not claim physical erasure from logical state.
- **B-STATE-006:** Context/ChangeSet/ContextVersion state transitions need G's exact current Owner contract pin; not yet reconciled here.

## 8. Gate status / 门禁状态

B2 is **IN PROGRESS**. This document establishes a typed vocabulary proposal and records exact Owner boundaries; it does not close Owner-specific state machines or approve the cross-owner Applied/Forget/Storage contract. No universal status enum or production schema is authorized.

B2 **进行中**。本文件建立类型化状态词汇提案并记录 Owner 权威边界，但不关闭 Owner 专属状态机，也不批准跨 Owner Applied/Forget/Storage 契约。不授权通用状态枚举或生产 Schema。
