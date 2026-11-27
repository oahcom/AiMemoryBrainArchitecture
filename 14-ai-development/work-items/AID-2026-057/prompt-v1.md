---
document_metadata:
  domain: ai-development
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "Every count in section 1 was produced by running the gate's own is_allowed_new_path() predicate over git ls-tree -r --name-only at main a23e6cc, then bucketing the result with an explicit classifier whose buckets were reconciled against the 113 total. The first draft of this prompt did not close: four paths fell outside every bucket. They were read, assigned, and the totals recomputed. No figure is carried over from the round-21 report, whose 144/11.3% predates #893 admitting the 31 AID manifests."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative

  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-057 — classify the 113 paths the admission gate would refuse, and admit none of them by extension

**Work item:** `AID-2026-057`
**Class / risk:** `GATE/POLICY` / `R2`
**Status:** `DISPATCHED`
**Measured at:** `main = a23e6cc`

---

## 1. What was measured, and how

The gate's own predicate was imported and run over the tracked tree — not a shell glob, not an
extension guess:

```
tracked total: 1286
refused if added as a new path: 113   (8.8%)
```

By extension, every count measured:

| Extension | Count |
|---|---|
| `.json` | 69 |
| `.yaml` | 16 |
| `.toml` | 12 |
| `.txt` | 8 |
| `.log` | 1 |
| `.lock` | 1 |
| `.csv` | 1 |
| `.cfg` | 1 |
| `.tla` | 1 |
| `.jsonl` | 1 |
| `.sha256` | 1 |
| no extension | 1 |

The round-21 figure was 144 / 11.3%. The difference is not a measurement error: #893 added a rule
admitting `14-ai-development/work-items/AID-*/manifest.yaml`, and 31 such manifests already exist.
144 − 31 = 113. That arithmetic is the proof that the gate re-run after #893 is the number to use,
and that the older figure must not be quoted forward.

---

## 2. What this work item is not

**It is not a request to admit 113 files.** The Owner's round-22 ruling is explicit:

> No global suffix additions based on this inventory. No blanket admission of `.json`, `.yaml`,
> `.toml`, `.txt`, or the remaining eight extensions. Preserve the fixed allowlist and
> reject-by-default behavior. Classify each candidate by its intended repository role and the
> exact future path shape it should permit.

The 113 is a candidate inventory. A file existing in the base tree does not prove that a new file
of the same shape should be admissible. Some of the 113 should stay permanently inadmissible.

**It is not part of AID-2026-055 or #893.** The Owner required a separate work item.

---

## 3. The classification

Decided by opening representative files, not by reading the extension. Categories are the Owner's:
**A** repeatable shape deserving a narrow rule, **B** exact singleton deserving an exact-path rule,
**C** historical/obsolete, stays inadmissible as new, **D** unclear, needs an Owner decision.

### A — repeatable shapes (74 paths, 6 groups)

| # | Shape (POSIX glob, whole-path anchored) | N | What the files are |
|---|---|---|---|
| A1 | `08-bmcp-protocol/schemas/*.schema.json` | 32 | Versioned JSON Schema documents. Versions run 1.0.0 → 1.2.17; a new protocol version adds files. |
| A2 | `08-bmcp-protocol/tests/conformance/**/*.json` except `package.json` / `package-lock.json` | 16 | Conformance fixtures and vector files: 10 under `provider_outcome/fixtures`, 4 under `recovery_cutoff/fixtures`, and 2 at the family root (`i_crypto_profile_vector.json`, `wire_interop_vectors.json`) — both are test vectors with the same role as the fixtures, verified by reading them. |
| A4 | `crates/*/Cargo.toml` | 12 | Rust crate manifests, one per crate. A new crate necessarily adds one. |
| A5 | `14-ai-development/governance-register/evidence/*.json` | 9 | Machine-written evidence captures from API reads (attribution, direct-commit filesets, issue closures, merge-gate evidence). Same role as the raw API evidence cited in #875's record. |
| A6 | `crates/*/VERIFICATION.txt` | 3 | Per-crate verification records (Clippy baselines, source pins). One per crate, same lifetime as the crate. |
| A8 | `scripts/bilingual-baseline.txt`, `scripts/ci/baselines/*.txt` | 2 | **Ratchet baselines consumed by the gates themselves** (`check_bilingual_docs.py:170`, `gate_ratchet.py`). Adding a baseline is how a ratchet is raised. |

### B — exact singletons (4 paths, 4 groups)

| # | Exact path | N | What it is |
|---|---|---|---|
| B9 | `.governance/GOV-DOC-001-inheritance.json` | 1 | Machine-read declaration consumed by `tests/test_policy_inheritance.py:30`. Stable identity, one file, never duplicated. |
| B10 | `00-governance/architecture-document-metadata.schema.yaml` | 1 | **The metadata schema itself.** `00-governance/architecture-document-management-policy.md:54`: "parsed by the gate's own parser and compared against the gate's constants in both directions by T19". Also one of the 21 `EMBEDDED_BILINGUAL_SOURCES`. |
| B11 | `00-governance/document-scope-registry.yaml` | 1 | Consumed by `scripts/check_document_management.py:84` as `SCOPE_REGISTRY`. Single fixed path. |
| B12 | `14-ai-development/remote-worker-inventory.yaml` | 1 | Live inventory of remote workers; referenced by the runbook pair and touched by ordinary commits. Single fixed path. |

### C — historical / obsolete, stays inadmissible as new (19 paths, 5 groups)

| # | Shape | N | Why it stays refused |
|---|---|---|---|
| C13 | `14-ai-development/work-items/FIX-2026-P1-T3/tier-*.yaml` | 2 | Machine-generated **proposals** marked `PROPOSAL_PENDING_HUMAN_CONFIRMATION`, generated by `generate-tier-proposal.py` against a pinned `baseline_commit`. Regenerable, subordinate to their own baseline. |
| C14 | `*.json` under `benchmarks/`, `reviews/`, `crates/*/fixtures/` | 9 | Benchmark outputs, review-pilot corpus, crate test fixtures. Ad hoc, one-shot, tied to a specific measurement that has already happened. |
| C15 | `Cargo.lock` | 1 | Generated by cargo. Adding one deliberately would be wrong. |
| C16 | `VERIFICATION.txt` (root) | 1 | The Clippy-baseline record from 2026-11-21, superseded by the per-crate versions. |
| C18 | `recovery/PR-RECOVERY-002-INVENTORY.csv`, `*.sha256`, `*.cfg`, `*.tla`, `*.jsonl`, `*.log` | 6 | One-shot inventory, hash manifest, model-checker inputs, corpus, test log. |

### D — needs an Owner decision (16 paths, 5 groups)

| # | Shape | N | The question, and the two answers |
|---|---|---|---|
| D3 | `14-ai-development/work-items/*/{manifest,authorization-manifest}.yaml` where the ID is **not** `AID-YYYY-NNN` | 11 | **Q:** are the legacy ID families (`FIX-2026-P1-*`, `P2-T2-*`, `ADOPTION-EVIDENCE-*`) still live, so that a new one may be created? **If yes:** the rule must cover those families by name, not by wildcard, and the wildcard must stay refused. **If no:** they stay inadmissible and the 11 are frozen history. The implementer must not pick. Note this is why #893's `AID-[0-9]{4}-[0-9]{3}` rule does not reach them: 10 are `authorization-manifest.yaml`, 1 is `FIX-2026-P1-T1/manifest.yaml`. |
| D7 | `requirements.txt` under `08-bmcp-protocol/tests/conformance/*/` | 1 | **Q:** should the root-only `requirements*.txt` rule extend to nested test-harness pins? **If yes:** the rule is `08-bmcp-protocol/tests/conformance/*/requirements.txt` and the root-only rule stays. **If no:** the nested pin is refused and the harness must be pinned another way. |
| D17 | `08-bmcp-protocol/tests/conformance/package.json`, `package-lock.json` | 2 | **Q:** the allowlist admits root `package.json` but not this one. Is that intentional (only the root Node project is sanctioned) or an oversight? **If oversight:** the rule is the exact conformance path. **If intentional:** say so and keep refusing. This is a live inconsistency either way and should be stated, not silently resolved. |
| D19 | `14-ai-development/work-items/AID-2026-003/t2-snapshot-fix-prompt.source.txt` | 1 | **Q:** is a prompt **source** snapshot a repeatable artefact, given hashes are pinned against such files? **If yes:** the rule is `14-ai-development/work-items/*/*.source.txt`. **If no:** it is a one-off and stays refused. |
| D20 | `14-ai-development/work-items/AID-2026-001/reference-model/.gitignore` | 1 | **Q:** only the root `.gitignore` is admitted. Should a nested `.gitignore` inside a work item's reference model be admitted? **If yes:** the rule is the work-item reference-model shape. **If no:** it stays refused and the reference model must not carry one. Found by reconciliation — the first draft of this inventory missed it. |

**Reconciliation: 74 + 4 + 19 + 16 = 113.** The buckets account for every measured path. A
classifier run that does not sum to 113 means a path was silently dropped, and that is a defect in
the inventory, not a rounding difference.

---

## 4. What the implementer must produce

One PR that adds rules **and** proves each rule is narrow. All mandatory:

1. **One rule per admitted shape. Not one rule per extension.** A `.json` rule is forbidden. A
   `08-bmcp-protocol/schemas/*.schema.json` rule is the shape.
2. **Each rule needs at least one positive and one negative test through the real tree-diff
   path** — driving `check_new_paths()` against a real temporary git repo, not calling the
   predicate in isolation. Required by the Owner in round 22.
3. **The negative test must be a near-miss, not a wild miss.** For `crates/*/Cargo.toml` the
   negatives are `crates/x/Cargo.lock`, root `Cargo.toml`, and `crates/x/y/Cargo.toml`. A test
   that only checks `docs/x.md` tests something already tested.
4. **The 13 existing `test_*_is_rejected` tests must all still pass.** They are the fence around
   the `AID-*` rule; a new rule that widens them is a regression, not a feature.
5. **Category C is not admitted.** No rule for `Cargo.lock`, `*.log`, `*.csv`, `*.tla`, `*.cfg`,
   `*.jsonl`, `*.sha256`, root `VERIFICATION.txt`, the tier proposals, or the benchmark/review
   JSON. Record each as deliberately refused.
6. **Category D is not decided by the implementer.** For each D group the PR states the question
   and both candidate answers with their consequences. It does not pick one.
7. **`CHECK_VERSION` must be bumped and the new value must appear in the gate output.** Current
   value is `2026-11-24.1`. A rule change without a version bump makes two different policies
   report the same identity.
8. **The rule must be a regex anchored on the whole path**, following #893's shape
   (`^14-ai-development/work-items/AID-[0-9]{4}-[0-9]{3}/manifest\.yaml$`), not a suffix test and
   not an unanchored `search()`.
9. **A2's two exclusions must be explicit.** If A2 is written as `conformance/**/*.json`, it
   silently admits `package.json` and `package-lock.json`, which are D17. Either exclude them in
   the pattern or split the rule so the exclusion is visible.

---

## 5. Acceptance criteria

| ID | Criterion | How it is measured |
|---|---|---|
| AC1 | Every A and B shape has a rule and is admitted | Positive test per shape, real git tree, exit 0 |
| AC2 | Every admitted shape has a near-miss negative test | Negative test per shape, real git tree, exit 1 with `no allowlist rule for '<path>'` |
| AC3 | The 13 pre-existing rejection tests still pass | `python -m unittest scripts.test_check_repository_hygiene` — full suite green |
| AC4 | No extension-only rule exists | Read the diff: every added pattern constrains a directory or exact path |
| AC5 | Category C stays refused | A table listing each C path with the gate's refusal on it |
| AC6 | Category D is stated, not decided | One subsection per D group with the question and both candidate answers |
| AC7 | `CHECK_VERSION` differs from `2026-11-24.1` and prints | Grep the workflow log for the new version string |
| AC8 | The rule set is not wider than the inventory | Re-run the classifier: the newly-admitted set must equal A∪B (78 paths), and no more |
| AC9 | The inventory closes | Re-run the bucketing classifier and confirm the four bucket totals sum to the refused total |

AC8 is the one that catches over-reach. If a rule admits a path outside A∪B, the rule is wider than
what was justified. AC9 is the one that catches a silently dropped path — the failure this prompt
itself had on its first draft.

---

## 6. Prohibitions

- Do not add a suffix rule for any extension.
- Do not admit any category-C path.
- Do not resolve a category-D question without the Owner.
- Do not describe the 113 as "files that should be admitted". It is a candidate inventory.
- Do not weaken or delete an existing rejection test to make a new rule fit.
- Do not claim the admission gap is closed by this work item; it is closed per-shape, and the
  shapes are enumerated above.
- Do not report a bucket total that does not reconcile to the refused total.
