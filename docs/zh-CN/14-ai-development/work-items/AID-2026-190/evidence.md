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
        - "14-ai-development/work-items/AID-2026-190/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "本节每个数字都是在本工作树、基点 4326669caa6c43193d34219a0451b80762b712ff 上运行所列 git 命令得出的；针对 8142b1ca 的十用例运行，所用文件由 git archive 从该提交解出。本工作项修正的两份记录只被引述、未被重新断言。凡未由这里所示命令产出的 CI 结果、合并结果或 blob 摘要，一律不作声称。"
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
    canonical_scope: "AID-2026-190：修正两份无法从仓库树复现其测试输出与 blob 身份的治理记录"
    canonical_scope_id: "ai-development/aid-2026-190-unreproducible-governance-identities"
    canonical_scope_keywords:
      - "governance-register"
      - "restore-evidence"
      - "blob-identity"
      - "reproducibility"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-190/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-190/evidence.md"
    zh-CN: null
---
# AID-2026-190 — 两份治理记录载有本仓库无法复现的测试输出与 blob 身份

**状态：DRAFT — 仅记录与追加修正。** 任何历史表格、历史声明与 front-matter 声明都未被编辑。每份受影响文件只追加了一节 `## Correction (2026-11-27)`，两处 `verification_status` 仍保留原作者写入的值。

## 1. 本记录为何存在

两份已合并的记录声称的验证，树并不支持：

- `14-ai-development/governance-register/GOV-REV-2026-11-21-PR425-001.md` §2 粘贴了十行 `ok`，来源是 `python -m unittest discover -s 04-memory-compiler/reference-model`；§3 又在这条基线上搭了一张变异表（M0 基线、M1/M2 KILLED、M3 SURVIVED）。而在 `origin/main` 上，没有 `04-memory-compiler/reference-model` 目录，也没有任何包含这十个名字的测试文件。
- `14-ai-development/work-items/AID-2026-113/restore-evidence.md` 声明 `verification_status: Verified`，说明为「Source and mirror blob identities … recorded」，两张表共列出 15 个新 blob SHA。这 15 个 SHA 没有任何一个能作为 git 对象解析，也没有任何一个等于该路径实际所在的 blob。

两份文件都会被后来者当作"数字经过推导"的证据引用。无法从仓库重新推导的记录比没有记录更糟，因为它转嫁了一份从未赚到的信任。因此本工作项不改写任何一份文件，只追加一段读者在 `main` 上能自己重跑的测量，并写明该测量支持什么、不支持什么。

## 2. GOV-REV-2026-11-21-PR425-001 — 十行 `ok`，零匹配代码

测量点：`origin/main` = `4326669caa6c43193d34219a0451b80762b712ff`。

| 量 | 值 | 测量方式 |
|---|---|---|
| HEAD 上 `04-memory-compiler/` 下的文件数 | 7 | `git ls-tree -r --name-only HEAD -- 04-memory-compiler` |
| HEAD 上 `04-memory-compiler/reference-model/` 下的文件数 | 0 | 同一条命令换路径 |
| HEAD 上包含十个用例名中任意一个的 Python 文件数 | 0 | 十条独立的 `git grep -c -F "<name>" HEAD -- "*.py"`，均无输出、退出码 1 |
| HEAD 上包含这些名字的文档数 | 每个名字 3 份；`test_validation_rejects_digest_mismatch` 另在 `TEST-DRAFT-2026-11-21-PR425-M3.md`（canonical / en / zh-CN）出现 | `git grep -l -F "<name>" HEAD` |
| 从 `origin/main` 可达、且曾含 `04-memory-compiler/reference-model` 的提交数 | 0 | `git merge-base --is-ancestor 8142b1ca origin/main` 退出 1 |

### 2.1 这十个用例确实存在的位置

`git ls-remote --heads origin owner-e/gap-01-memory-compiler-contract` 返回 `8142b1caadd17770685d0b1f2816e584065854ac`——正是登记 §1 记下的 exact head，位于一个从未合并的分支上。用 `git archive` 从该提交解出 `04-memory-compiler/reference-model`，在其中执行登记自己的发现模式，实测：

```
Ran 10 tests in 0.001s

OK
EXIT=0
```

所以追加的修正并不称粘贴的输出是伪造的。它记录的是更窄、也可核查的缺陷：该输出只能对着一个未被合并的分支复现，而原记录从未把那个分支作为分支记下来——§1 钉的是一个 main 上不可达、只有在显式 fetch 该分支后才存在的提交对象。只持有 `main` 的读者无法验证 §2，也就无法验证 §3 三条变异判定所依据的 M0 基线。

文件中记录的结论：`NOT_VERIFIABLE_FROM_REPOSITORY`。

## 3. AID-2026-113 — 十五个新 blob 身份，全部不可解析

| 量 | 值 |
|---|---|
| 两张表中的新 blob 单元格数 | 15（5 个 Canonical + 10 个镜像） |
| 可通过 `git cat-file -t` 解析的新 blob SHA | 0 / 15（`fatal: git cat-file: could not get object info`，退出 128） |
| 等于 `origin/main:<path>` 处 blob 的新 blob SHA | 0 / 15 |
| 等于复原提交 `9142698f:<path>` 处 blob 的新 blob SHA | 0 / 15 |
| 同表中可解析的源、原始与孤立镜像 blob SHA | 17 / 17 |
| 等于 `1908ce4d:<path>` 的 Canonical 源 blob | 5 / 5 |
| `1908ce4d:<path>` 与 `9142698f:<path>` 逐行对比的删除行数 | 五个文件均为 0 |
| 复原新增的 frontmatter 行数 | 47 / 48 / 53 / 47 / 48 |

复原本身是真的：15 个路径在 `main` 上都存在，每个 Canonical 文件只增加了 frontmatter，正与 `FRONTMATTER_ADDED; source body retained unchanged` 相符。失败的是身份那一列。不在对象库中的 SHA-1 不可能标识该路径的任何已提交版本，因此该列无法描述文件所报告的复原，建立在其上的 `Verified` 说明按字面不成立。

文件中记录的结论：`NEW_BLOB_IDENTITIES_NOT_VERIFIABLE`。

## 4. 改了什么，没改什么

六个文件被修改，且均为追加：

| 文件 | 新增行 | 删除行 |
|---|---|---|
| `14-ai-development/governance-register/GOV-REV-2026-11-21-PR425-001.md` | 91 | 0 |
| `docs/en/14-ai-development/governance-register/GOV-REV-2026-11-21-PR425-001.md` | 91 | 0 |
| `docs/zh-CN/14-ai-development/governance-register/GOV-REV-2026-11-21-PR425-001.md` | 91 | 0 |
| `14-ai-development/work-items/AID-2026-113/restore-evidence.md` | 70 | 0 |
| `docs/en/14-ai-development/work-items/AID-2026-113/restore-evidence.md` | 70 | 0 |
| `docs/zh-CN/14-ai-development/work-items/AID-2026-113/restore-evidence.md` | 70 | 0 |

明确未改动：

- 追加节之前的任何表格单元格、粘贴输出块与正文段落；
- 任何 `verification_status`、`last_verified_date`、`last_verification_note` 值——原始声明原样留存，修正就写在它旁边，说明它不成立；
- 任何 blob、`05-memory-runtime/` 下的 canonical 文档、`04-memory-compiler/` 下的任何文件；
- 任何 checker、基线、注册表、工作流或 required context；
- 没有把任何一份记录重新声明为 verified，也没有推断 §5 审查者会得出什么结论。

## 5. 复现

```bash
# GOV-REV-2026-11-21-PR425-001
git ls-tree -r --name-only HEAD -- 04-memory-compiler/reference-model        # 零行，退出 0
git ls-tree -r --name-only HEAD -- 04-memory-compiler                        # 七个文件，无 reference-model/
git grep -c -F "test_derive_identity_is_stable" HEAD -- "*.py"               # 无输出，退出 1
git grep -l -F "test_validation_rejects_digest_mismatch" HEAD                # 六份文档，无代码
git ls-remote --heads origin owner-e/gap-01-memory-compiler-contract
git merge-base --is-ancestor 8142b1ca origin/main; echo $?                   # 1

# AID-2026-113
git cat-file -t 028bc3b63693145617290ef1b8f8cd617f931e2e                     # fatal，退出 128
git rev-parse origin/main:05-memory-runtime/activation-policy-engine.md      # 11ee1a70…
git rev-parse 9142698f:05-memory-runtime/activation-policy-engine.md         # ce15bec1…
```

上面每一行 `git grep ... -- "*.py"` 都对着修正节里的十个名字逐条执行过；十条全部无输出、退出 1。

## 6. 本记录不主张的事

- 不主张粘贴的十行 `ok` 是凭空编造；它记录的是这些输出无法从 main 可达的任何内容复现，并指出那个能复现的分支。
- 不主张 AID-2026-113 的复原没有发生；它记录的是描述该复原的身份列不可解析，而复原内容本身核对通过。
- 不主张任何原作者存有恶意。身份列与终端粘贴输出都是最容易手工转抄、也最难发现抄错的东西。
- 不关闭或重开任何 Issue，也不对这两份文件断言任何验收决定。
