---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-325/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "The decision uses supplied measurements and delivery evidence; this documentation record has not independently rerun repository or GitHub measurements."
    usage_status: Active
    modification_status: Modified
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
    canonical_scope: "Adjudication of Issue #1247 and disposition of the three proposed independent-review gate paths."
    canonical_scope_id: "ai-development/aid-2026-325-decision-record"
    canonical_scope_keywords:
      - "AID-2026-325"
      - "independent-review"
      - "decision"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Decision record 鈥?AID-2026-325

## 1. Decision

**Disposition: TAKEN 鈥?session declaration with explicit NOT_ASSIGNED accounting.**

Issue #1247 identified a disagreement between the executable
`independent_review` gate and PR-GOVERNANCE-001 搂5.

The disagreement has already been corrected in code and merged through
PR #1325. This work item records the adjudication and its evidence. It
does not repeat that implementation.

The governing criterion is:

> Independence is a property of the reviewing session, not of the
> GitHub account that carries it.

A review is independent when its reviewing session did not author or
implement the change and reaches its conclusion from the artifacts rather
than from the author's account of them. Two sessions may share one GitHub
identity. One session may not become independent by adopting another role
or another identity string.

The gate's session fields establish a declaration. They do not establish
that the declared sessions correspond to distinct real execution contexts.
That limitation is material and must remain explicit.

## 2. Why the identity criterion had to fail

### 2.1 The executable implemented a retired criterion

The pre-amendment wording of PR-GOVERNANCE-001 搂5 stated:

> A review performed through the same connected GitHub identity as the
> author is not independent, even if the session adopts a different role.

The former executable comparison implemented that exact proposition:

```python
aliases = _normalized_aliases(data.get("review_identity_aliases", {}))
if _identity(evidence["reviewer"], aliases) == _identity(evidence["implementer"], aliases):
    raise ValueError("REVIEWED reviewer and implementer must be different identities")
```

The predicate compared normalized account-identifying strings. It did
not compare execution sessions.

Amendment
`GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036` replaced the
retired wording. The amended text is recorded at
`14-ai-development/PR-GOVERNANCE-001.md`, 搂5, line 138.

The amendment explicitly says that:

- Independence belongs to the reviewing session.
- Separate sessions may share one GitHub identity.
- Account identity is the carrier, not the independence criterion.
- The relevant question is whether the reviewing context is shared.
- AI role simulation inside the authoring session is not independent review.

The clause changed the predicate. The original executable did not change
at the same time. Consequently, the executable was implementing a
superseded rule.

This is a semantic mismatch, not a disagreement about normalization or
the quality of an account-alias table.

### 2.2 The identity predicate has an empty lawful satisfying set here

Let:

- \(A\) be the set of GitHub accounts available as repository write
  principals.
- \(R\) be the set of reviews performed through those principals.
- \(I(r)\) be the normalized GitHub identity of the reviewer in review
  \(r\).
- \(W(r)\) be the normalized GitHub identity of the implementer in review
  \(r\).
- \(S_r\) and \(S_w\) be their respective execution sessions.

The retired gate accepted a review only when:

\[
I(r) \ne W(r)
\]

The governing clause accepts an independent review when:

\[
S_r \ne S_w
\]

These predicates are not equivalent.

The measured repository state has exactly one direct account with
permission to push:

```text
GET /repos/oahcom/AiMemoryBrainArchitecture/collaborators?affiliation=direct&per_page=100

1 entry:
login=oahcom
permissions:
  admin: true
  maintain: true
  push: true
  triage: true
  pull: true
```

The repository owner is also `oahcom`.

The measured recent merged-PR sample is consistent with this
single-principal write model:

- 10 of 10 recent merged PRs have `author=oahcom` and
  `merged_by=oahcom`.
- A wider sample contains 132 of 132 merged PRs authored by `oahcom`.
- PR #1325, which implemented the correction, was also authored and
  merged by `oahcom`.

For the repository's measured write and merge path, the set of distinct
write-capable identities is therefore:

\[
A = \{\text{oahcom}\}
\]

For any review whose implementer and reviewer are drawn from that
single-principal write path:

\[
I(r) = W(r) = \text{oahcom}
\]

Therefore:

\[
\{r \in R : I(r) \ne W(r)\} = \varnothing
\]

The old predicate has no satisfying review in that operating model.

The amended clause permits a lawful arrangement in which:

\[
I(r) = W(r)
\quad\land\quad
S_r \ne S_w
\]

The old executable rejects that arrangement.

Conversely, the old executable can accept:

\[
I(r) \ne W(r)
\quad\land\quad
S_r = S_w
\]

The amended clause explicitly forbids that arrangement because the
reviewing session shares the authoring context.

Thus the old predicate rejects the lawful same-account, separate-session
case and accepts the forbidden different-account, same-session case.

The measured account and PR distributions establish why the retired
criterion is structurally unsuitable for this repository's observed
write path. They are not a claim that no external read-only reviewer
could ever participate. The decisive defect is that account inequality
is neither necessary nor sufficient for session independence.

### 2.3 Alias normalization cannot repair the predicate

`review_identity_aliases` has a legitimate carrier-identity purpose:
different spellings of one GitHub account may be normalized to one
identity.

That table cannot manufacture another principal, cannot establish
another execution context, and cannot distinguish two sessions carried
by the same account.

Changing alias entries therefore cannot make account inequality a
correct test of session independence.

The corrected implementation retains alias validation and computes
the same-account condition as a diagnostic assignment. That diagnostic
is not the verdict.

The current assignment is:

```python
_same_account = (_identity(evidence["reviewer"], aliases)
                 == _identity(evidence["implementer"], aliases))
```

The assignment is currently unread. This is a residual implementation
issue, not a reason to restore the retired identity verdict.

### 2.4 Why the mismatch remained invisible

Three independent conditions explain the absence of an earlier
operational signal.

**First: no CI wiring.**

The checker is not referenced by any GitHub Actions workflow:

```bash
git grep -l check_status_gates -- .github/workflows
```

The measured result is no output.

The checker has repository references in documentation and tests, but
those references do not make it a required workflow context.

**Second: earlier corpus failures stopped at other validation arms.**

The independent verification at commit `9c3ecf2` measured 56 manifests:

```text
2 pass / 54 fail

37  status is not an exact canonical state
15  missing/invalid lifecycle
 1  unknown gate records: registration
 1  invalid gate disposition: merge
```

Those earlier validation failures prevented most manifests from
reaching the independent-review comparison.

**Third: no manifest supplied a passing independent-review gate.**

The corrected independent verification found four manifests carrying
an `independent_review` record, but none with status `PASS`.

The current measured corpus contains five such records and again
contains zero with status `PASS`.

Consequently, the defective predicate had no passing corpus input
that would expose its semantic disagreement.

The absence of an observed failure was not evidence that the criterion
was correct. It was a consequence of validation order, absent CI
wiring, and absent passing gate inputs.

## 3. The three paths considered

### 3.1 Path 1 鈥?Session declaration plus explicit NOT_ASSIGNED accounting

**What changes**

Independence is declared at session level through:

- `reviewer_session`
- `implementer_session`

The checker compares normalized session tokens for inequality.

The account comparison remains a disclosed diagnostic, not the
independence verdict.

A review that cannot name a distinct reviewing session must not be
silently waived or represented as independent. Its accounting remains
`NOT_ASSIGNED` where no qualifying independent session can be assigned.

The required evidence fields are:

```python
"independent_review": (
    "reviewer",
    "implementer",
    "reviewer_session",
    "implementer_session",
    "reviewed_head",
    "report",
    "findings_disposition",
)
```

The implemented comparison rejects equal normalized session tokens:

```python
if _session_token(evidence["reviewer_session"]) == _session_token(
        evidence["implementer_session"]):
    raise ValueError(
        "REVIEWED reviewer_session and implementer_session must be different sessions")
```

**Verifiable acceptance criterion**

All of the following must hold:

1. `test_one_account_with_two_sessions_is_independent` passes.
2. `test_two_accounts_sharing_one_session_is_not_independent` passes.
3. A manifest omitting a required session field is rejected.
4. The measured 130-manifest checker output contains no
   `different identities` failure.
5. The behavioral test suite passes.

The measured results are recorded in `evidence.md`.

**Cost and limitation**

Session values are writer-declared strings.

The checker can normalize and compare those declarations. It cannot
prove that the named sessions existed, that they were separate
execution contexts, or that their authors did not share context.

The honest provenance label for this limitation is:

`executed_prompt_provenance: NOT_VERIFIED`

The gate therefore verifies a declaration, not the historical
existence of two independently executed sessions.

The declaration must not be promoted into stronger provenance evidence
than the repository can corroborate.

**Disposition: TAKEN**

Implemented and merged through PR #1325.

Merge commit:

`3daebd2cad699b5ecccd7ffa7df86029dfbecec6`

The measured behavioral tests and corpus results are recorded in
sections 5 and 6 of this record and in `evidence.md`.

Residual limitations:

- `_same_account` is assigned but never read.
- The checker has no CI workflow surface.

Neither residual is fixed by this decision record.

### 3.2 Path 2 鈥?Keep the identity comparison and mark the gate unsatisfiable

**What changes**

Leave the original executable identity comparison in place and amend
the governance clause to say that independent review by account is
unattainable in a single-write-identity repository.

Under this path, `independent_review` would be recorded as
`BLOCKED` or `NOT_ASSIGNED` for every item requiring independent review.

**Verifiable acceptance criterion**

Both conditions would be required:

1. Every `REVIEWED` item in the 130-manifest corpus would have
   independent-review accounting of `NOT_ASSIGNED` or `BLOCKED`,
   with zero `PASS`.
2. The canonical clause would explicitly state the account-level
   unsatisfiability rule.

**Cost**

This converts a fixable semantic mismatch into permanent,
repository-wide non-conformance.

It contradicts the amended session-level rule in PR-GOVERNANCE-001
搂5, line 138.

It would also require amendment of a Canonical + Approved document,
which carries its own approval chain and is outside this work item's
authority and scope.

**Disposition: REJECTED**

The clause is already correct.

Every lawful same-account, separate-session review would remain
rejected by the executable. Every affected `REVIEWED` transition
would be subject to the retired criterion.

### 3.3 Path 3 鈥?Cancel the gate and demote 搂5 to a process requirement

**What changes**

Remove the `independent_review` arm from
`check_status_gates.py` and leave independence solely as governance
prose.

**Verifiable acceptance criterion**

Both conditions would be required:

1. The `independent_review` arm no longer exists in
   `check_status_gates.py`.
2. PR-GOVERNANCE-001 搂5 carries no machine-checkable independent-review
   requirement.

**Cost**

This deletes the only executable validation surface for an invariant
that 搂5 makes mandatory for security, identity, authorization,
lifecycle, canonical persistence, recovery, cross-owner contracts,
and production operations.

It also removes evidence fields that make non-independence visible
rather than silently allowing the transition to proceed.

The repository's single-principal operating pattern makes the
authoring-session self-review failure particularly important to
prevent.

**Disposition: REJECTED**

The failure mode 搂5 exists to prevent is one session reviewing its
own work.

Removing the gate would remove the machine-checkable declaration
boundary without resolving the underlying independence problem.

## 4. Implementation adjudication

The selected path was implemented before this documentation work item.

**Pull request**

- PR: #1325
- Title: `fix(241): decide independent review by session, not by GitHub account`
- Author: `oahcom`
- Merger: `oahcom`
- Merged: `2026-11-27T04:38:43Z`
- Merge commit: `3daebd2cad699b5ecccd7ffa7df86029dfbecec6`
- Final PR head: `fe16a378930e3f06a71a55e6b9036fb9397522f1`

The delivery record reports:

- 16 of 16 required contexts SUCCESS.
- `behind=0`.
- The six files of AID-2026-241 were checked individually after merge.
- The PR merge commit and `origin/main` blobs were identical.

The corresponding commit on `main` is:

`0f7dfbc9`

Its subject is:

`fix(082): decide independent review by session, not by GitHub account`

The difference between the PR title's `241` and the commit subject's `082`
is recorded as an observation. This decision does not classify it as a
defect.

The implementation work item is:

`14-ai-development/work-items/AID-2026-241/manifest.yaml`

Its recorded status is `MERGED`, its class is `GATE/POLICY`, and its
tracking issue is `#1247`.

This work item does not claim that PR #1325 is a merge produced by
AID-2026-325. It records that implementation as an existing dependency
and adjudication fact.

## 5. Residuals

Two residuals remain explicitly open.

### 5.1 Dead account diagnostic

`_same_account` is assigned exactly once in
`check_status_gates.py` and is never read.

It is therefore not currently an observable diagnostic output.
Calling it a disclosed diagnostic describes its intended semantic
role, not a claim that the current implementation exposes a usable
diagnostic record.

This is not fixed here.

A separate carrier must define:

- How the same-account condition is exposed.
- Where that diagnostic is recorded.
- How alias normalization is represented.
- Tests proving the diagnostic does not affect the independence verdict.
- An acceptance criterion proving the diagnostic is observable and
  non-authoritative.

### 5.2 Missing CI surface

The checker has no GitHub Actions workflow reference.

This is not fixed here.

A separate carrier must define:

- The required workflow and job.
- Its trigger and execution scope.
- The repository state against which it evaluates manifests.
- Its failure propagation and required-context behavior.
- A verifiable workflow-level acceptance criterion.

Neither residual is declared harmless. Neither is silently waived.

## 6. Carrier boundary

This work item is documentation only.

It produces:

- `manifest.yaml`
- `decision.md`
- `evidence.md`
- `session-evidence.md`
- `prompt-v1.md`
- Exactly one row in `14-ai-development/work-items/INDEX.md`

It does **not** modify:

- `14-ai-development/PR-GOVERNANCE-001.md`
- `scripts/governance/status_migration/check_status_gates.py`
- `scripts/governance/status_migration/test_status_migration.py`

It does not change any workflow, schema, or executable gate.

The two residuals identified above are not fixed here:

1. The dead `_same_account` diagnostic requires its own carrier.
2. The checker having no CI surface requires its own carrier.

Each carrier must have its own scope, implementation authority,
acceptance criteria, and verification evidence.

No code or clause amendment is proposed as part of this PR.

## 7. Acceptance and authority

This record is a decision-authoring artifact, not an Owner acceptance
instrument.

The authoring session is not an independent reviewer of its own record.
It does not assert Owner acceptance, domain-owner acceptance, or
independent review.

The manifest therefore records:

- `review.status: NOT_ASSIGNED`
- `acceptance.status: NOT_ASSIGNED`
- `acceptance_authority: NOT_ASSIGNED`

The documentation record remains pending the designated acceptance
process.

## 8. Final disposition of Issue #1247

The substantive discrepancy reported by Issue #1247 has been corrected
by the already merged PR #1325.

The selected rule is session-level independence, consistent with
PR-GOVERNANCE-001 搂5.

The old identity comparison is not the independence verdict.

The repository still cannot verify the truth of writer-declared session
identifiers. That limitation is explicit and is not represented as
proof of independent execution.

The dead diagnostic and absent CI wiring remain separate unresolved
implementation residuals.

This decision record documents the adjudication. It does not itself
close the issue, merge a pull request, or claim completion of the
separate residual work.

Issue #1247 may be closed by the authorized executor after this
documentation carrier has passed its required repository gates,
been merged, and had its delivery recorded.
