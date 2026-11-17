# C C-submit / I-Authorization / D-ForgetFence 因果排序双语复审

- 日期：2026-11-17
- 源分支：`session-c-agent-integration-2026-11-16`
- 源路径：`07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`
- 精确源 Blob SHA：`45a48249717c8cddb07ab96197730ef93d406c22`
- 范围：完整 EN/zh-CN 配对文件，包括 C 对 CGH-APPLIED-1.1 recovery-batch 的精确版本接受及 JF-10 bridge Issue #8 决议。
- 非目标：coordinator 部署、Provider 实现、H Schema 冻结、超出 G 自身固定决议的 G Applied 接受，或一致性测试执行。

## 1. 工件

- EN：`docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`
- zh-CN：`docs/zh-CN/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`

英文 companion 嵌入精确 Owner 源文件内容和 Blob pin。中文 companion 保留相同源 pin，并提供双向语言链接。

## 2. 结构读回

| 指标 | Owner 源文件 | 英文 | 中文 |
|---|---:|---:|---:|
| 标题数 | 14 | 14 | 14 |
| 表格行数 | 0 | 0 | 0 |
| 行数 | 151 | 154 | 154 |

所有工件均已从 GitHub 读回。英文内容与源文件完全一致。中文保留全部标题及完整合同/决议结构。

## 3. 语义复核

- C 仍是实际成功 Provider/Runtime Submit 证据的唯一生产者；C 不拥有 I authorization、D ForgetFence、coordinator 运营或 G Applied。
- ParticipantIntent 必须先于 Provider side effect；I single-use receipt terminalization 和 D complete-lineage clearance 必须先于 reservation；Provider 在稳定幂等合同下恰好调用一次。
- CSubmitOutcome 区分 ACCEPTED、确定的 REJECTED 和 UNKNOWN/IN_DOUBT；未知 outcome 不得作为新 transaction 重试，也不得释放 I/D barrier。
- CausalOrderTerminalProof 绑定 C/I/D 证据，但不替代 Owner 权威。
- C 明确接受精确 CGH-APPLIED-1.1 recovery-batch 修订，并列明例外；固定到 A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819` 和 companion COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`。
- C 的 JF-10 bridge Issue #8 决议另行固定到列明的精确 A/I/D/Storage/H 工件，并保留单一 PolicyDomain 限制。
- H Schema/密码学互操作、coordinator/participant registry 部署、Provider 专属同 key 恢复，以及 C-CO/H-JF10 测试执行仍开放或 NOT RUN。

本次针对性翻译复审未发现重大语义偏差。

## 4. 结论

**双语语义一致性：针对该精确源 Blob，PASS。**

**C36-AP-01 在 C 源决议层面 RESOLVED：** C 的独立 cross-authority causal-order 合同明确接受精确 CGH-APPLIED-1.1 recovery-batch package，并规定 C 自有 CSubmitOutcome/Provider 证据。这不解决 H36-AP-09、H Wire Schema/SDK 映射、I/D/Storage 实现、coordinator 部署、G 独立接受门禁或任何一致性/生产门禁。
