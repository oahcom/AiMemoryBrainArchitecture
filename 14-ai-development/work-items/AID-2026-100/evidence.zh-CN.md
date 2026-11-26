---
id: AID-2026-100
id_status: PROVISIONAL
title: "#1037 证据采集——完整克隆只读结果"
date: 2026-11-26
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
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "数据来自完整克隆上的本地只读执行，由用户提供；不是 CI。交接材料未提供 census 脚本精确调用命令和原始输出附件。"
    usage_status: Active
    modification_status: Unchanged
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
    source: "14-ai-development/work-items/AID-2026-100/evidence.md"
    en: "14-ai-development/work-items/AID-2026-100/evidence.en.md"
    zh-CN: null
---

# AID-2026-100 — #1037 证据记录（简体中文）

**署名：** user-authorized operator (delegated by account owner)  
**日期：** 2026-11-26  
**目的：** 关闭 Issue #1037 的两项证据类 BLOCKED；#1037 Issue 本身仍保持 OPEN。


## Evidence provenance and execution environment

The following measurements were supplied as results of read-only local execution in a **complete clone**, not from CI. The earlier partial-clone worktree failure describes only the previous VM attempt and is superseded for these two evidence items by this complete-clone capture.

- Platform: Windows
- Python: 3.12.3
- Environment: `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`
- Clone: complete history; `git cat-file -t` returned `commit` for `c6b7d987`, `cb4b36d0`, and `dc826e4e`
- Worktrees: detached at `c6b7d987b959c42af5072932963dae9ed55721e4` and `dc826e4eae381d78a9fc4b1fcbb2cbc783ed2706`
- Checker command, identical in both worktrees: `python scripts/check_document_management.py`
- Scan mode: full-tree scan; no `--require-changed`

The exact invocation of the separate read-only census script was not included in the supplied capture record; it is therefore marked `NOT_PROVIDED` below rather than reconstructed.

## Evidence A — full-tree checker capture

Command (both snapshots): `python scripts/check_document_management.py`

| Item | Baseline `c6b7d987` | Fix `dc826e4e` |
|---|---:|---:|
| Exit code | `2` | `2` |
| stdout bytes | 5443 | 5943 |
| stdout SHA-256 | `FCDDF7DE725A3676CD9AFAAA37EC897E8C6F4EBACBB49FF79814F591AC75CA8B` | `347292A4A6BD768A43DDE42FBD6DA8FAE01E1974DB3355C269B5922A1031F8DA` |
| stderr bytes | 230 | 230 |
| stderr SHA-256 | `EE34929E76B0FC03EE3842D206A7E9EC7695AB51CF87E34035287DC0A43CA92A` | `D4161D94B7EF4939374EAA80157553531176292BCE37BE528B9593CC77DCD926` |
| stdout lines | 50 | 55 |

**stdout is not byte-identical**: 5443 vs 5943 bytes and different SHA-256 values. Both exit codes are `2`.

The stderr semantic lines, as supplied (the only difference is the numbers):

- Baseline: `INCOMPLETE: no rule violations in 278 classified documents, but 484 governed documents are still unclassified`
- Fix: `INCOMPLETE: no rule violations in 293 classified documents, but 469 governed documents are still unclassified`

Interpretation: both snapshots report **no rule violations**. Exit code `2` means `INCOMPLETE` (the full-tree classification is incomplete), not failure and not PASS.

The full raw stdout/stderr byte streams were measured for the byte counts and digests above, but separate downloadable raw-output files were not included in the supplied handoff. The recorded hashes are the supplied measurements; this document does not claim to attach the streams themselves.

## Evidence B — stdout line-difference attribution

Supplied `Compare-Object` summary: **8 base-only lines and 13 fix-only lines**.

Base-only lines:

```text
GOV-DOC-002: 762 governed documents, 278 classified, 484 unclassified
::notice::advisory (non-blocking): 121 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)
::notice::advisory (non-blocking):   139 distinct prose status value(s), 144 occurrence(s):
::notice::advisory (non-blocking):   (+129 more distinct value(s) not shown)
  01-system-architecture: 0/7 classified
  02-domain-model: 0/12 classified
  docs: 81/283 classified
  adoption backlog: ... ... (+479)
```

Fix-only lines:

```text
GOV-DOC-002: 762 governed documents, 293 classified, 469 unclassified
::notice::advisory (non-blocking): 117 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)
::notice::advisory (non-blocking):   135 distinct prose status value(s), 140 occurrence(s):
::notice::advisory (non-blocking):   (+125 more distinct value(s) not shown)
  01-system-architecture: 4/7 classified
  02-domain-model: 1/12 classified
  docs: 91/283 classified
  adoption backlog: ... ... (+464)
  authority: architecture/logical-system-component-map -> 01-system-architecture/component-map.md
  authority: architecture/subsystem-responsibility-matrix -> 01-system-architecture/responsibility-matrix.md
  authority: architecture/system-boundaries -> 01-system-architecture/system-boundaries.md
  authority: architecture/system-overview-guide -> 01-system-architecture/system-overview.md
  authority: domain-model/phase-1-domain-model-freeze -> 02-domain-model/phase-1-domain-model-freeze.md
```

Attribution recorded in the supplied result:

- Five new authority bindings appear in the fix output.
- Classified documents: 278 → 293 (**+15**): `01-system-architecture` +4, `02-domain-model` +1, `docs` +10.
- Unclassified documents: 484 → 469 (**−15**).
- Advisory counts: body-status documents 121 → 117; distinct prose status values 139 → 135; occurrences 144 → 140.

Thus the outputs are **not equivalent**; the reported differences are attributed to the classification and authority-binding changes above. The abbreviated adoption-backlog lines are preserved exactly as supplied (including ellipses); this evidence record does not expand omitted entries.

## Evidence C — fix-commit frontmatter census

Snapshot: fix commit `dc826e4eae381d78a9fc4b1fcbb2cbc783ed2706`.

Execution: read-only script traversing all `*.md` files and parsing YAML frontmatter. Exact script invocation: `NOT_PROVIDED` in the supplied capture record. Exit code: `0`.

Report JSON SHA-256: `DD6A4CC1440A331EE984518C6D6306A7C233B0A4324DDBE9035EF95D309F15CC`.

| Metric | Count |
|---|---:|
| `total_md` | 1020 |
| `with_frontmatter` | 294 |
| `no_frontmatter` | 726 |
| `malformed_frontmatter` | 0 |

`document_metadata.lifecycle.modification_status` distribution:

| Value | Count |
|---|---:|
| `Unchanged` | 159 |
| `Modified` | 117 |
| `Pending-Reapproval` | 15 |
| `Active-Modified` | 2 |
| `None` | 1 |

`document_metadata.authority.normative_status` distribution:

| Value | Count |
|---|---:|
| `Informative` | 241 |
| `Normative` | 52 |
| `None` | 1 |

**Pending-Reapproval = 15**, comprising **12 Normative** and **3 Informative**:

```text
Normative   00-governance/architecture-invariants.md
Normative   00-governance/design-principles.md
Normative   14-ai-development/adr/OWNER-DECISION-FACT-CLAIM-001.md
Normative   14-ai-development/adr/OWNER-RULING-ATTESTOR-ISSUER-SEPARATION-031.md
Informative 14-ai-development/governance-register/GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036.md
Normative   14-ai-development/PR-GOVERNANCE-001.md
Normative   14-ai-development/work-items/I-OWNER-DECISION-AUTHORIZATION-DECISION-001.md
Normative   docs/en/00-governance/architecture-invariants.md
Normative   docs/en/00-governance/design-principles.md
Normative   docs/en/14-ai-development/adr/OWNER-DECISION-FACT-CLAIM-001.md
Informative docs/en/14-ai-development/governance-register/GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036.md
Normative   docs/zh-CN/00-governance/architecture-invariants.md
Normative   docs/zh-CN/00-governance/design-principles.md
Normative   docs/zh-CN/14-ai-development/adr/OWNER-DECISION-FACT-CLAIM-001.md
Informative docs/zh-CN/14-ai-development/governance-register/GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036.md
```

Aggregation: five documents each have three mirrors (`architecture-invariants`, `design-principles`, `OWNER-DECISION-FACT-CLAIM-001`, and `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`) plus two root-only documents (`PR-GOVERNANCE-001` and `I-OWNER-DECISION-AUTHORIZATION-DECISION-001`) = 15. The three `Informative` entries are the root/EN/ZH-CN mirrors of the same governance-register record, consistent with the earlier Issue comment.

The report digest is recorded above. The complete JSON inventory itself was not attached in the supplied handoff, so no file attachment/path is claimed.

## Evidence D — incremental-mode comparison (supplementary; not an equivalence proof)

Command: `python scripts/check_document_management.py --require-changed c6b7d987b959c42af5072932963dae9ed55721e4`.

| Snapshot | Exit | stdout | stderr |
|---|---:|---|---|
| `c6b7d987` | `3` | 0 bytes; SHA-256 `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` | `NOT_APPLICABLE: --require-changed resolved to zero changed or untracked paths; no incremental verification was performed` |
| `dc826e4e` | `0` | 7986 bytes; SHA-256 `130A0B10EDBD11D0EFBA5D98955F399E3AFB93F3BE9A57C86770BE893B97FAAE` | 5261 bytes; SHA-256 `4E7C397CD0900538EAC8E286D0FBFA75CCC8948A36997A20A1AFD9F258F28253` |

On the baseline, `--require-changed <baseline itself>` necessarily resolves to zero changed paths. Incremental mode therefore cannot serve as the baseline/fix equivalence comparison; the full-tree scan in Evidence A is the valid comparison. The baseline stderr SHA-256 corresponds to 122 bytes of raw content, whereas fix stderr is 5261 bytes and includes Windows GBK decoding noise; these stderr streams are not comparable. Evidence D is supplementary only.

## Resolution and scope

- `byte-for-byte output equivalence`: **RESOLVED as an evidence question**. The evidence does **not** show byte equality; it establishes that stdout differs, both exit codes are 2, both report no rule violations, and the supplied line-difference report attributes the observed changes. No claim of “output equivalent” is made.
- `fresh metadata recount`: **RESOLVED** by the fix-commit read-only census in Evidence C.
- Provenance: complete-clone local read-only execution, **not CI**.
- These two evidence items for **#1037 are closed**.
- **Issue #1037 as a whole remains OPEN**. Owner acceptance and any other outstanding acceptance work are not completed by this evidence capture.
- No runtime, validator, or workflow semantics were changed. This PR remains Draft and is not to be merged as part of this task.

