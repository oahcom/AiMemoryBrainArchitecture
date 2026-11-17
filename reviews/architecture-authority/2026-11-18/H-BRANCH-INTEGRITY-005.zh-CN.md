# Session 4 — A：H 分支基线完整性事件
# Session 4 — A: H Branch Baseline Integrity Incident

- 日期：2026-11-18
- 仓库：`oahcom/AiMemoryBrainArchitecture`
- Main HEAD：`e52594f181d2edb77448adcfed64a0fbdffaf3aa`；Tree `7096e0bc3fdc9a390fccff388f9261522fa424f2`
- H 分支 HEAD：`0277a8b9ee63be850acc0b8b1b08625524aaa33b`
- H 父提交 / 上次审查的 H HEAD：`0d36324457e39bd50ad56ae902d477c4ea765b61`
- 裁决：**DEFERRED — CRITICAL BASELINE INTEGRITY REGRESSION**
- 范围：只读发现与治理升级；不修改 Owner 分支。

## 1. 事件摘要

继续审查 H 1.2.15 Issuer-side 闭环时，发现 H 分支前进了一个提交：
`0277a8b9ee63be850acc0b8b1b08625524aaa33b`
提交信息：`docs(H): record exact Applied delivery evidence mapping decision`。

该提交的父提交正是上次审查的 H HEAD `0d36324457e39bd50ad56ae902d477c4ea765b61`。GitHub Commit Endpoint 报告 160 additions、92,969 deletions。Compare Endpoint 识别出 205 个文件删除和 3 个 Workflow 重命名。当前 H 递归 Tree 仅有 7 个条目，包括两个新 Phase 3.8.23 Review 文档和三个 Workflow。此前的 1.2.15 Schema、Validator、Tests、Fixtures 以及大部分 H Protocol 源文件均不在当前 H 分支 Tree 中。

这不是正常的增量证据更新，而是破坏性的分支基线变更，导致上一轮 H 源 Bundle 无法从当前 H HEAD 获取。

## 2. Main 隔离核验

当前 Main HEAD 为 `e52594f181d2edb77448adcfed64a0fbdffaf3aa`，Tree 为 `7096e0bc3fdc9a390fccff388f9261522fa424f2`，与此前记录的 Main Tree 完全相同。破坏性 H 分支提交不在 Main 上。本轮未发现 Main 文件树受到影响。

A 审查 PR #67 仍为 OPEN / DRAFT / 未合并，仍保持原来的双文件报告 Head `abd9156d3e9aa171eeb03693b2be1e722e8d33ff`。它没有包含或合并 H 分支删除提交。

## 3. 对此前 1.2.15 结论的影响

此前成功的 CI 证据仍只属于旧 H Commit `0d363244...`：
- Provider Outcome Run `44079842914`：91 项测试，0 失败。
- Recovery Cutoff Run `44079842878`：288 项测试，22 项跳过，0 失败。

这些 Run 不能验证新的 H HEAD `0277a8b9...`。本轮没有建立当前 HEAD 的 CI 证据。由于 1.2.15 Schema/Validator/Test 文件不在当前 H Tree 中，之前的精确 Bundle 不能继续被视为当前 H 分支候选。

Issuer-side C-before-H-signing 缺口、生产 Trust/Key Lifecycle、Origin Transport Authentication 和 Durable Replay 缺口仍未解决。此次分支回归是新增的 Critical Blocker，而非对上述条件的替代。

## 4. 必须执行的恢复动作

| ID | Owner | 必需证据 | 关闭标准 |
|---|---|---|---|
| H-BI-01 | H | 明确解释提交 `0277a8b9...` 的意图与范围；说明大规模删除是有意、误操作还是分支迁移 | H Owner 针对精确 Commit 留下决议 |
| H-BI-02 | H | 恢复或正式迁移权威 H Protocol 源、Schema、Validator、Tests、Fixtures 和 Workflows；不得静默丢失现行合同 | 精确当前 Tree Inventory 和 Source Pins |
| H-BI-03 | H | 基于恢复后的当前 H Tree 发布新的不可变 1.2.15 Candidate Manifest | 精确 Blob Manifest 已读回 |
| H-BI-04 | H | 针对恢复后的精确 H HEAD 重跑必需 CI；确认关键 1.2.15 Suite 没有跳过或遗漏 | 成功 Run/Job SHA 证据 |
| H-BI-05 | C + I + A | 对恢复后的精确 Bundle 重新审查；旧 Review 不自动转移到变更/缺失的 Blob | 精确版本 C/I 决议与 A 复审 |

不虚构截止日期。只有规定证据发布并完成读回后，条件才可关闭。

## 5. 治理裁决

**DEFERRED。** 将 H 1.2.15 视为**当前不在 H 分支 HEAD 中**。此前 CI 仅是旧 Commit 的历史证据。不得声称当前 H Conformance、Schema Freeze、Gate A 完成、Gate B/C 就绪或生产授权。

本协调审查不擅自 Revert、Force-push 或以其他方式修改 H Owner 分支。H 必须先给出意图与恢复决议。不得合并 PR、关闭 Issue 或解除 Gate。
