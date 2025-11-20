import json
from src.cli.main import main


def create(title, description=None, status=None):
    args = ["create", "--title", title]
    if description:
        args += ["--description", description]
    if status:
        args += ["--status", status]
    rc = main(args)
    assert rc == 0


def test_cli_search_finds_title_and_description(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    create("Write spec", "Initial MVP")
    create("Refactor code", "Improve clarity", "in-progress")
    create("Test Search")
    capsys.readouterr()  # clear creation output
    rc = main(["search", "spec"])  # title match
    assert rc == 0
    out = capsys.readouterr().out
    assert "Write spec" in out

    rc = main(["search", "clar"])  # description match
    assert rc == 0
    out = capsys.readouterr().out
    assert "Refactor code" in out

    rc = main(["search", "SEARCH"])  # case-insensitive title match
    assert rc == 0
    out = capsys.readouterr().out
    assert "Test Search" in out


def test_cli_search_no_matches(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    create("Alpha")
    capsys.readouterr()
    rc = main(["search", "zzz"])  # no match
    assert rc == 0
    out = capsys.readouterr().out
    assert "No tasks" in out or "No matching" in out


def test_cli_search_blank_query_error(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    rc = main(["search", ""])  # blank query should error
    assert rc == 1
    captured = capsys.readouterr()
    assert "Search query cannot be blank" in captured.err
