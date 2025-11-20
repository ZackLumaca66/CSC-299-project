import json
from src.cli.main import main
import pathlib


def create(title, status=None):
    args = ["--json", "create", "--title", title]
    if status:
        args += ["--status", status]
    rc = main(args)
    assert rc == 0


def test_cli_list_json(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    create("A")
    create("B", "done")
    capsys.readouterr()  # clear create outputs
    rc = main(["--json", "list"])  # list all json
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    titles = {t["title"] for t in data["tasks"]}
    assert {"A", "B"} <= titles


def test_cli_list_json_filter_status(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    create("A")
    create("B", "done")
    capsys.readouterr()  # clear create outputs
    rc = main(["--json", "list", "--status", "done"])  # filter
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    titles = {t["title"] for t in data["tasks"]}
    assert titles == {"B"}


def test_cli_list_json_empty(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    rc = main(["--json", "list"])  # list when empty
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    assert data["tasks"] == []