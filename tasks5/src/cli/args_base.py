"""Base argparse setup with global flags."""
from __future__ import annotations
import argparse


def build_base_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tasks", description="Task manager CLI")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of human-readable format")
    return parser