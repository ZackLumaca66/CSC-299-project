"""CLI entrypoint wiring subcommands."""
from __future__ import annotations
import argparse
import sys

from src.cli.args_base import build_base_parser
from src.cli.logging_setup import configure_logging
from src.cli.commands import create as create_cmd
from src.cli.commands import list as list_cmd
from src.cli.commands import search as search_cmd


def build_parser() -> argparse.ArgumentParser:
    parser = build_base_parser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    create_cmd.build_parser(subparsers)
    list_cmd.build_parser(subparsers)
    search_cmd.build_parser(subparsers)
    return parser


def dispatch(args: argparse.Namespace) -> int:
    json_mode = getattr(args, "json", False)
    if args.command == "create":
        return create_cmd.run(args, json_mode=json_mode)
    if args.command == "list":
        return list_cmd.run(args, json_mode=json_mode)
    if args.command == "search":
        return search_cmd.run(args, json_mode=json_mode)
    print("Unknown command", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    parser = build_parser()
    args = parser.parse_args(argv)
    return dispatch(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())