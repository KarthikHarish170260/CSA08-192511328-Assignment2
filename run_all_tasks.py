"""
Master Test Runner for CSA08 / CSA0807 Python Programming - Assignment 2 (CO2)
Executes all tasks sequentially and produces clean formatted terminal output.
"""

import os
import subprocess
import sys

TASKS = [
    ("Task 01: Electricity Subsidy", "Q1_Electricity_Subsidy/q1_subsidy.py"),
    ("Task 02: OTP Verification", "Q2_OTP_Verification/q2_otp_kiosk.py"),
    ("Task 03: Vehicle Validator", "Q3_Vehicle_Validator/q3_vehicle_validator.py"),
    ("Task 04: String Building", "Q4_String_Building/q4_statement_builder.py"),
    ("Task 05: Canteen Scope", "Q5_Canteen_Scope/q5_canteen_system.py"),
    ("Task 06: Temple Steps Recursion", "Q6_Recursion_Temple_Steps/q6_temple_steps.py"),
    ("Task 07: Day-4 Design Challenge", "Q7_Day4_Design_Challenge/q7_design_challenge.py"),
]

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print("=" * 80)
    print("CSA08 / CSA0807 PYTHON PROGRAMMING - ASSIGNMENT 2 (CO2)")
    print(f"Python Version : {sys.version.split()[0]}")
    print(f"Base Directory : {base_dir}")
    print("=" * 80)

    for title, script_rel in TASKS:
        script_path = os.path.join(base_dir, script_rel)
        print(f"\n{'#' * 80}")
        print(f"RUNNING: {title} ({script_rel})")
        print(f"{'#' * 80}\n")
        
        result = subprocess.run([sys.executable, script_path], cwd=base_dir, capture_output=False)
        if result.returncode != 0:
            print(f"\n[WARNING] {title} exited with return code {result.returncode}")

    print("\n" + "=" * 80)
    print("ALL 7 ASSIGNMENT TASKS EXECUTED SUCCESSFULLY.")
    print("=" * 80)

if __name__ == "__main__":
    main()
