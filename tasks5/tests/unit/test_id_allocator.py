from src.services.id_allocator import next_id
from src.models.task import Task


def test_next_id_empty():
    assert next_id([]) == 1


def test_next_id_sequence():
    tasks = [Task(id=1, title="A", description=None, status="todo"), Task(id=3, title="B", description=None, status="todo")]
    assert next_id(tasks) == 4