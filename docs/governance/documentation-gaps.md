---
document_metadata:
  domain: security-governance
  role: work-record
  lifecycle:
    approval:
      decision_status: Under-Review
      approver: NOT_RECORDED
      decision_date: NOT_RECORDED
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "00-governance/architecture-document-management-policy.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Records gaps observed during the GOV-DOC-002 rollout; no independent verification of each gap's status exists."
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
    normative_status: Informative
    canonical_conflict_status: None
---

# Documentation gaps / 文档缺口登记

Referenced-but-missing normative documents. Each entry records a link that could not be resolved during the GOV-DOC-002 rollout.

指向但缺失的规范文档。每条记录在 GOV-DOC-002 推行过程中无法解析的链接。

This file is governed by GOV-DOC-002 even though `docs/` as a whole is not: the policy cites it in three places as the record of what remains unclosed, so a change here that escaped the gate would let the governance record drift outside governance. It is listed individually in `GOVERNED_FILES` rather than by directory, to keep the exception as small as its reason.

本文件虽位于整体不受治理的 `docs/` 下，仍受 GOV-DOC-002 治理：条例三处引用它作为"尚未闭合事项"的记录，因此若对它的修改能绕过门禁，治理记录本身就会漂移到治理之外。它在 `GOVERNED_FILES` 中按单文件登记，而非按目录，以使例外的范围与理由一样小。

| ID | Missing document | Referenced from | Disposition |
|---|---|---|---|
| GAP-01 | `phase-3.5-forget-suppression-and-cursor-consumption.md` (Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract) | `docs/en/05-memory-runtime/{retrieval-engine, runtime-overview, working-set-and-cache}.md`, `docs/zh-CN/05-memory-runtime/{retrieval-engine, runtime-overview, working-set-and-cache}.md` | OPEN — never committed to this repository. Referencing text preserved; links replaced with an explicit missing-document marker. Content must NOT be reconstructed by an agent. |
| GAP-02 | Governance enforcement on direct pushes to `main` | `00-governance/architecture-document-management-policy.md` §8, `.github/workflows/document-management.yml` | PARTIAL — `--require-changed` runs on both pull requests (PR base) and direct pushes (`github.event.before`). Residual gap: the first push of a branch has no base commit, so the workflow falls back to the whole-tree scan. That scan now returns **INCOMPLETE (exit 2)** while backlog remains, so it fails loudly rather than reporting a pass it cannot justify — but it still cannot prove the *newly added* files are classified, only that a backlog exists. Closing it requires branch protection that mandates pull requests. |
| GAP-03 | Honesty of an exclusion reason in the scope registry | `00-governance/architecture-document-management-policy.md` §2, `00-governance/document-scope-registry.yaml` | PARTIAL — the ninth review showed this was not only unproven but already violated: `docs/` was excluded as "not documentation" while 26 of its files are architecture documents (minimum-runnable architecture, canonical transaction, source-of-truth inventory), and their own `DRAFT / NON-NORMATIVE` header is a value of `lifecycle.approval.decision_status`, not a reason to be outside classification. That directory is now `backlog`: scanned, counted, and reported as unclassified. What remains unresolved is narrower: DM-14 can check that an exclusion names `not-documentation` and gives a bilingual reason, but it cannot check that the claim is true. `reviews/` (196 Markdown files, review transcripts) is the only large exclusion still resting on that basis. Closing it requires a human to defend the exclusion, which is a review duty, not a machine check. |
| GAP-04 | A mirror can be **stale while its annotation count agrees** | `scripts/check_bilingual_docs.py` (existence), `00-governance/architecture-document-management-policy.md` §9.1 (`M-05`) | OPEN — found three times on 2026-11-25/26, and the third time is the one that names the gap. `check_bilingual_docs.py` proves both files exist and point at each other; it does not read either body. Counting annotations across the three copies catches drift in *density* — it caught `docs/zh-CN/.../OWNER-DECISION-REVIEW-INDEPENDENCE-001.md` carrying seven fewer notes than root, and later root carrying one fewer than zh. It does **not** catch a body that was rendered stale while its count stayed plausible: `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036` had its English segment corrected on 2026-11-24 and its **Chinese segment inside `docs/en` left at the old text**, still asserting a retracted and verifiably false claim (that no document defines independence at the session level — zero hits; the real counts on `1259f1af` are 8 / 10 / 11 / 6), while the three copies sat at 2 / 4 / 2 annotations and looked consistent. Only a byte comparison of the bodies finds that, and only where the root body is itself Chinese, so the mirror is expected to be identical rather than a translation. A whole-tree check on that narrower class (root body ≥15% CJK, 25 groups) is currently clean: 25 / 25 identical. Closing this properly needs the same check as a gate rule, which means deciding that "root body is Chinese ⇒ zh mirror must be byte-identical" is a contract and not a coincidence — that is a policy decision (`M-05` territory), not a tooling change. |
| GAP-05 | A **section can be stale while the amendment that retired it sits in the same file** | `OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025` §6 (commissioned the note), `I-OWNER-DECISION-AUTHORIZATION-DECISION-001` §3.3 (the note that was never written) | OPEN — five instances, not one. The same failure as GAP-04, one level in: a file can carry a correct, complete amendment section at the end and still have the amended section's own body reading the retired way, because the amendment is appended and the body is not. First found in `I-001` §3.3 ("may validate candidate field syntax and **reject Pending**"; the shipped gate at `crates/memory-domain/src/lib.rs:1024` rejects `Absent` only, and `OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025` §1 forbids rejecting `Placeholder`) — and the ruling had already commissioned that note on 2026-11-22. An independent re-check found four more, three of them in the same file: `I-001` criterion 12 (still says "propagated authority `Err`" after the amendment changed which assertion satisfies it), `I-001` criterion 1 (still two-state `Pending/Issued` after D2 made it three), `PUBLICATION-RECORD-001` D3 (still requires the literal `false` that D8.2 replaced with a sourced read), and `PUBLICATION-RECORD-001` Consequences (still promises the D-side registry that D7.1 withdraws). Annotation count cannot see any of them: each file was internally consistent in every countable respect. See the GAP-05 detail below for the detector, its four false-positive classes, and the three structural reasons it missed these four. |

## GAP-04 detail / 详情

The failure mode is worth stating separately because the obvious detector is the wrong one.

A stale mirror and a correct mirror can carry the same number of dated annotations, the same front matter, the same headings, and the same length. The difference lives inside one paragraph. Any check that counts something — annotations, CJK characters, headings, line counts — is looking at a projection of the body, and the projection agreed in all three cases found so far.

What does work, on the class of documents where it is well defined: **compare the bodies directly**. For a document whose root body is Chinese, the `docs/zh-CN` mirror is not a translation and should be byte-identical; a diff is drift. For a document whose root body is English, the zh mirror is a translation and a byte diff proves nothing — that case stays with `M-05` and a human.

The boundary matters, because applying byte comparison to translated pairs would generate 42 false positives on this tree, which is exactly how a real signal gets buried.

失效模式值得单独写明，因为最显然的检测手段是错的那个。

陈旧镜像与正确镜像可以带同样多的日期注记、同样的 front matter、同样的标题、同样的长度。差别只在某一段里。任何"计数"式检查——注记数、汉字数、标题数、行数——看的都是正文的一个投影，而迄今为止发现的三个案例里，这个投影全都一致。

真正有效的，是在定义清楚的那一类文档上：**直接比正文**。根正文为中文的文档，其 `docs/zh-CN` 镜像不是译文，本应逐字节相同，出现差异就是漂移。根正文为英文的文档，zh 镜像是译文，字节差异不说明任何问题——那一类仍归 `M-05` 与人工审查。

这个边界很重要：若把字节比对套到译文对上，本树会产出 42 个假阳性，而那正是真信号被埋掉的方式。

## GAP-05 detail / 详情

GAP-04 says a *mirror* can be stale while its annotation count agrees. GAP-05 is the same statement one level in: a *section* can be stale while the amendment that retired it sits in the same file, correct and complete.

The mechanism is structural, not accidental. This repository appends amendments at the end of the document. An amendment section that names §4.3 and says what replaced it is complete as a record, and it is also the only place the change was made. If nobody goes back to §4.3 and points at it, a reader who navigates by heading — which is how these documents are read — gets the retired instruction with no signal that it lapsed. All the same properties hold: the front matter is right, the amendment is right, the closure criteria are right, the count of annotations is right. The body is wrong.

GAP-04 说*镜像*可以在注记数一致的情况下陈旧。GAP-05 是同一句话往里一层：*某个章节*可以陈旧，而撤回它的那条修订就正确、完整地躺在同一个文件里。

机制是结构性的，不是偶然的。本仓库把修订追加在文档末尾。一条修订写明 §4.3 被什么取代，作为记录它是完整的，同时也构成了这次改动的全部。若无人回到 §4.3 指向它，按标题导航的读者（这些文档就是这么读的）会读到已退役的指令，且没有任何信号表明它已失效。所有可数性质都成立：front matter 对、修订对、关闭判据对、注记数对。正文错。

### The detector / 检测器

Not a search for the retired phrasing — that phrasing is often legitimately quoted inside the amendment that retires it, and it is often paraphrased in the body. The detector works from the amendment outward:

1. Split each file at its **last** amendment-ish heading (append-at-the-end is the convention here, so the last one bounds the amendment region).
2. In that region, find paragraphs carrying a **strong** retirement verb (`is/are superseded|narrowed|replaced|retired|withdrawn|revoked`).
3. Extract the section numbers those paragraphs name.
4. For each, find the body heading with that number and check whether the first nine lines carry a pointer (`amended|superseded|narrowed|see the amendment|retired`).
5. Report the named-but-unpointed ones.

不是去搜退役措辞——那个措辞常常被撤回它的修订合法引用，在正文里也常常被改写。检测器从修订往外走：切、找强退役动词、抽出章节号、回到正文按号找标题、看前九行有无指针、报未带指针者。

### Four false-positive classes, and why each is excluded / 四类误报，及各自为何被排除

Getting this from 108 raw hits to one real finding required four exclusions. Each is a real distinction, not a regex tweak, which is why they are recorded rather than merely coded:

| Class | Example | Why it is not a carrier |
|---|---|---|
| **Value supersession** | an amendment paragraph about a blob `5b86fe23ab7c` or a SHA being replaced | The thing superseded is a byte string, not a rule. Detected by a `12`–`40`-hex token in the paragraph; such paragraphs are skipped entirely. |
| **Section-reference prefix** | `§4` reported when the paragraph says `§4.3` | `§4` is not retired by a statement about §4.3. A ref is dropped when a longer ref with the same prefix appears in the same paragraph. |
| **Cited as evidence** | `§8`/`§9.1` named in "§9.1 already said otherwise" | The section is being used to *support* the amendment's claim, not being retired by it. Caught by the `stand|unchanged|still required|not touched` marker: sections named after that marker are untouched. |
| **Change-log table** | `00-governance/architecture-document-management-policy.md` §11 | A version table lists *what each release changed*, citing §2, §4.1, §3.2 as **objects** of change. Every row is a completed edit, not a pending retirement. This one is not auto-excluded — it is the class that shows the detector's ceiling. |

The fourth is the honest limit. A change-log table is indistinguishable from a retirement list by grammar alone: both say "§X changed on date D". Distinguishing them needs to know whether the cited section already carries the result, which is a semantic judgement per row. On this tree the class is one document, so the right response is to read it, not to widen the regex until it disappears.

第四类是诚实的边界。变更日志表格与退役清单在语法上不可区分：两者都说「§X 在 D 日变了」。要区分，必须知道被引章节是否已承载该结果，那是逐行的语义判断。本树该类只有一份文档，正确做法是去读它，而不是把正则放宽到它消失。

### What this does and does not establish / 本项确立与未确立之事

Establishes: **five** rule-level instances of the pattern on 2026-11-26, all now annotated. The first was found by the detector; the other four were found by an independent re-check that used a different search path, which is the point recorded in the next subsection.

Does not establish: that the pattern is absent from sections **not** named by any amendment. A section can be stale because the world moved and nobody wrote an amendment at all; that is a currency failure, not a supersession failure, and it has no amendment region to search from. It stays with review.

确立：2026-11-26 本树有**五处**规则级的该形态，现已全部加注。第一处由检测器发现；其余四处由一次走不同检索路径的独立复核发现——这正是下一小节记录的重点。

未确立：该形态不存在于**任何修订都未指名**的章节。章节可以因为没有修订（世界变了而无人记录）而陈旧；那是时效失效，不是取代失效，而且它没有可供搜索的修订区。这一类仍归审查。

### Why the detector found one and a reader found five / 检测器只找到一处，读者找到五处

The first pass reported exactly one instance and I recorded that as the answer. An independent re-check — given the three claims and told to falsify them, working from a different direction — found four more, three of them in the same file the detector had just cleared. That outcome is worth recording precisely, because the detector did not malfunction; it was answering a narrower question than the claim made on its behalf.

第一轮只报出一处，我把它当成了答案。一次独立复核——带着三条论断、被要求去证伪、从另一个方向入手——又找到四处，其中三处就在检测器刚刚判为干净的那个文件里。这个结果值得精确记录，因为检测器并没有坏；它回答的问题比替它宣称的那个论断要窄。

Three structural limits, each producing one of the misses:

| Limit | Consequence |
|---|---|
| It splits at the **last** amendment heading only | `PUBLICATION-RECORD-001` has four amendment regions (D6, D7, post-decision, D8). Everything D7 retired is invisible to a split that starts at D8. |
| It looks for a **heading** with the retired number | Decisions are bold items (`**D3.**`, `**D7.1.**`) and closure criteria are list items (`1.`–`13.`), not headings. No heading, no lookup, no finding — criteria 1 and 12 and D3 all escaped this way. |
| Its retirement verbs are **English-only** | `取代/撤回/不成立/已被` never match, and the tree has a whole `docs/zh-CN/` mirror. |

三条结构性限制，各自对应一处漏检：只切最后一个修订区（`PUBLICATION-RECORD-001` 有四个修订区，D7 的撤回整片不可见）；只按标题号回查（决策项是粗体、判据是列表项，都不是标题）；退役动词只认英文（中文修订区一律不命中，而本树有整片 `docs/zh-CN/`）。

The lesson is not "write a better regex". It is that a detector whose reach is "sections named by the last amendment, addressed by heading number, described in English" cannot support the claim "this tree has one instance". The claim was wider than the instrument. Stating the instrument's reach first, and the count second, would have made the gap visible without the re-check.

教训不是「写个更好的正则」。而是：一个覆盖范围是「最后一个修订区点名、以标题号寻址、以英文描述」的检测器，支撑不起「本树只有一处」这个论断。论断比仪器宽。先写清仪器的覆盖范围、再报数量，这处缺口本来就会自己显形。

## GAP-01 detail / 详情

Six references across the `05-memory-runtime` specifications cite this contract as the authoritative source for the F consumer matrix, retrieval-stage suppression matrix, cache/Working Set invalidation, index rebuild, and ten conformance specifications.

`05-memory-runtime` 各规范中共有六处引用将该契约视为 F Consumer Matrix、Retrieval-stage Suppression Matrix、Cache/Working Set Invalidation、Index Rebuild 及十项 Conformance Specification 的权威来源。

The file does not exist in the working tree or in the git history reachable from `main`. Because the referenced normative content is unavailable, the references are **not** satisfiable by rewriting them to a different file, and the content MUST NOT be invented.

该文件在工作树与 `main` 可达历史中均不存在。由于被引用的规范内容不可得，**不能**通过改指其他文件来满足这些引用，其内容也禁止臆造。

Required resolution / 需要的处置：

1. The owning party for `05-memory-runtime` supplies the actual contract, or
2. the six referencing passages are amended to state that the contract is not yet published.

1. 由 `05-memory-runtime` 责任方提供该契约原文；或
2. 将六处引用改写为「该契约尚未发布」。

Until then, any consumer reading `05-memory-runtime` MUST treat the forget-suppression and typed-cursor semantics as **not specified in a published normative document**.

在此之前，任何阅读 `05-memory-runtime` 的消费者 MUST 将 forget-suppression 与 typed-cursor 语义视为**尚无已发布的规范文档定义**。
