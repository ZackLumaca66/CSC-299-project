"""Create command implementation."""
from __future__ import annotations
import sys
import argparse
from typing import List

from src.repository.json_repository import JsonTaskRepository
from src.services.id_allocator import next_id
from src.models.task import Task
from src.models.status import ALLOWED_STATUSES, is_valid_status
from .common import print_error


def build_parser(subparsers) -> argparse.ArgumentParser:
    p = subparsers.add_parser("create", help="Create a new task")
    p.add_argument("--title", required=True, help="Task title (required)")
    p.add_argument("--description", required=False, help="Optional description")
    p.add_argument("--status", required=False, help="Optional status")
    return p


def run(args: argparse.Namespace, json_mode: bool) -> int:
    title = args.title
    description = args.description
    status = args.status or "todo"

    if not isinstance(title, str) or not title.strip():
        print_error("Title cannot be blank", json_mode)
        return 1

    if not is_valid_status(status):
        print_error(f"Invalid status '{status}'. Allowed: {', '.join(ALLOWED_STATUSES)}", json_mode)
        return 1

    repo = JsonTaskRepository()
    existing = repo.load_all_tasks()
    new_id = next_id(existing)
    task = Task(id=new_id, title=title.strip(), description=description, status=status)
    repo.save_new_task(task)

    if json_mode:
        import json as _json
        print(_json.dumps({"task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
        }}), end="")
    else:
        desc = f" - {task.description}" if task.description else ""
        print(f"Created [{task.id}] {task.title} ({task.status}){desc}")
    return 0