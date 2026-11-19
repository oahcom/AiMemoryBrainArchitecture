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
sections={"tier1":{},"tier2":{},"tier3_per_file":{}}; rules=[]; section=current=pending=None
for line in mapping.read_text(encoding="utf-8").splitlines():
    top=re.match(r"^([A-Za-z0-9_]+):\s*$",line)
    if top: section=top.group(1); current=pending=None; continue
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
try:
    files=subprocess.run(["git","-C",str(root),"ls-files","-z","--","*.md"],check=True,capture_output=True).stdout.decode().split("\0")
except (OSError,subprocess.CalledProcessError) as exc:
    print(f"ERROR: cannot enumerate files: {exc}",file=sys.stderr); raise SystemExit(1)
rules.sort(key=lambda x:len(x[0]),reverse=True); unknown=[]; drift=[]
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
        actual=subprocess.run(["git","-C",str(root),"rev-parse",f"HEAD:{path}"],capture_output=True,text=True)
        if actual.returncode or actual.stdout.strip()!=sha:
            drift.append(path); print(f"STALE_BLOB_SHA\t{path}\texpected={sha}\tactual={actual.stdout.strip() or 'MISSING'}")
print("SUMMARY\t"+"\t".join(f"{k}={v}" for k,v in counts.items()))
if unknown: print(f"NEEDS_CONFIRMATION\t{len(unknown)} path(s); UNKNOWN is not PASS",file=sys.stderr)
if drift: print(f"BASELINE_DRIFT\t{len(drift)} Tier 1/2 blob SHA mismatch(es)",file=sys.stderr)
if drift: raise SystemExit(1)
if unknown: raise SystemExit(2)
PY
