# FIX-2026-P1-MANIFEST-YAML-001 — INDEX registration record

This file records the execution of `authorization-manifest.yaml` `registration_deferral`,
which deferred the INDEX row for this work item and attached terms to the deferral. The
terms required the row to be written after the merge, from binding facts, with no pending
assertion at the moment of writing.

## Authorization

    authority: FIX-2026-P1-MANIFEST-YAML-001/authorization-manifest.yaml registration_deferral
               ("scope: its own authorization, one path")
    decision:  DEC-FIX-2026-P1-MANIFEST-YAML-001-GO-001 (self-issued coordinator decision)
    note:      self-issued; not an Owner approval and not an independent authorization.

The deferral stated responsible party, trigger, condition, scope, and that the deferral
expires with the registration. This record is that registration, executed on the trigger.

## Binding facts written into the row

| Fact | Value | How obtained |
|---|---|---|
| merge commit | `d6e3344f62c12adeba71c37462f94455fa5dbbd4` | `GET /pulls/298` after merge |
| merge time | `2026-11-19T19:57:21Z` | same |
| merge parents | `c262164e` (pre-merge main tip) + `bd95cd92` (exact Head) | merge commit read-back |
| merged file blobs | `5de2c3b4` AID-2026-002 manifest, `7caabbe5` T1 manifest, `8251dc6c` INDEX-REFRESH authorization manifest, `8b1ed770` T4-FU3 authorization manifest, `543c5682` this work item's authorization manifest, `a9e0ce71` audit record | `git ls-tree` on the merge commit |
| untouched INDEX blob at merge | `2928ff9b` | same read-back (INDEX.md was not in this PR's change set) |
| review chain | R1 (conv `6aff537c-eed8-83e8-9ae0-8581a34575f8`) DISPOSITION PASS | comment `7020524461` |
| exception | RULING-06, Actions billing interruption, `UNATTRIBUTED`, exact head `bd95cd92` | comment `7020524937` |
| acceptance | §2.1 four-line record | comment `7020525425` |
| main-move re-read | main advanced `87fd195a` → `c262164e` before merge; gate re-run with identical output sha256 `83bb9719…c329` | comment `7020572653` |
| post-merge verification | blob parity 6/6, parents and main tip read back | comment `7020599750` |

## What the row does not claim

The row closes scan findings M-1..M-4 only. F-P1 (the dangling
`ai-development-standard.en.md` reference) remains a self-declared `MISSING_IN_REPO /
PENDING_DECISION` state; tier-mapping `UNKNOWN=376` awaits human confirmation per
bilingual-tiering policy §4.3; Tier 1 translation debt remains registered as `EN_ONLY`
in the bilingual governance migration register. None of these is asserted closed here.
No policy status change: `AI-DOC-EVIDENCE-TIERING` and `bilingual-tiering-policy` remain
`PROPOSED`.
