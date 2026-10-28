"""
Task 03: Engineer a Vehicle Registration Number Validator
Course: CSA08 / CSA0807 Python Programming (CO2)
Bloom's Level: K4 - Analyse

Requirements:
- Only string operations (indexing, slicing, len, upper, replace, strip, isalpha, isdigit, split, join).
- No regular expressions in primary validator.
- Complete TODO 1 and TODO 2.
- Format valid receipt as 'TN 09 AB 1234'.
- Predict 6 inputs (including 2 invalid).
- Inquiries on immutability, text.upper(), s[-4:] and s[4:-4].
- Alternative concept: regex comparison and Big-O analysis.
"""

import re
import time


# ==============================================================================
# Complete the Code: TODO 1 & TODO 2
# ==============================================================================
def normalise(text: str) -> str:
    """'tn 09 ab 1234' -> 'TN09AB1234' (spaces and hyphens removed, upper case)."""
    # TODO 1: Remove spaces and hyphens and convert to upper case using string methods
    return text.replace(" ", "").replace("-", "").strip().upper()


def is_valid(reg: str) -> bool:
    """Valid form: 2 letters, 2 digits, 1 or 2 letters, 4 digits (e.g. TN09AB1234)."""
    # TODO 2: Check the length is 9 or 10, then check each part using slicing with
    #         isalpha() and isdigit()
    if len(reg) not in (9, 10):
        return False

    state = reg[:2]  # First 2 chars: State code (e.g., 'TN')
    district = reg[2:4]  # Next 2 chars: District code (e.g., '09')
    series = reg[4:-4]  # Chars between index 4 and last 4: Series (1 or 2 chars, e.g. 'AB' or 'M')
    number = reg[-4:]  # Last 4 chars: Vehicle number (e.g., '1234')

    return (
        state.isalpha()
        and district.isdigit()
        and series.isalpha()
        and number.isdigit()
    )


# ==============================================================================
# Additional Function: Format for Receipt
# ==============================================================================
def format_receipt(reg: str) -> str:
    """
    Formats a valid normalised vehicle number into standard toll receipt format:
    'TN 09 AB 1234' or 'KA 01 M 0007'.
    """
    if not is_valid(reg):
        return "INVALID_REGISTRATION"
    state = reg[:2]
    district = reg[2:4]
    series = reg[4:-4]
    number = reg[-4:]
    return f"{state} {district} {series} {number}"


# ==============================================================================
# Alternative Concept: Regular Expression Validator
# ==============================================================================
def is_valid_regex(reg: str) -> bool:
    """
    Alternative implementation using Python's 're' module.
    Pattern: 2 uppercase letters, 2 digits, 1-2 uppercase letters, 4 digits.
    Time Complexity: O(L) where L = len(reg).
    """
    pattern = r"^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$"
    return bool(re.fullmatch(pattern, reg))


# ==============================================================================
# Verification and Inquiry Demonstration
# ==============================================================================
def run_validator_tests():
    print("=" * 85)
    print("TASK 03: VEHICLE REGISTRATION NUMBER VALIDATOR (TOLL PLAZA)")
    print("=" * 85)

    # 1. Official assignment test cases from prompt
    print("\n[Official Assignment Test Cases from Prompt]:")
    for raw in ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]:
        reg = normalise(raw)
        status = "valid" if is_valid(reg) else "INVALID"
        print(f"{raw:15} -> {reg:11} {status}")

    # 2. Predicted 6 Test Cases (including 2 invalid)
    print("\n" + "=" * 85)
    print("PREDICTED 6 TEST CASES (WITH 2 INVALID CASES)")
    print("=" * 85)

    test_cases = [
        # (Input, Predicted Status, Predicted Normalised, Reason)
        ("tn 09 ab 1234", "VALID", "TN09AB1234", "Standard 10-char plate with spaces"),
        ("KA-01-M-0007", "VALID", "KA01M0007", "Single-letter series (9-char) with hyphens"),
        ("mh 12 pq 9999", "VALID", "MH12PQ9999", "Valid Maharashtra 10-char registration"),
        ("dl-04-c-1010", "VALID", "DL04C1010", "Valid Delhi 9-char single series with hyphens"),
        ("TN9AB1234", "INVALID", "TN9AB1234", "REJECT: Single-digit district (len 8, requires 2 digits)"),
        ("TN 22 1234 AB", "INVALID", "TN221234AB", "REJECT: Swapped series and digits (digits at series pos)"),
    ]

    print(f"{'Input Raw':<18} | {'Predicted':<10} | {'Observed':<10} | {'Normalised':<12} | {'Formatted Receipt':<16} | {'Match?'}")
    print("-" * 85)

    for raw, pred_status, pred_norm, reason in test_cases:
        norm = normalise(raw)
        valid = is_valid(norm)
        obs_status = "VALID" if valid else "INVALID"
        receipt = format_receipt(norm) if valid else "REJECTED"
        match = "PASS" if pred_status == obs_status and norm == pred_norm else "FAIL"
        print(f"{raw:<18} | {pred_status:<10} | {obs_status:<10} | {norm:<12} | {receipt:<16} | {match}")

    # 3. Inquiry Explanations & Slicing Demonstration
    print("\n" + "=" * 85)
    print("INQUIRY: NEGATIVE SLICING BEHAVIOR DEMONSTRATION")
    print("=" * 85)
    s9 = "KA01M0007"
    s10 = "TN09AB1234"
    print(f"9-character plate  : '{s9}'")
    print(f"  s[-4:]  (Number) : '{s9[-4:]}'  (Last 4 chars: indices 5,6,7,8)")
    print(f"  s[4:-4] (Series) : '{s9[4:-4]}'     (Slice from index 4 to 9-4=5: 1 character)")
    print(f"10-character plate : '{s10}'")
    print(f"  s[-4:]  (Number) : '{s10[-4:]}'  (Last 4 chars: indices 6,7,8,9)")
    print(f"  s[4:-4] (Series) : '{s10[4:-4]}'    (Slice from index 4 to 10-4=6: 2 characters)")
    print("Insight: Using s[4:-4] elegantly extracts the series whether length is 9 or 10 without branching!")

    # 4. Performance Comparison (Slicing vs Regular Expression)
    iterations = 50_000
    sample = "TN 09 AB 1234"
    norm_sample = normalise(sample)

    t0 = time.perf_counter()
    for _ in range(iterations):
        is_valid(norm_sample)
    t_slice = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(iterations):
        is_valid_regex(norm_sample)
    t_regex = time.perf_counter() - t0

    print(f"\nMicro-benchmark ({iterations:,} iterations):")
    print(f"- Slicing & isalpha/isdigit : {t_slice:.4f} s (Built-in C methods, zero overhead)")
    print(f"- Regular Expression (re)   : {t_regex:.4f} s (DFA state machine traversal)")


if __name__ == "__main__":
    run_validator_tests()
