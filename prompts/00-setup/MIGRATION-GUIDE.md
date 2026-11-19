# Prompt v1 → v2 Migration Guide / 提示词 v1 → v2 迁移指南

- Guide ID: AI-PROMPT-MIGRATION-001
- Version: 1.0
- Status: PROPOSED — requires governance adoption

## 1. Migration policy / 迁移政策
v2 compresses the prompt structure from 15 mandatory headings to seven core sections. It does not delete applicable governance obligations, evidence, approvals, or historical records.

- Existing executed v1 prompts remain valid and immutable.
- Do not mass-rewrite active prompts. Create a v2 copy only when a new execution/version is needed and authorized.
- Preserve the original prompt, version, SHA-256, Issue/PR links, commits, review and acceptance records.
- If source bytes or a historical digest cannot be verified, record NOT_VERIFIED; never guess.
- The seven sections are the prompt layout. The Work Item manifest, evidence bundle, global prompts, GOV-DOC-001 and session closeout remain applicable.

## 2. Mapping / 旧新映射
| v2 core section | v1 elements consolidated | Migration rule |
|---|---|---|
| 1. Task identity | 1, 3, 4 (identity/roles/repository) | Consolidate Work Item, Prompt ID/version, Owner, implementer, reviewer, repo/branch, class/risk and carrier. Keep base/dependency SHAs in section 3. |
| 2. Goal and boundaries | 2, 6 | State What, Why and explicit Out of Scope. |
| 3. Context and dependencies | 4, 5 | Record exact base SHA, source paths/revisions and dependency contracts. |
| 4. Constraints and execution guidance | 7, 8, applicable parts of 11, 14 | Separate mandatory invariants/authority from adaptable recommended steps. Risk analysis occurs at the appropriate lifecycle gate. |
| 5. Acceptance and deliverables | 9, 12, applicable parts of 15 | Define observable completion and deliverables, including bilingual paths/manifest when GOV-DOC-001 applies. |
| 6. Evidence and review | 1 (prompt digest), 10, 13, applicable parts of 12/15 | Keep prompt SHA-256, commit/head/changed paths/read-back/acceptance evidence. Tests remain required when applicable and under R2/R3 policies. |
| 7. Stop conditions and coordination | 14 | Preserve stop, escalation, decision-owner, coordination and resume conditions. |

## 3. Relocated, not waived / 迁移但不豁免
### Security, failure, concurrency, recovery and compatibility (v1-11)
These are not removed from governance. The prompt no longer requires speculative exhaustive analysis before the task is understood. The Owner addresses applicable risks at design, implementation, verification and review gates. R2/R3 and security/data-integrity requirements remain unchanged.

### Bilingual documentation (v1-15)
Bilingual work is governed by GOV-DOC-001 and GLB-DOC-001, not by a separate fifteenth heading. The prompt must still identify affected Chinese/English paths, include bilingual work in scope/acceptance where architecture meaning changes, and provide parity evidence. A missing counterpart remains NOT DONE unless a formally approved, time-bounded STALE exception exists.

### Tests and evidence (v1-10, v1-13)
P0/P1 is an applicability classification, not permission to skip required checks. Exact commands may be pending during early architecture exploration, then become concrete before the verification gate. Every executed check records its tested SHA and outcome. A required check that did not run is NOT RUN, never PASS.

### SHA-256 and Git traceability (v1-1, v1-13)
Git commit/blob identifiers do not replace SHA-256 for the exact executed prompt snapshot where required. Store the prompt digest in the Work Item manifest/evidence bundle. Commit SHA, final Head SHA, changed paths, read-back and review/acceptance records remain P0.

## 4. Migration procedure / 迁移步骤
1. Identify the source prompt and verify Work Item, Owner, execution status, source revision and historical digest.
2. Preserve the source unchanged. Create a new v2 artifact only for a new/authorized execution; link it to the source version.
3. Move fields using the mapping table. Classify each requirement as retained in a core section, governed by global policy, not applicable with reason, or unresolved.
4. Re-check Owner authority, allowed/forbidden paths, dependency SHAs, observable acceptance, evidence and stop conditions.
5. Check GOV-DOC-001 applicability, paired paths, parity manifest and coverage register.
6. Compute and independently verify SHA-256 for exact new prompt bytes before execution; record it in the manifest.
7. Obtain required prompt review/Owner authorization. Start only when applicable Definition of Ready gates pass.

## 5. Pilot migration / 试点迁移
A real source prompt was located: 14-ai-development/work-items/AID-2026-003/prompt-v1.md (blob 71332a2b8f412d1bb58d4d53bdb25880dc2f1431). It is an executed, immutable historical artifact and MUST NOT be overwritten.

The companion work-item-003-v2-migration-example.md is a non-executed migration example derived from that real source. It demonstrates the seven-section organization; it does not supersede the historical prompt, reopen AID-2026-003, or claim Owner approval. Its executed-prompt SHA-256 is NOT APPLICABLE because it is not authorized for execution.

## 6. Migration checklist / 迁移检查表
- [ ] Source prompt and historical identity verified; source remains unchanged.
- [ ] New Prompt ID/version assigned; relation to source recorded.
- [ ] Seven sections populated; no required authority/constraint is lost.
- [ ] Base/dependency refs and exact source paths are current.
- [ ] Acceptance criteria are observable and have evidence locations.
- [ ] P0 traceability and applicable P1 verification are preserved.
- [ ] GOV-DOC-001 and bilingual manifest requirements are satisfied.
- [ ] Applicable security, failure, concurrency, recovery and compatibility gates are retained.
- [ ] Prompt digest is computed from exact bytes and recorded before execution.
- [ ] Required review and Owner authorization recorded.
