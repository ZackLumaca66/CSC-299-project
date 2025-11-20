"""Search service providing case-insensitive substring matching over tasks."""
from __future__ import annotations

from typing import Iterable, List
from src.models.task import Task


def search_tasks(tasks: Iterable[Task], query: str) -> List[Task]:
    """Return tasks whose title or description contains the substring query (case-insensitive).

    Raises ValueError if query is blank.
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Search query cannot be blank")
    needle = query.lower()
    results: List[Task] = []
    for t in tasks:
        if needle in t.title.lower() or (t.description and needle in t.description.lower()):
            results.append(t)
    return results

__all__ = ["search_tasks"]
