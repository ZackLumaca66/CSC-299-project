from src.models.task import Task


def filter_status(tasks, status):
    from src.services.filtering import filter_by_status  # local import to trigger failure before implementation
    return filter_by_status(tasks, status)


def test_filter_by_status_matches_only_requested():
    tasks = [
        Task(id=1, title="A", description=None, status="todo"),
        Task(id=2, title="B", description=None, status="done"),
        Task(id=3, title="C", description=None, status="in-progress"),
    ]
    done = filter_status(tasks, "done")
    assert len(done) == 1 and done[0].status == "done"


def test_filter_by_status_invalid_returns_empty():
    tasks = [Task(id=1, title="A", description=None, status="todo")]
    result = filter_status(tasks, "bad")
    assert result == []