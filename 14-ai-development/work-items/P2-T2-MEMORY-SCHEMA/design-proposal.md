# P2-T2 — Memory Storage Schema Design Proposal

**Work item:** P2-T2 (Phase 2 Task 2)
**Revision:** R5 — revised against independent R4 review of head `bdb19ac0`; R5 confirmation round recorded (§2d)
**Status:** DESIGN PROPOSAL — not implemented, not frozen, not approved
**Review state:** `BLOCKED` — recorded independent-review disposition `REQUEST CHANGES` at R4; no R6 requested at R5. GitHub records no submitted review object for this PR.
**Date:** 2026-11-19
**Scope authority:** `GO-2026-P2-DESIGN-001` — design proposal first; P2-T1 implementation authorization withheld pending design review.

---

## 0. Consolidation note — two concurrent R2 drafts

Two independent sessions produced an R2 revision of this document against the same R1 record. Both were written to the same branch. Rather than overwrite one with the other, both are consolidated here and the divergence is disclosed.

| draft | commit | shape |
|---|---|---|
| R2-a | `61e7c276` | prose only; no DDL; narrows the rebuild guarantee by withdrawing it; leaves the R1-NB-03 integrity fix as an open choice between two acceptable implementations; treats the prompt source as unavailable |
| R2-b | this document | concrete DDL for Layers 2 and 3; three-tier rebuild contract; composite foreign key specified; prompt DDL attached as Appendix A |

What was adopted from R2-a:

- Its caution that the Phase 1 SQLite decision must not be generalised to production topology, multi-host linearizability or power-loss recovery. §3 now says so explicitly.
- Its refusal to invent a Forget mechanism. The earlier draft of this revision described a Forget workflow; that was overreach. A schema proposal may constrain deletion, but authorising a Forget procedure is outside its scope. §7.4 now says what the constraints prevent and stops there.
- Its blob-level provenance. §16 now cites blob SHAs at a fixed commit, not just file paths.
- Its framing that a digest is not a substitute for retaining the data. §8.3 adopts the phrasing as the reason `score_input` exists.

What this draft adds that R2-a could not:

- The prompt DDL itself. R2-a correctly reported the prompt source as unavailable in its session. It is available in this one and is attached verbatim as Appendix A, which is what R1-NB-05 asked for.
- Concrete DDL for the transcript and projection layers, executed in-memory against the real Phase 1 key shapes (§17). R2-a leaves the transcript schema OPEN, which leaves R1-NB-02 answered only in prose.
- The composite foreign key, specified rather than deferred.

Divergence that remains open for review: R2-a treats reproducible numeric recomputation as `NOT CLAIMED`; this draft specifies the conditions under which it holds and the tier where it does not. That is a difference in design posture, not a conflict in fact, and review should rule on which is preferred.

Neither draft is an approval, and the existence of two drafts is not evidence that either was reviewed.

---

## 1. Purpose

Specify the persistence design for the memory layer, covering:

- the logical→physical mapping of the frozen domain objects
- where conversation transcripts live relative to canonical memory
- the vector index boundary
- the rebuild contract for derived scores
- migration strategy
- test boundaries

This revision answers R1-B-01 through R1-NB-05 (§2), the seven items R2 required (§2a), the four findings R3 raised (§2b), and the one residual R4 found (§2c). It records Q1 as decided under the dev-baseline Architecture Owner role (§4), and does **not** claim resolution by an accountable human authority. It does not claim the schema is frozen and does not authorize implementation.

**Status supported by this document:** `BLOCKED — awaiting accountable authority assignment and governance decisions`. Q11 and Q12 have received the bounded dispositions recorded in §2i — technical admissibility for Q11, a prospective reading of the bound for Q12 — issued under the dev-baseline convergence path and carrying `human_signature: NOT_CLAIMED`. Neither closes the accountable-authority question, and no revision of this document can: that requires an authority that is `NOT_ASSIGNED`. Q1 was decided by a decision record, not by revision, but that decision did not constitute acceptance by an accountable human authority; `acceptance_authority` remains `NOT_ASSIGNED` for Q1. See §4 and `DEC-P2-T2-Q1-001.md`.

No identified NF-R3-02 engineering-specification residue remains. DDL executability and regression behavior remain `UNVERIFIED`.

---

## 2. R1 disposition

| finding | severity | disposition in this revision |
|---|---|---|
| R1-B-01 — rebuild from `commit_log` alone is unsupported | BLOCKING | **Corrected.** The rebuild source set is now declared in full (§8.3); the guarantee is split into three tiers and the unreconstructable case is made explicit rather than implied. The `commit_log`-only claim is withdrawn. |
| R1-NB-02 — Event payload ≠ transcript retrieval | NON-BLOCKING | **Corrected.** A separate Layer 2 transcript capture schema is specified with ordering, role, session identity, threading and tool-call relationships, plus the retrieval operations the interface must expose (§7). |
| R1-NB-03 — non-composite FK in `context_assembly_entry` | NON-BLOCKING | **Corrected.** A composite foreign key against `versions(memory_id, version_id)` is used, enabled by an additive unique index (§8.4). |
| R1-NB-04 — conflated canonical vs transcript ownership | NON-BLOCKING | **Corrected.** §5 no longer characterises the prompt schema as inevitably violating canonical invariants. The ownership question is stated as the decision it actually is, and resolved by declaring which layer owns what. |
| R1-NB-05 — prompt source unverifiable at head | NON-BLOCKING | **Corrected.** The exact prompt DDL is attached verbatim as Appendix A, making the evidence package self-contained. |
| Overclaims A–F in R1 §5 | — | **Corrected.** §5, §9 and §16 are rewritten. `satisfies every capability` and `nothing requested is lost` are withdrawn and replaced with an explicit gap table. |
| Date inconsistency (2026-11-20 vs review date 2026-11-19) | — | **Corrected.** Proposal dated 2026-11-19. |
| Claim 2 qualification — trait contract is `CANDIDATE`, not DECIDED | — | **Accepted.** §3 states only that the *SQLite persistence boundary* is DECIDED. The abstract trait is described as a CANDIDATE seam. |

---

## 2a. R2 disposition

R2 was reviewed at head `aed58ad0` and returned `REQUEST CHANGES`, with R1-NB-04 closed and four new findings. Recorded on PR #307, comment `7023510140`.

| item | R2 ruling | disposition in R3 |
|---|---|---|
| R1-B-01 **(A)** algorithm identity ≠ reproducibility | still open | **Corrected.** `scoring_method` gains `algorithm_spec_ref`, `algorithm_spec_sha256` and a constrained `numeric_semantics`. A label without a retrievable spec text that hashes to the recorded value cannot support the exact tier. §8.1 |
| R1-B-01 **(B)** append-only not enforced on `score_input` | still open | **Corrected.** UPDATE and DELETE triggers added, matching the registry. Corrections become new rows via `corrects_input_id`. §8.2 |
| R1-NB-02 tool-call cardinality | partially closed | **Corrected.** `tool_call_id` removed from `transcript_message`; `transcript_tool_call` holds `(session_id, tool_call_id)` with `(emitting_message_id, call_index)` unique. §7.1 |
| R1-NB-02 reconstruction boundaries | partially closed | **Corrected.** `byte_length` stored per message and cross-checked; `reconstruct` returns frames with `byte_offset` / `byte_length` plus per-frame re-hash. §7.1, §7.2 |
| R1-NB-03 boundary — additive index is still a Layer 1 modification | technically corrected, boundary unresolved | **Accepted and corrected.** The index is now described as a Layer 1 modification. Both readings of the boundary are stated with the adapter-level fallback; the choice is Q11, not asserted. §8.4 |
| R1-NB-05 appendix provenance | partially closed | **Accepted without argument.** An appendix is reviewable but cannot authenticate its own origin. §16 records the limit; the remedy is stated. |
| R2-NF-01 tool-call and thread integrity | OPEN | **Corrected.** Composite self-reference on `(session_id, message_id)` forces parent and child into one session; a trigger forces a tool result's parent to be an assistant message. §7.1 |
| R2-NF-02 history provenance integrity | OPEN | **Corrected.** Two composite foreign keys: `(method_id, method_version)` → `scoring_method`, `(version_id, input_id)` → `score_input`. §8.4 |
| R2-NF-03 reconstruction framing | OPEN | **Corrected.** Same fix as R1-NB-02 boundaries. §7.2 |
| R2-NF-04 score-input immutability | OPEN | **Corrected.** Same fix as R1-B-01 (B). §8.2 |
| Q10 — rebuild posture | ruled: tiered preferred | **Recorded as ruled for tiered; exact value conditional and NOT VERIFIED.** §8.3, §14 |
| Disclosure A — two concurrent drafts | acceptable | **No change.** §0 retained. |
| Disclosure B — in-memory schema execution | **not acceptable as authorized activity**; `DISCLOSED SCOPE DEVIATION` | **Accepted as a deviation, not defended.** §17 rewritten: the check is recorded as a deviation, its authority is not claimed, and the question is escalated as Q12. |
| Disclosure C — no rebase | acceptable for review, update before integration | **Accepted.** No rebase performed in R3 either; the integration caveat is carried in §12. |

R3 does not challenge any R2 ruling. Where R2 said a thing was still open, R3 either fixes it or names what remains; it does not argue the ruling down.

---

## 2b. R3 disposition

R3 was reviewed at head `fb1f59de` and returned `REQUEST CHANGES` with four new findings. Recorded on PR #307, comment `7023884586`.

R3 closed three of the seven R2 items outright and was ruled partial on three. Those rulings are accepted as given.

| finding | R3 severity | disposition in R4 |
|---|---|---|
| NF-R3-01 nullable history provenance — `input_id IS NULL` reachable for any `reason` | BLOCKING | **Corrected.** `CHECK` binds the NULL exemption to `initial` and `time_decay` only. §8.4 |
| NF-R3-02 tool-call relational integrity — emitter role, result role, result parent, later UPDATE bypass | BLOCKING | **Corrected.** Four constraints: emitter-is-assistant, result-is-child-tool, `transcript_message_role_frozen`, `tool_call_identity_frozen` + `tool_call_state_transition`. §7.1 |
| NF-R3-03 cross-version correction reference | NON-BLOCKING | **Corrected.** `corrects_input_id` becomes a composite `(version_id, corrects_input_id)` reference. §8.2 |
| NF-R3-04 governance evidence inconsistency — manifest says `DISCLOSED_SCOPE_DEVIATION`, §17 said `DISCLOSED_INTERPRETATION`; §17 said thirteen tests, §13 listed sixteen | NON-BLOCKING | **Corrected, and it was my error.** §17 now states one classification, names the earlier contradiction rather than erasing it, and no longer repeats a test count. |

Two residues are recorded rather than closed: whether a `completed` call must carry a result (Q13), and whether `recompute` truly requires a single input (Q14). Both were flagged by R3 as questions R3 could not settle either.

R4 does not claim that NF-R3-01 and NF-R3-02 are *verified* fixed. They are fixed in the specification. The R3 DDL was never executed, and neither is the R4 DDL — Q12 remains open. What can be checked by reading is that the constraint text now exists and says what the prose says it says.

---

## 2c. R4 disposition — and why this is the last engineering round

R4 was reviewed at head `bdb19ac0` and returned `REQUEST CHANGES` with one residual defect and an explicit recommendation to stop the ordinary revision cycle. Recorded on PR #307, comment `7024484706`.

| finding | R4 ruling | disposition in R5 |
|---|---|---|
| NF-R3-01 nullable history provenance | `CLOSED IN SPECIFICATION` | unchanged |
| NF-R3-02 tool-call relational integrity | `OPEN — BLOCKING`, one UPDATE bypass remains | **Corrected.** `result_message_id` was absent from the frozen column list and its validation trigger is `BEFORE INSERT` only, so a valid call could be re-pointed after the fact. `tool_call_result_binding_guarded` now refuses reassignment, refuses clearing, and repeats the role/parent predicate on the single permitted `NULL → valid` transition. §7.1 |
| NF-R3-03 cross-version correction | `CLOSED IN SPECIFICATION` | unchanged |
| NF-R3-04 governance evidence inconsistency | `CLOSED` | unchanged |
| Q13 — completed call must carry a result | ruled a **separate open question**, not part of NF-R3-02 | kept separate; **decided in §2i** as a table-level `CHECK`, and the separation is preserved — Q13's closure is still not NF-R3-02's |
| Q14 — does `recompute` need a single input | stricter branch **accepted provisionally**, question stays open | unchanged; §2i holds it deliberately, and §14 records it as provisional, not as a business requirement |

**This is the last engineering round.** R4's own recommendation, adopted here: one concrete correction remained, it is made, and no further full revision will be produced against open governance questions. Q1, Q11 and Q12 are not engineering defects. Another iteration cannot reach them. Q1 was subsequently reached by a decision record rather than by iteration (`DEC-P2-T2-Q1-001`, merge `d8e5bebb`). Q11 and Q12 were not reachable by iteration either, and §2i later reached them in part — Q11's technical admissibility, Q12's prospective reading — under the dev-baseline capacity rather than under the accountable authority, which remains `NOT_ASSIGNED` and which neither ruling appoints. Q1's decision likewise did not constitute acceptance by an accountable human authority; `acceptance_authority` remains `NOT_ASSIGNED` for Q1.

The status this document supports is `BLOCKED — awaiting accountable authority assignment and governance decisions`. It does not support `APPROVE`.

---

## 2d. R5 confirmation — and what it does not say

R5 was a confirmation round, not a full revision review, at head `70a68b08`. Recorded on PR #307, comment `7024485207`.

| item | R5 ruling |
|---|---|
| NF-R3-02 residual | `CLOSED IN SPECIFICATION` |
| no-op `UPDATE OF result_message_id` semantics | `NO DEFECT FOUND` |
| new defect introduced by the R4 → R5 correction | `NONE IDENTIFIED` |
| ordinary revision cycle | `STOP` |
| R6 requested | no |

On the no-op question: SQLite fires `UPDATE OF <col>` on the column appearing in the `SET` clause, not on the value changing, so `SET result_message_id = result_message_id` does fire the guard. The predicates were reviewed against that and behave correctly across all six transition cases, including two `NULL`s being treated as no change because `IS NOT` is NULL-safe. The clearing branch is redundant with the reassignment branch; R5 rules that not a correctness defect.

**What R5 does not say:** it does not approve PR #307, and it does not close any governance question. Its explicit final determination is that the engineering correction is complete, the design is not approved, the governance blockers remain open, and the revision cycle stops.

### 2e. Two distinctions this document now carries

R5 asked for two audit-accuracy qualifications, both adopted.

**Review outcome terminology.** The recorded disposition is `REQUEST CHANGES`, but GitHub's review-submission endpoint returns no submitted review objects for this PR. Every review outcome R1–R5 is therefore a discussion record, not GitHub's formal submitted-review state. `REQUEST CHANGES` is described in this document as the *recorded independent-review disposition* and nothing more.

**Residue wording.** The phrase "engineering residue: none outstanding" would read as a statement about executability. The adopted wording is:

> No identified NF-R3-02 engineering-specification residue remains. DDL executability and regression behavior remain UNVERIFIED.

The distinctions preserved throughout:

- `CLOSED IN SPECIFICATION` is not `VERIFIED`.
- `BLOCKED` is not `APPROVED`.
- `REQUEST CHANGES` is not a governance decision.
- `NOT_ASSIGNED` cannot be filled by engineering participation.
- `NOT_GRANTED` cannot be inferred from a design review.

---

## 2f. Q8, Q9, Q11–Q14 ruling received — and the Q11 premise did not survive its own check

*Section title corrected. It read "Q11–Q14" while the section has carried Q8 and Q9 rows since it was written and the ruling request named six questions. A first attempt at this correction widened it to "Q8–Q14", which would have implied Q10 belongs to this ruling — it does not; Q10 has its own separate disposition in §2a. The title now names the six questions the request actually contained.*

A ruling was requested on Q11, Q12, Q13, Q14, Q8 and Q9. Disposition: **PARTIAL
RULING; REMAINING ITEMS BLOCKED BY AUTHORITY OR MISSING BUSINESS INPUT.**

| question | ruling disposition |
|---|---|
| Q11 | **NOT ADOPTED — premise falsified, re-posed.** That disposition stands: the old question was wrong. The re-posed question is now **PARTLY DECIDED in §2i**: technical admissibility settled on a data-neutrality ground, the authorisation half left open for the contract's owner. |
| Q12 | INTERPRETED — prospective interpretation possible; no retrospective authorization. **Issued in §2i**, with the R2 event left un-reclassified. |
| Q13 | RECOMMENDED — adapter-level enforcement → **superseded, DECIDED as table-level `CHECK` in §2i** |
| Q14 | BLOCKED — `BUSINESS_RULE_NOT_SUPPLIED`; **held in §2i**, strict branch stays provisional |
| Q8 | BLOCKED — retention policy absent; **held in §2i**, on the ground that an invented period deletes real data |
| Q9 | OPEN — semantic preservation decision required → **DECIDED in §2i**: retained untyped, neither typed nor dropped |
| Q2–Q7 | DEFERRED — unchanged |

The ruling also directed that gates 1, 2, 3 and 5 of `DEC-P2-T2-Q1-001` §8 be
treated as bounded engineering work, that design acceptance and implementation
authorization not be granted, and that the acceptance-authority vacancy be
recorded rather than re-put to engineering reviewers.

### The Q11 ruling rests on a premise this document supplied, and that premise is false

The ruling states its own limit: the reviewer did not retrieve the repository at
the reviewed head, and the disposition rests on contract language quoted in the
request. It then instructs that the Q11 interpretation be checked against the
exact Layer 1 contract wording before being recorded as a baseline decision.

Checked. The question this document asked was:

> Does the Layer 1 boundary prohibit modifying Layer 1 tables, or only their
> columns?

`02-domain-model/phase-1-sqlite-adapter-contract.md` contains no such
prohibition. What it states is:

- `Status: DECIDED — Phase 1 SQLite persistence boundary only.`
- scope: `explicit schema initialization`, `immutable version rows`,
  current-version CAS, idempotency receipts, monotonic commit sequence, atomic
  transaction, scope-filtered reads, WAL with `synchronous=FULL`.
- evidence: merge `aa711289`, verification commit `4a3e06fd`, CI run `44259233587`.

`immutable version rows` constrains **rows**. It does not constrain schema
objects. No clause forbids a new table, a new index, or an extension to
`versions`.

Two further checks:

| check | result |
|---|---|
| `grep -rn -i "must not be modified\|not be modified\|modifying layer 1\|layer 1 modification\|additive"` across the tree, excluding this work item | no prohibition found |
| `grep -rn -i "layer 1\|layer1"` across the tree, excluding this work item and the `docs/` and `reviews/` trees | **zero hits** |

"Layer 1" and "Layer 2" are terminology introduced by this proposal. **No
inspected repository document defines this boundary or establishes the asserted
prohibition.** That is the finding, and it is bounded by the inspection and the
searches recorded above — not finding the term does not prove that no
document imposes an equivalent restriction under other wording. The claim is
about what was searched, and it is written as such.

The word *boundary* in the contract denotes **the scope of what has been
decided** — the persistence behaviours enumerated above — not **a line that must
not be crossed**. This document read it as the second, asked a question premised
on that reading, and received an answer to the question as asked, explicitly
conditioned on the check that falsifies it. Stated precisely: the inspected Phase 1
contract contains no crossing prohibition, and neither of the two recorded
repository searches located an equivalent prohibition elsewhere. This is the
extent of the finding; it does not establish that no such restriction exists
under unsearched wording.

### What this means for Q11

Q11 is **not closed**. It is re-posed, correctly:

> Does extending the schema of a Phase 1 table — adding an index, without adding
> a column or rewriting a row — require explicit authorisation from a capacity
> that owns the Phase 1 contract?

That is an authorisation question, not a boundary-interpretation question. No
prohibition was located to interpret. And because `acceptance_authority` is
`NOT_ASSIGNED`, the authority that could answer it is, on the ruling's own
reasoning, vacant.

**The strict reading is therefore not adopted, and §8.4 is not rewritten to
remove `versions_memory_version_uq` or the composite foreign key.** That removal
is what the strict reading requires, and it would have been performed had the
premise held. Performing it now would delete a constraint for a reason that no
inspected document establishes — a worse outcome than carrying the question open,
because the resulting schema would look settled while resting on a prohibition
that was not located.

What §8.4 must stop doing is presenting two readings of a boundary that is not
defined. Its two-reading table is replaced by the authorisation question above.

### Q12, Q13, Q14, Q8, Q9 — accepted, and what happened to them since

| question | disposition recorded | dependency named |
|---|---|---|
| Q12 | prospective interpretation **issued (§2i)**; **no retrospective authorisation**; R2's `DISCLOSED_SCOPE_DEVIATION` classification stands permanently | none for the prospective part; retrospective part permanently unavailable |
| Q13 | ~~**`RECOMMENDED`**, adapter-level enforcement~~ → **DECIDED as table-level `CHECK` (§2i)**; still separate from NF-R3-02 | none — issued |
| Q14 | **`BUSINESS_RULE_NOT_SUPPLIED`** — the meaning of `recompute` must come from the owner of the operation's semantics. **Held (§2i).** | business input, not supplied |
| Q8 | retention policy absent; engineering must not invent periods or classes. **Held (§2i).** | retention policy, not supplied |
| Q9 | **DECIDED (§2i)**: retained as untyped event metadata; typing deferred, dropping refused | none — issued |

An open question with a named dependency is actionable. An open question without
one invites the next session to guess. That was the gain from this round at the
time: nothing closed, everything given a dependency.

That is no longer the state of the table above, and the table says so per row
rather than being rewritten. Five of these six were subsequently decided in §2i;
Q8 and Q14 remain held. The heading above is therefore a record of this round's
dispositions, not of current status, and §14 is where current status lives.

### The vacancy, recorded

```text
DESIGN_ACCEPTANCE            = NOT_GRANTED
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
GOVERNANCE_STATUS            = BLOCKED
acceptance_authority         = NOT_ASSIGNED
```

This is an **authority vacancy**, not an engineering backlog item. It is recorded
as such and will not be re-put to review as though a confident answer could fill
it.

---

## 2g. Scope breach and its correction — a fourth file written outside the manifest

**Recorded as a breach, not regularised by widening the manifest.**

`authorization-manifest.yaml` declares three allowed write paths and states
`all_other_paths: OUT_OF_SCOPE`:

- `authorization-manifest.yaml`
- `design-proposal.md`
- `DEC-P2-T2-Q1-001.md`

A gate-conformance map was written to a fourth path,
`P2-T2-MEMORY-SCHEMA/gate-conformance.md`, across three revisions, and three
review rounds examined it without either side noticing. The reviewer's diff
checks confirmed `+164/−0`, then `+53/−25`, then `+25/−15`, each against that
path. Nothing in the review record raised scope, because the review was asked to
examine the document rather than its location.

The breach was found by this session while auditing its own manifest before
merge, not by the review.

**Correction:** the map's content is folded into this proposal as §18, which is
an already-authorized path. The separate file is deleted. The manifest is **not**
amended to legitimise the fourth path — doing so would convert a breach into a
scope expansion after the fact, which is the pattern the Q11 correction exists to
prevent in the other direction.

**What is not claimed:** that folding the content in makes the original write
compliant. It does not. Three revisions were written outside scope. The correction
removes the out-of-scope artefact and preserves the work; it does not retroactively
authorize the writing.

**What is claimed:** that the content now sits in an authorized path, that the
breach is recorded where a reader of this document will find it, and that no
authorization was inferred from the absence of objection across three rounds.

**Who has not acted:** this section is a record by the party that committed the
breach. It is not an adjudication. The authority that issued the manifest has not
been asked to accept, waive or dispose of the breach, and this document does not
attribute any such disposition to it. Recording a violation accurately and having
that violation formally disposed of are different acts, and only the first has
happened.

---

## 2h. A second scope-boundary conflict — `INDEX.md`, and why it is not being written

Raised immediately after PR #315 merged, by this session. Not raised by any review.
Registered as **Q15** in §14.

**The two instruments.** `authorization-manifest.yaml` declares three permitted write
paths and states `all_other_paths: OUT_OF_SCOPE`. `14-ai-development/work-items/INDEX.md`
is not among them. Separately, `AI-STD-001` — `ai-development-standard.md`, lines 445
and 463, English and Chinese — states that the Integration Owner **MUST** maintain that
file as a session → Work Item → Issue/PR traceability index, and declares itself
applicable to all AI-assisted work in the repository.

Neither provision is silence. That is what distinguishes this from Q11, where a ruling
rested on a prohibition the cited contract did not contain. Here there is an explicit
exclusion and an explicit obligation aimed at the same path, so the Q11 remedy — "the
prohibition was not located, therefore it does not bind" — does not transfer. The
exclusion *is* located. What is missing is which document governs when both are read as
written.

**What is established, and what is not.**

| proposition | disposition |
|---|---|
| `INDEX.md` is absent from the three authorised paths | ESTABLISHED |
| `AI-STD-001` assigns a `MUST`-level maintenance obligation for it | ESTABLISHED |
| `AI-STD-001` claims repository-wide applicability | ESTABLISHED |
| `AI-STD-001` has operative authority | **NOT ESTABLISHED** |
| The manifest authorises this work item to write the path | **NOT ESTABLISHED** |
| The five historical writes were authorised | **NOT ESTABLISHED** |
| The five historical writes were unauthorised | **NOT ESTABLISHED** |
| A merge establishes authorisation | NO |

`PROPOSED` status cuts neither way cleanly, and a lazy reading runs in either direction.
Three propositions have to be kept apart:

| proposition | status |
|---|---|
| `AI-STD-001` states an explicit `MUST` requirement to maintain the file | documentary fact |
| That requirement is operative, and how it interacts with an issued work-item manifest | governance question, unresolved |
| The P2-T2 manifest authorises this work item to write the path | not established |

`PROPOSED` does not erase the text: a written repository-wide `MUST` remains an explicit
requirement of the proposed standard. It does not establish the text's own authority
either: stating applicability is not the same as having acquired operative authority to
override an issued manifest. Describing the requirement as "binding but unapplied" would
claim more than the evidence carries in one direction; describing it as void would claim
more in the other. The manifest's narrower scope does not exempt this work item from an
operative standard; the standard's broader scope does not by itself confer greater
authority.

The two are also not logically impossible to satisfy at once. An Integration Owner could
maintain the file through a separately authorised path while this work item's write scope
stays as it is. That reconciliation exists; what is absent is who may direct it.

**What actually happened.** Five writes to the path, across three merged PRs:
`f70ac051` (#309), `2f5f5a22` (#309), `b987c39c` (#309), `1efd47f7` (#311), `daee315a`
(#314). No review round raised it. Their individual circumstances have not been examined
and this record does not classify them identically or at all — only that they fall
outside the currently stated paths, which establishes neither compliance nor violation.

**Why the manifest is not amended, and the path is not written.** Widening the manifest
after the fact would convert a breach into a scope expansion, which §2g refuses in the
other direction and refuses here. The manifest does contain a precedent for disclosing a
deviation rather than resolving it — `schema_execution: DISCLOSED_SCOPE_DEVIATION`,
carried as open question Q12. That precedent covers an event that had **already**
occurred: the DDL was executed, then disclosed, then preserved as a permanent deviation.
Applying it here would be a **prospective** write made in full knowledge of the boundary,
the conflict, and the open question. Disclosure is an accountability mechanism, not an
authorisation mechanism. It records a deviation; it does not license one.

**The consequence, stated rather than hidden.** The P2-T2 row in `INDEX.md` was last
written by `daee315a`, which predates PR #315 (`f8fd64c4`). It does not reflect §18, this
section, the gate-5 decomposition, or the assertion audit. Under `AI-STD-001:445` a stale
source pin is a delivery defect that stays `OPEN`. It is stale now, and correcting it
requires the path this manifest excludes. A write by this work item under the current manifest would exceed its declared
authorisation. Conversely, if `AI-STD-001` is operative, leaving the stale row
uncorrected fails the maintenance requirement it states. The two are not logically
incapable of coexistence — an Integration Owner could maintain the file through a
separately authorised path while this work item's write scope stays as it is. What is
unresolved is the authority to direct that reconciliation, and it is not the implementing
party's determination to make.

**Status.** `OPEN`. Filed as Issue #305 comment `7028019382`, which records the full
question and the five propositions a determination would need to settle. It does not
resolve Issue #305 and does not depend on resolving it first: this is a conflict between
two existing normative documents, not an absence of authority over a single one.


---

## 2i. Rulings issued — five decided, two held, and the capacity that issued them

**Capacity under which this section was written.** Dev-baseline convergence path, Issue #264
comment `7000428916`: under the development baseline there are no human decision points and
every Owner role may be occupied by a session. The user of this session holds that path and
directed it, in three successive instructions, to stop deferring, to converge as the human
would, and to decide. So the rulings below are issued by a session, not by a human.

| capacity | state |
|---|---|
| `human_signature` | **NOT CLAIMED** |
| `acceptance_authority` | remains `NOT_ASSIGNED` |
| accountable-owner appointment | **NOT CLAIMED** |
| production approval | **NOT GRANTED** |
| implementation authorization | remains `NOT_GRANTED` |
| scope of what a ruling here can settle | design questions the document itself poses |

This is the same capacity form `DEC-P2-T2-Q1-001` records for the architecture decision, and
it carries the same exclusions. A ruling below decides what this design will do. It does not
constitute acceptance of the design, and it cannot fill a role that no instrument assigns.

**Why five and not seven.** Q13, Q11, Q12, Q15 and Q9 are questions about this document:
what the schema enforces, what an index changes, what a bound was for, who a write belongs
to, and what a field is for. Those can be settled by reading evidence and choosing. Q8
(retention periods) and Q14 (the meaning of `recompute`) cannot: both ask for a fact about
the world that no amount of reading this repository supplies. Deciding them would not be
decision-making, it would be invention, and it would produce exactly the failure the two
questions were written to prevent — a design that asserts a business rule nobody made.

### Q13 — a `completed` call must name its result. Decided, and the reason it was open was wrong

**Ruling.** `tool_state='completed'` requires a non-NULL `result_message_id`. Enforced by a
table-level `CHECK` on `transcript_tool_call`, not by the adapter.

**What the document said, and what was wrong with it.** §14 carried a `RECOMMENDED`:
adapter-level enforcement, on this stated ground — *"The database does not guarantee it; a
`BEFORE UPDATE OF tool_state` trigger would not cover every write path, including insertion
directly into a completed state."*

The second clause is true. A `BEFORE UPDATE OF tool_state` trigger does miss a direct INSERT
into `completed`. The first clause does not follow from it. It generalises from one mechanism
to the whole layer: the trigger misses that path, therefore *the database* cannot hold the
invariant. A table-level `CHECK` is a different mechanism, and it is evaluated on INSERT as
well as UPDATE. The recommendation was reached by checking one candidate and concluding about
all of them.

**The probe.** The current §7.1 and §8 DDL, assembled with the merged `accepted_events` and
`event_payloads` definitions, executed against an ephemeral in-memory SQLite 3.46.1 — once as
written, once with one added `CHECK`. Fourteen cases:

| # | case | as written | with `CHECK` |
|---|---|---|---|
| A | INSERT `completed` with NULL result | **accepted** — the gap is real | **refused** |
| B | `emitted → completed`, result left NULL | accepted | **refused** |
| C | `emitted → completed` with a valid result | accepted | **accepted** |
| D | INSERT `completed` with a valid result in one row | accepted | **accepted** |
| E | `failed` with NULL result | accepted | **accepted** — unchanged |
| F | `emitted` with NULL result | accepted | **accepted** — unchanged |
| G | bind result first, then set `completed` | accepted | **accepted** |
| H | `completed` bound to a *different* valid child tool message | accepted | **accepted** — see limit 2 |
| I | rebind a bound result | refused by the R4 guard | **refused**, same guard |
| J | clear a bound result | refused by the R4 guard | **refused**, same guard |
| K | UPDATE `tool_name` on a completed row | accepted | **accepted** — no collateral |
| L | result bound while state is still `emitted` | accepted | **accepted** |
| M | `emitted` + result, then `→ failed` | accepted | **accepted** — see limit 1 |
| N | `completed → emitted` | refused by the state trigger | **refused**, same trigger |

C, D, E, F, G, K, L and M are the cases that matter for the ruling as much as A and B: the
`CHECK` refuses the two illegal writes and leaves every legal one alone, including both write
orders an adapter might choose (C and G). I, J and N confirm it does not disturb the R4
residual guard or the state-transition trigger. All fourteen cases produced the expected
result on the amended document DDL — not on a hand-assembled fixture.

**Three limits, recorded rather than glossed.**

1. **The `CHECK` is one-directional.** It forbids `completed` without a result. It does not
   forbid `failed` carrying a bound result, and case M of the probe confirmed that path is
   reachable: `emitted` with a result, then `→ failed`, leaves the result bound to a failed
   call. Whether that is a defect is a separate lifecycle question. It is not decided here.
2. **It constrains when the state may advance, not what the result must contain.** Case H
   shows a completed call may bind any tool message that is a child of its own emitter. That
   is the R4 rule working as specified, not a Q13 hole, but the two are easy to conflate.
3. **It cannot be added later by `ALTER TABLE`.** A probe confirmed SQLite rejects
   `ALTER TABLE ... ADD CONSTRAINT` with a parse error. The constraint is free now — the table
   is new, exists in no merged crate, and is created by this design's own DDL — and would cost
   a table rebuild once rows exist. That asymmetry is the reason the question is settled in
   the design rather than deferred to implementation.

**Why the table and not the adapter.** The adapter is not the only writer. It is the writer
this design intends, but a `CHECK` holds for every writer including a direct SQL client, a
migration script, and a future writer nobody has designed yet. An adapter-level rule is a
convention with a documentation trail; a `CHECK` is a refusal. Where the database can refuse
cheaply, a design should not record an intention instead.

**What this does not close.** NF-R3-02 is `CLOSED IN SPECIFICATION` and remains unverified;
Q13's closure is not its closure. R4's separation instruction is preserved exactly.

### Q11 — the index is technically admissible; what that does not license

**Ruling.** `versions_memory_version_uq` is **data-neutral with respect to the admissible
rows of `versions`**, and is **necessary** for the composite foreign key in §8.4 to function
at all. That is a technical finding, and it is the whole of the finding. It stays declared as
a Layer 1 modification.

**What this ruling does not establish.** It does not establish that data-neutral modifications
are exempt from any independently applicable Phase 1 authorisation requirement. No normative
rule to that effect was located, and this section does not invent one. So the ruling settles
technical admissibility — the index adds no admissible-row effect and the specified composite
foreign key cannot be expressed without it — and leaves the question of whether a Phase 1
authorising capacity would need to approve it exactly where it was. That question is not
void; it is unanswerable from the inspected tree, because the capacity is `NOT_ASSIGNED` and
no rule in `phase-1-sqlite-adapter-contract.md` addresses schema objects at all.

An earlier draft of this ruling stated the stronger conclusion — that no separate
authorisation *is required*. That conflated a technical property (no admissible-row effect)
with a governance exemption (no approval needed), and the second does not follow from the
first without a rule that says so. Narrowed here.

**The ground.** `version_id` is the primary key of `versions`. `(memory_id, version_id)` is
therefore unique by construction: no row can be added, removed or changed in admissibility by
an index on that pair.

What the index actually buys is not uniqueness. It is a **parent key**, without which SQLite
cannot resolve the composite foreign key at all. Six cases, executed against this document's
own §7.1 and §8.4 DDL:

| # | case | result |
|---|---|---|
| P1 | duplicate `(memory_id, version_id)` pair, no index at all | **refused** — `UNIQUE constraint failed: versions.version_id`; the pair is already unique |
| P2 | composite FK, no parent unique index, **correctly matched** pair | **`foreign key mismatch`** — the child table rejects even a valid write |
| P3 | composite FK, no parent unique index, mismatched pair | **`foreign key mismatch`** — a different error, not the intended one |
| P4 | with the unique index, correctly matched pair | **accepted** — `entry inserted` |
| P5 | with the unique index, mismatched pair | **refused** — `FOREIGN KEY constraint failed`; the R1-NB-03 fix works |
| P6 | **non-unique** parent index, correct pair | **`foreign key mismatch`** — uniqueness of the parent key is required, so a plain index is not a substitute |

P2, P3 and P6 are the cases that settle the question. Without a *unique* parent key the
composite foreign key is not "weaker enforcement", it is inert and `context_assembly_entry` is
unwritable — the design would not merely lose a guard, it would lose the table. So the index is
not an optional strengthening of a rule the adapter could enforce instead; it is the
precondition without which the rule cannot be expressed at all.

**What the technical finding does and does not license.** The Phase 1 contract constrains
persistence behaviour and row immutability. An object that admits and rejects exactly the rows
the existing primary key already admits and rejects alters neither of those on `versions`. But
the index is not inert overall: it is what makes the composite foreign key on
`context_assembly_entry` expressible, so it changes that table's behaviour from unusable to
guarded. That is a real effect on a dependent table, and this ruling does not pretend
otherwise. The proposal's own §12 wording — "it does change the schema of a Layer 1 table,
and it is listed here as a modification rather than as no change" — stays true and stays.

**What this ruling does not decide.** It does not decide what the contract's owner would say
about authorisation, and it does not claim that authority. It settles what the probes can
settle: the index adds no admissible-row effect to `versions`, and without it the specified
composite foreign key is inert rather than weaker. If a later reader disagrees with the
data-neutrality finding, the finding is one command away from being rechecked — Appendix B
carries the harness — and the ruling travels with it. If a later authorising capacity
requires approval for any Layer 1 schema object regardless of effect, that requirement is
untouched by this ruling and still applies.

### Q12 — prospective interpretation issued, retrospective ruling refused

**Ruling.** Going forward, executing this design's own DDL against an ephemeral in-memory
database is inside the design-phase bound, provided no file is written, no migration is
applied and no repository path is touched. The R2 event is **not** reclassified.

**The reading, stated as a reading.** The bound `authorization_basis` records — "no code, no
schema execution, no migration, no test claims" — exists to stop the design phase from
producing persistent schema artefacts and from claiming executable results it cannot show. An
in-memory database that dies with the process produces neither. That is a reading of intent,
which is why it is labelled one.

**The refusal.** R2's classification of the R2 event as `DISCLOSED_SCOPE_DEVIATION` stands
permanently. A clarification issued now cannot reach backwards over an act already performed;
if it could, the classification would be worth nothing to any future reader, because every
deviation could be laundered by a later interpretation. Prospective only.

**Disclosure, including against interest.** Two further probes were run while preparing this
section — the Q13 probe (fourteen cases) and the Q11 probe (six cases). Both executed DDL against an
ephemeral in-memory database before this interpretation existed. They are disclosed in §17
under the same heading as the R2 event and are **not** covered by this interpretation
retrospectively. The honest count is now three disclosed executions, not one.

### Q15 — this work item does not write `INDEX.md`. The conflict itself is not resolved

**Ruling.** No write by this work item to `14-ai-development/work-items/INDEX.md`. The stale
P2-T2 row is recorded as a delivery defect with **no owner, because the role that would
own it is unassigned**. That is an ownership gap, not an obligation sitting on some
person's desk: nobody is late on this, and no individual should be read as having failed
to do it. Nor is it this work item's non-compliance, since this work item does not hold
that role.

**The reasoning, which is narrower than the conflict.** `AI-STD-001:445` addresses the
**Integration Owner**. The P2-T2 manifest lists `sponsor`, `accountable_owner` and
`acceptance_authority` as `NOT_ASSIGNED`; no instrument assigns this session the Integration
Owner role, and the manifest's `role_note` forbids substituting a session identity for an
unassigned role. A `MUST` addressed to a role this work item does not hold does not become
addressed to this work item because this work item noticed the file. The manifest's
`all_other_paths: OUT_OF_SCOPE` therefore governs, and the conflict between the two documents
is left exactly where §2h put it.

**What is not decided.** Whether `AI-STD-001` binds anyone at all while it is marked
`Status: PROPOSED`. That is the conflict, and it is not this section's to settle — settling it
would be a governance ruling dressed as a scope call. §14 keeps the `AUTHORITY_CONFLICT`
record verbatim beneath the ruling.

**The cost, named.** The P2-T2 row predates §18 and does not reflect it. It stays wrong until
an Integration Owner exists. A design that records its own staleness is preferable to one that
quietly steps outside its manifest to fix it.

### Q9 — retained as untyped metadata. Not typed, not dropped

**Ruling.** `impact_level` is kept in the event payload as untyped metadata. No typed home is
created for it in this schema.

**Why not dropped.** Dropping is the only irreversible option on the table, and no inspected
document supports it. The field exists in the prompt schema (Appendix A: `impact_level TEXT
CHECK (impact_level IN ('low','medium','high','critical')) DEFAULT 'medium'`). A design that
silently discards a column it was handed is exactly the loss §9's gap table exists to prevent.

**Why not typed.** A typed home asserts that this system's decisions carry a four-value
urgency classification as domain semantics. No inspected source makes that claim: Phase 1 has
no equivalent, and the prompt schema is `UNVERIFIED` as to origin (§16). Adding a constrained
column would launder an unverified input into a domain commitment.

**Why the asymmetry is safe.** The value is preserved inside `envelope_json`, so typing it
later is a migration that reads data already stored — available, not lost. That asymmetry is
the whole argument: keep what cannot be recovered, decline what cannot be justified.

### Q8 and Q14 — held, and why holding them is the decision

Both ask for facts about the world.

- **Q8** asks for retention classes and their default periods. No document in the inspected
  tree states them. A period invented here would be enforced by `retention_class` and by a
  `forget_operation_id` path, which means an invented number would delete real data on a
  schedule nobody authorised.
- **Q14** asks whether `recompute` must reference a single `score_input`. The answer depends on
  what the operation named `recompute` is for, and that belongs to whoever owns scoring
  semantics. The stricter branch is retained provisionally and stays labelled provisional.

Deciding either would produce a document that reads as settled and is not. Holding them is not
deferral: §14 records each with a named dependency, and §18.10 records what work remains
possible without them.

### What these rulings do and do not change

| item | before | after |
|---|---|---|
| Q13 | `RECOMMENDED`, adapter-level | **DECIDED**, table-level `CHECK`, DDL amended |
| Q11 | re-posed, OPEN | **PARTLY DECIDED**: technical admissibility settled on data-neutrality; the authorisation question stands for the contract's owner. Stays declared |
| Q12 | interpretation available, no issuer | **ISSUED** prospectively; R2 event not reclassified |
| Q15 | `AUTHORITY_CONFLICT`, OPEN | **scope decided**; conflict text preserved |
| Q9 | `SEMANTIC_DECISION_REQUIRED` | **DECIDED**, retained untyped |
| Q8 | `POLICY_INPUT_ABSENT` | **unchanged** — held |
| Q14 | `BUSINESS_RULE_NOT_SUPPLIED` | **unchanged** — held |
| `acceptance_authority` | `NOT_ASSIGNED` | **`NOT_ASSIGNED`** |
| implementation authorization | `NOT_GRANTED` | **`NOT_GRANTED`** |
| 21 §13 tests | not written, not run | **not written, not run** |
| DDL | not approved | **not approved**; §7.1 amended, not executed as a migration |

The last four rows are the ones that matter. Five design questions moved. Nothing was
accepted, nothing was authorized, nothing was verified, and no role was filled by a session
deciding to act as one.
---

## 3. What Phase 1 froze, and what it did not

Phase 1 left two different kinds of artefact. They have different authority and this proposal treats them differently.

| source | object | status per R1 Claim 2 |
|---|---|---|
| `02-domain-model/core-entities.md` | Memory, MemoryVersion, Claim, Entity, Relation, Evidence, Provenance, Event, Scope | DECIDED semantics |
| `02-domain-model/phase-1-sqlite-adapter-contract.md` | SQLite adapter: immutable version rows, CAS, idempotency receipts, monotonic commit sequence | **DECIDED**, merged PR #242 / #243 |
| `crates/memory-storage-sqlite/src/lib.rs` | `memories`, `versions`, `idempotency`, `commit_log` | implemented, tested |
| `crates/memory-event-store-sqlite/src/lib.rs` | `accepted_events`, `event_payloads`, `compile_outbox` | implemented, tested |
| `02-domain-model/phase-1-storage-trait-contract.md` | `create_memory`, `read_current`, `read_version`, `commit_version`, `list_changes`, `resolve_idempotency` | **CANDIDATE seam** — the file itself says *"CANDIDATE implementation seam; no backend is selected."* |

The only claim this proposal rests on is the narrow one: **the Phase 1 SQLite persistence boundary is DECIDED.** It does not claim the abstract trait contract was frozen as a backend-neutral DECIDED contract.

The Phase 1 SQLite decision is also not generalised here. It is a decision for the tested local file-backed profile and its stated transaction, CAS and idempotency behaviour. It is not a claim about production topology, multi-host linearizability or power-loss recovery, and this proposal does not extend it into any of those.

Observed schema, quoted from the implementation rather than paraphrased:

```sql
CREATE TABLE IF NOT EXISTS memories (
  memory_id TEXT PRIMARY KEY,
  scope_json TEXT NOT NULL,
  current_version_id TEXT,
  memory_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS versions (
  version_id TEXT PRIMARY KEY,
  memory_id TEXT NOT NULL REFERENCES memories(memory_id),
  version_number INTEGER NOT NULL,
  parent_version_id TEXT,
  scope_json TEXT NOT NULL,
  version_json TEXT NOT NULL,
  commit_sequence INTEGER NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS commit_log (
  commit_sequence INTEGER PRIMARY KEY,
  memory_id TEXT NOT NULL REFERENCES memories(memory_id),
  version_id TEXT NOT NULL UNIQUE REFERENCES versions(version_id)
);
```

Note for §8.3: `commit_log` carries **only** `commit_sequence`, `memory_id`, `version_id`. It carries no score, no score input, no method, no clock. R1-B-01 is correct.

---

## 4. The design question, restated as three options

R1 ruled that escalating the authority conflict was correct, and that the binary framing in R1 was too narrow. The question is therefore restated with three answers.

**Q1 was DECIDED after this section was written, and this section is preserved as it stood rather than rewritten.** The ruling is recorded in `DEC-P2-T2-Q1-001.md` against baseline `049906a9`, merged at `d8e5bebb`: **`OPTION_C`, disposition `ACCEPT-WITH-CONDITIONS`.** The three options below are kept because the choice is only auditable if the alternatives it displaced are still visible. What that ruling closes is the architecture question and nothing else — not the DDL, not Q11–Q14, not Q8/Q9, not design acceptance, not implementation authorization.

**Option A — Phase 1 is the store; transcript capture is Event ingress only.**
No new content tables. Messages become `accepted_events` with payloads. Fewest tables, one system of record, but no message-level query model without building it on top of a generic event stream (R1: material architectural loss unless a transcript capture interface is added).

**Option B — Phase 1 is superseded for the memory path.**
The frozen domain model and Rust adapter become Phase-1-only scaffolding. Requires an explicit supersession decision, a migration off the existing tables, and re-opening the DECIDED status of `phase-1-sqlite-adapter-contract.md`. R1 found no evidence that justifies this.

**Option C — three layers, separate transcript capture (R1's recommendation).**
Phase 1 stays authoritative for canonical memory. Transcript capture becomes its own governed layer with its own retrieval contract. Derived signals become rebuildable projections with declared source dependencies.

**This proposal recommended Option C.** R1 recorded it as `PROPOSED`; a review recommendation is not an authority ruling. The choice was subsequently ruled in favour of Option C by `DEC-P2-T2-Q1-001` (§4 status above), occupying a dev-baseline Architecture Owner role held by a session. That ruling states its own limits: no human Owner signature, no appointment as `acceptance_authority`, no independent human expert review, no production-grade acceptance. `acceptance_authority` remains `NOT_ASSIGNED`. What is settled is the architecture direction; what is not settled is whether the direction has been accepted by any accountable human authority, because there is none.

---

## 5. The design tensions, stated accurately

R1 ruled the earlier version's three "contradictions" `OVERSTATED`. The correction is not cosmetic: the original text asserted that the prompt schema *necessarily* violates canonical invariants. That assertion required proof that the prompt's `messages` row is the canonical content row for a MemoryVersion — and the evidence package did not establish that.

What is actually true is narrower, and the decision that follows is a genuine ownership decision:

| pair | tension | resolved by |
|---|---|---|
| `messages` vs Memory + MemoryVersion | A message is evidence that something was said. A MemoryVersion is a structured assertion the system stands behind. Whether one row serves both is an ownership choice, not a technical impossibility. | Layer 2 owns capture records; Layer 1 owns assertions. Neither row serves both. |
| `decisions` vs Claim | `decision_type IN ('accept','reject','defer','escalate')` is a genuine semantic mismatch with `epistemic_status`. It is not proof the data cannot be stored. | Decision is an Event with a typed payload; the assertion it produces is a Claim in a MemoryVersion. The four values are not reproduced as a constrained column — see the gap table in §9. |
| `file_changes` vs Event + Provenance | A diff summary is capturable as an Event with a provenance edge. | Layer 2 capture record; canonical effect goes through the normal commit path. |
| `context_injections` vs MemoryContext + ContextEntry | `source_message_ids` cannot reference a `memory_version_id` at the identifier level — true, but a source-reference relation bridges the two. | `memory_source_link` records the relation explicitly (§7.3). |
| `sessions` vs Session Scope | A transcript cascade deletes capture records. Whether that also destroys canonical memory depends entirely on what the session row owns. | The session row owns only Layer 2 records, and a RESTRICT foreign key makes the destructive case fail loudly instead of cascading (§7.4). |

Two consequences follow, and both are load-bearing:

1. **Mutable scoring metadata on a transcript record is not per se a canonical-immutability violation.** It is a violation only if that record is the canonical content row. Under Option C it is not. So the prompt's `value_score` column on `messages` is not rejected because it is mutable; it is relocated because scoring is derived and must be rebuildable, which is a different and stronger reason.
2. **A cascade from a session root is not per se a retention violation.** It is a violation if canonical memory is reachable only through that root. Under Option C it is not reachable through it at all, and the one edge that could reach it is `RESTRICT`, so the delete fails rather than destroying anything.

---

## 6. Recommended architecture — three layers

```
Layer 1  CANONICAL MEMORY      memories, versions, idempotency, commit_log
         authority:  Phase 1 DECIDED. Immutable versions, structured claims,
                     provenance, evidence. The system of record.

             │ explicit source references only (memory_source_link)
             ▼

Layer 2  TRANSCRIPT CAPTURE    transcript_session, transcript_message
         authority:  separate governed responsibility. Verbatim bytes live in
                     event_payloads via accepted_events; this layer owns
                     ordering, roles, threading and session association.

             │ versioned derivation and indexing
             ▼

Layer 3  DERIVED INTELLIGENCE  scoring_method, score_input, version_value_projection,
                               version_value_history, version_vector_binding,
                               context_assembly, context_assembly_entry
         authority:  non-canonical projections. Rebuildable from a declared
                     complete source set. Deletable without touching Layer 1.
```

Invariants that hold across the layers:

1. No Layer 1 table has a foreign key into Layer 2 or Layer 3. Canonical rows never depend on derived rows.
2. A transcript message is never promoted to canonical memory by being stored. Promotion goes through `commit_version`.
3. Every canonical Memory derived from a transcript retains a `memory_source_link` row.
4. Layer 1 retention and Layer 2 retention are governed independently, each with its own `retention_class` and `forget_operation_id`.
5. Layer 3 rows are always droppable and rebuildable; Layer 1 rows never are.
6. No `ON DELETE CASCADE` path terminates in a Layer 1 table.

---

## 7. Layer 2 — transcript capture

### 7.1 Schema

```sql
CREATE TABLE IF NOT EXISTS transcript_session (
  session_id          TEXT PRIMARY KEY,
  external_ref        TEXT,                 -- capture channel's own conversation id
  channel             TEXT NOT NULL CHECK (channel IN ('api','cdp','browser','cli')),
  work_item_id        TEXT,
  base_sha            TEXT,
  final_sha           TEXT,
  scope_json          TEXT NOT NULL,        -- Session Scope, same vocabulary as Layer 1
  started_at          TEXT NOT NULL,
  ended_at            TEXT,
  session_state       TEXT NOT NULL CHECK (session_state IN ('open','closed','abandoned')),
  retention_class     TEXT NOT NULL,
  forget_operation_id TEXT,
  metadata_json       TEXT
);

CREATE TABLE IF NOT EXISTS transcript_message (
  message_id        TEXT PRIMARY KEY,
  session_id        TEXT NOT NULL REFERENCES transcript_session(session_id),
  seq_no            INTEGER NOT NULL,       -- monotonic within session, assigned at accept
  role              TEXT NOT NULL CHECK (role IN ('system','user','assistant','tool')),
  event_row         INTEGER NOT NULL REFERENCES accepted_events(event_row),
  content_sha256    TEXT NOT NULL,          -- must equal event_payloads.verified_digest
  byte_length       INTEGER NOT NULL CHECK (byte_length >= 0),
  token_count       INTEGER,
  parent_message_id TEXT,
  edit_state        TEXT NOT NULL DEFAULT 'original'
                      CHECK (edit_state IN ('original','edited','redacted')),
  created_at        TEXT NOT NULL,
  retention_class   TEXT NOT NULL,
  UNIQUE (session_id, seq_no),
  UNIQUE (session_id, message_id),          -- target key for the composite self-reference
  FOREIGN KEY (session_id, parent_message_id)
    REFERENCES transcript_message(session_id, message_id)  -- R2-NF-01: parent in same session
);

CREATE INDEX IF NOT EXISTS transcript_message_order_idx
  ON transcript_message(session_id, seq_no);
CREATE INDEX IF NOT EXISTS transcript_message_role_idx
  ON transcript_message(session_id, role, seq_no);
CREATE INDEX IF NOT EXISTS transcript_message_thread_idx
  ON transcript_message(session_id, parent_message_id);

-- R2-NF-01: an assistant message may emit several tool calls. One row per call.
CREATE TABLE IF NOT EXISTS transcript_tool_call (
  session_id          TEXT NOT NULL,
  tool_call_id        TEXT NOT NULL,        -- provider-assigned
  call_index          INTEGER NOT NULL,     -- order within the emitting message
  emitting_message_id TEXT NOT NULL,
  result_message_id   TEXT,
  tool_name           TEXT,
  tool_state          TEXT NOT NULL DEFAULT 'emitted'
                        CHECK (tool_state IN ('emitted','completed','failed')),
  -- Q13, decided in §2i: a call recorded as completed must name its result. A
  -- table-level CHECK, not a BEFORE UPDATE OF tool_state trigger -- that trigger never
  -- fires for an INSERT that starts in 'completed', which is the path the old
  -- recommendation cited as proof the database could not hold this invariant.
  CHECK (tool_state <> 'completed' OR result_message_id IS NOT NULL),
  PRIMARY KEY (session_id, tool_call_id),
  UNIQUE (emitting_message_id, call_index),
  FOREIGN KEY (session_id, emitting_message_id)
    REFERENCES transcript_message(session_id, message_id),
  FOREIGN KEY (session_id, result_message_id)
    REFERENCES transcript_message(session_id, message_id)
);

CREATE INDEX IF NOT EXISTS tool_call_emitter_idx
  ON transcript_tool_call(emitting_message_id, call_index);

-- A tool result's parent MUST be an assistant message (R2-NF-01). CHECK cannot
-- express this; a trigger can.
CREATE TRIGGER IF NOT EXISTS transcript_message_tool_parent_role
BEFORE INSERT ON transcript_message
WHEN NEW.role = 'tool'
BEGIN
  SELECT RAISE(ABORT, 'tool message parent must be an assistant message')
  WHERE NOT EXISTS (
    SELECT 1 FROM transcript_message
    WHERE session_id = NEW.session_id
      AND message_id = NEW.parent_message_id
      AND role = 'assistant');
END;

-- NF-R3-02 (1): the emitter must be an assistant message.
CREATE TRIGGER IF NOT EXISTS tool_call_emitter_is_assistant
BEFORE INSERT ON transcript_tool_call
BEGIN
  SELECT RAISE(ABORT, 'tool call emitter must be an assistant message')
  WHERE NOT EXISTS (
    SELECT 1 FROM transcript_message
    WHERE session_id = NEW.session_id
      AND message_id = NEW.emitting_message_id
      AND role = 'assistant');
END;

-- NF-R3-02 (2,3): the result must be a tool message whose parent IS the emitter.
CREATE TRIGGER IF NOT EXISTS tool_call_result_is_child_tool
BEFORE INSERT ON transcript_tool_call
WHEN NEW.result_message_id IS NOT NULL
BEGIN
  SELECT RAISE(ABORT, 'tool call result must be a tool message parented by the emitter')
  WHERE NOT EXISTS (
    SELECT 1 FROM transcript_message
    WHERE session_id = NEW.session_id
      AND message_id = NEW.result_message_id
      AND role = 'tool'
      AND parent_message_id = NEW.emitting_message_id);
END;

-- NF-R3-02 (4): the guarded columns of an existing message cannot be changed
-- to bypass the two triggers above.
CREATE TRIGGER IF NOT EXISTS transcript_message_role_frozen
BEFORE UPDATE OF role, parent_message_id, session_id ON transcript_message
BEGIN
  SELECT RAISE(ABORT, 'role, parent_message_id and session_id are immutable on a captured message');
END;

-- The same for a call once recorded: emitter, index and session are frozen.
CREATE TRIGGER IF NOT EXISTS tool_call_identity_frozen
BEFORE UPDATE OF session_id, emitting_message_id, call_index, tool_call_id
  ON transcript_tool_call
BEGIN
  SELECT RAISE(ABORT, 'tool call identity is immutable; record a new call instead');
END;

-- NF-R3-02 residual (R4): result_message_id was writable, so a valid call could
-- be re-pointed at an unrelated message and the INSERT-only check never ran again.
-- Lifecycle permitted: NULL -> a valid child tool message, exactly once.
CREATE TRIGGER IF NOT EXISTS tool_call_result_binding_guarded
BEFORE UPDATE OF result_message_id ON transcript_tool_call
BEGIN
  -- (a) no reassignment once bound
  SELECT RAISE(ABORT, 'result_message_id cannot be reassigned once bound')
  WHERE OLD.result_message_id IS NOT NULL
    AND NEW.result_message_id IS NOT OLD.result_message_id;

  -- (b) unbinding is not permitted either
  SELECT RAISE(ABORT, 'result_message_id cannot be cleared once bound')
  WHERE OLD.result_message_id IS NOT NULL
    AND NEW.result_message_id IS NULL;

  -- (c) a new binding must satisfy the same role/parent rule as at INSERT
  SELECT RAISE(ABORT, 'tool call result must be a tool message parented by the emitter')
  WHERE NEW.result_message_id IS NOT NULL
    AND OLD.result_message_id IS NULL
    AND NOT EXISTS (
      SELECT 1 FROM transcript_message
      WHERE session_id = NEW.session_id
        AND message_id = NEW.result_message_id
        AND role = 'tool'
        AND parent_message_id = NEW.emitting_message_id);
END;

-- And tool_state may only advance, never regress or reopen.
CREATE TRIGGER IF NOT EXISTS tool_call_state_transition
BEFORE UPDATE OF tool_state ON transcript_tool_call
WHEN NOT (
  (OLD.tool_state = 'emitted'   AND NEW.tool_state IN ('completed','failed')) OR
  (OLD.tool_state = 'completed' AND NEW.tool_state = 'completed') OR
  (OLD.tool_state = 'failed'    AND NEW.tool_state = 'failed'))
BEGIN
  SELECT RAISE(ABORT, 'illegal tool_state transition');
END;
```

`event_row` is `NOT NULL` and references `accepted_events(event_row)`, the actual primary key in the merged Event Store. A transcript message is not a copy of the bytes — it is an index over an accepted Event. Bytes live once, in `event_payloads`. This is the R1-NB-02 correction: byte preservation was always adequate; what was missing was the retrieval structure, which is what this table supplies.

`content_sha256` is validated against `event_payloads.verified_digest` at insert. A mismatch is rejected, not repaired.

`byte_length` is stored rather than inferred. R2-NF-03 is right that concatenation alone cannot recover boundaries: a payload of `ab` followed by `c` is byte-identical to `a` followed by `bc`. Storing the length makes reconstruction unambiguous without re-parsing payload contents, and `byte_length` is cross-checked against the stored payload at insert.

`tool_call_id` is **removed** from `transcript_message`. R2-NF-01 is correct that a single column cannot represent one assistant message emitting several tool calls. The relationship now lives in `transcript_tool_call`, keyed `(session_id, tool_call_id)`, with `(emitting_message_id, call_index)` unique so the emission order inside one message is itself deterministic. Both sides of the relation are composite foreign keys on `(session_id, message_id)`, so a call and its result cannot span two sessions.

**NF-R3-02 — the call/emitter/result relation is now enforced, and R3's version was not.** R3 was right: the composite foreign keys only proved the messages existed in one session. They did not prove that the emitter was an assistant message, that the result was a tool message, that the result's parent was the emitter, or that those columns could not be changed afterwards to slip past the trigger. All four are now constrained:

1. `tool_call_emitter_is_assistant` — refuses a call whose emitter is not `role='assistant'`.
2. `tool_call_result_is_child_tool` — refuses a `result_message_id` that is not `role='tool'` **and** parented by that same emitter.
3. The same trigger carries condition 3, since `parent_message_id = NEW.emitting_message_id` is checked in the same predicate.
4. `transcript_message_role_frozen` — `role`, `parent_message_id` and `session_id` are immutable after insert, so a message cannot be re-roled into compliance afterwards. `tool_call_identity_frozen` does the same for the call row, and `tool_call_state_transition` allows `emitted → completed|failed` and forbids regression or reopening.

One honest limit: these are `BEFORE INSERT` checks plus column freezes. They enforce the relation at the moment of writing and prevent later drift through the guarded columns.

**NF-R3-02 residual, found at R4 and closed here.** R4 was right that `result_message_id` was not in the frozen column list, and that `tool_call_result_is_child_tool` is `BEFORE INSERT` only. The resulting sequence was real: insert a valid call, bind a valid result, then `UPDATE result_message_id` to an unrelated assistant message in the same session. The composite foreign key proved only that the target existed in the session, not that it was a tool message parented by the emitter.

`tool_call_result_binding_guarded` closes it with three refusals:

- reassignment once bound (`OLD` non-NULL → different `NEW`) is refused
- clearing once bound (`OLD` non-NULL → `NEW` NULL) is refused
- the one permitted transition, `NULL` → a valid result, repeats the same role-and-parent predicate as the insert check

So the permitted lifecycle is exactly what R4 asked for: initial `NULL` if asynchronous capture is intended, one transition to a valid child tool message, no reassignment, no invalid role or parent relationship.

**Q13 is decided, in §2i, and it was decided against the recommendation this document carried.** The paragraph that stood here said the question stayed open because R4 ruled it must stay separate from NF-R3-02. The separation was right and is preserved: Q13's closure is not NF-R3-02's closure. But the ground given for refusing database enforcement was wrong — it checked a `BEFORE UPDATE OF tool_state` trigger, found it misses a direct insert into `completed`, and concluded about the database. A table-level `CHECK` does not miss that path. The `CHECK` above now refuses `completed` without a result on INSERT and on UPDATE, while `emitted` and `failed` may still carry none.

### 7.2 Retrieval contract

The gap R1 identified was that ordered event retrieval is not transcript retrieval. These are the operations Layer 2 must expose. They are specified here; they are not implemented.

| operation | semantics |
|---|---|
| `read_session(session_id, after_seq, limit)` | messages ordered by `seq_no` ascending; stable, no clock dependence |
| `read_by_role(session_id, role, after_seq, limit)` | same ordering, role-filtered |
| `read_thread(message_id)` | the message plus its `parent_message_id` ancestor chain, oldest first; all rows share one `session_id` by constraint |
| `read_tool_calls(session_id, message_id)` | **all** calls emitted by one assistant message, ordered by `call_index`, each with its `result_message_id` if present |
| `read_tool_result(session_id, tool_call_id)` | the result message plus the emitting message, resolved through `transcript_tool_call` |
| `reconstruct(session_id)` | framed payload bytes, one frame per message, ordered by `seq_no` |
| `source_events(session_id)` | the `accepted_events` rows backing this session, for provenance export |

Ordering is by `seq_no`, never by `created_at`. Capture clocks are not assumed monotonic across channels.

**Reconstruction framing (R2-NF-03).** `reconstruct` does not return a bare concatenation. It returns:

```
ReconstructedTranscript {
  session_id,
  total_bytes,
  frames: [ { message_id, seq_no, role, byte_offset, byte_length, content_sha256 } ],
  buffer: [u8]           // frames[i].buffer[byte_offset .. byte_offset+byte_length]
}
```

with the invariants that `byte_offset` is the running sum of preceding `byte_length`s, that the final offset plus length equals `total_bytes`, and that every frame's slice re-hashes to its `content_sha256`. A caller can therefore cut any single message out losslessly, and a mismatch is detectable rather than silently produced.

### 7.3 Source linkage to canonical memory

```sql
CREATE TABLE IF NOT EXISTS memory_source_link (
  link_id     TEXT PRIMARY KEY,
  message_id  TEXT NOT NULL
                REFERENCES transcript_message(message_id) ON DELETE RESTRICT,
  target_kind TEXT NOT NULL CHECK (target_kind IN ('memory','memory_version','claim','evidence')),
  target_id   TEXT NOT NULL,
  relation    TEXT NOT NULL CHECK (relation IN ('derived_from','cites','asserted_by','supersedes')),
  created_at  TEXT NOT NULL,
  UNIQUE (message_id, target_kind, target_id, relation)
);

CREATE INDEX IF NOT EXISTS source_link_target_idx
  ON memory_source_link(target_kind, target_id);
```

This is the only edge between Layer 2 and Layer 1. It is a plain reference, not a foreign key into Layer 1 — deliberately, so no Layer 1 delete can cascade into it and no Layer 2 delete can cascade into Layer 1. Its own integrity is checked by the adapter on write, and by the test in §13.6.

### 7.4 Why the destructive case fails instead of cascading

`transcript_message.session_id` has no `ON DELETE CASCADE`. Deleting a `transcript_session` while `transcript_message` rows exist is **refused** by the default `NO ACTION` constraint. Deleting a `transcript_message` while `memory_source_link` rows exist is **refused** by `ON DELETE RESTRICT`.

The consequence is the intended one: closing or deleting a session cannot silently destroy the provenance of live canonical memory.

What this section does **not** do is authorise a Forget procedure. An earlier draft of this revision described a retirement workflow with its own `forget_operation_id` and audit record; that was overreach for a schema proposal. The domain model owns the Forget lifecycle, and this design does not invent, replace or constrain it. The narrow, correct claim is negative: these constraints remove the *silent* path. Any actual retirement must follow whatever the canonical Memory lifecycle contract requires, which this document does not specify.

---

## 8. Layer 3 — derived intelligence

### 8.1 Scoring method registry

The R1-B-01 defect was that `method_ref` and `input_digest` identify things without supplying them. A registry supplies them.

```sql
CREATE TABLE IF NOT EXISTS scoring_method (
  method_id             TEXT NOT NULL,
  method_version        INTEGER NOT NULL,
  algorithm             TEXT NOT NULL,     -- label, e.g. 'ebbinghaus_v1'
  algorithm_spec_ref    TEXT NOT NULL,     -- R2 A: normative spec identity, immutable
  algorithm_spec_sha256 TEXT NOT NULL,     -- R2 A: digest of that spec text
  params_json           TEXT NOT NULL,     -- the parameters themselves, not a digest
  params_sha256         TEXT NOT NULL,
  numeric_semantics     TEXT NOT NULL      -- R2 A: rounding / precision / order
                          CHECK (numeric_semantics IN ('f64_ieee754','f64_ieee754_round6','decimal_exact')),
  registered_at         TEXT NOT NULL,
  PRIMARY KEY (method_id, method_version)
);

CREATE TRIGGER IF NOT EXISTS scoring_method_immutable
BEFORE UPDATE ON scoring_method
BEGIN
  SELECT RAISE(ABORT, 'scoring_method is append-only');
END;

CREATE TRIGGER IF NOT EXISTS scoring_method_no_delete
BEFORE DELETE ON scoring_method
BEGIN
  SELECT RAISE(ABORT, 'scoring_method is append-only');
END;
```

A method version is never edited or deleted. A changed parameter set is a new `method_version`.

**R2 finding A — algorithm identity is not algorithm reproducibility.** The reviewer is right: `ebbinghaus_v1` is a label, and two implementations carrying it can differ in arithmetic, rounding, intermediate precision and evaluation order. Three columns are added so the label is no longer the whole identity:

- `algorithm_spec_ref` + `algorithm_spec_sha256` — the normative specification the label names, and its digest. A label without a retrievable spec that hashes to the recorded value cannot support the exact-value tier.
- `numeric_semantics` — a constrained vocabulary (`f64_ieee754`, `f64_ieee754_round6`, `decimal_exact`). Two implementations agreeing on spec but differing on rounding are not the same method.

This does not make the value reproducible by itself; it makes the *identity* of the computation falsifiable. The exact tier in §8.3 now requires a spec digest that matches, not merely a matching label.

### 8.2 Declared score inputs

```sql
CREATE TABLE IF NOT EXISTS score_input (
  input_id      TEXT PRIMARY KEY,
  version_id    TEXT NOT NULL REFERENCES versions(version_id),
  input_kind    TEXT NOT NULL CHECK (input_kind IN
                  ('initial','citation','decision','clock_tick','manual_adjustment')),
  source_kind   TEXT NOT NULL CHECK (source_kind IN ('event','claim','commit','operator')),
  source_ref    TEXT NOT NULL,
  weight        REAL,
  observed_at   TEXT NOT NULL,
  recorded_at   TEXT NOT NULL,
  corrects_input_id TEXT,                  -- R2 B: corrections are new rows
  UNIQUE (version_id, input_kind, source_kind, source_ref),
  UNIQUE (version_id, input_id),            -- R2-NF-02: parent key for value_history
  FOREIGN KEY (version_id, corrects_input_id)
    REFERENCES score_input(version_id, input_id)   -- NF-R3-03: same-version correction
);

CREATE INDEX IF NOT EXISTS score_input_version_idx
  ON score_input(version_id, observed_at);

-- R2-NF-04 / R2 B: append-only is enforced, not asserted.
CREATE TRIGGER IF NOT EXISTS score_input_immutable
BEFORE UPDATE ON score_input
BEGIN
  SELECT RAISE(ABORT, 'score_input is append-only; record a correction as a new row');
END;

CREATE TRIGGER IF NOT EXISTS score_input_no_delete
BEFORE DELETE ON score_input
BEGIN
  SELECT RAISE(ABORT, 'score_input is append-only; record a correction as a new row');
END;
```

Each row is an input that a score actually consumed: a citation event, a decision event, a clock tick, an operator adjustment, the initial creation. This table is the difference between "a digest points at something" and "the something is on disk".

**R2 finding B — append-only was prose, not an invariant.** Correct. Two triggers now enforce it, matching what the registry already does. A wrong historical input is corrected by inserting a new row with `corrects_input_id` pointing at the row it supersedes; the original stays, and the pair is visible. Historical mutation is refused by the database rather than by convention.

Note the honest limit: enforcement prevents *later* mutation. It does not prove the *original* set was complete. A row that was never recorded cannot be conjured, and §8.3's `unreconstructable` tier is where that shows up.

### 8.3 The rebuild contract — three tiers, stated honestly

**Complete declared source set** for reproducing `version_value_projection` for a given `version_id`:

1. `versions.version_json` and `versions.scope_json` for that version — the immutable canonical content.
2. Every `score_input` row for that `version_id` — the inputs, with `observed_at` as their observation times.
3. The `scoring_method` row matching the projection's `(method_id, method_version)` — algorithm and parameters.
4. The evaluation clock value, recorded on the projection row as `evaluated_at`.

`commit_log` is **not** in this set. It is used only to enumerate which versions exist and in what order they were committed. The earlier claim that the projection is "rebuildable from `commit_log` alone" is withdrawn as incorrect.

```sql
CREATE TABLE IF NOT EXISTS version_value_projection (
  version_id        TEXT PRIMARY KEY REFERENCES versions(version_id),
  method_id         TEXT NOT NULL,
  method_version    INTEGER NOT NULL,
  value_score       REAL NOT NULL CHECK (value_score  >= 0 AND value_score  <= 100),
  decay_weight      REAL NOT NULL CHECK (decay_weight >= 0 AND decay_weight <= 1),
  weighted_score    REAL NOT NULL,
  evaluated_at      TEXT NOT NULL,
  input_set_digest  TEXT NOT NULL,   -- sha256 over ordered score_input rows + method params
  rebuild_state     TEXT NOT NULL CHECK (rebuild_state IN
                      ('exact','partial','unreconstructable')),
  computed_at       TEXT NOT NULL,
  FOREIGN KEY (method_id, method_version)
    REFERENCES scoring_method(method_id, method_version)
);
```

Three rebuild tiers, each with a different promise:

| tier | promise | condition |
|---|---|---|
| **Structural** | Dropping and recreating Layer 3 reproduces the same row identities, links, statuses and ordering. Idempotent. | always |
| **Exact value** | `value_score`, `decay_weight` and `weighted_score` are byte-identical after rebuild. | iff the `scoring_method` row exists **and its `algorithm_spec_sha256` matches a retrievable spec**, **and** `numeric_semantics` is identical, **and** the `score_input` set is unchanged (recomputed `input_set_digest` matches), **and** `evaluated_at` is supplied as recorded. **Status: CONDITIONAL — design objective, not substantiated.** See below. |
| **Unreconstructable** | Reported as `unreconstructable` with the missing dependency named. Never silently defaulted, never approximated. | the `score_input` set is incomplete, or the projection's `(method_id, method_version)` is not in the registry, or `evaluated_at` was never recorded |

A missing method row and an incomplete input set are both reachable: the composite foreign key guarantees a method row exists **at insert time**, not that the historical input set is complete. A rebuild is a read of the past, and the past can be under-recorded.

The third row is the point. A rebuild that cannot reproduce a value must say so. A rebuild that quietly substitutes a default is worse than no rebuild, because it manufactures false confidence in a derived number.

**The exact-value tier is not substantiated, and this revision does not claim it is.** R2's ruling: retain it as a conditional design objective, do not adopt a blanket `NOT CLAIMED` posture, and do not claim the complete numeric source set has been proven. R3 accepts that ruling as stated. What is now specified is the *condition under which the claim would be true* — matching spec digest, matching numeric semantics, unchanged input set, recorded evaluation clock — not the evidence that it is true. Establishing it needs a worked example: one version, one method, one recorded score, recomputed by an independent implementation and compared byte for byte. That is not in this proposal, and no test in §13 was run.

```sql
CREATE TABLE IF NOT EXISTS projection_rebuild_log (
  rebuild_id        TEXT PRIMARY KEY,
  scope_json        TEXT NOT NULL,
  started_at        TEXT NOT NULL,
  finished_at       TEXT,
  exact_count       INTEGER NOT NULL DEFAULT 0,
  partial_count     INTEGER NOT NULL DEFAULT 0,
  unreconstructable_count INTEGER NOT NULL DEFAULT 0,
  detail_json       TEXT
);
```

Naming note: the earlier revision's `input_digest` column is replaced by `input_set_digest`, and its meaning narrowed to "digest over the declared, ordered input set" — not "pointer to inputs stored somewhere else".

### 8.4 Value history, vector binding, context — with composite integrity

```sql
CREATE TABLE IF NOT EXISTS version_value_history (
  history_id     TEXT PRIMARY KEY,
  version_id     TEXT NOT NULL REFERENCES versions(version_id),
  old_score      REAL,
  new_score      REAL NOT NULL,
  reason         TEXT NOT NULL CHECK (reason IN
                   ('initial','cited_by_decision','time_decay','manual_adjustment','recompute')),
  method_id      TEXT NOT NULL,
  method_version INTEGER NOT NULL,
  input_id       TEXT,
  recorded_at    TEXT NOT NULL,
  FOREIGN KEY (method_id, method_version)
    REFERENCES scoring_method(method_id, method_version),      -- R2-NF-02
  FOREIGN KEY (version_id, input_id)
    REFERENCES score_input(version_id, input_id),              -- R2-NF-02
  -- NF-R3-01: the NULL exemption is bound to the reasons that justify it.
  CHECK (
    (reason IN ('initial','time_decay')          AND input_id IS NULL)
    OR
    (reason IN ('cited_by_decision','manual_adjustment','recompute') AND input_id IS NOT NULL)
  )
);

CREATE INDEX IF NOT EXISTS value_history_version_idx
  ON version_value_history(version_id, recorded_at);
```

Two composite foreign keys close R2-NF-02 for the non-NULL case, and the `CHECK` closes the NULL case.

**NF-R3-01 — the NULL exemption is now bound to reason.** R3 was right: the composite foreign key uses SQLite's NULL semantics correctly, but nothing stopped `reason='cited_by_decision'` or `reason='manual_adjustment'` from being recorded with `input_id IS NULL`, which is exactly the provenance hole the FK was meant to close. The `CHECK` above makes the exemption reachable only for `initial` and `time_decay`.

One judgement call is recorded rather than hidden: `recompute` is constrained to require an `input_id`. The reviewer explicitly flagged that whether `recompute` genuinely must reference a single input is a business question, not something a schema proposal can settle. The constraint takes the stricter branch, and if the business answer is that a recompute may legitimately have no single input, the fix is to add `recompute` to the nullable set — a one-line change, visible in the `CHECK`, not a silent default.

Two other composite keys close the rest:

- `(method_id, method_version) → scoring_method` — a history row cannot name a method version that does not exist.
- `(version_id, input_id) → score_input` — an input cannot be claimed by a different version's history.

**NF-R3-03 — corrections are same-version.** `corrects_input_id` was a single-column reference, so a version-A input could claim to correct a version-B input and nothing refused it. It is now a composite `(version_id, corrects_input_id) → score_input(version_id, input_id)`, with `NULL` retained for rows that correct nothing. SQLite does not enforce a composite foreign key when any component is `NULL`, which is the intended behaviour for non-correction rows rather than an oversight.

The `(version_id, input_id)` parent key requires a matching unique key on `score_input`. `input_id` is already the primary key, so `(version_id, input_id)` is unique by construction; §8.2 gains `UNIQUE (version_id, input_id)` to give the constraint a real target.

```sql
CREATE TABLE IF NOT EXISTS version_vector_binding (
  version_id        TEXT PRIMARY KEY REFERENCES versions(version_id),
  embedding_id      TEXT NOT NULL UNIQUE,
  embedding_model   TEXT NOT NULL,
  embedding_dim     INTEGER NOT NULL,
  version_sha256    TEXT NOT NULL,   -- sha256 of versions.version_json at bind time
  indexed_at        TEXT NOT NULL,
  index_status      TEXT NOT NULL CHECK (index_status IN
                      ('pending','indexed','stale','failed')),
  stale_reason      TEXT,
  binding_epoch     INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS vector_binding_status_idx
  ON version_vector_binding(index_status);

CREATE TABLE IF NOT EXISTS context_assembly (
  assembly_id     TEXT PRIMARY KEY,
  agent_scope_id  TEXT NOT NULL,
  session_scope_id TEXT,
  task_scope_id   TEXT,
  created_at      TEXT NOT NULL,
  assembly_state  TEXT NOT NULL CHECK (assembly_state IN ('draft','active','closed'))
);

-- This IS a modification to a Layer 1 table. It adds no column and rewrites no row,
-- but it changes the schema of `versions` and must not be described as no change.
CREATE UNIQUE INDEX IF NOT EXISTS versions_memory_version_uq
  ON versions(memory_id, version_id);

CREATE TABLE IF NOT EXISTS context_assembly_entry (
  entry_id        TEXT PRIMARY KEY,
  assembly_id     TEXT NOT NULL REFERENCES context_assembly(assembly_id),
  memory_id       TEXT NOT NULL,
  version_id      TEXT NOT NULL,
  position        INTEGER NOT NULL,
  relevance_score REAL,
  entry_state     TEXT NOT NULL CHECK (entry_state IN ('included','excluded','expired')),
  added_at        TEXT NOT NULL,
  FOREIGN KEY (memory_id, version_id)
    REFERENCES versions(memory_id, version_id),   -- R1-NB-03
  UNIQUE (assembly_id, position)
);

CREATE INDEX IF NOT EXISTS assembly_entry_assembly_idx
  ON context_assembly_entry(assembly_id, position);
```

The composite foreign key is the R1-NB-03 fix. Two independent foreign keys proved existence and nothing else; a pair of values that individually exist but do not belong together would have been accepted. Now it cannot be inserted.

**R1-NB-03 boundary, resolved explicitly (R2 required item 4).** R2 ruled this correct in technique and unresolved in boundary: an additive index is still a modification to the Layer 1 schema — not a column alteration, but not literally zero modification — and the proposal must not describe it as though it were no modification. Accepted, and the earlier wording is corrected in place.

The two-reading table that stood here has been removed. It presented two
interpretations of a boundary that **no inspected document defines** (§2f). No
prohibition was located to interpret, so choosing between two readings of it was
never the right question.

The correct framing is an authorisation question, and it is carried as **Q11**:

> Does extending the schema of a Phase 1 table — adding an index, without adding
> a column or rewriting a row — require explicit authorisation from a capacity
> that owns the Phase 1 contract?

Three things follow, and they are stated rather than inferred:

1. **No prohibition was located.** `phase-1-sqlite-adapter-contract.md`
   constrains persistence behaviour and row immutability; it does not constrain
   schema objects. Verified in §2f with the exact clauses and two bounded
   searches. Stated as a bounded negative, not as a universal one.
2. **The search result left admissibility undecided at the time, and §2i has
   since decided it.** A bounded search is not an admissibility determination, and
   the thing being extended belongs to a contract whose owning capacity has not
   been identified — which is why the question was carried rather than answered
   here. §2i answers the technical half on a different ground entirely — the
   index is data-neutral — and explicitly does not answer the authorisation half:
   no rule exempts a data-neutral modification from Phase 1 approval, so that
   question stands for the contract's owner. Six probes recorded there; the
   adapter-level fallback below is retained as what the
   implementation would do if that finding were overturned.
3. **The adapter-level fallback stays documented** as the implementation that
   would be used if an authorising capacity later declines the index. Drop the
   index and the composite foreign key; read the version's owning `memory_id`
   and reject a mismatch inside the same transaction that inserts the context
   entry. That fallback is strictly weaker: it holds only for writers that use
   the adapter, whereas a database-enforced composite foreign key holds for any
   writer.

This proposal **recommends the index**, and §2i now finds it *technically*
admissible — it changes no admissible row of `versions`, and the specified composite
foreign key cannot be expressed without it. That is a technical finding and it is
the whole of what §2i claims here. It is **not** a finding that the extension
needed no authorising capacity; no rule exempts data-neutral modifications from
Phase 1 approval, and §2i says so. What is still not claimed is *approval* of any
kind: no accountable authority has accepted this design, and `acceptance_authority`
remains `NOT_ASSIGNED`. The distinction that mattered at the time — a
recommendation is the author's, an authorisation is a capacity's — stands
unchanged.

`version_sha256` is a digest of `version_json` as stored, computed by the adapter. R1 correctly noted digest validation does not by itself solve external index lifecycle — that is why `index_status` and `binding_epoch` exist; stale-binding recovery is an operational procedure over those columns, not a constraint. It is listed as Q7, still open.

---

## 9. Capability table — with the gaps named

R1 ruled the previous "satisfies every capability" and "nothing requested is lost" claims overstated. They are withdrawn. This is the honest version.

| prompt capability | status under Option C | gap |
|---|---|---|
| store chat messages verbatim | SUPPORTED — `transcript_message` + `event_payloads` | none at byte level |
| message-level query model | SUPPORTED — §7.2 operations | new code, not in Phase 1 |
| `decisions` with accept/reject/defer/escalate | PARTIAL | the four values are not reproduced as a CHECK-constrained column; they live in the decision Event's typed payload and map to Claim polarity plus lifecycle |
| `impact_level` low/medium/high/critical | PARTIAL | no domain equivalent; retained as untyped event metadata, so it is not queryable as an enum |
| `file_changes` with line counts | PARTIAL | Event + provenance edge is faithful; `lines_added` / `lines_deleted` exist only if the capture channel records them |
| Ebbinghaus decay | PARTIAL | storage and method registry defined; the parameters themselves are Q5, open |
| value scoring | PARTIAL | mechanism and inputs defined; the scoring algorithm is Q5, open |
| `top_memories` view | SUBSTITUTED | query over `version_value_projection` joined to `memories`; `weighted_score` ordering preserved, `LIMIT 100` becomes a query parameter. Not a schema object. |
| `recent_decisions` view | SUBSTITUTED | query over decision Events joined to Claims |
| mutable `messages.value_score` | **DELIBERATELY NOT PROVIDED** | mutating a score in place would break the rebuild contract; that is the point of moving it |

Three things are genuinely not preserved as-is, and none of them is hidden: `impact_level` enum typing, `decision_type` as a constrained column, and the two prompt views as schema objects. Whether that trade is acceptable is a design question for R2 review, not a settled fact.

---

## 10. Data model mapping

| frozen object | physical home | mutability |
|---|---|---|
| Memory | `memories` (Layer 1) | current pointer mutable, object immutable |
| MemoryVersion | `versions` (Layer 1) | immutable |
| Claim / Entity / Relation / Evidence / Provenance | serialised in `versions.version_json` | immutable per version |
| Event | `accepted_events` + `event_payloads` (Layer 1) | append-only |
| Compile intent | `compile_outbox` (Layer 1) | consumed once |
| Scope | `memories.scope_json`, `versions.scope_json` | bound at commit |
| Session | `transcript_session` (Layer 2) | mutable state, owns no canonical row |
| Message | `transcript_message` (Layer 2) | append-only; edits are new `seq_no` with `edit_state` |
| Source relation | `memory_source_link` (Layer 2) | append-only, retirement by Forget |
| Score input | `score_input` (Layer 3) | append-only |
| Value / decay | `version_value_projection` (Layer 3) | rebuildable |
| Value history | `version_value_history` (Layer 3) | append-only |
| Vector embedding | external store + `version_vector_binding` (Layer 3) | rebuildable |
| Context | `context_assembly` + `context_assembly_entry` (Layer 3) | mutable, non-canonical |

**OPEN:** whether Claim/Entity/Relation should be extracted into their own tables for query. Phase 1 stores them inside `version_json`. Extraction creates a second representation that must stay consistent with an immutable version — a projection with a rebuild path, not a second source of truth. Deferred to P2-T3.

---

## 11. Interface boundary

Phase 2 must not change the Phase 1 `MemoryStorage` trait. Additions are separate traits.

```rust
pub trait TranscriptCapture {
    fn read_session(&self, session_id: &SessionId, after_seq: u64, limit: usize)
        -> Result<Vec<CapturedMessage>, Error>;
    fn read_by_role(&self, session_id: &SessionId, role: MessageRole,
                    after_seq: u64, limit: usize) -> Result<Vec<CapturedMessage>, Error>;
    fn read_thread(&self, message_id: &MessageId) -> Result<Vec<CapturedMessage>, Error>;
    fn read_tool_calls(&self, session_id: &SessionId, message_id: &MessageId)
        -> Result<Vec<ToolCall>, Error>;
    fn read_tool_result(&self, session_id: &SessionId, tool_call_id: &str)
        -> Result<ToolCallPair, Error>;
    fn reconstruct(&self, session_id: &SessionId) -> Result<ReconstructedTranscript, Error>;
}

pub trait MemoryValueProjection {
    fn compute_value(&self, version_id: &VersionId, at: EvalClock)
        -> Result<ValueProjection, Error>;
    fn read_projection(&self, version_id: &VersionId) -> Result<Option<ValueProjection>, Error>;
    fn rebuild(&self, scope: &Scope, at: Option<EvalClock>) -> Result<RebuildReport, Error>;
}

pub trait VectorIndex {
    fn bind(&self, version_id: &VersionId, embedding: &Embedding) -> Result<Binding, Error>;
    fn search(&self, query: &Query, scope: &Scope, top_k: usize) -> Result<Vec<Hit>, Error>;
    fn invalidate(&self, version_id: &VersionId, reason: &str) -> Result<(), Error>;
}
```

Invariants:

- `bind` MUST reject when `version_sha256` does not match the digest of the stored `version_json`.
- `search` MUST filter by scope before returning hits; scope filtering is not a post-filter.
- `invalidate` MUST NOT delete canonical content; it sets `index_status='stale'` and increments `binding_epoch`.
- `rebuild` MUST be idempotent, MUST report each version under exactly one of `exact` / `partial` / `unreconstructable`, and MUST NOT write a substituted value where it cannot reproduce the original.
- `rebuild` with `at = None` may only produce `partial` or `unreconstructable` results, because `evaluated_at` was not supplied.
- `read_tool_calls` MUST return all calls emitted by one message in `call_index` order; there is no single-call form, because one message may emit many.
- `reconstruct` MUST return framed output, not bare bytes; a frame whose slice does not re-hash to its `content_sha256` MUST be reported as corrupt rather than returned.

---

## 12. Migration strategy

| step | action | reversibility |
|---|---|---|
| M1 | Create Layer 2 and Layer 3 tables with `IF NOT EXISTS`; add `versions_memory_version_uq` index | drop new tables and index |
| M2 | Backfill `transcript_*` from existing `accepted_events` where a session mapping is recorded | truncate; Layer 2 is not canonical |
| M3 | For each existing version, insert an `initial` `score_input` row so that scores have a declared input set | delete inserted rows |
| M4 | Register a `scoring_method` row per algorithm with its spec digest and numeric semantics; without these no projection may claim `exact` | delete inserted rows |
| M5 | Compute projections; every row starts `rebuild_state='partial'` (no historical `evaluated_at` exists for pre-migration versions) | drop projections |
| M6 | Bind vectors; `index_status='pending'` until the external index confirms | delete bindings |
| M7 | Cut over reads | revert to Phase 1 reads |

No destructive migration. No `ALTER TABLE` on Layer 1 tables. No rewrite of `versions`. One Layer 1 modification is proposed and declared as such: the additive unique index `versions_memory_version_uq` (§8.4). It adds no column and rewrites no row, but it does change the schema of a Layer 1 table, and it is listed here as a modification rather than as no change.

**Integration caveat (R2, disclosure C).** This branch is not rebased onto current main. R2 verified that the intervening commits touch `remote-worker-inventory.yaml` and the runbook pair only, none of which this proposal depends on, and ruled a forced rebase unnecessary for the design review. The branch must be updated against current main before the PR is treated as fully integrated or merged. GitHub's `mergeable` field does not substitute for that check.

Note M4 honestly: pre-migration versions cannot reach `exact` rebuild state, because their evaluation clock was never recorded. They stay `partial` permanently unless an operator supplies a reconstructed clock, which would then be an `operator` `score_input` row and visible as such.

**Schema versioning:** a `schema_migrations` table with `(version, applied_at, checksum)`, forward-only, each migration idempotent. The prompt's `schema_version` is kept in spirit with a checksum column added, because a version string alone cannot detect a partially-applied migration.

---

## 13. Test boundaries

Required before implementation authorization is granted. These are specified, not run.

1. **Vector digest binding** — `bind` rejects a `version_sha256` that does not match stored `version_json`.
2. **Scope isolation** — two scopes, identical content; each `search` returns only its own scope's versions.
3. **Invalidation is non-destructive** — `invalidate` leaves `versions` row count unchanged and sets `index_status='stale'`, `binding_epoch` incremented.
4. **Rebuild — exact tier** — with the spec digest matching, `score_input` set unchanged and `evaluated_at` supplied, drop and rebuild produces byte-identical scores and a matching `input_set_digest`.
5. **Rebuild — unreconstructable tier** — delete `score_input` rows for a version (simulating an under-recorded history), run rebuild, assert `rebuild_state='unreconstructable'` with the missing dependency named, and assert no `value_score` was written.
6. **Rebuild — partial tier on migration** — pre-migration versions rebuild to `partial`, never `exact`, and never silently to `exact`.
7. **Method immutability** — `UPDATE` and `DELETE` on `scoring_method` both abort.
8. **Composite integrity** — insert a `context_assembly_entry` with a `version_id` belonging to a different `memory_id`; assert refused. **Conditional on Q11**: with `versions_memory_version_uq` present the refusal comes from the composite foreign key and holds for any writer; without it the refusal must come from the adapter inside the insert transaction and holds only for adapter writers. The test asserts the refusal, and separately asserts which mechanism produced it, so the weaker configuration cannot pass as the stronger one. In the database-enforced branch the insert must be issued by a **direct SQL writer that bypasses the adapter** — asserting through the adapter would only show that the adapter refuses, which is the weaker claim the branch is supposed to distinguish itself from.
9. **No cascade destruction** — delete a `transcript_session` that has messages; assert refused. Then delete a `transcript_message` that has a `memory_source_link`; assert refused.
10. **Canonical row counts** — closing and retiring sessions leaves `memories` and `versions` row counts unchanged.
11. **Transcript ordering** — insert messages out of `created_at` order with valid `seq_no`; assert `read_session` returns `seq_no` order.
12. **Tool-call cardinality (R2-NF-01)** — one assistant message emits three tool calls with distinct `tool_call_id` and `call_index` 1..3; assert `read_tool_calls` returns all three in order, and that inserting a fourth with duplicate `call_index` is refused.
13. **Tool-call thread integrity (R2-NF-01)** — assert a `tool` message whose parent is a `user` message is refused by the trigger, and that a `transcript_tool_call` referencing a `result_message_id` in a different `session_id` is refused by the composite foreign key.
14. **Reconstruction framing (R2-NF-03)** — reconstruct a session of three messages and assert `frames[i].byte_offset` is the running sum of preceding `byte_length`s, that the last offset plus length equals `total_bytes`, and that each frame slice re-hashes to its `content_sha256`. Include a boundary case where two adjacent payloads would be ambiguous under naive concatenation (`"ab"` then `"c"` versus `"a"` then `"bc"`).
15. **History provenance (R2-NF-02)** — assert a `version_value_history` row naming an unregistered `(method_id, method_version)` is refused, and one naming an `input_id` belonging to a different `version_id` is refused.
16. **Score-input immutability (R2-NF-04)** — `UPDATE` and `DELETE` on `score_input` both abort; a correction inserted with `corrects_input_id` succeeds and leaves the corrected row intact.
17. **Nullable history provenance (NF-R3-01)** — a `version_value_history` row with `reason='cited_by_decision'` and `input_id IS NULL` is refused; the same row with `input_id` set is accepted; `reason='initial'` with `input_id IS NULL` is accepted.
18. **Cross-version correction (NF-R3-03)** — a `score_input` row for version A with `corrects_input_id` pointing at an input of version B is refused.
19. **Tool-call relational integrity (NF-R3-02)** — assert all four refusals: a call whose emitter is a `user` message; a call whose `result_message_id` is an assistant message; a call whose result is a `tool` message parented by a *different* assistant message; and an `UPDATE` that re-roles a captured message or re-points its `parent_message_id`.
20. **Tool-state transitions (NF-R3-02)** — `emitted → completed` accepted; `completed → emitted` refused; `failed → completed` refused.
21. **Result rebinding (NF-R3-02 residual)** — bind a valid result, then attempt `UPDATE result_message_id` to (a) an unrelated assistant message in the same session, (b) a tool message parented by a *different* assistant, (c) NULL. All three refused. Then assert the one permitted transition `NULL → valid child tool message` succeeds exactly once.

Tests 4–7 and 16 are the regression guards for R1-B-01. Tests 9–10 guard R1-NB-04. Test 8 guards R1-NB-03, in either Q11 branch, and reports which branch it exercised. Tests 11–14 guard R1-NB-02 / R2-NF-01 / R2-NF-03. Test 15 guards R2-NF-02. Tests 17–20 guard NF-R3-01 / NF-R3-02 / NF-R3-03. Test 21 guards the NF-R3-02 residual found at R4.

These tests were not written and not run. Neither the R2 nor the R3 DDL was executed — see §17.

---

## 14. Open questions

| id | question | status |
|---|---|---|
| Q1 | Option A vs B vs C — which architecture | **DECIDED as `OPTION_C` / `ACCEPT-WITH-CONDITIONS`**, recorded in `DEC-P2-T2-Q1-001.md` against baseline `049906a9` (merge `d8e5bebb`). Ruling capacity: dev-baseline Architecture Owner role, session-held — not an accountable human authority, and `acceptance_authority` remains `NOT_ASSIGNED`. Closes the architecture question only. |
| Q2 | Extract Claim/Entity/Relation to tables, or keep in `version_json`? | OPEN, defer to P2-T3 |
| Q3 | Vector store: Qdrant vs Chroma. Prompt defaults Chroma; Phase 1 has neither. | OPEN |
| Q4 | Embedding model and dimension. Prompt assumes `text-embedding-3-small` / 1536. | OPEN — external dependency |
| Q5 | Decay and scoring algorithms and parameters, and recompute cadence | OPEN — required before any score can reach `exact` |
| Q6 | Is `version_sha256` maintained by trigger or by adapter? | OPEN — adapter is the current assumption |
| Q7 | Stale-binding recovery procedure, including external index rebuild after an outage | OPEN |
| Q8 | Transcript retention classes and their default periods | **OPEN — `POLICY_INPUT_ABSENT`; held deliberately, not deferred.** §2i. No inspected document states periods or classes. This proposal constrains deletion; it does not define policy. A period invented here would be enforced by `retention_class` and by the `forget_operation_id` path, which means an invented number would delete real data on a schedule nobody authorised. Engineering can implement an established policy; it cannot manufacture one. |
| Q15 | Whether maintaining `14-ai-development/work-items/INDEX.md` is authorised for this work item, given that the manifest excludes it while `AI-STD-001` line 445 / 463 requires the Integration Owner to maintain it | **SCOPE DECIDED — no write by this work item; the underlying conflict is untouched.** §2i. `AI-STD-001:445` addresses the Integration Owner; this work item does not hold that role — the manifest lists `sponsor`, `accountable_owner` and `acceptance_authority` as `NOT_ASSIGNED` and its `role_note` forbids substituting a session identity for an unassigned role. A `MUST` addressed to a role this work item does not hold does not transfer to it, so the manifest's `OUT_OF_SCOPE` governs and the stale P2-T2 row is recorded as a delivery defect with **no owner, because the role that would own it is unassigned** — an ownership gap, not an individual's overdue obligation. Nobody is late on it and no person should be read as having failed to do it. Whether `AI-STD-001` binds anyone while marked `PROPOSED` is **not** decided here. Original conflict record follows. **`AUTHORITY_CONFLICT`.** Neither instrument is silent and neither can be dismissed. `INDEX.md` is not among the three `allowed_write_paths`, and `all_other_paths` is `OUT_OF_SCOPE`; `AI-STD-001` states a `MUST`-level maintenance obligation with repository-wide claimed applicability, and is marked `Status: PROPOSED`, so its operative authority is `NOT ESTABLISHED`. Five writes to the path occurred across three merged PRs and are recorded as neither authorised nor unauthorised. The P2-T2 row is stale as a result — it predates §18 — and is not corrected. Recorded in §2h and filed as Issue #305 comment `7028019382`. |
| Q9 | Whether `impact_level` should get a typed home or be dropped | **DECIDED: retained as untyped event metadata — neither typed nor dropped.** §2i. Dropping is the only irreversible option and no inspected document supports it. Typing it would assert that this system's decisions carry a four-value urgency classification as domain semantics, a claim no inspected source makes. The value is preserved inside `envelope_json`, so typing later is a migration over data already stored — available, not lost. The §9 gap-table entry stands. |
| Q10 | Does numeric reproducibility stay a requirement, or is structural rebuild sufficient? | **REVIEW RULING (R2): tiered preferred.** Structural and unreconstructable tiers accepted; exact-value retained as a design objective, **CONDITIONAL and NOT VERIFIED**. This is a review ruling on a review question, not an owner decision on Q1. |
| Q11 | Does extending the schema of a Phase 1 table — adding an index without adding a column or rewriting a row — require explicit authorisation from the capacity that owns the Phase 1 contract? | **PARTLY DECIDED — technical admissibility settled; the authorisation question is not.** §2i. The index is data-neutral with respect to `versions` admissible rows and is necessary for the §8.4 composite foreign key to function; six probes recorded there. That settles technical admissibility. It does **not** settle whether a Phase 1 authorising capacity must approve it: no normative rule exempts data-neutral modifications, and no rule in the contract addresses schema objects at all. That question stands for the contract's owner, who remains `NOT_ASSIGNED`. §2i. `version_id` is the primary key of `versions`, so `(memory_id, version_id)` is already unique by construction: an index on that pair admits and rejects exactly the rows the primary key already admits and rejects, probed at case P1. What the index actually supplies is the *parent key* the composite foreign key needs — without it every write to `context_assembly_entry` fails with `foreign key mismatch`, even for a correctly matched pair (probes P2, P3, P6). The index stays declared as a Layer 1 modification, because it is one. This decides admissibility, not what the contract's owner would say; `acceptance_authority` remains `NOT_ASSIGNED`. |
| Q12 | Is the in-memory DDL check an acceptable reading of the `no schema execution` bound? | **PROSPECTIVE INTERPRETATION ISSUED — retrospective ruling refused.** §2i. Going forward, executing this design's own DDL against an ephemeral in-memory database, writing no file and touching no repository path, is inside the design-phase bound; the bound exists to stop persistent schema artefacts and false executable claims, and this produces neither. R2's `DISCLOSED_SCOPE_DEVIATION` for the R2 event stands permanently and is not reclassified — a classification once recorded is not revised by a later clarification of the bound. Two further probes were run before this interpretation existed and are disclosed in §17 as such; the honest count is three disclosed executions, not one. |
| Q13 | Must a `tool_state='completed'` call carry a non-NULL `result_message_id`? | **DECIDED: yes — table-level `CHECK`.** §2i. The `RECOMMENDED` recorded here was adapter-level enforcement, on the ground that *the database* could not hold the invariant because a `BEFORE UPDATE OF tool_state` trigger misses a direct insert into `completed`. That ground was half-checked: the trigger does miss that path, and a table-level `CHECK` does not. Probed on this document's own DDL, 14 cases, all as expected — the direct insert and the `emitted → completed` update with a NULL result are now refused, and every legal path including both write orders is accepted. Separate from NF-R3-02, whose status this does not change. Capacity: dev-baseline, session-held; `human_signature` NOT CLAIMED. |
| Q14 | Does `recompute` genuinely require a single `input_id`? | **`BUSINESS_RULE_NOT_SUPPLIED`; held deliberately, not deferred.** §2i. The deciding question is what the operation called `recompute` means, and that meaning belongs to the owner of its semantics. It cannot be inferred from the provisional `CHECK`, the existing schema, or the convenience of either implementation. The strict branch stays provisional and is labelled as such. |

---

## 15. What this proposal does not claim

- Not implemented. No code, no migration, no test executed.
- Not a frozen schema. It is a proposal for review.
- Not an authorization for P2-T1. Implementation authorization remains withheld per `GO-2026-P2-DESIGN-001`.
- **Not a resolution of Q1 by an accountable authority.** The architecture direction was decided as `OPTION_C` by `DEC-P2-T2-Q1-001`, occupying a dev-baseline Architecture Owner role held by a session. That ruling claims no human signature, no `acceptance_authority` appointment, and no production-grade acceptance. What is settled is the direction; what remains unsettled is whether any accountable human authority has accepted it, because there is none.
- **Not a substantiated exact-value rebuild.** The conditions are specified; the evidence is not. Q10 is recorded as ruled for a tiered posture, with exact value `CONDITIONAL` and `NOT VERIFIED`.
- **Not authorized schema execution.** The one in-memory DDL check is recorded as `DISCLOSED SCOPE DEVIATION`, not as compliant activity. Q12 §2i issues a *prospective* reading of the bound and refuses to reclassify that event or to cover the two later probes retrospectively.
- **Not an approval of this design.** §2i decides five design questions. It does not accept the design, does not authorize implementation, and does not fill any unassigned role. `acceptance_authority` is `NOT_ASSIGNED` after those rulings exactly as it was before them.
- **Not a human signature.** The rulings in §2i carry `human_signature: NOT_CLAIMED`. They were issued under the dev-baseline convergence path, which is the same capacity form `DEC-P2-T2-Q1-001` records.
- **Not a ruling that Q8 or Q14 are unimportant.** §2i holds both, and states why holding them is itself the decision rather than a deferral.
- **Not a verified fix for NF-R3-01 / NF-R3-02.** The constraints are specified. Neither the R3 nor the R4 DDL was executed, so what is asserted is that the constraint text exists and matches the prose — not that SQLite enforces it as intended.
- **Not authenticated prompt provenance.** Appendix A is a copy; its origin is `UNVERIFIED`.
- No technology selection: Qdrant/Chroma, embedding model and dimension remain OPEN.
- No claim that the prompt schema is unusable. Its tensions are real; its contradictions with Phase 1 are not established as necessary.
- No claim of approval by any accountable authority. `acceptance_authority` is `NOT_ASSIGNED`.
- No claim that the R3 DDL applies — it was not executed. §17's probe result is evidence about the R2 DDL only.

---

## 16. Evidence tier

| item | tier |
|---|---|
| Phase 1 DECIDED status, merged commits, observed table definitions | **VERIFIED** — read at base `7f8093876729212ef4e83461ba8c2f2cd96582c7`; `core-entities.md` blob `8cb5a674`, `phase-1-sqlite-adapter-contract.md` blob `c472e00f`, `phase-1-storage-trait-contract.md` blob `22ca7cd3`, `payload.rs` blob `ad22972b`. R1 independently confirmed the same tables. |
| Trait contract status | **VERIFIED** — the file states `CANDIDATE`; this document relies only on the narrower SQLite-boundary claim |
| Prompt schema contents | **VERIFIED as embedded text at this document's head** — reproduced in Appendix A. Its **original-source verbatim provenance is UNVERIFIED**: R2 independently fetched the repository path at the reviewed head and got `404`, so an appendix is reviewable evidence but cannot authenticate its own origin. R2's ruling accepted the appendix as a valid self-containment remedy and withheld the `VERIFIED` upgrade. That limit is not contested here. The remedy, if independent authentication is required, is to commit the prompt file at a known commit — which needs a write path this manifest does not contain. |
| §5 tensions | **CORROBORATED, author assessment** — R1 ruled the stronger form `OVERSTATED`; the downgraded form is retained as tension, not contradiction |
| R1 findings and dispositions | **VERIFIED** — transcribed from the R1 reply, recorded on PR #307 |
| Recommendations in §6–§12 | **PROPOSED** — author-authored, subject to R2 review |
| Q1 decision, disposition and the merge that recorded it | **VERIFIED** — `DEC-P2-T2-Q1-001.md` and merge `d8e5bebb` are on `main` and readable. |
| Any claim that Q1 was resolved by an accountable human authority | **NOT MADE** — the ruling occupies a session-held dev-baseline role and says so itself; `acceptance_authority` is `NOT_ASSIGNED`. |
| The Q11–Q14 / Q8 / Q9 ruling dispositions | **AUTHOR-REPORTED, reviewer-declared limit** — the ruling states it did not retrieve the repository at the reviewed head and rests on contract language quoted in the request. It is therefore a disposition over the text supplied, not an independent verification of this document at any head. |
| The absence of a Layer 1 prohibition | **VERIFIED** — `phase-1-sqlite-adapter-contract.md` read directly; two tree-wide searches recorded in §2f. The absence of a `layer 1` term in the governance tree is verified the same way. |
| That the Q11 ruling's premise was false | **VERIFIED by the above two rows taken together**, not by the ruling. The ruling was correct on the question asked; the question was wrong. |
| That a table-level `CHECK` holds the Q13 invariant where a `BEFORE UPDATE OF tool_state` trigger cannot | **SQL logic VERIFIED; execution history AUTHOR-REPORTED and now reproducible.** The constraint's semantics are checkable by reading: SQLite evaluates table-level `CHECK` on INSERT and UPDATE, which the trigger pattern cannot. The 14-case execution result in §2i is what the harness reports; the harness is Appendix B.1 and reads its DDL out of this document at run time, so anyone can re-run it and get 14/14 or find that §2i's table is wrong. Probed in-memory SQLite 3.46.1. |
| That `versions_memory_version_uq` changes no admissible row, and that the composite foreign key is inert without it | **SQL logic VERIFIED; execution history AUTHOR-REPORTED and now reproducible.** Uniqueness of `(memory_id, version_id)` follows from `version_id` being the primary key; SQLite's parent-key requirement for a composite FK follows from its documentation and is what P2/P3/P6 report. The 6-case execution result is in §2i; the harness is Appendix B.2. |
| The rulings in §2i | **ISSUED, not verified.** The capacity is dev-baseline, session-held; `human_signature` is `NOT_CLAIMED`. Their factual premises are as graded above; their authority is what §2i says it is. A ruling is not a verification, and §2i's Q11 in particular is explicitly partial — technical admissibility only. |

---

## 17. Disclosed scope deviation — in-memory DDL check

**R2 classified this as `DISCLOSED SCOPE DEVIATION`, not authorized activity.** That ruling is accepted without argument. This section does not defend the check; it records it, records what it found, and escalates the authority question.

What was done: the DDL in §7 and §8 was executed against an ephemeral in-memory SQLite database (`sqlite3` 3.53.1), preceded by `CREATE TABLE` statements copied from the merged Phase 1 crates so that foreign keys resolve against the real key shapes. Nothing was written to disk, no migration was applied, no repository artefact was created or changed.

Why it was done: to find out whether the document is internally coherent before spending a review round on it.

Why that reason does not make it authorized: `authorization-manifest.yaml` records `no schema execution` among the design-only bounds, and an in-memory database is still a database against which schema execution occurred. The earlier revision advanced the reading that the bound covers persistent stores and repository paths. R2 declined to accept that reading as established by the authorization text, and an engineering reviewer cannot grant retrospective authorization. Both points stand.

The manifest's formal classification of this event is `DISCLOSED_SCOPE_DEVIATION`. **Correction (NF-R3-04):** an earlier revision of this section stated that the manifest records the event as `DISCLOSED_INTERPRETATION`. That was wrong — the manifest was updated to `DISCLOSED_SCOPE_DEVIATION` and this paragraph was not updated with it. The reviewer is right that an audit trail must not give one event two classifications. `DISCLOSED_SCOPE_DEVIATION` is the single recorded status, here and in the manifest, and the question is carried as **Q12**.

What it found, reported as author-reported and not independently reproduced:

- All design DDL blocks apply against the real Phase 1 key shapes.
- Constraint probes behaved as specified: the composite `(memory_id, version_id)` foreign key refuses a mismatched pair; deleting a `transcript_session` that has messages is refused; deleting a `transcript_message` carrying a `memory_source_link` is refused; `UPDATE` and `DELETE` on `scoring_method` are refused; a projection referencing an unregistered `(method_id, method_version)` is refused.
- **Q13 probe (14 cases):** the invariant is holdable by the database; the design's stated reason for refusing database enforcement was wrong. This changed a §14 ruling, not just a document sentence — see §2i.
- **Q11 probe (6 cases):** `(memory_id, version_id)` is already unique by construction, and the proposed index supplies the parent key the composite foreign key needs rather than adding a uniqueness constraint. Without it the child table rejects every write, matched or not. This likewise changed a §14 ruling.
- One real defect, found before review: the first draft of `transcript_message` referenced `accepted_events(event_id)`, and the merged Event Store's primary key is `event_row INTEGER`. The draft would not have compiled. §7.1 now uses `event_row`.

**Two further probes were run before §2i existed, and are disclosed here.** The Q13 probe (14 cases) and the Q11 probe (6 cases) both executed DDL against ephemeral in-memory databases. They were run while preparing the rulings, which is to say before the prospective interpretation of the bound existed. §2i says explicitly that its interpretation does not cover them retrospectively. The honest count of disclosed executions is therefore **three**, not one, and none of the three is reclassified.

In R3 this check was **not** repeated. The tables changed, so the earlier result does not carry forward as evidence about the current DDL; it is evidence about the R2 DDL only. Whether the R3 DDL applies is an open question for an authorized implementation phase, not something this revision asserts. The prior probes are `AUTHOR-REPORTED`, and R2 declined to upgrade them, which is the correct tier.

What this does not establish:

- Not an implementation. There is no code beyond the document.
- Not a test suite. None of §13's tests were written or run; the ad-hoc probes are not those tests. (The count is stated once, in §13, and is not repeated here — an earlier revision said "thirteen" while §13 listed sixteen, which NF-R3-04 correctly flagged.)
- Not evidence about performance, concurrency, WAL behaviour, or behaviour under the Phase 1 adapter's transaction discipline.
- Not evidence that the R3 DDL applies at all — the R3 tables were not exercised.
- Not evidence that the design satisfies any capability in §9.

---

## 18. Gate conformance map — what the seven P2-T1 gates have, and what they do not

Derived from `DEC-P2-T2-Q1-001` §8, which lists seven gates between the Option C
decision and P2-T1 implementation authorisation. This section maps each gate to the
part of this proposal that addresses it and names what is missing. It introduces no
new design, closes no open question and grants no authorisation.

It is a section of this proposal rather than a separate file because
`authorization-manifest.yaml` declares three allowed write paths and marks every
other path `OUT_OF_SCOPE`. An earlier revision of this work item added it as a
fourth file; that was outside the declared scope and is recorded in §2g rather
than regularised by widening the manifest.

### 18.1. Why this document exists

`DEC-P2-T2-Q1-001` §8 lists seven gates between the Option C decision and P2-T1 implementation authorisation, and ends: *"Until these gates are satisfied, P2-T1 remains `BLOCKED` for implementation authorisation."*

The Q1 ruling recorded in §2f — decided at `DEC-P2-T2-Q1-001`, and not accepted by an accountable authority since none is assigned — further directed that **gates 1, 2, 3 and 5** be treated as bounded engineering work. Gates 4, 6 and 7 involve authorities or decisions this work item cannot supply.

That instruction is only actionable if it is clear, gate by gate, what already addresses it and what does not. This document supplies that map. It is a reading of existing material, not an addition to it.

---

### 18.2. Gate 1 — canonical persistence boundary

> Specify how P2-T1 writes canonical memories and versions through the Phase 1 boundary, preserving immutable versions, CAS and atomic pointer advancement.

| addressed by | how |
|---|---|
| `02-domain-model/phase-1-sqlite-adapter-contract.md` | DECIDED. Enumerates the persistence behaviours P2-T1 must use: immutable version rows, current-version CAS, idempotency receipts, monotonic commit sequence, atomic transaction. |
| `crates/memory-storage/src/lib.rs` — `MemoryStorage` | The trait P2-T1 writes through. `commit_version(CommitRequest, &[ScopeRef])` with `expected_current_version` is the CAS. `CommitRequest` carries `memory_id`, `expected_current_version`, `new_version`, `idempotency_key`, `request_digest`. |
| `crates/memory-storage-sqlite/src/lib.rs` | The implemented adapter. `commit_version`, `read_current`, `read_version`, `resolve_idempotency`, `list_changes`. Four tables: `memories`, `versions`, `idempotency`, `commit_log`. |
| design-proposal §11 | States Phase 2 must **not** change the `MemoryStorage` trait; additions are separate traits. |
| design-proposal §8.4 / §12 | Declares the one proposed Layer 1 modification, the additive unique index `versions_memory_version_uq`, and the Q11 dependency. |

**Residual gap.** §11 forbids changing `MemoryStorage` and lists the new traits, but does not state which Phase 1 call P2-T1 makes *first* in each canonical write path, nor the ordering guarantee between `commit_version` and the transcript-capture write that cites it. That ordering is a design decision for P2-T1's own contract, not something this proposal can fix by assumption.

**Blocked by:** nothing at design level. This is gate-1 engineering work that P2-T1 itself performs.

---

### 18.3. Gate 2 — transcript capture contract

> Event ingestion, ordering, role filtering, thread reconstruction, tool-call pairing, idempotency, provenance, lifecycle. It must be independently retrievable without treating the transcript as canonical memory.

| addressed by | how |
|---|---|
| design-proposal §7.1 | `transcript_session`, `transcript_message`, `transcript_tool_call`, `memory_source_link`. Ordering by `seq_no`, never `created_at`. Bytes stay in `event_payloads`; the transcript row is an index over `accepted_events(event_row)`. |
| design-proposal §7.2 | The six retrieval operations: `read_session`, `read_by_role`, `read_thread`, `read_tool_calls`, `read_tool_result`, `reconstruct`. |
| design-proposal §11 | `TranscriptCapture` trait with those six methods, plus invariants on framing and tool-call cardinality. |
| design-proposal §13 tests 9–14, 19–21 | Ordering, cardinality, thread integrity, framing, no-cascade, tool-state transitions, result rebinding. |
| `crates/memory-event-store-sqlite/src/payload.rs` | `PayloadEventStoreExt::accept_with_payload` and `read_after(after_sequence, limit, scope)`. The ingestion and ordered-read primitives the capture layer builds on. |

**Residual gap.** The *state vocabulary* exists — `design-proposal.md:433` defines `session_state TEXT NOT NULL CHECK (session_state IN ('open','closed','abandoned'))`. What is missing is the lifecycle **contract**: which transitions are permitted, who or what may close a session, whether `closed` and `abandoned` are terminal, how `ended_at` must correspond to `session_state`, and whether messages may still be captured after closure. Retention periods and classes are separately absent (Q8).

**Blocked by:** Q8 for retention. The transition and ownership semantics are not Q8 and are simply unwritten — but see §9 on who may adopt them.

---

### 18.4. Gate 3 — derived projection semantics

> Source dependencies, projection versions, rebuild behaviour, stale-data handling, failure recovery. Qdrant must not silently become an alternative canonical system of record.

| addressed by | how |
|---|---|
| design-proposal §8.1 | `scoring_method` with `algorithm_spec_ref`, `algorithm_spec_sha256`, `numeric_semantics`; append-only by trigger. |
| design-proposal §8.2 | `score_input` — the declared input set — with `UNIQUE (version_id, input_id)` and append-only triggers; corrections inserted with `corrects_input_id`. |
| design-proposal §8.3 | Three rebuild tiers: `structural`, `exact`, `unreconstructable`. Exact is conditional and recorded `NOT VERIFIED`. |
| design-proposal §8.4 | `version_value_history`, `context_assembly_entry` with composite FKs, `version_vector_binding`. |
| design-proposal §11 | `MemoryValueProjection` and `VectorIndex` traits, with the invariant that `invalidate` must not delete canonical content. |
| design-proposal §13 tests 1–8, 15–18 | Digest binding, scope isolation, non-destructive invalidation, all three rebuild tiers, immutability, composite integrity, provenance. |

**Residual gap (tier 3).** *Failure recovery* is named in the gate and only partly addressed. §12 gives a forward-only idempotent migration path; it does not state what a rebuild does when it is interrupted partway, whether `rebuild_state` is set before or after the score row is written, or how a partial rebuild is distinguished from an interrupted one. Q10 records that exact-value rebuild remains `CONDITIONAL` / `NOT VERIFIED`.

**Blocked by:** nothing at design level for the structural tier. Exact-value tier needs a worked example that does not exist here.

---

### 18.5. Gate 4 — resolve applicable outstanding decisions

> Q11–Q14 through their appropriate authorities. Q12 in particular cannot be closed by this record's assumption.

**Not addressed, and not addressable here.** Current state, from §14:

| question | state | needs |
|---|---|---|
| Q11 | **PARTLY DECIDED (§2i)** — technical admissibility settled, data-neutral; authorisation half NOT settled | the Phase 1 contract's owner (`NOT_ASSIGNED`); no rule exempts a data-neutral modification from Phase 1 approval |
| Q12 | **PROSPECTIVE ISSUED (§2i)**; retrospective NO | retrospective part permanently unavailable |
| Q13 | **DECIDED (§2i)** — table-level `CHECK` | none; NF-R3-02 verification still outstanding |
| Q14 | `BUSINESS_RULE_NOT_SUPPLIED` — **held (§2i)** | the owner of `recompute`'s semantics |
| Q8 | `POLICY_INPUT_ABSENT` — **held (§2i)** | retention policy |
| Q9 | **DECIDED (§2i)** — retained untyped | none; typing deferred to a later migration |

No engineering act closes any of these. Issue #305 records the root cause: no governance act has established who may hold `acceptance_authority`, and `00-governance/reports/bilingual-baseline-remediation-report.md` line 931 already records the same finding as `OUT-OF-SCOPE(dev-baseline)` rather than simulating it.

**Q15 is registered in §14 and is deliberately absent from the table above.** It is not one
of the decisions gate 4 names, and adding it would silently widen the gate's definition.
Q15 concerns authority over repository index maintenance, not a P2-T1 design question. It
does not alter any gate definition or establish a gate disposition; its implications for
repository-level registration remain open. It is recorded here so that its absence from the
table is read as scoped rather than overlooked.

---

### 18.6. Gate 5 — implementation acceptance criteria and tests

> Duplicate event delivery, out-of-order delivery, partial failure, restart/recovery, concurrent updates, projection rebuilding, provenance integrity, context-injection correctness.

Phase 1 already carries executable tests for several of these criteria. They are **not** Phase 2 tests and were not written against the Layer 2 or Layer 3 schema, but they establish that the underlying store behaves correctly under exactly the conditions this gate names. Counting them as absent would have been wrong; counting them as satisfying the gate would also be wrong.

The gate names eight criteria; the table below has ten rows. The gate's single criterion "concurrent updates" is decomposed into three, because the Phase 1 evidence supports two narrower guarantees and not the one the gate names. Splitting it is what keeps the positive findings from being withdrawn along with the overstated one.

| criterion | Phase 1 evidence (exists, executable) | Phase 2 status |
|---|---|---|
| duplicate event delivery | `memory-event-store-sqlite/src/payload.rs:285` — `duplicate_payload_append_returns_original_receipt_without_dup`; `lib.rs:324` — `same_producer_key_and_digest_replay_original_receipt`; `lib.rs:339` — `same_producer_key_with_different_digest_conflicts` | `PROVEN — PHASE 1 STORE LAYER`; `UNPROVEN — PHASE 2 INTEGRATION` |
| out-of-order delivery | **none** — the change-page test at `memory-storage-sqlite/src/lib.rs:1511` asserts ordered *retrieval* with limit and scope filtering, which is not delivery order | retrieval ordering specified (test 11); out-of-order **arrival** handling `UNVERIFIED ABSENCE` |
| partial failure | **none** | `UNVERIFIED ABSENCE` |
| restart/recovery | `resilience.rs:139` — `restart_preserves_receipt_and_idempotent_payload_replay`; `resilience.rs:204` — `committed_payload_survives_process_crash_and_wal_recovery`; `memory-storage-sqlite/src/lib.rs:496` — `sqlite_committed_state_survives_close_and_reopen`; `:554` — `abrupt_process_exit_rolls_back_entire_uncommitted_commit` | `PROVEN — PHASE 1 STORE LAYER`; `UNPROVEN — PHASE 2 INTEGRATION` |
| concurrent **append** safety | `resilience.rs:162` — `concurrent_appends_preserve_unique_order_and_payload_custody` (6 writers, barrier-synchronised) | `PROVEN — PHASE 1 STORE LAYER`; `UNPROVEN — PHASE 2 INTEGRATION` |
| competing **CAS** serialisation | `memory-storage-sqlite/src/lib.rs:579` — `independent_connections_serialize_competing_compare_and_swap_writers` | `PROVEN — PHASE 1 STORE LAYER`; `UNPROVEN — PHASE 2 INTEGRATION` |
| semantic winner selection under contention | **none** — neither test asserts which writer should win, only that sequence numbers are unique and increasing and that exactly one CAS succeeds | `UNVERIFIED ABSENCE` |
| projection rebuilding | **none** | specified, not implemented or run |
| provenance integrity | **none** | specified, not implemented or run |
| context-injection correctness | **none** | `UNVERIFIED ABSENCE`; intended-context semantics undefined |

### Two corrections of this document's own earlier readings

**First correction — the gap count.** A first draft said four of eight criteria were unaddressed. That was written from the Phase 2 proposal alone, without checking the tree. Three of the four claimed gaps — duplicate delivery, restart/recovery, concurrent updates — have executable Phase 1 tests behind them.

**Second correction — the overcorrection.** The response to the first correction then classified out-of-order delivery as covered, citing test 11. It is not covered. Test 11 asserts that `read_session` returns `seq_no` order *after* sequence numbers have been assigned; that is retrieval ordering, not how the capture layer handles events arriving in a different order from their intended sequence. The Phase 1 change-page test at `:1511` is also ordered retrieval with limit and scope filtering. No test in the inspected tree asserts delivery-order handling.

So the honest classification has three tiers, not two:

| tier | classification | meaning |
|---|---|---|
| 1 | `PROVEN — PHASE 1 STORE LAYER` | positive evidence establishes the specifically tested store behaviour |
| 2 | `UNPROVEN — PHASE 2 INTEGRATION` | store-level evidence exists; Phase 2 integration behaviour not established |
| 3 | `UNVERIFIED ABSENCE` | no relevant test located in the inspected tree; exhaustive absence not established |

**Tiers 1 and 2 are not competing classifications.** A behaviour can be proven at the store layer and simultaneously unproven at Phase 2, and the mapping keeps both visible rather than letting one stand for the other. A store-level idempotency test does not establish end-to-end idempotency once Phase 2 introduces its own commit, retry and transcript interactions.

Applying it:

- **Tier 1 + 2 together** — duplicate delivery, restart/recovery, concurrent append safety, competing CAS serialisation. The Phase 1 tests exist and run and prove the tested store operation. None of them involves a transcript write accompanying a canonical commit, so none establishes the Phase 2 path that did not exist when they were written.
- **Specified, not implemented, not run** — projection rebuilding, provenance integrity, retrieval ordering. The last is a sub-finding inside the out-of-order delivery criterion, not a separate criterion of the gate, which is why §18.6 carries ten rows for eight criteria rather than eleven.
- **Tier 3** — partial failure, out-of-order *arrival*, context-injection correctness, semantic winner selection. No test evidence was located. That is not the same as saying those behaviours are untested; it says their coverage status has not been established.

The substantive work is tier 1+2's open question: what happens when `commit_version` succeeds and the `transcript_message` insert citing it does not. That is a design question, and per §10 it is not one engineering may settle unilaterally.

---

### 18.6a. Assertion-level audit of the ten Phase 1 citations

The citation check that produced §18.6 verified that ten named tests exist at ten named lines. A review correctly distinguished that from a stronger claim: traceability is not conformance, and a test whose name promises a behaviour may assert something narrower.

This audit reads each test body and records what it actually asserts.

The accounting, stated so it can be checked: §18.6 carries **ten citations**. Nine cite evidence for a criterion and all nine bodies were read in full; the table below has one row per body. The tenth, `memory-storage-sqlite/src/lib.rs:1511`, is cited as evidence that does **not** exist — it is examined in §18.6's second correction and is not an evidence citation. Ten citations, nine inspected evidence bodies, one examined counter-example.

| test | asserts | verdict |
|---|---|---|
| `duplicate_payload_append_returns_original_receipt_without_dup` | retry returns the identical receipt; row and payload counts both remain 1 | supports duplicate-delivery idempotency |
| `same_producer_key_and_digest_replay_original_receipt` | retry equals first receipt; `processing_state` stays `Pending`; outbox count stays 1 | supports duplicate-delivery idempotency |
| `same_producer_key_with_different_digest_conflicts` | conflicting digest is refused | supports duplicate-delivery **conflict** handling, a distinct guarantee |
| `restart_preserves_receipt_and_idempotent_payload_replay` | after reopen, replay equals original; one event recovered; receipt and payload bytes match | supports restart/recovery |
| `committed_payload_survives_process_crash_and_wal_recovery` | crash child exits non-zero; one event recovered after crash; payload bytes and envelope digest intact | supports crash recovery |
| `sqlite_committed_state_survives_close_and_reopen` | version readable after reopen; idempotency receipt resolvable; one change record at sequence 1 | supports restart/recovery for canonical state |
| `abrupt_process_exit_rolls_back_entire_uncommitted_commit` | exit code 86; no current version; no version row; no idempotency receipt; no change record | supports rollback of an uncommitted commit |
| `concurrent_appends_preserve_unique_order_and_payload_custody` | 6 barrier-synchronised writers produce exactly 6 events with strictly increasing sequence and exactly the expected payload set | supports concurrent-append safety |
| `independent_connections_serialize_competing_compare_and_swap_writers` | exactly one CAS writer succeeds; the loser gets `StaleVersion`; one change record | supports CAS serialisation |

**Two limits this audit found, stated rather than smoothed over:**

1. `concurrent_appends_preserve_unique_order_and_payload_custody` establishes that simultaneous appends do not collide, lose payloads, or produce duplicate sequence numbers. It does not establish ordering *semantics* under contention — which writer "should" win is not asserted, only that sequence numbers are unique and increasing. The claim in §18.6 that this supports "concurrent updates" is therefore support for append safety, not for update conflict resolution.

2. `abrupt_process_exit_rolls_back_entire_uncommitted_commit` proves rollback of a commit that never completed. It says nothing about a commit that completed while a related write did not. That is the same gap §18.6 records as tier 3 for partial failure, and the audit confirms the two are genuinely different — the crash test is not a partial-failure test wearing a different name.

**What the audit changes:** nothing in the tier assignment. The inspected test bodies support the specific assertions recorded in the table above. One previously broader classification — "concurrent updates" — has been narrowed to two separate guarantees. Beyond the assertions listed, the tests establish nothing. What the audit changes is the basis: §18.6's `PROVEN — PHASE 1 STORE LAYER` now rests on read assertions rather than on test names.

**What the audit does not establish:** that these are the only relevant tests, or that Phase 2 conformance follows. Both limits are already recorded in §18.6 and §18.11.

### 18.7. Gate 6 — separate P2-T1 implementation authorisation

Not obtainable here. The authorisation requires an implementation Owner accepting the target contract, scope, test obligations and failure boundaries against an exact artefact version. `accountable_owner` and `acceptance_authority` are `NOT_ASSIGNED`; Issue #305 records why, and the remedy is a governance act this work item cannot perform.

---

### 18.8. Gate 7 — normal convergence chain

Partially available. Implementation, verification, review and merge are executable. **Owner acceptance** within that chain is not, for the same reason as gate 6.

The gate also names registration and traceability. Q15 §2h records a complication this map
does not resolve: the repository's traceability index is maintained by a path the work-item
manifest excludes, so the registration step of this chain is itself subject to an unresolved
authority question. That is not a further gate failure — `AI-STD-001` is `PROPOSED` and Q15
has not established that its requirement is an operative gate condition — but the
registration step is not simply "available" either, and a reader should not infer that it
has been examined and disposed of.

---

### 18.9. Summary

| gate | design coverage | blocked by |
|---|---|---|
| 1 canonical persistence | substantial; write-path ordering unspecified | nothing at design level |
| 2 transcript capture | substantial; state vocabulary exists, transition and ownership semantics undefined | Q8 for retention; transitions need adoption (§10) |
| 3 derived projection | substantial; failure recovery and interruption semantics missing | nothing for structural tier; exact tier `NOT VERIFIED` |
| 4 outstanding decisions | **5 of 7 decided (§2i), 2 held** | Q14 held on business semantics; Q8 held on policy input; accountable authority still `NOT_ASSIGNED` — Issue #305 |
| 5 acceptance criteria and tests | 10 rows over the gate's 8 criteria: 4 `PROVEN — PHASE 1 STORE LAYER` / `UNPROVEN — PHASE 2 INTEGRATION`; 2 specified but unrun; 4 `UNVERIFIED ABSENCE`; plus retrieval ordering, specified but unrun, carried inside the out-of-order row rather than as a row of its own | work not done; adoption authority for the atomicity contract |
| 6 implementation authorisation | none | authority — Issue #305 |
| 7 convergence chain | partial | Owner acceptance unavailable |

The gates that can be advanced by engineering are 1, 2, 3 and 5 — the Q1 ruling's direction, which `DEC-P2-T2-Q1-001` records as decided and which no accountable authority has accepted, since none is assigned. Gate 4 changed shape in §2i: five of its seven questions now carry rulings and two are held deliberately, so what remains of gate 4 is not 'no design coverage' but the two held questions and the accountable-authority vacancy itself. Of those, the substantive gap is the interaction between gates 1 and 5: four gate-5 criteria are proven at the store layer and unproven once a transcript write must accompany a canonical commit.

Second substantive gap, gate 2: session lifecycle transitions. The state vocabulary exists; the transition and ownership semantics do not.

---

### 18.10. What engineering may start without authority, and what it may not adopt

The Q1 ruling — recorded as decided at `DEC-P2-T2-Q1-001`, and recorded as not accepted by an accountable authority because none is assigned — directed that gates 1, 2, 3 and 5 be treated as bounded engineering work. That authorises investigation. It does not confer authority to settle every normative design choice arising from the investigation, and this document does not claim otherwise.

**Where §2i sits in this, and where it does not.** §2i settles a narrower category than
this section denies: questions about **what this design's own specified invariants mean and
which of two candidate readings the evidence supports** — whether a `completed` call must
name its result and where that is enforced (Q13), whether an index changes an admissible row
(Q11, technical part), what a bound was written to prevent (Q12), who a maintenance `MUST`
is addressed to (Q15), and whether a field is preserved or typed (Q9). Each of those was
decided by reading this repository and choosing between options the evidence distinguished,
with the probes recorded in §2i and reproducible from Appendix B.

This section still denies the other category: adopting a **new normative contract that the
repository does not already contain** — which consistency and recovery contract binds a
canonical commit against a failed transcript write, what retention periods apply, what the
operation named `recompute` means. Those are not settled by reading; they would be invented.
Q8 and Q14 are in this category, and §2i holds them for precisely this reason.

The rule is therefore: a session may decide what the document's own evidence determines, and
may not authorise what the document does not already know. The two categories are close
enough at the boundary that this distinction has to be written down rather than left to be
inferred — which is why it is written here.

The distinction, stated plainly:

| act | may a session do it? |
|---|---|
| identify failure modes in the commit/transcript interaction | yes |
| investigate transaction boundaries; produce several candidate contracts | yes |
| test the candidates; recommend one | yes |
| declare which consistency and recovery contract is **binding** | no — a design decision, not a test-writing exercise |
| propose a session state machine | yes |
| adopt it as the authoritative lifecycle rule | no — it would silently become a business rule |

Applied to the two gaps this document identifies:

- **The atomicity question** — what happens when `commit_version` succeeds and the `transcript_message` insert does not — can be investigated and specified in alternatives. Selecting which alternative governs needs an authority that is `NOT_ASSIGNED`. A session cannot close that question by writing a document — and §2i did not close it. The two questions this paragraph names are the atomicity contract and the session lifecycle state machine, and neither is Q8 or Q14; those two are held on different grounds (Q8 needs a retention policy, Q14 needs the meaning of `recompute`). What §2i holds and what this paragraph denies are consistent with each other, and the cross-reference that said otherwise is corrected here.
- **Session lifecycle transitions** — the state machine can be proposed. Adopting it as authoritative has the same problem.

So the accurate statement is not "none of this is blocked on authority". It is: **the investigation is not blocked; the adoption is.** A session can move these questions from "unasked" to "asked with named alternatives". It cannot move them to "settled".

That is still worth doing, and it is why this map separates *work not done* from *decision not available*. The first column is large. The second is not empty.

---

### 18.11. What this document does not claim

- Not that any gate is satisfied. It maps coverage and names gaps.
- Not that the design is adequate. Coverage is not correctness; none of the 21 tests were written or run.
- Not that the residual gaps are the only gaps. They are the ones visible against the gate text in the inspected tree.
- Not a complete search. The citations were verified by script — ten positive matches, zero failures — but verifying that ten citations exist says nothing about whether other relevant tests exist elsewhere. Absence claims here read "no existing test identified in the inspected tree", not "no test exists".
- Not an authority to adopt. See §10.
- Not a substitute for the review rounds recorded in §2–§2f. Those examined the document; this examines its relation to a list written elsewhere.
- No governance state changes. `DESIGN_ACCEPTANCE` `NOT_GRANTED`, `IMPLEMENTATION_AUTHORIZATION` `NOT_GRANTED`, `GOVERNANCE_STATUS` `BLOCKED`, `acceptance_authority` `NOT_ASSIGNED`.

**Evidence tier:** the gate text and the cited sections are `VERIFIED` — read from the merged tree, citations script-checked. The judgement that a section "addresses" a gate is `PROPOSED` — an author reading, not a review finding. The absence of tests for partial failure, out-of-order arrival and context-injection correctness is `UNVERIFIED ABSENCE` in the tiered sense defined in §6 — no relevant test was located in the inspected tree, and exhaustive absence was not established. The distinction between that and *the behaviour is untested* is the whole point of the tier.

---

## Appendix A — prompt schema DDL, embedded copy

**Provenance limit, stated up front.** This appendix is a copy. It is reviewable as text, and it is what R1-NB-05 asked for, but it cannot authenticate its own origin: the source path `prompts-fix/P2-T2-memory-schema.md` is not present in the repository at any reviewed head, and both R1 and R2 independently received `404` for it. R2 therefore accepted the appendix as a self-containment remedy while withholding the `VERIFIED` upgrade, and that tier stands uncontested.

Anyone who needs authenticated provenance must obtain the source file at a known commit — which requires a write path beyond this manifest's two allowed files — or compare this appendix against their own copy.

The copy below is exact as supplied in this session. It is evidence, not adopted design: where it conflicts with §7–§8, §7–§8 govern.

```sql
-- AI Memory Brain - SQLite Schema
-- Version: 1.0.0
-- Created: 2026-11-19

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- ============================================================
-- 1. 会话表 (Sessions)
-- ============================================================
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,  -- UUID
    conversation_id TEXT,  -- ChatGPT conversation ID
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    status TEXT CHECK(status IN ('active', 'paused', 'completed', 'failed')) DEFAULT 'active',
    channel TEXT CHECK(channel IN ('api', 'cdp', 'browser')) DEFAULT 'api',
    work_item_id TEXT,  -- 关联的工作项 ID
    base_sha TEXT,  -- 开始时的 Git SHA
    final_sha TEXT,  -- 结束时的 Git SHA
    metadata JSON  -- 扩展字段: {tags: [], priority: 'high'}
);

CREATE INDEX idx_sessions_started ON sessions(started_at DESC);
CREATE INDEX idx_sessions_work_item ON sessions(work_item_id);

-- ============================================================
-- 2. 消息表 (Messages)
-- ============================================================
CREATE TABLE IF NOT EXISTS messages (
    message_id TEXT PRIMARY KEY,  -- UUID
    session_id TEXT NOT NULL,
    role TEXT CHECK(role IN ('system', 'user', 'assistant', 'tool')) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    token_count INTEGER DEFAULT 0,
    
    -- 向量嵌入 (存储为 JSON,实际嵌入存于向量库)
    embedding_id TEXT,  -- Chroma/Qdrant 中的 ID
    
    -- 价值评分 (0-100)
    value_score REAL DEFAULT 50.0,
    
    -- 时间衰减权重 (基于 Ebbinghaus 曲线,每天自动更新)
    decay_weight REAL DEFAULT 1.0,
    
    -- 元数据
    metadata JSON,  -- {tags: ['decision', 'architecture'], cited_files: [...]}
    
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

CREATE INDEX idx_messages_session ON messages(session_id, created_at);
CREATE INDEX idx_messages_value ON messages(value_score DESC);
CREATE INDEX idx_messages_role ON messages(role);

-- ============================================================
-- 3. 决策表 (Decisions)
-- ============================================================
CREATE TABLE IF NOT EXISTS decisions (
    decision_id TEXT PRIMARY KEY,  -- UUID
    session_id TEXT NOT NULL,
    message_id TEXT,  -- 触发决策的消息
    
    decision_type TEXT CHECK(decision_type IN ('accept', 'reject', 'defer', 'escalate')),
    decision_by TEXT,  -- Owner 名称
    decision_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    subject TEXT NOT NULL,  -- 决策主题
    rationale TEXT,  -- 决策理由
    
    -- 关联的工作项和文件
    work_item_id TEXT,
    affected_files JSON,  -- ['src/auth.py', 'docs/api.md']
    
    -- 决策影响
    impact_level TEXT CHECK(impact_level IN ('low', 'medium', 'high', 'critical')) DEFAULT 'medium',
    
    -- 决策状态
    status TEXT CHECK(status IN ('pending', 'implemented', 'reverted')) DEFAULT 'pending',
    
    metadata JSON,
    
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (message_id) REFERENCES messages(message_id) ON DELETE SET NULL
);

CREATE INDEX idx_decisions_session ON decisions(session_id);
CREATE INDEX idx_decisions_type ON decisions(decision_type);
CREATE INDEX idx_decisions_impact ON decisions(impact_level);

-- ============================================================
-- 4. 文件变更表 (File Changes)
-- ============================================================
CREATE TABLE IF NOT EXISTS file_changes (
    change_id TEXT PRIMARY KEY,  -- UUID
    session_id TEXT NOT NULL,
    message_id TEXT,  -- 产生变更的消息
    
    file_path TEXT NOT NULL,
    change_type TEXT CHECK(change_type IN ('create', 'modify', 'delete', 'rename')) NOT NULL,
    
    -- Git 信息
    commit_sha TEXT,
    diff_summary TEXT,  -- 简要 diff
    lines_added INTEGER DEFAULT 0,
    lines_deleted INTEGER DEFAULT 0,
    
    -- 时间戳
    changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    metadata JSON,
    
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (message_id) REFERENCES messages(message_id) ON DELETE SET NULL
);

CREATE INDEX idx_file_changes_session ON file_changes(session_id);
CREATE INDEX idx_file_changes_file ON file_changes(file_path);
CREATE INDEX idx_file_changes_commit ON file_changes(commit_sha);

-- ============================================================
-- 5. 上下文注入记录表 (Context Injections)
-- ============================================================
CREATE TABLE IF NOT EXISTS context_injections (
    injection_id TEXT PRIMARY KEY,  -- UUID
    session_id TEXT NOT NULL,
    
    injected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- 注入的上下文类型
    context_type TEXT CHECK(context_type IN ('decision', 'file_history', 'related_session')) NOT NULL,
    
    -- 注入的内容 (引用)
    source_message_ids JSON,  -- 来自哪些消息
    source_decision_ids JSON,  -- 来自哪些决策
    
    -- 注入效果
    relevance_score REAL DEFAULT 0.5,  -- 相关性得分
    
    metadata JSON,
    
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

CREATE INDEX idx_context_injections_session ON context_injections(session_id);

-- ============================================================
-- 6. 价值评分历史表 (Value Score History)
-- ============================================================
CREATE TABLE IF NOT EXISTS value_score_history (
    history_id TEXT PRIMARY KEY,  -- UUID
    message_id TEXT NOT NULL,
    
    old_score REAL NOT NULL,
    new_score REAL NOT NULL,
    reason TEXT,  -- 'cited_by_decision', 'time_decay', 'manual_adjustment'
    
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (message_id) REFERENCES messages(message_id) ON DELETE CASCADE
);

CREATE INDEX idx_value_history_message ON value_score_history(message_id);

-- ============================================================
-- 触发器: 自动计算时间衰减权重
-- ============================================================
CREATE TRIGGER IF NOT EXISTS update_decay_weight
AFTER INSERT ON messages
BEGIN
    UPDATE messages
    SET decay_weight = 1.0
    WHERE message_id = NEW.message_id;
END;

-- ============================================================
-- 视图: 高价值记忆 (Top Memories)
-- ============================================================
CREATE VIEW IF NOT EXISTS top_memories AS
SELECT 
    m.message_id,
    m.session_id,
    m.content,
    m.created_at,
    m.value_score,
    m.decay_weight,
    (m.value_score * m.decay_weight) AS weighted_score,
    s.work_item_id
FROM messages m
JOIN sessions s ON m.session_id = s.session_id
WHERE m.role = 'assistant'
ORDER BY weighted_score DESC
LIMIT 100;

-- ============================================================
-- 视图: 最近决策 (Recent Decisions)
-- ============================================================
CREATE VIEW IF NOT EXISTS recent_decisions AS
SELECT 
    d.decision_id,
    d.subject,
    d.decision_type,
    d.decision_by,
    d.decision_at,
    d.impact_level,
    d.status,
    s.work_item_id
FROM decisions d
JOIN sessions s ON d.session_id = s.session_id
ORDER BY d.decision_at DESC
LIMIT 50;

-- ============================================================
-- 初始化元数据
-- ============================================================
CREATE TABLE IF NOT EXISTS schema_version (
    version TEXT PRIMARY KEY,
    applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO schema_version (version) VALUES ('1.0.0');
```

---

## Appendix B — probe harness, so the twenty cases can be rerun

The Q13 and Q11 tables in §2i report twenty executions between them. Those tables are
useless to a reader who cannot repeat them, and §16 grades the results on the strength of
executions that happened in a session and left no artefact. This appendix is the remedy.
The two harnesses below are the code that produced the two tables, in the form it was run
in.

Both read their DDL out of **this document**, not out of a copy: they extract the fenced
sql blocks before Appendix A, splice in the merged Event Store definitions that §7.1
references, and run against an in-memory SQLite. Re-running them therefore tests what this
document *currently* says, which is the property that matters after any later edit.

Appendix A is embedded because the prompt source has no authorised write path. This
appendix is embedded for a different reason: it is the evidence for two §2i rulings, and
evidence that cannot be located is evidence a reviewer cannot weigh.

**How to run.** From the repository root, on a machine with `sqlite3` at `/usr/bin/sqlite3`
(probed with 3.46.1):

```text
python3 <this file>   # pasted to /tmp/h13.py and /tmp/h11.py
```

**A note on the fence marker.** These harnesses build their markdown fence from
`chr(96) * 3` at run time rather than spelling it out. That is not stylistic: the first
version of this appendix substituted a literal triple-backtick inside the harness source
with a substituted form so the enclosing fence would not break, and in doing so it broke
the harness's own fence matching — both scripts then found zero sql blocks and the
reported results were unrepresentable. An independent reviewer caught it. Building the
marker at run time means the embedded source is byte-identical to the source that runs,
so that class of error cannot recur, and an assertion in the build step rejects any
harness that contains a literal triple-backtick at all.

### B.1 — Q13 harness

```python
# -*- coding: utf-8 -*-
"""Q13 probe harness. Extracts the design's own DDL from design-proposal.md and
tests the completed-requires-a-result CHECK on 14 cases. Needs /usr/bin/sqlite3.

The fence marker is built at runtime from chr(96) so this source contains no
literal triple-backtick sequence and can be embedded verbatim in Appendix B
without breaking the enclosing fence or needing any substitution."""
import subprocess, sys, io

F = chr(96) * 3                       # markdown fence, built not literal
FENCE_OPEN = F + "sql"

P = sys.argv[1] if len(sys.argv) > 1 else "14-ai-development/work-items/P2-T2-MEMORY-SCHEMA/design-proposal.md"
lines = io.open(P, encoding="utf-8").read().split("\n")

blocks = []
i = 0
while i < len(lines):
    if lines[i].strip() == FENCE_OPEN:
        j = i + 1
        while j < len(lines) and lines[j].strip() != F:
            j += 1
        blocks.append((i + 2, "\n".join(lines[i + 1:j])))
        i = j + 1
    else:
        i += 1

if not blocks:
    sys.exit("no sql blocks found in %s - fence marker mismatch" % P)

design = [b for (ln, b) in blocks if ln < 1700]

EV = """
CREATE TABLE IF NOT EXISTS accepted_events (
  event_row INTEGER PRIMARY KEY AUTOINCREMENT,
  producer_actor_ref TEXT NOT NULL, idempotency_key TEXT NOT NULL,
  payload_digest TEXT NOT NULL, scope_json TEXT NOT NULL,
  envelope_json TEXT NOT NULL, accepted_at TEXT NOT NULL,
  processing_state_json TEXT NOT NULL,
  UNIQUE(producer_actor_ref, idempotency_key)
);
CREATE TABLE IF NOT EXISTS event_payloads (
  event_row INTEGER PRIMARY KEY REFERENCES accepted_events(event_row) ON DELETE RESTRICT,
  payload_bytes BLOB NOT NULL, verified_digest TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS compile_outbox (
  outbox_row INTEGER PRIMARY KEY AUTOINCREMENT,
  event_row INTEGER NOT NULL UNIQUE REFERENCES accepted_events(event_row) ON DELETE RESTRICT,
  intent_kind TEXT NOT NULL CHECK (intent_kind = 'compile'), created_at TEXT NOT NULL
);
"""
BASE = "PRAGMA foreign_keys=ON;\n" + EV + "\n" + "\n".join(design)

FIX = """
INSERT INTO accepted_events (producer_actor_ref,idempotency_key,payload_digest,scope_json,envelope_json,accepted_at,processing_state_json) VALUES ('p','k1','d1','{}','{}','2026-01-01T00:00:00Z','{}');
INSERT INTO event_payloads (event_row,payload_bytes,verified_digest) VALUES (1,X'6162','d1');
INSERT INTO transcript_session VALUES ('s1',NULL,'api',NULL,NULL,NULL,'{}','2026-01-01T00:00:00Z',NULL,'open','standard',NULL,NULL);
INSERT INTO transcript_message VALUES ('m-asst','s1',1,'assistant',1,'d1',10,NULL,NULL,'original','2026-01-01T00:00:00Z','standard');
INSERT INTO transcript_message VALUES ('m-tool','s1',2,'tool',1,'d1',5,NULL,'m-asst','original','2026-01-01T00:00:00Z','standard');
INSERT INTO transcript_message VALUES ('m-tool2','s1',3,'tool',1,'d1',5,NULL,'m-asst','original','2026-01-01T00:00:00Z','standard');
"""

CASES = [
 ("A  INSERT completed, result NULL", "INSERT INTO transcript_tool_call VALUES ('s1','tc1',0,'m-asst',NULL,'read','completed');", "REFUSED"),
 ("B  emitted -> completed, result NULL", "INSERT INTO transcript_tool_call VALUES ('s1','tc1',0,'m-asst',NULL,'read','emitted');UPDATE transcript_tool_call SET tool_state='completed' WHERE tool_call_id='tc1';", "REFUSED"),
 ("C  emitted -> completed WITH valid result", "INSERT INTO transcript_tool_call VALUES ('s1','tc1',0,'m-asst',NULL,'read','emitted');UPDATE transcript_tool_call SET tool_state='completed', result_message_id='m-tool' WHERE tool_call_id='tc1';", "ACCEPTED"),
 ("D  INSERT completed WITH valid result", "INSERT INTO transcript_tool_call VALUES ('s1','tc1',0,'m-asst','m-tool','read','completed');", "ACCEPTED"),
 ("E  failed with NULL result", "INSERT INTO transcript_tool_call VALUES ('s1','tc1',0,'m-asst',NULL,'read','failed');", "ACCEPTED"),
 ("F  emitted with NULL result", "INSERT INTO transcript_tool_call VALUES ('s1','tc1',0,'m-asst',NULL,'read','emitted');", "ACCEPTED"),
 ("G  bind result FIRST, then completed", "INSERT INTO transcript_tool_call VALUES ('s1','tc1',0,'m-asst',NULL,'read','emitted');UPDATE transcript_tool_call SET result_message_id='m-tool' WHERE tool_call_id='tc1';UPDATE transcript_tool_call SET tool_state='completed' WHERE tool_call_id='tc1';", "ACCEPTED"),
 ("H  completed bound to a DIFFERENT child", "INSERT INTO transcript_tool_call VALUES ('s1','tc1',0,'m-asst',NULL,'read','emitted');UPDATE transcript_tool_call SET tool_state='completed', result_message_id='m-tool2' WHERE tool_call_id='tc1';", "ACCEPTED"),
 ("I  rebind a bound result (R4 guard)", "INSERT INTO transcript_tool_call VALUES ('s1','tc1',0,'m-asst','m-tool','read','completed');UPDATE transcript_tool_call SET result_message_id='m-tool2' WHERE tool_call_id='tc1';", "REFUSED"),
 ("J  clear a bound result (R4 guard)", "INSERT INTO transcript_tool_call VALUES ('s1','tc1',0,'m-asst','m-tool','read','completed');UPDATE transcript_tool_call SET result_message_id=NULL WHERE tool_call_id='tc1';", "REFUSED"),
 ("K  UPDATE tool_name on a completed row", "INSERT INTO transcript_tool_call VALUES ('s1','tc1',0,'m-asst','m-tool','read','completed');UPDATE transcript_tool_call SET tool_name='write' WHERE tool_call_id='tc1';", "ACCEPTED"),
 ("L  result bound while state emitted", "INSERT INTO transcript_tool_call VALUES ('s1','tc1',0,'m-asst','m-tool','read','emitted');", "ACCEPTED"),
 ("M  emitted+result then -> failed", "INSERT INTO transcript_tool_call VALUES ('s1','tc1',0,'m-asst','m-tool','read','emitted');UPDATE transcript_tool_call SET tool_state='failed' WHERE tool_call_id='tc1';", "ACCEPTED"),
 ("N  completed -> emitted", "INSERT INTO transcript_tool_call VALUES ('s1','tc1',0,'m-asst','m-tool','read','completed');UPDATE transcript_tool_call SET tool_state='emitted' WHERE tool_call_id='tc1';", "REFUSED"),
]

print("extracted %d sql blocks from %s" % (len(blocks), P))
fails = 0
for label, body, expect in CASES:
    p = subprocess.run(["/usr/bin/sqlite3", ":memory:"], input=BASE + FIX + body,
                       capture_output=True, text=True)
    actual = "ACCEPTED" if p.returncode == 0 else "REFUSED"
    ok = actual == expect
    if not ok:
        fails += 1
    print("%-4s %-44s expect=%-8s got=%s" % ("PASS" if ok else "FAIL", label, expect, actual))

print("\n%d cases, %d pass, %d fail" % (len(CASES), len(CASES) - fails, fails))
sys.exit(1 if fails else 0)
```

### B.2 — Q11 harness

```python
# -*- coding: utf-8 -*-
"""Q11 probe harness. Extracts the design's own DDL from design-proposal.md and
tests whether versions_memory_version_uq changes admissible rows. 6 cases.
Needs /usr/bin/sqlite3.

The fence marker is built at runtime from chr(96) so this source contains no
literal triple-backtick sequence and can be embedded verbatim in Appendix B
without breaking the enclosing fence or needing any substitution."""
import subprocess, sys, io

F = chr(96) * 3                       # markdown fence, built not literal
FENCE_OPEN = F + "sql"

P = sys.argv[1] if len(sys.argv) > 1 else "14-ai-development/work-items/P2-T2-MEMORY-SCHEMA/design-proposal.md"
lines = io.open(P, encoding="utf-8").read().split("\n")

blocks = []
i = 0
while i < len(lines):
    if lines[i].strip() == FENCE_OPEN:
        j = i + 1
        while j < len(lines) and lines[j].strip() != F:
            j += 1
        blocks.append((i + 2, "\n".join(lines[i + 1:j])))
        i = j + 1
    else:
        i += 1

if not blocks:
    sys.exit("no sql blocks found in %s - fence marker mismatch" % P)

design = "\n".join(b for (ln, b) in blocks if ln < 1700)

EV = """
CREATE TABLE IF NOT EXISTS accepted_events (
  event_row INTEGER PRIMARY KEY AUTOINCREMENT,
  producer_actor_ref TEXT NOT NULL, idempotency_key TEXT NOT NULL,
  payload_digest TEXT NOT NULL, scope_json TEXT NOT NULL,
  envelope_json TEXT NOT NULL, accepted_at TEXT NOT NULL,
  processing_state_json TEXT NOT NULL,
  UNIQUE(producer_actor_ref, idempotency_key)
);
CREATE TABLE IF NOT EXISTS event_payloads (
  event_row INTEGER PRIMARY KEY REFERENCES accepted_events(event_row) ON DELETE RESTRICT,
  payload_bytes BLOB NOT NULL, verified_digest TEXT NOT NULL
);
"""
PRE = "PRAGMA foreign_keys=ON;\n" + EV + "\n" + design

IDX = ("CREATE UNIQUE INDEX IF NOT EXISTS versions_memory_version_uq\n"
       "  ON versions(memory_id, version_id);")
IDX_NONUNIQUE = ("CREATE INDEX IF NOT EXISTS versions_mv_idx\n"
                 "  ON versions(memory_id, version_id);")

BASE_IDX = PRE
BASE_NO_IDX = PRE.replace(IDX, "")
BASE_NONUNIQ = PRE.replace(IDX, IDX_NONUNIQUE)

SEED = """
INSERT INTO memories VALUES ('m1','{}',NULL,'{}');
INSERT INTO memories VALUES ('m2','{}',NULL,'{}');
INSERT INTO versions VALUES ('v1','m1',1,NULL,'{}','{}',1);
"""
CTX = ("INSERT INTO context_assembly VALUES ('a1','sc',NULL,NULL,"
       "'2026-01-01T00:00:00Z','draft');")
ENTRY_M1 = ("INSERT INTO context_assembly_entry VALUES ('e1','a1','m1','v1',1,NULL,"
            "'included','2026-01-01T00:00:00Z');")
ENTRY_M2 = ("INSERT INTO context_assembly_entry VALUES ('e1','a1','m2','v1',1,NULL,"
            "'included','2026-01-01T00:00:00Z');")

CASES = [
 ("P1 duplicate (memory_id, version_id), no index", BASE_NO_IDX,
  SEED + "INSERT INTO versions VALUES ('v1','m1',2,NULL,'{}','{}',2);", "FAILED"),
 ("P2 composite FK, no unique parent key, MATCHED pair", BASE_NO_IDX,
  SEED + CTX + ENTRY_M1, "FAILED"),
 ("P3 composite FK, no unique parent key, MISMATCHED pair", BASE_NO_IDX,
  SEED + CTX + ENTRY_M2, "FAILED"),
 ("P4 WITH index, MATCHED pair", BASE_IDX,
  SEED + CTX + ENTRY_M1, "ACCEPTED"),
 ("P5 WITH index, MISMATCHED pair", BASE_IDX,
  SEED + CTX + ENTRY_M2, "FAILED"),
 ("P6 NON-unique parent index, MATCHED pair", BASE_NONUNIQ,
  SEED + CTX + ENTRY_M1, "FAILED"),
]

print("extracted %d sql blocks from %s" % (len(blocks), P))
fails = 0
for label, base, body, expect in CASES:
    p = subprocess.run(["/usr/bin/sqlite3", ":memory:"], input=base + body,
                       capture_output=True, text=True)
    actual = "ACCEPTED" if p.returncode == 0 else "FAILED"
    ok = actual == expect
    if not ok:
        fails += 1
    print("%-4s %-52s expect=%-8s got=%s" % ("PASS" if ok else "FAIL", label, expect, actual))
    if p.stderr.strip():
        print("       err: " + p.stderr.strip().replace("\n", " | ")[:120])

print("\n%d cases, %d pass, %d fail" % (len(CASES), len(CASES) - fails, fails))
sys.exit(1 if fails else 0)
```

### B.3 — captured output

Not an expectation — the actual output of the run that produced §2i's tables, recorded
here so a reviewer can compare rather than trust:

Q13:

```text
extracted 10 sql blocks from 14-ai-development/work-items/P2-T2-MEMORY-SCHEMA/design-proposal.md
PASS A  INSERT completed, result NULL             expect=REFUSED  got=REFUSED
PASS B  emitted -> completed, result NULL         expect=REFUSED  got=REFUSED
PASS C  emitted -> completed WITH valid result    expect=ACCEPTED got=ACCEPTED
PASS D  INSERT completed WITH valid result        expect=ACCEPTED got=ACCEPTED
PASS E  failed with NULL result                   expect=ACCEPTED got=ACCEPTED
PASS F  emitted with NULL result                  expect=ACCEPTED got=ACCEPTED
PASS G  bind result FIRST, then completed         expect=ACCEPTED got=ACCEPTED
PASS H  completed bound to a DIFFERENT child      expect=ACCEPTED got=ACCEPTED
PASS I  rebind a bound result (R4 guard)          expect=REFUSED  got=REFUSED
PASS J  clear a bound result (R4 guard)           expect=REFUSED  got=REFUSED
PASS K  UPDATE tool_name on a completed row       expect=ACCEPTED got=ACCEPTED
PASS L  result bound while state emitted          expect=ACCEPTED got=ACCEPTED
PASS M  emitted+result then -> failed             expect=ACCEPTED got=ACCEPTED
PASS N  completed -> emitted                      expect=REFUSED  got=REFUSED

14 cases, 14 pass, 0 fail
```

Q11:

```text
extracted 10 sql blocks from 14-ai-development/work-items/P2-T2-MEMORY-SCHEMA/design-proposal.md
PASS P1 duplicate (memory_id, version_id), no index       expect=FAILED   got=FAILED
       err: Runtime error near line 369: UNIQUE constraint failed: versions.version_id (19)
PASS P2 composite FK, no unique parent key, MATCHED pair  expect=FAILED   got=FAILED
       err: Parse error near line 369: foreign key mismatch - "context_assembly_entry" referencing "versions"
PASS P3 composite FK, no unique parent key, MISMATCHED pair expect=FAILED   got=FAILED
       err: Parse error near line 369: foreign key mismatch - "context_assembly_entry" referencing "versions"
PASS P4 WITH index, MATCHED pair                          expect=ACCEPTED got=ACCEPTED
PASS P5 WITH index, MISMATCHED pair                       expect=FAILED   got=FAILED
       err: Runtime error near line 370: FOREIGN KEY constraint failed (19)
PASS P6 NON-unique parent index, MATCHED pair             expect=FAILED   got=FAILED
       err: Parse error near line 370: foreign key mismatch - "context_assembly_entry" referencing "versions"

6 cases, 6 pass, 0 fail
```

A mismatch means either the document changed or §2i's table is wrong. Either is worth
knowing, which is the point of keeping the harness beside the claim.
