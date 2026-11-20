#!/usr/bin/env python3
"""REQ-06 pilot: repository-document retrieval evaluation; stdlib only.

The third arm is a policy-shaped reference proxy, NOT the integrated Brain runtime.
No model inference, production storage, adapter, or real user telemetry is exercised.
"""
from __future__ import annotations
import argparse, hashlib, json, math, re, statistics, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "corpus.jsonl"
TOP_K = 3
STOP = {"a","an","and","are","as","at","be","before","by","does","for","from","how","in","is","it","of","on","or","that","the","this","to","what","when","which","with"}
TASKS = [
 {"id":"T1-continuity","class":"long_horizon_continuity","query":"portable traceable memory across agents models runtimes","relevant":["DOC-README-ARCH"]},
 {"id":"T2-layer-facts","class":"factual_recall","query":"difference canonical memory memory context applied context adapter proof","relevant":["DOC-README-LAYERS","DOC-CONTEXT-APPLIED"]},
 {"id":"T3-scope-safety","class":"factual_recall","query":"permission scope predicate before candidate ranking global ANN post filter","relevant":["DOC-RETRIEVAL-SCOPE"]},
 {"id":"T4-routing-plan","class":"planning","query":"route rare quoted terms full text temporal entity relation provenance source proof","relevant":["DOC-RETRIEVAL-CHANNELS"]},
 {"id":"T5-correction-forget","class":"correction","query":"forget fence suppress stale cache and activation forgotten lifecycle archived","relevant":["DOC-LIFECYCLE-FORGET","DOC-RETRIEVAL-FRESHNESS"]},
 {"id":"T6-lineage","class":"factual_recall","query":"source digest locator evidence role provenance derivation lineage authenticity truth","relevant":["DOC-EVIDENCE-PROVENANCE"]},
 {"id":"T7-abstain-personal","class":"negative_abstention","query":"what food does this user personally prefer for breakfast","relevant":[]},
]

def tokens(s: str) -> set[str]:
    return {x for x in re.findall(r"[a-z0-9]+", s.lower()) if len(x)>1 and x not in STOP}

def load_corpus():
    rows=[json.loads(line) for line in CORPUS.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len({r["id"] for r in rows}) != len(rows): raise ValueError("duplicate corpus id")
    return rows

def no_memory(_task, _rows): return []

def lexical(task, rows):
    q=tokens(task["query"])
    scored=[]
    for row in rows:
        overlap=q & tokens(row["text"])
        if overlap:
            score=len(overlap)/len(q) + 0.15*len(overlap)/len(tokens(row["text"]))
            scored.append((score,row["id"]))
    return [doc_id for score,doc_id in sorted(scored,key=lambda x:(-x[0],x[1]))[:TOP_K]]

def brain_policy_proxy(task, rows):
    # Explicit policy gates: exact project scope, active lifecycle, repository-backed evidence.
    eligible=[r for r in rows if r["scope"]=="project:AiMemoryBrainArchitecture"
              and r["lifecycle"]=="active" and r["evidence_state"]=="documented"
              and r["source_kind"]=="repository_document" and len(r["source_blob"])==40]
    return lexical(task, eligible)

def wilson(successes, n, z=1.959963984540054):
    if n==0: return [0.0,1.0]
    p=successes/n; den=1+z*z/n
    center=(p+z*z/(2*n))/den
    half=z*math.sqrt((p*(1-p)+z*z/(4*n))/n)/den
    return [round(max(0,center-half),4),round(min(1,center+half),4)]

def evaluate(name, fn, rows):
    results=[]; lat=[]
    for task in TASKS:
        start=time.perf_counter(); selected=fn(task,rows); lat.append((time.perf_counter()-start)*1000)
        relevant=set(task["relevant"]); got=set(selected)
        if relevant:
            success=bool(relevant & got)
            recall=len(relevant & got)/len(relevant)
            precision=len(relevant & got)/len(got) if got else 0.0
            rr=next((1/(i+1) for i,x in enumerate(selected) if x in relevant),0.0)
        else:
            success=(len(selected)==0); recall=1.0 if not selected else 0.0
            precision=1.0 if not selected else 0.0; rr=1.0 if not selected else 0.0
        selected_rows=[next(r for r in rows if r["id"]==x) for x in selected]
        harmful=sum(1 for r in selected_rows if r["lifecycle"]!="active" or r["scope"]!="project:AiMemoryBrainArchitecture")
        results.append({"task":task["id"],"class":task["class"],"success":success,"selected":selected,
                        "recall":recall,"precision":precision,"reciprocal_rank":rr,
                        "harmful_activations":harmful})
    n=len(results); positives=sum(bool(t["relevant"]) for t in TASKS)
    return {"arm":name,"task_success_rate":round(sum(x["success"] for x in results)/n,4),
            "task_success_wilson95":wilson(sum(x["success"] for x in results),n),
            "positive_task_hit_rate":round(sum(x["success"] for x,t in zip(results,TASKS) if t["relevant"])/positives,4),
            "mean_recall":round(statistics.mean(x["recall"] for x,t in zip(results,TASKS) if t["relevant"]),4),
            "mean_precision":round(statistics.mean(x["precision"] for x,t in zip(results,TASKS) if t["relevant"]),4),
            "mrr_all_tasks":round(statistics.mean(x["reciprocal_rank"] for x in results),4),
            "harmful_activations":sum(x["harmful_activations"] for x in results),
            "selected_count":sum(len(x["selected"]) for x in results),
            "median_local_latency_ms":round(statistics.median(lat),4),"tasks":results}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--json",action="store_true"); args=ap.parse_args()
    rows=load_corpus()
    arms=[evaluate("no_memory",no_memory,rows),evaluate("simple_lexical_top3",lexical,rows),
          evaluate("brain_policy_reference_proxy_NOT_INTEGRATED",brain_policy_proxy,rows)]
    payload={"experiment":"REQ06-PILOT-2026-11-20-v1","corpus_records":len(rows),
      "repository_document_records":sum(r["source_kind"]=="repository_document" for r in rows),
      "synthetic_control_records":sum(r["source_kind"]=="synthetic_control" for r in rows),
      "tasks":len(TASKS),"positive_tasks":sum(bool(t["relevant"]) for t in TASKS),"negative_abstention_tasks":1,
      "top_k":TOP_K,"seed":"not_applicable_deterministic_no_sampling",
      "corpus_sha256":hashlib.sha256(CORPUS.read_bytes()).hexdigest(),"arms":arms,
      "limitations":["Repository-document pilot corpus; not representative real-user task traces.",
        "Queries and relevance labels are hand-authored from source documents.",
        "Brain arm is a local policy-shaped reference proxy, not the integrated Brain runtime.",
        "Lexical overlap is not semantic retrieval; no model calls or production tokenizer.",
        "Latency is local Python function time only; not service or end-to-end latency.",
        "Seven tasks yield wide uncertainty intervals; no statistical superiority claim."]}
    print(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True) if args.json else summary(payload))

def summary(p):
    out=[f"experiment={p['experiment']} corpus={p['corpus_records']} (repo={p['repository_document_records']}, controls={p['synthetic_control_records']}) tasks={p['tasks']} top_k={p['top_k']}"]
    for a in p["arms"]:
        out.append(f"{a['arm']}: success={a['task_success_rate']} Wilson95={a['task_success_wilson95']} positive_hit={a['positive_task_hit_rate']} recall={a['mean_recall']} precision={a['mean_precision']} MRR={a['mrr_all_tasks']} harmful={a['harmful_activations']} selected={a['selected_count']} median_ms={a['median_local_latency_ms']}")
        for t in a["tasks"]: out.append(f"  {t['task']}: success={t['success']} selected={','.join(t['selected']) or '-'}")
    out.append("LIMIT: Brain arm is proxy only; not integrated runtime or product evidence.")
    return "\n".join(out)

if __name__=="__main__": main()
