# CSA0807 Python Programming – Assignment 2 (CO2)
**Course:** CSA08 / CSA0807 – Python Programming  
**Unit Coverage:** CO2 (Control Flow, String Operations, Functions, Recursion, and Scope)  
**Bloom’s Levels Assessed:** K3 – Apply, K4 – Analyse, K5 – Evaluate  
**Student Name:** V. Karthik Harish  
**Register Number:** 192511328
**Submission Date:** 30/10/2026  
**Python Version:** Python 3.14.3 (Compatible with Python 3.10+)  
**Repository Name:** `CSA08-192511328-Assignment2`

---

## 📋 Table of Contents
1. [Overview & Repository Layout](#-overview--repository-layout)
2. [Libraries and Environment](#-libraries-and-environment)
3. [Execution Guide & Commands](#-execution-guide--commands)
4. [Task Summary & Key Results](#-task-summary--key-results)
5. [Git Progressive Commit History](#-git-progressive-commit-history)

---

## 📁 Overview & Repository Layout

This repository contains full, working implementations for all 7 tasks of Assignment 2, including "Complete the Code" challenges, alternative concept implementations, empirical benchmarks, and the Day-4 Design Challenge.

```text
CSA08-192511328-Assignment2/
│
├── Q1_Electricity_Subsidy/
│   └── q1_subsidy.py                  # Task 01: Subsidy eligibility boundary analysis
│
├── Q2_OTP_Verification/
│   └── q2_otp_kiosk.py                # Task 02: OTP retry loop, loop-else & dynamic retry extension
│
├── Q3_Vehicle_Validator/
│   └── q3_vehicle_validator.py        # Task 03: String slicing & receipt formatter (no regex)
│
├── Q4_String_Building/
│   └── q4_statement_builder.py        # Task 04: += vs join() vs f-string empirical benchmark
│
├── Q5_Canteen_Scope/
│   └── q5_canteen_system.py           # Task 05: Mutable default fix, tuple return, scope demo
│
├── Q6_Recursion_Temple_Steps/
│   └── q6_temple_steps.py             # Task 06: Temple steps recursion, memoisation & call tree
│
├── Q7_Day4_Design_Challenge/
│   └── q7_design_challenge.py         # Task 07: Bottleneck diagnosis, sliding window DP redesign
│
├── run_all_tasks.py                   # Master test runner executing all tasks sequentially
├── requirements.txt                   # Environment specifications
├── .gitignore                         # Python cache/bytecode ignore rules
└── README.md                          # Repository documentation and verification guide
```

---

## 🛠 Libraries and Environment

This assignment strictly utilizes Python's built-in standard library, ensuring zero dependency setup issues across operating systems.

```text
# requirements.txt
python>=3.10
time          # Standard library (high-precision perf_counter)
sys           # Standard library (recursion limit, digit conversion)
functools     # Standard library (lru_cache)
tracemalloc   # Standard library (memory allocation tracking)
io            # Standard library (StringIO)
re            # Standard library (regex comparison baseline)
```

To verify Python installation:
```powershell
python --version
```

---

## 🚀 Execution Guide & Commands

Each task is self-contained and executable independently or via the master test runner.

### Run All Tasks Sequentially:
```powershell
python run_all_tasks.py
```

### Individual Task Commands:

| Task | Execution Command | Assessed Area |
| :--- | :--- | :--- |
| **Q1** | `python Q1_Electricity_Subsidy/q1_subsidy.py` | `if`, `if-else`, chained comparisons, match-case |
| **Q2** | `python Q2_OTP_Verification/q2_otp_kiosk.py` | `while`, `for`, `break`, `continue`, `pass`, `loop-else` |
| **Q3** | `python Q3_Vehicle_Validator/q3_vehicle_validator.py` | Slicing (`s[-4:]`, `s[4:-4]`), string methods, immutability |
| **Q4** | `python Q4_String_Building/q4_statement_builder.py` | String concatenation (`+=`) vs `str.join()`, CPython `realloc` |
| **Q5** | `python Q5_Canteen_Scope/q5_canteen_system.py` | Mutable default parameter bug (`__defaults__`), local/global/nonlocal |
| **Q6** | `python Q6_Recursion_Temple_Steps/q6_temple_steps.py` | Plain recursion, memoisation (`@lru_cache`), call limits |
| **Q7** | `python Q7_Day4_Design_Challenge/q7_design_challenge.py` | Diagnose, Redesign (Sliding Window DP & Matrix Exp), Validate |

---

## 📊 Task Summary & Key Results

### Q1: Decisions with Many Boundaries (K4 – Analyse)
- **Problem:** Electricity subsidy eligibility with boundaries at 100, 101, 200, 201 units.
- **Bug Diagnosed:** Independent `if` statements evaluate sequentially. A household consuming 100 units with a ration card qualified for *both* "Full Subsidy" and "Partial Subsidy".
- **Fix:** Implemented mutually exclusive `if-elif-else` ladder with chained comparisons (`101 <= units <= 200`).
- **Result:** Exactly 1 subsidy tier awarded per household. At 150 units, `if-elif-else` executes in **0.0057 s** for 100,000 iterations ($O(1)$ space).

### Q2: Loops that Count Attempts (K3 – Apply)
- **Problem:** Bank kiosk OTP verification (3 attempts, blank entries ignored, lock account on 3 failures).
- **Control Flow:** `continue` skips blank entries without incrementing `attempts`; `break` exits on valid OTP; `loop-else` fires strictly when all attempts are exhausted.
- **Changed Condition:** When a security question grants 2 extra attempts, `while` dynamically increments `max_attempts += 2` seamlessly, whereas a `for i in range(3)` iterator cannot be modified during iteration.

### Q3: Toll Plaza Vehicle Registration Validator (K4 – Analyse)
- **Problem:** Validate and format vehicle plates (e.g., `tn 09 ab 1234` $\to$ `TN 09 AB 1234`) using only string methods and slicing.
- **Key Technique:** Evaluated series using negative slicing `reg[4:-4]` and number using `reg[-4:]`. This elegantly handles both 9-character (`KA01M0007`) and 10-character (`TN09AB1234`) plates without conditional branching.
- **Result:** Successfully validated and rejected all 6 predicted test cases; matched official assignment output format.

### Q4: Building Long Text: + vs join() (K4 – Analyse)
- **Problem:** Generating monthly SMS statements for 200,000 items.
- **Key Finding:**
  - `str.join()` completed in **0.0031 s** ($O(N)$ linear time, single pre-sized buffer allocation).
  - Repeated `+=` took **0.2589 s** (82.4x slower) due to CPython heap fragmentation and buffer re-allocations.
  - Explanation: Strings are immutable in Python. Although CPython optimizes `+=` when `ob_refcnt == 1`, `join()` remains best practice because it guarantees $O(N)$ across all Python runtimes.

### Q5: Functions, Parameters and Scope (K4 – Analyse)
- **Problem:** College canteen order system leaking previous customer items (`order=[]`).
- **Bug Diagnosed:** Default parameters are evaluated *once* at function definition time and stored in `add_item_buggy.__defaults__`. Modifying a mutable default list persists across all calls.
- **Fix:** Used sentinel `order=None` and instantiated `order = []` dynamically inside the call frame.
- **Result:** Verified 3 sequential customers with completely independent orders and demonstrated tuple unpacking for multiple return values (`subtotal, gst, total`).

### Q6: Recursion and Its Limits (K5 – Evaluate)
- **Problem:** Temple step climbing ($W(n) = W(n-1) + W(n-2)$).
- **Key Finding:**
  - For $n = 25$: Naive took **242,785 calls**; Memoised took **26 calls** (matches expected prompt output).
  - Calling `ways_memo(1000)` triggered `RecursionError: maximum recursion depth exceeded` (`sys.getrecursionlimit() = 1000`).
  - Deployment Decision: Iterative loop is chosen over raising `sys.setrecursionlimit()` because it avoids OS C-stack overflows, eliminates cache overhead, and reduces space from $O(n)$ to $O(1)$.

### Q7: Day-4 Design Challenge – Diagnose, Redesign and Validate (K5 – Evaluate)
- **Problem Selected:** Q6 (Staircase / Temple Steps Climbing).
- **Diagnosis:** Plain recursion exhibits exponential explosion ($O(1.618^n)$). Memoised recursion triggers fatal `RecursionError` at $n = 1000$ due to call stack limit and consumes $O(n)$ cache heap memory.
- **Redesign:** Bottom-up Dynamic Programming with Markovian State Reduction (2-variable sliding window), and an $O(\log n)$ matrix exponentiation engine.
- **Validation:**
  - Successfully computed $n = 100,000$ in **0.0600 seconds** (20,899 digits).
  - Memory footprint tracked via `tracemalloc`: Peak auxiliary RAM was only **2,868 bytes** ($O(1)$ scalar state).
  - Zero `RecursionError`, zero crashes.

---

## 📜 Git Progressive Commit History

The project repository was committed progressively following standard development workflows:

1. `Initial project setup: directory layout, requirements.txt, .gitignore, README.md`
2. `Task 01: State electricity subsidy eligibility with separate if vs if-elif-else boundary analysis`
3. `Task 02: OTP verification kiosk with while vs for loops, loop-else, and dynamic retry extension`
4. `Task 03: Toll plaza vehicle number validator using string operations and negative slicing`
5. `Task 04: Monthly SMS statement string builder benchmark (+ vs join vs f-string)`
6. `Task 05: College canteen order system resolving mutable default parameter and demonstrating scope`
7. `Task 06: Temple steps staircase climbing recursion, call tree, and memoisation analysis`
8. `Task 07: Day-4 Design Challenge - Bottleneck diagnosis, iterative redesign, and empirical validation`
9. `Final: Master test runner and execution verification`
