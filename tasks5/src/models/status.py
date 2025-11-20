"""Status definitions for tasks.

Defines allowed statuses as simple constants to avoid enum overhead.
"""

ALLOWED_STATUSES = ("todo", "in-progress", "done")

def is_valid_status(value: str) -> bool:
    return isinstance(value, str) and value in ALLOWED_STATUSES