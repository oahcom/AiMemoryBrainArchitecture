# FIX-2026-P1-MANIFEST-YAML-001 — Audit record

Full translation/manifest scan and the parseability remediation it produced.
Scan date: 2026-11-19 (UTC) / 2026-11-20 (+08). Operator: coordinator session 13-20-04.

## 1. Scan scope and tools

Three scan surfaces over the repository at `87fd195a` (main tip after PR #296):

1. **Tier mapping consistency** — `scripts/governance/bilingual/check-bilingual-tiering.sh`
   against `14-ai-development/work-items/FIX-2026-P1-T3/tier-mapping-proposal.yaml`.
2. **Bilingual pairing / sync** — pair enumeration over the normative roots and
   `14-ai-development/`, plus `scripts/governance/bilingual/check-bilingual-sync.sh`
   per pair.
3. **Manifest strictness** — all `manifest.yaml` and `authorization-manifest.yaml`
   under `14-ai-development/work-items/`, parsed with a duplicate-key-rejecting
   SafeLoader; required fields (`title`, `status` on work-item manifests); referenced
   repo paths resolved against the working tree.

## 2. Findings and dispositions

### M-1 … M-4 — YAML parseability defects (fixed in this PR)

| ID | File | Defect | Fix |
|---|---|---|---|
| M-1 | `AID-2026-002/manifest.yaml` | unquoted scalar with `": "` inside (`bilingual_status`, "translation commits: AI-EXEC-001 …") — parse error "mapping values are not allowed here" | value wrapped in double quotes; parsed scalar byte-identical |
| M-2 | `FIX-2026-P1-T1/manifest.yaml` | unquoted scalar with `": "` inside (`prior_failed_reason`, "required BILINGUAL-MANIFEST: COMPLETE declaration") | same |
| M-3 | `FIX-2026-P1-INDEX-REFRESH-001/authorization-manifest.yaml` | Markdown prose in a `.yaml` file; parse error "expected '<document start>', but found '<block mapping start>'" | converted to parseable YAML; prose moved verbatim into block scalars; the two already YAML-shaped fragments (decision, write allowlist) became real mappings |
| M-4 | `FIX-2026-P1-T4-FU3/authorization-manifest.yaml` | same | same |

Series convention was established by `FIX-2026-P1-T4`, `-FU1`, `-FU2` manifests
(structured YAML, parseable); M-3 and M-4 were the two deviants.

### Preservation check for the M-3/M-4 conversions (mechanical, not asserted)

Method: every non-blank, non-comment line of the old file must appear in the new
file's parsed content (values flattened and matched). Result:

- **M-3: 0 deltas.** Every old content line appears in the new file.
- **M-4: 4 deltas, all structural, values preserved verbatim:**
  1. `- scripts/governance/evidence/test_template_example_executable.py   (new file)`
     → `{path: scripts/governance/evidence/test_template_example_executable.py, note: new file}`
  2. `- 14-ai-development/work-items/FIX-2026-P1-T4-FU3/authorization-manifest.yaml`
     → `{path: …, note: this manifest}`
  3. `independent review: separate session, same \`oahcom\` identity.`
     → `independent_review: separate session, same \`oahcom\` identity.` (key style)
  4. `platform-axis independence: NOT MET, not claimed.`
     → `platform_axis_independence: NOT MET, not claimed.` (key style)

No fact is dropped, softened or upgraded by the conversion. One pre-existing
internal inconsistency is preserved as-is rather than silently corrected: section 6
records "full suite: 72 tests" while section 9 says "the 70/70 above"; the record
was merged with that text and this PR does not rewrite history.

### F-P1 — dangling path (NOT a defect; recorded so the negative is evidenced)

`FIX-2026-P1-T3/authorization-manifest.yaml` references
`14-ai-development/ai-development-standard.en.md`, which does not exist. The same
manifest states at its own line 186: *"ai-development-standard.en.md is MISSING_IN_REPO /
PENDING_DECISION."* The absence is self-declared and tracked inside the referencing
carrier; rewriting the reference would falsify that record. **Not touched.**

### T-1 — tier mapping UNKNOWN count (tracked; not auto-fixable)

`check-bilingual-tiering.sh` exits 2 and reports
`SUMMARY TIER1=26 TIER2=10 TIER3=219 UNKNOWN=376`.
TIER1/TIER2/TIER3 counts match the policy's declared baseline exactly.
UNKNOWN distribution: `docs/` 174, `14-ai-development/` 99, `13-engineering-decisions/`
58, `prompts/` 36, `00-governance/` 8, `08-bmcp-protocol/` 1.
Bilingual-tiering policy section 4.3: *"未知分类必须标记为 UNKNOWN 并等待人工确认。工具必须
输出文件路径和待确认状态，不得将其默认归入 Tier 2 或 Tier 3，不得自动修复分类，也不得将
UNKNOWN 报告为 PASS。"* The scan therefore reports and stops. Classification of the 376
awaits human confirmation (dev-baseline: OUT-OF-SCOPE, tracked, review-by 2026-12-02
conventions apply to the policy adoption as a whole).

### T-2 — Tier 1 bilingual completeness (tracked migration debt; not a new defect)

The 26 Tier 1 entries contain exactly one explicit file pair
(`04-memory-compiler/phase-1-event-store-contract.md` + `-zh-CN.md`); several files are
embedded-bilingual in one source; the rest are single-language. This state is already
carried by `00-governance/bilingual-governance-migration-register.md`
(`Original_Language_State: EN_ONLY`, 28 in the summary counts, 349 EN_ONLY row mentions)
and the tier-mapping file is itself `status: PROPOSAL`. Policy tiering obligations bind
after formal adoption. No file is created or translated by this PR: translation is a
semantic act that requires review, and the policy forbids treating unconfirmed states as
PASS.

### T-3 — pair-sync metadata (observation only)

`check-bilingual-sync.sh` requires `source-revision`/`source-version` and `bilingual-pair`
reciprocal metadata. Three existing pairs fail this check
(`phase-1-event-store-contract` ↔ `-zh-CN`; `evidence-tiering-policy` ↔ `.en`;
`bilingual-tiering-policy` ↔ `.en`). Neither `bilingual-documentation-policy.md` nor
`bilingual-tiering-policy.md` mandates this metadata for legacy pairs; the tool defines a
convention that pre-existing pairs have not adopted. Recorded as an observation for the
policy-adoption package, not fixed here.

## 3. Verification of the fix

- Strict parse (duplicate-key-rejecting SafeLoader): **15/15 manifest files** now parse
  (was 11/15). The only remaining scan line is F-P1, classified above.
- Full regression: **72/72 OK** (`python -m unittest discover -s scripts/governance/evidence -p "test_*.py"`).
- Preservation check: 0 undeclared deltas (section 2).

## 4. Limits

- Scan tooling used for this audit lives in the session workspace and is not committed
  under `scripts/` (outside this authorization's allowlist; the repo's own
  `check-bilingual-tiering.sh` / `check-bilingual-sync.sh` are committed and were invoked
  as-is).
- No workflow wiring; the evidence-tiering checker and the bilingual tiering script still
  run only when someone runs them.
- No policy status change. `AI-DOC-EVIDENCE-TIERING` v1.0 and `bilingual-tiering-policy`
  remain `PROPOSED`.
- CI cannot execute (Actions billing interruption); local compensation is registered on
  the PR per enforcement v1.2 section 1 with a RULING-06 exception.
- Platform-axis independence NOT MET (same `oahcom` identity); not claimed.
