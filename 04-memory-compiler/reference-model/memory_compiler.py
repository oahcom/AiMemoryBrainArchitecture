"""Contract-level Memory Compiler reference model; not production infrastructure."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Iterable

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class StageError(ValueError):
    """Fail-closed contract violation."""


def _required(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise StageError(f"MISSING_{field.upper()}")
    return value


def _digest(value: str, field: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise StageError(f"INVALID_{field.upper()}")
    return value


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class SourceMemory:
    memory_id: str
    source_event_id: str
    scope_ref: str
    content: str
    content_digest: str
    derived: bool = False
    parent_memory_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class NormalizedMemory:
    memory_id: str
    scope_ref: str
    normalized_content: str
    normalization_version: str
    source_digest: str


@dataclass(frozen=True)
class ProvenanceRecord:
    derived_memory_id: str
    derivation_id: str
    transformation_id: str
    transformation_version: str
    immediate_source_memory_ids: tuple[str, ...]
    root_source_memory_ids: tuple[str, ...]
    source_event_ids: tuple[str, ...]
    source_digests: tuple[str, ...]
    scope_ref: str
    compiler_contract_version: str
    parameter_digest: str
    parent_derived_memory_ids: tuple[str, ...]


def ingest(event_id: str, scope_ref: str, content: str) -> SourceMemory:
    _required(event_id, "event_id")
    _required(scope_ref, "scope_ref")
    if not isinstance(content, str) or not content:
        raise StageError("MISSING_CONTENT")
    digest = sha256_text(content)
    return SourceMemory(
        memory_id=f"src:{event_id}", source_event_id=event_id,
        scope_ref=scope_ref, content=content, content_digest=digest,
    )


def validate_source(source: SourceMemory) -> SourceMemory:
    _required(source.memory_id, "memory_id")
    _required(source.source_event_id, "source_event_id")
    _required(source.scope_ref, "scope_ref")
    if not source.content:
        raise StageError("MISSING_CONTENT")
    _digest(source.content_digest, "content_digest")
    if sha256_text(source.content) != source.content_digest:
        raise StageError("CONTENT_DIGEST_MISMATCH")
    if source.derived and not source.parent_memory_ids:
        raise StageError("DERIVED_SOURCE_WITHOUT_PARENTS")
    if not source.derived and source.parent_memory_ids:
        raise StageError("ROOT_SOURCE_HAS_PARENTS")
    return source


def normalize(source: SourceMemory, version: str = "normalizer-v1") -> NormalizedMemory:
    validate_source(source)
    _required(version, "normalization_version")
    # Deliberately narrow deterministic transform for the reference model.
    normalized = " ".join(source.content.split())
    return NormalizedMemory(
        memory_id=source.memory_id, scope_ref=source.scope_ref,
        normalized_content=normalized, normalization_version=version,
        source_digest=source.content_digest,
    )


def _canonical_digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256_text(encoded)


def derive(
    inputs: Iterable[NormalizedMemory], transformation_id: str,
    transformation_version: str, parameter_digest: str,
) -> tuple[str, str]:
    ordered = tuple(inputs)
    if not ordered:
        raise StageError("DERIVE_REQUIRES_INPUTS")
    _required(transformation_id, "transformation_id")
    _required(transformation_version, "transformation_version")
    _digest(parameter_digest, "parameter_digest")
    for item in ordered:
        _required(item.memory_id, "source_memory_id")
        _digest(item.source_digest, "source_digest")
    # Stable identity depends on ordered sources, transformation and parameters.
    identity = _canonical_digest({
        "sources": [(x.memory_id, x.source_digest) for x in ordered],
        "transformation_id": transformation_id,
        "transformation_version": transformation_version,
        "parameter_digest": parameter_digest,
    })
    content = "\n".join(x.normalized_content for x in ordered)
    return f"drv:{identity}", content


def resolve_provenance(
    derived_memory_id: str, parents: tuple[str, ...],
    graph: dict[str, SourceMemory],
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    _required(derived_memory_id, "derived_memory_id")
    if not parents:
        raise StageError("PROVENANCE_REQUIRES_PARENTS")

    roots: set[str] = set()
    events: list[str] = []
    digests: list[str] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def walk(memory_id: str) -> None:
        if memory_id in visiting:
            raise StageError("PROVENANCE_CYCLE")
        if memory_id in visited:
            return
        node = graph.get(memory_id)
        if node is None:
            raise StageError("PROVENANCE_MISSING_PARENT")
        validate_source(node)
        visiting.add(memory_id)
        if node.derived:
            for parent_id in node.parent_memory_ids:
                walk(parent_id)
        else:
            roots.add(node.memory_id)
            events.append(node.source_event_id)
            digests.append(node.content_digest)
        visiting.remove(memory_id)
        visited.add(memory_id)

    for parent_id in parents:
        walk(parent_id)
    if not roots:
        raise StageError("PROVENANCE_EMPTY_ROOTS")
    return (
        tuple(sorted(roots)), tuple(events), tuple(digests),
        tuple(parent for parent in parents if graph[parent].derived),
    )


def make_provenance(
    derived_memory_id: str, derivation_id: str, transformation_id: str,
    transformation_version: str, parents: tuple[str, ...],
    graph: dict[str, SourceMemory], scope_ref: str,
    contract_version: str, parameter_digest: str,
) -> ProvenanceRecord:
    _required(derivation_id, "derivation_id")
    _required(transformation_id, "transformation_id")
    _required(transformation_version, "transformation_version")
    _required(scope_ref, "scope_ref")
    _required(contract_version, "compiler_contract_version")
    _digest(parameter_digest, "parameter_digest")
    roots, events, digests, derived_parents = resolve_provenance(
        derived_memory_id, parents, graph
    )
    immediate_digests = tuple(graph[parent].content_digest for parent in parents)
    immediate_events = tuple(graph[parent].source_event_id for parent in parents)
    # Preserve one event/digest anchor per immediate parent; transitive roots
    # are separately represented by root_source_memory_ids.
    return ProvenanceRecord(
        derived_memory_id=derived_memory_id, derivation_id=derivation_id,
        transformation_id=transformation_id,
        transformation_version=transformation_version,
        immediate_source_memory_ids=parents,
        root_source_memory_ids=roots,
        source_event_ids=immediate_events,
        source_digests=immediate_digests,
        scope_ref=scope_ref, compiler_contract_version=contract_version,
        parameter_digest=parameter_digest,
        parent_derived_memory_ids=derived_parents,
    )
