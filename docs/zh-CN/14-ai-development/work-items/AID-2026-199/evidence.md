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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-199/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "本节每个改前/改后数字，都是在本工作树中运行所列命令得出的；改前文件取自 origin/main 的 2f4f4118bd2c2d8e43a23975f667deeb06553f3c。本文不声称任何 CI 结果、合并 SHA 或平台上下文。"
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
    canonical_scope: "AID-2026-199：让三个门禁助手在其输入缺失、仅以注释出现或使用 .yaml 后缀时 fail-closed"
    canonical_scope_id: "ai-development/aid-2026-199-gates-fail-closed-on-unreadable-inputs"
    canonical_scope_keywords:
      - "fail-closed"
      - "index-membership"
      - "declared-check-contexts"
      - "test-reachability"
      - "comment-stripping"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-199/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-199/evidence.md"
    zh-CN: null
---

# AID-2026-199 — 三个门禁在回答一个它读不到的问题

**状态：DRAFT — 仅助手与测试改动。** 没有新增、改名或删除任何 required context、job id、job 显示名、索引行或 baseline 条目。每个门禁原有的判定一律保留，改动只在它的输入缺失、以 `.yaml` 结尾、或只出现在注释里时发生什么。

## 1. 本记录为何存在

本仓库的三个检查是关系式，而不是单文件检查：

| 检查 | 关系 | 两侧 |
|---|---|---|
| `check_index_membership` | 目录 ↔ 索引行 | `14-ai-development/work-items/*/` 与 `INDEX.md` |
| `check_declared_check_contexts` | 声明 ↔ 产出 | `PR-GOVERNANCE-001.md` 里的围栏块与 `.github/workflows/` 里的 job |
| `check_test_reachability` | 测试文件 ↔ workflow | 树中的 `test_*.py` 与 workflow 实际执行的东西 |

三者都曾在关系的一侧为空时给出绿色。一侧为空不是关系被满足，而是关系未被绑定。以下三例均为实测，不是推断——改前文件取自 `origin/main` = `2f4f4118bd2c2d8e43a23975f667deeb06553f3c` 的版本。

## 2. 缺陷一 — 索引成员检查在空集合上通过

`check_index_membership` 有两处提前返回：

```python
directories = work_item_directories(head_paths)
if not directories:
    return []                      # 目录侧为空 -> 无违规
if WORK_ITEMS_INDEX not in head_paths:
    return []                      # 索引侧为空 -> 无违规
```

`main()` 把 `[]` 读作"无可报告"，随后打印通过行。用改前文件、在一棵只有 `README.md` 的树上实测：

| 输入 | 改前 | 改后 |
|---|---|---|
| 完全没有 work-item 目录（`work-items/` 被改名后就是这个形状） | 返回 `[]`；检查器打印 `Repository hygiene check passed` 并 exit 0 | `RuntimeError` → `::error::repository hygiene cannot be determined: no work-item directories under '14-ai-development/work-items' ...` → exit 2 |
| 目录存在，但 head 树里没有 `INDEX.md` | 返回 `[]`；exit 0 | `RuntimeError` → `::error::... the work-item index '14-ai-development/work-items/INDEX.md' is absent from the tree ...` → exit 2 |

`RuntimeError` 是本文件既有的"无法判定"通道，`main()` 早已把它转成 exit 2——即本文件其它检查在输入缺失时给出的同一个答案。没有引入新退出码，也没有新增消息通道。`CHECK_VERSION` 升到 `2026-11-27.2`，因为引用版本号的人引用的是规则集，而规则集变了。`2026-11-27.1` 是 main 上另一处改动（无参数运行现在 exit 2，头树那一半必须用 `--head-tree-only` 请求）；两者分开正是本次另取一个号、而不是复用它。

## 3. 缺陷二 — 一段注释吃掉了一个 workflow

两个 workflow 读取器各有一处盲点。

### 3.1 `jobs:  # comment`

`produced_contexts` 只认 `rstrip()` 后等于 `jobs:` 的行，否则就等第 0 列出现键来结束映射。`jobs:  # comment` 两者都不是，于是读取器从未进入 jobs 映射，该文件产出零个 context。声明与产出的对比是子集比较，空产出集合无法让它失败——每个声明名都被其它文件"满足"了。

在一个三 job 夹具（`fmt`、它的显示名、`audit`）上，把注释放到头部后实测：

| | 改前 | 改后 |
|---|---|---|
| `produced_contexts(...)` 结果 | 0 个 context | 3 个：`fmt`、`Rust format (hard gate)`、`audit` |

反向也钉住了：只以 `  # audit:` 形式存在的 job 不产出任何 context，因此依赖被注释 job 的声明会失败，报 `declares required check context 'audit', but no job in .github/workflows produces it`。

### 3.2 只认 `.yml`

两个读取器都只 glob `*.yml`。GitHub 同样把 `.yaml` 当作 workflow。用一个只含声明 job 的 `gates.yaml` 实测：

| | 改前 | 改后 |
|---|---|---|
| `.yaml`-only 树上运行 `check_declared_check_contexts.main` | exit 2 — `INCOMPLETE: no workflows under .github/workflows` | exit 0，context 被产出 |
| `check_test_reachability` 面对含 `discover` 根与 gate `run:` 的 `.yaml` workflow | 该文件根本没被读取 | 0 unreachable，gate 已接线 |

## 4. 缺陷三 — 一段注释让测试"可达"

Rule B 拿测试的路径、文件名、stem 或点分模块名去匹配拼接后的 workflow 文本。那份文本是原始文件，所以注释里的名字也算"被执行"，而同一模块的 gate 分支早已剥掉注释——同一个问题两个答案，宽松的那个生效。在一棵只有一份测试文件、workflow 里唯一提到它的地方是 `# TODO` 注释的树上实测：

| | 改前 | 改后 |
|---|---|---|
| `check_test_reachability` | exit 0，"0 unreachable"——该测试被报告为已执行 | exit 1，`pkg/test_x.py` 被列为不可达 |

同一读法往前推了一步：被注释掉的 `# - run: python3 -m unittest discover -s pkg` 曾是一个发现根，覆盖 `pkg` 下全部测试。两个分支现在都读同一份"剥注释视图"，由 gate 分支早已使用的 `strip_comment` 产出。

## 5. 改了什么

| 文件 | 改动 |
|---|---|
| `scripts/ci/check_repository_hygiene.py` | 两处 `return []` 改为 `RuntimeError`；`CHECK_VERSION` → `2026-11-27.2`；docstring 写明 fail-closed 规则，以及为何空的一侧不是被满足的关系 |
| `scripts/check_declared_check_contexts.py` | 新增 `strip_yaml_comment` / `strip_yaml_comments`，在 `produced_contexts` 内部应用；`WORKFLOW_GLOBS = ("*.yml", "*.yaml")` 与 `workflow_files()` |
| `scripts/ci/check_test_reachability.py` | `read_workflows` 使用 `WORKFLOW_GLOBS`；新增 `workflow_text()`（剥注释），供 `discovery_rules` 与 Rule B 文本共用 |
| `scripts/test_check_repository_hygiene.py` | `with_index` 夹具开关、两个 fail-closed 用例，以及让每个夹具都带上关系两侧的 `commit()` 助手 |
| `scripts/test_check_declared_check_contexts.py` | 三个用例：注释头部、注释 job、`.yaml` workflow |
| `scripts/ci/test_check_test_reachability.py` | 三个用例：注释中的测试名、注释中的 `discover`、两个分支各读 `.yaml` |

## 6. 改前改后实测

下列数字均在本工作树产出。第 2-4 节的缺陷实测使用的是 `origin/main` = `2f4f4118` 的改前文件；下表
拿本分支与它实际合并的那份 `origin/main`（`9dc98a52`）对比，因此计数不会过期。

| 指标 | 改前（9dc98a52） | 改后 |
|---|---|---|
| `check_repository_hygiene.py` 版本 | `2026-11-27.1` | `2026-11-27.2` |
| `Work-item index membership ... directories= / linked=` | 110 / 110，exit 0 | 带本工作项为 111 / 111（不含它则是 110 / 110：它恰好增加一个目录与一行），exit 0 |
| `check_declared_check_contexts.py` | 16 declared、16 produced，exit 0 | 16 declared、16 produced，exit 0 |
| `check_test_reachability.py` | 66 个测试文件、66 可达；18 个 gate 脚本、3 未接线、3 已 baseline | 完全相同 |
| `scripts/test_check_repository_hygiene.py` | Ran 101，OK（skipped=1） | Ran 103，OK（skipped=1） |
| `scripts/ci/test_check_test_reachability.py` | Ran 24，OK | Ran 27，OK |
| `scripts/test_check_declared_check_contexts.py` | Ran 13，OK | Ran 16，OK |

`check_declared_check_contexts` 的"声明 vs 产出"一侧是刻意注入声明的：实时分支保护载荷需要 token 与一次网络往返，而本记录不声称任何平台结果。`check_repository_hygiene` 与 `check_test_reachability` 按 CI 的调用方式在本树上运行。

## 7. 新增用例可被推翻

每处修复单独回退后再跑套件，失败的恰好是新用例：

| 回退 | 失败的新用例 | 其余 |
|---|---|---|
| `produced_contexts` 里的 `strip_yaml_comments` | `test_jobs_header_with_a_trailing_comment_still_produces_contexts`、`test_yaml_workflow_suffix_is_read` | 全绿 |
| 两个读取器里 `*.yaml` 那一半 glob | `test_yaml_workflow_suffix_is_read_for_both_branches`、`test_yaml_workflow_suffix_is_read` | 全绿 |
| Rule B 文本的剥注释 | `test_test_named_only_in_a_comment_is_unreachable` | 全绿 |

两个 fail-closed 用例断言 exit 2 与具体消息，改前的 `[]` 按构造只会 exit 0，因此无法满足它们。

## 8. 夹具改动不是放宽用例

`scripts/test_check_repository_hygiene.py` 的共享 `commit()` 助手只写该用例的文件加一份空 schema registry。那些夹具既没有 work-item 目录也没有 `INDEX.md`，于是成员检查现在会对它们 fail-closed——这是正确的，但与该用例想测的东西无关。因此助手改为写一个 work-item 目录，并为夹具中每个目录写一行 `INDEX.md`，除非用例自带这些内容或传入 `with_index=False`。

两个方向都验证过：不改助手时（合并前 97 个用例的那套夹具）97 个用例里有 65 个失败；而两个*关于*缺失侧的用例使用 `with_index=False` 并断言 exit 2。

## 9. 本记录不声称什么

- 不声称任何 SHA 上的 CI context 结果。
- 不声称合并 SHA，也不声称分支保护状态。
- 未改动 16 个声明上下文、16 个产出上下文或任何 job 名。
- 未新增任何 gate-wiring baseline 条目：三个已 baseline 的未接线 gate 保持原状。
- 未对本次未点名的任何检查作任何声称。

## 10. 身份

本工作项最初分配到 AID-2026-192。PR 挂起期间 main 从 2f4f4118 前进到 9dc98a52，而那份 main 自带
AID-2026-192，以及 197 与 198。于是本分支变 dirty，在每条 AID-2026-192 路径上出现 add/add 冲突，
GitHub 没有为它创建任何 check run。按分配规则，本工作项在一个提交内改号为 AID-2026-199——即 main
树、开放 PR 与远端分支名之外的下一个号码——三棵目录树与所有引用一并迁移。此前写下的提交信息与 PR
正文仍写作 AID-2026-192；本树内所有路径写作 AID-2026-199，prompt 摘要因快照自身带路径而重新计算。
