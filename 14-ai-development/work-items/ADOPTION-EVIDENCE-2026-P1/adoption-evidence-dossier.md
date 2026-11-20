# Adoption Evidence Dossier — AI-DOC-EVIDENCE-TIERING and AI-DOC-BILINGUAL-TIERING

**Prepared:** 2026-11-20
**Prepared by:** coordinator session (operational work, NOT an authorization)
**Status:** EVIDENCE ASSEMBLED, ADOPTION NOT GRANTED. Both policies remain `PROPOSED`.
**Covers:** `AI-DOC-EVIDENCE-TIERING` v1.0 and `AI-DOC-BILINGUAL-TIERING`.

This dossier exists so that a future governance authority can adopt either policy
without re-deriving the facts. It states what is ready, what is missing, and what
must not be claimed. It is not an adoption record; the blank form lives in
`adoption-record-template.md` beside this file.

---

## 1. What the policies themselves require for adoption

Read verbatim from each policy's own effectiveness clause — these are the policies'
own terms, not this dossier's invention.

| | `AI-DOC-EVIDENCE-TIERING` §8 | `AI-DOC-BILINGUAL-TIERING` §8 |
|---|---|---|
| Approver | required | required |
| Effective date | required | required |
| Versioned instrument | checker version **and** its commit SHA | adopted per-file classification inventory version **and** its SHA |
| Explicit non-adoption clause | yes — "passing independent review and merging an implementation does not constitute adoption" | yes — remains PROPOSED until formally adopted |
| Automation obligation on adoption | none stated beyond the checker | "All automation MUST comply … especially human confirmation for UNKNOWN, the non-downgradability of Tier 1, and the architecture-semantic bilingual gate" |

Both texts also require that any change to their definitions go through a formal
change record (evidence §8 item 1) and that they be maintained bilingually
(evidence §7; bilingual policy carries the same obligation by its own Tier 1
nature).

## 2. Facts as of baseline `723446225af5daa863e6641106a669e3ad8ba11b`

Measured by reading the tree at that commit. Re-measure at signing time; do not
copy these into an adoption record.

### 2.1 Instruments named by the policies

| Instrument | Path | Blob at baseline |
|---|---|---|
| Evidence policy (ZH) | `14-ai-development/evidence-tiering-policy.md` | `bbc1d54640f652672d84db8b2b8502a5486d3e74` |
| Evidence policy (EN) | `14-ai-development/evidence-tiering-policy.en.md` | `a6c784d5bc97ca8df555966ebf60d7bec22495b7` |
| Evidence checker | `scripts/governance/evidence/check-evidence-tiering.py` | `93f3f0d5fa2ff53502e2c2065e8f4f2aecb3f583` |
| Evidence checker tests | `scripts/governance/evidence/test_evidence_tiering.py` | `0107fc19e777713c4d4185033e6cb897f168f9a3` |
| Bilingual policy (ZH) | `14-ai-development/bilingual-tiering-policy.md` | `be0c058a25074d78feeec09b3d09506b9f198f6b` |
| Bilingual policy (EN) | `14-ai-development/bilingual-tiering-policy.en.md` | `c81287caa12e2faaff45c2ef77b33f7ee8f979a5` |
| Bilingual tiering checker | `scripts/governance/bilingual/check-bilingual-tiering.sh` | `a131dadcc2e933165cc80a2e32b28dd066e8ee3a` |
| Bilingual sync checker | `scripts/governance/bilingual/check-bilingual-sync.sh` | `613e25e917156c162636a17debdfa8682c62eb8c` |

Both policies are paired ZH/EN. Neither pair is registered as a Tier 1 pair with
a confirmed tier — that is exactly what remains open (section 3.2).

### 2.2 Readiness by required field

| Required field | Evidence policy | Bilingual policy |
|---|---|---|
| `approver` | **MISSING** — no approver exists in the repository; all of `sponsor` / `accountable_owner` / `acceptance_authority` are `NOT_ASSIGNED` | **MISSING** — same |
| `effective_date` | **MISSING** — cannot exist before an approver signs | **MISSING** — same |
| Versioned instrument | **READY** — checker path and its blob SHA are measured above; the script carries no version constant, so the blob SHA is the version | **NOT READY** — what §8 requires is an **adopted** per-file inventory plus its SHA. Proposal data exists and is not that: `tier-mapping-proposal.yaml` (63 entries) and `tier-confirmation-proposal.yaml` (377 rows, every row `confirmation_record: PENDING`), both self-declared PROPOSAL in their own headers. The data is present; the approval is not. |
| Change-record discipline | stated in policy, no change yet | stated in policy, no change yet |
| Bilingual maintenance | ZH/EN pair present at baseline | ZH/EN pair present at baseline |

## 3. What is genuinely blocking, and what is not

### 3.1 Blockers that cannot be resolved inside this repository

1. **No approver.** Both policies name "the project governance authority" as the
   adopter. No such authority is present in the repository, and the coordinator
   session is explicitly not one. R-D8-01 ruled that the coordinator may not
   self-register any role appointment, and that the only acceptable label for
   its mandate is `HUMAN-PERSPECTIVE-OPERATIONAL-AUTHORIZATION` — which "must
   not be cited as acceptance_authority appointment, sponsor/accountable_owner
   appointment, formal policy adoption, completion of human confirmation, or
   authorization for anything the baseline excludes."
2. **No effective date**, which follows from the absence of an approver.

### 3.2 Blockers that are repository work but need a human decision

1. **No approved per-file classification inventory.** The bilingual policy's
   adoption record requires one. What exists instead:
   - `tier-mapping-proposal.yaml` — 63 per-file entries at baseline `f0a3747b`,
     status PROPOSAL.
   - `tier-confirmation-proposal.yaml` — 377 rows covering the four UNKNOWN
     buckets at baseline `9546f78d`, every row `confirmation_record: PENDING`.
   - The policy's own counts (Tier 1 = 26, Tier 2 = 10, Tier 3 = 27, directory
     rules 530) were measured at `f0a3747b`. The tree has drifted since; the
     policy's own section 1 says actual counts govern and later references must
     carry the file-list commit SHA.
   A human confirmation pass over the 377 rows, plus the 24 `PAIR-DIVERGENT`
   rows, is what turns the proposal into the inventory the adoption record
   needs. Until then the bilingual policy cannot be adopted as written: its §8
   names an **adopted** per-file classification inventory and its SHA, and what
   exists is proposal data, not an adopted inventory. The two are different
   things — the data is present, the approval is not.
2. **Roles.** `acceptance_authority` / `sponsor` / `accountable_owner` are
   `NOT_ASSIGNED` repository-wide. This is a true governance state, tracked as
   F-ROLE-ASSIGN, and must not be substituted by the implementing Owner.

### 3.3 Things that look like blockers and are not

1. **Merging the policies.** Evidence policy §8 item 2 says so in as many words:
   passing independent review and merging an implementation does not constitute
   adoption.
2. **The checkers being unwired.** A checker that nothing calls is not an
   obstacle to adoption; it is an obstacle to enforcement, which is a different
   question. Adoption would in fact be what authorizes wiring them.
3. **CI billing.** Unrelated to adoption. It affects evidence form for PR gates,
   not whether a policy is adopted.

## 4. What this dossier claims, and what it must not be cited for

**Claims:** the field list in section 1 is read from the policy texts; the blob
SHAs in section 2.1 were measured at baseline `72344622`; the readiness table in
2.2 reflects that state; section 3 separates blockers by who can clear them.

**Must not be cited for:**
- that either policy has been adopted, is in force, or is effective;
- that any UNKNOWN or PENDING classification has been confirmed;
- that an approver exists, has been identified, or has been delegated;
- that the per-file inventory required by the bilingual policy exists;
- that any role appointment has occurred.

## 5. How a future adoption would actually proceed

1. A governance authority with real appointment power selects one policy.
2. Re-measure the policy blob and the named instrument **at that moment** — do
   not reuse section 2.1.
3. For the bilingual policy: first complete human confirmation over the 377 rows
   and the 24 divergent pairs, producing the approved per-file inventory and its
   SHA. Without that, §8 cannot be satisfied.
4. Fill `adoption-record-template.md`, complete Part C, sign it.
5. Only then change the policy's `Status:` line from `PROPOSED` to `ADOPTED`,
   and only then wire the checkers as binding.

Until step 4 happens, the correct status of both policies is `PROPOSED`, and the
correct treatment of everything depending on them is BLOCKED / NEEDS_CONFIRMATION.
