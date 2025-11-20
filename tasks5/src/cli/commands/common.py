"""Common CLI command utilities to reduce duplication."""
from __future__ import annotations
import sys
from typing import Iterable

from src.repository.json_repository import JsonTaskRepository
from src.cli.formatting import format_tasks_human, format_tasks_json, format_error_json
from src.models.task import Task


def get_repository() -> JsonTaskRepository:
    return JsonTaskRepository()


def load_tasks() -> list[Task]:
    repo = get_repository()
    return repo.load_all_tasks()


def print_tasks(tasks: Iterable[Task], json_mode: bool) -> None:
    if json_mode:
        print(format_tasks_json(tasks), end="")
    else:
        print(format_tasks_human(tasks))


def print_error(message: str, json_mode: bool) -> None:
    if json_mode:
        print(format_error_json(message), end="")
    else:
        print(message, file=sys.stderr)

__all__ = ["load_tasks", "print_tasks", "print_error", "get_repository"]
