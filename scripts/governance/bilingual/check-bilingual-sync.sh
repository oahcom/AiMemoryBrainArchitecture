#!/usr/bin/env bash
set -euo pipefail
PYTHON_BIN="$(printenv PYTHON_BIN || printf python3)"
# exec preserves checker failure status; do not mask it with ! or a conditional pipeline.
exec "$PYTHON_BIN" - "$@" <<'PY'
import argparse,re,sys,os
from pathlib import Path
def meta(text,key):
    m=re.search(r"(?im)^\s*(?:<!--\s*)?"+re.escape(key)+r"\s*[:=]\s*([^\s>]+)",text)
    return m.group(1).strip().rstrip("-->") if m else None
p=argparse.ArgumentParser(description="Verify bilingual source revision and reciprocal pairing metadata.")
p.add_argument("--source",required=True); p.add_argument("--counterpart",required=True); a=p.parse_args()
source,target=Path(a.source),Path(a.counterpart)
try: st,tt=source.read_text(encoding="utf-8"),target.read_text(encoding="utf-8")
except OSError as e: print(f"FAIL: cannot read bilingual pair: {e}",file=sys.stderr); raise SystemExit(1)
sv=meta(st,"source-revision") or meta(st,"source-version"); tv=meta(tt,"source-revision") or meta(tt,"source-version")
if not sv or not tv: print("FAIL: both files need source-revision or source-version",file=sys.stderr); raise SystemExit(1)
if sv!=tv: print(f"FAIL: source revision mismatch: {sv!r} != {tv!r}",file=sys.stderr); raise SystemExit(1)
sp,tp=meta(st,"bilingual-pair"),meta(tt,"bilingual-pair")
if not sp or not tp: print("FAIL: reciprocal bilingual-pair metadata is required",file=sys.stderr); raise SystemExit(1)
expected_t=os.path.relpath(target.resolve(),source.resolve().parent); expected_s=os.path.relpath(source.resolve(),target.resolve().parent)
if Path(sp).as_posix()!=Path(expected_t).as_posix(): print(f"FAIL: source pair points to {sp!r}, expected {expected_t!r}",file=sys.stderr); raise SystemExit(1)
if Path(tp).as_posix()!=Path(expected_s).as_posix(): print(f"FAIL: counterpart pair points to {tp!r}, expected {expected_s!r}",file=sys.stderr); raise SystemExit(1)
print(f"PASS: source revision and reciprocal pairing verified ({sv})")
PY
