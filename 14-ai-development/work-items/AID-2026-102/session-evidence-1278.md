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
      last_verification_note: "Every digest, byte count and blob enumeration in this record came from a command run in this session against the tree it names. What this record cannot support - that the correction was independently reviewed - is stated as not supported rather than argued."
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

# Session evidence — AID-2026-102

## Session role / use case

IMPLEMENTER of a one-field correction, and MEASURER of the defect it corrects. This session
continued the registry correction AID-2026-101 began, re-ran its digest audit on the tree that
work item merged into, and found a second instance of the same defect class with a different
shape. It did not write AID-2026-092 and did not change anything that work item produced except
the two fields that assert a measurement.

It did not change any gate. The absence of a checker over the top-level `prompt_sha256` field is
restated as finding F2 and left unbuilt, because building it is code.

## Actual AI input

The standing instruction, verbatim:

> 你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可，若因人类干预才可继续你可以当作为人类去收敛，但不能自己动手写代码。以最高效率去执行，动用最多可动用的资源，使用最多的子线程子代理

The constraint `不能自己动手写代码` is why this change is two YAML scalars, one added field and
one INDEX cell, with no checker in it — and why F2, the gate the defect shows is missing, is
described rather than written.

`prompt-v1.md` in this directory is the instruction this change was carried out against, pinned
at `df3c53282d858ecc7302ba86b4fb419bf6a31c8030d30cee256b64840b4e4e7a`, 4470 bytes, computed
from the committed bytes rather than composed.

`executed_prompt_provenance` is `NOT_VERIFIED`: the digest proves the committed file has not
changed since it was pinned, not that it is byte-for-byte what the session read.

**Read before writing:**

| input | what it settled |
|---|---|
| `AID-2026-092/manifest.yaml` at `d5107f68` | the declared pair `2455 / 9be8aebf`, and that `prompt_id` still reads `AID-2026-083-PROMPT` |
| `git rev-list --all` over both prompt paths | that exactly four blobs have ever existed at those paths (7689, 3772, 2915, 4137 bytes) and none is 2455, so the declared value matched no version rather than an earlier one |
| `cac933cb` — the commit that created the manifest | that the false pair was present from creation, in the same commit where the pinned file is already 3772 bytes |
| `AID-2026-101/manifest.yaml` and `session-evidence-1244.md` | the shape to follow: itemised `corrections` with `prior_value`, canonical `session_evidence` entries, and an `implementation` block that stays `NOT_STARTED` until the merge exists |

## AI-visible output

- Issue #1278 — the defect report, including the blob enumeration and why this is not the
  AID-2026-047 shape.
- `14-ai-development/work-items/AID-2026-102/` — `manifest.yaml` with findings F1–F3 and a
  `corrections:` table, `prompt-v1.md`, and this record.
- `14-ai-development/work-items/AID-2026-092/manifest.yaml` — `prompt_sha256` and
  `prompt_bytes` corrected, `prompt_digest_correction` added.
- `14-ai-development/work-items/INDEX.md` — the AID-2026-092 prompt cell refreshed, plus one
  new row for this work item.

**Role:** IMPLEMENTER. **Session:** owner-proxy, 2026-11-26. **Platform session identity:**
NOT_RECORDED.

## Limits of this record

- No independent review is recorded. The session that measured the defect made the correction,
  so an `APPROVE` from it would be self-review and is not claimed.
- The correction says the old value matched no version. That is a claim about every ref that
  existed when the enumeration ran, not a claim about refs that never will; a later reader
  wanting to know whether it is still true must re-run the enumeration, which is quoted in full
  in the manifest.
- `prompt_id` is deliberately left reading `AID-2026-083-PROMPT`. The work item was renumbered
  083 to 092 at merge and the pinned bytes were not rewritten to match, which is correct: the
  snapshot is the executed input. Only the digest was wrong.
