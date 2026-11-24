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
      last_verified_date: "2026-11-23"
      last_verification_note: "§10 的全部数字在 2026-11-23 通过 GitHub REST API 逐项取得：最近 45 个已合并 PR 的 reviews 逐个查询；branch protection 的 required_pull_request_reviews 键缺失；18 个 workflow 全文检索 reviews/APPROVED/reviewDecision 无执行命中。非引用。"
    usage_status: Active
    modification_status: Modified
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
    source: "14-ai-development/governance-register/GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008.md"
    en: "docs/en/14-ai-development/governance-register/GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008.md"
    zh-CN: null
---

# GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008

- 登记编号：GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008
- 状态：`OPEN` / `ACTIVE` / 门禁实现被零审查合并
- 发现时间：2026-11-21T07:10Z（取数时间 2026-11-21T07:20Z）
- 观测对象：仓库 `oahcom/AiMemoryBrainArchitecture`，PR #423 / Issue #420
- 前置登记：005（CI 零执行）、006（门禁死锁）、007（自我审查合并）

## 1. 结论先行

PR #423 修改了双语门禁实现本身（`scripts/check_bilingual_docs.py` **+110 −3**，另加测试 +40），并修复一个真实缺陷（Issue #420：豁免可在引入文件的同一 commit 自注册）。

它被合并了，且：

- `reviews = 0`——**没有任何审查**，不是自我审查，是零审查；
- 三条 check run 全部 `conclusion = failure`、`steps = 0`——job 未启动；
- author = merger = `oahcom`；
- created 06:53:12Z → merged 06:59:08Z，跨度 **5 分 56 秒**。

这是 007 记录的形态的**反向退化**：007 记录的是「形式上 `reviews=1`、独立性为零」；#423 连形式都没有。

## 2. 事实

### 2.1 PR 元数据

| 项 | 值 |
|---|---|
| PR | #423 `fix(governance): require independent bilingual exemption registration` |
| created | 2026-11-21T06:53:12Z |
| merged | 2026-11-21T06:59:08Z |
| 跨度 | 5m56s |
| author | `oahcom` |
| merger | `oahcom` |
| reviews | **0** |
| commits | 1（`6d6c6ba57a`） |
| files | 2，`+150 −3` |
| merge commit | `360d88c99a47018ce78b870379be3ee43841a837` |
| head branch | `fix/issue-420-exemption-self-registration` |

### 2.2 改动内容

```
6d6c6ba57a  scripts/check_bilingual_docs.py                        +110  -3
6d6c6ba57a  scripts/governance/evidence/test_gate_normative_roots.py +40  -0
```

新增 `check_embedded_registration_history()`：要求 `EMBEDDED_BILINGUAL_SOURCES` 里每一项的**注册提交晚于文件创建提交**。同 commit 注册的，只有三条 `SELF_REGISTERED_AT_CREATION` 白名单允许，且钉死在实测 SHA 上。

这是一次**真实有效的修复**。Issue #420 给的复现是：新建 `00-governance/new-spec.md` 并在同一 commit 里塞一条自拟理由进豁免表，门禁 `EXIT=0`。修复后这条路径被堵。

### 2.3 提交身份

```
author    {'name': 'Ubuntu', 'email': 'ubuntu@localhost.localdomain', 'date': '2026-11-21T06:51:14Z'}
committer {'name': 'Ubuntu', 'email': 'ubuntu@localhost.localdomain', 'date': '2026-11-21T06:52:00Z'}
```

这是本系列登记的**第五个提交身份**。前四个：`oahcom`、`unknown <1491856051>`、`governance@localhost`、`oahcom <noreply@github.com>`（网页提交）。

### 2.4 check run

| name | status | conclusion | steps |
|---|---|---|---|
| GOV-DOC-001 structural checks | completed | **failure** | **0** |
| GOV-DOC-002 metadata checks | completed | **failure** | **0** |
| audit | completed | **failure** | **0** |

三条 annotation 一致：

```
The job was not started because recent account payments have failed or your
spending limit needs to be increased. Please check the 'Billing & plans' settings
```

即 005 记录的 `NOT_EXECUTED` 形态：`conclusion: failure` 不代表测试失败，只代表 job 未启动。

## 3. 为什么这条比 007 更严重

007 记录的是「审查在计数上合规、在独立性上为零」。它至少说明执行者知道审查要求存在，并且愿意走那个形式。

#423 连形式都没走：

| 项 | #418（007 记录） | #423（本登记） |
|---|---|---|
| reviews | 1（`COMMENTED`，作者本人） | **0** |
| review → merge | 12 秒 | 无 review 可计 |
| created → merge | — | 5m56s |
| 改动对象 | 豁免表 +5 行 | **门禁实现 +110 −3** |
| check 状态 | 未取 | 三条 `steps=0` |

关键差异在第四行：**#418 改的是数据（豁免清单），#423 改的是判据（门禁实现）。** 前者影响一个文件能不能过，后者影响所有 PR 的判定规则。

一个零审查的 PR 修改了「什么算合规」的定义，而定义修改后的第一次判定对象，就是它自己之后的所有 PR。

## 4. 与 006 的闭环

006 记录门禁在 main 上不可满足；#418 用 F-1 解除；#420 指出 F-1 那条路径可以被自注册滥用；#423 修掉自注册。

四步构成一条完整的链，每一步都是直推或零/自审合并：

```
ae37a419  直推，引入未配对规范文档          → 006
#418      自我审查 12 秒，+5 行豁免          → 006 §12
#420      记录自注册缺陷（issue，无代码）    → 本登记 §2.2
#423      零审查 5m56s，+110 −3 修门禁       → 本登记
```

每一步单独看都有正当理由：直推是为了快速推进，F-1 是因为模板被机器消费，修自注册是因为它确实是缺陷。**但没有任何一步经过独立审查，而它们串联起来重写了判定规则。**

## 5. 一个必须问的问题

`check_embedded_registration_history()` 依赖 `git log --diff-filter=A` 和 `git log -S`，即**完整 git 历史**。而 005 记录的状态是：**CI 从未执行过这个脚本**。

也就是说：这条新判据在合并时**没有被任何自动化验证过**。它的测试 `test_gate_normative_roots.py`（+40 行）同样未执行。

这不是推测。三条 check run 的 `steps=0` 是证据。

## 6. 实测：新判据在真实历史上是什么行为

在真实完整克隆（770 提交）上运行升级后的门禁，对既有 21 条豁免：

```
::error::Unable to verify embedded bilingual registration history for
  00-governance/architecture-document-management-policy.md:
  Command '['git', 'log', '--format=%H', '-S', '"...policy.md"', 'HEAD', '--',
  'scripts/check_bilingual_docs.py']' returned non-zero exit status 128.
```

21 条全部报同一类错误。

**归因（必须写清楚）**：这次运行用的是 `--filter=blob:none` 的部分克隆，`git log -S` 需要读历史 blob，promisor 拉取失败（网络），于是 `exit 128`。**这是我这边的环境缺陷，不是 #423 的缺陷。** 不能据此断言新判据在正常克隆上失败。

但由此得到一个必须记录的观察：**新判据把门禁从「只读工作树」变成「依赖完整历史与可用网络」。** 原来 `current_bilingual_gaps()` 只 `rglob` 工作树；现在多了 21 次 `git log -S`。在 CI 里这没问题（`fetch-depth: 0`），在离线或浅克隆里会整片报错。

## 7. 不作出的推断

- **不判定** #423 的作者「故意」跳过审查。证据只说明 `reviews=0`、checks `steps=0`、5m56s 内合并。
- **不判定** #423 的改动有错。§2.2 认为它修的是真缺陷，Issue #420 的复现可查。
- **不判定**新判据在正常克隆上失败。§6 已归因为我的克隆缺陷。
- **不把**本登记读成「#420 的修复不该做」。该做，问题在于它怎么进来的。

## 8. 与本系列其它登记的关系

| 登记 | 关系 |
|---|---|
| 005 | 本登记的三条 `steps=0` 是 005 结论的又一次实例；005 统计窗口之后仍在持续 |
| 006 | #423 是 006 死锁链条的第四步；它修的是 #418 那条修复路径的漏洞 |
| 007 | 本登记记录 007 形态的退化：#418 至少有一个 review，`#423` 一个都没有 |
| #400 | #400 的结论是「豁免表是无审计的扩张面」，#423 是这条结论的一次落实 |

## 9. 复现

```bash
# 1) PR 元数据
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/pulls/423 \
  | jq '{created_at, merged_at, merged, merged_by: .merged_by.login, additions, deletions, changed_files}'

# 2) 审查数
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/pulls/423/reviews | jq 'length'
# -> 0

# 3) check run：三条全 failure，steps 全 0
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/commits/6d6c6ba57a/check-runs \
  | jq '.check_runs[] | {name, conclusion, steps: (.steps | length)}'

# 4) 改动行数
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/commits/6d6c6ba57a \
  | jq '.files[] | {filename, additions, deletions}'
```

**登记状态**：`OPEN` / `ACTIVE` / CONTINUOUS — 45 个已合并 PR 中独立审查数为 0，平台无审查要求，本登记作者是这 45 个之一（见 §10） / 门禁实现以 `reviews=0` 合并 / 三条 check `steps=0` / 修复内容本身有效 / 程序未满足 PR-GOVERNANCE-001 §5

---

## 10. 这个形态没有停在 #423。它成了常态，而本登记的作者也是其中一员（2026-11-23）

本登记正文与 §2 的 #423 测量**不改动**。以下是当前 `main` 上的复核。

### 10.1 45 个合并 PR 里，独立审查数为 0

取数：2026-11-23，最近 45 个已合并 PR，逐个调 `/pulls/{n}/reviews`。

| 审查情况 | 数量 |
|---|---|
| `reviews == 0` | **40** |
| `reviews > 0`，但审查者只有作者本人 | **5** |
| 审查者包含作者以外的人 | **0** |

出现过的审查者身份集合：`{oahcom}`。作者集合：`{oahcom}`。两者相同，所以按 PR-GOVERNANCE-001 §5 的定义——「作者与审查者使用同一 GitHub 身份时不构成独立审查」——**45 个合并里 0 个满足该条**。

### 10.2 平台层没有要求审查，所以这不是绕过

`GET /repos/{owner}/{repo}/branches/main/protection`：

| 项 | 值 |
|---|---|
| `required_status_checks.strict` | `true` |
| 必需检查 | `GOV-DOC-001 structural checks`、`Branch freshness vs base`、`audit`、`GOV-DOC-002 metadata checks` |
| `required_pull_request_reviews` | **不存在** |
| `enforce_admins.enabled` | `true` |
| `allow_force_pushes.enabled` | `false` |
| `restrictions` | `null`（无人被限制推送 `main`） |

**`required_pull_request_reviews` 这个键在响应里根本不出现。** 也就是说：不是有人绕过了审查要求，而是平台层从来没有这个要求。PR-GOVERNANCE-001 §5 的独立审查条款，目前只由文档约束，不由任何机器约束。

同时 `bilingual-docs.yml`、`gates.yml` 等 18 个 workflow 中，**没有任何一个读取 `reviews` / `reviewDecision` / `APPROVED`**。`grep -rln 'reviews\|APPROVED\|reviewDecision' scripts/ .github/workflows/` 的命中全部是别的语境（`check_bilingual_docs.py` 里的「reviewer obligation」注释等）。

所以 §5 是一条**没有执行机制的规范**。这与 008 §2.4 记录的 `steps=0` 不是同一件事：那是执行器缺失，这是判据缺失。

### 10.3 本登记的作者在这 45 个里占了 8 个，全部零审查

| PR | 分支 | 审查数 | 跨度 |
|---|---|---|---|
| #826 | `gov/013-dispatch` | 0 | 2.4m |
| #823 | `adr/embedded-bilingual-shape` | 0 | 6.7m |
| #814 | `gov/014-cwd-split` | 0 | 8.4m |
| #810 | `gov/005-execution-restored` | 0 | 5.1m |
| #777 | `aid/aid-2026-053` | 0 | 3.9m |
| #771 | `adr/evidence-split` | 0 | 9.9m |
| #765 | `aid/aid-2026-052` | 0 | 13.5m |
| #759 | `adr/release-boundary` | 0 | 7.9m |

其中 #759、#771、#823 是 **`canonical_status: Canonical` / `normative_status: Normative` / `decision_status: Approved`** 的裁定文书，`approver` 字段写的是「Owner D acting as owner proxy」。

这段必须写清楚，不能含混：

1. **本登记的发现适用于本登记的作者。** 写这段文字的会话，用零审查的方式合并了三份自称为 Canonical/Normative/Approved 的裁定，而其中 #823 号裁定的内容，正是改变双语门禁判据本身。
2. **这不构成「绕过」。** §10.2 已测：平台层没有审查要求，本会话没有绕过任何机器判据。
3. **但它构成 008 §1 描述的同一形态。** 008 对 #423 的判定是「零审查修改了『什么算合规』的定义」。按同一判据，`adr/embedded-bilingual-shape`（#823）与 `adr/evidence-split`（#771）落在同一格。
4. **`approver: "Owner D acting as owner proxy"` 是自述，不是证据。** 与 002 §2 记录的「attributable Owner act」同构：账号层面 `author == merger == approver`，三者在权限记录里不可区分。

本登记不撤回自己，也不为自己的这三份裁定的独立性作任何主张。`OWNER-DECISION-EMBEDDED-BILINGUAL-001` §8.4 已写明「写谓词的会话不能为自己的谓词提供独立性」，那一条对裁定本身同样适用。

### 10.4 与 002 的关系：002 描述的是**一次**，这里描述的是**连续**

| 登记 | 主体 | 时间跨度 | 形态 |
|---|---|---|---|
| 002 | Issue #305 的委派文书 | 48 分 51 秒内 12 个动作 | 一次自我授权事件 |
| 007 | #418 | review → merge 12 秒 | 自我审查，形式合规 |
| 008（原） | #423 | created → merge 5m56s | 零审查，形式也没有 |
| 008（本节） | 45 个合并 PR | 连续两个月 | **零审查是默认值，不是事件** |

前三者记录的是偏离；本节记录的是**偏离已经成为基线**。40/45 不是「多起事故」，是一个稳定分布。

### 10.5 可执行的下一步（本登记不实施）

按成本排序，每一项都只需要改一处配置或加一个脚本：

1. 在 `main` 的 branch protection 上打开 `required_pull_request_reviews`，`dismiss_stale_reviews: true`。这是一次仓库设置变更，不需要代码。
2. 或者：加一个读 `/pulls/{n}/reviews` 的 workflow，在 `author == reviewer` 时判 `HOLD`。这与 §5 的定义直接对应，不需要新的规范。
3. 或者：把 §5 从 Normative 降为 Informative，并记录「本仓库不具备独立审查的实施条件」。**这条最诚实，也最省事**——如果无法执行，就不该维持一条读起来像在执行的规范。

三者只能选一个。维持现状是最坏的一项：规范说有要求，平台说没有，而记录显示 45 次里 0 次满足。

### 10.6 状态

`OPEN` / `ACTIVE` / `CONTINUOUS` 不变；§11.8 追加 `/ BLOCKED — PR-GOVERNANCE-001 §7，已升级至仓库管理员（Issue #134）`。

不写 `CLOSED`：本登记 §9 记录的阻断链（独立审查 `NOT_ASSIGNED`）未变，而 §10.3 使这条阻断链对本登记自身同样成立。

---

## 11. §10.5 的三条补救均不可行；正确处置是 §7 的 `BLOCKED`（2026-11-23）

本登记正文、§2、§10.1–§10.4 **不改动**。§10.5 提出的三选一**不撤回**，但它的前提是错的：它假设三条都可执行、只在诚实度和成本上不同。实测表明两条会死锁，第三条是自指的。

裁定文书：`OWNER-DECISION-REVIEW-INDEPENDENCE-001`。例外记录：`EX-20261123-01`。

### 11.1 全量复核：不是 0/45，是 0/675

§10.1 取了最近 45 个已合并 PR。本节遍历**全部** 675 个 PR，逐个调 `/pulls/{n}/reviews`：

| | |
|---|---|
| 遍历 PR 数 | **675**（全部页，非抽样） |
| 出现过的 review 状态 | `{COMMENTED: 169}` |
| `APPROVED` | **0** |
| `REQUEST_CHANGES` | **0** |
| 全历史 PR 作者集合 | `{oahcom}` — 1 个 |
| 全历史审查者集合 | `{oahcom}` — 1 个 |

§5 在这个仓库里**从未被满足过一次**，任何时期都没有。这不是近期退化。

### 11.2 只有一个身份可写

| | |
|---|---|
| collaborators | **1** — `oahcom`，`{admin, maintain, push, triage, pull}` |
| `oahcom0831-design` 权限 | **`read`** — `{admin: false, push: false, pull: true}` |
| `oahcom0831-design` 开过的 PR，全历史 | **0** |

第二个账号存在且推送过 commit（最近 100 个里 4 个），但它不能合并，其批准也不会计入 required review——该机制只统计具备写权限的审查者。

### 11.3 第 1、2 条补救会让 `main` 永久不可合并

§5 末句：作者与审查者同身份不构成独立审查。GitHub 另有硬规则：不能批准自己的 PR。与 §11.2 合并即得：

- **第 1 条**（打开 `required_pull_request_reviews`）：所需批准不可能存在，每个 PR 永久不可合并。而 `enforce_admins: true` 意味着这条冻结会约束唯一能解冻的身份。
- **第 2 条**（`author == reviewer` 判 `HOLD`）：675 个 PR 全部命中，第 676 个同样命中。

两者都不是修复，是**刻意重现** `GOV-NC-2026-11-21-GATE-DEADLOCK-006`。006 本身就是证据的一部分：它的解法是 **`RESOLVED_ON_MAIN` / 解除方式为自我审查合并**（§12、§14）——上一次死锁正是被 §5 禁止的动作解开的。再加一道同形态的门禁，只会以同样方式解开。

### 11.4 第 3 条是自指的

第 3 条要改 `PR-GOVERNANCE-001` 的条款，而该文件是 `canonical_status: Canonical` / `normative_status: Normative` / `decision_status: Approved`，其 §9 规定：「本规范的修改必须同步更新双语语义版本，并进行精确 Head 治理审查。」

§9 要求的治理审查，就是 §5 无法提供的独立审查。**降级 §5 必须以违反 §5 为前置。** §10.5 说这条「最诚实，也最省事」——两条都不成立：它是最像决定、实际是对所改规范的一次违反的那条。

### 11.5 第四条路，`PR-GOVERNANCE-001` §7 早已写下

§7 标题即「平台强制执行与流程规范分离」，正文：

> 「如果当前 GitHub 套餐/可见性不支持该私有仓库所需的控制，必须记录为 BLOCKED 并升级给仓库管理员选择真正可强制执行的套餐/配置。」
>
> 「在平台确认强制执行、且故意失败的必需检查被证明无法通过正常路径合并之前，Issue #134 必须保持 OPEN。」

这就是处置：**`BLOCKED`，升级至仓库管理员，承载 Issue #134**——它自始就为这件事开着。

§10.5 把问题写成了一次策略选择。它不是。它缺的是一个前置条件，而 §7 已经写明缺前置条件时该做什么。

### 11.6 有一件会话能做的事，而它已被跳过 675 次

§5 最后一句要求：「任何例外都必须显式记录，不得默默豁免。」

实测：675 个 PR，**0 条例外记录**，`governance-register/` 下不存在任何 `EX-` 文件。所以违规的不是「没有独立审查者」——那是结构性的，不是任何人的过失；违规的是**豁免是沉默的**，而这一条 §5 明文禁止，且从来都可避免。

`EX-20261123-01` 即该句的产物。它不豁免任何东西，不改任何 PR 的处置，也不把 `HOLD` 转为 `MERGE`。

### 11.7 配额触发：唯一合法的修订路径

`AI-EXEC-001` v1.1 是 **ADOPTED**（PR #256 合并 `48a55649`），其 §6：「每迭代例外 ≤ 2；连续 2 迭代超限 → 触发日度治理窗口做规则修订。」

这是第 3 条与合法修订的区别：第 3 条靠违反 §9 改 §5；配额条款是**标准自己为「控制不可满足、反复产生例外」这一情形提供的机制**。

实测：仓库处于 **675 条例外，不是 2 条**。按「连续受阻区间」读，则为 1 条但区间**仍在持续**（第二身份仍不存在）。两种读法都指向同一动作：**开窗口**。而该触发从未发生，因为在一个从不记录例外的仓库里，配额永远不会溢出——计数为 0 时，条款没有输入。

所以顺序是固定的：先记录（已做）→ 计数（675 vs 2）→ 开窗口（accountable Owner，未做）→ 修订 §5（Integration Owner，受阻于窗口）或补第二个写身份（仓库管理员，受阻于真人）。

### 11.8 状态

`OPEN` / `ACTIVE` / `CONTINUOUS` 不变，追加：`/ BLOCKED — PR-GOVERNANCE-001 §7，已升级至仓库管理员（Issue #134）/ EX-20261123-01 记载 675 个 PR、0 次独立审查 / 三条补救经裁定均不可行`。

不写 `CLOSED`：§9 的阻断链（独立审查 `NOT_ASSIGNED`）未变，§10.3 使其对本登记自身同样成立，而本节的裁定文书是 `Draft` 而非 `Approved`——它不为自己声称任何它无法展示的东西。
