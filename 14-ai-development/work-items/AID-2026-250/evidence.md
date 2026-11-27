# Evidence — AID-2026-250

## Scope and baseline
- Base: `386d8f57b02d8e3c511ff0e3980b9ce0af8b3028`
- Branch: `w7/aid-250`
- Related Issue: #262
- Four reports: SYS-RISK-001 EN/ZH-CN and architecture-complexity-assessment EN/ZH-CN.

## Historical provenance boundary
All four reports identify historical baseline `b372b62c640a2b656e54b6db62a4ee67d7d8c001`. The metadata preserves that source baseline. SYS-RISK-001 does not record the original assessor session identity; that limitation is disclosed. The attachment does not retroactively prove a contemporaneous signature.

## Checker evidence
- Checker and tests: `scripts/ci/check_req_assessment_signatures.py`, `scripts/ci/test_check_req_assessment_signatures.py`.
- Exact PR Head execution and output: PENDING CI; no unexecuted result is represented as PASS.

## Integration
Reuse the existing `work-item-manifest-schema` job. No new job/context, branch-protection mutation, Issue body change, or Issue closure.
