import json
from src.cli.main import main
import pathlib


def create(title, status=None):
    args = ["create", "--title", title]
    if status:
        args += ["--status", status]
    rc = main(args)
    assert rc == 0


def test_cli_list_shows_tasks(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    create("A")
    create("B", "done")
    rc = main(["list"])  # list all
    assert rc == 0
    captured = capsys.readouterr()
    out = captured.out
    assert "A" in out and "B" in out


def test_cli_list_filter_status(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    create("A")
    create("B", "done")
    capsys.readouterr()  # clear buffer after creations
    rc = main(["list", "--status", "done"])
    assert rc == 0
    out = capsys.readouterr().out
    # Expect only filtered task(s)
    assert "B" in out
    assert "A" not in out


def test_cli_list_empty_store_message(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    rc = main(["list"])  # nothing created
    assert rc == 0
    out = capsys.readouterr().out
    assert "No tasks" in out