"""Offline GraphQL fixtures for merge-group candidate tests."""

from __future__ import annotations

import copy


BASE_SHA = "b" * 40
CANDIDATE_SHA = "c" * 40
HEAD_1 = "1" * 40
HEAD_2 = "2" * 40
HEAD_3 = "3" * 40


def entry(position, number, head_sha, candidate_sha=None):
    return {
        "position": position,
        "pullRequest": {
            "number": number,
            "headRefOid": head_sha,
        },
        "headCommit": {
            "oid": candidate_sha or head_sha,
        },
    }


def graphql_page(nodes, has_next=False, cursor=None):
    """Return the data object consumed by candidate._graphql()."""
    return {
        "repository": {
            "mergeQueue": {
                "entries": {
                    "nodes": copy.deepcopy(nodes),
                    "pageInfo": {
                        "hasNextPage": has_next,
                        "endCursor": cursor,
                    },
                }
            }
        }
    }


def two_page_graphql_sequence():
    first = [entry(1, 101, HEAD_1)]
    second = [entry(2, 102, HEAD_2)]
    return [
        graphql_page(first, True, "cursor-1"),
        graphql_page(second, False, None),
        graphql_page(first, True, "cursor-1"),
        graphql_page(second, False, None),
    ]


def one_page_graphql_sequence(nodes, has_next=False, cursor=None):
    page = graphql_page(nodes, has_next, cursor)
    return [copy.deepcopy(page), copy.deepcopy(page)]


def valid_prefix():
    return [
        entry(1, 101, HEAD_1),
        entry(2, 102, HEAD_2),
        entry(3, 103, HEAD_3),
    ]


def compare_response(ancestor, behind_by=0, merge_base_sha=None):
    return {
        "behind_by": behind_by,
        "merge_base_commit": {
            "sha": merge_base_sha or ancestor,
        },
    }


def member(number, body, position=None, head_sha=HEAD_1):
    return {
        "position": position if position is not None else number - 100,
        "number": number,
        "head_sha": head_sha,
        "body": body,
    }
