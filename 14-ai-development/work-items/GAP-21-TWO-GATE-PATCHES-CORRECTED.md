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
      last_verified_date: "2026-11-22"
      last_verification_note: "The 50/15/17/0 counts are produced by scanning every *.md with a document_metadata block at main @ 1a7e3cddae and reading canonical_scope_id and canonical_status out of the frontmatter. The DM-06 guard at :1040 and the drop at :1249 are read from the script itself."
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

# GAP-21 (corrected) — the two gate patches, with the false positives I missed

**Status:** Open — one patch stands, one is replaced
**Measured at:** `main` @ `1a7e3cddae`
**Supersedes:** `GAP-21-TWO-ONE-LINE-GATE-PATCHES.md` §2 (defect A) — see §2 below
**Author:** owner delegate under standing instruction (Issue #564, comment 7074302216)

---

## 1. What I got wrong

The first version of this document proposed treating every `canonical_scope_id: null` as an error. I wrote it from three files I had found by hand, and I generalised from them.

There are not three. Measured on the tree:

```
docs with document_metadata:            50
  canonical_scope_id present but null:  15
  canonical_scope_id absent:            17
Canonical or Candidate with null scope:  0
```

Fifteen documents declare `canonical_scope_id: null`. **Zero of them are `Canonical` or `Candidate`.** All fifteen are `Non-Canonical` — they opted out of the canonical scope graph by status, and `null` is the honest way to say "this document is not canonical of anything".

My patch would have produced fifteen false positives on the first run, and the three files I started from were a coincidence of my sample rather than a pattern.

## 2. Why the three files I found were still a real finding

The original observation was not wrong, only over-generalised. `check_document_management.py:1040` applies DM-06 under:

```python
if canonical in ("Canonical", "Candidate"):
```

So a `null` scope is only a defect when the document claims canonical status. Among the fifteen, none does — today. The three files I named carry non-empty `canonical_scope` prose while declaring `canonical_scope_id: null`, and that combination is still worth a check, but the check is **not** "null is invalid". It is "null contradicts a non-empty scope description":

| state | correct? |
|---|---|
| `canonical_status: Non-Canonical`, `canonical_scope_id: null`, no scope prose | correct — opted out cleanly |
| `canonical_status: Non-Canonical`, `canonical_scope_id: null`, **scope prose present** | **contradictory** — prose describes a scope the id denies |
| `canonical_status: Canonical`, `canonical_scope_id: null` | already caught by DM-06 at `:1044` |

That third row is why my patch was redundant as well as wrong: DM-06 already refuses a Canonical document without a scope id. The case that reaches the grouping code at `:1249` and gets silently dropped is only ever a `Non-Canonical` document, which is exactly the document that should be dropped.

## 3. The corrected patch A

Replace `:1249`–`:1251`:

```python
        authority = meta.get("authority") if isinstance(meta.get("authority"), dict) else {}
        scope_id = authority.get("canonical_scope_id")
        scope_prose = authority.get("canonical_scope")
        if scope_id is None:
            # `null` is legitimate for a Non-Canonical document that describes no
            # scope. It is contradictory when the same block carries scope prose:
            # the prose claims a scope the id denies. DM-06 already refuses a
            # Canonical document with no scope id, so this branch only ever sees
            # Non-Canonical documents and must not treat null itself as an error.
            if isinstance(scope_prose, str) and scope_prose.strip():
                errors.append(
                    f"DM-07 {rel}: authority.canonical_scope_id is null but "
                    "authority.canonical_scope is non-empty; name the scope or "
                    "remove the prose"
                )
            continue
        scopes.setdefault(str(scope_id), []).append(rel)
```

Three differences from what I proposed before, each traceable to the measurement:

1. **`null` alone is not an error.** Fifteen documents do it correctly.
2. **The error condition is the contradiction**, not the value. Prose without an id is a document describing something the gate cannot index.
3. **The comment states the reason the branch can only see Non-Canonical documents**, so the next reader does not "fix" it back into an unconditional error.

## 4. The count this changes

Under the corrected patch, the expected new errors are **three**, not fifteen — the three files named in the original document:

- `07-agent-integration/adapter-capability-tiers.zh-CN.md`
- `07-agent-integration/agent-integration-architecture-completion.md`
- `07-agent-integration/agent-integration-guide.md`

If a run reports more than three, the patch is catching something I did not measure and should be read before it is applied.

## 5. Patch B stands unchanged

DM-07's missing lower bound is unaffected by any of the above:

```
:1259   if len(canonical) > 1:
```

Add after it:

```python
        if not canonical:
            errors.append(
                f"DM-07 scope {scope_id!r} owns 0 Canonical documents; "
                "a declared scope must resolve to at least one Canonical document"
            )
```

The ordering dependency from the original document still holds, and is now narrower: apply patch A first, because it removes the only `null`-derived scope from the grouping, and patch B then has nothing spurious to report.

## 6. What this correction demonstrates

I generalised a rule from three hand-found instances without counting the population. The population was 50 documents, and the count took one script and less than a minute. The same minute would have told me that fifteen do this and none of them is canonical.

The pattern is the one `GAP-20` §6 named from the other direction: I had three examples of a thing and wrote a rule for the class. Three examples is enough to notice, not enough to legislate. The measurement that would have prevented it is the one this document now contains.

## 7. What stands from the original

- **Patch B and its ordering dependency** — unchanged.
- **The verification commands** in §5 of the original — unchanged, except that the `grep 'present but null'` check is replaced by `grep 'is null but'` and the expected count is 3.
- **The 563 baseline claim** — corrected elsewhere: it is 566 at `1a7e3cddae`, and the earlier number was quoted from a run whose `DM-10` component had not executed (`GAP-25`).
