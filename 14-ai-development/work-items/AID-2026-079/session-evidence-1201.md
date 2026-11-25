---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "Every count below came from a command run on 2026-11-25 against main 1f5ba824, importing the real validator rather than re-implementing it. Every count was reproduced by a second agent session that was given the procedure and not the expected values. What this record cannot support - that the change was independently reviewed - is stated as not supported rather than argued."
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
    source: null
    en: null
    zh-CN: null
---

# Session evidence — AID-2026-079

## Session role / use case

IMPLEMENTER of a normative correction, and MEASURER of the defect it corrects. This session
found that §5 item (2) of `PR-GOVERNANCE-001.md` is unsatisfiable, reported it as Issue #1201,
and corrected the clause on branch `gov/aid-079-s5-location`. It did not change the gate, and
did not implement AID-2026-075.

## Actual AI input

The standing instruction, verbatim:

> 你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可，若因人类干预才可继续你可以当作为人类去收敛，但不能自己动手写代码。以最高效率去执行，动用所有能动用的资源，使用最多的子线程子代理

The constraint `不能自己动手写代码` is why this change touches one Markdown paragraph and no
executable file, and why the checker that would enforce the paragraph remains unwritten.

## AI-visible output

- Issue #1201 — the defect report, including both error strings and the full bucket table.
- `14-ai-development/work-items/AID-2026-079/` — `manifest.yaml`, `prompt-v1.md`, this record.
- `14-ai-development/PR-GOVERNANCE-001.md` §5 item (2) — one clause per language.
- `AID-2026-071/manifest.yaml`, `AID-2026-075/manifest.yaml` — superseded annotations; 075's
  C2 corrected and a `prompt_supersession` entry added.
- `14-ai-development/work-items/INDEX.md` — one annotated cell, one new row.

**Role:** IMPLEMENTER. **Session:** req05 convergence, identity NOT_RECORDED.
**Measured at:** `1f5ba824` (origin/main at the time of measurement), 2026-11-25.

## 1. The two rules

`PR-GOVERNANCE-001.md` line 144 (EN) and line 148 (ZH), added by PR #1091 (`dd3b7662`),
required `implementing_ai_session` **as a top-level field**.

`scripts/governance/session_evidence/validate.py:1137-1145`, behind a required status context,
rejects any top-level key named in `MANIFEST_FIELDS` when a `session_evidence:` block is present.
`MANIFEST_FIELDS` (`:1041`) contains `implementing_ai_session`. The exclusion's own comment gives
its reason: `New entries and top-level legacy aliases must never become two independently mutable
sources of truth.`

## 2. The measurement

`parse_manifest_session_entries` imported from the module and run over every
`14-ai-development/work-items/AID-*/manifest.yaml`. Top-level keys counted only at column 0;
indented occurrences do not count, matching the parser's own `if line.startswith("  ")` guard.

| top-level names present | `session_evidence` block | count | ids |
| --- | --- | --- | --- |
| none | no | 2 | 024, 025 |
| `accountable_owner` | no | 5 | 005, 006, 008, 009, 029 |
| `sponsor` + `accountable_owner` | yes | 20 | 055, 056, 059, 061-078 |
| all three | no | 27 | 001-004, 011, 014, 023, 026, 030, 040-054, 057, 058, 060 |

**All three top level AND accepted by the parser: 0 of 54.**
Accepted by the parser: 20 of 54. Rejected: 34.

The 27 manifests that satisfy the clause are rejected by the gate. The 20 that pass the gate
violate the clause. There is no third option, because the guard fires on presence, not on value.

## 3. The two error strings

A manifest that satisfies the clause (AID-2026-001, all three names at top level, no block):

```
14-ai-development/work-items/AID-2026-001/manifest.yaml: incomplete legacy manifest; missing
executed_prompt_bytes, executed_prompt_provenance, executed_prompt_sha256,
executed_prompt_snapshot_file, session_evidence_ref, session_reference_status
```

— the legacy reader demands all seven `MANIFEST_FIELDS` (`:1106-1113`), and the clause asks for
three names, so satisfying the clause still leaves five fields short.

A manifest that passes the gate (AID-2026-055) with the one line the clause asks for inserted
after its `sponsor:` line:

```
14-ai-development/work-items/AID-2026-055/manifest.yaml: top-level legacy fields conflict with
session_evidence entries
```

## 4. The source the clause cites

Issue #262 comment `7153428650` — the comment §5 is derived from — counted verbatim:

```
assessor 0   assessed_version 0   evidence_baseline 0
implementing_ai_session 1   accountable_owner 1   sponsor 1
top-level 0  顶层 0
```

The one sentence carrying the three names says the registrations "carry" them and states no
location. The `top-level` requirement was therefore added by this session when composing §5,
not carried over from the accepted source.

## 5. The statements the correction retires

Four records described the deviation; all four are annotated rather than deleted, and each
annotation names AID-2026-079:

- `AID-2026-071/manifest.yaml` — the `Known deviation, stated rather than repaired` block.
- `AID-2026-075/manifest.yaml` — the same block, plus criterion **C2**, which instructed the
  observer to read top-level fields and to report a nested-only `implementing_ai_session` as
  non-compliant. Left as written it would have reported 20 conformant manifests as violations.
- `INDEX.md` — the AID-2026-071 row's sentence about the top-level field requirement.
- `AID-2026-075/prompt-v1.md` line 95 — **not edited**. Its digest pins bytes that exist, so
  the passage is named in the manifest's `prompt_supersession` instead of rewritten.

## Limits of this record

- **No independent review is recorded.** §9 requires an exact-Head governance review for
  changes to this standard, and §5's closing sentence says this paragraph is exemptible only
  by an exception record that names it. None exists. `review.status` stays `NOT_ASSIGNED`
  until a session that did not write the change reads that exact Head.
- The reproduction in §2 was performed by a second agent session given the procedure and not
  the expected values. It reproduced all four bucket counts, the 0-of-54 figure and both
  error strings. That is a reproducibility check, not an independent review: the session that
  wrote the change spawned it.
- **The second defect in the same paragraph is not repaired.** The clause also says principal
  identity, not string inequality, decides whether `accountable_owner` and
  `implementing_ai_session` differ. No principal registry exists in this repository — the term
  appears only in `01-system-architecture/data-flows.md`, its `docs/` mirrors, and
  `08-bmcp-protocol/validators/envelope_auth_validator.py` — so nothing can settle that
  requirement today. One defect per change; it is registered separately.
- **34 of 54 manifests still fail `parse_manifest_session_entries`.** Only the 27 that fail
  *because of this clause* are addressed here. The rest fail for reasons of their own, mostly
  an incomplete legacy field set predating the canonical format, and this work item does not
  change that count.
- **The clause is now satisfiable, not enforced.** Nothing reads §5 item (2) automatically.
  AID-2026-075 is the work item that would, and it is still unimplemented.
