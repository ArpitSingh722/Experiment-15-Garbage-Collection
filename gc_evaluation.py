"""
Experiment No. 15 (CO-5)
Evaluate Python's automatic garbage collection mechanism by experimenting with
manual garbage collection using the gc module and analyzing its impact on
memory usage and performance.
"""

import gc
import time
import tracemalloc


class Node:
    """Sample node class capable of forming cyclic references."""

    def __init__(self, node_id: int) -> None:
        self.node_id = node_id
        self.payload = [i for i in range(100)]
        self.partner: "Node | None" = None


def create_cyclic_objects(num_pairs: int) -> None:
    """Creates pairs of Node objects referencing each other in cycles."""
    for i in range(num_pairs):
        a = Node(i)
        b = Node(i + 1)
        a.partner = b
        b.partner = a


def run_automatic_gc_benchmark(num_pairs: int) -> tuple[float, float, float]:
    """Runs object allocation with Python's automatic garbage collector enabled."""
    gc.enable()
    gc.collect()

    tracemalloc.start()
    start_time = time.perf_counter()

    create_cyclic_objects(num_pairs)

    elapsed = time.perf_counter() - start_time
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return elapsed, current_mem / (1024 * 1024), peak_mem / (1024 * 1024)


def run_manual_gc_benchmark(num_pairs: int) -> tuple[float, float, float, int]:
    """Disables automatic GC, allocates cyclic objects, and triggers manual gc.collect()."""
    gc.collect()
    gc.disable()

    tracemalloc.start()
    start_time = time.perf_counter()

    create_cyclic_objects(num_pairs)

    # Measure memory before manual collection
    before_collect_mem, _ = tracemalloc.get_traced_memory()

    # Manually invoke garbage collection across all generations
    collected_objects = gc.collect()

    elapsed = time.perf_counter() - start_time
    after_collect_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Re-enable automatic GC after benchmark
    gc.enable()

    return (
        elapsed,
        before_collect_mem / (1024 * 1024),
        after_collect_mem / (1024 * 1024),
        collected_objects,
    )


def main() -> None:
    num_pairs = 15_000

    print("=" * 65)
    print("Python Garbage Collection (gc) Memory & Performance Evaluation")
    print("=" * 65)
    print(f"Default GC Enabled    : {gc.isenabled()}")
    print(f"GC Thresholds (G0,1,2): {gc.get_threshold()}")
    print(f"Initial GC Counts     : {gc.get_count()}")
    print("-" * 65)

    # 1. Automatic Garbage Collection Benchmark
    auto_time, auto_curr_mb, auto_peak_mb = run_automatic_gc_benchmark(num_pairs)
    print("[1] Automatic Garbage Collection (gc.enable()):")
    print(f"    Execution Time        : {auto_time:.4f} seconds")
    print(f"    Current Memory Traced : {auto_curr_mb:.3f} MB")
    print(f"    Peak Memory Traced    : {auto_peak_mb:.3f} MB")
    print("-" * 65)

    # 2. Manual Garbage Collection Benchmark
    man_time, before_mb, after_mb, collected = run_manual_gc_benchmark(num_pairs)
    print("[2] Manual Garbage Collection (gc.disable() + gc.collect()):")
    print(f"    Execution Time (incl. manual collect) : {man_time:.4f} seconds")
    print(f"    Memory Before Manual gc.collect()     : {before_mb:.3f} MB")
    print(f"    Memory After Manual gc.collect()      : {after_mb:.3f} MB")
    print(f"    Unreachable Cyclic Objects Reclaimed  : {collected}")
    print("=" * 65)


if __name__ == "__main__":
    main()
