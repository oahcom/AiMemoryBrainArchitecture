#!/usr/bin/env python3
"""Bounded explicit-state Forget protocol model. Run: python3 forget_model.py"""
from collections import deque
from dataclasses import dataclass

@dataclass(frozen=True)
class State:
    fence: bool=False
    epoch: int=0
    durable_epoch: int=0
    forget_ever_happened: bool=False
    admitted: bool=False
    admitted_epoch: int=-1
    published: bool=False
    publish_after_fence: bool=False
    post_fence_admission: bool=False
    index_after_fence: bool=False
    cache_after_fence: bool=False
    barrier_closed: bool=False
    unresolved_work: bool=False
    terminalized: bool=False
    receipt_durable: bool=False
    ack_seen: bool=False
    restore_released: bool=False

ACTIONS=("admit","install_fence","publish","retry_publish","rebuild_index",
         "repopulate_cache","close_barrier","terminalize","persist_receipt",
         "lose_ack","retry_forget","restore")

def step(s, action, mutant=None):
    d=dict(s.__dict__)
    if action=="admit":
        if s.fence and mutant!="admission_race": return None
        d.update(admitted=True, admitted_epoch=s.epoch, post_fence_admission=s.fence)
    elif action=="install_fence":
        d.update(fence=True, epoch=s.epoch+1,
                 durable_epoch=max(s.durable_epoch,s.epoch+1),
                 forget_ever_happened=True,
                 unresolved_work=s.admitted and not s.published)
    elif action in ("publish","retry_publish"):
        if not s.admitted: return None
        if (s.fence or s.admitted_epoch!=s.epoch) and mutant!="stale_worker": return None
        d.update(published=True,publish_after_fence=s.fence,unresolved_work=False)
    elif action=="rebuild_index":
        if not s.published or (s.fence and mutant!="stale_index"): return None
        d["index_after_fence"]=s.fence
    elif action=="repopulate_cache":
        if not s.published or (s.fence and mutant!="stale_cache"): return None
        d["cache_after_fence"]=s.fence
    elif action=="close_barrier":
        if not s.fence or s.unresolved_work: return None
        d["barrier_closed"]=True
    elif action=="terminalize":
        if not s.barrier_closed: return None
        d["terminalized"]=True
    elif action=="persist_receipt":
        if not s.terminalized: return None
        d["receipt_durable"]=True
    elif action=="lose_ack":
        if not s.receipt_durable: return None
        d["ack_seen"]=False
    elif action=="retry_forget":
        pass # same key+digest is idempotent; no durable state rollback
    elif action=="restore":
        if mutant=="stale_restore":
            d.update(fence=False,epoch=0,durable_epoch=0,published=True,restore_released=True)
        else:
            d.update(epoch=max(s.epoch,s.durable_epoch),
                     fence=s.fence or s.durable_epoch>0,restore_released=True)
    else: raise ValueError(action)
    return State(**d)

def violates(s, mutant):
    if mutant is None:
        return (s.fence and (s.publish_after_fence or s.post_fence_admission or
                s.index_after_fence or s.cache_after_fence)) or (
                s.forget_ever_happened and s.restore_released and not s.fence)
    if mutant=="stale_worker": return s.fence and s.publish_after_fence
    if mutant=="admission_race": return s.fence and s.post_fence_admission
    if mutant=="stale_index": return s.fence and s.index_after_fence
    if mutant=="stale_cache": return s.fence and s.cache_after_fence
    if mutant=="stale_restore":
        return s.forget_ever_happened and s.restore_released and not s.fence and s.published
    return False

def shortest_counterexample(mutant=None, max_depth=10):
    q=deque([(State(),[])])
    seen={(State(),0)}
    while q:
        s,trace=q.popleft()
        if violates(s,mutant): return trace,s
        if len(trace)>=max_depth: continue
        for a in ACTIONS:
            n=step(s,a,mutant)
            if n is None: continue
            k=(n,len(trace)+1)
            if k not in seen:
                seen.add(k); q.append((n,trace+[a]))
    return None,None

def count_safe_states(max_depth=10):
    q=deque([(State(),0)])
    seen={(State(),0)}
    while q:
        s,depth=q.popleft()
        if depth>=max_depth: continue
        for a in ACTIONS:
            n=step(s,a)
            if n is not None and (n,depth+1) not in seen:
                seen.add((n,depth+1)); q.append((n,depth+1))
    return len(seen)

def run():
    assert shortest_counterexample(None,10)[0] is None
    print(f"SAFE MODEL: no counterexample through depth 10 ({count_safe_states()} state/depth pairs)")
    expected={
      "stale_worker":["admit","install_fence","publish"],
      "admission_race":["install_fence","admit"],
      "stale_index":["admit","publish","install_fence","rebuild_index"],
      "stale_cache":["admit","publish","install_fence","repopulate_cache"],
      "stale_restore":["install_fence","restore"]}
    for mutant,want in expected.items():
        got,_=shortest_counterexample(mutant,8)
        assert got==want,(mutant,got,want)
        print("COUNTEREXAMPLE "+mutant+": "+" -> ".join(got))
    # Lost ACK is epistemic only: durable receipt and terminal state remain.
    s=State(fence=True,epoch=1,durable_epoch=1,forget_ever_happened=True,
            barrier_closed=True,terminalized=True,receipt_durable=True)
    n=step(step(s,"lose_ack"),"retry_forget")
    assert n.receipt_durable and n.terminalized and n.epoch==1
    print("ACK-LOSS RETRY: durable receipt and terminal state remain monotonic")
    print("MODEL CHECK COMPLETE (bounded abstraction only)")

if __name__=="__main__": run()
