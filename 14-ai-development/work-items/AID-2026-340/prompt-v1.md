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
        - "14-ai-development/work-items/AID-2026-340/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Prompt snapshot is an authoring reference. Exact transmission provenance has not been independently verified."
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
    canonical_scope: "Repair instructions for AID-2026-340 unrestored Phase 3.5/3.6 reference disclosure."
    canonical_scope_id: "ai-development/aid-2026-340-prompt-snapshot"
    canonical_scope_keywords:
      - "AID-2026-340"
      - "prompt"
      - "dangling-normative-reference"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# 角色

你是 `oahcom/AiMemoryBrainArchitecture` 的修复作者。你没有仓库读写权限，只输出逐字编辑块；我用脚本机械套用。

# 已裁决、待修的缺陷

## A. DEF-refs-03 / DEF-authority-02：Canonical 文档把规范内容指向仓库中不存在的文件

`git ls-tree -r --name-only origin/main` 证明下列文件**不存在**：

- `05-memory-runtime/phase-3.5-forget-suppression-and-cursor-consumption.md`
- `09-security-governance/phase-3.5-global-identity-forget-governance.md`
- `09-security-governance/phase-3.6-principal-trust-chain-authorization-revocation.md`
- `09-security-governance/governance-decision-register.md`

它们的状态已在 `14-ai-development/work-items/AID-2026-107/evidence.md` 登记为 `UNDECIDED / U-OWNER-DECISION`（`AID-2026-107/evidence.md:418`、`:435`、`:437`、`:444`），且该证据文件 `:20` 明写 "classified 189 missing paths ... **no missing path was restored**"。

**已有的正确写法先例**（英文镜像里已经这么做了，正文与 Canonical 不一致，属于镜像侧先行修复）：

```md
**Phase 3.5 dependency review:** D/E/I/G/H/C/B owner-branch contracts are present and were re-read at the exact heads recorded in `phase-3.5-forget-suppression-and-cursor-consumption.md`（未提交，见 [GAP-01](../../governance/documentation-gaps.md)）. F's consumer semantics are DECIDED; ...
```

```md
The normative F consumer matrix, ... are maintained in [phase-3.5-forget-suppression-and-cursor-consumption.md](../../governance/documentation-gaps.md).
```

即：**保留文件名作为历史指称，但把链接目标改为 `documentation-gaps.md`，并明写"未提交/未恢复"**。

## B. DEF-corpus-08：三份英文镜像的 `Source revision` 指针落后于 Canonical

实测（`origin/main`）：

| Canonical | 当前 canonical blob | 镜像里的 Source revision |
|---|---|---|
| `01-system-architecture/responsibility-matrix.md` | `7fc26ca93f4db3b5074156e76bee3555ac744e3a` | `85548fcee05b28f8c2d54d4c0a8bf77840c8cdf3` |
| `01-system-architecture/system-boundaries.md` | `bf20b204688bf51a1df76968db7e52ee0dd597c1` | `ad9ea5ce00e74dba89d325601677270a50f30926` |
| `00-governance/design-principles.md` | `9fb729a4bd6ebcfa9576e5318804a65e2a95abe2` | `9792e189d63fbbc3694ab891fc4aeba5143b3b1c` |

正文一致性实测（去掉 frontmatter 与 `- Document ID/- Version/- Source/- Source revision` 头块后逐行 diff）：

- `responsibility-matrix.md`：**2 行**差异，且只是 `- Status:` 行与一句"These questions remain design questions"的位置/格式；
- `system-boundaries.md`：**4 行**差异，`**Status:**` → `- Status:`、`**Scope:**` 行；
- `design-principles.md`：**2 行**差异，`**Current version status: APPROVED — Normative.**` → `- Status: APPROVED / Normative — ...`。

请你判断：**能否只更新 Source revision 指针**，还是必须同时把这几行正文差异也补齐（指针只能指向"镜像实际对应的源版本"，否则就是新的假证据）。按你的判断给块。

# 输出契约（严格）

只输出编辑块，不要解释、不要计划、不要复述。每个块：

```
===FILE: <仓库根相对路径>|REPLACE===
---OLD---
<逐字原文，必须与下方给出的原文完全一致，包括行尾空格>
---NEW---
<逐字新文>
===END===
```

规则：

1. `OLD` 必须能在给出的原文里逐字找到；找不到就说明你要改的是另一处，重新给。
2. 同一文件多处修改 → 多个块，块顺序按行号升序。
3. 不许改行尾、不许改缩进、不许改引号风格（英文文件用 ASCII 引号，中文文件用全角标点）。
4. 需要新增文件时用 `|CREATE`。
5. 不要输出 markdown 围栏包裹整段（块本身用三反引号是允许的，但不要额外再包一层）。

# 待改原文

### 05-memory-runtime/retrieval-engine.md:149
```
The detailed owner/consumer contract is in [Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract](phase-3.5-forget-suppression-and-cursor-consumption.md). This supplement supersedes any earlier provisional wording in this file where the two differ.
```

### 05-memory-runtime/runtime-overview.md:59
```
**Phase 3.5 dependency review:** D/E/I/G/H/C/B owner-branch contracts are present and were re-read at the exact heads recorded in `phase-3.5-forget-suppression-and-cursor-consumption.md`. F's consumer semantics are DECIDED; callable cross-module schemas, Storage realization and runtime conformance remain OPEN. No wire schema is frozen by this document.
```

### 05-memory-runtime/runtime-overview.md:148
```
The normative F consumer matrix, retrieval-stage suppression matrix, cache/Working Set invalidation contract, index rebuild contract and ten conformance specifications are maintained in [phase-3.5-forget-suppression-and-cursor-consumption.md](phase-3.5-forget-suppression-and-cursor-consumption.md).
```

### 05-memory-runtime/working-set-and-cache.md:144
```
The detailed contract and conformance cases are in [Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract](phase-3.5-forget-suppression-and-cursor-consumption.md). This addendum supersedes earlier provisional wording where inconsistent.
```

### 09-security-governance/principal-actor-and-authorization-contract.md:312
```
The Principal/Permission Mapping and Producer/Recipient inventory reconciliation are expanded in `phase-3.5-global-identity-forget-governance.md` §§2–3.
```

### 09-security-governance/principal-actor-and-authorization-contract.md:319
```
The end-to-end trust-chain sequence, Issuer Trust Registry requirements, Producer/Agent/Adapter/Runtime Session binding rules, complete authorization tuple, PermissionEpoch contract, revocation race matrix, Governance Decision Register and I36-T01..T20 test specifications are maintained in `phase-3.6-principal-trust-chain-authorization-revocation.md`.
```

### 09-security-governance/security-and-identity-overview.md:182
```
The authoritative Phase 3.5 I-owned mapping is recorded in `phase-3.5-global-identity-forget-governance.md`; decision approval status is tracked in `governance-decision-register.md`.
```

### 09-security-governance/global-forget-target-inventory-and-completion-evidence.md:316
```
The detailed I-owned identity and two-layer producer inventory mapping is normative candidate policy in `phase-3.5-global-identity-forget-governance.md` §§2–3. The following clarifications apply to this inventory contract:
```

### 09-security-governance/forget-retention-backup-and-erasure-policy.md:415
```
The authoritative I-owned Producer/Recipient Domain Inventory, ACK-to-Target mapping and Global Forget Completion Vector are consolidated in `phase-3.5-global-identity-forget-governance.md` §§3–5 and the detailed target contract.
```

### docs/en/05-memory-runtime/runtime-overview.md:54
```
**Phase 3.5 dependency review:** D/E/I/G/H/C/B owner-branch contracts are present and were re-read at the exact heads recorded in `phase-3.5-forget-suppression-and-cursor-consumption.md`（未提交，见 [GAP-01](../../governance/documentation-gaps.md)）. F's consumer semantics are DECIDED; callable cross-module schemas, Storage realization and runtime conformance remain OPEN. No wire schema is frozen by this document.
```

### docs/en/05-memory-runtime/runtime-overview.md:143
```
The normative F consumer matrix, retrieval-stage suppression matrix, cache/Working Set invalidation contract, index rebuild contract and ten conformance specifications are maintained in [phase-3.5-forget-suppression-and-cursor-consumption.md](../../governance/documentation-gaps.md).
```

### docs/zh-CN/05-memory-runtime/runtime-overview.md:59
```
- Phase 3.5 依赖审查：D/E/I/G/H/C/B Owner 分支契约已存在，并在 phase-3.5-forget-suppression-and-cursor-consumption.md 记录的精确 HEAD 上重新读取。F 的 Consumer Semantics 已 DECIDED；可调用的跨模块 Schema、Storage 实现和 Runtime Conformance 仍为 OPEN。本文不冻结 Wire Schema。
```

### docs/zh-CN/05-memory-runtime/runtime-overview.md:132
```

```

### docs/en/01-system-architecture/responsibility-matrix.md:37
```
- Source revision: 85548fcee05b28f8c2d54d4c0a8bf77840c8cdf3
```

### docs/en/01-system-architecture/system-boundaries.md:37
```
- Source revision: ad9ea5ce00e74dba89d325601677270a50f30926
```

### docs/en/00-governance/design-principles.md:56
```
- Source revision: 9792e189d63fbbc3694ab891fc4aeba5143b3b1c
```
# 额外约束

- `05-memory-runtime/retrieval-engine.md`、`working-set-and-cache.md` 在 `docs/en` / `docs/zh-CN` 下**没有对应句子**（已实测无匹配），所以只改 Canonical，不要造镜像内容。
- `09-security-governance/principal-actor-and-authorization-contract.md` 的同一句在 `docs/en`（L308、L315）与 `docs/zh-CN`（L315、L322）都存在；`docs/zh-CN` 那份正文实际是英文原文（已知语料缺陷），所以三份都要给块，内容保持同一句。
- 不要引入新链接目标；只允许链到 `docs/governance/documentation-gaps.md`（相对路径按各文件位置计算）或 AID-2026-107 证据文件。
- 若你判断某处不应改（例如它描述的是"候选策略"而不是"已生效规范"），就在该处给一个 `===FILE: <path>|SKIP===` 块并附一行理由。
