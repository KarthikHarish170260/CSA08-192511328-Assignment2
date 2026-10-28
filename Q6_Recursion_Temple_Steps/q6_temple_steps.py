"""
Task 06: Recursion and Its Limits - Counting Ways to Climb Temple Steps
Course: CSA08 / CSA0807 Python Programming (CO2)
Bloom's Level: K5 - Evaluate

Context: A devotee climbs 1 or 2 steps at a time to reach the top of n steps.
Recurrence relation: W(n) = W(n-1) + W(n-2) with W(0) = 1, W(1) = 1.
"""

from functools import lru_cache
import sys
import time

calls = 0


# ==============================================================================
# 1. Plain (Naive) Recursive Implementation
# ==============================================================================
def ways_naive(n: int) -> int:
    """Ways to climb n temple steps taking 1 or 2 steps at a time."""
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)


# ==============================================================================
# 2. Memoised Recursive Implementation (Completing TODO 1)
# ==============================================================================
@lru_cache(maxsize=None)
def ways_memo(n: int) -> int:
    """
    TODO 1: Memoised recursive solution using @lru_cache.
    Stores previous results to prevent redundant subtree evaluations.
    """
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)


# ==============================================================================
# 3. Iterative Implementation (Alternative Concept & Production Solution)
# ==============================================================================
def ways_iterative(n: int) -> int:
    """
    Iterative bottom-up solution keeping only the last two values.
    Time Complexity: O(n)
    Space Complexity: O(1) auxiliary memory (no stack frames, no cache tables).
    """
    if n <= 1:
        return 1
    prev2, prev1 = 1, 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1


# ==============================================================================
# Call Tree for n = 5 (ASCII Visualization)
# ==============================================================================
CALL_TREE_N5 = """
Call Tree for ways_naive(5):
                         ways(5)
                     /             \\
              ways(4)               ways(3)*
             /       \\              /       \\
         ways(3)*    ways(2)*    ways(2)*   ways(1)
         /      \\    /     \\     /     \\
     ways(2)* ways(1) w(1) w(0) w(1)  w(0)
     /     \\
   w(1)   w(0)

[*] Marks redundant sub-evaluations:
- ways(3) is recomputed 2 times
- ways(2) is recomputed 3 times
- ways(1) is invoked 5 times
- ways(0) is invoked 3 times
Total calls = 15 calls for n=5; grows as O(phi^n) where phi approx. 1.618.
"""


# ==============================================================================
# Verification and Experiment Suite
# ==============================================================================
def run_temple_step_experiments():
    global calls
    print("=" * 85)
    print("TASK 06: TEMPLE STEPS CLIMBING - RECURSION, MEMOISATION & CALL LIMITS")
    print("=" * 85)

    # 1. Correctness Check: Hand Calculation vs Code (n = 1 to 6)
    print("\n[Correctness Verification: Hand Calculations vs Code (n = 1 to 6)]")
    hand_calculations = {
        1: (1, ["(1)"]),
        2: (2, ["(1+1)", "(2)"]),
        3: (3, ["(1+1+1)", "(1+2)", "(2+1)"]),
        4: (5, ["(1+1+1+1)", "(1+1+2)", "(1+2+1)", "(2+1+1)", "(2+2)"]),
        5: (8, ["(1+1+1+1+1)", "4 ways with one 2", "3 ways with two 2s"]),
        6: (13, ["Detailed combinations sum to 13"]),
    }

    print(f"{'n':<4} | {'Hand Calculated':<16} | {'ways_naive':<12} | {'ways_iterative':<16} | {'Status'}")
    print("-" * 65)
    for n_val in range(1, 7):
        hand_val, _ = hand_calculations[n_val]
        naive_val = ways_naive(n_val)
        iter_val = ways_iterative(n_val)
        status = "MATCH" if hand_val == naive_val == iter_val else "MISMATCH"
        print(f"{n_val:<4} | {hand_val:<16} | {naive_val:<12} | {iter_val:<16} | {status}")

    # 2. Official Assignment Execution Check (n = 25)
    print("\n" + "=" * 85)
    print("[Official Assignment Execution Check for n = 25]")
    ways_memo.cache_clear()
    calls = 0
    res_naive = ways_naive(25)
    c_naive = calls
    print(f"naive: {res_naive} calls = {c_naive}")

    calls = 0
    res_memo = ways_memo(25)
    c_memo = calls
    print(f"memo : {res_memo} calls = {c_memo}")

    # 3. Growth Investigation: n = 10, 20, 25, 30
    print("\n" + "=" * 85)
    print("GROWTH INVESTIGATION: NAIVE VS MEMOISED CALL COUNTS")
    print("=" * 85)
    print(f"{'n':<5} | {'Result W(n)':<14} | {'Predicted Naive (2W-1)':<24} | {'Actual Naive Calls':<20} | {'Predicted Memo (n+1)':<22} | {'Actual Memo Calls'}")
    print("-" * 105)

    test_ns = [10, 20, 25, 30]
    for n in test_ns:
        # Measure Naive
        calls = 0
        ans = ways_naive(n)
        actual_naive = calls
        predicted_naive = 2 * ans - 1

        # Measure Memo
        ways_memo.cache_clear()
        calls = 0
        ways_memo(n)
        actual_memo = calls
        predicted_memo = n + 1

        print(f"{n:<5} | {ans:<14} | {predicted_naive:<24} | {actual_naive:<20} | {predicted_memo:<22} | {actual_memo}")

    # 4. Display ASCII Call Tree
    print("\n" + "=" * 85)
    print(CALL_TREE_N5)

    # 5. Deployment Decision & Recursion Limit Investigation (n = 1000)
    print("=" * 85)
    print("DEPLOYMENT INVESTIGATION: n = 1000 & sys.getrecursionlimit()")
    print("=" * 85)
    current_limit = sys.getrecursionlimit()
    print(f"Current Python Recursion Limit : {current_limit}")

    # Clear cache and attempt n = 1000
    ways_memo.cache_clear()
    try:
        print("Attempting ways_memo(1000)...")
        ways_memo(1000)
    except RecursionError as e:
        print(f">> Caught Expected Exception: RecursionError ({e})")
        print(">> Cause: Maximum call stack depth (1,000 frames) was exceeded by recursive call chain.")

    # Execute Iterative for n = 1000
    t0 = time.perf_counter()
    ans_1000 = ways_iterative(1000)
    t_iter = time.perf_counter() - t0
    num_digits = len(str(ans_1000))
    print(f"\nIterative Solution for n = 1,000:")
    print(f">> Success! Calculated {num_digits}-digit result in {t_iter * 1000:.4f} ms.")
    print(f">> First 20 digits: {str(ans_1000)[:20]}... (Total {num_digits} digits)")
    print(f">> Auxiliary Stack Space: O(1) memory! Zero RecursionError risk.")

    print("\n[DEPLOYMENT DECISION DEFENSE]")
    print("1. Raising the recursion limit via sys.setrecursionlimit() is DANGEROUS in production because:")
    print("   - It risks an uncatchable OS-level C-stack overflow segmentation fault.")
    print("   - It consumes unnecessary memory for activation records on the heap/stack.")
    print("2. Rewriting with an iterative loop is the strictly superior engineering decision:")
    print("   - Eliminates call overhead entirely.")
    print("   - Reduces space complexity from O(n) to strictly O(1).")
    print("   - Safely scales to n = 100,000+ with zero crashes.")


if __name__ == "__main__":
    run_temple_step_experiments()
