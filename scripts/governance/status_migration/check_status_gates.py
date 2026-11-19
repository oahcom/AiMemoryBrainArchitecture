#!/usr/bin/env python3
"""Fail-closed gate validator for migrated YAML manifests. Requires PyYAML."""
import argparse,json,sys
from pathlib import Path
import yaml

PHASES={"INTAKE","READY","ACTIVE","VALIDATION","ACCEPTANCE","COMPLETE"}
REQUIRED={"VERIFIED":"verified","REVIEWED":"independent_review","INTEGRATION_READY":"integration","ACCEPTED":"owner_acceptance","MERGED":"merge","CLOSED":"closeout"}
def check(path):
 d=yaml.safe_load(Path(path).read_bytes())
 if not isinstance(d,dict): raise ValueError("manifest root must be a mapping")
 life=d.get("lifecycle")
 if not isinstance(life,dict) or life.get("phase") not in PHASES: raise ValueError("missing/invalid lifecycle phase")
 if life.get("source_status")!=d.get("status"): raise ValueError("source_status mismatch; original status must remain exact")
 gates=life.get("gates",{})
 if not isinstance(gates,dict): raise ValueError("lifecycle.gates must be a mapping")
 token=str(d.get("status","")).strip().split()[0].upper()
 if token in REQUIRED and REQUIRED[token] not in gates: raise ValueError("missing independent gate record: "+REQUIRED[token])
 markers=life.get("markers",{})
 if not isinstance(markers,dict): raise ValueError("lifecycle.markers must be a mapping")
 for marker in ("BLOCKED","REJECTED"):
  if marker in str(d.get("status","")).upper() and marker.lower() not in markers and marker.lower() not in d:
   raise ValueError("marker not separately recorded: "+marker)
 return {"result":"PASS","path":str(path),"phase":life["phase"]}
def main():
 p=argparse.ArgumentParser();p.add_argument("paths",nargs="+");a=p.parse_args();bad=0
 for f in a.paths:
  try: print(json.dumps(check(f),ensure_ascii=False))
  except Exception as e:
   bad+=1;print(json.dumps({"result":"FAIL","path":f,"error":str(e)},ensure_ascii=False))
 return 1 if bad else 0
if __name__=="__main__":sys.exit(main())
