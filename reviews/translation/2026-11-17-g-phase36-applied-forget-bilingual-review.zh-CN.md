# G Phase 3.6 Applied / Forget / Reconciliation 双语复审

- 日期：2026-11-17
- 源分支：`session-g-memory-context`
- 源路径：`06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md`
- 精确源 Blob SHA：`aa3afa73d8a76cc6f025839c52bfbff6a983046a`
- 范围：完整 EN/zh-CN 配对文件，包括 CGH-APPLIED-1.1 recovery-batch 修订之前的全部 Owner 决议补充。
- 非目标：超出源文件既有决议的 Owner 批准、C/G/H 全局冻结、实现验证或一致性测试执行。

## 1. 工件

- EN：`docs/en/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md`
- zh-CN：`docs/zh-CN/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md`

英文 companion 嵌入精确 Owner 源文件内容和 Blob pin。中文 companion 保留相同源 pin，并提供双向语言链接。

## 2. 结构读回

| 指标 | Owner 源文件 | 英文 | 中文 |
|---|---:|---:|---:|
| 标题数 | 21 | 21 | 21 |
| 表格行数（含表头/分隔行） | 37 | 37 | 37 |
| 行数 | 272 | 275 | 273 |

三个工件均已从 GitHub 读回。英文 companion 包含与 Owner 源文件完全相同的内容。中文 companion 保留全部 21 个标题和 37 行表格，包括全部 15 个 G-36 一致性案例及所有决议补充。

## 3. 语义复核

- 六个生命周期阶段保持分离；只有 G 拥有 Applied 接受权。
- Full Applied 保留全部 13 项接受谓词，包括精确 request/boundary 身份、认证身份/session、Scope/Environment、Managed Region inventory/digest、当前 I PermissionEpoch/decision、D ForgetFence/lineage、H CapabilityEpoch、C Submit 证据，以及此前不存在失效事件。
- 历史 Applied 与当前使用有效性保持分离；后续 Forget/撤销使当前使用无效，但不改写有效历史。
- Forget tombstone 范围及 G 自有的九项抑制/失效动作均得到保留；G 不声称 F index/cache purge 或 H 本地 Adapter purge 已完成。
- Context Remove 仍只是成员关系移除，不是 Canonical Forget。
- Reconnect 仍是新的信任边界；未经当前权威检查，不得重放过期 Snapshot/Delta 或旧 ACK。
- G-36-01..15 仍为 SPECIFIED / NOT RUN。
- CFG、Issue #3、Issue #6、CGH-APPLIED-1.1、当前候选再次确认及 recovery-batch 修订均保留精确 Blob 引用、Owner 处置和列明的例外。
- 翻译没有把 G 的 ACCEPT WITH ENUMERATED EXCEPTIONS 升格为全局冻结或实现批准。

本次针对性复审未发现重大语义偏差。

## 4. 结论

**双语语义一致性：针对该精确源 Blob，PASS。**

G 源状态仍为：语义决策已记录；C/G/H Applied 冻结阻塞；实现/执行未验证。G 自身的精确版本决议仍仅适用于其固定的 A package 版本及列明例外。G 一致性测试仍为 SPECIFIED / NOT RUN。本复审不证明 C/G/H 全局冻结、实现、Runtime 行为、全局 Forget 完成或物理擦除。
