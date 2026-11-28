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
    canonical_scope: "Repair instructions for AID-2026-347: reject newly added Markdown outside NORMATIVE_ROOTS in check_bilingual_docs.py."
    canonical_scope_id: "ai-development/aid-2026-347-prompt-v2"
    canonical_scope_keywords:
      - "AID-2026-347"
      - "prompt"
      - "bilingual"
      - "outside-root"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

下面是你要的模块级上下文。

### check_bilingual_docs.py 1-70
1: #!/usr/bin/env python3
2: """Conservative bilingual documentation gate for pull requests.
3: 
4: This checks changed-file pairing and explicit PR declarations. It does not
5: claim semantic translation parity; that remains a reviewer responsibility.
6: """
7: from __future__ import annotations
8: 
9: import ast
10: import os
11: import tempfile
12: from datetime import date
13: import subprocess
14: import sys
15: import re
16: from collections import Counter
17: from pathlib import Path
18: 
19: NORMATIVE_ROOTS = {
20:     "00-governance", "01-system-architecture", "02-domain-model", "03-memory-brain",
21:     "04-memory-compiler", "05-memory-runtime", "06-memory-context", "07-agent-integration",
22:     "08-bmcp-protocol", "09-security-governance", "10-storage-consistency", "13-engineering-decisions",
23:     "14-ai-development",
24: }
25: ROOT = Path(__file__).resolve().parents[1]
26: _missing_roots = sorted(r for r in NORMATIVE_ROOTS if not (ROOT / r).is_dir())
27: if _missing_roots:
28:     sys.stderr.write(
29:         "NORMATIVE_ROOTS references non-existent directories: "
30:         + ", ".join(_missing_roots) + "\n"
31:     )
32:     sys.exit(2)
33: # 14-ai-development subtrees holding operational records or prompt templates,
34: # not bilingual specifications. The PR-body declaration requirement still
35: # applies; counterpart pairing does not.
36: PAIR_EXEMPT_PREFIXES = (
37:     "14-ai-development/work-items/",
38:     "14-ai-development/prompts/",
39:     "14-ai-development/adr/",
40: )
41: # For 14-ai-development, counterpart pairing applies to prose documents only.
42: PAIR_ENFORCED_SUFFIXES = {".md"}
43: # Exact side-by-side pairs temporarily known to be incomplete translations.
44: # Each key is an unordered pair of repository-relative paths.
45: # Keep empty when no reviewed partial pair remains unresolved.
46: PARTIAL_SIDE_BY_SIDE_PAIRS: set[frozenset[str]] = set()
47: EXEMPT_SUFFIXES = {".png", ".jpg", ".jpeg", ".svg", ".drawio"}
48: # Each entry is a reviewed single-file bilingual source. The reason must add
49: # information about the file's external contract, consumer, or governance role
50: # that the file does not already state about itself. This is a reviewer
51: # obligation, not a regex/checker rule: reviewers must reject self-describing
52: # reasons that merely repeat the document's own subject or contents.
53: #
54: # Three legacy registrations were made by the same author in the commit that
55: # created each file. They remain exempt only as explicitly named findings, not
56: # as precedent for future registrations. IMPORTANT: every SHA in this mapping
57: # MUST come from _file_add_commit() with complete Git history. A shallow clone
58: # can report its shallow-boundary commit instead of the true creation commit.
59: # Example measured on full history: bilingual-documentation-policy.md was
60: # created at cd1ab0fb346c770d779b1d8d24297f6811a1a74f and registered at
61: # 32a35f422ba6442d1f700cfb327f348c0740a7f2; these are distinct commits.
62: # Never calculate or refresh this mapping from a shallow clone.
63: # Owner measurement found bilingual
64: # headings and both scripts interleaved across 15–19% of lines (above the 9%
65: # control-template density), confirming that their content is genuinely
66: # embedded-bilingual; the defect was the missing second-party registration.
67: SELF_REGISTERED_AT_CREATION: dict[str, str] = {
68:     "00-governance/architecture-document-management-policy.md": "0c73f639bf7392a5381d0cc0d9cafd53017bfe05",
69:     "00-governance/drafts/GOV-DOC-001-v1.2-DRAFT.md": "04d35f90d6f1389ee17dc8fba1a32600bd7ac8ec",
70:     "00-governance/reports/f06-object-reconciliation.md": "9990b645555aef83714ff92c97255110b1fa0960",
### main() 起点 1447
1447: def main() -> int:
1448:     if len(sys.argv) == 2 and sys.argv[1] == "--write-baseline":
1449:         try:
1450:             return write_baseline()
1451:         except Exception as exc:
1452:             print(f"::error::Unable to write bilingual baseline: {exc}")
1453:             return 2
1454:     if len(sys.argv) > 1:
1455:         print("::error::Unknown argument. Supported option: --write-baseline")
1456:         return 2
1457: 
1458:     # Refuse to make any gate judgment from a shallow checkout. This must run
1459:     # before baseline/path checks so their unrelated diagnostics cannot mask
1460:     # the fact that provenance is unverifiable.
1461:     try:
1462:         _require_full_git_history()
1463:     except ShallowRepositoryError as exc:
1464:         print(f"::error::{exc}")
1465:         return 2
1466:     except (OSError, subprocess.CalledProcessError, RuntimeError) as exc:
1467:         print(f"::error::Unable to determine Git history completeness: {exc}")
1468:         return 2
1469: 
1470:     try:
1471:         statuses = changed_status()
1472:         changed = set(statuses)
1473:     except Exception as exc:
1474:         print(f"::error::Unable to determine changed paths: {exc}")
1475:         return 2
1476: 
1477:     if not changed:
1478:         print(
1479:             "::error::NOT_APPLICABLE: BASE_SHA...HEAD_SHA contains zero changed paths; "
1480:             "no bilingual incremental verification was performed."
1481:         )
1482:         return 2
1483: 
1484:     baseline = read_baseline()
1485:     if baseline is None:
1486:         return 2
### skipped 附近 1565-1610
1566:                 normative_changes.append(path)
1567: 
1568:     if normative_changes and not complete and not exception:
1569:         errors.append(
1570:             "Normative source files changed but PR body lacks "
1571:             "'BILINGUAL-MANIFEST: COMPLETE' or a fully documented "
1572:             "'BILINGUAL-EXCEPTION: APPROVED': "
1573:             + ", ".join(normative_changes)
1574:         )
1575: 
1576:     errors.extend(
1577:         check_normative_pairing(
1578:             normative_changes,
1579:             changed,
1580:             statuses,
1581:             complete,
1582:             exception,
1583:             catch_up_declarations,
1584:         )
1585:     )
1586:     errors.extend(check_normative_root_departures(exception))
1587: 
1588:     skipped = [p for p in changed if Path(p).parts and Path(p).parts[0] not in NORMATIVE_ROOTS
1589:                and Path(p).suffix.lower() == ".md"]
1590:     if skipped:
1591:         sys.stderr.write(f"NOTE: {len(skipped)} changed .md path(s) outside NORMATIVE_ROOTS were not pairing-checked\n")
1592: 
1593:     if exception:
1594:         print("Approved bilingual exception declaration detected; human governance approval remains mandatory.")
1595:     if errors:
1596:         for error in errors:
1597:             print(f"::error::{error}")
1598:         print("Bilingual documentation gate: FAIL")
1599:         return 1
1600: 
1601:     print(f"exemptions: {len(EMBEDDED_BILINGUAL_SOURCES)}")
1602:     print(f"Bilingual documentation and prompt-library gate: PASS ({len(changed)} changed paths inspected).")
1603:     print("This is a structural gate only; semantic parity requires independent review.")
1604:     return 0
1605: 
1606: 
1607: if __name__ == "__main__":
1608:     sys.exit(main())
1609: 
### NORMATIVE_ROOTS 定义 19
19: NORMATIVE_ROOTS = {
20:     "00-governance", "01-system-architecture", "02-domain-model", "03-memory-brain",
21:     "04-memory-compiler", "05-memory-runtime", "06-memory-context", "07-agent-integration",
22:     "08-bmcp-protocol", "09-security-governance", "10-storage-consistency", "13-engineering-decisions",
23:     "14-ai-development",
24: }
25: ROOT = Path(__file__).resolve().parents[1]
26: _missing_roots = sorted(r for r in NORMATIVE_ROOTS if not (ROOT / r).is_dir())
27: if _missing_roots:
28:     sys.stderr.write(

# 修正上一版的三个问题

1. **不要嵌套定义函数**：`outside_root_markdown_paths` 与 `outside_root_additions` 必须是**模块级**纯函数，放在 `NORMATIVE_ROOTS` 定义之后、`main()` 之前。
2. **不要 `sys.exit(1)` 就地退出**：`main()` 已有的错误聚合/退出码机制要保持一致——把错误追加到现有的 errors 列表（或等价的 reporter），由既有出口统一决定退出码。
3. 错误文案用英文（与文件内其它 `::error::` 一致），点名路径与两条出路。

然后输出：
- `scripts/check_bilingual_docs.py` 的模块级函数插入块（用 `NORMATIVE_ROOTS` 定义块做锚点）；
- `main()` 内 skipped 段的替换块（调用模块级函数）；
- `scripts/test_check_bilingual_docs_outside_root.py` 的完整测试文件（unittest，直接 import 模块级函数；若 import 路径有问题，用 `importlib.util.spec_from_file_location`）。

只输出编辑块，不要解释。
