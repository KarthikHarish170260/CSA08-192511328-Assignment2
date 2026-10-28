"""
Task 02: Loops that Count Attempts - OTP Verification at a Bank Kiosk
Course: CSA08 / CSA0807 Python Programming (CO2)
Bloom's Level: K3 - Apply

Rules:
- Max 3 attempts for OTP.
- Blank entry does NOT count as an attempt.
- 3 failed attempts locks account for 30 minutes (handled via loop-else).
- Changed condition: 2 extra attempts if security question is answered correctly.
"""

from typing import Iterator


# ==============================================================================
# 1. Implementation A: Using while Loop (Natural condition-driven structure)
# ==============================================================================
def otp_kiosk_while(correct_otp: str, input_stream: Iterator[str]) -> str:
    """
    Simulates OTP verification with a while loop.
    Demonstrates: break, continue, pass, and loop-else.
    """
    attempts = 0
    max_attempts = 3

    print("\n--- Starting While-Loop OTP Verification ---")
    while attempts < max_attempts:
        try:
            entry = next(input_stream)
        except StopIteration:
            break

        # Check for blank entry: Must NOT count as an attempt
        cleaned_entry = entry.strip()
        if not cleaned_entry:
            # pass acts as an explicit placeholder (e.g. for future telemetry/logging hook)
            pass
            print("  [Input: Blank] Blank entry detected. Ignored; please enter a valid OTP.")
            continue  # Skips loop remainder; attempts counter is NOT incremented!

        # Check if OTP matches
        if cleaned_entry == correct_otp:
            print(f"  [Input: '{cleaned_entry}'] Success! OTP verified on attempt #{attempts + 1}.")
            break  # Exits loop immediately; skips the 'else' block!
        else:
            attempts += 1
            remaining = max_attempts - attempts
            print(f"  [Input: '{cleaned_entry}'] Incorrect OTP! Attempts used: {attempts}/{max_attempts}. Remaining: {remaining}")
    else:
        # Loop-else: Executes ONLY if the loop finishes without encountering a 'break'
        print("  >> [SECURITY ALERT] Account locked for 30 minutes due to 3 failed attempts.")
        return "LOCKED"

    return "GRANTED"


# ==============================================================================
# 2. Implementation B: Using for Loop with range(3)
# ==============================================================================
def otp_kiosk_for(correct_otp: str, input_stream: Iterator[str]) -> str:
    """
    Simulates OTP verification with a for loop.
    Note: In Python, `for i in range(3)` advances the counter unconditionally.
    To avoid counting blank entries, we must consume blank entries using an inner loop,
    or use while. Here we illustrate the structural rigidity of for-range.
    """
    print("\n--- Starting For-Loop OTP Verification ---")
    for attempt in range(1, 4):
        # We must repeatedly pull inputs until a non-blank entry is obtained
        while True:
            try:
                raw_input = next(input_stream)
            except StopIteration:
                return "STREAM_ENDED"
            if raw_input.strip():
                entry = raw_input.strip()
                break
            else:
                pass  # Placeholder
                print("  [Input: Blank] Blank entry detected in for-loop. Ignored.")
                continue

        if entry == correct_otp:
            print(f"  [Input: '{entry}'] Success! OTP verified on attempt #{attempt}.")
            break
        else:
            remaining = 3 - attempt
            print(f"  [Input: '{entry}'] Incorrect OTP! Attempts used: {attempt}/3. Remaining: {remaining}")
    else:
        print("  >> [SECURITY ALERT] Account locked for 30 minutes due to 3 failed attempts.")
        return "LOCKED"

    return "GRANTED"


# ==============================================================================
# 3. Changed Condition: 2 Extra Attempts via Security Question
# ==============================================================================
def otp_kiosk_dynamic(correct_otp: str, input_stream: Iterator[str], security_answer: str, user_sec_input: str) -> str:
    """
    Demonstrates why 'while' is far more natural when conditions change dynamically.
    If 3 attempts fail, an interactive security challenge can grant 2 bonus attempts.
    """
    attempts = 0
    max_attempts = 3
    security_prompted = False

    print("\n--- Starting Dynamic While-Loop (with Security Question Extension) ---")
    while attempts < max_attempts:
        try:
            entry = next(input_stream)
        except StopIteration:
            break

        cleaned = entry.strip()
        if not cleaned:
            continue

        if cleaned == correct_otp:
            print(f"  [Success] OTP verified on attempt #{attempts + 1}!")
            break
        else:
            attempts += 1
            print(f"  [Failed] Attempt {attempts}/{max_attempts} exhausted.")

            # If initial 3 attempts are exhausted and challenge has not been offered
            if attempts == max_attempts and not security_prompted:
                security_prompted = True
                print("  >> Initial 3 attempts failed. Prompting Security Question: 'What is your mother's maiden name?'")
                if user_sec_input.strip().lower() == security_answer.lower():
                    max_attempts += 2  # Dynamically extend boundary!
                    print(f"  >> Security Answer Verified! 2 Extra attempts granted. New limit: {max_attempts}.")
                else:
                    print("  >> Security Answer Incorrect.")
    else:
        print(f"  >> [SECURITY ALERT] All {max_attempts} attempts failed. Account locked for 30 minutes.")
        return "LOCKED"

    return "GRANTED"


# ==============================================================================
# 4. Alternative Concept: Recursive OTP Verification
# ==============================================================================
def otp_kiosk_recursive(correct_otp: str, input_stream: Iterator[str], attempt: int = 0, max_attempts: int = 3) -> str:
    """
    Alternative: Recursive approach without loops.
    Time Complexity: O(a) where a is number of attempts.
    Space Complexity: O(a) call stack frames (vs O(1) for loops).
    """
    if attempt >= max_attempts:
        print("  >> [RECURSIVE SECURITY ALERT] Account locked for 30 minutes.")
        return "LOCKED"

    try:
        raw = next(input_stream)
    except StopIteration:
        return "STREAM_ENDED"

    cleaned = raw.strip()
    if not cleaned:
        # Blank entry does not consume an attempt; recurse with same attempt count
        return otp_kiosk_recursive(correct_otp, input_stream, attempt, max_attempts)

    if cleaned == correct_otp:
        print(f"  [Recursive Success] Verified on attempt #{attempt + 1}.")
        return "GRANTED"
    else:
        print(f"  [Recursive Fail] Wrong OTP. Attempt {attempt + 1}/{max_attempts} used.")
        return otp_kiosk_recursive(correct_otp, input_stream, attempt + 1, max_attempts)


# ==============================================================================
# Verification Suite
# ==============================================================================
def run_tests():
    CORRECT_OTP = "482910"

    print("=" * 80)
    print("SCENARIO 1: While Loop with 2 Blank Entries, 1 Wrong, then Correct OTP")
    print("=" * 80)
    inputs_1 = iter(["", "   ", "999999", "482910"])
    res1 = otp_kiosk_while(CORRECT_OTP, inputs_1)
    print("Result:", res1)

    print("\n" + "=" * 80)
    print("SCENARIO 2: While Loop with 3 Consecutive Wrong Entries (Account Lockout)")
    print("=" * 80)
    inputs_2 = iter(["111111", "222222", "333333"])
    res2 = otp_kiosk_while(CORRECT_OTP, inputs_2)
    print("Result:", res2)

    print("\n" + "=" * 80)
    print("SCENARIO 3: Changed Condition - Security Question grants 2 extra attempts")
    print("=" * 80)
    # 3 wrong attempts, then correct security answer ("Sharma"), then succeeds on 4th attempt
    inputs_3 = iter(["000001", "000002", "000003", "482910"])
    res3 = otp_kiosk_dynamic(CORRECT_OTP, inputs_3, security_answer="Sharma", user_sec_input="Sharma")
    print("Result:", res3)

    print("\n" + "=" * 80)
    print("SCENARIO 4: Recursive Alternative Execution")
    print("=" * 80)
    inputs_4 = iter(["", "123456", "482910"])
    res4 = otp_kiosk_recursive(CORRECT_OTP, inputs_4)
    print("Result:", res4)


if __name__ == "__main__":
    run_tests()
