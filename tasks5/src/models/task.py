"""Task model with basic validation per constitution guidelines."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from .status import is_valid_status, ALLOWED_STATUSES


@dataclass(frozen=True, slots=True)
class Task:
    id: int
    title: str
    description: Optional[str]
    status: str

    def __post_init__(self):  # type: ignore[override]
        # Basic id check
        if not isinstance(self.id, int) or self.id < 1:
            raise ValueError("Task id must be positive integer")
        # Title validation
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Task title cannot be blank")
        # Status validation
        if not is_valid_status(self.status):
            raise ValueError(f"Invalid status '{self.status}'. Allowed: {', '.join(ALLOWED_STATUSES)}")