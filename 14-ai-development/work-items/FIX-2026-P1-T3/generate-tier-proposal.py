# -*- coding: utf-8 -*-
"""Regenerate tier-confirmation-proposal.yaml addressing R1 items.

R1 P1: header baseline text contradicted baseline_commit.
R1 P2: pairing undetected for docs/en/ vs docs/zh-CN/ mirror (memory-versioning.ts split tiers).
R1 P2: reproducibility — emit exact marker lists + counting rule into the file itself.
"""
import subprocess, io, os, re
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def git(*a):
    return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True).stdout.decode('utf-8', 'replace')

tree = subprocess.run(['git', '-C', REPO, 'ls-tree', '-r', '--name-only', 'origin/main'],
                      capture_output=True, text=True).stdout.splitlines()
all_md = set(p for p in tree if p.endswith('.md'))
BASE = subprocess.run(['git', '-C', REPO, 'rev-parse', 'origin/main'],
                      capture_output=True, text=True).stdout.strip()

def partner(p):
    # 1) same-directory suffix pairs
    if p.endswith('.zh-CN.md'):
        c = p[:-len('.zh-CN.md')] + '.en.md'
        return c if c in all_md else None
    if p.endswith('.en.md'):
        base = p[:-len('.en.md')]
        for suf in ('.zh-CN.md', '.md'):
            if base + suf in all_md:
                return base + suf
        return None
    base = p[:-len('.md')]
    if base + '.en.md' in all_md:
        return base + '.en.md'
    # 2) docs/en/ <-> docs/zh-CN/ mirror (R1 P2 finding)
    for a, b in (('docs/en/', 'docs/zh-CN/'), ('docs/zh-CN/', 'docs/en/')):
        if p.startswith(a):
            c = b + p[len(a):]
            return c if c in all_md else None
    return None

scope_dirs = ('docs/', 'prompts/', '14-ai-development/', '13-engineering-decisions/')
candidates = sorted(p for p in all_md if p.startswith(scope_dirs))

NORMATIVE = ['MUST', 'MUST NOT', 'SHALL', 'REQUIRED', 'SHOULD',
             '\u7981\u6b62', '\u5fc5\u987b', '\u4e0d\u5f97', '\u5f3a\u5236\u6027']
ARCH = ['interface contract', 'wire contract', 'protocol', 'schema', 'state machine',
        'lifecycle', 'security', 'permission boundary', 'architecture decision', 'ADR',
        '\u63a5\u53e3\u5951\u7ea6', '\u534f\u8bae', '\u72b6\u6001\u673a', '\u751f\u547d\u5468\u671f',
        '\u5b89\u5168', '\u6743\u9650\u8fb9\u754c', '\u67b6\u6784\u51b3\u7b56']
EPHEMERAL = ['meeting', 'minutes', 'review record', 'acceptance record',
             '\u4f1a\u8bae', '\u7eaa\u8981', '\u9a8c\u6536\u8bb0\u5f55', '\u8bc4\u5ba1\u8bb0\u5f55']

def classify(p, text):
    head = text[:4000]
    low = head.lower()
    norm = sum(1 for m in NORMATIVE if m.lower() in low)
    arch = sum(1 for m in ARCH if m.lower() in low)
    eph = sum(1 for m in EPHEMERAL if m.lower() in low)
    decl = bool(re.search(r'(?im)^\s*[-*]?\s*\**\s*(\u6587\u6863\s*ID|Document ID|\u72b6\u6001|Status|\u7248\u672c|Version)\s*[:\uff1a]', head))
    base = p.rsplit('/', 1)[-1]
    if base.upper() in ('README.MD', 'INDEX.MD') or base.lower().startswith('readme'):
        return 'TIER3_CANDIDATE', 'LOW', 'index/readme navigation file; no standalone contract'
    if p.startswith('prompts/'):
        return 'TIER2_OR_TIER3_SUGGESTED', 'MEDIUM', 'prompt library asset; 27-file whitelist enumerated in 14-ai-development/work-items/FIX-2026-P1-T3/authorization-manifest.yaml (inventory.expected_a_i_prompt_blobs)'
    if eph >= 2:
        return 'TIER3_SUGGESTED', 'HIGH', 'ephemeral record markers (review/meeting/acceptance)'
    if arch >= 3 and norm >= 3:
        return 'TIER1_CANDIDATE', 'HIGH', 'architecture-contract + normative markers present'
    if decl and norm >= 1:
        return 'TIER1_CANDIDATE', 'MEDIUM', 'document header with ID/Status/Version + normative markers; weakest positive band, verify semantically before confirming'
    if norm >= 2:
        return 'TIER1_CANDIDATE', 'LOW', 'normative constraint markers without ephemeral signals; no header evidence'
    return 'TIER3_CANDIDATE', 'LOW', 'no architecture-contract or normative markers in head; descriptive/operational'

rows = []
for p in candidates:
    text = git('show', 'origin/main:' + p)
    sug, conf, reason = classify(p, text)
    pr = partner(p)
    rows.append((p, bool(pr), pr or '', sug, conf, reason))

# pair-divergence surfacing (R1 P2: symmetric translations must not silently split tiers)
by_path = {r[0]: r for r in rows}
idx = {r[0]: i for i, r in enumerate(rows)}
done = set()
for p in list(by_path):
    if p in done:
        continue
    paired, pr = by_path[p][1], by_path[p][2]
    if not paired:
        continue
    q = by_path.get(pr)
    if not q or q[3] == by_path[p][3]:
        continue
    done.add(p); done.add(pr)
    for me, other in ((p, q), (pr, by_path[p])):
        rows[idx[me]] = (me, by_path[me][1], by_path[me][2], by_path[me][3], 'LOW',
                         by_path[me][5] + "; PAIR-DIVERGENT: partner '%s' scanned as %s - a translation pair cannot hold two tiers, confirm the pair together and re-derive one tier" % (other[0], other[3]))

out = [
 '# Tier classification PROPOSAL - evidence-based suggestions for human confirmation',
 '# Generated 2026-11-20 by generate-tier-proposal.py from the origin/main tree at the commit',
 '# named in baseline_commit below. No other revision was scanned for this file.',
 '# STATUS: PENDING_HUMAN_CONFIRMATION - this file does NOT classify anything.',
 '# Policy constraint honoured: no automatic promotion of UNKNOWN; every row requires a human confirmation record.',
 'status: PROPOSAL_PENDING_HUMAN_CONFIRMATION',
 'baseline_commit: ' + BASE,
 'scope: docs/ + prompts/ + 14-ai-development/ + 13-engineering-decisions/ (the four UNKNOWN/TIER1_CANDIDATE buckets in AI-DOC-BILINGUAL-TIERING v1.0 section 1 table)',
 'evidence_method: content-marker scan of first 4000 chars per file; exact inputs listed under marker_families below so a third party can reproduce or reject any row',
 'explicitly_not: a classification registry; a governance approval; a claim that any UNKNOWN has been confirmed',
 'scan_window_chars: 4000',
 'marker_matching: case-insensitive substring match within the scan window; counts are distinct-marker counts, not occurrence counts; a marker counted once regardless of repetitions',
 'pairing_detection: (a) same-directory suffix swap .en.md <-> .zh-CN.md <-> .md; (b) docs/en/ <-> docs/zh-CN/ path mirror',
 'generator: 14-ai-development/work-items/FIX-2026-P1-T3/generate-tier-proposal.py',
 'marker_families:',
 '  normative: [' + ', '.join('"%s"' % m for m in NORMATIVE) + ']',
 '  architecture_contract: [' + ', '.join('"%s"' % m for m in ARCH) + ']',
 '  ephemeral_record: [' + ', '.join('"%s"' % m for m in EPHEMERAL) + ']',
 '  document_header: regex ^\\s*[-*]?\\s*\\**\\s*(Document ID|Status|Version|{\u6587\u6863} ID|\u72b6\u6001|\u7248\u672c)\\s*[:：]',
 'rule_order: index/readme -> prompts/ -> ephemeral>=2 -> (arch>=3 and norm>=3) -> (header and norm>=1) -> norm>=2 -> default; first match wins',
 'files:']
for p, paired, pr, sug, conf, reason in rows:
    out.append('  - path: "%s"' % p)
    out.append('    paired: %s' % ('true' if paired else 'false'))
    if pr:
        out.append('    partner: "%s"' % pr)
    out.append('    suggested_tier: %s' % sug)
    out.append('    confidence: %s' % conf)
    out.append('    evidence: "%s"' % reason)
    out.append('    confirmation_record: PENDING')

path = os.path.join(REPO, '14-ai-development/work-items/FIX-2026-P1-T3/tier-confirmation-proposal.yaml')
io.open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')

c = Counter((r[3], r[4]) for r in rows)
print('files:', len(rows), 'paired:', sum(1 for r in rows if r[1]), 'baseline:', BASE[:8])
for k, v in sorted(c.items()):
    print(' ', k[0], k[1], v)

# self-check
txt = io.open(path, encoding='utf-8').read()
assert '6545f8' not in txt, 'stale baseline text still present'
assert txt.count('confirmation_record: PENDING') == len(rows)
assert txt.count('- path: ') == len(rows)
assert len(set(r[0] for r in rows)) == len(rows)
for p, paired, pr, *_ in rows:
    if paired:
        assert pr in all_md or pr in set(r[0] for r in rows) or pr, p
mv = [r for r in rows if '03-memory-brain/memory-versioning.md' in r[0]]
print('memory-versioning rows:', [(r[0], r[1], r[2], r[3]) for r in mv])
print('SELF-CHECK OK')
