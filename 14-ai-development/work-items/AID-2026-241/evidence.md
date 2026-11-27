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
      evidence_reference:
        - "AID-2026-241/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Every figure below came from a command run on 2026-11-26 against main 8d90843a, and the two discriminating cases were executed by the real checker rather than reasoned about. The probe manifests were deleted before commit and are reproduced here so the measurement can be repeated. What this record cannot support - that the corrected gate has been reviewed - is stated as not supported."
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
    canonical_scope_keywords:
      - "independent-review"
      - "session-identity"
      - "governance-gate"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Session evidence — AID-2026-241

## Session role / use case

MEASURER. This session measured that the `independent_review` arm of
`scripts/governance/status_migration/check_status_gates.py` decides independence by GitHub
account string while `PR-GOVERNANCE-001.md` section 5 decides it by session, and that the two
rules disagree in both directions. It did not write the correction, did not review it, and
asserts no acceptance. The correction is the IMPLEMENTER session's work, recorded separately.

## Actual AI input

The standing instruction that governed this session, verbatim:

> 你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可，若因人类干预才可继续你可以当作为人类去收敛，但不能自己动手写代码。以最高效率去执行，动用所有能动用的资源，使用最多的子线程子代理

and, as the session resumed after interruptions:

> 请继续执行任务

`不能自己动手写代码` is the constraint the record has to be honest about. Nine delegated
sessions in this task terminated on an upstream proxy fault (`ECONNREFUSED` / `ETIMEDOUT` to
192.168.1.108:20127) or on `upstream connection lost`, several after running for 12 to 76
minutes. The measurement below was therefore executed directly by the orchestrating session.
It is measurement, not implementation: the commands are reproductions of a defect, and the
files they wrote were probe manifests under `_probe-081/`, deleted before commit.

## AI-visible output

`scripts/governance/status_migration/check_status_gates.py` was read, not modified. The
deliverable is this record, the manifest that registers the work item, the prompt snapshot, and
Issue #1247.

---

## 1. What the code does

`check_status_gates.py:275-277`, verbatim:

```python
aliases = _normalized_aliases(data.get("review_identity_aliases", {}))
if _identity(evidence["reviewer"], aliases) == _identity(evidence["implementer"], aliases):
    raise ValueError("REVIEWED reviewer and implementer must be different identities")
```

`_identity()` at line 228-234:

```python
def _identity_token(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("review identities must be non-empty strings")
    normalized = unicodedata.normalize("NFKC", value).strip().casefold()
    normalized = re.sub(r"^(?:https?://)?(?:www\.)?github\.com/", "", normalized)
    normalized = normalized.lstrip("@")
    return re.sub(r"[^a-z0-9]", "", normalized)
```

The comparison is between account strings. `review_identity_aliases` exists to collapse two
spellings of one account, which confirms the intended subject is the account.

## 2. What the clause says

`14-ai-development/PR-GOVERNANCE-001.md:136-138`, English, extracted:

> Independence is a property of the reviewing session, not of the GitHub account that carries
> it. A review is independent when it is performed by a session that did not author the change
> and did not implement it... Separate sessions may share one GitHub identity; the identity is
> the carrier, and independence is decided by whether the context is shared, not by whether the
> account differs... **AI role simulation inside the authoring session is not independent
> review**...

This wording replaced text that said the opposite, on 2026-11-24, recorded in
`GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`. That register quotes the retired
wording verbatim in its section 4: *"A review performed through the same connected GitHub
identity as the author is not independent, even if the session adopts a different role."*

The retired sentence is the code above, written in prose. The clause was amended; the
executable was not.

## 3. The two cases, executed

Both manifests are `status: REVIEWED` with `source_authenticity: NOT_VERIFIED`, all six gate
records present (the four future gates `NOT_RECORDED`), and evidence fields pointing at a
committed blob that exists at `subject_head`, because `_evidence_file()` requires blob equality
with the committed tree rather than the working tree. They differ only in the two identity
values.

Case A — two sessions, one identity. Lawful under section 5:

```yaml
independent_review:
  status: PASS
  evidence:
    reviewer: "req05-session-a"
    implementer: "req05-session-a"
```

Case B — one session, two identity strings. Forbidden by section 5:

```yaml
independent_review:
  status: PASS
  evidence:
    reviewer: "reviewer-alice"
    implementer: "implementer-bob"
```

Output, `subject_head = 9ee89b322a160cc7ea5bcbd44ae2151850e289a0`:

```
CASE A: {"result": "FAIL", "error": "REVIEWED reviewer and implementer must be different identities"}
CASE B: {"result": "PASS", "phase": "VALIDATION", "content_integrity": "PASS", "source_authenticity": "NOT_VERIFIED"}
```

The gate fails the arrangement section 5 permits and passes the arrangement section 5
forbids. This is not a weak check on the right question; it is a correct check on the retired
question.

## 4. Why nothing caught it

```
grep -rn 'check_status_gates' .github/workflows/ scripts/ci/
-> no match
```

The checker is reachable only by invoking it by hand. Its behaviour is exercised by its own test
module and by nothing else, so a disagreement with the clause has no CI surface.

## 5. The defect is latent, and the measurement says so

Over all 57 manifests at `8d90843a`:

```
lifecycle.gates.independent_review present: 0 of 57
checker over the real corpus: 2 pass / 55 fail
  of the 55: "status is not an exact canonical state" or "missing/invalid lifecycle"
```

No manifest reaches the `independent_review` arm at all, so no merged review has been judged by
the wrong criterion. The count is stated because it bounds the claim: this is a trap for the
first work item that reaches `REVIEWED`, not damage already done.

## 6. What this record does not claim

- Not claimed that a session string proves two contexts existed. It is a writer-chosen string;
  the `session_evidence` contract already labels its provenance `NOT_VERIFIED`. The corrected
  check can verify a declaration, not an event, and the code comment is required to say so.
- Not claimed that the 55 corpus failures are this work item's business. 53 are status
  vocabulary and belong to #1154.
- Not claimed that the correction is reviewed, accepted or merged. None of those has happened.


## Renumbering evidence

This work item was originally stored under `AID-2026-082`, which collided with a distinct item already present on `main`. The assigned replacement is `AID-2026-241`. The original `prompt-v1.md` bytes were 6,983 bytes with SHA-256 `5c8f02062568720bb9132b27bdb3d6a4c9ac9fbb603d0c42a4818f6c2105002a`. After changing the work-item identifier and all self-referential paths, the current `prompt-v1.md` is 7,096 bytes with SHA-256 `6d00802519f99412119dc879ee64c5a89598ad5ff5d915d7aa5207cec2e825e2`. This digest was recomputed over the complete current file bytes; it is not a digest of the directory name or Git blob.
