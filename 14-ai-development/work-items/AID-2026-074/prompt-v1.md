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
      last_verification_note: "Every manifest quote, line number and count in this file was re-read on 2026-11-25 from the committed tree at 30c7277e with py + a duplicate-key-rejecting SafeLoader; the four failing files were each parsed before and after repair and the scalar values compared byte-for-byte. The byte size and digest were measured from the file after this front matter was added."
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

# AID-2026-074 — PARSE-PROMPT (v1)

## Goal

Close the detection gap that let four work-item manifests sit unparseable while every gate
reported green.

## What is measured

At `main = 30c7277e`, four of the 49 `14-ai-development/work-items/AID-*/manifest.yaml` files
do not survive a strict YAML parse:

| File | Defect class | Parser verdict |
|---|---|---|
| `AID-2026-023` | unquoted scalar containing `": "` (`implementing_ai_session`, line 18) | `mapping values are not allowed here` |
| `AID-2026-029` | the same key twice (`related_prs: [356]` then `related_prs: []`, lines 8-9) | duplicate key; the default loader keeps `[]` and drops PR 356 |
| `AID-2026-040` | two unquoted scalars containing `": "` (`sponsor`, `accountable_owner`, lines 15-16) | `mapping values are not allowed here` |
| `AID-2026-055` | unescaped `"` inside a double-quoted list item (lines 160-161) | `expected <block end>, but found '<scalar>'` |

The default loader is the dangerous case, not the loud one. `AID-2026-029` parses "successfully"
under `yaml.safe_load` and silently discards `related_prs: [356]`, which is the only record of the
PR that carried its implementation. A record that reads clean and loses a field is worse than one
that refuses to load.

## Why no gate caught it

`scripts/ci/check_repository_hygiene.py` reads manifests as **text** and extracts scalars with
`_top_level_manifest_scalar`, a regex over unindented lines. It never constructs a YAML document.
Its `manifests=49 ... violations=0` line is therefore a statement about a text scan, not about
parseability.

`scripts/governance/status_migration/check_status_gates.py` is the only checker in the tree that
calls `yaml.safe_load` on manifest content, and no workflow invokes it. `test_status_migration`
exercises it against fixtures the test writes itself, not against the repository's manifests.

This is the second occurrence. `FIX-2026-P1-MANIFEST-YAML-001` repaired four instances of the same
class on 2026-11-19 (`M-1`..`M-4`) and recorded in its own audit record: *"No workflow wiring; the
evidence-tiering checker and the bilingual tiering script still run only when someone runs them."*
Nothing was wired, so the class recurred. The repair alone was not the fix.

## Acceptance criteria

- **AC1** — A check in `scripts/ci/` parses every committed work-item manifest with a
  duplicate-key-rejecting loader and fails on any parse error, naming the path and the parser
  message. Settled by running it against a tree with one intentionally broken manifest and seeing
  exit 1 with that path named.
- **AC2** — The same check fails on a duplicate key even when the default loader would accept the
  document. Settled by `AID-2026-029`'s exact shape (`related_prs` twice) in a fixture: default
  `yaml.safe_load` returns a document, the check exits 1.
- **AC3** — The check is wired into a workflow that runs on every PR, not only by hand. Settled by
  the workflow file naming the check in a `run:` step and by the check appearing in the run log.
- **AC4** — The four manifests named above parse under that check at the commit this lands.
  Settled by the check exiting 0 over the real tree.
- **AC5** — The check states what it does not verify (field semantics, cross-file consistency) so
  a green result is not read as "the manifests are correct", only "they parse".

## What this does not authorise

No change to `check_repository_hygiene.py`'s existing rules; no change to any manifest's content
beyond the four repairs if they have not already landed; no policy status change.

## Provenance

Registered in the session that measured it. The four repairs were applied in the same session that
found the gap, which is the wrong order for a clean audit trail and is recorded rather than hidden:
the repair is why the check can be tested against a real green tree, and the check is why the next
occurrence will not need a human to notice it.
