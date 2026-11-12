import time
import tracemalloc
from search_engines import solve
from puzzle_board import GOAL_STATE


def run_profile(start, algorithm, heuristic):
    tracemalloc.start()
    started = time.perf_counter()
    try:
        path, expanded, generated = solve(start, algorithm, heuristic)
        elapsed = time.perf_counter() - started
        _, peak_memory = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    return {
        "path": path,
        "moves": len(path) - 1 if path else None,
        "expanded": expanded,
        "generated": generated,
        "time_seconds": round(elapsed, 6),
        "peak_memory_kb": round(peak_memory / 1024, 2),
        "goal": list(GOAL_STATE)
    }
