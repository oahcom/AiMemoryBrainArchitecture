# AI-EXEC-002 Amendment Proposal — Canonical Prompt Reference Dispatch
# AI-EXEC-002 修订提案 — 规范提示词引用投递

- **Proposal ID:** AID-2026-001-AI-EXEC-002-ADD-001
- **Version:** 1.0
- **Status:** PROPOSED — NOT YET INCORPORATED OR ADOPTED
- **Target:** `14-ai-development/AI-EXEC-002.md`, §2 (开工前必录字段)
- **Exact target baseline:** main at the time of drafting; AI-EXEC-002 Blob SHA `c1d1e5bffe0a92af701e59c7f2627350b1d9fddf`
- **Carrier:** `remediation/aid-2026-001-forget-contract-closure-2026-11-18`
- **Work Item:** AID-2026-001 · Issue #41
- **Authority:** Integration Owner must incorporate/review this proposal in the canonical AI-EXEC-002 document. This file does not itself amend or adopt AI-EXEC-002.

## 1. Proposed rule (English)

Where an immutable, versioned prompt has been committed to the repository, a session may be dispatched by an exact repository reference instead of retransmitting the full prompt body. The repository file at the pinned commit is the sole canonical instruction source for that dispatch.

A valid short-reference dispatch MUST identify all of:

1. Repository full name.
2. Exact repository path.
3. Prompt ID and version.
4. Exact immutable commit SHA (not a branch, tag that can move, `main`, `latest`, or an unpinned PR head).
5. Assigned Owner/role.
6. Work Item ID and tracking Issue.
7. Any separately versioned run-specific addendum, each pinned to its own exact commit SHA.

Before execution, the receiving session MUST fetch and read the file at that exact commit, verify that Prompt ID/version and role/scope match the dispatch, and record the source path, commit SHA, Git blob SHA, actual UTF-8 byte count and SHA-256 when computable. Hash the actual repository bytes without Unicode/newline normalization. A missing or uncomputable SHA-256 is recorded as `NOT_VERIFIED`, never fabricated.

The receiving session MUST treat the pinned repository prompt as the complete and sole canonical instruction source. The short dispatch is routing metadata only: it MUST NOT silently add, remove, override, reinterpret or relax prompt instructions. Chat history, rendered UI copies, branch names and user-supplied summaries are not substitutes for the pinned file.

If the exact commit/file cannot be fetched, the Prompt ID/version does not match, or integrity cannot be established, STOP before task execution and report `PROMPT_SOURCE_UNAVAILABLE` or `PROMPT_INTEGRITY_UNVERIFIED`. Do not fall back to a chat-rendered copy.

Any material run-specific change MUST be a separately versioned and committed addendum, explicitly named in the dispatch and read alongside the base prompt. Do not inject substantive changes into the short dispatch itself.

A frozen historical prompt remains immutable. If its recorded branch/PR/base pins are stale or its own stop conditions are triggered, archive it as historical and author a new prompt version for current execution; do not silently refresh its pins in place.

## 2. 拟议规则（中文）

当一份不可变、带版本的提示词已提交到仓库时，会话可以使用精确仓库引用进行派工，无需每次重新传输完整提示词正文。该派工唯一规范指令源是所 pin 的精确 Commit 中的仓库文件。

短引用派工必须明确包含：

1. 仓库全名。
2. 精确仓库路径。
3. Prompt ID 与版本。
4. 精确、不可变的 Commit SHA（不得仅使用分支名、可移动 Tag、`main`、`latest` 或未 pin 的 PR Head）。
5. 指派的 Owner/角色。
6. Work Item ID 与跟踪 Issue。
7. 任何独立版本化的本次运行增补文件；每个文件均须 pin 到自己的精确 Commit SHA。

执行前，接收会话必须从该精确 Commit 获取并读取文件，核对 Prompt ID/版本及角色/范围与派工引用一致，并记录来源路径、Commit SHA、Git Blob SHA、实际 UTF-8 字节数，以及在可计算时的 SHA-256。必须对仓库实际字节计算摘要，不得进行 Unicode 或换行归一化。若 SHA-256 缺失或无法计算，记录为 `NOT_VERIFIED`，不得补造。

接收会话必须将所 pin 的仓库提示词视为完整且唯一的规范指令源。短派工仅用于路由，不得暗中增加、删除、覆盖、重新解释或放宽提示词指令。聊天历史、UI 渲染副本、分支名和用户摘要均不能替代精确 pin 的文件。

若无法获取精确 Commit/文件、Prompt ID/版本不匹配，或无法建立完整性证据，必须在执行任务前 STOP，并报告 `PROMPT_SOURCE_UNAVAILABLE` 或 `PROMPT_INTEGRITY_UNVERIFIED`。不得回退使用聊天渲染副本。

任何实质性的本次运行变更必须作为独立版本化并已提交的增补文件，在派工中明确列出，并与基础提示词一并读取。不得把实质变更塞入短派工文本。

冻结历史提示词必须保持不可变。若其记录的分支/PR/基线 pin 已过时，或触发了自身停止条件，应将其归档为历史版本，并为当前执行编写新版本；不得在原版本内静默刷新 pin。

## 3. Canonical short-dispatch template / 规范短引用模板

```text
Read and execute the immutable prompt:
Repository: <owner/repository>
File: <exact repository path>
Prompt ID: <ID> v<version>
Commit: <exact commit SHA>
Owner role: <assigned role>
Work Item: <AID-YYYY-NNN>
Issue: #<number>
Addenda (if any): <exact path>@<exact commit SHA>

The pinned repository file(s) are the sole canonical instruction source.
Fetch and read them before execution. Verify Prompt ID/version, role/scope,
and record blob SHA, actual UTF-8 byte count and SHA-256 (or NOT_VERIFIED).
If unavailable or integrity cannot be verified, STOP; do not use chat history
or rendered copies as fallback.
```

```text
读取并执行以下不可变提示词：
Repository: <owner/repository>
File: <精确仓库路径>
Prompt ID: <ID> v<版本>
Commit: <精确 Commit SHA>
Owner role: <指派角色>
Work Item: <AID-YYYY-NNN>
Issue: #<编号>
Addenda（如有）: <精确路径>@<精确 Commit SHA>

所 pin 的仓库文件是唯一规范指令源。
执行前必须获取并读取，核验 Prompt ID/版本、角色/范围，
并记录 Blob SHA、实际 UTF-8 字节数及 SHA-256（或 NOT_VERIFIED）。
若文件不可用或完整性无法核验，立即 STOP；不得回退使用聊天历史
或渲染副本。
```

## 4. Adoption and compatibility notes / 采纳与兼容说明

- This is a proposal artifact only. It does not change the current ADOPTED status or text of AI-EXEC-002.
- The target AI-EXEC-002 file was not present in the current AID-2026-001 remediation branch at its observed Head. This proposal therefore records the exact main-branch target Blob instead of copying the whole standard into the stacked branch.
- Integration Owner must re-read the current main version before incorporation; if its Blob differs from the pinned target above, rebase the proposal semantically and record the new source pin.
- Existing full-text prompt dispatch remains valid. This amendment adds a safe reference-based alternative; it does not force short references where the recipient cannot access GitHub.
- No claim is made that this proposal has been reviewed, adopted, or incorporated into AI-EXEC-002.
