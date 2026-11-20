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
    p = subprocess.run(['git', '-C', REPO] + list(a), capture_output=True)
    # strict decode: a UnicodeDecodeError is itself the read-failure signal.
    # errors='replace' was rejected because a legitimate U+FFFD in valid UTF-8
    # would then be indistinguishable from a decode artefact.
    try:
        return p.stdout.decode('utf-8'), p.returncode == 0, False
    except UnicodeDecodeError:
        return '', p.returncode == 0, True

tree, tree_ok, tree_bad = git('ls-tree', '-r', '--name-only', 'origin/main')
assert tree_ok and not tree_bad, 'git ls-tree failed or was not valid UTF-8; refusing to write a proposal from a partial tree'
all_md = set(p for p in tree.splitlines() if p.endswith('.md'))
BASE = subprocess.run(['git', '-C', REPO, 'rev-parse', 'origin/main'],
                      capture_output=True, text=True).stdout.strip()

def build_pairs():
    """Return {path: partner}. Pairing is computed once, globally, so the
    result is reciprocal by construction.

    Order of claims (a file already paired is not claimed again):
      1. x.zh-CN.md <-> x.en.md
      2. x.en.md <-> x.md            (only if that .en.md is still free)
      3. docs/en/P <-> docs/zh-CN/P
    A plain x.md whose x.en.md is already taken by a x.zh-CN.md is left
    unpaired rather than forced into a non-reciprocal link.
    """
    pairs = {}

    def claim(a, b):
        if a not in all_md or b not in all_md:
            return False
        if a in pairs or b in pairs:
            return False
        pairs[a] = b
        pairs[b] = a
        return True

    for p in sorted(all_md):
        if p.endswith('.zh-CN.md'):
            claim(p, p[:-len('.zh-CN.md')] + '.en.md')
    for p in sorted(all_md):
        if p.endswith('.en.md'):
            claim(p, p[:-len('.en.md')] + '.md')
    for p in sorted(all_md):
        for a, b in (('docs/en/', 'docs/zh-CN/'), ('docs/zh-CN/', 'docs/en/')):
            if p.startswith(a):
                claim(p, b + p[len(a):])
    return pairs

PAIRS = build_pairs()

def partner(p):
    return PAIRS.get(p)

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

HEADER_RE = r'(?im)^\s*[-*]?\s*\**\s*(\u6587\u6863\s*ID|Document ID|\u72b6\u6001|Status|\u7248\u672c|Version)\s*[:\uff1a]'

def classify(p, text):
    head = text[:4000]
    low = head.lower()
    norm = sum(1 for m in NORMATIVE if m.lower() in low)
    arch = sum(1 for m in ARCH if m.lower() in low)
    eph = sum(1 for m in EPHEMERAL if m.lower() in low)
    decl = bool(re.search(HEADER_RE, head))
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
read_failures = []
for p in candidates:
    text, ok, bad = git('show', 'origin/main:' + p)
    sug, conf, reason = classify(p, text)
    if bad:
        read_failures.append(p)
        reason = 'READ-FAILURE: bytes were not valid UTF-8 and strict decode refused them; no scan of this file took place. ' + reason
        conf = 'LOW'
    elif not ok:
        read_failures.append(p)
        reason = 'READ-FAILURE: git show exited non-zero for this path; the empty scan below is an artefact, not a finding. ' + reason
        conf = 'LOW'
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
                         by_path[me][5] + "; PAIR-DIVERGENT: partner '%s' scanned as %s - the two sides of one translation pair cannot hold two tiers, so at most one of the two suggestions is right. Confirm the pair together and derive one tier for both. This flag records a conflict between the heuristic and itself; it is not evidence that a human read of either file would differ." % (other[0], other[3]))

# ---- validate BEFORE any write: a failing assertion must leave no file behind ----
by_path_final = {r[0]: r for r in rows}
pair_bad = []
for p, paired, pr, *_ in rows:
    if not paired:
        assert not pr, p
        continue
    assert pr in all_md, 'partner not in tree: %s -> %s' % (p, pr)
    back = partner(pr)
    if back != p:
        pair_bad.append((p, pr, back))
assert not pair_bad, 'non-reciprocal pairing: %r' % pair_bad[:5]

divergent = sorted({r[0] for r in rows if 'PAIR-DIVERGENT' in r[5]})

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
 'file_enumeration: git ls-tree -r --name-only origin/main, filtered to paths ending .md and starting with one of the four scope prefixes, then sorted with Python sorted() (byte-wise ASC on the full path). No glob, no .gitignore, no filesystem walk - the tree object is the only source.',
 'path_exclusions: none beyond the scope prefixes and the .md filter; the proposal files themselves are not excluded, so they appear as UNKNOWN-bucket rows like any other new document',
 'read_failure_handling: strict UTF-8 decode (UnicodeDecodeError is the failure signal; errors=replace is rejected because a legitimate U+FFFD would be indistinguishable from a decode artefact) plus a non-zero git show exit; either condition prefixes the row evidence with READ-<FAILURE> and forces LOW confidence; such a row is never equivalent to a genuine negative',
 'write_order: all assertions (pairing reciprocity, row counts, no stale baseline text, no tabs) run against the in-memory text before any byte reaches disk; the text is then written to a .tmp in the same directory through a context manager, so the handle is closed before os.replace promotes it; any exception removes the .tmp and re-raises, so a failing run leaves no partial proposal',
 'run_environment: python 3.13, git 2.x, no network access, no third-party packages; output is LF-terminated UTF-8',
 'marker_matching: case-insensitive substring match within the scan window; counts are distinct-marker counts, not occurrence counts; a marker counted once regardless of repetitions',
 'pairing_detection: computed once, globally, as a set of mutual claims, so reciprocity holds by construction. Claim order: (1) x.zh-CN.md <-> x.en.md; (2) x.en.md <-> x.md; (3) docs/en/P <-> docs/zh-CN/P. A file already paired is never claimed again, so a plain x.md whose x.en.md is already taken by a x.zh-CN.md is left unpaired rather than forced into a non-reciprocal link. A claim whose counterparty is absent from the baseline tree is dropped.',
 'generator: 14-ai-development/work-items/FIX-2026-P1-T3/generate-tier-proposal.py',
 'marker_families:',
 '  normative: [' + ', '.join('"%s"' % m for m in NORMATIVE) + ']',
 '  architecture_contract: [' + ', '.join('"%s"' % m for m in ARCH) + ']',
 '  ephemeral_record: [' + ', '.join('"%s"' % m for m in EPHEMERAL) + ']',
 '  document_header: regex ' + HEADER_RE,
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

text = '\n'.join(out) + '\n'

# ---- validate the built string before it is allowed to touch disk ----
assert '6545f8' not in text, 'stale baseline text still present'
assert text.count('confirmation_record: PENDING') == len(rows)
assert text.count('- path: ') == len(rows)
assert len(set(r[0] for r in rows)) == len(rows)
assert text.count('PAIR-DIVERGENT') == len(divergent)
assert text.count('\t') == 0, 'tab character in output'

# ---- atomic write: temp file in the same directory, then os.replace ----
# The handle is closed by the `with` block before os.replace runs, so a
# successful replace is a complete file; any exception before the replace
# removes the temp file and leaves the previous proposal (or none) in place.
path = os.path.join(REPO, '14-ai-development/work-items/FIX-2026-P1-T3/tier-confirmation-proposal.yaml')
tmp = path + '.tmp'
try:
    with io.open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    os.replace(tmp, path)
except BaseException:
    if os.path.exists(tmp):
        os.remove(tmp)
    raise

c = Counter((r[3], r[4]) for r in rows)
print('files:', len(rows), 'paired:', sum(1 for r in rows if r[1]), 'baseline:', BASE[:8])
for k, v in sorted(c.items()):
    print(' ', k[0], k[1], v)
print('divergent pairs:', len(divergent) // 2, 'rows:', len(divergent))
for p in divergent:
    print('  DIV', p, '->', by_path_final[p][2])
print('read failures:', len(read_failures), read_failures[:5])
print('SELF-CHECK OK')
