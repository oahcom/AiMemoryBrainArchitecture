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
        - "14-ai-development/work-items/AID-2026-188/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "以下每个数字都由本工作树在基线 1e9341da603dec78377fed240f4d6dbabaa8838e 上运行已提交文件产生：根集合与缺口集合由导入门禁模块读出，两份基线由 read_baseline_entries() 读出，登记表由读取其声明键得出，两个测试套件由实际运行得出。本文不声称任何未在本地产生的门禁结果、CI 结果或合并结果。"
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
    canonical_scope: "AID-2026-188 核验：03-memory-brain 规范根及其三份 canonical 文档早已登记，不再欠任何登记变更"
    canonical_scope_id: "ai-development/aid-2026-188-memory-brain-root-registration-verification"
    canonical_scope_keywords:
      - "bilingual"
      - "normative-root"
      - "memory-brain"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-188/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-188/evidence.md"
    zh-CN: null
---

# AID-2026-188 — `03-memory-brain` 规范根早已登记：这是一份核验记录，不是一次修复

**状态：DRAFT —— 仅记录。** 本工作项不修改任何一行检查器、不修改任何一条基线条目、不修改登记表取值、不修改任何镜像。它存在的原因是：被派发来执行的那次登记早已落地，而一个未被纠正的派发前提会持续生产同一个 no-op 任务。

## 1. 这份记录为什么存在

有一份修复契约被派发，要求把 `"03-memory-brain"` 加入 `scripts/check_bilingual_docs.py` 的 `NORMATIVE_ROOTS`，其前提是：该集合现有 13 项且不含该根。下面的实测与该前提相矛盾：该根是集合的第四项，集合之所以是 13 项正是因为包含它，再"加入"一次是空操作而不是修复。

这是同一单元的第三次派发。前两次因上游原因失败，与前提无关；但尝试次数本身并不构成关于前提的证据，它只意味着：如果描述不在记录上被纠正，第四次派发会照着同一段文字再来一遍。第 2 节按实测陈述分歧，第 3 节给出可复现的测量，第 6 节列出有意未做的修改。

本文不主张先前那次登记正确、完整或充分。它只主张：在所声明的基线上，被要求的改动已经存在，因此该改动无法表达该要求；而任何假装做出该改动的后续编辑都会构成虚假陈述。

## 2. 派发前提与实测状态

| # | 派发前提 | 在 `1e9341da` 上的实测 | 判定 |
|---|---|---|---|
| P1 | `NORMATIVE_ROOTS` 共 13 项且不含 `03-memory-brain`。 | 共 13 项且包含 `03-memory-brain`，它是第四项（`check_bilingual_docs.py:20`）。去掉该根后字面量只剩 12 项。 | **被推翻。** 项目数与成员资格不可能同时如描述那样成立。 |
| P2 | `03-memory-brain/` 有 3 份 canonical，`docs/en`、`docs/zh-CN` 各有 13 个镜像，且这 3 份都在。 | `03-memory-brain/` 3 个文件；`docs/en/03-memory-brain/` 13 个；`docs/zh-CN/03-memory-brain/` 13 个；3 个 canonical 名称在两侧均存在。 | **成立。** |
| P3 | 进程内加入该根后 `current_bilingual_gaps()` 由 77 变 77，`new=0`、`gone=0`。 | 已复现，且这正是"向集合插入一个它已包含的元素"的特征：`set | {"03-memory-brain"} == set`。该观测与"该根早已存在"一致，而不能证明"登记尚未完成"。 | **已复现，但需重新解释。** 空操作本身证明元素早已在集合中。 |
| P4 | `check_bilingual_docs_full.py` 中可能存在第二份根清单，需同步修改。 | 不存在第二份字面量。该文件导入 `NORMATIVE_ROOTS` 并*从目录树推导*集合，两者不一致即以退出码 2 失败。 | **单一定义。** |

P1 与 P3 正是本工作项成为核验记录的原因。一个已含某元素的字面量无法通过"加入该元素"来修复：`NORMATIVE_ROOTS = {...}` 是 `set` 字面量，编辑会被静默吸收并产生零字节 diff——而任何只比较退出码的检查都会把它报成"已应用"。

## 3. 测量

以下命令均在本工作树内以 `PYTHONUTF8=1` 执行（见第 8 节）。基线为 `origin/main` = `1e9341da603dec78377fed240f4d6dbabaa8838e`。

### 3.1 根集合

`scripts/check_bilingual_docs.py:19-24`：

```
19 : NORMATIVE_ROOTS = {
20 :     "00-governance", "01-system-architecture", "02-domain-model", "03-memory-brain",
21 :     "04-memory-compiler", "05-memory-runtime", "06-memory-context", "07-agent-integration",
22 :     "08-bmcp-protocol", "09-security-governance", "10-storage-consistency", "13-engineering-decisions",
23 :     "14-ai-development",
24 : }
```

该区间的 `git blame` 把第 19-20 行归属到 `6ab36b3697a0994d8de449d2b9c344f23aac0fda`（2026-11-26 22:02:51 +0800，`docs(memory-brain): restore three D normative roots (AID-2026-150)`）。字面量最初来自 `32a35f422ba6442d1f700cfb327f348c0740a7f2`；在该基线上把 `03-memory-brain` 纳入受强制范围的，是上述恢复提交。

导入模块并读取该常量：

```
NORMATIVE_ROOTS count = 13
roots = ['00-governance', '01-system-architecture', '02-domain-model', '03-memory-brain',
         '04-memory-compiler', '05-memory-runtime', '06-memory-context', '07-agent-integration',
         '08-bmcp-protocol', '09-security-governance', '10-storage-consistency',
         '13-engineering-decisions', '14-ai-development']
03 in roots: True
```

### 3.2 缺口、两份基线与副本一致性

```
gaps 77 baseline 77 new 0 gone 0
ci baseline entries 77
copies agree []
memory-brain gaps: []
```

- `current_bilingual_gaps()` = 77；`read_baseline()`（读 `scripts/bilingual-baseline.txt`）= 77；`read_baseline_entries(CI_BASELINE_PATH)`（读 `scripts/ci/baselines/bilingual-docs.txt`）= 77。
- `new = gaps - baseline = 0`，`gone = baseline - gaps = 0`：本次登记不改变门禁判定。
- `check_baseline_copies_agree()` 返回 `[]`，即 AID-2026-172 的比较看到两份冻结副本一致。
- 缺口集合中不存在 `03-memory-brain/` 下的任何路径，即三份 canonical 文档均已配对。

### 3.3 另一份根清单是推导出来的，不是复制出来的

`scripts/check_bilingual_docs_full.py`：

- `:24-28` 从权威模块导入 `EMBEDDED_BILINGUAL_SOURCES`、`NORMATIVE_ROOTS`、`PAIR_EXEMPT_PREFIXES`。
- `:35-39` 按 `NN-name` 形状从 `ROOT.iterdir()` 推导 `_DERIVED_ROOTS`。
- `:40-45` 在 `_DERIVED_ROOTS != NORMATIVE_ROOTS` 时以退出码 2 退出，并同时打印两个集合。

因此仓库的 Python 源码中只有一份根字面量，全树清单由一道等值断言绑定到它。**仅一处定义**；没有第二份清单被更新，因为没有第二份清单可更新。该文件 `:15-23` 的注释记录了这一缘由：此文件此前的确持有自己的副本，其中点名了七个并不存在的目录（`:19` 处的 `03-memory-brain` 即是其一），并就同一批字节与权威给出了不一致的结论。

### 3.4 全树双语清单

```
GOV-DOC-001 full scan: 906 in-scope Markdown files; 371 exempt; 77 violations.
```

该工具是严格的全仓库清单，不是增量必需门禁；它没有自己的基线，因此把每一条基线条目都报成违例。其计数等于冻结清单数，所以它与 3.2 节一致而非矛盾。在改动后的 head 上重跑，它仍报同样的 77 条：本工作项新增的 Markdown 位于 `14-ai-development/work-items/`，属于 `PAIR_EXEMPT_PREFIXES` 子树，不附加配对义务。

### 3.5 三份文档早已是受治理文档

`00-governance/document-scope-registry.yaml:46-59` 声明了十三个 `governed:` 根，`03-memory-brain` 位于第 50 行：

```
46 : governed:
47 :   - 00-governance
48 :   - 01-system-architecture
49 :   - 02-domain-model
50 :   - 03-memory-brain
...
59 :   - 14-ai-development
```

`scripts/check_document_management.py` 对该根内文件分类如下：

```
03-memory-brain: 3/3 classified
GOV-DOC-002: 934 governed documents, 488 classified, 446 unclassified
```

`3/3` 正是对派发中登记表那一半的直接回答：三份 canonical 文档位于受治理根内、被扫描、且携带可解析的元数据。那 446 份未分类文档是既存的全树状态，该门禁对每个根都会报告它们，与本改动无关。

还有一处结构性要点，正是派发中的 `documents:` 编辑并不被欠下的原因。登记表只有四个顶层键——`governed:`、`governed_files:`、`backlog:`、`excluded:`——**根本没有 `documents:` 键**。逐文件登记只以 `governed_files:`（`:70`）形式存在，其唯一一条是 `docs/governance/documentation-gaps.md`：一个*所在目录不受治理*的文件。把 `03-memory-brain/*.md` 列在那里，等于声称它们所在目录不受治理，而这与第 50 行的事实相反。该门禁强制的会计恒等式是"声明范围对磁盘"，而不是"受治理根内的逐文件名册"；因此追加三条路径只会让例外清单说假话，并且不改变任何判定结果。

## 4. 测试结果

覆盖该脚本的两个套件都跑了，因为派发只点名了其中一个目录，而 AID-2026-172 的用例在另一个里。

```
$ python -m unittest discover -s scripts -p "test_check_bilingual*"
Ran 15 tests in 8.353s
OK

$ python -m unittest discover -s tests -p "test_check_bilingual*"
Ran 7 tests in 0.000s
OK
```

那 15 个是 AID-2026-172 新增的：`BaselineCopyConsistencyTests`（5 个：两份副本一致通过、仅冻结副本含该条目、仅棘轮副本含该条目、棘轮副本缺失时失败关闭、注释与空行不算条目）、`ChangedPathTests`（7 个，含 `test_added_entry_refuses_and_leaves_file_untouched`、`test_missing_current_baseline_refuses`、`test_shrinking_set_is_written`）以及 `test_same_head_is_not_applicable_not_pass`。全部在未改动脚本的情况下通过。`tests/` 下的 7 个是全树清单自身的用例，也通过。

`test_pair_checked_normative_doc_still_needs_manifest` 是"若改了规范根而未附声明就会变红"的那个用例；本改动未触发它，因为没有做这类改动。

## 5. 读者应当与不应当得出的结论

应当得出：派发所述登记在 `1e9341da` 已存在且被强制；缺口数仍为 77，新增 0、消解 0；两份冻结基线仍然一致；三份 canonical 文档已配对并携带元数据；派发前提有误，且照同一段文字第四次派发会重犯该错误。

不应当得出：该登记*充分*；77 条缺口可接受；相关文件中点名的另外九份 canonical 已被恢复；或任何 Owner 接受已经发生。`#1212` 仍为 OPEN。本文 `normative_status` 为 `Informative`：这是测量记录，不是裁决。

## 6. 有意未做的动作

| 未做 | 理由 |
|---|---|
| 编辑 `NORMATIVE_ROOTS` | 元素已存在；集合字面量无法容纳两次，该编辑会产生空 diff 却看似满足契约。 |
| 重新生成任一份基线 | 两份都持有同样的 77 条，`new` 与 `gone` 均为 0，且只缩不增的写入器会拒绝任何新增条目。 |
| 给登记表加 `documents:` 名册 | 该键不存在（见 3.5 节）；`governed_files:` 的含义是"位于非受治理目录中的文件"，会歪曲这三份。 |
| 把 `03-memory-brain/*.md` 加入 `governed_files:` | 同上，且会让一份本就应当与其理由同样小的例外清单无故变大。 |
| 任何检查器语义变更 | 派发明确排除，且没有必要：判定结果已经是预期结果。 |
| 恢复其余 canonical 文档 | 明确排除。它们的缺失是另一个仍然开放的决定。 |
| 删除或编辑任何镜像 | 超出范围；镜像正是这三份文档已配对的依据。 |
| 关闭任何 Issue | 超出范围。 |

## 7. 双语对应件

`docs/en/14-ai-development/work-items/AID-2026-188/evidence.md` 携带同一正文，`canonical_status: Non-Canonical` 且 `source` 指向本文件。`docs/zh-CN/14-ai-development/work-items/AID-2026-188/evidence.md`（本文件）携带同一批章节的中文译文。两者都是本文件的镜像，不是独立权威，除完整呈现第 1-8 节外不主张超出该范围的语义对等。

## 8. 环境说明（locale 工件，不是缺陷）

本机需要 `PYTHONUTF8=1`。缺少它时，Python 的 `subprocess` 捕获 `git` 与 `python` 输出会按 GBK 控制台代码页解码 UTF-8 字节，在遇到非 ASCII 路径时抛出 `UnicodeDecodeError`；于是门禁报出一个与仓库树无关的解码失败。上文引用的每条命令都在 `PYTHONUTF8=1` 下执行。这是 Windows 主机 locale 的属性，不是检查器的属性，本文不提出修复。

## 9. 复现

```powershell
cd <worktree>
$env:PYTHONUTF8="1"
python -c "import importlib.util as u; s=u.spec_from_file_location('c','scripts/check_bilingual_docs.py'); m=u.module_from_spec(s); s.loader.exec_module(m); g=m.current_bilingual_gaps(); b=m.read_baseline(); print(len(m.NORMATIVE_ROOTS), '03-memory-brain' in m.NORMATIVE_ROOTS, len(g), len(b), len(g-b), len(b-g), m.check_baseline_copies_agree())"
# -> 13 True 77 77 0 0 []
python scripts/check_bilingual_docs_full.py   # -> 906 in-scope; 371 exempt; 77 violations（全树清单）
python scripts/check_document_management.py   # -> 03-memory-brain: 3/3 classified
python -m unittest discover -s scripts -p "test_check_bilingual*"   # -> Ran 15 tests, OK
python -m unittest discover -s tests -p "test_check_bilingual*"     # -> Ran 7 tests, OK
```

## 10. 限制

- 只为根声明读取了上述两个评分脚本与登记表。若某份工作流、shell 脚本、Rust 文件或 crate 夹具中另有根字面量，则在本记录之外；本次检索范围为 `scripts/**/*.py` 与 `00-governance/*.yaml`。
- `git blame` 在所述基线上的完整克隆中执行；浅克隆会把浅边界提交误报成字面量的来源。
- 本文不主张任何 CI 上下文、合并 SHA 或 blob 摘要。AID-2026-188 为 `DISPATCHED` / `PROVISIONAL`，其载体是本记录所在的 pull request。
- 派发原文逐字保存在 `prompt-v1.md`，包括其中两处前提陈述，因此分歧可被核验而不必依赖转述。
