"""Central validation utilities for tasks."""
from __future__ import annotations

from .status import is_valid_status


def validate_title(title: str) -> None:
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title cannot be blank")


def validate_status(status: str) -> None:
    if not is_valid_status(status):
        raise ValueError("Invalid status")