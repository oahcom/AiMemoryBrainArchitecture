#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
ROOT="$(printenv REPO_ROOT || git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || pwd)"
MAPPING="$ROOT/14-ai-development/work-items/FIX-2026-P1-T3/tier-mapping-proposal.yaml"
if [ "$#" -gt 0 ]; then MAPPING="$1"; fi
PYTHON_BIN="$(printenv PYTHON_BIN || printf python3)"
exec "$PYTHON_BIN" - "$ROOT" "$MAPPING" <<'PY'
import re,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve(); mapping=Path(sys.argv[2])
if not mapping.is_absolute(): mapping=(root/mapping).resolve()
if not mapping.is_file(): print(f"ERROR: mapping missing: {mapping}",file=sys.stderr); raise SystemExit(1)
sections={"tier1":{},"tier2":{},"tier3_per_file":{}}; rules=[]; section=current=pending=None; baseline=None
for line in mapping.read_text(encoding="utf-8").splitlines():
    top=re.match(r"^([A-Za-z0-9_]+):\s*$",line)
    if top: section=top.group(1); current=pending=None; continue
    bm=re.match(r"^baseline_commit:\s*'?([0-9a-f]{40})",line)
    if bm: baseline=bm.group(1); continue
    if section in sections:
        m=re.match(r"^\s+- path:\s*[\"']?([^\"'#]+)[\"']?\s*$",line)
        if m: pending=m.group(1).strip(); sections[section][pending]=None; continue
        m=re.match(r"^\s+blob_sha:\s*[\"']?([0-9a-f]{40})",line)
        if m and pending: sections[section][pending]=m.group(1); pending=None
    elif section=="directory_rules":
        m=re.match(r"^\s+- directory:\s*[\"']?([^\"'#]+)[\"']?\s*$",line)
        if m: current=m.group(1).strip().rstrip("/")+"/"; continue
        m=re.match(r"^\s+tier:\s*([A-Z0-9_]+)",line)
        if m and current: rules.append((current,m.group(1))); current=None
# The declared baseline commit is the classification evidence anchor.
# Verify it exists and is a commit object; fall back to HEAD only if undeclared.
if baseline:
    kind=subprocess.run(["git","-C",str(root),"cat-file","-t",baseline],capture_output=True,text=True,encoding="utf-8",errors="replace")
    if kind.returncode or kind.stdout.strip()!="commit":
        print(f"ERROR: declared baseline_commit {baseline} is not a commit object",file=sys.stderr)
        raise SystemExit(1)
    ref=baseline
else:
    ref="HEAD"
try:
    files=subprocess.run(["git","-C",str(root),"ls-files","-z","--","*.md"],check=True,capture_output=True).stdout.decode("utf-8",errors="replace").split("\0")
except (OSError,subprocess.CalledProcessError) as exc:
    print(f"ERROR: cannot enumerate files: {exc}",file=sys.stderr); raise SystemExit(1)
rules.sort(key=lambda x:len(x[0]),reverse=True); unknown=[]; drift=[]; missing=[]
counts={"TIER1":0,"TIER2":0,"TIER3":0,"UNKNOWN":0}
for path in sorted(x for x in files if x):
    tier=sha=None
    for key,value in (("tier1","TIER1"),("tier2","TIER2"),("tier3_per_file","TIER3")):
        if path in sections[key]: tier,sha=value,sections[key][path]; break
    if tier is None:
        for prefix,declared in rules:
            if path.startswith(prefix):
                tier=declared if declared in ("TIER1","TIER2","TIER3") else "UNKNOWN"; break
    tier=tier or "UNKNOWN"; counts[tier]+=1; print(f"{tier}\t{path}")
    if tier=="UNKNOWN": unknown.append(path)
    if sha:
        actual=subprocess.run(["git","-C",str(root),"rev-parse",f"{ref}:{path}"],capture_output=True,text=True,encoding="utf-8",errors="replace")
        if actual.returncode or actual.stdout.strip()!=sha:
            drift.append(path); print(f"STALE_BLOB_SHA\t{path}\texpected={sha}\tactual={actual.stdout.strip() or 'MISSING'}\tref={ref}")
# Registered per-file entries must bind to the declared baseline tree:
# 1. every entry MUST carry a valid blob_sha (no unanchored registrations);
# 2. every registered path MUST exist in the baseline tree itself, checked
#    directly with git cat-file -e <baseline>:<path> — not inferred from the
#    working index, which can contain paths absent from the baseline.
for key in sections:
    for path,sha in sections[key].items():
        if not sha:
            missing.append(path); print(f"NO_BLOB_SHA\t{path}\tregistered in {key} without blob_sha",file=sys.stderr); continue
        probe=subprocess.run(["git","-C",str(root),"cat-file","-e",f"{ref}:{path}"],capture_output=True)
        if probe.returncode:
            missing.append(path); print(f"MISSING_IN_BASELINE\t{path}\tregistered in {key} but absent from tree {ref}",file=sys.stderr)
print("SUMMARY\t"+"\t".join(f"{k}={v}" for k,v in counts.items()))
if unknown: print(f"NEEDS_CONFIRMATION\t{len(unknown)} path(s); UNKNOWN is not PASS",file=sys.stderr)
if drift: print(f"BASELINE_DRIFT\t{len(drift)} blob SHA mismatch(es) against declared baseline {ref}",file=sys.stderr)
if missing: print(f"BASELINE_BINDING_FAIL\t{len(missing)} registered path(s) missing from baseline tree or lacking blob_sha",file=sys.stderr)
if drift or missing: raise SystemExit(1)
if unknown: raise SystemExit(2)
PY
