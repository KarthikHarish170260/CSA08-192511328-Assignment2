"""
Task 01: Decisions with Many Boundaries - State Electricity Subsidy Eligibility
Course: CSA08 / CSA0807 Python Programming (CO2)
Bloom's Level: K4 - Analyse

Rules:
- Units <= 100: Full Subsidy
- 101 <= Units <= 200: Partial Subsidy (ONLY if has ration card, else No Subsidy)
- Units > 200: No Subsidy (UNLESS member age > 80, receives Senior Special Subsidy)
"""

import time


# ==============================================================================
# 1. Implementation A: Flawed implementation using separate 'if' statements
# ==============================================================================
def subsidy_separate_if(units: int, has_ration_card: bool, has_senior_above_80: bool) -> list[str]:
    """
    Simulates the developer's buggy logic where independent 'if' statements
    are checked sequentially. Notice that if conditions are not mutually exclusive,
    a single household can qualify for multiple subsidies.
    """
    subsidies = []

    # Check 1: Low usage
    if units <= 100:
        subsidies.append("Full Subsidy")

    # Check 2: Ration card assistance (Flawed: written as units <= 200 instead of 101 <= units <= 200)
    # Even if written as separate if, non-exclusive conditions grant dual benefits.
    if units <= 200 and has_ration_card:
        subsidies.append("Partial Subsidy")

    # Check 3: Senior citizen assistance
    if units > 200 and has_senior_above_80:
        subsidies.append("Senior Special Subsidy")

    # Check 4: Ineligibility condition (separate if can overwrite or append)
    if not subsidies:
        subsidies.append("No Subsidy")

    return subsidies


# ==============================================================================
# 2. Implementation B: Correct implementation using if-elif-else with chained comparisons
# ==============================================================================
def subsidy_if_elif_else(units: int, has_ration_card: bool, has_senior_above_80: bool) -> str:
    """
    Correct mutually exclusive decision ladder using chained comparisons:
    101 <= units <= 200. Exactly one branch is guaranteed to execute.
    """
    if units <= 100:
        return "Full Subsidy"
    elif 101 <= units <= 200:
        if has_ration_card:
            return "Partial Subsidy"
        else:
            return "No Subsidy"
    else:  # units > 200
        if has_senior_above_80:
            return "Senior Special Subsidy"
        else:
            return "No Subsidy"


# ==============================================================================
# 3. Design Comparison: Nested if vs Combined Boolean conditions
# ==============================================================================
def subsidy_combined_boolean(units: int, has_ration_card: bool, has_senior_above_80: bool) -> str:
    """Flat structure using combined Boolean conditions (and / or)."""
    if units <= 100:
        return "Full Subsidy"
    elif (101 <= units <= 200) and has_ration_card:
        return "Partial Subsidy"
    elif units > 200 and has_senior_above_80:
        return "Senior Special Subsidy"
    else:
        return "No Subsidy"


# ==============================================================================
# 4. Alternative Concepts: match-case & Slab Lookup Table
# ==============================================================================
def subsidy_match_case(units: int, has_ration_card: bool, has_senior_above_80: bool) -> str:
    """Alternative 1: Python 3.10+ Pattern Matching with Guard Clauses."""
    match units:
        case u if u <= 100:
            return "Full Subsidy"
        case u if 101 <= u <= 200 and has_ration_card:
            return "Partial Subsidy"
        case u if u > 200 and has_senior_above_80:
            return "Senior Special Subsidy"
        case _:
            return "No Subsidy"


def subsidy_lookup_table(units: int, has_ration_card: bool, has_senior_above_80: bool) -> str:
    """
    Alternative 2: Table-driven lookup using sorted upper limits.
    Time complexity: O(k) for k slabs, Space: O(k) data structure.
    """
    slabs = [
        (100, lambda card, senior: "Full Subsidy"),
        (200, lambda card, senior: "Partial Subsidy" if card else "No Subsidy"),
        (float("inf"), lambda card, senior: "Senior Special Subsidy" if senior else "No Subsidy"),
    ]
    for limit, decision_fn in slabs:
        if units <= limit:
            return decision_fn(has_ration_card, has_senior_above_80)
    return "No Subsidy"


# ==============================================================================
# Test Harness & Boundary Verification
# ==============================================================================
def run_boundary_tests():
    print("=" * 85)
    print("TASK 01: STATE ELECTRICITY SUBSIDY ELIGIBILITY EVALUATION")
    print("=" * 85)

    # 8 distinct households covering all boundary values: 100, 101, 200, 201
    households = [
        # (ID, Units, RationCard, Senior80, Predicted Decision)
        ("H1", 50, False, False, "Full Subsidy (<= 100 units)"),
        ("H2 (Boundary 100)", 100, True, False, "Full Subsidy (Exact boundary <= 100)"),
        ("H3 (Boundary 101)", 101, True, False, "Partial Subsidy (101 <= units <= 200 with ration card)"),
        ("H4 (Boundary 101)", 101, False, False, "No Subsidy (101 <= units <= 200 without ration card)"),
        ("H5 (Boundary 200)", 200, True, False, "Partial Subsidy (Exact boundary 101 <= units <= 200)"),
        ("H6 (Boundary 200)", 200, False, False, "No Subsidy (Exact boundary 200 without ration card)"),
        ("H7 (Boundary 201)", 201, False, True, "Senior Special Subsidy (> 200 units with senior > 80)"),
        ("H8 (Boundary 201)", 201, True, False, "No Subsidy (> 200 units without senior; ration card invalid)"),
    ]

    print(f"{'HH ID':<18} | {'Units':<5} | {'Card':<5} | {'Snr':<5} | {'Predicted Decision':<32} | {'Separate if (Flawed)':<26} | {'if-elif-else (Correct)'}")
    print("-" * 125)

    for h_id, units, card, snr, predicted in households:
        res_separate = ", ".join(subsidy_separate_if(units, card, snr))
        res_elif = subsidy_if_elif_else(units, card, snr)
        print(f"{h_id:<18} | {units:<5} | {str(card):<5} | {str(snr):<5} | {predicted[:32]:<32} | {res_separate:<26} | {res_elif}")

    print("-" * 125)
    print("\n[KEY FINDING & ANALYSIS]")
    print("1. In H2 (100 units with ration card):")
    print("   - Separate if grants BOTH 'Full Subsidy' AND 'Partial Subsidy' because both if statements are evaluated independently.")
    print("   - if-elif-else grants ONLY 'Full Subsidy' because it short-circuits as soon as 'units <= 100' matches.")
    print("2. Chained comparison (101 <= units <= 200) prevents boundary leakage between adjacent slabs.")

    # Micro-benchmarks
    iterations = 100_000
    t0 = time.perf_counter()
    for _ in range(iterations):
        subsidy_if_elif_else(150, True, False)
    t_elif = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(iterations):
        subsidy_lookup_table(150, True, False)
    t_table = time.perf_counter() - t0

    print(f"\nBenchmark ({iterations:,} iterations at 150 units):")
    print(f"- if-elif-else Ladder Time : {t_elif:.4f} s (O(1) auxiliary space, direct bytecode jumps)")
    print(f"- Table Lookup Time        : {t_table:.4f} s (O(k) linear scan with lambda dispatch)")


if __name__ == "__main__":
    run_boundary_tests()
