# Simplified Work Prompt Template v2 / 简化任务提示词模板 v2

- Template ID: AI-PROMPT-TPL-002
- Version: 2.0
- Status: PROPOSED — requires governance adoption
- Applies to: new work prompts; existing executed prompts remain immutable

**中文对应文档 / Chinese counterpart:** [TEMPLATE-v2.zh-CN.md](TEMPLATE-v2.zh-CN.md)

> Seven core elements are seven sections, not seven metadata fields. This changes prompt organization, not authority, verification, bilingual, security, or acceptance gates.

## 1. Task identity / 任务标识
- **Work Item ID:** [WI-ID]
- **Prompt ID / Version:** [PROMPT-ID] v[VERSION]
- **Accountable Owner:** [A–I / named cross-cutting Owner]
- **Implementer:** [session/role]
- **Independent Reviewer:** [session/role, or PENDING with reason]
- **Repository:** [owner/repository]
- **Branch:** [branch]
- **Task Class / Risk:** [ARCH / IMPL / TEST / SEC / MIG / PERF / DOC / OPS] / [R0–R3]
- **Owning Issue / PR:** [URL or NOT_CREATED + reason]

## 2. Goal and boundaries / 目标与边界
**What — 做什么:** [Observable task objective.]

**Why — 为什么:** [Motivation, impact, and decision context.]

**Out of Scope — 不做什么:**
- [Explicit non-goal.]
- [Excluded files, modules, decisions, or operations.]

## 3. Context and dependencies / 上下文与依赖
- **Base:** [base branch] @ [full commit SHA]
- **Required sources:** [exact path + version/status + blob SHA or commit SHA]
- **Dependency contracts:** [Owner + contract + exact revision; or NONE]
- **Applicable global/Owner prompts:** [Prompt IDs and paths]
- **Bilingual sources:** [affected Chinese/English paths and source revision, when applicable]

If a required source, revision, approval, or dependency is unavailable or conflicting, stop at that boundary and report it; do not infer it.

## 4. Constraints and execution guidance / 约束与执行指导
**Mandatory constraints / 强制约束**
- [Normative rules, invariants, trust boundaries, compatibility requirements.]
- [Authority boundary: permitted files/modules and prohibited cross-Owner decisions.]
- Read and comply with GOV-DOC-001 and applicable global/Owner prompts. Architecture-significant changes require Chinese/English counterparts in the same change set unless a formally approved, time-bounded STALE exception applies.
- Security, failure, concurrency, recovery, privacy, and compatibility analysis MUST occur at the lifecycle gate appropriate to task class/risk. This template does not waive those reviews.

**Recommended steps / 推荐步骤**
1. [Suggested inspection/design/implementation sequence.]
2. [Suggested validation or handoff.]
These steps are adaptable unless explicitly marked MUST.

## 5. Acceptance and deliverables / 验收与交付物
**Observable acceptance criteria / 可观测验收条件**
- [ ] [Objective condition, evidence location, and pass rule.]
- [ ] [Objective condition, evidence location, and pass rule.]

**Required deliverables / 必需交付物**
- [Code/document/configuration/report paths.]
- [Decision record, bilingual manifest, or other applicable artifact.]
- [List NOT APPLICABLE items with reason.]

Acceptance criteria define completion. An artifact's existence alone does not prove correctness or approval.

## 6. Evidence and review / 证据与审查
**P0 — mandatory minimum evidence**
- Executed Prompt ID/version and SHA-256 of the immutable prompt snapshot, recorded in the Work Item manifest. Never invent an unavailable digest.
- Base SHA, implementation Commit SHA(s), final branch Head SHA, and exact Changed Files list.
- Read-back confirmation for changed artifacts.
- Acceptance criteria disposition with evidence links and owning Issue/PR closeout.
- Independent review disposition and authorized acceptance record, when required by governance.

**P1 — applicable verification evidence**
- Exact test/check command, environment, tested commit SHA, expected/actual result, and evidence link.
- Mark unavailable or inapplicable checks NOT RUN / NOT APPLICABLE with reason; never imply PASS.
- R2/R3, security, data-integrity, migration, concurrency, recovery, and other applicable policies retain their full test/review evidence. P1 is not a waiver.

**Review level:** [R0 / R1 / R2 / R3]  
**Bilingual parity evidence:** [Chinese/English paths, source revision, reviewer and result, when applicable.]

## 7. Stop conditions and coordination / 停止条件与协调
**Stop and escalate when**
- [A required authority, approval, source, or dependency is missing/conflicting.]
- [The change crosses an Owner boundary or threatens an invariant.]
- [Acceptance cannot be verified or unexpected scope appears.]

**Escalation / coordination**
- **Decision Owner:** [named Owner / authority]
- **Tracking route:** [Issue/PR, affected Owner(s), requested decision]
- **Resume condition:** [objective condition required before work continues]

## Use notes / 使用说明
- Keep the seven headings; use NONE, NOT APPLICABLE, or PENDING + reason instead of inventing content.
- Compute SHA-256 over the exact immutable executed prompt snapshot and store it in the Work Item evidence bundle/manifest. Do not put a self-referential digest inside the bytes being hashed.
- This prompt does not replace the Work Item manifest, required global prompts, GOV-DOC-001, AI-STD-001, ADRs, or the GitHub Issue/PR carrier.
- Existing v1 prompts remain valid and immutable. Migrate only for a new execution/version; never rewrite an executed prompt in place.
