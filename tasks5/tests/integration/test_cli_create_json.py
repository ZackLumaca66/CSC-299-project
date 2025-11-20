import json
import pathlib
from src.cli.main import main


def test_cli_create_json_output(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    rc = main(["--json", "create", "--title", "Write spec"])
    assert rc == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["task"]["title"] == "Write spec"


def test_cli_create_json_invalid_status(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    rc = main(["--json", "create", "--title", "X", "--status", "badvalue"])
    assert rc != 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert "error" in payload
    assert "status" in payload["error"]["message"].lower()