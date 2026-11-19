#!/usr/bin/env python3
"""Additive, backup-first YAML status migration. Requires PyYAML; dry-run is default."""
import argparse, json, shutil, sys
from pathlib import Path
import yaml

PHASES = {
 "PROPOSED":"INTAKE","ANALYZED":"INTAKE","PROMPT_READY":"INTAKE",
 "READY":"READY","IN_PROGRESS":"ACTIVE","IMPLEMENTED":"ACTIVE",
 "VERIFIED":"VALIDATION","REVIEWED":"VALIDATION","INTEGRATION_READY":"VALIDATION",
 "ACCEPTED":"ACCEPTANCE","MERGED":"COMPLETE","CLOSED":"COMPLETE"
}

def run(path, apply=False, rollback=False):
 path=Path(path)
 backup=path.with_name(path.name+".pre-status-migration.bak")
 if rollback:
  if not backup.is_file(): raise ValueError("byte-for-byte backup missing")
  shutil.copy2(backup,path)
  return {"result":"ROLLED_BACK","path":str(path)}
 raw=path.read_bytes()
 data=yaml.safe_load(raw)
 if not isinstance(data,dict): raise ValueError("manifest root must be a mapping")
 source=data.get("status")
 if not isinstance(source,str) or not source.strip(): raise ValueError("missing/non-string status")
 token=source.strip().split()[0].upper()
 if token not in PHASES: raise ValueError("unknown/ambiguous status: "+token)
 phase=PHASES[token]
 if "lifecycle" in data:
  life=data["lifecycle"]
  if isinstance(life,dict) and life.get("source_status")==source and life.get("phase")==phase:
   return {"result":"ALREADY_MIGRATED","path":str(path),"phase":phase}
  raise ValueError("conflicting lifecycle metadata; refusing overwrite")
 markers={k:data[k] for k in ("blocked","rejected") if k in data}
 data["lifecycle"]={"phase":phase,"source_status":source,"gates":{
  "verified":{"status":"NOT_RECORDED"},"independent_review":{"status":"NOT_RECORDED"},
  "integration":{"status":"NOT_RECORDED"},"owner_acceptance":{"status":"NOT_RECORDED"},
  "merge":{"status":"NOT_RECORDED"},"closeout":{"status":"NOT_RECORDED"}
 },"markers":markers}
 if not apply: return {"result":"WOULD_MIGRATE","path":str(path),"phase":phase}
 if backup.exists(): raise ValueError("backup already exists; refusing overwrite")
 shutil.copy2(path,backup)
 path.write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False,width=1000),encoding="utf-8")
 return {"result":"MIGRATED","path":str(path),"phase":phase,"backup":str(backup)}

def main():
 p=argparse.ArgumentParser()
 p.add_argument("paths",nargs="+")
 g=p.add_mutually_exclusive_group()
 g.add_argument("--apply",action="store_true")
 g.add_argument("--rollback",action="store_true")
 a=p.parse_args(); failed=0
 for name in a.paths:
  try: print(json.dumps(run(name,a.apply,a.rollback),ensure_ascii=False))
  except Exception as e:
   failed+=1; print(json.dumps({"result":"BLOCKED","path":name,"error":str(e)},ensure_ascii=False))
 return 1 if failed else 0
if __name__=="__main__": sys.exit(main())
