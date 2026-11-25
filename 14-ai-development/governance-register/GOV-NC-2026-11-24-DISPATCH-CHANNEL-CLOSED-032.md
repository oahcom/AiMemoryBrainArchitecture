---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "Both admissions were run, not read. The rejection of AID-2026-055/manifest.yaml was produced by scripts/ci/check_repository_hygiene.py --base HEAD~1 --head HEAD on a branch containing exactly that file, and it is also the CI annotation on PR #889 check run 138238290710. The admission of .md came from the same script's ALLOWED_DOCUMENT_SUFFIXES read at main 215f87b5, and from the fact that the three .md files in this change passed the same gate. The dating of cfcafc98a and a3c6280aa came from git log --diff-filter=A."
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
    en: "docs/en/14-ai-development/governance-register/GOV-NC-2026-11-24-DISPATCH-CHANNEL-CLOSED-032.md"
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-24-DISPATCH-CHANNEL-CLOSED-032.md"
---

# GOV-NC-2026-11-24-DISPATCH-CHANNEL-CLOSED-032

**Status:** `OPEN` / `MEASUREMENT_ONLY` / `NO_IMPLEMENTATION`
**Nature:** `REGISTER_ONLY / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 215f87b5`
**Register author:** orchestrator session acting as owner-proxy. **Not** an independent reviewer, **not** the accountable owner.

---

## 1. 结论先行

自 `cfcafc98a`（#844，2026-11-24，`ci(hygiene): admit new files through an explicit whitelist`）起，**任何新的 AID 工作单都无法登记**。

原因是准入白名单放行 `.md` 与源码后缀，`.yaml` 只在 `.github/workflows/` 与 `.github/actions/` 下放行；而每个 AID 的载体是 `14-ai-development/work-items/AID-…/manifest.yaml`，没有任何规则覆盖它。

实测（本地跑同一支闸门，不是读代码）：

```
$ python scripts/ci/check_repository_hygiene.py --base HEAD~1 --head HEAD
::error::new-file admission violation: no allowlist rule for
        '14-ai-development/work-items/AID-2026-055/manifest.yaml'
```

这条不是新发现的边角：它是**发派通道本身被关闭**。仓库现在有 30 份登记未测、多份标着 `OPEN` / `NOT_ASSIGNED`，而把它们变成工作的唯一机制——AID 工单——已经无法新建。

本登记记录这个闭合，并说明为什么本会话不自行打开它。

---

## 2. 时间线是硬的

| 事件 | 提交 | 日期 |
|---|---|---|
| `AID-2026-054` 的 `manifest.yaml` 合入 | `a3c6280aa`（#823） | 2026-11-23 |
| 准入白名单引入 | `cfcafc98a`（#844） | **2026-11-24** |
| 本会话尝试登记 `AID-2026-055` | 分支 `gov/aid-2026-055` | 2026-11-24 |

白名单比最后一支工作单晚一天。所以 `054` 的载体在规则生效前已经存在，它不构成「规则本意允许」的证据——它只是没被规则看见。

**这是一个纯时间事实，不是推断**：`git log --diff-filter=A` 给出 054 manifest 的引入提交；`git log` 给出白名单脚本的引入提交；两者的日期关系如上。

---

## 3. 白名单的实际内容

`scripts/ci/check_repository_hygiene.py` 的 `is_allowed_new_path()` 放行五类：

| 规则 | 内容 | 覆盖 `manifest.yaml` |
|---|---|---|
| `ALLOWED_DOCUMENT_SUFFIXES` | `.md` `.rst` `.adoc` | 否 |
| `ALLOWED_SOURCE_SUFFIXES` | `.py` `.sh` `.rs` `.ts` … | 否 |
| `ALLOWED_CONFIG_PATHS` | `.gitignore` `Cargo.toml` `package.json` 等**精确文件名** | 否 |
| 根目录 `requirements*.txt` | — | 否 |
| `.github/workflows/` 或 `.github/actions/` 下的 `.yml`/`.yaml` | — | 否 |

五类之外一律拒绝。`manifest.yaml` 不在任何一类。

对比之下，`scripts/check_bilingual_docs.py` 把 `14-ai-development/work-items/` 整体列入 `PAIR_EXEMPT_PREFIXES`，理由写着「operational records or prompt templates, not bilingual specifications」——也就是说，**同一批目录在双语闸门眼里是正式的运营记录，在准入闸门眼里是不被承认的文件类型**。

---

## 4. 为什么本会话不自己改那一行

需要的改动是一行：让 `14-ai-development/work-items/` 下的 `.yaml` 通过准入。它落在 `is_allowed_new_path()` 里，也就是闸门源码里。

本会话在本系列中一贯拒绝自行修改闸门源码——`AID-2026-054` 的 prompt 明确把 `check_bilingual_docs.py` 列为只读，本会话也没有违背过。若在此处破例，破例的理由只能是「我需要它」：

> 唯一想要这扇门打开的主体，正是唯一有动机把门开得比需要的更宽的主体。

这与 `SELF-REVIEW-007`、`SELF-AUTH-002` 的结构相同，只是换了一个位置。仓库当前只有**一个可写身份**、**零次独立审查**（README 记录的 675 个 PR / 0 条 APPROVED），所以「由需要者自行放宽」正是缺的那道检查本身。**本会话不以 owner-proxy 的身份签发这项放宽。**

> **〔2026-11-25 附注〕** 本句以「一个可写身份」与「零次独立审查」——账号层事实——作为「由需要者自行放宽正是缺的那道检查」的理由。§5 已于 2026-11-24 由 `2eb4e352`（PR #935）修订为会话层判据（见 `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`）：同一 GitHub 身份下的另一会话即可构成独立审查。`/pulls/{n}/reviews` 只返回 `user.login`，不返回会话，故「同一身份 ⇒ 同一会话」这一步在该载荷里无法核实。此处应读作「账号层不独立、会话层未核实」。**结论本身成立，但换了一条不需要 §5 的理由**：自我签发的放宽由构造即未被验证——需要放宽的一方自己签发，无论谁审查、审查是否独立，这次放宽都没有经过第二方核对，所以「由需要者自行放宽」仍是缺的那道检查。**不成立的是**「零次独立审查」作为会话层断言；在账号层，`APPROVED = 0` 仍是一个测量（README 记录的 675 个 PR / 0 条 `APPROVED`），它说明没有批准，但不说明没有独立会话审查。

因此本会话的处置是：记录，不实施；把工单内容保留在 §6，等放宽落地后一分钟内即可登记。

---

## 5. 这不是要我发明的新缺陷，是两条现有记录的交叉

- 准入白名单是 `#844` 明确引入的，提交信息自己说「explicit whitelist」，所以它的排他性是设计意图，不是遗漏。
- 工作单载体是 `manifest.yaml`，这是 `AID-2026-001` 以来的既有形态，`INDEX.md` 的每一行都链接到 `manifest.yaml`。

两者单独看都合理。交叉处没人测过：**白名单引入时没有同时测「现有工作单形态能否再次被创建」**。这与登记 030 的形态相同——修复本身正确，修复的副作用没人测。

---

## 6. 待登记的工作单内容（放宽落地后可直接使用）

保留在此，以免测量结果随未合并的分支消失。

**对象**：`scripts/governance/evidence/test_gate_normative_roots.py` + `.github/workflows/repository-hygiene.yml`

**依据**：`main @ ef7266db` 实测 `Ran 52 tests / FAILED (failures=3, errors=21)`，且 `grep -rn 'test_gate_normative_roots' .github/` 零命中。原因见 `GOV-NC-2026-11-23-UNREACHABLE-GUARD-030` §4：`load_gate()` 只设 `mod.ROOT`，而 `changed_status()` 用 `cwd=REPO_ROOT`，于是临时仓库里的测试在真仓库里跑 `git diff`，退出 128。

**验收条件（可逐条复核）**

1. 51→52 个测试不变，0 failures、0 errors，不删、不跳、不标 `expectedFailure`。
2. 改完后，该文件内任何测试都到不了真仓库——测试通过不能依赖真仓库恰好干净。
3. 逐条归因表：每个问题的测试名、异常文本、是否被 helper 修复解决。
4. 变异测试甲：删掉 `and not partial_side_by_side`，至少一个测试必须变红，贴出输出。
5. 变异测试乙：把 `cwd=REPO_ROOT` 改回 `cwd=ROOT`，套件必须变红；若不红，说明 helper 修复让套件对它该检测的变更变得无感，必须写明而不是绕过。
6. 在 `repository-hygiene.yml` 既有的 `for f in \` 列表里按字母序加一行。
7. `scripts/check_bilingual_docs.py` 只读；`register_closure: NOT_GRANTED`。

**为什么这些条件重要**：这套测试存在的目的就是抓住一次回归，而它被静默解除武装。让它变绿而不证明它能变红，等于用更好看的数字重复同一次失效。

---

## 7. 本登记不主张什么

- 不主张白名单本身错了。`.yaml` 任意放行会让快照与数据文件涌入，`#844` 的理由成立。
- 不主张回退 `#844`。需要的是一条**前缀受限**的规则，不是没有规则。
- 不主张本会话有权实施它，也不主张下一位读者没有。签发权限在 Owner，不在这里。
- 不声称 30 份未测登记中的任何一份因此变红或变绿。它们的状态不被本登记改变。
- 不指派独立审查。该席位 `NOT_ASSIGNED`，本登记不能填。

**阻断链：** 独立审查 `NOT_ASSIGNED`，放宽授权 `NOT_AUTHORISED`，sponsor / accountable owner `NOT_ASSIGNED`。

---

## 8. 复现

```
repo:  oahcom/AiMemoryBrainArchitecture
main:  215f87b5

# 1. 白名单拒绝工作单载体（在含 manifest.yaml 的分支上）
python scripts/ci/check_repository_hygiene.py --base HEAD~1 --head HEAD
-> ::error::new-file admission violation: no allowlist rule for
   '14-ai-development/work-items/AID-2026-055/manifest.yaml'

# 2. 白名单放行 .md
#    同一分支只含 .md 变更时，同一条命令输出
-> Repository new-file admission passed: N new path(s) checked.

# 3. 时间关系
git log --diff-filter=A --format='%h %ad %s' --date=short \
  -- 14-ai-development/work-items/AID-2026-054/manifest.yaml     # -> a3c6280aa  2026-11-23
git log --format='%h %ad %s' --date=short -2 \
  -- scripts/ci/check_repository_hygiene.py                      # -> cfcafc98a  2026-11-24

# 4. 被闭合的工单所依据的测量
python -m unittest scripts.governance.evidence.test_gate_normative_roots
-> Ran 52 tests in 72.708s / FAILED (failures=3, errors=21)
grep -rn 'test_gate_normative_roots' .github/
-> (no output)
```
