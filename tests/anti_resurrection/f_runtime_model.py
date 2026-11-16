"""F runtime anti-resurrection logical reference model (not production code)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Set, Tuple


class Blocked(RuntimeError):
    """Protected retrieval cannot be proven safe."""


class Conflict(RuntimeError):
    """An immutable invalidation identity was rebound to changed content."""


@dataclass(frozen=True)
class RuntimeEntry:
    memory_ref: str
    scope_ref: str
    environment_ref: str
    policy_domain_ref: str
    permission_epoch: int
    fence_generation: int
    memory_version: str
    partition: str = "p0"
    score: float = 1.0
    payload: str = "payload"
    lineage: Tuple[str, ...] = ()


@dataclass
class IndexPartition:
    partition: str = "p0"
    watermark: int = 100
    required_watermark: int = 100
    complete: bool = True
    generation: int = 1
    entries: List[RuntimeEntry] = field(default_factory=list)


@dataclass(frozen=True)
class FillIntent:
    fill_id: str
    cache_key: Tuple[object, ...]
    entry: RuntimeEntry
    captured_permission_epoch: int
    captured_fence_generation: int
    captured_index_generation: int


class RuntimeModel:
    """Models current authorization/fence checks at index/cache/working-set boundaries."""

    def __init__(self) -> None:
        self.authorities_available = True
        self.permission_epoch: Dict[str, int] = {"pd-A": 7}
        self.allowed_scopes: Set[str] = {"scope-A"}
        self.allowed_environments: Set[str] = {"env-A"}
        self.fence_generation = 0
        self.blocked_refs: Set[str] = set()
        self.index = IndexPartition()
        self.cache: Dict[Tuple[object, ...], RuntimeEntry] = {}
        self.in_flight: Dict[str, FillIntent] = {}
        self.working_set: List[RuntimeEntry] = []
        self.invalidation_receipts: Dict[str, str] = {}
        self.stale_evictions = 0
        self.last_exposed_count = 0

    @staticmethod
    def cache_key(entry: RuntimeEntry, principal: str = "principal-A",
                  issuer: str = "issuer-A", query_digest: str = "query-A",
                  config_version: str = "cfg-1") -> Tuple[object, ...]:
        # Authorization dimensions are key material, never the authorization decision.
        return (principal, issuer, entry.policy_domain_ref, entry.scope_ref,
                entry.environment_ref, entry.permission_epoch, entry.fence_generation,
                entry.memory_ref, entry.memory_version, entry.partition,
                query_digest, config_version)

    def _blocked(self, entry: RuntimeEntry) -> bool:
        refs = {entry.memory_ref, *entry.lineage}
        return bool(refs.intersection(self.blocked_refs))

    def _authorized(self, entry: RuntimeEntry) -> bool:
        current = self.permission_epoch.get(entry.policy_domain_ref)
        return (current is not None and current == entry.permission_epoch
                and entry.scope_ref in self.allowed_scopes
                and entry.environment_ref in self.allowed_environments)

    def validate(self, entry: RuntimeEntry) -> bool:
        if not self.authorities_available:
            raise Blocked("I/D authoritative state unavailable")
        if self._blocked(entry):
            return False
        if entry.fence_generation != self.fence_generation:
            # A generation mismatch is stale unless a current authoritative lookup
            # proves the target is unaffected. This model chooses fail-closed.
            return False
        return self._authorized(entry)

    def retrieve(self, candidates: Optional[Iterable[RuntimeEntry]] = None,
                 limit: int = 10) -> List[RuntimeEntry]:
        if not self.authorities_available:
            raise Blocked("I/D authoritative state unavailable")
        if not self.index.complete or self.index.watermark < self.index.required_watermark:
            raise Blocked("index watermark/coverage is incomplete")
        source = list(self.index.entries if candidates is None else candidates)
        # Security and Forget filtering precedes ranking, counts and materialization.
        visible = [entry for entry in source if self.validate(entry)]
        visible.sort(key=lambda entry: entry.score, reverse=True)
        self.last_exposed_count = len(visible)
        return visible[:limit]

    def cache_get(self, key: Tuple[object, ...]) -> Optional[RuntimeEntry]:
        if not self.authorities_available:
            raise Blocked("I/D authoritative state unavailable; stale cache is not a miss")
        entry = self.cache.get(key)
        if entry is None:
            return None
        if not self.validate(entry):
            self.cache.pop(key, None)
            self.stale_evictions += 1
            return None
        return entry

    def start_fill(self, fill_id: str, entry: RuntimeEntry) -> None:
        if not self.validate(entry):
            raise Blocked("candidate is not currently authorized/visible")
        intent = FillIntent(fill_id, self.cache_key(entry), entry,
                            self.permission_epoch[entry.policy_domain_ref],
                            self.fence_generation, self.index.generation)
        prior = self.in_flight.get(fill_id)
        if prior is not None and prior != intent:
            raise Conflict("fill identity rebound to changed entry")
        self.in_flight[fill_id] = intent

    def complete_fill(self, fill_id: str) -> bool:
        intent = self.in_flight.pop(fill_id)
        if not self.authorities_available:
            return False
        if (intent.captured_permission_epoch != self.permission_epoch.get(intent.entry.policy_domain_ref)
                or intent.captured_fence_generation != self.fence_generation
                or intent.captured_index_generation != self.index.generation
                or not self.validate(intent.entry)):
            return False
        self.cache[intent.cache_key] = intent.entry
        return True

    def apply_forget(self, operation_id: str, digest: str, refs: Iterable[str]) -> str:
        refs_set = set(refs)
        prior = self.invalidation_receipts.get(operation_id)
        if prior is not None:
            if prior != digest:
                raise Conflict("invalidation operation identity rebound to changed digest")
            return "IDEMPOTENT_REPLAY"
        self.invalidation_receipts[operation_id] = digest
        self.fence_generation += 1
        self.blocked_refs.update(refs_set)
        self.cache = {k: v for k, v in self.cache.items() if not self._blocked(v)}
        self.working_set = [v for v in self.working_set if not self._blocked(v)]
        # In-flight fills are not assumed cancelled; completion must revalidate.
        return "APPLIED"

    def revoke(self, policy_domain_ref: str, new_epoch: int) -> None:
        current = self.permission_epoch[policy_domain_ref]
        if new_epoch <= current:
            raise Conflict("PermissionEpoch must advance monotonically")
        self.permission_epoch[policy_domain_ref] = new_epoch
        self.cache = {k: v for k, v in self.cache.items() if self._authorized(v)}
        self.working_set = [v for v in self.working_set if self._authorized(v)]

    def rebuild(self, snapshot_entries: Iterable[RuntimeEntry], *,
                contiguous_replay: bool, watermark: int, generation: int) -> None:
        self.index.entries = list(snapshot_entries)
        self.index.watermark = watermark
        self.index.generation = generation
        self.index.complete = contiguous_replay
        if not contiguous_replay or watermark < self.index.required_watermark:
            raise Blocked("snapshot + contiguous replay is not complete")

    def reconnect(self, restored_entries: Iterable[RuntimeEntry], *,
                  fresh_i_state: bool, fresh_d_state: bool,
                  checkpoint_reconciled: bool) -> None:
        # Old Working Set is made unreachable before any restored item is considered.
        self.working_set.clear()
        if not self.authorities_available or not fresh_i_state or not fresh_d_state:
            raise Blocked("fresh I/D authority state required before restore")
        if not checkpoint_reconciled:
            raise Blocked("invalidation checkpoint requires snapshot + contiguous replay")
        safe = [entry for entry in restored_entries if self.validate(entry)]
        self.working_set.extend(safe)

    def report_target_evidence(self, target_id: str) -> dict:
        # F reports only its own local target slice; it never confirms I global completion.
        if not self.authorities_available:
            return {"target_id": target_id, "state": "UNKNOWN", "owner": "F"}
        return {"target_id": target_id, "state": "SUPPRESSED" if self.blocked_refs else "LOCAL_CLEAR",
                "owner": "F", "global_completion": "NOT_AUTHORIZED"}