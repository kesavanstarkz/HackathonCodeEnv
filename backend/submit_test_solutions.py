#!/usr/bin/env python
"""
Submit a correct and incorrect solution to assignment ID 4 and print results.
Run:
    python submit_test_solutions.py
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE = os.getenv("BASE_URL", "http://127.0.0.1:8000")
ASSIGNMENT_ID = int(os.getenv("TEST_ASSIGNMENT_ID", "4"))

# Correct solution (reads two ints and prints sum)
correct_code = """
import sys
data = sys.stdin.read().strip().split()
if not data:
    print(0)
else:
    a, b = map(int, data[:2])
    print(a + b)
"""

# Incorrect solution (prints product)
incorrect_code = """
import sys
data = sys.stdin.read().strip().split()
if not data:
    print(0)
else:
    a, b = map(int, data[:2])
    print(a * b)
"""

def submit(code, label):
    payload = {
        "assignment_id": ASSIGNMENT_ID,
        "code": code
    }
    print(f"\nSubmitting {label} solution to assignment {ASSIGNMENT_ID}...")
    r = requests.post(f"{BASE}/assignments/submit-code", json=payload, timeout=15)
    print("Status:", r.status_code)
    try:
        data = r.json()
    except Exception as e:
        print("Failed to parse JSON response:", e)
        print(r.text)
        return

    # Pretty print results
    print("Response JSON:", data)
    if data.get("success") is not None:
        print("Overall success:", data.get("success"))
    if "total_tests" in data:
        print(f"Passed {data.get('passed_tests')}/{data.get('total_tests')}")
    if "results" in data:
        for i, t in enumerate(data["results"], start=1):
            # t may be a dict with varying keys depending on executor
            if isinstance(t, dict):
                # print a safe summary
                status = t.get("status") or t.get("result") or t.get("pass")
                expected = t.get("expected") or t.get("expected_output")
                got = t.get("got") or t.get("output") or t.get("actual")
                print(f" Test {i}: {status} - expected={expected}, got={got}")
            else:
                print(f" Test {i}: {t}")
    if data.get("code_error"):
        print("Code error:\n", data.get("code_error"))

if __name__ == '__main__':
    submit(correct_code, "CORRECT")
    submit(incorrect_code, "INCORRECT")
