#!/usr/bin/env python3
"""Diff-only human translation work-order generator; no model/API calls."""
import argparse,difflib,hashlib,sys
from pathlib import Path
def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(65536),b""): h.update(chunk)
    return h.hexdigest()
def failure(out,source,target,error):
    body=("# Translation Work Order\n\nstatus: FAILED\nresult: NOT_GENERATED\n\n"
          f"- source: {source}\n- target: {target}\n- failure: {error}\n"
          "- required_action: resolve input/output error and rerun generator\n")
    try: out.parent.mkdir(parents=True,exist_ok=True); out.write_text(body,encoding="utf-8")
    except OSError as write_error:
        print(f"ERROR: failure registration also failed: {write_error}",file=sys.stderr); return 2
    print(f"FAILED: {error}; failure status registered at {out}",file=sys.stderr); return 1
def main():
    p=argparse.ArgumentParser(description="Compare bilingual Markdown and generate a human checklist.")
    p.add_argument("--source",required=True); p.add_argument("--target",required=True); p.add_argument("--output",required=True)
    a=p.parse_args(); source,target,out=Path(a.source),Path(a.target),Path(a.output)
    try:
        sl=source.read_text(encoding="utf-8").splitlines(); tl=target.read_text(encoding="utf-8").splitlines()
        matcher=difflib.SequenceMatcher(None,[x.rstrip() for x in sl],[x.rstrip() for x in tl],autojunk=False)
        changes=[x for x in matcher.get_opcodes() if x[0]!="equal"]; blocks=[]
        for n,(tag,i1,i2,j1,j2) in enumerate(changes,1):
            blocks.append(f"## Item {n}: {tag.upper()}\n\n- Source lines: {i1+1}-{i2}\n- Counterpart lines: {j1+1}-{j2}\n- [ ] Human translator/reviewer: reconcile; preserve normative force, identifiers, status, examples and links.\n")
            if i1<i2: blocks.append("Source excerpt (indented):\n\n    "+"\n    ".join(sl[i1:i2][:8])+"\n")
            if j1<j2: blocks.append("Counterpart excerpt (indented):\n\n    "+"\n    ".join(tl[j1:j2][:8])+"\n")
        status="PENDING_TRANSLATION" if changes else "NO_DIFFERENCES_DETECTED"
        report=["# Translation Work Order","",f"status: {status}","generator: translate-document.py (diff-only; no model/API invocation)",
                f"- source: {source.as_posix()}",f"- target: {target.as_posix()}",
                f"- source_sha256: {digest(source)}",f"- target_sha256: {digest(target)}",
                f"- changed_blocks: {len(changes)}","","## Checklist",""]
        report.extend(blocks or ["- [x] No textual differences detected; semantic parity still requires human review."])
        out.parent.mkdir(parents=True,exist_ok=True); out.write_text("\n".join(report).rstrip()+"\n",encoding="utf-8")
        print(f"{status}: {len(changes)} changed block(s) -> {out}"); return 0
    except (OSError,UnicodeError) as e: return failure(out,source,target,str(e))
if __name__=="__main__": raise SystemExit(main())
