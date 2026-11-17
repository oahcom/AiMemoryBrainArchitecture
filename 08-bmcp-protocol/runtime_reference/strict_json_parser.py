"""Strict JSON envelope parser reference model; not a production BMCP transport."""
import json


class ProtocolParseError(ValueError):
    pass


class DuplicateKeyError(ProtocolParseError):
    pass


class UnknownCriticalExtension(ProtocolParseError):
    pass


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise ProtocolParseError(f"non-finite JSON number is forbidden: {value}")


def _depth(value, limit):
    stack = [(value, 1)]
    while stack:
        node, depth = stack.pop()
        if depth > limit:
            raise ProtocolParseError(f"JSON nesting exceeds configured limit {limit}")
        if isinstance(node, dict):
            stack.extend((v, depth + 1) for v in node.values())
        elif isinstance(node, list):
            stack.extend((v, depth + 1) for v in node)


def parse_strict_json(raw, *, max_bytes=262144, max_depth=32):
    if isinstance(raw, str):
        encoded = raw.encode("utf-8", errors="strict")
    elif isinstance(raw, bytes):
        encoded = raw
    else:
        raise ProtocolParseError("message must be UTF-8 bytes or text")
    if len(encoded) > max_bytes:
        raise ProtocolParseError("message exceeds configured byte limit")
    try:
        decoded = encoded.decode("utf-8", errors="strict")
        value = json.loads(decoded, object_pairs_hook=_unique_object,
                           parse_constant=_reject_constant)
    except ProtocolParseError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProtocolParseError(f"invalid UTF-8 JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ProtocolParseError("BMCP message root must be a JSON object")
    _depth(value, max_depth)
    return value


def validate_critical_extensions(message, *, known_fields, known_extensions=()):
    critical = message.get("critical_extensions", [])
    if not isinstance(critical, list) or any(not isinstance(x, str) or not x for x in critical):
        raise ProtocolParseError("critical_extensions must be an array of non-empty strings")
    if len(set(critical)) != len(critical):
        raise ProtocolParseError("critical_extensions contains duplicate names")
    supported = set(known_extensions)
    unknown = [name for name in critical if name not in supported and name not in known_fields]
    if unknown:
        raise UnknownCriticalExtension("unsupported critical extension(s): " + ", ".join(sorted(unknown)))
    # Unknown non-critical fields are preserved as opaque data; they are never interpreted.
    return {k: v for k, v in message.items()
            if k not in known_fields and k != "critical_extensions"}