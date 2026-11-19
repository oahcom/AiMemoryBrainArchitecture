# FIX-2026-P1-GATE-ROOTS-001 — audit record

**Finding:** F-07 [P1] — `NORMATIVE_ROOTS` 未覆盖 `14-ai-development` (Issue #266 comment `7005657700`)
**Carrier:** this PR (branch `fix/f07-gate-normative-roots`)
**Date:** 2026-11-20

## 1. What the finding measured

`scripts/check_bilingual_docs.py` `NORMATIVE_ROOTS` covered 00–13 but not
`14-ai-development`, the directory carrying AI-STD-001, AI-EXEC-001/002,
AI-EXEC-ROLLOUT-001, AI-PROMPT-STD-001 and the AI-EXEC rulings. Measured
asymmetry: PR #272 changing `14-ai-development/ai-development-standard.md`
passed CI while PR #273 changing `docs/en/14-ai-development/AI-EXEC-002.md`
failed it. The gate's own policy documents were the only ungated normative
root.

## 2. Disposition of the deferral

F-07's registration named the Governance Owner as responsible and declined
coordinator action ("扩根目录属规范决策不是机械修复"). Under the user's
standing order (all owners may be one session; continue to convergence) the
Governance-Owner session made the decision in this work item. The decision is
not a silent constant edit: it is registered here with its design, tests and
limits.

## 3. Design decisions and why

1. **Root added:** `14-ai-development` joins `NORMATIVE_ROOTS`. Changes to its
   normative files now require the same `BILINGUAL-MANIFEST: COMPLETE` /
   `BILINGUAL-EXCEPTION: APPROVED` declaration as any other normative root.
2. **Pairing conventions made explicit.** The directory mixes three pairing
   layouts, and the old single convention (`docs/en/` + `docs/zh-CN/` mirrors)
   does not fit them:
   - side-by-side `X.md` ↔ `X.en.md` (zh primary, e.g. `evidence-tiering-policy.md`)
   - side-by-side `X.en.md` ↔ `X.zh-CN.md` (en primary, e.g. `status-migration-map.en.md`)
   - docs mirror `14-ai-development/X.md` (zh) ↔ `docs/en/14-ai-development/X.md`
     (en, e.g. `AI-EXEC-002.md`)
   The resolver accepts all three and demands both sides change together.
3. **Embedded bilingual sources registered per file** (F-07 exit-condition
   option 2): nine files verified to carry both languages in one source
   (CJK and English-word counts both substantial) are listed in
   `EMBEDDED_BILINGUAL_SOURCES`, so their exemption is documented rather than
   implied by the constant gap. Registration asserts single-file bilingual
   form only; semantic parity remains a reviewer responsibility.
4. **Operational-record subtrees are declaration-only.**
   `work-items/`, `prompts/`, `adr/` hold records and templates, not bilingual
   specifications; pairing is exempt there. This is why the in-flight INDEX
   registration work does not turn red.
5. **Pairing enforced for `.md` only** under `14-ai-development`; yaml/json/
   toml/proto are data or contracts, declaration-only.
6. **Unpaired root prose is now enforced debt.** `ai-run-003-…md`,
   `ubuntu-self-hosted-runner-bootstrap.md`, `continuous-owner-runtime-architecture.md`
   have no counterpart; changing them now fails unless paired or covered by a
   documented exception. That is the intended effect (new debt cannot land
   silently) and is listed in the manifest as known debt NOT closed here.
7. **F-08 narrowed, not closed.** For `docs/en/14-ai-development/*` the
   counterpart now resolves to the root zh source instead of a
   `docs/zh-CN/` mirror that does not exist — removing the #273-style false
   red on EN-mirror edits. The docs/zh-CN mirror gaps themselves remain
   tracked debt.

## 4. Evidence

- `scripts/governance/evidence/test_gate_normative_roots.py` — 14 tests:
  declared-but-unpaired must fail; partner-not-changed must fail; both side-by-side
  conventions pass; docs-mirror pair passes and lone mirror edit fails;
  embedded registration skips pairing and all registrations sit under a
  normative root; work-items/ prompts/ yaml exemptions asserted; 00-governance
  and legacy docs/en↔zh behaviour unchanged (regression).
- Full suite 86/86 OK (72 pre-existing + 14 new).
- Exact-Head local gate run on the PR head (compensation path; Actions
  billing interruption exception per RULING-06) — output sha256 recorded in
  the PR acceptance comment.

## 5. Limits

- Tooling enforcement only; no policy text changed. GOV-DOC-001 v1.2 adoption
  stays a separate item.
- F-07 stays OPEN in the finding registry until reviewer concurrence with this
  remediation; the exit condition's reproducible evidence is this PR's tests
  plus the gate runs.
- Translation debt (F-08, EN_ONLY migration register entries) is not closed.
- CI could not execute (billing); compensation + named exception as for
  #301–#303.
