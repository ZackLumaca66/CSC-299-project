"""List command implementation."""
from __future__ import annotations
import argparse
from src.services.filtering import filter_by_status
from .common import load_tasks, print_tasks


def build_parser(subparsers) -> argparse.ArgumentParser:
    p = subparsers.add_parser("list", help="List tasks optionally filtered by status")
    p.add_argument("--status", required=False, help="Filter by status")
    return p


def run(args: argparse.Namespace, json_mode: bool) -> int:
    tasks = load_tasks()
    filtered = filter_by_status(tasks, args.status)
    print_tasks(filtered, json_mode)
    return 0