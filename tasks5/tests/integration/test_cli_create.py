import json
import pathlib
from src.cli.main import main


def test_cli_create_persists_task(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    rc = main(["create", "--title", "Write spec"])
    assert rc == 0
    captured = capsys.readouterr()
    assert "Write spec" in captured.out
    data_file = pathlib.Path("tasks.json")
    assert data_file.exists()
    data = json.loads(data_file.read_text())
    assert data["tasks"][0]["title"] == "Write spec"


def test_cli_create_invalid_title(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    rc = main(["create", "--title", "   "])
    assert rc != 0
    captured = capsys.readouterr()
    assert "title" in captured.err.lower()