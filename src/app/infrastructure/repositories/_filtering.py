"""Helpers shared by the in-memory repositories."""

from collections.abc import Iterable


def matches_all(criteria: Iterable[tuple[object | None, object]]) -> bool:
    """True when every `(wanted, actual)` pair matches; a `wanted` of `None` matches anything."""
    return all(wanted is None or wanted == actual for wanted, actual in criteria)
