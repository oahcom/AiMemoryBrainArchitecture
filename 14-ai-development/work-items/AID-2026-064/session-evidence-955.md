---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
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
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "Every SHA, line count and delta in the output section was measured in this session against the blobs in this worktree at 350be84b; none is carried over from Issue #955 or from the lead's re-measurement at 1a17d89e. The one judgement that is not machine-derived — that the English Appendix B bullet was never revised for F-006 — is supported by the diff of 4c38ae25 shown below."
    usage_status: Active
    modification_status: Active-Modified
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

# Session role

IMPLEMENTER. Re-verify, and correct, the bilingual registration record of
`AID-2026-004` for Issue #955. Read-only against the six documents: no translation was
written and no source document was edited. The only writes are the AID-2026-004
manifest, this record, and this work item's own manifest and prompt file.

The session was executed by an AI agent under the team role `a955`. This record is
written by that agent about its own session, so it is a self-report, not a third-party
attestation.

# Actual AI input

Two inputs governed the session and both are quoted.

**1. The task assignment**, reproduced in full in `prompt-v1.md`. It fixes the ruling
the session must apply and is reproduced rather than summarised because the ruling is
the thing being executed:

> - **Claimed:** `bilingual_status: COMPLETE` is an *activity assertion* — it asserts
>   the two sides are aligned *now*. The files were edited after registration, so the
>   field can no longer be read unconditionally as "aligned", and the manifest neither
>   re-verified, nor downgraded, nor recorded a pending review.
> - **Not claimed:** that the three pairs are currently semantically mismatched. Six
>   drifted SHAs prove only that the *registered version* is stale, not that the
>   *content* diverged.
>
> Do not conflate those two. The fix direction is re-verification, not re-translation.

**2. Issue #955's own text**, read from `GET /repos/oahcom/AiMemoryBrainArchitecture/issues/955`
during the session. Its proposed repair steps 1–4 are the shape this record follows;
step 5 scopes out any new automated drift check, and that scope was respected.

The session's language directive (respond in Simplified Chinese) is a standing
instruction rather than a task input; the repository artefacts are written in the
documents' own language, which is English for this record.

# AI-visible output

The output is a re-measurement, three per-pair verdicts, one corrected manifest and this
record. No document content was produced, edited or retranslated. Every figure below was
computed in this session; the two tables that could have been copied from Issue #955 or
from the lead's re-measurement were re-derived instead, and both disagree with the
earlier measurements because `main` moved.

## 1. Registered versus current blob, all six files

Measured at `origin/main = 350be84b547d040d3a689ffe24fb75cca6bc10c7`. "Registered" is
`AID-2026-004/manifest.yaml` as it stood at that commit; "current" is `git rev-parse
HEAD:<path>` in this worktree.

| Document | Side | Registered | Current | Match |
|---|---|---|---|---|
| AI-EXEC-001 | source | `372a290359f9e9de2bd81d7901beb2f084e6e3a4` | `58af59af266b81109269156ea667df1a15edfb7b` | no |
| AI-EXEC-001 | translation | `c93db6a480bbe8f5ebbc8f3e56b570a920a20ad7` | `b809d770f93f5a2244988f04f68ad913b29f5e76` | no |
| AI-EXEC-002 | source | `ebb7f1ee9a084864c454711d271499cfbf8d386f` | `0a42d90391c166878031ecd2478ca9bb87c2f4a0` | no |
| AI-EXEC-002 | translation | `96aab56ce856484e24ad99ec6944a4c45ceb763b` | `0dd2f9ff7c5ad1f74c153fa57df9a92548644aba` | no |
| AI-EXEC-ROLLOUT-001 | source | `14082151e2839e966349498138b9001d01de9bed` | `f9560a0b3f8e86e5abc8b17a5f84f1d592b66d24` | no |
| AI-EXEC-ROLLOUT-001 | translation | `87e4314d1df9bbff2321eb1053078bb5f7148d8d` | `eb9a34edceb75fe64308e9d966dc11924aa34037` | no |

6/6 drift, which is the issue's claim and not new information. It says nothing about
content.

## 2. Per-pair line deltas, measured with `git diff --numstat <registered-blob> <current-blob>`

| Pair | Source +/− | Translation +/− | Net difference |
|---|---|---|---|
| AI-EXEC-001 | +3 / −3 | +1 / −1 | source +2, translation +2 |
| AI-EXEC-002 | +63 / −15 | +62 / −14 | source +1, translation +1 |
| AI-EXEC-ROLLOUT-001 | +47 / −3 | +46 / −2 | source +1, translation +1 |

These differ from Issue #955's table (+3/+64/+47 versus +1/+63/+46) because the issue
measured at `8e489ec1`. They also differ from the lead's at `1a17d89e`. Both are
superseded by the values above.

## 3. Per-pair verdict, and what was compared

**AI-EXEC-002 — ALIGNED.** The source diff has thirteen hunks: 44 lines of
`document_metadata` front matter, Version 1.1→1.2 and Status →`v1.2 PENDING ADOPTION`,
the Tracking link, the Translation status header, the English summary rewritten for
F-006, a `.`-prefixed link repair at §1, the §3 heading plus the new *Structural
authority* and *All-risk-level baseline obligation (F-02)* blockquotes, the 12-item
sentence reworded to "12 content obligations", three tiered-emphasis bullets reworded
from 结构 to 内容义务, the RULING-01 blockquote rewritten, §5 red line 4 restated
against PR-GOVERNANCE-001 §5 as amended 2026-11-24, and the Closeout INDEX link. The
translation diff carries a counterpart for every one of them, in the same order. The
one-line difference is the Translation status header, which exists only in the Chinese
source and was rewritten there; the English header carries a different line that did
not change. Structure also agrees: 15 headings and 5 table rows on both sides.

**AI-EXEC-ROLLOUT-001 — ALIGNED.** Source hunks: the same 44-line front matter, the
Tracking link, the Translation status header, and the L5 red-line restatement
("independence is a property of the reviewing session, not of the GitHub account",
PR-GOVERNANCE §5 as amended 2026-11-24). The translation carries the front matter, the
Tracking link and the L5 restatement. The +1 difference is again the Chinese-only
Translation status header. Structure agrees: 18 headings and 47 table rows on both
sides.

**AI-EXEC-001 — DIVERGED.** Source hunks: three one-line revisions — the Translation
status header (STALE → COMPLETE), the English summary rewritten for F-006, and the
Appendix B bullet. The translation carries exactly one of them, the summary. The
Appendix B bullet in `docs/en/14-ai-development/AI-EXEC-001.md` is **byte-identical to
the registered blob**:

| Side | Appendix B bullet, as it stands |
|---|---|
| Source | `提示词结构统一为七章节、15 项内容义务按 AI-PROMPT-STD-001 §4 映射（#269 后锚点，F-006 修订）` |
| Translation | `prompts are unified to 15 items` |

This is a source revision the translation does not carry. It was introduced by
`4c38ae25` (PR #273, the F-006 fix), whose message claims "F-01 include AI-EXEC-001
zh+en anchor wording in the change set": that commit changed the Chinese file by two
lines and the English file by one. The second Chinese line is the Appendix B bullet;
the missing English counterpart is the defect.

The narrower claim that survives is that F-006 *information* is not absent from the
English document — its summary paragraph carries "seven-sections prompt structure with
15 mapped content obligations (post-#269 anchor, F-006)". What is absent is the
revision of the paragraph itself, so the English document now states the pre-F-006
framing in Appendix B and the post-F-006 framing in its summary, in the same file. That
is a translation defect, and it is not a content gap that a reader could not recover;
it is recorded as DIVERGED because the field asserts alignment and this paragraph is
not aligned.

## 4. Status chosen, and the ceiling

`scripts/check_bilingual_docs.py`, `scripts/check_document_management.py`,
`scripts/check_traceability.py`, `scripts/ci/check_repository_hygiene.py` and
`14-ai-development/work-items/manifest-schema-registry.yaml` were each read or grepped
for `bilingual_status`. **No code path reads the field and none constrains it to an
enumeration.** The registry file governs only `record_type` exclusion from the manifest
consistency gate. The three observed values in the tree (`AID-2026-002`,
`AID-2026-003`, `AID-2026-004`) are all narrative strings beginning `COMPLETE`, so the
precedent is "token, then an em-dash elaboration", not a closed set. There was no gate
ceiling to hit.

`AID-2026-004` therefore records `DIVERGED`, with per-pair verdicts beside the original
registration.

## 5. What this record does not contain

- **No retranslation.** The English Appendix B bullet was not edited. Fixing it is a
  separate change under AI-EXEC-001, and the session was instructed not to write
  translations.
- **No claim that AI-EXEC-002 or ROLLOUT-001 are semantically equivalent to their
  sources.** A hunk-by-hunk correspondence proves coverage of the paragraphs that
  changed, not that any sentence is a good translation.
- **No claim about translation quality anywhere.** The one defect recorded is that a
  revision is missing, not that a rendering is clumsy.
- **No prompt-frozen-before-execution claim.** `executed_prompt_provenance` is
  `NOT_VERIFIED`: the digest pins the bytes of `prompt-v1.md`, and that file was written
  after the session from the assignment as received.
- **No session transcript identifier.** `session_reference_status` is `NOT_RECORDED`.
- **The `Session Evidence` gate verdict for this PR is not reported here.** It depends on
  the PR, which does not exist at the moment this file is written; the PR body carries
  the verdict read after the run.
