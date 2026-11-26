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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Every count and every SHA in this record came from a command run in this session against the tree it names. What this record cannot support - that the correction was independently reviewed - is stated as not supported rather than argued."
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

# Session evidence — AID-2026-101

## Session role / use case

IMPLEMENTER of a registry correction, and MEASURER of the three defects it corrects. This
session did not write the work items whose records it repairs; it read their manifests, their
INDEX cells and the carriers those cells name, and found three that describe states the
carriers have already left. It opened Issue #1244 to hold the measurement, so that the
correction answers to an Issue of its own instead of borrowing the authority of the records it
edits.

It did not change any gate. The absence of a freshness gate for named-carrier cells is
recorded as finding F4 and deliberately left unbuilt: building it is code, and the standing
constraint below forbids that.

## Actual AI input

The standing instruction, verbatim:

> 你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可，若因人类干预才可继续你可以当作为人类去收敛，但不能自己动手写代码。以最高效率去执行，动用最多可动用的资源，使用最多的子线程子代理

The constraint `不能自己动手写代码` is why this change is four INDEX cells, three manifest
fields and one new work-item directory, with no Rust file, no checker and no workflow in it —
and why F4, the freshness gate the audit shows is missing, is described rather than written.

`prompt-v1.md` in this directory is the instruction this change was carried out against,
pinned at `89ac65f2d58e187451b7c0a98648d0dd4352e3dac79f521b8029b0432f7e94c1`, 4470 bytes,
computed from the committed bytes rather than composed.

`executed_prompt_provenance` is `NOT_VERIFIED`: the digest proves the committed file has not
changed since it was pinned, not that it is byte-for-byte what the session read.

**Read before writing:**

| input | what it settled |
|---|---|
| `14-ai-development/work-items/INDEX.md` line 39 and the `merge=union` note beside it | that a named-carrier Status cell must be refreshed when the carrier merges or closes, that a stale cell is a registry defect and not a historical record, and that no cell may be rewritten without an authorization naming it — hence the per-cell `prior_value` table in the manifest |
| `AID-2026-047/manifest.yaml` and `prompt-v1.md` | that the pinned digest is the digest of the file with `AID-2026-044` substituted for `AID-2026-047`; the substitution reproduces `1f547ad7…b236` exactly at the same 2185 bytes |
| `GET /repos/…/pulls/1155` and `pulls/1082`, `pulls/1057` | that #1155 and #1082 merged and that #1057 closed unmerged, with the merge commits and timestamps the cells now carry |
| `scripts/governance/session_evidence/validate.py` | that this manifest, being changed by this pull request, must use canonical `session_evidence` entries rather than the top-level legacy fields — the CI failure this record exists to answer |

## AI-visible output

- Issue #1244 — the defect report: the three stale cells, the false digest, and the commands
  behind each.
- `14-ai-development/work-items/AID-2026-101/` — `manifest.yaml` with `findings` F1–F5 and a
  `corrections:` table giving the prior value of every changed cell, `prompt-v1.md`, and this
  record.
- `14-ai-development/work-items/INDEX.md` — three refreshed rows, one new row for this work
  item, and the removal of a duplicate `AID-2026-080` row that the `merge=union` driver left
  behind on rebase.
- `AID-2026-047/manifest.yaml`, `AID-2026-072/manifest.yaml`, `AID-2026-076/manifest.yaml` —
  one corrected digest with the superseded value retained under `prompt_digest_correction`, and
  two `implementation` blocks changed from open to merged with the carrier history preserved.

**Role:** IMPLEMENTER. **Session:** owner-proxy, 2026-11-26. **Platform session identity:**
NOT_RECORDED.

## Limits of this record

- No independent review is recorded. The session that measured the defects made the
  correction, so an `APPROVE` from it would be self-review and is not claimed.
- The three cells were verified against the GitHub API on 2026-11-26. A later reader who wants
  to know whether they are *still* correct must re-fetch; this record is a measurement at a
  time, not a standing guarantee.
- The `AID-2026-080` duplicate row was resolved by choosing main's copy by hand, as the
  `merge=union` note requires. The dropped row is the superseded one; that it was superseded is
  the judgement, and the evidence for it is that it still carries the retaken pin `3e0fdfc7` /
  `11496` that round 3 of the 080 review refused.
