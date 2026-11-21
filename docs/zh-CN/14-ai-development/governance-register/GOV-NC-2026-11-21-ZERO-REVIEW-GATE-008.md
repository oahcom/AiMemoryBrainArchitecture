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

**登记状态**：`OPEN` / `ACTIVE` / 门禁实现以 `reviews=0` 合并 / 三条 check `steps=0` / 修复内容本身有效 / 程序未满足 PR-GOVERNANCE-001 §5
