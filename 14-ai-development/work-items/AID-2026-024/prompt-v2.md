# WORK ITEM: PROPOSED AID-2026-024 — PROMPT v2
# Review of the Existing REQ-06 Evaluation Pilot
# Statistical Validity, Harmful Activation Risk, and Scale-Up Evidence
# REQ-06

## 0. VERSION AND SUPERSESSION

This is prompt v2.

It supersedes prompt v1, which scoped designing a three-arm evaluation
architecture from zero. That premise no longer holds: a REQ-06 pilot already
exists in `main` under `reviews/req06-evaluation-pilot/`.

| version | status | execution basis |
|---|---|---|
| v1 | `FROZEN`, `superseded_by: scope_revision_v2` | no |
| v2 | this document | yes, once R2 is authorised |

v1's SHA-256 and byte count are unchanged in the manifest. v1 is preserved as
history, not overwritten.

**Do not repackage v1's three-arm architecture design task for re-execution.**
That is the exact failure mode this version exists to prevent.

## 1. IDENTITY AND ROLE

You are an Evaluation Methodologist reviewing an existing experiment.

Primary requirement:
REQ-06 — Issue #346
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/346

Joint requirement:
REQ-10 — Issue #350
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/350

Coordination hub:
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/345

Continuation Issue for the integrated path:
Issue #374
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/374

## 2. WHAT THIS WORK ITEM OWNS — AND WHAT IT DOES NOT

**Owned here:**

- Review of the existing pilot against its own stated claims.
- Statistical validity of the reported figures.
- Sample and control design gaps, and the specific claim each gap blocks.
- Harmful-activation risk as delivered, and the evidence needed to bound it.
- Scale-up evaluation plan, including the minimum sample size implied by a
  chosen confidence level.
- Reproducibility and traceability requirements for any scale-up run.
- The boundary against Issue #374's acceptance scope.

**Not owned here:**

- Building or specifying the integrated Brain execution path — Issue #374.
- Re-running the pilot or producing new benchmark numbers.
- Designing a three-arm architecture from zero.
- Any product-improvement claim, including for the policy proxy arm.
- REQ-10 performance measurement — the joint requirement supplies context, but
  the arm-comparability review here does not become a REQ-10 acceptance.

## 3. BASELINE

Repository:
https://github.com/oahcom/AiMemoryBrainArchitecture

Pilot artifacts, all on `main`:

- `reviews/req06-evaluation-pilot/README.md`
- `reviews/req06-evaluation-pilot/corpus.jsonl`
- `reviews/req06-evaluation-pilot/evaluate.py`
- `reviews/req06-evaluation-pilot/pilot-results.json`
- `reviews/req06-evaluation-pilot/test_evaluate.py`
- `reviews/req06-evaluation-pilot/threshold-decision.md`

Pilot carrier: PR #360, merge `0a3e05dc1022f753d0dd6b9eb5ff1470e8dbb730`.

Read every one of those files at current `main`. Do not trust this list's
descriptions of them; read the content and form your own view.

State the commit you read and the blob SHA of each file.

## 4. WHAT THE PILOT CLAIMS — ESTABLISH IT FROM THE SOURCE

Before evaluating, establish what the pilot actually asserts. Read
`threshold-decision.md` and `pilot-results.json` and record:

1. Each numeric figure reported.
2. Each qualitative claim made.
3. Each claim that is explicitly *not* made (the pilot may already bound itself;
   credit that).

Reported figures from the pilot as delivered, for cross-checking only — verify
each against the source rather than taking these as given:

| metric | reported |
|---|---|
| Wilson 95% lower bound | 0.6457 |
| positive hit rate | 1.00 |
| mean precision | 0.4444 |
| harmful activations (proxy arm) | 0 |
| harmful activations (lexical arm) | 6 |
| median latency, proxy | 0.0763 ms |
| median latency, lexical | 0.0838 ms |
| latency ratio | 0.9105× |
| hand-authored tasks | 7 |

If any figure in the source differs from this table, the source wins and the
difference is itself a finding.

## 5. STATISTICAL VALIDITY

This is the core of the Work Item. Answer each, showing the arithmetic:

1. The pilot reports a 7-task Wilson interval of `[0.6457, 1.0]`. What effective
   sample size does that interval imply, and does it match 7?
2. What is the width of that interval, and what does the width alone rule out?
   Specifically: can a lower bound of 0.6457 with an upper bound of 1.0 support
   any claim of superiority over a baseline?
3. Precision is reported as 0.4444. What is the underlying numerator and
   denominator? With that denominator, what is the 95% interval for precision?
4. `harmful = 0` on the proxy arm. With that sample size, what is the upper
   bound of the 95% interval for the harmful-activation rate? A zero count does
   not mean a zero rate — state the bound.
5. The threshold decision adopts gates of Wilson lower bound ≥ 0.60, positive hit
   ≥ 0.80, precision ≥ 0.40, harmful = 0. Are these gates met by the pilot's own
   numbers, or are they met only because the sample is small enough that the
   interval is wide? These are different things. Distinguish them.
6. The latency comparison is 0.0763 ms vs 0.0838 ms, a ratio of 0.9105. With no
   reported variance or run count for latency, what can be said about whether
   that difference is distinguishable from noise?
7. If a reader wanted a Wilson lower bound of 0.60 with a 95% interval whose
   width is at most 0.10, how many independent tasks would be required at the
   observed hit rate? Show the calculation.

For each answer, state whether it changes the pilot's conclusion, narrows it, or
leaves it intact.

## 6. ARM COMPARABILITY

The pilot's third arm is `brain_policy_reference_proxy_NOT_INTEGRATED`, not the
integrated Brain path.

Answer:

1. What exactly does the proxy arm do? Read the evaluator, do not infer from the
   name.
2. Is the proxy arm a fair upper or lower bound on what the integrated Brain
   would do? Justify either way, or state that neither can be established.
3. The lexical arm reports 6 harmful activations and the proxy arm 0. Is that
   comparison confounded by anything other than the mechanism under test —
   corpus selection, task ordering, threshold choice?
4. Are the three arms evaluated on the same tasks with the same scoring? Verify
   from `evaluate.py`.
5. What would have to change for the third arm to be the integrated Brain, and
   which Issue owns that change?

Do not claim product improvement. Do not claim the proxy is a conservative
substitute for the integrated path unless you can show it.

## 7. SAMPLE AND CONTROL GAPS

The pilot corpus is described as 8 repository-grounded records plus 2 synthetic
controls, with 7 hand-authored tasks.

For each gap below, name the specific claim it blocks:

| gap | claim blocked |
|---|---|
| no preference-retention tasks | ? |
| no multi-session handoff tasks | ? |
| no real-user traces | ? |
| no independent relevance labels | ? |

Fill in the right column with the concrete claim that cannot be made while the
gap exists. "Generalisation is limited" is too vague; name what specifically
cannot be asserted.

Also assess: are the 2 synthetic controls used as controls (comparison baseline)
or as test items (part of the measured set)? If the latter, they are not
controls.

## 8. HARMFUL ACTIVATION RISK

1. Define "harmful activation" as the pilot defines it, quoting the definition.
2. Is that definition adequate? Name a harmful case the definition would miss.
3. The lexical arm produced 6 harmful activations out of how many opportunities?
   Compute the rate and its interval.
4. What corpus additions would be needed to bound the proxy arm's harmful rate
   below some stated threshold with 95% confidence?
5. If the integrated Brain path can retrieve context the proxy cannot, is the
   proxy's zero harmful count informative about the integrated path at all?

## 9. SCALE-UP PLAN

Produce a plan, not a wish list. It must state:

1. Target corpus size, derived from §5 item 7's calculation, not picked.
2. Arm integration path: what must exist for the third arm to be the integrated
   Brain, and which Issue delivers it.
3. Minimum run count and what makes runs independent.
4. What is held fixed across arms, and what is allowed to vary.
5. The stopping rule — under what result would the evaluation conclude "no
   product benefit" and be believed.
6. Cost envelope, stated in terms that can actually be measured, or explicitly
   `NOT_ESTIMABLE_FROM_AVAILABLE_DATA`.

## 10. REPRODUCIBILITY AND TRACEABILITY

Specify, concretely:

- Corpus identity: how a run pins the exact corpus (hash algorithm, what is
  hashed, where the hash is recorded).
- Source pins: which blob SHAs must be recorded for a run to be re-derivable.
- Experiment identity: what fields make two runs distinguishable.
- Environment: what must be recorded so a latency number is meaningful
  (hardware, OS, runtime version, load).
- Result storage: where results go and in what schema.

A reader must be able to take a recorded run and either reproduce it or explain
precisely why not.

## 11. BOUNDARY AGAINST ISSUE #374

State, in two lists:

- What this Work Item concludes that Issue #374 may rely on.
- What Issue #374 must establish that this Work Item does not.

The two must not overlap. If a question genuinely belongs to both, say which one
owns it and why.

## 12. REQUIRED OUTPUT

A. Pilot claim inventory, from source.
B. Figure verification table: reported value, source value, match or mismatch.
C. Statistical validity analysis, with arithmetic for each item in §5.
D. Arm comparability assessment.
E. Sample and control gap table, with the claim each gap blocks.
F. Harmful-activation risk assessment with interval bounds.
G. Scale-up plan per §9.
H. Reproducibility and traceability specification per §10.
I. Boundary statement against Issue #374 per §11.
J. Unresolved questions, each with who must answer.

## 13. AUTHORITY

Do not modify `main`.

Do not re-run the pilot and present new numbers as if they were the existing
results.

Do not claim product improvement.

Do not claim REQ-06 or REQ-10 acceptance.

Do not design a three-arm architecture from zero.

Do not specify or build the integrated Brain path.

Do not claim tests passed unless actually run. A run against an excerpt rather
than the repository module graph is `NOT_VERIFIED_AT_REPOSITORY_SCOPE`.

Do not invent model prices, token counts, or performance targets. If the data
was not collected, the answer is `NOT_MEASURED`.

Formal Work Item registration and R2 authorisation must both precede substantive
execution.

## 14. ACCEPTANCE

The review is acceptable only if:

1. Every reported figure is verified against the source, with mismatches flagged
   rather than smoothed over.
2. The statistical analysis shows arithmetic, not adjectives.
3. The zero-harmful-count interval bound is computed, not asserted.
4. Arm comparability is judged from the evaluator's code, not its name.
5. Each sample gap is tied to a specific blocked claim.
6. The scale-up corpus size is derived from a calculation.
7. The stopping rule would actually be believed if it triggered.
8. Reproducibility requirements are concrete enough to implement.
9. The boundary against Issue #374 has no overlap.
10. No product-improvement claim is made anywhere in the document.

## 15. NEXT TASK

Independent methodological review of this assessment. That review is a separate
session; it is not this prompt's deliverable.
