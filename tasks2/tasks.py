#!/usr/bin/env python3
"""
tasks2: Enhanced prototype command-line task manager.

Adds:
- complete <id>: mark a task as completed
- delete <id>: delete a task by id
- list [--status all|pending|completed]
- search <term>

Data is stored in tasks.json in this directory.
"""
import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

DATA_FILE = Path(__file__).with_name("tasks.json")

def load_tasks(path: Path = DATA_FILE) -> List[Dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Warning: '{path.name}' contains invalid JSON. Starting with an empty list.")
        return []

def save_tasks(tasks: List[Dict[str, Any]], path: Path = DATA_FILE) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)

def next_id(tasks: List[Dict[str, Any]]) -> int:
    return max([t.get("id", 0) for t in tasks] + [0]) + 1


def add_task(description: str, path: Path = DATA_FILE) -> None:
    tasks = load_tasks(path)
    tid = next_id(tasks)
    tasks.append({"id": tid, "description": description, "status": "pending"})
    save_tasks(tasks, path)
    print(f'Added task {tid}: "{description}"')


def list_tasks(status: str = "all", path: Path = DATA_FILE) -> None:
    tasks = load_tasks(path)
    filtered = tasks if status == "all" else [t for t in tasks if t.get("status") == status]
    if not filtered:
        print("No tasks found.")
        return
    print("--- Task List ---")
    for t in filtered:
        print(f"  [{t.get('id','N/A')}] {t.get('description','')} ({t.get('status','unknown')})")
    print("-----------------")

def search_tasks(term: str, path: Path = DATA_FILE) -> None:
    tasks = load_tasks(path)
    matches = [t for t in tasks if term.lower() in t.get("description", "").lower()]
    if not matches:
        print(f'No tasks found matching "{term}".')
        return
    print(f'--- Search Results for "{term}" ---')
    for t in matches:
        print(f"  [{t.get('id','N/A')}] {t.get('description','')} ({t.get('status','unknown')})")
    print("-----------------")

def complete_task(tid: int, path: Path = DATA_FILE) -> None:
    tasks = load_tasks(path)
    for t in tasks:
        if t.get("id") == tid:
            if t.get("status") == "completed":
                print(f"Task {tid} is already completed.")
            else:
                t["status"] = "completed"
                print(f"Marked task {tid} as completed.")
            save_tasks(tasks, path)
            return
    print(f"Task {tid} not found.")

def delete_task(tid: int, path: Path = DATA_FILE) -> None:
    tasks = load_tasks(path)
    new_tasks = [t for t in tasks if t.get("id") != tid]
    if len(new_tasks) == len(tasks):
        print(f"Task {tid} not found.")
        return
    save_tasks(new_tasks, path)
    print(f"Deleted task {tid}.")

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="tasks2 CLI task manager")
    sub = p.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("description", nargs=argparse.REMAINDER, help="Task description")

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--status", choices=["all", "pending", "completed"], default="all")

    p_search = sub.add_parser("search", help="Search tasks")
    p_search.add_argument("term", help="Search term")

    p_complete = sub.add_parser("complete", help="Complete a task")
    p_complete.add_argument("id", type=int, help="Task id")

    p_delete = sub.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", type=int, help="Task id")
    return p

def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    ns = parser.parse_args(argv)
    if ns.command == "add":
        desc = " ".join(ns.description).strip()
        if not desc:
            print("Error: description cannot be empty.")
            return
        add_task(desc)
    elif ns.command == "list":
        list_tasks(ns.status)
    elif ns.command == "search":
        search_tasks(ns.term)
    elif ns.command == "complete":
        complete_task(ns.id)
    elif ns.command == "delete":
        delete_task(ns.id)

if __name__ == "__main__":
    main()