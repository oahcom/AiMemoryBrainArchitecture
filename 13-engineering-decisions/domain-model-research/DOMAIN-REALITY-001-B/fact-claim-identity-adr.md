# B ADR — Fact / Claim Semantics and Identity Across Memory Versions
# B ADR — Fact / Claim 语义与跨 Memory Version 身份

- ADR: B-ADR-FACT-CLAIM-001
- Status: DECISION REQUEST / CANDIDATE — NOT DECIDED, NOT ACCEPTED, NOT SCHEMA-FROZEN
- Domain authority: B
- Required consumers: D (canonical lifecycle/versioning), E (compiler derivation), F (runtime retrieval), G (Context references), Storage (immutable persistence), A (contract registry)
- Date: 2026-11-17

## 1. Problem statement / 问题陈述

The current main domain overview marks Fact as a qualified Claim and labels the decision DECIDED. The bilingual domain guide and A's current integration assessment retain Fact/Claim as ADR-BLOCKED and prohibit downstream schema freeze. The core entity schema calls the object “Claim (canonical Fact/Claim object)”, assigns a required `claim_id` described as stable under a declared identity policy, and stores `ClaimSnapshot[]` inside immutable MemoryVersion. The identity policy across Memory Versions is not specified.

当前 main 领域总览将 Fact 定义为带限定的 Claim，并标记为 DECIDED。双语领域指南和 A 当前集成评估仍将 Fact/Claim 保留为 ADR-BLOCKED，并禁止下游 Schema 冻结。核心实体 Schema 将对象称为“Claim（规范 Fact/Claim 对象）”，要求 `claim_id`，但其稳定性依赖尚未声明的身份策略，并在不可变 MemoryVersion 内存储 `ClaimSnapshot[]`。跨 Memory Version 的身份策略尚未定义。

This ADR separates two questions that must not be collapsed:
1. **Conceptual semantics:** whether “Fact” is a separate domain object or a qualified Claim.
2. **Identity/version semantics:** whether a Claim keeps one stable identity across Memory Versions, or each snapshot is version-local with explicit lineage.

本 ADR 将两个不得混为一谈的问题分开：
1. **概念语义：**“Fact”是独立领域对象，还是带限定的 Claim。
2. **身份/版本语义：**Claim 是否跨 Memory Version 保持同一稳定身份，还是每个 Snapshot 都是版本局部对象并通过显式谱系关联。

## 2. Exact source evidence / 精确来源证据

| Source / 来源 | Exact main Blob / 精确 main Blob | Relevant statement / 相关陈述 |
|---|---|---|
| `02-domain-model/domain-model-overview.md` | `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` | Fact/Claim decision is marked DECIDED; Memory contains multiple Claims; epistemic and temporal qualifications belong to each Claim. / Fact/Claim 决策被标记为 DECIDED；Memory 可包含多个 Claim；认知和时间限定属于各 Claim。 |
| `02-domain-model/core-entities.md` | `8cb5a674eec8eac1f3c4d83c400dc08d00166f23` | Claim has required claim_id; MemoryVersion stores immutable ClaimSnapshot[]; identity policy remains referenced but unspecified. / Claim 要求 claim_id；MemoryVersion 存储不可变 ClaimSnapshot[]；身份策略虽被引用但尚未定义。 |
| `02-domain-model/epistemic-and-temporal-semantics.md` | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` | Epistemic status is orthogonal to lifecycle, confidence, relevance, trust and evidence strength. / 认知状态与生命周期、置信度、相关性、信任和证据强度正交。 |
| `02-domain-model/lifecycle-model.md` | `81c48c928cb5f9c76ca29d493fbd9479079e62f7` | Claim epistemic lifecycle is separate from Memory lifecycle; corrections/retractions preserve history. / Claim 认知生命周期独立于 Memory 生命周期；更正/撤回保留历史。 |
| `02-domain-model/relationships-and-provenance.md` | `e762f84c59f69de7a44baad2123aed46e1ffea16` | Claims participate in typed Relations and evidence/provenance lineage. / Claim 参与类型化 Relation 以及 Evidence/Provenance 谱系。 |
| B research conflict register | `a3cc523b67c2433a8e53bdb0ebfff121705618c6` | B-CONFLICT-001 / 006 remain BLOCKING / HIGH; no closure claimed. / B-CONFLICT-001 / 006 仍为 BLOCKING / HIGH，未宣称关闭。 |
| A assessment | PR #53 and current B baseline audit | Fact/Claim ADR remains a blocker to B2/B3 and dependent schema freeze. / Fact/Claim ADR 仍阻塞 B2/B3 及依赖它的 Schema 冻结。 |

The five main-domain Blob SHAs above were re-fetched from current main during this audit. Their file contents match the recorded pins.

以上五个 main 领域文件 Blob SHA 已在本次审计中从当前 main 重新读取，文件内容与登记 Pin 一致。

## 3. Non-negotiable invariants / 不可妥协的不变量

Regardless of the selected option:

无论选择何种方案，均必须满足：

1. A Claim is a proposition, not a guarantee of truth. A Memory is a retained knowledge asset, not a truth guarantee.
2. Epistemic status (Observed/Reported/Inferred/Verified/Disputed/Retracted), Memory lifecycle, valid time, confidence, relevance, source trust and Evidence strength remain orthogonal dimensions.
3. Intent, plan, prediction and pending action are not completed outcomes without outcome Evidence.
4. A Claim's subject, predicate, object, polarity, qualifiers, scope and temporal meaning must be explicit and typed; free-text paraphrase is not a canonical identity.
5. Claim correction/retraction never silently rewrites historical MemoryVersion snapshots.
6. Evidence and Provenance remain separately addressable; evidence availability/retention does not silently rewrite the historical assertion that it existed.
7. MemoryVersion remains immutable. Current pointer advancement and version persistence are governed by D/Storage, not by this ADR.
8. No schema is frozen by a B candidate or by absence of Owner objection.

1. Claim 是命题，不保证为真。Memory 是保留的知识资产，不保证为真。
2. 认知状态（Observed/Reported/Inferred/Verified/Disputed/Retracted）、Memory 生命周期、有效时间、置信度、相关性、来源信任和 Evidence 强度保持正交。
3. 没有结果 Evidence 时，意图、计划、预测和待处理动作不得视为已完成结果。
4. Claim 的 Subject、Predicate、Object、Polarity、Qualifiers、Scope 和时间语义必须显式且类型化；自由文本改写不是规范身份。
5. Claim 更正/撤回不得静默改写历史 MemoryVersion Snapshot。
6. Evidence 与 Provenance 保持独立寻址；Evidence 可用性/保留变化不得静默改写其曾存在这一历史断言。
7. MemoryVersion 保持不可变。当前指针推进和版本持久化由 D/Storage 管辖，不由本 ADR 决定。
8. B 候选或 Owner 未反对，不构成 Schema 冻结。

## 4. Conceptual alternatives / 概念方案

### C1 — Fact is a separate canonical entity

Fact has an independent identity and lifecycle; Claim is a broader proposition or draft/qualified assertion.

Advantages: may distinguish a proposition from an accepted factual record. Disadvantages: creates a second semantic object adjacent to Claim, requires a precise admission/verification threshold, and risks treating “Fact” as truth by name. It can duplicate epistemic status and Memory lifecycle.

方案优点：可能区分一般命题与被接纳的事实记录。缺点：在 Claim 旁增加第二个语义对象，需要精确定义准入/验证门槛，并有因名称而把 Fact 误解为真理的风险；也可能重复认知状态和 Memory 生命周期。

### C2 — Fact is a qualified Claim (candidate recommendation)

There is one canonical proposition concept: Claim. “Fact” is either a human-facing label for a Claim satisfying a declared epistemic predicate, or a view/query category; it is not a second identity-bearing entity.

Advantages: preserves one proposition model; supports Reported, Inferred, Disputed and Retracted propositions without implying truth. Disadvantages: requires careful language to avoid treating Fact as a synonym for Verified; user-facing “fact” terminology may need qualification.

方案优点：保留单一命题模型；可容纳 Reported、Inferred、Disputed、Retracted 命题而不暗示真理。缺点：必须谨慎定义术语，避免把 Fact 当作 Verified 的同义词；面向用户的“事实”表述可能需要限定。

**B recommendation:** C2, subject to explicit ADR acceptance and consumer review. This is a recommendation, not a decision or freeze.

**B 建议：**倾向 C2，但须经明确 ADR 验收和消费者复审。这是建议，不是决定或冻结。

## 5. Identity/version alternatives / 身份/版本方案

### I1 — Stable Claim identity + immutable Claim revisions/snapshots (candidate recommendation)

- `claim_id` identifies the continuing proposition lineage within its declared identity scope.
- Each immutable MemoryVersion embeds a `ClaimSnapshot` containing `claim_id`, a version-local `claim_revision_id` (or equivalent immutable revision identity), canonical proposition payload, epistemic status and temporal/evidence references as of that MemoryVersion.
- A semantic change that changes proposition identity (for example, subject/predicate/object/polarity beyond declared correction rules) creates a new `claim_id` and explicit predecessor/successor lineage. A non-identity-changing annotation/epistemic update may create a new revision under the same `claim_id`.
- A Claim may be referenced by multiple MemoryVersions only if the identity and snapshot semantics are explicit and no historical snapshot is overwritten.

优点：稳定引用和跨版本追踪；历史 Snapshot 不变；更正可明确区分同一命题的修订与新命题。成本：需要 Claim Identity Policy、revision identity、change classification、concurrency and retention rules.

### I2 — Version-local ClaimSnapshot identity

- Every MemoryVersion owns its own ClaimSnapshot identity.
- Cross-version continuity is represented only by explicit `supersedes_claim_snapshot_ref`, `derived_from_claim_snapshot_ref` or correction lineage.
- No globally stable `claim_id` is implied unless a separate identity service/object is later approved.

优点：版本边界清晰，较少跨版本共享身份语义。成本：查询同一持续命题需要遍历 lineage；跨 Memory、Context、Relation 和 Evidence 的引用复杂度增加。

### I3 — Independent canonical Claim object plus MemoryVersion references

- Claim is independently persisted and versioned as a canonical object.
- MemoryVersion stores references to exact Claim revision IDs rather than embedding snapshots.
- Storage and D must define atomic consistency between MemoryVersion commit and Claim revision/reference updates.

优点：Claim 可独立寻址、共享和版本化。成本：增加独立生命周期、并发写入、事务边界、Forget 传播、引用完整性及存储复杂度；可能超出当前需求。

**B recommendation:** I1 as the least-complex candidate consistent with the current embedded immutable `ClaimSnapshot[]` model. I2 remains a viable alternative if D/E demonstrate that stable Claim identity creates unacceptable coupling. I3 is not recommended without a demonstrated independent lifecycle/use case.

**B 建议：**优先 I1，作为与当前嵌入式不可变 `ClaimSnapshot[]` 模型一致且复杂度最低的候选。如果 D/E 证明稳定 Claim 身份带来不可接受的耦合，I2 仍可选。除非证明存在独立生命周期/使用场景，否则不建议 I3。

## 6. Decision matrix / 决策矩阵

| Criterion / 评估维度 | C1 separate Fact / C1 独立 Fact | C2 Fact=qualified Claim / C2 Fact 为限定 Claim | I1 stable identity + snapshots / I1 稳定身份+快照 | I2 version-local snapshots / I2 版本局部快照 | I3 independent Claim store / I3 独立 Claim 存储 |
|---|---|---|---|---|---|
| Single proposition vocabulary / 单一命题词汇 | No / 否 | Yes / 是 | Yes / 是 | Yes / 是 | Yes / 是 |
| Avoid “Fact means true” hazard / 避免 Fact 名称暗示真理 | Weak / 较弱 | Strong if qualified / 限定清晰时较强 | Strong / 较强 | Strong / 较强 | Strong / 较强 |
| Historical immutability / 历史不可变性 | Possible / 可实现 | Possible / 可实现 | Native / 原生支持 | Native / 原生支持 | Requires cross-object transaction / 需要跨对象事务 |
| Cross-version reference simplicity / 跨版本引用简洁性 | N/A / 不适用 | N/A / 不适用 | Strong / 较强 | Lineage traversal / 需要遍历谱系 | Strong / 较强 |
| Storage/Forget complexity / Storage 与 Forget 复杂度 | Higher / 较高 | Lowest / 最低 | Medium / 中等 | Low/medium / 较低至中等 | Highest / 最高 |
| Fit to current core schema / 与当前核心 Schema 的适配 | Requires changes / 需要修改 | Fits terminology intent / 符合术语意图 | Fits snapshots with added revision semantics / 适配 Snapshot，但需增加 Revision 语义 | Requires claim_id policy change / 需要修改 claim_id 策略 | Requires major redesign / 需要重大重构 |
| Current status / 当前状态 | Not selected / 未选择 | Recommended candidate / 推荐候选 | Recommended candidate / 推荐候选 | Alternative / 替代方案 | Deferred / 延后 |

## 7. Required decisions by authority / 各权威必须作出的决定

| Owner / 责任方 | Explicit question / 明确问题 | Acceptance evidence required / 所需验收证据 |
|---|---|---|
| B | C2 vs C1; I1 vs I2 vs I3; define identity-changing vs non-identity-changing Claim updates. / 选择 C2/C1、I1/I2/I3；定义改变 Claim 身份与不改变身份的更新。 | B-authored explicit ADR disposition with exact version and examples. / 由 B 明确作出 ADR 裁决，包含精确版本和示例。 |
| D | Does MemoryVersion own the authoritative immutable ClaimSnapshot set? How do correction, retraction, supersession and Forget affect snapshot identity/lineage? / MemoryVersion 是否拥有权威不可变 ClaimSnapshot 集？更正、撤回、替代和 Forget 如何影响 Snapshot 身份/谱系？ | D exact-version acceptance or enumerated exceptions; preserve lifecycle/Forget race semantics. / D 精确版本验收或列明例外；保留生命周期/Forget 竞态语义。 |
| E | Can compiler output preserve stable Claim identity/revision without inferring truth? How are re-extraction, deduplication and provenance bound? / Compiler 输出能否在不推断真理的前提下保留稳定 Claim 身份/修订？重新抽取、去重和 Provenance 如何绑定？ | E exact-version producer contract acceptance and fixtures. / E 对精确版本生产契约及 Fixtures 的验收。 |
| F | How do retrieval and conflict detection group Claim revisions without collapsing different scope/time/modality? / 检索和冲突检测如何对 Claim 修订分组，同时不合并不同 Scope/时间/模态？ | F exact-version consumer acceptance; ranking cannot alter canonical identity/status. / F 精确版本消费者验收；Ranking 不得改变规范身份/状态。 |
| G | Are ContextEntry references to MemoryVersion only, or can they address ClaimSnapshot/revision? What does a ContextVersion freeze? / ContextEntry 只能引用 MemoryVersion，还是也可引用 ClaimSnapshot/Revision？ContextVersion 冻结什么？ | G exact-version schema/consumer acceptance. / G 对精确版本 Schema/消费者契约的验收。 |
| Storage | Can immutable snapshots and identity lineage be committed with the owning MemoryVersion/current pointer without a new independent Claim transaction? / 能否在不引入独立 Claim 事务的情况下，将不可变 Snapshot 与身份谱系和所属 MemoryVersion/Current Pointer 一并提交？ | Storage exact-version interface and atomicity acceptance; no L4 claim without engine evidence. / Storage 精确版本接口与原子性验收；无引擎证据不得声称 L4 完成。 |
| A | Register accepted ADR and exact consumer pins; maintain gate impact. / 登记已接受 ADR 和精确消费者 Pin，并维护门禁影响。 | A registry update after Owner decisions, not before. / A 应在 Owner 决策后更新 Registry，不得提前登记。 |

## 8. Required examples / 必须验证的例子

1. Same proposition repeated in a new MemoryVersion with only a changed display label: stable `claim_id` under I1; new snapshot/revision, no semantic identity change. / 同一命题仅更改显示标签并出现在新的 MemoryVersion 中：按 I1 保持 `claim_id` 稳定；创建新的 Snapshot/Revision，但不改变语义身份。
2. Same proposition gains new Evidence and changes Reported → Verified: same `claim_id` only if the proposition itself is unchanged; new immutable revision/snapshot; verification method and Evidence required. / 同一命题获得新 Evidence，状态从 Reported 变为 Verified：只有命题本身未改变时才保持相同 `claim_id`；必须创建新的不可变 Revision/Snapshot，并提供验证方法和 Evidence。
3. Subject changes from Entity A to Entity B: new `claim_id` unless a formally approved identity rule says otherwise; explicit lineage. / Subject 从 Entity A 变为 Entity B：除非正式批准的身份规则另有规定，否则必须创建新的 `claim_id` 并建立显式谱系。
4. Predicate polarity changes from positive to negative: distinct proposition identity; never overwrite prior snapshot. / Predicate 极性从肯定变为否定：属于不同命题身份；不得覆盖先前 Snapshot。
5. Valid Time is corrected while Recorded At remains later: preserve both temporal histories and explain correction provenance. / 修正 Valid Time，但 Recorded At 仍较晚：必须保留两条时间历史，并说明修正 Provenance。
6. Claim is Disputed then Retracted: retain prior status/snapshot; retraction authority/reason and conflicting position references required. / Claim 先变为 Disputed 再变为 Retracted：保留先前状态/Snapshot；必须记录撤回权威、原因及冲突立场引用。
7. One Claim appears in two MemoryVersions: both snapshots remain independently immutable; no mutable shared object can retroactively change either version. / 同一 Claim 出现在两个 MemoryVersion 中：两个 Snapshot 均须独立保持不可变；不得通过可变共享对象追溯性修改任一版本。
8. Forget one Memory lineage: D/I/Storage decide target inventory and erasure; B's Claim identity does not authorize retaining reconstructive forgotten content in a shared Claim object. / 对一个 Memory 谱系执行 Forget：由 D/I/Storage 决定目标清单和擦除；B 的 Claim 身份规则不授权在共享 Claim 对象中保留可重建的已遗忘内容。

## 9. Complexity and risk assessment / 复杂度与风险评估

- C1 creates semantic duplication and an additional truth-admission threshold: HIGH semantic complexity.
- C2 + I1 retains one proposition vocabulary and local immutable snapshots: MEDIUM complexity; requires explicit revision/identity policy.
- C2 + I2 has simpler local persistence but higher cross-version lineage/query complexity: MEDIUM complexity.
- C2 + I3 adds cross-object transactional and Forget propagation coupling: HIGH to VERY HIGH complexity.
- The dominant risk is not the number of fields. It is identity ambiguity causing false merges, false splits, evidence misattribution, stale Context references, or resurrection after Forget.

- C1 会造成语义重复并增加事实准入门槛：语义复杂度 HIGH。
- C2 + I1 保留单一命题词汇和局部不可变 Snapshot：复杂度 MEDIUM，但需要明确修订/身份策略。
- C2 + I2 持久化较简单，但跨版本谱系/查询复杂度较高：复杂度 MEDIUM。
- C2 + I3 增加跨对象事务与 Forget 传播耦合：复杂度 HIGH 至 VERY HIGH。
- 主导风险不是字段数量，而是身份歧义导致错误合并/拆分、Evidence 错误归属、Context 引用过期或 Forget 后复活。

## 10. Interim rule and gate / 临时规则与门禁

Until explicit decisions and consumer acceptances are recorded:

在明确决定及消费者验收记录完成前：

- Adopt the Owner-selected semantic direction in §12: Claim is an attributable proposition thread; Fact is a separately identified, governed attestation object (Option A); ClaimRef is stable and each assertion state is an immutable ClaimRevision (I1).
- This is a semantic decision only. It does not freeze field-level canonical schema, ID allocation/commit APIs, DDL, persistence layout, or BMCP wire payloads.
- Keep E CandidateProposition/ExtractionIR neutral and pre-canonical. E MUST NOT mint ClaimRef, ClaimRevisionRef, FactRef or FactRevisionRef; D remains the canonical identity/lifecycle authority.
- Keep exact schema mapping, D/I/Storage interfaces, migration/compatibility and consumer conformance blocked until the B ADR §8 conditions are evidenced.
- Do not issue JSON Schema, database migration, Runtime implementation authorization or downstream contract freeze based on this semantic selection alone.
- Treat ambiguous identity classification as unresolved; fail closed and never deduplicate or merge by text similarity alone.

- 暂以 `Claim` 作为工作命题术语；不创建独立 Fact 实体。
- `claim_id` 身份策略继续 OPEN；不得假定全局稳定身份或版本局部身份。
- 保持 `ClaimSnapshot` 不可变，不修改持久化 Schema。
- 不得基于本候选发布 JSON Schema、数据库迁移、实现授权或下游契约冻结。
- 身份语义不明确的 Claim 引用视为未解决；不得仅凭文本相似度去重或合并。

**ADR status:** Owner semantic direction selected (Option A + I1) by §12. The B ADR itself remains **ADR-BLOCKED / NOT ACCEPTED / NOT SCHEMA-FROZEN** until its §8 consumer mapping, migration/compatibility and conformance conditions are exact-version pinned. B2/B3 remain OPEN; B4 remains NOT READY. No schema approval is inferred from this semantic selection.

**ADR 状态：**Owner 已在 §12 选择语义方向（Option A + I1）。B ADR 本身仍为 **ADR-BLOCKED / NOT ACCEPTED / NOT SCHEMA-FROZEN**，直至 §8 消费者映射、迁移/兼容和符合性条件均完成精确版本 Pin。B2/B3 保持 OPEN；B4 仍 NOT READY。本语义选择不构成 Schema 批准。


## 11. Current B Owner ADR reconciliation — 2026-11-18 / 当前 B Owner ADR 对账 — 2026-11-18

**Supersession notice / 替代说明.** The earlier recommendation in §4 for C2 (Fact as a qualified Claim) is superseded as the *current B-preferred candidate* by the newer B Owner branch artifacts below. It was never approved and must not be treated as a decision. The current B Owner recommendation is Option A (separate Fact attestation object and Claim proposition thread), still **ADR-BLOCKED / NOT APPROVED** pending formal Architecture Governance decision. This update changes the recommendation record only; it does not create an approved canonical model.

**替代说明。** §4 中此前倾向 C2（Fact 是限定 Claim）的建议，现已被下列较新的 B Owner 分支工件取代，作为“当前 B 优先候选”。此前建议从未获批，不得视为决策。当前 B Owner 推荐 Option A（Fact 独立 Attestation 对象，Claim 为命题线程），但仍 **ADR-BLOCKED / NOT APPROVED**，等待正式 Architecture Governance 决议。本次仅更新建议记录，不创建已批准的规范模型。

### 11.1 Exact current B Owner evidence / 当前 B Owner 精确证据

| Artifact / 工件 | Branch / 分支 | Exact Blob SHA / 精确 Blob SHA | Status / 状态 |
|---|---|---|---|
| `02-domain-model/ADR-001-fact-claim-semantics.md` | `session-b-domain-model-phase3` @ `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | `a1024938ff5baba069cf128c69496a44e143330c` | ADR-BLOCKED; B recommends Option A; Architecture Governance authority/approval not recorded |
| `02-domain-model/adr/ADR-001-fact-claim-canonical-model.md` | same | `df77e4a93cb8fef689ae7c828888d960cbf381d6` | ADR-BLOCKED; Option A preferred candidate; Option B requires explicit I-04/P-04 amendment |
| `02-domain-model/fact-claim-consumer-mapping.md` | same | `dd45a37199c9b69ab6b68f65e051a484a04691d4` | CANDIDATE; canonical Fact/Claim identity portions blocked |
| `02-domain-model/phase-3.6-b-owner-formal-actor-scope-environment-type-mapping-confirmation.md` | same | `3a1e77889cd9a90cd5822d9f0cb3437880868706` | B-approved typed-reference semantics only; explicitly does not approve Fact/Claim ADR |

### 11.2 Current option mapping and boundaries / 当前方案映射与边界

The current B Owner ADR's Option A corresponds to this research ADR's earlier C1: Claim is an attributable proposition thread with immutable ClaimRevision; Fact is a separately addressable, evidence-backed attestation/adjudication object with FactRevision, exact ClaimRevisionRef(s), authorized attestor, method/version, evidence, Scope, validity and decision history. Option B corresponds to earlier C2: Fact is a qualification/view of an exact ClaimRevision without separate identity. The current B Owner recommendation prefers Option A because it preserves I-04/P-04 and provides a distinct auditable attestation boundary; it remains conditional on a concrete product attestation use case and D/I/governance boundary agreement.

当前 B Owner ADR 的 Option A 对应本研究 ADR 早先的 C1：Claim 是带不可变 ClaimRevision 的可归属命题线程；Fact 是独立可寻址、由 Evidence 支持的 Attestation/Adjudication 对象，拥有 FactRevision、精确 ClaimRevisionRef、授权 Attestor、Method/Version、Evidence、Scope、Validity 和决策历史。Option B 对应早先的 C2：Fact 是精确 ClaimRevision 的限定/视图，不具有独立身份。当前 B Owner 推荐 Option A，因为它保留 I-04/P-04 并提供独立可审计的 Attestation 边界；但仍以存在真实产品 Attestation 用例，以及 D/I/Governance 边界达成一致为条件。

The current B Owner ADR also proposes (not freezes) stable ClaimRef + immutable ClaimRevisionRef, exact revision-pinned Evidence/Provenance, and ConflictSet over exact ClaimRevisionRefs. D owns canonical identity allocation, persistence, revision commit and ConflictSet lifecycle/commit shape after approval. E remains neutral CandidateProposition/ExtractionIR and may not mint canonical ClaimRef/FactRef. F/G may consume only candidate-neutral or exact version-pinned references while blocked. H wire fields remain H-owned and unfrozen. No Fact/Claim schema, DDL, API or wire contract may be frozen.

当前 B Owner ADR 还提出（但未冻结）稳定 ClaimRef + 不可变 ClaimRevisionRef、精确版本绑定的 Evidence/Provenance，以及基于精确 ClaimRevisionRef 的 ConflictSet。批准后，D 负责规范身份分配、持久化、Revision Commit 和 ConflictSet 生命周期/Commit 形态。E 必须继续使用中立 CandidateProposition/ExtractionIR，不得创建规范 ClaimRef/FactRef。阻塞期间 F/G 只能消费中立候选或精确版本绑定引用。H Wire 字段仍由 H 负责且未冻结。不得冻结 Fact/Claim Schema、DDL、API 或 Wire 契约。

### 11.3 Governance blocker / 治理阻塞

Main I-04 (Blob `33b037318e459ebb73bea33b3186f31a41d5dcfe`) and P-04 (Blob `192e6ba6e9287792a02b679dda0d391844270228`) normatively distinguish Fact from Claim as distinct domain concepts/objects. Main domain overview Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` still describes Fact as a qualified interpretation of Claim, while both current bilingual guides (EN Blob `8a19cebacf5aefb0aded5fdbfeaff406291a5cf1`; ZH Blob `a9f53a453aec25c47c58c4aea75adc43c83028d3`) explicitly retain ADR-BLOCKED and prohibit downstream schema freeze. Main terminology Blob `9b287ebe027ae01128baf164952ce15aad050638` still defines “Fact / Claim” jointly. These source-level inconsistencies remain unresolved.

Main I-04（Blob `33b037318e459ebb73bea33b3186f31a41d5dcfe`）和 P-04（Blob `192e6ba6e9287792a02b679dda0d391844270228`）规范性地区分 Fact 与 Claim，视为不同领域概念/对象。Main Domain Overview Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` 仍将 Fact 描述为 Claim 的限定解释；而当前中英文指南（EN Blob `8a19cebacf5aefb0aded5fdbfeaff406291a5cf1`；ZH Blob `a9f53a453aec25c47c58c4aea75adc43c83028d3`）明确保留 ADR-BLOCKED，并禁止下游 Schema 冻结。Main Terminology Blob `9b287ebe027ae01128baf164952ce15aad050638` 仍将 “Fact / Claim” 合并定义。这些来源层面的不一致仍未解决。

Issue #43 remains OPEN and preserves the Fact/Claim schema/consumer blocker. Issue #5 remains OPEN for I36 governance approvals; it is a separate I identity-trust governance dependency and must not be misrepresented as the missing Architecture Governance decision authority for this ADR. An Owner semantic decision is now recorded in §12 and PR #438; it selects Option A + I1 only. It does not constitute B/D/E/F/G/H/I/Storage consumer acceptance, does not satisfy the B ADR §8 migration/conformance checklist, and does not approve schema/API/DDL/wire fields. Therefore the B ADR remains BLOCKED for schema freeze and implementation mapping.

Issue #43 仍 OPEN，并保留 Fact/Claim Schema/消费者阻塞。Issue #5 仍 OPEN，负责 I36 治理批准；它是独立的 I 身份信任治理依赖，不得误称为本 ADR 缺失的 Architecture Governance 决策权威。§12 和 PR #438 现已记录 Owner 语义决策，仅选择 Option A + I1。该决策不等于 B/D/E/F/G/H/I/Storage 消费者验收，不满足 B ADR §8 的迁移/符合性清单，也不批准 Schema/API/DDL/Wire 字段。因此 B ADR 对 Schema 冻结和实现映射仍保持 BLOCKED。

## 12. Owner semantic selection — 2026-11-21 / Owner 语义选择 — 2026-11-21

**Decision record:** `OWNER-DECISION-FACT-CLAIM-001`, PR #438, head `60fb3a6a36bcd2ebe9197e4a1c8d24302b34f168` (Draft / not merged at this ADR revision).

**Selected semantic direction:** Option A + I1.

- Claim is an attributable proposition thread; ClaimRevision is an immutable assertion state under stable ClaimRef.
- Fact is a separately identified, governed attestation/adjudication thread; FactRevision is immutable and references exact ClaimRevisionRef(s), Evidence/Provenance, Scope, authorized attestor, method/version, applicable I authorization, temporal context and correction/revocation lineage.
- A Claim may exist without a Fact. A Verified Claim does not automatically create a Fact. Confidence does not mint Fact or canonical identity.
- D owns canonical identity allocation, lifecycle, revision commit and ConflictSet lifecycle. I owns Principal/attestor authorization, PermissionEpoch, revocation, retention and global Forget policy. D/I retain their respective Forget Fence and global completion boundaries.
- E remains neutral CandidateProposition/ExtractionIR and may submit proposals only; it cannot mint canonical IDs or infer Fact from extraction confidence. F/G consume exact revision-pinned references. H may carry opaque references but owns and has not frozen wire representation.

**Explicit boundary:** this selection resolves the semantic direction only. B-ADR-FACT-CLAIM-001 remains ADR-BLOCKED for canonical schema freeze, field mapping, DDL, API, migrations and Runtime implementation until the §8 checklist is complete: exact B/D/E/F/G/H/I/Storage consumer mapping and acceptance, migration/compatibility plan, conformance scenarios and source-version pins. This addendum does not claim B Owner sign-off on behalf of B, does not close Issue #43, and does not change Issue #7's `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`.

**决策记录：**`OWNER-DECISION-FACT-CLAIM-001`，PR #438，Head `60fb3a6a36bcd2ebe9197e4a1c8d24302b34f168`（本 ADR 修订时仍为 Draft / 未合并）。

**选择的语义方向：**Option A + I1。

- Claim 是可归属的命题线程；ClaimRevision 是稳定 ClaimRef 下的不可变断言状态。
- Fact 是独立标识、受治理的 Attestation/Adjudication 线程；FactRevision 不可变，并引用精确 ClaimRevisionRef、Evidence/Provenance、Scope、授权 Attestor、Method/Version、适用的 I 授权、时间上下文以及更正/撤销谱系。
- Claim 可以没有 Fact。Verified Claim 不会自动生成 Fact。Confidence 不会签发 Fact 或规范身份。
- D 负责规范身份分配、生命周期、Revision Commit 和 ConflictSet 生命周期。I 负责 Principal/Attestor 授权、PermissionEpoch、撤销、保留和 Global Forget Policy。D/I 保留各自的 Forget Fence 和全局完成边界。
- E 继续使用中立 CandidateProposition/ExtractionIR，只能提交提案；不得签发规范 ID，也不得从抽取置信度推导 Fact。F/G 只消费精确版本绑定引用。H 可以传递不透明引用，但 Wire 表示仍归 H 所有且尚未冻结。

**明确边界：**本选择只解决语义方向。B-ADR-FACT-CLAIM-001 对 Canonical Schema 冻结、字段映射、DDL、API、迁移和 Runtime 实施仍为 ADR-BLOCKED，直至 §8 清单完成：B/D/E/F/G/H/I/Storage 精确消费者映射与验收、迁移/兼容计划、符合性场景及来源版本 Pin。本补充不代替 B Owner 签字，不关闭 Issue #43，也不改变 Issue #7 的 `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`。
