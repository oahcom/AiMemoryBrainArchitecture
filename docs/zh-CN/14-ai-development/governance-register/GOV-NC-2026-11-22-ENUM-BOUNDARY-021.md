# GOV-NC-2026-11-22-ENUM-BOUNDARY-021 — 双语闸门枚举边界与基线写保护

- 登记编号：GOV-NC-2026-11-22-ENUM-BOUNDARY-021
- 日期：2026-11-22
- 类别：Engineering Governance / CI Gate Integrity
- 状态：OPEN — Awaiting implementation and independent verification
- 影响组件：`scripts/check_bilingual_docs.py`
- 关联登记：GOV-NC-2026-11-22-REPO-ROOT-014
- 实施范围：闸门枚举边界、冻结基线写保护及仓库根目录一致性
- 禁止范围：`crates/`、既有冻结基线条目及既有 PR

## 1. 问题概述

本登记记录双语文档闸门的两个相互独立但会共同影响
CI 可信度的缺陷。

第一，`current_bilingual_gaps()` 使用文件系统递归枚举，
而不是 Git 跟踪文件集。被 `.gitignore` 忽略的缓存文件、
临时文件及未跟踪 Markdown 文件可能被误判为规范文档缺口。

第二，`write_baseline()` 没有在写入之前验证工作树状态。
未跟踪文件产生的幻影路径可能被永久写入冻结基线。
由于基线规则禁止增加条目，这种污染不能通过普通运行自动恢复。

两个缺陷分别影响闸门的枚举正确性和治理状态的可恢复性。

## 2. 缺陷一：枚举边界错误

### 2.1 原实现

原实现：

    for root_name in sorted(NORMATIVE_ROOTS):
        root = REPO_ROOT / root_name
        for path in sorted(root.rglob("*.md")):
            source = path.relative_to(REPO_ROOT).as_posix()

`Path.rglob()` 枚举磁盘文件，不区分：

- Git 已跟踪文件；
- 未跟踪文件；
- 被 `.gitignore` 忽略的文件；
- 测试缓存；
- 临时文件。

因此，闸门实际检查的集合并不等于仓库受版本控制的文档集合。

### 2.2 受控实验原文

在干净 detached 检出中执行：

    $ printf '# probe\n' > 06-memory-context/_probe-untracked.md
    $ BASE_SHA=$HEAD_SHA=origin/main python scripts/check_bilingual_docs.py
    ::error::New bilingual gap outside frozen baseline: 06-memory-context/_probe-untracked.md
    EXIT=2

随后执行：

    $ git ls-files --error-unmatch 06-memory-context/_probe-untracked.md
    error: pathspec ... did not match any file(s) known to git

这证明闸门把不属于 Git 跟踪集的文件误判成了新的双语缺口。

### 2.3 已发生的实际影响

以下两个被忽略的缓存文件：

- `08-bmcp-protocol/.pytest_cache/README.md`
- `08-bmcp-protocol/tests/conformance/.pytest_cache/README.md`

会导致主工作树检查返回 `EXIT=2`。

同一 commit 的干净检出却得到：

    PASS / 77 frozen / 0 new gaps

同一提交出现本地红、干净检出绿的结果，说明闸门受到工作树附加文件污染，无法提供稳定的 CI 判定。

### 2.4 治理裁定

`current_bilingual_gaps()` 必须只从 Git 跟踪集取得 Markdown 路径。

采用 `git ls-files` 作为唯一枚举来源，并以仓库根目录作为命令工作目录。

路径必须使用仓库相对 POSIX 形式，与既有 `source` 标识完全一致。

以下内容不得进入 gap 集合：

- 未跟踪文件；
- ignored 文件；
- pytest 缓存；
- 临时文件；
- 其他不属于 Git 跟踪集的磁盘文件。

Git 不可执行、仓库无法识别、命令失败或输出无法可靠解析时，必须 fail-closed。
不得回退到 `rglob()`，也不得把执行失败解释为零缺口。

已经跟踪的 Markdown 文件仍然必须接受原有完整双语检查。
本次修复不允许降低规范严格性。

## 3. 缺陷二：冻结基线缺少写保护

### 3.1 原实现

原实现：

    def write_baseline() -> int:
        gaps = sorted(current_bilingual_gaps())
        header = (...)
        BASELINE_PATH.write_text(
            header + "\n".join(gaps) + "\n",
            encoding="utf-8",
        )

该函数没有检查工作树是否干净。

### 3.2 风险

冻结基线包含以下治理约束：

    # This baseline may only shrink; entries must never be added.

如果脏工作树中存在未跟踪 Markdown 文件，原来的磁盘枚举可能将它们写入冻结基线。

一旦写入，幻影路径便成为永久冻结条目，普通检查不会自动清除它们。

这会把临时工作树状态转化为长期治理状态。

### 3.3 治理裁定

`write_baseline()` 必须在任何基线写操作之前执行：

    git status --porcelain --untracked-files=all

以下情况必须拒绝写入：

- 工作树存在已跟踪文件修改；
- 存在已跟踪文件删除；
- 存在未跟踪文件；
- Git 状态检查命令执行失败。

拒绝时必须：

1. 返回非零状态；
2. 输出明确的错误信息；
3. 不修改原 baseline 的任何字节；
4. 不留下半写入文件。

正常写入采用同目录临时文件和 `os.replace()` 原子替换。
先完成状态检查，再生成内容，最后提交替换。
发生异常时清理临时文件并保留原文件。

## 4. 与 GOV-NC-2026-11-22-REPO-ROOT-014 的关系

本登记与 014 关联，但不合并问题定义。

### 014：仓库根目录定位

014 处理的是：

    REPO_ROOT versus Path.cwd()

即脚本从仓库外部目录执行时，不能把调用者当前工作目录误当成仓库根目录。

其核心问题是路径解析锚点错误。

### 021：枚举边界和基线写保护

021 处理的是：

1. `Path.rglob()` 枚举磁盘，而不是 Git 跟踪集；
2. `write_baseline()` 缺少脏树拒绝机制。

其核心问题分别是文件集合定义错误和冻结状态写入缺少前置保护。

本次还必须保证相关 Git 操作、文件定位和 baseline 操作统一以 `REPO_ROOT` 为锚点，完成与 014 的集成回归。

021 不取代 014，也不意味着 014 的历史问题可以被重新归类为已经完成。

## 5. 实施要求

### 5.1 修复提交

通过独立新分支和新 PR 实施。

实施提交必须只包含：

- `scripts/check_bilingual_docs.py`
- 本登记的中文源；
- 中文逐字节镜像；
- 英文翻译镜像。

不得修改 `crates/` 或冻结基线。

关联 PR 的最终 head SHA 和合并 SHA 必须在验收记录中登记，不得预先伪造。

### 5.2 枚举实现

- 使用 `git ls-files`；
- 只接纳规范目录下的 `.md` 跟踪路径；
- 以仓库相对 POSIX 路径进行比较；
- Git 命令失败时拒绝继续；
- 不允许回退到磁盘递归枚举。

### 5.3 基线写保护

- 先检查 `git status --porcelain --untracked-files=all`；
- 非空即拒绝；
- 检查失败即拒绝；
- 使用同目录临时文件；
- 使用 `os.replace()` 完成原子替换；
- 异常时清理临时文件。

### 5.4 不变量

以下现有语义必须保持：

- `_require_full_git_history()` 仍在正常入口的 baseline/path 检查之前；
- `check_normative_pairing()` 不改变；
- `check_side_by_side_catch_up()` 不改变；
- `BILINGUAL-MANIFEST: COMPLETE` 的判定不改变；
- `PARTIAL_SIDE_BY_SIDE_PAIRS` 不改变；
- `PR_BODY` 仍由 `os.environ.get("PR_BODY", "")` 读取；
- 已跟踪文档的双语要求不放松；
- `scripts/bilingual-baseline.txt` 不修改。

## 6. 必须执行的测试清单

### T01：未跟踪 Markdown

在规范目录中创建未跟踪 `.md` 文件。

预期：

- 不进入 `current_bilingual_gaps()`；
- 不产生 New bilingual gap；
- 删除实验文件后工作树恢复干净。

### T02：pytest 缓存

在规范目录中创建或保留：

    08-bmcp-protocol/.pytest_cache/README.md
    08-bmcp-protocol/tests/conformance/.pytest_cache/README.md

预期：两个文件均不进入 gap 集合。

### T03：ignored Markdown

创建一个匹配 `.gitignore` 的 Markdown 文件。

预期：不进入 gap 集合。

### T04：已跟踪 Markdown

创建：

    06-memory-context/_probe-tracked.md

执行 `git add`，使其成为已跟踪文件，再运行闸门。

预期：

- 文件进入 gap 集合；
- 缺少双语镜像时仍报告新 gap；
- 退出码为 2。

这是防止本次修复意外放松闸门的强制回归锁。

### T05：脏树基线拒绝

保存原 baseline 的字节内容和 SHA-256。

创建未跟踪文件，运行：

    python scripts/check_bilingual_docs.py --write-baseline

预期：

- 返回非零；
- 输出明确拒绝原因；
- 原 baseline 字节完全不变；
- 不产生临时残留文件。

### T06：干净树基线写入

在干净 detached worktree 中执行：

    python scripts/check_bilingual_docs.py --write-baseline

预期：正常完成，生成内容与当前受跟踪文件 gap 集合一致。

### T07：外部 cwd

从仓库外部目录执行脚本。

预期：

- 使用 `REPO_ROOT` 定位仓库；
- Git 命令正常执行；
- baseline 使用正确仓库路径；
- 不受外部 `Path.cwd()` 影响。

### T08：冻结基线不变性

干净 detached 检出，设置：

    BASE_SHA=HEAD_SHA=origin/main

预期必须严格保持：

    bilingual baseline: 77 frozen, 0 new gaps
    exemptions: 21
    Bilingual documentation and prompt-library gate: PASS
    EXIT=0

77 条原有条目不得增减。

### T09：changed-path 语义

验证：

- changed-path 集合不变；
- side-by-side catch-up 行为不变；
- COMPLETE manifest 行为不变；
- PR_BODY 读取通道不变；
- shallow history 拦截仍先于 baseline/path 检查。

## 7. 最小复现步骤

1. 获取干净的 detached worktree。
2. 创建未跟踪的规范目录 Markdown 文件。
3. 运行双语闸门，确认它不产生新 gap。
4. 对该文件执行 `git add`。
5. 再运行闸门，确认它仍然产生新 gap。
6. 保存 baseline 原始字节。
7. 在脏树执行 `--write-baseline`。
8. 比较 baseline 原始字节，确认完全相同。
9. 清理实验文件，恢复干净工作树。
10. 再执行 `--write-baseline`，确认正常完成。
11. 从仓库外部目录运行闸门，确认仓库定位正确。

## 8. 关闭条件

本登记只有同时满足以下条件才允许关闭：

1. 新 PR 已创建，且未修改既有 PR。
2. 修复范围符合本登记的文件限制。
3. Git 跟踪集成为唯一 gap 枚举来源。
4. Git 失败路径经过验证，确保 fail-closed。
5. 七项新增测试全部通过。
6. 冻结基线严格保持 77 条。
7. exemptions 严格保持 21 条。
8. 已跟踪缺双语文件仍能触发 EXIT=2。
9. 脏树基线写入被拒绝，原文件字节不变。
10. 干净树基线写入成功。
11. 仓库外部 cwd 测试通过。
12. changed-path 及 shallow-history 相关行为没有回归。
13. 中文源与 `docs/zh-CN` 镜像逐字节一致。
14. `docs/en` 内容与中文源语义一致。
15. PR body 包含：

    BILINGUAL-MANIFEST: COMPLETE

16. 协调方提供真实命令输出、最终提交 SHA 和独立验收证据。

在全部关闭条件满足之前，登记状态保持 OPEN。

## 9. 治理结论

双语闸门的输入集合必须由版本控制事实定义，而不是由某一工作树当前恰好存在的文件定义。

冻结基线是受治理状态，不是工作树扫描结果的任意快照。

因此：

- 枚举必须可复现；
- 跟踪状态必须明确；
- 基线写入必须有前置保护；
- 文件替换必须具有原子性；
- 所有失败必须可见，不能静默放行。

本登记只修复上述边界，不授权降低任何既有双语合规要求。
