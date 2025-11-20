import pytest
from src.models.task import Task

# Import will fail until search service implemented
from src.services.search import search_tasks


def sample_tasks():
    return [
        Task(id=1, title="Write spec", description="Initial MVP", status="todo"),
        Task(id=2, title="Refactor code", description="Improve clarity", status="in-progress"),
        Task(id=3, title="Test Search", description=None, status="done"),
    ]


def test_search_case_insensitive_title():
    tasks = sample_tasks()
    results = search_tasks(tasks, "SPEC")
    assert len(results) == 1 and results[0].title == "Write spec"


def test_search_matches_description_substring():
    tasks = sample_tasks()
    results = search_tasks(tasks, "clar")
    assert len(results) == 1 and results[0].id == 2


def test_search_no_matches():
    tasks = sample_tasks()
    results = search_tasks(tasks, "xyz")
    assert results == []


def test_search_empty_query_raises():
    tasks = sample_tasks()
    with pytest.raises(ValueError):
        search_tasks(tasks, "")
