import pytest

from src.models.task import Task
from src.models.status import ALLOWED_STATUSES


def test_create_valid_task():
    t = Task(id=1, title="Write spec", description="Initial", status="todo")
    assert t.id == 1
    assert t.title == "Write spec"
    assert t.status == "todo"


@pytest.mark.parametrize("bad_title", ["", "   ", None])
def test_create_task_blank_title_raises(bad_title):
    with pytest.raises(ValueError) as exc:
        Task(id=1, title=bad_title, description=None, status="todo")
    assert "title" in str(exc.value).lower()


def test_create_task_bad_status_raises():
    bad = "doing"  # not in allowed
    assert bad not in ALLOWED_STATUSES
    with pytest.raises(ValueError) as exc:
        Task(id=1, title="X", description=None, status=bad)
    assert "status" in str(exc.value).lower()