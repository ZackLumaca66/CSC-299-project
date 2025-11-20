"""Formatting helpers for human and JSON outputs."""
from __future__ import annotations
import json
from typing import Iterable

from src.models.task import Task


def format_tasks_human(tasks: Iterable[Task]) -> str:
    if not tasks:
        return "No tasks"
    lines = []
    for t in tasks:
        desc = f" - {t.description}" if t.description else ""
        lines.append(f"[{t.id}] {t.title} ({t.status}){desc}")
    return "\n".join(lines)


def format_tasks_json(tasks: Iterable[Task]) -> str:
    payload = {
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "status": t.status,
            }
            for t in tasks
        ]
    }
    return json.dumps(payload)


def format_error_json(message: str, error_type: str = "error") -> str:
    return json.dumps({"error": {"type": error_type, "message": message}})