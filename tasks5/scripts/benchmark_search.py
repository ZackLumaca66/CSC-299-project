"""Benchmark script for list/search performance.

Generates synthetic tasks (unless at or above target) then measures median
timings for list and search operations over multiple iterations.

Usage (PowerShell):
  python scripts/benchmark_search.py --target 5000 --query spec --iterations 10
"""
from __future__ import annotations
import json, time, random, string, pathlib, argparse, statistics

DATA_FILE = pathlib.Path("tasks.json")


def load_tasks():
    if not DATA_FILE.exists():
        return []
    data = json.loads(DATA_FILE.read_text())
    return data.get("tasks", [])


def synthesize_if_needed(target: int) -> None:
    if not DATA_FILE.exists():
        DATA_FILE.write_text(json.dumps({"schema_version": 1, "tasks": []}, indent=2))
    data = json.loads(DATA_FILE.read_text())
    tasks = data.get("tasks", [])
    if len(tasks) >= target:
        return
    next_id = (max([t["id"] for t in tasks], default=0) + 1) if tasks else 1
    remaining = target - len(tasks)
    for _ in range(remaining):
        title = "Task " + ''.join(random.choices(string.ascii_lowercase, k=8))
        tasks.append({"id": next_id, "title": title, "description": "desc", "status": "todo"})
        next_id += 1
    data["tasks"] = tasks
    DATA_FILE.write_text(json.dumps(data))


def time_list_and_search(tasks: list[dict], query: str) -> tuple[float, float, int]:
    start_list = time.perf_counter()
    _ = list(tasks)
    list_time = (time.perf_counter() - start_list) * 1000
    start_search = time.perf_counter()
    lowered = query.lower()
    results = [t for t in tasks if lowered in t["title"].lower() or lowered in (t.get("description") or "").lower()]
    search_time = (time.perf_counter() - start_search) * 1000
    return list_time, search_time, len(results)


def benchmark(target: int, query: str, iterations: int) -> None:
    synthesize_if_needed(target)
    tasks = load_tasks()
    list_times = []
    search_times = []
    matches = 0
    for _ in range(iterations):
        lt, st, m = time_list_and_search(tasks, query)
        list_times.append(lt)
        search_times.append(st)
        matches = m
    print(
        f"Tasks: {len(tasks)} | Query: '{query}' | Matches: {matches}\n"
        f"List median: {statistics.median(list_times):.2f} ms | Search median: {statistics.median(search_times):.2f} ms"
    )


def parse_args():
    p = argparse.ArgumentParser(description="Benchmark list/search performance")
    p.add_argument("--target", type=int, default=5000, help="Target number of tasks to synthesize")
    p.add_argument("--query", type=str, default="spec", help="Search query to benchmark")
    p.add_argument("--iterations", type=int, default=5, help="Iterations for timing")
    return p.parse_args()


if __name__ == "__main__":  # pragma: no cover
    args = parse_args()
    benchmark(args.target, args.query, args.iterations)
