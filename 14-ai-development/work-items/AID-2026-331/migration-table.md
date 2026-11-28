---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-331/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Nine reference declarations are transcribed from supplied observations. Prompt snapshot byte counts are supplied; complete digest and execution-commit provenance values remain unverified."
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
    canonical_scope: "Migration record for the three reference families under Issue #1350"
    canonical_scope_id: "ai-development/aid-2026-331-migration-table"
    canonical_scope_keywords:
      - "authored_indexes"
      - "related_evidence"
      - "executed_prompt_snapshot_file"
      - "migration"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Migration Table — AID-2026-331

## 1. Migration rules

This table records the migration required by both Owner decisions.

- **Option C:** preserve the six `authored_indexes[]` digests and classify them as historical authorship references.
- **Option C:** preserve the three `related_evidence[0]` digests and add `reference_mode: historical` to the containing entry.
- **`PROMPT-SNAPSHOT-REFERENCE-SEMANTICS-001`:** preserve the declared prompt snapshot digest and byte count for AID-2026-101 and AID-2026-102. Reclassify those declarations as point-in-time session evidence, not candidate-tree assertions.
- Do not rewrite any of the eleven declared digest/byte-count records to make candidate-tree comparisons green.

The nine historical-reference observations report that each declared blob exists in the history of its corresponding exact path and that the later path edits were independent work. For the two prompt-snapshot records, the Owner explicitly reclassifies the four candidate-tree findings as false positives. The recorded execution commit or unambiguous entry history must still be assessed.

## 2. Nine authored-index and related-evidence declarations

| Field | Path | Declared blob | Current blob | Assigned semantics / mode | Migration action |
|---|---|---|---|---|---|
| `authored_indexes[0].root` | `05-memory-runtime/README.md` | `107c225b631eaa5732bab90bc09144799a542502` | `216760a45c54386b95c2c985f7bf188d7479f776` | Historical authorship reference | Preserve digest; reclassify as historical. The declared blob is reported in this exact path's history. The later current blob does not falsify the historical reference; changing the digest would replace the historical record, not repair it. |
| `authored_indexes[0].en_mirror` | `docs/en/05-memory-runtime/README.md` | `2fac42740167293c941c1450437ca780d0488b5d` | `8808e9b298c78c2c4c64a9675b27e973c0e996bc` | Historical authorship reference | Preserve digest; reclassify as historical. The declared blob is reported in this exact path's history. The later current blob does not falsify the historical reference; changing the digest would replace the historical record, not repair it. |
| `authored_indexes[0].zh_cn_mirror` | `docs/zh-CN/05-memory-runtime/README.md` | `9881fd88fcbfe1b3760154503c8d13e781ad89f0` | `c945394cf4aa667874938d64fc1c2b551d3ad5a9` | Historical authorship reference | Preserve digest; reclassify as historical. The declared blob is reported in this exact path's history. The later current blob does not falsify the historical reference; changing the digest would replace the historical record, not repair it. |
| `authored_indexes[1].root` | `09-security-governance/README.md` | `1046665b0990183b689ed6db88edc9ba1089c83e` | `37b4c8a7f6b807bc22e9f278106972cbe84af8c8` | Historical authorship reference | Preserve digest; reclassify as historical. The declared blob is reported in this exact path's history. The later current blob does not falsify the historical reference; changing the digest would replace the historical record, not repair it. |
| `authored_indexes[1].en_mirror` | `docs/en/09-security-governance/README.md` | `7c8b434c7161c47c5e35e0ffcadc736981996c4a` | `9edb8239b2bc34922a0618f5645ca27c6d8d1eb1` | Historical authorship reference | Preserve digest; reclassify as historical. The declared blob is reported in this exact path's history. The later current blob does not falsify the historical reference; changing the digest would replace the historical record, not repair it. |
| `authored_indexes[1].zh_cn_mirror` | `docs/zh-CN/09-security-governance/README.md` | `772025aa9da8afe706af6f607ae47e35c5020522` | `6b2c25ba19f11cdd58d4ad1558373be8c2026f1d` | Historical authorship reference | Preserve digest; reclassify as historical. The declared blob is reported in this exact path's history. The later current blob does not falsify the historical reference; changing the digest would replace the historical record, not repair it. |
| `related_evidence[0].path` | `14-ai-development/work-items/AID-2026-100/evidence.md` | `87adf4a8cde8ba5c4c14596932f3488ec988a38c` | `ae46c7a4424778d0c8e4c5b21c6535023a9b460d` | `reference_mode: historical` | Preserve digest; add `reference_mode: historical` to the containing `related_evidence[0]` entry. The declared blob is reported in this exact path's history; later independent edits do not falsify it. No digest repair. |
| `related_evidence[0].en_mirror` | `docs/en/14-ai-development/work-items/AID-2026-100/evidence.md` | `da156fe2409f17b364e9af65446bb73ab709e539` | `425e5eaf6c99286342e20f5ecf525ee297d75e0c` | `reference_mode: historical` | Preserve digest; add `reference_mode: historical` to the containing `related_evidence[0]` entry. The declared blob is reported in this exact path's history; later independent edits do not falsify it. No digest repair. |
| `related_evidence[0].zh_cn_mirror` | `docs/zh-CN/14-ai-development/work-items/AID-2026-100/evidence.md` | `d750ef5555916bfb82180f30a6e83b3a0766fdfc` | `fda38f1355f6160db78facde996fee3345905ea1` | `reference_mode: historical` | Preserve digest; add `reference_mode: historical` to the containing `related_evidence[0]` entry. The declared blob is reported in this exact path's history; later independent edits do not falsify it. No digest repair. |

## 3. Two executed prompt snapshot records

The four candidate-tree findings consist of one digest finding and one byte-count finding for each session. The Owner ruling classifies all four as false positives caused by applying candidate-tree equality to a point-in-time evidence family.

| Field | Path | Declared digest | Declared bytes | Current digest | Current bytes | Disposition and migration action |
|---|---|---|---:|---|---:|---|
| `AID-2026-101.session_evidence[0].executed_prompt_snapshot_file` | `14-ai-development/work-items/AID-2026-101/prompt-v1.md` | `NOT_VERIFIED` | 4470 | `NOT_VERIFIED` | 4412 | Reclassify as point-in-time session evidence; preserve declared digest and byte count; no rewrite. The candidate-tree digest and byte-count findings are false positives under the Owner's ruling. Verify snapshot bytes against the session-recorded commit or unambiguous entry history; assess missing commit provenance separately. |
| `AID-2026-102.session_evidence[0].executed_prompt_snapshot_file` | `14-ai-development/work-items/AID-2026-102/prompt-v1.md` | `NOT_VERIFIED` | 4470 | `NOT_VERIFIED` | 4412 | Reclassify as point-in-time session evidence; preserve declared digest and byte count; no rewrite. The candidate-tree digest and byte-count findings are false positives under the Owner's ruling. Verify snapshot bytes against the session-recorded commit or unambiguous entry history; assess missing commit provenance separately. |

`NOT_VERIFIED` means the complete SHA-256 value is not established in the evidence used to prepare this table. It is not a replacement digest and must not be written into either manifest. The execution commit or unambiguous entry history is also not established here. No commit identifier is inferred.

## 4. Required related-evidence migration shape

The key belongs inside the existing `related_evidence[0]` mapping, alongside its existing path, mirror, and blob declarations:

```yaml
related_evidence:
  - reference_mode: historical
    # Preserve all existing path, mirror, and blob declaration values.
```

This is the required target shape. This documentation-only work item does not apply the change to `AID-2026-100/manifest.yaml`.

## 5. Prompt snapshot checker boundary

The blob-pin checker must stop asserting candidate-tree digest and byte-count equality for `session_evidence[].executed_prompt_snapshot_file`.

Session Evidence validator check 11 remains the enforcing PR-head-tree gate for `executed_prompt_sha256` and `executed_prompt_bytes`. Historical verification of the executed snapshot remains a Session Evidence provenance responsibility.

If a session entry does not identify a commit sufficiently to resolve the declared snapshot unambiguously, record a separate missing historical-provenance defect. Do not substitute candidate-tree bytes or rewrite declarations.

## 6. Migration boundary

This table does not:

- rewrite any of the nine authored-index or related-evidence digests;
- rewrite either prompt-snapshot digest or byte-count declaration;
- substitute current prompt-file bytes for the historical session snapshots;
- restore either current prompt-v1.md solely to satisfy the blob-pin check;
- modify any existing manifest;
- change the blob-pin checker, Session Evidence validator, workflow, or prompt/evidence template;
- weaken or remove Session Evidence check 11;
- claim that AID-2026-101/-102 historical provenance has been resolved;
- constitute AID-2026-255 acceptance;
- close or accept Issue #1350.

AID-2026-336 implements the checker behavior. Migration and provenance verification remain evidence-producing work, not completed outcomes asserted by this table.
