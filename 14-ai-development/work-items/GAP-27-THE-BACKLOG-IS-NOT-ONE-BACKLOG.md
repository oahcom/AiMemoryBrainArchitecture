---
document_metadata:
  domain: ai-development
  role: review-report

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-22"
      last_verification_note: "The 567 total and the per-directory table come from check_document_management.py --strict at f292257a98. The 48 prompt-shaped files are counted by filename pattern over that same output, which the document states is a proxy needing review before any exemption is written."
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

# GAP-27 — The 567 backlog is not one backlog: 48 of it is prompts, and the repo already treats them differently

**Status:** Open · **Area:** `check_document_management.py` DM-01 scope
**Measured at:** `main` @ `f292257a98`
**Author:** owner delegate under standing instruction (Issue #564, comment 7074302216)

---

## 1. The number, and what it is made of

`check_document_management.py --strict` at `f292257a98`:

```
FAIL: 567 error(s)
  567 DM-01
   13 DM-10   (tarball artifact — GAP-25)
```

By top-level directory:

| directory | DM-01 |
|---|---:|
| `docs/` | 235 |
| `14-ai-development/` | 213 |
| `13-engineering-decisions/` | 58 |
| `06-memory-context/` | 21 |
| `02-domain-model/` | 12 |
| `00-governance/` | 10 |
| `01-system-architecture/` | 7 |
| `08-bmcp-protocol/` | 6 |
| `07-agent-integration/` | 3 |
| `04-memory-compiler/` | 2 |

That is a real backlog and it needs working. But one slice of it is a different kind of thing:

**48 of the 567 are prompt and task files** — 8.5 percent.

```
14-ai-development/prompts/global/chatgpt-session-contract-v1.md
14-ai-development/prompts/owners/A/owner-session-v1.md
14-ai-development/prompts/owners/B/owner-session-v2.md
14-ai-development/work-items/AID-2026-049/prompt-v1.md
14-ai-development/work-items/AID-2026-001/integration-review-prompt.md
14-ai-development/prompt-and-evidence-template.md
...
```

## 2. Why this slice is different, and the repository already says so

`check_bilingual_docs.py:35`:

```python
PAIR_EXEMPT_PREFIXES = (
    "14-ai-development/work-items/",
    "14-ai-development/prompts/",
    "14-ai-development/adr/",
)
```

The bilingual gate exempts prompts from pairing. The reason is obvious once stated: a prompt is an instruction to a model, not a normative statement about the system. It has no Chinese counterpart because nobody reads it in Chinese, and translating it would change the thing it is — a prompt whose wording matters would be a different prompt after translation.

`DM-01` does not know this. It applies to every `.md` with no `document_metadata` block, and it has no exemption list at all. So a file the repository has already decided is not a normative document still owes the full normative frontmatter: `domain`, `role`, `lifecycle.approval`, `lifecycle.usage_status`, `lifecycle.modification_status`, `lifecycle.supersession`, `authority.canonical_status`, `authority.canonical_conflict_status`, `authority.normative_status`.

For `AID-2026-049/prompt-v1.md` — a task brief that says "TASK 360 — second repair: the module duplicates a type `main` already has" — that frontmatter is not merely absent, it is meaningless. What is the `canonical_status` of a prompt? What would `Approved` mean for an instruction to a model that was written and dispatched in the same hour?

## 3. The two readings, and why only one is right

**Reading A: the 48 are defects.** They are `.md` files, DM-01 says every `.md` needs metadata, so add it. Cost: 48 files × 9 fields, most of them semantically empty, and a permanent maintenance burden every time a prompt is revised.

**Reading B: DM-01's scope is wrong for this class.** The repository already distinguishes prompts from documents in `PAIR_EXEMPT_PREFIXES`. DM-01 should make the same distinction, with the same list.

I think B is right, and the argument is not "it is inconvenient." It is that **a field which is always filled with a placeholder carries no information**, and a gate that forces it teaches everyone to fill placeholders. That is how a metadata system stops being read.

The counter-argument deserves stating: an exemption list is where things hide. `GAP-24` is exactly that failure — a `zh-CN` file that passes because the check resolves a path and never reads the file. Adding a DM-01 exemption for `prompts/` could hide a real normative document that was placed there.

The answer to that is to make the exemption **narrow and named**, not prefix-based:

- `14-ai-development/prompts/**` — prompts, exempt, with the reason `PAIR_EXEMPT_PREFIXES` already gives.
- `14-ai-development/work-items/*/prompt*.md` and `**/*-prompt.md` — task briefs, exempt.
- Everything else under `work-items/` — **not** exempt. `GAP-10-IMPLEMENTATION-FRONTIER.md` is a work record and should have metadata; it currently does not, and that is a real DM-01.

A prefix exemption for all of `work-items/` would sweep 213-ish files under `14-ai-development/` into silence, which is the `GAP-24` failure at scale.

## 4. What I am not proposing

**Not lowering the number.** The 519 remaining are documents and they need metadata. This is not a way to make the gate green.

**Not exempting `14-ai-development/` wholesale.** 213 of its files are DM-01 and most are work records, reviews and registers that should carry metadata. Only the prompt-shaped ones should not.

**Not doing it before the 48 are counted precisely.** I counted by filename pattern (`prompt|task`), which is a proxy. Before any exemption is written, the exact set should be enumerated and reviewed, because a wrong exemption is worse than a missing one — it is invisible forever after.

## 5. The measurement, so it can be repeated

```bash
python3 scripts/check_document_management.py --strict 2>&1 \
  | grep 'DM-01 missing' \
  | sed 's/.*block: //' \
  | grep -icE 'prompt|task'
```

At `f292257a98` that prints `48`. The per-directory table in §1 comes from the same output with `cut -d/ -f1 | sort | uniq -c`.

Both are approximations of the question "how many of these are not documents." The exact answer needs a human reading 48 paths, and 48 is small enough to read.

## 6. Why this is worth writing down

Because the backlog has been quoted as a single number — 563, then 564, then 566, now 567 — for the whole of this session, and every time it was quoted it was described as "all DM-01" as though DM-01 were one kind of thing.

It is at least two: documents that need metadata, and prompts that cannot meaningfully have it. The repository already distinguishes them for bilingual pairing. Nobody has asked whether DM-01 should, and the number has been growing by one prompt at a time — `AID-2026-049/prompt-v1.md` arrived in `8a599491ff`, an unrelated context commit, as a side effect.

A backlog that grows as a side effect of unrelated work is not being managed. It is being counted.
