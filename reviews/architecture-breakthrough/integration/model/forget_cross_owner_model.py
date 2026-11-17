#!/usr/bin/env python3
"""Bounded cross-owner Forget model. Python standard library only.

Run:
  python3 forget_cross_owner_model.py
"""
from collections import deque
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class State:
    # D-owned admission and Forget fence namespace
    registered: bool = False
    reg_seq: int = 0
    post_fence_admission: bool = False
    fence: bool = False
    fence_gen: int = 0
    fence_hwm: int = 0
    durable_fence_gen: int = 0

    # E-owned work/attempt lifecycle and dependency registration
    work: str = "ABSENT"
    no_publication_proof: bool = False  # abstract external D/E/Storage durable proof input
    attempt: int = 0
    lease_active: bool = False
    deps_complete: bool = False

    # I-owned authorization namespace and sequencer outcome
    i_decision: str = "NONE"  # NONE, COMMIT_WON, UNKNOWN, REVOCATION_WON, NO_PUBLICATION
    i_participant_open: bool = False
    i_commit_epoch: int = -1
    permission_epoch: int = 0  # I-local only; never compared with D counters
    revoked: bool = False
    revocation_pending: bool = False

    # Storage visibility and downstream projections
    visible: bool = False
    published_fence_gen: int = -1
    published_after_revocation: bool = False
    suppressed: bool = False
    cached: bool = False
    disclosure_after_fence: bool = False

    # I inventory, D barrier, restore and receipt monotonicity
    inventory_complete: bool = True
    barrier_closed: bool = False
    restore_started: bool = False
    restored_fence_gen: int = 0
    restore_released: bool = True
    durable_at_release: int = 0
    restored_at_release: int = 0
    receipt_durable: bool = False
    receipt_ever_durable: bool = False
    ack_observed: bool = False
    core_barrier_ready: bool = False  # scoped D/I-core predicate; NOT I GlobalForget Completed


ACTIONS = (
    "register", "install_fence", "record_no_publication_proof", "run", "stage", "register_dependencies",
    "i_commit", "i_unknown", "revoke", "publish", "resolve_no_publication",
    "expire_lease", "retry", "park_dlq", "suppress", "terminalize",
    "close_barrier", "inventory_gap", "seal_inventory", "cache_fill", "read",
    "restore_backup", "replay_fence_highwater", "reconcile_restore", "release_restore",
    "persist_receipt", "lose_ack", "retry_forget", "mark_core_barrier_ready",
)


def step(s: State, action: str, mutant: str | None = None):
    d = dict(s.__dict__)

    if action == "register":
        if s.registered or (s.fence and mutant != "post_fence_admission"):
            return None
        d.update(registered=True, reg_seq=s.reg_seq + 1,
                 post_fence_admission=s.fence, work="REGISTERED")

    elif action == "install_fence":
        if s.fence:
            return None
        d.update(fence=True, fence_gen=s.fence_gen + 1,
                 durable_fence_gen=max(s.durable_fence_gen, s.fence_gen + 1),
                 fence_hwm=s.reg_seq, barrier_closed=False)

    elif action == "record_no_publication_proof":
        # External authority input: D/E/Storage must define the durable proof contract.
        # Never infer cancellation merely from the absence of a Worker run.
        if (not s.fence or not s.registered or s.work != "REGISTERED" or
                s.lease_active or s.i_participant_open or s.visible):
            return None
        d.update(work="NO_PUBLICATION_PROVEN", no_publication_proof=True)

    elif action == "run":
        if not s.registered or s.work not in ("REGISTERED", "RETRY"):
            if not (mutant == "stale_worker_after_cancel" and s.work == "NO_PUBLICATION_PROVEN"):
                return None
        d.update(work="RUNNING", lease_active=True)

    elif action == "stage":
        if s.work != "RUNNING" or not s.lease_active:
            return None
        d.update(work="STAGED")

    elif action == "register_dependencies":
        if s.work != "STAGED":
            return None
        d.update(deps_complete=True)

    elif action == "i_commit":
        # I's sequencer result is independent from D's final visibility gate.
        if s.work != "STAGED" or s.i_decision not in ("NONE", "UNKNOWN"):
            return None
        if s.revoked:
            d.update(i_decision="REVOCATION_WON", i_participant_open=False)
        else:
            d.update(i_decision="COMMIT_WON", i_participant_open=True,
                     i_commit_epoch=s.permission_epoch)

    elif action == "i_unknown":
        if s.work != "STAGED" or s.i_decision != "NONE":
            return None
        d.update(i_decision="UNKNOWN", i_participant_open=True)

    elif action == "revoke":
        if s.revoked or s.revocation_pending:
            return None
        if s.i_participant_open:
            # COMMIT_WON/UNKNOWN participant must be resolved before revocation closes.
            d.update(revocation_pending=True)
        else:
            d.update(revoked=True, permission_epoch=s.permission_epoch + 1,
                     i_decision="REVOCATION_WON")

    elif action == "publish":
        if s.work != "STAGED":
            return None
        if not s.deps_complete and mutant != "missing_dependencies":
            return None
        if s.i_decision != "COMMIT_WON" and not (
            mutant == "stale_permission" and s.i_decision == "REVOCATION_WON"
        ):
            return None
        if s.fence and mutant != "stale_publication":
            return None
        if (s.revoked or s.i_commit_epoch != s.permission_epoch) and mutant != "stale_permission":
            return None
        d.update(visible=True, work="PUBLISHED", published_fence_gen=s.fence_gen,
                 i_participant_open=False, lease_active=False)
        if s.revocation_pending:
            d.update(revoked=True, permission_epoch=s.permission_epoch + 1,
                     revocation_pending=False)

    elif action == "resolve_no_publication":
        if not s.i_participant_open or s.i_decision not in ("COMMIT_WON", "UNKNOWN"):
            return None
        d.update(i_participant_open=False, i_decision="NO_PUBLICATION")
        if s.revocation_pending:
            d.update(revoked=True, permission_epoch=s.permission_epoch + 1,
                     revocation_pending=False)

    elif action == "expire_lease":
        if not s.lease_active or s.work in ("PUBLISHED", "TERMINAL"):
            return None
        d.update(lease_active=False, work="RETRY")

    elif action == "retry":
        if s.work not in ("RETRY", "DLQ"):
            return None
        d.update(work="RUNNING", lease_active=True, attempt=s.attempt + 1)

    elif action == "park_dlq":
        if s.work not in ("RETRY", "RUNNING"):
            return None
        d.update(work="DLQ", lease_active=False)

    elif action == "suppress":
        if not s.fence or not s.visible:
            return None
        d.update(suppressed=True, cached=False)

    elif action == "terminalize":
        if mutant == "cancel_without_proof":
            if (not s.fence or not s.registered or s.work != "REGISTERED" or
                    s.lease_active or s.i_participant_open or s.visible):
                return None
            d.update(work="TERMINAL")
        elif mutant == "unknown_terminalization":
            if (not s.registered or s.work == "TERMINAL" or s.lease_active or
                    not s.i_participant_open or s.i_decision != "UNKNOWN"):
                return None
            if s.visible and not s.suppressed:
                return None
            d.update(work="TERMINAL")
        else:
            if (not s.registered or s.work == "TERMINAL" or s.lease_active or
                    s.i_participant_open):
                return None
            if s.visible and not s.suppressed:
                return None
            if (not s.visible and s.i_decision not in ("NO_PUBLICATION", "REVOCATION_WON")
                    and not s.no_publication_proof):
                return None
            d.update(work="TERMINAL")

    elif action == "close_barrier":
        if not s.fence or s.barrier_closed:
            return None
        if not s.inventory_complete and mutant != "inventory_barrier":
            return None
        if s.i_participant_open and mutant != "unknown_terminalization":
            return None
        if s.registered and s.work != "TERMINAL":
            if mutant != "dlq_barrier" or s.work != "DLQ":
                return None
        if s.fence_hwm < s.reg_seq:
            return None
        d.update(barrier_closed=True)

    elif action == "inventory_gap":
        if not s.inventory_complete:
            return None
        # A newly discovered inventory gap invalidates and reopens a prior barrier proof.
        d.update(inventory_complete=False, core_barrier_ready=False, barrier_closed=False)

    elif action == "seal_inventory":
        if s.inventory_complete:
            return None
        d.update(inventory_complete=True)

    elif action == "cache_fill":
        if not s.visible or (s.fence and mutant not in ("stale_cache", "stale_cache_disclosure")):
            return None
        d.update(cached=True)

    elif action == "read":
        if mutant == "stale_cache_disclosure" and not s.cached:
            return None
        if not (s.visible or s.cached):
            return None
        if (s.fence or s.revoked) and mutant not in ("stale_read", "stale_cache_disclosure"):
            return None
        d.update(disclosure_after_fence=s.disclosure_after_fence or s.fence or s.revoked)

    elif action == "restore_backup":
        if s.restore_started:
            return None
        d.update(restore_started=True, restore_released=False, restored_fence_gen=0)

    elif action == "replay_fence_highwater":
        if not s.restore_started or s.restore_released:
            return None
        d.update(restored_fence_gen=s.durable_fence_gen)

    elif action == "reconcile_restore":
        if not s.restore_started or s.restore_released:
            return None
        if s.restored_fence_gen >= s.durable_fence_gen:
            d.update(restore_released=True, durable_at_release=s.durable_fence_gen,
                     restored_at_release=s.restored_fence_gen)

    elif action == "release_restore":
        if not s.restore_started or s.restore_released:
            return None
        if mutant == "stale_restore" or s.restored_fence_gen >= s.durable_fence_gen:
            d.update(restore_released=True, durable_at_release=s.durable_fence_gen,
                     restored_at_release=s.restored_fence_gen)

    elif action == "persist_receipt":
        if not s.barrier_closed or s.receipt_durable:
            return None
        d.update(receipt_durable=True, receipt_ever_durable=True, ack_observed=True)

    elif action == "lose_ack":
        if not s.receipt_durable:
            return None
        if mutant == "ack_loss_rollback":
            d.update(receipt_durable=False, ack_observed=False)
        else:
            d.update(ack_observed=False)

    elif action == "retry_forget":
        if not s.receipt_ever_durable:
            return None
        # Same operation key + normalized digest; return the original durable receipt.
        d.update(receipt_durable=True, ack_observed=True)

    elif action == "mark_core_barrier_ready":
        if (not s.fence or not s.barrier_closed or not s.inventory_complete or
                s.i_participant_open):
            return None
        d.update(core_barrier_ready=True)

    else:
        raise ValueError(action)

    n = State(**d)
    if action == "publish":
        n = replace(n, published_after_revocation=(s.revoked or s.i_decision == "REVOCATION_WON"))
    return n


def invariant_violations(s: State):
    bad = []
    if s.post_fence_admission:
        bad.append("post-fence-admission")
    if s.fence and s.visible and s.published_fence_gen >= s.fence_gen:
        bad.append("visible-after-fence")
    if s.visible and not s.deps_complete:
        bad.append("visible-without-dependencies")
    if s.published_after_revocation:
        bad.append("visible-after-revocation-won")
    if s.disclosure_after_fence:
        bad.append("read-after-fence-or-revocation")
    if s.barrier_closed and (
        not s.inventory_complete or s.i_participant_open or
        (s.registered and s.work != "TERMINAL")
    ):
        bad.append("premature-barrier-close")
    if s.core_barrier_ready and (
        not s.inventory_complete or not s.barrier_closed or s.i_participant_open
    ):
        bad.append("false-core-barrier-ready")
    if (s.registered and s.work == "TERMINAL" and not s.visible and
            s.i_decision == "NONE" and not s.no_publication_proof):
        bad.append("terminal-without-authoritative-no-publication-proof")
    if s.no_publication_proof and s.work in ("RUNNING", "STAGED", "PUBLISHED"):
        bad.append("stale-worker-after-cancel-proof")
    if s.restore_started and s.restore_released and s.restored_at_release < s.durable_at_release:
        bad.append("stale-restore-release")
    if s.receipt_ever_durable and not s.receipt_durable:
        bad.append("durable-receipt-rollback")
    return bad


def bfs(mutant=None, max_depth=14):
    q = deque([(State(), [])])
    seen = {(State(), 0)}
    while q:
        s, trace = q.popleft()
        bad = invariant_violations(s)
        if bad:
            return trace, bad, s, len(seen)
        if len(trace) >= max_depth:
            continue
        for action in ACTIONS:
            nxt = step(s, action, mutant)
            if nxt is None:
                continue
            key = (nxt, len(trace) + 1)
            if key not in seen:
                seen.add(key)
                q.append((nxt, trace + [action]))
    return None, None, None, len(seen)


EXPECTED_COUNTEREXAMPLES = {
    "post_fence_admission": ["install_fence", "register"],
    "stale_publication": ["register", "install_fence", "run", "stage",
                          "register_dependencies", "i_commit", "publish"],
    "missing_dependencies": ["register", "run", "stage", "i_commit", "publish"],
    "stale_permission": ["register", "run", "stage", "register_dependencies",
                         "revoke", "publish"],
    "stale_read": ["register", "run", "stage", "register_dependencies",
                   "i_commit", "revoke", "publish", "read"],
    "stale_cache_disclosure": ["register", "run", "stage", "register_dependencies",
                               "i_commit", "revoke", "publish", "cache_fill", "read"],
    "stale_restore": ["install_fence", "restore_backup", "release_restore"],
    "dlq_barrier": ["register", "install_fence", "run", "park_dlq", "close_barrier"],
    "unknown_terminalization": ["register", "install_fence", "run", "stage",
                                "i_unknown", "expire_lease", "terminalize", "close_barrier"],
    "inventory_barrier": ["install_fence", "inventory_gap", "close_barrier"],
    "ack_loss_rollback": ["install_fence", "close_barrier", "persist_receipt", "lose_ack"],
    "cancel_without_proof": ["register", "install_fence", "terminalize"],
    "stale_worker_after_cancel": ["register", "install_fence", "record_no_publication_proof", "run"],
}


def apply_actions(state, *actions):
    for action in actions:
        state = step(state, action)
        if state is None:
            raise AssertionError(f"illegal safe transition: {action}")
    return state


def run_checks():
    trace, bad, _, count = bfs(None, 14)
    assert trace is None and bad is None
    assert count == 28383, count

    for mutant, expected in EXPECTED_COUNTEREXAMPLES.items():
        got, violations, _, _ = bfs(mutant, 14)
        assert got == expected, (mutant, got, expected)
        assert violations, mutant

    # Cache bytes alone are not a disclosure: final read gate still blocks them.
    cache_only_trace, cache_only_bad, _, _ = bfs("stale_cache", 14)
    assert cache_only_trace is None and cache_only_bad is None

    # I COMMIT_WON first: revocation is held until this exact participant closes.
    s = apply_actions(State(), "register", "run", "stage",
                      "register_dependencies", "i_commit", "revoke")
    assert s.i_participant_open and s.revocation_pending and not s.revoked
    s = apply_actions(s, "publish")
    assert s.visible and s.revoked and not s.i_participant_open and not s.revocation_pending

    # Revocation first: I records REVOCATION_WON and no publication can follow.
    r = apply_actions(State(), "register", "run", "stage",
                      "register_dependencies", "revoke")
    assert r.i_decision == "REVOCATION_WON" and r.revoked
    assert step(r, "i_commit") is None and step(r, "publish") is None

    # Fence first: I participant resolves NO_PUBLICATION; lease and barrier close explicitly.
    f = apply_actions(State(), "register", "run", "stage",
                      "register_dependencies", "i_commit", "install_fence")
    assert step(f, "publish") is None
    f = apply_actions(f, "resolve_no_publication", "expire_lease",
                      "terminalize", "close_barrier", "persist_receipt",
                      "lose_ack", "retry_forget")
    assert f.receipt_durable and f.ack_observed and f.barrier_closed

    # Publication first: fence captures the work; suppression precedes terminalization.
    p = apply_actions(State(), "register", "run", "stage",
                      "register_dependencies", "i_commit", "publish", "install_fence")
    assert p.visible and not p.barrier_closed
    assert step(p, "terminalize") is None
    p = apply_actions(p, "suppress", "terminalize", "close_barrier")
    assert p.barrier_closed

    # Restore can release only after replaying the current D-local high-water.
    restore = apply_actions(State(), "install_fence", "restore_backup", "replay_fence_highwater", "reconcile_restore")
    assert restore.restore_released and restore.restored_at_release == restore.durable_at_release

    # A registered-but-never-started item needs an explicit external durable proof.
    never_started = apply_actions(State(), "register", "install_fence")
    assert step(never_started, "terminalize") is None
    never_started = apply_actions(never_started, "record_no_publication_proof", "terminalize", "close_barrier")
    assert never_started.barrier_closed

    # The model predicate is intentionally scoped and is not I GlobalForget Completed.
    core = apply_actions(State(), "install_fence", "close_barrier", "mark_core_barrier_ready")
    assert core.core_barrier_ready

    # UNKNOWN is nonterminal and holds the barrier until authoritative resolution.
    u = apply_actions(State(), "register", "run", "stage",
                      "register_dependencies", "i_unknown", "install_fence")
    assert step(u, "close_barrier") is None
    u = apply_actions(u, "resolve_no_publication", "expire_lease",
                      "terminalize", "close_barrier")
    assert u.barrier_closed

    print(f"SAFE MODEL: no invariant violation through depth 14 ({count} state/depth pairs)")
    for mutant, expected in EXPECTED_COUNTEREXAMPLES.items():
        print(f"COUNTEREXAMPLE {mutant}: {' -> '.join(expected)}")
    print("CACHE NEGATIVE CONTROL: stale cache fill alone is not disclosure; final read gate blocks")
    print("SERIAL ORDER / UNKNOWN / PRE-EXECUTION PROOF / ACK-LOSS CHECKS: PASS")
    print("MODEL CHECK COMPLETE (bounded abstraction only)")


if __name__ == "__main__":
    run_checks()
