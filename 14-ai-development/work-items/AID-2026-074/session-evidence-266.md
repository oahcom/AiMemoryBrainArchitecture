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
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "All forty-nine manifests were parsed on 2026-11-25 from the committed tree with a duplicate-key-rejecting SafeLoader; the four failures were each repaired and their affected scalars re-parsed and compared to the pre-edit text byte-for-byte. The claims about gate coverage were read from the checker source, not inferred from a green run."
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Session role / use case

MEASURER, then registrant. This session found four unparseable work-item manifests while
auditing the register for something else, repaired them, and registered the missing check
so the next occurrence fails a gate instead of waiting for a human to notice.

The order is recorded honestly rather than presented as a clean sequence: the repairs
came first because they were cheap and the defect was live, and the work item for the
check was registered after. That means the check will be written against a tree that is
already green, which makes its negative test the only thing that can prove it works.

# Actual AI input

**Committed, byte-exact.** `prompt-v1.md` in this directory is the instruction this
registration was carried out against. It is the file the manifest pins by digest
(`79aa1749585cd105be73bea8b8ef42aa1eedd6c47b3e6769c454c727e1058f67`, 5476 bytes).

**Read before writing:**

| input | what it settled |
|---|---|
| `FIX-2026-P1-MANIFEST-YAML-001/audit-record.md` | the class already occurred once, on 2026-11-19, as `M-1`..`M-4`; its §4 states "No workflow wiring", which is why it recurred |
| `scripts/ci/check_repository_hygiene.py:586` | `_top_level_manifest_scalar` is a regex over unindented lines; the manifest check never constructs a document |
| `scripts/governance/status_migration/check_status_gates.py:12` | the only `import yaml` over manifest content, and no workflow invokes it |
| `scripts/governance/status_migration/test_status_migration.py` | its tests build their own `manifest.yaml` fixtures under a temp dir, so they cannot see a repository manifest |
| `AID-2026-057/manifest.yaml` | Owner ruling R6 admits the ten A/B groups (78 paths); its `implementation.note` records 83 admitted / 30 refused over the 113-path inventory |

`executed_prompt_provenance` is `NOT_VERIFIED`: the digest proves the committed file has
not changed since it was pinned, not that it is byte-for-byte what the platform showed.

# Measurements this session took

**Strict parse over all 49 `AID-*/manifest.yaml` at `30c7277e`, duplicate-key-rejecting
SafeLoader:**

```
parsed ok 45   failed 4

AID-2026-023  ScannerError       mapping values are not allowed here
                                 line 18 col 66: (session identity: NOT_RECORDED)
AID-2026-029  ConstructorError   duplicate key 'related_prs'  line 9 col 1
AID-2026-040  ScannerError       mapping values are not allowed here
                                 line 15 col 98: ... in this session: "所有 owner ...
AID-2026-055  ParserError        while parsing a block collection
                                 line 160 col 3: - "A required status check on ma ...
```

**The silent case.** `AID-2026-029` under plain `yaml.safe_load`:

```
related_prs = []
top keys 24
```

Line 8 is `related_prs: [356]` and line 9 is `related_prs: []`. The loader keeps the
second and discards PR 356, which is the PR that carried that work item's implementation
(`02136d14`, "[Issue #264] Repair and dereference source revision pointers"). No error is
raised. This is the shape a checker built on `safe_load` alone cannot see.

**After repair — 49/49 parse, every affected scalar byte-identical:**

| file | change | value preserved |
|---|---|---|
| `AID-2026-023` | `implementing_ai_session` wrapped in double quotes | yes |
| `AID-2026-029` | the duplicate `related_prs: []` deleted, `[356]` kept | yes (and 356 is no longer dropped) |
| `AID-2026-040` | `sponsor`, `accountable_owner` wrapped, inner quotes escaped | yes, both |
| `AID-2026-055` | inner `"` escaped in `deliverables[0]` and `[1]` | yes, both |

**Gap this session could not close, and did not claim to:** the checker does not exist.
`scripts/ci/check_manifest_parse.py`, its tests and the workflow step are `NOT_STARTED`.

# What this record does not claim

- It does not claim the four manifests are now *correct*. They are now *parseable*. Field
  semantics, cross-file consistency and whether `related_prs: [356]` was the right value
  are different questions and were not opened.
- It does not claim `FIX-2026-P1-MANIFEST-YAML-001` was wrong. Its repair was correct and
  its own audit record named the missing wiring; this session is the second time that
  limit cost a set of files.
- It does not claim independent review. No reviewer has read this manifest.
