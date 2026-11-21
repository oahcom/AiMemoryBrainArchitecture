# Issue #407 — Zero-CJK File Disposition (First Batch)

**Scope:** The 50 files in `scripts/bilingual-baseline.txt` under `14-ai-development/` whose current file contents contain zero characters in U+4E00–U+9FFF. This is a disposition inventory only; it does not authorize mirrors, translations, exemptions, or archival.

**Method:** Read each of the 125 baseline paths under `14-ai-development/`, counted CJK Unified Ideographs in the file contents, and selected exactly 50 with a count of zero. Line counts use `splitlines()` on the current file contents. Pair shape identifies a gate-accepted structural option; no counterpart was created. Classification is a review disposition: transient work-item artifacts are scoped prompts, execution/evidence records, test designs, errata, and work-item support docs; durable artifacts are reusable policy/ADR/ruling/register/index/template documents.

| Path | Lines | Accepted pair shape that fits | Disposition |
|---|---:|---|---|
| `14-ai-development/AI-EXEC-INDEPENDENCE-RULING-001.en.md` | 165 | `AI-EXEC-INDEPENDENCE-RULING-001.en.md` + `AI-EXEC-INDEPENDENCE-RULING-001.md` (X.en.md + X.md) | Standing policy (durable) |
| `14-ai-development/PR-MERGE-EVIDENCE-SUMMARY-001.en.md` | 93 | `PR-MERGE-EVIDENCE-SUMMARY-001.en.md` + `PR-MERGE-EVIDENCE-SUMMARY-001.zh-CN.md` (X.en.md + X.zh-CN.md) | Work-item prompt/log (transient) |
| `14-ai-development/adr/ADR-RUN-002-github-app-webhook-security-and-secrets.en.md` | 234 | `ADR-RUN-002-github-app-webhook-security-and-secrets.en.md` + `ADR-RUN-002-github-app-webhook-security-and-secrets.md` (X.en.md + X.md) | Standing policy (durable) |
| `14-ai-development/adr/ADR-RUN-003-owner-worker-isolation-and-execution-boundary.en.md` | 181 | `ADR-RUN-003-owner-worker-isolation-and-execution-boundary.en.md` + `ADR-RUN-003-owner-worker-isolation-and-execution-boundary.md` (X.en.md + X.md) | Standing policy (durable) |
| `14-ai-development/bilingual-tiering-policy.en.md` | 101 | `bilingual-tiering-policy.en.md` + `bilingual-tiering-policy.md` (X.en.md + X.md) | Standing policy (durable) |
| `14-ai-development/evidence-tiering-policy.en.md` | 136 | `evidence-tiering-policy.en.md` + `evidence-tiering-policy.md` (X.en.md + X.md) | Standing policy (durable) |
| `14-ai-development/governance-register/GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004.en.md` | 323 | `GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004.en.md` + `GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004.md` (X.en.md + X.md) | Standing policy (durable) |
| `14-ai-development/governance-register/GOV-NC-2026-11-20-MERGE-AFTER-RULING-003.en.md` | 298 | `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003.en.md` + `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003.md` (X.en.md + X.md) | Standing policy (durable) |
| `14-ai-development/governance-register/GOV-NC-CONVERGENCE-2026-11-20.en.md` | 161 | `GOV-NC-CONVERGENCE-2026-11-20.en.md` + `GOV-NC-CONVERGENCE-2026-11-20.md` (X.en.md + X.md) | Standing policy (durable) |
| `14-ai-development/governance-register/README.en.md` | 88 | `README.en.md` + `README.md` (X.en.md + X.md) | Standing policy (durable) |
| `14-ai-development/status-migration-map.en.md` | 36 | `status-migration-map.en.md` + `status-migration-map.zh-CN.md` (X.en.md + X.zh-CN.md) | Standing policy (durable) |
| `14-ai-development/work-items/ADOPTION-EVIDENCE-2026-P1/adoption-evidence-dossier.md` | 137 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/ADOPTION-EVIDENCE-2026-P1/adoption-record-template.md` | 55 | `docs/en/<path>` + `docs/zh-CN/<path>` | Standing policy (durable) |
| `14-ai-development/work-items/AID-2026-001/prompt-v1.md` | 52 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/erratum-003.md` | 32 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/erratum-004.md` | 40 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-002.md` | 101 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-003.md` | 85 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-004.md` | 77 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-005.md` | 104 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-006.md` | 85 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-007.md` | 39 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-008.md` | 98 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-009.md` | 40 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-010.md` | 80 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-011.md` | 72 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-012.md` | 30 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-013.md` | 74 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-014.md` | 65 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-015.md` | 65 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-016.md` | 163 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-017.md` | 291 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-018.md` | 278 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/reference-model/EXECUTION-RECORD.md` | 64 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/reference-model/R3-RUNBOOK.md` | 57 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-001/reference-model/README.md` | 75 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-002/prompt-v1.md` | 61 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-003/prompt-v1-errata.md` | 90 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-009/test-design/NESTED-CLAIM-MULTI-SCOPE-DISCLOSURE.md` | 68 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-009/test-design/NESTED-CLAIM-MULTI-SCOPE-WRITE.md` | 66 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-011/prompt-v1.md` | 152 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-023/prompt-v1.md` | 199 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-024/prompt-v1.md` | 198 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-024/prompt-v2.md` | 293 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-025/prompt-v1.md` | 184 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-026/prompt-v1.md` | 153 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/AID-2026-026/prompt-v2.md` | 230 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/FIX-2026-P1-MANIFEST-YAML-001/registration-record.md` | 41 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/FIX-2026-P1-T4-FU1/audit-record.md` | 96 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |
| `14-ai-development/work-items/FIX-2026-P1-T4-FU3/registration-record.md` | 50 | `docs/en/<path>` + `docs/zh-CN/<path>` | Work-item prompt/log (transient) |

**Not in scope:** The remaining 157 backlog rows are not classified or modified by this batch.
