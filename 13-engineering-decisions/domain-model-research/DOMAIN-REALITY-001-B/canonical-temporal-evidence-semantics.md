# Canonical Temporal, Evidence and Provenance Semantics
# 规范时间、证据与来源追溯语义

- ID: B-TEMP-001
- Status: CANDIDATE CONSOLIDATION; core distinctions DECIDED in source; uncertain-time representation OPEN
- Sources: epistemic/temporal Blob 8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7; core entities Blob 8cb5a674eec8eac1f3c4d83c400dc08d00166f23; relationships/provenance Blob e762f84c59f69de7a44baad2123aed46e1ffea16; D commit/cursor Blob 4688a0ca487bf4d853c7f0220408abe8d743d159.

## 1. Time dimensions / 时间维度

| Canonical term | 中文 | Meaning | Authority / source of truth | Mutation |
|---|---|---|---|---|
| Occurred At / Event Time | 发生时间 / 事件时间 | When the represented occurrence happened; may be unknown, approximate or source-reported | Source event/observer evidence; B defines meaning, C/E preserve source semantics | Immutable for a captured event; correction is a new assertion/revision with provenance |
| Observed At | 观察时间 | When an observer actually observed a state/phenomenon | Observer/source evidence; Evidence owner captures | Immutable per observation |
| Recorded At | 记录时间 | When Brain durably accepted/recorded the information | Owning durable acceptance boundary | Immutable; replay preserves original and adds replay metadata |
| Valid From / Valid Until | 有效起始 / 有效截止 | Interval in which a Claim/Relation is asserted to hold in the represented world | Claim/Relation assertion and its evidence | New assertion/revision; do not rewrite history silently |
| Transaction Time | 事务时间 | When a fact/version became part of authoritative persisted history | Storage/canonical commit authority | System-assigned; immutable per committed version |
| Created At | 创建时间 | Creation time of a particular record/aggregate/version | Owner's creation event / authoritative store | Immutable for that record |
| Updated At | 更新时间 | Time the current mutable pointer/descriptor was last advanced | Owner's current-state authority | Changes only on accepted update; not a substitute for immutable version timestamps |
| Superseded At | 被替代时间 | Time a successor took over current-use role | Lifecycle owner and successor evidence | Append-only transition time |
| Expired At | 到期时间 | Policy/validity expiration point, not necessarily deletion | Owning policy/state machine | Derived or explicit; preserve source and policy basis |
| Forgotten At | 遗忘时间 | Time governed Forget lifecycle transition/effective suppression event is recorded | D lifecycle/fence authority, gated by I criterion | Immutable event time; does not prove physical erasure |
| Deleted At | 删除时间 | Time a defined logical deletion action is committed | Deleting subsystem / Storage | Immutable deletion evidence; deletion scope must be explicit |
| Purged At | 物理清除时间 | Time a named physical target meets approved purge criterion | Storage/backup operator under I policy | Immutable target-scoped proof; never inferred from missing data |

### Chinese time-field definition mirror / 中文时间字段定义对照

| Canonical term | Meaning / 中文语义 | Authority and mutation / 权威与变更规则 |
|---|---|---|
| Occurred At / Event Time | 所表示的事件实际发生的时间；可能未知、近似或仅由来源报告。 | 以来源事件/观察证据为准；捕获后不可变。更正必须创建带 Provenance 的新断言/Revision。 |
| Observed At | 观察者实际观察到某个状态/现象的时间。 | 由观察者/来源 Evidence 支持；每次 Observation 独立且不可变。 |
| Recorded At | Brain 持久接受/记录该信息的时间。 | 由所属持久接受边界确定；不可变。Replay 保留原值并增加 Replay Metadata。 |
| Valid From / Valid Until | Claim/Relation 在所表示世界中被主张成立的时间区间。 | 由 Claim/Relation 断言及 Evidence 支持；更正创建新断言/Revision，不得静默改写历史。 |
| Transaction Time | 某事实/版本进入权威持久历史的时间。 | 由 Storage/规范提交权威分配；每个已提交版本不可变。 |
| Created At | 特定记录/聚合/版本创建的时间。 | 由 Owner 创建事件/权威存储提供；对该记录不可变。 |
| Updated At | 当前可变指针/描述符最近一次推进的时间。 | 由 Owner 当前状态权威控制；仅在接受更新时改变，不替代不可变版本时间。 |
| Superseded At | 后继对象接替当前使用角色的时间。 | 由生命周期 Owner 和后继证据确定；作为追加式转换时间。 |
| Expired At | 策略/有效期到期点，不一定代表删除。 | 由所属策略/状态机确定；可派生或显式记录，但保留来源和策略依据。 |
| Forgotten At | 受治理 Forget 生命周期转换/有效抑制事件被记录的时间。 | 由 D Lifecycle/Fence 权威控制，并受 I 条件约束；不可变，但不证明物理擦除。 |
| Deleted At | 定义明确的逻辑删除动作提交的时间。 | 由删除子系统/Storage 提供不可变删除证据；必须明确删除范围。 |
| Purged At | 指定物理目标满足批准 Purge 标准的时间。 | 由 I 策略下的 Storage/备份操作方提供不可变目标级证明；不得从数据缺失推断。 |

Recorded At, Transaction Time and Created At may coincide in a simple transaction but are not semantically interchangeable. An event can occur before observation and be recorded later. A Claim can be recorded today but be valid from a past interval.

Recorded At、Transaction Time 和 Created At 在简单事务中可能相同，但语义不可互换。事件可能先发生、后被观察、再被记录。Claim 可以今天记录，却从过去某个区间开始有效。

## 2. Precision, uncertainty and nullability / 精度、不确定性与空值

- Unknown is explicit; null/unknown does not mean timeless, all-time or zero.
- Preserve original source phrase, timezone, precision and provenance when relevant.
- Approximate expressions such as “early May” or “around 3pm” must not be normalized into a false exact instant.
- An inferred time carries method/source provenance and uncertainty bounds.
- Current source interval convention is half-open [from, to); open bounds mean unknown/unbounded only where schema explicitly distinguishes them.
- Do not use wall-clock time to fill an unknown Occurred At or Valid Time.

OPEN: proposed TimeValue shape (lower_bound, upper_bound, precision, timezone, certainty, source_text) is not an approved canonical schema. Distinguish unknown, approximate, range, open-ended and not-applicable.

### 中文精度、不确定性与空值规则

- 未知必须显式表达；null/unknown 不表示无时间限制、所有时间或零。
- 相关时保留来源原始短语、时区、精度和 Provenance。
- “五月初”“下午三点左右”等近似表达不得规范化为虚假的精确时间点。
- 推断时间必须携带方法/来源 Provenance 和不确定性边界。
- 当前来源区间约定为半开区间 [from, to)；只有 Schema 明确区分时，开放边界才表示未知/无界。
- 不得使用墙上时钟时间填补未知的 Occurred At 或 Valid Time。

OPEN：提议的 TimeValue 结构（lower_bound、upper_bound、precision、timezone、certainty、source_text）尚不是已批准的规范 Schema。必须区分 unknown、approximate、range、open-ended 和 not-applicable。

## 3. Bitemporal suitability / 双时态适用性

### Decision proposal

Adopt a bitemporal semantic capability for time-qualified Claims/Relations and immutable Memory revisions: retain (a) Valid Time — when the proposition is asserted to hold in the represented world, and (b) Record/Transaction Time — when the Brain's authoritative record/version contained that assertion.

对带时间限定的 Claim/Relation 和不可变 Memory Revision，建议采用双时态语义能力：保留 (a) Valid Time，即命题在所表示世界中成立的时间；(b) Record/Transaction Time，即 Brain 权威记录/版本何时包含该命题。

It supports two distinct questions: “What was true/claimed at world-time T?” and “What did the Brain know/record as of system-time T2?” It does not require a full temporal database engine or bitemporal fields on every entity. Apply only where historical correction, delayed observation, backdated facts, conflict resolution or audit queries justify the cost.

它支持两个不同问题：“世界时间 T 时什么成立/被主张？”以及“系统时间 T2 时 Brain 已知/记录了什么？”这不要求完整时态数据库引擎，也不要求每个实体都携带双时态字段。仅在历史更正、延迟观察、回溯事实、冲突解决或审计查询确有价值时应用。

| Option | Benefit | Cost / limitation | Disposition |
|---|---|---|---|
| Single timestamp | Simple schema/query | Conflates occurrence, validity and knowledge time | REJECTED for canonical Claims/Relations |
| Valid Time only | Models when proposition held | Cannot distinguish late-arriving evidence or historical knowledge | Insufficient alone |
| Record/Transaction Time only | Audits when Brain recorded changes | Cannot model real-world validity intervals | Insufficient alone |
| Bitemporal fields on every object | Uniform query semantics | High write/index/query complexity; unnecessary for immutable identity/config objects | REJECTED as universal rule |
| Selective bitemporal Claims/Relations/revisions | Preserves meaningful history without universal temporal DB | Requires precise field/query contract | RECOMMENDED CANDIDATE |

### 中文双时态方案比较

| 方案 | 收益 | 成本/局限 | 处置 |
|---|---|---|---|
| 单一 Timestamp | Schema 和查询简单。 | 混淆发生时间、有效时间和系统获知时间。 | 对规范 Claim/Relation 拒绝。 |
| 仅 Valid Time | 能表达命题何时成立。 | 无法区分迟到 Evidence 或历史时点系统已知内容。 | 单独使用不足。 |
| 仅 Record/Transaction Time | 能审计 Brain 何时记录变更。 | 无法表达现实世界有效区间。 | 单独使用不足。 |
| 每个对象都使用双时态字段 | 查询语义统一。 | 写入、索引、查询复杂度高；不可变身份/配置对象无此必要。 | 拒绝作为通用规则。 |
| 对 Claim/Relation/Revision 选择性使用双时态 | 保留有意义的历史，又不要求全系统时态数据库。 | 需要精确字段和查询契约。 | 推荐候选。 |

Existing source marks preservation of valid-time and record-time histories separately as DECIDED; the exact bitemporal query contract and transaction-time representation remain CANDIDATE/OPEN and require B + D + Storage confirmation.

现有源规范已将 Valid Time 与 Record Time 历史分别保留标记为 DECIDED；精确双时态查询契约和 Transaction Time 表示仍为 CANDIDATE/OPEN，需 B、D、Storage 确认。

### Complexity and owner impact

- Storage: immutable revision/commit metadata and temporal indexes; no mandate for temporal DB.
- D: lifecycle events and canonical commit cursor are not Valid Time.
- E: preserve source time expressions and transformation provenance.
- F: temporal filters must be scope-safe; relevance cannot rewrite epistemic/temporal truth.
- G: ContextVersion time is not Claim Valid Time or MemoryVersion Transaction Time.
- I: time metadata may expose routines/location patterns and needs policy/retention controls.

### Chinese owner-impact mirror / 中文 Owner 影响对照

- **Storage：** 需要不可变 Revision/Commit Metadata 和时间索引；不强制使用时态数据库。
- **D：** 生命周期事件和规范 Commit Cursor 不等于 Valid Time。
- **E：** 保留来源时间表达式和转换 Provenance。
- **F：** 时间过滤必须满足 Scope 安全；相关性排序不得改写认知/时间真值。
- **G：** ContextVersion 时间不等于 Claim Valid Time 或 MemoryVersion Transaction Time。
- **I：** 时间元数据可能暴露作息/位置模式，必须受策略和保留控制。

## 4. Evidence semantics / 证据语义

Evidence is an independently addressable source-material/observation object used to support, refute or qualify a Claim or Relation. It is not the Claim, not the Source itself, and not a confidence score.

Evidence 是可独立寻址的来源材料/观察对象，用于支持、反驳或限定 Claim 或 Relation。它不是 Claim 本身，不等于 Source，也不是 Confidence 分数。

Current core schema evidence attributes include stable evidence_id; evidence_kind; typed source_ref; optional locator and permitted retained excerpt/content reference; observed_at and immutable recorded_at; collector_ref (ActorRef resolved by the trust boundary); optional integrity digest; evidential role (supports, refutes, qualifies, context_only); Scope references; and availability state.

One Evidence may support multiple Claims; one Claim may have multiple Evidence items. Where role/strength/time/scope differs per Claim, use an explicit Claim–Evidence assessment/link, not a global Evidence property.

一份 Evidence 可以支持多个 Claim；一个 Claim 也可以有多份 Evidence。如果角色/强度/时间/Scope 因 Claim 而异，应建模为显式 Claim–Evidence 评估/关联，而不是 Evidence 的全局属性。

### 中文 Evidence 属性与关系

当前核心 Schema 的 Evidence 属性包括：稳定 evidence_id、evidence_kind、类型化 source_ref、可选 Locator 和允许保留的 Excerpt/Content Ref、observed_at、不可变 recorded_at、由信任边界解析的 collector_ref（ActorRef）、可选完整性摘要、证据角色（supports/refutes/qualifies/context_only）、Scope 引用及可用性状态。

一份 Evidence 可以支持多个 Claim，一个 Claim 可以拥有多份 Evidence。若角色/强度/时间/Scope 因 Claim 而异，应使用显式 Claim–Evidence Assessment/Link，而不是 Evidence 的全局属性。

Evidence 可用性可根据保留/Forget 策略变化，但不得改写“该 Evidence 曾经存在”的历史事实。允许保留的非内容审计元数据不得保留可重建的已遗忘内容。

Evidence availability can change under retention/Forget policy without rewriting the historical fact that the evidence once existed. Permitted non-content audit metadata must not preserve reconstructive forgotten content.

Evidence 可用性可随保留/Forget 策略变化，但不得改写 Evidence 曾经存在的历史事实。允许保留的非内容审计元数据不得保留可重建的已遗忘内容。

## 5. Source vs Evidence vs Provenance / Source、Evidence 与 Provenance

| Concept | Meaning | Example |
|---|---|---|
| Source | Origin from which information is obtained | User message, document, event stream, tool/provider or external record |
| Evidence | Addressable material/observation selected as support/refutation/qualification | Specific document page span or observation |
| Provenance | Trace of how a target assertion/asset was captured or derived from exact inputs and methods | Extraction run + input version digests + method version |

### 中文 Source / Evidence / Provenance 对照

| 概念 | 含义 | 示例 |
|---|---|---|
| Source | 信息取得的原始来源。 | User Message、Document、Event Stream、Tool/Provider 或外部记录。 |
| Evidence | 被选作支持/反驳/限定的可寻址材料或观察。 | 文档中的特定页码/片段，或一条 Observation。 |
| Provenance | 目标断言/资产如何由精确输入和方法捕获/派生的追溯链。 | Extraction Run + 输入版本摘要 + Method Version。 |

A mutable URL alone is not durable Evidence. Source retention may be restricted; preserve only permitted references/metadata and mark unavailable/redacted state accurately. Evidence access is independently authorized and may be stricter than access to derived Memory.

仅有可变 URL 不能构成持久 Evidence。Source 保留可能受限；只能保留允许的引用/元数据，并准确标记不可用/脱敏状态。Evidence 访问必须单独授权，且可能比派生 Memory 的访问更严格。

## 6. Provenance requirements / 溯源要求

For a derived Memory/Claim/Relation, Provenance must make it possible to answer: exact source object and version(s); exact source portion/locator where available; transformation/derivation kind; method/component/model/rule version; derived-at time; input digests; parent provenance references; unavailable/redacted reason where incomplete.

对于派生 Memory/Claim/Relation，Provenance 必须能够回答：精确来源对象及版本；可用时的来源片段/Locator；转换/派生类型；方法/组件/模型/规则版本；派生时间；输入摘要；父级 Provenance 引用；以及信息不完整时的 unavailable/redacted 原因。

对于派生 Memory/Claim/Relation，Provenance 必须能够回答：精确来源对象及版本、可用时的来源片段/定位、转换/派生类型、方法/组件/模型/规则版本、派生时间、输入摘要、父级溯源引用，以及信息不完整时的不可用/脱敏原因。

A method reference explains how an artifact was produced; it does not prove correctness. Do not require metadata the system cannot obtain or verify.

方法引用解释产物如何生成，但不证明其正确性。不得要求系统无法获得或验证的元数据。

方法引用解释产物如何生成，不证明其正确性。不得要求系统无法获得或验证的元数据。

Lineage constraints:
- Source-to-target direction is explicit; do not confuse source and derived target.
- Derived outputs must not masquerade as original Evidence.
- Cycles are not automatically permitted; DAG-vs-limited-cycles remains OPEN in source.
- Multi-generation derivation preserves ancestry and input version references.
- Duplicate copies of one source do not count as independent corroboration.
- Source unavailability/Forget triggers downstream re-evaluation under D/I policy; unavailability does not prove source never existed.

### 中文谱系约束

- Source → Target 方向必须明确；不得混淆 Source 和 Derived Target。
- 派生产物不得伪装成原始 Evidence。
- 不得默认允许循环；DAG 与有限循环策略仍 OPEN。
- 多代派生必须保留祖先谱系和输入版本引用。
- 同一来源的重复副本不能算作独立佐证。
- Source 不可用/Forget 时，按 D/I 策略重新评估下游对象；不可用不证明 Source 从未存在。

## 7. Forget and evidence retention / 遗忘与证据保留

D owns ForgetOperation, ForgetFence and canonical Memory lifecycle transition semantics. I owns authorization, retention, backup/external-copy rules, exceptions and global completion criteria. Storage/backup operators own physical erasure evidence. B defines that Evidence/Provenance links do not override source retention or access rules. Logical suppression, derivative cleanup, physical purge and audit metadata retention are separate facts. A Forget/Deleted/Purged timestamp must name its subject, target scope, authority and proof; no single timestamp stands for all targets.

D 负责 ForgetOperation、ForgetFence 和规范 Memory 生命周期转换语义。I 负责授权、保留、备份/外部副本规则、例外和全局完成条件。Storage/备份操作方负责物理擦除证据。B 规定 Evidence/Provenance 关系不得覆盖来源保留或访问规则。逻辑抑制、派生物清理、物理擦除和审计元数据保留是不同事实。Forget/Deleted/Purged 时间必须注明对象、目标范围、权威和证明；任何单一时间都不能代表所有目标。

## 8. Invariants / 不变量

1. Event Time ≠ Observed At ≠ Recorded At ≠ Valid Time ≠ Transaction Time.
2. Unknown time is not zero, timeless or “always valid”.
3. Valid Time and Record/Transaction Time histories remain distinguishable.
4. Time correction is a new assertion/revision with provenance, not silent overwrite.
5. Evidence is not Confidence; Confidence is method-qualified and cannot verify itself.
6. Evidence role/strength is Claim-relative.
7. Source, Evidence and Provenance are distinct.
8. Derived artifacts preserve exact input/version lineage or explicitly mark what is unavailable.
9. Source unavailability does not imply source nonexistence.
10. Forget/suppression does not imply physical purge; audit metadata is governed separately.

### 中文不变量对照

1. Event Time、Observed At、Recorded At、Valid Time、Transaction Time 彼此不同。
2. 未知时间不等于零、永恒或“始终有效”。
3. Valid Time 与 Record/Transaction Time 历史必须保持可区分。
4. 时间更正必须创建带 Provenance 的新断言/Revision，不得静默覆盖。
5. Evidence 不等于 Confidence；Confidence 必须带方法限定，不能自我验证。
6. Evidence 角色/强度相对于 Claim。
7. Source、Evidence 和 Provenance 是不同概念。
8. 派生产物必须保留精确输入/版本谱系，或明确标记不可获得的信息。
9. Source 不可用不意味着 Source 不存在。
10. Forget/Suppression 不意味着物理 Purge；审计元数据保留另行治理。

## 9. Open decisions / 未决事项

- B-TEMP-001: exact TimeValue encoding for fuzzy/approximate time.
- B-TEMP-002: exact boundary and meaning of Record Time vs Storage Transaction Time.
- B-TEMP-003: whether every Claim/Relation revision is bitemporal or only time-sensitive assertions.
- B-TEMP-004: Claim–Evidence assessment record identity and strength rubric.
- B-TEMP-005: provenance graph cycle policy and compaction threshold.
- B-TEMP-006: retention-safe provenance metadata after Forget; I/D/Storage decision required.

### 中文未决事项

- B-TEMP-001：模糊/近似时间的精确 TimeValue 编码。
- B-TEMP-002：Record Time 与 Storage Transaction Time 的精确边界和含义。
- B-TEMP-003：是否所有 Claim/Relation Revision 都采用双时态，还是仅时间敏感断言采用。
- B-TEMP-004：Claim–Evidence Assessment 的记录身份和强度量规。
- B-TEMP-005：Provenance 图循环策略和压缩阈值。
- B-TEMP-006：Forget 后符合保留策略的 Provenance Metadata；需 I/D/Storage 决策。

## 10. Gate status / 门禁状态

B2 is IN PROGRESS. Core distinctions are supported by existing DECIDED source contracts, while selective bitemporal recommendation and fuzzy-time schema remain CANDIDATE/OPEN. No physical temporal database, event store, graph engine or JSON Schema is selected.

B2 进行中。核心区分由现有 DECIDED 源契约支持；选择性双时态建议和模糊时间 Schema 仍为 CANDIDATE/OPEN。不选择任何物理时态数据库、事件存储、图引擎或 JSON Schema。
