"""Filtering services for tasks."""
from __future__ import annotations
from typing import Iterable, List

from src.models.task import Task
from src.models.status import ALLOWED_STATUSES


def filter_by_status(tasks: Iterable[Task], status: str | None) -> List[Task]:
    if status is None:
        return list(tasks)
    if status not in ALLOWED_STATUSES:
        return []
    return [t for t in tasks if t.status == status]