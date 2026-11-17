#!/usr/bin/env python3
"""Synthetic Memory Resource Manager comparison; not production workload evidence."""
import random, time, statistics
SEED=20261118
N_TASKS=30
CANDS_PER_TASK=24
GLOBAL_BUDGET=9000
TASK_CAP=650

def generate():
    random.seed(SEED)
    tasks={}; all_candidates=[]
    for t in range(N_TASKS):
        cs=[]
        for i in range(CANDS_PER_TASK):
            required=i<4
            c={"id":f"m{t}_{i}","task":t,"required":required,
               "relevance":random.uniform(.78,.99) if required else random.uniform(.35,.95),
               "authority":random.uniform(.65,1) if required else random.uniform(.25,.95),
               "freshness":random.uniform(.7,1) if required else random.uniform(.25,1),
               "evidence":random.uniform(.7,1) if required else random.uniform(.2,1),
               "value":random.uniform(.8,1) if required else random.uniform(.1,.8),
               "cost":random.randint(25,110),"topic":f"topic_{t}_{random.randint(0,5)}",
               "allowed":random.random()>.04,"forgotten":random.random()<.015}
            c["rerank"]=(.35*c["relevance"]+.20*c["authority"]+
                         .15*c["freshness"]+.15*c["evidence"]+.15*c["value"])
            cs.append(c); all_candidates.append(c)
        tasks[t]=cs
    return tasks,all_candidates

def topk(tasks):
    d=[]
    for cs in tasks.values():
        valid=[c for c in cs if c["allowed"] and not c["forgotten"]]
        d.extend(sorted(valid,key=lambda c:c["relevance"],reverse=True)[:6])
    d.sort(key=lambda c:c["relevance"],reverse=True)
    selected=[]; used=0
    for c in d:
        if used+c["cost"]<=GLOBAL_BUDGET:
            selected.append(c); used+=c["cost"]
    return selected

def rerank_budget(tasks,all_candidates):
    valid=[c for c in all_candidates if c["allowed"] and not c["forgotten"]]
    ranked=sorted(valid,key=lambda c:c["rerank"]/c["cost"],reverse=True)
    selected=[]; used=0
    for c in ranked:
        if used+c["cost"]<=GLOBAL_BUDGET:
            selected.append(c); used+=c["cost"]
    return selected

def unified_rm(tasks):
    by_task={t:sorted([c for c in tasks[t] if c["allowed"] and not c["forgotten"]],
                      key=lambda c:c["rerank"]/c["cost"],reverse=True) for t in tasks}
    selected=[]; selected_ids=set(); spent={t:0 for t in tasks}; used=0
    floor=GLOBAL_BUDGET//N_TASKS
    for t in range(N_TASKS):
        for c in by_task[t]:
            if spent[t]+c["cost"]<=floor and used+c["cost"]<=GLOBAL_BUDGET:
                selected.append(c); selected_ids.add(c["id"])
                spent[t]+=c["cost"]; used+=c["cost"]
    remaining=set(tasks)
    while remaining and used<GLOBAL_BUDGET:
        progressed=False
        for t in sorted(remaining,key=lambda x:spent[x]/TASK_CAP):
            c=next((x for x in by_task[t] if x["id"] not in selected_ids
                    and spent[t]+x["cost"]<=TASK_CAP
                    and used+x["cost"]<=GLOBAL_BUDGET),None)
            if c:
                selected.append(c); selected_ids.add(c["id"])
                spent[t]+=c["cost"]; used+=c["cost"]; progressed=True
            if used>=GLOBAL_BUDGET: break
        remaining={t for t in remaining if any(x["id"] not in selected_ids
                    and spent[t]+x["cost"]<=TASK_CAP for x in by_task[t])}
        if not progressed: break
    return selected

def measure(selected,latency_ms):
    tokens=sum(c["cost"] for c in selected)
    relevant=[c for c in selected if c["required"]]
    coverage=[sum(1 for c in selected if c["task"]==t and c["required"])/4
              for t in range(N_TASKS)]
    task_tokens=[sum(c["cost"] for c in selected if c["task"]==t)
                 for t in range(N_TASKS)]
    counts={}
    for c in selected:
        key=(c["task"],c["topic"]); counts[key]=counts.get(key,0)+1
    redundancy=sum(max(0,n-1) for n in counts.values())/len(selected) if selected else 0
    squares=sum(x*x for x in coverage)
    fairness=sum(coverage)**2/(N_TASKS*squares) if squares else 0
    return {"selected":len(selected),"tokens":tokens,"budget_util":tokens/GLOBAL_BUDGET,
      "recall":len(relevant)/(N_TASKS*4),
      "precision":len(relevant)/len(selected) if selected else 0,
      "token_eff":sum(c["cost"] for c in relevant)/tokens if tokens else 0,
      "redundancy_rate":redundancy,"task_coverage":sum(coverage)/N_TASKS,
      "starved_tasks":sum(1 for x in task_tokens if x==0),
      "fairness_jain_task_coverage":fairness,"latency_ms":latency_ms}

def main():
    tasks,all_candidates=generate()
    methods=[("Direct Top-K",lambda:topk(tasks)),
      ("Rerank + Budget",lambda:rerank_budget(tasks,all_candidates)),
      ("Unified RM",lambda:unified_rm(tasks))]
    print(f"seed={SEED} tasks={N_TASKS} candidates={N_TASKS*CANDS_PER_TASK} "
          f"global_budget={GLOBAL_BUDGET} task_cap={TASK_CAP} runs=100")
    for name,fn in methods:
        samples=[]; last=None
        for _ in range(100):
            start=time.perf_counter(); last=fn()
            samples.append((time.perf_counter()-start)*1000)
        result=measure(last,statistics.median(samples))
        print(name)
        for key,value in result.items():
            print(f"  {key}={value:.4f}" if isinstance(value,float) else f"  {key}={value}")
if __name__=="__main__": main()
