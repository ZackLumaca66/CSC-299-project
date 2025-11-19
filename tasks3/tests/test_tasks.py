import os
import json
from tasks3 import list_tasks

def test_list_tasks_empty(tmp_path, monkeypatch):
    # Create a temporary tasks.json and point the module to it
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    file_path = data_dir / "tasks.json"
    file_path.write_text("[]", encoding="utf-8")

    # Monkeypatch the DATA_FILE path used by tasks3
    import tasks3
    monkeypatch.setattr(tasks3, "DATA_FILE", str(file_path))

    tasks = list_tasks()
    assert isinstance(tasks, list)
    assert tasks == []
