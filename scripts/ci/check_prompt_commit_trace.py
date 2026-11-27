#!/usr/bin/env python3
"""Read-only prompt-to-implementation trace audit.

Primary decision order (contract; tested): NO_TRACE first when either required
identity is absent/placeholder; then DIGEST_MISMATCH when the prompt is not
pinned and verified; then COMMIT_UNREACHABLE; otherwise TRACEABLE.
The independent findings and prompt×commit matrix retain orthogonal facts.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_ROOT = "14-ai-development/work-items"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
PLACEHOLDERS = {"", "PENDING", "NOT_STARTED", "NOT_VERIFIED", "N/A", "NULL"}
PRIMARY = ("NO_TRACE", "DIGEST_MISMATCH", "COMMIT_UNREACHABLE", "TRACEABLE")
PROMPT = ("PINNED_OK", "HEAD_MATCH", "UNPINNED_MISMATCH", "ABSENT")
COMMITS = ("REACHABLE", "UNREACHABLE", "ABSENT")
FINDINGS = ("digest_absent", "digest_not_verified", "digest_unpinned",
 "digest_head_mismatch", "digest_pinned_mismatch", "commit_absent",
 "commit_pending", "commit_unresolvable", "commit_unreachable")

def git(root, *args, check=True):
    p = subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode:
        raise RuntimeError(p.stderr.decode("utf-8", "replace").strip())
    return p.stdout

def real(v):
    return isinstance(v, str) and v.strip().upper() not in PLACEHOLDERS

def manifests(root, ref):
    names = git(root, "ls-tree", "-r", "--name-only", ref).decode().splitlines()
    return sorted(p for p in names if p.startswith(MANIFEST_ROOT + "/") and p.endswith("/manifest.yaml"))

def blob(root, commit, path):
    if not real(commit) or not re.fullmatch(r"[0-9a-fA-F]{7,40}", commit):
        return None
    resolved = git(root, "rev-parse", "--verify", commit + "^{commit}", check=False).decode().strip()
    if not HEX40.fullmatch(resolved): return None
    p = subprocess.run(["git", "show", resolved + ":" + path], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout if p.returncode == 0 else None

def audit(root, ref):
    rows = []
    for mp in manifests(root, ref):
        raw = blob(root, ref, mp)
        if raw is None: raise RuntimeError("cannot read manifest " + mp)
        doc = yaml.safe_load(raw.decode("utf-8")) or {}
        digest, pfile = doc.get("prompt_sha256"), doc.get("prompt_file")
        pblob, pcommit = doc.get("prompt_file_blob_sha"), doc.get("prompt_file_commit_sha")
        impl = doc.get("implementation_commit_sha")
        findings = []
        if not real(digest): findings.append("digest_absent" if digest is None else "digest_not_verified")
        pin = real(pblob) and real(pcommit)
        if not pin and real(digest): findings.append("digest_unpinned")
        head_bytes = blob(root, ref, pfile) if real(pfile) else None
        head_match = bool(head_bytes is not None and HEX64.fullmatch(str(digest or "")) and hashlib.sha256(head_bytes).hexdigest() == digest.lower())
        if real(digest) and not head_match: findings.append("digest_head_mismatch")
        pinned_bytes = blob(root, pcommit, pfile) if pin and real(pfile) else None
        pinned_blob = (git(root, "rev-parse", "--verify", f"{pcommit}:{pfile}", check=False).decode().strip()
                       if pinned_bytes is not None else "")
        pinned_ok = bool(pinned_bytes is not None and pinned_blob == str(pblob).lower() and
                         HEX64.fullmatch(str(digest or "")) and
                         hashlib.sha256(pinned_bytes).hexdigest() == digest.lower())
        if pin and not pinned_ok: findings.append("digest_pinned_mismatch")
        if not real(impl):
            findings.append("commit_absent" if impl is None else "commit_pending")
            cdim = "ABSENT"
        else:
            resolved = git(root, "rev-parse", "--verify", str(impl) + "^{commit}", check=False).decode().strip()
            if not HEX40.fullmatch(resolved):
                findings.append("commit_unresolvable"); cdim = "UNREACHABLE"
            else:
                target = doc.get("merge_commit_sha") or doc.get("base_commit_sha") or ref
                target_sha = git(root, "rev-parse", "--verify", str(target) + "^{commit}", check=False).decode().strip()
                ancestor = False
                if HEX40.fullmatch(target_sha):
                    probe = subprocess.run(["git", "merge-base", "--is-ancestor", resolved, target_sha],
                                           cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    ancestor = probe.returncode == 0
                cdim = "REACHABLE" if ancestor else "UNREACHABLE"
                if not ancestor: findings.append("commit_unreachable")
        pdim = "PINNED_OK" if pin and pinned_ok else ("HEAD_MATCH" if not pin and head_match else ("UNPINNED_MISMATCH" if real(digest) else "ABSENT"))
        # Contract decision order is intentionally explicit and must not be reordered.
        if not real(digest) or not real(impl): primary = "NO_TRACE"
        elif pdim != "PINNED_OK": primary = "DIGEST_MISMATCH"
        elif cdim != "REACHABLE": primary = "COMMIT_UNREACHABLE"
        else: primary = "TRACEABLE"
        rows.append({"manifest":mp,"work_item_id":doc.get("work_item_id",Path(mp).parent.name),
                     "primary_status":primary,"findings":findings,"prompt_dimension":pdim,
                     "commit_dimension":cdim})
    return rows

def summarize(rows):
    counts={s:0 for s in PRIMARY}; matrix={p:{c:0 for c in COMMITS} for p in PROMPT}
    fc={f:0 for f in FINDINGS}
    for r in rows:
        counts[r["primary_status"]]+=1; matrix[r["prompt_dimension"]][r["commit_dimension"]]+=1
        for f in r["findings"]: fc[f]+=1
    return {"manifest_count":len(rows),"primary_status":counts,"matrix":matrix,"findings":fc,
            "manifests":rows}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root",type=Path,default=ROOT); ap.add_argument("--commit",default="HEAD")
    ap.add_argument("--json",action="store_true")
    ap.add_argument("--baseline",type=Path)
    args=ap.parse_args()
    try:
        ref=git(args.root,"rev-parse",args.commit+"^{commit}").decode().strip()
        result=summarize(audit(args.root,ref))
        if args.baseline:
            base=json.loads(args.baseline.read_text())
            old=base.get("manifests",{})
            rank={s:i for i,s in enumerate(PRIMARY)}
            violations=[]
            for r in result["manifests"]:
                ident=r["work_item_id"]; prior=old.get(ident)
                if prior is None and r["primary_status"]!="TRACEABLE":
                    violations.append(f"NEW_NON_TRACEABLE {ident} {r['primary_status']}")
                elif prior and rank[r["primary_status"]]>rank[prior["primary_status"]]:
                    violations.append(f"REGRESSION {ident} {prior['primary_status']} -> {r['primary_status']}")
            if args.json: print(json.dumps(result,sort_keys=True,indent=2))
            else:
                print(f"PROMPT-COMMIT-TRACE main={ref} manifests={result['manifest_count']}")
                for s,n in result["primary_status"].items(): print(f"PRIMARY {s}={n}")
                for p,cs in result["matrix"].items():
                    for c,n in cs.items(): print(f"MATRIX {p} x {c}={n}")
                for f,n in result["findings"].items(): print(f"FINDING {f}={n}")
                for r in result["manifests"]: print(f"{r['primary_status']} {r['work_item_id']} findings={','.join(r['findings']) or '-'}")
                for v in violations: print(v)
            return 1 if violations else 0
        print(json.dumps(result,sort_keys=True,indent=2) if args.json else result)
        return 0
    except Exception as exc:
        print(f"INCOMPLETE: {exc}",file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main())
