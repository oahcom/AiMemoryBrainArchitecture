---
document_metadata:
  domain: ai-development
  role: work-record
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-347/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Prompt snapshot is an authoring reference. Exact transmission provenance has not been independently verified."
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
    canonical_scope: "Repair instructions for AID-2026-347: sanitize INDEX.md before AID link matching in check_traceability.py."
    canonical_scope_id: "ai-development/aid-2026-347-prompt-v1"
    canonical_scope_keywords:
      - "AID-2026-347"
      - "prompt"
      - "traceability"
      - "sanitize"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

下面是你要的完整上下文。

### check_traceability.py 1-60
1: #!/usr/bin/env python3
2: """Structural requirement/work-item traceability checker.
3: 
4: The requirements registry is a non-authoritative index. GitHub Issues remain
5: the requirement authority. This checker does not assess semantic correctness.
6: 
7: The registry is deliberately restricted to JSON syntax, which is a valid
8: YAML subset. No PyYAML or third-party package is required.
9: 
10: Manifest parsing is deliberately narrow: only selected top-level scalar
11: values are read. Nested YAML is ignored. Unsupported or malformed input is
12: reported as indeterminate rather than silently interpreted.
13: """
14: 
15: from __future__ import annotations
16: 
17: import json
18: import os
19: import re
20: import subprocess
21: import sys
22: from pathlib import Path
23: from typing import Dict, List, Optional, TextIO, Tuple
24: 
25: 
26: REGISTRY_PATH = Path("00-governance/requirements-registry.yaml")
27: INDEX_PATH = Path("14-ai-development/work-items/INDEX.md")
28: WORK_ITEMS_DIR = Path("14-ai-development/work-items")
29: 
30: REQUIREMENT_ID_RE = re.compile(r"^REQ-[0-9]{2,}$")
31: ISSUE_URL_RE = re.compile(
32:     r"^https://github\.com/[^/]+/[^/]+/issues/([1-9][0-9]*)$"
33: )
34: AID_LINK_RE = re.compile(
35:     r"\[\s*(AID-[0-9]{4}-[0-9]{3})\s*\]\(([^)]+/manifest\.yaml)\)"
36: )
37: ISSUE_NUMBER_RE = re.compile(r"#([1-9][0-9]*)")
38: REQ_REF_RE = re.compile(r"\bREQ-[0-9]{2,}\b")
39: SHA_RE = re.compile(r"^[0-9a-fA-F]{40,64}$")
40: 
41: STAGE_0_RECORD_TYPE = "STAGE_0_WORK_ITEM_REGISTRATION"
42: 
43: # Closed historical compatibility list. These records may use `aid:` instead
44: # of the normative `work_item_id:` key until their manifests are migrated.
45: LEGACY_AID_KEY_IDS = {
46:     "AID-2026-014",
47:     "AID-2026-023",
48:     "AID-2026-026",
49: }
50: 
51: MANIFEST_KEYS = {
52:     "work_item_id",
53:     "aid",
54:     "record_type",
55:     "tracking_issue",
56:     "base_commit_sha",
57: }
58: 
59: 
60: class CheckFailure(Exception):
### 560-640
560:             authority_issues.add(issue_match.group(1))
561: 
562:         docs = item.get("linked_docs")
563:         if not isinstance(docs, list):
564:             reporter.error(
565:                 "T-02 {} linked_docs must be an array".format(rid)
566:             )
567:             docs = []
568: 
569:         for doc in docs:
570:             path = safe_repo_path(root, doc)
571: 
572:             if path is None:
573:                 reporter.error(
574:                     "T-02 {} has unsafe linked_docs path {!r}".format(
575:                         rid, doc
576:                     )
577:                 )
578:             elif not path.is_file():
579:                 reporter.error(
580:                     "T-02 {} references missing document {}".format(
581:                         rid, doc
582:                     )
583:                 )
584: 
585:         linked = item.get("linked_work_items")
586:         if not isinstance(linked, list):
587:             reporter.error(
588:                 "T-03 {} linked_work_items must be an array".format(rid)
589:             )
590:             linked = []
591: 
592:         index_path = root / INDEX_PATH
593:         index_text = None
594: 
595:         if linked:
596:             try:
597:                 index_text = index_path.read_text(encoding="utf-8")
598:             except OSError as exc:
599:                 raise CheckFailure(
600:                     "cannot read work item INDEX: {}".format(exc)
601:                 ) from exc
602: 
603:         for work_item_id in linked:
604:             if not isinstance(work_item_id, str) or not re.fullmatch(
605:                 r"AID-[0-9]{4}-[0-9]{3}", work_item_id
606:             ):
607:                 reporter.error(
608:                     "T-03 {} has invalid linked work item {!r}".format(
609:                         rid, work_item_id
610:                     )
611:                 )
612:                 continue
613: 
614:             if not re.search(
615:                 r"\[\s*" + re.escape(work_item_id) + r"\s*\]\(",
616:                 index_text or "",
617:             ):
618:                 reporter.error(
619:                     "T-03 {} links {} but it is absent from INDEX.md".format(
620:                         rid, work_item_id
621:                     )
622:                 )
623: 
624:         if not linked:
625:             no_item = item.get("no_work_item_yet")
626:             reason = item.get("no_work_item_yet_reason")
627: 
628:             if (
629:                 no_item is not True
630:                 or not isinstance(reason, str)
631:                 or not reason.strip()
632:             ):
633:                 reporter.error(
634:                     "T-07 {} needs linked_work_items or "
635:                     "no_work_item_yet=true with a reason".format(rid)
636:                 )
637: 
638:         validate_acceptance(rid, item, reporter)
639: 
640:     return requirement_ids, authority_issues
### 705-760
705:                     manifest_path, manifest_id
706:                 ),
707:                 repo_relative_path(root, manifest_path),
708:             )
709:             return False
710: 
711:         reporter.warn(
712:             "T-04 {} uses legacy aid identity key; migrate to "
713:             "work_item_id".format(aid)
714:         )
715:         return True
716: 
717:     reporter.error(
718:         "T-04 manifest {} has no recognized identity key "
719:         "(work_item_id required)".format(manifest_path),
720:         repo_relative_path(root, manifest_path),
721:     )
722:     return False
723: 
724: 
725: def validate_index_and_manifests(
726:     root: Path,
727:     authority_issues: set,
728:     reporter: Reporter,
729: ) -> Tuple[int, set]:
730:     index_path = root / INDEX_PATH
731: 
732:     try:
733:         index_text = index_path.read_text(encoding="utf-8")
734:     except OSError as exc:
735:         raise CheckFailure(
736:             "cannot read {}: {}".format(INDEX_PATH, exc)
737:         ) from exc
738: 
739:     index_entries: Dict[str, str] = {}
740: 
741:     for match in AID_LINK_RE.finditer(index_text):
742:         aid, manifest_relative = match.groups()
743: 
744:         if aid in index_entries:
745:             reporter.error("T-04 duplicate INDEX entry {}".format(aid))
746: 
747:         index_entries[aid] = manifest_relative
748: 
749:     manifests = sorted(
750:         (root / WORK_ITEMS_DIR).glob("AID-*/manifest.yaml")
751:     )
752:     manifest_by_id = {path.parent.name: path for path in manifests}
753: 
754:     # Forward direction: every INDEX entry must resolve to its manifest.
755:     for aid, manifest_relative in index_entries.items():
756:         expected = safe_work_item_manifest_path(root, manifest_relative)
757: 
758:         if expected is None:
759:             reporter.error(
760:                 "T-04 {} has unsafe manifest path {}".format(

# 补充约束

1. `sanitize_index_text` 必须是**模块级**函数（供 `validate_requirements` 与 `validate_index_and_manifests` 共用），不要嵌套在函数里。
2. 清洗实现建议：按行扫描，跟踪 `<!--` / `-->` 状态与 ``` 围栏状态；被清洗的字符用空格替换、换行保留，保证 `text.splitlines()` 长度与原文一致。
3. 三处消费点：`:597`（T-03 的 `index_text`）、`:733`（T-04 的 `index_text`）、`:741`（`AID_LINK_RE.finditer`）。请只改必要的赋值处，让两处 `index_text` 都已经是清洗后的文本，`finditer` 无需改。
4. 新增 `scripts/test_check_traceability_sanitize.py`（unittest，直接 import `scripts.check_traceability` 会触发包路径问题——请先看该文件顶部是否已有 `sys.path` 处理；如果没有，测试里用 `importlib.util.spec_from_file_location` 加载，避免新增 `__init__.py`）。
5. 不要改 `scripts/test_check_traceability.py`。

只输出编辑块，不要解释。
