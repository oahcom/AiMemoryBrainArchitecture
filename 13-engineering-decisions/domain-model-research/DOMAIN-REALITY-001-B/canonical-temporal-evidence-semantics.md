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

Existing source marks preservation of valid-time and record-time histories separately as DECIDED; the exact bitemporal query contract and transaction-time representation remain CANDIDATE/OPEN and require B + D + Storage confirmation.

现有源规范已将 Valid Time 与 Record Time 历史分别保留标记为 DECIDED；精确双时态查询契约和 Transaction Time 表示仍为 CANDIDATE/OPEN，需 B、D、Storage 确认。

### Complexity and owner impact

- Storage: immutable revision/commit metadata and temporal indexes; no mandate for temporal DB.
- D: lifecycle events and canonical commit cursor are not Valid Time.
- E: preserve source time expressions and transformation provenance.
- F: temporal filters must be scope-safe; relevance cannot rewrite epistemic/temporal truth.
- G: ContextVersion time is not Claim Valid Time or MemoryVersion Transaction Time.
- I: time metadata may expose routines/location patterns and needs policy/retention controls.

## 4. Evidence semantics / 证据语义

Evidence is an independently addressable source-material/observation object used to support, refute or qualify a Claim or Relation. It is not the Claim, not the Source itself, and not a confidence score.

Evidence 是可独立寻址的来源材料/观察对象，用于支持、反驳或限定 Claim 或 Relation。它不是 Claim 本身，不等于 Source，也不是 Confidence 分数。

Current core schema evidence attributes include stable evidence_id; evidence_kind; typed source_ref; optional locator and permitted retained excerpt/content reference; observed_at and immutable recorded_at; collector_ref (ActorRef resolved by the trust boundary); optional integrity digest; evidential role (supports, refutes, qualifies, context_only); Scope references; and availability state.

One Evidence may support multiple Claims; one Claim may have multiple Evidence items. Where role/strength/time/scope differs per Claim, use an explicit Claim–Evidence assessment/link, not a global Evidence property.

一份 Evidence 可以支持多个 Claim；一个 Claim 也可以有多份 Evidence。如果角色/强度/时间/Scope 因 Claim 而异，应建模为显式 Claim–Evidence 评估/关联，而不是 Evidence 的全局属性。

Evidence availability can change under retention/Forget policy without rewriting the historical fact that the evidence once existed. Permitted non-content audit metadata must not preserve reconstructive forgotten content.

## 5. Source vs Evidence vs Provenance / Source、Evidence 与 Provenance

| Concept | Meaning | Example |
|---|---|---|
| Source | Origin from which information is obtained | User message, document, event stream, tool/provider or external record |
| Evidence | Addressable material/observation selected as support/refutation/qualification | Specific document page span or observation |
| Provenance | Trace of how a target assertion/asset was captured or derived from exact inputs and methods | Extraction run + input version digests + method version |

A mutable URL alone is not durable Evidence. Source retention may be restricted; preserve only permitted references/metadata and mark unavailable/redacted state accurately. Evidence access is independently authorized and may be stricter than access to derived Memory.

仅有可变 URL 不能构成持久 Evidence。Source 保留可能受限；只能保留允许的引用/元数据，并准确标记不可用/脱敏状态。Evidence 访问必须单独授权，且可能比派生 Memory 的访问更严格。

## 6. Provenance requirements / 溯源要求

For a derived Memory/Claim/Relation, Provenance must make it possible to answer: exact source object and version(s); exact source portion/locator where available; transformation/derivation kind; method/component/model/rule version; derived-at time; input digests; parent provenance references; unavailable/redacted reason where incomplete.

对于派生 Memory/Claim/Relation，Provenance 必须能够回答：精确来源对象及版本、可用时的来源片段/定位、转换/派生类型、方法/组件/模型/规则版本、派生时间、输入摘要、父级溯源引用，以及信息不完整时的不可用/脱敏原因。

A method reference explains how an artifact was produced; it does not prove correctness. Do not require metadata the system cannot obtain or verify.

方法引用解释产物如何生成，不证明其正确性。不得要求系统无法获得或验证的元数据。

Lineage constraints:
- Source-to-target direction is explicit; do not confuse source and derived target.
- Derived outputs must not masquerade as original Evidence.
- Cycles are not automatically permitted; DAG-vs-limited-cycles remains OPEN in source.
- Multi-generation derivation preserves ancestry and input version references.
- Duplicate copies of one source do not count as independent corroboration.
- Source unavailability/Forget triggers downstream re-evaluation under D/I policy; unavailability does not prove source never existed.

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

## 9. Open decisions / 未决事项

- B-TEMP-001: exact TimeValue encoding for fuzzy/approximate time.
- B-TEMP-002: exact boundary and meaning of Record Time vs Storage Transaction Time.
- B-TEMP-003: whether every Claim/Relation revision is bitemporal or only time-sensitive assertions.
- B-TEMP-004: Claim–Evidence assessment record identity and strength rubric.
- B-TEMP-005: provenance graph cycle policy and compaction threshold.
- B-TEMP-006: retention-safe provenance metadata after Forget; I/D/Storage decision required.

## 10. Gate status / 门禁状态

B2 is IN PROGRESS. Core distinctions are supported by existing DECIDED source contracts, while selective bitemporal recommendation and fuzzy-time schema remain CANDIDATE/OPEN. No physical temporal database, event store, graph engine or JSON Schema is selected.

B2 进行中。核心区分由现有 DECIDED 源契约支持；选择性双时态建议和模糊时间 Schema 仍为 CANDIDATE/OPEN。不选择任何物理时态数据库、事件存储、图引擎或 JSON Schema。
