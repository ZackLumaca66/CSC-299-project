from src.cli.formatting import (
    format_tasks_human,
    format_tasks_json,
    format_error_json,
)
from src.models.task import Task


def test_format_tasks_human_empty():
    assert format_tasks_human([]) == "No tasks"


def test_format_tasks_human_non_empty():
    tasks = [Task(id=1, title="A", description=None, status="todo"), Task(id=2, title="B", description="Desc", status="done")]
    out = format_tasks_human(tasks)
    assert "[1] A (todo)" in out
    assert "[2] B (done) - Desc" in out


def test_format_tasks_json():
    tasks = [Task(id=1, title="A", description=None, status="todo")]
    js = format_tasks_json(tasks)
    assert '"tasks"' in js
    assert '"A"' in js


def test_format_error_json():
    err = format_error_json("Bad", "validation")
    assert '"error"' in err and '"validation"' in err and '"Bad"' in err