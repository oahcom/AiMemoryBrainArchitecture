---
document_metadata:
  domain: security-governance
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-22"
      last_verification_note: "All three issues re-probed by running the gates on main @ 3b7c787c, not by reading them. The zero-member scope count is a direct enumeration of every canonical_scope_id in the tree."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

# GAP-20 — Three gate findings: one is fixed, one is real but not where it was reported, one is a new silent state

**Status:** Open — one issue to close, two to amend
**Area:** governance / CI gates
**Measured at:** `main @ 3b7c787c`, `2026-11-22T09:05Z`
**Subject:** #635, #630, #522

---

## 1. Summary

| issue | claim | current state | verdict |
|---|---|---|---|
| #522 | bilingual gate requires `docs/en` + `docs/zh-CN` copies of JSON schemas and fixtures | **fixed** | close it |
| #635 | both gates print `PASS` on an empty changed-path set | **fixed** | close it, one caveat |
| #630 | DM-07 has no lower bound, a scope can own zero Canonical documents | **partly right, wrong diagnosis** | amend it |

Measured by running the gates, not by reading them.

## 2. #522 is fixed

The issue's probe: touch one existing schema and nothing else, then run the bilingual gate. It reported:

```
::error::08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json
  requires all counterparts changed in this PR
```

Reproduced on `3b7c787c`, with `core.autocrlf=false` so the probe changes exactly one file:

```
$ git diff --name-only $BASE $HEAD
08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json

$ BASE_SHA=$BASE HEAD_SHA=$HEAD PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
    python3 scripts/check_bilingual_docs.py
::error::New bilingual gap outside frozen baseline: 14-ai-development/governance-register/...-024.md
```

Zero `::error` lines mention a schema. The single remaining error is a different file, unrelated to the probe.

The cause is `scripts/check_bilingual_docs.py:1152-1159`:

```python
normative_changes = []
for path in sorted(changed):
    parts = Path(path).parts
    if len(parts) >= 2 and parts[0] in NORMATIVE_ROOTS:
        if Path(path).suffix.lower() in EXEMPT_SUFFIXES:
            continue
        if Path(path).suffix.lower() == ".md":
            normative_changes.append(path)
```

The `== ".md"` guard means a `.schema.json` under a normative root never enters the normative set. #522 asked for exactly this and got it.

## 3. #635 is fixed, with one caveat that is not the one it reports

The issue reports two things: an empty changed set prints `PASS`, and one gate degrades to a two-dot diff on a path-like base ref.

**The vacuous-PASS half is fixed.** Two probes:

- `--require-changed <base>` where `base == HEAD` (empty diff, real git history): `FAIL: 13 error(s)`, exit 1. Not PASS.
- Bilingual gate with `BASE_SHA`/`HEAD_SHA` unset: `::error::Unable to determine changed paths: BASE_SHA and HEAD_SHA are required`, exit 2. Not PASS.

Both now refuse rather than pass. The behaviour #635 describes cannot be reproduced.

**The caveat worth keeping.** `--require-changed` on an empty diff returns **FAIL**, and the 13 errors are all `DM-10 approved_version ... is not a commit in this repository`. That is correct behaviour for a shallow clone and wrong for a real one: an empty diff on a full-history checkout would presumably return `PASS` with `0 changed paths inspected`. So the vacuous-PASS *shape* may still exist for whole-tree mode; what is fixed is that it no longer happens silently on the incremental path.

I did not test whole-tree-with-no-base, because whole-tree mode always inspects everything and cannot be vacuous. The remaining exposure, if any, is small. #635's own reproduction required a specific invocation, and that invocation now errors.

**Caveat on my own measurement:** these probes ran in a locally-initialised git repo, which is why `DM-10` fires. The real CI uses `fetch-depth: 0`. A re-measurement with real history would settle whether empty-diff `PASS` survives; I am not claiming it does or does not, only that the two reported paths now refuse.

## 4. #630 is real, but the mechanism is different and worse

The issue says: `DM-07` is an upper bound only (`if len(canonical) > 1`), so a scope can own zero Canonical documents and no rule cares.

That line is correct. `scripts/check_document_management.py:1257`:

```python
if len(canonical) > 1:
    errors.append(...)
```

There is no `len(canonical) == 0` branch. Confirmed by reading and by `grep`.

**But the scope-owning-zero-Canonical state is not the silent one, and it is not reachable in the way described.** I counted every declared scope in the tree:

```
distinct declared scopes: 13
scopes with ZERO Canonical documents: 1
  null
```

Only one, and its id is the string `null`.

### 4.1 The actual defect: `canonical_scope_id: null` is silently discarded

Three files under `07-agent-integration/` declare:

```yaml
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Agent Adapter capability tier specification"
    canonical_scope_id: null
```

- `07-agent-integration/adapter-capability-tiers.zh-CN.md`
- `07-agent-integration/agent-integration-architecture-completion.md`
- `07-agent-integration/agent-integration-guide.md`

YAML parses `null` to `None`. The gate reads it at `:1249`:

```python
scope_id = dig(meta, "authority", "canonical_scope_id")
if scope_id:
    scopes.setdefault(str(scope_id), []).append(rel)
```

`None` is falsy, so the document is **dropped from the scope map entirely**. It is not registered under a scope with zero members — it is not registered at all. DM-07 never sees it, DM-11 never sees it, and `resolve_canonical()` cannot be asked about it because no caller knows the scope exists.

This is worse than #630 describes. #630's state is "a scope exists with no canonical owner, and nothing complains". The actual state is "a document claims a scope, the claim is unreadable, and the document leaves the graph silently". The `canonical_scope` prose is present and non-empty on all three; only the id is `null`, so the document is asserting an authority scope it is not actually declaring.

### 4.2 Why DM-06 does not catch it

DM-06 at `:1042` requires `canonical_scope_id` when `canonical in ("Canonical", "Candidate")`. All three files are `Non-Canonical`, so DM-06 does not apply and `null` is accepted as "not declared".

That is defensible in isolation — a `Non-Canonical` document is not claiming authority, so it need not scope itself. What is not defensible is that it *does* claim a scope in prose and sets the id to the literal `null` rather than omitting the key. The two are indistinguishable to the gate and distinguishable to a reader.

### 4.3 The fix, and it is two lines

Either is sufficient; the first is honest about intent.

**Option A — reject the literal.** A `canonical_scope_id` key that is present with a null value is a declaration the author made and then emptied. Treat it as an error:

```python
raw_scope = authority.get("canonical_scope_id", "<absent>")
if raw_scope is None:
    errors.append(
        "DM-06 canonical_scope_id is present but null; omit the key "
        "or declare '<domain>/<kebab-case>'"
    )
```

This makes the three files fail, which is correct — they currently say something they do not mean.

**Option B — add the lower bound #630 asks for.** After the `len(canonical) > 1` branch:

```python
if not canonical:
    errors.append(
        f"DM-07 scope {scope_id!r} has no Canonical document; "
        "a declared scope must resolve to at least one owner"
    )
```

Option B alone would not catch these three files, because they are not in the scope map. Option A alone would. **Both are needed for different reasons**: A catches the dropped documents, B catches genuinely orphaned scopes.

## 5. What this changes about #630

- The reported line (`:1257`, upper bound only) is accurate.
- The reported consequence (a scope can own zero Canonical documents silently) is **not** what is happening. There is one such scope in the tree, and its id is `null`, which means it is not really a scope.
- The measured defect is **three documents dropping out of the scope graph** because a null value is falsy at `:1249`.
- The lower bound is still worth adding, but it is the smaller of the two fixes and would not have caught the live instance.

## 6. Why this matters

The gate has 563 `DM-01` errors, all of them the adoption backlog, and zero rule violations. That reads as "the tree is compliant". Three documents are asserting scopes that the gate cannot see, and one of the two rules that would notice is an upper bound only.

A gate that is silent about a state is not the same as a gate that approves of it. The distinction is only visible if someone counts, and nobody had counted the zero-member scopes before this document. The number is one, and it is not what it appears to be.
