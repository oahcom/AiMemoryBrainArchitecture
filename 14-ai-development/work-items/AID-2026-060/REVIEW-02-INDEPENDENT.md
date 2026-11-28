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
      last_verification_note: "This record states the state round 2 actually examined, origin/main at 21279d3b, and not the state after the two non-blocking corrections it produced. It reproduces the defect directly with the real gate_ratchet.py rather than trusting the manifest's description of it. Round 2 returned APPROVE with no blocking item."
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

# REVIEW-02-INDEPENDENT — AID-2026-060

## Provenance (written before any finding)

| Field | Value |
|---|---|
| Reviewed artefact | `14-ai-development/work-items/AID-2026-060/manifest.yaml` |
| Worktree | `C:\Users\Administrator\AppData\Local\Temp\opencode\wt-rv060` (detached) |
| Reviewed commit | `21279d3b` |
| Reviewer | this session (`r2c`); **not** the author |
| Author | registering session of AID-2026-060, and the author of its round-1 corrections |
| Independence level | **session-level only.** Under PR-GOVERNANCE-001 §5 as amended by `2eb4e352` (#935), two sessions of the same GitHub identity are not independent in the identity sense. This review is a second session, not a second party. **Disclosed, not claimed as independence.** |
| Relationship to prior round | This is round 2. Round 1 (`REVIEW-01-INDEPENDENT.md`) raised findings B1-B4/F4-F7; the corrections reviewed here are the author's. A passing second session neither confirms nor elevates them. |
| Tools | `py` (PyYAML 6.0.3) with a duplicate-key-detecting loader; `scripts/ci/gate_ratchet.py` at the reviewed commit, unmodified |
| Files modified by this review | none in the worktree. Helper scripts and this report live under `scratch-untracked/` |
| Verdict | **APPROVE** — see §5. No blocking item. Three material/informational items for the author to correct before dispatch. |

---

## 1. Parse (duplicate-key-detecting loader)

Loader: `yaml.SafeLoader` subclass whose mapping constructor raises on a repeated key. A duplicate would abort the parse; it did not.

| Metric | Value |
|---|---|
| Byte count | **22 987** (single-byte throughout: chars == bytes, no BOM, no CRLF) |
| Top-level keys | **38** (listed: `work_item_id, title, class, risk, risk_rationale, security_scope, authorization, scope, prompt_supersession, status, sponsor, accountable_owner, implementing_ai_session, repository, base_branch, base_commit_sha, tracking_issue, created_at, updated_at, prompt_id, prompt_version, prompt_file, prompt_status, prompt_sha256, prompt_bytes, prompt_provenance_tier, prompt_provenance_note, owner_decisions, deliverables, acceptance_criteria, withdrawn_acceptance_criteria, independent_reviewer, integration_reviewer, review, acceptance, implementation, errata, findings`) |
| Mapping keys, total (recursive) | **157** |
| Duplicate keys | **none** |
| `acceptance_criteria` ids (8) | `AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8` |
| `withdrawn_acceptance_criteria` ids (1) | `AC1-ORIGINAL` |
| Id appearing in both lists | **none** (intersection empty) |
| Other counts | `deliverables`: 5, `findings`: 8, `owner_decisions`: 1 (OD-26), `errata`: 1 |

The `AC1-ORIGINAL` suffix does what the manifest says it does: it cannot be mistaken for `AC1`, and no consumer that reads `acceptance_criteria[*].id` will see a withdrawn id. Clean.

---

## 2. Reproduction of the claimed defect (real `scripts/ci/gate_ratchet.py`)

Flags, from the argparse block at lines 81-90: `--baseline` (required, `Path`), `--command` (required, str), `--format` (`schema|paths`, default `schema`). Invoked as `py scripts/ci/gate_ratchet.py --baseline <b> --format paths --command "<cmd>"`, cwd = worktree root, script unmodified, no shim.

Two supporting checks first, because a "PASS" is only evidence if the wrapped command actually ran:

- Control: `--command "py -c \"print('brand/new/item.md')\""` → `baseline=77 current=1 regressions=1`, exit 1. The `--command` path executes and its stdout is parsed. (An earlier attempt of mine passed a `/c/Users/...` path that `cmd.exe` could not resolve; it produced an empty parse that would have been mistaken for the defect. Discarded — it is not in the record below, and it is exactly the confound this gate exists to prevent.)

### Case (a) — empty baseline, command prints nothing, exits 9

```
$ py scripts/ci/gate_ratchet.py --baseline ../scratch-untracked/empty_baseline.txt \
      --format paths --command "py -c \"import sys; sys.exit(9)\""
ratchet: ../scratch-untracked/empty_baseline.txt
ratchet: baseline=0 current=0 regressions=0 fixed=0
ratchet: PASS - failure set matches the baseline exactly.
EXIT=0
```

### Case (b) — real 77-entry baseline, command prints exactly those 77 lines, exits 9

Baseline measured: 77 raw lines, 77 entries after blank/`#` filtering, 77 unique. Command: `py -c "import sys; sys.stdout.write(open('scripts/ci/baselines/bilingual-docs.txt',encoding='utf-8').read()); sys.exit(9)"` — it demonstrably ran, because its output arrived.

```
$ py scripts/ci/gate_ratchet.py --baseline scripts/ci/baselines/bilingual-docs.txt \
      --format paths --command "py -c \"...print 77 lines...; sys.exit(9)\""
ratchet: scripts/ci/baselines/bilingual-docs.txt
ratchet: baseline=77 current=77 regressions=0 fixed=0
ratchet: PASS - failure set matches the baseline exactly.
EXIT=0
```

**Both cases behave exactly as the manifest claims.** `regressions=0 fixed=0`, `PASS`, exit 0, in both, with exit status 9 in both. The premise of AC1 — "Measured at b80e5a40: empty baseline plus a command exiting 9 gives `regressions=0 fixed=0 PASS exit 0`, so this criterion fails today" — is **confirmed**, and the stronger claim (non-empty baseline, status 9, PASS) is confirmed too. No correction to the premise is needed.

Case (a) is also the strongest available demonstration that `proc.returncode` is not merely ignored on one branch: nothing else in the script's inputs differs between a status-0 and a status-9 run.

---

## 3. `returncode` occurrences, and the verbatim quotation

`returncode` in `scripts/ci/gate_ratchet.py`: **0 hits, in any casing, in any line.** Confirmed twice — a line-by-line scan of all 132 lines, and the manifest's own claim that the only reference to the completed process is `current = normalize(proc.stdout.splitlines(), args.format)`, which is at **line 105 exactly**, as findings[F1] states. AC1's diagnosis is accurate, including the line number.

(The sibling `scripts/ci/*.py` do read it: `check_branch_freshness.py:76,82,84`, `check_line_endings.py:57`, `check_repository_hygiene.py:180`. The omission is in this file alone, not a repository-wide convention — so AC5's claim that this script is the odd one out is the right framing.)

The quoted comment, at lines 102-104:

```
    # Items are printed to stdout. stderr carries interpreter warnings and
    # tracebacks, which are not items; a crash yields zero items and is caught
    # below as a stale baseline (fail-closed), never as a pass.
```

The manifest's quotation in deliverables[3] — "a crash yields zero items and is caught below as a stale baseline (fail-closed), never as a pass" — is **verbatim**. Only the source's line wrapping differs; no word is added, dropped, or reordered. **Not blocking.**

And the substance of the claim about that comment is correct, not just its wording: with a non-empty baseline a crash does produce `fixed=N` and exit 1 (fail-closed, and case (b)-adjacent behaviour confirms it); with an empty baseline the same crash produces `fixed=0` and PASS (case (a)). The comment's guarantee is conditional on baseline non-emptiness, which it does not say. AC7 is a real requirement.

---

## 4. 060 AC4 against 058 AC3 — the conflict is real, and the withdrawal is sound

**060 AC4 (quoted):** "An empty baseline with a zero status and an empty parsed set exits 0 and prints PASS. This is required, not tolerated: AID-2026-058's AC4 brings `scripts/ci/baselines/traceability.txt` to zero entries in the same commit that lands its inputs, and its AC3 requires this script over that baseline to exit 0. Rejecting empty baselines makes 058 unimplementable…"

**058 AC3 (quoted):** "`gate_ratchet.py --baseline scripts/ci/baselines/traceability.txt --format paths --command 'python scripts/check_traceability.py'` exits 0 with regressions=0, **and** a deliberately injected failure is caught: with one path temporarily removed from INDEX.md, the same command must exit non-zero with regressions=1, and the path restored afterwards. fixed=0 is NOT required."

Can both hold? **Yes, and they are the same requirement seen from two sides.** 058 AC3 needs a 0-entry baseline to yield exit 0; 060 AC4 supplies exactly that and nothing more. 058 AC3's injected-failure clause needs `regressions=1` on a 1-item set against a 0-entry baseline, which is AC1's ordinary regression path and needs no change from 060. There is no state in which AC4 forbids something AC3 requires, or vice versa.

The conflict was with the **withdrawn** criterion, not with AC4. 060's `AC1-ORIGINAL` ("Empty baseline, command exits 0: non-zero exit, message names the baseline path, no PASS on stdout") and 058 AC3 ("exits 0 with regressions=0" over a 0-entry baseline) are mutually exclusive — one demands non-zero on that input, the other demands zero. With OD-26 ordering 060 first, the literal original would have stranded a DISPATCHED 058. findings[F4] states this accurately and the withdrawal is the correct disposition: four independent confirmations (this session's parse, the two runs in §2, the 058 AC3 text, and 058 AC4's removal-only emptying of the baseline).

**The conflict is therefore not false.** No -1 applies. One precision note for the record: the manifest's shorthand "AID-2026-058's AC4 … and its AC3" elides that the operative conflict is with 058's `prompt_supersession`-amended AC3 requiring `fixed=0` as *originally* written — 058 has since dropped `fixed=0` ("fixed=0 is NOT required"). The conflict survives that amendment, because the *exit 0* half of 058 AC3 is load-bearing and unchanged. A reader who checked only 058's first version would reach the same conclusion; a reader who checked only the current version might think the amendment dissolved the conflict. It does not. Worth one clause in F4; not a defect.

---

## 5. Findings

### No blocking item

The three things that would have been blocking each came out clean: the quotation is verbatim (§3), the defect reproduces exactly as stated in both configurations, and the 058 conflict is real rather than manufactured to justify a withdrawal (§4). Duplicate keys: none. AC/withdrawn id collision: none.

### N1 — material — a cross-reference in a blocking finding's resolution describes the wrong criterion

`findings[F7].resolution` ends: "Pinned by AC5, which uses a **non-empty baseline and a status of 9**."

`acceptance_criteria[AC5]` says: "A non-empty baseline with **status 1** and a parsed set equal to the baseline exits 0 and prints PASS."

AC5 is the live-caller pin (status 1, must pass); it cannot also be the status-9 pin, and a test written from AC5 will not fail if the status-9 guard is removed. The status-9-with-non-empty-baseline case *is* required — by `AC1` ("whatever the parsed set and whatever the baseline contains. Tested with both an empty and a non-empty baseline") — so the requirement is present and the citation is wrong. Since F7 is a blocking finding whose resolution is the evidence that it is closed, this is the one place in the manifest where a reader is told a check exists that the text does not ask for. Correct the sentence to "Pinned by AC1's non-empty-baseline case; AC5 pins the opposite direction (status 1 must pass)."

### N2 — material — AC4 accepts the exact indistinguishability `risk_rationale` calls fatal

`risk_rationale` (line 5): "A gate that cannot tell 'never ran' from 'ran and found nothing' converts every baseline it guards into a decoration."

`AC4`: an empty baseline, status 0, empty set → PASS. That is precisely a state in which "never ran" and "ran and found nothing" are indistinguishable: a command that silently does nothing and returns 0 satisfies AC4 identically to a correct checker over a clean repository. AC1-AC3 close the non-zero and the status/set-disagreement cases, but not this one.

This is defensible — deliverable 4 and AC7 require "naming the input class that remains undetectable, if any survives the change", and 058 needs the empty-baseline pass — but the manifest should not leave the impression that the sentence in `risk_rationale` is fully discharged. State the residual class in AC7's implementation note: *status 0 with an empty set over an empty baseline is indistinguishable from a no-op, and is accepted by design because 058 requires it.* Otherwise the next reader tests the work item against its own rationale and finds it short.

### N3 — informational — claims I verified outside the four assigned steps, and one I did not

Verified while checking AC5's premise: `.github/workflows/gates.yml` lines **161-164** are exactly `python3 scripts/ci/gate_ratchet.py \ --baseline scripts/ci/baselines/bilingual-docs.txt \ --format paths \ --command "python3 scripts/check_bilingual_docs_full.py"`. The citation is correct, the caller is the only one in `gates.yml`, and `scripts/ci/baselines/` at `21279d3b` contains **only** `bilingual-docs.txt` — `traceability.txt` does not yet exist, consistent with 058 `files_to_create` and with AC8(b)'s "once AID-2026-058 lands".

Not verified, and not claimed either way: `prompt_sha256` / `prompt_bytes: 7797` against `prompt-v1.md`; the `ba293506` and `b80e5a40` measurements attributed to other sessions; `gates.yml` check name "Bilingual docs coverage (ratchet)" as rendered by GitHub. None affects this verdict.

---

## VERDICT: APPROVE

Blocking items: none. The manifest's three load-bearing factual claims — the verbatim comment, the two-case reproduction, the 058 conflict — are each correct as written, and the withdrawn criterion was withdrawn for a real reason rather than a convenient one. That is the failure mode this round was sent to look for, and it is absent.

Two corrections requested before dispatch (neither blocks): **N1**, the F7→AC5 cross-reference that describes the wrong criterion (line: `findings[F7].resolution`, last sentence; the false sentence is "Pinned by AC5, which uses a non-empty baseline and a status of 9" — contradicted by AC5's own text, "A non-empty baseline with status 1"); and **N2**, the residual indistinguishability that AC4 accepts and `risk_rationale` still reads as closed.

Independence: session-level only, same GitHub identity — see the provenance table. This APPROVE is a second session's check, not a second party's.
