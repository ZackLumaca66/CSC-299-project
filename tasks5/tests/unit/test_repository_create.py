import json
import pathlib
import pytest
import time

from src.repository.json_repository import JsonTaskRepository
from src.models.task import Task


def test_repository_creates_file_and_persists_task(tmp_path):
    data_file = tmp_path / "tasks.json"
    repo = JsonTaskRepository(path=data_file)
    assert not data_file.exists()
    t = Task(id=1, title="Write spec", description=None, status="todo")
    repo.save_new_task(t)
    assert data_file.exists()
    loaded = json.loads(data_file.read_text())
    assert loaded["schema_version"] == 1
    assert loaded["tasks"][0]["title"] == "Write spec"


def test_repository_atomic_write(tmp_path, monkeypatch):
    data_file = tmp_path / "tasks.json"
    repo = JsonTaskRepository(path=data_file)

    wrote_temp = False
    original_write_text = pathlib.Path.write_text

    def tracking_write(self, content, *args, **kwargs):  # noqa: D401
        nonlocal wrote_temp
        if self.name.endswith(".tmp"):
            wrote_temp = True
        return original_write_text(self, content, *args, **kwargs)

    monkeypatch.setattr(pathlib.Path, "write_text", tracking_write)
    repo.save_new_task(Task(id=1, title="A", description=None, status="todo"))
    assert wrote_temp, "Expected atomic temp write before replace"


def test_repository_corrupt_file_backup(tmp_path):
    data_file = tmp_path / "tasks.json"
    data_file.write_text("{ this is not valid json")
    repo = JsonTaskRepository(path=data_file)
    # Loading should trigger backup and reset
    tasks = repo.load_all_tasks()
    assert tasks == []
    backups = list(tmp_path.glob("tasks.json.bak-*"))
    assert backups, "Corrupt file should have been backed up"


def test_repository_load_existing_tasks(tmp_path):
    data_file = tmp_path / "tasks.json"
    data = {"schema_version": 1, "tasks": [
        {"id": 1, "title": "A", "description": None, "status": "todo"},
        {"id": 2, "title": "B", "description": "desc", "status": "in-progress"},
    ]}
    data_file.write_text(json.dumps(data))
    repo = JsonTaskRepository(path=data_file)
    tasks = repo.load_all_tasks()
    assert len(tasks) == 2
    assert tasks[1].status == "in-progress"


def test_repository_skips_invalid_entries(tmp_path):
    data_file = tmp_path / "tasks.json"
    # Second entry invalid (blank title)
    data = {"schema_version": 1, "tasks": [
        {"id": 1, "title": "A", "description": None, "status": "todo"},
        {"id": 2, "title": "", "description": None, "status": "todo"},
    ]}
    data_file.write_text(json.dumps(data))
    repo = JsonTaskRepository(path=data_file)
    tasks = repo.load_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == 1


def test_repository_save_appends_and_preserves_schema_version(tmp_path):
    data_file = tmp_path / "tasks.json"
    repo = JsonTaskRepository(path=data_file)
    repo.save_new_task(Task(id=1, title="A", description=None, status="todo"))
    repo.save_new_task(Task(id=2, title="B", description=None, status="done"))
    data = json.loads(data_file.read_text())
    assert data["schema_version"] == 1
    assert len(data["tasks"]) == 2
    assert data["tasks"][1]["status"] == "done"