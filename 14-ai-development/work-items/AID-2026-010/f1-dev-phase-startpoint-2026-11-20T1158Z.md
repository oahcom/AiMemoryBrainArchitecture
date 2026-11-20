# F-43-01/F1 开发阶段起点：骨架齐备，五个 `todo!()` 待实现

测量时点 `2026-11-20T11:58Z`，对象 `oahcom/AiMemoryBrain` main `341bb04b3c53`。

本文件只登记测量到的事实：F1 的**接口骨架已经就位**，缺口是**五个 `todo!()` 函数体**加三个 `#[ignore]` 测试的启用。这使「开发阶段起点」从抽象描述变为可逐项核对的清单。

## 一、已就位的骨架（不需要再设计）

| 位置 | 内容 | 状态 |
|---|---|---|
| `src/authority.rs` | `trait DAuthoritativeSource`（`identity()` / `read_authoritative_snapshot()`）、`AuthorityIdentity`、`AuthorityError`（5 变体） | **已定义** |
| `src/receipt.rs` | `struct ReceiptSample`（7 字段，含 `is_fixture`）、`ReceiptError`（3 变体） | **已定义** |
| `src/d_predicates.rs` | `DHighWaterSnapshot` | 已定义 |
| `tests/scenarios/f1-dual-high-water-scenarios.yaml` | 场景定义数据 | **已存在** |
| `src/normalization.rs` + `ucd.rs` + `build.rs` | UCD 15.1.0 锁定与 NFC/NFD | **已实现并通过测试** |

`src/authority.rs` 的文档注释已经明确边界：

> A test double is useful for testing predicate logic, but it is not operational evidence and cannot close F-43-01/F1.
>
> Implementations must obtain a real authoritative observation. A constant response, unconditional true callback, fixture-only adapter, or local synthetic snapshot is not a production/operational D callback.

## 二、待实现清单（精确到函数）

| # | 文件:行 | 函数 | `todo!()` 内容 |
|---:|---|---|---|
| 1 | `src/receipt.rs:23` | `validate_operational_receipt` | `"Step 2: implement Receipt provenance and fixture rejection"` |
| 2 | `src/d_predicates.rs:53` | （六条 D 契约谓词） | `"Step 2: map and implement the six exact D-contract predicates"` |
| 3 | `src/d_predicates.rs:63` | （provenance/identity 校验） | `"Step 2: enforce real-source provenance and adapter identity"` |
| 4 | `tests/f1_scenarios.rs:11` | `all_ten_scenarios_are_defined_and_clause_mapped` | `"Step 2: require exactly ten mapped scenarios"` |
| 5 | `tests/f1_scenarios.rs:17` | `test_double_cannot_satisfy_operational_proof` | `"Step 2: assert test-double evidence is rejected operationally"` |
| 6 | `tests/f1_scenarios.rs:23` | `real_authority_and_receipt_are_required_for_operational_proof` | `"Step 2: exercise the real-authority evidence gate"` |
| 7 | `tests/d_normalization_vectors.rs:9` | D 专用向量集加载执行 | `"Step 2: load and execute the D-specific vector set"` |

三项 `src/` 实现 + 四项测试启用，共 **7 项**。测试带 `#[ignore = "Step 2 implementation pending"]`，实现完成后需移除 ignore 标记。

## 三、为什么这仍不构成 F1 关闭

即便这 7 项全部实现并通过，F1 关闭条件中仍有两项无法由代码满足：

| F1 关闭条件 | 代码能否满足 |
|---|---|
| D/H 对同一精确扩展映射 Blob 的独立接受 | 否（治理签署） |
| D authoritative query contract 精确绑定映射 | 部分（契约已存在） |
| 查询响应绑定 exact operation/request/receipt/snapshot/currentness/revocation 且 fail-closed | **是**（第 1–3 项实现） |
| H 消费端 parser/range/receipt-binding 实现及精确测试由 H Owner 接受 | 部分（需 H Owner 接受） |
| A 对最终 D/H 精确版本和运行证据独立复核 | 否（治理复核） |

**关键**：`DAuthoritativeSource` 的实现需要指向一个**真实的** D 权威端点。当前 ledger 记载 `canonical Runtime repository、authoritative storage、trust root、endpoint/transport、operational key registry 均未指定`。因此第 1–3 项可以写出通过编译、通过单元测试的实现，但**无法产出操作级证据**——除非真实端点存在。

这与 `development-readiness-register.md` §4 的表述完全一致：

> F1 remains OPEN because no real D-authoritative callback exists. Building the integration boundary can proceed; claiming operational proof cannot.

## 四、开发阶段的正确切分

| 阶段 | 内容 | 前置 |
|---|---|---|
| **可立即做** | 第 1–7 项实现与测试启用；谓词逻辑用 test double 覆盖全部分支 | 无（准入已开） |
| **不可做** | 声称 F1 操作级证明、声称 S1–S7 已 RUN、关闭 F1 | 需真实 D 权威端点 + 治理签署 |

把第一阶段成果表述为「F1 已实现」是错误的；正确表述是「F1 集成边界已实现，操作级证明待真实端点」。

## 五、复现

```
cd /home/ubuntu/ai-projects/AiMemoryBrain/AiMemoryBrain
grep -rn 'todo!' src tests
grep -rn 'Step 2 implementation pending' src tests
```

输出应为 7 处 `todo!` + 4 处 ignore 标注。

## 六、记录边界

本文件只登记代码事实。是否据此派工、是否调整 F1 表述、是否指定真实 D 权威端点，均由 A 与相应 Owner 裁定。L0 不代行编码，也不代行端点指定。
