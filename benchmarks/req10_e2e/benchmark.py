#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math, os, shlex, subprocess, sys, time
from pathlib import Path

def pct(values, p):
    s=sorted(values); rank=(len(s)-1)*p; lo=math.floor(rank); hi=math.ceil(rank)
    return s[lo] if lo==hi else s[lo]*(hi-rank)+s[hi]*(rank-lo)

def storage_bytes(path):
    if path is None or not path.exists(): return None
    if path.is_file(): return path.stat().st_size
    return sum(p.stat().st_size for p in path.rglob('*') if p.is_file())

def usage():
    try:
        import resource
        r=resource.getrusage(resource.RUSAGE_CHILDREN)
        return r.ru_utime+r.ru_stime, r.ru_maxrss
    except (ImportError, AttributeError, OSError): return None

def send(proc, payload):
    proc.stdin.write(json.dumps(payload,separators=(',',':'))+'\n'); proc.stdin.flush()
    line=proc.stdout.readline()
    if not line: raise RuntimeError(f'adapter exited before response (rc={proc.poll()}): {proc.stderr.read()}')
    result=json.loads(line)
    if not isinstance(result,dict): raise RuntimeError('adapter response must be a JSON object')
    return result

def main():
    ap=argparse.ArgumentParser(description='JSONL end-to-end workload benchmark harness')
    ap.add_argument('--command',required=True); ap.add_argument('--samples',type=int,default=100)
    ap.add_argument('--warmup',type=int,default=10); ap.add_argument('--concurrency',type=int,default=1)
    ap.add_argument('--records',type=int,default=1000); ap.add_argument('--memories',type=int,default=100)
    ap.add_argument('--claims-per-memory',type=int,default=3); ap.add_argument('--storage-path',type=Path)
    ap.add_argument('--report',type=Path,default=Path('benchmark-report.json')); a=ap.parse_args()
    if a.samples<1 or a.warmup<0 or a.concurrency!=1: ap.error('samples >= 1, warmup >= 0, concurrency == 1 required')
    if min(a.records,a.memories,a.claims_per_memory)<0: ap.error('dataset dimensions must be non-negative')
    before_store=storage_bytes(a.storage_path); before_usage=usage(); lat=[]; stages={}
    calls=itok=otok=0; costs=[]; metrics_ok=True
    proc=subprocess.Popen(shlex.split(a.command),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
    for i in range(a.warmup+a.samples):
        phase='warmup' if i<a.warmup else 'measure'
        payload={'workload':'representative_memory_ingest_compile_retrieve_context','phase':phase,'operation_index':i,
          'dataset':{'records':a.records,'memories':a.memories,'claims_per_memory':a.claims_per_memory,'approx_claims':a.memories*a.claims_per_memory},'concurrency':a.concurrency}
        t=time.perf_counter(); result=send(proc,payload); elapsed=(time.perf_counter()-t)*1000
        if phase=='warmup': continue
        lat.append(elapsed)
        if isinstance(result.get('stage_ms'),dict):
            for k,v in result['stage_ms'].items():
                if isinstance(v,(int,float)): stages.setdefault(str(k),[]).append(float(v))
        m=result.get('model_metrics')
        if isinstance(m,dict) and all(k in m for k in ('calls','input_tokens','output_tokens','cost_usd')):
            calls+=int(m['calls']); itok+=int(m['input_tokens']); otok+=int(m['output_tokens']); costs.append(float(m['cost_usd']))
        else: metrics_ok=False
    proc.stdin.close(); rc=proc.wait(timeout=30); stderr=proc.stderr.read()
    if rc: raise RuntimeError(f'adapter exited rc={rc}: {stderr}')
    after_usage=usage(); after_store=storage_bytes(a.storage_path); cpu=None; rss=None
    if before_usage is not None and after_usage is not None:
        cpu=max(0,after_usage[0]-before_usage[0]); rss=after_usage[1]*(1024 if sys.platform.startswith('linux') else 1)
    elapsed=sum(lat)/1000
    report={'classification':'DEV_BASELINE_HARNESS_FIXTURE_OR_UNVERIFIED_ADAPTER','integrated_runtime':'NOT_MEASURED',
      'workload':'representative_memory_ingest_compile_retrieve_context','dataset':{'records':a.records,'memories':a.memories,'claims_per_memory':a.claims_per_memory,'approx_claims':a.memories*a.claims_per_memory},
      'environment':{'python':sys.version.split()[0],'platform':sys.platform,'system':os.uname().sysname if hasattr(os,'uname') else os.name,'command':shlex.split(a.command)},
      'concurrency':a.concurrency,'warmup':a.warmup,'samples':len(lat),'latency_ms':{'p50':pct(lat,.5),'p95':pct(lat,.95),'p99':pct(lat,.99)},
      'throughput_ops_per_sec':len(lat)/elapsed if elapsed else None,
      'process_wide':{'cpu_seconds':cpu if cpu is not None else 'NOT_MEASURED','peak_rss_bytes':rss if rss is not None else 'NOT_MEASURED','storage_bytes_before':before_store if before_store is not None else 'NOT_MEASURED','storage_bytes_after':after_store if after_store is not None else 'NOT_MEASURED'},
      'per_operation':{'cpu_seconds':'NOT_MEASURED','peak_memory_bytes':'NOT_MEASURED','storage_bytes':'NOT_MEASURED'},
      'stage_latency_ms':{k:{'p50':pct(v,.5),'p95':pct(v,.95),'p99':pct(v,.99)} for k,v in stages.items()},
      'model_metrics':{'calls':calls,'input_tokens':itok,'output_tokens':otok,'cost_usd':sum(costs)} if metrics_ok and len(costs)==len(lat) else 'NOT_MEASURED',
      'notes':['Harness execution is not evidence of an integrated product-runtime path.','Process CPU and peak RSS are child-process-wide; no per-operation attribution is inferred.','Stage timings are adapter-reported.','Storage footprint is file/directory bytes before and after; absent path is NOT_MEASURED.','Throughput uses summed measured request wall time; serial concurrency is 1.']}
    a.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('classification=DEV_BASELINE_HARNESS_FIXTURE_OR_UNVERIFIED_ADAPTER'); print('integrated_runtime=NOT_MEASURED')
    print(f'samples={len(lat)} warmup={a.warmup} concurrency={a.concurrency} dataset=records:{a.records},memories:{a.memories},claims_per_memory:{a.claims_per_memory}')
    print('latency_ms p50={:.3f} p95={:.3f} p99={:.3f}'.format(pct(lat,.5),pct(lat,.95),pct(lat,.99)))
    print('throughput_ops_per_sec={:.3f}'.format(len(lat)/elapsed))
    print(f'process_cpu_seconds={cpu if cpu is not None else "NOT_MEASURED"} peak_rss_bytes={rss if rss is not None else "NOT_MEASURED"}')
    print(f'storage_bytes_before={before_store if before_store is not None else "NOT_MEASURED"} storage_bytes_after={after_store if after_store is not None else "NOT_MEASURED"}')
    print(f'per_operation_cpu=NOT_MEASURED per_operation_memory=NOT_MEASURED model_tokens_cost={"measured" if metrics_ok and len(costs)==len(lat) else "NOT_MEASURED"}')
    print(f'report={a.report}'); return 0
if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as e: print(f'ERROR: {e}',file=sys.stderr); raise SystemExit(1)
