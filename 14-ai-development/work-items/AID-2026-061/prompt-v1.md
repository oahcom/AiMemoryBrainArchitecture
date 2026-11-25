# WO-01 executed prompt snapshot (consolidated)

This file consolidates the two prompts the ruling session received for this work
item. They are reproduced verbatim below; nothing was edited or reordered.

Provenance is `NOT_VERIFIED`, as recorded in `manifest.yaml`. The digest proves
this file has not changed since it was pinned. It does not prove the ruling
session received these bytes.

---

## 1/2 — Round 30: exact patch specification

# REQ-01 / Round 30 — WO-01 落地：仓库自带治理门禁与「故意失败 Head 实验」的现有载体

同一会话续接。基线 `main = a33b482e`。R29 已封版调查交付物，转入 WO-01（F9）执行。

本轮我在派工前先普查了仓库自带的门禁基础设施，发现 **WO-01 的大部分零件已经在仓库里**，而且仓库自己的治理文档已经把你要的负向实验列为「未执行、故未证明」。请据此把 WO-01 收敛成一份**可直接落地的补丁规格**，不要新增机制。

## §1 新证据：仓库已有「声明 context ↔ workflow job」的机器门禁

`.github/workflows/repository-hygiene.yml:109-123`：

```
109        # PR-GOVERNANCE-001 §7 declares the required check contexts on `main`.
110        # Renaming a job leaves the document claiming a context nothing produces;
111        # this holds the declaration to the tree. Exit 2 (INCOMPLETE) is a failure
112        # here too: an unreadable condition must never read as green.
113        - name: Check declared check contexts are produced by a job
114          run: python3 scripts/check_declared_check_contexts.py
115
116        # Run from this directory because test_check_declared_check_contexts
117        # imports its checker by bare name.
118        - name: Self-check the declared-check-contexts gate
119          shell: bash
120          run: |
121            set -euo pipefail
122            cd scripts
123            python3 -m unittest test_check_declared_check_contexts
```

存在文件：`scripts/check_declared_check_contexts.py`、`scripts/test_check_declared_check_contexts.py`。

声明载体：`14-ai-development/PR-GOVERNANCE-001.md:258-272`，带机器可读标记：

```
258  <!-- declared-check-contexts: read by scripts/check_declared_check_contexts.py -->
259  ```text
260  GOV-DOC-001 structural checks
261  Branch freshness vs base
262  audit
263  GOV-DOC-002 metadata checks
264  BMCP protocol index (hard gate)
265  BMCP conformance suite (hard gate)
266  Schema non-empty audit (hard gate)
267  Bilingual docs coverage (ratchet)
268  Rust clippy (hard gate)
269  Repository hygiene (hard gate)
270  Rust format (hard gate)
271  Rust doctests (hard gate)
272  ```
```

→ **要做的不是新建配置漂移检查，而是把 `rust-workspace-test` 与 `Session Evidence` 加进这个已存在的声明块 + 真实 branch protection，让已有门禁自动开始校验它们。**

## §2 新证据：仓库自己的规范已经把「故意失败 Head 实验」记为未执行

`14-ai-development/PR-GOVERNANCE-001.md:256`（英文）：

> - **Status checks — enforced.** 12 required contexts, `strict: true`, `enforce_admins: {enabled: true}`, `allow_force_pushes: {enabled: false}`, `allow_deletions: {enabled: false}`. A required check that fails or is absent on the exact Head cannot merge through the normal path. The twelve names are declared below so that each must still be produced by a workflow in this tree:

`:275`：

> - **The deliberately-failing-head experiment — not run, so that half is unproven.** The 12-context payload proves the configuration, not the behaviour under a failing Head. Until that experiment is executed and recorded, "a deliberately failing required check cannot merge" MUST NOT be recorded as satisfied.

`:281`（中文镜像，同义）：

> - **故意失败 Head 实验——未执行，故该半条件未获证明。** 12 条上下文的载荷证明的是配置，不是失败 Head 下的实际行为。在该实验被执行并记录之前，「故意失败的必需检查无法合并」MUST NOT 记为已满足。

`:283-285`：该未决问题由 Issue `#134` 承载；Issue 状态不构成强制执行证据。

`:274` 另有一条与本仓实际情况一致的事实：**本仓库只有一个写入身份**，`作者 == 合并者 == 批准者` 在账号层面成立，故 `required_pull_request_reviews` 缺失是**设计**而非遗漏；`required_conversation_resolution = {enabled:false}`。

## §3 新证据：目标 workflow 的现状（逐行）

`.github/workflows/rust-phase1.yml` 全文 43 行：

```
1   name: Rust Phase 1 Workspace Tests
2
3   on:
4     pull_request:
5       branches: [main]
6       paths:
7         - "Cargo.toml"
8         - "Cargo.lock"
9         - "crates/**"
10        - "scripts/check_fmt.py"
11        - "scripts/test_check_fmt.py"
12        - ".github/workflows/rust-phase1.yml"
13    push:
14      branches: [main]
15      paths:
16        - "Cargo.toml"
17        - "Cargo.lock"
18        - "crates/**"
19        - "scripts/check_fmt.py"
20        - "scripts/test_check_fmt.py"
21        - ".github/workflows/rust-phase1.yml"
22
23  permissions:
24    contents: read
25
26  jobs:
27    rust-workspace-test:
28      runs-on: ubuntu-latest
29      timeout-minutes: 45
30      steps:
31        - uses: actions/checkout@v4
32        - name: Self-test format checker against dirty worktrees
33          run: python3 scripts/test_check_fmt.py
34        - uses: dtolnay/rust-toolchain@stable
35          with:
36            components: rustfmt
37        - name: Verify repository formatting at this commit
38          run: python3 scripts/check_fmt.py --expect "$GITHUB_SHA"
39        - name: Test all workspace targets
40          run: cargo test --workspace --all-targets --no-fail-fast
41        - name: Test workspace doctests
42          run: cargo test --workspace --doc --no-fail-fast
```

关键点：`rust-workspace-test` 这个 job **没有 `name:` 字段**，因此它的 check context 名就是 job id `rust-workspace-test`。`timeout-minutes: 45` 已设。

`.github/workflows/session-evidence.yml:15-16` 的 context 名是 `Session Evidence`（job 内 `name: Session Evidence`）。

## §4 请你产出 WO-01 的可落地补丁规格

不要新增任何脚本或机制。请按下列五项，给出**逐字节可套用**的内容。

**P1 `rust-phase1.yml` 的 `on:` 块新文本。**
要求：
- `pull_request` **删除 `paths` 过滤**（对本仓而言任何 PR 都必须跑一次 workspace 全量测试）。
- `push` 是否保留 `paths`，请裁定并说明理由（保住 CI 预算 vs 避免分支 stale 后的重复消耗；注意 `strict:true` 下 stale 分支要求重新验证）。
- 是否给 job 加 `name:` 字段？若加，必须同步 P3 的声明块与 P5 的 branch protection payload，三处字符串必须逐字一致；若不加，说明为何沿用 job id 作为 context 名更好。

**P2 `Session Evidence` 的 jobs 是否需要改 `on:`。**
其现状（`session-evidence.yml:1-18`）：

```
1   name: Session Evidence Gate
2
3   on:
4     pull_request:
5
6   permissions:
7     contents: read
8     pull-requests: read
9     issues: read
10
11  env:
12    AI_SESSION_EVIDENCE_EFFECTIVE_AT_UTC: "2026-12-01T00:00:00Z"
13
14  jobs:
15    session-evidence:
16      name: Session Evidence
17      runs-on: ubuntu-latest
18      timeout-minutes: 5
```

→ `pull_request:` 无 `branches` / `paths` 过滤，即**已对所有 PR 产生结果**。请直接裁定「无需改动」或指出仍缺的触发条件（例如 `push` 到 main 后的自检），并说明 `2026-12-01` 生效日与该实验的先后关系：**在生效日之前**把 `Session Evidence` 加进必需集，是否会让生效日前的所有 PR 因「未生效而判 pass」或「未生效而判 fail」而被误阻断？请给判定依据。

**P3 `PR-GOVERNANCE-001.md` §7 声明块的新全文（英文块 + 中文镜像同步）。**
要求：新增两条 context 后的完整 `text` 块（保持既有顺序风格）、并把「12 required contexts」改为新数量；给出 `:256` 与 `:279` 两处的替换文本（英文/中文各一段）。

**P4 §7「未执行」段落的处理口径。**
分两种情形给出最终文本：
- (a) 实验执行**成功**（故意失败的必需检查确实阻断合并）→ `:275`/`:281` 应改成什么（须保留「这是带日期的实测」风格，不得写成永久断言）；
- (b) 实验执行**失败**（未能阻断）→ 应改成什么，以及必须同时新增什么记录（不得静默改口）。
请给出两种情形各自的英文 + 中文成稿。

**P5 branch protection 的新 payload 规格。**
给出需要 PUT 的完整字段（`required_status_checks.contexts` 全量列表，含新增两条与顺序），并明确：
- 是否必须与 P3 声明块**完全同集合**（多一条/少一条会怎样，`check_declared_check_contexts.py` 会怎么判）；
- `strict: true` / `enforce_admins: true` 是否应在同一次 PUT 中保持不变；
- 变更后如何用 `GET` 复核（给判定字段）。

**P6 故意失败 Head 实验的执行协议。**
必须满足：
- 在**独立分支**上制造一个**真实的**失败（请指定用哪一种：故意失败的单元测试 / 故意不合格式的文件 / 其他），且该失败必须落在 `rust-workspace-test` 的检查范围内；
- 开 PR 到 `main`，等待必需检查产生结果；
- 用 `PUT /pulls/{n}/merge` 实际尝试合并，`405` 为预期；
- 记录：PR 号、Head SHA、失败 job 名、失败日志摘要、merge API 返回的 `message`；
- 实验后如何处置（关闭 PR 还是保留证据分支）；
- 该实验产生的证据应写进哪里（`PR-GOVERNANCE-001.md` §7？Issue `#134`？还是 WO 结项记录？给出唯一落点，不要三处都写）。

## §5 边界

- 不许新增工作流、脚本、检查器；只允许改上述三个已有载体的文本与 GitHub 配置。
- 文档改动必须中英双语同步（本仓有 `Bilingual docs coverage (ratchet)` 与 `GOV-DOC-001` 两道门禁）。
- 不要写实现代码以外的解释；直接给可套用的文本块。

最后一句请回答：**P1–P6 全部落完后，F9-E 能否翻绿；若不能，还缺哪一条。**

---

## 2/2 — Round 31: compliant PR body and evidence carrier

# REQ-01 / Round 31 — WO-01 已开 PR 并被三道门禁拦下：请给合规的 PR 正文与证据载体

同一会话续接。R30 的 P1/P3 已按你的文本**逐字节落盘**并开 PR。结果：`rust-workspace-test` 绿（证明 P1 有效），但 PR 被三道门禁拦下。GitHub REST 配额此刻耗尽（5000/5000，约 30 分钟后重置），我先把失败原文交给你，请裁定处置。

## §1 已落地的事实

- 分支：`governance/wo01-required-contexts`，PR **#1018**。
- 变更仅两文件：`.github/workflows/rust-phase1.yml`（删 `pull_request.paths`，保留 `push.paths`，不加 `name:`）、`14-ai-development/PR-GOVERNANCE-001.md`（§7 声明块 12→14，中英各一处）。
- 本地预检通过：`python3 scripts/check_declared_check_contexts.py` → `::notice::14 declared check contexts, all produced` / `DECLARED CHECK CONTEXTS: PASS`。
- 已 rebase 到最新 `main = e95c6198`（含 `#1020` session-evidence mutant tests、`#1014` 自测跑 head、`#1011` 模板对齐）。

## §2 三道门禁的失败原文（逐字）

**F-1 `Branch freshness vs base`｜已修复。** 开 PR 时 `main` 已从 `a33b482e` 前进到 `a3a62021`；`rebase origin/main` 后推送成功。此类失败是 `strict:true` 的正常行为，不需裁定。

**F-2 `GOV-DOC-001 structural checks`｜`failure`**

```
##[error]Normative source files changed but PR body lacks 'BILINGUAL-MANIFEST: COMPLETE' or a fully documented 'BILINGUAL-EXCEPTION: APPROVED'.
Bilingual documentation gate: FAIL
```

对应代码 `scripts/check_bilingual_docs.py:1156-1172`：`NORMATIVE_ROOTS` 下的 `.md` 变更，若 PR 正文无 `BILINGUAL-MANIFEST: COMPLETE` 也无例外声明，直接判错。

而 `PR-GOVERNANCE-001.md` 本身登记在 `EMBEDDED_BILINGUAL_SOURCES`（`check_bilingual_docs.py:133-136`，理由是「Defines shared PR lifecycle, review, and integration controls; divergent copies could assign different authority to the same repository actions.」），故 `check_normative_pairing` 对它 `continue` 跳过配对检查——**它不需要外部对照文件，只需正文声明**。

**F-3 `Session Evidence`｜`failure`**

```
MISSING: PR: missing AI-assisted work declaration
```

对应 `scripts/governance/session_evidence/validate.py`：
- `check_01_pr_fields_and_issue_references` 先跑 `_parse_status(_extract_field(ctx.body, "AI-assisted work"), "PR")`，取不到即抛 `{location}: missing AI-assisted work declaration`（`:431-435`）。
- 字段别名表 `FIELD_ALIASES`（`:325-335`）只认五种标签：`ai-assisted work`、`session evidence reference(s)`、`session evidence references`、`related issue(s)`、`related issues`、`owning issue`、`owning issue url`。
- 若 PR 声明 `YES`，`_parse_reference_lines` 解析出的每个路径必须是**PR Head tree 中的常规文件**（`check_04_head_tree_evidence_paths` → `_validate_regular_file`），且路径规范化规则严格（禁反斜杠、禁绝对路径、禁 URL scheme、禁 `%`、禁 `.`/`..` 段、禁空段）。
- 还必须存在**逐 Issue 映射表**：表头须同时含 `Related Issue`、`Issue AI-assisted work`、`Evidence refs for this Issue` 三个片段，每行**恰好三列**（`parse_pr_issue_table`，`:1` 起）。
- `mapping` 的 Issue 集合必须与 `Related issue(s)` 解析出的集合**完全相等**（`_run_checks:1946-1952`，`missing=`/`extra=` 报错）。
- 历史 Issue 豁免路径在 `:1959-1988`：`_historical_not_applicable` 为真（全部关联 Issue 均 `created_at < 2026-12-01` **且** 正文无 `AI-assisted work` 声明）时返回 `AI-SESSION-EVIDENCE: NOT_APPLICABLE (linked issue #N predates …)`；**但在该分支内若 PR 自身声明 `YES`，仍会执行 `check_04` + `_validate_reference_scopes` + `_check_manifest_entries`**（`:1962-1981`）。
- `_check_manifest_entries` → `_manifest_path_from_pr`（`body` 内必须出现 `AID-YYYY-NNN`，否则 `PR description: Work Item ID AID-YYYY-NNN is required`），再读 `14-ai-development/work-items/<AID>/manifest.yaml`，然后跑 check_09/10/11（manifest 结构、单值字段、prompt 快照哈希）。

## §3 需要你裁定的四项

**Q7. PR 正文的最终文本。**
请直接给出**完整 PR 正文**（可整段粘贴），必须一次性满足：`AI-assisted work`、`Session evidence reference(s)`、`Related issue(s)`、逐 Issue 三列映射表、`BILINGUAL-MANIFEST: COMPLETE`。要求：
- 若走「PR 声明 `NO` + 证据 `N/A`」路径，请说明它是否会在 `_historical_not_applicable` 分支下绕过 check_04/09/10/11；**并明确：本次改动确由 AI 会话产出，声明 `NO` 是否构成虚假声明**。若构成，则不得选此路径。
- 若走 `YES` 路径，请给出必须存在的证据文件路径与内容形态。

**Q8. 证据载体的选择。**
三条路，请择一并给理由：
- (a) 新建 `14-ai-development/work-items/AID-2026-06x/`（manifest + session evidence + prompt 快照），走完整 AID 体系；
- (b) 复用既有 AID（如 `AID-2026-059`）追加本 PR 的 session evidence；
- (c) 不写 AID，PR 正文声明 `NO`。
请特别说明：(b) 是否会污染他人的工作项归属；(a) 是否会触发 `Repository hygiene` 的新文件准入与 INDEX 登记要求；以及「本 PR 是纯治理门禁修复、不含领域产物」这一性质是否影响你的选择。

**Q9. `BILINGUAL-MANIFEST: COMPLETE` 的诚实性边界。**
`PR-GOVERNANCE-001.md` 是嵌入式双语单文件（中英同文件）。我实际只改了：英文 `:256`（`12`→`14`、`twelve`→`fourteen`）、声明块追加两行、中文 `:279`（`12 条`→`14 条`）。请裁定：
- 声明 `COMPLETE` 在此情形下是否属实（即「同一文件的两种语言均已同步修改」是否即为 complete）；
- 若属实，PR 正文该行应写成什么精确措辞才不越界；
- 若不属实，正确的声明形态是什么。

**Q10. 三道门禁的处置顺序与「实验」关系。**
F-2/F-3 修复后本 PR 才能合并；而 P6「故意失败 Head 实验」要求 `rust-workspace-test` 成为必需 context，这必须先合并本 PR 再 PUT protection。请确认：
- 顺序是否为「修 F-2/F-3 → 合并 #1018 → PUT 14 项 protection → 开 probe 分支跑 P6 → 回写 §7」；
- 在本 PR 尚未把 `rust-workspace-test` 列入 required 的当下，**它已经在 #1018 上真实运行并返回 `success`**（因为 P1 删了 paths 过滤）。请裁定：这是否构成「P1 生效」的独立证据，以及它是否**不能**替代 P6（即「能跑」≠「能阻断」）。

## §4 边界

- 不要给实现代码；只给 PR 正文文本、文件路径与内容骨架、以及顺序裁定。
- 任何声明必须与事实一致；不允许为了让门禁变绿而写与事实不符的字段。

最后一句：**若 Q8 选 (a)，本 PR 体积会从 2 文件扩到 5+ 文件；在「一个 PR 一个集成单元」的原则下，是否应拆成两个 PR（先 AID 载体、后门禁变更），还是必须同 PR？**
