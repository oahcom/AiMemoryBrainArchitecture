---
document_metadata:
  domain: ai-development
  role: decision-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: NOT_RECORDED
      decision_date: NOT_RECORDED
      approved_version: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "No formal approval record, approver identity or decision date exists in this repository; recorded as NOT_RECORDED rather than inferred."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

# D-OWNER-DECISION-PROTECTED-VISIBILITY-001 — Protected visibility 授权签发者

**状态：** DECIDED（Owner-proxy 裁决；开发基线及当前仓库契约）  
**裁决者：** 在 D 所有的发布权威边界内履职的 Owner D  
**裁决日期：** 2026-11-21  
**基线：** `main @ 6edf116`  
**范围：** GAP-14-B；`PublicationProof::protected_visibility_authorized`  
**兼容性：** Phase 1 冻结不变；不修改 Rust、Schema、Public API 或 `DomainError`。

## 1. Decision（裁决）

**D 裁定：在当前开发基线及仓库契约下，`protected_visibility_authorized` 永久保持 `false`。权威边界是 `compiler-stage-contract.md` §8 指定的 Storage 与适用 D/I 授权组成的联合权威边界：Storage 拥有受保护可见性状态推进的职责，适用的 D/I 权威必须分别独立建立各自的授权条件。任何单一本地组件，包括 D 的 owner-proxy 开发基线签发者和 E 的 `AdmissionStore`，均不得替代这一联合权威。目前不存在能够合法证明该 flag 为 true 的权威、可验证、持久化授权记录及验证器。不授权任何本地 issuer、调用方断言、开发信任锚或委托捷径。**

本裁决关闭 GAP-14-B 在当前基线下的第三个问题。

本裁决不将 protected visibility 授权合并为 PublicationParticipant Admission。两者是独立的证明条件，必须分别建立。

## 2. 签发者身份与权威边界辨析

### 2.1 规范已经指定权威归属

`docs/en/04-memory-compiler/compiler-stage-contract.md` §8 明确规定：

| 操作 | 所需权威 | E 的权限 |
|---|---|---|
| Protected visibility advancement | Storage and applicable D/I authorization | No independent authority |

因此，规范层面的权威归属并没有缺失。

它指定的是一个组合权威：

1. **Storage**：拥有实际受保护可见性推进操作及权威存储状态。
2. **D**：在具体操作需要时，提供 D 所有的 Fence、lineage 和发布授权证据。
3. **I**：在具体操作需要时，提供 I 所有的授权决定。
4. **E**：可以调用操作并保留精确证据，但不得决定或制造授权。

不得将“Storage and applicable D/I authorization”简化为“只有 D 授权”“只有 Storage preparation”或“E publication authority”。

### 2.2 C 的 protected-provider 契约确认跨 Owner 证据边界

`docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` 中 JF-10 prepared-participant / COC bridge 约束要求：在针对精确不可变操作元组调用 protected provider side effect 之前，必须具备：

- 已获得 quorum-committed 的 `JF10_PREPARE_INTENT_REGISTERED`；
- Storage 签名的 `PreparedParticipantReceipt`，并已持久注册为 `JF10_PREPARED_PARTICIPANT_REGISTERED`；
- I owner-final gate 针对该操作元组产生的权威终态决定。

同一契约还保留 D 的 Fence 和 lineage 义务，包括精确 participant 与 operation 绑定。

这确认了 protected operation 依赖独立的 Owner 证据。它不授权 C、E 或本地 SQLite ledger 替代这些签发者。

C 契约中的 provider side-effect 要求是跨 Owner 权威边界的相关证据，但它本身并没有定义新的本地 publication-visibility 签发者，也没有使 provider submission 等同于 publication visibility advancement。

### 2.3 这些权威不等于现有本地实现

以下组件均不等同于所要求的组合权威：

- `crates/memory-compiler/src/admission.rs` 中的 `AdmissionStore`；
- `AdmissionPublicationAuthority`；
- `d-owner-proxy/dev-baseline-v1`；
- 本地布尔值或 request field；
- 仅供测试使用的 publication authority。

`AdmissionStore` 是 E 侧本地 SQLite 生命周期 ledger。其 publication receipt、producer 和 dependency 记录不能建立 Storage 的 protected visibility 决定，也不能建立适用的 D/I 授权。

仅仅持久保存一个“visibility 已获授权”的断言，不会使该断言变成权威证据。

## 3. 记录、类型与验证器

**当前基线不适用。**

本裁决不指定任何本地授权记录、引用类型、数据表或验证器。

当前仓库没有提供能够建立全部必要事实的完整权威链：

| 所需证据 | 权威 | 当前限制 |
|---|---|---|
| 精确 Storage publication preparation 与 protected visibility 状态 | Storage | Storage 拥有该状态，但 E 无法取得完整的跨 Owner 授权记录及验证链 |
| 适用的 D Fence/lineage 授权 | D | 尚未建立完整的本地 publication-visibility issuer |
| 适用的 I owner-final 授权 | I | 不允许任何本地替代者签发或推断该决定 |
| 各 Owner 证据之间的精确 tuple 绑定 | 适用的 Owners / coordinator | C 契约规定了跨 Owner 证据要求，但没有建立完整的本地生产验证器 |
| 编译器消费的组合授权 | Storage 和适用的 D/I 权威 | 不存在权威本地记录和验证器 |

现有的 `publication_receipts` 和 `publication_preparations` 记录不能替代所需授权。

描述 `PreparedHidden` 的记录只能证明 preparation 状态，不能证明有权推进 protected visibility。

同样，单独的 publication receipt、COC intent、I decision、D clearance 或 Storage receipt，均不得被提升为完整的组合授权。

本裁决不授权新增任何数据表、本地 issuer、引用类型或验证器。

## 4. 为什么该 flag 必须保持 false

当前基线不存在合法建立 `protected_visibility_authorized = true` 的途径。

原因如下：

1. `OWNER-DECISION-PUBLICATION-RECORD-001` D3 记录了 `protected_visibility_authorized` 在 `crates/memory-compiler/src/lib.rs` 之外出现次数为零，并且没有 policy input 或 table。
2. `compiler-stage-contract.md` §8 明确将 protected visibility advancement 交给 Storage 和适用的 D/I 授权，同时否定 E 的独立授权权。
3. C 的 JF-10 bridge 要求 protected operation 具备独立的 COC、Storage 和 I 证据。不能以本地断言替代该证据链。
4. E 侧 `AdmissionStore` 不拥有 Storage visibility 或 I authorization。
5. 不存在将必要 Owner 证据绑定到精确 publication tuple 的完整本地记录与验证器。
6. 不存在允许本地开发 issuer 代表 Storage 或 I 行事的委托授权文件。

在这些条件下创建本地 issuer，会把不可验证的主张转化成表面上具有授权效力的证据。

这属于替代授权决定，而不是对既有权威契约的实现。

**因此，在当前基线及当前契约下，`protected_visibility_authorized` 必须永久保持 false。**

这里的“永久”意味着当前基线下任何实现都不得将该 flag 设为 true。改变这一结论必须经过新的、明确的跨 Owner 决策及经验证的权威集成；未来组件可用并不会自动产生授权。

### 委托裁决

**当前基线不授权委托。**

D 无权代表 Storage 委托其可见性状态权威，也无权代表 I 委托其授权权威。

未来跨 Owner 委托至少必须具备：

- 每个受影响权威 Owner 的明确授权；
- 不可变、可验证的委托凭证；
- 精确的 scope、operation、tuple 和允许操作绑定；
- 签发者身份与完整性验证；
- 有效期及 generation/replay 约束；
- 明确的撤销语义和持久化撤销证据；
- 能拒绝过期、已撤销、不匹配或不完整委托证据的验证器。

当前不存在这样的委托凭证或验证器。

本地开发代理、配置开关、调用方布尔值或 E 侧 registry 均不构成委托凭证。

## 5. 与前序决策的关系

### D3 — `OWNER-DECISION-PUBLICATION-RECORD-001`

D3 将 `protected_visibility_authorized` 记录为无来源。

本裁决进一步明确：

- 规范中的权威边界已经在 §8 指定；
- 缺失的不是未命名的权威类别；
- 缺失的是具体权威证据、签发者集成、持久化绑定和验证器。

D3 的 fail-closed 结论保持不变。

### D7.1 / D7.2

D7.1 因为 COC quorum、Storage signing 和 I terminal decision 不能由本地 D/E registry 制造，永久禁止当前基线下的 `publication_participant_admitted`。

D7.2 将这些外部依赖分别归属于 COC、Storage 和 I。

本裁决与两项决定保持一致：

- 不创造本地 protected-visibility issuer；
- 不混淆 participant admission 与 protected visibility authorization。

这两个 flag 是不同的授权条件，尽管它们在最终 Suppressed 分支中同时被消费。

### `D-OWNER-DECISION-PARTICIPANT-ADMISSION-001`

本裁决采用相同的开发基线规则：

- 本地记录不能铸造缺失的外部权威；
- 调用方断言不能变成权威证据；
- 开发代理不能替代外部 Owner；
- 生产 adapter 必须继续输出 false。

本裁决不重新打开或修改 participant-admission 决策。

### GAP-14-B

本裁决给出第三个也是最后一个答案：

1. `canonical_commit_confirmed`：D6——当前契约下永久 false。
2. `publication_participant_admitted`：D7——当前基线下永久 false。
3. `protected_visibility_authorized`：本裁决——当前基线下永久 false。

三个问题现在全部 DECIDED。

## 6. Phase 1 兼容性

本裁决仅修改文档。

不修改：

- `PublicationProof` 或其八个字段；
- Phase 1 冻结契约；
- `dm2_14` 的预期或输入；
- Rust 源码、Schema、DDL、序列化、Public API 或 `DomainError`；
- `Blocked`、`Suppressed` 或 `Published` 的 disposition 定义。

现有 gate 语义保持不变：

```rust
if !proof.producer_admitted
    || !proof.dependency_closure_complete
    || !proof.canonical_commit_confirmed
    || !proof.storage_prepared_hidden
{
    return Ok(PublishedDerivative {
        derivative: staged,
        disposition: PublicationDisposition::Blocked,
    });
}

if !proof.publication_participant_admitted
    || !proof.protected_visibility_authorized
{
    return Ok(PublishedDerivative {
        derivative: staged,
        disposition: PublicationDisposition::Suppressed,
    });
}
```

两组条件的区别具有实际意义：

- 前四个条件是发布前置条件，失败产生 `Blocked`。
- 最后两个条件是独立授权条件，失败产生 `Suppressed`。

因此，protected visibility authorization 不是 participant admission 或 storage preparation 的另一种名称。

### Production 可达性结论

由于 D7.1 要求 `publication_participant_admitted = false`，在当前基线及契约下，生产环境的 `Published` 分支永久不可达。

即使其余六个 flag 全部变成 true，第二组授权条件仍然无法通过。

如果前四个条件满足，结果是 `Suppressed`，不是 `Published`。

如果前四个条件中任意一个不满足，结果仍然是 `Blocked`。

这是已采纳权威模型的明确后果，不是应当通过把某个 flag 强行设为 true 来修复的实现缺陷。

## 7. 本裁决不决定的事项

以下事项仍然属于 **OUT-OF-SCOPE（dev-baseline）**：

- 生产密码学套件、规范化、签名算法和密钥策略；
- Storage 签名密钥托管、轮换、撤销和 HSM；
- Storage 生产可见性状态推进实现与部署；
- COC quorum 算法、成员资格、共识、故障切换和运维部署；
- I 的生产授权 sequencer 与终态决定实现；
- D 消费精确 Storage/I 证据的生产 Fence/Admission 集成；
- 跨 Owner 委托策略及委托凭证实现；
- 生产 tuple 绑定、互操作性及端到端一致性验证；
- 生产 publication 激活，以及未来任何允许 `Published` 的新决策。

本裁决不批准未来签发者，也不承诺未来组件可用后自动获得发布授权。

未来任何将该 flag 改为 true 的提案，都必须通过新的跨 Owner 决策，明确指定实际签发者、记录、验证器、tuple 绑定规则、适用的委托规则及生产验证证据。

## 8. Closure criteria（关闭标准）

1. `compiler-stage-contract.md` §8 继续将 Storage 和适用 D/I 授权指定为 protected visibility advancement 的必要权威；E 不拥有独立授权权。
2. 在当前基线下，生产 adapter 中的 `protected_visibility_authorized` 始终为 `false`。
3. 不得引入本地 protected-visibility issuer、授权表、引用类型、调用方可控布尔值或开发信任锚捷径。
4. 不得将 `AdmissionStore` 及其 publication receipts 描述为 Storage visibility authorization 或 D/I authorization。
5. C 的 JF-10 protected-operation 证据要求保持完整，不得将其描述为已经实现的本地 publication-visibility 实现。
6. 不得暗示或引入向 D owner-proxy、E、本地 registry 或开发信任锚的委托。
7. `PublicationProof` 八个字段、Phase 1 freeze 和 `dm2_14` 输入保持不变；发布前正常验证环境必须记录未改变的 `dm2_14` PASS。
8. GAP-14-B 必须引用本裁决作为第三项已完成的裁决。
9. 当任意前四个前置条件为 false 时，生产 disposition 保持 `Blocked`；当前四个前置条件通过但两个独立授权条件中任意一个为 false 时，生产 disposition 为 `Suppressed`。
10. 任何未来将 flag 改为 `true` 的变更，都必须通过新的跨 Owner 决策，明确 Storage 和适用 D/I 的具体签发者、持久化证据、验证器、tuple 绑定规则及生产验证。
11. 必须准确记录当前生产结论：由于 `publication_participant_admitted` 在当前基线及契约下永久保持 false，`Published` 不可达。

---

**最终裁决：** 当前开发基线下 `protected_visibility_authorized = false`。不授权本地 issuer 或委托。GAP-14-B 的三个决策问题全部完成。在当前契约下，`Published` 仍然无法在 production 中到达。
