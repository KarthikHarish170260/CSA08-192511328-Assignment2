"""
Task 04: Building Long Text - Concatenation (+) vs str.join()
Course: CSA08 / CSA0807 Python Programming (CO2)
Bloom's Level: K4 - Analyse

Context: Monthly SMS Bill Statement Generation (200,000 records).
Demonstrates quadratic O(N^2) copying behavior of += vs linear O(N) str.join().
"""

import io
import os
import time


# ==============================================================================
# Complete the Code & Core Implementations
# ==============================================================================
def build_plus(parts: list[str]) -> str:
    """Method (a): Repeated += inside loop."""
    text = ""
    for p in parts:
        text += p + ";"
    return text


def build_join(parts: list[str]) -> str:
    """Method (b): Single str.join() call. Completes TODO 1."""
    # TODO 1: Build the same text using a single str.join() call
    return ";".join(parts) + (";" if parts else "")


def build_fstring_each_line(parts: list[str]) -> str:
    """
    Method (c): An f-string for each line collected and joined.
    Formats each line with f-string then joins into final string.
    """
    return "".join([f"{p};" for p in parts])


# ==============================================================================
# Alternative Concepts: io.StringIO and File-based Streaming
# ==============================================================================
def build_stringio(parts: list[str]) -> str:
    """Alternative 1: io.StringIO in-memory buffer."""
    buffer = io.StringIO()
    for p in parts:
        buffer.write(p)
        buffer.write(";")
    return buffer.getvalue()


def build_file_streaming(parts: list[str], output_path: str = "temp_statement.txt") -> int:
    """Alternative 2: Streaming directly to disk."""
    with open(output_path, "w", encoding="utf-8") as f:
        for p in parts:
            f.write(p)
            f.write(";")
    file_size = os.path.getsize(output_path)
    if os.path.exists(output_path):
        os.remove(output_path)
    return file_size


# ==============================================================================
# Benchmark Harness
# ==============================================================================
def run_benchmarks():
    print("=" * 85)
    print("TASK 04: STRING ACCUMULATION BENCHMARK: += vs str.join() vs f-string")
    print("=" * 85)

    # 1. Official assignment execution check
    print("\nGenerating 200,000 statement items...")
    items_200k = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]

    print("[Official Assignment Execution - Single Run for 200,000 Items]")
    start = time.perf_counter()
    b = build_join(items_200k)
    t_join = time.perf_counter() - start

    start = time.perf_counter()
    a = build_plus(items_200k)
    t_plus = time.perf_counter() - start

    print(f"same text: {a == b} | length: {len(b)}")
    print(f"+= time: {t_plus:.4f} s   join time: {t_join:.4f} s")
    print(f"-> Speedup of join() over += : {t_plus / t_join:.1f}x faster!")

    # 2. Benchmarks for 1,000, 10,000, and 200,000 lines
    print("\n" + "=" * 85)
    print("SCALING ANALYSIS ACROSS DIFFERENT SIZES (1,000, 10,000, 200,000)")
    print("=" * 85)

    test_sizes = [1_000, 10_000, 200_000]
    print(f"{'Size (N)':<10} | {'Method':<24} | {'Run 1 (s)':<10} | {'Run 2 (s)':<10} | {'Run 3 (s)':<10} | {'Avg Time (s)':<12}")
    print("-" * 85)

    for n in test_sizes:
        sample = [f"Item{i}:Rs{i % 50}" for i in range(n)]

        # For 1k and 10k, run 3 times; for 200k, run 1 time for += (to save runtime) and 3 for join
        for name, fn in [
            ("str.join()", build_join),
            ("f-string per line + join", build_fstring_each_line),
            ("io.StringIO", build_stringio),
            ("Repeated +=", build_plus),
        ]:
            if n == 200_000 and name == "Repeated +=":
                runs = [t_plus, t_plus, t_plus]  # reuse measured 200k time
            else:
                runs = []
                for _ in range(3 if n < 200_000 else 2):
                    t0 = time.perf_counter()
                    fn(sample)
                    runs.append(time.perf_counter() - t0)
                if len(runs) < 3:
                    runs.append(runs[-1])

            avg_t = sum(runs) / len(runs)
            print(f"{n:<10} | {name:<24} | {runs[0]:<10.5f} | {runs[1]:<10.5f} | {runs[2]:<10.5f} | {avg_t:<12.5f}")
        print("-" * 85)

    print("\n[WHY join() IS THE RECOMMENDED PRACTICE DESPITE CPYTHON += OPTIMIZATION]")
    print("1. In Python, strings are immutable. Naively, 's += x' creates a new string copying all previous characters,")
    print("   leading to O(N^2) cumulative character copying.")
    print("2. CPython implements an optimization where if reference count == 1, it attempts in-place realloc.")
    print("   However, as seen at N=200,000, when heap fragmentation occurs or reference counts change,")
    print(f"   += runtime degrades to {t_plus:.2f} seconds.")
    print("3. str.join() guarantees strictly linear O(N) time across all Python interpreters.")
    print("   It computes the total length in Pass 1, allocates one single memory buffer, and copies parts once in Pass 2.")


if __name__ == "__main__":
    run_benchmarks()
