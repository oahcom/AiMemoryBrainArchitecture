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
      last_verified_date: "2026-11-25"
      last_verification_note: "Every count in this prompt came from a measurement run on 2026-11-25 against main 1f5ba824, importing the real validator rather than re-implementing it, and was reproduced independently by a second session."
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

# AID-2026-079 — Make §5 item (2) satisfiable

## The defect, measured

Issue #1201 records it. In short: §5 item (2) of `14-ai-development/PR-GOVERNANCE-001.md`,
added by PR #1091 (`dd3b7662`), requires `implementing_ai_session` **as a top-level field**.
`scripts/governance/session_evidence/validate.py:1137-1145` rejects any top-level key named
in `MANIFEST_FIELDS` when a `session_evidence:` block is present, and
`implementing_ai_session` is one of them. A manifest therefore has to choose which of the
two rules to break.

Against the real validator, over the 54 manifests at `1f5ba824`:

| shape | count | clause §5(2) | gate |
| --- | --- | --- | --- |
| all three names top level, no block | 27 | satisfied | rejected |
| `sponsor` + `accountable_owner` top level, `implementing_ai_session` in the block | 20 | violated | accepted |
| `accountable_owner` only | 5 | violated | rejected |
| none of the three | 2 | violated | rejected |

**0 of 54 satisfy both.**

The clause is not merely unimplemented. It is unsatisfiable, and it is the newer of the two
rules. The gate's exclusion is deliberate and says why in its own comment: `New entries and
top-level legacy aliases must never become two independently mutable sources of truth.`

## What is being changed

One clause, in both languages, in one file.

**English, §5 item (2), line 144 — before:**

> The manifest must carry `sponsor`, `accountable_owner` and `implementing_ai_session` as
> top-level fields at the same time; `sponsor` and `accountable_owner` may identify the same
> principal, but …

**after:**

> The manifest must carry `sponsor`, `accountable_owner` and `implementing_ai_session` at the
> same time, each of them in exactly one place — top level, or the `session_evidence` entry
> that carries the session, and not both; `sponsor` and `accountable_owner` may identify the
> same principal, but …

**Chinese, line 148 — before:**

> manifest 必须同时在顶层携带 `sponsor`、`accountable_owner` 和 `implementing_ai_session` 三个字段；
> `sponsor` 与 `accountable_owner` 可以指向同一主体，但 …

**after:**

> manifest 必须同时携带 `sponsor`、`accountable_owner` 和 `implementing_ai_session` 三个字段，
> 每个字段只能出现于一处：顶层，或承载该会话的 `session_evidence` 条目内，不得两处并存；
> `sponsor` 与 `accountable_owner` 可以指向同一主体，但 …

Nothing else in the paragraph moves. Everything from `sponsor` and `accountable_owner` may
identify the same principal` to the closing non-exemption sentence is byte-identical.

## Why the location requirement is deleted rather than moved

Three reasons, in order of weight.

1. **It was never in the accepted source.** Issue #262 comment `7153428650` accepted five
   requirement gaps. It states no location for any field, and it contains zero occurrences
   of `assessor`, `assessed_version` and `evidence_baseline`. The `top-level` wording was
   added when this session composed §5 in PR #1091. It is not a requirement that was
   accepted and then implemented badly; it is a requirement this session invented.
2. **The alternative is worse.** Teaching the gate to accept a top-level alias alongside the
   block would give one field two mutable homes, contradict the stated design intent of the
   exclusion, and require `schema_change` authorization that no work item holds.
3. **Location was never the obligation.** The obligation is that three principals are named
   and that `accountable_owner` and `implementing_ai_session` are different principals.
   Nothing in that obligation depends on which YAML level the names sit at.

Replacing "top-level" with "exactly one place" is not a weakening. It states the invariant
the gate actually enforces, so the document and the checker can no longer disagree.

## The sweep this retires

The clause's defect was disclosed rather than hidden in three places, each of which now
describes a requirement that no longer exists. They are annotated as superseded and not
deleted, per the history-preservation principle in §4.1 Rule L1:

- `AID-2026-071/manifest.yaml` — the `Known deviation, stated rather than repaired` comment.
  After the correction that manifest satisfies the clause: `sponsor` and `accountable_owner`
  top level, `implementing_ai_session` inside `session_evidence[0]`, each in one place.
- `AID-2026-075/manifest.yaml` — the same comment, and criterion **C2**, which instructs the
  observer to read top-level fields and to report a nested-only `implementing_ai_session` as
  non-compliant. Left as written, C2 would have written the defect into code and reported 20
  of 54 conformant manifests as violations. C2 is corrected here; the work item's own scope
  is unchanged.
- `14-ai-development/work-items/INDEX.md` — the AID-2026-071 row's sentence that the
  manifest does not satisfy the clause's top-level field requirement.

`AID-2026-075/prompt-v1.md` also states the top-level requirement. It is a **recorded prompt
snapshot** with a pinned digest, so it is not edited. The manifest gains a
`prompt_supersession` entry naming the superseded passage, the way AID-2026-055 already does,
so a pin that no longer matches the requirement is visible from the manifest instead of from
a diff nobody reads.

## What this does not change

- **The gate.** No file under `scripts/`, `.github/` or `tests/` is touched. Exit codes,
  required contexts and branch protection are untouched.
- **The principal-identity requirement.** The same paragraph says textual difference between
  `accountable_owner` and `implementing_ai_session` is not evidence, and that principal
  identity decides. No principal registry exists anywhere in this repository, so nothing can
  settle that today. That is a second, independent defect in the same paragraph. One defect
  per change; it is registered separately and is not repaired here.
- **The approval block.** `decision_status`, `approved_version` and `modification_status` are
  not refreshed by the session that writes the change.
- **AID-2026-075's implementation.** Stage one still has no code. This work item removes the
  contradiction that blocked it and corrects the criterion; it does not start the work.

## Acceptance criteria

- **C1** — The location requirement is gone from both languages, and the invariant that
  replaces it is stated in both. Settled by reading the two paragraphs side by side and by
  `git diff -U0` showing exactly one changed line in each language.
- **C2** — No other sentence in §5 changes. Settled by `git diff` on the file showing two
  changed lines and no added or deleted line, and by the closing non-exemption sentence
  being byte-identical before and after in both languages.
- **C3** — The corrected clause is satisfiable, demonstrated rather than asserted. Settled by
  taking a block-form manifest that carries the three names in exactly one place each, and by
  `parse_manifest_session_entries` accepting it; and by the count of manifests that satisfy
  the corrected clause being reported with the command that produced it.
- **C4** — The corrected clause is not vacuous: it still rejects the manifests that name
  fewer than three principals. Settled by the same measurement reporting the 5 + 2 = 7
  manifests that name one or none, and naming their ids.
- **C5** — Nothing executable changes. Settled by `git diff --name-only` containing no path
  under `scripts/`, `.github/`, `tests/` or `crates/`.
- **C6** — Every statement the correction retires is annotated rather than deleted, and the
  annotation names the work item that retires it. Settled by the three files listed under
  *the sweep* each carrying a dated superseded clause, and by the recorded prompt snapshot
  being unmodified with a `prompt_supersession` entry in its manifest.
- **C7** — The review is at the exact Head and at the session level. Settled by the review
  naming the Head SHA it read and the session that performed it, and by not claiming an
  account-level approval; §9 requires an exact-Head governance review for changes to this
  standard, and §5's closing sentence says this paragraph is exemptible only by an exception
  record that names it, which none exists for.

## Out of scope

The principal-identity half of the same paragraph; the Session Evidence gate; the 34 manifests
that fail `parse_manifest_session_entries` for reasons unrelated to this clause; AID-2026-075's
observer; and every path not listed in the manifest's `scope`.
