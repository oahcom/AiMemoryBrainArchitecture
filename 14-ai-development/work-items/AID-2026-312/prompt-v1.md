# AID-2026-312 — prompt snapshot v1

Role: IMPLEMENTATION_SESSION
Work item: register the LINE 01 development-baseline closeout (PR #1411) as a work item.
Repository: oahcom/AiMemoryBrainArchitecture

This snapshot is the executed order plus the Owner rulings that authorized it. It is a
transcription: the prompt reached the execution session as the `### PROMPT-01` block of
`scripts/accounts/acct6/replies/reply-6b08f751-112543.md` (prompt `63-wb-convergence.md`),
and the rulings below are the Owner's answers to `scripts/prompts/64-wb-decisions.md`
items A and C. Byte-for-byte identity with the delivered prompt is therefore not claimed
(`executed_prompt_provenance: NOT_VERIFIED`).

## 1. Executed order — PROMPT-01 (verbatim from reply-6b08f751-112543.md)

```text
### PROMPT-01

你继续担任 AI 大脑架构项目的执行者。本轮接受 WB 总控的开发基线收敛授权。

仓库：oahcom/AiMemoryBrainArchitecture
默认分支：main
总控提供的基线：788fbc011877a14976fc0a974ffe2e013dd9991b
以上 SHA 只是核验起点。第一步必须自行执行 git ls-remote、git fetch，并用 GitHub API 核实远端 main、PR 和 Issue 状态。不得把本地 checkout SHA 当作 main。

已知历史候选 PR：
#1358 782460c2
#1336 f53cf728
#1335 75ef044c
#1334 b5762c48
#1325 0f7dfbc9
#1321 65b50760
#1309 df192ede
#1305 319c3f3a
#1297 e476fef3

已知历史基线中的事实：
- #1329 已由 GitHub API 实测为 merged。
- #1329 merge commit = 76684cb28b132917b3f250e9bf6430713e61c362。
- 总控提供的 788fbc... 包含 #1329 的合并历史。
- 本地旧 checkout 2afe24cd 不是 main。
以上仍须在执行时重测。

本轮唯一任务：
完成 AI 大脑架构项目的开发基线历史记录纠错与证据收敛，形成一个可审计的最终 closeout 记录。

按以下动作序列执行：

1. 刷新远端 main，列出全部 open PR 和相关 Issue 的实际状态。
   对每个相关 PR 获取：
   number、state、draft、head SHA、base SHA、mergeable_state、merge commit SHA、check-runs、required checks。
   无法读取的字段写 NOT_RECORDED，不得推断。

2. 对 #262：
   - 重新读取完整 Issue 正文。
   - 核验 E1–E6 六个目标位置。
   - 核验 AC 实际计数及 Owner-D 的 7/1 口径。
   - 核验 AC2 的引用链，区分 7156638485 与后续纠正 7157542128。
   - 在保留其他最新正文内容的前提下，完成既定六步正文纠错：
     L286 [x]→[ ]；
     追加 PARTIAL 说明；
     更新 §8 Current Status；
     更新 Remaining Gaps；
     更新中文前四条；
     更新中文第五条。
   - 写入前保存原始正文、正文 SHA/版本信息；写入后重新读取完整正文，逐项比对六项。
   - 不得把 7/1 预期口径冒充为实测结果。

3. 对 #265：
   - 不得恢复 NOT_RECOVERED 的三条 AC 为已完成。
   - 追查原始证据来源。
   - 无法恢复的内容永久保留 NOT_RECOVERED，不得根据协调层转述补造。
   - 将当前终态和证据缺口明确登记。

4. 对 #266：
   - 核验补清单条目的原始要求。
   - 完成开发基线内可验证的记录补齐。
   - 不改变领域 Owner 的架构决定。

5. 对 #1220：
   - 逐条复核十二个历史 blob pin。
   - 特别核验以下六个已知 mismatch：
     05-memory-runtime/README.md:
       pinned 107c225b / actual 13570e9f
     docs/en/05-.../README.md:
       2fac4274 / ad36c55c
     docs/zh-CN/05-.../README.md:
       9881fd88 / a5c9e3d9
     AID-2026-100/evidence.md:
       87adf4a8 / ae46c7a4
     EN mirror:
       da156fe2 / 425e5eaf
     ZH mirror:
       d750ef55 / fda38f13
   - 必须重新计算 blob SHA，不得直接沿用上述结果。
   - 记录历史 pin 与当前 blob 的区别，不得把历史错误伪装成历史正确。
   - 逐项核验 #1220 的状态事件操作者。缺失的操作者写 NOT_RECORDED。

6. 对 #1248、#1249、#1281：
   - 核验 canonical session_evidence 是否存在。
   - 核验 AID-2026-096 两份证据文件的删除及后续恢复情况。
   - 核验 Work Item ID: NONE 是否已经补登记。
   - 每项附当前 main 上的 exact path/blob SHA。
   - 缺失的自然人归属不得补造。

7. 完成 ATTRIBUTION.md 的开发基线归属记录。
   署名只能采用：
   user-authorized operator (delegated by account owner)
   同时注明：
   代理登记，非自然人 Owner 签署。
   不得将代理署名写成自然人 Owner 的亲自签署。

8. 核验本地 checkout 与远端 main 的差异。
   将 patrol.log 中把 2afe24cd 当 main 的错误登记为历史台账纠错。
   不得擅自把原工作分支强制重置到 main。

9. 为上述工作形成唯一的开发基线 closeout 记录。
   每项包含：
   原始状态、实测状态、处理动作、exact SHA、blob SHA、验证命令、验证结果、遗留缺口。

授权边界：
- 允许开发基线内的文档记录修正、证据登记、提交和 Draft PR。
- 对 #262 的正文修改，本提示词明确授权执行上述六项精确修改；必须先读取最新正文，保留无关内容，并保存前后证据。
- 不授权合并任何 PR。
- 不授权关闭或重新打开任何 Issue。
- 不授权改号、重分配 Work Item ID。
- 不授权改变 Runtime、Validator、API、Schema 或 Wire 语义。
- 不授权替 D/I/F 等领域 Owner 签署架构接受。
- 不得把缺失的自然人签署改写成代理签署后宣称已满足自然人审查。
- 不得伪造 CI、测试、review 或 merge。

OUT-OF-SCOPE(dev-baseline)：
真人专家审查、生产激活、Runtime/API/Schema Freeze、Migration、Deployment、Architecture Exit。
这些事项不得阻塞本轮收敛。

最终验收：
A. 六步 #262 修改均能从最新 Issue 正文回读验证。
B. #265 三条 NOT_RECOVERED 状态未被伪造。
C. #266 补清单可追溯。
D. #1220 十二个 pin 均有重新计算结果或明确 NOT_VERIFIED。
E. #1248/#1249/#1281 均有独立处置结果。
F. ATTRIBUTION.md 代理署名符合规定。
G. 本地 main 身份错误已纠正留痕。
H. 所有提交有 commit SHA，所有文件有 blob SHA。
I. 所有测试有实际命令、原始输出和对应 commit SHA。

回报格式：

STATUS: PARTIAL / OPEN / BLOCKED / NOT VERIFIED

1. 基线：
   remote main SHA：
   local HEAD：
   fetch 时间：
2. 处理清单：
   每项原始状态 / 最终状态 / 证据。
3. Issue 正文修改：
   修改前后证据及回读结果。
4. 提交：
   branch / commit SHA / changed files / blob SHA。
5. 测试：
   命令 / 原始输出 / commit SHA。
6. 未完成事项：
   精确原因及 OUT-OF-SCOPE 分类。
7. 禁止事项核对：
   merge / close / 改号 / 伪造签署均须明确报告。

没有完成的项目必须如实保留 PARTIAL、OPEN、BLOCKED 或 NOT VERIFIED。
不得用总结性文字代替逐项证据。```

## 2. Ruling source — 64-wb-decisions.md, item A (verbatim)

**A. PR #1411 的 Session Evidence 必然红。** 它声明 `AI-assisted work: YES` + `Work Item ID: NONE`，而 `validate.py:1861` 只允许 `NONE` 配 `NO`。执行者选择如实红，不伪造 `NO`。三个选项：
- A1：分配一个新 AID（当前可信空闲 ≥ 241，需先扫再原子占位），把 closeout 登记成工作项；
- A2：保持红 + Draft，等后续有人认领；
- A3：其他（请给具体形态）。

## 3. Ruling source — 64-wb-decisions.md, item C (verbatim)

**C. `2002::1`（6to4）能绕过 SSRF 守卫**：`is_global=True`，守卫不解包 `sixtofour/teredo/ipv4_mapped`。这是 pre-existing（main 上同样失败）。是否授权开一个新 AID 修守卫并补测试？

## 4. Owner ruling delivered to the executing session (verbatim)

```text
A1 — keep PR #1411's `AI-assisted work: YES`, never fake `NO`; scan for a trustworthy free
AID, then allocate atomically, and register the closeout as a work item.
```
