# H Adapter Capability / Applied Attestation 双语复审

- 日期：2026-11-17
- 源分支：`session-h-bmcp-protocol`
- 精确源路径：`08-bmcp-protocol/adapter-capability-and-applied-attestation.md`
- 精确源 Blob SHA：`db59b63e322d7255b8b400f47859dcac32bb3027`
- 范围：完整 EN/zh-CN 配对文件的结构一致性与针对性语义复核。
- 非目标：Owner 批准、协议/Schema 冻结、密码学批准、实现验证、互操作或一致性测试执行。

## 1. 工件

- EN：`docs/en/08-bmcp-protocol/adapter-capability-and-applied-attestation.md`
- zh-CN：`docs/zh-CN/08-bmcp-protocol/adapter-capability-and-applied-attestation.md`

英文 companion 嵌入精确源文件内容和 Blob pin。中文 companion 保留相同源 pin，并提供双向语言链接。

## 2. 结构读回

| 指标 | Owner 源文件 | 英文 | 中文 |
|---|---:|---:|---:|
| 标题数 | 22 | 22 | 22 |
| 表格行数（含表头/分隔行） | 33 | 33 | 33 |
| 章节 | 1–11，包括 11.1–11.7 | 相同 | 相同 |

已从各自分支重新读取 Owner 精确源文件、英文 companion 和中文 companion。英文 companion 包含与源文件完全相同的内容。中文 companion 保留完整章节层级和表格行结构。

## 3. 语义复核

- 能力声明/CapabilityEpoch 失效与逐请求证据保持区分。
- Tier 1 要求观测最终不可变请求及成功提交；Tier 2 不得声称 Full；Tier 3 仅证明传输。
- C/G 六阶段生命周期未被合并；H 不拥有 G 的 Applied 接受权。
- H §11 明确标记为 CANDIDATE，并要求 C/G/I/D/B Owner 决议；没有声称 Wire 冻结。
- 精确请求/边界身份、Context/Delivery/attempt、Managed Region inventory/coverage/digest、verifier 身份绑定、I/D 权威引用、来源信息、逐请求 bypass、重放身份及时间顺序均得到保留。
- Forget ACK 与 Applied Attestation 仍是不同证据族。
- 隐私非声明得到保留：摘要不等于匿名化；默认不包含原始 prompt/记忆文本。
- H 一致性测试仍为 SPECIFIED / NOT RUN；实现与互操作仍 NOT VERIFIED。

本次针对性翻译复审未发现重大语义偏差。

## 4. 结论

**双语语义一致性：针对该精确源 Blob，PASS。**

**源状态不变：** CANDIDATE；final-request proof profile 与 C 的对齐仍 OPEN；authorization binding 与 I 的对齐仍 OPEN。C/G/H 冻结仍 BLOCKED。本复审不构成 H Owner 接受、C/G 接受、I/D/B 批准、Wire/Schema 冻结、实现验证或测试执行。
