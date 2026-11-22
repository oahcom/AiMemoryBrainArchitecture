# GAP-EXEC-2026-11-22-PHASE2-BLOCKED-021

**登记编号**：GAP-EXEC-2026-11-22-PHASE2-BLOCKED-021
**性质**：MEASUREMENT_ONLY / TEST_DRAFT_ONLY / NO_IMPLEMENTATION / REQUIRES_INDEPENDENT_REVIEW
**测量点**：`main = dba34a35`（初版）→ `main = fe9e25a5`（v2 复测）
**登记时间**：2026-11-22
**作者**：协调会话（非独立审查者）
**版本**：v2 — §0.1 记录初版发布后 3 小时内被并行实现关闭 7 条

---

## 0.1 初版发布后被并行实现关闭的 7 条

初版在 `dba34a35` 测得 **9 条 ignore**。发布后 3 小时内，并行会话合入四个 PR：

| 条目 | 关闭者 | 提交 |
|---|---|---|
| `dm2_01` / `dm2_02` / `dm2_04` | #570 `ClaimRevisionRegistry`（同时提供 `ClaimRevisionResolver` trait，精确解析与 head 解析分开） | `5c50b910` |
| `dm2_03` | 测试体按初版 §4.1 草案改写为 `claim_revision_successor` 构造 | 见 `phase2_acceptance.rs:295` |
| `dm2_08` / `dm2_09` | `0c640a17` + #581 `a0d4f7d7`（`RelationTypeRegistry` + `RelationExtension::scope_refs`，并区分失败模式） | `0c640a17` |
| `dm2_12` | #582 `ProvenanceGraph` + `EvidenceIndependence::validate_independent` | `fe9e25a5` |

复测：

```
$ CC=zigcc AR=zigar cargo test --workspace --all-targets   # main = fe9e25a5
binaries: 30
passed=499  failed=0  ignored=2
```

`dba34a35` 时为 438 / 0 / 9。**净增 61 个通过测试，ignore 从 9 降到 2。**

剩下 2 条：

| 条目 | 阻塞者 | 是否我判断错了 |
|---|---|---|
| `dm2_06` | 权威 I（`AuthorizationDecisionRef` 契约） | **没判断错**。初版 §3 就写明这是唯一硬阻塞条目 |
| `dm2_11` | 待合 PR #583（`Provenance` lineage 字段） | 判断没错，但**当时未记录有一个 open PR 正在做这件事** |

### 0.1.1 这次更正推翻的我自己的一条方法论

初版 §2 把 9 条都写成「缺口」，并按「是否有外部决定阻塞」排序。这个排序是**对的**，
但漏了一个维度：**是否有并行会话已经在做**。

`dm2_11` 的初版条目说「依赖：无」，这是真的；但它同时被 #583 在做，而我没查开放 PR
就写了「可立即做」。结论没错，可执行性判断错了——对一个正在被别人的分支解决的条目
说「可以立即做」，等于建议重复劳动。

修正后的判据应有三档，不是两档：

| 档 | 判据 | 处置 |
|---|---|---|
| A | 无外部决定，且无开放 PR 在做 | 可立即派工 |
| B | 无外部决定，但有开放 PR 在做 | **不派工**，等那个 PR 落地后复测 |
| C | 被外部决定阻塞 | 不派工，等决定 |

初版只有 A 和 C，缺 B。这个缺陷在 §3 的依赖顺序里直接体现为「7 of 8 不需要任何外部
决定」这句话——它数字上对，可执行性上误导。

---

## 0. 本登记要解决的问题

「Phase 2/3 领域模型扩展（100% 未启动）」这个说法是错的，但错的方式值得精确记录：
Phase 2 有 **11 个验收维度真实通过**，另有 **9 个维度被 `#[ignore]` 挡住**，且每一条
都写明了缺失的 API 名称。

这不是「未启动」，是「规格已写、验收已写、实现未写」。两者的推进方式完全不同：
前者要先写规格，后者只需要按清单补 API。

本登记做三件事：

1. 把 9 条 ignore 理由逐条实测复核（哪些仍成立、哪些已过期）；
2. 把每条缺失 API 展开成可判定的缺口条目（输入、输出、拒绝条件）；
3. 为每条给出**测试草案**，使实现方落地后不需要再设计验收。

边界：**本登记不含任何实现代码**，也不修改 `phase2_acceptance.rs`。测试草案是
文字与伪代码，作者可直接采纳或改写。

---

## 1. 复核结果：1 条过期，8 条成立

### 1.1 `dm2_03` 的 ignore 理由是假的

`#545`（`444deef1`）新增 `crates/memory-domain/src/claim_identity.rs`，经
`lib.rs:7` 的 `pub use claim_identity::*` 再导出，提供的正是 ignore 理由声称
不存在的函数：

```rust
pub fn classify(prior: &ClaimRevision, candidate: &ClaimRevision) -> ClaimIdentityDecision
```

```
$ cargo test -p memory-domain --lib claim_identity
test result: ok. 19 passed; 0 failed; 0 ignored
```

19 个测试覆盖 CI-01、CI-02、CI-03、CI-04、CI-07、CI-08、CI-09、CI-10、CI-11、
CI-13，加上 label-only、qualifier 歧义、多维度歧义、scope 歧义、跨 Claim、
禁止回落、确定性。

**但 `dm2_03` 不能简单去掉 ignore**：它的函数体是 `unimplemented!()`，从未针对
`classify()` 写过。所以这是一个**验收文件缺陷**，不是领域 crate 缺陷。

`CI-05` / `CI-06` / `CI-12` 在模块头被记录为**不可达**（`ClaimRevision` 无
quantifier、modality、confidence 字段），不是缺失。`SubstantiveQualifier` 同理：
spec 的判据是语义的，实现只能报歧义。这三条加上 `SubstantiveQualifier` 是
**结构性不可达**，不应被计入缺口。

### 1.2 其余 8 条逐条实测

| 测试 | 探测符号 | `crates/` 命中 | 结论 |
|---|---|---:|---|
| `dm2_01` | `ClaimRevisionRegistry`、`register_revision` | 0 | 成立 |
| `dm2_02` | `AcceptedRevisionState` | 0 | 成立 |
| `dm2_04` | `ClaimRevisionResolver`、`resolve_claim_head` | 0 | 成立 |
| `dm2_06` | 已验证状态的 `AuthorizationDecisionRef` | 仅 `pending_i()` | 成立 |
| `dm2_08` | `RelationTypeRegistry`、`contains_relation_type` | 0 | 成立 |
| `dm2_09` | `RelationExtension.scope_refs` | 结构体无此字段 | 成立 |
| `dm2_11` | `Provenance::validate`、`parent_provenance_refs`、`unavailable_reason` | 0 | 成立 |
| `dm2_12` | `ProvenanceGraph`、`DerivationEdge`、`validate_independent` | 0 | 成立 |

佐证（`memory-domain/src/lib.rs` 实测字段）：

```
RelationExtension { subject, object, directionality, qualifiers, valid_time,
                    epistemic_status, evidence_refs, lifecycle_state }
                    ← 无 scope_refs

Provenance { provenance_id, source_refs, derivation_kind, actor_ref, created_at }
                    ← 无 source_version_ref / parent_provenance_refs / unavailable_reason
```

两条理由准确。

---

## 2. 缺口条目（可判定形式）

每条给出：**缺口 ID / 需要的能力 / 判据 / 拒绝条件 / 依赖**。

### G2-01 — Claim revision 唯一性注册表

- **能力**：跨 revision 的 `ClaimRevisionRef` 唯一性检查。`ClaimRevision::validate`
  只校验单个值，无法检测两个 revision 用了同一个 ID。
- **判据**：`register_revision(&mut self, rev: &ClaimRevision) -> Result<(), DomainError>`，
  第二次注册同一 `revision_ref` 返回 `Err`。
- **拒绝条件**：重复 `revision_ref`；空 `revision_ref`（已有 `EmptyId`）。
- **依赖**：无。纯内存、无 I/O。

### G2-02 — 接受状态的 append-only 转移

- **能力**：区分「不可变值」与「被接受后不可回退」。当前只有前者。
- **判据**：状态机 `Draft → Accepted`，`Accepted` 无出边；对 `Accepted` 施加任何
  转移返回 `Err`。
- **拒绝条件**：`Accepted → Draft`；`Accepted → Accepted`（重复接受）。
- **依赖**：无。

### G2-03 — 验收测试对齐已存在的分类器（**非缺口，是修复**）

- **能力**：已存在（`classify()`）。
- **需要做的**：把 `dm2_03` 的 `unimplemented!()` 换成针对 `classify()` 的向量断言，
  移除 ignore。
- **判据**：13 条 CI 中 10 条可达（CI-05/06/12 不可达），加上 4 条歧义规则。
- **注意**：这是唯一一条**不需要新增任何生产 API** 的条目。它可以在任何时间被
  独立完成，不依赖任何权威决定。
- **依赖**：无。

### G2-04 — 解析器拒绝 head 替换

- **能力**：`FactRevision` 已保存精确 `ClaimRevisionRef`，但没有解析器，因此无法
  证明「解析时不得把精确引用升级为 head」。
- **判据**：`resolve_revision(&self, r: &ClaimRevisionRef) -> Result<&ClaimRevision, _>`；
  当传入的是 head 而 pin 的是旧 revision 时，必须返回 pin 的那个，不得返回 head。
- **拒绝条件**：pin 的 revision 不存在；pin 与 head 不一致且调用方要求 head。
- **依赖**：G2-01（需要注册表才能按 ID 解析）。

### G2-06 — 缺失授权必须阻断 Fact 发布

- **能力**：`FactRevision::initial` 强制要求 `AuthorizationDecisionRef`，但唯一公开
  构造是 `pending_i()`，类型没有「缺失」与「已验证」两种状态。
- **判据**：`AuthorizationDecisionRef` 至少三态：`Absent` / `Pending` / `Validated`；
  `FactRevision::validate` 在 `Absent` 与 `Pending` 上返回 `Err`。
- **拒绝条件**：`Absent`、`Pending`。
- **已知冲突**：`fact_with_placeholder_attestor_validates_today` 固定了「当前占位符
  可通过」这一事实。该测试必须随本条目一起改，否则新判据会与旧测试互斥。
- **依赖**：**I 权威**。`pending_i()` 的文档写明「closes only when I defines the
  contract」。这是唯一一条被外部决定硬阻塞的条目。

### G2-08 — Relation type 注册表

- **能力**：`RelationDefinition` 描述单个 `relation_type` 的允许端点，但没有注册表，
  无法判定一个非空 `relation_type` 是否已注册。
- **判据**：`contains_relation_type(&self, t: &str) -> bool`；`RelationExtension::validate`
  在未注册类型上返回 `Err`。
- **拒绝条件**：未注册的 `relation_type`（非空但不在表内）。
- **依赖**：无。

### G2-09 — 时间 / scope / lifecycle 三维独立

- **能力**：`RelationExtension` 有 `valid_time`、`epistemic_status`、`lifecycle_state`，
  无 `scope_refs`，因此无法断言三者可独立变化。
- **判据**：加入 `scope_refs: Vec<ScopeRef>`；构造三组实例，分别只改一维，断言另两维
  不变且 `validate()` 均通过。
- **拒绝条件**：空 `scope_refs`（与 `ClaimRevision` 的 `EmptyRequiredField` 一致）。
- **依赖**：无，但**是 breaking change**：`RelationExtension` 的构造点需要同步。
  实测构造点数量需在实现前统计。

### G2-11 — Provenance 血缘或不可用理由，二者必居其一

- **能力**：`Provenance` 只有 `provenance_id / source_refs / derivation_kind /
  actor_ref / created_at`。没有 `source_version_ref`、`parent_provenance_refs`、
  `unavailable_reason`，也没有 `validate`。
- **判据**：`Provenance::validate` 要求 `parent_provenance_refs` 非空 **或**
  `unavailable_reason` 非空；两者都空返回 `Err`。
- **拒绝条件**：两者皆空；两者皆非空（互斥，避免既声称有血缘又声称不可用）。
- **依赖**：无。

### G2-12 — 共享祖先不构成独立证据

- **能力**：无 `ProvenanceGraph` / `DerivationEdge`，无法判定两条 Evidence 是否共享祖先。
- **判据**：`EvidenceIndependence::validate_independent(&graph, a, b)` 在 a、b 共享
  任一祖先时返回 `Err`。
- **拒绝条件**：直接共享父节点；间接共享祖先（传递闭包）；自反（a 与 a 比较）。
- **依赖**：G2-11（需要 `parent_provenance_refs` 才能建图）。

---

## 3. 依赖顺序（v2 修订）

初版在此处写「**8 条里 7 条不需要任何外部决定**」。数字仍对，但按 §0.1.1 的三档判据
重排后，可派工范围小得多：

```
【A 档 — 无外部决定，无开放 PR，可立即派工】
（空）

【B 档 — 无外部决定，但已有开放 PR 在做，等落地后复测】
G2-11  <- #583 feat/provenance-lineage-fields (open)

【C 档 — 被外部决定阻塞，不派工】
G2-06  <- 权威 I
```

初版列为 A 档的 G2-01、G2-02、G2-04、G2-08、G2-09、G2-12 **全部已被合入**（§0.1 表），
G2-03 同理。所以 A 档现在是空的，而这不是坏消息——它意味着 Phase 2 的实现缺口在
`fe9e25a5` 上只剩 2 条，其中 1 条有 PR 在做、1 条等权威。

**这是本登记最有价值的一行结论**：「Phase 2/3 领域模型 100% 未启动」在
`dba34a35` 就已经是错的（11 个维度通过），在 `fe9e25a5` 上错得更彻底（13 个维度通过、
2 个待办）。这个方向从来不是「未启动」，而是「已在收尾」。

---

## 4. 测试草案（v2：已落地部分的草案转为实现记录）

草案只写**判据**与**最小构造**，不写实现。实现方落地 API 后可直接采用。

### 4.1 G2-03（已落地，草案被采纳）

初版草案提示「字段若私有，需改为通过 `successor()` 构造」。实际实现正是这样做的
（`phase2_acceptance.rs:281` 新增 `claim_revision_successor` helper，用闭包改草稿
再 `successor()`）。这是草案里唯一一处前瞻判断被验证的地方。

### 4.2 G2-03 草案原文（已被采纳）

```rust
#[test]
fn dm2_03_ci_classification_vectors() {
    // 可达维度：只改一个字段，断言分类结果。
    let base = claim_revision("cr-1", "claim-1", &["ev-1"]);

    // CI-01 subject referent
    let mut other_subject = base.clone();
    other_subject.subject = "different".into();
    assert_eq!(
        classify(&base, &other_subject),
        ClaimIdentityDecision::Classified {
            class: ClaimIdentityClass::NewClaim,
            dimension: ChangeDimension::SubjectReferent,
        }
    );

    // CI-09 evidence 顺序变化不改变身份
    let mut reordered = base.clone();
    reordered.evidence_refs.reverse();
    assert_eq!(
        classify(&base, &reordered),
        ClaimIdentityDecision::Classified {
            class: ClaimIdentityClass::NewRevision,
            dimension: ChangeDimension::PresentationOnly,
        }
    );

    // 不可达维度必须以「歧义」表达，不得回落 NewRevision
    let mut quantifier = base.clone();
    quantifier.qualifiers = vec!["most".into()];
    assert!(matches!(
        classify(&base, &quantifier),
        ClaimIdentityDecision::RequiresGovernedDecision { .. }
    ));
}
```

**说明**：字段赋值是否可行取决于 `ClaimRevision` 字段可见性。若字段私有，草案需
改为通过 `successor()` 构造。这是实现方落地时要解决的细节，不是判据问题。

### 4.3 G2-01 草案原文（已落地，见 `5c50b910`）

初版草案要求「拒绝后注册表必须仍是原状态」。实现的 `ClaimRevisionRegistry` 满足
这一点，且额外把精确解析与 head 解析拆成两个方法（`ClaimRevisionResolver` trait），
比我草案里隐含的「一个 resolve」更严——从类型上杜绝了 pin 被静默升级为 head。

```rust
#[test]
fn dm2_01_claim_revision_ref_uniqueness_enforced() {
    let mut registry = ClaimRevisionRegistry::new();
    let first = claim_revision("cr-dup", "claim-1", &["ev-1"]);
    let second = claim_revision("cr-dup", "claim-2", &["ev-2"]);

    assert!(registry.register_revision(&first).is_ok());
    assert_eq!(
        registry.register_revision(&second),
        Err(DomainError::DuplicateRevisionRef)
    );
    // 失败注册不得污染注册表
    assert!(registry.get(second.revision_ref()).is_none());
}
```

最后一行是**关键断言**：拒绝之后注册表必须仍是原状态，否则拒绝是假的。

### 4.4 G2-02 草案原文（已落地，见 `5c50b910`）

```rust
#[test]
fn dm2_02_accepted_revision_is_append_only() {
    let mut state = AcceptedRevisionState::draft(claim_revision("cr-1", "claim-1", &["ev-1"]));

    assert!(state.accept().is_ok());
    assert_eq!(state.current(), AcceptedRevisionState::Accepted);

    // 无出边
    assert!(state.accept().is_err());
    assert!(state.revert().is_err());
    // 拒绝后状态不变
    assert_eq!(state.current(), AcceptedRevisionState::Accepted);
}
```

### 4.5 G2-04 草案原文（已落地，见 `5c50b910`）

```rust
#[test]
fn dm2_04_resolution_rejects_claim_head_substitution() {
    let mut resolver = ClaimRevisionResolver::new();
    resolver.insert(claim_revision("cr-1", "claim-1", &["ev-1"]));
    resolver.insert(claim_revision("cr-2", "claim-1", &["ev-2"])); // head

    let pinned = ClaimRevisionRef::new("cr-1").unwrap();
    let resolved = resolver.resolve_revision(&pinned).unwrap();

    assert_eq!(resolved.revision_ref().as_str(), "cr-1");
    assert_ne!(resolved.revision_ref(), resolver.head_of(ClaimRef::new("claim-1").unwrap()));
}
```

### 4.6 G2-08 草案原文（已落地，见 `0c640a17` / #581）

```rust
#[test]
fn dm2_08_unregistered_relation_type_rejected() {
    let mut registry = RelationTypeRegistry::new();
    registry.register(RelationDefinition { relation_type: "causes".into(), ..default() });

    assert!(registry.contains_relation_type("causes"));
    assert!(!registry.contains_relation_type("implies"));

    let mut rel = relation_extension("implies");
    assert_eq!(rel.validate(&registry), Err(DomainError::UnregisteredRelationType));
}
```

### 4.7 G2-09 草案原文（已落地，见 `0c640a17`）

```rust
#[test]
fn dm2_09_relation_time_scope_lifecycle_independent() {
    let base = relation_extension_full();

    let mut time_changed = base.clone();
    time_changed.valid_time = Some(ValidTimeRef::new("2026-06-01T00:00:00Z").unwrap());
    assert_eq!(time_changed.scope_refs, base.scope_refs);
    assert_eq!(time_changed.lifecycle_state, base.lifecycle_state);

    let mut scope_changed = base.clone();
    scope_changed.scope_refs = vec![scope("s2")];
    assert_eq!(scope_changed.valid_time, base.valid_time);
    assert_eq!(scope_changed.lifecycle_state, base.lifecycle_state);

    let mut lifecycle_changed = base.clone();
    lifecycle_changed.lifecycle_state = RelationLifecycleState::Retired;
    assert_eq!(lifecycle_changed.valid_time, base.valid_time);
    assert_eq!(lifecycle_changed.scope_refs, base.scope_refs);

    for r in [&time_changed, &scope_changed, &lifecycle_changed] {
        assert!(r.validate().is_ok());
    }
}
```

三组断言必须**都**存在。只断言一组是常见造假方式：证明「能改」不等于证明「独立」。

### 4.8 G2-11 草案原文（**未落地**，等 #583）

```rust
#[test]
fn dm2_11_provenance_lineage_or_unavailable_reason_mandatory() {
    // 两者皆空 → 拒绝
    let bare = Provenance { parent_provenance_refs: vec![], unavailable_reason: None, ..base() };
    assert_eq!(bare.validate(), Err(DomainError::ProvenanceLineageUnaccounted));

    // 只有血缘 → 通过
    let with_parent = Provenance { parent_provenance_refs: vec![prov("p1")], ..base() };
    assert!(with_parent.validate().is_ok());

    // 只有理由 → 通过
    let with_reason = Provenance { unavailable_reason: Some("source purged".into()), ..base() };
    assert!(with_reason.validate().is_ok());

    // 两者皆有 → 拒绝（互斥）
    let both = Provenance {
        parent_provenance_refs: vec![prov("p1")],
        unavailable_reason: Some("source purged".into()),
        ..base()
    };
    assert_eq!(both.validate(), Err(DomainError::ProvenanceLineageAmbiguous));
}
```

### 4.9 G2-12 草案原文（已落地，见 `fe9e25a5`）

```rust
#[test]
fn dm2_12_shared_ancestry_not_independent_evidence() {
    // 图：root <- a, root <- b   （a、b 共享祖先）
    let mut graph = ProvenanceGraph::new();
    graph.add(DerivationEdge::new(prov("root"), prov("a")));
    graph.add(DerivationEdge::new(prov("root"), prov("b")));

    assert_eq!(
        EvidenceIndependence::validate_independent(&graph, prov("a"), prov("b")),
        Err(DomainError::SharedAncestry { ancestor: prov("root") })
    );

    // 独立分支
    graph.add(DerivationEdge::new(prov("root2"), prov("c")));
    assert!(EvidenceIndependence::validate_independent(&graph, prov("a"), prov("c")).is_ok());

    // 自反
    assert!(EvidenceIndependence::validate_independent(&graph, prov("a"), prov("a")).is_err());
}
```

**注意**：错误必须携带 `ancestor`，否则调用方无法解释为什么判定不独立。只返回
bool 的实现不满足判据。

---

## 5. 本登记不做的事

- 不修改 `phase2_acceptance.rs`；
- 不新增任何生产代码；
- 不声称任何条目「已实现」；
- 不声称本登记是独立审查——作者是协调会话，不是独立审查者；
- 不决定 `G2-06` 的 I 契约形态（那是 I 权威的事）。

## 6. 复核清单（供后续会话重新推导）

```sh
# 1. ignore 数量与理由
grep -n "#\[ignore" crates/memory-domain/tests/phase2_acceptance.rs

# 2. 每条缺失 API 是否已存在
for s in ClaimRevisionRegistry AcceptedRevisionState ClaimRevisionResolver \
         resolve_claim_head RelationTypeRegistry contains_relation_type \
         ProvenanceGraph DerivationEdge validate_independent; do
  printf '%s %s\n' "$(grep -rc "$s" --include=*.rs crates/ 2>/dev/null | \
    awk -F: '{n+=$2}END{print n+0}')" "$s"
done

# 3. 分类器是否仍存在且通过
cargo test -p memory-domain --lib claim_identity

# 4. 全量
CC=zigcc AR=zigar cargo test --workspace --all-targets
```

第 2 步的输出中，任何非零值都意味着该条目的 ignore 理由需要重新核对——`dm2_03`
就是这样被发现的。
