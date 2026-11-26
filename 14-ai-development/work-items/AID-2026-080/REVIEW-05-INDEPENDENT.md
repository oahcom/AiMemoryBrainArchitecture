---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "The verdict reproduced below is the reviewing session's own text, in its original Chinese, extracted from its reply and not translated or summarised. Its blocking items are dispositioned in the manifest's review.round_5, not in this file, so that the reviewer's words stay unedited next to the account of them."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Independent governance review - AID-2026-080, round 5

Round 5 of the exact-Head governance review required by section 9. Same reviewing session as
rounds 1-4 (`6b07448b-ac9c-83ec-9115-f056a313f972`), reading the branch through its own GitHub
connector.

| field | value |
| --- | --- |
| Head reviewed | `a37cd5bb95bd26a50752231e5dbc1dc71168e884` |
| PR under review | #1266 |
| Verdict | `NEEDS REVISION` |
| Blocking items | 2 |
| Round 4's open items | both closed on content |

Round 5 is the first round that checked the base of the branch rather than only its contents, and
it is the round that caught two things I had wrong.

**The base was stale, and that is a blocking item.** `a37cd5bb` is a merge commit whose second
parent is `d5107f68`; by the time round 5 read it, `main` had advanced to `baca092b`, 20 commits
further, and that increment modifies `INDEX.md`, which this PR also modifies. `mergeable: true` with
`mergeable_state: behind` is exactly the state that section 6.1.3 says must be revalidated after a
base update, and green checks on the old combination do not stand in for it.

**A number in the review request was wrong.** I gave round 5 `31385bc1` as "`origin/main` at this
Head". Verified: `31385bc1` is an ancestor of `d5107f68`, 21 commits back. It was `main` when the
branch was cut, not `main` when the branch was read. The reviewer used the commit graph instead of
my table, which is the correct behaviour and is why the error was found.

**F3 was answered but the reason was overstated.** I had written that `DM-10` is the only rule
constraining `modification_status` and that the policy constrains it nowhere else. Wrong: Rule L1
(stale approval, policy `:160` EN / `:162` ZH) is the normative requirement, and `DM-10` is its
machine check. The conclusion survives because L1 does not fire on a `Draft` with
`approved_version.value: null`, but the description of the rule's source had to be corrected. It is
corrected in `review.round_4.non_blocking_checked`.

Round 5 also did something I had not done: it checked `32f87d46`, the Head PR #1240 actually merged
at, and found 16 successful check runs there. My record had stopped at `fa6e227b`, the Head I pushed
the repair to. The stronger statement was available and I had not made it.

## Verdict, verbatim

The text below is the reviewer's reply, unedited and untranslated. It is in Chinese because that is
the language it was written in; translating it would put my words where its words belong.

```
我已核对 PR #1266 的实际 Head `a37cd5bb95bd26a50752231e5dbc1dc71168e884`，而不是把提示中的描述当作证据。

**当前 PR 状态：** open，`mergeable: true`、`mergeable_state: clean`。实际 PR 文件列表正好是四项：新增 `REVIEW-04-INDEPENDENT.md`，修改 manifest、`session-evidence-1201.md` 和 `INDEX.md`。精确 Head 上有 20 条 check runs；其中较早的一次 `Session Evidence` 失败，随后同一 Head 的重跑成功。不能把历史失败抹掉，但最新该项结果是成功。 

## 总裁定：NEEDS REVISION

**PR #1266 的治理记录主体正确，但当前 `a37cd5bb` 不能作为可合并候选接受。** 阻断原因是它相对于当前 `main` 已落后，且 `main` 的增量修改了本 PR 同样修改的 `INDEX.md`。这触发了规范 §6.1.3 的 base 更新后重新验证要求。

### 1. Round 4 的裁定与 pre-merge deviation 是否记录正确？

**实质上正确。**

逐项核验：

- `REVIEW-04-INDEPENDENT.md` 明确记录了 Round 4 的精确 Head `7e9c9f3d…`、`NEEDS REVISION`、两项阻断事项，以及对 `489b6048 → f7bc0789` 的独立增量审查。正文包含完整的审查意见，而不是把它改写成 `APPROVED`。
- manifest 的 `review.round_4` 保存了相同的裁定结构，并区分 `open_at_verdict` 与事后处置，没有把后来的修复冒充成 Round 4 当时已经检查过的内容。
- `session-evidence-1201.md` 和 INDEX 同步记录了 Round 4 历史，没有覆盖 Round 3 的记录。
- GitHub 事实确认 PR #1240 已合并：Head `32f87d46…`，merge commit `8d90843a…`，合并时间 `2026-11-26T06:24:13Z`。该最终 Head 有 16 条 check runs，全部成功。因此 F1 的修复不只是停留在 `fa6e227b` 的检查结果上；最终合并 Head 也有完整的绿色检查记录。
- F2 正是本 PR 新增 Round 4 记录，已在内容层面补齐。

**pre-merge deviation 的表述也正确，而且没有试图用事后审查抵销它。** #1215 与 #1240 的审查 Head 和合并 Head 不同；记录明确说两次都没有在实际合并 Head 上完成事前审查，也没有把两次增量当作审查覆盖。这是正确的历史陈述。

不过，当前 PR 的 base 有一个必须处理的新问题：

- PR #1266 的 Head `a37cd5bb…` 是一个 merge commit，其第二父提交是 `d5107f68…`。
- PR API 当前报告 base 是 `d5107f68…`，而实时 `main` 已前进到 `baca092b…`。
- `d5107f68… → baca092b…` 有 20 个新提交；其中包括对 `14-ai-development/work-items/INDEX.md` 的修改，而 INDEX 正是 PR #1266 修改的文件。
- 当前 GitHub PR 状态为 `mergeable: true`，但 `mergeable_state: behind`。

另一个基线差异：你提供的 `31385bc1` 不是当前实时 `main`，也不是 `a37cd5bb` 的第二父提交；它比 `d5107f68` 早 21 个提交。这里我以 GitHub 当前分支和提交图为准。

因此，§6.1.3 要求对更新后的 base 与 PR Head 组合重新验证。由于新 base 也改了 INDEX，不能仅以 `a37cd5bb` 上的绿色检查或本轮对旧组合的审查代替。**需要把当前 main 合入 PR 分支，重新跑检查，并审查更新后的最终候选 Head。** 这不是对 Round 4 记录内容的否定，而是 PR #1266 当前仍未满足的合并前置条件。

### 2. F3 是回答了，还是回避了？

**F3 已经实质回答，不是回避；但 manifest 对规则来源的描述有一处不准确。**

我核对了两份文件在 `7e9c9f3d` 上的 frontmatter：

- `REVIEW-AMENDMENT.md`：`decision_status: Draft`，`approved_version.value: null`，`modification_status: Unchanged`。
- `session-evidence-1201.md`：同样是 `Draft`、`approved_version.value: null`、`Unchanged`。

因此，结论成立：**没有规则要求这两份 Draft 文件仅因为正文被编辑，就必须把 `modification_status` 改为 `Modified`。**

但 manifest 中这句：

> `DM-10` is the only rule that constrains this field … The policy constrains the field nowhere else.

不准确。政策中还有明确的 **Rule L1 — stale approval**：已批准内容在 `approved_version` 后发生变化时，`modification_status` 必须变为 `Pending-Reapproval`。DM-10 是这项要求的机器检查规则；L1 本身也是规范性约束，不能说政策在别处完全没有约束该字段。

这不改变两份 Draft 的结论：它们没有已批准版本，L1 的 stale-approval 条件并未触发。更精确的说法应是：

- L1 是 stale-approval 的规范要求，DM-10 是对应的机器检查；
- 两份文件均为 Draft 且 `approved_version.value: null`，不满足该要求的触发条件；
- 政策没有另外规定“凡正文编辑就必须设为 Modified”。

因此，F3 不是被搁置，也不需要为了制造一个未定义的语义而翻转字段；需要修正的是“DM-10 是唯一约束来源、政策别处没有约束”的过度表述。另：我没有独立重算 `294 / 149 / 112` 的全库统计，因此不把这些数字作为本轮结论的依据。

### 3. 最终处置建议

当前需要区分三个不同结论：

1. **Round 4 的两个开放事项：内容上已闭合。** F1 在合并前修复并在最终合并 Head 上有 16 项成功检查；F2 由本 PR 记录。
2. **F3：实质回答了。** 不要求 Draft 文件翻转 `Unchanged`；但应把 L1 与 DM-10 的关系写准确。
3. **AID-2026-080 的合规状态：不能标记为 compliant。** 两次 pre-merge exact-Head deviation 都是已经发生的历史事实，没有后续操作能追溯性地满足当时的事前审查要求。

所以，我不建议把这个 work item 描述成“合规完成”。**在 PR #1266 更新到当前 main、重新验证并通过审查后，可以诚实地将 work item 关闭为 `MERGED`，同时保留两次 deviation；`MERGED` 不等于 `COMPLIANT`，也不等于 Owner acceptance。** manifest 现有 `acceptance.status: NOT_ASSIGNED` 也应继续与合并状态分开。

当前 `a37cd5bb` 的裁定仍是 **NEEDS REVISION**：阻断点是 §6.1.3 的 base 更新后重新验证；F3 的措辞则是应一并订正的准确性问题，而不是要求修改两份 Draft 的字段值。
```

## What this round settles

Round 5 separates three conclusions that had been running together, and the separation is the
useful part:

1. Round 4's two open items are closed on content. F1 was repaired before #1240 merged and the
   merged Head `32f87d46` carries 16 green checks; F2 is the round-4 record.
2. F3 is answered. No rule requires the two `Draft` files to say `Modified`; the correction is to
   how the rule's source is described, not to the field values.
3. AID-2026-080 cannot be marked compliant. Both pre-merge exact-Head deviations are historical
   facts, and no later action can retroactively satisfy a requirement that applied at merge time.

The work item can honestly be closed as `MERGED` once this branch is updated and revalidated, with
both deviations preserved. `MERGED` is not `COMPLIANT`, and it is not Owner acceptance;
`acceptance.status: NOT_ASSIGNED` stays separate from merge state, as it already is.

Nothing in this file claims `APPROVED`. It is not a human review; it is session-level independence
under section 5.
