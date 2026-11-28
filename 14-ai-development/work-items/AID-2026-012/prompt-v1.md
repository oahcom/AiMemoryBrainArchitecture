---
document_metadata:
  steward: "Architecture Governance"
  domain: ai-development
  role: reference
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Prepared from dispatch-provided repository facts. The execution step must verify generated artifacts against the stated repository HEAD and CI checks; this prompt itself is not an execution or acceptance record."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "The registration instructions and required evidence artifacts for work item AID-2026-012, covering the Protection fingerprint workflow and checker changes already present on the assigned branch."
    canonical_scope_id: "AID-2026-012"
    canonical_scope_keywords:
      - "AID-2026-012"
      - "Protection fingerprint"
      - "executed prompt"
      - "work item registration"
      - "session evidence"
    canonical_conflict_status: None
    normative_status: Informative
---

# AID-2026-012 Executed Prompt — Protection Fingerprint

# Execution prompt — register AID-2026-012

## 1. Role and execution objective

You are the registration-artifact author for work item `AID-2026-012` in repository `oahcom/AiMemoryBrainArchitecture`.

Execute this prompt against the assigned working tree:

- Working tree: `D:\code\wt-protection`
- Branch: `feat/2026-11-27-protection-fingerprint`
- `origin/main`: `cc5d22b9126e00e3f93ffe71282554309908bc89`
- Branch HEAD after rebase: `355b0ccf8`
- The branch has four commits.
- The work item identifier is assigned and fixed: `AID-2026-012`.

The objective is to produce the complete registration and PR-description package for the Protection fingerprint work already implemented on this branch. Do not redesign, reimplement, or rewrite the existing branch changes. Treat the supplied repository facts and constraints below as the controlling dispatch record, and verify repository state where the execution environment permits.

Produce exactly these deliverables:

1. `14-ai-development/work-items/AID-2026-012/manifest.yaml`
2. `14-ai-development/work-items/AID-2026-012/evidence.md`
3. `14-ai-development/work-items/AID-2026-012/session-evidence.md`
4. One new nine-column row to append to `14-ai-development/work-items/INDEX.md`; provide the row text only, not a replacement INDEX file.
5. A PR title.
6. A complete PR body.
7. A commit message.
8. A precise decision and, if applicable, exact front matter insertion for `14-ai-development/PR-GOVERNANCE-001.md`.

Do not create or modify any other file unless a repository checker proves that one of the required deliverables cannot otherwise be registered. If that occurs, explain the minimum necessary additional change explicitly; do not silently broaden scope.

Do not claim that a commit was created, a PR was opened or merged, an Owner accepted the work, or an Issue was closed. This task produces registration materials and proposed PR text; it does not authorize those actions.

## 2. Existing branch changes — describe, do not rewrite

The following changes already exist on the assigned branch. They are not to be recreated, overwritten, or modified as part of this registration task:

```text
.github/workflows/protection-fingerprint.yml
14-ai-development/PR-GOVERNANCE-001.md
14-ai-development/design/protection-fingerprint-ratchet.md
scripts/ci/baselines/protection-fingerprint.json
scripts/ci/check_protection_fingerprint.py
scripts/ci/test_check_protection_fingerprint.py
```

The branch changes are understood to be:

- The checker reads `GET /repos/{owner}/{repo}/branches/{branch}` (the branch summary endpoint) and does not call the Administration-only `/protection` endpoint.
- The checker supports `--endpoint auto|full|summary`; `auto` is the default and tries `full` first, falling back to `summary` on HTTP 401, 403, or 404.
- The baseline uses `schema_version: 4` and contains:
  - `fingerprint`: 12 fields;
  - `summary_fingerprint`: `enabled`, `contexts`, and `enforcement_level`;
  - `experiment`: date `2026-11-25`, head `b5cf4f25…`, PR `#1038`, run `138943464904`.
- The workflow is named `Protection fingerprint`. Its only triggers are `push: main`, daily cron `0 3 * * *`, and `workflow_dispatch`. It has no `pull_request` trigger.
- A real local run without a token produced `DEGRADED MODE — 3 field(s) verifiable, 11 unverifiable` and exit code 0.
- The offline test command `cd scripts/ci; python -m unittest test_check_protection_fingerprint` passed all 60 tests.
- The platform currently has 16 required contexts. `Protection fingerprint` is not one of them, and this PR must not make it a required check.

The 16 platform-required contexts measured by `GET /branches/main/protection` are:

1. `GOV-DOC-001 structural checks`
2. `Branch freshness vs base`
3. `audit`
4. `GOV-DOC-002 metadata checks`
5. `BMCP protocol index (hard gate)`
6. `BMCP conformance suite (hard gate)`
7. `Schema non-empty audit (hard gate)`
8. `Bilingual docs coverage (ratchet)`
9. `Rust clippy (hard gate)`
10. `Repository hygiene (hard gate)`
11. `Rust format (hard gate)`
12. `Rust doctests (hard gate)`
13. `Session Evidence`
14. `Session Evidence self-test (base)`
15. `Session Evidence self-test (head)`
16. `rust-workspace-test`

The `PR-GOVERNANCE-001.md` declaration currently has 17 entries, while the platform has 16 required contexts. Do not describe these as an exact match. Preserve the distinction between the 16 platform-required contexts and the 17 declared entries.

## 3. Registration artifact requirements

### 3.1 Manifest

Create `14-ai-development/work-items/AID-2026-012/manifest.yaml`.

The manifest must satisfy every rule in section 4.A and 4.B below. In particular:

- Use the fixed identifier `AID-2026-012`.
- Use a clear title describing the Protection fingerprint workflow/checker work.
- Set the repository to `oahcom/AiMemoryBrainArchitecture`.
- Record the assigned base branch and exact base commit SHA from this prompt.
- Record the actual implementation status supported by the branch. Do not mark work accepted or complete merely because the implementation is present.
- List the six existing changed paths in `implementation.files_changed`, accurately distinguishing implementation, design, baseline, tests, workflow, and governance declaration.
- Include non-empty `documentation` and `session_evidence` lists.
- Every documentation path must exist in the target HEAD git tree. Do not list a file that is only planned for creation unless it will exist in the final target tree.
- For the session evidence entry, use the actual `session-evidence.md` path and record the executing AI session identifier given in section 5.
- In the session evidence entry, include `executed_prompt_snapshot_file` pointing to this exact prompt file:
  `14-ai-development/work-items/AID-2026-012/prompt-v1.md`.
- Set `executed_prompt_sha256` to the literal placeholder token `EXECUTED_PROMPT_SHA256_TOKEN`.
- Set `executed_prompt_bytes` to the literal placeholder token `EXECUTED_PROMPT_BYTES_TOKEN`.

The two placeholder tokens are intentional. The orchestration layer will replace them with the actual SHA-256 and byte length after this prompt file has been written to disk. Do not estimate, calculate from a partial copy, or substitute invented values.

Use strict YAML with no duplicate keys. Ensure every required top-level field is present exactly once.

### 3.2 Evidence

Create `14-ai-development/work-items/AID-2026-012/evidence.md`.

The evidence document must distinguish:

- supplied and independently verified facts;
- branch implementation facts;
- local test results;
- limitations and degraded-mode behavior;
- facts that still require execution-time or PR-time verification.

Record the exact local test command and the reported result of 60 passing tests as dispatch-provided evidence. Do not claim that you personally ran the command unless you actually did so in the execution environment.

Explain the security and operational reason for the summary endpoint/degraded behavior without claiming that all 12 full-protection fields are observable with the workflow token.

Include the baseline experiment metadata exactly as supplied. Clearly distinguish that metadata from the current branch HEAD and base SHA.

Include the workflow trigger policy and state explicitly that the workflow has no `pull_request` trigger.

Include the platform-required context count and list or otherwise faithfully identify all 16 names from section 2. State that `Protection fingerprint` is not required and is not added to the required-context list by this PR.

Do not claim merge, acceptance, deployment, or Issue closure.

### 3.3 Session evidence

Create `14-ai-development/work-items/AID-2026-012/session-evidence.md`.

Use the session facts in section 5. Preserve all ten recorded rounds, timestamps, prompt filenames, prompt character counts, reply character counts, and supplied round identifiers exactly. Do not infer missing round identifiers for rounds for which none were supplied.

The session is:

- Session ID: `6b0935f1-14d8-83ec-92e4-31725a7c96a7`
- Account: `acct3`
- Conversation log: `logs/conversations/6b0935f1-14d8-83ec-92e4-31725a7c96a7.jsonl`

The log contains ten begin/end pairs. Every recorded round has `status 200` and `reply_state captured`.

Include an `## Actual AI input` section. It must be non-empty and must contain the actual `SEND <prompt_file> -> 200 respLen=… in …s` records and the conversation ID. The literal SEND records are not contained in the supplied session table; they exist only in the delivery process stdout. The orchestration layer will return the actual SEND lines for this registration execution after delivery. Insert those exact returned records into `## Actual AI input`. Do not invent, reconstruct, paraphrase, or fabricate SEND lines or response lengths. If the records have not yet been returned, explicitly mark the section as awaiting the orchestration-provided records rather than pretending that the requirement has been fulfilled. The final session evidence file must not be considered ready for submission until the actual records have been inserted.

Include the issue mapping required by section 4.D. The only relevant Issue identified by the dispatch is `#134`. Treat it as a historical Issue with undeclared AI-assisted work, and map it as `LEGACY_UNDECLARED` with evidence reference `N/A`.

### 3.4 Work item INDEX row

Provide one new row to append to `14-ai-development/work-items/INDEX.md`.

The row must contain exactly nine cells in the existing column order:

`| Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance |`

The first cell must link to:

`[AID-2026-012](AID-2026-012/manifest.yaml)`

The Prompt cell must link to `AID-2026-012/prompt-v1.md`. The Implementation cell must describe the existing Protection fingerprint implementation without implying that this registration task changed it. Use the appropriate current status; do not imply review or acceptance that has not occurred.

Append the row at the end of the table. Do not reorder or rewrite existing rows.

### 3.5 PR title, PR body, and commit message

Provide a concise PR title accurately describing registration of the Protection fingerprint implementation.

The PR body must include all of the following:

- `## Work Item ID`
- The exact work item ID `AID-2026-012`
- `AI-assisted work: YES`
- `## Session evidence`
- A parseable `Related issue(s)` field containing `#134`
- A three-column Issue mapping table with headers:
  - `Related Issue`
  - `Issue AI-assisted work`
  - `Evidence refs for this Issue`
- Exactly one mapping row for `#134`, with status `LEGACY_UNDECLARED` and evidence reference `N/A`
- A concise change summary identifying the existing workflow, checker, baseline, design, tests, and governance declaration changes
- Gate/test evidence, with attribution that the 60-test result and local degraded-mode result are supplied measurements unless independently rerun
- An explicit statement that the new `Protection fingerprint` workflow is **not** made a required check by this PR
- An explicit statement that `Protection fingerprint` is not among the 16 platform-required contexts
- An explanation that `GITHUB_TOKEN` cannot read `/protection`, leaving 11 full-protection fields unverifiable in the degraded summary mode, with a reference to the design document section `Why degrade instead of fail` (§9)
- No statement that the PR has been merged, accepted, or deployed, and no statement that Issue #134 has been closed

The commit message must follow this format:

`work-item(AID-2026-012): <concise description>`

Do not invent a commit SHA.

## 4. Hard constraints — preserve and obey exactly

The following constraints are copied from the dispatch specification. They are mandatory for the next execution. Do not weaken, omit, reinterpret, or silently normalize them.

### A. `scripts/ci/check_work_item_manifest_schema.py`

`REQUIRED` 顶层键（缺一即红）：`work_item_id` `title` `class` `risk` `risk_rationale` `status` `id_status` `sponsor` `accountable_owner` `acceptance_authority` `attribution` `date` `repository` `base_branch` `base_commit_sha` `scope` `evidence` `documentation` `session_evidence` `implementation`。
- `documentation` 必须是非空列表，每项 `{path, relationship}`，`relationship ∈ {normative, design, implementation, evidence, reference, code, schema}`，`path` 必须是**存在于 HEAD git tree** 的仓库相对路径（反斜杠、绝对路径、`..` 都红）。
- `session_evidence` 必须是非空列表，每项必须含 `role`、`issue_refs`、`implementing_ai_session`、`session_evidence_ref`；`session_evidence_ref` 的文件名必须以 `session-evidence` 开头、`.md` 结尾。
- `implementation` 必须含 `status`（`∈ {NOT_STARTED, IN_PROGRESS, IMPLEMENTED, BLOCKED, NOT_APPLICABLE}`）、`summary`、`files_changed`（列表）、`tests`（列表）。
- 顶层键重复即红（严格 YAML，重复键拒绝）。

### B. `scripts/ci/check_manifest_blob_pins.py`

`session_evidence[i].executed_prompt_snapshot_file` 配 `executed_prompt_sha256`（64 hex）与 `executed_prompt_bytes`（整数）时，二者必须等于该文件在提交树里的**整文件字节**的 SHA-256 与长度。执行者拿不到这个值，所以 manifest 里请写占位符 token：`EXECUTED_PROMPT_SHA256_TOKEN` 与 `EXECUTED_PROMPT_BYTES_TOKEN`，由编排层在落盘后用真实值替换。

### C. `scripts/check_document_management.py --require-changed origin/main`

所有新增/改动的受治理 `.md` 都必须有合法 front matter（同第 1 节字段）。**实测当前红**，原文：

```text
FAIL: 1 error(s)
  14-ai-development/PR-GOVERNANCE-001.md: DM-15 new governed document must declare a non-empty steward
```

原因：本分支改了 `14-ai-development/PR-GOVERNANCE-001.md`（新增 `Protection fingerprint` 到 declared 清单、并把「16 required contexts」改写成「16 platform-required contexts（declaration 列 17）」），而该文件的 front matter 没有 `steward` 字段。派发方曾机械地加过一行 `steward: "Architecture Governance"`（已 stash，未提交），需要你确认或另给值——请在下一步的输出里明确给出这个 front matter 改动（给出要插入的确切行与位置），或给出「撤回 PR-GOVERNANCE-001.md 改动」的决定与理由。注意该文件的 `approval.approval_applicability` 是 `Not-Applicable-To-Current-Version`，所以改 front matter 不会触发 DM-10 内容哈希失配（实测：只报 DM-15 一条）。

**Required decision for this registration:** retain the existing `PR-GOVERNANCE-001.md` content changes. Confirm the proposed steward value `Architecture Governance`. In the next-step output, specify the exact insertion line:

```yaml
  steward: "Architecture Governance"
```

Insert it as a member of the existing `document_metadata:` mapping, at the same indentation as the other `document_metadata` child fields. Do not insert it at the YAML root if `document_metadata` is a nested mapping. Do not revert the governance declaration changes merely to avoid the metadata repair. The approval applicability fact above means this metadata-only repair is not expected to trigger DM-10 content-hash mismatch; still run the checker to verify.

### D. `scripts/governance/session_evidence/validate.py`（CI 必过，context 名 `Session Evidence`）

- PR body 必须有可解析的 `Related issue(s)` 字段，且至少一个 `#N` 或 issue URL；`Related issue(s): None.` 会直接判 `MISSING: PR description: no parseable Related Issues`（实测解析函数行为）。
- 必须有 3 列表格，表头含 `Related Issue` / `Issue AI-assisted work` / `Evidence refs for this Issue`，每个 related issue 一行；行状态 `∈ {YES, NO, LEGACY_UNDECLARED}`；未声明 AI 工作的历史 Issue 必须 `LEGACY_UNDECLARED` + `N/A`。
- `Work Item ID` 字段写 `AID-2026-012`；`AI-assisted work: YES` 时 `Session evidence reference(s)` 必须给仓库相对路径（如 `14-ai-development/work-items/AID-2026-012/session-evidence.md`）。
- 派发方查到唯一真正相关的开放 Issue：**#134**（open，created 2026-11-17，`P0 — Enforce main merge gates; remediate PR #129 failed-check merge`）。它是历史 Issue，未声明 AI 工作 → 对应行 `LEGACY_UNDECLARED` + `N/A`。**不得引用 #1145**（无关）。请你决定 Related issue(s) 用 #134 还是别的，并给理由。

**Required decision for this registration:** use `Related issue(s): #134`. It is the only relevant open Issue identified by the dispatch, and its historical record did not declare AI-assisted work. Do not cite `#1145`. In the PR body and session evidence, map `#134` to `LEGACY_UNDECLARED` and `N/A`.

### E. `scripts/ci/check_repository_hygiene.py`

`INDEX.md` 与工作项目录必须双向一致（任一方向缺失都红）。新目录必须被 INDEX 链接，链接目标 `AID-2026-012/manifest.yaml` 必须存在。新文件准入按后缀/精确路径：`.md` 允许，`manifest.yaml` 由 `AID-\d{4}-\d{3}/manifest.yaml` 精确匹配允许。

### F. `14-ai-development/work-items/INDEX.md` 行格式

表头 9 列：`| Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance |`。新行追加到表末，第一列形如 `| [AID-2026-012](AID-2026-012/manifest.yaml) | …`，共 9 个单元格。

### G. 会话证据的既有事实（下一步 session-evidence.md 用）

会话 `6b0935f1-14d8-83ec-92e4-31725a7c96a7`（acct3），`logs/conversations/6b0935f1-14d8-83ec-92e4-31725a7c96a7.jsonl` 里 10 轮 begin/end，全部 `status 200`、`reply_state captured`：

| 轮 | ts | prompt_file | prompt_chars | reply_chars |
|---|---|---|---|---|
| R1 | 2026-11-27T15:49:00 | 34-protection-fingerprint.md | 4730 | 40033 |
| R2 | 2026-11-27T16:03:01 | round2.md | 2411 | 39664 |
| R3 | 2026-11-27T16:13:19 | round3.md | 3663 | 16107 |
| R4 | 2026-11-27T16:48:35 | round4.md | 4360 | 49051 |
| R5 | 2026-11-27T17:21:32 | round5.md | 2359 | 23398 |
| R6 | 2026-11-27T17:36:38 | round6.md | 3264 | 271 |
| R6b | 2026-11-27T17:38:40 | round6b.md | 52911 | 609 |
| R6c | 2026-11-27T17:40:12 | round6c.md | 3254 | 78096 |
| R6d | 2026-11-27T18:15:49 | round6d.md | 1167 | 216 |
| R6d2 | 2026-11-28T08:03:21 | round6d2.md | 24630 | 24758 |

派发方给的轮次标识原文：R1 `150456374`、R2 `30047903`、R3 `12033212`、R4 `112959637`、R5 `9268021`、R6c `240075069`、R6d2 `11275772`。
`SEND <prompt_file> -> 200 respLen=… in …s` 的字面记录只存在于投递进程 stdout；本轮及下一轮的 SEND 行由编排层在投递后原文回传，你再把它写进 `## Actual AI input`（该段必须非空且含真实 SEND 记录与 conv id）。

### H. 提交与 PR 纪律

- 提交作者 `oahcom <1491856051@qq.com>`；提交信息由你给（格式参考 `work-item(AID-2026-012): …`）。
- PR body 必须含 `## Work Item ID`、`AI-assisted work: YES`、`## Session evidence`、逐 Issue 映射表、变更摘要、门禁证据，并**写明**：本 PR 新增 workflow `Protection fingerprint`，**不设为 required**——它不在 16 条平台必需里；原因是 `GITHUB_TOKEN` 读不到 `/protection`，11 个字段永久不可验证，见设计文档《Why degrade instead of fail》（§9）。
- 不得声称合并、Owner 验收、Issue 关闭。

## 5. Required session record

Use this table without altering any supplied value:

| Round | Timestamp | Prompt file | Prompt chars | Reply chars | Supplied round identifier |
|---|---|---|---:|---:|---|
| R1 | 2026-11-27T15:49:00 | 34-protection-fingerprint.md | 4730 | 40033 | 150456374 |
| R2 | 2026-11-27T16:03:01 | round2.md | 2411 | 39664 | 30047903 |
| R3 | 2026-11-27T16:13:19 | round3.md | 3663 | 16107 | 12033212 |
| R4 | 2026-11-27T16:48:35 | round4.md | 4360 | 49051 | 112959637 |
| R5 | 2026-11-27T17:21:32 | round5.md | 2359 | 23398 | 9268021 |
| R6 | 2026-11-27T17:36:38 | round6.md | 3264 | 271 | Not supplied |
| R6b | 2026-11-27T17:38:40 | round6b.md | 52911 | 609 | Not supplied |
| R6c | 2026-11-27T17:40:12 | round6c.md | 3254 | 78096 | 240075069 |
| R6d | 2026-11-27T18:15:49 | round6d.md | 1167 | 216 | Not supplied |
| R6d2 | 2026-11-28T08:03:21 | round6d2.md | 24630 | 24758 | 11275772 |

Every one of these ten rounds has `status 200` and `reply_state captured` in the supplied conversation log facts.

The next execution of this prompt is an additional AI input. Its actual delivery record must be added when the orchestration layer returns it. The session evidence must include that actual SEND record and the conversation ID `6b0935f1-14d8-83ec-92e4-31725a7c96a7`. Do not represent the ten historical rounds as if they were the current execution's SEND record.

## 6. Verification and completion protocol

Before presenting the registration package:

1. Inspect the assigned branch and confirm the repository, branch, base SHA, and HEAD match the dispatch facts. If they differ, stop and report the exact observed values; do not silently substitute a different base or work item identifier.
2. Confirm the six existing changed paths in section 2 are present and describe their actual state. Do not overwrite them.
3. Confirm all `documentation[].path` entries selected for the manifest exist in the target HEAD git tree.
4. Ensure the manifest has every required top-level key, no duplicate YAML keys, and all nested structures satisfy section 4.A.
5. Leave the two executed-prompt pin fields as the exact placeholder tokens specified in section 3.1. The orchestration layer, not this authoring step, replaces them after the prompt is written.
6. Ensure the session evidence includes all ten historical rounds and does not fabricate the missing SEND lines. Keep the final file pending until the orchestration layer supplies the literal SEND records for the current and next execution.
7. Ensure the PR body satisfies the exact parser requirements in section 4.D, including the `Related issue(s): #134` field and the three-column issue mapping table.
8. Include the exact `document_metadata` steward insertion decision from section 4.C. Retain the existing governance declaration content changes.
9. Run the relevant repository checks when the environment permits. At minimum, check manifest schema, blob pins after orchestration substitutes the actual prompt hash/byte count, document management with `--require-changed origin/main`, repository hygiene, and Session Evidence validation against the proposed PR body.
10. Report actual command results only. If a check cannot be run, identify it as not run; do not infer success from supplied prior measurements.
11. Do not mark the work item accepted or claim that all gates pass unless the actual execution evidence supports those statements.

## 7. Output contract for the next execution

Return the deliverables in this order:

1. Full contents of `manifest.yaml`.
2. Full contents of `evidence.md`.
3. Full contents of `session-evidence.md`.
4. The single INDEX row.
5. PR title.
6. Full PR body.
7. Commit message, with author `oahcom <1491856051@qq.com>` identified separately if the execution environment requires author metadata.
8. The exact front matter insertion line and location for `PR-GOVERNANCE-001.md`.

Use explicit file/path labels so each artifact can be saved without ambiguity. Do not include replacement contents for the six existing branch files. Do not output this prompt again as one of the next-step artifacts. Do not change the assigned work item ID. Do not claim actions or verification that were not actually performed.
