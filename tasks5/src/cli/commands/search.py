"""Search command implementation."""
from __future__ import annotations
import sys
import argparse

from src.services.search import search_tasks
from .common import load_tasks, print_tasks, print_error


def build_parser(subparsers) -> argparse.ArgumentParser:
    p = subparsers.add_parser("search", help="Search tasks by substring (title or description)")
    p.add_argument("query", help="Substring to search (case-insensitive)")
    return p


def run(args: argparse.Namespace, json_mode: bool) -> int:
    query = args.query
    if not isinstance(query, str) or not query.strip():
        print_error("Search query cannot be blank", json_mode)
        return 1
    tasks = load_tasks()
    matches = search_tasks(tasks, query)
    print_tasks(matches, json_mode)
    return 0
