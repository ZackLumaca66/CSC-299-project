"""ID allocation service separate from repository for testability."""
from __future__ import annotations
from typing import Iterable

from src.models.task import Task


def next_id(existing: Iterable[Task]) -> int:
    max_id = 0
    for t in existing:
        if t.id > max_id:
            max_id = t.id
    return max_id + 1