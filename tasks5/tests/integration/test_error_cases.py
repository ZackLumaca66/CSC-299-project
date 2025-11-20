import json
from src.cli.main import main


def test_create_blank_title_error(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    rc = main(["create", "--title", " "])  # blank
    assert rc == 1
    err = capsys.readouterr().err
    assert "Title cannot be blank" in err


def test_create_invalid_status_error(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    rc = main(["create", "--title", "Task", "--status", "invalid-status"])  # invalid
    assert rc == 1
    err = capsys.readouterr().err
    assert "Invalid status" in err


def test_search_blank_query_error(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    rc = main(["search", ""])  # blank query
    assert rc == 1
    err = capsys.readouterr().err
    assert "Search query cannot be blank" in err


def test_corrupt_json_recovery(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    # Write corrupt tasks.json
    bad = tmp_path / "tasks.json"
    bad.write_text("{ this is : not json }")
    # Listing should not raise; returns 0 and empty set
    rc = main(["list"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "No tasks" in out
    # Backup file should exist
    backups = list(tmp_path.glob("tasks.json.bak-*"))
    assert backups, "Expected backup of corrupt file"
