# Prompt snapshot — AID-2026-268 ledger hotfix

<!--
Reconstructed record of the prompt delivered to the planning session
(reply id 6b09312b, prompt name prompt-unblock-ledger-pr.md). Passages the
planning session quoted back verbatim are reproduced exactly; the
surrounding request wording is as delivered. The transmitted bytes were not
captured to a file at send time, so manifest.yaml records
executed_prompt_provenance as NOT_VERIFIED rather than VERIFIED.
-->

重要反转：work-item uniqueness 规则在 main 上已经改了，新增路径不再被拒。ledger hotfix 可以走真实 PR，请你改判 Q2。

## 实测

main 上现在这一版是 16744 字节 / 445 行，只校验 `ROOT/<AID|FIX>/manifest.yaml` 的声明唯一性，**没有 `new_paths` 概念**。

隔离 worktree 探针（在 AID-2026-051 下新增 session-evidence 文件）：

```text
python scripts/ci/check_work_item_uniqueness.py --base f0843a8f… --head <probe>
rc=0
WORK-ITEM UNIQUENESS: PASS (candidate_ids=167 target_ids=167 introduced=0 shared=167 duplicate_declarations=0)
```

## 需要的四项

1. 证据文件路径与**完整文件正文**（要能被 `scripts/governance/session_evidence/validate.py` 解析；它要求 `Session role / use case`、`Actual AI input`、`AI-visible output` 三节，我按你给的原文落盘）。
2. PR body（按仓库模板）：Work Item ID、Related issue(s)（#1349）、AI-assisted work: YES、Session evidence reference(s) 指向上面的路径、Base/Head SHA 的写法（我会填实际值）、PR-GOVERNANCE-001 状态。
3. 是否更正 #1349 里「awaiting a non-AI maintainer」那条旧 hand-off。
4. 如果必需检查全绿，谁执行 merge。

## 边界

- 只改 ledger 两行 `repin_commit`（`6045af65…` → `2ab66153…`），不动 checker、baseline、manifest pin 值、AID-2026-261 的 sentinel 声明。
- 不伪造任何检查结果；未实测写 NOT_MEASURED。
