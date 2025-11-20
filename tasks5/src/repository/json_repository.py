"""JSON repository handling persistence with atomic writes & backup on corruption."""
from __future__ import annotations
import json
import pathlib
import time
from typing import List

from .schema import SCHEMA_VERSION, base_document
from .errors import CorruptDataError, AtomicWriteError
from src.models.task import Task


class JsonTaskRepository:
    def __init__(self, path: pathlib.Path | str = pathlib.Path("tasks.json")) -> None:
        self.path = pathlib.Path(path)

    def _ensure_loaded(self) -> dict:
        if not self.path.exists():
            doc = base_document()
            self._write_atomic(doc)
            return doc
        raw = self.path.read_text(encoding="utf-8")
        try:
            data = json.loads(raw)
            if "schema_version" not in data or "tasks" not in data:
                raise ValueError("Missing required keys")
            return data
        except Exception:
            # Backup corrupt file named original.json.bak-<timestamp>
            backup = self.path.parent / f"{self.path.name}.bak-{int(time.time())}"
            try:
                self.path.rename(backup)
            except Exception:
                backup = None  # ignore backup failure
            doc = base_document()
            self._write_atomic(doc)
            raise CorruptDataError(f"Corrupt JSON file backed up to {backup}")

    def load_all_tasks(self) -> List[Task]:
        try:
            data = self._ensure_loaded()
        except CorruptDataError:
            # After corruption reset we return empty list
            return []
        tasks = []
        for item in data.get("tasks", []):
            try:
                tasks.append(Task(**item))
            except Exception:
                # Skip invalid entries silently; could log
                continue
        return tasks

    def save_new_task(self, task: Task) -> None:
        try:
            data = self._ensure_loaded()
        except CorruptDataError:
            data = base_document()
        data_tasks = data.get("tasks", [])
        data_tasks.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
        })
        data["tasks"] = data_tasks
        data["schema_version"] = SCHEMA_VERSION
        self._write_atomic(data)

    def _write_atomic(self, data: dict) -> None:
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        try:
            tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            tmp.replace(self.path)
        except Exception as e:  # pragma: no cover - rare failure path
            raise AtomicWriteError(f"Atomic write failed: {e}")