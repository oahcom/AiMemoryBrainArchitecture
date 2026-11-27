# AID-2026-250 — implementation prompt

Repository: oahcom/AiMemoryBrainArchitecture
Base: main@386d8f57b02d8e3c511ff0e3980b9ce0af8b3028
Branch: w7/aid-250
Issue: #262

Add assessor, assessed_version and evidence_baseline metadata to SYS-RISK-001 EN/ZH-CN and architecture-complexity-assessment EN/ZH-CN. Preserve each report's historical baseline and disclose provenance limits; do not fabricate a contemporaneous session signature. Add a deterministic read-only checker and tests under scripts/ci/. Run it in the existing work-item-manifest-schema job, without creating a new job or required context. Do not modify Issue #262 body or close it.
