import json
from src.cli.main import main


def create(title, description=None, status=None):
    args = ["--json", "create", "--title", title]
    if description:
        args += ["--description", description]
    if status:
        args += ["--status", status]
    rc = main(args)
    assert rc == 0


def test_cli_search_json_matches(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    create("Write spec", "Initial MVP")
    create("Refactor code", "Improve clarity", "in-progress")
    capsys.readouterr()
    rc = main(["--json", "search", "spec"])  # title
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    titles = {t["title"] for t in data["tasks"]}
    assert "Write spec" in titles

    rc = main(["--json", "search", "clar"])  # description
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    titles = {t["title"] for t in data["tasks"]}
    assert "Refactor code" in titles


def test_cli_search_json_empty(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    rc = main(["--json", "search", "nonefound"])  # no tasks yet
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    assert data["tasks"] == []


def test_cli_search_json_blank_query_error(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    rc = main(["--json", "search", ""])  # blank query
    assert rc == 1
    raw = capsys.readouterr().out
    data = json.loads(raw)
    assert data["error"]["message"].startswith("Search query cannot be blank")
