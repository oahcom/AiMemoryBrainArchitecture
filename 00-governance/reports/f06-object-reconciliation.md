# F-06 Object-Level Reconciliation Report / F-06 对象级对账报告

- Work Item: GOV-DOC-001 (bilingual governance baseline), F-06 follow-up
- Reconciliation baseline: `f86fddc0fa0291ea8a5e080e741f083ce179a0a2` (main at execution time)
- Register under test: `00-governance/bilingual-governance-migration-register.md`
- Method: anchors recomputed from the Git object store and the GitHub REST API at execution time; every number below is computed, not transcribed.
- Status of this report: evidence record. It does not migrate any historical object, does not change any language classification, and does not authorise policy adoption.

## 1. Result summary / 结论摘要

| Dimension / 维度 | Register claim / 登记声明 | Recomputed / 复算 | Verdict |
|---|---|---|---|
| Commit records / Commit 记录 | 313 | 313 verified, 0 mismatch, 0 missing | MATCH |
| Commit SHA uniqueness | not asserted | 313 unique of 313 | MATCH |
| Commit classification | 312 EN_ONLY + 1 EN_ZH_MIXED | 312 `EN_ONLY` + 1 `EN_ZH_MIXED` (C168) | MATCH |
| Issue records / Issue 记录 | 39 (28/10/1) | 38 verified, 1 drifted | ONE ANCHOR DRIFT |
| PR grouping / PR 归组 | 232 PRs; "14 remain unassigned" | 242 PRs exist; groups cover 230; 14/14 of the claimed set are assigned | **CLAIM STALE — CORRECTED** |

## 2. Commits / 提交

- All 313 records carry a 40-hex `sha` and a `msg_sha256` anchor; `msg_sha256 = SHA-256(commit message bytes, stripped)` — the convention was confirmed by recomputation, not assumed.
- 313/313 anchors match; 0 commit objects missing; 0 content mismatches; 313 of 313 are ancestors of the reconciliation baseline.
- **Identity key:** `sha` is unique (313/313). `msg_sha256` is **not** an identity key: 7 groups of records share an identical message digest, covering 25 rows (examples: `C037/C038`, `C113/C114/C115`, `C125/C126`, `C230/C231/C232/C233/C234/C235/C236/C237/C238/C239/C240/C241/C242`, `C258/C259/C260/C261/C262`, `C267/C268/C269`, `C302/C303/C304/C305`). These are genuinely identical messages (bulk revert/removal commits), not registration errors. Any future join on message digest must expect collisions and fall back to `sha`.
- Classification tally recomputed from the register's own `language_state` column: 312 `EN_ONLY` + 1 `EN_ZH_MIXED` (C168) — consistent with the register's stated 312/1 split.

## 3. Issues / Issue

- 38/39 `body_sha256` anchors match exactly (`SHA-256(issue body, UTF-8)`).
- **Anchor drift — #266:** recorded `d984146097e7ce9a031f7046f4267ce7e2b40cd0380ccd6c37f98d17e93fadef`; recomputed `aaa599ccbfa45a20f4083ac2c9958739013dd4f816b9bda391964bd6b84ce3a9`; the issue was edited at `2026-11-19T16:34:35Z` (state `open`), i.e. after the inventory snapshot. The body still carries both languages (paired EN/ZH headings and parallel sections), so the `EN_ZH_MIXED` classification remains valid; only the anchor is stale.
- **Disposition:** the stale anchor is superseded by the recomputed value above. The historical anchor is preserved in this record rather than overwritten in the register table, so the edit trail stays auditable. A dedicated anchor-refresh entry should be appended to the register when the next revision lands.
- Classification tally: 28 `EN_ONLY` + 10 `EN_ZH_MIXED` + 1 `ZH_ORIGINAL_WITH_EN_TERMS` — consistent with the register's stated 28/10/1 split.

## 4. PR grouping / PR 归组

- The repository holds **242** PRs at the reconciliation baseline; the register states 232. The difference is explained by PRs created after the inventory snapshot (#271 onward).
- The six group tables in §8.4 cover **230** PR numbers with no overlap between groups (checked pairwise).
- **The §9 statement "fourteen PRs remain unassigned" is stale and, as of this baseline, incorrect.** All fourteen numbers it lists are present in the §8.4 group tables:

| PR | Group assigned in §8.4 |
|---|---|
| #269 | P-01 |
| #207 | P-04 |
| #197 | P-05 |
| #194 | P-05 |
| #193 | P-05 |
| #192 | P-05 |
| #191 | P-03 |
| #190 | P-05 |
| #189 | P-05 |
| #154 | P-05 |
| #143 | P-05 |
| #141 | P-04 |
| #139 | P-05 |
| #136 | P-02 |

- The actual unassigned set is **12 PRs**: `#48` and `#271`–`#281`. Assignments by integration-unit evidence (title, scope of the change) are proposed below. Language state is **not** inferred from titles; body-language classification for these 12 PRs remains untouched `MIGRATION_DEBT`, as for every existing group.

| PR | Proposed group | Title (verbatim, truncated) | Evidence basis |
|---|---|---|---|
| #48 | P-05 | docs(review): system-wide architecture risk assessment / 全系统架构风险评估 | architecture/research review record |
| #271 | P-02 | [GOV-DOC-001] Expand Bilingual Governance Baseline / 扩充双语治理基线 | bilingual governance baseline |
| #272 | P-01 | merge 12-state gates to 6-phase lifecycle | governance lifecycle gates |
| #273 | P-01 | F-006 fix — seven-sections structure anchor + RULING-01 revision | governance structure anchor / ruling |
| #274 | P-04 | typed watermark and fence binding contract carrier | publication/forget fence contract |
| #275 | P-05 | clarify project positioning and strategic direction in README | architecture positioning |
| #276 | P-04 | owner snapshot namespace and fence currentness contract | publication/forget fence contract |
| #277 | P-01 | AID-2026-001: integrate R3 dev-baseline | AI execution governance |
| #278 | P-01 | acceptance-comment minimum checklist §2.1 | AI governance / merge gate |
| #279 | P-02 | bilingual documentation tiering (policy + inventory + checks) | bilingual governance |
| #280 | P-01 | direct-push ratification record (audit A-3) | AI governance audit |
| #281 | P-01 | codify platform check unavailability handling (enforcement v1.2) | AI governance / merge gate |

- After these assignments, group coverage is **242/242** for the PR numbers existing at this baseline. Assignment is not migration: every group keeps `MIGRATION_DEBT` and `Accountable_Owner: NOT_ASSIGNED`.
- Group sizes at this baseline: P-01 14, P-02 19, P-03 45, P-04 34, P-05 116, P-06 2.

## 5. What this does and does not close / 本记录的效力边界

**Closes / 关闭：**
- The F-06 sub-requirement "object-level reconciliation of counts, classification totals, object uniqueness, identity matching, required anchors, and missing/duplicate records" — every element is now recomputed and reported above with a verdict.
- The F-06 sub-requirement "PR grouping/reconciliation" — the grouping exists for every PR at this baseline; the stale "14 unassigned" claim is corrected.

**Does not close / 不关闭：**
- Historical bilingual migration itself. Assignment and anchoring are registration facts, not migration completion; `MIGRATION_DEBT != EXEMPTION` remains in force.
- Body-language classification for PRs #48 and #271–#281, which was never in scope of the 39-Issue/313-Commit inventory.
- The #266 anchor re-pin inside the register table (this report carries the evidence; the register edit is a separate, additive revision).
- Any normative effect: GOV-DOC-001 v1.1 remains NORMATIVE, v1.2 remains DRAFT / NOT_ADOPTED.

## 6. Limitations / 限制

- GitHub API state was read at the execution timestamp; issues and PRs can change afterwards, and any later edit will produce a new drift of the same kind described in §3.
- The 39-Issue population and the 313-Commit population are taken as given by the register; this report verifies their anchors and internal consistency, not the completeness of the original census against repository history.
- Commit messages were read from the local clone; the clone was at the reconciliation baseline and every SHA resolved locally.

---

中文摘要：本报告对 F-06 要求的对象级对账逐项复算——313 条 Commit 锚点全部命中（sha 唯一，msg_sha256 有 7 组 25 行重复，属真实同文提交，不能作身份键）；39 条 Issue 锚点命中 38 条，#266 因正文在清点后被编辑而漂移，已在本文保留旧值与新值，分类不变；PR 侧实际 242 个，分组覆盖 230 个，§9「14 个未归组」的说法已过期——该 14 个在 §8.4 中均有归组，真正未归组的是 #48 与 #271–#281 共 12 个，本文按集成单元证据给出归组提案。归组不等于迁移，各分组继续维持 `MIGRATION_DEBT`。
