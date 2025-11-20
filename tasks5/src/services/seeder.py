"""Seeder utility for sample tasks."""
from __future__ import annotations
from typing import Iterable

from src.repository.json_repository import JsonTaskRepository
from src.services.id_allocator import next_id
from src.models.task import Task

SAMPLE_TASKS = [
    ("Write spec", "Initial MVP document", "in-progress"),
    ("Implement create", "CLI create command", "todo"),
    ("Add search", "Implement substring search", "todo"),
]


def seed(repository: JsonTaskRepository | None = None) -> int:
    repo = repository or JsonTaskRepository()
    existing = repo.load_all_tasks()
    current_ids = {t.id for t in existing}
    added = 0
    for title, desc, status in SAMPLE_TASKS:
        new_id = next_id(existing)
        if new_id in current_ids:
            continue
        task = Task(id=new_id, title=title, description=desc, status=status)
        repo.save_new_task(task)
        existing.append(task)
        current_ids.add(new_id)
        added += 1
    return added