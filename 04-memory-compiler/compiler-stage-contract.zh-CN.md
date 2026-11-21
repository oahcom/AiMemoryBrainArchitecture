# Memory Compiler 阶段契约

**状态：** PROPOSED — 契约级参考；不构成生产授权
**Owner：** E — Memory Compiler 与派生记忆生产
**Work Item：** GAP-BASELINE-001 / GAP-01
**基线：** 1ad6c2cf67a228f597fcbe1c7149c328ecbf38e9

## 1. 目的与权限

本文定义从已接受的源事件/源记忆到带有明确来源链的派生记忆候选项的编译转换边界。本文不重新定义 Event Store 的托管契约。Event Store 接受不等于已编译、已验证、已索引、已发布或已成为 Canonical。

Owner E 仅拥有阶段转换和来源链生产权限。本文不裁定 Owner I 的权限/保留/安全策略，也不裁定 Owner D 的 Canonical 权威与发布规则。

## 2. 类型

- `SourceEvent`：已接受的事件信封引用，包含 `event_id`、`producer_actor_ref`、`scope_ref`、`payload_ref`、`payload_digest`、`idempotency_key` 和 `accepted_at`。
- `SourceMemory`：由已接受事件物化的源记忆；包含 `memory_id`、`source_event_id`、`scope_ref`、`content`、`content_digest`、`created_at`。
- `NormalizedMemory`：经过验证和规范化的表示；包含 `memory_id`、`scope_ref`、`normalized_content`、`normalization_version`、`source_digest`。
- `DerivationRequest`：不可变输入集合，包含源记忆 ID、转换 ID/版本和确定性参数。
- `DerivedMemoryCandidate`：派生内容及必需的来源链元数据；它本身不具有 Canonical 身份，也不代表可发布。
- `ProvenanceRecord`：派生候选项与其直接来源、传递根来源之间的不可变映射。
- `StageFailure`：类型化失败，包含阶段、稳定错误码、是否可重试和输入身份。错误载荷不得泄露受保护内容。

所有 ID 和引用都是非空不透明字符串。摘要为 64 字符的小写十六进制 SHA-256。时间戳为 RFC 3339 UTC 时刻。内容均视为不可信数据，不得作为可执行指令。

## 3. 阶段枚举与契约

| 阶段 | 输入 → 输出 | 失败语义 | 幂等性 |
|---|---|---|---|
| Ingest（摄取） | `SourceEvent` → `SourceMemory`（零个或多个，每个保留事件身份） | **FAIL-CLOSED**：信封格式错误、缺少必需托管字段或摘要不匹配时，拒绝该事件进入编译；不得部分接受 | 相同 event ID + 相同摘要产生相同逻辑源身份；相同 event ID + 不同摘要构成冲突 |
| Validate（验证） | `SourceMemory` → `ValidatedSourceMemory` | **FAIL-CLOSED**：缺少身份/Scope/内容或摘要无效时停止该条目 | 纯验证；相同字节和规则产生相同结果 |
| Normalize（规范化） | `ValidatedSourceMemory` → `NormalizedMemory` | **FAIL-CLOSED**：不支持的编码、必需结构存在歧义或规范化器错误时，不产生输出 | 以源记忆 ID + 源摘要 + 规范化器 ID/版本为键；重复执行返回等价输出 |
| Derive（派生） | 有序的 `NormalizedMemory[]` + `DerivationRequest` → `DerivedMemoryCandidate` | **FAIL-CLOSED**：输入不足、转换错误或输出无效时不产生候选项；禁止静默部分派生 | 以有序源 ID/摘要 + 转换 ID/版本 + 规范化参数摘要为键 |
| Provenance（来源追踪） | 候选项 + 直接来源链 → `ProvenanceRecord` | **FAIL-CLOSED**：来源缺失、存在环、链路断裂或根来源无法解析时，候选项不得继续 | 相同候选身份和来源链输入产生相同记录；重复写入必须逻辑等价 |
| Publish gate（发布门） | 候选项 + 来源记录 + 策略决策 → 发布请求 | **FAIL-CLOSED**：所有必需策略/权威决策未就绪前关闭；本文不定义发布副作用 | 未来发布器必须使用稳定候选身份/幂等身份；语义待 Owner D/I 决策 |

任何阶段都不得把失败转换成看似成功的空结果。可重试失败可以使用相同幂等身份重试。不可重试失败必须修正输入或使用新的转换版本。

## 4. 必需的来源追踪字段

每个派生候选项 MUST 携带以下字段。“可省略：否”表示省略即使候选项无效。

| 字段 | 类型 | 可省略？ | 含义 |
|---|---|---:|---|
| `derived_memory_id` | string | 否 | 派生记忆的稳定身份 |
| `derivation_id` | string | 否 | 本次派生执行/逻辑操作的稳定身份 |
| `transformation_id` | string | 否 | 派生算法名称 |
| `transformation_version` | string | 否 | 不可变算法版本 |
| `immediate_source_memory_ids` | string[]（非空） | 否 | 直接源记忆 ID |
| `root_source_memory_ids` | string[]（非空） | 否 | 去重后的终端源记忆 ID |
| `source_event_ids` | string[]（非空） | 否 | 锚定源记忆的事件身份 |
| `source_digests` | string[]（SHA-256） | 否 | 与直接来源顺序对齐的内容摘要 |
| `scope_ref` | string | 否 | 作为数据复制的 Scope 标签；不暗示权限继承 |
| `created_at` | RFC3339 UTC | 否 | 候选项创建时刻 |
| `compiler_contract_version` | string | 否 | 生成候选项时使用的契约版本 |
| `parameter_digest` | SHA-256 | 否 | 规范化派生参数的摘要 |
| `parent_derived_memory_ids` | string[] | 是 | 本身也是派生记忆的直接父节点 |

直接来源数组的顺序具有意义且必须稳定。根 ID 必须去重并按字典序排序，以便确定性比较。源摘要和事件 ID 必须与直接来源顺序对齐。每个源记忆的源事件身份必须沿链保留；如果上游源记忆具有多个事件锚点，必须全部保留。

### 来源回溯终止条件

来源链遍历只有在到达一个明确分类为非派生根节点的源记忆时才能终止，该节点必须具有非空的 `source_event_id` 和可验证的源摘要。派生节点必须至少有一个直接父节点，且每个父节点都必须能够解析。节点缺失、存在环、根节点为空、事件锚点缺失或摘要不匹配均属于错误；遍历绝不能静默截断。根源 ID 是所有可达非派生根节点的集合。

## 5. 跨 Owner 决策 — 尚未解决

- **PENDING CROSS-OWNER DECISION — Owner I：** 源记忆产生派生记忆时，必须继承或重新评估哪些权限、Principal、Scope、撤销、保留和 Forget 约束（如有）？源策略变化会使哪些既有派生记忆失效或受到抑制？**本契约不自行裁定，待 Owner I 明确。**
- **PENDING CROSS-OWNER DECISION — Owner D：** 哪个权威定义 Canonical 状态？派生候选项在任何 Canonical 登记或发布之前必须通过什么验证/验收门槛？派生记忆是否可能成为 Canonical，以及由何种权威决定？**本契约不自行裁定，待 Owner D 明确。**

在上述裁定完成前，参考模型止于非 Canonical 候选项及其来源记录。它不授权发布、Canonical 登记、权限继承或绕过策略。

## 6. 参考模型与验证边界

`reference-model/` 下的 Python 参考模型仅演示确定性的契约不变量：必需身份/摘要检查、确定性规范化/派生身份、完整来源链解析、环/缺失父节点拒绝以及 fail-closed 行为。

它不是生产实现。它不提供存储、事务性、WAL、fsync、崩溃恢复、队列、Worker 租约、分布式协调、载荷字节的密码学验证、授权、保留/Forget 执行、Canonical 登记、发布、索引、检索或性能/安全资格验证。本文不声称任何生产耐久性或运行时行为已得到证明。

在仓库根目录运行：

```sh
python3 -m unittest discover -s 04-memory-compiler/reference-model -p 'test_*.py' -v
```

测试套件会在实际执行时报告准确数量。参考模型测试通过不等于架构验收或独立审查。
