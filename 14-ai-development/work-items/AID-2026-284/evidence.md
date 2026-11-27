# Evidence — AID-2026-284

## 1. Purpose and scope

This carrier replaces the conflicting AC8 exclusion claim in AID-2026-260 with the disposition already established by AID-2026-280: AC8 remains in REQ-04 scope and is ABSENT. It does not edit AID-2026-260, the Issue #265 body, or any unrelated carrier.

## 2. Repository blob evidence (offline-recomputable)

| Source | Immutable blob | Relevant location | Finding |
|---|---|---|---|
| `14-ai-development/work-items/AID-2026-260/scope-confirmation.md` | `e6425787d2ae3c8aa3e2eb21e1adf7cc1542611a` | lines 69, 82 | line 69 records AC8 as EXCLUDED; line 82 says EXIT-2 remains the sole effective disposition |
| `14-ai-development/work-items/AID-2026-280/decision.md` | `3cde57f77fa9c93a702eaab0f3164f27c70c4573` | lines 75, 105–112 | line 75 rules EXIT-2 ineffective; lines 105–112 name the seven closure evidence units |
| `00-governance/architecture-document-management-policy.md` | `f3cb0caee4653bbff645b129bb2aa538a13c6262` | lines 166, 212, 248, 435 | decision_status enum; verification_status enum; superseded_by is CI-derived and must not be written back; M-02 does not verify that an approval exists |
| `14-ai-development/work-items/AID-2026-254/evidence.md` | `02567b538a87e52361a78cb3eaea1fe00d79cee9` | lines 98, 107 | root/domain fan-out is a proxy; does not measure actual human attention or context transitions |
| `scripts/measure_attention_context_cost.py` | `fe80f67332145748acd7b8cd1485743154f337e4` | lines 1–6 | script is a read-only declared root/domain fan-out measurement |

Recompute source blobs and line locations from a repository checkout:

```sh
git cat-file -p e6425787d2ae3c8aa3e2eb21e1adf7cc1542611a
git cat-file -p 3cde57f77fa9c93a702eaab0f3164f27c70c4573
git cat-file -p f3cb0caee4653bbff645b129bb2aa538a13c6262
git show <base>:14-ai-development/work-items/AID-2026-260/scope-confirmation.md | nl -ba | sed -n '69p;82p'
git show <base>:14-ai-development/work-items/AID-2026-280/decision.md | nl -ba | sed -n '75p;105,112p'
git show <base>:00-governance/architecture-document-management-policy.md | nl -ba | sed -n '166p;212p;248p;435p'
git show <base>:14-ai-development/work-items/AID-2026-254/evidence.md | nl -ba | sed -n '98p;107p'
git show <base>:scripts/measure_attention_context_cost.py | nl -ba | sed -n '1,6p'
```

The policy line numbers above were read from the current 489-line file before authoring this evidence. In particular, the requested policy anchors are not line 143/210: the current actual anchors are 166 (decision_status), 212 (verification_status), 248 (single-direction supersession declaration), and 435 (M-02).

## 3. GitHub-hosted facts (not offline-recomputable)

Issue #265's current body was fetched from the GitHub Issue API. It still contains AC1 as an unchecked OWNER_ACTION item and AC8 as an unchecked ABSENT criterion. The body was not patched.

Issue #305 comment 7042461592 was fetched from the GitHub Issue Comments API. It is the delegation instrument. Its boundary is not silently enlarged by this work item. The relevant record must be re-read from GitHub:

```sh
gh api repos/oahcom/AiMemoryBrainArchitecture/issues/265
gh api repos/oahcom/AiMemoryBrainArchitecture/issues/comments/7042461592
```

These two facts cannot be independently recomputed from repository Git blobs alone. They are therefore explicitly excluded from the offline-recomputable set and the scope document remains Unverified.

## 4. Disposition

AID-2026-260 is superseded by this new carrier through the new document's forward `supersedes` declaration only. Policy §6.2 (current line 248) makes `superseded_by` CI-derived and forbids writing it back into the source document. No source file in AID-2026-260 is modified.

AC8 remains in scope, is not satisfied, and has status ABSENT with direct-measurement carrier NO_CARRIER_FOUND. AID-2026-254 remains an optional out-of-scope proxy observation and is not an AC8 acceptance carrier. AC1 remains unchecked pending Owner confirmation; AC9 remains NOT YET JUDGEABLE.
